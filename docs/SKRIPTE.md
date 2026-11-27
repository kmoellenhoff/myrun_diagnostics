# Diagnoseprogramme – Bedienung

Stand: Code gelesen und geprüft am 27.11.2026 (alle sechs Skripte mit `python3 -m py_compile` ohne Fehler übersetzt). Es wurde für diese Dokumentation keine Verbindung zu einem Laufband aufgebaut und kein Motorbefehl gesendet. Alle Aussagen zum Verhalten sind Code-Lesarten, keine Messungen.

Die Programme sind Hilfsmittel für ein motorisiertes Laufband. **Aktive Programme dürfen nur an einem vollständig montierten, mechanisch sicheren Gerät laufen: niemand auf dem Band, Not-Stopp-Schlüssel in Reichweite.** Ein Software-STOP kann vom Gerät abgelehnt werden (z. B. `80 08 04`, `OPERATION_FAILED`) und ersetzt nie den physischen Stopp. Das BLE-Protokoll steht in [BLE_PROTOKOLL.md](BLE_PROTOKOLL.md); Beispiel-Logs liegen unter `docs/beispiel_logs/`.

## 1. Auswahl nach Verhalten (Sicherheitsstufen)

| Stufe | Bedeutung |
|---|---|
| 0 – passiv | Kein FTMS-Init, kein Setup. Nur Notifications und/oder reine Lesebefehle auf dem Textkanal. |
| 1 – Lesen mit Init | FTMS-Init und Setup-Befehle werden gesendet (`@DISABLE_PACE#`, `@SSIUNITS#`, `@RJSK_EN 1#`, `@LJSK_EN 1#`), aber kein START/STOP und kein Neigungsbefehl. |
| 2 – bewegt | Sendet FTMS START (Band läuft an, ca. 1,2 km/h ohne Geschwindigkeitsbefehl) und ggf. Geschwindigkeit/Neigung; am Ende STOP-Versuch. |

| Programm / Modus | Stufe | Motor-/Steigungsbefehle | Zweck |
|---|---|---|---|
| `myrun_fast_monitor.py --listen-only` | 0 | keine | Nur Notifications sammeln, keinerlei Befehle |
| `myrun_fast_monitor.py --listen-poll SEC` | 0 | keine | Lesebefehle (`@RENC#`, `@STATUS#`, `@DUMPIO#`, `@RPWM#`, `@RERRORLOG#`) bei Konsolenstart |
| `myrun_renc_watch.py` | 0 | keine | Nur Encoder (`@RENC#`) mitschreiben |
| `myrun_dump.py` | 1 | keine | Einmaliger Diagnosebericht |
| `myrun_probe.py` | 1 | keine | Dokumentierte (und optional vermutete) Lesebefehle durchprobieren |
| `myrun_fast_monitor.py --no-start` | 1 | keine | Polling mit Init/Setup, ohne START |
| `myrun_fast_monitor.py` (Standard) | 2 | START nach Enter, optional Profil, STOP-Versuch | Lauf mit Aufzeichnung |
| `myrun_fast_monitor.py --auto-start` | 2 | START **ohne Enter** nach Countdown | Nur für bewusst vorbereitete Versuche |
| `myrun_incline_test.py` | 2 | START nach 3-s-Countdown, Zielneigung, 0 %, STOP | Kurzer Höhenverstellungstest |
| `myrun_fault_monitor.py` | 2 | START nach Texteingabe, optional eine Neigung, STOP-Versuch | Älterer Fehlerübergangsmonitor (Vorgänger) |

„Lesend“ beschreibt die abgefragte Gerätefunktion, nicht das Ausbleiben aller BLE-Schreiboperationen: jeder Textbefehl wird per BLE-Write gesendet, und das Setup der Stufe 1 ist keine reine Abfrage. Unbekannte Befehle gelten nicht als garantiert wirkungslos.

### Voraussetzungen

Python 3, Linux mit BlueZ und das Paket `bleak` (`python3 -m pip install bleak`). Andere BLE-Verbindungen (Technogym-App, nRF Connect, qdomyos-zwift) vorher trennen; das Gerät akzeptiert nur eine Verbindung.

