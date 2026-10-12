#!/usr/bin/env python3
"""¿Estabiliza Israel–Stewart el modo de gradiente de Paper 5? (2026-10-11)

Quinta lectura de P5. El paper afirma (Q1) que con ζ̃/(τ_Π H₀) = s_DE = |w₀|
el fluido IS queda «exactamente marginalmente estable», c²_eff = w₀ + s_DE = 0,
y (Q2) lo «comprueba» integrando el sistema con la aproximación cuasi-estática
Π̃' = 0. Aquí se mide, sin aproximaciones, qué hace el sistema COMPLETO.

1. Dispersión de un modo que CRECE, e^{λt}, en Minkowski (apéndice A de P5,
   mismas ecuaciones):  λ² = k² [ |c²| − s·λτ/(1+λτ) ].
   Con |c²| = s (la identidad de P5):  λ² = k² s / (1+λτ)  > 0  para todo k.
   Límite NS (τ→0, lo que integra la aproximación cuasi-estática): λ → s/(ζ̃)
   = 1/τ acotado. Límite IS (λτ ≫ 1): λ ≈ (k² s/τ)^{1/3}, crece con k.
2. Integración cosmológica de las 5 variables (δ_m, v_m, δ_DE, v_DE, Π̃)
   contra la cuasi-estática de 4, en el cierre de Paper 1 (el campo lleva w₀:
   inercia ρ_DE(1+w₀) > 0; la viscosa lleva el cruce fantasma).
3. Controles: (a) ζ = 0 da λ = k√s (el caso desnudo); (b) con el c²_s del
   campo de Paper 7 (+0.021284) y la misma viscosidad, NO crece nada.

Units H₀ = c = 1; d/d ln a en lo cosmológico.
"""
import json
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
import ssee_core as S  # noqa: E402
from procedencia import cabecera, con_acta  # noqa: E402
print(cabecera(__file__), flush=True)

W0, WA, OM, KAL0, TAU = S.W0, S.WA, S.OMEGA_M_TOTAL, S.KAL0, S.TAU_PI_H0
OD = 1.0 - OM
ZT = KAL0 / 3.0                      # ζ̃, Paper 5 ec. IS_params
S_DE = ZT / TAU                      # = |w₀| (la identidad de P5)
CS2_CAMPO = (1 + W0) / (5 - 3 * W0)  # c²_s del condensado de Paper 7


def lam_minkowski(k, cs2, s, tau):
    """Raíz real positiva de λ² = k²[−cs2 − s·λτ/(1+λτ)] (0 si no hay)."""
    f = lambda L: L**2 - k**2 * (-cs2 - s * L * tau / (1 + L * tau))
    hi = k * np.sqrt(abs(cs2) + s) + 10.0
    if f(1e-12) >= 0:          # sin cambio de signo ⟹ sin modo creciente
        return 0.0
    return brentq(f, 1e-12, hi)


def fde(a):
    return a**(-3 * (1 + W0 + WA)) * np.exp(-3 * WA * (1 - a))


def H(a):
    return np.sqrt(OM * a**-3 + OD * fde(a))


def rhs(x, Y, k, completo, cs2):
    a = np.exp(x)
    h = H(a)
    opw = 1.0 + W0                      # inercia del campo (Paper 1, cruce)
    dm, vm, dd, vd, P = Y
    Phi = -(1.5 / k**2) * (OM * dm / a + a**2 * OD * fde(a) * dd)
    kH = k / (a * h)
    if not completo:                    # cuasi-estática: Π̃' = 0
        P = -ZT * kH * h * vd
    dvd = -(1 - 3 * cs2) * vd + kH * (cs2 * dd / opw + P) + kH * Phi
    dP = (-P - ZT * kH * h * vd) / (TAU * h) if completo else 0.0
    return [-kH * vm, -vm + kH * Phi, -opw * kH * vd, dvd, dP]


def integra(k, completo, cs2, a_ini=0.05):
    Y0 = [a_ini, -a_ini * a_ini * H(a_ini) / k, 0.0, 0.0, 0.0]
    s = solve_ivp(rhs, [np.log(a_ini), 0.0], Y0, args=(k, completo, cs2),
                  method="LSODA", rtol=1e-9, atol=1e-14)
    dm, _, dd, _, _ = s.y[:, -1]
    return dict(k=k, exito=bool(s.success), delta_m=float(dm), r=float(dd / dm))


def main():
    ks = [2.0, 5.0, 10.0, 20.0, 50.0, 100.0]
    disp = []
    for k in ks:
        disp.append(dict(
            k=k,
            lam_IS=lam_minkowski(k, W0, S_DE, TAU),
            lam_IS_asintota=float((k**2 * S_DE / TAU) ** (1 / 3)),
            lam_desnudo_zeta0=lam_minkowski(k, W0, 0.0, TAU),
            lam_campo_P7=lam_minkowski(k, CS2_CAMPO, S_DE, TAU),
        ))
    lam_NS = S_DE / ZT  # = 1/τ_Π H₀
    cosm = dict(
        cuasi_estatica=[integra(k, False, W0) for k in ks],
        completa=[integra(k, True, W0) for k in ks],
        completa_campo_P7=[integra(k, True, CS2_CAMPO) for k in ks],
    )
    # controles
    ctrl_desnudo = all(abs(d["lam_desnudo_zeta0"] - d["k"] * np.sqrt(S_DE)) < 1e-6 * d["k"]
                       for d in disp)
    ctrl_campo = all(d["lam_campo_P7"] == 0.0 for d in disp)
    ctrl_identidad = abs(S_DE + W0) < 1e-12
    out = dict(
        pregunta="¿estabiliza IS el modo de gradiente de P5 con zeta_t/(tau H0) = |w0|?",
        s_DE=S_DE, tau_Pi_H0=TAU, zeta_tilde=ZT, cs2_bare=W0, cs2_campo_P7=CS2_CAMPO,
        lam_NS_limite=lam_NS,
        dispersion_minkowski=disp,
        cosmologica=cosm,
        controles=dict(zeta0_da_k_raiz_s=ctrl_desnudo, campo_P7_no_crece=ctrl_campo,
                       identidad_s_mas_w0_cero=ctrl_identidad),
        lectura=("Con |c2| = s exacto, el modo creciente tiene lambda^2 = k^2 s/(1+lambda tau) > 0 "
                 "a todo k: IS NO estabiliza; c2_eff = 0 solo vale para oscilaciones con "
                 "omega tau -> infinito. La cuasi-estatica es el limite NS y acota la tasa a 1/tau. "
                 "Con el c2_s del campo de Paper 7 no hay modo creciente."),
    )
    p = os.path.join(_R, "results", "logs", "p5_estabilidad_IS_completa.json")
    with open(p, "w") as fh:
        json.dump(con_acta(out, __file__), fh, indent=1, ensure_ascii=False)
    for d in disp:
        print(f"k={d['k']:6.1f}  lam_IS={d['lam_IS']:8.3f}  asint={d['lam_IS_asintota']:8.3f}  "
              f"zeta0={d['lam_desnudo_zeta0']:8.3f}  campoP7={d['lam_campo_P7']:.3f}")
    print(f"lam_NS = {lam_NS:.4f}")
    for nom, filas in cosm.items():
        print(nom, [(f["k"], f"{f['r']:+.3e}", f["exito"]) for f in filas])
    print("controles:", out["controles"])
    print("->", p)


if __name__ == "__main__":
    main()
