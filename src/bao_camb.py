#!/usr/bin/env python3
"""bao_camb.py — distancias DESI DR2 de SSEE con CAMB, tabuladas en H0.

POR QUE (2026-09-28). chi2_bao_posterior.py y el MCMC de Paper 2 calculaban
D_M y D_H con un E(z) analitico SIN radiacion ni neutrinos masivos. Difiere
de CAMB en ~1e-4, pero eso vale 0.17 en chi2 (11.576 analitico contra 11.406
CAMB con el mismo r_d; control C3 de lcdm_conjunta.py). Junto con r_d
(rd_camb.py) cierra la diferencia entera.

METODO. En el MCMC de Paper 2 w_m es el ALGEBRAICO fijo y Omega_m = w_m/h^2
se deriva por muestra, asi que el fondo depende SOLO de H0 (w_b no mueve el
fondo a w_m fijo). Se tabula D_M(z_i) y D_H(z_i) de CAMB (PPF, w0-wa y mnu de
SSEE) en una rejilla de H0 y se interpola. Fuera de la rejilla, falla.

CONTROL R53 (`verifica`), criterio declarado antes:
  (a) interpolado vs CAMB directo en H0 al azar: error < 1e-5 relativo;
  (b) en el clavo, con r_d de CAMB, reproduce el 11.406 del control C3 de
      lcdm_conjunta (results/logs/lcdm_conjunta_control.json) a < 1e-3.

Uso: from bao_camb import pred_desi, chi2_desi
"""
import json
import os

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_TABLA = os.path.join(_R, "data", "processed", "bao_camb_ssee.json")
_LOG = os.path.join(_R, "results", "logs", "bao_camb_control.json")
H0_REJ = np.round(np.arange(55.0, 80.0001, 0.05), 4)   # ORIGEN-VALOR: 55-80 — contiene el posterior de P2 (67.8 +- 0.35) con > 30 sigma de margen
_T = None


_D = None


def _desi():
    global _D
    if _D is None:
        from desi_dr2_data import desi_covariance, load_desi_dr2
        d = load_desi_dr2()
        _D = (np.asarray(d["z"], float), np.asarray(d["type"]),
              np.asarray(d["value"], float), np.linalg.inv(desi_covariance(d)))
    return _D


def _camb_dist(H0):
    import camb
    from astropy import constants as const
    from ssee_core import OMEGA_B_H2, OMEGA_C_H2, SUM_MNU_EV, W0, WA
    z = _desi()[0]
    p = camb.set_params(H0=H0, ombh2=OMEGA_B_H2, omch2=OMEGA_C_H2, mnu=SUM_MNU_EV,
                        w=W0, wa=WA, dark_energy_model="ppf")
    r = camb.get_background(p)
    return r.comoving_radial_distance(z), const.c.to("km/s").value / r.hubble_parameter(z)


def _tabla():
    global _T
    if _T is None:
        from scipy.interpolate import CubicSpline
        t = json.load(open(_TABLA)) if os.path.exists(_TABLA) else None
        if t is None or t["H0"] != H0_REJ.tolist():
            dm, dh = zip(*[_camb_dist(h) for h in H0_REJ])
            t = dict(H0=H0_REJ.tolist(), DM=np.array(dm).tolist(), DH=np.array(dh).tolist())
            os.makedirs(os.path.dirname(_TABLA), exist_ok=True)
            json.dump(t, open(_TABLA, "w"))
        _T = (CubicSpline(t["H0"], np.array(t["DM"]), axis=0),
              CubicSpline(t["H0"], np.array(t["DH"]), axis=0))
    return _T


def en_rango(H0):
    return H0_REJ[0] <= H0 <= H0_REJ[-1]


def pred_desi(H0, rd):
    if not en_rango(H0):
        raise ValueError(f"H0={H0} fuera de la tabla CAMB ({H0_REJ[0]}-{H0_REJ[-1]})")
    fm, fh = _tabla()
    z, t = _desi()[:2]
    dm, dh = fm(H0), fh(H0)
    return np.where(t == 0, dm, np.where(t == 1, dh, (z * dm ** 2 * dh) ** (1 / 3))) / rd


def chi2_desi(H0, rd):
    obs, Ci = _desi()[2:]
    r = pred_desi(H0, rd) - obs
    return float(r @ Ci @ r)


def verifica():
    from rd_camb import rd_mpc
    from ssee_core import H0_GLOBAL, OMEGA_B_H2, OMEGA_M_H2
    rng = np.random.default_rng(20260928)            # ORIGEN-VALOR: semilla fija (la fecha)
    peor = 0.0
    for h in rng.uniform(56, 79, 10):
        dm, dh = _camb_dist(h)
        fm, fh = _tabla()
        peor = max(peor, np.abs(fm(h) / dm - 1).max(), np.abs(fh(h) / dh - 1).max())
    c = chi2_desi(H0_GLOBAL, rd_mpc(OMEGA_B_H2, OMEGA_M_H2))
    ref = json.load(open(os.path.join(_R, "results", "logs", "lcdm_conjunta_control.json")))["C3"]["ssee_camb"]
    pasa = bool(peor < 1e-5 and abs(c - ref) < 1e-3)
    json.dump(dict(fecha="2026-09-28", error_max_rel=float(peor), chi2_clavo=c, ref_C3=ref,
                   criterio="(a) < 1e-5 relativo; (b) |chi2 - C3| < 1e-3 (declarado antes)",
                   pasa=pasa), open(_LOG, "w"), indent=1)
    print(f"  (a) error max interpolado vs CAMB: {peor:.2e}")
    print(f"  (b) chi2 en el clavo {c:.4f} vs C3 {ref:.4f}  -> {'PASA' if pasa else 'NO PASA'}")
    return pasa


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(0 if verifica() else 1)
