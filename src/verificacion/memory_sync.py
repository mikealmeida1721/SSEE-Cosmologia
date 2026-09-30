#!/usr/bin/env python3
"""
memory_sync.py — el sincronizador de las 3 memorias de SSEE.

Las 3 memorias deben concordar SIEMPRE (regla de Mike):
  • Guardián  — VERIFICATION_LEDGER.md (resultados/valores)
  • Obsidian  — /home/mike/SSEE-Vault (conexiones/cadenas)
  • CLAUDE.md — contexto/estado

Este script lee CANONICAL_VALUES.yaml (fuente única de verdad) y revisa que
NINGUNA memoria presente un valor RETIRADO como vigente. Un valor retirado
sólo se permite si en su misma FRASE hay una marca de contexto
(retirado, viejo, Type-P, coincidencia, sin re-correr…).

    .venv/bin/python3 src/verificacion/memory_sync.py            # las 3 memorias
    .venv/bin/python3 src/verificacion/memory_sync.py --vault    # sólo el vault

  VERDE → memorias sincronizadas.   DRIFT → una memoria quedó desfasada.

Diseñado para ser barato: correr tras cada cambio de valor. También lo invoca
ssee_verify.py (el Guardián) como su capa de coherencia de memorias.
"""
import os
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
# Vault personal (Obsidian); configurable con SSEE_VAULT, default ~/SSEE-Vault.
# Si no existe, el sync de vault se omite con gracia (no rompe en otra PC).
VAULT = pathlib.Path(os.environ.get("SSEE_VAULT", pathlib.Path.home() / "SSEE-Vault"))
CANON = ROOT / "CANONICAL_VALUES.yaml"


