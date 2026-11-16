"""Technische Anschluss-Skizze, keine Platinenbildgenerierung. Originalfotos bleiben unverändert."""
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/myrun-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

OUT = Path(__file__).resolve().parent
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'svg.fonttype': 'none'})
fig, ax = plt.subplots(figsize=(16, 12))
fig.subplots_adjust(0, 0, 1, 1)
ax.set(xlim=(0, 16), ylim=(0, 12))
ax.axis('off')
green, blue, orange, red, grey = '#007b66', '#2366aa', '#b36208', '#ae3651', '#7c8590'
def txt(x, y, s, **kw):
    return ax.text(x, y, s, va='top', **kw)
def wire(points, c, dashed=False):
    ax.plot(*zip(*points), color=c, lw=2, ls='--' if dashed else '-', solid_capstyle='round')
def mark(p, c):
    ax.add_patch(Circle(p, .055, color=c, zorder=5))

txt(.55, 11.7, 'GIRT S6T30 · MCU: bestätigte Anschlüsse', fontsize=22, weight='bold')
txt(.55, 11.22, 'Stand 16.11.2026 · Draufsicht auf die Bauteilseite', color=grey, fontsize=12)
txt(.55, 10.9, 'Pin-Nr. = Arbeitsnummer: ab Gehäusemarke gegen den Uhrzeigersinn gezählt (1–32). Ob das die Datenblatt-Nummern sind, ist offen.', fontsize=12)

ax.add_patch(Rectangle((6, 3), 4, 4, facecolor='#eef2f6', edgecolor='#283444', lw=2))
pos = [3.35 + i * 3.3 / 7 for i in range(8)]
xp = [6.35 + i * 3.3 / 7 for i in range(8)]
for y in pos:
    ax.add_patch(Rectangle((5.65, y-.075), .35, .15, facecolor='#d2d8df', edgecolor=grey))
    ax.add_patch(Rectangle((10, y-.075), .35, .15, facecolor='#d2d8df', edgecolor=grey))
for x in xp:
    ax.add_patch(Rectangle((x-.075, 7), .15, .35, facecolor='#d2d8df', edgecolor=grey))
    ax.add_patch(Rectangle((x-.075, 2.65), .15, .35, facecolor='#d2d8df', edgecolor=grey))
ax.add_patch(Circle((6.4, 3.4), .13, facecolor='#283444'))
txt(8, 6.35, 'MCU · 32 Anschlüsse', ha='center', fontsize=15, weight='bold')
txt(8, 5.85, 'Typ / Datenblatt-Pinout\nnicht gesichert', ha='center', fontsize=12)
txt(8, 5.05, 'X und Y: getrennte Netze\nKeine Brücke setzen', ha='center', color=red, fontsize=12, weight='bold')
txt(8, 4.35, 'Grau: nicht zugeordnet\nMCU-GND-Pin noch offen', ha='center', color=grey)
txt(6.65, 3.75, 'Gehäusemarke (Pin 1)', fontsize=10)
txt(5.65, 7.95, 'Ecke bei P13', color=grey, fontsize=10, ha='center')
txt(10.2, 7.95, 'Ecke bei P70', color=grey, fontsize=10, ha='center')
txt(7.6, 2.25, 'Blauer Stecker P602\nunterhalb des MCU', ha='center', color=grey, fontsize=10)
txt(11, 2.6, 'EEPROM rechts unten', color=grey, fontsize=10)

# F27: obere Reihe, linker Eckanschluss (Originalfoto um 90 Grad gedreht).
wire([(xp[0],7.35),(xp[0],10.45),(.65,10.45)],orange)
mark((xp[0],7.35),orange)
txt(.65,10.3,'Pin 24 · F27 · Ausgang zum Relaistreiber T4',color=orange,weight='bold',fontsize=13)
txt(.65,9.92,'Obere Reihe: 1. Anschluss ab P13-Ecke\nMCU → 1 kΩ (1001) → Basis T4 (L)\nF27-Spule: +24 V → Spule → Kollektor T4 (O)\nEmitter T4 (R) → 0VA\nSpulenplus = SOT-223-Tab; Bauteiltyp offen\nBisher: 0 V über Spule bei Standby / Fehlstart\nT4-Ansteuerung im Betrieb noch nicht gemessen.',fontsize=10.5,linespacing=1.4)

