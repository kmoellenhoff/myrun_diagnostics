# Fehlercodes – Beobachtungen und Vergleichshypothesen

Stand 27.11.2026, nach der Reparatur (Ursache: defekter Kondensator C602 im Netzspannungs-Messzweig, siehe [REPARATUR.md](REPARATUR.md)). Hardware-Hintergrund: [HARDWARE.md](HARDWARE.md).

Diese Übersicht trennt vier Ebenen: **HF-Nummer der Konsole**, **numerische err-Anzeige**, **STS2-Blinkmuster auf der GIRT** und **Protokollantworten über BLE**. Gleiche Ziffern auf unterschiedlichen Ebenen sind nicht automatisch derselbe Fehler. Eine vollständige Hersteller-Codetabelle für die untersuchte GIRT S6T30 liegt nicht vor; die Firmware ist nicht dokumentiert.

Belegstufen: **M** elektrische Messung, **O** Beobachtung (Anzeige, Foto, Video, BLE-Log), **I** Ableitung, **H** Hypothese. **Jede Übertragung von einem anderen Technogym-Laufband oder einer anderen Treibergeneration ist H**, auch wenn sie in Handbüchern steht. Aus einer elektrischen Messung wird kein unbekannter Firmwarecode abgeleitet. Die Rohprotokolle der Einzelläufe liegen im Branch `archiv-vor-aufraeumen-2026-11-27`.

Hinweis zur Zeit: Die Gerätezeit im Fehlerspeicher entspricht ungefähr UTC, im Winter liegt sie also eine Stunde hinter der Ortszeit zurück (Zeitstempel im Fehlerspeicher nicht mit Ortszeit-Notizen verwechseln).

## 1. Am untersuchten Gerät beobachtete Meldungen

Der Fehlerspeicher (`@RERRORLOG#`) zeigt die letzten 5 Einträge.

| Ebene / Code | Beobachtung | Einordnung |
|---|---|---|
| Konsole **HF904 / 904** | Wiederholter Fehlstart: Konsole fordert PWM an, Encoder und `MeasSpeed` bleiben 0, DC MOTOR bleibt auf 0 V, später `QSHardwareFault` und neuer Eintrag 904. Der Motor bekommt keine Spannung. | Start ohne Drehzahl, Motor nicht in Bewegung gesetzt **I**. Der Code allein beweist weder fehlende Gate-PWM noch deren Ursache. In der zitierten älteren MyRun-Ausgabe ist HF904 nicht definiert. |
| Konsole **HF902 / 902** | Abbruch im Lauf, u. a. kurze Läufe mit err 4 bzw. err 9 (10.11.); ein Eintrag auch ohne START im Standby (19.11.). | Abbruch während oder ohne Motorlauf; keine feste Gleichsetzung mit „Fehler nur im Lauf“ **I**. Genaue Firmwaredefinition unbekannt. |
| Konsole **HF901 / 901** | Fehler im Wartezustand (`QSWaitForStart901`), z. B. wenn das Band im Stillstand von Hand bewegt wird; am 14.11. und 23.11. reproduziert. | Plausibilitätsprüfung der Drehzahl im Stillstand **I**; **kein** Hinweis auf einen defekten Sensor. Reproduzierbar auch am reparierten Gerät, weil durch die Handbewegung ausgelöst. |
| Konsole **HF900** | In früheren Notizen als gesehen genannt, Einzelbeleg mit Datum nicht gesichert. | Das ältere MyRun-Handbuch nennt HF900 im Zusammenhang mit der Geschwindigkeitsrückmeldung (**H**); nicht mit HF904 gleichsetzen. |
| Fehlerspeicher **1001** | Neuer Eintrag nach bewusstem Ziehen des Not-Stopp-Schlüssels (11.11.); FTMS meldet zusätzlich `Stopped by safety key [03]`. | Not-Stopp-Schlüssel gezogen, experimentell gestützt **I**. Nicht „HF1001“ oder „GIRT-Code 1001“ nennen. |
| Fehlerspeicher **1004** | Zwei Einträge bei Hantieren am Schlüssel, Band nicht aktiv. | Schlüssel im Stillstand getrennt bzw. wackelnder Kontakt **H**. |
| Anzeige **err 4**, **STS2 4×** | Zusammen mit HF902 nach ca. 1 s Bandlauf (10.11.); Blinkzahl und Anzeige passten zusammen. | Zusammenpassen von Anzeige und Blinkzahl **O**. Deutung 04 = Überspannung (OU) bleibt **H**; aus dem Code folgt keine gemessene Überspannung. |
| **STS2 8×** („Code 08“) | Beim Fehlstart (HF904, Eintrag 904) und bei Handbewegung im Standby; erster Impuls ≤ 1,5 s bis ≈ 5 s nach START. | Zahl 8 beobachtet **O**; Lesart „Treibercode 08“ **I**; fremde Definition 08 = Bandmotor-Encoderfehler **H**. Kann Folge ausbleibenden Antriebs oder eines Plausibilitätskonflikts sein, nicht zwingend ein Sensordefekt. |
| Anzeige **err 9**, **STS2 9×** | err-9-Abbrüche am 10.11. (Blinkzahl und Anzeige passten zusammen), 11.11. und 19.11. | Vergleich 09 = Motor-Thermoschalter (OtM) **H**. Der Thermoschalter war stromlos ≈ 0 Ω, also kein Defekt nachgewiesen; die Enable-Kette kann auch anders unterbrochen worden sein. |
| **STS2 dunkel** | Auch Fehlstarts ohne beobachteten STS2-Code kamen vor. | Dunkle STS2 beweist keine Motorfreigabe. |

