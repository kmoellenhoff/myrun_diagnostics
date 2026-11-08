# B18 – Kandidat: Hochspannungs-Teiler / Spannungsüberwachung DC-Motor (Rückseite)

Stand 2026-11-08, nur aus Fotos (keine Messung). Status: **Hypothese [H]**, Bauteilwerte teilweise [I] gelesen.

Fotos: `img/b18_chain_4753_1004_1001.jpg` (Makro der Kette), `img/b18_context_wide.jpg` (Umgebung, Quelle PXL_20261108_153921371).
Lage: Rückseite, Raster E5 (±1; korrigiert gegen die Übersicht, vorher F6 geschätzt), südwestlich unterhalb des SO-20-IC (B3), Box B18 in der Übersicht. Auf der Vorderseite liegt der Bereich unter dem Kühlkörper.

## B18-A: Hochohm-Kette (Kandidat für Teiler zum DC-Link / Motorspannung)

| ID | Aufdruck | Wert | Sicherheit | Bemerkung |
|---|---|---|---|---|
| B18-R1 | 4753 | 475 kΩ | I (gut lesbar) | wie die Netz-Ketten in B10 (2×475 kΩ) |
| B18-R2 | 1004 | 1,00 MΩ | I (gut lesbar) | in Reihe zu R1 |
| B18-R3 | "h001" = 1004 um 180° gedreht gelesen | 1,00 MΩ | I (Orientierung aus Foto) | in Reihe zu R2 |
| B18-P1 | rundes verzinntes Pad auf der Leiterbahn links von R1 | – | I | Anfang der Kette, Bahn läuft schräg nach links oben (siehe B18-B) |
| B18-P2 | quadratisches verzinntes Pad rechts von R3 | – | I | Ende der Kette, am Rand des grossen Kupferfeldes; mögliche Anschlussfläche |
| B18-V1 | Via/Rundpad unter dem R2/R3-Knoten | – | I | Abgriff-Knoten (Ebenenwechsel) |
| B18-V2 | Via/Rundpad über dem rechten Ende von R3 | – | I | Ebenenwechsel am Kettenende |

Topologie laut Foto [I, nicht gemessen]:
`P1 – R1(475k) – R2(1M) – [Knoten V1] – R3(1M) – P2/V2`
Summe ≈ 2,475 MΩ, Abgriff nach 1,475 MΩ.

Das passt zum gemessenen Verhalten J1 → L+ (steigt auf ≈4 MΩ und fällt wieder leicht): ein Hochohm-Pfad im Bereich einiger MΩ zwischen Niederspannungsseite und DC-Link.

Übersichts-IDs: B18 = Kette, B19 = Widerstandsblock (E6), B20 = Reihe aus 4 Widerständen + SOT-23 (E6).

## B18-B: Weiterführung von P1

Die Bahn von P1 läuft schräg nach links oben und trifft dort auf einen Block aus kleinen Widerständen (Aufdruck u. a. "1003", "1001", zwei bis drei hochkant stehende SMD-Widerstände, kleine SMD-Kondensatoren). Der Block liegt neben den drei grossen SMD-Elkos/Keramikkondensatoren (Hilfsversorgung) und ist sehr wahrscheinlich Teil der Messaufbereitung (Filter, Teilerfuss, Referenz). Aufdrucke dort aus den Fotos nicht sicher lesbar (Bewegungsunschärfe) → neue Makros nötig.

## B18-C (Übersicht: B20): Reihe aus vier Widerständen (E6)

Vier SMD-Widerstände in einer Reihe (Aufdrucke grob "4701"?/"4751"/"1003"/"4751"?, nicht sicher), daneben "4714"? und ein SOT-23 mit zwei 2,2k/1,2k-Widerständen. Die rechten Enden führen über Rundpads auf Bahnen nach rechts ins grosse Kupferfeld / zur Leistungsstufe. Vermutung [H]: Strom-/Spannungsabgriff am Motorausgang. Status offen, neue Makros nötig.

## Messplan (stromlos, Elko < 5 V, rot zuerst, Motor abgesteckt)

Alle Messungen in-circuit, Werte steigen/fallen wegen Kondensatoren → Wert bei 0 s, 30 s, 2 min notieren.

1. B18-R1 / R2 / R3 einzeln direkt über die Widerstandskörper-Enden. Erwartung: 475k / 1M / 1M (parallele Pfade ergeben kleinere Werte, das ist dann der Hinweis auf Parallelzweige).
2. P1 ↔ DC MOTOR L+ , P1 ↔ L− , P1 ↔ 0VA , P1 ↔ AC L, P1 ↔ AC N.
3. P2 ↔ L+ , L− , 0VA , +5VA.
4. V1 (Abgriff) ↔ 0VA und ↔ +5VA: ein Teilerfuss gegen 0VA wäre hier ein klarer Beweis.
5. Zusätzlich L+ ↔ 0VA und L− ↔ 0VA mit Zeitverlauf (30 s, 2 min).
6. Wenn Werte vorliegen: Foto vom Messpunkt mitliefern, damit ich Pad-Zuordnung und Raster nachtrage.

Nicht tun: nichts auslöten, nichts verbinden; der Bereich liegt auf Netzpotenzial (0VA = DC−).

## Messung 08.11. 21:10 (messprotokoll_b18.csv) – Auswertung

In-circuit: R1 = 378k (Nennwert 475k), R2 = 600k und R3 = 600k (Nennwert je 1M), Gegenrichtung 406k / 840k / 840k.
Alle drei liegen unter dem Nennwert und passen genau zu einem **geschlossenen Ring** R1–R2–R3, dessen Enden P1 und P2 niederohmig verbunden sind:
- R1 ∥ (R2+R3) = 475k ∥ 2M = 384k (gemessen 378k)
- R2 ∥ (R1+R3) = 1M ∥ 1,475M = 596k (gemessen 600k)
- R3 ∥ (R1+R2) = 596k (gemessen = R2, wie erwartet)
Folgerung [H]: P1 und P2 sind (in Vorwärtsrichtung) mit höchstens einigen 10 kΩ verbunden – die Kette ist kein offener Teiler gegen den DC-Link. Die Gegenrichtung (höher) deutet auf ein Halbleiter-/Ladeeffekt im Rückweg hin.
Nächste Messungen: P1↔P2 direkt, P2↔0VA/L−/L+, P1↔0VA, V1↔0VA.

**Nachtrag 21:12 (B18-M04):** Gesamte Kette P1↔P2 (Nennwert 2,475M): 170k steigend (rot an P1-Seite, Richtung B19), invertiert 619k steigend.
Daraus Aussenpfad zwischen P1 und P2 ≈ 180k vorwärts / ≈ 830k rückwärts (beide noch steigend, also Ladeeffekt/Halbleiter beteiligt). Die frühere Abschätzung „ext ≲ 50k“ ist damit auf **ext ≈ 100–200k** korrigiert; P1 und P2 sind nicht derselbe Knoten, aber über ein Netz von einigen 100 kΩ gekoppelt.
