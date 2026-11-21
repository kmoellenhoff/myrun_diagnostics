# Gemeinsamer Schaltplan der gemessenen GIRT-S6T30-Teilnetze

**[Schaltplan, Detailansichten und Messregister (PDF)](gesamtschaltplan.pdf)** · [Gesamtblatt (PDF)](uebersicht_A1.pdf) · [SVG zum Zoomen](gesamtschaltplan.svg) · [Bearbeitbare KiCad-Datei](GIRT_Gesamtschaltplan.kicad_sch)

Stand **21.11.2026**, Branch **main**, Quellenstand `89748e932129eaaa9f03a0504eaa5261f45b501d`. Der historische Verzeichnisname bleibt erhalten. Das gemeinsame KiCad-Blatt im **Sonderformat 841 × 1250 mm** enthält 58 Bauteile/Anschlussblöcke mit 151 Pins und zeigt die **rekonstruierte Originalschaltung**. `uebersicht_A1.pdf` behält seinen Dateinamen; das Blatt ist nicht A1. Die Sammel-PDF hat 42 Seiten einschließlich Details, separatem Ist-Umbau und Messregister.

**Neu: [B10-Ist-Umbau vom 21.11. (PDF)](b10_umbau_2026-11-21.pdf) · [SVG](b10_umbau_2026-11-21.svg) · [KiCad](B10_Umbau_2026-11-21.kicad_sch).** Dieses eigenständige Blatt dokumentiert die tatsächlich eingesetzten neuen Teile (US1M, 470 kΩ) je Seite in der Reihenfolge **Faston – 470 kΩ – 470 kΩ – US1M – J** (Kathode an J), also der Reihenfolge der Originalschaltung mit neuen Teilen. Die neuen Teile sitzen auf den alten Pads; die zusätzlichen Litzen überbrücken dieselben Knoten und sind keine Parallelzweige. Es ist keine zusätzliche Parallelschaltung zum Originalblatt. **Korrigiert am 21.11. nach Nutzerangabe 14:50–14:53; der Neuaufbau von PDF/SVG/XML mit KiCad ist OFFEN (siehe unten).** C602 (J gegen 0VA, kalt 0,43 nF gemessen) ist in beiden Ansichten als **DNP / derzeit ausgebaut** markiert. 470 pF ist der abgeleitete Nennwertkandidat, kein gelesener Originalwert.

[Prüfung, Korrekturen und noch fehlende Verbindungen](../PRUEFUNG_SCHALTPLAN_2026-11-21.md) · [Neue Befunde](befunde_2026-11-21.csv) · [Aktuelles Tagesprotokoll](../LAUF_2026-11-21.md). C602 filtert schnelle Störungen; er erkennt keine Spannungsspitzen und garantiert ohne Bestückung keine MCU-Abschaltung. Die 100-Hz-Netzwelle wird durch rund 470 pF kaum geglättet.

![Gemeinsamer Schaltplan](gesamtschaltplan.svg)

## Aktuelle Verbindungen

