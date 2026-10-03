#!/usr/bin/env python3
"""cajones_algebra.py — las cuentas de álgebra y aritmética que citan los cajones (2026-10-02).

POR QUE. R74 marcaba en OPEN_PROBLEMS.md y VERIFICATION_LEDGER.md números que no
salen de ninguna corrida: son cuentas a mano sobre φ y π (φ¹¹, √(3/2), π−φ,
4·KAL₀−22…) o sobre constantes físicas conocidas. Escritas a mano no se puede
saber si están bien, y de hecho al calcularlas aparecieron tres erratas
(η del slow-roll, V_end^(1/4) de Paper B y √AURA/MIRA). Aquí cada una se CALCULA
desde src/ssee_core.py, con su fórmula al lado, y queda en
results/logs/cajones_algebra.json con acta. Los cajones citan ese valor.

No es un resultado del modelo: es la aritmética de los comentarios. Una cuenta
del modelo (con datos) va en su propio script.

CONTROL (R53). Cada identidad que se declara EXACTA en los cajones se comprueba
por dos caminos (p. ej. r = 16ε contra φ⁻¹⁰, n_s(orden 1) = 1−2/N_* contra
1−φ⁻⁷), y el otro lado: una identidad falsa a propósito (φ¹¹ contra 200) tiene
que dar distinto. Si algo no cuadra, el script sale con error.
"""
import json
import math
import os
import sys

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
import ssee_core as S  # noqa: E402
from procedencia import con_acta  # noqa: E402

PHI, PI = S.PHI, S.PI
SALIDA = os.path.join(_R, "results", "logs", "cajones_algebra.json")

# Constantes físicas EXTERNAS (no son del modelo):
M_P_GEV = 0.93827208816     # ORIGEN-VALOR: 0.93827208816 GeV — masa del protón, CODATA 2018 / PDG 2024
M_E_GEV = 0.00051099895     # ORIGEN-VALOR: 0.00051099895 GeV — masa del electrón, CODATA 2018
M_HE4_NUC_GEV = 3.727379    # ORIGEN-VALOR: 3.727379 GeV — masa del núcleo de He-4 (alfa), CODATA 2018 (3727.3794066 MeV)
E_H_GEV = 13.6e-9           # ORIGEN-VALOR: 13.6 eV — ligadura del hidrógeno (despreciable a 6 cifras; se incluye por completitud)
X_H, Y_HE = 0.75, 0.25      # ORIGEN-VALOR: 0.75/0.25 — fracciones de masa H/He que declara OPEN_PROBLEMS (anotación 2026-09-08)
RHO_C100_GEV_CM3 = 1.05368e-5   # ORIGEN-VALOR: 1.05368e-5 h^2 GeV cm^-3 — densidad crítica, PDG 2024 tabla de constantes astrofísicas
N_GAMMA_CM3 = 410.7         # ORIGEN-VALOR: 410.7 cm^-3 — densidad de fotones del CMB a T=2.7255 K, PDG 2024

out = {}


def anota(clave, formula, valor):
    out[clave] = dict(formula=formula, valor=float(valor))
    return float(valor)


# ── OP-1 ──────────────────────────────────────────────────────────────
anota("ob_formula_vieja_P4", "3(pi-phi)/200", 3 * (PI - PHI) / 200)
anota("phi_11", "phi^11", PHI ** 11)
anota("pi_menos_phi", "pi - phi", PI - PHI)
anota("ob_h2_alg", "(pi-phi)/(3 Omega^2)", S.OMEGA_B_H2)

# ── OP-2: slow-roll del alfa-atractor con N_* = 2 phi^7, alfa = phi^4/3 ──
N = anota("N_star", "2 phi^7", 2 * PHI ** 7)
alfa = anota("alfa_atractor", "phi^4/3", PHI ** 4 / 3)
eps = anota("epsilon_V", "3 alfa/(4 N_*^2)", 3 * alfa / (4 * N ** 2))
eta = anota("eta_V", "-1/N_*", -1 / N)
anota("ns_orden1", "1 - 2/N_*  (orden dominante en 1/N_*)", 1 - 2 / N)
anota("ns_slowroll_completo", "1 + 2 eta_V - 6 epsilon_V", 1 + 2 * eta - 6 * eps)
r = anota("r_tensor", "16 epsilon_V", 16 * eps)
anota("phi_menos10", "phi^-10", PHI ** -10)

