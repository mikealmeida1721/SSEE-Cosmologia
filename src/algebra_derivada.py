#!/usr/bin/env python3
"""algebra_derivada.py — el ALGEBRA que los papers imprimen y el nucleo no nombra.

POR QUE (2026-09-30). Los papers escriben combinaciones de phi y pi (2 phi^7,
phi^-10, sqrt(AURA), 3 Omega_DE (5 - 3 w0), ...) a mano. Tienen fuente —el
algebra—, pero nada las calculaba en un sitio que alguien pudiera abrir, y a
mano se cuelan errores: al armar esta tabla salieron mal la ultima cifra de
sqrt(AURA) en Paper 8, dos celdas de la tabla de Paper 4 (pi+KAL y
phi+pi+KAL) y alpha_K en 22 sitios (calculado con el H viejo: Omega_m =
omega_m / h^2 y h cambio el 09-28). Los valores buenos estan en el log; los
malos, en migra_a_val.CORRIGE.

Cada entrada: nombre, formula sobre ssee_core y para que se usa. Este script
evalua todas y escribe results/logs/algebra_derivada.json (con acta); los
papers las imprimen con \\val{nombre} via manuscript/valores.yaml.

CONTROL (R53): las identidades que el algebra exige (u por sus dos formas
cerradas, AURA = 2 MIRA, n por sus dos formas) tienen que cumplirse a 1e-12; y
una entrada con formula rota (division por cero) tiene que fallar ruidosa.
"""
import json
import math
import os
import sys

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(_R, "src"))
import ssee_core as S  # noqa: E402
from procedencia import con_acta  # noqa: E402

N = {k: getattr(S, k) for k in dir(S) if k.isupper()}
N["math"] = math
N["OMDE_DENS"] = 1.0 - S.OMEGA_M_TOTAL      # Omega_DE como DENSIDAD (no la saturacion S_DE)

