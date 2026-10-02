"""
SSEE — Experimento corto: MCMC bajo 3 priors de H₀
====================================================

Pregunta: ¿el H₀=67.756 del Paper 2 está arrastrado por el prior Planck,
o DESI realmente lo prefiere?

Tres priors a comparar (50 walkers × 10000 steps cada uno, ~3-5 min total):
  (A) Planck 2018:    H₀ = 67.36 ± 0.54  (status quo Paper 2)
  (B) SSEE: H_glob = SH0ES·(1−f_screen) ± σ propagado (ssee_core.H0_GLOBAL)
  (C) Plano amplio:   H₀ ∈ [50, 90], sin info externa  (DESI puro)

Mide: posterior H₀, χ²_MAP, distancia entre los tres centroides.
Si las tres convergen al mismo H₀ → DESI es dominante.
Si A→67.4, B→67.96, C→intermedio → el prior arrastra y el "ganador" es
el modelo cuyo prior coincide con el resultado.
"""
import numpy as np
import time, os, sys
import warnings
warnings.filterwarnings("ignore")

import emcee
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os as _reloc_os, sys as _reloc_sys  # reloc: anclar src/
_reloc_sys.path.insert(0, _reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__))))
from procedencia import cabecera  # noqa: E402
print(cabecera(__file__, entradas=["data/raw/desi_dr2_bao.csv"]), flush=True)
from ssee_core import (
    PHI, PI, KAL0, W0, WA, OMEGA_M_TOTAL, OMEGA_M_H2, H0_ALG, H0_GLOBAL, SIG_H0_GLOBAL
)

# ───── Constantes ─────
C_KM = 2.998e5

# ───── Datos DESI DR2 (copia exacta de ssee_paper2_mcmc.py) ─────
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

# 2026-10-01: SIN termino de cumulos. Era la formula del marco MOND de abril (M = M_ig*KAL0*(1+f_nu))
# con 4 cumulos que no estan en la fuente citada (Zhang+2026); una constante que no movia H0.
# La prueba de cumulos vive aparte, en RG y con los 46 sistemas reales: src/p02_mcmc/cumulos_zhang2026.py

# ───── Física ─────
def f_de_cpl(z, w0, wa):
    a = 1.0 / (1.0 + z)
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*(1-a))

def E_ssee(z, Om):
    # Om es ARGUMENTO: SSEE fija ω_m (absoluto); Ω_m = ω_m/h² es DERIVADO (R25).
    return np.sqrt(Om*(1+z)**3 + (1.0-Om)*f_de_cpl(z, W0, WA))

def DC(z_max, Om, n=300):
    zz = np.linspace(0, z_max, n)
    return np.trapezoid(1.0/E_ssee(zz, Om), zz)

# ORIGEN-VALOR: 0.1432 — pivote omega_m h^2 de la eq. rd de Paper 2 (Planck 2018 TT,TE,EE+lowE); cita EH98 pendiente en FUENTES_PENDIENTES.md FP-7
import os as _os_rd, sys as _sys_rd
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), ".."))
from rd_camb import rd_mpc as _rd_camb  # r_d de CAMB, una sola funcion (2026-09-28)


def sound_horizon_rd(ob_h2, om_h2):
    return _rd_camb(ob_h2, om_h2, mnu=None)  # CAMB; antes 147.27*(...) con normalizacion 0.15 % alta

def predict_desi(H0, rd, Om):
    preds = []
    for z, qty in zip(DESI_Z, DESI_TYPE):
        dm = (C_KM/H0) * DC(z, Om)
        dh = C_KM / (H0 * E_ssee(z, Om))
        if qty == "DM_rd":   preds.append(dm / rd)
        elif qty == "DH_rd": preds.append(dh / rd)
        else:                preds.append((z*dm**2*dh)**(1/3) / rd)
    return np.array(preds)

from bao_camb import pred_desi as _pred_camb, en_rango as _en_rango  # D_M, D_H de CAMB (2026-09-28)


def ll_bao(H0, om_h2, ob_h2, Om):
    # D_M, D_H y r_d de CAMB, como el MCMC canonico de P2 (2026-09-28). Fuera de
    # la tabla CAMB (H0 55-80) la verosimilitud es -inf (declarado).
    if not _en_rango(H0):
        return -np.inf
    rd = sound_horizon_rd(ob_h2, om_h2)
    r  = _pred_camb(H0, rd) - DESI_OBS
    return -0.5 * (r @ DESI_COV_INV @ r)


