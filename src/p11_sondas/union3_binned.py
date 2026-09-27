#!/usr/bin/env python3
"""union3_binned.py — Union3 (UNITY1.5) y Union3.1 (UNITY1.8) contra el fondo clavado.

QUE SE USA. El producto que la colaboracion publica para ajustes externos: las
distancias binadas mu(z_i) en 22 nodos con su covarianza completa (sistematicos
incluidos), que salen de ajustar las 2087/2085 SNe con UNITY. Es como Rubin et
al. 2023 hacen SU PROPIA cosmologia (arXiv:2311.12098, sec. «SN+External»: «The
frequentist spline-interpolated SN distances are also how we release our
distances to the community»).
  Union3   : mu_mat_union3_cosmo=2_mu.fits (release oficial; mu ABSOLUTO,
             bloque interior = covarianza INVERSA)
  Union3.1 : pipeline/data_release/union31_unity18_binned_mu/mu_mat.fits
             (mu = RESIDUO respecto de FlatLambdaCDM(H0=70, Om0=0.3); se suma
             ese fiducial, como indica su README; interior = INVERSA)

CALIBRADOR LCDM (R53, que reproduzca lo PUBLICADO). Antes de mirar SSEE se
ajusta LCDM plano a Union3 con el mismo procedimiento del articulo (offset libre
perfilado; intervalo donde chi2 sube 1) y tiene que devolver su Tabla de
constraints, fila «SNe», Flat LCDM:  chi2 = 24.0 (20 gl),  Om = 0.356 +0.028 -0.026.
Esos tres numeros se LEEN del .tex del articulo (fuente arXiv descargada en el
HDD), no se teclean. El articulo fija Omega_gamma h^2 = 2.4729e-5 y N_eff = 3.04;
aqui igual.

SSEE: CERO LIBRES COSMOLOGICOS. Fondo del nucleo (w0, wa, omegas, H0) por CAMB,
igual que sn_geometria.py. El unico nuisance es el offset en mu (M_B + H0), y se
marginaliza analiticamente (Goliath+2001), que para un offset gaussiano con prior
plano da el mismo chi2 que perfilarlo, que es lo que hace el articulo.

CONTROL DEL OTRO LADO: LCDM-Planck con el mismo montaje (si da igual que SSEE,
Union3 no discrimina el fondo).

Salida: results/logs/union3_en_el_clavo.json
"""
import json
import os
import re
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from sn_geometria import mu_teo  # noqa: E402

U3 = "/mnt/datos/SSEE_data/sn_ia/union3"
TEX = f"{U3}/paper/merged.tex"          # fuente arXiv:2311.12098 (e-print)
OUT = os.path.join(_R, "results", "logs", "union3_en_el_clavo.json")


def publicado():
    """Fila «SNe» del bloque Flat LCDM, leida del .tex del articulo."""
    t = open(TEX).read()
    blq = t[t.index(r"\multicolumn{8}{c}{Flat $\Lambda$CDM}"):]
    fila = re.search(r"\nSNe & ([\d.]+) \((\d+)\).*?\$([\d.]+)\^\{\+([\d.]+)\}_\{-([\d.]+)\}\$", blq)
    og = re.search(r"Omega_\{\\gamma\} h\^2 = ([\d.]+)\\times 10\^\{(-?\d+)\}", t)
    ne = re.search(r"N_\{\\mathrm\{eff\}\} = ([\d.]+)", t)
    mg = re.search(r"\(1 \+ ([\d.]+) \\, N_\{\\mathrm\{eff\}\}\)", t)
    return dict(chi2=float(fila.group(1)), dof=int(fila.group(2)),
                Om=float(fila.group(3)), mas=float(fila.group(4)),
                menos=float(fila.group(5)),
                ogh2=float(og.group(1)) * 10.0 ** int(og.group(2)),
                neff=float(ne.group(1)), mangano=float(mg.group(1)))


def carga(cual):
    from astropy.io import fits
    if cual == "Union3":
        m = fits.getdata(f"{U3}/mu_mat_union3_cosmo=2_mu.fits")
        return m[0, 1:], m[1:, 0], m[1:, 1:]
    from astropy.cosmology import FlatLambdaCDM
    m = fits.getdata(f"{U3}/pipeline/data_release/union31_unity18_binned_mu/mu_mat.fits")
    z = m[0, 1:]
    fid = FlatLambdaCDM(H0=70, Om0=0.3).distmod(z).value     # su README
    return z, m[1:, 0] + fid, m[1:, 1:]


def chi2_offset(mu, mth, Ci):
    """chi2 minimo sobre un offset constante (= marginalizado, prior plano)."""
    r = mu - mth
    u = np.ones_like(r)
    A, B, C = r @ Ci @ r, r @ Ci @ u, u @ Ci @ u
    return float(A - B * B / C)


