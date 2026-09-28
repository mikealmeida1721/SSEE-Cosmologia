#!/usr/bin/env python3
"""act_dr6_calibra.py — calibrador ΛCDM de ACT DR6 lensing: ¿reproducimos lo publicado?

QUÉ PREGUNTA. Antes de leer el χ² de SSEE en ACT (act_dr6_lensing.py) hay que
saber si NUESTRO montaje de la verosimilitud oficial reproduce el resultado de
la colaboración. ACT DR6 solo lente publica (Qu+2024, arXiv:2304.05202):
    S8^CMBL ≡ σ8 (Ωm/0.3)^0.25 = 0.818 ± 0.022.
Se corre ΛCDM con SUS priors (Madhavacheril+2024, arXiv:2304.05203, tabla de
priors, bloque «Lensing + BAO» sin BAO) y se compara.

TODO SE LEE DE LA FUENTE: el blanco, del resumen de 2304.05202; los priors, de
priors.tex de 2304.05203; nada tecleado.

MONTAJE, igual que el paper:
  - act_dr6_lenslike, variante act_baseline, lens_only=True (lente sola).
  - libres: ω_c [uniforme], ω_b N(μ,σ), logA [uniforme], n_s N(μ,σ),
    100θ_MC [uniforme]; se rechaza H0 fuera de [hmin, hmax].
  - Σmν = 0.06 eV, un autoestado masivo (sec. 2 de 2304.05203).
  - τ NO se muestrea en lente sola (no está en el bloque); se fija en el de
    Planck 2018 (lcdm_planck.py). El espectro de lente no depende de τ.

CRITERIO, declarado antes de correr:
  |media − 0.818| < 0.25 σ_publicada  y  |σ − 0.022| / 0.022 < 15 %,
  con la cadena convergida (Gelman-Rubin R−1 < 0.02).

Uso:  mpirun -n 4 .venv/bin/python3 src/p11_sondas/act_dr6_calibra.py corre
      .venv/bin/python3 src/p11_sondas/act_dr6_calibra.py lee
Salida: results/logs/act_dr6_calibrador.json · cadenas en el HDD.
"""
import glob
import json
import os
import re
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from lcdm_planck import TAU_PLANCK  # noqa: E402

PAP = "/mnt/datos/SSEE_data/cmb_lensing/papers"
CAD = "/mnt/datos/SSEE_data/cmb_lensing/act_dr6_calibrador"
OUT = os.path.join(_R, "results", "logs", "act_dr6_calibrador.json")
MNU = 0.06   # ORIGEN: 2304.05203 L249, «fix the sum of neutrino masses ... 0.06 eV (one massive)»


def blanco():
    t = open(f"{PAP}/2304.05202/main.tex").read()
    m = re.search(r"S\^\{\\mathrm\{CMBL\}\}_8=\s*([0-9.]+)\\pm([0-9.]+)\$ from ACT DR6 CMB lensing alone", t)
    return float(m.group(1)), float(m.group(2))


def priors():
    t = open(f"{PAP}/2304.05203/priors.tex").read()
    return {k: float(v) for k, v in re.findall(r"\\newcommand\{\s*\\(\w+)\s*\}\s*\{\s*([-0-9.]+)\s*\}", t)}


def info():
    p = priors()
    return {
        'packages_path': os.environ.get('COBAYA_PACKAGES_PATH', os.path.expanduser('~/cobaya_packages')),
        'likelihood': {'act_dr6_lenslike.ACTDR6LensLike': {
            'lens_only': True, 'variant': 'act_baseline', 'lmax': 4000, 'stop_at_error': True}},
        'theory': {'camb': {'extra_args': {
            'halofit_version': 'mead', 'WantTensors': False, 'lens_potential_accuracy': 4,
            'num_massive_neutrinos': 1}}},
        'params': {
            'omch2': {'prior': {'min': p['omchmin'], 'max': p['omchmax']}, 'ref': 0.12, 'proposal': 0.005},
            'ombh2': {'prior': {'dist': 'norm', 'loc': p['obmean'], 'scale': p['obsigma']},
                      'ref': p['obmean'], 'proposal': p['obsigma']},
            'logA': {'prior': {'min': p['logamin'], 'max': p['logamax']}, 'ref': 3.05, 'proposal': 0.05,
                     'drop': True},
            'As': {'value': 'lambda logA: 1e-10*np.exp(logA)'},
            'ns': {'prior': {'dist': 'norm', 'loc': p['nsmean'], 'scale': p['nssigma']},
                   'ref': p['nsmean'], 'proposal': 0.01},
            'theta_MC_100': {'prior': {'min': p['thetamin'], 'max': p['thetamax']}, 'ref': 1.0411,
                             'proposal': 0.002, 'drop': True},
            'cosmomc_theta': {'value': 'lambda theta_MC_100: 1.e-2*theta_MC_100', 'derived': False},
            'H0': {'min': p['hmin'], 'max': p['hmax']},
            'tau': TAU_PLANCK, 'mnu': MNU,
            'omegam': None, 'sigma8': None,
            'S8CMBL': {'derived': 'lambda sigma8, omegam: sigma8*(omegam/0.3)**0.25'},
        },
        'sampler': {'mcmc': {'Rminus1_stop': 0.02, 'Rminus1_cl_stop': 0.2, 'max_tries': 10000}},
        'output': f"{CAD}/act_lcdm",
        'resume': True,
    }


def lee():
    from getdist import loadMCSamples
    mu, sg = blanco()
    s = loadMCSamples(f"{CAD}/act_lcdm", settings={'ignore_rows': 0.3})
    m = float(s.mean('S8CMBL')); e = float(s.std('S8CMBL'))
    prog = np.loadtxt(f"{CAD}/act_lcdm.progress", ndmin=2)
    r1 = float(prog[-1, 3])
    pasa = bool(abs(m - mu) < 0.25 * sg and abs(e - sg) / sg < 0.15 and r1 < 0.02)
    res = dict(fecha="2026-09-28", sonda="ACT DR6 lensing, calibrador ΛCDM",
               blanco=dict(S8CMBL=mu, sigma=sg, fuente="arXiv:2304.05202, resumen"),
               priors=dict(fuente="arXiv:2304.05203 priors.tex", valores=priors()),
               nuestro=dict(S8CMBL=m, sigma=e, Rminus1=r1, filas=int(s.numrows)),
               tirones_sigma=(m - mu) / sg, razon_sigmas=e / sg,
               criterio="|dmedia| < 0.25 sigma; |dsigma|/sigma < 15 %; R-1 < 0.02 (declarado antes)",
               pasa=pasa)
    json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"  publicado S8CMBL = {mu} ± {sg}")
    print(f"  nuestro   S8CMBL = {m:.4f} ± {e:.4f}   tirón {(m-mu)/sg:+.2f}σ   R−1 {r1:.3f}")
    print(f"  -> {'PASA' if pasa else 'NO PASA'}   ({OUT})")
    return pasa


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "lee"
    if modo == "blanco":
        print(blanco(), priors())
    elif modo == "corre":
        os.makedirs(CAD, exist_ok=True)
        from cobaya.run import run
        run(info())
    else:
        sys.exit(0 if lee() else 1)
