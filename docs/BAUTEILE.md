# Bauteilregister GIRT S6T30 (Platine ECS2458-6)

Stand 27.11.2026. Dieses Register ordnet die verschiedenen Namenssysteme des Repos einander zu. Es benennt nichts um und ersetzt weder die [Platinenübersicht](GIRT_Platinen_Uebersicht.pdf) noch den [Schaltplan](schaltplan/README.md); es führt nur zusammen, was die Quellen belegen (Übersicht, `schaltplan/bauteile*.csv`, `schaltplan/netze.csv`, [HARDWARE.md](HARDWARE.md), [REPARATUR.md](REPARATUR.md), [Fotoatlas](fotoatlas/README.md), [MCU-Pins](mcu_pins/README.md)). Eine Zuordnung zwischen Schaltplan-Referenz und F-/B-ID steht nur, wenn eine Quelle sie herstellt (Feldangabe, Repository-ID oder gleicher Aufdruck); sonst steht „–“ bzw. „Zuordnung offen“.

Belegstufen: **M** gemessen · **F** Foto/Aufdruck/Beobachtung (in [HARDWARE.md](HARDWARE.md) „[O]“) · **I** abgeleitet · **H** Hypothese. Steht in „Funktion“ eine Belegangabe, gilt sie für den Text davor; „ermittelt“ = M/F, „vermutet“ = I/H. Lagen sind Foto-Lagen (±1 Feld). Die Netzseite der Platine ist nicht galvanisch getrennt, siehe Sicherheitshinweise in [HARDWARE.md](HARDWARE.md).

## Bezeichnungen

1. **Raster A–L / 1–6** (Feld): eigenes Koordinatenraster auf den Übersichtsfotos vom 08.11.; ein Feld meint auf Vorder- und Rückseite dieselbe Stelle. Kein Aufdruck.
2. **Bereichs-IDs F1–F33 (Vorderseite) und B1–B21 (Rückseite)**: eigene Nummern aus der Platinenübersicht, keine Herstelleraufdrucke. B12 existiert nicht. *Verwechslungsgefahr:* **F27** ist das Relais RT334024, **F28** der Bereich der Sicherung FUSE MOT; **B10** ist die Netzerfassung (Bereich, Feld J6); „B10-…“ in den Repository-IDs des Schaltplans nennt dieselbe elektrische Gruppe, sagt aber nicht, wo R601/R602/C602 liegen (Feld E6/D6). Außerdem können ID und Feld gleich lauten und trotzdem Verschiedenes meinen: die ID **B5** (P2-Lötpads) liegt im Feld **F1**, das Feld **B5** enthält dagegen Q2/P600 (F33, F15, B21).
3. **Schaltplan-Referenzen** (R601, C602, U602, K501, TH501, D901 …) in [docs/schaltplan/](schaltplan/README.md): beim Rekonstruieren vergeben, **stehen nicht auf der Platine**. C602 ist laut Befund vom 21.11. eine neu vergebene CAD-Referenz. Die Nummernkreise ähneln Bestückungsdruck (z. B. gedruckt P600/P601/P602, C400/C401, U702 gegenüber Schaltplan R601, U601, C601); nicht verwechseln. In `netze.csv` sind Namen wie „B18-P2“ oder „B10-R1“ Pad-/Bauteilnamen der Rekonstruktion, nicht der Steckverbinder P2.
4. **Aufdrucke**: Bestückungsdruck der Platine (z. B. FUSE MOT, P2, P4, P600, STS2, C400) und SMD-Wertcodes. Letztere: 2212 = 22,1 kΩ, 1001 = 1 kΩ, 4753 = 475 kΩ (Original-Messketten), 4703 = 470 kΩ (neue Teile im B10-Umbau), 4752 = 47,5 kΩ, 4702 = 47 kΩ, 1003 = 100 kΩ, 1004 = 1 MΩ, 3922 = 39,2 kΩ, 4750 = 475 Ω, 2211 = 2,21 kΩ, 4751 = 4,75 kΩ.
5. **Eigene Knotennamen und MCU-Arbeitsnummern**: J, X, Y, 0VA, L+ … (Abschnitt „Knoten“) sowie die MCU-Anschlüsse 1–32, gezählt ab Gehäusemarke gegen den Uhrzeigersinn. Das sind Arbeitsnummern, keine Datenblatt-Pins (MCU-Typ unbekannt): [mcu_pins/README.md](mcu_pins/README.md).

