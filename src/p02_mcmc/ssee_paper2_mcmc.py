"""
SSEE — MCMC Profesional (overnight run)
  1. Covarianza DESI block-diagonal 13×13 (Abdul-Karim et al. 2025, same-bin correlated)
  2. N_walkers=100, N_steps=25000, N_burn=5000  →  N_eff >> 1000 por parámetro
  3. Guardado incremental de cadenas (.npz) cada 500 pasos (no se pierde nada si se corta)
  4. Log en tiempo real con progress=False (para nohup)
  5. Figura corner + posterior predictive check guardados automáticamente
"""

import numpy as np
from scipy import integrate, stats
import warnings, time, sys, os
warnings.filterwarnings("ignore")

import emcee
import corner

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

t0 = time.time()

LOG_FILE = "results/logs/mcmc_professional.log"
OUT_DIR  = "results/figures"
# Portable: chains (~GB) al HDD si existe (regla de disco), a results/ en otra PC.
# Override con:  export SSEE_DATA_DIR=/ruta/a/disco/grande
_DATA = os.environ.get("SSEE_DATA_DIR") or ("/mnt/datos/SSEE_data" if os.path.isdir("/mnt/datos") else "results/data")
CHAIN_FILE = os.path.join(_DATA, "mcmc/paper2_3models/mcmc_chains_professional.npz")
os.makedirs("results/logs", exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CHAIN_FILE), exist_ok=True)

def log(msg):
    elapsed = (time.time()-t0)/60
    line = f"[{elapsed:6.1f}m] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

log("=" * 65)
log("SSEE — MCMC PROFESIONAL (overnight)")
log("=" * 65)

# ─────────────────────────────────────────────────────────────
# 1. CONSTANTES SSEE
# ─────────────────────────────────────────────────────────────
import os as _reloc_os, sys as _reloc_sys  # reloc: anclar src/
_reloc_sys.path.insert(0, _reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__))))
from ssee_core import (
    PHI, PI, BETA, KAL0, P_SC as P_sc, K_V as KV, T_R as TR, M_V as MV,
    W0 as W0_SSEE, WA as WA_SSEE, OMEGA_DE as OMDE_SSEE,
    OMEGA_M_TOTAL as OM_GEOM,      # 0.308881 — Ω_m en el ancla (diagnóstico; NO congelar en el MCMC)
    OMEGA_M_H2 as WM_ALG,          # 0.14267 — ω_m algebraico: lo que SSEE realmente fija
    OMEGA_CDM_SECTOR as OM_SECTOR, # 0.160050 = 1+w0, número de la ECUACIÓN DE ESTADO.
                                   # NO es una densidad y NUNCA entra en geometría. La
                                   # etiqueta «sector frío (Paper 6)» era del sector
                                   # retirado el 2026-08-01; corregida 2026-09-26.
)

log(f"w0={W0_SSEE:.4f}  wa={WA_SSEE:.4f}  Om_total={OM_GEOM:.5f} (geometría, ÚNICA densidad)  s_m=1+w0={OM_SECTOR:.6f} (ecuación de estado, NO densidad)  KAL0={KAL0:.4f}")

# ─────────────────────────────────────────────────────────────
# 2. FÍSICA DEL FONDO
# ─────────────────────────────────────────────────────────────
C_KM = 2.998e5

def f_de_cpl(z, w0, wa):
    a = 1.0 / (1.0 + z)
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*(1-a))

def E_ssee(z, Om):
    # Geometría de fondo: usa la materia TOTAL, NUNCA el sector frío 0.160 (=1+w0);
    # meterlo daba el χ²=726 espurio con DESI DR2 (V-L4-DESI, 2026-07-09).
    #
    # PARAMETRIZACIÓN (corregida 2026-07-25): Om llega como ARGUMENTO porque SSEE
    # fija ω_m = ω_b+ω_c+ω_ν = 0.14267 (absoluto, algebraico) y Ω_m = ω_m/h² es
    # DERIVADO. Antes Ω_m=0.308881 estaba congelado dentro de la función: al variar
    # H₀ el ω_m implícito se despegaba hasta ±1.8% de la predicción de SSEE, y sólo
    # coincidía en H₀=67.962 — el ancla. Eso evaluaba SSEE fielmente sólo ahí y un
    # modelo ligeramente distinto en el resto, sesgando el posterior hacia el ancla.
    return np.sqrt(Om*(1+z)**3 + (1.0-Om)*f_de_cpl(z, W0_SSEE, WA_SSEE))

