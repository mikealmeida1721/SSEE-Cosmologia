#!/usr/bin/env python3
"""des_y3_calibra.py — CALIBRADOR LCDM de DES Y3 3x2pt (maglim): ¿nuestro montaje
reproduce lo que DES publico?

MOTOR. CosmoSIS oficial (conda-forge, entorno en el HDD) con el ini MANTENIDO de
la libreria estandar: examples/des-y3-maglim.ini. Sus cortes de escala son
identicos a los que trae embebidos la cadena publicada, y su FITS 2pt es el
mismo archivo que bajamos (mismo sha256, ver data/manifiesto_descargas_T2.json).

QUE SE COMPARA. La cadena publica de DES (chain_3x2pt_lcdm_SR_maglim.txt) guarda
por cada muestra el chi2 de su vector de datos (DATA_VECTOR--2PT_CHI2). Se toma
su punto de MAXIMA POSTERIOR, se fijan sus 31 parametros en un values.ini y se
evalua con el sampler `test`. El chi2 que saca nuestro montaje tiene que dar el
de la cadena.

Criterio (declarado ANTES de correr): |dchi2| < 1. No se pide 0: la cadena se
corrio en 2021 con CAMB Jan15 + Halofit_Takahashi; la libreria de hoy usa pycamb
con halofit takahashi. Una diferencia de version de ese orden mueve el chi2 en
decimas; un error de montaje (cortes, nuisances, n(z)) lo mueve en decenas.

CONTROL DEL OTRO LADO (R53): el mismo montaje en un punto LEJOS del maximo
(Omega_m desplazado +0.05) debe EMPEORAR el chi2 claramente, y el chi2 que da
tiene que ser el que la cadena asigna a una muestra con ese Omega_m (se toma la
muestra de la cadena mas cercana en Omega_m a ese valor y se compara igual).

Salida: results/logs/des_y3_calibrador.json
"""
import configparser
import json
import os
import subprocess
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = "/mnt/datos/SSEE_data/des_y3"
ENT = f"{D}/entorno"
CSL = f"{ENT}/csl"
CADENA = f"{D}/cadenas/chain_3x2pt_lcdm_SR_maglim.txt"
TRABAJO = f"{D}/calibrador"
OUT = os.path.join(_R, "results", "logs", "des_y3_calibrador.json")


def lee_cadena():
    cab = open(CADENA).readline()[1:].split()
    a = np.loadtxt(CADENA)
    return cab, a


def values_fijos(cab, fila, nombre):
    """values.ini del ejemplo oficial, con TODO parametro variado de la cadena
    fijado al valor de `fila`."""
    cp = configparser.ConfigParser(strict=False, inline_comment_prefixes=(";",))
    cp.optionxform = str.lower
    for f in ("des-y3-values.ini", "des-y3-maglim-values.ini"):
        txt = "".join(l for l in open(f"{CSL}/examples/{f}") if not l.startswith("%include"))
        cp.read_string(txt)
    cp.remove_option("cosmological_parameters", "mnu")       # la cadena usa omnuh2
    fijados = {}
    for k, col in enumerate(cab):
        if "--" not in col or col.isupper() or col.startswith("COSMOLOGICAL") \
                or col.startswith("DATA_VECTOR"):
            continue
        sec, par = col.split("--")
        if not cp.has_section(sec):
            cp.add_section(sec)
        cp.set(sec, par.lower(), repr(float(fila[k])))
        fijados[col] = float(fila[k])
    ruta = f"{TRABAJO}/{nombre}_values.ini"
    with open(ruta, "w") as fh:
        cp.write(fh)
    return ruta, fijados


def evalua(values, nombre):
    """Corre CosmoSIS `test` y devuelve el chi2 del vector de datos."""
    sal = f"{TRABAJO}/{nombre}"
    env = dict(os.environ, OMP_NUM_THREADS="2",
               PATH=f"{ENT}/cosmosis/bin:" + os.environ["PATH"])
    cmd = (f"source cosmosis-configure >/dev/null 2>&1; cd {CSL}; "
           f"cosmosis examples/des-y3-maglim.ini "
           f"-p pipeline.values={values} test.save_dir={sal} "
           f"runtime.verbosity=quiet")
    r = subprocess.run(["bash", "-c", cmd], env=env, capture_output=True, text=True)
    log = r.stdout + r.stderr
    open(f"{sal}.log", "w").write(log)
    if r.returncode != 0:
        raise RuntimeError(f"CosmoSIS fallo ({nombre}); ver {sal}.log\n{log[-1500:]}")
    c = float(open(f"{sal}/data_vector/2pt_chi2.txt").read().split()[-1]) \
        if os.path.exists(f"{sal}/data_vector/2pt_chi2.txt") else None
    if c is None:                                   # otro formato: values.txt
        for l in open(f"{sal}/data_vector/values.txt"):
            if l.split("=")[0].strip() == "2pt_chi2":
                c = float(l.split("=")[1])
    return c


def main():
    os.makedirs(TRABAJO, exist_ok=True)
    cab, a = lee_cadena()
    ic = cab.index("DATA_VECTOR--2PT_CHI2")
    j = a[:, cab.index("post")].argmax()
    v, fij = values_fijos(cab, a[j], "maxpost")
    c = evalua(v, "maxpost")
    pub = float(a[j, ic])
    ok = bool(abs(c - pub) < 1.0)
    print(f"  max-post de la cadena DES: chi2 publicado = {pub:.3f}")
    print(f"  nuestro montaje            : chi2          = {c:.3f}   "
          f"dif {c - pub:+.3f}   -> {'REPRODUCE' if ok else 'NO REPRODUCE'}")

    # control: muestra de la cadena con Omega_m ~ max-post + 0.05
    om = a[:, 0]
    k = np.abs(om - (om[j] + 0.05)).argmin()
    v2, _ = values_fijos(cab, a[k], "lejos")
    c2 = evalua(v2, "lejos")
    pub2 = float(a[k, ic])
    ok2 = bool(abs(c2 - pub2) < 1.0 and c2 > c + 2)
    print(f"  CONTROL muestra lejos (Om={om[k]:.4f} vs {om[j]:.4f}): "
          f"publicado {pub2:.3f}, nuestro {c2:.3f}, dif {c2 - pub2:+.3f}   "
          f"-> {'OK' if ok2 else 'FALLA'}")
    json.dump(dict(
        fecha="2026-09-27", motor="CosmoSIS (conda-forge) + cosmosis-standard-library "
        + subprocess.run(["git", "-C", CSL, "log", "-1", "--format=%h"],
                         capture_output=True, text=True).stdout.strip(),
        ini="examples/des-y3-maglim.ini (cortes identicos a los embebidos en la cadena)",
        cadena=CADENA, criterio="|dchi2|<1 declarado antes",
        maxpost=dict(indice=int(j), chi2_publicado=pub, chi2_nuestro=c,
                     dif=c - pub, reproduce=ok, parametros=fij),
        control_lejos=dict(indice=int(k), Om=float(om[k]), chi2_publicado=pub2,
                           chi2_nuestro=c2, dif=c2 - pub2, pasa=ok2)),
        open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"  -> {OUT}")
    sys.exit(0 if ok and ok2 else 1)


if __name__ == "__main__":
    main()
