# Messplan – aktualisiert nach den Sensortests am 17.11.2026

Maßgeblich: [Prüfung des aktuellen Stands](PRUEFUNG_2026-11-16_spaet.md), [Schaltplan](gesamtschaltplan_110926/README.md) und [chronologisches Protokoll](LAUF_2026-11-14.md). Neue Ergebnisse stehen im [Protokoll vom 17.11.](LAUF_2026-11-17.md); die Tabellen unten beschreiben weiterhin geplante Messungen. MCU-Pins sind Arbeitsnummern, keine bestätigte Herstellerbelegung.

**Ziel für den 17.11.:** Signalfehler zeitlich vor der Abschaltung erkennen und Steuerbefehl von Schaltreaktion unterscheiden. Die Prüfung vom 17.11. hat die Tacho-Funktion des ADM485/OC06 bisher nicht bestätigt. Vorrang hat jetzt die stromlose Verfolgung des tatsächlichen Pfads ab P4; PWM-Übertragung auf der Netzseite bleibt bei ungeklärtem Messaufbau zurückgestellt.

## Vorrang nach den Nachtragsmessungen vom 17.11.

- **Sensor/P4 erledigt:** C–E schaltet bei manueller Bewegung etwa 0 ↔ 11,75 V, an P4 etwa 0 ↔ 12 V. High-Wackeltest stabil; P2.7 gegen P4-0V konstant 0 V berichtet. Späteres ×10-Versehen und Wiederholungen sind im Tagesprotokoll ausdrücklich dokumentiert.
- **K1/K2/K3 im Standby geprüft:** ADM485 Pin8 4,8 V; /RE Pin2 0 V, DE Pin3 0 V; Pin6/A **2,4 V**, Pin7/B **2,2 V**, OC06-K/RO **4,8 V**, alle drei Signalpegel auch bei manueller Bandbewegung konstant. Pin6 0,2 V ist überholt. Versorgung während START/kurze Einbrüche nicht separat erfasst. Kein Defektnachweis, keine bestätigte Tacho-Funktion des ADM485/OC06. Endliche Widerstände zu P4 allein belegen keinen vollständigen Signalpfad.
- **50 Hz erneut bei fraglichem Kontakt:** 2,70 Vpp/50 Hz auch bei DC-Kopplung; nach Neupositionieren beider Messkontakte verschwunden. Messkontakt-/Einkopplungseffekt deutlich gestützt, Masseklemme allein als Ursache nicht bewiesen.
- **K4 teilweise erledigt:** P2.6 Standby nahe 0 V. **OC05 Pin1/Anode** im Standby nahe 0 V, bei Start kurze Pulse um 1 V (VMAX 1,0 V, Vpp 1,1 V). LED-begrenzte Spannung plausibel; Frequenz/Tastgrad und Übertragung zum MCU offen. Ursprüngliche Nutzerbezeichnung OC06 für dieses Bild ausdrücklich zu OC05 korrigiert. Keine gesicherte neue Motor-/Fehlercodechronologie zu diesem Start.
- **Jetzt stromlos den realen Pfad ab P4 verfolgen:** Sensorstecker abziehen; platinen­seitigen TACHO-Kontakt gegen beide Kappen des zuvor verfolgten ersten „1000“ nahe P4 messen. Beim richtigen 100-Ω-Serienwiderstand ungefähr 0 Ω / 100 Ω erwartet, Parallelpfade beachten. Noch keine Ergebnisse. Danach nur bis zum nächsten elektrisch bestätigten Anschluss weitergehen. [Ergebnisse, Korrekturen und nächste Schritte](LAUF_2026-11-17.md).
- **N2 / OC05 Pin3 gegen 0VA zurückgestellt:** Elektrisch das richtige Messpaar, aber Netzpotential des gesamten Kreises gegenüber Erde. Keine Herstellerbestätigung für OT3 samt Tastkopf/Kabel zum potentialfreien Anschluss an 0VA vorhanden. Akkubetrieb ohne Erdung/USB und CAT-Aufdruck allein ersetzen diese nicht. Erst geeigneten Aufbau nachweisen; P2.7 nie mit 0VA verbinden. Diese Messung wurde nicht ausgeführt.
- Sensor/Kabel unter den getesteten Bedingungen entlastet, nicht für alle Drehzahlen/Lastfälle freigegeben. OC06-Ausgang→MCU bleibt offen. Manuelle Bewegungsversuche getrennt von späteren Start-/Fehleraufnahmen halten.

