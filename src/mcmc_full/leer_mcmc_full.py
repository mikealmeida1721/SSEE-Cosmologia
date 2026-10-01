#!/usr/bin/env python3
"""leer_mcmc_full.py — posteriores de la corrida multisonda completa (Unified tab:mcmc_full).

POR QUE (2026-09-30). R73 encontro que la tabla tab:mcmc_full de Unified tiene
filas que no salen de ningun log (Omega_c h^2 0.11935, r_drag 147.20, Omega_m
0.3288). La tabla se escribio el 2026-07-09 (e8efc6a) desde estas cadenas sin
dejar lector. Este script es ese lector.

CADENAS: /mnt/datos/SSEE_data/mcmc/mcmc_full/c{1..4}/ssee_full (Cobaya, 4
cadenas independientes; CAMB + plik_lite TTTEEE + lensing + prior tau + DESI DR2
+ fsigma8, w0/wa libres, H0 plano [60,80]). Se descarta el 30 % inicial de cada
cadena (mismo corte que el resto de lectores del repo).

CONTROL (R53): las filas de la tabla que YA coincidian por valor (H0,
w0, wa, Omega_b h^2; ver CONTROL abajo) tienen que salir iguales a su
redondeo; si no, el lector no lee la misma corrida y lo demas no vale.

Salida: results/logs/mcmc_full_posteriores.json
"""
import json
import os

import numpy as np

import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from procedencia import con_acta  # noqa: E402

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE = "/mnt/datos/SSEE_data/mcmc/mcmc_full"
PAR = ["ombh2", "omch2", "rdrag", "H0", "omegam", "w", "wa", "sigma8", "S8"]
# filas de tab:mcmc_full que ya casaban por valor: son el CONTROL, no resultados
CONTROL = {"H0": "65.87",        # ORIGEN-VALOR: 65.87 — fila H0 de tab:mcmc_full (control)
           "w": "-0.655", "wa": "-1.104",
           "ombh2": "0.02243"}   # ORIGEN-VALOR: 0.02243 — fila Omega_b h^2 de tab:mcmc_full (control)

filas, nombres = [], None
for i in (1, 2, 3, 4):
    f = f"{BASE}/c{i}/ssee_full.1.txt"
    nombres = open(f).readline().lstrip("#").split()
    d = np.loadtxt(f)
    filas.append(d[int(0.3 * len(d)):])
d = np.vstack(filas)
w = d[:, nombres.index("weight")]
res = {}
for p in PAR:
    x = d[:, nombres.index(p)]
    m = float(np.average(x, weights=w))
    s = float(np.sqrt(np.average((x - m) ** 2, weights=w)))
    res[p] = dict(media=m, sigma=s)
ctrl = {p: dict(tabla=v, lector=res[p]["media"],
                coincide=bool(f"{res[p]['media']:.{len(v.split('.')[1])}f}" == v))
        for p, v in CONTROL.items()}
# Tensiones frente al valor ALGEBRAICO de SSEE (2026-10-01; la tabla del Unified
# las traia tecleadas). r_d: CAMB con los ingredientes del nucleo (lya_auditoria, escenario B).
import ssee_core as _S  # noqa: E402
LYA = os.path.join(R, "results/logs/lya_auditoria.json")
ALG = dict(ombh2=_S.OMEGA_B_H2, omch2=_S.OMEGA_C_H2, rdrag=json.load(open(LYA))["escenario_B"]["rd"],
           H0=_S.H0_GLOBAL, omegam=_S.OMEGA_M_TOTAL, w=_S.W0, wa=_S.WA)
tens = {p: dict(algebraico=v, tension_sigma=(res[p]["media"] - v) / res[p]["sigma"],
                tension_abs=abs(res[p]["media"] - v) / res[p]["sigma"]) for p, v in ALG.items()}
# Distancia conjunta en (w0, wa): covarianza pesada de las cadenas; SSEE y, como
# control del otro lado, el punto LCDM (-1, 0). Chi2 con 2 g.l. -> sigma equivalente.
from scipy import stats as _st  # noqa: E402
_X = np.vstack([d[:, nombres.index("w")], d[:, nombres.index("wa")]])
_mu = np.average(_X, axis=1, weights=w)
_C = np.cov(_X, aweights=w)


def _dist(p):
    dv = np.asarray(p) - _mu
    c2 = float(dv @ np.linalg.solve(_C, dv))
    return dict(chi2=c2, sigma=float(_st.norm.isf(_st.chi2.sf(c2, 2) / 2)))


dist_w0wa = dict(ssee=_dist([_S.W0, _S.WA]), lcdm=_dist([-1.0, 0.0]))
out = dict(fecha=str(__import__("datetime").date.today()), cadenas=f"{BASE}/c1..c4",
           filas_tras_corte=int(len(d)), corte="30 % inicial por cadena",
           posteriores=res, tensiones=tens, distancia_w0wa=dist_w0wa, control=ctrl, control_pasa=all(c["coincide"] for c in ctrl.values()))
json.dump(con_acta(out, __file__, entradas=[f"{BASE}/c{i}/ssee_full.1.txt" for i in (1, 2, 3, 4)] + [LYA]),
          open(os.path.join(R, "results/logs/mcmc_full_posteriores.json"), "w"), indent=1)
for p in PAR:
    print(f"  {p:7s} {res[p]['media']:.5f} ± {res[p]['sigma']:.5f}")
print("  control:", {p: (c["tabla"], round(c["lector"], 5), c["coincide"]) for p, c in ctrl.items()})
