#!/usr/bin/env python3
"""
ssee_core.py — Fuente única de verdad para SSEE
=====================================================
TODO script de SSEE (src/ y class_ssee/) DEBE importar de aquí sus constantes
algebraicas, sus datos observacionales y la función de fondo de Friedmann.

NUNCA redefinir localmente phi, w0, los datos fsigma8, etc. La divergencia entre
tres copias de la ODE de crecimiento (verification / plot_calibrated / mcmc) y el
bug E²(z=0)=1.16 de Paper 6 ocurrieron exactamente por copias locales divergentes.

Uso desde src/:           from ssee_core import PHI, W0, friedmann_E2, load_fsigma8
Uso desde class_ssee/:    import sys; sys.path.insert(0, '../src'); import ssee_core

Verificación rápida:      python3 src/ssee_core.py
  (imprime todas las constantes y corre todos los asserts de cordura).
"""
import math
import os

# ── Constantes fundamentales ─────────────────────────────────────────────────
PHI = (1.0 + math.sqrt(5.0)) / 2.0          # razón áurea
PI  = math.pi

# ── Registros estructurales derivados (Paper 1) ──────────────────────────────
OMEGA = PHI + PI                # Stability Metric        ≈ 4.7596
BETA  = (PHI + PI) / 2.0        # Base Coupling Scalar    ≈ 2.3798
KAL0  = BETA + PI               # Structural Retention    ≈ 5.5214
P_SC  = OMEGA + PHI             # Dynamical Evolution     ≈ 6.3776
K_V   = PHI + PI + OMEGA        # Structural Constraint   ≈ 9.5192
T_R   = 3.0 * (PHI + BETA)      # 3D Saturation Horizon   ≈ 11.9935
M_V   = PHI + PI + K_V          # Maximal Dim. Invariant  ≈ 14.2788

# ── Ecuación de estado y densidades ──────────────────────────────────────────
W0          = -T_R / M_V        # ≈ -0.840
IGNIS       = PI + P_SC         # IGNIS = π+PYROS         ≈ 9.5192
WA          = -P_SC / IGNIS     # ≈ -0.670  (denominador IGNIS, NUNCA el
                                #  scaffold K_V: mismo valor 2Ω, otra entidad)
# ── SATURACIONES (Postulado S) — NO llevan H ─────────────────────────────────
# s = T_r/M_v es la fracción de SATURACIÓN, no una fracción de densidad. Vive en
# la ECUACIÓN DE ESTADO (w0 = -s), no en el reparto de densidades.
#
# ¿POR QUE s_DE ES IGUAL A |w0|? No es coincidencia ni descubrimiento: es UN
# SOLO numero. w0 se define como -T_r/M_v y s_DE como +T_r/M_v; el mismo
# cociente con el signo cambiado. Y T_r/M_v = AURA/Omega es una IDENTIDAD, no
# un parecido: T_r = 3*AURA y M_v = 3*Omega, el 3 se cancela (verificado a 40
# digitos, diferencia 0.0). Dos caminos de construccion, un numero.
#
# LO QUE SATURA ES w, NO UNA DENSIDAD. Corrida del fondo acoplado
# (results/logs/fondo_acoplado.npz), hoy y hacia el futuro:
#     a      w_eff      Om_DE
#   0.100  -0.117356  0.045301
#   0.500  -0.782020  0.308746
#   0.999  -0.839923  0.690471   <- hoy
#   1.499  -0.843395  0.853353
#   3.000  -0.841630  0.967397
# w_eff se planta en -0.8399 y ahi se queda: ESO es la saturacion. Om_DE pasa
# de largo por 0.839950 sin detenerse (entre a=1.5 y a=2) camino a 1. O sea:
# 0.839950 NO es la fraccion de densidad en NINGUNA epoca -- ni hoy (0.691119)
# ni en el futuro (-> 1). Es un numero de la ecuacion de estado y nada mas.
#
# REGLA PRACTICA: si lleva H, es densidad (OMEGA_M_TOTAL, 1-OMEGA_M_TOTAL). Si
# no lleva H, es saturacion (S_DE, S_M, S_K). Por eso S_DE nunca debe
# multiplicar a rho_crit ni diluirse como a^-3: vigilado por R52 y R52b.
#
# REGLA: donde una fórmula no puede llevar H adentro (f_screen es el caso
# canónico: H = H_SH0ES*(1 - f_screen) tendría dos H), va S_DE / S_M. Donde sí
# se reparte densidad real, va OMEGA_DE_DENS / OMEGA_M_TOTAL (ésas sí llevan H:
# Omega_m = omega_m/h²). Medido: con S_DE, f_screen es idéntico al último bit
# para anclas de 60 a 100; con la fracción de densidad se mueve.
S_DE        = T_R / M_V         # ≈ 0.839950  saturación DE (= |w0|)
OMEGA_DE    = S_DE              # [ALIAS DEPRECADO] usar S_DE; el nombre Omega_
                                #  sugiere densidad y ésta NO lo es
