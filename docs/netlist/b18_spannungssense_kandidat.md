# B18 – Busspannungs-Teiler (Kandidat für die Spannungsüberwachung DC-Bus/Motor), Rückseite E5

**Maßgeblicher Stand: 2026-11-08 21:40.** Abschnitt 1–4 gilt; verworfene Zwischenhypothesen stehen nur in Abschnitt 6 (Historie) und dürfen **nicht** für Messungen verwendet werden.
Sicherheitsgrade: [M] gemessen, [I] aus Foto/Aufdruck gelesen, [H] Hypothese.

## 1. Maßgebliche Schaltung

```
DC MOTOR L+ (= DC-Bus nach Drossel)
   │  0 Ω [M]
  B18-P2 (quadratisches Pad)
   │
  B18-R3  1 MΩ  [I]
   │
  B18-V1 (TP1, Messpunkt, Abgriff)
   │
  B18-R2  1 MΩ  [I]
   │
  B18-R1  475 kΩ [I]
   │
  B18-P1 (rundes Pad auf der Bahn) ──► Bahn nach B19 (Widerstandsblock, E6) → Messauswertung [H]
   │
  ≈ 221 kΩ gegen 0VA  [M: P1↔0VA 223,7k konstant; P1↔+5VA 226,4k konstant]
```

- Teilerverhältnis nur über diese Widerstände ≈ 8 % (≈ 221k / 2,70 M). Was B19 danach noch teilt/filtert, ist **nicht bekannt**.
- Funktion „Busspannungs-Überwachung“ ist [H, plausibel], aber nicht bewiesen; der Fusspunkt „0VA“ ist wahrscheinlich, nicht belegt (Differenz 0VA/+5VA nur 2,7k ≈ Messfehler).
- Die Messwerte (Abschnitt 3) sind in-circuit; Kondensatoren/Halbleiter verfälschen die Anzeige (steigend/fallend). Einzelwerte sind keine Bauteil-Nennwerte.

## 2. Lage und Bauteil-IDs

Lage: Rückseite, Raster **E5** (± 1), unterhalb des SO-20-IC (B3); Vorderseite liegt der Bereich unter dem Kühlkörper. Übersichts-IDs: **B18** = Kette, **B19** = Widerstandsblock (E6), **B20** = Reihe aus 4 Widerständen + SOT-23 (E6).
Fotos: `img/b18_chain_annotiert_aufrecht.jpg`, `img/b18_chain_annotiert_foto.jpg`, `img/b18_chain_4753_1004_1001.jpg`, `img/b18_context_wide.jpg`.

| ID | Aufdruck | Wert | Grad | Bemerkung |
|---|---|---|---|---|
| B18-R1 | 4753 | 475 kΩ | I | wie die Netz-Ketten in B10 |
| B18-R2 | 1004 | 1,00 MΩ | I | |
| B18-R3 | "h001" = 1004 um 180° gedreht | 1,00 MΩ | I | |
| B18-P1 | rundes verzinntes Pad auf der Bahn links von R1 | – | I | Messknoten, Bahn schräg nach B19 |
| B18-P2 | quadratisches verzinntes Pad rechts von R3 | – | I/M | = DC MOTOR L+ (0 Ω) [M] |
| B18-V1 (=TP1) | Rundpad (Messpunkt, kein Via) unter dem R2/R3-Knoten | – | I | Abgriff |
| B18-V2 (=TP2) | Rundpad (Messpunkt) über dem rechten Ende von R3 | – | I | Netz von R3/P2 |

B19 (Widerstandsblock, Aufdrucke u. a. "1003", "1001", mehrere hochkant stehende Widerstände, kleine SMD-Kondensatoren) und B20 (Reihe aus 4 Widerständen + SOT-23): **Aufdrucke nicht sicher lesbar**, Funktion offen → scharfe Makros beider Seiten nötig.

## 3. Messwerte (alle in-circuit, stromlos; Rohdaten: `messprotokoll_b18.csv`)

