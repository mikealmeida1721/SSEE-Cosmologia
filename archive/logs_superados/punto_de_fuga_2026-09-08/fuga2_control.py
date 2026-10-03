"""El control del punto de fuga, corrido APARTE y AHORA — mas la prueba de
que el reparto de uno en uno no se lo inventa (objecion de M. Almeida).

DOS FALLOS DE DISENO QUE SENALO MIKE, 2026-09-08:

  1. EL CONTROL IBA AL FINAL. `punto_de_fuga2.py` interroga los ingredientes en
     el orden ombh2, omch2, H0, ns y deja `logA` —que es el control— para el
     ultimo. O sea que se pasa una hora midiendo sin saber si la maquina hace
     lo que dice. Si el control fallara, todo lo anterior se tira. El control
     va PRIMERO: si no pasa, no se gasta el resto.

  2. DE UNO EN UNO NO VE LAS COMBINACIONES. Soltar cada ingrediente por
     separado supone que el castigo se puede repartir entre culpables
     individuales. Puede no ser asi: dos que por separado callan poco pueden
     callar mucho JUNTOS, porque entre ellos hay degeneracion. Si la suma de
     los individuales no llega a lo que consiguen todos a la vez, el reparto de
     uno en uno esta contando de menos y hay que decirlo.

QUE HACE, en este orden:

  A. control  — suelta SOLO logA. Debe recuperar >95% del castigo: es el
                parametro clavado, o sea el culpable directo. Si no lo
                recupera, la maquina no mide ingredientes, mide al optimizador,
                y el reparto entero se tira.
  B. conjunto — suelta los CUATRO ingredientes del fondo a la vez (con logA
                clavado). Se compara con la suma de los individuales.

FUENTE: results/logs/cmb_fuga2_control.json
"""
import json
import pathlib
import sys
import time

from scipy.optimize import minimize

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "p03_cmb"))

import ssee_core as S                                   # noqa: E402
from cmb_eval import chi2_y_s8                          # noqa: E402

SALIDA = REPO / "results" / "logs" / "cmb_fuga2_control.json"

BASE = dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2,
            H0=S.H0_GLOBAL, ns=S.N_S, logA=3.044, tau=0.054)
W, WA = S.W0, S.WA
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

LIM = {"ombh2": (0.005, 0.100), "omch2": (0.001, 0.300),
       "H0": (40.0, 90.0), "ns": (0.500, 1.500),
       "logA": (1.0, 5.0), "tau": (0.010, 0.200)}


def optimiza(fijos, libres, maxiter=1500):
    x0 = [BASE[n] for n in libres]
    lim = [LIM[n] for n in libres]

    def f(u):
        if any(not (a < v < b) for v, (a, b) in zip(u, lim)):
            return 1e30
        return chi2_y_s8(dict(fijos, **{n: v for n, v in zip(libres, u)}),
                         W, WA)[0]
    r = minimize(f, x0, method="Nelder-Mead",
                 options=dict(xatol=1e-6, fatol=1e-3, maxiter=maxiter))
    return float(r.fun), {n: float(v) for n, v in zip(libres, r.x)}


def main():
    t0 = time.time()
    fondo = {k: BASE[k] for k in ("ombh2", "omch2", "H0", "ns")}

    print("=== referencia: logA y tau libres", flush=True)
    chi2_ref, _ = optimiza(fondo, ["logA", "tau"])
    print("    %.3f" % chi2_ref, flush=True)

    print("=== base: logA clavado en %.4f, tau libre" % LOGA_TARDE, flush=True)
    chi2_base, _ = optimiza(dict(fondo, logA=LOGA_TARDE), ["tau"])
    castigo = chi2_base - chi2_ref
    print("    %.3f   castigo = %.3f" % (chi2_base, castigo), flush=True)

    # ── A. EL CONTROL, PRIMERO ──────────────────────────────────────────
    print("=== A. CONTROL: se suelta SOLO logA (criterio: recupera >95%)",
          flush=True)
    c_ctrl, p_ctrl = optimiza(fondo, ["tau", "logA"])
    rec_ctrl = castigo - (c_ctrl - chi2_ref)
    pct_ctrl = 100.0 * rec_ctrl / castigo
    print("    chi2=%.3f  logA=%.4f  recupera %.1f = %.2f%%"
          % (c_ctrl, p_ctrl["logA"], rec_ctrl, pct_ctrl), flush=True)
    ok = pct_ctrl > 95.0
    print("    CONTROL %s" % ("PASA" if ok else "FALLA"), flush=True)

    if not ok:
        SALIDA.write_text(json.dumps(dict(
            control=dict(pasa=False, recupera_pct=pct_ctrl),
            veredicto="la maquina no reproduce el castigo soltando el propio "
                      "parametro clavado: el reparto por ingredientes NO vale"),
            indent=1))
        print("no se corre el conjunto: sin control no hay medida", flush=True)
        return

    # ── B. LOS CUATRO A LA VEZ ──────────────────────────────────────────
    print("=== B. CONJUNTO: los cuatro ingredientes libres a la vez",
          flush=True)
    ing = ["ombh2", "omch2", "H0", "ns"]
    c_conj, p_conj = optimiza(dict(logA=LOGA_TARDE), ["tau"] + ing,
                              maxiter=4000)
    rec_conj = castigo - (c_conj - chi2_ref)
    print("    chi2=%.3f  recupera %.1f = %.2f%%"
          % (c_conj, rec_conj, 100.0 * rec_conj / castigo), flush=True)
    for n in ing:
        print("      %-6s %.6f  (algebraico %.6f)" % (n, p_conj[n], BASE[n]),
              flush=True)

    out = dict(
        corrida="control del punto de fuga v2, corrido PRIMERO + prueba conjunta",
        motivo="objecion de M. Almeida: el control iba al final, y de uno en "
               "uno no se ven las combinaciones",
        referencia_chi2=chi2_ref, base_chi2=chi2_base, castigo=castigo,
        A_control=dict(criterio="soltar solo logA recupera >95% del castigo",
                       chi2=c_ctrl, logA=p_ctrl["logA"], tau=p_ctrl["tau"],
                       recupera=rec_ctrl, recupera_pct=pct_ctrl, pasa=ok),
        B_conjunto=dict(libres=ing, chi2=c_conj, recupera=rec_conj,
                        recupera_pct=100.0 * rec_conj / castigo,
                        mejor=p_conj,
                        nota="comparar con la SUMA de los individuales de "
                             "cmb_punto_de_fuga2.json: si el conjunto recupera "
                             "mucho mas, el reparto de uno en uno cuenta de menos"),
        segundos=time.time() - t0)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(out, indent=1))
    print("\nescrito -> %s" % SALIDA.relative_to(REPO), flush=True)


if __name__ == "__main__":
    main()
