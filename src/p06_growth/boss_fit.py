#!/usr/bin/env python3
"""
Ajuste de SSEE y LCDM a los multipolos CRUDOS de BOSS DR12.

Que se mide: la AMPLITUD que el agrupamiento de galaxias prefiere, con los
ingredientes de fondo FIJOS (algebraicos en SSEE, Planck en LCDM). Es el mismo
ejercicio que se hizo con la cizalla de KiDS, sobre la otra sonda de crecimiento.

Libres, identicos en los dos modelos:
    logA                    (1)  -- amplitud primordial, ln(1e10 A_s)
    b1  x 6                 (6)  -- bias lineal, uno por (z_bin, hemisferio)
    sig_v x 6               (6)  -- dispersion de velocidades, Mpc/h
  ------------------------------
                           13 libres contra 222 puntos

A_s entra como factor EXACTO en P_lin (teoria lineal), asi que CAMB se corre una
sola vez por cosmologia y por z: el ajuste no re-llama al Boltzmann.

Correccion de Hartlap aplicada: la covarianza viene de 2045/2048 mocks PATCHY,
un numero finito, y su inversa esta sesgada por (N-p-2)/(N-1).
"""
import json
import sys
import time

import numpy as np
import camb
from scipy.interpolate import InterpolatedUnivariateSpline as Spl
from scipy.optimize import minimize

sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src/p06_growth')
import ssee_core as S
import boss_rsd_model as M
from boss_dr12_data import ZBINS, CAPS, NMOCKS, load_multipole, load_cov, load_window

np.seterr(all='ignore')

KMAX = float(sys.argv[1]) if len(sys.argv) > 1 else 0.15
OUT = '/home/mike/Proyectos/SSEE/results/logs/growth_2026-07'

# --------------------------------------------------------------
#  Las dos cosmologias de fondo. Ninguna se ajusta.
# --------------------------------------------------------------
COSMO = {
    'SSEE': dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2, H0=S.H0_GLOBAL,
                 ns=S.N_S, mnu=S.SUM_MNU_EV, w0=S.W0, wa=S.WA),
    'LCDM': dict(ombh2=0.02237, omch2=0.1200, H0=67.36,
                 ns=0.9649, mnu=0.06, w0=-1.0, wa=0.0),
}
AS_REF = 2.1e-9          # normalizacion de referencia; logA la reescala


def camb_run(c, zs):
    """P_lin(k) y f(z) para cada z. A_s se factoriza fuera."""
    p = camb.CAMBparams()
    p.set_cosmology(H0=c['H0'], ombh2=c['ombh2'], omch2=c['omch2'], mnu=c['mnu'])
    p.InitPower.set_params(As=AS_REF, ns=c['ns'])
    if c['w0'] != -1.0 or c['wa'] != 0.0:
        p.set_dark_energy(w=c['w0'], wa=c['wa'], dark_energy_model='ppf')
    p.set_matter_power(redshifts=list(zs), kmax=30.0)
    r = camb.get_results(p)
    kh, zout, pk = r.get_matter_power_spectrum(minkh=1e-4, maxkh=25.0,
                                               npoints=800)
    s8 = np.array(r.get_sigma8())          # CAMB devuelve z decreciente
    fs8 = np.array(r.get_fsigma8())
    out = {}
    for i, z in enumerate(zout):
        j = int(np.argmin(np.abs(np.array(zs) - z)))
        sp = Spl(np.log(kh), np.log(pk[i]), k=3)
        klo, khi, nlo = kh[0], kh[-1], c['ns']

        def plin(x, sp=sp, klo=klo, khi=khi, nlo=nlo):
            x = np.clip(np.asarray(x), 1e-8, 1e4)
            base = np.exp(sp(np.log(np.clip(x, klo, khi))))
            return base * np.where(x < klo, (x / klo) ** nlo, 1.0) \
                        * np.where(x > khi, (x / khi) ** -3.0, 1.0)

        # f = (f sigma8)/sigma8, ambos de CAMB al mismo z
        m = int(np.argmin(np.abs(np.array(r.transfer_redshifts) - z)))
        out[zs[j]] = dict(plin=plin, f=float(fs8[m] / s8[m]),
                          sigma8=float(s8[m]))
    return out


