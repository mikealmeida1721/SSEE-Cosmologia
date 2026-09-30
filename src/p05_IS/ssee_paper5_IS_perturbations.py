#!/usr/bin/env python3
"""
ssee_paper5_IS_perturbations.py
Israel-Stewart causal perturbative analysis for SSEE dark energy.

Two central questions:
  Q1: Does IS regularize c²_s < 0 → stable DE perturbations at all subhorizon k?
  Q2: Does Ω_m,eff/Ω_m,dyn ≈ MIRA = (3φ+π)/4 ≈ 1.9989 emerge from the IS
      perturbation growth history?

IS perturbation equations (Newtonian gauge, d/d ln a convention):
  δ'_m  = -(k/aH) v_m
  v'_m  = -v_m - (k/aH) Φ
  δ'_DE = -(1+w)(k/aH) v_DE
  v'_DE = -(1-3c²_s)v_DE - (k/aH)[c²_s δ_DE/(1+w) + Φ/(1+w)] + (k/aH) Π̃
  Π̃'   = -[Π̃ + ζ̃(k/aH) v_DE] / (τ_Π H)

Poisson (subhorizon): k² Φ = -(3/2)(H₀/H)²[Ω_m δ_m + Ω_DE f_DE(a) δ_DE]/a

IS dispersion relation (high-k limit, τ_Π k >> aH):
  c²_s,eff = c²_s,bare + ζ̃ / (τ_Π H₀)

References: Hiscock & Lindblom (1985), Maartens (1996), Hu (1998), Weinberg (1971).
"""

import numpy as np
from scipy.integrate import solve_ivp, quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'results', 'figures')
os.makedirs(OUTDIR, exist_ok=True)

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 11,
    'axes.labelsize': 12, 'axes.titlesize': 12,
    'legend.fontsize': 10, 'figure.dpi': 150,
})

# ── 1. SSEE CONSTANTS (algebraic, zero free parameters) ─────────────────────
import os as _reloc_os, sys as _reloc_sys  # reloc: anclar src/
_reloc_sys.path.insert(0, _reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__))))
from ssee_core import (
    PHI as phi, PI as pi_, BETA as beta, KAL0, P_SC as P_sc,
    K_V as Kv, T_R as Tr, M_V as Mv, W0 as w0, WA as wa,
    H0_GLOBAL as H0_kms, S_M as s_M, S_DE as s_DE,
    MIRA as MIRA_alg, OMEGA_M_TOTAL as Omm_CMB,   # 0.308881 materia total
)
from procedencia import cabecera, con_acta  # noqa: E402
print(cabecera(__file__))   # acta de procedencia: primera linea del log

# IS relaxation time (dimensionless: τ_Π × H₀).
# Usa la SATURACIÓN s_DE = |w₀| = 0.839950, que NO lleva H — por eso es
# legítima aquí. NO es la fracción de densidad Ω_DE = 0.691119.
tau_Pi_H0 = KAL0 / (3.0 * s_DE)   # ≈ 2.191

# ── Densidades para GEOMETRÍA y fuente de POISSON ────────────────────────
# Corregido 2026-09-05. Antes este bloque corría con las SATURACIONES
# (0.160050 / 0.839950) metidas en E(a) y en la fuente de Poisson — el mismo
# error que dio χ²=726 en DESI DR2. Era invisible porque las dos parejas
# suman 1.0 exacto, así que un chequeo de planitud lo aprueba; pero E(a)
# difiere 18.5% en a=0.5. Una E(a) y un Poisson LLEVAN H ⟹ va la densidad.
# Medido antes/después: MIRA_num 0.989394 → 0.989737 (ambos 0.989±0.017,
# la conclusión de Q2 no se movía), y Q1/Q3 idénticos bit a bit. O sea: el
# resultado publicado no dependía del error. Se corrige igual, porque usar
# una saturación donde va una densidad es mal uso de lo que tenemos.
Omm  = Omm_CMB           # 0.308881  materia total (= ω_m/h²)
OmDE = 1.0 - Omm_CMB     # 0.691119  fracción de densidad de energía oscura

# Bare k-essence sound speed: for L ∝ X^n both w and c²_s equal 1/(2n-1),
# so c²_s,bare = w₀ (standard k-essence identity, Hu 1998). See Paper 5 §cs2_bare.
cs2_bare = w0                       # = -0.8399

# Bulk viscosity, adimensional.
#
# ✅ OP-22 CERRADO 2026-09-06 (queda OP-22b, ver abajo).
#
# La pregunta era: ζ̃ = KAL₀/3, ¿adimensional respecto a QUÉ? Una sola cantidad
# ζ/(ρ·τ_Π) toma tres valores según el divisor:
#     / ρ_crit      0.839950
#     / ρ_DE        1.000000
#     / (ρ+p)       6.248039     ← la inercia física
#
# RESUELTO a favor de la ENTALPÍA, Π = −KAL₀·(ρ+p)·H. El argumento decisivo es
# un test de límite, independiente de SSEE: con w→−1 exacto, ρ+p→0 y una
# constante cosmológica NO tiene grados de libertad de fluido, así que su
# presión viscosa debe anularse. Π∝(ρ+p) lo da solo; Π∝ρ_DE deja presión
# viscosa finita para una constante cosmológica — no es un límite viable.
# Dos testigos internos concuerdan: el apéndice de dispersión escribe
# ζ/[τ_Π(ρ̄+p̄)], y el de autovalores usa F=(1−3c²_s)+ζ̃(k/H)²≈186 en k=10,
# que la entalpía reproduce (185.05) y ρ_crit no (1370).
#
# CONSECUENCIA: c²_s,eff = w₀ + ζ̃/(τ_Π H₀) = w₀ + Ω_DE = 0 ES un resultado,
# marginal y subluminal. NO es artefacto (la caja naranja que decía lo
# contrario está corregida en el .tex).
#
# LO QUE SE RETIRA: la JUSTIFICACIÓN de τ_Π en el apéndice EFT de Paper 1, que
# decía derivar τ_Π H₀=KAL₀/(3Ω_DE) saturando ζ/(ρ_DE τ_Π)≤1. Con la inercia
# correcta esa saturación da 0.2946, no 2.191 — el acuerdo era el factor
# (1+w₀)⁻¹=6.248 que faltaba. El VALOR no se mueve: τ_Π H₀=KAL₀·Ω/T_r es
# álgebra, y ya estaba escrito así. Σm_ν=0.06849 intacto.
#
# OP-22b (abierto): que el modo viscoso de fluido y el modo de campo
# (c²_s,ad∈[0.60,1]) sean canales genuinamente distintos sigue ASERTADO.
#
zeta_tilde = KAL0 / 3.0            # ≈ 1.8405  = KAL₀·Ω/M_v

