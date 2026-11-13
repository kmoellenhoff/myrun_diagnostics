# Q2-Fotospuren und Tacho-Hypothese – 12.11.2026

Ausarbeitung begonnen am 12.11., abgeschlossen am 13.11.2026. Verzeichnisname bleibt zur Zuordnung erhalten.

Vorläufiger Entwurf, keine neuen elektrischen Messungen. Grundlage: Branch `110926` bei `975aef6`, ergänzt um `main` bei `1b52c0c`, insbesondere LAUF_2026-11-11.md und NEUBEWERTUNG_2026-11-12.md. Claudes Raster A–L × 1–6 sowie Q2/B21/B5 und die lokalen Anschlussnamen bleiben unverändert. „D5“ ist hier der **lokale Treiberanschluss**, kein neu zugeordnetes Rasterfeld.

[Fotoblätter und Schaltungsentwurf (PDF)](Q2_Fotospuren.pdf). Originaldateien bleiben unverändert. Die PDF enthält Originalfoto-Ausschnitte mit separaten Vektormarkierungen; keine generierten Platinenbilder. `quellen_sha256.json` dokumentiert die verwendeten Originale.

**M** = vorhandene elektrische Messung; **F** = jetzt optisch verfolgte Leiterbahn, noch keine Durchgangsbestätigung; **I/H** = bedingte Typ-/Funktionsannahme. Fotoverbindungen bleiben getrennt vom bestehenden gemessenen Gesamtschaltplan.

## 1. Konkreter neuer Zusammenhang an A

Referenzorientierung: `photos/2026-11-09/q2/50386.jpg`, Treiber oben drei Pins **A/B/C** von links nach rechts, unten **D5/E**. Widerstandsnamen beziehen sich ausschließlich auf diese lokale Gruppe.

| Verbindung | Beleg | Einordnung |
|---|---|---|
| A → linke Kappe des horizontalen 4752 | F | Im Nahmakro nachvollziehbare gebogene Bahn; NICHT D5. |
| Linke Kappe 4752 → linke Kappe des horizontalen 1001 darüber | F | Kurzer senkrechter Kupferabschnitt zwischen den Kappen. |
| Rechte Kappe 4752 → linke Kappe des kleinen Keramikkondensators rechts daneben → B | F | Breiter Kupferbereich; B ist separat als 0VA gemessen. |
| Rechte Kappe 1001 → linke Kappe 2211 rechts daneben | F | Kurzer Kupfersteg; Bestätigung besonders sinnvoll. |
| Linke Kappe 2211 → 1P.O (oberer Einzelpin) | M | Vorhandene 0-Ω-Messung. |
| Rechte Kappe 2211 → C | M | Vorhandene 0-Ω-Messung. |
| 1P.R (unten rechts) → 0VA | M | 0 Ω beidseitig. |
| C → Abblockkondensator, rechte Kappe in 50386 | M/F | Messung vom 11.11. in um 180° gedrehter Aufnahme; dort linke Kappe. Nach Nachlöten konstant 0 Ω. |
| C → L4981AD Pin 19 (VCC) | M | 11.11.: 0 Ω; gemeinsame Versorgung, keine Aussage über deren Betriebsspannung. |
| E → RG-U → 22-Ω-Widerstand → Q2.G | M/F | E–RG-U ≈0 Ω; Widerstand gemessen 22,2 Ω; Gatebahn bekannt. |

Daraus ergibt sich als **Fotoentwurf**:

```text
C / gemeinsame VDD ── 2211 (2,21 kΩ) ── N ── 1001 (1 kΩ) ── A
                                      │                    │
                                     1P.O                 4752
                                      │                 (47,5 kΩ)
                               1P, NPN-Kandidat            │
                                1P.R ─────────────────── B / 0VA
                                1P.L: Ansteuerung offen

D5 ── eigener Leiterbahnzug; Ursprung / nächster Anschluss nicht gesichert
E  ── 22,2 Ω ── Q2.G
C  ── kleiner Abblockkondensator, Wert unbekannt ── B
```

N ist nur ein Netzknotenname im Entwurf, kein neuer Platinenmesspunkt.

