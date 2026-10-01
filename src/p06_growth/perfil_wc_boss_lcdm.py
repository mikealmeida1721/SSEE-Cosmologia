"""Gemelo LCDM de perfil_wc_boss.py — el control del OTRO lado (R53).

El perfil en SSEE (2026-09-08) dio esto: al clavar la amplitud del CMB, BOSS
pide w_c = 0.114108 +/- 0.003099, y al dejarle su propia amplitud vuelve a la
identidad algebraica (0.117524, 0.51 sigma). Conclusion: la discrepancia esta
en la AMPLITUD, no en w_c.

Pero esa conclusion todavia no distingue dos causas:

  (a) es una propiedad del DATO — BOSS quiere menos amplitud, y punto
  (b) es una propiedad de SSEE — su fondo algebraico la fabrica

Este script decide entre las dos. Corre EXACTAMENTE el mismo perfil con el
fondo de LCDM. Si LCDM tambien desplaza su w_c hacia abajo al forzarle la
amplitud de Planck, la causa es (a) y ningun modelo la fabrica. Si LCDM se
queda quieto y solo SSEE se mueve, la causa es (b) y el sospechoso es el
fondo algebraico.

Es la misma logica que la celda `lcdmfijo` de KiDS: igualar la RIGIDEZ, no la
libertad.

CONTROL (R53): igual que el gemelo, el segundo perfil va a la amplitud que
LCDM mismo prefiere en BOSS (logA = 2.7898, medido en R1/R2). Ahi w_c debe
volver hacia su valor de Planck; si no vuelve, el perfil mide el borde de la
parametrizacion y no el dato.
"""
# ORIGEN-VALOR: 0.003099 — sigma de w_c del perfil BOSS, results/logs/perfil_wc_boss.log
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src/p06_growth')

import boss_lpt_R1R2 as B

# logA de Planck para LCDM: del ajuste conjunto del 2026-09-08
# (results/logs/cmb_ajuste_conjunto_wc_ns.json, bloque LCDM).
LOGA_CMB = 3.0453
# logA que LCDM mismo prefiere en BOSS: medido en R1/R2
# (results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json, lcdm/logA).
LOGA_BOSS = 2.7898

WB = 0.02237          # Planck 2018 LCDM
H = 0.6736            # Planck 2018 LCDM
WNU = B.MNU / 93.14
WC_REF = 0.1200       # w_c de Planck para LCDM — la referencia de este perfil

ESC = np.array([1.0, 1.0, 1.0])
P0 = np.array([2.0, 0.0, 0.0])
COTAS = [(0.5, 5.0), (-10.0, 10.0), (-10.0, 10.0)]


def sets_con(wc):
    """build() con un solo modelo LCDM, con este w_c."""
    Om = (WB + wc + WNU) / H ** 2
    B.COSMO.clear()
    B.COSMO['LCDM'] = dict(
        Om=Om, h=H, ombh2=WB,
        ns=0.9649, w0=-1.0, wa=0.0)
    return B.build(), Om


def ajusta(sets, logA):
    tot = 0.0
    for st in sets:
        u, best = P0.copy(), np.inf
        for _ in range(3):
            rr = minimize(
                lambda v: B.chi2_marg_set(st, 'LCDM', logA,
                                          v * ESC)[0],
                u, method='Nelder-Mead', bounds=COTAS,
                options=dict(maxiter=3000, xatol=1e-4,
                             fatol=1e-4))
            if rr.fun < best:
                best, u = float(rr.fun), rr.x
        tot += best
    return tot


def perfil(rej, logA, etiq):
    print(f'\n=== perfil w_c LCDM  |  logA fijo = {logA:.4f}'
          f'  ({etiq}) ===', flush=True)
    print(' w_c        Om        chi2', flush=True)
    out = []
    for wc in rej:
        t0 = time.time()
        sets, Om = sets_con(wc)
        c = ajusta(sets, logA)
        out.append(c)
        print(f'{wc:.6f}  {Om:.6f}  {c:10.3f}'
              f'   [{time.time()-t0:.0f}s]', flush=True)
    a = np.asarray(out)
    i = int(np.argmin(a))
    res = dict(logA=float(logA), etiqueta=etiq, w_c=[float(x) for x in rej],
               chi2=[float(x) for x in a], w_c_min_rejilla=float(rej[i]), chi2_min=float(a[i]))
    print(f'  minimo en w_c = {rej[i]:.6f}'
          f'   chi2 = {a[i]:.3f}', flush=True)
    if 0 < i < len(rej) - 1:
        cf = np.polyfit(rej[i - 1:i + 2], a[i - 1:i + 2], 2)
        wc0 = -cf[1] / (2 * cf[0])
        sg = np.sqrt(1.0 / cf[0]) if cf[0] > 0 else np.nan
        res.update(w_c_parabola=float(wc0), sigma_parabola=float(sg),
                   referencia=float(WC_REF), dist_sigma=float(abs(wc0 - WC_REF) / sg))
        print(f'  parabola: w_c = {wc0:.6f} +- {sg:.6f}',
              flush=True)
        print(f'  Planck LCDM {WC_REF:.6f}  ->  '
              f'{abs(wc0-WC_REF)/sg:.2f} sigma', flush=True)
    else:
        print('  AVISO: el minimo cae en un EXTREMO de la rejilla; '
              'no se ajusta parabola y el perfil no concluye', flush=True)
    return res


if __name__ == '__main__':
    os.environ['OMP_NUM_THREADS'] = '1'
    rej = np.linspace(0.090, 0.155, 9)
    import json
    from procedencia import con_acta
    r_cmb = perfil(rej, LOGA_CMB, 'A_s de Planck')
    r_boss = perfil(rej, LOGA_BOSS, 'CONTROL: A_s de BOSS')
    json.dump(con_acta(dict(fecha=time.strftime('%Y-%m-%d'), amplitud_cmb=r_cmb, control_amplitud_boss=r_boss),
                       __file__), open('/home/mike/Proyectos/SSEE/results/logs/perfil_wc_boss_lcdm.json', 'w'), indent=1)