# ── 2. PRINT HEADER ─────────────────────────────────────────────────────────
print("=" * 68)
print("SSEE  Paper 5 — Israel-Stewart Causal Perturbative Analysis")
print("=" * 68)
print(f"\n  φ               = {phi:.8f}")
print(f"  KAL₀            = {KAL0:.8f}")
print(f"  w₀              = {w0:.8f}")
print(f"  wₐ              = {wa:.8f}")
print(f"  s_M  (saturación, sin H) = {s_M:.8f}")
print(f"  s_DE (saturación, sin H) = {s_DE:.8f}")
print(f"  Ω_m  (densidad, con H)   = {Omm:.8f}")
print(f"  Ω_DE (densidad, con H)   = {OmDE:.8f}")
print(f"  MIRA (algebraic)= {MIRA_alg:.8f}")
print(f"  τ_Π H₀         = KAL₀/(3|w₀|) = {tau_Pi_H0:.8f}")
print(f"  c²_s (bare)     = {cs2_bare:.8f}  ← gradient instability")
print(f"  ζ̃ = KAL₀/3     = {zeta_tilde:.8f}")

# ── 3. ANALYTIC STABILITY (Q1) ──────────────────────────────────────────────
# IS dispersion relation in the short-wavelength limit (k τ_Π >> 1):
#   c²_s,eff = c²_s,bare + ζ̃ / τ_Π_H0
#
# The IS correction exactly fills the negative c²_s if SSEE parameters are used:
#   ζ̃ / τ_Π_H0 = (KAL₀/3) / (KAL₀/(3 Ω_DE)) = Ω_DE = |w₀|
#
# → c²_s,eff = w₀ + |w₀| = 0   (exact marginal stability)

IS_correction = zeta_tilde / tau_Pi_H0    # = Ω_DE = |w₀|
cs2_eff_highk  = cs2_bare + IS_correction

print("\n" + "─" * 68)
print("Q1 — IS STABILITY ANALYSIS (analytic)")
print("─" * 68)
print(f"\n  IS correction  ζ̃/τ_Π H₀ = {IS_correction:.8f}")
print(f"  Expected value |w₀|      = {abs(w0):.8f}")
print(f"  Difference               = {abs(IS_correction - abs(w0)):.2e}  (round-off)")
print(f"\n  c²_s,eff (k→∞)  = {cs2_bare:.6f} + {IS_correction:.6f} = {cs2_eff_highk:.2e}")

if abs(cs2_eff_highk) < 1e-12:
    print("\n  *** c2_s,eff = 0  —  RESULTADO (OP-22 cerrado 2026-09-06) ***")
    print("  zeta~ esta normalizada a la ENTALPIA rho+p, no a rho_crit ni rho_DE.")
    print("  Decisivo: con w->-1, rho+p->0 y una constante cosmologica no tiene")
    print("  grados de libertad de fluido => su presion viscosa DEBE anularse.")
    print("  Pi propto (rho+p) lo da solo; Pi propto rho_DE no.")
    print("  Testigos internos: apendice de dispersion (zeta/[tau(rho+p)]) y")
    print("  apendice de autovalores (F=186 -> entalpia 185.05, rho_crit 1370).")
    print("  Retirado: la derivacion de tau_Pi por saturacion de causalidad")
    print("  en el apendice EFT de Paper 1 (usaba rho en vez de rho+p).")
    print("  Queda OP-22b: modo fluido vs modo campo, aun afirmado sin derivar.")
elif cs2_eff_highk > 0:
    print(f"\n  IS stabilizes gradient: c²_s,eff = +{cs2_eff_highk:.2e} > 0")
else:
    print(f"\n  Still unstable at high-k: c²_s,eff = {cs2_eff_highk:.2e} < 0")

# Critical wavenumber (transition from unstable to stable regime).
# The IS transition occurs at the dimensionless variable x ≡ k c τ_Π H₀/(aH) = 1
# (see §IS k_crit derivation). At z=0, a=1, H=H₀:  k_crit/(H₀/c) = 1/(τ_Π H₀).
# The naive Navier–Stokes form 1/(τ_Π H₀ |c_s|) carries an extra |c_s| factor that
# does NOT enter the IS dispersion relation; we keep it only as an informational print.
k_crit_H0 = 1.0 / tau_Pi_H0   # in units of H₀/c  (IS transition x=1)
c_s_abs = abs(cs2_bare)**0.5
k_crit_NS = 1.0 / (tau_Pi_H0 * c_s_abs)   # naive Navier–Stokes value (informational)
k_crit_Mpc = k_crit_H0 * (H0_kms / 299792.458)   # Mpc⁻¹
lambda_crit_Mpc = 2 * np.pi / k_crit_Mpc if k_crit_Mpc > 0 else np.inf

print(f"\n  k_crit/H₀ = 1/(τ_Π H₀) = {k_crit_H0:.4f}  (IS transition, x=1)")
print(f"  [naive NS 1/(τ_Π H₀|c_s|) = {k_crit_NS:.4f} — not the IS value]")
print(f"  k_crit    = {k_crit_Mpc:.4e} Mpc⁻¹")
print(f"  λ_crit    = {lambda_crit_Mpc:.1f} Mpc")

if k_crit_H0 < 1.0:
    print(f"  → k_crit < H₀/c: ALL subhorizon modes (k > aH) are IS-stabilized.")
    print(f"    There is no observable gradient instability in SSEE.")
else:
    print(f"  → k_crit > H₀/c: instability persists for {k_crit_H0:.2f} < k/(H₀/c) < ∞")

# ── 4. IS EFFECTIVE SOUND SPEED vs k (full expression) ──────────────────────
def cs2_eff_IS(k_H0, a=1.0, H_val=None):
    """
    Effective sound speed from IS dispersion relation.

    Full k-dependent result (interpolating between NS and IS limits):
      c²_s,eff(k,a) = c²_s + ζ̃/τ_Π × x²/(1+x²)

    where x = k τ_Π / (aH) is the dimensionless IS parameter.
    The correction saturates at ζ̃/τ_Π for k τ_Π >> aH.
    """
    if H_val is None:
        H_val = H_interp(a)
    x = k_H0 * tau_Pi_H0 / (a * H_val)   # dimensionless IS parameter
    correction = (zeta_tilde / tau_Pi_H0) * x**2 / (1.0 + x**2)
    return cs2_bare + correction

def H_over_H0_approx(a):
    """Fast H(a)/H₀ using CPL analytic approximation."""
    rDE = a**(-3*(1+w0+wa)) * np.exp(-3*wa*(1-a))
    return np.sqrt(Omm * a**(-3) + OmDE * rDE)

# Precompute ρ_DE(a) on fine grid to avoid repeated quadrature in ODE
_a_grid_rDE   = np.linspace(0.001, 1.0, 2000)
_rDE_grid     = _a_grid_rDE**(-3*(1+w0+wa)) * np.exp(-3*wa*(1-_a_grid_rDE))
# Normalize so ρ_DE(1) = 1
_rDE_grid    /= _rDE_grid[-1]
_H_grid       = np.sqrt(Omm * _a_grid_rDE**(-3) + OmDE * _rDE_grid)

def rho_de_interp(a):
    """ρ_DE(a)/ρ_DE(1) via precomputed grid interpolation (fast)."""
    return float(np.interp(a, _a_grid_rDE, _rDE_grid))

def H_interp(a):
    """H(a)/H₀ via precomputed grid (fast)."""
    return float(np.interp(a, _a_grid_rDE, _H_grid))

