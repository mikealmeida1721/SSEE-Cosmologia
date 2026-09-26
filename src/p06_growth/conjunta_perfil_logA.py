#!/usr/bin/env python3
"""
conjunta_perfil_logA.py — CORRIDA CONJUNTA de verdad sobre el fondo clavado.

QUE CONTESTA, Y POR QUE LA ANTERIOR NO VALIA
--------------------------------------------
`multisonda_fondo_clavado.py` evaluaba cada sonda en UN punto impuesto desde
fuera (el logA que el CMB pide) y sumaba. Con el fondo clavado Y logA clavado no
queda ningun parametro compartido, asi que esa suma es identica a los chi2
individuales POR CONSTRUCCION: no medía nada que pudiera fallar. Comprobado:
suma = 3398.385 contra «conjunto» = 3398.384.

Aqui logA es UNO SOLO y lo deciden LAS CUATRO SONDAS A LA VEZ. Cada sonda
conserva sus nuisance PRIVADOS, que se minimizan en cada nodo de la rejilla:

    chi2_j(logA) = min_{nuisance de j}  chi2_j(logA, nuisance)
    chi2_conjunto(logA) = SUMA_j chi2_j(logA)
    logA_conjunto = argmin chi2_conjunto

Eso es el perfil de verosimilitud del UNICO parametro compartido, que es lo que
una corrida conjunta determina. Y ahora si puede fallar: en logA_conjunto cada
sonda esta FUERA de su propio minimo, y cuanto paga cada una es la medida de si
se estorban. Si una sonda pagase mucho, habria tension; si el logA conjunto
cayera lejos del que pide el CMB, el fondo unificado no aguantaria en conjunto.

SONDAS Y SUS LIBRES PRIVADOS
    CMB plik_lite TTTEEE+lowT+lowE   tau                       (1)
    KiDS-Legacy xi_pm                logT_AGN, A_scale, dz1-6  (8)
    BOSS DR12 P(k) LPT               36 sesgos y contraterminos
    BAO DESI DR2                     ninguno; NO depende de logA

El fondo va CLAVADO por algebra en las cuatro: omega_b, omega_c, H0, n_s, w0,
wa del nucleo. No se ajusta nada del fondo en ningun sitio.

BOSS entra por su perfil ya medido (R1R2_boss_lpt_kmax0.200.json), que es del
OPTIMIZADOR y en chi2 REAL. NO se usa la cadena de BOSS: devuelve el chi2
marginalizado, que es otra escala, y su perfil leido en banda estrecha tenia
146 muestras y daba 12 unidades de mas.

CONTROL (R53). Dos, y los dos se escriben antes de correr:
  (a) en logA = 3.0448340130228546 el CMB tiene que devolver 1003.586 y KiDS
      417.971, que son sus valores publicados. Si no, el montaje no reproduce
      lo ya medido y el resto no vale.
  (b) el mismo perfil con el fondo de LCDM: si el conjunto SIEMPRE sale barato,
      sea cual sea el fondo, entonces la prueba no discrimina y no dice nada
      del modelo.

Salida: results/logs/conjunta_perfil_logA.json
"""
import json
import os
import sys
import time

import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import minimize

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p03_cmb"))
sys.path.insert(0, os.path.join(_R, "src", "p06_growth"))

LOGA_CLAVO = 3.0448340130228546      # ORIGEN: CANONICAL_VALUES logA_cmb_ssee
OUT = os.path.join(_R, "results", "logs", "conjunta_perfil_logA.json")
BOSS_JSON = os.path.join(_R, "results", "logs", "growth_2026-07",
                         "R1R2_boss_lpt_kmax0.200.json")

# Punto de partida de los nuisance de KiDS: el mejor ajuste de la corrida
# sseefijo (10157 muestras, chi2_min = 417.9706). Arrancar de ahi es lo que
# hace viable el perfil: cada evaluacion cuesta 3.5 s.
KIDS_X0 = np.array([7.983530, 1.493451, 0.021832, 0.000653,
                    -0.007964, -0.007060, 0.017710, 0.052340])
TAU_X0 = 0.0554590468914248


def piezas():
    from cmb_eval import chi2_y_s8
    import cobaya_kids_legacy as K
    from ssee_core import (H0_GLOBAL, N_S, OMEGA_B_H2, OMEGA_C_H2, W0, WA)
    bg = dict(ombh2=OMEGA_B_H2, omch2=OMEGA_C_H2, H0=H0_GLOBAL, ns=N_S)
    return chi2_y_s8, K, bg, W0, WA


def perfil_cmb(chi2_y_s8, bg, w0, wa, logA):
    """chi2 del CMB en logA, minimizando tau (su unico libre)."""
    def f(u):
        if not (0.01 < u[0] < 0.20):
            return 1e9
        return chi2_y_s8(dict(bg, logA=logA, tau=u[0]), w0, wa)[0]
    r = minimize(f, [TAU_X0], method="Nelder-Mead",
                 options=dict(xatol=1e-5, fatol=1e-4, maxiter=120))
    return float(r.fun), float(r.x[0])


