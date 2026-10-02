"""
SSEE Paper 2 — MCMC PRODUCCIÓN bajo prior H_alg (reframe ω_m-directo)
=====================================================================
Variante de producción del MCMC de Paper 2 para el reframe ω_m-DIRECTO
(2026-06-18, OP-8 cerrado; prior MIRA 67.037 RETIRADO):

  Prior H₀:  H_MIRA (67.037, retirado)  →  H_glob = SH0ES·(1−f_screen) ± σ propagado
             (2026-09-28; antes el número puro 3(φ+π)² con el σ de Planck 0.54)

El centro NO es ad hoc: con ω_b=(π−φ)/(3Ω²) y ω_c=KAL₀·ω_b·n_s
FIJOS por álgebra, la verosimilitud CMB plik_lite se MINIMIZA en
H₀=67.962 (scan results/logs/p3_h0anchor_reframe.log; χ²=1005.41 mín).
Es decir, H_glob (salida de la cascada SH0ES) y el ancla CMB coinciden; 3(φ+π)² es el blanco puro de ambos.

Tamaño producción: 100 walkers × 25000 steps (= original Paper 2).
Solo corre SSEE (no ΛCDM ni CPL — ya están bien establecidos).

PREGUNTA QUE CONTESTA ESTE SCRIPT (no confundir con otros MCMC del repo):
  «Combinando la informacion del CMB (via el ancla, como prior) con los BAO de
   DESI DR2, ¿donde queda H₀?»  El prior NO es una suposicion a soltar: es uno
   de los DOS datasets que se estan combinando. Soltar H₀ contestaria otra
   pregunta —«¿que prefiere DESI solo?»— que responde
   src/p09_hubble/ssee_h0_prior_experiment.py (prior plano; se lee de h0_four_priors.json).

GEOMETRIA (corregido 2026-07-09 V-L4-DESI, docstring actualizado 2026-07-25):
  E(z), r_d y toda distancia BAO usan la materia TOTAL, y esta se construye
  del ABSOLUTO algebraico, no de una fraccion congelada:
      ω_m = ω_b + ω_c + ω_ν = 0.1426675     [fijo, sin H₀ adentro]
      Ω_m = ω_m/h²                          [DERIVADO por muestra]
  El sector frio Ω_m,dyn = 1+w₀ = 0.160 NUNCA entra en la geometria — meterlo
  daba el χ²=726 espurio. Vive solo en las perturbaciones (Paper 6) y en α_K.
  (La linea previa «El sector DESI usa Ω_m,dyn=0.160» era anterior a ese
   arreglo y contradecia al codigo; retirada.)
"""
import numpy as np
import time, os, sys, warnings, json
_SSEE_DATA = os.environ.get("SSEE_DATA_DIR") or ("/mnt/datos/SSEE_data" if os.path.isdir("/mnt/datos") else "results/data")  # portable: HDD si existe, si no results/ local
warnings.filterwarnings("ignore")
import emcee
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import corner
import os as _reloc_os, sys as _reloc_sys  # reloc: anclar src/
_reloc_sys.path.insert(0, _reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__))))
from ssee_core import (
    PHI, PI, BETA, KAL0, P_SC, K_V, T_R, M_V,
    W0, WA, OMEGA_DE, OMEGA_M_TOTAL, OMEGA_CDM_SECTOR, OMEGA_M_H2,
    OMEGA_M_CMB_MIRA, H0_ALG, H0_GLOBAL, SIG_H0_GLOBAL,
)

t0 = time.time()
LOG = "results/logs/mcmc_paper2_reframe.log"
# Regla de disco: la cadena (~1 GB) va al HDD, NO al SSD root (91% lleno)
CKPT = _SSEE_DATA + "/mcmc/paper2_reframe/mcmc_paper2_reframe_ckpt.npz"
OUT = "results/figures"
os.makedirs("results/logs", exist_ok=True)
os.makedirs(OUT, exist_ok=True)
from procedencia import acta, cabecera, con_acta  # noqa: E402
_ENT_ACTA = ["data/raw/desi_dr2_bao.csv"]
# 2026-10-01: el log se ABRIA en modo "a" y acumulaba corridas; ahora una corrida = un log, con su acta arriba
with open(LOG, "w") as _f:
    _f.write(cabecera(__file__, entradas=_ENT_ACTA) + "\n")

def log(msg):
    line = f"[{(time.time()-t0)/60:6.1f}m] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f: f.write(line + "\n")