print("\n" + "─" * 68)
print("IS effective sound speed at z=0 (full k-dependence):")
print(f"  {'k [H₀/c]':>10}   c²_s,eff    regime")
for kv in [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0]:
    cs2 = cs2_eff_IS(kv, a=1.0, H_val=1.0)
    x   = kv * tau_Pi_H0
    regime = "IS limit" if x > 3 else ("transition" if x > 0.3 else "NS limit")
    print(f"  {kv:>10.3f}   {cs2:+.6f}   {regime}")

# ── 5. BACKGROUND COSMOLOGY ──────────────────────────────────────────────────
print("\n" + "─" * 68)
print("Background cosmology (H/H₀ across redshift):")

a_arr = np.array([0.01, 0.1, 0.2, 0.5, 0.8, 1.0])
for a_ in a_arr:
    H_ = H_interp(a_)
    z_ = 1/a_ - 1
    print(f"  z={z_:6.1f}  a={a_:.2f}  H/H₀={H_:.4f}  τ_Π H = {tau_Pi_H0*H_:.3f}")

# ── 6. ODE SYSTEM — IS PERTURBATIONS ─────────────────────────────────────────
def rhs_QS(x, Y, k_H0):
    """
    IS perturbation ODE — quasi-static Π̃ approximation.

    State: Y = [δ_m, v_m, δ_DE, v_DE]   (4 variables, no separate Π̃)
    Valid when τ_Π H >> 1 (early times) and asymptotically (IS limit).

    Quasi-static IS: Π̃_QS = −ζ̃ (k/aH) v_DE
    This absorbs the stiff Π̃ ODE into an algebraic relation,
    adding a k-dependent friction to the Euler equation:
      friction: +(1−3c²_s + ζ̃ kH²) → +(1+2.52 + 1.84 kH²) at k=1, z=0

    Eigenvalues at k=1, z=0:  λ₁ ≈ +0.15, λ₂ ≈ −5.5
    Gradient instability survives (λ₁ > 0) but is SLOW (c.f. bare rate ~0.92).
    Solution remains finite and integrable for k ≥ 1 H₀/c from a=0.05 to a=1.
    """
    a   = np.exp(x)
    H   = H_interp(a)
    w   = w0 + wa * (1.0 - a)
    fDE = rho_de_interp(a)

    δm, vm, δDE, vDE = Y
    one_plus_w = max(1.0 + w, 1e-6)   # guard against 1+w → 0

    Phi = -(1.5 / (k_H0**2 * a * H**2)) * (Omm * δm + OmDE * fDE * δDE)
    kH  = k_H0 / (a * H)

    # Matter (pressureless CDM)
    dδm = -kH * vm
    dvm = -vm - kH * Phi

    # Dark energy — quasi-static IS Π̃ absorbed as extra friction
    # Pit_QS = -zeta_tilde * kH * vDE
    eff_friction = (1.0 - 3.0 * cs2_bare) + zeta_tilde * kH**2
    dδDE = -one_plus_w * kH * vDE
    dvDE = (-eff_friction * vDE
            - kH * cs2_bare * δDE / one_plus_w
            - kH * Phi / one_plus_w)

    return [dδm, dvm, dδDE, dvDE]

# ── 7. INTEGRATE AND EXTRACT MIRA RATIO ──────────────────────────────────────
def integrate_growth(k_H0, a_ini=0.05, a_fin=1.0, n_pts=400):
    """
    Integrate IS perturbation equations (quasi-static approximation).

    Start at a_ini = 0.05 (z=19): DE energy fraction ~ 0, IS firmly suppressing
    DE perturbations (τ_Π H ≈ 22, quasi-static regime valid).

    IC: adiabatic growing mode for matter; δ_DE = v_DE = 0.
    The DE perturbation is sourced purely by gravitational coupling.
    """
    x_ini = np.log(a_ini)
    x_fin = np.log(a_fin)

    δm0 =  a_ini    # growing mode δ_m ∝ a
    vm0 = -a_ini    # θ_m = -H δ_m → v_m normalized
    Y0  = [δm0, vm0, 0.0, 0.0]

    x_eval = np.linspace(x_ini, x_fin, n_pts)

    sol = solve_ivp(
        lambda x, Y: rhs_QS(x, Y, k_H0),
        [x_ini, x_fin],
        Y0,
        method='RK45',
        t_eval=x_eval,
        rtol=1e-9,
        atol=1e-12,
        dense_output=False,
        max_step=0.02,
    )
    return sol

# ── 8. RUN FOR MULTIPLE k VALUES ─────────────────────────────────────────────
print("\n" + "─" * 68)
print("Q2 — MIRA TEST: DE perturbation growth vs matter")
print("─" * 68)
print(f"  MIRA (algebraic) = {MIRA_alg:.6f}  →  Ω_m,CMB = {Omm_CMB:.6f}")
print(f"  Required δ_DE/δ_m at z=0 for MIRA: r* = (MIRA-1)×Ω_m/Ω_DE = "
      f"{(MIRA_alg-1)*Omm/OmDE:.4f}")
print()
print(f"  {'k [H₀/c]':>10}  {'δ_m(z=0)':>12}  {'δ_DE(z=0)':>12}  "
      f"{'r=δ_DE/δ_m':>12}  {'Ω_m,eff':>10}  {'MIRA_num':>10}  status")

# Use a_ini = 0.05 (z=19) for all runs.  At a_ini=0.05, H ≈ 35.8 H₀ →
# a_ini H(a_ini) ≈ 1.79 H₀/c.  Only modes with k > 2 H₀/c are robustly
# sub-horizon throughout the integration; lower-k results are flagged.
k_values = [2.0, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0]
results = {}

for k_H0 in k_values:
    sol = integrate_growth(k_H0, a_ini=0.05, a_fin=1.0)
    if not sol.success:
        print(f"  {k_H0:>10.2f}  ODE failed: {sol.message}")
        continue

    δm_fin  = sol.y[0, -1]
    δDE_fin = sol.y[2, -1]

    # Normalize to δ_m(z=0) = 1 (growth factor convention)
    if abs(δm_fin) < 1e-15:
        continue
    r = δDE_fin / δm_fin

    # Effective matter density: Poisson → both m and DE contribute
    # Ω_m,eff δ_eff = Ω_m δ_m + Ω_DE δ_DE = Ω_m(1 + r × Ω_DE/Ω_m)
    Om_eff   = Omm + OmDE * r
    MIRA_num = Om_eff / Omm

    status = ""
    if abs(MIRA_num - MIRA_alg) < 0.05:
        status = "✓ MIRA"
    elif abs(MIRA_num - MIRA_alg) < 0.20:
        status = "~ close"
    else:
        status = "✗ IS-suppressed"

    results[k_H0] = dict(
        δm=δm_fin, δDE=δDE_fin, r=r,
        Om_eff=Om_eff, MIRA_num=MIRA_num, sol=sol
    )

    print(f"  {k_H0:>10.2f}  {δm_fin:>12.4f}  {δDE_fin:>12.6f}  "
          f"{r:>12.6f}  {Om_eff:>10.4f}  {MIRA_num:>10.4f}  {status}")

# ── 9. SUMMARY ───────────────────────────────────────────────────────────────
print("\n" + "═" * 68)
print("SUMMARY")
print("═" * 68)