In den Beispielen ist **`BLE_ADRESSE` zu ersetzen**. In `myrun_fast_monitor.py` und `myrun_fault_monitor.py` ist eine gerätespezifische Standardadresse fest im Code hinterlegt, die hier nicht wiederholt wird. Die übrigen Programme haben keine Standardadresse und suchen ohne `--address` nur über den Namen. `--name MyRun` ist eine Teilstring-Suche und keine eindeutige Identifikation, falls mehrere gleichnamige Geräte in Reichweite sind. Alle Programme bieten `-h` / `--help` (beendet vor der Gerätesuche).

## 2. Empfohlene Abläufe

### (a) Nur Fehlerspeicher und Status lesen – `myrun_dump.py`

Geeignet für Dritte und für den ersten Kontakt: kein START, keine Bewegung.

```bash
python3 myrun_dump.py --address BLE_ADRESSE --output diagnosebericht.txt
```

Der Bericht enthält Firmware, Fehlerspeicher (`@RERRORLOG#`), Status, Höhen-ADC und Digital-I/O. Hinweise: Gerät eingeschaltet und in Ruhe lassen; Band nicht von Hand bewegen. Die Schritte Init und Setup werden trotzdem gesendet.

### (b) Lauf mit Profil und Aufzeichnung – `myrun_fast_monitor.py` (aktiv)

Nur wenn der Lauf wirklich gewollt ist:

1. Niemand auf dem Band, Gerät montiert, Abdeckungen geschlossen, Not-Stopp-Schlüssel erreichbar, Bereich frei.
2. Zuerst Ablauf (a) ausführen und den Fehlerspeicher prüfen. Das Skript startet nur bei `QSWaitForStart` oder `QSWaitForStartRC`; sonst bricht es mit „START suppressed“ ab (Gerät aus- und einschalten).
3. Mit Enter-Freigabe starten (nicht mit `--auto-start`, solange man nicht sicher ist):

```bash
python3 myrun_fast_monitor.py --address BLE_ADRESSE --duration 150 --start-delay 10 --ramp --output lauf_neu
```

4. Band nach dem Ende physisch prüfen. Das STOP-Quittungssignal beweist keinen Stillstand.

### (c) Passives Mitschreiben bei Konsolenstart – `--listen-poll`

Das Band wird an der Konsole gestartet, das Skript liest nur mit (Stufe 0):

```bash
python3 myrun_fast_monitor.py --address BLE_ADRESSE --listen-poll 1 --slow-every 5 --duration 180 --output passiv_neu
```

Für reines Notification-Sammeln ohne jeden Befehl: `--listen-only`. Für nur Encoderwerte: `myrun_renc_watch.py`. Ein Mitlaufen bleibt nicht völlig rückwirkungsfrei (Lesebefehle belegen den Textkanal). Hinweis: `--no-start` ist **kein** passiver Modus, denn es sendet Init und Setup.

## 3. `myrun_fast_monitor.py`

Zweck: TXT-/CSV-Aufzeichnung mit Zeitstempeln. Nimmt alle Notifications auf (FTMS Treadmill Data, Machine Status, Training Status, RSC, weitere), fragt `@RPWM#` und `@RENC#` schnell und `@STATUS#`/`@DUMPIO#` langsamer ab, optional Fahrprofil. Der Kommentarkopf des Skripts beschreibt es als Verbesserung von `myrun_fault_monitor.py` (siehe Abschnitt 5): es **löst diesen ab**. Stufe 0 bis 2 je nach Modus (Abschnitt 1). [Quelltext](../myrun_fast_monitor.py).

### Optionen

