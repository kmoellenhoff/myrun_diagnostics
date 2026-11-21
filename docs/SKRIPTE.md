# Diagnoseprogramme – Bedienung und Aufräumentwurf

**ENTWURF auf `aufraeumen`, Code geprüft auf Stand `83da2fb`, 21.11.2026. Kein Skript wurde geändert.**

**Ursache wahrscheinlich C602, Stand: Gegenversuch offen.** Die folgenden Beispiele sind Bedienungsentwürfe, keine Aufforderung, den Gegenversuch oder einen Motorlauf jetzt auszuführen. Das Gerät muss für aktive Tests vollständig montiert und mechanisch sicher sein. Niemand auf dem Band, physischer Sicherheitsstopp erreichbar. Ein Software-STOP kann abgelehnt werden.

## 1. Auswahl nach tatsächlichem Verhalten

| Programm / Modus | Initialisierung / Setup | Motor-/Steigungsbefehle | Zweck |
|---|---|---|---|
| `myrun_fast_monitor.py --listen-only` | Kein FTMS-Init, keine Diagnosebefehle; GATT-Abos werden eingerichtet | Kein START/STOP | Nur Notifications sammeln |
| `myrun_fast_monitor.py --listen-poll SEC` | Kein FTMS-Init/Setup; lesende Diagnoseabfragen werden über BLE geschrieben | Kein START/STOP | Konsolenstart beobachten, Encoder und Status abfragen |
| `myrun_fast_monitor.py --no-start` | **FTMS-Init und Setup werden gesendet** | Kein eigener START/STOP | Diagnoseabfragen mit Initialisierung; nicht mit rein passiv verwechseln |
| `myrun_fast_monitor.py`, aktiver Standard | FTMS-Init und Setup | START nach Enter; optionale Profile; STOP-Versuch am Ende | Fehlstart-/Laufvergleich |
| `myrun_fast_monitor.py --auto-start` | Wie aktiver Standard | **Automatischer START ohne Enter**, nach Bereitschaft und Countdown | Nur bewusst vorbereiteter aktiver Versuch |
| `myrun_incline_test.py` | FTMS-Init und Setup | **Automatischer START nach Countdown**, Zielneigung zweimal, 0 %, STOP-Versuch | Kurzer Höhenverstellungstest, kein reiner Standby-Test |
| `myrun_fault_monitor.py` | FTMS-Init und Setup nach Terminalfreigabe | START, optional eine Neigung, STOP-Versuch | Älterer ausführlicher Fehlerübergangsmonitor |
| `myrun_probe.py` | **FTMS-Init und Setup** | Kein START/STOP/Neigungsbefehl aus dem Probe-Ablauf | Feste und optionale Diagnosebefehle prüfen |
| `myrun_dump.py` | **FTMS-Init und Setup** | Kein START/STOP | Einmaliger Diagnosebericht |
| `myrun_renc_watch.py` | Kein FTMS-Init/Setup; nur Lesebefehle auf dem Textkanal | Kein START/STOP | Kleine Encoderaufzeichnung |

„Lesend“ beschreibt die abgefragte Gerätefunktion, nicht das Ausbleiben aller BLE-Schreiboperationen. Das gemeinsame Setup vieler Programme enthält `@DISABLE_PACE#`, `@SSIUNITS#`, `@RJSK_EN 1#`, `@LJSK_EN 1#` und ist keine reine Messwertabfrage. Unbekannte Befehle werden nicht als garantiert wirkungslose Leseoperationen behandelt.

### Voraussetzungen und Geräteauswahl

Python 3, Linux/Bluetooth-LE-Umgebung mit BlueZ und Paket `bleak`; andere verbundene Trainings-/BLE-Apps vorher trennen. `python3 -m pip install bleak` installiert die Python-Abhängigkeit, ersetzt aber keine funktionierende Bluetooth-Konfiguration.

