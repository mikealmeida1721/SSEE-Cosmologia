"""El mismo barrido, pero contra CADA A_s por separado — no contra el promedio.

DE DONDE VIENE (M. Almeida, 2026-09-08). El barrido anterior clava el A_s en el
PROMEDIO de KiDS y BOSS. Mike señalo dos cosas contra eso:

  (1) «no es que tengas 2 A_s, sino 3, de datos diferentes, porque A_s es
      LIBRE». Cada sonda prefiere el suyo: BOSS 2.7636, KiDS 2.8627, el propio
      fondo cosmico 3.0448. Promediarlos fabrica un cuarto valor que no lo
      prefiere nadie, y encima estrecha la barra: la deriva pasa de 2.87 sigma
      (BOSS sola) y 3.59 (KiDS sola) a 4.50 al promediar. Ese salto lo pone el
      promedio, no un dato nuevo.

  (2) «lo que salga es solo informacion para entender cuales ingredientes
      interactuan entre ellos». O sea que el barrido no busca culpables: busca
      el mapa de quien se empuja con quien. Y ese mapa puede ser DISTINTO segun
      que A_s se clave — que es justo lo que aqui se mide.

QUE HACE. El mismo motor: se clava logA, `tau` queda libre SIEMPRE, y se
sueltan los 4 ingredientes del fondo en los 15 subconjuntos no vacios. Lo unico
que cambia entre corridas es EN QUE VALOR se clava logA.

LA VEROSIMILITUD SIGUE SIENDO LA DEL FONDO COSMICO en las tres. O sea que la
pregunta es: «clavando el A_s que prefiere ESA sonda, ¿el fondo cosmico sigue
queriendo los ingredientes algebraicos, o quiere otros?». (La otra lectura
posible —evaluar la verosimilitud de BOSS en vez de la del CMB— es otra corrida
distinta, y no es esta; se dice aqui para que nadie la confunda.)

EL CONTROL SALE GRATIS Y ES EL CASO `fondo` (R53). Clavando logA en el valor que
el propio fondo cosmico prefiere, el castigo es CERO por construccion. Entonces
lo que se mueva ahi es lo que los ingredientes querian mover DE TODAS FORMAS,
sin ninguna deriva que absorber. Restando ese fondo se separa el movimiento
causado por la deriva del movimiento que el dato pide igualmente. Sin ese caso,
todo porcentaje de los otros dos esta sin cero.

LAS DOS COTAS, y por que van las dos (M. Almeida). `libre` deja al optimizador
correr entre cotas numericas: recupera mucho, pero comprando ω_c a -21 sigma.
`3sig` acota cada ingrediente a +-3 sigma de Planck. Un porcentaje de la primera
mide la GEOMETRIA de la verosimilitud; uno de la segunda mide lo que se puede
absorber SIN salirse de lo que el propio dato permite. Se calculan las dos en la
misma pasada para que cada fila lleve su precio al lado.

USO:  python fuga3_por_As.py <boss|kids|fondo|promedio>

FUENTE: results/logs/cmb_fuga3_<etiqueta>.json
"""
import itertools
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

BASE = dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2,
            H0=S.H0_GLOBAL, ns=S.N_S, logA=3.044, tau=0.054)
W, WA = S.W0, S.WA
ING = ["ombh2", "omch2", "H0", "ns"]

# Los TRES A_s, cada uno con su procedencia. Ninguno es un promedio.
LOGA = {
    "boss": (2.7636396611, 0.0981316176,
             "results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json (ssee)"),
    "kids": (2.8627107489, 0.0507836451,
             "results/logs/growth_2026-07/R3_ssee_kids_S8.json"),
    "fondo": (3.0448, None,
              "results/logs/cmb_dbic_tau_ajustado.json (SSEE.mejor.logA) "
              "— CONTROL: castigo cero por construccion"),
    # ORIGEN-VALOR: 0.0451 — inversa-varianza de boss (0.0981316) y kids (0.0507836) de arriba: 2.84178 +- 0.045102
    "promedio": (2.8418, 0.0451,
                 "combinacion inversa-varianza de los dos de arriba; se "
                 "conserva solo para comparar con la corrida vieja"),
}

LIM = {"ombh2": (0.005, 0.100), "omch2": (0.001, 0.300),
       "H0": (40.0, 90.0), "ns": (0.500, 1.500),
       "logA": (1.0, 5.0), "tau": (0.010, 0.200)}
SIG = {"ombh2": 0.00015, "omch2": 0.0012, "H0": 0.54, "ns": 0.0042}
N_SIG = 3.0


def cotas(n, modo):
    if modo == "3sig" and n in SIG:
        return (BASE[n] - N_SIG * SIG[n], BASE[n] + N_SIG * SIG[n])
    return LIM[n]


