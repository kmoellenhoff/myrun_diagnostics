#!/usr/bin/env python3
"""Erzeugt docs/GIRT_Platinen_Uebersicht.pdf (v3, Stand 27.11.2026).

Aufruf (relativ zum Repo): python docs/img/platinen_uebersicht_erzeugen.py

Die vier Platinenansichten (mit Raster und F-/B-Beschriftung) stammen unveraendert aus dem
Entwurf v2 (08.11.2026) und liegen als docs/img/uebersicht_v2_*.jpg vor (aus der alten PDF mit
`pdfimages -j` extrahiert, Originalpixel). Dieses Skript zeichnet nur die Markierungen
C602 (Rueckseite, E6) und FUSE MOT / F28 (Vorderseite, J2) hinein; die Lage stammt aus
docs/img/reparatur_c602_lage.jpg bzw. reparatur_fuse_mot_lage.jpg (2000 px breit, Faktor 1,5).
Gespiegelte Ansichten: y -> Bildhoehe - y.
"""
import os, sys, tempfile
from PIL import Image as PI, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Image, Spacer,
                                PageBreak, Table, TableStyle, ListFlowable, ListItem, KeepTogether)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(REPO, 'docs', 'GIRT_Platinen_Uebersicht.pdf')

def ttf(name):
    for d in ('/usr/share/fonts/truetype/dejavu', os.path.join(HERE, 'fonts')):
        p = os.path.join(d, name)
        if os.path.exists(p): return p
    sys.exit('Schrift fehlt: ' + name)
