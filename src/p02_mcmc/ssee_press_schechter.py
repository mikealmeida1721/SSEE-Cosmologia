#!/usr/bin/env python3
"""
Task 2B: Press-Schechter halo mass function — SSEE vs ΛCDM

CORRECCION 2026-09-25 — el delta_c postulado quedo FALSIFICADO (OP-27).
Este script calculaba con  dc_SSEE = dc_EdS * n_s = 1.6284,  postulado del
Paper 4. El colapso esferico top-hat corrido sobre el fondo del PROPIO modelo
(ecuacion no lineal exacta, DE suave — justificada por la friccion viscosa IS
de Paper 5, que crece como k^2, NO por c_s^2=0, que haria lo contrario) da:

    z_c = 0   ->  dc_SSEE = 1.67634   (LCDM 1.67599)
    z_c = 10  ->  dc_SSEE = 1.68647   (LCDM 1.68646)

o sea indistinguible de LCDM. Control: EdS reproduce 3/20 (12pi)^(2/3).
Script: notes/2026-09-25_crecimiento_alto_z/spherical_collapse_deltac.py
ORIGEN: results/logs/deltac_spherical_collapse.json   (de ahi se LEEN, abajo)

CONSECUENCIA, y no es que el efecto se anule — se INVIERTE. Con el delta_c
derivado, SSEE predice MENOS halos masivos tempranos que LCDM, no mas:
0.998 a 3e10 Msol (z=10), 0.892 a 3e12 (z=10), 0.778 a 3e12 (z=15). La causa
no es sigma8 (SSEE 0.8153 > LCDM 0.811) sino D(z): Omega_m menor y fondo CPL
hacen crecer menos hasta z alto.

Este script conserva AMBOS umbrales: el derivado (el que vale) y el postulado
(para poder dibujar de que tamano era la apuesta). USE_POSTULADO lo elige.
"""

import numpy as np
from scipy.integrate import quad
import os as _o66, sys as _s66
_s66.path.insert(0, _o66.path.dirname(_o66.path.dirname(_o66.path.abspath(__file__))))
import ssee_core as _C

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator

# ── SSEE algebraic constants ──────────────────────────────────────────────────
PHI    = (1 + np.sqrt(5)) / 2          # golden ratio ≈ 1.6180
n_s    = 1 - PHI**(-7)                 # spectral index  ≈ 0.96556 (SSEE algebraic)
dc_EdS = (3/20) * (12*np.pi)**(2/3)   # EdS collapse threshold ≈ 1.6865
# ── umbral de colapso: DERIVADO por defecto, postulado sólo para comparar ────
# Los dos delta_c NO se teclean: se LEEN del log del colapso esferico, que es
# su origen. Si ese calculo cambia, este script se entera; un literal no.
#   ORIGEN: results/logs/deltac_spherical_collapse.json
#   lo produce notes/2026-09-25_crecimiento_alto_z/spherical_collapse_deltac.py
import json as _json66
_LOG66 = _o66.path.join(_o66.path.dirname(_o66.path.dirname(_o66.path.dirname(
         _o66.path.abspath(__file__)))), "results", "logs",
         "deltac_spherical_collapse.json")
with open(_LOG66) as _f66:
    _DC66 = _json66.load(_f66)
USE_POSTULADO = False                  # True reproduce la figura vieja (OP-27)
dc_SSEE_POST  = dc_EdS * n_s           # postulado Paper 4 ≈ 1.6284 — FALSIFICADO
dc_SSEE_DERIV = _DC66["deltac_SSEE_zc0"]   # colapso esférico, z_c=0
dc_LCDM       = _DC66["deltac_LCDM_zc0"]   # mismo cálculo, fondo ΛCDM
dc_SSEE = dc_SSEE_POST if USE_POSTULADO else dc_SSEE_DERIV

print(f"n_s       = {n_s:.7f}  (1 − φ⁻⁷, Planck: 0.9649)")
print(f"δc(EdS)   = {dc_EdS:.7f}")
print(f"δc(SSEE)  = {dc_SSEE:.7f}"
      f"   [{'POSTULADO 1.6284 — FALSIFICADO, OP-27' if USE_POSTULADO else 'derivado, colapso esférico'}]")
print(f"δc(ΛCDM)  = {dc_LCDM:.7f}")
print(f"Δδc/δc    = {(dc_LCDM - dc_SSEE)/dc_LCDM*100:.2f}%")

