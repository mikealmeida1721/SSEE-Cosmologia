#!/usr/bin/env python3
"""s8_desde_b1.py — el S8 que Paper 6 atribuye al CMB, leido de las cadenas B1.

POR QUE (2026-09-30). R73 encontro sin log dos filas de la tabla de A_s de
Paper 6 (L388-389): S8 = 0.8262 +- 0.0054 («SSEE fit to raw Planck») y
0.8229 +- 0.0059 («LambdaCDM-fitted Planck value, borrowed»). Salen de las
cadenas B1 (results/chains/{ssee,lcdm}_cmb): S8 = sigma8 * sqrt(Omega_m / 0.3)
con Omega_m = omega_m/h^2 de SSEE (0.308881, del nucleo) en las DOS filas —la
segunda toma el sigma8 que pide el ajuste LambdaCDM y lo pone en el fondo de
SSEE, que es lo que la tabla llama «borrowed»—. La distancia al KiDS-1000
publicado (0.759 +- 0.024, CANONICAL obs_KiDS_S8) en suma cuadratica.

Mismo corte que el analisis B1: getdist, ignore_rows = 0.3.
CONTROL (R53): el sigma8 medio de cada cadena tiene que ser el que imprime
results/logs/b1_analyse.log (0.8142 SSEE, 0.8110 LambdaCDM, a 4 decimales).

Salida: results/logs/s8_desde_b1.json
"""
import json
import math
import os
import re
import sys

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "src"))
import yaml  # noqa: E402
from getdist import loadMCSamples  # noqa: E402

import ssee_core as S  # noqa: E402

KIDS = yaml.safe_load(open(os.path.join(R, "CANONICAL_VALUES.yaml")))["canonical"]["obs_KiDS_S8"]
KIDS_SIG = 0.024   # ORIGEN-VALOR: 0.024 — sigma de KiDS-1000 S8 (Asgari+2021), el mismo que CANONICAL anota junto a obs_KiDS_S8
fac = math.sqrt(S.OMEGA_M_CMB / 0.3) if hasattr(S, "OMEGA_M_CMB") else math.sqrt(S.OMEGA_M_TOTAL / 0.3)
log_b1 = open(os.path.join(R, "results/logs/b1_analyse.log")).read()
esperado = {lab: float(m) for lab, m in re.findall(r"\[(SSEE|LCDM)\].*?sigma8\s+=\s+([0-9.]+)", log_b1, re.S)}
out = dict(fecha=str(__import__("datetime").date.today()), factor_Om=fac, kids=dict(S8=KIDS, sigma=KIDS_SIG), filas={})
for lab, pref in (("SSEE", "ssee_cmb"), ("LCDM", "lcdm_cmb")):
    s = loadMCSamples(os.path.join(R, "results/chains", pref), settings={"ignore_rows": 0.3})
    m, e = float(s.mean("sigma8")), float(s.std("sigma8"))
    S8, S8e = m * fac, e * fac
    out["filas"][lab] = dict(sigma8=m, sigma8_sigma=e, logA=float(s.mean("logA")), logA_sigma=float(s.std("logA")),
                             S8=S8, S8_sigma=S8e, tension_kids=(S8 - KIDS) / math.hypot(S8e, KIDS_SIG),
                             control_sigma8_log=esperado.get(lab),
                             control_pasa=bool(esperado.get(lab) is not None and f"{m:.4f}" == f"{esperado[lab]:.4f}"))
    f = out["filas"][lab]
    print(f"  {lab:4s} logA {f['logA']:.3f}±{f['logA_sigma']:.3f}  S8 {S8:.4f}±{S8e:.4f}  "
          f"{f['tension_kids']:.2f}σ KiDS · control σ8 {m:.4f} vs log {esperado.get(lab)} -> {f['control_pasa']}")
json.dump(out, open(os.path.join(R, "results/logs/s8_desde_b1.json"), "w"), indent=1)