In allen Beispielen ist **`BLE_ADRESSE` vor Benutzung zu ersetzen**. Die gerätespezifischen Standardadressen aus zwei vorhandenen Skripten werden hier aus Datenschutzgründen nicht wiederholt. `--name MyRun` ist eine Namenssuche und keine eindeutige Identifikation mehrerer gleichnamiger Geräte. Alle sechs Programme bieten außerdem automatisch **`-h` / `--help`**; dadurch wird vor der Gerätesuche beendet.

## 2. `myrun_fast_monitor.py`

Zweck: TXT-/CSV-Aufzeichnung mit Zeitstempeln, Notifications, Encoder und langsamer abgefragtem Status/I/O, optional aktive Profile. [Quelltext](../myrun_fast_monitor.py).

### Sämtliche Optionen

| Option | Standard | Wirkung / Einschränkung |
|---|---|---|
| `--address ADRESSE` | Geräteadresse fest im Code | Zuerst Adresssuche; bei normaler Suche ggf. Namensfallback. Adresse bewusst setzen. |
| `--name TEXT` | `MyRun` | Teilstring für Namensfallback. **Mit positivem `--wait-device` erfolgt kein Namensfallback**, sondern wiederholte Adresssuche. |
| `--duration SEK` | `120.0` | Dauer der eigentlichen Aufzeichnung/Messschleife. Verbindung, Setup, Bereitschaft, Countdown und Abschlussabfragen kommen hinzu; laufende BLE-Aufrufe können den Endzeitpunkt überschreiten. |
| `--dumpio-every SEK` | `3.0` | Gewünschter Abstand von `@DUMPIO#` im normalen/aktiven Polling, keine garantierte Abtastrate. **Nicht der Takt im Listen-Poll-Modus.** |
| `--status-every SEK` | `5.0` | Entsprechend für `@STATUS#`; in Listen-Poll stattdessen `--slow-every`. |
| `--post-fault SEK` | `8.0` | Noch höchstens diese Zeit innerhalb des verbleibenden Zeitfensters nach erkanntem `QSHardwareFault` aufzeichnen; kein garantierter sofortiger physischer Stopp. |
| `--byte-delay SEK` | `0.04` | Pause zwischen ASCII-Befehlsbytes; Gerätetiming, nicht ohne Vergleich verkürzen. |
| `--no-write-response` | aus | ASCII-Schreiboperationen ohne ATT-Schreibbestätigung. Das deaktiviert keine Befehle und ändert nicht die FTMS-Quittierung. |
| `--no-start` | aus | Kein eigener START; Initialisierung und Setup bleiben aktiv. Der Modus kann das Konsolenverhalten beeinflussen. |
| `--listen-only` | aus | Nur Abos/Notifications, kein Init, kein Setup, keine Diagnoseabfragen, kein START/STOP. |
| `--listen-poll SEC` | `0` = aus | Bei positivem Wert Listen-Modus mit `@RENC#` je Zyklus und langsameren Zusatzabfragen; Fehlerlog am Anfang/Ende. Setzt intern `listen_only`. Negative Werte werden abgelehnt. |
| `--slow-every N` | `5` | Nur bei Listen-Poll: `@STATUS#`, `@DUMPIO#`, `@RPWM#` in jedem N-ten Zyklus, einschließlich erstem Zyklus. Intern mindestens 1. |
| `--steps PROFIL` | leer | Kommagetrennt `SEK:speed=WERT` oder `SEK:incline=WERT`, Dezimalpunkt. Zeitpunkte werden sortiert; gleiche Zeitpunkte sind kein zugesicherter Benutzerreihenfolge-Mechanismus. Nur mit aktivem START. |
| `--ramp` | aus | Vorgegebenes Profil unten; ein ausdrücklich nichtleeres `--steps` hat Vorrang. |
| `--wait-device SEK` | `0` | Wiederholte Adresssuche bis ungefähr zu diesem Zeitfenster. Einzelne Suchaufrufe können es überschreiten. |
| `--wait-ready SEK` | automatisch | Ohne `--wait-device`: 0; mit positivem `--wait-device`: 150. Wartet auf `QSWaitForStart` oder `QSWaitForStartRC` nach Verbindung/Setup; im reinen Listen-Modus nicht benutzt. |
| `--start-delay SEK` | `0` | Countdown nach Enter bzw. bei Auto-Start. Nicht negativ; bei Auto-Start bedeutet 0 intern 20. Bei positivem Countdown wird der Zustand vor START erneut geprüft. |
| `--auto-start` | aus | Kein Enter nötig. Nur aktiv; unvereinbar mit `--no-start`, `--listen-only`, positivem `--listen-poll`. Countdown mindestens 10 s, andernfalls Abbruch. |
| `--output BASIS` | `myrun_fast_monitor_YYYYMMDD_HHMMSS` | Erstellt `BASIS.txt` und `BASIS.csv`. Keine Erweiterung angeben. Vorhandene gleichnamige Dateien werden geöffnet mit `w` und überschrieben. |

