"""ΔBIC de Paper 3 con tau AJUSTADO en vez de prestado (cola #1).

QUE CONTESTA. Paper 3 publica ΔBIC = −24.02 sobre plik_lite TTTEEE + lowT +
lowE, SSEE (k=2) contra ΛCDM (k=6). Ese número se obtuvo con `tau` puesto al
valor fiducial de ΛCDM, no ajustado. Prestarle a un modelo el parámetro de
otro no es neutral: puede favorecerlo o perjudicarlo, y no se sabe cuál sin
medirlo. Aquí se ajusta `tau` en LOS DOS y se rehace la comparación.

QUE ESTA FIJO Y QUE LIBRE

  SSEE   fijo    ω_b, ω_c, H0, n_s por álgebra (leídos del núcleo);
                 w0, wa por álgebra
         libre   logA, tau                                    -> k = 2

  ΛCDM   fijo    w = −1, wa = 0
         libre   ω_b, ω_c, H0, n_s, logA, tau                 -> k = 6

BIC = χ²_min + k·ln(N). El ΔBIC que se reporta es BIC(SSEE) − BIC(ΛCDM);
negativo favorece a SSEE.

CONTROL (R53). El mínimo de ΛCDM tiene que caer donde Planck 2018 pone su
línea base: ω_b = 0.02237, ω_c = 0.1200, H0 = 67.36, n_s = 0.9649. Si el
optimizador aterriza lejos, no está midiendo el modelo sino su propia
convergencia, y el ΔBIC no vale. El criterio se escribe AQUI, antes de correr:
cada uno de los cuatro dentro de 2σ de Planck.

FUENTE: results/logs/cmb_dbic_tau_ajustado.json
"""
import json
import os
import pathlib
import sys
import time

import numpy as np
from scipy.optimize import minimize

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "p03_cmb"))

import ssee_core as S                                   # noqa: E402
from cmb_eval import chi2_y_s8                          # noqa: E402

SALIDA = REPO / "results" / "logs" / "cmb_dbic_tau_ajustado.json"

# ── N: SE MIDE, NO SE DECLARA (fix 2026-09-08, lo pidio Mike) ──────────
# Aqui decia `N_DATOS = 215 + 28 + 28 = 271`, con "215 bandas de plik_lite
# TTTEEE". FALSO: 215 son las bandas de TT SOLO. TTTEEE tiene 613, y se
# comprueba contando las lineas de cl_cmb_plik_v22.dat dentro del propio
# .clik. Con 271 el termino 4*ln(N) del BIC valia 22.41 en vez de 26.02, y
# ese unico error hacia que el dBIC pareciera EMPEORAR (-22.59) cuando en
# realidad MEJORA. El N se mide del likelihood o la corrida no corre.
_CLIK = pathlib.Path(os.path.expanduser(
    os.environ.get("COBAYA_PACKAGES_PATH", "~/cobaya_packages"))) / (
    "data/planck_2018/baseline/plc_3.0/hi_l/plik_lite/"
    "plik_lite_v22_TTTEEE.clik/clik/lkl_0/_external/cl_cmb_plik_v22.dat")
if not _CLIK.exists():
    raise SystemExit("no encuentro %s: N no se puede medir, no se corre" % _CLIK)
N_PLIK = sum(1 for _ in _CLIK.open())      # bandas TTTEEE de plik_lite
N_LOWT = 28                                # lowl.TT, ell = 2..29
N_LOWE = 28                                # lowl.EE (SimAll), ell = 2..29
N_DATOS = N_PLIK + N_LOWT + N_LOWE

FONDO_SSEE = dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2,
                  H0=S.H0_GLOBAL, ns=S.N_S)
W_SSEE, WA_SSEE = S.W0, S.WA

PLANCK = dict(ombh2=(0.02237, 0.00015), omch2=(0.1200, 0.0012),
              H0=(67.36, 0.54), ns=(0.9649, 0.0042))


def _log(*a):
    print(*a, flush=True)


def minimiza_ssee():
    """k=2: solo logA y tau. El fondo entero viene del algebra."""
    def f(u):
        if not (1.0 < u[0] < 5.0 and 0.010 < u[1] < 0.200):
            return 1e30
        return chi2_y_s8(dict(FONDO_SSEE, logA=u[0], tau=u[1]),
                         W_SSEE, WA_SSEE)[0]
    r = minimize(f, [3.044, 0.054], method="Nelder-Mead",
                 options=dict(xatol=1e-5, fatol=1e-3, maxiter=400))
    return float(r.fun), dict(logA=float(r.x[0]), tau=float(r.x[1]))


