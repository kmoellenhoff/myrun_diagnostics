# GIRT-S6T30-Diagnose – Zusammenfassung für Dritte

**ENTWURF, Branch `aufraeumen`, Quellenstand 21.11.2026 (`83da2fb`). Kein abgeschlossener Reparaturbericht.**

**Ursache wahrscheinlich C602, Stand: Gegenversuch offen.**

## Gerät und Zweck

Untersucht wird ein Technogym MyRun mit Gefran-Steuergerät **GIRT S6T30**. Der Bandmotor ist ein Bürsten-Gleichstrommotor; die GIRT schaltet seine Leistung aus dem gleichgerichteten Netz. Eine Konsole übermittelt Anforderungen und liefert BLE-Diagnosewerte. Dieses Repository dokumentiert die Fehlersuche an einem einzelnen Gerät, keine herstellerseitige Reparaturanweisung.

Einstieg in die Belege: [Hardware](HARDWARE.md), [aktuelles Tagesprotokoll und Gegenversuchsplan](LAUF_2026-11-21.md), [gemeinsamer Schaltplan](gesamtschaltplan_110926/README.md), [Prüfung und Beleggrenzen](PRUEFUNG_SCHALTPLAN_2026-11-21.md), [Fotoatlas](atlas_110926/README.md).

## Belegstufen und Grenzen

- **M:** berichtete elektrische Messung; Bedingungen und Messkontakt beachten.
- **F:** Zuordnung anhand eines Originalfotos; kein Ersatz für eine Durchgangsmessung.
- **I:** aus vorhandenen Befunden abgeleitet.
- **H:** unbestätigte Hypothese, insbesondere Fehlerursache und Übertragung fremder Fehlercode-Tabellen.

Anzeigen und Logereignisse werden als solche beschrieben, nicht automatisch als elektrische Messung bezeichnet. Historische Protokolle verwenden zusätzlich eigene Beobachtungs-/Handbuchkürzel; deren Aussagen werden hier nicht zu stärkeren Belegen hochgestuft. Statisch unauffällig bedeutet nicht unter allen Betriebsbedingungen fehlerfrei.

## Symptome

- Fehlstarts: Die Konsole meldet Laufanforderung und einen PWM-Diagnosewert, während Band und Encoder stehen bleiben; später **HF904**. Das ist kein Nachweis tatsächlicher Gate-PWM am Leistungstransistor.
- Zeitweise läuft das Band kurz und stoppt wieder; **HF902**, Anzeigen **err 4 / err 9** sowie STS2-Blinkgruppen sind protokolliert. Auch im Standby gab es einen Fehler ohne Motoranforderung.
- **Achtmal STS2-Blinken / Code 08** trat bei Fehlstarts und bei manueller Bandbewegung im Standby auf. Das zeigt einen Zusammenhang mit dem Antriebs-/Drehzahlzustand, beweist aber keinen defekten Sensor (I). Die Herstellerbedeutung für genau diese GIRT-Version ist nicht vollständig geklärt (H).
- Kurze und längere erfolgreiche Läufe wechseln sich mit Fehlern ab. Am 21.11. war der J-Einbruch durch Erwärmen des Bereichs um C602 reproduzierbar.

Quellen: [10.11.](LAUF_2026-11-10.md), [11.11.](LAUF_2026-11-11.md), [14.11.](LAUF_2026-11-14.md), [19.11.](LAUF_2026-11-19.md), [21.11.](LAUF_2026-11-21.md). Die getrennten Code-Ebenen werden im Entwurf [FEHLERCODES.md](FEHLERCODES.md) erklärt.

## Vorgehen und geprüfte Baugruppen

Die Suche kombinierte Sichtprüfung, stromlose Messungen, begrenzte Betriebswerte, BLE-Logs und schrittweise Rekonstruktion bestätigter Netzgruppen. Einzelschritte bleiben in den verlinkten Primärprotokollen.

