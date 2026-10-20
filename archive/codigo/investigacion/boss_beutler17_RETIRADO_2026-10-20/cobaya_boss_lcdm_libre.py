#!/usr/bin/env python3
"""cobaya_boss_lcdm_libre.py — el CONTROL de BOSS: LCDM con el fondo LIBRE (2026-10-17).

POR QUE EXISTE. La fila LCDM de cobaya_boss.py lleva el fondo de Planck FIJO:
sirve para comparar dos fondos fijos sobre el mismo dato, pero no es un
control. Un control es LCDM con su fondo libre reproduciendo un analisis
PUBLICADO del mismo dato (regla de Mike, 2026-10-17). Si lo reproduce, el
pipeline es sano y lo que da SSEE en el es limpio.

EL BLANCO. Chen, Vlah & White 2022 (arXiv:2110.05530, Tabla de resultados,
columna «P_ell»): el MISMO codigo (velocileptors, LPT a un lazo), los MISMOS
bines (z1 y z3, NGC y SGC), k <= 0.20. Publican
    ln(1e10 A_s) = 2.84 ± 0.13   Omega_m = 0.305 ± 0.010
    H_0 = 68.5 ± 1.1             sigma_8 = 0.738 ± 0.048
con omega_b = 0.02242 y n_s = 0.9665 FIJOS (mejor ajuste de Planck) y priors
planos Omega_m U(0.20, 0.40), H_0 U(60, 80), ln(1e10 A_s) U(1.61, 3.91).
Aqui se toman los mismos omega_b y n_s, y Sum m_nu = 0.06 eV (el de LCDM).
Diferencias que quedan y se declaran: ellos usan las medidas de Beutler+2021
(espectro deconvolucionado de la ventana) y solo l = 0, 2, k >= 0.02; aqui las
publicas de Beutler+2017 con la ventana aplicada al modelo, l = 0, 2, 4,
k >= 0.01 (la misma configuracion que corre SSEE). El criterio es reproducir
su posterior dentro de 1 sigma en cada parametro.

COMO SE HACE BARATO. Rehacer CAMB + LPT en cada muestra cuesta ~6.8 s (medido
2026-10-17). En lugar de eso las tablas LPT se construyen UNA vez en una malla
de Chebyshev en (Omega_m, h, logA) y se interpolan (formula baricentrica en
cada eje). Es la idea de la expansion de Taylor de Chen+2022, con nodos en vez
de derivadas. Fuera de la malla la verosimilitud es -inf: la malla ES el
prior efectivo, y se declara (Omega_m [0.25, 0.37], H_0 [62, 76], logA [2, 4],
mas de 5 sigma del blanco en cada eje). La precision de la interpolacion se
mide contra tablas rehechas en puntos que no son nodos (modo `prueba`).

Uso:
  mpirun -n 4 .venv/bin/python3 src/p06_growth/cobaya_boss_lcdm_libre.py cadena <dir>
  .venv/bin/python3 src/p06_growth/cobaya_boss_lcdm_libre.py prueba
"""
import os
import pickle
import sys
import time

import numpy as np

sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src/p06_growth')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src/p11_sondas')
np.seterr(all='ignore')

_ARGV = list(sys.argv)
sys.argv = [sys.argv[0], '0.20']
import boss_lpt_R1R2 as R                      # noqa: E402
sys.argv = _ARGV
from velocileptors.LPT.lpt_rsd_fftw import LPT_RSD  # noqa: E402

OMBH2, NS, MNU = 0.02242, 0.9665, 0.06       # ORIGEN-VALOR: Chen, Vlah & White 2022 (arXiv:2110.05530) §modelo: omega_b y n_s fijos al mejor ajuste de Planck; m_nu el de LCDM
OM_EJE, H_EJE = (0.25, 0.37), (0.62, 0.76)
N_OM = N_H = int(os.environ.get('BOSS_MALLA_N', '7'))   # 7 x 7 nodos; un N chico solo para probar el cableado
BLANCO = dict(fuente='Chen, Vlah & White 2022, arXiv:2110.05530, Tabla main_results, columna P_ell',
              logA=(2.84, 0.13), Om=(0.305, 0.010), H0=(68.5, 1.1), sigma8=(0.738, 0.048))
