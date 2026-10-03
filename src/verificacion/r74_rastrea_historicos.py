#!/usr/bin/env python3
"""r74_rastrea_historicos.py — busca en el historial de git el log de cada número
de los cajones que R74 marca sin procedencia (2026-10-02).

POR QUE. R74 deja 136 decimales de los cajones (Registro, OPEN_PROBLEMS, README,
CLAUDE.md) sin fuente vigente. Casi todos son valores HISTÓRICOS: corridas que
existieron y se superaron, cuyo log ya no está en el árbol pero sí en git. R74
acepta en la línea una referencia `git:<commit>:<ruta>` y la ABRE para comprobar
que el valor está escrito ahí; este script no decide nada: solo encuentra el
par (commit, ruta) que R74 va a verificar por su cuenta.

COMO. Para cada número: `git log -S<numero>` sobre results/logs, CANONICAL y el
núcleo da los commits que lo añadieron o quitaron; en cada uno (y en su padre,
para los que lo quitaron) se abre cada archivo tocado y se acepta el primero
donde R74 (`fuente_git`) da por bueno el valor. Sin hallazgo: queda en la lista
de deuda real, sin tocar la línea.

    python3 src/verificacion/r74_rastrea_historicos.py          # informa
    python3 src/verificacion/r74_rastrea_historicos.py aplica   # escribe las referencias
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src" / "verificacion"))
import r74_procedencia as P  # noqa: E402

# 2026-10-02: también results/ entero y archive/ (logs de scripts archivados); NO src/: un
# literal en un script es un número tecleado, no la salida que lo prueba (salvo el núcleo).
RUTAS = ["results", "archive", "CANONICAL_VALUES.yaml", "src/ssee_core.py"]
TEXTO = (".log", ".json", ".txt", ".csv", ".yaml", ".dat", "ssee_core.py")


def _git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, timeout=120).stdout


def candidato(s):
    for sha in _git("log", "--all", f"-S{s}", "--format=%H", "--", *RUTAS).split():
        for c in (sha, sha + "^"):
            for ruta in _git("show", "--name-only", "--format=", sha, "--", *RUTAS).split():
                if not ruta.endswith(TEXTO):
                    continue      # binarios (.npz, .png, .pdf) y prosa (.md): no son salidas
                if not P.fuente_admisible(ruta):
                    continue      # cadenas MCMC (casan por azar), reportes de cola/guardian y prosa: no prueban
                ref = f"git:{_git('rev-parse', '--short=10', c).strip()}:{ruta}"
                if P.fuente_git(ref, s):
                    return ref
    return None


def main(aplica):
    res = P.barrido()["cajones"]
    hallados, sin = {}, []
    for n, casos in res.items():
        for ln, s in casos:
            ref = candidato(s)
            (hallados.setdefault(n, {}).setdefault(ln, []).append((s, ref)) if ref else sin.append((n, ln, s)))
    tot = sum(len(v) for d in hallados.values() for v in d.values())
    print(f"con referencia historica: {tot} · sin hallazgo: {len(sin)}")
    for n, d in hallados.items():
        for ln, pares in d.items():
            for s_, r_ in pares:
                print(f"   CON  {n}:{ln}  {s_}  {r_}")
    for n, ln, s in sin:
        print(f"   SIN  {n}:{ln}  {s}")
    if aplica:
        for n, d in hallados.items():
            f = ROOT / n
            L = f.read_text().split("\n")
            for ln, pares in d.items():
                refs = sorted({r for _, r in pares})
                L[ln - 1] = L[ln - 1].rstrip() + " <!-- R74: " + " ".join(refs) + " -->"
            f.write_text("\n".join(L))
        print("referencias escritas")


if __name__ == "__main__":
    main(len(sys.argv) > 1 and sys.argv[1] == "aplica")
