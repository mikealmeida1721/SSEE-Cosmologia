#!/usr/bin/env python3
"""
ssee_paper2_mcmc_wmfix.py — MCMC con la parametrización CORRECTA de SSEE.

QUÉ CORRIGE (hallazgo 2026-07-25)
---------------------------------
Los MCMC previos (`ssee_paper2_mcmc_reframe.py`, `ssee_paper2_mcmc.py`) mantenían
FIJA la FRACCIÓN Ω_m = 0.308881 y dejaban derivar ω_m = Ω_m·h² en cada paso:

    om_h2 = Omega_m_congelado x h^2           # <- parametrizacion invertida

Pero SSEE no predice Ω_m. SSEE predice el ABSOLUTO:

    ω_b = (π−φ)/(3Ω²)        = 0.02242      (OP-1)
    ω_c = KAL₀·ω_b·n_s       = 0.11951      (forward, Paper 1)
    ω_ν = Σm_ν/C_ν           = 0.000735
    ω_m = ω_b+ω_c+ω_ν        = 0.14267      ← ESTO es lo que fija el álgebra

Ω_m = ω_m/h² es DERIVADO. Al fijar Ω_m y mover H₀, el ω_m implícito se despega
de la predicción hasta ±1.8%, y coincide EXACTAMENTE sólo en H₀ = 67.962 — el
ancla. Es decir: la vieja parametrización evaluaba SSEE de verdad únicamente en
el ancla, y un modelo ligeramente distinto en todos los demás puntos, lo que
sesga hacia el ancla y contamina incluso la corrida con prior de Planck.

Aquí ω_m queda FIJO en su valor algebraico y Ω_m(H₀) = ω_m/h² se recalcula en
cada muestra, tanto en E(z) como en r_d. Es la única lectura fiel del modelo.

Uso:  python3 src/p02_mcmc/ssee_paper2_mcmc_wmfix.py [--prior anchor|planck]
"""
import argparse
import os
import sys
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, ".."))

import emcee  # noqa: E402
from ssee_core import (W0, WA, KAL0, OMEGA_M_H2 as WM_ALG,  # noqa: E402
                       OMEGA_M_TOTAL, H0_ALG, H0_GLOBAL, SIG_H0_GLOBAL)
from desi_dr2_data import load_desi_dr2, desi_covariance  # noqa: E402

C_KM = 299792.458

ap = argparse.ArgumentParser()
ap.add_argument("--prior", choices=["anchor", "planck"], default="anchor")
ap.add_argument("--steps", type=int, default=25000)
# --param Om_fixed reproduce la parametrización VIEJA: sirve de control. Si con
# ella este script recupera el 67.9475 publicado, la diferencia con wm_fixed es
# real y no un bug de esta implementación.
ap.add_argument("--param", choices=["wm_fixed", "Om_fixed"], default="wm_fixed")
args = ap.parse_args()

# Prior en H₀. 'anchor' = el ancla algebraica (test de CONSISTENCIA: ¿tira DESI?).
# 'planck' = independiente del ancla (¿hacia dónde empujan los datos por sí solos?).
PRIOR_H0 = (H0_GLOBAL, SIG_H0_GLOBAL) if args.prior == "anchor" else (67.36, 0.54)
BBN_OBH2 = (0.02218, 0.00055)  # prior BBN de DESI (Schöneberg 2024)

_d = load_desi_dr2()          # dict de arrays (fuente única data/raw/desi_dr2_bao.csv)
DESI_Z = np.asarray(_d["z"])
DESI_OBS = np.asarray(_d["value"])
DESI_TYPE = list(_d["quantity"])   # 'DV_over_rd' | 'DM_over_rd' | 'DH_over_rd'
DESI_COV_INV = np.linalg.inv(desi_covariance(_d))

CLUSTERS = [
    {"M_ig": 1.8, "M_obs": 9.8, "dM_obs": 1.0},
    {"M_ig": 2.2, "M_obs": 12.0, "dM_obs": 1.2},
    {"M_ig": 1.5, "M_obs": 8.0, "dM_obs": 1.0},
    {"M_ig": 1.2, "M_obs": 6.5, "dM_obs": 1.0},
]
FNU_SSEE = 0.0


def f_de_cpl(z, w0, wa):
    a = 1.0 / (1.0 + z)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))


def om_of(H0):
    """Ω_m DERIVADO de ω_m algebraico fijo — el punto de todo el arreglo.
    En modo Om_fixed (control) devuelve la fracción congelada, como el script viejo."""
    if args.param == "Om_fixed":
        return OMEGA_M_TOTAL
    return WM_ALG / (H0 / 100.0) ** 2


