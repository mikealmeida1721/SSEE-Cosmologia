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
from desi_dr2_data import desi_covariance, load_desi_dr2  # noqa: E402

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
    ssee = M.bao_en_el_clavo()["chi2"]
    res = dict(fecha="2026-09-27", publicado=pub,
               lcdm_libre=dict(Om=float(r.x[0]), Om_err=float(err[0]), hrd=float(r.x[1]),
                               hrd_err=float(err[1]), chi2=float(r.fun), dof=13 - 2,
                               sigma_vs_publicado=dict(Om=s_om, hrd=s_hr), reproduce=ok),
               ssee_clavo=dict(chi2=ssee, dof=13, libres=0),
               delta_chi2_ssee_menos_lcdm_libre=ssee - float(r.fun))
    print(f"  CALIBRADOR LCDM libre: Om={r.x[0]:.4f}±{err[0]:.4f}  h r_d={r.x[1]:.2f}±{err[1]:.2f}  "
          f"chi2={r.fun:.3f}/11")
    print(f"     publicado DESI DR2 : Om={pub['Om']}±{pub['Om_err']}  h r_d={pub['hrd']}±{pub['hrd_err']}"
          f"  -> {s_om:+.2f} / {s_hr:+.2f} sigma  {'REPRODUCE' if ok else 'NO REPRODUCE'}")
    print(f"  SSEE clavo: chi2={ssee:.3f}/13   Delta chi2 (SSEE - LCDM libre) = {ssee - r.fun:+.3f}")
    json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
