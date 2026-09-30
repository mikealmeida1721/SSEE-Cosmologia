"""
SSEE Paper 10 — UV Completion Verification
M⁴ = 45α² × ρ_crit = 5φ⁸ × ρ_crit

Verifies, step by step:
  Step 1: Algebraic identity 45α² = 5φ⁸  (α = φ⁴/3, Paper 1 α-attractor)
  Step 2: Self-consistent X_bg from full K(X) = X/KAL + X²/M⁴
  Step 3: s_K_full from Bellini-Sawicki with K_X and K_XX contributions
  Step 4: f_screen_full = s_K_full / (3·MIRA)  →  H₀,local

The UV ladder:
  φ  →  α = φ⁴/3  →  M⁴ = 45α² ρ_crit = 5φ⁸ ρ_crit
  →  s_K_full = 0.41691  →  f_screen = 0.06952
  →  H₀,glob CANÓNICO = SH0ES·(1−f_UV) = 67.962142 km/s/Mpc
     (residuo +4.2e-06 contra el NÚMERO PURO 3(φ+π)² = 67.96214)
     [corregido 2026-09-19: esta línea decía «H_alg/(1−f_UV) = 73.040», que
      es la cascada AL REVÉS — metía un número sin unidades como entrada de
      una cadena dimensional. La dirección canónica desde el 2026-09-06 es
      SH0ES ENTRA, H_global SALE, y es la que el código ya calculaba en la
      línea 105: el texto contradecía a su propio cálculo.]
"""

import numpy as np

# ── Fundamental constants ────────────────────────────────────────────────────
import os as _reloc_os, sys as _reloc_sys  # reloc: anclar src/
_reloc_sys.path.insert(0, _reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__))))
from ssee_core import (
    PHI as phi, PI as pi, OMEGA as Omega, AURA, KAL0 as KAL, MIRA,
    W0 as w0, OMEGA_DE as Omega_DE, H0_ALG as H0_alg,
)
# Identidades: w₀ = -AURA/Ω = -Tr/Mv ;  Ω_DE = AURA/Ω ;  H₀^alg = 3(φ+π)²

# ── Physical anchor: the ONE critical density ρ_crit of the model ─────────────
# ρ_crit = 3 H₀² M_Pl²  (reduced Planck mass). There is a SINGLE critical density
# in SSEE; it enters every dimensionful quantity (X_bg, M⁴, ρ_DE) as a common
# scale and cancels exactly in s_K, f_screen and the H₀ boost (all of these are
# ratios). We pin ρ_crit to its canonical model value so X_bg and M⁴ carry real
# meV⁴ units — no implicit ρ_crit = 1 (which would leave them ambiguous to a
# referee even though the observable chain is invariant). Anchor (reframe
# ω_m-directo 2026-06-19): H_alg = 67.962 = global background H = CMB anchor.
H_ANCHOR     = __import__("ssee_core").H0_GLOBAL   # km/s/Mpc — H_glob = SH0ES·(1−f_screen)
M_PL_eV      = 2.435323e27         # reduced Planck mass [eV]
# FIX 2026-08-10: decia 2.1331951e-33 (error relativo 3.54e-5 -> 7.07e-5 en
# rho_crit, que va al cuadrado). DERIVADO, no copiado:
#   hbar = 6.582119569e-16 eV*s          (CODATA 2018)
#   Mpc  = 3.0856775814913673e22 m       (IAU: 648000/pi UA)
#   100 km/s/Mpc = 1e5/Mpc = 3.240779289444365e-18 1/s
#   x hbar       = 2.133119677986167e-33 eV
# No afecta Omega_m ni Omega_DE (el factor cancela en el cociente); si afecta
# rho_crit en meV^4 y por tanto M = (5 phi^8 rho_crit)^(1/4).
H0_PER_h_eV  = 2.133119677986167e-33   # 100 km/s/Mpc en eV (derivado arriba)
H_ANCHOR_eV  = (H_ANCHOR / 100.0) * H0_PER_h_eV
RHO_CRIT_eV4 = 3.0 * H_ANCHOR_eV**2 * M_PL_eV**2   # eV⁴
RHO          = RHO_CRIT_eV4 * 1e12               # meV⁴ ≈ 36.41  (1 meV⁴ = 1e-12 eV⁴)
RHO_qrt      = RHO**0.25                          # ρ_crit^(1/4) ≈ 2.4564 meV

