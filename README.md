# myrun_diagnostics

Small Linux/Python BLE diagnostic tools for the **Technogym MYRUN** treadmill.

The scripts were created while diagnosing a MYRUN DCKA-series machine whose incline mechanism no longer moved. They use standard FTMS plus Technogym's proprietary BLE command channel to read diagnostic information and, in the incline test, issue a controlled low-incline request.

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

## Safety

`myrun_dump.py` is intended to be read-only apart from the connection/setup sequence.

`myrun_incline_test.py` and `myrun_fault_monitor.py` send real FTMS control commands. In particular, the fault monitor sends `START/RESUME`, and optionally an incline request, then attempts `STOP/PAUSE`.

During any active test:

- nobody should stand on the treadmill,
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