#
# ⚠️ REGLA DE Ω_m (2026-07-09, tras el hallazgo del χ²=726, V-L4-DESI):
#   La GEOMETRÍA de fondo — E(z), distancias BAO, H(z), r_d, cualquier E²(z) —
#   usa SIEMPRE la materia TOTAL:  OMEGA_M_TOTAL = ω_m/h² = 0.308881.
#   El 0.160 NO es una densidad de materia: es el SECTOR frío dinámico (1+w0),
#   componente de perturbaciones (Paper 6: 0.160 + φ-DM 0.149 = 0.308) y factor
#   de la fórmula EFT α_K = 3|w0|·0.160. NUNCA va en un E(z).
#   Meter el sector (0.160) en la geometría fue el bug que dio χ²=726 en DESI DR2.
S_M              = 1.0 + W0      # ≈ 0.160050  saturación complementaria (S_DE + S_M = 1)
OMEGA_CDM_SECTOR = S_M           # [ALIAS DEPRECADO] usar S_M; no es una densidad
OMEGA_M_DYN      = S_M           # [ALIAS DEPRECADO] si es geometría, usar OMEGA_M_TOTAL

# s_K — la cantidad que entra en f_screen. OJO: NO es alpha_K.
# alpha_K (kineticidad de Bellini-Sawicki) es 3*v²/KAL con v = dphi/d(ln a):
# EVOLUCIONA, hoy vale 0.150703 y tiende a 0.480148. Probado 2026-08-10 que no
# existe ninguna época donde el campo tenga a la vez las dos ranuras de s_K.
# s_K es PURO EoS: 3*(-w0)*(1+w0), sin ninguna densidad y sin H.
S_K = 3.0 * S_DE * S_M           # ≈ 0.403302  (antes mal llamado alpha_K_IR)

# ── MIRA / AURA ──────────────────────────────────────────────────────────────
# MIRA persiste como ENTIDAD (= AURA/2, valor 1.9989); conserva su rol en
# f_screen y la identidad AURA = 2·MIRA. Lo que se reasignó (reframe 2026-06-17)
# es su ROL de factor-materia → pasa a π/φ. Ver project_halg_pifi_investigation.
MIRA = (3.0*PHI + PI) / 4.0     # ≈ 1.9989  (entidad; f_screen; = AURA/2)
AURA = (3.0*PHI + PI) / 2.0     # ≈ 3.9978  (= 2*MIRA = PHI+BETA)

