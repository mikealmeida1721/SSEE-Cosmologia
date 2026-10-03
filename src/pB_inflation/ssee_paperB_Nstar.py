"""
Paper B — Derivación de N_* = 2φ⁷ desde inflación quintaesencial α-attractor.

Potencial: V(φ) = V₀ (1 − e^{−√(2/3α) φ})²   con α = φ⁴/3
Reheating: gravitacional (stiff fluid w=1 post-inflación)
Fórmula N_*: García-Bellido & Ruiz Morales 2002; Pellejero-Ibáñez 2020
"""
import numpy as np

phi   = (1 + 5**0.5) / 2
pi    = np.pi
alpha = phi**4 / 3          # α-attractor parámetro SSEE

# Constantes físicas
Mpl   = 1.0                 # unidades de Planck reducida (ℏ=c=Mpl=1)
As    = 2.1e-9              # amplitud espectro escalar Planck 2018
g_rh  = 106.75              # g* en reheating (SM completo)
N_target = 2 * phi**7      # 58.069...

print("=" * 65)
print("Paper B — N_*(T_rh) para α-attractor quintaesencial")
print("=" * 65)
print(f"\n  α = φ⁴/3       = {alpha:.6f}")
print(f"  N_target = 2φ⁷ = {N_target:.6f} e-folds")

# ── Paso 1: Energía al final de la inflación ──────────────────────────────
# Para α-attractor, al final de slow-roll (ε=1):
# ε = (4/3α) e^{−2√(2/3α)φ_end} / (1 − e^{−√(2/3α)φ_end})² = 1
# Solución numérica de φ_end:
from scipy.optimize import brentq

kappa = np.sqrt(2 / (3 * alpha))   # = √(2/(3α)) = √(2·3/φ⁴·3) = √(2/φ⁴)

def epsilon(phi_inf):
    x = np.exp(-kappa * phi_inf)
    return (4 / (3 * alpha)) * x / (1 - x)**2

phi_end = brentq(lambda p: epsilon(p) - 1, 0.1, 5.0)
x_end   = np.exp(-kappa * phi_end)
V_end   = As * (3 * pi**2 / alpha) * (1 - x_end)**2   # en unidades Mpl⁴

print(f"\n[1] Fin de inflación")
print(f"  κ = √(2/3α)    = {kappa:.6f}")
print(f"  φ_end (Mpl)    = {phi_end:.4f}")
print(f"  ε(φ_end) check = {epsilon(phi_end):.6f}  (debe ser 1)")
print(f"  V_end/Mpl⁴     = {V_end:.4e}")
# 2026-10-02: convertía con 1.22e19 (Planck NO reducida) aunque todo va en Planck reducida;
# daba 1.136e17 GeV, 5x de más. La sección [6] ya lo hacía bien con Mpl_GeV.
print(f"  V_end^(1/4)    = {V_end**0.25:.4e} Mpl  ≈ {V_end**0.25 * 2.435e18:.3e} GeV  (Mpl reducida)")

# ── Paso 2: Fórmula N_* para reheating gravitacional (w=1) ───────────────
# Quintessential inflation con stiff fluid:
#   N_* = A − (1/3) ln(T_rh / GeV) + correcciones
#
# Fórmula exacta (Pellejero-Ibáñez et al. 2020, Eq. 3.14):
#   N_* = 58.25 − (1/3) ln(g_rh/106.75)^(1/4) − (1/3) ln(T_rh/10⁹ GeV)
#         + (2/3) ln(V_end^(1/4) / 10^{15.5} GeV)
#
# En unidades Planck (Mpl = 2.435e18 GeV):
Mpl_GeV = 2.435e18   # GeV

def N_star(T_rh_GeV):
    """N_* como función de T_rh en GeV (reheating gravitacional, w=1)."""
    # ρ_rh = (π²/30) g_rh T_rh⁴  en unidades GeV⁴/Mpl⁴
    rho_rh = (pi**2 / 30) * g_rh * (T_rh_GeV / Mpl_GeV)**4
    # ρ_end en Mpl⁴
    rho_end = 3 * V_end   # ρ_end ≈ 3V_end al final de slow-roll
    # N_* = 58.25 − (1/6)ln(ρ_end/ρ_rh)  para w_rh=1
    return 58.25 - (1/6) * np.log(rho_end / rho_rh)

