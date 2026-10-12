#!/usr/bin/env python3
"""ssee_fijo_k0.py — SSEE con NADA libre frente a DESI DR2 + Planck comprimido (Paper 2).

POR QUE (2026-10-11, pregunta de Mike: «¿por qué irían libres H y ω_b en SSEE
cuando son fijos?»). El MCMC de 3 modelos muestrea H0 y ω_b en SSEE y le cobra
k = 2. Pero en el modelo ω_b = (π−φ)/(3Ω²) es algebraico y H = H_SH0ES(1−f_screen)
sale de la cascada; sus dos libres, {A_s, τ}, no entran en BAO ni en el prior
comprimido. En esta prueba SSEE tiene k = 0: se evalúa en su punto, sin ajustar.

QUE SE MIDE. χ² de cada sonda (BAO DR2 con covarianza completa; prior Planck 3D)
en el punto algebraico; BIC con k = 0 frente a los BIC de ΛCDM y CPL de
resumen_3modelos.json (ln L, sin el prior de CPL); lo que cuesta fijar frente a
la versión con H0 y ω_b libres. Y el desglose por sonda de los tres modelos en
su máximo de verosimilitud, para el informe.

CONTROL (R53). Las mismas funciones evaluadas en el máximo de ln L de cada cadena
tienen que devolver el ln L_max de resumen_3modelos.json (a 1e-6): si no, este
script no mide lo mismo que el MCMC.
"""
import json
import os
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
import ssee_core as S  # noqa: E402
from procedencia import cabecera, con_acta  # noqa: E402
print(cabecera(__file__), flush=True)

MC = os.path.join(_R, "src", "p02_mcmc", "ssee_paper2_mcmc.py")
NPZ = "/mnt/datos/SSEE_data/mcmc/paper2_3models/mcmc_chains_professional.npz"
RES = os.path.join(_R, "results", "logs", "resumen_3modelos.json")

# las funciones de verosimilitud del MCMC, sin correr el MCMC (todo lo anterior a la seccion 6)
_src = open(MC).read()
G = {"__file__": MC, "__name__": "ssee_paper2_mcmc_funciones"}
exec(_src[:_src.index("# 6. MCMC CON GUARDADO")], G)
res = json.load(open(RES))
N = res["N"]


def sondas(m, t):
    """(chi2_BAO, chi2_Planck, -2 ln prior) en el punto t del modelo m."""
    if m == "ssee":
        H0, ob = t
        om = G["WM_ALG"]
        Om = om / (H0 / 100) ** 2
        lb = G["ll_bao_full"](H0, om, ob, G["E_ssee"], Om)
        pr = 0.0
    elif m == "lcdm":
        H0, Om, ob = t
        lb = G["ll_bao_full"](H0, Om * (H0 / 100) ** 2, ob, G["E_lcdm"], Om, mnu=G["_MNU_LCDM"])
        pr = 0.0
    else:
        H0, Om, w0, wa, ob = t
        lb = G["ll_bao_full"](H0, Om * (H0 / 100) ** 2, ob, G["E_cpl"], Om, w0, wa, mnu=G["_MNU_LCDM"])
        pr = -0.5 * ((w0 + 1.0) / 0.5) ** 2 - 0.5 * wa ** 2   # el prior de lpost_cpl
    return -2 * lb, -2 * G["ll_planck"](H0, Om, ob), -2 * pr


d = np.load(NPZ)
por_modelo, control = {}, {}
for m in ("ssee", "lcdm", "cpl"):
    flat, lp = d[f"{m}_flat"], d[f"{m}_lp"]
    if m == "cpl":
        lL = lp - (-0.5 * ((flat[:, 2] + 1.0) / 0.5) ** 2 - 0.5 * flat[:, 3] ** 2)
    else:
        lL = lp
    i = int(np.nanargmax(lL))
    cb, cp, _ = sondas(m, flat[i])
    por_modelo[m] = dict(punto=[float(x) for x in flat[i]], chi2_BAO=cb, chi2_Planck=cp,
                         menos2lnL=cb + cp, k=int(flat.shape[1]), BIC=res["modelos"][m]["BIC"])
    control[m] = dict(lnL_max_resumen=res["modelos"][m]["lnL_max"], lnL_aqui=-(cb + cp) / 2,
                      dif=abs(res["modelos"][m]["lnL_max"] + (cb + cp) / 2))
pasa = all(c["dif"] < 1e-6 for c in control.values())

# SSEE en su punto algebraico, k = 0
H0, ob = S.H0_GLOBAL, S.OMEGA_B_H2
cb, cp, _ = sondas("ssee", (H0, ob))
bic0 = cb + cp + 0 * np.log(N)
fijo = dict(H0=H0, omega_b=ob, Om=G["WM_ALG"] / (H0 / 100) ** 2, k=0,
            chi2_BAO=cb, chi2_Planck=cp, menos2lnL=cb + cp, BIC=bic0,
            dchi2_vs_libre=cb + cp - por_modelo["ssee"]["menos2lnL"],
            dBIC_vs_libre=bic0 - por_modelo["ssee"]["BIC"],
            dBIC_ssee_menos_lcdm=bic0 - por_modelo["lcdm"]["BIC"],
            dBIC_ssee_menos_cpl=bic0 - por_modelo["cpl"]["BIC"],
            dBIC_lcdm_vs=por_modelo["lcdm"]["BIC"] - bic0,
            dBIC_cpl_vs=por_modelo["cpl"]["BIC"] - bic0)

out = dict(N=N, ssee_fijo=fijo, maximo_por_modelo=por_modelo,
           control=dict(criterio="ln L en el maximo de cada cadena = ln L_max de resumen_3modelos.json",
                        modelos=control, pasa=bool(pasa)))
print(json.dumps(dict(ssee_fijo=fijo, control_pasa=pasa), indent=1))
assert pasa, "CONTROL NO PASA: este script no reproduce la verosimilitud del MCMC"
with open(os.path.join(_R, "results", "logs", "p2_ssee_fijo_k0.json"), "w") as fh:
    json.dump(con_acta(out, __file__, entradas=[NPZ, RES]), fh, indent=1, ensure_ascii=False)
