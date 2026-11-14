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

### Kandidaten (Priorität) – korrigiert 16:45
**Korrektur:** Die erste Fassung (21c7f28) stützte Kandidat „B18“ auf den veralteten Stand vom 08.11. (≈ 221 kΩ Fußpunkt, Ziel MCU). Seit 09.11. gemessen (ursprünglich Branch `110926`, am 14.11. in `main` gemergt): B18 → P1 → 100 kΩ → 100 kΩ → B19-Pad B → 39,2 kΩ → 0VA, **Pad B = L4981 Pin 14 (VFEED)**, also die **Spannungsrückführung des PFC-Reglers**, kein belegter MCU-Eingang (`netlist/b18_spannungssense_kandidat.md`, `messplan_stromlos_2026-11-08/B19_ERGEBNISSE_2026-11-09.md`). Solange T3 die PFC sperrt, spielt VFEED keine Rolle → B18 ist **kein** Kandidat für die Startverweigerung; die Verknüpfung mit err 4 ist unbelegt. Modellwerte bei 316 V (unbelastet): P1 ≈ 27,9 V, Pad B ≈ 4,6 V.

**B20 = T3:** Die am 09.11. vermessene Gruppe B20 (`messplan_stromlos_2026-11-08/B20_ERGEBNISSE_2026-11-09.md`) (Reihe aus 4 Widerständen + SOT-23, E6) ist genau T3 mit den Widerständen neben dem TL082: Ta (Einzelpin) 20,5 kΩ → 0VA = Kollektor an Pin 15 (heute gemessen 20,5 kΩ), Tb = 0VA = Emitter, Tc = Basis mit **14,8 kΩ → 0VA und 12,2 kΩ → +5VA** [M, 09.11.]. Die Basis hat also einen Pfad zu +5VA; denkbar ist ein **Pull-up, der T3 standardmäßig einschaltet** (PFC aus = sicherer Grundzustand), und die Quelle muss die Basis zum Freigeben aktiv auf low ziehen [H]. 0,7 V an der Basis unterscheidet nicht zwischen „Quelle treibt high“ und „niemand zieht low“.

Offene Kernfrage: **Warum bleibt die Sperransteuerung an T3 aktiv?** Nicht bewiesen sind: Quelle = MCU-Pin, bewusste Firmwareentscheidung, Zusammenhang mit der Motorfreigabe (T2). Kandidaten:
1. **Quelle der T3-Ansteuerung**: MCU-Pin (Firmware sperrt) oder vorgeschaltete Logik/Schutzschaltung (z. B. TL082-Komparator, Pull-up ohne aktives Low). Erst stromlos eindeutig zuordnen.
2. **Vorladung / F27**: Klickt F27 schon beim Netz-Ein? Fehlendes Klicken beim START beweist keine fehlende Ansteuerung.
3. Strommessung (TL082 → MCU), Netzspannungsmessung, sonstige Startbedingungen des MCU.
4. MCU-Defekt oder EEPROM-Parameter.

## 3. Messplan
Messpunkte: `img/messpunkte_2026-11-14_t3_quelle.jpg` (Schritte 1, 2, 4), `img/mcu_qfp32_pins.jpg` (Ziel von Schritt 1); F27-Spule: Foto der Rückseite unter F27 noch nötig.
Sicherheit: Messpunkte auf Netzpotential; Klemmen nur bei entladenem Elko (< 5 V) setzen, Bezug Elko-Minus (Rückseite) = 0VA, danach nichts berühren.

| # | Messung | Bedingung | Erwartung | Bedeutung bei Abweichung |
|---|---|---|---|---|
| 1 | **Quelle der T3-Ansteuerung stromlos**: vom quellenseitigen Ende von „2211“ (Testpad) bis zum nächsten Bauteilanschluss (MCU-Pin, IC-Pin, Transistor) | stromlos | ≈ 0 Ω zu genau einem Anschluss | MCU-Pin → Firmware; anderes Bauteil → Schutz-/Logikstufe |
| 2 | Testpad an „2211“ (quellenseitig) gegen Elko-Minus | Standby, Start | Pegel notieren (≈ 5 V = high bzw. Pull-up) | ändert sich beim Start nicht → Quelle gibt nie frei |
| 3 | F27 Spulen-Minus gegen Elko-Minus | Standby, dann Start | ≈ 0 V = Relais angezogen; ≈ 24 V = offen | offen in Standby und Start → MCU sieht Vorladung nicht als fertig |
| 4 | MCU-seitige Enden der vier Widerstände am TL082 (= B20-R1…R4) | Standby | feste Werte nahe 0 V oder mittlere Referenz | Anschlag (≈ Versorgung) → Strommessung verdächtig |
| 5 | Optional, erst wenn die PFC freigegeben wird: L4981 Pin 14 (VFEED) und B18-P1 im Betrieb | Start | Modell: Pad B ≈ 4,6 V, P1 ≈ 27,9 V bei 316 V (unbelastet, kein Sollwert) | nur für PFC-Regelung relevant |

Bei jedem Lauf: Skript `--start-delay 20`, Displaycode, STS2-Blinks, MIN/MAX notieren.