def E_lcdm(z, Om):
    return np.sqrt(Om*(1+z)**3 + (1-Om))

def E_cpl(z, Om, w0, wa):
    return np.sqrt(Om*(1+z)**3 + (1-Om)*f_de_cpl(z, w0, wa))

def DC(z_max, E_func, n=300):
    zz = np.linspace(0, z_max, n)
    return np.trapezoid(1.0/E_func(zz), zz)

import os as _os_rd, sys as _sys_rd
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), ".."))
from rd_camb import rd_mpc as _rd_camb  # r_d de CAMB, una sola funcion (2026-09-28)


def sound_horizon_rd(ob_h2, om_h2, mnu=None):
    # CAMB; antes 147.27*(...) con normalizacion 0.15 % alta. mnu=None = la de SSEE;
    # LCDM y CPL pasan la SUYA (0.06, lcdm_planck.py) desde 2026-09-29: antes usaban la de SSEE.
    return _rd_camb(ob_h2, om_h2, mnu=mnu)


_reloc_sys.path.insert(0, _reloc_os.path.join(_reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__))), "p11_sondas"))
_MNU_LCDM = __import__("lcdm_planck").LCDM_PLANCK["mnu"]

# ─────────────────────────────────────────────────────────────
# 3. DATOS
# ─────────────────────────────────────────────────────────────

# Vectores de observables DESI DR2 (en el mismo orden que la covarianza)
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

# Prior comprimido Planck 2018
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


# Cronometros: los 32 de Moresco+2022 del CSV cotejado (2026-10-02). Antes 11 tecleados aqui,
# uno de ellos (z=0.44, 82.6+-7.8) el H(z) BAO de WiggleZ, que no es un cronometro.
import csv as _csv_cc
_CC_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "raw", "cosmic_chronometers.csv")
CC_DATA = np.array([[float(f["z"]), float(f["Hz"]), float(f["sigma_Hz"])]
                    for f in _csv_cc.DictReader(l for l in open(_CC_CSV) if not l.startswith("#"))])
Z_CC, H_CC, DH_CC = CC_DATA[:,0], CC_DATA[:,1], CC_DATA[:,2]

# ─────────────────────────────────────────────────────────────
# 4. LOG-LIKELIHOODS
# ─────────────────────────────────────────────────────────────

def predict_desi(H0, rd, E_func, *Eargs):
    preds = []
    for z, qty in zip(DESI_Z, DESI_TYPE):
        dm = (C_KM/H0) * DC(z, lambda zz: E_func(zz, *Eargs))
        dh = C_KM / (H0 * E_func(z, *Eargs))
        if qty == "DM_rd":   preds.append(dm / rd)
        elif qty == "DH_rd": preds.append(dh / rd)
        else:                preds.append((z*dm**2*dh)**(1/3) / rd)
    return np.array(preds)

def ll_bao_full(H0, om_h2, ob_h2, E_func, *Eargs, mnu=None):
    rd = sound_horizon_rd(ob_h2, om_h2, mnu=mnu)
    r  = predict_desi(H0, rd, E_func, *Eargs) - DESI_OBS
    return -0.5 * (r @ DESI_COV_INV @ r)

def ll_planck(H0, Om, ob_h2):
    dv = np.array([H0-PLANCK_MU[0], Om-PLANCK_MU[1], ob_h2-PLANCK_MU[2]])
    return -0.5 * (dv @ PLANCK_COV_INV @ dv)


