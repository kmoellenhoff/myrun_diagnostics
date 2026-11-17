# Prüfung Netzsignalweg B10 → X → MCU 28 (17.11.2026, nachmittags)

Anlass: X im Standby nur 0,103 V DC / 0,044 V AC (T17-36, `LAUF_2026-11-17.md`), Rechenmodell ≈ 2,4 V DC / 1,1 V AC / 100 Hz. Abgleich aller Fotos, Messwerte und des Schaltplans (`gesamtschaltplan_110926/`, Stand 436b49f). Keine neuen Messungen. M gemessen, F Foto, I abgeleitet, H Hypothese.

## Plausibilität des Rechenmodells
950 kΩ / 22,1 kΩ und Teiler 1:2 ergeben bei 230 V ≈ 3,7 V Spitze an X, bei 264 V (+15 %) ≈ 4,2 V – eine typische Auslegung für einen MCU-Eingang mit 5 V Referenz [I]. Erwarteter Mittelwert (Vollweg) ≈ 2,3–2,4 V DC. 0,1 V passt nicht dazu.

## Abschnitte und Belegstand
| # | Abschnitt | Beleg | Wert / Bemerkung |
|---|---|---|---|
| 1 | AC-Pads L/N → B10 T1/T2 | M | 0 Ω (B10-M12/M13). Lage des Abgriffs relativ zu Sicherung/Filter nicht dokumentiert; Netz an den Fastons 237,8 V / 50,02 Hz (T17-01, abgezogen). Zwischenkreis 316 V im Standby → Netz liegt am Board an. |
| 2 | je 2 × 475 kΩ (R1–R4 B10) | M, eingebaut | 472,5 / 473,2 kΩ; Paare 0,92 / 0,923 MΩ |
| 3 | D1/D2 | M, Diodentest eingebaut | 0,497 / 0,499 V, Gegenrichtung OL |
| 4 | J → 22,1 kΩ → 0VA | M | 22,14 / 22,02 kΩ (16.11.) |
| 5 | J → 1,0 kΩ → TL082 Pin 3; Pin 1 = Pin 2; Pin 8 = +12VA, Pin 4 = −12VA | M (stromlos, 0 Ω) | Versorgung im Betrieb **nie gemessen** |
| 6 | TL082 Pin 1 → R1 (4,75 kΩ) → N; R2 (4,75 kΩ) N → 0VA | M (R1b = R2b, R2a = 0VA); Pin 1 → R1a nur Nutzerbeschreibung/Foto | R1 eingebaut 4,6 kΩ (09.11.) |
| 7 | N → 100 Ω „1000“ → X | I | Wert aus 6,53 − 6,43 kΩ abgeleitet; Pad-Identität N ↔ „1000“ nicht direkt gemessen |
| 8 | X = „1000“-Pad = Kondensatorpad = Via oberhalb LD3N-L → MCU 28 | M (Via ↔ Kondensatorpad 0 Ω, 16.11. 01:24) | Kondensator: ein Pad 0VA; Wert unbekannt; Pads eingebaut 2,65 / 3,34 kΩ |
| 9 | **Zweite Klemmdiode „LD3N“ mit Einzelpin (O) am Knoten X** | **F** (`photos/2026-11-15/netzsignal_pfad_ohne_markierung.jpg`, Diode unten Mitte unterhalb des Kondensatorpaars; vom Nutzer am 15.11. 22:19 als „zweite LD3N“ beschrieben) | **Nie gemessen, nicht im Schaltplan.** Die gemessene LD3N (L = 0VA, R = +5VA, O = Y/MCU 26) ist eine andere. |

## Widersprüche / Korrekturbedarf im Schaltplan
1. Klemmdiode an X (Zeile 9) fehlt im Schaltplan; Eintrag erst nach Messung (O ↔ X 0 Ω, Diodentest).
2. AKT-009 (TL082.1 ↔ OUT4751.1), AKT-010 (OUT4751.2 ↔ X.1000in) und AKT-025 (100 Ω) stehen als M, stützen sich aber auf Nutzerbeschreibung bzw. Ableitung → als F/I führen.
3. J ↔ 0VA 6,4–6,8 kΩ und J ↔ +5VA 9–10 kΩ (08.11.) sind mit 22,1 kΩ (16.11.) nicht vereinbar; Ursache offen (Messpunkt am Diodenbein, Zustand vor Reinigung).
4. Vierter B20-Widerstand (R4, „475…“, 4,77 kΩ) ist im Schaltplan unverbunden.
5. `netlist/b10_netlist.csv` führt R2/R4 noch als Hypothese, obwohl Messwerte vorliegen.

## Kandidaten für X ≈ 0,1 V [H], in Prüfreihenfolge
1. **Messkontakt am Via** (teilweise lackiert) – zuerst am Kondensatorpad bzw. am „1000“-Pad wiederholen.
2. **Versorgung des TL082 (+12VA/−12VA)** – im Betrieb nie gemessen. Fehlt +12VA, kann der Spannungsfolger nicht positiv aussteuern → X ≈ 0.
3. **Last am Knoten X:** ungemessene Klemmdiode (Zeile 9), Kondensator oder MCU-Eingang 28. Statisch X ↔ 0VA 2,65 / 3,34 kΩ spricht gegen einen harten Kurzschluss, nicht gegen einen spannungsabhängigen Leckstrom.
4. B10-Eingang (statisch unauffällig) – nur wenn bereits J fehlt.

## Messfolge im Standby (Multimeter V DC und V~ gegen Elko-Minus)
| Punkt | Rechenmodell DC / AC | Wenn deutlich zu niedrig |
|---|---|---|
| X am Kondensatorpad bzw. Einzelpin der zweiten LD3N | ≈ 2,4 V / 1,1 V | weiter stromaufwärts |
| N = obere Kappe R1 (⑤ in `img/messpunkte_2026-11-16_abend.jpg`) | ≈ 2,4 V / 1,1 V | N ok, X niedrig → Last an X |
| TL082 Pin 1 | ≈ 4,7 V / 2,3 V | Pin 1 ok, N niedrig → R1 oder starke Last an X |
| TL082 Pin 8 und Pin 4 | ≈ +12 V / −12 V | Versorgung fehlt → Quelle der ±12VA |
| TL082 Pin 3 bzw. J (①) | ≈ 4,7 V / 2,3 V | J niedrig → B10 |
Rechenwerte ohne Toleranz (keine Sollwerte); ein Faktor 2 ist noch kein Befund, ein Faktor 20 schon.
Stromlos danach je nach Ergebnis: Diodentest der zweiten LD3N (alle Pinpaare, Vergleich mit der gemessenen), O ↔ X (0 Ω erwartet).
