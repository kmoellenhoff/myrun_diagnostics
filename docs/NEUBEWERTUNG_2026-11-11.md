# Neubewertung des Fehlerbilds (11.11.2026, nachmittags)

Zusammenführung aller Befunde seit 07.11. Tags: **[M]** gemessen, **[O]** beobachtet, **[I]** gefolgert, **[H]** Hypothese.

## 1. Es sind zwei getrennte Fehlerbilder

| | A: Fehlstart ohne Motorspannung | B: Enable-Verlust (err 9) |
|---|---|---|
| Fehlerspeicher | **904** (07.11., 11.11. 12:07, 15:09) | **902** (10.11. 13:51, 11.11. 09:31/13:48 Gerätezeit) |
| Symptom | Konsole in `QSRunning`, PWM-Sollwert an P2.6 vorhanden (≈ 0,5 V Mittelwert, 08.11.), Enables = 1, **Motor 0 V**, Encoder 0 Hz → Konsole meldet nach ≈ 10 s Hardware-Fehler | P2.5 / rosa Ader fallen auf 0 V → LM2903 B kippt → OC04 aus → err 9; **auch im Stand ohne Start** (11.11. 14:4x) |
| Ort | **GIRT**: zwischen PWM-Eingang (Optokoppler) und Motorklemme | **vor der GIRT**: Konsole schaltet EM_POWENA/rosa ab, oder Konsole reagiert auf etwas |
| Status | Gate-Treiber-VDD hatte Wackelkontakt (nachgelötet) → danach 1 Lauf 10 s, dann wieder Fehlstarts | Schlüssel (1001) und Thermoschalter-Kette sind es nicht; Schaltschwelle hat 6 V Reserve |

Weitere Codes: **1001** = Not-Stopp-Schlüssel (11.11. 12:03), err 4 (OU) am 10.11. 13:34 nach ≈ 1 s Lauf.

## 2. Was ausgeschlossen bzw. unauffällig ist
Motorwicklung, Bürsten (Lauf möglich), Encoder-Mechanik, Q2/D3 statisch, Gate-Netzwerk, B10/B18/B19-Teiler, Shunts (nachgelötet), OC04 (Test B wie OC05), LM2903-Logik, P2-Kabel (konstant beim Wackeln), Thermoschalter (≈ 0 Ω, Wackeltest o. B.), Not-Stopp-Schlüssel (eigener Code 1001).

## 3. Hypothesen, neu gewichtet

1. **Schwache Hilfsversorgung (gemeinsame Ursache für A und B)** **[H]** – gealterte Elkos in den Hilfsnetzteilen (F18 4 × 330 µF, F19/F16 47 µF, VCC-Elko an L4981/Treiber) oder der Trafo-Zweig F17. Folgen bei Lastspitze (Relais, Gate-Treiber, Start): Treiber-VDD = L4981-VCC sackt ab → Q2 schaltet nicht (A); isolierte +12 V für die Konsole (P2.1/P2.4) sackt ab → Konsole nimmt EM_POWENA zurück (B). Passt zu: viele verschiedene Codes, sporadisch, statisch kein Defekt, Verhalten abhängig davon, ob der Elko entladen war. Mit Ohmmeter nicht erkennbar.
2. **Relais im Leistungspfad** **[H]** – Inrush-Relais F27 (RT334024, 24-V-Spule, schon früher Verdacht), Motorrelais F24–F26. Verbrannte Kontakte oder schwache Spulenspannung → Motorklemme 0 V trotz Ansteuerung (A), Kontaktunterbrechung unter Last → Lastabwurf → err 4.
3. **PWM-Eingangskanal der GIRT** **[H]** – Optokoppler/Leitung von P2.6 zum MCU (einer von OC02/03/05/08, noch nicht zugeordnet). Würde A erklären, nicht B.
4. **Konsole selbst** **[H]** – schaltet EM_POWENA aus eigenem Anlass ab (B). Erklärt A nur, wenn ihr PWM-Ausgang zeitweise fehlt (am 08.11. war er da).
5. Temperaturfühler P600 (Kühlkörper Q2), Wackel-/Widerstandstest offen – könnte das MCU am Antreiben hindern **[H]**.

## 4. Nächste Messungen (nach Aufwand/Nutzen)
Sicher (Konsolenseite, Bezug P2.7):
1. **P2.1 (+12 V) MIN/MAX** im Stand bis zum err 9 und bei einem Start. Einbruch → Hilfsversorgung (Hyp. 1).
2. **P2.6 (PWM)** bei einem Fehlstart im Hz/Duty-Modus. PWM da → Fehler sicher in der GIRT (Hyp. 2/3/5).
3. Hören, ob beim Einschalten und beim Start Relais klicken.
4. Skript `--listen-poll` parallel, um EM_POWENA-Zeitpunkt relativ zum Fehler zu sehen.

Netzpotential (nur geklemmt bei entladenem Elko, Batteriemultimeter, Hände weg):
5. **L4981 Pin 19 / Treiber-VDD gegen 0VA MIN** beim Start. Einbruch unter ≈ 10 V → Hyp. 1.
6. +24 V an P400 gegen 0V24 (= 0VA) MIN beim Start (Relaisversorgung).
7. Treiber IN+ (Pad A) gegen Pad B beim Start: PWM vom MCU vorhanden?

Ohne Messgerät: Elkos der Hilfsversorgung auf Wölbung/Austritt prüfen; mit ESR-Meter messen oder vorsorglich tauschen. Entscheidender Kurztest bei Verfügbarkeit: Tausch der GIRT oder der Konsole.
