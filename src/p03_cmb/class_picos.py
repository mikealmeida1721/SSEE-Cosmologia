#!/usr/bin/env python3
"""class_picos.py — el cruce con CLASS de la seccion CMB de Unified, con log.

POR QUE (2026-09-30). La seccion «CLASS Boltzmann Validation» de Unified cita
picos acusticos, residuos RMS y el factor de degradacion escritos a mano, de
corridas de mayo con .ini tecleados (w0 = -0.8399, Omega_cdm de la epoca MIRA).
Este script rehace las tres corridas desde el nucleo y lcdm_planck.py.

MODELOS (CLASS v3.3.4 via classy, l_max 2500, lensing):
  lcdm   Planck 2018 (lcdm_planck.py), A_s y tau de Planck.
  ssee   omega_b, omega_c, Sigma m_nu, n_s, w0, w_a del nucleo; H0_GLOBAL;
         A_s del CMB del modelo (CANONICAL logA_cmb_ssee); tau de Planck.
  naive  igual que ssee pero con s_m = 1+w0 como Omega_m en la geometria:
         omega_c = s_m h^2 - omega_b - omega_nu (el contraejemplo).
Picos: la misma receta que ssee_paper3_cmb.py (argrelmax, orden 60, l 50-1500).
RMS: sqrt(<(C_l/C_l^LCDM - 1)^2>) en l = 30-2500, TT lensado.
CONTROL (R53): los picos de SSEE por CLASS contra los de CAMB
(paper3_cmb_chi2.json#picos_TT.ssee): dos codigos, mismo fondo; tienen que
coincidir a Delta l <= 2.

Salida: results/logs/class_picos.json
"""
import json
import math
import os
import sys

import numpy as np
import yaml
from scipy.signal import argrelmax

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from classy import Class  # noqa: E402
import ssee_core as S  # noqa: E402
from lcdm_planck import AS_PLANCK, LCDM_PLANCK as LP, TAU_PLANCK  # noqa: E402
from procedencia import con_acta  # noqa: E402

C = yaml.safe_load(open(os.path.join(_R, "CANONICAL_VALUES.yaml")))["canonical"]
LMAX = 2500
T_CMB = 2.7255   # ORIGEN-VALOR: 2.7255 — T_cmb en K, el valor por defecto de CLASS (Fixsen 2009)
COMUN = dict(output="tCl,pCl,lCl", lensing="yes", l_max_scalars=LMAX, tau_reio=TAU_PLANCK,
             N_ur=2.0328, N_ncdm=1, T_ncdm=0.71611)   # ORIGEN-VALOR: 2.0328, 0.71611 — CLASS, 1 neutrino masivo y N_eff 3.044 (explanatory.ini)


def ssee(omch2):
    return dict(COMUN, h=S.H0_GLOBAL / 100, omega_b=S.OMEGA_B_H2, omega_cdm=omch2,
                m_ncdm=S.SUM_MNU_EV, n_s=S.N_S, A_s=math.exp(C["logA_cmb_ssee"]) * 1e-10,
                Omega_Lambda=0, w0_fld=S.W0, wa_fld=S.WA, use_ppf="yes")


h = S.H0_GLOBAL / 100
MODELOS = {
    "lcdm": dict(COMUN, h=LP["H0"] / 100, omega_b=LP["ombh2"], omega_cdm=LP["omch2"],
                 m_ncdm=LP["mnu"], n_s=LP["ns"], A_s=AS_PLANCK),
    "ssee": ssee(S.OMEGA_C_H2),
    "naive": ssee(S.S_M * h ** 2 - S.OMEGA_B_H2 - S.OMEGA_NU_H2),
}

tt, res = {}, {}
for n, p in MODELOS.items():
    c = Class()
    c.set(p)
    c.compute()
    cl = c.lensed_cl(LMAX)
    ell = cl["ell"]
    dl = ell * (ell + 1) * cl["tt"]
    tt[n] = dl
    i = argrelmax(dl[50:1500], order=60)[0] + 50
    res[n] = dict(picos=[int(ell[j]) for j in i[:3]], omega_cdm=float(p["omega_cdm"]))
    c.struct_cleanup()
    c.empty()
sel = slice(30, LMAX + 1)
for n in ("ssee", "naive"):
    r = tt[n][sel] / tt["lcdm"][sel] - 1
    res[n]["rms_vs_lcdm"] = float(np.sqrt(np.mean(r ** 2)))
