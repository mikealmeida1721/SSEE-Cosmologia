#!/usr/bin/env python3
"""procedencia_resella.py — re-sella un acta que salió «con cambios sin commitear»
cuando lo que corrió quedó DESPUÉS en un commit, bit a bit (2026-10-28).

POR QUE. Un acta con `reproducible_desde_commit: false` dice: «el commit de HEAD
no basta para reproducir esto, el script tenía cambios». Si esos cambios se
commitean más tarde SIN tocar un byte, el código que corrió sí existe en git,
sólo que en un commit posterior. Re-correr (días, para las minimizaciones de
ΛCDM conjunta) no aporta nada. Pasó el 2026-10-28: lcdm_conjunta.py tenía 2
líneas (ruta a las cadenas v2) sin commitear al lanzar min_kids y min_conjunta.

QUE EXIGE, todo o nada (si algo falla, no toca el log):
  1. el acta existe y está marcada `reproducible_desde_commit: false`
  2. lo sucio era sólo el script y/o src/ssee_core.py (lo único que mira acta())
  3. `git show <commit>:<script>` tiene el sha256 del acta, y lo mismo el núcleo
  4. el commit indicado desciende del commit original del acta
Entonces cambia `commit` al nuevo, pone `reproducible_desde_commit: true`,
vacía `cambios_sin_commitear` y deja constancia en `resellado` (commit original,
lista sucia original, fecha, motivo). Las entradas no se tocan: R75 las sigue
cotejando por su hash.

    python src/procedencia_resella.py <commit> <log> [<log> ...]
"""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from procedencia import MARCA, ROOT, lee_acta  # noqa: E402


def _show(commit, ruta):
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:{ruta}"],
                          capture_output=True).stdout


def resella(commit, log):
    p = pathlib.Path(log)
    a = lee_acta(p)
    if not a:
        return f"{log}: sin acta, no se toca"
    if a.get("reproducible_desde_commit"):
        return f"{log}: ya es reproducible, no se toca"
    permitidos = {a["script"], "src/ssee_core.py"}
    sucios = [ln.split()[-1] for ln in a.get("cambios_sin_commitear", []) if ln.strip()]
    if not sucios or not set(sucios) <= permitidos:
        return f"{log}: lo sucio {sucios} no es sólo script/núcleo, NO se re-sella"
    if hashlib.sha256(_show(commit, a["script"])).hexdigest() != a["script_sha256"]:
        return f"{log}: el script en {commit[:7]} NO es el que corrió, NO se re-sella"
    if a.get("nucleo_sha256") and \
            hashlib.sha256(_show(commit, "src/ssee_core.py")).hexdigest() != a["nucleo_sha256"]:
        return f"{log}: el núcleo en {commit[:7]} NO es el que corrió, NO se re-sella"
    if subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor",
                       a["commit"], commit]).returncode != 0:
        return f"{log}: {commit[:7]} no desciende de {a['commit'][:7]}, NO se re-sella"
    a["resellado"] = dict(commit_original=a["commit"], cambios_originales=a["cambios_sin_commitear"],
                          fecha=datetime.datetime.now().isoformat(timespec="seconds"),
                          motivo="el script que corrió quedó commiteado sin cambios; "
                                 "sha256 cotejado contra el commit nuevo")
    a["commit"], a["reproducible_desde_commit"], a["cambios_sin_commitear"] = commit, True, []
    if p.suffix == ".json":
        d = json.loads(p.read_text())
        d["_procedencia"] = a
        p.write_text(json.dumps(d, indent=1, ensure_ascii=False))
    else:
        lineas = p.read_text().splitlines(keepends=True)
        for i, ln in enumerate(lineas[:50]):
            if ln.startswith(MARCA) or ln.startswith("%" + MARCA[1:]):
                lineas[i] = ln[:len(MARCA)] + json.dumps(a, ensure_ascii=False) + "\n"
                break
        p.write_text("".join(lineas))
    return f"{log}: re-sellado en {commit[:7]} (era {a['resellado']['commit_original'][:7]})"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    c = subprocess.run(["git", "-C", str(ROOT), "rev-parse", sys.argv[1]],
                       capture_output=True, text=True).stdout.strip()
    for lg in sys.argv[2:]:
        print(resella(c, lg))
