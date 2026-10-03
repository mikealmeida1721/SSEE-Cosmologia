#!/usr/bin/env python3
"""
manifiesto_datos_T2.py — comprueba que los datos crudos bajados siguen siendo
los mismos bytes que se declararon, y dice lo que hay dentro de cada uno.

POR QUE EXISTE. El 2026-09-26 se bajaron las sondas que tenian T2 bloqueado
(DES Y3, SN Ia, lensing de CMB). Un dato bajado de internet sin huella no es
reproducible: dentro de un ano nadie sabra si el fichero que hay en el disco es
el que se uso. El manifiesto guarda el sha256 y la URL de origen de cada uno.

NO valida la fisica: valida que el fichero no cambio y que se puede abrir.
Correr:  .venv/bin/python3 src/verificacion/manifiesto_datos_T2.py
Fuente:  data/manifiesto_descargas_T2.json (2026-10-03: estaba en results/logs/ como si fuera
         un resultado; es un manifiesto de ENTRADA y vive junto a los datos)
"""
import hashlib
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MAN = os.path.join(REPO, "data", "manifiesto_descargas_T2.json")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    with open(MAN) as f:
        man = json.load(f)
    print(f"  Manifiesto de {man['fecha']} — {len(man['ficheros'])} ficheros\n")
    mal = []
    for it in man["ficheros"]:
        p = it["ruta"]
        if not os.path.exists(p):
            print(f"  [FALTA]  {it['nombre']}"); mal.append(it["nombre"]); continue
        if os.path.getsize(p) != it["bytes"]:
            print(f"  [TAMANO] {it['nombre']}"); mal.append(it["nombre"]); continue
        s = sha(p)
        ok = s == it["sha256"]
        print(f"  [{'  OK  ' if ok else 'CAMBIO'}] {it['nombre']:<38}{it['bytes']:>12,}")
        if not ok:
            mal.append(it["nombre"])
    for b in man["bloqueado_aun"]:
        print(f"\n  [BLOQUEADO] {b['sonda']}\n    {b['razon']}")
    if mal:
        print(f"\n  {len(mal)} fichero(s) no coinciden con el manifiesto.")
        sys.exit(1)
    print(f"\n  Los {len(man['ficheros'])} coinciden byte a byte con lo declarado.")


if __name__ == "__main__":
    main()
