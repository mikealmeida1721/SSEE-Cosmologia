#!/usr/bin/env python3
"""Inventario de números escritos a mano en los documentos publicados (2026-10-10).

Cuarta lectura (Mike: «que no haya un solo número sin que sea reproducible»).
Lista cada decimal del cuerpo de cada .tex que NO sale de \\val{}: quita
comentarios, \\val{..}, \\cite/\\ref/\\label/\\eqref, URLs, DOIs, arXiv ids y la
bibliografía. Cada número sale con su línea y su contexto, para clasificarlo:
  ALG  = álgebra de φ,π (se recalcula con src/ssee_core.py)
  LIT  = dato de literatura (lleva \\cite en la frase/fila)
  LOG  = resultado nuestro (debe ir por \\val desde su log)
  HIS  = valor retirado narrado como historia
  ?    = sin origen → se rastrea o se corrige

    python3 notes/lectura_cuarta/inventario.py            # conteo por documento
    python3 notes/lectura_cuarta/inventario.py P3         # detalle de un documento
"""
import re, sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = {
 "P1": ["manuscript/SSEE_Paper1_Framework.tex", "manuscript/SSEE_EFT_section.tex"],
 "P2": ["manuscript/SSEE_Paper2_MCMC.tex"], "P3": ["manuscript/SSEE_Paper3_CMB.tex"],
 "P4": ["manuscript/SSEE_Paper4_ToE.tex"], "P5": ["manuscript/SSEE_Paper5_IS.tex"],
 "P6": ["manuscript/SSEE_Paper6_Growth.tex"], "P7": ["manuscript/SSEE_Paper7_EFT.tex"],
 "P8": ["manuscript/SSEE_Paper8_StrongGravity.tex"], "P9": ["manuscript/SSEE_Paper9_HubbleTension.tex"],
 "P10": ["manuscript/SSEE_Paper10_UVCompletion.tex"], "SEALED": ["manuscript/SSEE_Sealed_Journal.tex"],
 "UNIFIED": ["manuscript/SSEE_Unified_Journal.tex"], "PRD": ["submission_PRD/SSEE_PRD.tex"],
 "ENDORSER": ["manuscript/SSEE_Endorser_Summary.tex"], "CARTA": ["manuscript/SSEE_Cover_Letter.tex"],
 "PORTADA": ["manuscript/SSEE_Cover.tex"],
}
QUITA = [r"\\val\{[^}]*\}", r"\\(?:cite[pt]?|citealp|ref|eqref|label|url|href|includegraphics|input|bibitem)\*?(?:\[[^\]]*\])*\{[^}]*\}",
         r"arXiv:\s*\d{4}\.\d{4,5}", r"\b\d{4}\.\d{4,5}\b", r"10\.\d{4,9}/\S+", r"https?://\S+",
         r"\\(?:hspace|vspace|setlength|resizebox|includegraphics|columnwidth|textwidth|linewidth)[^\s]*\{[^}]*\}",
         r"\[[0-9.]+(?:pt|cm|mm|em|ex|in)\]", r"[0-9.]+\\(?:textwidth|linewidth|columnwidth)", r"[0-9.]+(?:pt|cm|mm|em|ex)\b"]
NUM = re.compile(r"(?<![\w.])\d+\.\d+(?:\\times10\^\{?-?\d+\}?)?")

def limpia(tx):
    tx = tx.split(r"\begin{thebibliography}")[0].split(r"\bibliography{")[0]
    out = []
    for ln in tx.split("\n"):
        ln = re.sub(r"(?<!\\)%.*", "", ln).replace("\\pm", "\\pm ")
        for q in QUITA:
            ln = re.sub(q, " ", ln)
        out.append(ln)
    return out

def numeros(doc):
    res = []
    for f in DOCS[doc]:
        p = ROOT / f
        if not p.exists():
            continue
        for i, ln in enumerate(limpia(p.read_text(errors="ignore")), 1):
            for m in NUM.finditer(ln):
                res.append((pathlib.Path(f).name, i, m.group(0), ln.strip()[:160]))
    return res

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for r in numeros(sys.argv[1]):
            print(f"{r[0]}:{r[1]}  {r[2]:>12}  | {r[3]}")
    else:
        tot = 0
        for d in DOCS:
            n = numeros(d); tot += len(n)
            print(f"{d:9s} {len(n):5d} números a mano  ({len(set(x[1] for x in n))} líneas)")
        print("TOTAL", tot)
