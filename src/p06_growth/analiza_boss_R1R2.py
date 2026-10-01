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
  perfil_vs_marginal  el minimo del PERFIL de logA (boss_aisla_neutrinos.json,
                      A_canonico, ya con el m_nu de SSEE) contra la media
                      marginal de las cadenas, en sigmas de la marginal
CONTROL (R53): las cadenas LCDM NO se rehicieron; su resumen tiene que coincidir
con el del 2026-09-08 dentro de TOL_SIGMA en logA y fs8. El script original no
se guardo y el burn-in exacto no se conoce: cambiarlo entre 0.2 y 0.5 mueve logA
unas 0.01 sigma (medido el 2026-10-01), de ahi la tolerancia.

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
AISLA = os.path.join(LOGS, "boss_aisla_neutrinos.json")
VIEJO = os.path.join.join(_R, "archive", "logs_superados", "R1R2_boss_lpt_cobaya_20260908_mnu006.json")
QUEMA = float(re.search(r"^_QUEMA\s*=\s*([0-9.]+)", open(os.path.join(_R, "src", "p06_growth", "multisonda_fondo_clavado.py")).read(), re.M).group(1))
TOL_SIGMA = 0.05   # ORIGEN-VALOR: 0.05 — cinco veces lo que mueve el burn-in (0.01 sigma, medido)
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
        T = CB.R.templates(st, M) * np.exp(v[0])
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
v = json.load(open(VIEJO))["lcdm"]
if "lcdm" in out:
    n = out["lcdm"]
    d_logA = abs(n["logA"] - v["logA"]) / v["logA_sig"]
    d_fs8 = max(abs(n["fs8"][z][1] - v["fs8"][z][1]) / v["fs8"][z][2] for z in v["fs8"])
    pasa = bool(d_logA < TOL_SIGMA and d_fs8 < TOL_SIGMA and abs(n["chi2_marg_min"] - v["chi2_marg_min"]) < 1e-4)
    out["control_lcdm"] = dict(criterio=f"LCDM (cadenas sin rehacer) = resumen del 2026-09-08 dentro de {TOL_SIGMA} sigma; chi2_marg_min a 1e-4",
                               d_logA_sigma=float(d_logA), d_fs8_sigma_max=float(d_fs8), pasa=pasa)
    print(f"  control LCDM: logA {d_logA:.4f} sigma, fs8 {d_fs8:.4f} sigma, chi2 {n['chi2_marg_min']:.6f} vs {v['chi2_marg_min']:.6f} -> {'PASA' if pasa else 'NO PASA'}")
    if not pasa:
        sys.exit("control LCDM no pasa: no se escribe")
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
    ac = json.load(open(AISLA))["A_canonico"]
    out["perfil_vs_marginal"] = dict(perfil_logA=ac["logA"], perfil_sigma=ac["sig_logA"], perfil_chi2=ac["chi2"],
                                     mnu_perfil=ac["mnu"], marginal_logA=out["ssee"]["logA"], marginal_sigma=out["ssee"]["logA_sig"],
                                     sigmas=float((ac["logA"] - out["ssee"]["logA"]) / out["ssee"]["logA_sig"]))
    assert abs(ac["mnu"] - CB.R.S.SUM_MNU_EV) < 1e-9, "el perfil no lleva el m_nu de SSEE"
    entradas += [RSD, AISLA]
    print(f"  dchi2_real SSEE-LCDM {out['dchi2_real']:+.3f}; perfil-marginal {out['perfil_vs_marginal']['sigmas']:.2f} sigma")
    json.dump(con_acta(out, __file__, entradas=entradas), open(os.path.join(LOGS, "R1R2_boss_lpt_cobaya.json"), "w"), indent=1)
    print("  escrito -> results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json")
