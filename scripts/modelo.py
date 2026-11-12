"""Caso Rankine reproducible. Todas las propiedades se calculan con IF97::Water.

Ejecutar desde cualquier directorio: python scripts/modelo.py
Unidades internas: Pa, K, J/kg, J/(kg K), m3/kg. Salidas: unidades SI indicadas.
Las inversiones monofásicas usan bisección de las ecuaciones directas para
evitar la pequeña inconsistencia de las correlaciones inversas de IF97.
"""
from pathlib import Path
import csv
import json
import platform
import shutil
import subprocess
import sys
import numpy as np
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch
import CoolProp
from CoolProp.CoolProp import PropsSI

ROOT = Path(__file__).resolve().parents[1]
for folder in ('datos', 'figuras'):
    (ROOT/folder).mkdir(exist_ok=True)
F = 'IF97::Water'
PB, PC, T3, MDOT = 8e6, 1e4, 753.15, 10.0
ETA_T, ETA_P, ETA_B, ETA_E = .85, .80, .90, .97
PCI = 50000.0  # kJ/kg; supuesto nominal de metano, no análisis de combustible

def pq(p, x):
    return dict(p=p, T=PropsSI('T','P',p,'Q',x,F),
                h=PropsSI('H','P',p,'Q',x,F),
                s=PropsSI('S','P',p,'Q',x,F),
                v=1/PropsSI('D','P',p,'Q',x,F), x=float(x),
                fase='Líquido saturado' if x == 0 else
                     'Vapor saturado' if x == 1 else 'Mezcla líquido-vapor')

def pt(p, T):
    ts = PropsSI('T','P',p,'Q',0,F) if p < 22.064e6 else 647.096
    return dict(p=p,T=T,h=PropsSI('H','P',p,'T',T,F),
                s=PropsSI('S','P',p,'T',T,F),
                v=1/PropsSI('D','P',p,'T',T,F),x=None,
                fase='Líquido comprimido' if T < ts else 'Vapor sobrecalentado')

def inverse(p, key, target):
    sf, sg = pq(p,0), pq(p,1)
    if sf[key] <= target <= sg[key]:
        return pq(p,(target-sf[key])/(sg[key]-sf[key]))
    lo, hi = ((273.15, sf['T']-1e-7) if target < sf[key]
              else (sg['T']+1e-7,1073.15))
    for _ in range(85):
        mid=(lo+hi)/2
        if pt(p,mid)[key] < target: lo=mid
        else: hi=mid
    return pt(p,(lo+hi)/2)

def cycle(pb=PB, pc=PC, t3=T3, eta_t=1.0, eta_p=1.0):
    a=pq(pc,0)
    bs=inverse(pb,'s',a['s'])
    b=bs if eta_p == 1 else inverse(pb,'h',a['h']+(bs['h']-a['h'])/eta_p)
    c=pt(pb,t3)
    ds=inverse(pc,'s',c['s'])
    d=ds if eta_t == 1 else inverse(pc,'h',c['h']-eta_t*(c['h']-ds['h']))
    wb=(b['h']-a['h'])/1000
    wt=(c['h']-d['h'])/1000
    qi=(c['h']-b['h'])/1000
    qo=(d['h']-a['h'])/1000
    wn=wt-wb
    result=dict(wb=wb,wt=wt,qi=qi,qo=qo,wn=wn,eta=wn/qi,x4=d['x'],
                Wb=MDOT*wb/1000,Wt=MDOT*wt/1000,Wn=MDOT*wn/1000,
                Qin=MDOT*qi/1000,Qout=MDOT*qo/1000,
                residual=qi-qo-wn, bwr=wb/wt, steam_rate=3600/wn,
                fuel=MDOT*qi/(ETA_B*PCI),
                fuelMW=MDOT*qi/ETA_B/1000,
                eta_fuel=ETA_B*wn/qi,
                eta_electric=ETA_E*ETA_B*wn/qi,
                electricMW=ETA_E*MDOT*wn/1000)
    return [a,b,c,d],result

