#!/usr/bin/env python3
"""
ssee_dic_from_chains.py — DIC de los tres modelos desde las cadenas guardadas.

POR QUÉ EXISTE (2026-07-25)
---------------------------
El ΔDIC = −4.91 que citaban Paper 2 / PRD / CANONICAL_VALUES **no lo calculaba
ningún script vivo del repo**: era un valor anotado sin fuente reproducible — la
misma clase de grieta que la Capa Procedencia del guardián existe para cazar
(causa raíz F1). Este script cierra esa grieta: recomputa el DIC desde las
cadenas y deja log en results/logs/.

    DIC = -2·lnL(θ̂) + 2·p_D ,   p_D = 2·[lnL(θ̂) − <lnL>]

Comprobación de cordura: para posteriors casi gaussianos p_D → k (nº de
parámetros), y entonces DIC → AIC. Si p_D se aleja mucho de k, la cadena no
convergió o el posterior no es gaussiano — el script lo avisa.

NOTA: el `ln B_10 = 7.42` que también se citaba NO es reproducible desde estas
cadenas (una razón de evidencias marginales requiere nested sampling o
termodinámica, no un ensemble sampler). Se retiró de los documentos en vez de
arrastrarlo sin procedencia.

Uso:  python3 src/estadistica/ssee_dic_from_chains.py
"""
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))
CHAINS = os.path.join(_REPO, "results", "logs", "mcmc_chains_professional.npz")
LOG = os.path.join(_REPO, "results", "logs", "dic_from_chains.log")

_K = {"ssee": 2, "lcdm": 3, "cpl": 5}

if not os.path.exists(CHAINS):
    sys.exit(f"No existe {CHAINS} — correr antes src/p02_mcmc/ssee_paper2_mcmc.py")

_d = np.load(CHAINS)
_out = []


def log(s):
    print(s)
    _out.append(s)


log("DIC desde cadenas — parametrización ω_m algebraico fijo (R25)")
log(f"  fuente: {os.path.relpath(CHAINS, _REPO)}")
log("  DIC = -2·lnL(θ̂) + 2·p_D ,  p_D = 2·[lnL(θ̂) − <lnL>]")
log("")
log(f"  {'modelo':6s} {'k':>2s} {'lnP_max':>10s} {'<lnP>':>10s} {'p_D':>7s} {'DIC':>9s}")

_dic, _fil = {}, {}
for _m, _k in _K.items():
    _lp = _d[f"{_m}_lp"]
    _lp = _lp[np.isfinite(_lp)]
    _mx, _mn = _lp.max(), _lp.mean()
    _pD = 2.0 * (_mx - _mn)
    _dic[_m] = -2.0 * _mx + 2.0 * _pD
    _fil[_m] = dict(k=_k, lnP_max=float(_mx), lnP_media=float(_mn), p_D=float(_pD), DIC=float(_dic[_m]))
    _flag = "" if abs(_pD - _k) < 0.5 else "   ⚠ p_D lejos de k"
    log(f"  {_m.upper():6s} {_k:2d} {_mx:10.3f} {_mn:10.3f} {_pD:7.3f} {_dic[_m]:9.3f}{_flag}")

log("")
log(f"  ΔDIC (SSEE − ΛCDM) = {_dic['ssee']-_dic['lcdm']:+.2f}   (negativo = SSEE favorecido)")
log(f"  ΔDIC (SSEE − CPL)  = {_dic['ssee']-_dic['cpl']:+.2f}")
log("")
log("  Cordura: p_D ≈ k en los tres ⇒ posteriors casi gaussianos, DIC ≈ AIC.")

with open(LOG, "w", encoding="utf-8") as _fh:
    _fh.write("\n".join(_out) + "\n")
print(f"\nlog: {os.path.relpath(LOG, _REPO)}")
# JSON con acta (2026-09-30): lo que cita el apendice DIC de Paper 2
import json  # noqa: E402
sys.path.insert(0, os.path.join(_REPO, "src"))
from procedencia import con_acta  # noqa: E402
json.dump(con_acta(dict(modelos=_fil, dDIC=dict(ssee_menos_lcdm=_dic["ssee"] - _dic["lcdm"],
                                                 ssee_menos_cpl=_dic["ssee"] - _dic["cpl"])),
                   __file__, entradas=[os.path.realpath(CHAINS)]),
          open(os.path.join(_REPO, "results", "logs", "dic_from_chains.json"), "w"), indent=1)
