#!/usr/bin/env python3
"""algebra_derivada.py — el ALGEBRA que los papers imprimen y el nucleo no nombra.

POR QUE (2026-09-30). Los papers escriben combinaciones de phi y pi (2 phi^7 =
58.068884, phi^-10 = 8.130619e-3, sqrt(AURA), 3 Omega_DE (5 - 3 w0), ...) a mano.
Tienen fuente —el algebra—, pero nada las calculaba en un sitio que alguien
pudiera abrir, y a mano se cuelan errores: al armar esta tabla salieron
sqrt(AURA) = 1.99947 en Paper 8 (es 1.999462), 8.663001 y 10.281034 en la tabla
de Paper 4 (son 8.662999 y 10.281033) y alpha_K = 15.591335 en 22 sitios (con
el H de hoy es 15.591336: Omega_m = omega_m / h^2 y h cambio el 09-28).

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
    "r_staro":        ("3/PHI**14", "r de Starobinsky con N = 2 phi^7"),
    "dos_phi6":       ("2*PHI**6", "ventana de e-folds, Paper 1"),
    "dos_phi7":       ("2*PHI**7", "N_* = 2 phi^7"),
    "dos_phi8":       ("2*PHI**8", "ventana de e-folds, Paper 1"),
    "N_star_rh":      ("58.25-math.log(3)/6", "N_* con rho_rh = V_end, Paper 4"),   # ORIGEN-VALOR: 58.25 — N_* de referencia de Paper 4 (Liddle-Leach con rho_rh = V_end)
    "sqrt_AURA":      ("math.sqrt(AURA)", "deflexion del limite MOND-like, Paper 8"),
    "cuatro_AURA":    ("4*AURA", "CUARTAL, tabla de Paper 7"),
    "inv_phi":        ("1/PHI", "gamma algebraico = phi^-1"),
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
}
try:
    eval("1/(1+W0-1-W0)", {}, N)
    roto = False
except ZeroDivisionError:
    roto = True
out = dict(fecha=str(__import__("datetime").date.today()), algebra=res,
           control=dict(identidades=ctl, pasa=bool(all(v < 1e-12 for v in ctl.values()) and roto and not errores),
                        formula_rota_falla=roto, errores=errores))
json.dump(con_acta(out, __file__), open(os.path.join(_R, "results", "logs", "algebra_derivada.json"), "w"), indent=1)
print(f"  {len(res)} valores · identidades {ctl} · formula rota falla: {roto} · errores {errores}")
print(f"  control: {'PASA' if out['control']['pasa'] else 'NO PASA'}")