# ── Step 1: α-attractor parameter and UV identity ────────────────────────────
# α = φ⁴/3 is the curvature of the inflationary Starobinsky-like plateau (Paper 1)
# It predicts r = 12α/N² ≈ 0.00813 for N = 60 e-folds (LiteBIRD 2032 target)
alpha_attr = phi**4 / 3

M4_ratio = 45 * alpha_attr**2     # = 5φ⁸ exactly — the dimensionless M⁴/ρ_crit
M4_UV    = M4_ratio * RHO         # meV⁴ — physical UV cutoff⁴ (= 5φ⁸ ρ_crit)

# Verify algebraic identity
identity = abs(45 * alpha_attr**2 - 5 * phi**8)

# ── Step 2: IR (Paper 9) reference values ────────────────────────────────────
# s_K_IR — RENOMBRADA 2026-08-10: NO es s_K (kineticidad Bellini-Sawicki,
# que es 3*v^2/KAL, evoluciona, hoy 0.150703). s_K es puro EoS y no evoluciona.
# Omega_DE aqui es ALIAS de S_DE = 0.839950 (saturacion, NO densidad).
s_K_IR = 3 * Omega_DE * (1 + w0)          # = 3AURA(π−φ)/(2Ω²)  [dimensionless]
rho_DE_1pw = (s_K_IR / 3) * RHO            # = Ω_DE·(1+w₀)·ρ_crit  [meV⁴]
X_bg_IR    = s_K_IR * KAL / 6 * RHO        # self-consistent X, IR limit  [meV⁴]

# f_screen_IR from Paper 9 (AURA cancels)
f_screen_IR = (pi - phi) / Omega**2            # = s_K_IR / (3·MIRA) exactly

# ── Step 3: self-consistent X_bg from full K(X) = X/KAL + X²/M⁴ ─────────────
# Background EOM:  2X K_X = ρ_DE(1+w₀)
# K_X = 1/KAL + 2X/M⁴  →  quadratic: 4X²/M⁴ + 2X/KAL − ρ_DE(1+w₀) = 0
a = 4.0 / M4_UV
b = 2.0 / KAL
c = -rho_DE_1pw
disc = b**2 - 4*a*c
X_bg_UV = (-b + np.sqrt(disc)) / (2*a)        # physical (positive) root

X_ratio = X_bg_UV / X_bg_IR                   # should be close to 1 for M⁴ >> X²

# ── Step 4: s_K_full (Bellini-Sawicki, full K) ─────────────────────────────────
# s_K = 2(X K_X + 2X² K_XX) / (M²_Pl H²),  with M²_Pl H² = ρ_crit/3.
# Both numerator and denominator scale with ρ_crit → s_K is invariant (anchor-free).
MplH2   = RHO / 3.0                            # M²_Pl H² = ρ_crit/3  [meV⁴]
K_X_UV  = 1.0/KAL + 2*X_bg_UV/M4_UV            # dimensionless (X/M⁴ is a ratio)
K_XX_UV = 2.0/M4_UV                            # meV⁻⁴
s_K_UV = 2 * (X_bg_UV*K_X_UV + 2*X_bg_UV**2*K_XX_UV) / MplH2

UV_correction = s_K_UV / s_K_IR - 1.0  # fractional increase

# ── Step 5: f_screen_full and H₀,local ──────────────────────────────────────
f_screen_UV = s_K_UV / (3 * MIRA)

# Cascada: SH0ES ENTRA, H_global SALE. H0_alg = 3(phi+pi)^2 es un NUMERO PURO
# (sin unidades) y por eso NO puede ser la entrada de una cascada dimensional:
# es el blanco de comparacion. El unico H medido es SH0ES; el de Planck se
# infiere dentro de LCDM. Ver guardian R55.
H0_SH0ES   = 73.04
sigma_SH0ES = 1.04
H0_glob_UV  = H0_SH0ES * (1 - f_screen_UV)
H0_glob_IR  = H0_SH0ES * (1 - f_screen_IR)
sigma_glob  = sigma_SH0ES * (1 - f_screen_UV)
tension_UV  = abs(H0_glob_UV - H0_alg) / sigma_glob
tension_IR  = abs(H0_glob_IR - H0_alg) / sigma_glob

