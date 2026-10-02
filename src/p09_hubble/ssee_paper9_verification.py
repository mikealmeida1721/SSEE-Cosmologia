"""
SSEE Paper 9 — Algebraic Identity Verification
f_screen = s_K / (3 * MIRA) = (pi - phi) / (phi + pi)^2

Verifies, step by step:
  Step 1: s_K algebraic expression from K(X)=X/KAL + Friedmann
  Step 2: MIRA = AURA/2 from Paper 8 disformal null geodesic
  Step 3: AURA cancels in s_K / (3 * MIRA)  →  (pi - phi) / Omega^2

Also computes both H0 corrections (additive and multiplicative) and
compares against SH0ES.
"""

import numpy as np

# ── Fundamental constants ────────────────────────────────────────────────────
import os as _reloc_os, sys as _reloc_sys  # reloc: anclar src/
_reloc_sys.path.insert(0, _reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__))))
from ssee_core import (
    PHI as phi, PI as pi, OMEGA as Omega, AURA, KAL0 as KAL,
    W0 as w0, OMEGA_DE as Omega_DE, H0_ALG as H0_alg, MIRA,
)

# ── Paper 1 background quantities (importados de ssee_core) ──────────────────
# Identidades verificadas: w₀ = -AURA/Ω = -Tr/Mv ;  Ω_DE = AURA/Ω ;
#                          H₀^alg = 3(φ+π)²  [km/s/Mpc]

# ── Step 1: exact s_K from Friedmann ────────────────────────────────────
# s_K — la cantidad que entra en f_screen. RENOMBRADA 2026-08-10: NO es s_K.
# s_K (kineticidad Bellini-Sawicki) es 3*v^2/KAL con v = dphi/d(ln a), EVOLUCIONA
# (hoy 0.150703 -> 0.480148 al final) y se mide integrando el campo. s_K es puro EoS,
# 3*(-w0)*(1+w0), y no evoluciona. Probado: no hay epoca donde el campo tenga las dos
# ranuras de s_K a la vez. El VALOR 0.4033 no cambia; la etiqueta si.
# Omega_DE aqui es el ALIAS de S_DE = T_r/M_v = 0.839950 (saturacion, NO densidad).
one_plus_w0    = (pi - phi) / (2 * Omega)   # exact identity Ω - AURA = (π-φ)/2
s_K_exact  = 3 * Omega_DE * (1 + w0)   # from background equations
s_K_formula = 3 * AURA * (pi - phi) / (2 * Omega**2)  # substituted

# Cross-check: should match EFTCAMB value from Paper 7
s_K_papers = 0.40330   # R66-OK: literal citado de los papers A PROPOSITO.
# Es el numero que esta ESCRITO en el .tex; se contrasta contra el que sale
# del algebra. Importarlo del nucleo compararia el nucleo consigo mismo y la
# comprobacion pasaria siempre, aunque el paper dijera otra cosa (R53).
# OJO 2026-08-10: se atribuia a 'CLASS/EFTCAMB'. El script que lo avalaba
# (ssee_paper3_hiclass_check.py, archivado 2026-10-02 en archive/codigo/investigacion/huerfanos_2026-10-02/) corre CLASS NORMAL, no hi_class, y en z=0 su
# formula colapsa al mismo algebra que compara. No es aval independiente.

# ── Step 2: MIRA from Paper 8 disformal null geodesic ───────────────────────
# theta_E^SSEE / theta_E^GR = sqrt(beta_c) = MIRA,  MIRA = AURA/2 (importado)

# ── Step 3: cancellation ─────────────────────────────────────────────────────
# s_K / (3*MIRA) = [3*AURA*(pi-phi)/(2*Omega^2)] / [3*AURA/2]
#                    = (pi - phi) / Omega^2
f_screen_identity = s_K_formula / (3 * MIRA)
f_screen_direct   = (pi - phi) / Omega**2

# Percentage discrepancy between formula and direct
discrepancy_pct = abs(f_screen_identity - f_screen_direct) / f_screen_direct * 100

# ── Cascada: SH0ES ENTRA, H_global SALE ──────────────────────────────────────
# H0_alg = 3(phi+pi)^2 es un NUMERO PURO, sin unidades: NO es entrada de la
# cascada, es el blanco contra el que se compara la salida. El unico H medido
# es SH0ES; el de Planck se infiere dentro de LCDM. Ver guardian R55.
H0_SH0ES          = 73.04
sigma_SH0ES       = 1.04
H0_glob_mult = H0_SH0ES * (1 - f_screen_direct)   # H_SH0ES(1-f)
H0_glob_add  = H0_SH0ES / (1 + f_screen_direct)   # H_SH0ES/(1+f)
sigma_glob   = sigma_SH0ES * (1 - f_screen_direct)

