#!/usr/bin/env python3
"""
TWO-SECTOR contra los 225 datos CRUDOS de KiDS-1000 (nada de S8).

P_2sec(k,z) = P_cold_nolineal(k,z) * T2_Boltzmann(k,z)

T2 sale de CLASS (t2_grid.npz), NO del ajuste de Viel (ese estaba calibrado a
WDM-100% y sobre-suprimia 125x en k=1). El fondo es el mismo en ambas corridas
de CLASS, asi que T2 aisla el free-streaming del sector phi.

LIMITACION DECLARADA: T2 es LINEAL. HMcode no converge con una componente WDM
al 48% de la materia (`counter > _MAX_IT_`), asi que la respuesta no lineal
DENTRO del sector phi no esta modelada. Es lo mejor disponible sin N-body
(OP-5 nivel 2). Es el mismo caveat que ya esta catalogado.

Optimizacion anidada: (logA, halo_A) por fuera -> exige CAMB;
                      (A_IA, 5 dz, dc)  por dentro -> no exige CAMB.
"""
import numpy as np, sys, json, time
sys.path.insert(0, '/tmp/claude-1000/-home-mike-Proyectos-SSEE/'
                   '238cf748-10c3-466e-9be3-e8e03009063e/scratchpad')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
import kids_shear as K
import ssee_core as S
from scipy.optimize import minimize
from scipy.interpolate import RectBivariateSpline

MODO = sys.argv[1] if len(sys.argv) > 1 else '2sec'   # '2sec' | 'cold'

# optimo de a1 (SSEE un sector, A_s libre): punto de partida
LOGA0, HALO0, AIA0 = 2.86706, 2.5943, 0.7494112825375345
DZ0 = np.array([0.009268853998142845, -0.0007208738943109349,
                -0.02364196026974763, -0.013731424780223267,
                0.0033114336988825264])
DC0 = -7.881448171632882e-06

D = K.load_data(); MASK = K.scale_mask(D)
CINV = np.linalg.inv(D['C'][np.ix_(MASK, MASK)])

G = np.load('t2_grid.npz')
T2SPL = RectBivariateSpline(G['zg'], np.log(G['kh']), np.log(G['T2']),
                            kx=1, ky=3)


def aplica_T2(kh, z_pk, pk):
    """multiplica P(k,z) por T2(k,z), con extrapolacion plana fuera de rango."""
    kk = np.clip(kh, G['kh'][0] * 1.001, G['kh'][-1] * 0.999)
    zz = np.clip(np.asarray(z_pk), G['zg'][0], G['zg'][-1])
    return pk * np.exp(T2SPL(zz, np.log(kk)))


def chi2_nuis(x, res, p, kh, zp, pk, gr):
    aia, dz, dc = x[0], x[1:6], x[6]
    e, Cl, ix = K.cl_shear(D, res, p, kh, zp, pk, gr, aia, dz)
    th = K.theory_vector(D, e, Cl, ix, delta_c=dc)
    dv = (th - D['d'])[MASK]
    return float(dv @ CINV @ dv)


CACHE = {}


def chi2_outer(logA, halo_A, refina=True):
    key = (round(logA, 5), round(halo_A, 4))
    if key in CACHE:
        return CACHE[key]
    res, p, kh, zp, pk, gr = K.run_camb(
        omch2=S.OMEGA_C_H2, ombh2=S.OMEGA_B_H2, h0=S.H0_GLOBAL / 100, ns=S.N_S,
        As=1e-10 * np.exp(logA), mnu=S.SUM_MNU_EV, w=S.W0, wa=S.WA,
        halo_A=halo_A)
    if MODO == '2sec':
        pk = aplica_T2(kh, zp, pk)
    x0 = np.concatenate([[AIA0], DZ0, [DC0]])
    if refina:
        r = minimize(chi2_nuis, x0, args=(res, p, kh, zp, pk, gr),
                     method='Powell',
                     options=dict(maxiter=2000, xtol=1e-3, ftol=1e-3))
        val, xb = float(r.fun), r.x
    else:
        val, xb = chi2_nuis(x0, res, p, kh, zp, pk, gr), x0
    CACHE[key] = (val, xb)
    print(f'    logA={logA:.5f} halo_A={halo_A:.4f} -> chi2={val:.4f}',
          flush=True)
    return CACHE[key]


if __name__ == '__main__':
    t0 = time.time()
    print(f'# MODO = {MODO}   ({MASK.sum()} de {len(D["d"])} puntos usados)',
          flush=True)
    print(f'# referencia a1 (un sector, A_s libre) = 263.820\n', flush=True)

    def f(v):
        return chi2_outer(v[0], np.clip(v[1], 2.0, 3.13))[0]

    r = minimize(f, [LOGA0, HALO0], method='Nelder-Mead',
                 options=dict(xatol=2e-3, fatol=5e-3, maxfev=60))
    logA, halo_A = r.x[0], float(np.clip(r.x[1], 2.0, 3.13))
    val, xb = chi2_outer(logA, halo_A)
    print(f'\n  OPTIMO {MODO}:  chi2 = {val:.4f}')
    print(f'    logA   = {logA:.5f}   (a1: {LOGA0:.5f}; CMB: 3.040704)')
    print(f'    halo_A = {halo_A:.4f}   (a1: {HALO0:.4f})')
    print(f'    A_IA   = {xb[0]:.4f}    dc = {xb[6]:.3e}')
    print(f'    dz     = ' + ' '.join(f'{v:+.5f}' for v in xb[1:6]))
    json.dump(dict(modo=MODO, chi2=val, logA=logA, halo_A=halo_A,
                   A_IA=xb[0], dz=list(xb[1:6]), dc=xb[6]),
              open(f'kids_{MODO}.json', 'w'), indent=1)
    print(f'\n  minutos: {(time.time()-t0)/60:.1f}')
