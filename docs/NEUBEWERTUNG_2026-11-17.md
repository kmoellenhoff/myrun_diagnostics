# Neubewertung 17.11.2026 abends – Netzsignal J zeitweise ohne Einspeisung

Grundlage: T17-36 bis T17-52 (`LAUF_2026-11-17.md`, `messprotokoll_2026-11-17.csv`), `PRUEFUNG_2026-11-17_netzsignal.md`, `PRUEFUNG_B10_X_2026-11-17.md`, Schaltplan `gesamtschaltplan_110926/`. Keine neuen Messungen. M gemessen, O beobachtet, I abgeleitet, H Hypothese.

## 1. Die Werte sind in sich stimmig
| Zustand | J | TL082 Pin 3 / Pin 1 | X | Bewertung |
|---|---|---|---|---|
| „hoch“ | 5 V DC, 90 mV AC, 0 Hz (T17-39/40) | Pin 1 4,9 V (T17-41) | – | Rechenmodell bei 238 V: Mittelwert an J = 336,6 V × 0,637 × 22,1/972 ≈ **4,9 V** [I]. Ein schlechter Kontakt kann keinen Wert erzeugen, der so genau dem Modell entspricht. |
| „niedrig“ | ≈ 0,3 V an beiden J-Kontakten (T17-47/52) | ≈ 0,3 V / 0,3–0,41 V (T17-42/43/45) | 0,10–0,12 V (T17-36/37) | X ≈ halber J-Wert = Teiler 1:2 [I]. **Puffer, R1/R2, 100 Ω und Knoten X geben den niedrigen J-Pegel korrekt weiter.** |
- TL082-Versorgung im niedrigen Zustand vorhanden: +13,5 V / −14 V (T17-44/46) [M].
- Netz am Board 238 V (T17-48) [M, Gleichzeitigkeit mit dem J-Minimum nicht belegt].
- Folgerung [I]: Der MCU-Eingang X ist nicht selbst defekt; er bekommt schlicht kein Netzsignal, weil **J** zeitweise fast 0 V hat. Ansatz „Last an X / zweite Klemmdiode“ aus `PRUEFUNG_2026-11-17_netzsignal.md` tritt zurück.

## 2. Zusatzbefunde
- **Glättung an J [I/H]:** 90 mV AC statt ≈ 2,4 V (ungefilterte Vollwelle), 0 Hz, und der beobachtete allmähliche Abfall 5 V → 1 V → einige 100 mV (T17-49) passen zu einem Kondensator von einigen µF an J bzw. am TL082-Eingang (τ = 22,1 kΩ × C). Ein solcher Kondensator fehlt im Schaltplan. Prüfen: LCR J ↔ 0VA eingebaut, Bauteil suchen.
- **Relaisklicken folgt J [O/H]:** Beim Wiedereinstecken wechselt J zwischen 5 V und niedrig, jeweils mit Relaisklicken (T17-49). Lesart: Der MCU schaltet ein Relais (F27 oder F24–F26), sobald er Netz erkennt, und fällt bei Verlust zurück. Dann arbeitet die MCU-Logik, und das fehlende Netzsignal ist die Ursache der verweigerten Freigabe. Nicht belegt; Relais nicht identifiziert.
- **Restwert 0,3 V:** entspricht ≈ 14 µA in 22,1 kΩ, also ≈ 6 % der Sollspeisung (≈ 224 µA aus beiden Zweigen). Beide Zweige (L und N) fehlen gleichzeitig [I].

