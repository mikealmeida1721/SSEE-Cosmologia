#!/usr/bin/env python3
"""union3_repro_compara.py — ¿nuestra corrida de UNITY 1.8 reproduce el Union3.1 publicado?

La corrida (pipeline oficial rubind/union3, config
union31_unity18_published_binnedMu.yml, 2085 SNe desde los ajustes de curva de
luz, desciegada en linea de comandos) deja su mu_mat.fits en
/mnt/datos/SSEE_data/sn_ia/union3/runs/union31_repro/. Se compara con el
publicado (pipeline/data_release/union31_unity18_binned_mu/mu_mat.fits):

  1. nodo a nodo: (mu_nuestro - mu_publicado) / sigma_publicado
  2. chi2 de la diferencia con la covarianza publicada (el offset global no
     cuenta: se marginaliza, porque mu esta definido hasta una constante)
  3. razon de errores por nodo (sigma_nuestro / sigma_publicado)
  4. el chi2 de SSEE y de LCDM-Planck sobre NUESTRO producto, contra el que
     union3_binned.py obtuvo sobre el publicado

Criterio (declarado ANTES de ver la corrida): reproduce si ningun nodo se
aparta mas de 0.3 sigma, el chi2 de la diferencia es < 1 por cada 22 nodos
(es decir < 1 en total: dos muestreos MCMC del mismo posterior difieren por
ruido de Monte Carlo, no por sigma enteras) y los errores coinciden al 10 %.

Salida: results/logs/union3_repro_compara.json
"""
import json
import os
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from union3_binned import chi2_offset  # noqa: E402
from sn_geometria import mu_teo  # noqa: E402

U3 = "/mnt/datos/SSEE_data/sn_ia/union3"
PUB = f"{U3}/pipeline/data_release/union31_unity18_binned_mu/mu_mat.fits"
NUE = f"{U3}/runs/union31_repro/mu_mat.fits"
OUT = os.path.join(_R, "results", "logs", "union3_repro_compara.json")
PREVIO = os.path.join(_R, "results", "logs", "union3_en_el_clavo.json")


def lee(f):
    from astropy.io import fits
    from astropy.cosmology import FlatLambdaCDM
    m = fits.getdata(f)
    z = m[0, 1:]
    fid = FlatLambdaCDM(H0=70, Om0=0.3).distmod(z).value
    return z, m[1:, 0] + fid, m[1:, 1:]


def main():
    from ssee_core import H0_GLOBAL, N_S, OMEGA_B_H2, OMEGA_C_H2, W0, WA
    zp, mp, Cip = lee(PUB)
    zn, mn, Cin = lee(NUE)
    assert np.allclose(zp, zn), "los nodos de z no coinciden"
    sp = np.sqrt(np.diag(np.linalg.inv(Cip)))
    sn = np.sqrt(np.diag(np.linalg.inv(Cin)))
    d = mn - mp
    d0 = d - np.average(d, weights=1 / sp ** 2)      # sin el offset global
    tiron = d0 / sp
    c_dif = chi2_offset(mn, mp, Cip)
    razon = sn / sp
    ok = bool(np.abs(tiron).max() < 0.3 and c_dif < 1.0
              and np.abs(razon - 1).max() < 0.10)

    ssee = dict(ombh2=OMEGA_B_H2, omch2=OMEGA_C_H2, H0=H0_GLOBAL, ns=N_S)
    # ORIGEN: Planck 2018 VI (arXiv:1807.06209), Tabla 2, TT,TE,EE+lowE+lensing
    lcdm = dict(ombh2=0.02237, omch2=0.1200, H0=67.36, ns=0.9649)
    c_ssee = chi2_offset(mn, mu_teo(zn, zn, ssee, W0, WA), Cin)
    c_lcdm = chi2_offset(mn, mu_teo(zn, zn, lcdm, -1.0, 0.0), Cin)
    prev = json.load(open(PREVIO))["sondas"]["Union3.1"]

    print(f"  nodo a nodo: max |tiron| = {np.abs(tiron).max():.3f} sigma "
          f"(nodo z={zp[np.abs(tiron).argmax()]:.4f})")
    print(f"  chi2 de la diferencia (cov publicada) = {c_dif:.4f}")
    print(f"  razon de errores: {razon.min():.3f} .. {razon.max():.3f}")
    print(f"  -> {'REPRODUCE' if ok else 'NO REPRODUCE'} el Union3.1 publicado")
    print(f"  SSEE sobre nuestro producto: chi2 = {c_ssee:.3f} "
          f"(sobre el publicado {prev['chi2']:.3f})")
    print(f"  LCDM-Planck sobre el nuestro: chi2 = {c_lcdm:.3f} "
          f"(sobre el publicado {prev['control_lcdm_planck']['chi2']:.3f})")
    json.dump(dict(
        fecha="2026-09-27", publicado=PUB, nuestro=NUE,
        criterio="max|tiron|<0.3 sigma, chi2_dif<1, errores al 10% (declarado antes)",
        z=zp.tolist(), tiron_sigma=tiron.tolist(), razon_errores=razon.tolist(),
        chi2_diferencia=c_dif, reproduce=ok,
        ssee_chi2_nuestro=c_ssee, ssee_chi2_publicado=prev["chi2"],
        lcdm_planck_chi2_nuestro=c_lcdm,
        lcdm_planck_chi2_publicado=prev["control_lcdm_planck"]["chi2"]),
        open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
