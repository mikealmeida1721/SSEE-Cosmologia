#!/usr/bin/env python3
"""¿Acotar la cache de CAMB a 3 movio algun numero de los logs de KiDS-1000?

POR QUE EXISTE (2026-09-19). El commit 8a41450 acoto `_camb_cached` de
`cobaya_kids.py` de 300 espectros a 3 (era la fuga de memoria que corto la
maquina). `_camb_cached` esta en el camino de los CUATRO logs que produce ese
script, asi que R35 los marca como rancios. Hace bien en preguntar.

Una cache no deberia cambiar un resultado: solo decide si un espectro se
RECALCULA o se REUSA. Pero eso es un razonamiento. Esto lo EJECUTA: carga la
version del fichero del commit de CADA log y la de hoy, corre la funcion de
entrada de ese log sobre la MISMA secuencia de puntos y compara bit a bit.

La secuencia esta hecha para ejercitar lo que cambio:
  * cuatro claves de cache distintas -> con tope 3, la primera se DESALOJA;
  * vuelta a un punto desalojado   -> la version nueva lo recalcula;
  * A_IA y halo_A cambiando con el punto lento fijo -> reuso de cache.

Control del otro lado (R53): una cache ROTA a proposito (clave que ignora halo_A,
o sea reusa un espectro que no corresponde) tiene que dar OTRO numero. Si no lo
diera, esta prueba no sabria ver un defecto de cache y no mediria nada. El
control se corre en cada uno de los cuatro caminos.

Se corre solo:  python3 src/verificacion/prueba_equivalencia_kids_cache.py
"""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = "src/p06_growth/cobaya_kids.py"
SALIDA = REPO / "results" / "logs" / "equivalencia_kids_cache.log"
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "p06_growth"))

# log -> funcion de entrada (la misma que declara PROPAGACION.yaml; el R4 no
# declara entrada y corre `loglike_lcdm`, fondo libre).
CASOS = {
    "kids_ssee_wc_h":                           "loglike_ssee_wc_h",
    "kids_lcdm_fondofijo_reparto":              "loglike_lcdm_fijo",
    "kids_lcdm_fondofijo_SIN_REPARTO_20260908": "loglike_lcdm_fijo",
    "R4_lcdm_resume_20260805":                  "loglike_lcdm",
}
# Punto de base: arranque de las cadenas. Puntos de prueba, no medidas.
BASE = dict(ombh2=0.02237, omch2=0.1195, h0=0.68, ns=0.9649, logA=3.0,
            halo_A=2.6, A_IA=0.5, dz1=0.0, dz2=0.0, dz3=0.0, dz4=0.0,
            dz5=0.0, delta_c=0.0)
# ORIGEN-VALOR: 0.1180 — punto de prueba inventado para cambiar la clave de cache, no es medida
# ORIGEN-VALOR: 0.1210 — punto de prueba inventado para cambiar la clave de cache, no es medida
# ORIGEN-VALOR: 0.1170 — punto de prueba inventado para cambiar la clave de cache, no es medida
# Cuatro claves de cache distintas: se mueve halo_A (esta en la clave de todas
# las entradas) y, donde existen, omch2/h0/logA.
CLAVES = [dict(halo_A=2.6), dict(halo_A=2.8, omch2=0.1180, h0=0.690, logA=2.95),
          dict(halo_A=3.0, omch2=0.1210, h0=0.672, logA=3.05),
          dict(halo_A=2.4, omch2=0.1170, h0=0.685, logA=2.90)]


def secuencia(firma):
    s = []
    for c in CLAVES:
        # reuso con la clave lenta fija: A_IA (no toca CAMB) y halo_A (SI esta
        # en la clave de la cache). El segundo es el que el control necesita:
        # una cache que ignore halo_A solo se delata si halo_A cambia CON EL
        # RESTO FIJO. (La primera version generalizada movia halo_A solo junto
        # con la clave, y su control no pudo fallar: lo cazo R53.)
        for aia, dh in ((0.5, 0.0), (0.9, 0.0), (0.5, 0.2)):
            d = dict(BASE, **c, A_IA=aia)
            d["halo_A"] = c["halo_A"] + dh
            s.append({k: d[k] for k in firma})
    d = dict(BASE, **CLAVES[0])                   # vuelta a la desalojada
    s.append({k: d[k] for k in firma})
    return s


def carga(nombre, fuente):
    tmp = pathlib.Path(tempfile.mkdtemp()) / f"{nombre}.py"
    tmp.write_text(fuente, encoding="utf-8")
    sp = importlib.util.spec_from_file_location(nombre, tmp)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def evalua(mod, fn, seq):
    f = getattr(mod, fn)
    return [float(f(**kw)) for kw in seq]


def version_en(sha):
    return subprocess.run(["git", "show", f"{sha}:{SCRIPT}"], cwd=REPO,
                          capture_output=True, text=True).stdout


def sha_del_log(log):
    return subprocess.run(["git", "log", "-1", "--format=%H", "--",
                           f"results/logs/{log}.log"], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()


def rompe(mod):
    """Cache rota a proposito: la clave ignora halo_A."""
    orig, roto = mod._camb_cached, {}

    def _camb_roto(bg_key, As, halo_A):
        k = (bg_key, round(As, 15))
        if k not in roto:
            roto[k] = orig(bg_key, As, halo_A)
        return roto[k]
    mod._camb_cached = _camb_roto
    return mod


def main():
    import inspect
    hoy = (REPO / SCRIPT).read_text()
    casos, todo_ok = [], True
    for n, (log, fn) in enumerate(CASOS.items()):
        sha = sha_del_log(log)
        V = carga(f"ck_v{n}", version_en(sha))
        N = carga(f"ck_n{n}", hoy)
        R = rompe(carga(f"ck_r{n}", hoy))
        seq = secuencia(list(inspect.signature(getattr(N, fn)).parameters))
        a, b, c = evalua(V, fn, seq), evalua(N, fn, seq), evalua(R, fn, seq)
        dif = max(abs(x - y) for x, y in zip(a, b))
        dctl = max(abs(x - y) for x, y in zip(b, c))
        ok = dif == 0.0 and dctl > 1e-6
        todo_ok &= ok
        print(f"\n  {log}  ({fn}, commit del log {sha[:12]})")
        for i, (x, y, z) in enumerate(zip(a, b, c)):
            print(f"    {i:2d}  antes {x:15.9f}  ahora {y:15.9f}  rota {z:15.9f}")
        print(f"    max |antes - ahora| = {dif:.3e} (debe ser 0)   "
              f"max |ahora - rota| = {dctl:.3e} (debe ser > 0)")
        casos.append({"log": log, "entrada": fn, "commit_del_log": sha[:12],
                      "evaluaciones": len(seq), "max_dif_antes_ahora": dif,
                      "control_cache_rota_dif": dctl, "ok": ok,
                      "antes": a, "ahora": b, "rota": c})

    SALIDA.write_text(json.dumps(
        {"pregunta": "acotar la cache de CAMB a 3 mueve el loglike de los logs de cobaya_kids.py?",
         "respuesta": "no" if todo_ok else "SI, o la prueba no puede fallar — revisar",
         "commit_del_cambio": "8a41450", "casos": casos},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  escrito en {SALIDA.relative_to(REPO)}")
    if not todo_ok:
        print("\n  ROJO — o algun loglike cambio, o la prueba no puede fallar.")
        return 1
    print("\n  VERDE — los cuatro caminos dan lo mismo bit a bit, y en los")
    print("  cuatro una cache rota SI se detecta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
