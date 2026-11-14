# Messplan 14.11. abends – Startfreigabe des MCU

Ziel: herausfinden, welche Bedingung dem MCU für die Startfreigabe fehlt (Kandidaten: `NEUBEWERTUNG_2026-11-14.md`, Abschnitt 5).
Erwartungswerte nur, wo begründet; sonst Werte notieren.

Ergänzung nach Review des Standes `233fefe`: Die ursprünglichen Schritte A1–C5 bleiben erhalten. Vor der Durchführung auch die Präzisierungen und Zusatzschritte unten lesen; sie enthalten insbesondere die Bezugspunkte und Grenzen der Auswertung.

## A – Ausgebaut, stromlos (Elko < 1 V)
| # | Messung | Notieren / Erwartung |
|---|---|---|
| A1 | **J1** (unteres Bein D1, B10) ↔ beide Enden des „01C“ am SOT-23-5 | beide Werte |
| A2 | Beide Testpunkte am SOT-23-5 ↔ **0VA** und ↔ **+5VA** | ≈ 0 Ω zu einem davon = Versorgungspunkt (erklärt 10 kΩ) |
| A3 | Großer Durchsteckanschluss hinter „47R5“ → welches Bauteil auf der Vorderseite (Q1? Gate?) | Bauteil + Anschluss |
| A4 | **Aufdruck SOT-23-5**; jeder Pin ↔ 0VA, +5VA, VDD-Netz (L4981 Pin 19) | Pinrollen |
| A5 | J1 ↔ L4981 Pin 4, 6, 7; J1 ↔ MCU-Pins (alle 32, Auffälligste notieren) | Ziel von J |
| A6 | **OC02, OC03, OC08**: P2.2, P2.3, P2.9, P2.15, P2.17, P2.18 und P4-Tacho ↔ Anode (Pin 1) | kleinster Wert (≈ 1 kΩ wie bei OC05) = Zuordnung |
| A7 | OC01/OC07 Transistorseite ↔ ADM485 Pin 2 (/RE), 3 (DE), 4 (DI) | Zuordnung RS-485 |
| A8 | **Motorfreigabe T2**: Testpad Basis T2 → „01C“ → weiter bis MCU-Pin (wie bei T3), Pull-up/-down zu +5VA/0VA | MCU-Pin-Position (Kante + Nr.) |
| A9 | Testpunkt **P13** → welcher MCU-Pin | Position |
| A10 | Optional: F27 Spulen-Minus → Treibertransistor → dessen Basis → MCU-Pin | Position |
| A11 | Sichtprüfung: dunkle Stellen unter Lack (Foto mit Streiflicht), Faden an rechter unterer MCU-Ecke, Platine reinigen und trocknen lassen | Fotos |

## B – Eingebaut, Standby (klemmen bei entladenem Elko; Bezug Testpunkt 0VA bzw. Elko-Minus)
| # | Messung | Erwartung |
|---|---|---|
| B1 | +5VA, +12VA, −12VA | ≈ 5 V, +12 V, −12 V |
| B2 | P13, P70 (DC, ggf. Hz) | notieren |
| B3 | J1 (DC und Hz) | notieren (Signalform unbekannt) |
| B4 | SOT-23-5 Ein-/Ausgang (nach A4) | notieren |
| B5 | Anoden OC02/03/08 gegen **P2.7** (Konsolenseite, ungefährlich) | an ≈ 1,1 V, aus ≈ 0 V |
| B6 | MCU-Pin der Motorfreigabe (nach A8) | notieren |

## C – Start (je ein Lauf, Skript `--start-delay 20`, MIN/MAX)
Nur Punkte, deren Änderung beim Start etwas aussagt: C1 Anoden OC02/03/08 · C2 P13/P70 · C3 MCU-Pin Motorfreigabe · C4 J1/SOT-23-5 · C5 Versorgungen ±12VA/+5VA (MIN).
Zusätzlich: ein Startversuch an einem anderen Stromkreis ohne weitere Verbraucher.

## Ergänzungen nach Review – 14.11.2026

### Zusätzliche Schritte mit konkretem Diagnoseziel

