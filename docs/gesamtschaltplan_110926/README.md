# Gemeinsamer Schaltplan der gemessenen GIRT-S6T30-Teilnetze

**[Schaltplan, Detailansichten und Messregister (PDF)](gesamtschaltplan.pdf)** · [Gesamtblatt (PDF)](uebersicht_A1.pdf) · [SVG zum Zoomen](gesamtschaltplan.svg) · [Bearbeitbare KiCad-Datei](GIRT_Gesamtschaltplan.kicad_sch)

Stand **16.11.2026**, Branch **main**, Quellenstand `f60fe5d339c43876fd33d5baed5f18d2b33cc3d1`. Der historische Verzeichnisname bleibt erhalten. Ein gemeinsames, elektrisch verbundenes KiCad-Blatt im **Sonderformat 841 × 1100 mm** enthält 55 Bauteile/Anschlussblöcke mit 141 Pins. `uebersicht_A1.pdf` behält seinen Dateinamen aus Kompatibilitätsgründen; das Blatt ist nicht mehr A1. Die PDF hat 36 Seiten einschließlich vergrößerter Ausschnitte und Messregister.

![Gemeinsamer Schaltplan](gesamtschaltplan.svg)

## Aktuelle Verbindungen

| Bereich | Bestätigter Stand | CAD |
|---|---|---|
| B10 / TL082-A | J1 → 22,1 kΩ nach 0VA; J1 → 1 kΩ → TL082 Pin 3; Pin 1 = 2; Pin 8 +12VA, Pin 4 −12VA, Pin 5 0VA | R401–R404, D401/D402, R601/R602, U602 |
| Netzsignal X | TL082 Pin 1 → genau ein 4,75 kΩ → 100 Ω → X = MCU-Arbeitsnummer 28; Kondensator von X nach 0VA | R302, R603, C601, U601 |
| Y, Quelle offen | MCU-Arbeitsnummer 26 = LD3N O; L = 0VA, R = +5VA; Diodenrichtungen L → O → R. X und Y bleiben getrennt | U605, U601 |
| B20-Widerstände | Ausgangs-4751 ist B20-R2, a = TL082-Ausgang, b = Via-Richtung MCU. Auch R1a liegt am Ausgang; R1b bleibt offen. Die Zuordnung beruht auf Fotoabgleich [F], nicht auf einer neuen Durchgangsmessung. Beide ursprünglichen In-Circuit-Werte bleiben erhalten | R301–R304 |
| MCU / Koppler | Arbeitsnummer 8 +5VA; OC04/05 Kollektoren +5VA; OC04 Emitter → 12, OC05 Emitter → gemeinsam 17/18 | U601, U603/U604 |
| T3 / PFC-Sperre | MCU 11 → 2,21 kΩ → T3-Basis Tc; 10-kΩ-01C-Pullup von MCU11 nach +5VA. T3 Ta=C → L4981 Pin15, Tb=E → 0VA. MCU13 = P70 | U401, R604/R605, U301 |
| F27 / T4 | MCU24 → 1 kΩ → T4 Basis L; Emitter R 0VA; Kollektor O = Spulenminus. Spulenplus +24V = SOT223-Tab; dessen Typ offen. Historische Ca/Cb-Polzuordnung bleibt offen | R606, Q601, K501, TP604 |
| Q2-Freigabe | 1P.L → 475 Ω → 2,21 kΩ → T2 Kollektor O; T2 Emitter R = 0VA, Basis L = Testpad. Kleiner 01C/010 und dessen Quelle nicht ausreichend identifiziert | U202, R607/R608, Q602 |
| Treiberversorgung | Q2-Treiber C = L4981 Pin19, gemessen stabil 13,5 V. Dieses Netz ist kein MCU-VDD und ohne Gleichheitsbeleg nicht mit +12VA vereinigt | U201, U301 |

L− → Q2-Drain und L+ → Zwischenkreis-Elko-Plus sind inzwischen mit eigenen 0-Ω-Messungen vom 12.11. belegt. B18/B19, Motor/Q2, Gatepfad, P2/P4, NTC und bislang nicht ersetzte Teilnetze bleiben erhalten. **0VA und 0V_KONSOLE sind getrennt.** 0V24 = 0VA gilt weiterhin nur für den damals gemessenen Steckzustand. Die CAD-Referenzen ändern weder bestehende Bauteil-IDs noch Claudes Raster A–L × 1–6.

## Belege und Grenzen