# ───── 3 log-posteriors según prior ─────
PRIOR_PLANCK = (67.36, 0.54)
PRIOR_SSEE   = (H0_GLOBAL, SIG_H0_GLOBAL)   # H_glob = SH0ES·(1−f_screen), σ propagado de SH0ES
PRIOR_MIRA   = (67.08, 0.54)     # H₀ que sale de Planck con Ω_m,CMB=0.320 (Paper 3)

def lpost_factory(prior_kind):
    if prior_kind == "planck":
        mu, sig = PRIOR_PLANCK
        def lp(theta):
            H0, ob_h2 = theta
            if not (40 < H0 < 100): return -np.inf
            if not (0.015 < ob_h2 < 0.030): return -np.inf
            lp_H0  = -0.5*((H0-mu)/sig)**2
            lp_bbn = -0.5*((ob_h2-0.02218)/0.00055)**2   # prior BBN de DESI (Schöneberg 2024)
            om_h2  = OMEGA_M_H2                    # ω_m algebraico FIJO (R25)
            Om     = OMEGA_M_H2/(H0/100)**2        # Ω_m DERIVADO por muestra
            return lp_H0 + lp_bbn + ll_bao(H0, om_h2, ob_h2, Om)
        return lp
    elif prior_kind == "mira":
        mu, sig = PRIOR_MIRA
        def lp(theta):
            H0, ob_h2 = theta
            if not (40 < H0 < 100): return -np.inf
            if not (0.015 < ob_h2 < 0.030): return -np.inf
            lp_H0  = -0.5*((H0-mu)/sig)**2
            lp_bbn = -0.5*((ob_h2-0.02218)/0.00055)**2   # prior BBN de DESI (Schöneberg 2024)
            om_h2  = OMEGA_M_H2                    # ω_m algebraico FIJO (R25)
            Om     = OMEGA_M_H2/(H0/100)**2        # Ω_m DERIVADO por muestra
            return lp_H0 + lp_bbn + ll_bao(H0, om_h2, ob_h2, Om)
        return lp
    elif prior_kind == "ssee":
        mu, sig = PRIOR_SSEE
        def lp(theta):
            H0, ob_h2 = theta
            if not (40 < H0 < 100): return -np.inf
            if not (0.015 < ob_h2 < 0.030): return -np.inf
            lp_H0  = -0.5*((H0-mu)/sig)**2
            lp_bbn = -0.5*((ob_h2-0.02218)/0.00055)**2   # prior BBN de DESI (Schöneberg 2024)
            om_h2  = OMEGA_M_H2                    # ω_m algebraico FIJO (R25)
            Om     = OMEGA_M_H2/(H0/100)**2        # Ω_m DERIVADO por muestra
            return lp_H0 + lp_bbn + ll_bao(H0, om_h2, ob_h2, Om)
        return lp
    else:  # flat
        def lp(theta):
            H0, ob_h2 = theta
            if not (50 < H0 < 90): return -np.inf
            if not (0.015 < ob_h2 < 0.030): return -np.inf
            lp_bbn = -0.5*((ob_h2-0.02218)/0.00055)**2  # BBN se mantiene (prior BBN de DESI, Schöneberg 2024)
            om_h2  = OMEGA_M_H2                    # ω_m algebraico FIJO (R25)
            Om     = OMEGA_M_H2/(H0/100)**2        # Ω_m DERIVADO por muestra
            return lp_bbn + ll_bao(H0, om_h2, ob_h2, Om)
        return lp

# ───── Runner ─────
N_WALKERS = 50
N_STEPS   = 10000
N_BURN    = 1000

