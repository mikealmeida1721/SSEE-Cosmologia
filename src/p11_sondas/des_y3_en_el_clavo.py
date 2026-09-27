#!/usr/bin/env python3
"""des_y3_en_el_clavo.py — DES Y3 3x2pt (maglim) contra el fondo clavado de SSEE.

Requiere que des_y3_calibra.py haya pasado (el montaje reproduce la cadena
publica de DES: results/logs/des_y3_calibrador.json).

CERO LIBRES COSMOLOGICOS. El fondo sale del nucleo (h, omega_b h^2, omega_c h^2,
n_s, w0, wa, Sum m_nu) y A_s es el CLAVO del CMB (se cobra una sola vez, alli).
Se minimizan SOLO los nuisances de DES (shear m, photo-z de fuentes y lentes,
sesgo de lentes, alineamientos intrinsecos TATT), con los MISMOS priors
gaussianos y rangos que usa DES (examples/des-y3-maglim-*.ini), partiendo del
maximo de la cadena publica. max_posterior=T: se minimiza chi2 + penalizacion de
prior, como en el ajuste de DES; se reportan las dos piezas por separado.

w0-wa: CAMB con PPF (use_ppf_w=T). El fluido de CAMB no admite cruzar w=-1, y el
CPL de SSEE lo cruza en z~0.31. Es la misma eleccion que sn_geometria.py.

CONTROL DEL OTRO LADO (R53): LCDM con los parametros de Planck 2018, tratado
IGUAL (cosmologia fija, nuisances minimizados). Y como referencia, LCDM con
cosmologia LIBRE = el maximo de la cadena de DES (del calibrador).

DES Y3 entra SOLO como sonda individual contra el clavo: solapa cielo con
KiDS-Legacy y no hay covarianza cruzada publica.

Uso: des_y3_en_el_clavo.py {ssee|lcdm_planck}
Salida: results/logs/des_y3_en_el_clavo_<caso>.json
"""
import configparser
import json
import math
import os
import subprocess
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from des_y3_calibra import CSL, ENT, TRABAJO, lee_cadena  # noqa: E402

CAL = os.path.join(_R, "results", "logs", "des_y3_calibrador.json")


def cosmologia(caso):
    if caso == "ssee":
        from ssee_core import (H0_GLOBAL, N_S, OMEGA_B_H2, OMEGA_C_H2,
                               SUM_MNU_EV, W0, WA)
        # ORIGEN: results/logs/cmb_dbic_tau_ajustado.json -> SSEE/mejor (el clavo del CMB)
        with open(os.path.join(_R, "results", "logs", "cmb_dbic_tau_ajustado.json")) as fh:
            loga = json.load(fh)["SSEE"]["mejor"]["logA"]
        return dict(h0=H0_GLOBAL / 100, ombh2=OMEGA_B_H2, omch2=OMEGA_C_H2,
                    n_s=N_S, a_s=math.exp(loga) * 1e-10, mnu=SUM_MNU_EV,
                    w=W0, wa=WA)
    # ORIGEN: Planck 2018 VI (arXiv:1807.06209), Tabla 2, TT,TE,EE+lowE+lensing
    return dict(h0=67.36 / 100, ombh2=0.02237, omch2=0.1200, n_s=0.9649,
                a_s=math.exp(3.044) * 1e-10, mnu=0.06, w=-1.0, wa=0.0)  # Planck 2018


def values_nuisance(caso, cab, fila):
    cp = configparser.ConfigParser(strict=False, inline_comment_prefixes=(";",))
    cp.optionxform = str.lower
    for f in ("des-y3-values.ini", "des-y3-maglim-values.ini"):
        txt = "".join(l for l in open(f"{CSL}/examples/{f}") if not l.startswith("%include"))
        cp.read_string(txt)
    sec = "cosmological_parameters"
    for p in ("omega_m", "omega_b", "mnu", "a_s", "h0", "n_s"):
        cp.remove_option(sec, p)
    for p, v in cosmologia(caso).items():
        cp.set(sec, p, repr(float(v)))
    # nuisances: rango oficial, punto de partida = maximo de la cadena
    for k, col in enumerate(cab):
        if "--" not in col or col.startswith("cosmological") or col.isupper():
            continue
        s, p = col.split("--")
        lo_ini_hi = cp.get(s, p).split()
        if len(lo_ini_hi) == 3:
            cp.set(s, p, f"{lo_ini_hi[0]} {float(fila[k])!r} {lo_ini_hi[2]}")
    ruta = f"{TRABAJO}/clavo_{caso}_values.ini"
    with open(ruta, "w") as fh:
        cp.write(fh)
    return ruta


