from pathlib import Path
import hashlib, json
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sources=['photos/2026-11-08/q2/q2_rueckseite_makro.jpg','photos/2026-11-08/q2/q2_rueckseite_weit.jpg','photos/2026-11-09/q2/50386.jpg']
(OUT/'quellen_sha256.json').write_text(json.dumps({p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},indent=2)+'\n')
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
W,H=842,595
c=canvas.Canvas(str(OUT/'Q2_Fotospuren.pdf'),pagesize=(W,H))
c.setTitle('Q2: Originalmakros, Fotospuren und vorläufige Schaltung – 13.11.2026')
BLUE='#1662A0'; ORANGE='#A14C00'; GREEN='#087A45'; GRAY='#606873'
def text(x,y,s,size=10,color='#17212B',bold=False):
 c.setFillColor(color); c.setFont('DVB' if bold else 'DV',size); c.drawString(x,y,s)
def line(points,color=BLUE,dash=False,width=1.6):
 c.setStrokeColor(color);c.setLineWidth(width);c.setDash(4,3) if dash else c.setDash()
 p=c.beginPath();p.moveTo(*points[0]);[p.lineTo(*a) for a in points[1:]];c.drawPath(p)
 c.setDash()
def dot(x,y,color=BLUE):
 c.setFillColor(color);c.circle(x,y,2.8,fill=1,stroke=0)
def head(title,sub):
 text(30,561,title,18,bold=True);text(30,539,sub,9)
 line([(30,525),(812,525)],GRAY,width=.7)
def foot(n):
 text(30,20,'13.11.2026 | Q2 / B21 / Feld B5 unverändert | M: Messung  F: Fotospur  H: Hypothese',8)
 text(790,20,str(n),9)
def resistor(x,y,label,value):
 c.setStrokeColor('#17212B');c.setLineWidth(1);c.rect(x,y-7,48,14,fill=0)
 text(x-2,y+22,label,10,bold=True);text(x-2,y-23,value,9)
def image_clip(path,box,x,y,w,h):
 im=Image.open(ROOT/path).convert('RGB')
 # Original pixels only. Cropping for the document; no retouching or generated image content.
 im=im.crop(box)
 c.drawImage(ImageReader(im),x,y,width=w,height=h)
 return lambda px,py:(x+(px-box[0])*w/(box[2]-box[0]),y+h-(py-box[1])*h/(box[3]-box[1]))
def mark(f,pt,label,offset,color):
 x,y=f(*pt);c.setStrokeColor(color);c.setLineWidth(1.7);c.circle(x,y,4,fill=0,stroke=1)
 lx,ly=x+offset[0],y+offset[1]
 line([(x,y),(lx,ly)],color,width=.8)
 tw=pdfmetrics.stringWidth(label,'DVB',10)
 c.setFillColor('#FFFFFF');c.rect(lx-3,ly-3,tw+6,14,fill=1,stroke=0)
 text(lx,ly,label,10,color,True)