# ── Cosmological parameters ───────────────────────────────────────────────────
# LCDM Parameters (Planck 2018)
H0_L   = 67.36
Omm_L  = 0.3153
OmL_L  = 1 - Omm_L
h_L    = H0_L / 100
sig8_L = 0.811
gamma_L= 0.55

# SSEE Parameters
# ── CORRECCION 2026-09-07 ────────────────────────────────────────────────
# Cuatro valores estaban rancios y el primero era un BUG de categoria:
#
#   Omm_S = 0.1601  ->  0.308881
#       0.160050 es 1+w_0, la ecuacion de estado, NO una densidad. Entra en
#       Friedmann por la presion. Aqui alimentaba D_gamma() como densidad de
#       materia, que es el mismo bug que inflaba chi2_BAO a 726 antes del fix
#       de geometria (2026-07-09). Paper 1 Sec. two_omega_m lo declara
#       imposible: "There is one matter density, Omega_m = omega_m/h^2 =
#       0.308881, entering every observable that requires a matter density".
#
#   H0_S = 66.75  ->  67.962137
#       66.75 era el posterior MCMC con prior Planck-LCDM, superado por el
#       reframe omega_m-directo. El ancla algebraica es 3(phi+pi)^2.
#
#   sig8_S = 0.792  ->  0.7446
#       0.792 venia de la epoca two-sector, RETIRADA el 2026-08-01 (historico,
#       no vigente). Canonico (Registro linea 126):
#       MCMC R3 contra KiDS crudo, sigma_8 = 0.7446 +/- 0.0189.
#
#   gamma_S = 0.657  ->  0.5504
#       Paper 5 mide gamma_IS = 0.5504 +/- 0.0003 (linea 978). El 0.657 no
#       corresponde a ninguna medicion vigente.
H0_S   = _C.H0_GLOBAL
Omm_S  = _C.OMEGA_M_TOTAL
OmDE_S = 1 - Omm_S
w0_S   = -0.8399
wa_S   = -0.6699
h_S    = H0_S / 100
# ── CORRECCION 2026-09-25 ────────────────────────────────────────────────
# sig8_S = 0.7446  ->  0.8153
#     0.7446 era el MCMC R3 contra KiDS-1000 (A_s libre). SUPERADO el
#     2026-09-19 por KiDS-Legacy: la colaboracion recalibro n(z) y el dato
#     subio (los dos releases difieren ENTRE SI a 2.5σ). Canonico vigente
#     (CANONICAL_VALUES.yaml): sigma8_ssee_unif = 0.8153, PREDICCION del
#     modelo unificado con A_s FIJO en el valor del CMB — A_s se paga una
#     vez en el CMB y no se vuelve a cobrar en el crecimiento. Para la
#     pregunta "¿acomoda SSEE halos masivos tempranos?" el ancla correcta
#     es la prediccion propia del modelo, no lo que preferia un dato
#     ya recalibrado. (Con A_s libre en Legacy: 0.8075 ± 0.0160.)
sig8_S = 0.8153  # prediccion unificada, A_s fijado al CMB (canonico)
gamma_S= 0.5504  # gamma_IS medido en Paper 5

# ── Linear growth factor D(z) — IS and LCDM integrations ──────────────────────
def D_gamma(z, gamma, Omm, OmDE, w0, wa):
    """Computes growth factor normalized to 1 at z=0 using f = Om(a)^gamma."""
    def E2(zp):
        if OmDE == 0:
            return Omm*(1+zp)**3 + (1-Omm)
        return Omm*(1+zp)**3 + OmDE*(1+zp)**(3*(1+w0+wa))*np.exp(-3*wa*zp/(1+zp))
    
    def Om_z(zp):
        return Omm*(1+zp)**3 / E2(zp)
        
    def integrand(zp):
        return Om_z(zp)**gamma / (1+zp)
        
    val = quad(integrand, 0, z)[0]
    return np.exp(-val)

# Growth factors at key redshifts
z_vals = [0, 5, 6, 7, 8, 9, 10, 12, 15]
Dz_L = {z: D_gamma(z, gamma_L, Omm_L, 0, -1, 0) for z in z_vals}
Dz_S = {z: D_gamma(z, gamma_S, Omm_S, OmDE_S, w0_S, wa_S) for z in z_vals}

print("\nLinear growth factors D(z)/D(0):")
print(f"  z       ΛCDM        SSEE")
for z in [0, 5, 8, 10, 12, 15]:
    print(f"  {z:2d}    {Dz_L[z]:.5f}    {Dz_S[z]:.5f}")

