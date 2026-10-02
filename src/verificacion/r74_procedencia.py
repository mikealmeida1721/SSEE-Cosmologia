#!/usr/bin/env python3
"""R74 — PROCEDENCIA UNIVERSAL: ningun numero, en ningun lado, sin su fuente (2026-09-30).

LA REGLA DE MIKE, tal cual: «no debe existir un solo numero puesto a mano, y si
se pone a mano debe estar su razon detras; y eso incluye no solo los papers sino
todo lo demas». La credibilidad del modelo es que quien revise CUALQUIER numero
pueda reproducirlo. R65 lo exigia solo en scripts y R73 solo en una parte de los
papers: el modelo no es una carpeta.

SUPERFICIES y que cuenta como deuda en cada una:
  logs       results/logs/*: log sin script en PROPAGACION.yaml ni marca de historico
             (nadie sabe con que se reproduce).
  canonical  CANONICAL_VALUES.yaml `canonical:`: clave numerica cuyo valor no esta en
             ningun log ni en src/ssee_core.py, y sin `# FUENTE:` en su linea.
  papers     manuscript/*.tex, submission_PRD/*.tex: decimal de >=3 cifras sin log,
             dato crudo, CANONICAL, nucleo, cita en su frase ni ORIGEN-VALOR.
  cajones    VERIFICATION_LEDGER.md, README.md, OPEN_PROBLEMS.md, CLAUDE.md: igual.

LIMITE DECLARADO. Casar por VALOR es la red minima, no la trazabilidad plena: un
numero corto (0.33 sigma) no se puede rastrear por valor y uno largo puede casar
por azar. La meta es el ENLACE EXPLICITO (macro generada desde el log, o
`FUENTE: log#clave`). Hasta llegar ahi, esta regla impide que la deuda CREZCA.

    python3 src/verificacion/r74_procedencia.py           # cuentas por superficie
    python3 src/verificacion/r74_procedencia.py detalle   # cada caso
"""
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src" / "verificacion"))
import r73_papers as R  # noqa: E402  (misma maquinaria de fuentes y cifras: sin copia)

NUMALL = re.compile(r"(?<![\w.])(\d+\.\d+)(?![\w.])")
CAJONES = ["VERIFICATION_LEDGER.md", "README.md", "OPEN_PROBLEMS.md", "CLAUDE.md"]



# Logs de ORQUESTACION: colas, vigilantes y reportes del guardian. Registran
# horas, PIDs, la convergencia (R-1) de corridas ajenas o el veredicto del
# guardian, no resultados del modelo. UNA sola
# definicion: la usan R74, R75 y R33 (2026-09-30; antes la tupla estaba
# tecleada en dos sitios).
ORQUESTACION = ("cola_", "vigilante_", "guardian_")

def _fmt(v):
    s = repr(float(v))
    return s if "." in s and "e" not in s else f"{float(v):.6f}"


