#!/usr/bin/env python3
"""Pre-clasifica el inventario: ALG (núcleo φ,π), LIT (\\cite en la línea), LOG (valor de un log),
CAN (CANONICAL_VALUES.yaml), ? (sin origen). Escribe notes/lectura_cuarta/clasificacion.json."""
import json, math, re, sys, pathlib, importlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "notes/lectura_cuarta"))
import inventario as inv
import ssee_core as c

def plano(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from plano(v, f"{pre}.{k}" if pre else str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o[:400]): yield from plano(v, f"{pre}[{i}]")
    elif isinstance(o, (int, float)) and not isinstance(o, bool) and math.isfinite(o):
        yield pre, float(o)

ALG = {}
for k in dir(c):
    v = getattr(c, k)
    if isinstance(v, float) and math.isfinite(v): ALG[f"ssee_core.{k}"] = v
try:
    for k, v in plano(json.load(open(ROOT / "results/logs/algebra_derivada.json"))): ALG[f"algebra_derivada:{k}"] = v
except Exception: pass
LOGS = []
for p in (ROOT / "results/logs").rglob("*.json"):
    if any(s in p.name for s in ("cola", "vigilante")): continue
    try: d = json.load(open(p))
    except Exception: continue
    for k, v in plano(d):
        if "_procedencia" in k: continue
        LOGS.append((f"{p.relative_to(ROOT/'results/logs')}#{k}", v))
for p in (ROOT / "data/raw").rglob("*"):
    if p.is_file() and p.suffix in (".csv", ".txt", ".dat", ".yaml", ".json") and p.stat().st_size < 5e6:
        for m in re.finditer(r"-?\d+\.\d+(?:[eE][-+]?\d+)?", p.read_text(errors="ignore")):
            LOGS.append((f"data/raw/{p.relative_to(ROOT/'data/raw')}", float(m.group(0))))
import yaml
CAN = []
try:
    for k, v in plano(yaml.safe_load(open(ROOT / "CANONICAL_VALUES.yaml"))): CAN.append((k, v))
except Exception: pass

def casa(txt, v):
    d = len(txt.split(".")[1]); x = float(txt)
    for cand in (v, abs(v), 100 * v, abs(100 * v)):
        if abs(round(cand, d) - x) < 0.5 * 10 ** -d + 1e-12: return True
    return False

def clasifica(doc):
    out = []
    raw = {}
    for f in inv.DOCS[doc]:
        raw[pathlib.Path(f).name] = (ROOT / f).read_text(errors="ignore").split("\n")
    for f, i, n, ctx in inv.numeros(doc):
        if "\\times" in n: n = n.split("\\times")[0]
        orig = raw[f][i - 1]
        if re.search(r"\\cite", orig): cl, src = "LIT", ""
        elif re.search(r"retract|retired|withdrawn|earlier|once quoted|formerly|superseded|artefact|was an|previously", orig, re.I): cl, src = "HIS", ""
        else:
            sig = len(n.replace(".", "").lstrip("0"))
            a = next((k for k, v in ALG.items() if casa(n, v)), None) if sig >= 3 else None
            if a: cl, src = "ALG", a
            else:
                l = next((k for k, v in LOGS if casa(n, v)), None) if sig >= 3 else None
                if l: cl, src = "LOG", l
                else:
                    k = next((k for k, v in CAN if casa(n, v)), None) if sig >= 3 else None
                    cl, src = ("CAN", k) if k else ("?" if sig >= 3 else "corto"), ""
                    if k: src = k
        out.append(dict(doc=doc, file=f, line=i, num=n, clase=cl, fuente=src, ctx=ctx))
    return out

if __name__ == "__main__":
    todo = []
    for d in inv.DOCS: todo += clasifica(d)
    json.dump(todo, open(ROOT / "notes/lectura_cuarta/clasificacion.json", "w"), ensure_ascii=False, indent=0)
    from collections import Counter
    for d in inv.DOCS:
        cn = Counter(x["clase"] for x in todo if x["doc"] == d)
        print(f"{d:9s} " + "  ".join(f"{k}={cn.get(k,0)}" for k in ("ALG","LIT","LOG","CAN","?","corto")))
