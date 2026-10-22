#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""MYRUN fault-transition monitor with confirmed FTMS START and optional incline."""
import argparse
import asyncio
from datetime import datetime
from pathlib import Path
import sys
from bleak import BleakClient, BleakScanner

FTMS = "00002ad9-0000-1000-8000-00805f9b34fb"
WRITE = "df1eb8e4-1753-4bb9-a6a6-e018040af0a3"
NOTIFY = "6f26de4b-dcef-4459-9465-931f1b144c20"
INIT = bytes.fromhex("00 93 F0 51 E8 1B 42 92 8E")
SETUP = ("@DISABLE_PACE#", "@SSIUNITS#", "@RJSK_EN 1#", "@LJSK_EN 1#")

def stamp():
    return datetime.now().isoformat(timespec="milliseconds")

class Responses:
    def __init__(self):
        self.buffer = bytearray()
        self.queue = asyncio.Queue()
        self.ftms = []
        self.ftms_queue = asyncio.Queue()
    def tg(self, _sender, data):
        self.buffer.extend(data)
        while b"#" in self.buffer:
            pos = self.buffer.index(35)
            frame = bytes(self.buffer[:pos+1])
            del self.buffer[:pos+1]
            self.queue.put_nowait(frame)
    def ftms_cb(self, _sender, data):
        packet = bytes(data)
        self.ftms.append((stamp(), packet.hex(" ")))
        self.ftms_queue.put_nowait(packet)
    def reset(self):
        self.buffer.clear()
        while not self.queue.empty():
            self.queue.get_nowait()

async def command(client, rx, cmd, timeout=4.0):
    rx.reset()
    started = stamp()
    for byte in cmd.encode("ascii"):
        await client.write_gatt_char(WRITE, bytes([byte]), response=True)
        await asyncio.sleep(0.04)
    try:
        payload = await asyncio.wait_for(rx.queue.get(), timeout)
        return started, payload.decode("latin-1", "replace").strip(), "OK"
    except asyncio.TimeoutError:
        partial = rx.buffer.decode("latin-1", "replace")
        return started, partial, "TIMEOUT"

async def ftms_command(client, rx, payload, emit):
    while not rx.ftms_queue.empty():
        rx.ftms_queue.get_nowait()
    emit(f"FTMS TX {payload.hex(' ')}")
    await client.write_gatt_char(FTMS, payload, response=True)
    try:
        while True:
            answer = await asyncio.wait_for(rx.ftms_queue.get(), timeout=4.0)
            emit(f"FTMS RX {answer.hex(' ')}")
            if len(answer) >= 3 and answer[:2] == bytes((0x80, payload[0])):
                return answer[2] == 1
    except asyncio.TimeoutError:
        emit("FTMS response timeout; result unknown")
        return False

def fields(payload):
    import re
    return {k.strip():v.strip() for k,v in re.findall(
        r"(?m)(?:^|[,\n])\s*([A-Za-z_][A-Za-z_0-9]*):\s*([^,\n#]+)", payload)}