# ── σ_M(M, z=0) via power-law fit ─────────────────────────────────────────────
# We compute M8_L to anchor the power law.
rho_crit0_L = 2.775e11 * h_L**2     # M☉/Mpc³
rho_m0_L    = Omm_L * rho_crit0_L
M8_L        = (4*np.pi/3) * rho_m0_L * (8/h_L)**3  # ≈ 2.8e14 M☉
alpha       = 0.30                 # effective slope d ln σ / d ln M^{-1}

# For a fair comparison at the SAME physical mass M, we anchor both 
# to their respective sigma8 and M8. 
rho_crit0_S = 2.775e11 * h_S**2
rho_m0_S    = Omm_S * rho_crit0_S
M8_S        = (4*np.pi/3) * rho_m0_S * (8/h_S)**3  

def sigma_M_z0_L(M): return sig8_L * (M / M8_L)**(-alpha)
def sigma_M_z0_S(M): return sig8_S * (M / M8_S)**(-alpha)

def sigma_Mz_L(M, z): return sigma_M_z0_L(M) * Dz_L[z]
def sigma_Mz_S(M, z): return sigma_M_z0_S(M) * Dz_S[z]

print(f"\nM_8 (ΛCDM) = {M8_L:.3e} M☉  (σ_8 = {sig8_L})")
print(f"M_8 (SSEE) = {M8_S:.3e} M☉  (σ_8 = {sig8_S})")

# ── Press-Schechter ratio n_SSEE / n_ΛCDM ────────────────────────────────────
def ps_ratio(M, z):
    """n_SSEE(M,z) / n_ΛCDM(M,z) at true SSEE/LCDM variances."""
    sig_s = sigma_Mz_S(M, z)
    sig_l = sigma_Mz_L(M, z)
    nu_s = dc_SSEE / sig_s
    nu_l = dc_LCDM / sig_l
    return (nu_s / nu_l) * np.exp(-(nu_s**2 - nu_l**2) / 2)

# ── Exceedance probability ratio P(δ > δc) ────────────────────────────────────
from scipy.special import erfc

def exceedance_ratio(M, z):
    sig_s = sigma_Mz_S(M, z)
    sig_l = sigma_Mz_L(M, z)
    P_ssee = 0.5 * erfc(dc_SSEE / (np.sqrt(2) * sig_s))
    P_lcdm = 0.5 * erfc(dc_LCDM / (np.sqrt(2) * sig_l))
    return P_ssee / P_lcdm

# ── Mass table at z=10 ────────────────────────────────────────────────────────
masses = [3e10, 1e11, 3e11, 1e12, 3e12]
z_table = 10

print(f"\n{'='*82}")
print(f"Press-Schechter enhancement at z={z_table}")
print(f"{'M [M☉]':>12}  {'σ_M,ΛCDM':>10}  {'σ_M,SSEE':>10}  {'PS ratio':>10}  {'P-ratio':>10}")
print(f"{'-'*82}")
for M in masses:
    sig_l = sigma_Mz_L(M, z_table)
    sig_s = sigma_Mz_S(M, z_table)
    r     = ps_ratio(M, z_table)
    pe    = exceedance_ratio(M, z_table)
    print(f"{M:12.2e}  {sig_l:10.4f}  {sig_s:10.4f}  {r:10.3f}  {pe:10.3f}")
print(f"{'='*82}")

# ── Compare with JWST tension ─────────────────────────────────────────────────
print("\nJWST context (Boylan-Kolchin 2023, Nature Astronomy 7, 728):")
print("  ΛCDM deficit at M>10^10.8 M☉, z~10: ~10–100× in number density")
sig_l_jwst = sigma_Mz_L(10**10.8, z_table)
sig_s_jwst = sigma_Mz_S(10**10.8, z_table)
r_jwst   = ps_ratio(10**10.8, z_table)
print(f"  M = 10^10.8 M☉: σ_M,ΛCDM = {sig_l_jwst:.3f}, σ_M,SSEE = {sig_s_jwst:.3f}")
print(f"  n_SSEE/n_ΛCDM = {r_jwst:.2f}×")

# ── Compact table for Paper 4 (LaTeX-ready) ───────────────────────────────────
print("\nLaTeX table rows:")
tex_masses = [1e11, 3e11, 1e12]
tex_labels = [r"10^{11}", r"3\times10^{11}", r"10^{12}"]
for M, lab in zip(tex_masses, tex_labels):
    sig_l = sigma_Mz_L(M, z_table)
    sig_s = sigma_Mz_S(M, z_table)
    r   = ps_ratio(M, z_table)
    print(f"  ${lab}$ & ${sig_l:.3f}$ & ${sig_s:.3f}$ & ${r:.2f}$ \\\\")