## Vorderseite (Bauteilseite)

| Feld | Bereichs-ID | Aufdruck/Typ | Schaltplan-Ref. | Funktion | Beleg | Bemerkung |
|---|---|---|---|---|---|---|
| A1 | F1 | DC MOTOR (Flachstecker L+ orange, L− grau) | – (Netze L+/L−; M1 = Motor selbst, siehe unten) | ermittelt: Anschluss Bandmotor, 12,4 V DC bei 1,2 km/h unbelastet | M/F | nachgelötet; Pads auf der Rückseite = B13 |
| A2 | F2 | Ringkerndrossel (Motorausgang) | – | ermittelt: Drossel im Bereich Motorausgang (Lage); Funktion nicht untersucht | F | Zuordnung zu F22 (zweiter Ringkern) offen |
| E1 | F3 | P4 (4-polig: TACHO / 0V / +12V / 0V) | J204 | ermittelt: Anschluss Drehzahlsensor (Gabellichtschranke „1041/NXO“) | M/F | Sensor von Bürstenstaub gereinigt (13.11.); Schaltplan: TACHO/0V |
| F1 | F4 | P2 (18-polig, 2 × 9) | J201 (nur vermessene Pins) | ermittelt: Konsolenanschluss; Pinbelegung teils gemessen, teils aus Handbuch ([Man]) | M | gereinigt, nachgelötet; Lötpads = B5 (nicht Feld B5) |
| H1 | F5 | P3 (3 Pads neben der Erdschraube) | – | vermutet: Höhen-Poti-Anschluss | I | Übersicht nennt „P3 Poti“, HARDWARE.md „Zweck nicht bestätigt“; gereinigt |
| J1 | F6 | UP/DOWN | – | ermittelt: 230 V AC zum Höhenmotor über Relais und FUSE MOT | F/I | Pads gereinigt, nachgelötet; Rückseite = B15 |
| L1 | F7 | AC LINE | Netze AC_L / AC_N (Anschlussnamen) | ermittelt: Netzeingang 230 V AC | F | HARDWARE.md nennt „Bezeichnung nicht erfasst“, Übersicht/Schaltplan „AC LINE“; Rückseite = B16 |
| C2 | F8 | 2 × 74ACT14, LM2903, ADM485, 2 × 78L05 | U606 (nur ADM485, Teilanschlüsse); LM2903/74ACT14 in `netze.csv` nur als Pins ohne Ref. | ermittelt: Logikspalte Konsole ↔ MCU; vermutet: ADM485 als Tacho-Aufbereitung (I), LM2903 als Komparator (F) | F/I | Typen aus Aufdrucken; in HARDWARE.md zusätzlich „2 × SOT-223-Regler“ (siehe F16) |
| C2 | F9 | 8 × VO617A-8 (OC01–OC08; OC01 und OC07 um 180° gedreht) | U603 (OC04), U604 (OC05), U607 (OC06) | ermittelt: Optokoppler, Trennung Konsole ↔ Netzseite; Durchgang OC04-Emitter → MCU 12 („Enable“), OC05-Emitter → MCU 17/18 („PWM“) (M); Funktion im Betrieb nicht bewiesen (I); OC06 Ausgang/MCU-Pin offen | F/M/I | OC01–OC03, OC07, OC08 ohne Schaltplan-Ref. |
| B3 | F10 | P602 (14-polig, blau) | – | – (Funktion nicht belegt) | F | Referenzpunkt in den MCU-Fotos |
| B3 | F11 | P601 (RST / 0VA) | – (Netz 0VA) | ermittelt: Aufdruck RST/0VA; Funktion nicht untersucht | F | |
| C4 | F12 | MCU QFP-32, Typ nicht identifiziert | U601 (Arbeitsnummern, kein Datenblatt) | ermittelt: Mikrocontroller der Netzseite; Netz-Zuordnung einzelner Anschlüsse siehe [mcu_pins](mcu_pins/README.md) | F/M | Pin-Nummern nur Arbeitsnummern 1–32 |
| C4 | F13 | SO-8 („24C32?“) | – | vermutet: EEPROM 24C32 (Parameter) | H | Widerspruch: HARDWARE.md nennt „EEPROM 24C32“ ohne Vorbehalt, Übersicht mit Fragezeichen |
| C4 | F14 | P70 (6-polig, Debug) | – (Netz P70 = MCU 13) | ermittelt: Debug-Buchse, Netzseite, nicht anschließen; Rolle von MCU 13 offen | F/M | Rückseite = B2 |
| B5 | F15 | P600 (NTC 10 kΩ, an Q2 verschraubt) | TH501 (P600 Ka/Kb) | ermittelt: Temperaturfühler Q2; abgezogen 11,28 kΩ, gesteckt 3,11/2,47 kΩ in-circuit | M | Zuordnung der Pins Ka/Kb offen (Schaltplan README) |
| D3 | F16 | 2 × SOT-223, CPC1017N, 47 µF | – | ermittelt: CPC1017N (OptoMOS, Potentialtrennung) und zwei Regler; SOT-223-Typ nicht identifiziert | F | Klasse Hilfsspannung |
| E2 | F17 | Übertrager „ETI349X4 2110 FALCO“ | – | ermittelt: Übertrager des Hilfsnetzteils; vermutet: Flyback mit FSGM300N (DIP-8) | F/I | Widerspruch: HARDWARE.md Abschnitt 2 schreibt „ETI1349X4“, Abschnitt 9 und Übersicht „ETI349X4“ (Aufdruck vor Verwendung prüfen) |
| G2 | F18 | 4 × 330 µF, Thermistor RT700 | – | ermittelt: Elkos und Thermistor der Hilfsspannung; Funktion von RT700 nicht untersucht | F | RT700 = Bestückungsdruck |
| D2 | F19 | 47-µF-Elkos | – | – | F | |
| E3 | F20 | U702 (SO-8), C727, C703 | – | – (Funktion nicht belegt) | F | U702, C727, C703 = Bestückungsdruck, keine Schaltplan-Refs |
| E4 | F21 | DC-Link-Elko EPCOS B43630-C9567-M7, 560 µF/400 V, Aufkleber S890A16E | – (Netz L+: „Zwischenkreis-Elko.+“) | ermittelt: Zwischenkreis, Standby ca. 316–324 V; bis ca. 380 V DC im Betrieb | M/F | Vor Arbeiten entladen |
| G3 | F22 | großer Ringkern (Drossel) | – | vermutet: Drossel im Gleichrichter-/PFC-Zweig | I | Lage F/I; Block „Ringkern“ im Blockdiagramm |
| F3 | F23 | P400 (0V24 / +24V) | TP502 (+24V), TP503 (0V24) | ermittelt: 24-V-Anschluss/Testpunkte (Hilfsspannung); 0V24 = 0VA (0 Ω) | M/F | Zuordnung nur über gleichen Aufdruck; ob TP502/TP503 genau diese Pads sind, offen |
| I2 | F24 | Relais Schrack (orange) | – | vermutet: Relais der Höhenverstellung (HARDWARE.md nennt „Schrack PE014012“ in der Relaisgruppe UP/DOWN) | I | Zuordnung des Typs zu F24 nicht ausdrücklich belegt |
| I2 | F25 | 2 × Relais Panasonic (ALQ3F12, 12 V, 10 A) | – | ermittelt: Relais; vermutet: UP/DOWN | F/I | Typ aus HARDWARE.md „3 × ALQ3F12“ (F25 + F26 nach Anzahl); einzelne Kontakte nicht durchgemessen |
| J4 | F26 | Relais Panasonic (ALQ3F12) | – | ermittelt: Relais; vermutet: Freigabe/UP/DOWN | F/I | wie F25 |
| I4 | F27 | Relais Schrack RT334024 (24-V-Spule, 16 A) + weißer 7-W-Widerstand 68 Ω | K501 (Repository-ID „F27 RT334024“) | ermittelt: Einschaltbegrenzung/Hauptrelais; Spule 1,41 kΩ, Spulenplus +24 V, Kontaktgruppe 68,4 Ω in-circuit (M); Ansteuerung durch MCU 24 über 1 kΩ und T4 (Q601) (M, Durchgang); Rückmeldung nicht nachgewiesen | M/F | **nicht** FUSE MOT (F28). RT334024 + 68 Ω nachgelötet. Die 68 Ω haben keine Schaltplan-Ref. |
| J2 | F28 | FUSE MOT, Feinsicherung 5 × 20 mm, T4A träge, 250 V | – (nicht im Schaltplan) | ermittelt: Absicherung des 230-V-Zweigs zum Höhenmotor | F/M | **Defekt 2**: fehlte (Glaskörper weg), ersetzt durch T4A/250 V Keramik; Test bis 12 % Steigung bestanden. Nachbarn: C400/C401 (Druck), F24/F25, F6 |
| L4 | F29 | Netzfilter (X2 1 µF, 3 Drosseln, Varistoren RV300/RV301) | – | ermittelt: EMV-Filter am Netzeingang | F | **Nicht C601** (Schaltplan-„X-Filterkondensator“ am Signalknoten X, nicht der Netz-X2); Rückseite = B14 |
| F6 | F30 | Kühlkörper mit Q2, D3, D2, Q1 (Brückengleichrichter am rechten Kühlkörper) | D3 (Freilaufdiode) | ermittelt: Leistungshalbleiter (Chopper Q2 + D3, Gleichrichter/PFC Q1, D2); Kontakte nachgelötet | F/M | Widerspruch: bauteile.csv gibt für D3 Feld B5, Übersicht (F30) F6. Q1 und D2 ohne Schaltplan-Ref. Zeilen 5–6 vom Kühlkörper verdeckt |
| D5 | F31 | Testpunkte 0VA / +5VA | TP501 (+5VA) | ermittelt: Testpunkte Logikmasse und +5 V | M/F | 0VA hat keine eigene TP-Ref. (TP503 = 0V24 ist 0VA-Alias) |
| I2 | F32 | Testpunkte +12VISO / 0VISO | – (nicht im Schaltplan) | vermutet: potentialgetrennte +12-V-Seite (Name) | H | Aufdruck gelesen, Funktion nicht untersucht |
| B5 | F33 | Q2 (MOSFET, an Kühlkörper geklemmt, neben P600) | Q2 | ermittelt: Schalttransistor des Motor-Choppers (Gate über 22 Ω, Source 0VA, Drain L−); Body-Diode 0,444 V; MOSFET-Typ nicht identifiziert | M/F | Beine/Treiber auf der Rückseite = B21; Kontakte nachgelötet |

