"""Contraste IF97 (CoolProp) vs. tablas termodinámicas SQLite de Tablas.KchaParedes.

Uso:
  python scripts/contraste_tablas.py                 # usa datos/tablas_kchaparedes_solution.json
  python scripts/contraste_tablas.py --repo RUTA     # regenera ese JSON con el solver del repositorio
Repositorio: https://github.com/dilmar231gabriel-ops/Tablas.KchaParedes (commit 6b33d48)
"""
from pathlib import Path
import argparse, csv, json, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[1]
SOL = ROOT/'datos'/'tablas_kchaparedes_solution.json'
ap = argparse.ArgumentParser(); ap.add_argument('--repo'); a = ap.parse_args()
if a.repo:
    out = Path(tempfile.mkdtemp())
    subprocess.run([sys.executable, 'thermo.py', 'rankine', '--boiler-bar', '80', '--condenser-bar', '0.1',
                    '--turbine-inlet-c', '480', '--output', str(out)], cwd=a.repo, check=True, capture_output=True)
    shutil.copy2(out/'solution.json', SOL)
tab = json.loads(SOL.read_text(encoding='utf-8'))
res = json.loads((ROOT/'datos'/'resultados.json').read_text(encoding='utf-8'))
st = {e['number']: e for e in tab['final_states']}; cy = tab['cycle']
iff = {i+1: e for i, e in enumerate(res['estados_ideal'])}
def get(d, *keys):
    for k in keys:
        if k in d: return d[k]
    raise KeyError(keys)
rows = [(r'$h_1$ [kJ/kg]', iff[1]['h']/1e3, st[1]['h_kJkg']),
        (r'$h_2$ [kJ/kg]', iff[2]['h']/1e3, st[2]['h_kJkg']),
        (r'$h_3$ [kJ/kg]', iff[3]['h']/1e3, st[3]['h_kJkg']),
        (r'$h_4$ [kJ/kg]', iff[4]['h']/1e3, st[4]['h_kJkg']),
        (r'$x_4$ [--]', iff[4]['x'], st[4]['x']),
        (r'$\eta$ [\%]', 100*res['ideal']['eta'], cy['thermal_efficiency_percent'])]
rows = [(n, a_, b_*100 if n.startswith(r'$\eta') and b_ < 1 else b_) for n, a_, b_ in rows]
with open(ROOT/'datos'/'contraste_tablas.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['magnitud', 'IF97', 'tablas_SQLite', 'diferencia_pct'])
    for n, x, y in rows: w.writerow([n, x, y, 100*(y-x)/x])
lines = [r'\begin{tabular}{lrrr}', r'\toprule', r'Magnitud & IF97 & Tablas & $\Delta$ [\%]\\', r'\midrule']
for n, x, y in rows:
    d = 4 if 'x_4' in n or 's_3' in n else 2
    lines.append(f'{n} & {x:.{d}f} & {y:.{d}f} & {100*(y-x)/x:+.3f} \\\\'.replace('.', ','))
lines += [r'\bottomrule', r'\end{tabular}', '']
(ROOT/'datos'/'tabla_contraste.tex').write_text('\n'.join(lines), encoding='utf-8')
print('\n'.join(lines))