Blinkzeiten und Zeitverlauf der LED: [HARDWARE.md, Abschnitt 6](HARDWARE.md#6-leds-rückseite-der-platine-zwischen-d3-und-q2). Beobachtete Blinkcodes im Detail:

| Datum / Lauf | Impulse pro Gruppe | Gruppenperiode | Fehlerspeicher | Erster Impuls nach START |
|---|---|---|---|---|
| 07.11. 17:30 und 22:04 | 8 | 5,33 s | 904 | ≤ 1,5 s |
| 08.11. 13:26 | 4 | 3,33 s (Pause 1,53 s) | 902 | ≈ 5 s |

Im Lauf vom 08.11. kam der erste STS2-Impuls etwa 1,3 s *vor* dem Abfall der Freigabeleitungen der Konsole: Die GIRT bemerkt den Fehler vor der Konsole **[O]**.

## 2. Wie sich der C602-Defekt in den Codes zeigte

Der Kondensator C602 (ca. 470 pF) am Knoten J der Netzerfassung hatte einen inneren Nebenschluss. Dadurch brach das Netzspannungs-Messsignal wärmeabhängig ein (J von normal ≈ 4,9 V auf 0,1–0,9 V) **[M]**. Die Steuerung wertete das vermutlich als fehlerhafte Netzversorgung und verweigerte oder beendete den Motorbetrieb **[I]**; die Firmware ist nicht dokumentiert, daher ist die Verknüpfung mit einzelnen Codes nicht bewiesen. Die Erscheinungsformen passten dazu:

- **HF904 / STS2 8×:** Start wurde verweigert, Motor blieb bei 0 V, Relaisklicken. Das Messsignal war beim Start eingebrochen.
- **HF902 / 902:** Abbruch im Lauf, auch kurz nach Start, und ein Eintrag im Standby ohne START. Ein zufällig einbrechendes Messsignal kann auch im Stillstand auslösen.
- **STS2 4×, err 4 und STS2 9×, err 9:** Die Blinkzahl hing vermutlich vom Zeitpunkt des Einbruchs bzw. der Reaktion der Steuerung ab **[H]**. Dass „Überspannung“ oder „Thermoschalter“ vorlagen, ist nicht belegt.
- **Wärmeabhängigkeit:** Der Einbruch von J war wärmeabhängig: Im Föhntest am alten Aufbau sank J erst linear und sprang dann ein **[M]**. Ob die Fehlstarts im Betrieb ebenfalls von der Temperatur abhingen, ist nicht untersucht.

Nach dem Ersatz von C602 (23.11.): J 4,966 V konstant, auch unter Wärme; Läufe bis 20 km/h bzw. 6,6 km/h bei 12 % Steigung sowie mehrere Trainings ohne Fehler (Stand 27.11.) **[M/O]**. HF901 lässt sich weiter durch Handbewegung des Bandes im Stillstand auslösen und ist kein Defekt. Die Einträge 1001 und 1004 hängen mit dem Not-Stopp-Schlüssel zusammen und haben mit C602 nichts zu tun.

Der Ausfall am 24.11. während der Höhenverstellung hatte eine andere Ursache: ein lockerer Kaltgerätestecker (Knistern/Funken). Nach festem Stecken lief die Höhenverstellung ohne Fehler.

## 3. Vergleich mit anderen Technogym-Treibern – ausschließlich H

Die Bezeichnungen stammen aus Handbüchern anderer oder älterer Antriebe (siehe [HARDWARE.md, Abschnitt 10](HARDWARE.md#10-quellen)), die dort mit demselben Nummernschema über vier Antriebsgenerationen auftauchen. Nicht beobachtete Codes werden hier nicht als auf dieser GIRT aufgetreten dargestellt.

| Vergleichscode | Bezeichnung / Bedeutung im fremden Handbuch | Beobachtung an dieser GIRT | Status |
|---|---|---|---|
| 01 | OH, Übertemperatur | kein Beleg | **H** |
| 02 | OC, Überstrom | kein Beleg | **H** |
| 03 | UU, Unterspannung | kein Beleg | **H** |
| 04 | OU, Überspannung (DC-Zwischenkreis) | err 4 / 4× beobachtet, Bedeutung nicht bestätigt | **H** |
| 05 | ST, serieller Timeout | kein Beleg | **H** |
| 06 | PE, EEPROM-/Parameterfehler | kein Beleg | **H** |
| 07 | EdC1, Encoder der Höhenverstellung | kein Beleg | **H** |
| 08 | Encoderfehler Bandmotor | 8× beobachtet, Bedeutung nicht bestätigt | **H** |
| 09 | OtM, Motor-Thermoschalter | err 9 / 9× beobachtet, Bedeutung nicht bestätigt | **H** |
| 10 | Oli | kein Beleg | **H** |
| 11 | OLm | kein Beleg | **H** |
| 12 | OLr | kein Beleg | **H** |
| HF500–HF505 | älterer MyRun: Fehlerfamilie des Unterteils | kein Beleg | **H** |
| HF600 | älterer MyRun: Fehler des Höhenmotors | kein Beleg | **H** |

„Über-/Unterspannung“ in der fremden Antriebstabelle ist **keine direkte Anzeige der gemessenen Netz- oder Motorspannung**. Welchen Eingang und welche Schwellen die GIRT-Firmware auswertet, ist unbekannt. Die Netzspannung wird über den Knoten J erfasst (siehe [HARDWARE.md, Abschnitt 2.1](HARDWARE.md#21-netzerfassung-b10-und-messsignal-zum-mikrocontroller)); eine Verknüpfung von J mit einem bestimmten Fehlercode bleibt **H**.

## 4. BLE-/Statusmeldungen nicht mit Treibercodes verwechseln

| Meldung | Was belegt ist | Grenze |
|---|---|---|
| FTMS `80 07 04` | START/RESUME abgelehnt; die Skripte deuten Resultat 04 als `OPERATION_FAILED` (siehe [Skript](../myrun_fast_monitor.py)). | **Kein GIRT-err 4**, trotz gleicher Ziffer. |
| FTMS `80 08 04` | STOP/PAUSE abgelehnt, u. a. nach HF904. | Software-STOP ist keine zuverlässige physische Abschaltung. |
| FTMS Machine Status `[03]` | Beim absichtlichen Ziehen des Schlüssels als Safety-Key-Stopp protokolliert. | **Kein Hinweis auf GIRT-Code 03 / Unterspannung.** |
| FTMS `[02 01]` | „Stopped/paused by user“ erscheint auch im Zusammenhang mit Fehlerabläufen. | Die Meldung allein beweist keinen bewusst gedrückten STOP. |
| `@STATUS# Info:...` | Unterschiedliche Werte bei Fehlern und normalem Stopp, z. B. `000008`, `000055`, `000254`, `000016`. | Keine bestätigte Gleichsetzung mit STS2-/GIRT-Code. |
| `TIMEOUT`, `!CMD:ERROR`, blockierter Probe-Befehl | Antwortstatus der Diagnoseprogramme (siehe [Probe](../myrun_probe.py)). | Kein gemeldeter Hardwarefehler. |

## 5. Quellen und offene Punkte

Im Repository verlinkt ist das [MyRun Technical Service Manual, Rev. 2.2, französisch, November 2016](https://manuals.plus/m/077b22630fbae70ec842c1934cbd88c864a0677a4bc4fdc5807af41d91ae321d.pdf) (gedruckte Seiten 40–54 sowie 85–88; Auswertung im [Root-README](../README.md#myrun-technical-service-manual-and-diagnostic-cross-check)). Die dortige Unterteil-Generation entspricht nicht sicher der untersuchten GIRT; HF901/HF904 sind in dieser Ausgabe nicht definiert. Weitere Handbücher (Excite Run 500/700/900 Rev. 1.3, Run Personal + Unity Rev. 4.1, Jog Now Excite+ 700, Skillrun Unity 7000 Guide Rev. 6.0, WEG TPD500) sind in [HARDWARE.md, Abschnitt 10](HARDWARE.md#10-quellen) genannt; für die einzelne Codezuordnung gibt es dort keine Seitenverweise.

Offen bleibt:

1. Eine Originaltabelle für genau die GIRT S6T30 und ihre Firmware (HF901/902/904, STS2-Kodierung).
2. Handbuchausgabe und Seite je Vergleichscode; OLi/OLm/OLr erst nach Quellenprüfung ausschreiben.
3. Ein datierter Einzelbeleg für HF900.
4. Die genaue zeitliche Reihenfolge von STS2, Enable, Motor, Encoder und J aus synchronen Aufnahmen (nacheinander abgefragte BLE-Werte sind nicht gleichzeitig).
5. Ob alle historischen Codes tatsächlich auf C602 zurückgehen: Nachgewiesen ist, dass nach dem Ersatz keine Fehlstarts und Abbrüche mehr auftraten; welcher Code im Einzelfall welchen Mechanismus anzeigte, bleibt Hypothese.