## 3. Wahrscheinlichste Stelle [H]
Weil **beide** Netzzweige gleichzeitig ausfallen, liegt die Unterbrechung eher an einer **gemeinsamen** Stelle als in einzelnen 475-kΩ-Widerständen:
1. **Verbindung gemeinsame Kathode D1/D2 (J1/J3) → Widerstandsknoten J („2212“ rechts / „1001“ links)** – genau dort liegen die dunklen Stellen unter dem Lack (Korrosion). Ein intermittierender Übergang würde die Wechsel beim Antasten (Druck/Biegung der Platine) erklären.
2. Gemeinsamer Abgriff an den AC-Pads (T1/T2) bzw. deren Lötstellen.
3. Weniger wahrscheinlich: beide Widerstandsketten oder beide Dioden gleichzeitig; ein Pfad, der J zeitweise nach 0VA zieht (dann aber ≈ 1,3 kΩ nötig).
Passt zur Vorgeschichte: Band lief am 10./11.11. kurz, Fehler auch im Stand – intermittierendes Verhalten.

## 4. Entscheidende Messungen
| # | Zustand | Messung | Auswertung |
|---|---|---|---|
| 1 | Betrieb, **J niedrig** | Gemeinsame Kathode D1/D2 (J1/J3) gegen 0VA, V DC, Bereich ≥ 600 V, Leitungen stromlos festgeklemmt | Kathode hoch (zweistellig bis über 100 V), Widerstandsseite 0,3 V → Unterbrechung dazwischen. Kathode ebenfalls ≈ 0,3 V → weiter bei 2. |
| 2 | Betrieb, J niedrig | Anoden D1/D2 und T1/T2 gegen 0VA, V AC | Netzanteil vorhanden/fehlt → Unterbrechung vor bzw. hinter den Widerständen |
| 3 | stromlos | Ω: Kathode D1/D2 ↔ rechte Kappe „2212“ und ↔ linke Kappe „1001“, dabei Platine mit isoliertem Stab leicht biegen/drücken; ebenso R1–R4 und Diodentest D1/D2 | Springen des Wertes = Riss/Korrosion |
| 4 | stromlos | LCR J ↔ 0VA | Kapazität vorhanden → Glättungskondensator (Schaltplan ergänzen) |
| 5 | Betrieb, Netz-Ein | J und Spule F27 gleichzeitig (z. B. Oszi an J, Multimeter an F27-Spulen-Minus, beide Bezug 0VA) | Zieht F27 an, wenn J hoch ist? → Bestätigung der Lesart in Abschnitt 2 |
Messung 1 und 2 nur mit fest geklemmten Leitungen und ohne Berührung; der Kathodenknoten kann bei Unterbrechung hohe Spannung führen.

## 5. Nachtrag 20:10 – Korrekturen nach Kritik und Messung an beiden J-Kontakten
- **J an beiden B10-J-Kontakten (Diodenseite) ≈ 0,3 V** (Nutzer, T17-52) → die Verbindung Kathode → „2212“/„1001“ ist **nicht** die Ursache; Abschnitt 3 Punkt 1 entfällt.
- **Korrektur:** „Filter liegt nicht im B10-Weg“ war zu stark – 0 Ω zu den AC-Pads schließt eine Drosselwicklung im Weg nicht aus. Als Ursache bleibt eine Drossel trotzdem unwahrscheinlich (statisch 0 Ω, dicke Wicklung) [I].
- **Korrektur:** „L und N beide ≈ 0 V gegen 0VA“ ist bei 238 V zwischen L und N nicht möglich (U_L–N = U_L–0VA − U_N–0VA); diese Zeile der Messtabelle im Chat war falsch. Ein Relais im Rückweg ist nicht belegt.
- **Ergänzte Möglichkeit C – zusätzliche Last an J [H]:** Bei intakter Einspeisung würden ≈ 1,5 kΩ von J nach 0VA genügen, um J auf ≈ 0,3 V zu ziehen. Statisch J ↔ 0VA 22,1 kΩ (16.11.) spricht gegen eine dauerhafte Last, nicht gegen eine spannungsabhängige (z. B. undichter Glättungskondensator an J – Kapazität an J ist durch B10-M06 und den langsamen Abfall angedeutet – oder Leckpfad/Korrosion). Hinweis: Am 08.11. wurde J ↔ 0VA mit **6,4–6,8 kΩ** gemessen (B10-M25/M26); das wäre mit einer zeitweise vorhandenen Last an J vereinbar.
- **Unterscheidung A (Einspeisung offen) / C (Last an J), im Zustand „J niedrig“** [I]: DC-Spannung **über einem „4753“** je Zweig (Messspitzen auf beide Kappen). Fließt Strom (Fall C oder normal), liegen rechnerisch ≈ 50 V DC über dem Widerstand; fließt keiner (Fall A), ≈ 0 V. Zusätzlich L und N je gegen 0VA (V DC/V AC) und die Zwischenkreisspannung im selben Zustand. Mittel-/Effektivwerte und Belastung durch das Multimeter (10 MΩ) machen die Werte nur grob; es geht um „Strom fließt / fließt nicht“.
- Vorgehen bestätigt: nichts komplett auslöten; bei einem unklaren Bauteil höchstens ein Bein abheben. Statt die Platine zu biegen höchstens lokal mit isoliertem Stab leicht antippen.

