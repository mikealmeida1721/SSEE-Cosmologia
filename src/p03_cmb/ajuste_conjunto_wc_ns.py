#!/usr/bin/env python3
"""ajuste_conjunto_wc_ns.py — w_c y n_s LIBRES a la vez contra Planck crudo.

POR QUE (2026-09-30). Paper 8 (comentario junto a la identidad
w_c = KAL0*w_b*n_s) apoya su w_c en DOS medidas independientes: el perfil
chi2(w_c) (perfil_wc_cmb.py -> cmb_perfil_wc.json) y un ajuste conjunto con
n_s libre (results/logs/cmb_ajuste_conjunto_wc_ns.json). El segundo log entro
en el commit 01d4369 SIN el script que lo produjo (codigo suelto, perdido).
Una segunda medida que nadie puede re-correr no confirma nada: este script la
rehace.

COMO. Fondo fijo salvo (w_c, n_s); se minimiza chi2 plik_lite (cmb_eval) sobre
(w_c, n_s, logA, tau) con Nelder-Mead. SSEE: w_b y H del nucleo (el log viejo
usaba w_b redondeado y H0_ALG). LCDM: su propio fondo Planck 2018, w = -1.
  w_c_predicho = KAL0 * w_b * n_s(ajustado): lo que la identidad pide con el
  n_s que el dato prefiere.

CONTROLES (R53):
  (a) convergencia: se re-arranca Nelder-Mead desde el minimo encontrado con
      un simplex nuevo; si w_c se mueve mas de 0.2 sigma del perfil, el minimo
      no esta convergido y se dice.
  (b) solo SSEE: contra el log viejo, a 0.2 sigma del perfil. La fila LCDM del
      log viejo NO sirve de control: se reproduce (chi2 al 1e-3) solo
      evaluando LCDM con el w0, w_a de SSEE, o sea con el bug R64; medido el
      2026-09-30 al rehacerla.

Uso: ajuste_conjunto_wc_ns.py SSEE|LCDM   (una por proceso, 1 nucleo)
Salida: results/logs/cmb_ajuste_conjunto_wc_ns_{SSEE|LCDM}.json
"""
import json
import os
import sys

from scipy.optimize import minimize

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p03_cmb"))
import ssee_core as S  # noqa: E402
from cmb_eval import chi2_y_s8  # noqa: E402
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from lcdm_planck import LCDM_PLANCK as LP  # noqa: E402
from procedencia import con_acta  # noqa: E402

FONDOS = {
    "SSEE": dict(ombh2=S.OMEGA_B_H2, H0=S.H0_GLOBAL, w=S.W0, wa=S.WA,
                 arranque=[S.OMEGA_C_H2, S.N_S, 3.044, 0.054]),     # ORIGEN-VALOR: 3.044, 0.054 — arranque del minimizador (Planck 2018 logA, tau)
    "LCDM": dict(ombh2=LP["ombh2"], H0=LP["H0"], w=-1.0, wa=0.0,   # Planck 2018 (lcdm_planck.py)
                 arranque=[LP["omch2"], LP["ns"], 3.044, 0.054]),     # ORIGEN-VALOR: 3.044, 0.054 — arranque del minimizador (Planck 2018 logA, tau)
}
VIEJO = os.path.join(_R, "results", "logs", "cmb_ajuste_conjunto_wc_ns.json")
SIG_WC = 0.000246   # ORIGEN-VALOR: 0.000246 — anchura del perfil chi2(w_c), results/logs/cmb_perfil_wc.json

nombre = sys.argv[1]
f = FONDOS[nombre]


def obj(u):
    wc, ns, la, tau = u
    if not (0.10 < wc < 0.14 and 0.90 < ns < 1.03 and 1.5 < la < 4.5 and 0.011 < tau < 0.16):
        return 1e9
    return chi2_y_s8(dict(ombh2=f["ombh2"], H0=f["H0"], ns=ns, omch2=wc, logA=la, tau=tau),
                     f["w"], f["wa"])[0]


def nelder_mead(x0):
    return minimize(obj, x0, method="Nelder-Mead",
                    options=dict(xatol=1e-6, fatol=1e-4, maxiter=1500,
                                 initial_simplex=[x0,
                                                  [x0[0] + 0.0005] + x0[1:],
                                                  x0[:1] + [x0[1] + 0.004] + x0[2:],
                                                  x0[:2] + [x0[2] + 0.01, x0[3]],
                                                  x0[:3] + [x0[3] + 0.005]]))


r = nelder_mead(list(f["arranque"]))
wc, ns, la, tau = (float(x) for x in r.x)
r2 = nelder_mead([wc, ns, la, tau])           # control (a): re-arranque desde el minimo
conv = dict(w_c_rearranque=float(r2.x[0]), chi2_rearranque=float(r2.fun),
            dif_en_sigma=(float(r2.x[0]) - wc) / SIG_WC,
            pasa=bool(abs(r2.x[0] - wc) < 0.2 * SIG_WC))
ctl = dict(convergencia=conv)
if nombre == "SSEE":                          # control (b)
    viejo = json.load(open(VIEJO))[nombre]
    ctl["log_viejo"] = dict(w_c=viejo["w_c"], dif_en_sigma=(wc - viejo["w_c"]) / SIG_WC,
                            pasa=bool(abs(wc - viejo["w_c"]) < 0.2 * SIG_WC))
ctl["pasa"] = all(v["pasa"] for v in ctl.values() if isinstance(v, dict))
res = dict(modelo=nombre, w_b=f["ombh2"], H0=f["H0"], w_c=wc, n_s=ns, logA=la, tau=tau,
           chi2=float(r.fun), n_eval=int(r.nfev + r2.nfev), convergio=bool(r.success),
           w_c_predicho=float(S.KAL0 * f["ombh2"] * ns), control=ctl)
out = os.path.join(_R, "results", "logs", f"cmb_ajuste_conjunto_wc_ns_{nombre}.json")
json.dump(con_acta(res, __file__, entradas=[VIEJO]), open(out, "w"), indent=1)
print(f"{nombre}: w_c {wc:.6f}  n_s {ns:.5f}  logA {la:.4f}  tau {tau:.4f}  chi2 {r.fun:.4f}  "
      f"({res['n_eval']} eval)  controles {ctl}")
