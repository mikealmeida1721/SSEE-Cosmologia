"""La pinza CONJUNTA: KiDS + CMB en el mismo punto, con la rejilla extendida (cola #26)

=====================================================================
POR QUE, Y QUE CORRIGE
=====================================================================

La #24 midio que KiDS prefiere m_x ~ 0.8 eV y yo reporte que «Planck la
permite» porque su dNeff = 0.249 caia por debajo del 0.30 de la cota.

LA #25 DEMOSTRO QUE ESA LECTURA ERA FALSA. Preguntandole al CMB directamente,
ese punto cuesta +419.98 de chi2. dNeff es un RESUMEN del aporte relativista y
NO captura lo que el CMB le cobra a una especie que todavia iba rapida cerca de
la recombinacion. La cota a mano decia «permitido» para algo que el dato rechaza
de forma aplastante.

Y la #25 dejo el optimo conjunto PEGADO AL BORDE de la rejilla de masas
(m_x = 4.0 eV, el ultimo valor util que habia). Esta corrida extiende.

=====================================================================
LOS SIMBOLOS
=====================================================================

  m_x      masa de la particula, en eV                    -- se barre
  omega_x  densidad que lleva; se le RESTA a omega_c      -- se barre
  xi       su temperatura / la de los neutrinos           -- derivado
  dNeff    = xi^4. Se ANOTA, ya NO se usa como criterio   -- derivado
  d_KiDS   chi2_KiDS(punto) - chi2_KiDS(sin particula)
  d_CMB    chi2_CMB(punto)  - chi2_CMB(sin particula)
  d_TOTAL  la suma. ES EL VEREDICTO.

KiDS: fondo SSEE clavado, logA CLAVADO en 3.0448, molestias perfiladas.
CMB : fondo SSEE clavado, logA y tau AJUSTADOS (los dos libres de SSEE, k=2).

=====================================================================
CONTROLES (R53), PRIMERO (R24)
=====================================================================

  C1 · limite FRIO en las dos sondas a la vez: m_x = 3000 eV tiene que
       devolver d_KiDS ~ 0 y d_CMB ~ 0. Criterio |d| < 1.0 en cada una.
  C2 · el punto (0.8 eV, 0.0030) tiene que REPRODUCIR lo ya medido:
       d_KiDS = -16.45 y d_CMB = +419.98. Criterio < 0.5 en cada uno.
       Esto ata esta corrida a las dos anteriores.

Ninguna cifra entra en ningun paper.
FUENTE: results/logs/growth_2026-07/pinza_conjunta.json
"""
import json
import multiprocessing as mp
import pathlib
import sys
import time

import numpy as np
from scipy.optimize import minimize

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "p06_growth"))
sys.path.insert(0, str(REPO / "src" / "p03_cmb"))

import particula_que_prefiere_kids as K                    # noqa: E402
import precio_cmb_de_la_particula as P                     # noqa: E402

SALIDA = REPO / "results" / "logs" / "growth_2026-07" / "pinza_conjunta.json"

MASAS = np.array([2.2, 3.0, 4.0, 5.5, 7.5, 10.0, 15.0, 25.0])
# ORIGEN de los numeros (R65, 2026-09-19)
# ORIGEN-VALOR: 0.1426683 — omega_m que calcula CAMB con el fondo SSEE (0.14266828); el nucleo da 0.1426675 porque CAMB convierte Sum m_nu con su factor (~93.04, no 93.14)
# ORIGEN-VALOR: 0.00296 — A_sup/8 * omega_m = 0.1660/8 * 0.1426675 = 0.0029604, punto de control heredado de particula_que_prefiere_kids.py
# ORIGEN-VALOR: 0.0030 — punto (0.8 eV, 0.0030) ya medido en la cola #24, results/logs/growth_2026-07/particula_que_prefiere_kids.json
# ORIGEN-VALOR: 0.0020 — nodo de rejilla elegido: 0.002 a 0.005 en pasos de 0.001 y 0.0065 para pasar el borde de la #24
# ORIGEN-VALOR: 0.0040 — nodo de rejilla elegido (ver 0.0020)
# ORIGEN-VALOR: 0.0050 — nodo de rejilla elegido (ver 0.0020)
# ORIGEN-VALOR: 0.0065 — nodo de rejilla elegido (ver 0.0020)
OMEGAS = np.array([0.0020, 0.0030, 0.0040, 0.0050, 0.0065])
NPROC = 4