# ── OP-9 (retirado): números del barrido DW, sólo aritmética ──
anota("phi_menos21", "phi^-21", PHI ** -21)
anota("n_para_1e-5", "5 ln10 / ln phi  (phi^-n = 1e-5)", 5 * math.log(10) / math.log(PHI))

# ── OP-3 ──
anota("cuatro_tercios", "4/3", 4 / 3)

# ── OP-14: el offset 22 retirado ──
anota("cuatro_KAL", "4 KAL0", 4 * S.KAL0)
anota("R_offset22", "4 KAL0 - 22", 4 * S.KAL0 - 22)

# ── H_global en régimen IR (Paper 9) ──
anota("uno_menos_f_IR", "1 - f_screen^IR", 1 - S.F_SCREEN_IR)

# ── Paper 8: sqrt(AURA)/MIRA ──
anota("sqrtAURA_sobre_MIRA", "sqrt(AURA)/MIRA", math.sqrt(S.AURA) / S.MIRA)

# ── P7 / saturación: valores analíticos de la tabla del Registro ──
anota("alfa_sat_canonico", "sqrt(3/2)", math.sqrt(1.5))
anota("x_phi_MDE_canonico", "-1.2 sqrt(6)/3", -1.2 * math.sqrt(6) / 3)
anota("alfa_sat_SSEE", "sqrt(3/(phi+3 pi))", math.sqrt(3 / (PHI + 3 * PI)))

# ── OP-19: masa por barión y la lectura «misma cantidad» (anotación 2026-09-08) ──
m_H = M_P_GEV + M_E_GEV - E_H_GEV
m_He_por_barion = (M_HE4_NUC_GEV + 2 * M_E_GEV) / 4
mb = anota("m_barion_GeV", "1/(X/m_H + Y/(m_He4/4)), X=0.75, Y=0.25, con electrones",
           1 / (X_H / m_H + Y_HE / m_He_por_barion))
anota("m_proton_GeV", "CODATA", M_P_GEV)
kn = anota("KAL0_por_ns", "KAL0 n_s", S.KAL0 * S.N_S)
anota("m_DM_GeV", "KAL0 n_s m_barion", kn * mb)
nb = anota("n_b_cm3", "omega_b rho_c100 / m_barion", S.OMEGA_B_H2 * RHO_C100_GEV_CM3 / mb)
anota("eta_bariones", "n_b / n_gamma", nb / N_GAMMA_CM3)

# ── README, tabla de predicciones: Y_p y omega_c (2026-10-02) ──
# Y_p decía «AlterBBN = 0.2476» sin script ni log. Se calcula con el interpolador BBN de CAMB
# (tabla PArthENoPE, la del análisis de Planck 2018), en el omega_b algebraico y Delta N_eff = 0.
import camb.bbn as _bbn  # noqa: E402
YP_OBS = (0.2449, 0.0040)    # ORIGEN-VALOR: 0.2449 +- 0.0040 — Y_p observado, Aver, Olive & Skillman 2015 (JCAP 07, 011)
WC_PLANCK = (0.1200, 0.0012)  # ORIGEN-VALOR: 0.1200 +- 0.0012 — omega_c, Planck 2018 VI Tabla 2 (TT,TE,EE+lowE+lensing), data/raw/planck2018_VI/tabla2.tex
yp = anota("Yp_BBN_camb", "camb.bbn.get_predictor().Y_p(omega_b, 0)", _bbn.get_predictor().Y_p(S.OMEGA_B_H2, 0.0))
anota("Yp_tension_sigma", "(Y_p - 0.2449)/0.0040", (yp - YP_OBS[0]) / YP_OBS[1])
anota("wc_alg", "KAL0 omega_b n_s", S.OMEGA_C_H2)
anota("wc_tension_sigma", "(omega_c - 0.1200)/0.0012", (S.OMEGA_C_H2 - WC_PLANCK[0]) / WC_PLANCK[1])