ALGEBRA = {
    # nombre: (formula, uso)
    "alpha_K_z0":     ("3*OMDE_DENS*(5-3*W0)", "kineticidad hoy, Paper 7 y resumenes"),
    "x_K":            ("3*(5-3*W0)", "alpha_K(a) = x_K Omega_DE(a), Paper 7"),
    "r_tensor":       ("PHI**-10", "tensor-escalar r = phi^-10"),
    "r_tensor_mil":   ("1e3*PHI**-10", "r en unidades de 10^-3 (como lo escriben los papers)"),
    "r_staro":        ("3/PHI**14", "r de Starobinsky con N = 2 phi^7"),
    "dos_phi6":       ("2*PHI**6", "ventana de e-folds, Paper 1"),
    "dos_phi7":       ("2*PHI**7", "N_* = 2 phi^7"),
    "dos_phi8":       ("2*PHI**8", "ventana de e-folds, Paper 1"),
    "N_star_rh":      ("58.25-math.log(3)/6", "N_* con rho_rh = V_end, Paper 4"),   # ORIGEN-VALOR: 58.25 — N_* de referencia de Paper 4 (Liddle-Leach con rho_rh = V_end)
    "sqrt_AURA":      ("math.sqrt(AURA)", "deflexion del limite MOND-like, Paper 8"),
    "cuatro_AURA":    ("4*AURA", "CUARTAL, tabla de Paper 7"),
    "inv_phi":        ("1/PHI", "gamma algebraico = phi^-1"),
    "dos_AURA":       ("2*AURA", "DUAL, tabla de Paper 7"),
    "tres_MIRA":      ("3*MIRA", "3 MIRA = 3 AURA/2, Paper 9"),
    "sqrtAURA_MIRA":  ("math.sqrt(AURA)/MIRA", "sqrt(beta_c)/MIRA con beta_c = AURA, Paper 8"),
    "seis_alfa_KAL2": ("6*ALPHA_ATT*KAL0**2", "M^4 de la Ruta A en rho_crit, Paper 10"),
    "X_UV_sobre_IR":  ("_X_UV/(S_K*KAL0/6)", "X_bg UV / IR, Paper 10"),
    "c2X_c1_KX":      ("_X_UV*KAL0/_M4_UV", "c2 X / c1 del K(X) de Paper 10 (1/KAL0, 1/M^4)"),
    "M_meV_rhoLambda": ("(5*PHI**8)**0.25*2.25", "M con la escala LCDM rho_Lambda^(1/4) = 2.25 meV: la INCONSISTENTE que Paper 10 descarta"),   # ORIGEN-VALOR: 2.25 — rho_Lambda^(1/4) en meV de LCDM, el valor que Paper 10 cita para descartarlo
    "inv_1pw0":       ("1/(1+W0)", "entalpia rho+p en unidades de rho_DE(1+w0)"),
    "inv_1pw0_m1":    ("1/(1+W0)-1", "c_s^2 efectivo del intento descartado, Paper 5"),
    "MIRA_m1":        ("MIRA-1", "Paper 5 Q2"),
    "n_ssee":         ("(1+W0)/(2*W0)", "exponente n, seccion EFT"),
    "n_ssee_TM":      ("(T_R-M_V)/(2*T_R)", "la misma n por T_r, M_v (control)"),
    "wa_viejo":       ("-3*WA", "w_a con Gamma = w_a (version retirada), seccion EFT"),
    "u_condensado":   ("(1-W0)/(3*W0-1)", "u del condensado, Paper 7"),
    "u_condensado_TM": ("-(M_V+T_R)/(3*T_R+M_V)", "la misma u por T_r, M_v (control)"),
    "uno_mas_3u":     ("1+3*(1-W0)/(3*W0-1)", "Paper 7"),
    "uno_mas_6u":     ("1+6*(1-W0)/(3*W0-1)", "Paper 7 (no-ghost)"),
    "uno_mas_2u":     ("1+2*(1-W0)/(3*W0-1)", "Paper 7 (NEC)"),
    "X_sobre_Xmin":   ("-2*(1-W0)/(3*W0-1)", "punto del condensado, Paper 7"),
    "phi_mas_2pi":    ("PHI+2*PI", "SOLAR = MAR, Papers 1 y 4"),
    "pi_mas_KAL":     ("PI+KAL0", "tabla de Paper 4"),
    "phi_pi_KAL":     ("PHI+PI+KAL0", "tabla de Paper 4"),
    "dos_Omega_phi":  ("2*OMEGA+PHI", "tabla de Paper 4"),
    "dos_phi_":       ("2*PHI", "Sealed / PRD"),
    "SOLAR_NYX":      ("(PHI+2*PI)/((PHI+7*PI)/2)", "Sealed / PRD"),
    "KAL_KALeff":     ("KAL0/(PHI**2*math.sqrt(5/2))", "Paper 10, Ruta A"),
    "KAL_KALeff2":    ("(KAL0/(PHI**2*math.sqrt(5/2)))**2", "Paper 10, Ruta A"),
    "inv_S_M":        ("1/S_M", "agrupamiento pleno 1/Omega_m,dyn, Paper 5"),
    "sK_tercio":      ("S_K/3", "rho_phi(1+w0) en rho_crit = 1, Paper 10"),
    "X_bg_IR":        ("S_K*KAL0/6", "X_bg IR en rho_crit = 1, Paper 10"),
    "cs2_condensado": ("(1+W0)/(5-3*W0)", "c_s^2 del condensado, Paper 7"),
    "cs2_condensado_TM": ("(M_V-T_R)/(5*M_V+3*T_R)", "la misma c_s^2 por T_r, M_v (control)"),
    "sK_con_KX_de_P7": ("3*(5-3*W0)*S_DE", "6(XK_X+2X^2K_XX) con la K(X) de Paper 7 y rho_phi = S_DE (Paper 10, las dos K(X))"),
    "sK_con_KX_de_P7_c1": ("6*S_DE/(1+3*(1-W0)/(3*W0-1))*(1+6*(1-W0)/(3*W0-1))", "lo mismo desde c1 X y u (control)"),
    "factor_dos_KX":  ("3*(5-3*W0)*S_DE/S_K_FULL", "cociente contra s_K completo de Paper 10"),
    "wc_estatico_planck": ("KAL0*0.02237", "Omega_c h^2 = KAL0 * omega_b(Planck), relacion estatica de Paper 4"),   # ORIGEN-VALOR: 0.02237 — omega_b de Planck 2018 VI Tabla 2, la entrada que declara Paper 4
    "wc_estatico_sigma": ("(KAL0*0.02237-0.1200)/0.0012", "distancia a Planck 0.1200 +- 0.0012, Paper 4"),   # ORIGEN-VALOR: 0.02237, 0.1200, 0.0012 — Planck 2018 VI Tabla 2
    "wc_estatico_ssee": ("KAL0*OMEGA_B_H2", "Omega_c h^2 estatico con el omega_b PROPIO de SSEE (2026-10-01: Paper 4 usaba el de Planck, ingrediente de otro modelo)"),
    "wc_estatico_ssee_sigma": ("(KAL0*OMEGA_B_H2-0.1200)/0.0012", "su distancia a Planck"),   # ORIGEN-VALOR: 0.1200, 0.0012 — Planck 2018 VI Tabla 2
    "wc_ns_sigma":    ("(OMEGA_C_H2-0.1200)/0.0012", "omega_c = KAL0 omega_b n_s frente a Planck"),   # ORIGEN-VALOR: 0.1200, 0.0012 — Planck 2018 VI Tabla 2
    "Yp_ssee":        ("0.2471+0.96*(OMEGA_B_H2-0.02237)", "Y_p lineal, Paper 4"),   # ORIGEN-VALOR: 0.2471 y 0.02237 — ancla Planck 2018; 0.96 — dY_p/d(omega_b) de AlterBBN (Pisanti 2008)
    "Omega_b_alg":    ("OMEGA_B_H2/(H0_ALG/100)**2", "Omega_b = omega_b/h^2 con h = 3 Omega^2/100, Paper 4"),
    "Omega_b_alg_cerrada": ("1e4*(PI-PHI)/(27*OMEGA**6)", "la misma en forma cerrada (control)"),
    "horizonte_cs_Mpc": ("math.sqrt((1+W0)/(5-3*W0))*299792.458/H0_GLOBAL", "horizonte sonoro c_s c/H0 del condensado, Paper 7"),   # ORIGEN-VALOR: 299792.458 — c en km/s (definicion SI)
}