def run_mcmc(label, prior_kind):
    print(f"\n[{label}] arrancando ({N_WALKERS}w × {N_STEPS}s)...", flush=True)
    t0 = time.time()
    rng = np.random.default_rng(42)
    # ORIGEN-VALOR: 0.0005 — dispersion inicial de los walkers en omega_b, elegida (~1/3 del sigma BBN), no es medida
    pos = np.array([65.0, 0.02237]) + rng.standard_normal((N_WALKERS, 2)) * np.array([3.0, 0.0005])
    sampler = emcee.EnsembleSampler(N_WALKERS, 2, lpost_factory(prior_kind))
    sampler.random_state = np.random.RandomState(42).get_state()   # 2026-10-01: las propuestas de emcee tambien con semilla
    pos, _, _ = sampler.run_mcmc(pos, N_BURN, progress=False)
    sampler.reset()
    sampler.run_mcmc(pos, N_STEPS, progress=False)

    flat = sampler.get_chain(flat=True)
    lp   = sampler.get_log_prob(flat=True)
    idx_map = np.argmax(lp)

    res = {
        "label": label, "prior": prior_kind,
        "flat": flat, "lp": lp,
        "H0_med": np.median(flat[:,0]), "H0_std": np.std(flat[:,0]),
        "H0_p16": np.percentile(flat[:,0], 16), "H0_p84": np.percentile(flat[:,0], 84),
        "ob_med": np.median(flat[:,1]),
        "H0_map": flat[idx_map, 0], "lp_map": lp[idx_map],
        "acceptance": np.mean(sampler.acceptance_fraction),
        "elapsed_s": time.time() - t0,
    }
    print(f"  H₀ = {res['H0_med']:.3f} +{res['H0_p84']-res['H0_med']:.3f}/-{res['H0_med']-res['H0_p16']:.3f}"
          f"  | MAP={res['H0_map']:.3f}  ln P_MAP={res['lp_map']:.2f}"
          f"  | accept={res['acceptance']:.3f}  | {res['elapsed_s']:.1f}s", flush=True)
    return res

# ───── Run ─────
print("=" * 78)
print("EXPERIMENTO H₀: tres priors, mismo modelo SSEE, mismos datos DESI+BBN")
print("=" * 78)
print(f"Prior Planck: N({PRIOR_PLANCK[0]}, {PRIOR_PLANCK[1]})")
print(f"Prior MIRA:   N({PRIOR_MIRA[0]}, {PRIOR_MIRA[1]})  [= H₀ Paper 3 con Ω_m,CMB=0.320]")
print(f"Prior SSEE:   N({PRIOR_SSEE[0]:.4f}, {PRIOR_SSEE[1]})")
print(f"Prior plano:  U(50, 90)")

res_planck = run_mcmc("Prior Planck", "planck")
res_mira   = run_mcmc("Prior MIRA",   "mira")
res_ssee   = run_mcmc("Prior SSEE",   "ssee")
res_flat   = run_mcmc("Prior plano",  "flat")

results = [res_planck, res_mira, res_ssee, res_flat]

# ───── Análisis ─────
print("\n" + "=" * 78)
print("RESULTADO")
print("=" * 78)
print(f"\n  {'Prior':<18} {'H₀ mediana':>14} {'±':>10} {'H₀ MAP':>10} {'ln L_BAO':>10}")
print("  " + "-"*64)
for r in results:
    # ln L_BAO solo (sin prior H0) en MAP
    H0, ob = r["flat"][np.argmax(r["lp"])]
    om_h2  = OMEGA_M_H2                        # ω_m algebraico FIJO (R25)
    ll_b   = ll_bao(H0, om_h2, ob, OMEGA_M_H2/(H0/100)**2)
    print(f"  {r['label']:<18} {r['H0_med']:>14.3f} {r['H0_std']:>10.3f}"
          f" {r['H0_map']:>10.3f} {ll_b:>10.2f}")

# Distancia entre centroides
d_PS = abs(res_planck["H0_med"] - res_ssee["H0_med"])
d_PF = abs(res_planck["H0_med"] - res_flat["H0_med"])
d_SF = abs(res_ssee["H0_med"] - res_flat["H0_med"])
print(f"""
  Distancias entre medianas:
    |Planck − SSEE|   = {d_PS:.3f} km/s/Mpc
    |Planck − Plano|  = {d_PF:.3f} km/s/Mpc
    |SSEE   − Plano|  = {d_SF:.3f} km/s/Mpc

  Interpretación:
""")

# Diagnóstico automático
flat_H0 = res_flat["H0_med"]
dist_from_planck = abs(flat_H0 - PRIOR_PLANCK[0])
dist_from_ssee   = abs(flat_H0 - PRIOR_SSEE[0])

if dist_from_planck < dist_from_ssee - 0.2:
    print(f"  → DESI puro prefiere H₀ ≈ {flat_H0:.2f}, MÁS CERCA de Planck que de SSEE-alg")
    print(f"    H_glob está en tensión observacional ({dist_from_ssee/SIG_H0_GLOBAL:.1f}σ)")
