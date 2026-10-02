#!/usr/bin/env python3
"""perfil_h0_ancla.py — ¿dónde se minimiza el χ² del CMB en H₀ con los ω del modelo fijos?

POR QUE (2026-10-01). El Registro y CANONICAL decían «con ω_b, ω_c fijos por
álgebra, plik_lite se MINIMIZA en H = 67.962» y citaban como fuente
results/logs/p3_h0anchor_reframe.log. Ese log lo produce scan_omega_m.py, que
barre Ω_m con H FIJO: no contiene ningún barrido en H₀. El barrido en H₀ que
citaban (66.5→1214, 67.5→1021, 67.962→1005.5, 68.5→1044) era un escaneo
anterior que se sobrescribió al cambiar el script. La afirmación quedó sin log.

QUE HACE. Para cada modelo, con su fondo y sus ingredientes:
  SSEE  ω_b, ω_c, n_s algebraicos, w0/wa del modelo, Σm_ν 0.06849
  LCDM  ω_b, ω_c, n_s de Planck 2018 (lcdm_planck.py), w=-1, Σm_ν 0.06
recorre una rejilla de H₀ y en CADA punto reajusta (logA, τ) con Nelder-Mead
(un PERFIL: fijar A_s y τ en su mejor punto de H_glob sesgaría el mínimo hacia
H_glob). Verosimilitud: plik_lite TTTEEE + lowT + lowE (cmb_eval.chi2_y_s8).
Con los 5 nodos centrales ajusta una parábola: mínimo y ancho (Δχ² = 1).

CONTROL (R53): LCDM con los ω de Planck tiene que poner su mínimo cerca de su
propio H₀ de Planck (67.36 ± 0.54): si no, el perfil no mide lo que dice.

Salida: results/logs/perfil_h0_ancla.json
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import minimize

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
for _d in ("src", "src/p03_cmb", "src/p11_sondas"):
    sys.path.insert(0, os.path.join(_R, _d))
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)
import ssee_core as S  # noqa: E402
from cmb_eval import chi2_y_s8  # noqa: E402
from lcdm_planck import LCDM_PLANCK as P, LOGA_PLANCK, TAU_PLANCK  # noqa: E402

SIG_H0_PLANCK = 0.54   # ORIGEN-VALOR: 0.54 — Planck 2018 VI, Tabla 2 (la columna de lcdm_planck.py)
PASOS = [-1.5, -1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 1.0, 1.5]   # ORIGEN-VALOR: 1.5 — nodos de la rejilla alrededor del centro de cada modelo, elegidos (km/s/Mpc)
_CMB = json.load(open(os.path.join(_R, "results", "logs", "cmb_dbic_tau_ajustado.json")))
MODELOS = {
    "SSEE": dict(fijos=dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2, ns=S.N_S), w=S.W0, wa=S.WA, mnu=S.SUM_MNU_EV,
                 centro=S.H0_GLOBAL, arranque=(_CMB["SSEE"]["mejor"]["logA"], _CMB["SSEE"]["mejor"]["tau"])),
    "LCDM": dict(fijos=dict(ombh2=P["ombh2"], omch2=P["omch2"], ns=P["ns"]), w=-1.0, wa=0.0, mnu=P["mnu"],
                 centro=P["H0"], arranque=(LOGA_PLANCK, TAU_PLANCK)),
}


def perfil(m, H):
    f = lambda x: chi2_y_s8(dict(m["fijos"], H0=H, logA=x[0], tau=x[1]), m["w"], m["wa"], mnu=m["mnu"])[0]
    r = minimize(f, m["arranque"], method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-3, maxiter=400))   # ORIGEN-VALOR: 1e-3 — tolerancia en chi2, mil veces menor que el Δχ²=1 que se lee
    return float(r.fun), [float(v) for v in r.x], bool(r.success)


def _tarea(t):
    nom, d = t
    m = MODELOS[nom]
    H = m["centro"] + d
    c, x, ok = perfil(m, H)
    print(f"  {nom} H0 {H:8.4f}  chi2 {c:10.3f}  logA {x[0]:.4f}  tau {x[1]:.4f}  {'ok' if ok else 'NO CONVERGIO'}", flush=True)
    return nom, dict(H0=H, chi2=c, logA=x[0], tau=x[1], convergio=ok)


# Los 18 puntos (modelo, H0) son independientes: se reparten en NUCLEOS procesos, declarado
# en el comando de la etapa (regla de Mike). El resultado no depende del orden.
NUCLEOS = int(os.environ.get("NUCLEOS", "1"))
print(f"  NUCLEOS: {NUCLEOS}", flush=True)
import multiprocessing as _mp  # noqa: E402
with _mp.get_context("fork").Pool(NUCLEOS) as _pool:
    _res = _pool.map(_tarea, [(n, d) for n in MODELOS for d in PASOS], chunksize=1)
out = {}
for nom, m in MODELOS.items():
    filas = sorted([r for n, r in _res if n == nom], key=lambda r: r["H0"])
    hs = np.array([f["H0"] for f in filas]); cs = np.array([f["chi2"] for f in filas])
    i0 = int(np.argmin(cs)); sel = slice(max(0, i0 - 2), min(len(hs), i0 + 3))
    a, b, _ = np.polyfit(hs[sel], cs[sel], 2)
    hmin = -b / (2 * a); sig = 1 / np.sqrt(a)
    out[nom] = dict(filas=filas, H0_min_parabola=float(hmin), sigma_H0=float(sig), chi2_nodo_min=float(cs[i0]),
                    H0_nodo_min=float(hs[i0]), minimo_interior=bool(0 < i0 < len(hs) - 1),
                    todos_convergieron=all(f["convergio"] for f in filas))
    print(f"  {nom}: minimo {hmin:.3f} ± {sig:.3f} (parabola en {sel.stop - sel.start} nodos)", flush=True)

s = out["SSEE"]; l = out["LCDM"]
s["distancia_a_Hglob_sigma"] = float(abs(s["H0_min_parabola"] - S.H0_GLOBAL) / s["sigma_H0"])
l["distancia_a_H0_planck_sigma"] = float(abs(l["H0_min_parabola"] - P["H0"]) / np.hypot(l["sigma_H0"], SIG_H0_PLANCK))
pasa = l["minimo_interior"] and l["todos_convergieron"] and l["distancia_a_H0_planck_sigma"] < 1.0
out["control"] = dict(criterio="LCDM con los omega de Planck pone su minimo a < 1 sigma de su H0 de Planck (67.36 +- 0.54), interior y convergido",
                      pasa=bool(pasa))
print(f"  SSEE a {s['distancia_a_Hglob_sigma']:.2f} sigma de H_glob · control LCDM a {l['distancia_a_H0_planck_sigma']:.2f} sigma de Planck -> {'PASA' if pasa else 'NO PASA'}")
json.dump(con_acta(out, __file__, entradas=[os.path.join(_R, "results", "logs", "cmb_dbic_tau_ajustado.json")]),
          open(os.path.join(_R, "results", "logs", "perfil_h0_ancla.json"), "w"), indent=1)
if not pasa:
    sys.exit("control NO PASA")
