#!/usr/bin/env python3
"""analiza_boss_lcdm_libre.py — ¿el control LCDM libre de BOSS reproduce lo publicado? (2026-10-18)

QUE SE COMPARA CON QUE.
  Nuestro: LCDM con su fondo LIBRE (Omega_m, H_0, logA muestreados; omega_b,
           n_s fijos como en el blanco), corrido por nosotros con
           cobaya_boss_lcdm_libre.py sobre BOSS DR12 z1+z3 (Beutler+2017),
           velocileptors LPT a un lazo, k <= 0.20, l = 0, 2, 4.
  Blanco:  Chen, Vlah & White 2022 (arXiv:2110.05530), columna P_ell: el mismo
           codigo y los mismos bines, corridos por ellos sobre Beutler+2021.
  Estimador: media y desviacion pesadas de la posterior, tras quitar el
           burn-in (_QUEMA de multisonda_fondo_clavado.py, el mismo de todo P6).

CRITERIO. Dos configuraciones (BOSS_CONFIG de cobaya_boss_lcdm_libre.py):
  'chen'   = la del blanco (l = 0, 2; k en [0.02, 0.20]). Es la prueba de que el
             pipeline reproduce lo publicado: |nuestro - publicado| < 1 sigma
             publicado en logA, Omega_m, H_0 y sigma_8. Si no, no se escribe.
  'propia' = la que corre SSEE (l = 0, 2, 4; k en [0.01, 0.20]). Se informa su
             distancia al blanco y la diferencia propia - chen (lo que mueven el
             hexadecapolo y los k bajos), sin compuerta.
HISTORIA DEL CRITERIO, dicha: el primero (2026-10-17) era 1 sigma sobre la
'propia'. Su cadena, aun sin converger (R-1 0.083), quedo al borde (Omega_m
-1.07, H_0 -1.03 sigma). En vez de aflojar el umbral se agrego la configuracion
del blanco, que es la comparacion que corresponde, y el criterio se fijo antes de
correrla. Las dos cadenas deben estar convergidas (R-1 < 0.05).

CONTROL DEL CONTROL (R53). Se mide tambien la distancia del fondo de Planck
FIJO (Omega_m = 0.3153, H_0 = 67.36) al posterior libre: dice cuanto mueve el
fondo, que es justo lo que la fila LCDM de Planck fijo no puede ver.

Salida: results/logs/growth_2026-07/boss_lcdm_libre.json
"""
import ast
import json
import os
import re
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)
CAD = "/mnt/datos/SSEE_data/chains_p6/boss_lcdm_libre"
SRC = os.path.join(_R, "src", "p06_growth", "cobaya_boss_lcdm_libre.py")
SALIDA = os.path.join(_R, "results", "logs", "growth_2026-07", "boss_lcdm_libre.json")
QUEMA = float(re.search(r"^_QUEMA\s*=\s*([0-9.]+)", open(os.path.join(_R, "src", "p06_growth", "multisonda_fondo_clavado.py")).read(), re.M).group(1))
TOL_R1 = 0.05

# el blanco se lee del script que corrio la cadena (una sola fuente), sin importarlo (importarlo rehace CAMB)
_arbol = ast.parse(open(SRC).read())
BLANCO = next(ast.literal_eval(n.value) if isinstance(n.value, ast.Dict) else
              {k.arg: ast.literal_eval(k.value) for k in n.value.keywords}
              for n in _arbol.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "BLANCO")
PLANCK = dict(Om=0.3153, H0=67.36)   # ORIGEN-VALOR: el fondo FIJO de la fila LCDM de cobaya_boss.py (R.COSMO['LCDM'], Planck 2018 TT,TE,EE+lowE+lensing)

def lee(nombre):
    cads, fs = [], []
    for i in (1, 2, 3, 4):
        f = f"{CAD}/{nombre}.{i}.txt"
        cab = open(f).readline().lstrip("#").split()
        x = np.loadtxt(f)
        cads.append(x[int(QUEMA * len(x)):])
        fs.append(f)
    S = np.vstack(cads)
    r1 = float(open(f"{CAD}/{nombre}.progress").read().strip().splitlines()[-1].split()[3])
    return cab, S, r1, fs


def resumen(nombre):
    cab, S, r1, fs = lee(nombre)
    w = S[:, cab.index("weight")]
    est = {}
    for p in ("logA", "Om", "H0", "sigma8", "S8", "fs8_38", "fs8_61"):
        y = S[:, cab.index(p)]
        m = float(np.average(y, weights=w))
        est[p] = dict(nuestro=m, sigma=float(np.sqrt(np.average((y - m) ** 2, weights=w))))
        if p in BLANCO:
            mp, sp = BLANCO[p]
            est[p].update(publicado=mp, sigma_publicado=sp, distancia_sigma_publicado=(m - mp) / sp)
    pl = {p: dict(planck=PLANCK[p], distancia_sigma=(PLANCK[p] - est[p]["nuestro"]) / est[p]["sigma"]) for p in PLANCK}
    out = dict(n=int(len(S)), R_menos_1=r1, chi2_min=float(S[:, cab.index("chi2")].min()),
               parametros=est, planck_fijo_vs_libre=pl,
               dentro_1sigma=bool(all(abs(est[p]["distancia_sigma_publicado"]) < 1.0 for p in ("logA", "Om", "H0", "sigma8"))),
               convergida=bool(r1 < TOL_R1))
    print(f"  [{nombre}] R-1 {r1:.4f}  n {len(S)}  chi2_min {out['chi2_min']:.3f}")
    for p, e in est.items():
        extra = f"   publicado {e['publicado']} ± {e['sigma_publicado']}  ({e['distancia_sigma_publicado']:+.2f} sigma)" if "publicado" in e else ""
        print(f"    {p:7s} {e['nuestro']:.4f} ± {e['sigma']:.4f}{extra}")
    return out, fs


entradas = [SRC]
out = dict(que_se_compara="LCDM fondo libre (corrido aqui, BOSS DR12 Beutler+2017 z1+z3) contra Chen, Vlah & White 2022 (P_ell, Beutler+2021)",
           blanco=BLANCO["fuente"], quema=QUEMA)
for cfg, nombre in (("chen", "lcdm_libre_chen"), ("propia", "lcdm_libre")):
    out[cfg], fs = resumen(nombre)
    entradas += fs
out["propia_menos_chen"] = {p: out["propia"]["parametros"][p]["nuestro"] - out["chen"]["parametros"][p]["nuestro"]
                            for p in out["propia"]["parametros"]}
out["pasa"] = bool(out["chen"]["dentro_1sigma"] and out["chen"]["convergida"] and out["propia"]["convergida"])
print(f"  -> {'PASA' if out['pasa'] else 'NO PASA'} (config chen dentro de 1 sigma y ambas convergidas)")
if not out["pasa"]:
    sys.exit("el control no reproduce lo publicado (o no convergio): no se escribe")
json.dump(con_acta(out, __file__, entradas=entradas), open(SALIDA, "w"), indent=1)
print(f"  escrito -> {os.path.relpath(SALIDA, _R)}")