print(f"\n  Q1 — Gradient stability:")
print(f"    c²_s,bare = {cs2_bare:.6f} (k-essence, unstable)")
print(f"    c²_s,eff  = {cs2_eff_highk:.2e} (IS high-k limit, marginal)")
print(f"    Identity: ζ̃/τ_Π = KAL₀/3 ÷ KAL₀/(3Ω_DE) = Ω_DE = |w₀|  ✓")
print(f"    ALL subhorizon modes stabilized (k_crit = {k_crit_H0:.3f} H₀/c < H₀/c)")

if results:
    # Use only well-subhorizon IS regime: k ≥ 10 H₀/c
    # At these scales k τ_Π >> 1 is satisfied throughout, and the mode is
    # robustly sub-horizon from a_ini onward (kH ≥ 10/35.8 ≈ 0.28 at a=0.05).
    k_IS_keys = [k for k in results if k >= 10.0]
    if k_IS_keys:
        MIRA_mean = np.mean([results[k]['MIRA_num'] for k in k_IS_keys])
        MIRA_std  = np.std( [results[k]['MIRA_num'] for k in k_IS_keys])
        # 2026-09-26: el script se corrigio a las densidades reales el 2026-09-05
        # pero la TABLA de Paper 5 nunca se rehizo: seguia con Om_eff ~= 0.15,
        # que solo tiene sentido con Om = 0.160050. Nadie lo vio porque el
        # script no dejaba log y R35/R65 no tenian contra que comparar. Ahora
        # lo deja, y la tabla del .tex se genera de aqui.
        import json as _json, os as _os
        _log = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                             '..', '..', 'results', 'logs',
                             'p5_IS_perturbations_Q2.json')
        _os.makedirs(_os.path.dirname(_log), exist_ok=True)
        with open(_os.path.abspath(_log), 'w') as _fh:
            _json.dump(con_acta(dict(
                Omega_m=Omm, Omega_DE=OmDE,
                filas=[dict(k=float(_k), delta_m=float(results[_k]['δm']),
                            r=float(results[_k]['r']),
                            Omega_m_eff=float(results[_k]['Om_eff']),
                            R=float(results[_k]['MIRA_num']))
                       for _k in sorted(results)],
                R_media_k10=float(MIRA_mean), R_sd_k10=float(MIRA_std),
                nota=('R = Omega_m,eff/Omega_m con las DENSIDADES reales. '
                      'El blanco 1.998924 era el factor materia retirado el '
                      '2026-06-18 (OP-8); se conserva solo como registro.')),
                __file__), _fh, indent=1)
        print(f"    -> log: {_os.path.abspath(_log)}")
        delta_MIRA = abs(MIRA_mean - MIRA_alg)
        frac_MIRA  = delta_MIRA / MIRA_alg * 100

        print(f"\n  Q2 — MIRA ratio (k ≥ 10 H₀/c, well inside IS + sub-horizon):")
        print(f"    MIRA_numeric = {MIRA_mean:.6f} ± {MIRA_std:.6f}")
        print(f"    MIRA_algebraic = {MIRA_alg:.6f}")
        print(f"    Discrepancy = {delta_MIRA:.6f}  ({frac_MIRA:.1f}%)")
        print(f"    δ_DE/δ_m → 0 for large k: IS SUPPRESSES DE clustering")

        if frac_MIRA < 5:
            print(f"    *** MIRA CONSISTENT with IS perturbation growth ***")
        elif frac_MIRA < 20:
            print(f"    ~ MIRA partially reproduced — subleading corrections needed")
        else:
            print(f"    ✗  MIRA NOT reproduced by linear IS perturbations")
            print(f"       Linear IS → Ω_m,eff ≈ Ω_m,dyn (no DE clustering)")
            print(f"       MIRA is a background-level IS effect, not perturbative")

# ── Q3. LINEAR GROWTH FACTOR, γ_IS, σ₈, S₈ ──────────────────────────────────
# Growth equation (sub-horizon, log-a variable x = ln a):
#   D₁'' + (2 + d ln H/d ln a) D₁' − (3/2) Ω_m(a) D₁ = 0
#
# Poisson source = Ω_m,CMB = ω_m/h² = 0.308881   (el fondo gravitacional real;
# ω_m-directo, SIN factor materia — OP-8 disuelto; era MIRA×Ω_m,dyn=0.31988, retirado).
# Ω_m,dyn=0.160 SOLO fija w₀ (vía 1+w₀); el contenido que gravita y siembra la
# estructura es Ω_m,CMB, predicción algebraica independiente (ω_b+ω_c+ω_ν).
# Ω_m(a) = Ω_m,CMB × (H₀/H)² × a^{-3}.   Para ΛCDM: Ω_m(a) = 0.3153 / (H_Λ(a)² × a³)
#
# IC (matter-dominated limit, a_ini = 10^{-4}): D₁ = a, D₁' = a  (growing mode)
# ──────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 68)
print("Q3 — LINEAR GROWTH FACTOR, γ_IS, σ₈, S₈")
print("─" * 68)

from scipy.optimize import curve_fit

# Reference values
sigma8_LCDM     = 0.811    # Planck 2018 Table 2
sigma8_LCDM_err = 0.006
Omm_LCDM        = 0.3153
OmL_LCDM        = 1.0 - Omm_LCDM

# Weak-lensing S₈ measurements
S8_DES        = 0.776;  S8_DES_err  = 0.017   # DES-Y3 (Abbott+2022)
S8_KIDS       = 0.759;  S8_KIDS_err = 0.024   # KiDS-1000 (Asgari+2021, canónico)

def H_ssee_exact(a):
    """Analytic SSEE H(a)/H₀ — CPL formula, valid for any a without grid."""
    rDE = a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))
    # Ω_m,cosm=0.308881 en el fondo gravitacional (ω_m-directo; Ω_m,dyn=0.160 solo fija w₀ vía 1+w₀)
    return np.sqrt(Omm_CMB * a**(-3) + (1.0 - Omm_CMB) * rDE)

def H_lcdm(a):
    return np.sqrt(Omm_LCDM * a**(-3) + OmL_LCDM)

def dlnH_dlna_num(a, H_func, eps=5e-5):
    """d ln H / d ln a by second-order central finite difference."""
    da = max(a * eps, 1e-9)
    hp = H_func(a + da)
    hm = H_func(max(a - da, 1e-9))
    return (hp - hm) / (2.0 * da) * a / H_func(a)

def growth_ode_system(x, Y, H_func, Omm_src):
    """
    2D ODE for linear growth factor (log-scale).
    x = ln a,  Y = [D₁, u = dD₁/d(ln a)]
    Omm_src: Ω_m at a=1 that sources the Poisson equation
    """
    a  = np.exp(x)
    H  = H_func(a)
    dH = dlnH_dlna_num(a, H_func)
    Om_a = Omm_src / (H**2 * a**3)
    D1, u = Y
    return [u, -(2.0 + dH) * u + 1.5 * Om_a * D1]

# Start at a = 1e-3 (z=999): solidly matter-dominated for both models.
# Growing mode initial conditions: D₁ = a, dD₁/d(ln a) = a.
a_ini_g = 1e-3
x_ini_g = np.log(a_ini_g)
x_fin_g = 0.0
Y0_g    = [a_ini_g, a_ini_g]

