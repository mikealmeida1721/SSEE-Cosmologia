#!/usr/bin/env python3
"""bao_lcdm_libre.py — DESI DR2 BAO: SSEE en el clavo contra LCDM LIBRE.

LCDM libre en BAO solo tiene dos perillas que el dato ve: Omega_m y h*r_d
(D_M/r_d y D_H/r_d dependen de H0 y r_d solo a traves de su producto). Se
ajustan las dos. Es el competidor justo: LCDM con toda su libertad.

CALIBRADOR (R53): el ajuste tiene que devolver lo que publico DESI DR2 para BAO
solo en LCDM plano, leido de la fuente del articulo (arXiv:2503.14738,
main.tex): Omega_m = 0.2975 +- 0.0086, h r_d = 101.54 +- 0.73 Mpc.

SSEE: el chi2 del fondo clavado, de multisonda_fondo_clavado.bao_en_el_clavo()
(omega_b algebraico, corregido 2026-09-27). Cero libres.

FILA CLAVADA CON CAMB (2026-10-02). Para que DESI sea comparable con las demas
sondas se evaluan los DOS modelos con el fondo clavado y el mismo motor (CAMB:
distancias y r_d de cada uno): SSEE con su nucleo (Sum m_nu 0.06849, w0/wa) y
LCDM con Planck 2018 (lcdm_planck.py, m_nu 0.06). El chi2 de SSEE por formula de
r_d (10.904, 0.13 % largo) queda como referencia; el canonico es el de CAMB.
CONTROL (R53): el SSEE por CAMB tiene que dar el chi2 de bao_camb_control.json
(11.4065, el canonico) a 1e-3, o el script se para.

Salida: results/logs/bao_lcdm_libre.json
"""
import json
import os
import re
import sys

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p06_growth"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from desi_dr2_data import desi_covariance, load_desi_dr2  # noqa: E402
from procedencia import cabecera, con_acta  # noqa: E402
CTRL = os.path.join(_R, "results", "logs", "bao_camb_control.json")
print(cabecera(__file__, entradas=[CTRL]), flush=True)


def chi2_camb(d, Ci, H0, ombh2, omch2, mnu, w=-1.0, wa=0.0):
    """chi2 DESI con distancias y r_d de CAMB para un fondo dado (mismo motor para los dos)."""
    import camb
    from astropy import constants as const
    p = camb.set_params(H0=H0, ombh2=ombh2, omch2=omch2, mnu=mnu, w=w, wa=wa, dark_energy_model="ppf")
    r = camb.get_results(p)
    z = np.asarray(d["z"], float); t = np.asarray(d["type"])
    rd = r.get_derived_params()["rdrag"]
    dm = r.comoving_radial_distance(z); dh = const.c.to("km/s").value / r.hubble_parameter(z)
    pred = np.where(t == 0, dm, np.where(t == 1, dh, (z * dm ** 2 * dh) ** (1 / 3))) / rd
    res = pred - np.asarray(d["value"], float)
    Om = (ombh2 + omch2 + mnu / 93.14) / (H0 / 100) ** 2   # ORIGEN-VALOR: 93.14 — omega_nu = Sum m_nu / 93.14 eV (la misma convencion de ssee_core)
    return float(res @ Ci @ res), float(rd), float(Om), float(H0 / 100 * rd)

# ORIGEN: /mnt/datos/SSEE_data/desi_dr2_official/paper_2503.14738/main.tex
TEX = "/mnt/datos/SSEE_data/desi_dr2_official/paper_2503.14738/main.tex"
OUT = os.path.join(_R, "results", "logs", "bao_lcdm_libre.json")


def publicado():
    t = open(TEX).read()
    m = re.search(r"matter density parameter \$\\Om=([\d.]+)\\pm([\d.]+)\$ and product of the "
                  r"scaled Hubble constant and sound horizon at the drag epoch "
                  r"\$h\\rd=\(([\d.]+)\\pm([\d.]+)\)\$ Mpc", t)
    return dict(Om=float(m.group(1)), Om_err=float(m.group(2)),
                hrd=float(m.group(3)), hrd_err=float(m.group(4)), fuente="arXiv:2503.14738")


