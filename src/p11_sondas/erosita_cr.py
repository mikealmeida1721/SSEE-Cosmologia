#!/usr/bin/env python3
"""erosita_cr.py — conteos de cumulos eRASS1 contra el clavo, con seleccion PROPIA.

POR QUE ESTE Y NO erosita_conteos.py (2026-09-27, plan de M. Almeida)
El montaje anterior dio chi2 ~3550/80 para los dos fondos. Causas encontradas:
  1. catalogo equivocado: el primario (12247, ~11 % contaminantes en 0.1-0.8)
     en vez de la muestra de COSMOLOGIA (5259, pureza 94 %, Ghirardini+2024);
  2. seleccion en flujo con F50 = 5e-14 (Zhong+2026). Medido contra eFEDS, la
     muestra de cosmologia llega al 50 % a 2.46e-13 en el campo eFEDS
     (erosita_completitud.py), y la deteccion depende de los FOTONES reunidos,
     que varian x10 sobre el cielo con la exposicion;
  3. relacion L-M libre sin calibrar masa: los conteos solos no separan «mas
     masa» de «universo mas grumoso» y la cosmologia se escapa.
La seleccion oficial (Clerc+2024) NO es publica; aqui se mide una propia.

MODELO
  N(z, CR) = A_cielo int dz dV/dz/dOmega int dlnM n(M,z)
                 int_casilla dlnCR  Normal(lnCR | mu(M,z), sigma_X)  Cbar(CR)
  n(M,z)  Tinker+2008, M500c, CCL con CAMB-PPF (el mismo de erosita_conteos).
  mu      relacion CR-M de Ghirardini+2024 (su ec. de escala, log natural):
            ln(CR/0.1) = ln A_X + b_X(z) ln(M/2e14 Msun) - 2 ln(dL/dL_p)
                         + 2 ln(E/E_p) + G_X ln((1+z)/(1+z_p)),
            b_X = B_X + F_X ln((1+z)/(1+z_p)),  z_p = 0.35.
          G_X lleva la correccion K (su texto). dL y E son los de CADA modelo.
  Cbar    completitud promedio del cielo: C(nu) en fotones nu = CR * T, con
          C(nu) = 1/2 erfc((log nu50 - log nu)/(sqrt2 ancho)); nu50 sale de la
          medida contra eFEDS (F50 * razon de apertura / conversion F-CR * T
          en el campo eFEDS), TODO leido de logs o medido aqui; la exposicion
          T sobre el footprint = ley de barrido T0/cos(beta) (T0 medido con el
          catalogo primario) por la dispersion empirica EXP/ley, sobre las
          celdas HEALPix (nside 16) con cumulos de la muestra de cosmologia.
  Previos: A_X, B_X, F_X, G_X, sigma_X gaussianos con la tabla de ajuste de
  Ghirardini+2024 (leida de su .tex; error = media de los asimetricos). Se
  pierden sus correlaciones (la tabla no las da): DECLARADO.
  Estadistico: desviacion de Poisson (el «chi2» de los datos) + penalizacion
  de previos, reportadas por separado.

LIBRES
  SSEE         5 nuisance de la relacion. Fondo y A_s clavados.
  LCDM-Planck  los mismos 5; cosmologia Planck 2018 (lcdm_planck.py).
  LCDM libre   5 + (Omega_m, logA) en rejilla; es el CALIBRADOR contra el
               S8 = 0.86 +- 0.01 de Ghirardini+2024. Criterio declarado ANTES:
               |S8_nuestro - 0.86| < 2 sigma_nuestro, con sigma_nuestro del
               perfil (Delta = 1). Circularidad parcial declarada: la relacion
               CR-M se ajusto junto con SU cosmologia LCDM.
NO modela: contaminacion (~6 %), variacion de N_H y fondo sobre el cielo,
dispersion del z fotometrico. Se declaran.
Salida: results/logs/erosita_cr.json
Uso: /mnt/datos/SSEE_data/erosita/venv/bin/python src/p11_sondas/erosita_cr.py
"""
import json
import math
import os
import re
import sys

