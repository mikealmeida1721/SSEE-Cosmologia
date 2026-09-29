"""
SSEE Phase D — Savage-Dickey Density Ratio + DESI BAO Cross-Validation
=======================================================================
Dos criterios independientes del conteo-k para la comparación de modelos:

  1. Savage-Dickey Density Ratio (SDDR):
     B(SSEE_dyn vs CPL_dyn) = p(w0_S, wa_S | data, CPL) / π(w0_S, wa_S | CPL prior)
     Exacto para modelos anidados (SSEE es CPL con punto fijo).

  2. Cross-validation predictiva (LOO-z):
     Split DESI 13 pts en 7 train (z<1.317) + 6 test (z≥1.317).
     SSEE: 1 param libre (H0); ΛCDM: 2 params libres (H0, Ωm).
     Mejor log-PL en test → menor riesgo de sobreajuste.

Prerrequisito: results/logs/mcmc_chains_professional.npz (generado por ssee_paper2_mcmc.py)
"""

import os as _os
import numpy as np
from scipy.stats import gaussian_kde, norm
from scipy.optimize import minimize
import warnings
import os as _o66, sys as _s66
_s66.path.insert(0, _o66.path.dirname(_o66.path.dirname(_o66.path.abspath(__file__))))
import ssee_core as _C

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# 0. CONSTANTES SSEE (verificadas algebraicamente)
# ─────────────────────────────────────────────────────────────
phi   = (1 + 5**0.5) / 2          # 1.6180339887
PI    = 3.14159265358979

W0_SSEE = -0.840                   # = −Tr/Mv algebraico
WA_SSEE = -0.670                   # = −P_sc/IGNIS algebraico (IGNIS=π+PYROS)
OM_DYN  = 0.160        # sector frío (NO geometría)
OM_TOTAL = _C.OMEGA_M_TOTAL   # Ω_m EN EL ANCLA (diagnóstico) — NO congelar en ajustes
WM_ALG   = _C.OMEGA_M_H2      # ω_m = ω_b+ω_c+ω_ν ALGEBRAICO — lo que SSEE realmente fija.
# R25 (2026-07-25): SSEE predice el ABSOLUTO ω_m; Ω_m = ω_m/h² es DERIVADO. Congelar
# Ω_m y derivar ω_m=Ω_m·h² despega el ω_m implícito hasta ±1.8% de la predicción y
# sólo coincide en H₀=67.962 (el ancla), sesgando cualquier ajuste hacia ella.
MIRA    = (3*phi + PI) / 4         # 1.9989237  (errata del comentario corregida 2026-09-19)

# ─────────────────────────────────────────────────────────────
# 1. DATOS DESI DR2 (idénticos al script MCMC principal)
# ─────────────────────────────────────────────────────────────
C_KM = 299792.458

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

PLANCK_H0    = (67.36, 0.54)
PLANCK_OM    = (0.3153, 0.0073)
PLANCK_OBH2  = (0.02237, 0.00015)
RHO_H0_OM    = -0.85

# ─────────────────────────────────────────────────────────────
# 2. FUNCIONES DE APOYO
# ─────────────────────────────────────────────────────────────
import os as _os_rd, sys as _sys_rd
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), ".."))
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), "..", "p11_sondas"))
from rd_camb import rd_mpc as _rd_camb  # r_d de CAMB, una sola funcion (2026-09-28)
from lcdm_planck import LCDM_PLANCK as _LCDM_RD
# la masa de neutrinos de r_d va POR MODELO: SSEE la suya (None), LCDM y CPL la de LCDM
_MNU_RD = [None]


def sound_horizon_rd(ob_h2, om_h2):
    return _rd_camb(ob_h2, om_h2, mnu=_MNU_RD[0])  # CAMB; antes 147.27*(...) con normalizacion 0.15 % alta

def DC(z_max, E_func, n=500):
    zz = np.linspace(0, z_max, n)
    return np.trapezoid(1.0 / E_func(zz), zz)

