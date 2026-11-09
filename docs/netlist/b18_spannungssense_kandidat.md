# B18/B19 – Spannungsrückführung zum L4981AD

**Maßgeblicher Stand: 09.11.2026.** Claudes Raster bleibt B18 E5, B19/B20 E6. M = gemessen, F = sichtbare Bahn, I = Code/Hersteller-Pinout, H = Hypothese. Historische Rohmessungen bleiben erhalten; Abschnitt 6 enthält verworfene Annahmen.

## 1. Maßgebliche Schaltung

```text
DC MOTOR L+ = B18-P2 [M, 0 Ω]
  → R3 1 MΩ (1004) → V1/TP1 → R2 1 MΩ (1004)
  → R1 475 kΩ (4753) → P1 [F]
  → E1 [M, 0,4 Ω] → 1003 rechts / 100 kΩ → E2 = Pad A [M]
  → 1003 links / 100 kΩ → Pad B [F + Endkappenverbindungen M]
  → 3922 / 39,2 kΩ → 0VA [F + Endkappe–0VA M]

Pad B → L4981AD Pin 14 VFEED [M, 0 Ω; Funktion Hersteller-Pinout]
0VA → 4750 / 475 Ω → Pad C [F]; C-Weiterweg offen
B19: zwei zusätzliche 1004 / 1 MΩ parallel [M]; Einbindung offen
```

Nominales unbelastetes Modell an B: R_oben 2,675 MΩ, R_unten 39,2 kΩ, Verhältnis 1,444 %. 5,1 V am Abgriff entsprächen rechnerisch 353,1 V am Eingang; kein gemessener Betriebswert und kein bestätigter realer Sollwert. Eingangsbeschaltung, Referenzbezug und Dynamik sind nicht vollständig geprüft. Die Funktion Spannungsrückführung zum PFC-Regler ist durch die Verbindung zu VFEED identifiziert. Ein Fehler in diesem Netz ist damit nicht bewiesen.

## 2. Lage und Bauteil-IDs

Originale B18-IDs und TP1/TP2 bleiben unverändert. TP1/TP2 sind Testpads, keine Vias; TP2 liegt am R3/P2-Netz. B19-Rin bezeichnet weiterhin E1–E2, jetzt korrekt **1003 = 100 kΩ**. E1/E2 behalten die Originalpixel des Messplans. A/B/C sind nur lokale B19-Padnamen in der neuen Nutzerfoto-Orientierung (IC links, 1003 oben), keine Rasterkoordinaten.

| Teil | Aufdruck / Nennwert | Nachweis |
|---|---|---|
| B18-R1 | 4753 / 475 kΩ | I, historische In-Circuit-Messung |
| B18-R2 und R3 | 1004 / je 1 MΩ | I, historische In-Circuit-Messung |
| B19-Rin (E1–E2) | 1003 / 100 kΩ | I; 97,6 kΩ, wiederholt 102,6/90,4 kΩ M |
| B19-1003 links | 1003 / 100 kΩ | I; 102,6/90,4 kΩ M |
| B19-3922 | 3922 / 39,2 kΩ | I; 38,43/38,91 kΩ M |
| B19-4750 | 4750 / 475 Ω | I; 478 Ω beide Richtungen M |
| B19-1004-Paar | je 1 MΩ, parallel nominal 500 kΩ | I und Verbindungen M; 498/496 kΩ M |
| B3, SO20 | ST L4981AD | neues Nutzer-Originalmakro; Pin 14 VFEED laut ST-Datenblatt |

