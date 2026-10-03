#!/usr/bin/env python3
"""tabla_sondas_tex.py — la tabla SSEE contra LCDM sonda por sonda, para el PRD y el Sealed (2026-10-03).

POR QUE. sondas_ssee_vs_lcdm.json ya pone lado a lado el chi2 de SSEE (fondo
algebraico, cero libres cosmologicos) y el de LCDM en cada sonda nueva, pero el
PRD sólo citaba el contraste de DESI en prosa y con números escritos a mano. Este
lector no calcula física: copia los chi2 del log a una tabla LaTeX, sin adjetivos,
en dos bloques que no se mezclan:
  A. fondo CLAVADO en los dos modelos (LCDM con Planck 2018, cero ajustados);
  B. LCDM AJUSTA parámetros que SSEE no tiene (columna «ajustados»).
DESI DR2 BAO aparece en los dos bloques: clavado (B: LCDM-Planck) y libre (Om y
h r_d ajustados a DESI), porque es la única sonda con |dchi2| sobre el umbral del
log y la frase honesta necesita las dos filas.

CONTROL (R53). Se relee cada número escrito desde la tabla y se compara con el
log; además la fila DESI clavada debe coincidir con bao_lcdm_libre.json (la fuente
del log de sondas), o el script se para.

Salida: manuscript/tabla_sondas_generada.tex (con el acta en la primera línea).
"""
import json
import os
import re
import sys

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import cabecera  # noqa: E402

LOG = os.path.join(_R, "results", "logs", "sondas_ssee_vs_lcdm.json")
BAO = os.path.join(_R, "results", "logs", "bao_lcdm_libre.json")
OUT = os.path.join(_R, "manuscript", "tabla_sondas_generada.tex")

d = json.load(open(LOG))
b = json.load(open(BAO))
NOMBRE = {"supernovas (forma de d_L)": "SN", "supernovas (mu binned)": "SN",
          "lente del CMB": "CMB lensing", "BAO": "BAO", "cizalla + agrupamiento": "3$\\times$2pt",
          "CMB": "CMB", "cizalla": "shear",
          "BAO (CAMB, r_d de cada modelo)": "BAO"}

SONDA = {"Planck plik_lite": r"Planck plik\_lite", "Planck plik completo": "Planck plik (full)",
         "DES Y3 3x2pt": "DES Y3"}


def nom(s):
    return SONDA.get(s, s)


def f(x, n=2):
    return f"${x:.{n}f}$"   # entre $ para que el signo menos sea un menos, no un guion


filas, escritos = [], []
filas.append(r"\multicolumn{7}{l}{\emph{A. Background fixed in both models}} \\")
filas.append(r"\midrule")
clav = list(d["filas_clavadas"])
clav.insert(len(clav) - 1, dict(d["des_y3"], SSEE=dict(d["des_y3"]["SSEE"], dof=None),
                                LCDM_Planck=d["des_y3"]["LCDM_Planck"]))
for r in clav:
    s, l = r["SSEE"], r["LCDM_Planck"]
    N = "--" if s.get("dof") is None else str(s["dof"])
    marca = r"$^{a}$" if r["nota"].startswith("7 nuisance") else (r"$^{b}$" if r["sonda"] == "DES Y3 3x2pt" else "")
    filas.append(f"{nom(r['sonda'])}{marca} & {NOMBRE[r['tipo']]} & {N} & 0 / 0 & {f(s['chi2'])} & {f(l['chi2'])} & {f(r['dchi2'])} \\\\")
    escritos += [(s["chi2"], 2), (l["chi2"], 2), (r["dchi2"], 2)]
filas.append(r"\midrule")
filas.append(r"\multicolumn{7}{l}{\emph{B. $\Lambda$CDM fits parameters that SSEE does not have}} \\")
filas.append(r"\midrule")
bl = d["bao"]
filas.append(f"DESI DR2 BAO & BAO & 13 / 11 & 0 / 2 & {f(bl['SSEE']['chi2'])} & {f(bl['LCDM_libre']['chi2'])} & {f(bl['dchi2'])} \\\\")
escritos += [(bl["SSEE"]["chi2"], 2), (bl["LCDM_libre"]["chi2"], 2), (bl["dchi2"], 2)]
for r in d["filas_lcdm_ajusta"]:
    filas.append(f"{nom(r['sonda'])} & {NOMBRE[r['tipo']]} & -- & {r['ajustados_ssee']} / {r['ajustados_lcdm']} & "
                 f"{f(r['SSEE']['chi2'])} & {f(r['LCDM']['chi2'])} & {f(r['dchi2'])} \\\\")
    escritos += [(r["SSEE"]["chi2"], 2), (r["LCDM"]["chi2"], 2), (r["dchi2"], 2)]
filas.append(r"\bottomrule")

# --- control R53 -------------------------------------------------------------
desi = [r for r in d["filas_clavadas"] if r["sonda"] == "DESI DR2 BAO"][0]
assert abs(desi["SSEE"]["chi2"] - b["ssee_camb"]["chi2"]) < 1e-9, "DESI SSEE no coincide con bao_lcdm_libre"
assert abs(desi["LCDM_Planck"]["chi2"] - b["lcdm_planck_camb"]["chi2"]) < 1e-9, "DESI LCDM-Planck no coincide"
assert abs(bl["LCDM_libre"]["chi2"] - b["lcdm_libre"]["chi2"]) < 1e-9, "DESI LCDM libre no coincide"
cuerpo = "\n".join(filas)
leidos = [float(x) for x in re.findall(r"(?<![\w.])-?\d+\.\d{2}(?!\d)", cuerpo)]
assert len(leidos) == len(escritos), (len(leidos), len(escritos))
for x, (v, n) in zip(leidos, escritos):
    assert abs(x - v) <= 0.5 * 10 ** -n + 1e-12, (x, v)
# del otro lado: un dígito cambiado tiene que NO pasar
assert not abs(leidos[0] + 0.01 - escritos[0][0]) <= 0.5 * 10 ** -2 + 1e-12

with open(OUT, "w") as t:
    t.write(cabecera(__file__, entradas=[LOG, BAO], comentario="%") + "\n")
    t.write(cuerpo + "\n")
print(f"{OUT}: {len(clav)} filas clavadas + {1 + len(d['filas_lcdm_ajusta'])} con LCDM ajustando; "
      f"control: {len(leidos)} números releídos = log; dígito alterado rechazado")