head('Erster Schaltungsentwurf: Freigabe von Q2','Neue F-Verbindungen sind gestrichelt. FAN3100C und NPN-Funktion bleiben bedingte Typannahmen.')
# Main resistor chain
text(40,470,'C / VDD',12,bold=True);text(40,451,'= L4981 Pin 19 [M]',9)
line([(70,437),(70,408),(145,408)],BLUE)
resistor(145,408,'2211','2,21 kΩ')
line([(193,408),(245,408)],BLUE);dot(245,408)
text(233,427,'N',11)
line([(245,408),(290,408)],ORANGE,True)
resistor(290,408,'1001','1 kΩ')
line([(338,408),(395,408),(505,408)],ORANGE,True);dot(395,408,ORANGE)
text(455,419,'A / IN+ [H]',10)
line([(395,408),(395,342)],ORANGE,True)
c.setStrokeColor('#17212B');c.rect(388,294,14,48)
text(412,322,'4752',10,bold=True);text(412,306,'47,5 kΩ',9)
line([(395,294),(395,257)],ORANGE,True)
# transistor branch
line([(245,408),(245,370)],BLUE)
c.setStrokeColor('#17212B');c.rect(193,297,104,73)
text(208,348,'1P.O',10);text(208,330,'NPN? [H]',10,bold=True);text(208,312,'1P.R',10)
line([(245,297),(245,257)],BLUE)
text(35,330,'1P.L: Herkunft offen',9)
line([(162,335),(193,335)],GRAY,True)
# ground
line([(245,257),(395,257),(650,257),(650,306)],BLUE)
dot(395,257);text(270,235,'B / 0VA [M]',10)
# driver
c.setStrokeColor('#17212B');c.rect(505,306,220,139)
text(526,432,'100CA / FAN3100C? [H]',11,bold=True)
text(525,386,'OUT = IN+ UND NICHT IN−',10)
text(525,367,'nur bei ausreichender VDD',9)
text(525,329,'C: VDD     B: GND     E: OUT',9)
text(435,351,'D5 / IN−?',9)
line([(430,341),(505,341)],GRAY,True)
line([(725,400),(760,400),(760,296)],BLUE)
text(735,420,'E [M]',10)
c.setStrokeColor('#17212B');c.setLineWidth(1);c.rect(753,248,14,48)
text(680,278,'220',10,bold=True);text(672,262,'22,2 Ω [M]',9)
line([(760,248),(760,224)],BLUE);text(700,205,'Q2.G [M/F]',10,bold=True)
text(34,188,'Wirkungsmodell [H]',12,bold=True)
text(34,168,'1P leitet → N und A niedrig → Gate-Treiber gesperrt. 1P sperrt → Pull-up kann A anheben.',10)
text(34,149,'D5 bleibt ein separater, noch nicht vollständig verfolgter Eingang. Keine Verbindung zum Tacho belegt.',10)
text(34,119,'Messwertabgleich: A–0VA 4,17 kΩ; über 4752 4,16 kΩ; 1001 979/977 Ω; 2211 2,09 kΩ.',10)
text(34,100,'Der kleine Kondensator zwischen C und B ist als Abblockung belegt; Wert unbekannt (hier nicht gezeichnet).',9)
text(34,77,'Fotoverbindungen zuerst mit den vier Paaren auf Blatt 2 prüfen. Kein Bauteildefekt daraus bewiesen.',10,bold=True)
foot(1);c.showPage()

head('Originalmakro: A, Widerstandsnetz und Gate-Ausgang','q2_rueckseite_makro.jpg (08.11.) | Ausschnitt, unveränderte Pixel; Markierungen als PDF-Vektoren.')
f=image_clip(sources[0],(220,250,1150,1230),30,61,417,440)
# offsets clear above and below chip
for pt,lab,off,col in [((677,735),'A',(0,24),ORANGE),((760,735),'B',(0,42),BLUE),((843,735),'C',(20,24),BLUE),((677,975),'D5',(-43,-28),GRAY),((853,975),'E',(18,-20),BLUE),((350,560),'4752 links',(-34,-36),ORANGE),((540,560),'4752 rechts',(30,10),ORANGE),((350,390),'1001 links',(-45,28),ORANGE),((540,390),'1001 rechts',(-35,45),ORANGE),((610,390),'2211 links',(23,26),BLUE)]:
 mark(f,pt,lab,off,col)
for path in [[(677,735),(585,782),(468,782),(357,671),(350,610)],[(350,510),(350,445)],[(554,394),(594,394)],[(560,560),(720,560),(760,690)]]:
 line([f(*p) for p in path],ORANGE,True,1.8)
text(474,487,'Vier Bestätigungen, stromlos',13,bold=True)
items=[('1. A → 4752 links','Gebogene Leiterbahn zum linken Widerstandsende.'),('2. 4752 links → 1001 links','Kurze senkrechte Verbindung.'),('3. 1001 rechts → 2211 links','Kurzer Steg zwischen den nebeneinanderliegenden R.'),('4. 4752 rechts → B / 0VA','Breite Fläche zum Abblock-C und mittleren IC-Pin.')]
y=450
for title,desc in items:
 text(474,y,title,11,bold=True);text(474,y-19,desc,8.4);y-=65
text(474,165,'Erwartung jeweils:',11,bold=True)
text(474,145,'≈0 Ω nach Abzug des Messleitungswiderstands.',9)
text(474,126,'Bisher kein direkter Messwert für diese vier Paare.',9)
text(474,94,'Widerstandsaufdruck ≠ eingelöteter Messwert.',9,bold=True)
text(474,76,'4752: nominell 47,5 kΩ, eingebaut 4,16 kΩ.',9)
foot(2);c.showPage()