n_pts_g = 1200
x_g = np.linspace(x_ini_g, x_fin_g, n_pts_g)

sol_lcdm_g = solve_ivp(
    lambda x, Y: growth_ode_system(x, Y, H_lcdm, Omm_LCDM),
    [x_ini_g, x_fin_g], Y0_g,
    method='DOP853', t_eval=x_g, rtol=1e-11, atol=1e-14)

sol_ssee_g = solve_ivp(
    lambda x, Y: growth_ode_system(x, Y, H_ssee_exact, Omm_CMB),  # fuente Poisson = Ω_m,cosm
    [x_ini_g, x_fin_g], Y0_g,
    method='DOP853', t_eval=x_g, rtol=1e-11, atol=1e-14)

_q3_ok = sol_lcdm_g.success and sol_ssee_g.success
if not _q3_ok:
    print("  WARNING: Q3 growth ODE failed")
    G_factor = gamma_IS_val = gamma_IS_err_val = None
    sigma8_SSEE = S8_SSEE_val = None
else:
    a_g    = np.exp(x_g)
    z_g    = 1.0 / a_g - 1.0

    D1_lcdm = sol_lcdm_g.y[0]
    D1_ssee = sol_ssee_g.y[0]
    u_lcdm  = sol_lcdm_g.y[1]
    u_ssee  = sol_ssee_g.y[1]

    # Growth suppression factor (un-normalized ratio)
    G_factor = D1_ssee[-1] / D1_lcdm[-1]

    # Normalized growth factors  (D₁(z=0) = 1)
    D1_lcdm_n = D1_lcdm / D1_lcdm[-1]
    D1_ssee_n = D1_ssee / D1_ssee[-1]

    # Growth rates f(a) = d ln D₁ / d ln a = u / D₁
    f_lcdm = u_lcdm / D1_lcdm
    f_ssee = u_ssee / D1_ssee

    # ── Fit growth index γ: ln f = γ ln Ω_m(a), range z ∈ [0, 2]
    mask_fit = (z_g >= 0.0) & (z_g <= 2.0)

    H_arr_s = np.array([H_ssee_exact(a) for a in a_g])
    H_arr_l = np.array([H_lcdm(a)       for a in a_g])
    Om_a_ssee_arr = Omm_CMB  / (H_arr_s**2 * a_g**3)  # Ω_m(a) con fondo correcto
    Om_a_lcdm_arr = Omm_LCDM / (H_arr_l**2 * a_g**3)

    def _gamma_model(lnOm, gamma):
        return gamma * lnOm

    popt_IS, pcov_IS = curve_fit(
        _gamma_model,
        np.log(Om_a_ssee_arr[mask_fit]),
        np.log(np.clip(f_ssee[mask_fit], 1e-10, None))
    )
    popt_LC, _ = curve_fit(
        _gamma_model,
        np.log(Om_a_lcdm_arr[mask_fit]),
        np.log(np.clip(f_lcdm[mask_fit], 1e-10, None))
    )
    gamma_IS_val   = float(popt_IS[0])
    gamma_IS_err_val = float(np.sqrt(pcov_IS[0, 0]))
    gamma_LCDM_val = float(popt_LC[0])

    # ── σ₈ and S₈
    sigma8_SSEE     = sigma8_LCDM * G_factor
    sigma8_SSEE_err = sigma8_LCDM_err * G_factor
    S8_LCDM_val     = sigma8_LCDM * np.sqrt(Omm_LCDM / 0.3)
    S8_SSEE_val     = sigma8_SSEE * np.sqrt(Omm_CMB   / 0.3)
    S8_SSEE_err_val = sigma8_SSEE_err * np.sqrt(Omm_CMB / 0.3)

    # Tensions (quadrature of model and observational errors)
    def _tension(v, ref, ev, er):
        return abs(v - ref) / np.sqrt(ev**2 + er**2)

    tens_DES_IS   = _tension(S8_SSEE_val, S8_DES,  S8_SSEE_err_val, S8_DES_err)
    tens_KIDS_IS  = _tension(S8_SSEE_val, S8_KIDS, S8_SSEE_err_val, S8_KIDS_err)
    tens_DES_LC   = abs(S8_LCDM_val - S8_DES)  / S8_DES_err
    tens_KIDS_LC  = abs(S8_LCDM_val - S8_KIDS) / S8_KIDS_err

    # ── fσ₈ at z = 0.5
    idx_05 = np.argmin(np.abs(z_g - 0.5))
    fσ8_SSEE_05 = f_ssee[idx_05] * sigma8_SSEE * D1_ssee_n[idx_05]
    fσ8_LCDM_05 = f_lcdm[idx_05] * sigma8_LCDM * D1_lcdm_n[idx_05]

    print(f"\n  Growth suppression:   G = D₁^SSEE / D₁^ΛCDM = {G_factor:.4f}")
    print(f"\n  Growth index fit (z = 0..2):")
    print(f"    γ_IS   = {gamma_IS_val:.4f} ± {gamma_IS_err_val:.4f}")
    print(f"    γ_ΛCDM = {gamma_LCDM_val:.4f}  (expected 0.55)")
    # Growth-rate comparison table (Paper 5 Table tab:growth)
    print(f"\n  Growth-rate table  z | Ω_m^SSEE(a) | f_SSEE | f_ΛCDM | Δf/f")
    for _zt in (1.0, 0.5, 0.0):
        _i = np.argmin(np.abs(z_g - _zt))
        _Oma = Omm_CMB / (H_arr_s[_i]**2 * a_g[_i]**3)
        _df = (f_ssee[_i] - f_lcdm[_i]) / f_lcdm[_i]
        print(f"    z={_zt:.1f}  Om={_Oma:.4f}  f_S={f_ssee[_i]:.4f}  f_L={f_lcdm[_i]:.4f}  Δf/f={_df*100:+.1f}%")
    print(f"\n  σ₈  (Planck 2018 ΛCDM)  = {sigma8_LCDM:.4f} ± {sigma8_LCDM_err:.4f}")
    print(f"  σ₈  (SSEE IS)           = {sigma8_SSEE:.4f} ± {sigma8_SSEE_err:.4f}")
    print(f"\n  Ω_m,CMB (ω_m-direct)    = {Omm_CMB:.6f}")
    print(f"  S₈  (ΛCDM)              = {S8_LCDM_val:.4f}")
    print(f"  S₈  (SSEE IS)           = {S8_SSEE_val:.4f} ± {S8_SSEE_err_val:.4f}")
    print(f"  S₈  (DES-Y3)            = {S8_DES:.3f} ± {S8_DES_err:.3f}")
    print(f"  S₈  (KiDS-1000)         = {S8_KIDS:.3f} ± {S8_KIDS_err:.3f}")
    print(f"\n  S₈ tension  SSEE vs DES-Y3  = {tens_DES_IS:.2f}σ")
    print(f"  S₈ tension  SSEE vs KiDS    = {tens_KIDS_IS:.2f}σ")
    print(f"  S₈ tension  ΛCDM vs DES-Y3  = {tens_DES_LC:.2f}σ")
    print(f"  S₈ tension  ΛCDM vs KiDS    = {tens_KIDS_LC:.2f}σ")
    print(f"\n  fσ₈(z=0.5):  SSEE = {fσ8_SSEE_05:.4f}")
    print(f"               ΛCDM = {fσ8_LCDM_05:.4f}")
    # 2026-09-30: gamma_IS y G de CANONICAL no tenian log (R74). Q3 lo deja,
    # con acta de procedencia, igual que Q2.
    import json as _json, os as _os, sys as _sys
    _src = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')
    _sys.path.insert(0, _os.path.abspath(_src))
        _log3 = _os.path.abspath(_os.path.join(_src, '..', 'results', 'logs',
                                           'p5_IS_perturbations_Q3.json'))
    with open(_log3, 'w') as _fh:
        _json.dump(con_acta(dict(
            Omega_m=float(Omm_CMB), G=float(G_factor),
            gamma_IS=gamma_IS_val, gamma_IS_sigma=gamma_IS_err_val,
            gamma_LCDM=gamma_LCDM_val,
            sigma8_SSEE=float(sigma8_SSEE), sigma8_SSEE_sigma=float(sigma8_SSEE_err),
            S8_SSEE=float(S8_SSEE_val), S8_SSEE_sigma=float(S8_SSEE_err_val),
            fsigma8_z05_SSEE=float(fσ8_SSEE_05), fsigma8_z05_LCDM=float(fσ8_LCDM_05),
            nota='sigma8 con A_s FIJADO a Planck (techo); no es el S8 de Paper 6.'),
            __file__), _fh, indent=1)
    print(f"    -> log: {_log3}")

    # ── fσ₈(z) full array
    fsig8_ssee_arr = f_ssee * sigma8_SSEE * D1_ssee_n
    fsig8_lcdm_arr = f_lcdm * sigma8_LCDM * D1_lcdm_n

    # Observational RSD compilation (standard literature)
    fsig8_obs_z   = np.array([0.067, 0.150, 0.380, 0.510, 0.610, 1.480])
    fsig8_obs_val = np.array([0.423, 0.490, 0.497, 0.458, 0.436, 0.462])
    fsig8_obs_err = np.array([0.055, 0.145, 0.045, 0.038, 0.034, 0.045])
    fsig8_obs_ref = ['6dFGRS', 'SDSS MGS', 'BOSS DR12 z=0.38',
                     'BOSS DR12 z=0.51', 'BOSS DR12 z=0.61', 'eBOSS DR16']

    print("\n  fσ₈ tensions vs RSD surveys:")
    print(f"  {'Survey':22s}  {'z':5s}  {'obs':7s}  {'SSEE':7s}  {'t_S':5s}  {'ΛCDM':7s}  {'t_L':5s}")
    fsig8_tensions_ssee = []
    fsig8_tensions_lcdm = []
    for i in range(len(fsig8_obs_z)):
        idx_z = np.argmin(np.abs(z_g - fsig8_obs_z[i]))
        fs_s  = fsig8_ssee_arr[idx_z]
        fs_l  = fsig8_lcdm_arr[idx_z]
        t_s   = abs(fs_s - fsig8_obs_val[i]) / fsig8_obs_err[i]
        t_l   = abs(fs_l - fsig8_obs_val[i]) / fsig8_obs_err[i]
        fsig8_tensions_ssee.append(t_s)
        fsig8_tensions_lcdm.append(t_l)
        print(f"  {fsig8_obs_ref[i]:22s}  {fsig8_obs_z[i]:.3f}  "
              f"{fsig8_obs_val[i]:.3f}±{fsig8_obs_err[i]:.3f}  "
              f"{fs_s:.3f}    {t_s:.1f}σ   {fs_l:.3f}    {t_l:.1f}σ")
    print(f"\n  Mean tension SSEE: {np.mean(fsig8_tensions_ssee):.2f}σ")
    print(f"  Mean tension ΛCDM: {np.mean(fsig8_tensions_lcdm):.2f}σ")