## Bereits erledigt

- J–0VA **22,14/22,02 kΩ**, passend zum 22,1-kΩ-Fußwiderstand. Die früheren 6,4–6,8 kΩ sind nicht reproduziert. Keine erneute Suche nach einem daraus allein vermuteten 10-kΩ-Leck.
- **X/MCU28:** J → 1 kΩ → TL082 Pin3, Pin1=Pin2; Ausgang → **R1 4,75 kΩ** → N; **R2 4,75 kΩ N–0VA**; N → 100 Ω → X, C nach 0VA. N–100-Ω-Pad laut Abendbeleg abgeleitet, nicht separat durchgemessen. Modellwert X ca. 3,7 V Spitze bei 230 V AC, kein harter Sollwert.
- **Y/MCU26:** LD3N O, L=0VA, R=+5VA; Y–P600 Kontakt1 etwa 1 kΩ. **P600 Kontakt2=+5VA mit 0 Ω bestätigt**, Fühler war gesteckt. Temperatureingang plausibel; diskreter Massewiderstand und Ka/Kb-Alias offen. X/Y nicht verbinden.
- **OC04:** Pin4=+5VA, Pin3→MCU12. **OC05:** Pin4=+5VA, Pin3→MCU17/18. Die 3,3/10 kΩ gegen 0VA sind In-Circuit-Werte.
- **F27:** MCU24 → 1 kΩ → T4-Basis L; Emitter R=0VA, Kollektor O=Spulenminus; Spulenplus +24 V. Quelle nicht erneut suchen.
- **T3:** MCU11 → 2,21 kΩ → Basis, Pull-up 10 kΩ nach +5VA; bisher 4,9 V Steuerleitung / 0,7 V Basis / 6 mV L4981 Pin15. **T2-Quelle weiterhin offen.**
- **Konsolenseite:** ADM485 Pin5=LM2903 Pin4=P2.7, RO/Pin1=OC06-Kathode. P4 TACHO→Pin7 1,103 kΩ, →Pin6 12,94 kΩ; Bauteilpfad/Funktion noch nicht vollständig bestätigt.
- **P2.6–P2.7=10,96 kΩ**, nicht 19,96 kΩ. Die Kreuzmessungen passen zu Masse-Rückwegen; kein neuer Hinweis auf eine niederohmige PWM–Tacho-Brücke.

## Messaufbau und Grenzen

Vorhanden laut Repository: BSIDE OT3, akkubetrieben, 10 MHz. **Akkubetrieb, abgezogenes USB-Kabel und ein CAT-Aufdruck allein belegen keine Eignung des Oszilloskopeingangs samt Tastkopf zum potentialfreien Messen an 0VA.** 0VA/Elko-Minus und die MCU-Seite liegen auf Netzpotential. Für die Netzseiten-Schritte ist ein nach Herstellervorgaben dafür geeigneter Messaufbau bzw. eine entsprechend bemessene Differenz-/Isolationsmessung erforderlich. Solange diese Eignung ungeklärt ist, diese Oszi-Schritte nicht mit einer normalen Masseklemme ausführen. Kein USB/PC/Ladegerät während einer potentialfreien Messung; P2.7 und 0VA nicht verbinden.

Konsolenseite und Netzseite getrennt behandeln. Messanschlüsse netzgetrennt, Zwischenkreis nachweislich entladen vorbereiten; benachbarte IC-Pins nicht überbrücken. Auch „Konsolenseite“ bedeutet keine pauschale Gefahrlosigkeit der geöffneten, versorgten Baugruppe. Kein manuelles Erzwingen von Freigaben.

Gleiche Startfolge, STS1/STS2-Video mit Ton, Zeitpunkte Netz-Ein/START/erster Fehler/STOP protokollieren. Band vor dem normalen Startversuch nicht von Hand bewegen: Das löste bereits einen eigenen Fehler aus. Ein gesonderter Bewegungs-/Sensorvergleich muss davon getrennt bleiben. Bei einem einkanaligen Oszi sind nacheinander erfasste Signale keine zeitgleiche Korrelation.