import numpy as np
from scipy.optimize import minimize
from scipy.special import erfc

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
import erosita_conteos as EC  # noqa: E402  (cosmologias y lectura de Ghirardini)

E = "/mnt/datos/SSEE_data/erosita"
TEX_G = f"{E}/paper_ghirardini2024/48852corr.tex"
LOGS = os.path.join(_R, "results", "logs")
OUT = os.path.join(LOGS, "erosita_cr.json")
Z_BORDES = np.round(np.arange(0.1, 0.8001, 0.1), 4)   # ORIGEN-VALOR: 0.1-0.8 — rango de la muestra de cosmologia (Ghirardini+2024 sec. 2)
LCR_BORDES = np.arange(-2.0, 1.5001, 0.25)              # ORIGEN-VALOR: 1.5001 — tope de arange para que 1.5 entre; casillas en log10 CR, cubren el 99 % de la muestra
LNM = np.linspace(np.log(5e12), np.log(5e15), 70)       # ORIGEN-VALOR: 5e12-5e15 Msun — rango de integracion de Ghirardini+2024 (su sec. 4)
NSUB = 6                                                # ORIGEN-VALOR: 6 — subpuntos de integracion por casilla


# ── lecturas de fuente ──────────────────────────────────────────────────────
def tabla_ghirardini():
    t = open(TEX_G).read()
    out = {}
    for p in ("A", "B", "F", "G"):
        m = re.search(r"\$" + p + r"_\{X\}\$ & \$([-\d.]+)(?:\^\{\+([\d.]+)\}_\{-([\d.]+)\}|\\pm ([\d.]+))\$", t)
        v = float(m.group(1))
        s = float(m.group(4)) if m.group(4) else 0.5 * (float(m.group(2)) + float(m.group(3)))
        out[p] = (v, s)
    m = re.search(r"\$\\sigma_\{X\}\$ & \$([\d.]+)\^\{\+([\d.]+)\}_\{-([\d.]+)\}\$", t)
    out["sig"] = (float(m.group(1)), 0.5 * (float(m.group(2)) + float(m.group(3))))
    piv = re.search(r"C_\{R,p\} = ([\d.]+)\$?\s*cts.*?M_p = (\d+) \\times 10 \^\{(\d+)\}.*?z_p = ([\d.]+)", t, re.S)
    out["CRp"], out["Mp"], out["zp"] = float(piv.group(1)), float(piv.group(2)) * 10 ** int(piv.group(3)), float(piv.group(4))
    out["area"] = float(re.search(r"over an area of (\d+)~deg", t).group(1))
    return out


def datos():
    from astropy.io import fits
    c = fits.getdata(f"{E}/erass1/erass1cl_cosmology_v1.1.fits", 1)
    z, cr = c["Z_LAMBDA"].astype(float), c["CR500_NH0"].astype(float)
    m = np.isfinite(z) & np.isfinite(cr) & (cr > 0) & (z >= Z_BORDES[0]) & (z <= Z_BORDES[-1])
    return z[m], cr[m], c[m]