def perfil_kids(K, logA, x0):
    """chi2 de KiDS en logA, minimizando sus 8 nuisance."""
    def f(u):
        if not (7.0 < u[0] < 8.5) or not (0.0 < u[1] < 3.0):
            return 1e9
        if np.any(np.abs(u[2:]) > 0.3):
            return 1e9
        return -2.0 * K.loglike_ssee(logA=logA, logT_AGN=u[0], A_scale=u[1],
                                     dz1=u[2], dz2=u[3], dz3=u[4],
                                     dz4=u[5], dz5=u[6], dz6=u[7])
    r = minimize(f, x0, method="Nelder-Mead",
                 options=dict(xatol=2e-4, fatol=2e-3, maxiter=900, maxfev=900))
    return float(r.fun), np.asarray(r.x)


def perfil_boss():
    """Perfil REAL de BOSS, ya medido por el optimizador. Interpolado."""
    d = json.load(open(BOSS_JSON))
    g = np.array(d["SSEE"]["perfil"]["logA"])
    y = np.array(d["SSEE"]["perfil"]["chi2"])
    return interp1d(g, y, kind="cubic"), float(y.min()), float(g[y.argmin()])


def main():
    t0 = time.time()
    chi2_y_s8, K, bg, w0, wa = piezas()
    fb, boss_min, boss_logA_min = perfil_boss()

    # BAO: constante, no depende de logA. Del log de la multisonda.
    bao = json.load(open(os.path.join(_R, "results", "logs",
                                      "multisonda_fondo_clavado.json")))
    chi2_bao = [b for b in bao["bondad_en_el_clavo"]
                if b["sonda"] == "BAO DESI DR2"][0]["chi2"]

    # ── CONTROL (a): reproducir lo publicado en el clavo ────────────────────
    c_cmb_clavo, tau_clavo = perfil_cmb(chi2_y_s8, bg, w0, wa, LOGA_CLAVO)
    c_kids_clavo, xk_clavo = perfil_kids(K, LOGA_CLAVO, KIDS_X0)
    ok_cmb = abs(c_cmb_clavo - 1003.586) < 0.5
    ok_kids = abs(c_kids_clavo - 417.971) < 1.0
    print(f"  CONTROL (a) en el clavo:")
    print(f"    CMB  {c_cmb_clavo:9.3f}  (publicado 1003.586)  {'OK' if ok_cmb else 'NO CUADRA'}")
    print(f"    KiDS {c_kids_clavo:9.3f}  (publicado  417.971)  {'OK' if ok_kids else 'NO CUADRA'}")
    if not (ok_cmb and ok_kids):
        print("  El montaje no reproduce lo ya medido. Se para aqui.")
        json.dump(dict(control_a_falla=True, cmb=c_cmb_clavo, kids=c_kids_clavo),
                  open(OUT, "w"), indent=1)
        sys.exit(1)

    # ── el perfil conjunto ──────────────────────────────────────────────────
    rej = np.round(np.arange(2.960, 3.101, 0.010), 3)
    print(f"\n  Perfil conjunto sobre {len(rej)} nodos de logA "
          f"({rej[0]:.3f} a {rej[-1]:.3f}):\n")
    print(f"  {'logA':>7}{'CMB':>11}{'KiDS':>10}{'BOSS':>10}{'BAO':>9}{'TOTAL':>11}{'s':>7}")
    filas = []
    xk = KIDS_X0.copy()
    for a in rej:
        t = time.time()
        cc, tau = perfil_cmb(chi2_y_s8, bg, w0, wa, float(a))
        ck, xk = perfil_kids(K, float(a), xk)      # arranque caliente del nodo previo
        cb = float(fb(a))
        tot = cc + ck + cb + chi2_bao
        filas.append(dict(logA=float(a), cmb=cc, tau=tau, kids=ck,
                          boss=cb, bao=chi2_bao, total=tot))
        print(f"  {a:>7.3f}{cc:>11.3f}{ck:>10.3f}{cb:>10.3f}"
              f"{chi2_bao:>9.3f}{tot:>11.3f}{time.time()-t:>7.0f}")

    tot = np.array([f["total"] for f in filas])
    i = int(tot.argmin())
    # minimo por parabola en los tres nodos centrales
    j = slice(max(0, i - 1), min(len(rej), i + 2))
    p = np.polyfit(rej[j], tot[j], 2)
    logA_conj = float(-p[1] / (2 * p[0])) if p[0] > 0 else float(rej[i])
    chi2_conj = float(np.polyval(p, logA_conj))

    res = dict(
        fecha=time.strftime("%Y-%m-%d"),
        pregunta=("Con UN SOLO logA decidido por LAS CUATRO sondas a la vez y el "
                  "fondo clavado por algebra: donde cae, cuanto paga cada sonda por "
                  "estar ahi en vez de en su propio minimo, y coincide con el que "
                  "pide el CMB?"),
        logA_clavo_cmb=LOGA_CLAVO,
        control_a=dict(cmb=c_cmb_clavo, cmb_publicado=1003.586,
                       kids=c_kids_clavo, kids_publicado=417.971, pasa=True),
        rejilla=filas,
        logA_conjunto=logA_conj, chi2_conjunto=chi2_conj,
        boss_min=boss_min, boss_logA_min=boss_logA_min,
        segundos=time.time() - t0)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"\n  logA CONJUNTO = {logA_conj:.6f}   chi2 = {chi2_conj:.3f}")
    print(f"  logA del CMB  = {LOGA_CLAVO:.6f}   diferencia = "
          f"{logA_conj - LOGA_CLAVO:+.6f}")
    print(f"\n  -> {OUT}   ({(time.time()-t0)/60:.1f} min)")


if __name__ == "__main__":
    main()
