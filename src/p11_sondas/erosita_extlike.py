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

LIMITE CONOCIDO (modelos 1-3): el primario tambien exige DET_LIKE >= 5; ahi solo se
modela el recorte en EXT_LIKE. Los tres NO pasan (peor 8.8 sigma).

MODELO CONJUNTO (modo «conjunto», 2026-09-29, declarado ANTES de correr).
(ln EXT_LIKE, ln DET_LIKE) ~ normal bivariada con medias lineales en (ln CTS500,
ln theta500, ln EXP), sigmas dependientes de ln CTS500 y correlacion rho libre,
truncada a la vez en EXT_LIKE >= 3 Y DET_LIKE >= 5 (el recorte real del primario;
correlacion medida en el primario: 0.86). La fraccion con EXT_LIKE > 6 predicha es
P(EXT>6, DET>=5)/P(EXT>=3, DET>=5). MISMO control y MISMO criterio que los modelos
1-3: 24 casillas, pasa si ninguna se desvia mas de 2 sigma binomiales. Si no pasa,
eROSITA queda BLOQUEADA en la seleccion (la de Clerc+2024 no se publica como archivo).
RESULTADO: NO pasa (peor 11.3 sigma; los cumulos de mas cuentas con EXT_LIKE <= 6).

MODELO CONJUNTO + CONCENTRACION (modo «conjunto_c», declarado ANTES de correr).
Diagnostico: a igual numero de cuentas, los que quedan bajo EXT_LIKE 6 difieren en
FORMA: entre los brillantes son MAS difusos (C_R500 mediana -1.28 frente a -0.64),
entre los debiles MAS concentrados. Se agrega UNA variable medida por cumulo:
C_R500 (log concentracion, catalogo publico de morfologia Sanders+2025, DR1
SandersJ_DR1/erass1_cluster_morphology_v1.0, sha256 25ecc6a6..., cruce por DETUID,
cobertura 100 %). Mismo control, mismo criterio (24 casillas + 8 de C_R500, todas < 2 sigma).
RESULTADO: NO pasa (peor 13.2 sigma, chi2 439.7/32) aunque -lnL baja de 9857 a 7202: el
efecto de la forma CAMBIA DE SIGNO con las cuentas, y eso solo lo captura un modelo del
perfil (Clerc+2024 usa brillo en 7 anillos x 5 componentes, entrenado en sus simulaciones
gemelas, no publicas). VEREDICTO segun el criterio declarado: eROSITA BLOQUEADA en la
seleccion. No se agregan mas variables: seria buscar que pase, no informacion nueva.
Salida: results/logs/erosita_extlike.json
"""
import json, os, sys
import numpy as np
from astropy.io import fits
from astropy.cosmology import Planck18
from scipy.optimize import minimize
from scipy.stats import norm
from scipy.special import log_ndtr, ndtri_exp, logsumexp
R_ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
p = fits.getdata("/mnt/datos/SSEE_data/erosita/erass1/erass1cl_primary_v3.2.fits", 1)
e, z, R, c, T, d = (p[k].astype(float) for k in ("EXT_LIKE", "BEST_Z", "R500", "CTS500", "EXP", "DET_LIKE_0"))
m = np.isfinite(e) & np.isfinite(d) & (c > 0) & (z > 0.1) & (z < 0.8) & (R > 0) & (T > 0)   # ORIGEN-VALOR: 0.1-0.8 — rango de la muestra de cosmologia
ln = np.log(c[m]); lT = np.log(T[m])
lt = np.log(R[m] / Planck18.angular_diameter_distance(z[m]).to("kpc").value * 206265 / 60)  # theta500 en arcmin (cosmologia de referencia, declarada)
le = np.log(e[m]); obs = e[m] > 6; cut = np.log(3.0); one = np.ones_like(ln)
ld = np.log(d[m]); cutd = np.log(5.0)
OUT = os.path.join(R_, "results", "logs", "erosita_extlike.json")


def casillas(pred):
    tir = []
    for v in (ln, lt, lT):
        qq = np.quantile(v, np.linspace(0, 1, 9))
        for i in range(8):
            b = (v >= qq[i]) & (v <= qq[i + 1]); pm = pred[b].mean()
            tir.append(float((obs[b].mean() - pm) / np.sqrt(pm * (1 - pm) / b.sum())))
    return np.array(tir)


_u, _w = np.polynomial.legendre.leggauss(64)


def lcola2(a, b, r):
    """ln P(X>=a, Y>=b), normales estandar con correlacion r, TODO en logaritmos (sin recortes).
    x = Phi^-1 de la cola condicionada a x>=a (v uniforme en (0,1), Gauss-Legendre 64);
    ln P = ln Phi(-a) + ln < Phi(-(b - r x)/sqrt(1-r^2)) >_v.
    (La version anterior recortaba P en 1e-300 y el optimizador aprovechaba el desborde.)"""
    la = log_ndtr(-a)[:, None]; v = (_u[None, :] + 1) / 2
    x = -ndtri_exp(la + np.log(v))
    li = log_ndtr(-(b[:, None] - r * x) / np.sqrt(1 - r * r))
    return la[:, 0] + logsumexp(li + np.log(_w / 2)[None, :], axis=1)


if len(sys.argv) > 1 and sys.argv[1] in ("conjunto", "conjunto_c"):
    res = json.load(open(OUT)); conc = sys.argv[1] == "conjunto_c"
    X = np.c_[one, ln, lt, lT]; Xs = np.c_[one, ln]
    if conc:
        mo = fits.getdata("/mnt/datos/SSEE_data/erosita/erass1/erass1_cluster_morphology_v1.0.fits", 1)
        ix = {u.strip(): i for i, u in enumerate(mo["DETUID"])}
        jj = np.array([ix[u.strip()] for u in p["DETUID"][m]])
        lc = mo["C_R500"][jj].astype(float)
        X = np.c_[X, lc]
    k = X.shape[1]

    def partes(q):
        me, md = X @ q[:k], X @ q[k:2 * k]
        se, sd = np.exp(Xs @ q[2 * k:2 * k + 2]), np.exp(Xs @ q[2 * k + 2:2 * k + 4]); r = np.tanh(q[-1])
        return me, md, se, sd, r

    def nll(q):
        me, md, se, sd, r = partes(q)
        a, b = (le - me) / se, (ld - md) / sd
        lp = -np.log(2 * np.pi * se * sd * np.sqrt(1 - r * r)) - (a * a - 2 * r * a * b + b * b) / (2 * (1 - r * r))
        return -(lp - lcola2((cut - me) / se, (cutd - md) / sd, r)).sum()

    q0 = np.r_[0, 1, np.zeros(k - 2), 1, 1, np.zeros(k - 2), np.log(.6), 0, np.log(.6), 0, np.arctanh(.86)]
    r = minimize(nll, q0, method="Powell", options=dict(maxiter=400000, xtol=1e-7, ftol=1e-10))
    r = minimize(nll, r.x, method="Nelder-Mead", options=dict(maxiter=400000, xatol=1e-7, fatol=1e-9))
    me, md, se, sd, rr = partes(r.x)
    pred = np.exp(lcola2((np.log(6) - me) / se, (cutd - md) / sd, rr) - lcola2((cut - me) / se, (cutd - md) / sd, rr))
    tir = casillas(pred)
    if conc:
        qq = np.quantile(lc, np.linspace(0, 1, 9))
        for i in range(8):
            b = (lc >= qq[i]) & (lc <= qq[i + 1]); pm = pred[b].mean()
            tir = np.r_[tir, (obs[b].mean() - pm) / np.sqrt(pm * (1 - pm) / b.sum())]
    nom = "conjunto_ext_det_C" if conc else "conjunto_ext_det"
    res["modelos"][nom] = dict(
        params=r.x.tolist(), rho=float(rr), menos_lnL=float(r.fun), convergio=bool(r.success),
        peor_sigma=float(np.abs(tir).max()), chi2_casillas=float((tir ** 2).sum()), n_casillas=len(tir),
        tirones=tir.tolist(), pasa=bool(np.abs(tir).max() < 2),
        criterio="ninguna casilla > 2 sigma binomiales (declarado antes, mismo que modelos 1-3)", n_libres=len(r.x))
    json.dump(res, open(OUT, "w"), indent=1)
    print(f"  {nom}  rho {rr:.3f}  peor {np.abs(tir).max():.1f} sigma  chi2 {np.sum(tir**2):.1f}/{len(tir)}"
          f"  -> {'PASA' if np.abs(tir).max() < 2 else 'NO PASA'}")
    sys.exit(0)

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
json.dump(res, open(OUT, "w"), indent=1)
