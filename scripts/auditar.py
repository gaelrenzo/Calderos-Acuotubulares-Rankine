"""Controles automáticos complementarios a la inspección visual de las páginas."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'Grupo1_Calderos_Acuotubulares.pdf'
r=PdfReader(PDF)
texts=[p.extract_text() or '' for p in r.pages]
assert len(r.pages)==10
assert PDF.stat().st_size<100_000_000
assert all(len(t)>100 for t in texts)
assert all(abs(float(p.mediabox.width)-595.276)<1 and
           abs(float(p.mediabox.height)-841.890)<1 for p in r.pages)
text='\n'.join(texts)
assert not re.search(r'\b(?:TODO|PLACEHOLDER)\b|\?\?',text)
source=(ROOT/'main.tex').read_text(encoding='utf-8')
bib=(ROOT/'referencias.bib').read_text(encoding='utf-8')
cited={k.strip() for c in re.findall(r'\\cite\{([^}]+)\}',source) for k in c.split(',')}
entries=set(re.findall(r'@\w+\{([^,]+)',bib))
assert len(cited)>=5 and cited==entries
abstract=source.split(r'\begin{abstract}')[1].split(r'\end{abstract}')[0]
assert 150<=len(abstract.split())<=250
log=(ROOT/'build/main.log').read_text(encoding='utf-8',errors='replace')
assert not re.search(r'Overfull|Missing character|undefined|LaTeX Warning',log)
uris=[]
for pg in r.pages:
    for annot in pg.get('/Annots',[]):
        action=annot.get_object().get('/A')
        if action and action.get('/URI'):uris.append(str(action['/URI']))
assert len(set(uris))==17 and all(u.startswith('https://') for u in uris)
figure_fonts={}
for name in ['caldero','ciclo','ts_ideal','sensibilidad']:
    figure=PdfReader(ROOT/'figuras'/(name+'.pdf'))
    fonts=figure.pages[0]['/Resources']['/Font'].get_object()
    names=[str(obj.get_object()['/BaseFont']) for obj in fonts.values()]
    assert any('NimbusRomNo9L' in n for n in names), (name,names)
    assert all(any(allowed in n for allowed in ['NimbusRomNo9L','CMR','CMMI','CMSY','CMEX']) for n in names), (name,names)
    figure_fonts[name]=names
font_results=[]
if shutil.which('pdffonts'):
    out=subprocess.run(['pdffonts',str(PDF)],capture_output=True,check=True).stdout.decode('utf-8',errors='replace')
    (ROOT/'build/fuentes_pdf.txt').write_text(out,encoding='utf-8')
    for line in out.splitlines():
        m=re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',line)
        if m:font_results.append(dict(nombre=line.split()[0],incrustada=m[1]=='yes',unicode=m[3]=='yes'))
    assert font_results and all(x['incrustada'] for x in font_results)
report=dict(paginas=10,papel='A4',bytes=PDF.stat().st_size,
            texto_seleccionable=True,caracteres_por_pagina=list(map(len,texts)),
            referencias=len(cited),enlaces_externos_distintos=len(set(uris)),
            palabras_resumen=len(abstract.split()),avisos_latex=0,
            fuentes=font_results,fuentes_figuras=figure_fonts,
            sha256_pdf=hashlib.sha256(PDF.read_bytes()).hexdigest(),
            sha256_texto=hashlib.sha256(text.encode('utf-8')).hexdigest())
(ROOT/'datos/validacion_pdf.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['fuentes','caracteres_por_pagina']},indent=2,ensure_ascii=False))
