#!/usr/bin/env python3
"""
Technogym MYRUN - automatic BLE diagnostic dump

Runs the known read-only diagnostics automatically and writes ONE readable
timestamped report file in the current directory.

Install:
    python3 -m pip install --user bleak

Run:
    python3 myrun_dump.py

Optional:
    python3 myrun_dump.py --address E0:86:1D:FA:4D:A0
    python3 myrun_dump.py --output myrun_report.txt
"""

import argparse
import asyncio
from datetime import datetime
from pathlib import Path
import sys
import time

from bleak import BleakClient, BleakScanner

# Standard Fitness Machine Service control point
FTMS_CONTROL_POINT = "00002ad9-0000-1000-8000-00805f9b34fb"

# Technogym custom BLE characteristics observed on this MYRUN
TG_WRITE  = "df1eb8e4-1753-4bb9-a6a6-e018040af0a3"
TG_NOTIFY = "6f26de4b-dcef-4459-9465-931f1b144c20"

# QZ/qdomyos-zwift style initialization
QZ_FTMS_INIT = bytes.fromhex("00 93 F0 51 E8 1B 42 92 8E")

# These are setup commands, not diagnostics.
INIT_COMMANDS = [
    "@DISABLE_PACE#",
    "@SSIUNITS#",
    "@RJSK_EN 1#",
    "@LJSK_EN 1#",
]

# Known read-only diagnostics we want to collect automatically.
DIAG_COMMANDS = [
    ("Firmware",       "@FWVER#"),
    ("Error log",      "@RERRORLOG#"),
    ("Status",         "@STATUS#"),
    ("ADC / incline",  "@RADCEXT#"),
    ("Digital I/O",    "@DUMPIO#"),
]

