#!/usr/bin/env python3
"""resumen_3modelos.py — la comparacion SSEE / LCDM / CPL de Paper 2, en JSON.

POR QUE (2026-09-30). ssee_paper2_mcmc.py (3 modelos, prior Planck comprimido)
imprime BIC, AIC y posteriores en un log de texto; Paper 2 los cita a mano.
Este script los recalcula de las cadenas que ese MCMC guarda y los deja en
results/logs/resumen_3modelos.json, con acta, para que los papers los lean
con \\val.

COMO: las MISMAS formulas que ssee_paper2_mcmc.py (seccion 7):
  ln P_MAP = max de ln P en la cadena;  BIC = k ln N - 2 ln P_MAP;
  AIC = 2k - 2 ln P_MAP;  N = 13 puntos DESI DR2 + 3 restricciones Planck.
Posteriores: mediana y percentiles 16/84 de la cadena plana.
CONTROL (R53): BIC y AIC de los tres modelos tienen que coincidir con la tabla
impresa en results/logs/mcmc_paper2_3models_wmfix.log (a la precision impresa,
0.005), y ln P_MAP con el del log.
"""
import json
import os
import re
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from desi_dr2_data import load_desi_dr2  # noqa: E402
from procedencia import con_acta  # noqa: E402

NPZ = "/mnt/datos/SSEE_data/mcmc/paper2_3models/mcmc_chains_professional.npz"
LOG = os.path.join(_R, "results", "logs", "mcmc_paper2_3models_wmfix.log")
N_PLANCK = 3   # ORIGEN-VALOR: 3 — restricciones del prior Planck comprimido (H0, Omega_m, omega_b), ssee_paper2_mcmc.py L322
PLANCK_H0 = (67.36, 0.54)   # ORIGEN-VALOR: 67.36 +- 0.54 — Planck 2018 VI Tabla 2, el prior comprimido de ssee_paper2_mcmc.py
N = len(load_desi_dr2()["z"]) + N_PLANCK
NOMBRES = {"ssee": ["H0", "obh2"], "lcdm": ["H0", "Om", "obh2"],
           "cpl": ["H0", "Om", "w0", "wa", "obh2"]}
ETIQ = {"ssee": "SSEE", "lcdm": "ΛCDM", "cpl": "CPL"}

d = np.load(NPZ)
res = {}
for m, nom in NOMBRES.items():
    flat, lp = d[f"{m}_flat"], d[f"{m}_lp"]
    k = flat.shape[1]
    lpm = float(lp.max())
    p16, p50, p84 = np.percentile(flat, [16, 50, 84], axis=0)
    res[m] = dict(k=k, lnP_MAP=lpm, BIC=k * np.log(N) - 2 * lpm, AIC=2 * k - 2 * lpm,
                  posterior={n: dict(mediana=float(b), mas=float(c - b), menos=float(b - a),
                                     std=float(s))
                             for n, a, b, c, s in zip(nom, p16, p50, p84, flat.std(axis=0))})
for m in res:
    res[m]["dBIC_vs_ssee"] = res[m]["BIC"] - res["ssee"]["BIC"]
    res[m]["dAIC_vs_ssee"] = res[m]["AIC"] - res["ssee"]["AIC"]
    # con el signo de Paper 2: Delta = SSEE - modelo (negativo favorece a SSEE)
    res[m]["dBIC_ssee_menos"] = res["ssee"]["BIC"] - res[m]["BIC"]
    res[m]["dAIC_ssee_menos"] = res["ssee"]["AIC"] - res[m]["AIC"]
rho_cpl = float(np.corrcoef(d["cpl_flat"][:, 2], d["cpl_flat"][:, 3])[0, 1])
h = res["ssee"]["posterior"]["H0"]
tension_H0 = abs(h["mediana"] - PLANCK_H0[0]) / np.hypot(h["std"], PLANCK_H0[1])

# CONTROL: la tabla impresa por el MCMC
txt = open(LOG).read()
impreso = {}
for m, e in ETIQ.items():
    f = re.search(rf"{e}\s+(\d)\s+(-?[0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)", txt)
    impreso[m] = dict(lnP_MAP=float(f.group(2)), BIC=float(f.group(3)), AIC=float(f.group(5)))
pasa = all(abs(res[m][q] - impreso[m][q]) <= 0.005 + 1e-9 for m in res for q in ("lnP_MAP", "BIC", "AIC"))
out = dict(fecha=str(__import__("datetime").date.today()), N=N, modelos=res,
           tension_H0_ssee_planck=float(tension_H0), rho_w0_wa_cpl=rho_cpl,
           control=dict(log=os.path.relpath(LOG, _R), impreso=impreso, pasa=bool(pasa)))
json.dump(con_acta(out, __file__, entradas=[NPZ, LOG]),
          open(os.path.join(_R, "results", "logs", "resumen_3modelos.json"), "w"), indent=1)
for m, r in res.items():
    print(f"  {m:5s} k {r['k']}  lnP_MAP {r['lnP_MAP']:.3f}  BIC {r['BIC']:.3f} ({r['dBIC_vs_ssee']:+.3f})"
          f"  AIC {r['AIC']:.3f} ({r['dAIC_vs_ssee']:+.3f})")
print(f"  H0 SSEE {h['mediana']:.3f} +- {h['std']:.3f}  tension Planck {tension_H0:.2f} sigma")
print(f"  control contra la tabla del log: {'PASA' if pasa else 'NO PASA'}")