FONT, FONTB = ttf('DejaVuSans.ttf'), ttf('DejaVuSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('DV', FONT)); pdfmetrics.registerFont(TTFont('DVB', FONTB))
pdfmetrics.registerFont(TTFont('DVM', ttf('DejaVuSansMono.ttf')))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DVB', italic='DV', boldItalic='DVB')

# ---------- Markierungen in die Bilder zeichnen ----------
YEL, RED = (255, 230, 0), (205, 20, 20)
def label(d, cx, top, text, size=46):
    f = ImageFont.truetype(FONTB, size)
    l, t, r, b = d.textbbox((0, 0), text, font=f)
    w, h = r - l + 36, b - t + 24
    x0 = max(8, min(cx - w // 2, 3000 - w - 8))
    d.rectangle([x0, top, x0 + w, top + h], fill=RED, outline=YEL, width=5)
    d.text((x0 + 18 - l, top + 12 - t), text, font=f, fill='white')
    return top, top + h

def mark_c602(src, flip):
    im = PI.open(src).convert('RGB'); H = im.size[1]; d = ImageDraw.Draw(im)
    cx, cy, r = 1149, 72, 52                      # Lage aus reparatur_c602_lage.jpg (x1,5)
    ly = 292                                        # Beschriftung unterhalb (nicht flipped)
    if flip: cy, ly = H - cy, H - 292 - 66
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=YEL, width=9)
    d.ellipse([cx-r+9, cy-r+9, cx+r-9, cy+r-9], outline=RED, width=6)
    top, bot = label(d, cx, ly, 'C602 (Defekt 1, E6)')
    y0, y1 = (cy + r, top) if not flip else (bot, cy - r)
    d.line([cx, y0, cx, y1], fill=RED, width=7)
    return im

def mark_fuse(src, flip):
    im = PI.open(src).convert('RGB'); H = im.size[1]; d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 2412, 186, 2567, 512           # Lage aus reparatur_fuse_mot_lage.jpg (x1,5)
    ly = 567
    if flip: y0, y1, ly = H - y1, H - y0, H - 567 - 66
    d.rectangle([x0, y0, x1, y1], outline=YEL, width=9)
    d.rectangle([x0+9, y0+9, x1-9, y1-9], outline=RED, width=6)
    top, bot = label(d, (x0 + x1) // 2, ly, 'FUSE MOT (F28, Defekt 2, J2)')
    a, b = (y1, top) if not flip else (bot, y0)
    d.line([(x0 + x1) // 2, a, (x0 + x1) // 2, b], fill=RED, width=7)
    return im

tmp = tempfile.mkdtemp()
def img(name, fn, flip):
    out = os.path.join(tmp, name)
    fn(os.path.join(HERE, 'uebersicht_v2_' + name), flip).save(out, quality=92)
    return out
IMG_A_FRONT = img('A_vorderseite.jpg', mark_fuse, False)
IMG_A_BACK = img('A_rueckseite_gespiegelt.jpg', mark_c602, True)
IMG_B_BACK = img('B_rueckseite.jpg', mark_c602, False)
IMG_B_FRONT = img('B_vorderseite_gespiegelt.jpg', mark_fuse, True)

# ---------- Stile ----------
PW, PH = landscape(A3); M = 39
W = PW - 2 * M
H1 = ParagraphStyle('h1', fontName='DVB', fontSize=15, leading=19, spaceAfter=5)
H2 = ParagraphStyle('h2', fontName='DVB', fontSize=11.5, leading=15, spaceBefore=4, spaceAfter=5)
P = ParagraphStyle('p', fontName='DV', fontSize=8.4, leading=11, spaceAfter=3)
PR = ParagraphStyle('pr', parent=P, fontName='DVB', textColor=colors.HexColor('#b01414'))
CAP = ParagraphStyle('cap', fontName='DV', fontSize=8, leading=10, textColor=colors.HexColor('#555555'), spaceBefore=3)
TC = ParagraphStyle('tc', fontName='DV', fontSize=8.2, leading=10)
TCB = ParagraphStyle('tcb', parent=TC, fontName='DVB')
TCR = ParagraphStyle('tcr', parent=TCB, textColor=colors.HexColor('#b01414'))
LI = ParagraphStyle('li', fontName='DV', fontSize=10.5, leading=15, spaceAfter=5)

CLS = {'Netz/Hochspannung': '#e02020', 'Leistungsteil': '#f0a020', 'Logik/Signal': '#2060e0',
       'Anschluss': '#10a050', 'Hilfsspannung': '#9030c0'}
def chips():
    cells = [Paragraph('<font color="white">%s</font>' % k, ParagraphStyle('c', fontName='DV', fontSize=7.5, leading=9, alignment=1)) for k in CLS]
    t = Table([cells], colWidths=[104, 76, 76, 66, 80], hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND', (i, 0), (i, 0), colors.HexColor(c)) for i, c in enumerate(CLS.values())] +
                          [('LINEAFTER', (0, 0), (-2, -1), 3, colors.white), ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)]))
    return t

def image(path, cap):
    w, h = PI.open(path).size
    return [Image(path, width=W, height=W * h / w), Paragraph(cap, CAP)]

# ---------- Tabellen ----------
FRONT = [
 ('F1','A1','DC MOTOR L+/L-','Anschluss'), ('F2','A2','Ringkerndrossel Motorausgang','Leistungsteil'),
 ('F3','E1','P4 Tacho','Anschluss'), ('F4','F1','P2 Konsole 2x9','Anschluss'), ('F5','H1','P3 Poti','Anschluss'),
 ('F6','J1','UP/DOWN','Anschluss'), ('F7','L1','AC LINE','Anschluss'),
 ('F8','C2','Logik-ICs: 2x74ACT14, LM2903, ADM485, 2x78L05','Logik/Signal'),
 ('F9','C2','8x VO617A-8 (OC01-OC08; OC01+OC07 um 180° gedreht)','Logik/Signal'),
 ('F10','B3','P602 14-pol','Logik/Signal'), ('F11','B3','P601 RST/0VA','Logik/Signal'),
 ('F12','C4','MCU QFP-32','Logik/Signal'), ('F13','C4','SO-8 (24C32?)','Logik/Signal'),
 ('F14','C4','P70 6-pol Debug','Logik/Signal'), ('F15','B5','P600 NTC 10 kΩ (Temperatur Q2)','Logik/Signal'),
 ('F16','D3','SOT-223 x2, CPC1017N, 47uF','Hilfsspannung'), ('F17','E2','Trafo ETI349X4','Hilfsspannung'),
 ('F18','G2','4x330uF + RT700','Hilfsspannung'), ('F19','D2','47uF Elkos','Hilfsspannung'),
 ('F20','E3','U702 SO-8, C727, C703','Hilfsspannung'),
 ('F21','E4','DC-Link-Elko 560 µF/400 V (S890A16E), Standby ca. 316–324 V [M]','Leistungsteil'),
 ('F22','G3','großer Ringkern (Drossel)','Leistungsteil'), ('F23','F3','P400 0V24/+24V','Hilfsspannung'),
 ('F24','I2','Relais Schrack orange','Netz/Hochspannung'), ('F25','I2','2x Relais Panasonic','Netz/Hochspannung'),
 ('F26','J4','Relais Panasonic','Netz/Hochspannung'),
 ('F27','I4','Relais RT334024 (Einschaltbegrenzung, 24-V-Spule) + 68 Ω','Netz/Hochspannung'),
 ('F28','J2','FUSE MOT T4A träge 5×20 – fehlte, ersetzt (Defekt 2)','Netz/Hochspannung'),
 ('F29','L4','Netzfilter (X-Kondensatoren, 3 Drosseln)','Netz/Hochspannung'),
 ('F30','F6','Kühlkörper: Q2,D3,D2,Q1','Leistungsteil'), ('F31','D5','Testpunkte 0VA/+5VA','Logik/Signal'),
 ('F32','I2','Testpunkte +12VISO/0VISO','Hilfsspannung'),
 ('F33','B5','Q2 MOSFET (an Kühlkörper geklemmt) neben P600','Leistungsteil')]
BACK = [
 ('B1','C5','LEDs STS2/STS1/+5V/LINE','Logik/Signal'), ('B2','C4','6 Pads (P70)','Logik/Signal'),
 ('B3','F6','SO-20 L4981AP (PFC-Regler)','Logik/Signal'),
 ('B4','D6','2x SO-8, darunter TL082 (Puffer Netzspannungs-Messsignal)','Logik/Signal'),
 ('B5','F1','P2 Lötpads','Anschluss'), ('B6','F2','2x DPAK-Bauteil','Hilfsspannung'),
 ('B7','H4','4x R020 Shunt 0,02 Ohm (nicht 2-Draht messbar)','Leistungsteil'), ('B8','H3','SOT-223','Logik/Signal'),
 ('B9','K2','2x 471 SMD','Leistungsteil'),
 ('B10','J6','Netzerfassung L/N: je 2×470 kΩ + US1M (Umbau 21.11., Original 2×475 kΩ + Diode)','Netz/Hochspannung'),
 ('B11','B3','Testpad-Reihe','Logik/Signal'), ('B13','A1','DC MOTOR Pads','Anschluss'),
 ('B14','L4','Netz-/Filter-Pads','Netz/Hochspannung'), ('B15','J1','UP/DOWN Pads','Anschluss'),
 ('B16','L1','AC LINE Pads','Anschluss'), ('B17','E3','4702/47R0 SMD','Logik/Signal'),
 ('B21','B5','Q2 Beine G/D/S (3 Pads, 2 Isolierschlitze) + 22R + Treiber SOT-23-5','Leistungsteil'),
 ('B18','E5','PFC-Rückführung: L+ → 1M+1M+475k → … → L4981 Pin 14 VFEED (Verbindung gemessen)','Netz/Hochspannung'),
 ('B19','E6','Widerstandsblock der PFC-Rückführung (u. a. 2×1M parallel, 39,2 kΩ nach 0VA)','Logik/Signal'),
 ('B20','E6','Reihe aus 4 Widerständen + SOT-23 (NPN-ähnlich) [H]','Leistungsteil'),
 ('C602','E6','Kondensator 470 pF 0603 am Knoten J neben „2212“ (Filter Netzsignal) – defekt, ersetzt (Defekt 1)','Logik/Signal')]
HILITE = {'F28', 'C602'}

def table(rows, widths):
    data = [[Paragraph(h, TCB) for h in ('ID', 'Feld', 'Bauteil / Bereich', 'Klasse')]]
    style = [('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#444444')), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#eeeeee')),
             ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 1.8), ('BOTTOMPADDING', (0,0), (-1,-1), 1.8)]
    for i, (a, b, c, d) in enumerate(rows, 1):
        hl = a in HILITE
        data.append([Paragraph(a, TCR if hl else TCB), Paragraph(b, TCR if hl else TC),
                     Paragraph(c, TCR if hl else TC), Paragraph(d, TC)])
        if hl: style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#fff2b3')))
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(style)); return t
TW = [W*0.062, W*0.07, W*0.64, W*0.228]

