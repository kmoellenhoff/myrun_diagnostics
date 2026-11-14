# Messplan 14.11. abends – Startfreigabe des MCU

Ziel: herausfinden, welche Bedingung dem MCU für die Startfreigabe fehlt (Kandidaten: `NEUBEWERTUNG_2026-11-14.md`, Abschnitt 5).
Erwartungswerte nur, wo begründet; sonst Werte notieren.

## A – Ausgebaut, stromlos (Elko < 1 V)
| # | Messung | Notieren / Erwartung |
|---|---|---|
| A1 | **J1** (unteres Bein D1, B10) ↔ beide Enden des „01C“ am SOT-23-5 | beide Werte |
| A2 | Beide Testpunkte am SOT-23-5 ↔ **0VA** und ↔ **+5VA** | ≈ 0 Ω zu einem davon = Versorgungspunkt (erklärt 10 kΩ) |
| A3 | Großer Durchsteckanschluss hinter „47R5“ → welches Bauteil auf der Vorderseite (Q1? Gate?) | Bauteil + Anschluss |
| A4 | **Aufdruck SOT-23-5**; jeder Pin ↔ 0VA, +5VA, VDD-Netz (L4981 Pin 19) | Pinrollen |
| A5 | J1 ↔ L4981 Pin 4, 6, 7; J1 ↔ MCU-Pins (alle 32, Auffälligste notieren) | Ziel von J |
| A6 | **OC02, OC03, OC08**: P2.2, P2.3, P2.9, P2.15, P2.17, P2.18 und P4-Tacho ↔ Anode (Pin 1) | kleinster Wert (≈ 1 kΩ wie bei OC05) = Zuordnung |
| A7 | OC01/OC07 Transistorseite ↔ ADM485 Pin 2 (/RE), 3 (DE), 4 (DI) | Zuordnung RS-485 |
| A8 | **Motorfreigabe T2**: Testpad Basis T2 → „01C“ → weiter bis MCU-Pin (wie bei T3), Pull-up/-down zu +5VA/0VA | MCU-Pin-Position (Kante + Nr.) |
| A9 | Testpunkt **P13** → welcher MCU-Pin | Position |
| A10 | Optional: F27 Spulen-Minus → Treibertransistor → dessen Basis → MCU-Pin | Position |
| A11 | Sichtprüfung: dunkle Stellen unter Lack (Foto mit Streiflicht), Faden an rechter unterer MCU-Ecke, Platine reinigen und trocknen lassen | Fotos |

## B – Eingebaut, Standby (klemmen bei entladenem Elko; Bezug Testpunkt 0VA bzw. Elko-Minus)
| # | Messung | Erwartung |
|---|---|---|
| B1 | +5VA, +12VA, −12VA | ≈ 5 V, +12 V, −12 V |
| B2 | P13, P70 (DC, ggf. Hz) | notieren |
| B3 | J1 (DC und Hz) | notieren (Signalform unbekannt) |
| B4 | SOT-23-5 Ein-/Ausgang (nach A4) | notieren |
| B5 | Anoden OC02/03/08 gegen **P2.7** (Konsolenseite, ungefährlich) | an ≈ 1,1 V, aus ≈ 0 V |
| B6 | MCU-Pin der Motorfreigabe (nach A8) | notieren |

## C – Start (je ein Lauf, Skript `--start-delay 20`, MIN/MAX)
Nur Punkte, deren Änderung beim Start etwas aussagt: C1 Anoden OC02/03/08 · C2 P13/P70 · C3 MCU-Pin Motorfreigabe · C4 J1/SOT-23-5 · C5 Versorgungen ±12VA/+5VA (MIN).
Zusätzlich: ein Startversuch an einem anderen Stromkreis ohne weitere Verbraucher.