# ── Observables algebraicos de fondo ─────────────────────────────────────────
# DOS H, DOS NOMBRES (Mike, 2026-09-06 / 2026-09-28). NO son lo mismo:
#   H0_ALG    = 3(φ+π)² — NÚMERO PURO, sin unidades. Es el BLANCO contra el que
#               se compara la salida de la cascada. Nunca entra como H.
#   H0_GLOBAL = el H de SSEE (H global o geométrico), con unidades. SALE de la
#               cascada: SH0ES ENTRA (es el único H medido) y f_screen COMPLETO
#               (IR+UV, Paper 10) lo apantalla: H_glob = H_SH0ES·(1 − f_screen).
# Hasta 2026-09-28 aquí ponía H0_GLOBAL = H0_ALG: la cascada al revés. Coinciden
# a 4.2e-6, así que ningún número se movió, pero la ENTRADA estaba invertida.
H0_ALG       = 3.0 * OMEGA**2        # ≈ 67.96214  puro, sin unidades — el BLANCO
H0_SH0ES     = 73.04                 # km/s/Mpc  MEDIDO — Riess+2022 (ApJL 934 L7); ENTRADA
SIG_H0_SH0ES = 1.04                  # km/s/Mpc  — la misma fuente
ALPHA_ATT    = PHI**4 / 3.0          # α-attractor (Postulado I, Paper 1)
# s_K COMPLETO (Paper 10): raíz de 4X²/M⁴ + 2X/KAL₀ − s_K/3 = 0 con M⁴ = 45α²
# (unidades de ρ_crit), y s_K^full = s_K + 24X²/M⁴. Mismo cálculo que
# p10_uv/ssee_paper10_figures.py, ahora en un solo sitio.
_M4_UV       = 45.0 * ALPHA_ATT**2
_X_UV        = (-2.0/KAL0 + (4.0/KAL0**2 + 16.0*(S_K/3.0)/_M4_UV)**0.5) / (8.0/_M4_UV)
S_K_FULL     = S_K + 24.0 * _X_UV**2 / _M4_UV        # ≈ 0.41691
F_SCREEN     = S_K_FULL / (3.0 * MIRA)               # ≈ 0.069522  (IR+UV)
F_SCREEN_IR  = S_K / (3.0 * MIRA)                    # ≈ 0.06725   solo el término IR (régimen M→∞, Papers 1–9; NO canónico)
H0_GLOBAL    = H0_SH0ES * (1.0 - F_SCREEN)           # ≈ 67.962142 km/s/Mpc — EL H de SSEE
SIG_H0_GLOBAL = SIG_H0_SH0ES * (1.0 - F_SCREEN)      # ≈ 0.970 km/s/Mpc, propagado de SH0ES
H0_MIRA    = 67.037                  # ancla CMB-fit del escenario VIEJO (cascada pendiente re-run)
N_S        = 1.0 - PHI**(-7)         # ≈ 0.96556
R_TENSOR   = PHI**(-10)              # ≈ 0.00813
OMEGA_B_H2 = (PI - PHI) / (3.0 * OMEGA**2)   # ≈ 0.02242  (OP-1)
# ── Σm_ν activos — PREDICCIÓN ALGEBRAICA (Paper 4 §Neutrino Mass Sum) ────────
# Σm_ν = R₂·ω_b·C_ν/(τ_Π H₀), con C_ν=93.14 eV PDG (N_eff=3.046).
# 2026-09-05: el comentario de esta constante decía «= 40.70/594.28», es decir
# declaraba como procedencia la PARTÍCULA RETIRADA el 2026-08-01. El número es
# correcto, la atribución no: Σm_ν no cuelga de la partícula, cierra sola por
# álgebra. Quien siguiera la procedencia declarada aterrizaba en algo retirado.
#
# τ_Π H₀ = KAL₀/(3·S_DE) usa la SATURACIÓN (no lleva H), no la densidad
# Ω_DE=0.691119. No es cosmético: con la densidad daría Σm_ν=0.056354 eV,
# por DEBAJO del piso de oscilaciones 0.058 ⟹ la predicción quedaría falsada.
R2_STABILITY = OMEGA / (KAL0 * T_R)            # ≈ 0.071875  (razón de estabilidad)
TAU_PI_H0    = KAL0 / (3.0 * S_DE)             # ≈ 2.191  (tiempo de relajación IS)
SUM_MNU_EV = 0.06849                          # Σm_ν activos (canónico, 5 dec)
# CONTROL (R53): el álgebra tiene que reproducir el literal, y tiene que
# RECHAZAR la lectura de densidad. Si sólo comprobáramos lo primero, un cambio
# de símbolo pasaría inadvertido.
_smnu_alg = R2_STABILITY * OMEGA_B_H2 * 93.14 / TAU_PI_H0
_smnu_dens = R2_STABILITY * OMEGA_B_H2 * 93.14 / (KAL0 / (3.0 * 0.691119))
assert abs(_smnu_alg - SUM_MNU_EV) < 1e-5, (
    f"Sigma m_nu algebraico {_smnu_alg} != literal {SUM_MNU_EV}")
assert _smnu_dens < 0.058, (
    "el control se rompio: la lectura de densidad deberia caer bajo el "
    f"piso de oscilaciones 0.058, y da {_smnu_dens}")