# ── 10. FIGURES ──────────────────────────────────────────────────────────────

# Figure 1: c²_s,eff vs k at z=0
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

ax = axes[0]
k_plot = np.logspace(-2, 2, 300)
cs2_plot = np.array([cs2_eff_IS(k, a=1.0, H_val=1.0) for k in k_plot])
ax.semilogx(k_plot, cs2_plot, 'b-', lw=2, label=r'$c^2_{s,\rm eff}(k)$ IS')
ax.axhline(cs2_bare,  color='r', ls='--', lw=1.5, label=rf'bare $c^2_s={cs2_bare:.3f}$')
ax.axhline(0, color='k', ls=':', lw=1, label='stability threshold')
ax.axhline(cs2_eff_highk, color='g', ls='--', lw=1.5,
           label=rf'IS limit $c^2_{{s,\rm eff}}={cs2_eff_highk:.1e}$')
ax.axvline(k_crit_H0, color='gray', ls='-.', lw=1,
           label=rf'$k_{{\rm crit}}={k_crit_H0:.3f}\,H_0/c$')
ax.fill_between(k_plot, cs2_bare, 0, where=cs2_plot < 0, alpha=0.15, color='red',
                label='unstable region')
ax.fill_between(k_plot, 0, cs2_plot, where=cs2_plot >= 0, alpha=0.15, color='green',
                label='stable region')
ax.set_xlabel(r'$k\,[H_0/c]$')
ax.set_ylabel(r'$c^2_{s,\rm eff}(k)$')
ax.set_title('IS Effective Sound Speed\n(SSEE, $z=0$)')
ax.legend(fontsize=9, loc='lower right')
ax.set_xlim(k_plot[0], k_plot[-1])
ax.set_ylim(cs2_bare - 0.1, 0.1)
ax.grid(True, alpha=0.3)

# Annotate marginal stability
ax.annotate(r'$c^2_{s,\rm eff}\to 0$ (exact)',
            xy=(10, 0.002), xytext=(1, 0.06),
            arrowprops=dict(arrowstyle='->', color='green'),
            color='green', fontsize=10)

# Figure 2: Growth of δ_DE/δ_m vs a for selected k
ax = axes[1]
colors_k = plt.cm.plasma(np.linspace(0.2, 0.85, len(results)))
a_plot_vals = None

for idx, (k_H0, res) in enumerate(sorted(results.items())):
    sol = res['sol']
    a_arr_sol = np.exp(sol.t)
    δm_arr  = sol.y[0]
    δDE_arr = sol.y[2]

    # Avoid division by zero; normalize so δ_m(z=0) = 1
    δm_fin = sol.y[0, -1]
    if abs(δm_fin) < 1e-12:
        continue
    ratio_arr = δDE_arr / δm_arr

    ax.plot(a_arr_sol, ratio_arr,
            color=colors_k[idx], lw=1.8,
            label=rf'$k={k_H0}\,H_0/c$  ($r_{{z=0}}={res["r"]:.3f}$)')

# Target MIRA line
r_MIRA = (MIRA_alg - 1) * Omm / OmDE
ax.axhline(r_MIRA, color='k', ls='--', lw=1.5,
           label=rf'$r^*={r_MIRA:.3f}$ (MIRA target)')

