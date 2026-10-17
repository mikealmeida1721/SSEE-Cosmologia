#!/usr/bin/env python3
"""baja_externos.py — trae y VERIFICA todo lo que SSEE lee fuera de git (2026-10-17).

PARA QUIÉN. Para quien quiera comprobar SSEE en su máquina. Lee
data/manifiesto_externos.json (126 rutas, cada una con su origen y su receta) y:

  baja      descarga cada dato de su DUEÑO (SDSS, KiDS, DESI en Zenodo, eROSITA,
            GitHub de Pantheon+/DES-SN/Union3, arXiv, Planck vía cobaya-install),
            compila hi_class en su commit, y desempaca el paquete de datos propios
            de SSEE (cadenas MCMC: no se pueden bajar de nadie más).
  verifica  compara la huella sha256 de CADA archivo con la del manifiesto, que es la
            de los archivos con que corrió cada resultado. No confía en la descarga:
            también sirve para datos que el verificador consiguió por su cuenta.

DÓNDE. Las rutas del manifiesto son las ORIGINALES (/mnt/datos/SSEE_data…); aquí se
traducen a las carpetas del verificador, las mismas que monta entorno_ssee.sh:
    /mnt/datos/SSEE_data        → $SSEE_DATOS
    /home/mike/cobaya_packages  → $COBAYA_PACKAGES_PATH
    /mnt/datos/hi_class         → $SSEE_HICLASS
    rutas relativas             → este repositorio

USO
    export SSEE_DATOS=… COBAYA_PACKAGES_PATH=… SSEE_HICLASS=…
    .venv/bin/python3 src/verificacion/baja_externos.py baja --paquete <ruta o URL del .tar.gz>
    .venv/bin/python3 src/verificacion/baja_externos.py verifica
    (baja --solo kids1000,boss_dr12   para traer sólo esas recetas)
"""
import argparse
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFIESTO = ROOT / "data" / "manifiesto_externos.json"
AGENTE = "SSEE-verificacion/1.0 (reproducibilidad; https://github.com/mikealmeida1721)"


def raices():
    falta = [v for v in ("SSEE_DATOS", "COBAYA_PACKAGES_PATH", "SSEE_HICLASS") if not os.environ.get(v)]
    if falta:
        sys.exit("define " + ", ".join(falta) + " (ver el encabezado de este script)")
    return [("/mnt/datos/SSEE_data", os.environ["SSEE_DATOS"]),
            ("/home/mike/cobaya_packages", os.environ["COBAYA_PACKAGES_PATH"]),
            ("/mnt/datos/hi_class", os.environ["SSEE_HICLASS"])]


def local(ruta, R):
    """Ruta original del manifiesto → ruta en la máquina del verificador."""
    if not ruta.startswith("/"):
        return ROOT / ruta
    for orig, nueva in R:
        if ruta == orig or ruta.startswith(orig + "/"):
            return Path(nueva + ruta[len(orig):])
    raise ValueError(f"ruta sin raíz conocida: {ruta}")


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def esperados(m, R):
    """{ruta local: (sha256, receta)} de todo archivo que el manifiesto huella."""
    out = {}
    for e in m["ficheros"]:
        base = e["ruta"]
        es_dir = len(e["archivos"]) != 1 or e["archivos"][0]["rel"] != os.path.basename(base)
        for a in e["archivos"]:
            orig = f"{base}/{a['rel']}" if es_dir else base
            out[orig] = (local(orig, R), a["sha256"], e["receta"])
    return out


