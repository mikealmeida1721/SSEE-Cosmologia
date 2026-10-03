"""¿Cuánto le CUESTA al CMB la partícula que KiDS prefiere? (cola #25)

=====================================================================
POR QUÉ ESTA CORRIDA, Y QUÉ CIERRA
=====================================================================

La #24 midió que KiDS, con el fondo de SSEE clavado y `A_s` IMPUESTO por su
propio CMB, prefiere una partícula térmica: gana 16.45 de chi2 y llega a 0.29
de lo que consigue soltar la amplitud entera. O sea que **la partícula hace el
trabajo que hacía la perilla**, que es justo el mecanismo que se buscaba.

Pero la #24 cruzó con el CMB **a mano**, aplicando la cota `ΔN_eff < 0.30` por
fuera. Eso no vale como veredicto: `ΔN_eff` es un resumen, y el CMB tiene más
cosas que decir sobre una especie masiva que su aporte relativista (dónde cae
la igualdad materia-radiación, cuánto se amortigua la cola, dónde quedan los
picos). **Aquí se le pregunta al CMB directamente.**

=====================================================================
LOS SÍMBOLOS
=====================================================================

  m_x      masa de la partícula, en eV
  ω_x      densidad que lleva. Se le RESTA a `ω_c`, así que `ω_m` no se mueve
  ξ        su temperatura ÷ la de los neutrinos. Sale de m_x y ω_x
  ΔN_eff   = ξ⁴. Lo que la #24 usaba como cota a mano; aquí NO se usa como
           criterio, solo se anota para comparar
  logA, τ  los DOS libres de SSEE a nivel CMB (k=2). Se ajustan en cada punto
  χ²_CMB   plik_lite TTTEEE + lowT + lowE
  χ²_KiDS  el de la #24, ya medido, en el mismo punto de la rejilla

  El veredicto se lee sobre **χ²_CMB + χ²_KiDS**, que es la pinza de verdad.

=====================================================================
UNA PREGUNTA TEÓRICA QUE ESTA CORRIDA NO RESUELVE, Y HAY QUE DECIR
=====================================================================

SSEE predice `ω_c = KAL₀·ω_b·n_s = 0.1195144` por álgebra. Meter la partícula
restándosela a `ω_c` supone que esa identidad habla de **toda la materia
oscura**, y que la partícula es una sub-especie que vive dentro. Si la
identidad hablara específicamente de materia oscura FRÍA, restarle un 2% la
rompe. **Esta corrida no decide eso**: mantiene `ω_m` total en su valor
algebraico, que es lo que pidió Mike, y deja la pregunta abierta y anotada.

=====================================================================
CONTROLES (R53), PRIMERO (R24)
=====================================================================

  C0 · con la partícula APAGADA el chi2 del CMB tiene que ser el de siempre,
       bit a bit. Toco el constructor del modelo; si esto se mueve, todo lo
       demás sobra.
  C1 · límite FRÍO: m_x = 3000 eV es materia oscura fría normal ⟹ el chi2 del
       CMB tiene que volver al de sin partícula. Criterio |Δchi2| < 1.0.
  C2 · el simplex de (logA, τ) tiene que caber en sus cotas — el fallo que se
       cazó hoy en `fuga3`. Se comprueba explícitamente.

NINGUNA cifra entra en ningún paper.
FUENTE: results/logs/precio_cmb_de_la_particula.json
"""
# ORIGEN-VALOR: 0.00296 — A_sup/8 * omega_m = 0.1660/8 * 0.1426675 = 0.0029604 (regla de la cola #19, BANDEJA/2026-09-09_prediccion_particula_kids.md)
import json
import multiprocessing as mp
import pathlib
import sys
import time

import numpy as np
from scipy.optimize import minimize

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "p03_cmb"))

import cmb_eval as E                                       # noqa: E402
import ssee_core as S                                      # noqa: E402

SALIDA = REPO / "results" / "logs" / "precio_cmb_de_la_particula.json"
KIDS = REPO / "results" / "logs" / "growth_2026-07" / \
    "particula_que_prefiere_kids.json"

BASE = dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2, H0=S.H0_GLOBAL, ns=S.N_S)
LIM_LOGA, LIM_TAU = (1.0, 5.0), (0.010, 0.200)
X0 = np.array([3.044, 0.054])
PASO = np.array([0.02, 0.005])          # cabe holgado en las cotas
NPROC = 3


def ajusta(dneff, meff, om_x):
    """Ajusta (logA, tau) con el fondo de SSEE clavado y la particula dentro."""
    def f(u):
        lA, ta = float(u[0]), float(u[1])
        if not (LIM_LOGA[0] < lA < LIM_LOGA[1]):
            return 1e30
        if not (LIM_TAU[0] < ta < LIM_TAU[1]):
            return 1e30
        p = dict(BASE, omch2=BASE['omch2'] - om_x, logA=lA, tau=ta)
        return E.chi2_particula(p, S.W0, S.WA, dneff, meff)[0]
    sim = np.vstack([X0, X0 + [PASO[0], 0.0], X0 + [0.0, PASO[1]]])
    r = minimize(f, X0, method='Nelder-Mead',
                 options=dict(xatol=1e-5, fatol=1e-3, maxiter=400,
                              initial_simplex=sim))
    f0 = float(f(X0))
    if not np.isfinite(r.fun) or r.fun > f0:
        return f0, float(X0[0]), float(X0[1]), False
    return float(r.fun), float(r.x[0]), float(r.x[1]), True