def mu_lcdm(z, Om, ogh2, neff, mangano, h=0.7):
    """LCDM plano con radiacion como en el articulo. h solo entra por
    Omega_r (el offset absorbe H0)."""
    Or = (1 + mangano * neff) * ogh2 / h ** 2
    OL = 1 - Om - Or
    zz = np.linspace(0, z.max(), 20001)
    E = np.sqrt(Om * (1 + zz) ** 3 + Or * (1 + zz) ** 4 + OL)
    dc = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))])
    dl = (1 + z) * np.interp(z, zz, dc) * 299792.458 / (100 * h)
    return 5 * np.log10(dl) + 25


def calibra_lcdm(z, mu, Ci, pub):
    from scipy.optimize import brentq, minimize_scalar
    f = lambda Om: chi2_offset(mu, mu_lcdm(z, Om, pub["ogh2"], pub["neff"], pub["mangano"]), Ci)
    r = minimize_scalar(f, bounds=(0.05, 0.9), method="bounded",
                        options=dict(xatol=1e-7))
    om, c0 = r.x, r.fun
    hi = brentq(lambda x: f(x) - c0 - 1, om, 0.9)
    lo = brentq(lambda x: f(x) - c0 - 1, 0.05, om)
    return dict(Om=om, mas=hi - om, menos=om - lo, chi2=c0, dof=len(z) - 2)


def main():
    from scipy import stats
    from ssee_core import H0_GLOBAL, N_S, OMEGA_B_H2, OMEGA_C_H2, W0, WA
    ssee = dict(ombh2=OMEGA_B_H2, omch2=OMEGA_C_H2, H0=H0_GLOBAL, ns=N_S)
    # ORIGEN: Planck 2018 VI (arXiv:1807.06209), Tabla 2, TT,TE,EE+lowE+lensing
    lcdm = dict(ombh2=0.02237, omch2=0.1200, H0=67.36, ns=0.9649)

    pub = publicado()
    res = dict(fecha="2026-09-27",
               fuente_publicada="Rubin et al. 2023, arXiv:2311.12098, tabla de "
                                "constraints, Flat LCDM, fila SNe (leida de " + TEX + ")",
               publicado=pub, sondas={})

    # ---- CALIBRADOR: LCDM libre sobre Union3 debe devolver lo publicado
    z, mu, Ci = carga("Union3")
    cal = calibra_lcdm(z, mu, Ci, pub)
    sig = (cal["Om"] - pub["Om"]) / (pub["mas"] if cal["Om"] > pub["Om"] else pub["menos"])
    ok = bool(abs(cal["chi2"] - pub["chi2"]) < 0.1 and cal["dof"] == pub["dof"]
          and abs(cal["Om"] - pub["Om"]) < 0.002)
    print(f"  CALIBRADOR LCDM (Union3): Om = {cal['Om']:.4f} +{cal['mas']:.4f} "
          f"-{cal['menos']:.4f}   chi2 = {cal['chi2']:.3f} ({cal['dof']} gl)")
    print(f"     publicado            : Om = {pub['Om']:.3f} +{pub['mas']:.3f} "
          f"-{pub['menos']:.3f}   chi2 = {pub['chi2']:.1f} ({pub['dof']} gl)"
          f"   -> {'REPRODUCE' if ok else 'NO REPRODUCE'} ({sig:+.3f} sigma)")
    res["calibrador_lcdm_union3"] = dict(cal, sigma_vs_publicado=sig, reproduce=ok)
    if not ok:
        json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
        print("  -> el montaje NO reproduce lo publicado: se para aqui.")
        sys.exit(1)

    # ---- SSEE en el clavo (cero libres) y control LCDM-Planck
    for cual in ("Union3", "Union3.1"):
        z, mu, Ci = carga(cual)
        n = len(z); dof = n - 1                         # -1 por el offset
        c = chi2_offset(mu, mu_teo(z, z, ssee, W0, WA), Ci)
        ca = chi2_offset(mu, mu_teo(z, z, lcdm, -1.0, 0.0), Ci)
        pte = float(stats.chi2.sf(c, dof))
        # control interno: CAMB-LCDM contra el integrador propio con el Om de Planck
        om_p = (lcdm["ombh2"] + lcdm["omch2"]) / (lcdm["H0"] / 100) ** 2
        cprop = chi2_offset(mu, mu_lcdm(z, om_p, pub["ogh2"], pub["neff"], pub["mangano"], lcdm["H0"] / 100), Ci)
        print(f"\n  {cual}: {n} nodos, offset marginalizado, {dof} gl")
        print(f"    fondo SSEE        chi2 = {c:8.3f}   PTE = {pte:.4f}   "
              f"{stats.norm.isf(pte / 2):.2f} sigma")
        print(f"    CONTROL LCDM-Planck chi2 = {ca:8.3f}   diferencia {c - ca:+.3f}")
        print(f"    (CAMB vs integrador propio, LCDM-Planck: {ca:.3f} vs {cprop:.3f})")
        res["sondas"][cual] = dict(
            nodos=n, dof=dof, chi2=c, PTE=pte,
            sigma_equivalente=float(stats.norm.isf(pte / 2)),
            control_lcdm_planck=dict(chi2=ca, diferencia=c - ca,
                                     chi2_integrador_propio=cprop))
    json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"\n  -> {OUT}")


if __name__ == "__main__":
    main()
