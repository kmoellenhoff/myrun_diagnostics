# Messplan – Startfreigabe des MCU (Stand 16.11. 01:30)

Ziel: herausfinden, welche Bedingung dem MCU für die Startfreigabe fehlt (Kandidaten: `NEUBEWERTUNG_2026-11-14.md`, Abschnitt 5; Messprotokoll: `LAUF_2026-11-14.md`).
**Priorität:** (1) Versorgung → (2) bekannte Freigabe- und Messsignale am MCU → (3) weitere Startbedingungen.
Erwartungswerte nur, wo begründet; sonst Werte notieren. Netzseite: klemmen nur bei entladenem Elko (< 5 V), Bezug Elko-Minus = 0VA, danach nichts berühren.

## Erledigt (stromlos, 14.–16.11.)
- **Netzsignal B10 vollständig verfolgt, statisch ohne Befund:** Netz → 2 × 475 kΩ → D1/D2 → J (22,1 kΩ → 0VA) → 1,0 kΩ → TL082 (neben T3) Pin 3, als Puffer (Pin 1 = Pin 2) → 4,75 kΩ → Via → 100 Ω („1000“) → Knoten X (Kondensator nach 0VA; Via oberhalb „LD3N“-L) → **MCU-Pin X = 4. Pin ab der Ecke bei P13** (`img/mcu_pin_netzsignal.jpg`). TL082 versorgt mit +12VA (Pin 8) / −12VA (Pin 4).
- Nachbareingang **Y = 2. Pin ab der Ecke**: Schottky-Klemmdiode „LD3N“ (L = 0VA, R = +5VA, O = Y), Diodentest unauffällig. X ↔ Y 6,5 kΩ (Parallelpfad, kein Fehler).
- SOT-23-5 / „01C“ / „47R5“: nicht im B10-Weg (10 kΩ waren nicht der direkte Pfad); Funktion offen, vermutlich Treiberstufe.
- PFC-Sperre: MCU-Pin (untere linke Kante Nr. 3, `img/mcu_pin_kandidaten_t3.jpg`) → 2,21 kΩ → T3 → L4981 Pin 15; Pull-up 10 kΩ nach +5VA; MCU treibt Standby **und** Start aktiv 4,9 V.
- F27: Standby und Start 0 V über der Spule, Spulen-Plus 24 V.

## 1 – Versorgung (eingebaut)
| # | Zustand | Messung | Erwartung |
|---|---|---|---|
| 1.1 | Standby | +5VA, +12VA, −12VA gegen Testpunkt 0VA (Vorderseite neben D3) | ≈ 5 V, +12 V, −12 V |
| 1.2 | Start | dieselben mit MIN/MAX | kein Einbruch |

## 2 – Signale am MCU (eingebaut)
| # | Zustand | Messung | Notieren / Bewertung |
|---|---|---|---|
| **2.1** | **Standby** | **Netzsignal X: Via oberhalb „LD3N“-L** (= Kondensatorpad Signalseite) gegen Elko-Minus, **DC und Hz** | Signalform offen; Hz-Anzeige (50/100 Hz) = Netz kommt am MCU an; konstant/0 V = Spur |
| 2.2 | Standby | zum Vergleich TL082 Pin 1 und J (B10) gegen Elko-Minus, DC und Hz | Signal entlang des Weges vergleichen |
| 2.3 | Start | 2.1 mit MIN/MAX bzw. Hz während eines Startversuchs | Änderung? |
| 2.4 | Standby | Y (Diode O) gegen L, DC und Hz | Pegel notieren (Quelle von Y noch offen) |

## 3 – Weitere Freigabe- und Startsignale (erst stromlos zuordnen)
| # | Zustand | Messung | Notieren / Erwartung |
|---|---|---|---|
| 3.1 | stromlos | **Quelle von Y**: vom Via/Leiterbahn an Diode O rückwärts verfolgen | Signal, Beschaltung |
| 3.2 | erledigt | OC04 Kollektor → MCU-Eckpin (Reihe ab Gehäusepunkt, Seite P602); OC05 Kollektor → derselbe Eckpin (Korrektur 01:46); Emitter nicht an 0VA/+5VA | Pull-ups/Emitter noch prüfen |
| 3.3 | stromlos | **Motorfreigabe T2** unabhängig von T3 verfolgen (Basis → Quelle; Pull-up/-down) | Quelle |
| 3.4 | stromlos | **F27-Ansteuerung**: Spulen-Minus → Treibertransistor → Basis → Quelle | Quelle |
| 3.5 | Standby / Start | an den in 3.1–3.4 gefundenen Punkten messen | Pegel, Änderung beim Start |
| 3.6 | stromlos | **OC02, OC03, OC08**: P2.2, P2.3, P2.9, P2.15, P2.17, P2.18, P4-Tacho ↔ Anode (Pin 1) | kleinster Wert (≈ 1 kΩ wie OC05) = Zuordnung |
| 3.7 | Standby / Start | Anoden der zugeordneten Kanäle gegen P2.7 (Konsolenseite) | LED an ≈ 1,1 V, aus ≈ 0 V |
| 3.8 | stromlos | OC01/OC07 Transistorseite ↔ ADM485 Pin 2/3/4 | Zuordnung RS-485 |
| 3.9 | stromlos | übrige „LD3N“ (andere MCU-Eingänge): Diodentest | ≈ 0 V in beiden Richtungen = durchlegiert |
| 3.10 | – | Sichtprüfung: dunkle Stellen am Knoten J / weißlicher Belag nachreinigen, trocknen | Fotos |
| 3.11 | Start | Vergleichsversuch an anderem Stromkreis ohne weitere Verbraucher | läuft / läuft nicht |

## Zurückgestellt / verworfen
- **Brücke Kondensatorpad ↔ Diode O: nicht löten** – X und Y sind getrennte MCU-Eingänge.
- Alle 32 MCU-Pins rasterartig durchsuchen: nur gezielt entlang sichtbarer Bahnen.
- P13/P70 live: P13 nicht mit X verbunden, Funktion unbekannt.
- SOT-23-5 live: erst nach Funktionszuordnung.
- F27-Spulenspannung erneut: bereits gemessen; nur Treiberansteuerung (3.4).