`-h` / `--help` gehört ebenfalls zu diesem Parser. Weitere Grenzprüfungen sind nicht für sämtliche Zeitparameter einheitlich vorhanden; die Dokumentation behauptet keine zusätzliche Validierung.

### Profile und Grenzen

Die **programmierten Grenzen für explizite Profilwerte** sind **0,8–2,9 km/h** und **0–5 %**. Sie sind keine allgemeine Eignungs- oder Sicherheitsbescheinigung für ein defektes Gerät. START ohne expliziten Geschwindigkeitsbefehl hat am untersuchten Gerät etwa **1,2 km/h** ausgelöst; der Programmcode kann eine abweichende Firmware-Voreinstellung nicht durch seine Profilgrenzen begrenzen.

`--ramp` entspricht:

```text
30:speed=2.5,60:speed=2.9,75:incline=2.0,90:speed=2.5,105:incline=0,120:speed=1.2
```

Profile sind nur im aktiven Modus zulässig. Kurze `--duration` im Verhältnis zum letzten Schritt führt nur zu einem Hinweis, nicht zur automatischen Verlängerung. Schritte werden erst zwischen BLE-Abfragen bearbeitet und können verspätet gesendet werden. Bei erkanntem Hardwarefehler werden weitere Schritte unterlassen; eine zuvor angeforderte Steigung wird vor STOP nur zurückgesetzt, wenn die Verbindung besteht und noch kein Hardwarefehler erkannt wurde. Das ist kein garantiertes Zurückfahren.

### Beispiele

```bash
# Beobachten, Konsole separat bedienen; kein START durch das Skript
python3 myrun_fast_monitor.py --address BLE_ADRESSE --listen-poll 1 --slow-every 5 --duration 120 --output passiv_neuer_lauf

# Nur Notifications, keinerlei Diagnosebefehle
python3 myrun_fast_monitor.py --address BLE_ADRESSE --listen-only --duration 120

# Aktiver, ausdrücklich vorbereiteter Versuch mit Enter-Freigabe
python3 myrun_fast_monitor.py --address BLE_ADRESSE --duration 150 --ramp

# Aktiver automatischer Versuch: startet nach Bereitschaft ohne Enter
python3 myrun_fast_monitor.py --address BLE_ADRESSE --wait-device 300 --auto-start --start-delay 20 --duration 150 --steps "30:speed=2.0,60:speed=2.9,90:incline=1.0,120:incline=0"
```

`--no-start` ist kein geeigneter Ersatz für Listen-Poll, wenn ein manueller Konsolenstart unbeeinflusst beobachtet werden soll. Handbewegung des Bandes im Standby hat selbst schon einen Fehler ausgelöst; vor einem sauberen Startvergleich keine solche Bewegung einplanen.

### Ausgabe und Bedeutung der CSV

Genauer Header: **`t_rel_s,wallclock,utc,signal,value`**. Eine Zeile beschreibt einen einzelnen Wert mit eigener Zeit, keine simultane Messwertzeile.

