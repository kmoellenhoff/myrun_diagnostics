# Q2-Gatebaustein: FAN3100C als Kandidat

**Stand 09.11.2026: gut passender Kandidat [I], noch keine abschließend gesicherte Typnummer.** Claude-Raster Q2/B21/B5 und lokale Foto-IDs bleiben unverändert. M = gemessen; F = Foto; I = Aufdruck/Herstellerabgleich mit noch bedingter Typannahme.

Quelle ist das [onsemi-Herstellerdatenblatt FAN3100T/D, April 2025 Rev. 6](https://www.onsemi.com/download/data-sheet/pdf/fan3100t-d.pdf), Seiten 1–2. Es nennt für SOT23-5 den Code **100X** mit X=C oder T plus Datumscode M. Das [Nutzerfoto 50386.jpg](../../photos/2026-11-09/q2/50386.jpg) lässt **100C A** erkennen; der Nutzer las **1000CA**. Die zusätzliche Null in der Nutzerlesung bleibt als Rohangabe erhalten. Die Übereinstimmung von Kurzcode, Gehäuse und zwei gemessenen Anschlüssen stützt FAN3100C; sie ersetzt keinen sicheren vollständigen Typabgleich.

## Bedingte Zuordnung im unveränderten Foto

Foto 50386: drei Anschlüsse oben A/B/C von links nach rechts, zwei unten D5/E von links nach rechts. Die Schrift steht in dieser Aufnahme kopfüber. Abgleich mit Top View und Markierungsbild des Herstellers ergibt **unter der FAN3100C-Annahme**:

| Lokale Foto-ID | Kandidaten-Pin | Funktion laut Hersteller | eigener Nachweis |
|---|---:|---|---|
| A | 3 | IN+, nichtinvertierender Eingang | I; Netzfunktion nicht separat gemessen |
| B | 2 | GND | 0 Ω zu 0VA beidseitig [M], passend zum Kandidaten |
| C | 1 | VDD, Versorgung | I; tatsächliche Versorgung weiterhin offen |
| D5 | 4 | IN−, invertierender Eingang | I; Netzfunktion nicht separat gemessen |
| E | 5 | OUT | ≈0 Ω zu RG-U [M]; Gate-Pfad passend zum Kandidaten |

Die konkrete Pinlage wurde am Hersteller-Markierungsbild und der um 180° gedrehten Schriftinspektion abgeglichen. **A ist bei dieser Zuordnung nicht Pin 1.** Lokale Foto-IDs bleiben maßgeblich; keine Pin-Funktion wird als neue elektrische Messung ausgegeben.

## Bedeutung für die Fehlereingrenzung

Laut Datenblatt bleibt der Ausgang bei unzureichender Versorgung oder unpassender Eingangskombination LOW. Der angegebene Betriebsbereich ist 4,5–18 V. Diese Angaben gelten für den Kandidaten, nicht als gemessene Platinenwerte.

Eigene Befunde: B=0VA, E führt zum 22,2-Ω-Gatepfad. C–0VA 1,48/1,45 kΩ und C–+5VA 3,72/2,57 kΩ zeigen keine direkte Verbindung zu +5VA. Der Name +5VA bestimmt deshalb weiterhin nicht automatisch die Treiberversorgung. Eine fehlende Versorgung oder fehlende Eingangsfreigabe ist eine prüfbare Ursache für ausbleibende Gate-Ansteuerung; der IC ist durch die stromlosen Messungen weder als defekt noch als betriebsfähig bewiesen.

**Nächster gezielter stromloser Schritt:** Den sichtbaren Weg von **C** zum unmittelbar benachbarten Kondensator und weiter zum speisenden Netz/Regler verfolgen, dabei F und M trennen. Einen Messpunkt erst für eine konkrete unklare Verbindung anfordern; nicht alle sichtbaren Kupferstücke erneut durchmessen. Vor einer davon abhängigen Pin-Funktionsaussage Typannahme weiter prüfen. Keine Betriebsmessung aus der Kandidatenzuordnung ableiten.

[Alle Q2-Messwerte und Rohkorrekturen](../messplan_stromlos_2026-11-08/Q2_TREIBER_ERGEBNISSE_2026-11-09.md). Kein Bauteiltausch allein aufgrund des Kandidaten.
