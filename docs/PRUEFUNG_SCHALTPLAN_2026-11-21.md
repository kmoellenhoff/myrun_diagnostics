# Prüfung und Aktualisierung des Schaltplans, 21.11.2026

## Korrektur nach Nutzerangaben (21.11., 14:50–14:53)

Die ursprüngliche Fassung dieser Prüfung (Commit 7c8285a) enthielt Fehler, die hier korrigiert sind. Die Fakten stammen vom Nutzer und sind nicht erweitert.

1. **B10-Umbau, Reihenfolge:** Je Seite (L und N) steht eine Kette aus neuen Teilen **Faston-Pad – 470 kΩ (4703) – 470 kΩ (4703) – US1M – J** (gemeinsame Lötbrücke „2212/1001“). Der Diodenstrich (Kathode) liegt am J-Ende, die Anode am Widerstandsende. Das ist die Reihenfolge der Originalschaltung, nur mit neuen Teilen. Die neuen Teile sitzen auf den alten Pads; die Verbindungen sind zusätzlich mit Litzen überbrückt. Litzen sind zusätzliche Brücken über dieselben Knoten, **keine Parallelzweige**; es gibt keinen elektrisch parallelen alten Zweig. Die frühere Darstellung (Faston → US1M → R → R → J, Diode am Faston) war falsch. Belege: ca. 940 kΩ pro Seite (rot Faston, schwarz J; umgekehrt OL) [M] = zwei Widerstände in Reihe; J war gegen 0VA positiv (4,9 V) [M], also Kathode an J. Der Wärmetest und der Profil-Lauf liefen bereits mit diesem Aufbau (neue Teile plus Zusatzlitzen). Netze: Faston L/N = R1.1; R1.2 = R2.1; R2.2 = Anode; Kathode = J (`B10_KATHODEN`).
2. **TL082-Pinzählung geklärt:** Die vom Nutzer am 21.11. genannten Pinnummern waren um 180° gedreht gezählt (echt = 9 − genannt). Siehe Abschnitt „Widersprüche“, Punkt 1.
3. **C602, Bewertung:** Der Einbruch von J ist ein Nebenschluss, kein gewöhnlicher Leckstrom (Abschnitt „Funktion von C602“).
4. **Offene Lücke:** Zwei 1-Minuten-Läufe bei 9 und 12 km/h (Nutzer, nach 13:37) sind nicht dokumentiert (Details in `LAUF_2026-11-21.md`).
5. **Neuaufbau OFFEN:** KiCad CLI, PyMuPDF und ReportLab standen bei der Korrektur nicht zur Verfügung. CSV, JSON, `B10_Umbau_2026-11-21.kicad_sch` und die Generator-/Prüfskript-Erwartungen sind korrigiert. Die erzeugten `b10_umbau_2026-11-21.pdf/.svg/.xml`, `gesamtschaltplan.pdf/.svg/.xml`, `uebersicht_A1.pdf` sowie `pruefnachweis.json` und `unabhaengige_pruefung.json` zeigen noch den alten, falschen Stand und müssen mit `erzeugen.py` und `pruefen_unabhaengig.py` neu erzeugt werden. Die unten genannten Prüfungen („KiCad-Export“, „PDFs visuell geprüft“) beziehen sich auf den Stand vor dieser Korrektur.

Quellenstand `89748e932129eaaa9f03a0504eaa5261f45b501d`; vorhandener KiCad-Plan, Netzlisten, Schlusskorrekturen bis 16.11., Protokolle vom 17.–21.11. und Originalfotos des Umbaus. Keine neuen Messungen. Belegstufen M/F/I wie im Repository; Fehlerursachen bleiben Hypothesen.

## Ergänzungen und Korrekturen

| Bereich | Änderung / Ergebnis |
|---|---|
| Kondensator an J | **C602** neu, parallel zu R601 / „2212“, zwischen J und 0VA. Beide Anschlüsse sind am 21.11. als niederohmig zugeordnet. Ausgebaut kalt **0,43 nF** gemessen; ca. **470 pF** als Nennwertkandidat, Originalwert und Dielektrikum nicht abgelesen. |
| Aktuelle Bestückung | C602 ist **DNP / ausgebaut**, mit Kreuz und Text gekennzeichnet. Seine ursprüngliche Verbindung bleibt als Rekonstruktion sichtbar. Der erfolgreiche Profil-Lauf ist kein Nachweis für einen bereits eingebauten Ersatz. |
| Ursprüngliches B10 | Hauptblatt weiterhin **rekonstruierte Originalschaltung**: je zwei 475-kΩ-Widerstände vor der Diode. Historische Werte werden nicht durch die Werte der Ersatzteile überschrieben. Originaltyp „M7-Klasse?“ bleibt eine historische Typannahme. |
| Tatsächlicher Umbau | Neues eigenständiges KiCad-/PDF-/SVG-Blatt: Faston N/L → jeweils 470 kΩ → 470 kΩ → US1M → J (Kathode an J; Reihenfolge der Originalschaltung mit neuen Teilen, korrigiert am 21.11. 14:50). Neue CAD-Referenzen R901–R904 und D901/D902. Es gibt keinen parallelen alten Zweig; die Zusatzlitzen überbrücken nur dieselben Knoten. Das Blatt dokumentiert den Aufbau, es ist keine Freigabe seiner mechanischen Ausführung oder Isolation. |
| LD3N an Y | Die bisher gezeichneten zwei internen Dioden suggerierten eine nicht bestätigte Innenstruktur. Jetzt Anschlussblock mit den weiterhin bestätigten L/O/R-Netzen. Keine Änderung der gemessenen Verbindungen. |
| Datum und Register | Befunde vom 21.11. separat erfasst und im generierten Messregister ergänzt. Hauptblatt, Details, Ist-Blatt und Prüfungen neu erzeugt. Originalfotos und Claudes Raster unverändert. |