REF_CMB = 1003.581         # de la #25, con logA y tau ajustados
REF_KIDS_REJILLA = 282.1747   # el de la #24, con halo_A en rejilla de 5
REF_KIDS = None               # se MIDE en los controles, con este minimizador

HALO_LIM = (2.00, 3.13)       # el prior oficial de KiDS
ITER = 150


def perfila_libre(m_x, om_x, tibio=None):
    """Perfila halo_A, A_IA y delta_c, los TRES dentro del minimizador.

    La #24 ponia halo_A en una rejilla de 5 porque la cache de CAMB lo resuelve
    con 5 llamadas por punto. Pero eso deja el minimo pegado a las casillas: en
    la #24 tres de los ocho mejores puntos cayeron en 3.130, el borde. Aqui va
    libre. Mejora que venia en mi propia lista de pendientes de la #24 y que
    llego por una edicion externa; se adopta AQUI, no retocando la #24, que es
    una corrida cerrada y tiene que seguir reproduciendo su resultado.

    El simplex por defecto perturba un 5%: halo_A 0.13 y A_IA 0.028, los dos
    holgados dentro de sus rangos; delta_c arranca en 0 y scipy usa 2.5e-4, que
    es 1.09 sigma de su prior. Comprobado que CABE — el fallo de `fuga3`.
    """
    tibio = tibio if tibio is not None else {}
    p0 = np.asarray(tibio.get('p3', [2.60, 0.55, 0.0]), float)

    def f(u):
        h, a_ia, d_c = float(u[0]), float(u[1]), float(u[2])
        if not (HALO_LIM[0] <= h <= HALO_LIM[1]):
            return 1e10
        return K.chi2_de(m_x, om_x, h, np.array([a_ia, d_c]))

    o = minimize(f, p0, method='Nelder-Mead',
                 options=dict(maxiter=ITER, xatol=1e-3, fatol=1e-3))
    if o.fun > 1e9:                      # si sale de la caja, reintenta del centro
        o = minimize(f, np.array([2.60, 0.55, 0.0]), method='Nelder-Mead',
                     options=dict(maxiter=ITER, xatol=1e-3, fatol=1e-3))
    tibio['p3'] = np.asarray(o.x)
    return float(o.fun), dict(
        halo_A=float(o.x[0]), A_IA=float(o.x[1]), delta_c=float(o.x[2]),
        pegado_borde=bool(o.x[0] <= 2.01 or o.x[0] >= 3.12))


def un_punto(a):
    m_x, om_x = a
    xi, dn, meff = K.traduce(m_x, om_x)
    ck, arg = perfila_libre(m_x, om_x)
    cc, lA, ta, ok = P.ajusta(dn, meff, om_x)
    dk, dc = ck - REF_KIDS, cc - REF_CMB
    print("  m_x=%6.1f om_x=%.4f xi=%.4f dNeff=%.4f | KiDS %+8.2f | "
          "CMB %+9.2f | TOTAL %+9.2f" % (m_x, om_x, xi, dn, dk, dc, dk + dc),
          flush=True)
    return dict(m_x=float(m_x), omega_x=float(om_x), xi=float(xi),
                dNeff=float(dn), frac_de_omega_m=float(om_x / 0.1426683),
                chi2_kids=float(ck), chi2_cmb=float(cc),
                d_kids=float(dk), d_cmb=float(dc), d_total=float(dk + dc),
                logA_cmb=float(lA), tau_cmb=float(ta),
                minimizador_cmb_ok=bool(ok), **arg)