# ── Print verification ────────────────────────────────────────────────────────
sep = "=" * 72
print(sep)
print("SSEE Paper 10 — UV Completion Verification")
print(sep)

print(f"\n── Fundamental constants ────────────────────────────────────────────")
print(f"  φ       = {phi:.10f}")
print(f"  π       = {pi:.10f}")
print(f"  Ω=φ+π   = {Omega:.10f}")
print(f"  AURA    = (3φ+π)/2 = {AURA:.10f}")
print(f"  MIRA    = AURA/2   = {MIRA:.10f}")
print(f"  KAL     = (φ+π)/2+π = {KAL:.10f}")
print(f"  3(φ+π)² = 3Ω² = {H0_alg:.6f}   (número PURO, blanco)")

print(f"\n── Step 1: α-attractor parameter and UV identity ────────────────────")
print(f"  α = φ⁴/3            = {alpha_attr:.10f}   (Paper 1 inflaton curvature)")
print(f"  45α²                = {45*alpha_attr**2:.10f}")
print(f"  5φ⁸                 = {5*phi**8:.10f}")
print(f"  |45α² − 5φ⁸|        = {identity:.3e}   ← exact identity (machine precision)")
print(f"  ρ_crit (canónico)  = {RHO:.4f} meV⁴   [= 3 H_anchor² M_Pl², H_anchor={H_ANCHOR} km/s/Mpc]")
print(f"  ρ_crit^(1/4)       = {RHO_qrt:.6f} meV")
print(f"  M⁴ = 5φ⁸ ρ_crit    = {M4_UV:.4f} meV⁴   (ratio M⁴/ρ_crit = {M4_ratio:.4f})")
print(f"  M = φ²×5^(1/4)×ρ_crit^(1/4) = {M4_UV**0.25:.4f} meV  = Λ_SSEE")
print(f"  M / ρ_crit^(1/4)   = {M4_ratio**0.25:.8f}")
print(f"    φ²×5^(1/4)       = {phi**2 * 5**0.25:.8f}  ← algebraic form ✓")

print(f"\n── Step 2: IR (Paper 9) baseline ────────────────────────────────────")
print(f"  w₀            = −AURA/Ω     = {w0:.8f}")
print(f"  s_K_IR         = 3Ω_DE(1+w₀) = {s_K_IR:.8f}  [Paper 7 + Friedmann]")
print(f"  ρ_DE(1+w₀)    = s_K_IR/3    = {rho_DE_1pw:.8f}")
print(f"  X_bg_IR       = s_K_IR×KAL/6 = {X_bg_IR:.8f}")
print(f"  f_screen_IR   = (π−φ)/Ω²  = {f_screen_IR:.8f}  [AURA cancels exactly]")
print(f"  H₀,glob IR    = {H0_glob_IR:.4f} km/s/Mpc  →  {tension_IR:.2f}σ vs 3(φ+π)²")

print(f"\n── Step 3: self-consistent X_bg with full K(X) ──────────────────────")
print(f"  Quadratic: 4X²/M⁴ + 2X/KAL − ρ_DE(1+w₀) = 0")
print(f"  X_bg_UV          = {X_bg_UV:.8f} meV⁴")
print(f"  X_bg_IR          = {X_bg_IR:.8f} meV⁴")
print(f"  X_UV/X_IR        = {X_ratio:.8f}  (small suppression from UV term)")
print(f"  X_bg_UV/M⁴       = {X_bg_UV/M4_UV:.8f}  ← dimensionless invariant (anchor-free)")
print(f"  ε = X_bg_UV²/M⁴ = {X_bg_UV**2/M4_UV:.4e} meV⁴  (perturbative UV correction)")

print(f"\n── Step 4: s_K_full (Bellini-Sawicki) ───────────────────────────────")
print(f"  K_X  = 1/KAL + 2X/M⁴ = {K_X_UV:.10f}")
print(f"  K_XX = 2/M⁴           = {K_XX_UV:.10f}")
print(f"  s_K_IR (K(X)=X/KAL)    = {s_K_IR:.8f}")
print(f"  s_K_UV (K full)        = {s_K_UV:.8f}")
print(f"  s_K_UV/s_K_IR           = {s_K_UV/s_K_IR:.8f}  (+{UV_correction*100:.2f}%)")
print(f"  Δ s_K = +{(s_K_UV-s_K_IR):.6f}  (UV correction)")

