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
# Memoria de Claude Code para este proyecto; configurable con SSEE_MEMCLAUDE.
MEMCLAUDE = pathlib.Path(os.environ.get(
    "SSEE_MEMCLAUDE", pathlib.Path.home() / ".claude/projects/-home-mike-Proyectos-SSEE/memory"))


SELLO = "> **Registro fechado**"
_SELLO_RE = re.compile(r"«([^»]+)»")


def _estricta(label, path):
    """En la memoria de Claude, el indice y las reglas (feedback_/user_) son
    ESTADO VIVO: se barren sin sello. Las project_* son registros fechados."""
    return not label.startswith("Memoria") or path.name == "MEMORY.md" or \
        path.name.startswith(("feedback_", "user_"))


def _load():
    with open(CANON, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _retirados_por_historia(cfg):
    """Valores que FUERON canonicos y ya no lo son, sacados del historial git de
    CANONICAL_VALUES.yaml (2026-09-30). La lista `retired:` solo cubre lo que
    alguien declaro retirado; esto cubre lo que se cambio en `canonical:` sin
    declararlo. Filtros: se ignoran los cambios de signo por convencion
    (5.35 -> -5.35), los refinamientos de redondeo (0.30889 -> 0.308881, el
    vigente redondeado da el viejo), los valores de menos de 3 cifras
    significativas y los que hoy son el valor vigente de alguna clave."""
    import subprocess
    try:
        revs = subprocess.run(["git", "-C", str(ROOT), "log", "--format=%h %ad", "--date=short",
                               "--", CANON.name], capture_output=True, text=True, timeout=60).stdout.split()
    except Exception:
        return []
    # cache: el historial solo cambia con un commit nuevo del YAML o con el YAML
    # actual (que decide los filtros); la clave es ambos.
    import hashlib
    import json
    clave = hashlib.sha256((" ".join(revs) + CANON.read_text(encoding="utf-8")).encode()).hexdigest()
    cache = pathlib.Path.home() / ".cache" / "ssee_memory_sync_historial.json"
    try:
        c = json.loads(cache.read_text())
        if c.get("clave") == clave:
            return c["out"]
    except Exception:
        pass
    cur = cfg["canonical"]
    vigentes = {str(v) for v in cur.values()}
    ya = {r["pattern"] for r in cfg["retired"]}
    hist = {}
    for h, fecha in zip(revs[::2], revs[1::2]):
        txt = subprocess.run(["git", "-C", str(ROOT), "show", f"{h}:{CANON.name}"],
                             capture_output=True, text=True).stdout
        try:
            viejo = (yaml.safe_load(txt) or {}).get("canonical") or {}
        except yaml.YAMLError:
            continue
        for k, v in viejo.items():
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                hist.setdefault((k, str(v)), fecha)
    out = []
    for (k, sv), fecha in sorted(hist.items()):
        ahora = cur.get(k)
        cifras = re.sub(r"[^0-9]", "", sv.lstrip("-0."))
        if sv in vigentes or sv in ya or len(cifras) < 3:
            continue
        dec = len(sv.split(".")[1]) if "." in sv else 0

        def _redondeo(x):
            return (abs(float(sv)) == abs(x) or round(x, dec) == float(sv)
                    or abs(abs(float(sv)) - abs(x)) < 0.999 * 10 ** -dec)   # a menos de una unidad de su ultima cifra
            # (con 1.5 unidades pasaba −33.0→−32.9 del ΔBIC plik completo, que
            # es un cambio REAL: N 2409→2354. Visto en el control del 2026-09-30.)
        if isinstance(ahora, (int, float)):
            if _redondeo(ahora):
                continue
        elif k not in cur and any(_redondeo(x) for x in cur.values()
                                  if isinstance(x, (int, float)) and not isinstance(x, bool)):
            # CLAVE RENOMBRADA (2026-09-30: alpha_K_full -> s_K_full,
            # f_screen_UV -> f_screen): su valor viejo es el redondeo de uno
            # vigente con otro nombre, no un retirado. Solo para claves que ya
            # no existen; una clave viva se juzga contra SU valor.
            continue
        out.append({"pattern": sv.lstrip("-"), "auto": True,
                    "reason": f"historial git: {k} valia {sv} (visto {fecha}); hoy {ahora}"})
    try:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps({"clave": clave, "out": out}))
    except Exception:
        pass
    return out


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
        estado = [ROOT / "README.md", ROOT / "RIGOR_CHECKLIST.md", ROOT / "OPEN_PROBLEMS.md"]
        out.append(("Estado raíz", [p for p in estado if p.exists()]))
    if not vault_only and MEMCLAUDE.exists():
        # La memoria de Claude (2026-09-30): el indice MEMORY.md se carga en
        # CADA sesion y las memorias guian lo que Claude afirma. Un valor
        # retirado ahi se repite en la conversacion aunque los papers esten bien.
        out.append(("Memoria Claude", sorted(MEMCLAUDE.glob("*.md"))))
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
# en la MISMA frase que el valor: se corta en «. », «; » y en los
# limites del parrafo. (« · » NO corta: separa los items de una lista
# «RETIRADOS: a · b · c», que cuelgan todos de la misma marca.) El decimal «0.968» no corta (no lleva
# espacio tras el punto). Una FILA de tabla es un registro (como un item de
# lista): su unidad es la fila, cortada solo por frases dentro de ella; en .tex
# la fila termina en «\\\\».
_CORTE = re.compile(r"\.\s|;\s|\\\\")   # «\\\\» = fin de fila de tabla .tex


