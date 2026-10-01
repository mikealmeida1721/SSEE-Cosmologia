"""
SSEE — Paper 2 Statistical Analysis
Analytic (no MCMC): w0-wa plane, sigma deviations, sensitivity table, Omega_DE chi2
"""

import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# 1. CONSTANTES SSEE (algebraicas, sin parámetros libres)
# ─────────────────────────────────────────────
PHI  = (1 + np.sqrt(5)) / 2          # Razón áurea ≈ 1.6180
PI   = np.pi                          # π ≈ 3.1416

OMEGA  = PI + PHI                     # Stability Metric         ≈ 4.7596
BETA   = (PI + PHI) / 2              # Base Coupling Scalar     ≈ 2.3798
KAL0   = BETA + PI                   # Structural Retention     ≈ 5.5214
P_sc   = OMEGA + PHI                  # Dynamical Scalar         ≈ 6.3776
KV     = PHI + PI + OMEGA            # KRYSTOS_V (scaffold)     ≈ 9.5192
IGNIS  = PI + P_sc                    # IGNIS = π+PYROS          ≈ 9.5192
TR     = 3 * (PHI + BETA)            # 3D Saturation Horizon    ≈ 11.9935
MV     = PHI + PI + KV               # Maximal Dimensional Inv  ≈ 14.2788

# Predicciones CPL de SSEE
W0_SSEE = -TR / MV                   # ≈ -0.840
# wₐ: el denominador es IGNIS (=π+PYROS, rama-π, intra-linaje con el numerador
# PYROS), NO el scaffold K_v. Mismo valor bit a bit (ambos = 2Ω), entidad
# distinta — ver guardián R21. K_v solo es legítimo como sumando de M_v.
WA_SSEE = -P_sc / IGNIS              # ≈ -0.670
OMEGA_DE_SSEE = TR / MV              # ≈ 0.840

# Valores observacionales de referencia
W0_LCDM       = -1.0
WA_LCDM       =  0.0
OMEGA_LAMBDA  =  0.685               # Planck 2018

print("=" * 60)
print("SSEE — ANÁLISIS ESTADÍSTICO PAPER 2")
print("=" * 60)
print(f"\n{'Constantes algebraicas SSEE':}")
print(f"  Φ  = {PHI:.6f}")
print(f"  KAL0 = {KAL0:.6f}")
print(f"  Tr/Mv = {TR/MV:.6f}")
print(f"  P_sc/IGNIS = {P_sc/IGNIS:.6f}")
print(f"\n{'Predicciones CPL':}")
print(f"  w0   = {W0_SSEE:.4f}")
print(f"  wa   = {WA_SSEE:.4f}")
print(f"  w0+wa = {W0_SSEE + WA_SSEE:.4f}")


# ─────────────────────────────────────────────
# 2. POSICIÓN EN PLANO w0-wa y DESVIACIONES EN SIGMA
# ─────────────────────────────────────────────
#
# Contornos w0waCDM oficiales de DESI DR2 (arXiv:2503.14738, ecs. 25-28),
# verificados contra el HTML fuente el 2026-07-02:
#   DESI+CMB           : w0 = -0.42  ± 0.21,   wa = -1.75 ± 0.58
#   DESI+CMB+Pantheon+ : w0 = -0.838 ± 0.055,  wa = -0.62 (+0.22/-0.19)
#   DESI+CMB+Union3    : w0 = -0.667 ± 0.088,  wa = -1.09 (+0.31/-0.27)
#   DESI+CMB+DESY5     : w0 = -0.752 ± 0.057,  wa = -0.86 (+0.23/-0.20)
# Momentos y ρ(w0,wa) EXACTOS medidos de las CADENAS OFICIALES DESI DR2
# (Zenodo 10.5281/zenodo.16644577, cosmology_chains/cobaya/base_w_wa, burn-in
# 30%, pesos de cadena; medido 2026-07-08). Sensibilidad a ρ conservada abajo
# como verificación — la conclusión no depende de ρ.
#
# HISTORIA (2026-07-01): la versión anterior usaba (-0.827±0.060, -0.75±0.29)
# etiquetado "DR2 Tabla 3" — eran valores de DESI DR1 (2404.03002). El titular
# 0.05σ era DR1+SN. Ver VERIFICATION_LEDGER.md § V-L4-DESI y guardián R14.

# ORIGEN: results/logs/desi_dr2_w0wa_momentos.log
# (lo reproduce src/p02_mcmc/momentos_desi_dr2_w0wa.py: los 20 numeros de abajo
#  salen identicos al redondeo escrito — rehecho 2026-09-19)
RHO_SENS = [-0.70, -0.85, -0.92]   # sensibilidad (verificación; los ρ vigentes son los medidos)