| Signal / Gruppe | Inhalt |
|---|---|
| `enc_hz`, `enc_kmh` | Encoderfrequenz und daraus vom Gerät gemeldete Geschwindigkeit aus `@RENC#` |
| `meas_speed`, `state` | Werte aus `@STATUS#`; Zustand der Konsolendiagnose, kein direkter Nachweis der Q2-Ansteuerung |
| `io_...`, insbesondere `io_PWM_MOTOR` | I/O-Diagnosewerte; im normalen Modus vor allem Baseline und Änderungen gespeichert, daher keine lückenlose periodische Volltabelle |
| `pwm_pct` | Zahl aus `@RPWM#`; Skalierung/Beziehung zur wirklichen Q2-Gate-PWM nicht abschließend bestätigt |
| `ftms_speed_kmh` | Bei der untersuchten Firmware **Sollwert**, keine unabhängige Ist-Geschwindigkeit |
| `ftms_incline_pct` | Übertragenes Neigungsfeld; kein alleiniger Nachweis tatsächlicher Höhenbewegung |
| `rsc_speed_kmh`, `rsc_cadence` | Dekodierte RSC-Notifications |
| `machine_status`, `training_status`, `ftms_cp` | FTMS-Ereignisse und Control-Point-Antworten |
| `step_speed`, `step_incline` | Vom Profil gesendeter Zielwert; ACK und tatsächliche Reaktion im TXT prüfen |
| `raw_renc`, `raw_rpwm`, `raw_2acd`, weitere `raw_...` | Modusabhängige Rohantworten/Notifications; nicht alle Signale entstehen in jedem Modus |

TXT enthält u. a. Verbindungs-/GATT-Daten, Quittierungen, Zustandswechsel, Fehlerlog und ggf. Zusammenfassung. `SPEED_LOSS` ist eine Skriptmarkierung, kein Herstellerfehlercode. Eine ausgebliebene Änderung zwischen Polls schließt einen kurzen Aussetzer nicht aus. `--dumpio-every 1` kann im aktiven Modus häufigere Abfragen anfordern, aber keinen vollständigen 1-Hz-Takt garantieren.

## 3. `myrun_incline_test.py`

Zweck: Baseline, echter START, Zielneigung zweimal, Rückkehranforderung auf 0 %, STOP-Versuch und Statusabfragen. [Quelltext](../myrun_incline_test.py).

| Option | Standard | Wirkung |
|---|---|---|
| `--address ADRESSE` | keine | Adresssuche, danach ggf. Namenssuche |
| `--name TEXT` | `MyRun` | Namens-Teilstring |
| `--target PROZENT` | `2.0` | Akzeptiert **0,5–5 %**; 0 % wird intern für die Rückfahrt gesendet, ist aber kein zulässiger Testzielwert dieses Arguments |
| `--output DATEI` | `myrun_incline_test_YYYYMMDD_HHMMSS.txt` | Textbericht, bestehende Datei wird überschrieben |
| `-h`, `--help` | – | Hilfe und Beenden |

```bash
python3 myrun_incline_test.py --address BLE_ADRESSE --target 1.0 --output neuer_neigungstest.txt
```

**Kein Enter-Dialog und kein `--duration`: Nach Verbindung, Setup und Baseline läuft ein Drei-Sekunden-Countdown, danach wird START gesendet.** Auch nach nicht erfolgreich quittiertem START wird einmal regulär die Zielneigung angefordert und der weitere Test ausgeführt. Das ist ein reales vorhandenes Verhalten, keine empfohlene Schutzstrategie. Ein ACK bestätigt den Befehl, nicht die mechanische Bewegung. Ausgabe nur TXT mit Rohantworten, Zeitstempeln und FTMS-Antworten; keine eigene CSV.

## 4. `myrun_fault_monitor.py`

Zweck: Älterer aktiver Übergangsmonitor; ausführliche STATUS-/DUMPIO-Rohtexte und Fehlerlog. [Quelltext](../myrun_fault_monitor.py).

