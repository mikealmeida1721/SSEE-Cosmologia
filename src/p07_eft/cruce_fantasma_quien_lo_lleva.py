#!/usr/bin/env python3
"""
¿Quién puede llevar el cruce fantasma de SSEE?  (2026-09-27, pregunta de M. Almeida)

El CPL algebraico (w0, wa) cruza w = -1 en a* = 1 + (1+w0)/wa  (z ≈ 0.31).
Paper 1 dice que el cruce «no señala inestabilidad en la acción» y que la
presión viscosa Π lo compensa; Paper 7 dice que c_s² cambia de signo en el
cruce. Los dos hablan de OBJETOS distintos, y cada uno se prueba aparte:

  A. EL CAMPO. K(X) = c1 X + c2 X² (Paper 7). Se derivan w y c_s² por
     diferencias finitas de K —no con la fórmula cerrada— y se barre u = c2X/c1.
     Pregunta: ¿puede el campo tener w < -1 sin c_s² < 0?

  B. LA PRESIÓN VISCOSA. El campo se queda en w_φ = w0 (lo que P7 produce) y
     el cruce lo pone Π. Con la normalización de OP-22 (Π ∝ ρ+p, entalpía):
        1 + w_eff = (1 + w0)(1 - c(a)),   c = |Π|/(ρ+p)
     Pregunta: ¿qué c(a) exige reproducir el CPL, y cuánto vale donde hay cruce?

Controles (R53): A debe devolver w(u0) = w0 y c_s²(u0) = 0.021284 en el
u0 = -(M_v+T_r)/(3T_r+M_v) de Paper 7, y c_s² = 0 en w = -1. B debe dar
c(a*) = 1 exacto: el cruce ES el punto donde la viscosa iguala a la entalpía.

Salida: results/logs/cruce_fantasma_quien_lo_lleva.json
"""
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
import ssee_core as S                                   # noqa: E402

SALIDA = REPO / "results" / "logs" / "cruce_fantasma_quien_lo_lleva.json"
W0, WA = S.W0, S.WA

# ---------------------------------------------------------------- A. el campo
C1 = -1.0          # signo de P7 (c1 < 0, c2 > 0: ghost condensate); la escala no entra en w ni c_s²
X = 1.0            # u = c2 X / c1 se barre moviendo c2 con X fijo


def K(x, c2):
    return C1 * x + c2 * x * x


def derivadas(c2, h=1e-5):
    kx = (K(X + h, c2) - K(X - h, c2)) / (2 * h)
    kxx = (K(X + h, c2) - 2 * K(X, c2) + K(X - h, c2)) / h ** 2
    return kx, kxx


def campo(u):
    c2 = u * C1 / X
    kx, kxx = derivadas(c2)
    p = K(X, c2)
    rho = 2 * X * kx - p
    w = p / rho
    cs2 = kx / (kx + 2 * X * kxx)
    sin_fantasma = (kx + 2 * X * kxx) * np.sign(C1) > 0     # misma condición de no-fantasma que P7 con c1<0
    return w, cs2, bool(sin_fantasma)


U0 = -(S.M_V + S.T_R) / (3 * S.T_R + S.M_V)
w_u0, cs2_u0, _ = campo(U0)
w_m1, cs2_m1, _ = campo(-0.5)                  # u = -1/2 da w = -1 exacto
control_A = {
    "u0_P7": U0, "w(u0)": w_u0, "w0": W0,
    "cs2(u0)": cs2_u0, "cs2_P7": 0.021284,
    "cs2_en_w_menos_1": cs2_m1,
    "pasa": bool(abs(w_u0 - W0) < 1e-8 and abs(round(cs2_u0, 6) - 0.021284) < 1e-12 and abs(cs2_m1) < 1e-8),
}

barrido = []
for u in np.linspace(-0.60, -0.45, 31):
    w, cs2, ok = campo(u)
    barrido.append({"u": float(u), "w": float(w), "cs2": float(cs2),
                    "cs2_formula": float((1 + w) / (5 - 3 * w)),
                    "sin_fantasma": ok})
fantasmas = [b for b in barrido if b["w"] < -1 - 1e-9]
resultado_A = {
    "puntos_con_w_menor_que_menos_1": len(fantasmas),
    "de_ellos_con_cs2_positivo": sum(b["cs2"] > 0 for b in fantasmas),
    "max_dif_cs2_numerico_vs_formula": max(abs(b["cs2"] - b["cs2_formula"]) for b in barrido),
    "lectura": "todo w<-1 del campo tiene c_s^2<0 (inestabilidad de gradiente): el campo de P7 NO puede llevar el cruce",
}

# ---------------------------------------------------- B. la presión viscosa
A_STAR = 1 + (1 + W0) / WA
Z_STAR = 1 / A_STAR - 1


def c_entalpia(a):
    """c(a) = |Π|/(ρ+p) que hace 1+w_eff=(1+w0)(1-c) igual a 1+w0+wa(1-a)."""
    return -WA * (1 - a) / (1 + W0)


control_B = {"a_star": A_STAR, "z_star": Z_STAR, "c(a_star)": c_entalpia(A_STAR),
             "pasa": bool(abs(c_entalpia(A_STAR) - 1) < 1e-12)}
tabla_B = []
for z in (0.0, 0.1, 0.2, Z_STAR, 0.5, 0.75, 1.0, 1.5, 2.33):
    a = 1 / (1 + z)
    tabla_B.append({"z": z, "c=|Pi|/(rho+p)": c_entalpia(a),
                    "Pi/rho_DE (=wa(1-a))": WA * (1 - a),
                    "w_eff": W0 + WA * (1 - a)})
resultado_B = {
    "pendiente_dc_d(1-a)": -WA / (1 + W0),
    "lectura": ("con Π ∝ ρ+p, el cruce exige |Π| = ρ+p en z*, y |Π| > ρ+p en todo z > z*: "
                "la corrección viscosa supera a la entalpía que corrige. Si eso cae dentro o fuera "
                "de la validez de Israel-Stewart es la prueba que decide si P1 puede ser cierto."),
}

res = {
    "corrida": "quien puede llevar el cruce fantasma de SSEE",
    "pregunta": "M. Almeida (2026-09-27): P1 dice que el cruce no es inestable, P7 que c_s^2 cambia de signo; ver cual es cierta con pruebas",
    "fuentes": {"W0": "ssee_core.W0", "WA": "ssee_core.WA", "M_V,T_R": "ssee_core",
                "u0 y cs2=0.021284": "Paper 7 (manuscript/SSEE_Paper7_EFT.tex, abstract)"},
    "A_campo": {"control": control_A, "resultado": resultado_A, "barrido": barrido},
    "B_viscosa_entalpia": {"control": control_B, "tabla": tabla_B, "resultado": resultado_B},
}
SALIDA.write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps({k: v for k, v in res.items() if k in ("A_campo", "B_viscosa_entalpia")},
                 indent=1, ensure_ascii=False, default=float)[:3500])
print("->", SALIDA)
