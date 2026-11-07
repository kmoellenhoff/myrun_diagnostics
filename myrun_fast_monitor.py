#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2
"""
Technogym MYRUN - fast fault monitor (active FTMS START)

Improvements over myrun_fault_monitor.py:
  * Passively logs EVERY notify/indicate characteristic with ms timestamps
    (FTMS Treadmill Data 0x2ACD, Machine Status 0x2ADA, Training Status 0x2AD3,
    RSC, ...) - no polling cost. Treadmill Data speed is decoded.
  * Fast polling of short commands (@RPWM#, @RENC#) instead of the long
    @STATUS#/@DUMPIO# replies; DUMPIO/STATUS only every few seconds.
  * Writes a CSV (t_rel_s, signal, value) for plotting next to the text log.
  * Short summary at the end (when speed/encoder dropped, PWM at that moment,
    first EM_POWENA change, fault time).

Safety:
  * Sends FTMS START/RESUME after pressing Enter. Nobody on the belt,
    machine assembled, emergency stop reachable.
  * START is sent only if the baseline @STATUS# confirms QSWaitForStart or
    QSWaitForStartRC; otherwise the script exits (power-cycle first).
  * At the end FTMS STOP is sent; a faulted controller may reject it.
  * No write/reset/calibration commands are sent. No @SETDATE.

Usage:
    python3 myrun_fast_monitor.py
    python3 myrun_fast_monitor.py --duration 90 --dumpio-every 2 --status-every 4
    python3 myrun_fast_monitor.py --byte-delay 0.02 --no-write-response   # faster, test first
"""

import argparse
import asyncio
import csv
import re
import struct
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from bleak import BleakClient, BleakScanner

FTMS_CP = "00002ad9-0000-1000-8000-00805f9b34fb"
TG_WRITE = "df1eb8e4-1753-4bb9-a6a6-e018040af0a3"
TG_NOTIFY = "6f26de4b-dcef-4459-9465-931f1b144c20"
QZ_INIT = bytes.fromhex("00 93 F0 51 E8 1B 42 92 8E")
SETUP = ("@DISABLE_PACE#", "@SSIUNITS#", "@RJSK_EN 1#", "@LJSK_EN 1#")

UUID_TREADMILL_DATA = "00002acd-0000-1000-8000-00805f9b34fb"
UUID_MACHINE_STATUS = "00002ada-0000-1000-8000-00805f9b34fb"
UUID_TRAINING_STATUS = "00002ad3-0000-1000-8000-00805f9b34fb"
SAFE_START_STATES = {"QSWaitForStartRC", "QSWaitForStart"}
UUID_RSC = "00002a53-0000-1000-8000-00805f9b34fb"

MACHINE_STATUS = {
    0x01: "Reset", 0x02: "Stopped/paused by user", 0x03: "Stopped by safety key",
    0x04: "Started/resumed by user", 0x05: "Target speed changed",
    0x06: "Target incline changed", 0x07: "Target resistance changed",
    0x08: "Target power changed", 0x09: "Target heart rate changed",
    0xFF: "Control permission lost",
}


def stamp():
    return datetime.now().isoformat(timespec="milliseconds")


class Rx:
    def __init__(self):
        self.buf = bytearray()
        self.frames = asyncio.Queue()
        self.ftms_q = asyncio.Queue()

    def tg(self, _s, data):
        chunk = bytes(data)
        if b"!" in chunk and not self.buf:
            chunk = chunk[chunk.index(b"!"):]
        self.buf.extend(chunk)
        while b"#" in self.buf:
            i = self.buf.index(ord("#"))
            self.frames.put_nowait(bytes(self.buf[: i + 1]))
            del self.buf[: i + 1]
        # unknown commands are answered "!CMD:ERROR" without terminator
        if self.buf.startswith(b"!") and self.buf.endswith(b":ERROR"):
            self.frames.put_nowait(bytes(self.buf))
            self.buf.clear()

    def reset(self):
        self.buf.clear()
        while not self.frames.empty():
            self.frames.get_nowait()


class Recorder:
    def __init__(self, txt, csvfile):
        self.t0 = time.monotonic()
        self.txt = txt
        self.csv = csv.writer(csvfile)
        self.csv.writerow(["t_rel_s", "wallclock", "utc", "signal", "value"])
        self.csvfile = csvfile
        self.series = {}

    def rel(self):
        return time.monotonic() - self.t0

    def log(self, line):
        msg = f"[{stamp()} +{self.rel():7.3f}s] {line}"
        print(msg, flush=True)
        self.txt.write(msg + "\n")

    def sig(self, name, value):
        t = self.rel()
        self.csv.writerow([f"{t:.3f}", stamp(),
                           datetime.now(timezone.utc).isoformat(timespec="milliseconds"), name, value])
        self.series.setdefault(name, []).append((t, value))
        self.csvfile.flush()


