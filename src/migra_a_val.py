#!/usr/bin/env python3
"""migra_a_val.py — pasa a \\val{} los numeros ALGEBRAICOS escritos a mano en los .tex.

POR QUE (2026-09-30). Regla de Mike: ningun numero sin fuente. Los papers
escriben a mano constantes del nucleo (K_V) y algebra derivada (2 phi^7).
Su fuente es results/logs/algebra_derivada.json (con
acta); este script cambia cada aparicion por \\val{nombre_dN}, la macro que
valores_tex.py genera desde ese log, y anota en manuscript/valores.yaml las
entradas que hagan falta.

REGLAS (conservadoras: si duda, NO toca y lo lista):
  - solo la parte de codigo de cada linea (nunca comentarios), y nunca dentro
    de \\label, \\ref, \\eqref, \\cite*, \\href, \\url;
  - el numero escrito tiene que ser EXACTAMENTE el redondeo del valor a sus
    decimales, con >= 5 cifras significativas (menos es casarse por casualidad);
  - si el valor es negativo, el signo tiene que estar escrito delante;
  - CORRIGE: errores conocidos de la ultima cifra, nombrados uno a uno (ver
    algebra_derivada.py): se cambian por la macro, que imprime el valor bueno.
  - nombres retirados o alias deprecados del nucleo no se usan.
Uso: migra_a_val.py [--escribe] archivo.tex ...   (sin --escribe solo informa)
"""
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = "results/logs/algebra_derivada.json"
VAL = ROOT / "manuscript" / "valores.yaml"
NO_USAR = {"OMEGA_CDM_SECTOR", "OMEGA_M_DYN", "OMEGA_M_CMB_MIRA", "OMEGA_M_CMB_PIPHI",
           "OMEGA_M_CMB_GEOMETRIC", "H0_MIRA", "LCDM_H0", "LCDM_NS", "LCDM_OMEGA_M",
           "LCDM_SIGMA8", "OMEGA_DE", "u_condensado_TM", "n_ssee_TM", "inv_S_M",
           "OMEGA_M_CMB", "cs2_condensado_TM", "sK_con_KX_de_P7_c1"}   # alias de OMEGA_M_TOTAL (ssee_core L165): se usa el canonico
# errores de la ultima cifra hallados al armar algebra_derivada (2026-09-30)
# Cada uno es el valor MAL escrito que se encontro (no un resultado):
CORRIGE = {("sqrt_AURA", "1.99947"),      # ORIGEN-VALOR: 1.99947 — mal escrito en Paper 8 (el algebra da 1.999462)
           ("pi_mas_KAL", "8.663001"),    # ORIGEN-VALOR: 8.663001 — mal escrito en la tabla de Paper 4
           ("phi_pi_KAL", "10.281034"),   # ORIGEN-VALOR: 10.281034 — mal escrito en la tabla de Paper 4
           ("alpha_K_z0", "15.591335"),   # ORIGEN-VALOR: 15.591335 — alpha_K calculado con H0_ALG (22 sitios)
           ("tres_MIRA", "5.9967"),       # ORIGEN-VALOR: 5.9967 — truncado en Paper 9 (el algebra redondea a 5.9968)
           ("sqrtAURA_MIRA", "1.00030")}  # ORIGEN-VALOR: 1.00030 — mal escrito en Paper 8 (el algebra da 1.000269)
NUM = re.compile(r"(?<![\w.])(-?)(\d+\.\d+)(?![\w.])")
PROHIBIDO = re.compile(r"\\(?:label|ref|eqref|cite\w*|href|url)\{[^}]*$")


def fuentes():
    d = json.load(open(ROOT / LOG))
    out = {}
    for k, v in d["nucleo"].items():
        if k not in NO_USAR:
            out[k] = ("nucleo", v)
    for k, v in d["algebra"].items():
        if k not in NO_USAR:
            out[k] = ("algebra", v["valor"])
    return out


def cifras(s):
    return len(s.replace(".", "").lstrip("0"))


_ALG = re.compile(r"\(\\varphi\s*\+\s*\\pi\)\^2|\(\\phi\s*\+\s*\\pi\)\^2|rm\s*alg|\{alg|pure number|target|blanco", re.I)
_GLOB = re.compile(r"glob", re.I)


