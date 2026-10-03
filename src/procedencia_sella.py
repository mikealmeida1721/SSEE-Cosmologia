#!/usr/bin/env python3
"""procedencia_sella.py — pone el acta a un log que su script escribe sin ella (2026-10-03).

POR QUE. Muchos scripts anteriores a procedencia.py escriben su log sin acta. Para
meterlos en la cadena (R75) sin reescribir cada uno, la etapa DVC llama a este
sellador JUSTO DESPUES de correr el script, en el mismo `cmd`:

    python src/X.py && python src/procedencia_sella.py src/X.py results/logs/X.json [entradas...]

El acta es la MISMA que daría `con_acta` dentro del script: commit, sha256 del
script y del núcleo, hash de cada entrada declarada y si había cambios sin
commitear (en ese caso queda `reproducible_desde_commit: false` y R75 lo rechaza).
Sólo cambia quién la escribe. `argv` registra el del sellador, no el del script.

  .json -> clave `_procedencia` (si el log ya trae acta propia, no se toca)
  otro  -> primera línea `# ACTA-PROCEDENCIA {...}`
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from procedencia import MARCA, acta, lee_acta  # noqa: E402


def main(script, log, entradas):
    p = pathlib.Path(log)
    if not p.is_file():
        sys.exit(f"procedencia_sella: el script no dejó {log}")
    if lee_acta(p):
        print(f"procedencia_sella: {log} ya trae acta propia; no se toca")
        return
    a = acta(script, entradas)
    if p.suffix == ".json":
        d = json.loads(p.read_text())
        if not isinstance(d, dict):
            sys.exit(f"procedencia_sella: {log} no es un objeto JSON")
        d["_procedencia"] = a
        p.write_text(json.dumps(d, indent=1, ensure_ascii=False))
    else:
        p.write_text(MARCA + json.dumps(a, ensure_ascii=False) + "\n" + p.read_text())
    print(f"procedencia_sella: acta puesta en {log} (commit {a['commit'][:7]}, "
          f"reproducible={a['reproducible_desde_commit']})")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
