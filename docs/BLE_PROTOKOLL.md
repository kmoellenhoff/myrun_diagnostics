# BLE-Protokoll des Technogym MYRUN

Beobachtungen am untersuchten Gerät (Firmware `WFW0699_BA30.35167`). Andere Hardwarestände oder Firmwareversionen können sich anders verhalten. Die Angaben stammen aus dem Code der Skripte im Repository, aus dem Vergleich mit der Open-Source-Implementierung qdomyos-zwift und aus Beobachtungen am Gerät; sie sind keine Herstellerdokumentation. Bedienung der Programme: [SKRIPTE.md](SKRIPTE.md).

## 1. Dienste und Characteristics

```text
Technogym-Dienst (proprietär):
beb7705e-bd66-4501-80c0-0c8f0bcca1a5

Technogym Schreib-Characteristic (Befehle):
df1eb8e4-1753-4bb9-a6a6-e018040af0a3

Technogym Notify-Characteristic (Antworten):
6f26de4b-dcef-4459-9465-931f1b144c20

FTMS Control Point (Standard, 0x2AD9):
00002ad9-0000-1000-8000-00805f9b34fb
```

Weitere Notifications, die das Gerät sendet und der Fast-Monitor mitschreibt: FTMS Treadmill Data (0x2ACD), Fitness Machine Status (0x2ADA), Training Status (0x2AD3) und RSC Measurement (0x2A53).

Die Skripte schreiben ausschließlich auf die Technogym-Schreib-Characteristic und den FTMS Control Point. In den unbekannten Dienst `6e40a8d5-b5a3-f393-e0a9-e50e24dcca9e` wird nie geschrieben.

Der FTMS Control Point verlangt ein aktives Indication-Abo, bevor geschrieben wird; sonst meldet BlueZ `CCCD_IMPROPERLY_CONFIGURED`. Die Skripte abonnieren deshalb den Control Point vor dem ersten Schreiben.

## 2. Initialisierung

Der Ablauf entspricht dem Verhalten der qdomyos-zwift-MYRUN-Implementierung:

1. Notifications auf der Technogym-Notify-Characteristic und dem FTMS Control Point abonnieren.
2. FTMS-Init auf den Control Point schreiben (mit Antwort):

```text
00 93 F0 51 E8 1B 42 92 8E
```

3. Rund 0,8 s warten, dann die Setup-Befehle auf dem Textkanal senden:

```text
@DISABLE_PACE#
@SSIUNITS#
@RJSK_EN 1#
@LJSK_EN 1#
```

Das Setup ist keine reine Abfrage. `@SETDATE#` wird bewusst nicht gesendet, weil es die Zeitstempel im Fehlerspeicher verfälschen würde.

Die rein passiven Betriebsarten (`--listen-only`, `--listen-poll`, `myrun_renc_watch.py`) senden weder FTMS-Init noch Setup und fragen nur Lesebefehle ab; ob alle Lesebefehle ohne Init antworten, ist nicht für jeden Befehl bestätigt (das Skript warnt, wenn die Antwort ausbleibt).

## 3. Textkanal: Befehlsformat

- **Befehle** haben die Form `@NAME#` oder `@NAME PARAMETER#`, zum Beispiel `@STATUS#`, `@RJSK_EN 1#`.
- Sie werden **Byte für Byte** (je ein ASCII-Zeichen pro GATT-Write) auf die Schreib-Characteristic geschickt, mit etwa **0,04 s Pause** zwischen den Bytes. Kürzere Pausen sind nur mit Vergleich zu empfehlen.
- **Antworten** kommen auf der Notify-Characteristic, häufig ebenfalls in sehr kleinen Stücken bis hin zu einem Byte je Notification. Sie beginnen mit `!` und enden mit `#` (`!…#`). Der Empfänger setzt die Stücke zusammen, bis `#` erscheint.
- Unbekannte Befehle werden mit `!BEFEHL:ERROR` beantwortet, **ohne** abschließendes `#`. Der Empfänger muss ein Ende auf `:ERROR` ebenfalls als vollständige Antwort behandeln, sonst läuft er in den Timeout.
- Antworten sind mehrzeiliger ASCII-Text (Zeilenende `\r\n` möglich); innere Leerzeichen und Tabulatoren trennen Felder und sollten nicht entfernt werden.
- Es wird ein Befehl nach dem anderen gesendet; vor jedem Befehl sollte der Empfangspuffer geleert werden.

## 4. Bekannte Befehle