# --------------------------------------------------------------
#  Datos: 6 conjuntos (3 z x 2 hemisferios)
# --------------------------------------------------------------
def build():
    sets = []
    for zb, zeff in ZBINS.items():
        for cap in CAPS:
            d, kk, ee = [], [], []
            for ell in (0, 2, 4):
                k, P, _ = load_multipole(zb, cap, ell)
                d.append(P); kk.append(k); ee.append(np.full(len(k), ell))
            k_all = np.concatenate(kk); ell_all = np.concatenate(ee)
            P_all = np.concatenate(d)
            C, kc, ellc = load_cov(zb, cap)

            # alinear la covarianza con el vector de datos por (ell, k)
            idx = [int(np.argmin(np.abs(kc - kv) + 1e3 * (ellc != ev)))
                   for kv, ev in zip(k_all, ell_all)]
            C = C[np.ix_(idx, idx)]

            keep = k_all <= KMAX
            C = C[np.ix_(keep, keep)]
            n_p = int(keep.sum())
            hart = (NMOCKS[cap] - n_p - 2.0) / (NMOCKS[cap] - 1.0)
            sets.append(dict(zb=zb, cap=cap, z=zeff, k=k_all[keep],
                             ell=ell_all[keep], P=P_all[keep],
                             Cinv=np.linalg.inv(C) * hart, hartlap=hart,
                             npts=n_p,
                             win=M.Window(*load_window(zb, cap),
                                          integral_constraint=True)))
    return sets


def predict(st, cam, cos, logA, b1, sv):
    """multipolos predichos en los k del dato, ya convolucionados."""
    c = cam[st['z']]
    a_par, a_per = M.alphas(st['z'], cos['Om'], cos['w0'], cos['wa'])
    scale = np.exp(logA) * 1e-10 / AS_REF
    P0, P2, P4 = M.multipoles(M.K_MODEL, c['plin'], c['f'], b1, sv,
                              a_par, a_per)
    ks, q0, q2, q4 = st['win'](M.K_MODEL, P0, P2, P4)
    out = np.empty(len(st['k']))
    for ell, q in ((0, q0), (2, q2), (4, q4)):
        m = st['ell'] == ell
        out[m] = np.interp(st['k'][m], ks, q)
    return out * scale


def chi2(theta, sets, cam, cos):
    logA = theta[0]
    tot = 0.0
    for i, st in enumerate(sets):
        b1, sv = theta[1 + 2 * i], theta[2 + 2 * i]
        if not (0.5 < b1 < 5.0 and 0.0 <= sv < 30.0):
            return 1e10
        r = st['P'] - predict(st, cam, cos, logA, b1, sv)
        tot += float(r @ st['Cinv'] @ r)
    return tot


def _chi2_bin(p, st, cam, cos, logA):
    b1, sv = p
    if not (0.5 < b1 < 5.0 and 0.0 <= sv < 30.0):
        return 1e10
    r = st['P'] - predict(st, cam, cos, logA, b1, sv)
    return float(r @ st['Cinv'] @ r)


def profile(logA, sets, cam, cos, warm):
    """
    chi2 minimizado sobre (b1, sig_v) de CADA conjunto, con logA fijo.

    Los seis conjuntos son independientes entre si una vez fijada la amplitud:
    esto convierte un Nelder-Mead de 13 dimensiones (decenas de miles de
    evaluaciones, horas) en seis de 2 dimensiones, y de paso entrega la curva
    chi2(logA) directamente, que es la cantidad de interes.
    """
    tot, pars = 0.0, []
    for i, st in enumerate(sets):
        r = minimize(_chi2_bin, warm[i], args=(st, cam, cos, logA),
                     method='Nelder-Mead',
                     options=dict(xatol=1e-4, fatol=1e-3, maxfev=600))
        tot += r.fun
        pars.append(r.x)
        warm[i] = r.x                       # arranque caliente para el paso
    return tot, pars