## Rückseite (Lötseite)

| Feld | Bereichs-ID | Aufdruck/Typ | Schaltplan-Ref. | Funktion | Beleg | Bemerkung |
|---|---|---|---|---|---|---|
| C5 | B1 | LEDs LINE (blau), +5V (grün), STS1 (grün), STS2 (rot) | – | ermittelt: Status-LEDs; STS2 blinkt Fehlercodes (8×/4×); Zuordnung zu Treibercodes vermutet (H, siehe [FEHLERCODES.md](FEHLERCODES.md)) | F/H | „zwischen D3 und Q2“ (HARDWARE.md) |
| C4 | B2 | 6 Pads | – | ermittelt: Gegenstück zu P70 (F14) | F | |
| F6 | B3 | SO-20, Aufdruck „L4981AP“ | U301 (Typ „L4981AD“, Feld „E6“) | ermittelt: PFC-Regler; Anschluss 14 (VFEED) ↔ B19 (M, Durchgang), Anschluss 15 ↔ T3/U401 und Anschluss 19 ↔ Treiber U201 laut netze.csv | F/M | Widersprüche: Typ AP (Übersicht, REPARATUR.md) ↔ AD (bauteile.csv, HARDWARE.md); Feld F6 (Übersicht) ↔ E6 (bauteile.csv), REPARATUR.md „E/F6“. Zuordnung über Typ L4981 |
| D6 | B4 | 2 × SO-8, darunter TL082 | U602 (TL082I) | ermittelt: Puffer des Netzspannungs-Messsignals (Kanal A Spannungsfolger, Eingang Pin 3 an J, Kanal B ungenutzt) | F/M | Typ des zweiten SO-8 nicht belegt; Zuordnung über Typ TL082 |
| F1 | B5 | P2-Lötpads | J201 (Gegenstück zu F4) | ermittelt: Lötseite des Konsolenanschlusses | F/M | **ID B5, nicht Feld B5** (Feld B5 = Q2-Bereich) |
| F2 | B6 | 2 × DPAK-Bauteil | – | – (Funktion nicht belegt) | F | Klasse Hilfsspannung |
| H4 | B7 | 4 × R020 (Shunt 0,02 Ω) | – | ermittelt: Shunt-Widerstände, 2-Draht nicht messbar; vermutet: Strommessung PFC (I) | F/I | HARDWARE.md nennt zusätzlich 4 × R020 auf der Vorderseite nahe DC MOTOR; dafür gibt es in der Übersicht keine F-ID (Lücke) |
| H3 | B8 | SOT-223 | – | – (Funktion nicht belegt) | F | nicht TP604/F27-Tab (anderes Feld, I4) |
| K2 | B9 | 2 × „471“ SMD | – | – (Bauteilart offen: 471 als Widerstand 470 Ω oder Kondensator 470 pF) | F | **nicht C602** (anderes Feld K2 statt E6) |
| J6 | B10 | Netzerfassung L/N: Original je Seite 2 × 475 kΩ („4753“) + Diode (M7-Klasse?); Umbau je Seite 2 × 470 kΩ („4703“, 1206) + US1M | Original: R401–R404, D401, D402 (Repository-ID „B10-…“, Feld J6); Umbau (Ist-Blatt): R901–R904, D901, D902 | ermittelt: Netzspannungserfassung, speist über J den TL082-Puffer; Dioden 0,497/0,499 V (Original, M) | M/F | Umbau am 21.11. eingebaut (neue Teile auf alten Pads, zusätzliche Litzenbrücken); Zuordnung der R9xx/D9xx zu B10 über REPARATUR.md. J-Zweig R601/R602/C602 liegt **nicht** in J6 (siehe unten) |
| B3 | B11 | Testpad-Reihe | – | – | F | |
| A1 | B13 | DC MOTOR-Pads | – | ermittelt: Lötseite von F1 | F | nachgelötet |
| L4 | B14 | Netz-/Filter-Pads | – | ermittelt: Lötseite des Netzfilters (F29) | F | |
| J1 | B15 | UP/DOWN-Pads | – | ermittelt: Lötseite von F6 | F | gereinigt, nachgelötet |
| L1 | B16 | AC LINE-Pads | – | ermittelt: Lötseite von F7 | F | |
| E3 | B17 | SMD „4702“ (47 kΩ), „47R0“ (47 Ω) | – | – (Funktion nicht belegt) | F | Zuordnung zu Schaltplan-Refs offen |
| E5 | B18 | Spannungsteiler 1 MΩ (1004) + 1 MΩ (1004) + 475 kΩ (4753) | R101, R102, R103 (Repository-ID „B18-…“) | ermittelt: Kette L+ → … → Pad B → L4981 Anschluss 14 VFEED (Verbindung M); vermutet: Rückführung des PFC-Reglers (I) | M/I | Funktion nicht weiter verfolgt; „P1/P2“ in den Aliasen sind Pad-Namen von B18, nicht Steckverbinder |
| E6 | B19 | Widerstandsblock: 2 × 100 kΩ (1003), 39,2 kΩ (3922) nach 0VA, 475 Ω (4750), 2 × 1 MΩ (1004) | R104–R109 (Repository-ID „B19-…“) | ermittelt: Fortsetzung der VFEED-Kette bis L4981 Anschluss 14; 39,2 kΩ nach 0VA; rechnerisch ca. 1,44 % (Block „PFC-Rückführung“) | M/I | Feld E6 wie C602 und U301 (csv); nicht untereinander verwechseln |
| E6 | B20 | Reihe aus 4 Widerständen + SOT-23 (NPN-ähnlich) | R301–R304, U401 („T3“, Typ offen) | ermittelt: R301/R302 (4,75 kΩ, „4751“) als Teiler zwischen TL082-Ausgang und X; T3: Kollektor an L4981 Anschluss 15, Basis über 2,21 kΩ von MCU 11 („PFC-Sperre“) (M, Durchgang); vermutet: Transistor als PFC-Sperre (I) | M/I | Typ NPN-ähnlich [H]; Zweck von R303/R304 offen |
| B5 | B21 | Q2-Beine G/D/S (3 Pads, 2 Isolierschlitze), 22 Ω („220“), Treiber SOT-23-5 | R201 (22 Ω), U201 (Treiber, Kandidat FAN3100C, Aufdruck „100CA“), U202 („1P“, NPN), R202 (2211); nur über Feld B5: R203 (1001), R204 (4752) | ermittelt: Gatepfad von Q2 (22,2 Ω); Treiber-Ausgang an Q2-Gate; vermutet: SOT-23-5 = Gate-Treiber (H, Typ nur Kandidat) | M/H | R203/R204 stehen in bauteile.csv nur mit Feld B5 (keine Q2-Repository-ID): Zuordnung schwächer. Q2 selbst = F33 |