print(f"\n[2] N_*(T_rh) — rango de reheating cosmológico")
print(f"  {'T_rh (GeV)':<20} {'N_*':>10}")
print(f"  {'-'*20} {'-'*10}")
for T in [1e15, 1e12, 1e9, 1e6, 1e3, 1e0, 1e-3, 1e-4, 1e-6]:
    print(f"  {T:<20.2e} {N_star(T):>10.3f}")

# ── Paso 3: Invertir — qué T_rh produce N_* = 2φ⁷ exacto ────────────────
T_rh_solution = brentq(lambda T: N_star(T) - N_target, 1e-10, 1e18)

print(f"\n[3] T_rh que produce N_* = 2φ⁷ exacto")
print(f"  N_* = {N_star(T_rh_solution):.6f}  (target: {N_target:.6f})")
print(f"  T_rh = {T_rh_solution:.6e} GeV")
print(f"  T_rh = {T_rh_solution * 1e3:.6e} MeV")
print(f"  T_rh = {T_rh_solution * 1e9:.6e} keV")
print(f"  T_rh = {T_rh_solution * 1e12:.6e} eV")

# ── Paso 4: Comparar con constantes SSEE ─────────────────────────────────
print(f"\n[4] ¿T_rh tiene expresión SSEE?")
print(f"  (comparar T_rh en eV con constantes del modelo)")

T_eV = T_rh_solution * 1e9    # en eV (2026-10-02: era *1e12, GeV->eV es 1e9)

# Constantes SSEE en eV (usando H₀_SSEE = 67.96 km/s/Mpc)
# 2026-10-02: la conversion anterior (x3.241e-20 x1.973e-7 x1e9) no cerraba dimensiones (~4e-16 eV).
# H0 [km/s/Mpc] -> s^-1 (1 Mpc = 3.0856775814913673e19 km) -> eV (hbar = 6.582119569e-16 eV s, CODATA 2018)
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
H0_eV   = __import__("ssee_core").H0_GLOBAL / 3.0856775814913673e19 * 6.582119569e-16
Omega   = phi + pi
beta    = Omega / 2
KAL0    = beta + pi
MIRA    = (3*phi + pi) / 4
AURA    = (3*phi + pi) / 2
# RETIRADO 2026-09-19: aqui vivia `m_phi = 40.70` eV, la masa de la particula
# phi-DM, retirada el 2026-08-01. Entraba abajo como uno de los candidatos
# contra los que se compara T_rh, o sea como una escala fisica en uso.
Lambda_SSEE = 9.68e-3           # eV (= M UV completion, canónico Paper 10 con H_alg=67.962 (reframe; era 9.62@67.037))

# Escalas físicas conocidas
T_EW    = 100e9                 # eV (transición electroweak)
T_BBN   = 1e6                   # eV (nucleosíntesis)
T_QCDH  = 150e6                 # eV (transición QCD hadrónica)

candidates = {
    "T_EW (electroweak) 100 GeV":     T_EW,
    "T_BBN (nucleosíntesis) 1 MeV":   T_BBN,
    "T_QCD (hadrónica) 150 MeV":      T_QCDH,
    "Λ_SSEE = M = 9.68 meV":          Lambda_SSEE,
    "H₀_SSEE (eV)":                   H0_eV,
    "Ω × H₀ (eV)":                   Omega * H0_eV,
    "φ¹² × H₀ (eV)":                 phi**12 * H0_eV,
}

print(f"\n  T_rh = {T_eV:.4e} eV\n")
print(f"  {'Candidato':<35} {'Valor (eV)':>14} {'Ratio T_rh/X':>14} {'Cercano?':>10}")
print(f"  {'-'*35} {'-'*14} {'-'*14} {'-'*10}")
for name, val in candidates.items():
    ratio = T_eV / val
    close = "⭐" if 0.5 < ratio < 2.0 else ("~" if 0.1 < ratio < 10 else "")
    print(f"  {name:<35} {val:>14.3e} {ratio:>14.4f} {close:>10}")


