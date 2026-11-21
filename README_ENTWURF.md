# Technogym MyRun – GIRT-S6T30-Diagnose

**README-ENTWURF auf Branch `aufraeumen`, Stand 21.11.2026 (`83da2fb`). Die bestehende [README.md](README.md) wird nicht überschrieben. Kein Merge ohne Freigabe.**

Dieses Repository dokumentiert die Reparatursuche an einem Technogym MyRun mit Gefran-Steuergerät **GIRT S6T30**. Es enthält elektrische Messprotokolle, zugeordnete Originalfotos, einen rekonstruierten Teilschaltplan und Python-Werkzeuge zur Bluetooth-Diagnose.

**Ursache wahrscheinlich C602, Stand: Gegenversuch offen.** Der kleine Kondensator zwischen Netz-Messknoten J und 0VA ist nach Wärmeversuchen und erfolgreichen Läufen ohne ihn der Hauptverdächtige. Ein Ersatzkondensator und dessen Vergleichstest sind noch nicht als abgeschlossenes Ergebnis protokolliert. Ein Fehler im bearbeiteten Anschlussumfeld oder mehrere Fehler bleiben möglich (H).

## Hier beginnen

| Interesse | Einstieg |
|---|---|
| Was war kaputt, was wurde geprüft? | [Zusammenfassung und offener Ursachenstand](docs/ZUSAMMENFASSUNG.md) |
| Welche Meldungen sind tatsächlich beobachtet? | [Fehlercodes: Beobachtung und Vergleichshypothesen](docs/FEHLERCODES.md) |
| Neueste Messungen und Gegenversuch | [Tagesprotokoll 21.11. – „Arbeitshypothese und Gegenversuch“](docs/LAUF_2026-11-21.md) |
| Schaltung ansehen oder bearbeiten | [Gesamtschaltplan, PDF/SVG/KiCad und Belege](docs/gesamtschaltplan_110926/README.md) |
| Tatsächlicher B10-Umbau | [Separates Ist-Blatt](docs/gesamtschaltplan_110926/b10_umbau_2026-11-21.pdf) |
| Bauteile auf der Platine finden | [Fotoatlas mit bestehendem Raster](docs/atlas_110926/README.md) |
| Programme bedienen | [Alle Skriptoptionen, Modi, Ausgaben und Beispiele](docs/SKRIPTE.md) |
| Spätere Ordnung des Repositories | [Nur vorgeschlagene Struktur und Archivkandidaten](docs/AUFRAEUMVORSCHLAG.md) |

## Fehlerbild und Beleggrenzen

Das Band startet zeitweise nicht oder bricht nach kurzem Lauf ab. Protokolliert sind HF904/HF902, err-Anzeigen und STS2-Blinkgruppen, darunter achtmal Blinken. Eine angeforderte Geschwindigkeit oder ein PWM-Diagnosewert der Konsole beweist keine tatsächliche Motoransteuerung. Die vollständige GIRT-spezifische Fehlercodetabelle ist nicht bestätigt.

**M** = gemessen, **F** = Originalfoto, **I** = abgeleitet, **H** = Hypothese. Fremde Handbuchtabellen sind keine bestätigten GIRT-Definitionen. Anzeigen und Logereignisse werden mit Quelle wiedergegeben; ältere Protokollkürzel werden nicht stillschweigend zu neuen Messbelegen erklärt.

Der Schaltplan enthält bestätigte Teilnetze und ausdrücklich offene Verbindungen, keinen vollständigen Herstellerplan. Die Original- und Umbauansicht sind getrennte Bestückungsstände, keine zusätzlichen parallelen Schaltungen. C602 ist derzeit ausgebaut markiert. MCU-Nummern sind [Arbeitsnummern 1–32](docs/mcu_skizze_2026-11-16/README.md), keine bestätigten Datenblatt-Pins. TL082-Pins folgen der echten Belegung und den Korrekturen vom 21.11.

## Bluetooth-Diagnose: zuerst beobachten

Benötigt werden Python 3, `bleak` und eine funktionierende Linux-/BlueZ-Umgebung. Andere verbundene Trainings-/Bluetooth-Apps vorher trennen. Installation der Python-Abhängigkeit:

```bash
python3 -m pip install bleak
```

**`BLE_ADRESSE` ist ein Platzhalter und vor Benutzung zu ersetzen.** Der folgende Modus sendet keine Motorbefehle und führt kein FTMS-Setup aus; er schreibt lediglich lesende Diagnoseabfragen auf den Textkanal:

```bash
python3 myrun_fast_monitor.py --address BLE_ADRESSE --listen-poll 1 --slow-every 5 --duration 120 --output neuer_beobachtungslauf
```

Für ausschließlich eingehende Notifications, ohne Diagnosebefehle:

```bash
python3 myrun_fast_monitor.py --address BLE_ADRESSE --listen-only --duration 120
```

Ausgaben des Fast-Monitors: TXT und CSV mit `t_rel_s,wallclock,utc,signal,value`. Für die Ist-Geschwindigkeit `@RENC#`/`enc_hz` bzw. `MeasSpeed` auswerten; das FTMS-Geschwindigkeitsfeld ist auf der untersuchten Firmware ein Sollwert. Jede Abfrage hat einen eigenen Zeitstempel, BLE-Werte sind keine simultane Oszilloskopaufnahme.

