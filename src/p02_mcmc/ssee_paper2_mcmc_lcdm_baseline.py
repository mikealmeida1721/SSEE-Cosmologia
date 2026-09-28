"""
SSEE Paper 2 — ΛCDM baseline MCMC (igual datos que SSEE-MIRA)
==============================================================
Para ΔBIC limpio vs SSEE-MIRA, corremos ΛCDM con:
  - Mismos datos DESI DR2 (covarianza block-diagonal)
  - Mismos cúmulos
  - Mismos BBN
  - Prior Planck 3D nativo (no MIRA — ΛCDM no usa MIRA)
  - 100w × 25k (mismo tamaño)
"""
# ORIGEN-VALOR: 0.1432 — pivote omega_m h^2 de la eq. rd de Paper 2 (Planck 2018 TT,TE,EE+lowE); cita EH98 en FUENTES_PENDIENTES.md FP-7
import numpy as np
import time, os, sys, warnings
_SSEE_DATA = os.environ.get("SSEE_DATA_DIR") or ("/mnt/datos/SSEE_data" if os.path.isdir("/mnt/datos") else "results/data")  # portable: HDD si existe, si no results/ local
warnings.filterwarnings("ignore")
import emcee
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import corner

sys.path.insert(0, os.path.dirname(__file__))

t0 = time.time()
LOG = "results/logs/mcmc_paper2_lcdm_baseline.log"
# Regla de disco: chain al HDD
CKPT = _SSEE_DATA + "/mcmc/paper2_3models/mcmc_paper2_lcdm_baseline_ckpt.npz"
OUT = "results/figures"
os.makedirs("results/logs", exist_ok=True)
os.makedirs(OUT, exist_ok=True)

def log(msg):
    line = f"[{(time.time()-t0)/60:6.1f}m] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f: f.write(line + "\n")

log("=" * 70)
log("ΛCDM BASELINE — MCMC PRODUCCIÓN (para ΔBIC vs SSEE-MIRA)")
log("=" * 70)

C_KM = 2.998e5

# Datos DESI DR2
# ── DESI DR2 (2503.14738 Tabla 4) — FUENTE ÚNICA data/raw/desi_dr2_bao.csv ──
# NO hardcodear (drift DR1/DR2 corregido 2026-07-02; guardián R14).
import os as _dd_os, sys as _dd_sys
_dd_sys.path.insert(0, _dd_os.path.join(_dd_os.path.dirname(_dd_os.path.dirname(
    _dd_os.path.abspath(__file__)))))
from desi_dr2_data import load_desi_dr2 as _dd_load, desi_covariance as _dd_cov
_DESI_D      = _dd_load()
DESI_Z       = list(_DESI_D["z"])
_DD_QSHORT   = {"DM_over_rd": "DM_rd", "DH_over_rd": "DH_rd", "DV_over_rd": "DV_rd"}
DESI_TYPE    = [_DD_QSHORT[q] for q in _DESI_D["quantity"]]
DESI_OBS     = _DESI_D["value"]
DESI_SIGMA   = _DESI_D["sigma"]
DESI_COV     = _dd_cov(_DESI_D)          # bloque-diagonal, r_MH oficiales DR2
DESI_COV_INV = np.linalg.inv(DESI_COV)

# Prior Planck 3D (correlacionado)
PLANCK_H0   = (67.36, 0.54)
PLANCK_OM   = (0.3153, 0.0073)
PLANCK_OBH2 = (0.02237, 0.00015)
RHO_H0_OM   = -0.85

s0, s1, s2 = PLANCK_H0[1], PLANCK_OM[1], PLANCK_OBH2[1]
PLANCK_COV_INV = np.linalg.inv(np.array([
    [s0**2,           RHO_H0_OM*s0*s1, 0.0   ],
    [RHO_H0_OM*s0*s1, s1**2,           0.0   ],
    [0.0,             0.0,             s2**2 ],
]))
PLANCK_MU = np.array([PLANCK_H0[0], PLANCK_OM[0], PLANCK_OBH2[0]])

# Cúmulos (Zhang 2026)
KAL0_v = 5.521405974759637   # ssee_core KAL0
FNU = 0.020
CLUSTERS = [
    {"M_ig": 1.8, "dM_obs": 1.0, "M_obs": 9.8 },
    {"M_ig": 2.2, "dM_obs": 1.2, "M_obs": 12.0},
    {"M_ig": 1.5, "dM_obs": 1.0, "M_obs": 8.0 },
    {"M_ig": 1.2, "dM_obs": 1.0, "M_obs": 6.5 },
]
LL_CLUSTERS = -0.5 * sum(((c["M_ig"]*KAL0_v*(1+FNU) - c["M_obs"])/c["dM_obs"])**2
                         for c in CLUSTERS)

def E_lcdm(z, Om):
    return np.sqrt(Om*(1+z)**3 + (1-Om))

