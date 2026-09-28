"""Punto de fuga v2: con la amplitud clavada donde la ponen las sondas
tardias, ¿que ingrediente quiere moverse? Ahora con tau LIBRE (cola #6).

QUE CONTESTA. Las sondas tardias (cizalla de KiDS y agrupamiento de BOSS)
piden una amplitud primordial mas baja que el CMB. Si se CLAVA la amplitud en
ese valor tardio y se deja que el CMB se defienda, ¿que ingrediente del fondo
pide moverse para recuperar el ajuste, y cuanto recupera cada uno? Eso senala
por donde se escapa la tension: es un mapa de responsabilidades, no un ajuste.

POR QUE UNA v2. La v1 (`results/logs/cmb_punto_de_fuga.json`) dejo `tau`
CONGELADO en la linea base. Con la amplitud bajada y `tau` sin poder
acompanarla, la base salio absurda: chi2 = 14622 frente a 1005 de referencia.
Sobre una base rota, el "cuanto recupera cada ingrediente" no significa nada,
porque casi todo lo que recuperan es deshacer el destrozo. Aqui `tau` es libre
SIEMPRE, tanto en la base como en cada variante.

QUE ESTA FIJO Y QUE LIBRE

  referencia   fondo algebraico; logA y tau libres          -> el mejor ajuste
  base         fondo algebraico; logA CLAVADO al tardio;
               tau libre                                     -> el castigo
  variante_X   igual que la base, pero ademas X libre        -> cuanto recupera X

CONTROL (R53). Se incluye `logA` como una variante mas. Al soltarlo tiene que
recuperar TODO el castigo y volver a la referencia (recupera ~= chi2_base -
chi2_ref). Si no vuelve, el barrido no esta midiendo lo que dice: estaria
midiendo el optimizador. Criterio escrito antes de correr: que `logA` recupere
mas del 95% del castigo.

FUENTE: results/logs/cmb_punto_de_fuga2.json
"""
import json
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

SALIDA = REPO / "results" / "logs" / "cmb_punto_de_fuga2.json"

BASE = dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2,
            H0=S.H0_GLOBAL, ns=S.N_S, logA=3.044, tau=0.054)
W, WA = S.W0, S.WA

# La amplitud que piden las sondas tardias. logA = ln(10^10 A_s).
# 2.8418 = combinacion inversa-varianza de las DOS sondas tardias, con el
# fondo de SSEE en las dos:
#     KiDS R3   logA = 2.8627 +- 0.0508  (growth_2026-07/R3_ssee_kids_S8.json)
#     BOSS R1R2 logA = 2.7636 +- 0.0981  (growth_2026-07/R1R2_boss_lpt_cobaya.json)
#     combinada      = 2.841783 +- 0.0451   -> difiere 1.7e-05 del valor clavado
# Reproducido el 2026-09-08 desde esos dos logs. Antes aqui ponia solo "ajuste
# conjunto KiDS+BOSS previo (v1, mismo valor)", sin decir cual ni con que barra:
# imposible de comprobar sin rehacerlo.
#
# IMPORTA CUAL SE CLAVA (lo pregunto Mike): este es el A_s TARDIO. Si se clavara
# el que preferiria el propio CMB (logA = 3.0448, de cmb_dbic_tau_ajustado.json)
# NO habria castigo ninguno, por construccion. La deriva entre los dos es
# -0.2031, o sea 4.50 sigma de la barra tardia. Todo lo que mide esta corrida es
# quien puede absorber ESA deriva.
LOGA_TARDE = 2.8418

# ingrediente -> (limite inferior, limite superior, sigma para reportar)
SUELTA = {
    "ombh2": (0.005, 0.100, 0.00015),
    "omch2": (0.001, 0.300, 0.0012),
    "H0":    (40.0,  90.0,  0.54),
    "ns":    (0.500, 1.500, 0.0042),
    "logA":  (1.0,   5.0,   0.014),     # el CONTROL
}


def _chi2(p):
    return chi2_y_s8(p, W, WA)[0]


def optimiza(fijos, libres):
    """libres: lista de nombres. Devuelve (chi2, dict de los libres)."""
    x0 = [BASE[n] for n in libres]
    lim = [SUELTA[n][:2] if n in SUELTA else (0.010, 0.200) for n in libres]

    def f(u):
        if any(not (a < v < b) for v, (a, b) in zip(u, lim)):
            return 1e30
        return _chi2(dict(fijos, **{n: v for n, v in zip(libres, u)}))
    r = minimize(f, x0, method="Nelder-Mead",
                 options=dict(xatol=1e-6, fatol=1e-3, maxiter=1200))
    return float(r.fun), {n: float(v) for n, v in zip(libres, r.x)}


def main():
    t0 = time.time()
    fondo = {k: BASE[k] for k in ("ombh2", "omch2", "H0", "ns")}

    print("=== REFERENCIA: logA y tau libres", flush=True)
    chi2_ref, par_ref = optimiza(fondo, ["logA", "tau"])
    print("    chi2_ref = %.3f   %s" % (chi2_ref, par_ref), flush=True)

    print("=== BASE: logA CLAVADO al tardio %.4f, tau libre" % LOGA_TARDE,
          flush=True)
    chi2_base, par_base = optimiza(dict(fondo, logA=LOGA_TARDE), ["tau"])
    castigo = chi2_base - chi2_ref
    print("    chi2_base = %.3f   tau=%.4f   castigo = %.3f"
          % (chi2_base, par_base["tau"], castigo), flush=True)

    ing = {}
    for n, (_, _, sg) in SUELTA.items():
        libres = ["tau", n] if n != "logA" else ["tau", "logA"]
        fj = dict(fondo, logA=LOGA_TARDE)
        if n != "logA":
            fj.pop(n, None)
        c, p = optimiza(fj, libres)
        rec = castigo - (c - chi2_ref)
        ing[n] = dict(valor=p[n], algebraico=BASE[n],
                      sigmas=(p[n] - BASE[n]) / sg,
                      chi2=c, recupera=rec,
                      pct_del_castigo=100.0 * rec / castigo,
                      tau=p["tau"])
        print("    %-6s -> %.6f (%+.2f sig)  chi2=%.3f  recupera %.1f (%.1f%%)"
              % (n, p[n], ing[n]["sigmas"], c, rec, ing[n]["pct_del_castigo"]),
              flush=True)

    ok = ing["logA"]["pct_del_castigo"] > 95.0
    print("=== CONTROL: logA suelto recupera %.1f%% del castigo (criterio >95%%)"
          % ing["logA"]["pct_del_castigo"], flush=True)

    out = dict(
        corrida="punto de fuga v2 — tau LIBRE en la base y en cada variante",
        logA_tarde=LOGA_TARDE,
        referencia=dict(chi2=chi2_ref, **par_ref),
        base=dict(chi2=chi2_base, tau=par_base["tau"], castigo=castigo),
        ingredientes=ing,
        control=dict(criterio="logA suelto recupera >95% del castigo",
                     pasa=ok, recupera_pct=ing["logA"]["pct_del_castigo"]),
        v1_invalidada=dict(
            log="results/logs/cmb_punto_de_fuga.json",
            razon="tau congelado en la base: chi2_base=14622 frente a 1005 de "
                  "referencia. Sobre una base rota el reparto no significa nada"),
        segundos=time.time() - t0)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(out, indent=1))
    print("\nCONTROL %s" % ("PASA" if ok else "FALLA"), flush=True)
    print("escrito -> %s" % SALIDA.relative_to(REPO), flush=True)


if __name__ == "__main__":
    main()
