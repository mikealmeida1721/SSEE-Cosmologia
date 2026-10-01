"""Perfil de chi2(w_c) en BOSS con logA CLAVADO al valor del CMB.

Es el experimento SIMETRICO del que ya tenemos:

  ya hecho    w_c fijo por algebra, logA libre  -> logA = 2.7636 +- 0.0981
  este        logA fijo al del CMB, w_c libre   -> w_c = ?

Si BOSS con A_s del CMB pide un w_c compatible con 0.119514, entonces la
discrepancia de amplitud NO es de w_c: A_s se movio de veras (o falta
crecimiento). Si en cambio pide un w_c mucho menor, entonces lo que en el
perfil de logA parecia un A_s bajo era w_c disfrazado.

CONTROL (R53): el mismo perfil con logA al valor que BOSS mismo prefiere
(2.7636). Ahi w_c debe volver a ~la identidad; si no vuelve, el perfil esta
midiendo el borde de la parametrizacion, no el dato.
"""
# ORIGEN-VALOR: 0.0981 — sigma del logA viejo de BOSS, results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json (0.098131)
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src/p06_growth')

import boss_lpt_R1R2 as B

LOGA_CMB = 3.0438          # A_s medido por SSEE sobre Planck crudo
LOGA_BOSS = 2.7636         # control: el que BOSS mismo prefiere
WB = B.COSMO['SSEE']['ombh2']
H = B.COSMO['SSEE']['h']
WNU = B.MNU / 93.14
WC_ID = 0.119514           # R66-OK: centro de la rejilla del barrido, no una
# constante que entre en el calculo. Redondeado a proposito para que la
# rejilla siga siendo la de la corrida ya hecha (ver perfil_wc_cmb.py).

ESC = np.array([1.0, 1.0, 1.0])
P0 = np.array([2.0, 0.0, 0.0])
COTAS = [(0.5, 5.0), (-10.0, 10.0), (-10.0, 10.0)]


def sets_con(wc):
    """build() con un solo modelo, con este w_c."""
    Om = (WB + wc + WNU) / H ** 2
    B.COSMO.clear()
    B.COSMO['SSEE'] = dict(
        Om=Om, h=H, ombh2=WB,
        ns=B.S.N_S, w0=B.S.W0, wa=B.S.WA)
    return B.build(), Om


def ajusta(sets, logA):
    """chi2 total marginalizado, optimizando (b1,b2,bs) por conjunto."""
    tot, ths = 0.0, []
    for st in sets:
        u, best = P0.copy(), np.inf
        for _ in range(3):
            rr = minimize(
                lambda v: B.chi2_marg_set(st, 'SSEE', logA,
                                          v * ESC)[0],
                u, method='Nelder-Mead', bounds=COTAS,
                options=dict(maxiter=3000, xatol=1e-4,
                             fatol=1e-4))
            if rr.fun < best:
                best, u = float(rr.fun), rr.x
        tot += best
        ths.append(u * ESC)
    return tot, ths


def perfil(rej, logA, etiq):
    print(f'\n=== perfil w_c  |  logA fijo = {logA:.4f}'
          f'  ({etiq}) ===', flush=True)
    print(' w_c        Om        chi2', flush=True)
    out = []
    for wc in rej:
        t0 = time.time()
        sets, Om = sets_con(wc)
        c, _ = ajusta(sets, logA)
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
                   referencia=float(WC_ID), dist_sigma=float(abs(wc0 - WC_ID) / sg))
        print(f'  parabola: w_c = {wc0:.6f} +- {sg:.6f}',
              flush=True)
        print(f'  identidad {WC_ID:.6f}  ->  '
              f'{abs(wc0-WC_ID)/sg:.2f} sigma', flush=True)
    return res


if __name__ == '__main__':
    os.environ['OMP_NUM_THREADS'] = '1'
    rej = np.linspace(0.090, 0.155, 9)
    import json
    from procedencia import con_acta
    r_cmb = perfil(rej, LOGA_CMB, 'A_s del CMB')
    r_boss = perfil(rej, LOGA_BOSS, 'CONTROL: A_s de BOSS')
    json.dump(con_acta(dict(fecha=time.strftime('%Y-%m-%d'), amplitud_cmb=r_cmb, control_amplitud_boss=r_boss),
                       __file__), open('/home/mike/Proyectos/SSEE/results/logs/perfil_wc_boss.json', 'w'), indent=1)