res, errores = {}, []
for k, (f, uso) in ALGEBRA.items():
    try:
        res[k] = dict(formula=f, valor=float(eval(f, {}, N)), uso=uso)
    except Exception as e:
        errores.append(f"{k}: {e}")
ctl = {
    "u dos formas": abs(res["u_condensado"]["valor"] - res["u_condensado_TM"]["valor"]),
    "n dos formas": abs(res["n_ssee"]["valor"] - res["n_ssee_TM"]["valor"]),
    "AURA = 2 MIRA": abs(S.AURA - 2 * S.MIRA),
    "s_K con K(X) de P7, dos formas": abs(res["sK_con_KX_de_P7"]["valor"] - res["sK_con_KX_de_P7_c1"]["valor"]),
    "Omega_b dos formas": abs(res["Omega_b_alg"]["valor"] - res["Omega_b_alg_cerrada"]["valor"]),
    "c_s^2 dos formas": abs(res["cs2_condensado"]["valor"] - res["cs2_condensado_TM"]["valor"]),
}
try:
    eval("1/(1+W0-1-W0)", {}, N)
    roto = False
except ZeroDivisionError:
    roto = True
# El nucleo tambien, evaluado: los papers imprimen el valor de K_V, no la formula.
nucleo = {k: float(v) for k, v in N.items()
          if k.isupper() and isinstance(v, (int, float)) and not isinstance(v, bool)}
out = dict(fecha=str(__import__("datetime").date.today()), algebra=res, nucleo=nucleo,
           control=dict(identidades=ctl, pasa=bool(all(v < 1e-12 for v in ctl.values()) and roto and not errores),
                        formula_rota_falla=roto, errores=errores))
json.dump(con_acta(out, __file__), open(os.path.join(_R, "results", "logs", "algebra_derivada.json"), "w"), indent=1)
print(f"  {len(res)} valores · identidades {ctl} · formula rota falla: {roto} · errores {errores}")
print(f"  control: {'PASA' if out['control']['pasa'] else 'NO PASA'}")