**Messwertabgleich:** A–0VA 4,17 kΩ beidseitig; eingelöteter 4752 4,16 kΩ beidseitig. Das stützt den Fotobefund, beweist ihn allein aber nicht. Der Aufdruck 4752 bedeutet 47,5 kΩ; der niedrigere In-circuit-Wert enthält Parallelwege. 1001: 979/977 Ω; 2211: 2,09 kΩ beidseitig. D5–0VA 1,66 kΩ beidseitig passt zu einem anderen Netz.

**Funktionsidee [H]:** Unter der FAN3100C-Annahme ist A = IN+, D5 = IN−. Der 2211 wäre ein Pull-up zum gemeinsamen VDD-Netz; über 1001 erreicht dessen Knoten A. Leitet der 1P-NPN-Kandidat, zieht er diesen Knoten und damit A niedrig und sperrt den Gate-Ausgang. Sperrt er, kann A hoch werden. Der 4752 zieht A zusätzlich gegen Masse. Ein idealisiertes unbelastetes Widerstandsmodell ergibt A ≈ 0,94 × VDD bei gesperrtem 1P; das ist KEIN gemessener oder garantierter Betriebswert. Die Herkunft von 1P.L und D5 ist noch nicht geklärt. Ein klemmender/angesteuerter 1P wäre damit ein gezielter Untersuchungszweig, kein bewiesener Defekt.

