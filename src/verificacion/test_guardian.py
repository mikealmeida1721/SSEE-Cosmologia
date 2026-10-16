#!/usr/bin/env python3
"""
test_guardian.py — el vigilante vigilado ("who watches the watcher").

El guardián (`ssee_verify.py`) protege contra el FALSO VERDE (decir VERDE
cuando debería ser ROJO). Pero un check puede dejar de detectar en silencio
tras un refactor → el guardián daría falso verde sin que nadie lo note.

Este test vuelve PERMANENTES las pruebas negativas: para cada check crítico,
perturba un cajón a un estado que DEBE disparar ROJO, corre el guardián, y
exige que (a) salga con código ≠ 0 y (b) aparezca el check correcto. Luego
restaura el archivo (siempre, vía finally). Si un check deja de cazar lo suyo,
ESTE test falla → la grieta se delata en vez de pasar callada.

    .venv/bin/python3 src/verificacion/test_guardian.py
    → TODOS VERDES: el guardián detecta lo que debe.
    → ROJO: un check se debilitó; arreglarlo antes de confiar en un VERDE.
"""
import contextlib
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
GUARD = "src/verificacion/ssee_verify.py"
PY = sys.executable
_passed, _failed = 0, 0

# CERROJO compartido con `mutacion_guardian.py`. Las dos suites mutan archivos
# del repo; si corren a la vez se pisan, y la restauración de una escribe como
# «original» el defecto que la otra acababa de inyectar. Pasó el 2026-07-29.
_LOCK = REPO / ".mutacion.lock"
if _LOCK.exists():
    print(f"otra suite de mutación está corriendo (cerrojo {_LOCK.name}); espera.")
    sys.exit(1)
_LOCK.write_text("test_guardian.py\n")
import atexit as _atexit
_atexit.register(lambda: _LOCK.exists() and _LOCK.unlink())


