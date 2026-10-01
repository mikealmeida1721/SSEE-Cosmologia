#!/usr/bin/env python3
"""edad_universo.py — la edad t0 de Paper 9 (SSEE contra LCDM), con log.

POR QUE (2026-09-30). Paper 9 compara t0 de SSEE con el de LCDM con numeros
tecleados, y los dos venian de metodos distintos: el de SSEE de la integral sin
radiacion que el paper muestra, y el de LCDM de CAMB (con radiacion y
neutrinos). Aqui los dos salen del MISMO metodo, el que el paper declara:

    t0 = (1/H0) * int_0^inf dz / ((1+z) E(z)),
    E^2 = Om (1+z)^3 + (1-Om) f_DE(z),  f_DE de CPL.

SSEE: H0_GLOBAL, Omega_m total, w0, w_a del nucleo. LCDM: Planck 2018 (H0,
Omega_m publicados), w = -1.
CONTROL (R53): CAMB (radiacion y neutrinos masivos incluidos) para los dos
modelos; la integral sin radiacion tiene que quedar a menos de 0.01 Gyr de
CAMB en ambos (la radiacion solo pesa a z alto, donde el tiempo es poco).

Salida: results/logs/edad_universo.json
"""
import json
import os
import sys

import numpy as np
from scipy.integrate import quad

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
import camb  # noqa: E402
import ssee_core as S  # noqa: E402
from lcdm_planck import LCDM_PLANCK as LP  # noqa: E402
from procedencia import con_acta  # noqa: E402

MPC_KM = 3.0856775814913673e19   # ORIGEN-VALOR: 3.0856775814913673e19 — km por Mpc (IAU 2015)
GYR_S = 3.15576e16               # ORIGEN-VALOR: 3.15576e16 — s por Gyr (ano juliano)
OM_PLANCK = 0.3153               # ORIGEN-VALOR: 0.3153 — Omega_m de Planck 2018 VI Tabla 2 (el publicado, no recalculado)


def t0_integral(H0, Om, w0, wa):
    def E(z):
        return np.sqrt(Om * (1 + z) ** 3 + (1 - Om) * (1 + z) ** (3 * (1 + w0 + wa))
                       * np.exp(-3 * wa * z / (1 + z)))
    return quad(lambda z: 1 / ((1 + z) * E(z)), 0, np.inf, limit=500)[0] * MPC_KM / H0 / GYR_S


def t0_camb(**kw):
    return float(camb.get_background(camb.set_params(**kw)).get_derived_params()["age"])


ssee = dict(integral=t0_integral(S.H0_GLOBAL, S.OMEGA_M_TOTAL, S.W0, S.WA),
            camb=t0_camb(H0=S.H0_GLOBAL, ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2, mnu=S.SUM_MNU_EV,
                         w=S.W0, wa=S.WA, dark_energy_model="ppf"))
lcdm = dict(integral=t0_integral(LP["H0"], OM_PLANCK, -1.0, 0.0),
            camb=t0_camb(H0=LP["H0"], ombh2=LP["ombh2"], omch2=LP["omch2"], mnu=LP["mnu"]))
pasa = all(abs(m["integral"] - m["camb"]) < 0.01 for m in (ssee, lcdm))
out = dict(fecha=str(__import__("datetime").date.today()), ssee=ssee, lcdm=lcdm,
           diferencia_lcdm_menos_ssee=lcdm["integral"] - ssee["integral"],
           control=dict(criterio="integral sin radiacion a < 0.01 Gyr de CAMB", pasa=bool(pasa)))
json.dump(con_acta(out, __file__), open(os.path.join(_R, "results", "logs", "edad_universo.json"), "w"), indent=1)
print(f"  SSEE t0 = {ssee['integral']:.4f} Gyr (CAMB {ssee['camb']:.4f})")
print(f"  LCDM t0 = {lcdm['integral']:.4f} Gyr (CAMB {lcdm['camb']:.4f})")
print(f"  diferencia {out['diferencia_lcdm_menos_ssee']:.3f} Gyr   control: {'PASA' if pasa else 'NO PASA'}")
