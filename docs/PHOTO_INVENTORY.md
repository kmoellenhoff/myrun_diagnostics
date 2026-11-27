# GIRT S6T30 – Bauteilinventar aus den Makrofotos (08.11.2026)

Quelle: 41 Vorderseiten- und 57 Rückseitenmakros sowie eine Durchlichtübersicht. Gewissheit: **P** = Aufdruck im Foto gelesen, **I** = abgeleitet. Alles stammt aus eigener Beobachtung an einer rechtmäßig erworbenen Platine (Haftungshinweis siehe [HARDWARE.md](HARDWARE.md)).

## Logikleiste neben den Optokopplern (netzseitige Logik, Vorderseite)

| Teil | Gelesener Aufdruck (P) | Anzahl / Hinweis |
|---|---|---|
| Optokoppler | `VO617A-8` (Vishay, SMD-4) | 8 in einer Reihe neben P602 |
| Hex-Schmitt-Inverter | `74ACT14G` (SO-14) | 2 |
| Komparator | `2903` (LM2903, SO-8) | 1 |
| RS-485-Transceiver | `ADM485` (SO-8) | 1, Zweck [I]: Tachosignal von P4 |
| Spannungsregler | `78L05A` (SO-8) | 2, je einer an den Enden der Leiste |
| Halbleiterrelais | `CPC1017N` (SOP-4) | 1, neben zwei SOT-223-Reglern |
| MCU | QFP-32 nahe P13/P70, Aufdruck unleserlich | 1 |
| EEPROM | SO-8 neben der MCU | 1 |

## Steckverbinder und Testpunkte

P2 (2×9, Konsole), P3 (3-polig, Poti/+5 V, netzseitig), P4 (4-polig, TACHO/+12V/0V), **P602 (2×7, blau, Debug/Programmierung, netzseitig – nicht anschließen)**, P601 (RST/0VA), P600 (2-polig, NTC neben Q2), P70 (6-polig, Lochreihe), P13 (Testpad), P400 (0V24/+24V, Relaisspulenversorgung), DC MOTOR (L+ orange / L− grau), UP/DOWN (3-polig), AC LINE (braun L, hellblau N), FUSE MOT, Testpunkte 0VA/+5VA, +12VISO/0VISO, ±12VA.

Weitere Teile: 5 mechanische Relais (Schrack PE014012 = F24, zwei Panasonic ALQ3F12 = F25, ein Panasonic ALQ3F12 = F26, Schrack RT334024 = F27), 3 Netzfilterdrosseln, Ringkern RT700, Zwischenkreis-Elko (Aufdruck `S890A16E U12 GIRT 140421 V.10.05`), Transformator ETI349X4, Kühlkörper mit Q1/Q2/D3.

## Rückseite (Lötseite)

- Große Kupferflächen auf der Netzseite, Schlitze zwischen Netz- und Logikbereich; im Signalbereich dichte Leiterbahnen.
- LEDs LINE / +5V / STS1 / STS2, SO-20-IC (Aufdruck unleserlich) unten mittig, 4× `R020`-Shunt (0,02 Ω) am Kühlkörper, zwei `471`-Leistungswiderstände, 4753-Ketten (475 kΩ) mit Dioden am linken unteren Rand.
- P2-Lötpads oben mittig.

## Übersichten

[GIRT_Platinen_Uebersicht.pdf](GIRT_Platinen_Uebersicht.pdf) (Stand 08.11., Raster A–L × 1–6): Variante A = Vorderseite wie fotografiert und Rückseite vertikal gespiegelt ([overview_front.jpg](img/overview_front.jpg), [overview_back_flipped.jpg](img/overview_back_flipped.jpg)); Variante B = Rückseite wie fotografiert und Vorderseite gespiegelt ([overview_back_upright.jpg](img/overview_back_upright.jpg), [overview_front_flipped.jpg](img/overview_front_flipped.jpg)). Die Feldnamen sind in allen vier Bildern gleich; bei der aufrechten Rückseite laufen die Zeilen von 6 (oben) bis 1 (unten). Funktionszuordnungen in der PDF sind teilweise überholt, maßgeblich sind [HARDWARE.md](HARDWARE.md) und der [Schaltplan](schaltplan/README.md).

Q2 (MOSFET, Feld B5, vorn/hinten): Pinbelegung G/D/S auf den Fotos [q2_vorderseite_GDS.jpg](img/q2_vorderseite_GDS.jpg) und [q2_rueckseite_GDS.jpg](img/q2_rueckseite_GDS.jpg); Übersicht-IDs F33/B21.