def decode_treadmill_data(p: bytes):
    """FTMS 0x2ACD: returns dict with speed_kmh / incline_pct when present."""
    out = {}
    if len(p) < 2:
        return out
    flags = p[0] | (p[1] << 8)
    i = 2
    if not flags & 0x0001 and len(p) >= i + 2:          # instantaneous speed
        out["speed_kmh"] = struct.unpack_from("<H", p, i)[0] / 100.0
        i += 2
    if flags & 0x0002:                                    # average speed
        i += 2
    if flags & 0x0004:                                    # total distance (uint24)
        i += 3
    if flags & 0x0008 and len(p) >= i + 4:               # incline + ramp angle
        out["incline_pct"] = struct.unpack_from("<h", p, i)[0] / 10.0
        i += 4
    return out


async def tg_cmd(client, rx, cmd, byte_delay, write_resp, timeout=4.0):
    rx.reset()
    for b in cmd.encode("ascii"):
        await client.write_gatt_char(TG_WRITE, bytes([b]), response=write_resp)
        if byte_delay:
            await asyncio.sleep(byte_delay)
    try:
        f = await asyncio.wait_for(rx.frames.get(), timeout)
        return f.decode("latin-1", "replace").strip(), "OK"
    except asyncio.TimeoutError:
        part = bytes(rx.buf).decode("latin-1", "replace")
        rx.buf.clear()
        return part, "TIMEOUT"


async def ftms_cmd(client, rx, payload, rec):
    while not rx.ftms_q.empty():
        rx.ftms_q.get_nowait()
    rec.log(f"FTMS TX {payload.hex(' ')}")
    await client.write_gatt_char(FTMS_CP, payload, response=True)
    try:
        while True:
            ans = await asyncio.wait_for(rx.ftms_q.get(), 4.0)
            rec.log(f"FTMS RX {ans.hex(' ')}")
            if len(ans) >= 3 and ans[0] == 0x80 and ans[1] == payload[0]:
                return ans[2] == 1
    except asyncio.TimeoutError:
        rec.log("FTMS response timeout")
        return False


def parse_dumpio(text):
    text = text.replace("!DUMPIO:", "\n")
    return dict(re.findall(r"(?m)^(?:OUT|IN|PWM)\s+(\w+)\s*=\s*(\d+)", text))


def parse_status(text):
    st = re.search(r"Status:\s*(QS\w+)", text)
    ms = re.search(r"MeasSpeed:\s*([\d.]+)", text)
    return (st.group(1) if st else None), (float(ms.group(1)) if ms else None)