| Bereich | Ergebnis und verbleibende Grenze | Beleg / Quelle |
|---|---|---|
| Motor und Q2/D3 | Wicklung über mehrere Rotorstellungen unauffällig; MOSFET-/Diodenpfade statisch plausibel. Erfolgreiche Läufe zeigen prinzipielle Arbeitsfähigkeit, keine vollständige Lastprüfung. | M; [Hardware](HARDWARE.md), [11.11.](LAUF_2026-11-11.md) |
| Motoranschlüsse | L+ gegen Zwischenkreis-Plus und L− gegen Q2-Drain jeweils 0 Ω gemeldet. Die vollständige Netzeinspeisung ist damit nicht rekonstruiert. | M; [Schaltplan](gesamtschaltplan_110926/README.md) |
| Hilfsversorgung / Elkos | Treiber-VDD beim Fehlstart 13,5 V gemeldet; +5VA später über mindestens zwei Minuten stabil. Kapazitäts-/ESR-Befunde lieferten keinen belastbaren Austauschbefund; Parallelbeschaltungen begrenzen Einzelbewertungen. | M/I; [11.11.](LAUF_2026-11-11.md), [12.11., historisch](NEUBEWERTUNG_2026-11-12.md), [17.11.](LAUF_2026-11-17.md) |
| F27 und Ansteuerung | Spule ca. 1,4 kΩ; wiederholter externer Schaltversuch mit Kontakt ca. 0,03 Ω. Im untersuchten Fehlstart kein Anzug gemeldet. Schaltreaktion und vollständiger Leistungsweg sind getrennte Fragen. | M/I; [Schaltplan und Quellen](gesamtschaltplan_110926/README.md) |
| B18/B19 und PFC | Messpfad zu L4981 Pin 14/VFEED rekonstruiert. Er ist nicht der belegte MCU-Netzeingang; frühere gegenteilige Hypothesen sind überholt. PFC-Freigabe über T3 teilweise verfolgt. | M/F/I; [B18-Netzliste](netlist/b18_spannungssense_kandidat.md), [Neubewertung 14.11.](NEUBEWERTUNG_2026-11-14.md) |
| NTC / Not-Stopp / Enable | NTC reagiert auf Erwärmen; Thermoschalter kalt niederohmig. Rostiger Schlüsselkontakt und Enable-Auswertung wurden untersucht. Ein Enable-Abfall kann auch Folge einer Störung sein. | M/I; [11.11.](LAUF_2026-11-11.md), [Schaltplan](gesamtschaltplan_110926/README.md) |
| Tacho / Optokoppler | Sensor und P4-TACHO schalten bei Bewegung; Handtest liefert Encoderwerte. Nicht jeder Pfad zur GIRT-MCU ist dynamisch belegt. OC04/05 statisch untersucht; Signalübertragung unter Betriebsbedingungen nicht vollständig charakterisiert. | M/I; [14.11.](LAUF_2026-11-14.md), [17.11.](LAUF_2026-11-17.md) |
| B10 / J / TL082 / X | J ist ein Messsignal, keine Boardversorgung. Weg über TL082-Puffer und Teiler zu X rekonstruiert. J fiel zeitweise stark ab; Kondensator C602 liegt parallel zum 22,1-kΩ-Fußwiderstand. | M/F/I; [Schaltplan](gesamtschaltplan_110926/README.md), [21.11.](LAUF_2026-11-21.md) |

## Ersetzte Teile, Nacharbeiten und Korrekturen

