**Pausenstand 09.11.2026:** [Q2-C / R2211 / 1P: neue Netzzuordnungen und vorläufiger NPN-Ableitzweig](../messplan_stromlos_2026-11-08/Q2_C_1P_NACHTRAG_2026-11-09.md). Lüfter läuft auch beim Fehlstart an. Positive Treiberversorgung weiter offen; Diodentest am 1P-Bauteil auf später verschoben.

**Weiterer Nachtrag 09.11.2026:** [FAN3100C als gut passender Kandidat, bedingter Pinabgleich](q2_treiber_fan3100c_kandidat.md). Kurzcode 100C plus Datumscode und gemessene Anschlüsse B/E passen; Typ noch nicht abschließend gesichert.

**Nachtrag 09.11.2026:** [Aktueller Messblock Q2/Treiber 05/05b](../messplan_stromlos_2026-11-08/Q2_TREIBER_ERGEBNISSE_2026-11-09.md) hat Vorrang vor den folgenden historischen Erwartungen: B=0VA, E–RG-U ≈0 Ω bestätigt; Gatepfad 22,2 Ω, G–S 9,14 kΩ beidseitig, G–D 2,2 MΩ / rückwärts 1,86 MΩ langsam steigend (kein Endwert). Der Umfeldwiderstand trägt **2211 = 2,21 kΩ**, nicht 221/220 Ω. R1001 979/977 Ω, R2211 2,09 kΩ beidseitig, R4752 4,16 kΩ beidseitig. Aufdruck des Fünfbeiners laut Nutzer **1000CA**, Typ/Funktionspinout weiter offen. Folgender Text bleibt als Historie erhalten.

# Q2 (Motor-MOSFET, low-side) – Lage und Pinbelegung

Stand 2026-11-08 21:35, aus Fotos und Diodentests. Status: Lage [P/I], Pinbelegung G/D/S [I] (Standardpinout + Gate-Bahn), Messung offen.

**Lage:** Feld **B5** (Vorder- und Rückseite, ± 0,5 Feld), an den Kühlkörper geklemmt, Vorderseite direkt neben P600 (F15) und über den vier R020-Shunts; Übersichts-IDs F33 (vorn), B21 (hinten).
Fotos: `img/q2_vorderseite_GDS.jpg`, `img/q2_rueckseite_GDS.jpg`.

| Pin | Vorderseite (Foto, Beine unten, Tab zum Kühlkörper) | Rückseite (Foto, Beinreihe unten) | Funktion | Beleg |
|---|---|---|---|---|
| G | linkes Bein (neben P600) | **linkes Pad**, dünne Bahn nach oben zu Pad → 22-Ω-Widerstand ("220") → Treiber SOT-23-5 | Gate | Standard G-D-S; Bahn zum Gate-Widerstand |
| D | mittleres Bein | mittleres Pad | Drain = DC MOTOR L− | Diodentest 0VA→L− 0,444 V (Body-Diode) |
| S | rechtes Bein | rechtes Pad | Source = 0VA | s. o. |

Zwischen den Pads liegen zwei Isolierschlitze (Kriechstrecke G | D | S).
Beide Fotos sind relativ zur Übersicht um 180° gedreht: „links im Foto“ = grösserer x-Wert (Spalte B, rechte Hälfte). In der aufrechten Rückseiten-Übersicht (Variante B) liegt das Gate-Pad daher **rechts** von den drei Pads.

Treiber: 5-poliger SOT-23 oberhalb des Gate-Widerstands, Aufdruck nicht lesbar (nur "…0…A…1"): Typ offen.

## Messvorschlag (stromlos, Elko < 5 V, rot zuerst)
1. G ↔ Pad am 22-Ω-Widerstand (Bahn, ohne Auslöten): ≈ 0 Ω.
2. G ↔ 22-Ω-Widerstand zweites Ende: ≈ 22 Ω.
3. G ↔ S (0VA): Gate-Pulldown, erwartet einige 10 kΩ bis einige 100 kΩ; kleiner als 1 kΩ oder < 0,1 V im Diodentest wäre ein Fehler.
4. G ↔ D (L−): hochohmig/OL.
5. Diodentest rot S, schwarz D: ≈ 0,44 V (wie PW-M02), Gegenrichtung OL.

## Ergebnis 21:39 (messprotokoll_leistungsteil.csv PW-M03…M06)
G↔D 2,19 MΩ, G↔S 9,13 kΩ (beide Richtungen), Gate-Widerstand und Diodenstrecke wie erwartet.
→ Q2 statisch unauffällig (kein Gate-Schaden, kein D-S-Schluss), Gate-Pulldown ≈ 9,1k, Gate-Pfad bis zum 22-Ω-Widerstand intakt.
Offen: ob der Treiber (SOT-23-5) beim Fehlstart überhaupt schaltet (nur live prüfbar), und seine Versorgung/Ansteuerung.
