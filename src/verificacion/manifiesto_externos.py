#!/usr/bin/env python3
"""manifiesto_externos.py — huella y origen de cada dependencia de dvc.yaml que vive FUERA del repo.

POR QUÉ EXISTE (2026-10-10)
---------------------------
La auditoría de reproducibilidad (notes/lectura_tercera/REPRO.md, punto 5) contó
~100 rutas absolutas en los deps de dvc.yaml (/mnt/datos/SSEE_data/..., cobaya,
hi_class) sin manifiesto: un tercero no sabía de dónde bajarlas ni si lo bajado
era lo mismo. data/manifiesto_descargas_T2.json cubría sólo las sondas de T2.
Este script lo cubre todo y se puede volver a correr: calcula sha256 y bytes de
cada archivo (o de cada archivo dentro de un directorio dep) y le pega el origen
por prefijo de ruta. El origen por grupo salió de la investigación documentada en
notes/lectura_tercera/MANIFIESTO_EXTERNOS.md.

Clases: A = dato público de terceros (se descarga) · B = producto propio
(se regenera con la etapa/script indicado o se publica aparte) · S = software.

USO
    .venv/bin/python3 src/verificacion/manifiesto_externos.py   # escribe data/manifiesto_externos.json
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SALIDA = ROOT / "data" / "manifiesto_externos.json"

# prefijo de ruta -> (clase, origen, cita)
ORIGENES = [
    ("/mnt/datos/SSEE_data/boss_dr12/", "A", "https://data.sdss.org/sas/dr12/boss/papers/clustering/",
     "Beutler et al. 2017, MNRAS 466, 2242 (arXiv:1607.03149)"),
    ("/mnt/datos/SSEE_data/desi_dr2_official/", "A", "https://doi.org/10.5281/zenodo.16644577",
     "DESI DR2 cadenas oficiales (Abdul-Karim et al. 2025, arXiv:2503.14738)"),
    ("/mnt/datos/SSEE_data/cmb_lensing/spt3g/", "A", "https://github.com/SouthPoleTelescope/spt_candl_data.git (commit efe35b7)",
     "SPT-3G D1 lensing"),
    ("/mnt/datos/SSEE_data/cmb_lensing/", "A", "ver data/manifiesto_descargas_T2.json (grupo cmb_lensing)", ""),
    ("/mnt/datos/SSEE_data/kids1000/", "A", "https://kids.strw.leidenuniv.nl/ (KiDS-1000 cosmic shear data release)",
     "Asgari et al. 2021, A&A 645, A104 (arXiv:2007.15633)"),
    ("/mnt/datos/SSEE_data/kids_legacy/", "A", "https://kids.strw.leidenuniv.nl/DR5/legacy_wl.php",
     "Wright et al. 2025 (arXiv:2503.19441)"),
    ("/mnt/datos/SSEE_data/erosita/efeds/", "A", "CDS/VizieR (Bahar et al. 2022)", "eFEDS clusters V3.2"),
    ("/mnt/datos/SSEE_data/erosita/", "A", "https://erosita.mpe.mpg.de/ (eRASS1 data release)", "Bulbul et al. 2024"),
    ("/mnt/datos/SSEE_data/des_y3/cadenas/", "A", "https://des.ncsa.illinois.edu/releases/y3a2/Y3key-products (cadenas 3x2pt)",
     "DES Collaboration 2022, PRD 105, 023520 (arXiv:2105.13549)"),
    ("/mnt/datos/SSEE_data/des_y3/", "A", "ver data/manifiesto_descargas_T2.json (grupo des_y3)", ""),
    ("/mnt/datos/SSEE_data/sn_ia/", "A", "ver data/manifiesto_descargas_T2.json (grupo sn_ia/union3)", ""),
    ("/mnt/datos/SSEE_data/literatura/", "C", "arXiv (id = nombre de la carpeta)", "sólo lectura de fuentes; no se redistribuye"),
    ("/mnt/datos/SSEE_data/chains_p6/", "B", "producto propio: cadenas MCMC de Paper 6 (src/p06_growth/)", "regenerable; o dataset aparte"),
    ("/mnt/datos/SSEE_data/mcmc/", "B", "producto propio: cadenas MCMC (ver etapa DVC que lo produce)", "regenerable; o dataset aparte"),
    ("/home/mike/cobaya_packages/data/planck_2018/", "A",
     "cobaya-install planck_2018_highl_plik.TTTEEE_lite_native --packages-path $COBAYA_PACKAGES_PATH", "Planck 2018 (PR3)"),
    ("/home/mike/cobaya_packages/data/planck_supp_data_and_covmats/", "A",
     "cobaya-install planck_2018_lensing.native --packages-path $COBAYA_PACKAGES_PATH", "Planck 2018 lensing"),
    ("/mnt/datos/hi_class/", "S", "https://github.com/miguelzuma/hi_class_public.git (commit 0009f51d8; compilar)",
     "binario compilado: se reconstruye, no se compara por sha256"),
]


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _origen(ruta):
    for pre, clase, url, cita in ORIGENES:
        if ruta.startswith(pre):
            return clase, url, cita
    return "?", "SIN ORIGEN", ""


def main():
    etapas = yaml.safe_load(open(ROOT / "dvc.yaml"))["stages"]
    rutas = {}
    for nombre, s in etapas.items():
        for d in s.get("deps", []):
            d = d if isinstance(d, str) else list(d)[0]
            if d.startswith("/"):
                rutas.setdefault(d, []).append(nombre)

    ficheros, sin_origen, faltan = [], [], []
    for ruta in sorted(rutas):
        clase, url, cita = _origen(ruta)
        p = Path(ruta)
        if clase == "?":
            sin_origen.append(ruta)
        if not p.exists():
            faltan.append(ruta)
            continue
        if clase == "S":
            archivos = []
        elif p.is_dir():
            archivos = sorted(x for x in p.rglob("*") if x.is_file())
        else:
            archivos = [p]
        ficheros.append({
            "ruta": ruta, "clase": clase, "origen": url, "cita": cita, "etapas": sorted(rutas[ruta]),
            "archivos": [{"rel": str(a.relative_to(p)) if p.is_dir() else a.name,
                          "bytes": a.stat().st_size, "sha256": _sha(a)} for a in archivos],
        })

    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    acta = {
        "_procedencia": {"script": "src/verificacion/manifiesto_externos.py", "commit": commit,
                         "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                         "fuente_de_origenes": "notes/lectura_tercera/MANIFIESTO_EXTERNOS.md"},
        "resumen": {"rutas": len(rutas), "sin_origen": sin_origen, "no_existen": faltan,
                    "por_clase": {c: sum(1 for f in ficheros if f["clase"] == c) for c in "ABCS?"}},
        "ficheros": ficheros,
    }
    SALIDA.write_text(json.dumps(acta, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps(acta["resumen"], ensure_ascii=False))
    return 1 if sin_origen else 0


if __name__ == "__main__":
    sys.exit(main())
