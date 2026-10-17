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
(va en el paquete de datos de SSEE en Zenodo) · C = literatura (e-print de arXiv
en versión fija, o extracto citado que va en el paquete) · S = software (se compila).
Cada entrada lleva su RECETA: lo que ejecuta src/verificacion/baja_externos.py.

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

D = "/mnt/datos/SSEE_data"
GH = "https://raw.githubusercontent.com"

# Cómo se obtiene cada cosa (2026-10-17). Lo ejecuta src/verificacion/baja_externos.py;
# «en» es la ruta ORIGINAL (la que nombran dvc.yaml y las actas) y el script la traduce
# a las carpetas del verificador. Cada receta se probó: la huella sha256 de lo bajado
# coincide con la de los archivos con que se corrió.
#   url     archivo suelto o paquete (tar/zip) en la web del dueño del dato
#   git     repositorio clonado en un commit fijo
#   arxiv   fuente del e-print, versión fija
#   cobaya  `cobaya-install <componente>` (Planck Legacy Archive)
#   compila software: clonar en un commit y compilar (la huella del binario no viaja)
#   paquete productos propios (cadenas MCMC) y extractos de literatura: el paquete de
#           datos de SSEE en Zenodo, que arma src/verificacion/empaqueta_datos_propios.py
RECETAS = {
    "boss_dr12": {"tipo": "url", "desempaca": "tar", "en": f"{D}/boss_dr12",
                  "url": "https://data.sdss.org/sas/dr12/boss/papers/clustering/Beutler_etal_DR12COMBINED_fullshape_powspec.tar.gz"},
    "kids1000": {"tipo": "url", "desempaca": "tar", "en": f"{D}/kids1000",
                 "url": "https://kids.strw.leidenuniv.nl/DR4/data_files/KiDS1000_cosmic_shear_data_release.tgz"},
    "kcap": {"tipo": "git", "repo": "https://github.com/KiDS-WL/kcap.git",
             "commit": "36b40c55394caf26021408e71ff74538bfa3d51e", "en": f"{D}/kids1000/kcap"},
    "kids_legacy": {"tipo": "url", "desempaca": "tar", "en": f"{D}/kids_legacy",
                    "url": "https://kids.strw.leidenuniv.nl/sci_data/KiDS_Legacy_cosmic_shear_data_release.tar.gz"},
    "desi_dr2": {"tipo": "url", "desempaca": "zip", "interno": "dr2-bao-zenodo/cosmology_chains.zip",
                 "en": f"{D}/desi_dr2_official",
                 "url": "https://zenodo.org/api/records/16644577/files/dr2-bao-zenodo.zip/content"},
    "spt3g": {"tipo": "git", "repo": "https://github.com/SouthPoleTelescope/spt_candl_data.git",
              "commit": "efe35b7bfd815a115d5123e210a6849a4175bc81", "en": f"{D}/cmb_lensing/spt3g"},
    "des_y3_cadena": {"tipo": "url", "en": f"{D}/des_y3/cadenas/chain_3x2pt_lcdm_SR_maglim.txt",
                      "url": "https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/chains/chain_3x2pt_lcdm_SR_maglim.txt"},
    "erass1_primary": {"tipo": "url", "desempaca": "tar", "en": f"{D}/erosita/erass1",
                       "url": "https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/Catalogues_dr1/BulbulE_DR1/erass1cl_primary_v3.2.fits.tgz"},
    "erass1_cosmo": {"tipo": "url", "desempaca": "tar", "en": f"{D}/erosita/erass1",
                     "url": "https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/Catalogues_dr1/BulbulE_DR1/erass1cl_cosmology_v1.1.fits.tgz"},
    "efeds": {"tipo": "url", "en": f"{D}/erosita/efeds/eFEDS_clusters_V3.2.fits.gz",
              "url": "https://erosita.mpe.mpg.de/edr/eROSITAObservations/Catalogues/liuA/eFEDS_clusters_V3.2.fits.gz"},
    "union3_release": {"tipo": "url", "en": f"{D}/sn_ia/union3/mu_mat_union3_cosmo=2_mu.fits",
                       "url": f"{GH}/rubind/union3_release/f5c387349b68f3535fdabf0fbc4f45cd407f9084/mu_mat_union3_cosmo=2_mu.fits"},
    "union3_pipeline": {"tipo": "git", "repo": "https://github.com/rubind/union3.git",
                        "commit": "850dab25cead339ba6c5355abca96529697b59a2", "en": f"{D}/sn_ia/union3/pipeline"},
    "pantheon_dat": {"tipo": "url", "en": f"{D}/sn_ia/pantheon_plus/Pantheon+SH0ES.dat",
                     "url": f"{GH}/PantheonPlusSH0ES/DataRelease/c447f0fea703fcd0fff57de5000947b5ca81286b/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat"},
    "pantheon_cov": {"tipo": "url", "en": f"{D}/sn_ia/pantheon_plus/Pantheon+SH0ES_STAT+SYS.cov",
                     "url": f"{GH}/PantheonPlusSH0ES/DataRelease/c447f0fea703fcd0fff57de5000947b5ca81286b/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES_STAT+SYS.cov"},
    "dessn_hd": {"tipo": "url", "en": f"{D}/sn_ia/des_sn5yr/DES-Dovekie_HD.csv",
                 "url": f"{GH}/des-science/DES-SN5YR/c9a4fcafc4cbd19bd750dee47fc76194a45c181f/4_DISTANCES_COVMAT/DES-Dovekie_HD.csv"},
    "dessn_cov": {"tipo": "url", "en": f"{D}/sn_ia/des_sn5yr/STAT+SYS.npz",
                  "url": f"{GH}/des-science/DES-SN5YR/c9a4fcafc4cbd19bd750dee47fc76194a45c181f/4_DISTANCES_COVMAT/STAT+SYS.npz"},
    # la versión clik (la que leen cmb_eval y b1) y, de una vez, todo lo que los scripts piden a
    # cobaya, para que el verificador también pueda RE-CORRER (no sólo cotejar huellas)
    "planck_plik_lite": {"tipo": "cobaya", "componente": ["planck_2018_highl_plik.TTTEEE_lite",
                         "planck_2018_highl_plik.TTTEEE", "planck_2018_lowl.TT", "planck_2018_lowl.EE",
                         "planck_2018_highl_plik.TTTEEE_lite_native"]},
    "planck_lensing": {"tipo": "cobaya", "componente": "planck_2018_lensing.native"},
    "hi_class": {"tipo": "compila", "repo": "https://github.com/miguelzuma/hi_class_public.git",
                 "commit": "0009f51d89e6465c79e570b496c66fc90058fa77",
                 "make": "make class && /home/mike/Proyectos/SSEE/.venv/bin/pip install --no-deps .",
                 "en": "/mnt/datos/hi_class"},
    "paquete_ssee": {"tipo": "paquete", "url": None,
                     "nota": "paquete de datos de SSEE en Zenodo; la URL se fija al publicarlo"},
}

