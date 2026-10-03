#!/usr/bin/env python3
"""recorre_logs.py — ¿el script de HOY reproduce el log que dejó? (2026-10-03)

POR QUE. R75 cuenta 156 logs fuera de la cadena DVC: existen, los escribió un
script, pero nada comprueba que el script de hoy los siga dando. Mike: «corramos
con lo que tenemos y veamos si cuadran». Este script NO sella nada ni cambia el
repositorio: corre cada script, compara número a número su salida con el log
guardado, y deja el árbol como estaba. Sellar (etapa DVC + acta) es el paso
siguiente, y sólo para los que cuadran.

COMO.
  - Lista: el TSV que se le pasa (log, script, …), sólo los marcados «ligero».
  - Si el script nombra su log, el script lo escribe; si no, se captura su salida
    estándar como log nuevo.
  - Comparación: JSON por ruta de claves; texto línea a línea. Se ignoran fechas,
    horas, PIDs, duraciones, rutas y el acta. Cuadra si todos los números
    coinciden a la precisión con que están escritos (o a 1e-6 relativo en JSON).
  - Después de cada corrida se restaura todo archivo versionado que el script
    tocó (git checkout) y se borra lo que creó; los archivos que ya estaban
    modificados antes de empezar (p. ej. la cola de la conjunta) no se tocan.

CONTROL (R53). Antes de correr nada: una copia idéntica de un log tiene que
CUADRAR y la misma copia con un dígito cambiado tiene que NO cuadrar.

    python3 src/verificacion/recorre_logs.py lista.tsv salida.json
(las salidas que no cuadran quedan junto a salida.json, en recorre_salidas_nuevas/)
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
NUM = re.compile(r"[-+]?\d+\.\d+(?:[eE][-+]?\d+)?|[-+]?\d+[eE][-+]?\d+")
# Ruido que se QUITA de la línea (el resto de la línea se compara):
QUITA = re.compile(r"^\[\s*\d+(\.\d+)?m\]|\d{4}-\d{2}-\d{2}|\d{1,2}:\d{2}(:\d{2})?|"
                   r"\d+(\.\d+)?\s*(s|seg|segundos|min|h|it/s)\b")
# Líneas que se descartan enteras (no llevan resultados):
DESCARTA = re.compile(r"ACTA-PROCEDENCIA|PID|elapsed|tiempo|/home/|/mnt/|/tmp/|UserWarning|warnings\.warn", re.I)
PROTEGE = ("results/logs/lcdm_conjunta", "results/logs/vigilante_", "results/logs/cola_", "sandbox_unificado")
CLAVES_RUIDO = re.compile(r"fecha|_procedencia|tiempo|elapsed|duracion|host|pid", re.I)


def _git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout


def _estado():
    """{ruta: estado} de lo modificado o nuevo en el árbol."""
    out = {}
    for ln in _git("status", "--porcelain", "--untracked-files=all").splitlines():
        out[ln[3:].strip()] = ln[:2]
    return out


def _nums_texto(t):
    filas = []
    for ln in t.splitlines():
        if DESCARTA.search(ln):
            continue
        ns = NUM.findall(QUITA.sub(" ", ln))
        if ns:
            filas.append(ns)
    return filas


def _plano(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if CLAVES_RUIDO.search(str(k)):
                continue
            yield from _plano(v, f"{pre}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _plano(v, f"{pre}[{i}]")
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        yield pre, float(o)


def _iguales_texto(a, b):
    """a, b: cadenas tal como se escribieron. Iguales a la precisión del menos preciso."""
    x, y = float(a), float(b)
    if x == y:
        return True
    dec = min(len(a.split("e")[0].split("E")[0].split(".")[-1]) if "." in a else 0,
              len(b.split("e")[0].split("E")[0].split(".")[-1]) if "." in b else 0)
    esc = 10 ** int(f"{abs(x):e}".split("e")[1]) if ("e" in a.lower() or "e" in b.lower()) and x else 1
    return abs(x - y) <= 0.5 * 10 ** -dec * esc + 1e-12


def compara(viejo, nuevo):
    """Devuelve (cuadra, detalle)."""
    if viejo.suffix == ".json":
        try:
            A = dict(_plano(json.loads(viejo.read_text())))
            B = dict(_plano(json.loads(nuevo.read_text())))
        except Exception as e:
            return False, f"JSON ilegible: {e}"
        faltan = sorted(set(A) - set(B))
        malos = [(k, A[k], B[k]) for k in A if k in B
                 and not (A[k] == B[k] or abs(A[k] - B[k]) <= 1e-6 * max(abs(A[k]), abs(B[k])))]
        if faltan or malos:
            return False, {"claves_que_faltan": faltan[:5], "n_faltan": len(faltan),
                           "distintos": [f"{k}: {a!r} -> {b!r}" for k, a, b in malos[:8]], "n_distintos": len(malos)}
        return True, {"numeros_comparados": len(A)}
    A = _nums_texto(viejo.read_text(errors="ignore"))
    B = _nums_texto(nuevo.read_text(errors="ignore"))
    if len(A) != len(B):
        return False, {"filas_con_numeros": [len(A), len(B)]}
    malos = []
    for i, (fa, fb) in enumerate(zip(A, B)):
        if len(fa) != len(fb) or not all(_iguales_texto(a, b) for a, b in zip(fa, fb)):
            malos.append(f"fila {i}: {fa[:6]} -> {fb[:6]}")
    if malos:
        return False, {"n_distintos": len(malos), "distintos": malos[:8]}
    return True, {"numeros_comparados": sum(len(f) for f in A)}


def control():
    """R53: idéntico cuadra, un dígito cambiado no."""
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        # ORIGEN-VALOR: 12.3456 — dato sintetico del control del comparador (no es un resultado)
        # ORIGEN-VALOR: 0.4321 — idem, segundo numero sintetico del control
        (d / "a.log").write_text("[ 1.2m] chi2 = 12.3456  sigma 0.4321\n2026-10-03 12:00 fecha\n")
        (d / "b.log").write_text("[ 9.9m] chi2 = 12.3456  sigma 0.4321\n2026-10-04 13:00 fecha\n")
        # ORIGEN-VALOR: 12.3457 — el mismo dato sintetico con un digito alterado (debe NO cuadrar)
        (d / "c.log").write_text("[ 1.2m] chi2 = 12.3457  sigma 0.4321\n2026-10-03 12:00 fecha\n")
        (d / "a.json").write_text(json.dumps({"x": 1.5, "fecha": "hoy", "y": [2.25]}))
        (d / "b.json").write_text(json.dumps({"x": 1.5, "fecha": "mañana", "y": [2.25]}))
        (d / "c.json").write_text(json.dumps({"x": 1.5, "fecha": "hoy", "y": [2.26]}))
        r = [compara(d / "a.log", d / "b.log")[0], compara(d / "a.log", d / "c.log")[0],
             compara(d / "a.json", d / "b.json")[0], compara(d / "a.json", d / "c.json")[0]]
    return r == [True, False, True, False], r


def main(lista, salida):
    global DIF
    DIF = pathlib.Path(salida).parent / "recorre_salidas_nuevas"
    ok, r = control()
    print("CONTROL del comparador:", "PASA" if ok else "NO PASA", r)
    if not ok:
        sys.exit(1)
    casos = [ln.split("\t") for ln in open(lista).read().splitlines() if ln.strip()]
    antes = _estado()
    res = []
    for c in casos:
        log, scr = pathlib.Path(c[0]), c[1]
        if c[3] != "ligero":
            continue
        nombra = c[4] == "nombra-su-log"
        t0 = time.time()
        with tempfile.TemporaryDirectory() as d:
            copia = pathlib.Path(d) / log.name
            shutil.copy2(ROOT / log, copia)
            nuevo = pathlib.Path(d) / ("nuevo" + log.suffix)
            env = dict(os.environ, OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
                       MPLBACKEND="Agg", PYTHONPATH=str(ROOT / "src"))
            try:
                o = subprocess.run(["nice", "-n", "10", str(ROOT / ".venv/bin/python3"), scr], cwd=ROOT, env=env,
                                   capture_output=True, text=True, timeout=1200)
                rc, err = o.returncode, o.stderr[-600:]
                if nombra:
                    if (ROOT / log).exists():
                        shutil.copy2(ROOT / log, nuevo)
                else:
                    nuevo.write_text(o.stdout)
            except subprocess.TimeoutExpired:
                rc, err = "timeout", ""
            if rc == 0 and nuevo.exists():
                cuadra, det = compara(copia, nuevo)
                if not cuadra:
                    DIF.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(nuevo, DIF / log.name)   # la salida nueva, para mirarla; FUERA del repo
            else:
                cuadra, det = None, {"rc": rc, "stderr": err}
            # restaurar: sólo lo que ESTA corrida tocó
            despues = _estado()
            for ruta, est in despues.items():
                if ruta in antes and antes[ruta] == est:
                    continue
                if ruta.startswith(PROTEGE):
                    continue      # corridas ajenas en curso (la conjunta y sus colas): jamás se tocan
                if est.strip() == "??":
                    p = ROOT / ruta
                    if p.is_file():   # se MUEVE fuera del repo, no se borra: si algo se coló, se recupera
                        destino = DIF / "_creados" / ruta.replace("/", "__")
                        destino.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(p), destino)
                else:
                    _git("checkout", "--", ruta)
            shutil.copy2(copia, ROOT / log)   # el log vuelve a ser el de antes, byte a byte
        estado = "CUADRA" if cuadra else ("NO CUADRA" if cuadra is False else "NO CORRE")
        print(f"{estado:9s} {time.time() - t0:6.0f}s  {log}  <- {scr}", flush=True)
        res.append(dict(log=str(log), script=scr, estado=estado, detalle=det, segundos=round(time.time() - t0)))
    json.dump(dict(control_comparador=ok, casos=res), open(salida, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
