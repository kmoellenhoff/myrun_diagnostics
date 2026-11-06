#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""
Technogym MYRUN - read-only command probe

Fragt alle im Servicehandbuch (Rev. 2.2, Kap. 6.1.2) dokumentierten
LESE-Befehle ab und protokolliert die Antworten. Optional (--guess) werden
zusätzlich einige undokumentierte, vermutete Lesebefehle probiert, um zu sehen,
ob die neuere Firmware mehr Werte liefert (z. B. Temperatur, Lower-Kit-Status).

Sicherheit:
  * Es wird KEIN FTMS START/STOP und kein Steigungsbefehl gesendet.
  * Befehle, die etwas schreiben, zurücksetzen, kalibrieren oder bewegen,
    werden hart blockiert (siehe BLOCKED_PATTERNS), auch wenn man sie per
    --extra übergibt.

Aufruf:
    python3 myrun_probe.py
    python3 myrun_probe.py --guess
    python3 myrun_probe.py --extra "@RXYZ#" --extra "@RABC#"
    python3 myrun_probe.py --watch 60          # RENC/STATUS/DUMPIO wiederholt
"""

import argparse
import asyncio
import re
import sys
from datetime import datetime
from pathlib import Path

from bleak import BleakClient, BleakScanner

FTMS_CONTROL_POINT = "00002ad9-0000-1000-8000-00805f9b34fb"
TG_WRITE = "df1eb8e4-1753-4bb9-a6a6-e018040af0a3"
TG_NOTIFY = "6f26de4b-dcef-4459-9465-931f1b144c20"
QZ_FTMS_INIT = bytes.fromhex("00 93 F0 51 E8 1B 42 92 8E")

INIT_COMMANDS = ["@DISABLE_PACE#", "@SSIUNITS#", "@RJSK_EN 1#", "@LJSK_EN 1#"]

# Dokumentierte Lesebefehle (Servicehandbuch Rev. 2.2, S. 65-80)
DOCUMENTED = [
    ("Firmware-Version",                  "@FWVER#"),
    ("Encoder-Frequenz / Geschwindigkeit", "@RENC#"),
    ("ADC Steigung erweitert",             "@RADCEXT#"),
    ("Digital-I/O",                        "@DUMPIO#"),
    ("Status",                             "@STATUS#"),
    ("Fehlerspeicher",                     "@RERRORLOG#"),
    ("Kalibriertabelle Speed vs. PWM",     "@RKPWM#"),
    ("Quick-Start-Parameter",              "@RQSPAR#"),
    ("Nutzungsdaten (Zeiten, km)",         "@RSTAT#"),
    ("Letzte blockierte Task",             "@RTASKHANG#"),
    ("Runner-Detector Mindestspeed",       "@RRUNDETMINSP#"),
    ("Datum/Uhrzeit",                      "@GETDATE#"),
    ("BT-Seriennummer",                    "@RTG_ID#"),
    ("Gerätesensor UP",                    "@RDS_UP#"),
    ("Gerätesensor DOWN",                  "@RDS_DOWN#"),
]

# Undokumentierte Vermutungen. Alle beginnen mit "R" (Lesekonvention der
# Firmware) bzw. sind typische Hilfe-Befehle. Unbekannte Befehle werden von der
# Firmware normalerweise mit einer Fehlermeldung oder gar nicht beantwortet.
GUESSES = [
    "@HELP#", "@?#", "@LIST#",
    "@RTEMP#", "@RTEMPLK#", "@RNTC#",
    "@RLK#", "@RLKSTAT#", "@RLKSTATUS#", "@RLKVER#", "@RLKFW#", "@RLKERR#",
    "@RLOWKIT#", "@RINV#", "@RINVSTAT#", "@RDRIVE#",
    "@RVBUS#", "@RVDC#", "@RIMOT#", "@RCURR#", "@RMOT#", "@RMOTOR#",
    "@RPWM#", "@RSPEED#", "@RADC#",
    "@RCONF#", "@RPAR#", "@RPARAM#", "@RINFO#", "@RVER#",
    "@RERR#", "@RFAULT#", "@RALARM#",
]

# Alles, was nach Schreiben/Zurücksetzen/Bewegen aussieht, wird nie gesendet.
BLOCKED_PATTERNS = [
    r"RESET", r"^@S(?!TATUS#$)", r"SET", r"INIT", r"CAL", r"ELEV",
    r"FORCE", r"SUSPEND", r"STG_ID", r"WRITE", r"ERASE", r"CLEAR", r"FORMAT",
    r"UPD", r"BOOT", r"FLASH",
]

BYTE_DELAY = 0.040
TIMEOUT = 5.0


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def blocked(cmd: str) -> bool:
    body = cmd.upper()
    return any(re.search(p, body) for p in BLOCKED_PATTERNS)


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

    def clear(self):
        self.buf.clear()
        while not self.frames.empty():
            self.frames.get_nowait()


async def send(client, rx, cmd, timeout=TIMEOUT):
    rx.clear()
    for b in cmd.encode("ascii"):
        await client.write_gatt_char(TG_WRITE, bytes([b]), response=True)
        await asyncio.sleep(BYTE_DELAY)
    try:
        return await asyncio.wait_for(rx.frames.get(), timeout), None
    except asyncio.TimeoutError:
        part = bytes(rx.buf)
        rx.buf.clear()
        return part, "TIMEOUT"


def txt(b: bytes) -> str:
    return b.decode("latin-1", "replace").replace("\r\n", "\n").replace("\r", "\n")


async def find(address, name):
    if address:
        d = await BleakScanner.find_device_by_address(address, timeout=15)
        if d:
            return d
    return await BleakScanner.find_device_by_filter(
        lambda d, a: name.lower() in (d.name or a.local_name or "").lower(),
        timeout=20)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--address")
    ap.add_argument("--name", default="MyRun")
    ap.add_argument("--guess", action="store_true",
                    help="zusätzlich undokumentierte Lesebefehle probieren")
    ap.add_argument("--extra", action="append", default=[],
                    help="weiteren Befehl probieren, z. B. '@RXYZ#'")
    ap.add_argument("--watch", type=float, default=0,
                    help="danach N Sekunden RENC/STATUS/DUMPIO wiederholen")
    ap.add_argument("--output")
    a = ap.parse_args()

    out = Path(a.output or f"myrun_probe_{datetime.now():%Y%m%d_%H%M%S}.txt")
    cmds = [(l, c) for l, c in DOCUMENTED]
    if a.guess:
        cmds += [("Vermutung", c) for c in GUESSES]
    for c in a.extra:
        c = c if c.startswith("@") else "@" + c
        c = c if c.endswith("#") else c + "#"
        cmds.append(("Extra", c))

    dev = await find(a.address, a.name)
    if not dev:
        print("MYRUN nicht gefunden (andere Apps trennen).")
        return 2
    print(f"Gefunden: {dev.name} {dev.address}")
    rx = Receiver()
    summary = []

    with out.open("w", encoding="utf-8") as f:
        f.write(f"MYRUN READ-ONLY PROBE  {now()}  {dev.name} {dev.address}\n")
        async with BleakClient(dev, timeout=20) as cl:
            await cl.start_notify(TG_NOTIFY, rx.notify)
            # FTMS Control Point verlangt ein aktives Indication-Abo vor dem
            # Schreiben, sonst: CCCD_IMPROPERLY_CONFIGURED.
            try:
                await cl.start_notify(FTMS_CONTROL_POINT, lambda _s, _d: None)
            except Exception as e:
                print(f"Warnung FTMS-Abo: {e}")
            try:
                await cl.write_gatt_char(FTMS_CONTROL_POINT, QZ_FTMS_INIT, response=True)
            except Exception as e:
                print(f"Warnung FTMS-Init: {e} (Probe läuft trotzdem weiter)")
            await asyncio.sleep(0.8)
            for c in INIT_COMMANDS:
                await send(cl, rx, c)
                await asyncio.sleep(0.3)

            for label, c in cmds:
                if blocked(c):
                    f.write(f"\n### {c}  ({label})  -> BLOCKIERT, nicht gesendet\n")
                    summary.append((c, "BLOCKIERT"))
                    continue
                print(f"{c:18s} {label}")
                resp, err = await send(cl, rx, c)
                f.write(f"\n### {c}  ({label})  [{now()}]  {err or 'OK'}\n")
                f.write(txt(resp) if resp else "<keine Antwort>")
                f.write("\nHEX: " + (resp.hex(" ") if resp else "-") + "\n")
                f.flush()
                short = txt(resp).strip().replace("\n", " | ")[:70] if resp else "-"
                summary.append((c, err or short))
                await asyncio.sleep(0.4)

            if a.watch > 0:
                f.write(f"\n\n=== WATCH {a.watch:.0f} s: RENC / STATUS / DUMPIO ===\n")
                t_end = asyncio.get_event_loop().time() + a.watch
                while asyncio.get_event_loop().time() < t_end:
                    for c in ("@RENC#", "@STATUS#", "@DUMPIO#"):
                        resp, err = await send(cl, rx, c)
                        f.write(f"[{now()}] {c} {err or ''}\n{txt(resp) if resp else '-'}\n")
                        f.flush()
                    print(f"[{now()}] watch ...")

        f.write("\n\n=== ÜBERSICHT ===\n")
        for c, s in summary:
            f.write(f"{c:18s} {s}\n")

    print("\nÜbersicht:")
    for c, s in summary:
        print(f"  {c:18s} {s}")
    print(f"\nReport: {out.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        sys.exit(130)
