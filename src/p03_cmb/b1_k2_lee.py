#!/usr/bin/env python3
"""b1_k2_lee.py — DeltaBIC del CMB completo (B1): SSEE k=2 contra LCDM k=6.

POR QUE (2026-10-01). El titular «DeltaBIC = -32.9» de P1/P3/Unified no tenia log
(las cadenas k=2 del 23-jun se sobrescribieron). La cadena k=2 se rehizo (R-1 de
las medias 0.015) y el analisis de ssee_paper3_b1_mcmc.py tenia tres defectos:
k_SSEE=3 fijo, chi2 de la cadena 1 sola, y el MEJOR MUESTREADO en vez del minimo
(que favorece al modelo con menos parametros). Aqui:
  chi2     el MINIMO de b1_minimiza.py (results/logs/b1_min_{ssee,lcdm}.json)
  k        los parametros COSMOLOGICOS muestreados, contados del .input.yaml de
           cada cadena (los ~20 nuisance de plik son comunes y no cuentan)
  N        N_DATA de ssee_paper3_b1_mcmc.py (verificado contra clipy)
  posterior media y 68 % de logA, tau, sigma8 (y los de LCDM) de las 4 cadenas
CONTROL (R53): el DeltaBIC con el MEJOR MUESTREADO tiene que quedar del mismo lado
que con el minimo (si cambiara de signo, el resultado dependeria del estimador).

Salida: results/logs/b1_k2.json
"""
import glob
import json
import os
import sys

import numpy as np
import yaml

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p03_cmb"))
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)
import ssee_paper3_b1_mcmc as B  # noqa: E402

CH = os.path.join(_R, "results", "chains")
LOGS = os.path.join(_R, "results", "logs")
QUEMA = 0.3   # ORIGEN-VALOR: 0.3 — el burn-in de analyse_chains y de b1_minimiza
PREF = {"SSEE": "ssee_cmb_k2", "LCDM": "lcdm_cmb"}
MIN = {"SSEE": "b1_min_ssee.json", "LCDM": "b1_min_lcdm.json"}

out, entradas = {}, []
for M, pf in PREF.items():
    inp = yaml.safe_load(open(os.path.join(CH, pf + ".input.yaml")))
    k = [p for p, v in inp["params"].items() if isinstance(v, dict) and "prior" in v]
    mn = json.load(open(os.path.join(LOGS, MIN[M])))
    assert mn["control"]["pasa"], f"la minimizacion de {M} no paso su control"
    fs = sorted(glob.glob(os.path.join(CH, pf + ".[0-9].txt")))
    hdr = open(fs[0]).readline().lstrip("#").split()
    X = np.vstack([np.loadtxt(f)[int(QUEMA * sum(1 for _ in open(f))):] for f in fs])
    w = X[:, hdr.index("weight")]
    post = {}
    for p in k + ["sigma8"]:
        if p not in hdr:
            continue
        x = X[:, hdr.index(p)]
        o = np.argsort(x)
        c = np.cumsum(w[o]) / w.sum()
        post[p] = dict(media=float(np.average(x, weights=w)),
                       p16=float(x[o][np.searchsorted(c, 0.16)]), p84=float(x[o][np.searchsorted(c, 0.84)]))
    out[M] = dict(k=len(k), libres=k, chi2_min=mn["chi2_min"], chi2_mejor_muestreado=mn["chi2_mejor_muestreado"],
                  n_muestras=int(len(X)), posterior=post)
    entradas += fs + [os.path.join(CH, pf + ".input.yaml"), os.path.join(LOGS, MIN[M])]
    print(f"  {M}: k={len(k)} {k}  chi2_min {mn['chi2_min']:.3f}  (muestreado {mn['chi2_mejor_muestreado']:.3f})")

lnN = np.log(B.N_DATA)
dk = out["SSEE"]["k"] - out["LCDM"]["k"]
dchi = out["SSEE"]["chi2_min"] - out["LCDM"]["chi2_min"]
dchi_m = out["SSEE"]["chi2_mejor_muestreado"] - out["LCDM"]["chi2_mejor_muestreado"]
out.update(N_DATA=B.N_DATA, penal_por_parametro=float(lnN), dk=dk,
           dchi2=float(dchi), dBIC=float(dchi + dk * lnN), penal_BIC=float(dk * lnN),
           dchi2_muestreado=float(dchi_m), dBIC_muestreado=float(dchi_m + dk * lnN))
pasa = bool(np.sign(out["dBIC"]) == np.sign(out["dBIC_muestreado"]))
out["control"] = dict(criterio="el DeltaBIC con el mejor muestreado queda del mismo lado que con el minimo", pasa=pasa)
print(f"  dchi2 {dchi:+.3f}  dk {dk}  dBIC {out['dBIC']:+.3f}  (con muestreado {out['dBIC_muestreado']:+.3f}) -> control {'PASA' if pasa else 'NO PASA'}")
json.dump(con_acta(out, __file__, entradas=entradas), open(os.path.join(LOGS, "b1_k2.json"), "w"), indent=1)
if not pasa:
    sys.exit("control NO PASA")
