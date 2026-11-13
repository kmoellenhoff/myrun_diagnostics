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

## Nachtrag 22:56 – Folgefehler durch unvollständigen Reset; Treiber-Eingänge
- **Idee des Nutzers [H]:** Viele Fehlstarts sind Folgefehler. Nach einem echten Fehler bleibt die GIRT verriegelt, bis sie vollständig stromlos ist. Da sich der Zwischenkreis nach Netz-Aus nur langsam entlädt (gemessen: Elko braucht lange, Restspannung), läuft die Hilfsversorgung/MCU nach dem Ausschalten womöglich weiter → „Neustart“ ist kein Reset. Passt zu: Fehlstart 15:08 ohne vorheriges Entladen; gute Läufe nur nach langer Pause.
  - Prüfen: nach Netz-Aus Zeit messen, bis LINE, +5V und STS1 erlöschen. Ab jetzt nur noch **Kaltstarts** werten (alle LEDs aus, Elko < 5 V) und jeweils den **ersten** Fehler nach einem Kaltstart notieren.
- Bisherige „erste“ Fehler nach Lauf: 07.11. (95 s gut, danach 8×), 10.11. 13:34 (≈ 1 s, err 4), 11.11. 10:33 (10 s, err 9). Wechselnde Codes sprechen gegen den Speed-Sensor als alleinige Ursache (dann wäre durchgehend 08 zu erwarten) **[I]**; er ist aber nicht ausgeschlossen. Prüfen: Encoder (`@RENC#`) bei langsam von Hand gedrehtem Band und im nächsten Lauf im 1-s-Raster.
- **Hinweis ChatGPT [I]:** Beim FAN3100C ist OUT nur high, wenn IN+ (Pad A) high **und** IN− (Pad D) low ist. IN− kann ein Sperr-/Schutzeingang sein (z. B. Überstromabschaltung über TL082). Stromlos klären: Wohin führen Pad A und Pad D (bis zum nächsten Bauteil)? Außerdem offener Zweig VDD (Pad C) → 2,21 kΩ → „1P“ (SOT-23, Markierung passt zu MMBT2222A) → 0VA.

## Nachtrag 23:03 – Freigabe von Q2 (Schaltungsentwurf ChatGPT aus Makros, Branch 110926)
VDD (Pad C) → 2,21 kΩ → Knoten N → 1 kΩ → IN+ (Pad A); IN+ → 47,5 kΩ → 0VA; „1P“ (NPN?) Kollektor an N, Emitter an 0VA, Basis 1P.L Herkunft offen. Pad D (IN−?) läuft ins Leiterbahnbündel, Ende offen.
Lesart **[H]**: IN+ wird über VDD hochgezogen; leitet 1P, zieht er IN+ auf low → Treiber gesperrt. Ein dauerhaft leitender 1P (Basis angesteuert oder C-E-Leck) würde genau 904 („GIRT treibt nicht“) erklären.
Stromlos prüfen: 1P Diodentest L→R und L→O ≈ 0,6–0,7 V, Gegenrichtung OL; O–R eingebaut ≈ 48 kΩ (Parallelweg 1 k + 47,5 k), deutlich weniger = Leck. Danach 1P.L und Pad D bis zum Quell-IC verfolgen.

## Messungen 13.11. (Messplan Q2)
- **Reset-Zeit [M]:** Nach Netz-Aus sind alle LEDs (LINE, +5V, STS1) nach **3–5 s** aus → die Hilfsversorgung bricht schnell zusammen, die GIRT setzt sich nach wenigen Sekunden zurück. Die Folgefehler-Hypothese (kein Reset bei Neustart) gilt damit nur für Neustarts innerhalb weniger Sekunden **[I]**.
- **F27 stromlos [M]:** Kontakt (2 × 2 Pins, doppelt ausgeführt) = 68 Ω (parallel Vorwiderstand 68 Ω, weiß); Spule **1,4 kΩ in beide Richtungen** (keine Freilaufdiode direkt parallel messbar); Spulen-Plus = 0 Ω zu +24V. Bestromungstest offen.
- Zwischenkreisspannung noch nicht gemessen.
- **1P Diodentest [M]:** L→R 0,70 V, L→O 0,70 V (beide Übergänge gut); R→L 1,56 V, O→L 2,18 V (statt OL – eingebaut über Parallelwiderstände, z. B. Basis-Ableitwiderstand, plausibel **[I]**). Offen: Ohm O→R (≈ 48 kΩ erwartet), Verlauf von L und Pad D.
- **F27 Bestromungstest [M]:** Relais zieht mit 18 V (2 × 9 V) 20–30 × hörbar an; Kontaktwiderstand angezogen **0,03 Ω**. **F27 statisch in Ordnung.** Offen bleibt nur, ob es im Betrieb angesteuert wird (Klicken nach Einschalten, Spannung über 68 Ω).
- **1P Ohm O→R [M]: 3,39 kΩ.** Korrektur der Erwartung: Parallel zum Weg 1 k + 47,5 k (48,5 kΩ) liegt auch N → 2,21 kΩ → VDD → VDD-Netz gegen GND (1,45 kΩ, gemessen 11.11.) = 3,66 kΩ; 3,66 k ∥ 48,5 k = **3,40 kΩ** = Messwert **[I]**. Kein Kollektor-Emitter-Leck, das IN+ herunterziehen könnte (dafür müsste der Wert deutlich unter 1 kΩ liegen). **1P statisch in Ordnung.** Offen: Verlauf L und Pad D.
- **Basis 1P (L) [M/O]:** L → 4750 (475 Ω) → 2211 (2,21 kΩ) → Kollektor (O) des links benachbarten SOT-23 (Foto `photos/2026-11-12/q2_freigabe_1P_umfeld.jpg`). Zweistufige Ansteuerung: Transistor 2 schaltet über 2,68 kΩ die Basis von 1P **[I]**. Offen: Typ/Aufdruck von Transistor 2, dessen Basis- und Emitteranschluss, Pad D.
- **Transistor 2 [M]:** Diodentest von L (Basis) nach R und nach O je 0,67 V → NPN (bei roter Spitze auf L), Übergänge in Ordnung. **Emitter R gegen 0VA = 0 Ω [M].** Damit bilden Transistor 2 und 1P eine zweistufige Kette mit Emitter auf 0VA: T2 leitet → Basis 1P auf low → 1P sperrt → IN+ high → Treiber frei; T2 sperrt → 1P leitet (Pull-up an seiner Basis vorausgesetzt) → IN+ low → Treiber gesperrt **[I]**. Offen: Quelle an der Basis von T2 (MCU-Pin oder Komparator), Pull-up der Basis von 1P, Pad D.
