# Fehlercodes – Beobachtungen und Vergleichshypothesen

**ENTWURF auf `aufraeumen`, Quellenstand 21.11.2026 (`83da2fb`). Ursache wahrscheinlich C602, Stand: Gegenversuch offen.**

Diese Übersicht trennt vier Ebenen: **HF-Nummer der Konsole**, **numerische err-Anzeige**, **STS2-Blinkmuster auf der GIRT** und **Protokollantworten über BLE**. Gleiche Ziffern auf unterschiedlichen Ebenen sind nicht automatisch derselbe Fehler. Eine vollständige Hersteller-Codetabelle für die untersuchte GIRT S6T30 ist im Repository nicht belegt.

Belegstufen: M = elektrische Messung, F = Originalfoto, I = Ableitung, H = Hypothese. Anzeigen und Logereignisse werden als berichtete Beobachtung mit Quelle wiedergegeben. **Jede Übertragung von einem anderen Technogym-Laufband oder einer anderen Treibergeneration ist hier H**, auch wenn ältere Dateien dafür „Man“ verwenden. Aus einer elektrischen Messung wird kein unbekannter Firmwarecode abgeleitet.

## 1. Am untersuchten Gerät protokollierte Meldungen

| Ebene / Code | Beobachtung und Quelle im Repository | Zulässige Einordnung / offener Vergleich |
|---|---|---|
| Konsole **HF900** | In der [Hardware-Zusammenfassung, Abschnitt 5](HARDWARE.md#5-fault-behaviour-summary) als gesehen genannt; ein gleichwertiger datierter Einzelablauf wurde für diesen Entwurf nicht nachgewiesen. | Der ältere MyRun-Serviceleitfaden nennt HF900 im Zusammenhang mit Geschwindigkeitsrückmeldung. Übertragung auf diese Hardware **H**; nicht mit HF904 gleichsetzen. Einzelbeleg noch prüfen. |
| Konsole **HF901 / 901** | Handbewegung des Bandes ohne START am 14.11.; Logzustand `QSWaitForStart901`, neuer Eintrag 901. [Tagesprotokoll](LAUF_2026-11-14.md), [Rohlog](logs_2026-11-14/handtest_sensor_123653.txt). | Zusammenhang mit Fehler im Wartezustand **I**; keine im älteren Manual bestätigte GIRT-Definition. Erklärung als Drehzahl-/Antriebsplausibilität **H**, kein Beweis für einen kaputten Sensor. |
| Konsole **HF902 / 902** | U. a. kurze Läufe mit err 4/9 am 10.11.; am 19.11. auch **ohne START im Standby**. [10.11.](LAUF_2026-11-10.md), [19.11.](LAUF_2026-11-19.md), [Standby-Rohlog](logs_2026-11-19/myrun_fast_monitor_20261119_214052.txt). | Keine feste Gleichsetzung mit „Fehler nur während Motorlauf“. Genaue Firmwaredefinition offen. B10/J als gemeinsamer Auslöser bleibt **H**. |
| Konsole **HF904 / 904** | Wiederholter Fehlstart: Anforderung/PWM-Diagnosewert vorhanden, Encoder und MeasSpeed 0, später `QSHardwareFault` und neuer Eintrag 904. [11.11.](LAUF_2026-11-11.md), [14.11.](LAUF_2026-11-14.md), [Beispiellog](logs_2026-11-14/start_per_skript_125808.txt). | Ableitung „Startanforderung nicht erfolgreich in Bewegung umgesetzt“ **I**. Weder fehlende Gate-PWM noch deren Ursache werden durch HF904 allein bewiesen. HF904 fehlt in der zitierten älteren MyRun-Ausgabe. |
| Fehlerspeicher **1001** | Neuer Eintrag nach bewusstem Ziehen des Sicherheitsschlüssels am 11.11.; FTMS meldet zusätzlich `Stopped by safety key [03]`. [Protokoll](LAUF_2026-11-11.md), [Rohlog](logs_2026-11-11/myrun_fast_monitor_20261111_120215.txt). | Zusammenhang mit Not-Stopp-Schlüssel an diesem Gerät experimentell gestützt, als Zuordnung **I**. Nicht ohne Beleg „HF1001“ oder „GIRT-Code 1001“ nennen. |
| Anzeige **err 4**, **STS2 4×** | Zusammen mit HF902 nach ca. 1 s Bandlauf am 10.11.; weitere 4er-Beobachtungen in der [Hardware-Dokumentation](HARDWARE.md#7-leds-rear-of-the-board-between-d3-and-q2). [10.11.](LAUF_2026-11-10.md). | Dass Anzeige und Blinkzahl in diesem Ereignis zusammenpassen, ist beobachtet. Vergleich **04 = OU / Zwischenkreisüberspannung** bleibt **H**. Keine tatsächlich gemessene Überspannung aus dem Code folgern. |
| **STS2 8×**, als **Code 08** bezeichnet | Beim Fehlstart und bei Handbewegung im Standby; [14.11.](LAUF_2026-11-14.md), [Hardware-Blinkbeobachtungen](HARDWARE.md#7-leds-rear-of-the-board-between-d3-and-q2). | Zahl 8 ist beobachtet; ihre Interpretation als Treibercode 08 ist **I**. Fremde Definition **08 = Bandmotor-Encoderfehler** ist **H**. Die Meldung kann eine Folge ausbleibenden Antriebs oder eines Plausibilitätskonflikts sein (**H**), nicht zwingend Sensordefekt. |
| Anzeige **err 9**, **STS2 9×** | Am 10.11. und err-9-Abbrüche am 11./19.11.; [10.11.](LAUF_2026-11-10.md), [11.11.](LAUF_2026-11-11.md), [19.11.](LAUF_2026-11-19.md). Blinkzahl und err-Anzeige passten im dokumentierten 10.11.-Ereignis zusammen. | Vergleich **09 = OtM / Motor-Thermoschalter** bleibt **H**. Die Enable-Kette kann auch anders unterbrochen werden; ihr Abfall kann Ursache oder Folge sein. Kein durch den Code bewiesener Thermoschalterdefekt. |
| **STS2 dunkel / kein Blinkcode beobachtet** | Auch ein Fehlstart ohne beobachteten STS2-Code ist beschrieben. [11.11.](LAUF_2026-11-11.md), [Bewertung 16.11.](NEUBEWERTUNG_2026-11-16.md). | Dunkle STS2 ist kein Beweis für vorhandene Motorfreigabe. Beobachtungsumfang und Zeitpunkt beachten. |

Die Beobachtungen 4×/err 4 und 9×/err 9 stützen die Blinkzahl-Auswertung für diese Ereignisse (I). Daraus entsteht **keine vollständig bestätigte Codetabelle**. STS1-Bereit-/Laufanzeige ist ebenfalls kein Fehlercode und kein Messersatz für die Leistungsstufe.

## 2. Vergleichstabelle anderer Technogym-Treiber – ausschließlich H

Die folgenden Bezeichnungen stammen aus der bestehenden [Hardware-Quellenzusammenfassung](HARDWARE.md#10-sources) und deren [Code-Liste](HARDWARE.md#5-fault-behaviour-summary). Die dort genannten Handbücher betreffen andere oder ältere Geräte. Nicht belegte Codes werden hier **nicht als auf dieser GIRT aufgetreten** dargestellt.

| Vergleichscode | Im Repository übernommene Bezeichnung / Bedeutung | Beobachtung an dieser GIRT | Übertragungsstatus |
|---|---|---|---|
| 01 | OH, Übertemperatur | Kein eigener Ereignisbeleg gefunden | **H** |
| 02 | OC, Überstrom | Kein eigener Ereignisbeleg gefunden | **H** |
| 03 | UU, Unterspannung | Kein eigener Ereignisbeleg gefunden; Bezug zum Zwischenkreis für diese GIRT nicht verifiziert | **H** |
| 04 | OU, Überspannung; in der Vergleichsauslegung DC-Zwischenkreis | err 4 / 4× beobachtet, Bedeutung nicht bestätigt | **H** |
| 05 | ST, serieller Timeout | Kein eigener Ereignisbeleg gefunden | **H** |
| 06 | PE, EEPROM-/Parameterfehler | Kein eigener Ereignisbeleg gefunden | **H** |
| 07 | EdC1, Encoder der Höhenverstellung | Kein eigener Ereignisbeleg gefunden | **H** |
| 08 | Encoderfehler Bandmotor | 8× beobachtet, Bedeutung nicht herstellerseitig bestätigt | **H** |
| 09 | OtM, Motor-Thermoschalter | err 9 / 9× beobachtet, Bedeutung nicht herstellerseitig bestätigt | **H** |
| 10 | Oli | Kein eigener Ereignisbeleg; genaue Überlastzuordnung noch prüfen | **H** |
| 11 | OLm | Kein eigener Ereignisbeleg; genaue Überlastzuordnung noch prüfen | **H** |
| 12 | OLr | Kein eigener Ereignisbeleg; genaue Überlastzuordnung noch prüfen | **H** |
| HF500–HF505 | Älterer MyRun: Lower-Kit-Fehlerfamilie | Hier kein Einzelbeleg gefunden | **H** |
| HF600 | Älterer MyRun: Höhenmotorfehler | Hier kein Einzelbeleg gefunden | **H** |

„Über-/Unterspannung“ in einer fremden Antriebstabelle ist **keine direkte Anzeige der gemessenen Netzspannung L–N oder der Motorspannung**. Welchen Eingang und welche Schwellen die GIRT-Firmware dafür auswertet, ist unbekannt. J ist als Netz-Messsignal rekonstruiert; seine Verknüpfung mit einem bestimmten Fehlercode ist weiterhin H.

## 3. BLE-/Statusmeldungen nicht mit Treibercodes verwechseln

| Meldung | Was im Repository belegt ist | Grenze |
|---|---|---|
| FTMS `80 07 04` | START/RESUME abgelehnt; Skripte deuten Resultat 04 als `OPERATION_FAILED`. [10.11.](LAUF_2026-11-10.md), [Skript](../myrun_fast_monitor.py). | **Kein GIRT err 4**, trotz derselben Ziffer. |
| FTMS `80 08 04` | STOP/PAUSE abgelehnt, u. a. nach HF904. [Root-README](../README.md#myrun-technical-service-manual-and-diagnostic-cross-check). | Software-STOP ist keine zuverlässige physische Abschaltung. |
| FTMS Machine Status `[03]` | Beim absichtlichen Schlüsselziehen als Safety-Key-Stopp protokolliert. [11.11.](LAUF_2026-11-11.md). | **Kein Nachweis für GIRT-Code 03 / Unterspannung.** |
| FTMS `[02 01]` | „Stopped/paused by user“ wird auch im Kontext von Fehlerabläufen protokolliert. [19.11.-Rohlog](logs_2026-11-19/myrun_fast_monitor_20261119_214052.txt). | Meldung allein beweist keinen bewusst gedrückten STOP. |
| `@STATUS# Info:...` | Unterschiedliche Werte bei Fehlern und normalem Stopp, z. B. `000008`, `000055`, `000254`, `000016`. [14.11.](LAUF_2026-11-14.md), [19.11.-Log](logs_2026-11-19/myrun_fast_monitor_20261119_214052.txt), [21.11.-Log](logs_2026-11-21/myrun_fast_monitor_20261121_133144.txt). | Keine bestätigte Gleichsetzung mit STS2-/GIRT-Code. |
| `TIMEOUT`, `!CMD:ERROR`, blockierter Probe-Befehl | Antwort-/Auswertestatus der Diagnoseprogramme; siehe [Probe](../myrun_probe.py). | Für sich kein gemeldeter Hardwarefehler. |

## 4. Vorhandene Quellen und noch zu prüfen

Im Repository verlinkt ist das [MyRun Technical Service Manual, Rev. 2.2, französisch, November 2016](https://manuals.plus/m/077b22630fbae70ec842c1934cbd88c864a0677a4bc4fdc5807af41d91ae321d.pdf). Die [Quellenauswertung im Root-README](../README.md#myrun-technical-service-manual-and-diagnostic-cross-check) nennt gedruckte Seiten 40–54 sowie 85–88. Die dortige Lower-Kit-Generation entspricht nicht sicher der untersuchten GIRT. HF901/HF904 sind in dieser Ausgabe laut Repo-Auswertung nicht definiert. Der Link wurde für diesen Entwurf aus dem Repository übernommen, nicht neu als passend verifiziert.

Weitere Handbuchnamen sind in [HARDWARE.md, Abschnitt 10](HARDWARE.md#10-sources) aufgeführt: Excite Run 500/700/900 Rev. 1.3, Run Personal + Unity Rev. 4.1, Jog Now Excite+ 700, Skillrun Unity 7000 Guide Rev. 6.0 und WEG TPD500. **Direkte Links und konkrete Seiten für die einzelne Codezuordnung sind dort nicht vorhanden**; daher keine erfundenen URLs oder bestätigten Übertragungen. Eine belastbar verlinkte Forumquelle für die GIRT-Codetabelle wurde im Repository nicht gefunden.

Noch zu prüfen:

1. Originaltabelle für genau GIRT S6T30 und die vorhandene Firmware, insbesondere HF901/902/904 und STS2-Kodierung.
2. Je Vergleichscode Handbuchausgabe, Seitenzahl und tatsächlich passende Treibergeneration; OLi/OLm/OLr ausschreiben erst nach Quellenprüfung.
3. Einzelbeleg und Ablauf für HF900; direkte Anzeige „err 8“ von der Interpretation der acht Blinkimpulse unterscheiden.
4. Zeitliche Reihenfolge STS2, Enable, Motor, Encoder und J aus synchronen Aufnahmen; nacheinander abgefragte BLE-Werte nicht als simultan behandeln.
5. Nach dem geplanten C602-Gegenversuch beobachten, welche Meldungen verschwinden. Auch dann nicht ohne weiteren Beleg alle historischen Codes auf dieselbe Ursache zurückführen.

**Ursache wahrscheinlich C602, Stand: Gegenversuch offen.** Ein leerer/neuer unveränderter Fehlerspeicher während eines einzelnen Testlaufs bestätigt weder eine universelle Codetabelle noch den endgültigen Reparaturerfolg.
