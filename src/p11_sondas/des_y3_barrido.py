#!/usr/bin/env python3
"""des_y3_barrido.py — ¿de donde sale la diferencia con la cadena de DES Y3?

El calibrador (des_y3_calibra.py) reprodujo el max-post a +0.118 pero una
muestra lejana a +0.930, con criterio |dif| < 1. Evaluar el MISMO punto no
tiene ruido: +0.93 es un efecto sistematico que depende del punto. M. Almeida
lo marco (2026-09-27) como sospechoso de un numero mal usado.

Hecho ya: los 65 cortes de escala, los nuisance fijos y los neutrinos son los
mismos que en la cadena (su .ini va embebido en ella), y la instalacion pasa la
prueba de referencia de la propia libreria (6043.28 en [6043.23, 6043.37]).
Diferencia conocida: la cadena corrio CAMB Jan15 + halofit Takahashi como
modulo aparte; nosotros el CAMB actual con halofit dentro.

PRUEBA (criterio declarado ANTES de correr): 20 puntos de la cadena repartidos
por percentiles de Omega_m y S8 (semilla fija). Para cada uno,
dif = chi2_nuestro - chi2_cadena. Se correlaciona dif con cada parametro.
  * si el parametro que mas correlaciona es cosmologico de la potencia no
    lineal (omega_m, a_s, sigma_8/S8, h0, n_s) y dif varia suave  -> MOTOR
  * si es un nuisance (bias, IA, photo-z, m)                      -> USO
    INCORRECTO de ese parametro; se busca el error antes de seguir
Salida: results/logs/des_y3_barrido.json
"""
import json
import os
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from des_y3_calibra import evalua, lee_cadena, values_fijos  # noqa: E402

OUT = os.path.join(_R, "results", "logs", "des_y3_barrido.json")
N = 20
SEMILLA = 20260927        # ORIGEN-VALOR: 20260927 — semilla fija (la fecha), para que el barrido se repita


def main():
    cab, a = lee_cadena()
    ic = cab.index("DATA_VECTOR--2PT_CHI2")
    iw = cab.index("weight")
    om = a[:, cab.index("cosmological_parameters--omega_m")]
    s8c = [c for c in cab if c.upper() == "COSMOLOGICAL_PARAMETERS--S_8"]
    s8 = a[:, cab.index(s8c[0])] if s8c else None
    vivos = np.where(a[:, iw] > 0)[0]
    rng = np.random.default_rng(SEMILLA)
    # mitad por percentiles de Omega_m, mitad por S8 (o al azar si no hay S8)
    elegidos = []
    for eje in (om, s8 if s8 is not None else om):
        for q in np.linspace(0.03, 0.97, N // 2):
            obj = np.quantile(eje[vivos], q)
            cand = vivos[np.argsort(np.abs(eje[vivos] - obj))[:50]]
            elegidos.append(int(rng.choice(cand)))
    filas = []
    for n, k in enumerate(elegidos):
        v, fij = values_fijos(cab, a[k], f"barrido_{n:02d}")
        c = evalua(v, f"barrido_{n:02d}")
        pub = float(a[k, ic])
        filas.append(dict(indice=k, chi2_cadena=pub, chi2_nuestro=c, dif=c - pub,
                          parametros=fij,
                          S8=float(s8[k]) if s8 is not None else None))
        print(f"  {n:2d}  Om={om[k]:.4f}  chi2 cadena {pub:9.3f}  nuestro {c:9.3f}  dif {c - pub:+.3f}",
              flush=True)
    dif = np.array([f["dif"] for f in filas])
    corr = {}
    for p in filas[0]["parametros"]:
        x = np.array([f["parametros"][p] for f in filas])
        if x.std() > 0:
            corr[p] = float(np.corrcoef(x, dif)[0, 1])
    if s8 is not None:
        corr["S8 (derivado)"] = float(np.corrcoef([f["S8"] for f in filas], dif)[0, 1])
    orden = sorted(corr, key=lambda p: -abs(corr[p]))
    print(f"\n  dif: media {dif.mean():+.3f}  dispersion {dif.std():.3f}  "
          f"min {dif.min():+.3f}  max {dif.max():+.3f}")
    print("  correlacion de dif con cada parametro (las 8 mayores):")
    for p in orden[:8]:
        print(f"     {corr[p]:+.3f}  {p}")
    json.dump(dict(fecha="2026-09-27", semilla=SEMILLA, n=len(filas), filas=filas,
                   dif_media=float(dif.mean()), dif_std=float(dif.std()),
                   correlaciones=dict((p, corr[p]) for p in orden)),
              open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
