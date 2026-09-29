#!/usr/bin/env python3
"""spt3g_calibra.py — calibrador ΛCDM de SPT-3G D1 lente κκ: ¿reproducimos lo publicado?

QUÉ PREGUNTA (R53). spt3g_kk.py da el χ² de SSEE contra SPT-3G D1 GMV. Falta el
control del otro lado: que NUESTRO montaje de la verosimilitud oficial reproduzca
el resultado de la colaboración. SPT-3G D1 lente sola publica (Omori, Wu et al.
2026, arXiv:2608.31136, sec8_summary.tex L7):
    σ8 Ωm^0.25 = 0.6046 ± 0.0096.

MONTAJE: la configuración OFICIAL de la colaboración, sin tocar nada:
  cobaya/SPT3G_D1_KK/base_lens/gmv.yaml (teoría CAMB, priors cosmo_base,
  verosimilitud GMV con sus 7 nuisances con prior y 7 fijos, y su muestreador).
  Solo se cambia la carpeta de salida (al HDD).

TODO SE LEE DE LA FUENTE: el blanco, del TeX del paper; la configuración, del yaml.

CRITERIO, declarado antes de correr (el mismo que ACT DR6):
  |media − 0.6046| < 0.25 σ_publicada  y  |σ − 0.0096| / 0.0096 < 15 %,
  con la cadena convergida según el propio criterio del yaml (R−1 < 0.01).

Uso:  mpirun -n 4 .venv/bin/python3 src/p11_sondas/spt3g_calibra.py corre
      .venv/bin/python3 src/p11_sondas/spt3g_calibra.py lee
Salida: results/logs/spt3g_calibrador.json · cadenas en el HDD.
"""
import json
import os
import re
import sys
from datetime import date

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PAP = "/mnt/datos/SSEE_data/cmb_lensing/papers/2608.31136"
YML = "/mnt/datos/SSEE_data/cmb_lensing/spt3g/cobaya/SPT3G_D1_KK/base_lens/gmv.yaml"
CAD = "/mnt/datos/SSEE_data/cmb_lensing/spt3g_calibrador"
OUT = os.path.join(_R, "results", "logs", "spt3g_calibrador.json")


def blanco():
    t = open(f"{PAP}/sec8_summary.tex").read()
    m = re.search(r"lensing measurement alone constrains the structure-growth parameter to "
                  r"\$\\sigma_8\\Omega_\{\\rm m\}\^\{0\.25\}=([0-9.]+)\\pm([0-9.]+)\$", t)
    return float(m.group(1)), float(m.group(2))


def info():
    os.environ.setdefault("DIR_CHAINS", CAD)
    from cobaya.yaml import yaml_load_file
    d = yaml_load_file(YML)
    d["output"] = f"{CAD}/spt_lcdm"
    d["resume"] = True
    return d


def rminus1():
    return float(open(f"{CAD}/spt_lcdm.progress").read().strip().split("\n")[-1].split()[3])


def lee():
    from getdist import loadMCSamples
    mu, sg = blanco()
    info_ = info()
    s = loadMCSamples(f"{CAD}/spt_lcdm", settings={"ignore_rows": 0.3})
    m = float(s.mean("s8omegamp25")); e = float(s.std("s8omegamp25"))
    r1 = rminus1(); rstop = info_["sampler"]["mcmc"]["Rminus1_stop"]
    pasa = bool(abs(m - mu) < 0.25 * sg and abs(e - sg) / sg < 0.15 and r1 < rstop)
    res = dict(fecha=str(date.today()), sonda="SPT-3G D1 lente κκ GMV, calibrador ΛCDM",
               blanco=dict(s8omegamp25=mu, sigma=sg, fuente="arXiv:2608.31136 sec8_summary.tex"),
               configuracion=YML,
               nuestro=dict(s8omegamp25=m, sigma=e, Rminus1=r1, filas=int(s.numrows)),
               tiron_sigma=(m - mu) / sg, razon_sigmas=e / sg,
               criterio=f"|dmedia| < 0.25 sigma; |dsigma|/sigma < 15 %; R-1 < {rstop} (declarado antes)",
               pasa=pasa)
    json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"  publicado σ8Ωm^0.25 = {mu} ± {sg}")
    print(f"  nuestro   σ8Ωm^0.25 = {m:.4f} ± {e:.4f}   tirón {(m-mu)/sg:+.2f}σ   R−1 {r1:.3f}")
    print(f"  -> {'PASA' if pasa else 'NO PASA'}   ({OUT})")
    return pasa


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "lee"
    if modo == "blanco":
        print(blanco())
    elif modo == "corre":
        os.makedirs(CAD, exist_ok=True)
        from cobaya.run import run
        run(info())
    else:
        sys.exit(0 if lee() else 1)