| Maßnahme | Berichtetes Ergebnis, keine pauschale Fehlerbehebung | Quelle |
|---|---|---|
| Fehlende FUSE MOT durch T4A/250 V, 5×20 ersetzt | Höhenverstellung danach im früheren Test wieder funktionsfähig. Das bestätigt nicht ihre tatsächliche Bewegung im BLE-Profil vom 21.11. | [Hardware, Reparaturen](HARDWARE.md#8-repairs-and-work-done-on-this-unit) |
| Platinen-/Steckerreinigung, F2-/Shunt-/Relais-Lötstellen nachgearbeitet | Fehler nicht dauerhaft beseitigt; keine einzelne Nacharbeit als Ursache bewiesen. | [Hardware](HARDWARE.md), [11.11.](LAUF_2026-11-11.md) |
| Treiber-VDD-Lötstelle nachgelötet | Zuvor schwankender Durchgang, danach konstant 0 Ω gemeldet; kurzzeitiger erfolgreicher Lauf, anschließend weitere Fehler. | M; [11.11.](LAUF_2026-11-11.md) |
| Not-Stopp-Kontakt entrostet, Sensor gereinigt und befestigt | Verbesserte/stabile Einzelbefunde, spätere Fehlstarts blieben bestehen. Kein Sensortausch dokumentiert. | [11.11.](LAUF_2026-11-11.md), [14.11.](LAUF_2026-11-14.md) |
| Beide B10-Dioden durch US1M ersetzt | Untere ausgebaute Diode war auffällig; J brach mit Ersatz weiterhin ein. Ob der Diodenbefund ursprünglicher oder später hinzugekommener Fehler war, bleibt offen. | M/H; [17.11.](LAUF_2026-11-17.md), [19.11.](LAUF_2026-11-19.md), [21.11.](LAUF_2026-11-21.md) |
| Neue B10-Widerstände 470 kΩ statt 475 kΩ, neue Dioden und Zusatzlitzen | Reihenfolge laut Nutzerkorrektur: Faston → R → R → US1M → J, Kathode an J. Alte Pads weiter benutzt; nicht alle Pad-/Kupferfehler ausgeschlossen. Anfangs falsche Polung berichtet und korrigiert; erste Variante nicht lückenlos rekonstruierbar. | M/F/I; [Ist-Schaltplan](gesamtschaltplan_110926/b10_umbau_2026-11-21.pdf), [21.11.](LAUF_2026-11-21.md) |
| C602 ausgebaut, kalt 0,43 nF gemessen | Wärmebedingter J-Einbruch danach nicht reproduziert; Profil-Lauf rund 4½ Minuten ohne neuen Fehler. Zwei weitere kurze Läufe bei 9/12 km/h sind nur Nutzerbericht ohne vollständigen J-Verlauf und keine Empfehlung für weitere Tests. | M/I/H; [21.11.](LAUF_2026-11-21.md), [Profil-Rohlog](logs_2026-11-21/myrun_fast_monitor_20261121_133144.txt) |

TL082-Pinzählung und frühere B10-Reihenfolge wurden in der Dokumentation korrigiert; das waren keine belegten Bauteilvertauschungen. Die MCU-Nummern sind ausschließlich **Arbeitsnummern 1–32** aus der [MCU-Skizze](mcu_skizze_2026-11-16/README.md), keine bestätigten Datenblatt-Pins.

## Ursachenstand und offene Punkte

**Ursache wahrscheinlich C602, Stand: Gegenversuch offen.**

Die Kombination aus Wärmeeinbruch mit C602, ausbleibendem Einbruch nach Entfernen und anschließendem erfolgreichen Lauf stützt den Verdacht (I). Ein interner Isolationsfehler des Kondensators oder ein leitender Pfad im bearbeiteten Lötumfeld bleiben Ursachenhypothesen (H). Die kalte Kapazitätsmessung belegt keine intakte Isolation. Dass C602 schon der ursprüngliche Fehler vor allen Nacharbeiten war, ist nicht bewiesen; mehrere Fehler sind möglich (H).

Der Abschnitt **„16:11 – Arbeitshypothese und Gegenversuch“** im [Tagesprotokoll](LAUF_2026-11-21.md) beschreibt einen geplanten Versuch, noch kein Ergebnis. Neue Kondensatoren sind bestellt; ein eingebauter Ersatz und ein erfolgreicher Gegenversuch sind nicht dokumentiert. Das Endergebnis bleibt deshalb offen.

Noch erforderlich: Ersatz und vergleichbare Standby-/Betriebsbeobachtung mit J-Verlauf protokollieren; Pin-/Anschlussfragen und unvollständige Tacho-/Freigabepfade getrennt behandeln; die GIRT-spezifische Fehlercodetabelle verifizieren. Der alte Kondensator muss nicht zur Fehlerprovokation wieder in einen Motorlauf eingebaut werden.

Bei Live-Arbeiten liegt 0VA auf Netzpotenzial; Zwischenkreis und Relaispfade sind keine Schutzkleinspannung. Diese Übersicht ergänzt keine neue Messanweisung. Software-STOP kann scheitern. Skriptbeispiele bleiben im Entwurf [SKRIPTE.md](SKRIPTE.md) auf 0,8–2,9 km/h und 0–5 % begrenzt.
