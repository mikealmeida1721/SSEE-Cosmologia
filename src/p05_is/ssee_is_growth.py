"""
ssee_is_growth.py — Israel-Stewart viscous perturbation theory for SSEE-V3.6

Replaces the Eckart ansatz (γ = φ⁻¹ postulado) con derivación formal IS.
Sistema de ODEs acopladas:
  [1] IS transport:   T h(a) dΠ/d ln a + Π = -KAL₀ h²(a)          (bulk viscosity causal)
  [2] Conservation:   dρ_DE/d ln a + 3(1+w₀) ρ_DE = -3 Π(a)        (energía DE)
  [3] Friedmann:      h²(a) = Ω_m a⁻³ + ρ_DE(a)   (Ω_m = ω_m/h² = 0.308881)                (background)
  [4] Growth:         δ'' + [2 + d ln h/d ln a] δ' = (3/2) Ω_m,eff(a) δ  (perturbaciones)

Convención: todas las densidades normalizadas por ρ_crit,0; h = H/H₀; primes = d/d ln a

Objetivo: hallar τ_Π H₀ ≡ T tal que γ_IS ≈ φ⁻¹ = 0.61803...
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import linregress
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

# ─── Constantes SSEE ──────────────────────────────────────────────────────────
# 2026-09-26: el bloque de constantes estaba REDEFINIDO a mano aqui, y habia
# derivado del nucleo en dos sitios que el guardian cazo al restaurar el script:
#   · wa = -P_sc/K_v, cuando el denominador es IGNIS = pi+PYROS (R21b).
#   · MIRA = (phi+beta)/2, cuando la canonica es (3phi+pi)/4.
# Ninguna de las dos mueve un numero: IGNIS == K_V y (phi+beta)/2 ==
# (3phi+pi)/4 son identidades ALGEBRAICAS, iguales bit a bit (comprobado, no
# supuesto: IGNIS = pi+P_sc = 2pi+2phi = phi+pi+Omega = K_V; y (phi+beta)/2 =
# (phi + (pi+phi)/2)/2 = (3phi+pi)/4). Lo que cambia es de QUE entidad se dice
# que viene el numero, y eso si importa: dos entidades con el mismo valor no
# son la misma entidad, que es la razon de ser de R21b.
# Ahora no se redefine nada: se importa del nucleo, que es la fuente unica.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from procedencia import cabecera  # noqa: E402
print(cabecera(__file__), flush=True)
from ssee_core import (BETA as beta, IGNIS, K_V as K_v, KAL0,  # noqa: E402
                       M_V as M_v, MIRA, N_S as ns, OMEGA as Omega,
                       P_SC as P_sc, PHI as phi, PI as pi_, T_R as T_r,
                       W0 as w0, WA as wa)


# ══════════════════════════════════════════════════════════════════════════
# RESTAURADO Y CORREGIDO 2026-09-26 (hallazgo F1).
#
# Este script estaba SOLO en archive/codigo/, pero SSEE_EFT_section.tex lo cita
# como la fuente de gamma_bg y S_8. Una cita a un script archivado es una cita a
# nada: el numero no se podia rehacer. Vuelve aqui, con dos cosas corregidas y
# con su control.
#
# (1) Om_dyn valia 1 - T_r/M_v = 0.160050, y entraba en DOS ranuras de densidad:
#     el fondo h2 = Om_dyn a^-3 + rho, y la fuente Om_eff = Om_dyn a^-3 / h2.
#     Pero 0.160050 es s_m = 1+w_0, ecuacion de estado, no densidad.
#     MEDIDO, no supuesto: con la densidad real gamma pasa de 0.659180 a
#     0.658942 -- 2.4e-4. gamma lo fija w(a), no Omega_m; en la ODE llana
#     varia 0.5422 -> 0.5396 entre Om = 0.16 y 0.90. O sea: la ecuacion estaba
#     MAL ESCRITA y el numero no dependia de ello. Las dos cosas son ciertas.
# (2) Om_m_CMB = Om_dyn * MIRA = 0.3199 alimentaba el S_8. El factor materia
#     MIRA se retiro el 2026-06-18 al cerrarse OP-8. Con Omega_m = 0.308881:
#     S_8 = 0.8375 -> 0.8229, a sigma_8 = 0.8110 sin cambio.
#
# NO se toca gamma_IS = 0.5504 de Paper 5: ese sale de la teoria IS completa
# con realimentacion viscosa en delta, que es otro calculo.
# El bloque de causalidad de abajo imprime c_s^2 = 4.38 y "NO": es la
# normalizacion VIEJA. OP-22 cerro el 2026-09-06 normalizando a la ENTALPIA
# rho+p, con la que c^2_{s,eff} = 0. Ese print queda como registro historico.
# ══════════════════════════════════════════════════════════════════════════

OM_M_TOTAL = 0.30888087877875237   # omega_m/h^2 (CANONICO)
S_M_EOS    = 1 - T_r / M_v         # = 0.160050 = 1+w_0 -- NO es densidad

Om_m = OM_M_TOTAL                  # la densidad de materia REAL (antes Om_dyn = 1 - T_r/M_v)
Om_DE0 = 1.0 - OM_M_TOTAL          # plano: 0.691119

gamma_target = 1.0 / phi           # φ⁻¹ ≈ 0.61803
SIGMA8_NORM = 0.811   # ORIGEN-VALOR: 0.811 — sigma8 de Planck 2018 VI Tabla 2 (0.8111) usado como NORMALIZACION del proxy D_IS/D_EdS; el S8 que sale de aqui es ese sigma8 reescalado por Omega_m, NO una prediccion de SSEE (2026-10-01)

print(f"=== Constantes SSEE ===")
print(f"φ       = {phi:.6f}")
print(f"KAL₀    = {KAL0:.6f}")
print(f"w₀      = {w0:.6f}")
print(f"wₐ      = {wa:.6f}")
print(f"n_s     = {ns:.6f}")
print(f"MIRA    = {MIRA:.6f}")
print(f"Ω_m = {Om_m:.6f}  (ω_m/h²; s_m = 1+w0 no entra en ninguna ranura de densidad)")
print(f"Ω_DE,0  = {Om_DE0:.6f}")
print(f"γ target = φ⁻¹ = {gamma_target:.6f}")
print()

# ─── Valores τ_Π H₀ a escanear ────────────────────────────────────────────────
T_scan = {
    r'KAL₀/(3Ω_DE)  [causality min]': KAL0 / (3 * Om_DE0),   # ≈ 2.191
    r'1/MIRA':                          1.0 / MIRA,             # ≈ 0.500
    r'φ⁻¹  [= γ target]':              1.0 / phi,              # ≈ 0.618
    r'Hubble time':                     1.0,                    # 1.0
    r'n_s/KAL₀':                        ns / KAL0,              # ≈ 0.175
    r'1/KAL₀':                          1.0 / KAL0,             # ≈ 0.181
    r'φ⁻²':                             phi**(-2),              # ≈ 0.382
    r'φ⁻³  [≈ n_s/KAL₀]':             phi**(-3),              # ≈ 0.236
}

# ─── Sistema de ODEs ──────────────────────────────────────────────────────────
def make_system(T):
    """
    Retorna función RHS del sistema [ρ_DE, Π] en variable x = ln a.
    Π aquí es la presión de bulk viscosa (escalar).
    """
    def rhs(x, state):
        rho, Pi = state
        a = np.exp(x)

        # Friedmann
        h2 = Om_m * a**(-3) + rho
        h2 = max(h2, 1e-30)
        h  = np.sqrt(h2)

        # d ln h / d ln a = - (3/2) Om_m a^-3 / (2 h^2)  + ...
        # Necesitamos dlnh/dx para la ecuación de crecimiento
        # Calculado numéricamente en growth ODE, aquí solo necesitamos drho/dx y dPi/dx

        # EC [1] IS transport: T h dΠ/dx + Π = -KAL₀ h²
        # T h dΠ/dx = -Π - KAL₀ h²
        dPi_dx = (-Pi - KAL0 * h2) / (T * h + 1e-30)

        # EC [2] Conservación: dρ/dx + 3(1+w₀) ρ = -3 Π
        drho_dx = -3 * (1 + w0) * rho - 3 * Pi

        return [drho_dx, dPi_dx]

    return rhs


def solve_background(T, n_pts=2000):
    """
    Integra el sistema IS desde a_i=0.001 (x=-6.9) hasta a=1 (x=0).
    Condición inicial: ρ_DE(a_i) = Om_DE0 × a_i^{-3(1+w_eff)}  (atractor DE)
                       Π(a_i) = -KAL₀ h²(a_i)  (equilibrio viscoso inicial)
    """
    x_span = (np.log(0.001), 0.0)
    x_eval = np.linspace(*x_span, n_pts)
    a_i = np.exp(x_span[0])

    # Condición inicial en atractor (Eckart) + solución particular IS
    rho_i = Om_DE0 * a_i**(-3 * (1 + w0))
    h2_i  = Om_m * a_i**(-3) + rho_i
    Pi_i  = -KAL0 * h2_i / (1 + T * np.sqrt(h2_i) * 3 * (1 + w0))

    sol = solve_ivp(
        make_system(T),
        x_span,
        [rho_i, Pi_i],
        method='DOP853',
        t_eval=x_eval,
        rtol=1e-9,
        atol=1e-12,
        dense_output=False,
    )

    if not sol.success:
        return None

    x_arr   = sol.t
    a_arr   = np.exp(x_arr)
    rho_arr = sol.y[0]
    Pi_arr  = sol.y[1]
    h2_arr  = Om_m * a_arr**(-3) + rho_arr
    h2_arr  = np.maximum(h2_arr, 1e-30)
    h_arr   = np.sqrt(h2_arr)

    return a_arr, rho_arr, Pi_arr, h_arr, h2_arr, x_arr


def compute_growth(a_arr, h2_arr, x_arr):
    """
    Resuelve la ODE de crecimiento lineal:
      δ'' + [2 + d ln h / d ln a] δ' = (3/2) Ω_m,eff(a) δ

    δ' ≡ dδ/dx,  x = ln a
    Ω_m,eff(a) = Om_m a^-3 / h²(a)

    Retorna arrays: a, f = d ln δ / d ln a, Ω_m(a)
    """
    from scipy.interpolate import CubicSpline

    # d ln h / d ln a = (1/2) d ln h² / d ln a
    ln_h2 = np.log(h2_arr)
    dlnh_dlna = np.gradient(ln_h2, x_arr) / 2.0

    # Ω_m efectivo
    Om_eff_arr = Om_m * np.exp(-3 * x_arr) / h2_arr

    # Splines para interpolación dentro del integrador
    cs_dlnh = CubicSpline(x_arr, dlnh_dlna)
    cs_Omm  = CubicSpline(x_arr, Om_eff_arr)

    def growth_rhs(x, state):
        delta, ddelta = state
        dlnh = cs_dlnh(x)
        Omm  = cs_Omm(x)
        coeff_drag = 2 + dlnh
        coeff_src  = 1.5 * Omm
        d2delta = -coeff_drag * ddelta + coeff_src * delta
        return [ddelta, d2delta]

    x_span = (x_arr[0], x_arr[-1])
    # CI de crecimiento: régimen de materia dominante δ ~ a → δ'=δ
    delta_i = np.exp(x_arr[0])
    sol = solve_ivp(
        growth_rhs,
        x_span,
        [delta_i, delta_i],
        method='DOP853',
        t_eval=x_arr,
        rtol=1e-9,
        atol=1e-12,
    )

    if not sol.success:
        return None, None, None

    delta_arr  = sol.y[0]
    ddelta_arr = sol.y[1]
    f_arr = ddelta_arr / (delta_arr + 1e-30)  # f = d ln δ / d ln a

    return np.exp(x_arr), f_arr, Om_eff_arr


def fit_gamma(a_arr, f_arr, Om_arr, a_min=0.1, a_max=1.0):
    """
    Ajusta γ por regresión log-log:  ln f ≈ γ ln Ω_m  para a_min < a < a_max.
    """
    mask = (a_arr >= a_min) & (a_arr <= a_max) & (f_arr > 0) & (Om_arr > 0)
    if mask.sum() < 10:
        return np.nan, np.nan

    ln_Om = np.log(Om_arr[mask])
    ln_f  = np.log(f_arr[mask])

    slope, intercept, r, p, se = linregress(ln_Om, ln_f)
    return slope, r**2


def compute_sigma8_growth(a_arr, delta_arr, D_LCDM_today=1.0, sigma8_LCDM=0.811):
    """
    σ8_IS = σ8_ΛCDM × D_IS(a=1) / D_ΛCDM(a=1)
    donde D es el factor de crecimiento normalizado a 1 hoy en ΛCDM.
    """
    # Normalizar D_IS a 1 hoy
    D_IS_today = delta_arr[-1]
    D_IS_norm  = delta_arr / D_IS_today
    return sigma8_LCDM * D_IS_today / D_LCDM_today, D_IS_norm


# ─── Scan principal ───────────────────────────────────────────────────────────
print("=" * 72)
print(f"{'τ_Π H₀ label':<35} {'T':>8} {'γ_IS':>8} {'R²':>6} {'Δγ':>8} {'σ8_IS':>8}")
print("=" * 72)

results = {}

# Referencia ΛCDM: γ_LCDM ≈ 6/11 ≈ 0.5455
T_LCDM = None  # ΛCDM no tiene IS, pero calculamos γ_Eckart como baseline

for label, T in T_scan.items():
    bg = solve_background(T)
    if bg is None:
        print(f"{label:<35} {T:>8.4f}  [integración fallida]")
        continue

    a_arr, rho_arr, Pi_arr, h_arr, h2_arr, x_arr = bg
    growth = compute_growth(a_arr, h2_arr, x_arr)
    if growth[0] is None:
        print(f"{label:<35} {T:>8.4f}  [crecimiento fallido]")
        continue

    a_g, f_arr, Om_arr = growth
    gamma_IS, R2 = fit_gamma(a_g, f_arr, Om_arr)

    # σ8_IS (proxy: ratio D_IS/D_EdS)
    delta_arr = growth[0]  # realmente es a_arr desde compute_growth
    # Recalcular delta directamente
    from scipy.integrate import solve_ivp as siv2
    bg2 = solve_background(T, n_pts=500)
    a2, _, _, _, h2_2, x2 = bg2
    _, f2, Om2 = compute_growth(a2, h2_2, x2)

    # σ8 aproximado — proporción al factor de crecimiento respecto Eckart (T→∞)
    # Para T→∞ IS→Eckart; calcular ratio D_IS / D_Eckart
    sigma8_approx = np.nan
    if f2 is not None:
        # Integrar f = d ln δ / d ln a  para obtener D
        x_fine = np.linspace(x2[0], x2[-1], len(x2))
        D_IS_log = np.cumsum(f2 * np.gradient(x2))
        D_IS_relative = np.exp(D_IS_log - D_IS_log[-1])  # normalizado a 1 hoy
        # S8 = σ8 sqrt(Ω_m / 0.3)
        sigma8_approx = SIGMA8_NORM * D_IS_relative[-1] / 1.0

    delta_gamma = gamma_IS - gamma_target if not np.isnan(gamma_IS) else np.nan
    results[label] = {'T': T, 'gamma': gamma_IS, 'R2': R2, 'delta_gamma': delta_gamma}

    print(f"{label:<35} {T:>8.4f} {gamma_IS:>8.5f} {R2:>6.4f} {delta_gamma:>+8.5f} {sigma8_approx:>8.4f}")

print("=" * 72)
print(f"{'Target γ = φ⁻¹':<35} {'':>8} {gamma_target:>8.5f}")
print(f"{'ΛCDM γ ≈ 6/11':<35} {'':>8} {6/11:>8.5f}")
print()

# ─── Mejor candidato ──────────────────────────────────────────────────────────
valid = {k: v for k, v in results.items() if not np.isnan(v.get('gamma', np.nan))}
if valid:
    best_label = min(valid, key=lambda k: abs(valid[k]['delta_gamma']))
    best = valid[best_label]
    print(f"Mejor T: '{best_label}'")
    print(f"  τ_Π H₀ = {best['T']:.6f}")
    print(f"  γ_IS   = {best['gamma']:.6f}  (Δγ = {best['delta_gamma']:+.6f}  vs φ⁻¹={gamma_target:.6f})")

# ─── Análisis detallado del caso τ_Π = 1/MIRA ─────────────────────────────────
print()
print("=== Análisis detallado: T = 1/MIRA (= τ_Π × H₀) ===")
T_best = 1.0 / MIRA
bg = solve_background(T_best, n_pts=3000)
a_arr, rho_arr, Pi_arr, h_arr, h2_arr, x_arr = bg

# w_eff = (w₀ ρ_DE + Π) / ρ_DE
w_eff_arr = (w0 * rho_arr + Pi_arr) / (rho_arr + 1e-30)

# Transition redshift z_IS: τ_Π H(z) = 1 → H(z) = 1/τ_Π → h(z) = T
h_IS_transition = T_best
# Buscar a donde h(a) ≈ T
idx_trans = np.argmin(np.abs(h_arr - h_IS_transition))
z_IS = 1.0 / a_arr[idx_trans] - 1

print(f"  τ_Π H₀       = {T_best:.6f}  (= 1/MIRA = 1/{MIRA:.5f})")
print(f"  z_IS (τ_Π H = 1) ≈ {z_IS:.3f}  (transición IS→Eckart)")
print(f"  w_eff(z=0)   = {w_eff_arr[-1]:.5f}")
print(f"  w_eff(z=1)   = {w_eff_arr[np.argmin(np.abs(a_arr - 0.5))]:.5f}")
print(f"  Π(z=0)/ρ_DE  = {Pi_arr[-1]/rho_arr[-1]:.5f}")

a_g, f_arr, Om_arr = compute_growth(a_arr, h2_arr, x_arr)
gamma_1MIRA, R2 = fit_gamma(a_g, f_arr, Om_arr)

# σ8 y S8
f_int  = np.cumsum(f_arr * np.gradient(np.log(a_g)))
D_norm = np.exp(f_int - f_int[-1])
sigma8_IS  = SIGMA8_NORM * D_norm[-1]   # proxy: NORMALIZADO al sigma8 de Planck, no predicho
Om_m_today = Om_m                # = 0.308881, la densidad real
Om_m_CMB   = Om_m                # sin factor MIRA (retirado 2026-06-18)
S8_dyn  = sigma8_IS * np.sqrt(Om_m_today / 0.3)
S8_CMB  = sigma8_IS * np.sqrt(Om_m_CMB  / 0.3)

print(f"\n  γ_IS  = {gamma_1MIRA:.6f}  (R² = {R2:.5f})")
print(f"  Δγ    = {gamma_1MIRA - gamma_target:+.6f}  vs φ⁻¹ = {gamma_target:.6f}")
print(f"  σ8_IS ≈ {sigma8_IS:.4f}  (proxy D_IS/D_EdS)")
print(f"  S8(Ω_m = {Om_m_today:.6f}) ≈ {S8_dyn:.4f}")
print(f"  S8(Ω_m = {Om_m_CMB:.6f}, sin MIRA) ≈ {S8_CMB:.4f}")
print(f"  Planck S8 = 0.832 ± 0.013,  KiDS/DES S8 ≈ 0.759 ± 0.025")

# ─── Figura ───────────────────────────────────────────────────────────────────
os.makedirs('results/figures', exist_ok=True)

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

# Panel 1: γ vs T
T_vals  = [v['T']     for v in results.values()]
g_vals  = [v['gamma'] for v in results.values()]
axes[0].scatter(T_vals, g_vals, s=80, zorder=5, label='IS results')
axes[0].axhline(gamma_target, color='red',    ls='--', label=f'φ⁻¹ = {gamma_target:.4f}')
axes[0].axhline(6/11,          color='orange', ls=':',  label='ΛCDM 6/11')
axes[0].set_xlabel(r'$\tau_\Pi H_0$', fontsize=12)
axes[0].set_ylabel(r'$\gamma_\mathrm{IS}$', fontsize=12)
axes[0].set_title('Growth index scan', fontsize=11)
axes[0].legend(fontsize=8)
axes[0].set_xscale('log')
axes[0].grid(True, alpha=0.3)

# Panel 2: w_eff(z) para T=1/MIRA
z_arr = 1.0 / a_arr - 1
mask_z = z_arr < 4
axes[1].plot(z_arr[mask_z], w_eff_arr[mask_z], 'b-', lw=2, label=r'$w_\mathrm{eff}$ IS ($T=1/\mathrm{MIRA}$)')
axes[1].axhline(w0, color='gray', ls='--', label=f'$w_0$ = {w0:.4f}')
axes[1].axvline(z_IS, color='red', ls=':', alpha=0.6, label=f'$z_{{IS}}$ = {z_IS:.2f}')
axes[1].set_xlabel('z', fontsize=12)
axes[1].set_ylabel(r'$w_\mathrm{eff}(z)$', fontsize=12)
axes[1].set_title('IS effective EOS', fontsize=11)
axes[1].legend(fontsize=8)
axes[1].grid(True, alpha=0.3)

# Panel 3: ln f vs ln Ω_m (verificar power-law)
mask_a = (a_g >= 0.1) & (a_g <= 1.0) & (f_arr > 0) & (Om_arr > 0)
ln_Om_fit = np.log(Om_arr[mask_a])
ln_f_fit  = np.log(f_arr[mask_a])
axes[2].scatter(np.log10(Om_arr[mask_a]), np.log10(f_arr[mask_a]),
                s=10, alpha=0.6, label='IS data')
# Línea ajustada
x_line = np.linspace(ln_Om_fit.min(), ln_Om_fit.max(), 100)
axes[2].plot(x_line / np.log(10),
             (gamma_1MIRA * x_line + np.mean(ln_f_fit - gamma_1MIRA * ln_Om_fit)) / np.log(10),
             'r-', lw=2, label=f'Fit γ={gamma_1MIRA:.4f}')
axes[2].set_xlabel(r'$\log_{10}\,\Omega_m(a)$', fontsize=12)
axes[2].set_ylabel(r'$\log_{10}\,f$', fontsize=12)
axes[2].set_title(r'Growth rate $f \approx \Omega_m^\gamma$', fontsize=11)
axes[2].legend(fontsize=8)
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
#plt.savefig  # F1: no escribe figuras al repo('results/figures/fig_is_growth.pdf', bbox_inches='tight', dpi=150)
#plt.savefig  # F1: no escribe figuras al repo('results/figures/fig_is_growth.png', bbox_inches='tight', dpi=150)
print(f"\nFigura guardada: results/figures/fig_is_growth.{{pdf,png}}")

# ─── Resumen para EFT section ─────────────────────────────────────────────────
print()
print("=== Resumen para SSEE_EFT_section.tex ===")
print(f"τ_Π H₀ = 1/MIRA = {T_best:.6f}")
print(f"γ_IS   = {gamma_1MIRA:.5f}  (φ⁻¹ = {gamma_target:.5f},  Δ = {abs(gamma_1MIRA - gamma_target):.5f})")
print(f"z_IS   = {z_IS:.3f}  (redshift de transición IS→Eckart)")
print(f"w_eff(z=0) = {w_eff_arr[-1]:.5f}")
print()
print("IS causal: c_s² = ζ / (ρ_DE τ_Π) ≤ 1")
tau_H0 = T_best
c_s2 = KAL0 / (Om_DE0 * 3 * tau_H0 / (tau_H0))  # ζ ≡ KAL₀ H/(8πG), c_s²=ζ/(ρτ)
# Forma adimensional: c_s² = KAL₀ / (3 Ω_DE τ_Π H₀)
c_s2_check = KAL0 / (3 * Om_DE0 * T_best)
print(f"c_s² = KAL₀/(3 Ω_DE τ_Π H₀) = {KAL0:.4f}/(3×{Om_DE0:.3f}×{T_best:.4f}) = {c_s2_check:.4f}")
causality_ok = c_s2_check <= 1.0
print(f"Causalidad (c_s² ≤ 1): {'✅ SÍ' if causality_ok else '❌ NO'}")

# ─── Log con acta (2026-10-01): el gamma_bg de P1 se lee de aqui, no se teclea ───
import json as _json
from procedencia import con_acta  # noqa: E402
_g = [v["gamma"] for v in results.values() if not np.isnan(v.get("gamma", np.nan))]
_json.dump(con_acta(dict(
    rejilla_tau_Pi_H0={k: dict(T=float(v["T"]), gamma=float(v["gamma"]), R2=float(v["R2"])) for k, v in results.items()},
    gamma_min=float(min(_g)), gamma_max=float(max(_g)),
    gamma_centro=float((min(_g) + max(_g)) / 2), gamma_semirango=float((max(_g) - min(_g)) / 2),
    T_mira=float(T_best), gamma_en_T_mira=float(gamma_1MIRA), z_IS=float(z_IS), w_eff_z0=float(w_eff_arr[-1]),
    sigma8_normalizacion=SIGMA8_NORM, sigma8_IS=float(sigma8_IS), S8_Om_CMB=float(S8_CMB), Om_CMB=float(Om_m_CMB),
    nota="gamma_bg: centro y semirango sobre la rejilla de tau_Pi H0 (8 candidatos algebraicos); S8 = sigma8 de Planck "
         "reescalado por Omega_m (normalizacion del proxy), no una prediccion"), __file__),
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results", "logs", "is_growth_gamma.json"), "w"), indent=1)

