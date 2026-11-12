"""Crea el proyecto portable sin cachés, renders de QA ni PDFs ajenos."""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'Proyecto_LaTeX_Calderos_Acuotubulares.zip'
files={'main.tex','referencias.bib','IEEEtran.cls','IEEEtran.bst',
       'IEEEtran_README.txt','LPPL-1.3c.txt','requirements.txt','README.md',
       'latexmkrc','Verificacion_y_sustentacion.md',
       'Grupo1_Calderos_Acuotubulares.pdf'}
dirs={'scripts','datos','figuras','insumos'}
selected=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts:continue
    rel=p.relative_to(ROOT)
    if (len(rel.parts)==1 and rel.name in files) or rel.parts[0] in dirs or rel.as_posix()=='fuentes/Registro_de_fuentes.md':
        selected.append(p)
assert all((ROOT/n).is_file() for n in files)
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in selected:z.write(p,(Path('Proyecto_Calderos')/p.relative_to(ROOT)).as_posix())
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
print(f'{OUT.name}: {len(selected)} archivos, {OUT.stat().st_size} bytes; CRC correcto.')
