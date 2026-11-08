# GIRT S6T30: Teilschaltplan und weitere Fehlereingrenzung

Branch **110926**, auf Basis von `9d1f74617b602f57db36a1993998581de360b832`. Die vorhandenen Fotos, Messprotokolle und Claudes Raster bleiben erhalten. Neue elektrische Messungen wurden nicht durchgeführt.

[Schaltplan als PDF](teilschaltplan.pdf) · [Fotoatlas](../atlas_110926/README.md) · [Markierte Messkontakte und Messwertvorlage](../messplan_stromlos_2026-11-08/MESSPLAN.md) · [Verbindungsnachweis als CSV](verbindungen.csv)

## Was der Schaltplan abdeckt

| Blatt | Inhalt | Noch offen |
|---|---|---|
| [1: Motorstufe](blatt_1.svg) | L+/L−, Q2, Body-Diode, D3, 22-Ω-Gate-Pfad; NTC und Relais als getrennte Fragmente | Treibertyp und Pin-Funktionen, Versorgung/Freigabe, Relais-Netzanbindung |
| [2: B18/B19](blatt_2.svg) | 475-kΩ/1-MΩ/1-MΩ-Kette mit TP1/TP2; sichtbarer Weg P1 zum ersten B19-Widerstand | Teilerfusspunkt, Weiterweg ab B19-E2, Messeingang und B20-Netze |
| [3: B10 und Anschlüsse](blatt_3.svg) | Beide AC-Sense-Ketten mit Dioden; direkte P2/P4-Verbindungen | Kathoden-Auswertung, PWM-/Enable-/Tachoweg bis zu bestimmten IC-Pins |

![Motorstufe und offene Versorgungen](blatt_1.svg)

![B18 und erster B19-Anschluss](blatt_2.svg)

![B10 und Anschlussnetze](blatt_3.svg)

**Ein vollständiger Schaltplan lässt sich aus dem vorhandenen Material noch nicht zuverlässig erstellen.** Bauteile unter dem Kühlkörper, verdeckte Bahnen, unlesbare IC-Typen und unbekannte Ebenenwechsel bleiben Lücken. Der Fotoatlas schließt diese Lücken nicht durch Vermutungen. Die Zeichnungen sind elektrische Teilschaltungen; sie sind keine erzeugten Platinenbilder.

## Belege und Grenzen

- **M:** vorhandene Messung, mit Mess-ID in `verbindungen.csv`. Ein Messwert zwischen zwei Punkten ist nicht automatisch eine direkte Verbindung.
- **F:** im Originalfoto sichtbare Bahn oder Anschlusslage. Neue F-Verbindungen sollten durchgemessen werden, bevor sie als elektrisch bestätigt gelten.
- **I:** aus Aufdruck, Pinraster oder bisheriger Topologie abgeleitet. Ein gelesener Widerstandscode ist kein gemessener Einzelwert.
- **Offen/Modell:** gestrichelte Umrisse oder unbeschaltete Ports. Diese sind keine ergänzten Leiterbahnen.

Die gestrichelte graue Linie zwischen P4.TACHO und P2.9 auf Blatt 3 bezeichnet ausschließlich die gemessene 16-kΩ-Kopplung. Sie ist kein nachgewiesener Serienwiderstand. Ebenso werden 9,13 kΩ G–S, 223,7 kΩ P1–0VA und 226,4 kΩ P1–+5VA als **In-Circuit-Ersatzwerte** geführt; es wurden keine entsprechenden Einzelwiderstände identifiziert.

Die Zuordnung Q2-D = L− und Q2-S = 0VA folgt dem bisherigen Stand, dem Pinout und Diodentest. Ein neues separates Pad-zu-Klemmen-Durchgangsprotokoll liegt nicht vor. Bei D3 wurde Schwarz = L+ im ursprünglichen PW-M01-Protokoll angenommen. Dieser Vorbehalt bleibt erhalten.

B19-Rin ist ein neuer lokaler Name für den unteren horizontalen Widerstand mit Code `1001` im Originalmakro `PXL_20261108_153921371.jpg`. Seine Pads heißen im Messplan **E1** (P1-Seite) und **E2**. Sichtbar ist P1 → E1; der elektrische Durchgang ist noch nicht neu gemessen. Am Treiber heißen die fünf Kontakte **A/B/C/D5/E**, entsprechend dem markierten Originalmakro. Das sind keine Hersteller-Pinnummern. E → RG-U ist als sichtbare Bahn eingezeichnet; die Funktion „OUT“ oder eine bestimmte Treiberversorgung wird daraus noch nicht abgeleitet.

