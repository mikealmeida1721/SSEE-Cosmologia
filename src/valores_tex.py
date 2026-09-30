#!/usr/bin/env python3
"""valores_tex.py — los numeros de los papers SALEN de los logs, no se teclean (2026-09-30).

Es el patron `\\variable` de showyourwork (Luger et al.), sin la herramienta:
un solo archivo declara de que log y de que clave sale cada numero que un paper
cita (manuscript/valores.yaml) y este script escribe manuscript/valores_generados.tex
con una macro por numero. El paper escribe \\val{S8_b1_ssee}, nunca el numero tecleado.
Si el log cambia, el numero del paper cambia al regenerar; si alguien teclea el
numero a mano, R74 lo cuenta como sin procedencia.

valores.yaml:
    S8_b1_ssee:
      fuente: results/logs/s8_desde_b1.json#filas.SSEE.S8
      formato: ".4f"              # como se imprime (format spec de Python)

La fuente tiene que ser un resultado DE LA CADENA (declarado en dvc.yaml, con
lock y acta): una clave que apunte a un log fuera de la cadena es un error, no
un aviso — si no, la macro solo traslada el numero tecleado un paso mas atras.

Uso en LaTeX (una vez en el preambulo):  \\input{valores_generados.tex}
"""
import json
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from procedencia import cabecera  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEF = ROOT / "manuscript" / "valores.yaml"
OUT = ROOT / "manuscript" / "valores_generados.tex"


def _cadena():
    st = (yaml.safe_load((ROOT / "dvc.yaml").read_text()) or {}).get("stages") or {}
    return {o if isinstance(o, str) else list(o)[0] for d in st.values() for o in (d.get("outs") or [])}


def _lee(ref):
    ruta, clave = ref.split("#", 1)
    d = json.loads((ROOT / ruta).read_text())
    for k in clave.split("."):
        d = d[int(k)] if isinstance(d, list) else d[k]
    return ruta, d


def genera():
    defs = yaml.safe_load(DEF.read_text()) or {}
    cadena = _cadena()
    fuentes = sorted({ROOT / d["fuente"].split("#")[0] for d in defs.values()} | {DEF})
    lineas = [cabecera(__file__, entradas=fuentes, comentario="%"),
              "% GENERADO por src/valores_tex.py desde manuscript/valores.yaml — NO EDITAR A MANO.",
              "% Cada numero sale de un log de la cadena de procedencia (dvc.yaml + acta).",
              r"\providecommand{\val}[1]{\csname ssee@val@#1\endcsname}"]
    errores = []
    for nom, d in sorted(defs.items()):
        ruta, v = _lee(d["fuente"])
        if ruta not in cadena:
            errores.append(f"{nom}: {ruta} no esta en la cadena (dvc.yaml)")
            continue
        s = format(v, d.get("formato", "")) if not isinstance(v, str) else v
        lineas.append(rf"\expandafter\def\csname ssee@val@{nom}\endcsname{{{s}}}  % {d['fuente']}")
    if errores:
        sys.exit("valores_tex: " + "; ".join(errores))
    OUT.write_text("\n".join(lineas) + "\n")
    print(f"  {len(defs)} valores -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    genera()