Aus `myrun_probe.py` und `myrun_dump.py`; die Spalte „Antwort“ nennt nur, was die Skripte auswerten. Die Befehle der Gruppe „dokumentiert“ stehen im Servicehandbuch (Rev. 2.2, Kap. 6.1.2); `@RPWM#` und `@RADC#` sind dort nicht beschrieben, antworten aber auf der untersuchten Firmware.

| Befehl | Zweck | Antwort / ausgewertete Felder |
|---|---|---|
| `@FWVER#` | Firmware-Version | Text mit Version |
| `@RERRORLOG#` | Fehlerspeicher | Liste der gespeicherten Fehler |
| `@STATUS#` | Gerätezustand | u. a. `Status: QS…` (z. B. `QSWaitForStart`, `QSWaitForStartRC`, `QSRunningRC`, `QSHardwareFault`, `QSStopping`, `QSStoppingRC`), `MeasSpeed: …`, Sollwerte |
| `@DUMPIO#` | Digital-I/O und PWM-Rohwerte | Zeilen `OUT`/`IN`/`PWM <NAME> = <Zahl>`, z. B. `EM_POWENA`, `LK_ENABLE`, `PWM_MOTOR` |
| `@RENC#` | Encoder | `… Hz -> … km/h` (Encoderfrequenz und Geschwindigkeit) |
| `@RPWM#` | PWM-Tastgrad (undokumentiert) | `PWM=…%` |
| `@RADC#` | Steigungs-ADC kurz (undokumentiert) | Rohwert |
| `@RADCEXT#` | Steigungs-ADC erweitert | Rohwerte |
| `@RKPWM#` | Kalibriertabelle Geschwindigkeit/PWM | Tabelle |
| `@RQSPAR#` | Quick-Start-Parameter | Parameter |
| `@RSTAT#` | Nutzungsdaten (Zeiten, Kilometer) | Zähler |
| `@RTASKHANG#` | Zuletzt blockierte Task | Text |
| `@RRUNDETMINSP#` | Mindestgeschwindigkeit der Läufererkennung | Wert |
| `@GETDATE#` | Datum/Uhrzeit des Geräts | Text |
| `@RTG_ID#` | BT-Seriennummer | Kennung |
| `@RDS_UP#`, `@RDS_DOWN#` | Gerätesensoren oben/unten | Zustand |
| `@DISABLE_PACE#`, `@SSIUNITS#`, `@RJSK_EN 1#`, `@LJSK_EN 1#` | Setup (Abschnitt 2), schreibend | Quittung |

**Namenskonvention:** Lesebefehle beginnen mit `@R…`, Setzen mit `@S…`. Das ist eine Beobachtung, keine Zusicherung. Der Probe-Modus sperrt daher Befehle mit `RESET`, `^@S` (außer `@STATUS#`), `SET`, `INIT`, `CAL`, `ELEV`, `FORCE`, `SUSPEND`, `STG_ID`, `WRITE`, `ERASE`, `CLEAR`, `FORMAT`, `UPD`, `BOOT`, `FLASH`. Das beweist die Harmlosigkeit eines unbekannten Befehls nicht.

**Nicht verfügbar:** Auf der untersuchten Firmware gibt es über BLE **keine Temperatur-, Busspannungs- oder Stromwerte**. Die vermuteten Befehle (`@RTEMP#`, `@RVBUS#`, `@RVDC#`, `@RIMOT#`, …) blieben ohne Antwort (Timeout). Temperatur und Spannungen sind nur durch Messung am Gerät zugänglich.

## 5. FTMS Control Point

Es gilt der Standard der Fitness Machine Service. Verwendet werden:

```text
0x07                  START / RESUME
0x02 LL HH            SET TARGET SPEED        (uint16, Einheit 0,01 km/h)
0x03 LL HH            SET TARGET INCLINATION  (sint16, Einheit 0,1 %)
0x08 0x01             STOP / PAUSE
```

Beispiele: 2,0 % ist `03 14 00`; 2,5 km/h ist `02 FA 00`.

Antworten kommen als Indication im Format `80 <Opcode> <Ergebnis>`:

```text
80 03 01    Zielneigung: SUCCESS
80 03 04    Zielneigung: OPERATION_FAILED
```

Ergebnisse: `01` SUCCESS, `02` NOT_SUPPORTED, `03` INVALID_PARAMETER, `04` OPERATION_FAILED, `05` CONTROL_NOT_PERMITTED.

### Verhalten

