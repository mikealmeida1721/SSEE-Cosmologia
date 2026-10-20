#!/usr/bin/env python3
"""cobaya_boss_chen21.py — CONTROL de BOSS: reproducir Chen, Vlah & White 2022 con SU montaje (2026-10-19).

POR QUE EXISTE. El control anterior (cobaya_boss_lcdm_libre.py, archivado 2026-10-20 con el BOSS de Beutler+2017) corria LCDM con el
fondo libre pero con NUESTRO montaje, y quedaba ~0.75-1.1 sigma corrido de lo
publicado. Un control que reproduce queda pegado a lo publicado (KiDS-1000: 0.06
sigma). Leyendo el articulo (arXiv:2110.05530, nota 2) y su codigo publico
(github.com/sfschen/BOSSxPlanck, rsd_likelihood/pk_likelihood_gc_emu_lnA.py y
emulator/compute_pell_tables.py) aparecieron las diferencias. La mas grande: los
espectros publicos de Beutler+2017 que usabamos tienen un desajuste de
normalizacion ventana/espectro de ~10% que da sigma_8 sistematicamente bajo;
Beutler & McDonald 2021 (arXiv:2106.06324) los corrigieron. Medido aqui: P_0 viejo
/ nuevo = 0.90-0.92 en las cuatro muestras.

QUE SE COPIA DE CHEN+22, pieza por pieza (fuente entre parentesis):
  datos     ps1D_BOSS_DR12_{NGC,SGC}_{z1,z3}_..._renorm.dat (fbeutler.github.io/hub,
            Beutler & McDonald 2021), bines de 0.01 h/Mpc (combine_bins=10)
  multipolos l = 0, 2; 0.02 < k < 0.20 h/Mpc, 18 bines por multipolo (Sec. 4.1)
  ventana   P_conv = W M P_teoria: M (2000x1200, angulo ancho) y W (200x2000), modelo
            en 400 bines de 0.001 h/Mpc, spline cubico con extrapolacion constante y
            ancla P(0) = 0 (fs_observe / fs_predict de su codigo)
  covarianza LA SUYA: rsd_data/covariances/cov_joint_NGCSGCXi_{z1,z3}.dat de su
            repositorio (commit 0755be4), conjunta NGC+SGC por muestra, bloque P_l
            recortado, SIN Hartlap (su codigo la invierte tal cual). Primero se uso la
            C_2048 de Beutler por cada casquete: los datos salen identicos bit a bit,
            pero su matriz es otra realizacion (diagonal +-10 %, cruces NGC-SGC hasta
            0.12) y con ella el control quedaba con sigma_8 a -0.34 sigma, fuera del
            criterio. BOSS_COV=c2048 conserva aquella variante como diagnostico.
  P_lin     P_cb (frio + bariones, sin neutrinos) y f = f(a, Omega_m) (1 - 0.6 f_nu)
            con la f de crecimiento LCDM por hipergeometrica (su linear_theory.f_of_a)
  LPT       velocileptors LPT_RSD, kIR 0.2, cutoff 10, N 2000, jn 5, ngauss 3 (igual)
  fijos     omega_b 0.02242, n_s 0.9665, Sum m_nu 0.06 eV (Sec. 4.2)
  priors    Omega_m U(0.20, 0.40), H_0 U(60, 80), ln(1e10 A_s) U(1.61, 3.91),
            (1+b1) sigma_8 U(0.5, 3.0), b2 N(0, 10), bs N(0, 5), alpha_0 N(0, 100),
            alpha_2 N(0, 100), SN_0 N(0, 1000), SN_2 N(0, 5e4) (Tabla 1)
  AP        fiducial Omega_m = 0.31 (cabecera de los datos), z = 0.38 y 0.61
Los cuatro lineales (alpha_0, alpha_2, SN_0, SN_2) se integran en forma cerrada con
sus priors gaussianos: la posterior marginal de los demas parametros es la misma
que muestreandolos (se incluye el termino log det F). sigma_8 es el de materia
total a z = 0, como en su codigo.

COMO SE HACE BARATO. Igual que cobaya_boss_lcdm_libre: tablas LPT en una malla de
Chebyshev 7 x 7 en (Omega_m, h) por 13 nodos de logA, interpolacion baricentrica.
Fuera de la malla (Omega_m [0.25, 0.37], H_0 [62, 76], logA [2, 4]) -inf: mas de 5
sigma del blanco en cada eje. Su precision se mide en el modo `prueba`.

CRITERIO (fijado antes de correr): cada uno de logA, Omega_m, H_0, sigma_8 a menos
de 0.3 sigma publicada de Chen+22 (columna P_ell). Con el montaje copiado, una
distancia mayor es un error nuestro que hay que encontrar.

Uso:
  .venv/bin/python3 src/p06_growth/cobaya_boss_chen21.py prueba
  mpirun -n 4 .venv/bin/python3 src/p06_growth/cobaya_boss_chen21.py cadena <dir>
"""
import gzip
import os
import pickle
import sys
import time