## Weiterführende Messungen und ursprüngliche Prüferwartungen

Die Prioritäten und erledigten Teilprüfungen oben haben Vorrang. K1–K3 nicht pauschal erneut durchführen; N-Schritte bleiben an einen nachgewiesen geeigneten Messaufbau gebunden.

| Schritt | Messung / Bezug | Modus und begründete Erwartung | Entscheidung |
|---|---|---|---|
| **S0 – stromlos** | OC06-Transistorseite: Pin4 gegen +5VA/0VA, Pin3 gezielt zur nächsten Verbindung bzw. MCU verfolgen | Ω / Leiterbahnabgleich; Orientierung aus Originalfoto. Nicht einfach dieselbe Beschaltung wie OC04/05 voraussetzen. | Ein späterer RO-Befund soll einem tatsächlichen MCU-Eingang zugeordnet werden können. Offene Zuordnung ausdrücklich protokollieren. |
| **K1 – Konsolenseite** | ADM485 Versorgung Pin8 gegen Pin5/P2.7; Pin6 und Pin7 jeweils gegen P2.7 | DC im Standby, beim Start. Größe der Versorgung und A/B-Pegel notieren; kein pauschales „Abstand <0,3 V = Defekt“. | Versorgung oder Referenz auffällig → zuerst dort eingrenzen. Gleichspannung allein übersieht kurze Differenzstörungen. |
| **K2 – Konsolenseite** | ADM485 RO/Pin1 bzw. OC06-Kathode gegen P2.7 | Oszi DC, korrekt eingestellter Tastkopffaktor; zunächst AUTO zur Pegelbestimmung, dann passende Flanke/Schwelle und Zeitbasis für START/Einzelereignis. 2 ms/div ist nur ein Startwert, ggf. Übersichtsaufnahme über den ganzen Ablauf. | Unerwartete Übergänge bei sicher stillstehendem Band **vor** der Fehlermeldung sind ein gezielter Befund. Noch kein alleiniger Beweis für falsche Tachoimpulse oder den defekten ADM485. |
| **K3 – falls K2 auffällig** | P4-Tachosignal und ADM485-Eingang Pin7, bei Bedarf Vergleichseingang Pin6; jeweils P2.7 | Passende Signalform/Zeitskala, vergleichbarer Zustand. Auch Empfängerfreigabe/Pin2 und Versorgung berücksichtigen, wenn RO-Übergänge nicht zum Eingang passen. | Schon vor ADM485 gestört → Sensor/Versorgung/Kabel/Eingangsnetz. Eingang plausibel, RO auffällig → Vergleichspegel, Empfängerzustand/Aufbereitung prüfen. Zur sicheren Tacho-Funktionszuordnung muss RO nachvollziehbar auf echte Sensorwechsel reagieren; ein separater Bewegungsversuch darf den Starttest nicht vorbelasten. |
| **K4 – Konsolenseite** | P2.6 und/oder OC05 Pin1 gegen P2.7 | Oszi DC im Standby/START; High/Low, Frequenz, Tastgrad notieren. Anode liegt an einer LED, deshalb keine 5-V-Pulshöhe dort fordern. | Belegt das Konsolensignal; beweist noch nicht die Übertragung durch OC05. |
| **N1 – Netzseite, geeigneter Aufbau erforderlich** | +5VA und ±12VA gegen 0VA | DC, ergänzend MIN/MAX; bei Anlass zeitaufgelöst. Größenordnung/Polarität der beschrifteten Schienen erwartet, exakte Toleranzen unbekannt. | 13,5 V am Gate-Treiber/L4981 ersetzen diese Prüfung nicht. Kurze Einbrüche/Ripple können DMM-Messungen entgehen. |
| **N2 – Netzseite** | OC04 Pin3 (Enable/MCU12), OC05 Pin3 (PWM/MCU17/18), jeweils 0VA | OC04 Pegel und Zeitpunkt; OC05 Pulsform: Low/High/Frequenz/Tastgrad. OC05-Emitter wird bei LED-Strom positiver. | Der bisher abgeleitete PWM-Mittelwert etwa 0,5–0,7 V kann gute hohe Pulse bei kleinem Tastgrad oder einen unzureichenden Pegel bedeuten. Keine festen MCU-Schaltschwellen ohne Typkenntnis. |
| **N3 – Netzseite** | X: C-Signalseite / bestätigtes Via oberhalb LD3N-L; Y: LD3N-O; jeweils 0VA | X Signalform und Amplitude, DC/Hz nur ergänzend. Y zunächst DC und Stabilität. Modelle: X ca. 3,7 V Spitze, Y etwa 0,8 V bei Raumtemperatur. | Modelle sind keine Freigabegrenzen. Fehlende Hz-Anzeige beweist keinen Defekt. Y=0 V unterscheidet Fühlerunterbrechung nicht von fehlender Versorgung/Kurzschluss. Bei auffälligem X entlang J → TL082 Pin3 → Pin1 → N → X vergleichen. |
| **N4 – Netzseite** | T4-1001: **MCU-seitiges Ende und Basis-seitiges Ende**, je 0VA; danach bei Bedarf T4-Kollektor/Spule | Netz-Ein, Standby, START; DC/MIN/MAX als Vorprüfung, kurze Befehle mit geeigneter Einzelaufnahme. Einschaltzeitpunkt der Firmware unbekannt. | Quelle high, Basis niedrig: Widerstand/Kontakt/Basislast prüfen. Basis etwa 0,6–0,8 V und ausreichender Basisstrom, aber Kollektor bleibt hoch: Treiberweg prüfen. Beide Enden niedrig: kein anhaltender Befehl erfasst, Ursache davor/Quellzustand offen. |
| **N5 – nur bei weiter offenem Ablauf** | Steuerleitung T3, T4-Basis bzw. T2-Testpad, 0VA | Geeignete Einzelaufnahme für kurze Schaltversuche; pro Lauf Messpunkt eindeutig nennen. | DMM-MAX ab etwa 0,5 s kann kurze Versuche übersehen. T2-Basis bleibt ohne bekannte Quelle kein direkter MCU-Ausgangsnachweis. |

