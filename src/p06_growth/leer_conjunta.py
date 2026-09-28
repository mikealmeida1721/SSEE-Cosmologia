#!/usr/bin/env python3
"""leer_conjunta.py — lee la corrida CONJUNTA y la compara sonda por sonda.

LA PREGUNTA (de Mike, literal): con el fondo clavado por algebra Y logA clavado
al del CMB, una corrida CONJUNTA, que da a cada sonda el mismo chi2 que su
corrida INDIVIDUAL? Si lo da, juntar sondas no crea sesgos. Si no lo da, el
problema esta en las sondas, no en el modelo.

NO se suma nada a mano. Cada chi2 se LEE de la cadena conjunta, en su punto de
mejor ajuste conjunto.

REFERENCIAS INDIVIDUALES
  CMB  plik_lite TTTEEE+lowT+lowE   1003.5860   (cmb_dbic_tau_ajustado.json)
  KiDS KiDS-Legacy xi_pm             417.9710   (corrida sseefijo)
  BOSS DR12 P(k) LPT                 de boss_clavado, MISMA escala marginal
       (la escala REAL del optimizador es 197.438 -> 198.07 clavado = 0.63;
        son DOS escalas distintas y no se mezclan)
  BAO  DESI DR2                       constante, cero libres. Se CALCULA aqui
       con r_d y distancias de CAMB (bao_camb.chi2_desi en el clavo: 11.406).
       El literal viejo 10.8588 usaba la formula de r_d, 0.13 % larga
       (control C3 de lcdm_conjunta, 2026-09-27).
"""
import glob
import json
import os
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CAD = "/mnt/datos/SSEE_data/chains_p6/conjunta"
OUT = os.path.join(_R, "results", "logs", "conjunta_vs_individual.json")
sys.path.insert(0, os.path.join(_R, "src"))


def _chi2_bao_clavo():
    from bao_camb import chi2_desi
    from rd_camb import rd_mpc
    from ssee_core import H0_GLOBAL, OMEGA_B_H2, OMEGA_M_H2
    return chi2_desi(H0_GLOBAL, rd_mpc(OMEGA_B_H2, OMEGA_M_H2))


REF = dict(cmb=1003.5860397789045, kids=417.971, bao=_chi2_bao_clavo())


def carga(base):
    fs = sorted(glob.glob(f"{CAD}/{base}.[0-9]*.txt"))
    if not fs:
        sys.exit(f"no hay cadenas de {base}")
    cols = open(fs[0]).readline().lstrip("#").split()
    d = np.vstack([np.loadtxt(f, ndmin=2) for f in fs])
    return cols, d, len(fs)


def rminus1(base):
    p = f"{CAD}/{base}.progress"
    return float(open(p).read().split("\n")[-2].split()[-1]) if os.path.exists(p) else float("nan")


def main():
    cc, dc, nc = carga("conjunta")
    i = {k: cc.index(k) for k in cc}
    tot = dc[:, i["chi2"]]
    j = int(tot.argmin())
    conj = {s: float(dc[j, i[f"chi2__{s}"]]) for s in ("cmb", "kids", "boss")}
    # cuanto podria bajar cada sonda POR SU CUENTA dentro de la misma cadena:
    # cota inferior de lo que cede por estar en el punto conjunto
    solo = {s: float(dc[:, i[f"chi2__{s}"]].min()) for s in ("cmb", "kids", "boss")}

    # CONTROL del arranque comun: las 4 cadenas de la conjunta salieron del
    # MISMO punto inicial (Cobaya no sorteo la referencia). Eso no invalida el
    # resultado, pero hace que R-1 pueda parecer bajo antes de tiempo. El
    # control es exigir que CADA cadena, por separado, de el mismo chi2 por
    # sonda: si el arranque comun hubiera falseado algo, no coincidirian.
    por_cadena = []
    for f in sorted(glob.glob(f"{CAD}/conjunta.[0-9]*.txt")):
        dd = np.loadtxt(f, ndmin=2)
        k = int(dd[:, i["chi2"]].argmin())
        por_cadena.append(dict(
            cadena=os.path.basename(f), muestras=int(dd.shape[0]),
            **{s_: float(dd[k, i[f"chi2__{s_}"]]) for s_ in ("cmb", "kids", "boss")}))

    cb, db, nb = carga("boss_clavado")
    ib = cb.index("chi2__boss")
    boss_ind = float(db[:, ib].min())

    ind = dict(cmb=REF["cmb"], kids=REF["kids"], boss=boss_ind)
    filas = []
    for s in ("cmb", "kids", "boss"):
        d = conj[s] - ind[s]
        filas.append(dict(sonda=s, individual=ind[s], conjunta=conj[s],
                          delta=d, min_en_cadena_conjunta=solo[s]))
    t_conj = sum(conj.values()) + REF["bao"]
    t_ind = sum(ind.values()) + REF["bao"]

    res = dict(
        fecha="2026-09-26",
        pregunta=("Corrida CONJUNTA con el fondo clavado por algebra y logA "
                  "clavado al del CMB: da a cada sonda el mismo chi2 que su "
                  "corrida individual?"),
        logA_clavo=3.0448340130228546,
        muestras_conjunta=int(dc.shape[0]), cadenas_conjunta=nc,
        Rminus1_conjunta=rminus1("conjunta"),
        muestras_boss=int(db.shape[0]), cadenas_boss=nb,
        Rminus1_boss=rminus1("boss_clavado"),
        por_sonda=filas,
        control_arranque_comun=dict(
            nota=("las 4 cadenas salieron del mismo punto inicial; el control "
                  "es que cada una de el mismo chi2 por sonda"),
            por_cadena=por_cadena),
        bao=dict(chi2=REF["bao"], libres=0,
                 nota="constante: fuera del muestreador, no puede mover nada"),
        total_conjunta=t_conj, total_individual=t_ind,
        total_delta=t_conj - t_ind)
    json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)

    print(f"\n  conjunta: {dc.shape[0]} muestras, {nc} cadenas, "
          f"R-1 = {res['Rminus1_conjunta']:.4f}")
    print(f"  boss_clavado: {db.shape[0]} muestras, {nb} cadenas, "
          f"R-1 = {res['Rminus1_boss']:.4f}\n")
    print(f"  {'sonda':>6}{'individual':>13}{'conjunta':>12}{'delta':>10}")
    for f in filas:
        print(f"  {f['sonda']:>6}{f['individual']:>13.3f}"
              f"{f['conjunta']:>12.3f}{f['delta']:>+10.3f}")
    print(f"  {'BAO':>6}{REF['bao']:>13.3f}{REF['bao']:>12.3f}{0.0:>+10.3f}")
    print(f"  {'TOTAL':>6}{t_ind:>13.3f}{t_conj:>12.3f}"
          f"{t_conj - t_ind:>+10.3f}")
    print("\n  CONTROL arranque comun --- chi2 por sonda, cadena a cadena:")
    print(f"  {'cadena':>14}{'N':>8}{'CMB':>11}{'KiDS':>10}{'BOSS':>10}")
    for c in por_cadena:
        print(f"  {c['cadena']:>14}{c['muestras']:>8}{c['cmb']:>11.3f}"
              f"{c['kids']:>10.3f}{c['boss']:>10.3f}")
    print(f"\n  -> {OUT}")


if __name__ == "__main__":
    main()
