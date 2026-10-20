#!/usr/bin/env python3
"""coteja_transcripciones.py — cada transcripción de cadena se coteja contra su cadena.

POR QUÉ EXISTE (2026-10-16, deuda R75). Las transcripciones de las corridas MCMC
(la consola de cobaya o emcee) no son resultados: los números salen de etapas
selladas que leen las CADENAS. Pero tampoco se pueden «re-correr» para sellarlas:
varias se reanudaron tras el reinicio del 2026-09-19 y duran días. Lo que sí se
puede comprobar es que cada transcripción describe de verdad la cadena que está en
disco, y que esa cadena la lee una etapa sellada. Sin esto, la transcripción es
texto suelto que cualquiera podría editar o que podría hablar de otra corrida.

QUÉ COMPRUEBA, por cada «Sampling complete after N accepted steps» de cobaya:
  1. el prefijo de salida que la transcripción declaró antes de esa línea;
  2. que la suma de filas de prefijo.<k>.txt sea EXACTAMENTE N;
  3. que la transcripción diga «The run has converged!» antes de terminar;
  4. que alguna etapa de dvc.yaml lea esa cadena (la cadena está en la cadena).
(2026-10-20: salieron las dos transcripciones del BOSS de Beutler+2017 y la
cabecera de la conjunta b3, archivadas con su montaje en
archive/codigo/investigacion/boss_beutler17_RETIRADO_2026-10-20/.)

CONTROL (R53): una transcripción sintética con N de más se marca; la misma con el N
correcto pasa. Si el control falla, la salida dice pasa=false.

Salida: results/logs/coteja_transcripciones.json (con acta).
"""
import json
import pathlib
import re
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from procedencia import con_acta  # noqa: E402

# transcripción -> qué es (la lista es explícita: nada entra por patrón)
TRANSCRIPCIONES = [
    "results/logs/b1_full_run.log",
    "results/logs/b1_lcdm_run.log",
    "results/logs/b1_k2_run.log",
    "results/logs/kids_legacy_ssee.log",
    "results/logs/kids_legacy_sseefijo.log",
    "results/logs/kids_legacy_lcdmfijo.log",
    "results/logs/R4_lcdm_resume_20260805.log",
]

_PREF = [re.compile(r"Output to be read-from/written-into folder '([^']+)', with prefix '([^']+)'"),
         re.compile(r"Output prefix: (\S+)")]
_FIN = re.compile(r"Sampling complete after (\d+) accepted steps")


def _prefijo(linea):
    m = _PREF[0].search(linea)
    if m:
        return str(pathlib.Path(m.group(1)) / m.group(2))
    m = _PREF[1].search(linea)
    return m.group(1) if m else None


def filas(prefijo):
    p = pathlib.Path(prefijo)
    archivos = sorted(p.parent.glob(p.name + ".[0-9]*.txt")) or sorted(p.parent.glob(p.name + ".txt"))
    n = sum(sum(1 for l in open(a) if l.strip() and not l.startswith("#")) for a in archivos)
    return n, [str(a) for a in archivos]


def etapas_que_leen(archivos, stages):
    # dvc.yaml escribe las rutas del repo en relativo y las de /mnt en absoluto.
    rel = {str(pathlib.Path(a).resolve()) for a in archivos}
    leen = set()
    for nombre, s in stages.items():
        deps = [d if isinstance(d, str) else list(d)[0] for d in (s.get("deps") or [])]
        deps = {str((ROOT / d).resolve()) if not d.startswith("/") else d for d in deps}
        if rel & deps:
            leen.add(nombre)
    return sorted(leen)


def coteja(texto, contar=filas, stages=None):
    """-> lista de segmentos [{prefijo, N, filas, convergio, pasa, ...}] de una transcripción."""
    stages = stages or {}
    segs, pref, conv = [], None, False
    for linea in texto.splitlines():
        p = _prefijo(linea)
        if p:
            pref, conv = p, False
        if "The run has converged!" in linea:
            conv = True
        m = _FIN.search(linea)
        if m and pref:
            n = int(m.group(1))
            nf, archivos = contar(pref)
            leen = etapas_que_leen(archivos, stages) if stages else []
            segs.append(dict(prefijo=pref, N_declarado=n, filas=nf, convergio=conv,
                             etapas_que_leen=leen,
                             pasa=bool(n == nf and conv and (leen or not stages))))
    return segs


def control():
    with tempfile.TemporaryDirectory() as d:
        pref = pathlib.Path(d) / "x"
        (pathlib.Path(str(pref) + ".1.txt")).write_text("# a b\n1 2\n3 4\n5 6\n")
        cab = f"Output prefix: {pref}\nThe run has converged!\n"
        bien = coteja(cab + "Sampling complete after 3 accepted steps.\n")
        mal = coteja(cab + "Sampling complete after 4 accepted steps.\n")
    return bool(bien and bien[0]["pasa"] and mal and not mal[0]["pasa"])


if __name__ == "__main__":
    stages = yaml.safe_load(open(ROOT / "dvc.yaml"))["stages"]
    res = dict(transcripciones={}, control=control())
    for t in TRANSCRIPCIONES:
        segs = coteja((ROOT / t).read_text(errors="ignore"), stages=stages)
        res["transcripciones"][t] = dict(segmentos=segs)
    # La convergencia se exige por CADENA: b1_full_run vuelve a cargar lcdm_cmb (que
    # convergió en b1_lcdm_run) y por eso ese tramo no repite «converged».
    conv = {s["prefijo"] for v in res["transcripciones"].values() for s in v["segmentos"] if s["convergio"]}
    for v in res["transcripciones"].values():
        for s in v["segmentos"]:
            s["convergio_en_alguna"] = s["prefijo"] in conv
            s["pasa"] = bool(s["N_declarado"] == s["filas"] and s["convergio_en_alguna"] and s["etapas_que_leen"])
        v["pasa"] = bool(v["segmentos"]) and all(s["pasa"] for s in v["segmentos"])
    res["pasa"] = bool(res["control"]
                       and all(v["pasa"] for v in res["transcripciones"].values()))
    for t, v in res["transcripciones"].items():
        print(f"{'PASA' if v['pasa'] else 'FALLA'} {t}: " + "; ".join(
            f"{pathlib.Path(s['prefijo']).name} N={s['N_declarado']} filas={s['filas']} conv={s['convergio']} leen={s['etapas_que_leen']}"
            for s in v["segmentos"]) if v["segmentos"] else f"FALLA {t}: sin «Sampling complete»")
    print("control:", "PASA" if res["control"] else "FALLA")
    out = ROOT / "results" / "logs" / "coteja_transcripciones.json"
    entradas = [ROOT / t for t in TRANSCRIPCIONES]
    json.dump(con_acta(res, __file__, entradas=[str(e) for e in entradas]), open(out, "w"), indent=1)
    sys.exit(0 if res["pasa"] else 1)