| Option | Standard | Wirkung |
|---|---|---|
| `--address ADRESSE` | Geräteadresse im Code | Adresse, ggf. Namensfallback |
| `--name TEXT` | `MyRun` | Namenssuche |
| `--output DATEI` | `myrun_fault_monitor_YYYYMMDD_HHMMSS.txt` | Textbericht, `w`-Modus |
| `--incline PROZENT` | keine | Einmaliger Zielwert **0,5–2 %** nach erfolgreich quittiertem START; keine zugesicherte Rückfahrt auf 0 % |
| `--duration SEK` | `120.0` | Monitoring nach START, muss positiv sein |
| `--interval SEK` | `0.2` | Nichtnegative Pause **nach** STATUS-/DUMPIO-Paar; keine 5-Hz-Garantie |
| `-h`, `--help` | – | Hilfe und Beenden |

```bash
python3 myrun_fault_monitor.py --address BLE_ADRESSE --duration 120 --interval 0.2 --output neuer_fehlerlauf.txt
```

Vor der Verbindung ist exakt **`START FREIGEBEN`** einzutippen. START wird bei unlesbarer Baseline oder `QSHardwareFault` unterdrückt; die Bereitschaftsprüfung ist nicht dieselbe strenge Zustandsliste wie im Fast-Monitor. Bei erkannter Störung endet die normale Schleife und es folgen Abschlussabfragen/STOP-Versuch. Kein eigener Geschwindigkeitsparameter, keine CSV, keine Profiloptionen.

## 5. `myrun_probe.py`

Zweck: Diagnosebefehle einmal abfragen; optional zusätzliche angenommene Lesebefehle und Beobachtungsphase. [Quelltext](../myrun_probe.py).

| Option | Standard | Wirkung |
|---|---|---|
| `--address ADRESSE` | keine | Adresse, ggf. Namensfallback |
| `--name TEXT` | `MyRun` | Namenssuche |
| `--guess` | aus | Liste undokumentierter Befehle zusätzlich probieren; Semantik nicht herstellerseitig bestätigt, Timeouts möglich |
| `--extra BEFEHL` | leere Liste | Wiederholbar; fehlendes `@`/`#` wird ergänzt, danach Blockprüfung |
| `--watch SEK` | `0` | Nach der ersten Runde für diese Zeit RENC/STATUS/DUMPIO wiederholen; keine garantierte Messfrequenz |
| `--output DATEI` | `myrun_probe_YYYYMMDD_HHMMSS.txt` | TXT mit Befehlen, Antworten, HEX und Zusammenfassung; keine CSV |
| `-h`, `--help` | – | Hilfe und Beenden |

```bash
python3 myrun_probe.py --address BLE_ADRESSE --watch 30 --output neue_befehlsprobe.txt
```

Die Probe sendet keinen START/STOP, initialisiert aber FTMS und führt Setup aus. `BLOCKED_PATTERNS` sperrt schreib-/reset-/kalibrier-/bewegungsverdächtige Probe-Kommandos, auch aus `--extra`; **das feste Setup läuft außerhalb dieser Sperre**. Eine Namenskonvention und Blockliste beweisen nicht die Harmlosigkeit jedes undokumentierten Befehls. `--guess` und `--extra` sind deshalb keine empfohlenen Routinebeispiele. ERROR-Antworten können ohne `#` enden; der Empfänger berücksichtigt das.

## 6. `myrun_dump.py`

Zweck: Einmaliger Bericht mit Firmware, Fehlerlog, Status, erweitertem Höhen-ADC und I/O. [Quelltext](../myrun_dump.py).

| Option | Standard | Wirkung |
|---|---|---|
| `--address ADRESSE` | keine | Adresse, ggf. Namensfallback |
| `--name TEXT` | `MyRun` | Namenssuche |
| `--output DATEI` | `myrun_diagnostic_YYYYMMDD_HHMMSS.txt` | Vollständiger Dateiname; bestehende Datei wird überschrieben |
| `-h`, `--help` | – | Hilfe und Beenden |