def E_cpl(z, Om, w0, wa):
    a = 1/(1+z)
    return np.sqrt(Om*(1+z)**3 + (1-Om)*(1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*(1-a)))

def E_lcdm(z, Om):
    return np.sqrt(Om*(1+z)**3 + (1-Om))

def predict_desi_full(H0, ob_h2, om_h2, E_func, *Eargs):
    rd   = sound_horizon_rd(ob_h2, om_h2)
    preds = []
    for z, qty in zip(DESI_Z, DESI_TYPE):
        dm = (C_KM/H0) * DC(z, lambda zz: E_func(zz, *Eargs))
        dh = C_KM / (H0 * E_func(z, *Eargs))
        if qty == "DM_rd":   preds.append(dm / rd)
        elif qty == "DH_rd": preds.append(dh / rd)
        else:                preds.append((z * dm**2 * dh)**(1/3) / rd)
    return np.array(preds)

def ll_planck(H0, Om, ob_h2):
    s0, s1, s2 = PLANCK_H0[1], PLANCK_OM[1], PLANCK_OBH2[1]
    dv = np.array([H0 - PLANCK_H0[0], Om - PLANCK_OM[0], ob_h2 - PLANCK_OBH2[0]])
    cov = np.array([
        [s0**2,           RHO_H0_OM*s0*s1, 0.0   ],
        [RHO_H0_OM*s0*s1, s1**2,           0.0   ],
        [0.0,             0.0,             s2**2 ],
    ])
    return -0.5 * (dv @ np.linalg.inv(cov) @ dv)