def paso_simplex(n, modo):
    """Paso de cada arista del simplex INICIAL.

    ARREGLADO 2026-09-10. Nelder-Mead, si no le das simplex, perturba cada
    coordenada un 5% de SU VALOR. Para estos ingredientes ese 5% vale entre 5 y
    11 sigma de Planck (ns: 11.5), o sea que en modo `3sig` TODOS los vertices
    menos x0 caen FUERA de la caja, donde `f` devuelve 1e30: el simplex nace
    degenerado y el minimizador devuelve basura. Se vio porque cinco filas
    daban un chi2 PEOR que el punto de partida, y un minimizador con cotas que
    arranca dentro de la caja no puede hacer eso nunca.
    """
    if modo == "3sig" and n in SIG:
        return SIG[n]                      # 1 sigma: holgado dentro de la de 3
    return 0.05 * abs(BASE[n]) if BASE[n] else 2.5e-4


def optimiza(fijos, libres, modo):
    x0 = np.array([BASE[n] for n in libres], float)
    lim = [cotas(n, modo) for n in libres]
    it = 600 + 700 * len(libres)

    def f(u):
        if any(not (a < v < b) for v, (a, b) in zip(u, lim)):
            return 1e30
        return chi2_y_s8(dict(fijos, **{n: v for n, v in zip(libres, u)}),
                         W, WA)[0]

    pasos = np.array([paso_simplex(n, modo) for n in libres])
    sim = np.vstack([x0] + [x0 + np.eye(len(x0))[i] * pasos[i]
                            for i in range(len(x0))])
    r = minimize(f, x0, method="Nelder-Mead",
                 options=dict(xatol=1e-6, fatol=1e-3, maxiter=it,
                              initial_simplex=sim))
    # CONTROL GRATIS (R53): un minimizador que arranca DENTRO de la caja no
    # puede devolver algo peor que su punto de partida. Si lo hace, fallo.
    f0 = float(f(x0))
    if not np.isfinite(r.fun) or r.fun > f0:
        return f0, {n: float(v) for n, v in zip(libres, x0)}, False
    return float(r.fun), {n: float(v) for n, v in zip(libres, r.x)}, True


def revisa_anidamiento(res, tol=0.05):
    """CONTROL DE ANIDAMIENTO (R53) — instalado 2026-09-11, lo pidio Mike.

    LA REGLA. Un conjunto de ingredientes libres NO PUEDE absorber menos que un
    subconjunto suyo. Siempre puede dejar los ingredientes de mas en su valor de
    partida y repetir exactamente lo que consiguio el subconjunto. Si sale
    menos, el que fallo es el MINIMIZADOR, no la fisica.

    POR QUE HACIA FALTA OTRO CONTROL. El control gratis de `optimiza()` compara
    `r.fun` contra `f(x0)`, su propio punto de partida. Pero el `chi2_base` con
    el que se calcula `gana` se midio con `tau` YA ajustado, asi que
    `f(x0) > chi2_base` y un resultado peor que `chi2_base` pasaba igual. Este
    control no necesita ninguna vara externa: compara las filas ENTRE SI, y la
    aritmetica sola delata el fallo.

    PROBADO CONTRA EL DATO DEFECTUOSO: sobre
    `results/logs/cmb_fuga3_kids_3sig_rehecho.json` caza 8 de 15 filas que el
    control anterior dejo pasar (p.ej. `omch2+H0` absorbe -13.9% cuando `H0`
    solo absorbe 2.4%).

    res : dict {"omch2+H0": {"gana_pct": ...}, ...}
    tol : margen de ruido del optimizador, en puntos porcentuales.
    Devuelve la lista de violaciones, la peor primero. Lista vacia = PASA.
    """
    viol = []
    for nom, d in res.items():
        cj = frozenset(nom.split("+"))
        for otro, e in res.items():
            so = frozenset(otro.split("+"))
            if so < cj and e["gana_pct"] > d["gana_pct"] + tol:
                viol.append(dict(conjunto=nom, gana_pct=float(d["gana_pct"]),
                                 subconjunto=otro,
                                 gana_pct_subconjunto=float(e["gana_pct"]),
                                 deficit=float(e["gana_pct"] - d["gana_pct"])))
    viol.sort(key=lambda v: -v["deficit"])
    return viol


