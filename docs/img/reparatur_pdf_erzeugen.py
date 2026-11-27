#!/usr/bin/env python3
"""Erzeugt docs/REPARATUR.pdf (relativ zum Repo lauffaehig: python docs/img/reparatur_pdf_erzeugen.py)."""
import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak, Table, TableStyle
from PIL import Image as PI

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
def ttf(name):
    for d in ('/usr/share/fonts/truetype/dejavu', os.path.join(HERE, 'fonts')):
        p = os.path.join(d, name)
        if os.path.exists(p): return p
    sys.exit('Schrift fehlt: ' + name)
pdfmetrics.registerFont(TTFont('DV', ttf('DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DVB', ttf('DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DVB', italic='DV', boldItalic='DVB')

H1 = ParagraphStyle('h1', fontName='DVB', fontSize=14, leading=18, spaceAfter=2)
H2 = ParagraphStyle('h2', fontName='DVB', fontSize=12, leading=15, spaceBefore=6, spaceAfter=4)
B = ParagraphStyle('b', fontName='DV', fontSize=8.8, leading=12)
S = ParagraphStyle('s', fontName='DV', fontSize=7.8, leading=10.5, textColor=colors.HexColor('#333333'))
CAP = ParagraphStyle('c', fontName='DV', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#555555'))

W = A4[0] - 30*mm
def img(rel, width, cap):
    p = os.path.join(REPO, rel); w, h = PI.open(p).size
    return [Image(p, width=width, height=width*h/w), Paragraph(cap, CAP), Spacer(1, 3*mm)]
def img_h(rel, height):
    p = os.path.join(REPO, rel); w, h = PI.open(p).size
    return Image(p, width=height*w/h, height=height)
def facts(rows):
    t = Table([[Paragraph('<b>%s</b>' % a, B), Paragraph(b, B)] for a, b in rows], colWidths=[26*mm, W-26*mm])
    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.grey),
                           ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)]))
    return t
def foot(c, d):
    c.saveState(); c.setFont('DV', 7); c.setFillColor(colors.grey)
    c.drawString(15*mm, 8*mm, 'Technogym MyRun / GIRT S6T30 – Reparatur, Stand 27.11.2026')
    c.drawRightString(A4[0]-15*mm, 8*mm, 'Seite %d' % d.page); c.restoreState()

st = []
st += [Paragraph('Technogym MyRun / GIRT S6T30 – Reparatur: defekte Bauteile', H1),
       Paragraph('Stand 27.11.2026 · Gefran GIRT S6T30 (Platine ECS2458-6) · Belegstufen: [M] gemessen, [O] beobachtet, [I] abgeleitet, [H] Hypothese', S),
       Paragraph('Symptome vorher: Fehlstarts und Abbrüche (Konsole HF904/HF902/HF901, LED STS2 blinkt, Relaisklicken); Höhenverstellung ohne Funktion.', B),
       Paragraph('1. Kondensator C602 – Hauptursache der Fehlstarts', H2)]