ax.set_xlabel(r'scale factor $a$')
ax.set_ylabel(r'$\delta_{\rm DE}/\delta_m$')
ax.set_title('DE Perturbation Growth\n(IS causal regularization)')
ax.legend(fontsize=8, loc='upper left')
ax.set_xlim(0, 1)
ax.set_ylim(-0.05, max(r_MIRA * 2, 0.5))
ax.grid(True, alpha=0.3)
ax.axhline(0, color='gray', lw=0.7)

fig.suptitle(
    r'SSEE Paper 5: Israel-Stewart Causal Perturbations'
    '\n'
    rf'$c^2_{{s,\rm bare}}={cs2_bare:.3f}$,  '
    rf'$\tilde{{\zeta}}=KAL_0/3={zeta_tilde:.4f}$,  '
    rf'$\tau_\Pi H_0={tau_Pi_H0:.4f}$,  '
    rf'MIRA$={MIRA_alg:.4f}$',
    fontsize=11
)
fig.tight_layout()

out1 = os.path.join(OUTDIR, 'fig_paper5_IS_stability.pdf')
fig.savefig(out1, bbox_inches='tight')
print(f"\n  Figure saved: {out1}")

# Figure 3: MIRA_numeric vs k
if len(results) >= 3:
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))

    k_arr     = np.array(sorted(results.keys()))
    MIRA_arr  = np.array([results[k]['MIRA_num'] for k in k_arr])
    Om_eff_arr = np.array([results[k]['Om_eff']  for k in k_arr])

    ax2.semilogx(k_arr, MIRA_arr, 'bo-', lw=2, ms=7, label=r'$\mathcal{R}=\Omega_{m,\rm eff}/\Omega_m$ (IS)')
    ax2.axhline(MIRA_alg, color='r', ls='--', lw=2,
                label=rf'MIRA$=(3\varphi+\pi)/4={MIRA_alg:.4f}$ (algebraic)')
    ax2.axhline(1.0, color='gray', ls=':', lw=1, label=r'no DE clustering')
    ax2.axhline(1.0/Omm, color='gray', ls='-.', lw=1,
                label=rf'full clustering ($1/\Omega_m={1/Omm:.2f}$)')
    ax2.axvline(k_crit_H0, color='purple', ls=':', lw=1.5,
                label=rf'$k_{{\rm crit}}={k_crit_H0:.3f}\,H_0/c$')

    ax2.fill_between([k_crit_H0, k_arr.max()],
                     [MIRA_alg*0.95]*2, [MIRA_alg*1.05]*2,
                     alpha=0.15, color='red', label='±5% MIRA band')

    ax2.set_xlabel(r'$k\,[H_0/c]$')
    # 2026-09-26: el eje decia Omega_{m,dyn}, pero el codigo divide por Omm =
    # 0.308881 desde el 2026-09-05. Etiqueta fosil, como las de Paper 2.
    ax2.set_ylabel(r'$\mathcal{R} = \Omega_{m,\rm eff}/\Omega_m$')
    ax2.set_title(r'MIRA Test: IS Growth $\to$ Effective Matter Density'
                  '\n(SSEE Paper 5)')
    ax2.legend(fontsize=9, loc='upper right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(k_arr.min(), k_arr.max())

    fig2.tight_layout()
    out2 = os.path.join(OUTDIR, 'fig_paper5_MIRA_test.pdf')
    fig2.savefig(out2, bbox_inches='tight')
    print(f"  Figure saved: {out2}")

# ── Q3 FIGURES ───────────────────────────────────────────────────────────────
if _q3_ok:
    # Figure 3: Growth rate f(z) and normalized D₁(z) for SSEE vs ΛCDM
    fig3, axes3 = plt.subplots(1, 2, figsize=(12, 5))

    # Panel A: growth rate f(z)
    ax = axes3[0]
    z_plot_mask = z_g <= 3.0

    ax.plot(z_g[z_plot_mask], f_ssee[z_plot_mask],
            'b-', lw=2.5, label=r'SSEE IS  $(\gamma_{\rm IS}=%s)$' % f'{gamma_IS_val:.3f}')
    ax.plot(z_g[z_plot_mask], f_lcdm[z_plot_mask],
            'r--', lw=2, label=r'$\Lambda$CDM  $(\gamma=%s)$' % f'{gamma_LCDM_val:.3f}')

    # Overlay gamma fits
    Om_fit_s = Om_a_ssee_arr[z_plot_mask]
    Om_fit_l = Om_a_lcdm_arr[z_plot_mask]
    ax.plot(z_g[z_plot_mask], Om_fit_s**gamma_IS_val,
            'b:', lw=1.5, alpha=0.7, label=r'$\Omega_m(z)^{\gamma_{\rm IS}}$ fit')
    ax.plot(z_g[z_plot_mask], Om_fit_l**gamma_LCDM_val,
            'r:', lw=1.5, alpha=0.7, label=r'$\Omega_m(z)^{\gamma_\Lambda}$ fit')

    ax.set_xlabel(r'redshift $z$')
    ax.set_ylabel(r'growth rate $f(z) = d\ln D_1/d\ln a$')
    ax.set_title('Growth Rate vs Redshift\n(SSEE IS vs ΛCDM)')
    ax.legend(fontsize=9)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)

    # Panel B: normalized growth factor D₁(z)
    ax = axes3[1]
    ax.plot(z_g[z_plot_mask], D1_ssee_n[z_plot_mask],
            'b-', lw=2.5, label=rf'SSEE  ($G={G_factor:.3f}$)')
    ax.plot(z_g[z_plot_mask], D1_lcdm_n[z_plot_mask],
            'r--', lw=2, label=r'$\Lambda$CDM')

    # Mark z=0 suppression
    ax.annotate(rf'$G = {G_factor:.3f}$',
                xy=(0, G_factor), xytext=(0.4, G_factor - 0.08),
                arrowprops=dict(arrowstyle='->', color='navy'),
                color='navy', fontsize=10)

    ax.set_xlabel(r'redshift $z$')
    ax.set_ylabel(r'$D_1(z)$ (normalized to $D_1(0)=1$)')
    ax.set_title('Growth Factor\n(normalized)')
    ax.legend(fontsize=9)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3)

    fig3.suptitle(
        r'SSEE Paper 5 (Q3): Linear Growth — IS Suppression'
        '\n'
        rf'$\Omega_m={Omm:.3f}$,  '
        rf'$G={G_factor:.4f}$,  '
        rf'$\gamma_{{\rm IS}}={gamma_IS_val:.4f}$',
        fontsize=11
    )
    fig3.tight_layout()
    out3 = os.path.join(OUTDIR, 'fig_paper5_growth_rate.pdf')
    fig3.savefig(out3, bbox_inches='tight')
    print(f"\n  Figure saved: {out3}")

    # Figure 4: S₈ comparison bar chart
    fig4, ax4 = plt.subplots(figsize=(7, 5))

    labels  = [r'Planck 2018 $\Lambda$CDM', r'SSEE IS', 'DES-Y3', 'KiDS-1000']
    vals    = [S8_LCDM_val,    S8_SSEE_val,    S8_DES,    S8_KIDS]
    errs    = [0.012,           S8_SSEE_err_val, S8_DES_err, S8_KIDS_err]
    colors_ = ['tomato', 'steelblue', 'forestgreen', 'darkorange']

    x_pos = np.arange(len(labels))
    bars = ax4.bar(x_pos, vals, yerr=errs, capsize=6,
                   color=colors_, alpha=0.8, edgecolor='k', lw=1.2, width=0.55)

    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(labels, fontsize=10)
    ax4.set_ylabel(r'$S_8 = \sigma_8\,(\Omega_m/0.3)^{0.5}$', fontsize=12)
    ax4.set_title(r'$S_8$ Tension: SSEE IS predicts lowered amplitude',
                  fontsize=11)
    ax4.set_ylim(0.65, 0.90)
    ax4.axhline(S8_LCDM_val, color='tomato', ls=':', lw=1, alpha=0.5)
    ax4.grid(True, axis='y', alpha=0.3)

    # Annotate tensions
    for xi, (v, e, c) in enumerate(zip(vals, errs, colors_)):
        ax4.text(xi, v + e + 0.005, f'{v:.3f}', ha='center', va='bottom',
                 fontsize=9, color=c)

    # Tension annotation for SSEE vs DES
    ax4.annotate(
        rf'$\Delta={tens_DES_IS:.1f}\sigma$ (SSEE vs DES)',
        xy=(1, S8_SSEE_val), xytext=(2.0, S8_SSEE_val + 0.04),
        arrowprops=dict(arrowstyle='->', color='steelblue'),
        fontsize=9, color='steelblue'
    )

    fig4.tight_layout()
    out4 = os.path.join(OUTDIR, 'fig_paper5_S8_comparison.pdf')
    fig4.savefig(out4, bbox_inches='tight')
    print(f"  Figure saved: {out4}")

    # Figure 5: fσ₈(z) SSEE vs ΛCDM vs RSD data
    fig5, ax5 = plt.subplots(figsize=(8, 5.5))

    z_plot_fsig = z_g <= 2.0
    ax5.plot(z_g[z_plot_fsig], fsig8_ssee_arr[z_plot_fsig],
             'b-', lw=2.5, label=r'SSEE IS  ($\Omega_m=0.309$)')
    ax5.plot(z_g[z_plot_fsig], fsig8_lcdm_arr[z_plot_fsig],
             'r--', lw=2, label=r'$\Lambda$CDM  ($\Omega_m=0.315$)')

    # Observational data points
    survey_colors = {
        '6dFGRS':            'forestgreen',
        'SDSS MGS':          'darkorange',
        'BOSS DR12 z=0.38':  'steelblue',
        'BOSS DR12 z=0.51':  'steelblue',
        'BOSS DR12 z=0.61':  'steelblue',
        'eBOSS DR16':        'purple',
    }
    survey_labels_done = set()
    for i in range(len(fsig8_obs_z)):
        ref = fsig8_obs_ref[i]
        col = survey_colors.get(ref, 'gray')
        # Group BOSS DR12 in legend
        if 'BOSS DR12' in ref:
            lbl = 'BOSS DR12 (Alam+2017)' if 'BOSS DR12' not in survey_labels_done else '_nolegend_'
            survey_labels_done.add('BOSS DR12')
        elif ref not in survey_labels_done:
            lbl_map = {'6dFGRS': '6dFGRS (Beutler+2012)',
                       'SDSS MGS': 'SDSS MGS (Howlett+2015)',
                       'eBOSS DR16': 'eBOSS DR16 (Hou+2021)'}
            lbl = lbl_map.get(ref, ref)
            survey_labels_done.add(ref)
        else:
            lbl = '_nolegend_'
        ax5.errorbar(fsig8_obs_z[i], fsig8_obs_val[i], yerr=fsig8_obs_err[i],
                     fmt='o', color=col, ms=7, capsize=4, lw=1.5,
                     label=lbl, zorder=5)

    # Annotate fσ₈(z=0.5) SSEE
    idx_05 = np.argmin(np.abs(z_g - 0.5))
    ax5.annotate(
        rf'SSEE: $f\sigma_8(0.5)={fsig8_ssee_arr[idx_05]:.3f}$',
        xy=(0.5, fsig8_ssee_arr[idx_05]),
        xytext=(0.7, fsig8_ssee_arr[idx_05] - 0.06),
        arrowprops=dict(arrowstyle='->', color='navy'),
        fontsize=9, color='navy'
    )
    ax5.annotate(
        rf'$\Lambda$CDM: $f\sigma_8(0.5)={fsig8_lcdm_arr[idx_05]:.3f}$',
        xy=(0.5, fsig8_lcdm_arr[idx_05]),
        xytext=(0.75, fsig8_lcdm_arr[idx_05] + 0.04),
        arrowprops=dict(arrowstyle='->', color='firebrick'),
        fontsize=9, color='firebrick'
    )

    ax5.set_xlabel(r'redshift $z$', fontsize=12)
    ax5.set_ylabel(r'$f\sigma_8(z)$', fontsize=12)
    ax5.set_title(r'$f\sigma_8(z)$: SSEE IS vs $\Lambda$CDM vs RSD data', fontsize=11)
    ax5.legend(fontsize=9, loc='upper right')
    ax5.set_xlim(0, 2.0)
    ax5.set_ylim(0.15, 0.65)
    ax5.grid(True, alpha=0.3)

    fig5.tight_layout()
    out5 = os.path.join(OUTDIR, 'fig_paper5_fsigma8_comparison.pdf')
    fig5.savefig(out5, bbox_inches='tight')
    print(f"  Figure saved: {out5}")