elif dist_from_ssee < dist_from_planck - 0.2:
    print(f"  → DESI puro prefiere H₀ ≈ {flat_H0:.2f}, MÁS CERCA de H_glob que de Planck")
    print(f"    H_glob de SSEE gana sin necesidad de prior — predicción robusta")
else:
    print(f"  → DESI puro: H₀ ≈ {flat_H0:.2f}, ambiguo entre Planck y SSEE-alg")
    print(f"    Los datos no discriminan, el prior decide.")

# Figura comparativa
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#1f77b4", "#ff7f0e", "#d62728", "#2ca02c"]
labels_plot = [r"Prior Planck (67.36)", r"Prior MIRA (67.08)", r"Prior SSEE $H_{\rm glob}$", r"Prior plano"]
for r, c, lab in zip(results, colors, labels_plot):
    ax.hist(r["flat"][:,0], bins=80, density=True, alpha=0.5, color=c, label=lab)
    ax.axvline(r["H0_med"], color=c, ls="--", lw=1.5)

ax.axvline(PRIOR_PLANCK[0], color="black",  ls=":", alpha=0.4, label=f"Planck μ={PRIOR_PLANCK[0]}")
ax.axvline(PRIOR_MIRA[0],   color="brown",  ls=":", alpha=0.4, label=f"MIRA-P3 μ={PRIOR_MIRA[0]}")
ax.axvline(PRIOR_SSEE[0],   color="purple", ls=":", alpha=0.4, label=f"SSEE-alg μ={PRIOR_SSEE[0]:.3f}")
ax.set_xlabel(r"$H_0$ [km/s/Mpc]")
ax.set_ylabel("posterior density")
ax.set_title("Posterior H₀ bajo 3 priors — DESI DR2 + BBN + cúmulos (SSEE fondo)")
ax.legend(fontsize=8, loc="upper left")
ax.set_xlim(64, 72)
plt.tight_layout()
out = "results/figures/fig_h0_three_priors.pdf"
os.makedirs("results/figures", exist_ok=True)
import json as _jsfig
from procedencia import acta as _acta_fig  # noqa: E402
plt.savefig(out, bbox_inches="tight", metadata={"Keywords": "ACTA-PROCEDENCIA " + _jsfig.dumps(_acta_fig(__file__, entradas=["data/raw/desi_dr2_bao.csv"]))})
print(f"\nFigura: {out}")

# Guardar cadenas para análisis posterior
np.savez("results/logs/h0_four_priors.npz",
         planck=res_planck["flat"], mira=res_mira["flat"], ssee=res_ssee["flat"], flat=res_flat["flat"],
         planck_lp=res_planck["lp"], mira_lp=res_mira["lp"], ssee_lp=res_ssee["lp"], flat_lp=res_flat["lp"])
print("Cadenas: results/logs/h0_four_priors.npz")
# El resultado con prior PLANO (DESI sola) lo LEE el MCMC de Paper 2; antes lo tecleaba.
import json as _json
from procedencia import con_acta  # noqa: E402
_res4 = {k: dict(H0_mediana=float(r["H0_med"]), H0_std=float(r["H0_std"]))
         for k, r in (("planck", res_planck), ("mira", res_mira), ("ssee_hglob", res_ssee), ("plano", res_flat))}
# Distancias de DESI SOLA (prior plano), 2026-10-01 (antes se tecleaban en P2):
#   a H_glob con la sigma del posterior; a Planck con las dos sigmas en cuadratura
_sys_pl = __import__("sys"); _sys_pl.path.insert(0, _dd_os.path.join(_dd_os.path.dirname(_dd_os.path.abspath(__file__)), "..", "p11_sondas"))
from lcdm_planck import LCDM_PLANCK as _LP  # noqa: E402
SIG_H0_PLANCK = 0.54   # ORIGEN-VALOR: 0.54 — Planck 2018 VI, Tabla 2, TT,TE,EE+lowE+lensing (la columna de lcdm_planck.py)
_res4["plano"].update(sigma_a_Hglob=float(abs(H0_GLOBAL - res_flat["H0_med"]) / res_flat["H0_std"]),
                      sigma_a_Planck=float(abs(res_flat["H0_med"] - _LP["H0"]) / np.hypot(res_flat["H0_std"], SIG_H0_PLANCK)))
_json.dump(con_acta(_res4, __file__, entradas=["data/raw/desi_dr2_bao.csv"]),
           open("results/logs/h0_four_priors.json", "w"), indent=1)
print("Resumen: results/logs/h0_four_priors.json")
