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
