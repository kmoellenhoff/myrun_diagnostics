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
| 3.2 | erledigt | OC04/OC05: gemeinsamer Kollektor an +5VA (MCU-Eckpin = VDD); Emitterfolger, Emitter 3,3 kΩ bzw. 10 kΩ nach 0VA | OC04 Emitter → 4. Pin ab rechter Ecke; OC05 Emitter → Pin 1+2 ab Ecke bei P70 |
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

## Nächster Einbau – Live-Messung „Eingänge und Ausgänge des MCU“ (je Standby und Start, gegen 0VA)
| Messpunkt | Signal | Bekannt / Erwartung |
|---|---|---|
| OC04 Pin 3 (Emitter) | Enable von der Konsole → MCU | high, wenn Enable aktiv |
| OC05 Pin 3 (Emitter) | PWM-Sollwert → MCU | Standby ≈ 0 V; Start Mittelwert > 0, Hz |
| Via oberhalb „LD3N“-L | Netzsignal B10 → MCU-Pin X | DC + Hz, Signalform offen |
| Basis T4 (bzw. „1001“) | MCU → F27 (Vorladerelais) | ≈ 0,7 V = angesteuert; 0 V = nicht |
| Steuerleitung T3 (Testpad „2211“) | MCU → PFC-Sperre | bekannt: Standby und Start 4,9 V (gesperrt) |
| Testpad Basis T2 | MCU → Motorfreigabe | bekannt: Start 0,1 mV |
- Grafik Live-Messpunkte: `docs/img/live_messpunkte_2026-11-16.jpg`

## Oszilloskop (BSIDE OT3, akkubetrieben, 10 MHz, CAT II 400 V) – ab 16.11.

**Sicherheit:** Während Messungen auf der Netzseite **kein USB-Kabel** am Oszi (PC/Ladegerät können geerdet sein). Masseklemme nur an 0VA (Elko-Minus) bzw. auf der Konsolenseite an P2.7. Gerät während der Messung nicht anfassen; Klemmen nur bei entladenem Elko setzen. Oszi und Multimeter sind beide akkubetrieben und dürfen gleichzeitig messen, solange beide Massen am selben Bezug (0VA) liegen.

**Grundeinstellung:** Tastkopf und Gerät auf x10, Kopplung DC, Trigger Flanke steigend, Modus AUTO (für Einzelereignisse SINGLE).

| Lauf | Oszi (Kanal) | Masse | Einstellung | gleichzeitig Multimeter | Zweck |
|---|---|---|---|---|---|
| O1 | P2.6 bzw. OC05 Pin 1 (Konsolenseite) | P2.7 | 1 V/div, 1 ms/div, Trigger 0,5 V | – | Einarbeitung, PWM-Sollwert der Konsole: Frequenz/Tastgrad |
| O2 | Via oberhalb LD3N-L (Netzsignal X, MCU-Pin 28) | 0VA | 1 V/div, 5 ms/div, AUTO | OC04 Pin 3 (Enable) DC | Kommt das Netzsignal am MCU an? Standby genügt, dann Start |
| O3 | OC05 Pin 3 (PWM am MCU, Pin 17/18) | 0VA | 1 V/div, 1 ms/div, Trigger 2 V | Basis T4 DC MIN/MAX | Erreicht der Sollwert den MCU; schaltet der MCU F27 |
| O4 | Testpad Basis T2 bzw. Basis T4 | 0VA | 0,5 V/div, 100 ms/div, SINGLE, Trigger 0,3 V | Steuerleitung T3 DC MIN/MAX | Kurze Ansteuerungsversuche erfassen, die Multimeter-MAX nicht sieht |

## Ergänzung 16.11. abends – nach Durchsicht aller Unterlagen
Begründung und vollständige Liste: `NEUBEWERTUNG_2026-11-16.md`. Zusätzlich zu den Punkten oben, in dieser Reihenfolge:
1. Beim nächsten Startversuch STS1/STS2 mit Ton filmen (blinkt STS1 weiter? Zeit bis zum ersten STS2-Puls).
2. Stromlos: **J ↔ 0VA** in beiden Polaritäten (22 kΩ oder 6,4–6,9 kΩ?); Testpunkte am SOT-23-5 ↔ 0VA / +5VA.
3. Stromlos: Y (LD3N-O) ↔ B20-R1b und ↔ TL082 Pin 7 (Quelle von Y).
4. Punkt 3.6 vorziehen und um **P4 TACHO / P2.9** ergänzen: Zuordnung OC02/OC03/OC08, danach deren Emitter → MCU-Pin.
5. Punkt 3.7 vorziehen: P2.15, P2.17, P2.18 gegen P2.7 in Standby und Start (Konsolenseite).
6. Netzspannung an der Steckdose bei jedem Versuch notieren.

### Stand 16.11. 21:45
- Punkte 2 und 3 der Ergänzung erledigt (`LAUF_2026-11-14.md`, „16.11. abends“): J nur 22,1 kΩ nach 0VA; Teiler 1:2 vor X; Y = Temperatureingang über P600.
- Für die Live-Messung: **X** (Oszi, Lauf O2) rechnerisch ≈ 3,7 V Spitze; **Y** (LD3N-O gegen 0VA, Multimeter DC) rechnerisch ≈ 0,7–0,8 V bei Raumtemperatur, 0 V = Fühlerkreis offen. Beides Rechenmodelle, keine Sollwerte.
- Noch stromlos offen: P600 Kontakt 2 ↔ +5VA (0 Ω erwartet); Zuordnung OC02/OC03/OC08 (Punkt 4).