def cosmosis(args, nombre):
    env = dict(os.environ, OMP_NUM_THREADS="2",
               PATH=f"{ENT}/cosmosis/bin:" + os.environ["PATH"])
    cmd = (f"source cosmosis-configure >/dev/null 2>&1; cd {CSL}; "
           f"cosmosis examples/des-y3-maglim.ini -p {args} camb.use_ppf_w=T "
           f"runtime.verbosity=standard")
    r = subprocess.run(["bash", "-c", cmd], env=env, capture_output=True, text=True)
    open(f"{TRABAJO}/{nombre}.log", "w").write(r.stdout + r.stderr)
    if r.returncode != 0:
        raise RuntimeError(f"CosmoSIS fallo ({nombre}); ver {TRABAJO}/{nombre}.log\n"
                           + (r.stdout + r.stderr)[-1500:])


def lee_bloque(dirsal, seccion, clave):
    for l in open(f"{dirsal}/{seccion}/values.txt"):
        if l.split("=")[0].strip() == clave:
            return float(l.split("=")[1])
    raise KeyError(clave)


def main():
    caso = sys.argv[1]
    if not json.load(open(CAL))["maxpost"]["reproduce"]:
        sys.exit("el calibrador NO reproduce la cadena de DES: no se evalua nada")
    os.makedirs(TRABAJO, exist_ok=True)
    cab, a = lee_cadena()
    j = a[:, cab.index("post")].argmax()
    v = values_nuisance(caso, cab, a[j])
    mejor = f"{TRABAJO}/clavo_{caso}_mejor.ini"
    # 1) minimizar nuisances (cosmologia fija)
    cosmosis(f"pipeline.values={v} runtime.sampler=maxlike maxlike.method=Nelder-Mead "
             f"maxlike.maxiter=6000 maxlike.tolerance=1e-4 maxlike.max_posterior=T "
             f"maxlike.output_ini={mejor} pipeline.fast_slow=T "
             f"pipeline.first_fast_module=fits_nz "
             f"output.filename={TRABAJO}/clavo_{caso}_maxlike.txt", f"clavo_{caso}_min")
    # 2) evaluar en el mejor punto: chi2 de datos y prior por separado
    sal = f"{TRABAJO}/clavo_{caso}_test"
    cosmosis(f"pipeline.values={mejor} runtime.sampler=test test.save_dir={sal}",
             f"clavo_{caso}_test")
    chi2 = lee_bloque(sal, "data_vector", "2pt_chi2")
    s8 = lee_bloque(sal, "cosmological_parameters", "sigma_8")
    om = lee_bloque(sal, "cosmological_parameters", "omega_m")
    cal = json.load(open(CAL))["maxpost"]
    print(f"  {caso}: chi2_2pt = {chi2:.3f}   (LCDM libre, max de la cadena DES: "
          f"{cal['chi2_nuestro']:.3f})   diferencia {chi2 - cal['chi2_nuestro']:+.3f}")
    print(f"        Omega_m = {om:.4f}   S8 = {s8 * (om / 0.3) ** 0.5:.4f}")
    json.dump(dict(fecha="2026-09-27", caso=caso, cosmologia=cosmologia(caso),
                   chi2_2pt=chi2, Omega_m=om, sigma_8=s8,
                   S8=s8 * (om / 0.3) ** 0.5,
                   lcdm_libre_chi2=cal["chi2_nuestro"],
                   diferencia_vs_lcdm_libre=chi2 - cal["chi2_nuestro"],
                   mejor_ini=mejor, libres_cosmologicos=0,
                   nota="nuisances minimizados con sus priors DES (max_posterior=T); "
                        "el chi2 reportado es el del vector de datos"),
              open(os.path.join(_R, "results", "logs", f"des_y3_en_el_clavo_{caso}.json"), "w"),
              indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
