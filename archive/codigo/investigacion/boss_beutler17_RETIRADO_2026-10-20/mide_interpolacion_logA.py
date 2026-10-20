#!/usr/bin/env python3
"""mide_interpolacion_logA.py — ¿la tabla LPT interpolada en logA es la exacta? (2026-10-17)

POR QUE. Hasta el 2026-10-17 el modelo de BOSS construia la tabla LPT una vez, a
A_REF, y escalaba la salida por A_s/A_REF; eso es falso a un lazo (+3.88 en chi2
en el mejor punto de SSEE, ver AS_REF en boss_lpt_R1R2.py). Ahora la tabla se
construye en N_NODOS de logA y se interpola. Esta prueba compara, para cada
modelo y cada conjunto, el chi2 marginal con la tabla INTERPOLADA contra el chi2
con la tabla REHECHA a ese logA (sin interpolar), en varios logA del rango que
recorren las cadenas, con los bias del mejor punto de la cadena de cada modelo.

CRITERIO. |dchi2| < 0.01 en cada punto (cien veces por debajo de lo que se lee
de BOSS, que son diferencias de orden 0.3). Si no se cumple, no se escribe.

CONTROL (R53). Se mide tambien el error del metodo VIEJO (salida escalada) en
los mismos puntos: tiene que ser grande donde logA se aleja de A_REF (3.0445) y
~0 en A_REF. Si el viejo no falla, la prueba no distingue nada.

Salida: results/logs/growth_2026-07/interpolacion_logA.json
"""
import copy
import json
import os
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p06_growth"))
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)
sys.argv = [sys.argv[0], "0.20"]
import boss_lpt_R1R2 as R  # noqa: E402
from velocileptors.LPT.lpt_rsd_fftw import LPT_RSD  # noqa: E402

CAD = "/mnt/datos/SSEE_data/chains_p6/boss"
PUNTOS = [2.40, 2.76, 3.0445, 3.30, 3.60]   # ORIGEN-VALOR: el rango que recorren las cadenas z1+z3 (logA 2.76 ± 0.12) con holgura, A_REF y la zona alta del prior
TOL = 0.01
SALIDA = os.path.join(_R, "results", "logs", "growth_2026-07", "interpolacion_logA.json")

SETS = R.build()


def bias_mejor(nombre):
    cab = open(f"{CAD}/{nombre}.1.txt").readline().lstrip("#").split()
    X = np.vstack([np.loadtxt(f"{CAD}/{nombre}.{i}.txt") for i in (1, 2, 3, 4)])
    b = X[np.argmin(X[:, cab.index("chi2")])]
    return {f"{st['zb']}{st['cap']}": [float(b[cab.index(f"{k}_{st['zb']}{st['cap']}")]) for k in ("b1", "b2", "bs")]
            for st in SETS}


def exacta(st, name, logA):
    """Copia del conjunto con UNA tabla rehecha a ese logA (un solo nodo = sin interpolar)."""
    c = R.COSMO[name]
    kl, pl, fz, s8 = R.camb_lin(c, st["z"])
    a_par, a_per = R.M.alphas(st["z"], c["Om"], c["w0"], c["wa"])
    L = LPT_RSD(kl, pl * np.exp(logA) * 1e-10 / R.AS_REF, kIR=0.2, cutoff=10,
                extrap_min=-4, extrap_max=3, N=2000, threads=1, jn=5)
    L.make_pltable(fz, kv=st["kmod"], apar=a_par, aperp=a_per, ngauss=3)
    Y = np.repeat(np.stack([L.p0ktable, L.p2ktable, L.p4ktable])[None], R.N_NODOS, axis=0)
    st2 = copy.copy(st)
    st2["lpt"] = dict(st["lpt"])
    st2["lpt"][name] = dict(st["lpt"][name], L=L, Y=Y, sigma8=s8 * (1 + 1e-9 * logA))  # clave propia en la cache
    return st2


def escalada(st, name, logA):
    """El metodo viejo: la tabla del nodo mas cercano a A_REF, salida por A_s/A_REF."""
    st2 = exacta(st, name, np.log(R.AS_REF * 1e10))
    lp = st2["lpt"][name]
    lp["Y"] = lp["Y"] * (np.exp(logA) * 1e-10 / R.AS_REF)   # escala TODO, como antes
    lp["sigma8"] = lp["sigma8"] * (1 + 2e-9 * logA)
    return st2


out = {"criterio": f"|chi2 interpolado - chi2 exacto| < {TOL} en cada (modelo, punto)", "nodos": R.LOGA_NODOS.tolist(),
       "puntos": PUNTOS, "modelos": {}}
peor = 0.0
for name, cad in (("SSEE", "ssee"), ("LCDM", "lcdm")):
    bm = bias_mejor(cad)
    filas = []
    for a in PUNTOS:
        ci = ce = cv = 0.0
        for st in SETS:
            th = bm[f"{st['zb']}{st['cap']}"]
            ci += R.chi2_marg_set(st, name, a, th)[0]
            ce += R.chi2_marg_set(exacta(st, name, a), name, a, th)[0]
            cv += R.chi2_marg_set(escalada(st, name, a), name, a, th)[0]
        filas.append(dict(logA=a, chi2_interpolado=ci, chi2_exacto=ce, chi2_viejo_escalado=cv,
                          dif_interpolado=ci - ce, dif_viejo=cv - ce))
        peor = max(peor, abs(ci - ce))
        print(f"  {name} logA={a:.4f}: exacto {ce:.4f}  interpolado {ci - ce:+.2e}  viejo {cv - ce:+.3f}", flush=True)
    out["modelos"][name] = filas
viejo_ref = max(abs(f["dif_viejo"]) for m in out["modelos"].values() for f in m if abs(f["logA"] - 3.0445) < 1e-9)
viejo_lejos = max(abs(f["dif_viejo"]) for m in out["modelos"].values() for f in m)
out["peor_interpolado"] = peor
out["control_viejo"] = dict(en_A_REF=viejo_ref, maximo=viejo_lejos, pasa=bool(viejo_ref < TOL and viejo_lejos > 10 * TOL))
out["pasa"] = bool(peor < TOL and out["control_viejo"]["pasa"])
print(f"  peor interpolado {peor:.2e} (criterio {TOL}); viejo en A_REF {viejo_ref:.2e}, maximo {viejo_lejos:.3f} -> {'PASA' if out['pasa'] else 'NO PASA'}")
if not out["pasa"]:
    sys.exit("la interpolacion no reproduce la tabla exacta (o el control no distingue): no se escribe")
entradas = [f"{CAD}/{m}.{i}.txt" for m in ("ssee", "lcdm") for i in (1, 2, 3, 4)]
json.dump(con_acta(out, __file__, entradas=entradas), open(SALIDA, "w"), indent=1)
print(f"  escrito -> {os.path.relpath(SALIDA, _R)}")
