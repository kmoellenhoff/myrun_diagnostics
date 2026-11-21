# Prüfung und Aktualisierung des Schaltplans, 21.11.2026

Quellenstand `89748e932129eaaa9f03a0504eaa5261f45b501d`; vorhandener KiCad-Plan, Netzlisten, Schlusskorrekturen bis 16.11., Protokolle vom 17.–21.11. und Originalfotos des Umbaus. Keine neuen Messungen. Belegstufen M/F/I wie im Repository; Fehlerursachen bleiben Hypothesen.

## Ergänzungen und Korrekturen

| Bereich | Änderung / Ergebnis |
|---|---|
| Kondensator an J | **C602** neu, parallel zu R601 / „2212“, zwischen J und 0VA. Beide Anschlüsse sind am 21.11. als niederohmig zugeordnet. Ausgebaut kalt **0,43 nF** gemessen; ca. **470 pF** als Nennwertkandidat, Originalwert und Dielektrikum nicht abgelesen. |
| Aktuelle Bestückung | C602 ist **DNP / ausgebaut**, mit Kreuz und Text gekennzeichnet. Seine ursprüngliche Verbindung bleibt als Rekonstruktion sichtbar. Der erfolgreiche Profil-Lauf ist kein Nachweis für einen bereits eingebauten Ersatz. |
| Ursprüngliches B10 | Hauptblatt weiterhin **rekonstruierte Originalschaltung**: je zwei 475-kΩ-Widerstände vor der Diode. Historische Werte werden nicht durch die Werte der Ersatzteile überschrieben. Originaltyp „M7-Klasse?“ bleibt eine historische Typannahme. |
| Tatsächlicher Umbau | Neues eigenständiges KiCad-/PDF-/SVG-Blatt: Faston N/L → jeweils US1M → 470 kΩ → 470 kΩ → J. Neue CAD-Referenzen D901/D902 und R901–R904. Die alten Zweige werden nicht als zusätzliche Parallelzweige gezeichnet. Das Blatt dokumentiert den Aufbau, es ist keine Freigabe seiner mechanischen Ausführung oder Isolation. |
| LD3N an Y | Die bisher gezeichneten zwei internen Dioden suggerierten eine nicht bestätigte Innenstruktur. Jetzt Anschlussblock mit den weiterhin bestätigten L/O/R-Netzen. Keine Änderung der gemessenen Verbindungen. |
| Datum und Register | Befunde vom 21.11. separat erfasst und im generierten Messregister ergänzt. Hauptblatt, Details, Ist-Blatt und Prüfungen neu erzeugt. Originalfotos und Claudes Raster unverändert. |

## Funktion von C602

C602 **erkennt keine hochfrequenten Spannungsspitzen**. Seine plausible Aufgabe ist, schnelle Störanteile des Netz-Messsignals gegen 0VA abzuleiten. Widerstände und Kondensator bilden einen Tiefpass vor dem TL082-Puffer. 0VA ist dabei das netzbezogene Bezugspotenzial, keine Schutzerdung.

Größenordnung bei 470 pF: Die wirksame Quellimpedanz liegt wegen des 22,1-kΩ-Fußwiderstands bei rund 21–22 kΩ, nicht einfach bei 950 kΩ. Daraus folgen ungefähr **10 µs** Zeitkonstante bzw. **16 kHz** Grenzfrequenz im vereinfachten Kleinsignalmodell. Die Dioden machen die tatsächliche Schaltung zeitabhängig; die Rechnung beschreibt die Größenordnung, keine gemessene Frequenzantwort. Die 100-Hz-Vollwelle wird damit kaum geglättet. Die Hypothese eines großen Glättungskondensators ist durch die letzten Messungen nicht gestützt.

Ein Isolations-/Leckfehler von C602 könnte den hochohmig gespeisten Knoten J stark absenken. Kalte Kapazitätsmessung allein schließt das nicht aus. Wärmeeinbruch mit C, ausbleibender Einbruch nach Entfernen und anschließender erfolgreicher Lauf sprechen für C oder dessen bearbeitetes Anschlussumfeld. **Ein ausgebauter, temperaturabhängiger Leckstrom wurde noch nicht gemessen.** Deshalb wird kein gemessener Leckwiderstand eingezeichnet.

Ohne C ist das Signal weniger gegen schnelle Störungen gefiltert. Daraus folgt **keine garantierte Schutzabschaltung** der MCU: Fehlmessungen, Fehlabschaltungen oder andere Auswertungsfehler sind möglich; Firmware-Filterung und Schwellwerte sind unbekannt. Der endgültige Aufbau soll wieder einen geeigneten Ersatz enthalten.

## Widersprüche und weiterhin fehlende Verbindungen

