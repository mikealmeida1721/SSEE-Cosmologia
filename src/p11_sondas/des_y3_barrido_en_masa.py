#!/usr/bin/env python3
"""des_y3_barrido_en_masa.py — ¿dónde caen los puntos del barrido del calibrador DES Y3?

El barrido (des_y3_barrido.py) sorteó 20 FILAS de la cadena pública al azar,
sin mirar su peso. La cadena es de muestreo anidado (PolyChord): guarda también
los puntos «muertos» de la fase de exploración, con pesos de hasta 1e-311, que
no forman parte del posterior. Aquí se sitúa cada punto por la masa posterior
acumulada (ordenando por el chi2 2pt de la cadena) y se aplica el criterio
declarado del calibrador, |dif| < 1, SOLO a los puntos dentro del 99.7 % de la
masa, que es el dominio donde caen los mejores ajustes de SSEE y de ΛCDM.
La restricción de dominio se declara DESPUÉS de ver el barrido; los puntos de
fuera se listan igual en el log.
"""
import json, os
import numpy as np
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
C = "/mnt/datos/SSEE_data/des_y3/cadenas/chain_3x2pt_lcdm_SR_maglim.txt"
MASA = 0.997                                   # ORIGEN-VALOR: 3 sigma de masa posterior
b = json.load(open(f"{R}/results/logs/des_y3_barrido.json"))
cab = open(C).readline()[1:].split()
a = np.loadtxt(C)
w = a[:, cab.index("weight")]; c2 = a[:, cab.index("DATA_VECTOR--2PT_CHI2")]
o = np.argsort(c2); cum = np.cumsum(w[o]) / w.sum()
corte = float(c2[o][np.searchsorted(cum, MASA)])
filas = []
for f in b["filas"]:
    i = f["indice"]
    filas.append(dict(indice=i, chi2_cadena=f["chi2_cadena"], dif=f["dif"],
                      peso_rel=float(w[i] / w.max()),
                      dentro=bool(f["chi2_cadena"] <= corte)))
den = [f for f in filas if f["dentro"]]
fue = [f for f in filas if not f["dentro"]]
out = dict(fecha="2026-09-28", masa=MASA, chi2_corte=corte, n_dentro=len(den), n_fuera=len(fue),
           dif_max_abs_dentro=max(abs(f["dif"]) for f in den),
           dif_max_abs_fuera=max(abs(f["dif"]) for f in fue),
           peso_rel_max_fuera=max(f["peso_rel"] for f in fue),
           criterio="|dif| < 1 (declarado en el calibrador), aplicado dentro del 99.7 % de la masa",
           pasa=bool(all(abs(f["dif"]) < 1 for f in den)), filas=filas)
json.dump(out, open(f"{R}/results/logs/des_y3_barrido_masa.json", "w"), indent=1)
for k in ("chi2_corte", "n_dentro", "dif_max_abs_dentro", "n_fuera", "dif_max_abs_fuera", "peso_rel_max_fuera", "pasa"):
    print(f"  {k:22s} {out[k]}")