import camb
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as Spline
from scipy.special import hyp2f1

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(_R, 'src'))
sys.path.insert(0, os.path.join(_R, 'src', 'p06_growth'))
np.seterr(all='ignore')
_ARGV = list(sys.argv)
sys.argv = [sys.argv[0], '0.20']
import boss_lpt_R1R2 as R                      # noqa: E402  (solo nodos de logA, A_REF, alphas y tablas_logA)
sys.argv = _ARGV

DAT = '/mnt/datos/SSEE_data/boss_dr12_bm21'
OMBH2, NS, MNU = 0.02242, 0.9665, 0.06      # R66-OK: el omega_b fijo de Chen+22 (coincide con el algebraico de SSEE, pero es el suyo). ORIGEN-VALOR: Chen, Vlah & White 2022 (arXiv:2110.05530) Sec. 4.2
OM_EJE, H_EJE = (0.25, 0.37), (0.62, 0.76)
N_OM = N_H = int(os.environ.get('BOSS_MALLA_N', '7'))
KMIN, KMAX = 0.02, 0.20                       # ORIGEN-VALOR: Chen+22 Sec. 4.1
SIG_LIN = np.array([100.0, 100.0, 1000.0, 5.0e4])   # ORIGEN-VALOR: Chen+22 Tabla 1 (alpha0, alpha2, SN0, SN2)
COL_LIN = (12, 13, 16, 17)                    # columnas de velocileptors: alpha0, alpha2, sn, sn2
BLANCO = dict(fuente='Chen, Vlah & White 2022, arXiv:2110.05530, Tabla de resultados, columna P_ell',
              logA=(2.84, 0.13), Om=(0.305, 0.010), H0=(68.5, 1.1), sigma8=(0.738, 0.048))
TOL = 0.3
MALLA = f'/mnt/datos/SSEE_data/chains_p6/boss_chen21/malla_{N_OM}x{N_H}x{R.N_NODOS}.pkl'
MUESTRAS = (('z1', 0.38), ('z3', 0.61))
KMOD = np.logspace(-3, np.log10(0.5), 180)
K400 = np.linspace(0.0, 0.4, 400, endpoint=False) + 0.0005


def f_of_a(a, Om):
    """Tasa de crecimiento LCDM plana (copia de linear_theory.f_of_a de Chen)."""
    D = a * hyp2f1(1. / 3, 1, 11. / 6, -a ** 3 / Om * (1 - Om)) / hyp2f1(1. / 3, 1, 11. / 6, -1 / Om * (1 - Om))
    r = D / a - a * (6 * a ** 2 * (1 - Om) * hyp2f1(4. / 3, 2, 17. / 6, -a ** 3 * (1 - Om) / Om)) / (11 * Om) \
        / hyp2f1(1. / 3, 1, 11. / 6, -1 / Om * (1 - Om))
    return a * r / D


def _lee_matriz(f):
    return np.loadtxt(gzip.open(f'{DAT}/{f}', 'rt'))


