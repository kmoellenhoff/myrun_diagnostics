# Q2-Kontakt C, R2211 und „1P“: Pausenstand 09.11.2026

**Auf ausdrücklichen Nutzerwunsch gesichert. Der Diodentest am 1P-Dreibeiner ist AUSSTEHEND und wird später ausgeführt.** Die acht neuen Ω-Datensätze sind berichtet; es wurden keine Diodenwerte ergänzt. Kein verursachendes defektes Bauteil nachgewiesen. Claude-Raster **Q2/B21/B5** und alle bisherigen Anschluss-IDs bleiben unverändert.

[PDF mit markierter Originalaufnahme und Fortsetzung](Q2_C_1P_NACHTRAG_2026-11-09.pdf) · [neues Originalmakro ohne EXIF](../../photos/2026-11-09/q2/50396.jpg) · [Ergebnis-CSV](messprotokoll_2026-11-09.csv) · [Rohangaben](Q2_C_1P_ROHANGABEN_2026-11-09.json) · [leere Vorlage für den späteren Diodentest](Q2_1P_DIODENTEST_AUSSTEHEND.csv) · [Schaltplannachtrag](../schaltplan_110926/blatt_4.svg)

## Neue Betriebsbeobachtung: Gehäuselüfter läuft auch beim Fehlstart

Nutzer: „imboot vorgang und insbesondere beim fehlstart läuft lüfter definitiv lautstark an“. P400 ist laut vorheriger Nutzerangabe der Gehäuselüfteranschluss. Beim Anlauf steht dort zumindest zeitweise ausreichend Leistung für den Lüfter zur Verfügung. Ein vollständiger Ausfall dieses Versorgungszweigs wird dadurch weniger wahrscheinlich. Es sind weder eine Spannung noch die Stabilität während des gesamten Fehlstarts gemessen. Der Befund beweist keine lokale Gate-Treiberversorgung oder Eingangsfreigabe. Hörbare Lautstärke wird nicht in einen Spannungswert oder eine genaue Drehzahl umgerechnet.

## Messkontakte eindeutig benennen

**R2211** ist der korrigierte Code 2211 = 2,21 kΩ des bisher im Messplan **R221** genannten Widerstands. Linke Kappe = R221-a, rechte Kappe = R221-b. Die ursprünglichen a/b-Marker bleiben unverändert. Der fünfpolige Baustein behält A/B/C/D5/E; **C** ist dessen lokaler Kontakt oben rechts im Foto 50386.

Für den Dreibeiner unmittelbar über R2211 werden als reine Foto-Hilfen ergänzt:

| Foto-Hilfe | Lage in 50386 und 50396 | elektrisch gemessen | Funktion nur unter NPN-Kandidatenannahme [I] |
|---|---|---|---|
| Q2-1P.O | einzelner Anschluss oben | 0 Ω zur linken R2211-Kappe | Pin 3, Kollektor |
| Q2-1P.L | unten links | 4,78 kΩ zur linken R2211-Kappe | Pin 1, Basis |
| Q2-1P.R | unten rechts | 0 Ω zu 0VA beidseitig | Pin 2, Emitter |

O/L/R sind keine Herstellerpins oder neuen Rasterfelder. M = Nutzer-Messung, F = sichtbarer Fotoverlauf, I = Code-/Herstellerabgleich bzw. noch bedingte Funktion. Der Buchstabe C am Treiber ist nicht die automatisch gesicherte Kollektorbezeichnung des anderen Bauteils.

## Neue Ω-Messungen

Erste Richtung wie Rot/Schwarz angegeben. Leere Gegenrichtung bedeutet nicht berichtet, nicht OL oder automatisch gleicher Wert. Stromlos und in-circuit laut laufendem Ablauf; Temperaturen und detaillierte Steckzustände fehlen. P400 blieb laut letztem Bericht gesteckt, eine Änderung wurde nicht mitgeteilt.

| Mess-ID | Rot → Schwarz | Anzeige | Gegenrichtung | Verlauf |
|---|---|---:|---:|---|
| Q2C-01 | R221-a (Code 2211) → +24V | 41 kΩ | 50,8 kΩ | Beide Richtungen anfangs niedriger und ansteigend; berichtete Werte nach jeweils etwa 20 s erreicht |
| Q2C-02 | Q2-DRV.C → R221-b (Code 2211) | 0 Ω | nicht berichtet | nicht mitgeteilt |
| Q2C-03 | Q2-1P.O → R221-a (Code 2211) | 0 Ω | nicht berichtet | nicht mitgeteilt |
| Q2C-04 | Q2-1P.L → R221-a (Code 2211) | 4,78 kΩ | nicht berichtet | nicht mitgeteilt |
| Q2C-05 | Q2-1P.R → R221-a (Code 2211) | 3,38 kΩ | nicht berichtet | nicht mitgeteilt |
| Q2C-06 | Q2-1P.L → +24V | 57,5 kΩ, steigend | nicht berichtet | steigend auf 57,5 kΩ; Ablesezeit nicht mitgeteilt |
| Q2C-07 | Q2-1P.R → +24V | 37,46 kΩ | nicht berichtet | nicht mitgeteilt |
| Q2C-08 | Q2-1P.R → 0VA | 0 Ω | 0 Ω | nicht mitgeteilt |