def DC(z_max, Om, n=300):
    zz = np.linspace(0, z_max, n)
    return np.trapezoid(1.0/E_lcdm(zz, Om), zz)

import os as _os_rd, sys as _sys_rd
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), ".."))
from rd_camb import rd_mpc as _rd_camb  # r_d de CAMB, una sola funcion (2026-09-28)
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), "..", "p11_sondas"))  # lcdm_planck: la mnu de LCDM


def sound_horizon_rd(ob_h2, om_h2):
    return _rd_camb(ob_h2, om_h2, mnu=__import__("lcdm_planck").LCDM_PLANCK["mnu"])  # CAMB; antes 147.27*(...) con normalizacion 0.15 % alta

def predict_desi(H0, Om, rd):
    preds = []
    for z, qty in zip(DESI_Z, DESI_TYPE):
        dm = (C_KM/H0) * DC(z, Om)
        dh = C_KM / (H0 * E_lcdm(z, Om))
        if qty == "DM_rd":   preds.append(dm/rd)
        elif qty == "DH_rd": preds.append(dh/rd)
        else:                preds.append((z*dm**2*dh)**(1/3)/rd)
    return np.array(preds)

def ll_planck(H0, Om, ob_h2):
    dv = np.array([H0-PLANCK_MU[0], Om-PLANCK_MU[1], ob_h2-PLANCK_MU[2]])
    return -0.5 * (dv @ PLANCK_COV_INV @ dv)

def ll_bao(H0, Om, ob_h2):
    om_h2 = Om*(H0/100)**2
    rd = sound_horizon_rd(ob_h2, om_h2)
    r  = predict_desi(H0, Om, rd) - DESI_OBS
    return -0.5 * (r @ DESI_COV_INV @ r)

def lpost(theta):
    H0, Om, ob_h2 = theta
    if not (40 < H0 < 100): return -np.inf
    if not (0.15 < Om < 0.55): return -np.inf
    if not (0.015 < ob_h2 < 0.030): return -np.inf
    return ll_planck(H0, Om, ob_h2) + ll_bao(H0, Om, ob_h2) + LL_CLUSTERS

# MCMC
N_W, N_S, N_B, SAVE = 100, 25000, 5000, 500
rng = np.random.default_rng(42)
pos = np.array([67.4, 0.315, 0.02237]) + rng.standard_normal((N_W, 3)) * np.array([1.5, 0.015, 0.0003])
sampler = emcee.EnsembleSampler(N_W, 3, lpost)

log(f"\nBurn-in {N_B} steps...")
pos, _, _ = sampler.run_mcmc(pos, N_B, progress=False)
sampler.reset()
log("Producción...")

all_chains = []
for i in range(0, N_S, SAVE):
    pos, _, _ = sampler.run_mcmc(pos, SAVE, progress=False)
    all_chains.append(sampler.get_chain(flat=True))
    log(f"  {i+SAVE}/{N_S} steps  accept={np.mean(sampler.acceptance_fraction):.3f}")
    np.savez(CKPT, chain=np.concatenate(all_chains, axis=0))

flat = sampler.get_chain(flat=True)
lp   = sampler.get_log_prob(flat=True)
mask = np.isfinite(lp)
idx  = np.argmax(lp) if np.any(mask) else 0
try:
    tau = sampler.get_autocorr_time(quiet=True)
    n_eff = N_W * N_S / np.max(tau)
except Exception:
    tau, n_eff = np.array([np.nan]), np.nan

H0_med = np.median(flat[:,0]); H0_std = np.std(flat[:,0])
Om_med = np.median(flat[:,1]); Om_std = np.std(flat[:,1])
ob_med = np.median(flat[:,2])

log("\n" + "=" * 70)
log("ΛCDM BASELINE — RESULTADO")
log("=" * 70)
log(f"  H₀     = {H0_med:.4f} ± {H0_std:.4f}")
log(f"  Ω_m    = {Om_med:.5f} ± {Om_std:.5f}")
log(f"  Ω_b·h² = {ob_med:.5f}")
log(f"  ln P_MAP = {lp[idx]:.3f}")
log(f"  τ_max = {np.max(tau):.1f}    N_eff ≈ {n_eff:.0f}")
log(f"  acceptance = {np.mean(sampler.acceptance_fraction):.3f}")

N_data = 13 + 3  # 13 BAO + 3 Planck constraints
BIC = 3 * np.log(N_data) - 2 * lp[idx]
log(f"\n  BIC (k=3, N={N_data}): {BIC:.3f}")
log(f"\n  Para ΔBIC vs SSEE-MIRA: SSEE_BIC = 253.435 (k=2, N=15)")
log(f"                          ΛCDM_BIC = {BIC:.3f} (k=3, N={N_data})")
log(f"                          ΔBIC = {BIC - 253.435:+.3f}  (>0 favorece SSEE)")
log(f"\nTiempo total: {(time.time()-t0)/60:.1f} min")
