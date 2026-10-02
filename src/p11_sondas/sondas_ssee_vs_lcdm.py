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

QUE LCDM HAY EN CADA FILA (2026-10-02, pedido de Mike: que no parezca que LCDM
empato en todo con el fondo de Planck clavado). Cada fila lleva `fondo_lcdm`:
  «Planck clavado»          supernovas, lentes del CMB, DES Y3: 0 ajustados
  «Planck + A_s libre»      KiDS-Legacy: 1 ajustado (SSEE: 0, A_s del CMB)
  «libre»                   CMB (6 ajustados) y DESI BAO (Om y h r_d)
DES Y3 entra con TATT y con NLA: el empate cuenta como robusto si los dos |dchi2|
quedan bajo el umbral; el signo, si cambia, no vota.

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
    desL="des_y3_en_el_clavo_lcdm_planck.json", desSn="des_y3_en_el_clavo_ssee_nla.json",
    desLn="des_y3_en_el_clavo_lcdm_planck_nla.json", lite="cmb_dbic_mnu_propia.json",
    full="b1_k2.json", kl="kids_legacy_bic.json").items()}
L = {k: json.load(open(v)) for k, v in ENT.items()}


def sig(chi2, dof):
    pte = float(stats.chi2.sf(chi2, dof))
    return dict(chi2=float(chi2), dof=int(dof), PTE=pte, sigma=float(stats.norm.isf(pte / 2)))


def fila(nombre, tipo, cs, cl, dof, ve_As=None, calibrador=None, nota=""):
    if calibrador is not None and not calibrador:
        sys.exit(f"  {nombre}: su calibrador LCDM NO reproduce lo publicado; me paro")
    return dict(sonda=nombre, tipo=tipo, fondo_lcdm="Planck clavado", ajustados_lcdm=0,
                SSEE=sig(cs, dof), LCDM_Planck=sig(cl, dof), dchi2=float(cs - cl), ve_As=ve_As, nota=nota)


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
dS, dL, dSn, dLn = L["desS"], L["desL"], L["desSn"], L["desLn"]
assert all(d["convergido"] for d in (dS, dL, dSn, dLn))
_dT, _dN = float(dS["chi2_2pt"] - dL["chi2_2pt"]), float(dSn["chi2_2pt"] - dLn["chi2_2pt"])
des = dict(sonda="DES Y3 3x2pt", tipo="cizalla + agrupamiento", fondo_lcdm="Planck clavado", ajustados_lcdm=0,
           dchi2=_dT, dchi2_TATT=_dT, dchi2_NLA=_dN,
           SSEE=dict(chi2=dS["chi2_2pt"], chi2_NLA=dSn["chi2_2pt"], S8=dS["S8"]),
           LCDM_Planck=dict(chi2=dL["chi2_2pt"], chi2_NLA=dLn["chi2_2pt"], S8=dL["S8"]),
           empate_robusto=bool(max(abs(_dT), abs(_dN)) < 9.0), signo_estable=bool((_dT > 0) == (_dN > 0)),
           nota="alineamientos TATT (oficial) y NLA: el empate se mantiene con los dos; el signo de una diferencia "
                "despreciable cambia, asi que no separa modelos. Solo Delta chi2, sin sigma (nuisances minimizados)")
b = L["bao"]
assert b["lcdm_libre"]["reproduce"]
bao = dict(sonda="DESI DR2 BAO", tipo="BAO", fondo_lcdm="libre", ajustados_lcdm=b["ssee_clavo"]["dof"] - b["lcdm_libre"]["dof"], SSEE=sig(b["ssee_clavo"]["chi2"], b["ssee_clavo"]["dof"]),
           LCDM_libre=sig(b["lcdm_libre"]["chi2"], b["lcdm_libre"]["dof"]),
           dchi2=float(b["delta_chi2_ssee_menos_lcdm_libre"]),
           nota="LCDM LIBRE (Om y h r_d ajustados), no clavado: no es la misma comparacion que las demas")

