# Neubewertung 16.11.2026 (abends) – Durchsicht aller Unterlagen, weitere Ansätze

Ergänzt `NEUBEWERTUNG_2026-11-14.md` (dessen Befundtabelle und Kandidatenliste bleiben gültig). Grundlage: alle Protokolle (`LAUF_*`, `NEUBEWERTUNG_*`, `messplan_stromlos_2026-11-08/`, `netlist/`, `HARDWARE.md`, Logs) und der Gesamtschaltplan `gesamtschaltplan_110926/` (Quellenstand f60fe5d). **Keine neuen Messungen.**
Tags: [M] gemessen, [O] beobachtet, [I] gefolgert, [H] Hypothese.

## 1. Was die Durchsicht am Bild schärft

1. **Im Fehlstart geht die GIRT gar nicht in den Zustand „Lauf“.** STS1 blinkt im Bereitzustand mit 1 Hz und leuchtet im Lauf dauerhaft (`HARDWARE.md` §7) [O]. Im Fehlstart vom 07.11. 22:04 blinkt STS1 durchgehend weiter (`img/led_timeline.png`) [O]. Für die Fehlstarts ab 14.11. wurde STS1 nicht beobachtet.
2. **Code 08 kam am 07.11. schon ≤ 1,5 s nach START** [O], am 08.11. nach ≈ 5 s (dort Code 04). Ein Ablauf „Antrieb einschalten, auf Drehzahl warten, Zeitablauf“ passt dazu schlecht; eher wird der Fahrbefehl sofort abgewiesen [I].
3. **Derselbe Code 08 entsteht, wenn das Band im Standby von Hand bewegt wird** (14.11. 12:36) [M/O]. Code 08 heißt also „Drehzahl und Antriebszustand passen nicht zusammen“. Beim Fehlstart sind zwei Lesarten möglich: (a) Fahrbefehl ohne Drehzahl, (b) der MCU sieht beim Start ein Drehzahlsignal, obwohl er nicht antreibt [H]. Lesart (b) wurde bisher nicht geprüft; der Tacho-Kanal zum MCU ist nicht verfolgt.
4. Am 11.11. 15:08 gab es einen Fehlstart **ohne** STS2-Code [O]. Es gibt also mindestens zwei Varianten: „keine Reaktion“ und „sofort Code 08“.

## 2. Weitere Ansätze (alle [H], nach Gewicht)

### A – Widerspruch am Knoten J (Netzsignal)
- Schaltplan (15.11.): J → 22,1 kΩ → 0VA und J → 1,0 kΩ → TL082 Pin 3 (hochohmiger Eingang). Danach müsste J ↔ 0VA stromlos ≈ 22 kΩ zeigen.
- Gemessen am 08.11. (`netlist/messprotokoll_b10.csv`, B10-M23 bis M26): **J ↔ 0VA ≈ 6,4–6,8 kΩ**, J ↔ +5VA ≈ 9–10 kΩ [M].
- Beides passt zu einem **zweiten Pfad von ≈ 10 kΩ von J nach 0VA**: 22,1 kΩ ∥ 10 kΩ = 6,9 kΩ; plus 2,35 kΩ (0VA ↔ +5VA) = 9,2 kΩ [I]. Am 14.11. wurden von J zu den beiden Testpunkten am SOT-23-5 „exakt 10 kΩ“ gemessen [M]; ob diese Testpunkte auf 0VA liegen, ist nie geprüft worden.
- Bedeutung: Mit 22,1 kΩ allein lägen an J rechnerisch ≈ 7,4 V Spitze (325 V × 22,1/972), mit 6,9 kΩ nur ≈ 2,3 V. Ist der zweite Pfad kein Bauteil, sondern ein Kriechpfad (dunkle Stellen unter dem Lack liegen genau an J [O]), sieht der MCU nur rund ein Drittel der Netzspannung. Ist er ein Bauteil, fehlt er im Schaltplan.
- Das Netzsignal ist die einzige bisher gefundene Hochspannungsmessung am MCU (B18 geht an den L4981). Die Codes 04 (Überspannung) vom 08.11. und 10.11. können deshalb ebenfalls von hier stammen [H].

### B – Nicht verfolgte Konsolenkanäle OC02, OC03, OC08
- Drei Kanäle Konsole → MCU sind nicht zugeordnet; in Frage kommen Tacho, Wake-up (P2.15) und Sleep (P2.17) (`netlist/optokoppler_zuordnung.md`). OC08 ist optisch auffällig (`INSPECTION_2026-11-08.md`) [O].
- Laut Handbuch gibt die Konsole beim Einschalten des Bandes einen Wake-up-Impuls [Man]. Kommt er nicht an, bleibt die GIRT trotz PWM im Bereitzustand [H].
- Tacho-Kanal: siehe Lesart (b) in Abschnitt 1. Ein offener oder schwach abgeschlossener MCU-Eingang könnte beim Einsetzen der PWM Störimpulse sehen [H]. Dagegen spricht nichts Gemessenes, dafür auch nichts.