| Bereich | Bestätigter Stand | CAD |
|---|---|---|
| J-Filter | Kondensator zwischen J und 0VA am 21.11. zugeordnet; ausgebaut 0,43 nF, seit Wärmetest entfernt. Temperaturabhängiger Defekt oder Anschlussumfeld verdächtig, kein isolierter Lecknachweis | C602, DNP |
| B10 / TL082-A | J1 → 22,1 kΩ nach 0VA; J1 → 1 kΩ → TL082 Pin 3; Pin 1 = 2; Pin 8 +12VA, Pin 4 −12VA, Pin 5 0VA | R401–R404, D401/D402, R601/R602, U602 |
| Netzsignal X | TL082 Pin 1 → R1 (4,75 kΩ) → N; R2 (4,75 kΩ) N–0VA; N → 100 Ω → X/MCU28; C von X nach 0VA | R301/R302, R603, C601, U601 |
| Y, P600-Kandidat | MCU26 = LD3N O; L=0VA, R=+5VA. Y–P600 Kontakt1 ca. 1 kΩ, Kontakt2=+5VA. Endliche Messkopplung, kein erfundener Einzelwiderstand; Ka/Kb-Alias offen | U605, U601 |
| B20-Widerstände | **Fotozuordnung widerlegt:** R1 ist Serienwiderstand, R1b=R2b, R2a=0VA gemessen. R1a=TL082-Ausgang bleibt Fotozuordnung; N→100-Ω-Pad ist als Ableitung dokumentiert. Altwerte erhalten | R301–R304 |
| MCU / Koppler | Arbeitsnummer 8 +5VA; OC04/05 Kollektoren +5VA; OC04 Emitter → 12, OC05 Emitter → gemeinsam 17/18 | U601, U603/U604 |
| T3 / PFC-Sperre | MCU 11 → 2,21 kΩ → T3-Basis Tc; 10-kΩ-01C-Pullup von MCU11 nach +5VA. T3 Ta=C → L4981 Pin15, Tb=E → 0VA. MCU13 = P70 | U401, R604/R605, U301 |
| F27 / T4 | MCU24 → 1 kΩ → T4 Basis L; Emitter R 0VA; Kollektor O = Spulenminus. Spulenplus +24V = SOT223-Tab; dessen Typ offen. Historische Ca/Cb-Polzuordnung bleibt offen | R606, Q601, K501, TP604 |
| Q2-Freigabe | 1P.L → 475 Ω → 2,21 kΩ → T2 Kollektor O; T2 Emitter R = 0VA, Basis L = Testpad. Kleiner 01C/010 und dessen Quelle nicht ausreichend identifiziert | U202, R607/R608, Q602 |
| Treiberversorgung | Q2-Treiber C = L4981 Pin19, gemessen stabil 13,5 V. Dieses Netz ist kein MCU-VDD und ohne Gleichheitsbeleg nicht mit +12VA vereinigt | U201, U301 |

L− → Q2-Drain und L+ → Zwischenkreis-Elko-Plus sind inzwischen mit eigenen 0-Ω-Messungen vom 12.11. belegt. ADM485 Pin1=OC06-Kathode und Pin5=LM2903 Pin4=P2.7 sind nun nativ enthalten (U606/U607). Die Tacho-Funktion ist Kandidat; OC06-Ausgangsbezug und MCU-Pin bleiben offen. B18/B19, Motor/Q2, Gatepfad, P2/P4, NTC und bislang nicht ersetzte Teilnetze bleiben erhalten. **0VA und 0V_KONSOLE sind getrennt.** 0V24 = 0VA gilt weiterhin nur für den damals gemessenen Steckzustand. Die CAD-Referenzen ändern weder bestehende Bauteil-IDs noch Claudes Raster A–L × 1–6.

## Belege und Grenzen

[Befunde bis 16.11. morgens](befunde_2026-11-16.csv), [Abendbefunde](befunde_2026-11-16_abend.csv) und [Ergänzungen vom 21.11.](befunde_2026-11-21.csv) ergänzen die unveränderten historischen Rohprotokolle. Schlusskorrekturen haben Vorrang vor zurückgenommenen Zwischenständen. [Alle Verbindungsbelege](verbindungsbelege.csv), [Bauteile Originalmodell](bauteile.csv), [Bauteile Ist-Umbau](bauteile_umbau_2026-11-21.csv), [Netze Originalmodell](netze.csv), [Modell](connected_model.json), [KiCad-XML](gesamtschaltplan.xml), [Ist-Modell](umbau_model_2026-11-21.json), [Ist-XML](b10_umbau_2026-11-21.xml).