# ─────────────────────────────────────────────────────────────
# 5. LOG-POSTERIORS
# ─────────────────────────────────────────────────────────────

def lpost_ssee(theta):
    H0, ob_h2 = theta
    if not (40 < H0 < 100): return -np.inf
    if not (0.015 < ob_h2 < 0.030): return -np.inf
    lp_bbn = -0.5*((ob_h2-0.02218)/0.00055)**2  # prior BBN de DESI (Schöneberg 2024)
    lp_H0  = -0.5*((H0-PLANCK_H0[0])/PLANCK_H0[1])**2
    om_h2  = WM_ALG                # ω_m ALGEBRAICO fijo — la predicción de SSEE
    Om     = WM_ALG/(H0/100)**2    # Ω_m DERIVADO por muestra (no congelado)
    lb = ll_bao_full(H0, om_h2, ob_h2, E_ssee, Om)
    # 2026-10-01: SIN termino de cumulos. Era una constante (KAL0 y f_nu fijos, cero libres) que solo
    # llevaba SSEE: no movia el posterior, pero restaba chi2=0.49 al lnP_MAP de SSEE y no a LCDM/CPL,
    # con 4 datos que N_DATA no contaba. Ademas eran datos que no estan en la fuente citada y una formula
    # del marco MOND de abril (el SSEE vigente es RG: alpha_T=alpha_M=alpha_B=0). La prueba de cumulos
    # vive aparte, simetrica y sobre los 46 sistemas reales: src/p02_mcmc/cumulos_zhang2026.py
    return lp_bbn + lp_H0 + lb

def lpost_lcdm(theta):
    H0, Om, ob_h2 = theta
    if not (40 < H0 < 100): return -np.inf
    if not (0.15 < Om < 0.55): return -np.inf
    if not (0.015 < ob_h2 < 0.030): return -np.inf
    om_h2 = Om*(H0/100)**2
    return ll_planck(H0, Om, ob_h2) + ll_bao_full(H0, om_h2, ob_h2, E_lcdm, Om, mnu=_MNU_LCDM)

def lpost_cpl(theta):
    H0, Om, w0, wa, ob_h2 = theta
    if not (40 < H0 < 100): return -np.inf
    if not (0.15 < Om < 0.55): return -np.inf
    if not (-2.5 < w0 < 0.5): return -np.inf
    if not (-3.0 < wa < 2.0): return -np.inf
    if not (0.015 < ob_h2 < 0.030): return -np.inf
    om_h2 = Om*(H0/100)**2
    lp = ll_planck(H0, Om, ob_h2)
    lp += -0.5*((w0+1.0)/0.5)**2 - 0.5*(wa/1.0)**2
    return lp + ll_bao_full(H0, om_h2, ob_h2, E_cpl, Om, w0, wa, mnu=_MNU_LCDM)

# ─────────────────────────────────────────────────────────────
# 6. MCMC CON GUARDADO INCREMENTAL
# ─────────────────────────────────────────────────────────────

N_WALKERS  = 100
N_STEPS    = 25000
N_BURN     = 5000
SAVE_EVERY = 500

