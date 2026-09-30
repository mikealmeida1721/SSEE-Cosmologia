#!/usr/bin/env python3
"""s8_kids_legacy_camb.py — sigma8 y S8 del titular de Paper 6 (KiDS-Legacy), calculados.

POR QUE (2026-09-30). R74 encontro en CANONICAL cuatro valores del titular de
Paper 6 sin log: sigma8_ssee_unif 0.8153, S8_ssee_unif 0.8273 (la PREDICCION
con A_s clavado en el CMB), sigma8_kids_legacy 0.8075 +- 0.0160 y
S8_kids_legacy 0.8193 +- 0.0163 (A_s libre en la cizalla, «propagando +-1 sigma
de logA por CAMB»). La cadena con A_s fijo no guarda sigma8 (con A_s fijo es un
numero, no una distribucion), y nadie dejo el calculo. Este es.

COMO: la MISMA llamada de CAMB que usa la verosimilitud (kids_shear.run_camb,
fondo SSEE_BG de cobaya_kids_legacy), sigma8 = r.get_sigma8_0() (lineal,
independiente de logT_AGN), S8 = sigma8 * sqrt(Omega_m / 0.3) con Omega_m de
los propios parametros de CAMB (omch2 + ombh2 + omnuh2) / h^2.
  unif : logA = LOGA_CMB_SSEE (el que fija el CMB con este fondo)
  libre: logA = logA_kids_legacy +- 1 sigma, leidos de CANONICAL (su log es la
         cadena kids_legacy_ssee); la barra es la mitad del salto entre extremos.

CONTROL (R53): Omega_m de CAMB tiene que dar el 0.308881 del nucleo a 6
decimales; si no, CAMB no esta usando el fondo que se dice.

Salida: results/logs/s8_kids_legacy_camb.json
"""
import json
import math
import os
import sys

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "src"))
sys.path.insert(0, os.path.join(R, "src", "p06_growth"))
import yaml  # noqa: E402

import cobaya_kids_legacy as L  # noqa: E402
import kids_shear as K  # noqa: E402
import ssee_core as S  # noqa: E402

C = yaml.safe_load(open(os.path.join(R, "CANONICAL_VALUES.yaml")))["canonical"]
TXT = open(os.path.join(R, "CANONICAL_VALUES.yaml")).read()
bg = L.SSEE_BG
LOGT = 7.8   # ORIGEN-VALOR: 7.8 — logT_AGN de relleno: sigma8 es LINEAL y no depende de el


def s8(logA):
    r = K.run_camb(omch2=bg["omch2"], ombh2=bg["ombh2"], h0=bg["h0"], ns=bg["ns"],
                   As=math.exp(logA) * 1e-10, mnu=bg["mnu"], w=bg["w0"], wa=bg["wa"], logT_AGN=LOGT)[0]
    p = r.Params
    om = (p.omch2 + p.ombh2 + p.omnuh2) / (p.H0 / 100.0) ** 2
    sg = float(r.get_sigma8_0())
    return sg, sg * math.sqrt(om / 0.3), om


la = C["logA_kids_legacy"]
import re  # noqa: E402
sla = float(re.search(r"logA_kids_legacy:\s*[0-9.]+\s*#\s*±([0-9.]+)", TXT).group(1))
sg_u, S8_u, om = s8(L.LOGA_CMB_SSEE)
sg_c, S8_c, _ = s8(la)
sg_hi, S8_hi, _ = s8(la + sla)
sg_lo, S8_lo, _ = s8(la - sla)
out = dict(fecha=str(__import__("datetime").date.today()), fondo="SSEE_BG (cobaya_kids_legacy)",
           Omega_m_camb=om, control_Omega_m=dict(nucleo=S.OMEGA_M_TOTAL, pasa=bool(round(om, 6) == round(S.OMEGA_M_TOTAL, 6))),
           unif=dict(logA=L.LOGA_CMB_SSEE, sigma8=sg_u, S8=S8_u),
           libre=dict(logA=la, logA_sigma=sla, sigma8=sg_c, sigma8_sigma=(sg_hi - sg_lo) / 2,
                      S8=S8_c, S8_sigma=(S8_hi - S8_lo) / 2))
json.dump(out, open(os.path.join(R, "results/logs/s8_kids_legacy_camb.json"), "w"), indent=1)
print(f"  Omega_m CAMB {om:.6f} (nucleo {S.OMEGA_M_TOTAL:.6f}) control {out['control_Omega_m']['pasa']}")
print(f"  unif : sigma8 {sg_u:.4f}  S8 {S8_u:.4f}")
print(f"  libre: sigma8 {sg_c:.4f} ± {out['libre']['sigma8_sigma']:.4f}  S8 {S8_c:.4f} ± {out['libre']['S8_sigma']:.4f}")
