#!/usr/bin/env python3
"""
Robustness check (Mike, 2026-06-14): rerun REAL de CPL anclando el prior de H0
en varios valores, para responder con MUESTREO DIRECTO (sin el problema de ESS
de la reponderación) a qué H0 lleva el ajuste libre w0,wa hacia la predicción
algebraica de SSEE (-0.840, -0.670), y si ese H0 es SH0ES (73) o no.

Es la versión rigurosa del notebook lab_w0wa_degeneracy.ipynb (que solo reponderaba).
Corre CPL (5 params) con el prior de H0 centrado en cada ancla; el resto del
likelihood (DESI BAO + Planck Om/Obh2 + priors w0,wa) es idéntico a
ssee_paper2_mcmc.py.
"""
# ORIGEN-VALOR: 0.1432 — pivote omega_m h^2 de la eq. rd de Paper 2 (Planck 2018 TT,TE,EE+lowE); cita EH98 en FUENTES_PENDIENTES.md FP-7
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import emcee
from ssee_core import KAL0

C_KM = 2.998e5

# ── DESI DR2 (copiado de ssee_paper2_mcmc.py) ──
# ── DESI DR2 (2503.14738 Tabla 4) — FUENTE ÚNICA data/raw/desi_dr2_bao.csv ──
# NO hardcodear (drift DR1/DR2 corregido 2026-07-02; guardián R14).
import os as _dd_os, sys as _dd_sys
_dd_sys.path.insert(0, _dd_os.path.join(_dd_os.path.dirname(_dd_os.path.dirname(
    _dd_os.path.abspath(__file__)))))
from desi_dr2_data import load_desi_dr2 as _dd_load, desi_covariance as _dd_cov
_DESI_D      = _dd_load()
DESI_Z       = list(_DESI_D["z"])
_DD_QSHORT   = {"DM_over_rd": "DM_rd", "DH_over_rd": "DH_rd", "DV_over_rd": "DV_rd"}
DESI_TYPE    = [_DD_QSHORT[q] for q in _DESI_D["quantity"]]
DESI_OBS     = _DESI_D["value"]
DESI_SIGMA   = _DESI_D["sigma"]
DESI_COV     = _dd_cov(_DESI_D)          # bloque-diagonal, r_MH oficiales DR2
DESI_COV_INV = np.linalg.inv(DESI_COV)

# ── Prior Planck Om/Obh2 (la parte de H0 se ANCLA por escenario) ──
PLANCK_OM, PLANCK_OBH2 = (0.3153,0.0073), (0.02237,0.00015)
SIGMA_H0 = 0.54

def f_de_cpl(z,w0,wa):
    a=1.0/(1.0+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
def E_cpl(z,Om,w0,wa):
    return np.sqrt(Om*(1+z)**3+(1-Om)*f_de_cpl(z,w0,wa))
def DC(zmax,Om,w0,wa,n=300):
    zz=np.linspace(0,zmax,n); return np.trapezoid(1.0/E_cpl(zz,Om,w0,wa),zz)
import os as _os_rd, sys as _sys_rd
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), ".."))
from rd_camb import rd_mpc as _rd_camb  # r_d de CAMB, una sola funcion (2026-09-28)
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), "..", "p11_sondas"))  # lcdm_planck: la mnu de LCDM


def rd(ob_h2,om_h2):
    return _rd_camb(ob_h2, om_h2, mnu=__import__("lcdm_planck").LCDM_PLANCK["mnu"])  # CAMB; antes 147.27*(...) con normalizacion 0.15 % alta
def predict(H0,Om,w0,wa,rdv):
    out=[]
    for z,q in zip(DESI_Z,DESI_TYPE):
        dm=(C_KM/H0)*DC(z,Om,w0,wa); dh=C_KM/(H0*E_cpl(z,Om,w0,wa))
        out.append(dm/rdv if q=="DM_rd" else dh/rdv if q=="DH_rd" else (z*dm**2*dh)**(1/3)/rdv)
    return np.array(out)

def make_lpost(H0_anchor):
    """log-posterior CPL con el prior de H0 centrado en H0_anchor."""
    def lpost(th):
        H0,Om,w0,wa,ob=th
        if not(40<H0<100 and 0.15<Om<0.55 and -2.5<w0<0.5 and -3.0<wa<2.0 and 0.015<ob<0.030):
            return -np.inf
        om_h2=Om*(H0/100)**2
        lp =-0.5*((H0-H0_anchor)/SIGMA_H0)**2                       # ancla H0
        lp+=-0.5*((Om-PLANCK_OM[0])/PLANCK_OM[1])**2                # Planck Om
        lp+=-0.5*((ob-PLANCK_OBH2[0])/PLANCK_OBH2[1])**2            # Planck Obh2
        lp+=-0.5*((w0+1.0)/0.5)**2-0.5*(wa/1.0)**2                  # priors débiles w0,wa
        r=predict(H0,Om,w0,wa,rd(ob,om_h2))-DESI_OBS
        return lp-0.5*(r@DESI_COV_INV@r)
    return lpost

def run(anchor,nw=80,ns=4000,nb=1000):
    rng=np.random.default_rng(42)
    th0=np.array([anchor,0.315,-0.8,-0.6,0.02237])
    sc =np.array([0.4,0.01,0.1,0.25,0.0003])
    pos=th0+rng.standard_normal((nw,5))*sc
    s=emcee.EnsembleSampler(nw,5,make_lpost(anchor))
    pos,_,_=s.run_mcmc(pos,nb,progress=False); s.reset()
    s.run_mcmc(pos,ns,progress=False)
    ch=s.get_chain(flat=True)
    med=np.median(ch,axis=0); acc=np.mean(s.acceptance_fraction)
    return med,acc

if __name__=="__main__":
    SSEE=np.array([-0.840,-0.670])
    print(f"{'ancla H0':>10} | {'w0':>7} {'wa':>7} {'H0post':>7} {'Om':>6} | dist a SSEE | acc")
    print("-"*72)
    for name,a in [("MIRA",67.037),("Planck",67.36),("H_glob",__import__("ssee_core").H0_GLOBAL),("H0*~68.8",68.8),("SH0ES",73.0)]:
        med,acc=run(a)
        d=np.hypot(med[2]-SSEE[0],med[3]-SSEE[1])
        print(f"{name:>10} | {med[2]:+.3f} {med[3]:+.3f} {med[0]:7.2f} {med[1]:6.3f} | "
              f"{d:.3f} (eucl) | {acc:.2f}")
    print(f"{'SSEE alg':>10} | {SSEE[0]:+.3f} {SSEE[1]:+.3f}     —      —   |  0 (objetivo)")
