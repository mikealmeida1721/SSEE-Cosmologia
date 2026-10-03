#!/usr/bin/env python3
"""h0_por_metodos.py — OP-8b: ¿el apantallamiento lo ve todo método local, o solo el calibrado con Cefeidas? (2026-10-03)

POR QUE. La prueba por profundidad (h0_por_profundidad.json) mostró H0 plano de z=0.023 a 0.15.
Eso es compatible con la lectura de Mike (el apantallamiento es una propiedad de plano o de nivel,
no de volumen), pero también con «vive en la calibración Cefeida». Esta prueba separa esas dos.
Pre-registro: OPEN_PROBLEMS OP-8b, commit ade15d8, antes de correr.

HIPOTESIS
  P (plano universal): todo método local da  H_glob,DESI / (1 - f_screen)
  C (calibración Cefeida): los métodos sin Cefeidas dan H_glob,DESI (sin apantallamiento)
  Control del otro lado, LCDM sin apantallamiento: todo método local da el H0 de Planck 2018.
H_glob,DESI sale de DESI DR2 sola con prior plano (h0_four_priors.json, «plano»), NO de SH0ES, que
es la entrada de la cascada: así la predicción no es circular. f_screen sale del álgebra (ssee_core).
El error de la predicción es común a todos los métodos y entra como covarianza totalmente correlacionada.

DATOS. Cada valor titular se LEE del LaTeX del artículo (arXiv, en /mnt/datos/SSEE_data/literatura),
con un patrón que exige el texto que lo rodea. Errores asimétricos: normal partida (se usa el lado
hacia la predicción). Errores separados (estadístico, sistemático, SN): en cuadratura.

CRITERIOS (sobre el PRIMARIO: máseres, lentes TDCOSMO-2025, sirena GW170817)
  APOYA P frente a C : Δχ²(C−P) ≥ 9 y χ²_P con p > 0.05
  APOYA C frente a P : Δχ²(P−C) ≥ 9 y χ²_C con p > 0.05
  NO CONCLUYE        : lo demás
CONTROLES (R53)
  - Lectura: cada valor se vuelve a buscar en su .tex, y con un dígito alterado NO tiene que aparecer.
  - Potencia: 2000 simulaciones del PRIMARIO con sus errores reales, bajo P y bajo C. Si el criterio
    no recupera la hipótesis verdadera en ≥ 80 % de los casos, la prueba no tiene potencia: se reporta
    eso y la precisión combinada necesaria, no un veredicto.

Salida: results/logs/h0_por_metodos.json
"""
import json
import os
import re
import sys

import numpy as np
from scipy.stats import chi2 as CHI2

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from ssee_core import F_SCREEN  # noqa: E402
from procedencia import con_acta  # noqa: E402

LIT = "/mnt/datos/SSEE_data/literatura"
H4P = os.path.join(_R, "results", "logs", "h0_four_priors.json")
OUT = os.path.join(_R, "results", "logs", "h0_por_metodos.json")
rng = np.random.default_rng(20261003)

