#!/usr/bin/env python3
"""coteja_crudos.py — R76: los datos crudos de Planck, cotejados contra su fuente (2026-10-02).

POR QUE. data/raw/FUENTES.yaml declaraba «Planck PR4 Legacy Archive» para los
espectros TT/TE/EE. Al bajar la fuente, los tres archivos resultaron ser BYTE A
BYTE los COM_PowerSpect_CMB-*-full_R3.01.txt de Planck 2018 (PR3), no PR4
(NPIPE). La etiqueta estaba mal en 13 documentos (78 menciones) y la cita
apuntaba al artículo de NPIPE. Declarar no es cotejar: esto es el cotejo.

QUE COMPARA.
  - TT/TE/EE: sha256 del archivo del repo contra el sha256 del archivo oficial,
    bajado de IRSA el 2026-10-02 (URL abajo). Si alguien edita un número del
    repo, el sha cambia y falla.
  - lensing: columna por columna (L_eff, C_L^phiphi, error) contra el archivo
    oficial de la distribución de Cobaya (planck_supp_data_and_covmats), que
    es la fuente que el propio archivo declara en su cabecera.
CONTROL (R53): el mismo comparador, aplicado a una copia con un solo dígito
cambiado, tiene que fallar.

    .venv/bin/python3 src/verificacion/coteja_crudos.py
Salida: results/logs/coteja_crudos.json (con acta).
"""
import hashlib
import json
import pathlib
import sys
import tempfile

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from procedencia import con_acta  # noqa: E402

RAW = ROOT / "data" / "raw"
IRSA = "https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/cosmoparams/"
# ORIGEN-VALOR: los tres sha256 son los de los archivos oficiales tal como los sirvió IRSA el
# 2026-10-02 (curl de IRSA + sha256sum; copia en /mnt/datos/SSEE_data/fuentes_crudas/).
OFICIAL = {
    "planck2018_TT.txt": ("COM_PowerSpect_CMB-TT-full_R3.01.txt",
                          "ccf3113604020536f6f13ccf51680a7316ad0f32da558eee7f625e613bdd5522"),
    "planck2018_TE.txt": ("COM_PowerSpect_CMB-TE-full_R3.01.txt",
                          "8b2c97d8865ebfdfb2b23c3e6883a39820734b804ba6e353533657b3a2f71425"),
    "planck2018_EE.txt": ("COM_PowerSpect_CMB-EE-full_R3.01.txt",
                          "c865c56fe215e17e45eeed1069ddcd7d13365735f439fd63cc9c9325db97d67f"),
}
LENS_FUENTE = pathlib.Path("/home/mike/cobaya_packages/data/planck_supp_data_and_covmats/lensing/2018/"
                           "smicadx12_Dec5_ftl_mv2_ndclpp_p_teb_agr2_bandpowers.dat")


def _sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def coteja_espectro(ruta, sha_oficial):
    return _sha(ruta) == sha_oficial


def coteja_lensing(ruta, fuente):
    """El archivo del repo (L_eff, PP, err+, err-) contra la fuente (bin, Lmin, Lmax, L_av, PP, Error, Ahat)."""
    a = np.loadtxt(ruta)
    b = np.loadtxt(fuente)
    if a.shape[0] != b.shape[0]:
        return False, f"filas {a.shape[0]} vs {b.shape[0]}"
    ok = (np.array_equal(a[:, 0], b[:, 3]) and np.array_equal(a[:, 1], b[:, 4])
          and np.array_equal(a[:, 2], b[:, 5]) and np.array_equal(a[:, 3], b[:, 5]))
    return bool(ok), f"{a.shape[0]} bandas, L_eff/PP/error identicos" if ok else "difieren"


res = {}
for nombre, (oficial, sha) in OFICIAL.items():
    res[nombre] = dict(fuente=IRSA + oficial, sha256_oficial=sha, sha256_repo=_sha(RAW / nombre),
                       coincide=coteja_espectro(RAW / nombre, sha),
                       entrega="Planck 2018 (PR3, R3.01) — NO PR4")
ok_l, msg_l = coteja_lensing(RAW / "planck2018_lensing.txt", LENS_FUENTE)
res["planck2018_lensing.txt"] = dict(fuente=str(LENS_FUENTE), coincide=ok_l, detalle=msg_l,
                                     entrega="Planck 2018 lensing (PR3), agr2 MV bandpowers")

# CONTROL (R53): un digito cambiado tiene que hacer fallar a los dos comparadores
with tempfile.TemporaryDirectory() as d:
    t = pathlib.Path(d) / "tt.txt"
    t.write_text((RAW / "planck2018_TT.txt").read_text().replace("2.25895000e+02", "2.25895001e+02", 1))
    l = pathlib.Path(d) / "l.txt"
    l.write_text((RAW / "planck2018_lensing.txt").read_text().replace("1.33520e-07", "1.33521e-07", 1))
    control = dict(espectro_alterado_falla=not coteja_espectro(t, OFICIAL["planck2018_TT.txt"][1]),
                   lensing_alterado_falla=not coteja_lensing(l, LENS_FUENTE)[0])
control["pasa"] = all(control.values())

out = dict(archivos=res, todos_coinciden=all(v["coincide"] for v in res.values()), control=control)
json.dump(con_acta(out, __file__, entradas=[RAW / n for n in res] + [LENS_FUENTE]),
          open(ROOT / "results" / "logs" / "coteja_crudos.json", "w"), indent=1, ensure_ascii=False)
for n, v in res.items():
    print(f"  {n:24s} {'COINCIDE' if v['coincide'] else 'NO COINCIDE'}  ({v['entrega']})")
print(f"  control (un digito cambiado falla): {'PASA' if control['pasa'] else 'NO PASA'}")
sys.exit(0 if out["todos_coinciden"] and control["pasa"] else 1)