| Option | Standard | Wirkung |
|---|---|---|
| `--address ADRESSE` | feste Geräteadresse im Code | Zuerst Adresssuche (15 s; mit `--wait-device` wiederholt je 10 s). |
| `--name TEXT` | `MyRun` | Teilstring für den Namensfallback (20 s). **Mit positivem `--wait-device` gibt es keinen Namensfallback**, nur wiederholte Adresssuche. |
| `--duration SEK` | `120.0` | Dauer der Mess-/Poll-Schleife. Verbindung, Setup, Bereitschaft, Countdown und Abschlussabfragen kommen hinzu; laufende BLE-Aufrufe können das Ende verzögern. |
| `--dumpio-every SEK` | `3.0` | Mindestabstand zwischen zwei `@DUMPIO#` **im normalen/aktiven Modus** (auch mit `--no-start`). Wird bei `--listen-poll` nicht benutzt. Siehe Abschnitt 3.2. |
| `--status-every SEK` | `5.0` | Mindestabstand zwischen `@STATUS#` im normalen Modus; bei `--listen-poll` stattdessen `--slow-every`. |
| `--post-fault SEK` | `8.0` | Nach erkanntem `QSHardwareFault` noch höchstens so lange aufzeichnen (Ende der Schleife = Fehlerzeit + Wert, falls früher als `--duration`). Der Fehler wird nur beim `@STATUS#`-Poll erkannt. |
| `--byte-delay SEK` | `0.04` | Pause zwischen den ASCII-Befehlsbytes. Gerätetiming; nicht ohne Vergleich verkürzen. |
| `--no-write-response` | aus | Textbefehls-Bytes ohne ATT-Schreibbestätigung schreiben. FTMS-Schreibvorgänge bleiben mit Bestätigung. |
| `--no-start` | aus | Kein START und kein STOP. FTMS-Init, Setup, Baseline und die komplette Poll-Schleife (`@RPWM#`, `@RENC#`, `@DUMPIO#`, `@STATUS#`) laufen wie im aktiven Modus. Keine Enter-Abfrage, keine Zustandsprüfung als Startbedingung. Unvereinbar mit `--steps`/`--ramp`. |
| `--listen-only` | aus | Nur GATT-Inventar und Notifications, `--duration` lang; kein Init, Setup oder Befehl. |
| `--listen-poll SEC` | `0` (aus) | Wert > 0 aktiviert Listen-Poll (setzt `--listen-only` voraus): `@RERRORLOG#` am Anfang und Ende, dazwischen `@RENC#` je Zyklus. Zyklusziel SEC; ein langsamer Zyklus ist länger als SEC. Negativ: Abbruch mit Meldung. |
| `--slow-every N` | `5` | Nur Listen-Poll: `@STATUS#`, `@DUMPIO#`, `@RPWM#` in jedem N-ten Zyklus (Zyklen 0, N, 2N, … , also auch im ersten). Intern mindestens 1. |
| `--steps PROFIL` | leer | Zeitprofil nach START: kommagetrennt `SEK:speed=KMH` oder `SEK:incline=PROZENT`, Dezimalpunkt. Sortiert nach Zeit, bei gleicher Zeit zuerst `incline`, dann `speed`. Werte außerhalb der Grenzen (Abschnitt 3.1) brechen vor jeder Verbindung ab. Nur mit aktivem START. |
| `--ramp` | aus | Eingebautes Profil (3.1); ein nichtleeres `--steps` hat Vorrang. |
| `--wait-device SEK` | `0` | Adresssuche wiederholen, bis das Gerät sichtbar ist oder ungefähr SEK abgelaufen sind (Gerät erst nach Skriptstart einschalten). |
| `--wait-ready SEK` | automatisch | Standard 0 s; mit positivem `--wait-device` 150 s. Wartet nach Verbindung/Setup, alle 3 s per `@STATUS#`, auf `QSWaitForStart`/`QSWaitForStartRC`. Nicht im reinen Listen-Modus. Nach Ablauf wird im aktiven Modus START unterdrückt; mit `--no-start` läuft das Skript einfach weiter. |
| `--start-delay SEK` | `0` | Countdown (mit Signalton) nach Enter bzw. nach Bereitschaft bei `--auto-start`; danach wird der Zustand erneut geprüft und START nur bei Start-Zustand gesendet. Negativ: Abbruch. |
| `--auto-start` | aus | START ohne Enter. Unvereinbar mit `--no-start`, `--listen-only`, `--listen-poll > 0`. `--start-delay` 0 wird zu 20 s; Werte unter 10 s: Abbruch. |
| `--output BASIS` | `myrun_fast_monitor_JJJJMMTT_HHMMSS` | Erzeugt `BASIS.txt` und `BASIS.csv` (keine Erweiterung angeben). Vorhandene gleichnamige Dateien werden überschrieben. |

Rückgabewerte: 0 normal, 1 Start-Freigabe abgelehnt (Strg+C/EOF), 2 Argumentfehler oder Gerät nicht gefunden, 4 START unterdrückt (Zustand nicht bereit), 130 Abbruch.

### 3.1 Grenzen, Profile, Start

- **Profilgrenzen:** Geschwindigkeit **0,8–2,9 km/h** (unter der Läufererkennung bei 3,0 km/h), Neigung **0–5 %**. Sie gelten nur für explizite Profilwerte.
- START ohne Geschwindigkeitsbefehl lässt das Band am untersuchten Gerät mit etwa **1,2 km/h** anlaufen; diese Voreinstellung liegt in der Firmware und wird von den Profilgrenzen nicht begrenzt.
- Eingebautes Profil `--ramp`:

