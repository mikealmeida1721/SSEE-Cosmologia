#!/usr/bin/env python3
"""kids_publicados.py — los numeros de KiDS que CANONICAL cita, leidos de los
archivos OFICIALES y de nuestros logs, no tecleados (2026-09-30).

POR QUE. R74 encontro sin fuente cuatro claves de CANONICAL:
  S8_kids_legacy_dato  0.8265 ± 0.0176  «posterior oficial xi± fiducial,
                       calculado de sus muestras (sigma8·sqrt(Om/0.3))»
  chi2_kids_publicado  260.32           mejor ajuste publicado de KiDS-1000
  PTE_kids_ssee        0.0123           chi2 265.40 con 216 dof (R3)
  PTE_kids_lcdm        0.0101           chi2 262.75 con 212 dof (R4)
Aqui se recalculan de su fuente primaria:
  - KiDS-Legacy (Wright+2025, arXiv:2503.19441): cadena nautilus oficial
    output_nautilus_xipm_Fiducial.txt, pesos exp(log_weight).
  - KiDS-1000 (Asgari+2021): maxpost_multinest_start_C.txt, chi2 = -2·like
    (CosmoSIS reporta like = -chi2/2 sin normalizacion; ver control_kids.py).
  - PTE: distribucion chi2 con el chi2_min y los dof de los logs R3/R4.

CONTROL (R53): S8 de Legacy se calcula DOS veces — del parametro muestreado
s_8_input y de sigma8·sqrt(Om/0.3) derivado — y tienen que coincidir a 1e-4;
si no, las columnas no son lo que se dice. (La columna derivada S_8 del
release viene toda en NaN, por eso no se usa.)

Salida: results/logs/kids_publicados.json
"""
import json
import math
import os
import sys

import numpy as np
from scipy.stats import chi2 as _chi2

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "src"))
from procedencia import con_acta  # noqa: E402

LEG = ("/mnt/datos/SSEE_data/kids_legacy/KiDS_Legacy_cosmic_shear_data_release/"
       "chains_and_config_files/xipm/output_nautilus_xipm_Fiducial.txt")
K1K = ("/mnt/datos/SSEE_data/kids1000/KiDS1000_cosmis_shear_data_release/"
       "chains_and_config_files/main_chains_iterative_covariance/xipm/"
       "chain/maxpost_multinest_start_C.txt")
R3 = os.path.join(R, "results/logs/growth_2026-07/R3_ssee_kids_S8.json")
R4 = os.path.join(R, "results/logs/growth_2026-07/R4_lcdm_kids_S8.json")


def _tabla(ruta):
    with open(ruta) as f:
        col = f.readline().lstrip("#").split()
        filas = [ln.split() for ln in f if ln.strip() and not ln.startswith("#")]
    return col, np.array(filas, dtype=float)


# KiDS-Legacy: posterior pesado
col, X = _tabla(LEG)
c = {n: i for i, n in enumerate(col)}
# 1069 filas tienen log_weight = -inf (peso cero) y sigma8 NaN: fuera.
ok = np.isfinite(X[:, c["log_weight"]]) & np.isfinite(X[:, c["COSMOLOGICAL_PARAMETERS--SIGMA_8"]])
X = X[ok]
w = np.exp(X[:, c["log_weight"]] - X[:, c["log_weight"]].max())
w /= w.sum()
# La columna derivada S_8 del release viene TODA en NaN; el control usa
# s_8_input, que es el S8 que el muestreador varia directamente.
s8col = X[:, c["cosmological_parameters--s_8_input"]]
s8calc = X[:, c["COSMOLOGICAL_PARAMETERS--SIGMA_8"]] * np.sqrt(X[:, c["COSMOLOGICAL_PARAMETERS--OMEGA_M"]] / 0.3)
media = float(np.sum(w * s8calc))
sig = float(math.sqrt(np.sum(w * (s8calc - media) ** 2)))
media_col = float(np.sum(w * s8col))

# KiDS-1000: maximo posterior publicado
col1, Y = _tabla(K1K)
like = float(Y[-1, col1.index("like")])

r3, r4 = json.load(open(R3)), json.load(open(R4))
out = dict(
    fecha=str(__import__("datetime").date.today()),
    kids_legacy=dict(S8=media, S8_sigma=sig, S8_columna=media_col,
                     n_muestras=int(len(w)), n_eff=float(1.0 / np.sum(w ** 2)),
                     control_pasa=bool(abs(media - media_col) < 1e-4),
                     fuente="Wright+2025 (arXiv:2503.19441), cadena nautilus oficial"),
    kids1000_maxpost=dict(like=like, chi2=-2.0 * like, fuente="Asgari+2021, maxpost_multinest_start_C"),
    PTE=dict(ssee=dict(chi2=r3["chi2_min"], dof=r3["dof"], PTE=float(_chi2.sf(r3["chi2_min"], r3["dof"])),
                       z=(r3["chi2_min"] - r3["dof"]) / math.sqrt(2 * r3["dof"])),
             lcdm=dict(chi2=r4["chi2_min"], dof=r4["dof"], PTE=float(_chi2.sf(r4["chi2_min"], r4["dof"])),
                       z=(r4["chi2_min"] - r4["dof"]) / math.sqrt(2 * r4["dof"]))))
json.dump(con_acta(out, __file__, entradas=[LEG, K1K, R3, R4]),
          open(os.path.join(R, "results/logs/kids_publicados.json"), "w"), indent=1)
L, P = out["kids_legacy"], out["PTE"]
print(f"  KiDS-Legacy S8 {L['S8']:.4f} ± {L['S8_sigma']:.4f}  (columna {L['S8_columna']:.4f}) control {L['control_pasa']}")
print(f"  KiDS-1000 maxpost chi2 {out['kids1000_maxpost']['chi2']:.2f}")
for k in ("ssee", "lcdm"):
    print(f"  PTE {k}: chi2 {P[k]['chi2']:.2f}/{P[k]['dof']}  PTE {P[k]['PTE']:.4f}  {P[k]['z']:.2f}σ")