Für FAN3100C gilt bedingt: OUT hoch nur bei IN+ hoch UND IN− niedrig und ausreichender VDD. Deshalb genügt eine Messung von A allein nicht. [Herstellerdatenblatt](https://www.onsemi.com/pdf/datasheet/fan3100t-d.pdf). Keine Eingänge überbrücken oder zwangsweise freigeben.

## 2. D5: Grenze der Fotorekonstruktion

D5 führt im Nahmakro zum runden blanken Pad links unterhalb des Treibers und von dort diagonal nach links oben aus dem Ausschnitt [F]. Im überlappenden Weitfoto ist die Fortsetzung in das enge Leiterbahnbündel neben der LED-/P70-Zone erkennbar. Weitere Makros zeigen dessen Verlauf, aber der eindeutige Übergang bis zu einem bestimmten Widerstand, Transistor- oder MCU-Pin lässt sich nicht belastbar festlegen. Kein MCU-Pin und kein Tacho-Netz wird deshalb angeschlossen. Insbesondere ist „D5 = PWM vom MCU“ nur eine Funktionshypothese.

## 3. Nur vier gezielte Durchgangsbestätigungen für den neuen Entwurf

Stromlos, vom Netz getrennt, Zwischenkreis nachweislich entladen. Niedrigster Ω-Bereich, Messleitungswiderstand zuerst bestimmen; erwartet jeweils etwa dessen Wert, stabil und in beiden Richtungen gleich. Keine neue Betriebs-/Hochspannungsmessung aus diesem Entwurf ableiten.

1. **A → linke Kappe 4752**; bisher nur F, Soll ≈0 Ω nach Leitungsabzug.
2. **Linke Kappe 4752 → linke Kappe 1001**; bisher nur F, Soll ≈0 Ω.
3. **Rechte Kappe 1001 → linke Kappe 2211**; bisher nur F, Soll ≈0 Ω.
4. **Rechte Kappe 4752 → B/0VA**; bisher nur F, Soll ≈0 Ω.

Die Endkappen sind im PDF markiert. Ein abweichender stabiler Widerstand bedeutet zunächst: Fotozuordnung/Netzmodell überprüfen; nicht sofort Bauteildefekt. Am 1P steht zusätzlich weiterhin der bereits vereinbarte Diodentest L↔R und L↔O aus. Eingelötete Parallelwege erlauben daraus allein keine sichere Typbestimmung.

## 4. Speed-Sensor als Ursache oder Folge

**Ein intermittierender Sensor-/Tacho-Pfad ist nicht ausgeschlossen.** Die Formulierung „Encoder ausgeschlossen“ in der Neubewertung vom 12.11. ist zu stark. Belegt sind mechanische Inspektion, ein sich mit Bewegung ändernder Mittelwert am P2.9 und 300–310 Hz während des guten 95-s-Laufs am 07.11. Das belegt zeitweise Funktion, keine fehlerfreie Impulsform im Fehlermoment.

Dokumentierter funktionaler Weg: optische Gabel am Motor → P4.TACHO → noch nicht vollständig aufgelöste Aufbereitung auf der GIRT → P2.9 → Konsolenauswertung/RENC. P4.0V = P2.7/P2.8, **nicht 0VA**. P4.TACHO–P2.9 wurde mit 16 kΩ gemessen: keine direkte Kupferverbindung daraus machen. Ein möglicher zusätzlicher Abzweig zur GIRT-MCU ist elektrisch noch nicht durchgehend belegt. Empfang von RENC an der Konsole beweist deshalb nicht automatisch einen intakten GIRT-internen Tacho-Eingang.

Die vorgeschlagene Kette „Band läuft an → Tacho fällt aus → Sperre → spätere Folgefehler“ ist plausibel. Nicht belegt ist der zusätzliche Zustand „nach Neustart trotz dunkler STS2 weiterhin intern gesperrt“. Konsolen-Neustart, quittierter Fehler und DUMPIO-Enable=1 sind kein sicherer Reset-Nachweis der GIRT. Auch dunkle STS2 allein beweist weder eine versteckte Sperre noch vollständige Antriebsbereitschaft.

Gegen eine einfache Sensor-allein-Erklärung sprechen:
- 08.11. und 11.11.: Fehlstart mit gemeldeten 0 V am Motor. Am 08.11. war die MAX-Erfassung langsam; sehr kurze Ansteuerimpulse sind nicht ausgeschlossen. Ohne Bewegung ist RENC=0 erwartbar.
- 10.11.: err 4 nach kurzem Lauf, später err 9 ohne Lauf. Blinkzahl 4/9 beobachtet; die Bedeutungen OU/OtM stammen aus einer verwandten Handbuchtabelle, nicht aus einer verifizierten S6T30-Firmwarebeschreibung.
- 11.11.: Fehler 9 auch im Stand. Enable verschwand; Ursache/Folge zeitlich nicht eindeutig aufgelöst.
- 11.11.: tatsächlich gemeldeter intermittierender Kontakt am Treiber-VDD-Fuß; nach Nachlöten besserer Lauf, später erneut Fehlstarts. Das ist ein konkreter elektrischer Befund neben der Sensorhypothese.

**Gezielter nächster Vergleich:** vorhandenes `myrun_renc_watch.py --duration 120` verwenden. Das Skript sendet nur lesendes `@RENC#` und keinen START, STOP oder Steuerungs-Init. Ein Softwarefehler kann dadurch nicht als ausgeschlossen gelten, aber die Messung verändert keine Fahrbefehle. Bei sicher gegen unerwarteten Anlauf abgesichertem Prüfaufbau kann man die Reaktion auf langsame Bewegung des Bands ohne Startbefehl vergleichen: frisch eingeschaltet sowie im bereits vorhandenen Fehlerzustand. Keine Hände an offene Motor-/Riemenmechanik und keine Arbeiten an der unter Netzspannung stehenden Platine.

| Ergebnis bei tatsächlicher Bewegung | Schluss |
|---|---|
| RENC reagiert in beiden Zuständen plausibel | Dauerhafter Totalausfall Sensor→Konsole unwahrscheinlich; kurze Aussetzer und GIRT-Abzweig bleiben offen. |
| Bewegung, aber reproduzierbar RENC=0 oder Aussetzer | Sensorversorgung, Gabel, Kabel/P4 und Aufbereitung gezielt prüfen; allein daraus noch nicht Sensor defekt. |
| Nur Stillstand, RENC=0 | Keine diagnostische Aussage zum Sensor. |
| TIMEOUT/keine Antwort | Kommunikationsbefund, nicht mit gemessenen 0 Hz gleichsetzen. |

Ein eindeutig beobachteter Tachoausfall **vor** dem mechanischen Abbremsen würde die Hypothese stark stützen. Die ungefähr sekündliche BLE-Abfrage kann kurze Aussetzer und die genaue Reihenfolge beim 1-s-Lauf verpassen; dafür wäre eine fachgerecht isolierte, zeitaufgelöste Signalaufnahme nötig. Ein zweiter normaler Lauf allein trennt die Ursachen nicht.

**Priorität:** erst der gezielte Tacho-Vergleich und die vier neuen Kupferverbindungen; anschließend, falls Tacho unauffällig, Freigabe über 1P/A, D5 und gemeinsame Treiber-/PFC-Versorgung. Ein erneuter breiter Tausch von Elkos oder Nachlöten ohne Befund folgt aus den vorhandenen Daten nicht.


## 5. Abgleich mit den inzwischen hinzugekommenen Repo-Änderungen

Am 13.11. nochmals `main` bis `1b52c0c` gelesen: neuer bebilderter Messplan, Reset-Hypothese und schnellerer Encoder-Poll. Der neue Messplan übernimmt den oben beschriebenen Fotoentwurf, erhebt aber manche Hypothesen bereits zu Mess-Sollwerten. Folgende Punkte sind zu korrigieren:

- **„O–R deutlich unter 48 kΩ = Leck“ ist eingebaut unzulässig.** Neben 1001 + 4752 liegt der Weg über 2211 und das gemeinsame VDD-Netz. Mit nominell 2,21 kΩ und dem früher gemessenen C–0VA-Wert von 1,45 kΩ liefert eine grobe ohmsche Ersatzrechnung `(2,21 + 1,45) kΩ || (1 + 47,5) kΩ ≈ 3,40 kΩ`. Bereits am 09.11. wurden von 1P.R zur linken 2211-Kappe (=1P.O) **3,38 kΩ** gemessen (Q2C-05). Das passt zu Parallelpfaden ohne notwendigen Transistordefekt. Die Rechnung ist keine exakte Vorhersage: IC-/Halbleiterpfade sind nichtlinear, und die In-circuit-Messwerte enthalten selbst weitere Wege. Auch umgepolt nicht-OL im Diodentest beweist eingelötet noch keinen Defekt.
- **„A ohne Takt = Fehler“ ist nicht gesichert.** A kann in diesem Entwurf eine statische Freigabe sein, während D5 taktet. Umgekehrt kann D5 Schutzfunktion haben. Die tatsächliche Rollenverteilung ist offen; alle drei Zustände A/D5/VDD zählen.
- Länger leuchtende +5V nach Netz-Aus stützen eine verbleibende Versorgung, beweisen aber weder einen unterbliebenen MCU-Reset noch, dass *alle* bisherigen Fehler Folgefehler waren. Den ersten Fehler nach vollständigem Abschalten getrennt protokollieren ist sinnvoll. Keinen stärkeren Entladewiderstand ohne Auslegung nachrüsten.
- Der neue `--listen-poll 1 --slow-every 5`-Modus fragt RENC häufiger ab, aber jede fünfte Runde weiterhin mehrere lange Antworten. Das ist kein durchgängiges 1-s-Raster. Für den reinen Sensorvergleich bleibt der vorhandene RENC-only-Watcher einfacher. SPEED_JUMP/LOSS beim ungleichmäßigen Schieben oder bewussten Anhalten sind zunächst Bewegungsbeobachtungen, kein Sensordefekt.
- Der Plan empfiehlt externe Spannung direkt an der eingebauten Relaisspule. Das kann andere Schaltungsteile rückspeisen. Ein externer Relaistest braucht vorher elektrische Trennung der Spule vom Treiber/Versorgungsnetz und bestätigte Polarität/Typdaten. Aus einem ausbleibenden Klick bei Unterspannung folgt noch kein defektes Relais.

Die Netzspannungsmessungen des fremden Plans werden hier nicht als nächster Heimtest übernommen. 0VA ist Netzpotential; ein 600-V-Messbereich allein stellt keinen sicheren Messaufbau her. Der Entwurf dient zuerst den beschriebenen stromlosen Zuordnungen und dem Tacho-Vergleich.