st.append(facts([
    ('Bauteil', 'SMD-Keramikkondensator 0603, ca. 470 pF (ausgebaut kalt 0,43 nF; kein Aufdruck). „C602“ ist eine Schaltplan-Referenz, kein Aufdruck auf der Platine; erkennbar neben dem Widerstand „2212“'),
    ('Lage', 'Rückseite, Rasterfeld <b>E6</b> (Lage ±1 Feld), oberer Rand neben den Widerständen „2212“ (22,1 kΩ) und „1001“ (1 kΩ); Nachbarn: TL082 (SO-8, D6), L4981 (SO-20, E/F6). Nicht J6 (dort nur die B10-Dioden-/Widerstandsketten).'),
    ('Funktion', 'Netz-Messzweig: Knoten J nach 0VA parallel zu 2212, Tiefpass ca. 16 kHz vor dem TL082-Spannungsfolger [I]'),
    ('Fehlerbild', 'J normal ≈ 4,9 V; mit defektem C602 zeitweise Einbruch auf 0,1–0,9 V, wärmeabhängig [M] → Steuerung verweigert/bricht Motorbetrieb ab [I]'),
    ('Nachweis', 'Ohne C602 kein Einbruch; Altteil: 0,15–3 nF schwankend, Widerstand 2 MΩ → 20 kΩ (intakt OL) [M]. Neu: 460 pF stabil, OL. Nach Einbau J = 4,966 V konstant, Läufe bis 20 km/h fehlerfrei [M/O]'),
    ('Ersatz', '470 pF, 0603, ≥ 50 V, C0G/NP0 (X7R möglich), ±5–10 %; eingebaut 471 pF aus 0603-Sortiment'),
    ('Preis', 'ca. 0,10–0,30 € Einzelstück (DigiKey-Vergleichsteil 0,29 €); Großmenge ca. 0,015 € (Yageo CC0603JRNPO9BN471, RS 2006499P)'),
]))
st.append(Spacer(1, 3*mm))
st += img('docs/img/reparatur_c602_lage.jpg', W, 'Lage C602, Rückseite (aufrecht), Raster A–L / 1–6: Feld E6.')
st.append(Table([[img_h('docs/img/reparatur_c602_detail.jpg', 62*mm),
                  Paragraph('Detail: C602 (heller 0603-Kondensator) neben „2212“ und „1001“ am Knoten J. Foto 21.11.2026; Litzen gehören zum B10-Umbau (siehe Fußnote).', CAP)]],
                colWidths=[75*mm, W-75*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
st.append(PageBreak())
st.append(Paragraph('2. Sicherung FUSE MOT – Höhenverstellung', H2))
st.append(facts([
    ('Bauteil', 'Feinsicherung 5 × 20 mm, T4A träge, 250 V'),
    ('Lage', 'Vorderseite, Rasterfeld <b>J2</b> (Bauteil-ID F28, ±1 Feld), neben Aufdruck „FUSE MOT“, bei den Relais F24/F25 und den Kondensatoren C400/C401'),
    ('Funktion', 'Absicherung des 230-V-Zweigs zum Steigungsmotor (über Relais UP/DOWN)'),
    ('Fehlerbild', 'Sicherung fehlte beim Kauf (Glaskörper weg) → Höhenverstellung ohne Funktion [O]'),
    ('Nachweis', 'Nach Ersatz (T4A/250 V Keramik) Steigungstest 0 → 2 → 0 % bestanden, später bis 12 % [M/O]. Mögliche Vorgeschichte: Korrosion/Kriechstrom an UP/DOWN-Pads [H]'),
    ('Ersatz', '5 × 20 mm, T4A träge, 250 V, Keramik'),
    ('Preis', 'ca. 0,20–2 € Einzelstück; z. B. Conrad ESKA 522.723 (Best.-Nr. 537316), 1,92 €'),
]))
st.append(Spacer(1, 3*mm))
st += img('docs/img/reparatur_fuse_mot_lage.jpg', W, 'Lage FUSE MOT, Vorderseite: Bauteil F28, Feld J2.')
st.append(Table([[img_h('docs/img/reparatur_fuse_mot_detail.jpg', 55*mm),
                  Paragraph('Detail: Sicherungshalter FUSE MOT mit Keramiksicherung (Foto 08.11.2026).', CAP)]],
                colWidths=[85*mm, W-85*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
st.append(Spacer(1, 4*mm))
st.append(Paragraph('Weitere Maßnahmen (keine nachgewiesene Ursache)', H2))
st.append(Paragraph('Netzerfassung B10 neu aufgebaut (je Seite Faston – 470 kΩ – 470 kΩ – US1M – J, Litzenbrücken; <b>Umbau weiterhin eingebaut</b>); Reinigung von Salz-/Schweißkrusten; Nachlöten mehrerer Lötstellen (P2, DC MOTOR, UP/DOWN, Relais, Gleichrichter, Kühlkörperkontakte, B10); Drehzahlsensor gereinigt, Motorschrauben angezogen; 24.11. lockerer Kaltgerätestecker als Ursache eines Ausfalls (Stecker/Buchse prüfen).', S))
st.append(Spacer(1, 2*mm))
st.append(Paragraph('<b>Sicherheit:</b> Netzseite der GIRT nicht galvanisch getrennt; Zwischenkreis-Elko (560 µF/400 V) bis ca. 380 V DC. Nur stromlos arbeiten, Elko vorher messen/entladen.', S))

out = os.path.join(REPO, 'docs', 'REPARATUR.pdf')
doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=13*mm, bottomMargin=15*mm,
                        title='Technogym MyRun / GIRT S6T30 – Reparatur: defekte Bauteile', author='')
doc.build(st, onFirstPage=foot, onLaterPages=foot)
print(out)
