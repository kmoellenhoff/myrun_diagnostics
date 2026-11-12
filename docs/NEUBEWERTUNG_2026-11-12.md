# Neubewertung 12.11.2026 (abends)

Ersetzt die Gewichtung aus `NEUBEWERTUNG_2026-11-11.md`. Tags: [M] gemessen, [O] beobachtet, [I] gefolgert, [H] Hypothese.

## 1. Was jetzt ausgeschlossen bzw. unauffällig ist
Motor (Wicklung 1,5 Ω, Generatorspannung, Lauf 95 s am 07.11.), Encoder-Mechanik, Q2/D3 statisch, Gate-Netz, **Motorstromkreis ohne Relais/Sicherung** (L+ und L− je 0 Ω), Shunts (nachgelötet), B18/B19-Teiler statisch, Thermoschalter und Kabel (Wackeltest o. B.), Not-Stopp-Schlüssel (eigener Code 1001), Enable-Auswertung LM2903 → OC04 (6 V Reserve zur Schwelle), OC04 (Test B wie OC05), **alle Elkos** inkl. Zwischenkreis (100 Hz: 475 µF, tan δ 0,08).

## 2. Was übrig bleibt (Beobachtungen, die eine Erklärung brauchen)
1. **err 4 (OU, Überspannung) auch bei 0 V am Motor** (08.11. 13:26) und nach ≈ 1 s Lauf (10.11. 13:34) [O].
2. **904: GIRT treibt nicht** trotz Enable, PWM-Sollwert an P2.6 (≈ 0,5 V Mittel, 08.11.) und `QSRunning` [M/O]; die GIRT meldet ihren Fehler 1,3 s **vor** der Konsole (08.11.) [M].
3. **Läufe gelangen nur gelegentlich**, auffällig oft nach langer Pause bzw. vollständig entladenem Gerät (07.11. 17:18, 11.11. 10:33 nach der Nacht) [O, zu prüfen].
4. err 9: die Enable-Spannung (rosa/P2.5) war im **Fehlerzustand** 0 V. Da die Konsole nach jedem GIRT-Fehler EM_POWENA abschaltet (08.11.), ist offen, ob das Ursache oder Folge war [I].
5. **Die Zwischenkreisspannung wurde nie im Betrieb gemessen.** Der Elko ist nur für 400 V ausgelegt [O].

## 3. Hypothese (Hauptverdacht)
**Die Leistungsversorgung der GIRT ist beim Start nicht stabil: Vorlade-/Inrush-Relais F27 (Schrack RT334024, 24 V) mit Vorwiderstand 68 Ω (7 W) und/oder die PFC-Regelung der Zwischenkreisspannung.** [H]
- Schließt F27 nicht oder schlecht (verschmorte Kontakte, schwache Spulenspannung, Lötstelle), läuft die Leistung über 68 Ω. Im Leerlauf ist der Zwischenkreis trotzdem voll; unter Last bricht er ein, die PFC-Regelung schwingt → **OU (err 4)** bzw. die GIRT verweigert den Antrieb (904). Ein schwacher Kontakt erklärt die Zufälligkeit und die Abhängigkeit von Temperatur/Pause.
- F27 war schon am 08.11. verdächtig und wurde nachgelötet; die Kontakte selbst wurden nie geprüft.
- Alternativ misst die GIRT die Zwischenkreisspannung falsch (Teilerkette B10/B18, Kriechströme durch Salzreste) → OU-Fehlauslösung.

Zweiter Strang: **Ablauf Konsole ↔ GIRT** (wer schaltet zuerst ab bei err 9 / 902). Nur mit feiner Zeitauflösung klärbar.

## 4. Messplan (Reihenfolge)
**A – stromlos, Relais F27**
1. Kontaktpins finden: über den Kontakt misst man **≈ 68 Ω** (parallel liegender Vorwiderstand); Spulenpins zeigen ≈ 1–1,5 kΩ (Datenblatt RT3 24 V prüfen).
2. Spule mit 24 V (Netzteil oder 3 × 9-V-Block in Reihe) ansteuern, Platine sonst stromlos: Kontakt muss auf **< 0,1–0,2 Ω** fallen, 20 × wiederholen, dabei klopfen. Springende Werte oder > 1 Ω → Relais tauschen.

**B – im Betrieb, geklemmt (Netzpotential!)** — Klemmen nur bei entladenem Elko setzen, 600-V-Bereich, nichts anfassen
1. **Zwischenkreis L+ (eckiges Pad) gegen 0VA (rundes Pad), MAX/MIN**: Einschalten, 1 min Leerlauf, Start, Lauf/Abbruch. Erwartet ≈ 380–395 V stabil. Über ≈ 400 V oder starke Einbrüche → PFC/Relais.
2. **Spannung über dem 68-Ω-Widerstand** beim Einschalten und Start: muss nach ≈ 1–2 s auf ≈ 0 V gehen (Relais zu). Bleibt Spannung stehen → F27.
3. Ohr/Handy-Video: klickt F27 ≈ 1–2 s nach dem Einschalten?

**C – Zeitablauf** (sicher, Konsolenseite)
`--listen-poll` mit 1-s-Raster (DUMPIO/STATUS), parallel Handyvideo auf STS1/STS2 und Multimeter MIN an der rosa Ader. Zeigt, ob EM_POWENA vor oder nach dem STS2-Blinken fällt.

**D – Fehlstart 904 am Gate-Treiber** (geklemmt, Netzpotential): IN+ (Pad A) und OUT (Pad E) gegen Pad B, Hz/Duty.

**E – Protokoll jeder Einschaltung**: kalt/warm, Elko entladen ja/nein, Dauer bis Fehler, Displaycode, STS2-Blinkzahl. Bestätigt oder widerlegt Beobachtung 2.3.

Letzte Option: Tausch-Test mit einer zweiten GIRT S6T30 oder Konsole.
