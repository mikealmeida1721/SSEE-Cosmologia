#!/usr/bin/env python3
"""
CONTROL NEGATIVO de la maquinaria de BOSS: reproducir el resultado publicado.

La pregunta que responde: mi lectura + ventana + Alcock-Paczynski + Kaiser,
puesta a hacer lo MISMO que hizo Beutler, ¿devuelve lo mismo que el publico?

Beutler no fija la tasa de crecimiento: la deja libre y deja que el dato la
ponga. Aqui se hace igual. Si el resultado cae sobre el consenso de BOSS DR12
(Alam et al. 2017), la maquinaria esta sana y la unica limitacion conocida es la
formula de Kaiser. Si no cae, el error es de la maquinaria y todo lo anterior se
retira.

Reparametrizacion (la que hace identificable el problema): con
    P(k,mu) = (b1 + f mu^2)^2 P_lin(k | A_s)
y P_lin proporcional a A_s, se puede absorber la amplitud en los dos terminos,
    B = b1 * sigma8   ,   F = f * sigma8
de modo que lo que el dato mide directamente es (B, F) y NO (b1, f, A_s) por
separado. F es exactamente el f*sigma8 que publica BOSS.

Libres por bin de z: B_NGC, B_SGC, F (compartida: misma cosmologia, mismo z),
sig_v_NGC, sig_v_SGC  ->  5 por bin, 15 en total.
"""
import json
import sys

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src/p06_growth')
import boss_fit as B
import boss_rsd_model as M

np.seterr(all='ignore')

KMAX = float(sys.argv[1]) if len(sys.argv) > 1 else 0.08
OUT = '/home/mike/Proyectos/SSEE/results/logs/growth_2026-07'

# Consenso publicado BOSS DR12 (Alam et al. 2017, tabla 7) — la vara del control
CONSENSO = {0.38: (0.497, 0.045), 0.51: (0.458, 0.038), 0.61: (0.436, 0.034)}


def predict_BF(st, cam, cos, Bv, Fv, sv):
    """multipolos con (b1*sigma8, f*sigma8) en vez de (b1, f, A_s)."""
    c = cam[st['z']]
    a_par, a_per = M.alphas(st['z'], cos['Om'], cos['w0'], cos['wa'])
    s8 = c['sigma8']                       # sigma8 de la plantilla, A_s = AS_REF
    P0, P2, P4 = M.multipoles(M.K_MODEL, c['plin'], Fv / s8, Bv / s8, sv,
                              a_par, a_per)
    ks, q0, q2, q4 = st['win'](M.K_MODEL, P0, P2, P4)
    out = np.empty(len(st['k']))
    for ell, q in ((0, q0), (2, q2), (4, q4)):
        m = st['ell'] == ell
        out[m] = np.interp(st['k'][m], ks, q)
    return out


def chi2_z(p, pair, cam, cos):
    """p = [B_NGC, B_SGC, F, sv_NGC, sv_SGC] para los dos hemisferios de un z."""
    b_n, b_s, f, v_n, v_s = p
    if not (0.3 < b_n < 3.0 and 0.3 < b_s < 3.0 and 0.05 < f < 1.5
            and 0.0 <= v_n < 30.0 and 0.0 <= v_s < 30.0):
        return 1e10
    tot = 0.0
    for st, bb, vv in zip(pair, (b_n, b_s), (v_n, v_s)):
        r = st['P'] - predict_BF(st, cam, cos, bb, f, vv)
        tot += float(r @ st['Cinv'] @ r)
    return tot


