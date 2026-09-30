#!/usr/bin/env python3
"""procedencia.py — el ACTA DE NACIMIENTO de cada log (2026-09-30).

POR QUE. Regla de Mike: ningun numero sin su fuente, y quien revise cualquier
resultado tiene que poder reproducirlo. Un log que no dice con que codigo, que
datos y en que estado del repositorio se produjo no es una fuente: es un numero
escrito en un archivo. Es la «procedencia retrospectiva» del estandar W3C PROV
(y de herramientas como noWorkflow), en su forma minima.

QUE REGISTRA el acta:
  commit        git HEAD al correr, y si el arbol tenia cambios sin commitear
                en el script o en el nucleo (si los tiene, el commit NO basta
                para reproducir: se marca `reproducible_desde_commit: false`)
  script        ruta y sha256 del script que corrio
  nucleo        sha256 de src/ssee_core.py (las constantes del modelo)
  entradas      sha256 de cada archivo de entrada declarado (datos, cadenas, logs)
  argv, fecha, host, nucleos (OMP/MKL/OPENBLAS y mpirun), versiones de python,
  numpy, camb, cobaya, getdist (las que esten importadas)

USO en un script que escribe un .json:
    from procedencia import con_acta
    json.dump(con_acta(res, __file__, entradas=[ruta1, ruta2]), open(salida, "w"), indent=1)
Para un log de texto:
    from procedencia import cabecera
    print(cabecera(__file__, entradas=[...]))      # primera linea del log

La verificacion vive en el guardian (R75): el sha256 del script en el acta
tiene que coincidir con el del script EN ESE COMMIT, y las entradas con su hash.
"""
import datetime
import hashlib
import json
import os
import pathlib
import platform
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARCA = "# ACTA-PROCEDENCIA "


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _git(*a):
    try:
        return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True,
                              timeout=30).stdout.strip()
    except Exception:
        return ""


def _rel(p):
    p = pathlib.Path(p).resolve()
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def acta(script, entradas=()):
    script = pathlib.Path(script).resolve()
    core = ROOT / "src" / "ssee_core.py"
    sucio = _git("status", "--porcelain", "--", _rel(script), _rel(core))
    vers = {}
    for m in ("numpy", "scipy", "camb", "cobaya", "getdist"):
        if m in sys.modules:
            vers[m] = getattr(sys.modules[m], "__version__", "?")
    ent = {}
    for e in entradas:
        e = pathlib.Path(e)
        ent[_rel(e)] = sha256(e) if e.is_file() else "NO-EXISTE"
    return dict(
        commit=_git("rev-parse", "HEAD"),
        reproducible_desde_commit=not bool(sucio),
        cambios_sin_commitear=sucio.splitlines(),
        script=_rel(script), script_sha256=sha256(script),
        nucleo_sha256=sha256(core) if core.exists() else None,
        entradas=ent,
        argv=sys.argv, fecha=datetime.datetime.now().isoformat(timespec="seconds"),
        host=platform.node(), python=platform.python_version(), versiones=vers,
        nucleos={k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS",
                                                 "OPENBLAS_NUM_THREADS", "OMPI_COMM_WORLD_SIZE")})


def con_acta(res, script, entradas=()):
    """Devuelve una COPIA de `res` con su acta en la clave `_procedencia`."""
    out = dict(res)
    out["_procedencia"] = acta(script, entradas)
    return out


def cabecera(script, entradas=()):
    """Primera linea de un log de texto: el acta en una sola linea JSON."""
    return MARCA + json.dumps(acta(script, entradas), ensure_ascii=False)


def lee_acta(ruta):
    """El acta de un log (.json con `_procedencia` o texto con la MARCA), o None."""
    p = pathlib.Path(ruta)
    try:
        if p.suffix == ".json":
            return json.loads(p.read_text()).get("_procedencia")
        for ln in p.read_text(errors="ignore").splitlines()[:50]:
            if ln.startswith(MARCA):
                return json.loads(ln[len(MARCA):])
    except Exception:
        return None
    return None


def verifica(ruta):
    """(ok, motivo) para un log con acta: script y entradas tienen que ser, bit a
    bit, los que dice el acta — el script tal como estaba en su commit."""
    a = lee_acta(ruta)
    if not a:
        return False, "sin acta"
    if not a.get("reproducible_desde_commit"):
        return False, f"corrio con cambios sin commitear: {a.get('cambios_sin_commitear')}"
    viejo = subprocess.run(["git", "-C", str(ROOT), "show", f"{a['commit']}:{a['script']}"],
                           capture_output=True).stdout
    if not viejo or hashlib.sha256(viejo).hexdigest() != a["script_sha256"]:
        return False, "el script de su commit no tiene el hash del acta"
    for e, h in a.get("entradas", {}).items():
        f = ROOT / e if not os.path.isabs(e) else pathlib.Path(e)
        if h == "NO-EXISTE" or not f.is_file():
            return False, f"entrada ausente: {e}"
        if sha256(f) != h:
            return False, f"entrada cambiada desde la corrida: {e}"
    return True, "ok"