```text
30:speed=2.5,60:speed=2.9,75:incline=2.0,90:speed=2.5,105:incline=0,120:speed=1.2
```

- Zeiten zählen ab dem START-Befehl. Schritte werden erst zwischen BLE-Abfragen bearbeitet und können später als geplant gesendet werden. Schritte hinter dem Ende von `--duration` werden nie gesendet (es erscheint nur ein Hinweis, wenn `--duration` kürzer als letzter Schritt + 15 s ist).
- Nach erkanntem Hardwarefehler werden keine weiteren Schritte gesendet. Wurde eine Neigung gesendet, wird vor STOP 0 % angefordert, aber nur bei bestehender Verbindung und ohne erkannten Hardwarefehler.
- Nach einem erkannten Geschwindigkeitsverlust (Encoder 0 Hz nach >0, oder `MeasSpeed` 0 nach >0,2 außerhalb von Stopp-Zuständen) werden höchstens zwei Sofort-Schnappschüsse (`@DUMPIO#`, `@STATUS#`) aufgezeichnet.
- Normaler Modus: Der START wird nur gesendet, wenn die Baseline `QSWaitForStart` oder `QSWaitForStartRC` zeigt. Danach Enter (oder `--auto-start`), ggf. Countdown mit erneuter Zustandsprüfung. Am Ende immer STOP-Versuch, sofern START versucht wurde (auch ohne ACK).

### 3.2 `@DUMPIO#`: wie oft abgefragt, wann werden IO-Wechsel erfasst

Nur Code-Lesart, keine Aussage über einen bestimmten Lauf.

**Abfragehäufigkeit**

- *Normaler/aktiver Modus und `--no-start`:* Die Schleife fragt je Durchlauf `@RPWM#` und `@RENC#`. Am Ende jedes Durchlaufs wird geprüft, ob `--dumpio-every` (Standard 3 s) seit der letzten `@DUMPIO#`-Abfrage vergangen ist; wenn ja, wird abgefragt und der nächste Termin auf „jetzt + Wert“ gesetzt. Der tatsächliche Abstand ist also Wert + Dauer der DUMPIO-Antwort + Rest des laufenden Durchlaufs, praktisch etwas über 3 s. Zusätzlich je ein Basiswert vor dem Lauf, ein Wert bei „READY“ (nur bei `--wait-ready` > 0) und höchstens zwei Schnappschüsse nach Geschwindigkeitsverlust. Nach dem Lauf folgt `DUMPIO_END` (nur im TXT).
- *`--listen-poll`:* `--dumpio-every` wird ignoriert. `@DUMPIO#` wird in jedem `--slow-every`-ten Zyklus abgefragt (Standard 5, erster Zyklus eingeschlossen). Der Abstand ist etwa `slow-every` Zyklen; die Zykluszeit steht in jeder `POLL`-Zeile des TXT (`cycle x.x s`) und ist bei langsamen Zyklen größer als `--listen-poll`. Danach `DUMPIO_END` (nur im TXT).

**Was ins CSV kommt**

- `io_<NAME>` (nur Zeilen `OUT`/`IN`/`PWM <NAME> = <Ganzzahl>` der DUMPIO-Antwort) wird beim ersten erfolgreichen Parsen (Baseline bzw. erster langsamer Zyklus) vollständig und danach **nur bei Änderung gegenüber dem zuletzt bekannten Wert** geschrieben. Es gibt keine periodische Volltabelle.
- Die Abschlussabfrage `DUMPIO_END` steht nur im TXT, nicht im CSV.
- Folge: Bleibt jeder abgefragte IO-Wert gleich, stehen im CSV nur die Zeilen vom Anfang. Ein IO-Wechsel mitten im Lauf (z. B. ein Wechsel von `ELEV_DOWN`) erscheint dann, wenn der geänderte Wert bei einer DUMPIO-Abfrage noch ansteht. Sein Zeitstempel ist der Zeitpunkt nach Eintreffen der Antwort, der echte Wechsel liegt irgendwo zwischen der vorherigen und dieser Abfrage.
- Ein Wechsel, der kürzer dauert als der Abfrageabstand und vor der nächsten Abfrage wieder zurückgeht, wird nicht erfasst. Das gilt für beide Modi. Läuft eine DUMPIO-Antwort in den Timeout (4 s), wird nur der empfangene Teil ausgewertet.

