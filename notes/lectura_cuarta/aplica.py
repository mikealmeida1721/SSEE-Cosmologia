#!/usr/bin/env python3
"""Aplica las decisiones VAL / FIX de notes/lectura_cuarta/<DOC>.yaml (2026-10-10).

Para cada número con decision VAL:
  - comprueba que la fuente existe, que el log está en la cadena DVC (si no, no se
    puede \\val: se lista en «fuera_de_cadena») y que el valor, al formato pedido,
    es el del texto (si no y no hay `nuevo`, se lista en «no_casa»);
  - añade la macro a manuscript/valores.yaml si no existe (si existe con otra fuente,
    se lista en «choque» y no se toca);
  - reemplaza en la línea indicada el número por \\val{nombre} (sólo si aparece una
    vez fuera de \\val; si no, «ambiguo»).
FIX: reemplaza `num` por `nuevo` en la línea (misma regla de unicidad).
Las «afirmaciones» NO se aplican solas: las revisa y aplica Claude.

    python3 notes/lectura_cuarta/aplica.py P3            # ensayo (no escribe)
    python3 notes/lectura_cuarta/aplica.py P3 --escribe
"""
import json, re, sys, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "notes/lectura_cuarta"))
import inventario as inv

def cadena():
    outs = set()
    for s in yaml.safe_load(open(ROOT / "dvc.yaml"))["stages"].values():
        for o in s.get("outs", []) or []:
            outs.add(o if isinstance(o, str) else list(o)[0])
    return outs

def lee(ref):
    ruta, clave = ref.split("#", 1)
    v = json.load(open(ROOT / ruta))
    for k in re.findall(r"[^.\[\]]+|\[\d+\]", clave):
        v = v[int(k[1:-1])] if k.startswith("[") else v[k]
    return v

def main():
    doc, escribe = sys.argv[1], "--escribe" in sys.argv
    dec = yaml.safe_load(open(ROOT / f"notes/lectura_cuarta/{doc}.yaml"))
    vy = ROOT / "manuscript/valores.yaml"
    vals = yaml.safe_load(open(vy))
    cad = cadena()
    nuevos, rep = {}, {k: [] for k in ("fuera_de_cadena", "no_casa", "choque", "ambiguo", "sin_fuente", "hecho")}
    archivos = {pathlib.Path(f).name: ROOT / f for f in inv.DOCS[doc]}
    texto = {n: p.read_text().split("\n") for n, p in archivos.items()}
    # normaliza: «nombre (YA EXISTE)» → nombre; «ver línea N» hereda la decisión VAL de la
    # línea N con el mismo número; una macro existente manda su fuente y formato.
    porlinea = {}
    for x in dec.get("numeros", []) or []:
        if x.get("nombre"):
            x["nombre"] = re.split(r"[\s(/]", str(x["nombre"]).strip())[0]
        porlinea.setdefault((int(x["linea"]), str(x["num"]).lstrip("-")), x)
    for x in dec.get("numeros", []) or []:
        if x.get("decision") == "VAL" and not x.get("nombre"):
            m = re.search(r"ver l[ií]nea (\d+)", x.get("nota") or "")
            if m:
                ref = porlinea.get((int(m.group(1)), str(x["num"]).lstrip("-")))
                if ref and ref.get("nombre"):
                    x["nombre"] = ref["nombre"]
        if x.get("nombre") in vals:
            x["fuente"] = vals[x["nombre"]]["fuente"]; x["formato"] = vals[x["nombre"]].get("formato", "")
    for x in dec.get("numeros", []) or []:
        d = x.get("decision")
        if d not in ("VAL", "FIX"):
            continue
        f, ln, num = x["archivo"], int(x["linea"]), str(x["num"])
        if f not in texto:
            rep["sin_fuente"].append(x); continue
        if d == "VAL":
            nom, fu, fmt = x.get("nombre"), x.get("fuente"), x.get("formato", "")
            if not nom or not fu:
                rep["sin_fuente"].append(x); continue
            if fu.split("#")[0] not in cad:
                rep["fuera_de_cadena"].append(x); continue
            try:
                v = lee(fu)
            except Exception as e:
                rep["sin_fuente"].append({**x, "error": str(e)}); continue
            s = format(v, fmt) if not isinstance(v, str) else v
            if s.lstrip("-") != num.lstrip("-") and not x.get("nuevo"):
                rep["no_casa"].append({**x, "log_da": s}); continue
            if nom in vals and vals[nom]["fuente"] != fu:
                rep["choque"].append({**x, "existente": vals[nom]["fuente"]}); continue
            if nom not in vals:
                nuevos[nom] = {"fuente": fu, "formato": fmt}; vals[nom] = nuevos[nom]
            reemplazo = rf"\val{{{nom}}}"
            if num.startswith("-") is False and s.startswith("-"):
                reemplazo = reemplazo  # el signo del texto se respeta tal cual
        else:
            reemplazo = str(x.get("nuevo") or "")
            if not reemplazo or re.search(r"revisar|verificar|no coincide|PENDIENTE|recalc|≈", reemplazo, re.I):
                rep.setdefault("fix_sin_latex", []).append(x); continue
        L = texto[f][ln - 1]
        fuera = re.sub(r"\\val\{[^}]*\}", lambda m: "\0" * len(m.group(0)), L)
        pos = [m.start() for m in re.finditer(rf"(?<![\w.]){re.escape(num)}(?![\w])", fuera)]
        if len(pos) != 1:
            rep["ambiguo"].append({**x, "apariciones": len(pos)}); continue
        ini = pos[0]
        if d == "VAL" and s.startswith("-") and not num.startswith("-"):
            m = re.search(r"(-|−)\s*$", L[:ini])
            if not m:
                rep.setdefault("signo", []).append({**x, "log_da": s}); continue
            ini = m.start()
        texto[f][ln - 1] = L[:ini] + reemplazo + L[pos[0] + len(num):]
        rep["hecho"].append(f"{f}:{ln} {num} → {reemplazo}")
    for k, v in rep.items():
        print(f"{k}: {len(v)}")
        if k != "hecho":
            for e in v[:40]:
                print("   ", json.dumps(e, ensure_ascii=False)[:220])
    if escribe:
        for n, p in archivos.items():
            p.write_text("\n".join(texto[n]))
        if nuevos:
            with open(vy, "a") as fh:
                fh.write(f"# cuarta lectura {doc} (2026-10-10, notes/lectura_cuarta/{doc}.yaml)\n")
                for k, v in nuevos.items():
                    fh.write(f'{k}: {{fuente: "{v["fuente"]}", formato: "{v["formato"]}"}}\n')
        print(f"escrito: {len(rep['hecho'])} reemplazos, {len(nuevos)} macros nuevas")

if __name__ == "__main__":
    main()