MALLA = f'/mnt/datos/SSEE_data/chains_p6/boss_lcdm_libre/malla_{N_OM}x{N_H}x{R.N_NODOS}.pkl'


def _cheb(a, b, n):
    j = np.arange(n)
    x = 0.5 * (a + b) + 0.5 * (b - a) * np.cos(np.pi * j / (n - 1))
    w = (-1.0) ** j * np.where((j == 0) | (j == n - 1), 0.5, 1.0)
    return x, w


OM_N, OM_W = _cheb(*OM_EJE, N_OM)
H_N, H_W = _cheb(*H_EJE, N_H)


def _pesos(x, nodos, w):
    d = x - nodos
    j = int(np.argmin(np.abs(d)))
    if d[j] == 0.0:
        e = np.zeros(len(nodos))
        e[j] = 1.0
        return e
    c = w / d
    return c / c.sum()


def cosmo(Om, h):
    return dict(Om=Om, h=h, ombh2=OMBH2, ns=NS, w0=-1.0, wa=0.0, mnu=MNU)


def _objeto_lpt(z):
    """Un LPT_RSD en el centro de la malla, solo para combinar tablas (se pisan)."""
    c = cosmo(0.5 * sum(OM_EJE), 0.5 * sum(H_EJE))
    kl, pl, fz, _ = R.camb_lin(c, z)
    L = LPT_RSD(kl, pl, kIR=0.2, cutoff=10, extrap_min=-4, extrap_max=3, N=2000, threads=1, jn=5)
    L.make_pltable(fz, kv=SETS[0]['kmod'], apar=1.0, aperp=1.0, ngauss=3)
    return L


def construye_malla():
    """Y[z][iOm, ih, ilogA, l, k, termino], f, s8(z) y s8(0) en cada nodo (Om, h)."""
    if os.path.exists(MALLA):
        out = pickle.load(open(MALLA, 'rb'))
        out['L'] = {z: _objeto_lpt(z) for z in out['Y']}
        return out
    t0 = time.time()
    zs = sorted({st['z'] for st in SETS})
    kmod = SETS[0]['kmod']
    out = dict(Y={}, f={}, s8={}, s80=np.empty((N_OM, N_H)), L={})
    for z in zs:
        Y = None
        f = np.empty((N_OM, N_H))
        s8 = np.empty((N_OM, N_H))
        for i, Om in enumerate(OM_N):
            for j, h in enumerate(H_N):
                c = cosmo(Om, h)
                kl, pl, fz, s8z = R.camb_lin(c, z)
                a_par, a_per = R.M.alphas(z, Om, -1.0, 0.0)
                L, Yn = R.tablas_logA(kl, pl, fz, kmod, a_par, a_per)
                if Y is None:
                    Y = np.empty((N_OM, N_H) + Yn.shape)
                Y[i, j] = Yn
                f[i, j], s8[i, j] = fz, s8z
                if z == zs[0]:
                    out['s80'][i, j] = R.camb_lin(c, 0.0)[3]
            print(f'  malla z={z}: Om nodo {i + 1}/{N_OM}  ({time.time() - t0:.0f} s)', flush=True)
        out['Y'][z], out['f'][z], out['s8'][z], out['L'][z] = Y, f, s8, L
    os.makedirs(os.path.dirname(MALLA), exist_ok=True)
    # el objeto LPT_RSD lleva planes de pyfftw y no se serializa: se guarda solo
    # lo numerico y se rehace un objeto por z al cargar (sus tablas se pisan)
    pickle.dump({k: v for k, v in out.items() if k != 'L'}, open(MALLA, 'wb'))
    print(f'  malla construida en {(time.time() - t0) / 60:.1f} min', flush=True)
    return out


