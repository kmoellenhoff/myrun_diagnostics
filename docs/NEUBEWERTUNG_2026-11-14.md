# Neubewertung 14.11.2026 – PFC und Motor bleiben gesperrt (T3-Sperre)

Ersetzt den Hauptverdacht aus `NEUBEWERTUNG_2026-11-12.md`. Messdaten und Logs: `LAUF_2026-11-14.md`, `logs_2026-11-14/`.
Tags: [M] gemessen, [O] beobachtet, [I] gefolgert, [H] Hypothese.

## 1. Befund (reproduzierbar, 5 Fehlstarts am 14.11., alle nach Kaltstart)
Ablauf jedes Mal: START → Konsole `QSRunning`, PWM_MOTOR > 0 → Encoder 0 Hz → nach ≈ 5 s GIRT Code 08 (STS2 8×) → Konsole nimmt EM_POWENA zurück → `QSHardwareFault` → **904**.

| Prüfpunkt | Standby | Start | Bewertung |
|---|---|---|---|
| Speed-Sensor (gereinigt), Handtest | Impulse sauber, GIRT erkennt Bewegung | – | ok [M] |
| Enable P2.5 → LM2903 → OC04 | aktiv | aktiv | ok [M] (11.11.) |
| PWM-Sollwert P2.6 → OC05, LED-Seite | 7 mV | 100 → 160 mV | Konsole liefert PWM [M] |
| OC05 Transistorseite (C–E) | 4,95 V | 4,5 → 4,3 V | **PWM-Änderung am Ausgang von OC05** [M]; Weg zum MCU und Pulsform nicht gemessen |
| VCC L4981 / VDD Gate-Treiber | 13,5 V | 13,5 V | Versorgung ok [M] |
| Zwischenkreis | 316 V | 316 V | **PFC startet nicht** [M] |
| L4981 Pin 15 (P-UVLO) | 6 mV | 6 mV | PFC aktiv gesperrt [M] |
| L4981 Pin 12 (SS) | – | 0 V | passt zur Sperre [M] |
| Basis T3 (zieht Pin 15 auf Masse) | 0,7 V | 0,7 V | T3 dauerhaft angesteuert [M] |
| Basis T2 (Q2-Freigabe-Kette) | – | 0,1 mV | **Motor nie freigegeben** [M] |
| Relais F27 (Vorladung) | ? | kein Klicken | nie angesteuert? [O] |
| Temperaturfühler P600 | – | – | vom Nutzer zweimal geprüft, o. B. [M] |

Statisch in Ordnung: T2, 1P, T3 (alle NPN, Übergänge 0,67–0,70 V; C–E-Ohmwerte passen zum jeweiligen Parallelnetz, kein niederohmiger C–E-Pfad bei Ohmmessung – Verhalten unter Betriebsspannung damit nicht geprüft), F27 (Spule 1,4 kΩ, Kontakt angezogen 0,03 Ω), L4981-Pins (keine Brücken/Kurzschlüsse), alle Elkos, Q2/D3, Shunts, Motor.

## 2. Theorie [I/H]
Gemessen ist: Enable-Kanal aktiv, PWM-Änderung am OC05-Ausgang, Versorgung 13,5 V – trotzdem bleiben die PFC-Sperre (T3 an, Pin 15 ≈ 6 mV) und die fehlende Q2-Freigabe (Basis T2 ≈ 0 V) bestehen; beim START ist kein Relaisklicken hörbar. Danach meldet die GIRT 08.
**Hypothese [H]:** Beide Freigaben werden von derselben Stelle (vermutlich MCU) zurückgehalten, weil eine Startbedingung nicht erfüllt ist; ein einzelner defekter Pin würde nicht beide Pfade betreffen. **Nicht bewiesen:** Quelle der T3- und T2-Ansteuerung, bewusste Firmwareentscheidung (auch eine nachgewiesene MCU-Verbindung würde das allein nicht belegen), Zusammenhang beider Sperren.
→ Falls die Hypothese stimmt, ist eine Startbedingung nicht erfüllt, z. B. ein analoger Messwert. Dass Läufe gelegentlich gelingen (oft nach langer Pause), passt zu einem Messwert nahe einer Schwelle, der mit Temperatur/Feuchte driftet.

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
| 1 | **Quelle der T3-Ansteuerung stromlos** (14.11. 17:20: Testpad → „01C“ 10 kΩ; Knoten mit Via A, Gegenende Via B – vermutlich Pull-up +5VA, siehe LAUF_2026-11-14.md): vom quellenseitigen Ende von „2211“ (Testpad) bis zum nächsten Bauteilanschluss (MCU-Pin, IC-Pin, Transistor) | stromlos | ≈ 0 Ω zu einem Anschluss; Abzweigungen prüfen. Vorab: Testpad ↔ Basis T3 ≈ 2,2 kΩ (nicht 0 Ω) | MCU-Pin → Ansteuerung kommt vom MCU (Grund noch offen); anderes Bauteil → vorgeschaltete Logik/Schutzstufe, dort weiter |
| 2 | Testpad an „2211“ (quellenseitig) gegen Elko-Minus | Standby, Start | Rechnung bei Pull-up 10 kΩ → +5VA: **≈ 1,5 V** = niemand treibt; **≈ 5 V** = aktiv high; ≈ 0 V = aktiv low | Unterscheidet „Freigabe wird nie gegeben“ von „Sperre wird aktiv gehalten“ |
| 3 | F27: (a) Spulen-Plus gegen Elko-Minus, (b) **Spannung über der Spule** (Plus gegen Minus) | Standby, dann Start | (a) ≈ 24 V; (b) ≈ 24 V = angezogen, ≈ 0 V = nicht angesteuert | nur (b) zusammen mit (a) ist aussagekräftig; Spulen-Minus allein reicht nicht |
| 4 | Optional, nachrangig: obere Enden B20-R1b…R4b gegen Elko-Minus | Standby, Start | **keine begründete Erwartung** (Funktion unbekannt) | nur dokumentieren, keine Bewertung ohne Schaltungsfunktion |
| 5 | Optional, erst wenn die PFC freigegeben wird: L4981 Pin 14 (VFEED) und B18-P1 im Betrieb | Start | Modell: Pad B ≈ 4,6 V, P1 ≈ 27,9 V bei 316 V (unbelastet, kein Sollwert) | nur für PFC-Regelung relevant |