# ── la seleccion propia, promedio del cielo ─────────────────────────────────
def seleccion():
    """Cbar(CR) en una rejilla de log10 CR. No depende de la cosmologia."""
    import healpy as hp
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    from astropy.io import fits
    comp = json.load(open(os.path.join(LOGS, "erosita_completitud.json")))
    F50, ancho = comp["F50"], comp["radios"]["1.5"]["ancho_dex"]
    p = fits.getdata(f"{E}/erass1/erass1cl_primary_v3.2.fits", 1)
    c = fits.getdata(f"{E}/erass1/erass1cl_cosmology_v1.1.fits", 1)
    f = fits.getdata(f"{E}/efeds/eFEDS_clusters_V3.2.fits.gz", 1)
    # conversion F(0.5-2) -> CR500_NH0, medida con la muestra de cosmologia
    ip = {d: k for k, d in enumerate(p["DETUID"])}
    jj = np.array([ip.get(d, -1) for d in c["DETUID"]])
    ok = jj >= 0
    r = p["F500_0520"][jj[ok]] * 1e-14 / c["CR500_NH0"][ok]
    FporCR = float(np.median(r[np.isfinite(r) & (r > 0)]))
    # razon de apertura eRASS1(R500)/eFEDS(500 kpc) y exposicion en el campo eFEDS
    cf = SkyCoord(f["RA"] * u.deg, f["DEC"] * u.deg)
    cp = SkyCoord(p["RA"] * u.deg, p["DEC"] * u.deg)
    i, sep, _ = cf.match_to_catalog_sky(cp)
    dz = np.abs(p["BEST_Z"][i] - f["z"]) / (1 + f["z"])
    mm = (sep.arcmin < 1.5) & (dz < 0.1) & (f["F_500kpc"] > 0)
    apert = float(np.median(p["F500_0520"][i[mm]] * 1e-14 / f["F_500kpc"][mm]))
    T_efeds = float(np.median(p["EXP"][i[mm]]))
    nu50 = F50 * apert / FporCR * T_efeds
    # ley de barrido: T = T0 / cos(beta), T0 = mediana de EXP*cos(beta) con |beta|<10
    beta = np.abs(cp.barycentrictrueecliptic.lat.deg)
    ley = p["EXP"] * np.cos(np.radians(beta))
    T0 = float(np.median(ley[beta < 10]))
    fac = (p["EXP"] / (T0 / np.cos(np.radians(np.minimum(beta, 85.0)))))
    fac = fac[np.isfinite(fac) & (fac > 0)]
    # footprint: celdas nside 16 con cumulos de la muestra de cosmologia
    nside = 16
    pix = np.unique(hp.ang2pix(nside, c["RA"], c["DEC"], lonlat=True))
    lon, lat = hp.pix2ang(nside, pix, lonlat=True)
    bpix = np.abs(SkyCoord(lon * u.deg, lat * u.deg).barycentrictrueecliptic.lat.deg)
    Tcel = T0 / np.cos(np.radians(np.minimum(bpix, 85.0)))
    q = np.percentile(fac, np.linspace(2.5, 97.5, 20))        # dispersion empirica
    lcr = np.linspace(-3.0, 2.0, 501)
    C = np.zeros_like(lcr)
    for T in Tcel:
        nu = 10 ** lcr[:, None] * T * q[None, :]
        C += (0.5 * erfc((np.log10(nu50) - np.log10(nu)) / (math.sqrt(2) * ancho))).mean(1)
    C /= len(Tcel)
    info = dict(F50_efeds=F50, ancho_dex=ancho, F_por_CR=FporCR, apertura=apert,
                T_efeds=T_efeds, nu50_fotones=nu50, T0=T0, celdas=int(len(pix)),
                area_celdas=float(len(pix) * hp.nside2pixarea(nside, degrees=True)))
    return lcr, C, info


