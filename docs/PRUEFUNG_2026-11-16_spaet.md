# Prüfung des Repository-Stands d917aa8 – 16.11.2026

Abgleich der letzten Abendmessungen (bis 22:32) mit Schaltplan, Bewertung und Messplan. Keine neuen elektrischen Messungen. Die Bewertungen unten ersetzen widersprechende frühere Schlussfolgerungen; Original-Rohdaten bleiben erhalten.

## Was sich tatsächlich geändert hat

1. **Meine bisherige Fotozuordnung R1/R2 war falsch.** Gemessen ist jetzt R1b = R2b und R2a = 0VA. R1 ist der Serienwiderstand, R2 der Widerstand nach Masse. Der Generator deaktiviert die widerlegten Foto-Aliase AKT-059/060 ausdrücklich, statt sie zusätzlich zu den neuen Masseverbindungen zu vereinigen. R1a = TL082-Ausgang bleibt Fotozuordnung; N → 100-Ω-Eingang ist im Abendbeleg AKT-067 als Ableitung markiert, nicht als separat gemessene 0-Ω-Verbindung.
2. **J–0VA = 22,14/22,02 kΩ** passt zum 22,1-kΩ-Fußwiderstand. Der frühere Verdacht eines zusätzlichen etwa 10-kΩ-Pfads ist damit aktuell nicht gestützt. Das beweist nicht die Abwesenheit sämtlicher schwacher oder spannungsabhängiger Leckpfade.
3. **Vor X liegt nach dem aktuellen Modell ein 1:2-Teiler.** Damit ist ungefähr 3,7 V Spitze bei 230 V AC im unbelasteten Modell plausibel. Die frühere offene Frage „7,4 V am 5-V-MCU?“ wird hierdurch wesentlich entschärft. Tatsächliche Form, Filterung und Last bleiben zu messen; 3,7 V ist keine harte Sollgrenze.
4. **Y hängt plausibel am Temperaturfühler P600.** P600 Kontakt2 = +5VA ist direkt gemessen; Y–Kontakt1 etwa 1 kΩ. Die 1,883 kΩ nach Masse wurden mit gestecktem Fühler gemessen. Daraus lässt sich kein sicherer diskreter 2,2-kΩ-Widerstand rekonstruieren, solange Versorgungspfad und Parallelwege mitwirken. Y etwa 0,8 V und „wärmer → höher“ sind Erwartungen des beschriebenen Teilermodells, keine Funktionsfreigabe. Auch Y = 0 V würde nicht eindeutig einen offenen Fühler beweisen: Versorgung, Kurzschluss oder ein anderer Lastpfad kommen ebenfalls infrage.
5. **P4 TACHO → ADM485 → OC06 ist jetzt ein konkreter Funktionskandidat.** Sicher ist RO/Pin1 = OC06-Kathode und ADM485-GND = LM2903-GND = P2.7. Die 1,103 kΩ zu Pin7 und 12,94 kΩ zu Pin6 stützen die Tacho-Aufbereitung, sind aber keine vollständig nachverfolgten, isoliert identifizierten Serienbauteile. OC06-Ausgang → MCU ist noch offen. „OC06 ist sicher Tacho, RS-485 ist widerlegt“ geht über die bisherigen Belege hinaus.

Der native Schaltplan wurde neu erzeugt: R1/R2 korrigiert, neue Abendbelege eingebunden und die bestätigten ADM485/OC06-Kupferverbindungen ergänzt. Unbekannte OC06-Ausgangsanschlüsse bleiben offen. P600-Messkopplungen stehen als solche im Register und als Anmerkung; es werden keine 1-kΩ-/2,2-kΩ-Einzelbauteile erfunden. Die alte Zuordnung Ka/Kb zu Kontakt1/2 bleibt offen.

## Bewertung der neuen Tacho-Hypothese

**Störimpulse in der Tacho-Aufbereitung sind jetzt eine sinnvolle, gezielt prüfbare Hypothese.** Sie könnten eine Plausibilitätsabschaltung trotz stehenden Motors erklären. Sie sind noch kein nachgewiesener Fehler und verdrängen Enable/PWM nicht vollständig.

Die folgenden Aussagen im bisherigen Text sind zu stark:

