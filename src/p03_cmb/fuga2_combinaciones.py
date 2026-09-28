"""Punto de fuga, TODAS las combinaciones — 15 subconjuntos, no cuatro sueltos.

POR QUE (M. Almeida, 2026-09-08). El barrido de uno en uno mide cuanto calla
cada ingrediente por su cuenta, y de ahi se cae en la tentacion de SUMAR. Sumar
no vale: el universo no tiene componentes que actuen por separado, se empujan
entre ellos. Dos que a solas callan poco pueden callar mucho juntos porque se
compensan; o al reves, el castigo puede repartirse entre todos sin que ninguno
lo absorba. Solo con las combinaciones completas se puede decir DONDE se
amortigua y DONDE se castiga.

QUE HACE. Con la amplitud primordial CLAVADA en el valor que piden las sondas
tardias, se sueltan los 4 ingredientes del fondo en los 15 subconjuntos no
vacios (4 solos + 6 parejas + 4 tercias + 1 con los cuatro), y se mide cuanto
del castigo recupera cada subconjunto. `tau` (la niebla) esta libre SIEMPRE,
en la base y en cada combinacion — sin eso la base sale rota, que es el fallo
que invalido la v1.

SINERGIA. Para cada subconjunto se compara lo que recupera contra la SUMA de
lo que recuperan sus miembros por separado:
    sinergia = recupera(conjunto) - suma(recupera(individuales))
  > 0  se empujan a favor: juntos callan mas que la suma de sus partes
  ~ 0  actuan por separado, ahi sumar SI valdria
  < 0  se estorban: uno deshace lo que el otro consigue

CONTROL (R24), y va PRIMERO. Se suelta SOLO la amplitud, que es el parametro
clavado y por tanto el culpable directo: debe recuperar >95% del castigo. Si no
lo recupera, la maquina no mide ingredientes sino al optimizador, y se aborta
sin gastar el resto. (Ya paso al 100.0% en `cmb_punto_de_fuga2.json`; se repite
aqui porque el control tiene que vivir en la misma corrida que lo que valida.)

LO QUE ESTO **NO** ES, y hay que decirlo al reportarlo (M. Almeida): el reparto
que salga esta comprometido con lo que PREFIERE ESTE DATO. Es el fondo cosmico
quien reparte el castigo aqui. Con BOSS al lado, los ingredientes tiran hacia
otros sitios, porque cada sonda prefiere los suyos. Esto mide cuanto castiga el
fondo cosmico y quien lo absorbe, no cual es el ingrediente culpable en
absoluto.

FUENTE: results/logs/cmb_fuga2_combinaciones.json
"""
import itertools
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

SALIDA = REPO / "results" / "logs" / "cmb_fuga2_combinaciones.json"

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
ING = ["ombh2", "omch2", "H0", "ns"]

LIM = {"ombh2": (0.005, 0.100), "omch2": (0.001, 0.300),
       "H0": (40.0, 90.0), "ns": (0.500, 1.500),
       "logA": (1.0, 5.0), "tau": (0.010, 0.200)}
SIG = {"ombh2": 0.00015, "omch2": 0.0012, "H0": 0.54, "ns": 0.0042}


def optimiza(fijos, libres):
    x0 = [BASE[n] for n in libres]
    lim = [LIM[n] for n in libres]
    # mas dimensiones piden mas iteraciones, si no el minimo sale corto y la
    # combinacion parece peor de lo que es — sesgaria justo la sinergia
    it = 600 + 700 * len(libres)

    def f(u):
        if any(not (a < v < b) for v, (a, b) in zip(u, lim)):
            return 1e30
        return chi2_y_s8(dict(fijos, **{n: v for n, v in zip(libres, u)}),
                         W, WA)[0]
    r = minimize(f, x0, method="Nelder-Mead",
                 options=dict(xatol=1e-6, fatol=1e-3, maxiter=it))
    return float(r.fun), {n: float(v) for n, v in zip(libres, r.x)}