# (clave, nombre, grupo, archivo, patrón, cómo armar (valor, err+, err-) desde los grupos)
PAT_PM = r"([0-9]+\.[0-9]+)"
FUENTES = [
    ("maseres", "Máseres MCP (Pesce+2020)", "primario", "h0_metodos/2001.09213/main.tex",
     r"constrain the Hubble constant to be \$H_0 = " + PAT_PM + r" \\pm " + PAT_PM + r"\$", lambda g: (g[0], g[1], g[1])),
    ("lentes", "Lentes TDCOSMO-2025", "primario", "h0_metodos/2506.03023/main.tex",
     r"\\newcommand\{\\hnotflcdmonea\}\{" + PAT_PM + r"\^\{\+" + PAT_PM + r"\}_\{-" + PAT_PM + r"\}\}",
     lambda g: (g[0], g[1], g[2])),
    ("sirena", "Sirena GW170817", "primario", "h0_metodos/1710.05835/main.tex",
     r"\\newcommand\{\\HnaughtMAPMax\}\{" + PAT_PM + r"\}.*?\\newcommand\{\\HnaughtMAPOneSigmaUpperDiff\}\{" + PAT_PM
     + r"\}\s*\\newcommand\{\\HnaughtMAPOneSigmaLowerDiff\}\{" + PAT_PM + r"\}", lambda g: (g[0], g[1], g[2])),
    ("trgb_cchp", "TRGB, equipo CCHP (HST+JWST)", "secundario", "h0_metodos/2408.06153/Ho2024.tex",
     r"\\ho = " + PAT_PM + r" \$\\pm\$ " + PAT_PM + r" \(stat\) \$\\pm\$ " + PAT_PM + r" \(sys\) \$\\pm\$ " + PAT_PM
     + r" \(\$\\sigma_\{SN\}\)\$\), based on the TRGB method alone",
     lambda g: (g[0], np.sqrt(g[1] ** 2 + g[2] ** 2 + g[3] ** 2), np.sqrt(g[1] ** 2 + g[2] ** 2 + g[3] ** 2))),
    ("trgb_shoes", "TRGB, equipo SH0ES (JWST)", "secundario", "h0_metodos/2408.11770/main.tex",
     r"Cepheids, JAGB, and TRGB, we find \$" + PAT_PM + r"\\pm" + PAT_PM + r"\$, \$" + PAT_PM + r"\\pm" + PAT_PM
     + r"\$, and \$" + PAT_PM + r"\\pm" + PAT_PM + r"\$", lambda g: (g[4], g[5], g[5])),
    ("jagb_shoes", "JAGB, equipo SH0ES (JWST)", "secundario", "h0_metodos/2408.11770/main.tex",
     r"Cepheids, JAGB, and TRGB, we find \$" + PAT_PM + r"\\pm" + PAT_PM + r"\$, \$" + PAT_PM + r"\\pm" + PAT_PM
     + r"\$, and \$" + PAT_PM + r"\\pm" + PAT_PM + r"\$", lambda g: (g[2], g[3], g[3])),
    ("jagb_cchp", "JAGB, equipo CCHP (JWST)", "referencia", "h0_metodos/2408.06153/Ho2024.tex",
     r"\\ho = " + PAT_PM + r" \$\\pm\$ " + PAT_PM + r" \(stat\) \$\\pm\$ " + PAT_PM + r" \(sys\) \\hounits for the JAGB method",
     lambda g: (g[0], np.hypot(g[1], g[2]), np.hypot(g[1], g[2]))),
    ("cefeidas_hst", "Cefeidas SH0ES (HST) — entrada de la cascada", "referencia", "h0_metodos/2112.04510/shoes6.tex",
     r"\\newcommand\{\\hsbase\}\{\$ " + PAT_PM + r" \\pm " + PAT_PM + r" \$", lambda g: (g[0], g[1], g[1])),
    ("cefeidas_jwst", "Cefeidas SH0ES (JWST)", "referencia", "h0_metodos/2408.11770/main.tex",
     r"Cepheids, JAGB, and TRGB, we find \$" + PAT_PM + r"\\pm" + PAT_PM + r"\$", lambda g: (g[0], g[1], g[1])),
    ("sbf", "SBF (calibración Cefeida+TRGB)", "referencia", "h0_metodos/2101.02221/main.tex",
     r"H_0=" + PAT_PM + r"\{\\,\\pm\\,\}" + PAT_PM + r"\{\\,\\pm\\,\}" + PAT_PM + r"\$",
     lambda g: (g[0], np.hypot(g[1], g[2]), np.hypot(g[1], g[2]))),
]
PLANCK = ("1807.06209/ms.tex",
          r"\\twoonesig\[2\.8cm\]\{H_0 &= \(" + PAT_PM + r" \\pm " + PAT_PM + r"\) \\, \\Hunit,\}")
