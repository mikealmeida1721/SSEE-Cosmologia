#!/usr/bin/env python3
"""armar_zenodo.py — arma el paquete de una versión nueva de Zenodo, sin subir nada.

POR QUÉ EXISTE (2026-10-10)
---------------------------
Las versiones anteriores del record de papers (concept 10.5281/zenodo.19654118)
se armaron a mano contra la API: qué PDF iba con qué prefijo, de qué commit salía
el zip fuente y si cada PDF correspondía a su .tex sólo quedaba en la memoria de
la sesión. La auditoría de reproducibilidad (notes/lectura_tercera/REPRO.md)
encontró que no había ningún script que lo hiciera. Éste lo hace y deja un acta.

QUÉ HACE
--------
1. Exige árbol limpio en manuscript/, docs/ y submission_PRD/ (el paquete tiene
   que corresponder a un commit; si no, el zip fuente y los PDF no casan).
2. Comprueba que cada PDF de docs/ es byte a byte el que está en manuscript/
   (o submission_PRD/ para el PRD), es decir, que se copió tras compilar.
3. Copia los PDF con prefijo numérico (Zenodo no reordena por API: da 405).
4. `git archive HEAD` → zip fuente con el commit en el nombre.
5. Escribe MANIFIESTO.json con sha256 y md5 de cada archivo (Zenodo informa md5:
   tras subir se compara contra éste).

NO publica. Subir y publicar es un paso aparte, permanente, que va DESPUÉS de la
compuerta `preparar_publicacion.py --aplicar` (fecha única de portada).

USO
    .venv/bin/python3 src/verificacion/armar_zenodo.py            # arma en $SSEE_DATA_DIR/zenodo/
    .venv/bin/python3 src/verificacion/armar_zenodo.py --sin-git  # ensayo con árbol sucio (no vale para publicar)
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# (prefijo, PDF en docs/, PDF recién compilado del que debe ser copia)
PAQUETE = [
    ("00", "SSEE_Cover.pdf", "manuscript/SSEE_Cover.pdf"),
    ("01", "SSEE_Paper1_Framework.pdf", "manuscript/SSEE_Paper1_Framework.pdf"),
    ("02", "SSEE_Paper2_MCMC.pdf", "manuscript/SSEE_Paper2_MCMC.pdf"),
    ("03", "SSEE_Paper3_CMB.pdf", "manuscript/SSEE_Paper3_CMB.pdf"),
    ("04", "SSEE_Paper4_ToE.pdf", "manuscript/SSEE_Paper4_ToE.pdf"),
    ("05", "SSEE_Paper5_IS.pdf", "manuscript/SSEE_Paper5_IS.pdf"),
    ("06", "SSEE_Paper6_Growth.pdf", "manuscript/SSEE_Paper6_Growth.pdf"),
    ("07", "SSEE_Paper7_EFT.pdf", "manuscript/SSEE_Paper7_EFT.pdf"),
    ("08", "SSEE_Paper8_StrongGravity.pdf", "manuscript/SSEE_Paper8_StrongGravity.pdf"),
    ("09", "SSEE_Paper9_HubbleTension.pdf", "manuscript/SSEE_Paper9_HubbleTension.pdf"),
    ("10", "SSEE_Paper10_UVCompletion.pdf", "manuscript/SSEE_Paper10_UVCompletion.pdf"),
    ("11", "SSEE_Sealed_Journal.pdf", "manuscript/SSEE_Sealed_Journal.pdf"),
    ("12", "SSEE_Unified_Journal.pdf", "manuscript/SSEE_Unified_Journal.pdf"),
    ("13", "SSEE_Endorser_Summary.pdf", "manuscript/SSEE_Endorser_Summary.pdf"),
    ("14", "SSEE_Cover_Letter.pdf", "manuscript/SSEE_Cover_Letter.pdf"),
    ("15", "SSEE_PRD.pdf", "submission_PRD/SSEE_PRD.pdf"),
]


def _hash(p, algo):
    h = hashlib.new(algo)
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-git", action="store_true", help="ensayo: no exige árbol limpio")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()

    problemas = []
    sucio = _git("status", "--porcelain", "--", "manuscript", "docs", "submission_PRD")
    sucio = [l for l in sucio.splitlines() if not l.startswith("??")]
    if sucio:
        (print if a.sin_git else problemas.append)(
            "árbol sucio en manuscript/docs/submission_PRD: " + "; ".join(sucio[:8]))

    for pre, doc, fuente in PAQUETE:
        d, s = ROOT / "docs" / doc, ROOT / fuente
        if not d.exists():
            problemas.append(f"falta docs/{doc}")
        elif s.exists() and _hash(d, "sha256") != _hash(s, "sha256"):
            problemas.append(f"docs/{doc} no es copia del compilado {fuente}")

    if problemas:
        print("NO SE ARMA:\n  - " + "\n  - ".join(problemas))
        return 1

    commit = _git("rev-parse", "--short=7", "HEAD")
    base = Path(a.salida) if a.salida else Path(os.environ.get("SSEE_DATA_DIR", "/mnt/datos/SSEE_data")) / "zenodo"
    out = base / f"{datetime.now():%Y-%m-%d}_{commit}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    archivos = []
    for pre, doc, _ in PAQUETE:
        dst = out / f"{pre}_{doc}"
        shutil.copy2(ROOT / "docs" / doc, dst)
        archivos.append(dst)
    zp = out / f"16_SSEE_source_{commit}.zip"
    subprocess.run(["git", "archive", "--format=zip", "-o", str(zp), "HEAD"], cwd=ROOT, check=True)
    archivos.append(zp)

    acta = {
        "_procedencia": {
            "script": "src/verificacion/armar_zenodo.py",
            "commit": _git("rev-parse", "HEAD"),
            "arbol_limpio": not sucio,
            "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "concept_doi": "10.5281/zenodo.19654118",
        "archivos": [{"nombre": p.name, "bytes": p.stat().st_size,
                      "sha256": _hash(p, "sha256"), "md5": _hash(p, "md5")} for p in archivos],
    }
    (out / "MANIFIESTO.json").write_text(json.dumps(acta, indent=2, ensure_ascii=False) + "\n")
    print(f"paquete: {out}  ({len(archivos)} archivos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
