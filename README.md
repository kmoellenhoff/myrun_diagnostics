# myrun_diagnostics

Small Linux/Python BLE diagnostic tools for the **Technogym MYRUN** treadmill.

The scripts were created while diagnosing a MYRUN DCKA-series machine whose incline mechanism no longer moved and whose lower-kit belt drive (Gefran GIRT S6T30) faults on start. They use standard FTMS plus Technogym's proprietary BLE command channel to read diagnostic information and, in the active tests, issue controlled FTMS START/STOP and low-incline requests.

## Contents

### `myrun_dump.py`

Read-only diagnostic dump.

It connects to the MYRUN over BLE, performs the initialization sequence used by qdomyos-zwift (QZ), then runs these Technogym service-style commands:

- `@FWVER#`
- `@RERRORLOG#`
- `@STATUS#`
- `@RADCEXT#`
- `@DUMPIO#`

The MYRUN often returns the proprietary text protocol one byte per BLE notification. The script reassembles those bytes into readable `!...#` response frames and writes a timestamped text report.

### `myrun_incline_test.py`

Controlled incline diagnostic.

The script:

1. performs the same BLE/QZ-style initialization,
2. captures a baseline with `DUMPIO`, `STATUS`, and `RADCEXT`,
3. sends FTMS `START/RESUME`,
4. records controller status,
5. requests a small incline, default **2.0 %**,
6. immediately captures `DUMPIO`, `STATUS`, and `RADCEXT`,
7. repeats the incline request once,
8. requests **0.0 %** again,
9. sends FTMS `STOP/PAUSE`,
10. captures a final diagnostic state.

No speed command is sent by this script.

The test is intended to distinguish, for example, between:

- a request rejected by the high-level controller,
- a CPU/controller that asserts `ELEVAT_UP` / `ELEV_DOWN` but produces no physical motion,
- an incline feedback signal that does or does not change.

### `myrun_fault_monitor.py`

Timestamped fault-transition monitor with **actively confirmed FTMS START/RESUME**.

The monitor first reads firmware, the error log and the baseline state. Before connecting or sending any motor command, the operator must type the exact confirmation `START FREIGEBEN` in the terminal. It then sends FTMS `START/RESUME` **only if the baseline STATUS was successfully read and did not already report `QSHardwareFault`**.

It records repeated raw `@STATUS#` and `@DUMPIO#` responses, highlights state and I/O transitions, ends on `QSHardwareFault` (or after the configured duration), attempts FTMS `STOP/PAUSE`, and saves final error log/status/I/O snapshots.

**Important behavior observed:** FTMS START/RESUME automatically requested **1.2 km/h**, despite no explicit speed command. A faulty controller may reject the FTMS STOP command: on the tested MYRUN it returned `80 08 04` (`OPERATION_FAILED`) after HF904. **Software STOP is not a substitute for the physical safety stop.**

The optional `--incline 1.0` requests one incline adjustment after an acknowledged successful START. **Do not use it on a partially dismantled or electrically faulty treadmill.** The default is **no incline adjustment**.

### `myrun_fast_monitor.py`

Faster, higher-resolution fault monitor for the belt-drive failure. It has three modes:

| Mode | Sends | Use it for |
| --- | --- | --- |
| *default* (active), e.g. `--duration 90` | init, polling, FTMS `START`, FTMS `STOP` | reproducing the fault under script control |
| `--no-start` | init and polling, but **no** `START`/`STOP` | watching the controller without a script-commanded start |
| `--listen-only` | **nothing** (no init, no commands) | starting the belt manually from the console while recording |

**Active mode (default).** Before connecting, the script asks the operator to press Enter (Ctrl+C aborts). After the init sequence it reads firmware, error log, a baseline `@STATUS#` and `@DUMPIO#`. FTMS `START/RESUME` is sent **only if the baseline `@STATUS#` was read successfully and reports `QSWaitForStart` or `QSWaitForStartRC`**; in any other state (e.g. `QSHardwareFault`) the script aborts without starting and asks for a power cycle. Once a START has been attempted, FTMS `STOP/PAUSE` is **always** sent at the end, even if the START was not acknowledged. `--duration` is the maximum monitoring time (default 120 s).