# ── OP-21/22: viscosidad IS. c2_eff = w0 + zeta~/(tau_Pi H0), con zeta~ normalizado por la ENTALPÍA ──
tau = S.TAU_PI_H0
anota("c2_eff_zeta_1p5", "w0 + 1.5/(tau_Pi H0)", S.W0 + 1.5 / tau)
anota("c2_eff_zeta_2p2", "w0 + 2.2/(tau_Pi H0)", S.W0 + 2.2 / tau)
zm = anota("zeta_marginal", "-w0 · tau_Pi H0  (c2_eff = 0)", -S.W0 * tau)
anota("zeta_fisica_coef", "zeta_marginal · (1+w0)  (en unidades de rho_DE H0)", zm * (1 + S.W0))
anota("c2_eff_lectura_A", "w0 + zeta_marginal/((1+w0) tau_Pi H0)  (zeta~ leído por rho_DE)", S.W0 + zm / ((1 + S.W0) * tau))

# ── KAL0 = retención: sensibilidad (OP-19, anotación 2026-09-07) ──
smnu = S.R2_STABILITY * S.OMEGA_B_H2 * 93.14 / tau   # misma fórmula que ssee_core (_smnu_alg)
anota("sum_mnu_KALx1p1", "R2 omega_b 93.14/(tau_Pi H0), con KAL0 x1.1  (= /1.21)", smnu / 1.21)
anota("omega_c_KALx1p2", "1.2 · KAL0 omega_b n_s", 1.2 * S.OMEGA_C_H2)
anota("tauPiH0_KALx1p2", "1.2 · KAL0/(3 s_DE)", 1.2 * tau)
anota("R2_KALx1p2", "R2/1.2", S.R2_STABILITY / 1.2)
anota("X_sobre_KAL_KALx1p2", "(1/KAL0)/1.2  (X = 1)", 1 / (1.2 * S.KAL0))
anota("sum_mnu_tau_sin_sDE", "Sum m_nu / s_DE  (tau_Pi = KAL0/3 en vez de KAL0/(3 s_DE))", smnu / S.S_DE)
anota("C_nu_94p07_factor", "94.07 · omega_b / (tau_Pi H0)", 94.07 * S.OMEGA_B_H2 / tau)

# ── OP-18, ruta A: K_DE(X) = K_alfa(X/N) ──
kal_eff = anota("KAL_eff", "phi^2 sqrt(5/2)", PHI ** 2 * math.sqrt(2.5))
anota("uno_sobre_KAL0", "1/KAL0  (término lineal con X = 1)", 1 / S.KAL0)
anota("uno_sobre_KAL_eff", "1/KAL_eff", 1 / kal_eff)
anota("KAL0_sobre_KAL_eff", "KAL0/KAL_eff", S.KAL0 / kal_eff)

# ── OP-4: el radio de k-mouflage, con la fórmula publicada (rota) y con la que cierra ──
MSUN_KG = 1.98841e30          # ORIGEN-VALOR: 1.98841e30 kg — masa solar nominal, IAU 2015 B3 / CODATA 2018 G
GEV_KG = 1.78266192e-27       # ORIGEN-VALOR: 1.78266192e-27 kg/GeV — CODATA 2018
HBARC_GEV_M = 1.97326980e-16  # ORIGEN-VALOR: 1.97326980e-16 GeV m — hbar c, CODATA 2018
MPL_GEV = 2.435e18            # ORIGEN-VALOR: 2.435e18 GeV — masa de Planck reducida (la de Paper 8)
M_KM_GEV = 9.68e-12           # ORIGEN-VALOR: 9.68e-12 GeV — M = 9.68 meV, Paper 10 (M^4 = 5 phi^8 rho_crit)
AU_M, KPC_M = 1.495978707e11, 3.0856775814913673e19   # ORIGEN-VALOR: 1.495978707e11 m (UA, IAU 2012) y 3.0857e19 m (kpc)
msun = MSUN_KG / GEV_KG
for nom, m in (("sol", msun), ("vialactea", 1e12 * msun), ("cumulo", 1e15 * msun)):
    rhs = m / (4 * math.pi * MPL_GEV * M_KM_GEV ** 2)                  # GeV^-2
    rhs_ev = (m * 1e9) / (4 * math.pi * MPL_GEV * 1e9 * (M_KM_GEV * 1e9) ** 2)   # eV^-2
    anota(f"rkm_cubo_GeV_{nom}_m", "[M/(4 pi Mpl M^2)]^(1/3), todo en GeV, x hbar c", rhs ** (1 / 3) * HBARC_GEV_M)
    anota(f"rkm_cubo_eV_{nom}_m", "lo mismo todo en eV (x hbar c en eV m): la fórmula rota depende de la unidad",
          rhs_ev ** (1 / 3) * HBARC_GEV_M * 1e9)
    r2 = anota(f"rkm_cuadrado_{nom}_m", "[M/(4 pi Mpl M^2)]^(1/2) x hbar c  (forma que cierra, Brax & Valageas 2014)",
               math.sqrt(rhs) * HBARC_GEV_M)
    anota(f"rkm_cuadrado_{nom}_AU", "r / UA", r2 / AU_M)
    anota(f"rkm_cuadrado_{nom}_kpc", "r / kpc", r2 / KPC_M)

