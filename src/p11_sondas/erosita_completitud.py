#!/usr/bin/env python3
"""erosita_completitud.py — completitud PROPIA de la muestra de cosmologia de eRASS1.

POR QUE (2026-09-27). La seleccion oficial de eRASS1 (Clerc+2024, la que usa
Ghirardini+2024) NO es publica: es un proceso gaussiano entrenado sobre una
simulacion privada del survey; DR1 y DR2 no la traen. La S(L,z) de Zhong+2026
(arXiv:2602.20483, ec. 10-12) pone el 50 % de completitud en 5e-14, y con ella
el modelo de conteos dio chi2 ~3550/80 para los dos fondos.

METODO PROPIO. eFEDS es ~10 veces mas profundo que eRASS1 en su campo, asi que
su catalogo es casi el censo real. Completitud = fraccion de cumulos de eFEDS
que la muestra de COSMOLOGIA de eRASS1 (erass1cl_cosmology_v1.1, 5259) tambien
detecta. Cruce: separacion < RADIO y |dz|/(1+z) < 0.1. Se ajusta, cumulo a
cumulo (sin agrupar),
    C(F) = 1/2 erfc( (log F50 - log F) / (sqrt(2) ancho) )
por maxima verosimilitud binomial. Robustez: el radio del cruce se varia
(1.0, 1.5, 2.5 arcmin) y se prueba una pendiente en z.

Es el mismo tipo de comparacion que Clerc+2024 hace en su sec. 6 contra eFEDS:
si coincide, nuestro metodo reproduce el suyo por otra via.

Salida: results/logs/erosita_completitud.json
"""
import json
import os

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
E = "/mnt/datos/SSEE_data/erosita"
OUT = os.path.join(_R, "results", "logs", "erosita_completitud.json")
RADIOS = (1.0, 1.5, 2.5)       # ORIGEN-VALOR: 1.0/1.5/2.5 arcmin — radios de cruce de prueba (robustez), no medidas
DZ_MAX = 0.1                   # ORIGEN-VALOR: 0.1 — tolerancia |dz|/(1+z) de fotometrico vs fotometrico, declarada antes
Z_MIN, Z_MAX = 0.1, 0.8        # ORIGEN-VALOR: 0.1-0.8 — rango de z de la prueba (el mismo de erosita_conteos.py)


def lee():
    from astropy.io import fits
    f = fits.getdata(f"{E}/efeds/eFEDS_clusters_V3.2.fits.gz", 1)
    c = fits.getdata(f"{E}/erass1/erass1cl_cosmology_v1.1.fits", 1)
    z = f["z"].astype(float)
    F = f["F_500kpc"].astype(float)
    ok = np.isfinite(z) & (z >= Z_MIN) & (z <= Z_MAX) & np.isfinite(F) & (F > 0)
    return f[ok], z[ok], F[ok], c


def cruza(f, z, c, radio):
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    a = SkyCoord(f["RA"] * u.deg, f["DEC"] * u.deg)
    b = SkyCoord(c["RA"] * u.deg, c["DEC"] * u.deg)
    i, sep, _ = a.match_to_catalog_sky(b)
    dz = np.abs(c["Z_LAMBDA"][i] - z) / (1 + z)
    return ((sep.arcmin < radio) & (dz < DZ_MAX)).astype(float)


def ajusta(lf, z, det, conz=False):
    from scipy.optimize import minimize
    from scipy.special import erfc

    def nll(p):
        m50 = p[0] + (p[2] * (z - 0.3) if conz else 0.0)
        C = np.clip(0.5 * erfc((m50 - lf) / (np.sqrt(2) * abs(p[1]))), 1e-9, 1 - 1e-9)
        return -np.sum(det * np.log(C) + (1 - det) * np.log(1 - C))
    x0 = [-12.6, 0.2] + ([0.0] if conz else [])
    r = minimize(nll, x0, method="Nelder-Mead",
                 options=dict(xatol=1e-6, fatol=1e-8, maxiter=5000))
    return r


def main():
    from scipy.stats import beta
    f, z, F, c = lee()
    lf = np.log10(F)
    res = dict(fecha="2026-09-27", n_efeds=int(len(z)), rango_z=[Z_MIN, Z_MAX],
               zhong_F50=5e-14, radios={})
    for rad in RADIOS:
        det = cruza(f, z, c, rad)
        r, rz = ajusta(lf, z, det), ajusta(lf, z, det, True)
        res["radios"][str(rad)] = dict(detectados=int(det.sum()), logF50=float(r.x[0]),
                                       ancho_dex=float(abs(r.x[1])),
                                       pendiente_z=float(rz.x[2]),
                                       mejora_2lnL_con_z=float(2 * (r.fun - rz.fun)))
        print(f"  radio {rad}': {int(det.sum())} detectados  log F50 = {r.x[0]:.3f}  "
              f"ancho {abs(r.x[1]):.3f} dex  (pendiente z {rz.x[2]:+.3f}, "
              f"mejora {2 * (r.fun - rz.fun):.2f})")
    det = cruza(f, z, c, 1.5)
    tabla = []
    bordes = [-14.5, -13.5, -13.25, -13.0, -12.75, -12.5, -11.0]  # ORIGEN-VALOR: bordes de la tabla de lectura, no entran al ajuste
    for a, b in zip(bordes[:-1], bordes[1:]):
        m = (lf >= a) & (lf < b)
        n, k = int(m.sum()), int((det * m).sum())
        lo = beta.ppf(0.16, k, n - k + 1) if k > 0 else 0.0
        hi = beta.ppf(0.84, k + 1, n - k) if k < n else 1.0
        tabla.append(dict(logF=[a, b], detectados=k, total=n, completitud=k / n,
                          banda_68=[float(lo), float(hi)]))
    res["tabla_radio_1.5"] = tabla
    base = res["radios"]["1.5"]
    res["F50"] = 10 ** base["logF50"]
    res["factor_vs_zhong"] = res["F50"] / res["zhong_F50"]
    print(f"  F50 = {res['F50']:.2e}  ->  {res['factor_vs_zhong']:.1f} veces el 5e-14 de Zhong")
    json.dump(res, open(OUT, "w"), indent=1)
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