def E_ssee(z, Om):
    return np.sqrt(Om * (1 + z) ** 3 + (1.0 - Om) * f_de_cpl(z, W0, WA))


def DC(z_max, Om, n=300):
    zz = np.linspace(0, z_max, n)
    return np.trapezoid(1.0 / E_ssee(zz, Om), zz)


import os as _os_rd, sys as _sys_rd
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), ".."))
from rd_camb import rd_mpc as _rd_camb  # r_d de CAMB, una sola funcion (2026-09-28)


def sound_horizon_rd(ob_h2, om_h2):
    return _rd_camb(ob_h2, om_h2, mnu=None)  # CAMB; antes 147.27*(...) con normalizacion 0.15 % alta


def predict_desi(H0, Om, rd):
    preds = []
    for z, qty in zip(DESI_Z, DESI_TYPE):
        dm = (C_KM / H0) * DC(z, Om)
        dh = C_KM / (H0 * E_ssee(z, Om))
        if qty == "DM_over_rd":
            preds.append(dm / rd)
        elif qty == "DH_over_rd":
            preds.append(dh / rd)
        else:
            preds.append((z * dm ** 2 * dh) ** (1 / 3) / rd)
    return np.array(preds)


LL_CLUSTERS = -0.5 * sum(((c["M_ig"] * KAL0 * (1 + FNU_SSEE) - c["M_obs"])
                          / c["dM_obs"]) ** 2 for c in CLUSTERS)


def lpost(theta):
    H0, ob_h2 = theta
    if not (40 < H0 < 100):
        return -np.inf
    if not (0.015 < ob_h2 < 0.030):
        return -np.inf
    Om = om_of(H0)                      # ← DERIVADO, no fijo
    om_h2 = (OMEGA_M_TOTAL * (H0 / 100.0) ** 2 if args.param == "Om_fixed"  # R25-control
             else WM_ALG)               # ← ω_m algebraico FIJO (la predicción)
    rd = sound_horizon_rd(ob_h2, om_h2)
    r = predict_desi(H0, Om, rd) - DESI_OBS
    lp_H0 = -0.5 * ((H0 - PRIOR_H0[0]) / PRIOR_H0[1]) ** 2
    lp_bbn = -0.5 * ((ob_h2 - BBN_OBH2[0]) / BBN_OBH2[1]) ** 2
    return lp_H0 + lp_bbn - 0.5 * (r @ DESI_COV_INV @ r) + LL_CLUSTERS


print("SSEE — MCMC con parametrización CORRECTA (ω_m algebraico fijo)")
print(f"  prior H₀   = {PRIOR_H0[0]:.3f} ± {PRIOR_H0[1]:.2f}  [{args.prior}]  param={args.param}")
print(f"  ω_m fijo   = {WM_ALG:.7f}   (ω_b+ω_c+ω_ν algebraicos)")
print(f"  Ω_m        = ω_m/h², derivado por muestra "
      f"(en H₀={H0_ALG:.3f} da {om_of(H0_ALG):.5f}; el viejo fijaba {OMEGA_M_TOTAL:.5f})")

N_W, N_B = 100, 5000
p0 = np.array([PRIOR_H0[0], BBN_OBH2[0]]) + 1e-3 * np.random.randn(N_W, 2)
t0 = time.time()
sampler = emcee.EnsembleSampler(N_W, 2, lpost)
sampler.run_mcmc(p0, args.steps, progress=False)
ch = sampler.get_chain(discard=N_B, flat=True)

H0_med = np.median(ch[:, 0])
H0_lo, H0_hi = np.percentile(ch[:, 0], [15.865, 84.135])
ob_med = np.median(ch[:, 1])
print(f"\n--- RESULTADO ({time.time()-t0:.1f}s, {N_W}w × {args.steps}s) ---")
print(f"  H₀    = {H0_med:.4f}  +{H0_hi-H0_med:.4f}/-{H0_med-H0_lo:.4f} km/s/Mpc")
print(f"  Ω_b h²= {ob_med:.5f}")
print(f"  Ω_m(H₀ post) = {om_of(H0_med):.5f}")
_s = (H0_hi - H0_lo) / 2
print(f"  distancia al ancla {H0_ALG:.3f}: {abs(H0_med-H0_ALG)/_s:.2f}σ")
_omh2_post = (OMEGA_M_TOTAL*(H0_med/100)**2 if args.param=="Om_fixed" else WM_ALG)
print(f"  r_d = {sound_horizon_rd(ob_med, _omh2_post):.2f} Mpc")
_r = predict_desi(H0_med, om_of(H0_med), sound_horizon_rd(ob_med, _omh2_post)) - DESI_OBS
print(f"  χ²_BAO en el posterior = {_r @ DESI_COV_INV @ _r:.2f}  (13 puntos)")