**`--no-start`.** Polls `@RPWM#`, `@RENC#`, `@DUMPIO#` and `@STATUS#` exactly as in active mode, but sends no `START`/`STOP`. It still sends the FTMS request-control init (`00 93 F0 …`) and the Technogym setup commands. On 7 November 2026 a `--no-start` run coincided with the console refusing a manual start and repeated FTMS Machine Status "Target incline changed" notifications. **If you want to start the belt from the console, use `--listen-only` instead.**

**`--listen-only`.** Connects, logs the GATT inventory and subscribes to notifications, then only records them for `--duration` seconds. No init, no Technogym commands and no FTMS control-point writes are sent.

What it records:

- The full GATT inventory and **all** notify/indicate characteristics, with ms timestamps: FTMS Treadmill Data (0x2ACD, speed and incline decoded), Machine Status (0x2ADA, decoded), Training Status (0x2AD3), RSC speed/cadence (0x2A53), FTMS Control Point responses, and any other characteristic as raw hex. Approach taken from qdomyos-zwift, which subscribes to every notifying characteristic. Packets per characteristic (rate) are logged at the end.
- In the fast loop only the short replies `@RPWM#` (PWM %) and `@RENC#` (encoder Hz and km/h); `@DUMPIO#` / `@STATUS#` only every few seconds (`--dumpio-every`, `--status-every`). The long replies are the bottleneck because the firmware answers one byte per notification. Raw replies and parse failures are logged too.
- Live `SPEED_LOSS` markers when the encoder (`@RENC#`) drops from >0 Hz to 0 Hz, or `MeasSpeed` in `@STATUS#` drops from >0.2 km/h to 0 outside `QSStopping*`. Each loss (at most two) triggers an immediate `@DUMPIO#` + `@STATUS#` snapshot. `@STATUS#` state changes and `@DUMPIO#` I/O changes are logged as they happen.
- When `@STATUS#` reports `QSHardwareFault`, logging continues for `--post-fault` seconds (default 8), then STOP (active mode only) and final error log, status and I/O snapshots are taken.

**Start before power-on (`--wait-device`, `--wait-ready`).** `--wait-device N` keeps scanning up to N seconds, so the script can be started before the treadmill is switched on and logs from the first moment after boot. After connecting it polls `@STATUS#` until `QSWaitForStart*` (up to `--wait-ready`, default 150 s with `--wait-device`). The Enter prompt for `START` now always appears after the connection and the ready check, immediately before `START` is sent.

```bash
python3 myrun_fast_monitor.py --wait-device 300 --duration 150 --ramp
```

**Timed speed/incline profile (`--steps`, `--ramp`).** In active mode the script can change speed and incline at fixed times after `START` via the FTMS Control Point (`0x02` Set Target Speed in 0.01 km/h, `0x03` Set Target Inclination in 0.1 %). `--ramp` is a shortcut for `30:speed=2.5,60:speed=2.9,75:incline=2.0,90:speed=2.5,105:incline=0,120:speed=1.2` (seconds after START). Hard limits: speed 0.8–2.9 km/h (below the runner-detector threshold of 3.0 km/h), incline 0–5 %. Steps stop after a hardware fault; if an incline step was sent, incline 0 % is requested again before `STOP`. Steps are executed at the next poll cycle, so the actual send time (logged as `STEP +x s`) can lag the planned time by a few seconds.

```bash
python3 myrun_fast_monitor.py --duration 150 --ramp
python3 myrun_fast_monitor.py --duration 120 --steps "30:speed=2.0,60:incline=1.5,90:incline=0"
```
- A summary at the end: per `enc_hz` / `meas_speed`, the first value >0 after START and every >0 → 0 drop (with time resolution and the PWM % values around it), plus the first `EM_POWENA=0` after START and the mean polling period.

