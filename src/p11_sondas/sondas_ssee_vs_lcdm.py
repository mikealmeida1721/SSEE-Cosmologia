#!/usr/bin/env python3
"""sondas_ssee_vs_lcdm.py — SSEE contra LCDM en las sondas nuevas, leido de sus logs.

POR QUE (2026-10-01). Cada sonda nueva (supernovas, lente del CMB, BAO, DES Y3)
guardo en su log el chi2 de SSEE en el clavo y el de LCDM con SUS parametros de
Planck 2018 (lcdm_planck.py, arreglo 2026-09-27), pero ningun sitio los ponia lado
a lado con su sigma. Este lector no calcula fisica: lee los chi2 de los logs y
convierte cada uno a PTE y sigma equivalente con los MISMOS grados de libertad
para los dos modelos (los dos con cero libres cosmologicos).

Filas:
  SSEE        fondo algebraico + logA clavado del CMB de SSEE
  LCDM-Planck Planck 2018 VI Tabla 2 completo (m_nu 0.06, logA 3.044, tau 0.0544)
  Delta chi2  SSEE - LCDM (negativo = SSEE ajusta mejor)
Las tres compilaciones de supernovas comparten objetos: NO se suman entre si.
BAO: el log solo trae LCDM LIBRE (2 ajustados, 11 dof), no LCDM-Planck; se reporta
tal cual con su dof, sin mezclarlo con las filas clavadas.

CONTROL (R53): cada log ya trae su calibrador LCDM que reproduce lo publicado; aqui
se exige que ese calibrador diga reproduce=True donde exista, o el lector se para.

Salida: results/logs/sondas_ssee_vs_lcdm.json
"""
import json
import os
import sys

from scipy import stats

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)
LOGS = os.path.join(_R, "results", "logs")
ENT = {k: os.path.join(LOGS, v) for k, v in dict(
    sn="sn_geometria_en_el_clavo.json", u3="union3_en_el_clavo.json",
    act="act_dr6_en_el_clavo.json", spt="spt3g_kk_en_el_clavo.json",
    bao="bao_lcdm_libre.json", desS="des_y3_en_el_clavo_ssee.json",
    desL="des_y3_en_el_clavo_lcdm_planck.json").items()}
L = {k: json.load(open(v)) for k, v in ENT.items()}


def sig(chi2, dof):
    pte = float(stats.chi2.sf(chi2, dof))
    return dict(chi2=float(chi2), dof=int(dof), PTE=pte, sigma=float(stats.norm.isf(pte / 2)))


def fila(nombre, tipo, cs, cl, dof, ve_As=None, calibrador=None, nota=""):
    if calibrador is not None and not calibrador:
        sys.exit(f"  {nombre}: su calibrador LCDM NO reproduce lo publicado; me paro")
    return dict(sonda=nombre, tipo=tipo, SSEE=sig(cs, dof), LCDM_Planck=sig(cl, dof),
                dchi2=float(cs - cl), ve_As=ve_As, nota=nota)


filas = []
for n in ("Pantheon+", "DES-SN5YR"):
    s = L["sn"]["sondas"][n]
    filas.append(fila(n, "supernovas (forma de d_L)", s["chi2"], s["control_a_lcdm"]["chi2"], s["dof"],
                      ve_As=s["ve_As"], calibrador=s["calibrador_lcdm"]["reproduce"]))
for n in ("Union3", "Union3.1"):
    s = L["u3"]["sondas"][n]
    filas.append(fila(n, "supernovas (mu binned)", s["chi2"], s["control_lcdm_planck"]["chi2"], s["dof"],
                      calibrador=L["u3"]["calibrador_lcdm_union3"]["reproduce"]))
a = L["act"]
filas.append(fila("ACT DR6", "lente del CMB", a["chi2_en_el_clavo"], a["control_a_fondo_lcdm"]["chi2"], a["dof"],
                  ve_As=a["control_b_sensibilidad_As"]["ve_As"]))
s = L["spt"]
filas.append(fila("SPT-3G D1 KK", "lente del CMB", s["chi2_en_el_clavo"], s["control_a_fondo_lcdm"]["chi2"], s["dof"],
                  ve_As=s["control_b_sensibilidad_As"]["ve_As"],
                  nota=f"{s['nuisance_libres']} nuisance minimizados igual en los dos modelos"))
dS, dL = L["desS"], L["desL"]
assert dS["convergido"] and dL["convergido"]
des = dict(sonda="DES Y3 3x2pt", tipo="cizalla + agrupamiento", dchi2=float(dS["chi2_2pt"] - dL["chi2_2pt"]),
           SSEE=dict(chi2=dS["chi2_2pt"], S8=dS["S8"]), LCDM_Planck=dict(chi2=dL["chi2_2pt"], S8=dL["S8"]),
           nota="montaje ABIERTO (motor y TATT pendientes): solo Delta chi2, sin sigma")
b = L["bao"]
assert b["lcdm_libre"]["reproduce"]
bao = dict(sonda="DESI DR2 BAO", tipo="BAO", SSEE=sig(b["ssee_clavo"]["chi2"], b["ssee_clavo"]["dof"]),
           LCDM_libre=sig(b["lcdm_libre"]["chi2"], b["lcdm_libre"]["dof"]),
           dchi2=float(b["delta_chi2_ssee_menos_lcdm_libre"]),
           nota="LCDM LIBRE (Om y h r_d ajustados), no clavado: no es la misma comparacion que las demas")

for f in filas:
    print(f"  {f['sonda']:14s} SSEE {f['SSEE']['chi2']:9.3f}/{f['dof'] if 'dof' in f else f['SSEE']['dof']}"
          f" ({f['SSEE']['sigma']:.2f}s)   LCDM {f['LCDM_Planck']['chi2']:9.3f} ({f['LCDM_Planck']['sigma']:.2f}s)"
          f"   dchi2 {f['dchi2']:+.3f}")
print(f"  {des['sonda']:14s} dchi2 {des['dchi2']:+.3f}   ({des['nota']})")
print(f"  {bao['sonda']:14s} SSEE {bao['SSEE']['chi2']:.3f}/{bao['SSEE']['dof']} ({bao['SSEE']['sigma']:.2f}s)"
      f"   LCDM libre {bao['LCDM_libre']['chi2']:.3f}/{bao['LCDM_libre']['dof']} ({bao['LCDM_libre']['sigma']:.2f}s)")
discrimina = [f["sonda"] for f in filas if abs(f["dchi2"]) >= 9.0]   # ORIGEN-VALOR: 9.0 — Delta chi2 = 3^2, el umbral de 3 sigma de Mike para 1 grado
out = dict(filas_clavadas=filas, des_y3=des, bao=bao, umbral_discrimina_dchi2=9.0, discriminan=discrimina,
           nota_suma="las supernovas comparten objetos y las dos lentes del CMB el cielo: no se suman")
json.dump(con_acta(out, __file__, entradas=list(ENT.values())),
          open(os.path.join(LOGS, "sondas_ssee_vs_lcdm.json"), "w"), indent=1, ensure_ascii=False)
print(f"  discriminan (|dchi2| >= 9): {discrimina or 'ninguna'}")
