"""Dibujos técnicos (no a escala) del ciclo y del caldero acuotubular.

Ejecutar: python scripts/esquemas.py   (lo invoca también scripts/modelo.py)
Solo requiere matplotlib, pdfLaTeX y pdftocairo/pdftoppm. No usa CoolProp:
las figuras son esquemas de equipos, no resultados numéricos.
"""
from pathlib import Path
import shutil
import subprocess
import numpy as np
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyArrowPatch, Rectangle, FancyBboxPatch,
                                Circle, Polygon, Ellipse)

ROOT = Path(__file__).resolve().parents[1]
(ROOT/'figuras').mkdir(exist_ok=True)
plt.rcParams.update({'pgf.texsystem': 'pdflatex', 'pgf.rcfonts': False,
    'pgf.preamble': r'\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\renewcommand{\rmdefault}{ptm}',
    'font.family': 'serif', 'font.size': 8})
BLUE, RED, GRAY, STEEL = '#174f78', '#a73927', '#69757d', '#2b2b2b'
WATER, METAL, REFR = '#d6e6f2', '#eef1f3', '#f3e2d9'


def save(fig, name):
    pdf = ROOT/'figuras'/(name+'.pdf')
    fig.savefig(pdf, bbox_inches='tight', pad_inches=0.02)
    plt.close(fig)
    renderer = shutil.which('pdftocairo') or shutil.which('pdftoppm')
    if not renderer:
        raise RuntimeError('Se necesita pdftocairo o pdftoppm para la vista PNG.')
    r = subprocess.run([renderer, '-singlefile', '-png', '-r', '220', str(pdf),
                        str(ROOT/'figuras'/name)], capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr.decode(errors='replace'))


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set(xlim=(0, xmax), ylim=(0, ymax)); ax.set_aspect('equal'); ax.axis('off')
    return fig, ax


def pipe(ax, pts, color=BLUE, lw=1.6, arrow=True, ls='-', z=3):
    pts = np.asarray(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, ls=ls, solid_capstyle='butt', zorder=z)
    if arrow:  # flecha a mitad del tramo más largo
        seg = np.argmax(np.linalg.norm(np.diff(pts, axis=0), axis=1))
        a, b = pts[seg], pts[seg+1]; m = (a+b)/2; d = (b-a)/np.linalg.norm(b-a)*0.12
        ax.add_patch(FancyArrowPatch(m-d, m+d, arrowstyle='-|>', mutation_scale=9,
                                     color=color, lw=0, zorder=z+1))


def arrow(ax, a, b, color=RED, lw=1.2, ms=9, z=4):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=ms, color=color, lw=lw, zorder=z))


def tag(ax, x, y, n):
    ax.add_patch(Circle((x, y), 0.2, fc='white', ec=STEEL, lw=0.8, zorder=6))
    ax.text(x, y, str(n), ha='center', va='center', fontsize=8, fontweight='bold', zorder=7)


def coil(ax, x0, x1, y0, y1, n, color=BLUE, lw=1.0, z=3):
    """Serpentín de n pasos verticales con curvas en U."""
    xs = np.linspace(x0, x1, n); r = (xs[1]-xs[0])/2; pts = []
    for i, x in enumerate(xs):
        ya, yb = (y0+r, y1-r) if i % 2 == 0 else (y1-r, y0+r)
        pts += [(x, ya), (x, yb)]
        if i < n-1:
            c = (x+r, yb); th = np.linspace(np.pi, 0, 12) if i % 2 == 0 else np.linspace(-np.pi, 0, 12)
            pts += list(zip(c[0]+r*np.cos(th), c[1]+r*np.sin(th)))
    pts = np.array(pts); ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, zorder=z)


def drum(ax, x, y, w, h, level=None, z=4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={h/2}',
                                fc=METAL, ec=STEEL, lw=1.2, zorder=z))
    if level is not None:
        yl = y+level*h
        ax.add_patch(FancyBboxPatch((x+0.03, y+0.03), w-0.06, yl-y-0.03,
                     boxstyle=f'round,pad=0,rounding_size={min(h/2-0.03, (yl-y)/2)}',
                     fc=WATER, ec='none', zorder=z+0.1))
        ax.plot([x+0.12, x+w-0.12], [yl, yl], color=BLUE, lw=0.6, zorder=z+0.2)


def flame(ax, x, y, L, H):
    t = np.linspace(0, 2*np.pi, 60)
    px = x+L*(1-np.cos(t))/2; py = y+H/2*np.sin(t)*(1-np.cos(t))/2*1.6
    ax.add_patch(Polygon(np.c_[px, py], fc='#e8833a', ec=RED, lw=0.7, zorder=5))
    ax.add_patch(Polygon(np.c_[x+0.6*L*(1-np.cos(t))/2, y+0.35*H*np.sin(t)*(1-np.cos(t))/2*1.6],
                         fc='#f7d154', ec='none', zorder=6))


