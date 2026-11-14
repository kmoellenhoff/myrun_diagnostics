# Messergebnisse vom 09.11.2026 – Blatt 01, RT334024

**Status:** Blatt 01 stromlos abgearbeitet; beim Übergang zu Blatt 02 dokumentiert. Quelle sind die vom Eigentümer im Chat berichteten Messwerte. Berichtsdatum 09.11.2026; genaue Messzeit, Temperatur, Zeitverlauf und aktueller Prüfspitzenwiderstand wurden nicht mitgeteilt. Keine Werte wurden durch die Auswertung selbst gemessen.

[Messplan und Kontaktbilder](MESSPLAN.md#blatt-01--rt334024-spule-und-kontaktpins) · [Ergebnis-CSV](messprotokoll_2026-11-09.csv) · [markiertes Originalmakro](makros/01.png)

Bauteil **F27**, Claudes Feld **I4**. Rote Prüfspitze ist jeweils der zuerst genannte Anschluss. Die Werte werden als angezeigte In-Circuit-Werte übernommen, ohne nachträgliche Prüfspitzenkorrektur.

| Mess-ID | Rot | Schwarz | Anzeige | Gegenrichtung | Einordnung |
|---|---|---|---|---|---|
| RLY-01 | Ca | Cb | 1,41 kΩ | 1,41 kΩ | Plausibler Spulenwiderstand; beide Richtungen gleich |
| RLY-02 | 11a | 11b | 0 Ω | 0 Ω | Gemeinsame Leiterbahn zwischen den beiden Pads bestätigt |
| RLY-03 | 14a | 14b | 0 Ω | 0 Ω | Gemeinsame Leiterbahn zwischen den beiden Pads bestätigt |
| RLY-04 | 11a | 14a | 68,4 Ω | 68,4 Ω | Symmetrischer Widerstand zwischen den Kontaktseiten |
| RLY-04b | 11b | 14b | 68,4 Ω | ebenfalls 68,4 Ω, zusammenfassend berichtet | Bestätigt den Wert an den jeweils anderen Pads |
| RLY-04c | 11a | 14b | 68,4 Ω | 68,4 Ω | Weitere berichtete Kreuzkombination |

11b–14a wurde nicht als zusätzliche, ausdrücklich einzeln berichtete Messung eingetragen. Aufgrund der gemessenen 0-Ω-Verbindungen innerhalb beider Padpaare ist derselbe Wert elektrisch zu erwarten; das ist eine Ableitung und keine weitere Rohmessung.

## Interpretation

**Spule:** Der Hersteller-Nennwert beträgt 1,44 kΩ bei 23 °C, Toleranz ±10 % (1,296–1,584 kΩ). Die gemeldeten 1,41 kΩ liegen rund 2,1 % darunter und passen dazu. Eine Spulenunterbrechung oder ein harter Spulenkurzschluss wird durch diesen Wert nicht gestützt. Eine tatsächliche Temperatur- oder Kennlinienprüfung liegt nicht vor; bei der eingelöteten Spule können zusätzliche Pfade beteiligt sein.

**Pad-Doppelpaare:** Die 0 Ω zwischen 11a/11b sowie 14a/14b bestätigen die gemeinsame Leiterbahn je Paar. Damit ist kein Schließen des inneren Relaiskontakts nachgewiesen.

**Kontaktseiten:** 68,4 Ω in beiden Richtungen passen sehr gut zum dokumentierten 68-Ω-Vorladewiderstand als möglichem Parallelpfad zum unbestromten Relaiskontakt. Die nominelle Abweichung beträgt etwa +0,6 %. Diese Interpretation ist plausibel, jedoch wurde der Pfad über den konkreten 68-Ω-Bauteil nicht separat verfolgt bzw. gemessen. Aus einem Widerstand zwischen zwei Knoten wird deshalb kein zusätzlicher einzelner Widerstand als belegt in den Schaltplan eingefügt.

Der gemessene Querwiderstand spricht gegen einen dauerhaft niederohmig geschlossenen Kontakt zwischen diesen Padgruppen. **Ob das Relais bei Ansteuerung zuverlässig anzieht, der Kontakt schließt und unter Last niederohmig bleibt, ist weiterhin offen.** Ein verschlissener oder nicht anziehender Kontakt kann stromlos dieselben Werte zeigen.

**Gesamtbewertung:** Bei den vorgesehenen stromlosen Messungen kein auffälliger Befund am RT334024. Das ist keine vollständige Funktionsfreigabe des Relais und schließt intermittierende Fehler nicht aus.

## Rohangaben des Eigentümers

> erster werd ist mit roter spitze gemessen:
>
> 11a -11b= 0 ohm
> 11b - 11a= 0 ohm
> 14a -b =0ohm
> 14b-a=0ohm
> beides nicht verwundderlich weil uf einer leiterbahn
>
> 11a-14a=68,4 ohm
> invers und an 11b und 14b ebenfalls; 11a gegen 14b und andersherum ebenfalls 68,4

> ca - cb=  1,41 kohm = cb-ca

## Weiterer Ablauf

Als Nächstes wird **Blatt 02 – P600/NTC** bearbeitet. Die Ergebnisse dieses noch laufenden Bauteils werden gemäß Absprache erst nach dessen Abschluss und dem nächsten Blattwechsel in GitHub eingepflegt. Die ursprüngliche CSV-Vorlage und das Messplan-PDF bleiben als Planstand vom 08.11.2026 erhalten; ausgefüllte Ergebnisse stehen separat in diesem Nachtrag.
