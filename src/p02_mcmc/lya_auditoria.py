#!/usr/bin/env python3
"""lya_auditoria.py — el apendice B.2 de Paper 2 (Ly-alpha a z = 2.33), con log.

POR QUE (2026-09-30). El apendice cita E(2.33), D_H, r_d, D_H/r_d y su pull
para dos escenarios, y el chi2 diagonal de los 13 puntos DESI con sus
residuos mas grandes, todo escrito a mano: ningun log lo calculaba.

MODELOS (Paper 2, apendice B.2):
  ssee: omega_b, omega_c, Sigma m_nu del nucleo, Omega_m = omega_m/h^2 (la unica
    densidad), H0 = H0_GLOBAL, w0 y w_a de SSEE; r_d, D_M, D_H de CAMB (PPF),
    la convencion de todo el repo desde 2026-09-28 (rd_camb.py, bao_camb.py).
  lcdm_planck: Planck 2018 con sus parametros (lcdm_planck.py).
(2026-10-03: se retira el «escenario A», que ponia s_m = 1+w0 = 0.160 como
 Omega_m: omega_c = s_m h^2 - ... . s_m es un numero de la ecuacion de estado;
 ese caso no es una version del modelo. Con el sale la formula vieja de r_d.)

CONTROL (R53): el chi2 de B con la covarianza COMPLETA tiene que ser el
canonico de bao_camb.chi2_desi (11.406 en H_glob) a 1e-3; y el de LCDM, el de
results/logs/bao_lcdm_planck.json.

Salida: results/logs/lya_auditoria.json
"""
import json
import os
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
import camb  # noqa: E402
import ssee_core as S  # noqa: E402
from bao_camb import chi2_desi  # noqa: E402
from desi_dr2_data import desi_covariance, load_desi_dr2  # noqa: E402
from lcdm_planck import LCDM_PLANCK as L  # noqa: E402
from procedencia import con_acta  # noqa: E402

C_KMS = camb.constants.c / 1e3
Z_LYA = 2.33   # ORIGEN-VALOR: 2.33 — z efectivo del punto Ly-alpha de DESI DR2 (data/raw/desi_dr2_bao.csv)
d = load_desi_dr2()
z, tipo, obs, sig = (np.asarray(d[k]) for k in ("z", "type", "value", "sigma"))
tipo = tipo.astype(int)
Cinv = np.linalg.inv(desi_covariance(d))
i_lya = int(np.where((np.abs(z - Z_LYA) < 1e-6) & (tipo == 1))[0][0])
NOMBRE = {0: "DM/rd", 1: "DH/rd", 2: "DV/rd"}


def fondo(H0, ombh2, omch2, mnu, w0, wa):
    p = camb.set_params(H0=H0, ombh2=ombh2, omch2=omch2, mnu=mnu, w=w0, wa=wa,
                        dark_energy_model="ppf" if (w0, wa) != (-1.0, 0.0) else "fluid")
    r = camb.get_background(p)
    rd = r.get_derived_params()["rdrag"]
    dm = r.comoving_radial_distance(z)
    dh = C_KMS / r.hubble_parameter(z)
    pred = np.where(tipo == 0, dm, np.where(tipo == 1, dh, (z * dm ** 2 * dh) ** (1 / 3))) / rd
    res = pred - obs
    pull = res / sig
    k = int(np.argmax(np.abs(pull)))
    E = r.hubble_parameter(Z_LYA) / H0
    f_de = float(r.get_Omega("de", Z_LYA))
    # rho_DE(z)/rho_DE(0) de CPL (lo que el apendice llama f_DE)
    rho_de = (1 + Z_LYA) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * Z_LYA / (1 + Z_LYA))
    return dict(rd=float(rd), E_lya=float(E), DH_lya=float(C_KMS / (H0 * E)), f_DE_lya=f_de,
                rhoDE_z_sobre_rhoDE_0_lya=float(rho_de),
                DH_rd_lya=float(pred[i_lya]), pull_lya=float(pull[i_lya]),
                Om=float((ombh2 + omch2 + mnu / 93.14) / (H0 / 100) ** 2),  # ORIGEN-VALOR: 93.14 — conversion de CAMB m_nu -> omega_nu que usa omch2 aqui
                chi2_diag=float(np.sum(pull ** 2)), chi2_cov=float(res @ Cinv @ res),
                pull_max=dict(z=float(z[k]), cantidad=NOMBRE[tipo[k]], pull=float(pull[k])),
                pulls=[dict(z=float(a), cantidad=NOMBRE[b], pull=float(c)) for a, b, c in zip(z, tipo, pull)])


B = fondo(S.H0_GLOBAL, S.OMEGA_B_H2, S.OMEGA_C_H2, S.SUM_MNU_EV, S.W0, S.WA)
LC = fondo(L["H0"], L["ombh2"], L["omch2"], L["mnu"], -1.0, 0.0)

ref_B = chi2_desi(S.H0_GLOBAL, B["rd"])
ref_L = json.load(open(os.path.join(_R, "results", "logs", "bao_lcdm_planck.json")))["lcdm_planck"]["chi2"]
ctl = dict(B_cov_vs_bao_camb=dict(aqui=B["chi2_cov"], bao_camb=ref_B),
           LCDM_cov_vs_bao_lcdm_planck=dict(aqui=LC["chi2_cov"], log=ref_L))
pasa = abs(B["chi2_cov"] - ref_B) < 1e-3 and abs(LC["chi2_cov"] - ref_L) < 1e-3
out = dict(fecha=str(__import__("datetime").date.today()),
           dato_lya=dict(z=Z_LYA, DH_rd=float(obs[i_lya]), sigma=float(sig[i_lya])),
           ssee=B, lcdm_planck=LC, rd_B_sobre_lcdm=B["rd"] / LC["rd"],
           control=dict(contra=ctl, pasa=bool(pasa)))
json.dump(con_acta(out, __file__, entradas=[os.path.join(_R, "data", "raw", "desi_dr2_bao.csv"),
                                             os.path.join(_R, "results", "logs", "bao_lcdm_planck.json")]),
          open(os.path.join(_R, "results", "logs", "lya_auditoria.json"), "w"), indent=1)
for n, x in (("SSEE", B), ("LCDM", LC)):
    print(f"  {n:4s} r_d {x['rd']:.2f}  f_DE {x['f_DE_lya']:.3f}  E {x['E_lya']:.3f}  D_H {x['DH_lya']:.0f}"
          f"  D_H/r_d {x['DH_rd_lya']:.3f} ({x['pull_lya']:+.2f} sigma)  chi2 diag {x['chi2_diag']:.2f}"
          f"  cov {x['chi2_cov']:.3f}  pull max {x['pull_max']}")
print(f"  control: {'PASA' if pasa else 'NO PASA'} {ctl}")