- **M** = berichtete Messung, **F** = Fotoverlauf, **I** = Ableitung. **AKT-059/060 waren falsche Foto-Aliase** und werden nicht mehr als Kupfer vereinigt. Die neuen Messungen AKT-065/066 haben Vorrang. AKT-024 bezeichnet nun R1; AKT-061 wird auf den weiterhin fotografisch zugeordneten R1a-Anschluss begrenzt. Historische Eingabe-CSV unverändert; wirksame Belegliste kennzeichnet die Überholung. Es gibt keinen dritten 4751.
- MCU-Nummern sind **Arbeitsnummern nach angenommener QFP-Zählung**, keine bestätigten Datenblatt-Pins oder Herstellerfunktionen. MCU-Typ, Masseanschluss und übrige Pins bleiben unbekannt.
- OC04 E–0VA 3,3 kΩ, OC05 E–0VA 10 kΩ und P2.5 → LM2903.6 17 kΩ sind **In-Circuit-Messungen**, keine identifizierten Einzelwiderstände. OC04 Kathode liegt an LM2903.7. OC05 Kathode liegt an P2.7; der 0,956-kΩ-Pfad von P2.6 zur Anode bleibt als unaufgelöster Serienpfad dokumentiert. Die nicht aufgeklärte OC04-Anode wird nicht erfunden.
- LD3N ist ein Schottky-Kandidat, Innenstruktur nicht bestätigt. Die zuvor gezeichneten zwei Dioden wurden durch einen Anschlussblock ersetzt; bestätigte L/O/R-Netze bleiben erhalten. Es gibt weder eine X–Y-Brücke noch einen Serienkondensator. P13 wird nicht mit X verbunden.
- **TL082-Pinzählung am 21.11. geklärt:** Alle am 21.11. vom Nutzer genannten Pinnummern waren um 180° gedreht gezählt (echte Pinnummer = 9 − genannte). Der Schaltplan-Pin 3 für 1001 (Eingang A+) bleibt richtig. Echte Belegung: 1 OUT A, 2 IN A−, 3 IN A+, 4 V− (−12VA), 5 IN B+, 6 IN B−, 7 OUT B, 8 V+ (+12VA). Pin 6 ist als offener Pin ohne belegtes Netz geführt (`N_TL082_6`); „Pin 6/7 vermutlich verbunden, nicht gemessen“ ist Hypothese [H] (NOV21-015), kein Kupfer. Der braune Kondensator (genannt „Pin 5“) liegt an echtem Pin 4 (−12VA) gegen 0VA: wahrscheinlich Abblockkondensator der Versorgung [I], kein Eingangsfilter; die Zuordnung der früheren 0-Ω-/5-MΩ-Angaben bleibt offen.
- F27 wurde extern wiederholt geschaltet, Kontakt angezogen 0,03 Ω; Spule ca. 1,4 kΩ. Im Fehlstart waren über der Spule 0 V gemeldet. Eine Freilaufdiode, T4-Bahn(b)-Funktion und ein Relais-Rückmeldesignal sind nicht zugeordnet.
- 1P-Diodentests wurden **13.11. durchgeführt**: L→R/L→O je 0,70 V, rückwärts 1,56/2,18 V eingebaut; O–R 3,39 kΩ. Die alte Datei mit ausstehenden Tests bleibt als historische Quelle erhalten und beschreibt nicht den aktuellen Status.
- Der [Fotoentwurf Q2-A/1001/4752](../fotospuren_2026-11-12/README.md) bleibt ausdrücklich eine separate F-Rekonstruktion. Seine bisher nicht elektrisch bestätigten Verbindungen sind hier nicht als gemessene Kupferverbindungen übernommen; R203/R204 bleiben unzugeordnet. FAN3100C und genaue 1P-/T2-/T3-/T4-Typen bleiben Kandidaten. D5- und T2-Quelle sind offen.
- Original-Messwerte einschließlich überholter B10-M16-Angabe, historischer Relaiswerte und B20-Widerstandswerte bleiben im [Messregister CSV](messwerte.csv) und [vollständigen Rohfeldern JSON](messwerte_vollstaendig.json). 243 Zeilen umfassen 87 Zeilen vom 09.11., 97 aktuelle/historisch korrigierte Belege einschließlich 21.11. und 59 historische Messungen/Beobachtungen. Vollständige spätere Betriebslogs bleiben in ihren Sitzungsdateien.

## Korrektur vom 21.11. (Nutzerangabe 14:50–14:53) und offener Neuaufbau

