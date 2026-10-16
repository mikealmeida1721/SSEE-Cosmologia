"""Prueba de MUTACIÓN del guardián, dirigida por el registro de reglas.

Inyecta un defecto CONOCIDO en un manuscrito, corre el guardián, y exige que
falle **la regla que dice cubrirlo** — no cualquiera. Después restaura el archivo
y verifica que quedó idéntico.

POR QUÉ EXISTE (2026-07-29). Mike: «que el guardián me dé verde no significa que
esté bien». Un VERDE demuestra que nada saltó; NO demuestra que algo habría
saltado. Eso sólo se prueba rompiendo el documento a propósito.

POR QUÉ SE EXIGE LA REGLA CONCRETA. La primera versión sólo miraba si el guardián
enrojecía. Eso deja pasar el peor caso: la regla nueva no funciona, pero otra
salta por casualidad y el resultado parece correcto. Atribuir el fallo demuestra
que la regla añadida es la que trabaja.

Así se destapó el agujero original: «$n_s = 1-\\varphi^{-7}$ & $0.965123$» —un
valor sencillamente MAL, a 4.4e-4 del exacto— pasaba VERDE, porque la ventana de
identificación de R38 lo leía como «esta celda no habla de n_s» y los patrones de
R30 esperan «fórmula = valor» con el valor en la misma celda.

Uso:  python3 src/verificacion/mutacion_guardian.py
"""
# ORIGEN-VALOR: 0.965123 — defecto INYECTADO a proposito (n_s con error 4e-4), el mismo caso de registro_reglas.py
import re
import sys
import pathlib
import subprocess

_AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_AQUI))
import registro_reglas as _reg   # noqa: E402

REPO = _AQUI.parent.parent
TEX = REPO / _reg.TEX_MUTACION
GUARDIAN = _AQUI / "ssee_verify.py"


def corre():
    """(sin regresiones?, [nombres de los checks que fallaron]).

    Se mira el eje REGRESIÓN, no el titular. Desde que el veredicto separa
    «regresión» de «modelo» (2026-09-07), un repo sano titula AMARILLO mientras
    queden problemas abiertos, y esta suite —que sólo pregunta si el guardián
    enrojece ante un defecto inyectado— se quedaba abortando en la línea base
    con «el guardián ya está en rojo». Inutilizada sin que nada lo dijera: el
    fallo era silencioso porque salía por la puerta de un caso legítimo.
    """
    r = subprocess.run([sys.executable, str(GUARDIAN)],
                       capture_output=True, text=True, cwd=REPO)
    fallos = re.findall(r"^\s*x\s+(\S+)", r.stdout, re.M)
    return ("sin regresiones" in r.stdout), fallos, r.stdout


# El árbol debe estar LIMPIO antes de mutar. Si una corrida anterior murió a
# mitad —un timeout, un Ctrl-C— deja el defecto inyectado en el disco, y la
# siguiente arranca sobre un repo roto sin saberlo. Pasó el 2026-07-29: matar
# `test_guardian.py` a los 2 minutos dejó «HERMES = PHI + KAL + 0.0» escrito en
# look_elsewhere_full.py, y el guardián amaneció en ROJO por una causa que no
# estaba en ningún sitio.
# Se vigilan SÓLO los archivos que alguna mutación toca —los declarados en el
# registro más el .tex— y también los de `test_guardian.py`, que muta por su
# cuenta. Vigilar el árbol entero marcaría el propio trabajo en curso sobre la
# infraestructura de verificación y volvería inservible el aviso.
_objetivos = sorted({_reg.TEX_MUTACION} |
                    {v["archivo"] for v in _reg.REGLAS.values() if v.get("archivo")} |
                    {"src/estadistica/look_elsewhere_full.py"})
# CERROJO. La comprobación de árbol sucio mira el disco al ARRANCAR, y eso no
# basta: si la otra suite ya está corriendo, este proceso arranca sobre un árbol
# limpio y las dos se pisan los archivos a mitad. Pasó el 2026-07-29 — lanzar
# `test_guardian.py` mientras esta suite corría dejó un valor mutado en
# VERIFICATION_LEDGER.md, que la restauración de esta suite volvió a escribir
# como si fuera el original, y el control negativo salió ROJO sin defecto.
# Las dos suites mutan; sólo puede haber UNA viva a la vez.
_LOCK = REPO / ".mutacion.lock"
if _LOCK.exists():
    print(f"otra suite de mutación está corriendo (cerrojo {_LOCK.name}).")
    print("  Espera a que termine: dos suites a la vez se pisan los archivos")
    print("  y la restauración de una sobrescribe el defecto de la otra.")
    print("  Si sabes que ninguna corre, bórralo a mano.")
    sys.exit(1)