# ── OP-1: eta publicado (comparación de la cadena de conteo) ──
anota("eta_publicado", "PDG 2024, revisión BBN", 6.12e-10)   # ORIGEN-VALOR: 6.12e-10 — eta = n_b/n_gamma, PDG 2024 (Big-Bang Nucleosynthesis)

# ── Registro (corrección 2026-09-08): chi2_2D = 0.42 con 2 g.l. -> P -> sigma ──
from scipy.stats import norm as _norm, chi2 as _chi2_dist  # noqa: E402
pex = anota("P_exceder_chi2_0p42", "exp(-0.42/2)  (chi2, 2 g.l.; 0.42 = Paper 2 ec. 26 redondeado)", _chi2_dist.sf(0.42, 2))
anota("sigma_eq_chi2_0p42", "Phi^-1(1 - P/2)", _norm.isf(pex / 2))

# ── RETIRADO (aritmética histórica, para que el linaje se pueda comprobar) ──
# V-L2-10 del Registro: m_phi = Sum m_nu^active · (Omega^4 + AURA·KAL0), con el factor viejo
# 0.960318 (C_nu ≈ 93.86) que se retiró precisamente por NO tener fuente. Aquí sólo se
# comprueba que la cuenta escrita en el Registro es la que dice; nada de esto es vigente.
C_NU_VIEJO = 0.960318   # ORIGEN-VALOR: 0.960318 — factor RETIRADO sin fuente (Registro V-L2-10); se usa sólo para reproducir la cuenta histórica
r2 = anota("R2_retirado", "Omega/(KAL0 T_r)", S.OMEGA / (S.KAL0 * S.T_R))
snu = anota("sum_mnu_viejo_retirado", "R2 · 0.960318", r2 * C_NU_VIEJO)
mult = anota("multiplicador_viejo_retirado", "Omega^4 + AURA·KAL0", S.OMEGA ** 4 + S.AURA * S.KAL0)
anota("m_phi_viejo_retirado", "sum_mnu_viejo · multiplicador_viejo", snu * mult)

# ── CONTROL ──
ctrl = dict(
    r_igual_phi_menos10=abs(r - PHI ** -10) < 1e-15,
    ns_orden1_igual_1_menos_phi_menos7=abs((1 - 2 / N) - S.N_S) < 1e-15,
    otro_lado_phi11_distinto_de_200=abs(PHI ** 11 - 200) > 0.5,
    otro_lado_ns_completo_distinto_de_orden1=abs((1 + 2 * eta - 6 * eps) - (1 - 2 / N)) > 1e-3,
)
pasa = all(ctrl.values())
json.dump(con_acta(dict(identidades=out, control=dict(casos=ctrl, pasa=pasa)), __file__),
          open(SALIDA, "w"), indent=1)
for k, v in out.items():
    print(f"{k:30s} {v['valor']:.10g}   = {v['formula']}")
print("CONTROL:", "PASA" if pasa else "NO PASA", ctrl)
sys.exit(0 if pasa else 1)
