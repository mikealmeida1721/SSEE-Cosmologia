#!/usr/bin/env python3
"""h0_por_profundidad.py — OP-8b: ¿el apantallamiento de Paper 9 se promedia con la profundidad? (2026-10-03)

POR QUE. Hipótesis de Mike (OP-8b, escrita y commiteada ANTES de esta corrida,
commit f2f7472): el apantallamiento f_screen sería una proyección del crecimiento
local sobre la medida de H. Si es un efecto del VOLUMEN local que se promedia al
crecer el volumen, el H0 que da cada capa de profundidad del flujo de Hubble debe
BAJAR con z hacia H_glob. Si es propiedad de la escalera de distancias (o vive solo
en el volumen de los calibradores), todas las capas dan el mismo H0.

DATOS. Pantheon+SH0ES (Scolnic+2022, Brout+2022): 77 filas de calibradores con
distancia Cefeida (CEPH_DIST) y 277 SNe del flujo de Hubble de SH0ES
(USED_IN_SH0ES_HF, 0.023 < z < 0.15), con la covarianza STAT+SYS completa
(incluye la de los anfitriones Cefeida). Nada se tabula a mano.

AJUSTE (mínimos cuadrados generalizados, exacto: el modelo es lineal).
  m_i = M_B + CEPH_DIST_i                         (calibradores)
  m_i = M_B + g_i(z) + a(z_i),  a = -5 log10 H0   (flujo de Hubble)
  g_i = 5 log10[(1+zHEL) c ∫0^zHD dz/E(z)] + 25   (forma de d_L; el modelo entra solo aquí)
  a(z) = a0 + a1 (z - z_lo)                       (lineal en z: da H0(z_lo) y H0(z_hi))
  y aparte a_k por cuartil de z.
Forma de E(z) con los ingredientes de cada modelo: SSEE (w0, wa de ssee_core,
Om = 0.308881 derivado) y LCDM Planck 2018 (lcdm_planck.py). La radiación se
desprecia (< 1e-4 a z < 0.15).

CRITERIOS (copiados de OP-8b, fijados antes):
  APOYA   : H0(0.023) - H0(0.15) > 0 a >= 2 sigma
  EXCLUYE : caída compatible con 0 (< 2 sigma) y H0 de la capa más profunda a > 3 sigma sobre H_glob
  NO CONCLUYE: lo demás
REVISIÓN (2026-10-03, decisión de Mike, DESPUÉS de ver el dato; el original se conserva y se reporta):
  el control plano del criterio original falló (56 % < 80 %) porque sumaba el ±0.968 de H_glob, que
  sale del mismo ±1.04 de SH0ES que ya carga la calibración común de las capas. Ahora:
  EXCLUYE : caída < DELTA_REQ = H_SH0ES·f_screen a > 3 sigma (solo la caída: el M_B común se cancela)
  y se reporta la fracción máxima del apantallamiento que podría promediarse antes de z_hi (3 sigma).

CONTROLES (R53; si uno falla, la prueba no vale y el script se para).
  1. Reproducir Brout+2022, LCDM plano (SNe con zHD > 0.01 + calibradores, Om libre):
     su H0 publicado 73.6 ± 1.1 se LEE del .tex del artículo; tolerancia 0.3.
  2. Catálogo simulado con H0 que cae linealmente de 73 a 68 entre z_lo y z_hi
     (mismas z, misma covarianza): el valor esperado (sin ruido) TIENE que dar APOYA,
     y al menos el 80 % de 200 realizaciones con ruido de la covarianza también.
  3. Igual con H0 plano en 73: TIENE que dar EXCLUYE.

Salida: results/logs/h0_por_profundidad.json
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy.integrate import cumulative_trapezoid

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from ssee_core import W0, WA, H0_GLOBAL, SIG_H0_GLOBAL, OMEGA_M_TOTAL, H0_SH0ES, F_SCREEN  # noqa: E402
from lcdm_planck import LCDM_PLANCK  # noqa: E402
from procedencia import con_acta  # noqa: E402

PP = "/mnt/datos/SSEE_data/sn_ia/pantheon_plus"
DAT = f"{PP}/Pantheon+SH0ES.dat"
COV = f"{PP}/Pantheon+SH0ES_STAT+SYS.cov"
TEX = "/mnt/datos/SSEE_data/sn_ia/papers/2202.04077/main.tex"
OUT = os.path.join(_R, "results", "logs", "h0_por_profundidad.json")
C_KMS = 299792.458
Z_LO, Z_HI = 0.023, 0.15
rng = np.random.default_rng(20261003)

# --- H_glob, su sigma y Om de SSEE: de ssee_core (la cascada SH0ES·(1−f)), no tecleados ---
H_GLOB, H_GLOB_S, OM_SSEE = H0_GLOBAL, SIG_H0_GLOBAL, OMEGA_M_TOTAL
# Caída que exige la versión de VOLUMEN si el apantallamiento se promedia del todo antes de z_hi:
# el exceso local entero, H_SH0ES·f = H_SH0ES − H_glob.
DELTA_REQ = H0_SH0ES * F_SCREEN
h_l = LCDM_PLANCK["H0"] / 100.0
OM_LCDM = (LCDM_PLANCK["ombh2"] + LCDM_PLANCK["omch2"] + LCDM_PLANCK["mnu"] / 93.14) / h_l ** 2


def E_cpl(z, om, w0, wa):
    a = 1.0 / (1.0 + z)
    de = a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
    return np.sqrt(om * (1 + z) ** 3 + (1 - om) * de)


def integral(zs, om, w0=-1.0, wa=0.0):
    zz = np.linspace(0, zs.max() * 1.001, 20001)
    I = cumulative_trapezoid(1.0 / E_cpl(zz, om, w0, wa), zz, initial=0.0)
    return np.interp(zs, zz, I)


def g_forma(d, om, w0=-1.0, wa=0.0):
    return 5 * np.log10((1 + d.zHEL.values) * C_KMS * integral(d.zHD.values, om, w0, wa)) + 25


def gls(X, y, Cinv):
    F = X.T @ Cinv @ X
    Fi = np.linalg.inv(F)
    th = Fi @ (X.T @ Cinv @ y)
    r = y - X @ th
    return th, Fi, float(r @ Cinv @ r)


def H(a):
    return 10 ** (-a / 5)


# --- datos ---------------------------------------------------------------------
d_all = pd.read_csv(DAT, sep=r"\s+")
with open(COV) as fh:
    n = int(fh.readline())
    C_all = np.fromfile(fh, sep=" ", count=n * n).reshape(n, n)
assert n == len(d_all) == 1701


def sub(mask):
    idx = np.where(mask)[0]
    return d_all.iloc[idx].reset_index(drop=True), C_all[np.ix_(idx, idx)]


cal = d_all.IS_CALIBRATOR.values == 1
hf = (d_all.USED_IN_SH0ES_HF.values == 1) & ~cal
d, C = sub(cal | hf)
es_cal = d.IS_CALIBRATOR.values == 1
Cinv = np.linalg.inv(C)


def disenio_lineal(d, es_cal):
    X = np.zeros((len(d), 3))
    X[:, 0] = 1
    X[~es_cal, 1] = 1
    X[~es_cal, 2] = d.zHD.values[~es_cal] - Z_LO
    return X


def disenio_cuartiles(d, es_cal):
    zh = d.zHD.values
    cortes = np.quantile(zh[~es_cal], [0, .25, .5, .75, 1])
    k = np.clip(np.searchsorted(cortes, zh, side="right") - 1, 0, 3)
    X = np.zeros((len(d), 5))
    X[:, 0] = 1
    for j in range(4):
        X[(~es_cal) & (k == j), 1 + j] = 1
    return X, cortes


def evalua(y, X, Cinv):
    th, Fi, chi2 = gls(X, y, Cinv)
    a_lo, a_hi = th[1], th[1] + th[2] * (Z_HI - Z_LO)
    J_lo = np.array([0, 1, 0])
    J_hi = np.array([0, 1, Z_HI - Z_LO])
    k = np.log(10) / 5
    H_lo, H_hi = H(a_lo), H(a_hi)
    # caída = H_lo - H_hi; gradiente respecto de theta
    g = -k * (H_lo * J_lo - H_hi * J_hi)
    caida, s_caida = H_lo - H_hi, float(np.sqrt(g @ Fi @ g))
    s_hi = float(k * H_hi * np.sqrt(J_hi @ Fi @ J_hi))
    s_lo = float(k * H_lo * np.sqrt(J_lo @ Fi @ J_lo))
    return dict(M_B=th[0], H0_zlo=H_lo, H0_zlo_s=s_lo, H0_zhi=H_hi, H0_zhi_s=s_hi,
                caida=caida, caida_s=s_caida, caida_sigma=caida / s_caida,
                hondo_sobre_Hglob_sigma=(H_hi - H_GLOB) / np.hypot(s_hi, H_GLOB_S),
                deficit_sigma=(DELTA_REQ - caida) / s_caida,
                fraccion_max_3sigma=(caida + 3 * s_caida) / DELTA_REQ,
                chi2=chi2, N=len(y))


def veredicto_original(r):
    """Criterio de f2f7472, conservado. FALLA su control plano (56 % < 80 %): compara la capa
    honda con H_glob sumando el ±0.968 de H_glob, que sale del MISMO ±1.04 de SH0ES que ya
    lleva la calibración común de todas las capas ⟹ cuenta dos veces el mismo error."""
    if r["caida_sigma"] >= 2:
        return "APOYA"
    if abs(r["caida_sigma"]) < 2 and r["hondo_sobre_Hglob_sigma"] > 3:
        return "EXCLUYE"
    return "NO CONCLUYE"


def veredicto(r):
    """Criterio REVISADO (2026-10-03, decisión de Mike, DESPUÉS de ver el dato; declarado en OP-8b).
    Usa solo la caída, en la que el M_B común se cancela: EXCLUYE si la caída es menor que la que
    exige la versión de volumen (DELTA_REQ) a más de 3 sigma."""
    if r["caida_sigma"] >= 2:
        return "APOYA"
    if (DELTA_REQ - r["caida"]) / r["caida_s"] > 3:
        return "EXCLUYE"
    return "NO CONCLUYE"


# --- control 1: Brout+2022, LCDM plano ------------------------------------------
pub = re.search(r"^\\def\\fLCDMHPanSH\{\$([0-9.]+)\\pm([0-9.]+)\$\}", open(TEX).read(), re.M)
H_pub, H_pub_s = float(pub.group(1)), float(pub.group(2))
mB = (d_all.zHD.values > 0.01) | cal
dB, CB = sub(mB)
cB = dB.IS_CALIBRATOR.values == 1
CBinv = np.linalg.inv(CB)
mejor = None
# ORIGEN-VALOR: 0.0025 — paso de la rejilla en Ω_m (eleccion de resolucion, no un dato)
for om in np.arange(0.20, 0.45001, 0.0025):
    yB = dB.m_b_corr.values - np.where(cB, dB.CEPH_DIST.values, g_forma(dB, om))
    XB = np.zeros((len(dB), 2))
    XB[:, 0] = 1
    XB[~cB, 1] = 1
    th, Fi, chi2 = gls(XB, yB, CBinv)
    if mejor is None or chi2 < mejor[0]:
        mejor = (chi2, om, H(th[1]), np.log(10) / 5 * H(th[1]) * np.sqrt(Fi[1, 1]))
ctrl1 = dict(H0_publicado=H_pub, H0_publicado_s=H_pub_s, H0_aqui=mejor[2], H0_aqui_s=mejor[3],
             Om_aqui=mejor[1], chi2=mejor[0], N=len(dB), pasa=abs(mejor[2] - H_pub) < 0.3)
print(f"control 1 (Brout+2022 LCDM plano): {mejor[2]:.2f} ± {mejor[3]:.2f} (Om={mejor[1]:.3f}) "
      f"vs publicado {H_pub} ± {H_pub_s} -> {'PASA' if ctrl1['pasa'] else 'FALLA'}")
assert ctrl1["pasa"], "control 1 falla: la prueba no vale"

# --- la prueba, con cada modelo ---------------------------------------------------
modelos = {"SSEE": (OM_SSEE, W0, WA), "LCDM_Planck": (OM_LCDM, -1.0, 0.0)}
res_mod = {}
X = disenio_lineal(d, es_cal)
Xq, cortes = disenio_cuartiles(d, es_cal)
for nom, (om, w0, wa) in modelos.items():
    g = g_forma(d, om, w0, wa)
    y = d.m_b_corr.values - np.where(es_cal, d.CEPH_DIST.values, g)
    r = evalua(y, X, Cinv)
    thq, Fq, chi2q = gls(Xq, y, Cinv)
    k = np.log(10) / 5
    r["cuartiles"] = [dict(z_min=float(cortes[j]), z_max=float(cortes[j + 1]), H0=float(H(thq[1 + j])),
                           H0_s=float(k * H(thq[1 + j]) * np.sqrt(Fq[1 + j, 1 + j]))) for j in range(4)]
    r["veredicto"] = veredicto(r)
    r["veredicto_criterio_original"] = veredicto_original(r)
    r["Om"], r["w0"], r["wa"] = om, w0, wa
    res_mod[nom] = r
    print(f"{nom:12s} H0(z={Z_LO})={r['H0_zlo']:.2f}±{r['H0_zlo_s']:.2f}  H0(z={Z_HI})={r['H0_zhi']:.2f}±{r['H0_zhi_s']:.2f}  "
          f"caída {r['caida']:+.2f}±{r['caida_s']:.2f} ({r['caida_sigma']:+.2f}σ)  hondo−H_glob {r['hondo_sobre_Hglob_sigma']:.2f}σ  "
          f"-> {r['veredicto']} (criterio original: {r['veredicto_criterio_original']}; déficit {r['deficit_sigma']:.2f}σ, fracción máx 3σ {r['fraccion_max_3sigma']:.2f})")
    print("             cuartiles:", "  ".join(f"[{q['z_min']:.3f},{q['z_max']:.3f}] {q['H0']:.2f}±{q['H0_s']:.2f}" for q in r["cuartiles"]))

# --- controles 2 y 3: catálogos simulados (forma SSEE) -----------------------------
gS = g_forma(d, *modelos["SSEE"])
MB = res_mod["SSEE"]["M_B"]
L = np.linalg.cholesky(C)


def mock(H_de_z, ruido):
    a = -5 * np.log10(H_de_z(d.zHD.values))
    m = MB + np.where(es_cal, d.CEPH_DIST.values, gS + a)
    if ruido:
        m = m + L @ rng.standard_normal(len(d))
    return m - np.where(es_cal, d.CEPH_DIST.values, gS)


def baja(z):
    return 73.0 + (68.0 - 73.0) * (np.clip(z, Z_LO, Z_HI) - Z_LO) / (Z_HI - Z_LO)


def plano(z):
    return np.full_like(z, 73.0)


ctrl = {}
for nom, f, esperado in (("cae_73_a_68", baja, "APOYA"), ("plano_73", plano, "EXCLUYE")):
    r0 = evalua(mock(f, False), X, Cinv)
    rs = [evalua(mock(f, True), X, Cinv) for _ in range(200)]
    v0, vs = veredicto(r0), [veredicto(x) for x in rs]
    frac = vs.count(esperado) / len(vs)
    frac_orig = [veredicto_original(x) for x in rs].count(esperado) / len(rs)
    ctrl[nom] = dict(esperado=esperado, sin_ruido=v0, fraccion_con_ruido=frac,
                     criterio_original=dict(sin_ruido=veredicto_original(r0), fraccion_con_ruido=frac_orig),
                     pasa=(v0 == esperado and frac >= 0.8))
    print(f"control {nom}: sin ruido {v0}, con ruido {frac:.0%} {esperado} -> {'PASA' if ctrl[nom]['pasa'] else 'FALLA'}")
assert all(c["pasa"] for c in ctrl.values()), "un control simulado falla: la prueba no vale"

res = dict(fecha="2026-10-03", delta_requerida=DELTA_REQ, criterio_revisado="caida < delta_requerida a >3 sigma (declarado tras ver el dato)", hipotesis="OP-8b, Mike: apantallamiento como proyección del crecimiento local",
           criterios_commit="f2f7472", z_lo=Z_LO, z_hi=Z_HI, H_glob=H_GLOB, H_glob_s=H_GLOB_S,
           N_calibradores=int(es_cal.sum()), N_flujo=int((~es_cal).sum()),
           modelos=res_mod, control_brout=ctrl1, control_simulados=ctrl)
json.dump(con_acta(res, __file__, entradas=[DAT, COV, TEX]), open(OUT, "w"), indent=1,
          ensure_ascii=False, default=float)
print("->", OUT)