_LOCK.write_text(f"mutacion_guardian.py pid={__import__('os').getpid()}\n")
import atexit as _atexit
import signal as _signal
_atexit.register(lambda: _LOCK.exists() and _LOCK.unlink())

# RESTAURACION ANTE MUERTE. El `finally` de cada caso devuelve el archivo, pero
# no corre si al proceso lo matan a mitad —un timeout, un Ctrl-C—, y entonces el
# defecto inyectado se queda escrito en el disco. Paso el 2026-09-08: una corrida
# cortada a los 280 s dejo la mutacion de R57 en prueba_rol.py, y el arbol
# amanecio con un defecto que no estaba en ningun sitio.
# Dos contramedidas: (a) el cerrojo ANOTA que archivo esta mutado ahora mismo,
# para que quien lo encuentre sepa exactamente que restaurar; (b) se atienden
# SIGTERM y SIGINT restaurando antes de salir. Contra SIGKILL no hay defensa
# posible — para eso queda (a).
_EN_CURSO = {"archivo": None, "base": None}


def _restaura_en_curso(*_a):
    if _EN_CURSO["archivo"] is not None:
        (REPO / _EN_CURSO["archivo"]).write_text(_EN_CURSO["base"])
        print(f"\nrestaurado {_EN_CURSO['archivo']} antes de salir")
    if _LOCK.exists():
        _LOCK.unlink()
    sys.exit(1)


for _sig in (_signal.SIGTERM, _signal.SIGINT):
    _signal.signal(_sig, _restaura_en_curso)

_sucio = subprocess.run(["git", "status", "--porcelain", "--"] + _objetivos,
                        capture_output=True, text=True, cwd=REPO).stdout.strip()
if _sucio:
    print("árbol SUCIO antes de mutar — puede ser el resto de una corrida muerta:")
    for _l in _sucio.splitlines():
        print("   ", _l)
    print("  revísalo y déjalo limpio; si no, no se distingue un defecto real")
    print("  de un residuo, que es justo lo que la prueba existe para evitar.")
    sys.exit(1)


# EFECTOS COLATERALES (2026-10-16). Un caso puede ensuciar archivos que NO muta:
# con el nucleo alterado, algo calculo r_d con otra Σm_ν y la escribio en el
# cache data/processed/rd_camb_tabla.json. El `finally` solo restaura el archivo
# mutado, asi que el cache quedo cambiado, R75 lo vio al final y el control
# negativo salio ROJO «sin defecto»: ruido de la propia suite. Ahora, tras cada
# caso, todo archivo rastreado que no estaba sucio al empezar y lo esta ahora se
# devuelve a su version de git, y se nombra el caso que lo ensucio.
def _sucios():
    _o = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"],
                        capture_output=True, text=True, cwd=REPO).stdout
    return {_l[3:] for _l in _o.splitlines() if _l[3:] and not _l[3:].startswith("sandbox_unificado")}


_SUCIOS0 = _sucios()
colaterales = []


def _limpia_colaterales(etiqueta):
    _nuevos = sorted(_sucios() - _SUCIOS0)
    if _nuevos:
        subprocess.run(["git", "checkout", "--"] + _nuevos, cwd=REPO, check=True)
        colaterales.append(f"{etiqueta}: {', '.join(_nuevos)}")
        print(f"      (efecto colateral restaurado: {', '.join(_nuevos)})")


orig = TEX.read_text()
verde, _, _ = corre()
print(f"línea base: {'VERDE' if verde else 'ROJO'}")
if not verde:
    print("  el guardián ya está en rojo: arréglalo antes de mutar.")
    sys.exit(1)

problemas = []
# CASOS DE ESTADO. Algunas reglas no vigilan texto sino una condicion del
# sistema de ficheros —R31 vigila un `.pyc` rancio con el fuente INTACTO— y no
# caben en (archivo, viejo, nuevo). En vez de declararlas «no mutables», que es
# como se acumulan los puntos ciegos, la regla declara `estado` y aqui se
# prepara y se restaura llamando a mutacion_estado.py.
_EST = _AQUI / "mutacion_estado.py"
for regla, info in _reg.REGLAS.items():
    if not info.get("estado"):
        continue
    etiqueta = f"{regla} · estado: {info['estado']}"
    subprocess.run([sys.executable, str(_EST), info["estado"], "prepara"],
                   cwd=REPO, check=True)
    try:
        _, fallos, salida = corre()
    finally:
        subprocess.run([sys.executable, str(_EST), info["estado"], "restaura"],
                       cwd=REPO, check=True)
        _limpia_colaterales(etiqueta)
    if not fallos and "comprobaciones" not in salida:
        problemas.append(f"{etiqueta}: el guardian se CAYO")
        print(f"  [  CAIDA  ] {etiqueta}")
    elif not any(f.startswith(tuple(info.get("prefijos", [regla]))) for f in fallos):
        problemas.append(f"{etiqueta}: no lo detecta {regla}"
                         + (f" (lo caza {fallos[0]})" if fallos else " — nadie"))
        print(f"  [ {'OTRA    ' if fallos else ' PASA   '} ] {etiqueta}")
    else:
        print(f"  [ DETECTA ] {etiqueta}")

