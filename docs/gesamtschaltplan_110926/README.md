# Gemeinsamer Schaltplan der gemessenen GIRT-S6T30-Teilnetze

**[Schaltplan, Detailansichten und Messregister (PDF)](gesamtschaltplan.pdf)** · [Gesamtblatt (PDF)](uebersicht_A1.pdf) · [SVG zum Zoomen](gesamtschaltplan.svg) · [Bearbeitbare KiCad-Datei](GIRT_Gesamtschaltplan.kicad_sch)

Stand **16.11.2026**, Branch **main**, Quellenstand `d917aa8dcadb72afa94c133d4b6bf7259a89952a`. Der historische Verzeichnisname bleibt erhalten. Ein gemeinsames, elektrisch verbundenes KiCad-Blatt im **Sonderformat 841 × 1250 mm** enthält 57 Bauteile/Anschlussblöcke mit 149 Pins. `uebersicht_A1.pdf` behält seinen Dateinamen aus Kompatibilitätsgründen; das Blatt ist nicht mehr A1. Die PDF hat 40 Seiten einschließlich vergrößerter Ausschnitte und Messregister.

![Gemeinsamer Schaltplan](gesamtschaltplan.svg)

## Aktuelle Verbindungen

| Bereich | Bestätigter Stand | CAD |
|---|---|---|
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

[Befunde bis 16.11. morgens](befunde_2026-11-16.csv) und [Abendbefunde](befunde_2026-11-16_abend.csv) ergänzen die unveränderten historischen Rohprotokolle. Die jeweils letzten bestätigten Korrekturen im [Tagesprotokoll](../LAUF_2026-11-14.md) haben Vorrang vor zurückgenommenen Zwischenständen. [Alle Verbindungsbelege](verbindungsbelege.csv), [Bauteile](bauteile.csv), [Netze](netze.csv), [Modell](connected_model.json), [KiCad-XML](gesamtschaltplan.xml).

- **M** = berichtete Messung, **F** = Fotoverlauf, **I** = Ableitung. **AKT-059/060 waren falsche Foto-Aliase** und werden nicht mehr als Kupfer vereinigt. Die neuen Messungen AKT-065/066 haben Vorrang. AKT-024 bezeichnet nun R1; AKT-061 wird auf den weiterhin fotografisch zugeordneten R1a-Anschluss begrenzt. Historische Eingabe-CSV unverändert; wirksame Belegliste kennzeichnet die Überholung. Es gibt keinen dritten 4751.
- MCU-Nummern sind **Arbeitsnummern nach angenommener QFP-Zählung**, keine bestätigten Datenblatt-Pins oder Herstellerfunktionen. MCU-Typ, Masseanschluss und übrige Pins bleiben unbekannt.
- OC04 E–0VA 3,3 kΩ, OC05 E–0VA 10 kΩ und P2.5 → LM2903.6 17 kΩ sind **In-Circuit-Messungen**, keine identifizierten Einzelwiderstände. OC04 Kathode liegt an LM2903.7. OC05 Kathode liegt an P2.7; der 0,956-kΩ-Pfad von P2.6 zur Anode bleibt als unaufgelöster Serienpfad dokumentiert. Die nicht aufgeklärte OC04-Anode wird nicht erfunden.
- LD3N ist ein Schottky-Kandidat. Diodentests belegen keine Leckdiagnose. Es gibt weder eine X–Y-Brücke noch einen Serienkondensator. P13 wird nicht mit X verbunden.
- F27 wurde extern wiederholt geschaltet, Kontakt angezogen 0,03 Ω; Spule ca. 1,4 kΩ. Im Fehlstart waren über der Spule 0 V gemeldet. Eine Freilaufdiode, T4-Bahn(b)-Funktion und ein Relais-Rückmeldesignal sind nicht zugeordnet.
- 1P-Diodentests wurden **13.11. durchgeführt**: L→R/L→O je 0,70 V, rückwärts 1,56/2,18 V eingebaut; O–R 3,39 kΩ. Die alte Datei mit ausstehenden Tests bleibt als historische Quelle erhalten und beschreibt nicht den aktuellen Status.
- Der [Fotoentwurf Q2-A/1001/4752](../fotospuren_2026-11-12/README.md) bleibt ausdrücklich eine separate F-Rekonstruktion. Seine bisher nicht elektrisch bestätigten Verbindungen sind hier nicht als gemessene Kupferverbindungen übernommen; R203/R204 bleiben unzugeordnet. FAN3100C und genaue 1P-/T2-/T3-/T4-Typen bleiben Kandidaten. D5- und T2-Quelle sind offen.
- Original-Messwerte einschließlich überholter B10-M16-Angabe, historischer Relaiswerte und B20-Widerstandswerte bleiben im [Messregister CSV](messwerte.csv) und [vollständigen Rohfeldern JSON](messwerte_vollstaendig.json). 228 Zeilen umfassen 87 Zeilen vom 09.11., 82 aktuelle/historisch korrigierte Belege und 59 historische Messungen/Beobachtungen.

## Reproduktion und Prüfung