- **B10-Umbau:** Je Seite (L und N) eine Kette aus neuen Teilen: Faston-Pad – 470 kΩ (4703) – 470 kΩ (4703) – US1M – J (Lötbrücke „2212/1001“), Diodenstrich (Kathode) am J-Ende, Anode am Widerstandsende. Netze: Faston L/N = R1.1; R1.2 = R2.1; R2.2 = Anode; Kathode = J (`B10_KATHODEN`). Die frühere Darstellung (Faston → US1M → R → R → J) war falsch. Belege: ca. 940 kΩ pro Seite (rot Faston, schwarz J; umgekehrt OL) [M], J gegen 0VA positiv (4,9 V) [M]; Reihenfolge und Pads nach Foto/Nutzerangabe [F]/[I].
- **Geändert:** `befunde_2026-11-21.csv` (NOV21-004 bis -015), `verbindungsbelege.csv`, `messwerte.csv`, `messwerte_vollstaendig.json`, `netze.csv`, `connected_model.json`, `bauteile_umbau_2026-11-21.csv`, `umbau_model_2026-11-21.json`, `B10_Umbau_2026-11-21.kicad_sch`, Textzeile im Hauptblatt `GIRT_Gesamtschaltplan.kicad_sch`, Erwartungen in `erzeugen.py` und `pruefen_unabhaengig.py`. Diese Dateien wurden mit den Generatorfunktionen ohne KiCad-Export und ohne PDF-Erzeugung neu geschrieben, nicht von Hand in den generierten Ausgaben verändert.
- **OFFEN (Neuaufbau):** In der Bearbeitungsumgebung fehlten KiCad CLI, PyMuPDF und ReportLab. Deshalb sind `b10_umbau_2026-11-21.pdf/.svg/.xml`, `gesamtschaltplan.pdf/.svg/.xml`, `uebersicht_A1.pdf`, `pruefnachweis.json` und `unabhaengige_pruefung.json` **noch auf dem alten (falschen) Stand** und zeigen im Umbau-Blatt noch die Reihenfolge Faston → US1M → R → R → J. Bitte mit KiCad CLI 9 `python docs/gesamtschaltplan_110926/erzeugen.py` und danach `pruefen_unabhaengig.py` ausführen und die Ergebnisse committen. Bis dahin gelten CSV/JSON/.kicad_sch und diese Beschreibung, nicht die alten PDF/SVG/XML.

## Reproduktion und Prüfung

`python docs/gesamtschaltplan_110926/erzeugen.py` benötigt KiCad CLI 9, PyMuPDF und ReportLab. Der Generator bildet die erwarteten Netze aus den Quellen und vergleicht alle Pinpaare mit den tatsächlich exportierten KiCad-Netzlisten. [Prüfnachweis](pruefnachweis.json) (Stand vor der Korrektur vom 21.11., Neuaufbau OFFEN): Hauptblatt **151 Pins, 22.801 Vergleiche**, Ist-Blatt **18 Pins, 324 Vergleiche**, Netzgruppen identisch. Getrennte Masse-/Versorgungsnetze, X/Y und Serienpfade bleiben erhalten. PDF/SVG/XML wurden exportiert. Das ist eine Dateikonsistenzprüfung, kein elektrischer Funktionstest.

[Originalmedien-Prüfung](originalmedien_pruefung.json): Alle **282** im Quellenstand vorhandenen Original-/Referenzdateien unter `photos/`, `docs/img/` und den Messplan-Makros sind bytegleich erhalten. Es wurden keine neuen Messungen ausgeführt, keine Fotos geändert oder erzeugt und keine Fehlerursache bewiesen. Der [alte Teilschaltplan](../schaltplan_110926/README.md) bleibt historisch erhalten.

## Unabhängige Endprüfung

