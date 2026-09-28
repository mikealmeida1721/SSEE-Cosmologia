"""¿Quien mide MEJOR A_s, el fondo cosmico o KiDS? (pregunta de M. Almeida)

POR QUE NO ES OBVIO. Ya se midio que KiDS mide A_s por si mismo cuando el fondo
de SSEE esta clavado (D = 1.16) y que BOSS no (D = 4.01, enredado con el sesgo
de galaxia). Falta la otra mitad: **el fondo cosmico tampoco lo mide a solas**.
Lo ve multiplicado por la niebla de reionizacion: los fotones dispersados
amortiguan los picos como exp(-2·tau), asi que lo que el dato fija de verdad es
la combinacion A_s·exp(-2·tau). Subir A_s y subir tau a la vez deja el espectro
casi igual. Por eso la pregunta «quien mide mejor» hay que contestarla con el
MISMO diagnostico en los dos, no comparando barras publicadas.

QUE SE MIDE. Con el fondo de SSEE clavado por algebra, se calcula la curvatura
(la Hessiana) de chi2 en el plano (logA, tau) alrededor del minimo. De ahi:
    marginal    = lo que el CMB sabe de logA sin ayuda
    condicional = lo que sabria con tau clavado
    D           = marginal / condicional
y la combinacion mejor medida, que deberia parecerse a logA - 2·tau si la
degeneracion es la que se espera.

CONTROL (R53, y va PRIMERO por R24). Dos, y los dos son numericos:
  (a) la Hessiana se calcula con dos pasos distintos (h y h/2); si la sigma
      cambia mas del 5%, el paso esta mal elegido y no se mide nada;
  (b) prueba de curvatura: moverse 1 sigma marginal en logA (reoptimizando tau)
      tiene que subir chi2 en ~1. Si no, la Hessiana no describe el minimo.

FUENTE: results/logs/cmb_quien_mide_As.json
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

SALIDA = REPO / "results" / "logs" / "cmb_quien_mide_As.json"

FONDO = dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2, H0=S.H0_GLOBAL, ns=S.N_S)
W, WA = S.W0, S.WA

# KiDS, medido sobre su cadena (D = 1.16); ver As_medido_o_producto.json
KIDS = dict(logA=2.8627107489, marginal=0.0507836451, condicional=0.0431, D=1.16)


def chi2(logA, tau):
    return chi2_y_s8(dict(FONDO, logA=logA, tau=tau), W, WA)[0]


# ORIGEN-VALOR: 0.01364 — sigma(logA) que daba el metodo VIEJO (diferencias
# finitas, paso h) el 2026-09-08. No tiene log porque es el numero de un
# metodo RETIRADO: se conserva en el texto para explicar por que se retiro.
# ORIGEN-VALOR: 0.01232 — el mismo control con h/2, la otra mitad de esa
# comparacion (10.7% de diferencia contra un criterio del 5%).
def hessiana(x0, radio, n=5):
    """Hessiana 2x2 por AJUSTE de parabola sobre una rejilla n x n.

    FIX 2026-09-08: aqui habia diferencias finitas centradas, y FALLARON su
    propio control: sigma(logA) daba 0.01364 con paso h y 0.01232 con h/2, un
    10.7% de diferencia contra un criterio del 5%. La causa no es fisica: una
    segunda diferencia divide por h^2, asi que amplifica el ruido numerico del
    calculo del espectro justo cuando se acorta el paso. Un ajuste por minimos
    cuadrados sobre varios puntos PROMEDIA ese ruido en vez de amplificarlo.

    Devuelve (H, residuo_maximo_del_ajuste).
    """
    la, ta = x0
    rl, rt = radio
    A, T = np.meshgrid(np.linspace(la - rl, la + rl, n),
                       np.linspace(ta - rt, ta + rt, n))
    A, T = A.ravel(), T.ravel()
    y = np.array([chi2(a, b) for a, b in zip(A, T)])
    x, z = A - la, T - ta
    # chi2 = c0 + c1 x + c2 z + c3 x^2 + c4 x z + c5 z^2
    M = np.column_stack([np.ones_like(x), x, z, x * x, x * z, z * z])
    c, *_ = np.linalg.lstsq(M, y, rcond=None)
    H = np.array([[2 * c[3], c[4]], [c[4], 2 * c[5]]])
    return H, float(np.max(np.abs(M @ c - y))), float(y.max() - y.min())


def sigmas(H):
    C = np.linalg.inv(0.5 * H)          # chi2 = 2 * (-lnL)
    marg = np.sqrt(np.diag(C))
    cond = 1.0 / np.sqrt(np.diag(0.5 * H))
    return C, marg, cond


def main():
    t0 = time.time()
    print("=== minimo del fondo cosmico con el fondo de SSEE clavado", flush=True)
    r = minimize(lambda u: chi2(u[0], u[1]), [3.044, 0.054],
                 method="Nelder-Mead",
                 options=dict(xatol=1e-6, fatol=1e-4, maxiter=400))
    la, ta = float(r.x[0]), float(r.x[1])
    print("    logA = %.5f   tau = %.5f   chi2 = %.3f" % (la, ta, r.fun),
          flush=True)

    # ── CONTROL (a): la Hessiana no puede depender del paso ──────────────
    H1, res1, rango1 = hessiana((la, ta), (0.020, 0.008))
    H2, res2, rango2 = hessiana((la, ta), (0.012, 0.005))
    rel1, rel2 = res1 / rango1, res2 / rango2
    _, m1, c1 = sigmas(H1)
    C, m2, c2 = sigmas(H2)
    dif = abs(m1[0] - m2[0]) / m2[0]
    ok_a = bool(dif < 0.05)
    # FIX 2026-09-09: el criterio era `residuo < 0.05` en unidades de chi2
    # ABSOLUTAS, y eso no significa nada: el residuo de un ajuste cuadratico
    # tiene que compararse con cuanto VARIA chi2 sobre la caja, no con un
    # numero suelto. Sobre la rejilla chi2 recorre decenas, asi que 0.05 era
    # inalcanzable por construccion. Criterio nuevo, sin escala: el residuo
    # tiene que ser menos del 10% de lo que chi2 recorre en la propia rejilla.
    # Lo declaro como lo que es — yo escribi mal el criterio, y lo cambio
    # ANTES de mirar si el resultado me gusta. El control que de verdad decide
    # es el (b), que es independiente de todo esto.
    ok_a = bool(ok_a and rel1 < 0.10 and rel2 < 0.10)
    print("=== CONTROL (a): dos radios distintos + residuo del ajuste")
    print("    sigma(logA) = %.5f y %.5f   difieren %.1f%%"
          % (m1[0], m2[0], 100 * dif))
    print("    residuo del ajuste / recorrido de chi2 en la rejilla:")
    print("      %.4f/%.1f = %.1f%%   y   %.4f/%.1f = %.1f%%   (criterio <10%%)"
          % (res1, rango1, 100 * rel1, res2, rango2, 100 * rel2))
    print("    -> %s" % ("PASA" if ok_a else "FALLA"), flush=True)

    # ── CONTROL (b): moverse 1 sigma marginal debe costar ~1 en chi2 ─────
    def chi2_perfilado(logA):
        rr = minimize(lambda t: chi2(logA, t[0]), [ta], method="Nelder-Mead",
                      options=dict(xatol=1e-6, fatol=1e-4, maxiter=200))
        return float(rr.fun)
    d_chi2 = chi2_perfilado(la + m2[0]) - r.fun
    ok_b = bool(abs(d_chi2 - 1.0) < 0.35)
    print("=== CONTROL (b): +1 sigma marginal en logA (reoptimizando tau)")
    print("    delta chi2 = %.3f   (debe ser ~1)  -> %s"
          % (d_chi2, "PASA" if ok_b else "FALLA"), flush=True)

    if not (ok_a and ok_b):
        print("\n>>> ABORTA. Hessiana con paso h:\n%s" % H1)
        print(">>> Hessiana con paso h/2:\n%s" % H2)
        print(">>> sigmas h: %s   h/2: %s" % (m1, m2), flush=True)
        SALIDA.write_text(json.dumps(dict(
            control=dict(paso=dict(pasa=ok_a, sigma_h=float(m1[0]),
                                   sigma_h_medio=float(m2[0]),
                                   difiere_pct=float(100 * dif)),
                         curvatura=dict(pasa=ok_b, delta_chi2=float(d_chi2))),
            residuos_ajuste=[res1, res2],
            residuo_relativo=[rel1, rel2],
            hessiana_r=[[float(x) for x in f] for f in H1],
            hessiana_r_menor=[[float(x) for x in f] for f in H2],
            minimo=dict(logA=la, tau=ta, chi2=float(r.fun)),
            veredicto="la Hessiana no describe el minimo: no se mide nada"),
            indent=1))
        return

    D = m2 / c2
    rho = C[0, 1] / (m2[0] * m2[1])
    w, V = np.linalg.eigh(C)
    v = V[:, 0]
    v = v / abs(v).max()

    print("\n=== FONDO COSMICO (fondo de SSEE clavado, k=2: logA y tau)")
    print("    logA  marginal %.5f  condicional %.5f  D = %.2f"
          % (m2[0], c2[0], D[0]))
    print("    tau   marginal %.5f  condicional %.5f  D = %.2f"
          % (m2[1], c2[1], D[1]))
    print("    correlacion logA-tau = %+.3f" % rho)
    print("    combinacion mejor medida: %+.2f·logA %+.2f·tau  (sigma %.5f)"
          % (v[0], v[1], np.sqrt(w[0])), flush=True)

    print("\n=== COMPARACION")
    print("    %-22s %10s %12s %6s" % ("sonda", "sigma(logA)", "condicional", "D"))
    print("    %-22s %10.5f %12.5f %6.2f"
          % ("fondo cosmico", m2[0], c2[0], D[0]))
    print("    %-22s %10.5f %12.5f %6.2f"
          % ("KiDS (fondo SSEE)", KIDS["marginal"], KIDS["condicional"], KIDS["D"]))
    mejor = "fondo cosmico" if m2[0] < KIDS["marginal"] else "KiDS"
    print("    -> mide MEJOR (barra mas estrecha): %s" % mejor)
    print("    -> mide mas LIMPIO (D mas cerca de 1): %s"
          % ("fondo cosmico" if D[0] < KIDS["D"] else "KiDS"), flush=True)

    dif_logA = KIDS["logA"] - la
    sig_conj = (m2[0] ** 2 + KIDS["marginal"] ** 2) ** 0.5
    print("\n=== LA DIFERENCIA, con las DOS barras")
    print("    KiDS - fondo cosmico = %+.4f" % dif_logA)
    print("    barra conjunta       = %.4f" % sig_conj)
    print("    tension              = %.2f sigma" % abs(dif_logA / sig_conj),
          flush=True)

    # ── ¿PUEDE LA NIEBLA ABSORBER LA DERIVA? ────────────────────────────
    # La direccion que el CMB NO distingue es (aprox) logA - 2 tau. Para bajar
    # su logA hasta el de KiDS sin empeorar el ajuste habria que bajar tau la
    # mitad de esa cantidad. Pero tau tiene SUELO FISICO: no puede ser
    # negativa, y la reionizacion se ve en los cuasares, asi que tampoco puede
    # bajar de ~0.04. Eso convierte una degeneracion en un limite duro.
    # d(logA)/d(tau) a lo largo de la direccion que el CMB NO distingue.
    # v es la combinacion MEJOR medida (v0·logA + v1·tau); moverse sin
    # empeorar el ajuste = mantenerla constante => v0·dlogA + v1·dtau = 0.
    # OJO al signo: es -v1/v0, no -v0/v1 (eso daba la pendiente INVERSA).
    pend = -v[1] / v[0]
    for suelo, quien in ((0.0, "tau = 0, o sea NINGUNA reionizacion"),
                         (0.040, "tau = 0.040, suelo de los cuasares")):
        d_max = pend * (suelo - ta)
        print("\n    si tau baja hasta %s:" % quien)
        print("      logA podria bajar %.4f de los %.4f que hacen falta = %.0f%%"
              % (abs(d_max), abs(dif_logA), 100 * abs(d_max / dif_logA)))
    tau_necesaria = ta + dif_logA / pend
    print("\n    tau que haria falta para cerrar la deriva ENTERA: %.4f  -> %s"
          % (tau_necesaria,
             "IMPOSIBLE, es negativa" if tau_necesaria < 0 else "posible"),
          flush=True)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(dict(
        corrida="¿quien mide mejor A_s, el fondo cosmico o KiDS?",
        pregunta="M. Almeida — si dos sondas distintas miden A_s distinto con "
                 "el MISMO fondo ajustado, la tension es real",
        fondo_fijo_por_algebra=FONDO,
        minimo=dict(logA=la, tau=ta, chi2=float(r.fun)),
        control=dict(paso=dict(pasa=True, sigma_r=float(m1[0]),
                               sigma_r_menor=float(m2[0]),
                               difiere_pct=float(100 * dif),
                               residuos=[res1, res2],
                               residuo_relativo=[rel1, rel2]),
                     curvatura=dict(pasa=True, delta_chi2=float(d_chi2),
                                    criterio="+1 sigma debe costar ~1")),
        cmb=dict(logA=la, marginal=float(m2[0]), condicional=float(c2[0]),
                 D=float(D[0]), tau_marginal=float(m2[1]),
                 correlacion_logA_tau=float(rho),
                 combinacion_mejor_medida="%+.2f logA %+.2f tau" % (v[0], v[1]),
                 sigma_de_esa_combinacion=float(np.sqrt(w[0]))),
        kids=KIDS,
        diferencia=dict(delta_logA=float(dif_logA),
                        sigma_conjunta=float(sig_conj),
                        tension_sigma=float(abs(dif_logA / sig_conj))),
        puede_la_niebla_absorberlo=dict(
            pendiente_dlogA_dtau=float(pend),
            tau_necesaria_para_cerrarla=float(tau_necesaria),
            posible=bool(tau_necesaria >= 0.0),
            fraccion_que_cubre_con_tau_cero=float(
                abs(pend * (0.0 - ta) / dif_logA)),
            fraccion_que_cubre_con_suelo_cuasares=float(
                abs(pend * (0.040 - ta) / dif_logA)),
            nota="tau no puede ser negativa, y la reionizacion se ve en los "
                 "cuasares (tau >~ 0.04). El suelo fisico convierte la "
                 "degeneracion en un limite duro"),
        alcance="no toca ningun paper; diagnostico para saber si la deriva de "
                "A_s es una medicion contra otra o una sombra de degeneracion",
        segundos=time.time() - t0), indent=1))
    print("\nescrito -> %s" % SALIDA.relative_to(REPO), flush=True)


if __name__ == "__main__":
    main()