# Filas donde LCDM NO va con el fondo de Planck clavado: ajusta algo a la propia sonda
c_lite, c_full, kl = L["lite"], L["full"], L["kl"]["corridas"]
con_libres = [
    dict(sonda="Planck plik_lite", tipo="CMB", fondo_lcdm="libre", ajustados_lcdm=c_lite["k_lcdm"], ajustados_ssee=c_lite["k_ssee"],
         SSEE=dict(chi2=c_lite["chi2_ssee"]), LCDM=dict(chi2=c_lite["chi2_lcdm_mnu006"]), dchi2=c_lite["dchi2"], dBIC=c_lite["dBIC"]),
    dict(sonda="Planck plik completo", tipo="CMB", fondo_lcdm="libre", ajustados_lcdm=c_full["LCDM"]["k"], ajustados_ssee=c_full["SSEE"]["k"],
         SSEE=dict(chi2=c_full["SSEE"]["chi2_min"]), LCDM=dict(chi2=c_full["LCDM"]["chi2_min"]), dchi2=c_full["dchi2"], dBIC=c_full["dBIC"]),
    dict(sonda="KiDS-Legacy", tipo="cizalla", fondo_lcdm="Planck + A_s libre",
         ajustados_lcdm=kl["lcdmfijo"]["k"] - kl["sseefijo"]["k"], ajustados_ssee=0,
         SSEE=dict(chi2=kl["sseefijo"]["chi2_min"], BIC=kl["sseefijo"]["BIC"]), LCDM=dict(chi2=kl["lcdmfijo"]["chi2_min"], BIC=kl["lcdmfijo"]["BIC"]),
         dchi2=kl["sseefijo"]["chi2_min"] - kl["lcdmfijo"]["chi2_min"], dBIC=kl["sseefijo"]["BIC"] - kl["lcdmfijo"]["BIC"],
         nota="ajustados = los cosmologicos que LCDM ajusta de mas (A_s); los nuisance de KiDS son los mismos en los dos"),
]
for f in filas:
    print(f"  {f['sonda']:14s} SSEE {f['SSEE']['chi2']:9.3f}/{f['dof'] if 'dof' in f else f['SSEE']['dof']}"
          f" ({f['SSEE']['sigma']:.2f}s)   LCDM {f['LCDM_Planck']['chi2']:9.3f} ({f['LCDM_Planck']['sigma']:.2f}s)"
          f"   dchi2 {f['dchi2']:+.3f}")
print(f"  {des['sonda']:14s} dchi2 TATT {des['dchi2_TATT']:+.3f}  NLA {des['dchi2_NLA']:+.3f}  empate robusto {des['empate_robusto']}")
for f in con_libres:
    print(f"  {f['sonda']:20s} LCDM {f['fondo_lcdm']:18s} ({f['ajustados_lcdm']} ajustados)  dchi2 {f['dchi2']:+.3f}  dBIC {f['dBIC']:+.2f}")
print(f"  {bao['sonda']:14s} SSEE {bao['SSEE']['chi2']:.3f}/{bao['SSEE']['dof']} ({bao['SSEE']['sigma']:.2f}s)"
      f"   LCDM libre {bao['LCDM_libre']['chi2']:.3f}/{bao['LCDM_libre']['dof']} ({bao['LCDM_libre']['sigma']:.2f}s)")
discrimina = [f["sonda"] for f in filas if abs(f["dchi2"]) >= 9.0]   # ORIGEN-VALOR: 9.0 — Delta chi2 = 3^2, el umbral de 3 sigma de Mike para 1 grado
out = dict(filas_clavadas=filas, des_y3=des, bao=bao, filas_lcdm_ajusta=con_libres, umbral_discrimina_dchi2=9.0, discriminan=discrimina,
           nota_suma="las supernovas comparten objetos y las dos lentes del CMB el cielo: no se suman")
json.dump(con_acta(out, __file__, entradas=list(ENT.values())),
          open(os.path.join(LOGS, "sondas_ssee_vs_lcdm.json"), "w"), indent=1, ensure_ascii=False)
print(f"  discriminan (|dchi2| >= 9): {discrimina or 'ninguna'}")
