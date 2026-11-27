"""Read exported XML only; source-based expectations independent of generator graph."""
from pathlib import Path
import xml.etree.ElementTree as ET
import json,itertools,hashlib,subprocess
root=Path(__file__).resolve().parents[2]
here=root/'docs/gesamtschaltplan_110926'
xml=ET.parse(here/'gesamtschaltplan.xml')
nets={}
for net in xml.findall('.//nets/net'):
 for p in net.findall('node'): nets[p.attrib['ref']+'.'+p.attrib['pin']]=net.attrib['name']
def n(p): return nets.get(p,'UNCONNECTED:'+p)
checks=[]
def same(*pins):
 assert len({n(p) for p in pins})==1,('same',pins,[n(p) for p in pins])
 checks.append({'same':pins})
def separate(*pins):
 assert len({n(p) for p in pins})==len(pins),('separate',pins,[n(p) for p in pins])
 checks.append({'separate':pins})
same('D401.2','D402.2','R601.1','R602.1')
same('C602.1','R601.1','R602.1')
same('C602.2','R601.2')
separate('C602.1','C602.2','C601.1','U605.O')
assert xml.find(".//components/comp[@ref='C602']/property[@name='dnp']") is not None
assert not any(c.attrib['ref'].startswith(('D90','R90')) for c in xml.findall('.//components/comp'))
same('R601.2','U602.5','C601.2','U401.Tb','Q601.E','Q602.E','U201.B','U202.R','TP503.1')
same('R602.2','U602.3')
separate('U602.6','U602.7','U602.5','U602.3','U602.1')
same('U602.1','U602.2','R301.1')
same('R302.1','TP503.1')
same('R301.2','R302.2','R603.1')
same('R603.2','C601.1','U601.28')
same('U605.O','U601.26')
same('U605.L','TP503.1')
same('U605.R','TP501.1','U601.8','U603.C','U604.C')
same('U603.E','U601.12')
same('U604.E','U601.17','U601.18')
same('U604.K','J201.7','J201.8','J204.0V')
same('U601.11','R604.1','R605.2')
same('R605.1','TP501.1')
same('R604.2','U401.Tc')
same('U401.Ta','U301.15')
same('U301.19','U201.C','R202.1')
same('U601.24','R606.1')
same('R606.2','Q601.B')
same('Q601.C','K501.minus')
same('K501.plus','TP502.1','TP604.1')
same('U202.L','R607.1')
same('R607.2','R608.1')
same('R608.2','Q602.C')
separate('U601.8','U601.11','U601.12','U601.13','U601.17','U601.24','U601.26','U601.28')
separate('TP503.1','J201.7','TP501.1','TP502.1','U602.4','U602.8','U201.C')
separate('K501.plus','K501.minus','K501.11a','K501.14a')
separate('U602.1','R302.2','U601.28','U601.26')
separate('Q602.B','U601.11','U601.24','U201.D5')
separate('R301.1','R302.1')
same('U606.1','U607.K')
same('U606.5','J201.7')
separate('U607.C','U607.E','U601.17','U601.12','TP501.1','J201.7')
separate('U606.6','U606.7','U606.5','U606.1')
for comp in xml.findall('.//components/comp'):
 ref=comp.attrib['ref']
 if ref.startswith('R'):
  separate(ref+'.1',ref+'.2')
assert len([p for p in xml.findall('.//components/comp') if p.attrib['ref'] in ['R301','R302']])==2
assert '470' in xml.find(".//components/comp[@ref='C602']/value").text
# A separate exported drawing must represent the new chains in their actual
# order (Nutzerangabe 21.11. 14:50): Faston -> 470k -> 470k -> US1M -> J, with
# the cathode at J. This is the order of the original circuit, built from new
# parts. Never put the replacement chains in the original drawing, and never
# draw an additional parallel old branch (the Litzen only bridge the same nodes).
umbau=ET.parse(here/'b10_umbau_2026-11-21.xml')
unets={}
for net in umbau.findall('.//nets/net'):
 for pin in net.findall('node'):
  unets[pin.attrib['ref']+'.'+pin.attrib['pin']]=net.attrib['name']
uc=[]
def usame(*pins):
 assert len({unets[p] for p in pins})==1,('umbau same',pins)
 uc.append({'same':pins})
def useparate(*pins):
 assert len({unets[p] for p in pins})==len(pins),('umbau separate',pins)
 uc.append({'separate':pins})
usame('R901.2','R902.1');usame('R902.2','D901.1')
usame('R903.2','R904.1');usame('R904.2','D902.1')
usame('D901.2','D902.2','R601.1','R602.1','C602.1')
usame('R601.2','C602.2')
useparate('R901.1','R903.1','C602.1','C602.2')
useparate('R901.1','R901.2','D901.1','C602.1')
useparate('R903.1','R903.2','D902.1','C602.1')
useparate('C602.1','R602.2','C602.2')
assert unets['R901.1'].lstrip('/')=='AC_N'
assert unets['R903.1'].lstrip('/')=='AC_L'
assert unets['C602.2'].lstrip('/')=='0VA'
for ref in ['R901','R902','R903','R904']:
 assert umbau.find(f".//components/comp[@ref='{ref}']/value").text=='470 k / 4703'
for ref in ['D901','D902']:
 assert umbau.find(f".//components/comp[@ref='{ref}']/value").text=='US1M'
assert umbau.find(".//components/comp[@ref='C602']/property[@name='dnp']") is not None
assert not {'R401','R402','R403','R404','D401','D402'} & {c.attrib['ref'] for c in umbau.findall('.//components/comp')}
media=[]
media_details=[]
baseline='d11d0b216334c2af546306586f4df1c6df6b13a6'
for entry in subprocess.check_output(['git','ls-tree','-rz',baseline,'--','photos','docs/img','docs/messplan_stromlos_2026-11-08/makros'],cwd=root).split(b'\0'):
 if not entry: continue
 head,path=entry.split(b'\t',1);blob=head.split()[2].decode();name=path.decode();data=(root/name).read_bytes()
 got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 assert got==blob,('media changed',name)
 media.append(name)
 media_details.append({'path':name,'sha256':hashlib.sha256(data).hexdigest(),'unchanged':True})
(here/'originalmedien_pruefung.json').write_text(json.dumps({'base_commit':baseline,'checked_files':len(media),'all_unchanged':True,'files':media_details},ensure_ascii=False,indent=2)+'\n')
result={'baseline':baseline,'independent_native_net_assertions':len(checks),'independent_umbau_net_assertions':len(uc),'all_passed':True,'checks':checks,'umbau_checks':uc,'C602_DNP_in_both_sheets':True,'original_and_modified_B10_separate':True,'unchanged_original_and_reference_files':len(media),'source':'Final corrections through 16 Nov; C602 connections, measured capacity and actual B10 replacement in LAUF_2026-11-21.md; original photographs','hardware_function_verified':False,'reviewed_xml_sha256':hashlib.sha256((here/'gesamtschaltplan.xml').read_bytes()).hexdigest(),'reviewed_umbau_xml_sha256':hashlib.sha256((here/'b10_umbau_2026-11-21.xml').read_bytes()).hexdigest()}
(here/'unabhaengige_pruefung.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'checks','umbau_checks'}},ensure_ascii=False))
