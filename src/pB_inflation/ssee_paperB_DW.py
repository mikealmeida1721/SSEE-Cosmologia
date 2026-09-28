"""
⚠️  PRE-CANÓNICO — usa m_φ=5.60 eV (fórmula Σm_ν×H_alg, RETIRADA 2026-06-04).
    El que la sucedió, m_φ=40.70 eV (Σm_ν×SOLAR²·KRYSTOS=594.28), está
    **RETIRADO desde el 2026-08-01** junto con la partícula entera, igual que
    36.95 vía 535.28 y 42.47 vía 615.33. Ninguna masa φ-DM está vigente.
    Script conservado como registro de por qué la ruta DW con 5.60 eV fue descartada.

Paper B — Problema 2: Ángulo de mezcla Dodelson-Widrow para Ω_φDM = Ω_CDM.

Pregunta: dado m_φ=5.60 eV y Ω_φDM h²=0.0739, ¿qué sin²(2θ) requiere
el mecanismo DW? ¿Tiene ese ángulo una expresión algebraica SSEE?

Referencia principal: Boyarsky, Ruchayskiy & Shaposhnikov (2009) rev.
  sin²2θ = C(m_s) × (Ω_s h² / 0.12) × (keV/m_s)^{1.83}
  C ≈ 3.6×10⁻⁹ (ajuste numérico a la integral de Boltzmann completa)

Producción DW: mezcla vacío θ pequeño → ν_active → ν_sterile en plasma
caliente vía colisiones (sin resonancia MSW). T_peak ~ m_W²/T_QCD ~ GeV.
"""
import numpy as np
from scipy.optimize import brentq

# ── Constantes algebraicas SSEE ───────────────────────────────────────────────
phi   = (1 + 5**0.5) / 2          # razón áurea ≈ 1.6180
pi    = np.pi
Omega = phi + pi                   # ≈ 4.7596
beta  = Omega / 2                  # ≈ 2.3798
KAL0  = beta + pi                  # ≈ 5.5214
MIRA  = (3*phi + pi) / 4          # ≈ 1.9989
AURA  = (3*phi + pi) / 2          # ≈ 3.9978
alpha_K = 12*phi**4 / (3*(2*phi**7)**2)  # αK=0.4033 (Paper 7)

# Parámetros cosmológicos SSEE
Omm_dyn  = 0.160                   # Ω_m,dyn
Om_CDM   = Omm_dyn                 # = Ω_φDM (unificación algebraica)
Om_phiDM = (MIRA - 1) * Omm_dyn   # ≈ 0.15987
# ORIGEN-VALOR: 0.6796 — H_alg/100 = 3(phi+pi)^2/100 = 0.679621. El comentario de al lado lo atribuia al MCMC de Paper 2, que da 0.6779: atribucion equivocada (script RETIRADO)
# ORIGEN-VALOR: 0.0739 — (MIRA-1)*0.160*0.6796^2 = 0.07382 (el 0.0739 del texto esta corrido en la 4a cifra), de la particula RETIRADA
h_ssee   = 0.6796                  # H₀/100 = H_alg/100 (NO el MCMC de P2; corregido 2026-09-19)
Om_phiDM_h2 = Om_phiDM * h_ssee**2  # ≈ 0.0739

m_phi_eV = 5.60                    # eV — derivado algebraicamente (Paper 6)
m_phi_keV = m_phi_eV * 1e-3       # en keV

print("=" * 70)
print("Paper B — Problema 2: Ángulo de mezcla DW para m_φ=5.60 eV")
print("=" * 70)
print(f"\n  m_φ          = {m_phi_eV:.4f} eV  = {m_phi_keV:.6f} keV")
print(f"  Ω_φDM h²     = {Om_phiDM_h2:.6f}")
print(f"  (Ω_φDM = (MIRA−1)·Ω_m,dyn ≈ {Om_phiDM:.6f})")

