"""COLA #29 — el optimo de la rejilla extendida, con A_s y tau CONTINUOS
   (2026-09-13)

=====================================================================
POR QUE, Y QUE HUECO CIERRA
=====================================================================

La `rejilla_extendida` (#28b) encontro su minimo en m_x=7.5 eV, om_x=0.0080,
dchi2 = -11.45 contra la base. Pero lo hizo con DOS aproximaciones:

  A1 · logA se eligio sobre una malla DISCRETA de 9 puntos, paso 0.0275.
       El CMB mide logA con sigma = 0.01454, asi que ese paso vale
       **1.89 sigma**. El salto de -1.77sig a +0.12sig entre casillas
       vecinas es resolucion de malla, no fisica.

  A2 · tau estaba FIJO. La #25 (`precio_cmb_de_la_particula`) si lo suelta,
       pero su rejilla se corto en m_x=4.0 / om_x=0.0050 y NUNCA llego al
       optimo. Por tanto nadie ha preguntado al CMB, con sus dos libres
       sueltos, cuanto cuesta la particula EN EL PUNTO QUE GANA.

Aqui se sueltan las dos: para cada casilla se minimiza

    chi2_total(logA, tau) = chi2_CMB(logA, tau) + chi2_KiDS(logA)
                                               + chi2_BOSS(logA)

con el fondo de SSEE clavado (Om, w0, wa por algebra). chi2_CMB se evalua
de verdad (CAMB + plik_lite); chi2_KiDS y chi2_BOSS se INTERPOLAN por spline
cubico del perfil de 9 puntos que la #28b ya guardo por casilla. Esa
interpolacion es la unica aproximacion que queda, y se declara: los perfiles
son suaves y monotonos o de una sola curvatura en el rango usado.

=====================================================================
LO QUE ES FIJO Y LO QUE ES LIBRE (declarado antes de correr)
=====================================================================

  FIJO POR ALGEBRA (no se toca):
    Om = 0.308881   w0 = -0.839950   wa = -0.669975   H0 = 3(phi+pi)^2
    ns = 1 - phi^-7        omega_b = (pi-phi)/(3 Om^2)
    omega_c = KAL0 * omega_b * ns = 0.11951

  LIBRE DEL MODELO (los k=2 de siempre):
    logA, tau

  DE LA HIPOTESIS QUE SE PRUEBA -- no se asume, se mide para saberlo
  (los Dk=2 que se pagan):
    m_x, om_x     -> om_x se RESTA de omega_c; dNeff = xi^4
    Aqui NO SE ASUME nada: m_x y om_x son justamente lo que se pone a
    prueba. El script mide lo que CUESTAN en chi2, no los da por buenos.
    La particula phi-DM quedo RETIRADA el 2026-08-01 y esto no la
    reabre: pregunta cuanto pagaria el CMB por una componente asi.

=====================================================================
LIMITES, FIJADOS ANTES (heredados de la #28b)
=====================================================================
  L2 · om_x <= 10 % de omega_c = 0.011951.  El punto 0.0125 se corre
       igual, marcado `fuera_del_tope`, solo para ver la forma.
  L3 · |logA - logA_CMB| <= 2 sigma = 0.0291 -> quien lo pase, RECHAZADA.
       Ahora logA es continuo, asi que este limite muerde de verdad.

=====================================================================
COMO SE LEE (fijado antes de mirar)
=====================================================================
  a) Si el optimo continuo sigue en om_x interior y el dchi2 se mantiene
     alrededor de -11: la #28b no era artefacto de malla.
  b) Si al soltar logA/tau el dchi2 se ENCOGE: parte de la mejora era la
     base mal servida por la malla gruesa, no la particula.
  c) Si CRECE mucho: la malla estaba castigando a la particula.
  En los tres casos manda el BIC, no el chi2 (Dk=2, N ~ 1100).

CONTROL R53 · la casilla om_x=0 se corre con EL MISMO minimizador. Tiene
que reproducir chi2_CMB ~ 1003.58 y total <= 1481.70 (la malla no puede
haber encontrado algo mejor que el continuo). Si no, el minimizador miente
y la corrida entera se descarta.

Ninguna cifra entra en ningun paper.
FUENTE: results/logs/growth_2026-07/precio_cmb_rejilla_extendida.json
"""
import json
import multiprocessing as mp
import pathlib
import sys
import time

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "p03_cmb"))

import cmb_eval as E                                       # noqa: E402
import ssee_core as S                                      # noqa: E402

