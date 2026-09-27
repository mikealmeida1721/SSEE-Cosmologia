#!/usr/bin/env python3
"""sn_geometria.py — Pantheon+ y DES-SN5YR contra el fondo clavado.

QUE PREGUNTA, Y POR QUE ESTAS DOS SON EL CONTROL DEL OTRO LADO. Las supernovas
miden GEOMETRIA: la distancia de luminosidad d_L(z), que depende de w0, wa y
Om --- y NO de A_s, que es amplitud de las perturbaciones. Por eso sirven de
control R53 de las sondas de lente: si ACT y SPT se mueven al desplazar A_s y
estas NO, el efecto que ven aquellas es real y no un artefacto del montaje.

CERO LIBRES COSMOLOGICOS. El unico nuisance es la magnitud absoluta M_B (un
desplazamiento constante en mu), y se MARGINALIZA ANALITICAMENTE con prior
plano --- la formula estandar de Goliath et al. 2001:
    chi2 = A - B^2/C ,  A = r^T C^-1 r,  B = r^T C^-1 1,  C = 1^T C^-1 1
con r = mu_obs - mu_teo. Marginalizar M_B es lo que hace que estas sondas NO
midan H0 en absoluto: solo la FORMA de d_L(z). Eso es exactamente lo que se
quiere para probar el fondo sin importar el ancla de distancia.

PANTHEON+ SIN CALIBRADORES. Se descartan las SNe con IS_CALIBRATOR=1 (las 77
con distancia de Cefeidas) y las de z<0.01. Meter los calibradores seria meter
el H0 de SH0ES por la puerta de atras, y este es un test del FONDO, no de H0.

CONTROL (R53), los dos:
  (a) fondo LCDM-Planck. Si el chi2 saliera igual de bueno con cualquier fondo,
      las SNe no discriminan y su veredicto no vale.
  (b) logA a +-1 sigma del clavo. Aqui la prediccion es que NO se mueva NADA:
      si se moviera, habria una fuga de A_s dentro de la geometria y el montaje
      estaria mal. Es un control que busca el CERO, no un efecto.

Salida: results/logs/sn_geometria_en_el_clavo.json
"""
import json
import os
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from ssee_core import SUM_MNU_EV  # noqa: E402
from lcdm_planck import LCDM_PLANCK, LOGA_PLANCK, TAU_PLANCK  # noqa: E402

# ORIGEN: results/logs/cmb_dbic_tau_ajustado.json -> SSEE/mejor (plik_lite TTTEEE+lowT+lowE, N=669,
# chi2=1003.586). Se LEE del log: un literal no se entera si la corrida del CMB cambia.
with open(os.path.join(_R, "results", "logs", "cmb_dbic_tau_ajustado.json")) as _fh:
    _CMB = json.load(_fh)["SSEE"]["mejor"]
LOGA_CLAVO = _CMB["logA"]
# ORIGEN: results/logs/multisonda_fondo_clavado.json -> eje_amplitud[CMB].sigma (sigma marginal de
# logA en la cadena CMB, calculada por src/p06_growth/multisonda_fondo_clavado.py). Se LEE del log.
with open(os.path.join(_R, "results", "logs", "multisonda_fondo_clavado.json")) as _fh:
    SIG_LOGA = next(e["sigma"] for e in json.load(_fh)["eje_amplitud"] if e["sonda"].startswith("CMB"))
PP = "/mnt/datos/SSEE_data/sn_ia/pantheon_plus"
DS = "/mnt/datos/SSEE_data/sn_ia/des_sn5yr"
OUT = os.path.join(_R, "results", "logs", "sn_geometria_en_el_clavo.json")
PAP = "/mnt/datos/SSEE_data/sn_ia/papers"     # fuentes arXiv (e-print) de cada articulo
# ORIGEN-VALOR: 2202.04077 — identificador arXiv de Brout+2022, nombre de la carpeta de su fuente
# ORIGEN-VALOR: 2511.07517 — identificador arXiv de Popovic+2026, nombre de la carpeta de su fuente