Die Zeitangabe etwa 20 s gilt nur für die beiden Richtungen Q2C-01. Vorher waren die Anzeigen niedriger und stiegen an. Eine weitere Stabilität nach Erreichen der berichteten Werte wurde nicht ausdrücklich beschrieben. Für Q2C-06 wurde nur „steigend auf 57,5 kΩ“ berichtet; dafür keine 20 s erfinden. Die zahlenlosen Angaben „beide nicht 0 ohm“ wurden später durch die zwei Einzelwerte ergänzt; numerische Gegenrichtungen fehlen weiterhin.

Die +24V-Messungen zeigen keinen direkten niederohmigen Anschluss der geprüften Pins an den +24V-Testpunkt. Der Vergleich 37,46 kΩ unten rechts gegen +24V mit zuvor 37,49 kΩ 0V24→+24V legte Masse nahe; die anschließende direkte 0-Ω-Messung zu 0VA hat diesen Bezug bestätigt. Die höheren, teils steigenden Anzeigen bleiben effektive Netzwerte, keine isolierten Einzelwiderstände.

## Aufdruck und Kandidat – noch kein Defektbefund

Das neue Originalmakro zeigt **1P** deutlich. Der Nutzer beschreibt zusätzlich ein nicht sicher erkennbares Symbol oder eine gedrehte „3“; dessen Bedeutung bleibt offen. **MMBT2222A/PMBT2222A-Familie, NPN**, ist ein gut passender Kandidat aus Kurzcode, SOT23-Gehäuse und den zwei gemessenen Anschlusszuordnungen. Hersteller, genaue Variante und Zusatzzeichen sind noch nicht eindeutig identifiziert. Der angefragte Diodentest ist nicht durchgeführt.

Primärquelle: [Nexperia PMBT2222A, Datenblatt 27.07.2022](https://assets.nexperia.com/documents/data-sheet/PMBT2222A.pdf), Seite 1: Pin 1 Basis, Pin 2 Emitter, Pin 3 Kollektor; Seite 2: Markierung %1P, wobei % einen Fertigungsstätten-Code bezeichnet. Das konkrete Zusatzzeichen im Foto wird dadurch nicht automatisch entschlüsselt.

## Gesicherter äußerer Verlauf und korrigierte Arbeitshypothese

```text
Q2-Treiberkontakt C
   ─ 0 Ω [M] ─ R221-b ─ 2211 / 2,21 kΩ [I; zuvor 2,09 kΩ beidseitig M]
   ─ R221-a ─ 0 Ω [M] ─ Q2-1P.O (oberer Einzelanschluss)

Q2-1P.R (unten rechts) ─ 0 Ω beidseitig [M] ─ 0VA
Q2-1P.L (unten links): Steuer-/Anschlussfunktion noch bedingt
```

**Eine positive Versorgungszuleitung zu C ist damit nicht gefunden.** Die anfängliche Betrachtung „R2211 vor C = speisender Zweig“ war eine Arbeitshypothese und ist nicht belegt. Unter der NPN-Annahme kann der Zweig C über R2211 und den Transistor gegen Masse belasten; ein gesteuerter Ableit-/Steuerzweig ist deshalb plausibel. Ob das eine Abschaltung, Begrenzung oder andere Funktion hat und ob der Transistor beim Fehlstart falsch aktiv ist, bleibt offen. Ebenso bleibt die FAN3100C-Zuordnung des Fünfbeiners ein Kandidat; C=VDD ist weiterhin eine bedingte Funktion.

Das beobachtete Lüfteranlaufen und die statischen Widerstände erklären den fehlenden Motorlauf noch nicht. Es wurde weder ein defekter Transistor noch ein bestimmter falscher Steuerpegel nachgewiesen. Kein Bauteiltausch oder Eingriff aus der Kandidatenzuordnung abgeleitet.

## Hier später fortsetzen – Diodentest AUSSTEHEND

Weiter stromlos nach dem bestehenden Restspannungs-Prüfablauf, Multimeter auf Diodenmodus. Im **neuen Foto 50396**:

1. **Rot unten links (L), Schwarz unten rechts (R)**; danach umpolen.
2. **Rot unten links (L), Schwarz oben einzeln (O)**; danach umpolen.

Erst die vier tatsächlichen Anzeigen in V oder OL eintragen. Für isolierte Si-NPN-Basisübergänge wären vorwärts ungefähr 0,5–0,8 V und rückwärts Sperren plausibel; eingelötet können Parallelpfade endliche Gegenanzeigen verursachen. Keine pauschale harte Gut-/Schlechtgrenze und kein vorweggenommener Funktionsnachweis.

## Foto-/Dokumentnachweis

50396.jpg wurde vor dem GitHub-Import von EXIF/XMP bereinigt, ohne JPEG-Neukodierung und ohne Änderung dekodierter Pixel. [Metadatennachweis](../../photos/2026-11-09/q2/50396_metadaten_pruefung.json). Das PDF bettet diese Originalaufnahme ein und ergänzt nur Vektormarkierungen; Punkte und Hash stehen in [Q2_1P_foto_nachweis.json](Q2_1P_foto_nachweis.json). Vorhandene Originalfotos, Rasterindex und die acht bisherigen Markermakros sind unverändert. Kein Platineninhalt wurde generiert. Der Assistent hat selbst keine elektrische Messung ausgeführt.