def un_punto(arg):
    m_x, om_x, xi, dn, meff, chi2_kids = arg
    c, lA, ta, ok = ajusta(dn, meff, om_x)
    print("  m_x=%8.1f eV  om_x=%.4f  dNeff=%.4f | CMB %9.2f  logA %.4f "
          "tau %.4f %s" % (m_x, om_x, dn, c, lA, ta, "" if ok else "<-FALLA"),
          flush=True)
    return dict(m_x=m_x, omega_x=om_x, xi=xi, dNeff=dn, chi2_cmb=c,
                logA=lA, tau=ta, minimizador_ok=bool(ok), chi2_kids=chi2_kids)


def main():
    t0 = time.time()
    d = json.loads(KIDS.read_text())
    C_NU = d['C_nu_eV']
    ref_kids = d['chi2_sin_particula']

    print("=" * 74, flush=True)
    print("  CONTROLES (primero, R24)", flush=True)
    print("=" * 74, flush=True)

    # C2 · el simplex cabe
    ok2 = bool(LIM_LOGA[0] < X0[0] + PASO[0] < LIM_LOGA[1]
               and LIM_TAU[0] < X0[1] + PASO[1] < LIM_TAU[1])
    print("  C2 · simplex de (logA, tau) dentro de cotas -> %s"
          % ("PASA" if ok2 else "FALLA"), flush=True)

    # C0 · particula apagada = el CMB de siempre, bit a bit
    p0 = dict(BASE, logA=3.044, tau=0.054)
    a = E.chi2_y_s8(p0, S.W0, S.WA)[0]
    b = E.chi2_particula(p0, S.W0, S.WA, 0.0, 0.0)[0]
    ok0 = bool(a == b)
    print("  C0 · particula apagada: %.10f vs %.10f -> %s"
          % (a, b, "PASA" if ok0 else "FALLA"), flush=True)

    # referencia: SSEE sin particula, con logA y tau ajustados
    ref, lA0, ta0, _ = ajusta(0.0, 0.0, 0.0)
    print("\n  REFERENCIA CMB sin particula: chi2 = %.3f  (logA %.4f, tau %.4f)"
          % (ref, lA0, ta0), flush=True)

    # C1 · limite frio
    m_frio, om_frio = 3000.0, 0.00296
    xi_f = (C_NU * om_frio / m_frio) ** (1 / 3.0)
    c_frio, _, _, _ = ajusta(xi_f ** 4, om_frio * C_NU, om_frio)
    ok1 = bool(abs(c_frio - ref) < 1.0)
    print("  C1 · m_x=3000 eV (frio): %.3f vs %.3f -> %s"
          % (c_frio, ref, "PASA" if ok1 else "FALLA"), flush=True)

    if not (ok0 and ok1 and ok2):
        SALIDA.write_text(json.dumps(dict(
            corrida="cola #25", controles=dict(C0=ok0, C1=ok1, C2=ok2),
            veredicto="los controles no pasan; no se lee nada"), indent=1))
        print("\nCONTROLES FALLAN — no se mide nada.", flush=True)
        return

    # ── los puntos: los mismos de la rejilla de KiDS, sin la columna 0 ──
    puntos = []
    for fila in d['rejilla']:
        for p in fila:
            if p['omega_x'] <= 0 or p['m_x'] is None or p['m_x'] > 60.0:
                continue
            xi = p['xi']
            puntos.append((p['m_x'], p['omega_x'], xi, p['dNeff'],
                           p['omega_x'] * C_NU, p['chi2']))
    puntos.sort(key=lambda t: t[5])
    puntos = puntos[:20]                      # los 20 mejores para KiDS
    print("\n" + "=" * 74, flush=True)
    print("  EL PRECIO — %d puntos, los mejores de KiDS" % len(puntos), flush=True)
    print("=" * 74, flush=True)

    with mp.Pool(NPROC) as pool:
        res = pool.map(un_punto, puntos)

    for r in res:
        r['d_cmb'] = r['chi2_cmb'] - ref
        r['d_kids'] = r['chi2_kids'] - ref_kids
        r['d_total'] = r['d_cmb'] + r['d_kids']
    res.sort(key=lambda r: r['d_total'])

    SALIDA.write_text(json.dumps(dict(
        corrida="cola #25 — cuanto le cuesta al CMB la particula que KiDS pide",
        pregunta="M. Almeida — la #24 cruzo con el CMB a mano via dNeff; aqui "
                 "se le pregunta al CMB directamente y se suman los dos chi2",
        controles=dict(C0=ok0, C1=ok1, C2=ok2, chi2_frio=float(c_frio)),
        chi2_cmb_sin_particula=float(ref), logA_sin=float(lA0), tau_sin=float(ta0),
        chi2_kids_sin_particula=float(ref_kids),
        pregunta_teorica_abierta="restar omega_x a omega_c supone que la "
                                 "identidad omega_c = KAL0*omega_b*n_s habla de "
                                 "TODA la materia oscura, no solo de la fria",
        puntos=res, mejor=res[0],
        alcance="ninguna cifra entra en ningun paper",
        segundos=time.time() - t0), indent=1, default=float))

    b = res[0]
    print("\n  MEJOR EN CONJUNTO: m_x=%.1f eV  om_x=%.4f  dNeff=%.3f" % (
        b['m_x'], b['omega_x'], b['dNeff']), flush=True)
    print("     CMB %+.2f   KiDS %+.2f   TOTAL %+.2f"
          % (b['d_cmb'], b['d_kids'], b['d_total']), flush=True)
    print("\nescrito -> %s  (%.2f h)"
          % (SALIDA.relative_to(REPO), (time.time() - t0) / 3600), flush=True)


if __name__ == "__main__":
    main()
