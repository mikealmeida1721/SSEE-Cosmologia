#!/usr/bin/env python3
"""rutas_mv.py — cuenta y verifica las rutas aditivas al techo M_v = 3(φ+π) (2026-10-15).

POR QUE. Paper 4 decía «exactamente veinte rutas (6 + 11 + 3)», tecleado a mano y sin
script; el diccionario publicado (zenodo_dictionary/SSEE_Constant_Dictionary.md §4) dice
veinticuatro (8 + 13 + 3) desde las pasadas de linaje de 2026-07. Lo vio la lectura fría
de P4. Este script lee las rutas DEL MISMO código que define el diccionario
(src/estadistica/look_elsewhere_full.py), no de una lista aparte, para que el conteo no
pueda divergir otra vez del diccionario.

QUE HACE. Recorre por AST las asignaciones de look_elsewhere_full.py. Una ruta es una
asignación cuyo lado derecho es una SUMA de nombres (sin productos ni restas: ley aditiva)
cuyo valor es M_v. Para cada una registra sus padres y verifica:
  * suma = M_v a < 1e-14 (redondeo de punto flotante);
  * no-auto-suma: ningún padre repetido;
  * 2 ≤ número de padres ≤ 4.
TRÏSTAL = 3·Ω es la copia pura (producto, no suma): se cuenta aparte, no es ruta aditiva.

CONTROL (R53). El total y el desglose deben coincidir con lo que declara el diccionario
(24 = 8 + 13 + 3); se escriben los dos y `control_pasa` dice si coinciden.

Salida: results/logs/p04_rutas_mv.json (con acta).
"""
import ast
import json
import math
import os
import sys

_R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import con_acta  # noqa: E402

FUENTE = os.path.join(_R, "src", "estadistica", "look_elsewhere_full.py")
DICCIONARIO = os.path.join(_R, "zenodo_dictionary", "SSEE_Constant_Dictionary.md")
# ORIGEN-VALOR: 8, 13, 3 — desglose que declara el diccionario publicado (§4, «Count = 24 =
# 8 (two-parent) + 13 (three-parent) + 3 (four-parent)»); es el blanco del control, no un dato
DECLARADO = {2: 8, 3: 13, 4: 3}

src = open(FUENTE).read()
arbol = ast.parse(src)

# valores: se ejecuta el módulo de definiciones hasta el diccionario FAMILY (sin correr la búsqueda)
corte = src.index("\nFAMILY = {")
ns = {}
exec(compile(src[:corte], FUENTE, "exec"), ns)
MV = 3 * (ns["PHI"] + ns["PI"])


def sumandos(nodo):
    """Nombres de una suma pura a+b+c; None si hay otra operación."""
    if isinstance(nodo, ast.Name):
        return [nodo.id]
    if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Add):
        a, b = sumandos(nodo.left), sumandos(nodo.right)
        return None if a is None or b is None else a + b
    return None


rutas = []
for nodo in ast.walk(arbol):
    if not isinstance(nodo, ast.Assign) or len(nodo.targets) != 1:
        continue
    destino = nodo.targets[0]
    if not isinstance(destino, ast.Name) or destino.lineno > src[:corte].count("\n") + 1:
        continue
    padres = sumandos(nodo.value)
    if not padres or len(padres) < 2:
        continue
    valor = sum(ns[p] for p in padres)
    if abs(valor - MV) > 1e-9:
        continue
    rutas.append(dict(nombre=destino.id, padres=padres, n_padres=len(padres),
                      desvio=valor - MV,
                      sin_auto_suma=len(set(padres)) == len(padres)))

por_n = {n: sum(1 for r in rutas if r["n_padres"] == n) for n in (2, 3, 4)}
fuera = [r["nombre"] for r in rutas if r["n_padres"] > 4]
max_desvio = max(abs(r["desvio"]) for r in rutas)
todas_legales = all(r["sin_auto_suma"] for r in rutas) and not fuera
control = (por_n == DECLARADO) and todas_legales and max_desvio < 1e-14

for r in sorted(rutas, key=lambda r: (r["n_padres"], r["nombre"])):
    print(f"  {r['n_padres']}  {r['nombre']:10s} = {' + '.join(r['padres']):34s} "
          f"desvio {r['desvio']:+.1e}")
print(f"\n  total {len(rutas)}  (2: {por_n[2]}, 3: {por_n[3]}, 4: {por_n[4]})   "
      f"max |desvio| {max_desvio:.1e}   control {'PASA' if control else 'FALLA'}")

json.dump(con_acta(dict(
    que="rutas aditivas con nombre al techo M_v = 3(phi+pi), leidas del codigo del diccionario",
    M_v=MV,
    total=len(rutas), dos=por_n[2], tres=por_n[3], cuatro=por_n[4],
    copia_pura="TRISTAL = 3*OMEGA (producto; no es ruta aditiva)",
    max_desvio=max_desvio,
    rutas=sorted(rutas, key=lambda r: (r["n_padres"], r["nombre"])),
    declarado_diccionario=DECLARADO,
    control_pasa=control,
), __file__, entradas=[FUENTE, DICCIONARIO]),
    open(os.path.join(_R, "results", "logs", "p04_rutas_mv.json"), "w"), indent=1, ensure_ascii=False)
if not control:
    sys.exit("CONTROL FALLA: el conteo no coincide con el diccionario")
