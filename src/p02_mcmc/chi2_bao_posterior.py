#!/usr/bin/env python3
"""chi2_bao_posterior.py — χ²_BAO evaluado en el posterior (13 puntos DESI DR2).

POR QUÉ EXISTE (2026-07-25)
---------------------------
El PRD §3 afirma «χ²_BAO ≈ 10.3 over 13 points, against ≈726 for the incorrect
background geometry». El 726 lo remacha el canario R14 del guardián, pero el
**10.3 no lo producía ningún script con log**: era un número correcto sin fuente
reproducible — la misma grieta que la Capa Procedencia existe para cazar.

Este script lo recomputa desde las MISMAS fuentes que usa todo lo demás
(`desi_dr2_data` como loader único + `ssee_core` para el álgebra), con la
parametrización R25: **ω_m algebraico FIJO y Ω_m = ω_m/h² DERIVADO por muestra**.
Congelar Ω_m fabrica un ω_m que SSEE no predice y sesga el resultado hacia el
ancla; ese fue el bug que R25 vigila.

Se reportan tres puntos para que la comparación sea legible:
  · el posterior canónico (67.7869, ω_b h² = 0.02207)
  · el ancla algebraica    (67.9621)
  · el posterior superado  (67.9475, Ω_m congelado) — para ver que el χ² MEJORA
    al corregir la parametrización, no empeora.

Uso:  .venv/bin/python3 src/p02_mcmc/chi2_bao_posterior.py
"""
# ORIGEN-VALOR: 0.1432 — pivote omega_m h^2 de la eq. rd de Paper 2 (Planck 2018 TT,TE,EE+lowE); cita EH98 en FUENTES_PENDIENTES.md FP-7
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "src"))

import desi_dr2_data as D                                    # noqa: E402
from ssee_core import W0, WA, OMEGA_M_H2                     # noqa: E402

LOG = os.path.join(_REPO, "results", "logs", "chi2_bao_posterior.log")
CKM = 2.998e5

_d = D.load_desi_dr2()
_C = D.desi_covariance(_d)
_Cinv = np.linalg.inv(_C)
_Z, _Q, _OBS = list(_d["z"]), list(_d["quantity"]), _d["value"]


def _fde(z):
    a = 1.0 / (1.0 + z)
    return (1 + z) ** (3 * (1 + W0 + WA)) * np.exp(-3 * WA * (1 - a))


def _E(z, Om):
    return np.sqrt(Om * (1 + z) ** 3 + (1 - Om) * _fde(z))


def _DC(zm, Om, n=400):
    zz = np.linspace(0, zm, n)
    return np.trapezoid(1.0 / _E(zz, Om), zz)


import os as _os_rd, sys as _sys_rd
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), ".."))
from rd_camb import rd_mpc as _rd_camb  # r_d de CAMB, una sola funcion (2026-09-28)


def _rd(obh2, omh2):
    """r_d Eisenstein–Hu calibrado; ω_m es el ALGEBRAICO, no Ω_m·h²."""
    return _rd_camb(obh2, omh2, mnu=None)  # CAMB; antes 147.27*(...) con normalizacion 0.15 % alta


from bao_camb import chi2_desi as _chi2_camb  # D_M, D_H de CAMB (2026-09-28)


def chi2_bao(H0, obh2):
    """chi2 BAO con D_M, D_H y r_d de CAMB (antes: E(z) analitico + r_d por formula)."""
    Om = OMEGA_M_H2 / (H0 / 100.0) ** 2          # DERIVADO por muestra (R25)
    return _chi2_camb(H0, _rd(obh2, OMEGA_M_H2)), Om


_out = []


def log(s):
    print(s)
    _out.append(s)


log("χ²_BAO en el posterior — DESI DR2, parametrización R25 (ω_m fijo, Ω_m derivado)")
log(f"  ω_m algebraico = {OMEGA_M_H2:.6f}   (w₀={W0:.6f}, wₐ={WA:.6f})")
log(f"  {len(_Z)} puntos, covarianza block-diagonal con los r_MH oficiales")
log("")
log(f"  {'escenario':34s} {'H₀':>9s} {'ω_b h²':>8s} {'Ω_m deriv':>10s} {'χ²_BAO':>8s}")
# ORIGEN: results/logs/mcmc_paper2_reframe.json (el posterior, leido; antes estaba tecleado)
import json as _json
from ssee_core import H0_ALG as _HALG, OMEGA_B_H2 as _OBH2
_post = _json.load(open(os.path.join(_REPO, "results", "logs", "mcmc_paper2_reframe.json")))
_filas = []
for _etq, _H0, _ob in (
        ("posterior canónico (R25)", _post["H0_mediana"], _post["obh2_mediana"]),
        ("ancla algebraica 3(φ+π)²", _HALG, _OBH2)):
    _c, _Om = chi2_bao(_H0, _ob)
    _filas.append(_c)
    log(f"  {_etq:34s} {_H0:9.4f} {_ob:8.5f} {_Om:10.6f} {_c:8.2f}")
log("")
_d = _filas[0] - _filas[1]
log(f"  Lectura: el posterior ajusta BAO {'mejor' if _d < 0 else 'peor'} que el ancla "
    f"algebraica por {abs(_d):.2f} en chi2 (13 puntos).")
log("  D_M, D_H y r_d de CAMB (bao_camb.py, rd_camb.py), 2026-09-28. Con la formula")
log("  de r_d y el E(z) analitico el chi2 salia ~0.5 mas bajo; ver lcdm_conjunta C3.")
log("  El contraste con χ²≈725 (sector frío 0.160 en E(z)) lo vigila R14.")

with open(LOG, "w", encoding="utf-8") as _fh:
    _fh.write("\n".join(_out) + "\n")
print(f"\nlog: {os.path.relpath(LOG, _REPO)}")