# ── Bloque A: Fórmula DW estándar ────────────────────────────────────────────
print("\n" + "=" * 70)
print("[A] Boyarsky-Ruchayskiy-Shaposhnikov 2009 — scaling law")
print("=" * 70)

# Fit numérico a Boltzmann DW completo:
# Ω_s h² = C_DW × sin²2θ × (m_s/keV)^{1.83} × (g_*/10.75)^{-3/4}
C_DW     = 1.1e8              # de BRS 2009 (con g_*=10.75 absorbido en C)
alpha_DW = 1.83               # exponente de masa
g_star   = 106.75             # DOF en T_peak ~ GeV (SM completo)
g_ref    = 10.75              # referencia BRS 2009

# Corrección g_*:
g_corr = (g_star / g_ref)**(-0.75)

# sin²2θ desde Ω_φDM h²:
# Ω h² = C_DW × sin²2θ × m_keV^{1.83} × g_corr
# → sin²2θ = Ω h² / (C_DW × m_keV^{1.83} × g_corr)
sin2theta_BRS = Om_phiDM_h2 / (C_DW * m_phi_keV**alpha_DW * g_corr)

print(f"\n  Parámetros:")
print(f"    C_DW     = {C_DW:.2e}")
print(f"    α_DW     = {alpha_DW}")
print(f"    g_*      = {g_star}  →  g_corr = {g_corr:.4f}")
print(f"    m_φ^1.83 = {m_phi_keV**alpha_DW:.4e}")
print(f"\n  sin²(2θ)_DW = {sin2theta_BRS:.4e}")
print(f"  θ_DW        = {np.degrees(0.5*np.arcsin(np.sqrt(sin2theta_BRS))):.4f}°")

# Verificación inversa:
Omega_check = C_DW * sin2theta_BRS * m_phi_keV**alpha_DW * g_corr
print(f"\n  Verificación: Ω h² = {Omega_check:.6f}  (target: {Om_phiDM_h2:.6f})")

# ── Bloque B: Fórmula DW alternativa — Dodelson & Widrow 1994 original ───────
print("\n" + "=" * 70)
print("[B] Dodelson & Widrow 1994 — fórmula original")
print("=" * 70)
print("""
  La fórmula original DW94 (no corregida por QCD) para m_s >> m_ν,activos:

    Ω_s h² ≈ 0.3 × (sin²2θ / 3×10⁻⁹) × (m_s / 3 keV)²

  Válida estrictamente para m_s ~ keV donde la producción ocurre cerca
  de T_QCD ~ 150 MeV. Para m_φ=5.60 eV, la producción se desplaza a
  T_peak ~ GeV donde la corrección de QCD importa → usar BRS 2009.
""")

C_DW94 = 0.3 / 3e-9 / (3)**2   # = 0.3 / (3e-9 × 9) = 1.11e7 keV⁻²
sin2theta_DW94 = Om_phiDM_h2 / (C_DW94 * m_phi_keV**2)

print(f"  sin²(2θ)_DW94 = {sin2theta_DW94:.4e}")
print(f"  θ_DW94        = {np.degrees(0.5*np.arcsin(min(1,np.sqrt(sin2theta_DW94)))):.4f}°")

# ── Bloque C: T_peak para m_φ=5.60 eV ───────────────────────────────────────
print("\n" + "=" * 70)
print("[C] Temperatura de producción pico T_peak(m_φ=5.60 eV)")
print("=" * 70)

GF_eV2  = 1.1664e-5 * (1e-9)**2   # G_F en eV⁻²
mW_eV   = 80.4e9                    # m_W en eV

# La mezcla en materia se suprime cuando V_T ~ δm²:
# V_T ≈ 8√2 G_F E <E> / m_W² × T³ ~ C_V × T^5 (de QCD/EW)
# δm² ≈ m_s² (para m_s >> m_activo)
# T_peak cuando d/dT [Γ×s/H] = 0 → T_peak ∝ (m_s² m_W² / G_F)^{1/5}
T_peak_eV = (m_phi_eV**2 * mW_eV**2 / GF_eV2)**0.2