Die Relais-Pinzuordnung basiert auf Gehäuselage und RT1-Pinraster. Ca/Cb sind das Spulenpaar; ihre individuelle A1/A2-Zuordnung bleibt offen. 11a/11b und 14a/14b sind abgeleitete Kontakt-Doppelpaare, keine neuen Messbefunde. Herstellerangaben: [TE RT334024](https://www.te.com/en/product-4-1393240-8.html), 24 V DC, 1,44 kΩ Spule, 0,4 W, Schließer. Der Nennwert gilt für die Spule allein, nicht beliebig für die eingelötete Umgebung.

## Was sich am Fehler bereits eingrenzen lässt

| Befund | Daraus folgt | Bleibt möglich |
|---|---|---|
| Q2-Body-Diode 0,444 V/OL; G–S 9,13 kΩ beidseitig; G–D 2,19 MΩ; Gate-R-Pfad ca. 22 Ω | Dauerhafter D–S-Schluss oder harter Gate-Schaden wird durch die statischen Werte nicht gestützt | Treiber-/Versorgungs-/Freigabefehler und temperatur-/lastabhängiger Q2-Fehler |
| D3 0,397 V/OL laut bisherigem Test | Statischer Diodenschluss wird nicht gestützt | Dynamischer/intermittierender Fehler; ursprüngliche Polungsangabe beachten |
| B10 beide Ketten und Dioden unauffällig | Keine nachgewiesene dauerhafte Unterbrechung dieser AC-Sense-Ketten | Kontakt-/Leck-/Auswertefehler hinter den Ketten |
| B18-P2 = L+ mit 0 Ω; P1 führt in B19 | Konkreter Ansatz zur Verfolgung eines plausiblen Bus-/Motorspannungs-Messpfads | Vollständige Funktion, Fusspunkt, IC-Eingang und Verhalten beim Fehlstart |
| NTC ca. 11 kΩ kalt, 10,75 kΩ warm | Sensor zeigte einen plausiblen NTC-Trend | Intermittierender Stecker-/Leitungs-/Buchsenfehler; keine genaue Kennlinienprüfung |
| Motorwicklung 1,5–1,6 Ω über viele Rotorstellungen; Generatorwirkung beobachtet | Dauerhaft offene Wicklung wird nicht gestützt | Bürsten-/Lastfehler; erklärt noch nicht die ausgebliebene Ansteuerung |
| P2/P4 bis zum jeweils ersten Kontakt 0,3–0,5 Ω bei 0,2–0,4 Ω Spitzenwiderstand | Die zuerst geprüften Teilstrecken waren leitend | Weiterer Signalweg, Leckströme, druck-/temperaturabhängige Kontakte |
| STS2 setzt beim dokumentierten Fehlstart vor dem Enable-Abfall der Konsole ein | Der Konsole-Abbruch allein erklärt den ersten GIRT-Fehlerhinweis nicht | Falsches Eingangssignal, Sperr-/Messpfad oder Versorgung auf der GIRT |

**Arbeitsrichtung:** zuerst Versorgung, Relais/Kontakte und Treiber/Freigabe von einem vermeintlichen Leistungs-MOSFET-Defekt unterscheiden. Den Tachosensor nicht allein wegen einer vermuteten Blinkcode-Deutung ersetzen. Der Sensor-/Signalweg bleibt eine offene, prüfbare Möglichkeit; ein eindeutiger defekter Bauteil ist bisher nicht belegt.

Das dokumentierte Multimeter/MAX-Verfahren konnte kurze Ausgangspulse unter etwa 0,5 s nicht sicher erfassen. „Anzeige blieb 0 V“ bedeutet deshalb nicht, dass es garantiert keinen kurzen Ansteuerungsversuch gab. Auch 4 bzw. 8 STS2-Pulse belegen ohne GIRT-spezifische Codetabelle weder Überspannung noch Encoderfehler. Die verwandten Technogym-Handbücher liefern dafür nur eine Hypothese.

## Nächste Messungen mit Entscheidungskriterium

Die Kontaktbilder und Polungen stehen im [vorhandenen Messplan](../messplan_stromlos_2026-11-08/MESSPLAN.md). Dessen Reihenfolge bleibt bestehen. Neu ist hier die Entscheidung, welche Aussage ein Ergebnis tatsächlich erlaubt.

| Reihenfolge | Konkreter Test | Entscheidung nach dem Ergebnis |
|---|---|---|
| 1 | **F27 Ca–Cb**, Ω in beiden Richtungen; danach **11a–11b**, **14a–14b** und unbestromt **11a–14a** | Spule allein 1,44 kΩ ±10 % bei 23 °C. Ein niedrigerer oder polungsabhängiger In-Circuit-Wert erfordert Prüfung von Diode/Parallelpfad. OL beidseitig erst nach sicherem Kontakt als Spulenunterbrechungsverdacht werten. Doppelpaare sollten Spitzenwiderstand zeigen. Ein endlicher Widerstand quer über den Schließer beweist eingelötet keinen klebenden Kontakt. |
| 2 | **P600 Ka–Kb**, Sensor abgezogen: kalt, handwarm, bei konstanter Temperatur vorsichtig Leitung bewegen; Buchsen-Lötstellen separat prüfen | Gleichmäßig fallender Widerstand ohne Sprünge stützt den Sensor. Sprünge/OL grenzen auf Sensor/Leitung/Crimp ein. Ein stabiler Kabelseitenwert gibt die Buchse nicht frei; bei gestecktem Test können Platinen-Parallelpfade Fehler verdecken. |
| 3 | **B18-P1 → B19-E1**, danach **B19-E1 → E2**, jeweils Ω beidseitig; neue scharfe B19/B20-Makros | P1–E1 nahe Spitzenwiderstand bestätigt den ersten Weg. Bei sicherem Kontakt und deutlich abweichendem Wert die sichtbare Strecke/Lötstellen untersuchen. E1–E2: Code legt 1 kΩ nahe; niedrigerer In-Circuit-Wert ist nicht allein ein Widerstandsdefekt. Weiterverfolgung beginnt danach an E2. |
| 4 | **Q2-DRV A/B/C/D5/E** einzeln gegen **0VA** und **+5VA**, Ω und Diode beidseitig; **E → RG-U**; Treiberaufdruck neu fotografieren | Direkter Durchgang ordnet ein Netz zu. Das identifiziert noch keine Pin-Funktion und bestätigt +5VA nicht als tatsächliche Treiberversorgung. Fehlende Verbindung E–RG-U trotz sicherem Kontakt grenzt auf die sichtbare Gate-Treiber-Strecke ein. Typ erst nach sicher lesbarem Code festlegen. |
| 5 | **0VA ↔ +5VA**: Verlauf und Gegenrichtung; P400-Testlöcher zuerst zu den markierten Steckkontakten durchmessen, dann **+24V ↔ 0V24** | +5VA-Referenz bisher 2,16/2,55 kΩ. Dauerhaft nahe Spitzenwiderstand ist ein neuer Kurzschlussverdacht, passende statische Werte schließen dynamische Einbrüche nicht aus. Für 24 V gibt es noch keinen numerischen Ω-Sollwert. 0V24 und 0VA nicht ungeprüft gleichsetzen. |

Start-/10-s-/60-s-Anzeige, Endwert, Polung, Temperatur und Steckzustand eintragen. Weiter steigende/fallende Werte ausdrücklich als nicht eingeschwungen kennzeichnen. Keine neue Messung wurde in die Ergebnisfelder eingetragen.

### Kleiner erster Datenblock für die nächste Runde

1. Relais Ca–Cb: Wert in beiden Richtungen und stabil/steigend/fallend.
2. NTC abgezogen: Kaltwert, warmer Wert und Sprünge beim vorsichtigen Bewegen ja/nein.
3. P1–E1 und E1–E2: beide Richtungen.
4. E–RG-U: Wert; anschließend Treiber-Messmatrix aus der CSV.

Damit lässt sich zwischen einer Unterbrechung im Sensor-/Kontaktpfad, dem ersten Sense-Pfad und dem Gate-Treiber-Pfad unterscheiden, bevor Bauteile auf Verdacht ersetzt werden. Eine intermittierende Versorgung oder fehlende Gate-Ansteuerung im Betrieb lässt sich aus Fotos und stromlosen Widerständen allein nicht endgültig entscheiden.

## Messgrenzen bleiben bestehen

Netz und externe Versorgung trennen; Restspannung am Zwischenkreis-Elko zuerst in V DC prüfen. Gemäß Repository erst nach bestätigtem Wert unter 5 V zu den stromlosen Arbeiten wechseln; Ω/Diode nur spannungsfrei. 0VA ist DC− auf Netzpotenzial. Keine Kontakte überbrücken, kein fremdes Netzteil an Treiber/Spule einspeisen, nichts allein aufgrund eines In-Circuit-Werts ersetzen. Die im Stand zurückgestellten Live-Messungen bleiben zurückgestellt. Das hier gezeichnete getrennte Fragment einer Versorgung oder eines Sensors beweist keine galvanische Trennung.

## Nachprüfbarkeit

`verbindungen.csv` enthält 55 Einträge mit Art, Status und Quellen. `Kupfer direkt`, `Widerstand`, `Diode` und `In-Circuit-Messung` bleiben verschiedene Kategorien. Nur direkte Kupferverbindungen dürfen beim Weiterzeichnen zu einem gemeinsamen Netz zusammengefasst werden; Werte im kΩ-/MΩ-Bereich dürfen das nicht.

Die Originalquellen bleiben maßgeblich: `STAND_2026-11-08.md`, die aktuelle Fassung `netlist/b18_spannungssense_kandidat.md` ohne verworfene Historie, `netlist/q2_zuordnung.md` mit Ergebnisstand 21:39, die Mess-CSV-Dateien und `HARDWARE.md`. Die ältere unbestätigte Annahme P2 = L− und die pauschale Gate-Pulldown-Erwartung aus einem Zwischenstand werden nicht übernommen.
