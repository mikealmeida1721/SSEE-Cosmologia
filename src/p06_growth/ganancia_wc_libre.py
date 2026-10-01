#!/usr/bin/env python3
"""ganancia_wc_libre.py — cuanto chi2 gana cada modelo en BOSS si se le suelta w_c.

POR QUE (2026-09-30). Paper 6 (perfil de w_c) dice que LCDM gana mas chi2 que
SSEE al liberar w_c: es un DIAGNOSTICO, no una comparacion de modelos (en SSEE
w_c es algebraico; soltarlo saca al modelo de si mismo). Los dos numeros
estaban tecleados; salian de restar a mano dos logs.

COMO, para cada fondo (SSEE, LCDM):
  como_es   = chi2 minimo de la cadena BOSS de R1/R2 (w_c fijo, A_s libre):
              /mnt/datos/SSEE_data/chains_p6/boss/{ssee,lcdm}.N.txt, columna chi2
              (la misma lectura que multisonda_fondo_clavado.py).
  w_c_libre = chi2 minimo del perfil de w_c con la amplitud que BOSS prefiere
              (perfil_wc_boss{,_lcdm}.json, control_amplitud_boss.chi2_min).
  ganancia  = como_es - w_c_libre.
CONTROL (R53): el como_es leido aqui tiene que ser el que imprime
results/logs/multisonda_fondo_clavado.log («min libre»), a la precision
impresa (0.0005).

Salida: results/logs/ganancia_wc_libre.json
"""
import glob
import json
import os
import re
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import con_acta  # noqa: E402

CAD = "/mnt/datos/SSEE_data/chains_p6/boss"
LOGS = os.path.join(_R, "results", "logs")
PERFIL = {"SSEE": "perfil_wc_boss.json", "LCDM": "perfil_wc_boss_lcdm.json"}

res, entradas = {}, []
impreso = open(os.path.join(LOGS, "multisonda_fondo_clavado.log")).read()
for m, fp in PERFIL.items():
    rutas = sorted(glob.glob(f"{CAD}/{m.lower()}.[0-9].txt"))
    entradas += rutas + [os.path.join(LOGS, fp)]
    with open(rutas[0]) as f:
        col = f.readline().lstrip("#").split()
    como_es = float(min(np.loadtxt(r, usecols=col.index("chi2"), ndmin=1).min() for r in rutas))
    libre = json.load(open(os.path.join(LOGS, fp)))["control_amplitud_boss"]["chi2_min"]
    log_min = float(re.search(rf"BOSS con fondo {m}\s*: min libre\s+([0-9.]+)", impreso).group(1))
    res[m] = dict(chi2_como_es=como_es, chi2_wc_libre=libre, ganancia=como_es - libre,
                  control_min_libre_multisonda=log_min)
pasa = all(abs(r["chi2_como_es"] - r["control_min_libre_multisonda"]) <= 5e-4 + 1e-9 for r in res.values())
out = dict(fecha=str(__import__("datetime").date.today()), modelos=res,
           diferencia_como_es_ssee_menos_lcdm=res["SSEE"]["chi2_como_es"] - res["LCDM"]["chi2_como_es"],
           control=dict(pasa=bool(pasa)))
json.dump(con_acta(out, __file__, entradas=entradas + [os.path.join(LOGS, "multisonda_fondo_clavado.log")]),
          open(os.path.join(LOGS, "ganancia_wc_libre.json"), "w"), indent=1)
for m, r in res.items():
    print(f"  {m}: como es {r['chi2_como_es']:.3f}  w_c libre {r['chi2_wc_libre']:.3f}  gana {r['ganancia']:.3f}")
print(f"  control contra multisonda: {'PASA' if pasa else 'NO PASA'}")