def valve(ax, x, y, s=0.16, vertical=True):
    if vertical:
        tri = [[(x-s, y+s), (x+s, y+s), (x, y)], [(x-s, y-s), (x+s, y-s), (x, y)]]
    else:
        tri = [[(x-s, y-s), (x-s, y+s), (x, y)], [(x+s, y-s), (x+s, y+s), (x, y)]]
    for t in tri:
        ax.add_patch(Polygon(t, fc='white', ec=STEEL, lw=0.9, zorder=6))


# ---------------------------------------------------------------- ciclo
fig, ax = canvas(7.1, 2.75, 14.2, 5.5)
# Caldero acuotubular (corte esquemático)
ax.add_patch(Rectangle((1.5, 1.95), 3.6, 3.0, fc=REFR, ec=STEEL, lw=1.3, zorder=1))
ax.add_patch(Rectangle((1.7, 2.15), 3.2, 2.6, fc='white', ec=GRAY, lw=0.6, zorder=1.5))
drum(ax, 2.9, 4.05, 1.9, 0.55, level=0.5)          # domo de vapor
drum(ax, 3.2, 2.3, 1.3, 0.38, level=1.0)           # domo inferior
for xt in np.arange(3.35, 4.45, 0.13):              # haz convectivo
    ax.plot([xt, xt], [2.68, 4.05], color=BLUE, lw=0.8, zorder=3)
for yt in np.arange(2.3, 4.6, 0.16):                 # paredes de agua del hogar
    ax.add_patch(Circle((1.82, yt), 0.055, fc=WATER, ec=BLUE, lw=0.5, zorder=3))
ax.add_patch(Rectangle((1.2, 2.85), 0.5, 0.36, fc=METAL, ec=STEEL, lw=1, zorder=4))  # quemador
flame(ax, 1.75, 3.03, 1.15, 0.55)
coil(ax, 4.55, 4.85, 3.0, 3.85, 3, color=RED, lw=0.9)   # sobrecalentador
ax.add_patch(Rectangle((4.45, 4.95), 0.45, 0.5, fc=METAL, ec=STEEL, lw=1, zorder=2))  # chimenea
arrow(ax, (4.68, 5.05), (4.68, 5.5), GRAY, ms=7)
arrow(ax, (0.1, 3.03), (1.2, 3.03), RED); ax.text(0.05, 3.55, 'Combustible\ny aire', fontsize=7, color=RED, linespacing=0.9)
ax.text(2.9, 5.1, 'Caldero acuotubular', ha='center', fontsize=8, fontweight='bold')
ax.text(0.05, 4.3, r'$\dot Q_{\rm entrada}$', fontsize=8, color=RED, zorder=7)
# Turbina + generador
turb = [(7.0, 3.85), (7.0, 4.35), (8.6, 4.85), (8.6, 3.35)]
ax.add_patch(Polygon(turb, fc=METAL, ec=STEEL, lw=1.3, zorder=4))
for xb in np.linspace(7.3, 8.3, 5):                  # etapas de álabes
    hb = 0.25+0.48*(xb-7.0)/1.6
    ax.plot([xb, xb], [4.1-hb*0.9, 4.1+hb*0.9], color=GRAY, lw=0.6, zorder=5)
