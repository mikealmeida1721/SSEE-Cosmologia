"""¿Qué partícula prefiere KiDS, con el fondo de SSEE clavado? (cola #24)

=====================================================================
LOS SÍMBOLOS, todos, antes de usar ninguno
=====================================================================

  m_x      masa de la partícula, en eV.  LIBRE — es lo que se mide.
  ω_x      cuánta densidad lleva la partícula (adimensional, como ω_c).
           LIBRE — se barre. 0.002960 sería el 2.08% de ω_m.
  ξ        temperatura de la partícula dividida por la de los neutrinos.
           NO es libre: sale forzada de m_x y ω_x. Más pesada ⟹ tienen que
           ser menos ⟹ vinieron de un baño más frío.
  ΔN_eff   cuánta energía relativista aporta mientras va rápido, medida en
           «neutrinos». Vale ξ⁴. Planck deja ≲ 0.3 y no más.
  ω_c      materia oscura fría de siempre. Se le RESTA ω_x, para que la
           materia total no se mueva (lo pidió Mike explícitamente).
  halo_A   apantallamiento por bariones (HMcode c_min). Bajo = suprime más.
  A_IA     alineamiento intrínseco de las galaxias. Alto = rebaja la señal.
  delta_c  desplazamiento del punto cero de la cizalla.

  logA     ln(10^10 A_s). Va CLAVADO en 3.0448340130228546, el que pide el
           CMB de SSEE. No se ajusta: si se suelta, se lleva él el efecto y
           la prueba no mide nada.

=====================================================================
QUÉ PREGUNTA, Y POR QUÉ ASÍ
=====================================================================

Con el fondo de SSEE clavado y la amplitud impuesta por su propio CMB, KiDS
pide ~18 de chi2 menos de los que le salen. Ya está descartado que lo fabrique
el fondo (`lcdmfijo`: el de Planck da el mismo agujero), que lo fabriquen los
ingredientes (`fuga3 fondo`: se mueven <0.6 sigma) y que sea la regla de medir
(el volumen es `ln det F`, y KiDS no lo lleva).

La cola #19 midió la FORMA de lo que falta con una familia inventada por mí,
`P(k)*[1 - A_sup*x²/(1+x²)]`. Salió indistinguible de plana. Esta corrida
sustituye esa familia inventada por FÍSICA DE VERDAD: una especie térmica
masiva integrada por CAMB, que no necesita que yo dibuje ninguna raya sobre
cuándo la partícula «ya se frenó».

=====================================================================
LA TRADUCCIÓN A CAMB — verificada antes de correr, no supuesta
=====================================================================

CAMB acepta una especie térmica extra por el canal `meffsterile`, con una
degeneración g = nnu - 3.044 y una densidad ω = meffsterile/C_nu.

    g          = ξ⁴            reproduce el aporte relativista
    meffsterile = ω_x · C_nu   reproduce la densidad de hoy

y con eso la masa INTERNA que usa CAMB sale m_camb = m_x/ξ. Como CAMB pone la
especie a la temperatura de los neutrinos, el cociente m_camb/T_nu = m_x/T_x:
la distribución de momentos es la misma, y como p/T se conserva al expandirse,
el free-streaming es idéntico. C_nu se MIDE del propio CAMB al arrancar
(sale ~94.06 eV), no se toma de una constante escrita a mano.

=====================================================================
CONTROLES (R53), y van PRIMERO (R24)
=====================================================================

  C0 · Acabo de tocar `run_camb`, que es física validada. Con la partícula
       apagada tiene que dar EXACTAMENTE el chi2 de antes. Criterio: idéntico
       bit a bit. Si falla, el resto no vale nada.
  C1 · La densidad de materia total no se puede mover al meter la partícula:
       ω_b + ω_c + ω_nu + ω_x tiene que salir igual con y sin ella.
       Criterio: < 1e-6.
  C2 · Una partícula MUY pesada y MUY fría es indistinguible de materia
       oscura fría normal ⟹ tiene que devolver el chi2 de sin partícula.
       Criterio: |Δchi2| < 1.0, con las molestias FIJAS para que sea exacto.
       (No pongo 1e-6: aprendí en la #19 que un criterio por debajo del ruido
       de mi propio minimizador falla por mi culpa, no por física.)

=====================================================================
LO QUE ESTA CORRIDA NO HACE
=====================================================================

- NO reabre la partícula φ-DM retirada el 2026-08-01. Aquella salía de restar
  una densidad menos una ecuación de estado; ésta sale de un déficit medido.
- NO decide que la partícula exista. Mide qué masa y qué densidad prefiere
  KiDS, y eso se cruza después con lo que Planck permite.
- NINGUNA cifra entra en ningún paper.

FUENTE: archive/logs_superados/particula_colas_24_29_2026-09/particula_que_prefiere_kids.json (archivada 2026-10-16)
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

import camb                                                     # noqa: E402
import cobaya_kids as C                                         # noqa: E402
import kids_shear as K                                          # noqa: E402

SALIDA = REPO / "results" / "logs" / "growth_2026-07" / \
    "particula_que_prefiere_kids.json"

LOGA_CMB_SSEE = 3.0448340130228546      # el que pide el CMB de SSEE. CLAVADO.
BG = dict(C.SSEE_BG)                    # fondo algebraico de SSEE

# --- la rejilla ---
MASAS = np.array([0.3, 0.5, 0.8, 1.3, 2.2, 4.0, 10.0, 50.0, 3000.0])   # eV
# ORIGEN de los numeros (R65, 2026-09-19)
# ORIGEN-VALOR: 0.002960 — A_sup/8 * omega_m = 0.1660/8 * 0.1426675 = 0.0029604; regla dP/P=-8f de la cola #19, que CAMB corrigio (BANDEJA/2026-09-09_prediccion_particula_kids.md). Aqui solo es un punto de prueba de C1/C2
# ORIGEN-VALOR: 0.0029600 — el mismo 0.002960 de arriba, escrito con un cero mas
# ORIGEN-VALOR: 0.1426683 — omega_m que calcula CAMB con el fondo SSEE (ombh2+omch2+omnuh2 = 0.14266828); difiere del nucleo 0.1426675 porque CAMB convierte Sum m_nu con su factor (~93.04, no 93.14)
# ORIGEN-VALOR: 0.0010 — nodo de rejilla elegido: omega_x de 0 a 0.005 en pasos de 0.001, abarca el 0.00296
# ORIGEN-VALOR: 0.0020 — nodo de rejilla elegido (ver 0.0010)
# ORIGEN-VALOR: 0.0030 — nodo de rejilla elegido (ver 0.0010)
# ORIGEN-VALOR: 0.0040 — nodo de rejilla elegido (ver 0.0010)
# ORIGEN-VALOR: 0.0050 — nodo de rejilla elegido (ver 0.0010)
OMEGAS = np.array([0.0, 0.0010, 0.0020, 0.0030, 0.0040, 0.0050])
# halo_A cubre el prior ENTERO U(2.0, 3.13) — en la #19 puse 3 puntos y dos
# filas se pegaron al 2.15, que era el borde de MI rejilla y no el del prior.
HALO = np.array([2.00, 2.30, 2.60, 2.90, 3.13])
ITER = 40
NPROC = 4                               # 4 nucleos: la cadena usa 4 y #17 usa 1


def mide_C_nu():
    """Mide del propio CAMB cuanta omega aporta la esteril por eV de meffsterile."""
    def om(meff, dn):
        p = camb.CAMBparams()
        # sin `num_massive_neutrinos`: ver la nota en kids_shear.run_camb
        kw = dict(nnu=3.044 + dn, meffsterile=meff) if meff > 0 else {}
        p.set_cosmology(H0=BG['h0'] * 100.0, ombh2=BG['ombh2'],
                        omch2=BG['omch2'], mnu=BG['mnu'], omk=0.0, **kw)
        return p.omnuh2
    return 1.0 / (om(1.0, 0.1) - om(0.0, 0.0))


C_NU = mide_C_nu()


def traduce(m_x, om_x):
    """(masa, densidad) -> (xi, dNeff, meffsterile) para CAMB."""
    if om_x <= 0.0:
        return 0.0, 0.0, 0.0
    xi = (C_NU * om_x / m_x) ** (1.0 / 3.0)
    return xi, xi ** 4, om_x * C_NU


_CACHE = {}


def camb_de(m_x, om_x, halo_A):
    key = (round(m_x, 6), round(om_x, 8), round(halo_A, 4))
    if key not in _CACHE:
        _, dn, meff = traduce(m_x, om_x)
        if len(_CACHE) > 12:
            _CACHE.clear()
        _CACHE[key] = K.run_camb(
            omch2=BG['omch2'] - om_x, ombh2=BG['ombh2'], h0=BG['h0'],
            ns=BG['ns'], As=np.exp(LOGA_CMB_SSEE) * 1e-10, mnu=BG['mnu'],
            w=BG['w0'], wa=BG['wa'], halo_A=halo_A,
            dneff=dn, meffsterile=meff)
    return _CACHE[key]


def chi2_de(m_x, om_x, halo_A, extra):
    """chi2 total (dato + priores) con la particula dentro del fondo."""
    A_IA, delta_c = extra
    dz = C.DZ_MEAN
    try:
        r, p, kh, zpk, pk, gr = camb_de(m_x, om_x, halo_A)
        ells, Cl, idx = K.cl_shear(C.D, r, p, kh, zpk, pk, gr, A_IA, dz)
        th = K.theory_vector(C.D, ells, Cl, idx, delta_c=delta_c)
    except Exception:
        return 1e10
    dv = (th - C.D['d'])[C.MASK]
    rr = dz - C.DZ_MEAN
    return (float(dv @ C.CINV @ dv) + float(rr @ C.SOM_INV @ rr)
            + (delta_c / C.DELTA_C_SIG) ** 2)


def perfila(m_x, om_x, tibio=None):
    """Minimiza sobre halo_A (rejilla de 5) y (A_IA, delta_c) (Nelder-Mead).

    DEVUELVE LOS PARAMETROS, no solo el chi2 — en la #19 los tire y hubo que
    recalcular los puntos clave a mano.  Regla nueva de Mike: toda corrida
    guarda los parametros en CADA punto de la rejilla.
    """
    tibio = tibio if tibio is not None else {}
    mejor, arg = 1e10, None
    for h in HALO:
        e0 = np.asarray(tibio.get(round(float(h), 4), [0.55, 0.0]))
        o = minimize(lambda e: chi2_de(m_x, om_x, h, e), e0,
                     method='Nelder-Mead',
                     options=dict(maxiter=ITER, xatol=1e-3, fatol=1e-3))
        tibio[round(float(h), 4)] = np.asarray(o.x)
        if o.fun < mejor:
            mejor = float(o.fun)
            arg = dict(halo_A=float(h), A_IA=float(o.x[0]),
                       delta_c=float(o.x[1]))
    arg['pegado_borde'] = bool(arg['halo_A'] in (HALO[0], HALO[-1]))
    return mejor, arg


# =====================================================================
#  CONTROLES — corren PRIMERO
# =====================================================================

def controles():
    print("=" * 74, flush=True)
    print("  CONTROLES (van primero, R24)", flush=True)
    print("=" * 74, flush=True)
    e = np.array([0.55, 0.0])
    ok = {}

    # C0 · toque `run_camb`; sin particula tiene que dar lo mismo BIT A BIT
    a = chi2_de(1.0, 0.0, 2.60, e)                     # ruta con dneff=meff=0
    r = K.run_camb(omch2=BG['omch2'], ombh2=BG['ombh2'], h0=BG['h0'],
                   ns=BG['ns'], As=np.exp(LOGA_CMB_SSEE) * 1e-10,
                   mnu=BG['mnu'], w=BG['w0'], wa=BG['wa'], halo_A=2.60)
    ells, Cl, idx = K.cl_shear(C.D, r[0], r[1], r[2], r[3], r[4], r[5],
                               e[0], C.DZ_MEAN)
    th = K.theory_vector(C.D, ells, Cl, idx, delta_c=e[1])
    dv = (th - C.D['d'])[C.MASK]
    b = float(dv @ C.CINV @ dv) + (e[1] / C.DELTA_C_SIG) ** 2
    ok['C0'] = bool(a == b)
    print("  C0 · run_camb sin particula: %.10f vs %.10f  -> %s"
          % (a, b, "PASA" if ok['C0'] else "FALLA"), flush=True)

    # C1 · la materia total no se mueve
    def om_m(om_x):
        p = camb_de(3000.0 if om_x else 1.0, om_x, 2.60)[1]
        return p.ombh2 + p.omch2 + p.omnuh2
    d = abs(om_m(0.0029600) - om_m(0.0))
    ok['C1'] = bool(d < 1e-6)
    print("  C1 · omega_m con y sin particula difiere en %.2e  -> %s"
          % (d, "PASA" if ok['C1'] else "FALLA"), flush=True)

    # C2 · una particula pesada y fria = materia oscura fria normal
    c_sin = chi2_de(1.0, 0.0, 2.60, e)
    c_fria = chi2_de(3000.0, 0.0029600, 2.60, e)
    xi, dn, _ = traduce(3000.0, 0.0029600)
    ok['C2'] = bool(abs(c_fria - c_sin) < 1.0)
    print("  C2 · m=3000 eV (xi=%.4f, dNeff=%.1e): %.4f vs %.4f sin particula"
          "  -> %s" % (xi, dn, c_fria, c_sin,
                       "PASA" if ok['C2'] else "FALLA"), flush=True)

    ok['pasa'] = bool(all(ok[k] for k in ('C0', 'C1', 'C2')))
    print("  C_nu medido del propio CAMB: %.4f eV" % C_NU, flush=True)
    return ok, float(c_sin)


# =====================================================================
#  LA MEDIDA
# =====================================================================

def una_masa(m_x):
    """Una fila entera de la rejilla: todas las densidades para una masa."""
    tibio, fila = {}, []
    for om_x in OMEGAS:
        if om_x <= 0.0:
            fila.append(None)          # la columna 0 se rellena con la referencia
            continue
        xi, dn, _ = traduce(m_x, float(om_x))
        c, arg = perfila(m_x, float(om_x), tibio)
        arg.update(chi2=c, m_x=float(m_x), omega_x=float(om_x), xi=float(xi),
                   dNeff=float(dn), frac_de_omega_m=float(om_x / 0.1426683))
        fila.append(arg)
    print("  m_x=%8.1f eV  chi2: %s" % (
        m_x, "  ".join("%7.2f" % f['chi2'] for f in fila if f)), flush=True)
    return fila


def main():
    t0 = time.time()
    ok, chi2_ref = controles()
    ref, arg_ref = perfila(1.0, 0.0)
    print("\n  referencia SIN particula (perfilada): chi2 = %.4f  "
          "halo_A=%.3f A_IA=%.4f" % (ref, arg_ref['halo_A'], arg_ref['A_IA']),
          flush=True)

    if not ok['pasa']:
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        SALIDA.write_text(json.dumps(dict(
            corrida="cola #24", controles=ok,
            veredicto="los controles no pasan; no se lee nada"), indent=1))
        print("\nCONTROLES FALLAN — no se mide nada.", flush=True)
        return

    print("\n" + "=" * 74, flush=True)
    print("  LA REJILLA   omega_x: %s" % "  ".join("%.4f" % o for o in OMEGAS[1:]),
          flush=True)
    print("=" * 74, flush=True)

    with mp.Pool(NPROC) as pool:
        filas = pool.map(una_masa, [float(m) for m in MASAS])

    arg_ref2 = dict(arg_ref); arg_ref2.update(
        chi2=ref, m_x=None, omega_x=0.0, xi=0.0, dNeff=0.0, frac_de_omega_m=0.0)
    for f in filas:
        f[0] = arg_ref2

    plano = [p for f in filas for p in f if p['omega_x'] > 0]
    mejor = min(plano, key=lambda p: p['chi2'])

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(dict(
        corrida="cola #24 — que particula prefiere KiDS con el fondo de SSEE fijo",
        pregunta="M. Almeida — con el fondo de SSEE clavado y A_s impuesto por su "
                 "propio CMB, que masa y que densidad de una especie termica "
                 "masiva prefiere KiDS",
        traduccion="g=xi^4, meffsterile=omega_x*C_nu; C_nu medido del propio CAMB",
        C_nu_eV=float(C_NU), logA_clavado=LOGA_CMB_SSEE,
        controles=ok, chi2_sin_particula=float(ref),
        params_sin_particula=arg_ref,
        masas_eV=MASAS.tolist(), omegas=OMEGAS.tolist(),
        halo_A_rejilla=HALO.tolist(),
        rejilla=filas, mejor=mejor,
        gana_vs_sin_particula=float(ref - mejor['chi2']),
        alcance="NO reabre la particula phi-DM retirada; NO decide que exista; "
                "ninguna cifra entra en ningun paper",
        segundos=time.time() - t0), indent=1, default=float))
    print("\n  MEJOR: m_x=%.2f eV  omega_x=%.5f (%.2f%% de omega_m)  "
          "xi=%.4f  dNeff=%.4f  chi2=%.2f  (gana %.2f)"
          % (mejor['m_x'], mejor['omega_x'], mejor['frac_de_omega_m'] * 100,
             mejor['xi'], mejor['dNeff'], mejor['chi2'], ref - mejor['chi2']),
          flush=True)
    print("\nescrito -> %s  (%.2f h)"
          % (SALIDA.relative_to(REPO), (time.time() - t0) / 3600), flush=True)


if __name__ == "__main__":
    main()