# Entornos de software aparte del .venv del repo, que sólo hacen falta para RE-CORRER
# las etapas que los usan (no para verificar sus salidas). Especificación exacta en git.
ENTORNOS = {
    "cosmosis_des_y3": {
        "etapas": ["des_y3_tatt", "des_y3_nla", "sello_des_y3_calibrador"],
        "en": f"{D}/des_y3/entorno",
        "pasos": [
            "micromamba create -p <en>/cosmosis --file data/entornos/cosmosis_des_y3.explicit.txt",
            "git clone https://github.com/joezuntz/cosmosis-standard-library <en>/csl && git -C <en>/csl checkout 9e3dd611fc20bf39489d43bf4afeb503d26b4e79",
            "cd <en>/csl && source cosmosis-configure && make",
        ],
        "nota": "CosmoSIS 3.25.2 (conda-forge, 231 paquetes con md5); src/p11_sondas/des_y3_calibra.py",
    },
    "venv_erosita": {
        "etapas": ["sello_erosita_conteos_erass1", "sello_erosita_conteos_efeds", "sello_erosita_cr_v3"],
        "en": f"{D}/erosita/venv",
        "pasos": ["python3.12 -m venv <en> && <en>/bin/pip install -r data/entornos/erosita_venv.txt"],
        "nota": "pyccl 3.3.6 + astropy; las etapas lo llaman por su ruta",
    },
}

