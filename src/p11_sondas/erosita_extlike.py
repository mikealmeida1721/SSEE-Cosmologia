#!/usr/bin/env python3
"""erosita_extlike.py — ¿de que depende EXT_LIKE? La seleccion REAL de la muestra de cosmologia.

POR QUE (2026-09-29). La muestra de cosmologia de eRASS1 se corta en EXT_LIKE > 6
(Ghirardini+2024, .tex L2018), no en fotones. EXT_LIKE depende de los fotones Y del
tamano aparente del cumulo (masa y distancia): a igual tasa de cuentas, uno grande y
cercano se ve extendido distinto que uno chico y lejano. El modelo anterior
(erosita_cr.py) seleccionaba solo en fotones; la pendiente B_X a +17 sigma en todos
los modelos es lo que eso deja. Aqui se MIDE la seleccion en el catalogo primario
(EXT_LIKE >= 3), sin nada de Zhong.

METODO. ln EXT_LIKE = X·beta + ruido normal con sigma(X), truncado en EXT_LIKE = 3
(regresion Tobit truncada). Control (declarado antes): la fraccion con EXT_LIKE > 6
predicha contra la observada, en 8 casillas de cada variable; pasa si ninguna casilla
se desvia mas de 2 sigma binomiales.

LIMITE CONOCIDO: el primario tambien exige DET_LIKE >= 5; aqui solo se modela el
recorte en EXT_LIKE. Salida: results/logs/erosita_extlike.json
"""
import json, os
import numpy as np
from astropy.io import fits
from astropy.cosmology import Planck18
from scipy.optimize import minimize
from scipy.stats import norm
R_ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
p = fits.getdata("/mnt/datos/SSEE_data/erosita/erass1/erass1cl_primary_v3.2.fits", 1)
e, z, R, c, T = (p[k].astype(float) for k in ("EXT_LIKE", "BEST_Z", "R500", "CTS500", "EXP"))
m = np.isfinite(e) & (c > 0) & (z > 0.1) & (z < 0.8) & (R > 0) & (T > 0)   # ORIGEN-VALOR: 0.1-0.8 — rango de la muestra de cosmologia
ln = np.log(c[m]); lT = np.log(T[m])
lt = np.log(R[m] / Planck18.angular_diameter_distance(z[m]).to("kpc").value * 206265 / 60)  # theta500 en arcmin (cosmologia de referencia, declarada)
le = np.log(e[m]); obs = e[m] > 6; cut = np.log(3.0); one = np.ones_like(ln)
res = dict(fecha="2026-09-29", N=int(m.sum()), modelos={})
for nom, X, Xs in (("nu_theta", np.c_[one, ln, lt], np.c_[one, ln]),
                   ("nu_theta_T", np.c_[one, ln, lt, lT], np.c_[one, ln]),
                   ("nu_theta_T_cruzado", np.c_[one, ln, lt, lT, ln * lt], np.c_[one, ln, lT])):
    k = X.shape[1]
    def nll(q):
        mu = X @ q[:k]; s = np.exp(Xs @ q[k:])
        return -(norm.logpdf(le, mu, s) - norm.logsf(cut, mu, s)).sum()
    q0 = np.r_[0, 1, np.zeros(k - 2), np.log(.6), np.zeros(Xs.shape[1] - 1)]
    r = minimize(nll, q0, method="Powell", options=dict(maxiter=300000, xtol=1e-7, ftol=1e-9))
    mu = X @ r.x[:k]; s = np.exp(Xs @ r.x[k:]); pred = norm.sf(np.log(6), mu, s) / norm.sf(cut, mu, s)
    tir = []
    for v in (ln, lt, lT):
        qq = np.quantile(v, np.linspace(0, 1, 9))
        for i in range(8):
            b = (v >= qq[i]) & (v <= qq[i + 1]); pm = pred[b].mean()
            tir.append(float((obs[b].mean() - pm) / np.sqrt(pm * (1 - pm) / b.sum())))
    tir = np.array(tir)
    res["modelos"][nom] = dict(params=r.x.tolist(), menos_lnL=float(r.fun), peor_sigma=float(np.abs(tir).max()),
                               chi2_casillas=float((tir ** 2).sum()), n_casillas=len(tir),
                               pasa=bool(np.abs(tir).max() < 2))
    print(f"  {nom:22s} peor {np.abs(tir).max():.1f} sigma  chi2 {np.sum(tir**2):.1f}/{len(tir)}  -> {'PASA' if np.abs(tir).max() < 2 else 'NO PASA'}")
json.dump(res, open(os.path.join(R_, "results", "logs", "erosita_extlike.json"), "w"), indent=1)