def run_mcmc_professional(log_post, theta0, scales, ndim, label):
    log(f"\n[{label}]  ndim={ndim}  {N_WALKERS}w × {N_STEPS}s  (guardado cada {SAVE_EVERY})")
    rng = np.random.default_rng(42)
    pos = theta0 + rng.standard_normal((N_WALKERS, ndim)) * scales
    sampler = emcee.EnsembleSampler(N_WALKERS, ndim, log_post)

    # Burn-in
    log(f"  Burn-in: {N_BURN} pasos...")
    pos, lp0, _ = sampler.run_mcmc(pos, N_BURN, progress=False)
    sampler.reset()
    log(f"  Burn-in completo. Iniciando producción...")

    # Producción con checkpoints
    all_chains = []
    for i in range(0, N_STEPS, SAVE_EVERY):
        pos, lp0, _ = sampler.run_mcmc(pos, SAVE_EVERY, progress=False)
        all_chains.append(sampler.get_chain(flat=True))
        log(f"  {label}: {i+SAVE_EVERY}/{N_STEPS} pasos  "
            f"aceptación={np.mean(sampler.acceptance_fraction):.3f}")
        # Checkpoint incremental
        np.savez(CHAIN_FILE.replace(".npz", f"_{label.replace(' ','_')}_ckpt.npz"),
                 chain=np.concatenate(all_chains, axis=0))

    try:
        tau = sampler.get_autocorr_time(quiet=True)
        tau_max = np.max(tau)
        n_eff = N_WALKERS * N_STEPS / tau_max
    except Exception:
        tau_max, n_eff = np.nan, np.nan

    flat2 = sampler.get_chain(flat=True)
    all_lp = sampler.get_log_prob(flat=True)
    mask = np.isfinite(all_lp)
    idx = np.argmax(all_lp) if np.any(mask) else 0

    log(f"  τ_max={tau_max:.1f}  N_eff≈{n_eff:.0f}  ln P_MAP={all_lp[idx]:.2f}")
    return {
        "label": label, "ndim": ndim,
        "flat": flat2, "lp": all_lp, "mask": mask,
        "theta_map": flat2[idx], "lp_map": all_lp[idx],
        "medians": np.median(flat2, 0), "stds": np.std(flat2, 0),
        "p16": np.percentile(flat2, 16, 0), "p84": np.percentile(flat2, 84, 0),
        "tau_max": tau_max, "n_eff": n_eff,
        "acceptance": np.mean(sampler.acceptance_fraction),
    }

def load_ssee_from_checkpoint(label="SSEE"):
    ckpt = CHAIN_FILE.replace(".npz", f"_{label.replace(' ','_')}_ckpt.npz")
    data = np.load(ckpt)
    flat2 = data["chain"]
    all_lp = np.array([lpost_ssee(flat2[i]) for i in range(min(len(flat2), 50000))])
    # Aproximar lp para toda la cadena si es grande
    if len(flat2) > 50000:
        all_lp_full = np.full(len(flat2), -np.inf)
        all_lp_full[:50000] = all_lp
        all_lp = all_lp_full
    mask = np.isfinite(all_lp)
    idx  = np.argmax(all_lp) if np.any(mask) else 0
    log(f"\n[{label}] Cargado desde checkpoint: {len(flat2)} muestras")
    log(f"  ln P_MAP ≈ {all_lp[idx]:.2f}  (evaluado en primeras 50k muestras)")
    return {
        "label": label, "ndim": 2,
        "flat": flat2, "lp": all_lp, "mask": mask,
        "theta_map": flat2[idx], "lp_map": all_lp[idx],
        "medians": np.median(flat2, 0), "stds": np.std(flat2, 0),
        "p16": np.percentile(flat2, 16, 0), "p84": np.percentile(flat2, 84, 0),
        "tau_max": np.nan, "n_eff": len(flat2) / N_WALKERS,
        "acceptance": 0.714,
    }

SSEE_CKPT = CHAIN_FILE.replace(".npz", "_SSEE_ckpt.npz")
# (2026-09-29) La cadena guardada SOLO se reutiliza si se pide (REUSAR_SSEE=1). El 29-sep
# la corrida cargó en silencio una cadena del 25 de julio (r_d por fórmula) y mezcló un
# SSEE viejo con ΛCDM y CPL nuevos. Por defecto se re-corre.
if os.path.exists(SSEE_CKPT) and os.environ.get("REUSAR_SSEE") == "1":
    log("Cadena SSEE encontrada. Cargando desde checkpoint...")
    res_ssee = load_ssee_from_checkpoint()
else:
    res_ssee = run_mcmc_professional(lpost_ssee,
        np.array([62.0, 0.02237]), np.array([2.0, 0.0003]), 2, "SSEE")

res_lcdm = run_mcmc_professional(lpost_lcdm,
    np.array([67.4, 0.315, 0.02237]), np.array([1.5, 0.015, 0.0003]), 3, "ΛCDM")