def main():
    etq = sys.argv[1] if len(sys.argv) > 1 else "boss"
    if etq not in LOGA:
        raise SystemExit("etiqueta desconocida: %s (usa %s)"
                         % (etq, "|".join(LOGA)))
    loga, sig_loga, proc = LOGA[etq]
    salida = REPO / "results" / "logs" / ("cmb_fuga3_%s.json" % etq)

    t0 = time.time()
    fondo = {k: BASE[k] for k in ING}
    print("=== A_s clavado: %s   logA = %.6f" % (etq.upper(), loga))
    print("    procedencia: %s\n" % proc, flush=True)

    chi2_ref, _, _ = optimiza(fondo, ["logA", "tau"], "libre")
    chi2_base, _, _ = optimiza(dict(fondo, logA=loga), ["tau"], "libre")
    castigo = chi2_base - chi2_ref
    print("referencia (logA y tau libres) = %.3f" % chi2_ref)
    print("base (logA clavado)            = %.3f" % chi2_base)
    print("CASTIGO                        = %.3f" % castigo, flush=True)

    # Si el castigo es ~0 (el caso `fondo`), los porcentajes no significan
    # nada: se reporta el Δχ² ABSOLUTO que gana cada subconjunto.
    en_pct = castigo > 1.0
    if not en_pct:
        print("    castigo ~ 0: este es el CONTROL. Se reporta Δchi2 absoluto,")
        print("    o sea lo que los ingredientes mueven SIN deriva que absorber.",
              flush=True)

    # ── CONTROL PRIMERO (R24) ───────────────────────────────────────────
    if en_pct:
        c_ctrl, _, _ = optimiza(fondo, ["tau", "logA"], "libre")
        pct = 100.0 * (castigo - (c_ctrl - chi2_ref)) / castigo
        print("\nCONTROL: soltar solo logA recupera %.2f%% (criterio >95%%) -> %s"
              % (pct, "PASA" if pct > 95.0 else "FALLA"), flush=True)
        if pct <= 95.0:
            salida.write_text(json.dumps(dict(
                etiqueta=etq, logA=loga,
                control=dict(pasa=False, recupera_pct=pct),
                veredicto="sin control no hay medida: abortado"), indent=1))
            return
    else:
        pct = None

    # ── LOS 15 SUBCONJUNTOS, con las DOS cotas ──────────────────────────
    res = {}
    subs = [c for n in range(1, len(ING) + 1)
            for c in itertools.combinations(ING, n)]
    print("\n%-24s %10s %9s %10s %9s"
          % ("combinacion", "chi2 libre", "gana", "chi2 3sig", "gana"),
          flush=True)
    for cb in subs:
        fila = dict(libres=list(cb))
        for modo in ("libre", "3sig"):
            fj = dict(logA=loga)
            fj.update({k: BASE[k] for k in ING if k not in cb})
            c, p, ok = optimiza(fj, ["tau"] + list(cb), modo)
            gana = castigo - (c - chi2_ref)
            fila[modo] = dict(
                chi2=c, gana=gana, minimizador_ok=bool(ok),
                gana_pct=(100.0 * gana / castigo) if en_pct else None,
                valores={n: p[n] for n in cb},
                sigmas={n: (p[n] - BASE[n]) / SIG[n] for n in cb},
                pegado_al_borde=[n for n in cb
                                 if abs(abs(p[n] - BASE[n]) / SIG[n] - N_SIG)
                                 < 0.02] if modo == "3sig" else [],
                tau=p["tau"])
        res["+".join(cb)] = fila
        f_l, f_3 = fila["libre"], fila["3sig"]
        u = "%7.1f%%" if en_pct else "%9.1f"
        print(("%-24s %10.3f " + u + " %10.3f " + u)
              % ("+".join(cb), f_l["chi2"],
                 f_l["gana_pct"] if en_pct else f_l["gana"],
                 f_3["chi2"], f_3["gana_pct"] if en_pct else f_3["gana"]),
              flush=True)
        print("      libre: %s" % " ".join(
            "%s=%+.1fsig" % (n, v) for n, v in f_l["sigmas"].items()), flush=True)
        print("      3sig : %s%s" % (
            " ".join("%s=%+.1fsig" % (n, v) for n, v in f_3["sigmas"].items()),
            ("   PEGADO: " + ",".join(f_3["pegado_al_borde"]))
            if f_3["pegado_al_borde"] else ""), flush=True)

    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(dict(
        corrida="barrido de 15 subconjuntos con el A_s de UNA sonda, no del promedio",
        idea="M. Almeida — hay TRES A_s, uno por dato, porque A_s es libre; "
             "y el mapa de que ingredientes se empujan puede cambiar con cual "
             "se clave",
        etiqueta=etq, logA_clavado=loga, sigma_del_logA=sig_loga,
        procedencia=proc,
        verosimilitud="fondo cosmico (plik_lite TTTEEE + lowT + lowE) en los "
                      "tres casos; lo unico que cambia es el A_s clavado",
        chi2_referencia=chi2_ref, chi2_base=chi2_base, castigo=castigo,
        es_control=not en_pct,
        control_solo_logA_pct=pct,
        cotas=dict(libre="numericas (LIM) — mide la GEOMETRIA",
                   tres_sigma="BASE +- 3 sigma de Planck — mide lo absorbible "
                              "SIN salirse de lo que el dato permite",
                   N_SIG=N_SIG),
        subconjuntos=res,
        alcance="informacion sobre que ingredientes se empujan entre si bajo "
                "un A_s dado. NO senala culpables ni toca ningun paper",
        segundos=time.time() - t0), indent=1))
    print("\nescrito -> %s" % salida.relative_to(REPO), flush=True)


if __name__ == "__main__":
    main()
