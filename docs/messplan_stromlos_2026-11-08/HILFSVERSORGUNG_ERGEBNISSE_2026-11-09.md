# Blätter 06/07: Hilfsversorgungen und Massebezüge – 09.11.2026

**Der gemessene stromlose Block ist dokumentiert.** Die Messwerte aller acht Blätter einschließlich 05b sind damit erfasst; die nicht durchgeführten Sicht-, ESR-, Last- und einzelnen Steckkontaktprüfungen bleiben offen. Kein verursachendes defektes Bauteil nachgewiesen. Claudes Raster und die bisherigen Foto-/Bauteil-IDs bleiben unverändert.

[Ergebnis-CSV](messprotokoll_2026-11-09.csv) · [markierte Originalkontakte Blatt 06](makros/06.png) · [Blatt 07](makros/07.png) · [Messplan mit aktuellem Stand](MESSPLAN.md) · [Teilschaltplan](../schaltplan_110926/README.md)

## Ergebnisse

Erste Anzeige Rot am zuerst genannten Messpunkt, Gegenrichtung umgepolt, entsprechend dem laufenden Auftrag. Stromlos, in-circuit. Temperatur, genaue Ablesezeit und Verlauf/Endwert wurden für diesen Block nicht mitgeteilt; eine Zahl allein wird nicht als nachgewiesen eingeschwungen bezeichnet.

| Mess-ID | Rot → Schwarz | Anzeige | Gegenrichtung | Steckzustand |
|---|---|---:|---:|---|
| SUP-01 | 0VA → +5VA | 2,18 kΩ | 2,57 kΩ | nicht vollständig mitgeteilt |
| SUP-03 | **0V24 → +24V** | **37,49 kΩ** | **47,5 kΩ** | Gehäuselüfter an P400 gesteckt |
| SUP-04 | **0V24 → 0VA** | **0 Ω** | **0 Ω** | P400 weiterhin gesteckt laut vorheriger Angabe; weitere Steckzustände offen |

Die Schreibweise „0v24 -24v“ wird als Messpunktpaar 0V24/+24V verstanden, nicht als neu entdeckte negative Versorgung. Die tatsächlich berichtete Polung SUP-03 ist umgekehrt zur ursprünglichen Vorlagenzeile +24V→0V24; die Werte werden deshalb nicht vertauscht.

## Einordnung

- **+5VA-Rail:** 2,18/2,57 kΩ reproduziert exakt die vorherige Messung Q2-DRV.B (=0VA) gegen +5VA. Historische Referenz 2,16/2,55 kΩ liegt nahe. Kein neuer niederohmiger Kurzschlussbefund aus dieser Anzeige; keine Aussage über Ausgangsspannung, Welligkeit oder Verhalten unter Last.
- **24-V-Rail:** 37,49/47,5 kΩ sind effektive Werte des ganzen angeschlossenen Netzes. Der Nutzer bestätigt **P400 als Anschluss des Gehäuselüfters**, Lüfter gesteckt. Seine Elektronik und andere Schaltungspfade können zur Anzeige beitragen. Ein numerischer Sollwert ist unbekannt. Die Werte beweisen weder einen defekten Lüfter noch dessen Funktion oder eine funktionierende Versorgung.
- **Massebezug:** 0V24 und 0VA sind im geprüften Aufbau beidseitig mit 0 Ω verbunden. Für diesen Steckzustand haben die Messpunkte denselben Bezug. Die frühere offene Frage ist dadurch im gemessenen Umfang beantwortet. Eine galvanisch getrennte 24-V-Masse darf daraus nicht angenommen werden. Der physische Weg der Verbindung und die abgesteckte Platine wurden nicht separat untersucht.
- **Grenzen:** Kein ESR-/Kapazitätsnachweis, keine neue dokumentierte Elko-/Regler-Sichtprüfung und keine Bestätigung dynamischer Spannung oder Startverhalten. Ein intermittierender Versorgungs- oder Freigabefehler bleibt möglich.

## Bestätigtes Fragment und Beleggrenze

```text
0V24 ─── 0 Ω beidseitig [M, geprüfter Steckzustand] ─── 0VA

0VA → +5VA:   2,18 / 2,57 kΩ [M, gesamtes Netz]
0V24 → +24V: 37,49 / 47,5 kΩ [M, P400-Gehäuselüfter gesteckt]
```

Die Null-Ohm-Verbindung ist ein elektrischer Befund im Aufbau, keine nachträglich erfundene Fotoleiterbahn. Die kΩ-Werte sind Messkopplungen, keine eingezeichneten Einzelwiderstände und keine Kurzschlüsse zwischen Versorgung und Masse. 0VISO bleibt ein eigener, hier nicht geprüfter Name.

Die im ursprünglichen Blatt 07 vorgeschlagenen Paare Testloch→P400-schwarz/rot (**SUP-02a/b**) wurden nicht separat berichtet. Die gemessenen 24-V-Punkte wurden vom Nutzer als die beschrifteten Punkte direkt neben P400 bezeichnet. Eine bestimmte Steckkontakt- oder Relais-Spulenanbindung ist damit nicht neu gemessen. Vorhandene 10-V-Elkos werden weiterhin nicht allein aus ihrer Nähe einem +24-V-Netz zugeordnet.

## Nutzer-Rohangaben

```text
Blatt 6 :
0VA-5VA 2,18 kohm; invertiert 2,57
Blatt 7: P400 ist Anschluss gehäuse. lüfter. dieser steckt.
direkt daneben
0v24 -24v: 37,49kohm; 47,5kohm

0v24-0va beide richtungen 0 ohm
```

## Fortsetzung

Der bisherige Plan liefert noch keinen eindeutigen defekten Bauteil. Sinnvoll bleiben die konkrete Versorgung und Eingänge des Q2-Gatebausteins, die dokumentierte Sichtprüfung der Hilfsversorgung und gegebenenfalls der Einfluss von Verschmutzungen. [FAN3100C ist inzwischen ein gut passender Kandidat mit bedingtem Pinabgleich](../netlist/q2_treiber_fan3100c_kandidat.md); Versorgung am lokalen Kontakt C und Eingangswege wären dadurch gezielt verfolgbar. Typannahme weiter belegen; keine Live- oder Einspeiseprüfung aus einem ungesicherten Typ ableiten. Die im Repository zurückgestellten Betriebsmessungen bleiben zurückgestellt.

Originalfotos, Rasterindex und markierte Makrokopien sind unverändert. Neue Platinenbilder wurden nicht erzeugt. Der Assistent hat selbst keine elektrische Messung durchgeführt.
