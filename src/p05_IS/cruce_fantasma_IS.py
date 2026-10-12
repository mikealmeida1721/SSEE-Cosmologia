#!/usr/bin/env python3
"""OP-24, la pregunta que quedó abierta (2026-10-11): ¿cabe el cruce fantasma
de SSEE dentro de Israel–Stewart, y lo atraviesan las perturbaciones?

Cierre de Paper 1 (§phantom crossing): el campo de Paper 7 lleva w₀ (> −1) y
la presión viscosa de fondo Π lleva el resto,
    1 + w_eff = (1 + w₀)(1 − c),   c = |Π|/(ρ+p)_campo = −w_a(1−a)/(1+w₀).

(a) VALIDEZ. La teoría IS lineal (truncada) es de cerca del equilibrio:
    |Π| ≪ |p| (p = presión de equilibrio). Se mide |Π|/|p| = |w_a|(1−a)/|w₀|
    y |Π|/ρ = |w_a|(1−a). El régimen |Π| ~ |p| es el de la extensión NO lineal
    de Maartens & Méndez (1997, PRD 55, 1937), donde ya hay soluciones
    fantasma (Cruz & Lepe 2017, PLB; Cruz, Cruz & Lepe 2017, PLB 769, 159).
    Segunda ley: ζ = ζ̃ ρ(1+w₀)/H₀ > 0 en toda la historia (normalizada a la
    entalpía del CAMPO), así que la producción de entropía Π²/(ζT) ≥ 0 no
    cambia de signo en el cruce.
(b) PERTURBACIONES con la inercia TOTAL (1+w_eff, que cruza el cero), en la
    variable U = (1+w)θ/k de Kunz & Sapone (2006, PRD 74, 123503): regular en
    w = −1 si δp se fija finita fuera del sistema en reposo (aquí:
    δp = ĉ²δρ + 3ℋ(ĉ²−w)ρU/k, sin el término ẇ/(1+w) del sistema en reposo).
    ĉ² = c²_s del campo de Paper 7. Control: con ĉ² = w₀ crece.

H₀ = c = 1, d/d ln a. w_eff(a) = CPL (w₀, w_a).
"""
import json
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
import ssee_core as S  # noqa: E402
from procedencia import cabecera, con_acta  # noqa: E402
print(cabecera(__file__), flush=True)

W0, WA, OM = S.W0, S.WA, S.OMEGA_M_TOTAL
OD = 1.0 - OM
CS2_CAMPO = (1 + W0) / (5 - 3 * W0)
A_CRUCE = 1 + (1 + W0) / WA


def fde(a):
    return a**(-3 * (1 + W0 + WA)) * np.exp(-3 * WA * (1 - a))


def H(a):
    return np.sqrt(OM * a**-3 + OD * fde(a))


def validez(z):
    a = 1 / (1 + z)
    return dict(z=z, c=-WA * (1 - a) / (1 + W0), Pi_sobre_rho=-WA * (1 - a),
                Pi_sobre_p=-WA * (1 - a) / abs(W0), w_eff=W0 + WA * (1 - a))


def rhs(x, Y, k, c2):
    a = np.exp(x)
    h = H(a)
    w = W0 + WA * (1 - a)
    dm, vm, dd, U = Y
    psi = -(1.5 / k**2) * (OM * dm / a + a**2 * OD * fde(a) * dd)
    kH = k / (a * h)
    ddd = -kH * U - 3 * (c2 - w) * dd - 9 * (c2 - w) * U / kH
    dU = -(1 - 3 * c2) * U + kH * c2 * dd + (1 + w) * kH * psi
    return [-kH * vm, -vm + kH * psi, ddd, dU]


def integra(k, c2, a_ini=0.05):
    Y0 = [a_ini, -a_ini * a_ini * H(a_ini) / k, 0.0, 0.0]
    s = solve_ivp(rhs, [np.log(a_ini), 0.0], Y0, args=(k, c2),
                  method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
    x_c = np.log(A_CRUCE)
    yc = s.sol(x_c)
    dm, _, dd, _ = s.y[:, -1]
    return dict(k=k, exito=bool(s.success), delta_m=float(dm), r=float(dd / dm),
                r_en_cruce=float(yc[2] / yc[0]),
                finito=bool(np.all(np.isfinite(s.y))))


def main():
    zs = [0.0, 1 / A_CRUCE - 1, 0.5, 1.0, 2.33]
    tabla = [validez(z) for z in zs]
    ks = [2.0, 5.0, 10.0, 20.0, 50.0, 100.0]
    campo = [integra(k, CS2_CAMPO) for k in ks]
    control = [integra(k, W0) for k in ks]
    ctrl_cruce = abs(validez(1 / A_CRUCE - 1)["c"] - 1) < 1e-12
    ctrl_wcruce = abs(validez(1 / A_CRUCE - 1)["w_eff"] + 1) < 1e-12
    out = dict(
        pregunta="OP-24: cabe el cruce fantasma en IS y lo atraviesan las perturbaciones",
        a_cruce=A_CRUCE, z_cruce=1 / A_CRUCE - 1, cs2_campo=CS2_CAMPO,
        validez=tabla,
        criterio_IS_lineal="|Pi| << |p| (cerca del equilibrio); |Pi| ~ |p| = IS no lineal (Maartens & Mendez 1997)",
        perturbaciones_campo=campo,
        control_c2_w0=control,
        controles=dict(c_igual_1_en_cruce=ctrl_cruce, w_eff_igual_menos1_en_cruce=ctrl_wcruce,
                       campo_finito=all(f["finito"] and f["exito"] for f in campo),
                       control_crece=control[-1]["r"] > 1.0),
    )
    p = os.path.join(_R, "results", "logs", "p5_cruce_fantasma_IS.json")
    with open(p, "w") as fh:
        json.dump(con_acta(out, __file__), fh, indent=1, ensure_ascii=False)
    for t in tabla:
        print(f"z={t['z']:.3f}  w_eff={t['w_eff']:+.4f}  c={t['c']:.3f}  "
              f"|Pi|/rho={t['Pi_sobre_rho']:.3f}  |Pi|/|p|={t['Pi_sobre_p']:.3f}")
    for f, g in zip(campo, control):
        print(f"k={f['k']:6.1f}  campo r={f['r']:+.3e} (cruce {f['r_en_cruce']:+.3e})  "
              f"control w0 r={g['r']:+.3e}")
    print("controles:", out["controles"], "->", p)


if __name__ == "__main__":
    main()
