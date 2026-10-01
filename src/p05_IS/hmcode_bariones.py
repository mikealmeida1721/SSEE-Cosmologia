#!/usr/bin/env python3
"""hmcode_bariones.py — la supresion barionica (HMcode-2020) que cita Paper 5, con log.

POR QUE (2026-10-01). Paper 5 (§S8) cita B_eff = 0.9447 (supresion de P(k) en el
rango de lensing), B_sigma8 = 0.9956 (la que actua sobre sigma_8) y el techo
corregido S8 ~ 0.824. Salian de src/.../ssee_op5_hmcode.py, ARCHIVADO, corrido
en mayo sobre el fondo de la epoca MIRA (H0 = 66.75, Omega_m = 0.3199) y sin log.

QUE HACE. Dos corridas CLASS por fondo: HMcode-2020 y HMcode-2020 con
retroalimentacion barionica; la receta es la del script archivado, tal cual:
  B_eff    = int k (P_bar/P_NL) dk / int k dk,     k = 0.03..2 h/Mpc (300 puntos log)
  B_sigma8 = sqrt( int k^2 P_bar W^2 / int k^2 P_NL W^2 ),  top-hat R = 8 Mpc/h, mismo rango
FONDOS:
  canonico  config/class/techo_ssee_canonico.ini (el del techo de P5, A_s de Planck).
  mayo      las entradas del script archivado (control).
Y el techo corregido: S8_techo (p5_techo_sigma8_As_fijo.json) * B_sigma8.
CONTROL (R53): el fondo de mayo tiene que reproducir su B_eff publicado, 0.9447,
a la cuarta cifra; si no, la receta no es la misma y nada de lo de abajo vale.

Salida: results/logs/hmcode_bariones.json
"""
import json
import os
import sys

import numpy as np
from classy import Class

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)   # acta de procedencia: primera linea del log

INI = os.path.join(_R, "config", "class", "techo_ssee_canonico.ini")
TECHO = os.path.join(_R, "results", "logs", "p5_techo_sigma8_As_fijo.json")
ARCH = os.path.join(_R, "archive", "codigo", "investigacion", "open_problems", "ssee_op5_hmcode.py")
K = np.logspace(np.log10(0.03), np.log10(2.0), 300)   # ORIGEN-VALOR: 0.03, 2.0, 300 — rango y rejilla de lensing del script archivado
R8 = 8.0
B_EFF_MAYO = 0.9447   # ORIGEN-VALOR: 0.9447 — B_eff que P5 cita del script archivado (corrida de mayo, sin log)


def lee_ini(ruta):
    p = {}
    for ln in open(ruta):
        ln = ln.split("#")[0].strip()
        if "=" in ln:
            k, v = (x.strip() for x in ln.split("=", 1))
            if k not in ("root", "overwrite_root", "write_parameters"):
                p[k] = v
    return p


# Fondo de mayo: las entradas del script archivado, leidas de su fuente
_ns = {}
_src = open(ARCH).read()
exec(_src[_src.index("# ── Constantes algebraicas"):_src.index("# Baseline Paper 6")], {"np": np}, _ns)
MAYO = dict(H0=_ns["H0_ssee"], omega_b=_ns["Omb_h2"], omega_cdm=_ns["omch2"], Omega_fld=_ns["Omega_fld"],
            w0_fld=_ns["w0_ssee"], wa_fld=_ns["wa_ssee"], cs2_fld=1.0, n_s=_ns["n_s_ssee"], A_s=_ns["A_s_ssee"])


def W(x):
    return 3.0 * (np.sin(x) - x * np.cos(x)) / x ** 3


def supresion(base):
    pk = {}
    for v in ("2020", "2020_baryonic_feedback"):
        c = Class()
        c.set(dict(base, output="mPk", z_pk=0.0, **{"P_k_max_h/Mpc": 10.0}, non_linear="hmcode", hmcode_version=v))
        c.compute()
        h = c.h()
        pk[v] = np.array([c.pk(k * h, 0.0) * h ** 3 for k in K])
        c.struct_cleanup()
        c.empty()
    r = pk["2020_baryonic_feedback"] / pk["2020"]
    w2 = W(K * R8) ** 2
    return dict(B_eff=float(np.trapezoid(K * r, K) / np.trapezoid(K, K)),
                B_sigma8=float(np.sqrt(np.trapezoid(K ** 2 * pk["2020_baryonic_feedback"] * w2, K)
                                       / np.trapezoid(K ** 2 * pk["2020"] * w2, K))))


can = supresion({k: v for k, v in lee_ini(INI).items() if k not in ("output", "z_pk", "P_k_max_h/Mpc", "k_per_decade_for_pk")})
may = supresion(MAYO)
for d in (can, may):
    d["pct_P"] = 100 * (1 - d["B_eff"])
    d["pct_sigma8"] = 100 * (1 - d["B_sigma8"])
techo = json.load(open(TECHO))["S8_techo"]
pasa = round(may["B_eff"], 4) == B_EFF_MAYO
out = dict(fecha=str(__import__("datetime").date.today()), canonico=can, mayo=may,
           S8_techo=techo, S8_techo_bar=techo * can["B_sigma8"],
           control=dict(B_eff_mayo_publicado=B_EFF_MAYO, B_eff_mayo_rehecho=may["B_eff"], pasa=bool(pasa)))
json.dump(con_acta(out, __file__, entradas=[INI, TECHO, ARCH]),
          open(os.path.join(_R, "results", "logs", "hmcode_bariones.json"), "w"), indent=1)
print(f"  canonico: B_eff {can['B_eff']:.5f}  B_sigma8 {can['B_sigma8']:.5f}  S8 techo {techo:.4f} -> {out['S8_techo_bar']:.4f}")
print(f"  mayo    : B_eff {may['B_eff']:.5f}  B_sigma8 {may['B_sigma8']:.5f}")
print(f"  control: B_eff de mayo {may['B_eff']:.4f} vs publicado {B_EFF_MAYO} -> {'PASA' if pasa else 'NO PASA'}")