# ---------- Dokument ----------
def deco(c, d):
    c.saveState(); c.setFont('DV', 7.5); c.setFillColor(colors.HexColor('#777777'))
    c.drawString(M, 18, 'GIRT S6T30 (ECS2458-6) – Platinen-Übersicht v3, Stand 27.11.2026')
    c.drawRightString(PW - M, 18, 'Seite %d' % d.page); c.restoreState()
doc = BaseDocTemplate(OUT, pagesize=(PW, PH), leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=34,
                      title='GIRT S6T30 (ECS2458-6) – Platinen-Übersicht v3 (Stand 27.11.2026, repariert)',
                      author='myrun_diagnostics')
doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(M, 34, W, PH - M - 34, 0, 0, 0, 0)], onPage=deco)])

st = [Paragraph('GIRT S6T30 (ECS2458-6) – Platinen-Übersicht v3 (Stand 27.11.2026, repariert)', H1), chips(), Spacer(1, 5),
 Paragraph('<b>Raster:</b> 12 Spalten (A–L) × 6 Zeilen (1–6). Ein Feld meint auf Vorder- und Rückseite <b>dieselbe Stelle der Platine</b> (z. B. P2 = F1/G1). Die Felder sind in allen vier Bildern gleich benannt; wenn ein Bild vertikal gedreht ist, laufen die Zeilenziffern am Bildrand von <b>6 oben nach 1 unten</b>.', P),
 Paragraph('<b>Zwei Varianten:</b> <b>A</b> = Vorderseite wie fotografiert, Rückseite vertikal gespiegelt (Zeilen laufen gleich, Rückseiten-Schrift steht auf dem Kopf). <b>B</b> = Rückseite wie fotografiert (Schrift lesbar), Vorderseite vertikal gespiegelt (Vorderseiten-Schrift steht auf dem Kopf). Die Bauteiltabellen stehen jeweils einmal hinter Variante A und gelten für beide.', P),
 Paragraph('<b>Gewissheit:</b> Positionen aus Foto (ungefähr, ±1 Feld). Leiterbahnen nur teilweise verfolgt (siehe docs/schaltplan/). Funktionszuordnungen sind Vermutungen, soweit nicht aus Aufdrucken oder Messungen belegt ([H] = Hypothese). Zeilen 5–6 der Vorderseite sind im Foto vom Kühlkörper verdeckt.', P),
 Paragraph('Reparatur: Defekt 1 = C602 (Rückseite E6), Defekt 2 = FUSE MOT (Vorderseite J2), Details docs/REPARATUR.md', PR),
 Paragraph('Variante A – Vorderseite (Bauteilseite), wie fotografiert', H2)]