def minimiza_lcdm():
    """k=6: el fondo entero libre, con w = -1 y wa = 0."""
    LIM = [(0.005, 0.100), (0.001, 0.990), (20.0, 100.0),
           (0.500, 1.500), (1.0, 5.0), (0.010, 0.200)]

    def f(u):
        if any(not (a < v < b) for v, (a, b) in zip(u, LIM)):
            return 1e30
        return chi2_y_s8(dict(ombh2=u[0], omch2=u[1], H0=u[2], ns=u[3],
                              logA=u[4], tau=u[5]), -1.0, 0.0)[0]
    x0 = [0.02237, 0.1200, 67.36, 0.9649, 3.044, 0.054]
    r = minimize(f, x0, method="Nelder-Mead",
                 options=dict(xatol=1e-6, fatol=1e-3, maxiter=3000))
    k = ["ombh2", "omch2", "H0", "ns", "logA", "tau"]
    return float(r.fun), {n: float(v) for n, v in zip(k, r.x)}


def main():
    t0 = time.time()
    _log("=== SSEE (k=2): solo logA y tau libres")
    chi2_s, par_s = minimiza_ssee()
    _log("    chi2_min = %.3f   logA=%.4f tau=%.4f"
         % (chi2_s, par_s["logA"], par_s["tau"]))

    _log("=== LCDM (k=6): fondo entero libre")
    chi2_l, par_l = minimiza_lcdm()
    _log("    chi2_min = %.3f" % chi2_l)
    for n, v in par_l.items():
        _log("      %-6s %.6f" % (n, v))

    lnN = float(np.log(N_DATOS))
    bic_s = chi2_s + 2 * lnN
    bic_l = chi2_l + 6 * lnN
    dbic = bic_s - bic_l

    # CONTROL: el minimo de LCDM contra la linea base de Planck 2018.
    ctrl, ok = {}, True
    for n, (mu, sg) in PLANCK.items():
        d = abs(par_l[n] - mu) / sg
        ctrl[n] = dict(medido=par_l[n], planck=mu, sigma=d)
        if d > 2.0:
            ok = False
    _log("=== CONTROL: minimo LCDM vs Planck 2018 (criterio: < 2 sigma)")
    for n, c in ctrl.items():
        _log("    %-6s %.6f  vs %.6f   %.2f sigma%s"
             % (n, c["medido"], c["planck"], c["sigma"],
                "" if c["sigma"] <= 2 else "   <-- FUERA"))

    out = dict(
        corrida="ΔBIC Paper 3 con tau AJUSTADO en los dos modelos",
        N_datos=N_DATOS, ln_N=lnN,
        N_desglose=dict(plik_lite_TTTEEE=N_PLIK, lowl_TT=N_LOWT, lowl_EE=N_LOWE,
                        medido_en=str(_CLIK),
                        nota="antes se declaraba 271 con '215 bandas TTTEEE'; "
                             "215 es TT solo. Medido: %d" % N_PLIK),
        SSEE=dict(k=2, chi2_min=chi2_s, BIC=bic_s, libres=["logA", "tau"],
                  fondo_fijo_por_algebra=dict(FONDO_SSEE, w0=W_SSEE, wa=WA_SSEE),
                  mejor=par_s),
        LCDM=dict(k=6, chi2_min=chi2_l, BIC=bic_l,
                  libres=["ombh2", "omch2", "H0", "ns", "logA", "tau"],
                  fondo_fijo=dict(w0=-1.0, wa=0.0), mejor=par_l),
        delta_BIC=dbic,
        publicado_con_tau_prestado=-24.02,
        control=dict(criterio="cada parametro de LCDM a < 2 sigma de Planck 2018",
                     pasa=ok, detalle=ctrl),
        segundos=time.time() - t0,
    )
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(out, indent=1))
    _log("\nΔBIC = %.2f   (publicado con tau prestado: -24.02)" % dbic)
    _log("CONTROL %s" % ("PASA" if ok else "FALLA"))
    _log("escrito -> %s" % SALIDA.relative_to(REPO))


if __name__ == "__main__":
    main()