| # | Messung / Vorbereitung | Auswertung / Grenze |
|---|---|---|
| A12 | **MCU-Versorgung zuordnen:** stromlos einen lokalen Abblockkondensator am MCU identifizieren; Masseanschluss und Verbindung des anderen Anschlusses zum Versorgungsnetz bzw. eindeutig identifizierten Versorgungspin prüfen. Fotopunkt und Polarität dokumentieren. | +5VA als Testpunkt und 13,5 V am L4981 beweisen die Versorgung direkt am MCU nicht. MCU-Typ/Pinout sind nicht sicher bekannt: keine Versorgungspins raten und noch keinen 3,3-/5-V-Sollwert festlegen. |
| A13 | **Bekannte Freigaben bis zum Empfänger verfolgen:** OC04 und OC05 auf der Transistorseite jeweils vom Kollektor/Emitter über die sichtbaren Widerstände oder Logikstufen bis zum nächsten Anschluss verfolgen. Zugängliche Pads und zugehörigen Massebezug dokumentieren. | OC04 = Enable-Kanal, OC05 = Sollwert-Kanal. Bisherige Funktionstests bzw. DC-Änderungen am Koppler beweisen noch nicht, dass das passende Signal am MCU-Eingang ankommt. Endliche kΩ-Werte allein bestätigen keinen direkten Signalweg. |
| B7/C6 | **Lokale MCU-Versorgung** am nach A12 bestätigten, sicher kontaktierbaren Kondensator: Standby und Start, DC sowie MIN/MAX. | Mit dem identifizierten Versorgungsnetz vergleichen. Abweichungen zwischen Versorgungstestpunkt und MCU können auf eine Zuleitung/Filterstelle hinweisen. Unauffällige Multimeterwerte schließen kurze Einbrüche oder Resetimpulse nicht aus. |
| B8/C7 | **OC04/OC05 hinter der Ausgangsbeschaltung**, nur an nach A13 eindeutig zugeordneten, vorab geklemmten Pads: Standby/Start vergleichen und mit den bereits bekannten Kopplerwerten abgleichen. | Ein statischer Enable-Pegel lässt sich erst mit bekannter Polarität beurteilen. Beim PWM-Kanal ist DC nur der Mittelwert; Hz/Tastgrad nur nutzen, wenn Messgerät und Signalpegel dafür geeignet sind. Kein Hz-Wert ist kein Nachweis fehlender Impulse. |

Diese Schritte sind Zuordnungsaufträge, keine bereits bestätigten neuen Messpunkte. Für jeden neuen Betriebsmesspunkt zuerst Originalfoto mit genauer Endkappe/Pad, Referenz und Messmodus festhalten. Claudes Raster und bestehende Anschluss-IDs bleiben unverändert.

### Präzisierungen für die vorhandenen Schritte

- **A1–A5 / B10:** J1 immer am bestätigten Kathodenanschluss von B10-D1 kontaktieren. Bereits bekannt: J1 → +5VA ca. 9–10 kΩ; ähnliche Werte zu anderen Punkten können über Versorgungspfade entstehen. Die beiden Enden des lokalen 01C getrennt protokollieren. Nur eine bestätigte Kupferverbindung zu einer Endkappe würde die vermutete direkte Einspeisung dort stützen. Pin 4 (IAC), 6 (LFF) und 7 (VRMS) des L4981 sind Prüfkandidaten, keine bekannten Ziele von J1; auch eine gefundene Verbindung zum PFC-Regler beweist keinen MCU-Messeingang. Signalform und Sollpegel an J1 bleiben offen.
- **A4 / B4:** Durchgang zu Versorgung und Masse identifiziert noch nicht Ein- und Ausgang des SOT-23-5. Dafür Aufdruck/Pinout und Beschaltung einschließlich des Anschlusses hinter 47R5 klären. Bis dahin B4/C4 am unbekannten IC zurückstellen; keine Gate-Treiberpins als vermeintliche Netzsignal-Eingänge interpretieren.
- **A6:** Kleinster Widerstand = Kandidat, nicht gesicherte Zuordnung. Bei OC05 ist der direkte Pfad über ca. 1 kΩ bestätigt; andere Kanäle können über aktive Stufen laufen. Bei fehlendem Treffer die sichtbare Bahn bis zum nächsten Widerstand/Logikpin verfolgen. Steckzustand notieren; für die reine Platinenzuordnung P2/P4 abziehen. Kein zusätzliches Signal einspeisen.
- **B5 / C1:** OC02/03/08-Kathoden → P2.7 wurden bereits mit 0 Ω dokumentiert (`netlist/optokoppler_zuordnung.md`). Die Bewertung Anode gegen P2.7 gilt für diese bestätigte Zuordnung. Bei gepulster Ansteuerung sind auch Mittelwerte weit unter 1,1 V möglich; daraus nicht „aus/defekt“ folgern. Eine Änderung eines unbekannten Kanals beweist noch keine Wake-/Sleep-Funktion.
- **B1 / C5:** Bei +5 V und +12 V zeigt ein Einbruch einen kleineren Wert (**MIN**); bei −12 V geht ein Einbruch Richtung 0 V, also zu einem größeren Wert (**MAX**, z. B. −8 V). Für alle Schienen beide Extremwerte notieren. Zur Prüfung der TL082-Versorgung zusätzlich stromlos bestätigen, dass die Testpunktnetze die tatsächlichen Versorgungspins erreichen; bei Auffälligkeit deren Zuleitung verfolgen.
- **Messgrenzen und Bezug:** 0VA/Elko-Minus liegt auf Netzpotential und ist nicht P2.7 oder Schutzleiter. Die Formulierung „Konsolenseite, ungefährlich“ ist keine Freigabe zum freien Antasten der offenen, versorgten Platine. Betriebsmessungen nur mit geeigneter Ausrüstung und Fachkenntnis, vorab stromlos gesetzten isolierten Klemmen und gesicherter Mechanik. Keine geerdete Oszilloskopmasse oder USB-Messverbindung an 0VA; eine notwendige Signalformmessung erfordert geeignete potentialgetrennte Messtechnik. Messbereich oder Klemmen nur spannungsfrei ändern. Keine Isolationsprüfung mit hoher Prüfspannung an der bestückten Elektronik.