```bash
python3 myrun_dump.py --address BLE_ADRESSE --output neuer_diagnosebericht.txt
```

Kein eigener START/STOP, aber FTMS-Init und Setup. Fester Ablauf, kein `--duration`, kein `--watch`, keine CSV. Der Bericht enthält Zeitpunkte, Befehlsantworten, HEX und ggf. unvollständige Restdaten. Init-/Setup-Timing ist im Skript festgelegt, nicht per Kommandozeile einstellbar.

## 7. `myrun_renc_watch.py`

Zweck: Kleine Encoderaufzeichnung ohne Initialisierung und Motorbefehle. [Quelltext](../myrun_renc_watch.py).

| Option | Standard | Wirkung |
|---|---|---|
| `--address ADRESSE` | keine | Adresse, ggf. Namensfallback |
| `--name TEXT` | `MyRun` | Namenssuche |
| `--duration SEK` | `60` | Beobachtungsfenster; Timer beginnt vor dem BLE-Verbindungsaufbau |
| `--interval SEK` | `0.5` | Pause nach Abfrage, zusätzlich zur BLE-Laufzeit |
| `--byte-delay SEK` | `0.04` | Pause zwischen Befehlsbytes |
| `--cmd BEFEHL` | keiner | Exakt `@STATUS#`, `@DUMPIO#` oder `@RPWM#`, zusätzlich nach jedem fünften RENC-Zyklus |
| `--output DATEI` | `myrun_renc_watch_YYYYMMDD_HHMMSS.csv` | CSV, bestehende Datei wird überschrieben |
| `-h`, `--help` | – | Hilfe und Beenden |

```bash
python3 myrun_renc_watch.py --address BLE_ADRESSE --duration 60 --interval 0.5 --cmd "@STATUS#" --output neuer_encoderverlauf.csv
```

Exakter CSV-Header: **`t_rel_s,wallclock,enc_hz,enc_kmh,raw`**. Die Zusatzbefehle erzeugen Zeilen mit leeren Encoderfeldern. In Rohtexten werden Zeilenumbrüche ersetzt und Kommas in Semikolons geändert; keine identische CSV-Implementierung wie im Fast-Monitor. Kein zusätzlicher TXT-Bericht. Manuelle Bandbewegung kann im Standby einen GIRT-Fehler auslösen; das Beispiel enthält keine Aufforderung dazu.

## 8. Grenzen und Datenschutz

Die Beispiele bleiben bei expliziten Fahrprofilen auf **0,8–2,9 km/h** und **0–5 %**; einzelne Skripte haben engere Neigungsbereiche. Die berichteten historischen 9-/12-km/h-Läufe sind keine Erweiterung dieser Entwurfsgrenzen. Ein START kann ohne explizite Geschwindigkeit bereits Bewegung auslösen. Quittierung ist kein Beleg tatsächlicher Bewegung, und STOP kann scheitern.

Bei passiven Konsolenstarts bleibt die mechanische Verantwortung am Gerät. Alle Skripte sind BLE-Werkzeuge, keine Anleitung für Oszilloskopmessungen an Netzpotenzial. Es wurden für diese Dokumentation keine Verbindung zu einem Laufband und kein Bewegungsbefehl ausgeführt.

Bestehende Programme schreiben teilweise Geräteadresse/-name, Serienkennungen aus Antworten, GATT-Daten und lokale Zeitstempel in Reports; am Ende können lokale Ausgabepfade erscheinen. **Rohreports daher nicht ungeprüft öffentlich hochladen.** Auch Skriptvorgaben enthalten gerätebezogene Adressen. Hier wurden diese Kennungen nicht übernommen. Eine spätere Veröffentlichung sollte eine separate redigierte Kopie verwenden und die unveränderten Messbelege erhalten; in diesem Branch werden keine vorhandenen Dateien umgeschrieben und keine Fotos hochgeladen.