# ── piezas por cosmologia ───────────────────────────────────────────────────
class Modelo:
    def __init__(self, cosmo, zobs, crobs, sel, G, area):
        import pyccl as ccl
        lcr_s, C_s = sel
        zs = []
        for i in range(len(Z_BORDES) - 1):
            zs.append(np.linspace(Z_BORDES[i], Z_BORDES[i + 1], NSUB + 1)[:-1]
                      + (Z_BORDES[i + 1] - Z_BORDES[i]) / NSUB / 2)
        self.zg = np.array(zs)
        a = 1 / (1 + self.zg.ravel())
        hmf = ccl.halos.MassFuncTinker08(mass_def=ccl.halos.MassDef500c)
        M = np.exp(LNM)
        dndlog10M = np.array([hmf(cosmo, M, ai) for ai in a])            # Mpc^-3 por dex
        self.dndlnM = (dndlog10M / np.log(10)).reshape(self.zg.shape + (len(LNM),))
        self.dVdz = (ccl.comoving_volume_element(cosmo, a) * a ** 2).reshape(self.zg.shape)
        self.dz = (Z_BORDES[1] - Z_BORDES[0]) / NSUB
        zp = G["zp"]
        ap = 1 / (1 + zp)
        self.ldL = np.log(ccl.luminosity_distance(cosmo, a) / ccl.luminosity_distance(cosmo, ap)).reshape(self.zg.shape)
        self.lE = np.log(ccl.h_over_h0(cosmo, a) / ccl.h_over_h0(cosmo, ap)).reshape(self.zg.shape)
        self.l1z = np.log((1 + self.zg) / (1 + zp))
        self.lnMM = LNM - math.log(G["Mp"])
        self.lnCRp = math.log(G["CRp"])
        # sub-rejilla de CR por casilla y la seleccion en ella
        self.lcr = np.array([np.linspace(LCR_BORDES[j], LCR_BORDES[j + 1], NSUB + 1)[:-1]
                             + 0.25 / NSUB / 2 for j in range(len(LCR_BORDES) - 1)])
        self.dlncr = 0.25 / NSUB * np.log(10)
        self.S = np.interp(self.lcr, lcr_s, C_s)
        self.omega = area * EC.DEG2_SR
        self.n = np.histogram2d(zobs, np.log10(crobs), bins=[Z_BORDES, LCR_BORDES])[0]

    def esperado(self, th):
        lnA, B, F, Gx, sig = th
        bX = B + F * self.l1z                                            # (zb, zs)
        mu = (self.lnCRp + lnA + bX[..., None] * self.lnMM[None, None, :]
              - 2 * self.ldL[..., None] + 2 * self.lE[..., None] + Gx * self.l1z[..., None])
        x = self.lcr * np.log(10)                                        # (cb, cs) en ln
        g = np.exp(-0.5 * ((x[None, None, :, :, None] - mu[:, :, None, None, :]) / sig) ** 2) \
            / (math.sqrt(2 * math.pi) * sig)
        dlnM = LNM[1] - LNM[0]
        integ = (g * self.dndlnM[:, :, None, None, :]).sum(-1) * dlnM    # (zb,zs,cb,cs)
        integ = (integ * self.S[None, None]).sum(-1) * self.dlncr         # (zb,zs,cb)
        return (integ * self.dVdz[:, :, None]).sum(1) * self.dz * self.omega

    def desviacion(self, th):
        mu = np.maximum(self.esperado(th), 1e-30)
        n = self.n
        t = np.where(n > 0, n * np.log(np.where(n > 0, n, 1) / mu), 0.0)
        return float(2 * np.sum(mu - n + t))


def previos(G):
    c = np.array([math.log(G["A"][0]), G["B"][0], G["F"][0], G["G"][0], G["sig"][0]])
    s = np.array([G["A"][1] / G["A"][0], G["B"][1], G["F"][1], G["G"][1], G["sig"][1]])
    return c, s


def ajusta(mod, G, x0=None):
    c, s = previos(G)

    def obj(th):
        if th[4] <= 0.05:
            return 1e12
        return mod.desviacion(th) + float((((th - c) / s) ** 2).sum())
    best = None
    for k in range(3):                                   # tres arranques
        x = (c if x0 is None else x0) + (0 if k == 0 else np.random.default_rng(k).normal(0, 1, 5) * s)
        r = minimize(obj, x, method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-6, maxiter=4000))
        if best is None or r.fun < best.fun:
            best = r
    th = best.x
    dev = mod.desviacion(th)
    return dict(total=float(best.fun), desviacion=dev, previo=float(best.fun - dev),
                nuisance=dict(zip(["lnA_X", "B_X", "F_X", "G_X", "sigma_X"], map(float, th))),
                tirones_previo=dict(zip(["A_X", "B_X", "F_X", "G_X", "sigma_X"],
                                        map(float, (th - c) / s))),
                n_obs=float(mod.n.sum()), n_esp=float(mod.esperado(th).sum()), x=th)


