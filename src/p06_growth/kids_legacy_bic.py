#!/usr/bin/env python3
"""kids_legacy_bic.py — chi2_min y BIC de las tres corridas de KiDS-Legacy, de sus cadenas.

POR QUE (2026-09-30). La tabla de seleccion de modelos de Paper 6 (chi2_min y
BIC de: SSEE unificado con A_s del CMB, SSEE con A_s libre, LCDM con fondo
Planck) y CANONICAL citan estos numeros, pero ningun log propio los
calculaba: aparecian copiados en logs de otras corridas (multisonda, conjunta).
Este script los saca de las cadenas.

COMO: cadenas /mnt/datos/SSEE_data/chains_p6/kids_legacy/{sseefijo,ssee,
lcdmfijo}.{1-4}.txt; chi2_min = minimo de la columna chi2 tras quitar el
burn-in del 30 % de cada cadena — la MISMA convencion de R3/R4 (KiDS-1000) y la
que tiene CANONICAL. Medido el 2026-09-30: en la corrida con A_s libre el
minimo absoluto cae DENTRO del burn-in y es menor; se guarda como dato
informativo (`chi2_min_todas_las_filas`), no se usa. k = parametros muestreados (columnas entre
minuslogpost y minuslogprior); N = 357 puntos xi+- (Wright+2025);
BIC = chi2_min + k ln N.
CONTROL (R53): chi2_min de la corrida unificada tiene que ser el de CANONICAL
(chi2_min_ssee_unif) a 1e-3, y el de A_s libre el de chi2_min_kids_legacy.

Salida: results/logs/kids_legacy_bic.json
"""
import glob
import json
import math
import os
import sys

import numpy as np
import yaml

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import con_acta  # noqa: E402

CAD = "/mnt/datos/SSEE_data/chains_p6/kids_legacy"
BURN = 0.30
N_DATOS = 357   # ORIGEN-VALOR: 357 — puntos xi+- de KiDS-Legacy (Wright+2025, A&A 703, A158)
C = yaml.safe_load(open(os.path.join(_R, "CANONICAL_VALUES.yaml")))["canonical"]
CORRIDAS = {"sseefijo": "SSEE unificado (A_s del CMB)", "ssee": "SSEE, A_s libre",
            "lcdmfijo": "LCDM, fondo Planck 2018, A_s libre"}

res, entradas = {}, []
for nom, desc in CORRIDAS.items():
    rutas = sorted(glob.glob(f"{CAD}/{nom}.[1-4].txt"))
    entradas += rutas
    with open(rutas[0]) as f:
        col = f.readline().lstrip("#").split()
    k = col.index("minuslogprior") - col.index("minuslogpost") - 1
    cad = [np.loadtxt(r, usecols=col.index("chi2"), ndmin=1) for r in rutas]
    post = np.concatenate([a[int(BURN * len(a)):] for a in cad])
    c2 = float(post.min())
    res[nom] = dict(descripcion=desc, chi2_min=c2, k=k, N=N_DATOS, dof=N_DATOS - k,
                    BIC=c2 + k * math.log(N_DATOS), filas_post_burnin=int(len(post)),
                    chi2_min_todas_las_filas=float(min(a.min() for a in cad)))
ctl = dict(unif=dict(log=res["sseefijo"]["chi2_min"], canonical=C["chi2_min_ssee_unif"]),
           libre=dict(log=res["ssee"]["chi2_min"], canonical=C["chi2_min_kids_legacy"]))
pasa = all(abs(v["log"] - v["canonical"]) < 1e-3 for v in ctl.values())
out = dict(fecha=str(__import__("datetime").date.today()), corridas=res,
           deltaBIC=dict(libre_menos_unif=res["ssee"]["BIC"] - res["sseefijo"]["BIC"],
                         lcdm_menos_unif=res["lcdmfijo"]["BIC"] - res["sseefijo"]["BIC"]),
           control=dict(contra_canonical=ctl, pasa=pasa))
json.dump(con_acta(out, __file__, entradas=entradas + [os.path.join(_R, "CANONICAL_VALUES.yaml")]),
          open(os.path.join(_R, "results", "logs", "kids_legacy_bic.json"), "w"), indent=1)
for nom, r in res.items():
    print(f"  {nom:9s} chi2_min {r['chi2_min']:.3f}  k {r['k']}  BIC {r['BIC']:.2f}")
print(f"  dBIC libre-unif {out['deltaBIC']['libre_menos_unif']:+.2f}  lcdm-unif {out['deltaBIC']['lcdm_menos_unif']:+.2f}")
print(f"  control contra CANONICAL: {'PASA' if pasa else 'NO PASA'} {ctl}")
