#!/usr/bin/env python3
"""ppc_cronometros.py — chequeo predictivo H(z) de Paper 2 contra los 32 cronómetros (2026-10-02).

POR QUE. ssee_paper2_mcmc.py hacía este chequeo con 11 puntos tecleados dentro del
script (CC_DATA). Uno de ellos, z=0.44 con H=82.6±7.8, no es un cronómetro: es el
H(z) de BAO de WiggleZ (Blake+2012). Paper 2 lo presenta como «model-independent
Cosmic Chronometer measurements». Además, el paper citaba 0.482/0.471 cuando el log
vigente del MCMC imprimía 0.479/0.472.
Aquí los datos se leen de data/raw/cosmic_chronometers.csv (los 32 puntos de
Moresco+2022, cotejados por coteja_crudos.py), y el MAP de cada modelo se lee de
las cadenas que guardó el MCMC. No se re-corre ninguna cadena: el chequeo es
predictivo y los cronómetros no entran en el posterior.

COMO. Las MISMAS fórmulas que ssee_paper2_mcmc.py, sección 8:
  MAP = la muestra de ln P máximo en la cadena guardada;
  SSEE: H = H0·E(z; Ω_m = ω_m/h²), con ω_m algebraico; ΛCDM y CPL: su E(z) con su MAP;
  χ²_r = Σ((H_pred − H_obs)/σ)² / N  (dividido por N, no por N−k: nada se ajusta a H(z)).
Sólo la diagonal: Moresco+2022 pide usar la covarianza sistemática completa, y su
código no está en el repositorio. El CSV lo dice en su cabecera.

CONTROL (R53). (1) Con los 11 puntos viejos, leídos de ssee_paper2_mcmc.py EN EL COMMIT b14ff14,
este script tiene que reproducir el χ²_r que imprime el log del MCMC
(mcmc_paper2_3models_wmfix.log), a su precisión de 3 decimales. Eso prueba que el
MAP y E(z) son los mismos y que el cambio viene sólo de los datos.
(2) El otro lado: el mismo cálculo sin el punto de WiggleZ, para medir cuánto pesaba.
"""
import ast
import json
import os
import re
import sys

import numpy as np
from scipy.stats import chi2 as _chi2

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from ssee_core import W0, WA, OMEGA_M_H2  # noqa: E402
from procedencia import con_acta, cabecera  # noqa: E402

NPZ = "/mnt/datos/SSEE_data/mcmc/paper2_3models/mcmc_chains_professional.npz"
CSV = os.path.join(_R, "data", "raw", "cosmic_chronometers.csv")
COMMIT_VIEJO = "b14ff14"   # ORIGEN-VALOR: b14ff14 — ultimo commit en que ssee_paper2_mcmc.py lleva CC_DATA tecleado (el log del MCMC se corrio con esos 11)
VIEJO = "src/p02_mcmc/ssee_paper2_mcmc.py"
LOG = os.path.join(_R, "results", "logs", "mcmc_paper2_3models_wmfix.log")
SALIDA = os.path.join(_R, "results", "logs", "ppc_cronometros.json")
TABLA = os.path.join(_R, "manuscript", "tabla_cronometros_generada.tex")
Z_WIGGLEZ = 0.44   # ORIGEN-VALOR: 0.44 — z del H(z) BAO de WiggleZ (Blake+2012, MNRAS 425, 405, Tabla 2) dentro de CC_DATA


def f_de(z, w0, wa):
    a = 1.0 / (1.0 + z)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))


def H_pred(m, th, z):
    if m == "ssee":
        Om = OMEGA_M_H2 / (th[0] / 100) ** 2
        return th[0] * np.sqrt(Om * (1 + z) ** 3 + (1 - Om) * f_de(z, W0, WA))
    if m == "lcdm":
        return th[0] * np.sqrt(th[1] * (1 + z) ** 3 + 1 - th[1])
    return th[0] * np.sqrt(th[1] * (1 + z) ** 3 + (1 - th[1]) * f_de(z, th[2], th[3]))


def chi2(m, th, z, h, s):
    return float(np.sum(((H_pred(m, th, z) - h) / s) ** 2))