def _fija(st, Om, h, logA):
    """Pone en el conjunto (como modelo 'LCDM') las tablas interpoladas a (Om, h, logA)."""
    z = st['z']
    wo, wh, wa = _pesos(Om, OM_N, OM_W), _pesos(h, H_N, H_W), _pesos(logA, R.LOGA_NODOS, R._W_NODOS)
    Y = np.tensordot(wa, np.tensordot(wh, np.tensordot(wo, G['Y'][z], 1), 1), 1)
    L = G['L'][z]
    L.p0ktable, L.p2ktable, L.p4ktable = Y[0], Y[1], Y[2]
    s8 = float(wo @ G['s8'][z] @ wh)
    # Y ya esta a logA: un solo nodo, para que fija_logA no vuelva a interpolar
    st['lpt']['LCDM'] = dict(L=L, Y=np.repeat(Y[None], R.N_NODOS, axis=0),
                             f=float(wo @ G['f'][z] @ wh), sigma8=s8 * (1 + 1e-7 * (Om + 3 * h)))


def dentro(Om, h, logA):
    return (OM_EJE[0] <= Om <= OM_EJE[1] and H_EJE[0] <= h <= H_EJE[1]
            and R.LOGA_MIN <= logA <= R.LOGA_MAX)


def loglike(Om, H0, logA, **b):
    h = H0 / 100.0
    if not dentro(Om, h, logA):   # fuera de la malla: -inf, pero cobaya exige TODOS los derivados
        return -np.inf, {d: np.nan for d in ('sigma8', 'S8', *[f'fs8_{int(round(100 * z))}' for z in G['f']])}
    tot = 0.0
    for st in SETS:
        _fija(st, Om, h, logA)
        tag = f"{st['zb']}{st['cap']}"
        c, _ = R.chi2_marg_set(st, 'LCDM', logA, [b[f'b1_{tag}'], b[f'b2_{tag}'], b[f'bs_{tag}']])
        tot += c
    wo, wh = _pesos(Om, OM_N, OM_W), _pesos(h, H_N, H_W)
    s80 = float(wo @ G['s80'] @ wh) * np.sqrt(np.exp(logA) * 1e-10 / R.AS_REF)
    der = dict(sigma8=s80, S8=s80 * np.sqrt(Om / 0.3))
    for z in sorted(G['f']):
        der[f'fs8_{int(round(100 * z))}'] = (float(wo @ G['f'][z] @ wh) * float(wo @ G['s8'][z] @ wh)
                                            * np.sqrt(np.exp(logA) * 1e-10 / R.AS_REF))
    return -0.5 * tot, der


def _params():
    import cobaya_boss as CB
    p = dict(Om=dict(prior=dict(min=0.20, max=0.40), ref=0.305, proposal=0.005, latex=r'\Omega_m'),
             H0=dict(prior=dict(min=60.0, max=80.0), ref=68.5, proposal=0.5, latex='H_0'),
             logA=dict(prior=dict(min=1.61, max=3.91), ref=2.84, proposal=0.03, latex=r'\log(10^{10}A_s)'))
    for st in SETS:
        tag = f"{st['zb']}{st['cap']}"
        for k in ('b1', 'b2', 'bs'):
            q = dict(CB._PRIOR[k])
            q['ref'] = dict(dist='norm', loc=CB._SEMILLA[('b1', 'b2', 'bs').index(k)], scale=0.1)
            p[f'{k}_{tag}'] = q
    for d in ('sigma8', 'S8', *[f'fs8_{int(round(100 * z))}' for z in sorted({st["z"] for st in SETS})]):
        p[d] = dict(latex=d)
    return p


def _ll(Om, H0, logA, **kw):
    v, der = loglike(Om, H0, logA, **kw)
    return v, der


