# Schaltplan der Steuerung GIRT S6T30 (Platine ECS2458-6)

Rekonstruiert aus Messungen und Fotos, **kein Herstellerplan**. Er zeigt die gemessenen Teilnetze der Platine, nicht jedes Bauteil.

| Datei | Inhalt |
|---|---|
| [gesamtschaltplan.pdf](gesamtschaltplan.pdf) | Hauptblatt **Original-Rekonstruktion**, direkter KiCad-Export (eine Seite, Stand 27.11.2026); die frühere 43-seitige Fassung mit Detailansichten und Messregister liegt im Archiv-Branch |
| [uebersicht_A1.pdf](uebersicht_A1.pdf) | Gesamtblatt in einem Stück (Sonderformat, trotz Dateiname nicht A1) |
| [gesamtschaltplan.svg](gesamtschaltplan.svg) | dasselbe zum Zoomen im Browser |
| [GIRT_Gesamtschaltplan.kicad_sch](GIRT_Gesamtschaltplan.kicad_sch) | bearbeitbare KiCad-Quelle (KiCad 9) |
| [b10_umbau_2026-11-21.pdf](b10_umbau_2026-11-21.pdf), [.svg](b10_umbau_2026-11-21.svg), [KiCad](B10_Umbau_2026-11-21.kicad_sch) | **Ist-Blatt B10-Umbau**: die tatsächlich eingebaute Netzerfassung (je Seite Faston – 470 kΩ – 470 kΩ – US1M – J) |
| [netze.csv](netze.csv), [bauteile.csv](bauteile.csv), [bauteile_umbau_2026-11-21.csv](bauteile_umbau_2026-11-21.csv) | Netzliste und Bauteillisten (Original bzw. Umbau) |
| `*.xml` | KiCad-Netzlisten-Export beider Blätter |

Das Original-Blatt und das Ist-Blatt sind zwei getrennte Bestückungsstände derselben Stelle, keine parallelen Schaltungen. Bauteil-IDs und das Raster A–L / 1–6 entsprechen dem [Fotoatlas](../fotoatlas/README.md) und der [Platinenübersicht](../GIRT_Platinen_Uebersicht.pdf).

## Belegstufen

- **M** gemessen, **F** aus Foto abgelesen, **I** abgeleitet, **H** Hypothese. Eine Verbindung aus bloßer Vermutung wird nicht als Kupfer eingezeichnet.
- MCU-Nummern sind **Arbeitsnummern 1–32** (siehe [mcu_pins](../mcu_pins/README.md)), keine Datenblatt-Pins.
- TL082-Pinbelegung: 1 OUT A, 2 IN A−, 3 IN A+, 4 V− (−12VA), 5 IN B+, 6 IN B−, 7 OUT B, 8 V+ (+12VA).
- 0VA (Netzseite/Logik) und 0V_KONSOLE sind getrennte Netze.

## C602

C602 (J gegen 0VA, 470 pF 0603) ist im Plan als **ersetzt** vermerkt (neu 460 pF gemessen [M]; der alte hatte einen Nebenschluss). PDF und SVG beider Blätter wurden am **27.11.2026 mit KiCad CLI 9.0.2** aus den vorhandenen KiCad-Dateien neu exportiert. `uebersicht_A1.pdf` entspricht dem neuen einseitigen Gesamtblatt. Die KiCad-Quellen wurden beim Export nicht verändert.

Die Exporte lassen sich im Verzeichnis `docs/schaltplan/` so wiederholen (die SVG-Ausgaben auf die bestehenden, unten angegebenen Dateinamen umbenennen):

```bash
kicad-cli sch export pdf GIRT_Gesamtschaltplan.kicad_sch -o gesamtschaltplan.pdf
kicad-cli sch export svg GIRT_Gesamtschaltplan.kicad_sch -o .
kicad-cli sch export pdf B10_Umbau_2026-11-21.kicad_sch -o b10_umbau_2026-11-21.pdf
kicad-cli sch export svg B10_Umbau_2026-11-21.kicad_sch -o .
```

Die erzeugten SVGs `GIRT_Gesamtschaltplan.svg` und `B10_Umbau_2026-11-21.svg` werden als `gesamtschaltplan.svg` und `b10_umbau_2026-11-21.svg` abgelegt; anschließend `gesamtschaltplan.pdf` auch nach `uebersicht_A1.pdf` kopieren.

## Offene Lücken

- MCU-Typ, Masseanschluss und die meisten MCU-Pins sind unbekannt; ebenso die Typen von 1P, T2, T3, T4 und FAN3100C (nur Kandidaten).
- Zuordnung der P600-/NTC-Sensorpins (Ka/Kb), Anode von OC04, Quelle von D5/T2, Freilaufdiode an F27, Rückmeldesignal des Relais.
- TL082 Pin 6/7 sind im Symbol vorhanden, ihre mögliche Verbindung ist Hypothese [H].
- Das Relais-/Treiber-Umfeld ist nur so weit gezeichnet, wie es gemessen wurde.

## Generator und Belegregister

Der Python-Generator (`erzeugen.py`), die Prüfskripte, die Befund-CSVs mit allen Einzelmessungen und das Verbindungsregister liegen im Archiv-Branch `archiv-vor-aufraeumen-2026-11-27` unter `docs/gesamtschaltplan_110926/`.