def _logs_sin_script():
    P = yaml.safe_load((ROOT / "PROPAGACION.yaml").read_text())
    mapa = set()

    def w(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and v.startswith("src/"):
                    mapa.add(k)
                else:
                    w(v)
        elif isinstance(o, list):
            for x in o:
                w(x)
    w(P)
    hist = set(P.get("historicos") or [])
    st = (yaml.safe_load((ROOT / "dvc.yaml").read_text()) or {}).get("stages") or {} \
        if (ROOT / "dvc.yaml").exists() else {}
    cadena = {o if isinstance(o, str) else list(o)[0] for d in st.values() for o in (d.get("outs") or [])}
    # orquestacion (cola_*, vigilante_*): horas y PIDs, no resultados (mismo criterio que R75)
    return sorted(str(p.relative_to(ROOT)) for p in (ROOT / "results/logs").rglob("*")
                  if p.is_file() and p.suffix in (".log", ".json", ".txt", ".csv")
                  and not p.name.startswith(ORQUESTACION)
                  and str(p.relative_to(ROOT)) not in cadena
                  and p.stem not in mapa and p.stem not in hist)


def _canonical_sin_fuente():
    txt = (ROOT / "CANONICAL_VALUES.yaml").read_text()
    c = yaml.safe_load(txt)["canonical"]
    core = (ROOT / "src" / "ssee_core.py").read_text()
    logs = []
    for p in (ROOT / "results/logs").rglob("*"):
        if p.suffix in (".log", ".json", ".txt", ".csv") and R.es_fuente(p):
            logs += [abs(float(x)) for x in R.NUM.findall(p.read_text(errors="ignore"))]
    logs = sorted(set(logs + R.nucleo_evaluado()))
    lineas = {m.group(1): m.group(0) for m in re.finditer(r"^\s{2}(\w+):.*$", txt, re.M)}
    out = []
    for k, v in c.items():
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            continue
        s = _fmt(abs(v))
        if R.cifras(s) < 3 or R.en_fuente(s, logs) or str(v) in core:
            continue
        if fuente_verificada(lineas.get(k, ""), v):
            continue
        out.append((k, v))
    return out


FUENTE_REF = re.compile(r"#\s*FUENTE:\s*(\S+)")


def fuente_verificada(linea, v):
    """Una `# FUENTE: <ref>` NO vale por estar escrita: se abre y se comprueba.
      <ruta>              el valor, a su redondeo, aparece en ese archivo
      ssee_core.<NOMBRE>  el nucleo, importado, da ese valor a su redondeo
    Sin ref, ref ilegible o valor ausente: no hay fuente."""
    m = FUENTE_REF.search(linea)
    if not m:
        return False
    ref = m.group(1).rstrip(".,;)")
    s = _fmt(abs(v)) if not float(v).is_integer() else str(int(abs(v)))
    if ref.startswith("ssee_core."):
        import importlib.util
        sp = importlib.util.spec_from_file_location("_core74", ROOT / "src" / "ssee_core.py")
        core = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(core)
        x = getattr(core, ref.split(".", 1)[1], None)
        if not isinstance(x, (int, float)):
            return False
        dec = len(s.split(".")[1]) if "." in s else 0
        return round(abs(x), dec) == abs(float(s))
    f = ROOT / ref.split("#")[0]
    if not f.is_file():
        return False
    t = f.read_text(errors="ignore")
    if "." not in s:
        return re.search(rf"(?<![\d.]){s}(?![\d.])", t) is not None
    return R.en_fuente(s, sorted({abs(float(x)) for x in R.NUM.findall(t)}))


GIT_REF = re.compile(r"git:([0-9a-f]{7,40}):(\S+?)(?=[\s`),;]|$)")


def fuente_git(linea, s):
    """2026-10-01. Un valor HISTORICO de un cajon (una corrida que existio y fue
    superada) no tiene log vigente: su log vive en el historial. La linea lo
    declara como `git:<commit>:<ruta>` y aqui se ABRE ese archivo en ese commit
    y se comprueba que el valor, a su redondeo, este escrito ahi. Una referencia
    a un commit o ruta inexistente, o donde el valor no aparece, no es fuente."""
    import subprocess
    for sha, ruta in GIT_REF.findall(linea):
        o = subprocess.run(["git", "show", f"{sha}:{ruta}"], cwd=ROOT, capture_output=True,
                           text=True, timeout=20)
        if o.returncode == 0 and R.en_fuente(s, sorted({abs(float(x)) for x in R.NUM.findall(o.stdout)})):
            return True
    return False


def _texto(f, sin_comentarios):
    t = f.read_text(errors="ignore")
    if sin_comentarios:
        t = "\n".join(re.sub(r"(?<!\\)%.*", "", ln) for ln in t.split("\n"))
    return t


def _sin_origen(f, pool, tex):
    raw = f.read_text(errors="ignore")
    decl = {m.group(1) for m in R.DECL.finditer(raw) if m.group(2).strip()} if tex else set()
    t = _texto(f, tex)
    out = []
    for m in NUMALL.finditer(t):
        s = m.group(1)
        if R.cifras(s) < 3 or s in decl or R.en_fuente(s, pool):
            continue
        if R.CITA.search(R.unidad(t, m.start())) or R.es_arxiv(t, m.start(), s):
            continue
        ln = t.count("\n", 0, m.start()) + 1
        if not tex and "git:" in t.split("\n")[ln - 1] and fuente_git(t.split("\n")[ln - 1], s):
            continue
        out.append((ln, s))
    return out


def barrido():
    pool = R.fuentes()
    res = {"logs": _logs_sin_script(), "canonical": _canonical_sin_fuente(), "papers": {}, "cajones": {}}
    for f in sorted((ROOT / "manuscript").glob("*.tex")) + sorted((ROOT / "submission_PRD").glob("*.tex")):
        if f.name == "valores_generados.tex":
            continue   # generado desde logs de la cadena: lo vigila R75 por hash y acta
        s = _sin_origen(f, pool, True)
        if s:
            res["papers"][str(f.relative_to(ROOT))] = s
    for n in CAJONES:
        f = ROOT / n
        if f.exists():
            s = _sin_origen(f, pool, False)
            if s:
                res["cajones"][n] = s
    return res


def cuentas(res):
    return {"logs": len(res["logs"]), "canonical": len(res["canonical"]),
            "papers": sum(len(v) for v in res["papers"].values()),
            "cajones": sum(len(v) for v in res["cajones"].values())}


if __name__ == "__main__":
    res = barrido()
    print("R74 procedencia universal —", cuentas(res))
    if len(sys.argv) > 1:
        print("## logs sin script:", *res["logs"], sep="\n   ")
        print("## canonical sin fuente:", *res["canonical"], sep="\n   ")
        for k in ("papers", "cajones"):
            for f, v in sorted(res[k].items()):
                print(f"## {f} ({len(v)}):", " ".join(f"L{a}:{b}" for a, b in v[:40]))