def run_guardian():
    r = subprocess.run([PY, GUARD], cwd=REPO, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


@contextlib.contextmanager
def perturbed(relpath, transform):
    """Perturba un archivo y SIEMPRE lo restaura (bytes originales)."""
    p = REPO / relpath
    original = p.read_bytes()
    try:
        p.write_text(transform(original.decode("utf-8", errors="ignore")),
                     encoding="utf-8")
        yield
    finally:
        p.write_bytes(original)


def expect_red(name, relpath, transform, must_contain):
    global _passed, _failed
    # Ancla perdida (2026-10-16): R29 y R30 inyectaban sobre literales que el PRD
    # ya había pasado a \val; el reemplazo no cambiaba nada, el guardián daba
    # VERDE con razón y la prueba fallaba sin decir por qué. Un caso que no
    # inyecta nada no prueba nada: se marca como tal.
    _txt = (REPO / relpath).read_text(encoding="utf-8", errors="ignore")
    if transform(_txt) == _txt:
        print(f"  [FALLA] {name}\n        ancla perdida: la inyección no cambia {relpath}")
        _failed += 1
        return
    with perturbed(relpath, transform):
        rc, out = run_guardian()
    low = out
    ok = rc != 0 and all(k in low for k in must_contain)
    print(f"  [{'PASS' if ok else 'FALLA'}] {name}")
    if not ok:
        print(f"        esperaba ROJO con {must_contain}; rc={rc}")
    _passed += ok
    _failed += (not ok)


# ── Test positivo: estado limpio → VERDE (exit 0) ───────────────────────
print("Vigilante vigilado — el guardián debe detectar cada falla simulada\n")
rc0, out0 = run_guardian()
_ok0 = rc0 == 0 and "VERDE" in out0
print(f"  [{'PASS' if _ok0 else 'FALLA'}] estado limpio → VERDE (exit 0)")
_passed += _ok0
_failed += (not _ok0)

# ── Tests negativos: cada perturbación DEBE dar ROJO ────────────────────
# F1 — valor de pipeline que NO coincide con su log de procedencia (R9)
expect_red("R9 procedencia: ΔBIC −24.7 no está en el log → ROJO",
           "VERIFICATION_LEDGER.md",
           lambda t: t.replace("−35.0 (SSEE favorecido)", "−24.7 (SSEE favorecido)"),
           ["procedencia", "ROJO"])

# R1 — claim de prioridad temporal
expect_red("R1 cronología: 'predating DESI DR2' → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\n% test predating DESI DR2\n",
           ["R1", "ROJO"])

# R2 — enlace al compendio multidominio retirado
expect_red("R2 multidominio: DOI 19679049 → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\n% test zenodo.19679049\n",
           ["R2", "ROJO"])

# R10 — overclaim 'zero-parameter' global
expect_red("R10 overclaim: 'is a zero-parameter framework' → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\nSSEE is a zero-parameter framework.\n",
           ["R10", "ROJO"])

# R11 — conteo de serie congelado
expect_red("R11 conteo serie: 'Papers~3--7' → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\nextensions in Papers~3--7.\n",
           ["R11", "ROJO"])

# R21 — wₐ con denominador K_v en vez de IGNIS
expect_red("R21 wₐ/K_v: 'P_{sc}/K_v' → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\n$-P_{sc}/K_v$\n",
           ["R21", "ROJO"])

# ORIGEN-VALOR: 0.67000 — defecto INYECTADO a proposito: wa con ceros de precision falsa (R22)
# ORIGEN-VALOR: 0.0229999 — defecto INYECTADO a proposito: omega_b alterado en CANONICAL_VALUES (R26)
# R22 — precisión falsa (wₐ = -0.67000)
expect_red("R22 precisión: '-0.67000' → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\n$w_a=-0.67000$\n",
           ["R22", "ROJO"])

# R23 — fósil Σ₉ / MIKAEL_V / 5D
expect_red("R23 fósil: '\\Sigma_9' → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\n$\\Sigma_9$\n",
           ["R23", "ROJO"])

# R24 — conteo del diccionario retirado (1 of 378)
expect_red("R24 conteo: '1 of 378' → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\n1 of 378 ratios.\n",
           ["R24", "ROJO"])

# ── Cobertura añadida 2026-07-25 ────────────────────────────────────────
# Motivo: el drift de Σm_ν sobrevivió 15 días en VERDE porque R17 verificaba
# el STRING "94.07" y no el NÚMERO derivado. Al medir la cobertura del propio
# auto-test salió que de 16 reglas R con nombre, sólo 9 tenían mutación: las
# otras 7 se asumían buenas — el mismo falso verde, un nivel más arriba.
# Estas mutaciones cierran esa brecha. R14 (procedencia DESI) es la más
# importante del repo: existe porque los BAO venían mal etiquetados DR1/DR2.

# R15 — dos redondeos distintos de la MISMA tensión n_s en un manuscrito
expect_red("R15 n_s redondeo incoherente: 0.16σ y 0.2σ juntos → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           # DEBE caer en la ventana de R15: ancla varphi^{-7} + mención Planck.
           lambda t: t + ("\n$n_s=1-\\varphi^{-7}$ is $0.16\\sigma$ from Planck.\n"
                          "\n$n_s=1-\\varphi^{-7}$ is $0.2\\sigma$ from Planck.\n"),
           ["R15", "ROJO"])

# R17 — la constante ν vuelve a bifurcarse (94.07 reaparece en un manuscrito)
expect_red("R17 constante ν bifurcada: '94.07' reaparece → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\n$\\Sigma m_\\nu = 94.07\\,\\mathrm{eV}\\,\\Omega_\\nu h^2$\n",
           ["R17", "ROJO"])

# R18 — narrativa H0-posterior stale (el r_d agrandado que V-L4-DESI retiró)
expect_red("R18 narrativa stale: 'downward to compensate' → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\nThe posterior shifts downward to compensate.\n",
           ["R18", "ROJO"])

# R19 — un valor BAO de DR1 se cuela en un manuscrito (el bug del mislabel)
expect_red("R19 BAO DR1-mislabeled: D_H=20.08 (DR2=21.863) → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\n$D_H/r_d = 20.08$ for the LRG sample.\n",
           ["R19", "ROJO"])

# R14 — procedencia DESI: alterar un dígito del csv oficial DEBE doler
expect_red("R14 procedencia DESI: csv alterado ≠ Tabla 4 oficial → ROJO",
           "data/raw/desi_dr2_bao.csv",
           # OJO: "21.863" aparece antes en un COMENTARIO de cabecera; hay que
           # mutar la FILA DE DATOS o la mutación no prueba nada (lección propia).
           lambda t: t.replace("0.510,LRG1,DH_over_rd,21.863",
                               "0.510,LRG1,DH_over_rd,21.860", 1),
           ["R14", "ROJO"])

# R20 — meter la PREDICCIÓN SSEE (0.758) en el hueco del DATO KiDS (0.759)
expect_red("R20 ancla observacional: KiDS 0.759 → 0.758 (predicción) → ROJO",
           "CANONICAL_VALUES.yaml",
           lambda t: t.replace("obs_KiDS_S8:         0.759", "obs_KiDS_S8:         0.758", 1),
           ["R20", "ROJO"])

# V-L2-11 — el cierre del sector ν: desincronizar core vs YAML DEBE doler.
# Ésta es la mutación que, de haber existido el 2026-07-10, habría delatado
# el drift en el momento de escribirse la regla.
expect_red("V-L2-11 cierre ν: Σm_ν del core desincronizado del YAML → ROJO",
           "src/ssee_core.py",
           lambda t: t.replace("SUM_MNU_EV = 0.06849", "SUM_MNU_EV = 0.06902", 1),
           ["L2-11", "ROJO"])

# R25 — reintroducir la parametrización invertida (Ω_m congelado · h² para
# fabricar ω_m dentro de código SSEE) DEBE doler. Es el error que sesgó el
# posterior de H₀ hacia el ancla (0.04σ) hasta 2026-07-25.
expect_red("R25 parametrización: ω_m = Ω_m·h² con Ω_m constante → ROJO",
           "src/p02_mcmc/ssee_paper2_mcmc_reframe.py",
           lambda t: t + "\n_bad_om = OMEGA_M_TOTAL*(H0/100)**2\n",
           ["R25", "ROJO"])

# R26a — un canónico SIN fuente declarada. Es la mutación que representa
# directamente a OP-20: el 0.960318 existió porque no había campo que exigiera
# declarar su origen.
expect_red("R26 procedencia: canónico sin `source` → ROJO",
           "CANONICAL_VALUES.yaml",
           lambda t: t.replace(
               '    source:     "Paper 1 (registro estructural); src/ssee_core.py:OMEGA"',
               '    source:     ""'),
           ["R26", "ROJO"])

# R26b — documentación stale: el valor declarado deja de ser el vigente.
# Es la otra mitad de la enfermedad (el docstring del MCMC de P2 que seguía
# diciendo que el sector 0.160 iba en la geometría).
expect_red("R26 procedencia: valor documentado ≠ recomputado → ROJO",
           "CANONICAL_VALUES.yaml",
           lambda t: t.replace("    value:      0.0224178",
                               "    value:      0.0229999"),
           ["R26", "ROJO"])

# R21b — el linaje de wₐ se rompe en el CÓDIGO (no en el .tex). Ésta es la
# mutación que representa la grieta hallada el 2026-07-25: como K_v e IGNIS son
# iguales bit a bit, ningún número cambia — sólo un check de linaje la caza.
expect_red("R21b código: script divide por K_v en vez de IGNIS → ROJO",
           "src/p02_mcmc/ssee_paper2_analysis.py",
           lambda t: t.replace("WA_SSEE = -P_sc / IGNIS", "WA_SSEE = -P_sc / KV", 1),
           ["R21b", "ROJO"])

# R27 — el diccionario crece y los papers quedan citando el denominador viejo.
# Ya pasó dos veces en la vida real (46→50→55 nombres); es el número que un
# referee hostil va a querer reproducir primero.
expect_red("R27 look-elsewhere: manuscrito cita 1-de-378 (denominador viejo) → ROJO",
           "manuscript/SSEE_Paper7_EFT.tex",
           lambda t: t + "\nThe target is unique: 1 of 378 ratios.\n",
           ["R27", "ROJO"])

# R28 — las dos copias del script del diccionario vuelven a derivar. Es la
# mutación de la falsa alarma del 2026-07-25: los valores coincidían (55/25/490)
# y aun así el código era distinto, con el denominador de wₐ equivocado en la
# copia del repo. Ningún check numérico podía verlo.
expect_red("R28 espejo: la copia del repo deriva del diccionario citable → ROJO",
           "src/estadistica/look_elsewhere_full.py",
           lambda t: t.replace("HERMES  = PHI + KAL", "HERMES  = PHI + KAL + 0.0", 1),
           ["R28", "ROJO"])

# R29 — la tabla de notación del PRD asigna un símbolo a la entidad equivocada.
# Es EL error de esta semana escrito en la tabla: K_v e I_g valen lo mismo
# (9.519253285), así que ningún check numérico puede distinguirlos — sólo la
# correspondencia símbolo↔entidad lo hace.
# R29 (columna φ,π) — la reducción a álgebra ordinaria deja de dar el valor.
# Esa columna existe para poder distinguir de un vistazo; si fuera decorativa
# —copiada y nunca verificada— la tabla mentiría justo donde promete transparencia.
expect_red("R29 notación: la reducción en φ,π no da el valor de su fila → ROJO",
           "submission_PRD/SSEE_PRD.tex",
           lambda t: t.replace(r"$2(\varphi+\pi)$            & $\val{K_V_d6}$",
                               r"$2(\varphi+3\pi)$           & $\val{K_V_d6}$", 1),
           ["R29", "ROJO"])

expect_red("R29 notación: la tabla del PRD llama IGNIS a K_v → ROJO",
           "submission_PRD/SSEE_PRD.tex",
           lambda t: t.replace("$K_v$       & KRYSTOS$_V$", "$K_v$       & IGNIS      ", 1),
           ["R29", "ROJO"])

# R30 — un valor mostrado deja de ser el redondeo correcto de su cantidad exacta.
# Es el caso real de 2026-07-25: Ω_m arrastraba un dígito de más en 157 sitios
# porque se redondeaba ω_m ANTES de dividir. Media unidad del último decimal es
# el umbral: 0.30889 dista 9.1e-6 de 0.308881, más de 5e-6.
expect_red("R30 redondeo: Ω_m mostrado ≠ redondeo correcto del exacto → ROJO",
           "submission_PRD/SSEE_PRD.tex",
           lambda t: t.replace(r"single matter density $\Omega_m=\omega_m/h^2=\val{OMEGA_M_TOTAL_d6}$",
                               r"single matter density $\Omega_m=\omega_m/h^2=0.30889$", 1),
           ["R30", "ROJO"])

# R30b — falsa precisión: una constante MEDIDA rellenada hasta el techo de 6
# decimales. Es el caso que planteó Mike: el número es finito, la regla de
# redondeo «no aplica» y de hecho la ATRAVIESA (|93.140000 − 93.14| = 0) mientras
# afirma cuatro decimales que ningún experimento midió.
expect_red("R30b falsa precisión: C_ν medido rellenado a 93.140000 → ROJO",
           "submission_PRD/SSEE_PRD.tex",
           lambda t: t.replace("93.14", "93.140000", 1),
           ["R30", "ROJO"])

# Escáner de valores retirados: un valor RETIRADO presentado como vigente
expect_red("memorias: valor retirado (ω_ν=0.000741) sin marcar → ROJO",
           "VERIFICATION_LEDGER.md",
           lambda t: t + "\n\nEl valor vigente de omega_nu es 0.000741 en toda la suite.\n",
           ["memoria", "ROJO"])


# ── R31: un .pyc RANCIO miente sobre el estado del core (caso especial) ──
# No es un replace de texto: hay que fabricar la condición. Se compila un core
# con el valor viejo, se restaura el fuente correcto y se falsifica el header
# del .pyc (mtime, size) para que Python lo dé por válido — exactamente lo que
# ocurrió dos veces el 2026-07-25, la segunda arruinando un MCMC de producción
# de 35 min que arrancó con Ω_m de la cadena rancia.
def test_bytecode_rancio():
    global _passed, _failed
    import importlib.util
    import py_compile
    import shutil
    import struct
    core = REPO / "src" / "ssee_core.py"
    orig = core.read_bytes()
    try:
        core.write_text(orig.decode().replace("SUM_MNU_EV = 0.06849",
                                              "SUM_MNU_EV = 0.06902", 1),
                        encoding="utf-8")
        py_compile.compile(str(core), doraise=True)
        core.write_bytes(orig)                     # fuente vuelve al correcto
        st = core.stat()
        pyc = pathlib.Path(importlib.util.cache_from_source(str(core)))
        d = bytearray(pyc.read_bytes())
        d[8:12] = struct.pack("<I", int(st.st_mtime))    # header: «soy válido»
        d[12:16] = struct.pack("<I", st.st_size)
        pyc.write_bytes(bytes(d))
        rc, out = run_guardian()
    finally:
        core.write_bytes(orig)
        shutil.rmtree(REPO / "src" / "__pycache__", ignore_errors=True)
    ok = rc != 0 and "R31" in out
    print(f"  [{'PASS' if ok else 'FALLA'}] R31 bytecode: .pyc rancio con header "
          f"falsificado → ROJO")
    _passed += ok
    _failed += (not ok)


test_bytecode_rancio()


# ── Archivo: cajón sin entrada en la Bitácora → ROJO (caso especial dir) ─
def test_archive_orphan():
    global _passed, _failed
    d = REPO / "archive" / "_test_orphan_dir"
    try:
        d.mkdir(exist_ok=True)
        rc, out = run_guardian()
    finally:
        if d.exists():
            d.rmdir()
    ok = rc != 0 and "archivo" in out
    print(f"  [{'PASS' if ok else 'FALLA'}] R12 archivo: cajón sin bitácora → ROJO")
    _passed += ok
    _failed += (not ok)


test_archive_orphan()

# ── Veredicto ───────────────────────────────────────────────────────────
print(f"\n{'='*55}")
total = _passed + _failed
if _failed:
    print(f"ROJO — {_failed}/{total} pruebas del vigilante FALLARON.")
    print("Un check del guardián se debilitó: arreglarlo antes de confiar en un VERDE.")
    sys.exit(1)
print(f"VERDE — el guardián detecta las {total} fallas simuladas. Vigilante íntegro.")
sys.exit(0)