for regla, info in _reg.REGLAS.items():
    for caso in info["mutacion"]:
        # Un caso puede declarar el archivo que muta. Sin declararlo, es el .tex.
        # Las capas de FÍSICA no viven en un manuscrito: se prueban tocando
        # `ssee_core.py` o el propio guardián, que es donde vive lo que afirman.
        arch, (nombre, viejo, nuevo) = ((info.get("archivo", _reg.TEX_MUTACION), caso)
                                        if len(caso) == 3 else (caso[0], caso[1:]))
        destino = REPO / arch
        base = destino.read_text()
        etiqueta = f"{regla} · {nombre}"
        if viejo not in base:
            problemas.append(f"{etiqueta}: el ancla ya no existe en {arch}")
            print(f"  [ ANCLA?  ] {etiqueta}")
            continue
        _EN_CURSO.update(archivo=arch, base=base)
        _LOCK.write_text(f"mutacion_guardian.py pid={__import__('os').getpid()}\n"
                         f"MUTANDO AHORA: {arch}\n"
                         f"si esta corrida murio, restaura ese archivo con "
                         f"`git checkout -- {arch}` antes de nada\n")
        destino.write_text(base.replace(viejo, nuevo, 1))
        try:
            _, fallos, salida = corre()
        finally:
            destino.write_text(base)      # restaurar SIEMPRE
            _EN_CURSO.update(archivo=None, base=None)
            _limpia_colaterales(etiqueta)
        # CAIDA != NO DETECTADO. Si el guardian ni siquiera llego al veredicto
        # —el nucleo mutado no importa, por ejemplo— no hay lista de fallos, y
        # la version anterior lo contaba como «nadie lo detecta (VERDE por
        # vacio)». Es un diagnostico FALSO, y del peor tipo: describe como
        # ceguera lo que fue una interrupcion. Se separan (2026-09-08).
        if not fallos and "comprobaciones" not in salida:
            problemas.append(f"{etiqueta}: el guardian se CAYO, no llego a "
                             f"veredicto — no se puede concluir nada")
            print(f"  [  CAIDA  ] {etiqueta}")
            continue
        if not fallos:
            problemas.append(f"{etiqueta}: nadie lo detecta (VERDE por vacío)")
            print(f"  [  PASA   ] {etiqueta}")
        elif not any(f.startswith(tuple(info.get("prefijos", [regla]))) for f in fallos):
            problemas.append(f"{etiqueta}: lo detecta {fallos[0]}, no {regla}")
            print(f"  [ OTRA    ] {etiqueta} → lo caza {fallos[0]}")
        else:
            print(f"  [ DETECTA ] {etiqueta}")

# Control negativo: sin defecto, nadie debe disparar. Una regla que se queja del
# documento correcto es tan inútil como una que no se queja del roto.
TEX.write_text(orig)
verde, _, _ = corre()
print(f"  [{' CONTROL ' if verde else ' FALLA   '}] documento intacto → "
      f"{'VERDE, nadie dispara' if verde else 'ALGUIEN DISPARA SIN DEFECTO'}")
if not verde:
    problemas.append("control negativo: hay ruido sobre el documento correcto")

assert TEX.read_text() == orig, "¡el archivo NO volvió a su estado original!"
if colaterales:
    print("\nefectos colaterales (restaurados; no son defectos del guardian):")
    for _c in colaterales:
        print("   ·", _c)
print("\narchivo restaurado idéntico ✓")

if problemas:
    print(f"\nMUTACIÓN-ROJO — {len(problemas)} caso(s):")
    for p in problemas:
        print("   x ", p)
    sys.exit(1)
print(f"\nMUTACIÓN-VERDE — {sum(len(v['mutacion']) for v in _reg.REGLAS.values())} "
      f"defectos inyectados, cada uno detectado por SU regla.")