Die Aktualisierung wurde an **GPT-6.1 Sol mit niedrigem Reasoning-Aufwand** delegiert und anschließend vom Hauptagenten gegen die Originalbelege geprüft. Die erste Prüfung bestätigte fälschlich eine Fotozuordnung von R2 als Serienwiderstand. Die Abendmessungen widerlegen diese; der Hauptagent hat nun R1 als Serienwiderstand und R2 als Widerstand nach Masse korrigiert. Die damalige Dateikonsistenzprüfung war kein unabhängiger elektrischer Beleg für die Fotozuordnung. Versorgungshinweise, TL082-Rückkopplung und T2-Serienpfad bleiben erhalten. Zusätzliche Detailansichten zeigen Anschlüsse und MCU-Arbeitsnummern lesbar.

Die [Prüfung ohne Generatorimport](unabhaengige_pruefung.json) verwendet eigene Anschluss-Erwartungen direkt gegen die exportierten XML-Netzlisten. Zu den bisherigen 64 Netzprüfungen kommen drei C602-Prüfungen und zehn Prüfungen des separaten Ist-Blatts; DNP, Ersatzteilwerte und Trennung der Bestückungsstände werden zusätzlich geprüft. [Prüfskript](pruefen_unabhaengig.py): `python docs/gesamtschaltplan_110926/pruefen_unabhaengig.py`. Original-/Referenzdateien inklusive Messplan-Markierungen werden gegen den aktuellen Quellenstand bytegleich geprüft. Das ist eine getrennte Prüflogik desselben Bearbeiters, keine neue unabhängige elektrische Messung.


## Historische Nachträge bis 17.11. – damaliger CAD-Stand

Die folgenden Einträge dokumentieren die damaligen Arbeitsstände. Aussagen „CAD/PDF bleibt Stand 16.11.“ wurden durch den oben beschriebenen Neuaufbau am **21.11.** abgelöst; die jeweiligen Messgrenzen bleiben gültig.

### Abendstand und verbleibende Grenzen

PDF, SVG, KiCad, Register und Prüfnachweise sind nach Einbindung von AKT-064 bis AKT-082 neu erzeugt. Der Generator liest beide Befunddateien und deaktiviert widersprochene Fotoverbindungen. Zusätzlich zur Korrektur des X-Teilers enthält er die bestätigte ADM485/OC06-Kupfergruppe.

P600-Kontakt1–Y ca. 1 kΩ und Y–0VA 1,883 kΩ sind Messkopplungen, keine isoliert identifizierten Bauteile. P600-Kontakt2=+5VA ist als Netzalias gemessen; die Zuordnung zu den alten Sensorpins Ka/Kb ist weiterhin offen. Deshalb bleibt die native NTC-Darstellung mit den alten Sensorlabels getrennt und erhält die neuen Befundhinweise. Auch P4 TACHO→ADM485 Pin7 1,103 kΩ ist kein als isolierter Einzelwiderstand eingezeichnetes Bauteil. [Bewertung und Messentscheidungen](../PRUEFUNG_2026-11-16_spaet.md).


## Messnachtrag 17.11.2026 – Sensor bis P4

[Tagesprotokoll mit Bewertung und nächstem Messpunkt](../LAUF_2026-11-17.md), [Messregister dieser Sitzung](../messprotokoll_2026-11-17.csv). Sensor C–E und P4-TACHO schalten bei manueller Bewegung etwa 0–12 V; High-Wackeltest unauffällig. Braun–C und Weiß–A je 0 Ω, beide 0-V-Adern zeigen im gemessenen Aufbau 0 Ω zu E/K; Einzeladerzuordnung ohne Parallelrückwege und LED-Strombegrenzung bleiben offen. Kein neuer Funktionsnachweis für ADM485/OC06 oder dessen MCU-Ziel.

Der native CAD-/PDF-Stand bleibt ausdrücklich **16.11.**; die heutigen Betriebswerte sind im verlinkten Sitzungsregister, nicht im bisherigen generierten Messregister enthalten. Die bestätigte P4–Konsolenmasse/ADM485-RO–OC06-K-Topologie ändert sich nicht. Die externe Sensorplatine mit A/K/C/E ist im nativen Blatt noch nicht detailliert modelliert. Keine ungesicherten Einzeladern, Vorwiderstände oder MCU-Anschlüsse ergänzt. Für die neue Messanweisung gilt OC06-K = ADM485.1 (AKT-082).