if __name__ == '__main__':
    B.KMAX = KMAX
    print('=' * 78)
    print(f'  CONTROL NEGATIVO — tasa de crecimiento LIBRE, como en el analisis')
    print(f'  publicado.  Plantilla LCDM-Planck,  k_max = {KMAX}')
    print('=' * 78)

    sets = B.build()
    c = B.COSMO['LCDM']
    h = c['H0'] / 100.0
    om = (c['ombh2'] + c['omch2'] + c['mnu'] / 93.14) / h ** 2
    cos = dict(Om=om, w0=c['w0'], wa=c['wa'])
    zs = sorted({st['z'] for st in sets})
    cam = B.camb_run(c, zs)

    print(f'\n  {"z":>6}  {"f*sigma8 medido":>18}  {"publicado":>16}'
          f'  {"tension":>9}  {"chi2/dof":>9}')
    print('  ' + '-' * 68)
    res_all, tot_chi2, tot_dof = [], 0.0, 0
    for z in zs:
        pair = [st for st in sets if st['z'] == z]
        x0 = [1.2, 1.2, 0.45, 3.0, 3.0]
        r = minimize(chi2_z, x0, args=(pair, cam, cos), method='Nelder-Mead',
                     options=dict(xatol=1e-4, fatol=1e-3, maxfev=2500,
                                  maxiter=2500))
        r = minimize(chi2_z, r.x, args=(pair, cam, cos), method='Nelder-Mead',
                     options=dict(xatol=1e-5, fatol=1e-4, maxfev=2500,
                                  maxiter=2500))
        n = sum(st['npts'] for st in pair)
        dof = n - 5
        tot_chi2 += r.fun; tot_dof += dof
        fs8 = r.x[2]

        # Incertidumbre por Delta chi2 = 1, perfilando el resto de parametros.
        # Barrido corto con arranque caliente + parabola: la version por fuerza
        # bruta (paso 0.005 con minimizacion completa en cada paso) eran horas.
        def prof(fv):
            q = minimize(lambda y: chi2_z([y[0], y[1], fv, y[2], y[3]],
                                          pair, cam, cos),
                         [r.x[0], r.x[1], r.x[3], r.x[4]],
                         method='Nelder-Mead',
                         options=dict(xatol=1e-4, fatol=1e-3, maxfev=500))
            return q.fun - r.fun
        off = np.array([-0.06, -0.04, -0.02, 0.02, 0.04, 0.06])
        dd = np.array([prof(fs8 + o) for o in off])
        # chi2 - chi2_min ~ (dF/sigma)^2  =>  ajuste de la curvatura
        a = float(np.sum(dd * off ** 2) / np.sum(off ** 4))
        sig = float(1.0 / np.sqrt(a)) if a > 0 else float('nan')

        pub, epub = CONSENSO[z]
        tens = (fs8 - pub) / np.hypot(sig, epub)
        res_all.append(dict(z=z, fsigma8=float(fs8), sigma=float(sig),
                            publicado=pub, err_pub=epub, tension=float(tens),
                            chi2=float(r.fun), dof=int(dof),
                            b1s8_NGC=float(r.x[0]), b1s8_SGC=float(r.x[1]),
                            sv_NGC=float(r.x[3]), sv_SGC=float(r.x[4])))
        print(f'  {z:6.2f}  {fs8:9.4f} +- {sig:.4f}  {pub:8.3f} +- {epub:.3f}'
              f'  {tens:+8.2f}s  {r.fun/dof:9.4f}', flush=True)

    print('  ' + '-' * 68)
    print(f'  chi2 total = {tot_chi2:.2f}   dof = {tot_dof}   '
          f'chi2/dof = {tot_chi2/tot_dof:.4f}')
    t = np.array([x['tension'] for x in res_all])
    print(f'\n  tension media con el publicado: {np.abs(t).mean():.2f} sigma')
    print('  VEREDICTO: ' + ('maquinaria SANA — reproduce el publicado'
                             if np.abs(t).max() < 2.0 else
                             'NO reproduce el publicado — revisar maquinaria'))
    with open(f'{OUT}/boss_control_kmax{KMAX:.3f}.json', 'w') as fh:
        json.dump(dict(kmax=KMAX, bins=res_all, chi2=tot_chi2, dof=tot_dof),
                  fh, indent=1)
    print(f'  -> {OUT}/boss_control_kmax{KMAX:.3f}.json')
