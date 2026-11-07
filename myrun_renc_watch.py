#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""
Technogym MYRUN - minimal encoder watch

Sends ONLY the read command @RENC# (encoder frequency) on the Technogym text
channel, about once per second, and logs the answers. Nothing else is written:
no FTMS request-control init, no setup commands (@DISABLE_PACE#, @SSIUNITS#,
@RJSK_EN/@LJSK_EN), no START/STOP, no other commands.

Purpose: push the belt slowly by hand and check whether the encoder signal
still reaches the console through the lower kit (e.g. with the GIRT locked,
SIS2 blinking, and again after a power cycle).

    python3 myrun_renc_watch.py                 # 60 s
    python3 myrun_renc_watch.py --duration 120
    python3 myrun_renc_watch.py --cmd "@STATUS#" # optionally a 2nd read command

Output: myrun_renc_watch_<timestamp>.csv (t_rel_s, wallclock, enc_hz, enc_kmh, raw)
"""

import argparse
import asyncio
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from bleak import BleakClient, BleakScanner

TG_WRITE = "df1eb8e4-1753-4bb9-a6a6-e018040af0a3"
TG_NOTIFY = "6f26de4b-dcef-4459-9465-931f1b144c20"
ALLOWED_EXTRA = {"@STATUS#", "@DUMPIO#", "@RPWM#"}   # read-only only

RE_RENC = re.compile(r"RENC:\s*([\d.]+)\s*Hz\s*->\s*([\d.]+)\s*km/h", re.I)


class Receiver:
    def __init__(self):
        self.buf = bytearray()
        self.frames = asyncio.Queue()

    def notify(self, _s, data):
        chunk = bytes(data)
        if b"!" in chunk and not self.buf:
            chunk = chunk[chunk.index(b"!"):]
        self.buf.extend(chunk)
        while b"#" in self.buf:
            i = self.buf.index(ord("#"))
            self.frames.put_nowait(bytes(self.buf[: i + 1]))
            del self.buf[: i + 1]
        if self.buf.startswith(b"!") and self.buf.endswith(b":ERROR"):
            self.frames.put_nowait(bytes(self.buf))
            self.buf.clear()

    def clear(self):
        self.buf.clear()
        while not self.frames.empty():
            self.frames.get_nowait()


async def send(client, rx, cmd, byte_delay, timeout=4.0):
    rx.clear()
    for b in cmd.encode("ascii"):
        await client.write_gatt_char(TG_WRITE, bytes([b]), response=True)
        await asyncio.sleep(byte_delay)
    try:
        return (await asyncio.wait_for(rx.frames.get(), timeout)).decode("latin-1", "replace")
    except asyncio.TimeoutError:
        return None


async def find(address, name):
    if address:
        d = await BleakScanner.find_device_by_address(address, timeout=15)
        if d:
            return d
    return await BleakScanner.find_device_by_filter(
        lambda d, a: name.lower() in (d.name or a.local_name or "").lower(), timeout=20)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--address")
    ap.add_argument("--name", default="MyRun")
    ap.add_argument("--duration", type=float, default=60)
    ap.add_argument("--interval", type=float, default=0.5, help="pause between polls [s]")
    ap.add_argument("--byte-delay", type=float, default=0.04)
    ap.add_argument("--cmd", choices=sorted(ALLOWED_EXTRA),
                    help="optional second read command, polled every 5th cycle")
    ap.add_argument("--output")
    a = ap.parse_args()

    out = Path(a.output or f"myrun_renc_watch_{datetime.now():%Y%m%d_%H%M%S}.csv")
    dev = await find(a.address, a.name)
    if not dev:
        print("MYRUN nicht gefunden (andere Apps trennen).")
        return 2
    print(f"Gefunden: {dev.name} {dev.address} - sende nur @RENC#"
          + (f" und {a.cmd}" if a.cmd else ""))
    rx = Receiver()
    t0 = time.monotonic()
    with out.open("w", encoding="utf-8") as f:
        f.write("t_rel_s,wallclock,enc_hz,enc_kmh,raw\n")
        async with BleakClient(dev, timeout=20) as cl:
            await cl.start_notify(TG_NOTIFY, rx.notify)
            await asyncio.sleep(0.5)
            n = 0
            while time.monotonic() - t0 < a.duration:
                r = await send(cl, rx, "@RENC#", a.byte_delay)
                t = time.monotonic() - t0
                wc = datetime.now().isoformat(timespec="milliseconds")
                m = RE_RENC.search(r or "")
                hz, kmh = (m.group(1), m.group(2)) if m else ("", "")
                raw = (r or "TIMEOUT").replace("\r", "\\r").replace("\n", "\\n").replace(",", ";")
                f.write(f"{t:.3f},{wc},{hz},{kmh},{raw}\n")
                f.flush()
                bar = "#" * min(int(float(hz) / 10), 60) if hz else ""
                print(f"{t:7.2f}s  {hz or '?':>6} Hz  {bar}" if m else f"{t:7.2f}s  {raw}")
                n += 1
                if a.cmd and n % 5 == 0:
                    r2 = await send(cl, rx, a.cmd, a.byte_delay)
                    print("         " + (r2 or "TIMEOUT").replace("\r\n", " | ")[:160])
                    f.write(f"{time.monotonic() - t0:.3f},{datetime.now().isoformat(timespec='milliseconds')},,,"
                            f"{(r2 or 'TIMEOUT').replace(chr(13), '').replace(chr(10), ' | ').replace(',', ';')}\n")
                await asyncio.sleep(a.interval)
    print(f"\nCSV: {out.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        sys.exit(130)