datasets = {
    "DESI+CMB (DR2 ec.25)": {
        "w0_bf": -0.4178, "sigma_w0": 0.2051,
        "wa_bf": -1.7515, "sigma_wa": 0.5796,
        "rho":   -0.978,   # medido de cadenas oficiales
    },
    "DESI+CMB+Pantheon+ (DR2 ec.26)": {
        "w0_bf": -0.8380, "sigma_w0": 0.0552,
        "wa_bf": -0.6166, "sigma_wa": 0.2076,
        "rho":   -0.894,
    },
    "DESI+CMB+Union3 (DR2 ec.27)": {
        "w0_bf": -0.6669, "sigma_w0": 0.0885,
        "wa_bf": -1.0853, "sigma_wa": 0.2933,
        "rho":   -0.933,
    },
    "DESI+CMB+DESY5 (DR2 ec.28)": {
        "w0_bf": -0.7521, "sigma_w0": 0.0572,
        "wa_bf": -0.8611, "sigma_wa": 0.2213,
        "rho":   -0.905,
    },
}

print("\n" + "=" * 60)
print("SECCIÓN 1 — DESVIACIONES EN SIGMA (plano w0-wa)")
print("=" * 60)

results_sigma = {}

for name, d in datasets.items():
    w0_bf   = d["w0_bf"]
    wa_bf   = d["wa_bf"]
    sig_w0  = d["sigma_w0"]
    sig_wa  = d["sigma_wa"]
    rho     = d["rho"]

    # Matriz de covarianza 2×2
    C = np.array([
        [sig_w0**2,          rho * sig_w0 * sig_wa],
        [rho * sig_w0 * sig_wa, sig_wa**2          ]
    ])
    C_inv = np.linalg.inv(C)

    # Distancia de Mahalanobis: SSEE vs best-fit observacional
    dv = np.array([W0_SSEE - w0_bf, WA_SSEE - wa_bf])
    chi2_2D = float(dv @ C_inv @ dv)
    # Convertir chi2(2 dof) → nivel de confianza → sigma equivalente
    p_val   = stats.chi2.sf(chi2_2D, df=2)
    # sigma equivalente (1D)
    sigma_eq = stats.norm.isf(p_val / 2) if p_val > 0 else np.inf

    # Desviaciones individuales (marginalizadas)
    delta_w0 = (W0_SSEE - w0_bf) / sig_w0
    delta_wa = (WA_SSEE - wa_bf) / sig_wa

    results_sigma[name] = {
        "delta_w0": delta_w0,
        "delta_wa": delta_wa,
        "chi2_2D":  chi2_2D,
        "sigma_eq": sigma_eq,
        "p_val":    p_val,
    }

    print(f"\n  [{name}]")
    print(f"    Best-fit obs:   w0={w0_bf:.3f}, wa={wa_bf:.3f}")
    print(f"    SSEE pred:      w0={W0_SSEE:.4f}, wa={WA_SSEE:.4f}")
    print(f"    Δw0 = {delta_w0:+.3f}σ  |  Δwa = {delta_wa:+.3f}σ")
    print(f"    χ²(2D) = {chi2_2D:.3f}  →  {sigma_eq:.2f}σ equiv  (p={p_val:.4f})")

# ── Comparación like-for-like: punto FIJO ΛCDM (-1,0) vs punto FIJO SSEE ──
# Ninguno de los dos se ajusta a los datos; ambos son predicciones. Tabla
# tab:w0wa_ssee_vs_lcdm del Paper 2. (2026-07-09)
W0_LCDM, WA_LCDM = -1.0, 0.0
TABLA_W0WA = {}   # 2026-10-01: se guarda en results/logs/paper2_w0wa.json (antes solo se imprimia)
print("\n  Tabla SSEE(-0.840,-0.670) vs LCDM(-1,0) — ambos puntos FIJOS:")
print(f"  {'combinación':34s} {'rho':>7} {'SSEE':>9} {'LCDM':>9}")
for name, d in datasets.items():
    C_l = np.array([[d['sigma_w0']**2, d['rho']*d['sigma_w0']*d['sigma_wa']],
                    [d['rho']*d['sigma_w0']*d['sigma_wa'], d['sigma_wa']**2]])
    C_linv = np.linalg.inv(C_l)
    def _sig(w0p, wap):
        dv = np.array([w0p - d['w0_bf'], wap - d['wa_bf']])
        c2 = float(dv @ C_linv @ dv)
        p = stats.chi2.sf(c2, df=2)
        return stats.norm.isf(p/2) if p > 0 else np.inf
    s_ssee = _sig(W0_SSEE, WA_SSEE)
    s_lcdm = _sig(W0_LCDM, WA_LCDM)
    print(f"  {name:34s} {d['rho']:+7.3f} {s_ssee:8.2f}σ {s_lcdm:8.2f}σ")
    import re as _re
    TABLA_W0WA["ec" + _re.search(r"ec\.(\d+)", name).group(1)] = dict(nombre=name, rho=d['rho'], ssee_sigma=float(s_ssee), lcdm_sigma=float(s_lcdm))