`python docs/gesamtschaltplan_110926/erzeugen.py` benötigt KiCad CLI 9, PyMuPDF und ReportLab. Der Generator bildet die erwarteten Netze aus den historischen Eingaben und der separaten aktuellen Befund-CSV; er vergleicht alle Pinpaare mit der tatsächlich exportierten KiCad-Netzliste. [Prüfnachweis](pruefnachweis.json): **149 Pins, 22.201 Vergleiche, Netzgruppen identisch**. Getrennte Masse-/Versorgungsnetze, X/Y und Serienpfade werden zusätzlich ausdrücklich geprüft. PDF/SVG/XML wurden erfolgreich exportiert. Das ist eine Dateikonsistenzprüfung, kein elektrischer Funktionstest.

[Originalmedien-Prüfung](originalmedien_pruefung.json): Alle 252 bereits im Quellenstand vorhandenen Dateien unter `photos/` und `docs/img/` sind bytegleich erhalten. Es wurden keine neuen Messungen ausgeführt, keine Fotos geändert oder erzeugt und keine Fehlerursache bewiesen. Der [alte Teilschaltplan](../schaltplan_110926/README.md) bleibt historisch erhalten.

## Unabhängige Endprüfung

Die Aktualisierung wurde an **GPT-6.1 Sol mit niedrigem Reasoning-Aufwand** delegiert und anschließend vom Hauptagenten gegen die Originalbelege geprüft. Die erste Prüfung bestätigte fälschlich eine Fotozuordnung von R2 als Serienwiderstand. Die Abendmessungen widerlegen diese; der Hauptagent hat nun R1 als Serienwiderstand und R2 als Widerstand nach Masse korrigiert. Die damalige Dateikonsistenzprüfung war kein unabhängiger elektrischer Beleg für die Fotozuordnung. Versorgungshinweise, TL082-Rückkopplung und T2-Serienpfad bleiben erhalten. Zusätzliche Detailansichten zeigen Anschlüsse und MCU-Arbeitsnummern lesbar.

Die [zweite Prüfung](unabhaengige_pruefung.json) verwendet eigene, aus den letzten Protokollkorrekturen abgeleitete Anschluss-Erwartungen direkt gegen die exportierte KiCad-XML-Netzliste – ohne Import des Generators oder seines Netzmodells. **64 Prüfungen bestanden**, darunter getrennte MCU-Eingänge, Versorgungen, Konsolenmasse und alle Widerstandsenden. [Prüfskript](pruefen_unabhaengig.py): `python docs/gesamtschaltplan_110926/pruefen_unabhaengig.py`. Zusätzlich sind **260 Original-/Referenzdateien** inklusive der bisherigen Messplan-Markierungen gegenüber dem Quellenstand bytegleich.


## Abendstand und verbleibende Grenzen

PDF, SVG, KiCad, Register und Prüfnachweise sind nach Einbindung von AKT-064 bis AKT-082 neu erzeugt. Der Generator liest beide Befunddateien und deaktiviert widersprochene Fotoverbindungen. Zusätzlich zur Korrektur des X-Teilers enthält er die bestätigte ADM485/OC06-Kupfergruppe.

P600-Kontakt1–Y ca. 1 kΩ und Y–0VA 1,883 kΩ sind Messkopplungen, keine isoliert identifizierten Bauteile. P600-Kontakt2=+5VA ist als Netzalias gemessen; die Zuordnung zu den alten Sensorpins Ka/Kb ist weiterhin offen. Deshalb bleibt die native NTC-Darstellung mit den alten Sensorlabels getrennt und erhält die neuen Befundhinweise. Auch P4 TACHO→ADM485 Pin7 1,103 kΩ ist kein als isolierter Einzelwiderstand eingezeichnetes Bauteil. [Bewertung und Messentscheidungen](../PRUEFUNG_2026-11-16_spaet.md).


## Messnachtrag 17.11.2026 – Sensor bis P4

[Tagesprotokoll mit Bewertung und nächstem Messpunkt](../LAUF_2026-11-17.md), [Messregister dieser Sitzung](../messprotokoll_2026-11-17.csv). Sensor C–E und P4-TACHO schalten bei manueller Bewegung etwa 0–12 V; High-Wackeltest unauffällig. Braun–C und Weiß–A je 0 Ω, beide 0-V-Adern zeigen im gemessenen Aufbau 0 Ω zu E/K; Einzeladerzuordnung ohne Parallelrückwege und LED-Strombegrenzung bleiben offen. Kein neuer Funktionsnachweis für ADM485/OC06 oder dessen MCU-Ziel.

Der native CAD-/PDF-Stand bleibt ausdrücklich **16.11.**; die heutigen Betriebswerte sind im verlinkten Sitzungsregister, nicht im bisherigen generierten Messregister enthalten. Die bestätigte P4–Konsolenmasse/ADM485-RO–OC06-K-Topologie ändert sich nicht. Die externe Sensorplatine mit A/K/C/E ist im nativen Blatt noch nicht detailliert modelliert. Keine ungesicherten Einzeladern, Vorwiderstände oder MCU-Anschlüsse ergänzt. Für die neue Messanweisung gilt OC06-K = ADM485.1 (AKT-082).