def desempata(nombres, frase, signo):
    """Reglas de desempate cuando un valor casa con dos nombres (2026-09-30):
    identidades del nucleo o la propia frase. Sin regla clara: None."""
    n = set(nombres)
    if n == {"S_DE", "W0"}:                 # S_DE = -W0 por definicion
        return "W0" if signo else "S_DE"
    if n == {"IGNIS", "K_V"}:               # mismo valor, ENTIDADES distintas
        return "IGNIS" if "IGNIS" in frase else "K_V"
    if n == {"H0_ALG", "H0_GLOBAL"}:        # el blanco puro vs el H del modelo
        a, g = bool(_ALG.search(frase)), bool(_GLOB.search(frase))
        return "H0_ALG" if a and not g else "H0_GLOBAL" if g and not a else None
    return None


def candidato(signo, s, F, frase=""):
    """Un solo nombre o ninguno. Si el valor casa con DOS entidades distintas
    (el H redondeado a 3 decimales es H0_ALG y H0_GLOBAL), no se elige: se
    lista para decidir a mano."""
    d = len(s.split(".")[1])
    hits = []
    for k, (sec, v) in F.items():
        if f"{abs(v):.{d}f}" == s or (k, s) in CORRIGE:   # CORRIGE es una lista EXPLICITA, revisada a mano
            hits.append((k, sec, d, v))
    if not hits:
        return None, None
    if len(hits) > 1:
        k = desempata([h[0] for h in hits], frase, signo)
        if k is None:
            return None, "ambiguo: " + ", ".join(h[0] for h in hits)
        hits = [h for h in hits if h[0] == k]
    k, sec, d, v = hits[0]
    if v < 0 and not signo:
        return None, f"valor negativo sin signo escrito ({k})"
    return hits[0], None


def migra(path, F, escribe):
    lineas = path.read_text().split("\n")
    usados, dudas, cambios = set(), [], 0
    for i, ln in enumerate(lineas):
        m = re.search(r"(?<!\\)%", ln)
        cod, com = (ln[:m.start()], ln[m.start():]) if m else (ln, "")
        nuevo, pos = [], 0
        for n in NUM.finditer(cod):
            signo, s = n.group(1), n.group(2)
            if cifras(s) < 5 or PROHIBIDO.search(cod[:n.start()]):
                continue
            c, duda = candidato(signo, s, F, cod)
            if duda:
                dudas.append(f"L{i+1} {signo}{s}: {duda}")
            if not c:
                continue
            k, sec, d, v = c
            ini = n.start() if (v < 0 and signo) else n.start(2)
            nom = f"{k}_d{d}"
            nuevo.append(cod[pos:ini] + "\\val{" + nom + "}")
            pos = n.end()
            usados.add((nom, sec, k, d))
            cambios += 1
            if (k, s) in CORRIGE:
                dudas.append(f"L{i+1} CORRIGE {s} -> {abs(v):.{d}f} ({k})")
        if nuevo:
            lineas[i] = "".join(nuevo) + cod[pos:] + com
    if escribe and cambios:
        path.write_text("\n".join(lineas))
    return cambios, usados, dudas


def anota(usados):
    defs = yaml.safe_load(VAL.read_text()) or {}
    nuevas = []
    for nom, sec, k, d in sorted(usados):
        if nom in defs:
            continue
        ruta = f"{LOG}#{sec}.{k}" + (".valor" if sec == "algebra" else "")
        nuevas.append(f'{nom}: {{fuente: "{ruta}", formato: ".{d}f"}}')
    if nuevas:
        with open(VAL, "a") as f:
            f.write("# algebra y nucleo — src/migra_a_val.py (2026-09-30)\n" if "migra_a_val" not in VAL.read_text() else "")
            f.write("\n".join(nuevas) + "\n")
    return len(nuevas)


if __name__ == "__main__":
    escribe = "--escribe" in sys.argv
    F = fuentes()
    todos = set()
    for a in [x for x in sys.argv[1:] if x != "--escribe"]:
        c, u, dudas = migra(ROOT / a, F, escribe)
        todos |= u
        print(f"{a}: {c} numeros -> \\val{{}}")
        for x in dudas:
            print("   ", x)
    if escribe:
        print(f"  valores.yaml: {anota(todos)} entradas nuevas")
