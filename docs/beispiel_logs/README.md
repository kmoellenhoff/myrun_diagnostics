# Beispiel-Logs

Drei ausgewählte Aufzeichnungen, damit man die Ausgabeformate der Skripte und das Fehlerbild kennt. Alle übrigen Rohlogs liegen im Archiv-Branch `archiv-vor-aufraeumen-2026-11-27`.

| Datei | Skript | Zeigt |
|---|---|---|
| `myrun_fast_monitor_20261111_150758.txt` / `.csv` | `myrun_fast_monitor.py` (aktiv) | **Fehlstart vor der Reparatur** (11.11.2026): START, Zustandswechsel `QSRunning -> QSHardwareFault`, Encoder 0 Hz, Fehlerspeicher mit HF904/HF902 (`@RERRORLOG#`). Zeitstempel in der CSV: Ortszeit und UTC. |
| `myrun_fast_monitor_20261123_212407.txt` / `.csv` | `myrun_fast_monitor.py` (aktiv) | **Guter Lauf nach der Reparatur** (23.11.2026, C602 ersetzt): Anlauf und Geschwindigkeitsstufen 2,0 / 2,5 / 2,9 km/h per FTMS, kein Zustandswechsel nach `QSHardwareFault`, Fehlerspeicher am Ende unverändert (die Einträge vom 19.–21.11. stammen aus der Zeit vor dem Einbau). |
| `myrun_dump_20261124.txt` | `myrun_dump.py` | **Diagnose-Dump** (24.11.2026): Firmware, Fehlerspeicher, `@STATUS#`, `@RADCEXT#`, `@DUMPIO#`. |

CSV-Spalten des Fast-Monitors: `t_rel_s, wallclock, utc, signal, value`.

Die Gerätezeit im Fehlerspeicher entspricht etwa UTC (im Winter 1 h hinter der Ortszeit). Die Logs enthalten Gerätename/BLE-Adresse des Laufbands, aber keine Benutzer- oder Pfadangaben.