async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--address", default="E0:86:1D:FA:4D:A0")
    parser.add_argument("--name", default="MyRun")
    parser.add_argument("--output")
    parser.add_argument("--incline", type=float, default=None, help="Optional single incline command (0.5..2.0 percent) after successful START")
    parser.add_argument("--duration", type=float, default=120.0, help="Monitoring seconds (default 120)")
    parser.add_argument("--interval", type=float, default=0.2, help="Delay between STATUS/DUMPIO pairs")
    args = parser.parse_args()
    if args.incline is not None and not (0.5 <= args.incline <= 2.0):
        parser.error("--incline must be between 0.5 and 2.0 percent")
    if args.duration <= 0 or args.interval < 0:
        parser.error("--duration must be positive and --interval nonnegative")
    print("\\nACHTUNG: FTMS START/RESUME kann das Band selbstständig mit ca. 1,2 km/h starten.")
    print("Nicht auf dem Band stehen. Sicherheitsstopp erreichbar halten.")
    print("Nicht starten bei beschädigter Mechanik, offenen Abdeckungen oder unklarem elektrischen Defekt.")
    confirmation = input("Ist das Gerät vollständig montiert, mechanisch frei und darf anlaufen? Tippe START FREIGEBEN: ")
    if confirmation.strip() != "START FREIGEBEN":
        print("Keine Freigabe; Abbruch ohne Verbindung.")
        return 1
    path = Path(args.output or f"myrun_fault_monitor_{datetime.now():%Y%m%d_%H%M%S}.txt")
    dev = await BleakScanner.find_device_by_address(args.address, timeout=15)
    if dev is None:
        dev = await BleakScanner.find_device_by_filter(
            lambda d,a: args.name.lower() in (d.name or a.local_name or "").lower(), timeout=20)
    if dev is None:
        print("MYRUN nicht gefunden; andere BLE-Apps trennen.")
        return 2
    rx = Responses()
    previous = {}
    fault = False
    start_attempted = False
    with path.open("w", encoding="utf-8", buffering=1) as log:
        def emit(line):
            message = f"[{stamp()}] {line}"
            print(message, flush=True)
            log.write(message + "\n")
        emit(f"DEVICE {dev.name} {dev.address}; active FTMS START monitor; duration={args.duration}s; incline={args.incline}")
        async with BleakClient(dev, timeout=20) as client:
            await client.start_notify(NOTIFY, rx.tg)
            try:
                await client.start_notify(FTMS, rx.ftms_cb)
            except Exception as exc:
                emit(f"FTMS subscribe warning: {exc}")
            await client.write_gatt_char(FTMS, INIT, response=True)
            await asyncio.sleep(0.8)
            emit(f"FTMS initialization indications: {rx.ftms}")
            for setup in SETUP:
                t, response, state = await command(client, rx, setup)
                emit(f"SETUP {setup} {state} {response!r}")
            for label, cmd in (("FWVER","@FWVER#"), ("ERRORLOG_START","@RERRORLOG#")):
                t, response, state = await command(client, rx, cmd)
                emit(f"{label} {state} {response!r}")
            # Baseline first: do not command START when already faulted.
            t, baseline, baseline_state = await command(client, rx, "@STATUS#")
            emit(f"BASELINE STATUS {baseline_state} {baseline!r}")
            t, io, io_state = await command(client, rx, "@DUMPIO#")
            emit(f"BASELINE DUMPIO {io_state} {io!r}")
            if baseline_state != "OK" or "QSHardwareFault" in baseline:
                emit("Already faulted or baseline unavailable: START suppressed.")
                return 4
            emit("FTMS START/RESUME requested after explicit terminal confirmation.")
            start_attempted = True
            started_ok = await ftms_command(client, rx, bytes([0x07]), emit)
            emit(f"START acknowledged SUCCESS={started_ok}")
            if started_ok and args.incline is not None:
                import struct
                value = int(round(args.incline * 10))
                incline_ok = await ftms_command(client, rx, bytes([0x03]) + struct.pack("<h", value), emit)
                emit(f"INCLINE {args.incline:.1f}% acknowledged SUCCESS={incline_ok}")
            emit("MONITOR START.")
            end = asyncio.get_running_loop().time() + args.duration
            count = 0
            try:
                while asyncio.get_running_loop().time() < end:
                    for label, cmd in (("STATUS","@STATUS#"), ("DUMPIO","@DUMPIO#")):
                        t, response, state = await command(client, rx, cmd)
                        emit(f"RAW {label} sent={t} {state} {response!r}")
                        if state == "OK":
                            if label == "STATUS":
                                import re
                                match = re.search(r"Status:\s*(QS\w+)", response)
                                current = match.group(1) if match else None
                                if current and previous.get("state") != current:
                                    emit(f"STATE CHANGE {previous.get('state')} -> {current}")
                                previous["state"] = current
                                if current == "QSHardwareFault":
                                    fault = True
                            else:
                                import re
                                values = dict(re.findall(r"(?m)^(?:OUT|IN|PWM)\s+(\w+)\s*=\s*(\d+)", response))
                                for key, value in values.items():
                                    if key in previous and previous[key] != value:
                                        emit(f"IO CHANGE {key}: {previous[key]} -> {value}")
                                    previous[key] = value
                        else:
                            emit(f"WARNING {label}: {state}")
                    count += 1
                    if fault:
                        emit("HARDWARE FAULT detected; collecting final error log.")
                        break
                    await asyncio.sleep(args.interval)
            except KeyboardInterrupt:
                emit("Interrupted by user")
            finally:
                if start_attempted and client.is_connected:
                    try:
                        emit("FTMS STOP/PAUSE requested")
                        stopped = await ftms_command(client, rx, bytes([0x08, 0x01]), emit)
                        emit(f"STOP acknowledged SUCCESS={stopped}; verify belt stopped physically")
                    except Exception as exc:
                        emit(f"STOP ERROR {type(exc).__name__}: {exc}; use physical stop")
                for label, cmd in (("ERRORLOG_END","@RERRORLOG#"), ("STATUS_END","@STATUS#"), ("DUMPIO_END","@DUMPIO#")):
                    try:
                        t, response, state = await command(client, rx, cmd)
                        emit(f"{label} {state} {response!r}")
                    except Exception as exc:
                        emit(f"{label} ERROR {type(exc).__name__}: {exc}")
                emit(f"END cycles={count}; hardware_fault={fault}")
    print(f"Report: {path.resolve()}")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("Abgebrochen")
        sys.exit(130)
