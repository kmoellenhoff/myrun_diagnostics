# Vorschlag zur Repository-Struktur

**ENTWURF auf `aufraeumen`, 21.11.2026. Nichts archiviert, verschoben, gelöscht oder umbenannt. Bestehende Dateien bleiben unverändert. Merge erst nach Freigabe.**

**Ursache wahrscheinlich C602, Stand: Gegenversuch offen.** Eine vermutete Reparatur ist kein Grund, frühere Rohdaten oder widersprechende Befunde auszusortieren. Der geplante Gegenversuch ist im [aktuellen Protokoll](LAUF_2026-11-21.md) noch nicht als abgeschlossenes Ergebnis dokumentiert.

## 1. Einstieg statt sofortiger Umbau

Vorerst genügt eine verständliche Navigation über fünf neue Entwürfe:

| Einstieg | Aufgabe |
|---|---|
| [README-Entwurf](../README_ENTWURF.md) | Erste Orientierung, Ursachenstand, sichere Unterscheidung der Skriptmodi |
| [ZUSAMMENFASSUNG.md](ZUSAMMENFASSUNG.md) | Reparaturgeschichte ohne Wiederholung jedes Messschritts |
| [FEHLERCODES.md](FEHLERCODES.md) | Beobachtete Meldungen und Vergleichshypothesen getrennt |
| [SKRIPTE.md](SKRIPTE.md) | Optionen, Ausgaben und nur vorgeschlagene Codebereinigung |
| Diese Datei | Mögliche spätere Ordnung und deren Voraussetzungen |

Die neuen Übersichten ersetzen keine Primärprotokolle. Titel und Versionshinweise sind verlässlicher als stilles Entfernen älterer Einschätzungen. Das ursprüngliche Root-README bleibt auf diesem Branch unverändert.

## 2. Unverändert auffindbar halten

| Bestand | Warum behalten / vorerst nicht verschieben |
|---|---|
| `docs/LAUF_*.md` | Chronologie, Nutzerkorrekturen, tatsächliche Messbedingungen, geplanter Gegenversuch. Frühere Bewertungen sind nicht automatisch aktuelle Tatsachen. |
| `docs/logs_2026-11-10/`, `logs_2026-11-11/`, `logs_2026-11-14/`, `logs_2026-11-19/`, `logs_2026-11-21/` | Rohbelege für Fehlstart, Standby-Fehler, Handtest und erfolgreichen Profil-Lauf. TXT und CSV paarweise erhalten; die Formate enthalten unterschiedliche Informationen. Die verkürzten Namen in dieser Zelle liegen jeweils ebenfalls unter `docs/`. |
| `photos/` samt Datumspfaden und Indizes | Originalfotos und Quellenzuordnung bleiben unverändert. Metadatenstatus nur aus vorhandenen Fotoprotokollen übernehmen; keine Originaldatei neu speichern. |
| `docs/atlas_110926/` | Gemeinsames Raster, Foto-IDs, Zuordnungen und Herkunft. Historischer Verzeichnisname ist Teil bestehender Verweise, kein Grund zur Umbenennung. |
| `docs/gesamtschaltplan_110926/` | Aktuelles Rekonstruktionsmodell und separates B10-Ist-Blatt, Quellen-CSV, Generator, PDFs/SVGs/XMLs, Netze und Prüfnachweise gehören zusammen. Original- und Umbauansicht nicht zu einem Parallelstromkreis verschmelzen. |
| `docs/mcu_skizze_2026-11-16/` | Definition der MCU-Arbeitsnummern, keine Datenblatt-Pinbelegung. Darauf bauen Verweise auf. |
| `docs/netlist/` und `docs/messprotokoll_2026-11-17.csv` | Rohmesswerte, ursprüngliche Netze und jüngere Betriebsbefunde; später korrigierte Zuordnungen bleiben nachvollziehbar. |
| `docs/messplan_stromlos_2026-11-08/` | Historische Messblätter und Originalbeschriftungen, teilweise aktive Eingaben des Schaltplangenerators. Nicht pauschal nach Datum archivieren. |
| `docs/schaltplan_110926/verbindungen.csv` | Trotz historischen Ordnernamens weiterhin **aktive Generatoreingabe**. Ein Verschieben des ganzen alten Schaltplanordners würde die Reproduktion brechen. |
| `docs/fotospuren_2026-11-12/` | Separater Fotoentwurf mit eigenen F-/I-Grenzen. Nicht mit bestätigten Kupfernetzen gleichsetzen oder als bloße Dublette behandeln. |
| Sechs Root-Skripte, `LICENSE`, `CLAUDE.md` | Existierende Aufrufe, Verhalten und Lizenz erhalten. Gemeinsame Funktionen wären ein späteres Codeprojekt, keine Dateiverschiebung in diesem Entwurf. |