# ── Figure ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# Panel A: ratio vs sigma_M_LCDM (to show enhancement as a function of the standard variance)
sigma_l_arr = np.linspace(0.15, 1.0, 300)
# To plot against sig_l, we need to map sig_l to sig_s. 
# sig_s / sig_l is independent of M at fixed z.
R_sig = Dz_S[z_table] / Dz_L[z_table] * (sig8_S / sig8_L) * (M8_S / M8_L)**alpha
ratio_arr = []
exceedance_arr = []
for sig_l in sigma_l_arr:
    sig_s = sig_l * R_sig
    nu_s = dc_SSEE / sig_s
    nu_l = dc_LCDM / sig_l
    ratio_arr.append((nu_s / nu_l) * np.exp(-(nu_s**2 - nu_l**2) / 2))
    
    P_ssee = 0.5 * erfc(dc_SSEE / (np.sqrt(2) * sig_s))
    P_lcdm = 0.5 * erfc(dc_LCDM / (np.sqrt(2) * sig_l))
    exceedance_arr.append(P_ssee / P_lcdm)

ax = axes[0]
ax.plot(sigma_l_arr, ratio_arr,     'b-',  lw=2.0, label=r'PS ratio $n_{\rm SSEE}/n_{\Lambda{\rm CDM}}$')
ax.plot(sigma_l_arr, exceedance_arr,'b--', lw=1.5, label=r'Exceedance ratio $P_{\rm SSEE}/P_{\Lambda{\rm CDM}}$')
ax.axhline(1, color='k', ls=':', lw=0.8)
ax.axvspan(0.3, 0.65, alpha=0.12, color='orange', label=r'JWST regime ($z\sim10$)')

# Mark representative points
for M, lab in [(1e11, r'$10^{11}\,M_\odot$'), (3e11, r'$3\times10^{11}\,M_\odot$'), (1e12, r'$10^{12}\,M_\odot$')]:
    sig_l = sigma_Mz_L(M, z_table)
    r   = ps_ratio(M, z_table)
    ax.plot(sig_l, r, 'o', color='darkorange', ms=5, zorder=5)
    ax.annotate(lab, (sig_l, r), xytext=(sig_l+0.02, r+0.05), fontsize=7.5)

ax.set_xlabel(r'$\sigma_{M}^{\Lambda{\rm CDM}}$ (at $z=10$)', fontsize=12)
ax.set_ylabel(r'Halo-count enhancement', fontsize=12)
ax.set_title(rf'$\delta_c^{{\rm SSEE}}={dc_SSEE:.5f}$ vs $\delta_c^{{\Lambda{{\rm CDM}}}}={dc_LCDM:.5f}$'
             + ('  (postulado, OP-27)' if USE_POSTULADO else '  (derivado)'), fontsize=11)
ax.set_ylim(0.7, 5.5) if USE_POSTULADO else ax.set_ylim(0.70, 1.10)
ax.legend(fontsize=8.5, loc='upper right')
ax.grid(True, alpha=0.3)

# Panel B: ratio vs z at fixed masses
ax2 = axes[1]
colors = ['blue', 'green', 'darkorange']
mass_labels = [r'$M=10^{11}\,M_\odot$', r'$M=3\times10^{11}\,M_\odot$', r'$M=10^{12}\,M_\odot$']
plot_z_vals = [5, 6, 7, 8, 9, 10, 12, 15]

for M, col, lab in zip([1e11, 3e11, 1e12], colors, mass_labels):
    ratios_z = [ps_ratio(M, z) for z in plot_z_vals]
    ax2.plot(plot_z_vals, ratios_z, '-o', color=col, ms=4, label=lab)

ax2.axhline(1, color='k', ls=':', lw=0.8)
ax2.set_xlabel(r'Redshift $z$', fontsize=12)
ax2.set_ylabel(r'$n_{\rm SSEE}/n_{\Lambda{\rm CDM}}$', fontsize=12)
ax2.set_title(r'Enhancement vs redshift', fontsize=11)
ax2.legend(fontsize=8.5)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
outpath = 'results/figures/fig_press_schechter.pdf'
plt.savefig(outpath, dpi=150, bbox_inches='tight')
plt.savefig(outpath.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
print(f"\nFigure → {outpath}")
print("Done.")