# ── Densidad de materia CMB — ω_m DIRECTO (reframe 2026-06-18) ────────────────
# OP-8 CERRADO: no hay "factor materia" que derivar. Ω_m,CMB es el observable
# físico estándar ω_m/h², con cada pieza algebraica de SSEE:
#   ω_b = (π-φ)/(3Ω²)              (OP-1)
#   ω_c = KAL₀·ω_b·n_s            (identidad forward, ya en Paper 1; 0.41σ)
#   ω_ν = Σm_ν/93.14 eV           (neutrinos activos)
# Ω_m,CMB = ω_m/h² es DERIVADO, no postulado. El viejo factor π/φ (y antes MIRA)
# queda RETIRADO: Ω_m,dyn=0.160 (DESI) y ω_m (CMB) son dos predicciones
# independientes, ya no ligadas por un factor. Ver project_halg_pifi_investigation.
OMEGA_C_H2 = KAL0 * OMEGA_B_H2 * N_S           # ≈ 0.11952  (forward, Paper 1)
OMEGA_NU_H2 = SUM_MNU_EV / 93.14               # ≈ 0.000735
OMEGA_M_H2 = OMEGA_B_H2 + OMEGA_C_H2 + OMEGA_NU_H2   # ≈ 0.14268  (ω_m físico)
# MATERIA TOTAL — la ÚNICA densidad que entra en cualquier geometría de fondo:
OMEGA_M_TOTAL = OMEGA_M_H2 / (H0_GLOBAL/100.0)**2    # ≈ 0.308881  (CANÓNICO, derivado, ω_m/h²)
OMEGA_M_CMB   = OMEGA_M_TOTAL                         # [ALIAS] mismo número; usar OMEGA_M_TOTAL
# Identidades históricas (RETIRADAS como factor-materia, conservadas para trazar):
OMEGA_M_CMB_PIPHI     = (PI / PHI) * OMEGA_CDM_SECTOR # ≈ 0.31069  (factor π/φ — superado)
OMEGA_M_CMB_MIRA      = MIRA * OMEGA_CDM_SECTOR       # ≈ 0.31983  (identidad MIRA — histórico)
OMEGA_M_CMB_GEOMETRIC = (PI - PHI) / (PI + PHI)      # ≈ 0.32010  (geométrico)

# ── Valores ΛCDM de referencia (Planck 2018, A&A 641 A6) ─────────────────────
LCDM_OMEGA_M = 0.3153
LCDM_H0      = 67.36
LCDM_SIGMA8  = 0.8111
LCDM_NS      = 0.9649

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         '..', 'data', 'raw')


# ── Fondo de Friedmann — ÚNICA implementación válida ─────────────────────────
def friedmann_E2(a, Omega_m, Omega_de=None, w0=W0, wa=WA, Omega_r=0.0):
    """E²(a) = H²(a)/H₀² para un fondo con energía oscura CPL.

    Si Omega_de se omite, se fija a 1 - Omega_m - Omega_r, de modo que
    Σ Ω = 1 por construcción y E²(a=1) == 1 SIEMPRE. El bug de Paper 6
    (E²(z=0)=1.16) vino de pasar Omega_m=0.320 y Omega_de=0.840 a la vez:
    nunca pasar ambos salvo que su suma + Omega_r sea exactamente 1.
    """
    if Omega_de is None:
        Omega_de = 1.0 - Omega_m - Omega_r
    f_de = a**(-3.0*(1.0 + w0 + wa)) * math.exp(-3.0*wa*(1.0 - a))
    return Omega_r*a**-4 + Omega_m*a**-3 + Omega_de*f_de


# ── Cargadores de datos observacionales (con procedencia en el archivo) ──────
def load_fsigma8():
    """Devuelve la lista canónica fσ₈(z): dicts z, fsigma8, sigma, survey, ref."""
    path = os.path.join(_DATA_DIR, 'fsigma8_rsd.csv')
    rows = []
    with open(path) as fh:
        header = None
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if header is None:
                header = line.split(',')
                continue
            vals = line.split(',')
            row = dict(zip(header, vals))
            rows.append({
                'z':       float(row['z_eff']),
                'fsigma8': float(row['fsigma8']),
                'sigma':   float(row['sigma']),
                'survey':  row['survey'],
                'ref':     row['reference'],
            })
    return rows


