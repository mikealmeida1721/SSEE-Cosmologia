#!/usr/bin/env python3
"""erosita_conteos.py — conteos de cumulos eROSITA (eRASS1 y eFEDS) contra el clavo.

QUE SE COMPARA. Los mismos puntos crudos para los dos modelos: cuantos cumulos
hay en cada casilla de (redshift z, flujo F). Se usa el FLUJO, no la luminosidad
del catalogo: la L500 del catalogo ya viene calculada con una cosmologia LCDM de
referencia (L = 4 pi D_L^2 F). Aqui cada modelo convierte flujo en luminosidad
con SU propia distancia D_L.

  eRASS1 : catalogo primario v3.2, F500 en 0.2-2.3 keV, BEST_Z, 13116 deg^2
  eFEDS  : Liu+2022 V3.2, F_500kpc en 0.5-2 keV, z, 140 deg^2
  Corte  : 0.1 <= z <= 0.8 (el rango de la muestra cosmologica de eRASS1)
  No se suman: eFEDS cae dentro del cielo de eRASS1 (comparten cumulos).

MODELO (el mismo para los dos fondos). Cuentas esperadas en cada casilla:
  N = Omega_cielo * int dz dV/dz/dOmega * int dlog10M n(M,z)
        * int_casilla dlogF  Normal(logL | mu(M,z), sigma_int) * S(L,z)
  n(M,z)  : funcion de masa de Tinker+2008, M500c (CCL, pyccl, LSST-DESC),
            P(k) lineal de CAMB con PPF para w0-wa
  logL    = logF + log10(4 pi D_L^2)            (sin correccion K, igual en ambos)
  mu(M,z) = logA + B (log10 M - 14.5) + gamma log10 E(z)
  S(L,z)  : seleccion de Zhong+2026 (arXiv:2602.20483, ecs. 10-12), con
            F_lim leido de su .tex. OJO: el articulo escribe
            sigma_L = L_lim - L_q16 en erg/s dentro de un erf en dex; aplicada
            literal da S=0.5 para todo. Se usa sigma_L = log L_lim - log L_q16
            (dex), que es lo que dibuja su figura de seleccion (curvas del 10 %
            al 90 % separadas ~0.2 dex). L_q16: percentil 16 de log L de los
            cumulos con F < F_lim en cada casilla de z, con la D_L de cada modelo.
  Verosimilitud: Poisson; el «chi2» es la desviacion 2 sum[mu - n + n ln(n/mu)].

LIBRES.
  SSEE          : 4 nuisance de la relacion L-M (logA, B, gamma, sigma_int).
                  Fondo y A_s CLAVADOS (cero cosmologicos).
  LCDM-Planck   : los mismos 4 nuisance; cosmologia de Planck 2018 fija.
  LCDM libre    : los 4 nuisance + Omega_m y logA; h, omega_b, n_s, m_nu de
                  Planck. Es el calibrador: se REPORTA su distancia al resultado
                  oficial de Ghirardini+2024 (arXiv:2402.08458), leido de su
                  resumen, como DIAGNOSTICO --- su analisis calibra la masa con
                  lente debil y usa la funcion de seleccion oficial; este no.

Salida: results/logs/erosita_conteos.json
Uso: erosita_conteos.py [erass1|efeds]   (con el python de /mnt/datos/SSEE_data/erosita/venv)
"""
import html
import json
import math
import os
import re
import sys

import numpy as np
from scipy.optimize import minimize
from scipy.special import erf

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from lcdm_planck import AS_PLANCK, LCDM_PLANCK, LOGA_PLANCK  # noqa: E402

E = "/mnt/datos/SSEE_data/erosita"
OUT = os.path.join(_R, "results", "logs", "erosita_conteos.json")
MPC_CM = None                           # se llena desde astropy.units en main()
DEG2_SR = (math.pi / 180) ** 2
# ORIGEN-VALOR: 0.8001 — tope de arange para incluir el borde 0.8 (rango de la muestra cosmologica eRASS1)
Z_BORDES = np.round(np.arange(0.1, 0.8001, 0.1), 4)
LOGF_BORDES = np.arange(-14.0, -10.99, 0.25)
LOGM = np.linspace(13.0, 15.7, 55)


# ------------------------------------------------------------ lecturas de fuente
def _texto(ruta):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", open(ruta).read())))


def flujo_limite():
    t = open(f"{E}/paper_2602.20483/AA_final.tex").read()
    m = re.search(r"F_\{\\rm lim\} = (\d+) \\times 10\^\{(-\d+)\}", t)
    return float(m.group(1)) * 10.0 ** int(m.group(2))