## Weiterer Nachtrag 17.11. – ADM485 und OC05

Im [vollständigen Tagesprotokoll](../LAUF_2026-11-17.md) und [Sitzungs-CSV](../messprotokoll_2026-11-17.csv) sind jetzt **28 Mess-/Beobachtungszeilen** einschließlich korrigierter Zwischenstände enthalten. ADM485 Pin6/A 2,4 V (ersetzt 0,2 V), Pin7/B 2,2 V, RO/OC06-K 4,8 V, ohne sichtbaren Wechsel bei manueller Bandbewegung. Versorgung Pin8 4,8 V, /RE und DE je 0 V. Die Tacho-Funktion dieses Pfads wurde dynamisch nicht bestätigt; ein Defekt ist nicht bewiesen. Die bestehenden 0-Ω-Netze bleiben belegt, endliche Widerstände zu P4 werden nicht als direkte Signalverbindung interpretiert.

OC05-Anode zeigt beim Startversuch kurze Pulse um 1 V; diese Aufnahme wurde vom Nutzer ausdrücklich von OC06 zu OC05 korrigiert. Der native Anschluss OC05.E → MCU17/18 bleibt als Kupfer belegt, seine dynamische Signalqualität ist weiter offen. Messung an Pin3 gegen 0VA wurde wegen ungeklärter Eignung des Oszilloskopaufbaus zurückgestellt und nicht als Ergebnis eingetragen. Keine neue elektrisch geklärte Kupfergruppe: CAD/PDF und deren generiertes Register bleiben beim dokumentierten Stand 16.11., die Betriebswerte stehen separat im Sitzungsregister.


## Foto-/Messwert-Abgleich B10 bis MCU am 17.11.

[Ausführlicher Review](../PRUEFUNG_B10_X_2026-11-17.md): Topologie der Originalmakros, letzte Korrekturen und KiCad-XML sind für die geprüfte B10–X-Kette konsistent; neun Anschlussgruppen und die Trennung X/Y abgeglichen. Belegstufen AKT-009/010/025 sind hinsichtlich der Rohbelege zu stark, und eine zweite Klemmdiode an X ist erst Foto-Kandidat, noch nicht im nativen CAD. Vollständigkeit der X-Schutzbeschaltung ist daher offen. Foto-/Ableitungsgrenzen bleiben ausdrücklich erhalten. Modell an X bei 230 V: 2,35 V DC, 3,70 V Spitze; kein Hersteller-Sollwert. T17-36 (103 mV DC) verlangt zuerst gesicherten Kontakt am X-Kondensatorpad, dann Vergleich J/Pin3/Pin1/N/X und reale ±12VA-Versorgung. CAD-Stand unverändert 16.11.; keine neuen Kupferbelege oder elektrischen Messungen durch diesen Review.


## Messnachtrag bis T17-52 – keine neue Kupfergruppe

[Tagesprotokoll](../LAUF_2026-11-17.md) und [Sitzungs-CSV](../messprotokoll_2026-11-17.csv) enthalten jetzt **52** Mess-/Beobachtungszeilen, einschließlich der zuvor nur im Protokoll vorhandenen T17-29 bis T17-36. J-/TL082-Abfälle sind kontaktierungsbedingt ungesichert; zuletzt beide J-Kontakte etwa 300 mV ohne Klicken. TL082-Schienen −14/+13,5 V bei Einzelmessungen, +5VA stabil 5 V mindestens 2 Minuten ohne Relaisereignis. Keine gleichzeitige Entwarnung für die frühere Klickfolge. Der [aktuelle Plan](../MESSPLAN_2026-11-14_abend.md) verlangt zuerst sichere stationäre Kontaktierung. CAD/PDF und deren Register bleiben ausdrücklich Stand 16.11.; unsichere Spannungswerte erzeugen keine neuen Kupferverbindungen. [Gerätespezifikationen](../MESSGERAET_ASTROAI_DM6000AR.md).
