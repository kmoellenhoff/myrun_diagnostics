R,G,O,N='#d40000','#2e8b2e','#e69500','#444'
BG={'R':'#fdeaea','G':'#e8f5e8','O':'#fff6e0','N':'#f4f4f4'}
BC={'R':R,'G':G,'O':O,'N':N}
boxes=[]
def box(x,y,w,h,t,sub='',st='N',num=None,dash=False,extra=''):
    boxes.append((x,y,w,h,t,sub,st,num,dash,extra))
box(28,155,115,150,'AC LINE','230 V')
box(170,155,200,150,'EMV-Filter','3 Drosseln, X2 1 µF<br>Varistoren RV300/301')
box(403,155,228,150,'Einschaltbegrenzung','68 Ω/7 W, RT334024 (24 V)<br>+ ALQ3F12 (12 V)<br><small>Freilaufdioden an Spulen</small>','R',3)
box(665,155,185,150,'Gleichrichter + PFC','Brücke, Ringkern, Q1, D2<br>4× R020 (Rückseite)<br><small style="color:#d40000">Lötstellen korrodiert</small>','R',2)
box(885,155,170,150,'Zwischenkreis','560 µF EPCOS<br>ca. 300–380 V DC<br><small>L+ = DC-Bus (nach Drossel)</small>','O',None,True)
box(1090,155,200,150,'Chopper (low-side)','Q2 (B5) + D3, 4× R020<br><small>Dioden/Gate-Netz statisch OK [M]<br>Schalten live ungeprüft</small>','G',4)
box(1323,155,130,150,'DC MOTOR','L+ orange<br>L− grau','R',5)
box(1487,155,185,150,'Bandmotor','1,5 Ω, Generator OK<br>Thermoschalter<br>0 Ω (kalt) OK','G')
box(403,385,228,100,'UP/DOWN-Relais','Schrack PE + 2× ALQ3F12<br><span style="color:#d40000">Stecker-Pads korrodiert</span>','R',6)
box(665,385,185,100,'FUSE MOT','<span style="color:#d40000">FEHLT (T 4 A, 5×20)</span>','R',None,True)
box(885,385,285,100,'Höhenmotor AC','70/71/141 Ω, 6,25 µF<br>Poti an P3 (korrodiert)')
box(1200,365,335,125,'Busspannungs-Teiler (B18, E5)','L+ (=P2, 0 Ω) → 475k+1M+1M → P1<br>P1 ≈ 221k gegen 0VA (≈ 8 %)<br>→ Block B19 → Auswertung<br><small>Hypothese, 6 Messwerte passen [H]</small>','O',None,True)
box(28,500,340,100,'Netzerfassung (B10, J6)','L/N → 2×475k → Diode → Knoten J<br>J ≈ 6,8k gegen 0VA<br><small>Nulldurchgang/Netz da, gemessen gesund [M]</small>','G')
box(403,610,228,112,'Hilfsnetzteil','Flyback FSGM300N<br>läuft (Konsole an)','G')
box(665,610,242,112,'Hilfsspannungen','+12 V für Konsole (≤2,5 A)<br>+24 V, ±12 V, +5 V','G')
box(940,610,285,130,'8× Optokoppler → MCU QFP-32','0VA/+5VA · TL082 · LM2903<br>PWM → SOT-23-5 → 22 Ω → Gate Q2','N')
box(1417,610,255,112,'P4 Tacho','+12 V / 0 V / TACHO<br>Sensorplatine, 72-Loch-Scheibe')
box(940,800,285,128,'P2 (18-pol.) zur Konsole','PWM, Notlinie (Pin 5, vermutet)<br>Tacho, Up/Down, Poti, +12 V<br><span style="color:#d40000">Salzkruste zwischen Pins</span>','R',1)
box(940,1005,285,100,'Konsole (CPU)','EM_POWENA → 5-V-Notlinie<br>liest LOWKITENA/B, LK_ENABLE')
box(1317,992,355,112,'Notlinie über Motor-Thermoschalter','schwarzer 2-pol. Stecker<br>rosa → Thermoschalter → orange<br><small>gemessen ≈ 0 Ω</small>','G')
html='''<!doctype html><meta charset=utf-8><style>
body{margin:0;background:#fff;font-family:Arial,Helvetica,sans-serif}#c{position:relative;width:1700px;height:1700px}
.b{position:absolute;box-sizing:border-box;border:3px solid;border-radius:10px;padding:8px 10px;text-align:center;font-size:17px;line-height:1.25;display:flex;flex-direction:column;justify-content:center}
.b h{font-weight:bold;font-size:19px;display:block;margin-bottom:4px}.b small{font-size:14.5px}.d{border-style:dashed}
.n{position:absolute;left:-14px;top:-18px;width:34px;height:34px;border-radius:50%;background:#d40000;color:#fff;font-weight:bold;font-size:20px;display:flex;align-items:center;justify-content:center;border:3px solid #fff}
.t{position:absolute;font-size:16px;color:#444}
#leg{position:absolute;left:28px;top:1148px;width:1644px;box-sizing:border-box;border:2px solid #ccc;border-radius:14px;background:#f6f6f6;padding:16px 20px;font-size:17px;line-height:1.5}
#leg b{font-size:20px}svg{position:absolute;left:0;top:0}
</style><div id=c>
<div style="position:absolute;left:28px;top:14px;font-size:31px;font-weight:bold">Gefran GIRT S6T30 (MyRun) – geschätztes Funktionsschaltbild, Version 4</div>
<div style="position:absolute;left:28px;top:56px;font-size:17px;color:#444;line-height:1.35">Neu seit V3 (08.11.2026 abends): B10 (Netzerfassung), B18 (Busspannungs-Teiler), Q2 (Gate/Dioden) gemessen; Optokoppler-Zahl korrigiert (8, nicht 2×8).<br>Kein Leiterbahnplan. Netzseite nicht galvanisch getrennt (0VA = DC−), Zwischenkreis bis ca. 380 V – nur stromlos messen.</div>
'''
for (x,y,w,h,t,sub,st,num,dash,extra) in boxes:
    c=BC[st];n=f'<div class=n>{num}</div>' if num else ''
    html+=f'<div class="b{" d" if dash else ""}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-color:{c};background:{BG[st]}">{n}<h>{t}</h>{sub}</div>\n'