res["degradacion_rms_naive_sobre_ssee"] = res["naive"]["rms_vs_lcdm"] / res["ssee"]["rms_vs_lcdm"]

# CONTROL de la receta (2026-10-01): el caso naive de mayo, con su .ini tal cual
# (class_ssee/ssee_v36_nomira.ini), por la MISMA receta de RMS. Si da su 31.5 %
# la diferencia esta en las entradas; si no, en la receta.
INI_VIEJO = os.path.join(_R, "class_ssee", "ssee_v36_nomira.ini")
pv = {}
for ln in open(INI_VIEJO):
    ln = ln.split("#")[0].strip()
    if "=" in ln:
        k, v = (x.strip() for x in ln.split("=", 1))
        if k not in ("root", "overwrite_root", "output", "P_k_max_h/Mpc"):
            pv[k] = v
if "N_eff" in pv:   # CLASS 3.3 ya no lee N_eff; sin neutrinos masivos en ese .ini, N_eff = N_ur
    pv["N_ur"] = pv.pop("N_eff")
pv.update(output="tCl,pCl,lCl", lensing="yes", l_max_scalars=LMAX)
c = Class()
c.set(pv)
c.compute()
cl = c.lensed_cl(LMAX)
dl_v = cl["ell"] * (cl["ell"] + 1) * cl["tt"]
iv = argrelmax(dl_v[50:1500], order=60)[0] + 50
res["naive_ini_mayo"] = dict(picos=[int(cl["ell"][j]) for j in iv[:3]],
                              rms_vs_lcdm=float(np.sqrt(np.mean((dl_v[30:LMAX + 1] / tt["lcdm"][30:LMAX + 1] - 1) ** 2))),
                              rms_publicado_pct=31.5)   # ORIGEN-VALOR: 31.5 — el RMS que cita Unified de esa corrida de mayo (sin log)
c.struct_cleanup()
c.empty()
camb = json.load(open(os.path.join(_R, "results", "logs", "paper3_cmb_chi2.json")))["picos_TT"]["ssee"]
pasa = all(abs(a - b) <= 2 for a, b in zip(res["ssee"]["picos"], camb))
out = dict(fecha=str(__import__("datetime").date.today()), modelos=res,
           control=dict(picos_ssee_camb=camb, picos_ssee_class=res["ssee"]["picos"], pasa=bool(pasa)))
json.dump(con_acta(out, __file__, entradas=[os.path.join(_R, "CANONICAL_VALUES.yaml"), INI_VIEJO,
                                             os.path.join(_R, "results", "logs", "paper3_cmb_chi2.json")]),
          open(os.path.join(_R, "results", "logs", "class_picos.json"), "w"), indent=1)
# Figura de Unified (fig:cmb_tt): D_l TT lensado de los tres modelos, desde ESTA corrida.
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
ell_p = np.arange(LMAX + 1)
fig, ax = plt.subplots(figsize=(8, 4.5))
ESTILO = {"naive": ("0.55", "-", "SSEE with $s_m$ as matter (naive)"),
          "ssee": ("tab:red", "-", r"SSEE (total $\Omega_m$)"),
          "lcdm": ("tab:blue", "--", r"$\Lambda$CDM (Planck 2018)")}   # LCDM al final: encima de SSEE
for n, (col, ls, lab) in ESTILO.items():
    ax.plot(ell_p[2:], 1e12 * T_CMB ** 2 * tt[n][2:] / (2 * np.pi), color=col, ls=ls, lw=1.2, label=lab)
ax.set_xlim(2, LMAX)
ax.set_xlabel(r"$\ell$")
ax.set_ylabel(r"$D_\ell^{TT}$ [$\mu$K$^2$]")
ax.legend(frameon=False)
fig.tight_layout()
FIG = os.path.join(_R, "results", "figures", "fig_class_tt.pdf")
fig.savefig(FIG)
for n in MODELOS:
    print(f"  {n:5s} picos {res[n]['picos']}  " + (f"RMS {100 * res[n]['rms_vs_lcdm']:.2f}%" if n != "lcdm" else ""))
print(f"  naive .ini de mayo: picos {res['naive_ini_mayo']['picos']}  RMS {100 * res['naive_ini_mayo']['rms_vs_lcdm']:.2f}% (publicado 31.5%)")
print(f"  degradacion {res['degradacion_rms_naive_sobre_ssee']:.1f}x   control CLASS vs CAMB: {'PASA' if pasa else 'NO PASA'}")
