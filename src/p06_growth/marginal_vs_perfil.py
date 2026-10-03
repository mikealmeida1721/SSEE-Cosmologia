"""¿La media marginal de KiDS esta sesgada por VOLUMEN? (lo pidio Mike)

LA PREGUNTA REAL. Todo el lio del A_s de BOSS resulto ser de ESTIMADOR: media
marginal 2.7636 contra minimo del perfil 2.9448. Pero Mike puso el dedo donde
importa: **BOSS no mide A_s de todos modos** (D=4.01), y la tension que si nos
interesa es **KiDS contra el fondo cosmico**. Asi que la pregunta que vale no es
cual estimador usar en BOSS, sino:

    ¿los DOS numeros de esa tension estan medidos con la MISMA regla?

Verificado leyendo los logs, y NO lo estan:
    CMB   3.0448  = `SSEE/mejor/logA` de una MINIMIZACION  -> es un PERFIL
    KiDS  2.8627  = `logA/media` de una cadena MCMC        -> es una MARGINAL

Si la marginal de KiDS arrastra sesgo de volumen, la tension KiDS-CMB (cmb_quien_mide_As.json) esta medida
con dos varas distintas, igual que lo estaba el 0.81 de BOSS.

COMO SE MIDE, SIN CORRER NADA NUEVO. La cadena ya guarda el chi2 de cada punto.
Se compara la media marginal contra el logA del MEJOR punto de la cadena. Si el
volumen empuja, la media se aparta del mejor ajuste; si no hay volumen que
empuje, coinciden. El mejor punto no es el minimo exacto (una cadena muestrea el
bulto, no la punta) pero con d chico el hueco esperado es minusculo, y ese hueco
se calcula y se declara, no se supone.

CONTROL (R53, y va PRIMERO por R24). La misma medida sobre **BOSS**, donde el
desplazamiento YA esta medido por otra via (0.1811 entre marginal y perfil, con
D=4.01). Si el diagnostico no ve nada en BOSS, no sirve para absolver a KiDS.
    criterio: en BOSS el diagnostico debe ver un hueco > 0.05 (mitad del sigma
    de BOSS). Si no lo ve, se aborta y no se lee la fila de KiDS.

FUENTE: results/logs/growth_2026-07/marginal_vs_perfil.json
"""
# ORIGEN-VALOR: 0.1811 — desplazamiento marginal-perfil, results/logs/growth_2026-07/marginal_vs_perfil.json
import json
import pathlib

import numpy as np
from scipy import stats

REPO = pathlib.Path(__file__).resolve().parents[2]
CAD = pathlib.Path("/mnt/datos/SSEE_data/chains_p6")
SALIDA = REPO / "results" / "logs" / "growth_2026-07" / "marginal_vs_perfil.json"

# El hueco que el CONTROL tiene que ver para que la prueba valga.
UMBRAL_CONTROL = 0.05

CASOS = {
    "boss": dict(dir=CAD / "boss", pref="ssee", papel="CONTROL — aqui SI hay "
                 "desplazamiento medido por otra via (perfil - marginal = 0.1811)",
                 # leidos de R1R2_boss_lpt_cobaya.json (2026-10-02; antes tecleados: 2.7636 era la cadena vieja)
                 publicado=json.load(open(REPO / "results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json"))["ssee"]["logA"],
                 perfil_conocido=json.load(open(REPO / "results/logs/growth_2026-07/"
                                                "R1R2_boss_lpt_cobaya.json"))["perfil_vs_marginal"]["perfil_logA"]),
    "kids": dict(dir=CAD / "kids", pref="ssee", papel="la fila que importa: una "
                 "de las dos mitades de la tension KiDS-CMB (cmb_quien_mide_As.json)",
                 publicado=json.load(open(REPO / "results/logs/growth_2026-07/"
                                          "R3_ssee_kids_S8_rehecho.json"))["logA"]["media"],
                 perfil_conocido=None),
}


def lee(d, pref):
    """Junta las 4 cadenas. Devuelve (peso, logA, chi2) y el burn-in aplicado.

    El burn-in del 30% es el mismo que uso el analisis publicado (R3 declara
    `burn_in_frac: 0.3`), asi que la media marginal que salga aqui tiene que
    reproducir la publicada — y eso es en si una comprobacion de que estoy
    leyendo bien el fichero.
    """
    ws, xs, cs = [], [], []
    for f in sorted(d.glob(f"{pref}.[0-9].txt")):
        cab = open(f).readline().lstrip("#").split()
        a = np.loadtxt(f)
        if a.ndim == 1:
            a = a[None, :]
        n0 = int(0.3 * len(a))
        a = a[n0:]
        ws.append(a[:, cab.index("weight")])
        xs.append(a[:, cab.index("logA")])
        cs.append(a[:, cab.index("chi2")])
    return np.concatenate(ws), np.concatenate(xs), np.concatenate(cs)