def main():
    global REF_KIDS
    t0 = time.time()
    print("=" * 78, flush=True)
    print("  CONTROLES (primero, R24)", flush=True)
    print("=" * 78, flush=True)

    # C0 - la referencia SIN particula, medida con ESTE minimizador. Comparar
    # un chi2 de minimizador libre contra una referencia de rejilla sesgaria
    # todos los d_KiDS, asi que se remide aqui.
    REF_KIDS, arg0 = perfila_libre(1.0, 0.0)
    mejora = REF_KIDS_REJILLA - REF_KIDS
    ok0 = bool(mejora >= -0.05)          # libre nunca puede ser PEOR que rejilla
    print("  C0 . referencia sin particula: %.4f (libre) vs %.4f (rejilla #24)"
          % (REF_KIDS, REF_KIDS_REJILLA), flush=True)
    print("       gana %.4f  halo_A=%.3f%s  -> %s"
          % (mejora, arg0['halo_A'], " PEGADO" if arg0['pegado_borde'] else "",
             "PASA" if ok0 else "FALLA"), flush=True)

    # C1 - limite frio en las dos sondas
    xi, dn, meff = K.traduce(3000.0, 0.00296)
    ck, _ = perfila_libre(3000.0, 0.00296)
    cc, _, _, _ = P.ajusta(dn, meff, 0.00296)
    d1k, d1c = ck - REF_KIDS, cc - REF_CMB
    ok1 = bool(abs(d1k) < 1.0 and abs(d1c) < 1.0)
    print("  C1 · frio m=3000 eV:  d_KiDS %+.4f   d_CMB %+.4f  -> %s"
          % (d1k, d1c, "PASA" if ok1 else "FALLA"), flush=True)

    # C2 - reproduce el punto ya medido en la #24 y la #25
    xi, dn, meff = K.traduce(0.8, 0.0030)
    ck, arg08 = perfila_libre(0.8, 0.0030)
    cc, _, _, _ = P.ajusta(dn, meff, 0.0030)
    # El CMB usa el mismo ajustador que la #25, asi que tiene que REPRODUCIR.
    e_c = abs((cc - REF_CMB) - 419.98)
    # KiDS usa un minimizador MEJOR que la #24, asi que solo puede bajar.
    ok2 = bool(e_c < 0.5 and ck <= 265.73 + 0.05)
    print("  C2 . (0.8 eV, 0.0030): CMB err %.3f (reproduce la #25)   "
          "KiDS %.3f vs %.3f de la #24 -> %s"
          % (e_c, ck, 265.73, "PASA" if ok2 else "FALLA"), flush=True)

    if not (ok0 and ok1 and ok2):
        SALIDA.write_text(json.dumps(dict(
            corrida="cola #26", controles=dict(C0=ok0, C1=ok1, C2=ok2),
            veredicto="los controles no pasan; no se lee nada"), indent=1))
        print("\nCONTROLES FALLAN — no se mide nada.", flush=True)
        return

    puntos = [(float(m), float(o)) for m in MASAS for o in OMEGAS]
    print("\n" + "=" * 78, flush=True)
    print("  LA PINZA — %d puntos" % len(puntos), flush=True)
    print("=" * 78, flush=True)
    with mp.Pool(NPROC) as pool:
        res = pool.map(un_punto, puntos)
    res.sort(key=lambda r: r['d_total'])

    SALIDA.write_text(json.dumps(dict(
        corrida="cola #26 — la pinza conjunta KiDS+CMB, rejilla extendida",
        corrige="la #24 leyo el CMB via la cota dNeff<0.30 a mano y dijo que el "
                "punto de 0.8 eV estaba permitido; la #25 midio que ese punto le "
                "cuesta al CMB +419.98. dNeff NO sirve de criterio.",
        controles=dict(C0=ok0, C1=ok1, C2=ok2),
        ref_kids=REF_KIDS, ref_kids_rejilla_24=REF_KIDS_REJILLA,
        halo_A="libre en el minimizador, prior U(2.00, 3.13)", ref_cmb=REF_CMB,
        masas_eV=MASAS.tolist(), omegas=OMEGAS.tolist(),
        puntos=res, mejor=res[0],
        alcance="ninguna cifra entra en ningun paper",
        segundos=time.time() - t0), indent=1, default=float))
    b = res[0]
    print("\n  MEJOR CONJUNTO: m_x=%.1f eV  om_x=%.4f (%.2f%% de om_m)  "
          "dNeff=%.4f" % (b['m_x'], b['omega_x'],
                          b['frac_de_omega_m'] * 100, b['dNeff']), flush=True)
    print("     KiDS %+.2f   CMB %+.2f   TOTAL %+.2f"
          % (b['d_kids'], b['d_cmb'], b['d_total']), flush=True)
    print("\nescrito -> %s  (%.2f h)"
          % (SALIDA.relative_to(REPO), (time.time() - t0) / 3600), flush=True)


if __name__ == "__main__":
    main()