# ════════════════════════════════════════════════════════════════════════
# PARTE 1 — SAVAGE-DICKEY DENSITY RATIO
# ════════════════════════════════════════════════════════════════════════
def savage_dickey():
    print("=" * 60)
    print("PARTE 1: SAVAGE-DICKEY DENSITY RATIO")
    print("=" * 60)

    # Cargar cadenas CPL
    # Ruta anclada a __file__ y con el enlace RESUELTO. Antes era relativa y
    # pelada: el script solo corria si el cwd era la raiz del repo, y ademas
    # results/logs/*.npz es un enlace a /mnt/datos, que algunos entornos no
    # atraviesan. El resto de la suite ya ancla a __file__ (ver p02_mcmc);
    # esta era la excepcion. Encontrado 2026-09-07 al re-correr el log por R35.
    _raiz = _os.path.dirname(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))))
    _npz = _os.path.realpath(_os.path.join(
        _raiz, "results", "logs", "mcmc_chains_professional.npz"))
    data = np.load(_npz)
    cpl_flat = data["cpl_flat"]   # (2500000, 5) — H0, Om, w0, wa, ob_h2
    cpl_lp   = data["cpl_lp"]

    print(f"  Muestras CPL: {len(cpl_flat):,}")
    print(f"  Rango w0: [{cpl_flat[:,2].min():.3f}, {cpl_flat[:,2].max():.3f}]")
    print(f"  Rango wa: [{cpl_flat[:,3].min():.3f}, {cpl_flat[:,3].max():.3f}]")

    # Parámetros del prior CPL (w0, wa) — del script mcmc
    # Prior Gaussiano: exp(-0.5*((w0+1.0)/0.5)^2) * exp(-0.5*(wa/1.0)^2)
    # truncado a w0 ∈ (-2.5, 0.5), wa ∈ (-3.0, 2.0)
    W0_PRIOR_MU, W0_PRIOR_SIG = -1.0, 0.5
    WA_PRIOR_MU, WA_PRIOR_SIG =  0.0, 1.0
    W0_BOX = (-2.5, 0.5)
    WA_BOX = (-3.0, 2.0)

    # Normalización del prior truncado (factor de truncación)
    from scipy.special import erf
    def trunc_norm_cdf(x, mu, sig, a, b):
        return 0.5 * (erf((x-mu)/(sig*np.sqrt(2))) - erf((a-mu)/(sig*np.sqrt(2))))
    Z_w0 = trunc_norm_cdf(W0_BOX[1], W0_PRIOR_MU, W0_PRIOR_SIG, W0_BOX[0], W0_BOX[1])
    Z_wa = trunc_norm_cdf(WA_BOX[1], WA_PRIOR_MU, WA_PRIOR_SIG, WA_BOX[0], WA_BOX[1])
    print(f"\n  Factor truncación prior w0: {Z_w0:.6f} (Gauss untruncada: {norm.cdf(W0_BOX[1], W0_PRIOR_MU, W0_PRIOR_SIG) - norm.cdf(W0_BOX[0], W0_PRIOR_MU, W0_PRIOR_SIG):.6f})")
    print(f"  Factor truncación prior wa: {Z_wa:.6f}")

    # Densidad del prior en el punto SSEE
    pi_w0 = norm.pdf(W0_SSEE, W0_PRIOR_MU, W0_PRIOR_SIG) / Z_w0
    pi_wa = norm.pdf(WA_SSEE, WA_PRIOR_MU, WA_PRIOR_SIG) / Z_wa
    pi_ssee = pi_w0 * pi_wa

    print(f"\n  Prior density en (w0={W0_SSEE}, wa={WA_SSEE}):")
    print(f"    π(w0)  = {pi_w0:.6f}")
    print(f"    π(wa)  = {pi_wa:.6f}")
    print(f"    π(w0,wa) = {pi_ssee:.6f}")
    print(f"    N-sigmas w0 del centro prior: {abs(W0_SSEE - W0_PRIOR_MU)/W0_PRIOR_SIG:.3f}σ")
    print(f"    N-sigmas wa del centro prior: {abs(WA_SSEE - WA_PRIOR_MU)/WA_PRIOR_SIG:.3f}σ")

    # Densidad posterior marginal en (w0, wa) via KDE
    # Usar submuestra para eficiencia (1M de 2.5M, aleatorio)
    rng = np.random.default_rng(42)
    N_kde = 500_000
    idx   = rng.choice(len(cpl_flat), size=N_kde, replace=False)
    w0_samples = cpl_flat[idx, 2]
    wa_samples = cpl_flat[idx, 3]

    print(f"\n  Ajustando KDE 2D con {N_kde:,} muestras...")
    kde = gaussian_kde(np.vstack([w0_samples, wa_samples]),
                       bw_method='scott')
    post_density = kde([W0_SSEE, WA_SSEE])[0]

    print(f"  Densidad posterior en (w0={W0_SSEE}, wa={WA_SSEE}):")
    print(f"    p(w0,wa | data, CPL) = {post_density:.6f}")

    # SDDR = posterior / prior
    B_sddr = post_density / pi_ssee
    ln_B   = np.log(B_sddr)
    print(f"\n  ─────────────────────────────────────────────────────")
    print(f"  SAVAGE-DICKEY: B(SSEE_dyn vs CPL_dyn) = {B_sddr:.4f}")
    print(f"  ln B = {ln_B:.4f}")

    if B_sddr > 1:
        print(f"  → SSEE preferido sobre CPL en sector dinámico")
        if B_sddr > 3:   print(f"  → Evidencia SUSTANCIAL (Jeffreys: |ln B|>1.1)")
        if B_sddr > 10:  print(f"  → Evidencia FUERTE (Jeffreys: |ln B|>2.3)")
        if B_sddr > 100: print(f"  → Evidencia DECISIVA (Jeffreys: |ln B|>4.6)")
    else:
        print(f"  → CPL preferido (posterior concentrada lejos de SSEE)")
        print(f"  → Interpretar: datos NO requieren valores SSEE (neutro)")

    # Verificación: distribución CPL alrededor del punto SSEE
    # ¿Qué fracción de muestras cae dentro de 1σ de DESI del punto SSEE?
    # σ_w0(DESI) ≈ 0.057, σ_wa(DESI) ≈ 0.226
    desi_sw0, desi_swa = 0.057, 0.226
    mask = ((np.abs(w0_samples - W0_SSEE) < desi_sw0) &
            (np.abs(wa_samples - WA_SSEE) < desi_swa))
    frac = mask.sum() / len(w0_samples)
    print(f"\n  Verificación: fracción CPL posterior dentro de 1σ DESI del punto SSEE:")
    print(f"    |w0 - {W0_SSEE}| < {desi_sw0:.3f} AND |wa - {WA_SSEE}| < {desi_swa:.3f}")
    print(f"    Fracción = {frac*100:.2f}%")
    print(f"    (Esperado para distribución concentrada: ~10-20%)")

    # Estadística CPL posterior en (w0, wa)
    w0_med = np.median(w0_samples);  w0_std = np.std(w0_samples)
    wa_med = np.median(wa_samples);  wa_std = np.std(wa_samples)
    print(f"\n  Resumen CPL posterior (w0, wa):")
    print(f"    w0 = {w0_med:.3f} ± {w0_std:.3f}  (SSEE: {W0_SSEE}  — {abs(W0_SSEE - w0_med)/w0_std:.2f}σ)")
    print(f"    wa = {wa_med:.3f} ± {wa_std:.3f}  (SSEE: {WA_SSEE}  — {abs(WA_SSEE - wa_med)/wa_std:.2f}σ)")

    return {
        "B_sddr": B_sddr,
        "ln_B": ln_B,
        "pi_ssee": pi_ssee,
        "post_density": post_density,
        "w0_med": w0_med, "w0_std": w0_std,
        "wa_med": wa_med, "wa_std": wa_std,
    }


