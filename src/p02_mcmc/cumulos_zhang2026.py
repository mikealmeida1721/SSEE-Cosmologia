#!/usr/bin/env python3
"""cumulos_zhang2026.py — la prueba de cumulos de Paper 2 contra la tabla REAL de Zhang+2026.

POR QUE (2026-10-01). Paper 2 cita a Zhang, Hasani Zonoozi & Kroupa 2026
(arXiv:2602.06082) como fuente de Coma, A2029, A478 y el Bullet. Leida la
fuente: Coma y el Bullet NO estan en sus tablas; A2029 y A478 si, pero con
otros numeros (A2029: M_tot,IG 1.97 y M_N,dyn 12.77, no 2.2 y 12.0; A478:
M_N,dyn 11.45, no 8.0). Los datos de abril no salen del articulo citado.
Aqui la prueba se rehace con TODAS las filas de sus Tablas II y III (46
sistemas, sin escoger), leidas del extracto literal data/raw/zhang2026/.

LOS DOS MODELOS, ambos sin parametros libres (el control R53 es ΛCDM):
  SSEE   M_dyn = KAL0 (1 + f_nu) M_tot,IG     (IGIMF, como en Paper 2)
  ΛCDM   M_dyn = (Omega_m/Omega_b) M_tot,IMF  (IMF canonica, fraccion cosmica de Planck 2018)
contra M_N,dyn (masa dinamica newtoniana dentro del radio virial, Brownstein &
Moffat 2006, segun el pie de las tablas). Variantes: SSEE con f_nu = 0, SSEE
con IMF canonica, ΛCDM con IGIMF.
ERROR: sigma^2 = sigma_dyn^2 + (k sigma_bar)^2, con el lado de la barra
asimetrica que mira hacia la prediccion; cada barra con piso 0.01/sqrt(12), el
error de redondeo de una tabla a dos decimales (algunas barras salen «0.00»).
CONTROL de lectura: el parser tiene que leer 13 + 33 filas y reproducir, de la
tabla, A2029 (1.71, 1.97, 12.77) y A0478 (11.45) tal como estan en el PDF.

Salida: results/logs/cumulos_zhang2026.json
"""
import json
import os
import re
import sys

import numpy as np
from scipy import stats

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
import ssee_core as S  # noqa: E402
from lcdm_planck import LCDM_PLANCK as LP  # noqa: E402
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)

FUENTE = os.path.join(_R, "data", "raw", "zhang2026", "tablas_II_III.tex")
F_NU = 0.020   # ORIGEN-VALOR: 0.020 — f_nu de Paper 2 (ec. M_SSEE), el mismo que cumulos_7.py; su origen esta en revision
C_NU = 93.14   # ORIGEN-VALOR: 93.14 — clausura nu del nucleo (omega_nu = Sum m_nu / 93.14)
SIG_RED = 0.01 / np.sqrt(12)   # piso: la tabla redondea a 2 decimales (uniforme en +-0.005); hay barras impresas «0.00»
COLS = ["z", "M_gas", "M_g_IMF", "M_g_IG", "M_I_IMF", "M_I_IG", "M_tot_IMF", "M_tot_IG", "M_M_dyn", "M_N_dyn", "f_ICL"]

_num = re.compile(r"\$?([0-9.]+)(?:\^\{([0-9.]+)\}_\{([0-9.]+)\})?\$?")


def lee():
    filas, tabla = [], None
    for ln in open(FUENTE):
        if "label{WINGS_table}" in ln:
            tabla = "II_WINGS"
        if "label{2MASS_table}" in ln:
            tabla = "III_2MASS"
        if "&" not in ln or "Name" in ln or tabla is None:
            continue
        celdas = [c.strip() for c in ln.split("\\\\")[0].split("&")]
        if len(celdas) != 12:
            continue
        d = dict(nombre=celdas[0], tabla=tabla)
        for col, c in zip(COLS, celdas[1:]):
            m = _num.fullmatch(c)
            v, up, lo = m.group(1), m.group(2), m.group(3)
            d[col] = float(v)
            d[col + "_mas"] = float(up) if up else 0.0
            d[col + "_menos"] = float(lo) if lo else 0.0
        filas.append(d)
    return filas


F = lee()
n2 = sum(f["tabla"] == "II_WINGS" for f in F)
n3 = sum(f["tabla"] == "III_2MASS" for f in F)
P = {f["nombre"]: f for f in F}
ctl = dict(filas_II=n2, filas_III=n3,
           A2029=[P["A2029"]["M_tot_IMF"], P["A2029"]["M_tot_IG"], P["A2029"]["M_N_dyn"]],
           A0478_M_N_dyn=P["A0478"]["M_N_dyn"])
lectura_pasa = (n2 == 13 and n3 == 33 and ctl["A2029"] == [1.71, 1.97, 12.77] and ctl["A0478_M_N_dyn"] == 11.45)
print(f"  lectura: {n2} + {n3} filas; A2029 {ctl['A2029']}; A0478 M_N,dyn {ctl['A0478_M_N_dyn']} -> {'PASA' if lectura_pasa else 'NO PASA'}")
if not lectura_pasa:
    sys.exit("la lectura de la tabla no reproduce la fuente: no se sigue")

