#!/usr/bin/env python3
"""armar_prd.py — arma el zip de envío a Physical Review D y lo compila en vacío.

POR QUÉ EXISTE (2026-10-16). El zip que había (`SSEE_PRD_submission.zip`) era del
2026-07-24: el .tex y las figuras de julio. Y el .tex vigente hace
`\\input{../manuscript/valores_generados.tex}`, una ruta FUERA del paquete: la revista
no habría podido compilarlo. Este script lo arma desde el árbol y lo prueba.

QUÉ HACE
  1. Copia SSEE_PRD.tex reescribiendo a local TODO lo que lee de ../manuscript/
     (valores_generados.tex y las tablas generadas, también con el \\input primitivo).
  2. Añade esos archivos, la bibliografía (.bib) y el .bbl ya resuelto (REVTeX
     lo acepta y evita depender de bibtex en el servidor de la revista).
  3. Añade SÓLO las figuras que el .tex incluye, desde submission_PRD/figures/.
  4. Descomprime el zip en una carpeta temporal VACÍA y compila con pdflatex tres veces (la tercera asienta el índice);
     falla si hay errores o referencias sin definir.
  5. Exige que el PDF del paquete tenga las mismas páginas y EL MISMO TEXTO que
     submission_PRD/SSEE_PRD.pdf (un \\val sin valor no da error: sale vacío en silencio).

USO
    .venv/bin/python3 src/verificacion/armar_prd.py            # escribe submission_PRD/SSEE_PRD_submission.zip
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
PRD = ROOT / "submission_PRD"
SALIDA = PRD / "SSEE_PRD_submission.zip"
# Todo lo que el .tex lee de ../manuscript/, con llaves o con el \input primitivo.
ENTRADAS = re.compile(r"\.\./manuscript/([A-Za-z0-9_]+\.tex)")


def paginas(pdf):
    o = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", o)
    return int(m.group(1)) if m else None


def main():
    tex = (PRD / "SSEE_PRD.tex").read_text()
    leidos = sorted(set(ENTRADAS.findall(tex)))
    if "valores_generados.tex" not in leidos:
        sys.exit("armar_prd: el .tex no lee valores_generados.tex")
    tex = ENTRADAS.sub(lambda m: m.group(1), tex)
    figs = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex)
    faltan = [f for f in figs if not (PRD / "figures" / f).exists()]
    if faltan:
        sys.exit(f"armar_prd: faltan figuras {faltan}")
    with tempfile.TemporaryDirectory() as d:
        z = pathlib.Path(d) / "paquete.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("SSEE_PRD.tex", tex)
            for f in leidos:
                zf.write(ROOT / "manuscript" / f, f)
            zf.write(PRD / "ssee_unified.bib", "ssee_unified.bib")
            zf.write(PRD / "SSEE_PRD.bbl", "SSEE_PRD.bbl")
            for f in sorted(set(figs)):
                zf.write(PRD / "figures" / f, f"figures/{f}")
        prueba = pathlib.Path(d) / "vacio"
        prueba.mkdir()
        zipfile.ZipFile(z).extractall(prueba)
        for _ in range(3):   # la tercera asienta el índice (sus páginas se corren una)
            r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "SSEE_PRD.tex"],
                               cwd=prueba, capture_output=True, text=True)
        log = (prueba / "SSEE_PRD.log").read_text(errors="ignore")
        errores = len(re.findall(r"^! ", log, re.M))
        sin_def = len(re.findall(r"(Reference|Citation) `[^']+' on page \d+ undefined", log))
        # Un \\val sin valor NO da error en LaTeX: sale vacío en silencio. Por eso se compara
        # el TEXTO entero del PDF del paquete con el del PDF de referencia.
        txt = lambda pdf: subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                                         capture_output=True, text=True).stdout
        texto_igual = txt(prueba / "SSEE_PRD.pdf") == txt(PRD / "SSEE_PRD.pdf")
        p_nuevo, p_ref = paginas(prueba / "SSEE_PRD.pdf"), paginas(PRD / "SSEE_PRD.pdf")
        print(f"armar_prd: {len(leidos)} archivos de manuscript/ {leidos}, {len(set(figs))} figuras, errores={errores}, sin definir={sin_def}, "
              f"páginas {p_nuevo} (referencia {p_ref}), texto idéntico={texto_igual}")
        if errores or sin_def or p_nuevo != p_ref or not texto_igual:
            sys.exit("armar_prd: el paquete NO compila igual que el PDF de referencia; no se escribe")
        shutil.copy(z, SALIDA)
    print(f"armar_prd: escrito {SALIDA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