USA_CEFEIDAS = {"cefeidas_hst", "cefeidas_jwst", "sbf"}


def lee(archivo, patron):
    t = open(os.path.join(LIT, archivo), errors="ignore").read()
    m = re.search(patron, t, re.S)
    assert m, f"no encuentro el valor en {archivo}"
    return [float(x) for x in m.groups()], m.group(0), t


# --- lectura + control de lectura -------------------------------------------------
med, lectura = {}, {}
for clave, nombre, grupo, arch, pat, arma in FUENTES:
    g, txt, t = lee(arch, pat)
    v, ep, em = arma(g)
    i = next(k for k, ch in enumerate(txt) if ch.isdigit())
    alterado = txt[:i] + str((int(txt[i]) + 1) % 10) + txt[i + 1:]
    ok = (txt in t) and (alterado not in t)
    assert ok, f"control de lectura falla en {arch}"
    med[clave] = dict(nombre=nombre, grupo=grupo, H0=float(v), err_mas=float(ep), err_menos=float(em),
                      usa_cefeidas=clave in USA_CEFEIDAS, fuente=f"arXiv:{arch.split('/')[1]}", texto=txt[:160])
    lectura[clave] = ok
gp, txtp, tp = lee(*PLANCK)
H_PL, S_PL = gp
lectura["planck"] = (txtp in tp)

d4 = json.load(open(H4P))["plano"]
H_D, S_D = d4["H0_mediana"], d4["H0_std"]
mu_P, s_P = H_D / (1 - F_SCREEN), S_D / (1 - F_SCREEN)
mu_C, s_C = H_D, S_D


def pred(hip, clave):
    if hip == "P":
        return mu_P, s_P
    if hip == "C":
        return (mu_P, s_P) if med[clave]["usa_cefeidas"] else (mu_C, s_C)
    return H_PL, S_PL          # LCDM sin apantallamiento


def chi2_conj(claves, hip, xs=None):
    x = np.array([med[k]["H0"] for k in claves]) if xs is None else xs
    mus = np.array([pred(hip, k)[0] for k in claves])
    sp = pred(hip, claves[0])[1]
    r = x - mus
    s = np.array([med[k]["err_menos"] if ri > 0 else med[k]["err_mas"] for k, ri in zip(claves, r)])
    Cov = np.diag(s ** 2) + sp ** 2 * np.ones((len(x), len(x)))
    return float(r @ np.linalg.solve(Cov, r))


def veredicto(cP, cC, n):
    if cC - cP >= 9 and CHI2.sf(cP, n) > 0.05:
        return "APOYA P"
    if cP - cC >= 9 and CHI2.sf(cC, n) > 0.05:
        return "APOYA C"
    return "NO CONCLUYE"


PRIM = [k for k, *_ in FUENTES if med[k]["grupo"] == "primario"]


def simula(hip, escala=1.0, n=2000):
    mu, sp = (mu_P, s_P) if hip == "P" else (mu_C, s_C)
    aciertos = 0
    for _ in range(n):
        verdad = mu + sp * rng.standard_normal()
        xs = []
        for k in PRIM:
            z = rng.standard_normal()
            s = med[k]["err_mas"] if z > 0 else med[k]["err_menos"]
            xs.append(verdad + escala * s * z)
        xs = np.array(xs)
        guard = {k: (med[k]["err_mas"], med[k]["err_menos"]) for k in PRIM}
        for k in PRIM:
            med[k]["err_mas"] *= escala
            med[k]["err_menos"] *= escala
        v = veredicto(chi2_conj(PRIM, "P", xs), chi2_conj(PRIM, "C", xs), len(PRIM))
        for k in PRIM:
            med[k]["err_mas"], med[k]["err_menos"] = guard[k]
        aciertos += v == ("APOYA " + hip)
    return aciertos / n