BYTE_DELAY = 0.040
RESPONSE_TIMEOUT = 6.0


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def clean_text(data: bytes) -> str:
    """Decode response while keeping tabs/newlines readable."""
    text = data.decode("latin-1", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Do not strip internal whitespace/tabs: the MYRUN uses it for fields.
    return text


class Receiver:
    """
    Reassembles the MYRUN's one-byte BLE notifications into whole textual
    response frames. Text responses normally start with ! and end with #.
    """
    def __init__(self):
        self.buffer = bytearray()
        self.frames = asyncio.Queue()
        self.frame_log = []
        self.ftms_log = []

    def tg_notify(self, sender, data: bytearray):
        chunk = bytes(data)

        # If garbage precedes a new textual response, keep only from "!" onward.
        if b"!" in chunk and not self.buffer:
            self.buffer.extend(chunk[chunk.index(b"!"):])
        else:
            self.buffer.extend(chunk)

        # A callback is usually one byte, but support multiple frames/chunks.
        while b"#" in self.buffer:
            idx = self.buffer.index(ord("#"))
            frame = bytes(self.buffer[:idx + 1])
            del self.buffer[:idx + 1]

            self.frame_log.append((now(), frame))
            try:
                self.frames.put_nowait(frame)
            except asyncio.QueueFull:
                pass

    def ftms_notify(self, sender, data: bytearray):
        b = bytes(data)
        self.ftms_log.append((now(), b))

    def clear_pending(self):
        self.buffer.clear()
        while not self.frames.empty():
            try:
                self.frames.get_nowait()
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


async def send_bytewise(client, text):
    for b in text.encode("ascii"):
        await client.write_gatt_char(TG_WRITE, bytes([b]), response=True)
        await asyncio.sleep(BYTE_DELAY)


async def send_and_collect(client, rx, command, timeout=RESPONSE_TIMEOUT):
    """
    Send one command and wait for the next complete !...# response.
    Waiting for '#' is important because this MYRUN returns responses one byte
    per BLE notification.
    """
    rx.clear_pending()
    sent_at = now()
    await send_bytewise(client, command)

    try:
        frame = await asyncio.wait_for(rx.frames.get(), timeout=timeout)
        return sent_at, frame, None
    except asyncio.TimeoutError:
        partial = bytes(rx.buffer)
        rx.buffer.clear()
        return sent_at, partial, "TIMEOUT"


def write_section(f, title):
    f.write("\n" + "=" * 78 + "\n")
    f.write(title + "\n")
    f.write("=" * 78 + "\n")


def write_command_result(f, label, command, sent_at, response, error=None):
    write_section(f, label)
    f.write(f"Zeit:     {sent_at}\n")
    f.write(f"Befehl:   {command}\n")
    if error:
        f.write(f"Status:   {error}\n")
    else:
        f.write("Status:   Antwort vollständig empfangen\n")

    f.write("\nANTWORT (lesbar):\n")
    f.write("-" * 78 + "\n")
    if response:
        text = clean_text(response)
        # Make protocol envelope less visually noisy, but preserve it.
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")
    else:
        f.write("<keine Antwort>\n")

    f.write("\nRAW HEX:\n")
    f.write("-" * 78 + "\n")
    f.write(response.hex(" ") if response else "<leer>")
    f.write("\n")


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--address", help="BLE address, e.g. E0:86:1D:FA:4D:A0")
    ap.add_argument("--name", default="MyRun", help="device-name substring")
    ap.add_argument("--output", help="output filename")
    args = ap.parse_args()

    if args.output:
        output = Path(args.output)
    else:
        output = Path(f"myrun_diagnostic_{datetime.now():%Y%m%d_%H%M%S}.txt")

    dev = await find_device(args.address, args.name)
    if not dev:
        print("MYRUN nicht gefunden.")
        print("Technogym-App, nRF Connect und QZ vollständig trennen und erneut versuchen.")
        return 2

    print(f"Gefunden: {dev.name!r}  {dev.address}")
    print("Verbinde ...")

    rx = Receiver()
    disconnected = asyncio.Event()

    def disconnected_cb(_client):
        disconnected.set()
        print("\n*** Bluetooth-Verbindung getrennt ***")

    with output.open("w", encoding="utf-8") as f:
        f.write("TECHNOGYM MYRUN - BLE DIAGNOSTIC REPORT\n")
        f.write(f"Erstellt:  {now()}\n")
        f.write(f"Gerät:     {dev.name!r}\n")
        f.write(f"Adresse:   {dev.address}\n")

        async with BleakClient(
            dev,
            disconnected_callback=disconnected_cb,
            timeout=20.0
        ) as client:
            f.write(f"Connected: {client.is_connected}\n")
            print(f"Verbunden: {client.is_connected}")

            if not client.is_connected:
                f.write("FEHLER: Verbindung nicht hergestellt.\n")
                return 3

            uuids = {
                c.uuid.lower()
                for service in client.services
                for c in service.characteristics
            }
            missing = [
                u for u in (TG_WRITE, TG_NOTIFY, FTMS_CONTROL_POINT)
                if u.lower() not in uuids
            ]
            if missing:
                write_section(f, "FEHLER")
                f.write("Fehlende Characteristic(s):\n")
                for u in missing:
                    f.write(f"  {u}\n")
                return 4

            await client.start_notify(TG_NOTIFY, rx.tg_notify)

            try:
                await client.start_notify(FTMS_CONTROL_POINT, rx.ftms_notify)
            except Exception as e:
                f.write(f"\nWARNUNG FTMS subscribe: {type(e).__name__}: {e}\n")

            # ---- FTMS initialization ----
            write_section(f, "BLE / FTMS INITIALISIERUNG")
            f.write(f"TX: {QZ_FTMS_INIT.hex(' ')}\n")
            print("FTMS-Initialisierung ...")
            await client.write_gatt_char(
                FTMS_CONTROL_POINT, QZ_FTMS_INIT, response=True
            )
            await asyncio.sleep(0.8)

            if rx.ftms_log:
                for t, b in rx.ftms_log:
                    f.write(f"RX {t}: {b.hex(' ')}\n")
            else:
                f.write("RX: <keine FTMS-Indication protokolliert>\n")

            # ---- QZ-style ASCII setup ----
            write_section(f, "TECHNOGYM BLE SETUP")
            for cmd in INIT_COMMANDS:
                if disconnected.is_set() or not client.is_connected:
                    f.write("ABBRUCH: Gerät getrennt.\n")
                    return 5

                print(f"Setup: {cmd}")
                sent_at, response, error = await send_and_collect(
                    client, rx, cmd, timeout=RESPONSE_TIMEOUT
                )
                f.write(f"\n[{sent_at}] {cmd}\n")
                if response:
                    f.write(clean_text(response))
                    if not clean_text(response).endswith("\n"):
                        f.write("\n")
                else:
                    f.write(f"<{error or 'keine Antwort'}>\n")
                # Give firmware a moment before the next setup command.
                await asyncio.sleep(0.35)

            # ---- Automatic diagnostic sequence ----
            write_section(f, "AUTOMATISCHE DIAGNOSE")
            f.write(
                "Die folgenden Diagnosebefehle wurden automatisch "
                "nacheinander ausgeführt.\n"
            )

            for label, cmd in DIAG_COMMANDS:
                if disconnected.is_set() or not client.is_connected:
                    write_section(f, label)
                    f.write("ABBRUCH: Bluetooth-Verbindung getrennt.\n")
                    break

                print(f"Diagnose: {label:14s} {cmd}")
                sent_at, response, error = await send_and_collect(
                    client, rx, cmd, timeout=RESPONSE_TIMEOUT
                )
                write_command_result(
                    f, label, cmd, sent_at, response, error
                )
                f.flush()
                await asyncio.sleep(0.5)

            # Any incomplete residual bytes should not disappear.
            if rx.buffer:
                write_section(f, "UNVOLLSTÄNDIGE RESTDATEN")
                f.write(clean_text(bytes(rx.buffer)) + "\n")
                f.write("HEX: " + bytes(rx.buffer).hex(" ") + "\n")

            f.write("\n\nENDE DES REPORTS\n")
            f.write(f"Beendet: {now()}\n")

            try:
                await client.stop_notify(TG_NOTIFY)
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
