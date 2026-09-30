#!/usr/bin/env python3
"""R73 — de donde sale CADA numero-resultado de los papers (2026-09-30).

R65 exige origen a cada numero de los SCRIPTS. Nada lo exigia en los PAPERS:
un valor tecleado mal en un .tex, que nunca paso por CANONICAL_VALUES.yaml, no
lo veia ni memory_sync (solo conoce valores RETIRADOS) ni el guardian.

QUE SE MIDE. Numero-resultado = decimal pegado a una incertidumbre o a una
distancia en sigma: «a\\pm b», «x\\sigma», «a^{+b}». Solo los de
3 o mas cifras significativas: con menos, casar por valor contra ~3e4 numeros
de logs es azar, no rastreo (se cuentan aparte, como no verificables).

ORIGEN, igual que R65 (cualquiera basta):
  (a) el valor, a su redondeo, esta en un log (results/logs), un dato crudo
      (data/raw), CANONICAL_VALUES.yaml o src/ssee_core.py;
  (b) la frase o la fila de tabla lleva \\cite (valor de literatura);
  (c) el archivo declara «% ORIGEN-VALOR: <n> — <razon>» con razon no vacia.

    python3 src/verificacion/r73_papers.py          # resumen por paper
    python3 src/verificacion/r73_papers.py detalle  # cada numero sin origen
"""
import bisect
import glob
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
NUM = re.compile(r"[-+]?\d+\.\d+(?:[eE][-+]?\d+)?")
# decimal seguido (con espacios, llaves o $ de por medio) de \pm, ^{+ o \sigma
RES = re.compile(r"(?<![\d.])(\d+\.\d+)(?=\s*\$?\s*(?:\\pm|\^\{\s*\+|\\,?\s*\\sigma|~?\\sigma))")
DECL = re.compile(r"%[ \t]*ORIGEN-VALOR:[ \t]*([-+]?\d+\.\d+)[ \t]*[—-]+[ \t]*(\S[^\n]*)")
CITA = re.compile(r"\\cite[pt]?\*?\{")
_CORTE = re.compile(r"(?<!\d)\.\s|\\\\")   # fin de frase o de fila .tex


def cifras(s):
    return len(re.sub(r"[^0-9]", "", s.lstrip("0.").replace(".", "")))


def fuentes():
    """Todos los numeros de logs, datos crudos, CANONICAL y ssee_core (abs, ordenados)."""
    out = []

    def walk(o):
        if isinstance(o, dict):
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            out.append(abs(float(o)))

    rutas = [p for d in ("results/logs", "data/raw") for p in (ROOT / d).rglob("*")]
    for p in rutas:
        if not p.is_file() or p.stat().st_size > 50e6:
            continue
        if p.suffix == ".json":
            try:
                walk(json.loads(p.read_text(errors="ignore")))
                continue
            except Exception:
                pass
        if p.suffix in (".json", ".log", ".txt", ".csv", ".md", ".dat", ".tsv"):
            out += [abs(float(x)) for x in NUM.findall(p.read_text(errors="ignore"))]
    import yaml
    walk(yaml.safe_load((ROOT / "CANONICAL_VALUES.yaml").read_text()))
    out += [abs(float(x)) for x in NUM.findall((ROOT / "src" / "ssee_core.py").read_text())]
    return sorted(set(out))


def en_fuente(s, pool):
    x = float(s)
    d = len(s.split(".")[1])
    u = 0.5 * 10 ** -d + 1e-12
    i = bisect.bisect_left(pool, x - u)
    return i < len(pool) and pool[i] <= x + u


def unidad(texto, pos):
    """Frase o fila de tabla que contiene pos (el texto ya viene sin comentarios)."""
    ini = max([m.end() for m in _CORTE.finditer(texto, 0, pos)], default=0)
    m = _CORTE.search(texto, pos)
    return texto[ini:m.start() if m else len(texto)]


def revisa(texto, pool):
    """Devuelve (sin_origen, no_verificables) para un .tex dado como texto."""
    decl = {m.group(1) for m in DECL.finditer(texto) if m.group(2).strip()}
    # se quitan los comentarios (conservando la longitud por linea no importa:
    # se trabaja sobre el texto limpio de punta a punta)
    lim = "\n".join(re.sub(r"(?<!\\)%.*", "", ln) for ln in texto.split("\n"))
    sin, nover = [], 0
    for m in RES.finditer(lim):
        s = m.group(1)
        if cifras(s) < 3:
            nover += 1
            continue
        if s in decl or en_fuente(s, pool) or CITA.search(unidad(lim, m.start())):
            continue
        ln = lim.count("\n", 0, m.start()) + 1
        sin.append((ln, s, lim.split("\n")[ln - 1].strip()[:110]))
    return sin, nover


def barrido(pool=None):
    pool = fuentes() if pool is None else pool
    res, nover = {}, 0
    tex = sorted((ROOT / "manuscript").glob("*.tex")) + sorted((ROOT / "submission_PRD").glob("*.tex"))
    for f in tex:
        s, n = revisa(f.read_text(errors="ignore"), pool)
        nover += n
        if s:
            res[str(f.relative_to(ROOT))] = s
    return res, nover


if __name__ == "__main__":
    res, nover = barrido()
    print(f"R73: {sum(len(v) for v in res.values())} numeros-resultado sin origen "
          f"en {len(res)} papers · {nover} de <3 cifras no verificables por valor")
    for f, v in sorted(res.items()):
        print(f"## {f} ({len(v)})")
        if len(sys.argv) > 1:
            for ln, s, t in v:
                print(f"   L{ln:<5} {s:>10} | {t}")
