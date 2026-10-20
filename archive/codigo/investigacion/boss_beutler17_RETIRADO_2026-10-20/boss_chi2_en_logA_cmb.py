#!/usr/bin/env python3
"""boss_chi2_en_logA_cmb.py — cuánto le cuesta a BOSS que A_s se clave al del CMB (2026-10-17).

QUÉ MIDE. El χ² del perfil de BOSS (LPT, k ≤ 0.20, fondo de SSEE fijo, un solo
sector, SIN partícula) en el log(10¹⁰A_s) que mide el CMB del propio modelo, y su
diferencia con el mínimo del perfil. Es el «cuesta clavar» de Paper 6 §BOSS: BOSS
no vota en la amplitud. (Era 0.63, luego 0.60, con el perfil de 3 bines solapados
y A_s escalado; ambos errores se corrigieron el 2026-10-17.)

POR QUÉ EXISTE. Ese número salía de `base_sin_particula.json`, el control sin
partícula de la rejilla de la cola #28 (`conjunta_tres_sondas.py`, partícula
térmica contra KiDS-1000). La partícula está retirada (2026-08-01; KiDS-Legacy
la deja innecesaria, 2026-09-20) y esa familia se archivó: el número de BOSS no
necesita nada de ella. Además aquel valor era el nodo de rejilla logA = 3.045, no
el logA del CMB (3.0432): aquí se evalúa en el valor medido.

CÓMO. El perfil sellado tiene χ²(logA) en una rejilla fija de paso 0.05. Se ajusta
una parábola a los tres nodos más cercanos al logA del CMB y se evalúa ahí: el
mismo método con que `boss_lpt_R1R2.run` ubica su mínimo. La incertidumbre del método
es la diferencia con la parábola de los otros tres nodos que rodean ese logA.
Control (R53): sobre el perfil VIEJO archivado (3 bines, A_s escalado), la
interpolación LINEAL en el nodo 3.045 tiene que dar el 198.07 de base_sin_particula
(así se calculaba allí): prueba que esta lectura es la de entonces; y la parábola
reproduce sus tres nodos del perfil nuevo.

ENTRADAS (selladas): results/logs/growth_2026-07/R1R2_boss_lpt_kmax0.200.json
                     results/logs/growth_2026-07/quien_mide_As.json
                     archive/logs_superados/R1R2_boss_lpt_kmax0.200_20261015_3bines_As_escalado.json (solo el control)
SALIDA: results/logs/growth_2026-07/boss_chi2_en_logA_cmb.json
"""
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from procedencia import con_acta  # noqa: E402

G = REPO / "results" / "logs" / "growth_2026-07"
BOSS = G / "R1R2_boss_lpt_kmax0.200.json"
AS = G / "quien_mide_As.json"
VIEJO = REPO / "archive" / "logs_superados" / "R1R2_boss_lpt_kmax0.200_20261015_3bines_As_escalado.json"
SALIDA = G / "boss_chi2_en_logA_cmb.json"


def main():
    b = json.load(open(BOSS))["SSEE"]
    a = json.load(open(AS))["CMB"]
    x, y = np.array(b["perfil"]["logA"]), np.array(b["perfil"]["chi2"])
    l_cmb, s_cmb = float(a["logA"]), float(a["sigma"])
    i = np.argsort(np.abs(x - l_cmb))[:3]
    i.sort()
    cf = np.polyfit(x[i], y[i], 2)
    chi2_cmb = float(np.polyval(cf, l_cmb))
    chi2_min, l_min = float(b["chi2"]), float(b["logA"])
    # incertidumbre del método: la otra terna de nodos que encierra l_cmb
    j = np.searchsorted(x, l_cmb)
    otra = [k for k in ([j - 2, j - 1, j], [j - 1, j, j + 1]) if sorted(k) != i.tolist()][0]
    chi2_otra = float(np.polyval(np.polyfit(x[otra], y[otra], 2), l_cmb))
    # control R53
    resid = float(np.max(np.abs(np.polyval(cf, x[i]) - y[i])))
    bv = json.load(open(VIEJO))["SSEE"]["perfil"]
    lineal_3045 = float(np.interp(3.045, bv["logA"], bv["chi2"]))
    ok = resid < 1e-6 and round(lineal_3045, 2) == 198.07
    out = dict(
        que_mide="chi2 del perfil de BOSS (SSEE, sin particula) en el logA del CMB del modelo",
        logA_cmb=l_cmb, sigma_logA_cmb=s_cmb,
        logA_min_boss=l_min, sigma_logA_boss=float(b["sig_logA"]),
        chi2_min_boss=chi2_min, chi2_en_logA_cmb=chi2_cmb,
        cuesta_clavar=chi2_cmb - chi2_min,
        nodos_usados=x[i].tolist(), parabola=cf.tolist(),
        metodo=dict(nodos_otra_terna=x[otra].tolist(), chi2_otra_terna=chi2_otra,
                    diferencia=chi2_otra - chi2_cmb),
        control=dict(residuo_en_nodos=resid, lineal_en_nodo_3045_perfil_viejo=lineal_3045,
                     referencia_base_sin_particula=198.07, pasa=bool(ok)),
    )
    json.dump(con_acta(out, __file__, entradas=[BOSS, AS, VIEJO]), open(SALIDA, "w"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
