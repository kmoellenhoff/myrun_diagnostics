# Arbeitshypothese 18.11.2026: gestörte Netzerkennung verhindert Motorfreigabe

Abgleich der Fehlstart-Logs mit dem [gemeinsamen Schaltplan](gesamtschaltplan_110926/README.md), dessen [Netzliste](gesamtschaltplan_110926/netze.csv) und den letzten Messungen. **Keine neuen Messungen; Ursache und Firmwareablauf nicht bewiesen.**

Belegstufen: **M** = berichtete elektrische Messung, **O** = Log-/Videobeobachtung, **I** = Ableitung, **H** = Hypothese. MCU-Pins sind die bestehenden Arbeitsnummern, keine bestätigten Datenblattfunktionen.

## 1. Hypothese und bekannter Signalweg

**[H] Eine intermittierende Störung im B10-Diodenbereich verfälscht J und damit den Netzerkennungs-Eingang X der GIRT-MCU. Die lokale Steuerung verweigert oder entzieht daraufhin die Leistungsfreigabe. Die Konsole fordert weiter Motorleistung an, erhält keine Drehzahl und beendet den Start mit Fehler.**

Der elektrisch rekonstruierte Messweg lautet: B10-Zweige von L/N über jeweils 2 × 475 kΩ und eine Diode → gemeinsamer Knoten J → 1 kΩ → TL082 Pin 3; Pin 1 = Pin 2 als Spannungsfolger → R1 (4,75 kΩ) → Teilermitte N, R2 (4,75 kΩ) nach 0VA → 100 Ω → X/MCU28 mit Filterkondensator nach 0VA. Beleggrenzen einzelner Zuordnungen stehen im [B10–X-Review](PRUEFUNG_B10_X_2026-11-17.md). Die Teilermitte N ist **nicht** der Netz-Neutralleiter.

J ist ein **Messsignal**, keine Versorgung des gesamten Boards. Elektronik-Hilfsversorgung und der aus dem Netz gespeiste Zwischenkreis können weiter vorhanden sein, obwohl das Netzsignal falsch ist. Die Bandmotorenergie kommt aus dem Zwischenkreis über die Q2-Leistungsstufe. [I]

Bekannte Steuerwege der GIRT-MCU sind MCU11 → T3 → L4981 Pin 15 (PFC-Sperre) und MCU24 → T4 → F27-Spule. Dass ein falsches J/X genau diese Wege betätigt, ist nicht gemessen. Die Quelle der T2-Ansteuerung und die vollständige Erzeugung der Q2-Gate-PWM sind weiterhin offen. **Ein Relais, das B10/J abtrennt, ist nicht nachgewiesen.**

## 2. Was die Fehlstart-Logs tatsächlich zeigen

Beispiel: [14.11., Start per Skript 12:58, Rohlog](logs_2026-11-14/start_per_skript_125808.txt) und [CSV](logs_2026-11-14/start_per_skript_125808.csv). Zeiten ab protokolliertem START bei t = 49,817 s, gerundet; unterschiedliche Größen werden nacheinander abgefragt und sind keine simultanen Messungen. [O]

| Zeit ab START | Beobachtung |
|---|---|
| 0 s | START gesendet und quittiert; Sollgeschwindigkeit 1,2 km/h |
| +4,9 s | `PWM_MOTOR` 0 → 7446 |
| +9,3 s | `PWM_MOTOR` 7446 → 8526; `EM_POWENA` und zugehörige Enable-Signale 1 → 0 |
| +15,4 s | Enable-Signale wieder 1; `PWM_MOTOR` 8526 → 6726 |
| +23,2 s | `QSHardwareFault`; am Ende neuer Fehlerspeichereintrag HF904 |
| Gesamter Versuch | Alle erfassten Encoder- und MeasSpeed-Werte 0 |

Weitere passende Befunde:

