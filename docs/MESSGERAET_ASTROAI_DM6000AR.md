# AstroAI DM6000AR – Herstellerangaben für die GIRT-Diagnose

Am 17.11.2026 recherchiert. Modellname mit Nutzerfoto abgeglichen: **DM6000AR**, nicht M6K0R oder anderes 6000-Counts-Modell.

## Primärquellen

- [Offizielle Produktseite DM6000AR](https://www.astroai.com/digital-multimeter-6000-counts-dm6000ar/ap/100019).
- [Offizielle deutsche Anleitung, ASIMT5000A-DE-v1.pdf](https://help.astroai.com/sku/user-manual/ASIMT5000A-DE-v1.pdf?version=1720715232). PDF-Titel „AstroAI Digital Multimeter 6000 Counts, DM6000AR -DE“, 38 Seiten, Erstellungsdatum 05.07.2024. Vom Herstellerprodukt verlinkt; Tabellen auf PDF-Seiten 31–33 und 36 visuell geprüft. Die PDF-Bildseiten wurden zur Suche temporär per OCR gelesen. Original-PDF hier nicht dupliziert.
- [Offizielle englische Anleitung](https://help.astroai.com/sku/user-manual/ASIMT5000A-EN-v1.pdf?version=1784279190), ebenfalls von der Produktseite. Die nachstehenden Werte stammen aus der deutschen Fassung.

## Relevante Daten

| Funktion | Angabe | PDF-Seite |
|---|---|---|
| Anzeige | 6000 Counts / maximal 5999 | 31 und Geräteaufdruck |
| Aktualisierungsrate | 2-mal pro Sekunde | 31 |
| Eingangswiderstand V DC / V AC | 10 MΩ | 32 |
| DC 600 mV | Auflösung 0,1 mV, ±(0,8 % + 5 Digits) | 32 |
| DC 6 V | Auflösung 1 mV, ±(0,8 % + 3 Digits) | 32 |
| DC 60 V | Auflösung 10 mV, ±(0,8 % + 3 Digits) | 32 |
| AC 600 mV | Auflösung 0,1 mV, ±(1,2 % + 8 Digits) | 32 |
| AC 6 V | Auflösung 1 mV, ±(1,2 % + 6 Digits) | 32 |
| AC 60 V | Auflösung 10 mV, ±(1,2 % + 6 Digits) | 32 |
| AC 600 V | Auflösung 100 mV, ±(1,2 % + 6 Digits) | 32 |
| AC-Spannungsmessung, Frequenzbereich | **40–400 Hz** | 33 |
| Separate Frequenzfunktion | **10 Hz–10 MHz**, ±(1,0 % + 5 Digits) | 36 |
| Frequenzfunktion Überlastschutz | **250 V DC/AC RMS**; keine pauschale Übernahme der höheren Spannungsbereiche | 36 |
| Sicherheitskennzeichnung | EN 61010-1, CAT III 600 V / CAT II 1000 V | 31 |

Digits bedeutet Schritte der letzten angezeigten Stelle; die Genauigkeitsangaben gelten unter den Herstellerbedingungen (23 °C ±5 °C, unter 80 % rF, angegebener Einjahreszeitraum). Der Hersteller bezeichnet das Gerät als True RMS. Die Gleichspannungsanteil-Unterdrückung und Genauigkeit für jede mögliche nichtsinusförmige Kurvenform sind durch „True RMS“ allein nicht vollständig spezifiziert.

## Konsequenzen und Grenzen

- DC an J/X ist der erste Vergleich. 10 MΩ belastet die bekannte kΩ-Schaltung gering; schlechter Kontakt oder ein falscher Messpunkt werden dadurch nicht ausgeschlossen.
- 100 Hz liegt im AC-Messbereich. Gleichgerichtete Wellen und besonders schmale PWM-Pulse enthalten zusätzliche Oberwellen; oberhalb 400 Hz ist die angegebene AC-Spannungsgenauigkeit nicht zugesichert. Eine niedrige AC-Anzeige am OC05-Emitter ist deshalb kein alleiniger Nachweis schwacher Pulse.
- Die Frequenz-Tabelle nennt keine Eingangsempfindlichkeit/Triggerschwelle. Bei kleinem Wechselanteil sind 0 Hz oder schwankende Angaben nicht automatisch Fehler des Messobjekts. Die 10-MHz-Zählergrenze ist keine 10-MHz-Bandbreite der AC-Spannungsmessung.
- 2 Aktualisierungen/s beschreibt nicht garantiert die MIN/MAX-Ereigniserfassung. Eine verifizierte MIN/MAX-Erfassungszeit liegt hier nicht vor; kurze Versorgungseinbrüche können übersehen werden.
- Die 250-V-Überlastschutzangabe der Hz-Funktion ist kein empfohlener Betriebswert und keine allgemeine Freigabe für Netzmessungen mit dieser Funktion. Für die erste L–N-Prüfung V AC verwenden, zulässigen gesamten Aufbau beachten. Die hohen V-DC-/V-AC-Bereiche gelten nicht automatisch für Hz/Ω/C.
- Beim GIRT ist **0VA = Zwischenkreis-Elko-Minus** auf Netzpotential, nicht Schutzleiter, N oder P2.7. Richtige Differenzspannung und geeignete Spannungs-/Kategorieauslegung der Messmittel samt Leitungen und Kontaktierung sind beide erforderlich. Daraus folgt keine Eignungsbestätigung für das separate BSIDE-OT3-Oszilloskop.

[Tagesprotokoll](LAUF_2026-11-17.md) · [Aktueller Messplan](MESSPLAN_2026-11-14_abend.md).