log("=" * 70)
log("SSEE — MCMC PRODUCCIÓN bajo prior H_glob (cascada SH0ES, reframe ω_m-directo)")
log("=" * 70)
log(f"  Ω_m,total (geometría, ÚNICA densidad) = {OMEGA_M_TOTAL:.8f}  |  s_m = 1+w0 = {OMEGA_CDM_SECTOR:.8f} (ecuación de estado)")
log(f"  Ω_m,CMB (ω_m/h², reframe) = 0.308881  (sin factor; OP-8 cerrado)")
log(f"  w0 = {W0:.10f},  wa = {WA:.10f}")
log(f"  H_glob = H_SH0ES·(1−f_screen) = {H0_GLOBAL:.6f} ± {SIG_H0_GLOBAL:.4f}   (blanco puro 3(φ+π)² = {H0_ALG:.6f})")

C_KM = 2.998e5

# ─── Datos DESI DR2 (2503.14738 Tabla 4) — FUENTE ÚNICA data/raw/desi_dr2_bao.csv ───
# NO hardcodear (evita drift DR1/DR2). src/ ya está en path (línea ~29).
from desi_dr2_data import load_desi_dr2, desi_covariance  # noqa: E402
_DESI        = load_desi_dr2()
DESI_Z       = list(_DESI["z"])
_QSHORT      = {"DM_over_rd": "DM_rd", "DH_over_rd": "DH_rd", "DV_over_rd": "DV_rd"}
DESI_TYPE    = [_QSHORT[q] for q in _DESI["quantity"]]
DESI_OBS     = _DESI["value"]
DESI_COV_INV = np.linalg.inv(desi_covariance(_DESI))   # bloque-diagonal (r_MH oficiales DR2)


# ─── PRIOR H_alg EXACTO (reframe ω_m-directo) ───
# Ancla CMB del reframe: con ω_b y ω_c FIJOS por álgebra SSEE, la
# verosimilitud plik_lite TTTEEE se minimiza en H₀ = 3(φ+π)² = 67.962
# (scan: results/logs/p3_h0anchor_reframe.log; χ²=1005.41 mín, ΔBIC=−24.02).
# NOTA 2026-09-09: ese ΔBIC quedó superado por −26.21 (A_s y τ ajustados,
# N=669 medido); ver results/logs/cmb_dbic_tau_ajustado.json.
# El H global de fondo y el ancla CMB coinciden — no son dos números.
# σ = 0.54 (error Planck H₀ propagado, conservador).
# (prior MIRA 67.037 RETIRADO: usaba Ω_m,CMB=MIRA×Ω_m,dyn, factor disuelto OP-8)
PRIOR_HGLOB = (H0_GLOBAL, SIG_H0_GLOBAL)   # H_glob = SH0ES·(1−f_screen) ± σ propagado (2026-09-28; era (67.962, 0.54) tecleado, con el número puro y el σ de Planck)
BBN_OBH2 = (0.02218, 0.00055)  # prior BBN de DESI (Schöneberg 2024)

def f_de_cpl(z, w0, wa):
    a = 1.0/(1.0+z)
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*(1-a))

def E_ssee(z, Om):
    # PARAMETRIZACIÓN (corregida 2026-07-25): Om llega como ARGUMENTO. SSEE fija
    # ω_m = ω_b+ω_c+ω_ν = 0.14267 (absoluto, algebraico); Ω_m = ω_m/h² es DERIVADO.
    # Antes Ω_m=0.308881 estaba congelado: al mover H₀ el ω_m implícito se despegaba
    # hasta ±1.8% de la predicción y sólo coincidía en H₀=67.962 (el ancla), de modo
    # que el MCMC evaluaba SSEE fielmente SÓLO en el ancla → sesgo hacia ella
    # (posterior 67.947 = 0.04σ). Con ω_m fijo da 67.783 = 0.50σ y χ²_BAO MEJORA
    # (10.72→10.33). Ver ssee_paper2_mcmc_wmfix.py (control que reproduce el viejo).
    return np.sqrt(Om*(1+z)**3 + (1.0-Om)*f_de_cpl(z, W0, WA))

def DC(z_max, Om, n=300):
    zz = np.linspace(0, z_max, n)
    return np.trapezoid(1.0/E_ssee(zz, Om), zz)

import os as _os_rd, sys as _sys_rd
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), ".."))
from rd_camb import rd_mpc as _rd_camb  # r_d de CAMB, una sola funcion (2026-09-28)


def sound_horizon_rd(ob_h2, om_h2):
    return _rd_camb(ob_h2, om_h2, mnu=None)  # CAMB; antes 147.27*(...) con normalizacion 0.15 % alta

