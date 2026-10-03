"""LA REJILLA HASTA EL BORDE REAL — extension de la cola #28 (2026-09-13)

=====================================================================
POR QUE, Y QUE PREGUNTA CONTESTA
=====================================================================

La cola #28 dio su minimo en om_x = 0.0065, que es EL ULTIMO VALOR DE SU
REJILLA. La mejora no se agoto: se acabo la malla. Con `base_sin_particula`
ya sabemos contra que se lee (dchi2 = -10.87, Dk = 2), pero un minimo
pegado al borde no es un minimo: es un aviso de que falta mirar mas alla.

Esto extiende la rejilla en om_x hasta donde el MODELO lo permite, no hasta
donde el chi2 siga bajando. La diferencia es todo el asunto.

=====================================================================
LOS DOS LIMITES, FIJADOS ANTES DE CORRER (R24)
=====================================================================

  L1 · dNeff.  La particula entra como radiacion extra con dNeff = xi^4,
       xi = (94.0641 * om_x / m_x)^(1/3). Planck+BBN admiten ~0.3.
       Para m=7.5 eso deja subir hasta om_x = 0.0323. MUCHO margen.

  L2 · omega_c.  om_x se le RESTA a omch2, y omch2 no es una perilla:
       es omega_c = KAL0 * omega_b * n_s = 0.11951, FIJADO POR ALGEBRA
       (identidad forward de Paper 1, 0.41sigma). Quitarle una tajada
       grande a omega_c no es "ajustar un parametro": es romper la
       prediccion que sostiene el modelo.
       Se fija el tope en el 10 % de omega_c -> om_x <= 0.0120.

  MANDA L2, y esto es el resultado de haber hecho la cuenta: el limite no
  viene de fuera (Neff, BBN) sino de DENTRO. Lo que acota a la particula
  es la propia algebra del modelo que la alojaria.

  La rejilla llega a 0.0125 (10.5 %) a proposito: un punto FUERA del tope,
  para ver la forma de la curva al cruzarlo. Ese punto se marca
  `fuera_del_tope` y NO puede ser el resultado. Esta ahi para mirar, no
  para elegir.

  L3 · el limite de A_s de la cola #28 sigue vigente: |dlogA| <= 2 sigma
       del CMB (0.0291). Quien lo pase se marca RECHAZADA.

=====================================================================
COMO SE LEE (fijado antes de mirar)
=====================================================================

  a) Si el minimo cae DENTRO del tope y con om_x interior a la rejilla:
     hay un punto de equilibrio, y entonces el dchi2 significa algo.
  b) Si el minimo vuelve a pegarse al borde superior (0.0125, fuera del
     tope): el ajuste pide mas particula de la que el modelo puede
     albergar sin romper omega_c. Eso NO es una deteccion: es que la
     mejora y el modelo tiran en direcciones distintas, y hay que decirlo.
  c) Si el chi2 deja de bajar antes del tope: hay minimo propio, que es
     el mejor de los desenlaces.

Ninguna cifra entra en ningun paper.
R53: su control es results/logs/growth_2026-07/base_sin_particula.json.
FUENTE: results/logs/growth_2026-07/rejilla_extendida.json
"""
import json, multiprocessing as mp, pathlib, sys, time
import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[2]
for s in ("src", "src/p06_growth", "src/p03_cmb"): sys.path.insert(0, str(REPO/s))

# OJO AL ORDEN (lo aprendimos por las malas el 2026-09-13): el Pool se crea
# ANTES de que este proceso llame a CAMB. Si se toca CAMB primero, los hijos
# heredan por fork los mutexes de sus hilos ya bloqueados y la corrida se
# queda colgada a 0 % de CPU sin dar error. `conjunta_tres_sondas` lo hace
# bien; `base_sin_particula` en su primera version lo hizo mal.
import conjunta_tres_sondas as Q
import ssee_core as S

SALIDA = REPO/"results"/"logs"/"growth_2026-07"/"rejilla_extendida.json"
BASE   = REPO/"results"/"logs"/"growth_2026-07"/"base_sin_particula.json"
# omega_c NO se teclea: sale del nucleo. Un literal aqui se queda rancio
# en silencio el dia que el nucleo cambie — asi sobrevivio 15 dias el
# drift de Sigma m_nu.
OMEGA_C = float(S.OMEGA_C_H2)
TOPE_OMC = 0.10                      # fraccion maxima de omega_c
TOPE = TOPE_OMC * OMEGA_C            # = 0.011951
MASAS  = [4.0, 7.5]
# ORIGEN de los numeros (R65, 2026-09-19)
# ORIGEN-VALOR: 0.0065 — minimo de la cola #28 (ultimo nodo de su rejilla), results/logs/growth_2026-07/conjunta_tres_sondas.json
# ORIGEN-VALOR: 0.0323 — dNeff = xi^4 = 0.3 => xi^3 = 0.40536; om_x = 0.40536*7.5/94.0641 = 0.032321
# ORIGEN-VALOR: 0.0120 — 10 % de omega_c = 0.10 * 0.11951 = 0.011951, redondeado a 4 decimales (TOPE, abajo)
# ORIGEN-VALOR: 0.0291 — 2 * 0.0145437 = 0.029087 (0.0145437 = sigma(logA) del CMB de SSEE, results/logs/growth_2026-07/quien_mide_As.json)
# ORIGEN-VALOR: 0.0080 — nodo de rejilla elegido: de 0.0080 a 0.0125 en pasos de 0.0015, mas alla del borde 0.0065 de la #28
# ORIGEN-VALOR: 0.0095 — nodo de rejilla elegido (ver 0.0080)
# ORIGEN-VALOR: 0.0110 — nodo de rejilla elegido (ver 0.0080)
# ORIGEN-VALOR: 0.0125 — nodo elegido FUERA del tope a proposito (10.46 % de omega_c) para ver la curva al cruzarlo
OMEGAS = [0.0080, 0.0095, 0.0110, 0.0125]
NPROC = 4


