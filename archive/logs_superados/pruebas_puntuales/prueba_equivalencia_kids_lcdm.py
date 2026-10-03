#!/usr/bin/env python3
"""¿El cambio de `cobaya_kids.py` movio el camino de LCDM fondo-fijo?

POR QUE EXISTE (2026-09-19). R35 marco como rancios `kids_lcdm_fondofijo_*`
porque el commit 8f49b48 toco `bg_key_to_dict`, que SI esta en su camino. La
regla hace bien en preguntar: el codigo del camino cambio.

Pero lo que se anadio es una GUARDA de retorno temprano para otro modelo:

    if bg_key[0] == 'SSEEwch':      # <- texto
        ...

y el camino de LCDM fondo-fijo llama con

    bg_key = (0.02237, 0.1200, 0.6736, 0.9649)     # <- cuatro flotantes (Planck 2018)

asi que `bg_key[0]` es un float y la comparacion con un str es False SIEMPRE.
La rama es inalcanzable para este log.

Eso es un razonamiento, y un razonamiento no es una prueba. Esto lo EJECUTA:
saca la funcion de las dos versiones del fichero (la del commit del log y la
de hoy), las corre sobre la clave real de LCDM fondo-fijo, y compara.

Se corre solo:  python3 src/verificacion/prueba_equivalencia_kids_lcdm.py
"""
# ORIGEN-VALOR: 0.6736 — h de Planck 2018 (arXiv:1807.06209) dentro de una clave de control
import ast
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = "src/p06_growth/cobaya_kids.py"
LOGS = ("kids_lcdm_fondofijo_reparto", "kids_lcdm_fondofijo_SIN_REPARTO_20260908")
# La clave con la que `loglike_lcdm_fijo` entra a `loglike` (Planck 2018 clavado)
CLAVE = (0.02237, 0.1200, 0.6736, 0.9649)   # Planck 2018 (arXiv:1807.06209)
SALIDA = REPO / "results" / "logs" / "equivalencia_kids_lcdm.log"


def version_en(sha):
    return subprocess.run(["git", "show", f"{sha}:{SCRIPT}"], cwd=REPO,
                          capture_output=True, text=True).stdout


def sha_del_log(nombre):
    return subprocess.run(["git", "log", "-1", "--format=%H", "--",
                           f"results/logs/{nombre}.log"], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()


def saca_funcion(fuente, nombre):
    """Extrae la funcion y las asignaciones de modulo que necesita, y la
    ejecuta en un espacio limpio. Asi no hace falta importar cobaya ni camb."""
    arbol = ast.parse(fuente)
    fn = next(n for n in arbol.body
              if isinstance(n, ast.FunctionDef) and n.name == nombre)
    usa = {x.id for x in ast.walk(fn) if isinstance(x, ast.Name)}
    cuerpo = [s for s in arbol.body
              if isinstance(s, ast.Assign)
              and {x.id for t in s.targets for x in ast.walk(t) if isinstance(x, ast.Name)} & usa]
    # El nucleo, con el alias que use cada version (`import ssee_core as S`).
    import importlib.util as _ilu
    _sp = _ilu.spec_from_file_location("_core_eq", REPO / "src" / "ssee_core.py")
    _core = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_core)
    ns = {}
    for s_ in arbol.body:
        if isinstance(s_, ast.Import):
            for a in s_.names:
                if a.name == "ssee_core":
                    ns[a.asname or a.name] = _core
    exec(compile(ast.Module(body=cuerpo + [fn], type_ignores=[]),
                 "<extraido>", "exec"), ns)
    return ns[nombre]


def main():
    filas, todo_igual = [], True
    for log in LOGS:
        sha = sha_del_log(log)
        vieja = saca_funcion(version_en(sha), "bg_key_to_dict")
        nueva = saca_funcion((REPO / SCRIPT).read_text(), "bg_key_to_dict")
        a, b = vieja(CLAVE), nueva(CLAVE)
        igual = a == b
        todo_igual &= igual
        filas.append({"log": log, "commit_del_log": sha[:12],
                      "clave": list(CLAVE), "antes": a, "ahora": b,
                      "identico": igual})
        print(f"  {log}")
        print(f"    commit del log : {sha[:12]}")
        print(f"    antes          : {a}")
        print(f"    ahora          : {b}")
        print(f"    identico       : {'SI' if igual else 'NO'}")

    # Control del otro lado (R53): la comprobacion tiene que poder FALLAR.
    # Con la clave del OTRO modelo las dos versiones deben diferir — si no
    # difirieran, esta prueba no estaria midiendo nada.
    ctrl_ok = False
    try:
        vieja = saca_funcion(version_en(sha_del_log(LOGS[0])), "bg_key_to_dict")
        nueva = saca_funcion((REPO / SCRIPT).read_text(), "bg_key_to_dict")
        clave_otra = ('SSEEwch', 0.12, 0.6736)
        try:
            av = vieja(clave_otra)
        except Exception:
            av = "ERROR"
        an = nueva(clave_otra)
        ctrl_ok = (av != an)
        print(f"\n  CONTROL con la clave del otro modelo {clave_otra}:")
        print(f"    antes: {str(av)[:60]}")
        print(f"    ahora: {str(an)[:60]}")
        print(f"    difieren (debe ser SI): {'SI' if ctrl_ok else 'NO'}")
    except Exception as e:
        print("  CONTROL no se pudo correr:", e)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(
        {"pregunta": "el cambio de cobaya_kids.py mueve el camino de LCDM fondo-fijo?",
         "respuesta": "no" if todo_igual else "SI — hay que re-correr",
         "control_puede_fallar": ctrl_ok, "casos": filas},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  escrito en {SALIDA.relative_to(REPO)}")
    if not (todo_igual and ctrl_ok):
        print("\n  ROJO — o el camino cambio, o la prueba no puede fallar.")
        return 1
    print("\n  VERDE — el camino de LCDM da lo mismo antes y despues,")
    print("  y la prueba sabe distinguirlo (el control difiere).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
