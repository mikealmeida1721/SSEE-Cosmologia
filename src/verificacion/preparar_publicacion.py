#!/usr/bin/env python3
"""preparar_publicacion.py — la compuerta ANTES de publicar una versión.

POR QUÉ EXISTE (2026-07-27)
---------------------------
La fecha de portada de un preprint significa **«ésta es la versión que publiqué
ese día»** — como arXiv v1/v2. No es la fecha de inicio del proyecto ni la de
hoy. De ahí se sigue algo que costó entender:

  · mientras se trabaja, la fecha NO se toca;
  · el día que se publica, se mueve UNA vez y para TODOS los documentos.

Hoy la suite tiene cinco fechas distintas (April/May/June/«2026»/\\today) y los
diez papers se publicaron JUNTOS en Zenodo. Quien descargue el paquete ve una
serie que parece desincronizada. El `\\today` del Sealed es peor: cambia en cada
compilación, así que dos personas compilando el mismo .tex obtienen PDFs
distintos — en el documento que se llama «sellado».

El error que este script evita (lo cometí): poner la fecha de la *última versión
ya publicada*. Esa versión contiene justamente los errores que se están
corrigiendo; fecharla así afirma que el trabajo de hoy ya estaba dentro. La
fecha correcta es la del día en que se publica la versión NUEVA.

QUÉ TOCA Y QUÉ NO
-----------------
SÓLO el `\\date{...}` del preámbulo — la portada. Nunca una fecha del cuerpo:
«DESI DR2 (2025)», «Planck 2018», los años de las citas y las fechas de los
logs son fechas de OTRAS cosas y deben quedarse como están. Por construcción
este script no puede tocarlas: sólo mira `\\date{}`.
El sufijo descriptivo se conserva («--- Paper 9 of the SSEE series»).

USO
---
    # 1) mirar sin tocar nada (por defecto)
    .venv/bin/python3 src/verificacion/preparar_publicacion.py

    # 2) el día de publicar, con la fecha de ESE día
    .venv/bin/python3 src/verificacion/preparar_publicacion.py \\
        --fecha "September 2026" --aplicar

Sale 0 si la suite está lista para publicar, 1 si hay algo que mirar antes.
"""
import argparse
import pathlib
import re
import sys

_REPO = pathlib.Path(__file__).resolve().parents[2]
_DIRS = ("manuscript", "submission_PRD")
_MES = re.compile(r"^\s*(?:\\today|[A-Z][a-z]+\s+\d{4}|\d{4})\s*")


def portadas():
    """(ruta, fecha_actual, sufijo) de cada documento con \\date en el preámbulo."""
    out = []
    for d in _DIRS:
        for tx in sorted((_REPO / d).glob("*.tex")):
            m = re.search(r"\\date\{([^}]*)\}", tx.read_text(errors="ignore"))
            if m:
                out.append((tx, m.group(1), _MES.sub("", m.group(1))))
    return out


def bloquea_today(fechas):
    """True si alguna fecha de portada es \\today (no reproducible)."""
    return any("\\today" in f for f in fechas)


def revision_pendiente():
    """Páginas que la lectura página-por-página aún no cerró."""
    log = _REPO / "LECTURA_PAPERS.md"
    if not log.exists():
        return None
    txt = log.read_text(errors="ignore")
    return txt.count("| ⬜") + len(re.findall(r"\|\s*⬜\s*\|", txt))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fecha", help='fecha de la versión NUEVA, p. ej. "September 2026"')
    ap.add_argument("--aplicar", action="store_true",
                    help="escribir los cambios (sin esto, sólo informa)")
    a = ap.parse_args()

    docs = portadas()
    fechas = {_MES.match(f).group(0).strip() if _MES.match(f) else f
              for _, f, _ in docs}
    listo = True

    print(f"\nPortadas encontradas: {len(docs)} documentos\n")
    for tx, actual, _ in docs:
        print(f"  {tx.name:38s} {actual}")

    print("\n── Estado ──")
    if len(fechas) > 1:
        print(f"  ✗ {len(fechas)} fechas distintas en la misma serie: "
              + ", ".join(sorted(fechas)))
        print("    Una serie publicada junta debe llevar UNA fecha.")
        listo = False
    else:
        print(f"  ✓ fecha única en toda la serie: {fechas.pop()}")

    if bloquea_today(f for _, f, _ in docs):
        print("  ✗ hay \\today: cambia en cada compilación — dos builds del mismo")
        print("    .tex dan PDFs distintos. No se publica con \\today.")
        listo = False
    else:
        print("  ✓ ningún \\today (fechas reproducibles)")

    pend = revision_pendiente()
    if pend:
        print(f"  ✗ la lectura página-por-página tiene ~{pend} páginas sin cerrar")
        print("    Sólo se publica cuando la revisión terminó y Mike la verificó.")
        listo = False
    elif pend == 0:
        print("  ✓ lectura página-por-página sin páginas pendientes")

    if a.fecha:
        nueva = a.fecha.strip()
        if _MES.match(nueva) is None:
            print(f"\n  ✗ «{nueva}» no parece una fecha de portada (esperado: «Month YYYY»)")
            return 1
        print(f"\n── {'APLICANDO' if a.aplicar else 'SIMULACIÓN (usa --aplicar)'} → {nueva} ──")
        for tx, actual, suf in docs:
            destino = (nueva + " " + suf).strip() if suf else nueva
            if destino == actual:
                continue
            print(f"  {tx.name:38s} {actual!r} → {destino!r}")
            if a.aplicar:
                s = tx.read_text()
                m = re.search(r"\\date\{([^}]*)\}", s)
                tx.write_text(s[:m.start()] + "\\date{" + destino + "}" + s[m.end():])
        if a.aplicar:
            print("\n  Recompilar los .tex y sincronizar docs/ antes de subir.")
    elif not listo:
        print('\n  Para fijar la fecha de la versión nueva:'
              '\n    --fecha "Month YYYY" --aplicar   (usa el día en que publicás,'
              '\n                                      NO la fecha de la versión anterior)')

    print(f"\n{'LISTA para publicar' if listo else 'NO publicar todavía'}\n")
    return 0 if listo else 1


if __name__ == "__main__":
    sys.exit(main())