def area_deg2(cual):
    if cual == "erass1":
        return float(re.search(r"in a (\d+) square degree region",
                               _texto(f"{E}/erass1cl_primary_v3.2.html")).group(1))
    return float(re.search(r"In the (\d+) deg\$\^2\$ area covered by eFEDS",
                           open(f"{E}/efeds/Liu2022_abstract.txt").read()).group(1))


def ghirardini():
    t = open(f"{E}/Ghirardini2024_abstract.txt").read()
    om = re.search(r"Omega_\{\\mathrm\{m\}\}=([\d.]+)\^\{\+([\d.]+)\}_\{-([\d.]+)\}", t)
    s8 = re.search(r"S_8=\\sigma_8.*?=([\d.]+)\\pm([\d.]+)", t)
    sg = re.search(r"sigma_8=([\d.]+)\\pm([\d.]+)", t)
    return dict(Om=float(om.group(1)), Om_mas=float(om.group(2)), Om_menos=float(om.group(3)),
                sigma8=float(sg.group(1)), sigma8_err=float(sg.group(2)),
                S8=float(s8.group(1)), S8_err=float(s8.group(2)), fuente="arXiv:2402.08458")


def datos(cual):
    from astropy.io import fits
    if cual == "erass1":
        d = fits.getdata(f"{E}/erass1/erass1cl_primary_v3.2.fits", 1)
        z, F = d["BEST_Z"].astype(float), d["F500"].astype(float) * 1e-14   # unidad 10**-14 (su doc)
    else:
        d = fits.getdata(f"{E}/efeds/eFEDS_clusters_V3.2.fits.gz", 1)
        z, F = d["z"].astype(float), d["F_500kpc"].astype(float)
    m = np.isfinite(z) & np.isfinite(F) & (F > 0) & (z >= Z_BORDES[0]) & (z <= Z_BORDES[-1])
    return z[m], F[m]


# ------------------------------------------------------------ cosmologias
def cosmologia(caso, Om=None, logA=None):
    import pyccl as ccl
    ext = {"camb": {"dark_energy_model": "ppf"}}
    if caso == "ssee":
        from ssee_core import (H0_GLOBAL, N_S, OMEGA_B_H2, OMEGA_C_H2,
                               SUM_MNU_EV, W0, WA)
        # ORIGEN: results/logs/cmb_dbic_tau_ajustado.json -> SSEE/mejor (el clavo del CMB)
        with open(os.path.join(_R, "results", "logs", "cmb_dbic_tau_ajustado.json")) as fh:
            la = json.load(fh)["SSEE"]["mejor"]["logA"]
        h = H0_GLOBAL / 100
        return ccl.Cosmology(Omega_c=OMEGA_C_H2 / h ** 2, Omega_b=OMEGA_B_H2 / h ** 2,
                             h=h, n_s=N_S, A_s=math.exp(la) * 1e-10, m_nu=SUM_MNU_EV,
                             mass_split="single", w0=W0, wa=WA,
                             transfer_function="boltzmann_camb",
                             matter_power_spectrum="linear", extra_parameters=ext)
    P = LCDM_PLANCK
    h = P["H0"] / 100
    ob = P["ombh2"] / h ** 2
    oc = P["omch2"] / h ** 2
    if Om is not None:                          # Omega_nu lo calcula CCL, no se teclea
        import pyccl as _c
        base = _c.Cosmology(Omega_c=oc, Omega_b=ob, h=h, n_s=P["ns"], A_s=AS_PLANCK,
                            m_nu=P["mnu"], mass_split="single")
        oc = Om - (base["Omega_m"] - oc)        # Omega_m - (Omega_b + Omega_nu)
    As = AS_PLANCK if logA is None else math.exp(logA) * 1e-10
    return ccl.Cosmology(Omega_c=oc, Omega_b=ob, h=h, n_s=P["ns"], A_s=As,
                         m_nu=P["mnu"], mass_split="single", w0=-1.0, wa=0.0,
                         transfer_function="boltzmann_camb",
                         matter_power_spectrum="linear", extra_parameters=ext)