def prueba():
    """Malla interpolada contra tablas REHECHAS en puntos que no son nodos."""
    rng = np.random.default_rng(20261017)
    th = [1.0, -1.0, 0.5]
    peor = 0.0
    for _ in range(4):
        Om = rng.uniform(0.28, 0.33)
        h = rng.uniform(0.65, 0.72)
        la = rng.uniform(2.5, 3.2)
        ci = ce = 0.0
        for st in SETS:
            _fija(st, Om, h, la)
            ci += R.chi2_marg_set(st, 'LCDM', la, th)[0]
            c = cosmo(Om, h)
            kl, pl, fz, s8 = R.camb_lin(c, st['z'])
            a_par, a_per = R.M.alphas(st['z'], Om, -1.0, 0.0)
            L = LPT_RSD(kl, pl * np.exp(la) * 1e-10 / R.AS_REF, kIR=0.2, cutoff=10,
                        extrap_min=-4, extrap_max=3, N=2000, threads=1, jn=5)
            L.make_pltable(fz, kv=st['kmod'], apar=a_par, aperp=a_per, ngauss=3)
            Yx = np.stack([L.p0ktable, L.p2ktable, L.p4ktable])
            st['lpt']['LCDM'] = dict(L=L, Y=np.repeat(Yx[None], R.N_NODOS, axis=0), f=fz,
                                     sigma8=s8 * (1 + 3e-7))
            ce += R.chi2_marg_set(st, 'LCDM', la, th)[0]
        peor = max(peor, abs(ci - ce))
        print(f'  Om={Om:.4f} h={h:.4f} logA={la:.4f}: exacto {ce:.4f}  interpolado {ci - ce:+.2e}', flush=True)
    print(f'  peor {peor:.2e}')
    return peor


SETS = R.build()
G = construye_malla()

# CONFIGURACION (2026-10-18). 'propia' = la de SSEE (l = 0, 2, 4; k en [0.01, 0.20]).
# 'chen' = la de Chen, Vlah & White 2022 (l = 0, 2; k en [0.02, 0.20]): es la que
# prueba si el pipeline REPRODUCE lo publicado, porque es su misma configuracion
# salvo los datos (Beutler+2017 aqui, +2021 alli). Criterio declarado ANTES de
# correrla: la 'chen' debe caer a < 1 sigma publicado en cada parametro; la
# diferencia propia - chen mide cuanto mueven el hexadecapolo y los k bajos.
# El recorte se hace aqui y no en el nucleo: la covarianza se reconstruye de la
# inversa (C = inv(Cinv) * Hartlap), se recorta y se recalcula el Hartlap con los
# puntos que quedan. Las tablas LPT y la ventana no cambian.
CONFIG = os.environ.get('BOSS_CONFIG', 'propia')
if CONFIG == 'chen':
    for st in SETS:
        keep = (st['ell'] != 4) & (st['k'] >= 0.02)
        C = np.linalg.inv(st['Cinv']) * st['hartlap']
        n_p = int(keep.sum())
        hart = (R.NMOCKS[st['cap']] - n_p - 2.0) / (R.NMOCKS[st['cap']] - 1.0)
        st.update(k=st['k'][keep], ell=st['ell'][keep], d=st['d'][keep], npts=n_p, hartlap=hart,
                  Cinv=np.linalg.inv(C[np.ix_(keep, keep)]) * hart)
        print(f"  config chen: {st['zb']} {st['cap']} {n_p} puntos  Hartlap={hart:.4f}", flush=True)
elif CONFIG != 'propia':
    sys.exit(f'BOSS_CONFIG desconocida: {CONFIG}')

if __name__ == '__main__':
    modo = _ARGV[1] if len(_ARGV) > 1 else 'prueba'
    if modo == 'prueba':
        sys.exit(0 if prueba() < 0.05 else 1)
    from cobaya.run import run
    chains = _ARGV[2] if len(_ARGV) > 2 else '/mnt/datos/SSEE_data/chains_p6/boss_lcdm_libre'
    p = _params()
    info = dict(likelihood={'boss_lcdm_libre': {'external': _ll, 'input_params': [k for k in p if 'prior' in p[k]],
                                                 'output_params': [k for k in p if 'prior' not in p[k]]}},
                params=p, sampler={'mcmc': {'Rminus1_stop': 0.03, 'max_tries': 20000}},
                output=f"{chains}/lcdm_libre{'' if CONFIG == 'propia' else '_' + CONFIG}", force=True, resume=False)
    t0 = time.time()
    run(info)
    print(f'\nTERMINADO en {(time.time() - t0) / 3600:.2f} h', flush=True)