[Befunde 12.–16.11. als separate Eingabequelle](befunde_2026-11-16.csv) ergänzen die unveränderten historischen Rohprotokolle. Die jeweils letzten bestätigten Korrekturen im [Tagesprotokoll](../LAUF_2026-11-14.md) haben Vorrang vor zurückgenommenen Zwischenständen. [Alle Verbindungsbelege](verbindungsbelege.csv), [Bauteile](bauteile.csv), [Netze](netze.csv), [Modell](connected_model.json), [KiCad-XML](gesamtschaltplan.xml).

- **M** = berichtete Messung, **F** = Fotoverlauf, **I** = Ableitung. Die physische B20-R2-Zuordnung verwendet `50370.jpg`, die ursprüngliche R1–R4-Definition und `netzsignal_4751.jpg`. Es gibt keinen zusätzlichen dritten 4751.
- MCU-Nummern sind **Arbeitsnummern nach angenommener QFP-Zählung**, keine bestätigten Datenblatt-Pins oder Herstellerfunktionen. MCU-Typ, Masseanschluss und übrige Pins bleiben unbekannt.
- OC04 E–0VA 3,3 kΩ, OC05 E–0VA 10 kΩ und P2.5 → LM2903.6 17 kΩ sind **In-Circuit-Messungen**, keine identifizierten Einzelwiderstände. OC04 Kathode liegt an LM2903.7. OC05 Kathode liegt an P2.7; der 0,956-kΩ-Pfad von P2.6 zur Anode bleibt als unaufgelöster Serienpfad dokumentiert. Die nicht aufgeklärte OC04-Anode wird nicht erfunden.
- LD3N ist ein Schottky-Kandidat. Diodentests belegen keine Leckdiagnose. Es gibt weder eine X–Y-Brücke noch einen Serienkondensator. P13 wird nicht mit X verbunden.
- F27 wurde extern wiederholt geschaltet, Kontakt angezogen 0,03 Ω; Spule ca. 1,4 kΩ. Im Fehlstart waren über der Spule 0 V gemeldet. Eine Freilaufdiode, T4-Bahn(b)-Funktion und ein Relais-Rückmeldesignal sind nicht zugeordnet.
- 1P-Diodentests wurden **13.11. durchgeführt**: L→R/L→O je 0,70 V, rückwärts 1,56/2,18 V eingebaut; O–R 3,39 kΩ. Die alte Datei mit ausstehenden Tests bleibt als historische Quelle erhalten und beschreibt nicht den aktuellen Status.
- Der [Fotoentwurf Q2-A/1001/4752](../fotospuren_2026-11-12/README.md) bleibt ausdrücklich eine separate F-Rekonstruktion. Seine bisher nicht elektrisch bestätigten Verbindungen sind hier nicht als gemessene Kupferverbindungen übernommen; R203/R204 bleiben unzugeordnet. FAN3100C und genaue 1P-/T2-/T3-/T4-Typen bleiben Kandidaten. D5- und T2-Quelle sind offen.
- Original-Messwerte einschließlich überholter B10-M16-Angabe, historischer Relaiswerte und B20-Widerstandswerte bleiben im [Messregister CSV](messwerte.csv) und [vollständigen Rohfeldern JSON](messwerte_vollstaendig.json). 209 Zeilen umfassen 87 Zeilen vom 09.11., 63 aktuelle Belege und 59 historische Messungen/Beobachtungen.

## Reproduktion und Prüfung

`python docs/gesamtschaltplan_110926/erzeugen.py` benötigt KiCad CLI 9, PyMuPDF und ReportLab. Der Generator bildet die erwarteten Netze aus den historischen Eingaben und der separaten aktuellen Befund-CSV; er vergleicht alle Pinpaare mit der tatsächlich exportierten KiCad-Netzliste. [Prüfnachweis](pruefnachweis.json): **141 Pins, 19.881 Vergleiche, Netzgruppen identisch**. Getrennte Masse-/Versorgungsnetze, X/Y und Serienpfade werden zusätzlich ausdrücklich geprüft. PDF/SVG/XML wurden erfolgreich exportiert. Das ist eine Dateikonsistenzprüfung, kein elektrischer Funktionstest.

[Originalmedien-Prüfung](originalmedien_pruefung.json): Alle 246 bereits im Quellenstand vorhandenen Dateien unter `photos/` und `docs/img/` sind bytegleich erhalten. Es wurden keine neuen Messungen ausgeführt, keine Fotos geändert oder erzeugt und keine Fehlerursache bewiesen. Der [alte Teilschaltplan](../schaltplan_110926/README.md) bleibt historisch erhalten.