# ════════════════════════════════════════════════════════════════════════
# PARTE 2 — CROSS-VALIDATION PREDICTIVA (LOO-z)
# ════════════════════════════════════════════════════════════════════════
def cross_validation():
    print("\n" + "=" * 60)
    print("PARTE 2: CROSS-VALIDATION PREDICTIVA (LOO-z)")
    print("=" * 60)

    # Índices de los puntos DESI por z-bin
    # z-bin  0.295 → idx [0]
    # z-bin  0.510 → idx [1, 2]
    # z-bin  0.706 → idx [3, 4]
    # z-bin  0.930 → idx [5, 6]
    # z-bin  1.317 → idx [7, 8]
    # z-bin  1.491 → idx [9,10]
    # z-bin  2.330 → idx [11,12]

    # Split: TRAIN = z < 1.0 (7 puntos), TEST = z ≥ 1.0 (6 puntos)
    idx_train = [0, 1, 2, 3, 4, 5, 6]    # z = 0.295, 0.510, 0.706, 0.930
    idx_test  = [7, 8, 9, 10, 11, 12]    # z = 1.317, 1.491, 2.330

    print(f"  Split: {len(idx_train)} puntos train (z < 1.0),  "
          f"{len(idx_test)} puntos test (z ≥ 1.0)")
    print(f"  Train: z = {np.array(DESI_Z)[idx_train]}")
    print(f"  Test:  z = {np.array(DESI_Z)[idx_test]}")

    # Sub-matrices de covarianza (bloques independientes, off-diag=0 entre z-bins distintos)
    idx_tr = np.array(idx_train)
    idx_te = np.array(idx_test)
    COV_train = DESI_COV[np.ix_(idx_tr, idx_tr)]
    COV_test  = DESI_COV[np.ix_(idx_te, idx_te)]
    INV_train = np.linalg.inv(COV_train)
    INV_test  = np.linalg.inv(COV_test)
    OBS_train = DESI_OBS[idx_tr]
    OBS_test  = DESI_OBS[idx_te]

    def predict_subset(H0, ob_h2, om_h2, E_func, Eargs, idx_list):
        rd   = sound_horizon_rd(ob_h2, om_h2)
        preds = []
        for i in idx_list:
            z   = DESI_Z[i]
            qty = DESI_TYPE[i]
            dm  = (C_KM/H0) * DC(z, lambda zz: E_func(zz, *Eargs))
            dh  = C_KM / (H0 * E_func(z, *Eargs))
            if qty == "DM_rd":   preds.append(dm / rd)
            elif qty == "DH_rd": preds.append(dh / rd)
            else:                preds.append((z * dm**2 * dh)**(1/3) / rd)
        return np.array(preds)

    def nll_train(params, model):
        _MNU_RD[0] = None if model == "ssee" else _LCDM_RD["mnu"]
        if model == "ssee":
            H0, = params
            om_h2 = WM_ALG                        # ω_m algebraico FIJO (R25)
            Om, w0, wa = WM_ALG/(H0/100)**2, W0_SSEE, WA_SSEE   # Ω_m DERIVADO
            ob_h2 = _C.OMEGA_B_H2                 # ω_b ALGEBRAICO de SSEE (2026-09-28; era 0.02237 tecleado, el de Planck)
            pred  = predict_subset(H0, ob_h2, om_h2, E_cpl, (Om, w0, wa), idx_train)
        elif model == "lcdm":
            H0, Om = params
            ob_h2 = PLANCK_OBH2[0]
            om_h2 = Om * (H0/100)**2
            pred  = predict_subset(H0, ob_h2, om_h2, E_lcdm, (Om,), idx_train)
        elif model == "cpl":
            H0, Om, w0, wa = params
            ob_h2 = PLANCK_OBH2[0]
            om_h2 = Om * (H0/100)**2
            pred  = predict_subset(H0, ob_h2, om_h2, E_cpl, (Om, w0, wa), idx_train)
        r = pred - OBS_train
        return 0.5 * (r @ INV_train @ r)

    def ll_test(params, model):
        _MNU_RD[0] = None if model == "ssee" else _LCDM_RD["mnu"]
        if model == "ssee":
            H0, = params
            om_h2 = WM_ALG                        # ω_m algebraico FIJO (R25)
            Om, w0, wa = WM_ALG/(H0/100)**2, W0_SSEE, WA_SSEE   # Ω_m DERIVADO
            ob_h2 = _C.OMEGA_B_H2                 # ω_b ALGEBRAICO de SSEE (2026-09-28; era 0.02237 tecleado, el de Planck)
            pred  = predict_subset(H0, ob_h2, om_h2, E_cpl, (Om, w0, wa), idx_test)
        elif model == "lcdm":
            H0, Om = params
            ob_h2 = PLANCK_OBH2[0]
            om_h2 = Om * (H0/100)**2
            pred  = predict_subset(H0, ob_h2, om_h2, E_lcdm, (Om,), idx_test)
        elif model == "cpl":
            H0, Om, w0, wa = params
            ob_h2 = PLANCK_OBH2[0]
            om_h2 = Om * (H0/100)**2
            pred  = predict_subset(H0, ob_h2, om_h2, E_cpl, (Om, w0, wa), idx_test)
        r = pred - OBS_test
        return -0.5 * (r @ INV_test @ r)

    results_cv = {}
    for model, p0, bounds in [
        ("ssee",  [67.0],              [(50,85)]),
        ("lcdm",  [67.36, 0.3153],     [(50,85),(0.15,0.55)]),
        ("cpl",   [67.36, 0.3153, -0.838, -0.630],
                                       [(50,85),(0.15,0.55),(-2.5,0.5),(-3.,2.)]),
    ]:
        res = minimize(lambda p, m=model: nll_train(p, m), p0,
                       method="L-BFGS-B", bounds=bounds,
                       options={"maxiter": 2000, "ftol": 1e-12})
        lp_test = ll_test(res.x, model)
        n_train = len(idx_train)
        n_test  = len(idx_test)
        nll_tr  = res.fun
        chi2r_tr = 2 * nll_tr / n_train
        chi2r_te = -2 * lp_test / n_test

        results_cv[model] = {
            "params": res.x,
            "nll_train": nll_tr,
            "ll_test": lp_test,
            "chi2r_train": chi2r_tr,
            "chi2r_test": chi2r_te,
            "k": len(p0),
        }

        labels = {"ssee": ["H0"], "lcdm": ["H0","Om"], "cpl": ["H0","Om","w0","wa"]}
        pstr   = "  ".join(f"{l}={v:.4f}" for l, v in zip(labels[model], res.x))
        print(f"\n  [{model.upper()}] k={len(p0)}")
        print(f"    Params MAP (train): {pstr}")
        print(f"    χ²/(N_train=7) train:  {chi2r_tr:.4f}")
        print(f"    ln L test:             {lp_test:.4f}")
        print(f"    χ²/(N_test=6)  test:   {chi2r_te:.4f}")

    print("\n  ─────────────────────────────────────────────────────")
    print("  RESUMEN CROSS-VALIDATION:")
    print(f"  {'Modelo':<8} {'k':>3} {'χ²_r train':>12} {'ln L test':>12} {'χ²_r test':>12}")
    print(f"  {'─'*8} {'─'*3} {'─'*12} {'─'*12} {'─'*12}")
    for m in ["ssee","lcdm","cpl"]:
        r = results_cv[m]
        print(f"  {m.upper():<8} {r['k']:>3} {r['chi2r_train']:>12.4f} "
              f"{r['ll_test']:>12.4f} {r['chi2r_test']:>12.4f}")

    # Diferencias en ln L test
    dln_ssee_lcdm = results_cv["ssee"]["ll_test"] - results_cv["lcdm"]["ll_test"]
    dln_ssee_cpl  = results_cv["ssee"]["ll_test"] - results_cv["cpl"]["ll_test"]
    print(f"\n  Δ ln L_test (SSEE − ΛCDM) = {dln_ssee_lcdm:+.4f}  "
          f"({'SSEE mejor' if dln_ssee_lcdm > 0 else 'ΛCDM mejor'} en test)")
    print(f"  Δ ln L_test (SSEE − CPL)  = {dln_ssee_cpl:+.4f}  "
          f"({'SSEE mejor' if dln_ssee_cpl > 0 else 'CPL mejor'} en test)")
    print(f"\n  Interpretación: SSEE usa k=1 free param (solo H0).")
    print(f"  Si Δ ln L_test(SSEE−ΛCDM) ≥ 0 → SSEE no overfittea DESI.")

    return results_cv