def _descarga(url, cache):
    cache.mkdir(parents=True, exist_ok=True)
    dest = cache / hashlib.sha1(url.encode()).hexdigest()[:16]
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    print(f"  ↓ {url}", flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(req, timeout=600) as r, open(str(dest) + ".parcial", "wb") as f:
        shutil.copyfileobj(r, f, 1 << 20)
    os.replace(str(dest) + ".parcial", dest)
    return dest


def _extrae(arch, tipo, en, necesarios, interno=None):
    """Saca del paquete sólo los miembros cuyo destino está en «necesarios»."""
    en = Path(en)
    hechos = 0
    if tipo == "zip":
        z = zipfile.ZipFile(arch)
        if interno:
            z = zipfile.ZipFile(io.BytesIO(z.read(interno)))
        for n in z.namelist():
            d = en / n
            if str(d) in necesarios:
                d.parent.mkdir(parents=True, exist_ok=True)
                with z.open(n) as src, open(d, "wb") as dst:
                    shutil.copyfileobj(src, dst, 1 << 20)
                hechos += 1
    else:
        with tarfile.open(arch) as t:
            for mi in t:
                d = en / mi.name
                if mi.isfile() and str(d) in necesarios:
                    d.parent.mkdir(parents=True, exist_ok=True)
                    with t.extractfile(mi) as src, open(d, "wb") as dst:
                        shutil.copyfileobj(src, dst, 1 << 20)
                    hechos += 1
    return hechos


def _git(repo, commit, en):
    en = Path(en)
    if not (en / ".git").exists():
        en.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--quiet", repo, str(en)], check=True)
    subprocess.run(["git", "-C", str(en), "checkout", "--quiet", commit], check=True)


def receta(nombre, r, necesarios, R, args, cache):
    t = r["tipo"]
    if t == "url":
        a = _descarga(r["url"], cache)
        if r.get("desempaca"):
            n = _extrae(a, r["desempaca"], local(r["en"], R), necesarios, r.get("interno"))
            print(f"  {n} archivos desempacados")
        else:
            d = local(r["en"], R)
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(a, d)
    elif t == "git":
        _git(r["repo"], r["commit"], local(r["en"], R))
    elif t == "arxiv":
        a = _descarga(f"https://arxiv.org/e-print/{r['id']}", cache)
        time.sleep(3)  # cortesía con arXiv
        d = local(r["en"], R)
        d.parent.mkdir(parents=True, exist_ok=True)
        try:
            with tarfile.open(a) as tf:
                with tf.extractfile(os.path.basename(str(d))) as src, open(d, "wb") as dst:
                    shutil.copyfileobj(src, dst)
        except tarfile.ReadError:  # e-print de un solo archivo, sólo comprimido
            with gzip.open(a) as src, open(d, "wb") as dst:
                shutil.copyfileobj(src, dst)
    elif t == "cobaya":
        cob = ROOT / ".venv" / "bin" / "cobaya-install"
        comp = r["componente"] if isinstance(r["componente"], list) else [r["componente"]]
        subprocess.run([str(cob), *comp, "--packages-path", os.environ["COBAYA_PACKAGES_PATH"]], check=True)
    elif t == "compila":
        en = local(r["en"], R)
        _git(r["repo"], r["commit"], en)
        subprocess.run(r["make"], shell=True, cwd=en, check=True)
    elif t == "paquete":
        fuente = args.paquete or r.get("url")
        if not fuente:
            print("  (sin paquete: pasa --paquete con la ruta o URL de ssee_datos_propios.tar.gz)")
            return
        a = Path(fuente) if Path(fuente).exists() else _descarga(fuente, cache)
        with tarfile.open(a) as tf:
            for mi in tf:
                if not mi.isfile() or mi.name == "SHA256SUMS":
                    continue
                cab, resto = mi.name.split("/", 1)
                d = (Path(os.environ["SSEE_DATOS"]) if cab == "SSEE_data" else ROOT) / resto
                d.parent.mkdir(parents=True, exist_ok=True)
                with tf.extractfile(mi) as src, open(d, "wb") as dst:
                    shutil.copyfileobj(src, dst, 1 << 20)
    else:
        raise ValueError(f"receta desconocida: {t}")


def baja(m, R, args):
    esp = esperados(m, R)
    recetas = dict(m["recetas"])
    for e in m["ficheros"]:  # las de arXiv se arman desde la entrada
        if str(e["receta"]).startswith("arxiv:"):
            recetas[e["receta"]] = {"tipo": "arxiv", "id": e["receta"][6:], "en": e["ruta"]}
    solo = set(args.solo.split(",")) if args.solo else None
    cache = Path(os.environ["SSEE_DATOS"]) / ".descargas"
    for nombre, r in recetas.items():
        if solo and nombre not in solo:
            continue
        necesarios = {str(p) for p, _, rc in esp.values() if rc == nombre}
        if necesarios and all(Path(p).exists() and _sha(p) == s for p, s, rc in esp.values() if rc == nombre):
            print(f"[{nombre}] ya está y coincide")
            continue
        print(f"[{nombre}] {r['tipo']}", flush=True)
        receta(nombre, r, necesarios, R, args, cache)


def verifica(m, R):
    ok, falta, distinto = 0, [], []
    for orig, (p, sha, rc) in sorted(esperados(m, R).items()):
        if not p.exists():
            falta.append((orig, rc))
        elif _sha(p) != sha:
            distinto.append((orig, rc))
        else:
            ok += 1
    software = [e["ruta"] for e in m["ficheros"] if e["clase"] == "S"]
    for s in software:
        estado = "compilado" if local(s, R).exists() else "FALTA (receta hi_class)"
        print(f"software {s}: {estado} — su huella no se compara: depende de la máquina")
    for o, rc in falta:
        print(f"FALTA     {o}   [receta {rc}]")
    for o, rc in distinto:
        print(f"DISTINTO  {o}   [receta {rc}]")
    print(f"\n{ok} archivos idénticos a los del manifiesto · {len(falta)} faltan · {len(distinto)} distintos")
    return 0 if not (falta or distinto) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("modo", choices=["baja", "verifica"])
    ap.add_argument("--paquete", help="ruta o URL de ssee_datos_propios.tar.gz")
    ap.add_argument("--solo", help="recetas separadas por coma")
    args = ap.parse_args()
    R = raices()
    m = json.load(open(MANIFIESTO))
    if args.modo == "baja":
        baja(m, R, args)
    return verifica(m, R)


if __name__ == "__main__":
    sys.exit(main())