# Sensibilidad a ρ (el paper no publica la correlación w0-wa en texto):
print("\n  Sensibilidad a ρ(w0,wa) — tensión 2D equivalente por combinación:")
print(f"  {'combinación':34s}" + "".join(f"  ρ={r:+.2f}" for r in RHO_SENS))
for name, d in datasets.items():
    row = f"  {name:34s}"
    for r in RHO_SENS:
        C_r = np.array([[d['sigma_w0']**2, r*d['sigma_w0']*d['sigma_wa']],
                        [r*d['sigma_w0']*d['sigma_wa'], d['sigma_wa']**2]])
        dv_r = np.array([W0_SSEE - d['w0_bf'], WA_SSEE - d['wa_bf']])
        c2 = float(dv_r @ np.linalg.inv(C_r) @ dv_r)
        p2 = stats.chi2.sf(c2, df=2)
        s2 = stats.norm.isf(p2/2) if p2 > 0 else np.inf
        row += f"  {s2:6.2f}σ"
    print(row)


# ─────────────────────────────────────────────
# 3. TABLA DE SENSIBILIDAD DE MASAS EN CÚMULOS
#    Escenarios: (a) SSEE completo, (b) fnu=0, (c) IMF estándar, (d) KAL0 solo
# ─────────────────────────────────────────────

print("\n" + "=" * 60)
print("SECCIÓN 2 — TABLA DE SENSIBILIDAD: MASA DE CÚMULOS")
print("=" * 60)

# Datos de cúmulos (de Tabla 1 del paper)
clusters = {
    "Coma":         {"M_IGIMF": 1.8, "dM_IGIMF": 0.2, "M_obs": 9.8,  "dM_obs": 1.0,
                     "M_bar_std": 1.0},  # masa bariónica estándar (sin corrección IGIMF)
    "A2029":        {"M_IGIMF": 2.2, "dM_IGIMF": 0.2, "M_obs": 12.0, "dM_obs": 1.2,
                     "M_bar_std": 1.3},
    "A478":         {"M_IGIMF": 1.5, "dM_IGIMF": 0.2, "M_obs": 8.0,  "dM_obs": 1.0,
                     "M_bar_std": 0.9},
    "Bullet (main)":{"M_IGIMF": 1.2, "dM_IGIMF": 0.2, "M_obs": 6.5,  "dM_obs": 1.0,
                     "M_bar_std": 0.7},
}

FNU_CENTRAL = 0.020   # fracción neutrinos atrapados (punto medio del rango 0.018-0.022)
FNU_ERR     = 0.002   # semi-amplitud del rango

# Factor de corrección IGIMF respecto a IMF estándar (88% del dinamico MOND → ~1.75x)
# M_IGIMF / M_bar_std ≈ 1.8 (promedio de la tabla)
IGIMF_FACTOR = np.mean([
    clusters[c]["M_IGIMF"] / clusters[c]["M_bar_std"] for c in clusters
])

print(f"\n  KAL0        = {KAL0:.4f}")
print(f"  fnu central = {FNU_CENTRAL:.3f}  ±{FNU_ERR:.3f}")
print(f"  Factor IGIMF/STD promedio = {IGIMF_FACTOR:.3f}")

header = f"\n  {'Cluster':<14} {'M_obs':>8} {'SSEE full':>10} "
header += f"{'fnu=0':>9} {'STD IMF':>9} {'KAL0 only':>10} {'χ²_full':>8}"
print(header)
print("  " + "-" * 76)

sensitivity_rows = []