def _lee_espectro(cap, zb):
    sys.path.insert(0, DAT)
    import pk_tools
    d = pk_tools.read_power(f'{DAT}/ps1D_BOSS_DR12_{cap}_{zb}_COMPnbar_TSC_700_700_700_400_renorm.dat', combine_bins=10)
    return np.asarray(d['k_center']), np.asarray(d['pk0']), np.asarray(d['pk2'])


def construye_datos():
    sets = []
    for zb, z in MUESTRAS:
        for cap in ('NGC', 'SGC'):
            kc, p0, p2 = _lee_espectro(cap, zb)
            m = (kc > KMIN) & (kc < KMAX)
            n = len(kc)                                            # 40 bines
            sel = np.concatenate([np.where(m)[0], 2 * n + np.where(m)[0]])   # l=0 y l=2 en el orden de 5 multipolos
            C = _lee_matriz(f'C_2048_BOSS_DR12_{cap}_{zb}_V6C_1_1_1_1_1_10_200_200_prerecon.matrix.gz')[np.ix_(sel, sel)]
            M = _lee_matriz(f'M_BOSS_DR12_{cap}_{zb}_V6C_1_1_1_1_1_1200_2000.matrix.gz')
            W = _lee_matriz(f'W_BOSS_DR12_{cap}_{zb}_V6C_1_1_1_1_1_10_200_2000_averaged_v1.matrix.gz')
            WM = (W @ M)[sel]
            sets.append(dict(zb=zb, cap=cap, z=z, tag=f'{zb}{cap}', d=np.concatenate([p0[m], p2[m]]),
                             Cinv=np.linalg.inv(C), WM=WM, npts=int(len(sel))))
            print(f'  {zb} {cap}: {len(sel)} puntos (l=0,2; {kc[m][0]:.3f}-{kc[m][-1]:.3f})', flush=True)
        w = np.where(m)[0]
        cj = np.loadtxt(f'{DAT}/chen22_cov/cov_joint_NGCSGCXi_{zb}.dat')    # NGC P0,P2, SGC P0,P2 (40 c/u), Xi
        CJINV[zb] = np.linalg.inv(cj[np.ix_(*(2 * [np.concatenate([w, 40 + w, 80 + w, 120 + w])]))])
    return sets


CJINV = {}
COV = os.environ.get('BOSS_COV', 'chen')       # 'chen' (la suya, conjunta) | 'c2048' (Beutler por casquete)


def _piezas(st, Y, b1, b2, bs):
    mono = np.array([1, b1, b1 ** 2, b2, b1 * b2, b2 ** 2, bs, b1 * bs, b2 * bs, bs ** 2, 0.0, 0.0,
                     0, 0, 0, 0, 0, 0, 0])
    return _observa(st, np.einsum('lkt,t->lk', Y, mono)), np.stack([_observa(st, Y[:, :, c]) for c in COL_LIN], axis=1)


def chi2_muestra(zb, pares):
    """chi2 marginal de NGC+SGC juntos con la covarianza conjunta de Chen (lineales de cada casquete aparte)."""
    r, T = [], []
    for st, Y, b1, b2, bs in pares:
        m0, t = _piezas(st, Y, b1, b2, bs)
        r.append(st['d'] - m0)
        T.append(t)
    r = np.concatenate(r)
    TT = np.zeros((len(r), 4 * len(T)))
    for i, t in enumerate(T):
        TT[i * t.shape[0]:(i + 1) * t.shape[0], 4 * i:4 * (i + 1)] = t
    Ci = CJINV[zb]
    F = TT.T @ Ci @ TT + np.diag(np.tile(1.0 / SIG_LIN ** 2, len(T)))
    b = TT.T @ Ci @ r
    return float(r @ Ci @ r - b @ np.linalg.solve(F, b) + np.linalg.slogdet(F)[1])