ax.plot([6.6, 10.0], [4.1, 4.1], color=STEEL, lw=1.0, ls=(0, (6, 2, 1, 2)), zorder=3)  # eje
ax.add_patch(Circle((10.55, 4.1), 0.55, fc=METAL, ec=STEEL, lw=1.3, zorder=4))
ax.text(10.55, 4.1, 'G', ha='center', va='center', fontsize=11, fontweight='bold', zorder=5)
ax.text(7.8, 5.05, 'Turbina', ha='center', fontsize=8, fontweight='bold')
ax.text(10.55, 3.3, 'Generador', ha='center', fontsize=8, fontweight='bold')
arrow(ax, (11.1, 4.1), (12.2, 4.1), GRAY); ax.text(11.25, 4.25, r'$\dot W_t$', fontsize=8)
# Condensador de superficie (carcasa y tubos)
drum(ax, 6.6, 0.75, 3.4, 1.2)
coil(ax, 7.05, 9.45, 1.0, 1.75, 9, color='#3a86c8', lw=0.8, z=5)
ax.add_patch(Rectangle((7.6, 0.45), 0.8, 0.32, fc=WATER, ec=STEEL, lw=1, zorder=4))  # pozo caliente
pipe(ax, [(9.45, 1.05), (10.5, 1.05), (11.3, 1.05)], color='#3a86c8', lw=1.1)
pipe(ax, [(11.3, 1.7), (10.5, 1.7), (9.45, 1.7)], color='#3a86c8', lw=1.1)
ax.text(11.35, 1.32, 'Agua de\nenfriamiento', fontsize=7, color='#3a86c8', linespacing=0.9, va='center')
ax.text(8.35, 2.15, 'Condensador', ha='left', fontsize=8, fontweight='bold')
ax.text(11.35, 0.45, r'$\dot Q_{\rm salida}$', fontsize=8, color=RED)
# Bomba centrífuga + motor
ax.add_patch(Circle((3.6, 0.95), 0.42, fc=METAL, ec=STEEL, lw=1.3, zorder=4))
ax.add_patch(Polygon([(3.35, 0.72), (3.35, 1.18), (3.88, 0.95)], fc='white', ec=STEEL, lw=0.8, zorder=5))
ax.plot([2.4, 3.18], [0.95, 0.95], color=STEEL, lw=1.0, zorder=3)
ax.add_patch(Circle((2.1, 0.95), 0.32, fc=METAL, ec=STEEL, lw=1.1, zorder=4))
ax.text(2.1, 0.95, 'M', ha='center', va='center', fontsize=8, fontweight='bold', zorder=5)
ax.text(3.6, 0.2, 'Bomba', ha='center', fontsize=8, fontweight='bold')
arrow(ax, (0.9, 0.95), (1.78, 0.95), GRAY); ax.text(0.95, 1.12, r'$\dot W_b$', fontsize=8)
# Tuberías y estados
pipe(ax, [(7.6, 0.45), (7.6, 0.2), (5.0, 0.2), (5.0, 0.95), (4.02, 0.95)])   # 1: pozo -> bomba
pipe(ax, [(3.6, 1.37), (3.6, 1.75), (5.4, 1.75), (5.4, 2.5), (4.5, 2.5)])    # 2: bomba -> domo inferior
pipe(ax, [(4.7, 4.6), (4.7, 4.75), (5.6, 4.75), (5.6, 4.1), (7.0, 4.1)], color=RED)  # 3: vapor -> turbina
pipe(ax, [(8.1, 3.5), (8.1, 1.95)], color=RED)                                      # 4: escape
tag(ax, 5.95, 0.2, 1); tag(ax, 5.4, 2.1, 2); tag(ax, 6.3, 4.1, 3); tag(ax, 8.1, 2.65, 4)
save(fig, 'ciclo')

# --------------------------------------------------------------- caldero
fig, ax = canvas(7.1, 3.05, 14.2, 6.1)
# Envolvente y hogar
ax.add_patch(Rectangle((0.9, 0.55), 9.3, 5.15, fc=REFR, ec=STEEL, lw=1.4, zorder=1))
ax.add_patch(Rectangle((1.1, 0.75), 8.9, 4.75, fc='white', ec='none', zorder=1.2))
for yt in np.arange(0.95, 5.35, 0.2):                # pared de agua (tubos en corte)
    ax.add_patch(Circle((1.22, yt), 0.07, fc=WATER, ec=BLUE, lw=0.5, zorder=3))
for xt in np.arange(1.4, 3.7, 0.2):                  # techo y piso con tubos
    for yy in (5.38, 0.87):
        ax.add_patch(Circle((xt, yy), 0.07, fc=WATER, ec=BLUE, lw=0.5, zorder=3))
ax.add_patch(Rectangle((0.35, 2.3), 0.85, 0.55, fc=METAL, ec=STEEL, lw=1.1, zorder=4))  # quemador
flame(ax, 1.25, 2.58, 2.1, 1.1)
ax.text(2.3, 4.6, 'Hogar', ha='center', fontsize=8, fontweight='bold', color=RED)
# Domos y haz de tubos
drum(ax, 3.9, 4.55, 3.0, 0.9, level=0.5)
drum(ax, 4.3, 0.85, 2.2, 0.6, level=1.0)
for i, xt in enumerate(np.arange(4.45, 6.45, 0.17)):
    ax.plot([xt, xt], [1.45, 4.55], color=BLUE if i > 2 else '#3a86c8', lw=0.9, zorder=3)
for xs in (4.6, 5.1):                                # separadores ciclónicos
    ax.add_patch(Polygon([(xs, 5.25), (xs+0.3, 5.25), (xs+0.15, 4.95)], fc='white', ec=STEEL, lw=0.6, zorder=5))
# Descendente externo
pipe(ax, [(6.9, 4.8), (7.2, 4.8), (7.2, 1.15), (6.5, 1.15)], lw=2.2)
# Deflectores de gases
ax.add_patch(Rectangle((3.75, 0.75), 0.1, 3.3, fc=GRAY, ec='none', zorder=2))
ax.add_patch(Rectangle((7.45, 0.75), 0.1, 3.15, fc=GRAY, ec='none', zorder=2))
# Sobrecalentador y economizador en el paso convectivo
coil(ax, 7.8, 9.7, 3.3, 5.2, 7, color=RED, lw=1.0)
coil(ax, 7.8, 9.7, 0.95, 2.6, 8, color=BLUE, lw=1.0)
# Precalentador de aire tubular y chimenea
ax.add_patch(Rectangle((10.7, 1.5), 1.3, 2.4, fc=METAL, ec=STEEL, lw=1.2, zorder=2))
for xt in np.arange(10.9, 11.95, 0.18):
    ax.plot([xt, xt], [1.6, 3.8], color=GRAY, lw=0.7, zorder=3)
