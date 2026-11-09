# Blatt 03: B18/B19 – Ergebnisse vom 09.11.2026

**Im geprüften stromlosen Umfang abgeschlossen; als Nächstes Blatt 04 (B20).** Quelle sind die im Chat berichteten Nutzer-Messungen und zwei dort gezeigte neue Originalmakros. Der Assistent hat selbst keine elektrische Messung ausgeführt. Der Endwert P2–0VA bleibt offen. Ein verursachendes defektes Bauteil ist nicht nachgewiesen.

[Messwerte als CSV](messprotokoll_2026-11-09.csv) · [korrigierter Messplan](MESSPLAN.md#blatt-03--b18--b19-knoten-und-erster-widerstand) · [aktueller Teilschaltplan](../schaltplan_110926/README.md) · [B18-Netzliste mit Historie](../netlist/b18_spannungssense_kandidat.md)

## Korrektur und Anschlussbezeichnungen

Der zunächst als `1001 = 1 kΩ` gelesene B19-Widerstand E1–E2 trägt **1003 = 100 kΩ**. Der frühere Planwert war ein Lesefehler. Auch der benachbarte Widerstand trägt 1003. Diese Korrektur betrifft B19; der 1001 im Q2-Treiberumfeld bleibt unverändert.

Die folgenden Richtungen beziehen sich auf das neue Nutzerfoto mit dem L4981AD links und den beiden 1003 oben. Sie ersetzen weder Claudes Raster A–L × 1–6 noch die vorhandenen Bauteil-IDs. Die alten Messplanmarker E1/E2 behalten ihre Quellpixel.

| Lokale Foto-ID | Anschluss |
|---|---|
| E1 | obere Endkappe des rechten 1003, P1-Seite |
| E2 | untere Endkappe desselben 1003 |
| B19-Pad A | Rundpad links neben den 1003; E2 und obere Endkappe des linken 1003 elektrisch bestätigt |
| B19-Pad B | Rundpad links am 3922; untere Endkappe des linken 1003 und L4981AD Pin 14 elektrisch bestätigt |
| B19-Pad C | Rundpad rechts/unterhalb des 4750; Bahn zum rechten Ende 4750 sichtbar [F] |
| 0VA | rechte Endkappe 3922 und linke Endkappe 4750 jeweils mit 0 Ω bestätigt |

A/B/C sind ausschließlich lokale B19-Padnamen, keine Q2-Treiberanschlüsse und keine neuen Rasterfelder. [M] = gemessen, [F] = sichtbare Bahn, [I] = Code/Hersteller-Pinout. Sichtbare, eindeutige Leiterbahnen werden als F geführt; zusätzliche Durchgangstests sind für unklare oder diagnostisch wichtige Strecken vorgesehen.

## Messwerte

Alle Angaben in-circuit, stromlos laut angekündigtem Ablauf. Leere Gegenrichtung bedeutet **nicht berichtet**, nicht OL und nicht automatisch gleicher Wert. Temperatur, genaue Ablesezeit und Steckzustände wurden für diesen Block nicht detailliert mitgeteilt. Bei nicht ausdrücklich genannter Anfangspolung bezeichnet die Tabellenrichtung nur das Anschlusspaar; siehe Hinweis in der CSV.

| Mess-ID | Anschlusspaar | erste Richtung | Gegenrichtung | Verlauf / Hinweis |
|---|---|---|---|---|
| PATH-01 | B18-P1 → B19-E1 | 0,4 Ω | nicht berichtet | nicht mitgeteilt |
| PATH-02.start | B19-E1 → B19-E2 | 97,6 kΩ | nicht berichtet | Erste Messung; später separat wiederholt. Gegenrichtung hier nicht berichtet. |
| B19-P1E2.start | B18-P1 → B19-E2 | 97,6 kΩ | nicht berichtet | Nutzer setzte P1–E2 und E1–E2 gleich; beide Angaben erhalten. |
| B18-01.repeat | B18-P2 → 0VA | bis 6 MΩ, dann fallend | nicht berichtet | Kein eingeschwungener Endwert und keine Gegenrichtung berichtet. |
| PATH-02.repeat | B19-E1 → B19-E2 | 102,6 kΩ | 90,4 kΩ | Rechter 1003 in der Orientierung des neuen Nutzerfotos; Code 1003 = 100 kΩ. |
| B19-R1003links | B19-1003links.oben → B19-1003links.unten | 102,6 kΩ | 90,4 kΩ | Als gleiche Werte wie E1–E2 berichtet; Rot oben, Schwarz unten. |
| B19-R3922 | B19-3922.Ende1 → B19-3922.Ende2 | 38,43 kΩ | 38,91 kΩ | Welches physische Ende bei der ersten Richtung rot war, wurde nicht mitgeteilt. Code 3922 = 39,2 kΩ. |
| B19-R1004oben | B19-1004oben.Ende1 → B19-1004oben.Ende2 | 498 kΩ | 498 kΩ | Absolute Anfangspolung nicht mitgeteilt; nominal 1 MΩ. Parallelverbindung separat bestätigt. |
| B19-R1004unten | B19-1004unten.Ende1 → B19-1004unten.Ende2 | 496 kΩ | 496 kΩ | Absolute Anfangspolung nicht mitgeteilt; nominal 1 MΩ. Parallelverbindung separat bestätigt. |
| B19-R4750 | B19-4750.Ende1 → B19-4750.Ende2 | 478 Ω | 478 Ω | Vom Nutzer ausdrücklich von 478 kΩ auf 478 Ω korrigiert. Anfangspolung nicht mitgeteilt; Code 4750 = 475 Ω. |
| B19-PAR-L | B19-1004oben.links → B19-1004unten.links | 0 Ω | nicht berichtet | nicht mitgeteilt |
| B19-PAR-R | B19-1004oben.rechts → B19-1004unten.rechts | 0 Ω | nicht berichtet | nicht mitgeteilt |
| B19-AB | B19-PadA → B19-PadB | 98,4 kΩ | 94,7 kΩ | nicht mitgeteilt |
| B19-AC | B19-PadA → B19-PadC | 135 kΩ | 130 kΩ | nicht mitgeteilt |
| B19-CB | B19-PadC → B19-PadB | 39 kΩ | 39 kΩ | nicht mitgeteilt |
| B19-A0 | B19-PadA → 0VA | 134,8 kΩ | 130 kΩ | nicht mitgeteilt |
| B19-B0 | B19-PadB → 0VA | 38,7 kΩ | 38,6 kΩ | nicht mitgeteilt |
| B19-C0 | B19-PadC → 0VA | 478 Ω | 478 Ω | Einheit vom Nutzer ausdrücklich auf Ohm berichtigt. |
| B19-4750-GND | B19-4750.links → 0VA | 0 Ω | nicht berichtet | Linkes Ende = Ende in Richtung 3922 im neuen Nutzerfoto. |
| B19-3922-GND | B19-3922.rechts → 0VA | 0 Ω | nicht berichtet | nicht mitgeteilt |
| B19-AE2 | B19-E2 → B19-PadA | 0 Ω | nicht berichtet | Explizit als E2 und Pad präzisiert; Anfangspolung nicht angegeben. |
| B19-A1003 | B19-PadA → B19-1003links.oben | 0 Ω | nicht berichtet | Beide folgenden Verbindungen als „beide 0 ohm“ zusammenfassend bestätigt. |
| B19-B1003 | B19-PadB → B19-1003links.unten | 0 Ω | nicht berichtet | Beide Verbindungen zusammenfassend bestätigt. |
| B19-B14 | B19-PadB → L4981AD.14 VFEED | 0 Ω | nicht berichtet | nicht mitgeteilt |

## Bestätigter und sichtbarer Schaltungsverlauf

```text
L+ = B18-P2 [M, 08.11.]
 ─ 1 MΩ (1004) ─ TP1 ─ 1 MΩ (1004) ─ 475 kΩ (4753) ─ B18-P1 [F]
 ─ 0,4 Ω [M] ─ E1 ─ 100 kΩ (1003 rechts) ─ E2 = Pad A [M]
 ─ 0 Ω [M] ─ obere Endkappe 1003 links
 ─ 100 kΩ (1003 links) ─ untere Endkappe = Pad B [M]
 ─ 3922 / 39,2 kΩ [F, Code I] ─ 0VA [M]

Pad B ─ 0 Ω [M] ─ L4981AD Pin 14 (VFEED [Hersteller-Pinout])
0VA ─ 4750 / 475 Ω ─ Pad C [F]; weitere Funktion C offen

Zwei weitere B19-1004: links–links 0 Ω, rechts–rechts 0 Ω [M].
Daher parallel: nominal 1 MΩ || 1 MΩ = 500 kΩ.
Einbindung dieser beiden gemeinsamen Netze in die übrige Schaltung offen.
```

Herstellerquelle: [ST L4981-Datenblatt](https://www.st.com/resource/en/datasheet/l4981.pdf), L4981AD in SO20, Pin 14 VFEED (Spannungsrückführung), Pin 3 OVP. Die Verbindung zu Pin 14 ist gemessen; ein bestimmter OVP-Pfad an Pin 3 wurde nicht nachgewiesen. Pin 10 S-GND wurde nicht separat zu 0VA gemessen. +5VA ist nicht automatisch mit Pin 11 VREF gleichzusetzen.

## Einordnung und offene Punkte

- **PFC-Spannungsrückführung identifiziert:** Der Weg von B18/B19 endet an VFEED. Das ist mehr als eine vermutete MCU-Auswertung. Die Funktion im Betrieb und das Fehlstartverhalten sind damit noch nicht geprüft.
- **1003:** 102,6/90,4 kΩ bzw. 98,4/94,7 kΩ zwischen A/B sind In-Circuit-Anzeigen mit Polungsabhängigkeit. Sie beweisen weder den exakten Einzelwert noch einen Defekt. Die frühere Erwartung von 1 kΩ entfällt.
- **3922:** 38,43/38,91 kΩ und B–0VA 38,7/38,6 kΩ liegen in der Nähe des Nennwerts 39,2 kΩ. Eine kleine parallele Belastung ist möglich; daraus allein folgt kein fehlerhaftes Bauteil.
- **1004-Paar:** 498/496 kΩ passen zum bestätigten Parallelnetz mit nominal 500 kΩ. Die Anzeigen sind keine zwei auf etwa die Hälfte abgesunkenen Einzelwiderstände. Toleranz und zusätzliche Belastung bleiben im eingelöteten Zustand ungetrennt.
- **4750:** korrigiert **478 Ω**, etwa +0,63 % gegen nominal 475 Ω. Auch C–0VA beträgt 478 Ω. Die früher getippte Einheit kΩ ist verworfen.
- **P2–0VA:** nur Ladekurve bis 6 MΩ mit anschließendem Fallen; ohne Endwert keine abschließende Widerstandsbewertung.

Nominales, unbelastetes Modell am Knoten B: R_oben = 1 MΩ + 1 MΩ + 475 kΩ + 100 kΩ + 100 kΩ = **2,675 MΩ**, R_unten = **39,2 kΩ**. Verhältnis B/L+ ≈ **1,444 %**. Rechnerisch entsprechen 5,1 V am Abgriff etwa **353,1 V** am Eingang. Das ist **keine gemessene Betriebsspannung und kein bewiesener realer Sollwert**: Referenzbezug, Belastung, Kompensation und die vollständige Beschaltung sind nicht geklärt. Historische P1–0VA 223,7 kΩ bleiben effektive In-Circuit-Werte; kein physischer 221-kΩ-Widerstand wurde identifiziert.

## Frage nach Verschmutzungen am L4981AD und an Leiterbahnen

Leitfähige oder feuchte Rückstände können Leckströme zwischen Pins, Pads oder freiliegendem Kupfer verursachen und hochohmige Rückführungen beeinflussen. Besonders relevant ist die Umgebung von VFEED/Pad B. Eine intakte Lötstoppmaske isoliert Leiterbahnen; offene Anschlüsse, beschädigte Beschichtung oder Korrosion sind deshalb gezielt anzusehen. Sichtbare Rückstände können auch Flussmittel oder Beschichtung sein: **Aus dem Foto ist ihre Leitfähigkeit nicht bewiesen.**

Reines Rechenbeispiel, keine Messung: 1 MΩ zusätzlich parallel zu 39,2 kΩ ergibt etwa 37,72 kΩ (−3,77 %). Ein Leck zu einem anderen Potenzial kann anders wirken. Die bisherigen Widerstandswerte schließen einen feuchte-/temperaturabhängigen Fehler nicht aus; sie belegen ihn auch nicht.

Bei einer späteren Reinigung: erst vorhandenen Zustand fotografieren und Vergleichswerte festhalten; stromlos und nach geprüfter Restspannung mit einem für Material/Beschichtung geeigneten rückstandsfreiem Reiniger arbeiten. Nach vollständiger Trocknung dieselben Punkte mit gleicher Polung, Temperatur und Ablesezeit vergleichen. Keine Isolationsprüfung mit hoher Prüfspannung an den angeschlossenen IC-Eingängen. Reinigung ist hier noch **nicht durchgeführt** und kein bewiesener Reparaturerfolg.

## Foto- und Datenherkunft

Die zwei neuen B19-Makros liegen im Chat als eingebettete Bilder vor. Ihre Originaldateien sind im verfügbaren Arbeitsverzeichnis nicht zugänglich; sie wurden deshalb **nicht als angeblich gesicherte Originaldateien ins Repository übernommen**. Der korrigierte Plan verwendet weiterhin ausschließlich die unveränderten Repository-Originalfotos und die vorhandenen Kopien mit Markierungen. Keine Platineninhalte wurden generiert, keine Originalfotos geändert. Für einen späteren Fotoimport gilt weiterhin: EXIF vor dem Hinzufügen entfernen.

Die Tabelle und die CSV geben die Nutzerberichte wieder. Insbesondere bleiben die Anfangsmessung 97,6 kΩ und die Wiederholung 102,6/90,4 kΩ getrennt. „Beide 0 ohm“ wurde nur auf die zwei angekündigten Verbindungen A–oberer linker 1003 und B–unterer linker 1003 bezogen. Fehlende Gegenrichtungen oder Temperaturen wurden nicht ergänzt.

## Übergabe

Blätter 01–03 sind im jeweils dokumentierten Umfang abgearbeitet. **Nächster Arbeitsschritt: Blatt 04, B20 / E6** – die vier Widerstände und den SOT-23 anhand eines scharfen Originalmakros lesen, dann gezielt messen. Weitere GitHub-Übernahme wieder am vereinbarten Bauteil-/Blattwechsel. Offene B19-Fragen bleiben im Protokoll erhalten.