**Dichter abfragen (nur Optionen, kein Codeeingriff):** im aktiven Modus `--dumpio-every 1`, im Listen-Poll `--slow-every 1`. Auch dann bleibt die Rate durch die Schleifendauer begrenzt (Befehl mit 0,04 s je Byte plus Antwort). Gleiche Standardwerte können daher in einem Lauf nur Anfangszeilen und in einem anderen einen Mittelwechsel liefern, abhängig davon, ob sich zum Abfragezeitpunkt ein IO-Wert unterscheidet.

### 3.3 Beispiele

```bash
# Passiv mitschreiben (Stufe 0), Konsole separat bedienen
python3 myrun_fast_monitor.py --address BLE_ADRESSE --listen-poll 1 --slow-every 5 --duration 120 --output passiv_neu

# Nur Notifications, keinerlei Befehle
python3 myrun_fast_monitor.py --address BLE_ADRESSE --listen-only --duration 120

# Polling mit Init, ohne START; Gerät erst nach Skriptstart einschalten, keine Enter-Abfrage
python3 myrun_fast_monitor.py --address BLE_ADRESSE --no-start --wait-device 300 --duration 120 --output ohne_start

# Aktiver Lauf mit Enter-Freigabe und eingebautem Profil
python3 myrun_fast_monitor.py --address BLE_ADRESSE --duration 150 --ramp

# Aktiv und automatisch: startet nach Bereitschaft und 20 s Countdown OHNE Enter
python3 myrun_fast_monitor.py --address BLE_ADRESSE --wait-device 300 --auto-start --start-delay 20 --duration 150 --steps "30:speed=2.0,60:speed=2.9,90:incline=1.0,120:incline=0"
```

`--no-start` zusammen mit `--wait-device` wartet auf das Gerät und (bis `--wait-ready`, hier 150 s) auf einen Start-Zustand, fragt aber **nicht** nach Enter und sendet nie START/STOP.

### 3.4 Ausgabe

TXT: Verbindungs- und GATT-Daten, Setup-Antworten, Firmware, Fehlerlog am Anfang/Ende, Zustandswechsel (`STATE`), `IO CHANGE`, Quittierungen, `SPEED_LOSS`/`SPEED_JUMP` (Markierungen des Skripts, keine Herstellerfehlercodes), Notification-Zähler und Zusammenfassung.

CSV, Header **`t_rel_s,wallclock,utc,signal,value`**. Eine Zeile je Einzelwert mit eigener Zeit, keine simultane Messwertzeile.

| `signal` | Inhalt |
|---|---|
| `enc_hz`, `enc_kmh` | Aus `@RENC#`: Encoderfrequenz und daraus vom Gerät berechnete Geschwindigkeit |
| `state`, `meas_speed` | Aus `@STATUS#`: Zustandsname (`QS…`) und `MeasSpeed` |
| `io_<NAME>` | Aus `@DUMPIO#`, nur bei Änderung (3.2); z. B. `io_PWM_MOTOR` |
| `pwm_pct` | Zahl aus `@RPWM#`; Beziehung zur echten Gate-PWM nicht bestätigt |
| `ftms_speed_kmh` | FTMS 0x2ACD-Geschwindigkeit; bei der untersuchten Firmware der **Sollwert**, keine Ist-Geschwindigkeit |
| `ftms_incline_pct` | Neigungsfeld aus 0x2ACD; kein Nachweis tatsächlicher Höhenbewegung |
| `rsc_speed_kmh`, `rsc_cadence` | Dekodierte RSC-Notifications |
| `machine_status`, `training_status`, `ftms_cp` | FTMS-Ereignisse und Control-Point-Antworten (Hexdaten) |
| `step_speed`, `step_incline` | Vom Profil gesendeter Zielwert (Quittung und Wirkung im TXT prüfen) |
| `raw_renc`, `raw_rpwm` | Rohantworten, nur in der aktiven Schleife |
| `raw_2acd`, `raw_<4 Hex>` | Rohnotification von 0x2ACD bzw. weiteren Characteristics (4 Hexzeichen der UUID) |

Nicht jedes Signal entsteht in jedem Modus. Eine ausgebliebene Änderung zwischen Polls schließt einen kurzen Aussetzer nicht aus.

## 4. `myrun_incline_test.py`