Output: `<base>.txt` (log) and `<base>.csv` with the columns `t_rel_s, wallclock, utc, signal, value`, for plotting. The default base name is `myrun_fast_monitor_YYYYMMDD_HHMMSS`.

**Speed field caveat:** On firmware `WFW0699_BA30.35167` the speed field in FTMS Treadmill Data (0x2ACD) is the **setpoint**, not the measured belt speed: it kept reporting 1.2 km/h in `QSHardwareFault` while the belt was standing still. The monitor therefore only logs it and detects speed loss exclusively from `@RENC#` (encoder) and `MeasSpeed` in `@STATUS#`.

Unlike QZ it does **not** send `@SETDATE` (QZ writes a fixed 2022 date, which would corrupt error-log timestamps).

### `myrun_probe.py`

Read-only command probe. After the usual init sequence it sends each read command once and writes the raw reply (text and hex) plus an overview to `myrun_probe_YYYYMMDD_HHMMSS.txt`. No FTMS START/STOP and no incline commands are sent.

- Default command list: the read commands documented in the 2016 service manual (`@FWVER#`, `@RENC#`, `@RADCEXT#`, `@DUMPIO#`, `@STATUS#`, `@RERRORLOG#`, `@RKPWM#`, `@RQSPAR#`, `@RSTAT#`, `@RTASKHANG#`, `@RRUNDETMINSP#`, `@GETDATE#`, `@RTG_ID#`, `@RDS_UP#`, `@RDS_DOWN#`) plus two **undocumented** commands that answer on `WFW0699_BA30.35167`: `@RPWM#` (PWM duty cycle in %) and `@RADC#` (short incline ADC reading).
- `--guess` additionally tries a list of undocumented, guessed read/help commands (`@HELP#`, `@RTEMP#`, `@RLKSTAT#`, `@RVBUS#`, …). Unknown commands are answered with `!CMD:ERROR` (without `#`), which the probe recognizes as a reply.
- `--extra CMD` (repeatable) probes additional commands; `@` and `#` are added if missing.
- `--watch N` repeats `@RENC#`, `@STATUS#` and `@DUMPIO#` for N seconds afterwards.
- Hard block list: any command matching a write/reset/calibrate pattern (`RESET`, `SET`, `@S…` except `@STATUS#`, `INIT`, `CAL`, `ELEV`, `FORCE`, `SUSPEND`, `STG_ID`, `WRITE`, `ERASE`, `CLEAR`, `FORMAT`, `UPD`, `BOOT`, `FLASH`) is never sent, including commands passed via `--extra`; it is logged as blocked instead. (The fixed init/setup sequence is not subject to this list.)

### `myrun_renc_watch.py`

Minimal encoder watch. Writes nothing except the read command `@RENC#`
(optionally one of `@STATUS#`, `@DUMPIO#`, `@RPWM#` every 5th cycle) on the
Technogym text channel: no FTMS request-control init, no setup commands, no
START/STOP. Intended for pushing the belt by hand to check whether the encoder
signal still reaches the console through the lower kit, e.g. while the drive is
locked and again after a power cycle. Output: CSV with
`t_rel_s, wallclock, enc_hz, enc_kmh, raw`.

    python3 myrun_renc_watch.py --duration 60

## Hardware documentation

### Fotoatlas und Schaltplan (Branch `110926`)

- [Alle 110 Originalfotos zugeordnet, mit Raster und Gewissheit](docs/atlas_110926/README.md)
- [Belegter Teilschaltplan, Quellen und weitere Fehlereingrenzung](docs/schaltplan_110926/README.md)
- [Stromloser Messplan mit acht markierten Originalmakros und Messwertvorlage](docs/messplan_stromlos_2026-11-08/MESSPLAN.md)