- **START ohne Geschwindigkeitsbefehl** lässt das Band am untersuchten Gerät mit etwa **1,2 km/h** anlaufen. Der Wert ist eine Firmware-Voreinstellung.
- **STOP kann fehlschlagen.** Ein Gerät in einem Hardwarefehlerzustand kann STOP ablehnen (beobachtet: `80 08 04`, `OPERATION_FAILED`). Ein Software-STOP ersetzt nie den physischen Stopp.
- Ein ACK bestätigt den Befehl, nicht die mechanische Bewegung.
- **Treadmill Data (0x2ACD)** ist auf `WFW0699_BA30.35167` keine zuverlässige Geschwindigkeitsmessung: das Geschwindigkeitsfeld ist der **Sollwert**; es meldete im Zustand `QSHardwareFault` bei stehendem Band weiter 1,2 km/h. Für die tatsächliche Geschwindigkeit dienen `@RENC#` (Encoder) oder `MeasSpeed` in `@STATUS#`.
- Das Neigungsfeld in 0x2ACD und ein positiv quittierter Neigungsbefehl sind kein Nachweis tatsächlicher Höhenbewegung.

## 6. Technisches Servicehandbuch und Abgleich

Ein öffentlich gehostetes **MYRUN TECHNOGYM Technical Service Manual**, Revision **2.2 (November 2016)**, **französisch, 112 Seiten**, ist als externes PDF verfügbar:

- [MYRUN-Servicehandbuch (PDF, manuals.plus)](https://manuals.plus/m/077b22630fbae70ec842c1934cbd88c864a0677a4bc4fdc5807af41d91ae321d.pdf)

Nützliche gedruckte Seiten (Anschlussbelegung und Platinen-LEDs sind bei späterer Hardware nicht zwingend gleich):

| Seiten (gedruckt) | Thema |
|---|---|
| 18–20 | Elektrische Verdrahtung, 220-V-Version |
| 40–43 | Lower Drive Kit, Diagnose-LEDs, gemeinsames RELAY ENABLED für Band und Steigung |
| 44–47 | DC-Laufbandmotor, PWM-Eingang, Drehzahlrückführung, optischer Encoder |
| 48–51 | AC-Steigungsmotor über zwei Relais, Potentiometer-Rückführung |
| 52–54 | Not-Aus-Verriegelungen, thermischer Motorschutz |
| 64–70 | ASCII-Diagnosebefehle, u. a. `@STATUS#`, `@DUMPIO#`, Fehlerspeicher |
| 85–88 | Fehlercodes, Fehlersuche HF900 (Geschwindigkeitsrückführung) |
| 89–91 | Fehlersuche Steigung |
| 95 | Kapitel Demontage enthält **keine Ausbauschritte**, verweist auf Technogym-Schulung |

**Revisionshinweis:** Das Handbuch von 2016 zeigt ein älteres Lower-Controller-Design. Das untersuchte Gerät hat einen **Gefran GIRT S6T30** (Teil S0WR01179AG) mit Firmware `WFW0699_BA30.35167`. Lage von D21/D50/D24, Steckerbelegung (CN J3), Bauteillayout und angegebene Spannungen dürfen **nicht ungeprüft** auf diesen Controller übertragen werden.

Fehlercodes im Handbuch von 2016:

- **HF500–505:** Fehler des Lower Drive Kits.
- **HF600:** Fehler Steigungsmotor.
- **HF900:** Geschwindigkeitssignal/Rückführung; abgenutzte Motorbürsten werden als Möglichkeit genannt.
- **HF901 und HF904:** in dieser Ausgabe **nicht definiert**. Die Deutung von HF901 als „Inverter-Fehler“ ist durch das Handbuch **nicht belegt**.

## 7. Hintergrund und Quellen

Die BLE-Initialisierung und das FTMS-Verhalten wurden zum Teil durch Einsicht in die Open-Source-Implementierung **qdomyos-zwift (QZ)** für das Technogym MYRUN abgeleitet:

- https://github.com/cagnulein/qdomyos-zwift

Dieses Repository ist ein gezieltes Diagnosewerkzeug und kein Ersatz für QZ. Es ist unabhängig von Technogym; die BLE-Initialisierung wurde teils aus dem GPL-3.0-lizenzierten qdomyos-zwift-Projekt abgeleitet, enthält aber eine eigene Python-Implementierung. Getestet wurde an einem Technogym MYRUN der DCKA-Serie mit Firmware `WFW0699_BA30.35167`.