html+='''
<div class=t style="left:75px;top:405px;font-weight:bold;font-size:18px">Höhenverstellung<br><span style="font-weight:normal;font-size:16px">(getrennter AC-Pfad)</span></div>
<div class=t style="left:1000px;top:500px;width:195px;text-align:right">PWM an Chopper</div>
<div class=t style="left:410px;top:517px">Relaistreiber / Freigabe (Annahme, nicht verfolgt)</div>
<div class=t style="left:1590px;top:450px">Drehzahl</div>
<div class=t style="left:1418px;top:740px">Tacho → GIRT → P2 → Konsole</div>
<div class=t style="left:735px;top:906px">+12 V zur Konsole</div>
<div class=t style="left:1245px;top:878px">zurück zu P2</div>
<div class=t style="left:1312px;top:520px;width:225px;font-size:14px">P1 → B19 → Messeingang</div>
<div class=t style="left:215px;top:775px;font-size:14.5px;width:700px">Netzerfassung → Auswertung (Weg zum MCU unbekannt: Knoten J führt über X4 auf die andere Lage)</div>
<svg width=1700 height=1700 viewBox="0 0 1700 1700"><defs><marker id=a markerWidth=10 markerHeight=10 refX=9 refY=5 orient=auto><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>
<g stroke="#333" stroke-width=2.5 fill=none marker-end="url(#a)">
<path d="M143,230 H168"/><path d="M370,230 H401"/><path d="M631,230 H663"/><path d="M850,230 H883"/><path d="M1055,230 H1088"/><path d="M1290,230 H1321"/><path d="M1453,230 H1485"/>
<path d="M517,305 V383"/><path d="M631,435 H663"/><path d="M850,435 H883"/>
<path d="M1580,305 V608"/><path d="M1415,665 H1227"/>
<path d="M1205,608 V307"/>
<path d="M1085,800 V742"/><path d="M1085,1005 V930"/><path d="M1493,992 V905 H1227"/><path d="M1317,1048 H1227"/>
<path d="M1388,305 V363"/>
<path d="M1300,490 V635 H1227"/>
<path d="M60,305 V498"/>
</g>
<g stroke="#e69500" stroke-width=2.5 fill=none stroke-dasharray="7 6" marker-end="url(#a)">
<path d="M200,600 V765 H1000 V742"/>
</g>
<g stroke="#777" stroke-width=2.5 fill=none stroke-dasharray="7 6" marker-end="url(#a)">
<path d="M631,666 H663"/><path d="M878,722 V900 H938"/><path d="M992,608 V545 H385 V268 H401"/>
</g></svg>
<div id=leg><b>Grün = gemessen/belegt in Ordnung · Rot = verdächtig (nach Priorität) · Orange gestrichelt = Hypothese/offen</b><br>
<b style="color:#d40000">1</b> P2: Salzkruste zwischen Pins – PWM/Notlinie kann hochohmig sein oder Kriechstrom haben. Reinigen, Pin-Durchgang messen.<br>
<b style="color:#d40000">2</b> Korrodierte Lötstellen neben den R020 der Rückseite: Bereich Brücke/RT334024 (speist den Zwischenkreis).<br>
<b style="color:#d40000">3</b> Einschaltbegrenzung: 68 Ω stromlos messen, RT334024 beim Start auf Klicken achten und Spule messen; NTC P600 prüfen. Die ≈5 s Verzögerung nach START passt zu Relais/Bus-Aufladung und Busspannungs-Prüfung (B18) [H].<br>
<b style="color:#d40000">4</b> Chopper: Q2 + D3 statisch in Ordnung (D3 0,397 V, Body-Diode 0,444 V, G–S 9,13 kΩ, G–D 2,19 MΩ, 22-Ω-Gate-R). Offen: Treiber SOT-23-5 und Schalten – nur live (Trenntrafo nötig, nicht vorhanden).<br>
<b style="color:#d40000">5</b> Live-Messung L+/L− beim Start (DC): bei 1,2 km/h nur wenige Volt erwartet (Handbuch S. 46: 0,8 km/h ≈ 2,6 V).<br>
<b style="color:#d40000">6</b> UP/DOWN-Pads und P3 korrodiert: Kriechstrom bei 230 V kann FUSE MOT zerstört haben. Betrifft nur die Höhenverstellung.<br>
<b>Neu in Version 4:</b> B10 = Netzerfassung 2×(2×475k)+Diode (gesund, nicht Fehlerbereich) · B18 = Teiler L+ → 2,475 MΩ → P1 → ≈221k → 0VA (P2 = L+, 0 Ω; P1↔0VA 223,7k) · Q2 B5: G links im Foto (Rückseite: Pad mit Bahn zum 22-Ω-Widerstand) · Fehlstart: erster Impuls ≈5 s nach START, dann Abbruch, STS2 blinkt 4/8 (Fehler 902/904).
</div></div>'''
open('bd.html','w',encoding='utf-8').write(html)