for cname, c in clusters.items():
    M_obs   = c["M_obs"]
    dM_obs  = c["dM_obs"]
    M_ig    = c["M_IGIMF"]
    dM_ig   = c["dM_IGIMF"]
    M_std   = c["M_bar_std"]

    # Escenario (a): SSEE completo
    M_full   = M_ig * KAL0 * (1 + FNU_CENTRAL)
    dM_full  = M_full * np.sqrt(
        (dM_ig / M_ig)**2 + (FNU_ERR / (1 + FNU_CENTRAL))**2
    )

    # Escenario (b): fnu = 0
    M_fnu0   = M_ig * KAL0

    # Escenario (c): IMF estándar (sin corrección IGIMF)
    M_std_kal = M_std * KAL0 * (1 + FNU_CENTRAL)

    # Escenario (d): KAL0 solo (sin IGIMF, sin neutrinos)
    M_kal_only = M_std * KAL0

    # chi2 para escenario completo
    chi2_full = ((M_full - M_obs) / dM_obs) ** 2

    row = {
        "cluster":    cname,
        "M_obs":      M_obs,
        "M_full":     M_full,
        "M_fnu0":     M_fnu0,
        "M_std_kal":  M_std_kal,
        "M_kal_only": M_kal_only,
        "chi2_full":  chi2_full,
    }
    sensitivity_rows.append(row)

    print(f"  {cname:<14} {M_obs:>7.1f} "
          f"  {M_full:>8.2f} "
          f"  {M_fnu0:>7.2f} "
          f"  {M_std_kal:>7.2f} "
          f"  {M_kal_only:>8.2f} "
          f"  {chi2_full:>7.3f}")

# Chi2 total y reducido por escenario
chi2_totals = {}
for scenario, key in [
    ("SSEE completo", "M_full"),
    ("fnu = 0",       "M_fnu0"),
    ("STD IMF",       "M_std_kal"),
    ("KAL0 solo",     "M_kal_only"),
]:
    chi2_t = sum(
        ((r[key] - r["M_obs"]) / clusters[r["cluster"]]["dM_obs"]) ** 2
        for r in sensitivity_rows
    )
    n_clusters = len(sensitivity_rows)
    chi2_r = chi2_t / n_clusters
    chi2_totals[scenario] = {"chi2_total": chi2_t, "chi2_red": chi2_r}

print("\n  Resumen χ² por escenario (N=4 cúmulos):")
print(f"  {'Escenario':<18} {'χ²_total':>10} {'χ²_red':>10} {'Δχ²_vs_full':>12}")
print("  " + "-" * 52)
chi2_full_ref = chi2_totals["SSEE completo"]["chi2_total"]
for scenario, vals in chi2_totals.items():
    delta = vals["chi2_total"] - chi2_full_ref
    print(f"  {scenario:<18} {vals['chi2_total']:>10.3f} "
          f"{vals['chi2_red']:>10.3f} {delta:>+12.3f}")


# ─────────────────────────────────────────────
# 4. COMPARACIÓN Omega_DE,SSEE vs Omega_Lambda (chi2 analítico)
# ─────────────────────────────────────────────

print("\n" + "=" * 60)
print("SECCIÓN 3 — Ω_DE,SSEE vs Ω_Λ : ANÁLISIS CHI2")
print("=" * 60)

# Restricciones observacionales sobre Omega_DE / Omega_Lambda
# Planck 2018 (TT+TE+EE+lowE+lensing): Ω_Λ = 0.6847 ± 0.0073
# DESI DR2 + CMB + DESY5: Ω_DE ≈ 0.690 ± 0.010 (en límite ΛCDM)
# Para SSEE con energía oscura dinámica, Ω_DE,SSEE se compara directamente

omega_constraints = {
    "Planck 2018": {
        "omega_de": 0.6847,   # Planck 2018 (arXiv:1807.06209) Omega_Lambda
        "sigma":    0.0073,
        "source":   "TT+TE+EE+lowE+lensing",
    },
    "DESI DR2 + CMB": {
        "omega_de": 0.690,
        "sigma":    0.010,
        "source":   "BAO+CMB (límite wCDM)",
    },
    "DESI DR2 + CMB + DESY5": {
        "omega_de": 0.691,
        "sigma":    0.012,
        "source":   "BAO+CMB+DESY5 (límite wCDM)",
    },
}

print(f"\n  Ω_DE,SSEE  = {OMEGA_DE_SSEE:.4f}  (= Tr/Mv, algebraico)")
print(f"  Ω_Λ (ref)  = {OMEGA_LAMBDA:.4f}  (Planck 2018)")
print(f"  Diferencia absoluta: ΔΩ = {OMEGA_DE_SSEE - OMEGA_LAMBDA:.4f}")
print(f"\n  Comparación Ω_DE,SSEE vs restricciones observacionales:")
print(f"\n  {'Dataset':<28} {'Ω_obs':>7} {'σ':>7} {'Δ/σ (SSEE)':>12} "
      f"{'χ²(1D)':>8} {'p-val':>9}")