- [11.11., 15:08](logs_2026-11-11/myrun_fast_monitor_20261111_150758.txt): Beim zweiten Start `QSRunning`, `PWM_MOTOR` 6126 und Enable-Signale 1, Encoder 0; später `QSHardwareFault` und HF904. Der Nutzer hatte dazwischen STOP gedrückt. [O]
- [14.11., 12:45, Start direkt an der Konsole ohne Skript-Initialisierung](logs_2026-11-14/lauf_nach_reinigung_124536.txt): START t = 31,235 s, `QSRunning` 33,535 s, `PWM_MOTOR` 6966 bei 35,550 s; Encoder durchgehend 0. Nutzer-STOP bei 47,587 s, `QSHardwareFault` 56,051 s, Enable-Abfall 57,808 s. Der Fehlerzeitpunkt ist wegen des vorherigen STOPs kein isolierter Nachweis eines automatischen Anlauf-Timeouts. [O]
- Beim synchronisierten Video-/Logabgleich vom 08.11. begann STS2 etwa 1,3 s **vor** dem Enable-Abfall der Konsole zu blinken; siehe [Hardware-Protokoll, Abschnitt 5](HARDWARE.md#5-fault-behaviour-summary). Das unterstützt eine zuerst lokal erkannte Störung, bestimmt aber nicht deren Eingang. [O/I]

**Bewertung [I]:** Die Konsole kann weiter Antrieb anfordern, obwohl die GIRT-Leistungsstufe nicht wirksam arbeitet. `QSRunning`, `MotON` und `PWM_MOTOR` aus der Konsolendiagnose sind keine Messung der tatsächlichen Q2-Schaltimpulse und kein bestätigter interner GIRT-MCU-Zustand. Hohe Konsolen-Enable-Rückmeldungen beweisen ebenfalls keine vollständige Freigabe aller lokalen Schutzfunktionen.

## 3. Präzisierung der PWM-Rollen

Die vorherige Erklärung „Konsole sendet nur einen per PWM codierten Geschwindigkeitssollwert, GIRT berechnet alles Weitere“ war zu bestimmt.

- P2.6 ist nach bisheriger Servicezuordnung und Messung der Anforderungskanal zur GIRT über OC05. Am OC05-Eingang wurden beim Start Pulse beobachtet; ein gültiges Signal am MCU-Eingang ist damit noch nicht vollständig dynamisch geprüft. [M/O/I]
- Bei gleichbleibender Sollgeschwindigkeit und ausbleibender Drehzahl steigt `PWM_MOTOR`. **Das spricht dafür, dass die Konsole bereits eine Motorstellgröße berechnet und erhöht**, statt lediglich eine feste Geschwindigkeitszahl zu übertragen. Die vollständige Aufteilung der Drehzahlregelung zwischen Konsole und GIRT bleibt offen. [O/I]
- `PWM_MOTOR` und die mit Prozentzeichen ausgegebene `@RPWM`-Antwort sind Diagnosewerte der Konsole. Skalierung und Beziehung zur tatsächlichen Q2-Gate-PWM sind nicht abschließend geklärt. Aus ihnen wird hier kein physischer Tastgrad des Motortransistors abgeleitet.

Die Hypothese benötigt lediglich eine Motoranforderung von der Konsole und eine lokal verweigerte Umsetzung; sie setzt keine bestimmte Aufteilung des Drehzahlreglers voraus.

## 4. Warum B10 konkret verdächtig ist – und was fehlt

- Die [Prüfungen vom 17.11.](LAUF_2026-11-17.md) zeigen eine mechanisch auslösbare Unterbrechung im unteren B10-Diodenbereich, anschließend auch einen auffälligen Test der ausgebauten unteren Diode. Das ist der konkrete Reparaturbefund. Die zweite Diode ist nicht gleichermaßen als defekt nachgewiesen. [M]
- J wurde zeitweise mit etwa 5 V und zeitweise nur wenigen hundert Millivolt gemeldet. Mehrere Betriebsmessungen erfolgten mit handgehaltenen Spitzen; Kontaktierungsfehler sind nicht vollständig ausgeschlossen. [M/O]
- Während dokumentierter Fehlstarts waren Treiber-VDD 13,5 V und Zwischenkreis 316 V vorhanden; F27 zog in späteren Messungen nicht an. Das unterstützt die Suche nach einer nicht erfüllten Startbedingung, beweist aber weder eine bewusste MCU-Sperre noch B10 als deren Ursache. Siehe [14.11.](LAUF_2026-11-14.md). [M/I]
- **J/X wurden in den ausgewerteten Fehlstart-Logs nicht gleichzeitig erfasst.** Es fehlt die zeitliche Korrelation zwischen Netzsignalstörung und ausbleibender Freigabe. MCU-Schwellwerte, Firmwareablauf und vollständige Rückmeldung zur Konsole sind unbekannt.
- Der Ausfall nur eines gleichrichtenden Zweiges erklärt im einfachen Modell fehlende Halbwellen bzw. ungefähr den halben Mittelwert. **Er erklärt allein nicht J ≈ 0,3 V.** Zweiter unterbrochener Pfad, zusätzliche Belastung oder Messkontakt bleiben mögliche Erklärungen; keine davon ist bewiesen.
- Der am 18.11. diskutierte zusätzliche 10-kΩ-Pfad von J zum SOT-23-5 wurde durch die [letzten Messungen](LAUF_2026-11-18.md) nicht bestätigt und ist keine Stütze dieser Hypothese.
- Ein fehlendes oder unplausibles Drehzahlsignal kann Folge fehlender Motoransteuerung sein. **HF904 und achtmal STS2-Blinken beweisen B10 als Ursache nicht.** Die komplette GIRT-spezifische Codetabelle ist nicht gesichert; der Handtest vom 14.11. erzeugte achtmal Blinken auch durch Bandbewegung im Standby. Frühere Code-4-/Code-9-Abbrüche sind mit der B10-Hypothese noch nicht vollständig erklärt.
- Alternative Ursachen bleiben eine andere lokale Startbedingung, ein unzureichendes OC04-/OC05-Signal auf der MCU-Seite, die Ansteuerungs-/Leistungsstufe oder ein noch nicht aufgeklärter Tacho-Pfad. Kein neuer Defekt dieser Bereiche festgestellt.

## 5. Empfehlung und überprüfbare Erwartung

**Nächster Schritt bleibt die gezielte Reparatur des B10-Diodenbereichs:** beide Dioden durch geeignete Ersatzteile ersetzen, korrodierte Anschlüsse reinigen und den bereits dokumentierten angehobenen Padbereich elektrisch und mechanisch sorgfältig instand setzen. Der Austausch der zweiten Diode erfolgt wegen desselben beanspruchten Bereichs, nicht wegen eines bereits bewiesenen zweiten Diodendefekts.

Danach unter vergleichbaren Bedingungen einen Kaltstart und wiederholte Startversuche mit denselben Logs beobachten; Band vorher nicht im Standby von Hand bewegen. J/X nur mit geeignetem, sicher vorbereitetem Messaufbau erfassen; keine Schutzfunktion überbrücken und J nicht künstlich auf +5 V legen.

**Stützendes Ergebnis:** Nach Reparatur stabiles, zur Netzversorgung plausibles J/X, zuverlässiges Anlaufen, Encoderanstieg und keine bisherigen Fehlstarts. Das wäre ein starker Zusammenhang. Bleibt der Fehler trotz plausibler Netzerkennung bestehen, erklärt der Diodenbefund das Problem nicht allein; dann andere Startbedingungen und die tatsächliche lokale Ansteuerung prüfen. Keine weiteren Bauteile ohne Befund tauschen.

Keine neuen Kupferverbindungen bestätigt: CAD/Netzliste und Originalfotos unverändert. Dieses Dokument ergänzt die historischen Bewertungen, ohne deren damalige Aussagen als aktuelle Beweise zu übernehmen.