### Aktive Programme bewusst auswählen

- Fast-Monitor ohne Listen-Optionen: START nach Bereitschaft und Enter; `--auto-start` startet nach Countdown **ohne Enter**.
- `--no-start` sendet keinen START, führt aber **Initialisierung und Setup** aus; es ist kein rein passiver Modus.
- `myrun_incline_test.py` sendet nach eigenem Countdown **automatisch START** und Neigungsbefehle. Es ist kein bloßer Test einer stillstehenden Höhenverstellung.
- Dump und Probe senden keine eigenen Motor-STARTs, initialisieren aber die Sitzung und führen Setup aus. RENC-Watch arbeitet ohne dieses Setup.

Alle Optionen, genauere Unterschiede und vorbereitete aktive Beispiele stehen in [SKRIPTE.md](docs/SKRIPTE.md). Dort bleiben explizite Testprofile bei **0,8–2,9 km/h** und **0–5 %**, mit teils engeren Grenzen einzelner Skripte. Historisch berichtete höhere Geschwindigkeiten erweitern diese Beispiele nicht. START kann ohne ausdrücklich gesetzte Geschwindigkeit bereits Bewegung auslösen.

## Grenzen der Anwendung und Veröffentlichung

Aktive Tests nur am vollständig montierten und mechanisch sicheren Gerät, niemand auf dem Band, physischer Sicherheitsstopp erreichbar. **Software-STOP kann scheitern.** Handbewegung des Bandes im Standby kann selbst einen Fehlerzustand auslösen. Diese Programme ersetzen keine elektrische Sicherheitsprüfung.

Die GIRT enthält netzbezogene Schaltungsteile und einen geladenen Zwischenkreis. 0VA ist nicht automatisch Schutzkleinspannung, Neutralleiter oder Schutzleiter. Die Dokumentation ist keine Freigabe für Live-Messungen oder das Überbrücken von Schutzfunktionen.

Bestehende Programme/Reports können Gerätekennungen und lokale Ausgabepfade enthalten. Vor öffentlicher Weitergabe nur geeignete Veröffentlichungskopien prüfen; unveränderte Rohbelege erhalten. Neue Fotokopien vor Veröffentlichung von Metadaten bereinigen, vorhandene Originalfotos nicht verändern. Die Entwurfsarbeit fügt keine Fotos hinzu und verändert keine bestehenden Dateien.

## Herkunft und Lizenz

Unabhängige Reparaturdokumentation, nicht von Technogym, Gefran oder WEG unterstützt oder freigegeben. Bestehende Lizenz- und Urheberhinweise bleiben maßgeblich: [EUPL-1.2](LICENSE). Teile des BLE-Initialisierungsverständnisses stammen laut ursprünglichem Repository aus der Untersuchung von [qdomyos-zwift](https://github.com/cagnulein/qdomyos-zwift); eigene Python-Implementierung. Herstellerhandbücher und deren Übertragungsgrenzen sind in der [Quellenübersicht](docs/FEHLERCODES.md#4-vorhandene-quellen-und-noch-zu-prüfen) beschrieben.

## Review-Notizen zum bisherigen Root-README

Dieser Abschnitt erläutert den Entwurf und wäre vor einer späteren Übernahme als Haupteinstieg redaktionell zu behandeln. Die bisherige Datei bleibt hier unangetastet.

| Befund im bisherigen README | Vorschlag in diesem Entwurf |
|---|---|
| Langer englischer Skripteinstieg vor dem heutigen Ursachenstand | Deutscher Einstieg mit offenem Reparaturstatus und Navigation |
| Bedienung in „Contents“ und „Usage“ teilweise doppelt | Ein kurzer Einstieg, vollständige Referenz in `docs/SKRIPTE.md` |
| Enter-Zeitpunkt einmal vor der Verbindung, später nach Bereitschaft beschrieben | Dem tatsächlichen Code folgen: Fast-Monitor fragt nach Verbindung/Bereitschaft; Auto-Start ist gesondert |
| Listen-Poll an einer Stelle noch als ohne Init ungetestet bezeichnet | Vom Code und den vorhandenen Sitzungen ausgehen; Hardware-Funktion weiterhin nicht universell behaupten |
| Pauschale Aussagen zu rein lesender Nutzung / fehlenden Geschwindigkeitsbefehlen | Setup-Wirkung und inzwischen vorhandene Profile ausdrücklich unterscheiden |
| STS2-/HF-Deutungen und historische Hypothesen verstreut | Eigene Code-Tabelle mit durchgängig H-gekennzeichnetem Fremdvergleich |
| Gerätebezogene Kennungen und lokale Ausgabedaten im Altbestand | Nicht in den neuen Einstieg übernehmen; gesonderter Veröffentlichungsprüfpunkt, keine stille Rohdatenänderung |

**Keine Funktionsänderung, kein abschließender Reparaturerfolg, kein automatischer Merge. Ursache wahrscheinlich C602, Stand: Gegenversuch offen.**