# Linke Seite: ab oberer Ecke (P13) nach unten zählen.
y_y, y_x = pos[-2], pos[-4]
wire([(5.65,y_y),(4.9,y_y),(4.9,7.9),(.65,7.9)], blue); mark((5.65,y_y),blue)
txt(.65,7.8,'Pin 26 · Y · Signalquelle offen',color=blue,weight='bold',fontsize=13)
txt(.65,7.45,'2. Anschluss ab P13-Ecke\nLD3N: O = Y; L = 0VA; R = +5VA\nKlemmung gemessen; Eingangsfunktion offen',fontsize=10.5)
wire([(5.65,y_x),(4.65,y_x),(.65,y_x)],green); mark((5.65,y_x),green)
txt(.65,y_x-.12,'Pin 28 · X · Netzsignal aus B10',color=green,weight='bold',fontsize=13)
txt(.65,y_x-.48,'4. Anschluss ab P13-Ecke\nJ → 1 kΩ → TL082 Pin 3\nPin 1 = Pin 2: Spannungsfolger\nAusgang → 4,75 kΩ → 100 Ω → X\nFilterkondensator von X nach 0VA\nP13 selbst ist nicht mit X verbunden.',fontsize=10.5,linespacing=1.5)

# Obere Seite: erste zwei Anschlüsse ab rechter Ecke bei P70.
for x in xp[-2:]:
    wire([(x,7.35),(x,8.12)],green); mark((x,7.35),green)
wire([(xp[-2],8.12),(xp[-1],8.12),(10.5,8.12)],green)
txt(10.7,8.72,'Pin 17 + 18 · PWM-Sollwert · OC05 Emitter',color=green,weight='bold',fontsize=12)
txt(10.7,8.35,'Obere Reihe: 1. + 2. ab P70-Ecke\nBeide verbunden laut Messprotokoll.\nZweck der Doppelbelegung unbekannt.',fontsize=10.5)

# Rechte Seite: Zählung ab unterer Ecke (EEPROM/P602).
for idx,c,yy,title,body in [
    (4,grey,6.7,'Pin 13 · P70 · Funktion offen','5. Anschluss ab unterer Ecke\nVerbindung zum Testpunkt bestätigt.'),
    (3,green,5.4,'Pin 12 · Enable · OC04 Emitter','4. Anschluss ab unterer Ecke\nSignalpfad bestätigt; Live-Pegel offen.'),
    (2,orange,4.1,'Pin 11 · PFC-Sperre · Ausgang zu T3','3. Anschluss ab unterer Ecke\n→ 2,21 kΩ → Basis T3 → L4981 Pin 15\n10-kΩ-Pull-up nach +5VA am Steuerknoten\nStandby / Fehlstart: 4,9 V am Knoten.')]:
    p=(10.35,pos[idx]); wire([p,(10.65,pos[idx]),(11,yy),(15.3,yy)],c); mark(p,c)
    txt(11,yy-.12,title,color=c,weight='bold',fontsize=12)
    txt(11,yy-.48,body,fontsize=10.3,linespacing=1.4)

wire([(xp[-1],2.65),(xp[-1],1.95),(11,1.95)],red); mark((xp[-1],2.65),red)
txt(11,1.84,'Pin 8 · +5VA · Versorgungsknoten',color=red,weight='bold',fontsize=12)
txt(11,1.5,'Unterer Eckanschluss rechts\n= Kollektoren von OC04 und OC05\nKein Enable-/PWM-Eingang.',fontsize=10.5)
txt(.65,2.15,'OC04 / OC05: Ausgänge an den Emittern',weight='bold',fontsize=12)
txt(.65,1.8,'Kollektoren gemeinsam an +5VA. Emitter → 0VA:\nOC04: 3,3 kΩ; OC05: 10 kΩ (in-circuit gemessen).\nLED-Strom kann den Emitter anheben; Signalqualität noch offen.',fontsize=10.5,linespacing=1.5)
txt(.65,.72,'Noch nicht am MCU lokalisiert: Motorfreigabe T2, OC02/03/08, RS-485. T4-Bahn (b): Funktion offen.',color=grey,fontsize=11)
txt(.65,.35,'Gemessene Verbindungen ≠ Funktionsnachweis. Netzseite: 0VA ist nicht Schutzleiter. Quellen und Orientierung: README.md.',color=grey,fontsize=10)

# Arbeitsnummern: ab Gehäusemarke (unten links) gegen den Uhrzeigersinn.
for i,x in enumerate(xp):            # unten, links -> rechts: 1..8
    ax.text(x, 3.08, str(1+i), ha='center', va='bottom', fontsize=9, color='#283444', weight='bold')
for i,y in enumerate(pos):           # rechts, unten -> oben: 9..16
    ax.text(9.92, y, str(9+i), ha='right', va='center', fontsize=9, color='#283444', weight='bold')
for i,x in enumerate(reversed(xp)):  # oben, rechts -> links: 17..24
    ax.text(x, 6.92, str(17+i), ha='center', va='top', fontsize=9, color='#283444', weight='bold')
for i,y in enumerate(reversed(pos)): # links, oben -> unten: 25..32
    ax.text(6.08, y, str(25+i), ha='left', va='center', fontsize=9, color='#283444', weight='bold')
for ext in ('png','svg','pdf'):
    fig.savefig(OUT / f'mcu_anschluesse.{ext}', dpi=160, facecolor='white')
svg = OUT / 'mcu_anschluesse.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
