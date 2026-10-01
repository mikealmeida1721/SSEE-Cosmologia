#!/usr/bin/env python3
"""analiza_ssee_R3.py — la lectura de la cadena R3 (SSEE, KiDS-1000), con script.

POR QUE (2026-09-30). results/logs/growth_2026-07/R3_ssee_kids_S8.json es la
fuente de Paper 6 para KiDS-1000 (S8 = 0.7555 +- 0.0192, chi2_min 265.44,
y de ahi Delta chi2, AIC, BIC y PTE en kids_publicados.py). Entro el
2026-08-01 (commit 7866edc) como lectura hecha a mano: sin el script que la
produjo. R4 si tenia el suyo (analiza_lcdm_R4.py). Este es el de R3.

COMO (el metodo que el propio log declara):
  - cadenas /mnt/datos/SSEE_data/chains_p6/kids/ssee.{1-4}.txt, burn-in 30 %
    de las filas de CADA cadena, pesos de Cobaya;
  - medias y sigmas pesadas de logA y de los nuisance;
  - sigma8 = sigma8_ref * sqrt(A_s / A_s_ref), con sigma8_ref de CAMB en el
    fondo fijo de SSEE (valido porque el fondo NO varia en la cadena);
  - S8 = sigma8 * sqrt(Omega_m / 0.3), Omega_m de los parametros de CAMB;
  - chi2: media pesada y minimo sobre las filas post burn-in; dof = 225 - 9.
CONTROL (R53): cada numero se compara con el del log viejo. Los que dependen
solo de la cadena tienen que coincidir a 1e-6 relativo; sigma8/S8 dependen
ademas de CAMB en el fondo, que cambio de H0_ALG a H0_GLOBAL el 09-28 (4e-6),
asi que se les pide 1e-4 relativo. Si algo no pasa, se escribe igual el log
pero con `control.pasa = false` y se dice.

Salida: results/logs/growth_2026-07/R3_ssee_kids_S8.json (misma estructura).
"""
import glob
import json
import math
import os
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p06_growth"))
import cobaya_kids as CK  # noqa: E402
import kids_shear as K  # noqa: E402
from procedencia import con_acta  # noqa: E402

CAD = "/mnt/datos/SSEE_data/chains_p6/kids"
OUT = os.path.join(_R, "results", "logs", "growth_2026-07", "R3_ssee_kids_S8.json")
BURN = 0.30
N_DATOS = 225   # ORIGEN-VALOR: 225 — puntos xi+- de KiDS-1000 tras la mascara de escalas (el log viejo, campo "datos")
AS_REF = 2.1e-9  # ORIGEN-VALOR: 2.1e-9 — A_s de referencia de la calibracion sqrt(A_s), el que declara el log viejo

viejo = json.load(open(OUT))
rutas = sorted(glob.glob(f"{CAD}/ssee.[1-4].txt"))
with open(rutas[0]) as f:
    col = f.readline().lstrip("#").split()
bloques, lineas = [], []
for r in rutas:
    X = np.loadtxt(r)
    lineas.append(len(X))
    bloques.append(X[int(BURN * len(X)):])
X = np.vstack(bloques)
c = {n: i for i, n in enumerate(col)}
w = X[:, c["weight"]]


def mom(v):
    m = float(np.sum(w * v) / np.sum(w))
    return dict(media=m, sigma=float(math.sqrt(np.sum(w * (v - m) ** 2) / np.sum(w))))


bg = CK.SSEE_BG
r0, = K.run_camb(omch2=bg["omch2"], ombh2=bg["ombh2"], h0=bg["h0"], ns=bg["ns"], As=AS_REF,
                 mnu=bg["mnu"], w=bg["w0"], wa=bg["wa"], logT_AGN=7.8)[:1]   # ORIGEN-VALOR: 7.8 — logT_AGN de relleno: sigma8 es LINEAL
p = r0.Params
om = (p.omch2 + p.ombh2 + p.omnuh2) / (p.H0 / 100.0) ** 2
s8ref = float(r0.get_sigma8_0())
As = np.exp(X[:, c["logA"]]) * 1e-10
sg8 = s8ref * np.sqrt(As / AS_REF)
chi2 = X[:, c["chi2"]]
nuevo = dict(viejo)
nuevo.update(
    lineas_por_cadena=lineas, burn_in_frac=BURN, n_filas_post_burnin=int(len(X)),
    n_efectivas=float(np.sum(w)), logA=mom(X[:, c["logA"]]), sigma8=mom(sg8),
    S8=mom(sg8 * math.sqrt(om / 0.3)), chi2=mom(chi2),
    **{k: mom(X[:, c[k]]) for k in ("halo_A", "A_IA", "dz1", "dz2", "dz3", "dz4", "dz5", "delta_c")},
    chi2_min=float(chi2.min()), dof=N_DATOS - len(viejo["parametros_libres"]),
    chi2_min_por_dof=float(chi2.min()) / (N_DATOS - len(viejo["parametros_libres"])),
    fondo_fijo=dict(viejo["fondo_fijo"], Omega_m=om),
    sigma8_ref_calibracion=dict(viejo["sigma8_ref_calibracion"], sigma8_ref=s8ref, As_ref=AS_REF))
nuevo["comparacion_KiDS"] = dict(viejo["comparacion_KiDS"])
nuevo["comparacion_KiDS"]["tension_sigma"] = (nuevo["S8"]["media"] - viejo["comparacion_KiDS"]["S8_publicado"]) / \
    math.hypot(nuevo["S8"]["sigma"], viejo["comparacion_KiDS"]["err_publicado"])

# CONTROL campo por campo
fallos, tol_cadena, tol_camb = [], 1e-6, 1e-4
for k in ("logA", "chi2", "halo_A", "A_IA", "dz1", "dz2", "dz3", "dz4", "dz5", "delta_c", "sigma8", "S8"):
    tol = tol_camb if k in ("sigma8", "S8") else tol_cadena
    for s in ("media", "sigma"):
        a, b = viejo[k][s], nuevo[k][s]
        if abs(a - b) > tol * max(abs(a), 1e-12):
            fallos.append(f"{k}.{s}: viejo {a} nuevo {b}")
for k in ("chi2_min", "n_efectivas", "n_filas_post_burnin"):
    if abs(viejo[k] - nuevo[k]) > tol_cadena * abs(viejo[k]):
        fallos.append(f"{k}: viejo {viejo[k]} nuevo {nuevo[k]}")
if viejo["lineas_por_cadena"] != lineas:
    fallos.append(f"lineas_por_cadena: viejo {viejo['lineas_por_cadena']} nuevo {lineas}")
nuevo["control_contra_log_viejo"] = dict(pasa=not fallos, fallos=fallos,
                                         tolerancias=dict(cadena=tol_cadena, camb=tol_camb))
nuevo["fecha_analisis"] = str(__import__("datetime").datetime.now().isoformat(timespec="seconds"))
json.dump(con_acta(nuevo, __file__, entradas=rutas), open(OUT, "w"), indent=1)
print(f"  S8 {nuevo['S8']['media']:.4f} ± {nuevo['S8']['sigma']:.4f}  sigma8 {nuevo['sigma8']['media']:.4f}"
      f"  chi2_min {nuevo['chi2_min']:.5f}  N_eff {nuevo['n_efectivas']:.0f}")
print(f"  control contra el log viejo: {'PASA' if not fallos else 'NO PASA'}")
for x in fallos:
    print("   ", x)