### Ablauf und Entscheidungsregeln

1. Zuerst stromlose Zuordnungen A1–A4 und A12/A13. A1–A4 klären, ob der neue SOT-23-5-Bereich überhaupt zu B10 gehört. Liegt eine andere Funktion vor, diese getrennt dokumentieren und B10 ab J1 weiterverfolgen.
2. Dann Versorgung B1/B7; bei einer klaren Versorgungsabweichung zuerst diese lokalisieren, bevor unbekannte Signalpegel bewertet werden.
3. Bei passenden Versorgungen bekannte Eingänge OC04/OC05 bis zur Empfängerseite prüfen. Die Zuordnung weiterer Koppler A6 kann stromlos parallel vorbereitet werden. Erst danach unbekannte P13/P70-Pegel oder weitere Analogsignale priorisieren.
4. Pro Startversuch nur die vorbereitete Messung durchführen. Gleiche Ausgangslage: keine Handbewegung des Bandes vor START, Steckzustand und Ausschaltpause notieren. Zeitpunkt START, erste Bewegung, STS2, eigener STOP und Konsolenfehler getrennt festhalten; die Abfragezeiten im Log sind keine exakten elektrischen Flankenzeitpunkte.
5. Vergleich anderer Stromkreis: gleiche Ausgangslage und keine gleichzeitige Reinigung/Nachlötung. Ein einzelner erfolgreicher Start beweist bei diesem sporadischen Fehler keine Netzursache; bei sicher durchführbarem Vergleich Rückvergleich am bisherigen Anschluss vorsehen. Bei spontan erfolgreichem Lauf sind Vergleichswerte derselben vorbereiteten Messpunkte besonders aussagekräftig.

Pro Messung festhalten: Schritt-ID, Foto/Pad, Rot/Schwarz, Modus und Einheit, Steckzustand, Standbywert, Startwert, MIN/MAX und Ablesedauer. Eine konkrete Abweichung zunächst reproduzieren und entlang des zugehörigen Netzes eingrenzen; keine Bauteile allein wegen einer Hypothese tauschen.

### Änderungsvorschläge zur Rückmeldung – ursprüngliche Zeilen nicht gestrichen

- **A5 „alle 32 MCU-Pins“ sowie B2/C2 P13/P70 nachrangig:** Ohne bekannte Funktion ergeben sich viele Widerstands- und Mittelwerte ohne Entscheidungskriterium. Zuerst entlang sichtbarer Bahnen bis zum nächsten Bauteil gehen; eine vollständige Pin-Suche erst, wenn der Weg dort endet.
- **A8 nicht auf einen 01C festlegen:** Ein 10-kΩ-Pull-up ist an T3 belegt, nicht automatisch an T2. Die T2-Kette anhand ihrer tatsächlichen Bauteile verfolgen, ohne die T3-Schaltung zu übertragen.
- **A10 F27 nicht als Wiederholung des Relaistests:** 24 V am Spulen-Plus und 0 V über der Spule beim Fehlstart sind bereits gemessen. Ein neuer Erkenntnisgewinn wäre die Zuordnung/Prüfung der Treiberansteuerung; die fehlende Spulenspannung allein beweist keine bewusste MCU-Entscheidung.

Quellen: [Tagesprotokoll](LAUF_2026-11-14.md), [B10-Messwerte](netlist/messprotokoll_b10.csv), [Optokoppler-Zuordnung](netlist/optokoppler_zuordnung.md). Diese Ergänzung enthält keine neuen Messergebnisse und ändert keine Originalfotos.
