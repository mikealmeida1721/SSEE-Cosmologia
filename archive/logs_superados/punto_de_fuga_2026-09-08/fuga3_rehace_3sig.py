"""Rehace SOLO la columna `3sig` de un barrido `fuga3`, con el simplex arreglado.

POR QUE. En `cmb_fuga3_kids.json` cinco de las quince filas daban un chi2 PEOR
que el punto de partida. Un minimizador con cotas que arranca DENTRO de la caja
no puede hacer eso nunca, asi que no era fisica: era el minimizador.

LA CAUSA, medida. Nelder-Mead, sin simplex explicito, perturba cada coordenada
un 5% de SU VALOR. En unidades de sigma de Planck ese 5% vale:

    ombh2  7.5 sigma      omch2  5.0 sigma
    H0     6.3 sigma      ns    11.5 sigma

o sea que en modo `3sig` TODOS los vertices del simplex inicial menos x0 caen
FUERA de la caja, donde `f` devuelve 1e30. El simplex nace degenerado. **No son
cinco filas malas: es la columna entera**, incluidas las que salian con pinta
razonable. Se tira completa y se rehace.

La columna `libre` NO esta afectada: sus cotas son LIM, anchas, y el 5% cae
dentro. Se conserva tal cual y se copia.

ARREGLO. `paso_simplex` en `fuga3_por_As.py`: en modo `3sig` el paso es 1 sigma,
holgado dentro de la caja de 3. Mas un control gratis que devuelve el punto de
partida si el minimizador acaba peor que el.

USO:  python fuga3_rehace_3sig.py <boss|kids|fondo|promedio>
SALIDA: results/logs/cmb_fuga3_<etq>_3sig_rehecho.json
"""
import itertools
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "p03_cmb"))

import fuga3_por_As as F                                  # noqa: E402


def main():
    etq = sys.argv[1] if len(sys.argv) > 1 else "kids"
    viejo = REPO / "results" / "logs" / ("cmb_fuga3_%s.json" % etq)
    salida = REPO / "results" / "logs" / ("cmb_fuga3_%s_3sig_rehecho.json" % etq)
    d = json.loads(viejo.read_text())

    loga = d['logA_clavado']
    chi2_ref = d['chi2_referencia']
    castigo = d['castigo']
    base = {k: F.BASE[k] for k in F.ING}
    t0 = time.time()

    print("=== rehace 3sig · %s · logA=%.6f · castigo=%.2f" % (etq, loga, castigo))
    print("    chi2 en el punto de partida (todo algebraico) = %.3f"
          % (chi2_ref + castigo), flush=True)

    # ── CONTROL PRIMERO (R24): el simplex nuevo cabe en la caja ──────────
    print("\n  paso del simplex en modo 3sig, en sigmas de Planck:", flush=True)
    ok0 = True
    for n in F.ING:
        s = F.paso_simplex(n, "3sig") / F.SIG[n]
        ok0 &= bool(s < F.N_SIG)
        print("    %-6s %.2f sigma  -> %s" % (n, s,
              "cabe" if s < F.N_SIG else "NO CABE"), flush=True)
    print("  CONTROL simplex: %s" % ("PASA" if ok0 else "FALLA"), flush=True)
    if not ok0:
        raise SystemExit("el simplex sigue sin caber; no se mide nada")

    subs = [c for n in range(1, len(F.ING) + 1)
            for c in itertools.combinations(F.ING, n)]
    res, fallos = {}, []
    print("\n  %-22s %10s %9s  %s" % ("combinacion", "chi2", "absorbe", "sigmas"),
          flush=True)
    for cb in subs:
        fj = dict(logA=loga)
        fj.update({k: base[k] for k in F.ING if k not in cb})
        c, p, ok = F.optimiza(fj, ["tau"] + list(cb), "3sig")
        gana = castigo - (c - chi2_ref)
        sig = {n: (p[n] - base[n]) / F.SIG[n] for n in cb}
        peg = [n for n in cb if abs(abs(sig[n]) - F.N_SIG) < 0.02]
        if not ok:
            fallos.append("+".join(cb))
        res["+".join(cb)] = dict(
            chi2=float(c), gana=float(gana),
            gana_pct=float(100.0 * gana / castigo),
            minimizador_ok=bool(ok),
            valores={n: float(p[n]) for n in cb},
            sigmas={n: float(v) for n, v in sig.items()},
            pegado_al_borde=peg, tau=float(p["tau"]))
        print("  %-22s %10.2f %8.1f%%  %s%s%s" % (
            "+".join(cb), c, 100.0 * gana / castigo,
            " ".join("%s=%+.1f" % (n, v) for n, v in sig.items()),
            ("  PEGADO:" + ",".join(peg)) if peg else "",
            "   <-- MINIMIZADOR FALLA" if not ok else ""), flush=True)

    mejor = max(res.items(), key=lambda t: t[1]['gana_pct'])

    # CONTROL DE ANIDAMIENTO (R53): un conjunto no puede absorber menos que un
    # subconjunto suyo. Si lo hace, fallo el minimizador y esas filas NO se leen.
    anid = F.revisa_anidamiento(res)
    rotas = sorted({v['conjunto'] for v in anid})
    print("\n  CONTROL DE ANIDAMIENTO -> %s" % (
        "PASA" if not anid else "FALLA en %d filas de %d (%d pares)"
        % (len(rotas), len(res), len(anid))), flush=True)
    for v in anid:
        print("    x %-22s %7.1f%%  <  %-16s %7.1f%%" % (
            v['conjunto'], v['gana_pct'], v['subconjunto'],
            v['gana_pct_subconjunto']), flush=True)
    salida.write_text(json.dumps(dict(
        corrida="rehace la columna 3sig de fuga3 con el simplex arreglado",
        etiqueta=etq, logA_clavado=loga, chi2_referencia=chi2_ref,
        chi2_base=chi2_ref + castigo, castigo=castigo,
        motivo="el simplex inicial por defecto de Nelder-Mead (5% del valor) "
               "cae entre 5 y 11.5 sigma fuera de la caja de 3 sigma; la "
               "columna 3sig entera del JSON viejo se retira",
        arreglo="paso_simplex = 1 sigma en modo 3sig + control de no-empeorar",
        control_simplex_cabe=bool(ok0),
        filas_con_minimizador_fallando=fallos,
        control_anidamiento=dict(
            regla="un conjunto de libres no puede absorber menos que un "
                  "subconjunto suyo: puede dejar los extras quietos y repetirlo",
            pasa=bool(not anid), filas_rotas=rotas,
            violaciones=anid),
        subconjuntos_3sig=res,
        mejor=dict(nombre=mejor[0], gana_pct=mejor[1]['gana_pct'],
                   chi2=mejor[1]['chi2']),
        columna_libre="sin tocar; vive en cmb_fuga3_%s.json y NO esta afectada"
                      % etq,
        alcance="informacion sobre que ingredientes se empujan entre si. NO "
                "senala culpables ni toca ningun paper",
        segundos=time.time() - t0), indent=1, default=float))
    print("\n  MEJOR con 3 sigma: %s absorbe %.1f%% (chi2 %.2f)"
          % (mejor[0], mejor[1]['gana_pct'], mejor[1]['chi2']), flush=True)
    print("  filas donde el minimizador aun falla: %s"
          % (", ".join(fallos) if fallos else "ninguna"), flush=True)
    print("\nescrito -> %s  (%.2f h)"
          % (salida.relative_to(REPO), (time.time() - t0) / 3600), flush=True)


if __name__ == "__main__":
    main()
