#!/usr/bin/env python3
"""
Technogym MYRUN - controlled incline diagnostic test

Purpose:
- connect via BLE
- perform the same QZ-style initialization used by qdomyos-zwift
- take baseline STATUS / RADCEXT / DUMPIO
- send FTMS START/RESUME without setting a belt speed
- verify controller state
- request a small incline via FTMS (default +2.0 %)
- immediately sample DUMPIO / STATUS / RADCEXT several times
- request 0.0 % again
- send FTMS STOP/PAUSE
- take final samples
- write everything as a readable report

Install:
    python3 -m pip install --user bleak

Run:
    python3 myrun_incline_test.py

Optional:
    python3 myrun_incline_test.py --address E0:86:1D:FA:4D:A0
    python3 myrun_incline_test.py --target 1.0
    python3 myrun_incline_test.py --output incline_test.txt

Safety:
- nobody should stand on the belt during this test
- the script does NOT set a speed, but START/RESUME is a real FTMS control command
- STOP/PAUSE is sent in a finally block after START/RESUME whenever possible
"""

import argparse
import asyncio
from datetime import datetime
from pathlib import Path
import struct
import sys

from bleak import BleakClient, BleakScanner

FTMS_CONTROL_POINT = "00002ad9-0000-1000-8000-00805f9b34fb"

TG_WRITE = "df1eb8e4-1753-4bb9-a6a6-e018040af0a3"
TG_NOTIFY = "6f26de4b-dcef-4459-9465-931f1b144c20"

# QZ-style MYRUN initialization, confirmed working on the test machine.
QZ_FTMS_INIT = bytes.fromhex("00 93 F0 51 E8 1B 42 92 8E")
INIT_COMMANDS = [
    "@DISABLE_PACE#",
    "@SSIUNITS#",
    "@RJSK_EN 1#",
    "@LJSK_EN 1#",
]

# FTMS Control Point opcodes.
FTMS_SET_TARGET_INCLINATION = 0x03
FTMS_START_RESUME = 0x07
FTMS_STOP_PAUSE = 0x08