1. **TL082-Pinzählung am 21.11.:** „1001 → Pin 6“ widerspricht der bisherigen Zuordnung zu Pin 3. Ebenso wäre die neue Aussage „weiterer Kondensator zwischen Pin 5 und 0VA“ bei der bisherigen Zuordnung Pin 5 = 0VA kein sinnvoller Entstörpfad. Die jüngste Zählung ist ausdrücklich offen; eine umgekehrte Zählung ist möglich, aber kein Messbeweis. Bestehende Pin-3-Verbindung wird mit Warnhinweis beibehalten. Keine Umverdrahtung auf Pin 6, kein neuer Kondensator an den unsicheren Pins. Gehäuseorientierung und Versorgungspins 4/8 vor einer solchen Änderung prüfen.
2. **B10-Rückweg / F27:** Leistungskontakte von F27, Vorladewiderstand, Gleichrichter und Netzfilter sind nicht vollständig verfolgt. Ein Relais in einem J-Rückweg ist nicht belegt. Haupt- und Ist-Blatt erfinden keinen solchen Strompfad. 317–319 V am Zwischenkreis entscheiden einen kurzzeitigen Rückwegfehler nicht allein.
3. **Tacho und Konsole:** P4-Sensor liefert Impulse; der Weg über ADM485/OC06 bis zu einem MCU-Eingang ist nicht vollständig dynamisch bestätigt. Die Versorgung und Ruhepegel vom 17.11. werden als Betriebswerte notiert, nicht als neue Kupferverbindungen. 2,4/2,2 V an den Eingängen machen ADM485 allein nicht defekt. Die externe Sensorplatine A/K/C/E und ihre vollständige Versorgung bleiben nicht vollständig modelliert.
4. **Enable/PWM:** OC04/05 haben bekannte Anschlussnetze. Mittelwerte und konsolenseitige Pulse ersetzen keine vollständige Pegel-/Pulsprüfung an der MCU-Seite. `PWM_MOTOR` ist keine Messung der Q2-Gateimpulse; die Aufteilung der Regelung zwischen Konsole und GIRT ist nicht vollständig entschlüsselt.
5. **Q2/PFC-Treiber:** Vollständige T2-Quelle, einige Anschlüsse des „100CA“-Treiberbereichs und dessen sichere Abgrenzung zu einem möglichen PFC-Treiber fehlen. Die Kennzeichnung FAN3100C bleibt Kandidat. Der Nachtrag vom 18.11. beweist keine neue direkte Verbindung von J zu diesem Bereich.
6. **Y/P600 und X-Schutz:** P600-Kontakt2 = +5VA, Kontakt1 zu Y ca. 1 kΩ; Ka/Kb-Aliase weiter offen. Eine zweite Schutzdiode an X ist fotografischer Kandidat. Keine X–Y-Brücke und keine erfundene innere LD3N-Schaltung ergänzen.
7. **Weitere Relais / OptoMOS:** F24, die beiden F25-Relais und F26 sind gezählt, aber ihre Kontakt- und Spulenwege nicht vollständig gemessen. CPC1017N ist ebenfalls noch nicht elektrisch zugeordnet. F27 bleibt das einzige detailliert modellierte mechanische Relais. Insgesamt fünf mechanische Relais, kein Beleg für fünf Motorfreigaben.
8. **Weitere Widerstände und Versorgungen:** R303/R304, R203/R204, Hilfsnetzteil und die vollständige MCU-Versorgung/Masse sind nicht fertig rekonstruiert. Eingezeichnete endliche In-Circuit-Werte werden nicht als identifizierte Einzelbauteile ausgegeben. Die Schlusskorrekturen zu R301/R302 und getrennten Massebereichen bleiben erhalten.

Diese offenen Punkte verhindern einen vollständigen Herstellerschaltplan, nicht die gezielte Ergänzung des bestätigten J-Filters.

## Prüfung

- KiCad-Export beider eigenständigen Dateien nach XML, PDF und SVG; alle modellierten Pinpaare gegen die exportierten Netzgruppen verglichen.
- Ergänzte Prüfung ohne Import des Generators: C602 liegt an J/0VA und ist von C601/X sowie Y getrennt; DNP in beiden Dateien; richtige Reihenfolge und Werte der Ersatzketten; keine alten B10-Zweige im Ist-Blatt und keine Ersatzketten im Originalblatt.
- Bestehende Prüfungen für Serienwiderstände, TL082-Rückkopplung, MCU-Arbeitsnummern und getrennte Versorgungs-/Massebereiche bleiben erhalten.
- PDFs visuell auf Anschlussführung, lesbare Beschriftung und Bestückungskennzeichnung geprüft. Original-/Referenzmedien gegen den Quellenstand bytegleich geprüft.

Die Prüfnachweise bestätigen Datei- und Belegkonsistenz, keine elektrische Funktionsprüfung und keinen endgültigen Defektnachweis.