N1–N5 sind keine pauschale Freigabe für das OT3 auf Netzpotential. DMM-Prüfungen können grobe Pegelfehler zeigen; wenn nur die Pulsqualität offen bleibt, ersetzen weitere Widerstandsmatrizen keine geeignete zeitaufgelöste Messung.

## Was sich gegenüber dem bisherigen Plan ändert

- Erledigte J-/Y-/P600-/F27-Zuordnungen nicht wiederholen. Kein Rückgriff auf den widerlegten R2-Serienpfad.
- Nach den konstanten ADM485-/OC06-Pegeln zuerst den tatsächlichen Pfad ab P4 stromlos prüfen. OC06 nicht allein aufgrund der Widerstandskopplung als Tachokanal behandeln. OC02/03/08/Wake-up/Sleep bleiben ohne konkreten Pfadbefund nachrangig.
- Nicht jeden RO-Puls sofort als Tacho-Fehler interpretieren. Zuerst Funktion, tatsächlichen Stillstand und zeitliche Reihenfolge absichern.
- Keine pauschalen Aussagen „≥4 V sicher“, „2–3,5 V grenzwertig“, „beidseitig 0 V im Diodentest = dieses Bauteil defekt“. Typgrenzen und eingelötete Parallelwege beachten.
- F27-Spulenmessung nur gezielt wiederholen, wenn ein Steuerbefehl/kurzer Versuch oder Widerspruch gefunden wird. Kein weiterer Batterie-Test ohne Anlass.
- B18/B19 bleibt PFC-Rückführung; während gehaltener T3-Sperre nachrangig. Y ist jetzt Temperaturkandidat, nicht Strommess-/Nulldurchgangskandidat aus dem TL082-Feld.
- Weitere Reinigung/Nachlöten, unbekannte Testpunkte, breite RS-485-Suche und MCU-/EEPROM-Tausch erst bei entsprechendem Befund. Dunkle Stellen allein beweisen keine Kriechströme.

Vorhandene Markierungsfotos bleiben unverändert. Für Funktion und Reihenfolge gilt dieser Stand; Messpunkte aus alten Bildern anhand der unveränderten lokalen Bezeichnungen und des aktuellen Netzmodells wählen.