st += image(IMG_A_FRONT, 'Gelb/rot markiert: FUSE MOT (F28, Feld J2) – Defekt 2.')
st += [PageBreak(), Paragraph('Tabelle Vorderseite (F-IDs)', H1), table(FRONT, TW), PageBreak(),
       Paragraph('Variante A – Rückseite (Lötseite), vertikal gespiegelt (Zeilen wie Vorderseite)', H2)]
st += image(IMG_A_BACK, 'Gelb/rot markiert: C602 (Feld E6, Lage ±1 Feld) – Defekt 1. Beschriftung der Markierung zur Lesbarkeit aufrecht.')
st += [PageBreak(), Paragraph('Tabelle Rückseite (B-IDs)', H1), table(BACK, TW), PageBreak(),
       Paragraph('Variante B – Rückseite (Lötseite), wie fotografiert (Schrift lesbar; Zeilen 6 oben → 1 unten)', H2)]
st += image(IMG_B_BACK, 'Gelb/rot markiert: C602 (Feld E6, Lage ±1 Feld) – Defekt 1.')
st += [PageBreak(), Paragraph('Variante B – Vorderseite, vertikal gespiegelt (Zeilen 6 oben → 1 unten)', H2)]
st += image(IMG_B_FRONT, 'Gelb/rot markiert: FUSE MOT (F28, Feld J2) – Defekt 2. Beschriftung der Markierung zur Lesbarkeit aufrecht.')