om_lcdm = LP["ombh2"] + LP["omch2"] + LP["mnu"] / C_NU
K_LCDM = om_lcdm / LP["ombh2"]
K_SSEE = S.KAL0 * (1 + F_NU)
F_NU_COSMICO = S.OMEGA_NU_H2 / S.OMEGA_M_H2   # lo que P2 dice que es f_nu: la fraccion cosmica de masa en neutrinos
# SSEE en relatividad general (2026-10-01): el modelo vigente NO modifica la
# gravedad (P7: alpha_T = alpha_M = alpha_B = 0 => mu = 1, P8). Un cumulo ve
# entonces la materia total de SSEE, como en LCDM: M_dyn = (omega_m/omega_b) M_bar,
# con omega_m y omega_b del nucleo. La formula con KAL0 viene del marco MOND de abril.
K_SSEE_RG = S.OMEGA_M_H2 / S.OMEGA_B_H2
DESC_RG = dict(bariones=1.0, materia_oscura_fria=S.OMEGA_C_H2 / S.OMEGA_B_H2,
               kal0_por_ns=S.KAL0 * S.N_S, neutrinos=S.OMEGA_NU_H2 / S.OMEGA_B_H2)
assert abs(sum(DESC_RG[k] for k in ("bariones", "materia_oscura_fria", "neutrinos")) - K_SSEE_RG) < 1e-12
assert abs(DESC_RG["materia_oscura_fria"] - DESC_RG["kal0_por_ns"]) < 1e-12   # omega_c = KAL0 omega_b n_s
MODELOS = {"ssee": ("M_tot_IG", K_SSEE), "ssee_rg": ("M_tot_IMF", K_SSEE_RG), "ssee_rg_igimf": ("M_tot_IG", K_SSEE_RG), "ssee_fnu0": ("M_tot_IG", S.KAL0),
           "ssee_fnu_cosmico": ("M_tot_IG", S.KAL0 * (1 + F_NU_COSMICO)), "ssee_imf": ("M_tot_IMF", K_SSEE),
           "lcdm": ("M_tot_IMF", K_LCDM), "lcdm_igimf": ("M_tot_IG", K_LCDM)}


def chi2_fila(f, col, k):
    pred, obs = k * f[col], f["M_N_dyn"]
    arriba = pred > obs   # la barra que mira hacia la prediccion
    s_obs = max(f["M_N_dyn_mas"] if arriba else f["M_N_dyn_menos"], SIG_RED)
    s_bar = max(f[col + "_menos"] if arriba else f[col + "_mas"], SIG_RED)
    s2 = s_obs ** 2 + (k * s_bar) ** 2
    return (pred - obs) ** 2 / s2, (pred - obs) / np.sqrt(s2), pred / obs


res = {}
for m, (col, k) in MODELOS.items():
    filas = [dict(nombre=f["nombre"], tabla=f["tabla"], pred=k * f[col], obs=f["M_N_dyn"],
                  pull=float(chi2_fila(f, col, k)[1]), razon=float(chi2_fila(f, col, k)[2])) for f in F]
    c = sum(r["pull"] ** 2 for r in filas)
    rz = np.array([r["razon"] for r in filas])
    pv = float(stats.chi2.sf(c, len(F)))
    res[m] = dict(columna_bar=col, factor=k, chi2=float(c), N=len(F), chi2r=float(c / len(F)),
                  p_valor=pv, sigma_equiv=float(stats.norm.isf(pv / 2)),
                  razon_media=float(rz.mean()), razon_mediana=float(np.median(rz)),
                  razon_dispersion=float(rz.std(ddof=1)),
                  pulls_mayores_3=int(sum(abs(r["pull"]) > 3 for r in filas)),
                  peores=sorted(filas, key=lambda r: -abs(r["pull"]))[:5],
                  sub_P2=[r for r in filas if r["nombre"] in ("A2029", "A0478", "A2142")])
    print(f"  {m:11s} k={k:6.3f}  chi2/N = {c:9.2f}/{len(F)} = {c / len(F):7.2f}   "
          f"p {res[m]['p_valor']:.3g} ({res[m]['sigma_equiv']:.2f} sigma)   pred/obs mediana {np.median(rz):.3f}   |pull|>3: {res[m]['pulls_mayores_3']}")

out = dict(fecha=str(__import__("datetime").date.today()),
           fuente="Zhang, Hasani Zonoozi & Kroupa 2026, arXiv:2602.06082v1, Tablas II y III",
           no_estan_en_la_fuente=["Coma", "Bullet", "Perseus", "A2744"],
           control_lectura=dict(ctl, pasa=lectura_pasa),
           piso_redondeo=SIG_RED, K_SSEE=K_SSEE, K_SSEE_RG=K_SSEE_RG, descomposicion_RG=DESC_RG, f_nu_cosmico=F_NU_COSMICO, K_LCDM=K_LCDM, f_nu=F_NU, modelos=res,
           filas=F)
json.dump(con_acta(out, __file__, entradas=[FUENTE]),
          open(os.path.join(_R, "results", "logs", "cumulos_zhang2026.json"), "w"), indent=1)