Bei jedem Lauf: Skript `--start-delay 20`, Displaycode, STS2-Blinks, MIN/MAX notieren.

## 4. Stand 17:45 – Sperre kommt aktiv vom MCU [M]
Kette vollständig gemessen: **MCU-Pin (untere linke Kante Nr. 3, vermutl. Pin 11)** → Knoten → 2,21 kΩ → Basis T3 → T3 zieht L4981 Pin 15 auf 0VA; Pull-up 10 kΩ („01C“) nach +5VA. Pegel am Knoten: **Standby 4,9 V, Start 4,9 V** (bei reinem Pull-up wären ≈ 1,5 V zu erwarten) → der MCU **treibt aktiv high** und gibt die PFC beim Start nicht frei. Die Sperransteuerung selbst ist damit in Ordnung; offen ist, **warum der MCU nicht freigibt**.

### Nächste Schritte
1. **F27-Spule** (Plus gegen Elko-Minus und Spannung über der Spule), Standby und Start: Schließt der MCU die Vorladung überhaupt ab?
2. **Testpunkte P70 (MCU-Pin 5 der unteren linken Kante) und P13** gegen Testpunkt 0VA (Vorderseite), Standby und Start: Herstellertestpunkte liegen meist an wichtigen Signalen; jede Änderung beim Start ist ein Hinweis.
3. **Basis T2 bzw. Motorfreigabe-Pin** am MCU zuordnen (gleiches Vorgehen wie bei T3), um zu sehen, ob beide Freigaben am MCU enden.
4. Eingänge des MCU identifizieren, die vor dem Start ausgewertet werden könnten: Netz-/Zwischenkreismessung (Ketten in B10), Strommessung (TL082 → B20-R1…R4), Netzerkennung (LINE), Konsolen-Signale (OC04 Enable, OC05 PWM, OC06 RS-485). Jeweils: Weg zum MCU-Pin, Pegel Standby/Start.
5. Erst danach: EEPROM 24C32 (Parameter) und MCU-Tausch/Tausch-GIRT als Option.

## 5. Kandidaten: Warum erteilt der MCU die Startfreigabe nicht? (Stand 19:10, alle [H])
Belegt ist nur: Enable-Kanal aktiv, PWM-Änderung am OC05-Ausgang, VDD 13,5 V, Steuerleitung T3 bleibt 4,9 V, F27 ohne Spulenspannung, Basis T2 ≈ 0 V.

| # | Kandidat | Warum plausibel | Prüfung (Aufwand) |
|---|---|---|---|
| 1 | **Weitere Konsolen-Signale über OC02/OC03/OC08** (z. B. Wake-up P2.15, Sleep P2.17, weitere Freigabe) | drei Konsole→MCU-Kanäle sind nicht zugeordnet; ein fehlendes „Wake“/aktives „Sleep“ würde den MCU im Standby halten, obwohl PWM ankommt | P2-Pins → Anoden OC02/03/08 stromlos zuordnen; im Betrieb Anodenspannung gegen P2.7 (Konsolenseite, ungefährlich) Standby/Start (gering) |
| 2 | **Hilfsversorgungen ±12VA, +5VA** | TL082 (Strommessung) braucht vermutlich ±12VA; fehlt eine Schiene, liegt die Strommessung am Anschlag → Selbsttest vor dem Start scheitert | Testpunkte −12VA, +12VA, +5VA gegen 0VA (Vorderseite neben D3) im Standby (sehr gering) |
| 3 | **Netz-/Zwischenkreiserkennung** (B10 oder anderer Teiler) | Vorladerelais wird typisch erst nach erkannter Netz-/Zwischenkreisspannung geschlossen | Weg von J1 eindeutig zuordnen; Vergleich an anderem Stromkreis (mittel) |
| 4 | **Motorkreis-Prüfung vor dem Start** (Bürstenkontakt) | Handbuch nennt bei HF900 abgenutzte Bürsten; offene Lamellen/Bürsten nur bei bestimmter Rotorstellung → sporadisch | Motorwiderstand L+/L− bei mehreren Rotorstellungen (Band schrittweise von Hand verschieben, Stecker ab) (gering) |
| 5 | **Strommessung (TL082) Offset** | Nullpunktprüfung vor Start üblich | erst nach 2; Ausgänge TL082 im Standby (mittel) |
| 6 | **RS-485 (ADM485, OC06/OC01/OC07)** | Statusflags kommen an, aber ein Startbefehl/Parameter könnte über den Bus laufen | Zuordnung OC01/OC07, Signal mit Hz-Messung (mittel) |
| 7 | **Gespeicherte Sperre / Parameter im EEPROM 24C32** | manche Antriebe verriegeln nach wiederholten Fehlern dauerhaft | nur durch Tausch/Auslesen klärbar (hoch) |
| 8 | **MCU/Firmware-Defekt** | nachrangig, MCU arbeitet sonst normal | Tausch-GIRT (hoch) |