def run(name, sets):
    c = COSMO[name]
    h = c['H0'] / 100.0
    om = (c['ombh2'] + c['omch2'] + c['mnu'] / 93.14) / h ** 2
    cos = dict(Om=om, w0=c['w0'], wa=c['wa'])
    zs = sorted({st['z'] for st in sets})
    t0 = time.time()
    cam = camb_run(c, zs)
    print(f'\n  {name}:  Om_total={om:.6f}  h={h:.5f}  w0={c["w0"]:.4f} '
          f'wa={c["wa"]:.4f}   (CAMB {time.time()-t0:.1f}s)')
    for z in zs:
        ap, aq = M.alphas(z, om, c['w0'], c['wa'])
        print(f'      z={z}:  f={cam[z]["f"]:.5f}  sigma8={cam[z]["sigma8"]:.5f}'
              f'  alpha_par={ap:.5f}  alpha_perp={aq:.5f}')

    # barrido en logA con (b1, sig_v) perfilados; la curva ES el resultado
    grid = np.arange(2.55, 3.46, 0.05)
    warm = [np.array([1.9, 4.0]) for _ in sets]
    curve = []
    for la in grid:
        c2, _ = profile(la, sets, cam, cos, warm)
        curve.append(c2)
        print(f'        logA={la:.3f}  chi2={c2:9.3f}', flush=True)
    curve = np.array(curve)

    # refinado parabolico alrededor del minimo del barrido
    j = int(np.argmin(curve))
    lo, hi = grid[max(j - 1, 0)], grid[min(j + 1, len(grid) - 1)]
    fine = np.linspace(lo, hi, 11)
    warm = [np.array([1.9, 4.0]) for _ in sets]
    fc, fp = [], []
    for la in fine:
        c2, pp = profile(la, sets, cam, cos, warm)
        fc.append(c2); fp.append(pp)
    fc = np.array(fc)
    jf = int(np.argmin(fc))
    logA, best, pars = float(fine[jf]), float(fc[jf]), fp[jf]

    # incertidumbre de logA por Delta chi2 = 1 sobre la curva perfilada
    allA = np.concatenate([grid, fine]); allC = np.concatenate([curve, fc])
    o = np.argsort(allA); allA, allC = allA[o], allC[o]
    d = allC - best
    try:
        left = np.interp(1.0, d[allA <= logA][::-1], allA[allA <= logA][::-1])
        right = np.interp(1.0, d[allA >= logA], allA[allA >= logA])
        sig_logA = 0.5 * (right - left)
    except Exception:
        sig_logA = float('nan')

    n = sum(st['npts'] for st in sets)
    dof = n - (1 + 2 * len(sets))
    print(f'      chi2 = {best:.3f}   dof = {dof}   chi2/dof = {best/dof:.4f}')
    print(f'      logA = {logA:.5f} +- {sig_logA:.5f}   '
          f'(A_s = {np.exp(logA)*1e-10:.4e})')
    res = type('R', (), dict(x=np.concatenate([[logA]] + [p for p in pars]),
                             fun=best))()
    sc = np.sqrt(np.exp(logA) * 1e-10 / AS_REF)
    out = dict(model=name, chi2=float(res.fun), dof=int(dof), npts=int(n),
               logA=float(logA), sig_logA=float(sig_logA), kmax=KMAX,
               Om=om, w0=c['w0'], wa=c['wa'],
               curve=dict(logA=allA.tolist(), chi2=allC.tolist()), bins=[])
    for i, st in enumerate(sets):
        b1, sv = res.x[1 + 2 * i], res.x[2 + 2 * i]
        s8 = cam[st['z']]['sigma8'] * sc
        f = cam[st['z']]['f']
        print(f'      {st["zb"]} {st["cap"]}: b1={b1:.4f}  sig_v={sv:.3f}'
              f'   f*sigma8 = {f*s8:.5f}')
        out['bins'].append(dict(zb=st['zb'], cap=st['cap'], z=st['z'],
                                b1=float(b1), sig_v=float(sv),
                                f=float(f), sigma8=float(s8),
                                fsigma8=float(f * s8)))
    return out


if __name__ == '__main__':
    print('=' * 78)
    print(f'  BOSS DR12 full-shape — ajuste con fondo FIJO   (k_max = {KMAX})')
    print('=' * 78)
    sets = build()
    n = sum(st['npts'] for st in sets)
    print(f'  {len(sets)} conjuntos, {n} puntos, 13 libres '
          f'(logA + 6 b1 + 6 sig_v)')
    print(f'  Hartlap: ' + '  '.join(f'{st["cap"]}/{st["zb"]}='
                                     f'{st["hartlap"]:.4f}' for st in sets[:2]))
    r = {m: run(m, sets) for m in ('LCDM', 'SSEE')}
    print('\n' + '=' * 78)
    print(f'  Delta chi2 (LCDM - SSEE) = {r["LCDM"]["chi2"]-r["SSEE"]["chi2"]:+.3f}'
          f'   con los MISMOS 13 libres')
    print(f'  logA:  LCDM {r["LCDM"]["logA"]:.5f}   SSEE {r["SSEE"]["logA"]:.5f}')
    with open(f'{OUT}/boss_fit_kmax{KMAX:.3f}.json', 'w') as fh:
        json.dump(r, fh, indent=1)
    print(f'  -> {OUT}/boss_fit_kmax{KMAX:.3f}.json')