def _load():
    with open(CANON, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _targets(vault_only=False):
    """Los cajones a escanear, como (etiqueta, lista de Paths).

    Cobertura completa de la propagación: las 3 memorias (Ledger, CLAUDE,
    vault) MÁS el cajón de papers (manuscript/*.tex). Una corrida marca cada
    lugar donde un canónico retirado quedó como vigente — la contabilidad
    automática de propagación (detecta, no edita: nunca produce '1+1=3')."""
    out = []
    if not vault_only:
        out.append(("Guardián (Ledger)", [ROOT / "VERIFICATION_LEDGER.md"]))
        out.append(("CLAUDE.md", [ROOT / "CLAUDE.md"]))
        out.append(("Papers (cajón)", sorted((ROOT / "manuscript").glob("*.tex"))))
        # El PRD de envío vive FUERA de manuscript/ y por eso nadie lo barría
        # (hallazgo 2026-09-19, auditoría Zenodo): es el documento que se manda
        # a la revista, o sea el de mayor consecuencia si queda rancio.
        out.append(("PRD (envío)", sorted((ROOT / "submission_PRD").glob("*.tex"))))
        # Docs de ESTADO VIVO en la raíz (sin fecha, cara pública vigente).
        # NO se incluyen los de REGISTRO/FECHADOS: CHANGELOG.md y
        # AUDIT.md (deliverable fechado 2026-05-17, con banner de superación),
        # MEMORY_PROTOCOL.md (usa valores viejos como ejemplos del drift) ni
        # archive/ (incluye HALG_PIFI_CHANGEMAP.md y el material de investigación
        # —open_problems, mira_attempts— movido a archive/codigo/investigacion/ el 2026-06-24).
        estado = [ROOT / "README.md", ROOT / "RIGOR_CHECKLIST.md"]
        out.append(("Estado raíz", [p for p in estado if p.exists()]))
    if VAULT.exists():
        # `Archivo/` es el cajón de retirados del vault — el equivalente exacto
        # del `archive/` del repo, que ya se excluye arriba. Una nota archivada
        # DEBE poder narrar el valor retirado con todas sus letras: ése es su
        # trabajo. Escanearla obligaría a censurar la historia que se conserva.
        out.append(("Obsidian (vault)",
                    sorted(p for p in VAULT.rglob("*.md")
                           if "Archivo" not in p.relative_to(VAULT).parts)))
    elif not vault_only:
        print(f"  [aviso] vault no encontrado en {VAULT} — se omite Obsidian")
    return out


# `_marked` (ventana ±1 línea) vivía aquí y se BORRÓ el 2026-09-19. Dos
# razones, y la segunda es la que importa: ya no la llamaba nadie —la
# sustituyó `_marked_parrafo` el mismo día—, y su docstring ilustraba la
# ventana con «72.86», un valor de la cascada invertida retirado el
# 2026-09-06. Un ejemplo no necesita un número retirado para explicar una
# ventana, y usarlo lo vuelve indistinguible de una afirmación viva.


def _parrafo(lines, i):
    """Limites del parrafo que contiene la linea i (bloques entre lineas en
    blanco). Para .md se respetan ademas los items de lista: un item es una
    afirmacion propia y no lo exonera su vecino."""
    import re as _r
    _item = _r.compile(r"^\s*(?:>\s*)?(?:[-*+]\s|\d+[.)]\s)")
    ini = i
    while ini > 0:
        if _item.match(lines[ini]):
            break
        if not lines[ini - 1].strip():
            break
        if _item.match(lines[ini - 1]) and not lines[ini].startswith((" ", "\t")):
            break
        ini -= 1
    fin = i
    while fin + 1 < len(lines):
        s = lines[fin + 1]
        if not s.strip():
            break
        if _item.match(s) and not s.startswith((" ", "\t")):
            break
        fin += 1
    return ini, fin


def _marked_parrafo(lines, lines_low, i, markers):
    a, b = _parrafo(lines, i)
    ventana = " ".join(lines_low[a:b + 1])
    return any(mk in ventana for mk in markers)


# LA UNIDAD ES LA FRASE, NO EL PARRAFO (2026-09-30). El parrafo seguia siendo
# demasiado ancho: en CLAUDE.md un banner «> ...» o una tabla markdown no tienen
# lineas en blanco, asi que el parrafo era el banner ENTERO o la tabla ENTERA, y
# un solo «retirado» en cualquier fila eximia a todas las demas. Con eso el
# ΔBIC −26.21 retirado se vio en 1 de 16 sitios. Ahora la marca tiene que estar
# en la MISMA frase que el valor: se corta en «. », «; », « · » y en los
# limites del parrafo. El decimal «0.968» no corta (no lleva
# espacio tras el punto). Una FILA de tabla es un registro (como un item de
# lista): su unidad es la fila, cortada solo por frases dentro de ella; en .tex
# la fila termina en «\\\\».
_CORTE = re.compile(r"\.\s|;\s|\s·\s|\\\\")   # «\\\\» = fin de fila de tabla .tex


def _marked_frase(lines, lines_low, i, col, markers):
    if re.match(r"^\s*(?:>\s*)?\|", lines[i]):
        a = b = i
    else:
        a, b = _parrafo(lines, i)
    texto = " ".join(lines_low[a:b + 1])
    # un item de lista es UNA afirmacion (p. ej. una entrada de la historia de
    # H0 con su «Superado por…» al final): ahi la unidad es el item entero.
    if re.match(r"^\s*(?:>\s*)?(?:[-*+]\s|\d+[.)]\s)", lines[a]):
        return any(mk in texto for mk in markers)
    p = sum(len(lines_low[j]) + 1 for j in range(a, i)) + col
    # un corte DENTRO de un parentesis no cierra la frase: «(era X; Y DR1)» es
    # una sola acotacion historica y su marca vale para todo lo de adentro.
    prof, nivel = 0, []
    for ch in texto:
        prof += (ch == "(") - (ch == ")")
        nivel.append(max(prof, 0))
    cortes = [m for m in _CORTE.finditer(texto) if nivel[m.start()] == 0 or nivel[m.start()] < nivel[p]]
    ini = max([m.end() for m in cortes if m.end() <= p], default=0)
    fin = min([m.start() for m in cortes if m.start() >= p], default=len(texto))
    # (Se probo tambien lo inverso —que una marca en un parentesis mas hondo no
    # exima al valor de afuera— y se descarto: rompe el giro mas comun,
    # «20.98 (DR1, retirado)», donde el parentesis anota al valor.)
    frase = " " + texto[ini:fin]   # « era» al inicio de frase
    return any(mk in frase for mk in markers)


def scan(vault_only=False):
    """Devuelve (drifts, scanned). drifts = lista de (memoria, archivo, lineno, patrón, texto)."""
    cfg = _load()
    retired = cfg["retired"]
    markers = [m.lower() for m in cfg["context_markers"]]
    hist_heads = [h.lower() for h in cfg.get("historical_sections", [])]
    drifts = []
    scanned = 0

    for label, paths in _targets(vault_only):
        for path in paths:
            if not path.exists():
                continue
            scanned += 1
            lines = path.read_text(encoding="utf-8").splitlines()
            low = [ln.lower() for ln in lines]
            in_hist = False
            hist_level = 0
            for i, raw in enumerate(lines):
                # Seguimiento de sección con NIVEL de encabezado: una sección
                # histórica (##) sigue siéndolo a través de sus sub-encabezados
                # (###) y sólo se cierra con un encabezado hermano o superior.
                stripped = raw.lstrip()
                if stripped.startswith("#"):
                    level = len(stripped) - len(stripped.lstrip("#"))
                    if any(h in low[i] for h in hist_heads):
                        in_hist, hist_level = True, level
                    elif in_hist and level <= hist_level:
                        in_hist, hist_level = False, 0
                # LA MARCA VALE EN SU UNIDAD, NO EN LA LINEA DE AL LADO
                # (2026-09-19). `_marked` mira la linea i y sus vecinas +-1, y
                # con eso Paper 5 mantuvo VIVO el S8=0.758 retirado: la frase
                # «The phi-DM two-sector split once described here is
                # retracted» estaba en la linea ANTERIOR y eximia a la
                # siguiente, que afirmaba el 0.758 como resultado. memory_sync
                # salia VERDE. Lo encontro una auditoria externa.
                #
                # Es el mismo defecto que se cerro esa manana en el guardian
                # (R60: la unidad de afirmacion), y este era el componente al
                # que no se llevo el arreglo. Aqui la unidad es el PARRAFO:
                # un .tex justificado parte las frases por ancho de columna,
                # asi que la linea no significa nada, pero el parrafo si.
                if in_hist:
                    continue
                for item in retired:
                    pat = item["pattern"]
                    cols = [k for k in range(len(low[i])) if low[i].startswith(pat.lower(), k)]
                    # basta UNA aparicion sin marca en su frase para que sea drift
                    if not cols or all(_marked_frase(lines, low, i, k, markers) for k in cols):
                        continue
                    # Discriminador de cantidad (opcional): un decimal pelado como
                    # «0.766» puede ser un S₈ retirado O un χ²/N legítimo. El
                    # patrón puede declarar tokens de desambiguación que se buscan
                    # en la ventana ±1 (igual que los context_markers):
                    #   `requires`  → sólo es drift si ALGÚN token co-ocurre.
                    #   `excludes`  → NO es drift si ALGÚN token co-ocurre
                    #                 (p. ej. «χ²» marca un goodness-of-fit, no un S₈).
                    # Sin ninguno → comportamiento previo (substring puro).
                    win = [low[j] for j in (i - 1, i, i + 1) if 0 <= j < len(low)]
                    req = [r.lower() for r in item.get("requires", [])]
                    if req and not any(tok in l for l in win for tok in req):
                        continue
                    exc = [e.lower() for e in item.get("excludes", [])]
                    if exc and any(tok in l for l in win for tok in exc):
                        continue
                    rel = path.relative_to(VAULT if label.startswith("Obsidian") else ROOT)
                    drifts.append((label, str(rel), i + 1, pat, raw.strip()[:90]))
    return drifts, scanned


def run(vault_only=False, verbose=True):
    """Imprime el informe y devuelve la lista de drifts (vacía = sincronizado)."""
    drifts, scanned = scan(vault_only)
    if verbose:
        print(f"memory_sync — {scanned} archivos de memoria escaneados")
        if not drifts:
            print("  VERDE — las memorias concuerdan con CANONICAL_VALUES.yaml.")
        else:
            print(f"  DRIFT — {len(drifts)} valor(es) retirado(s) sin marcar:")
            for label, rel, ln, pat, txt in drifts:
                print(f"   [{label}] {rel}:{ln}  «{pat}»  →  {txt}")
    return drifts


if __name__ == "__main__":
    vo = "--vault" in sys.argv
    sys.exit(1 if run(vault_only=vo) else 0)
