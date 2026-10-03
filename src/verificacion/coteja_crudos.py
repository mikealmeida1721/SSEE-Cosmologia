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
TABLA2 = RAW / "planck2018_VI" / "tabla2.tex"   # extracto literal de arXiv:1807.06209, Tabla 2
TABLA_CC = RAW / "moresco2022" / "tabla_cc1.tex"   # extracto literal de arXiv:2201.07241, Tabla CC1
FS8 = RAW / "fsigma8_fuentes"   # extractos literales de las 4 fuentes de fsigma8
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


def coteja_prior(csv, tabla):
    """planck2018_prior.csv contra la columna TT,TE,EE+lowE+lensing (la 5a) de la Tabla 2.
    Devuelve (ok, detalle, columna) — la columna es la que reproduce los tres valores."""
    import re
    filas = {}
    for ln in pathlib.Path(tabla).read_text().splitlines():
        if ln.startswith("%") or "\\pm" not in ln:
            continue
        celdas = ln.rstrip("\\cr").split("&")
        filas[celdas[0].strip()] = [c.strip() for c in celdas[1:]]
    clave = {"H0": "H_0\\,[{\\rm km}\\,{\\rm s}^{-1}\\,{\\rm Mpc}^{-1}]",
             "Omega_m": "\\Omega_{\\mathrm{m}}", "Omega_b_h2": "\\Omega_{\\mathrm{b}} h^2"}
    rep = {}
    for ln in pathlib.Path(csv).read_text().splitlines():
        if ln.startswith("#") or ln.startswith("parameter") or not ln.strip():
            continue
        n, m, s = ln.split(",")
        rep[n] = (m, s)
    cols = []
    for j in range(5):
        if all(re.fullmatch(rf"{re.escape(rep[n][0])}\\pm\s*{re.escape(rep[n][1])}", filas[clave[n]][j])
               for n in rep):
            cols.append(j + 1)
    return cols == [5], f"los 3 valores coinciden con la(s) columna(s) {cols} (5 = TT,TE,EE+lowE+lensing)", cols


def coteja_cc(csv, tabla):
    """cosmic_chronometers.csv fila por fila (z, H, sigma, metodo, ref) contra la Tabla CC1."""
    import re
    fuente = [m.groups() for m in (re.match(r"^\s*([0-9.]+)\s*&\s*([0-9.]+)\s*&\s*([0-9.]+)\s*&\s*([FDL])\s*&\s*\\cite\{(\w+)\}", ln)
                                   for ln in pathlib.Path(tabla).read_text().splitlines()) if m]
    repo = [tuple(ln.split(",")) for ln in pathlib.Path(csv).read_text().splitlines()
            if ln and not ln.startswith("#") and not ln.startswith("z,")]
    if len(repo) != len(fuente):
        return False, f"{len(repo)} filas vs {len(fuente)} en la fuente"
    malas = [r for r, f in zip(repo, fuente)
             if [float(x) for x in r[:3]] != [float(x) for x in f[:3]] or tuple(r[3:]) != tuple(f[3:])]
    return not malas, (f"{len(repo)} filas identicas a la Tabla CC1" if not malas else f"difieren: {malas[:3]}")


def coteja_fs8(csv, d):
    """Cada fila de fsigma8_rsd.csv contra el extracto de SU referencia.
    Howlett+2015 da 0.49 (+0.15/-0.14): el csv usa la media simetrizada (0.15+0.14)/2."""
    import re
    ext = {k: (pathlib.Path(d) / f).read_text() for k, f in
           (("Beutler2012", "beutler2012.tex"), ("Howlett2015", "howlett2015.tex"),
            ("Alam2017", "alam2017.tex"), ("Hou2021", "hou2021.tex"))}
    malas = []
    for ln in pathlib.Path(csv).read_text().splitlines():
        if not ln or ln.startswith("#") or ln.startswith("z_eff"):
            continue
        z, v, e, _, ref = ln.split(",")
        t = ext.get(ref, "")
        if ref == "Howlett2015":
            m = re.search(r"f\\sigma_\{8\}=([0-9.]+)\^\{\+([0-9.]+)\}_\{-([0-9.]+)\}", t)
            ok = bool(m) and float(m.group(1)) == float(v) and abs((float(m.group(2)) + float(m.group(3))) / 2 - float(e)) < 1e-12
        elif ref == "Alam2017":
            m = re.search(rf"f\\sigma_8\({float(z):.2f}\)\$\s*&\s*([0-9.]+)\s*&\s*([0-9.]+)", t)
            ok = bool(m) and float(m.group(1)) == float(v) and float(m.group(2)) == float(e)
        else:
            ok = re.search(rf"{re.escape(v)}\s*\\pm\s*{re.escape(e)}", t) is not None and \
                 (ref != "Beutler2012" or z in t) and (ref != "Hou2021" or z.rstrip("0") in t)
        if not ok:
            malas.append(ln)
    return not malas, ("6 filas coinciden con su referencia" if not malas else f"difieren: {malas}")


