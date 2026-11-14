# Neubewertung 14.11.2026 – Der MCU startet den Fahrbetrieb nicht

Ersetzt den Hauptverdacht aus `NEUBEWERTUNG_2026-11-12.md`. Messdaten und Logs: `LAUF_2026-11-14.md`, `logs_2026-11-14/`.
Tags: [M] gemessen, [O] beobachtet, [I] gefolgert, [H] Hypothese.

## 1. Befund (reproduzierbar, 5 Fehlstarts am 14.11., alle nach Kaltstart)
Ablauf jedes Mal: START → Konsole `QSRunning`, PWM_MOTOR > 0 → Encoder 0 Hz → nach ≈ 5 s GIRT Code 08 (STS2 8×) → Konsole nimmt EM_POWENA zurück → `QSHardwareFault` → **904**.

| Prüfpunkt | Standby | Start | Bewertung |
|---|---|---|---|
| Speed-Sensor (gereinigt), Handtest | Impulse sauber, GIRT erkennt Bewegung | – | ok [M] |
| Enable P2.5 → LM2903 → OC04 | aktiv | aktiv | ok [M] (11.11.) |
| PWM-Sollwert P2.6 → OC05, LED-Seite | 7 mV | 100 → 160 mV | Konsole liefert PWM [M] |
| OC05 Transistorseite (C–E) | 4,95 V | 4,5 → 4,3 V | **Sollwert erreicht MCU** [M] |
| VCC L4981 / VDD Gate-Treiber | 13,5 V | 13,5 V | Versorgung ok [M] |
| Zwischenkreis | 316 V | 316 V | **PFC startet nicht** [M] |
| L4981 Pin 15 (P-UVLO) | 6 mV | 6 mV | PFC aktiv gesperrt [M] |
| L4981 Pin 12 (SS) | – | 0 V | passt zur Sperre [M] |
| Basis T3 (zieht Pin 15 auf Masse) | 0,7 V | 0,7 V | T3 dauerhaft angesteuert [M] |
| Basis T2 (Q2-Freigabe-Kette) | – | 0,1 mV | **Motor nie freigegeben** [M] |
| Relais F27 (Vorladung) | ? | kein Klicken | nie angesteuert? [O] |
| Temperaturfühler P600 | – | – | vom Nutzer zweimal geprüft, o. B. [M] |

Statisch in Ordnung: T2, 1P, T3 (alle NPN, Übergänge 0,67–0,70 V, keine Lecks), F27 (Spule 1,4 kΩ, Kontakt angezogen 0,03 Ω), L4981-Pins (keine Brücken/Kurzschlüsse), alle Elkos, Q2/D3, Shunts, Motor.

## 2. Theorie [I/H]
Der MCU bekommt alles, was er zum Fahren braucht (Enable, Sollwert, Versorgung), **schaltet aber keinen einzigen Ausgang ein**: keine PFC-Freigabe (T3 bleibt an), keine Q2-Freigabe (T2 bleibt aus), kein Vorladerelais. Danach meldet er „keine Drehzahl“ (08). Zwei getrennte Ausgänge bleiben gleichzeitig inaktiv → **Entscheidung der Firmware, kein einzelner defekter Pin**. Der MCU selbst arbeitet sonst normal.
→ **Eine Startbedingung des MCU ist nicht erfüllt**, typischerweise ein analoger Messwert. Dass Läufe gelegentlich gelingen (oft nach langer Pause), passt zu einem Messwert nahe einer Schwelle, der mit Temperatur/Feuchte driftet.

Verlauf der T3-Ansteuerung (aus Makros, `img/t3_ansteuerung_buendel.jpg`): Basis T3 → 2,21 kΩ („2211“) → Testpad → Bündel aus 4 Bahnen (die anderen 3 von den Widerständen am TL082) → Richtung MCU; kein weiteres Bauteil dazwischen erkennbar.

### Kandidaten (Priorität)
1. **Zwischenkreis-Messung, Kette B18** (475 kΩ + 1 MΩ + 1 MΩ, Fußpunkt ≈ 221 kΩ, `netlist/b18_spannungssense_kandidat.md`). Sehr hochohmig → empfindlich für Kriechströme, Feuchte, Korrosion (auf der Platine nachgewiesen). Zu niedriger Messwert → MCU hält die Vorladung für unvollständig, startet nicht. Zeitweise zu hoher Messwert → **err 4 (OU)**. Erklärt damit auch die früheren err-4-Fehler.
2. **Vorladung / F27:** Schließt der MCU F27 erst nach erkannter Vorladung, ist das fehlende Klicken Folge von (1) oder ein eigener Fehler in der Relaisansteuerung.
3. **Nullpunkt der Strommessung** (TL082 → MCU-ADC): verschobener Offset kann einen Selbsttest vor dem Start scheitern lassen.
4. Netzspannungsmessung (VRMS/Netzerkennung).
5. MCU-Defekt oder verstellte EEPROM-Parameter: nicht ausgeschlossen, nachrangig.

## 3. Messplan
Sicherheit: Messpunkte auf Netzpotential; Klemmen nur bei entladenem Elko (< 5 V) setzen, Bezug Elko-Minus (Rückseite) = 0VA, danach nichts berühren.

| # | Messung | Bedingung | Erwartung | Bedeutung bei Abweichung |
|---|---|---|---|---|
| 1 | **B18-P1** (rundes Pad links vom „4753“) gegen Elko-Minus, DC | Standby (Zwischenkreis 316 V) | **≈ 26 V** (316 V × 221k / 2696k) | deutlich weniger → Messkette zu hochohmig/MCU sieht zu wenig Zwischenkreis; schwankend → Kriechstrom |
| 2 | Zwischenkreis gleichzeitig ablesen (zweites Gerät oder direkt davor) | Standby | ≈ 316 V | Bezug für das Verhältnis aus 1 |
| 3 | F27 Spulen-Minus gegen Elko-Minus | Standby, dann Start | ≈ 0 V = Relais angezogen; ≈ 24 V = offen | offen in Standby und Start → MCU sieht Vorladung nicht als fertig |
| 4 | Testpad rechts neben „2211“ gegen Elko-Minus | Standby, Start | ≈ 3,3/5 V konstant | bestätigt Logikausgang als Quelle |
| 5 | Weg „2211“-Testpad → MCU-Pin (stromlos, Ohm) | stromlos | ≈ 0 Ω zu einem Pin (Position L/U/R/O, `img/mcu_qfp32_pins.jpg`) | Zuordnung des MCU-Pins |
| 6 | MCU-seitige Enden der vier Widerstände am TL082 | Standby | feste Werte nahe 0 V oder mittlere Referenz | Anschlag (≈ Versorgung) → Strommessung verdächtig |
| 7 | B18 stromlos: R1/R2/R3 einzeln und Kette gegen 0VA (wie 08.11.) | stromlos | Werte wie 08.11. (Tabelle B18-M01…M11) | Abweichung → Bauteil/Kriechstrom |
| 8 | Optional: Platinenbereich B18/B19 mit Isopropanol reinigen, trocknen, erneut 1 + Start | – | – | Start gelingt → Kriechstrom bestätigt |

Bei jedem Lauf: Skript `--start-delay 20`, Displaycode, STS2-Blinks, MIN/MAX notieren.
