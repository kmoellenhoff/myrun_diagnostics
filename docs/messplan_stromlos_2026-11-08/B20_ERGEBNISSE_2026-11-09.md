# Blatt 04: B20 – Ergebnisse vom 09.11.2026

**Im geprüften stromlosen Umfang abgeschlossen; nächstes Blatt 05, Q2-Treiber.** B20 bleibt in Claudes Feld **E6**. Quelle sind Nutzer-Messungen im Chat und das neue Originalmakro `50370.jpg`. Ein verursachendes defektes Bauteil wurde nicht identifiziert. SOT-23-Typ, vollständige Netzfunktion und R4-Code bleiben offen; das Blatt ist keine Funktionsfreigabe.

[Neue Aufnahme ohne EXIF](../../photos/2026-11-09/b20/50370.jpg) · [Metadaten-/Pixelnachweis](../../photos/2026-11-09/b20/metadaten_pruefung.json) · [ursprünglich markierte Anschlüsse](makros/04.png) · [alle Ergebnisse als CSV](messprotokoll_2026-11-09.csv) · [Messplan](MESSPLAN.md)

## Anschlusszuordnung und Korrektur

Die ursprünglichen Messplan-IDs bleiben unverändert. Im neuen Foto liegen **R1–R4 von links nach rechts**, jeweils **a unten, b oben**. Am SOT-23 links neben R1: **Ta unten einzeln, Tb oben links, Tc oben rechts**. Eine vorausgehende Chatbeschreibung a oben/b unten war vertauscht. Der Nutzer bestätigte ausdrücklich die Benennung aus dem ursprünglichen Messplan; insbesondere R2 a→b bedeutet im neuen Bild **Rot unten, Schwarz oben**.

R1 und R2 tragen 4751 = 4,75 kΩ; R3 trägt 1003 = 100 kΩ. Bei R4 ist nur 475… sicher lesbar: 4,77 kΩ gemessen passt zwar zu einem 4,75-kΩ-Bauteil, beweist aber keinen vollständigen Aufdruck. Beide sichtbaren achtpoligen ICs sind als TL082I (Doppel-Operationsverstärker) erkennbar; ihre genaue Netzfunktion wurde hier nicht verfolgt. Die Funktionspins des SOT-23 werden nicht als B/C/E, G/D/S oder Regleranschlüsse geraten.

## Messwerte

Alle Werte laut laufendem Messablauf stromlos und in-circuit. Erste Richtung: Rot am zuerst genannten Anschluss; bei den Referenzmessungen also zunächst Schwarz an 0VA beziehungsweise +5VA. Gegenrichtung umgepolt. Bei symmetrischen Widerstandswerten wurde die absolute Anfangspolung nicht noch einmal separat bestätigt. Temperatur, Ablesezeit, Zeitverlauf und detaillierte Steckzustände wurden nicht mitgeteilt.

| Mess-ID | Rot → Schwarz | Anzeige | Gegenrichtung |
|---|---|---:|---:|
| B20-01 | B20-R1a → B20-R1b | 4,6 kΩ | 4,6 kΩ |
| B20-02 | B20-R2a → B20-R2b | 2,7 kΩ | 3,3 kΩ |
| B20-03 | B20-R3a → B20-R3b | 72,3 kΩ | 72,3 kΩ |
| B20-04 | B20-R4a → B20-R4b | 4,77 kΩ | 4,77 kΩ |
| B20-D01 | B20-Ta → B20-Tb | 1,13 V | 0,70 V |
| B20-D02 | B20-Ta → B20-Tc | 2,38 V | 0,68 V |
| B20-D03 | B20-Tb → B20-Tc | 1,94 V | 0,69 V |
| B20-G01 | B20-Ta → 0VA | 20,5 kΩ | 20,5 kΩ |
| B20-G02 | B20-Tb → 0VA | 0 Ω | 0 Ω |
| B20-G03 | B20-Tc → 0VA | 14,8 kΩ | 14,8 kΩ |
| B20-V01 | B20-Ta → +5VA | 23,1 kΩ | 23,1 kΩ |
| B20-V02 | B20-Tc → +5VA | 12,2 kΩ | 12,2 kΩ |

Die letzten Angaben „ta 23,1 / tc 12,2, jeweils beide richtungen gleich“ werden im fortlaufenden kΩ-Messblock als kΩ übernommen; die Rohangabe enthält die Einheit nicht erneut. Die CSV weist das aus. Für Diodenanzeigen bleiben Ohm-Felder leer.