print(f"\n  T_peak(m_φ=5.60 eV) ≈ {T_peak_eV:.3e} eV  = {T_peak_eV/1e9:.3f} GeV")
print(f"  (Cf. T_peak para m_s=3 keV ≈ 130 MeV)")
print(f"\n  → Producción DW para m_φ=5.60 eV ocurre a T ~ {T_peak_eV/1e9:.1f} GeV")
print(f"    (rango pre-QCD, donde g_* ≈ 106.75 — fórmula BRS válida)")

# ── Bloque D: Estabilidad frente a decaimiento ────────────────────────────────
print("\n" + "=" * 70)
print("[D] Vida media frente a ν_s → ν_a + γ")
print("=" * 70)

# Tasa de decaimiento radiativo (Pal & Wolfenstein 1982):
# Γ = (9 α G_F² / 256 π⁴) × sin²2θ × m_s^5
# En unidades donde Γ [s⁻¹] = 5.5×10⁻²² × sin²2θ × (m_s/keV)^5
Gamma_decay = 5.5e-22 * sin2theta_BRS * m_phi_keV**5   # s⁻¹
tau_decay   = 1 / Gamma_decay if Gamma_decay > 0 else np.inf
t_universe  = 4.35e17  # s

print(f"\n  Γ(ν_s→ν_a γ) = {Gamma_decay:.2e} s⁻¹")
print(f"  τ_decay      = {tau_decay:.2e} s")
print(f"  t_universe   = {t_universe:.2e} s")
print(f"  τ/t_univ     = {tau_decay/t_universe:.2e}  {'✓ estable' if tau_decay > 100*t_universe else '✗ inestable'}")

# ── Bloque E: Scan de expresiones algebraicas SSEE ───────────────────────────
print("\n" + "=" * 70)
print("[E] Scan — ¿sin²(2θ) tiene expresión algebraica SSEE?")
print("=" * 70)

sin2_target = sin2theta_BRS
print(f"\n  Valor objetivo: sin²(2θ) = {sin2_target:.6e}")
print(f"  log₁₀[sin²2θ] = {np.log10(sin2_target):.4f}\n")

# Candidatos dimensionless desde constantes SSEE
candidates = {}

# Potencias de φ
for n in range(5, 30):
    candidates[f"φ⁻{n}"] = phi**(-n)

# Potencias de π
for n in range(5, 20):
    candidates[f"π⁻{n}"] = pi**(-n)

# Productos φ^n × π^m
for n in [1, 2, 3, 4, 5, 7, 10]:
    for m in [1, 2, 3, 4, 5]:
        candidates[f"φ⁻{n}×π⁻{m}"] = phi**(-n) * pi**(-m)

# Constantes compuestas SSEE
candidates["MIRA⁻¹⁰"] = MIRA**(-10)
candidates["MIRA⁻¹²"] = MIRA**(-12)
candidates["MIRA⁻¹⁵"] = MIRA**(-15)
candidates["AURA⁻⁸"]  = AURA**(-8)
candidates["AURA⁻¹⁰"] = AURA**(-10)
candidates["KAL₀⁻⁸"]  = KAL0**(-8)
candidates["KAL₀⁻¹⁰"] = KAL0**(-10)
candidates["Ω⁻¹⁰"]    = Omega**(-10)
candidates["Ω⁻¹²"]    = Omega**(-12)
candidates["αK²"]      = alpha_K**2
candidates["αK³"]      = alpha_K**3
candidates["αK/φ⁷"]    = alpha_K / phi**7
candidates["αK²/φ⁷"]   = alpha_K**2 / phi**7
candidates["αK/N_*"]   = alpha_K / (2*phi**7)
candidates["(π-φ)^10"] = (pi-phi)**10
candidates["(π-φ)^8"]  = (pi-phi)**8
candidates["1/N_*²"]   = 1/(2*phi**7)**2
candidates["1/N_*³"]   = 1/(2*phi**7)**3
candidates["φ⁻⁷/N_*"]  = phi**(-7) / (2*phi**7)
candidates["φ⁻¹⁰·π⁻³"] = phi**(-10) * pi**(-3)
candidates["φ⁻¹²·π⁻²"] = phi**(-12) * pi**(-2)
candidates["m_φ/mW²_nat"] = (m_phi_eV / 80.4e9)**2  # (m_φ/m_W)²