def predict_desi(H0, rd, Om):
    preds = []
    for z, qty in zip(DESI_Z, DESI_TYPE):
        dm = (C_KM/H0)*DC(z, Om)
        dh = C_KM/(H0*E_ssee(z, Om))
        if qty == "DM_rd":   preds.append(dm/rd)
        elif qty == "DH_rd": preds.append(dh/rd)
        else:                preds.append((z*dm**2*dh)**(1/3)/rd)
    return np.array(preds)

from bao_camb import pred_desi as _pred_camb, en_rango as _en_rango  # D_M, D_H de CAMB (2026-09-28)


def ll_bao(H0, om_h2, ob_h2, Om):
    # D_M, D_H y r_d de CAMB (bao_camb.py, rd_camb.py). Antes: E(z) analitico
    # sin radiacion ni neutrinos y r_d por formula con normalizacion 0.15 % alta.
    rd = sound_horizon_rd(ob_h2, om_h2)
    r  = _pred_camb(H0, rd) - DESI_OBS
    return -0.5 * (r @ DESI_COV_INV @ r)


def lpost(theta):
    H0, ob_h2 = theta
    if not (40 < H0 < 100): return -np.inf
    if not _en_rango(H0): return -np.inf   # tabla CAMB 55-80: >30 sigma del posterior (declarado)
    if not (0.015 < ob_h2 < 0.030): return -np.inf
    lp_H0  = -0.5*((H0-PRIOR_HGLOB[0])/PRIOR_HGLOB[1])**2
    lp_bbn = -0.5*((ob_h2-BBN_OBH2[0])/BBN_OBH2[1])**2
    om_h2  = OMEGA_M_H2                  # ω_m ALGEBRAICO fijo — lo que SSEE predice
    Om     = OMEGA_M_H2/(H0/100)**2      # Ω_m DERIVADO por muestra (no congelado)
    # 2026-10-01: SIN termino de cumulos. Era una constante (KAL0 y f_nu fijos, cero libres) que solo
    # llevaba SSEE: no movia el posterior, pero restaba chi2=0.49 al lnP_MAP de SSEE y no a LCDM/CPL,
    # con 4 datos que N_DATA no contaba. Ademas eran datos que no estan en la fuente citada y una formula
    # del marco MOND de abril (el SSEE vigente es RG: alpha_T=alpha_M=alpha_B=0). La prueba de cumulos
    # vive aparte, simetrica y sobre los 46 sistemas reales: src/p02_mcmc/cumulos_zhang2026.py
    return lp_H0 + lp_bbn + ll_bao(H0, om_h2, ob_h2, Om)

# ─── MCMC ───
N_W, N_S, N_B, SAVE = 100, 25000, 5000, 500
rng = np.random.default_rng(42)
pos = np.array([62.0, 0.02237]) + rng.standard_normal((N_W, 2)) * np.array([2.0, 0.0003])
sampler = emcee.EnsembleSampler(N_W, 2, lpost)
# 2026-10-01: la semilla 42 solo fijaba los caminantes INICIALES; las propuestas de emcee usaban un
# estado sin semilla, asi que cada re-corrida movia el H0 en la 3a-4a cifra (67.8244 -> 67.8206).
sampler.random_state = np.random.RandomState(42).get_state()

log(f"\nBurn-in {N_B} steps...")
pos, _, _ = sampler.run_mcmc(pos, N_B, progress=False)
sampler.reset()
log("Burn-in OK. Producción...")

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
H0_p16, H0_p84 = np.percentile(flat[:,0], [16, 84])
H0_map = flat[idx, 0]
ob_med = np.median(flat[:,1])

log("\n" + "=" * 70)
log("RESULTADO MCMC PRODUCCIÓN — Prior H_glob (cascada SH0ES)")
log("=" * 70)
log(f"  H₀     = {H0_med:.4f}  +{H0_p84-H0_med:.4f} / -{H0_med-H0_p16:.4f}  km/s/Mpc")
log(f"  H₀ MAP = {H0_map:.4f}")
log(f"  Ω_b·h² = {ob_med:.5f}")
log(f"  ln P_MAP = {lp[idx]:.3f}")
log(f"  τ_max = {np.max(tau):.1f}    N_eff ≈ {n_eff:.0f}")
log(f"  acceptance = {np.mean(sampler.acceptance_fraction):.3f}")

# BIC vs documentado en CLAUDE.md (SSEE k=2)
N_data = 13 + 2  # 13 BAO + 2 priors (H0 + BBN)
BIC = 2 * np.log(N_data) - 2 * lp[idx]
log(f"\n  BIC (k=2, N={N_data}): {BIC:.3f}")

