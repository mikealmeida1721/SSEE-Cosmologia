#!/usr/bin/env python3
"""descripcion_zenodo.py — llena la descripción de la versión de Zenodo desde valores_generados.tex.

POR QUÉ EXISTE (2026-10-16). La descripción de la versión de julio llevaba números
tecleados a mano (ΔBIC −32.9 sin log, H₀ local 72.86, la partícula de 40.70 eV) que
después se retiraron. Esta plantilla no lleva ningún número: cada {{clave}} sale de
manuscript/valores_generados.tex, la misma fuente que los PDF, así que la descripción
y los documentos no pueden decir cosas distintas. Falla si falta una clave.

USO
    .venv/bin/python3 src/verificacion/descripcion_zenodo.py SALIDA.html
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PLANTILLA = ROOT / "notes" / "zenodo" / "descripcion_papers.html.in"


def valores():
    vg = (ROOT / "manuscript" / "valores_generados.tex").read_text()
    out = {}
    # El valor puede traer llaves propias (4.2\times10^{-6}): se cuenta el balance.
    for m in re.finditer(r"ssee@val@([A-Za-z0-9_]+)\\endcsname\{", vg):
        i, prof = m.end(), 1
        while prof:
            prof += {"{": 1, "}": -1}.get(vg[i], 0)
            i += 1
        out[m.group(1)] = vg[m.end():i - 1]
    return out


def llenar(texto, vals):
    faltan = sorted({k for k in re.findall(r"\{\{([A-Za-z0-9_]+)\}\}", texto) if k not in vals})
    if faltan:
        sys.exit(f"faltan claves en valores_generados.tex: {faltan}")
    s = re.sub(r"\{\{([A-Za-z0-9_]+)\}\}", lambda m: vals[m.group(1)], texto)
    # Formato de LaTeX que no sirve en HTML: el signo menos y los \times.
    s = re.sub(r"(?<![\w.])-(?=\d)", "−", s)
    return s


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    vals = valores()
    vals["COMMIT"] = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                             cwd=ROOT, text=True).strip()
    html = llenar(PLANTILLA.read_text(), vals)
    resto = re.findall(r"\\[A-Za-z]+|\$", html)
    if resto:
        sys.exit(f"quedó LaTeX en la descripción: {sorted(set(resto))}")
    pathlib.Path(sys.argv[1]).write_text(html)
    print(f"escrito {sys.argv[1]} ({len(html)} caracteres, commit {vals['COMMIT']})")
