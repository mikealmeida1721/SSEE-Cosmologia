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

CONTROL (R53): Omega_m de CAMB frente al 0.308881 del nucleo. CAMB convierte
m_nu -> omega_nu con su propia aproximacion: m_nu/94.064 * (N_eff/3)^(3/4), o
sea /93.04 con N_eff=3.044 (sube la TEMPERATURA del neutrino con N_eff). El
nucleo usa /93.14 (Mangano+2005, desacople no instantaneo calculado entero, el
del PDG). Por eso el control (2026-10-01) pide dos cosas:
  (a) TODA la diferencia de Omega_m sale del neutrino: om - nucleo =
      (omnuh2_CAMB - omega_nu_nucleo)/h^2 a 1e-9 (omch2 y ombh2 son los del nucleo);
  (b) el impacto: se repite con la masa que hace omnuh2_CAMB = omega_nu del
      nucleo, y se reporta Delta sigma8 y Delta S8 frente a la barra.

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
from procedencia import con_acta  # noqa: E402

C = yaml.safe_load(open(os.path.join(R, "CANONICAL_VALUES.yaml")))["canonical"]
TXT = open(os.path.join(R, "CANONICAL_VALUES.yaml")).read()
bg = L.SSEE_BG
LOGT = 7.8   # ORIGEN-VALOR: 7.8 — logT_AGN de relleno: sigma8 es LINEAL y no depende de el


def s8(logA, mnu=bg["mnu"], params=False):
    r = K.run_camb(omch2=bg["omch2"], ombh2=bg["ombh2"], h0=bg["h0"], ns=bg["ns"],
                   As=math.exp(logA) * 1e-10, mnu=mnu, w=bg["w0"], wa=bg["wa"], logT_AGN=LOGT)[0]
    p = r.Params
    om = (p.omch2 + p.ombh2 + p.omnuh2) / (p.H0 / 100.0) ** 2
    sg = float(r.get_sigma8_0())
    return (sg, sg * math.sqrt(om / 0.3), om) + ((p,) if params else ())


la = C["logA_kids_legacy"]
import re  # noqa: E402
sla = float(re.search(r"logA_kids_legacy:\s*[0-9.]+\s*#\s*±([0-9.]+)", TXT).group(1))
sg_u, S8_u, om, P = s8(L.LOGA_CMB_SSEE, params=True)
h2 = (P.H0 / 100.0) ** 2
gap_nu = (P.omnuh2 - S.OMEGA_NU_H2) / h2
fac_camb = bg["mnu"] / P.omnuh2                      # eV: la constante que CAMB uso de hecho
mnu_eq = S.OMEGA_NU_H2 * fac_camb                   # la masa con la que CAMB da el omega_nu del nucleo
sg_e, S8_e, om_e = s8(L.LOGA_CMB_SSEE, mnu=mnu_eq)
sg_c, S8_c, _ = s8(la)
sg_hi, S8_hi, _ = s8(la + sla)
sg_lo, S8_lo, _ = s8(la - sla)
out = dict(fecha=str(__import__("datetime").date.today()), fondo="SSEE_BG (cobaya_kids_legacy)",
           Omega_m_camb=om, control_Omega_m=dict(
               nucleo=S.OMEGA_M_TOTAL, diferencia=om - S.OMEGA_M_TOTAL, de_neutrino=gap_nu,
               C_nu_camb=fac_camb, C_nu_nucleo=bg["mnu"] / S.OMEGA_NU_H2,
               pasa=bool(abs(om - S.OMEGA_M_TOTAL - gap_nu) < 1e-9),
               impacto=dict(mnu_equivalente=mnu_eq, Omega_m=om_e, d_sigma8=sg_u - sg_e, d_S8=S8_u - S8_e)),
           unif=dict(logA=L.LOGA_CMB_SSEE, sigma8=sg_u, S8=S8_u),
           libre=dict(logA=la, logA_sigma=sla, sigma8=sg_c, sigma8_sigma=(sg_hi - sg_lo) / 2,
                      S8=S8_c, S8_sigma=(S8_hi - S8_lo) / 2))
json.dump(con_acta(out, __file__, entradas=[os.path.join(R, "CANONICAL_VALUES.yaml"), L.__file__, K.__file__]),
          open(os.path.join(R, "results/logs/s8_kids_legacy_camb.json"), "w"), indent=1)
cm = out["control_Omega_m"]
print(f"  Omega_m CAMB {om:.7f} nucleo {S.OMEGA_M_TOTAL:.7f}  diferencia {cm['diferencia']:+.2e}, del neutrino {gap_nu:+.2e}")
print(f"  C_nu: CAMB {cm['C_nu_camb']:.3f} eV, nucleo {cm['C_nu_nucleo']:.3f} eV  -> control {'PASA' if cm['pasa'] else 'NO PASA'}")
print(f"  impacto (omega_nu del nucleo, Omega_m {om_e:.7f}): d_sigma8 {sg_u - sg_e:+.2e}  d_S8 {S8_u - S8_e:+.2e}")
print(f"  unif : sigma8 {sg_u:.4f}  S8 {S8_u:.4f}")
print(f"  libre: sigma8 {sg_c:.4f} ± {out['libre']['sigma8_sigma']:.4f}  S8 {S8_c:.4f} ± {out['libre']['S8_sigma']:.4f}")