## Einordnung

- R1: 4,6 kΩ, etwa 3,2 % unter nominal 4,75 kΩ. Parallelbelastung möglich; kein isolierter Toleranztest.
- R2: 2,7/3,3 kΩ sind niedriger und polungsabhängig. Das passt zu zusätzlicher Belastung durch die angeschlossene Schaltung; daraus folgt noch kein defekter Widerstand.
- R3: 72,3 kΩ liegt unter nominal 100 kΩ. Parallelpfade bleiben möglich; eine Einzelwertänderung ist in-circuit nicht abgetrennt.
- R4: 4,77 kΩ beidseitig. Ein Nennwert von 4,75 kΩ wäre plausibel, bleibt wegen des unvollständig lesbaren Codes vorläufig.
- SOT-23: 0,68–0,70 V sind mit Silizium-Halbleiterpfaden vereinbar. Die höheren Anzeigen in den jeweiligen Gegenrichtungen können weitere Schaltungspfade enthalten. Alle drei Paare liefern Werte in beiden Richtungen; das ist eingelötet weder ein eindeutiger Defektbeleg noch ein sicherer Typ-/Pinout-Test.
- **Tb–0VA = 0 Ω beidseitig:** direkte Masseverbindung elektrisch bestätigt. Ta und Tc sind gegen 0VA und +5VA endlich hochohmig; keine direkte Verbindung zu +5VA nachgewiesen. Die Referenz +5VA ist keine bestätigte Versorgung des SOT-23.

Die Differenzen zwischen den Widerständen gegen 0VA und +5VA sind keine isolierten Serienwiderstände und kein Beweis einer bestimmten Verschaltung. Es werden keine Netze aufgrund endlicher kΩ-Werte vereinigt. Aus den vorliegenden Messungen folgt kein Anlass, einen bestimmten B20-Widerstand oder den SOT-23 bereits als defekt zu ersetzen. Dynamische, feuchte- oder temperaturabhängige Fehler und tatsächliche Pin-Funktionen bleiben offen.

## Bestätigtes Fragment

```text
B20-Tb ─── 0 Ω [M, beide Richtungen] ─── 0VA

Ta: 20,5 kΩ zu 0VA; 23,1 kΩ zu +5VA, jeweils beidseitig [M]
Tc: 14,8 kΩ zu 0VA; 12,2 kΩ zu +5VA, jeweils beidseitig [M]
```

Diese kΩ-Angaben sind Messkopplungen des gesamten eingelöteten Netzes, keine eingezeichneten Einzelwiderstände. R1–R4 und das SO8-Umfeld bleiben eigenständige Bauteile; ihre vollständige Verbindung zum SOT-23 ist hier nicht ergänzt.

## Nutzer-Rohangaben

```text
r1 beide richtungen 4,6kohm
r2 a-b 2,7 kohm, b-a 3,3kohm
r3 72,3 kohm beide richtungen
r4 4,77 kohm beide richtungn

endkppen "a" und "b" so wie in ursprünglichem messplan

ta-tb 1,13; inv: 0,7
ta-tc 2,38 ; inv: 0,68
tb-tc 1,94; inv: 0,69

jeweils zu 0Va; erse messung schwarz an 0va; 2. wert rot an 0va:
Ta 1. 20,5 kohm 2. 20,5
Tb 1. 0 2. 0
Tc 1. 14,8kohm 2. 14,8

ta 23,1
tc 12,2
jeweils beide richtungen gleich
```

## Übergang zu Blatt 05

Nächster Schwerpunkt **Q2-Treiber, B21 / B5**: markierte G-/Gate-R-Punkte und die fünf lokalen Treiberkontakte A/B/C/D5/E gemäß Blatt 05. Diese Namen gelten nur am Q2-Treiber und sind nicht die B19-Pads A/B/C. Typcode und tatsächliche Versorgung/Freigabe bleiben zu identifizieren. Weitere GitHub-Übernahme wie vereinbart beim nächsten abgeschlossenen Bauteil-/Blattwechsel.

Die neue Aufnahme wurde vor dem GitHub-Import von EXIF/XMP bereinigt, ohne JPEG-Neukodierung oder Pixeländerungen. Alte Originalfotos, Rasterindex und vorhandene Markerpixel blieben unverändert. Keine Platineninhalte wurden generiert; der Assistent hat selbst keine elektrische Messung durchgeführt.