pot = {"P": simula("P"), "C": simula("C")}
tiene_potencia = min(pot.values()) >= 0.8
# precisión necesaria: escala de los errores del PRIMARIO con la que ambas potencias llegan a 80 %
lo, hi = 0.05, 1.0
for _ in range(14):
    mid = 0.5 * (lo + hi)
    if min(simula("P", mid, 600), simula("C", mid, 600)) >= 0.8:
        lo = mid
    else:
        hi = mid
escala_nec = lo
s_comb_hoy = float(np.sum([1 / (0.5 * (med[k]["err_mas"] + med[k]["err_menos"])) ** 2 for k in PRIM]) ** -0.5)

res_prim = {h: chi2_conj(PRIM, h) for h in ("P", "C", "LCDM")}
v_prim = veredicto(res_prim["P"], res_prim["C"], len(PRIM))


def tirones(k):
    out = {}
    for h in ("P", "C", "LCDM"):
        mu, sp = pred(h, k)
        r = med[k]["H0"] - mu
        s = med[k]["err_menos"] if r > 0 else med[k]["err_mas"]
        out[h] = dict(pred=mu, pred_s=sp, sigma=r / np.hypot(s, sp))
    return out


for k in med:
    med[k]["tirones"] = tirones(k)

print(f"H_glob,DESI = {H_D:.2f} ± {S_D:.2f};  f = {F_SCREEN:.6f};  P predice {mu_P:.2f} ± {s_P:.2f};  "
      f"C predice {mu_C:.2f} ± {s_C:.2f} (sin Cefeidas);  LCDM {H_PL} ± {S_PL}")
for k, m in med.items():
    t = m["tirones"]
    print(f"  {m['grupo']:10s} {m['nombre']:46s} {m['H0']:6.2f} +{m['err_mas']:.2f}/-{m['err_menos']:.2f}   "
          f"P {t['P']['sigma']:+5.2f}σ   C {t['C']['sigma']:+5.2f}σ   LCDM {t['LCDM']['sigma']:+5.2f}σ")
print(f"PRIMARIO χ²: P {res_prim['P']:.2f}  C {res_prim['C']:.2f}  LCDM {res_prim['LCDM']:.2f}  (n={len(PRIM)})")
print(f"potencia: recupera P {pot['P']:.0%}, recupera C {pot['C']:.0%} -> "
      f"{'TIENE potencia' if tiene_potencia else 'SIN POTENCIA'};  σ combinado hoy {s_comb_hoy:.2f}, "
      f"haría falta ×{escala_nec:.2f} ≈ {s_comb_hoy*escala_nec:.2f}")
print("veredicto:", v_prim if tiene_potencia else f"no se lee (sin potencia); el criterio diría {v_prim}")

res = dict(fecha="2026-10-03", preregistro_commit="ade15d8", f_screen=F_SCREEN,
           H_glob_desi=H_D, H_glob_desi_s=S_D, pred_P=mu_P, pred_P_s=s_P, pred_C=mu_C, pred_C_s=s_C,
           H0_planck=H_PL, H0_planck_s=S_PL, medidas=med, control_lectura=lectura,
           primario=PRIM, chi2_primario=res_prim, n_primario=len(PRIM),
           potencia=pot, tiene_potencia=tiene_potencia, escala_errores_necesaria=escala_nec,
           sigma_combinado_hoy=s_comb_hoy, sigma_combinado_necesario=s_comb_hoy * escala_nec,
           veredicto_criterio=v_prim, veredicto=v_prim if tiene_potencia else "SIN POTENCIA")
json.dump(con_acta(res, __file__, entradas=[H4P] + sorted({os.path.join(LIT, f[3]) for f in FUENTES}) + [os.path.join(LIT, PLANCK[0])]),
          open(OUT, "w"), indent=1, ensure_ascii=False, default=float)
print("->", OUT)