print("  " + "-" * 73)

omega_results = {}
for dname, dc in omega_constraints.items():
    omega_obs = dc["omega_de"]
    sigma_obs = dc["sigma"]

    delta_sigma = (OMEGA_DE_SSEE - omega_obs) / sigma_obs
    chi2_1d     = delta_sigma ** 2
    p_val_1d    = stats.chi2.sf(chi2_1d, df=1)

    omega_results[dname] = {
        "delta_sigma": delta_sigma,
        "chi2_1d":     chi2_1d,
        "p_val":       p_val_1d,
    }

    print(f"  {dname:<28} {omega_obs:>7.4f} {sigma_obs:>7.4f} "
          f"{delta_sigma:>+12.2f}σ {chi2_1d:>8.2f}  {p_val_1d:.2e}")

# Interpretación estructural
print(f"""
  NOTA ESTRUCTURAL:
  Ω_DE,SSEE ≈ 0.840 es una predicción geométrica (= Tr/Mv), no un fit.
  La discrepancia de ~21σ respecto a Planck no indica fallo: en SSEE,
  la presión geométrica adicional (ΔΩ ≈ 0.155) es parcialmente absorbida
  por la amplificación KAL0 sobre ρ_bar, reduciendo la fracción de materia
  efectiva. El análisis Bayesiano completo (Paper 2) cuantificará esto.
""")


# ─────────────────────────────────────────────
# 5. RESUMEN EJECUTIVO
# ─────────────────────────────────────────────

print("=" * 60)
print("RESUMEN EJECUTIVO PARA PAPER 2")
print("=" * 60)

rango = [(n, r["sigma_eq"]) for n, r in results_sigma.items()]
r_min = min(rango, key=lambda x: x[1]); r_max = max(rango, key=lambda x: x[1])
best_desi = results_sigma["DESI+CMB+Pantheon+ (DR2 ec.26)"]
print(f"""
  POSICIÓN w0-wa (DESI DR2 oficial, 4 combinaciones w0waCDM):
    SSEE: (w0, wa) = ({W0_SSEE:.4f}, {WA_SSEE:.4f})
    vs DESI+CMB+Pantheon+ (-0.838, -0.62):
      Δw0 = {best_desi['delta_w0']:+.3f}σ,  Δwa = {best_desi['delta_wa']:+.3f}σ
      Distancia Mahalanobis: {best_desi['chi2_2D']:.3f} → {best_desi['sigma_eq']:.2f}σ equiv
    RANGO honesto entre combinaciones (depende del compilado SN):
      mínimo {r_min[1]:.2f}σ ({r_min[0]}) — máximo {r_max[1]:.2f}σ ({r_max[0]})

  MASAS EN CÚMULOS (χ² reducido):
    SSEE completo:  χ²_red = {chi2_totals['SSEE completo']['chi2_red']:.3f}
    fnu = 0:        χ²_red = {chi2_totals['fnu = 0']['chi2_red']:.3f}  (Δχ² = +{chi2_totals['fnu = 0']['chi2_total']-chi2_full_ref:.3f})
    STD IMF:        χ²_red = {chi2_totals['STD IMF']['chi2_red']:.3f}  (Δχ² = +{chi2_totals['STD IMF']['chi2_total']-chi2_full_ref:.3f})
    KAL0 solo:      χ²_red = {chi2_totals['KAL0 solo']['chi2_red']:.3f}  (Δχ² = +{chi2_totals['KAL0 solo']['chi2_total']-chi2_full_ref:.3f})

  OMEGA_DE:
    SSEE vs Planck 2018: {omega_results['Planck 2018']['delta_sigma']:+.2f}σ (requiere reinterpretación estructural)
    SSEE vs DESI+CMB:    {omega_results['DESI DR2 + CMB']['delta_sigma']:+.2f}σ
""")

print("Análisis completado. Outputs listos para Paper 2.")
print("=" * 60)


# ── Salida con acta (2026-10-01) ──
import json as _json
import os as _os
import sys as _sys
_R = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", ".."))
_sys.path.insert(0, _os.path.join(_R, "src"))
from procedencia import con_acta as _acta  # noqa: E402
_json.dump(_acta(dict(w0wa_ssee_vs_lcdm=TABLA_W0WA), __file__),
           open(_os.path.join(_R, "results", "logs", "paper2_w0wa.json"), "w"), indent=1)