BYTE_DELAY = 0.040
TEXT_RESPONSE_TIMEOUT = 6.0
FTMS_RESPONSE_TIMEOUT = 4.0


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def clean_text(data: bytes) -> str:
    text = data.decode("latin-1", errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def ftms_result_name(code: int) -> str:
    return {
        0x01: "SUCCESS",
        0x02: "NOT_SUPPORTED",
        0x03: "INVALID_PARAMETER",
        0x04: "OPERATION_FAILED",
        0x05: "CONTROL_NOT_PERMITTED",
    }.get(code, hex(code))


class Receiver:
    def __init__(self):
        self.text_buffer = bytearray()
        self.text_frames = asyncio.Queue()
        self.ftms_frames = asyncio.Queue()

    def tg_notify(self, sender, data: bytearray):
        chunk = bytes(data)
        self.text_buffer.extend(chunk)

        # Reassemble !....# frames. MYRUN often notifies one byte at a time.
        while b"#" in self.text_buffer:
            idx = self.text_buffer.index(ord("#"))
            frame = bytes(self.text_buffer[:idx + 1])
            del self.text_buffer[:idx + 1]
            try:
                self.text_frames.put_nowait(frame)
            except asyncio.QueueFull:
                pass

    def ftms_notify(self, sender, data: bytearray):
        try:
            self.ftms_frames.put_nowait(bytes(data))
        except asyncio.QueueFull:
            pass

    def clear_text(self):
        self.text_buffer.clear()
        while not self.text_frames.empty():
            try:
                self.text_frames.get_nowait()
            except asyncio.QueueEmpty:
                break

    def clear_ftms(self):
        while not self.ftms_frames.empty():
            try:
                self.ftms_frames.get_nowait()
            except asyncio.QueueEmpty:
                break


async def find_device(address, name_substring):
    if address:
        print(f"Suche {address} ...")
        dev = await BleakScanner.find_device_by_address(address, timeout=15.0)
        if dev:
            return dev
        print("Adresse nicht gefunden, suche nach Gerätename ...")

    wanted = name_substring.lower()

    def filt(device, adv):
        n = (device.name or adv.local_name or "").lower()
        return wanted in n

    return await BleakScanner.find_device_by_filter(filt, timeout=20.0)


async def send_ascii_bytewise(client, text):
    for b in text.encode("ascii"):
        await client.write_gatt_char(TG_WRITE, bytes([b]), response=True)
        await asyncio.sleep(BYTE_DELAY)


async def text_command(client, rx, command):
    rx.clear_text()
    sent_at = now()
    await send_ascii_bytewise(client, command)
    try:
        frame = await asyncio.wait_for(
            rx.text_frames.get(), timeout=TEXT_RESPONSE_TIMEOUT
        )
        return sent_at, frame, None
    except asyncio.TimeoutError:
        partial = bytes(rx.text_buffer)
        rx.text_buffer.clear()
        return sent_at, partial, "TIMEOUT"


async def send_ftms(client, rx, payload: bytes):
    rx.clear_ftms()
    sent_at = now()
    await client.write_gatt_char(FTMS_CONTROL_POINT, payload, response=True)

    try:
        answer = await asyncio.wait_for(
            rx.ftms_frames.get(), timeout=FTMS_RESPONSE_TIMEOUT
        )
        return sent_at, payload, answer, None
    except asyncio.TimeoutError:
        return sent_at, payload, b"", "FTMS RESPONSE TIMEOUT"


async def send_incline(client, rx, percent):
    """
    FTMS target inclination = signed int16 in units of 0.1 %.
    QZ's MYRUN implementation sends:
      [0x03, low byte, high byte]
    """
    tenth_percent = int(round(percent * 10.0))
    payload = bytes([FTMS_SET_TARGET_INCLINATION]) + struct.pack(
        "<h", tenth_percent
    )
    return await send_ftms(client, rx, payload)


async def send_start(client, rx):
    return await send_ftms(client, rx, bytes([FTMS_START_RESUME]))


async def send_stop(client, rx):
    # FTMS stop/pause opcode + STOP parameter 0x01, matching QZ.
    return await send_ftms(client, rx, bytes([FTMS_STOP_PAUSE, 0x01]))


def section(f, title):
    f.write("\n" + "=" * 80 + "\n")
    f.write(title + "\n")
    f.write("=" * 80 + "\n")


def log_text_result(f, label, command, sent_at, response, error=None):
    section(f, label)
    f.write(f"Zeit:    {sent_at}\n")
    f.write(f"Befehl:  {command}\n")
    f.write(f"Status:  {error or 'OK'}\n\n")

    if response:
        txt = clean_text(response)
        f.write(txt)
        if not txt.endswith("\n"):
            f.write("\n")
        f.write(f"\nHEX: {response.hex(' ')}\n")
    else:
        f.write("<keine Antwort>\n")


def log_ftms_result(f, label, description, sent_at, payload, answer, error=None):
    section(f, label)
    f.write(f"Zeit:          {sent_at}\n")
    f.write(f"Aktion:        {description}\n")
    f.write(f"FTMS TX:       {payload.hex(' ')}\n")

    if answer:
        f.write(f"FTMS RX:       {answer.hex(' ')}\n")
        if len(answer) >= 3 and answer[0] == 0x80:
            f.write(f"FTMS Ergebnis:  {ftms_result_name(answer[2])}\n")
    else:
        f.write(f"FTMS RX:       <keine Antwort> ({error})\n")


def ftms_succeeded(answer: bytes) -> bool:
    return len(answer) >= 3 and answer[0] == 0x80 and answer[2] == 0x01


async def sample_triplet(client, rx, f, prefix):
    # DUMPIO first: capture elevation command bits as early as possible.
    for label, cmd in [
        (f"{prefix} - Digital I/O", "@DUMPIO#"),
        (f"{prefix} - Status", "@STATUS#"),
        (f"{prefix} - ADC / incline", "@RADCEXT#"),
    ]:
        sent_at, resp, err = await text_command(client, rx, cmd)
        log_text_result(f, label, cmd, sent_at, resp, err)
        f.flush()


async def sample_status(client, rx, f, prefix):
    sent_at, resp, err = await text_command(client, rx, "@STATUS#")
    log_text_result(f, f"{prefix} - Status", "@STATUS#", sent_at, resp, err)
    f.flush()


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--address", help="BLE address, e.g. E0:86:1D:FA:4D:A0")
    ap.add_argument("--name", default="MyRun")
    ap.add_argument(
        "--target",
        type=float,
        default=2.0,
        help="test target inclination in percent (default: 2.0)",
    )
    ap.add_argument("--output", help="report filename")
    args = ap.parse_args()

    if not (0.5 <= args.target <= 5.0):
        print("Aus Sicherheitsgründen erlaubt das Script nur 0.5 bis 5.0 %.")
        return 2

    output = Path(
        args.output
        if args.output
        else f"myrun_incline_test_{datetime.now():%Y%m%d_%H%M%S}.txt"
    )

    dev = await find_device(args.address, args.name)
    if not dev:
        print("MYRUN nicht gefunden.")
        print("Technogym-App, nRF Connect und QZ vollständig trennen.")
        return 3

    print(f"Gefunden: {dev.name!r}  {dev.address}")
    print("Verbinde ...")

    rx = Receiver()
    disconnected = asyncio.Event()
    start_sent = False

    def on_disconnect(_client):
        disconnected.set()
        print("\n*** BLE-Verbindung getrennt ***")

    with output.open("w", encoding="utf-8") as f:
        f.write("TECHNOGYM MYRUN - CONTROLLED INCLINE DIAGNOSTIC TEST\n")
        f.write(f"Erstellt:       {now()}\n")
        f.write(f"Gerät:          {dev.name!r}\n")
        f.write(f"Adresse:        {dev.address}\n")
        f.write(f"Testziel:       {args.target:.1f} %\n")

        async with BleakClient(
            dev,
            disconnected_callback=on_disconnect,
            timeout=20.0,
        ) as client:
            f.write(f"Connected:      {client.is_connected}\n")
            print(f"Verbunden: {client.is_connected}")

            await client.start_notify(TG_NOTIFY, rx.tg_notify)
            await client.start_notify(FTMS_CONTROL_POINT, rx.ftms_notify)

            try:
                # ---- Initialization ----
                section(f, "BLE / FTMS INITIALISIERUNG")
                rx.clear_ftms()
                f.write(f"FTMS TX: {QZ_FTMS_INIT.hex(' ')}\n")
                await client.write_gatt_char(
                    FTMS_CONTROL_POINT, QZ_FTMS_INIT, response=True
                )
                try:
                    ans = await asyncio.wait_for(
                        rx.ftms_frames.get(), timeout=FTMS_RESPONSE_TIMEOUT
                    )
                    f.write(f"FTMS RX: {ans.hex(' ')}\n")
                except asyncio.TimeoutError:
                    f.write("FTMS RX: <Timeout>\n")

                await asyncio.sleep(0.5)

                section(f, "TECHNOGYM SETUP")
                for cmd in INIT_COMMANDS:
                    sent_at, resp, err = await text_command(client, rx, cmd)
                    f.write(f"\n[{sent_at}] {cmd}\n")
                    if resp:
                        txt = clean_text(resp)
                        f.write(txt)
                        if not txt.endswith("\n"):
                            f.write("\n")
                    else:
                        f.write(f"<{err}>\n")
                    await asyncio.sleep(0.2)

                # ---- Baseline ----
                print("Baseline erfassen ...")
                await sample_triplet(client, rx, f, "BASELINE")

                print()
                print("ACHTUNG: Gleich wird FTMS START/RESUME gesendet.")
                print("Niemand darf auf dem Laufband stehen.")
                print("Das Script setzt KEINE Geschwindigkeit, aber START ist real.")
                for n in (3, 2, 1):
                    print(n, flush=True)
                    await asyncio.sleep(1.0)

                # ---- Start/Resume ----
                print("Sende START/RESUME ...")
                sent_at, payload, ans, err = await send_start(client, rx)
                start_sent = True
                log_ftms_result(
                    f,
                    "FTMS: START / RESUME",
                    "START/RESUME",
                    sent_at,
                    payload,
                    ans,
                    err,
                )
                f.flush()

                await asyncio.sleep(0.25)
                print("Status nach START erfassen ...")
                await sample_status(client, rx, f, "NACH START")

                if not ftms_succeeded(ans):
                    print("START/RESUME wurde nicht erfolgreich bestätigt.")
                    print("Incline wird trotzdem NICHT blind erzwungen; Diagnose geht weiter.")
                    section(f, "HINWEIS")
                    f.write(
                        "START/RESUME wurde nicht mit SUCCESS bestätigt. "
                        "Der Incline-Befehl wird dennoch einmal regulär über FTMS "
                        "gesendet, um die Antwort zu protokollieren; es wird kein "
                        "niedrigerer Sicherheitsmechanismus umgangen.\n"
                    )

                # ---- Incline up test ----
                print(f"Setze Zielneigung auf {args.target:.1f} % ...")
                sent_at, payload, ans_up1, err = await send_incline(
                    client, rx, args.target
                )
                log_ftms_result(
                    f,
                    "FTMS: ZIELNEIGUNG HOCH",
                    f"Zielneigung {args.target:.1f} %",
                    sent_at,
                    payload,
                    ans_up1,
                    err,
                )
                f.flush()

                await asyncio.sleep(0.10)
                print("Messung A direkt nach Incline-Befehl ...")
                await sample_triplet(client, rx, f, "NACH +INCLINE A")

                print("Zielneigung erneut anfordern ...")
                sent_at, payload, ans_up2, err = await send_incline(
                    client, rx, args.target
                )
                log_ftms_result(
                    f,
                    "FTMS: ZIELNEIGUNG HOCH - WIEDERHOLUNG",
                    f"Zielneigung {args.target:.1f} %",
                    sent_at,
                    payload,
                    ans_up2,
                    err,
                )
                f.flush()

                await asyncio.sleep(0.10)
                print("Messung B nach Wiederholung ...")
                await sample_triplet(client, rx, f, "NACH +INCLINE B")

                # ---- Return to zero ----
                print("Setze Zielneigung wieder auf 0.0 % ...")
                sent_at, payload, ans_zero, err = await send_incline(
                    client, rx, 0.0
                )
                log_ftms_result(
                    f,
                    "FTMS: ZIELNEIGUNG ZURÜCK AUF 0",
                    "Zielneigung 0.0 %",
                    sent_at,
                    payload,
                    ans_zero,
                    err,
                )
                f.flush()

                await asyncio.sleep(0.25)
                await sample_triplet(client, rx, f, "NACH 0 %")

            finally:
                # STOP/PAUSE after START whenever the BLE connection still exists.
                if start_sent and client.is_connected:
                    print("Sende STOP/PAUSE ...")
                    try:
                        sent_at, payload, ans_stop, err = await send_stop(
                            client, rx
                        )
                        log_ftms_result(
                            f,
                            "FTMS: STOP / PAUSE",
                            "STOP/PAUSE",
                            sent_at,
                            payload,
                            ans_stop,
                            err,
                        )
                        f.flush()
                        await asyncio.sleep(0.25)

                        if client.is_connected:
                            print("Abschlussstatus erfassen ...")
                            await sample_triplet(
                                client, rx, f, "NACH STOP"
                            )
                    except Exception as stop_exc:
                        section(f, "STOP / PAUSE FEHLER")
                        f.write(
                            f"{type(stop_exc).__name__}: {stop_exc}\n"
                        )
                        f.flush()
                        print(
                            "WARNUNG: STOP/PAUSE konnte nicht sauber gesendet werden."
                        )

                section(f, "ENDE")
                f.write(f"Beendet: {now()}\n")
                f.flush()

                if client.is_connected:
                    try:
                        await client.stop_notify(TG_NOTIFY)
                    except Exception:
                        pass
                    try:
                        await client.stop_notify(FTMS_CONTROL_POINT)
                    except Exception:
                        pass

    print()
    print("Fertig.")
    print(f"Report: {output.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\nAbgebrochen.")
        sys.exit(130)
    except Exception as e:
        print(f"\nFEHLER: {type(e).__name__}: {e}")
        sys.exit(1)