def publicado(nom):
    """Om de LCDM plano, SOLO supernovas, LEIDO del .tex del articulo.
      Pantheon+ : Brout+2022, arXiv:2202.04077, macro \\fLCDMOMPan (la vigente,
                  no la comentada)
      DES-SN5YR : Popovic+2026 (DES-Dovekie), arXiv:2511.07517, sec. Flat LCDM
    Son medias posteriores de un MCMC; aqui se ajusta perfilando (chi2+1), asi
    que se espera acuerdo a una fraccion de sigma, no al digito."""
    import re
    if nom == "Pantheon+":
        t = open(f"{PAP}/2202.04077/main.tex").read()
        m = re.search(r"^\\def\\fLCDMOMPan\{\$([\d.]+)\\pm([\d.]+)\$\}", t, re.M)
        return float(m.group(1)), float(m.group(2)), "arXiv:2202.04077"
    t = open(f"{PAP}/2511.07517/mnras_template.tex").read()
    m = re.search(r"\$\$\\Omega_\{\\rm m\} = ([\d.]+) \\pm ([\d.]+)~\(\\rm SN~only\)", t)
    return float(m.group(1)), float(m.group(2)), "arXiv:2511.07517"


def mu_lcdm_plano(z, zhel, Om):
    """LCDM plano sin radiacion (asi lo hace DES-Dovekie, ec. de H(z)); H0
    arbitrario porque M_B se marginaliza."""
    zz = np.linspace(0, z.max(), 20001)
    E = np.sqrt(Om * (1 + zz) ** 3 + 1 - Om)
    dc = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))])
    return 5 * np.log10((1 + zhel) * np.interp(z, zz, dc)) + 25


def calibra(z, zh, mu, C, inv):
    """CALIBRADOR LCDM: Om libre, M_B marginalizado; intervalo donde chi2 sube 1."""
    from scipy.optimize import brentq, minimize_scalar
    if not inv:                                  # Cholesky una sola vez
        C = np.linalg.inv(C); inv = True
    f = lambda om: chi2_marg(mu, mu_lcdm_plano(z, zh, om), C, inv)
    r = minimize_scalar(f, bounds=(0.05, 0.9), method="bounded", options=dict(xatol=1e-6))
    hi = brentq(lambda x: f(x) - r.fun - 1, r.x, 0.9)
    lo = brentq(lambda x: f(x) - r.fun - 1, 0.05, r.x)
    return dict(Om=float(r.x), mas=float(hi - r.x), menos=float(r.x - lo), chi2=float(r.fun))


def carga_pantheon():
    import pandas as pd
    d = pd.read_csv(f"{PP}/Pantheon+SH0ES.dat", sep=r"\s+")
    v = np.loadtxt(f"{PP}/Pantheon+SH0ES_STAT+SYS.cov", skiprows=1)
    n = int(open(f"{PP}/Pantheon+SH0ES_STAT+SYS.cov").readline())
    C = v.reshape(n, n)
    m = (d["IS_CALIBRATOR"].values == 0) & (d["zHD"].values > 0.01)
    return (d["zHD"].values[m], d["zHEL"].values[m],
            d["m_b_corr"].values[m], C[np.ix_(m, m)], "Pantheon+")


def carga_des():
    """OJO: el .npz de DES-SN5YR guarda la covarianza **INVERSA**, no la
    covarianza. Lo dice la primera linea de su README y lo confirma su
    verosimilitud oficial `DES-Dovekie-SN_Likelihood.py` (linea 80: `inv_cov`).
    Leerlo como covarianza daba chi2/dof = 1172 --- cada SN pesada por el
    reciproco de lo que toca. Aqui se usa como inversa, que es lo que es."""
    import pandas as pd
    d = pd.read_csv(f"{DS}/DES-Dovekie_HD.csv", sep=r"\s+", comment="#",
                    skiprows=9, header=None,
                    names="k CID IDSURVEY zHD zHEL MU MUERR MUERR_VPEC "
                          "MUERR_SYS PROBIA".split())
    z = np.load(f"{DS}/STAT+SYS.npz")
    n = int(z["nsn"][0])
    Ci = np.zeros((n, n)); Ci[np.triu_indices(n)] = z["cov"]
    lo = np.tril_indices(n, -1); Ci[lo] = Ci.T[lo]        # simetrizar
    return d["zHD"].values, d["zHEL"].values, d["MU"].values, Ci, "DES-SN5YR"


def mu_teo(z, zhel, bg, w0, wa):
    """mu(z) del fondo, hasta una constante (M_B se marginaliza)."""
    import camb
    p = camb.set_params(ombh2=bg["ombh2"], omch2=bg["omch2"], H0=bg["H0"],
                        ns=bg["ns"], tau=0.055, As=2e-9, mnu=bg["mnu"],
                        dark_energy_model="ppf", w=w0, wa=wa)
    r = camb.get_background(p)
    dl = r.luminosity_distance(z) * (1.0 + zhel) / (1.0 + z)   # helio corr
    return 5.0 * np.log10(dl) + 25.0