| Mess-ID | Messung (rot zuerst) | Wert | Gegenrichtung |
|---|---|---|---|
| B18-M01 | R1 (Ende Richtung B19) | 378 kΩ | 406 kΩ |
| B18-M02 | R2 | 600 kΩ | 840 kΩ |
| B18-M03 | R3 | wie R2 | wie R2 |
| B18-M04 | gesamte Kette P1↔P2 | 170 kΩ steigend | 619 kΩ steigend |
| B18-M05 | P1↔0VA | 223,7 kΩ konstant | |
| B18-M06 | P1↔+5VA | 226,4 kΩ konstant | |
| B18-M07 | P2↔0VA | 6 MΩ fallend (nicht eingeschwungen) | |
| B18-M08 | P2↔DC MOTOR L+ | **0 Ω** | |
| B18-M09 | P2↔DC MOTOR L− | 300 kΩ steigend | |
| B18-M10 | V1↔0VA | 1,211 MΩ | |
| B18-M11 | V1↔+5VA | 1,206 MΩ | |

Auswertung: Alle drei Widerstände messen unter Nennwert, weil parallel der Rest des Netzes liegt (R1 ∥ (R2+R3+Rest) ≈ 384k, R2 ∥ (R1+R3+Rest) ≈ 596k, jeweils passend). Der Aussenpfad P1–P2 beträgt ≈ 180 kΩ vorwärts / ≈ 830 kΩ rückwärts (steigend, Ladeeffekt/Halbleiter). V1↔0VA ≈ 1,2 MΩ passt zum Tap-Modell (Rx ≈ 3,2 M von L+ gegen 0VA über übrige Pfade).

## 4. Zusammenhang Leistungsstufe (messprotokoll_leistungsteil.csv, `q2_zuordnung.md`)

L+ = DC-Bus (nach Drossel), L− = Q2-Drain (Low-Side), 0VA = Source/DC−. D3 (L−→L+ 0,397 V) und Body-Diode Q2 (0VA→L− 0,444 V) statisch unauffällig; Q2-Gate-Netz (G–S 9,13k, G–D 2,19M) unauffällig. Aussagen gelten für diesen Messzeitpunkt; **intermittierende Fehler sind damit nicht ausgeschlossen.**

## 5. Offene Punkte

- B19/B20: Aufdrucke lesen (Makros Vorder- und Rückseite), Weg von P1 bis zum Messeingang (MCU/Komparator LM2903/TL082?) verfolgen.
- P2↔0VA einschwingen lassen (Endwert, Modell erwartet ≈ 1,5 M).
- P2↔L− = 300 kΩ steigend: Ursache offen (Bleeder/Snubber/D3/Q2-Umfeld?).
- Fusspunkt von P1: 0VA oder +5VA (Differenz 2,7k im Messfehler) – eindeutig nur über die Bahn bzw. eine Messung mit höherer Auflösung.
- Funktion als Busspannungs-Überwachung nur live prüfbar (Trenntrafo nötig, nicht vorhanden).

Nicht tun: nichts auslöten, nichts verbinden; Bereich liegt auf Netzpotenzial (0VA = DC−).

## 6. Historie (überholt – nicht für Messungen verwenden)

- 21:10: Interpretation „geschlossener Ring, P1/P2 niederohmig verbunden (ext ≲ 50k)“ → durch M04 korrigiert (ext ≈ 100–200k, Vorwärtsrichtung).
- 21:17: Hypothese „**P2 = L−** (Schaltknoten/Drain von Q2)“ und „Body-Diodentest 0VA→P2“ → **widerlegt** durch M08 (P2↔L+ = 0 Ω).
- 21:17: Übereinstimmung „J1→L− = 2,6 MΩ ≈ Kette + 221k“ → Zufall, ungeklärt; kein Zusammenhang mit der Kette.
- Anfangsbezeichnung „V1/V2 = Via/Ebenenwechsel“ → falsch; es sind einfache Messpunkte (TP1/TP2).
- Anfangslage „F6“ → korrigiert auf E5.
- Frühere Beschreibung von B20 als „Spalte aus vier Widerständen“ → es ist eine Reihe.
