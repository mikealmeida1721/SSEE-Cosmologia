#!/usr/bin/env python3
"""empaqueta_datos_propios.py — arma el paquete de datos de SSEE para Zenodo (2026-10-17).

QUÉ ES. Todo lo que las etapas de dvc.yaml leen y que NO es de terceros ni viaja en
git: las cadenas MCMC propias (Paper 2, Paper 3/B1, Paper 6, calibradores ACT/SPT),
el mejor punto de nuisances de DES, la reproducción de Union3, la copia exacta del
diccionario con que corrió p04_rutas_mv, y los extractos de literatura (resúmenes de
arXiv, ficha pública del catálogo eRASS1) que se citan pero no se pueden bajar con
huella estable. Son las entradas con receta «paquete_ssee» de
data/manifiesto_externos.json.

FAMILIAS. De cada cadena va la familia entera (mismo prefijo: .input.yaml,
.updated.yaml, .progress, .covmat…), no sólo los .txt declarados: getdist y los
lectores de convergencia las abren aunque dvc.yaml no las nombre.

DETERMINISTA. Orden alfabético, fechas, dueño y permisos fijos, gzip sin fecha: quien
lo vuelva a armar con los mismos archivos obtiene el mismo sha256.

DISPOSICIÓN dentro del tar:
    SSEE_data/<ruta bajo /mnt/datos/SSEE_data>   → la carpeta SSEE_DATOS del verificador
    repo/<ruta relativa al repositorio>          → el clon del repositorio
    SHA256SUMS                                    → huella de cada archivo

USO
    .venv/bin/python3 src/verificacion/empaqueta_datos_propios.py [carpeta_salida]
    (por defecto /mnt/datos/SSEE_paquete)
"""
import glob
import gzip
import hashlib
import io
import json
import os
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFIESTO = ROOT / "data" / "manifiesto_externos.json"
D = "/mnt/datos/SSEE_data"
FECHA_FIJA = 1767225600  # 2026-01-01 00:00 UTC; ORIGEN-VALOR: constante arbitraria para que el tar sea determinista


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _nombre_en_tar(ruta):
    if ruta.startswith(D + "/"):
        return "SSEE_data/" + ruta[len(D) + 1:]
    if not ruta.startswith("/"):
        return "repo/" + ruta
    raise ValueError(f"ruta fuera de SSEE_data y del repo: {ruta}")


def archivos_del_paquete():
    m = json.load(open(MANIFIESTO))
    declarados = []
    for e in m["ficheros"]:
        if e["receta"] != "paquete_ssee":
            continue
        base = e["ruta"] if e["ruta"].startswith("/") else str(ROOT / e["ruta"])
        if os.path.isdir(base):
            declarados += [os.path.join(base, a["rel"]) for a in e["archivos"]]
        else:
            declarados.append(base)
    todos = set(declarados)
    for f in declarados:
        d, n = os.path.split(f)
        if "/chains" in d or "/mcmc/" in d or "calibrador" in d:
            todos.update(glob.glob(os.path.join(d, n.split(".")[0] + ".*")))
    todos = {f for f in todos if os.path.isfile(f) and not f.endswith(".locked")}
    salida = []
    for f in sorted(todos):
        rel = os.path.relpath(f, ROOT) if f.startswith(str(ROOT) + "/") else f
        salida.append((f, _nombre_en_tar(rel)))
    return salida, len(declarados)


def main():
    destino = Path(sys.argv[1] if len(sys.argv) > 1 else "/mnt/datos/SSEE_paquete")
    destino.mkdir(parents=True, exist_ok=True)
    lista, n_decl = archivos_del_paquete()
    sumas = []
    salida = destino / "ssee_datos_propios.tar.gz"
    with open(salida, "wb") as crudo:
        with gzip.GzipFile(fileobj=crudo, mode="wb", compresslevel=6, mtime=0, filename="") as gz:
            with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tar:
                for origen, nombre in lista:
                    ti = tar.gettarinfo(origen, arcname=nombre)
                    ti.mtime, ti.uid, ti.gid, ti.uname, ti.gname, ti.mode = FECHA_FIJA, 0, 0, "", "", 0o644
                    with open(origen, "rb") as f:
                        tar.addfile(ti, f)
                    sumas.append(f"{_sha(origen)}  {nombre}")
                texto = ("\n".join(sumas) + "\n").encode()
                ti = tarfile.TarInfo("SHA256SUMS")
                ti.size, ti.mtime, ti.mode = len(texto), FECHA_FIJA, 0o644
                tar.addfile(ti, io.BytesIO(texto))
    (destino / "SHA256SUMS").write_text("\n".join(sumas) + "\n")
    resumen = {
        "paquete": str(salida), "sha256": _sha(salida), "bytes": salida.stat().st_size,
        "archivos": len(lista), "declarados_en_dvc": n_decl, "familia_extra": len(lista) - n_decl,
        "bytes_sin_comprimir": sum(os.path.getsize(o) for o, _ in lista),
    }
    (destino / "paquete.json").write_text(json.dumps(resumen, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps(resumen, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