[Alle Messungen, Paddefinitionen und Grenzen vom 09.11.](../messplan_stromlos_2026-11-08/B19_ERGEBNISSE_2026-11-09.md). [ST L4981-Datenblatt](https://www.st.com/resource/en/datasheet/l4981.pdf). B20 bleibt eine Reihe aus vier Widerständen und SOT-23, Werte/Funktionen offen.

## 3. Messwerte (alle in-circuit, stromlos; Rohdaten: `messprotokoll_b18.csv`)

| Mess-ID | Messung (rot zuerst) | Wert | Gegenrichtung |
|---|---|---|---|
| B18-M01 | R1 (Ende Richtung B19) | 378 kΩ | 406 kΩ |
| B18-M02 | R2 | 600 kΩ | 840 kΩ |
| B18-M03 | R3 | wie R2 | wie R2 |
| B18-M04 | gesamte Kette P1↔P2 | 170 kΩ steigend | 619 kΩ steigend |
| B18-M05 | P1↔0VA | 223,7 kΩ konstant | |
| B18-M06 | P1↔+5VA | 226,4 kΩ konstant | |
| B18-M07 | P2↔0VA | 6 MΩ fallend (nicht eingeschwungen) | |
| B18-M08 | P2↔DC MOTOR L+ | **0 Ω** | |
| B18-M09 | P2↔DC MOTOR L− | 300 kΩ steigend | |
| B18-M10 | V1↔0VA | 1,211 MΩ | |
| B18-M11 | V1↔+5VA | 1,206 MΩ | |

Historische Modellrechnung vom 08.11.: Die damaligen niedrigeren In-Circuit-Werte wurden durch Parallelpfade modelliert. Daraus folgen weder isolierte Bauteilwerte noch ein nachgewiesener physischer 221-kΩ-Widerstand. Der aktuelle Verlauf und die Ergebnisse vom 09.11. stehen im verlinkten B19-Bericht.

## 4. Zusammenhang Leistungsstufe (messprotokoll_leistungsteil.csv, `q2_zuordnung.md`)

L+ = DC-Bus (nach Drossel), L− = Q2-Drain (Low-Side), 0VA = Source/DC−. D3 (L−→L+ 0,397 V) und Body-Diode Q2 (0VA→L− 0,444 V) statisch unauffällig; Q2-Gate-Netz (G–S 9,13k, G–D 2,19M) unauffällig. Aussagen gelten für diesen Messzeitpunkt; **intermittierende Fehler sind damit nicht ausgeschlossen.**

## 5. Offene Punkte

- Blatt 04: [B20-Messungen vom 09.11.](../messplan_stromlos_2026-11-08/B20_ERGEBNISSE_2026-11-09.md) abgeschlossen im geprüften Umfang; Tb = 0VA bestätigt. Typ, R4-Code und vollständige Netzfunktion bleiben offen. Nächstes Blatt 05: Q2-Treiber.
- P2–0VA: neuer Verlauf steigend bis 6 MΩ, dann fallend; Endwert und Gegenrichtung fehlen.
- B19-1004-Parallelnetz: Einbindung der gemeinsamen Enden offen; Pad C: weitere Funktion offen.
- OVP-Pin 3 und Signal-/Leistungsmasse des L4981AD nicht separat verfolgt; +5VA nicht als VREF annehmen.
- Leitfähige Verschmutzung an Pins/Pads ist möglich, aber durch Fotos und Messwerte nicht bewiesen. Vergleich vor/nach geeigneter Reinigung bei gleicher Polung, Temperatur und Ablesezeit wäre aussagekräftig.
- P2–L−-Ladeverlauf, dynamische Versorgung und tatsächliches Verhalten beim Fehlstart bleiben ungeklärt. Stromlose Werte geben keine Betriebsfreigabe.

## 6. Historie (überholt – nicht für Messungen verwenden)

- 21:10: Interpretation „geschlossener Ring, P1/P2 niederohmig verbunden (ext ≲ 50k)“ → durch M04 korrigiert (ext ≈ 100–200k, Vorwärtsrichtung).
- 21:17: Hypothese „**P2 = L−** (Schaltknoten/Drain von Q2)“ und „Body-Diodentest 0VA→P2“ → **widerlegt** durch M08 (P2↔L+ = 0 Ω).
- 21:17: Übereinstimmung „J1→L− = 2,6 MΩ ≈ Kette + 221k“ → Zufall, ungeklärt; kein Zusammenhang mit der Kette.
- Anfangsbezeichnung „V1/V2 = Via/Ebenenwechsel“ → falsch; es sind einfache Messpunkte (TP1/TP2).
- Anfangslage „F6“ → korrigiert auf E5.
- Frühere Beschreibung von B20 als „Spalte aus vier Widerständen“ → es ist eine Reihe.

- 09.11.: B19-Code `1001 / 1 kΩ` korrigiert zu **1003 / 100 kΩ**. MCU-/Komparator-Zielhypothese durch gemessene Verbindung zu **L4981AD Pin 14 VFEED** ersetzt. Historische ≈221-kΩ-Modellgröße bleibt kein identifizierter Einzelwiderstand.