# ------------------------------------------------------------ piezas fijas por cosmologia
class Tablas:
    """Todo lo que depende SOLO de la cosmologia; los nuisance no lo tocan."""
    def __init__(self, cosmo, z, F, area, flim):
        import pyccl as ccl
        self.nz = 4                                          # puntos de z por casilla
        zc = []
        for i in range(len(Z_BORDES) - 1):
            zc.append(np.linspace(Z_BORDES[i], Z_BORDES[i + 1], self.nz + 1)[:-1]
                      + (Z_BORDES[i + 1] - Z_BORDES[i]) / self.nz / 2)
        self.zg = np.array(zc)                               # (nzb, nz)
        a = 1 / (1 + self.zg.ravel())
        hmf = ccl.halos.MassFuncTinker08(mass_def=ccl.halos.MassDef500c)
        self.dndlogM = np.array([hmf(cosmo, 10 ** LOGM, ai) for ai in a]).reshape(
            self.zg.shape + (len(LOGM),))                    # Mpc^-3 por dex
        dV = ccl.comoving_volume_element(cosmo, a) * a ** 2  # Mpc^3/sr por unidad de z
        self.dVdz = dV.reshape(self.zg.shape)
        self.dz = (Z_BORDES[1] - Z_BORDES[0]) / self.nz
        self.logE = np.log10(ccl.h_over_h0(cosmo, a)).reshape(self.zg.shape)
        DL = ccl.luminosity_distance(cosmo, a) * MPC_CM
        self.logD = np.log10(4 * math.pi * DL ** 2).reshape(self.zg.shape)
        self.omega = area * DEG2_SR
        # seleccion de Zhong+2026 con la D_L de ESTA cosmologia
        self.loglim = math.log10(flim) + self.logD
        zb = np.digitize(z, Z_BORDES) - 1
        DLd = ccl.luminosity_distance(cosmo, 1 / (1 + z)) * MPC_CM
        logL = np.log10(F) + np.log10(4 * math.pi * DLd ** 2)
        self.sig = np.zeros(len(Z_BORDES) - 1)
        for i in range(len(Z_BORDES) - 1):
            sub = logL[(zb == i) & (F < flim)]
            lim_c = math.log10(flim) + np.log10(4 * math.pi * (ccl.luminosity_distance(
                cosmo, 1 / (1 + 0.5 * (Z_BORDES[i] + Z_BORDES[i + 1]))) * MPC_CM) ** 2)
            s = lim_c - np.percentile(sub, 16) if len(sub) >= 5 else 0.1
            self.sig[i] = max(s, 0.02)                      # piso: evita un escalon exacto
        # sub-rejilla de flujo dentro de cada casilla de F
        self.nf = 6
        self.lf = np.array([np.linspace(LOGF_BORDES[j], LOGF_BORDES[j + 1], self.nf + 1)[:-1]
                            + 0.25 / self.nf / 2 for j in range(len(LOGF_BORDES) - 1)])
        self.dlf = 0.25 / self.nf
        # conteos observados
        self.n = np.histogram2d(z, np.log10(F), bins=[Z_BORDES, LOGF_BORDES])[0]

    def esperado(self, th):
        logA, B, gam, sint = th
        # logL en cada (zbin, zsub, fbin, fsub)
        logL = self.lf[None, None, :, :] + self.logD[:, :, None, None]
        S = 0.5 * (1 - erf((self.loglim[:, :, None, None] - logL)
                           / (math.sqrt(2) * self.sig[:, None, None, None])))
        mu = logA + B * (LOGM - 14.5)[None, None, :] + gam * self.logE[:, :, None]   # (zb,zs,M)
        g = np.exp(-0.5 * ((logL[:, :, :, :, None] - mu[:, :, None, None, :]) / sint) ** 2) \
            / (math.sqrt(2 * math.pi) * sint)                                         # por dex de L
        dlogM = LOGM[1] - LOGM[0]
        integ = (g * self.dndlogM[:, :, None, None, :]).sum(-1) * dlogM              # (zb,zs,fb,fs)
        integ = (integ * S).sum(-1) * self.dlf                                        # (zb,zs,fb)
        N = (integ * self.dVdz[:, :, None]).sum(1) * self.dz * self.omega
        return N

    def desviacion(self, th):
        if th[3] <= 0.02 or th[3] > 2.0 or not (0.1 < th[1] < 4.0):
            return 1e12
        mu = np.maximum(self.esperado(th), 1e-30)
        n = self.n
        t = np.where(n > 0, n * np.log(np.where(n > 0, n, 1) / mu), 0.0)
        return float(2 * np.sum(mu - n + t))


def ajusta_nuisance(tab, x0=(43.8, 1.3, 2.0, 0.25)):
    mejor = None
    for arr in (x0, (43.5, 1.6, 1.0, 0.35), (44.1, 1.0, 3.0, 0.2)):
        r = minimize(tab.desviacion, arr, method="Nelder-Mead",
                     options=dict(maxiter=4000, xatol=1e-4, fatol=1e-4))
        r = minimize(tab.desviacion, r.x, method="Powell", options=dict(xtol=1e-4, ftol=1e-6))
        if mejor is None or r.fun < mejor.fun:
            mejor = r
    return mejor