head('Originalmakro: getrennte Wege A und D5','q2_rueckseite_weit.jpg (08.11.) | D5 lässt sich ins Leiterbahnbündel verfolgen; Endanschluss bleibt offen.')
f=image_clip(sources[1],(680,0,1400,580),30,118,504,406)
for pt,lab,off,col in [((1245,460),'D5',(14,-28),GRAY),((1245,366),'A',(-50,17),ORANGE),((1183,425),'D5-Pad',(-80,-12),GRAY),((1278,366),'B',(0,23),BLUE),((1308,366),'C',(23,15),BLUE),((1235,154),'1P.L',(-54,0),BLUE),((1275,75),'1P.O',(18,12),BLUE),((1306,159),'1P.R',(15,-8),BLUE)]:
 mark(f,pt,lab,off,col)
# Only short unambiguous D5 section is drawn; no speculative long path.
line([f(*p) for p in [(1240,459),(1210,459),(1183,425),(1110,351),(1101,283),(1080,267),(920,254)]],GRAY,True,1.6)
text(558,481,'Hier endet die sichere Zuordnung',12,bold=True)
text(558,452,'D5 → rundes Pad → Leiterbahnbündel [F].',9)
text(558,432,'Weitere Makros wurden abgeglichen;',9)
text(558,415,'ein bestimmter End-Pin ist nicht gesichert.',9)
text(558,380,'Bereits gemessen [M]',11,bold=True)
text(558,356,'1P.O → 2211 links: 0 Ω',10)
text(558,336,'1P.R → 0VA: 0 Ω',10)
text(558,316,'2211 rechts → C: 0 Ω',10)
text(558,279,'Noch nicht bewiesen [H]',11,bold=True)
text(558,255,'1P = NPN; O = Kollektor, R = Emitter.',9)
text(558,235,'D5 = PWM; Ursprung MCU/Schutzlogik.',9)
text(558,215,'Ein Zusammenhang mit dem Tacho-Netz.',9)
text(34,85,'Kein Anschluss wurde über verdeckte Leiterbahnabschnitte oder einen ungesicherten Seitenwechsel ergänzt.',10)
text(34,65,'Der Sensorverdacht und die trennenden Prüfschritte stehen in der zugehörigen README.md.',10)
foot(3);c.showPage()
head('Wichtige Korrektur: 3,38 kΩ beweisen keinen 1P-Defekt','Abgleich am 13.11.2026 mit dem neuen Messplan in main (1b52c0c).')
text(35,480,'Es gibt mindestens zwei äußere Parallelwege zwischen 1P.O und 1P.R:',12,bold=True)
text(55,441,'Weg 1: N → 1001 → 4752 → 0VA',12)
text(55,416,'Nominell 1 kΩ + 47,5 kΩ = 48,5 kΩ.',11)
text(55,371,'Weg 2: N → 2211 → C/VDD-Netz → 0VA',12)
text(55,346,'2211 nominell 2,21 kΩ; C–0VA zuvor 1,45–1,48 kΩ gemessen.',11)
text(55,299,'Grobe Ersatzrechnung: 3,66 kΩ parallel 48,5 kΩ ≈ 3,40 kΩ.',14,bold=True)
text(55,269,'Vorhandene Messung vom 09.11.: 1P.R → N = 3,38 kΩ (Q2C-05).',12)
text(35,218,'Die Übereinstimmung zeigt: Der kleine Wert braucht keinen lecken Transistor als Erklärung.',11)
text(35,193,'Nichtlinearität und weitere Parallelpfade begrenzen die Rechnung; sie ist kein Bauteiltest.',10)
text(35,150,'Auch die Eingangsrollen bleiben offen:',12,bold=True)
text(35,126,'A kann eine statische Freigabe sein; ein fehlender Takt an A allein beweist keinen Fehler.',11)
text(35,103,'D5 kann Steuer- oder Schutzfunktion haben. Keine Freigabe erzwingen oder Schutzpfade überbrücken.',10)
text(35,71,'Diodentest am 1P bleibt sinnvoll, aber Rückwärtsleitung eingebaut nicht automatisch als Defekt werten.',10)
foot(4);c.save()