def main():
    from astropy import constants as const
    c_kms = const.c.to("km/s").value
    d = load_desi_dr2()
    Ci = np.linalg.inv(desi_covariance(d))

    def pred(Om, hrd):
        E = lambda z: np.sqrt(Om * (1 + z) ** 3 + 1 - Om)
        out = []
        for z, t in zip(d["z"], d["type"]):
            dm = c_kms / 100 * quad(lambda x: 1 / E(x), 0, z)[0] / hrd
            dh = c_kms / 100 / E(z) / hrd
            out.append(dm if t == 0 else dh if t == 1 else (z * dm ** 2 * dh) ** (1 / 3))
        return np.array(out)

    def chi2(p):
        r = pred(*p) - d["value"]
        return float(r @ Ci @ r)

    r = minimize(chi2, (0.3, 100.0), method="Nelder-Mead",
                 options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000))
    # errores por la curvatura (Fisher numerico) --- DESI da errores de posterior
    h = np.array([1e-4, 1e-2])
    H = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            ei, ej = np.eye(2)[i] * h[i], np.eye(2)[j] * h[j]
            H[i, j] = (chi2(r.x + ei + ej) - chi2(r.x + ei - ej) - chi2(r.x - ei + ej)
                       + chi2(r.x - ei - ej)) / (4 * h[i] * h[j]) / 2
    err = np.sqrt(np.diag(np.linalg.inv(H)))
    pub = publicado()
    s_om = (r.x[0] - pub["Om"]) / pub["Om_err"]
    s_hr = (r.x[1] - pub["hrd"]) / pub["hrd_err"]
    ok = bool(abs(s_om) < 0.3 and abs(s_hr) < 0.3)

    import multisonda_fondo_clavado as M
    ssee = M.bao_en_el_clavo()["chi2"]   # r_d por formula: referencia
    from ssee_core import H0_GLOBAL, OMEGA_B_H2, OMEGA_C_H2, SUM_MNU_EV, W0, WA
    from lcdm_planck import LCDM_PLANCK as P
    cS = chi2_camb(d, Ci, H0_GLOBAL, OMEGA_B_H2, OMEGA_C_H2, SUM_MNU_EV, W0, WA)
    cL = chi2_camb(d, Ci, P["H0"], P["ombh2"], P["omch2"], P["mnu"])
    ref = json.load(open(CTRL))["chi2_clavo"]
    if abs(cS[0] - ref) > 1e-3:
        sys.exit(f"CONTROL NO PASA: SSEE por CAMB {cS[0]:.4f} contra el canonico {ref:.4f}")
    res = dict(fecha="2026-09-27", publicado=pub,
               lcdm_libre=dict(Om=float(r.x[0]), Om_err=float(err[0]), hrd=float(r.x[1]),
                               hrd_err=float(err[1]), chi2=float(r.fun), dof=13 - 2,
                               sigma_vs_publicado=dict(Om=s_om, hrd=s_hr), reproduce=ok),
               ssee_clavo=dict(chi2=ssee, dof=13, libres=0, nota="r_d por formula (0.13 % largo): referencia, no canonico"),
               ssee_camb=dict(chi2=cS[0], rd=cS[1], Om=cS[2], hrd=cS[3], dof=13, libres=0),
               lcdm_planck_camb=dict(chi2=cL[0], rd=cL[1], Om=cL[2], hrd=cL[3], dof=13, libres=0),
               control_ssee_camb=dict(ref=ref, pasa=True),
               delta_chi2_ssee_menos_lcdm_libre=ssee - float(r.fun),
               delta_chi2_camb_ssee_menos_lcdm_planck=cS[0] - cL[0],
               delta_chi2_camb_ssee_menos_lcdm_libre=cS[0] - float(r.fun))
    print(f"  CALIBRADOR LCDM libre: Om={r.x[0]:.4f}±{err[0]:.4f}  h r_d={r.x[1]:.2f}±{err[1]:.2f}  "
          f"chi2={r.fun:.3f}/11")
    print(f"     publicado DESI DR2 : Om={pub['Om']}±{pub['Om_err']}  h r_d={pub['hrd']}±{pub['hrd_err']}"
          f"  -> {s_om:+.2f} / {s_hr:+.2f} sigma  {'REPRODUCE' if ok else 'NO REPRODUCE'}")
    print(f"  SSEE clavo: chi2={ssee:.3f}/13   Delta chi2 (SSEE - LCDM libre) = {ssee - r.fun:+.3f}")
    print(f"  CAMB, fondo clavado: SSEE chi2={cS[0]:.3f}/13 (Om {cS[2]:.4f}, h r_d {cS[3]:.2f})   "
          f"LCDM-Planck chi2={cL[0]:.3f}/13 (Om {cL[2]:.4f}, h r_d {cL[3]:.2f})   control SSEE vs canonico {ref:.4f}: PASA")
    res["fecha"] = str(__import__("datetime").date.today())
    json.dump(con_acta(res, __file__, entradas=[CTRL]), open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
