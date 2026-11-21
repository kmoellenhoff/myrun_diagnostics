# Prüfung und Aktualisierung des Schaltplans, 21.11.2026

## Korrektur nach Nutzerangaben (21.11., 14:50–14:53)

Die ursprüngliche Fassung dieser Prüfung (Commit 7c8285a) enthielt Fehler, die hier korrigiert sind. Die Fakten stammen vom Nutzer und sind nicht erweitert.

1. **B10-Umbau, Reihenfolge:** Je Seite (L und N) steht eine Kette aus neuen Teilen **Faston-Pad – 470 kΩ (4703) – 470 kΩ (4703) – US1M – J** (gemeinsame Lötbrücke „2212/1001“). Der Diodenstrich (Kathode) liegt am J-Ende, die Anode am Widerstandsende. Das ist die Reihenfolge der Originalschaltung, nur mit neuen Teilen. Die neuen Teile sitzen auf den alten Pads; die Verbindungen sind zusätzlich mit Litzen überbrückt. Litzen sind zusätzliche Brücken über dieselben Knoten, **keine Parallelzweige**; es gibt keinen elektrisch parallelen alten Zweig. Die frühere Darstellung (Faston → US1M → R → R → J, Diode am Faston) war falsch. Die Reihenfolge folgt der ausdrücklichen Nutzerkorrektur. Die Gesamtmessung von ca. 940 kΩ pro Seite und die positive J-Spannung stützen den Serienpfad und die Gleichrichtung, beweisen aber nicht, an welcher Position innerhalb der Serie die Diode sitzt. Der Wärmetest und der Profil-Lauf liefen bereits mit diesem Aufbau (neue Teile plus Zusatzlitzen). Netze: Faston L/N = R1.1; R1.2 = R2.1; R2.2 = Anode; Kathode = J (`B10_KATHODEN`).
2. **TL082-Pinzählung geklärt:** Die vom Nutzer am 21.11. genannten Pinnummern waren um 180° gedreht gezählt (echt = 9 − genannt). Siehe Abschnitt „Widersprüche“, Punkt 1.
3. **C602, Bewertung:** Ein niederohmiger Nebenschluss ist mit dem Einbruch vereinbar. Die Rechnung allein unterscheidet einen internen Isolationsfehler des Kondensators nicht von einer externen Brücke; die Zahlen wurden mit einem Thevenin-Modell präzisiert (Abschnitt „Funktion von C602“).
4. **Offene Lücke:** Zwei 1-Minuten-Läufe bei 9 und 12 km/h (Nutzer, nach 13:37) sind nicht dokumentiert (Details in `LAUF_2026-11-21.md`).
5. **Neuaufbau erledigt:** Nach Übernahme der Nutzerkorrekturen aus `d11d0b2` wurden beide KiCad-Dateien und ihre PDF-/SVG-/XML-Exporte neu erzeugt. Die Netzprüfungen und Medienprüfung wurden gegen diesen korrigierten Stand wiederholt. Pin 6 und Pin 7 des TL082 sind nun auch im nativen Symbol enthalten, ohne behauptete Verbindung zwischen ihnen.

Quellenstand `d11d0b216334c2af546306586f4df1c6df6b13a6`; vorhandener KiCad-Plan, Netzlisten, Schlusskorrekturen bis 16.11., Protokolle vom 17.–21.11. und Originalfotos des Umbaus. Keine neuen Messungen. Belegstufen M/F/I wie im Repository; Fehlerursachen bleiben Hypothesen.

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

Im vereinfachten Modell mit unveränderter Einspeisung und ursprünglich J = 4,9 V ergibt sich aus Rth = 22,1 kΩ ∥ 940 kΩ ≈ 21,6 kΩ ein zusätzlicher Parallelwiderstand Rzus = Rth · Jniedrig / (4,9 V − Jniedrig). Für 0,1 V sind das ca. **0,45 kΩ**, für 0,9 V ca. **4,9 kΩ**; ca. 1 kΩ passt eher zu J ≈ 0,2 V. Das sind Modellwerte, keine Widerstandsmessungen. Ein solcher niederohmiger Nebenschluss kann durch eine interne temperaturabhängige Isolationsstörung von C602 oder einen leitenden Pfad im Anschlussumfeld entstehen. Die Rechnung beweist weder eine Metallbrücke noch einen harten 0-Ω-Kurzschluss. Gewöhnlicher kleiner Isolationsleckstrom wäre zu gering; ein stark erhöhter Leckstrom ist als Mechanismus nicht ausgeschlossen. Kalte Kapazitätsmessung allein schließt eine Isolationsstörung nicht aus. Wärmeeinbruch mit C, ausbleibender Einbruch nach Entfernen und anschließender erfolgreicher Lauf sprechen für C oder dessen bearbeitetes Anschlussumfeld. Ein ausgebauter, temperaturabhängiger Nebenschluss wurde noch nicht gemessen; kein entsprechender Einzelwiderstand wird eingezeichnet.

Ohne C ist das Signal weniger gegen schnelle Störungen gefiltert. Daraus folgt **keine garantierte Schutzabschaltung** der MCU: Fehlmessungen, Fehlabschaltungen oder andere Auswertungsfehler sind möglich; Firmware-Filterung und Schwellwerte sind unbekannt. Der endgültige Aufbau soll wieder einen geeigneten Ersatz enthalten.

## Widersprüche und weiterhin fehlende Verbindungen

1. **TL082-Pinzählung am 21.11. geklärt:** Laut Nutzerkorrektur entspricht die am 21.11. genannte 6 der echten 3, die genannte 5 der echten 4 (angegebene Umrechnung: echt = 9 − genannt). Damit bleibt 1001 → Pin 3 richtig. Pin 4 ist V−, Pin 8 V+, Pin 5 IN+ B, Pin 6 IN− B und Pin 7 OUT B. Ein Kondensatoranschluss mit 0 Ω zu Pin 4 ist für einen Abblockkondensator gegen 0VA plausibel. Nur Pin 4 selbst mit 0 Ω gegen 0VA wäre ein Widerspruch zu den bisherigen ±12VA-Messungen. Der braune Kondensator wird mangels eindeutiger Anschlusswiederholung noch nicht neu modelliert. Pin 6 und Pin 7 sind im nativen TL082-Symbol vorhanden, ihre Fortsetzungen aber nicht bestätigt. NOV21-015 (mögliche Verbindung 6/7) bleibt H, kein Kupfer und keine Aussage, die echten Pins seien unbeschaltet.
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
- Ergänzte Prüfung ohne Import des Generators: C602 liegt an J/0VA und ist von C601/X sowie Y getrennt; DNP in beiden Dateien; korrigierte Reihenfolge Faston – 470 kΩ – 470 kΩ – US1M – J mit Kathode an J; tatsächliche Ersatzteilwerte; keine zusätzlichen alten Zweige im Ist-Blatt. Pin 6/7 des TL082 werden nicht mit anderen Pins vereinigt.
- Bestehende Prüfungen für Serienwiderstände, TL082-Rückkopplung, MCU-Arbeitsnummern und getrennte Versorgungs-/Massebereiche bleiben erhalten.
- PDFs visuell auf Anschlussführung, lesbare Beschriftung und Bestückungskennzeichnung geprüft. Original-/Referenzmedien gegen den Quellenstand bytegleich geprüft.

Die Prüfnachweise bestätigen Datei- und Belegkonsistenz, keine elektrische Funktionsprüfung und keinen endgültigen Defektnachweis.