Zweck: Baseline, START, Zielneigung zweimal, Rückkehr auf 0 %, STOP, jeweils mit Proben von `@DUMPIO#`, `@STATUS#`, `@RADCEXT#`. Stufe 2. [Quelltext](../myrun_incline_test.py).

| Option | Standard | Wirkung |
|---|---|---|
| `--address ADRESSE` | keine | Adresssuche (15 s), danach Namenssuche (20 s) |
| `--name TEXT` | `MyRun` | Namens-Teilstring |
| `--target PROZENT` | `2.0` | Zielneigung; zulässig **0,5–5,0 %**, sonst Abbruch mit Rückgabe 2. 0 % wird intern für die Rückfahrt gesendet. |
| `--output DATEI` | `myrun_incline_test_JJJJMMTT_HHMMSS.txt` | Textbericht, wird überschrieben |

```bash
python3 myrun_incline_test.py --address BLE_ADRESSE --target 1.0 --output neigungstest.txt
```

Ablauf: FTMS-Init, Setup, Baseline-Proben, 3-s-Countdown, **START ohne weitere Abfrage**, Zielneigung, Probe A, Zielneigung erneut, Probe B, Neigung 0 %, Probe, STOP/PAUSE, Abschlussprobe. Kein Enter-Dialog, keine Zustandsprüfung vor START (auch bei Hardwarefehler wird gesendet). Wird START nicht mit SUCCESS quittiert, wird die Zielneigung trotzdem angefordert (die Antwort wird protokolliert). STOP wird im `finally`-Block gesendet, sofern START gesendet wurde und die Verbindung besteht. Ein ACK bestätigt nur den Befehl, nicht die Bewegung. Textantwort-Timeout 6 s, FTMS-Timeout 4 s, Byteabstand 0,04 s (fest). Ausgabe nur TXT (Befehl, Zeit, Rohantwort, HEX, FTMS TX/RX und Ergebnisname), keine CSV.

## 5. `myrun_fault_monitor.py` (Vorgänger)

Zweck: Älterer aktiver Fehlerübergangsmonitor. Der Kommentarkopf von `myrun_fast_monitor.py` führt seine Verbesserungen ausdrücklich gegenüber diesem Programm auf (Notifications, schnellere Kurzabfragen, CSV, Zusammenfassung); der Fault-Monitor bleibt als ältere, einfachere Implementierung im Repo. Für neue Aufzeichnungen ist `myrun_fast_monitor.py` vorzuziehen. Stufe 2. [Quelltext](../myrun_fault_monitor.py).

| Option | Standard | Wirkung |
|---|---|---|
| `--address ADRESSE` | feste Geräteadresse im Code | Adresse, danach Namensfallback |
| `--name TEXT` | `MyRun` | Namens-Teilstring |
| `--output DATEI` | `myrun_fault_monitor_JJJJMMTT_HHMMSS.txt` | Textbericht, wird überschrieben |
| `--incline PROZENT` | keine | Einmaliger Zielwert **0,5–2,0 %** nach erfolgreich quittiertem START; es gibt keine Rückfahrt auf 0 % |
| `--duration SEK` | `120.0` | Monitoring nach START; muss > 0 sein |
| `--interval SEK` | `0.2` | Pause (≥ 0) nach jedem STATUS/DUMPIO-Paar; keine 5-Hz-Abtastung |

```bash
python3 myrun_fault_monitor.py --address BLE_ADRESSE --duration 120 --interval 0.2 --output fehlerlauf.txt
```

Vor der Verbindung muss genau **`START FREIGEBEN`** eingetippt werden. Nach Init/Setup und Baseline wird START unterdrückt, wenn die Baseline nicht lesbar ist oder `QSHardwareFault` enthält (Rückgabe 4). Andere Zustände (also nicht nur `QSWaitForStart*`) lassen START zu, im Unterschied zum Fast-Monitor. Schleife: `@STATUS#` und `@DUMPIO#` im Wechsel mit vollem Rohtext im TXT; bei `QSHardwareFault` endet die Schleife sofort. Am Ende STOP-Versuch und Abschlussabfragen. Keine CSV, kein Geschwindigkeitsparameter, kein Profil.

## 6. `myrun_probe.py`

Zweck: Lesebefehle einmal abfragen; optional vermutete Befehle und eine Beobachtungsphase. Stufe 1. [Quelltext](../myrun_probe.py).