- Ein ADM485-RO-Impuls bei stehendem Band ist zunächst eine **Beobachtung**. Für den Fehlerzusammenhang muss klar sein, dass dieser Ausgang hier tatsächlich Drehzahl überträgt, der Impuls nicht zu einer anderen Funktion gehört, die Mechanik wirklich stillsteht und das Ereignis **vor** dem Fehler auftritt. Auch Versorgung/Empfänger-Freigabe bzw. ein Einschaltübergang können relevant sein.
- Ein kleiner DC-Abstand zwischen ADM485 A/B ist prüfenswert. „Unter 0,3 V = kritisch/defekt“ ist ohne genaue Schaltschwelle, Hysterese, zeitliche Differenzspannung, Gleichtaktbereich und Enable-Zustand keine belastbare Grenze. Ein Multimeter kann die kurzen Störungen gerade übersehen.
- Die korrigierten P2-Werte passen sehr gut zu einem gemeinsamen Rückweg: 10,96 + 6,38 = 17,34 kΩ gegenüber 17,35 kΩ gemessen; 10,96 + 12,47 = 23,43 gegenüber 23,45 kΩ. Das ist **kein Hinweis auf eine zusätzliche niederohmige PWM–Tacho-Brücke**. „Ausschließlich über Masse, jeder direkte Weg ausgeschlossen“ wäre wegen Bestückung, Nichtlinearität und Messgrenzen dennoch zu absolut.
- Code08 und STS1-Zustand unterstützen die zeitliche Einordnung, liefern aber ohne verifizierte Firmwarebeschreibung keine eindeutige interne Fehlerdefinition. Eine Wartezeit von ≤1,5 s allein widerlegt auch keinen Drehzahl-Timeout.

## Was aus der vorherigen Prüfung weiter gilt

- **OC05-Mittelwert ist kein Pulsnachweis:** Bei angenommenen stabilen 5 V am Kollektor entsprechen 4,95 → 4,5–4,3 V C–E ungefähr 0,05 → 0,5–0,7 V mittlerer Emitterspannung. Das kann zu richtigen hohen Pulsen mit kleinem Tastgrad passen, aber auch zu unzureichender Ansteuerung. High/Low, Pulsbreite und Frequenz am Emitter/MCU17/18 prüfen; keine festen MCU-Logikschwellen behaupten, solange der Typ unbekannt ist.
- **Enable am MCU12** ist durch einen früheren LM2903-/LED-Test noch nicht für den aktuellen Fehlstart freigegeben. Pegel und Zeitpunkt des Abfalls zählen.
- **13,5 V sind Treiber-/L4981-Versorgung**, nicht MCU-VDD. +5VA und TL082 ±12VA bleiben eigene Prüfungen.
- **T2-Quelle bleibt offen.** Basis 0,1 mV beweist keinen MCU-Ausgangszustand und schließt einen kurzen Schaltversuch nicht aus.
- **T3 high spricht für starke High-Speisung, nicht für nachgewiesene Firmwareabsicht.** Bei 4,9 V Steuerleitung und 0,7 V Basis fließen rechnerisch etwa 1,9 mA durch 2,21 kΩ; der 10-kΩ-Pull-up von 5 V liefert dabei nur etwa 10 µA. Ein hochohmiger Quellpin allein passt daher nicht zum Modell. Ausgangszustand, unerwünschter Pfad nach +5VA und Grund der Ansteuerung sind dadurch nicht unterschieden.
- **F27-Befehl und Ausführung trennen:** MCU-seitiges Ende des 1-kΩ-Widerstands versus T4-Basis; bei Ansteuerung zusätzlich Kollektor/Spule. Ein hoher Befehl ohne Schaltreaktion lenkt die Suche in die Treiberstufe. Bleibt bereits der Befehl niedrig, ist die Ursache davor oder im Quellzustand zu suchen.

## Gewichtung und Konsequenz

Der statische Verdacht gegen B10/Temperaturpfad wird durch die neuen Daten geringer. B10 ist nun als normaler gepufferter und geteilter Messeingang plausibel. Vorrang haben die **dynamisch noch nicht belegten Signale**: Tacho-Kandidat ADM485/OC06, Enable OC04, PWM OC05 – zusammen mit ihren Versorgungen. Danach F27-Befehl gegen tatsächliche Schaltreaktion abgleichen.

MCU-/EEPROM-Defekt bleibt nachrangig. Mehr flächiges Reinigen, Nachlöten oder breite Widerstandsmatrizen ergeben ohne konkreten neuen Befund derzeit weniger Erkenntnis. Die neue Hypothese kann auch eine Störung in der Signalaufbereitung betreffen, obwohl der Sensor selbst zeitweise funktioniert. Frühere kurze Laufabbrüche und heutige Nichtanläufe müssen nicht dieselbe Ursache haben.

Der [aktuelle Messplan](MESSPLAN_2026-11-14_abend.md) setzt diese Reihenfolge um. Originalfotos, Raster und alte Messwerte bleiben unverändert.