def main():
    t0 = time.time()
    fondo = {k: BASE[k] for k in ING}

    chi2_ref, _ = optimiza(fondo, ["logA", "tau"])
    print("referencia (todo en su sitio, logA y tau libres) = %.3f"
          % chi2_ref, flush=True)

    chi2_base, _ = optimiza(dict(fondo, logA=LOGA_TARDE), ["tau"])
    castigo = chi2_base - chi2_ref
    print("base (logA clavado en %.4f)                     = %.3f"
          % (LOGA_TARDE, chi2_base), flush=True)
    print("CASTIGO                                          = %.3f\n"
          % castigo, flush=True)

    # ── CONTROL PRIMERO (R24) ───────────────────────────────────────────
    c_ctrl, p_ctrl = optimiza(fondo, ["tau", "logA"])
    pct_ctrl = 100.0 * (castigo - (c_ctrl - chi2_ref)) / castigo
    print("CONTROL: soltar solo logA recupera %.2f%% (criterio >95%%) -> %s\n"
          % (pct_ctrl, "PASA" if pct_ctrl > 95.0 else "FALLA"), flush=True)
    if pct_ctrl <= 95.0:
        SALIDA.write_text(json.dumps(dict(
            control=dict(pasa=False, recupera_pct=pct_ctrl),
            veredicto="sin control no hay medida: abortado"), indent=1))
        return

    # ── LOS 15 SUBCONJUNTOS ─────────────────────────────────────────────
    res = {}
    subs = [c for n in range(1, len(ING) + 1)
            for c in itertools.combinations(ING, n)]
    print("%-28s %10s %8s %s" % ("combinacion", "chi2", "recupera", "valores"),
          flush=True)
    for cb in subs:
        fj = dict(logA=LOGA_TARDE)
        fj.update({k: BASE[k] for k in ING if k not in cb})
        c, p = optimiza(fj, ["tau"] + list(cb))
        rec = castigo - (c - chi2_ref)
        res["+".join(cb)] = dict(
            libres=list(cb), chi2=c, recupera=rec,
            recupera_pct=100.0 * rec / castigo,
            valores={n: p[n] for n in cb},
            sigmas={n: (p[n] - BASE[n]) / SIG[n] for n in cb},
            tau=p["tau"])
        print("%-28s %10.3f %7.1f%% %s"
              % ("+".join(cb), c, 100.0 * rec / castigo,
                 " ".join("%s=%+.1fsig" % (n, (p[n] - BASE[n]) / SIG[n])
                          for n in cb)), flush=True)

    # ── SINERGIA: conjunto contra la suma de sus partes ─────────────────
    print("\n%-28s %10s %10s %10s"
          % ("combinacion", "recupera", "suma", "sinergia"), flush=True)
    for k, v in res.items():
        if len(v["libres"]) == 1:
            continue
        suma = sum(res[n]["recupera"] for n in v["libres"])
        v["suma_individuales"] = suma
        v["sinergia"] = v["recupera"] - suma
        print("%-28s %10.1f %10.1f %+10.1f"
              % (k, v["recupera"], suma, v["sinergia"]), flush=True)

    out = dict(
        corrida="punto de fuga — 15 combinaciones, con sinergia",
        motivo="M. Almeida: sumar no vale; los componentes se empujan entre "
               "ellos, hay que ver todas las combinaciones",
        logA_tarde=LOGA_TARDE, referencia_chi2=chi2_ref,
        base_chi2=chi2_base, castigo=castigo,
        control=dict(criterio="soltar solo logA recupera >95%",
                     recupera_pct=pct_ctrl, pasa=True),
        combinaciones=res,
        alcance="el reparto esta comprometido con lo que prefiere ESTE dato "
                "(el fondo cosmico). Con BOSS al lado los ingredientes tiran "
                "hacia otros sitios. Esto mide cuanto castiga el CMB y quien "
                "lo absorbe, no cual es el culpable en absoluto",
        segundos=time.time() - t0)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(out, indent=1))
    print("\nescrito -> %s" % SALIDA.relative_to(REPO), flush=True)


if __name__ == "__main__":
    main()