res_cpl  = run_mcmc_professional(lpost_cpl,
    np.array([67.4, 0.315, -0.90, -0.40, 0.02237]),
    np.array([1.5, 0.015, 0.10, 0.25, 0.0003]), 5, "CPL")

# ─────────────────────────────────────────────────────────────
# 7. COMPARACIÓN DE MODELOS
# ─────────────────────────────────────────────────────────────

N_DATA = len(DESI_BAO_Z := DESI_Z) + 3   # 13 BAO + 3 Planck constraints
models = [res_ssee, res_lcdm, res_cpl]
for r in models:
    r["BIC"] = r["ndim"] * np.log(N_DATA) - 2 * r["lp_map"]
    r["AIC"] = 2 * r["ndim"] - 2 * r["lp_map"]
bic_min = min(r["BIC"] for r in models)
aic_min = min(r["AIC"] for r in models)

log("\n" + "="*65)
log("COMPARACIÓN DE MODELOS (covarianza DESI same-bin block-diagonal)")
log("="*65)
log(f"\n  {'Modelo':<14} {'k':>3} {'ln P_MAP':>10} {'BIC':>8} {'ΔBIC':>7} {'AIC':>8} {'ΔAIC':>7} {'N_eff':>8}")
log("  " + "-"*63)
for r in models:
    log(f"  {r['label']:<14} {r['ndim']:>3} {r['lp_map']:>10.2f} "
        f"{r['BIC']:>8.2f} {r['BIC']-bic_min:>7.2f} "
        f"{r['AIC']:>8.2f} {r['AIC']-aic_min:>7.2f} "
        f"{r['n_eff']:>8.0f}")

# ─────────────────────────────────────────────────────────────
# 8. PARÁMETROS POSTERIORES
# ─────────────────────────────────────────────────────────────

param_names = {
    "SSEE": ["H₀", "Ω_b·h²"],
    "ΛCDM":      ["H₀", "Ω_m", "Ω_b·h²"],
    "CPL":       ["H₀", "Ω_m", "w₀", "wₐ", "Ω_b·h²"],
}
log("\n" + "="*65)
log("PARÁMETROS POSTERIORES (mediana ± 1σ)")
log("="*65)
for r in models:
    log(f"\n  [{r['label']}]  τ_max={r['tau_max']:.1f}  N_eff≈{r['n_eff']:.0f}  accept={r['acceptance']:.3f}")
    for nm, med, p16, p84 in zip(param_names[r["label"]],
                                  r["medians"], r["p16"], r["p84"]):
        log(f"    {nm:<12} = {med:.5f}  +{p84-med:.5f}/-{med-p16:.5f}")
    if r["label"] == "SSEE":
        log(f"    {'Ω_m,total':<12} = {OM_GEOM:.5f}  [geometría; ω_m/h²]")
        log(f"    {'s_m = 1+w0':<12} = {OM_SECTOR:.6f}  [ecuación de estado, NO densidad]")
        log(f"    {'w₀,wₐ':<12} = {W0_SSEE:.4f}, {WA_SSEE:.4f}  [algebraico]")

# Tensiones
def get_rd(r):
    H0 = r["medians"][0]; ob = r["medians"][-1]
    if r["label"] == "SSEE":                       # ω_m algebraico (R25), no Ω_m congelado
        return sound_horizon_rd(ob, WM_ALG)
    return sound_horizon_rd(ob, r["medians"][1]*(H0/100)**2, mnu=_MNU_LCDM)