# Filtrar y mostrar los 20 más cercanos
sorted_cands = sorted(candidates.items(),
                      key=lambda x: abs(np.log10(x[1]) - np.log10(sin2_target)))

print(f"  {'Expresión':<22} {'Valor':>14} {'log₁₀':>8} {'Δlog₁₀':>10} {'Δ%':>10}")
print(f"  {'-'*22} {'-'*14} {'-'*8} {'-'*10} {'-'*10}")
for name, val in sorted_cands[:25]:
    log_diff = abs(np.log10(val) - np.log10(sin2_target))
    pct_diff = abs(val - sin2_target) / sin2_target * 100
    star = " ★★" if pct_diff < 2 else (" ★" if pct_diff < 10 else ("~" if pct_diff < 30 else ""))
    print(f"  {name:<22} {val:>14.4e} {np.log10(val):>8.3f} {log_diff:>10.3f} {pct_diff:>9.1f}%{star}")

# ── Bloque F: Mejor candidato — análisis detallado ────────────────────────────
print("\n" + "=" * 70)
print("[F] Mejor candidato SSEE — análisis de consistencia")
print("=" * 70)

best_name, best_val = sorted_cands[0]
best_pct = abs(best_val - sin2_target) / sin2_target * 100

print(f"\n  Mejor candidato: {best_name}")
print(f"  Valor SSEE:      {best_val:.6e}")
print(f"  Valor DW:        {sin2_target:.6e}")
print(f"  Discrepancia:    {best_pct:.2f}%")

# ── Bloque G: Verificación alternativa — producción gravitacional ─────────────
print("\n" + "=" * 70)
print("[G] Alternativa — Producción Gravitacional (sin mezcla activo-estéril)")
print("=" * 70)
print("""
  Para φ-DM con m_φ ~ eV, la producción gravitacional (Parker 1969;
  Chung, Kolb & Riotto 1998) es una alternativa natural al DW:

    Ω_φDM ≈ C_grav × (m_φ/H_end)^{1/2} × V_end/ρ_crit

  Ventaja: cero parámetros de mezcla — solo depende de m_φ y el
  potencial inflacionario V(φ), ambos ya fijados en SSEE.

  Si este mecanismo reproduce Ω_φDM=Ω_CDM, el modelo es completamente
  libre de parámetros sin necesitar θ_DW.
""")

# Estimación orden de magnitud de producción gravitacional
# Chung+Riotto+Kolb 1998: n_s ~ 10^{-2} H_end^3 para m_s << H_end
# ρ_s = m_s × n_s → Ω_s = ρ_s / ρ_crit,0
Mpl_GeV   = 2.435e18        # GeV
As_planck = 2.1e-9          # amplitud espectral
alpha_inf = phi**4 / 3      # α = φ⁴/3

# V_end (de script ssee_paperB_Nstar.py): V_end ≈ As × 3π²/α × (1-x_end)²
# Aproximación numérica:
V_end_Mpl4 = 1.505e-8       # Mpl⁴ (del script Nstar)
H_end_Mpl  = V_end_Mpl4**0.5   # H_end ≈ √V_end (Friedmann)

m_phi_Mpl  = m_phi_eV / (Mpl_GeV * 1e9)  # en unidades Mpl