# ── Paso 5: La near-coincidencia ρ_end/ρ_rh ≈ 3 ─────────────────────────
print("\n" + "=" * 65)
print("DESCUBRIMIENTO: ρ_end/ρ_rh ≈ 3 (casi exacto)")
print("=" * 65)

rho_end_Mpl4 = 3 * V_end
rho_rh_Mpl4  = (pi**2 / 30) * g_rh * (T_rh_solution / Mpl_GeV)**4
ratio_found   = rho_end_Mpl4 / rho_rh_Mpl4

print(f"\n  ρ_end / ρ_rh  = {ratio_found:.6f}")
print(f"  vs exacto 3   = 3.000000")
print(f"  Diferencia    = {abs(ratio_found - 3):.6f}  ({abs(ratio_found-3)/3*100:.3f}%)")

# Si ρ_end/ρ_rh = 3 EXACTO → ¿qué N_* daría?
N_if_ratio3 = 58.25 - (1/6) * np.log(3.0)
print(f"\n  Si ρ_end/ρ_rh = 3 exacto:")
print(f"  N_* = 58.25 − ln(3)/6 = 58.25 − {np.log(3)/6:.6f} = {N_if_ratio3:.6f}")
print(f"  2φ⁷ =                                                {N_target:.6f}")
print(f"  Δ = {abs(N_if_ratio3 - N_target):.6f}  ← depende de la constante 58.25")

# El 58.25 en la fórmula tiene correcciones de orden (1/N*)
# Si la constante exacta del modelo es 58.25 + δ, el ratio 3 cierra exactamente
delta_needed = N_target - (58.25 - np.log(3)/6)
print(f"\n  Corrección δ para cierre exacto: 58.25 + {delta_needed:.6f}")
print(f"  Esta corrección es O(1/N_*) ≈ {1/N_target:.4f}  — dentro de incertidumbre teórica")

print(f"""
  INTERPRETACIÓN:
  ─────────────────────────────────────────────────
  La condición ρ_end/ρ_rh = 3 es físicamente natural:
  • 3 = dimensiones espaciales (argumento de equipartición)
  • ρ_end = 3V_end (inflación con ε = 1: KE = 2V, total = 3V)
  • ρ_rh = V_end → T_rh = V_end^(1/4) × (30/π²g*)^(1/4)
  
  Si este ansatz (ρ_rh = V_end) se deriva desde el modelo de
  reheating gravitacional SSEE, entonces N_* = 2φ⁷ es consecuencia.
  
  El puente faltante: demostrar que la eficiencia de producción
  gravitacional de partículas con α=φ⁴/3 da exactamente ρ_rh = V_end.
""")

# ── Paso 6: T_rh en unidades SSEE naturales ──────────────────────────────
print("[5] T_rh expresada en términos de V_end^(1/4)")
print("-" * 65)
Vend_quarter_GeV = V_end**0.25 * Mpl_GeV
coeff = T_rh_solution / Vend_quarter_GeV
print(f"  V_end^(1/4)      = {Vend_quarter_GeV:.4e} GeV")
print(f"  T_rh             = {T_rh_solution:.4e} GeV")
print(f"  T_rh / V_end^(1/4) = {coeff:.6f}")
print(f"  (30/π²g*)^(1/4)  = {(30/(pi**2*g_rh))**0.25:.6f}")
print(f"  Ratio / (30/π²g*)^(1/4) = {coeff / (30/(pi**2*g_rh))**0.25:.6f}  ≈ {coeff / (30/(pi**2*g_rh))**0.25:.3f}")
print(f"\n  → T_rh = (30/π²g*)^(1/4) × V_end^(1/4)  si ρ_rh = V_end (ratio=3)")
print(f"  → T_rh está completamente determinada por α=φ⁴/3 y As (ambos SSEE/Planck)")
