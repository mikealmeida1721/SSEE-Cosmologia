"""
SSEE — CMB Unified Likelihood Evaluation via Cobaya
Scans H0 to find the minimum chi2_eff against the full Planck 2018 plik_lite TTTEEE + lowT + lowE.
Calculates Delta BIC correctly with k=2 for SSEE vs k=6 for LambdaCDM.
"""
# ORIGEN-VALOR: 0.0544 — tau de Planck 2018 TT,TE,EE+lowE (arXiv:1807.06209)

import numpy as np
import os
import time
from scipy.optimize import minimize_scalar

PACKAGES_PATH = os.environ.get("COBAYA_PACKAGES_PATH", os.path.expanduser("~/cobaya_packages"))

# ---------------------------------------------------------------------------
# SSEE constants (algebraically fixed)
# ---------------------------------------------------------------------------
import os as _reloc_os, sys as _reloc_sys  # reloc: anclar src/
_reloc_sys.path.insert(0, _reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__))))
from ssee_core import (
    PHI as phi, PI as pi, OMEGA as Omega, BETA as beta, KAL0,
    P_SC as P_sc, K_V as Kv, T_R as Tr, M_V as Mv,
    W0 as w0_ssee, WA as wa_ssee, OMEGA_DE as OmDE,
    AURA, MIRA,
    N_S as ns_ssee, SUM_MNU_EV as _MNU,
)

ombh2_ssee = 0.02237                # Planck 2018 prior (no algebraico)
# ns_ssee = 1 - phi^-7 = 0.96556 — importado de ssee_core
As_ssee    = np.exp(3.044) * 1e-10
tau_ssee   = 0.054
mnu_ssee   = _MNU                    # Σm_ν canónico del nucleo (C_ν=93.14 PDG)

# ΛCDM Planck 2018 best-fit (TT+TE+EE+lowE, Table 2)
H0_lcdm    = 67.36
ombh2_lcdm = 0.02237
omch2_lcdm = 0.1200
ns_lcdm    = 0.9649
As_lcdm    = np.exp(3.044) * 1e-10
tau_lcdm   = 0.0544
mnu_lcdm   = 0.06                    # baseline estándar Planck (mín. jerarquía normal)

def build_cobaya_info(H0, ombh2, omch2, w0, wa, As, ns, tau, mnu=0.06):
    """Build a Cobaya model info dict for fixed-parameter likelihood evaluation."""
    return {
        "packages_path": PACKAGES_PATH,
        "likelihood": {
            "planck_2018_highl_plik.TTTEEE_lite": None,
            "planck_2018_lowl.TT": None,
            "planck_2018_lowl.EE": None,
        },
        "theory": {
            "camb": {
                "extra_args": {
                    "dark_energy_model": "ppf",
                    "halofit_version": "mead",
                    "WantTensors": False,
                    "lens_potential_accuracy": 2,
                },
            }
        },
        "params": {
            "H0":     H0,
            "ombh2":  ombh2,
            "omch2":  omch2,
            "As":     As,
            "ns":     ns,
            "tau":    tau,
            "mnu":    mnu,
            "omk":    0.0,
            "w":      w0,
            "wa":     wa,
            "A_planck": 1.0,
        },
        "debug": False,
    }

def evaluate_model(H0, ombh2, omch2, w0, wa, As, ns, tau, mnu=0.06, quiet=False):
    from cobaya.model import get_model
    import logging

    # Suppress cobaya output during scan
    logging.getLogger('cobaya').setLevel(logging.ERROR)

    info = build_cobaya_info(H0, ombh2, omch2, w0, wa, As, ns, tau, mnu)
    model = get_model(info)

    loglikes, derived = model.loglikes({})
    total_loglike = sum(loglikes)
    chi2_eff = -2 * total_loglike

    if not quiet:
        like_names = list(info["likelihood"].keys())
        like_dict = dict(zip(like_names, loglikes))
        print(f"\n  Log-likelihoods at minimum:")
        for name, val in like_dict.items():
            short = name.split(".")[-1]
            print(f"    {short:30s}  logL = {val:10.3f}  chi2_eff = {-2*val:.3f}")
        print(f"  {'TOTAL':30s}  logL = {total_loglike:10.3f}  chi2_eff = {chi2_eff:.3f}")

    return chi2_eff

# 2026-10-03: get_ssee_chi2() y main() se retiran. Barrian H0 con
# Omega_m,CMB = MIRA x s_m = 0.31983, una densidad construida desde s_m = 1+w0,
# que es un numero de la ecuacion de estado (factor materia retirado el
# 2026-06-18; el 0.160 no es densidad, 2026-07-30). Su ΔBIC −32.2 era ese escenario.
# Este archivo queda como BIBLIOTECA (evaluate_model y los parametros LCDM/SSEE),
# que usa scan_omega_m.py. El ΔBIC canonico de plik_lite es −26.03
# (results/logs/cmb_dbic_mnu_propia.json).


if __name__ == "__main__":
    raise SystemExit("ssee_paper3_cobaya_unified.py es una biblioteca: su barrido "
                     "MIRA x s_m quedo retirado el 2026-10-03 (ver comentario).")
