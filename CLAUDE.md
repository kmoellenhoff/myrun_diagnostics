# Arbeitsregeln für dieses Repo (myrun_diagnostics)

Sprache: Deutsch. Branch: `main` (Branch `110926` ist gemergt). Aufräumarbeiten laufen auf Branch `aufraeumen`; Vollarchiv: `archiv-vor-aufraeumen-2026-11-27`.

## Schaltplan als Referenz (Anweisung Nutzer, 16.11.2026; Pfade angepasst 27.11.2026)
- **Vor jeder neuen Theorie oder Messentscheidung** den gemeinsamen Schaltplan prüfen:
  `docs/schaltplan/` (README, `gesamtschaltplan.pdf/.svg`, KiCad `GIRT_Gesamtschaltplan.kicad_sch`, Ist-Blatt `B10_Umbau_2026-11-21.kicad_sch`, Netzliste `netze.csv`, `bauteile*.csv`).
  Theorie und Messpunkte müssen zu den dort bestätigten Netzen passen; Widersprüche ausdrücklich nennen.
- **Generator und Belegregister liegen nur noch im Archiv-Branch** `archiv-vor-aufraeumen-2026-11-27` (`docs/gesamtschaltplan_110926/`: `erzeugen.py`, `pruefen_unabhaengig.py`, `befunde_*.csv`, `verbindungsbelege.csv`). Auf `aufraeumen`/`main` nur die Endprodukte.
- **Neue Befunde**: kurzer Nachtrag in `docs/HARDWARE.md` bzw. `docs/REPARATUR.md`; Detailprotokolle bei Bedarf als `docs/protokoll/LAUF_<Datum>.md`.
  Wird eine ganze Gruppe elektrisch geklärt (Signalpfad bis zum MCU, Treiberstufe), den Schaltplan in `docs/schaltplan/` ergänzen (KiCad-Quelle ändern, Netz-/Bauteil-CSV anpassen) und PDF/SVG mit KiCad 9 neu exportieren (`kicad-cli sch export pdf ...`). Fehlt KiCad, den Neuexport als offen in `docs/schaltplan/README.md` vermerken.
- Belegstufen beibehalten: M gemessen, F Foto, I abgeleitet, H Hypothese. Keine Verbindung aus Vermutung als Kupfer eintragen.
- MCU-Pins: Arbeitsnummern 1–32 ab Gehäusemarke gegen den Uhrzeigersinn (`docs/mcu_pins/`), nicht als Datenblatt-Pins ausgeben.

## Protokoll
- Das Repo ist für Dritte aufgeräumt (Stand 27.11.2026): Reparatur in `docs/REPARATUR.md`, Hardware in `docs/HARDWARE.md`, Fehlercodes in `docs/FEHLERCODES.md`. Messpläne, Neubewertungen und Rohprotokolle bleiben im Archiv-Branch.
- Fotos nach `photos/<Datum>/`, Markierungsbilder nach `docs/img/`, markierte Makros in `docs/img/makros/`. Originalfotos nicht verändern.
- Beispiel-Logs in `docs/beispiel_logs/`.
- Nach jeder Änderung committen und pushen. Relative Links in .md-Dateien nach Änderungen prüfen.

## Arbeitsweise mit Agenten (Anweisung Nutzer, 16.11.2026)
- **Claude (Hauptagent) plant**, Agenten führen aus.
- Ausführende Agenten: **höchstens `sonnet` mit Aufwand `medium`**. Einfache Tätigkeiten (Dateien kopieren, Protokollzeilen eintragen, Bilder beschriften, Suchen) an kleinere Modelle (`haiku`) mit geringem Aufwand.
- **Niemals ein größeres Modell als sonnet/medium für Agenten** – auch nicht für Kritik-Runden – ohne ausdrückliche Freigabe des Nutzers.
- Am Ende prüft Claude das Ergebnis selbst (gegen Messprotokoll, Schaltplan, Fotos).
- Bei Unzufriedenheit: Kritik **einmal** an einen passenden Agenten zurückgeben.
- Passt es danach immer noch nicht: den Nutzer darauf hinweisen und fragen, ob Claude die Arbeit selbst erledigen soll.
- Kurze Rückfragen, Einordnung von Messwerten im Dialog und Sicherheitshinweise beantwortet Claude direkt.