### Schaltplan-Bauteile ohne eigene F-/B-ID

| Feld | Bereichs-ID | Aufdruck/Typ | Schaltplan-Ref. | Funktion | Beleg | Bemerkung |
|---|---|---|---|---|---|---|
| E6 (±1, Grenze D6/E6) | – | SMD-Keramikkondensator 0603, ca. 470 pF; **kein Aufdruck** | **C602** | ermittelt: parallel zu 2212 zwischen Knoten J und 0VA; vermutet: Tiefpass ca. 16 kHz (Entstörung des Messsignals) | M/F; I | **Schaltplan-Referenz, kein Aufdruck auf der Platine; erkennbar neben dem Widerstand „2212“.** **Defekt 1**: innerer Nebenschluss, ersetzt durch 471 pF (460 pF gemessen). Feld: bauteile.csv „E6 / neben 2212“, Übersicht E6; der Fotoatlas führt B10 auf J6 – zwei verschiedene Orte (B10 und J-Zweig sind nur elektrisch über J verbunden) |
| E6 / D6 (neben C602) | – | SMD „2212“ (22,1 kΩ) | R601 (Repository-ID „B10-2212“) | ermittelt: J → 0VA | M/F | Zuordnung zu einer F-/B-ID offen: Repository-ID „B10-…“ benennt die elektrische Gruppe, die Lage ist nicht J6 |
| E6 / D6 (neben C602) | – | SMD „1001“ (1 kΩ) | R602 (Repository-ID „B10-1001“) | ermittelt: J → TL082 Pin 3 | M/F | wie R601 |
| – | – | SMD „1000“ (100 Ω) | R603 (Repository-ID „Netzsignal-1000“) | ermittelt: Reihenwiderstand vor Knoten X | M | Zuordnung offen |
| – | – | Kondensator, Wert offen | C601 | ermittelt: Knoten X → 0VA (Filterung des MCU-Eingangs) | M | Zuordnung offen; **nicht der X2-Kondensator im Netzfilter (F29)** |
| – | – | LD3N (Aufdruck laut Repository-ID) | U605 | ermittelt: an Knoten Y (O → Y, L → 0VA, R → +5VA); vermutet: Klemm-/Schutzstufe (H) | M/H | Innenstruktur offen; Zuordnung offen |
| – | – | SMD „2211“ (2,21 kΩ), „01C“ (10 kΩ), „1001“ (1 kΩ) | R604, R605, R606 | ermittelt: R604 T3-Basis ← MCU 11; R605 Pull-up 10 kΩ nach +5VA; R606 MCU 24 → T4-Basis | M | Zuordnung offen (in der Nähe von T3/T4 geführt) |
| – | – | „1P“-Transistor T4 (NPN, Typ offen) | Q601 | ermittelt: Ansteuerung der Spule von F27 (Kollektor = Spulenminus, Emitter 0VA); Funktion unter Last offen | M/I | Zuordnung zu K501/F27 funktional, Lage offen |
| – | – | SMD „4750“ (475 Ω), „2211“ (2,21 kΩ) | R607, R608 | ermittelt: Reihenkette zwischen „1P“-Anschluss L (U202) und T2-Kollektor | M | Zuordnung offen |
| – | – | Transistor T2 (NPN, Typ offen) | Q602 | ermittelt: Emitter 0VA, Basis/Kollektor über R607/R608; Funktion offen | M | Ansteuerung nicht lokalisiert; Zuordnung offen |
| – | – | SOT-223 neben F27 (Tab = +24 V) | TP604 | ermittelt: Tab auf +24 V und an Spulenplus von K501 | M | Typ des SOT-223 offen; nicht B8 (anderes Feld) |
| – | – | Motor-Thermoschalter (schwarzer 2-pol. Zwischenstecker am Motorkabel) | SW501 | ermittelt: kalt geschlossen (≈ 0 Ω); in der Notlinie über P2 Pin 5 | M | Bauteil im Motor, nicht auf der Platine |
| – | – | Bürsten-DC-Motor | M1 | ermittelt: Wicklung 1,5–1,6 Ω, 16 Rotorpositionen | M | Bauteil extern; Anschluss = F1/B13 |