def main():
    cual = sys.argv[1] if len(sys.argv) > 1 else "erass1"
    import pyccl as ccl
    from astropy import units as u
    global MPC_CM
    MPC_CM = float((1 * u.Mpc).to(u.cm).value)
    z, F = datos(cual)
    flim, area = flujo_limite(), area_deg2(cual)
    nb = (len(Z_BORDES) - 1) * (len(LOGF_BORDES) - 1)
    print(f"  {cual}: {len(z)} cumulos en 0.1<=z<=0.8, {area:.0f} deg2, "
          f"F_lim={flim:.1e}, {nb} casillas")
    res = dict(fecha="2026-09-27", muestra=cual, n_cumulos=int(len(z)), area_deg2=area,
               F_lim=flim, casillas=nb, z_bordes=Z_BORDES.tolist(),
               logF_bordes=LOGF_BORDES.tolist(), casos={})

    def caso(nombre, cosmo, libres_cosmo):
        tab = Tablas(cosmo, z, F, area, flim)
        r = ajusta_nuisance(tab)
        dof = nb - 4 - libres_cosmo
        from scipy import stats
        pte = float(stats.chi2.sf(r.fun, dof))
        s8 = ccl.sigma8(cosmo)
        om = cosmo["Omega_m"]
        d = dict(chi2=float(r.fun), dof=dof, PTE=pte, sigma_equivalente=float(stats.norm.isf(pte / 2)),
                 nuisance=dict(zip(["logA", "B", "gamma", "sigma_int"], map(float, r.x))),
                 Omega_m=float(om), sigma8=float(s8), S8=float(s8 * (om / 0.3) ** 0.5),
                 sigma_seleccion_dex=tab.sig.tolist(), n_obs=float(tab.n.sum()),
                 n_esp=float(tab.esperado(r.x).sum()))
        print(f"    {nombre:12s} chi2={r.fun:9.3f}  gl={dof}  PTE={pte:.4f} "
              f"({d['sigma_equivalente']:.2f} sigma)  Om={om:.4f} S8={d['S8']:.4f}  "
              f"N obs/esp={d['n_obs']:.0f}/{d['n_esp']:.1f}")
        return d, tab, r

    res["casos"]["ssee"], _, _ = caso("SSEE", cosmologia("ssee"), 0)
    res["casos"]["lcdm_planck"], _, _ = caso("LCDM-Planck", cosmologia("planck"), 0)

    # LCDM libre: perfil sobre (Omega_m, logA), nuisance minimizados dentro
    cache = {}

    def perfil(p):
        Om, la = p
        if not (0.1 < Om < 0.6 and 2.0 < la < 4.0):
            return 1e12
        k = (round(Om, 5), round(la, 5))
        if k not in cache:
            tab = Tablas(cosmologia("libre", Om, la), z, F, area, flim)
            cache[k] = ajusta_nuisance(tab).fun
        return cache[k]
    r = minimize(perfil, (cosmologia("planck")["Omega_m"], LOGA_PLANCK),
                 method="Nelder-Mead", options=dict(maxiter=120, xatol=2e-3, fatol=1e-2))
    d, _, _ = caso("LCDM libre", cosmologia("libre", *r.x), 2)
    g = ghirardini()
    d["vs_ghirardini"] = dict(g, dif_S8_sigma=(d["S8"] - g["S8"]) / g["S8_err"])
    res["casos"]["lcdm_libre"] = d
    print(f"    diagnostico: S8 LCDM libre {d['S8']:.4f} vs Ghirardini {g['S8']}±{g['S8_err']} "
          f"-> {d['vs_ghirardini']['dif_S8_sigma']:+.2f} sigma")
    c = res["casos"]
    res["delta_chi2_ssee_menos_lcdm_libre"] = c["ssee"]["chi2"] - c["lcdm_libre"]["chi2"]
    res["delta_BIC_ssee_menos_lcdm_libre"] = (c["ssee"]["chi2"] - c["lcdm_libre"]["chi2"]
                                             - 2 * math.log(nb))   # 2 libres mas en LCDM; N = casillas
    out = OUT.replace(".json", f"_{cual}.json")
    json.dump(res, open(out, "w"), indent=1, ensure_ascii=False)
    print(f"  -> {out}")


if __name__ == "__main__":
    main()
