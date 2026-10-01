#!/usr/bin/env python3
"""b1_minimiza.py — minimo de chi2 de B1 (CMB completo) para SSEE k=2 y LCDM.

POR QUE (2026-10-01). El analisis de B1 (ssee_paper3_b1_mcmc.py) calculaba el
DeltaBIC con el MEJOR chi2 MUESTREADO de la cadena 1 sola. Eso no es el minimo, y
el sesgo no es simetrico: con 2 parametros (SSEE k=2) la cadena se acerca al
minimo mucho mas que con 6 + los ~20 nuisance de plik (LCDM), asi que favorece al
modelo con menos parametros. El BIC pide la verosimilitud MAXIMA de cada modelo.

QUE HACE. Para un modelo (ssee | lcdm):
  1. lee el .updated.yaml de su cadena (mismos ingredientes, mismas likelihoods);
  2. busca el mejor punto MUESTREADO en las 4 cadenas (tras burn-in 0.3);
  3. arranca ahi el minimizador de Cobaya (BOBYQA), minimizando el chi2 de las
     likelihoods (ignore_prior), y escribe <prefijo>_min.minimum.
CONTROL (R53): el minimo tiene que ser <= el mejor muestreado (si sale mayor, el
minimizador fallo y se dice). Se corre igual para los dos modelos.

Uso: b1_minimiza.py ssee|lcdm
"""
import glob
import json
import os
import sys

import numpy as np
import yaml

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)
MOD = sys.argv[1]
PREF = os.path.join(_R, "results", "chains", {"ssee": "ssee_cmb_k2", "lcdm": "lcdm_cmb"}[MOD])
QUEMA = 0.3   # ORIGEN-VALOR: 0.3 — el mismo burn-in que usa analyse_chains de ssee_paper3_b1_mcmc.py

# La configuracion se construye con las MISMAS funciones que corrieron la cadena
# (el .updated.yaml no guarda la funcion logA -> As). El .updated.yaml solo da la
# lista de libres (con los nuisance de plik) y sirve de control de ingredientes.
sys.path.insert(0, os.path.join(_R, "src", "p03_cmb"))
import ssee_paper3_b1_mcmc as B  # noqa: E402
upd = yaml.safe_load(open(PREF + ".updated.yaml"))
info = B._ssee_info(PREF, h0_fixed=True) if MOD == "ssee" else B._lcdm_info(PREF)
libres = [p for p, v in upd["params"].items() if isinstance(v, dict) and "prior" in v]
_fijos = {p: v for p, v in info["params"].items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
_mal = [p for p, v in _fijos.items() if abs(float(upd["params"].get(p, {}).get("value", np.nan)) - v) > 1e-9]
print(f"  ingredientes fijos: {_fijos}", flush=True)
if _mal:
    sys.exit(f"  la configuracion reconstruida NO es la de la cadena en {_mal}")
fs = sorted(glob.glob(PREF + ".[0-9].txt"))
mejor, mejor_chi2 = None, np.inf
for f in fs:
    hdr = open(f).readline().lstrip("#").split()
    x = np.loadtxt(f)
    x = x[int(QUEMA * len(x)):]
    i = int(np.argmin(x[:, hdr.index("chi2")]))
    if x[i, hdr.index("chi2")] < mejor_chi2:
        mejor_chi2 = float(x[i, hdr.index("chi2")])
        mejor = {p: float(x[i, hdr.index(p)]) for p in libres}
print(f"  {MOD}: {len(libres)} libres (con nuisance), {len(fs)} cadenas; mejor muestreado chi2 = {mejor_chi2:.3f}", flush=True)

for p in libres:
    if p in info["params"] and isinstance(info["params"][p], dict):
        info["params"][p] = dict(info["params"][p], ref=mejor[p])
    else:   # nuisance de plik: su definicion tal como corrio
        info["params"][p] = dict(upd["params"][p], ref=mejor[p])
    info["params"][p].pop("proposal", None)
info["sampler"] = {"minimize": {"ignore_prior": True, "best_of": 1}}
info["output"] = PREF + "_min"
info["force"] = True
info.pop("resume", None)
for k in ("post", "debug", "timing"):
    info.pop(k, None)

from cobaya.run import run  # noqa: E402
upd, sampler = run(info)
prod = sampler.products()
chi2_min = float(2.0 * prod["minimum"]["minuslogpost"]) if "minuslogpost" in prod["minimum"] else None
try:
    chi2_min = float(prod["minimum"]["chi2"])
except Exception:
    pass
pasa = chi2_min is not None and chi2_min <= mejor_chi2 + 1e-6
print(f"  {MOD}: chi2 minimo = {chi2_min:.3f} (mejor muestreado {mejor_chi2:.3f}) -> control {'PASA' if pasa else 'NO PASA'}", flush=True)
out = dict(modelo=MOD, cadenas=fs, libres=libres, n_libres=len(libres),
           chi2_mejor_muestreado=mejor_chi2, chi2_min=chi2_min,
           punto_min={p: float(prod["minimum"][p]) for p in libres},
           control=dict(criterio="chi2_min <= mejor muestreado", pasa=bool(pasa)))
json.dump(con_acta(out, __file__, entradas=fs + [PREF + ".updated.yaml"]),
          open(os.path.join(_R, "results", "logs", f"b1_min_{MOD}.json"), "w"), indent=1)
if not pasa:
    sys.exit("control NO PASA")
