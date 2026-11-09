# Blätter 05/05b: Q2 und Treiberumfeld – Ergebnisse vom 09.11.2026

**Im vorgesehenen stromlosen Umfang abgeschlossen; als Nächstes Blatt 06 (Hilfsversorgung).** Claudes Feld Q2/B21 = **B5** bleibt unverändert. Quelle sind Nutzer-Messungen und das neue Originalmakro 50386.jpg. Kein verursachendes defektes Bauteil nachgewiesen. Treibertyp, tatsächliche Versorgung, Freigabe/Eingang und Verhalten beim Schalten bleiben offen.

[Neue Aufnahme ohne EXIF](../../photos/2026-11-09/q2/50386.jpg) · [markierte Kontakte Blatt 05](makros/05.png) · [05b](makros/05b.png) · [Ergebnis-CSV](messprotokoll_2026-11-09.csv) · [Rohangaben mit Korrekturen](Q2_ROHANGABEN_2026-11-09.json) · [Teilschaltplan](../schaltplan_110926/README.md)

## Korrekturen und Herkunft

- Der frühere 220-Ω-Sollwert für Foto-ID R221 war falsch: Neues Originalmakro zeigt **2211 = 2,21 kΩ**. In Texten wird auch der Alias **R2211** verwendet. Die bestehenden R221-a/b-Pixel bleiben identisch. Der separate Gate-R trägt 220 = 22 Ω.
- **R1001: 979/977 Ω**, ausdrücklich vom Nutzer korrigiert („ohm nicht kohm“). Die anfängliche kΩ-Einheit ist zurückgenommen, keine gültige hohe Widerstandsmessung.
- **B–0VA im Diodentest: korrigiert 0,0 V**. Die anfängliche Vorwärtsanzeige 1,96 V erklärte der Nutzer als falsch gemessen. Gegenrichtung war bereits 0,0 V. Der vermeintliche Widerspruch zu 0 Ω beidseitig ist aufgelöst.
- A–+5VA rückwärts: Tippfehler „183“ unmittelbar auf **1,83 V** korrigiert.
- C–0VA und E-Referenzwerte: kΩ nachträglich ausdrücklich bestätigt. R2211 2,09 wird im fortlaufenden kΩ-Kontext als kΩ geführt; die Rohangabe schreibt die Einheit nicht erneut aus.
- „R-RGU 22,2 ohm“ wird als Messung im Gatewiderstandspfad dokumentiert. Der Nutzer schrieb als Startpunkt R, nicht ausdrücklich G; G und RG-G sind durch die erste 0-Ω-Messung elektrisch derselbe Knoten.
- Der Nutzer nennt den Treiberaufdruck **1000CA**. Das ist eine dokumentierte Lesung, keine bestätigte vollständige Typnummer. Die bisherige Recherche hat keinen eindeutigen, durch Herstellerdaten belegten Typabgleich ergeben. Keine Pin-Funktionen aus ähnlich klingenden Codes übernommen.

Alle Werte laut laufendem Ablauf stromlos und in-circuit. Temperatur, genaue Ablesezeit und detaillierte Steckzustände wurden nicht mitgeteilt. Leere Gegenrichtungen sind nicht berichtet, nicht automatisch OL oder gleich. Die Foto-IDs A/B/C/D5/E gelten nur am fünfpoligen Q2-Bauteil; keine Herstellerpinnummern, keine B19-Padnamen.

## Gate- und MOSFET-Pfad

| Messung | Ergebnis | Grenze |
|---|---|---|
| G–RG-G | 0 Ω | Gegenrichtung nicht separat berichtet |
| Gate-Seite–RG-U | 22,2 Ω | Rohbezeichnung des Startpunkts R; siehe oben |
| G–S | 9,14 kΩ beidseitig | eingelötetes Netz, kein isolierter Gate-Lecktest |
| G–D | 2,2 MΩ; rückwärts 1,86 MΩ langsam steigend | Rückwärtswert nicht eingeschwungen; Endwert offen |
| S→D, Diodenmodus | Referenz 0,444 V / rückwärts OL unverändert bestätigt | zusammenfassende Bestätigung „werte gleihgeblieben“, keine neuen Ziffernanzeigen |
| E–RG-U | ≈ 0 Ω ausdrücklich bestätigt | keine separat ausgeschriebene genaue Anzeige; Gegenrichtung nicht separat berichtet |

**Belegt:** E → RG-U → Gatewiderstand → RG-G → G. E–0VA 9,16 kΩ passt rechnerisch zu G–S 9,14 kΩ + 22,2 Ω = 9,1622 kΩ. Das stützt den Pfad; die direkte E–RG-U-Verbindung wurde zusätzlich ausdrücklich bestätigt. Q2 zeigt keinen neuen eindeutigen statischen Defekthinweis; Betriebsschalten und Ansteuerung sind damit nicht freigegeben.

## Treiberkontakte: Ω-Matrix

Erste Anzeige Rot am Treiberkontakt und Schwarz an der Referenz; zweite umgepolt.