items = [
 '<b>Defekt 1 – Kondensator C602 (Rückseite, Feld E6, Lage ±1 Feld; nicht J6):</b> SMD-Keramikkondensator 0603, ca. 470 pF, am Knoten J der Netzerfassung direkt neben dem 22,1-kΩ-Widerstand „2212“ (Tiefpass/Filter vor dem TL082-Spannungsfolger [I]). '
 'Fehlerbild: innerer Nebenschluss; J brach wärmeabhängig von ≈ 4,9 V auf 0,1–0,9 V ein [M], die Steuerung verweigerte bzw. brach den Motorbetrieb ab (HF904/HF902, STS2 blinkt) [I]. '
 'Ersatz: 470 pF, 0603, ≥ 50 V, C0G/NP0 bevorzugt (eingebaut: 471 pF); danach J = 4,966 V konstant, auch unter Wärme, Läufe fehlerfrei [M/O].',
 '<b>Defekt 2 – FUSE MOT (Vorderseite, Feld J2, F28):</b> Feinsicherung 5 × 20 mm, T4A träge, 250 V, im 230-V-Zweig des Höhenmotors. Sie fehlte (Glaskörper weg), die Höhenverstellung war ohne Funktion [O]. '
 'Ersetzt durch eine Keramiksicherung gleichen Typs; Steigungstest 0 → 2 → 0 % bestanden, später bis 12 % [M/O]. Nur den vorgegebenen Typ einsetzen.',
 '<b>Weitere Maßnahmen (nicht als Ursache nachgewiesen):</b> Netzerfassung B10 mit neuen Teilen aufgebaut (je Seite 2 × 470 kΩ + US1M, bleibt eingebaut); Salz-/Schweißkrusten gereinigt (P2, P3, Erdschraube, UP/DOWN-Pads); '
 'nachgelötet: P2, DC MOTOR, UP/DOWN, RT334024 + 68 Ω, Brückengleichrichter, Kühlkörperkontakte Q2/D2/D3, B10-Bereich; Drehzahlsensor (P4) von Bürstenstaub gereinigt, lose Schrauben am Motorgehäuse angezogen. '
 'Der Ausfall vom 24.11. während der Höhenverstellung lag an einem lockeren Kaltgerätestecker; Stecker/Buchse prüfen, ggf. tauschen.',
 '<b>Weitere Platinenhinweise:</b> B7 (H4): vier R020-Shunts 0,02 Ω – 2-Draht nicht messbar [I]. B1 (C5): LEDs STS2/STS1/+5V/LINE; B2: 6 Pads (Gegenstück zu P70 vorn, F14).',
 '<b>Sicherheit:</b> Die Netzseite der GIRT ist nicht galvanisch getrennt; der Zwischenkreis-Elko (560 µF/400 V) liegt bis ca. 380 V DC. Nur stromlos arbeiten, Elko vorher messen und ggf. über einen Widerstand entladen.']
st += [PageBreak(), Paragraph('Reparaturhinweise (Stand 27.11.2026)', H1),
       ListFlowable([ListItem(Paragraph(t, LI), leftIndent=16) for t in items], bulletType='bullet', start='•', leftIndent=16)]
doc.build(st)
print('geschrieben:', OUT)