def cosmo_camb(Om, h, z):
    """P_cb(k) a A_REF, f de Chen, sigma8(z=0) total, alphas AP."""
    p = camb.CAMBparams()
    omch2 = Om * h ** 2 - OMBH2 - MNU / 93.14
    p.set_cosmology(H0=100 * h, ombh2=OMBH2, omch2=omch2, mnu=MNU, omk=0.0)
    p.InitPower.set_params(As=R.AS_REF, ns=NS)
    p.set_matter_power(redshifts=[z, 0.0], kmax=3.0)
    r = camb.get_results(p)
    k, zz, pk = r.get_matter_power_spectrum(minkh=1e-4, maxkh=2.0, npoints=800, var1='delta_nonu', var2='delta_nonu')
    iz = int(np.argmin(np.abs(np.asarray(zz) - z)))
    s8 = r.get_sigma8()                       # en el orden de redshifts crecientes de CAMB
    s80 = float(s8[int(np.argmin(np.abs(np.asarray(r.transfer_redshifts) - 0.0)))])
    fnu = (MNU / 93.14) / (Om * h ** 2)
    f = float(f_of_a(1.0 / (1.0 + z), Om) * (1 - 0.6 * fnu))
    a_par, a_per = R.M.alphas(z, Om, -1.0, 0.0)
    return k, pk[iz], f, s80, a_par, a_per


def _cheb(a, b, n):
    j = np.arange(n)
    return 0.5 * (a + b) + 0.5 * (b - a) * np.cos(np.pi * j / (n - 1)), (-1.0) ** j * np.where((j == 0) | (j == n - 1), 0.5, 1.0)


OM_N, OM_W = _cheb(*OM_EJE, N_OM)
H_N, H_W = _cheb(*H_EJE, N_H)


def _pesos(x, nodos, w):
    d = x - nodos
    j = int(np.argmin(np.abs(d)))
    if d[j] == 0.0:
        e = np.zeros(len(nodos)); e[j] = 1.0
        return e
    c = w / d
    return c / c.sum()


def construye_malla():
    """Y[z][iOm, ih, ilogA, l, k, termino] y s80[iOm, ih] (sigma8 total z=0 a A_REF)."""
    if os.path.exists(MALLA):
        return pickle.load(open(MALLA, 'rb'))
    t0 = time.time()
    out = dict(Y={}, s80=np.empty((N_OM, N_H)))
    for zb, z in MUESTRAS:
        Y = None
        for i, Om in enumerate(OM_N):
            for j, h in enumerate(H_N):
                kl, pl, f, s80, a_par, a_per = cosmo_camb(Om, h, z)
                _, Yn = R.tablas_logA(kl, pl, f, KMOD, a_par, a_per)
                if Y is None:
                    Y = np.empty((N_OM, N_H) + Yn.shape)
                Y[i, j] = Yn
                out['s80'][i, j] = s80
            print(f'  malla z={z}: Om nodo {i + 1}/{N_OM}  ({time.time() - t0:.0f} s)', flush=True)
        out['Y'][z] = Y
    os.makedirs(os.path.dirname(MALLA), exist_ok=True)
    pickle.dump(out, open(MALLA, 'wb'))
    print(f'  malla construida en {(time.time() - t0) / 60:.1f} min', flush=True)
    return out


def tablas(z, Om, h, logA):
    wo, wh, wa = _pesos(Om, OM_N, OM_W), _pesos(h, H_N, H_W), _pesos(logA, R.LOGA_NODOS, R._W_NODOS)
    return np.tensordot(wa, np.tensordot(wh, np.tensordot(wo, G['Y'][z], 1), 1), 1), float(wo @ G['s80'] @ wh)


def _observa(st, P):
    """P[l, k] en KMOD (l=0,2,4) -> vector convolucionado (l=0,2 en el rango): spline ext=3, ancla en 0, W M."""
    kv = np.append(0.0, KMOD)
    thy = np.concatenate([Spline(kv, np.append(0.0, P[l]), ext=3)(K400) for l in range(3)])
    return st['WM'] @ thy