# e-prints de arXiv que las etapas leen (para cotejar transcripciones), versión fija.
ARXIV = {
    "cmb_lensing/papers/2304.05202/main.tex": "2304.05202v3",
    "cmb_lensing/papers/2608.31136/sec8_summary.tex": "2608.31136v1",
    "erosita/paper_2602.20483/AA_final.tex": "2602.20483v2",
    "erosita/paper_ghirardini2024/48852corr.tex": "2402.08458v2",
    "literatura/1807.06209/ms.tex": "1807.06209v4",
    "literatura/h0_metodos/1710.05835/main.tex": "1710.05835v1",
    "literatura/h0_metodos/2001.09213/main.tex": "2001.09213v2",
    "literatura/h0_metodos/2101.02221/main.tex": "2101.02221v2",
    "literatura/h0_metodos/2112.04510/shoes6.tex": "2112.04510v3",
    "literatura/h0_metodos/2408.06153/Ho2024.tex": "2408.06153v3",
    "literatura/h0_metodos/2408.11770/main.tex": "2408.11770v2",
    "literatura/h0_metodos/2506.03023/main.tex": "2506.03023v4",
    "sn_ia/papers/2202.04077/main.tex": "2202.04077v2",
}

# prefijo de ruta -> (clase, origen, cita, receta). Gana el prefijo MÁS LARGO.
ORIGENES = [
    (f"{D}/boss_dr12/", "A", "https://data.sdss.org/sas/dr12/boss/papers/clustering/",
     "Beutler et al. 2017, MNRAS 466, 2242 (arXiv:1607.03149)", "boss_dr12"),
    (f"{D}/desi_dr2_official/", "A", "https://doi.org/10.5281/zenodo.16644577",
     "DESI DR2 cadenas oficiales (Abdul-Karim et al. 2025, arXiv:2503.14738)", "desi_dr2"),
    (f"{D}/cmb_lensing/spt3g/", "A", "https://github.com/SouthPoleTelescope/spt_candl_data.git (commit efe35b7)",
     "SPT-3G D1 lensing", "spt3g"),
    (f"{D}/cmb_lensing/act_dr6_calibrador/", "B", "producto propio: cadenas ΛCDM de src/p11_sondas/act_dr6_calibra.py",
     "calibrador: reproduce el ΛCDM publicado por ACT antes de meter SSEE", "paquete_ssee"),
    (f"{D}/cmb_lensing/spt3g_calibrador/", "B", "producto propio: cadenas ΛCDM de src/p11_sondas/spt3g_calibra.py",
     "calibrador: reproduce el ΛCDM publicado por SPT antes de meter SSEE", "paquete_ssee"),
    (f"{D}/kids1000/kcap/", "A", "https://github.com/KiDS-WL/kcap.git (commit 36b40c5)",
     "Asgari et al. 2021, A&A 645, A104 (arXiv:2007.15633)", "kcap"),
    (f"{D}/kids1000/", "A", "https://kids.strw.leidenuniv.nl/DR4/ (KiDS-1000 cosmic shear data release)",
     "Asgari et al. 2021, A&A 645, A104 (arXiv:2007.15633)", "kids1000"),
    (f"{D}/kids_legacy/", "A", "https://kids.strw.leidenuniv.nl/DR5/legacy_wl.php",
     "Wright et al. 2025 (arXiv:2503.19441)", "kids_legacy"),
    (f"{D}/erosita/efeds/eFEDS_clusters_V3.2.fits.gz", "A", "eROSITA EDR (Liu et al. 2022)", "eFEDS clusters V3.2", "efeds"),
    (f"{D}/erosita/erass1/erass1cl_primary", "A", "https://erosita.mpe.mpg.de/dr1/ (eRASS1)", "Bulbul et al. 2024", "erass1_primary"),
    (f"{D}/erosita/erass1/erass1cl_cosmology", "A", "https://erosita.mpe.mpg.de/dr1/ (eRASS1)", "Bulbul et al. 2024", "erass1_cosmo"),
    (f"{D}/erosita/", "C", "extracto de literatura (resumen de arXiv o ficha pública del catálogo)",
     "texto citado; va en el paquete de SSEE", "paquete_ssee"),
    (f"{D}/des_y3/calibrador/", "B", "producto propio: mejor punto de nuisances de DES (des_y3_en_el_clavo.py nuevo/continua)",
     "la minimización corre fuera de DVC (días de CPU); la etapa evalúa este punto", "paquete_ssee"),
    (f"{D}/des_y3/cadenas/", "A", "https://des.ncsa.illinois.edu/releases/y3a2/Y3key-products (cadenas 3x2pt)",
     "DES Collaboration 2022, PRD 105, 023520 (arXiv:2105.13549)", "des_y3_cadena"),
    (f"{D}/sn_ia/union3/runs/", "B", "producto propio: reproducción de Union3.1 (src/p11_sondas/union3_repro_compara.py)",
     "se compara con el release publicado", "paquete_ssee"),
    (f"{D}/sn_ia/union3/pipeline/", "A", "https://github.com/rubind/union3.git (commit 850dab2)", "Rubin et al. 2023", "union3_pipeline"),
    (f"{D}/sn_ia/union3/", "A", "https://github.com/rubind/union3_release", "Rubin et al. 2023 (arXiv:2311.12098)", "union3_release"),
    (f"{D}/sn_ia/pantheon_plus/Pantheon+SH0ES.dat", "A", "https://github.com/PantheonPlusSH0ES/DataRelease",
     "Scolnic et al. 2022 (arXiv:2112.03863)", "pantheon_dat"),
    (f"{D}/sn_ia/pantheon_plus/Pantheon+SH0ES_STAT+SYS.cov", "A", "https://github.com/PantheonPlusSH0ES/DataRelease",
     "Brout et al. 2022 (arXiv:2202.04077)", "pantheon_cov"),
    (f"{D}/sn_ia/des_sn5yr/DES-Dovekie_HD.csv", "A", "https://github.com/des-science/DES-SN5YR", "DES-SN5YR (Dovekie)", "dessn_hd"),
    (f"{D}/sn_ia/des_sn5yr/STAT+SYS.npz", "A", "https://github.com/des-science/DES-SN5YR", "DES-SN5YR (Dovekie)", "dessn_cov"),
    (f"{D}/chains_p6/", "B", "producto propio: cadenas MCMC de Paper 6 (src/p06_growth/)", "paquete de datos de SSEE", "paquete_ssee"),
    (f"{D}/mcmc/", "B", "producto propio: cadenas MCMC (ver etapa DVC que lo produce)", "paquete de datos de SSEE", "paquete_ssee"),
    ("/home/mike/cobaya_packages/data/planck_2018/", "A",
     "cobaya-install planck_2018_highl_plik.TTTEEE_lite_native --packages-path $COBAYA_PACKAGES_PATH", "Planck 2018 (PR3)",
     "planck_plik_lite"),
    ("/home/mike/cobaya_packages/data/planck_supp_data_and_covmats/", "A",
     "cobaya-install planck_2018_lensing.native --packages-path $COBAYA_PACKAGES_PATH", "Planck 2018 lensing", "planck_lensing"),
    ("/mnt/datos/hi_class/", "S", "https://github.com/miguelzuma/hi_class_public.git (commit 0009f51d8; compilar)",
     "binario compilado: se reconstruye, no se compara por sha256", "hi_class"),
    # rutas del repo que git no lleva (pesadas o de otro repositorio)
    ("results/chains/", "B", "producto propio: cadenas CMB de B1 (src/p03_cmb/)", "paquete de datos de SSEE", "paquete_ssee"),
    ("zenodo_dictionary/", "B", "diccionario de constantes (repo aparte, concept DOI 10.5281/zenodo.20684908)",
     "la copia exacta con que corrió la etapa va en el paquete de SSEE", "paquete_ssee"),
]


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _origen(ruta):
    rel = ruta[len(D) + 1:] if ruta.startswith(D + "/") else None
    if rel in ARXIV:
        v = ARXIV[rel]
        return "C", f"https://arxiv.org/abs/{v}", "fuente del e-print (se coteja la transcripción)", f"arxiv:{v}"
    for pre, clase, url, cita, receta in sorted(ORIGENES, key=lambda o: -len(o[0])):
        if ruta.startswith(pre):
            return clase, url, cita, receta
    return "?", "SIN ORIGEN", "", None