def main():
    t0 = time.time()
    pts = [(float(m), float(o)) for m in MASAS for o in OMEGAS]
    print("=" * 104, flush=True)
    print("  REJILLA EXTENDIDA — %d casillas nuevas" % len(pts), flush=True)
    print("  tope por omega_c (%.0f %%): om_x <= %.5f" % (100*TOPE_OMC, TOPE), flush=True)
    print("  limite de A_s heredado: |dlogA| <= %.4f" % Q.LIMITE, flush=True)
    print("=" * 104, flush=True)

    with mp.Pool(NPROC) as pool:          # el Pool, PRIMERO
        res = pool.map(Q.un_punto, pts)

    base = json.loads(BASE.read_text())
    for r in res:
        r["fuera_del_tope"] = bool(r["omega_x"] > TOPE)
        r["pct_omega_c"] = 100.0 * r["omega_x"] / OMEGA_C
        r["dchi2_vs_base"] = r["chi2_total"] - base["chi2_base"]

    viejo = json.loads((REPO/"results"/"logs"/"growth_2026-07"/
                        "conjunta_tres_sondas.json").read_text())["puntos"]
    for r in viejo:
        r["fuera_del_tope"] = bool(r["omega_x"] > TOPE)
        r["pct_omega_c"] = 100.0 * r["omega_x"] / OMEGA_C
        r["dchi2_vs_base"] = r["chi2_total"] - base["chi2_base"]

    todos = sorted(viejo + res, key=lambda r: r["chi2_total"])
    print("\n  %5s %8s %7s %9s %9s %10s %9s %s" % (
        "m_x", "om_x", "%om_c", "logA", "sigCMB", "TOTAL", "dchi2", ""), flush=True)
    for r in todos[:14]:
        print("  %5.1f %8.4f %6.1f%% %9.4f %+9.2f %10.2f %+9.2f %s%s" % (
            r["m_x"], r["omega_x"], r["pct_omega_c"], r["logA"], r["sigmas_vs_CMB"],
            r["chi2_total"], r["dchi2_vs_base"],
            "FUERA DEL TOPE " if r["fuera_del_tope"] else "",
            "RECHAZADA A_s" if r["rechazada_por_limite"] else ""), flush=True)

    validos = [r for r in todos if not r["fuera_del_tope"]
               and not r["rechazada_por_limite"]]
    mejor = validos[0] if validos else None
    borde = bool(mejor and mejor["omega_x"] == max(
        o for o in OMEGAS + [0.0065] if o <= TOPE))
    if mejor is None:
        ver = "ningun punto cumple los dos limites"
    elif borde:
        ver = ("el minimo valido vuelve a caer en el borde: el ajuste pide mas "
               "particula de la que omega_c puede ceder. NO es una deteccion")
    else:
        ver = ("hay minimo propio dentro de los limites: el punto de equilibrio "
               "existe y el dchi2 se puede leer")

    if mejor:
        print("\n  MEJOR DENTRO DE LOS DOS LIMITES: m_x=%.1f om_x=%.4f (%.1f %% de omega_c)"
              "  TOT %.2f  dchi2 %+.2f" % (mejor["m_x"], mejor["omega_x"],
              mejor["pct_omega_c"], mejor["chi2_total"], mejor["dchi2_vs_base"]), flush=True)
    print("  VEREDICTO: %s" % ver, flush=True)

    SALIDA.write_text(json.dumps(dict(
        corrida="rejilla extendida — hasta el borde que el MODELO permite",
        limites=dict(tope_omega_c_frac=TOPE_OMC, tope_om_x=TOPE,
                     omega_c_algebraico=OMEGA_C, limite_dlogA=Q.LIMITE,
                     dNeff_permitiria="m=7.5 -> 0.0323; manda omega_c, no Neff",
                     fijados="antes de correr"),
        chi2_base_sin_particula=base["chi2_base"],
        masas=MASAS, omegas=OMEGAS, puntos_nuevos=res, todos=todos,
        mejor_dentro_de_limites=mejor, minimo_en_el_borde=borde,
        veredicto=ver, segundos=time.time()-t0), indent=1, default=float))
    print("\nescrito -> %s (%.2f h)" % (SALIDA.relative_to(REPO),
                                        (time.time()-t0)/3600), flush=True)


if __name__ == '__main__':
    main()