def chi2_set(st, Y, b1, b2, bs):
    """chi2 marginal (lineales integrados con sus priors) + log det F."""
    mono = np.array([1, b1, b1 ** 2, b2, b1 * b2, b2 ** 2, bs, b1 * bs, b2 * bs, bs ** 2, 0.0, 0.0,
                     0, 0, 0, 0, 0, 0, 0])
    m0 = _observa(st, np.einsum('lkt,t->lk', Y, mono))
    T = np.stack([_observa(st, Y[:, :, c]) for c in COL_LIN], axis=1)
    Ci = st['Cinv']
    r = st['d'] - m0
    F = T.T @ Ci @ T + np.diag(1.0 / SIG_LIN ** 2)
    b = T.T @ Ci @ r
    return float(r @ Ci @ r - b @ np.linalg.solve(F, b) + np.linalg.slogdet(F)[1])


def dentro(Om, h, logA):
    return OM_EJE[0] <= Om <= OM_EJE[1] and H_EJE[0] <= h <= H_EJE[1] and R.LOGA_MIN <= logA <= R.LOGA_MAX


DERIV = ('sigma8', *[f'b1_{zb}{cap}' for zb, _ in MUESTRAS for cap in ('NGC', 'SGC')])


def loglike(Om, H0, logA, **b):
    h = H0 / 100.0
    if not dentro(Om, h, logA):
        return -np.inf, {d: np.nan for d in DERIV}
    tot, der, s8 = 0.0, {}, None
    pares = {}
    for st in SETS:
        Y, s80 = tablas(st['z'], Om, h, logA)
        s8 = s80 * np.sqrt(np.exp(logA) * 1e-10 / R.AS_REF)
        b1 = b[f'bsig8_{st["tag"]}'] / s8 - 1.0
        der[f'b1_{st["tag"]}'] = b1
        par = (st, Y, b1, b[f'b2_{st["tag"]}'], b[f'bs_{st["tag"]}'])
        if COV == 'chen':
            pares.setdefault(st['zb'], []).append(par)
        else:
            tot += chi2_set(*par)
    for zb, pp in pares.items():
        tot += chi2_muestra(zb, pp)
    der['sigma8'] = s8
    return -0.5 * tot, der


def _params():
    p = dict(Om=dict(prior=dict(min=0.20, max=0.40), ref=dict(dist='norm', loc=0.305, scale=0.01), proposal=0.005, latex=r'\Omega_m'),
             H0=dict(prior=dict(min=60.0, max=80.0), ref=dict(dist='norm', loc=68.5, scale=0.5), proposal=0.5, latex='H_0'),
             logA=dict(prior=dict(min=1.61, max=3.91), ref=dict(dist='norm', loc=2.84, scale=0.05), proposal=0.03, latex=r'\ln(10^{10}A_s)'))
    for st in SETS:
        t = st['tag']
        p[f'bsig8_{t}'] = dict(prior=dict(min=0.5, max=3.0), ref=dict(dist='norm', loc=1.5, scale=0.05), proposal=0.02)
        p[f'b2_{t}'] = dict(prior=dict(dist='norm', loc=0.0, scale=10.0), ref=dict(dist='norm', loc=0.0, scale=0.3), proposal=0.3)
        p[f'bs_{t}'] = dict(prior=dict(dist='norm', loc=0.0, scale=5.0), ref=dict(dist='norm', loc=0.0, scale=0.3), proposal=0.3)
    for d in DERIV:
        p[d] = dict(latex=d)
    return p