## 9. Aufräumvorschläge – nicht umgesetzt

| Vorschlag | Nutzen / unverändert zu erhaltendes Verhalten |
|---|---|
| Gemeinsame Konstanten für UUIDs, Encoder-/Statusparser und FTMS-Payloads | Weniger Duplikate. Bytes, Rundung, Ausgabeschlüssel und Ergebnisprüfung zunächst exakt erhalten. |
| Gemeinsamer Textkanal-Transport mit expliziter Timing-Konfiguration | Mehrere Receiver unterscheiden sich bei Teilantworten, `!…:ERROR`, Queue-Reset und Timeout-Rückgaben. Diese Unterschiede vor Auslagerung mit aufgezeichneten Frames prüfen, nicht unbemerkt vereinheitlichen. |
| Getrennte Sitzungsmodi: nur Abos, Lesepolling, Setup ohne START, aktiver Lauf | Verhindert, dass ein Refactor passive Modi versehentlich initialisiert. Kein automatisches Zusammenlegen von `--no-start` und Listen-Modi. |
| Gemeinsames Logging / optionale öffentliche Exportkopie | UTC-/Monotonie-Felder und CSV-Formate sind derzeit verschieden. Alte Formate und Rohdaten erhalten; eine Redaktionsfunktion wäre separat zu entwerfen. |
| Einheitliche Hilfe und Argumentvalidierung | Gleiche Einheitendarstellung; pro Skript unterstützte Optionen ausdrücklich angeben. Eine neue Option, andere Standardadresse oder neue Bereichssperre ist eine bewusste Verhaltensänderung, kein stiller Dokumentationsfix. |
| Statische Totcode-Kandidaten prüfen | `POLL_READ` im Fast-Monitor wird nur definiert; `fields()` im Fault-Monitor hat keinen lokalen Aufrufer; `time` im Dump wird nicht als Importname benutzt; das `disconnected`-Event im Incline-Test wird gesetzt, aber nicht abgefragt. Vor Entfernung externe Importe/Seiteneffekte prüfen. Keine dieser Stellen wurde gelöscht. |
| Weniger unklare Dateirollen | Fast-Monitor für neue Vergleiche bevorzugt dokumentieren, Fault-Monitor als eigene ältere Implementierung erhalten; keine ersatzlose Löschung oder Umbenennung. |

Besonders zu trennen sind echte Sicherheitsänderungen: zusätzliche START-Zustandsprüfungen, Abbruch nach fehlendem START-ACK, andere Cleanup-/STOP-Reihenfolge oder kürzere Timeouts würden Verhalten ändern. Dafür wären ein gesonderter Code-Commit, Tests und ausdrückliche Bewertung nötig.

Für einen späteren reinen Refactor eignen sich Hardware-freie Prüfungen: zerstückelte/verkettete Textframes, ERROR ohne Abschlusszeichen, Timeouts mit Restdaten, ACK-Zuordnung, Datenparser, Profilgrenzen und nachgewiesen kein Init/START in passiven Modi. Ein Syntaxcheck allein prüft diese Eigenschaften nicht. In diesem Entwurf bleibt der Code bytegleich; es gibt keinen Code-Änderungscommit.

## 10. Prüfung dieses Entwurfs

Alle **45 ausdrücklich definierten Kommandozeilenoptionen** wurden per AST den jeweiligen Dokumentationsabschnitten zugeordnet; automatische `-h`/`--help`-Optionen sind zusätzlich beschrieben. `--help` wurde bei allen sechs Programmen erfolgreich ausgeführt, ebenso `python -m py_compile` für alle sechs Dateien. Es wurde keine BLE-Geräteverbindung aufgebaut und kein START gesendet. Syntax-/Hilfetests belegen keine elektrische Sicherheit oder Hardwarefunktion. Programmdateien und bestehende Daten bleiben unverändert.
