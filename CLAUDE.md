# Arbeitsregeln für dieses Repo (myrun_diagnostics)

Sprache: Deutsch. Branch: `main` (Branch `110926` ist gemergt).

## Schaltplan als Referenz (Anweisung Nutzer, 16.11.2026)
- **Vor jeder neuen Theorie oder Messentscheidung** den gemeinsamen Schaltplan prüfen:
  `docs/gesamtschaltplan_110926/` (README, `gesamtschaltplan.pdf/.svg`, KiCad `GIRT_Gesamtschaltplan.kicad_sch`, Netzlisten `netze.csv`, `verbindungsbelege.csv`).
  Theorie und Messpunkte müssen zu den dort bestätigten Netzen passen; Widersprüche ausdrücklich nennen.
- **Neu gemessene Gruppen ergänzen** – nicht jedes Einzelteil, sondern ganze Abschnitte, sobald eine Gruppe
  (z. B. ein Signalpfad bis zum MCU, eine Treiberstufe) elektrisch geklärt ist.
  - Eingabe: neue Zeilen in einer Befund-CSV (Format wie `befunde_2026-11-16.csv`: ID;Knoten_A;Knoten_B;Art;Status;Wert;Quelle;Originalfoto;Bemerkung), Status M/F/I.
  - Erzeugen: `python docs/gesamtschaltplan_110926/erzeugen.py` (braucht KiCad CLI 9, PyMuPDF, ReportLab), danach `pruefen_unabhaengig.py`.
  - Fehlen die Werkzeuge in der Umgebung: Befund-CSV und README trotzdem ergänzen und den Neuaufbau als offen vermerken.
- Belegstufen beibehalten: M gemessen, F Foto, I abgeleitet, H Hypothese. Keine Verbindung aus Vermutung als Kupfer eintragen.
- MCU-Pins: Arbeitsnummern 1–32 ab Gehäusemarke gegen den Uhrzeigersinn (`docs/mcu_skizze_2026-11-16/`), nicht als Datenblatt-Pins ausgeben.

## Protokoll
- Messungen chronologisch in `docs/LAUF_2026-11-14.md` (bzw. Folgedatei), Bewertung in `docs/NEUBEWERTUNG_*.md`, Messplan in `docs/MESSPLAN_*.md`.
- Fotos nach `photos/<Datum>/`, Markierungsbilder nach `docs/img/`. Originalfotos nicht verändern.
- Nach jeder Änderung committen und pushen.

## Arbeitsweise mit Agenten (Anweisung Nutzer, 16.11.2026)
- **Claude (Hauptagent) plant**, Agenten führen aus.
- Ausführende Agenten: **höchstens `sonnet` mit Aufwand `medium`**. Einfache Tätigkeiten (Dateien kopieren, Protokollzeilen eintragen, Bilder beschriften, Suchen) an kleinere Modelle (`haiku`) mit geringem Aufwand.
- **Niemals ein größeres Modell als sonnet/medium für Agenten** – auch nicht für Kritik-Runden – ohne ausdrückliche Freigabe des Nutzers.
- Am Ende prüft Claude das Ergebnis selbst (gegen Messprotokoll, Schaltplan, Fotos).
- Bei Unzufriedenheit: Kritik **einmal** an einen passenden Agenten zurückgeben.
- Passt es danach immer noch nicht: den Nutzer darauf hinweisen und fragen, ob Claude die Arbeit selbst erledigen soll.
- Kurze Rückfragen, Einordnung von Messwerten im Dialog und Sicherheitshinweise beantwortet Claude direkt.