res = {}
for nombre, (oficial, sha) in OFICIAL.items():
    res[nombre] = dict(fuente=IRSA + oficial, sha256_oficial=sha, sha256_repo=_sha(RAW / nombre),
                       coincide=coteja_espectro(RAW / nombre, sha),
                       entrega="Planck 2018 (PR3, R3.01) — NO PR4")
ok_l, msg_l = coteja_lensing(RAW / "planck2018_lensing.txt", LENS_FUENTE)
res["planck2018_lensing.txt"] = dict(fuente=str(LENS_FUENTE), coincide=ok_l, detalle=msg_l,
                                     entrega="Planck 2018 lensing (PR3), agr2 MV bandpowers")

ok_p, msg_p, cols_p = coteja_prior(RAW / "planck2018_prior.csv", TABLA2)
res["planck2018_prior.csv"] = dict(fuente="arXiv:1807.06209 Tabla 2 (extracto data/raw/planck2018_VI/tabla2.tex)",
                                   coincide=ok_p, detalle=msg_p, entrega="Planck 2018 VI, TT,TE,EE+lowE+lensing",
                                   no_cotejado="rho(H0,Om)=-0.85 de la cabecera: no esta en la Tabla 2 (sale de cadenas)")

ok_c, msg_c = coteja_cc(RAW / "cosmic_chronometers.csv", TABLA_CC)
res["cosmic_chronometers.csv"] = dict(fuente="arXiv:2201.07241 Tabla CC1 (extracto data/raw/moresco2022/tabla_cc1.tex)",
                                      coincide=ok_c, detalle=msg_c, entrega="Moresco+2022, 32 puntos, solo diagonal")

ok_f, msg_f = coteja_fs8(RAW / "fsigma8_rsd.csv", FS8)
res["fsigma8_rsd.csv"] = dict(fuente="Beutler+2012, Howlett+2015, Alam+2017, Hou+2021 (extractos data/raw/fsigma8_fuentes/)",
                              coincide=ok_f, detalle=msg_f, entrega="6 puntos; los 3 de BOSS estan correlacionados (covarianza en Alam+2017)")

# CONTROL (R53): un digito cambiado tiene que hacer fallar a los dos comparadores
with tempfile.TemporaryDirectory() as d:
    t = pathlib.Path(d) / "tt.txt"
    t.write_text((RAW / "planck2018_TT.txt").read_text().replace("2.25895000e+02", "2.25895001e+02", 1))
    l = pathlib.Path(d) / "l.txt"
    l.write_text((RAW / "planck2018_lensing.txt").read_text().replace("1.33520e-07", "1.33521e-07", 1))
    cc = pathlib.Path(d) / "cc.csv"
    cc.write_text((RAW / "cosmic_chronometers.csv").read_text().replace("0.48,97,62", "0.48,97,60"))
    fs = pathlib.Path(d) / "fs.csv"
    fs.write_text((RAW / "fsigma8_rsd.csv").read_text().replace("0.510,0.458,0.038", "0.510,0.458,0.039"))
    control = dict(fs8_alterado_falla=not coteja_fs8(fs, FS8)[0],
                   cc_alterado_falla=not coteja_cc(cc, TABLA_CC)[0],
                   espectro_alterado_falla=not coteja_espectro(t, OFICIAL["planck2018_TT.txt"][1]),
                   lensing_alterado_falla=not coteja_lensing(l, LENS_FUENTE)[0])
control["pasa"] = all(control.values())

out = dict(archivos=res, todos_coinciden=all(v["coincide"] for v in res.values()), control=control)
json.dump(con_acta(out, __file__, entradas=[RAW / n for n in res] + [TABLA2, TABLA_CC, LENS_FUENTE] + sorted(FS8.glob('*.tex'))),
          open(ROOT / "results" / "logs" / "coteja_crudos.json", "w"), indent=1, ensure_ascii=False)
for n, v in res.items():
    print(f"  {n:24s} {'COINCIDE' if v['coincide'] else 'NO COINCIDE'}  ({v['entrega']})")
print(f"  control (un digito cambiado falla): {'PASA' if control['pasa'] else 'NO PASA'}")
sys.exit(0 if out["todos_coinciden"] and control["pasa"] else 1)