| Option | Standard | Wirkung |
|---|---|---|
| `--address ADRESSE` | keine | Adresse, danach Namensfallback |
| `--name TEXT` | `MyRun` | Namens-Teilstring |
| `--guess` | aus | Zusätzlich 31 vermutete, undokumentierte Befehle probieren (`@HELP#`, `@RTEMP#`, `@RVBUS#`, …). Unbekannte Befehle ergeben `!…:ERROR` oder Timeout. |
| `--extra BEFEHL` | leer | Weiteren Befehl probieren; wiederholbar. Fehlendes `@`/`#` wird ergänzt. |
| `--watch SEK` | `0` | Nach der Hauptrunde SEK lang `@RENC#`, `@STATUS#`, `@DUMPIO#` fortlaufend wiederholen |
| `--output DATEI` | `myrun_probe_JJJJMMTT_HHMMSS.txt` | Report |

```bash
python3 myrun_probe.py --address BLE_ADRESSE --watch 30 --output befehlsprobe.txt
```

Feste Liste (17 Befehle, u. a. `@FWVER#`, `@RERRORLOG#`, `@STATUS#`, `@DUMPIO#`, `@RENC#`, `@RPWM#`, `@RADC#`, `@RADCEXT#`, `@RKPWM#`, `@RQSPAR#`, `@RSTAT#`, `@RTASKHANG#`, `@RRUNDETMINSP#`, `@GETDATE#`, `@RTG_ID#`, `@RDS_UP#`, `@RDS_DOWN#`). **Sperrliste `BLOCKED_PATTERNS`** (Regex auf den Befehl in Großbuchstaben): `RESET`, `^@S` (außer genau `@STATUS#`), `SET`, `INIT`, `CAL`, `ELEV`, `FORCE`, `SUSPEND`, `STG_ID`, `WRITE`, `ERASE`, `CLEAR`, `FORMAT`, `UPD`, `BOOT`, `FLASH`. Betroffene Befehle (auch aus `--extra`) werden nicht gesendet und als „BLOCKIERT“ vermerkt. Das feste Setup läuft außerhalb dieser Sperre. Die Sperrliste beweist nicht die Harmlosigkeit jedes unbekannten Befehls; `--guess` und `--extra` sind keine Routineoptionen. Timeout je Befehl 5 s, 0,4 s Pause zwischen Befehlen, Byteabstand fest 0,04 s. Ausgabe nur TXT: je Befehl Zeit, Status, lesbare Antwort und HEX, am Ende eine Übersicht; keine CSV. Die bisher erprobten Vermutungsbefehle (Temperatur, Busspannung, Strom) lieferten keine Antwort (siehe [BLE_PROTOKOLL.md](BLE_PROTOKOLL.md)).

## 7. `myrun_dump.py`

Zweck: Einmaliger Diagnosebericht. Stufe 1. [Quelltext](../myrun_dump.py).

| Option | Standard | Wirkung |
|---|---|---|
| `--address ADRESSE` | keine | Adresse, danach Namensfallback |
| `--name TEXT` | `MyRun` | Namens-Teilstring |
| `--output DATEI` | `myrun_diagnostic_JJJJMMTT_HHMMSS.txt` | Berichtsdatei, wird überschrieben |

```bash
python3 myrun_dump.py --address BLE_ADRESSE --output diagnosebericht.txt
```

Ablauf (fest): Prüfung, dass die drei benötigten Characteristics vorhanden sind (sonst Rückgabe 4), FTMS-Init, Setup, dann `@FWVER#`, `@RERRORLOG#`, `@STATUS#`, `@RADCEXT#`, `@DUMPIO#` je mit 6-s-Timeout und 0,5 s Pause. Bei Verbindungsverlust Abbruch (Rückgabe 5). Der Bericht (nur TXT) enthält Zeit, Befehl, lesbare Antwort und HEX, am Ende ggf. unvollständige Restdaten. Kein `--duration`, kein `--watch`, keine CSV; das Timing ist nicht per Option änderbar.

## 8. `myrun_renc_watch.py`

Zweck: Kleine Encoderaufzeichnung, z. B. um zu sehen, ob das Encodersignal bei von Hand bewegtem Band die Konsole erreicht. Stufe 0: nur Lesebefehle, kein Init, kein Setup, kein START/STOP. [Quelltext](../myrun_renc_watch.py).

