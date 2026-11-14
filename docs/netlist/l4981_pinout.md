# L4981AD (PFC-Controller, SO-20) – Pinbelegung laut Datenblatt

Quelle: ST/SGS-Thomson Datenblatt L4981A/L4981B. Pin 1 = Punkt; Pins 1–10 oben (rechts → links), 11–20 unten (links → rechts), siehe `../img/l4981_messpins_pfc.jpg`.
Erwartung stromlos = typische Beschaltung, auf dieser Platine **nicht** gemessen, sofern nicht vermerkt.

| Pin | Name | Funktion | Typische Beschaltung | Erwartung stromlos gegen S-GND |
|---|---|---|---|---|
| 1 | P-GND | Leistungsmasse (Gate-Treiber) | an 0VA | ≈ 0 Ω |
| 2 | IPK | Spitzenstrombegrenzung | Widerstand zum Shunt (A-Version) | wenige 100 Ω (gemessen 11.11.: 580 Ω zu den Shunts) |
| 3 | OVP | Überspannungsschutz, Schwelle 5,1 V | Teiler vom Zwischenkreis | einige 10 kΩ |
| 4 | IAC | Eingangsstrom für Multiplizierer (Netzform) | großer Widerstand vom gleichgerichteten Netz | hoch (100 kΩ … MΩ) |
| 5 | CA-OUT | Ausgang Stromverstärker | RC-Netz zu Pin 9 | mittel/hoch |
| 6 | LFF | Lastvorsteuerung | Teiler/Kondensator | mittel/hoch |
| 7 | VRMS | Netzspannung (Effektivwert-Eingang) | Teiler mit Filterkondensatoren | Wert steigt (Kondensator) |
| 8 | MULT-OUT | Multipliziererausgang | Widerstand zum Shunt | wenige 100 Ω … kΩ |
| 9 | I_SENSE | Eingang Stromverstärker | Widerstand zum Shunt | (gemessen 11.11.: 10 kΩ) |
| 10 | S-GND | Signalmasse | an 0VA | ≈ 0 Ω |
| 11 | V_REF | Referenzausgang 5,1 V | Kondensator nach Masse | Wert steigt |
| 12 | SS | Soft-Start | Kondensator nach Masse (intern 100 µA Ladestrom; bei OVP/UVLO intern entladen) | Wert steigt; **≈ 0 Ω = festgehalten** |
| 13 | VA-OUT | Ausgang Spannungsregler | RC-Netz zu Pin 14 | mittel/hoch |
| 14 | VFEED | Rückführung Zwischenkreisspannung | Teiler vom Zwischenkreis | einige 10 kΩ |
| 15 | P-UVLO | programmierbare VCC-Einschaltschwelle | Teiler VCC/Masse (ohne: 15,5 V ein / 10 V aus) | kΩ … 100 kΩ |
| 16 | SYNC (A) / FREQ-MOD (B) | Synchronisation bzw. Frequenzmodulation | oft offen oder Widerstand | hoch |
| 17 | R_OSC | Oszillator-Ladestrom | Widerstand nach Masse | einige 10 kΩ |
| 18 | C_OSC | Schaltfrequenz | Kondensator nach Masse | Wert steigt |
| 19 | V_CC | Versorgung | = VDD Gate-Treiber (gemessen 13,5 V; 1,45 kΩ gegen Masse) | ≈ 1,45 kΩ |
| 20 | GDRV | Gate-Ausgang zum PFC-MOSFET | Gate-Widerstand, Ableitwiderstand | kΩ-Bereich |

**Betrieb:** Die PFC taktet nur, wenn VCC die Einschaltschwelle überschreitet (Pin 15) und SS (Pin 12) hochläuft; OVP (Pin 3) > 5,1 V schaltet ab. Ein eigener Enable-Pin existiert nicht.