rd_ssee = get_rd(res_ssee); rd_lcdm = get_rd(res_lcdm)
H0_s    = res_ssee["medians"][0]; H0_s_std = res_ssee["stds"][0]
t_H0    = abs(H0_s - PLANCK_H0[0]) / np.sqrt(H0_s_std**2 + PLANCK_H0[1]**2)
_Om_post = WM_ALG/(H0_s/100)**2                        # Ω_m derivado en el posterior SSEE
t_Om    = abs(_Om_post - PLANCK_OM[0]) / PLANCK_OM[1]  # (era con OM_GEOM del ancla congelado)
log(f"\n  r_d(SSEE)={rd_ssee:.2f} Mpc  r_d(ΛCDM)={rd_lcdm:.2f} Mpc  ratio={rd_ssee/rd_lcdm:.3f}")
log(f"  H₀(SSEE)={H0_s:.2f}±{H0_s_std:.2f}  Planck={PLANCK_H0[0]}±{PLANCK_H0[1]}  tensión={t_H0:.2f}σ")
log(f"  Ω_m tensión SSEE vs Planck: {t_Om:.2f}σ")

# PPC Cosmic Chronometers
def H_pred(r, z):
    th = r["theta_map"]
    # SSEE: Ω_m se deriva del H₀ MAP (ω_m algebraico fijo), no se congela
    if r["label"] == "SSEE": return th[0]*E_ssee(z, WM_ALG/(th[0]/100)**2)
    if r["label"] == "ΛCDM":      return th[0]*E_lcdm(z, th[1])
    return th[0]*E_cpl(z, th[1], th[2], th[3])

log("\n  PPC — Cosmic Chronometers χ²_r:")
for r in models:
    c2r = np.sum(((H_pred(r, Z_CC)-H_CC)/DH_CC)**2) / len(Z_CC)
    log(f"    {r['label']:<14}: {c2r:.3f}")

# ─────────────────────────────────────────────────────────────
# 9. FIGURAS
# ─────────────────────────────────────────────────────────────

log("\nGenerando figuras...")

# Corner SSEE
fig_ssee = corner.corner(res_ssee["flat"],
    labels=[r"$H_0$", r"$\Omega_b h^2$"],
    quantiles=[0.16, 0.5, 0.84], show_titles=True,
    title_kwargs={"fontsize": 10})
fig_ssee.suptitle("SSEE posterior (N=25000, covarianza DESI completa)", y=1.01)
fig_ssee.savefig(f"{OUT_DIR}/fig_corner_ssee_professional.pdf", bbox_inches="tight")
plt.close(fig_ssee)

# Corner ΛCDM
fig_lcdm = corner.corner(res_lcdm["flat"],
    labels=[r"$H_0$", r"$\Omega_m$", r"$\Omega_b h^2$"],
    quantiles=[0.16, 0.5, 0.84], show_titles=True,
    title_kwargs={"fontsize": 10})
fig_lcdm.suptitle("ΛCDM posterior (N=25000, covarianza DESI completa)", y=1.01)
fig_lcdm.savefig(f"{OUT_DIR}/fig_corner_lcdm_professional.pdf", bbox_inches="tight")
plt.close(fig_lcdm)

# Corner CPL
fig_cpl = corner.corner(res_cpl["flat"],
    labels=[r"$H_0$", r"$\Omega_m$", r"$w_0$", r"$w_a$", r"$\Omega_b h^2$"],
    quantiles=[0.16, 0.5, 0.84], show_titles=True,
    title_kwargs={"fontsize": 10})
fig_cpl.suptitle("CPL posterior (N=25000, covarianza DESI completa)", y=1.01)
fig_cpl.savefig(f"{OUT_DIR}/fig_corner_cpl_professional.pdf", bbox_inches="tight")
plt.close(fig_cpl)

# Guardar cadenas finales
np.savez(CHAIN_FILE,
    ssee_flat=res_ssee["flat"], ssee_lp=res_ssee["lp"],
    lcdm_flat=res_lcdm["flat"], lcdm_lp=res_lcdm["lp"],
    cpl_flat=res_cpl["flat"],   cpl_lp=res_cpl["lp"],
)

elapsed_total = (time.time()-t0)/3600
log(f"\nFiguras guardadas en {OUT_DIR}/")
log(f"Cadenas guardadas en {CHAIN_FILE}")
log(f"Tiempo total: {elapsed_total:.2f}h")
log("FIN MCMC PROFESIONAL")