## Knoten (eigene Namen in `schaltplan/netze.csv`)

Nur soweit in [netze.csv](schaltplan/netze.csv), [HARDWARE.md](HARDWARE.md) oder [mcu_pins](mcu_pins/README.md) belegt. Pin-Kürzel in den CAD-Pins: A Anode, K Kathode, C Kollektor, E Emitter, B Basis (O/L/R sind lokale Anschlussnamen des Messprotokolls). Ein Knoten „K“ ist in `netze.csv` nicht als Netz geführt (nur als Pin-Kürzel „.K“ = Kathode).

| Knoten | Bedeutung | Beleg |
|---|---|---|
| J (Netz „B10_KATHODEN“) | gemeinsame Kathoden der Netzzweige L/N; Messknoten: nach 0VA über 22,1 kΩ („2212“, R601) und C602, über 1 kΩ („1001“, R602) zu TL082 Pin 3. ≈ 4,9 V DC bei ≈ 238 V Netz; nach der Reparatur 4,966 V | M |
| N_J_1001R | Seite des 1-kΩ-Widerstands R602 am TL082-Eingang (Pin 3) | M |
| X | Netzsignal nach TL082 → 4,75-kΩ-Teiler → 100 Ω; C601 nach 0VA; MCU-Arbeitsnummer 28 | M/F |
| X_VOR_100R | Knoten zwischen 4,75-kΩ-Teiler und 100 Ω (R603) | M |
| Y | getrennt von X; LD3N (U605) → Y; MCU-Arbeitsnummer 26; Quelle offen | M |
| 0VA | Bezug der Netzseite/Logik (DC−), nicht galvanisch getrennt; 0V24 und weitere Pins sind Aliase (0 Ω) | M |
| 0V24 | 24-V-Rückleiter, gleich 0VA (0 Ω); Testpunkt TP503, Aufdruck an P400 | M/F |
| 0V_KONSOLE | Bezug der Konsolenseite (P2 Pin 7/8, P4 0V, OC05/LM2903/ADM485-Bezug); getrennt von 0VA | M |
| +5VA | 5-V-Versorgung der Netzseite (TP501, MCU Arbeitsnummer 8, Kollektoren OC04/OC05) | M |
| +24V | 24-V-Hilfsspannung (TP502, Spulenplus K501, SOT-223-Tab TP604) | M |
| +12VA / −12VA | Versorgung des TL082 (Pin 8 / Pin 4) | M |
| L+ / L− | L+: Zwischenkreis-Pluspol, DC MOTOR L+ und Beginn der PFC-Rückführungskette (B18); L−: DC MOTOR L− und Drain von Q2 | M |
| AC_L / AC_N | Netzanschluss der beiden B10-Zweige | M |
| VFEED | PFC-Rückführung: B19-Block → L4981 Anschluss 14 | M |
| GATE, RG_U, DRV_C | Gatepfad von Q2: Q2-Gate ← R201 (22 Ω) ← Treiber U201; Treiber-C ↔ L4981 Anschluss 19 | M |
| ENABLE | OC04-Emitter ↔ MCU Arbeitsnummer 12 | M |
| PWM | OC05-Emitter ↔ MCU Arbeitsnummer 17/18 | M |
| PFC_CTRL | MCU Arbeitsnummer 11 → R604 (2,21 kΩ) → T3-Basis, Pull-up R605 | M |
| F27_CTRL | MCU Arbeitsnummer 24 → R606 (1 kΩ) → T4-Basis (Q601) | M |

Die Zuordnung der MCU-Arbeitsnummern 1–32 steht in [mcu_pins/README.md](mcu_pins/README.md). Sie gilt nur für die dortige Zählung, nicht für Datenblatt-Pins.