def main():
    etapas = yaml.safe_load(open(ROOT / "dvc.yaml"))["stages"]
    rutas = {}
    for nombre, s in etapas.items():
        for d in s.get("deps", []):
            d = d if isinstance(d, str) else list(d)[0]
            if d.startswith("/"):
                rutas.setdefault(d, []).append(nombre)
    # deps relativas que git NO lleva y que ninguna etapa produce (cadenas pesadas,
    # el diccionario de otro repo): también tienen que llegarle al verificador
    salidas = {o if isinstance(o, str) else list(o)[0] for s in etapas.values() for o in s.get("outs", [])}
    en_git = set(subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n"))
    for nombre, s in etapas.items():
        for d in s.get("deps", []):
            d = d if isinstance(d, str) else list(d)[0]
            if d.startswith("/") or d in salidas or d in en_git or any(g.startswith(d.rstrip("/") + "/") for g in en_git):
                continue
            rutas.setdefault(d, []).append(nombre)

    ficheros, sin_origen, faltan = [], [], []
    for ruta in sorted(rutas):
        clase, url, cita, receta = _origen(ruta)
        p = Path(ruta) if ruta.startswith("/") else ROOT / ruta
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
            "ruta": ruta, "clase": clase, "origen": url, "cita": cita, "receta": receta,
            "etapas": sorted(rutas[ruta]),
            "archivos": [{"rel": str(a.relative_to(p)) if p.is_dir() else a.name,
                          "bytes": a.stat().st_size, "sha256": _sha(a)} for a in archivos],
        })

    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    acta = {
        "_procedencia": {"script": "src/verificacion/manifiesto_externos.py", "commit": commit,
                         "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                         "fuente_de_origenes": "notes/lectura_tercera/MANIFIESTO_EXTERNOS.md"},
        "resumen": {"rutas": len(rutas), "sin_origen": sin_origen, "no_existen": faltan,
                    "por_clase": {c: sum(1 for f in ficheros if f["clase"] == c) for c in "ABCS?"},
                    "por_receta": {r: sum(1 for f in ficheros if f["receta"] == r)
                                   for r in sorted({f["receta"] for f in ficheros if f["receta"]})}},
        "recetas": RECETAS,
        "entornos": ENTORNOS,
        "ficheros": ficheros,
    }
    SALIDA.write_text(json.dumps(acta, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps(acta["resumen"], ensure_ascii=False))
    sin_receta = [f["ruta"] for f in ficheros if f["receta"] not in RECETAS and not str(f["receta"]).startswith("arxiv:")]
    for r in sin_receta:
        print("SIN RECETA:", r)
    return 1 if (sin_origen or sin_receta or faltan) else 0


if __name__ == "__main__":
    sys.exit(main())