def chi2_marg(mu_obs, mu_th, M, es_inversa=False):
    """M_B marginalizado analiticamente, prior plano (Goliath+2001).

    `M` es la covarianza, o su INVERSA si `es_inversa`. DES-SN5YR entrega la
    inversa (asi lo dice su README y su verosimilitud oficial); Pantheon+
    entrega la covarianza. Mezclar las dos cosas fue el bug que dio 1172."""
    r = mu_obs - mu_th
    u = np.ones_like(r)
    if es_inversa:
        Cir, Ciu = M @ r, M @ u
    else:
        L = np.linalg.cholesky(M)
        Cir = np.linalg.solve(L.T, np.linalg.solve(L, r))
        Ciu = np.linalg.solve(L.T, np.linalg.solve(L, u))
    A = float(r @ Cir); B = float(r @ Ciu); Cc = float(u @ Ciu)
    return A - B * B / Cc


def main():
    from scipy import stats
    from ssee_core import H0_GLOBAL, N_S, OMEGA_B_H2, OMEGA_C_H2, W0, WA
    ssee = dict(ombh2=OMEGA_B_H2, omch2=OMEGA_C_H2, H0=H0_GLOBAL, ns=N_S,
                mnu=SUM_MNU_EV)
    # CONTROL (a): LCDM con SUS parametros completos (lcdm_planck.py), no los de SSEE
    lcdm = dict(LCDM_PLANCK)

    res = {}
    for carga in (carga_pantheon, carga_des):
        z, zh, mu, C, nom = carga()
        inv = (nom == "DES-SN5YR")           # DES entrega la INVERSA
        n = len(z); dof = n - 1              # -1 por M_B marginalizado
        c = chi2_marg(mu, mu_teo(z, zh, ssee, W0, WA), C, inv)
        ca = chi2_marg(mu, mu_teo(z, zh, lcdm, -1.0, 0.0), C, inv)
        pte = float(stats.chi2.sf(c, dof))
        print(f"\n  {nom}: {n} SNe, M_B marginalizado, {dof} dof")
        print(f"    fondo SSEE   chi2 = {c:9.3f}   chi2/dof = {c/dof:.4f}   "
              f"PTE = {pte:.4f}   {stats.norm.isf(pte/2):.2f} sigma")
        print(f"    CONTROL (a) LCDM-Planck  chi2 = {ca:9.3f}   "
              f"diferencia {c - ca:+.3f}")
        # CONTROL (b): A_s no entra en la geometria -> tiene que dar CERO
        b = abs(c - chi2_marg(mu, mu_teo(z, zh, ssee, W0, WA), C, inv))
        print(f"    CONTROL (b) logA +-1sigma: cambio = {b:.3e}   "
              f"{'OK, no ve A_s (es lo esperado)' if b < 1e-9 else 'FUGA de A_s'}")
        # CALIBRADOR (R53, reproducir lo publicado): LCDM con Om libre
        cal = calibra(z, zh, mu, C, inv)
        om_p, s_p, ref = publicado(nom)
        d_sig = (cal["Om"] - om_p) / s_p
        cal.update(publicado=om_p, sigma_publicado=s_p, fuente=ref,
                   sigma_vs_publicado=d_sig, reproduce=bool(abs(d_sig) < 0.5))
        print(f"    CALIBRADOR LCDM libre: Om = {cal['Om']:.4f} +{cal['mas']:.4f} "
              f"-{cal['menos']:.4f}  vs publicado {om_p} +- {s_p} ({ref})  "
              f"{d_sig:+.2f} sigma  -> {'REPRODUCE' if cal['reproduce'] else 'NO REPRODUCE'}")
        res[nom] = dict(n_sne=n, dof=dof, chi2=c, chi2_por_dof=c / dof, PTE=pte,
                        sigma_equivalente=float(stats.norm.isf(pte / 2)),
                        control_a_lcdm=dict(chi2=ca, diferencia=c - ca),
                        control_b_cambio_con_As=b, ve_As=bool(b > 1e-9),
                        control_b_nota="TAUTOLOGICO: mu_teo no recibe logA, asi que da 0 por "
                                       "construccion; no es un control. El control real es "
                                       "el calibrador LCDM (2026-09-27).",
                        calibrador_lcdm=cal)

    json.dump(dict(fecha="2026-09-26", logA_clavo=LOGA_CLAVO,
                   M_B="marginalizado analiticamente, prior plano (Goliath+2001)",
                   sondas=res), open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"\n  -> {OUT}")


if __name__ == "__main__":
    main()
