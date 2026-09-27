#!/usr/bin/env python3
"""covmat_conjunta.py — matriz de PROPUESTA bloque-diagonal para la conjunta.

POR QUE HACE FALTA. Medido 2026-09-26: la conjunta arrancada sin covmat daba
1.8 muestras/min/cadena. Cobaya no comprueba convergencia hasta 40*d = 1080
muestras por cadena, o sea 10 h para el PRIMER R-1, y varios multiplos de eso
para bajar de 0.05. Y boss_clavado, con solo 18 libres y sin covmat, tenia R-1
SUBIENDO (0.159 -> 2.199 en 5 min): la cadena descubria la anchura del
posterior en vez de muestrearlo.

QUE CAMBIA Y QUE NO. La covmat es la matriz de la PROPUESTA del Metropolis: no
entra en la verosimilitud ni en el prior, asi que NO puede mover el posterior
ni ningun chi2. Solo cambia por donde salta la cadena. Con propuesta diagonal
del prior, casi todo salto se rechaza; con la forma real del posterior, se
acepta. Es el mismo muestreo, no otro.

DE DONDE SALE CADA BLOQUE --- y ninguno del resultado que se quiere medir:
  tau   (1)  curvatura de chi2_CMB(tau) con logA clavado, MEDIDA aqui:
             sigma^2 = 2 / (d2chi2/dtau2). No es un numero tecleado.
  KiDS  (8)  kids_legacy/sseefijo.covmat --- la corrida INDIVIDUAL de KiDS con
             A_s clavado, la misma que da el 417.971 de referencia.
  BOSS (18)  boss/ssee.covmat --- la corrida convergida de BOSS, quitando su
             columna logA (aqui logA no se muestrea).

Bloque-diagonal: se da la forma de cada sonda por separado y se deja que
Cobaya aprenda las correlaciones CRUZADAS sobre la marcha. Justamente esas
cruzadas son lo que la prueba quiere ver, asi que no se le regalan.

CONTROL (R53). La covmat tiene que ser simetrica y definida positiva (todos
sus autovalores > 0): si no, no es una covarianza y Cobaya la rechazaria en
silencio pasando a la diagonal. Se comprueba y se imprime.
"""
import os
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p03_cmb"))
sys.path.insert(0, os.path.join(_R, "src", "p06_growth"))

CH = "/mnt/datos/SSEE_data/chains_p6"
OUT = f"{CH}/conjunta/propuesta_conjunta.covmat"
LOGA_CLAVO = 3.0448340130228546
TAU0 = 0.0554590468914248


def lee(path, quita=()):
    nom = open(path).readline().lstrip("#").split()
    M = np.loadtxt(path)
    keep = [i for i, n in enumerate(nom) if n not in quita]
    return [nom[i] for i in keep], M[np.ix_(keep, keep)]


def sigma_tau():
    """sigma(tau) por la curvatura de chi2_CMB(tau), con logA clavado."""
    from cmb_eval import chi2_y_s8
    from ssee_core import H0_GLOBAL, N_S, OMEGA_B_H2, OMEGA_C_H2, W0, WA
    bg = dict(ombh2=OMEGA_B_H2, omch2=OMEGA_C_H2, H0=H0_GLOBAL, ns=N_S,
              logA=LOGA_CLAVO)
    h = 0.004
    ts = np.array([TAU0 - h, TAU0, TAU0 + h])
    cs = np.array([chi2_y_s8(dict(bg, tau=float(t)), W0, WA)[0] for t in ts])
    d2 = (cs[0] - 2 * cs[1] + cs[2]) / h ** 2
    print(f"  chi2_CMB(tau) en {ts.round(6)} = {cs.round(4)}")
    print(f"  d2chi2/dtau2 = {d2:.1f}   ->  sigma(tau) = {np.sqrt(2/d2):.6f}")
    if d2 <= 0:
        sys.exit("  la curvatura no es positiva: tau no esta en un minimo")
    return float(np.sqrt(2.0 / d2))


def main():
    st = sigma_tau()
    nk, Mk = lee(f"{CH}/kids_legacy/sseefijo.covmat")
    nb, Mb = lee(f"{CH}/boss/ssee.covmat", quita=("logA",))
    nom = ["tau"] + nk + nb
    d = len(nom)
    M = np.zeros((d, d))
    M[0, 0] = st ** 2
    M[1:1+len(nk), 1:1+len(nk)] = Mk
    M[1+len(nk):, 1+len(nk):] = Mb

    # CONTROL R53
    sim = float(np.abs(M - M.T).max())
    ev = np.linalg.eigvalsh(M)
    print(f"\n  CONTROL: {d} parametros  ({1} tau + {len(nk)} KiDS + {len(nb)} BOSS)")
    print(f"    asimetria maxima  {sim:.3e}   {'OK' if sim < 1e-12 else 'NO'}")
    print(f"    autovalor minimo  {ev.min():.3e}   "
          f"{'OK (definida positiva)' if ev.min() > 0 else 'NO: no es covarianza'}")
    if not (sim < 1e-12 and ev.min() > 0):
        sys.exit(1)

    np.savetxt(OUT, M, header=" ".join(nom))
    print(f"\n  -> {OUT}")


if __name__ == "__main__":
    main()