# Parker formula: n_s ~ (H_end/2π)³ × (m_s/H_end)^{1/2} (para m_s << H_end)
n_grav_Mpl3 = (H_end_Mpl/(2*pi))**3 * (m_phi_Mpl/H_end_Mpl)**0.5

# Densidad hoy: ρ_s = m_φ × n_s × (a_end/a_0)³
# (a_end/a_0)³ desde entropía: s ~ g_* T³, a³ s = const
# a_end/a_0 = (g_*s,0 T_0³ / g_*s,rh T_rh³)^{1/3} × (T_rh/T_0)
T_rh_Mpl    = 9.345e15 / (Mpl_GeV*1e9)   # T_rh en Mpl (del script Nstar)
T0_Mpl      = 2.348e-4 / (Mpl_GeV*1e9)    # T_0 = 2.348×10⁻⁴ eV en Mpl
g_rh        = 106.75
g0_s        = 3.91

dilution = (g0_s * T0_Mpl**3) / (g_rh * T_rh_Mpl**3)
rho_phi_today = m_phi_Mpl * n_grav_Mpl3 * dilution

rho_crit_Mpl4 = (__import__("ssee_core").H0_GLOBAL * 1e3 / (3.086e22)) **2 * 3 / (8*pi) / (Mpl_GeV*1e9)**4
Omega_grav = rho_phi_today / rho_crit_Mpl4

print(f"  H_end         = {H_end_Mpl:.3e} Mpl  ≈ {H_end_Mpl * Mpl_GeV*1e9:.3e} eV")
print(f"  m_φ / H_end   = {m_phi_Mpl/H_end_Mpl:.3e}  (≪ 1 — producción IR ✓)")
print(f"  n_grav (Mpl³) = {n_grav_Mpl3:.3e}")
print(f"  dilución      = {dilution:.3e}")
print(f"  Ω_φ,grav (estimación) ≈ {Omega_grav:.3e}")
print(f"  Ω_φDM (target) = {Om_phiDM:.6f}")
print(f"  Ratio          = {Omega_grav/Om_phiDM:.3e}")
print(f"""
  → La producción gravitacional sub-estimada aquí en {Omega_grav/Om_phiDM:.1e}×:
    requiere corrección de prefactor C_grav no trivial.
    Paper B necesita la integral de producción gravitacional completa
    para m_φ ~ eV con espectro de Starobinsky (α-attractor).
""")

# ── CONCLUSIÓN ────────────────────────────────────────────────────────────────
print("=" * 70)
print("RESUMEN — Paper B Problema 2")
print("=" * 70)
print(f"""
MECANISMO DW ESTÁNDAR:
  m_φ = {m_phi_eV} eV,  Ω_φDM h² = {Om_phiDM_h2:.4f}
  → sin²(2θ)_DW = {sin2theta_BRS:.4e}  (BRS 2009)
  → sin²(2θ)_DW = {sin2theta_DW94:.4e}  (DW 1994 original)
  → T_peak       ≈ {T_peak_eV/1e9:.2f} GeV  (pre-QCD, g_*≈{g_star:.0f})
  → τ_decay/t_univ = {tau_decay/t_universe:.1e}  ✓ estable

MEJOR CANDIDATO ALGEBRAICO SSEE:
  {best_name} = {best_val:.4e}  (Δ = {best_pct:.1f}% de sin²2θ_DW)

ESTADO:
  - Si Δ < 5%:  resultado "limpio" — señal SSEE. Requiere derivación física.
  - Si Δ > 10%: DW no admite forma algebraica SSEE → explorar producción
                gravitacional como mecanismo alternativo.
  - Producción gravitacional: estimación orden magnitud = {Omega_grav:.1e},
    factor {Omega_grav/Om_phiDM:.1e} bajo del target — necesita C_grav del espectro exacto.

APERTURA:
  Como en N_*=2φ⁷, la derivación completa requiere Paper B:
  especificar el mecanismo de producción de φ-DM y calcular su
  relic abundance desde primeros principios con α=φ⁴/3.
""")