ax.add_patch(Polygon([(12.5, 1.5), (13.2, 1.5), (13.05, 5.9), (12.65, 5.9)], fc=METAL, ec=STEEL, lw=1.2, zorder=2))
# Recorrido de gases (rojo)
for a, b in [((2.7, 3.3), (3.6, 4.2)), ((3.95, 4.3), (7.75, 4.3)), ((9.93, 4.9), (9.93, 1.5)),
             ((10.05, 1.3), (10.65, 1.9)),
             ((12.0, 3.6), (12.6, 3.6)), ((12.85, 4.4), (12.85, 5.6))]:
    arrow(ax, a, b, RED, lw=0.9, ms=7)
ax.text(13.3, 5.5, 'Gases a\nchimenea', fontsize=7, color=RED, linespacing=0.9)
# Aire de combustión (gris)
ax.add_patch(Circle((11.35, 0.55), 0.3, fc=METAL, ec=STEEL, lw=1, zorder=4))
ax.plot([11.2, 11.5], [0.42, 0.68], color=STEEL, lw=0.8, zorder=5); ax.plot([11.2, 11.5], [0.68, 0.42], color=STEEL, lw=0.8, zorder=5)
ax.text(11.75, 0.35, 'Ventilador', fontsize=7)
pipe(ax, [(11.35, 0.85), (11.35, 1.5)], color=GRAY, lw=1.1)
pipe(ax, [(10.7, 3.4), (10.45, 3.4), (10.45, 0.25), (0.15, 0.25), (0.15, 2.58), (0.35, 2.58)], color=GRAY, lw=1.1, ls='--')
ax.text(5.5, 0.05, 'Aire caliente de combustión', fontsize=7, color=GRAY, ha='center')
# Agua y vapor
pipe(ax, [(13.9, 1.1), (10.3, 1.1), (9.7, 1.1)])                       # agua de alimentación (2)
tag(ax, 13.75, 1.1, 2)
pipe(ax, [(7.8, 1.1), (7.62, 1.1), (7.62, 5.55), (6.3, 5.55), (6.3, 5.45)])  # economizador -> domo
pipe(ax, [(4.4, 5.45), (4.4, 5.85), (7.72, 5.85), (7.72, 3.45), (7.8, 3.45)], color=RED)  # vapor saturado -> sobrecalentador
pipe(ax, [(9.7, 5.05), (11.9, 5.05)], color=RED)  # vapor sobrecalentado (3)
tag(ax, 12.1, 5.05, 3)
# Purga
pipe(ax, [(5.4, 0.85), (5.4, 0.45)], lw=1.1, arrow=False); valve(ax, 5.4, 0.55, 0.11)
# Rótulos con guía
def lab(txt, xy, xyt, c=STEEL):
    ax.annotate(txt, xy, xytext=xyt, fontsize=7, color=c, ha='center', va='center', zorder=8,
                arrowprops=dict(arrowstyle='-', color=GRAY, lw=0.5),
                bbox=dict(fc='white', ec='none', pad=0.6, alpha=0.9))
lab('Domo de vapor', (6.0, 5.1), (2.45, 5.95))
lab('Domo inferior', (4.4, 1.1), (2.8, 1.55))
lab('Haz convectivo\n(ascendentes)', (5.6, 3.0), (5.6, 3.05))
lab('Descendente', (7.2, 2.0), (6.6, 2.2))
lab('Pared de agua', (1.22, 4.05), (2.3, 3.95))
lab('Quemador', (0.7, 2.3), (0.75, 1.75))
ax.text(8.75, 3.08, 'Sobrecalentador', fontsize=7, ha='center', va='center', color=RED, zorder=8)
ax.text(8.75, 2.8, 'Economizador', fontsize=7, ha='center', va='center', color=BLUE, zorder=8)
lab('Precalentador\nde aire', (11.35, 3.9), (11.35, 4.25))
lab('Purga', (5.4, 0.55), (6.2, 0.55))
ax.text(12.15, 1.27, 'Agua de alimentación', fontsize=7, color=BLUE, ha='center')
ax.text(11.0, 5.3, 'Vapor a turbina', fontsize=7, color=RED, ha='center')
save(fig, 'caldero')
print('Esquemas generados: figuras/ciclo.pdf, figuras/caldero.pdf')