print(f"\n── Step 5: f_screen_full and H₀,local ──────────────────────────────")
print(f"  f_screen_UV = s_K_full/(3·MIRA) = {f_screen_UV:.8f}")
print(f"  f_screen_IR = (π−φ)/Ω²        = {f_screen_IR:.8f}")
print(f"  Δf = +{(f_screen_UV-f_screen_IR):.6f}  (+{(f_screen_UV/f_screen_IR-1)*100:.2f}%)")
print(f"")
print(f"  3(φ+π)² PURO        = {H0_alg:.6f}  (blanco, sin unidades)")
print(f"  SH0ES (ENTRADA)     =              {H0_SH0ES:.4f} km/s/Mpc  ±{sigma_SH0ES:.2f}")
print(f"  H₀,glob IR          = SH0ES(1−f_IR) = {H0_glob_IR:.4f} km/s/Mpc  →  {tension_IR:.2f}σ")
print(f"  H₀,glob UV          = SH0ES(1−f_UV) = {H0_glob_UV:.6f} km/s/Mpc  →  {tension_UV:.2e}σ")
print(f"  residuo UV          = {H0_glob_UV-H0_alg:+.3e} km/s/Mpc   (σ propagado {sigma_glob:.4f})")
print(f"")

# ── UV ladder summary ─────────────────────────────────────────────────────────
print(f"── UV ladder: φ → α → M⁴ → s_K_full → H₀ ────────────────────────────")
print(f"  φ = {phi:.8f}")
print(f"  α = φ⁴/3 = {alpha_attr:.8f}  (inflaton curvature → r=0.00813)")
# ρ_crit^(1/4) = RHO_qrt meV con H_anchor=67.962 km/s/Mpc (H_alg, reframe)
print(f"  M⁴ = 45α² = 5φ⁸ ρ_crit = {M4_UV:.4f} meV⁴  →  M = {M4_UV**0.25:.3f} meV")
print(f"  s_K_full = {s_K_UV:.5f}  (+{UV_correction*100:.2f}% over s_K_IR={s_K_IR:.5f})")
print(f"  f_screen = {f_screen_UV:.5f}")
print(f"  H₀,glob  = {H0_glob_UV:.6f} km/s/Mpc  ← residuo {H0_glob_UV-H0_alg:+.2e} vs 3(φ+π)²")

print(f"\n── Cross-check: AURA cancellation at UV ──────────────────────────────")
# At UV, AURA does NOT cancel in f_screen_full because s_K_full ≠ s_K_IR.
# But the numerical result still rounds to SH0ES.
# The cancellation f_screen_UV = exact function of φ,π would require:
# s_K_full / (3·MIRA) = (π-φ)/Ω² × (1 + UV_corr)
# The UV correction IS a function of AURA through s_K_IR.
AURA_check = s_K_UV / (3 * (pi - phi) / Omega**2)
print(f"  s_K_full / [(π−φ)/Ω²]  = {AURA_check:.8f}  (= 3·MIRA × s_K_full/s_K_full×...)")
print(f"  Effective MIRA needed  = {s_K_UV/(3*f_screen_IR):.8f}  (vs MIRA={MIRA:.8f})")
print(f"  ΔMIRA_eff              = +{s_K_UV/(3*f_screen_IR)-MIRA:.8f}  (UV correction to Paper 8 sector)")