# ── Asserts de cordura — corren al importar el módulo ────────────────────────
def _sanity_checks():
    assert abs(PHI**2 - (PHI + 1.0)) < 1e-12, "identidad áurea phi^2=phi+1 rota"
    assert abs(AURA - 2.0*MIRA) < 1e-12,      "AURA debe ser 2*MIRA"
    assert abs(S_M + S_DE - 1.0) < 1e-12, "las dos saturaciones deben sumar 1"
    assert abs(S_K - 3.0 * S_DE * S_M) < 1e-15, "s_K debe ser 3*S_DE*S_M"
    assert abs(S_K / (3.0 * MIRA) - (PI - PHI) / OMEGA**2) < 1e-12, \
        "f_screen = s_K/(3*MIRA) debe ser (pi-phi)/Omega^2 exacto"
    assert round(W0, 3) == -0.840,  f"w0 fuera de rango: {W0}"
    assert round(WA, 3) == -0.670,  f"wa fuera de rango: {WA}"
    assert round(OMEGA_CDM_SECTOR, 3) == 0.160, f"sector frío fuera de rango: {OMEGA_CDM_SECTOR}"
    assert OMEGA_M_DYN == OMEGA_CDM_SECTOR, "alias OMEGA_M_DYN roto"
    assert 0.0 < N_S < 1.0,         f"n_s no físico: {N_S}"
    assert 66.0 < H0_ALG < 69.0,    f"H0_alg fuera de rango: {H0_ALG}"
    # la salida de la cascada contra el blanco puro (residuo publicado +4.2e-06)
    assert abs(H0_GLOBAL - H0_ALG) < 1e-5, f"cascada vs blanco: {H0_GLOBAL - H0_ALG:+.3e}"
    assert H0_GLOBAL is not H0_ALG, "H0_GLOBAL tiene que SALIR de la cascada, no ser el blanco"
    assert abs(friedmann_E2(1.0, OMEGA_CDM_SECTOR) - 1.0) < 1e-9, "E^2(a=1) != 1 (sector)"
    assert abs(friedmann_E2(1.0, OMEGA_M_TOTAL) - 1.0) < 1e-9, "E^2(a=1) != 1 (total)"
    assert round(OMEGA_M_TOTAL, 4) == 0.3089, f"Omega_m,total (ω_m/h²) fuera de rango: {OMEGA_M_TOTAL}"
    assert OMEGA_M_CMB == OMEGA_M_TOTAL, "alias OMEGA_M_CMB roto"
    assert abs(OMEGA_M_TOTAL - OMEGA_M_H2 / (H0_GLOBAL/100.0)**2) < 1e-12, "Omega_m,total debe ser ω_m/h²"
    assert round(OMEGA_M_H2, 4) == 0.1427, f"ω_m algebraico fuera de rango: {OMEGA_M_H2}"
    # Ω_m,CMB reproducible en 3 s: los TRES términos son necesarios.
    # Omitir ω_ν devuelve 0.30729 (no 0.308881) — el ν NO es opcional (Sealed §two-omega).
    _h2 = (H0_GLOBAL / 100.0) ** 2
    _om_sin_nu = (OMEGA_B_H2 + OMEGA_C_H2) / _h2
    # ORIGEN-VALOR: 0.3073 — (omega_b + omega_c)/h^2 = 0.307289, calculado aqui mismo (_om_sin_nu), a 4 decimales
    # ORIGEN-VALOR: 0.30729 — el mismo (omega_b + omega_c)/h^2 = 0.307289 a 5 decimales
    assert round(_om_sin_nu, 4) == 0.3073, \
        f"Ω_m,CMB sin ω_ν debe dar ~0.30729 (ν no opcional): {_om_sin_nu}"
    assert round((OMEGA_B_H2 + OMEGA_C_H2 + OMEGA_NU_H2) / _h2, 4) == 0.3089, \
        "Ω_m,CMB con los tres términos debe dar 0.308881"
    assert abs(OMEGA_C_H2 - KAL0 * OMEGA_B_H2 * N_S) < 1e-12, "ω_c debe ser KAL₀·ω_b·n_s"


_sanity_checks()


def check():
    """Imprime todas las constantes y confirma los asserts. Paso de auditoría."""
    print("=" * 64)
    print("ssee_core.py — constantes canónicas SSEE")
    print("=" * 64)
    for name in ('PHI', 'PI', 'OMEGA', 'BETA', 'KAL0', 'P_SC', 'K_V', 'T_R',
                 'M_V', 'W0', 'WA', 'S_DE', 'S_M', 'S_K', 'OMEGA_M_TOTAL',
                 'MIRA', 'AURA',
                 'OMEGA_B_H2', 'OMEGA_C_H2', 'OMEGA_NU_H2', 'OMEGA_M_H2',
                 'OMEGA_M_CMB', 'OMEGA_M_CMB_PIPHI', 'OMEGA_M_CMB_MIRA',
                 'OMEGA_M_CMB_GEOMETRIC', 'H0_ALG', 'H0_GLOBAL', 'SIG_H0_GLOBAL', 'H0_SH0ES', 'F_SCREEN', 'S_K_FULL', 'N_S',
                 'R_TENSOR', 'SUM_MNU_EV'):
        print(f"  {name:24s} = {globals()[name]:.10f}")
    fs = load_fsigma8()
    print(f"\n  fsigma8 canónico: {len(fs)} puntos "
          f"(z={fs[0]['z']}..{fs[-1]['z']}, surveys {sorted(set(r['survey'] for r in fs))})")
    _sanity_checks()
    print("\n  Todos los asserts de cordura: OK")


if __name__ == '__main__':
    check()
