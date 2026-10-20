#!/usr/bin/env python3
"""analiza_boss_R1R2.py — de las cadenas R1/R2 de BOSS al resumen que leen los perfiles y P6.

POR QUE (2026-10-01). results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json no
tenia acta y ningun script del repo lo escribia: el que lo hizo el 2026-09-08 no
se guardo. Ademas su bloque SSEE salio de cadenas corridas con el m_nu de LCDM
(0.06 en vez de 0.06849). Las cadenas SSEE se rehicieron el 2026-10-01; este
script hace el resumen y lo deja reproducible. El viejo se conserva como
archive/logs_superados/R1R2_boss_lpt_cobaya_20260908_mnu006.json.

QUE CALCULA, por modelo, tras quitar el burn-in (_QUEMA de multisonda, 0.3):
  logA, logA_sig      media y desviacion pesadas
  chi2_marg_min       minimo de la columna chi2 (sesgos lineales integrados)
  chi2_real_min       en ese punto, sum_conjuntos [chi2_marg - ln det F]
  fs8 por z           f * sigma8_ref * sqrt(e^logA 1e-10 / A_ref) (plantilla de cobaya_boss)
y entre modelos (lo que cita Paper 6, sin teclear nada):
  dchi2_real          SSEE - LCDM, misma libertad (Delta k = 0)
  vs_publicado        distancia de cada fs8 al consenso BOSS DR12 de Alam+2017,
                      leido de data/raw/fsigma8_rsd.csv, en cuadratura
  perfil_vs_marginal  el minimo del PERFIL de logA (R1R2_boss_lpt_kmax0.200.json,
                      bloque SSEE, con el m_nu de SSEE y los mismos bines z1+z3)
                      contra la media marginal de las cadenas, en sigmas de la
                      marginal. (Hasta el 2026-10-17 se leia de
                      boss_aisla_neutrinos.json, A_canonico: el mismo perfil, que
                      queda con los tres bines como medicion historica.)
BINES (2026-10-17). Desde ese dia solo z1 y z3 (ver BINES DE z en
boss_lpt_R1R2.py): los tres bines publicos se solapan y se contaban dos veces.
El resumen de tres bines queda en
archive/logs_superados/R1R2_boss_lpt_cobaya_20261015_3bines_solapados.json.

CONTROL (R53), por modelo, contra ese resumen de tres bines:
  (1) cableado: el chi2 re-evaluado en el mejor punto = la columna de la cadena
      a 1e-4;
  (2) quitar dato no puede afinar: sigma(logA) con z1+z3 >= la de tres bines;
  (3) z1+z3 es un subconjunto del mismo dato: logA no se mueve mas de 1 sigma
      (la de tres bines).
(El control anterior comparaba LCDM con el resumen del 2026-09-08; dejo de
aplicar al cambiar el dato.)

Uso: analiza_boss_R1R2.py [lcdm|ssee|ambos]   (lcdm solo = prueba del control)
Salida: results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json
"""
import json
import os
import re
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)
QUE = sys.argv[1] if len(sys.argv) > 1 else "ambos"
sys.argv = sys.argv[:1]
import cobaya_boss as CB  # noqa: E402

CAD = "/mnt/datos/SSEE_data/chains_p6/boss"
LOGS = os.path.join(_R, "results", "logs", "growth_2026-07")
RSD = os.path.join(_R, "data", "raw", "fsigma8_rsd.csv")
PERFIL = os.path.join(LOGS, "R1R2_boss_lpt_kmax0.200.json")   # perfil de logA (boss_lpt_kmax020), mismos bines
VIEJO = os.path.join(_R, "archive", "logs_superados", "R1R2_boss_lpt_cobaya_20261015_3bines_solapados.json")
QUEMA = float(re.search(r"^_QUEMA\s*=\s*([0-9.]+)", open(os.path.join(_R, "src", "p06_growth", "multisonda_fondo_clavado.py")).read(), re.M).group(1))
PL = CB.plantilla_fsigma8()


def lee(nombre):
    cads = []
    for i in (1, 2, 3, 4):
        f = f"{CAD}/{nombre}.{i}.txt"
        cab = open(f).readline().lstrip("#").split()
        x = np.loadtxt(f)
        cads.append(x[int(QUEMA * len(x)):])
    return cab, np.vstack(cads), [f"{CAD}/{nombre}.{i}.txt" for i in (1, 2, 3, 4)]