LOGS = REPO / "results" / "logs" / "growth_2026-07"
REJILLA = LOGS / "rejilla_extendida.json"
BASE_JSON = LOGS / "base_sin_particula.json"
KIDS_JSON = LOGS / "particula_que_prefiere_kids.json"
SALIDA = LOGS / "precio_cmb_rejilla_extendida.json"

BASE = dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2, H0=S.H0_GLOBAL, ns=S.N_S)
LIM_LOGA, LIM_TAU = (2.80, 3.30), (0.010, 0.200)
X0 = np.array([3.044, 0.054])
PASO = np.array([0.02, 0.005])
NPROC = 3
TOPE_OM_X = 0.10 * S.OMEGA_C_H2
# ORIGEN de los numeros (R65, 2026-09-19)
# ORIGEN-VALOR: 0.0080 — minimo de la #28b en m_x=7.5 eV, results/logs/growth_2026-07/rejilla_extendida.json
# ORIGEN-VALOR: 0.0275 — paso de la malla de logA de la #28b (9 puntos, 2.88 a 3.10), results/logs/growth_2026-07/rejilla_extendida.json
# ORIGEN-VALOR: 0.01454 — 0.0145437 = sigma(logA) del CMB de SSEE, results/logs/growth_2026-07/quien_mide_As.json (decia 0.01455, errata de redondeo corregida 2026-09-19; el 1.89 sigma no cambia: 0.0275/0.0145437 = 1.891)
# ORIGEN-VALOR: 0.0050 — borde de la rejilla de la #25: sus 20 puntos llegan a m_x=4.0 y omega_x=0.005, results/logs/precio_cmb_de_la_particula.json
# ORIGEN-VALOR: 0.0125 — nodo FUERA del tope heredado de la #28b (rejilla_extendida.py)
# ORIGEN-VALOR: 0.0291 — 2 * 0.0145437 = 0.029087, redondeado a 4 decimales
# ORIGEN-VALOR: 0.02908 — 2 * 0.0145437 = 0.029087 TRUNCADO (redondeado seria 0.02909). Ninguna de las 51 casillas con dlogA en los logs cae en [0.0290, 0.0292], asi que no movio ningun veredicto
LIM_DLOGA = 0.02908
SIG_LOGA = LIM_DLOGA / 2.0


def splines(perfil):
    """KiDS y BOSS como funcion continua de logA, del perfil de 9 puntos."""
    x = np.asarray(perfil['logA'], float)
    return (CubicSpline(x, np.asarray(perfil['kids'], float)),
            CubicSpline(x, np.asarray(perfil['boss'], float)),
            float(x[0]), float(x[-1]))


def ajusta_total(dneff, meff, om_x, perfil):
    """Minimiza chi2_CMB(logA,tau) + KiDS(logA) + BOSS(logA). CMB de verdad."""
    sk, sb, lo, hi = splines(perfil)

    def f(u):
        lA, ta = float(u[0]), float(u[1])
        if not (LIM_LOGA[0] < lA < LIM_LOGA[1]):
            return 1e30
        if not (LIM_TAU[0] < ta < LIM_TAU[1]):
            return 1e30
        if not (lo <= lA <= hi):          # no extrapolar los splines
            return 1e30
        p = dict(BASE, omch2=BASE['omch2'] - om_x, logA=lA, tau=ta)
        c = E.chi2_particula(p, S.W0, S.WA, dneff, meff)[0]
        return float(c) + float(sk(lA)) + float(sb(lA))

    sim = np.vstack([X0, X0 + [PASO[0], 0.0], X0 + [0.0, PASO[1]]])
    r = minimize(f, X0, method='Nelder-Mead',
                 options=dict(xatol=1e-5, fatol=1e-3, maxiter=400,
                              initial_simplex=sim))
    f0 = float(f(X0))
    if not np.isfinite(r.fun) or r.fun > f0:
        lA, ta, ok = float(X0[0]), float(X0[1]), False
        tot = f0
    else:
        lA, ta, ok = float(r.x[0]), float(r.x[1]), True
        tot = float(r.fun)
    p = dict(BASE, omch2=BASE['omch2'] - om_x, logA=lA, tau=ta)
    c_cmb = float(E.chi2_particula(p, S.W0, S.WA, dneff, meff)[0])
    return dict(chi2_total=tot, chi2_cmb=c_cmb, chi2_kids=float(sk(lA)),
                chi2_boss=float(sb(lA)), logA=lA, tau=ta,
                minimizador_ok=bool(ok))