def prueba():
    """Malla interpolada contra tablas REHECHAS (con el mismo cb y la misma f) en puntos que no son nodos.

    CONTROL (R53): en los mismos puntos se mide tambien el metodo VIEJO (tabla a
    A_REF y salida escalada por A_s/A_REF, retirado el 2026-10-17). Tiene que
    errar mucho mas que la malla; si no, la prueba no distingue nada.
    Escribe results/logs/growth_2026-07/boss_chen21_malla.json (con acta).
    """
    import json
    sys.path.insert(0, os.path.join(_R, 'src'))
    from procedencia import con_acta
    rng = np.random.default_rng(20261019)
    peor = peor_viejo = 0.0
    puntos = []
    la_ref = np.log(R.AS_REF * 1e10)
    for _ in range(4):
        Om, h, la = rng.uniform(0.28, 0.33), rng.uniform(0.65, 0.72), rng.uniform(2.6, 3.1)
        ci = ce = cv = 0.0
        for st in SETS:
            Yi, _ = tablas(st['z'], Om, h, la)
            ci += chi2_set(st, Yi, 1.0, -1.0, 0.5)
            Yr, _ = tablas(st['z'], Om, h, la_ref)
            cv += chi2_set(st, Yr * np.exp(la) * 1e-10 / R.AS_REF, 1.0, -1.0, 0.5)
            kl, pl, f, _, a_par, a_per = cosmo_camb(Om, h, st['z'])
            from velocileptors.LPT.lpt_rsd_fftw import LPT_RSD
            L = LPT_RSD(kl, pl * np.exp(la) * 1e-10 / R.AS_REF, kIR=0.2, cutoff=10, extrap_min=-4, extrap_max=3, N=2000, threads=1, jn=5)
            L.make_pltable(f, kv=KMOD, apar=a_par, aperp=a_per, ngauss=3)
            ce += chi2_set(st, np.stack([L.p0ktable, L.p2ktable, L.p4ktable]), 1.0, -1.0, 0.5)
        peor, peor_viejo = max(peor, abs(ci - ce)), max(peor_viejo, abs(cv - ce))
        puntos.append(dict(Om=Om, h=h, logA=la, chi2_exacto=ce, d_interpolado=ci - ce, d_viejo=cv - ce))
        print(f'  Om={Om:.4f} h={h:.4f} logA={la:.4f}: exacto {ce:.4f}  interpolado {ci - ce:+.2e}  viejo {cv - ce:+.2e}', flush=True)
    pasa, distingue = peor < 0.05, peor_viejo > 10 * max(peor, 1e-6)
    print(f'  peor interpolado {peor:.2e} (criterio 0.05) · peor viejo {peor_viejo:.2e} -> '
          f'{"PASA" if pasa and distingue else "FALLA"}')
    out = os.path.join(_R, 'results', 'logs', 'growth_2026-07', 'boss_chen21_malla.json')
    json.dump(con_acta(dict(corrida='malla 7x7x13 de tablas LPT (Om, h, logA) contra tablas exactas',
                            criterio='|dchi2| < 0.05 en cada punto (fijado antes de correr); el metodo viejo '
                                     'tiene que errar mas de 10 veces lo que erra la malla',
                            puntos=puntos, peor_interpolado=peor, pasa=bool(pasa),
                            control_viejo=dict(maximo=peor_viejo, pasa=bool(distingue))),
                      __file__, entradas=[MALLA]), open(out, 'w'), indent=1)
    return peor if distingue else 1.0


SETS = construye_datos()
G = construye_malla()

if __name__ == '__main__':
    modo = _ARGV[1] if len(_ARGV) > 1 else 'prueba'
    if modo == 'prueba':
        sys.exit(0 if prueba() < 0.05 else 1)
    from cobaya.run import run
    chains = _ARGV[2] if len(_ARGV) > 2 else '/mnt/datos/SSEE_data/chains_p6/boss_chen21'
    p = _params()
    info = dict(likelihood={'boss_chen21': {'external': loglike, 'input_params': [k for k in p if 'prior' in p[k]],
                                            'output_params': list(DERIV)}},
                params=p, sampler={'mcmc': {'Rminus1_stop': 0.03, 'max_tries': 20000}},
                output=f'{chains}/lcdm_chen21' + ('_covchen' if COV == 'chen' else ''), force=True, resume=False)
    t0 = time.time()
    run(info)
    print(f'\nTERMINADO en {(time.time() - t0) / 3600:.2f} h', flush=True)