def resumen(nombre):
    M = nombre.upper()
    cab, S, fs = lee(nombre)
    w, logA = S[:, cab.index("weight")], S[:, cab.index("logA")]
    chi = S[:, cab.index("chi2")]
    m = float(np.average(logA, weights=w))
    s = float(np.sqrt(np.average((logA - m) ** 2, weights=w)))
    i = int(np.argmin(chi))
    v = [S[i, cab.index(n)] for n in CB.NOMBRES]
    real, marg = 0.0, 0.0
    for j, st in enumerate(CB.SETS):
        cm, _ = CB.R.chi2_marg_set(st, M, v[0], v[1 + 3 * j: 4 + 3 * j])
        T = CB.R.templates(st, M, v[0])
        F = T.T @ st["Cinv"] @ T + CB.R._LAMBDA
        real += cm - np.linalg.slogdet(F)[1]
        marg += cm
    fs8 = {}
    for p in PL[M]:
        if p["cap"] != "NGC":
            continue
        y = p["f"] * p["s8_ref"] * np.sqrt(np.exp(logA) * 1e-10 / PL["A_ref"])
        my = float(np.average(y, weights=w))
        fs8[p["zb"]] = [float(p["z"]), my, float(np.sqrt(np.average((y - my) ** 2, weights=w)))]
    print(f"  {M}: logA {m:.5f} +- {s:.5f}  chi2_marg_min {chi[i]:.6f} (re-evaluado {marg:.6f})  chi2_real_min {real:.4f}  n {len(S)}")
    return dict(logA=m, logA_sig=s, chi2_marg_min=float(chi[i]), chi2_marg_reevaluado=float(marg),
                chi2_real_min=float(real), n=int(len(S)), fs8=fs8), fs


modelos = ["lcdm", "ssee"] if QUE == "ambos" else [QUE]
out, entradas = {}, [VIEJO]
for nm in modelos:
    out[nm], fs = resumen(nm)
    entradas += fs
V = json.load(open(VIEJO))
assert tuple(st["zb"] for st in CB.SETS[::2]) == ("z1", "z3"), "BOSS no corre con z1+z3"
out["control"] = {}
for nm in modelos:
    n, v = out[nm], V[nm]
    cab = abs(n["chi2_marg_min"] - n["chi2_marg_reevaluado"])
    d_logA = abs(n["logA"] - v["logA"]) / v["logA_sig"]
    pasa = bool(cab < 1e-4 and n["logA_sig"] >= v["logA_sig"] and d_logA < 1.0)
    out["control"][nm] = dict(criterio="chi2 re-evaluado = cadena a 1e-4; sigma(logA) z1+z3 >= la de 3 bines; |dlogA| < 1 sigma de 3 bines",
                              dif_cableado=float(cab), logA_sig_3bines=v["logA_sig"], logA_3bines=v["logA"],
                              d_logA_sigma=float(d_logA), pasa=pasa)
    print(f"  control {nm.upper()}: cableado {cab:.1e}, sigma {n['logA_sig']:.4f} >= {v['logA_sig']:.4f}, dlogA {d_logA:.2f} sigma -> {'PASA' if pasa else 'NO PASA'}")
    if not pasa:
        sys.exit(f"control {nm} no pasa: no se escribe")
if QUE == "ambos":
    pub = {}
    for ln in open(RSD):
        c = ln.strip().split(",")
        if ln.startswith("#") or len(c) < 4 or c[3] != "BOSS_DR12":
            continue
        pub[round(float(c[0]), 2)] = (float(c[1]), float(c[2]))
    vp = {}
    for m in ("ssee", "lcdm"):
        vp[m] = {}
        for zb, (z, f, sf) in out[m]["fs8"].items():
            pf, ps = pub[round(z, 2)]
            vp[m][zb] = dict(z=z, publicado=pf, publicado_sigma=ps, sigma=float(abs(pf - f) / np.hypot(ps, sf)))
    out["vs_publicado"] = dict(fuente="Alam et al. 2017 (data/raw/fsigma8_rsd.csv)", modelos=vp)
    out["dchi2_real"] = out["ssee"]["chi2_real_min"] - out["lcdm"]["chi2_real_min"]
    out["datos"] = dict(bines=[st["zb"] for st in CB.SETS[::2]], conjuntos=CB.NSET, npts=CB.NPTS,
                        n_libres=CB.NFREE, n_muestreados=CB.NMUESTRA, n_marginalizados=CB.NMARG,
                        dof=CB.NPTS - CB.NFREE)
    ac = dict(json.load(open(PERFIL))["SSEE"])
    assert ac["npts"] == CB.NPTS, "el perfil no usa los mismos bines que las cadenas"
    ac["mnu"] = CB.R.COSMO["SSEE"]["mnu"]   # el perfil lo corre boss_lpt_R1R2 con este COSMO
    out["perfil_vs_marginal"] = dict(perfil_logA=ac["logA"], perfil_sigma=ac["sig_logA"], perfil_chi2=ac["chi2"],
                                     mnu_perfil=ac["mnu"], marginal_logA=out["ssee"]["logA"], marginal_sigma=out["ssee"]["logA_sig"],
                                     sigmas=float((ac["logA"] - out["ssee"]["logA"]) / out["ssee"]["logA_sig"]))
    assert abs(ac["mnu"] - CB.R.S.SUM_MNU_EV) < 1e-9, "el perfil no lleva el m_nu de SSEE"
    entradas += [RSD, PERFIL]
    print(f"  dchi2_real SSEE-LCDM {out['dchi2_real']:+.3f}; perfil-marginal {out['perfil_vs_marginal']['sigmas']:.2f} sigma")
    json.dump(con_acta(out, __file__, entradas=entradas), open(os.path.join(LOGS, "R1R2_boss_lpt_cobaya.json"), "w"), indent=1)
    print("  escrito -> results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json")
