"""Regenera los datos y compila con el pdfLaTeX/BibTeX instalado en la máquina.

No instala ni sustituye la distribución TeX. Si latexmk y Perl están disponibles,
también puede usarse el comando alternativo del README.
"""
from pathlib import Path
import argparse
import re
import shutil
import subprocess
import sys
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = 'Grupo1_Calderos_Acuotubulares.pdf'

def run(args, logfile):
    result = subprocess.run(args,cwd=ROOT,capture_output=True)
    (ROOT/'build'/logfile).write_bytes(result.stdout+result.stderr)
    if result.returncode:
        raise RuntimeError(f'Fallo de {args[0]}; revisar build/{logfile}')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--sin-modelo',action='store_true',help='Compilar usando datos y figuras ya incluidos')
    opts=ap.parse_args()
    (ROOT/'build').mkdir(exist_ok=True)
    for exe in ['pdflatex','bibtex']:
        if not shutil.which(exe):raise RuntimeError(f'{exe} no aparece en PATH')
    if not opts.sin_modelo:run([sys.executable,'scripts/modelo.py'],'modelo_salida.txt')
    tex=['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
         '-output-directory=build','main.tex']
    run(tex,'compilacion_1.txt')
    run(['bibtex','build/main'],'bibtex_salida.txt')
    run(tex,'compilacion_2.txt')
    run(tex,'compilacion_3.txt')
    log=(ROOT/'build/main.log').read_text(encoding='utf-8',errors='replace')
    forbidden=[r'Overfull \\hbox',r'Overfull \\vbox',r'Missing character:',
               r'LaTeX Warning:.*undefined',r'There were undefined references',
               r'Label\(s\) may have changed',r'Fatal error']
    for pat in forbidden:
        if re.search(pat,log):raise RuntimeError(f'Control tipográfico no superado: {pat}')
    pdf=ROOT/'build/main.pdf';reader=PdfReader(pdf)
    if len(reader.pages)!=10:raise RuntimeError(f'Se esperan 10 páginas y hay {len(reader.pages)}')
    for i,p in enumerate(reader.pages,1):
        if len(p.extract_text() or '')<100:raise RuntimeError(f'Página {i} vacía o sin texto seleccionable')
    if pdf.stat().st_size>=100_000_000:raise RuntimeError('El PDF supera 100 MB')
    shutil.copy2(pdf,ROOT/OUTPUT)
    print(f'Correcto: {OUTPUT}, 10 páginas, {pdf.stat().st_size} bytes.')

if __name__=='__main__':main()