| Kontakt | gegen 0VA | Gegenrichtung | gegen +5VA | Gegenrichtung |
|---|---:|---:|---:|---:|
| A | 4,17 kΩ | 4,17 kΩ | 6,7 kΩ | 6,7 kΩ |
| B | 0 Ω | 0 Ω | 2,18 kΩ | 2,57 kΩ |
| C | 1,48 kΩ | 1,45 kΩ | 3,72 kΩ | 2,57 kΩ |
| D5 | 1,66 kΩ | 1,66 kΩ | 11,69 kΩ | 9,16 kΩ |
| E | 9,16 kΩ | 9,16 kΩ | 11,68 kΩ | 11,68 kΩ |

**B = 0VA ist mit 0 Ω beidseitig gemessen.** B–+5VA 2,18/2,57 kΩ passt zur bisherigen 0VA–+5VA-Referenz 2,16/2,55 kΩ. Keiner der übrigen Kontakte zeigt in dieser Matrix eine direkte Verbindung zu +5VA. Daraus folgt weder eine bestimmte Versorgungsspannung noch eine Herstellerpinbelegung. Alle endlichen kΩ-Werte sind Ersatzwerte des angeschlossenen Netzes, keine isolierten Widerstände; sie werden nicht als Kupferverbindungen zusammengefasst.

## Treiberkontakte: Diodenmatrix

Erste Anzeige Rot am Treiberkontakt; zweite umgepolt. Alle Angaben in V.

| Kontakt | gegen 0VA | Gegenrichtung | gegen +5VA | Gegenrichtung |
|---|---:|---:|---:|---:|
| A | 1,96 V | 0,69 V | 2,2 V | 1,83 V |
| B | 0 V | 0 V | 0,44 V | 1,3 V |
| C | 0,84 V | 0,522 V | 1,16 V | 1,7 V |
| D5 | 2,75 V | 0,7 V | 2,8 V | 1,85 V |
| E | 1,33 V | 0,63 V | 1,69 V | 1,81 V |

Für B–0VA ist ausschließlich der korrigierte 0-V-Befund gültig. Anzeigen um 0,5–0,7 V sind mit Silizium-Halbleiterpfaden vereinbar; höhere Anzeigen können mehrere Schaltungspfade enthalten. Werte in beiden Richtungen beweisen eingelötet weder einen defekten IC noch dessen Funktionsfähigkeit. Kein Hersteller-Gut-/Schlecht-Grenzwert für den unbekannten Treiber wird erfunden.

## Drei Widerstände, Blatt 05b

| Foto-ID / Alias | tatsächlicher Code | Nennwert | erste Anzeige | Gegenrichtung |
|---|---|---:|---:|---:|
| R1001 | 1001 | 1 kΩ | **979 Ω** | **977 Ω** |
| R221 / R2211 | **2211** | **2,21 kΩ** | 2,09 kΩ | 2,09 kΩ |
| R4752 | 4752 | 47,5 kΩ | 4,16 kΩ | 4,16 kΩ |

R1001 liegt rund 2,1/2,3 % unter 1 kΩ, R2211 rund 5,4 % unter 2,21 kΩ. Das sind eingelötete Anzeigen, keine isolierten Toleranztests. R4752 liegt deutlich unter nominal 47,5 kΩ; ein Parallelpfad kann das erklären. Dass der effektive Wert nahe A–0VA 4,17 kΩ liegt, beweist allein noch keine direkte Zuordnung des Widerstands zu A. Es wird kein Einzelbauteil allein aufgrund dieser Messung als defekt erklärt oder ersetzt.

## Übergang und offene Fragen

Nächstes Blatt **06: 0VA / +5VA und Hilfsversorgung**. Der aktuelle Vergleich aus B (=0VA) gegen +5VA beträgt bereits 2,18/2,57 kΩ; eine zusätzliche Messung an den beschrifteten Testpunkten ist nur für andere Bedingungen oder einen Zeitverlauf ein neuer Befund. Sichtkontrolle von Regler-/Elkoanschlüssen bleibt sinnvoll. Ω-Messungen bestimmen weder ESR/Kapazität noch die Versorgung unter Last.

Offen bleiben Treibertyp/Herstellerpinbelegung, tatsächliche Versorgung und Eingangs-/Freigabesignal, MOSFET-Funktion im Betrieb, Einbindung aller umgebenden Widerstände sowie der rückwärts steigende G–D-Endwert. Keine Live-Messung, kein Auslöten und keine externe Einspeisung wurden durchgeführt. Die Fotos zeigen keine bewiesene leitfähige Verschmutzung oder einen sicheren Reparaturerfolg.

Neue Aufnahme vor dem GitHub-Import ohne EXIF/XMP, JPEG-Pixel unverändert. Bereits vorhandene Originalfotos, Rasterindex und alle acht markierten Makrokopien bleiben unverändert. Der Assistent hat selbst keine elektrische Messung durchgeführt.