### C – Quelle von Y liegt vermutlich im Widerstandsfeld am TL082
- Im Bündel zum MCU laufen vier Bahnen: PFC-Sperre, X (über B20-R2) und zwei weitere aus dem Widerstandsfeld [O]. Kandidaten für Y (Arbeitsnummer 26): (1) **B20-R1b** – R1a liegt ebenfalls am Ausgang von Verstärker A [F], R1 wäre dann ein zweiter Abgriff des Netzsignals, z. B. für die Nulldurchgangserkennung; (2) der **Ausgang von Verstärker B** (Pin 7). Dessen Pin 5 liegt an 0VA [M], also vermutlich ein invertierender Verstärker für ein Shuntsignal mit R3 100 kΩ und R4 4,75 kΩ [I].
- Fall (1): Y bekäme ein Netzsignal; fehlt es oder erreicht es die Schaltschwelle nicht, wartet der MCU möglicherweise vergeblich auf einen Nulldurchgang (z. B. zum Schalten von F27) [H]. Fall (2): Liegt Y im Standby nicht nahe 0 V, sieht der MCU Strom ohne Antrieb [H].
- In beiden Fällen hängt das Signal an der Versorgung des TL082; ±12VA sind im Betrieb noch nie gemessen worden.

### D – Enable-Pegel am MCU nur indirekt belegt
- OC04 arbeitet als Emitterfolger auf 3,3 kΩ [M]. Für ≥ 4 V am MCU braucht der Koppler ≈ 1,2 mA Kollektorstrom. Gemessen ist nur die LED-Seite (LM2903 Pin 7 = 0,2 V). Ein Pegel zwischen 2 und 3,5 V wäre grenzwertig und könnte sowohl Fehlstarts als auch die err-9-Meldungen im Stand erklären [H].

### E – Kurze Schaltversuche
- Alle Messungen an T3-Steuerleitung, Basis T2 und F27 stammen vom Multimeter (träge, MAX-Erfassung ab ≈ 0,5 s). Ein Versuch von wenigen Millisekunden wäre unsichtbar. Durch den Oszi-Lauf O4 abgedeckt.

### F – Netzspannung und Nachbarbahnen
- Die Netzspannung an der Steckdose wurde nie notiert. Beide Code-04-Ereignisse lagen gegen 13:30 Uhr (nur zwei Datenpunkte).
- Die Isolationsprüfung benachbarter Bahnen im korrodierten Bündel an der Platinenkante (`HARDWARE.md` §9) ist seit dem 08.11. offen.

### G – MCU-Typ
- Aufdruck „11EBAA 109F200“ bzw. „109KZ00“ ist nicht zugeordnet. Mit dem Typ wären Pinfunktionen (ADC, Timer, Reset) bekannt. Ein Makrofoto mit Streiflicht könnte ein Herstellerlogo zeigen.

## 3. Prüfungen in sinnvoller Reihenfolge

| # | Bedingung | Prüfung | Bewertung |
|---|---|---|---|
| 1 | Start | Handyvideo mit Ton auf STS1/STS2 beim nächsten Startversuch; beim Einschalten auf ein mehrere Sekunden langes Brummen achten (in `img/led_timeline.png` für den 07.11. eingetragen) | STS1 blinkt weiter = GIRT geht nicht in „Lauf“; Zeit bis zum ersten STS2-Puls notieren |
| 2 | stromlos | J ↔ 0VA in beiden Polaritäten; beide Testpunkte am SOT-23-5 ↔ 0VA und ↔ +5VA | ≈ 22 kΩ = nur Fußwiderstand; ≈ 6,4–6,9 kΩ = zweiter Pfad, diesen suchen |
| 3 | stromlos | Y (LD3N-O) ↔ B20-R1b und ↔ TL082 Pin 7; Pin 6 ↔ R3/R4 | ≈ 0 Ω bzw. kleiner Serienwiderstand = Quelle von Y |
| 4 | stromlos | P4 TACHO, P2.9, P2.15, P2.17, P2.18 ↔ Anoden OC02/OC03/OC08; Emitter dieser Koppler → MCU-Pin | kleinster Wert = Zuordnung |
| 5 | Standby/Start, Konsolenseite | P2.15, P2.17, P2.18 gegen P2.7 (Multimeter, dann Oszi) | Pegelwechsel beim Start? |
| 6 | Standby, Netzseite | Oszi an TL082 Pin 1 bzw. X (Lauf O2): Spitzenwert und Form | ≈ 2,3 V oder ≈ 7,4 V (an X geklemmt); stark abweichend = Befund |
| 7 | Standby/Start | OC04 Pin 3 gegen 0VA | ≥ 4 V unkritisch; 2–3,5 V grenzwertig |
| 8 | Standby | +12VA, −12VA gegen 0VA; Y gegen 0VA (Multimeter, dann Oszi) | ±12 V; Y je nach Ergebnis von 3 bewerten |
| 9 | Start | Oszi SINGLE an Steuerleitung T3 und Basis T4 (Lauf O4) | kurzer Schaltversuch ja/nein |
| 10 | Start | nach 4: Tacho-Kanal am MCU mit dem Oszi bei stehendem Band | Impulse ohne Bandbewegung = Befund |
| 11 | jeder Versuch | Netzspannung AC an der Steckdose notieren | Zusammenhang mit Fehlern? |
| 12 | – | Makrofoto MCU-Aufdruck mit Streiflicht | Typ |

## 4. Abgleich mit dem Schaltplan
- **Widerspruch:** J ↔ 0VA (Abschnitt 2 A). Bis zur Klärung nicht ändern.
- Nicht im Schaltplan enthalten und für die Fehlersuche wichtig: Tacho-Kanal zum MCU, OC02/OC03/OC08, Quelle von Y, Quelle der T2-Ansteuerung, Funktion des SOT-23-5.

## 5. Korrektur
- OC05 (14.11. 13:41): gemessen wurde Kollektor gegen Emitter (4,95 → 4,5 → 4,3 V). Der Emitter (= MCU-Eingang) steigt also im Mittel von ≈ 0 auf ≈ 0,45–0,65 V; das Signal ist **nicht invertiert**. Eine anderslautende Bemerkung im Dialog vom 16.11. morgens war falsch.
