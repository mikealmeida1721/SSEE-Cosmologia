#!/usr/bin/env python3
"""rd_camb.py — el horizonte de sonido r_d, UNA sola funcion para todo el repo.

POR QUE (2026-09-28). Once scripts llevaban su propia copia de
    r_d = 147.27 (w_m/0.1432)^-0.255 (w_b/0.02237)^-0.134 Mpc
Los exponentes son las derivadas locales en el pivote (verificado 2026-09-19,
results/logs/formula_rd_exponentes.log), pero la NORMALIZACION no: en ese
mismo pivote CAMB integra 147.05 Mpc, no 147.27 (+0.15 %). Lo cazo el control
C3 de lcdm_conjunta.py: el chi2 BAO de SSEE daba 10.904 con la formula y 11.406
con CAMB, y toda la diferencia era r_d.

Primer intento (descartado, mismo dia): la ley de potencias con normalizacion
y exponentes de CAMB. En el punto de SSEE daba -0.015 %, pero en las esquinas
de la rejilla 0.070 %, por encima del criterio declarado de 0.05 %. No se movio
el criterio: se cambio el metodo.

METODO. r_d de CAMB tabulado en una rejilla (w_b, w_m) con la masa de
neutrinos de cada modelo, e interpolado con un spline bicubico. La tabla se
calcula una vez y se guarda; si falta, se rehace.

CONTROL R53 (`verifica`): interpolado contra CAMB directo en puntos al azar
dentro de la rejilla y en el punto de SSEE. Criterio declarado antes: error
maximo < 0.001 %.

Uso:  from rd_camb import rd_mpc      rd_mpc(ob_h2, om_h2, mnu=<masa del modelo>)
      python3 src/rd_camb.py           (construye la tabla, corre el control)
"""
import json
import os

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_TABLA = os.path.join(_R, "data", "processed", "rd_camb_tabla.json")
_LOG_CTRL = os.path.join(_R, "results", "logs", "rd_camb_control.json")
# Rejilla ANCHA: el MCMC LCDM de P2 recorre w_m = Om h^2 lejos de 0.14, y el
# canario R14 del guardian evalua el sector 0.160 (w_m ~ 0.05). Fuera de la
# rejilla la funcion FALLA en voz alta: un spline no extrapola en silencio.
WB = np.linspace(0.010, 0.035, 26)       # ORIGEN-VALOR: 0.010-0.035 — contiene el prior de w_b de los MCMC de P2 (0.015-0.030)
WM = np.linspace(0.040, 0.260, 45)       # ORIGEN-VALOR: 0.040-0.260 — contiene el canario R14 y el recorrido LCDM de P2
_SPL = {}


def _camb(wb, wm, mnu):
    import camb
    # h no entra en r_d a w fijos; omega_nu = mnu/93.14 es la conversion de CAMB
    p = camb.set_params(H0=67.36, ombh2=wb, omch2=wm - wb - mnu / 93.14,  # ORIGEN-VALOR: 67.36 y 93.14 — ver comentario
                        mnu=mnu, As=2.1e-9, ns=0.965)
    return camb.get_background(p).get_derived_params()["rdrag"]


def _tabla():
    t = json.load(open(_TABLA)) if os.path.exists(_TABLA) else {}
    # una tabla hecha con otra rejilla no vale: se descarta entera
    return {k: v for k, v in t.items() if v.get("WB") == WB.tolist() and v.get("WM") == WM.tolist()}


def _spline(mnu):
    from scipy.interpolate import RectBivariateSpline
    k = f"{float(mnu):.6f}"
    if k in _SPL:
        return _SPL[k]
    t = _tabla()
    if k not in t:
        rd = [[_camb(b, m, float(mnu)) for m in WM] for b in WB]
        t[k] = dict(WB=WB.tolist(), WM=WM.tolist(), rd=rd)
        os.makedirs(os.path.dirname(_TABLA), exist_ok=True)
        json.dump(t, open(_TABLA, "w"))
    e = t[k]
    _SPL[k] = RectBivariateSpline(e["WB"], e["WM"], np.array(e["rd"]), kx=3, ky=3)
    return _SPL[k]


def rd_mpc(ob_h2, om_h2, mnu=None):
    """r_d en Mpc, de CAMB. mnu = masa de neutrinos del modelo (por defecto SSEE)."""
    if mnu is None:
        from ssee_core import SUM_MNU_EV
        mnu = SUM_MNU_EV
    if not (WB[0] <= ob_h2 <= WB[-1] and WM[0] <= om_h2 <= WM[-1]):
        raise ValueError(f"r_d fuera de la tabla CAMB: w_b={ob_h2}, w_m={om_h2} "
                         f"(rejilla w_b {WB[0]}-{WB[-1]}, w_m {WM[0]}-{WM[-1]})")
    return float(_spline(mnu)(ob_h2, om_h2)[0, 0])


def verifica():
    from ssee_core import OMEGA_B_H2, OMEGA_M_H2, SUM_MNU_EV
    rng = np.random.default_rng(20260928)          # ORIGEN-VALOR: semilla fija (la fecha)
    filas, peor = [], 0.0
    for mnu in (SUM_MNU_EV, 0.06):                  # ORIGEN-VALOR: 0.06 — la de LCDM (lcdm_planck.py)
        for _ in range(12):
            b, m = rng.uniform(WB[0], WB[-1]), rng.uniform(WM[0], WM[-1])
            c = _camb(b, m, mnu)
            e = rd_mpc(b, m, mnu) / c - 1
            peor = max(peor, abs(e))
            filas.append(dict(mnu=mnu, w_b=float(b), w_m=float(m), camb=float(c), error=float(e)))
    c_s = _camb(OMEGA_B_H2, OMEGA_M_H2, SUM_MNU_EV)
    e_s = rd_mpc(OMEGA_B_H2, OMEGA_M_H2) / c_s - 1
    vieja = 147.27 * (OMEGA_M_H2 / 0.1432) ** -0.255 * (OMEGA_B_H2 / 0.02237) ** -0.134  # ORIGEN-VALOR: 0.1432 — pivote de la formula VIEJA (147.27, 0.1432, 0.02237), solo para mostrar el cambio
    pasa = bool(peor < 1e-5 and abs(e_s) < 1e-5)
    res = dict(fecha="2026-09-28", tabla=_TABLA, puntos=filas, error_max=float(peor),
               ssee=dict(camb=float(c_s), interpolado=rd_mpc(OMEGA_B_H2, OMEGA_M_H2),
                         formula_vieja=float(vieja), error_interp=float(e_s),
                         error_formula_vieja=float(vieja / c_s - 1)),
               criterio="error < 0.001 % en 24 puntos al azar y en SSEE (declarado antes)",
               pasa=pasa)
    json.dump(res, open(_LOG_CTRL, "w"), indent=1)
    print(f"  24 puntos al azar: error max {peor * 100:.6f} %")
    print(f"  SSEE: CAMB {c_s:.4f}  interpolado {rd_mpc(OMEGA_B_H2, OMEGA_M_H2):.4f} "
          f"({e_s * 100:+.6f} %)   formula vieja {vieja:.4f} ({(vieja / c_s - 1) * 100:+.4f} %)")
    print(f"  -> {'PASA' if pasa else 'NO PASA'}   {_LOG_CTRL}")
    return pasa


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(0 if verifica() else 1)
