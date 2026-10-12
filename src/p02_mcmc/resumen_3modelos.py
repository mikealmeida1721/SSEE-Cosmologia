#!/usr/bin/env python3
"""resumen_3modelos.py — la comparacion SSEE / LCDM / CPL de Paper 2, en JSON.

POR QUE (2026-09-30). ssee_paper2_mcmc.py (3 modelos, prior Planck comprimido)
imprime BIC, AIC y posteriores en un log de texto; Paper 2 los cita a mano.
Este script los recalcula de las cadenas que ese MCMC guarda y los deja en
results/logs/resumen_3modelos.json, con acta, para que los papers los lean
con \\val.

COMO: las MISMAS formulas que ssee_paper2_mcmc.py (seccion 7):
  ln P_MAP = max de ln P en la cadena;  BIC = k ln N - 2 ln P_MAP;
  AIC = 2k - 2 ln P_MAP;  N = 13 puntos DESI DR2 + 3 restricciones Planck.
Posteriores: mediana y percentiles 16/84 de la cadena plana.
CONTROL (R53): BIC y AIC de los tres modelos tienen que coincidir con la tabla
impresa en results/logs/mcmc_paper2_3models_wmfix.log (a la precision impresa,
0.005), y ln P_MAP con el del log.

CORRECCION (2026-10-11, informe de la corrida de P2). El BIC y el AIC se definen
con la VEROSIMILITUD maxima, no con el posterior. SSEE y LCDM solo tienen cotas
planas (ln prior = 0 dentro), pero CPL lleva un prior gaussiano en (w0, wa)
(ssee_paper2_mcmc.py, lpost_cpl): con ln P le cobraba a CPL 0.42 de chi2 que no
son dato. Ahora BIC = k ln N - 2 ln L_max, con ln L = ln P - ln prior por muestra.
Los BIC/AIC con ln P se conservan (BIC_lnP, AIC_lnP) solo para el control contra
la tabla del log, que el MCMC imprime con ln P.
"""
import json
import os
import re
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
import ssee_core as S  # noqa: E402
from desi_dr2_data import load_desi_dr2  # noqa: E402
from procedencia import con_acta  # noqa: E402

NPZ = "/mnt/datos/SSEE_data/mcmc/paper2_3models/mcmc_chains_professional.npz"
LOG = os.path.join(_R, "results", "logs", "mcmc_paper2_3models_wmfix.log")
N_PLANCK = 3   # ORIGEN-VALOR: 3 — restricciones del prior Planck comprimido (H0, Omega_m, omega_b), ssee_paper2_mcmc.py L322
PLANCK_H0 = (67.36, 0.54)   # ORIGEN-VALOR: 67.36 +- 0.54 — Planck 2018 VI Tabla 2, el prior comprimido de ssee_paper2_mcmc.py
N = len(load_desi_dr2()["z"]) + N_PLANCK
NOMBRES = {"ssee": ["H0", "obh2"], "lcdm": ["H0", "Om", "obh2"],
           "cpl": ["H0", "Om", "w0", "wa", "obh2"]}
ETIQ = {"ssee": "SSEE", "lcdm": "ΛCDM", "cpl": "CPL"}


def ln_prior(m, flat):
    """ln prior no plano de cada modelo, el MISMO de ssee_paper2_mcmc.py (lpost_*)."""
    if m == "cpl":   # ORIGEN-VALOR: 0.5 y 1.0 — anchos del prior gaussiano de lpost_cpl en ssee_paper2_mcmc.py
        return -0.5 * ((flat[:, 2] + 1.0) / 0.5) ** 2 - 0.5 * (flat[:, 3] / 1.0) ** 2
    return np.zeros(len(flat))

d = np.load(NPZ)
res = {}
for m, nom in NOMBRES.items():
    flat, lp = d[f"{m}_flat"], d[f"{m}_lp"]
    k = flat.shape[1]
    lpm = float(lp.max())
    lL = lp - ln_prior(m, flat)
    lLm = float(lL[np.isfinite(lL)].max())
    p16, p50, p84 = np.percentile(flat, [16, 50, 84], axis=0)
    res[m] = dict(k=k, lnP_MAP=lpm, lnL_max=lLm, BIC=k * np.log(N) - 2 * lLm, AIC=2 * k - 2 * lLm,
                  BIC_lnP=k * np.log(N) - 2 * lpm, AIC_lnP=2 * k - 2 * lpm,
                  posterior={n: dict(mediana=float(b), mas=float(c - b), menos=float(b - a),
                                     std=float(s))
                             for n, a, b, c, s in zip(nom, p16, p50, p84, flat.std(axis=0))})
