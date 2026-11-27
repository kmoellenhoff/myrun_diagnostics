# Fotoatlas GIRT S6T30

> **Hinweis:** Die Übersichts-PDF ([GIRT_Platinen_Uebersicht.pdf](../GIRT_Platinen_Uebersicht.pdf), Stand 27.11.2026, v3) ist auf dem Reparaturstand. Ergänzend gelten [HARDWARE.md](../HARDWARE.md) und der [Schaltplan](../schaltplan/README.md). Das Koordinatenraster A–L / 1–6 und die Bauteil-IDs (F = Vorderseite, B = Rückseite) gelten unverändert.

**Alle 110 Originalfotos sind erfasst:** 57 Rückseite, 41 Vorderseite, 3 Q2, 7 verkleinerte Inspektionsfotos und 2 Übersichtskopien. Originaldateien und ursprünglicher Rückseitenindex bleiben unverändert.

**Foto-Nachtrag 09.11.2026:** [Zwei weitere Aufnahmen von P600-Buchse und Kabelstecker](../../photos/2026-11-09/p600/README.md), vor dem GitHub-Upload von EXIF/Metadaten bereinigt. Der folgende Index und Kontaktatlas bleiben der historische Bestand vom 08.11.2026.

[Kontaktatlas als PDF](kontaktatlas.pdf) · [Vollständiger Index CSV](fotoindex.csv) · [Bauteil-/Foto-Suchindex](bauteil_fotoindex.csv) · [Registrierungen/Originalprüfsummen JSON](registrierungen.json) · [Schaltplan](../schaltplan/README.md)

| Teil | Fotos |
|---|---|
| [Rückseite](Rueckseite.md) | 57 |
| [Vorderseite](Vorderseite.md) | 41 |
| [Q2-Makros](Q2.md) | 3 |
| [Inspektionsmakros](Inspektion.md) | 7 |
| [Übersichtskopien](Uebersichten.md) | 2 |

## Vorgehen und Gewissheit

1. Bestehende Übersichten `docs/img/overview_front.jpg` und `overview_back_upright.jpg` sind die Referenz. Claudes A–L/1–6-Raster, F-/B-Bauteil-IDs und Ausrichtungen bleiben erhalten. Rückseite aufrecht: Zeilen 6 oben bis 1 unten; Vorderseite wie fotografiert: 1 oben bis 6 unten.
2. Die SIFT/RANSAC-Registrierung ordnet **ein Foto derselben Platinenseite** zur bestehenden Übersicht zu. Es wurde keine neue geometrische Kalibrierung zwischen Vorder- und Rückseite eingeführt. Bei schwachem Direktabgleich erfolgt eine dokumentierte Verkettung über ein überlappendes Original-Nachbarfoto.
3. Bildabgleich braucht genügend verteilte Inlier, geringe Residuen und ein plausibles konvexes Bildfenster. Selbst ein freigegebener Treffer ist nur eine grobe Lokalisierung (weiterhin etwa ±1 Feld), kein Nachweis jedes verdeckten Bauteils oder einer Leiterbahn.
4. Eindeutige Aufdrucke/Bauformen erlauben zusätzlich eine visuelle **Bereichs-/Bauteilzuordnung**. Mehrere Felder bedeuten dabei sichtbare Bereiche, nicht einen exakt vermessenen Bildmittelpunkt. Bei Q2/P600 und den OC-Seitenansichten verhindert Bestückung eine überall gültige Ebene; dort wird kein geometrischer Eckpunktanspruch erhoben.
5. Alte Mittelfeld-/Eckwerte stehen unverändert in eigenen CSV-Spalten. Größere Abweichungen werden separat ausgewiesen und begründet; ein alter Fehlmatch verschiebt das Platinenraster nicht. Neue Werte sind im neuen Index, nicht im Originalindex gespeichert.
6. `Projizierte_Bereiche_nicht_Sichtbarkeitsbeleg` ist eine Suchhilfe aus Feldmittelpunkten, keine Bauteilidentifizierung. `median_error_px` ist ein RANSAC-Residuum des jeweiligen Abgleichs; bei einer Verkettung im skalierten Nachbarfoto, nicht eine physikalische Genauigkeit in mm. Beide Homographien können Fehler beitragen.

