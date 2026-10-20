#!/usr/bin/env python3
"""analiza_boss_chen21.py — BOSS en el montaje de Chen+22: control, SSEE clavado y LCDM-Planck (2026-10-20).

TRES FILAS, en este orden (regla de Mike, 2026-10-19):
  1. CONTROL   LCDM libre (lcdm_chen21_covchen) contra lo PUBLICADO por Chen, Vlah &
               White 2022 (columna P_ell). Criterio fijado antes de correr: logA,
               Omega_m, H_0 y sigma_8 a menos de 0.3 sigma publicada, y R-1 < 0.03.
               Si no pasa, el script sale con error y no escribe nada.
  2. SSEE      todo clavado (fondo algebraico y logA del CMB del modelo): cero
               parametros cosmologicos libres. Se compara contra lo PUBLICADO, o sea
               contra el LCDM libre del control.
  3. LCDM_PLANCK todo clavado en Planck 2018: «comparacion de fondos», no control.

QUE SE COMPARA (regla de Mike, 2026-10-20): el chi2 CRUDO contra el dato. Para cada
fila, chi2 = (d - m)^T C^-1 (d - m) en los 144 puntos (l = 0, 2 en NGC y SGC de z1 y
z3), mas la penalizacion gaussiana de los cuatro lineales por muestra (sus priors de
Chen; vale ~1). Los lineales se perfilan en forma cerrada y el resto (cosmologia en
el control; sesgos en todas) se minimiza con varios minimizadores en cadena (Powell,
L-BFGS-B, Nelder-Mead), arrancando de la mejor muestra; se queda el menor.
  BIC = chi2_min + k ln N, con k = parametros ajustados: control 31 (3 cosmologicos +
  12 sesgos + 16 lineales), fijos 28. Delta k = 3 cosmologicos.
Aparte, como referencia, el chi2 MARGINAL de la cadena (-2 ln L con los lineales
integrados: lleva el termino log det F, de VOLUMEN, no de ajuste; por eso es
negativo). No es la medida de ajuste: depende de cuanto espacio de lineales permite
cada fondo.
σ_8, ln A y f σ_8 son SALIDAS de cada modelo: se reportan para entender que ve cada
uno, no son la comparacion.

SALIDA: results/logs/growth_2026-07/boss_chen21.json
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import minimize

_ARGV = list(sys.argv)
sys.argv = [sys.argv[0]]
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src/p06_growth')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
if __name__ == '__main__':                # el acta va en la PRIMERA linea del log
    from procedencia import cabecera as _cab
    print(_cab(__file__), flush=True)
import cobaya_boss_chen21 as C          # noqa: E402
import cobaya_boss_chen21_fijo as F     # noqa: E402
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
from procedencia import cabecera, con_acta   # noqa: E402
sys.argv = _ARGV

CH = '/mnt/datos/SSEE_data/chains_p6/boss_chen21'
SALIDA = '/home/mike/Proyectos/SSEE/results/logs/growth_2026-07/boss_chen21.json'
BURN = 0.3
NPTS = sum(st['npts'] for st in C.SETS)


def lee(nombre):
    fs = sorted(f'{CH}/{nombre}.{i}.txt' for i in range(1, 5))
    cols = open(fs[0]).readline().split()[1:]
    bloques = []
    for f in fs:
        a = np.loadtxt(f)
        bloques.append(a[int(BURN * len(a)):])
    ult = [l for l in open(f'{CH}/{nombre}.progress').read().splitlines() if l.strip() and not l.startswith('#')][-1]
    return cols, np.concatenate(bloques), float(ult.split()[3])   # columnas: N, fecha, aceptacion, Rminus1, Rminus1_cl


def media(cols, A, p):
    w, x = A[:, 0], A[:, cols.index(p)]
    m = float(np.average(x, weights=w))
    return m, float(np.sqrt(np.average((x - m) ** 2, weights=w)))


def minimo(cols, A, nombres, menos_loglike):
    chi2_col = A[:, cols.index('chi2')]
    i0 = int(np.argmin(chi2_col))
    x0 = np.array([A[i0, cols.index(n)] for n in nombres])
    r = minimize(lambda x: menos_loglike(dict(zip(nombres, x))), x0, method='Powell',
                 options=dict(xtol=1e-4, ftol=1e-7, maxfev=60000))
    return float(chi2_col[i0]), float(min(2 * r.fun, chi2_col[i0])), dict(zip(nombres, map(float, r.x)))


def chi2_crudo(pz):
    """chi2 crudo de los 144 puntos + penalizacion de los lineales perfilados (cov conjunta de Chen)."""
    tot = 0.0
    for zb, pares in pz.items():
        r, T = [], []
        for st, Y, b1, b2, bs in pares:
            m0, t = C._piezas(st, Y, b1, b2, bs)
            r.append(st['d'] - m0)
            T.append(t)
        r = np.concatenate(r)
        TT = np.zeros((len(r), 4 * len(T)))
        for i, t in enumerate(T):
            TT[i * t.shape[0]:(i + 1) * t.shape[0], 4 * i:4 * (i + 1)] = t
        Ci = C.CJINV[zb]
        P = np.diag(np.tile(1.0 / C.SIG_LIN ** 2, len(T)))
        bh = np.linalg.solve(TT.T @ Ci @ TT + P, TT.T @ Ci @ r)
        res = r - TT @ bh
        tot += float(res @ Ci @ res + bh @ P @ bh)
    return tot


def min_crudo(x0, nombres, f):
    best, xb, rastro = f(dict(zip(nombres, x0))), np.asarray(x0, float), []
    for met in ('Powell', 'L-BFGS-B', 'Nelder-Mead', 'Powell'):
        op = dict(maxiter=5000) if met == 'L-BFGS-B' else dict(maxiter=30000, maxfev=60000)
        r = minimize(lambda x: f(dict(zip(nombres, x))), xb, method=met, options=op)
        rastro.append(dict(metodo=met, chi2=float(r.fun), evaluaciones=int(r.nfev)))
        if r.fun < best:
            best, xb = float(r.fun), r.x
    return best, dict(zip(nombres, map(float, xb))), rastro


def main():
    out = dict(npts=NPTS, blanco=C.BLANCO, criterio_sigma=C.TOL, burn_in=BURN)

    # 1. CONTROL
    cols, A, rm1 = lee('lcdm_chen21_covchen')
    ctl = dict(Rminus1=rm1, parametros={})
    pasa = rm1 < 0.03
    for p in ('logA', 'Om', 'H0', 'sigma8'):
        m, s = media(cols, A, p)
        m0, s0 = C.BLANCO[p]
        d = (m - m0) / s0
        ctl['parametros'][p] = dict(media=m, sigma=s, publicado=m0, sigma_pub=s0, distancia_sigma=d,
                                    razon_barras=s / s0)
        pasa &= abs(d) < C.TOL
    ctl['pasa'] = bool(pasa)
    print(json.dumps(ctl, indent=1), flush=True)
    if not pasa:
        sys.exit('CONTROL NO PASA: no se escribe la comparacion')
    libres = [c for c in cols if c in ('Om', 'H0', 'logA') or c.startswith(('bsig8_', 'b2_', 'bs_'))]

    def ml_ctl(d):
        ll = C.loglike(d['Om'], d['H0'], d['logA'], **{k: v for k, v in d.items() if k not in ('Om', 'H0', 'logA')})[0]
        return 1e30 if not np.isfinite(ll) else -ll
    ctl['chi2_cadena'], ctl['chi2_min'], ctl['mejor'] = minimo(cols, A, libres, ml_ctl)
    ctl['k'] = len(libres)

    def pz_ctl(d):
        h = d['H0'] / 100.0
        if not C.dentro(d['Om'], h, d['logA']):
            return None
        pz = {}
        for st in C.SETS:
            Y, s80 = C.tablas(st['z'], d['Om'], h, d['logA'])
            s8 = s80 * np.sqrt(np.exp(d['logA']) * 1e-10 / C.R.AS_REF)
            t = st['tag']
            pz.setdefault(st['zb'], []).append((st, Y, d[f'bsig8_{t}'] / s8 - 1.0, d[f'b2_{t}'], d[f'bs_{t}']))
        return pz
    ctl['chi2_crudo_min'], ctl['mejor_crudo'], ctl['rastro_crudo'] = min_crudo(
        [ctl['mejor'][n] for n in libres], libres, lambda d: 1e30 if (pz := pz_ctl(d)) is None else chi2_crudo(pz))
    ctl['k_crudo'] = len(libres) + 16
    out['control_lcdm_libre'] = ctl
    print('control chi2 crudo min %.3f' % ctl['chi2_crudo_min'], flush=True)
    print('control chi2 cadena %.3f  min %.3f' % (ctl['chi2_cadena'], ctl['chi2_min']), flush=True)

    # 2 y 3. FIJOS
    for modelo in ('SSEE', 'LCDM_PLANCK'):
        cols, A, rm1 = lee(f'fijo_{modelo}')
        T = F.tablas(modelo)
        ll = F.hace_loglike(T)
        nuis = [c for c in cols if c.startswith(('bsig8_', 'b2_', 'bs_'))]
        fila = dict(Rminus1=rm1, fondo=F.FONDOS[modelo],
                    por_z={str(z): {k: v for k, v in T[z].items() if k != 'Y'} for z in T}, k=len(nuis))
        fila['chi2_cadena'], fila['chi2_min'], fila['mejor'] = minimo(cols, A, nuis, lambda d: -ll(**d)[0])
        s8 = fila['por_z'][str(C.MUESTRAS[0][1])]['sigma8_0']

        def pz_fijo(d, T=T, s8=s8):
            pz = {}
            for st in C.SETS:
                t = st['tag']
                pz.setdefault(st['zb'], []).append((st, T[st['z']]['Y'], d[f'bsig8_{t}'] / s8 - 1.0, d[f'b2_{t}'], d[f'bs_{t}']))
            return pz
        fila['chi2_crudo_min'], fila['mejor_crudo'], fila['rastro_crudo'] = min_crudo(
            [fila['mejor'][n] for n in nuis], nuis, lambda d: chi2_crudo(pz_fijo(d)))
        fila['k_crudo'] = len(nuis) + 16
        fila['chi2_crudo_por_muestra'] = {zb: chi2_crudo({zb: pp}) for zb, pp in pz_fijo(fila['mejor_crudo']).items()}
        fila['dchi2_crudo_vs_lcdm_libre'] = fila['chi2_crudo_min'] - ctl['chi2_crudo_min']
        fila['dBIC_crudo_vs_lcdm_libre'] = fila['dchi2_crudo_vs_lcdm_libre'] + (fila['k_crudo'] - ctl['k_crudo']) * np.log(NPTS)
        m, s = ctl['parametros']['sigma8']['media'], ctl['parametros']['sigma8']['sigma']
        la, sla = ctl['parametros']['logA']['media'], ctl['parametros']['logA']['sigma']
        fila['sigma8_vs_control_sigma'] = (s8 - m) / s
        fila['logA_vs_control_sigma'] = (fila['fondo']['logA'] - la) / sla
        fila['sigma8_vs_publicado_sigma'] = (s8 - C.BLANCO['sigma8'][0]) / C.BLANCO['sigma8'][1]
        fila['dchi2_vs_lcdm_libre'] = fila['chi2_min'] - ctl['chi2_min']
        fila['dBIC_vs_lcdm_libre'] = fila['dchi2_vs_lcdm_libre'] + (fila['k'] - ctl['k']) * np.log(NPTS)
        out[modelo] = fila
        print(modelo, json.dumps({k: v for k, v in fila.items() if k not in ('mejor', 'por_z')}, indent=1), flush=True)
    out['dchi2_marginal_ssee_menos_planck'] = out['SSEE']['chi2_min'] - out['LCDM_PLANCK']['chi2_min']
    out['dchi2_crudo_ssee_menos_planck'] = out['SSEE']['chi2_crudo_min'] - out['LCDM_PLANCK']['chi2_crudo_min']
    for m in ('control_lcdm_libre', 'SSEE', 'LCDM_PLANCK'):
        out[m]['chi2_crudo_por_gl'] = out[m]['chi2_crudo_min'] / (NPTS - out[m]['k_crudo'])
    print('crudo: libre %.3f  SSEE %.3f  Planck %.3f' % tuple(out[m]['chi2_crudo_min'] for m in ('control_lcdm_libre', 'SSEE', 'LCDM_PLANCK')))
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    ss, pl, ct = out['SSEE'], out['LCDM_PLANCK'], out['control_lcdm_libre']
    z1, z3 = (str(z) for _, z in C.MUESTRAS)
    out['resumen'] = dict(
        npts=NPTS, k_libre=ct['k_crudo'], k_fijo=ss['k_crudo'],
        chi2_libre=ct['chi2_crudo_min'], chi2_ssee=ss['chi2_crudo_min'], chi2_planck=pl['chi2_crudo_min'],
        gl_libre=NPTS - ct['k_crudo'], gl_fijo=NPTS - ss['k_crudo'],
        chi2gl_libre=ct['chi2_crudo_por_gl'], chi2gl_ssee=ss['chi2_crudo_por_gl'], chi2gl_planck=pl['chi2_crudo_por_gl'],
        dchi2_ssee_libre=ss['dchi2_crudo_vs_lcdm_libre'], dchi2_planck_libre=pl['dchi2_crudo_vs_lcdm_libre'],
        dchi2_ssee_planck=out['dchi2_crudo_ssee_menos_planck'],
        dBIC_ssee_libre=ss['dBIC_crudo_vs_lcdm_libre'], dBIC_planck_libre=pl['dBIC_crudo_vs_lcdm_libre'],
        dchi2_ssee_planck_z1=ss['chi2_crudo_por_muestra']['z1'] - pl['chi2_crudo_por_muestra']['z1'],
        dchi2_ssee_planck_z3=ss['chi2_crudo_por_muestra']['z3'] - pl['chi2_crudo_por_muestra']['z3'],
        ctl_Rm1=ct['Rminus1'],
        **{f'ctl_{p}': ct['parametros'][p]['media'] for p in ('logA', 'Om', 'H0', 'sigma8')},
        **{f'ctl_{p}_sig': ct['parametros'][p]['sigma'] for p in ('logA', 'Om', 'H0', 'sigma8')},
        **{f'ctl_{p}_dist': ct['parametros'][p]['distancia_sigma'] for p in ('logA', 'Om', 'H0', 'sigma8')},
        sigma8_ssee=ss['por_z'][z1]['sigma8_0'], sigma8_planck=pl['por_z'][z1]['sigma8_0'],
        fs8_ssee_z1=ss['por_z'][z1]['fsigma8'], fs8_ssee_z3=ss['por_z'][z3]['fsigma8'],
        fs8_planck_z1=pl['por_z'][z1]['fsigma8'], fs8_planck_z3=pl['por_z'][z3]['fsigma8'],
        s8_ssee_vs_ctl=ss['sigma8_vs_control_sigma'], s8_planck_vs_ctl=pl['sigma8_vs_control_sigma'],
        logA_ssee_vs_ctl=ss['logA_vs_control_sigma'], Rm1_ssee=ss['Rminus1'], Rm1_planck=pl['Rminus1'])
    print('resumen', json.dumps(out['resumen'], default=float), flush=True)
    entradas = [os.path.abspath(__file__), C.__file__, F.__file__]
    for n in ('lcdm_chen21_covchen', 'fijo_SSEE', 'fijo_LCDM_PLANCK'):
        entradas += [f'{CH}/{n}.{i}.txt' for i in range(1, 5)] + [f'{CH}/{n}.progress']
    entradas += [f'{C.DAT}/chen22_cov/cov_joint_NGCSGCXi_{zb}.dat' for zb, _ in C.MUESTRAS]
    out = json.loads(json.dumps(out, default=float))
    json.dump(con_acta(out, __file__, entradas=entradas), open(SALIDA, 'w'), indent=1)
    print('escrito', SALIDA)


if __name__ == '__main__':
    main()