def write_csv(name, rows):
    with (ROOT/'datos'/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

states, base=cycle()
actual, real=cycle(eta_t=ETA_T,eta_p=ETA_P)
rows=[]
for model, arr in [('ideal',states),('no_ideal',actual)]:
    for i,a in enumerate(arr,1):
        rows.append(dict(modelo=model,estado=i,P_MPa=a['p']/1e6,T_C=a['T']-273.15,
                         h_kJ_kg=a['h']/1000,s_kJ_kgK=a['s']/1000,
                         v_m3_kg=a['v'],x=a['x'],fase=a['fase']))
write_csv('estados.csv',rows)
write_csv('balances.csv',[dict(modelo='ideal',**base),dict(modelo='no_ideal',**real)])

sweeps={}
for tag,vals,arg in [('temperatura',[400,440,480,520,560],'t3'),
                     ('condensador',[5,7.5,10,15,20],'pc'),
                     ('caldero',[4,6,8,10,12],'pb')]:
    data=[]
    for val in vals:
        v=val+273.15 if arg=='t3' else val*(1000 if arg=='pc' else 1e6)
        for kind,et,ep in [('ideal',1,1),('no_ideal',ETA_T,ETA_P)]:
            _,r=cycle(**{arg:v},eta_t=et,eta_p=ep)
            data.append(dict(entrada=val,modelo=kind,eta_pct=r['eta']*100,
                             wnet_kJ_kg=r['wn'],x4=r['x4']))
    sweeps[tag]=data;write_csv('sensibilidad_'+tag+'.csv',data)

# Verificación independiente frente a valores publicados de la región 1,
# tabla 5 de IAPWS R7-97(2012). La tolerancia contempla el redondeo publicado.
checks=[]
for T,p,h,s,v in [(300,3e6,115.331273,.392294792,.00100215168),
                  (300,80e6,184.142828,.368563852,.000971180894),
                  (500,3e6,975.542239,2.58041912,.00120241800)]:
    z=pt(p,T)
    errors={k:abs(z[k]/scale-ref)/abs(ref) for k,scale,ref in
            [('h',1000,h),('s',1000,s),('v',1,v)]}
    assert max(errors.values()) < 1e-7, errors
    checks.append(dict(T_K=T,P_MPa=p/1e6,**errors))
for arr,r in [(states,base),(actual,real)]:
    assert abs(r['residual']) < 1e-9
    assert 0 < r['eta'] < 1 and 0 < r['x4'] < 1
    assert abs(arr[0]['p']-arr[3]['p']) < 1e-6
assert abs(states[1]['s']-states[0]['s']) < 1e-7
assert abs(states[3]['s']-states[2]['s']) < 1e-7
assert actual[1]['s'] > actual[0]['s'] and actual[3]['s'] > actual[2]['s']
write_csv('verificacion_IF97.csv',checks)

hf,hg=pq(PB,0)['h']/1000,pq(PB,1)['h']/1000
extras=dict(TsatB=pq(PB,0)['T']-273.15, hfB=hf,hgB=hg,
            sfC=pq(PC,0)['s']/1000,sgC=pq(PC,1)['s']/1000,
            hfC=pq(PC,0)['h']/1000,hgC=pq(PC,1)['h']/1000,
            vfC=pq(PC,0)['v'],vgC=pq(PC,1)['v'],
            eco=hf-states[1]['h']/1000,evap=hg-hf,sup=states[2]['h']/1000-hg,
            pump_approx=states[0]['v']*(PB-PC)/1000,
            coolwater=base['Qout']*1000/(4.18*10),
            rejected_pct=100*(1-base['eta']),
            eta_drop=100*(base['eta']-real['eta']),
            boilerlossMW=base['fuelMW']-base['Qin'],
            boilerloss_realMW=real['fuelMW']-real['Qin'],
            bwpct=100*base['bwr'], humidity=100*(1-base['x4']),
            Tmean=base['qi']/((states[2]['s']-states[1]['s'])/1000),
            carnot=100*(1-states[0]['T']/states[2]['T']),
            purge_extra=.02*MDOT*(hf-states[1]['h']/1000)/1000)
macros={}
for prefix,rr in [('I',base),('R',real),('E',extras)]:
    for k,v in rr.items():
        macros[prefix+k]=v
for prefix,arr in [('I',states),('R',actual)]:
    for i,a in enumerate(arr,1):
        for k in ['T','h','s','v','x']:
            if a[k] is not None:
                macros[f'{prefix}{k}{i}']=(a[k]-273.15 if k=='T' else
                                          a[k]/1000 if k in ['h','s'] else a[k])
macros.update(Ietapct=100*base['eta'],Retapct=100*real['eta'],
              Ietafuelpct=100*base['eta_fuel'],Retafuelpct=100*real['eta_fuel'],
              Ietaelecpct=100*base['eta_electric'],Retaelecpct=100*real['eta_electric'])
for tag,short in [('temperatura','T'),('condensador','C'),('caldero','B')]:
    rr=[a for a in sweeps[tag] if a['modelo']=='ideal']
    for end,a in [('lo',rr[0]),('hi',rr[-1])]:
        for key,col in [('eta','eta_pct'),('wn','wnet_kJ_kg'),('x','x4')]:
            macros['S'+short+end+key]=a[col]
    macros['S'+short+'hixR']=sweeps[tag][-1]['x4']
# Reproducción de una referencia docente a condiciones idénticas a las suyas.
_,mit=cycle(pb=3e6,pc=7384,t3=733.15)
macros.update(Metapct=100*mit['eta'],Mx=mit['x4'])
write_csv('comparacion_MIT.csv',[dict(pb_MPa=3,pc_kPa=7.384,T3_C=460,
    eta_IF97_pct=mit['eta']*100,eta_referencia_pct=35.9,x4_IF97=mit['x4'],
    x4_referencia=.851,fuente='Carmichael, Rankine cycle, MIT OCW, PDF 24-10-2005')])
lines=['% Generado por scripts/modelo.py. No editar cifras.']
for k,v in macros.items():
    digits=5 if k.endswith(('s1','s2','s3','s4')) or k in ('EsfC','EsgC','Epurge_extra') else 6 if 'v'==k[1:2] or k.endswith('fuel') else 4 if 'x'==k[1:2] or k.endswith(('x','xR')) else 2
    formatted=f'{v:.{digits}f}'.replace('.','{,}')
    lines.append(r'\expandafter\def\csname val'+k+r'\endcsname{'+formatted+r'}')
for k,rr in [('Iresidual',base),('Rresidual',real)]:
    mantissa,exponent=f"{rr['residual']:.2e}".split('e')
    value=mantissa.replace('.','{,}')+r'\times10^{'+str(int(exponent))+'}'
    lines.append(r'\expandafter\def\csname val'+k+r'\endcsname{'+value+r'}')
lines.append(r'\newcommand{\CPversion}{'+CoolProp.__version__+'}')
(ROOT/'datos'/'valores.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def tex_states(arr):
    return '\n'.join(f"{i} & {a['p']/1e6:.3f} & {a['T']-273.15:.2f} & {a['h']/1000:.2f} & {a['s']/1000:.5f} & {a['v']:.6f} & "+('No aplica' if a['x'] is None else f"{a['x']:.4f}")+f" & {a['fase']} \\\\" for i,a in enumerate(arr,1)).replace('.',',')
state_header = r'''\begin{tabular}{crrrrrlp{.21\textwidth}}
\toprule
Estado & $p$ [MPa] & $T$ [$^\circ$C] & $h$ [kJ/kg] & $s$ [kJ/(kg K)] & $v$ [m$^3$/kg] & $x$ [--] & Fase\\
\midrule
'''
table_end = '\n'+r'\bottomrule'+'\n'+r'\end{tabular}'+'\n'
(ROOT/'datos'/'tabla_estados.tex').write_text(state_header+tex_states(states)+table_end,encoding='utf-8')
(ROOT/'datos'/'tabla_estados_real.tex').write_text(state_header+tex_states(actual)+table_end,encoding='utf-8')
for tag,data in sweeps.items():
    tx=[]
    for i in range(0,len(data),2):
        a,b=data[i:i+2]
        tx.append(f"{a['entrada']:g} & {a['eta_pct']:.2f} & {a['wnet_kJ_kg']:.2f} & {a['x4']:.4f} & {b['eta_pct']:.2f} & {b['wnet_kJ_kg']:.2f} & {b['x4']:.4f} \\\\")
    label={'temperatura':r'$T_3$ [$^\circ$C]', 'condensador':r'$p_c$ [kPa]', 'caldero':r'$p_b$ [MPa]'}[tag]
    header = r'''\begin{tabular}{rrrrrrr}
\toprule
& \multicolumn{3}{c}{Ciclo ideal} & \multicolumn{3}{c}{Variante no ideal}\\
'''+label+r''' & $\eta$ [\%] & $w_{\rm neto}$ [kJ/kg] & $x_4$ & $\eta$ [\%] & $w_{\rm neto}$ [kJ/kg] & $x_4$\\
\midrule
'''
    (ROOT/'datos'/f'tabla_{tag}.tex').write_text(header+'\n'.join(tx).replace('.',',')+table_end,encoding='utf-8')
    small_header = r'''\begin{tabular}{rrrr}
\toprule
'''+label+r''' & $\eta$ [\%] & $w_{\rm neto}$ [kJ/kg] & $x_4$\\
\midrule
'''
    small_rows=[f"{a['entrada']:g} & {a['eta_pct']:.2f} & {a['wnet_kJ_kg']:.2f} & {a['x4']:.4f} \\\\" for a in data if a['modelo']=='ideal']
    (ROOT/'datos'/f'tabla_{tag}_breve.tex').write_text(small_header+'\n'.join(small_rows).replace('.',',')+table_end,encoding='utf-8')

# Los rótulos se componen con el mismo pdfLaTeX y la misma familia ptm
# (Times/Nimbus Roman) de IEEEtran. La matemática conserva Computer Modern,
# como el cuerpo del artículo. No se sustituyen las fuentes por una sans serif.
plt.rcParams.update({'pgf.texsystem':'pdflatex','pgf.rcfonts':False,
    'pgf.preamble':r'\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\renewcommand{\rmdefault}{ptm}',
    'font.family':'serif','font.size':9,'axes.labelsize':9,
    'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8,
    'axes.spines.top':False,'axes.spines.right':False})
BLUE,RED,GRAY = '#174f78','#a73927','#69757d'
def save(fig,name):
    pdf=ROOT/'figuras'/(name+'.pdf')
    fig.savefig(pdf,bbox_inches='tight')
    plt.close(fig)
    renderer=shutil.which('pdftocairo') or shutil.which('pdftoppm')
    if not renderer:
        raise RuntimeError('Se necesita pdftocairo o pdftoppm para generar la vista PNG del PDF LaTeX.')
    result=subprocess.run([renderer,'-singlefile','-png','-r','220',str(pdf),
                           str(ROOT/'figuras'/name)],capture_output=True)
    if result.returncode:
        raise RuntimeError(f'No se pudo renderizar {name}: '+result.stderr.decode(errors='replace'))
def arrow(ax,xy1,xy2,color=BLUE,style='-|>',**kw):
    ax.add_patch(FancyArrowPatch(xy1,xy2,arrowstyle=style,mutation_scale=9,
                                linewidth=1.1,color=color,**kw))

# T-s: trayectorias calculadas, no interpolación entre estados arbitrarios.
fig,ax=plt.subplots(figsize=(3.55,3.0))
temps=np.linspace(278.15,647.05,420)
for x in [0,1]:
    ss=[PropsSI('S','T',t,'Q',x,F)/1000 for t in temps]
    ax.plot(ss,temps-273.15,color=GRAY,lw=.9)
paths=[]
paths.append([inverse(float(p),'s',states[0]['s']) for p in np.geomspace(PC,PB,90)])
ts=pq(PB,0)['T']
paths.append([pt(PB,float(t)) for t in np.linspace(states[1]['T'],ts-1e-5,100)]
             +[pq(PB,float(x)) for x in np.linspace(0,1,90)]
             +[pt(PB,float(t)) for t in np.linspace(ts+1e-5,T3,100)])
paths.append([inverse(float(p),'s',states[2]['s']) for p in np.geomspace(PB,PC,180)])
paths.append([pq(PC,float(x)) for x in np.linspace(states[3]['x'],0,100)])
path_rows=[]
for i,path in enumerate(paths):
    xx=np.array([a['s']/1000 for a in path]);yy=np.array([a['T']-273.15 for a in path])
    ax.plot(xx,yy,color=BLUE,lw=1.5)
    j=int(len(path)*(.65 if i==1 else .5))
    arrow(ax,(xx[max(0,j-3)],yy[max(0,j-3)]),(xx[min(len(path)-1,j+3)],yy[min(len(path)-1,j+3)]))
    path_rows.extend(dict(proceso=f'{i+1}-{(i+1)%4+1}',s_kJ_kgK=a['s']/1000,T_C=a['T']-273.15,P_MPa=a['p']/1e6) for a in path)
for p in [1e5,1e6]:
    tt=PropsSI('T','P',p,'Q',0,F)
    xs=[pq(p,0)['s']/1000,pq(p,1)['s']/1000]
    ax.plot(xs,[tt-273.15]*2,ls=':',lw=.7,color=GRAY)
    # Las isóbaras se rotulan en espacio libre dentro de la campana, sin
    # atravesar la expansión ni la curva de saturación.
    ax.annotate(f'{p/1e6:g}'.replace('.',',')+' MPa',(4.1,tt-273.15),
                xytext=(0,5),textcoords='offset points',ha='center',
                fontsize=8,color=GRAY)
for i,a in enumerate(states,1):
    x,y=a['s']/1000,a['T']-273.15
    ax.plot(x,y,'o',ms=3,color=BLUE)
    offset={1:(-7,2),2:(-7,18),3:(6,2),4:(7,-7)}[i]
    ax.annotate(str(i),(x,y),xytext=offset,textcoords='offset points',
                fontsize=9,fontweight='bold',va='center',ha='right' if i==1 else 'left',
                bbox=dict(facecolor='white',edgecolor='none',pad=.3),
                arrowprops=dict(arrowstyle='-',color=GRAY,lw=.55) if i==2 else None)
ax.text(3.35,310,'8 MPa',fontsize=8,color=BLUE)
ax.text(2.65,20,'0,010 MPa',fontsize=8,color=BLUE)
ax.set(xlim=(0,9.0),ylim=(0,535),xlabel=r'Entropía específica $s$ [kJ/(kg K)]',ylabel=r'Temperatura $T$ [$^\circ$C]')
ax.grid(alpha=.18);fig.tight_layout();save(fig,'ts_ideal')
write_csv('trayectorias_Ts.csv',path_rows)

# Los dibujos técnicos del ciclo y del caldero están en scripts/esquemas.py.
subprocess.run([sys.executable,str(ROOT/'scripts'/'esquemas.py')],check=True)

# Sensibilidad determinista.
fig,axs=plt.subplots(1,3,figsize=(7.1,2.45))
for ax,tag,lab in zip(axs,sweeps,[r'Turbina: $T_3$ [$^\circ$C]',r'Condensador: $p_c$ [kPa]',r'Caldero: $p_b$ [MPa]']):
    for kind,col,ls in [('ideal',BLUE,'-'),('no_ideal',RED,'--')]:
        d=[a for a in sweeps[tag] if a['modelo']==kind]
        ax.plot([a['entrada'] for a in d],[a['eta_pct'] for a in d],marker='o',ms=3,lw=1.2,c=col,ls=ls,label='Ideal' if kind=='ideal' else 'No ideal')
    ax.set_xlabel(lab);ax.grid(alpha=.2)
axs[0].set_ylabel('Eficiencia del ciclo [%]');axs[0].legend(loc='best');fig.tight_layout();save(fig,'sensibilidad')

report=dict(entradas=dict(pb_Pa=PB,pc_Pa=PC,t3_K=T3,mdot_kg_s=MDOT,
    eta_t=ETA_T,eta_p=ETA_P,eta_caldero=ETA_B,eta_conversion=ETA_E,PCI_kJ_kg=PCI),
    ideal=base,no_ideal=real,estados_ideal=states,estados_no_ideal=actual,
    adicionales=extras,verificacion=checks,
    versiones=dict(python=platform.python_version(),CoolProp=CoolProp.__version__,
                   numpy=np.__version__,matplotlib=matplotlib.__version__))
(ROOT/'datos'/'resultados.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(dict(ideal=base,no_ideal=real,adicionales=extras,versiones=report['versiones']),indent=2))

subprocess.run([sys.executable,str(ROOT/'scripts'/'contraste_tablas.py')],check=True)