Die vorhandenen Originalfotos und Claudes Koordinatensystem bleiben erhalten. Offene Pin-/Netzzuordnungen werden ausdrücklich gekennzeichnet.


[`docs/HARDWARE.md`](docs/HARDWARE.md) (also as [PDF](docs/HARDWARE.pdf)) collects what is known about the lower kit (Gefran GIRT S6T30): block diagram, board areas and identified parts, connector pinouts for P2 (console, 18 pin) and P4 (speed sensor) from both plug and solder side, DUMPIO signals, LED behaviour, fault sequence, repairs and corrosion findings. Each statement is tagged as measured, observed, from a manual, or inferred.

## Requirements

- Linux with working BlueZ/Bluetooth LE
- Python 3
- [`bleak`](https://github.com/hbldh/bleak)

Install:

```bash
python3 -m pip install --user bleak
```

Before running a script, disconnect other applications from the MYRUN, such as:

- Technogym app
- nRF Connect
- qdomyos-zwift / QZ
- other BLE terminal apps

## Usage

### Read-only diagnostic dump

```bash
python3 myrun_dump.py
```

Optionally specify the BLE address:

```bash
python3 myrun_dump.py --address E0:86:1D:FA:4D:A0
```

A report similar to this is created in the current directory:

```text
myrun_diagnostic_YYYYMMDD_HHMMSS.txt
```

### Controlled incline test

```bash
python3 myrun_incline_test.py
```

Specify a different small target incline:

```bash
python3 myrun_incline_test.py --target 1.0
```

Or both address and output file:

```bash
python3 myrun_incline_test.py \
  --address E0:86:1D:FA:4D:A0 \
  --target 2.0 \
  --output incline_test.txt
```

For safety, the script only accepts test targets from **0.5 % to 5.0 %**.

### Fault-transition monitor (actively starts the belt)

```bash
python3 myrun_fault_monitor.py --duration 180
```

The program waits for the exact terminal confirmation `START FREIGEBEN` before any BLE connection / start attempt. **Nobody may be on the belt; the treadmill must be completely assembled, mechanically safe and ready to stop using the physical emergency stop.**

Optional flags:

```bash
python3 myrun_fault_monitor.py --duration 120 --interval 0.2 --output myrun_fault.txt
# Only on a fully assembled, demonstrably safe machine:
python3 myrun_fault_monitor.py --duration 120 --incline 1.0
```

- `--duration`: monitoring time after START, in seconds (default 120).
- `--interval`: delay between complete STATUS/DUMPIO polling pairs, **not** the actual sample period; BLE calls take much longer (default 0.2 seconds).
- `--incline`: one optional target of 0.5–2.0% after START success; default: disabled.
- `--address`, `--name`, `--output`: device selection / report path.

### Fast fault monitor

```bash
# Active: press Enter to allow START; starts only from QSWaitForStart/QSWaitForStartRC
python3 myrun_fast_monitor.py --duration 90
# Poll RPWM/RENC/DUMPIO/STATUS without START/STOP (still sends the init)
python3 myrun_fast_monitor.py --no-start --duration 120
# Send nothing; start the belt from the console while recording
python3 myrun_fast_monitor.py --listen-only --duration 120
```

- `--duration`: maximum monitoring time in seconds (default 120); with `--listen-only`, the listening time.
- `--dumpio-every` / `--status-every`: seconds between `@DUMPIO#` / `@STATUS#` polls (defaults 3 and 5).
- `--post-fault`: keep logging N seconds after `QSHardwareFault` is detected (default 8).
- `--byte-delay`: pause between command bytes (default 0.04 s); `--no-write-response`: write command bytes without write response. Both only for testing faster command writes; check that the firmware still accepts the commands.
- `--no-start`, `--listen-only`: see above.
- `--address` (default `E0:86:1D:FA:4D:A0`), `--name` (default `MyRun`): device selection.
- `--output`: base filename **without extension**; `.txt` and `.csv` are appended.

### Read-only command probe

```bash
python3 myrun_probe.py
python3 myrun_probe.py --guess
python3 myrun_probe.py --extra "@RXYZ#" --extra "@RABC#"
python3 myrun_probe.py --watch 60
```

- `--address`, `--name` (default `MyRun`), `--output`: device selection / report path.

## Safety

`myrun_dump.py` and `myrun_probe.py` are intended to be read-only apart from the connection/setup sequence. `myrun_fast_monitor.py --listen-only` sends no commands at all.

`myrun_incline_test.py`, `myrun_fault_monitor.py` and `myrun_fast_monitor.py` (active mode) send real FTMS control commands. In particular, the fault monitors send `START/RESUME` (the fault monitor optionally an incline request), then attempt `STOP/PAUSE`.

Rules followed by all scripts:

- no writing, reset or calibration commands are sent (the probe hard-blocks them),
- no `@SETDATE` (it would corrupt the error-log timestamps),
- nothing is ever written to the unknown service `6e40a8d5-b5a3-f393-e0a9-e50e24dcca9e`; writes go only to the Technogym write characteristic and the FTMS Control Point listed below.

During any script start, and in particular any active test:

- nobody may be on the belt,
- the emergency stop must be within reach,
- the treadmill must be fully assembled and mechanically safe,
- do not run the test with the incline linkage disconnected or unsupported,
- keep the area around the treadmill clear.

No explicit speed command is issued, but `START/RESUME` **did cause the tested machine to request 1.2 km/h**. The active fault monitor attempts `STOP/PAUSE` at the end of monitoring, but during a hardware fault this can fail. Use the physical safety stop as needed. Never run an active test while the motor compartment is open or wiring is exposed. Disconnect mains and verify safe discharge before inspecting the motor controller or its connectors.

These tools are experimental and are not affiliated with or supported by Technogym.

## Protocol notes

On the tested MYRUN, the following BLE characteristics were observed:

```text
Technogym custom service:
beb7705e-bd66-4501-80c0-0c8f0bcca1a5

Technogym write characteristic:
df1eb8e4-1753-4bb9-a6a6-e018040af0a3

Technogym notify characteristic:
6f26de4b-dcef-4459-9465-931f1b144c20

FTMS Control Point:
00002ad9-0000-1000-8000-00805f9b34fb
```

The proprietary Technogym commands are sent **byte by byte** on the custom write characteristic. Responses are received on the notify characteristic and typically form ASCII frames beginning with `!` and ending with `#`.

The initialization currently mirrors the behavior observed in the open-source qdomyos-zwift MYRUN implementation:

```text
FTMS initialization:
00 93 F0 51 E8 1B 42 92 8E
```

followed by:

```text
@DISABLE_PACE#
@SSIUNITS#
@RJSK_EN 1#
@LJSK_EN 1#
```

The incline test uses the standard FTMS Control Point:

```text
0x07                  START / RESUME
0x03 LL HH            SET TARGET INCLINATION
0x08 0x01             STOP / PAUSE
```

Target inclination is encoded as a signed 16-bit little-endian integer in units of **0.1 %**. For example:

```text
2.0 % -> 03 14 00
```

An FTMS response of:

```text
80 03 01
```

means the target-inclination command succeeded, while:

```text
80 03 04
```

means `OPERATION_FAILED`.

FTMS Treadmill Data (0x2ACD) is not a reliable speed measurement on `WFW0699_BA30.35167`: its speed field is the **setpoint** and kept reporting 1.2 km/h in `QSHardwareFault` with the belt standing. Use `@RENC#` (encoder) or `MeasSpeed` in `@STATUS#` for the actual belt speed.

## MYRUN technical service manual and diagnostic cross-check

A publicly hosted **MYRUN TECHNOGYM Technical Service Manual**, revision **2.2 (November 2016)**, **French, 112 pages**, is available as an external PDF:

- [MYRUN service manual (PDF, manuals.plus)](https://manuals.plus/m/077b22630fbae70ec842c1934cbd88c864a0677a4bc4fdc5807af41d91ae321d.pdf)

Useful printed pages (not necessarily compatible pinouts / board LEDs on later hardware):

| Printed pages | Topic |
| --- | --- |
| 18–20 | Electrical wiring, 220 V version |
| 40–43 | Lower drive kit; diagnostic LEDs, including common RELAY ENABLED for belt and incline |
| 44–47 | DC treadmill motor, PWM input, RPM feedback and optical encoder |
| 48–51 | AC incline actuator controlled through two relays; potentiometer feedback |
| 52–54 | Emergency interlocks and motor thermal-protection circuit |
| 64–70 | ASCII diagnostic commands, including `@STATUS#`, `@DUMPIO#` and error log |
| 85–88 | Error codes and HF900 (speed-feedback) troubleshooting flowchart |
| 89–91 | Incline troubleshooting flowchart |
| 95 | Dismantling chapter **does not provide removal steps**; refers to Technogym's training course |

**Revision caveat:** The 2016 manual illustrates an older lower-controller design. The tested machine uses a **Gefran GIRT S6T30**, part **S0WR01179AG**, and firmware `WFW0699_BA30.35167`. **Do not assume D21/D50/D24 LED locations, CN J3 connector pins, component layouts or listed voltages apply unchanged to this later controller.**

The 2016 manual lists:
- **HF500–505:** lower drive-kit faults.
- **HF600:** incline motor fault.
- **HF900:** speed signal / feedback fault; worn motor brushes are noted as a possibility.
- **HF901 and HF904:** **not defined** in this edition. In particular, identifying HF901 as an “inverter error” is **not verified by this manual**.

### Observed failure on the tested device (20 October 2026)

On an operator-confirmed FTMS START, the controller reported `QSRunningRC`, `SpeedSet=1.2`, `MotON=1` and increasing `PWM_MOTOR` raw values (6486→8526), but `MeasSpeed` remained 0.0 and the belt did not move. `EM_POWENA`, `EM_STATUS`, `LOWKITENA`, `LOWKITENB` and `LK_ENABLE` simultaneously dropped to 0, recovered, then dropped again; the state changed to `QSHardwareFault` and a new HF904 was logged. Subsequent FTMS STOP returned `80 08 04`.

These observations establish a failed start under motor demand but **do not distinguish** failed power output, relay/contact problems, motor/brush wiring, an interlock/thermal trip, or a feedback fault. The older service manual makes the common lower drive/interlock path worth checking, but it does **not** definitively diagnose the S6T30.

## Background / attribution

The BLE initialization and FTMS behavior used here were derived in part by inspecting the open-source **qdomyos-zwift (QZ)** implementation for the Technogym MYRUN:

- https://github.com/cagnulein/qdomyos-zwift

This repository is intended as a focused diagnostic aid, not as a replacement for QZ.

## Tested device

Initial development/testing was performed on a Technogym MYRUN DCKA-series treadmill with firmware reporting:

```text
WFW0699_BA30.35167
```

Other hardware revisions or firmware versions may behave differently.

## License

Copyright (c) 2026 Klaus Möllenhoff

Licensed under the European Union Public Licence v1.2 (EUPL-1.2); see [`LICENSE`](LICENSE).

Provided as is, without warranty and without support. Use at your own risk: these tools talk to a motorized treadmill, and a software STOP is no substitute for the physical safety stop.

This is an independent hobby project, not affiliated with or endorsed by Technogym. Technogym and MYRUN are trademarks of their respective owner. The BLE initialization was derived in part from inspecting the open-source qdomyos-zwift project (GPL-3.0); this repository contains its own Python implementation.