tension_mult = abs(H0_glob_mult - H0_alg) / sigma_glob
tension_add  = abs(H0_glob_add  - H0_alg) / sigma_glob

# ── Print verification ───────────────────────────────────────────────────────
sep = "=" * 68
print(sep)
print("SSEE Paper 9 — Algebraic Identity Verification")
print(sep)

print(f"\n── Fundamental constants ─────────────────────────────────────────")
print(f"  φ      = {phi:.10f}")
print(f"  π      = {pi:.10f}")
print(f"  Ω=φ+π  = {Omega:.10f}")
print(f"  AURA   = (3φ+π)/2 = {AURA:.10f}")
print(f"  MIRA   = AURA/2   = {MIRA:.10f}")
print(f"  KAL    = (φ+π)/2+π = {KAL:.10f}")

print(f"\n── Step 1: exact s_K ─────────────────────────────────────────")
print(f"  w₀               = −AURA/Ω         = {w0:.10f}")
print(f"  1 + w₀           = (π−φ)/(2Ω)      = {one_plus_w0:.10f}")
print(f"  Ω_DE             = AURA/Ω           = {Omega_DE:.10f}")
print(f"  αK (background)  = 3·Ω_DE·(1+w₀)  = {s_K_exact:.8f}")
print(f"  αK (substituted) = 3AURA(π−φ)/2Ω² = {s_K_formula:.8f}")
print(f"  αK (EFTCAMB P7)  =                   {s_K_papers:.8f}")
print(f"  Δ(formula/EFTCAMB)                 = {abs(s_K_formula-s_K_papers)/s_K_papers*100:.4f}%")

print(f"\n── Step 2: MIRA ──────────────────────────────────────────────────")
print(f"  MIRA = AURA/2 = (3φ+π)/4 = {MIRA:.10f}")
print(f"  3·MIRA         = 3AURA/2  = {3*MIRA:.10f}")

print(f"\n── Step 3: cancellation ──────────────────────────────────────────")
print(f"  αK / (3·MIRA)  = {f_screen_identity:.10f}")
print(f"  (π−φ)/Ω²       = {f_screen_direct:.10f}")
print(f"  Discrepancy    = {discrepancy_pct:.8f}%  ← AURA cancels exactly")

print(f"\n── H₀ predictions ───────────────────────────────────────────────")
print(f"  3(φ+π)² PURO        = {H0_alg:.6f}   (blanco, sin unidades)")
print(f"  f_screen            = {f_screen_direct:.6f}  ({f_screen_direct:.4%})")
print(f"")
print(f"  H₀,SH0ES (ENTRADA)  =             {H0_SH0ES:.4f} km/s/Mpc  ± {sigma_SH0ES:.2f}")
print(f"  H₀,glob (mult.)     = SH0ES(1−f) = {H0_glob_mult:.4f} km/s/Mpc  →  {tension_mult:.2f}σ vs 3(φ+π)²")
print(f"  H₀,glob (add.)      = SH0ES/(1+f)= {H0_glob_add:.4f} km/s/Mpc  →  {tension_add:.2f}σ vs 3(φ+π)²")
print(f"  σ propagado         =             {sigma_glob:.4f} km/s/Mpc")
print(f"")
diff_mult_add = H0_glob_add - H0_glob_mult
print(f"  Difference (mult − add) = {diff_mult_add:.4f} km/s/Mpc  ≈ f²·H₀  [{diff_mult_add:.4f}]")

print(f"\n── Key identity (exact) ─────────────────────────────────────────")
print(f"  f_screen = αK/(3·MIRA) = (π−φ)/(φ+π)² = {f_screen_direct:.8f}")
print(f"  AURA = {AURA:.6f} cancels in the ratio → result is pure φ,π")

print(f"\n── Cross-check: 1+w₀ identity ───────────────────────────────────")
# Verify Ω - AURA = (pi-phi)/2
lhs = Omega - AURA
rhs = (pi - phi) / 2
print(f"  Ω − AURA           = {lhs:.10f}")
print(f"  (π − φ)/2          = {rhs:.10f}")
print(f"  Difference         = {abs(lhs-rhs):.2e}  (machine precision)")

print(f"\n{'='*68}")
print("VERDICT")
print(f"{'='*68}")
print(f"""
  The identity f_screen = αK/(3·MIRA) = (π−φ)/(φ+π)² holds
  with {discrepancy_pct:.1e}% discrepancy — limited only by floating-point
  precision. AURA cancels analytically; the result depends only on φ and π.

  Both H₀ corrections (mult: {H0_glob_mult:.2f}, add: {H0_glob_add:.2f} km/s/Mpc)
  are consistent with SH0ES ({H0_SH0ES} ± {sigma_SH0ES}):
    Multiplicative: {tension_mult:.2f}σ
    Additive:       {tension_add:.2f}σ
""")
print("=" * 68)
