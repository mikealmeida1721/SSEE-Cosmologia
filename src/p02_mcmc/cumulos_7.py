#!/usr/bin/env python3
"""cumulos_7.py — la tabla de sensibilidad de cumulos de Paper 2 (siete cumulos), con log.

POR QUE (2026-09-30). Las tablas tab:cluster_data y tab:cluster_sensitivity de
Paper 2, sus chi2_r (0.122 / 0.126 / 14.05 / 14.91), los Delta chi2 y la prueba
de robustez a las barras de error estaban tecleados. ssee_paper2_analysis.py
solo tiene los cuatro cumulos de Zhang; los tres de la extension (Perseus,
A2142, A2744) se hicieron a mano con f_b = 0.184 y un factor IGIMF «~1.71»
redondeados. Aqui todo lo derivado se calcula; solo entran datos publicados.

DATOS (externos, 10^14 M_sun, dentro de R_200, como declara la tabla del paper):
  Zhang+2026 (arXiv:2602.06082): M_bar^IGIMF, su error, M_bar con IMF estandar,
      M_obs y su error, para Coma, A2029, A478, Bullet.
  Simionescu+2011 (Perseus), Tchernin+2016 (A2142), Merten+2011 (A2744): M_200
      y su error. Para estos tres el paper declara
      M_bar^IGIMF = f_b * M_200,  f_b = media de M_bar^IGIMF/M_obs en Zhang,
      M_bar^std  = M_bar^IGIMF / F,  F = media de M_bar^IGIMF/M_bar^std en Zhang.
MODELO (P2 ec. de M_SSEE): M = M_bar * KAL0 * (1 + f_nu), f_nu = 0.020.
ESCENARIOS: SSEE (IGIMF, f_nu) · f_nu = 0 · IMF estandar · KAL0 solo.
ROBUSTEZ: chi2_r(SSEE) con las barras multiplicadas por s; el s en que
  chi2_r cruza 1 y 2 (chi2 escala como 1/s^2).
CONTROL (R53): con los cuatro cumulos de Zhang, las masas y el chi2_r tienen
que coincidir con los de ssee_paper2_analysis.py (mismo modelo, otro script),
que se ejecuta aqui y se lee de su salida.

Salida: results/logs/cumulos_7.json
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from ssee_core import KAL0  # noqa: E402
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)   # acta de procedencia: primera linea del log

# ORIGEN-VALOR: Zhang+2026 arXiv:2602.06082 — (M_bar_IGIMF, error, M_bar_std, M_obs, error)
ZHANG = {
    "Coma": (1.8, 0.2, 1.0, 9.8, 1.0),
    "A2029": (2.2, 0.2, 1.3, 12.0, 1.2),
    "A478": (1.5, 0.2, 0.9, 8.0, 1.0),
    "Bullet (main)": (1.2, 0.2, 0.7, 6.5, 1.0),
}
# ORIGEN-VALOR: M_200 y error — Simionescu+2011 (Science 331, 1576), Tchernin+2016 (A&A 595, A42), Merten+2011 (MNRAS 417, 333)
EXTENSION = {"Perseus": (6.65, 0.45), "A2142": (14.5, 1.5), "A2744": (18.0, 4.0)}
F_NU = 0.020   # ORIGEN-VALOR: 0.020 — f_nu de Paper 2 (ec. M_SSEE), punto medio del rango 0.018-0.022 del script original

f_b = float(np.mean([z[0] / z[3] for z in ZHANG.values()]))
F_igimf = float(np.mean([z[0] / z[2] for z in ZHANG.values()]))

datos = {n: dict(M_igimf=z[0], M_std=z[2], M_obs=z[3], dM_obs=z[4], fuente="Zhang2026") for n, z in ZHANG.items()}
for n, (m, dm) in EXTENSION.items():
    datos[n] = dict(M_igimf=f_b * m, M_std=f_b * m / F_igimf, M_obs=m, dM_obs=dm, fuente="extension f_b")

ESC = {"ssee": ("M_igimf", F_NU), "fnu0": ("M_igimf", 0.0), "std_imf": ("M_std", F_NU), "kal0_solo": ("M_std", 0.0)}
for d in datos.values():
    for e, (col, fn) in ESC.items():
        d[e] = d[col] * KAL0 * (1 + fn)
    d["chi2_ssee"] = ((d["ssee"] - d["M_obs"]) / d["dM_obs"]) ** 2


def chi2(nombres, e, s=1.0):
    return sum(((datos[n][e] - datos[n]["M_obs"]) / (s * datos[n]["dM_obs"])) ** 2 for n in nombres)


def resumen(nombres):
    r = {e: dict(chi2=chi2(nombres, e), chi2r=chi2(nombres, e) / len(nombres)) for e in ESC}
    for e in ESC:
        r[e]["dchi2_vs_ssee"] = r[e]["chi2"] - r["ssee"]["chi2"]
    c0 = r["ssee"]["chi2r"]
    r["robustez"] = dict(chi2r_s0p5=c0 / 0.25, chi2r_s1p5=c0 / 2.25,
                         reduccion_para_chi2r_1=1 - np.sqrt(c0 / 1.0),
                         reduccion_para_chi2r_2=1 - np.sqrt(c0 / 2.0),
                         max_residuo_sigma=max(np.sqrt(datos[n]["chi2_ssee"]) for n in nombres))
    # en porcentaje (x100): el macro no puede llevar «%» (comentaria la linea en LaTeX)
    r["robustez"]["pct_reduccion_chi2r_1"] = 100 * r["robustez"]["reduccion_para_chi2r_1"]
    r["robustez"]["pct_reduccion_chi2r_2"] = 100 * r["robustez"]["reduccion_para_chi2r_2"]
    r["robustez"] = {k: float(v) for k, v in r["robustez"].items()}
    r["N"] = len(nombres)
    return r


r4, r7 = resumen(list(ZHANG)), resumen(list(datos))
r7["subprediccion_std_imf_media"] = float(np.mean([datos[n]["M_obs"] / datos[n]["std_imf"] for n in datos]))

# Control: el script original (4 cumulos)
sal = subprocess.run([sys.executable, os.path.join(_R, "src", "p02_mcmc", "ssee_paper2_analysis.py")],
                     capture_output=True, text=True, cwd=_R, env=dict(os.environ, MPLBACKEND="Agg")).stdout
m = re.search(r"SSEE completo\s+([0-9.]+)\s+([0-9.]+)", sal)
orig = dict(chi2=float(m.group(1)), chi2r=float(m.group(2)))
masas_orig = {n: float(re.search(rf"{re.escape(n)}\s+[0-9.]+\s+([0-9.]+)", sal).group(1)) for n in ZHANG}
pasa = (abs(orig["chi2r"] - r4["ssee"]["chi2r"]) <= 5e-4
        and all(abs(masas_orig[n] - datos[n]["ssee"]) <= 5e-3 for n in ZHANG))

out = dict(fecha=str(__import__("datetime").date.today()), KAL0=KAL0, f_nu=F_NU, f_b=f_b, F_igimf=F_igimf,
           cumulos=datos, cuatro=r4, siete=r7,
           control=dict(original_4=orig, masas_original=masas_orig, pasa=bool(pasa)))
json.dump(con_acta(out, __file__), open(os.path.join(_R, "results", "logs", "cumulos_7.json"), "w"), indent=1)

print(f"  f_b = {f_b:.5f}   F_IGIMF = {F_igimf:.4f}")
for n, d in datos.items():
    print(f"  {n:14s} {d['ssee']:6.2f} {d['fnu0']:6.2f} {d['std_imf']:6.2f} {d['kal0_solo']:6.2f}  "
          f"{d['M_obs']:5.2f}±{d['dM_obs']:.2f}  chi2 {d['chi2_ssee']:.3f}")
for k, r in (("4", r4), ("7", r7)):
    print(f"  N={k}: " + "  ".join(f"{e} {r[e]['chi2r']:.3f} ({r[e]['dchi2_vs_ssee']:+.2f})" for e in ESC))
    print(f"        robustez {r['robustez']}")
print(f"  control contra ssee_paper2_analysis (4 cumulos): {orig} -> {'PASA' if pasa else 'NO PASA'}")
