# Messplan 14.11. abends – Startfreigabe des MCU (überarbeitet 20:45)

Ziel: herausfinden, welche Bedingung dem MCU für die Startfreigabe fehlt (Kandidaten: `NEUBEWERTUNG_2026-11-14.md`, Abschnitt 5).
**Priorität:** (1) Versorgung prüfen → (2) bekannte Freigabesignale bis zum Empfänger verfolgen → (3) weitere Startbedingungen untersuchen.
Erwartungswerte nur, wo begründet; sonst Werte notieren. Zurückgestellte Punkte stehen mit Begründung am Ende.

## 1 – Versorgung
| # | Zustand | Messung | Erwartung |
|---|---|---|---|
| 1.1 | Standby | +5VA, +12VA, −12VA gegen Testpunkt 0VA | ≈ 5 V, +12 V, −12 V |
| 1.2 | Start | dieselben mit MIN/MAX (ein Lauf pro Schiene) | kein Einbruch |

## 2 – Bekannte Freigabesignale bis zum Empfänger (stromlos zuordnen, dann messen)
| # | Zustand | Messung | Notieren |
|---|---|---|---|
| 2.1 | stromlos | **OC04 Transistorseite** (Enable) → sichtbaren Leiterbahnen bis zum Empfänger folgen (MCU-Pin oder Zwischenstufe) | Empfänger, Beschaltung |
| 2.2 | stromlos | **OC05 Kollektor** (PWM-Sollwert) → wie 2.1 | Empfänger, Beschaltung |
| 2.3 | stromlos | **Motorfreigabe T2**: von der Basis T2 bzw. ihrem Testpad **unabhängig** verfolgen (Beschaltung von T3 nicht voraussetzen); Pull-up/-down zu +5VA/0VA prüfen | Empfänger/Quelle, Beschaltung |
| 2.4 | stromlos | **F27-Ansteuerung**: Spulen-Minus → Treiberstufe (Transistor) → deren Basis/Gate → Quelle | Quelle, Beschaltung |
| 2.5 | Standby / Start | an den in 2.1–2.4 gefundenen Empfänger- bzw. Quellpunkten messen | Pegel, Änderung beim Start |

## 3 – Weitere Startbedingungen
| # | Zustand | Messung | Notieren / Erwartung |
|---|---|---|---|
| 3.1 | stromlos | **OC02, OC03, OC08**: P2.2, P2.3, P2.9, P2.15, P2.17, P2.18, P4-Tacho ↔ Anode (Pin 1) | kleinster Wert (≈ 1 kΩ wie OC05) = Zuordnung |
| 3.2 | Standby / Start | Anoden der in 3.1 zugeordneten Kanäle gegen P2.7 (Konsolenseite) | LED an ≈ 1,1 V, aus ≈ 0 V |
| 3.3 | stromlos | OC01/OC07 Transistorseite ↔ ADM485 Pin 2/3/4 | Zuordnung RS-485 |
| 3.4 | stromlos | B10: J1 ↔ beide Enden „01C“ am SOT-23-5; beide SOT-Testpunkte ↔ 0VA/+5VA; großer Durchsteckanschluss hinter „47R5“ → Bauteil Vorderseite; Aufdruck SOT-23-5; von J1 sichtbaren Bahnen folgen | Zuordnung, Funktion SOT-23-5 |
| 3.5 | Standby | J1 (DC, Hz) | Signalform notieren (nicht festgelegt) |
| 3.6 | – | Sichtprüfung: dunkle Stellen (Streiflicht-Foto), Faden am MCU, reinigen/trocknen | Fotos |
| 3.7 | Start | Vergleichsversuch an anderem Stromkreis ohne weitere Verbraucher | läuft / läuft nicht |

## Zurückgestellt (mit Begründung)
- **Alle 32 MCU-Pins gegen J1 durchsuchen:** erst sichtbaren Leiterbahnen folgen; Rasterwerte ohne Bezug liefern viele Zahlen ohne klare Aussage.
- **P13/P70 live messen:** Funktion unbekannt → kein Bewertungskriterium. Erst zuordnen.
- **SOT-23-5 Ein-/Ausgang live:** erst nach Funktionszuordnung; Versorgungspins allein legen Ein- und Ausgang nicht fest.
- **F27-Spulenspannung erneut:** bereits gemessen (Standby und Start 0 V); jetzt nur die Treiberansteuerung (2.4).