def main():
    from scipy.stats import chi2 as chi2d, norm
    G = tabla_ghirardini()
    z, cr, _ = datos()
    lcr, C, info = seleccion()
    print(f"  seleccion: nu50 = {info['nu50_fotones']:.1f} fotones, T0 = {info['T0']:.1f} s, "
          f"footprint {info['area_celdas']:.0f} deg2 en celdas (publicado {G['area']:.0f})")
    gh = EC.ghirardini()
    nb = (len(Z_BORDES) - 1) * (len(LCR_BORDES) - 1)
    res = dict(fecha="2026-09-27", n_cumulos=int(len(z)), area_deg2=G["area"],
               seleccion=info, previos_ghirardini={k: G[k] for k in ("A", "B", "F", "G", "sig")},
               casillas=nb, ghirardini=gh, casos={})

    def caso(nombre, cosmo, libres):
        mod = Modelo(cosmo, z, cr, (lcr, C), G, G["area"])
        r = ajusta(mod, G)
        gl = nb - libres
        pte = float(chi2d.sf(r["desviacion"], gl))
        r.update(gl=gl, PTE=pte, sigma=float(norm.isf(pte / 2)) if pte > 0 else float("inf"),
                 Omega_m=float(cosmo["Omega_m"]), sigma8=float(__import__("pyccl").sigma8(cosmo)))
        r["S8"] = r["sigma8"] * math.sqrt(r["Omega_m"] / 0.3)
        r.pop("x")
        res["casos"][nombre] = r
        print(f"  {nombre:12s} desviacion {r['desviacion']:8.2f}  previo {r['previo']:6.2f}  gl {gl}  "
              f"PTE {pte:.4f}  N obs/esp {r['n_obs']:.0f}/{r['n_esp']:.1f}  S8 {r['S8']:.4f}", flush=True)
        return r

    caso("ssee", EC.cosmologia("ssee"), 0)
    caso("lcdm_planck", EC.cosmologia("lcdm_planck"), 0)
    # LCDM libre: rejilla (Omega_m, logA), nuisance minimizados en cada nodo
    oms = np.linspace(0.20, 0.44, 9)                 # ORIGEN-VALOR: rejilla de busqueda del calibrador
    las = np.linspace(2.70, 3.40, 9)                 # ORIGEN-VALOR: rejilla de busqueda del calibrador
    rej = []
    for om in oms:
        for la in las:
            cos = EC.cosmologia("lcdm_libre", Om=float(om), logA=float(la))
            mod = Modelo(cos, z, cr, (lcr, C), G, G["area"])
            r = ajusta(mod, G)
            s8 = float(__import__("pyccl").sigma8(cos)) * math.sqrt(om / 0.3)
            rej.append(dict(Om=float(om), logA=float(la), S8=s8, total=r["total"],
                            desviacion=r["desviacion"]))
            print(f"    Om {om:.3f} logA {la:.3f} S8 {s8:.3f}  total {r['total']:9.2f}", flush=True)
    tot = np.array([x["total"] for x in rej])
    k = int(tot.argmin())
    s8s = np.array([x["S8"] for x in rej])
    dentro = tot - tot.min() <= 1.0
    lo, hi = float(s8s[dentro].min()), float(s8s[dentro].max())
    borde = rej[k]["Om"] in (oms[0], oms[-1]) or rej[k]["logA"] in (las[0], las[-1])
    sig_nuestro = max(0.5 * (hi - lo), 1e-3)
    pasa = abs(rej[k]["S8"] - gh["S8"]) < 2 * sig_nuestro and not borde
    res["lcdm_libre"] = dict(rejilla=rej, mejor=rej[k], S8_banda_1sigma=[lo, hi],
                             sigma_S8=sig_nuestro, en_borde=bool(borde),
                             calibrador_pasa=bool(pasa),
                             criterio="|S8-0.86|<2 sigma_nuestro y minimo fuera del borde (declarado antes)")
    print(f"  CALIBRADOR LCDM libre: S8 = {rej[k]['S8']:.3f} [{lo:.3f}, {hi:.3f}] vs Ghirardini "
          f"{gh['S8']}±{gh['S8_err']}  borde={borde}  -> {'PASA' if pasa else 'NO PASA'}")
    for nom in ("ssee", "lcdm_planck"):
        d = res["casos"][nom]["total"] - rej[k]["total"]
        res["casos"][nom]["delta_total_vs_lcdm_libre"] = d
        print(f"  {nom}: total - LCDM libre = {d:+.2f}")
    json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False, default=float)
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
