# GIRT S6T30 – component inventory from macro photos (11/08/2026)

Source: 41 front + 57 back macro photos and one backlight overview by the owner. Certainty: **P** = printed text read in photo, **I** = inferred. Everything is own observation of a lawfully owned board (see disclaimer in HARDWARE.md).

## Logic strip next to the optocouplers (mains-side logic, front, left edge of signal area)
| Part | Marking read (P) | Count / note |
|---|---|---|
| Optocoupler | `VO617A-8` (Vishay, SMD-4, CTR 130–260 %) | **8** in one column next to the 14-pin P602 side (earlier estimate "~10" to be rechecked at other places) |
| Hex Schmitt inverter | `74ACT14G` (ON Semi, SO-14) | **2** |
| Comparator | `2903` (LM2903, SO-8) | 1 |
| RS-485 transceiver | `ADM485` (Analog Devices, SO-8) | 1 – new finding; purpose unknown (console link? isolation?) [I] |
| Voltage regulator | `78L05A` (ST, SO-8) | **2**, one at each end of the strip (top and bottom) |
| Solid-state relay | `CPC1017N` (Clare/IXYS, SOP-4), next to two SOT-223 regulators | 1 |
| MCU | QFP-32 near P13/P70, marking illegible | 1 |
| EEPROM | SO-8 beside MCU (24C32 per earlier reading) | 1 |

## Connectors/test points seen
P2 (2×9, console), P3 (3-pin POT / +5 V, mains-side), P4 (4-pin TACHO/+12V/0V), **P602 (2×7 header, blue, debug/programming, mains side – do not connect)**, P601 (2-pin RST/0VA), P600 (2-pin, NTC next to Q2), P70 (6-pin, hole row, debug), P13 (test pad), P400 (2-pin, 0V24/+24V – relay coil supply), DC MOTOR (L+ orange / L− grey), UP/DOWN 3-pin (WHITE/COM, DOWN, UP, BLACK), AC LINE (BROWN L, LIGHT BLUE N), FUSE MOT, test points 0VA/+5VA, +12VISO/0VISO, ±12VA.
Parts seen: 3 relays (1 Schrack RT334024 orange, 2 Panasonic grey), 3 mains-filter chokes (C301–C304 area), toroid RT700 / large toroid, DC link electrolytic `S890A16E U12 GIRT 140421 V.10.05` (label), transformer ETI349X4 (Falco), aluminum heatsink with Q1/Q2/D3 (green isolators).

## Back side (solder side)
- Large copper pours on the mains side, slots (isolation) between mains and logic; backlight shows continuous copper only in the pour regions, signal area dense two-layer-looking tracks (layer count not yet confirmed).
- LED labels LINE / +5V / STS1 / STS2 (SMD LEDs), SO-20 IC (marking illegible) bottom middle (back), three 4702 / 47R0 SMD resistors, 4× `R020` shunt resistors (0.02 Ω) next to heatsink, two `471` SMD power resistors, 4753 (475 kΩ) chains with diodes at the lower left edge.
- P2 solder pads at top centre (two rows).

## Open
Full per-net table not started; next steps need grid + IDs (see report section 8).

## Overview drafts
See `docs/GIRT_Platinen_Uebersicht_Entwurf.pdf` (v2, grid A-L x 1-6, both variants): variant A = front as photographed + back flipped vertically (`docs/img/overview_front.jpg`, `overview_back_flipped.jpg`); variant B = back as photographed (readable text) + front flipped vertically (`overview_back_upright.jpg`, `overview_front_flipped.jpg`). Same field names in all four; in flipped-to-upright variants the row digits run 6 (top) to 1 (bottom). New boxes B18-B20 (voltage-sense candidate, hypothesis). Traces not yet traced.