d = np.load(NPZ)
MAP = {m: d[f"{m}_flat"][np.argmax(d[f"{m}_lp"])] for m in ("ssee", "lcdm", "cpl")}

# los 32 de Moresco+2022
import csv as _csv  # noqa: E402
filas = list(_csv.DictReader(l for l in open(CSV) if not l.startswith("#")))
z32, h32, s32 = (np.array([float(f[c]) for f in filas]) for c in ("z", "Hz", "sigma_Hz"))

# los 11 viejos, leídos literalmente del script que los usaba
src = __import__("subprocess").run(["git", "show", f"{COMMIT_VIEJO}:{VIEJO}"], cwd=_R, capture_output=True, text=True, check=True).stdout
bloque = re.search(r"CC_DATA = np\.array\((\[.*?\])\)", src, re.S).group(1)
viejo = np.array(ast.literal_eval(bloque))
z11, h11, s11 = viejo.T
sin_wz = ~np.isclose(z11, Z_WIGGLEZ)

res = {}
for m, th in MAP.items():
    c32 = chi2(m, th, z32, h32, s32)
    c11 = chi2(m, th, z11, h11, s11)
    c10 = chi2(m, th, z11[sin_wz], h11[sin_wz], s11[sin_wz])
    res[m] = dict(theta_map=[float(x) for x in th],
                  chi2_32=c32, N_32=len(z32), chi2r_32=c32 / len(z32),
                  p_32=float(_chi2.sf(c32, len(z32))),
                  chi2r_11_viejos=c11 / len(z11),
                  chi2r_10_sin_wigglez=c10 / int(sin_wz.sum()))
for m in res:
    res[m]["dchi2_32_ssee_menos"] = res["ssee"]["chi2_32"] - res[m]["chi2_32"]

# CONTROL 1: el log del MCMC
txt = open(LOG).read()
blq = txt[txt.index("Cosmic Chronometers"):]
ETIQ = {"ssee": "SSEE", "lcdm": "ΛCDM", "cpl": "CPL"}
impreso = {m: float(re.search(rf"{e}\s*:\s*([0-9.]+)", blq).group(1)) for m, e in ETIQ.items()}
pasa = all(abs(res[m]["chi2r_11_viejos"] - impreso[m]) <= 0.0005 + 1e-9 for m in res)

out = dict(
    datos=dict(csv=os.path.relpath(CSV, _R), N=len(z32), covarianza="solo diagonal (la fuente pide la sistematica completa)"),
    convencion="chi2_r = chi2/N; MAP de cada modelo en el MCMC de 3 modelos de Paper 2 (prior Planck comprimido)",
    modelos=res,
    wigglez=dict(z=Z_WIGGLEZ, nota="H(z) BAO de WiggleZ (Blake+2012), no es un cronometro; estaba en CC_DATA"),
    control=dict(log=os.path.relpath(LOG, _R), puntos_11=f"git:{COMMIT_VIEJO}:{VIEJO}", impreso_11=impreso, pasa=bool(pasa)))
json.dump(con_acta(out, __file__, entradas=[NPZ, CSV, LOG]), open(SALIDA, "w"), indent=1)

# la tabla de Paper 2, del mismo CSV (antes 23 filas tecleadas, distintas de las 11 del chequeo)
METODO = {"F": "F", "D": "D", "L": "L"}
with open(TABLA, "w") as t:
    t.write(cabecera(__file__, entradas=[CSV], comentario="%") + "\n")
    for f in filas:
        t.write(f"{float(f['z']):.4g} & {float(f['Hz']):.1f} & {float(f['sigma_Hz']):.1f} & {METODO[f['metodo']]} \\\\\n")
for m, r in res.items():
    print(f"{ETIQ[m]:5s} 32: chi2={r['chi2_32']:.3f} chi2_r={r['chi2r_32']:.3f} p={r['p_32']:.3f} | "
          f"11 viejos {r['chi2r_11_viejos']:.4f} (log {impreso[m]}) | sin WiggleZ {r['chi2r_10_sin_wigglez']:.3f}")
print("CONTROL:", "PASA" if pasa else "NO PASA")
sys.exit(0 if pasa else 1)