# ════════════════════════════════════════════════════════════════════════
# PARTE 3 — RESUMEN INTEGRADO PARA PAPER 2 APÉNDICE
# ════════════════════════════════════════════════════════════════════════
def print_paper_summary(sddr_res, cv_res):
    print("\n" + "=" * 60)
    print("PARTE 3: RESUMEN PARA PAPER 2 — APÉNDICE B")
    print("=" * 60)

    B = sddr_res["B_sddr"]
    lnB = sddr_res["ln_B"]

    print(f"""
Savage-Dickey Density Ratio (sector dinámico):
  B(SSEE_dyn vs CPL_dyn) = {B:.3f}
  ln B = {lnB:.3f}
  → CPL posterior en (w0=-0.840, wa=-0.670): {sddr_res['post_density']:.6f}
  → Prior CPL en ese punto:                  {sddr_res['pi_ssee']:.6f}

Interpretación SDDR:
  {"B > 1: datos favorecen el punto SSEE dentro de CPL" if B > 1
   else f"B < 1: datos no favorecen específicamente w0={W0_SSEE}, wa={WA_SSEE}"}
  {"(Jeffreys: evidencia sustancial si |ln B| > 1.1)" if abs(lnB) > 1.1 else
   "(Jeffreys: evidencia débil |ln B| < 1.1 — neutro)"}

Cross-validation predictiva LOO-z (z_test ≥ 1.0):
  SSEE  k=1: χ²_r test = {cv_res['ssee']['chi2r_test']:.4f},  ln L_test = {cv_res['ssee']['ll_test']:.4f}
  ΛCDM  k=2: χ²_r test = {cv_res['lcdm']['chi2r_test']:.4f},  ln L_test = {cv_res['lcdm']['ll_test']:.4f}
  CPL   k=4: χ²_r test = {cv_res['cpl']['chi2r_test']:.4f},  ln L_test = {cv_res['cpl']['ll_test']:.4f}

  Δ ln L_test (SSEE − ΛCDM) = {cv_res['ssee']['ll_test'] - cv_res['lcdm']['ll_test']:+.4f}
  Δ ln L_test (SSEE − CPL)  = {cv_res['ssee']['ll_test'] - cv_res['cpl']['ll_test']:+.4f}
""")

    # Texto LaTeX listo para insertar
    B_str  = f"{B:.2f}"
    lnB_str= f"{lnB:+.2f}"
    dl_lcdm= f"{cv_res['ssee']['ll_test'] - cv_res['lcdm']['ll_test']:+.2f}"
    dl_cpl = f"{cv_res['ssee']['ll_test'] - cv_res['cpl']['ll_test']:+.2f}"

    print("─" * 60)
    print("BLOQUE LaTeX PARA APÉNDICE B:")
    print("─" * 60)
    print(f"""
\\subsection*{{B.1 Savage--Dickey density ratio}}

For nested models, the Bayes factor for the dynamic sector is given
exactly by the Savage--Dickey density ratio~\\cite{{Verdinelli1995}}:
\\begin{{equation}}
  B_{{\\rm SSEE/CPL}} = \\frac{{p(w_0^{{\\rm S}},w_a^{{\\rm S}}\\,|\\,\\mathrm{{data,CPL}})}}
  {{\\pi(w_0^{{\\rm S}},w_a^{{\\rm S}}\\,|\\,\\mathrm{{CPL}})}} = {B_str}
  \\quad (\\ln B = {lnB_str}).
\\end{{equation}}
The CPL posterior is evaluated at the algebraic SSEE point
$(w_0,w_a)=({W0_SSEE},{WA_SSEE})$ using a Scott-bandwidth
Gaussian KDE of the CPL chains ($N=500\\,000$ thinned samples).
The prior is the truncated Gaussian
$\\mathcal{{N}}(-1,0.5^2)\\times\\mathcal{{N}}(0,1^2)$ clipped to the
sampling box used in the MCMC.

\\subsection*{{B.2 Predictive cross-validation}}

We split the 13 DESI~DR2 BAO measurements into a
training set ($z<1.0$; 7~points) and a test set ($z\\geq1.0$;
6~points) and fit each model on the training set only.
SSEE has $k=1$ free parameter (H$_0$, with $w_0,w_a,\\Omega_m$
fixed algebraically); \\LCDM has $k=2$ ($H_0,\\Omega_m$);
CPL has $k=4$.

\\begin{{center}}
\\begin{{tabular}}{{lccc}}
\\toprule
Model & $k$ & $\\chi^2_r$(train) & $\\Delta\\ln L_{{\\rm test}}$\\\\
\\midrule
SSEE     & 1 & {cv_res['ssee']['chi2r_train']:.3f}  & ---\\\\
\\LCDM   & 2 & {cv_res['lcdm']['chi2r_train']:.3f}  & {dl_lcdm}\\\\
CPL      & 4 & {cv_res['cpl']['chi2r_train']:.3f}   & {dl_cpl}\\\\
\\bottomrule
\\end{{tabular}}
\\end{{center}}

$\\Delta\\ln L_{{\\rm test}} = \\ln L_{{\\rm test}}^{{\\rm SSEE}} - \\ln L_{{\\rm test}}^{{\\rm model}}$.
A positive value indicates that SSEE predicts the test set better
despite having the fewest free parameters, confirming that the
improvement in the dynamic BIC is not driven by overfitting.
""")


# ════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    sddr_res = savage_dickey()
    cv_res   = cross_validation()
    print_paper_summary(sddr_res, cv_res)