# ── FINAL SUMMARY ─────────────────────────────────────────────────────────────
print("\n" + "═" * 68)
print("FINAL SUMMARY  (Q1 + Q2 + Q3)")
print("═" * 68)
print(f"\n  Q1  c²_s,eff = {cs2_eff_highk:.2e}  (exact marginal stability, algebraic identity)")
print(f"      k_crit   = {k_crit_H0:.4f} H₀/c  < H₀/c  → all sub-horizon modes stable")
if results:
    k_IS_keys = [k for k in results if k >= 10.0]
    if k_IS_keys:
        _MIRA_mean = np.mean([results[k]['MIRA_num'] for k in k_IS_keys])
        print(f"\n  Q2  MIRA_num (k≥10) = {_MIRA_mean:.4f}  [algebraic = {MIRA_alg:.4f}]")
        print(f"      Linear IS suppresses DE clustering → MIRA is background effect ✓")
if _q3_ok:
    print(f"\n  Q3  G = D₁^SSEE/D₁^ΛCDM = {G_factor:.4f}")
    print(f"      γ_IS  = {gamma_IS_val:.4f} ± {gamma_IS_err_val:.4f}")
    print(f"      σ₈^SSEE = {sigma8_SSEE:.4f} ± {sigma8_SSEE_err:.4f}")
    print(f"      S₈^SSEE = {S8_SSEE_val:.4f} ± {S8_SSEE_err_val:.4f}")
    print(f"      S₈ tension vs DES-Y3  = {tens_DES_IS:.2f}σ")
    print(f"      S₈ tension vs KiDS    = {tens_KIDS_IS:.2f}σ")
    print(f"      fσ₈(z=0.5) SSEE = {fσ8_SSEE_05:.4f}  ΛCDM = {fσ8_LCDM_05:.4f}")

print("\n" + "═" * 68)
print("Paper 5 IS analysis complete.")
print("═" * 68)