def un_punto(arg):
    m_x, om_x, xi, dn, meff, perfil, etq = arg
    t0 = time.time()
    r = ajusta_total(dn, meff, om_x, perfil)
    r.update(m_x=m_x, omega_x=om_x, xi=xi, dNeff=dn, etiqueta=etq,
             fuera_del_tope=bool(om_x > TOPE_OM_X),
             pct_omega_c=100.0 * om_x / S.OMEGA_C_H2,
             minutos=(time.time() - t0) / 60.0)
    print("  %-9s m_x=%6.1f om_x=%.4f | logA %.5f tau %.5f | CMB %9.2f "
          "KiDS %7.2f BOSS %7.2f | TOT %9.2f  (%.1f min)%s"
          % (etq, m_x, om_x, r['logA'], r['tau'], r['chi2_cmb'],
             r['chi2_kids'], r['chi2_boss'], r['chi2_total'], r['minutos'],
             "" if r['minimizador_ok'] else "  <-MINIMIZADOR FALLA"),
          flush=True)
    return r


def main():
    t0 = time.time()
    print("=" * 100)
    print("  COLA #29 — el optimo de la #28b con logA y tau CONTINUOS")
    print("  tope om_x <= %.6f (10 %% de omega_c=%.5f) | L3 |dlogA| <= %.4f"
          % (TOPE_OM_X, S.OMEGA_C_H2, LIM_DLOGA))
    print("=" * 100, flush=True)

    rej = json.loads(REJILLA.read_text())
    bas = json.loads(BASE_JSON.read_text())
    C_NU = json.loads(KIDS_JSON.read_text())['C_nu_eV']
    print("  C_nu del propio CAMB: %.4f eV" % C_NU, flush=True)

    perfil_base = dict(logA=bas['rejilla_logA'], kids=bas['kids'],
                       boss=bas['boss'], cmb=bas['cmb'])

    # el control R53 va PRIMERO: si la base no cierra, no se sigue
    print("\n  --- CONTROL R53: la casilla om_x=0, mismo minimizador ---",
          flush=True)
    ctrl = un_punto((0.0, 0.0, 0.0, 0.0, 0.0, perfil_base, "BASE"))
    ok_cmb = abs(ctrl['chi2_cmb'] - 1003.586) < 1.0
    ok_tot = ctrl['chi2_total'] <= 1481.71
    print("    C_R53a · chi2_CMB %.3f vs 1003.586 -> %s"
          % (ctrl['chi2_cmb'], "OK" if ok_cmb else "FALLA"))
    print("    C_R53b · total %.2f <= 1481.70 (la malla no supera al "
          "continuo) -> %s" % (ctrl['chi2_total'], "OK" if ok_tot else
                               "FALLA"), flush=True)
    if not (ok_cmb and ok_tot and ctrl['minimizador_ok']):
        SALIDA.write_text(json.dumps(dict(
            corrida="cola #29", aborto="el control R53 de la base no cierra",
            control=ctrl, ok_cmb=ok_cmb, ok_tot=ok_tot), indent=1))
        print("\n  ABORTADO: el control de la base no cierra. Nada que leer.")
        return

    # las casillas: todas las de la #28b que mejoraban, mas los topes
    puntos = []
    for p in rej['todos']:
        if p['dchi2_vs_base'] > 5.0 and not p['fuera_del_tope']:
            continue                      # ya perdidas por mucho, no gastar
        puntos.append((p['m_x'], p['omega_x'], p['xi'], p['dNeff'],
                       p['omega_x'] * C_NU, p['perfil'], "cand"))
    puntos.sort(key=lambda a: (a[0], a[1]))
    print("\n  --- %d casillas (de las 24 de la #28b) ---\n" % len(puntos),
          flush=True)

    with mp.Pool(NPROC) as pool:
        res = pool.map(un_punto, puntos)

    base_tot = ctrl['chi2_total']
    for r in res:
        r['dchi2_vs_base_continua'] = r['chi2_total'] - base_tot
        r['dlogA_vs_CMB'] = r['logA'] - ctrl['logA']
        r['sigmas_vs_CMB'] = r['dlogA_vs_CMB'] / SIG_LOGA
        r['rechazada_por_limite'] = bool(abs(r['dlogA_vs_CMB']) > LIM_DLOGA)

    vivos = [r for r in res if not r['fuera_del_tope']
             and not r['rechazada_por_limite']]
    mejor = min(vivos, key=lambda r: r['chi2_total']) if vivos else None

    print("\n%8s%9s%8s%10s%9s%9s%11s%10s%10s%11s%10s"
          % ("m_x", "om_x", "%om_c", "logA", "tau", "sigCMB", "CMB", "KiDS",
             "BOSS", "TOTAL", "dchi2"))
    print("-" * 105)
    for r in sorted(res, key=lambda r: r['chi2_total']):
        f = "FUERA" if r['fuera_del_tope'] else \
            ("RECHAZ" if r['rechazada_por_limite'] else "")
        print("%8.1f%9.4f%7.1f%%%10.5f%9.5f%+9.2f%11.2f%10.2f%10.2f%11.2f"
              "%+10.2f  %s"
              % (r['m_x'], r['omega_x'], r['pct_omega_c'], r['logA'],
                 r['tau'], r['sigmas_vs_CMB'], r['chi2_cmb'], r['chi2_kids'],
                 r['chi2_boss'], r['chi2_total'],
                 r['dchi2_vs_base_continua'], f))

    om_vivos = sorted({r['omega_x'] for r in vivos})
    interior = (mejor is not None and om_vivos
                and mejor['omega_x'] not in (om_vivos[0], om_vivos[-1]))
    if mejor is None:
        ver = "no queda ninguna casilla viva: todas rechazadas o fuera del tope"
    elif interior:
        ver = ("minimo propio interior tambien con logA y tau continuos: "
               "la #28b no era artefacto de malla")
    else:
        ver = ("el minimo continuo se pega a un extremo de om_x: no es "
               "deteccion, es que la mejora y el modelo tiran distinto")
    print("\n  BASE continua: logA=%.5f tau=%.5f CMB %.2f TOT %.2f"
          % (ctrl['logA'], ctrl['tau'], ctrl['chi2_cmb'], ctrl['chi2_total']))
    if mejor:
        d = mejor['dchi2_vs_base_continua']
        print("  MEJOR VIVO: m_x=%.1f om_x=%.4f (%.1f %% de omega_c)  "
              "TOT %.2f  dchi2 %+.2f" % (mejor['m_x'], mejor['omega_x'],
                                         mejor['pct_omega_c'],
                                         mejor['chi2_total'], d))
        for N in (1116,):
            print("  Dk=2, N=%d ->  dAIC %+.2f   dBIC %+.2f"
                  % (N, d + 4.0, d + 2.0 * np.log(N)))
    print("  VEREDICTO: %s" % ver, flush=True)

    SALIDA.write_text(json.dumps(dict(
        corrida="cola #29 — el optimo de la #28b con logA y tau continuos",
        que_hueco_cierra=("la #28b eligio logA en malla de paso 1.89 sigma y "
                          "con tau fijo; la #25 solto los dos pero se corto "
                          "en m_x=4.0/om_x=0.0050 y no llego al optimo"),
        aproximacion_que_queda=("KiDS y BOSS interpolados por spline cubico "
                               "del perfil de 9 puntos de la #28b; el CMB se "
                               "evalua de verdad"),
        fijos_por_algebra=dict(Om=float(S.OMEGA_M_TOTAL), w0=float(S.W0), wa=float(S.WA),
                               H0=float(S.H0_GLOBAL), ns=float(S.N_S),
                               omega_b=float(S.OMEGA_B_H2),
                               omega_c=float(S.OMEGA_C_H2)),
        libres_del_modelo=["logA", "tau"],
        # No se asume: es la hipotesis que se somete a prueba, y lo que el
        # log guarda es su PRECIO en chi2 (ver la cabecera del fichero).
        libres_de_la_hipotesis=["m_x", "omega_x"],   # no se asume: se mide
        limites=dict(tope_om_x=TOPE_OM_X, limite_dlogA=LIM_DLOGA,
                     sigma_logA=SIG_LOGA),
        control_R53=dict(base=ctrl, ok_cmb=ok_cmb, ok_total=ok_tot),
        chi2_base_continua=base_tot,
        puntos=res, mejor_vivo=mejor, minimo_interior=bool(interior),
        veredicto=ver, delta_k=2,
        alcance="ninguna cifra entra en ningun paper",
        segundos=time.time() - t0), indent=1))
    print("\nescrito -> %s (%.2f h)"
          % (SALIDA.relative_to(REPO), (time.time() - t0) / 3600.0),
          flush=True)


if __name__ == "__main__":
    main()