for m in res:
    res[m]["dBIC_vs_ssee"] = res[m]["BIC"] - res["ssee"]["BIC"]
    res[m]["dAIC_vs_ssee"] = res[m]["AIC"] - res["ssee"]["AIC"]
    # con el signo de Paper 2: Delta = SSEE - modelo (negativo favorece a SSEE)
    res[m]["dBIC_ssee_menos"] = res["ssee"]["BIC"] - res[m]["BIC"]
    res[m]["dAIC_ssee_menos"] = res["ssee"]["AIC"] - res[m]["AIC"]
# Ω_m de SSEE no se muestrea: es ω_m algebraico / h² en cada muestra (P2 tab:posteriors
# imprimía el valor del ancla, 0.308881, como si fuera el posterior; 2026-10-11)
_om = S.OMEGA_M_H2 / (d["ssee_flat"][:, 0] / 100.0) ** 2
_a, _b, _c = np.percentile(_om, [16, 50, 84])
res["ssee"]["posterior"]["Om_derivado"] = dict(mediana=float(_b), mas=float(_c - _b), menos=float(_b - _a),
                                               std=float(_om.std()))
rho_cpl = float(np.corrcoef(d["cpl_flat"][:, 2], d["cpl_flat"][:, 3])[0, 1])
# distancia del punto algebraico de SSEE a la mediana CPL, por eje, en sigmas
pc = res["cpl"]["posterior"]
dist_ssee_cpl = dict(w0=abs(S.W0 - pc["w0"]["mediana"]) / pc["w0"]["std"],
                     wa=abs(S.WA - pc["wa"]["mediana"]) / pc["wa"]["std"])
h = res["ssee"]["posterior"]["H0"]
tension_H0 = abs(h["mediana"] - PLANCK_H0[0]) / np.hypot(h["std"], PLANCK_H0[1])

# CONTROL: la tabla impresa por el MCMC
txt = open(LOG).read()
impreso = {}
for m, e in ETIQ.items():
    f = re.search(rf"{e}\s+(\d)\s+(-?[0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+(\d+)", txt)
    impreso[m] = dict(lnP_MAP=float(f.group(2)), BIC=float(f.group(3)), AIC=float(f.group(5)))
    # N_eff: lo calcula el MCMC con el tiempo de autocorrelacion de emcee; se toma de su log
    res[m]["N_eff_del_log"] = int(f.group(7))
# diagnosticos de convergencia (tabla de P2), tal como los imprime el MCMC al cerrar cada modelo:
# «[SSEE]  τ_max=31.9  N_eff≈78380  accept=0.714». Antes la tabla llevaba los de una corrida vieja
# tecleados a mano (cuarta lectura, 2026-10-10).
for m, e in {"ssee": "SSEE", "lcdm": "ΛCDM", "cpl": "CPL"}.items():
    g = re.search(rf"\[{e}\]\s+τ_max=([0-9.]+)\s+N_eff≈(\d+)\s+accept=([0-9.]+)", txt)
    res[m]["tau_max"], res[m]["aceptacion"] = float(g.group(1)), float(g.group(3))
    res[m]["Ns_sobre_tau"] = 25000 / float(g.group(1))
pasa = all(abs(res[m][q] - impreso[m][c]) <= 0.005 + 1e-9 for m in res
           for q, c in (("lnP_MAP", "lnP_MAP"), ("BIC_lnP", "BIC"), ("AIC_lnP", "AIC")))
out = dict(fecha=str(__import__("datetime").date.today()), N=N, modelos=res,
           tension_H0_ssee_planck=float(tension_H0), rho_w0_wa_cpl=rho_cpl,
           dist_ssee_a_mediana_cpl_sigma=dist_ssee_cpl,
           control=dict(log=os.path.relpath(LOG, _R), impreso=impreso, pasa=bool(pasa)))
json.dump(con_acta(out, __file__, entradas=[NPZ, LOG]),
          open(os.path.join(_R, "results", "logs", "resumen_3modelos.json"), "w"), indent=1)
for m, r in res.items():
    print(f"  {m:5s} k {r['k']}  lnP_MAP {r['lnP_MAP']:.3f}  BIC {r['BIC']:.3f} ({r['dBIC_vs_ssee']:+.3f})"
          f"  AIC {r['AIC']:.3f} ({r['dAIC_vs_ssee']:+.3f})")
print(f"  H0 SSEE {h['mediana']:.3f} +- {h['std']:.3f}  tension Planck {tension_H0:.2f} sigma")
print(f"  control contra la tabla del log: {'PASA' if pasa else 'NO PASA'}")