# Comparación
log(f"\nComparación con resultados previos:")
log(f"  Retirado (prior MIRA 67.037, 100w×25k): H₀ = 66.53 ± 0.44")
log(f"  ESTE (prior H_glob {H0_GLOBAL:.3f}±{SIG_H0_GLOBAL:.3f}, 100w×25k): H₀ = {H0_med:.3f} ± {H0_std:.3f}")

# Distancia al H0 que DESI prefiere SIN ningún prior informativo (prior plano
# U(50,90)). MEDIDO, no exploratorio: 67.660 +0.462/-0.466 con la parametrización
# ω_m algebraico fijo (R25). El 65.530 que figuraba aquí era un valor exploratorio
# hardcodeado, nunca recalculado tras el reframe — misma familia de drift que R25
# vigila. Fuente: src/p09_hubble/ssee_h0_prior_experiment.py (4 priors)
#   → results/logs/h0_four_priors_wmfix.log
# 2026-09-28: se LEE de results/logs/h0_four_priors.json (lo escribe ese script;
# corre DESPUÉS de este en la cola, así que es el de la corrida anterior). Si no
# existe, se dice y no se inventa.
_fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results", "logs", "h0_four_priors.json")
if os.path.exists(_fp):
    desi_pure_H0 = json.load(open(_fp))["plano"]["H0_mediana"]
    delta = abs(H0_med - desi_pure_H0)
    log(f"\n  Distancia a DESI-puro ({desi_pure_H0:.3f}, prior plano, h0_four_priors.json): {delta:.3f} km/s/Mpc")
else:
    log("\n  DESI-puro: falta results/logs/h0_four_priors.json (correr ssee_h0_prior_experiment.py)")

# Figura
fig = corner.corner(flat,
    labels=[r"$H_0$ [km/s/Mpc]", r"$\Omega_b h^2$"],
    quantiles=[0.16, 0.5, 0.84], show_titles=True,
    title_kwargs={"fontsize": 10})
# Título en UNA línea, subido, sin duplicar H₀ (ya aparece en el título de cada panel)
fig.suptitle(r"SSEE posterior — MCMC under the $H_{\rm alg}$ prior (DESI DR2, reframe)", y=1.06, fontsize=11)
# El acta va en los metadatos del PDF (Keywords): un PDF no puede llevarla como linea de texto (R75)
fig.savefig(f"{OUT}/fig_corner_ssee_halg_prior.pdf", bbox_inches="tight",
            metadata={"Keywords": "ACTA-PROCEDENCIA " + json.dumps(acta(__file__, entradas=_ENT_ACTA))})
plt.close(fig)
log(f"\nFigura: {OUT}/fig_corner_ssee_halg_prior.pdf")
import json as _json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "p11_sondas"))
from lcdm_planck import LCDM_PLANCK  # noqa: E402
SIG_H0_PLANCK = 0.54   # ORIGEN-VALOR: 0.54 — Planck 2018 VI, Tabla 2, TT,TE,EE+lowE+lensing (la misma columna que lcdm_planck.py)
# Distancias en sigma (2026-10-01; antes se tecleaban en los papers):
#   a H_glob: con la sigma del POSTERIOR (el prior ya contiene a H_glob; sumar su ±0.968 la contaria dos veces)
#   a Planck: dos medidas independientes, sigmas en cuadratura
d_hglob = abs(H0_GLOBAL - H0_med) / H0_std
d_planck = abs(H0_med - LCDM_PLANCK["H0"]) / np.hypot(H0_std, SIG_H0_PLANCK)
log(f"  distancia a H_glob {d_hglob:.3f} sigma · a Planck {d_planck:.3f} sigma")
_json.dump(con_acta(dict(fecha=time.strftime("%Y-%m-%d"), H0_mediana=float(H0_med), H0_p16=float(H0_p16),
                H0_p84=float(H0_p84), H0_std=float(H0_std), H0_MAP=float(H0_map),
                H0_mas=float(H0_p84 - H0_med), H0_menos=float(H0_med - H0_p16),
                obh2_mediana=float(ob_med), lnP_MAP=float(lp[idx]), BIC=float(BIC),
                N_eff=float(n_eff), rd="CAMB (rd_camb.py)", distancias="CAMB (bao_camb.py)",
                sigma_a_Hglob=float(d_hglob), sigma_a_Planck=float(d_planck),
                H0_planck=LCDM_PLANCK["H0"], sig_H0_planck=SIG_H0_PLANCK, semilla=42),
                __file__, entradas=_ENT_ACTA),
           open("results/logs/mcmc_paper2_reframe.json", "w"), indent=1)
log(f"Cadena: {CKPT}")
log(f"Tiempo total: {(time.time()-t0)/60:.1f} min")
