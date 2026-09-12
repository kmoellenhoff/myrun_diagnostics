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

## Safety

`myrun_dump.py` is intended to be read-only apart from the connection/setup sequence.

`myrun_incline_test.py` sends real FTMS control commands. In particular, it sends `START/RESUME`, an incline request, and `STOP/PAUSE`.

During the incline test:

- nobody should stand on the treadmill,
- the treadmill must be fully assembled and mechanically safe,
- do not run the test with the incline linkage disconnected or unsupported,
- keep the area around the treadmill clear.

The script does **not** set a belt speed, but `START/RESUME` is still a real machine-control command. `STOP/PAUSE` is sent in a `finally` block whenever the BLE connection is still available after a start attempt.

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
