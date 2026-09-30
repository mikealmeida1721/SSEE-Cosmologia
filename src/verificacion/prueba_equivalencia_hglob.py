#!/usr/bin/env python3
"""¿Mueve algun resultado el cambio H0_ALG -> H0_GLOBAL del 2026-09-28 (c8d1566)?

POR QUE. Ese commit cambio en ~15 scripts el H de fondo de 3(phi+pi)^2 =
67.962137 (el blanco puro) a H_glob = SH0ES*(1-f_screen) = 67.962142 (la
salida de la cascada). Son 4.2e-06 km/s/Mpc. R35 marco como rancios los logs
de esos scripts, y hace bien: «es despreciable» se MIDE, no se supone.

QUE MIDE. El chi2 de cada verosimilitud que usa ese H, con los dos valores y
todo lo demas igual (mejor punto de SSEE):
  CMB   plik_lite TTTEEE+lowT+lowE (cmb_eval.chi2_y_s8)
  BAO   DESI DR2 con distancias y r_d de CAMB (chi2_bao_posterior.chi2_bao)
  KiDS  KiDS-Legacy xi+- (cobaya_kids_legacy.loglike, fondo SSEE)

CRITERIO (declarado antes): |dchi2| < 1e-3 en las tres.
CONTROL (R53): el mismo calculo con un salto de H 1000 veces mayor (4.2e-3)
tiene que dar un |dchi2| mayor que el del cambio real: si no, el evaluador no
esta viendo H y el «cero» no prueba nada.

Salida: results/logs/prueba_equivalencia_hglob.json
"""
import json
import os
import sys

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
for d in ("src", "src/p03_cmb", "src/p02_mcmc", "src/p06_growth"):
    sys.path.insert(0, os.path.join(R, d))
import ssee_core as S  # noqa: E402

H_VIEJO, H_NUEVO = S.H0_ALG, S.H0_GLOBAL
SALTO = 1000 * (H_NUEVO - H_VIEJO)
mejor = json.load(open(os.path.join(R, "results/logs/cmb_dbic_tau_ajustado.json")))["SSEE"]["mejor"]


def cmb(H):
    from cmb_eval import chi2_y_s8
    c, _ = chi2_y_s8(dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2, H0=H, ns=S.N_S,
                          logA=mejor["logA"], tau=mejor["tau"]), S.W0, S.WA)
    return float(c)


def bao(H):
    from chi2_bao_posterior import chi2_bao
    return float(chi2_bao(H, S.OMEGA_B_H2)[0])


def kids(H):
    import cobaya_kids_legacy as K
    K.SSEE_BG["h0"] = H / 100.0
    K._CACHE.clear() if hasattr(K, "_CACHE") else None
    # nuisances en su centro de prior: aqui solo importa la DIFERENCIA
    return float(-2 * K.loglike("SSEE", K.LOGA_CMB_SSEE, 7.8, 1.0, [0.0] * 6))


res = dict(fecha=str(__import__("datetime").date.today()), H_viejo=H_VIEJO, H_nuevo=H_NUEVO,
           dH=H_NUEVO - H_VIEJO, criterio="|dchi2| < 1e-3 en CMB, BAO y KiDS (declarado antes)",
           sondas={})
for nom, f in (("CMB", cmb), ("BAO", bao), ("KiDS", kids)):
    a, b, c = f(H_VIEJO), f(H_NUEVO), f(H_VIEJO + SALTO)
    res["sondas"][nom] = dict(chi2_viejo=a, chi2_nuevo=b, dchi2=b - a,
                              dchi2_control_salto_x1000=c - a,
                              control_ve_H=bool(abs(c - a) > abs(b - a)))
    print(f"  {nom:5s} chi2 {a:.6f} -> {b:.6f}  d={b - a:+.2e}   control x1000 d={c - a:+.2e}")
res["pasa"] = all(abs(v["dchi2"]) < 1e-3 and v["control_ve_H"] for v in res["sondas"].values())
json.dump(res, open(os.path.join(R, "results/logs/prueba_equivalencia_hglob.json"), "w"), indent=1)
print("  ->", "PASA" if res["pasa"] else "NO PASA")