## 6. Nachtrag 18.11. – Möglicher zweiter Pfad von J über 10 kΩ (Beobachtung, keine neue Messung)
- **0,3 V an J** erfordern, dass beide B10-Zweige gleichzeitig ausfallen **oder** J zusätzlich belastet wird. Ein einzelner Diodenausfall ergibt nur etwa den halben Wert (≈ 2,4 V) [I]. Dass zwei unabhängige Wackelkontakte über viele Messungen gleichzeitig aussetzen, ist als Zufall wenig plausibel; die alleinige Erklärung „untere Diode“ wird dadurch schwächer.
- **Rechnerische Übereinstimmung [I]:** J ↔ 0VA am 08.11. **6,4–6,8 kΩ** (B10-M25/M26), am 16.11. **22,1 kΩ** (AKT-064). **22,1 kΩ ∥ 10 kΩ = 6,9 kΩ.** Von J zu den beiden Testpunkten am SOT-23-5 wurden am 14.11. **genau 10 kΩ** gemessen. Auch J ↔ +5VA ≈ 9–10 kΩ (08.11.) passt: 6,9 kΩ + 0VA↔+5VA 2,35 kΩ ≈ 9,3 kΩ (vgl. B10-A01).
- **Lesart [H]:** J hat neben „2212“ einen zweiten Pfad über 10 kΩ zu einem Knoten am SOT-23-5. Dieser Knoten lag am 08.11. (stromlos) niederohmig an 0VA, am 16.11. nicht. Möglich: das SOT-23-5 (Schalter/Vergleicher o. Ä.) zieht seinen Ausgang zeitweise auf 0VA; stromlos kann aber auch ein ungespeistes Bauteil je nach Ladezustand seiner Versorgung niederohmig wirken. Ebenso möglich: Unterschiede durch Messpunkt (08.11. am Diodenbein, Platine nicht fixiert) oder Belag vor der Reinigung am 10.11.
- Größenordnung: Diese Last allein senkt J im Betrieb nur auf ≈ 1,5 V, nicht auf 0,3 V; zusammen mit einem fehlenden Zweig ergeben sich Werte in der Nähe der gemessenen.
- **Prüfung:** stromlos beide SOT-23-5-Testpunkte gegen 0VA und +5VA, Aufdruck des SOT-23-5 ablesen; beide B10-Dioden ersetzen (nicht nur die untere); bei erneutem Abfall von J sofort SOT-23-5-Testpunkt gegen 0VA messen.

- **Nachtrag 18.11.:** Abschnitt 6 nicht bestätigt – J ↔ Testpunkt ② = 31,2 kΩ (= 22,1 + 9,2 kΩ, nur über 0VA); SOT-23-5 „100CA“ vermutlich PFC-Gate-Treiber (FAN3100C). Details: LAUF_2026-11-18.md.