## Unabhängige Endprüfung

Die Aktualisierung wurde an **GPT-6.1 Sol mit niedrigem Reasoning-Aufwand** delegiert und anschließend vom Hauptagenten gegen die Originalbelege geprüft. Korrigiert wurden die physische B20-R2-Zuordnung (statt eines ungesicherten R1/R2-Alias), veraltete Versorgungshinweise, Belegstellen sowie die Darstellung von TL082-Rückkopplung und T2-Serienpfad. Zusätzliche Detailansichten zeigen Anschlüsse und MCU-Arbeitsnummern lesbar.

Die [zweite Prüfung](unabhaengige_pruefung.json) verwendet eigene, aus den letzten Protokollkorrekturen abgeleitete Anschluss-Erwartungen direkt gegen die exportierte KiCad-XML-Netzliste – ohne Import des Generators oder seines Netzmodells. **59 Prüfungen bestanden**, darunter getrennte MCU-Eingänge, Versorgungen, Konsolenmasse und alle Widerstandsenden. [Prüfskript](pruefen_unabhaengig.py): `python docs/gesamtschaltplan_110926/pruefen_unabhaengig.py`. Zusätzlich sind **254 Original-/Referenzdateien** inklusive der bisherigen Messplan-Markierungen gegenüber dem Quellenstand bytegleich.

## Offen: Neuaufbau nach Messungen vom 16.11. abends

Neue Eingabe: [befunde_2026-11-16_abend.csv](befunde_2026-11-16_abend.csv) (AKT-064 bis AKT-082; Quelle: [Protokoll 16.11. abends](../LAUF_2026-11-14.md)). Die bestehende `befunde_2026-11-16.csv` bleibt unverändert. PDF, SVG, KiCad-Schaltplan, Netzlisten und Prüfnachweise sind **noch nicht neu erzeugt** und deshalb in folgenden Punkten überholt:

- Tabellenzeilen „Netzsignal X“, „B20-Widerstände“ und „Y, Quelle offen“; Netze TL082_OUT, X_VOR_100R, Y, N_P600-Ka/Kb; Bauteile R301/R302.

Beim Neuaufbau zu ändern:

- R1 (4,75 kΩ) ist der Serienwiderstand TL082 Pin 1 → Knoten N (= B20-R1b = B20-R2b = TL082-seitiges Pad des „1000“, Netz X_VOR_100R); danach 100 Ω → X.
- R2 (4,75 kΩ) liegt von X_VOR_100R nach 0VA (B20-R2a ↔ 0VA 0 Ω gemessen). AKT-059 bis AKT-061 und die R2-Zuordnung in AKT-024 sind damit ersetzt.
- Y (MCU-Arbeitsnummer 26) hängt über ≈ 1 kΩ an P600 Kontakt 1; Widerstand Y → 0VA (1,883 kΩ eingebaut) mit offenem Einzelwert; keine direkte Verbindung zu TL082 Pin 1/Pin 7 oder B20-R1b.
- P600 Kontakt 2 ↔ +5VA ist gemessen (0 Ω, AKT-077); „Y = Temperatureingang“ ist Ableitung, keine Kupferverbindung. Zuordnung „Kontakt 1/2“ zu P600-Ka/Kb ist offen.
- Nachtrag 16.11. spätabends (AKT-077 bis AKT-082, Quelle: [Protokoll](../LAUF_2026-11-14.md), „16.11. spätabends“): Neue Gruppe „Tacho-Kanal“: P4 TACHO → ≈ 1,1 kΩ → ADM485 Pin 7; ADM485 Pin 6 = Vergleichspegel (12,94 kΩ von P4 TACHO); ADM485 Pin 1 → Kathode OC06 (0 Ω, 11.11.); ADM485 Pin 5 = LM2903 Pin 4 = 0 V Konsole (0 Ω zu P2.7). Der Ableitzweig 01C/4751/4751 nach Masse ist nur als Fotoverlauf (F) belegt. Offen: OC06 Transistorseite → MCU-Pin, LM2903 Komparator A, Weg des Tachosignals zu P2.9.

Der Neuaufbau ist offen, weil KiCad CLI und PyMuPDF in dieser Umgebung fehlen. `erzeugen.py` liest bisher nur `befunde_2026-11-16.csv` ein und muss die neue Datei noch einbinden; danach ist `pruefen_unabhaengig.py` (Erwartungen zu X-Pfad, B20-Widerständen, Y) anzupassen.