def _frase(lines, lines_low, i, col):
    if re.match(r"^\s*(?:>\s*)?\|", lines[i]):
        a = b = i
    else:
        a, b = _parrafo(lines, i)
    texto = " ".join(lines_low[a:b + 1])
    # un item de lista es UNA afirmacion (p. ej. una entrada de la historia de
    # H0 con su «Superado por…» al final): ahi la unidad es el item entero.
    if re.match(r"^\s*(?:>\s*)?(?:[-*+]\s|\d+[.)]\s)", lines[a]):
        return texto
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
    return " " + texto[ini:fin]   # « era» al inicio de frase


def scan(vault_only=False):
    """Devuelve (drifts, scanned). drifts = lista de (memoria, archivo, lineno, patrón, texto)."""
    cfg = _load()
    retired = cfg["retired"] + _retirados_por_historia(cfg)
    coincid = cfg.get("coincidencias") or []
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
            # REGISTRO FECHADO (memoria project_* de Claude): su sello lista los
            # numeros superados que contiene A PROPOSITO. Solo esos quedan
            # exentos; uno retirado despues vuelve a avisar hasta re-sellar.
            sellados = set()
            if not _estricta(label, path):
                for ln in lines:
                    if ln.startswith(SELLO):
                        sellados = set(_SELLO_RE.findall(ln))
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
                if in_hist or raw.startswith(SELLO):
                    continue
                for item in retired:
                    pat = item["pattern"]
                    pl = pat.lower()
                    if pl not in low[i]:
                        continue
                    cols = [m.start() for m in re.finditer(re.escape(pl), low[i])]
                    if item.get("auto"):
                        # un numero sacado del historial se compara ENTERO:
                        # «0.337» no debe casar dentro de «0.3371»
                        # (ceros finales permitidos: «40.7» casa con «40.70»)
                        def _fin(k):
                            e = k + len(pat)
                            if "." in pat:
                                while e < len(low[i]) and low[i][e] == "0":
                                    e += 1
                            return e
                        cols = [k for k in cols if not (k > 0 and (low[i][k - 1].isdigit() or low[i][k - 1] == "."))
                                and not (_fin(k) < len(low[i]) and low[i][_fin(k)].isdigit())]
                    req = [r.lower() for r in item.get("requires", [])]
                    exc = [e.lower() for e in item.get("excludes", [])]

                    def exenta(fr):
                        # marca de contexto, `requires` y `excludes` se miden en la
                        # MISMA unidad (la frase). Antes requires/excludes miraban
                        # ±1 linea y un «68.13» de la linea de Paper 9 eximia el
                        # «±0.970» de la de Paper 10 en CLAUDE.md (2026-09-30).
                        return (any(mk in fr for mk in markers)
                                or (req and not any(t in fr for t in req))
                                or (exc and any(t in fr for t in exc)))
                    # basta UNA aparicion no exenta en su frase para que sea drift
                    if pat in sellados:
                        continue
                    if not cols or all(exenta(_frase(lines, low, i, k)) for k in cols):
                        continue
                    # COINCIDENCIA REVISADA: el mismo numero pero OTRA cantidad
                    # (p. ej. wa = -0.659 medido por DESI frente a k_fs = 0.659 de
                    # la particula). Cada una se anota en `coincidencias:` del
                    # YAML con archivo, contexto y razon — nunca se exime en silencio.
                    if any(c["pattern"] == pat and str(path).endswith(c["archivo"])
                           and c["contexto"].lower() in low[i] for c in coincid):
                        continue
                    # Discriminador de cantidad (opcional): un decimal pelado como
                    # «0.766» puede ser un S₈ retirado O un χ²/N legitimo. El patron
                    # declara tokens: `requires` → solo es drift si ALGUNO esta en
                    # la frase; `excludes` → NO es drift si alguno esta (arriba).
                    rel = path.relative_to(VAULT if label.startswith("Obsidian") else MEMCLAUDE if label.startswith("Memoria") else ROOT)
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


def sellar_memorias():
    """Escribe/actualiza el sello de cada memoria project_* con avisos: la lista
    se CALCULA del barrido, no se teclea. Las estrictas no se sellan: se corrigen."""
    import datetime
    drifts, _ = scan()
    por = {}
    for label, rel, _ln, pat, _t in drifts:
        if label.startswith("Memoria") and not _estricta(label, MEMCLAUDE / rel):
            por.setdefault(rel, set()).add(pat)
    for rel, pats in sorted(por.items()):
        p = MEMCLAUDE / rel
        L = p.read_text(encoding="utf-8").split("\n")
        viejo = next((i for i, l in enumerate(L) if l.startswith(SELLO)), None)
        if viejo is not None:
            pats |= set(_SELLO_RE.findall(L[viejo]))
            del L[viejo]
            if viejo < len(L) and not L[viejo].strip():
                del L[viejo]
        lista = " · ".join(f"«{x}»" for x in sorted(pats))
        sello = (f"{SELLO} (sellado {datetime.date.today()} por memory_sync). Los numeros "
                 f"son los de su fecha; los vigentes estan en CANONICAL_VALUES.yaml. "
                 f"Superados en esta nota: {lista}")
        fin = 0
        if L and L[0].strip() == "---":
            fin = next(i for i in range(1, len(L)) if L[i].strip() == "---") + 1
        L[fin:fin] = ["", sello, ""] if fin else [sello, ""]
        p.write_text("\n".join(L), encoding="utf-8")
        print(f"  sellada {rel}: {len(pats)} valor(es)")


if __name__ == "__main__":
    if "--sellar-memorias" in sys.argv:
        sellar_memorias()
        sys.exit(0)
    vo = "--vault" in sys.argv
    sys.exit(1 if run(vault_only=vo) else 0)