print(f"\n{sep}")
print("VERDICT")
print(f"{sep}")
print(f"""
  Step 1: M⁴ = 5φ⁸ ρ_crit = {M4_UV:.4f} meV⁴  [ratio 5φ⁸={M4_ratio:.4f}, |diff|={identity:.1e}]
  Step 2: X_bg_UV = {X_bg_UV:.6f} meV⁴  (X/M⁴ = {X_bg_UV/M4_UV:.2e} — perturbative ✓)
  Step 3: s_K_full = {s_K_UV:.6f}  = s_K_IR × {s_K_UV/s_K_IR:.6f}  (+{UV_correction*100:.2f}%)
  Step 4: f_screen_UV = {f_screen_UV:.6f}  (+{(f_screen_UV/f_screen_IR-1)*100:.2f}% over Paper 9)

  CANÓNICO (2026-09-06): SH0ES ENTRA, H_global SALE. Blanco 3(φ+π)²={H0_alg:.6f} (PURO):
    IR:  H₀,glob = SH0ES(1−f_IR) = {H0_glob_IR:.4f} km/s/Mpc  ({tension_IR:.2f}σ)  ← titular Paper 9
    UV:  H₀,glob = SH0ES(1−f_UV) = {H0_glob_UV:.6f} km/s/Mpc  (residuo {H0_glob_UV-H0_alg:+.2e})  ← titular Paper 10  [M⁴=5φ⁸]
    σ propagado de SH0ES = {sigma_glob:.4f} km/s/Mpc — DOMINA sobre el residuo UV:
    la cascada NO mide M⁴ (compatible desde 0.2× hasta ∞).

  The same α that fixes the inflationary tensor-to-scalar ratio r = 12α/N² ≈ 0.00813
  (testable by LiteBIRD 2032) also fixes the dark-energy UV cutoff M = φ²×5^(1/4)×ρ_crit^(1/4).
  The reframe makes H_glob (SH0ES·(1−f_screen)) both the global background H and the CMB anchor
  (with ω_b,ω_c fixed by algebra, plik_lite minimises there). The cascade runs
  SH0ES IN, H_global OUT: the pure number is the TARGET the output is compared
  against, never the seed.
  The UV step remains CONDITIONAL on Postulate C.1 (Theorem C.1, Paper 10).

  PENDING (Paper 10): first-principles derivation of M⁴ = 45α² without using SH0ES as input.
    Ruta A: K(X) Taylor matching with K_α(X) = −3α ln(1−X/(3α)) → M⁴ = 6αKAL² ≈ 418 ≠ 234.9
            (requires additional normalization constraint — under investigation)
    Ruta B: Technical naturalness EFT → M² = √45 × α × ρ_crit^(1/2)
    Ruta C: Full P(X,φ) Lagrangian from Paper 1 → determines M algebraically at 2nd order
""")
print(sep)

# ── LOG con acta (2026-09-30) ───────────────────────────────────────────────
# Hasta hoy este script solo imprimia: por eso Paper 9 llevaba a mano
# «s_K^full = s_K^IR + 0.013608 = 0.416910», 5e-6 corrido de lo que este
# calculo da (0.013603 / 0.416905). f_screen tiene TRES piezas y se guardan
# las tres con su nombre: el termino IR, la correccion UV y el COMPLETO
# (IR+UV), que es el unico canonico — la cascada usa el completo.
# CONTROL (R53): el nucleo calcula s_K_full por otra via (en unidades de
# rho_crit, sin anclar meV); los dos tienen que coincidir a 1e-12.
import json as _json
import ssee_core as _S
from procedencia import con_acta as _con_acta
_log = _reloc_os.path.join(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__)),
                           "..", "..", "results", "logs", "p10_uv_fscreen.json")
_res = dict(
    s_K_IR=float(s_K_IR), s_K_UV_corr=float(s_K_UV - s_K_IR), s_K_full=float(s_K_UV),
    f_screen_IR=float(f_screen_IR), f_screen_UV_corr=float(f_screen_UV - f_screen_IR),
    f_screen_full=float(f_screen_UV),
    H0_SH0ES=H0_SH0ES, sigma_SH0ES=sigma_SH0ES,
    H0_glob=float(H0_glob_UV), sigma_H0_glob=float(sigma_glob),
    H0_glob_IR_historico=float(H0_glob_IR),
    residuo_vs_numero_puro=float(H0_glob_UV - H0_alg),
    control_nucleo=dict(s_K_full_nucleo=float(_S.S_K_FULL),
                        pasa=bool(abs(s_K_UV - _S.S_K_FULL) < 1e-12)),
    nota="f_screen COMPLETO = IR + correccion UV; es el canonico. El IR solo es el regimen M->inf (Papers 1-9).")
with open(_reloc_os.path.abspath(_log), "w") as _fh:
    _json.dump(_con_acta(_res, __file__), _fh, indent=1)
print(f"  -> log: {_reloc_os.path.abspath(_log)}  (control nucleo: {_res['control_nucleo']['pasa']})")