**Zuordnungsstand:** 110 Fotos mit Bereichs-/Rasterzuordnung; 0 ohne belastbare Lage. 3 größere Abweichungen vom alten Mittelfeld werden unten aufgeführt. Fehlende oder unsichere Pin-/Bauteilfunktionen bleiben auch bei guter Fotolage offen.

## Bauteil-/Foto-Suche

`bauteil_fotoindex.csv` führt alle 53 F-/B-Bereiche aus Claudes Übersicht mit unverändertem Feld. Explizite visuelle Zuordnungen und bloße Treffer des Feldmittelpunkts im projizierten Fotofenster stehen in getrennten Spalten. Ein Fenster-Treffer beweist bei Bestückung/Kühlkörper keine Sichtbarkeit.

## Abweichungen vom bisherigen Rückseitenindex

Diese Bilder werden nicht stillschweigend an den alten Mittelfeldern festgehalten. Die Tabelle enthält Altwert und Nachbarfoto-Abgleich. Die Bildlage ist eine geometrische/visuelle Auswertung, keine elektrische Messung.

| Foto | Altes Mittelfeld | Neuer Abgleich | Referenz / Prüfung |
|---|---|---|
| [PHOTO003](../../photos/2026-11-08/back/PXL_20261108_153802461.jpg) | G4 | L5 | 45 Inlier über `photos/2026-11-08/back/PXL_20261108_153750178.jpg`; Originalindex abweichend: G4; Nachbarfoto-Abgleich L5; visuell bestätigt; [Bildnachweis](abgleich/PHOTO003.jpg) |
| [PHOTO012](../../photos/2026-11-08/back/PXL_20261108_153832358.jpg) | G4 | I5 | 100 Inlier über `photos/2026-11-08/back/PXL_20261108_154119736.jpg`; Originalindex abweichend: G4; Nachbarfoto-Abgleich I5; visuell bestätigt; [Bildnachweis](abgleich/PHOTO012.jpg) |
| [PHOTO047](../../photos/2026-11-08/back/PXL_20261108_154029418.jpg) | H3 | A2 | 114 Inlier über `photos/2026-11-08/back/PXL_20261108_154053061.jpg`; Originalindex abweichend: H3; Nachbarfoto-Abgleich A2; visuell bestätigt; [Bildnachweis](abgleich/PHOTO047.jpg) |

## Noch nicht eindeutig lokalisierte Fotos

Kein Foto bleibt ohne grobe Bereichszuordnung. Das ist ausdrücklich keine vollständige Zuordnung aller Bauteilanschlüsse: verdeckte Bahnen, unlesbare Codes und Ebenenwechsel bleiben in Schaltplan offen.

## Originale und Prüfbarkeit

Vorschauen sind verkleinerte, ungedrehte Kopien mit Foto-ID und Zuordnung in einem zusätzlichen Rand. Es wurden keine Platinenbilder generiert. Die Originalfotos wurden nur gelesen. `registrierungen.json` enthält für jedes Original die SHA-256-Prüfsumme, Quelle, Methode und gegebenenfalls die Transformation in die bestehende Übersicht. Die ursprüngliche Datei `photos/2026-11-08/back_raster_index.csv` ist unverändert.

Der Schaltplan verwendet ausschließlich ausdrücklich belegte Verbindungen. Ein gutes Bild-Matching ergänzt keine unsichtbare Leiterbahn und identifiziert keinen unbekannten IC-Pin.

### Neue Rückseitenaufnahme B20, 09.11.2026

[50370.jpg und Zuordnung](../../photos/2026-11-09/b20/README.md), vor dem Import ohne EXIF/XMP bereinigt, Bildpixel unverändert. B20 / E6 bleibt unverändert; der historische Index der 110 Fotos wird nicht umnummeriert.

### Neues Q2-Rückseitenmakro, 09.11.2026

[50386.jpg ohne EXIF und mit Zuordnung](../../photos/2026-11-09/q2/README.md), Q2/B21/B5 unverändert. Historische Foto-IDs und der 110-Foto-Index bleiben erhalten.

### Detail 50396: 1P-Dreibeiner, 09.11.2026

[Originalmakro ohne EXIF und Metadatennachweis](../../photos/2026-11-09/q2/README.md). Q2/B21/B5 unverändert; historischer 110-Foto-Index bleibt unverändert.
