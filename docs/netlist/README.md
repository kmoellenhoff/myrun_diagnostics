# Netlist workspace (draft)
Files: `parts.csv` (IDs, orientation), `messprotokoll_v0_chatgpt.csv` (measurements to date, as compiled by the second AI), image `../img/optocoupler_pads.png` (pad roles OC01–OC08). Pad IDs: `OC03.4` = optocoupler OC03, pin 4. Board grid: see `../GIRT_Platinen_Uebersicht_Entwurf.pdf`. Only measured or photo-verified connections go into a net table; everything else stays hypothesis.

## Status scheme
Every connection has: **Art** (copper direct / via component / via) and **Status** (Foto, Messung, Datenblatt, Hypothese). Only `Messung` or `Foto` of a visible copper track counts as established; component values read from codes stay `Hypothese` until measured. Sub-ID scheme: `<Gruppe>-<Teil><Nr>.<Anschluss>` (e.g. `B10-R2.1`), pads `<Gruppe>-T/N/J/X<Nr>`.
Front/back alignment check (11/08): five mounting-hole pairs match within ≈0.1–0.4 grid cells (the back image is flipped vertically). Not yet a homography fit.