def mide(w, x, c, d_muestreadas):
    """Media marginal (con pesos) contra el logA del mejor punto de la cadena."""
    med = float(np.average(x, weights=w))
    sig = float(np.sqrt(np.average((x - med) ** 2, weights=w)))
    i = int(np.argmin(c))
    mejor = float(x[i])
    n = float(w.sum())
    # Cuanto Dchi2 por encima del minimo real cabe esperar del mejor punto de
    # n muestras en d dimensiones. Si el hueco medido es de ese orden, el mejor
    # punto es un proxy honesto del minimo del perfil.
    hueco = float(stats.chi2.ppf(1.0 / n, d_muestreadas))
    return dict(marginal=med, sigma=sig, mejor_punto=mejor,
                desplazamiento=mejor - med,
                en_sigmas=(mejor - med) / sig if sig else None,
                chi2_mejor=float(c[i]), n_efectivo=n,
                d_muestreadas=d_muestreadas,
                dchi2_esperado_del_mejor=hueco)


def main():
    res = {}
    for nom, cfg in CASOS.items():
        w, x, c = lee(cfg["dir"], cfg["pref"])
        d = 19 if nom == "boss" else 9        # BOSS: logA + (b1,b2,bs)x6 ; KiDS: 9 libres
        r = mide(w, x, c, d)
        r["papel"] = cfg["papel"]
        r["publicado"] = cfg["publicado"]
        r["reproduce_publicado"] = abs(r["marginal"] - cfg["publicado"]) < 5e-3
        if cfg["perfil_conocido"]:
            r["perfil_conocido"] = cfg["perfil_conocido"]
            r["perfil_menos_marginal"] = cfg["perfil_conocido"] - r["marginal"]
        res[nom] = r
        print("\n=== %s · %s" % (nom.upper(), cfg["papel"]))
        print("    media marginal     = %.5f +- %.5f   (publicado %.5f  %s)"
              % (r["marginal"], r["sigma"], cfg["publicado"],
                 "REPRODUCE" if r["reproduce_publicado"] else "NO REPRODUCE"))
        print("    mejor punto        = %.5f   (chi2 = %.3f)"
              % (r["mejor_punto"], r["chi2_mejor"]))
        print("    desplazamiento     = %+.5f  = %+.2f sigma"
              % (r["desplazamiento"], r["en_sigmas"]))
        print("    Dchi2 esperado del mejor de %.0f muestras con d=%d: %.2f"
              % (r["n_efectivo"], d, r["dchi2_esperado_del_mejor"]))

    # --- CONTROL PRIMERO (R24) --------------------------------------------
    ctrl = abs(res["boss"]["desplazamiento"])
    pasa = ctrl > UMBRAL_CONTROL
    print("\n" + "=" * 70)
    print("  CONTROL: el diagnostico ve el desplazamiento conocido de BOSS?")
    print("     |desplazamiento BOSS| = %.5f   (criterio > %.2f)  ->  %s"
          % (ctrl, UMBRAL_CONTROL, "PASA" if pasa else "FALLA"))
    print("=" * 70, flush=True)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    sal = dict(
        corrida="la media marginal de KiDS, sesgada por volumen?",
        pregunta="M. Almeida — BOSS no mide A_s igual; lo que hay que resolver "
                 "es KiDS contra el fondo, asi que la pregunta es si ESOS dos "
                 "estan medidos con la misma regla",
        hallazgo_previo=dict(
            cmb="3.0448 sale de SSEE/mejor/logA de una MINIMIZACION -> PERFIL",
            kids="el logA de KiDS sale de logA/media de una cadena MCMC -> MARGINAL",
            log_cmb="results/logs/cmb_dbic_tau_ajustado.json",
            log_kids="results/logs/growth_2026-07/R3_ssee_kids_S8_rehecho.json"),
        control=dict(criterio="ve el desplazamiento conocido de BOSS (>%.2f)"
                     % UMBRAL_CONTROL, medido=ctrl, pasa=bool(pasa)),
        casos=res,
        alcance="mide si la media marginal se aparta del mejor ajuste. NO "
                "sustituye a la cola #23 (dato sintetico con la verdad "
                "conocida), que es la unica que dice cual estimador es INSESGADO")
    if not pasa:
        sal["veredicto"] = ("el diagnostico no ve el desplazamiento que YA se "
                            "sabe que existe en BOSS: no absuelve a KiDS")
        SALIDA.write_text(json.dumps(sal, indent=1))
        print("\nescrito -> %s" % SALIDA.relative_to(REPO), flush=True)
        return

    k = res["kids"]
    sal["veredicto"] = (
        "KiDS: la media marginal se aparta del mejor ajuste %+.5f (%+.2f sigma)"
        % (k["desplazamiento"], k["en_sigmas"]))
    SALIDA.write_text(json.dumps(sal, indent=1))
    print("\nescrito -> %s" % SALIDA.relative_to(REPO), flush=True)


if __name__ == "__main__":
    main()