| Option | Standard | Wirkung |
|---|---|---|
| `--address ADRESSE` | keine | Adresse, danach Namensfallback |
| `--name TEXT` | `MyRun` | Namens-Teilstring |
| `--duration SEK` | `60` | Beobachtungsfenster; der Timer läuft ab Gerätefund, also inklusive Verbindungsaufbau |
| `--interval SEK` | `0.5` | Pause nach jeder Abfrage, zusätzlich zur Befehls- und Antwortzeit (ein Zyklus dauert daher deutlich über 0,5 s) |
| `--byte-delay SEK` | `0.04` | Pause zwischen Befehlsbytes |
| `--cmd BEFEHL` | keiner | Erlaubt genau `@STATUS#`, `@DUMPIO#` oder `@RPWM#`; zusätzlich nach jedem fünften RENC-Zyklus abgefragt |
| `--output DATEI` | `myrun_renc_watch_JJJJMMTT_HHMMSS.csv` | CSV, wird überschrieben |

```bash
python3 myrun_renc_watch.py --address BLE_ADRESSE --duration 60 --interval 0.5 --cmd "@STATUS#" --output encoderverlauf.csv
```

CSV-Header **`t_rel_s,wallclock,enc_hz,enc_kmh,raw`**. Bei Timeout steht in `raw` `TIMEOUT` und die Zahlenfelder bleiben leer. Zeilen des Zusatzbefehls haben leere Encoderfelder und die Antwort in `raw`; Zeilenumbrüche sind ersetzt, Kommas durch Semikolons. Kein TXT-Bericht. Das Mitschreiben an einem Gerät im Standby: Handbewegung des Bandes kann dort einen GIRT-Fehler auslösen; das Skript fordert dazu nicht auf.

## 9. Grenzen und Datenschutz

- Explizite Profilwerte im Fast-Monitor: **0,8–2,9 km/h**, **0–5 %**; Incline-Test: Ziel 0,5–5,0 %; Fault-Monitor: 0,5–2,0 %. Die Skripte enthalten keinen Befehl für höhere Geschwindigkeiten.
- Der Fast-Monitor sendet START nur bei `QSWaitForStart`/`QSWaitForStartRC`; Incline-Test und Fault-Monitor prüfen weniger oder nichts (siehe 4 und 5).
- Keines der Skripte sendet `@SETDATE#` (verfälscht die Zeitstempel im Fehlerspeicher) oder schreibt in den unbekannten Dienst `6e40a8d5-…`.
- Reports können Geräteadresse und -namen, Seriennummern aus Antworten, GATT-Daten, lokale Zeitstempel und lokale Dateipfade enthalten. **Rohreports vor einer Veröffentlichung prüfen**; die festen Standardadressen stehen im Quelltext von `myrun_fast_monitor.py` und `myrun_fault_monitor.py`.

## 10. Mögliche spätere Verbesserungen

Nicht umgesetzt; jede Änderung, die Befehle, Timing, Standardwerte oder Sperren berührt, ist eine bewusste Verhaltensänderung mit eigener Prüfung.

- Gemeinsame Konstanten (UUIDs, Parser, FTMS-Payloads) und ein gemeinsamer Textkanal-Empfänger; die Empfänger unterscheiden sich derzeit bei Teilantworten, `!…:ERROR` ohne `#` und Timeout-Rückgaben und sollten nur mit aufgezeichneten Frames zusammengeführt werden.
- Klar getrennte Sitzungsmodi (nur Abos, Lesepolling, Setup ohne START, aktiver Lauf), damit passive Modi nicht versehentlich initialisieren.
- Einheitliche Optionen und Validierung (Standardadresse nur über Option oder Umgebung, gleiche Zeitparameter) und ein gemeinsames CSV-Format.
- Zusätzliche Schutzprüfungen im Incline-Test und Fault-Monitor (START nur aus Start-Zustand, Abbruch ohne START-ACK).
- Möglichkeit, `@DUMPIO#`-Volltabellen periodisch in die CSV zu schreiben statt nur Änderungen.
- Tote Stellen prüfen: `POLL_READ` (Fast-Monitor) ist definiert, aber unbenutzt; `fields()` (Fault-Monitor) hat keinen Aufrufer; das `disconnected`-Event im Incline-Test wird gesetzt, aber nicht abgefragt.
- Rein softwareseitige Tests ohne Gerät: zerstückelte Textframes, `ERROR` ohne Abschluss, Timeouts mit Restdaten, Profilgrenzen, keine Init/START-Befehle in passiven Modi.