## Funktion von C602

C602 **erkennt keine hochfrequenten Spannungsspitzen**. Seine plausible Aufgabe ist, schnelle Störanteile des Netz-Messsignals gegen 0VA abzuleiten. Widerstände und Kondensator bilden einen Tiefpass vor dem TL082-Puffer. 0VA ist dabei das netzbezogene Bezugspotenzial, keine Schutzerdung.

Größenordnung bei 470 pF: Die wirksame Quellimpedanz liegt wegen des 22,1-kΩ-Fußwiderstands bei rund 21–22 kΩ, nicht einfach bei 950 kΩ. Daraus folgen ungefähr **10 µs** Zeitkonstante bzw. **16 kHz** Grenzfrequenz im vereinfachten Kleinsignalmodell. Die Dioden machen die tatsächliche Schaltung zeitabhängig; die Rechnung beschreibt die Größenordnung, keine gemessene Frequenzantwort. Die 100-Hz-Vollwelle wird damit kaum geglättet. Die Hypothese eines großen Glättungskondensators ist durch die letzten Messungen nicht gestützt.

Der Einbruch von J auf ca. 0,1 V (0,9 V in anderen Phasen) verlangt rechnerisch einen **Nebenschluss** von ca. 0,5 kΩ (bei 0,9 V nach Dreisatz rund 4 kΩ; die Nutzerangabe ca. 1 kΩ weicht davon ab, offen) parallel zu 22,1 kΩ. Das ist ein Kurzschluss bzw. eine Brücke, kein gewöhnlicher Leckstrom. Möglich sind ein **Nebenschluss durch Riss mit Metallbrücke oder durch leitende Verschmutzung am Pad** (Status I). Kalte Kapazitätsmessung allein schließt das nicht aus. Wärmeeinbruch mit C, ausbleibender Einbruch nach Entfernen und anschließender erfolgreicher Lauf sprechen für C oder dessen bearbeitetes Anschlussumfeld. **Ein ausgebauter, temperaturabhängiger Nebenschluss wurde noch nicht gemessen.** Deshalb wird kein gemessener Nebenschlusswiderstand eingezeichnet.

Ohne C ist das Signal weniger gegen schnelle Störungen gefiltert. Daraus folgt **keine garantierte Schutzabschaltung** der MCU: Fehlmessungen, Fehlabschaltungen oder andere Auswertungsfehler sind möglich; Firmware-Filterung und Schwellwerte sind unbekannt. Der endgültige Aufbau soll wieder einen geeigneten Ersatz enthalten.

## Widersprüche und weiterhin fehlende Verbindungen

1. **TL082-Pinzählung am 21.11. (geklärt, Nutzerangabe 14:50–14:53):** Alle am 21.11. genannten Pinnummern waren um 180° gedreht gezählt (echte Pinnummer = 9 − genannte). Der Schaltplan-Pin 3 für 1001 (Eingang A+) ist richtig; der Nutzersatz „1001 hängt an Pin 6“ war gedreht gezählt und bedeutet echten Pin 3. Echte Belegung: 1 OUT A, 2 IN A−, 3 IN A+, 4 V− (−12VA), 5 IN B+, 6 IN B−, 7 OUT B, 8 V+ (+12VA). Der „braune Kondensator“ an genanntem Pin 5 liegt an echtem Pin 4 (−12VA) gegen 0VA: wahrscheinlich Abblockkondensator der Versorgung (Status I), kein Eingangsfilter. Die frühere Messung „0 Ω zu Pin 5, 5 MΩ zu Pin 3“ bleibt als Originalangabe stehen; die Zuordnung ist offen (0 Ω an echtem Pin 4 wäre unplausibel; der Nutzer prüft Pin 4 und Pin 5 gegen Elko-Minus). Pin 6 fehlte in der Netzliste und ist als offener Pin geführt (`N_TL082_6`, kein Netz erfunden); „Pin 6/7 vermutlich verbunden, nicht gemessen“ ist nur Hypothese [H] in NOV21-015, kein Kupfer. Keine Umverdrahtung.
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
- Ergänzte Prüfung ohne Import des Generators: C602 liegt an J/0VA und ist von C601/X sowie Y getrennt; DNP in beiden Dateien; Reihenfolge Faston – 470 kΩ – 470 kΩ – US1M – J (Kathode an J) und Werte der neuen Ketten (Erwartungen am 21.11. korrigiert, Lauf nach Neuaufbau OFFEN); keine alten B10-Zweige im Ist-Blatt und keine neuen Ketten im Originalblatt.
- Bestehende Prüfungen für Serienwiderstände, TL082-Rückkopplung, MCU-Arbeitsnummern und getrennte Versorgungs-/Massebereiche bleiben erhalten.
- PDFs visuell auf Anschlussführung, lesbare Beschriftung und Bestückungskennzeichnung geprüft. Original-/Referenzmedien gegen den Quellenstand bytegleich geprüft.

Die Prüfnachweise bestätigen Datei- und Belegkonsistenz, keine elektrische Funktionsprüfung und keinen endgültigen Defektnachweis.