## 3. Denkbare Archivkandidaten – erst nach Freigabe

Ein möglicher späterer Zielbereich wäre `docs/archiv/`. Er wird hier **nicht angelegt**. Archiv bedeutet weiterhin versioniert und verlinkt erreichbar, nicht gelöscht und nicht aus der öffentlichen Historie entfernt.

| Kandidaten | Denkbares Ziel / Nutzen | Voraussetzung |
|---|---|---|
| Frühe `NEUBEWERTUNG_2026-11-11.md`, `..._12.md`, `..._14.md` | Historische Bewertungssammlung, damit der aktuelle Einstieg nicht mehrere konkurrierende Hauptverdachte anbietet | Erst nach Gegenversuch und Freigabe; Zusammenfassung und alle relativen Links anpassen; Primärmessungen erhalten |
| `docs/STAND_2026-11-08.md` | Datierter Ausgangsstand in einer Historiengruppe | Nicht überschreiben oder in einen vermeintlich aktuellen Endbericht umdeuten; Generator-/Quellenverweise prüfen |
| Überholte Messpläne wie `docs/ESR_PLAN_2026-11-12.md` und ältere Plan-PDFs | Geplante, nicht zwingend durchgeführte Tests von aktuellen offenen Schritten trennen | Prüfen, welche Schritte noch offen sind; leere Tabellen nicht zu negativen Messbefunden erklären |
| Alte Teilschaltplan-Ansichten unter `docs/schaltplan_110926/` | Historische CAD-/PDF-Ansichten separat auffindbar | Nicht den ganzen Ordner verschieben: aktive CSV-Eingaben, Quellenhashes und bisherige Links zuerst einzeln prüfen |
| Versionierte Blockdiagramme und Renderquellen unter `docs/img/` | Historie von Hypothesen übersichtlicher machen | Varianten, zugehörigen Quellcode und Verweise als Einheit behandeln; keine Fotoreferenz löschen |

Rohlogs und Originalfotos würde ich **nicht** allein wegen eines vermuteten Reparaturerfolgs archivieren. Der Vorher-/Nachher-Vergleich bleibt auch für den Gegenversuch relevant. Aktuelle offene Prüfungen dürfen nicht unter einem historischen Ordner verschwinden.

## 4. Redundanzprüfung

Ein SHA-256-Vergleich der verfolgten Dateien fand genau eine Gruppe bytegleicher Inhalte:

- [block_diagram.png](img/block_diagram.png) und [block_diagram_v6.png](img/block_diagram_v6.png).

Die identischen Bytes bedeuten nicht, dass beide Namen entbehrlich sind: einer kann der aktuelle Verweis, der andere der feste Versionsbeleg sein. **Vorerst beide behalten.** Eine spätere Konsolidierung würde zuerst alle Verweise und die historische Bedeutung klären.

Weitere Inhalte sind eher fachlich überlappend als bytegleich:

| Paar / Gruppe | Bewertung |
|---|---|
| Root-README: „Contents“ und „Usage“ | Viele Skripterklärungen doppelt; einzelne Angaben sind gegenüber dem Code veraltet. README auf Einstieg begrenzen, vollständige Optionen in `SKRIPTE.md` pflegen. |
| `HARDWARE.md` und `HARDWARE.pdf` | Möglicherweise unterschiedliche Änderungsstände; PDF vor einer Kennzeichnung als aktuell gegen Markdown prüfen. Keine identischen Fassungen unterstellen. |
| Alter Teilplan und heutiger Gesamtschaltplan | Unterschiedliche Belegstände. Historie darf bleiben, sollte aber eindeutig als solche verlinkt sein. |
| CAD, SVG, PDF, XML und Modell-JSON | Beabsichtigte Ausgabeformate: bearbeiten, ansehen, drucken, elektrisch prüfen. Nicht als unnötige Mehrfachdateien löschen. Nach Änderungen gemeinsam reproduzieren. |
| `vorschau/`, `abgleich/`, Rasterbilder und Originalfotos | Ableitungen erfüllen andere Zwecke als die Originale. Vor möglicher Neuorganisation prüfen, welche Dateien Render-/Registrierungseingaben und welche nachweislich reproduzierbare Ausgaben sind. |
| TXT-/CSV-Logs | TXT enthält Quittierungen, Rohantworten und Ablauf; CSV einzelne zeitgestempelte Signale. Kein gegenseitiger Ersatz. |
| `Q2_1P_DIODENTEST_AUSSTEHEND.csv` und spätere Diodenbefunde | Der Dateiname beschreibt einen historischen Plan, nicht zwingend den heutigen Messstatus. Datei ist zudem Bestandteil bestehender Generatorprüfungen; nicht löschen oder historische Leerfelder nachträglich füllen. |

## 5. Mögliche spätere Zielstruktur

Nur eine Skizze; **keine dieser Verschiebungen wird ausgeführt**:

```text
README.md                         kurzer deutscher Einstieg nach Freigabe
docs/
  ZUSAMMENFASSUNG.md               aktuelle, belegte Übersicht
  FEHLERCODES.md                   Beobachtung / H-Vergleich getrennt
  SKRIPTE.md                       vollständige Bedienung und Ausgabeformate
  LAUF_*.md                       weiterhin datierte Primärprotokolle
  logs_<Datum>/                   weiterhin Rohbelege pro Sitzung
  gesamtschaltplan_110926/         aktuelles Modell und Reproduktion
  atlas_110926/                   vorhandene Fotozuordnung
  archiv/                         nur später freigegebene historische Ansichten
photos/                           unveränderte Originalquellen
myrun_*.py                        bestehende Einstiegspunkte bleiben erhalten
```

Eine zusätzliche Python-Bibliothek für gemeinsame Funktionen wäre eine **getrennte spätere Codeänderung**, z. B. für Parser, Transport und Logging. Die vorhandenen Kommandozeilenprogramme und Ausgabeschlüssel müssten kompatibel bleiben; siehe [Vorschläge und Tests](SKRIPTE.md#9-aufräumvorschläge--nicht-umgesetzt).

## 6. Datenschutz und Freigabekriterien

Der Altbestand enthält gerätebezogene BLE-Kennungen und teilweise lokale Pfadangaben in Programmen/Reports. Diese Werte werden hier nicht wiederholt. Das ist ein gesonderter Veröffentlichungsprüfpunkt, kein Anlass, im Entwurfsbranch Rohbelege zu überschreiben. Eine spätere öffentliche Exportkopie könnte Kennungen redigieren und ihre Herkunft dokumentieren. Eine Archivverschiebung entfernt private Daten **nicht** aus Git-Historie oder Öffentlichkeit.

Neue Fotos wären nur als gesonderte, metadatenbereinigte Veröffentlichungskopien hinzuzufügen; vorhandene Originalfotos bleiben unverändert. Für die fünf Entwürfe wurden keine Fotos erzeugt, hochgeladen oder neu gespeichert.

Vor einer späteren Umsetzung: Gegenversuch als Ergebnis protokollieren, Ursache gegebenenfalls neu bewerten, Vorschlag ausdrücklich freigeben, alle Referenzen/Generatorquellen prüfen und Originaldateien vor/nach Änderungen vergleichen. Erst dann getrennte, nachvollziehbare Umstrukturierungscommits planen. Dieser Branch liefert ausschließlich Vorarbeit und wird nicht automatisch nach `main` gemergt.