async def main():
    ap = argparse.ArgumentParser(description="MYRUN fast fault monitor")
    ap.add_argument("--address", default="E0:86:1D:FA:4D:A0")
    ap.add_argument("--name", default="MyRun")
    ap.add_argument("--duration", type=float, default=120.0, help="max. monitoring seconds")
    ap.add_argument("--dumpio-every", type=float, default=3.0, help="seconds between @DUMPIO# polls")
    ap.add_argument("--status-every", type=float, default=5.0, help="seconds between @STATUS# polls")
    ap.add_argument("--post-fault", type=float, default=8.0, help="keep logging N s after fault detected")
    ap.add_argument("--byte-delay", type=float, default=0.04, help="pause between command bytes")
    ap.add_argument("--no-write-response", action="store_true",
                    help="write command bytes without response (faster; test whether firmware accepts)")
    ap.add_argument("--no-start", action="store_true", help="passive mode: monitor without sending START")
    ap.add_argument("--listen-only", action="store_true",
                    help="purely passive: no init, no commands at all; only GATT inventory + notifications")
    ap.add_argument("--output", help="base filename (without extension)")
    a = ap.parse_args()
    write_resp = not a.no_write_response

    if a.listen_only:
        a.no_start = True
    if not a.no_start:
        print("\nACHTUNG: FTMS START lässt das Band mit ca. 1,2 km/h anlaufen.")
        print("Niemand auf dem Band, Gerät montiert, Not-Aus griffbereit.")
        try:
            input("Enter = Start freigeben,  Strg+C = Abbruch ... ")
        except (KeyboardInterrupt, EOFError):
            print("\nAbbruch ohne Verbindung.")
            return 1

    base = a.output or f"myrun_fast_monitor_{datetime.now():%Y%m%d_%H%M%S}"
    txt_path, csv_path = Path(base + ".txt"), Path(base + ".csv")

    dev = await BleakScanner.find_device_by_address(a.address, timeout=15)
    if dev is None:
        dev = await BleakScanner.find_device_by_filter(
            lambda d, ad: a.name.lower() in (d.name or ad.local_name or "").lower(), timeout=20)
    if dev is None:
        print("MYRUN nicht gefunden (andere BLE-Apps trennen).")
        return 2

    rx = Rx()
    with txt_path.open("w", encoding="utf-8", buffering=1) as txt, \
         csv_path.open("w", newline="", encoding="utf-8") as cf:
        rec = Recorder(txt, cf)
        rec.log(f"DEVICE {dev.name} {dev.address}; start={'no' if a.no_start else 'yes'}; "
                f"byte_delay={a.byte_delay}; write_response={write_resp}")

        async with BleakClient(dev, timeout=20) as client:
            # --- custom channel + FTMS control point
            await client.start_notify(TG_NOTIFY, rx.tg)

            def ftms_cb(_s, d):
                d = bytes(d)
                rec.sig("ftms_cp", d.hex(" "))
                rx.ftms_q.put_nowait(d)

            await client.start_notify(FTMS_CP, ftms_cb)

            # --- passively subscribe to everything else that notifies/indicates
            def make_cb(uuid):
                def cb(_s, d):
                    d = bytes(d)
                    u = uuid.lower()
                    if u == UUID_TREADMILL_DATA:
                        dec = decode_treadmill_data(d)
                        if "speed_kmh" in dec:
                            v = dec["speed_kmh"]
                            prev = last_speed.get("ftms")
                            # 0x2ACD carries the SETPOINT on this firmware: it kept
                            # reporting 1.2 km/h in QSHardwareFault with the belt
                            # standing still (07.11.). So it is only logged, never
                            # used as a speed-loss trigger.
                            if prev is not None and abs(prev - v) >= 0.05:
                                rec.log(f"FTMS 0x2ACD speed field (setpoint) {prev:.2f} -> {v:.2f} km/h")
                            last_speed["ftms"] = v
                            rec.sig("ftms_speed_kmh", v)
                        if "incline_pct" in dec:
                            rec.sig("ftms_incline_pct", dec["incline_pct"])
                        rec.sig("raw_2acd", d.hex(" "))
                    elif u == UUID_MACHINE_STATUS:
                        txtv = MACHINE_STATUS.get(d[0], f"0x{d[0]:02x}") if d else "-"
                        rec.sig("machine_status", f"{txtv} [{d.hex(' ')}]")
                        rec.log(f"MACHINE STATUS {txtv} [{d.hex(' ')}]")
                    elif u == UUID_TRAINING_STATUS:
                        rec.sig("training_status", d.hex(" "))
                    elif u == UUID_RSC and len(d) >= 4:
                        rec.sig("rsc_speed_kmh", round(int.from_bytes(d[1:3], "little") * 3.6 / 256, 3))
                        rec.sig("rsc_cadence", d[3])
                    else:
                        rec.sig(f"raw_{u[4:8]}", d.hex(" "))
                    counters[u[4:8]] = counters.get(u[4:8], 0) + 1
                return cb

            subscribed = []
            counters = {}
            last_speed = {}
            loss_flag = {"pending": None, "done": 0}
            for svc in client.services:
                for ch in svc.characteristics:
                    rec.log(f"GATT {svc.uuid} / {ch.uuid} ({','.join(ch.properties)})")
            for svc in client.services:
                for ch in svc.characteristics:
                    u = ch.uuid.lower()
                    if u in (TG_NOTIFY, FTMS_CP):
                        continue
                    if "notify" in ch.properties or "indicate" in ch.properties:
                        try:
                            await client.start_notify(ch, make_cb(u))
                            subscribed.append(u)
                        except Exception as e:
                            rec.log(f"subscribe failed {u}: {e}")
            rec.log("SUBSCRIBED " + ", ".join(subscribed))

            if a.listen_only:
                rec.log(f"LISTEN-ONLY for {a.duration:.0f} s (no init, no commands)")
                await asyncio.sleep(a.duration)
                el = max(rec.rel(), 1e-6)
                rec.log("NOTIFY packets per UUID: " + ", ".join(
                    f"{k}={n} ({n / el:.1f}/s)" for k, n in sorted(counters.items())))
                return 0

            # --- init as QZ / existing scripts (without @SETDATE!)
            await client.write_gatt_char(FTMS_CP, QZ_INIT, response=True)
            await asyncio.sleep(0.8)
            for c in SETUP:
                r, s = await tg_cmd(client, rx, c, a.byte_delay, write_resp)
                rec.log(f"SETUP {c} {s} {r!r}")
            for label, c in (("FWVER", "@FWVER#"), ("ERRORLOG_START", "@RERRORLOG#")):
                r, s = await tg_cmd(client, rx, c, a.byte_delay, write_resp)
                rec.log(f"{label} {s} {r!r}")

            r, s = await tg_cmd(client, rx, "@STATUS#", a.byte_delay, write_resp)
            state, _ = parse_status(r)
            rec.log(f"BASELINE STATUS {s} {state}")
            r2, s2 = await tg_cmd(client, rx, "@DUMPIO#", a.byte_delay, write_resp)
            io_prev = parse_dumpio(r2)
            rec.log(f"BASELINE DUMPIO {s2} {io_prev}")
            for k, v in io_prev.items():
                rec.sig(f"io_{k}", int(v))

            start_attempted = False
            t_start = None
            if not a.no_start and (s != "OK" or state not in SAFE_START_STATES):
                rec.log(f"Baseline state {state!r} ({s}) not a confirmed start state "
                        f"{sorted(SAFE_START_STATES)} -> START suppressed. Power-cycle first.")
                return 4

            # --- fast loop
            loop = asyncio.get_running_loop()
            t_end = loop.time() + a.duration
            next_dump = loop.time() + a.dumpio_every
            next_stat = loop.time() + a.status_every
            fault_at = None
            cycles = 0
            try:
                if not a.no_start:
                    start_attempted = True        # STOP is sent even if no ACK arrives
                    t_start = rec.rel()
                    ok = await ftms_cmd(client, rx, bytes([0x07]), rec)
                    rec.log(f"START acknowledged = {ok}")
                while loop.time() < t_end:
                    r, s = await tg_cmd(client, rx, "@RPWM#", a.byte_delay, write_resp, 2.5)
                    rec.sig("raw_rpwm", f"{s} {r!r}")
                    m = re.search(r"PWM=([\d.]+)%", r)
                    if m:
                        rec.sig("pwm_pct", float(m.group(1)))
                    else:
                        rec.log(f"PARSE FAIL @RPWM# {s} {r!r}")
                    r, s = await tg_cmd(client, rx, "@RENC#", a.byte_delay, write_resp, 2.5)
                    rec.sig("raw_renc", f"{s} {r!r}")
                    m = re.search(r"([\d.]+)\s*Hz\s*->\s*([\d.]+)\s*km/h", r)
                    if not m:
                        rec.log(f"PARSE FAIL @RENC# {s} {r!r}")
                    if m:
                        hz = float(m.group(1))
                        prev = last_speed.get("enc")
                        if prev is not None and prev > 0 and hz == 0:
                            rec.log(f"SPEED_LOSS (encoder) {prev:g} Hz -> 0 Hz")
                            loss_flag["pending"] = loss_flag["pending"] or "encoder"
                        last_speed["enc"] = hz
                        rec.sig("enc_hz", hz)
                        rec.sig("enc_kmh", float(m.group(2)))
                    if loss_flag["pending"] and loss_flag["done"] < 2:
                        # immediate snapshot right after a speed loss
                        src = loss_flag["pending"]
                        loss_flag["pending"] = None
                        loss_flag["done"] += 1
                        tnow = rec.rel()
                        ages = []
                        for nm in ("pwm_pct", "enc_hz", "meas_speed"):
                            ser = rec.series.get(nm)
                            if ser:
                                ages.append(f"{nm}={ser[-1][1]} (age {tnow - ser[-1][0]:.2f}s)")
                        rec.log(f"SNAPSHOT after SPEED_LOSS [{src}]: " + ", ".join(ages))
                        r, s = await tg_cmd(client, rx, "@DUMPIO#", a.byte_delay, write_resp)
                        rec.log(f"SNAPSHOT DUMPIO {s} {r!r}")
                        io = parse_dumpio(r)
                        for k, v in io.items():
                            if io_prev.get(k) != v:
                                rec.log(f"IO CHANGE {k}: {io_prev.get(k)} -> {v}")
                                rec.sig(f"io_{k}", int(v))
                        io_prev.update(io)
                        r, s = await tg_cmd(client, rx, "@STATUS#", a.byte_delay, write_resp)
                        rec.log(f"SNAPSHOT STATUS {s} {r!r}")
                    now = loop.time()
                    if now >= next_dump:
                        next_dump = now + a.dumpio_every
                        r, s = await tg_cmd(client, rx, "@DUMPIO#", a.byte_delay, write_resp)
                        io = parse_dumpio(r)
                        for k, v in io.items():
                            if io_prev.get(k) != v:
                                rec.log(f"IO CHANGE {k}: {io_prev.get(k)} -> {v}")
                                rec.sig(f"io_{k}", int(v))
                        io_prev.update(io)
                    if now >= next_stat:
                        next_stat = now + a.status_every
                        r, s = await tg_cmd(client, rx, "@STATUS#", a.byte_delay, write_resp)
                        st, ms = parse_status(r)
                        if st:
                            if st != last_speed.get("state"):
                                rec.log(f"STATE {last_speed.get('state')} -> {st}")
                            last_speed["state"] = st
                            rec.sig("state", st)
                        if ms is not None:
                            prev = last_speed.get("meas")
                            if (prev is not None and prev > 0.2 and ms == 0
                                    and st not in ("QSStoppingRC", "QSStopping")):
                                rec.log(f"SPEED_LOSS (MeasSpeed) {prev:g} -> 0 km/h, state {st}")
                                loss_flag["pending"] = loss_flag["pending"] or "MeasSpeed"
                            last_speed["meas"] = ms
                            rec.sig("meas_speed", ms)
                        if st == "QSHardwareFault" and fault_at is None:
                            fault_at = loop.time()
                            rec.log(f"HARDWARE FAULT detected, logging {a.post_fault:.0f} s more")
                            t_end = min(t_end, fault_at + a.post_fault)
                    cycles += 1
            except (KeyboardInterrupt, asyncio.CancelledError):
                rec.log("interrupted")
            except Exception as e:
                rec.log(f"ERROR in monitor loop: {type(e).__name__}: {e}")
            finally:
                if start_attempted and client.is_connected:
                    try:
                        ok = await ftms_cmd(client, rx, bytes([0x08, 0x01]), rec)
                        rec.log(f"STOP acknowledged = {ok} (verify belt physically)")
                    except Exception as e:
                        rec.log(f"STOP error {e}")
                for label, c in (("ERRORLOG_END", "@RERRORLOG#"), ("STATUS_END", "@STATUS#"),
                                 ("DUMPIO_END", "@DUMPIO#")):
                    try:
                        r, s = await tg_cmd(client, rx, c, a.byte_delay, write_resp)
                        rec.log(f"{label} {s} {r!r}")
                    except Exception as e:
                        rec.log(f"{label} error {e}")
                el = max(rec.rel(), 1e-6)
                rec.log("NOTIFY packets per UUID: " + ", ".join(
                    f"{k}={n} ({n / el:.1f}/s)" for k, n in sorted(counters.items())))
                rec.log(f"END cycles={cycles}, mean poll period "
                        f"{(rec.rel() / max(cycles, 1)):.3f} s per RPWM+RENC pair")

        # --- summary
        S = rec.series
        def first(name, pred):
            return next((t for t, v in S.get(name, []) if pred(v)), None)
        def last(name, pred):
            return next((t for t, v in reversed(S.get(name, [])) if pred(v)), None)
        t0 = t_start if t_start is not None else 0.0
        def after(name):
            return [(t, v) for t, v in S.get(name, []) if t >= t0]
        def drops(name):
            """first transitions >0 -> 0 after START: (t_last_pos, t_first_zero)"""
            out, prev = [], None
            for t, v in after(name):
                if prev is not None and prev[1] > 0 and v == 0:
                    out.append((prev[0], t))
                prev = (t, v)
            return out
        rec.log(f"SUMMARY (times in s since script start; START at {t_start})")
        for nm in ("enc_hz", "meas_speed"):
            ser = after(nm)
            t_on = next((t for t, v in ser if v > 0), None)
            rec.log(f"  {nm}: samples={len(ser)}, first >0 at {t_on}")
            for t_pos, t_zero in drops(nm):
                pw = [(round(t, 2), v) for t, v in after("pwm_pct") if t_pos - 1.0 <= t <= t_zero + 1.0]
                rec.log(f"    DROP: last >0 at {t_pos:.2f}, first 0 at {t_zero:.2f} "
                        f"(resolution {t_zero - t_pos:.2f} s); PWM % nearby: {pw}")
        t_pow = next((t for t, v in after("io_EM_POWENA") if v == 0), None)
        rec.log(f"  first EM_POWENA=0 after START at {t_pow}")
        rec.log(f"  files: {txt_path.resolve()} / {csv_path.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("Abgebrochen")
        sys.exit(130)
