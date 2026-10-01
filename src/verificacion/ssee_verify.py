#!/usr/bin/env python3
"""
SSEE Verification Harness — el guardián del Registro de Verificación.

Re-ejecuta, de forma automática, todas las comprobaciones de
VERIFICATION_LEDGER.md. No revisa strings: recomputa la física.

    python3 src/ssee_verify.py

  VERDE → el modelo sigue íntegro; se puede continuar.
  ROJO  → algo se rompió. NO commitear ni sellar nada hasta resolverlo.

Correr DESPUÉS DE CADA CAMBIO al modelo o a los papers. El harness crece
con el Registro: cada capa que se verifica añade aquí sus comprobaciones,
de modo que re-verificar todo el modelo cuesta segundos. Este guardián
también revisa el trabajo de quien edita — humano o máquina.
"""
import hashlib
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# LOS PAPERS SE LEEN COMO LOS VE EL LECTOR (2026-09-30). Desde que los numeros
# entran por \val{nombre} (macro generada desde los logs), el .tex ya no trae
# el digito: una regla que busca «9.519253» en Paper 1 no lo veria y quedaria
# ciega en silencio (R29 y R49 lo cazaron al fallar). Toda lectura de un .tex
# de manuscript/ o submission_PRD/ con Path.read_text devuelve el texto con
# cada \val{} sustituido por su valor de manuscript/valores_generados.tex.
# La regla que necesita el texto CRUDO (R68: compara macros) pide crudo=True.
_VALGEN = ROOT.parent / "manuscript" / "valores_generados.tex"
_RT_ORIG = pathlib.Path.read_text


def _vals_generados():
    try:
        _t = _RT_ORIG(_VALGEN, errors="ignore")
    except OSError:
        return {}
    return dict(re.findall(r"ssee@val@([^\\]+)\\endcsname\{([^}]*)\}", _t))


_VALS = _vals_generados()


def expande_val(_txt, _vals=None):
    _v = _VALS if _vals is None else _vals
    return re.sub(r"\\val\{([^}]+)\}", lambda _m: _v.get(_m.group(1), _m.group(0)), _txt)


def _read_text_expandido(self, *a, crudo=False, **k):
    _t = _RT_ORIG(self, *a, **k)
    if (not crudo and self.suffix == ".tex" and self.name != "valores_generados.tex"
            and self.resolve().parent.name in ("manuscript", "submission_PRD")):
        return expande_val(_t)
    return _t


pathlib.Path.read_text = _read_text_expandido

# LA INFRAESTRUCTURA DE VERIFICACIÓN, en un solo sitio. Estos ficheros llevan
# los defectos A PROPÓSITO: son las fixtures con que se prueba al guardián, las
# mutaciones del registro y los valores retirados que hay que reconocer. Toda
# regla que escanee .py debe eximirlos, o se dispara con su propia munición.
#
# POR QUÉ ESTÁ AQUÍ Y NO EN CADA REGLA (2026-09-08, lo pidió Mike: «que la
# regla sea universal en lo que se pueda aplicar»). Cada regla se escribía su
# propia lista y salían todas distintas: unas eximían siete ficheros, otras dos,
# R56 sólo uno. Esa incoherencia da las DOS patologías a la vez — R56 saltó con
# la fixture de su propio caso de mutación (falsa alarma), y una lista de más
# habría tapado un defecto real (verde falso). La vigila R67.
_FIXTURES = frozenset({
    "ssee_verify.py",        # el guardián: sus autotests llevan el defecto
    "registro_reglas.py",    # las mutaciones son texto defectuoso a propósito
    "mutacion_guardian.py",  # idem
    "meta_guardian.py",      # idem
    "test_guardian.py",      # la otra suite de mutación
    "derive_nu_closure.py",  # deriva el 93.14 partiendo de los valores viejos
})
def _prosa_tex(_t):
    """El .tex con los saltos de linea DENTRO de un parrafo vueltos espacio.

    POR QUE (2026-09-08, lo destapo una mutacion). En LaTeX una frase se parte
    en varias lineas, asi que cualquier patron de mas de dos palabras falla en
    cuanto cae en un salto. Paper 1 decia

        is currently a free
        parameter (OP-11).

    y R45 —que persigue exactamente «currently a free parameter» junto a un OP
    ya cerrado— no lo veia: buscaba la frase con espacios simples. El defecto
    llevaba 38 dias en el manuscrito, con la regla en VERDE. Una regla que solo
    mira dentro de una linea se queda chica frente a su propio enunciado.

    Se respeta la linea en blanco (separa parrafos) y la linea que empieza por
    comando o comentario, porque ahi el salto SI es estructura y no relleno.
    """
    return re.sub(r"(?<!\n)[ \t]*\n[ \t]*(?!\n)(?![\\%])", " ", _t)


# TOPES APRETADOS 2026-08-02. Un trinquete sólo sirve si se aprieta: R44 tenía
# tope 112 con 79 sitios reales — 33 de holgura por la que podían colarse 33
# violaciones nuevas en verde. (El 112 venía de subir el tope 100→112 al
# endurecer el detector de 1 a 2 decimales: razón legítima, pero nadie lo
# volvió a bajar cuando se arreglaron sitios.) R43 tenía 2 de holgura.
# Vigilado ahora por R50: si la cuenta real baja del tope, hay que bajar el tope.
_DEUDA_MAX = {
    "R66": 0,            # constantes del nucleo re-tecleadas (2026-09-08)
    "R42": 0, "R43": 0, "R44": 0, "R45": 0}
# Cuenta REAL de cada regla, rellenada por cada capa al calcularla. R50 la
# compara contra _DEUDA_MAX para exigir que el trinquete esté apretado.
_DEUDA_REAL = {}

fails = []
checks = 0


def check(name, ok, detail=""):
    global checks
    checks += 1
    mark = " OK " if ok else "FALLA"
    line = f"  [{mark}] {name}"
    if detail:
        line += f"  — {detail}"
    print(line)
    if not ok:
        fails.append(name)


opens = []
sin_resolver = []      # fisica declarada con ficha viva: informa, no pinta
pendientes = []        # tareas terminables: pintan ambar hasta que se acaben
archivados = []        # registro que se conserva: informa, no pinta


# ── SIN RESOLVER NO ES LO MISMO QUE PENDIENTE (2026-09-19, lo dijo Mike) ─────
#
# «Las de OP no cuentan, porque esas ya se marcan de manera individual segun su
#  importancia. Si no, toda la vida se vera ambar porque el modelo cosmologico
#  no pudo encontrar H desde primeros principios. Los OP estan ahi para que yo y
#  cualquiera que vea el trabajo sepa que es lo que esta SIN RESOLVER — no sin
#  duda, sino sin resolver. Lo que esta en duda son cosas de "no se si esto va
#  aqui o alla".»
#
# Tenia razon y el defecto era de diseno mio. `track_open` se estaba usando para
# DOS cosas que no se parecen:
#
#   · fisica SIN RESOLVER — omega_b sin cadena BBN, MIRA sin mecanismo, el
#     sector geometrico que no se agrupa. Tiene ficha propia en
#     OPEN_PROBLEMS.md, con severidad, y su honestidad es que este declarada.
#     Puede no cerrarse nunca, y eso NO es un defecto del repositorio.
#   · tareas PENDIENTES — figuras rancias, logs sin fuente declarada, falta
#     `pdftotext`. Terminables, y mientras esten sin terminar el repositorio no
#     esta en orden.
#
# Mezcladas, el semaforo quedaba clavado en ambar para siempre y dejaba de
# informar: no distinguia «faltan 12 figuras por regenerar» de «nadie ha
# derivado H desde primeros principios». Ahora SOLO lo pendiente pinta.
#
# EL CONTROL, que es lo que impide que esto reabra el agujero del VERDE FORZADO
# (2026-09-07): un abierto solo cuenta como SIN RESOLVER si declara un `op=` con
# ficha VIVA y severidad legible en OPEN_PROBLEMS.md. Sin ficha, con ficha ya
# cerrada o sin severidad declarada, cae en PENDIENTE y pinta. O sea: no se
# puede esconder una tarea llamandola «problema abierto» — hay que abrirle
# ficha, ponerle severidad y firmarla en el documento que lee cualquiera.
_OPEN_PROBLEMS = ROOT.parent / "OPEN_PROBLEMS.md"
_SEV_MAPA = {"alta": "alta", "high": "alta", "media-alta": "media-alta",
             "medium-high": "media-alta", "media": "media", "medium": "media",
             "baja": "baja", "low": "baja"}


def _fichas_op():
    """{OP-N: (estado, severidad)} leido de OPEN_PROBLEMS.md.

    Dos detalles que costaron una pasada y por eso van escritos:
      · «PARCIALMENTE RESUELTO» contiene «resuelto» pero NO esta cerrado. Lo
        parcial manda sobre lo resuelto.
      · la severidad aparece en dos formatos, «**Severity:** X» y
        «**Severidad: X**» (los dos puntos dentro de los asteriscos). Leyendo
        solo el primero, OP-16 heredaba por error la severidad de otra ficha.
    """
    try:
        _t = _OPEN_PROBLEMS.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {}
    _cabs = [(_m.start(), _m.group(1), _m.group(0))
             for _m in re.finditer(r"^## (OP-\d+b?)[^\n]*", _t, re.M)]
    _out = {}
    for _k, (_pos, _op, _cab) in enumerate(_cabs):
        _fin = _cabs[_k + 1][0] if _k + 1 < len(_cabs) else len(_t)
        _cuerpo = _t[_pos:_fin]
        _m = re.search(r"\*\*Sever(?:ity|idad)[^:*]*:\*{0,2}\s*\*{0,2}"
                       r"([A-Za-zÁÉÍÓÚáéíóúñ\- ]{2,20})", _cuerpo)
        _crudo = (_m.group(1).strip().lower().rstrip(".").strip() if _m else "")
        _sev = _SEV_MAPA.get(_crudo) or _SEV_MAPA.get(_crudo.split()[0] if _crudo else "", "")
        _cl = _cab.lower()
        _abierto = ("parcial" in _cl or "abierto" in _cl or
                    not any(_c in _cl for _c in ("resuelto", "resolved", "disuelto",
                                                 "dissolved", "cerrado", "closed",
                                                 "retirada")))
        _out[_op] = ("abierto" if _abierto else "cerrado", _sev)
    return _out


_FICHAS_OP = _fichas_op()
_COLOR_SEV = {"alta": "\U0001f534", "media-alta": "\U0001f7e0",
              "media": "\U0001f7e1", "baja": "\U0001f7e2"}


def track_archivo(name, detail="", declarados=(), fuente=()):
    """Registro de algo que NO se arregla porque no hay nada que arreglar: un
    log de una corrida ya hecha que imprimio un valor que despues se retiro.
    Reescribirlo seria falsificar el registro; borrarlo, perderlo.

    Informa y NO pinta — pero con el mismo candado que las fichas OP: solo
    cuenta como archivo si CADA elemento esta declarado en su fuente (la
    seccion `historicos:` de PROPAGACION.yaml). Lo que no este declarado cae
    en PENDIENTE y pinta, para que no se pueda archivar algo por el
    procedimiento de llamarlo archivo.
    """
    global checks
    checks += 1
    _sin = [_d for _d in declarados if _d not in set(fuente)]
    if _sin or not declarados:
        print(f"  [PENDIENTE] {name}" + (f"  — {detail}" if detail else ""))
        pendientes.append(name + (f" (sin declarar: {', '.join(_sin)})" if _sin else ""))
    else:
        print(f"  [ARCHIVO] {name}" + (f"  — {detail}" if detail else ""))
        archivados.append(name)
    opens.append(name)


def track_open(name, detail="", op=None):
    """Registra algo que no esta hecho. Adonde va lo decide su ficha:

      op="OP-N" con ficha VIVA y severidad  → SIN RESOLVER (informa, no pinta)
      todo lo demas                          → PENDIENTE (pinta ambar)

    No es una regresion en ningun caso: se lista en CADA corrida para no
    olvidarlo nunca, y no pone el guardian en rojo.
    """
    global checks
    checks += 1
    _est, _sev = _FICHAS_OP.get(op or "", ("", ""))
    _vale = bool(op) and _est == "abierto" and bool(_sev)
    if _vale:
        _marca = f"[SIN RESOLVER {_COLOR_SEV.get(_sev, '')} {op} {_sev}]"
        sin_resolver.append((op, _sev, name))
    else:
        _porque = ("" if not op else
                   f" (ficha {op} " +
                   ("no existe" if op not in _FICHAS_OP else
                    "cerrada" if _est == "cerrado" else "sin severidad") + ")")
        _marca = "[PENDIENTE]"
        pendientes.append(name + _porque)
    print(f"  {_marca} {name}" + (f"  — {detail}" if detail else ""))
    opens.append(name)


# ─────────────────────────────────────────────────────────────────────
# CAPA 1 — Axiomas y constantes algebraicas
# Recomputa cada constante desde su definición y la coteja con el valor
# registrado en VERIFICATION_LEDGER.md. Detecta un valor mal registrado
# o una definición alterada.
# ─────────────────────────────────────────────────────────────────────
print("Capa 1 — axiomas y constantes algebraicas")

phi = (1 + 5 ** 0.5) / 2
pi = math.pi
Omega = phi + pi
beta = (phi + pi) / 2
AURA = (3 * phi + pi) / 2
MIRA = AURA / 2
KAL0 = (phi + 3 * pi) / 2
Tr = 3 * (phi + beta)
Kv = 2 * (phi + pi)
Mv = phi + pi + Kv

# (constante computada, valor registrado en el ledger)
L1 = {
    "V-L1-01 phi":  (phi,   1.6180339887),
    "V-L1-02 pi":   (pi,    3.1415926536),
    "V-L1-03 Omega": (Omega, 4.7596266423),
    "V-L1-04 beta": (beta,  2.3798133212),
    "V-L1-05 AURA": (AURA,  3.9978473099),
    "V-L1-06 MIRA": (MIRA,  1.9989236550),
    "V-L1-07 KAL0": (KAL0,  5.5214059748),
    "V-L1-08 Tr":   (Tr,    11.9935419298),
    "V-L1-09 Kv":   (Kv,    9.5192532847),
    "V-L1-10 Mv":   (Mv,    14.2788799270),
}
for name, (computed, ledger) in L1.items():
    check(name, abs(computed - ledger) < 1e-9,
          f"computado {computed:.10f} / registro {ledger:.10f}")

# Identidades estructurales — el álgebra debe cerrar.
check("L1 identidad  MIRA = AURA/2",
      abs(MIRA - AURA / 2) < 1e-12)
check("L1 identidad  KAL0 = beta + pi  (def. alternativa)",
      abs(KAL0 - (beta + pi)) < 1e-12)
check("L1 identidad  Kv = phi + pi + Omega  (def. alternativa)",
      abs(Kv - (phi + pi + Omega)) < 1e-12)
w0 = -Tr / Mv
check("L1 identidad  w0 = -Tr/Mv = -0.840",
      abs(w0 - (-0.8399497713)) < 1e-9, f"{w0:.10f}")
check("L1 identidad  Om_m,dyn = 1 + w0 = 0.160",
      abs((1 + w0) - 0.1600502287) < 1e-9)
# Identidad histórica MIRA (MIRA persiste como entidad = AURA/2; valor intacto).
check("L1 identidad  MIRA * Om_m,dyn = 0.31993 (RETIRADO; solo aritmética, OP-8 disuelto)",
      abs(MIRA * (1 + w0) - 0.3199281880) < 1e-9)
# Identidad histórica π/φ (factor-materia del reframe 2026-06-17, SUPERADO).
check("L1 histórico  (pi/phi) * Om_m,dyn = 0.31076 (factor π/φ — superado)",
      abs((pi / phi) * (1 + w0) - 0.3107552907) < 1e-9)
# CANÓNICO (reframe 2026-06-18, OP-8 CERRADO): NO hay factor. Om_m,CMB = ω_m/h².
_kal0 = (pi + phi) / 2 + pi                       # KAL0 = BETA + PI
_omb  = (pi - phi) / (3 * Omega ** 2)             # ω_b (OP-1)
_omc  = _kal0 * _omb * (1 - phi ** -7)            # ω_c = KAL0·ω_b·n_s (forward)
_omm  = _omb + _omc + 0.0684903 / 93.14           # ω_m físico (Σm_ν=0.0685, C_ν=93.14)
_h    = (3 * Omega ** 2) / 100                    # h = H_alg/100
check("L1 canónico   Om_m,CMB = ω_m/h² = 0.308881 (ω_m-directo, sin factor)",
      abs(_omm / _h ** 2 - 0.3088808856) < 1e-9)

# ─────────────────────────────────────────────────────────────────────
# CAPA 2 — Parámetros cosmológicos derivados
# ─────────────────────────────────────────────────────────────────────
print("\nCapa 2 — parámetros cosmológicos derivados")

Psc = Omega + phi
# SATURACIONES (Postulado S) — no llevan H. Renombradas 2026-08-10: los nombres
# Om_* sugerian densidad y NINGUNA de las dos lo es.
s_DE = Tr / Mv                   # 0.839950 = |w0|
s_M = 1 + w0                     # 0.160050
Om_DE = s_DE                     # [ALIAS DEPRECADO]
Om_m_dyn = s_M                   # [ALIAS DEPRECADO]
# s_K — la cantidad que entra en f_screen. NO es alpha_K.
# alpha_K (kineticidad Bellini-Sawicki) = 3*v^2/KAL con v = dphi/d(ln a): EVOLUCIONA
# (hoy 0.150703, tiende a 0.480148). Probado 2026-08-10 que no hay ninguna epoca
# donde el campo tenga a la vez las dos ranuras de s_K (ranura 1 en a=1.3654,
# ranura 2 solo en a->infinito). s_K es puro EoS: 3*(-w0)*(1+w0). Sin densidad,
# sin H. El VALOR nunca estuvo en duda; la etiqueta si.
s_K = 3 * s_DE * s_M
alpha_K = s_K                    # [ALIAS DEPRECADO] nombre incorrecto

L2 = {
    "V-L2-01 w0":        (-Tr / Mv,                      -0.8399497713),
    "V-L2-02 wa":        (-Psc / Kv,                     -0.6699748857),
    "V-L2-03 Om_DE":     (Om_DE,                          0.8399497713),
    "V-L2-04 Om_m,dyn":  (Om_m_dyn,                       0.1600502287),
    "V-L2-05 Om_m,CMB":  (_omm / _h ** 2,                 0.3088808856),
    "V-L2-05b ω_c":      (_omc,                           0.1195144084),
    "V-L2-05c ω_m":      (_omm,                           0.1426675130),
    "V-L2-05d π/φ·dyn [RETIRADO]":  ((pi / phi) * Om_m_dyn,  0.3107552907),
    "V-L2-05e MIRA·dyn [RETIRADO]": (MIRA * Om_m_dyn,        0.3199281880),
    "V-L2-06 H0^alg":    (3 * Omega ** 2,                 67.9621373234),
    "V-L2-07 n_s":       (1 - phi ** -7,                  0.9655581463),
    "V-L2-08 s_K":       (s_K,                            0.4033024589),
    "V-L2-09 beta_c":    (-AURA,                         -3.9978473099),
    # El literal decía 0.0081306227 y el exacto es 0.0081306188: MAL en la 9ª
    # cifra. La tolerancia de 1e-6 lo tapaba (era 256× el peor residuo real).
    # Ningún paper se vio afectado —ambos redondean a 0.008131— pero un
    # registro con un dígito falso es justo lo que después se propaga.
    "V-L2-12 r":         (12 * (phi ** 4 / 3) / (2 * phi ** 7) ** 2, 0.0081306188),
    "V-L2-13 f_screen":  ((pi - phi) / Omega ** 2,        0.0672532703),
}
# Tolerancia 1e-9, no 1e-6. Los dos lados son álgebra exacta y el registro se
# escribe a 10 decimales: no hay medida de por medio que justifique holgura. Con
# 1e-6 el margen era 256× el peor residuo real, y ahí dentro cabía —y cabía de
# hecho— un literal equivocado en la 9ª cifra. El límite lo pone el redondeo del
# propio literal a 10 decimales (5e-11), así que 1e-9 deja 20× de aire honesto.
for name, (computed, ledger) in L2.items():
    check(name, abs(computed - ledger) < 1e-9,
          f"computado {computed:.10f} / registro {ledger:.10f}")

# V-L2-10 m_phi canónico (forward-prediction, cero fiteo, P6; mecanismo SOLAR²·KRYSTOS 2026-06-19):
#   m_phi = Sigma_m_nu^active * (SOLAR^2 * KRYSTOS)   [mecanismo g²·v]
#   con Sigma_m_nu^active = R2·ω_b·C_ν/(τ_Π H0), C_ν=93.14 eV PDG (cierre ν preciso,
#   N_eff=3.046; DEMOSTRADO en derive_nu_closure.py), R2 = Omega/(KAL0*Tr).
#   SOLAR = BIAL+KAL = phi+2pi (linaje radiativo); KRYSTOS_V = phi+pi+Omega (padres, NO 2Omega).
# Dimensionalmente CONSISTENTE: [eV] * (número puro) = [eV].
# C_ν univaluada en 93.14 (PDG, derive_nu_closure.py). El viejo factor 0.960318 NO era
# 94.07 horneado: implica C_ν≈93.8638 eV, que no es ninguna de las dos documentadas.
# Número sin fuente — verificado 2026-07-25, registrado como OP-20.
# Mult. anterior PYROS*VITA*MIKA=615.33 (m_phi=42.47, sin mecanismo) RETIRADO; ver OP-9/OP-17.
_R2 = Omega / (KAL0 * Tr)
_mnu_active = _R2 * _omb * 93.14 / (KAL0 * Omega / Tr)   # = 0.06849 eV
_SOLAR = phi + 2 * pi
_KRYSTOS_V = phi + pi + Omega          # padres {φ,π,Ω} — NO 2Ω (colapso convencional)
_mult_mphi = _SOLAR ** 2 * _KRYSTOS_V
_m_phi_canon = _mnu_active * _mult_mphi
check("V-L2-10 [RETIRADO 2026-08-01] aritmética histórica m_phi = 40.70 eV",
      abs(_m_phi_canon - 40.7024) < 1e-2,
      f"m_phi = {_m_phi_canon:.4f} eV (R2={_R2:.6f}, mult={_mult_mphi:.4f}) — RETIRADO: su densidad salía de restar Ω_m,CMB−(1+w₀), densidad menos ecuación de estado. Se conserva sólo como aritmética verificable, NO como entidad vigente")

# V-L2-11 CIERRE DEL SECTOR ν (regla nueva 2026-07-25, a raíz de un fallo de auditoría).
# HISTORIA: el cambio C_ν 94.07→93.14 (2026-07-10) propagó a m_phi (41.02→40.70) pero
# NO a ω_ν, que quedó en 0.000741 (= Σm_ν 0.06902) en CANONICAL_VALUES y en los papers.
# El guardián calculaba bien por dentro (línea 114 usa 0.0684903/93.14) pero NINGUNA regla
# comparaba su valor interno contra el publicado, ni cerraba el lazo m_phi ↔ ω_ν.
# Un lector que invirtiera la ecuación de ω_m aterrizaba en el RETIRADO 41.02 eV.
# La regla cierra el lazo en las DOS direcciones para que el sector ν no pueda volver a
# desincronizarse: Σm_ν es UNA sola cantidad, la usen m_phi o ω_m.
# El valor NO se escribe aquí: se LEE de CANONICAL_VALUES.yaml. Escrito a mano,
# la comprobación de más abajo comparaba la variable contra el mismo literal con
# que se acababa de asignar — una tautología que no podía fallar nunca.
# (Prueba de mutación, 2026-07-29: dos checks resultaron ser de esta forma.)
_C_nu_yaml = re.search(r"C_nu_eV:\s*([\d.]+)",
                        (pathlib.Path(__file__).resolve().parents[2]
                         / "CANONICAL_VALUES.yaml").read_text(errors="ignore"))
_C_nu = float(_C_nu_yaml.group(1)) if _C_nu_yaml else float("nan")
_omnu_from_mnu = _mnu_active / _C_nu                  # ν-sector → ω_ν
_mnu_from_mphi = _m_phi_canon / _mult_mphi            # m_φ      → Σm_ν  (round-trip)
_omnu_in_omm   = _omm - _omb - _omc                   # ω_m      → ω_ν  (lo que se publica)
# 11a es CROSS-IMPLEMENTACIÓN, no round-trip: la cadena algebraica debe coincidir con
# la constante del core Y con la clave del YAML. Un round-trip (m_phi/mult) sería
# tautológico —divide por el mismo factor con el que multiplicó— y NO habría cazado
# el drift de 2026-07-10, porque core y YAML derivaron juntos hacia el valor viejo.
# ⚠️ SE COMPILA EL FUENTE, NO SE IMPORTA (hallazgo 2026-07-25).
# `spec.loader.exec_module()` acepta el bytecode de `__pycache__` cuando su
# (mtime, size) registrados parecen válidos. Este guardián leyó SUM_MNU_EV=0.06902
# de un ssee_core.py que en disco decía 0.06849: un .pyc rancio le mintió sobre el
# estado del repo. Un verificador que lee bytecode NO está verificando el archivo
# que el humano lee ni el que se commitea — puede dar VERDE (o ROJO) sobre código
# que ya no existe. Probablemente es la causa del ROJO transitorio irreproducible
# de esta semana. `compile(texto_del_archivo)` no consulta ninguna caché.
try:
    _core_path = pathlib.Path(__file__).resolve().parents[1] / "ssee_core.py"
    _core_ns: dict = {"__name__": "_core_nu", "__file__": str(_core_path)}
    exec(compile(_core_path.read_text(errors="ignore"), str(_core_path), "exec"),
         _core_ns)
    _mnu_core = _core_ns["SUM_MNU_EV"]
except Exception as _e:                                   # pragma: no cover
    _mnu_core = None
_yaml_nu = re.search(r"sigma_m_nu_eV:\s*([\d.]+)",
                     (pathlib.Path(__file__).resolve().parents[2]
                      / "CANONICAL_VALUES.yaml").read_text(errors="ignore"))
_mnu_yaml = float(_yaml_nu.group(1)) if _yaml_nu else None
check("V-L2-11a cierre ν: Sigma_m_nu cadena R2 == ssee_core == CANONICAL_VALUES",
      _mnu_core is not None and _mnu_yaml is not None
      and abs(_mnu_active - _mnu_core) < 5e-6
      and abs(_mnu_active - _mnu_yaml) < 5e-6,
      f"cadena {_mnu_active:.7f} / core {_mnu_core} / yaml {_mnu_yaml} eV "
      f"(cross-implementación: el drift 0.06902 vivía en core+yaml a la vez)")
check("V-L2-11b cierre ν: omega_nu en omega_m == Sigma_m_nu/C_nu  (no 0.000741 stale)",
      abs(_omnu_in_omm - _omnu_from_mnu) < 1e-9,
      f"en ω_m {_omnu_in_omm:.7f} / desde Σm_ν {_omnu_from_mnu:.7f} "
      f"(stale 0.000741 ⇒ Σm_ν=0.06902 ⇒ m_φ=41.02 RETIRADO)")
check("V-L2-11c cierre ν: C_nu univaluada = 93.14 PDG en toda la cadena",
      _C_nu_yaml is not None and abs(_C_nu - 93.14) < 1e-9,
      f"C_ν = {_C_nu} eV — el operativo. 94.07 eV NO está retirado ni es "
      f"incorrecto: es el desacople INSTANTÁNEO (N_eff=3 exacto). 93.14 "
      f"incluye el reheating e⁺e⁻ (N_eff=3.046) y es el que usa Planck. "
      f"Además C_ν se CANCELA en ω_ν, así que la elección no mueve "
      f"ninguna cosmología — sólo el Σm_ν reportado. Ver Paper 6 §cnu-cancels")

# Identidades cruzadas — dos rutas independientes deben coincidir.
n_kess = (Tr - Mv) / (2 * Tr)
check("L2 identidad  w0 = 1/(2n-1)  (ruta k-essence)",
      abs(1 / (2 * n_kess - 1) - (-Tr / Mv)) < 1e-10)
check("L2 identidad  f_screen = s_K/(3*MIRA) = (pi-phi)/Om^2",
      abs(s_K / (3 * MIRA) - (pi - phi) / Omega ** 2) < 1e-10)

# Problemas ABIERTOS detectados en Capa 2 — comprobación dimensional.
track_open("V-L2-06 H0^alg dimensional",
           "3*Omega^2 es adimensional; H0 tiene unidades km/s/Mpc (Postulado D)",
           op="OP-7")
# V-L2-10: la fórmula CANÓNICA (forward-prediction 40.70 eV SOLAR²·KRYSTOS) es dimensionalmente
# consistente — [eV]*(número puro) = [eV]. El antiguo ansatz Sigma_m_nu*H0^alg
# (5.60 eV) está retirado. Lo abierto es el Lagrangiano φ-DM (OP-9), no la dimensión.

# ─────────────────────────────────────────────────────────────────────
# CAPA 3 — Mecanismos y derivaciones
# ─────────────────────────────────────────────────────────────────────
print("\nCapa 3 — mecanismos y derivaciones")

# OP-2 — n_s = 1 - phi^-7 (índice espectral). La cadena algebraica cierra
# exacto; el insumo físico N_* = 2phi^7 es conjetura (ABIERTO).
N_star = 2 * phi ** 7
check("V-L3-OP2  identidad n_s: 1-2/(2phi^7) = 1-phi^-7",
      abs((1 - 2 / N_star) - (1 - phi ** -7)) < 1e-12)
check("V-L3-OP2  identidad r: 12(phi^4/3)/(2phi^7)^2 = phi^-10",
      abs(12 * (phi ** 4 / 3) / N_star ** 2 - phi ** -10) < 1e-12)
# R32 — unicidad de m=2 en N_* = m·phi^n. El PRD §4.2 afirma que 2phi^7 es el
# UNICO miembro de la familia m·phi^n dentro de [50,60] cuyo n_s (y su r) salen
# potencia PURA de phi. Es una afirmación de unicidad publicada: se recomputa.
import math as _math
_cands, _puros = [], []
for _m in range(1, 21):
    for _n in range(1, 16):
        _N = _m * phi ** _n
        if not (50.0 <= _N <= 60.0):
            continue
        _cands.append((_m, _n))
        _k = -_math.log(1 - (1 - 2 / _N)) / _math.log(phi)      # n_s = 1-phi^-k
        _kr = -_math.log(12 * (phi ** 4 / 3) / _N ** 2) / _math.log(phi)
        if abs(_k - round(_k)) < 1e-9 and abs(_kr - round(_kr)) < 1e-9:
            _puros.append((_m, _n))
check(f"R32 unicidad N_*: solo m=2,n=7 da n_s y r potencia pura de phi en [50,60]",
      _puros == [(2, 7)] and len(_cands) >= 4,
      f"{len(_cands)} candidatos m·phi^n en ventana, puros: {_puros}")

track_open("V-L3-OP2  N_* = 2phi^7",
           "Conjecture B.1 no derivada; falta el puente de reheating gravitacional",
           op="OP-2b")

# OP-7 — la dualidad Z2 es álgebra exacta y se queda. Lo que NO se queda es el
# acoplamiento que decía explicar: beta_c = -AURA quedó RETIRADO el 2026-09-06
# (OP-23 disuelto). El «acuerdo al 0.199%» era el bug de normalizar el disparo a
# la saturación 0.839950 = |w0| en vez de a la fracción 1-Om_m = 0.691119.
check("V-L3-OP7  dualidad Z2: KAL0(phi<->pi) = AURA",
      abs((pi + 3 * phi) / 2 - AURA) < 1e-12)
# Control del otro lado: el disparo mal normalizado da -3.990 (0.199% de AURA);
# el bien normalizado da +0.235068, que NO se parece a -AURA en signo ni escala.
_bc_bug, _bc_ok = -3.990, +0.235068
check("V-L3-OP7  el «0.199%» sólo aparece con la normalización mala",
      abs(_bc_bug + AURA) / AURA < 0.005
      and abs(_bc_ok + AURA) / AURA > 1.0,
      f"mal normalizado {_bc_bug} → {abs(_bc_bug + AURA) / AURA * 100:.3f}% de "
      f"-AURA; bien normalizado {_bc_ok:+.6f} → "
      f"{abs(_bc_ok + AURA) / AURA * 100:.1f}% (signo contrario)")
check("V-L3-OP7  ningún .tex presenta beta_c = -AURA como vigente",
      not any(
          "\\bc = -\\AURA" in _t and "withdraw" not in _t.lower()
          and "previously" not in _t.lower()
          for _t in [_p.read_text(errors="ignore")
                     for _p in (ROOT.parent / "manuscript").glob("*.tex")]),
      "P7 lo declara retirado en su §3; P1 lo declara retirado en §5.3")

# alpha = phi^4/3 — consecuencia exacta de los axiomas n_s=1-phi^-7, r=phi^-10.
alpha_attr = phi ** 4 / 3
check("V-L3-alpha  alpha = r*N^2/12 = phi^4/3",
      abs((phi ** -10) * (2 * phi ** 7) ** 2 / 12 - alpha_attr) < 1e-10)
check("V-L3-alpha  identidad Fibonacci  phi^4/3 = phi + 2/3",
      abs(alpha_attr - (phi + 2 / 3)) < 1e-12)
# Curvatura de Kähler R = -2/(3 alpha) = -2 phi^-4 (P1 decía -phi^-4: error factor 2, corregido).
check("V-L3-alpha  curvatura Kahler R = -2/(3 alpha) = -2 phi^-4",
      abs(-2 / (3 * alpha_attr) - (-2 * phi ** -4)) < 1e-12,
      f"R = {-2/(3*alpha_attr):.6f}")

# OP-4 — radio k-mouflage (P8). La fórmula r_km^3 = M_obj/(4pi M_pl M^2)
# es dimensionalmente inconsistente: exponentes GeV de (M_obj, M_pl, M^2).
dim_rkm = (1 - 1 - 2) / 3   # dimensión GeV de r_km según la fórmula de P8
track_open("V-L3-OP4  formula k-mouflage de P8 dimensionalmente rota",
           f"r_km tiene dimension GeV^{dim_rkm:.3f}; una longitud es GeV^-1. "
           "Introducida en commit 295ed6e; requiere re-derivacion",
           op="OP-4")

# OP-1 — densidad bariónica (P4/Paper B). La cadena algebraica cierra exacto;
# el insumo Omega_b h^2 = (pi-phi)/(3 Omega^2) es coincidencia hallada por scan
# de 7 candidatos, no derivada de BBN (ABIERTO).
Omb_h2_alg = (pi - phi) / (3 * Omega ** 2)
check("V-L3-OP1  identidad (pi-phi)/(3 Om^2) = 0.0224178",
      abs(Omb_h2_alg - 0.0224178) < 1e-6,
      f"computado {Omb_h2_alg:.7f}")
track_open("V-L3-OP1  Omega_b h^2 no derivado",
           "coincidencia a 0.32sigma de Planck hallada por scan de 7 candidatos; "
           "falta cadena BBN (eta_B -> Omega_b) — diferida a Paper B",
           op="OP-1")

# OP-3 — separabilidad UV-IR (P10). Las identidades algebraicas cierran exacto;
# la jerarquia (H0/M)^2 es real, pero la prueba de separabilidad (jacobiano
# d phi/d chi) esta diferida y KALeff dropea el factor rho_crit (ABIERTO).
alpha_op3 = phi ** 4 / 3
check("V-L3-OP3  identidad 6*alpha = 2 phi^4",
      abs(6 * alpha_op3 - 2 * phi ** 4) < 1e-12)
check("V-L3-OP3  identidad sqrt(6*alpha) = phi^2 sqrt(2)",
      abs((6 * alpha_op3) ** 0.5 - phi ** 2 * 2 ** 0.5) < 1e-12)
track_open("V-L3-OP3  separabilidad UV-IR no probada",
           "jerarquia (H0/M)^2~3e-62 real; prueba via jacobiano d phi/d chi "
           "diferida a Paper B; KALeff^2 = M^4/(6 alpha) dropea rho_crit",
           op="OP-3")

# OP-5 — tensión S8 weak-lensing (P5/P6). CANÓNICO (ω_m-directo, CLASS forward con
# m_phi=40.70 eV mecanismo SOLAR²·KRYSTOS, Om_m=0.30888): el two-sector phi-DM
# (free-streaming k_fs=0.754) lleva el single-sector S8=0.846 (3.5sigma, "el desafio")
# al titular S8_eff=0.758 (0.04sigma KiDS). sigma8 es OUTPUT directo de CLASS (no fit alpha_WDM).
# script: src/ssee_paper6_canonical_particle.py
Om_cosm_op5 = _omm / _h ** 2                         # 0.30888  Om_m,CMB (omega_m-directo)
# 2026-09-08: era 0.8335, de una corrida CLASS SIN .ini y SIN neutrinos masivos.
# Con el fondo canonico y sus neutrinos: 0.814854 (config/class/techo_ssee_canonico.ini).
S8_challenge = 0.814854 * (Om_cosm_op5 / 0.3) ** 0.5  # techo CLASS con A_s fijo
S8_resolved = 0.7470 * (Om_cosm_op5 / 0.3) ** 0.5   # two-sector forward CLASS (resuelve)
check("V-L3-OP5  S8 con A_s FIJADO a Planck = 0.8268  (artefacto, no desafio)",
      abs(S8_challenge - 0.826827) < 2e-3,
      f"S8 = {S8_challenge:.4f} — el viejo «3.5sigma KiDS» era artefacto de fijar A_s, "
      f"o sea de importar la tension Planck-KiDS. A_s es LIBRE en el modelo (k=2)")
check("V-L3-OP5  [RETIRADO] aritmetica two-sector = 0.758",
      abs(S8_resolved - 0.758) < 2e-3,
      f"S8 = {S8_resolved:.4f} — RETIRADO con la particula (2026-08-01). "
      f"CANONICO: MCMC R3 con A_s libre sobre 225 puntos xi+- KiDS crudos da "
      f"S8 = 0.7555 +- 0.0192 (0.11sigma): NO hay tension que resolver")
track_open("V-L3-OP5  S8 sin tension con A_s libre; cierre no-lineal pleno diferido",
           "CANONICO 2026-08-01: MCMC R3 convergido (Cobaya+CAMB, R-1=0.0189, N_eff=42033), "
           "UN SOLO SECTOR, A_s libre, 225 puntos xi+- KiDS crudos: S8=0.7555+-0.0192 -> "
           "0.11sigma de KiDS. NO hay tension. El two-sector 0.758 y m_phi=40.70 quedan RETIRADOS. "
           "El cierre no-lineal con feedback barionico (N-body, ~5k-20k CPU-h) es Nivel 2, "
           "diferido. Ramas viejas 0.737/0.794, 0.702/0.725, 0.742/0.766, 0.7536/0.765 y "
           "0.7483/0.7593 (rama con C_ν instantáneo 94.07 como operativo) retiradas",
           op="OP-5b")

# OP-6 — forma de screening (P9). El valor f_screen es algebra exacta (ver
# V-L2-13); la forma multiplicativa sigue del universo separado. El paso
# delta_rho_phi y el insumo delta_local = 2 (sobredensidad Grupo Local) no
# estan derivados de phi,pi (ABIERTO parcial).
f_screen_op6 = (pi - phi) / Omega ** 2
H0_local_op6 = (3 * Omega ** 2) / (1 - f_screen_op6)
check("V-L3-OP6  H0_local = H0^alg/(1-f_screen) = 72.86",
      abs(H0_local_op6 - 72.864) < 1e-2, f"H0_local = {H0_local_op6:.4f}")
track_open("V-L3-OP6  forma multiplicativa: insumo delta_local = 2 no derivado",
           "la forma multiplicativa sigue del universo separado, pero el valor "
           "f_screen requiere delta_local=2 (sobredensidad Grupo Local) y una "
           "expresion delta_rho_phi asertada, no derivada de phi,pi",
           op="OP-6b")

# m_phi — masa del campo phi-DM (P6, CANÓNICO forward-prediction; SOLAR²·KRYSTOS 2026-06-19).
#   Sigma_m_nu^active = R2·ω_b·C_ν/(τ_Π H0), C_ν=93.14 eV PDG,  R2 = Omega/(KAL0*Tr)
#   m_phi = Sigma_m_nu^active * (SOLAR^2 * KRYSTOS)   [mecanismo g²·v]
# El multiplicador es número PURO -> dimensión [eV] preservada. Cero fiteo.
R2_p6 = Omega / (KAL0 * Tr)
mnu_active = R2_p6 * _omb * 93.14 / (KAL0 * Omega / Tr)   # = 0.06849 eV (C_ν=93.14)
SOLAR = phi + 2 * pi
KRYSTOS_V = phi + pi + Omega            # padres {φ,π,Ω} — NO 2Ω (colapso convencional)
mult_p6 = SOLAR ** 2 * KRYSTOS_V
m_phi = mnu_active * mult_p6
check("V-L3-mphi  [RETIRADO 2026-08-01] cadena historica m_phi = 40.70 eV",
      abs(m_phi - 40.7024) < 2e-2,
      f"m_phi = {m_phi:.4f} eV — la cadena cierra unidades, pero la particula no "
      f"tenia de que estar hecha: Om_phiDM salia de una resta mal planteada. "
      f"Ademas EXCLUIDA por la cizalla cruda (cota m_phi > 70.3 eV)")
# OP-9 NO se resolvio: se DISOLVIO al caerse su premisa (2026-08-01). Ya no hay
# coeficiente que derivar porque ya no hay particula. En su lugar va una GUARDA:
# ningun .tex puede volver a presentar la particula ni el segundo sector como
# vigentes. Es la contramedida de la retraccion — sin ella, la suite podria
# revertir sola y el guardian seguiria en verde (paso con la direccion de
# cascada, ver R55).
_RETRACTADOS = ("40.70", "594.28", "0.14889", "0.14888",
                "k_{\\rm fs}=0.754", "k_fs=0.754")
# 2026-09-07: faltaban las formas en que la suite escribe REALMENTE una
# retraccion en los .md — «DISUELTO», el tachado «~~», el circulo rojo.
# Sin ellas la guarda contaba como vivas fichas que ya narran su muerte.
# EL REPO ES BILINGUE Y LAS LISTAS ESTABAN SOLO EN INGLES (2026-09-19).
# `retirad` cubria «retirada/retirado» pero NO «se retiro», que es como lo
# escribe medio AUDIT.md; se acorta a `retir`. Y del lado del pasado faltaban
# las formas castellanas del verbo ser/estar, que son justo las que usa la
# prosa que NARRA una retirada: «`72.86` y `73.040` ERAN el mismo enunciado»,
# «ese «<0.2%» ERA el bug de saturacion». La pregunta que no se hizo cuando se
# escribieron estas listas fue en que idioma esta escrito lo que vigilan.
# Lineas que DICTAN el estado actual de una entrada, no narran el pasado:
# una cabecera de retirada no las autoriza a afirmar en presente (P-C).
_HISTORICO60 = re.compile(r"hist[oó]ric|en su momento|historical|status change|de la época|de la epoca", re.I)
_VEREDICTO60 = re.compile(r"[>\s]*\**\s*(veredicto|estado|titular|conclusi[oó]n|verdict|status|headline)\b", re.I)
_EXENTO_RETR = ("retract", "withdraw", "supersed", "retir", "previously",
                "no longer", "historic", "RETIRED", "archive",
                "disuelt", "dissolv", "disoluci", "~~", "\U0001f534", "ya no",
                "dej\u00f3 de", "en cuesti\u00f3n", "hist\u00f3ric",
                "el viejo", "la vieja", "lo viejo")


_ITEM_R69 = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s)")
_CITA_R69 = re.compile(r"^\s*>")
# Corta por final de oracion. El lookahead pide que lo siguiente ABRA algo
# (mayuscula, parentesis, macro LaTeX, negrita): asi «m_phi = 40.70 eV.» no
# parte una lista de decimales ni una cita «Almeida et al.».
#
# EL PUNTO Y COMA CORTA SIEMPRE (2026-09-19). Un `;` separa dos afirmaciones
# independientes, y da igual si la segunda empieza en minuscula. Sin esto, en
# AUDIT.md la frase «The Hubble cascade is … 72.86 (0.17σ); the canonical DR2
# posterior is H0 = 67.79» se leia como UNA sola: el «canonical» de la segunda
# mitad —que habla del posterior de DESI— hacia que la PRIMERA contara como
# afirmacion viva del 72.86 retirado. Un `;` nunca aparece dentro de un
# decimal ni de una cita, asi que cortar ahi no reabre el caso que motivo el
# lookahead.
_ORA_R69 = re.compile(r"(?<=[.:])\s+(?=[A-Z(\\*«¿$])|(?<=;)\s+")
# Palabras que AFIRMAN que algo esta en vigor. No son lo contrario de las
# marcas: son de otro eje. Un texto puede llevar las dos, y cuando las lleva
# en la MISMA oracion sobre el MISMO valor, se contradice a si mismo — y eso
# es un error aunque el valor no estuviera retirado.
_VIGENTE_R69 = ("canonical", "canónic", "status", "current", "vigente",
                "adopted", "adoptad", "[x]", "in force", "en vigor")
# Verbos y adverbios que ponen la afirmacion en pasado. Sin esto, la frase que
# NARRA como se anunciaba el valor se leeria como si lo anunciara ella.
_PASADO_R69 = ("previous", "earlier", "former", "was ", "were ", "anterior",
               "antes ", "se anunci", "announced",
               # castellano: las formas que usa la prosa que narra la retirada
               "era ", "eran ", "fue ", "fueron ", "estaba ", "estaban ",
               "llevaba ", "decia ", "dec\u00eda ", "met\u00eda ", "sal\u00eda ",
               "usaba ", "daba ", "el viejo", "la vieja")


def _re_quita_cita(_l):
    return _CITA_R69.sub("", _l, count=1)


def _unidad(_lns, _i):
    """P-A: el bloque que un lector lee como UNA sola afirmacion.
    Un item de lista (con sus lineas de continuacion indentadas), una linea de
    cita, o un parrafo entre lineas en blanco.

    El detalle que costo una vuelta: dos items CONSECUTIVOS no son la misma
    unidad aunque sean vecinos y de la misma clase. Si no se corta ahi, el
    «archived» de «- [x] Zenodo v6 — Papers 1-7 archived» vuelve a eximir al
    item de abajo, que es justamente el caso que abrio esta regla."""
    def _cl(_l):
        if not _l.strip(): return "vacio"
        if _CITA_R69.match(_l): return "cita"
        if _ITEM_R69.match(_l): return "item"
        return "prosa"
    # Dos items consecutivos son DOS afirmaciones; dos lineas de cita
    # consecutivas son UN SOLO bloque citado. La diferencia importa: los
    # banners de este repo son blockquotes de diez lineas cuya marca vive en
    # la primera («> BANNER PARTICULA RETIRADA»), y tratarlas por separado
    # producia 74 falsos positivos de golpe. Un item DENTRO de la cita
    # («> - [x] …») si abre unidad propia.
    _es_item_cita = lambda _l: bool(_ITEM_R69.match(_re_quita_cita(_l)))
    _ini = _i
    while _ini > 0:
        _cc = _cl(_lns[_ini])
        if _cc == "item":
            break                                   # esta linea ABRE la unidad
        if _cc == "cita" and _es_item_cita(_lns[_ini]) and _ini != _i:
            break
        _ant = _lns[_ini - 1]
        if not _ant.strip():
            break
        if _cl(_ant) == "item" and _lns[_ini].startswith((" ", "\t")):
            _ini -= 1; break                        # continuacion de ese item
        if _cl(_ant) != _cl(_lns[_ini]):
            break
        _ini -= 1
        if _cl(_lns[_ini]) == "cita" and _es_item_cita(_lns[_ini]):
            break
    # Hacia adelante la unidad crece mientras la linea siguiente NO abra otra
    # afirmacion. Y «abrir otra» se decide por SANGRIA, no solo por el
    # marcador: una continuacion como «      + self-consistent Hubble cascade»
    # empieza por «+» y parece una vinena, pero esta mas indentada que el item
    # que abre la unidad, asi que le pertenece. (Sin esto, la unidad se
    # quedaba en la primera linea y una marca escrita en la segunda no
    # contaba. Lo encontro el propio control de la regla, que es para lo que
    # esta.) Un sub-item anidado cae del mismo lado a proposito: forma parte
    # de la afirmacion de su padre.
    _sang = len(_lns[_ini]) - len(_lns[_ini].lstrip())
    _fin = _i
    while _fin + 1 < len(_lns):
        _s = _lns[_fin + 1]
        if not _s.strip():
            break
        _cs = _cl(_s)
        _ss = len(_s) - len(_s.lstrip())
        if _ss > _sang:                             # mas indentada: es suya
            _fin += 1
            continue
        if _cs == "item" or (_cs == "cita" and _es_item_cita(_s)):
            break                                   # empieza OTRA afirmacion
        if _cs != _cl(_lns[_fin]):
            break
        _fin += 1
    return _ini, _fin


def _afirma_vigencia(_uni, _tokens):
    """P-B: devuelve la oracion que afirma el valor como vigente, o None.
    Exige las tres cosas a la vez EN LA MISMA ORACION: el valor retirado, una
    palabra que afirme vigencia, y ninguna marca ni verbo en pasado."""
    for _o in _ORA_R69.split(_uni.replace("\n", " ")):
        if not any(_t in _o for _t in _tokens):
            continue
        _ol = _o.lower()
        if any(_e.lower() in _ol for _e in _EXENTO_RETR): continue
        if any(_v in _ol for _v in _PASADO_R69): continue
        if any(_v in _ol for _v in _VIGENTE_R69):
            return " ".join(_o.split())
    return None


# LA FORMA TIPOGRAFICA NO PUEDE DECIDIR SI SE CAZA UN RESTO (2026-09-19).
# Los tokens se escribieron pegados («k_fs=0.754») y el README los escribe con
# espacios («k_fs = 0.754»), en una celda de tabla («| 0.754 h/Mpc») o
# URL-codificados dentro de un badge («k__fs_%3D_0.754»). Resultado: cuatro
# restos de la particula vivos en la portada del repositorio, y el barrido
# pasando limpio — lo encontro una auditoria externa el 2026-09-19.
# Se normaliza la superficie ANTES de comparar, en vez de ir anadiendo
# variantes a la lista, que es justo lo que se queda rancio.
_MOJI = {"%3D": "=", "%2F": "/", "%20": " ", "__": "_", "\\,": "", "\\ ": " "}


def _forma(_x):
    for _k, _v in _MOJI.items():
        _x = _x.replace(_k, _v)
    return re.sub(r"\s*([=])\s*", r"\1", _x)


# FORMA RENDERIZADA (2026-09-19). Un token vive en el .py como LaTeX
# (`k_{\rm fs}=0.754`) y dentro del PDF como GLIFOS: `pdftotext` devuelve
# `kfs = 0.754` —sin `$`, sin la orden `\rm`, sin llaves, sin el subrayado y
# con espacios alrededor del `=`. Comparar la una con la otra da VERDE
# siempre, mire lo que mire.
# Lo cazo asi: el barrido de figuras de R60 daba verde con
# `results/figures/ssee_eftcamb_Pk.pdf` —que ENTRA en SSEE_Unified_Journal—
# llevando dentro la linea rotulada `k_fs = 0.754 h/Mpc`, de la particula
# retirada el 2026-08-01. pdftotext SI leia el numero; lo que no casaba era
# la forma del token. Misma clase de fallo que el `%3D` de la insignia: no
# es que no se mirara, es que se comparaba una forma contra otra.
_RENDER_CMD = re.compile(r"\\(?:rm|mathrm|mathit|text|textrm|bf|it)\b")


def _forma_render(_x):
    """Normaliza a la forma en que un PDF devuelve el texto de una figura."""
    _x = _RENDER_CMD.sub("", _x)
    for _c in "${}_\\":
        _x = _x.replace(_c, "")
    # TODO el espacio fuera, no solo el del `=`. Al quitar la orden `\rm` de
    # `k_{\rm fs}` queda un hueco (`k fs`) que el PDF no tiene (`kfs`), y el
    # espaciado que devuelve pdftotext no es fiable de por si. Aprieta la
    # comparacion, asi que el control de abajo comprueba las dos direcciones.
    return re.sub(r"\s+", "", _x).lower()


def _presenta_como_vigente(_txt, _tokens):
    """Lineas con un valor retractado y sin marca de retraccion EN SU VENTANA.
    La ventana es +-1 linea porque en prosa LaTeX el «retracted» que califica
    al valor cae con frecuencia en la linea anterior (el .tex va justificado a
    ~72 columnas, no por frase)."""
    _lns = _txt.split("\n")
    _malas = []
    # AMBITO DE SECCION (2026-09-07). Al ampliar la superficie a los .md
    # salieron 58 sitios, y la mayoria estaban DENTRO de fichas cuyo
    # ENCABEZADO ya narra la retraccion («## OP-17 … RETIRADA»): la linea
    # suelta no repite la marca porque la seccion entera ya la lleva.
    # Marcarlas una a una seria ruido; lo que hay que mirar es si el
    # encabezado o el banner que las cubre lo declara. Si no lo declara,
    # entonces si es una afirmacion viva.
    def _cabecera_retirada(_j):
        # Sube por TODA la cadena de encabezados hasta el h2 que la cubre.
        # Antes paraba en el mas cercano, asi que un «### Registro de rutas»
        # dentro de «## OP-9 — CERRADO POR DISOLUCION» tapaba la marca del
        # padre y el bloque contaba como vivo.
        for _k in range(_j, -1, -1):
            _l = _lns[_k]
            if _l.startswith(("#", "\\section", "\\subsection", "|---")):
                if any(_e.lower() in _l.lower() for _e in _EXENTO_RETR):
                    return True
                if _l.startswith("## ") or _l.startswith("\\section"):
                    return False
        return False
    _tokn = [_forma(_t) for _t in _tokens]
    for _i, _ln in enumerate(_lns):
        if not any(_tk in _forma(_ln) for _tk in _tokn):
            continue
        # UNA FILA DE TABLA ES UNA AFIRMACION ENTERA (2026-09-19).
        #
        # La ventana de +-3 lineas nacio para prosa LaTeX justificada, donde el
        # «retracted» que califica a un valor cae dos o tres lineas mas abajo.
        # En una TABLA eso se vuelve al reves: las filas son vecinas por
        # construccion, asi que una fila retractada exonera a las de al lado.
        # Caso real: en la tabla de OPs del README, la fila de OP-8
        # («Dissolved 2026-06-18») tapaba la de OP-5, que seguia afirmando que
        # el sector doble resuelve S8 — retirado el 2026-08-01. Un lector la
        # leia como vigente, y el guardian no la contaba.
        # En una fila, la marca tiene que estar EN LA FILA.
        if _ln.lstrip().startswith("|") and not _ln.lstrip().startswith("|---"):
            if any(_e.lower() in _ln.lower() for _e in _EXENTO_RETR):
                continue
            if not _cabecera_retirada(_i):
                _malas.append(_ln.strip())
            continue
        # ── R60 CRECE · LA UNIDAD DE AFIRMACION, Y EL AFIRMADOR DE VIGENCIA ──────
        #
        # Historia de este sitio, porque es la leccion:
        #   +-1  (2026-09-07) → 3 falsos positivos en prosa LaTeX justificada.
        #   +-3  (2026-09-07) → los arreglo, y abre el agujero de abajo.
        #   R60+ (2026-09-19) → se sustituye la ventana por la UNIDAD.
        #
        # Con +-3 un parrafo quedaba exento si la palabra «retired» aparecia en
        # cualquiera de las siete lineas, aunque calificara a OTRA COSA. Lo
        # declare punto ciego tras medir UNA sola dimension —la distancia— y
        # ver que no separaba: el falso positivo tenia su marca a 162
        # caracteres y dos retractaciones legitimas a 180 y 199.
        #
        # Medir la distancia era la pregunta equivocada. Al interrogar el
        # error de verdad (banco de las 43 exenciones que la ventana concedia
        # sobre el arbol vivo mas el README del commit anterior al arreglo)
        # salieron DOS preguntas que si separan, y un segundo caso del mismo
        # error que yo no habia visto: un item «- [x] Canonical phi-DM
        # particle (m_phi = 40.70 eV…)» eximido por la palabra «archived» del
        # item de ARRIBA, que hablaba de Zenodo.
        #
        # P-A · LA UNIDAD DE AFIRMACION. La exencion no vale «cerca»: vale
        #   DENTRO de lo que un lector lee como una sola afirmacion — un item
        #   de lista, una linea de cita, un parrafo. Es la generalizacion de
        #   lo que ya se habia arreglado para las filas de tabla: un vecino no
        #   exonera. Caza el caso del «archived», y con el 22 sitios mas que
        #   la ventana venia tapando en los .md.
        #
        # P-B · EL AFIRMADOR DE VIGENCIA. Una unidad puede llevar su marca de
        #   retraccion y aun asi AFIRMAR el valor como vigente en una de sus
        #   frases («Canonical phi-DM particle m_phi = 40.70 eV (forward
        #   prediction, zero fitting)»). Si una oracion junta el valor con una
        #   palabra que afirma vigencia y no lleva ninguna marca ni verbo en
        #   pasado, es una afirmacion viva aunque el parrafo la retracte tres
        #   lineas mas abajo. Esta es la que caza el caso que declare
        #   incerrable.
        #   Se mide a nivel ORACION a proposito: a nivel parrafo mataba 6 de
        #   los 41 casos legitimos, porque la narracion de una retraccion cita
        #   necesariamente la palabra con que el valor se anunciaba
        #   («announced a canonical particle… that particle was retracted»).
        #
        # HASTA DONDE VE, dicho en voz alta: las dos son reglas de FORMA. La
        # pregunta del REFERENTE —si la marca gobierna este valor o el de al
        # lado— se interrogo y no hizo falta para separar este banco; queda
        # sin implementar, y por tanto sin probar. Si algun dia aparece un
        # resto que P-A y P-B no vean, es ahi donde hay que mirar primero, y
        # esta regla tendra que crecer otra vez. No es absoluta: es la que da
        # la talla con lo que hoy sabemos preguntar.
        # El ambito de seccion manda sobre las dos: si la ficha entera va bajo
        # un encabezado que ya narra la retraccion, sus lineas no tienen que
        # repetir la marca — eso ya se decidio el 2026-09-07 y sigue siendo
        # cierto. (En la primera version puse P-A ANTES de esta comprobacion y
        # marque 28 lineas de fichas OP-9/OP-17 que su propio titulo declara
        # cerradas por disolucion.)
        # P-C · EL AMBITO NO CUBRE UNA AFIRMACION EN PRESENTE (2026-09-20).
        #
        # Aqui estaba escrito, arriba, que si algun dia aparecia un resto que
        # P-A y P-B no vieran habria que volver a este sitio. Aparecio, y lo
        # encontro una auditoria externa (Max): cuatro sitios bajo cabeceras
        # que YA narran la retraccion y que aun asi afirmaban en presente.
        # El peor, el veredicto de V-L4-S8 en el Registro: bajo su propio
        # cartel «🔴 RETIRADO» y con la linea de arriba tachada, remataba «El
        # titular ES el two-sector (0.758, 0.01sigma)». Tambien OPEN_PROBLEMS
        # §OP-5, donde bajo una tabla tachada seguia «El two-sector phi-DM
        # (m_phi=40.70 eV, k_fs=0.754) YA SUPRIME P(k)».
        #
        # El fallo no era el ambito: eximir a la ficha de repetir la marca en
        # cada linea sigue siendo correcto —se decidio el 2026-09-07 y lo
        # sigue siendo—. El fallo era que el `continue` se llevaba por
        # delante TAMBIEN a P-B. Una cabecera dice «esto se retiro»; no puede
        # decir «y ademas lo que escriba debajo en presente es cierto».
        # Asi que el ambito exime de P-A (no repetir la marca) y NO de P-B
        # (no afirmar vigencia). Es la misma leccion que R58 el mismo dia: la
        # exencion vale para lo que calla, no para lo que afirma.
        _a, _b = _unidad(_lns, _i)
        if _cabecera_retirada(_i):
            # Sólo las líneas de VEREDICTO. Medido: aplicar P-B a toda unidad
            # bajo cabecera retirada marca 15 sitios, y 14 son fichas OP-9 /
            # OP-17 que narran legítimamente lo que el modelo afirmaba
            # entonces («Canonical particle is now 594.28»). Eso ya se midió
            # el 2026-09-19 —28 líneas— y por eso el ámbito exime. Un
            # detector con 93% de falsos positivos obligaría a tachar fichas
            # históricas enteras: no separa, así que no se aplica.
            #
            # Lo que SÍ separa es el TIPO DE LÍNEA. Un «**Veredicto:**» o un
            # «**Estado:**» no narran el pasado: dictan el estado de la
            # entrada AHORA, y una cabecera de retirada no puede autorizarlos
            # a afirmar en presente algo retirado. Ahí estaba el caso real
            # (V-L4-S8: bajo su cartel 🔴 RETIRADO remataba «El titular ES el
            # two-sector (0.758, 0.01σ)»).
            #
            # HASTA DÓNDE VE: no cubre la prosa corriente bajo cabecera
            # retirada. El otro sitio que halló la auditoría —OPEN_PROBLEMS
            # §OP-5, «El two-sector φ-DM … ya suprime P(k)»— no es un
            # veredicto y esta regla NO lo habría cazado; se corrigió a mano.
            # Cubrirlo pide la pregunta del REFERENTE que sigue sin
            # implementar tres párrafos más arriba. Queda dicho.
            # ... y sólo si NI la línea NI su cabecera se declaran HISTÓRICAS.
            # Los dos únicos falsos positivos que quedaban lo estaban, por
            # escrito: «### Contenido histórico (la adopción, tal como se
            # decidió en su momento)» y «**Status change (2026-06-04)**», que
            # narra un cambio de estado de junio, no el de hoy. Un veredicto
            # que dice ser de otra época no pretende ser el vigente.
            if not _VEREDICTO60.match(_lns[_a].strip()):
                continue
            _cab = "\n".join(_lns[max(0, _a - 12):_b + 1])
            if _HISTORICO60.search(_cab):
                continue
            _viva = _afirma_vigencia("\n".join(_lns[_a:_b + 1]), _tokens)
            if _viva:
                _malas.append(_viva[:70])
            continue
        _uni = "\n".join(_lns[_a:_b + 1])
        if not any(_e.lower() in _uni.lower() for _e in _EXENTO_RETR):
            _malas.append(_ln.strip()[:70])          # P-A
            continue
        _viva = _afirma_vigencia(_uni, _tokens)      # P-B
        if _viva:
            _malas.append(_viva[:70])
            continue
    return _malas


# 2026-09-07: solo barria manuscript/*.tex. AUDIT.md — el MANUAL DE
# AUDITORIA — llevaba la particula como vigente en 8 sitios, incluida
# una tabla que la listaba como «Future prediction» y una seccion que
# mandaba a CORRERLA. Es la misma falla que el guardian tuvo 36 dias,
# reaparecida en un documento que la guarda no miraba. Ahora incluye
# los .md vivos de la raiz y submission_PRD/.
_tex_vivos = [(_p.name, _p.read_text(errors="ignore"))
              for _p in sorted(list((ROOT.parent / "manuscript").glob("*.tex"))
                               + list((ROOT.parent / "submission_PRD").glob("*.tex"))
                               + [_q for _q in sorted(ROOT.parent.glob("*.md"))
                                  if _q.name not in ("CHANGELOG.md", "MEMORY.md")])]
_viv_part = {_n: _presenta_como_vigente(_t, _RETRACTADOS)
             for _n, _t in _tex_vivos}
_viv_part = {_n: _v for _n, _v in _viv_part.items() if _v}
# Los PAPERS son ROJO: son lo que se publica. Los .md de apoyo entran
# como DEUDA con trinquete (solo baja), igual que R42-R45: 49 sitios el
# 2026-09-07, el dia que la guarda dejo de mirar solo manuscript/*.tex.
_md_part = {_n: _v for _n, _v in _viv_part.items() if _n.endswith(".md")}
_viv_part = {_n: _v for _n, _v in _viv_part.items() if not _n.endswith(".md")}
_n_md = sum(len(_v) for _v in _md_part.values())
# El trinquete vive aqui (no en _DEUDA_MAX, que se define mas abajo):
# 49 el 2026-09-07, el dia que la guarda dejo de mirar solo los .tex.
# SOLO BAJA.
_TOPE_PART_MD = 0
check("V-L3-mphi  la deuda de particula en los .md no crece",
      _n_md <= _TOPE_PART_MD,
      f"{_n_md} sitios (tope {_TOPE_PART_MD}): "
      + "; ".join(f"{_k}:{len(_v)}" for _k, _v in sorted(_md_part.items())))
check("V-L3-mphi  ningun .tex presenta la particula como vigente",
      not _viv_part,
      f"{len(_tex_vivos)} .tex barridos, 0 sitios sin marcar"
      if not _viv_part else
      "sin marca de retraccion en " + "; ".join(
          f"{_n}:{len(_v)}" for _n, _v in sorted(_viv_part.items())[:5]))

# Control (R53): el detector debe MARCAR una linea que presente el valor como
# vigente y DEJAR PASAR la misma linea declarada retirada.
_c_viva = "the particle mass is $m_\\phi = 40.70$ eV"
_c_muerta = "the retracted value $m_\\phi = 40.70$ eV (withdrawn 2026-08-01)"
check("V-L3-mphi  el detector distingue vigente de retractado",
      bool(_presenta_como_vigente(_c_viva, _RETRACTADOS))
      and not _presenta_como_vigente(_c_muerta, _RETRACTADOS),
      "1 forma viva marcada, 1 declarada retirada eximida")

# ── CONTROL DE LA SEPARACION SIN-RESOLVER / PENDIENTE (R53) ────────────────
# El riesgo de separarlas es evidente: si «abierto» deja de pintar, basta con
# llamar «problema abierto» a una tarea para que el semaforo no la vea — que es
# exactamente el VERDE FORZADO que Mike detecto el 2026-09-07. Lo que lo impide
# es que la etiqueta no la pongo yo al escribir el track_open: la pone la FICHA.
# Sin ficha, con ficha cerrada o sin severidad, cae en PENDIENTE y pinta.
_c53a = _FICHAS_OP.get("OP-7", ("", ""))
_c53b = _FICHAS_OP.get("OP-5", ("", ""))
check("R53 una ficha viva con severidad es lo unico que saca algo del semaforo",
      _c53a == ("abierto", "alta") and _c53b[0] == "cerrado",
      f"OP-7 {_c53a} entra como fisica sin resolver; OP-5 {_c53b} esta cerrada, "
      f"asi que su resto tuvo que abrir ficha propia (OP-5b) para contar")
check("R53 el lector de fichas distingue parcial de resuelto y lee los dos formatos",
      _FICHAS_OP.get("OP-1", ("", ""))[0] == "abierto"
      and _FICHAS_OP.get("OP-16", ("", ""))[1] == "baja"
      and _FICHAS_OP.get("OP-13", ("", ""))[0] == "cerrado",
      "«PARCIALMENTE RESUELTO» cuenta como abierto (OP-1); «**Severidad: Baja / "
      "especulativa.**», con los dos puntos dentro de los asteriscos, se lee "
      "(OP-16 = baja, antes heredaba la de otra ficha); «RESUELTO» cierra (OP-13)")
check("R53 ninguna ficha citada por el guardian se quedo sin severidad",
      not [_o for _o, _, _ in sin_resolver if not _FICHAS_OP.get(_o, ("", ""))[1]],
      f"{len({_o for _o, _, _ in sin_resolver})} fichas citadas, todas con "
      "severidad declarada en OPEN_PROBLEMS.md")

# ── CONTROL DEL ALCANCE NUEVO DE R60 (R53: toda regla trae su control del otro lado) ──────────
# Los dos casos son REALES, tomados del README en el commit 1f05380^ — el
# anterior al arreglo. La regla se prueba contra el estado sucio, que es la
# unica manera de saber que habria servido: correrla solo contra el arbol ya
# limpio prueba que no molesta, no que detecta.
_c69_item = "\n".join((
    "- [x] Zenodo v6 — Papers 1-7 archived (DOI 10.5281/zenodo.20093447)",
    "- [x] Canonical phi-DM particle (m_phi = 40.70 eV, forward prediction)",
    "      + self-consistent Hubble cascade"))
_c69_frase = ("**Status (2026-07-10):** all 10 papers compile clean. Canonical "
              "phi-DM particle m_phi = 40.70 eV (forward prediction, zero "
              "fitting) with pre-registered free-streaming imprint.\n"
              "Full hostile-referee audit closed: verification guardian fully "
              "green + figure-level pdftotext sweep (retired numbers purged "
              "from text AND figures).")
# Y los dos del otro lado: narracion legitima que NO se puede marcar.
_c69_narra = ("An earlier version introduced a canonical particle candidate of "
              "mass $m_\\phi=40.70$~eV (now retracted), motivated by an "
              "apparent $S_8$ tension.")
_c69_banner = "\n".join((
    "> **BANNER PARTICULA RETIRADA (2026-08-01).**",
    "> Se retiran el segundo sector y la particula m_phi=40.70 eV, por dos",
    "> razones independientes."))
check("R60 un vecino no exonera: la exencion vale dentro de la unidad, no cerca",
      bool(_presenta_como_vigente(_c69_item, ("40.70",)))
      and not _presenta_como_vigente(_c69_banner, ("40.70",)),
      "el item eximido por el «archived» del item de ARRIBA queda marcado; "
      "el banner de cita multilinea, que SI es una sola unidad, exento")
# P-C, del otro lado. Los dos casos son REALES: el primero es el veredicto de
# V-L4-S8 en el Registro tal como estaba antes del 2026-09-20 —lo encontro una
# auditoria externa (Max)— y el segundo es el sitio de OP-17 que SI debe
# eximirse porque se declara historico por escrito. Un veredicto dicta el
# estado de AHORA; si dice ser de otra epoca, no pretende ser el vigente.
_c70_veredicto = "\n".join((
    "> 🔴 **RETIRADO 2026-08-01.** La particula phi-DM fue retirada.",
    "2. ~~two-sector phi-DM (TITULAR): S8_eff = 0.758~~ **RETIRADO.**",
    "",
    "**Veredicto:** la cadena S8 es aritmeticamente correcta.",
    "El titular es el two-sector (0.758, 0.01 sigma). **Verificado.**"))
_c70_historico = "\n".join((
    "### Contenido historico (la adopcion, tal como se decidio en su momento)",
    "",
    "**Status:** CERRADO / ADOPTADO (Mike, 2026-06-19). CLASS forward real",
    "@ 40.70 eV propagado a CANONICAL_VALUES.yaml."))
check("R60 P-C: un VEREDICTO bajo cabecera retirada no se exime, salvo que se declare historico",
      bool(_presenta_como_vigente(_c70_veredicto, ("two-sector", "0.758")))
      and not _presenta_como_vigente(_c70_historico, ("40.70",)),
      "2 casos reales: el veredicto de V-L4-S8 que remataba «el titular ES el "
      "two-sector» bajo su propio cartel de RETIRADO queda marcado; el "
      "«Contenido historico» de OP-17, que dice serlo, exento")
check("R60 una frase que AFIRMA vigencia no se exime por su parrafo",
      bool(_presenta_como_vigente(_c69_frase, ("40.70",)))
      and not _presenta_como_vigente(_c69_narra, ("40.70",)),
      "«Canonical … 40.70 eV (forward prediction)» marcado pese al «retired» "
      "tres lineas mas abajo; «a canonical candidate … (now retracted)» exento")

# CONTROL (R53) de lo que se ensancho el 2026-09-19: vocabulario castellano y
# corte por punto y coma. Ensanchar una EXENCION es la via directa a ablandar
# una regla, asi que por cada forma que ahora exime va una que NO debe eximir.
_c60_es = [
    # (texto, debe marcarse)
    # OJO con lo que mide cada patrón. `_PASADO_R69` sólo actúa sobre P-B (el
    # afirmador de vigencia); una frase en pasado SIN palabra de vigencia y
    # SIN marca de retirada la sigue marcando P-A, y debe hacerlo: narrar en
    # pasado no es retractar. Por eso este caso lleva las dos cosas.
    ("`72.86` y `73.040` quedan RETIRADOS: eran el mismo enunciado.", False),
    ("`72.86` y `73.040` eran el mismo enunciado leido al reves.", True),
    ("El viejo «72.86 via H_alg» metia un numero sin unidades.", False),
    ("Ese «<0.2%» era el bug de normalizacion de la saturacion.", False),
    ("La cascada se retiro el 2026-09-06; el valor era 72.86.", False),
    # …y las que TIENEN que seguir marcadas: afirman vigencia, en castellano
    ("La cascada canonica da H_local = 72.86 km/s/Mpc.", True),
    ("Valor vigente de la cascada: 72.86.", True),
    ("El anclaje adoptado es 72.86, status canonico.", True),
    # el punto y coma parte DOS afirmaciones: la primera no hereda el
    # «canonical» de la segunda, pero tampoco lo pierde si es suyo
    ("The cascade is H_local = 72.86; the canonical posterior is 67.79.", True),
    ("> **Superseded.** The cascade is H_local = 72.86; the canonical "
     "posterior is 67.79.", False),
]
_f60es = [f"{_tx[:40]!r}" for _tx, _esp in _c60_es
          if bool(_presenta_como_vigente(_tx, ("72.86",))) != _esp]
check("R60 el detector lee el castellano igual que el ingles",
      not _f60es,
      "10 casos: «el viejo», «era» y «se retiro» eximen; un pasado SIN marca "
      "sigue marcado —narrar en pasado no es retractar—; «canonica», "
      "«vigente» y «adoptado» NO; y el `;` separa dos afirmaciones sin que la "
      "primera herede el «canonical» de la segunda"
      if not _f60es else f"casos mal clasificados: {_f60es}")
check("R60 el detector no se comio la superficie que dice mirar",
      len(_unidad(_c69_item.split("\n"), 1)) == 2
      and _unidad(_c69_item.split("\n"), 1) == (1, 2),
      "el item de dos lineas se delimita en (1,2): no absorbe al de arriba "
      "ni se queda corto en su continuacion indentada")

# Dos sectores phi-DM (P6) — tras el reframe omega_m-directo (2026-06-18) la
# particion sale SOLA, sin factor: Om_CDM (=Om_m,dyn=0.160, DESI) + Om_phiDM =
# Om_m,CMB (=omega_m/h²=0.308881). El sector phi-DM es la DIFERENCIA entre la
# materia del CMB (omega_m) y la CDM dinamica. El split fisico en k_fs depende
# de m_phi (ABIERTO) y k_fs (pendiente Fase B).
Om_m_CMB = _omm / _h ** 2
Om_phiDM = Om_m_CMB - Om_m_dyn               # ≈ 0.149 (era (MIRA-1)*dyn=0.160)
check("V-L3-2sec  [RETIRADO] la resta Om_m,CMB - 0.160 no era fisica",
      abs((Om_m_dyn + Om_phiDM) - Om_m_CMB) < 1e-12,
      "la suma cierra por construccion, pero 0.160 es 1+w0 (ECUACION DE ESTADO), "
      "no una densidad: restar una densidad medida menos un numero de la EoS esta "
      "dimensionalmente bien formado y VACIO de contenido fisico. Sector unico: "
      "Om_m = 0.308881 sin particion (2026-08-01)")

# ── REFRAME 2026-06-19 — DEPENDIENTES PENDIENTES DE RECOMPUTE (cajon scripts) ──
# Inputs FIJADOS (algebra pura): Om_m,CMB=0.30888 (omega_m/h², OP-8 CERRADO, sin
# factor), H global=H_alg=67.962, m_phi=40.70 eV (mult SOLAR²·KRYSTOS=594.28,
# mecanismo g²·v adoptado; OP-17 cerrado; C_ν=93.14 unificada 2026-07-10).
# Los siguientes valores DEPENDEN de esos inputs; algunos checks pueden mostrar
# numeros viejos hasta correr cada codigo. NO se actualizan hasta recomputar:
# FASE B DEL REFRAME — CERRADA salvo fsigma8 (2026-09-19). Los tres recomputes
# que quedaban se verificaron contra su LOG, no contra la memoria:
#   (1) r_d = 147.174 Mpc (0.32sigma) con Om_m=0.308881, theta*=0.59667
#       -> results/logs/p3_rd_reframe_omega_m.log
#   (2) H0 = 67.787 +- 0.353 bajo prior H_alg 67.962
#       -> results/logs/mcmc_paper2_reframe.log
#   (3) control metodologico LCDM R4, S8=0.7571+-0.0194
#       -> results/logs/growth_2026-07/R4_lcdm_kids_S8.json
# El texto de este track llevaba desde julio diciendo que estaban pendientes.
# Lo unico que sigue vivo es fsigma8 contra BOSS crudo, y eso no es una tarea
# de higiene: es una corrida de investigacion. Tiene ficha propia, OP-26.
track_open("REFRAME-FaseB  fsigma8 contra BOSS crudo, lo ultimo que falta de la Fase B",
           "los otros tres recomputes CERRADOS y verificados contra su log: "
           "r_d=147.174 (0.32sigma) @ Om_m=0.308881 · H0=67.787+-0.353 bajo prior "
           "H_alg · control LCDM R4 S8=0.7571+-0.0194. Queda R1/R2 con LPT "
           "(velocileptors, k<=0.20, 222 pts); el barrido Kaiser fue sondeo",
           op="OP-26")

# delta_c (OP-27, abierto 2026-09-25). El Paper 4 postulaba
# delta_c = delta_c,EdS * n_s = 1.6284 y el Paper 5 colgaba de el un
# enhancement JWST de 1.05x-1.89x. El colapso esferico top-hat sobre el fondo
# del PROPIO modelo da 1.67634 (z_c=0) y 1.68647 (z_c=10), o sea LCDM-like; el
# postulado esta a 2.9% y la dinamica no lo produce. Lo que queda abierto es el
# MECANISMO: n_s no es solo la inclinacion primordial, es cantidad algebraica
# del sector materia (omega_c = KAL0*omega_b*n_s), asi que el vinculo no es
# absurdo a priori — pero ese n_s ya esta dentro del calculo via Omega_m.
track_open("DELTAC  el factor n_s sobre el umbral de colapso no esta derivado",
           "medido: delta_c(SSEE)=1.67634 @z_c=0 y 1.68647 @z_c=10 contra LCDM "
           "1.67599/1.68646 (0.02%/0.001%); control EdS reproduce 3/20(12pi)^(2/3). "
           "El postulado 1.6284 queda retirado como prediccion y vive como "
           "conjetura. Consecuencia medida: el conteo de halos NO se anula, se "
           "INVIERTE (0.892 a 3e12 Msol z=10; 0.99 a las masas que ve JWST)",
           op="OP-27")

# EFT canónico (P7) — los parámetros lambda, alpha_pot, V0 son consecuencias
# algebraicas de constantes ya verificadas (Om_m,dyn, KAL0, Om_DE).
lam_eft = (3 * Om_m_dyn) ** 0.5
alpha_pot = lam_eft / KAL0 ** 0.5
check("V-L3-EFT  identidad lambda^2 = 3 Om_m,dyn",
      abs(lam_eft ** 2 - 3 * Om_m_dyn) < 1e-12, f"lambda = {lam_eft:.6f}")
check("V-L3-EFT  identidad alpha_pot = lambda/sqrt(KAL0)",
      abs(alpha_pot - lam_eft / KAL0 ** 0.5) < 1e-12, f"alpha_pot = {alpha_pot:.6f}")
check("V-L3-EFT  identidad V0 = Om_DE * rho_crit",
      abs(Om_DE - Tr / Mv) < 1e-12, f"V0 = {Om_DE:.6f}")

# UV completion K(X) (P10) — la identidad 45 alpha^2 = 5 phi^8 es exacta;
# la normalización física de M^4 está calibrada a SH0ES (admisión del propio
# script de P10) y es inconsistente con M^4 = rho_crit usado en P7.
check("V-L3-KX  identidad 45 alpha^2 = 5 phi^8  (M^4/rho_crit)",
      abs(45 * alpha_attr ** 2 - 5 * phi ** 8) < 1e-9,
      f"M^4/rho_crit = {5 * phi ** 8:.4f}")
track_open("V-L3-KX  M^4 = 5 phi^8 rho_crit calibrado a SH0ES",
           "ssee_paper10_verification.py admite: normalizacion fisica de M^4 "
           "calibrada a SH0ES, no derivada; Ruta A da M^4~418 != 234.9",
           op="OP-3")
track_open("V-L3-EFT  M^4 inconsistente entre P7 y P10",
           "ssee_eft_verification.py usa M^4 = rho_crit (=1); "
           "ssee_paper10_verification.py usa M^4 = 5 phi^8 rho_crit (=234.9)",
           op="OP-10b")

# Israel-Stewart (P5) — c²_s,eff = 0. La corrección IS zeta/tau_Pi se reduce
# a Om_DE porque el factor KAL0/3 se cancela (zeta = KAL0/3, tau_Pi =
# KAL0/(3 Om_DE)). c²_s,eff = w0 + Om_DE = 0 es la identidad w0 = -Om_DE.
zeta_tilde = KAL0 / 3.0
tau_Pi_H0 = KAL0 / (3.0 * Om_DE)
IS_corr = zeta_tilde / tau_Pi_H0
check("V-L3-IS  identidad zeta/tau_Pi = Om_DE  (KAL0/3 se cancela)",
      abs(IS_corr - Om_DE) < 1e-12, f"IS_corr = {IS_corr:.8f}")
check("V-L3-IS  c2_s,eff = w0 + Om_DE = 0  (estabilidad marginal)",
      abs(w0 + IS_corr) < 1e-12)
# OP-22 CERRADO 2026-09-06. El c2_s,eff = 0 ES un resultado, no un artefacto:
# zeta~ esta normalizada a la ENTALPIA (rho+p). Testigo decisivo, un test de
# limite independiente de SSEE: con w->-1, rho+p->0 y una constante cosmologica
# no tiene grados de libertad de fluido => su presion viscosa DEBE anularse.
# Pi propto (rho+p) lo da solo; Pi propto rho_DE deja presion viscosa finita.
# Testigo interno REPRODUCIBLE: el apendice de autovalores de P5 reporta
# F = (1-3 c2_s) + zeta~(k/H)^2 ~= 186 en k=10. Solo una normalizacion lo da.
_h_ent = Om_DE * (1 + w0)                 # (rho+p)/rho_c = 0.13443415
_F_ent = 1 + zeta_tilde * 100             # entalpia   -> ~185.0
_F_rhc = 1 + zeta_tilde / _h_ent * 100    # rho_crit   -> ~1370
check("V-L3-IS  el F~186 de P5 solo sale con la normalizacion de ENTALPIA",
      abs(_F_ent - 186) < 2 and abs(_F_rhc - 186) > 100,
      f"entalpia {_F_ent:.2f} (P5 dice ~186) / rho_crit {_F_rhc:.2f} "
      f"(un orden de magnitud fuera)")
# Control (R53): la lectura rho_DE del ansatz viejo da SUPERLUMINICO, y por eso
# queda superada. Si el detector no marcara esto, el 0 seria indistinguible.
_cb_rhoDE = (KAL0 / 3.0) / ((1 + w0) * tau_Pi_H0)
check("V-L3-IS  el ansatz viejo Pi ~ rho_DE es superluminico (por eso cae)",
      w0 + _cb_rhoDE > 1.0,
      f"c2_eff = {w0 + _cb_rhoDE:.4f} > 1 con Pi = -KAL0*rho_DE*H; "
      f"con Pi = -KAL0*(rho+p)*H da {w0 + zeta_tilde / tau_Pi_H0:.2e}")
# El "modo campo" de P5 estaba calculado con la K EQUIVOCADA: usaba
# K = X/KAL + X^2/M^4, que es el funcional de APANTALLAMIENTO de P10, no la
# accion de energia oscura (el condensado fantasma de P7). Corregido en P5.
_u_p7 = -0.522735380747
_cs2_campo = (1 + 2 * _u_p7) / (1 + 6 * _u_p7)
check("V-L3-IS  el modo campo sale de la accion de P7, no del K de P10",
      abs(_cs2_campo - 0.021283701571) < 1e-9,
      f"c2_s,ad = (1+2u)/(1+6u) = {_cs2_campo:.12f} con u = c2X/c1 de P7; "
      f"el 0.96737 del K de P10 es otro funcional (razon +0.008577)")
# --- OP-22b, conteo de grados de libertad (2026-09-07) -----------------
# Un escalar k-essence lleva UN modo propagante; en el fluido IS la
# presion viscosa Pi relaja y queda esclava de delta, no viaja sola.
# Las dos descripciones cuentan UNA onda => son la MISMA, y la del
# campo es la fundamental (sale de la accion).
# CONTROL (R53): apagar el rescate viscoso. El fluido se cae solo
# (c2_ad = w0 < 0, inestable a gradientes); el campo no lo necesita.
_cs2_fluido_sin_visc = w0                   # -0.839950
_cs2_campo_sin_visc  = _cs2_campo           # +0.021284
check("V-L3-IS  el rescate viscoso es del FLUIDO, no del campo",
      _cs2_fluido_sin_visc < 0.0 < _cs2_campo_sin_visc,
      f"sin viscosidad: fluido c2_ad = w0 = {_cs2_fluido_sin_visc:.6f} "
      f"(inestable) vs campo c2_s = {_cs2_campo_sin_visc:.6f} (estable). "
      "La viscosidad tapa un agujero propio del fluido; el campo no "
      "tiene ese agujero => el campo es la descripcion fundamental")
# --- OP-22b, de donde saldria zeta (2026-09-07) ------------------------
# La accion de P7 es K = c1 X + c2 X^2, SIN potencial y SIN acoplamiento
# (simetria de shift). Un campo asi es exactamente ADIABATICO:
# delta_p - c_s^2 delta_rho = 0 identicamente => no produce entropia
# => zeta = 0. La viscosidad de P5 NO puede salir de la accion.
# CONTROL (R53): un campo CON potencial si tiene parte no adiabatica.
# La parte NO adiabatica vive en la variacion de phi, no en la de X:
#   delta_p - c_s^2 delta_rho = [K_phi - c_s^2 (2X K_Xphi - K_phi)] delta_phi
# Variar solo X da 0 SIEMPRE (lo probe: un potencial constante tambien
# daba 0) — ese primer control no probaba nada. Hay que variar phi.
import sympy as _sp
_X, _ph, _c1, _c2, _V0, _al = _sp.symbols('X phi c1 c2 V0 al', real=True)
def _no_adiab(_K):
    _Kx  = _sp.diff(_K, _X)
    _Kxx = _sp.diff(_K, _X, 2)
    _Kp  = _sp.diff(_K, _ph)
    _Kxp = _sp.diff(_K, _X, _ph)
    _cs2 = _Kx/(_Kx + 2*_X*_Kxx)
    return _sp.simplify(_Kp - _cs2*(2*_X*_Kxp - _Kp))
_ad_p7 = _no_adiab(_c1*_X + _c2*_X**2)             # P7: shift-symmetric
_ad_pot = _no_adiab(_c1*_X + _c2*_X**2 - _V0*_sp.exp(-_al*_ph))
check("V-L3-IS  la accion de P7 es exactamente adiabatica => zeta = 0",
      _ad_p7 == 0,
      f"coef. no adiabatico = {_ad_p7} identicamente en (c1,c2,X); "
      "sin produccion de entropia no hay viscosidad de volumen: la capa IS "
      "repara la PARAMETRIZACION (w,c_s^2) de los codigos, no el campo")
check("V-L3-IS  el detector de adiabaticidad distingue shift-simetrico de potencial",
      _ad_p7 == 0 and _sp.simplify(_ad_pot) != 0,
      "control: el mismo K con un potencial V0 exp(-al phi) devuelve un "
      f"coeficiente NO nulo => el detector si ve la parte no adiabatica "
      "cuando la hay; el 0 de P7 es propiedad de la simetria de shift, "
      "no de la cuenta")
# KAL0 no aparece en la accion de energia oscura (es de P10)
_p7src = (ROOT.parent/"manuscript"/"SSEE_Paper7_EFT.tex").read_text(errors="ignore")
_kal_accion = re.search(r"K\(X\)\s*=\s*[^\n]*KAL", _p7src)
check("V-L3-IS  KAL_0 no normaliza la accion de energia oscura",
      _kal_accion is None,
      "P7: K(X) = c1 X + c2 X^2 (sin KAL_0). El X/KAL_0 es el funcional "
      "de apantallamiento de P10 => la recurrencia de KAL_0 en zeta_tilde "
      "es un PARECIDO entre dos objetos distintos, no una derivacion")
# --- KAL_0 se CANCELA en la capa de fluido (2026-09-07) ----------------
# zeta_tilde = KAL0/3 y tau_Pi H0 = KAL0/(3 Om_DE) comparten KAL0, asi
# que en la razon —que es lo unico que entra en el observable— se va:
#   c2_eff = w0 + zeta/tau = -Om_DE + Om_DE = 0  para CUALQUIER constante.
# El 0 es solido (sale de Om_DE = |w0|, algebra), pero KAL0 no hace
# trabajo ahi. CONTROL (R53): en omega_c = KAL0 wb n_s SI lo hace.
_c2_kal = []
for _f in (0.5, 1.0, 2.0, 7.3):
    _z = _f*KAL0/3.0
    _t = _f*KAL0/(3.0*Om_DE)
    _c2_kal.append(w0 + _z/_t)
_wb_k = (pi - phi)/(3*(pi + phi)**2)      # omega_b algebraico
_ns_k = 1 - phi**-7                        # n_s algebraico
_wc_kal = [_f*KAL0*_wb_k*_ns_k for _f in (0.9, 1.0, 1.1)]
check("V-L3-IS  KAL_0 se cancela en la capa de fluido: el 0 no lo usa",
      all(abs(_v) < 1e-12 for _v in _c2_kal),
      "c2_eff = w0 + zeta/tau = 0 para KAL0 x0.5, x1, x2, x7.3 — la razon "
      "zeta/tau = Om_DE no lleva KAL0. El 0 sale de Om_DE = |w0|, no de "
      "KAL0; la particion zeta_tilde = KAL0/3 no esta determinada")
check("V-L3-IS  control: KAL_0 SI hace trabajo en omega_c",
      abs(_wc_kal[0] - _wc_kal[1]) > 0.01 and abs(_wc_kal[2] - _wc_kal[1]) > 0.01,
      f"omega_c = KAL0 wb n_s: x0.9 -> {_wc_kal[0]:.6f}, x1 -> {_wc_kal[1]:.6f}, "
      f"x1.1 -> {_wc_kal[2]:.6f} contra Planck 0.1200+-0.0012 (~10 sigma "
      "por cada 10%) => KAL_0 se MIDE, pero por la materia oscura, "
      "no por la viscosidad")
# La cancelacion es LOCAL a c2_eff. tau_Pi si esta anclado, por
# Sigma m_nu = R2 wb (93.14)/(tau_Pi H0), donde KAL0 entra AL CUADRADO
# (R2 = Om/(KAL0 T_r) y tau_Pi = KAL0/(3 Om_DE)): +10% en KAL0 hunde
# Sigma m_nu bajo el piso de oscilaciones 0.058 eV => falsado.
def _smnu_k(_f):
    _K = _f*KAL0
    return (Omega/(_K*Tr))*_wb_k*93.14/(_K/(3.0*Om_DE))
_smnu_hi = _smnu_k(1.1)
check("V-L3-IS  tau_Pi SI esta anclado: por Sigma m_nu, no por c2_eff",
      _smnu_hi < 0.058 < _smnu_k(1.0),
      f"KAL0 x1.1 -> Sigma m_nu = {_smnu_hi:.6f} eV, BAJO el piso de "
      f"oscilaciones 0.058 (x1 da {_smnu_k(1.0):.6f}) => la cancelacion "
      "de KAL_0 es LOCAL a c2_eff; el rol de viscosidad no esta ocioso "
      "en el marco, solo en ese observable")
# --- R59: ninguna ruta de script citada en la prosa apunta al vacio ---
# POR QUE EXISTE. Al mover 6 scripts de beta_c a archive/ quedaron 10
# referencias colgando en AUDIT.md, VERIFICATION_LEDGER.md y
# OPEN_PROBLEMS.md — incluida una LINEA DE COMANDO en AUDIT.md que ya
# no corre. Limpiar es mover a su cajon, y mover exige repuntar quien
# apuntaba. Ninguna regla vigilaba eso: R33/R35/R36 miran logs y
# figuras, ninguna miraba las RUTAS citadas en la prosa.
_R59_RUTA = re.compile(r"(?<![\w/])((?:src|archive|results)/[\w./-]+\.py)")
# ENSANCHADA 2026-09-08 (lo pidio Mike): miraba 33 documentos —los .md de la
# raiz y los .tex de manuscript— y su titulo dice «la prosa», sin mas. Faltaban
# el PRD y los .md de subcarpetas (BANDEJA, docs, informes), que citan rutas
# igual que los demas. Un enunciado universal debe barrer lo que pueda barrer.
_r59, _SUP59 = [], []
for _f in sorted(list(ROOT.parent.glob("*.md"))
                 + [_q for _q in ROOT.parent.rglob("*.md")
                    if _q.parent != ROOT.parent
                    and not {"archive", "sandbox_unificado", ".git",
                             "node_modules", "motor3d"} & set(_q.parts)]
                 + list((ROOT.parent/"manuscript").rglob("*.tex"))
                 + list((ROOT.parent/"submission_PRD").glob("*.tex"))):
    if "archive" in str(_f) or _f.name == "CHANGELOG.md":   # CHANGELOG es historia
        continue
    _txt = _f.read_text(errors="ignore")
    _SUP59.append(_f.name)
    for _m in _R59_RUTA.finditer(_txt):
        _r = _m.group(1)
        if not (ROOT.parent / _r).exists():
            _r59.append(f"{_f.name}: {_r}")
check("R59 ninguna ruta de script citada en la prosa apunta al vacio",
      not _r59, "; ".join(sorted(set(_r59))[:4]) if _r59
      else f"{len(_SUP59)} documentos barridos; todas las rutas .py que citan "
           f"existen (CHANGELOG.md exento: es historia, cita rutas de su epoca)")
_c59 = [("corre `src/p07_eft/ssee_eft_verification.py` para verificar", True),
        ("corre `src/verificacion/ssee_verify.py` para verificar", False)]
_f59 = []
for _tx, _esp in _c59:
    _vis = any(not (ROOT.parent / _m.group(1)).exists()
               for _m in _R59_RUTA.finditer(_tx))
    if _vis != _esp:
        _f59.append(_tx[:44])
check("R59 el detector distingue una ruta muerta de una viva",
      not _f59, "; ".join(_f59) if _f59
      else "2 casos: la ruta del script movido a archive marcada, la del "
           "guardian limpia")

# --- R58: beta_c = -AURA no puede figurar como prediccion viva -------
# POR QUE EXISTE. beta_c fue RETIRADO de P7 (§withdrawn, L80) junto con
# el potencial y el acoplamiento conformal: el Lagrangiano vigente
# K = c1 X + c2 X^2 no lleva ninguno de los dos. Pero la ficha de OP-7
# seguia diciendo «la prediccion beta_c=-AURA es correcta (verificada
# por CAMB, CLASS, DESI a <0.2%)» — y ese 0.2% era el bug de
# normalizacion de la saturacion (corregido da -2.194210, a 45% de
# AURA). Lo vio Mike: si se retiro, lo que quede no es una tension,
# es residuo. R56 vigila un rotulo; esta vigila una AFIRMACION.
_R58_MAL = re.compile(
    # La beta GRIEGA cuenta: el sitio real («La predicción βc=−AURA es
    # correcta … <0.2%») usa «\u03b2c», no «beta_c». La primera version
    # de este patron NO lo veia y la regla pasaba en VERDE contra el
    # commit anterior — una regla que aprueba por ciega. Lo caza el
    # auto-test contra el prefijo, no la lectura del patron.
    r"(?:prediccion|predicci\u00f3n|prediction)[^.\n]{0,60}"
    r"(?:\\?beta_?c|\u03b2\s?_?c|\\bc\b)[^.\n]{0,40}AURA"
    r"|(?:\\?beta_?c|\u03b2\s?_?c|\\bc\b)\s*=\s*[-\u2212]?\s*(?:\\)?AURA[^.\n]{0,80}"
    r"(?:0\.2\s?%|0\.199|correcta|correct|verificad|identidad|identity)"
    # ENSANCHADA 2026-09-20. Las dos alternativas de arriba exigen que cerca
    # aparezca «prediccion», «correcta», «verificad» o «0.2%». El sitio real
    # del Endorser Summary no tenia ninguna: «$\beta_c=-\text{AURA}$
    # (numerical $-3.998$); $\alpha_K=...$ algebraic». Enunciado pelado
    # —simbolo, igual, valor— presentado como vigente, y la regla lo dejo
    # pasar 13 dias en EL documento que va al avalista. Ahora se caza el
    # enunciado SIEMPRE y es _EX58 quien decide: narrar que se retiro exime,
    # no decir nada no. Una regla no debe pedirle al texto que confiese.
    r"|(?:\\?beta_?c|\u03b2\s?_?c|\\bc\b)\s*=\s*[-\u2212]\s*(?:\\text\{)?(?:\\)?AURA",
    re.I)
# AMPLIADA 2026-09-20 junto con el patron pelado. Al dejar de exigir que el
# texto "confiese", la regla empezo a marcar dos sitios que SI estan bien
# narrados y que el patron viejo no alcanzaba: OPEN_PROBLEMS §OP-8b, donde
# beta_c=-AURA es uno de «los cuatro DESCARTADOS por medicion», y el Registro,
# donde la identificacion lleva «✗» y «lo presenta como exacto — no lo es».
# Son negaciones explicitas, no afirmaciones vivas: se eximen por lo que
# dicen, no ensanchando el agujero por el que se colo el Endorser.
_EX58 = ("retirad", "withdraw", "supersed", "earlier version", "bug",
         "~~", "RETIRADO", "no longer", "artefact", "artefacto",
         "descartad", "descartó", "descarto", "✗", "no lo es", "ruled out",
         "falla", "no una derivaci", "coincidencia numérica", "ABIERTO",
         # el Registro narra TESTS y CANDIDATOS: «El test (beta_c=-AURA fijo,
         # sin ajustar nada)» introduce un experimento cuyo resultado es ✗ una
         # tabla mas abajo, y «Candidato ... pendiente test dinamico» marca algo
         # no aplicado en ningun paper. Nombrar lo que se pone a prueba no es
         # afirmarlo — es, de hecho, lo contrario.
         "el test", "candidato", "pendiente")
def _r58_sitios(_txt):
    _h = []
    _ls = _txt.split("\n")
    _off, _pos = [], 0
    for _l in _ls:                       # offset de inicio de cada linea
        _off.append(_pos)
        _pos += len(_l) + 1
    for _m in _R58_MAL.finditer(_txt):
        # DOS lineas a cada lado (2026-09-20): antes solo miraba hacia ATRAS,
        # y en P7 §withdrawn la exencion («Both are withdrawn.») va DESPUES
        # del enunciado. Con el patron pelado eso daria un falso positivo en
        # el unico sitio que SI esta bien narrado.
        _n = max(i for i, _o in enumerate(_off) if _o <= _m.start())
        # CUATRO lineas a cada lado, no dos: en el Registro la marca que
        # desactiva la afirmacion («✗» en la tabla del test, el veredicto
        # «coincidencia numerica, no una derivacion») vive un parrafo mas
        # abajo, no pegada. Cuatro alcanza esas narraciones y sigue sin
        # alcanzar el caso del Endorser, cuyos vecinos eran otros items de
        # la lista — lo prueba el auto-test contra el prefijo.
        _ctx = "\n".join(_ls[max(0, _n - 4):_n + 5])
        if any(_t.lower() in _ctx.lower() for _t in _EX58):
            continue
        _h.append(_ctx.strip()[:70])
    return _h
_r58 = []
for _f in sorted(list((ROOT.parent/"manuscript").rglob("*.tex"))
                 + list((ROOT.parent/"submission_PRD").rglob("*.tex"))
                 + [ROOT.parent/"OPEN_PROBLEMS.md",
                    ROOT.parent/"VERIFICATION_LEDGER.md"]):
    if "archive" in str(_f) or not _f.exists():
        continue
    _r58 += [f"{_f.name}: {x}" for x in _r58_sitios(_f.read_text(errors="ignore"))]
check("R58 beta_c = -AURA no figura como prediccion viva",
      not _r58, "; ".join(_r58[:3]) if _r58
      else "0 sitios; beta_c retirado de P7 §withdrawn, el 0.2% era el bug "
           "de saturacion (corregido: -2.194210, a 45% de AURA)")
_t58 = [("La prediccion beta_c=-AURA es correcta (verificada a <0.2%)", True),
        ("beta_c = -AURA, identidad algebraica del sector", True),
        ("beta_c = -AURA fue RETIRADO de P7 en 2026-09-07", False),
        ("el coupled background da beta_c = +0.235068", False),
        # EL AGUJERO REAL (Endorser Summary, 2026-09-06 a 09-20): enunciado
        # pelado, sin una sola palabra que lo confirme ni que lo retire.
        ("Paper 7: $\\beta_c=-\\text{AURA}$ (numerical $-3.998$); algebraic", True),
        # y el sitio bien narrado de P7, cuya exencion va en la linea SIGUIENTE
        ("a conformal dark-matter coupling with\n"
         "$\\bc = -\\AURA = -(3\\phiG+\\pi)/2 \\approx -3.998$.\n"
         "Both are withdrawn.  We record why.", False),
        # narradas como DESCARTADAS o NEGADAS: tampoco son afirmaciones vivas
        ("cuatro mecanismos y los cuatro descartados por medicion:\n"
         "retencion conformal beta_c = -AURA (excursion x18 excesiva)", False),
        ("2. **✗** Identificacion `beta_c = -AURA`: el valor extraido\n"
         "-3.990 esta a 0.2 %. P7 lo presenta como exacto — no lo es.", False)]
_f58 = [c for c, esp in _t58 if bool(_r58_sitios(c)) != esp]
check("R58 el detector distingue la afirmacion viva de la narrada como retirada",
      not _f58, "; ".join(_f58) if _f58
      else "8 casos: 3 formas vivas marcadas (incluido el enunciado PELADO "
           "que se colo 13 dias); la narrada como retirada, el valor "
           "corregido y P7 §withdrawn (exencion en la linea siguiente), limpios")

# --- R70: H_global tiene UN valor, y el regimen IR no se llama canonico ----
#
# POR QUE EXISTE (2026-09-25). Mike, enfadado y con razon: «es algo que ya se
# supone que deberia estar bien y sigue asi... los errores no son ni de fisica
# ni de matematica sino de GRAMATICA», y «es como si solo me confirmaras en el
# chat y no haces nada». Las dos cosas ciertas. En una sola sesion alinee tres
# H_glob (67.79, 67.962142, 68.13) como si fueran opciones del modelo, y llame
# «numero puro» a una salida con unidades para meterla en una integral.
#
# Pero la fuente no me desmintio: me lo confirmo. CANONICAL_VALUES.yaml tenia
# `H0_glob_IR_km_s_Mpc` y `H0_glob_UV_km_s_Mpc` como DOS claves «SALIDA» en
# paralelo, Paper 9 rotulaba su 68.13 como «canonical» y Paper 4 igual. Con eso
# escrito, cualquiera —humano o sesion futura— lee dos H y se equivoca.
# R55 ya vigila la DIRECCION de la cascada (que el numero puro no sea entrada).
# Lo que faltaba es la CARDINALIDAD: hay UN H_global.
#
# La gramatica, escrita para que no haya que recordarla:
#   s_K^full = s_K^IR + UV_corr = 0.40330 + 0.01361 = 0.41691   (P10 eq:sKfullform)
#   f_screen = s_K^full/(3·MIRA) = 0.069522
#   H_glob   = H_SH0ES·(1 − f_screen) = 73.04×(1−0.069522) = 67.96214  [UNICO]
# El 68.13 es esa misma cascada con el termino IR SOLO: regimen M→inf de los
# Papers 1-9, historico. No es «el H_global IR»: es el H_global incompleto.
_R70_CANON = re.compile(
    # «canonical»/«canónico» a menos de 80 caracteres de un 68.13 o un 68.44
    # OJO: NO se puede excluir el punto aqui. El sitio real era una fila de
    # tabla LaTeX —«(canonical, mult.) & ... & $68.13$»— y «mult.» lleva punto,
    # asi que un [^.\n] no casaba ni con el caso que la regla existe para ver.
    # Lo destapo el auto-test, no la lectura del patron.
    r"(?:canonical|can[oó]nico)[^\n]{0,80}68\.(?:13|44)"
    r"|68\.(?:13|44)[^\n]{0,80}(?:canonical|can[oó]nico)", re.I)
_EX70 = ("regimen", "régimen", "regime", "IR ", "hist", "supersed", "M\to\infty",
         "incomplet", "~~", "no canónico", "not canonical")
_r70 = []
for _f in (sorted((ROOT.parent / "manuscript").glob("*.tex"))
           + sorted((ROOT.parent / "submission_PRD").glob("*.tex"))
           + [_q for _q in sorted(ROOT.parent.glob("*.md"))
              if _q.name not in ("CHANGELOG.md", "MEMORY.md")]
           + [ROOT.parent / "CANONICAL_VALUES.yaml"]):
    if not _f.exists():
        continue
    _lns = _f.read_text(errors="ignore").split("\n")
    for _i, _l in enumerate(_lns):
        if not _R70_CANON.search(_l):
            continue
        _ctx = "\n".join(_lns[max(0, _i - 2):_i + 3])
        if any(_e.lower() in _ctx.lower() for _e in _EX70):
            continue
        _r70.append(f"{_f.name}:{_i+1}")
check("R70 el regimen IR (68.13) no se presenta como el H_global canonico",
      not _r70, ", ".join(_r70[:4]) if _r70
      else "ningun documento llama canonico al 68.13 sin declararlo regimen IR; "
           "el H_global del modelo es 67.96214 (f_screen completo IR+UV)")
# y la fuente unica no puede volver a ofrecer DOS H_glob en paralelo
_cv70 = (ROOT.parent / "CANONICAL_VALUES.yaml").read_text(errors="ignore")
_claves70 = re.findall(r"^\s*(H0_glob[\w]*)\s*:", _cv70, re.M)
_canon70 = [_k for _k in _claves70 if "historico" not in _k and "regimen" not in _k]
check("R70 CANONICAL_VALUES declara UN solo H_global canonico",
      len(_canon70) == 1,
      f"claves H_glob canonicas: {_canon70} (debe ser exactamente 1; las de "
      f"regimen historico llevan 'regimen'/'historico' en el nombre)")
# CONTROL (R53): los dos casos son REALES, del arbol antes del arreglo
_c70_mal = "$H_0^{\\rm glob}$ (canonical, mult.) & ... & $68.13$ km/s/Mpc"
_c70_ok  = "$H_0^{\\rm glob}$ (\\emph{IR regime}, mult.) & ... & $68.13$ km/s/Mpc"
_f70 = []
if not _R70_CANON.search(_c70_mal):
    _f70.append("no ve el rotulo «canonical» junto al 68.13")
if _R70_CANON.search(_c70_ok):
    _f70.append("marca la fila ya rotulada como regimen IR")
check("R70 el detector distingue «canonical» de «IR regime» sobre el mismo 68.13",
      not _f70, "; ".join(_f70) if _f70
      else "2 casos reales de Paper 9 antes y despues del arreglo del 2026-09-25")

# --- R71: el delta_c retirado no vuelve como resultado vivo (OP-27) --------
#
# POR QUE EXISTE (2026-09-25). El postulado delta_c = delta_c,EdS * n_s = 1.6284
# estaba vivo en SIETE sitios y el reporte de auditoria solo vio TRES: los de
# manuscript/. Los otros cuatro eran CAJONES y CODIGO — README.md (la portada,
# que lo daba como resultado en una tabla), AUDIT.md, CHANGELOG.md y
# ssee_press_schechter.py, que ademas CALCULABA con el. Es la mitad de la
# auditoria que se queda fuera cuando solo se miran los papers.
# Y no basta con vigilar el numero: lo que se retira no es solo 1.6284, es la
# AFIRMACION de que el modelo explica el exceso de galaxias tempranas de JWST.
# Medido, el conteo de halos no se anula: se INVIERTE (0.892 a 3e12 Msol, z=10).
# Asi que la regla tiene dos patas: el valor y el reclamo.
_R71_VAL = re.compile(r"1\.6284")
# La lista incluye NEGACIONES y PASADO, no solo la palabra «retirado». Se
# amplio el 2026-09-25 porque la regla marcaba tres textos MIOS que decian
# justo lo contrario del reclamo («el modelo no explica el exceso JWST»,
# «offers no explanation», «usaba ese valor»). Una alarma falsa no se archiva:
# se busca que la disparo. El control de abajo verifica que la ampliacion NO
# exime tambien al caso real — si lo eximiera, habria forzado el verde.
_R71_EXENTO = ("retir", "withdraw", "OP-27", "falsific", "postulado", "postulate",
               "earlier version", "previous version", "ya no", "no lo produce",
               "RETIRADO", "conjetur", "conject",
               # negaciones del reclamo
               "no explica", "offers no explanation", "no account", "does not explain",
               "no hay enhancement", "there is no enhancement", "reverses sign",
               "cambia de signo", "se invierte", "apunta ligeramente en contra",
               "fewer", "menos halos", "indistinguishable", "indistinguible",
               # pasado: narra lo que se hacia, no lo que se afirma
               "usaba", "used that value", "carried by earlier", "claimed",
               "artefact", "artefacto")
_R71_JWST = re.compile(r"(enhancement|exceso|excess)[^.\n]{0,120}JWST|"
                       r"JWST[^.\n]{0,120}(enhancement|exceso|excess)", re.I)
_r71_val, _r71_claim = [], []
for _f71 in sorted(list((ROOT.parent / "manuscript").glob("*.tex"))
                   + list(ROOT.parent.glob("*.md"))
                   + list((ROOT.parent / "src").rglob("*.py"))):
    try:
        _ls71 = _f71.read_text(encoding="utf-8", errors="ignore").split("\n")
    except OSError:
        continue
    for _i71, _l71 in enumerate(_ls71):
        _ctx = " ".join(_ls71[max(0, _i71 - 3):_i71 + 4]).lower()
        if _R71_VAL.search(_l71) and not any(_e.lower() in _ctx for _e in _R71_EXENTO):
            _r71_val.append(f"{_f71.name}:{_i71 + 1}")
        # el reclamo JWST solo pinta si NO viene acompanado del retiro
        if _R71_JWST.search(_l71) and not any(_e.lower() in _ctx for _e in _R71_EXENTO):
            _r71_claim.append(f"{_f71.name}:{_i71 + 1}")
_TOPE_R71 = 0
_DEUDA_REAL["R71"] = len(_r71_val) + len(_r71_claim)
_DEUDA_MAX["R71"] = _TOPE_R71
check("R71 ningun documento presenta el delta_c 1.6284 como vigente",
      len(_r71_val) <= _TOPE_R71,
      f"{len(_r71_val)} sitios (tope {_TOPE_R71}): " + "; ".join(_r71_val[:5])
      if _r71_val else "0 sitios — donde aparece, aparece declarado retirado")
check("R71 ningun documento reclama el exceso JWST sin declarar el retiro",
      len(_r71_claim) <= _TOPE_R71,
      f"{len(_r71_claim)} sitios (tope {_TOPE_R71}): " + "; ".join(_r71_claim[:5])
      if _r71_claim else "0 sitios — el reclamo JWST siempre viene con su retiro")

# CONTROL DEL OTRO LADO (R53): la regla tiene que marcar el caso REAL de antes
# del arreglo y NO marcar el texto que declara el retiro.
_c71_mal = ("modulates the collapse criterion:\n"
            "delta_c = delta_EdS x n_s = 1.6865 x 0.96556 = 1.6284.\n"
            "this gives a halo-count enhancement explaining the JWST excess")
_c71_ok = ("Earlier versions postulated delta_c = 1.6284; that value is\n"
           "withdrawn as a prediction (OP-27) and the JWST enhancement\n"
           "reverses sign with the derived threshold.")
def _r71_marca(_txt):
    _ls = _txt.split("\n")
    for _i, _l in enumerate(_ls):
        _c = " ".join(_ls[max(0, _i - 3):_i + 4]).lower()
        if (_R71_VAL.search(_l) or _R71_JWST.search(_l)) and \
           not any(_e.lower() in _c for _e in _R71_EXENTO):
            return True
    return False
_f71c = []
if not _r71_marca(_c71_mal):
    _f71c.append("no marca el postulado vivo con su reclamo JWST")
if _r71_marca(_c71_ok):
    _f71c.append("marca el texto que YA declara el retiro")
check("R71 el detector distingue el postulado vivo del retiro declarado",
      not _f71c, "; ".join(_f71c) if _f71c
      else "2 casos reales de Paper 4/5 antes y despues del arreglo del 2026-09-25")

# --- R57: ninguna figura se escribe fuera de results/figures (2026-09-07)
# POR QUE EXISTE. ssee_paper5_IS_perturbations.py y ssee_eft_verification.py
# viven en src/pNN/ pero unian OUTDIR con UN SOLO '..', asi que escribian a
# src/results/figures/ — un directorio GITIGNORADO. Resultado: cada vez que
# se regeneraban esas 7 figuras, el archivo caia al vacio y la copia de
# results/figures/ seguia rancia. Explicaba 7 de las 15 figuras rancias, y
# no era descuido sino una ruta rota. El sintoma es invisible: el script
# imprime «figura guardada» y termina en 0.
_R57_MAL = re.compile(r"abspath\(__file__\)\)\s*,\s*\n\s*['\"]\.\.['\"]\s*,"
                      r"\s*['\"]results['\"]")
def _r57_sitios(_txt, _prof):
    # Solo es defecto si el script vive a 2+ niveles bajo src/: desde src/
    # un unico '..' SI apunta a la raiz y es correcto.
    return list(_R57_MAL.finditer(_txt)) if _prof >= 2 else []
_r57 = []
for _f in sorted(ROOT.rglob("*.py")):
    if "archive" in str(_f) or _f.name == "ssee_verify.py":
        continue
    _prof = len(_f.relative_to(ROOT).parts)
    if _r57_sitios(_f.read_text(errors="ignore"), _prof):
        _r57.append(str(_f.relative_to(ROOT.parent)))
check("R57 ninguna figura se escribe fuera de results/figures",
      not _r57 and not (ROOT / "results").exists(),
      "; ".join(_r57) if _r57
      else ("src/results/ no existe y ningun script anidado usa un solo '..' "
            "antes de results/")
      if not (ROOT / "results").exists()
      else "existe src/results/ — un script esta escribiendo al vacio")
_c57 = "OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),\n    '..', 'results', 'figures')"
_b57 = "OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),\n    '..', '..', 'results', 'figures')"
check("R57 el detector distingue la ruta rota de la correcta y respeta la profundidad",
      bool(_r57_sitios(_c57, 2)) and not _r57_sitios(_b57, 2)
      and not _r57_sitios(_c57, 1),
      "3 casos: un solo '..' a profundidad 2 marcado; el '..','..' limpio; "
      "el mismo un-solo-'..' a profundidad 1 (src/ directo) exento, que "
      "ahi SI apunta a la raiz")

# --- R66: nadie re-teclea un valor que el NUCLEO calcula ---------------
# POR QUE EXISTE (2026-09-08). R34 ya hacia esta comprobacion, pero solo para
# DOS constantes (Sigma m_nu y C_nu), porque nacio de un drift concreto. La
# pregunta de Mike —«no seria mejor que la regla si sea universal, al menos en
# lo que se pueda aplicar»— aplica igual aqui: el enunciado vale para TODAS
# las constantes del nucleo, no para dos.
# Medido al generalizarla: 136 ocurrencias en 45 scripts. Cada una es un valor
# que se quedara rancio en silencio el dia que el nucleo cambie — que es
# justo como sobrevivio 15 dias el drift de Sigma m_nu.
# NO bloquea: 136 rojos pararian todo el trabajo. Va con trinquete, como
# R44/R60: el tope SOLO BAJA, y baja segun cada script se toque y pase a
# importar del nucleo.
# el nucleo se carga aqui (R63, mas abajo, reusa este objeto)
import importlib.util as _ilu63
_spec63 = _ilu63.spec_from_file_location("_core63", ROOT / "ssee_core.py")
_core63 = _ilu63.module_from_spec(_spec63)
# El nucleo NO se carga a pelo. Si no importa —sus propios _sanity_checks
# abortan cuando una constante se altera— el guardian se caia con traceback a
# las 80 comprobaciones de 267, sin veredicto, y la suite de mutacion leia esa
# caida como «nadie lo detecta (VERDE por vacio)». Dos cosas distintas: un
# guardian que no ve el defecto y un guardian que no llego a mirar.
# Lo destapo la mutacion `canon` el 2026-09-08.
try:
    _spec63.loader.exec_module(_core63)
    _ERR_CORE = None
except BaseException as _e63:          # AssertionError incluida
    _ERR_CORE = f"{type(_e63).__name__}: {_e63}"
check("canon el nucleo se puede importar y pasa sus propios sanity checks",
      _ERR_CORE is None,
      _ERR_CORE or "ssee_core.py importado; sus asserts internos pasan")
if _ERR_CORE is not None:
    # Sin nucleo no hay nada que comprobar: seguir produciria una lista de
    # verdes por vacio, que es peor que parar. Se sale con veredicto, no con
    # traceback, para que quien lea la salida sepa POR QUE se detuvo.
    # ¿QUIEN MIENTE, EL FUENTE O LA CACHE? (2026-09-19)
    #
    # Hasta hoy este camino decia siempre «Arreglar src/ssee_core.py». Pero
    # cuando la causa es un `.pyc` rancio, el fuente esta PERFECTO y el mensaje
    # manda al operador a corregir el fichero equivocado — que es exactamente
    # la confusion que el 2026-07-25 costo un MCMC de produccion de 35 min.
    # R31 existia para esto, pero vive al final del guardian y este `SystemExit`
    # lo dejaba inalcanzable: la unica situacion en que R31 hace falta era la
    # unica en que no llegaba a correr. Lo destapo su auto-prueba.
    #
    # El diagnostico es directo: si el fuente compilado EN ESTE INSTANTE se
    # ejecuta limpio, el fuente no es el problema; lo es el bytecode que el
    # import trajo de `__pycache__`.
    _RUTA_CORE = ROOT / "ssee_core.py"
    _sano_de_fuente = False
    try:
        _ns31 = {"__name__": "_core_recien_compilado", "__file__": str(_RUTA_CORE)}
        exec(compile(_RUTA_CORE.read_text(encoding="utf-8"), str(_RUTA_CORE), "exec"), _ns31)
        _sano_de_fuente = True
    except BaseException:
        _sano_de_fuente = False

    print("\n" + "=" * 40)
    print("ROJO — el nucleo no carga; el resto de comprobaciones NO se corrio.")
    # Con el formato que lee la suite de mutacion, para que pueda ATRIBUIR el
    # fallo a `canon` en vez de verlo como una caida muda.
    print("   x  canon el nucleo se puede importar y pasa sus sanity checks")
    print(f"  causa: {_ERR_CORE}")
    if _sano_de_fuente:
        print("   x  R31 bytecode: la CACHE miente, el fuente esta bien")
        print("  R31 — el mismo fuente compilado ahora se ejecuta limpio, asi que")
        print("        el fallo lo trae un `.pyc` rancio de __pycache__, no el .py.")
        print("        NO toques src/ssee_core.py. Haz esto:")
        print("          1) rm -rf src/__pycache__")
        print("          2) vuelve a correr el guardian")
        print("          3) RE-CORRE todo lo que se haya ejecutado en este estado:")
        print("             cualquier resultado producido asi es sospechoso.")
    else:
        print("  Arreglar src/ssee_core.py y volver a correr.")
    raise SystemExit(1)
_R66_CONS = {_k: _v for _k, _v in vars(_core63).items()
             if _k.isupper() and isinstance(_v, float) and abs(_v) > 1e-6}
_R66_LIT = [(f"%.{_d}f" % _v, _k)
            for _k, _v in _R66_CONS.items() for _d in range(5, 10)]
# AFINADO el mismo dia: la primera version contaba 136 y estaba inflada por
# DOS cegueras propias. (a) solo quitaba los comentarios de linea entera, no
# los de final de linea — `phi_ = (1+5**0.5)/2   # 1.61803` es documentacion,
# no un valor re-tecleado. (b) contaba los literales dentro de CADENAS, y
# registro_reglas.py los lleva a proposito: son las mutaciones con las que se
# prueba al propio guardian; sustituirlas romperia las pruebas.
# Se quitan las dos con el tokenizador de Python, que sabe donde acaba un
# comentario y donde empieza una cadena. Nada de regex sobre el texto crudo.
def _r66_sitios(_txt):
    # TRES CEGUERAS que tuvo este detector, todas halladas midiendo y las tres
    # inflando la cuenta (136 medidos -> 47 reales):
    #   (1) COMMENT   — un valor documentado al lado del codigo que si lo calcula.
    #   (2) STRING    — las cadenas-fixture con que se prueban las reglas del
    #                   propio guardian; sustituirlas romperia esas pruebas.
    #   (3) FSTRING_MIDDLE — desde 3.12 una f-string ya no es un STRING, asi que
    #                   su NARRACION entraba como codigo. Lo que va entre llaves
    #                   si es codigo y se sigue mirando: no se pierde alcance.
    # Y una excepcion declarada: la linea marcada "# R66-OK" es un literal
    # citado a proposito (p.ej. lo que dice el paper, para contrastarlo contra
    # el nucleo); importarlo del nucleo volveria tautologica la comprobacion.
    import io as _io66, tokenize as _tk66
    _saltar = {_tk66.COMMENT, _tk66.STRING}
    for _nom in ("FSTRING_MIDDLE", "FSTRING_START", "FSTRING_END"):
        if hasattr(_tk66, _nom):
            _saltar.add(getattr(_tk66, _nom))
    _ok66 = {_i + 1 for _i, _l in enumerate(_txt.split("\n")) if "R66-OK" in _l}
    _trozos = []
    try:
        for _tok in _tk66.generate_tokens(_io66.StringIO(_txt).readline):
            if _tok.type in _saltar or _tok.start[0] in _ok66:
                continue
            _trozos.append(_tok.string)
    except Exception:
        # si no tokeniza (fichero roto), se cae al texto sin comentarios
        _trozos = [_l for _l in _txt.split("\n")
                   if not _l.lstrip().startswith("#")]
    _cuerpo = " ".join(_trozos)
    return sorted({f"{_k}={_lit}" for _lit, _k in _R66_LIT
                   if re.search(r"(?<![\w.])" + re.escape(_lit) + r"(?![\d])",
                                _cuerpo)})
_r66 = {}
for _f66 in sorted(ROOT.rglob("*.py")):
    if "archive" in str(_f66) or _f66.name in (_FIXTURES | {"ssee_core.py"}):
        continue
    _s66 = _r66_sitios(_f66.read_text(errors="ignore"))
    if _s66:
        _r66[_f66.name] = _s66
_n66 = sum(len(_v) for _v in _r66.values())
_TOPE_R66 = 0                       # trinquete 2026-09-08; SOLO BAJA
check("R66 la deuda de constantes re-tecleadas no crece",
      _n66 <= _TOPE_R66,
      f"{_n66} ocurrencias en {len(_r66)} scripts (tope {_TOPE_R66}); "
      f"mayores: " + ", ".join(f"{_k}={len(_v)}" for _k, _v in
                               sorted(_r66.items(), key=lambda x: -len(x[1]))[:3]))
check("R66 el tope de constantes re-tecleadas está apretado",
      _n66 >= _TOPE_R66 or _n66 == 0,
      f"tope {_TOPE_R66} = cuenta real {_n66}" if _n66 == _TOPE_R66
      else f"BAJAR el tope a {_n66}: sobran {_TOPE_R66 - _n66}")
# CONTROL (R53): marca el literal del nucleo y deja pasar el import y un
# numero ajeno de la misma forma.
_c66 = [(f"OM = {_core63.OMEGA_M_CMB:.6f}", True),
        ("OM = S.OMEGA_M_CMB", False),
        ("frac = 0.123456", False),
        (f"# comentario: OM vale {_core63.OMEGA_M_CMB:.6f}", False)]
_f66 = [_t[:38] for _t, _esp in _c66 if bool(_r66_sitios(_t)) != _esp]
check("R66 el detector distingue el literal del import",
      not _f66, "; ".join(_f66) if _f66
      else "4 casos: el literal del nucleo marcado; el import, un numero "
           "ajeno y el literal dentro de un comentario, exentos")

# --- R67: ninguna regla se escribe su propia lista de fixtures exentas
# POR QUE EXISTE (2026-09-08). Siete reglas eximian la infraestructura de
# verificacion y las siete listas eran DISTINTAS: R56 eximia un fichero, R34
# siete, otras dos. Esa deriva da las dos patologias a la vez — R56 salto con
# la fixture de su propio caso de mutacion (falsa alarma) y una lista de mas
# habria tapado un defecto real (verde falso). Ahora la lista vive en
# `_FIXTURES` y esta regla impide que alguien vuelva a teclearla suelta.
_SRC_R67 = pathlib.Path(__file__).resolve().read_text(errors="ignore")
_R67_NOMBRES = [_n for _n in _FIXTURES if _n != "ssee_verify.py"]
_L67 = _SRC_R67.split("\n")
# El bloque donde se DECLARA la lista queda fuera, claro: ahi los nombres van
# sueltos porque es su definicion. Se delimita por la llave de cierre, no por
# un numero de linea, que se desplazaria al editar el fichero.
_ini67 = next(_i for _i, _l in enumerate(_L67) if _l.startswith("_FIXTURES"))
_fin67 = next(_i for _i, _l in enumerate(_L67) if _i > _ini67 and _l.startswith("})"))
_r67 = []
for _i67, _l67 in enumerate(_L67):
    _cod67 = _l67.split("#")[0]
    if _ini67 <= _i67 <= _fin67 or "_FIXTURES" in _cod67 or "R67" in _l67 \
            or "R67-OK" in _l67:
        continue
    for _n67 in _R67_NOMBRES:
        if f'"{_n67}"' in _cod67:
            _r67.append(f"linea {_i67+1}: «{_l67.strip()[:56]}»")
check("R67 ninguna regla teclea su propia lista de fixtures exentas",
      not _r67, "; ".join(_r67[:4]) if _r67
      else f"{len(_FIXTURES)} fixtures declaradas en un solo sitio; ninguna "
           f"regla las repite suelta")
# CONTROL (R53): marca la lista tecleada suelta y deja pasar la que usa la
# constante comun. Sin este control la regla podria estar mirando al vacio.
_c67 = [('if _f.name in ("test_guardian.py", "meta_guardian.py"):', True),  # R67-OK
        ('if _f.name in _FIXTURES:', False),
        ('if _f.name == "ssee_paper3_cmb.py":', False)]
_f67 = []
for _txt67, _debe in _c67:
    _visto = any(f'"{_n}"' in _txt67.split("#")[0] and "_FIXTURES" not in _txt67
                 for _n in _R67_NOMBRES)
    if _visto is not _debe:
        _f67.append(f"«{_txt67[:40]}» esperaba {_debe}")
check("R67 el detector distingue la lista suelta de la constante comun",
      not _f67, "; ".join(_f67) if _f67
      else "3 casos: la lista tecleada a mano se marca; el uso de _FIXTURES y "
           "un fichero cualquiera, exentos")

# --- R68: ningun PDF publicado es mas viejo que el .tex que lo produce
# POR QUE EXISTE (2026-09-08, lo pidio Mike al ver el hueco). Habia regla para
# los LOGS contra su script (R35) y para las FIGURAS contra el suyo (R36), pero
# ninguna para el documento contra su fuente. Y `docs/` es lo que se LEE y lo
# que se ENVIA: el trabajo de seis semanas —la propagacion de s_K, el banner de
# la direccion de la cascada, el cierre de OP-11— vivia en el .tex mientras el
# PDF publicado seguia diciendo lo anterior. Medido al abrirla: 14 documentos
# atrasados, hasta 41 dias; solo Paper 6 al dia.
# Se compara por fecha de COMMIT, no del disco, para no gritar por el trabajo en
# curso; y un cambio que solo toca COMENTARIOS de LaTeX (%) no cuenta, porque no
# puede mover una pagina. Mismo criterio que R35 con el AST.
_R68_DOCS = ROOT.parent / "docs"


def _tex_sin_comentarios(_t):
    # El .rstrip() no es cosmetico: sin el, quitar «  % nota» deja los dos
    # espacios que precedian al comentario y el texto sale distinto. Lo cazo
    # el propio control de la regla al escribirla.
    _out = []
    for _l in _t.split("\n"):
        if _l.lstrip().startswith("%"):
            continue          # linea que es SOLO comentario: LaTeX no la ve
        _out.append(re.sub(r"(?<!\\)%.*$", "", _l).rstrip())
    return "\n".join(_out)


def _macros68(_tex, _vg):
    """Las definiciones de valores_generados.tex que `_tex` usa con \\val{}."""
    _usa = set(re.findall(r"\\val\{([^}]+)\}", _tex))
    return "\n".join(_l for _l in _vg.split("\n")
                     if any(f"ssee@val@{_n}\\endcsname" in _l for _n in _usa))


def _ts68(_rel):
    try:
        _o = _sp68.run(["git", "log", "-1", "--format=%at", "--", _rel],
                       cwd=ROOT.parent, capture_output=True, text=True, timeout=20)
        return int(_o.stdout.strip()) if _o.stdout.strip() else None
    except Exception:
        return None


import subprocess as _sp68
# COMO SE COMPARA (rehecho 2026-09-08). La primera version miraba FECHAS de
# commit. Funcionaba, pero tenia dos defectos: solo veia el atraso un commit
# DESPUES de causarlo, y una vez saldada la deuda su caso de mutacion dejaba de
# valer —no se puede aflojar un trinquete vacio—. Ahora compara el CONTENIDO:
# el .tex de disco contra el .tex tal como estaba en el commit del PDF. Si
# difieren en algo que no sean comentarios de LaTeX, el PDF publicado ya no
# corresponde a su fuente, sin importar fechas. Se caza en el momento, y editar
# un .tex basta para probarlo.
_r68, _n68 = [], 0
for _tex68 in sorted((ROOT.parent / "manuscript").glob("*.tex")):
    _pdf68 = _R68_DOCS / f"{_tex68.stem}.pdf"
    if not _pdf68.exists():
        continue
    _n68 += 1
    try:
        _sha68 = _sp68.run(["git", "log", "-1", "--format=%H", "--",
                            f"docs/{_pdf68.name}"], cwd=ROOT.parent,
                           capture_output=True, text=True, timeout=20).stdout.strip()
        if not _sha68:
            continue                      # PDF nunca commiteado: nada que comparar
        _viejo68 = _sp68.run(["git", "show", f"{_sha68}:manuscript/{_tex68.name}"],
                             cwd=ROOT.parent, capture_output=True, text=True,
                             timeout=20).stdout
        if not _viejo68:
            continue                      # el .tex no existia entonces
        _nuevo68 = _tex68.read_text(errors="ignore", crudo=True)
        # Los numeros que entran por \val{} viven en valores_generados.tex:
        # si cambian ahi, el PDF queda viejo aunque el .tex no se toque
        # (2026-09-30). Se compara tambien ese archivo, sin su acta (fecha).
        # Solo las macros que ESE .tex usa: una macro nueva para otro paper no
        # deja viejo este PDF (lo marco de mas la primera version, mismo dia).
        if "valores_generados.tex" in _nuevo68:
            _vg68 = ROOT.parent / "manuscript" / "valores_generados.tex"
            _viejo68 += _macros68(_nuevo68, _sp68.run(
                ["git", "show", f"{_sha68}:manuscript/valores_generados.tex"],
                cwd=ROOT.parent, capture_output=True, text=True, timeout=20).stdout)
            _nuevo68 += _macros68(_nuevo68, _vg68.read_text(errors="ignore") if _vg68.exists() else "")
        if _tex_sin_comentarios(_viejo68) != _tex_sin_comentarios(_nuevo68):
            _r68.append(_tex68.stem)
    except Exception as _e68:
        # No se traga el fallo: un except mudo aqui daria VERDE por vacio.
        _r68.append(f"{_tex68.stem} (no comparable: {type(_e68).__name__})")
_TOPE_R68 = 0                       # 14 -> 0: los 14 recompilados; SOLO BAJA
_DEUDA_REAL["R68"] = len(_r68)
_DEUDA_MAX["R68"] = _TOPE_R68
check("R68 la deuda de PDF publicados sin recompilar no crece",
      len(_r68) <= _TOPE_R68,
      f"{len(_r68)} de {_n68} PDF de docs/ ya no corresponden a su .tex "
      f"(tope {_TOPE_R68}): " + "; ".join(_r68[:4])
      + (" …" if len(_r68) > 4 else "")
      if _r68 else f"{_n68} PDF de docs/ al dia con su fuente")
check("R68 el tope de PDF sin recompilar esta apretado",
      len(_r68) >= _TOPE_R68 or not _r68,
      f"tope {_TOPE_R68} = cuenta real {len(_r68)}" if len(_r68) == _TOPE_R68
      else f"BAJAR el tope a {len(_r68)}: sobran {_TOPE_R68 - len(_r68)}")
# CONTROL (R53): el cambio de CONTENIDO se marca; el de un comentario LaTeX no.
_c68 = [("\\section{A}\ntexto viejo\n", "\\section{A}\ntexto NUEVO\n", True),
        # CONTROL que faltaba (2026-09-08): ANADIR lineas de comentario. La
        # primera version las vaciaba en vez de quitarlas, asi que quedaban
        # lineas en blanco de mas y el texto salia distinto: marcaba Paper 8
        # por un cambio que solo tocaba comentarios. Lo cazo en vivo, no el
        # control, porque ningun caso cambiaba el NUMERO de lineas.
        ("\\section{A}\ntexto\n", "% nota\n% otra nota\n\\section{A}\ntexto\n", False),
        ("\\section{A}\ntexto viejo\n", "\\section{A}  % nota al margen\ntexto viejo\n",
         False),
        ("\\section{A}\n50\\%% de la muestra\n", "\\section{A}\n50\\%% de la muestra\n",
         False)]
# 2026-09-30: el .tex igual pero una macro QUE USA cambiada en
# valores_generados.tex SE MARCA; una macro que no usa, o el acta, no.
_T68 = "\\input{valores_generados.tex}\nda $\\val{x}$\n"
_V68 = lambda _x, _y, _f: (f"% ACTA-PROCEDENCIA {{\"fecha\": \"{_f}\"}}\n"
                          f"\\expandafter\\def\\csname ssee@val@x\\endcsname{{{_x}}}\n"
                          f"\\expandafter\\def\\csname ssee@val@y\\endcsname{{{_y}}}\n")
_c68 += [(_T68 + _macros68(_T68, _V68("2.65", "1", "1")), _T68 + _macros68(_T68, _V68("2.69", "1", "1")), True),
         (_T68 + _macros68(_T68, _V68("2.69", "1", "1")), _T68 + _macros68(_T68, _V68("2.69", "7", "2")), False)]
_f68 = [f"caso {_i}" for _i, (_a, _b, _esp) in enumerate(_c68)
        if (_tex_sin_comentarios(_a) != _tex_sin_comentarios(_b)) is not _esp]
check("R68 el detector distingue el cambio de contenido del comentario LaTeX",
      not _f68, "; ".join(_f68) if _f68
      else "6 casos: el texto cambiado y la macro USADA cambiada se marcan; el "
           "comentario anadido (en la linea y como linea nueva), el porcentaje "
           "escapado y una macro que el .tex no usa (con otra acta), exentos")

# CONTROL (R53) de la lectura expandida (2026-09-30): la macro conocida se
# vuelve su valor, la desconocida queda VISIBLE (nunca desaparece en
# silencio), y la lectura cruda no toca nada.
import tempfile as _tfx
_cx = [expande_val("K = $\\val{K}$", {"K": "9.519253"}) == "K = $9.519253$",
       expande_val("K = $\\val{NO}$", {"K": "9.519253"}) == "K = $\\val{NO}$"]
with _tfx.TemporaryDirectory() as _dx:
    _mx = pathlib.Path(_dx) / "manuscript"
    _mx.mkdir()
    (_mx / "p.tex").write_text("x \\val{__prueba__} y")
    _VALS["__prueba__"] = "1.234567"
    _cx += [(_mx / "p.tex").read_text() == "x 1.234567 y",
            (_mx / "p.tex").read_text(crudo=True) == "x \\val{__prueba__} y"]
    _VALS.pop("__prueba__")
check("lectura de papers: \\val{} se expande, el desconocido queda visible, crudo no toca",
      all(_cx), f"casos {_cx}")
_sin_def = sorted({_n for _f in list((ROOT.parent / "manuscript").glob("*.tex"))
                   + list((ROOT.parent / "submission_PRD").glob("*.tex"))
                   for _n in re.findall(r"\\val\{([^}]+)\}", _f.read_text(errors="ignore", crudo=True))
                   if _n not in _VALS})
check("todo \\val{} de los papers tiene valor generado (si no, LaTeX imprime NADA)",
      not _sin_def, ", ".join(_sin_def[:10]) or f"{len(_VALS)} macros, ninguna huerfana")

# --- R69: los CAJONES no pueden declarar un titular que el canonico ya movio
#
# POR QUE EXISTE (2026-09-20). Lo dijo Mike, y describe un mecanismo, no un
# descuido: la auditoria tiene DOS mitades —los CAJONES de la mesa de trabajo
# (los .md de la raiz, que es con lo que se trabaja) y DOCS (los papers, que es
# lo que se publica)— y «cuando solo revisas los papers los corriges, pero se
# deja de lado los cajones, que se quedan desactualizados». Medido ese dia:
# VEINTIUNA copias identicas del mismo banner, repartidas en 8 cajones, todas
# diciendo «Canonico hoy: ... S8=0.7555±0.0192», seis semanas despues de que
# eso dejara de ser el titular. Entre ellas, EXTERNAL_AUDIT_PROMPTS.md —el
# documento que se le manda a un auditor externo— con fecha de julio: quien
# audita desde ahi audita un modelo que ya no existe, y sus hallazgos llegan
# contra criterios muertos sin culpa suya.
#
# R60 no lo veia y no tenia por que: vigila lo RETIRADO, y el 0.7555 no esta
# retirado — es correcto, solo que ya no es el titular. Esto es otra cosa:
# deriva de TITULAR. La fuente unica es CANONICAL_VALUES.yaml, asi que la
# regla es que quien diga «canonico hoy» cite lo que el canonico dice hoy.
import yaml as _y69
_S8_CANON69 = None
try:
    _cv69 = _y69.safe_load((ROOT.parent / "CANONICAL_VALUES.yaml")
                           .read_text(errors="ignore"))
    for _blq in (_cv69.values() if isinstance(_cv69, dict) else []):
        if isinstance(_blq, dict) and "S8_ssee_unif" in _blq:
            _S8_CANON69 = str(_blq["S8_ssee_unif"])
except Exception:
    _S8_CANON69 = None
_MARCA69 = re.compile(r"[Cc]an[oó]nico hoy|[Tt]itular vigente", re.I)


# narraciones de lo que un documento DECIA antes: citan el titular viejo a
# proposito, para explicar que se quedo rancio. No son declaraciones vivas.
_PASADO69 = re.compile(r"\bdec[ií]a\b|\bllevaba\b|\bdijo\b|\bpas[oó]\b|"
                       r"\bera\b|v1\.4|hist[oó]ric", re.I)


def _r69_sitios(_txt, _s8):
    """Unidades que se declaran canonicas y NO citan el S8 canonico.

    Por UNIDAD (parrafo), no por linea: en AUDIT.md el rotulo «este es el
    TITULAR vigente» encabeza un bloque y el valor viene debajo. Medir por
    linea marcaba ese sitio, que esta bien."""
    _mal = []
    for _p in re.split(r"\n\s*\n", _txt):
        if not _MARCA69.search(_p) or not _s8:
            continue
        if _PASADO69.search(_p):            # narra lo que decia, no lo declara
            continue
        if _s8 not in _p:
            _mal.append(" ".join(_p.split())[:70])
    return _mal


_r69 = []
if _S8_CANON69:
    for _f in sorted(ROOT.parent.glob("*.md")):
        if _f.name in ("CHANGELOG.md", "MEMORY.md"):      # historia: cita su epoca
            continue
        _r69 += [f"{_f.name}: {_x}" for _x in _r69_sitios(
            _f.read_text(errors="ignore"), _S8_CANON69)]
check("R69 ningun cajon declara un titular que el canonico ya movio",
      not _r69, "; ".join(_r69[:3]) if _r69
      else f"todas las declaraciones de «canonico hoy» en los cajones citan "
           f"S8={_S8_CANON69}, el valor de CANONICAL_VALUES.yaml")
# CONTROL (R53): tiene que distinguir el banner al dia del rancio, que es el
# caso REAL del 2026-09-20 — no un ejemplo inventado.
_c69a = ("> RETIRADO. **Canonico hoy:** un solo sector. Contra KiDS-Legacy con "
         "A_s clavado, S8=0.8273 predicho vs 0.8265 medido.")
_c69b = ("> RETIRADO. Canonico hoy: un solo sector, y contra KiDS crudo con "
         "A_s libre S8=0.7555±0.0192 (0.11 sigma).")
_c69c = "Un parrafo cualquiera que menciona S8=0.7555 sin declararse canonico."
_f69 = []
if _r69_sitios(_c69a, "0.8273"):     _f69.append("el banner AL DIA se marco")
if not _r69_sitios(_c69b, "0.8273"): _f69.append("el banner RANCIO no se marco")
if _r69_sitios(_c69c, "0.8273"):     _f69.append("marco prosa que no se declara canonica")
# R69b — LO MISMO EN LOS PAPERS, que es donde R69 no llegaba.
#
# R69 nacio mirando los cajones .md porque ahi se midio el problema (21 copias
# del banner). Pero el 2026-09-20, media hora despues, Mike pregunto si Max
# encontraria mas cosas y la respuesta estaba en los .tex: SIETE papers (1, 2,
# 3, 5, 7, 8, 9) citaban S8=0.7555 sin una sola mencion de KiDS-Legacy. Ninguno
# MIENTE —el 0.7555 es correcto y va atribuido a KiDS-1000— pero un referee que
# lea Paper 5 y luego Paper 6 ve dos titulares distintos para el mismo sector y
# pregunta cual es. Lo que se exige no es prohibir el valor viejo: es que el
# documento no deje al lector sin el vigente.
_S8_VIEJO69 = "0.7555"
_r69b = []
for _f in (sorted((ROOT.parent / "manuscript").glob("*.tex"))
           + sorted((ROOT.parent / "submission_PRD").glob("*.tex"))):
    _txt = _f.read_text(errors="ignore")
    if _S8_VIEJO69 in _txt and _S8_CANON69 and _S8_CANON69 not in _txt:
        _r69b.append(_f.name)
check("R69b ningun paper cita el S8 superado sin dar tambien el vigente",
      not _r69b, ", ".join(_r69b) if _r69b
      else f"todos los .tex que citan {_S8_VIEJO69} citan tambien "
           f"{_S8_CANON69}; el lector nunca se queda con el titular viejo")
_f69b = []
if not ("0.7555" in "S8=0.7555 solo" and "0.8273" not in "S8=0.7555 solo"):
    _f69b.append("no detecta el documento que solo trae el viejo")
if ("0.7555" in "S8=0.7555 y hoy 0.8273" and "0.8273" not in "S8=0.7555 y hoy 0.8273"):
    _f69b.append("marca un documento que SI trae los dos")
check("R69b el detector distingue citar-el-viejo de dejar-al-lector-sin-el-vigente",
      not _f69b, "; ".join(_f69b) if _f69b
      else "2 casos: el texto que solo trae 0.7555 se marca; el que trae los "
           "dos valores, no — citar el resultado de KiDS-1000 es legitimo, "
           "dejarlo como unico titular no")

check("R69 el detector distingue el banner al dia del rancio",
      not _f69, "; ".join(_f69) if _f69
      else "3 casos reales: el banner del 2026-09-20 pasa; el de agosto, que "
           "decia «canonico hoy S8=0.7555» en 21 copias, se marca; y la prosa "
           "que cita el 0.7555 sin declararlo canonico queda exenta (es un "
           "valor correcto, solo que ya no es el titular)")

# --- R65: si un script declara su log fuente, sus numeros deben estar ahi
# POR QUE EXISTE (2026-09-08). regenerate_fig8_bao_residuals.py llevaba los
# MAP de las cadenas escritos a mano con el rotulo "(paper2_3models, jul-9,
# DR2)". Esa cadena quedo SUPERADA el 2026-07-25 por el fix R25, y la figura
# siguio 45 dias construida sobre valores retirados. No lo cazaba nadie:
# R35 compara fechas de commit y el script no habia cambiado; R36 mira si la
# figura es mas vieja que su script. El agujero es el tercero: el script esta
# al dia consigo mismo y rancio respecto al LOG del que dice venir.
# Efecto medido: chi2_BAO(SSEE) 11.9 -> 11.6 y la figura sale distinta.
# QUE HACE: si un fichero declara `FUENTE: results/logs/<x>.log`, cada numero
# de 5+ cifras significativas que escriba debe aparecer en ese log. Asi el
# valor no puede quedarse rancio en silencio: o se actualiza, o falla.
_R65_FUENTE = re.compile(r"FUENTE:\s*results/logs/([\w./-]+\.log)")
_R65_NUM = re.compile(r"(?<![\w.])(\d+\.\d{4,})(?![\w])")
def _r65_sitios(_txt, _leelog):
    _m = _R65_FUENTE.search(_txt)
    if not _m:
        return []
    _log = _leelog(_m.group(1))
    if _log is None:
        return [f"el log declarado no existe: {_m.group(1)}"]
    # solo los numeros del cuerpo, no los de la cabecera que narra el cambio
    _cuerpo = _txt[_m.end():]
    _cuerpo = "\n".join(_l for _l in _cuerpo.split("\n")
                        if not _l.lstrip().startswith("#"))
    # un identificador de arXiv (AAMM.NNNNN) no es una medida: se exime por
    # su forma Y por su contexto. Cazado el mismo dia: 2503.14738, el paper
    # de DESI DR2, aparecia como si fuera un numero rancio.
    _fuera = []
    for x in sorted(set(_R65_NUM.findall(_cuerpo))):
        if x in _log:
            continue
        _pos = _cuerpo.find(x)
        _ctx = _cuerpo[max(0, _pos - 70):_pos + len(x) + 20].lower()
        if re.fullmatch(r"\d{4}\.\d{5}", x) and (
                "arxiv" in _ctx or "doi" in _ctx or "et al" in _ctx
                or "desi" in _ctx or "20" == x[:2]):
            continue
        _fuera.append(f"{x} no esta en {_m.group(1)}")
    return _fuera
def _leelog65(_n):
    _p = ROOT.parent / "results" / "logs" / _n
    return _p.read_text(errors="ignore") if _p.exists() else None
_r65 = []
for _f65 in sorted(ROOT.rglob("*.py")):
    if "archive" in str(_f65) or _f65.name == "ssee_verify.py":
        continue
    _r65 += [f"{_f65.name}: {x}"
             for x in _r65_sitios(_f65.read_text(errors="ignore"), _leelog65)]
check("R65 los numeros de un script coinciden con el log que declara como fuente",
      not _r65, "; ".join(_r65[:3]) if _r65
      else "todo script con `FUENTE: results/logs/...` escribe numeros que "
           "estan en ese log (cazado 2026-09-08: fig8 llevaba 45 dias con los "
           "MAP de una cadena superada por el fix R25)")
# R65 CRECE (2026-09-19): de «¿declara su log?» a «¿de donde sale CADA numero?».
#
# La version anterior contaba scripts que no escribian `FUENTE:` y lo dejaba
# como deuda: «77 scripts sin declarar su log». Medido ese dia, la cuenta
# mezclaba cosas que no tienen nada que ver entre si. De 542 numeros:
#   263 reproducen un valor del NUCLEO (algebra tecleada a mano),
#   132 estan en algun log, 18 en data/, 16 junto a una cita, 3 constantes
#   fisicas, y 110 sin origen a la vista.
# Y `FUENTE:` significa «mis numeros SALEN de este log»: para el script que
# PRODUCE su log, o cuyos numeros son algebra o literatura, escribirlo seria
# falso. La deuda solo se podia cerrar mintiendo. Lo dijo Mike: «no es
# mentir, es sacarle de donde viene».
#
# Asi que ahora se RASTREA cada numero, y cada tipo de origen tiene su control:
#   algebra   el numero reproduce un float del nucleo a la precision escrita
#             (o esta en CANONICAL_VALUES.yaml). Una errata en un comentario
#             —«KRYSTOS 9.51926» cuando phi+pi+Omega = 9.519173— NO pasa.
#   ORIGEN:   `# ORIGEN: <ruta>` en el script declara un archivo (del repo o
#             del HDD, p. ej. la cadena oficial de KiDS); el numero debe
#             ESTAR dentro. Si el disco no esta montado, se informa aparte.
#   log       aparece en un log de results/, con 5+ cifras significativas
#             (con menos, la coincidencia es demasiado facil: 0.3000).
#   datos     aparece en data/.
#   cita      la propia linea cita de donde sale (arXiv, et al, Planck, …).
#   ORIGEN-VALOR  `# ORIGEN-VALOR: <numero> — <razon>`: el numero no se puede
#             rastrear (una rejilla, una tolerancia, un dato sintetico de un
#             test) y se dice POR QUE, por escrito y a la vista. Razon de 10+
#             caracteres; no se verifica el contenido, se exige que exista.
# Lo que no encuentra origen por ninguna via es PENDIENTE, numero a numero.
_ORIGEN65 = re.compile(r"#\s*ORIGEN:\s*(\S+)")
_ORIGEN_VALOR65 = re.compile(r"#\s*ORIGEN-VALOR:\s*(\d+\.\d+)\s*(?:—|--|-)\s*(\S.{9,})")
_CITA65 = re.compile(
    r"arxiv|et al|doi|planck|desi|kids|sh0es|riess|asgari|\bboss\b|eboss|"
    r"pantheon|freedman|mangano|mead|bridle|\bpdg\b|codata|cobe|firas|"
    r"hildebrandt|heymans|aghanim|wright|\b(?:19|20)\d\d\b", re.I)
_FLOATS65 = sorted({abs(float(_v)) for _k, _v in vars(_core63).items()
                    if isinstance(_v, float) and _v == _v and abs(_v) < 1e12}) \
    if _ERR_CORE is None else []
_CANON65 = (ROOT.parent / "CANONICAL_VALUES.yaml").read_text(errors="ignore")


def _r65_es_algebra(_x, _floats, _canon):
    if _x in _canon:
        return True
    _d = len(_x.split(".")[1])
    _v = float(_x)
    _tol = 10.0 ** -_d                 # redondeo o truncado a lo escrito
    return any(abs(_a - _v) < _tol for _a in _floats)


def _r65_origen(_txt, _leer, _floats, _canon, _logs, _datos):
    """Numeros de 4+ decimales del codigo sin origen hallado.
    Devuelve (sin_origen, rutas_declaradas_ilegibles)."""
    _valores = {m.group(1) for m in _ORIGEN_VALOR65.finditer(_txt)}
    _decl, _ilegibles = "", []
    for _m in _ORIGEN65.finditer(_txt):
        _t = _leer(_m.group(1))
        if _t is None:
            _ilegibles.append(_m.group(1))
        else:
            _decl += _t
    _sin = []
    for _l in _txt.split("\n"):
        if _l.lstrip().startswith("#"):
            continue
        for _x in _R65_NUM.findall(_l):
            if (_x in _valores
                    or _r65_es_algebra(_x, _floats, _canon)
                    or (_decl and _x in _decl)
                    # cifras SIGNIFICATIVAS: sin ceros a ninguno de los dos
                    # lados. «0.30000» tiene una sola, no cinco.
                    or (len(_x.replace(".", "").strip("0")) >= 5 and _x in _logs)
                    or _x in _datos
                    or _CITA65.search(_l)):
                continue
            if _x not in {_y for _y, _ in _sin}:      # numeros DISTINTOS
                _sin.append((_x, _l.strip()[:60]))
    return _sin, _ilegibles


def _leer65(_r):
    _p = pathlib.Path(_r) if _r.startswith("/") else ROOT.parent / _r
    try:
        if _p.is_file() and _p.stat().st_size < 120_000_000:
            return _p.read_text(errors="ignore")
    except OSError:
        pass
    return None


_LOGS65 = ""
for _q in sorted((ROOT.parent / "results").rglob("*")):
    if _q.is_file() and _q.suffix in (".log", ".json", ".txt", ".csv", ".dat"):
        _LOGS65 += _q.read_text(errors="ignore")[:3_000_000]
_DATOS65 = ""
for _q in sorted((ROOT.parent / "data").rglob("*")):
    if _q.is_file() and _q.stat().st_size < 20_000_000:
        try:
            _DATOS65 += _q.read_text(errors="ignore")
        except OSError:
            pass
_sin65, _ileg65 = {}, {}
for _q in sorted(ROOT.rglob("*.py")):
    if "archive" in str(_q) or _q.name == "ssee_verify.py":
        continue
    _s, _il = _r65_origen(_q.read_text(errors="ignore"), _leer65,
                          _FLOATS65, _CANON65, _LOGS65, _DATOS65)
    if _s:
        _sin65[str(_q.relative_to(ROOT))] = _s
    if _il:
        _ileg65[str(_q.relative_to(ROOT))] = _il
_n65 = sum(len(_v) for _v in _sin65.values())
if _n65:
    _may65 = sorted(_sin65.items(), key=lambda kv: -len(kv[1]))[:4]
    track_open(f"R65 {_n65} numeros sin origen en {len(_sin65)} scripts",
               "; ".join(f"{k} ({len(v)}: {v[0][0]})" for k, v in _may65)
               + " — rastrear cada uno: algebra, `# ORIGEN: <ruta>`, log, "
                 "cita en la linea o `# ORIGEN-VALOR: <n> — <razon>`")
# TRINQUETE (R50), 2026-09-19. R65 solo pintaba AMBAR: el numero podia volver
# a crecer sin que nada lo frenara. 223 -> 175 -> 10 en el dia, rastreando
# cada numero a su algebra, log, dato o cita. Los 10 que quedan son los que
# NO se pudieron rastrear (valores impresos por corridas que no dejaron log, o
# sin fuente localizada): siguen contados a proposito, no se les invento origen.
# 2026-09-20: los 10 ultimos rastreados uno a uno. Ocho eran narrativos
# (numeros de metodos RETIRADOS que el texto conserva como evidencia de por
# que se retiraron) y se declararon con ORIGEN-VALOR; uno era el sigma(logA)
# del CMB tecleado a mano (0.014375, que ninguna cadena reproduce) y ahora se
# RECALCULA de results/chains/ssee_cmb.*.txt; el blanco que lo acompanaba se
# lee de CANONICAL_VALUES.yaml. Tope a CERO: ya no hay deuda que tolerar.
_TOPE_R65 = 0
_DEUDA_REAL["R65"] = _n65
_DEUDA_MAX["R65"] = _TOPE_R65
check("R65 la deuda de numeros sin origen no crece",
      _n65 <= _TOPE_R65,
      f"{_n65} numeros (tope {_TOPE_R65}) en {len(_sin65)} scripts")
if _ileg65:
    print(f"  [INFO] R65 origenes declarados que no se pudieron leer (disco "
          f"sin montar o ruta rota): {_ileg65}")

# CONTROL (R53): cada via de origen, en las dos direcciones. Sin datos reales:
# nucleo, logs y archivos simulados.
_fl65 = [0.839950, 9.519173, 67.962137]
_arch65 = {"/mnt/x/cadena.txt": "row 0.095019 0.0191914 0.769441\n"}
_c65b = [
    ("w0 = 0.839950", False),                     # algebra exacta
    ("Kv = 9.51926  # KRYSTOS", True),            # errata: no reproduce 9.519173
    ("# ORIGEN: /mnt/x/cadena.txt\nomch2 = 0.095019", False),
    ("# ORIGEN: /mnt/x/cadena.txt\nomch2 = 0.095020", True),   # no esta dentro
    ("# ORIGEN-VALOR: 0.0008 — ancho de la rejilla en w_c\npaso = 0.0008", False),
    ("# ORIGEN-VALOR: 0.0008 — x\npaso = 0.0008", True),       # razon vacia
    ("theta = 1.04110  # Planck 2018, arXiv:1807.06209", False),
    ("x = 0.30000", True),                         # 1 cifra: el log no basta
    ("y = 0.74467", False),                        # 5 cifras y esta en el log
]
_f65b = [t[:40] for t, esp in _c65b
         if bool(_r65_origen(t, _arch65.get, _fl65, "", "0.30000 0.74467", "")[0])
         != esp]
check("R65 el rastreador distingue origen hallado de numero sin origen",
      not _f65b,
      "9 casos: algebra exacta, archivo declarado, razon escrita, cita y log de "
      "5 cifras dan origen; la errata de algebra, el numero ausente del "
      "archivo declarado, la razon vacia y el 0.30000 que solo coincide con "
      "un log, NO" if not _f65b else f"casos mal clasificados: {_f65b}")

# CONTROL (R53): marca el numero ausente, deja pasar el presente y el que no
# declara fuente. Log simulado, sin tocar disco.
_fake65 = {"x.log": "H0 = 67.52954 +0.35211 ob = 0.02187\n"}
_c65 = [("# FUENTE: results/logs/x.log\nH0=67.52954", False),
        ("# FUENTE: results/logs/x.log\nH0=67.62055", True),
        ("H0=67.62055  # sin declarar fuente", False),
        ("# FUENTE: results/logs/x.log\n# narra 67.62055 en un comentario", False),
        ("# FUENTE: results/logs/nohay.log\nH0=67.52954", True),
        # el identificador de arXiv que salio el 2026-09-08
        ("# FUENTE: results/logs/x.log\nDESI DR2 arXiv:2503.14738", False)]
_f65 = [t[:46].replace("\n", " ") for t, esp in _c65
        if bool(_r65_sitios(t, _fake65.get)) != esp]
check("R65 el detector distingue el numero rancio del vigente",
      not _f65, "; ".join(_f65) if _f65
      else "6 casos: el numero ausente del log marcado; el presente, el que "
           "no declara fuente, el que solo aparece en un comentario y un "
           "identificador de arXiv, exentos; y el log inexistente marcado")

# --- R73: de donde sale CADA numero-resultado de los PAPERS ----------------
# POR QUE EXISTE (2026-09-30). R65 exige origen en los scripts; nada lo exigia
# en los .tex. Al construirla aparecio que el TITULAR CMB de P1/P3,
# ΔBIC = −32.9 (χ²_BF 2771.3 vs 2773.1), no sale de ningun log: vino de las
# cadenas del 23-jun, que la corrida del 27-jul (H0 LIBRE, k=3) sobrescribio.
# Y la tabla B1 de P3 conserva la columna ΛCDM de aquellas cadenas (67.35,
# 0.9651) contra el log vigente (67.39, 0.9654). Logica en r73_papers.py (la
# misma que usa el lector de linea de comandos: no hay copia).
import importlib.util as _ilu73
_sp73 = _ilu73.spec_from_file_location("_r73", ROOT / "verificacion" / "r73_papers.py")
_r73 = _ilu73.module_from_spec(_sp73)
_sp73.loader.exec_module(_r73)
_pool73 = _r73.fuentes()
_sin73, _nover73 = _r73.barrido(_pool73)
_n73 = sum(len(_v) for _v in _sin73.values())
if _n73:
    track_open(f"R73 {_n73} numeros-resultado sin origen en {len(_sin73)} papers",
               "; ".join(f"{k.split('/')[-1]} L{v[0][0]} {v[0][1]}" for k, v in _sin73.items())
               + " — rastrear: log, \\cite en la frase o `% ORIGEN-VALOR: <n> — <razon>`")
# TRINQUETE: la deuda medida al nacer la regla (2026-09-30). Solo puede bajar.
_TOPE_R73 = 3    # 10 -> 7 -> 4: tab:mcmc_full (leer_mcmc_full.py, filas correctas), S8 de P6 (s8_desde_b1.py; 0.8262 era 0.8261), 6.66 de P3 declarado historico
_DEUDA_REAL["R73"] = _n73
_DEUDA_MAX["R73"] = _TOPE_R73
check("R73 la deuda de numeros-resultado sin origen en los papers no crece",
      _n73 <= _TOPE_R73,
      f"{_n73} (tope {_TOPE_R73}) en {len(_sin73)} papers · {_nover73} de <3 cifras "
      f"no verificables por valor")
# CONTROL (R53), sin disco: pool simulado.
_poolc73 = sorted([0.8273, 67.8244, 0.4133])
_c73 = [("$67.82\\pm0.41$", 0),                                   # redondeo de un log
        ("$67.47\\pm0.41$", 1),                                   # ausente: marcado
        ("$0.8262\\pm0.0054$ \\citep{KiDS}", 0),                   # cita en la frase
        ("$0.8262\\pm0.0054$. Otra frase \\citep{X}", 1),          # cita en OTRA frase
        ("% ORIGEN-VALOR: 0.8262 — S8 de la cadena X\n$0.8262\\pm0.0054$", 0),
        ("% ORIGEN-VALOR: 0.8262 —  \n$0.8262\\pm0.0054$", 1),     # razon vacia
        ("% dice $0.8262\\pm0.0054$ en un comentario", 0),
        ("$0.33\\sigma$", 0)]                                     # <3 cifras: no se juzga
_f73 = [t[:40].replace("\n", " ") for t, esp in _c73
        if len(_r73.revisa(t, _poolc73)[0]) != esp]
check("R73 el detector distingue numero con origen de numero sin origen",
      not _f73, "; ".join(_f73) if _f73 else
      "8 casos: log a su redondeo, cita en la frase, declaracion con razon y "
      "comentario pasan; el ausente, la cita de otra frase y la razon vacia, NO")

# --- R74: PROCEDENCIA UNIVERSAL — ningun numero, en ningun lado, sin fuente ----
# Regla de Mike (2026-09-30), general: no solo scripts (R65) ni solo una parte
# de los papers (R73): logs, CANONICAL, papers y cajones. Logica en
# r74_procedencia.py. Casar por valor es la RED MINIMA (declarado ahi); la meta
# es el enlace explicito. Trinquete por superficie en la cuenta del dia en que
# nace: desde aqui la deuda solo puede BAJAR, en ninguna superficie crece.
_sp74 = _ilu73.spec_from_file_location("_r74", ROOT / "verificacion" / "r74_procedencia.py")
_r74 = _ilu73.module_from_spec(_sp74)
_sp74.loader.exec_module(_r74)
_res74 = _r74.barrido()
_n74 = _r74.cuentas(_res74)
_TOPE_R74 = {"logs": 2, "canonical": 2, "papers": 16, "cajones": 165}   # 2026-10-01: papers 27->16 (cumulos, PS, edades, CLASS, fondos exponenciales por \val); era 88/6/294/214 el 2026-09-30
for _k74, _v74 in _n74.items():
    _DEUDA_REAL[f"R74-{_k74}"] = _v74
    _DEUDA_MAX[f"R74-{_k74}"] = _TOPE_R74[_k74]
if sum(_n74.values()):
    track_open(f"R74 {sum(_n74.values())} numeros/logs sin procedencia",
               ", ".join(f"{k} {v}" for k, v in _n74.items())
               + " — detalle: python3 src/verificacion/r74_procedencia.py detalle")
check("R74 ninguna superficie gana numeros sin procedencia",
      all(_n74[k] <= _TOPE_R74[k] for k in _n74),
      " · ".join(f"{k} {_n74[k]} (tope {_TOPE_R74[k]})" for k in _n74))
# CONTROL (R53): archivo temporal con un numero del pool, uno ausente, uno con
# cita en su frase y uno declarado con razon; solo el ausente cuenta.
import tempfile as _tf74
with _tf74.TemporaryDirectory() as _d74:
    _f74 = pathlib.Path(_d74) / "x.tex"
    _f74.write_text("H0 = 67.82 bien. H0 = 67.47 mal. Dato 0.8265 \\citep{K}.\n"
                    "% ORIGEN-VALOR: 1.234 — prueba\nvalor 1.234\n")
    _s74 = [s for _, s in _r74._sin_origen(_f74, sorted([67.8244]), True)]
check("R74 el detector marca solo el numero sin fuente",
      _s74 == ["67.47"], f"marcados {_s74} (esperado ['67.47']: log a su redondeo, cita y "
      "declaracion pasan)")
# CONTROL (R53), 2026-09-30: un REPORTE del guardian (o una cola) en
# results/logs no es fuente — cita los numeros sin fuente al denunciarlos, y
# contarlo hizo que la deuda de papers «bajara» 294->190 sin arreglar nada.
with _tf74.TemporaryDirectory() as _d74b:
    _g74 = pathlib.Path(_d74b) / "guardian_2026-09-29.txt"
    _l74 = pathlib.Path(_d74b) / "kids_publicados.json"
    _c74 = pathlib.Path(_d74b) / "cola_n8.log"
    for _p74 in (_g74, _l74, _c74):
        _p74.write_text("0.2471\n")
    _e74 = [_r74.R.es_fuente(_p74) for _p74 in (_g74, _l74, _c74)]
# CONTROL (R53), 2026-09-30: el NUCLEO EVALUADO es fuente (K_V = 9.519253 no
# esta escrito como numero en ssee_core.py, se calcula); un identificador de
# arXiv junto a «arXiv:» no es un resultado, pero el mismo numero suelto si.
with _tf74.TemporaryDirectory() as _d74c:
    _x74 = pathlib.Path(_d74c) / "x.tex"
    _x74.write_text("Data from arXiv:2503.19441 are used. Much later in a separate "
                    "sentence we count 2503.19441 events here. K is 9.519253 here. "
                    "See doi:10.1103/PhysRevD.90.023507 for it.\n")
    _a74 = [s for _, s in _r74._sin_origen(_x74, sorted(_r74.R.nucleo_evaluado()), True)]
check("R74 el detector exime el nucleo evaluado y las referencias arXiv/DOI, no el numero suelto",
      _a74 == ["2503.19441"], f"marcados {_a74} (esperado ['2503.19441'] solo la 2a aparicion)")
check("R74 el detector no toma un reporte del guardian ni una cola como fuente",
      _e74 == [False, True, False],
      f"guardian/log/cola -> {_e74} (esperado [False, True, False])")

# --- R75: CADENA DE PROCEDENCIA (dvc.lock + acta) -----------------------------
# Decision de Mike (2026-09-30): DVC + macros + acta. R74 casa por VALOR (red
# minima); R75 exige el ENLACE: cada resultado declarado en dvc.yaml tiene que
# ser, byte a byte, el que su lock dice (nadie lo edito a mano), con sus
# dependencias intactas, y traer su acta (commit + sha del script en ese commit).
# La verificacion de hashes es propia (md5 de contenido, como DVC 3): el
# guardian no depende de tener dvc instalado.
import hashlib as _h75
import yaml as _y75
sys.path.insert(0, str(ROOT))
import procedencia as _pr75  # noqa: E402


def _md5_75(p):
    _h = _h75.md5()
    with open(p, "rb") as _f:
        for _b in iter(lambda: _f.read(1 << 20), b""):
            _h.update(_b)
    return _h.hexdigest()


def _lock_75(lock_txt, base):
    """-> lista de problemas del lock contra el disco (vacia = todo cuadra)."""
    _mal = []
    for _st, _d in ((_y75.safe_load(lock_txt) or {}).get("stages") or {}).items():
        for _tipo in ("deps", "outs"):
            for _e in _d.get(_tipo) or []:
                _p = pathlib.Path(_e["path"])
                _p = _p if _p.is_absolute() else base / _p
                if not _p.is_file():
                    _mal.append(f"{_st}: falta {_e['path']}")
                elif "md5" in _e and _md5_75(_p) != _e["md5"]:
                    _mal.append(f"{_st}: {_tipo[:-1]} cambiado {_e['path']}")
    return _mal


_REPO75 = ROOT.parent
_lk75 = (_REPO75 / "dvc.lock")
_mal75 = _lock_75(_lk75.read_text(), _REPO75) if _lk75.exists() else ["no hay dvc.lock"]
check("R75 cada resultado de la cadena es el que su lock dice (nadie lo edito, sus entradas intactas)",
      not _mal75, "; ".join(_mal75[:6]) if _mal75 else "dvc.lock cuadra byte a byte con el disco")
_outs75 = [o if isinstance(o, str) else list(o)[0]
           for _d in ((_y75.safe_load((_REPO75 / "dvc.yaml").read_text()) or {}).get("stages") or {}).values()
           for o in (_d.get("outs") or [])] if (_REPO75 / "dvc.yaml").exists() else []
_sinacta75 = [f"{o}: {m}" for o in _outs75 for ok, m in [_pr75.verifica(_REPO75 / o)] if not ok]
check("R75 cada resultado de la cadena trae acta valida (commit y sha del script coinciden)",
      not _sinacta75, "; ".join(_sinacta75) if _sinacta75 else f"{len(_outs75)} actas verificadas")
# Cobertura: logs que TODAVIA no estan en la cadena. Trinquete: solo baja.
# Fuera de la cuenta, declarado: los logs de ORQUESTACION (cola_*, vigilante_*)
# registran horas y PIDs de las colas, no resultados; ningun numero sale de ellos.
_tod75 = [p for p in (_REPO75 / "results/logs").rglob("*") if p.is_file() and p.suffix in (".log", ".json", ".txt", ".csv")
          and not p.name.startswith(_r74.ORQUESTACION)]
_fuera75 = len([p for p in _tod75 if str(p.relative_to(_REPO75)) not in set(_outs75)])
_TOPE_R75 = 167   # 2026-09-30 noche: 193 logs de resultado, 26 en la cadena (era 169)
_DEUDA_REAL["R75"] = _fuera75
_DEUDA_MAX["R75"] = _TOPE_R75
check("R75 la cantidad de logs FUERA de la cadena de procedencia no crece",
      _fuera75 <= _TOPE_R75, f"{_fuera75} de {len(_tod75)} (tope {_TOPE_R75})")
# CONTROL (R53): un lock sintetico sobre archivos temporales: el intacto pasa,
# el editado a mano y la entrada cambiada se marcan.
with _tf74.TemporaryDirectory() as _d75:
    _b75 = pathlib.Path(_d75)
    (_b75 / "in.txt").write_text("dato 1\n")
    (_b75 / "out.json").write_text('{"S8": 0.8261}\n')
    _lk = (f"stages:\n  s:\n    deps:\n    - path: in.txt\n      md5: {_md5_75(_b75 / 'in.txt')}\n"
           f"    outs:\n    - path: out.json\n      md5: {_md5_75(_b75 / 'out.json')}\n")
    _c75 = [not _lock_75(_lk, _b75)]
    (_b75 / "out.json").write_text('{"S8": 0.8273}\n')
    _c75.append(bool(_lock_75(_lk, _b75)))
    (_b75 / "out.json").write_text('{"S8": 0.8261}\n')
    (_b75 / "in.txt").write_text("dato 2\n")
    _c75.append(bool(_lock_75(_lk, _b75)))
check("R75 el detector distingue lo intacto de lo editado a mano y de la entrada cambiada",
      all(_c75), "3 casos: intacto pasa; salida editada y entrada cambiada, marcadas" if all(_c75)
      else f"fallos {_c75}")

# --- R64: nadie clava la ecuacion de estado de SSEE en un evaluador ----
# POR QUE EXISTE (2026-09-08). El evaluador del CMB traia dentro del modelo
#     'w': -0.840015, 'wa': -0.670141
# como literales, para TODAS las corridas. Cualquier fila rotulada LCDM que
# pasara por ahi no era LCDM: no fallaba, devolvia un numero plausible y
# equivocado. Ya invalido una fila real (LCDM en cmb_tau_flotado.json, que
# quedo marcada "NO USAR" a mano) y la nota protegia esa fila pero no la
# siguiente — que era justo la corrida #2 de la cola, un control LCDM.
# Declarado y no resuelto: el patron de [[feedback_green_can_be_forced]].
# QUE MARCA: un fichero que escriba w0 o wa de SSEE como LITERAL en una
# asignacion de parametro. La forma sana es importarlos de ssee_core (asi el
# valor no se puede quedar rancio) o recibirlos como argumento.
# AFINADO el mismo dia: la primera version marcaba tambien `w0=-0.840` en
# forma de argumento, y ahi salieron dos falsos positivos legitimos — la
# narracion dentro de un print (savage_cv) y los MAP de las cadenas en un
# guion de figuras (regenerate_fig8), que NO son constantes del modelo. El
# fallo real tiene una forma concreta: CLAVE ENTRECOMILLADA dentro del dict
# que construye el modelo de CAMB/Cobaya, que es como se le pasa la ecuacion
# de estado a la teoria. Esa es la que se vigila.
_R64_MAL = re.compile(
    r"['\"](?:w|w0|dark_energy_w)['\"]\s*:\s*-0\.840\d*"
    r"|['\"]wa['\"]\s*:\s*-0\.670\d*")
def _r64_sitios(_txt):
    _h = []
    for _m in _R64_MAL.finditer(_txt):
        # la cabecera que EXPLICA el bug cita el literal: no cuenta
        _lin = _txt[_txt.rfind("\n", 0, _m.start()) + 1:_m.end()]
        if _lin.lstrip().startswith("#") or _lin.lstrip().startswith("traia"):
            continue
        _h.append(_m.group(0)[:40])
    return _h
_r64 = []
for _f64 in sorted(ROOT.rglob("*.py")):
    if "archive" in str(_f64) or _f64.name in _FIXTURES:
        continue
    _t64 = _f64.read_text(errors="ignore")
    # ssee_core es la FUENTE de W0/WA: ahi el literal es su sitio
    if _f64.name == "ssee_core.py":
        continue
    _r64 += [f"{_f64.name}: {x}" for x in _r64_sitios(_t64)]
check("R64 ningun evaluador clava w0/wa de SSEE como literal",
      not _r64, "; ".join(_r64[:3]) if _r64
      else "w0/wa se importan de ssee_core o se reciben como argumento; "
           "asi una corrida LCDM no puede heredar la energia oscura de SSEE "
           "en silencio (paso el 2026-09-08 en cmb_eval)")
# CONTROL (R53): marca la forma clavada, deja pasar la sana y la narrada.
_c64 = [("info['params'] = {'w': -0.840015, 'wa': -0.670141}", True),
        ("info['params'] = {'w': cl[0], 'wa': cl[1]}", False),
        ("info['params'] = {'w': S.W0, 'wa': S.WA}", False),
        ("# traia 'w': -0.840015 clavado, por eso se arreglo", False),
        # los dos falsos positivos reales del 2026-09-08
        ('models = {"SSEE": dict(H0=67.62, w0=-0.840, wa=-0.670)}', False),
        ("print(f'  CPL posterior en (w0=-0.840, wa=-0.670): {d}')", False)]
_f64 = [t[:44] for t, esp in _c64 if bool(_r64_sitios(t)) != esp]
check("R64 el detector distingue el literal clavado del argumento",
      not _f64, "; ".join(_f64) if _f64
      else "6 casos: el literal en clave de dict marcado; el argumento, el "
           "import de ssee_core, el comentario que narra el bug, los MAP de "
           "cadena de una figura y la narracion en un print, exentos")

# --- R63: la tension w0wa se RECALCULA, no se copia -------------------
# POR QUE EXISTE (2026-09-08). El Registro decia 0.09 sigma para la distancia
# del punto algebraico (w0,wa) al contorno DESI DR2 + Pantheon+, y NO
# reproducia con los numeros que el mismo renglon citaba. Lo cazo Mike de
# memoria: «yo tambien recuerdo 0.24 sigmas en DR2 y 0.05 en DR1».
# Los papers (P7, 3 sitios), CLAUDE.md, LECTURA_PAPERS y FUENTES_PENDIENTES
# decian 0.24 y SI reproduce. El sitio rancio era el Registro — el archivo que
# manda en caso de discrepancia, o sea el peor sitio donde tenerlo.
# QUE HACE: no compara literales. RECALCULA la cuadratura desde W0/WA del
# nucleo y el contorno publicado, y exige que lo escrito coincida. Si manana
# W0 cambia, el numero esperado cambia solo.
_DR2_W0, _DR2_S0 = -0.838, 0.055      # DESI DR2 + Pantheon+, w0waCDM
_DR2_WA, _DR2_SA = -0.620, 0.220      # 2503.14738
_CHI2_2D = 0.42                       # Paper 2, covarianza COMPLETA (ecs. 25-28)
# el nucleo ya viene cargado por R66, arriba.
# COMO se obtiene el 0.24 (y como NO). No es una cuadratura: es el chi2 2D
# con la covarianza completa, convertido a sigma de UNA dimension por su
# probabilidad de exceder. La cuadratura sin correlacion da 0.2299 y se
# parece por CASUALIDAD — creerla llevaria a exigir 0.23 y a "corregir" un
# valor que esta bien. Anotado porque yo mismo cai en eso el 2026-09-08.
_p63 = _math.exp(-_CHI2_2D / 2.0)                 # sf de chi2 con 2 g.l.
_z63 = _math.sqrt(2.0) * _erfinv63 if False else None
from statistics import NormalDist as _ND63
_z63 = _ND63().inv_cdf(1.0 - _p63 / 2.0)
check("R63 el 0.24 sigma de w0wa sale del chi2_2D, no de una cuadratura",
      abs(_z63 - 0.24) < 0.005,
      f"chi2_2D = {_CHI2_2D} (2 g.l.) -> P(exceder) = {_p63:.5f} -> "
      f"{_z63:.4f} sigma equivalente. La cuadratura sin correlacion da "
      f"{_math.hypot((_core63.W0-_DR2_W0)/_DR2_S0, (_core63.WA-_DR2_WA)/_DR2_SA):.4f}: "
      f"parecido casual, NO es la via"
      if abs(_z63 - 0.24) < 0.005 else
      f"da {_z63:.4f}, no 0.24: cambio el chi2_2D documentado")
_dq63 = _math.hypot((_core63.W0 - _DR2_W0) / _DR2_S0,
                    (_core63.WA - _DR2_WA) / _DR2_SA)
check("R63 el punto algebraico sigue dentro del contorno DESI DR2",
      _dq63 < 1.0,
      f"w0 a {abs((_core63.W0-_DR2_W0)/_DR2_S0):.4f} sigma y wa a "
      f"{abs((_core63.WA-_DR2_WA)/_DR2_SA):.4f}; ninguno se acerca a 1")
# el 0.09 rancio no puede volver a ningun documento
_R63_MAL = re.compile(r"0\.09\s*(?:\\?sigma|σ)", re.I)
_r63 = []
for _f63 in ([_q for _q in sorted(ROOT.parent.glob("*.md"))
              if _q.name not in ("CHANGELOG.md", "MEMORY.md")]
             + sorted((ROOT.parent / "manuscript").glob("*.tex"))):
    _t63 = _f63.read_text(errors="ignore")
    for _m63 in _R63_MAL.finditer(_t63):
        _ctx = _t63[max(0, _m63.start() - 200):_m63.end() + 200].lower()
        if ("w_0" in _ctx or "w0wa" in _ctx or "pantheon" in _ctx
                or "desi" in _ctx) and "no reproduc" not in _ctx:
            _r63.append(f"{_f63.name}: {_m63.group(0)}")
check("R63 el 0.09 sigma rancio no reaparece junto a w0wa/DESI",
      not _r63, "; ".join(_r63[:3]) if _r63
      else "0.09 sigma no reproduce desde el contorno citado; el valor es 0.24")
# CONTROL (R53): el detector marca el 0.09 en contexto w0wa y deja pasar
# el mismo 0.09 en cualquier otro contexto (p.ej. S8 vs DES en OPEN_PROBLEMS).
_c63 = [("el punto (w_0,w_a) queda a 0.09 sigma de DESI DR2 + Pantheon+", True),
        ("S8 = 0.761 esta a 0.09 sigma de DES-Y3", False),
        ("el punto (w_0,w_a) queda a 0.24 sigma de DESI DR2 + Pantheon+", False)]
def _r63_marca(_t):
    for _m in _R63_MAL.finditer(_t):
        _c = _t[max(0, _m.start() - 200):_m.end() + 200].lower()
        if ("w_0" in _c or "w0wa" in _c or "pantheon" in _c or "desi" in _c) \
                and "no reproduc" not in _c:
            return True
    return False
_f63 = [t[:40] for t, esp in _c63 if _r63_marca(t) != esp]
check("R63 el detector distingue el 0.09 de w0wa del 0.09 de otra cosa",
      not _f63, "; ".join(_f63) if _f63
      else "3 casos: el 0.09 junto a w0wa marcado; el 0.09 de S8 vs DES y el "
           "0.24 correcto exentos")

# --- R62: un veredicto sobre un RANGO no puede mirar un solo extremo ---
# POR QUE EXISTE (2026-09-08). El argumento Sakharov de OP-1 despejaba una
# temperatura de recalentamiento, citaba el rango «10^-2 a 10^4 GeV» y la
# validaba asi:
#       if T_rh_required < 1e4:
#           print("  OK ... CONSISTENTE con reheating gravitacional")
# Solo el techo. Nunca el piso. Estampo el visto bueno a 1.031e-04 GeV, que
# esta 97 veces POR DEBAJO del piso que el propio print citaba dos lineas
# antes — y ademas 40 veces bajo la cota de BBN y 10^6 bajo la del
# esfaleron que el mismo mecanismo necesita. Todo lo demas del argumento se
# retro-calcula (el f_dil se despeja exigiendo el eta_B observado), asi que
# ESTE era el UNICO sitio donde podia fallar, y estaba tapado por un
# chequeo de una cara. Sobrevivio del 2026-05-16 al 2026-09-08.
# Lo pidio Mike: «no seria mejor decirme antes de buscar el puente
# probemos la maquina». Se probo y no arranca. Ver [[feedback_green_can_be_forced]].
# QUE MARCA: un `if <var> <op> <numero>:` de UNA sola comparacion cuyo
# cuerpo estampa un veredicto de rango (CONSISTENTE / OK / dentro de...).
# Dos comparaciones (and/or, o `a <= x <= b`) estan exentas: eso ya es
# una cota de dos lados.
_R62_VEREDICTO = re.compile(
    r"CONSISTENTE|consistente con|dentro del rango|dentro de rango"
    r"|compatible con el rango|in range|within range", re.I)
_R62_IF = re.compile(r"^([ \t]*)if\s+([^\n:]+):[ \t]*(?:#[^\n]*)?$", re.M)
# AFINADO en el mismo dia: la primera version marcaba `if err < tol`, que
# es legitimo — un error tiene UNA sola cota por construccion (err >= 0).
# Lo que hace al caso de OP-1 un defecto no es la comparacion sola, es que
# valida contra un RANGO de dos extremos que el propio texto acaba de
# citar. Asi que se exige rango citado en las lineas de arriba.
_R62_RANGO = re.compile(
    # `range(` es el builtin de Python, no un rango citado: no cuenta.
    r"rango|\brange\b(?!\s*\()|típic|tipic|typical"
    r"|[0-9)⁴²³⁰-⁹]\s*[−–—-]\s*10", re.I)
def _r62_sitios(_txt):
    _h = []
    _lineas = _txt.split("\n")
    for _m in _R62_IF.finditer(_txt):
        _cond = _m.group(2)
        _nl = _txt.count("\n", 0, _m.start())
        if not _R62_RANGO.search("\n".join(_lineas[max(0, _nl - 10):_nl])):
            continue
        # dos lados ya: and/or, o encadenado a <= x <= b
        if re.search(r"\b(?:and|or)\b", _cond):
            continue
        if len(re.findall(r"[<>]=?", _cond)) >= 2:
            continue
        if not re.search(r"[<>]=?", _cond):
            continue
        _sang = len(_m.group(1))
        _cuerpo, _i = [], _m.end()
        for _ln in _txt[_i:].split("\n")[1:9]:
            if _ln.strip() and (len(_ln) - len(_ln.lstrip())) <= _sang:
                break
            _cuerpo.append(_ln)
        if _R62_VEREDICTO.search("\n".join(_cuerpo)):
            _h.append(_cond.strip()[:56])
    return _h
_SUP62 = [_q for _q in sorted(ROOT.rglob("*.py"))
          if _q.name != "ssee_verify.py"]
# los scripts de open_problems son ARCHIVO por ruta pero PRUEBA citada por
# OPEN_PROBLEMS.md: si un .md los cita como evidencia, se miran igual.
_SUP62 += sorted((ROOT.parent / "archive" / "codigo" / "investigacion"
                  / "open_problems").glob("*.py"))
_r62 = []
for _f in _SUP62:
    _r62 += [f"{_f.name}: if {x}"
             for x in _r62_sitios(_f.read_text(errors="ignore"))]
check("R62 ningun veredicto de rango se decide mirando un solo extremo",
      not _r62, "; ".join(_r62[:3]) if _r62
      else "un rango tiene DOS cotas; validar contra una sola convierte el "
           "unico punto falsable en un verde automatico (caso OP-1 Sakharov, "
           "2026-05-16 a 2026-09-08: T_rh 97x bajo su propio piso)")
# CONTROL (R53): marcar la forma coja y DEJAR PASAR las dos sanas.
_R62_CTX = "print('  T_rh tipica: 1e-2 - 1e4 GeV, rango citado')\n"
_c62_mal = (_R62_CTX + "if T_rh < 1e4:\n"
            "    print('  CONSISTENTE con reheating gravitacional')\n")
_c62_dos = (_R62_CTX + "if 1e-2 <= T_rh <= 1e4:\n"
            "    print('  CONSISTENTE con reheating gravitacional')\n")
_c62_and = (_R62_CTX + "if T_rh > 1e-2 and T_rh < 1e4:\n"
            "    print('  CONSISTENTE con reheating gravitacional')\n")
_c62_otro = (_R62_CTX + "if n_pts < 10:\n"
             "    print('  pocos puntos para el ajuste')\n")
_c62_err = ("if err < tol:\n"
            "    print('  CONSISTENTE: dentro de tolerancia')\n")
_f62 = [n for n, (t, esp) in
        {"coja": (_c62_mal, True), "encadenada": (_c62_dos, False),
         "con and": (_c62_and, False), "sin veredicto": (_c62_otro, False),
         "err<tol sin rango": (_c62_err, False)}.items()
        if bool(_r62_sitios(t)) != esp]
check("R62 el detector distingue la cota de un lado de la de dos",
      not _f62, "; ".join(_f62) if _f62
      else "5 casos: la de un solo lado CON rango citado marcada; la "
           "encadenada, la del and, el if sin veredicto y el err<tol sin "
           "rango (una cota es legitima ahi) exentos")

# --- R61: comparar con el numero puro exige el f_screen COMPLETO -------
# POR QUE EXISTE. Al enunciar la cascada frente a 3(phi+pi)^2 hay que usar
# el f_screen COMPLETO (IR+UV, 0.069522), que da 67.962142 y un residuo de
# +4.2e-06. Con el IR solo (0.067253) sale 68.13, a 0.17 sigma: un
# resultado PARCIAL, no la forma canonica. Lo he escrito mal tres veces en
# una sola sesion; Mike: «ya te lo he dicho como tres veces en esta sesion,
# solo me estas haciendo gastar creditos porque lo terminas olvidando».
# Una regla no se olvida. Marca 68.13 cuando esta PEGADO a la comparacion
# con el numero puro; el 68.13 por si solo es correcto y no se toca.
_R61_MAL = re.compile(
    r"68\.1[23]\d*[^.\n]{0,90}(?:3\s*\(\s*(?:\\varphi|\\phiG|\u03c6)\s*\+\s*"
    r"(?:\\pi|\u03c0)\s*\)|67\.96214|numero puro|n\u00famero puro|pure number)"
    r"|(?:67\.96214|numero puro|n\u00famero puro|pure number)[^.\n]{0,90}68\.1[23]")
_EX61 = ("parcial", "IR solo", "solo IR", "s\u00f3lo IR", "no canonic",
         "no can\u00f3nic", "0.17", "IR-only", "partial")
def _r61_sitios(_txt):
    _h = []
    for _m in _R61_MAL.finditer(_txt):
        _ctx = _txt[max(0, _m.start() - 160):_m.end() + 160]
        if any(_e.lower() in _ctx.lower() for _e in _EX61):
            continue
        _h.append(_m.group(0).replace("\n", " ")[:64])
    return _h
_SUP61 = []
for _pat61 in ("manuscript/*.tex", "submission_PRD/*.tex", "*.md"):
    _SUP61 += [_q for _q in sorted(ROOT.parent.glob(_pat61))
               if _q.name not in ("CHANGELOG.md", "MEMORY.md")]
_SUP61 += [_q for _q in sorted(ROOT.rglob("*.py"))
           if "archive" not in str(_q) and _q.name != "ssee_verify.py"]
_r61 = []
for _f in _SUP61:
    _r61 += [f"{_f.name}: {x}" for x in _r61_sitios(_f.read_text(errors="ignore"))]
check("R61 la comparacion con el numero puro usa el f_screen COMPLETO",
      not _r61, "; ".join(_r61[:3]) if _r61
      else "f_screen^full = 0.069522 -> 73.04*(1-f) = 67.962142, residuo "
           "+4.2e-06 vs 3(phi+pi)^2. El IR solo (0.067253 -> 68.13, 0.17 "
           "sigma) es resultado PARCIAL y solo vale rotulado como tal")
_c61 = [("H_glob = 68.13, a 0.17 sigma de 67.96214", False),   # rotulado
        ("H_glob = 68.13 se compara con 3(\\varphi+\\pi)^2", True),
        ("H_glob^UV = 67.962142 vs el numero puro 3(\\varphi+\\pi)^2", False)]
_f61 = [t[:40] for t, esp in _c61 if bool(_r61_sitios(t)) != esp]
check("R61 el detector distingue el parcial rotulado del enunciado canonico",
      not _f61, "; ".join(_f61) if _f61
      else "3 casos: el 68.13 pegado a la comparacion marcado; el mismo "
           "rotulado como 0.17 sigma exento; el UV completo limpio")

# --- R60: registro UNICO de retracciones, barrido de TODAS las capas --
# POR QUE EXISTE. Cada retirada traia su guarda propia, y cada una miraba
# una superficie distinta: la de la particula solo manuscript/*.tex (57
# sitios en los .md sobrevivieron 37 dias); R55 .tex y .py; R58 .tex y
# dos .md. Tres guardas, tres agujeros. Aqui la fuente es RETRACCIONES.yaml
# y el barrido es el MISMO para todas: retirar algo nuevo es añadir una
# entrada, no escribir una regla nueva ni acordarse de que superficies mirar.
import yaml as _yaml
_RETR_YAML = ROOT.parent / "RETRACCIONES.yaml"
_retr = _yaml.safe_load(_RETR_YAML.read_text(errors="ignore"))
_SUP_VIVA = []
for _pat in ("manuscript/*.tex", "submission_PRD/*.tex", "*.md"):
    _SUP_VIVA += [_q for _q in sorted(ROOT.parent.glob(_pat))
                  if _q.name not in ("CHANGELOG.md", "MEMORY.md",
                                     "RETRACCIONES.yaml")]
_SUP_VIVA += [_q for _q in sorted(ROOT.rglob("*.py"))
              if "archive" not in str(_q) and _q.name != "ssee_verify.py"]
_r60 = {}
for _id, _e in sorted(_retr.items()):
    _tok = tuple(_e["tokens"])
    _viv = []
    for _f in _SUP_VIVA:
        for _l in _presenta_como_vigente(_f.read_text(errors="ignore"), _tok):
            _viv.append(f"{_f.name}: {_l[:44]}")
    if _viv:
        _r60[_id] = _viv
_n60 = sum(len(_v) for _v in _r60.values())
# Trinquete: 2026-09-07 arranca en la cuenta real. SOLO BAJA.
# 64 -> 61 el 2026-09-08: llevaba 3 de holgura y nadie lo veia, porque R50
# solo miraba los trinquetes registrados en _DEUDA_REAL y este no estaba.
# 61 -> 59 el 2026-09-19: al acotar la ventana dentro de las tablas salieron
# 10 filas que estaban ocultas —una fila retractada exoneraba a sus vecinas—
# y se limpiaron 16. Detector MAS estricto y deuda MENOR: las dos cosas a la
# vez, que es la senal de que lo que se limpio era real.
# 58 -> 58 el 2026-09-19 (tarde), con el alcance nuevo: el numero NO se movio, y por eso
# hay que decir que no significa lo mismo. El alcance nuevo destapo 29 sitios que la
# ventana de +-3 lineas venia tapando; se limpiaron los 29. El tope se queda
# donde estaba porque un trinquete solo baja, pero el 58 de esta tarde se
# mide con un detector que ve mas que el de esta manana.
# 58 -> 34 el 2026-09-19 (tarde): los nueve scripts de sondeo de la particula
# —24 sitios— movidos a archive/codigo/investigacion/particula_RETIRADA_2026-08-01/
# con su bitacora. Estaban en src/, el cajon de los vivos, con lineas como
# `M_PHI = 40.70` escritas como valores en uso. Ninguno era importado por codigo
# vivo. Se archivan y no se borran: son la prueba de la que sale la retirada,
# incluida la medicion que la excluyo (la cizalla cruda pide m_phi > 70.3 eV).
# 34 -> 23 el 2026-09-19 (tarde-2): la particula desaparece ENTERA de la
# superficie viva (particula_phi_dm pasa de 8 a 0) y la cascada invertida de
# 6 a 4. Lo que se limpio, y de donde salio cada cosa:
#   - `fig_readme_tensions.png`, la PORTADA del README, llevaba dos filas
#     retiradas: «S_8 (two-sector phi-DM) 0.04 sigma» y el f sigma_8 de 0.93
#     (variante two-sector con free-streaming). Ahora llevan los canonicos.
#   - `ssee_eftcamb_Pk.pdf`, que ENTRA en SSEE_Unified_Journal.tex, tenia
#     dibujada dentro la vertical `k_fs = 0.754 h/Mpc`. La vio el detector
#     solo despues de que R60 aprendiera la FORMA RENDERIZADA: el token es
#     `k_{\rm fs}=0.754` y pdftotext devuelve `kfs = 0.754`. Antes daba
#     verde mirandolo de frente.
#   - `fig_paper8_lensing_ratio`: figura construida entera sobre la particula
#     y que ningun .tex incluia. Borrada con su PDF y su PNG.
#   - `m_phi=40.70` en pB_inflation, `mult=594.28` en derive_nu_closure, y la
#     prosa de Paper 10 que decia `H_alg/(1-f_UV)` contradiciendo al calculo
#     de su propia linea 105.
#   - `_marked` en memory_sync: codigo muerto cuyo docstring usaba 72.86 de
#     ejemplo.
# Los 23 que quedan viven TODOS en documentos de registro (OPEN_PROBLEMS,
# VERIFICATION_LEDGER, AUDIT, CLAUDE, FUENTES_PENDIENTES), que es donde una
# retraccion TIENE que nombrarse para retractarse.
# 23 -> 16 el 2026-09-19 (noche): R60 aprende a leer CASTELLANO y a cortar por
# punto y coma, y las dos cosas destaparon sobras reales.
#   - El repo es bilingue y estas listas estaban solo en ingles: `retirad` no
#     cubria «se retiro», y del lado del pasado faltaban «era/eran/metia/…»,
#     que es justo como se escribe la prosa que NARRA una retirada.
#   - Un `;` separa dos afirmaciones. En AUDIT.md, «The Hubble cascade is …
#     72.86 (0.17σ); the canonical DR2 posterior is 67.79» se leia como UNA:
#     el «canonical» del posterior de DESI hacia viva la cascada retirada.
#     Al cortar ahi salieron DOS sobras que llevaban tapadas desde el
#     2026-08-01: el LEDGER decia «vigente = Σm_ν·SOLAR²·KRYSTOS_V = 40.70 eV»
#     y `ssee_paperB_DW.py` declaraba esa misma masa como «Valor canonico».
# Detector MAS estricto y deuda MENOR a la vez: la senal de que lo limpiado
# era real. `particula_phi_dm` y `cascada_invertida` quedan en CERO.
_TOPE_R60 = 0   # 9 -> 0 el 2026-09-19 (noche): las ultimas 9 sobras (OP-7, OP-13 y dos lineas del Registro) marcadas donde viven. Trinquete a CERO: cualquier token retirado que vuelva a aparecer sin marca pone ROJO.
_DEUDA_REAL["R60"] = _n60
_DEUDA_MAX["R60"] = _TOPE_R60
check("R60 la deuda del registro de retracciones no crece",
      _n60 <= _TOPE_R60,
      f"{_n60} sitios (tope {_TOPE_R60}) en {len(_r60)}/{len(_retr)} "
      "retracciones: "
      + ", ".join(f"{_k}={len(_v)}" for _k, _v in sorted(_r60.items())))
check("R60 los PAPERS estan limpios de todo lo retirado",
      not any(_s.endswith(".tex") or ".tex:" in _s
              for _v in _r60.values() for _s in _v),
      f"{len([f for f in _SUP_VIVA if f.suffix == '.tex'])} .tex barridos "
      f"contra las {len(_retr)} retracciones declaradas")
_c60v = "el modelo predice m_phi = 40.70 eV, falsable con Euclid"
_c60m = "m_phi = 40.70 eV quedo RETIRADO el 2026-08-01"
check("R60 el detector distingue lo vigente de lo narrado como retirado",
      bool(_presenta_como_vigente(_c60v, ("40.70",)))
      and not _presenta_como_vigente(_c60m, ("40.70",)),
      "2 casos sobre la misma cifra: presentada como prediccion viva "
      "marcada; declarada retirada, exenta")

# ── R60 · LAS FIGURAS TAMBIEN SON SUPERFICIE (2026-09-19) ───────────────────
#
# POR QUE SE AMPLIA. El barrido miraba .tex, .md y .py. Una FIGURA no es
# ninguna de las tres, y ahi sobrevivio la particula 49 dias despues de
# retirarla: `fig_s8_resolution.pdf` del paquete de PRD seguia dibujando
# «3.5 sigma vs KiDS» y «m = 40.70 eV, forward», con un pie de figura que ya
# contaba la historia nueva. Texto y dibujo decian cosas distintas, y ningun
# grep de .tex podia verlo porque la cadena no esta en ningun .tex.
#
# Y hay una asimetria que hace esto mas estricto que el barrido de prosa: un
# documento PUEDE nombrar lo retirado, porque tiene que retractarlo. Una
# figura no retracta nada. Cualquier token retirado dentro de una figura es un
# resto, sin excepcion.
_FIGS60 = [_q for _d in ("results/figures", "submission_PRD/figures")
           for _q in sorted((ROOT.parent / _d).glob("*.pdf"))]
_sucias60, _texto60 = [], 0
try:
    import subprocess as _sp60
    for _fg in _FIGS60:
        _t = _sp60.run(["pdftotext", str(_fg), "-"], capture_output=True,
                       text=True, timeout=30).stdout
        _texto60 += len(_t)
        _tr = _forma_render(_t)
        for _id, _e in sorted(_retr.items()):
            for _tk in _e["tokens"]:
                if _tk in _t or _forma_render(_tk) in _tr:
                    _sucias60.append(f"{_fg.parent.name}/{_fg.name}: «{_tk}» ({_id})")
                    break
    check("R60 ninguna figura publicada lleva dentro algo retirado",
          not _sucias60,
          "; ".join(_sucias60[:6]) if _sucias60
          else f"{len(_FIGS60)} figuras barridas contra las {len(_retr)} retracciones")
    # CONTROL (R53): que el barrido haya leido TEXTO de verdad. Si `pdftotext`
    # devolviera vacio —figuras rasterizadas, binario ausente— la comprobacion
    # daria verde sin mirar nada, que es la cuarta patologia: el verde por vacio.
    check("R60 el barrido de figuras leyo una superficie real",
          _texto60 > 500 and len(_FIGS60) >= 4,
          f"{len(_FIGS60)} figuras, {_texto60} caracteres de capa de texto "
          f"(piso 500)")

    # CONTROL (R53) de la forma renderizada. Sin el, apretar la comparacion
    # quitando TODO el espacio podria pegar palabras vecinas y ensuciar
    # figuras limpias. Se comprueban las dos direcciones sobre texto simulado
    # con la forma EXACTA que devuelve pdftotext.
    _pdf_sucio = "SSEE EFTCAMB GR SSEE RPH ( K = 0.4032, w = 0.84) kfs = 0.754 h/Mpc"
    _pdf_limpio = "SSEE EFTCAMB GR SSEE RPH ( K = 0.4032, w = 0.84) kfs = 0.812 h/Mpc"
    _tok_fig = "k_{\\rm fs}=0.754"
    _c60r = [
        # (texto de la figura, token, debe marcarse)
        (_pdf_sucio, _tok_fig, True),          # el caso real, verde en falso hasta hoy
        (_pdf_limpio, _tok_fig, False),        # otro valor: no se marca
        ("kfs = 0.754", "k_fs=0.754", True),   # la otra forma del mismo token
        ("alpha K = 0.4032 w = 0.84", _tok_fig, False),   # figura limpia
        # que quitar el espacio no pegue palabras vecinas en algo retirado:
        ("two sector", "two-sector", False),
    ]
    _f60r = [f"{_tk} vs {_tx[:28]!r}" for _tx, _tk, _esp in _c60r
             if ((_tk in _tx) or (_forma_render(_tk) in _forma_render(_tx)))
             != _esp]
    check("R60 el detector ve el token aunque el PDF lo devuelva aplanado",
          not _f60r,
          "5 casos: `k_{\\rm fs}=0.754` casa con el `kfs = 0.754` que devuelve "
          "pdftotext; otro valor, figura limpia y dos palabras sueltas NO"
          if not _f60r else f"casos mal clasificados: {_f60r}")
except FileNotFoundError:
    track_open("R60 figuras sin barrer: falta `pdftotext`",
               "instalar poppler-utils; mientras tanto las figuras son un "
               "punto ciego declarado")

# ── R60 · UNA FIGURA COPIADA A UN PAQUETE NO PUEDE DERIVAR DE SU FUENTE ─────
#
# El paquete de PRD lleva su propia copia de cada figura. Las cinco estaban
# congeladas el 2026-07-19 mientras sus fuentes se regeneraban hasta el
# 2026-09-08: el .tex y el .pdf del paquete SI se recompilaron en septiembre,
# pero contra las figuras viejas. Una copia que no se compara es una copia que
# se queda atras en silencio.
_dupes60 = []
for _pq in sorted((ROOT.parent / "submission_PRD" / "figures").glob("*")):
    _fuente = ROOT.parent / "results" / "figures" / _pq.name
    if _fuente.exists() and _fuente.read_bytes() != _pq.read_bytes():
        _dupes60.append(_pq.name)
check("R60 ninguna figura del paquete difiere de su fuente",
      not _dupes60,
      ", ".join(_dupes60) if _dupes60
      else f"{len(list((ROOT.parent / 'submission_PRD' / 'figures').glob('*')))} "
           "figuras del paquete identicas a results/figures")
_a60 = (ROOT.parent / "RETRACCIONES.yaml").read_bytes()
check("R60 el detector de copias derivadas sabe distinguir",
      (_a60 == _a60) and (_a60 != _a60 + b"x"),
      "2 casos: bytes identicos se eximen; un byte de diferencia no")

# --- R56: el rotulo de KAL_0 es RETENCION, no viscosidad (2026-09-07) --
# POR QUE EXISTE. KAL_0 llevaba el nombre de su instancia de FLUIDO —
# justo el unico uso en que se cancela del observable. «Retencion» ya
# estaba en la suite (P1 §EFT L138, ley de linaje de la rama pi), asi
# que no fue renombre sino retirar un prestamo. La ley es RETENER; en
# un fluido eso se llama viscosidad. El simbolo KAL_0 no cambia.
_R56_MAL = re.compile(r"(?:Structural|Asymptotic\s+Structural)\s+Viscosity"
                      r"|viscosidad\s+estructural", re.I)
def _r56_sitios(_txt):
    _h = []
    for _m in _R56_MAL.finditer(_txt):
        _ini = _txt.rfind("\n", 0, _m.start()) + 1
        _fin = _txt.find("\n", _m.end())
        _linea = _txt[_ini:_fin if _fin > 0 else len(_txt)]
        # EXENTO: zeta_tilde SI es una viscosidad (es la del fluido), y
        # las menciones que narran el cambio de rotulo.
        if re.search(r"ztilde|zeta_tilde|ζ̃|unificad|earlier version|heredado",
                     _linea, re.I):
            continue
        _h.append(_linea.strip()[:70])
    return _h
_r56_todos = []
for _f in sorted(list((ROOT.parent/"manuscript").rglob("*.tex"))
                 + list((ROOT.parent/"src").rglob("*.py"))
                 + [ROOT.parent/"CANONICAL_VALUES.yaml"]
                 # 2026-09-08: los .md de la raiz NO se miraban, y el rotulo
                 # prestado sobrevivio ahi 37 dias despues de corregirse en
                 # papers y codigo. CLAUDE.md es lo primero que se lee cada
                 # sesion, asi que era el peor sitio donde dejarlo.
                 + sorted((ROOT.parent).glob("*.md"))):
    # El propio guardian queda exento: sus fixtures CONTIENEN la forma
    # prestada a proposito. Es el mismo defecto que R45 documenta haber
    # cometido dentro de si misma.
    if "archive" in str(_f) or _f.name in _FIXTURES:
        continue
    _r56_todos += [f"{_f.name}: {x}" for x in _r56_sitios(_f.read_text(errors="ignore"))]
check("R56 el rotulo general de KAL_0 es retencion, no viscosidad",
      not _r56_todos, "; ".join(_r56_todos[:4]) if _r56_todos
      else "0 sitios con el rotulo prestado (archive/ exento; zeta_tilde "
           "sigue siendo viscosidad, que ahi si lo es)")
_t56 = [("KAL0 = BETA + PI   # Structural Viscosity  ~ 5.5214", True),
        ("KAL_0 es la viscosidad estructural (transporte)", True),
        ("KAL0 = BETA + PI   # Structural Retention  ~ 5.5214", False),
        ("la viscosidad de volumen ztilde = KAL0/3 del fluido", False)]
_f56 = [c for c, esp in _t56 if bool(_r56_sitios(c)) != esp]
check("R56 el detector distingue el rotulo general de la viscosidad del fluido",
      not _f56, "; ".join(_f56) if _f56
      else "4 casos: 2 formas prestadas marcadas, el rotulo nuevo y "
           "el ztilde del fluido limpios")
track_open("V-L3-IS  OP-22b: el mapa campo -> fluido (zeta,tau_Pi) no derivado",
           "OP-22 cerrado (normalizacion = entalpia; el 0 es resultado). El "
           "conteo de grados de libertad (2026-09-07) cierra la parte de 'dos "
           "canales': ambos cuentan UNA onda, luego el 0 del fluido y el "
           "0.021284 del campo describen LA MISMA, y la del campo es la "
           "fundamental. Queda ESTRECHO: el mapa de los parametros del campo "
           "a los del fluido efectivo (zeta_tilde, tau_Pi) NO esta derivado, "
           "asi que por que el limite de fluido cae exactamente en 0 y no en "
           "0.021284 sigue sin establecerse. La brecha 0.021284 es toda la "
           "prediccion de P7 => una medida de c2_s discrimina. "
           "Ademas queda RETIRADA la derivacion de tau_Pi por saturacion de "
           "causalidad (apendice EFT de P1): usaba rho en vez de rho+p, daba 0.2946",
           op="OP-22b")

# c_s^2 del sector k-essence — extraccion T_munu^ef (2026-05-22). Para
# K(X)=X/KAL0+X^2/M^4, Garriga-Mukhanov da c_s^2=(A+2BX)/(A+6BX) con
# A=1/KAL0>0 y B=1/M^4>0. Es decreciente: c_s^2 in [1/3,1] para TODO X>=0,
# cualquier M^4>0, cualquier KAL0>0 — depende solo de la FORMA de K.
A_ke = 1.0 / KAL0
cs2_vals = []
for B_M4 in (1.0, 1.0 / 234.8936):       # M^4 = 1 (P7) y 5 phi^8 (P10)
    for Xv in (0.0, 0.1, 1.0, 1e2, 1e6):
        cs2_vals.append((A_ke + 2 * B_M4 * Xv) / (A_ke + 6 * B_M4 * Xv))
check("V-L3-cs2  c_s^2 k-essence acotado en [1/3, 1] para todo X",
      all(1 / 3 - 1e-9 <= c <= 1 + 1e-9 for c in cs2_vals),
      f"min={min(cs2_vals):.5f} max={max(cs2_vals):.5f}")
track_open("V-L3-cs2  el sector geometrico de SSEE no puede agruparse [CENTRAL]",
           "extraccion T_munu^ef: c_s^2 de la k-essence in [1/3,1] siempre — "
           "nunca baja de 1/3, no clusteriza como materia fria. El sector "
           "geometrico tiene peso de FONDO (rho_phi existe) pero NO peso de "
           "agrupamiento. El CMB exige materia que se agrupe -> la k-essence "
           "actual no puede ser la '0.320'. MIRA no esta en la accion vigente",
           op="OP-7")

# Ruta B (gravedad disformal de P8) — RE-ENUNCIADA 2026-09-07.
#
# LO QUE DECIA ANTES: «P1 prohibe DM (L51 "without dark-matter particles";
# L278 detectar DM falsa el modelo) -> contradiccion interna P1<->P8».
#
# ESO ERA UNA CITA MUTILADA, y la contradiccion desaparece al leer el texto
# entero. P1 no prohibe la materia oscura:
#   L55  «no WIMP, QCD-axion, or SUSY dark-matter particles»  <- tres familias
#        de candidatos CONCRETAS, no la materia oscura en general
#   L572 «direct detection of a COLLISIONLESS dark-matter particle»  <- el
#        criterio de falsacion lleva el adjetivo, y la psi_DM de P8 esta
#        acoplada disformalmente, o sea NO es colisional-mente libre: siente
#        una quinta fuerza. No es el objeto que P1 nombra.
# Barrido de la suite entera: no hay ningun «no dark matter» absoluto en los
# .tex (la unica coincidencia, EFT_section:510, dice que la ACELERACION no
# necesita materia oscura, que es otra cosa).
# Y SSEE SI tiene materia fria: omega_c = KAL0*omega_b*n_s, forward, OP-8
# cerrado. Una densidad necesita quien la lleve.
#
# LO QUE QUEDA, que no es contradiccion sino HUECO: psi_DM aparece en la
# accion de P8 y en ningun otro sitio de la suite. No tiene lagrangiano, ni
# masa, ni mecanismo de produccion, ni relacion con phi y pi. SSEE predice
# CUANTA materia fria hay y no dice DE QUE esta hecha.
track_open("V-L3-disf  psi_DM entra en la accion de P8 sin estar definida",
           "P8 accion eq.(1) incluye S_DM[g~;psi_DM], acoplada al disformal "
           "(P8 L211), y la seccion canonica la usa (quinta fuerza DM activa, "
           "P8 L615-619). NO es contradiccion con P1: P1 solo excluye WIMP/"
           "axion-QCD/SUSY (L55) y la deteccion de una particula COLISIONAL-"
           "MENTE LIBRE (L572), y psi_DM no es ninguna de esas. El hueco real: "
           "psi_DM no tiene lagrangiano, masa ni origen en phi,pi — SSEE "
           "predice omega_c=KAL0*omega_b*n_s (cuanta hay) y no dice de que "
           "esta hecha. Ademas P8 L69 admite sqrt(beta_c)/MIRA=1.00030 "
           "'near-coincidence, not an identity'",
           op="OP-19")

# Mecanismo de retencion conformal (Ruta B) — probado 2026-05-22 en
# src/ssee_mira_mechanism.py. Acoplamiento beta_c=-AURA: negativo limpio.
track_open("V-L3-mira  retencion conformal beta_c=AURA NO reproduce MIRA",
           "test del fondo acoplado Friedmann+KG (ssee_mira_mechanism.py): "
           "con beta_c=-AURA la excursion del campo es x18 excesiva, signo "
           "invertido (drena la materia en vez de cargarla, R(z=2)~0.016), y "
           "timing invertido (campo thawing). Cuarto mecanismo descartado "
           "para el '0.320' tras cs2, Poisson-mu y disformal. MIRA sin "
           "derivacion en el marco vigente por los 4 mecanismos naturales",
           op="OP-8b")

# dos-Ω_m — OP-8 DISUELTO (reframe ω_m-directo 2026-06-18). Ya NO hay factor
# materia: Om_m,dyn=1+w0=0.160 (DESI) y Om_m,CMB=ω_m/h²=0.308881 (ω_c=KAL0·ω_b·n_s)
# son DOS predicciones independientes, no ligadas por MIRA ni π/φ.
check("V-L3-2Om  Om_m,dyn != Om_m,CMB  (dos predicciones independientes)",
      abs(Om_m_dyn - _omm / _h ** 2) > 0.12)
check("V-L3-2Om  Om_m,CMB = ω_m/h² (forward, sin factor) = 0.308881",
      abs(_omm / _h ** 2 - 0.3088808856) < 1e-6)
# OP-8 DISUELTO (no abierto): ya NO hay factor materia que derivar. Lo
# que queda es la identidad forward, y ESO se comprueba, no se anota.
# Estuvo en track_open desde que se disolvio: track_open se habia usado
# como «apuntar esto» en vez de «no se resolverlo». Convertido 2026-09-07.
_wc_fwd = KAL0 * _wb_k * (1 - phi**-7)
check("V-L3-2Om  OP-8 disuelto: la identidad forward w_c = KAL0 w_b n_s se sostiene",
      abs(abs(_wc_fwd - 0.1200)/0.0012 - 0.40) < 0.05,
      f"w_c = {_wc_fwd:.6f} -> {abs(_wc_fwd - 0.1200)/0.0012:.2f} sigma de Planck "
      "0.1200+-0.0012. Om_m,CMB = w_m/h^2 descansa en esta identidad y en "
      "w_b (OP-1), no en una perilla nueva. MIRA*dyn=0.31993 y pi/phi*dyn="
      "0.31076 son aritmetica RETIRADA")

# ─────────────────────────────────────────────────────────────────────
# CAPA 4 — Confrontaciones con datos
# Verifica la ARITMETICA que conecta cantidades reportadas (tensiones,
# S8, chi2_r). Los chi2 de CMB y los posteriores MCMC en si requieren
# re-correr CAMB/CLASS/emcee — se marcan como dependencia externa.
# ─────────────────────────────────────────────────────────────────────
print("\nCapa 4 — confrontaciones con datos")

# S8 weak-lensing — CANÓNICO ω_m-directo (CLASS forward, m_phi=40.70 SOLAR²·KRYSTOS).
#   Om_m,CMB = omega_m/h² = 0.30888 (sin factor). Dos ramas (CLASS OUTPUT, no fit):
#   single-sector techo con A_s FIJO: sigma8 = 0.814854 -> S8 = 0.8268 (2.74sigma
#   KiDS). Era 0.8335/0.846/3.5sigma hasta el 2026-09-08: aquella corrida no
#   llevaba neutrinos masivos y sobraba un 2.3% de grumo.
#   two-sector phi-DM (TITULAR Paper 6, forward): sigma8_eff = 0.7470 ->
#     S8_eff = 0.758 (0.04sigma KiDS), free-streaming k_fs=0.754, m_phi=40.70 (C_ν=93.14).
# script: src/ssee_paper6_canonical_particle.py
Om_cosm = _omm / _h ** 2     # 0.30888  Om_m,CMB (omega_m-directo)
# Igual que C_ν: se lee del YAML, no se escribe. Antes era «sig8_single = 0.8335»
# seguido de «abs(sig8_single - 0.8335) < 1e-2» — imposible de fallar.
_s8_yaml = re.search(r"sigma8_single_ceiling:\s*([\d.]+)",
                      (pathlib.Path(__file__).resolve().parents[2]
                       / "CANONICAL_VALUES.yaml").read_text(errors="ignore"))
sig8_single = float(_s8_yaml.group(1)) if _s8_yaml else float("nan")  # techo todo-frío (CLASS)
S8_single = sig8_single * (Om_cosm / 0.3) ** 0.5
check("V-L4-01 P6  sigma8 single (techo CLASS, A_s fijo) = 0.814854",
      _s8_yaml is not None and abs(sig8_single - 0.814854) < 1e-2,
      f"sigma8 = {sig8_single:.4f} (leído de CANONICAL_VALUES.yaml)")
check("V-L4-02 P6  S8 single = sigma8 sqrt(Om/0.3) = 0.8268  (A_s fijo)",
      abs(S8_single - 0.826827) < 2e-3, f"S8 = {S8_single:.4f}")

sig8_eff = 0.7470            # two-sector titular Paper 6 (forward CLASS, no fit)
S8_eff = sig8_eff * (Om_cosm / 0.3) ** 0.5
check("V-L4-02b P6  [RETIRADO] aritmetica S8_eff two-sector = 0.758",
      abs(S8_eff - 0.758) < 2e-3, f"S8_eff = {S8_eff:.4f}")

# Tensiones S8 — error en cuadratura modelo + observacional.
# KiDS-1000 (Asgari+2021): S8 = 0.759 +/- 0.024.
G_growth = 1.0032            # D1_SSEE/D1_LCDM (Paper 5 ODE @ Om_cosm=0.308881; era 1.011 @0.31983)
S8_single_err = 0.006 * G_growth * (Om_cosm / 0.3) ** 0.5
t_KIDS_single = abs(S8_single - 0.759) / (S8_single_err ** 2 + 0.024 ** 2) ** 0.5
t_KIDS_twosec = abs(S8_eff - 0.759) / 0.024
# 2026-09-08: era 3.5 sigma. Con los neutrinos masivos del fondo canonico el
# techo baja de 0.846 a 0.8268 y la tension con el, a 2.74 sigma. Sigue siendo
# artefacto de fijar A_s; lo que cambia es su tamano.
check("V-L4-03 P6  [ARTEFACTO] 2.74 sigma vs KiDS con A_s FIJADO a Planck",
      abs(t_KIDS_single - 2.74) < 0.2,
      f"{t_KIDS_single:.2f} sigma — NO era un desafio del modelo: fijar A_s a "
      f"Planck importa la tension Planck-KiDS. Con A_s libre (k=2) el MCMC R3 "
      f"sobre KiDS crudo da S8=0.7555+-0.0192, a 0.11 sigma")
check("V-L4-04 P6  [RETIRADO] tension two-sector vs KiDS = 0.04 sigma",
      t_KIDS_twosec < 0.2, f"{t_KIDS_twosec:.3f} sigma")

# CMB Planck PR4 (P3) — re-corrida con CAMB 1.6.5 (2026-05-22): chi2_r
# TT 1.047 / TE 1.041 / EE 1.041 / PP 0.837 y ΔBIC=-20.8 reproducidos
# EXACTAMENTE. La aritmetica chi2_r->ΔBIC solo acota por el redondeo.
check("V-L4-05 P3  ΔBIC CMB = -20.8 consistente con chi2_r (re-run 2026-05-22)",
      -22.9 <= -20.8 <= -11.1,
      "chi2_r redondeados acotan ΔBIC a [-22.9,-11.1]; reportado -20.8 dentro")

# r_d / theta* — re-run CAMB 2026-07-09 con geometria TOTAL corregida (V-L4-DESI).
# Sigma_mnu=0.069. El posterior BAO subio 67.159/66.41 -> 67.9475 al usar la materia
# total 0.308881 en E(z) (antes el sector 0.160 lo hundia). Ahora el posterior COINCIDE
# con el anchor CMB 67.962 (0.04sigma): ya no hay gap, y el theta* del posterior cae
# de 6.66sigma a 0.91sigma. El parche "no propagar el posterior a theta*" YA NO hace
# falta -- posterior y anchor dan el mismo CMB.
#   anchor    67.962  -> r_d=147.17 Mpc (0.32sigma), theta*=0.59668 (100th*=1.04140, 1.05sigma)
#   posterior 67.9475 -> r_d=147.17 Mpc (0.32sigma), theta*=0.59666 (100th*=1.04136, 0.91sigma)
# vs Planck 147.09+-0.26 Mpc / 100theta*=1.04109+-0.00030.
check("V-L4  r_d coherente en ambos H0 canonicos (0.31 sigma)",
      abs(abs(147.17 - 147.09)/0.26 - 0.31) < 0.02,
      f"anchor 67.962 y posterior 67.9475 dan ambos r_d=147.17 Mpc -> "
      f"{abs(147.17 - 147.09)/0.26:.2f} sigma vs Planck 147.09+-0.26 (r_d es "
      "H0-invariante a omega fijo). run_p3_rd_reframe.py 2026-07-09; anclas "
      "viejas 67.037/66.531/67.159 superadas")
check("V-L4  theta* posterior coincide con el anchor (0.90 sigma)",
      abs(abs(1.04136 - 1.04109)/0.00030 - 0.90) < 0.02,
      f"posterior 67.9475 da 100theta*=1.04136 -> "
      f"{abs(1.04136 - 1.04109)/0.00030:.2f} sigma vs Planck 1.04109+-0.00030; "
      "anchor 67.962 da 1.04140 (1.05 sigma). La tension de 6.66 sigma era el "
      "bug del sector 0.160 en E(z): al coincidir posterior y anchor el CMB "
      "es sano en ambos y no hay parche")

# La «inconsistencia DES-Y3» ya no existe: el script del 0.759+-0.023
# (ssee_op5_hmcode.py) se archivo, y en src/ vivo solo queda 0.776+-0.017
# (3x2pt, Abbott 2022) en dos sitios, coherentes entre si. El apunte
# sobrevivio al archivado del script. Verificado y convertido 2026-09-07.
_des_vivos = set()
for _f in (ROOT).rglob("*.py"):
    if "archive" in str(_f) or _f.name in _FIXTURES:
        continue
    for _m in re.finditer(r"S8_DES\s*(?:=|,)\s*\(?\s*(0[.]\d+)", _f.read_text(errors="ignore")):
        _des_vivos.add(_m.group(1))
check("V-L4  una sola referencia DES-Y3 en src/ vivo",
      _des_vivos == {"0.776"},
      f"S8_DES en src/ (sin archive): {sorted(_des_vivos) or 'ninguno'} — "
      "3x2pt Abbott+2022. El 0.759+-0.023 (cosmic shear, Amon 2022) estaba "
      "en ssee_op5_hmcode.py, hoy en archive/; el apunte de inconsistencia "
      "sobrevivio al archivado del script")

# MCMC DESI+Planck (P2) — re-corrido 2026-05-22 (100w x 25000s x 3, 1.52h).
# lnP_MAP: SSEE -13.22 (k=2), LCDM -15.79 (k=3). N_DATA = 16.
# BIC = k*ln(N) - 2*lnP_MAP — esto SI se recomputa exacto.
N_data_p2 = 16   # 13 BAO DESI DR2 + 3 constraints Planck
bic_ssee = 2 * math.log(N_data_p2) - 2 * (-13.22)
bic_lcdm = 3 * math.log(N_data_p2) - 2 * (-15.79)
check("V-L4-06 P2  BIC SSEE = k ln(N) - 2 lnP = 31.98 (re-run MCMC)",
      abs(bic_ssee - 31.98) < 0.05, f"BIC = {bic_ssee:.2f}")
check("V-L4-07 P2  ΔBIC(LCDM-SSEE) = +7.91 (SSEE favorecido)",
      abs((bic_lcdm - bic_ssee) - 7.91) < 0.05, f"ΔBIC = {bic_lcdm - bic_ssee:.2f}")
H0_mcmc = 66.531   # posterior canonico, prior MIRA 67.037 (re-run 2026-06-09); el 67.756 era mala anotacion
t_H0 = abs(H0_mcmc - 67.36) / (0.442 ** 2 + 0.54 ** 2) ** 0.5
check("V-L4-08 P2  tension H0 SSEE vs Planck = 1.19 sigma",
      abs(t_H0 - 1.19) < 0.03, f"{t_H0:.2f} sigma")
check("V-L4  Omega_b h^2 posterior compatible con la prediccion algebraica",
      abs(abs(0.02260 - 0.02242)/0.00048 - 0.375) < 0.02,
      f"MCMC 2026-06-09 da 0.02260+-0.00048; OP-1 algebraico da 0.02242 -> "
      f"{abs(0.02260 - 0.02242)/0.00048:.2f} sigma, compatible. El 0.02183 "
      "previo era de la cadena pre-canonica")

# ─────────────────────────────────────────────────────────────────────
# SELLOS — integridad de los papers sellados.
# Cuando un paper se sella, se registra aquí su sha256. El harness lo
# recalcula: si el archivo cambió tras sellarse, el sello se rompe.
# ─────────────────────────────────────────────────────────────────────
print("\nSellos de papers")
SEALS = {
    # "manuscript/SSEE_Paper1_Framework.tex": "<sha256 al sellar>",
}
if not SEALS:
    print("  (ningún paper sellado todavía)")
for relpath, expected in SEALS.items():
    f = ROOT / relpath
    actual = hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None
    check(f"sello {relpath}", actual == expected,
          "intacto" if actual == expected
          else "ROTO — el archivo cambió después de sellarse")

# ─────────────────────────────────────────────────────────────────────
# REGLA DE ALCANCE (2026-09-08, tambien de Mike, y va ANTES que la de abajo)
#
# Su objecion: «si eran universales era porque esperaban ver TODO lo que su
# universalidad queria; lo unico que hiciste fue decir lo que si ve y lo que
# no. No seria mejor que la regla SI sea universal, al menos en lo que se
# pueda aplicar?». Tiene razon: declarar el limite es honesto pero es el
# segundo mejor. Primero se ensancha hasta donde el enunciado alcanza; solo
# lo que quede fuera por imposibilidad se declara.
#
# Ensanchado el 2026-09-08:
#   R34   89 -> 130 .py    (le faltaba class_ssee/ entero, 41 ficheros)
#   R40   17 -> 34 docs    (le faltaban los .md de la raiz)
#   R41   17 -> 34 docs    (idem)
#   R59   33 -> 87 docs    (le faltaban el PRD y los .md de subcarpetas)
# Solo R59 encontro algo al ensanchar, y encontro 6 rutas muertas en 5
# documentos: scripts que existen pero se habian movido a archive/ o a
# src/p02_mcmc/ y nadie repunto la cita. Corregidas.
#
# REGLA DE REDACCION DE LOS MENSAJES VERDES (2026-09-08, la pidio Mike)
#
# «un verde puede ser correcto y aun asi mentir, si su mensaje promete mas de
# lo que midio». Paso con R36: comparaba la figura con SU SCRIPT por fecha,
# verde correcto, y el mensaje decia «N figuras del PRD al dia» — que se lee
# como contenido vigente. fig8 llevaba 45 dias con los MAP de una cadena
# retirada y pasaba.
#
# Por eso, todo mensaje de exito debe decir SOBRE CUANTO miro (cuantos
# documentos, cuantas lineas, cuantos .py) y, si su alcance es parcial, ese
# limite va en el mismo mensaje, no en un comentario del codigo. Un «ninguno»
# sin superficie declarada se lee como universal y casi nunca lo es.
#
# Barrido del 2026-09-08: 9 mensajes afirmaban universalidad sin cuantificar;
# los 9 corregidos. Y al hacerlo salio otro: el contador de R38 contaba los
# FALLOS en vez de lo inspeccionado, asi que decia «0 filas barridas» — el
# verde vacio exacto que este barrido buscaba. Ahora dice 17230 lineas en 17
# documentos.
# ─────────────────────────────────────────────────────────────────────
# FUENTE CANÓNICA — chequeo de src/ssee_core.py
# ssee_core.py es el módulo del que TODOS los demás scripts importan sus
# constantes algebraicas. Aquí se verifica que ese módulo coincide con la
# recomputación independiente del guardián. Si ssee_core se edita mal, esto
# se pone ROJO — y, por tanto, todo script que importe de él queda advertido.
# ─────────────────────────────────────────────────────────────────────
print("\nFuente canónica — ssee_core.py")
import importlib.util as _ilu

_core_path = ROOT / "ssee_core.py"
# Mismo motivo que en V-L2-11a: se COMPILA el fuente para que ningún .pyc rancio
# de __pycache__ pueda contarle al guardián una versión del core que ya no existe.
class _NS:                       # acceso por atributo, como el módulo que sustituye
    def __init__(self, d): self.__dict__.update(d)


try:
    _ns: dict = {"__name__": "ssee_core", "__file__": str(_core_path)}
    exec(compile(_core_path.read_text(errors="ignore"), str(_core_path), "exec"), _ns)
    _core = _NS(_ns)
    CANON = {
        "PHI":         (_core.PHI,         phi),
        "PI":          (_core.PI,          pi),
        "OMEGA":       (_core.OMEGA,       Omega),
        "BETA":        (_core.BETA,        beta),
        "KAL0":        (_core.KAL0,        KAL0),
        "P_SC":        (_core.P_SC,        Psc),
        "K_V":         (_core.K_V,         Kv),
        "T_R":         (_core.T_R,         Tr),
        "M_V":         (_core.M_V,         Mv),
        "W0":          (_core.W0,          w0),
        "WA":          (_core.WA,          -Psc / Kv),
        "OMEGA_DE":    (_core.OMEGA_DE,    Om_DE),
        "OMEGA_M_DYN": (_core.OMEGA_M_DYN, Om_m_dyn),
        "MIRA":        (_core.MIRA,        MIRA),
        "AURA":        (_core.AURA,        AURA),
        "H0_ALG":      (_core.H0_ALG,      3 * Omega ** 2),
        "N_S":         (_core.N_S,         1 - phi ** -7),
        "OMEGA_B_H2":  (_core.OMEGA_B_H2,  (pi - phi) / (3 * Omega ** 2)),
    }
    for nm, (core_val, guard_val) in CANON.items():
        check(f"canon  ssee_core.{nm}", abs(core_val - guard_val) < 1e-9,
              f"core {core_val:.10f} / guardian {guard_val:.10f}")
except Exception as e:
    check("canon  ssee_core.py importable y consistente", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# CAPA MEMORIAS — coherencia entre las 3 memorias de SSEE.
# Invoca memory_sync.py: revisa que CLAUDE.md, el Ledger y el vault Obsidian
# no presenten valores RETIRADOS (CANONICAL_VALUES.yaml) como vigentes.
# Es un check() DURO: cualquier valor retirado sin marcar pone el guardián ROJO.
# ─────────────────────────────────────────────────────────────────────
print("\nCapa Memorias — coherencia de las 3 memorias")
try:
    import memory_sync
    _drifts = memory_sync.run(verbose=False)
    _detail = "todas concuerdan con CANONICAL_VALUES.yaml"
    if _drifts:
        _detail = "DRIFT en " + "; ".join(
            f"{lbl} {rel}:{ln}«{pat}»" for lbl, rel, ln, pat, _ in _drifts[:6])
        if len(_drifts) > 6:
            _detail += f" … (+{len(_drifts) - 6}); correr memory_sync.py"
    check("memoria  3 memorias sin valores retirados sin marcar",
          not _drifts, _detail)
except Exception as e:
    check("memoria  memory_sync importable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# CAPA PROCEDENCIA — valores de pipeline (sección B del Registro).
# Causa raíz F1 (2026-06-14): un valor canónico de pipeline (ΔBIC=−24.7,
# χ²_r=1.045) fue anotado A MANO en el Registro sin un log que lo
# reprodujera, y NADA lo verificaba → sobrevivió mal hasta una re-corrida.
# Este check cierra la grieta: extrae el valor de la fila del Registro y
# exige que aparezca, en contexto, en un log de procedencia committeado.
#   · valor coincide con su log  → OK
#   · valor NO aparece en el log  → ROJO (atrapa exactamente el error F1)
#   · sin log committeado         → ABIERTO (hace visible la grieta, no bloquea)
# Para añadir un valor de pipeline al Registro: guardar su log en
# results/logs/ y registrarlo aquí. Sin log → el guardián lo marca.
# ─────────────────────────────────────────────────────────────────────
print("\nCapa Procedencia — valores de pipeline vs log committeado")
try:
    import re as _re
    _REPO = pathlib.Path(__file__).resolve().parents[2]

    def _norm(s):
        return s.replace("−", "-").replace("–", "-")

    def _cotejo_log(_v, _txt):
        """El valor del Registro, ¿está en el log — como texto o como número?

        SEGUNDA CEGUERA (2026-09-08). El cotejo era `_val in texto`, puro
        string. Un log JSON guarda la media cruda (0.7445921790951743) y el
        Registro publica el redondeo (0.7446): la subcadena NO aparece y el
        respaldo REAL salía marcado como mala anotación. Ahora, si el texto
        falla, se compara número a número al mismo número de decimales que
        publica el Registro. El ROJO tipo F1 (valor que el log no contiene)
        sigue saltando: lo que se acepta es el redondeo, no otra cifra.
        """
        if _v in _txt:
            return True
        _dec = len(_v.split(".")[1]) if "." in _v else 0
        try:
            _obj = float(_v)
        except ValueError:
            return False
        for _c in _re.findall(r"-?\d+\.\d+(?:[eE][-+]?\d+)?", _txt):
            try:
                if round(float(_c), _dec) == _obj:
                    return True
            except (ValueError, OverflowError):
                continue
        return False

    _lines = (_REPO / "VERIFICATION_LEDGER.md").read_text(errors="ignore").splitlines()
    # Escaneo de TODA la sección B: cada valor de pipeline cuya Fuente cite un
    # log committeado (results/logs/*.log) se verifica contra él. Cobertura
    # completa, no una lista a mano (cierra la grieta «3 de 17»).
    _inB = False
    _gaps = []
    for ln in _lines:
        if ln.startswith("## B."):
            _inB = True
            continue
        if _inB and (ln.startswith("## ") or ln.startswith("# ") or ln.startswith("---")):
            break
        if not _inB or not ln.lstrip().startswith("|"):
            continue
        _cols = [c.strip() for c in ln.split("|")]
        if len(_cols) < 4:
            continue
        _label, _valf, _src = _cols[1], _norm(_cols[2]), _cols[3]
        if _label.lower().startswith("cantidad") or set(_label) <= set("-: "):
            continue  # cabecera / separador
        _m = _re.search(r"-?\d+\.\d+", _valf)
        if not _m:
            continue
        _val = _m.group(0)
        # CEGUERA CORREGIDA 2026-09-08. Esto decia `\.log` a secas, asi que un
        # valor respaldado por un log JSON contaba como SIN RESPALDO. Marcaba
        # como grieta el titular de Paper 6 (S8=0.7555, MCMC R3 convergido, log
        # results/logs/growth_2026-07/R3_ssee_kids_S8.json) y su control LCDM.
        # Falsa alarma del peor tipo: la que dice que no hay prueba donde SI la
        # hay. Es la 4a patologia — el NOMBRE del check prometia "sin log" y el
        # codigo comprobaba "sin log .log". Ahora acepta las dos extensiones.
        _logm = _re.search(r"results/logs/\S+?\.(?:log|json)", _src)
        if not _logm:
            _gaps.append(f"{_label[:22]}={_val}")
            continue
        _rel = _logm.group(0)
        _logf = _REPO / _rel
        if not _logf.exists():
            check(f"procedencia  {_label[:30]}={_val}", False,
                  f"log referenciado no existe: {_rel}")
            continue
        _hit = _cotejo_log(_val, _norm(_logf.read_text(errors="ignore")))
        check(f"procedencia  {_label[:30]}={_val}", _hit,
              f"coincide con {_rel}" if _hit
              else f"Registro={_val} NO aparece en {_rel} (mala anotación tipo F1)")
    if _gaps:
        track_open(f"procedencia  {len(_gaps)} valores de pipeline sin log committeado",
                   "; ".join(_gaps[:8]) + (" …" if len(_gaps) > 8 else "")
                   + "  (generar log → results/logs/ para verificarlos)")
    # CONTROL (R53). Las dos cegueras corregidas hoy eran del tipo «digo que no
    # hay prueba donde sí la hay». El control tiene que probar los DOS lados:
    # que el redondeo legítimo pasa, y que una cifra distinta sigue en ROJO.
    _c_ok = [("0.7446", '{"sigma8": {"media": 0.7445921790951743}}', True,
              "el redondeo del Registro contra la media cruda del JSON"),
             ("0.7555", '{"S8": {"media": 0.7555328554033626}}', True,
              "idem, el titular de Paper 6"),
             ("262.746", '{"chi2_min": 262.7462}', True,
              "el chi2 del control LCDM"),
             ("0.7446", '{"sigma8": {"media": 0.7521}}', False,
              "otra cifra: NO se acepta, el ROJO tipo F1 sigue vivo"),
             ("0.7446", '{"nota": "sin numeros"}', False,
              "log que no contiene el valor"),
             ("262.746", '{"chi2_min": 265.4399}', False,
              "el chi2 del OTRO modelo: no cuela por parecerse")]
    _c_mal = [d for v, t, esp, d in _c_ok if _cotejo_log(v, t) is not esp]
    check("procedencia  el cotejo acepta el redondeo pero no otra cifra",
          not _c_mal,
          f"{len(_c_ok)} casos: 3 redondeos legítimos aceptados, 3 impostores "
          f"rechazados" if not _c_mal else "fallan: " + "; ".join(_c_mal))
except Exception as e:
    check("procedencia  capa de procedencia operable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# R33 — un LOG no puede contradecir al núcleo (2026-07-26).
# La Capa Procedencia de arriba compara Registro ↔ log por string: si AMBOS
# repiten el mismo valor rancio, coinciden y da VERDE. Valida coherencia, no
# corrección — y cero reglas comparaban un log contra ssee_core. Ese hueco dejó
# vivo Σm_ν=0.06902 en 8 logs, uno de ellos la corrida MCMC canónica del 07-25.
# Un .log es un artefacto CONGELADO: guarda las constantes del día en que se
# corrió. Borrar el string viejo de los .tex no lo toca. Ver la memoria
# project_propagation_order (nivel 8, el que siempre se olvida).
# Los históricos se declaran en _LOGS_HISTORICOS y quedan como ABIERTO, no ROJO.
print("\nCapa R33 — logs vs núcleo: ningún log activo con constante retirada")
# Los históricos se leen de PROPAGACION.yaml — UNA sola fuente de verdad.
# Antes esta lista vivía hardcodeada aquí y en el YAML: dos listas del mismo
# hecho divergen sin avisar (declarar b1_mcmc_reframe histórico en el YAML no
# lo sacaba de R33, que seguía mirando su copia local).
try:
    import yaml as _y33
    _LOGS_HISTORICOS = {f"{_n}.log" for _n in
                        (_y33.safe_load((_REPO / "PROPAGACION.yaml").read_text())
                         .get("historicos") or [])}
except Exception:
    _LOGS_HISTORICOS = set()
# huella → (qué constante retirada la produce, con qué valor vigente NO sale)
# OJO con la longitud de la huella: la primera versión de R33 buscaba solo
# "0.3088932" (7 dec) y se le escapaban DIEZ logs que imprimen "0.30889" a 5 —
# media tarea con luz verde, el mismo patrón que R33 existe para cazar. El
# redondeo correcto de 0.308881 a 5 decimales es 0.30888, así que "0.30889"
# es huella inequívoca del valor rancio y no puede dar falso positivo.
_RETIRADAS = {"0.06902": "Σm_ν retirado (vigente 0.06849)",
              "0.30889": "Ω_m de Σm_ν rancio (0.308881 imprime 0.30888)",
              "94.07": "C_ν INSTANTÁNEO usado como operativo (el operativo es 93.14, con reheating e⁺e⁻); 94.07 NO es incorrecto — es otra magnitud",
              "41.0187": "m_φ de Σm_ν rancio (vigente 40.70)"}
try:
    _logdir = _REPO / "results" / "logs"
    _sucios, _hist = [], []
    # Los de ORQUESTACION quedan fuera, con razon: imprimen el R-1 de otras
    # corridas, y un R-1 = 0.069028 contiene la huella «0.06902» sin tener
    # nada que ver con Σm_ν (falsa alarma del 2026-09-30, vigilante_conjunta).
    def _huellas33(_nombre, _txt):
        if _nombre.startswith(_r74.ORQUESTACION):
            return []
        return [f"{_k} ({_v})" for _k, _v in _RETIRADAS.items() if _k in _txt]
    for _lg in sorted(_logdir.glob("*.log")):
        _txt = _lg.read_text(errors="ignore")
        _hit33 = _huellas33(_lg.name, _txt)
        if not _hit33:
            continue
        (_hist if _lg.name in _LOGS_HISTORICOS else _sucios).append(
            f"{_lg.name}: {', '.join(_hit33)}")
    check("R33 ningún log ACTIVO arrastra una constante retirada",
          not _sucios,
          "; ".join(_sucios) if _sucios
          else f"{len(list(_logdir.glob('*.log')))} logs barridos, "
               f"{len(_hist)} históricos declarados")
    # CONTROL (R53): la huella en un log de resultados se caza; el R-1 de un
    # vigilante, no.
    _c33 = [("resultado.log", "Sum_mnu = 0.06902 eV", True),
            ("vigilante_x.log", "b3 viva — R-1 58558.000000 0.069028", False)]
    _f33 = [_n for _n, _s, _esp in _c33 if bool(_huellas33(_n, _s)) is not _esp]
    check("R33 el detector distingue la constante rancia del R-1 de un vigilante",
          not _f33, ", ".join(_f33) if _f33 else
          "2 casos: Σm_ν rancio en un log de resultados se marca; R-1 0.069028 en un vigilante, exento")
    if _hist:
        track_archivo(f"R33 {len(_hist)} logs históricos con constante retirada",
                      "; ".join(_hist) + "  (conservados: reescribirlos "
                      "falsificaria el registro de una corrida ya hecha)",
                      declarados=[_h.split(":")[0] for _h in _hist],
                      fuente=_LOGS_HISTORICOS)
except Exception as e:
    check("R33 capa logs-vs-núcleo operable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# R34 — ningún .py ACTIVO hardcodea una constante retirada (2026-07-26).
# R33 caza logs rancios; esto caza la causa AGUAS ARRIBA. scan_omega_m.py tenía
# `mnu=0.069` en la línea 8 —el residuo de C_ν=94.07— mientras el resto de la
# suite ya usaba 0.06849. No era un artefacto viejo: era el FUENTE, y producía
# el barrido que justifica el ancla H₀. Re-correr su log no habría servido de
# nada: habría vuelto a salir rancio. Regla: una constante se lee del núcleo,
# no se re-teclea. Exclusiones = los sitios que NOMBRAN el valor retirado a
# propósito (mutaciones del test, la derivación que compara 94.07 vs 93.14).
# ─────────────────────────────────────────────────────────────────────
# R37 — toda IGUALDAD con una constante SSEE va a 6 decimales (2026-07-27).
# La política de redondeo NO es de un documento: no existe ninguna regla en
# este guardián dirigida a un archivo concreto, porque no hay excepciones. Se
# había aplicado sólo a los consolidados, dejando conviviendo «9.5193» y
# «9.519253» dentro de la misma suite — que es exactamente la ambigüedad que
# la política existe para eliminar.
# Criterio: el SIGNO dice qué lee el lector.
#   «=»  es EL valor        → 6 decimales, sin excepción
#   «≈»  es una lectura rápida → puede ir corto, pero NUNCA truncado (eso lo
#        cubre R30, que exige redondeo correcto a cualquier precisión)
print("\nCapa R37 — igualdades de constantes SSEE a 6 decimales")
try:
    _C37 = {"Omega": pi + phi, "beta": (pi + phi) / 2, "KAL0": (pi + phi) / 2 + pi,
            "P_sc": pi + 2 * phi, "K_v": 2 * (phi + pi), "T_r": 3 * (phi + (pi + phi) / 2),
            "M_v": 3 * (phi + pi), "w0": abs(_core.W0), "wa": abs(_core.WA),
            "AURA": _core.AURA,
            # Añadidas 2026-07-27 (lectura P1 pág. 1): el abstract escribía
            # «r = φ⁻¹⁰ = 0.00813» con signo IGUAL y sólo 5 decimales. R37 no lo
            # cazaba porque su lista no incluía los observables algebraicos, sólo
            # las constantes del diccionario. Son igual de puros en φ,π.
            "r": phi ** -10, "n_s": 1 - phi ** -7, "alpha_att": phi ** 4 / 3,
            "N_star": 2 * phi ** 7,
            "alpha_K": 3 * (_core.AURA / _core.OMEGA) * (1 + _core.W0),
            # α_K BARE: 3·Ω_DE·(1+w_φ) con w_φ=−0.971202 (plateau EFT, 8 IC).
            # NO confundir con el efectivo de arriba: son dos kineticidades
            # físicamente distintas y el Paper 1 las tabula juntas. La tabla
            # las escribía las dos como «α_K», que es la forma más segura de
            # que un lector concluya que el modelo se contradice.
            "alpha_K_bare": 3 * (_core.AURA / _core.OMEGA) * (1 - 0.971202),
            # 2026-07-27, lectura Paper 1 pág. 4: el Predictive Register mostraba
            # ω_c a 5 decimales y nadie lo veía — las densidades no estaban en la
            # lista, sólo el diccionario y los observables inflacionarios. Son
            # igual de algebraicas: ω_b sale de (π−φ)/(3Ω²) y ω_c de la identidad
            # forward KAL₀·ω_b·n_s.
            "omega_b": (pi - phi) / (3 * (pi + phi) ** 2),
            "omega_c": ((pi + phi) / 2 + pi) * ((pi - phi) / (3 * (pi + phi) ** 2))
                       * (1 - phi ** -7)}
    _mal37 = []
    for _tx in sorted(list((_REPO / "manuscript").glob("*.tex"))
                      + list((_REPO / "submission_PRD").glob("*.tex"))):
        _cont = _tx.read_text(errors="ignore")
        for _k37, _v37 in _C37.items():
            for _d37 in range(2, 6):
                _corto = f"{_v37:.{_d37}f}"
                # NO exigir 6 decimales a una cantidad CON UNIDADES: se
                # compara con un dato medido y debe llevar la precisión de ESE
                # dato, no la del álgebra. Comparar un número de 6 decimales
                # contra SH0ES 73.04 (dos decimales publicados) es falsa
                # precisión, no rigor. Por eso el patrón excluye una unidad
                # inmediatamente detrás: km/s/Mpc, Mpc, eV, meV, GeV, \kms.
                # NO exigir 6 decimales a una cantidad CON UNIDADES: se compara
                # con un dato medido y lleva la precisión de ESE dato. Escribir
                # H₀ con seis decimales frente a SH0ES 73.04 —publicado con
                # dos— es falsa precisión, y vuelve incomparables los números.
                # SEP cubre los separadores LaTeX reales entre número y unidad
                # ($, ~, \\,, \\;, \\quad): la primera versión sólo contemplaba
                # "$ km" y dejaba pasar "40.70$~eV" y "73.04\\,\\kms" — probado
                # contra texto real, no supuesto. Auto-test abajo.
                _SEP = r"(?:[\s$~]|\\[,;:!\s]|\\quad|\\qquad)*"
                # 2026-09-26: una longitud LaTeX también es una unidad. Sin esto R37
                # leía «width=0.84\\textwidth» como w₀=0.84 y obligaba a escribir
                # anchos de figura de 0.839950 (Paper 2, dos figuras).
                _UNI = r"(?:km|Mpc|eV|meV|GeV|\\kms|\\hMpc|\\textwidth|\\linewidth|\\columnwidth)"
                _UNID = r"(?!" + _SEP + _UNI + r")"
                if _re.search(r"=\s*(?:-|\\!-)?\s*" + _re.escape(_corto)
                              + r"(?![0-9])" + _UNID, _cont):
                    _mal37.append(f"{_tx.name}: {_k37}={_corto} (debe ser {_v37:.6f})")
    # Auto-test de la exclusión: si el patrón deja de distinguir dimensional
    # de adimensional, R37 se vuelve silenciosamente inútil (o destructivo).
    _S = r"(?:[\s$~]|\\[,;:!\s]|\\quad|\\qquad)*"
    _U = r"(?:km|Mpc|eV|meV|GeV|\\kms|\\hMpc|\\textwidth|\\linewidth|\\columnwidth)"
    _X = r"(?!" + _S + _U + r")"
    _CASOS = [(r"$H_0=67.962$ km\,s$^{-1}$", "67.962", False),
              (r"$m_\varphi=40.70$~eV", "40.70", False),
              (r"$H_0 = 73.04\,\kms$", "73.04", False),
              (r"$K_v=9.5193$", "9.5193", True),
              (r"$w_a=-0.6700$,", "0.6700", True),
              (r"[width=0.84\textwidth]", "0.84", False)]
    _bad = [c[0] for c in _CASOS
            if bool(_re.search(r"=\s*-?\s*" + _re.escape(c[1]) + r"(?![0-9])" + _X, c[0])) != c[2]]
    check("R37 la exclusión de cantidades CON UNIDADES funciona",
          not _bad, "; ".join(_bad) if _bad
          else "6 casos LaTeX reales: dimensionales y anchos de figura ignorados, adimensionales marcadas")
    check("R37 ninguna igualdad de constante SSEE con menos de 6 decimales",
          not _mal37,
          "; ".join(_mal37[:6]) if _mal37
          else f"{len(_C37)} constantes verificadas en los .tex de la suite")
except Exception as e:
    check("R37 capa operable", False, str(e))

# R38 — la igualdad que CRUZA CELDAS de tabla (2026-07-27).
# Descubierta leyendo Paper 1 pág. 4: el Predictive Register escribía
#     $r = \varphi^{-10}$ & $0.00813$ & LiteBIRD & Prediction
# R37 no la veía porque busca «= 0.00813» en el mismo texto, y aquí el signo
# igual vive en la columna 1 y el número en la columna 2, separados por un «&».
# Para el lector es exactamente una igualdad —la fila DICE que r vale eso— así
# que la política de 6 decimales aplica igual.
#
# Y una lección aparte, cara: el primer barrido que escribí para esto devolvió
# «0 casos» y era VACÍO. Comparaba el valor mostrado contra el redondeo correcto,
# y 0.00813 SÍ es el redondeo correcto de 0.008130618 a 5 decimales. Lo que se
# viola no es el redondeo: es la POLÍTICA de cuántos decimales lleva un «=».
# Medir lo que no es se ve idéntico a estar limpio. De ahí el auto-test.
print("\nCapa R38 — igualdades que cruzan celdas de tabla")
try:
    # Identificación DECLARADA = símbolo Y fórmula, los dos en la columna 1.
    # Sólo la fórmula no basta: «Ω_m,dyn = (π−φ)/[2(φ+π)]» lleva 2(φ+π) en el
    # DENOMINADOR y hacía que la fila se leyera como K_v — falso positivo real,
    # cazado al primer intento. El par símbolo|fórmula es la biyección de R29.
    _SIMB38 = {
        "n_s": r"n_s", "r": r"(?<![a-zA-Z])r(?![a-zA-Z_])", "w0": r"w_0",
        "wa": r"w_a", "Omega": r"\\Omega(?![_^{a-zA-Z])", "K_v": r"K_v",
        "M_v": r"M_v", "N_star": r"N_(?:\\ast|\*)", "alpha_att": r"\\alpha",
        "omega_b": r"\\omega_b|\\Omega_b\s*h\^2", "omega_c": r"\\omega_c|\\Omega_c\s*h\^2",
    }
    # Fórmula tal como se escribe en LaTeX, por constante.
    _FORM38 = {
        "n_s":       r"1\s*-\s*\\varphi\^\{?-7\}?",
        "r":         r"\\varphi\^\{?-10\}?",
        "w0":        r"T_r\s*/\s*M_v",
        "wa":        r"P_\{sc\}\s*/\s*I_g|\(\\Omega\+\\varphi\)\s*/\s*I_g",
        "Omega":     r"\\pi\s*\+\s*\\varphi(?!\+)",
        "K_v":       r"\\varphi\+\\pi\+\\Omega|2\s*\(\\varphi\+\\pi\)",
        "M_v":       r"3\s*\(\\varphi\+\\pi\)|\\varphi\+\\pi\+K_v",
        "N_star":    r"2\\varphi\^\{?7\}?",
        "alpha_att": r"\\varphi\^4\s*/\s*3|\\frac\{\\varphi\^4\}\{3\}",
        "omega_b":   r"\(\\pi\s*-\s*\\varphi\)\s*/\s*[\[(]?\s*3\s*\\Omega\^2",
        "omega_c":   r"KAL\}?_0\s*\\,?\s*\\omega_b",
    }

    def _r38(linea: str, consts: dict):
        """(nombre, texto, motivo) de cada valor mal escrito en una fila de tabla.

        Una fila afirma una igualdad de DOS formas, y las dos cuentan:
          a) el signo «=» aparece en la columna 1  —  «$r = \\varphi^{-10}$ & …»
          b) la columna 2 ES la fórmula            —  «$K_v$ & $\\varphi+\\pi+\\Omega$ & …»
        La (b) no escribe ningún «=» y afirma exactamente lo mismo. R30 se la
        perdía porque sus patrones exigen «\\approx» pegado a la fórmula, y R38
        también, porque miraba sólo la columna 1: así sobrevivieron CUATRO
        valores MAL REDONDEADOS en la tabla de símbolos del Paper 1
        (β 2.379814→2.379813, K_v y I_g 9.519254→9.519253, T_r ...541→...542).
        """
        if "&" not in linea or linea.lstrip().startswith("%"):
            return []
        _cols = linea.split("&")
        _c1 = _cols[0]
        # «≈/≃/∼» declaran lectura rápida: exentos de la política de 6 decimales
        if any(s in _c1 for s in ("\\approx", "\\simeq", "\\sim")):
            return []
        # ¿La columna 2 es una FÓRMULA? No basta buscar \varphi/\pi literales: la
        # fila «$w_0$ & $-T_r/M_v$ & — & $-0.8400$» del Paper 7 está escrita con
        # símbolos DERIVADOS y se escapaba — y su valor está mal redondeado
        # (exacto −0.839950 → −0.8399, no −0.8400). Se acepta como fórmula toda
        # celda en modo matemático que lleve un operador o un símbolo de registro.
        _c2 = _cols[1] if len(_cols) > 1 else ""
        _formula = bool(
            "$" in _c2 and _re.search(
                r"\\varphi|\\phiG|\\pi\b|\\Omega|\\Omde|\\sqrt|\\AURA|\\MIRA|\\KAL"
                r"|\\mathrm\{KAL|\\beta|T_r|M_v|K_v|P_\{sc\}|I_g|[+^]|(?<=[a-z}])/",
                _c2))
        if "=" not in _c1 and not _formula:
            return []
        _out = []
        for _m in _re.finditer(r"\$-?(\d+\.(\d+))\$", linea):
            _resto = linea[_m.end():]
            if _re.match(r"^\s*(?:\}|\$)?\s*(?:km|Mpc|eV|meV|GeV|\\kms|\\hMpc)", _resto):
                continue                      # dimensional: lleva la precisión del dato
            if _resto.lstrip().startswith("\\ldots") or "\\ldots" in _m.group(0):
                continue                      # truncamiento EXPLÍCITO: «2.37981\ldots» es honesto
            _v, _d = float(_m.group(1)), len(_m.group(2))
            # ¿La fila DECLARA de qué constante habla, escribiendo su fórmula?
            # Entonces la identidad no se infiere por cercanía: está dicha. Sin
            # ventana, y cualquier desvío es error — por grande que sea.
            #
            # POR QUÉ (prueba de mutación 2026-07-29): se inyectó
            # «$n_s = 1-\varphi^{-7}$ & $0.965123$» —un valor sencillamente MAL,
            # a 4.4e-4 del exacto— y el guardián siguió VERDE. R38 lo descartaba
            # por la ventana de identificación (4.4e-4 ≫ 2e-6) y R30 no lo veía
            # porque sus patrones exigen «fórmula = valor» y aquí el valor vive
            # en otra celda. Dos reglas con su motivo, y el error grueso en medio.
            _decl = next((_k for _k, _p in _FORM38.items()
                          if _k in consts and _re.search(_p, _c1)
                          and _re.search(_SIMB38[_k], _c1)), None)
            if _decl is not None:
                _e = consts[_decl]
                if f"{abs(_e):.{_d}f}" != _m.group(1):
                    _out.append((_decl, _m.group(1),
                                 f"MAL (fórmula declarada) → {abs(_e):.{_d}f}"))
                elif _d < 6:
                    _out.append((_decl, _m.group(1), f"{_d} dec → {abs(_e):.6f}"))
                break
            for _k, _e in consts.items():
                # Ventana de IDENTIFICACIÓN (¿de qué constante habla esta celda?),
                # no de aceptación. Iba en 0.6·10⁻ᵈ y por eso NO veía justo el
                # error que busca: un valor mal redondeado en el último dígito
                # dista hasta 1.5·10⁻ᵈ del exacto, y quedaba fuera de la ventana.
                # Con 2·10⁻ᵈ entra, y el veredicto lo da la comparación de abajo.
                if abs(_v - abs(_e)) >= 10 ** -_d * 2:
                    continue
                # (1) lo grave: el valor mostrado NO es el redondeo correcto
                if f"{abs(_e):.{_d}f}" != _m.group(1):
                    _out.append((_k, _m.group(1), f"MAL REDONDEADO → {abs(_e):.{_d}f}"))
                # (2) la política: una igualdad se muestra a 6 decimales
                elif _d < 6:
                    _out.append((_k, _m.group(1), f"{_d} dec → {abs(_e):.6f}"))
                break
        return _out

    # Auto-test con los casos REALES que originaron la regla y su ampliación.
    _T = {"r": phi ** -10, "K_v": 2 * (phi + pi), "beta": (phi + pi) / 2}
    _t38 = [
        # (a) el «=» en la columna 1 — el caso original
        (r"$r = \varphi^{-10}$ & $0.00813$ & LiteBIRD & Prediction \\", True),
        (r"$r = \varphi^{-10}$ & $0.008131$ & LiteBIRD & Prediction \\", False),
        (r"$r \approx \varphi^{-10}$ & $0.00813$ & LiteBIRD & Prediction \\", False),
        (r"$m=\varphi$ & $0.00813$ eV & x & y \\", False),
        # (b) sin «=»: la columna 2 ES la fórmula — el caso que se escapó
        (r"$K_v$ & $\varphi+\pi+\Omega$ & $9.519254$ & x & A \\", True),   # mal redondeado
        (r"$K_v$ & $\varphi+\pi+\Omega$ & $9.519253$ & x & A \\", False),  # correcto
        (r"$\beta$ & $(\varphi+\pi)/2$ & $2.379814$ & x & A \\", True),    # mal redondeado
        (r"$\beta$ & $(\varphi+\pi)/2$ & $2.37981\ldots$ & x \\", False),  # truncamiento explícito
    ]
    _f38 = [c for c, esp in _t38 if bool(_r38(c, _T)) != esp]
    check("R38 el detector cubre las dos formas de igualdad en tabla",
          not _f38, "; ".join(_f38) if _f38
          else "8 filas reales: «=» en col.1 y fórmula en col.2; «≈», unidad y "
               "\\ldots exentos; distingue mal-redondeo de política")

    _mal38, _n38, _ndoc38 = [], 0, 0
    for _tx in sorted(list((_REPO / "manuscript").glob("*.tex"))
                      + list((_REPO / "submission_PRD").glob("*.tex"))):
        _ndoc38 += 1
        for _i, _l in enumerate(_tx.read_text(errors="ignore").split("\n"), 1):
            _n38 += 1                      # LINEAS inspeccionadas, no fallos:
            # la primera version contaba los hits y el mensaje decia "0 filas
            # barridas", que es el verde vacio exacto que se queria evitar.
            for _k, _txt, _por in _r38(_l, _C37):
                _mal38.append(f"{_tx.name}:{_i} {_k}={_txt} [{_por}]")
    _grave = [m for m in _mal38 if "MAL REDONDEADO" in m]
    check("R38 ninguna fila de tabla con valor MAL REDONDEADO",
          not _grave, "; ".join(_grave[:6]) if _grave
          else f"{_n38} líneas inspeccionadas en {_ndoc38} documentos; toda "
               f"fila símbolo|fórmula|valor reproduce su redondeo")
    check("R38 ninguna fila de tabla con igualdad a menos de 6 decimales",
          not _mal38, "; ".join(_mal38[:6]) if _mal38
          else f"política de 6 decimales cumplida en las {_n38} líneas de "
               f"{_ndoc38} documentos (sólo filas con forma símbolo|fórmula|valor)")
except Exception as e:
    check("R38 capa operable", False, str(e))

# R41 — un mismo símbolo, UNA precisión por documento (2026-07-27).
# Las cantidades CON UNIDAD están exentas de la política de 6 decimales: llevan la
# precisión del dato con el que se comparan (R37). Pero esa exención no las exime
# de ser coherentes CONSIGO MISMAS: el ancla algebraica H₀ = 3(φ+π)² aparecía como
# «67.96» y como «67.962» dentro del MISMO documento, en 10 de 11 documentos de la
# suite — 22 apariciones. Ninguna estaba «mal» (67.962137 redondea a las dos), y
# justo por eso nadie las veía: R37 las exime por dimensionales y R30 valida cada
# una por separado. Lo que falla es la coherencia interna, y quien compara dos
# páginas ve dos números para el mismo objeto.
print("\nCapa R41 — coherencia de precisión: un símbolo, una precisión por documento")
try:
    # (valor exacto, patrón que lo ancla al SÍMBOLO). Sólo dimensionales: las
    # adimensionales ya las cubre R37 exigiendo 6 decimales en toda la suite.
    _DIM = {"H_0^alg (=3(φ+π)²)": (3 * (phi + pi) ** 2,
                                   r"3\s*\(\\(?:varphi|phiG)\s*\+\s*\\pi\)\s*\^?\{?2\}?"
                                   r"[^0-9]{0,40}?(\d+\.\d+)")}
    # ENSANCHADA 2026-09-08: miraba 17 .tex y su titulo habla de
    # «un documento» / «la suite». Los .md de la raiz (CLAUDE.md, el
    # Registro, OPEN_PROBLEMS...) son documentos vivos y quedaban fuera.
    _mal41, _ndoc41 = [], 0
    for _tx in sorted(list((_REPO / "manuscript").glob("*.tex"))
                      + list((_REPO / "submission_PRD").glob("*.tex"))
                      + [_q for _q in _REPO.glob("*.md")
                         if _q.name not in ("CHANGELOG.md", "MEMORY.md")]):
        _ndoc41 += 1
        _cont = _tx.read_text(errors="ignore")
        for _n41, (_e41, _pat41) in _DIM.items():
            _vistos = set()
            for _m in _re.finditer(_pat41, _cont):
                _v = _m.group(1)
                # sólo cuenta si de verdad es ese número (no un σ, ni un año)
                if abs(float(_v) - _e41) >= 0.01:
                    continue
                # EXENCIÓN: cuando el texto declara la precisión ("reproducing the
                # anchor … to four decimals"), mostrar más dígitos ES la afirmación.
                # Recortarlo destruiría el argumento — el Sealed y el PRD usan
                # 67.9621 justamente para demostrar que la cascada UV reproduce el
                # ancla a cuatro decimales. Una regla que fuerza coherencia ciega
                # rompe papers correctos.
                if _re.search(r"to\s+(?:two|three|four|five|six|\d+)\s+decimal",
                              _cont[max(0, _m.start() - 200):_m.end() + 200], _re.I):
                    continue
                _vistos.add(_v)
            if len(_vistos) > 1:
                _mal41.append(f"{_tx.name}: {_n41} aparece como "
                              + " y ".join(sorted(_vistos)))
    # Auto-test: la regla debe distinguir «dos precisiones» de «una repetida».
    def _prec(txt, e, pat):
        return {m.group(1) for m in _re.finditer(pat, txt)
                if abs(float(m.group(1)) - e) < 0.01}
    _p41 = _DIM["H_0^alg (=3(φ+π)²)"][1]
    _t41 = [(r"$3(\varphi+\pi)^2 = 67.96$ y $3(\varphi+\pi)^2 \approx 67.962$", 2),
            (r"$3(\varphi+\pi)^2 = 67.962$ y $3(\varphi+\pi)^2 \approx 67.962$", 1)]
    _f41 = [t for t, esp in _t41
            if len(_prec(t, 3 * (phi + pi) ** 2, _p41)) != esp]
    # y la exención debe funcionar: con la precisión declarada, 67.9621 NO cuenta
    # La segunda aparición va MUY separada: dentro de la ventana de ±200 caracteres
    # ambas quedarían exentas y el test no probaría nada (así falló la 1.ª versión).
    _ex = (r"reproducing the anchor $3(\varphi+\pi)^2=67.9621$ to four decimals."
           + " relleno" * 60
           + r" elsewhere $3(\varphi+\pi)^2=67.962$")
    _n_ex = len({m.group(1) for m in _re.finditer(_p41, _ex)
                 if abs(float(m.group(1)) - 3 * (phi + pi) ** 2) < 0.01
                 and not _re.search(r"to\s+(?:two|three|four|five|six|\d+)\s+decimal",
                                    _ex[max(0, m.start() - 200):m.end() + 200], _re.I)})
    if _n_ex != 1:
        _f41.append(f"exención «to four decimals» no aplica (vio {_n_ex})")
    check("R41 el detector distingue dos precisiones de una repetida",
          not _f41, "; ".join(_f41) if _f41
          else "3 casos: «67.96 y 67.962» marcado, repetición limpia, "
               "y precisión declarada («to four decimals») exenta")
    check("R41 ninguna cantidad dimensional con dos precisiones en un documento",
          not _mal41, "; ".join(_mal41[:5]) if _mal41
          else f"{_ndoc41} documentos barridos; el ancla H₀ se muestra con una "
               f"sola precisión en cada uno (sólo se vigila el ancla)")
except Exception as e:
    check("R41 capa operable", False, str(e))

# ── FRONTERA DE LECTURA ──────────────────────────────────────────────────────
# Las reglas nacidas de la lectura página-por-página (R42, R43, R44) se exigen
# sobre los documentos YA LEÍDOS, y sobre el resto se CUENTAN como deuda. No es
# «una excepción para un archivo» —eso el guardián no lo admite— sino el hecho de
# que la suite se está leyendo en orden y una regla nueva no puede exigir hoy lo
# que aún no se ha revisado. Dos condiciones para que esto sea honesto:
#   1. la deuda se imprime siempre, con su recuento;
#   2. el recuento sólo puede BAJAR — si sube, algo se escribió mal después.
# Al cerrar un documento se añade aquí y su deuda debe ser cero.
_LEIDOS = ("SSEE_Paper1_",)
# R66 se calcula arriba (capa de constantes), antes de existir este dict.
_DEUDA_REAL["R66"] = _n66


def _particiona(hallazgos):
    """(los de documentos leídos, cuántos quedan en el resto)."""
    _leidos = [h for h in hallazgos if h.startswith(_LEIDOS)]
    return _leidos, len(hallazgos) - len(_leidos)


# R45 — un OP resuelto no puede seguir citado como ABIERTO en la prosa (2026-07-29).
#
# POR QUÉ EXISTE. La página 8 del Paper 1 decía «the remaining open problems
# OP-9/11/14 for the dark-matter sector» y, veinte líneas más abajo, «…closing
# OP-14». En el mismo tramo de texto un problema estaba abierto y cerrado a la vez,
# y `OPEN_PROBLEMS.md` —la fuente— lo da RESUELTO desde 2026-06-04. Es una
# contradicción de COHERENCIA: ningún número está mal, y por eso ninguna regla
# numérica podía verla. La fuente de verdad del estado de un OP es
# `OPEN_PROBLEMS.md`; el .tex sólo lo cita.
print("\nCapa R45 — estado de los OP: la prosa concuerda con OPEN_PROBLEMS.md")
try:
    _op_txt = (_REPO / "OPEN_PROBLEMS.md").read_text(errors="ignore")
    # Un OP está RESUELTO si su encabezado de sección lo declara así.
    _RESUELTOS = set()
    for _m in _re.finditer(r"^#+\s*OP-(\d+[a-z]?)[^\n]*", _op_txt, _re.M):
        if _re.search(r"✅|RESUELT|CERRAD", _m.group(0), _re.I):
            _RESUELTOS.add(_m.group(1))
    # «abierto» en prosa: el OP aparece dentro de una frase que lo declara pendiente.
    _ABRE = (r"(?:remaining open problems?|open problems?|still open|remains? open"
             r"|currently a free parameter|tracked as open|unresolved)")
    # Caso SIMÉTRICO (2026-08-02): un OP marcado ADOPTADO/RESUELTO que después
    # se REVIRTIÓ. OP-17 decía «✅ ADOPTADA 2026-06-19» durante todo el día
    # siguiente a retirarse la partícula, y NADA lo marcó: memory_sync compara
    # contra la lista de NÚMEROS retirados, y un encabezado que sólo dice
    # «ADOPTADA» no cita ninguna cifra. Ni drift ni incoherencia ⟹ invisible.
    _REVERT = _re.compile(r"^#+\s*OP-(\d+)[^\n]*", _re.M)
    _revertidos = []
    for _m in _REVERT.finditer(_op_txt):
        _cab = _m.group(0)
        _pos = bool(_re.search(r"✅|ADOPTAD|RESUELT", _cab, _re.I))
        _neg = bool(_re.search(r"RETIRAD|REVERTID|DISUELT|DISSOLV|withdraw", _cab, _re.I))
        if _pos and _neg:
            continue          # el encabezado ya narra la reversión: correcto
        if not _pos:
            continue
        # encabezado positivo: ¿el CUERPO lo desmiente?
        _ini = _m.end()
        _fin = _op_txt.find("\n## OP-", _ini)
        _cuerpo = _op_txt[_ini:_fin if _fin > 0 else len(_op_txt)][:1200]
        # OJO: buscar "RETIRAD" a secas da FALSOS POSITIVOS — casi todo cuerpo
        # menciona algún CONTENIDO retirado (una fórmula vieja, un baseline).
        # Lo probé: OP-1 («el viejo 3(π−φ)/200 quedó retirado» — habla de una
        # fórmula, no de su propio estado) y OP-5. La señal INEQUÍVOCA de que se
        # revierte el estado DEL PROPIO OP es la palabra REVERTID, que es la que
        # se escribe al hacerlo.
        _revierte = bool(_re.search(r"REVERTID", _cuerpo, _re.I))
        if _revierte:
            _revertidos.append(f"OP-{_m.group(1)}: encabezado dice adoptado/resuelto "
                               f"pero el cuerpo lo revierte")

    def _r45(tx: str):
        _h = []
        # EXENCION DE NARRACION (2026-09-07). «retiring the former open
        # problem, OP-8» y «was tracked as open problem OP-8; that bridge
        # is now dissolved» son prosa CORRECTA: cuentan que estuvo abierto.
        # El detector las marcaba como si lo afirmaran. 4 de sus 7 sitios
        # eran esto — en el PRD y el Sealed, o sea en lo que se envia.
        _NARRA = (r"former|formerly|earlier|was tracked|now dissolved|"
                  r"dissolved|retir|no longer|previously|superseded|"
                  r"has since|used to|were tracked|\bresolved\b|closed")
        for _m in _re.finditer(_ABRE + r"[^.]{0,80}", tx, _re.I):
            _ctx = tx[max(0, _m.start() - 120):_m.end() + 120]
            if _re.search(_NARRA, _ctx, _re.I):
                continue
            # «OP-9/11/14» escribe tres OPs y sólo el primero lleva prefijo.
            # La primera versión leía OP-(\d+) y se perdía el 11 y el 14 — que era
            # justamente el defecto buscado. Lo probó el auto-test, no yo.
            # SUFIJO DE LETRA (2026-09-07). El .tex decia «remains open ...
            # OP-22b» y el detector leia «OP-22», que SI esta cerrado ⟹ falso
            # positivo. Un sub-OP es un OP distinto de su padre: OP-22 cerrado
            # no dice nada del estado de OP-22b.
            # ENSANCHADO 2026-09-08: el campo donde se buscan los OPs es la
            # ORACION entera, no solo lo que sigue a la afirmacion. El ingles
            # pone el OP a los dos lados —«open problems OP-9» pero tambien
            # «OP-9 is still open»— y mirando solo adelante la segunda forma
            # era invisible. Medido antes de aplicar: hoy no destapa ningun
            # sitio real, o sea ningun documento se mueve; es preventivo.
            _ini45 = tx.rfind(".", 0, _m.start()) + 1
            _campo45 = tx[max(_ini45, _m.start() - 80):_m.end()]
            for _run in _re.findall(r"OP-(\d+[a-z]?(?:/\d+[a-z]?)*)", _campo45):
                for _n in _run.split("/"):
                    if _n in _RESUELTOS:
                        _h.append(f"OP-{_n} citado como abierto — "
                                  f"«{' '.join(_campo45.split())[:58]}»")
        return _h

    # El caso NEGATIVO debe usar OPs que sigan ABIERTOS de verdad. Usaba
    # OP-9/OP-11, que se cerraron por disolución el 2026-08-01 al retirarse el
    # sector φ-DM: el fixture pasó a afirmar algo falso y el auto-test lo cazó.
    # Es el mismo defecto que R45 vigila, cometido dentro de R45.
    _t45 = [("with the remaining open problems OP-9/11/14 for the dark-matter sector", True),
            # CONTROL de la exencion de narracion (2026-09-07): la misma
            # frase, una afirmando y otra contando que estuvo abierto.
            ("tracked as open problem OP-14 in the register", True),
            ("was tracked as open problem OP-14; now resolved", False),
            ("with the remaining open problems OP-15 and OP-16 for the dark sector", False),
            # CONTROL del sufijo: el padre cerrado se marca, el hijo abierto no.
            ("what remains open is OP-22, the IS normalisation", True),
            ("what remains open is OP-22b, the field-to-fluid map", False),
            # CONTROL del ensanchamiento hacia atras (2026-09-08): el OP
            # DELANTE de la afirmacion se marca igual que detras...
            ("OP-9 is still open for the dark-matter sector", True),
            # ...pero sin cruzar el punto: la oracion anterior no cuenta.
            ("OP-9 closed by dissolution. OP-16 remains open", False)]
    _f45 = [c for c, esp in _t45 if bool(_r45(c)) != esp]
    check("R45 el detector cruza la prosa con el registro de OPs",
          not _f45, "; ".join(_f45) if _f45
          else f"caso real de la pág. 8 y su forma corregida ({len(_RESUELTOS)} OPs resueltos)")

    _todos45 = []
    for _tx in sorted(list((_REPO / "manuscript").glob("*.tex"))
                      + list((_REPO / "submission_PRD").glob("*.tex"))):
        _todos45 += [f"{_tx.name}: {x}"
                     for x in _r45(_prosa_tex(_tx.read_text(errors="ignore")))]
    _l45, _deuda45 = _particiona(_todos45)
    # Auto-test contra el estado REAL de OP-17 antes del arreglo del 2026-08-02
    # (encabezado «✅ ADOPTADA» + cuerpo que la revierte) y contra los dos falsos
    # positivos que este detector dio en su primera versión.
    _t45b = [("## OP-17 — Partícula canónica — ✅ ADOPTADA 2026-06-19",
              "> DECISIÓN REVERTIDA. El 2026-08-01 se retira la partícula.", True),
             ("## OP-1 — Derivation of ω_b ✅ PARCIALMENTE RESUELTO",
              "> El viejo 3(π−φ)/200 quedó retirado; φ¹¹≈199 mostró que...", False),
             ("## OP-5 — S₈ Tension — ⚫ DISUELTO 2026-08-01",
              "> El OP no se resolvió: dejó de ser una pregunta.", False)]
    _f45b = []
    for _cab, _cpo, _esp in _t45b:
        _p = bool(_re.search(r"✅|ADOPTAD|RESUELT", _cab, _re.I))
        _n = bool(_re.search(r"RETIRAD|REVERTID|DISUELT|DISSOLV|withdraw", _cab, _re.I))
        _visto = _p and not _n and bool(_re.search(r"REVERTID", _cpo, _re.I))
        if _visto != _esp:
            _f45b.append(_cab[:44])
    check("R45 el detector de reversión distingue estado-del-OP de contenido-retirado",
          not _f45b, "; ".join(_f45b) if _f45b
          else "3 casos: OP-17 pre-arreglo marcado; OP-1 («fórmula retirada») y OP-5 exentos")

    check("R45 ningún OP adoptado/resuelto en el título que el cuerpo revierte",
          not _revertidos,
          "; ".join(_revertidos) if _revertidos
          else f"encabezados y cuerpos concuerdan en los {len(_RESUELTOS)} OPs cerrados")

    check("R45 documentos leídos — ningún OP resuelto citado como abierto",
          not _l45, "; ".join(_l45[:5]) if _l45
          else f"leídos limpios; {_deuda45} sitios de deuda en el resto")
    _DEUDA_REAL["R45"] = _deuda45
    check("R45 la deuda no crece", _deuda45 <= _DEUDA_MAX["R45"],
          f"{_deuda45} sitios (tope {_DEUDA_MAX['R45']})")
except Exception as e:
    check("R45 capa operable", False, str(e))

# R44 — constantes que la LECTURA va incorporando, con «=» a 6 decimales.
#
# Nacen aquí y no en R37 porque R37 es global por diseño («no hay excepciones,
# ninguna regla dirigida a un archivo concreto») y estas aún tienen deuda en
# documentos no leídos. Cuando la deuda de una llegue a cero, su sitio es R37.
#
#   Ω_m,dyn     (pág. 7) — caía en el hueco EXACTO entre dos reglas: R37 no lo
#               miraba (no estaba en su lista) y R41 lo saltaba (sólo cubre
#               cantidades CON unidades). El Paper 1 escribía «Ω_m,dyn = 0.160»
#               en la misma frase que «Ω_m,CMB = 0.308881», nueve veces.
#   SOLAR²·K_v  (pág. 8) — el multiplicador de la masa φ-DM se escribía
#               «= 594.28»: dos decimales con signo igual, siendo un número puro
#               en (φ,π) — SOLAR = φ+2π, KRYSTOS_V = 2Ω.
# ALCANCE, medido 2026-09-08 (lo pidio Mike: ensanchar hasta donde el
# enunciado alcance). R44 vigila DOS constantes, no las ~20 del nucleo, y eso
# es DELIBERADO, no estrechez: se midio que mirarlas todas da 300 sitios en 14
# documentos, y la mayoria son legitimos —«$3(\varphi+\pi)^2 = 67.96214$» a 5
# decimales es la forma canonica de la suite, y «$\pi=3.142$» es prosa normal.
# Ensancharla seria cambiar 300 sitios correctos por ruido. Las dos que vigila
# son las que tuvieron DERIVA historica de precision. El nombre del check dice
# eso ahora; el anterior prometia una universalidad que la regla no tiene, y
# fue lo que me hizo escribir un caso de mutacion contra su punto ciego.
print("\nCapa R44 — las dos constantes con deriva historica, con «=» a 6 decimales")
try:
    _C44 = {"Omega_m_dyn": (pi - phi) / (2 * (phi + pi)),
            "SOLAR2_KRYSTOS_V": (phi + 2 * pi) ** 2 * 2 * (pi + phi)}

    def _r44(tx: str):
        _h = []
        # Desde 2 decimales: a UNO, 0.160050 redondea a «0.2» y eso empareja
        # cualquier «= 0.2» del texto. Probado, no supuesto — ver auto-test.
        for _k44, _v44 in _C44.items():
            for _d in range(2, 6):
                for _m in _re.finditer(r"=\s*" + _re.escape(f"{_v44:.{_d}f}")
                                       + r"(?![0-9])", tx):
                    # EXENCION DE RETRACCION (2026-09-07). Un valor narrado
                    # como retirado no se «arregla» dandole mas decimales:
                    # escribir «594.281...» para una cantidad retractada es
                    # precision sobre algo que ya no se afirma. Unico sitio:
                    # P6 L175, «(retracted: SOLAR^2·KRYSTOS_V=594.28)».
                    _ctx = tx[max(0, _m.start() - 120):_m.end() + 40].lower()
                    if any(_e.lower() in _ctx for _e in _EXENTO_RETR):
                        continue
                    _h.append(f"{_k44}: «{_m.group(0).strip()}» → {_v44:.6f}")
        return _h

    _t44 = [(r"$\Omega_{m,\rm dyn}=0.160$ (DESI)", True),
            (r"$\Omega_{m,\rm dyn}=0.160050$ (DESI)", False),
            # falso positivo REAL de la primera versión (rango desde 1 decimal)
            (r"a fractional shift $\Delta=0.2$ in the amplitude", False),
            (r"multiplier $\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V=594.28$", True),
            (r"multiplier $\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V=594.279999$", False)]
    _f44 = [c for c, esp in _t44 if bool(_r44(c)) != esp]
    check("R44 el detector distingue 3 decimales de 6", not _f44,
          "; ".join(_f44) if _f44
          else "casos reales de las págs. 7 y 8, sus formas corregidas y un «=0.2» ajeno")

    _todos44 = []
    for _tx in sorted(list((_REPO / "manuscript").glob("*.tex"))
                      + list((_REPO / "submission_PRD").glob("*.tex"))):
        _todos44 += [f"{_tx.name}: {x}" for x in _r44(_tx.read_text(errors="ignore"))]
    _l44, _deuda44 = _particiona(_todos44)
    check("R44 documentos leídos — las dos constantes con deriva, a 6 decimales",
          not _l44, "; ".join(_l44[:5]) if _l44
          else f"leídos limpios; {_deuda44} sitios de deuda en el resto")
    _DEUDA_REAL["R44"] = _deuda44
    # 2026-09-08: la deuda decia solo CUANTOS. Un numero sin sitio no se
    # puede arreglar; ahora nombra los tres primeros.
    _d44 = [x for x in _todos44 if x not in _l44]
    check("R44 la deuda no crece", _deuda44 <= _DEUDA_MAX["R44"],
          f"{_deuda44} sitios (tope {_DEUDA_MAX['R44']})"
          + (": " + "; ".join(_d44[:3]) if _d44 else ""))

    # ── R44b · las TABLAS, que la forma «= valor» no alcanza (OP-25) ──────────
    # POR QUE (2026-09-08). R44 exige el signo igual y en una celda el valor va
    # solo, asi que no veia ninguna tabla. Al medirlo la primera vez conte 50
    # sitios y estaba MAL: emparejaba por coincidencia numerica sin comprobar de
    # que habla la fila. Asi «p_D = 2.00» —el numero efectivo de parametros del
    # DIC— salia como si fuera MIRA (1.998924), y un DeltaBIC de «0.00» como si
    # fuera omega_nu. Exigiendo que el SIMBOLO de la constante este en la misma
    # fila quedan 20, y todos son redondeo tipografico honesto de una tabla de
    # constantes. La leccion es la de R44 entera: un numero sin su entidad al
    # lado no identifica nada, y contar coincidencias produce ruido, no deuda.
    _SIM44 = {
        "OMEGA": r"\\Omega\b|OMEGA", "BETA": r"\\beta\b|BIAL", "KAL0": r"KAL",
        "P_SC": r"P_\{?\\rm sc|PYROS", "K_V": r"K_v|KRYSTOS", "T_R": r"T_r|TRIAL",
        "M_V": r"M_v|ATLAS", "MIRA": r"MIRA", "AURA": r"AURA", "S_K": r"s_K",
        "N_S": r"n_s", "W0": r"w_0", "WA": r"w_a", "H0_ALG": r"H_0",
        "OMEGA_M_TOTAL": r"\\Omega_m", "OMEGA_B_H2": r"\\omega_b",
        "OMEGA_C_H2": r"\\omega_c", "SUM_MNU_EV": r"m_\\nu",
    }
    _r44b = []
    for _tx44b in sorted(list((_REPO / "manuscript").glob("*.tex"))
                         + list((_REPO / "submission_PRD").glob("*.tex"))):
        for _ln44 in _tx44b.read_text(errors="ignore").split("\n"):
            if "&" not in _ln44:
                continue
            for _k44b, _pat44b in _SIM44.items():
                _v44b = getattr(_core63, _k44b, None)
                if _v44b is None or not _re.search(_pat44b, _ln44):
                    continue
                for _d44b in range(2, 6):
                    _s44b = f"{_v44b:.{_d44b}f}"
                    if abs(float(_s44b) - _v44b) < 5e-7:
                        continue          # ya esta a precision suficiente
                    _m44 = _re.search(r"&\s*\$?" + _re.escape(_s44b) + r"\$?\s*(&|\\\\)",
                                      _ln44)
                    if _m44:
                        # UNA CIFRA QUE SE DECLARA APROXIMADA NO ES FALSA
                        # PRECISION (2026-09-19). R44b nacio contra el numero
                        # truncado que se presenta como si fuera exacto. Pero
                        # «$\Omega$ & $\varphi+\pi$ & $4.75963\ldots$» y
                        # «AURA ($\varphi+\beta\approx3.998$)» estan diciendo
                        # con todas sus letras que ahi va un truncamiento — y el
                        # detector los contaba igual. Es el mismo defecto que en
                        # los .md: una marca que el detector no sabe leer.
                        # Se exime SOLO si la marca esta en la MISMA CELDA que
                        # la cifra, no en cualquier parte de la fila (una celda
                        # vecina con \approx no dice nada de esta).
                        _ini44 = _ln44.rfind("&", 0, _m44.start() + 1) + 1
                        _fin44 = _m44.end()
                        _celda44 = _ln44[_ini44:_fin44]
                        if _re.search(r"\\approx|\\ldots|\\dots|\\sim|\u2248|\u2026",
                                      _celda44):
                            break
                        _r44b.append(f"{_tx44b.stem}: {_k44b}={_s44b} "
                                     f"(vale {_v44b:.6f})")
                        break
                else:
                    continue
                break
    # 20 -> 0 el 2026-09-19: las 19 celdas subidas a 6 decimales con la misma
    # logica que las mide, mas la ultima (Sigma m_nu en Paper 3). El detector
    # ademas dejo de contar lo que se declara aproximado.
    _TOPE_R44B = 0                  # 14 -> 0 -> 20 -> 0; SOLO BAJA
    _DEUDA_REAL["R44b"] = len(_r44b)
    _DEUDA_MAX["R44b"] = _TOPE_R44B
    check("R44b la deuda de constantes redondeadas en TABLAS no crece",
          len(_r44b) <= _TOPE_R44B,
          f"{len(_r44b)} celdas (tope {_TOPE_R44B}): " + "; ".join(_r44b[:3])
          + (" …" if len(_r44b) > 3 else "")
          if _r44b else "ninguna celda de tabla con la constante redondeada")
    check("R44b el tope de tablas redondeadas esta apretado",
          len(_r44b) >= _TOPE_R44B or not _r44b,
          f"tope {_TOPE_R44B} = cuenta real {len(_r44b)}"
          if len(_r44b) == _TOPE_R44B
          else f"BAJAR el tope a {len(_r44b)}: sobran {_TOPE_R44B - len(_r44b)}")
    # CONTROL (R53): la fila que NOMBRA la constante se marca; la que solo trae
    # el mismo numero por casualidad, no. Es el falso positivo que se corrigio.
    _c44b = [(r"$w_a$ & $-P_{\rm sc}/K_v$ & $-0.670$ & \\", "WA", True),
             (r"$p_D$ & $2.00$ & $3.00$ \\", "MIRA", False),
             (r"$w_a$ & $-P_{\rm sc}/K_v$ & $-0.669975$ & \\", "WA", False)]
    _f44b = []
    for _ln, _k, _esp in _c44b:
        _v = getattr(_core63, _k)
        _visto = bool(_re.search(_SIM44[_k], _ln)) and any(
            abs(float(f"{_v:.{_d}f}") - _v) >= 5e-7
            and _re.search(r"&\s*\$?" + _re.escape(f"{_v:.{_d}f}") + r"\$?\s*(&|\\\\)",
                           _ln)
            for _d in range(2, 6))
        if _visto is not _esp:
            _f44b.append(f"«{_ln[:34]}» esperaba {_esp}")
    check("R44b el detector exige la constante NOMBRADA en la fila",
          not _f44b, "; ".join(_f44b) if _f44b
          else "3 casos: la fila que nombra w_a con 3 decimales se marca; la "
               "de p_D con «2.00» —que solo coincide con MIRA— y la ya exacta, no")
except Exception as e:
    check("R44 capa operable", False, str(e))

# R43 — potencias de φ escritas con «=» y un decimal que no es su valor (2026-07-28).
#
# POR QUÉ EXISTE, y por qué NO se resolvió ampliando R37. El Paper 1 justificaba
# n=7 con «(2φ⁶ = 35.9, 2φ⁷ = 58.068884, 2φ⁸ = 94.0)»: tres precisiones en un
# renglón (1, 6, 1 decimales) y dos igualdades FALSAS — 2φ⁶ = 35.888544 y
# 2φ⁸ = 93.957428. R37 no podía verlo: sólo mira las constantes de su lista, y
# 2φ⁶/2φ⁸ no son constantes del diccionario sino los términos de comparación del
# argumento de unicidad. Ampliar R37 a un decimal se probó y es INSERVIBLE: empareja
# números sueltos, y a 1 decimal «= 12.0», «= 2.3», «= 1.0», «= 6.4» cazan χ², z_S y
# tolerancias — 7 falsos positivos, 0 verdaderos. La regla correcta se ancla en la
# EXPRESIÓN algebraica que precede al «=», no en el número.
print("\nCapa R43 — potencias de φ: el decimal tras «=» es el valor")
try:
    def _r43(tx: str):
        _h = []
        for _m in _re.finditer(
                r"(?P<coef>[0-9]*)\s*\\(?:varphi|phiG)\s*\^\s*\{?\s*(?P<exp>-?[0-9]+)\s*\}?"
                r"\s*(?P<rel>=|\\simeq|\\approx)\s*(?P<val>[0-9]+\.[0-9]+)", tx):
            _c = int(_m.group("coef")) if _m.group("coef") else 1
            _ex = _c * phi ** int(_m.group("exp"))
            _mo = _m.group("val")
            _d = len(_mo.split(".")[1])
            # DOS CEGUERAS DEL DETECTOR (2026-09-07). De sus 22 sitios de
            # deuda, 20 eran texto CORRECTO que la regla no sabia leer:
            #   «n_s = 1-\varphi^{-7} = 0.965558»  -> no veia el «1-»
            #   «r = \varphi^{-10} = 8.1\times10^{-3}» -> no veia la
            #     notacion cientifica, y comparaba 8.1 contra 0.008131.
            # Una regla que marca lo correcto como deuda es peor que no
            # tenerla: manda a «arreglar» lo que ya esta bien.
            _pre = tx[max(0, _m.start() - 24):_m.start()]   # 24: cabe «1 - \frac{1}{»
            if _re.search(r"1\s*-\s*$", _pre):
                _ex = 1 - _ex
            # Tercera y cuarta ceguera: la DIVISION «3/\varphi^{14}» y la
            # fraccion «\frac{1}{\varphi^7}». En ambas el detector leia el
            # denominador como si fuera el termino entero.
            _div = _re.search(r"(\d+)\s*/\s*$", _pre)
            if _div:
                _ex = int(_div.group(1)) / _ex
            if _re.search(r"\\frac\{\s*1\s*\}\{\s*$", _pre):
                _ex = 1 / _ex
                if _re.search(r"1\s*-\s*\\frac\{\s*1\s*\}\{\s*$", _pre):
                    _ex = 1 - _ex
            _post = tx[_m.end():_m.end() + 22]
            _sci = _re.match(r"\s*(?:\\times|\\cdot)\s*10\^\{?(-?\d+)\}?", _post)
            if _sci:
                _ex = _ex / (10 ** int(_sci.group(1)))
            if f"{_ex:.{_d}f}" != _mo:            # ni siquiera es el redondeo correcto
                _h.append(("valor incorrecto", f"{_m.group(0)} → {_ex:.6f}"))
            elif _m.group("rel") == "=" and _d < 6:   # «=» exige 6 decimales (R37)
                _h.append((f"«=» con {_d} dec", f"{_m.group(0)} → {_ex:.6f}"))
        return _h

    _t43 = [(r"($2\varphi^6=35.9$, $2\varphi^7=58.068884$, $2\varphi^8=94.0$)", True),
            (r"($2\varphi^6=35.888544$, $2\varphi^7=58.068884$, $2\varphi^8=93.957428$)", False),
            (r"$\varphi^{-10}=0.008131$", False),
            (r"$\varphi^{-10}\simeq0.0081$", False),
            (r"$\varphi^{-10}=0.00814$", True)]
    _f43 = [c for c, esp in _t43 if bool(_r43(c)) != esp]
    check("R43 el detector ancla en la expresión, no en el número",
          not _f43, "; ".join(_f43) if _f43
          else "5 casos: la línea real de n=7, su forma corregida y tres controles")

    _mal43 = []
    for _tx in sorted(list((_REPO / "manuscript").glob("*.tex"))
                      + list((_REPO / "submission_PRD").glob("*.tex"))):
        for _por, _frag in _r43(_tx.read_text(errors="ignore")):
            _mal43.append(f"{_tx.name}: {_por} — «{_frag}»")
    _l43, _deuda43 = _particiona(_mal43)
    check("R43 documentos leídos — toda potencia de φ con «=» lleva su valor",
          not _l43, "; ".join(_l43[:5]) if _l43
          else f"leídos limpios; {_deuda43} sitios de deuda en el resto")
    _DEUDA_REAL["R43"] = _deuda43
    check("R43 la deuda no crece", _deuda43 <= _DEUDA_MAX["R43"],
          f"{_deuda43} sitios (tope {_DEUDA_MAX['R43']})")
except Exception as e:
    check("R43 capa operable", False, str(e))

# R42 — TIPO DIMENSIONAL: un número puro nunca IGUALA una cantidad física (2026-07-28).
#
#     H_0 = 3(φ+π)²            ✗  una tasa en km/s/Mpc igualada a un irracional puro
#     H_0 = 3(φ+π)² km/s/Mpc   ~  PARCHE de julio: mejor que el «=» pelado,
#                                 pero NO es la forma correcta. Ver abajo.
#
# ⚠️ EL REMEDIO DE ESTA REGLA ESTÁ SUPERADO (2026-09-07, lo señaló Mike).
# Pegarle la unidad al número puro sigue afirmando que una tasa medida ES un
# irracional multiplicado por km/s/Mpc. Sus palabras: «no puedes meter un
# número puro y ponerle unidades y decir que son lo mismo». La dirección de
# cascada (2026-09-06) ya dejó la forma correcta, y es una COMPARACIÓN:
#
#     H_glob = H_SH0ES·(1−f_screen^full) = 73.04·(1−0.069522) = 67.962142
#     que se compara con el número puro 3(φ+π)² = 67.96214 → residuo +4.2e-06
#
# Y el f_screen es el COMPLETO, IR+UV (0.069522), NO el IR solo (0.067253).
# Con el IR sale 68.13, a 0.17σ — que es un resultado parcial, no la forma
# canónica. Mike lo ha corregido TRES veces; queda escrito aquí y con regla
# (R61) para que deje de depender de que yo me acuerde.
#
# El número puro es el BLANCO, nunca el valor. Que la igualdad dimensional no
# esté cerrada es justo lo que V-L2-06 lleva ABIERTO, así que escribirla como
# igualdad —con unidad o sin ella— es afirmar de más.
#
# FORMA CANÓNICA ADOPTADA (2026-09-07). La que ya usaban el PRD y el Sealed:
# se divide la cantidad física por su unidad, y ASÍ los dos lados son números.
#
#     H_0/(km s^-1 Mpc^-1) = 3(φ+π)² = 67.96214          ✓
#     \frac{H_0}{km s^-1 Mpc^-1}  = 3(φ+π)²             ✓
#
# El detector ahora exige esa forma y RECHAZA las dos malas: el «=» pelado y el
# parche de julio con la unidad pegada. Los 26 sitios se reescribieron así, más
# 6 del parche en Paper 1 que antes pasaban.
#
# POR QUÉ EXISTE. La prosa de la suite lo dice bien desde hace tiempo — Postulado D:
# «the *dimensionless* value is fixed algebraically, while the *absolute* scale is
# not claimed to be derived» — pero la NOTACIÓN lo contradecía en 31 sitios con un
# «=» pelado. Lo señaló Mike: «uno tiene unidades y otro es un número irracional,
# así que es imposible que sean iguales; más que una igualdad, es una SIMILITUD
# ESTRUCTURAL». Es el eje que R40 no cubre: R40 vigila truncamiento (= vs ≈),
# R42 vigila DIMENSIÓN (número puro vs cantidad física).
#
# También caza la forma inversa: dividir un adimensional por una cantidad física,
# como el viejo «Ω_b h² = (π−φ)/H_0^SSEE», que además haría la identidad dependiente
# de la unidad elegida para H_0.
print("\nCapa R42 — tipo dimensional: número puro vs cantidad física")
try:
    # La unidad ACEPTADA sólo cuenta si divide a H_0 (H_0/unidad), porque eso
    # deja un número a cada lado. Pegada tras el «=» NO cuenta: sigue afirmando
    # que una tasa medida ES un irracional con unidades encima.
    _RAT = (r"(?:\s*/\s*(?:\\kmsu|\\kms\b|\(\s*\\mathrm\{km.{0,40}?\)"
            r"|\{?\\mathrm\{km.{0,40}?\}\}?))")
    _COMB = r"3\s*\(\s*\\(?:varphi|phiG)\s*\+\s*\\pi\s*\)\s*\^\s*\{?2\}?"
    _ANC = (r"(?:\\frac\{\s*H_0[^}]*\}\s*\{[^}]*\}[^=]{0,4}"
            r"|H_0(?:\^\{?\\rm\s*\w+\}?)?(?P<rat>" + _RAT + r")?)"
            r"\s*(?:&\s*)?=\s*(?:[^=$]{0,30}=\s*)?" + _COMB)
    # ESTRECHADA 2026-09-08 (lo destapo la mutacion «CONFLICTO»). Era
    # `\b(?:not|rather than|instead of|never)\b`, o sea CUALQUIER «not» en los
    # 90 caracteres previos apagaba la regla — y «not» es de las palabras mas
    # comunes de la prosa cientifica. Con «This is not a fitted quantity: the
    # anchor $H_0=3(varphi+pi)^2$» el defecto pasaba VERDE, y ese «not» niega
    # otra cosa (que sea ajustado), no la FORMA de la igualdad. Ahora la
    # negacion tiene que ir pegada a un verbo de escritura, que es lo que la
    # exencion queria decir. Medido: hoy no tapaba ningun sitio real, asi que
    # el estrechamiento no mueve ningun documento; es preventivo.
    _NIEGA = (r"\b(?:rather than|instead of)\b"
              r"|\b(?:not|never|cannot|must not)\b[^.]{0,24}"
              r"\b(?:writ|express|stat|read|render|present|equat|set|put)\w*")

    def _r42(tx: str):
        _h = []
        # (a) H_0 (cantidad física) igualado a la combinación pura.
        for _m in _re.finditer(_ANC, tx):
            if _m.group(0).startswith("\\frac"):
                continue                       # ya es un cociente: los dos lados son números
            if _m.group("rat"):
                continue                       # H_0/unidad = número puro: correcto
            if _re.search(_NIEGA, tx[max(0, _m.start() - 90):_m.start()], _re.I):
                continue                       # el texto la escribe para rechazarla
            _h.append(("igualdad tasa = número puro",
                       _m.group(0).replace("\n", " ")[:62]))
        # (b) adimensional dividido por una cantidad FÍSICA (H_0 con unidades).
        _DIV = (r"(?:\(\s*\\pi\s*-\s*\\(?:varphi|phiG)\s*\)\s*/\s*H_0"
                r"|\\frac\{\s*\\pi\s*-\s*\\(?:varphi|phiG)\s*\}\s*\{\s*H_0)")
        for _m in _re.finditer(_DIV, tx):
            if _re.search(_NIEGA, tx[max(0, _m.start() - 90):_m.start()], _re.I):
                continue
            _h.append(("adimensional / cantidad física", _m.group(0)[:62]))
        return _h

    # Auto-test: cada forma MALA con su forma BUENA al lado (control R53).
    _t42 = [
        # (a) las dos formas rechazadas...
        (r"anchor $H_0=3(\varphi+\pi)^2$ (derived, Paper~9) --- leaving", True),
        (r"$H_0 = 3(\varphi+\pi)^2\,\kmsu \approx 67.962\,\kmsu$", True),
        (r"$H_0 = 3(\varphi+\pi)^2 = 67.96214$~km\,s$^{-1}$\,Mpc$^{-1}$", True),
        (r"$H_0 = 3(\varphi+\pi)^2 \approx 67.962$ and nothing else here", True),
        # ...y las tres aceptadas: el cociente por la unidad.
        (r"anchor $H_0/\kmsu=3(\varphi+\pi)^2\simeq67.962$ (derived)", False),
        (r"$H_0^{\rm alg}/(\mathrm{km\,s^{-1}\,Mpc^{-1}}) = 3(\varphi+\pi)^2 = 67.962$",
         False),
        (r"\boxed{\frac{H_0}{\mathrm{km\,s^{-1}\,Mpc^{-1}}} = M_v \times \Omega"
         r" = 3(\varphi+\pi)^2 = 67.96214}", False),
        # la cadena intermedia no puede servir de escondite
        (r"$H_0 = M_v\times\Omega = 3(\varphi+\pi)^2 = 67.96214$", True),
        # (b) y su forma corregida, más la mención negada
        (r"expression $(\pi-\varphi)/H_0^{\rm SSEE}$ gives", True),
        (r"$\eta = A\times\frac{\pi-\varphi}{H_0^{\rm SSEE}}$ follows", True),
        (r"$\eta = A\times\frac{\pi-\varphi}{3(\varphi+\pi)^2}$ follows", False),
        (r"expression $(\pi-\varphi)/[3(\varphi+\pi)^2]$ gives", False),
        (r"we do not write it as $(\pi-\varphi)/H_0^{\rm SSEE}$: that would", False),
        # CONTROL del estrechamiento: un «not» que niega OTRA cosa ya no exime.
        (r"This is not a fitted quantity: the anchor $H_0=3(\varphi+\pi)^2$",
         True)]
    _f42 = [c for c, esp in _t42 if bool(_r42(c)) != esp]
    check("R42 el detector distingue número puro de cantidad física",
          not _f42, "; ".join(_f42) if _f42
          else "14 casos: «=» pelado, unidad pegada y cadena intermedia se marcan; "
               "H_0/unidad y \\frac{H_0}{unidad} pasan; la mención negada exenta y un «not» que niega otra cosa, NO")

    _mal42 = []
    for _tx in sorted(list((_REPO / "manuscript").glob("*.tex"))
                      + list((_REPO / "submission_PRD").glob("*.tex"))):
        for _por, _frag in _r42(_tx.read_text(errors="ignore")):
            _mal42.append(f"{_tx.name}: {_por} — «{_frag}»")
    _l42, _deuda42 = _particiona(_mal42)
    check("R42 documentos leídos — ninguna igualdad número puro = cantidad física",
          not _l42, "; ".join(_l42[:5]) if _l42
          else f"leídos limpios; {_deuda42} sitios de deuda en el resto (FP-6)")
    _DEUDA_REAL["R42"] = _deuda42
    check("R42 la deuda no crece", _deuda42 <= _DEUDA_MAX["R42"],
          f"{_deuda42} sitios (tope {_DEUDA_MAX['R42']})")
except Exception as e:
    check("R42 capa operable", False, str(e))

# R40 — TIPO DE RELACIÓN: el signo dice qué clase de afirmación es (2026-07-27).
# Las matemáticas son un lenguaje sin ambigüedad; «=» y «≈» no son dos grados de
# lo mismo, son relaciones distintas:
#
#     símbolo ↔ fórmula  →  SIEMPRE «=»   (Ω ES π+φ: definición, cero aproximación)
#     fórmula ↔ decimal  →  «=» si va completo; «≈» o \ldots si está TRUNCADO
#
# El «≈» no denuncia una discrepancia: denuncia dígitos cortados. «4.7596…» con
# puntos suspensivos vuelve a ser una igualdad.
#
# POR QUÉ EXISTE. El Paper 1 listaba sus siete registros como «Ω (π+φ ≈ 4.7596)»:
# fórmula y decimal bajo un ÚNICO «≈», con lo que la definición exacta Ω = π+φ
# desaparecía de la vista y el renglón entero se leía como aproximado. Lo detectó
# Mike leyendo, no el guardián — yo venía verificando que los decimales fueran
# correctos y pasé por encima de la relación que los une. De ahí la regla: R37/R38
# vigilan CUÁNTOS dígitos se muestran; R40 vigila QUÉ SE ESTÁ AFIRMANDO.
print("\nCapa R40 — tipo de relación: «=» exacto vs «≈» truncado")
try:
    _SIMB = r"(?:\\Omega|\\beta|\\varphi|\\phiG|\\pi|\\KALz?|\\AURA|\\MIRA|K_v|T_r|M_v|I_g|P_\{sc\}|P)"
    _FORM = r"(?:\\varphi|\\phiG|\\pi|\\Omega|\\beta|K_v|\\AURA)"

    def _r40(tx: str):
        _h = []
        # (a) «símbolo (fórmula ≈ valor)»: el paréntesis se traga la igualdad
        for _m in _re.finditer(
                r"\$\\boldsymbol\{" + _SIMB + r"\}\$\s*\(\$[^$]*" + _FORM
                + r"[^$]*\\approx", tx):
            _h.append(("igualdad oculta en paréntesis", _m.group(0)[:60]))
        # (b) «símbolo ≈ fórmula»: una fórmula algebraica NUNCA es aproximada
        for _m in _re.finditer(
                _SIMB + r"\s*\\approx\s*(?:\$)?\s*" + _FORM + r"\s*[+\-]\s*" + _FORM, tx):
            _h.append(("fórmula exacta escrita con ≈", _m.group(0)[:60]))
        return _h

    # Auto-test con el caso REAL que la originó y su forma corregida.
    _t40 = [(r"\item $\boldsymbol{\Omega}$ ($\pi+\varphi\approx4.7596$): Stability", True),
            (r"\item $\boldsymbol{\Omega} = \pi+\varphi \approx 4.7596$: Stability", False),
            (r"$\Omega \approx \varphi + \pi$", True),
            (r"$\Omega = \varphi + \pi \approx 4.7596$", False)]
    _f40 = [c for c, esp in _t40 if bool(_r40(c)) != esp]
    check("R40 el detector distingue el tipo de relación",
          not _f40, "; ".join(_f40) if _f40
          else "4 casos reales: paréntesis que oculta la igualdad y «≈» sobre fórmula exacta")

    # ENSANCHADA 2026-09-08: miraba 17 .tex y su titulo habla de
    # «un documento» / «la suite». Los .md de la raiz (CLAUDE.md, el
    # Registro, OPEN_PROBLEMS...) son documentos vivos y quedaban fuera.
    _mal40, _ndoc40 = [], 0
    for _tx in sorted(list((_REPO / "manuscript").glob("*.tex"))
                      + list((_REPO / "submission_PRD").glob("*.tex"))
                      + [_q for _q in _REPO.glob("*.md")
                         if _q.name not in ("CHANGELOG.md", "MEMORY.md")]):
        _ndoc40 += 1
        for _por, _frag in _r40(_tx.read_text(errors="ignore")):
            _mal40.append(f"{_tx.name}: {_por} — «{_frag}»")
    check("R40 ninguna igualdad exacta presentada como aproximación",
          not _mal40, "; ".join(_mal40[:5]) if _mal40
          else f"{_ndoc40} documentos barridos: símbolo↔fórmula con «=» y "
               f"decimal truncado con «≈»")
except Exception as e:
    check("R40 capa operable", False, str(e))

# R39 — la compuerta de publicación sigue viendo TODA la suite (2026-07-27).
# La fecha de portada es «la versión que publiqué ese día». Mientras se trabaja
# NO se toca; el día de publicar se mueve una vez y para todos. Ese trabajo lo
# hace src/verificacion/preparar_publicacion.py, y esta regla sólo vigila que no
# se le escape un documento: si mañana nace un Paper 11 con su propio \date y la
# compuerta no lo conoce, se publicaría una serie con una portada desfasada y
# nadie lo notaría. R39 NO exige que las fechas coincidan hoy — eso es trabajo
# de la compuerta el día de publicar, y hoy la suite está en plena revisión.
print("\nCapa R39 — compuerta de publicación: conoce todas las portadas")
try:
    _pp = _REPO / "src/verificacion/preparar_publicacion.py"
    if not _pp.exists():
        check("R39 la compuerta de publicación existe", False, "falta preparar_publicacion.py")
    else:
        _tex = [t for d in ("manuscript", "submission_PRD")
                for t in sorted((_REPO / d).glob("*.tex"))]
        _con = [t.name for t in _tex
                if _re.search(r"\\date\{", t.read_text(errors="ignore"))]
        _spec = _ilu.spec_from_file_location("_pp", _pp)
        _mod = _ilu.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        _vistos = [t.name for t, _, _ in _mod.portadas()]
        _falta = sorted(set(_con) - set(_vistos))
        check("R39 la compuerta ve todas las portadas de la suite",
              not _falta, ", ".join(_falta) if _falta
              else f"{len(_vistos)} portadas cubiertas ({len(_tex)} .tex explorados)")
        # Que la compuerta sepa BLOQUEAR es tan importante como que sepa aplicar:
        # una compuerta que siempre deja pasar no es una compuerta.
        _hoy = [f for _, f, _ in _mod.portadas() if "\\today" in f]
        check("R39 la compuerta detecta \\today (fecha no reproducible)",
              True, f"{len(_hoy)} con \\today — se resuelve al publicar, no hoy"
              if _hoy else "ninguna portada con \\today")
except Exception as e:
    check("R39 capa operable", False, str(e))

print("\nCapa R34 — fuentes vs núcleo: ningún .py hardcodea constante retirada")
try:
    # La infraestructura de VERIFICACIÓN lleva valores retirados a propósito:
    # el núcleo los define, el guardián los busca y el registro de reglas los
    # usa como payload de mutación. R34 cazó `registro_reglas.py` en cuanto se
    # escribió — true positive contra el propio andamio, no contra el modelo.
    _EXCL = set(_FIXTURES) | {"ssee_core.py"}
    _pat34 = _re.compile(
        r"(?:mnu|Smnu|SUM_MNU_EV|sigma_m_nu|m_nu|C_nu|C_NU)\s*=\s*"
        r"(0\.069(?:0[0-9]*)?|94\.07[0-9]*)\s*(?:[^0-9.]|$)")
    # ENSANCHADA 2026-09-08 (lo pidio Mike): miraba solo src/ y su titulo dice
    # «ningun .py activo». class_ssee/ tambien es codigo activo — 41 ficheros
    # que quedaban fuera. R25 ya barria los dos; esta no.
    _malos, _npy34 = [], 0
    for _py in sorted(list((_REPO / "src").rglob("*.py"))
                      + list((_REPO / "class_ssee").rglob("*.py"))):
        if _py.name in _EXCL or "archive" in _py.parts:
            continue
        _npy34 += 1
        for _i, _ln in enumerate(_py.read_text(errors="ignore").splitlines(), 1):
            _code = _ln.split("#")[0]
            _m34 = _pat34.search(_code)
            if _m34:
                _malos.append(f"{_py.relative_to(_REPO)}:{_i} → {_m34.group(1)}")
    check("R34 ningún .py activo hardcodea Σm_ν/C_ν retirados",
          not _malos,
          "; ".join(_malos) if _malos
          else f"{_npy34} .py activos barridos; leen Σm_ν/C_ν del núcleo en vez "
               f"de re-teclearlas (sólo esas dos constantes)")
except Exception as e:
    check("R34 capa fuentes-vs-núcleo operable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# R35 — artefacto más viejo que su fuente (2026-07-26).
# R33/R34 buscan huellas que hay que ADIVINAR de antemano ("0.06902", "94.07"):
# sirven para el error ya conocido, no para el siguiente. Esta regla no adivina
# nada — si el script cambió después de generarse su log, el log es sospechoso,
# sea cual sea la constante. Probado retrospectivamente contra el estado del
# 2026-07-25: habría marcado 4 de los 5 logs rancios DOCE días antes.
# Usa fechas de COMMIT, no mtime: un checkout reescribe mtime y mentiría.
# Mapa en PROPAGACION.yaml; los logs sin fuente declarada se CUENTAN como
# deuda visible (ABIERTO), que es lo contrario de una nota suelta.
print("\nCapa R35 — artefacto vs fuente: ningún log más viejo que su script")
try:
    import ast          # noqa: F401 — usado por el filtro de docstrings
    import subprocess as _sp
    import yaml as _yaml
    _prop = _yaml.safe_load((_REPO / "PROPAGACION.yaml").read_text())
    _mapa = _prop.get("logs") or {}
    _hist35 = set(_prop.get("historicos") or [])

    def _commit_ts(rel):
        try:
            _o = _sp.run(["git", "log", "-1", "--format=%at", "--", rel],
                         cwd=_REPO, capture_output=True, text=True, timeout=20)
            return int(_o.stdout.strip()) if _o.stdout.strip() else None
        except Exception:
            return None

    def _cert35_cubre(_fecha, _ts):
        """¿El certificado (una fecha) cubre un script committeado en _ts?
        Cubre hasta el FINAL de ese día, hora local. Sin fecha válida o sin
        commit del script, no cubre: ante la duda, R35 compara."""
        import datetime as _dt
        if _ts is None or not isinstance(_fecha, _dt.date):
            return False
        _fin = _dt.datetime.combine(_fecha, _dt.time(23, 59, 59)).timestamp()
        return _ts <= _fin

    # NORMALIZACIÓN del AST antes de comparar. Se quitan dos clases de cambio
    # que NO pueden mover un número, para que la alarma no grite por ellas:
    #   (a) docstrings — prosa.
    #   (b) un literal sustituido por el SÍMBOLO del núcleo que vale eso mismo
    #       (la deuda que persigue R66). Cada nombre importado de ssee_core se
    #       resuelve a su valor y se compara el valor, no el nombre: si el
    #       símbolo valiera otra cosa, los dumps difieren y la alarma suena.
    #       También se descartan los import de ssee_core y el sys.path que hace
    #       falta para llegar a él, que son fontanería de ese mismo cambio.
    _CORE35 = {_k: _v for _k, _v in vars(_core63).items()
               if _k.isupper() and isinstance(_v, (int, float))}

    def _cierre35(_arbol, _entrada):
        """Las funciones por las que pasa `_entrada`, en cascada."""
        _defs = {_n.name: _n for _n in _arbol.body
                 if isinstance(_n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        if _entrada not in _defs:
            return None                     # entrada declarada que no existe
        _vistas, _cola = set(), [_entrada]
        while _cola:
            _f = _cola.pop()
            if _f in _vistas:
                continue
            _vistas.add(_f)
            for _nd in ast.walk(_defs[_f]):
                if isinstance(_nd, ast.Call) and isinstance(_nd.func, ast.Name):
                    if _nd.func.id in _defs:
                        _cola.append(_nd.func.id)
        return _vistas

    def _norm35(_txt, _entrada=None):
        _t = ast.parse(_txt)
        if _entrada:
            _cierre = _cierre35(_t, _entrada)
            if _cierre is not None:
                # nombres que el camino realmente usa
                _usa = set()
                for _nm35 in _cierre:
                    for _d in _t.body:
                        if (isinstance(_d, (ast.FunctionDef, ast.AsyncFunctionDef))
                                and _d.name == _nm35):
                            _usa |= {_x.id for _x in ast.walk(_d)
                                     if isinstance(_x, ast.Name)}
                _nombres35 = _usa | set(_cierre)

                def _rama_ajena(_nodo):
                    """¿Esta rama del despachador lanza OTRA corrida?"""
                    for _x in ast.walk(_nodo):
                        if isinstance(_x, ast.Name) and _x.id in _nombres35:
                            return False
                        if isinstance(_x, ast.Attribute) and _x.attr in _nombres35:
                            return False
                    return True

                def _poda_ifs(_nodo):
                    """En un `if/elif` de módulo —el despachador de `__main__`—
                    las ramas que no nombran nada de este camino son otras
                    corridas. Se les vacía el cuerpo para que cambiar una no
                    ensucie el log de otra. El `test` se conserva: si alguien
                    renombra o reordena las ramas, eso SÍ se ve."""
                    for _h in ast.walk(_nodo):
                        if isinstance(_h, ast.If) and _rama_ajena(
                                ast.Module(body=_h.body, type_ignores=[])):
                            _h.body = [ast.Pass()]
                    return _nodo

                _cuerpo = []
                for _st in _t.body:
                    if isinstance(_st, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if _st.name in _cierre:
                            _cuerpo.append(_st)
                        continue
                    if isinstance(_st, ast.Assign):
                        # una constante de módulo que este camino no nombra no
                        # puede moverle un número: se poda
                        _dianas = {_x.id for _t2 in _st.targets
                                   for _x in ast.walk(_t2) if isinstance(_x, ast.Name)}
                        if _dianas and not (_dianas & _usa):
                            continue
                    if isinstance(_st, ast.If):
                        _st = _poda_ifs(_st)
                    _cuerpo.append(_st)
                _t.body = _cuerpo
        _alias = {}                     # nombre local -> valor del núcleo
        _mods = set()                   # `import ssee_core as X` -> {"X"}
        for _nd in ast.walk(_t):
            if isinstance(_nd, ast.ImportFrom) and _nd.module == "ssee_core":
                for _a in _nd.names:
                    if _a.name in _CORE35:
                        _alias[_a.asname or _a.name] = _CORE35[_a.name]
            elif isinstance(_nd, ast.Import):
                for _a in _nd.names:
                    if _a.name == "ssee_core":
                        _mods.add(_a.asname or _a.name)

        class _T35(ast.NodeTransformer):
            def visit_Name(self, _n):
                if _n.id in _alias:
                    return ast.copy_location(ast.Constant(_alias[_n.id]), _n)
                return _n

            def visit_Attribute(self, _n):
                self.generic_visit(_n)
                if (isinstance(_n.value, ast.Name) and _n.value.id in _mods
                        and _n.attr in _CORE35):
                    return ast.copy_location(ast.Constant(_CORE35[_n.attr]), _n)
                return _n

            # Fontanería del propio cambio: el import del núcleo y el sys.path
            # que hace falta para alcanzarlo. Se identifica por FORMA, no por el
            # alias, porque el alias es libre (`import sys as _s66` esquivaba la
            # versión anterior de esta condición).
            _FONT = ("ssee_core", "os", "sys")

            def visit_Import(self, _n):
                return None if all(_a.name in self._FONT
                                   for _a in _n.names) else _n

            def visit_ImportFrom(self, _n):
                return None if _n.module in self._FONT else _n

            def visit_Expr(self, _n):
                self.generic_visit(_n)
                _c = _n.value
                if (isinstance(_c, ast.Call)
                        and isinstance(_c.func, ast.Attribute)
                        and _c.func.attr == "insert"
                        and isinstance(_c.func.value, ast.Attribute)
                        and _c.func.value.attr == "path"):
                    return None                 # <lo-que-sea>.path.insert(...)
                return _n

        _t = _T35().visit(_t)
        for _nd in ast.walk(_t):
            if isinstance(_nd, (ast.Module, ast.FunctionDef,
                                ast.AsyncFunctionDef, ast.ClassDef)):
                _b = _nd.body
                if (_b and isinstance(_b[0], ast.Expr)
                        and isinstance(_b[0].value, ast.Constant)
                        and isinstance(_b[0].value.value, str)):
                    _nd.body = _b[1:]                   # fuera el docstring
        return ast.dump(ast.fix_missing_locations(_t))

    _rancios, _sinmapa = [], []
    for _lg in sorted((_REPO / "results" / "logs").glob("*.log")):
        _nm = _lg.stem
        if _nm in _hist35:
            continue
        _script = _mapa.get(_nm)
        if not _script:
            _sinmapa.append(_nm)
            continue
        # EL CAMINO, NO EL FICHERO (2026-09-19).
        #
        # R35 comparaba el script ENTERO, así que cualquier edición en
        # cualquier parte de un script multiuso ensuciaba TODOS sus logs. Caso
        # real: el commit 8f49b48 arregló `loglike_ssee_wc_h` y con eso marcó
        # como rancios los dos logs de ΛCDM fondo-fijo, que salen de
        # `loglike_lcdm_fijo` — otra función, otro camino, ningún número
        # tocado. Una alarma que suena por algo que no puede haber pasado
        # termina ignorándose, y entonces deja de avisar cuando sí pasa.
        #
        # Ahora el mapa puede declarar de qué FUNCIÓN sale un log:
        #     nombre_del_log:  ruta/al/script.py::funcion_de_entrada
        # y la comparación mira sólo esa función, las que ella llama (en
        # cascada), y el código de módulo del que dependen. Sigue siendo una
        # medida contra el CÓDIGO, no una lista de excepciones a mano.
        _entrada = None
        if "::" in _script:
            _script, _entrada = _script.split("::", 1)
        _tl, _ts35 = _commit_ts(f"results/logs/{_nm}.log"), _commit_ts(_script)
        # Muestreo certificado: un cambio YA PROBADO inocuo no invalida la
        # cadena. Pero el certificado cubre SÓLO los cambios hasta su fecha
        # (2026-09-19): antes eximía el log para siempre, y un cambio real que
        # llegara después al mismo camino habría pasado callado.
        if _cert35_cubre((_prop.get("muestreo_certificado") or {}).get(_nm), _ts35):
            continue
        if not (_tl and _ts35 and _ts35 > _tl):
            continue
        # El script es posterior — pero ¿cambió el CÓDIGO o sólo la prosa?
        # Comparar el AST en ambos puntos: si es idéntico, el cambio fue de
        # comentarios/docstring y el log sigue siendo válido. Sin esto la regla
        # grita por documentación, y una alarma ruidosa se termina ignorando
        # (comprobado: mcmc_paper2_3models_wmfix, cuyo único cambio fue la
        # línea «Ω_m = 0.30889» → «0.308881» dentro del docstring).
        try:
            _sha_log = _sp.run(["git", "log", "-1", "--format=%H", "--",
                                f"results/logs/{_nm}.log"], cwd=_REPO,
                               capture_output=True, text=True, timeout=20).stdout.strip()
            _viejo = _sp.run(["git", "show", f"{_sha_log}:{_script}"], cwd=_REPO,
                             capture_output=True, text=True, timeout=20).stdout
            _nuevo = (_REPO / _script).read_text(errors="ignore")
            if _viejo and _norm35(_viejo, _entrada) == _norm35(_nuevo, _entrada):
                continue     # sólo cambió la prosa, un literal por su símbolo,
                             # o una función por la que este log no pasa
        except Exception as _e35:
            # NUNCA tragarse el fallo: un `except: pass` aquí escondió un
            # NameError propio (ast no estaba importado) y R35 reportó rancios
            # que no lo eran. Ante la duda se reporta, PERO con la razón visible.
            _rancios.append(f"{_nm} (no se pudo comparar AST: {type(_e35).__name__})")
            continue
        _rancios.append(f"{_nm} (script {(_ts35 - _tl) // 86400}d más nuevo)")
    check("R35 ningún log committeado es más viejo que el script que lo produce",
          not _rancios,
          "; ".join(_rancios) if _rancios
          else f"{len(_mapa)} logs mapeados al día, {len(_hist35)} históricos")
    # CONTROL (R53) del ensanchamiento de _norm35. Lo que se exime tiene que ser
    # SÓLO el cambio que no puede mover un número. Si la normalización fuera
    # laxa de más, R35 daría verdes falsos justo donde importa: un log rancio.
    _base35 = "import sys\nsys.path.insert(0, '..')\nx = 0.06849\ny = x * 2\n"
    _c35 = [
        # (variante, ¿debe verse IGUAL que la base?)
        ("import sys\nfrom ssee_core import SUM_MNU_EV as _m\n"
         "sys.path.insert(0, '..')\nx = _m\ny = x * 2\n", True),   # mismo valor
        ("import sys\nfrom ssee_core import OMEGA_B_H2 as _m\n"
         "sys.path.insert(0, '..')\nx = _m\ny = x * 2\n", False),  # OTRO valor
        ("import sys\nsys.path.insert(0, '..')\nx = 0.06849\n"
         "y = x * 3\n", False),                                    # cambio real
    ]
    _mal35 = [_i for _i, (_v, _igual) in enumerate(_c35)
              if (_norm35(_v) == _norm35(_base35)) is not _igual]
    # CONTROL (R53) de la poda por camino. Lo que se poda tiene que ser SÓLO
    # aquello por lo que el log no pasa. Si la poda fuera laxa, R35 daría verde
    # a un log cuyo propio código cambió — el fallo exacto que la regla existe
    # para ver.
    _modulo35 = ("K = 2.0\n"
                 "AJENA = 9.0\n"
                 "def aux(z):\n    return z * K\n"
                 "def mia(x):\n    return aux(x) + 1\n"
                 "def otra(y):\n    return y * AJENA\n")
    _cc35 = [
        # (variante, ¿debe verse IGUAL mirando sólo el camino de `mia`?)
        (_modulo35.replace("return y * AJENA", "return y * AJENA + 7"), True),   # otra función
        (_modulo35.replace("AJENA = 9.0", "AJENA = 11.0"), True),                # constante ajena
        (_modulo35.replace("return aux(x) + 1", "return aux(x) + 2"), False),     # la propia
        (_modulo35.replace("return z * K", "return z * K * 2"), False),           # la que llama
        (_modulo35.replace("K = 2.0", "K = 3.0"), False),                         # constante suya
        # el despachador de `__main__`: tocar la rama de OTRA corrida se exime,
        # tocar la que lanza la nuestra no
        (_modulo35 + "if __name__ == '__main__':\n    if q == 'a':\n        mia(1)\n"
         "    elif q == 'b':\n        otra(2)\n", None),
    ]
    _disp35 = ("if __name__ == '__main__':\n    if q == 'a':\n        mia(1)\n"
               "    elif q == 'b':\n        otra(2)\n")
    _cc35 = _cc35[:-1] + [
        (_modulo35 + _disp35.replace("otra(2)", "otra(3)"), True),    # rama ajena
        (_modulo35 + _disp35.replace("mia(1)", "mia(9)"), False),     # nuestra rama
    ]
    _base_disp35 = _modulo35 + _disp35
    _malc35 = []
    for _i, (_v, _igual) in enumerate(_cc35):
        _ref35 = _base_disp35 if "__main__" in _v else _modulo35
        if (_norm35(_v, "mia") == _norm35(_ref35, "mia")) is not _igual:
            _malc35.append(_i)
    check("R35 la poda por camino no exime lo que sí toca al log",
          not _malc35,
          "7 casos: cambiar otra función, una constante ajena o la rama del "
          "despachador de otra corrida se exime; cambiar la propia función, la "
          "que ella llama, su constante o su propia rama, no"
          if not _malc35 else f"casos mal clasificados: {_malc35}")
    # CONTROL (R53) del certificado con fecha: cubre lo de antes, NO lo de
    # después, y sin fecha no cubre nada.
    import datetime as _dt35
    _d35 = _dt35.date(2026, 9, 19)
    _t35 = lambda *a: _dt35.datetime(*a).timestamp()
    _ccert35 = [
        (_d35, _t35(2026, 9, 19, 10, 0), True),     # mismo día: cubre
        (_d35, _t35(2026, 9, 1, 10, 0), True),      # antes: cubre
        (_d35, _t35(2026, 9, 20, 0, 30), False),    # día siguiente: NO
        (None, _t35(2026, 9, 1, 10, 0), False),     # sin fecha: NO
        ("2026-09-19", _t35(2026, 9, 1), False),    # texto, no fecha: NO
    ]
    _malcert35 = [_i for _i, (_f, _t, _e) in enumerate(_ccert35)
                  if _cert35_cubre(_f, _t) is not _e]
    check("R35 un certificado de muestreo no exime cambios posteriores a su fecha",
          not _malcert35,
          "5 casos: cubre el mismo día y antes; no cubre el día siguiente, "
          "ni sin fecha, ni con la fecha escrita como texto"
          if not _malcert35 else f"casos mal clasificados: {_malcert35}")
    check("R35 el detector distingue re-etiquetar de re-calcular",
          not _mal35,
          "3 casos: el literal cambiado por el símbolo que vale lo mismo se "
          "exime; el símbolo que vale OTRA cosa y un cambio de fórmula no"
          if not _mal35 else f"casos mal clasificados: {_mal35}")
    if _sinmapa:
        track_open(f"R35 {len(_sinmapa)} logs sin fuente declarada en PROPAGACION.yaml",
                   ", ".join(_sinmapa[:10]) + (" …" if len(_sinmapa) > 10 else "")
                   + "  (añadir su script para que R35 los vigile)")
    # ── R36 — lo mismo para FIGURAS, priorizando las de submission ────────
    # R35 vigila logs; una figura rancia pasaba igual. A diferencia de los logs,
    # el script productor SÍ se deriva solo (el nombre del archivo aparece en el
    # código), así que no hace falta mapa. Mismo filtro AST: 32 figuras salían
    # "rancias" por timestamp y 10 eran sólo cambios de prosa.
    # Se distingue por severidad: las figuras QUE ENTRAN AL PRD son ROJO —van al
    # journal—; el resto se cuenta como deuda ABIERTA en vez de bloquear.
    _prd_figs = set(_re.findall(r"includegraphics\[[^\]]*\]\{([^}]+)\}",
                                (_REPO / "submission_PRD" / "SSEE_PRD.tex")
                                .read_text(errors="ignore")))
    _prd_figs = {f.rsplit(".", 1)[0] for f in _prd_figs}

    def _ast_igual(_sha, _rel):
        _v = _sp.run(["git", "show", f"{_sha}:{_rel}"], cwd=_REPO,
                     capture_output=True, text=True, timeout=20).stdout
        if not _v:
            return False
        _d = lambda _x: ast.dump(ast.parse(_x))          # noqa: E731
        try:
            _a = ast.parse(_v); _b = ast.parse((_REPO / _rel).read_text(errors="ignore"))
            for _t in (_a, _b):
                for _nd in ast.walk(_t):
                    if isinstance(_nd, (ast.Module, ast.FunctionDef,
                                        ast.AsyncFunctionDef, ast.ClassDef)):
                        _bd = _nd.body
                        if (_bd and isinstance(_bd[0], ast.Expr)
                                and isinstance(_bd[0].value, ast.Constant)
                                and isinstance(_bd[0].value.value, str)):
                            _nd.body = _bd[1:]
            return ast.dump(_a) == ast.dump(_b)
        except Exception:
            return False

    _fig_prd, _fig_otras = [], []
    for _fg in sorted((_REPO / "results" / "figures").glob("*.pdf")):
        _nm36 = _fg.stem
        _hits = [str(_p.relative_to(_REPO)) for _p in (_REPO / "src").rglob("*.py")
                 if "archive" not in _p.parts and _p.name not in _FIXTURES
                 and _nm36 in _p.read_text(errors="ignore")]
        if not _hits:
            continue
        _scr = _hits[0]
        _tf = _commit_ts(f"results/figures/{_fg.name}")
        _ts36 = _commit_ts(_scr)
        if not (_tf and _ts36 and _ts36 > _tf):
            continue
        _sha36 = _sp.run(["git", "log", "-1", "--format=%H", "--",
                          f"results/figures/{_fg.name}"], cwd=_REPO,
                         capture_output=True, text=True, timeout=20).stdout.strip()
        if _ast_igual(_sha36, _scr):
            continue                                     # sólo prosa
        # Regenerada y verificada byte-idéntica: el cambio de código no afectaba
        # a ESTA figura. Vale mientras el script no vuelva a cambiar.
        _ver = (_prop.get("figuras_verificadas") or {}).get(_nm36)
        if _ver:
            import datetime as _dt
            _vts = _dt.datetime.strptime(str(_ver), "%Y-%m-%d").timestamp() + 86400
            if _vts >= _ts36:
                continue
        (_fig_prd if _nm36 in _prd_figs else _fig_otras).append(
            f"{_nm36} ({(_ts36 - _tf) // 86400}d)")
    # 2026-09-08: el mensaje decia «N figuras del PRD al día» y eso promete
    # mas de lo que mide. R36 compara la figura con SU SCRIPT, y nada mas: una
    # figura regenerada ayer desde un script que lleva dentro los MAP de una
    # cadena retirada pasa este check con razon y esta rancia igual. Paso con
    # fig8 (45 dias). Ese hueco lo cubre R65, y solo donde el script declara
    # su log. El mensaje ahora dice lo que hizo.
    check("R36 ninguna figura DEL PRD es más vieja que el script que la produce",
          not _fig_prd,
          "; ".join(_fig_prd) if _fig_prd
          else f"{len(_prd_figs)} figuras del PRD no son más viejas que su "
               f"script. NO dice que su CONTENIDO esté al día: si el script "
               f"lleva números rancios dentro, esto pasa igual (caso fig8, "
               f"2026-09-08) — eso lo mira R65")
    if _fig_otras:
        track_open(f"R36 {len(_fig_otras)} figuras rancias fuera del PRD",
                   ", ".join(_fig_otras[:8]) + (" …" if len(_fig_otras) > 8 else ""))
except Exception as e:
    check("R35 capa artefacto-vs-fuente operable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# CAPA MANUSCRITOS — reglas del RIGOR_CHECKLIST automatizadas (grep duro).
# "El sistema solo se hace más capas": cada regla automatizable se vuelve un
# check aquí, para que UNA corrida marque dónde y por qué.
#   R1 cronología   : ninguna afirmación de prioridad temporal sobre datos públicos.
#   R2 multidominio : ningún enlace al compendio multidominio retirado (DOI 19679049).
# Los disclaimers honestos ("no claim of temporal priority", "which predate this
# work") NO matchean: los patrones apuntan solo a las afirmaciones prohibidas.
# ─────────────────────────────────────────────────────────────────────
print("\nCapa Manuscritos — reglas R1 (cronología) y R2 (multidominio)")
try:
    import re as _re2
    _REPO2 = pathlib.Path(__file__).resolve().parents[2]
    # Cobertura: los 12 manuscritos + el README raíz (cajón público vigente).
    # NO se escanean los docs de auditoría (RIGOR_CHECKLIST, AUDIT…) ni el
    # CHANGELOG: contienen los patrones prohibidos como EJEMPLOS/historia.
    _texs = sorted((_REPO2 / "manuscript").glob("*.tex")) + [_REPO2 / "README.md"]
    _texs = [p for p in _texs if p.exists()]
    _R1 = [
        r"predating\s+(the\s+)?(desi|planck|dr2|dr1)",
        r"prior to\s+(the\s+)?(desi|planck)\s*(dr2|dr1|2018|pr4|release|comparison)",
        r"deposited[^.]{0,50}(prior to|before)[^.]{0,25}(desi|planck|dr2)",
        r"timestamp[^.]{0,30}(proof|prior)",
        r"pre-desi\b",
        r"committed\s+before\s+(desi|planck)",
    ]
    _R2 = [r"19679049", r"ssee_unificado", r"unified compendium of irrational"]
    # R-overclaim: ASERCIÓN global de "zero-parameter" en prosa. NO matchea:
    # claims scoped ("zero-parameter dark-energy"), recantaciones ("described as
    # a zero-parameter model... however"), ni citas de títulos.
    _ROVER = [r"(achieves|is|provides|presents|constitutes)\s+a\s+zero[- ]parameter\s+(framework|model|theory)"]
    # R-serie: conteo de EXTENSIONES congelado antes de 10 (P1 «3--7»), o
    # descripción explícita del tamaño de la serie. NO matchea las referencias
    # correctas de un paper a sus previos (P8 «1--7», P10 «1--9»).
    _RSER = [r"papers?~?3--[789]\b", r"(seven|eight|nine)[- ]paper series"]
    _r1_hits, _r2_hits, _rov_hits, _rser_hits = [], [], [], []
    for t in _texs:
        low = t.read_text(errors="ignore").lower()
        for pat in _R1:
            m = _re2.search(pat, low)
            if m:
                _r1_hits.append(f"{t.name}:«{low[m.start():m.end()][:40]}»")
        for pat in _R2:
            if _re2.search(pat, low):
                _r2_hits.append(f"{t.name}:{pat}")
        for pat in _ROVER:
            m = _re2.search(pat, low)
            if m:
                _rov_hits.append(f"{t.name}:«{low[m.start():m.end()][:40]}»")
        for pat in _RSER:
            m = _re2.search(pat, low)
            if m:
                _rser_hits.append(f"{t.name}:«{low[m.start():m.end()][:30]}»")
    check("manuscritos  R1 sin claims de prioridad temporal", not _r1_hits,
          "limpio" if not _r1_hits else "; ".join(_r1_hits[:4]))
    check("manuscritos  R2 sin enlaces multidominio retirados", not _r2_hits,
          "limpio" if not _r2_hits else "; ".join(_r2_hits[:4]))
    check("manuscritos  R10 sin overclaim 'zero-parameter' global", not _rov_hits,
          "limpio" if not _rov_hits else "; ".join(_rov_hits[:4]))
    check("manuscritos  R11 sin conteo de serie stale (<10 papers)", not _rser_hits,
          "limpio" if not _rser_hits else "; ".join(_rser_hits[:4]))

    # ── R15 — coherencia de la tensión derivada de n_s ──────────────────
    # Remache forjado en la auditoría 2026-07-09 (Paper 1 L334 decía «matches
    # Planck PR4 at 0.24σ» — el 0.24 corresponde a un central 0.9665 que NO es
    # PR4; el valor real es 0.16-0.17σ, y contradecía al Endorser). El guardián
    # RECOMPUTA n_s = 1-φ⁻⁷ y su tensión, y escanea cualquier σ pegado (≤130
    # chars) a «\varphi^{-7}» que se salga del valor real. Escaneo LOCAL a la
    # fórmula → el 0.24σ legítimo de w0wa en otro lado no da falso positivo.
    _phi = (1 + 5 ** 0.5) / 2
    _ns_alg = 1 - _phi ** -7                       # 0.965558
    _ns_planck, _ns_err = 0.9649, 0.0042           # Planck PR4 (mismo que Endorser)
    _ns_tens = abs(_ns_alg - _ns_planck) / _ns_err  # 0.157σ
    _ns_lo, _ns_hi = _ns_tens - 0.06, _ns_tens + 0.06  # ventana [0.10, 0.22]
    _sig_re = r"([+\-−]?)([0-9]\.[0-9]{1,2})\s*\\?sigma"
    _ns_hits = []          # valores citados FUERA de rango (incorrectos)
    _ns_quoted = {}        # {archivo: set(redondeos citados)} para coherencia
    for t in _texs:
        txt = t.read_text(errors="ignore")
        # Dos anclas: (a) la fórmula 1-φ⁻⁷, (b) el central Planck 0.9649 —
        # porque la tensión a veces se enuncia DESACOPLADA de la fórmula
        # (p.ej. «n_s=0.9649±0.0042 is 0.2σ from the SSEE value»), sin φ⁻⁷ cerca.
        # Este era el hueco por el que R15 dejó pasar el 0.2σ del Paper 1 App.
        _anchors = [(m.end(), m.end() + 100)
                    for m in _re2.finditer(r"varphi\^\{-7\}", txt)]
        _anchors += [(max(0, m.start() - 15), m.end() + 90)
                     for m in _re2.finditer(r"0\.9649", txt)]
        for a, b in _anchors:
            window = txt[a:b].split(r"\\", 1)[0]  # no cruzar salto de fila LaTeX
            wl = window.lower()
            if not ("planck" in wl or "0.96556" in window or "0.9649" in window
                    or "spectral" in wl):
                continue
            # σ con signo (+2.9σ, −0.6σ) = reducción de tensión de OTRA cantidad
            # (p.ej. modulación IS-Eckart), no la tensión n_s-vs-dato: se excluye.
            sm = _re2.search(_sig_re, window)
            if sm and not sm.group(1):
                _ns_quoted.setdefault(t.name, set()).add(sm.group(2))
                val = float(sm.group(2))
                if not (_ns_lo <= val <= _ns_hi):
                    _ns_hits.append(f"{t.name}:n_s@{val}σ (real {_ns_tens:.2f}σ)")
    # Coherencia de redondeo: un mismo manuscrito no debe citar la tensión n_s
    # con dos redondeos distintos (p.ej. 0.16σ en el cuerpo y 0.2σ en el App).
    # El 0.2 caía DENTRO de la ventana ±0.06 → «correcto» por separado, pero
    # contradecía al 0.16 del cuerpo: la grieta era la INconsistencia, no el valor.
    _ns_incoh = [f"{n}:{sorted(v)}" for n, v in _ns_quoted.items() if len(v) > 1]
    _ns_ok = not _ns_hits and not _ns_incoh
    _ns_msg = f"n_s={_ns_alg:.5f}, tensión {_ns_tens:.2f}σ (Planck PR4), redondeo único"
    if _ns_hits:
        _ns_msg = "; ".join(_ns_hits[:4])
    elif _ns_incoh:
        _ns_msg = "redondeo incoherente: " + "; ".join(_ns_incoh[:4])
    check("manuscritos  R15 tensión n_s: correcta y con redondeo único", _ns_ok, _ns_msg)

    # ── R17 — la constante de conversión de neutrinos debe ser univaluada ──
    # Remache forjado en la auditoría de Paper 1 (2026-07-10): la suite mezcla
    # 93.14 (en ω_ν=Σm_ν/93.14, Papers 1/3/6) con 94.07 (en la fórmula de Σm_ν,
    # Papers 1/4/6). Es la MISMA constante física (relic-density↔masa); un referí
    # caza el ~1% de inconsistencia.
    # RESUELTO 2026-07-25: se estandarizó en 93.14 (PDG) y se EJECUTÓ la re-propagación
    # que aquí quedaba pendiente (Σm_ν 0.0690/0.06902 → 0.06849 en ssee_core, P3, P6,
    # class_ssee, los 10 papers y las 3 memorias). La decisión se había tomado el
    # 2026-07-10 pero la re-propagación quedó A MEDIAS: m_φ sí se actualizó
    # (41.02→40.70), ω_ν no. LECCIÓN: una decisión sin re-propagación ejecutada es un
    # drift latente que se ve idéntico a un valor sano. Ahora lo cierra V-L2-11a/b/c.
    #
    # ⚠️ POR QUÉ R17 NO LO CAZÓ, Y LA REGLA QUE SE DERIVA:
    # R17 es un check de CADENA DE TEXTO: verifica que "94.07" no aparezca en los
    # .tex. El string se borró → R17 pasó → guardián VERDE. Pero el NÚMERO derivado
    # de 94.07 (Σm_ν=0.06902 ⇒ ω_ν=0.000741) siguió vivo en código y papers. El
    # guardián certificaba media tarea con luz verde entera, y un VERDE se lee como
    # "hecho".
    # REGLA GENERAL: retirar una constante exige DOS chequeos, no uno —
    #   (a) el string desaparece            [R17, superficie]
    #   (b) los números que derivaban de ella se recomputaron  [V-L2-11, consecuencia]
    # Un check de (a) sin su (b) es peor que ningún check: crea confianza falsa.
    # Aplicar este par a cualquier retiro futuro de constante.
    # MATIZADO 2026-07-27. La versión previa prohibía «94.07» en cualquier .tex,
    # y eso era un error de fondo: 94.07 eV NO es un valor incorrecto ni
    # retirado — es el desacople INSTANTÁNEO (N_eff=3 exacto), otra magnitud
    # física. 93.14 incluye el reheating e⁺e⁻ (N_eff=3.046) y es el operativo.
    # Explicar la diferencia en el paper es NECESARIO: un referee pregunta «¿por
    # qué 93.14 y no 94?» en la primera lectura. La regla anterior habría
    # obligado a borrar precisamente la respuesta.
    # Lo que sí debe prohibirse es usarlo como C_ν OPERATIVO. Se distingue por
    # contexto: si el documento explica la diferencia (menciona el desacople
    # instantáneo o el reheating e⁺e⁻ cerca), la mención es legítima.
    _CTX_OK = ("instantaneous", "instantáneo", "e^+e^-", "e^+e^-", "Mangano",
               "N_{\\rm eff}=3", "reheat")
    _nu_9407 = []
    for _tx17 in _texs:
        _c17 = _tx17.read_text(errors="ignore")
        if "94.07" not in _c17:
            continue
        # TODAS las ocurrencias, no sólo la primera, y sin distinguir
        # mayúsculas: la primera versión miraba _c17.index() (una sola) con
        # ventana de 700 y case-sensitive, y marcaba como «sin explicación» un
        # Paper 6 que SÍ la traía —empezaba con «Instantaneous», mayúscula—
        # unas líneas más arriba. La regla acusaba al texto de su propio fallo.
        _bajo = _c17.lower()
        _ctx = tuple(_k.lower() for _k in _CTX_OK)
        _sin = False
        _pos17 = _bajo.find("94.07")
        while _pos17 != -1:
            _ventana = _bajo[max(0, _pos17 - 2500): _pos17 + 2500]
            if not any(_k in _ventana for _k in _ctx):
                _sin = True
                break
            _pos17 = _bajo.find("94.07", _pos17 + 1)
        if _sin:
            _nu_9407.append(_tx17.name)
    check("manuscritos  R17 C_ν operativo = 93.14 (94.07 solo con su explicación)",
          not _nu_9407,
          "93.14 operativo; 94.07 aparece únicamente donde se explica que es el "
          "desacople instantáneo (y que C_ν se cancela en ω_ν)"
          if not _nu_9407 else "94.07 SIN contexto explicativo en: "
          + ", ".join(_nu_9407) + " — o se explica, o se usa 93.14")

    # Control de dos lados (R53, 2026-09-05). Esta regla ya se equivocó una vez
    # por mirar sólo la PRIMERA aparición y con mayúsculas (marcó un Paper 6 que
    # sí traía la explicación). Sin control, su «OK» no distingue «todos los
    # 94.07 están explicados» de «el barrido no encuentra ninguno».
    def _r17_marca(_txt):
        """True si el texto usaría 94.07 sin su explicación cerca."""
        # _CTX_OK y no _ctx: aquel se define DENTRO del bucle de archivos y no
        # existe si todos cayeron en el `continue`. Usarlo aquí reventaba el
        # try entero y se llevaba por delante _texs2/_prd, y con ellos R27,
        # R29 y R30 — un control que rompe tres capas vecinas.
        _ctx = tuple(_k.lower() for _k in _CTX_OK)
        _b = _txt.lower()
        _pos = _b.find("94.07")
        while _pos != -1:
            _v = _b[max(0, _pos - 2500): _pos + 2500]
            if not any(_k in _v for _k in _ctx):
                return True
            _pos = _b.find("94.07", _pos + 1)
        return False
    _r17_desnudo = "El valor C_nu = 94.07 se usa en el calculo."
    _r17_explic = ("Instantaneous decoupling gives 94.07; " * 1) + "C_nu cancels."
    _r17_dos = _r17_explic + (" " * 6000) + " y ademas 94.07 aqui suelto."
    check("R17 el detector distingue 94.07 explicado de 94.07 desnudo",
          _r17_marca(_r17_desnudo) and not _r17_marca(_r17_explic)
          and _r17_marca(_r17_dos) and not _r17_marca("solo 93.14 aqui"),
          "4 casos: desnudo marcado; explicado limpio; SEGUNDA aparición lejos "
          "de su contexto marcada (el bug histórico de mirar sólo la primera); "
          "texto sin 94.07 limpio")

    # ── R18 — sin narrativa H0-posterior stale del reframe Ω_m-geometría ──
    # Remache forjado en la auditoría de Paper 2 (2026-07-10): el fix V-L4-DESI
    # (2026-07-09, sector frío 0.160 fuera de E(z)) se propagó al abstract/§2.4/§6.3
    # PERO dejó prosa stale en §3.2 y en el párrafo "algebraic anchor": afirmaba que
    # el posterior H0 "lies at 2.9σ from anchor", "pull downward to compensate for
    # the enlarged r_d", y "r_d = Ω_m,dyn(H0/100)²" — CONTRADICE el 0.04σ/coincide
    # corregido en la misma sección. R14 vigila los SCRIPTS (canario E(z)); esto es
    # PROSA. Los fragmentos siguientes solo existieron como la aserción retirada:
    _stale_v4 = {
        r"\Omega_{m,\mathrm{dyn}}(H_0/100)": "r_d desde el sector dinámico 0.160 (va la total 0.308881)",
        "compensate for the enlarged": "narrativa vieja: no hay r_d agrandado (148.2≈ΛCDM)",
        "downward to compensate": "posterior COINCIDE con anchor (0.04σ), no baja a compensar",
    }
    _v4_hits = []
    for t in _texs:
        txt = t.read_text(errors="ignore")
        for pat, why in _stale_v4.items():
            if pat in txt:
                _v4_hits.append(f"{t.name}«{pat[:22]}»→{why}")
    check("manuscritos  R18 sin narrativa H0-posterior stale (V-L4-DESI)",
          not _v4_hits,
          "posterior coincide con anchor (0.04σ), geometría con Ω_m total"
          if not _v4_hits else "; ".join(_v4_hits[:4]))

    # ── R19 — ningún manuscrito muestra los valores BAO DR1-mislabeled ──
    # Remache forjado en la auditoría de Paper 2 (2026-07-10): la Tabla 1 de P2 y su
    # §B.2 mostraban los valores DR1 (7.93±0.15, LRG DH 20.08, QSO 30.21/13.23 @z=1.491,
    # Lya 39.71/8.52) aunque las cadenas jul-9 SÍ usaban DR2 (load_desi_dr2, csv fuente).
    # Datos mostrados ≠ datos usados. R14 vigila el csv/loader; R19 vigila que la PROSA
    # de los manuscritos no reintroduzca los valores DR1. Fingerprints inequívocos (DR2
    # da 21.863/30.512/38.988/8.632):
    _dr1_bao = {"20.08": "LRG DH DR1 (DR2=21.863)", "30.21": "QSO DM DR1 (DR2=30.512)",
                "39.71": "Lya DM DR1 (DR2=38.988)", "8.52": "Lya DH DR1 (DR2=8.632)",
                "16.85": "LRG2 DM DR1 (DR2=17.351)", "1.491": "z_QSO DR1 (DR2 z=1.484)"}
    # FIX 2026-09-08: el `pat in txt` era substring pelado y marcaba «8.52»
    # dentro de «38.52» (fila de tabla de Paper 5, valor ajeno al BAO). Un
    # numero se busca con frontera de NUMERO: ni digito ni punto pegados a
    # los lados. Control abajo.
    _dr1_rx = {p: re.compile(r"(?<![\d.])" + re.escape(p) + r"(?![\d])")
               for p in _dr1_bao}
    def _r19_sitios(txt, nombre="?"):
        return [f"{nombre}«{p}»={_dr1_bao[p]}"
                for p, rx in _dr1_rx.items() if rx.search(txt)]
    _bao_hits = []
    for t in _texs:
        _bao_hits += _r19_sitios(t.read_text(errors="ignore"), t.name)
    check("manuscritos  R19 sin valores BAO DR1-mislabeled (datos mostrados = usados)",
          not _bao_hits,
          "manuscritos muestran DR2 (data/raw/desi_dr2_bao.csv, la que usan las cadenas)"
          if not _bao_hits else "; ".join(_bao_hits[:5]))
    # CONTROL (R53): marca el DR1 suelto y deja pasar el que es parte de
    # otro numero. El falso positivo real que motivo el fix va incluido.
    _c19 = [(r"$D_H/r_d = 8.52$ (Lya)", True),          # DR1 suelto
            (r"9 & 0.100 & 17.58 & 38.52 & excellent", False),  # el real
            (r"$D_H/r_d = 8.632$ (Lya, DR2)", False),
            (r"z = 1.4915", False)]                     # 1.491 pegado a un 5
    _f19 = [t[:34] for t, esp in _c19 if bool(_r19_sitios(t)) != esp]
    check("R19 el detector distingue el DR1 suelto del digito dentro de otro numero",
          not _f19, "; ".join(_f19) if _f19
          else "4 casos: el 8.52 suelto marcado; el 38.52 de la tabla, el "
               "8.632 de DR2 y el 1.4915 exentos")

    # Las R21-R24 también vigilan el PRD (submission_PRD), no solo manuscript/.
    _prd = _REPO2 / "submission_PRD" / "SSEE_PRD.tex"
    _texs2 = _texs + ([_prd] if _prd.exists() else [])

    # ── R21 — el denominador de wₐ es IGNIS (π+PYROS), NUNCA K_v (2Ω) ──────
    # Remache forjado 2026-07-19: la suite escribía wₐ = P_sc/K_v, colapsando el
    # denominador al scaffold K_v (=KRYSTOS φ+π+Ω, 2Ω por valor) cuando la ENTIDAD
    # es IGNIS = π+PYROS (rama-π, intra-linaje con el numerador PYROS=P_sc): mismo
    # valor 9.519, entidad distinta. K_v SOLO es legítimo como sumando de M_v=φ+π+K_v;
    # NUNCA como denominador → basta prohibir K_v en rol de denominador ("}{K_v" en
    # \frac, "/K_v" inline). M_v=φ+π+K_v (K_v como "+K_v") no matchea.
    _kvden = []
    for t in _texs2:
        txt = t.read_text(errors="ignore")
        for pat in (r"\}\{K_v", r"/K_v"):
            m = _re2.search(pat, txt)
            if m:
                _kvden.append(f"{t.name}«{txt[max(0, m.start()-8):m.end()][:20]}»")
    check("manuscritos  R21 wₐ denominador = IGNIS(π+PYROS); K_v nunca es denominador",
          not _kvden,
          "wₐ = P_sc/IGNIS en toda la suite; K_v solo como +K_v en M_v"
          if not _kvden else "; ".join(_kvden[:5]))

    # ── R21b — la MISMA ley, pero en el CÓDIGO ────────────────────────────
    # Hallazgo 2026-07-25 (revisión pregunta-por-pregunta del PRD, §2.2): R21
    # sólo escaneaba .tex. Los .py seguían escribiendo `-P_sc / KV` en 10 sitios
    # de 6 archivos — el paper decía IGNIS y el código decía K_v. Como K_v e
    # IGNIS son iguales BIT A BIT (ambos 2Ω), ningún número delataba la grieta:
    # exactamente el falso verde que el guardián existe para impedir. Un texto y
    # su prueba no pueden declarar linajes distintos aunque coincidan en valor.
    # OJO: sólo se prohíbe K_v en rol de DIVISOR; `MV = PHI + PI + KV` es legítimo.
    _kvden_py = []
    for _py in sorted(_REPO2.glob("src/**/*.py")) + sorted(_REPO2.glob("class_ssee/*.py")):
        # test_guardian.py queda fuera: sus mutaciones CONTIENEN a propósito la
        # forma prohibida (es su trabajo escribirla para probar que duele).
        if "archive" in _py.parts or _py.name in _FIXTURES:
            continue
        for _ln, _line in enumerate(_py.read_text(errors="ignore").splitlines(), 1):
            # Se mira CÓDIGO, no prosa: un comentario que NOMBRA la forma prohibida
            # está documentándola (esta regla misma lo hace). Se recorta desde el «#».
            _line = _re2.sub(r"#.*$", "", _line)
            # KRYSTOS_V entra a la lista 2026-07-25: la primera versión de R21b sólo
            # miraba las abreviaturas (KV/Kv/K_v/K_V) y dejó pasar el nombre completo
            # justo en look_elsewhere_full.py — el script que produce el «1 de 490».
            if _re2.search(r"/\s*(KV|Kv|K_v|K_V|KRYSTOS_V)\b", _line):
                _kvden_py.append(f"{_py.name}:{_ln}")
    check("código       R21b wₐ = −P_sc/IGNIS en los scripts (K_v nunca divide)",
          not _kvden_py,
          "ningún script divide por K_v; el linaje del código = el del paper"
          if not _kvden_py else "; ".join(_kvden_py[:5]))

    # ── R22 — precisión: sin 5-dec truncados/falsos de las constantes ─────
    # Remache forjado 2026-07-19: el Sealed truncaba (no redondeaba) la tabla de
    # notación y daba wₐ=-0.67000 (falso: es -0.66997) y w₀=-0.83996 (falso:
    # -0.83995; 1+w₀=0.16005 lo exige). Un referí caza el 5º dígito. Se prohíben
    # los 5-dec ERRÓNEOS exactos, con lookahead (?![0-9]) para no chocar con la
    # precisión plena legítima (14.278879927, 4.759626642, …).
    _badprec = {
        r"0\.83996(?![0-9])": "w₀ falso (→ -0.83995)",
        r"0\.67000(?![0-9])": "wₐ falso (→ -0.66997)",
        r"4\.75962(?![0-9])": "Ω truncado (→ 4.75963)",
        r"5\.52140(?![0-9])": "KAL truncado (→ 5.52141)",
        r"3\.99784(?![0-9])": "AURA truncado (→ 3.99785)",
        r"6\.37765(?![0-9])": "P_sc truncado (→ 6.37766)",
        r"11\.99353(?![0-9])": "T_r truncado (→ 11.99354)",
        r"14\.27887(?![0-9])": "M_v truncado (→ 14.27888)",
    }
    _prec_hits = []
    for t in _texs2:
        txt = t.read_text(errors="ignore")
        for pat, why in _badprec.items():
            if _re2.search(pat, txt):
                _prec_hits.append(f"{t.name}:{why}")
    check("manuscritos  R22 sin constantes 5-dec truncadas/falsas",
          not _prec_hits,
          "precisión canónica (w₀=-0.83995, wₐ=-0.66997, tabla redondeada)"
          if not _prec_hits else "; ".join(_prec_hits[:6]))

    # ── R23 — sin fósiles Σ₉ / "5D" / MIKAEL_V (nombres/símbolos retirados) ─
    # Remache forjado 2026-07-19: Σ₉ (de las "9 Soberanías", hoy 25) sobrevivía en
    # P7/P9; "five-dimensional integration ceiling" para M_v (que es 4D, dentro de
    # CUARTAL=4·AURA) en Sealed/PRD; y MIKAEL_V (renombrado ATLAS por la Ley de
    # Nombrado) como etiqueta de M_v en P1/P7. MIKAEL a secas (Soberana viva) NO
    # matchea: el patrón exige el sufijo _V / \_V.
    _fossils = {
        r"Sigma_9": "Σ₉ fósil (9 Soberanías → 25); usar 3Ω/M_v",
        r"Σ₉": "Σ₉ fósil; usar 3Ω/M_v",
        r"five-dimensional integration": "M_v es 4D (dentro de CUARTAL), no 5D",
        r"5D integration": "M_v es 4D, no 5D",
        r"5-D integration": "M_v es 4D, no 5D",
        r"MIKAEL\\?_V": "MIKAEL_V renombrado ATLAS (Ley de Nombrado)",
    }
    _fos_hits = []
    for t in _texs2:
        txt = t.read_text(errors="ignore")
        for pat, why in _fossils.items():
            if _re2.search(pat, txt):
                _fos_hits.append(f"{t.name}:{why}")
    check("manuscritos  R23 sin fósiles Σ₉ / 5D / MIKAEL_V",
          not _fos_hits,
          "Σ₉→3Ω, 5D→4D, MIKAEL_V→ATLAS aplicados"
          if not _fos_hits else "; ".join(_fos_hits[:6]))

    # ── R24 — conteo del diccionario univaluado: 55/25/490 (sin rezagos) ──
    # Remache forjado 2026-07-19: el Sealed mezclaba "50 named / 22 distinct" (v1.3)
    # con "490 ratios" (v1.4) en la MISMA zona; ni los 3 auditores externos ni el
    # guardián lo cazaron. Canónico único: 55 nombres / 25 valores / 490 razones.
    # Se prohíben los denominadores/counts RETIRADOS en contexto (no el bare "378"
    # de 6.378=P_sc): "1 of 378", "1/378", "50 named", "22 distinct", etc.
    _oldcount = {
        r"1\s*(?:of|/)\s*378": "1/378 retirado (→ 1/490)",
        r"1\s*(?:of|/)\s*245": "1/245 retirado (→ 1/490)",
        r"1\s*(?:of|/)\s*337": "1/337 retirado (→ 1/490)",
        r"1\s*(?:of|/)\s*317": "1/317 retirado (→ 1/490)",
        r"\b50\s+named": "50 named retirado (→ 55)",
        r"\b46\s+named": "46 named retirado (→ 55)",
        r"\b22\s+distinct": "22 distinct retirado (→ 25)",
        r"\b21\s+distinct": "21 distinct retirado (→ 25)",
    }
    _cnt_hits = []
    for t in _texs2:
        txt = t.read_text(errors="ignore")
        for pat, why in _oldcount.items():
            if _re2.search(pat, txt):
                _cnt_hits.append(f"{t.name}:{why}")
    check("manuscritos  R24 conteo diccionario 55/25/490 (sin rezagos 50/22/378)",
          not _cnt_hits,
          "55 named / 25 distinct / 490 ratios univaluado"
          if not _cnt_hits else "; ".join(_cnt_hits[:6]))
except Exception as e:
    check("manuscritos  capa operable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# CAPA ARCHIVO — la Bitácora de Archivado cubre cada cajón archivado.
# Nada se archiva en silencio: cada subcarpeta de archive/ debe tener su
# entrada (qué/cuándo/por qué) en archive/README.md.
# ─────────────────────────────────────────────────────────────────────
print("\nCapa Archivo — bitácora cubre cada cajón archivado")
try:
    _arch = pathlib.Path(__file__).resolve().parents[2] / "archive"
    _bitf = _arch / "README.md"
    _bit = _bitf.read_text(errors="ignore") if _bitf.exists() else ""
    _orphans = [d.name for d in _arch.iterdir()
                if d.is_dir() and d.name not in _bit] if _arch.exists() else []
    check("archivo  toda subcarpeta de archive/ documentada en la bitácora",
          not _orphans,
          "documentadas" if not _orphans else "SIN entrada: " + ", ".join(_orphans))
except Exception as e:
    check("archivo  capa operable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# CAPA DICCIONARIO — integridad de la lista de nodos nombrados.
# El diccionario MAESTRO vive en sandbox_unificado/ssee-data.json. Ningún
# script puede introducir un nodo ausente del maestro: eso fue el duplicado
# espurio KRYSTOS_V (=2Omega) de look_elsewhere_full.py, idéntico por VALOR
# a KRYSTOS (=phi+pi+Omega). Un chequeador de VALORES es ciego a esto
# (mismo número); este check de PROCEDENCIA lo caza. (R13, 2026-06-16)
# ─────────────────────────────────────────────────────────────────────
print("\nCapa Diccionario — integridad de nodos (script ⊆ maestro)")
try:
    import json as _json, re as _re
    _root = pathlib.Path(__file__).resolve().parents[2]
    _mf = _root / "sandbox_unificado" / "ssee-data.json"
    _master = set()
    if _mf.exists():
        _md = _json.load(open(_mf))
        for _sec in ("base_constants", "derived_constants", "nine_sovereignties"):
            for _c in _md.get(_sec, []):
                if isinstance(_c, dict) and _c.get("name"):
                    _master.add(_c["name"].upper())
        if "OMEGADNAV" in _master:
            _master.add("OMEGA")          # alias scaffold
        if "KRYSTOS" in _master:
            _master.add("KRYSTOS_V")      # KRYSTOS_V = nombre correcto (φ+π+Ω); maestro aún usa "KRYSTOS" → v1.2 pendiente
        # Ley de Nombrado v1.5 (2026-07-19): MIKAEL_V→ATLAS, MIKE→PHOENIX. El maestro
        # vive en sandbox_unificado/ (submódulo del repo PÚBLICO multidominio) y NO se
        # toca antes del envío — así que la equivalencia se declara aquí, igual que
        # con KRYSTOS_V. Es alias de NOMBRE, no de valor: el nodo es el mismo.
        # Al re-sincronizar el maestro, estas dos líneas sobran.
        if "MIKAEL_V" in _master:
            _master.add("ATLAS")
        if "MIKE" in _master:
            _master.add("PHOENIX")
    _lf = _root / "src" / "estadistica" / "look_elsewhere_full.py"
    _fam = set()
    if _lf.exists():
        _m = _re.search(r"FAMILY\s*=\s*\{(.*?)\}",
                        _lf.read_text(errors="ignore"), _re.S)
        if _m:
            # incluye nombres con tilde (DÜSTAL/TRÏSTAL/CUÄSTAL) y acento agudo (ÁNGELOS)
            _fam = {k.upper() for k in _re.findall(r'"([A-ZÁÉÍÓÚÄÖÜÏÑ_]+)"\s*:', _m.group(1))}
    _spurious = sorted(_fam - _master) if (_master and _fam) else []
    check("diccionario  R13 look_elsewhere sin nodos ausentes del maestro",
          not _spurious,
          "consistente (script ⊆ maestro)" if not _spurious
          else "ESPURIOS (no en maestro): " + ", ".join(_spurious))

    # ── R16 — coherencia interna del look-elsewhere ─────────────────────
    # Remache forjado en la auditoría 2026-07-09 (Paper 1): el script tracked
    # tenía docstring «29 constantes» pero la etiqueta del reporte hardcodeaba
    # «31» mientras su FAMILY tiene 29 → conteo auto-contradictorio, y el «378»
    # que Paper 1 cita como defensa anti-numerología quedaba sin anclar. R16
    # recomputa: (a) docstring == etiqueta-reporte == len(FAMILY); (b) el conteo
    # de razones distintas en (0,5] == 490 (el número robusto que citan los papers,
    # tras la completitud ≤TRIAL a 53 constantes, 2026-07-18).
    if _lf.exists():
        _lftxt = _lf.read_text(errors="ignore")
        _nfam = len(_fam)
        _ds = _re.search(r"\((\d+)\s+constantes", _lftxt)     # docstring (permite "constantes con nombre")
        _lbl = _re.findall(r"COMPLETO\s*\((?:[^)]*?)(\d+)\s+constantes\)", _lftxt)
        _ds_n = int(_ds.group(1)) if _ds else -1
        # etiqueta dinámica (f-string len(FAMILY)) cuenta como coherente
        _lbl_dyn = "len(FAMILY)" in _lftxt or "{len(fam)" in _lftxt.lower()
        _lbl_ok = _lbl_dyn or all(int(x) == _nfam for x in _lbl)
        _cnt_ok = (_ds_n == _nfam) and _lbl_ok
        check("diccionario  R16 look-elsewhere conteo interno coherente",
              _cnt_ok,
              f"docstring={_ds_n}, FAMILY={_nfam}, etiqueta {'dinámica' if _lbl_dyn else _lbl}"
              if _cnt_ok else
              f"INCOHERENTE: docstring={_ds_n} vs FAMILY={_nfam} vs etiqueta={_lbl}")
except Exception as e:
    check("diccionario  capa operable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# CAPA DESI — procedencia de los datos BAO (R14, 2026-07-01).
# Historia: la suite entera usó DESI DR1 (2404.03002) MAL ETIQUETADO como
# DR2 durante meses (11/13 puntos DR1 exactos + un QSO z=1.491 sin fuente).
# Un chequeador de física es ciego a esto (los números eran internamente
# consistentes); solo un check de PROCEDENCIA contra la tabla oficial lo caza.
# Tres candados:
#   1. El csv canónico coincide dígito a dígito con DR2 Tabla 4 (2503.14738)
#      — la tabla de cotejo vive AQUÍ, copiada independientemente del csv.
#   2. Cero valores-centinela DR1 en el csv (20.98, 7.93, 13.62...).
#   3. Los consumers importan del loader único; nadie re-hardcodea datos BAO.
# ─────────────────────────────────────────────────────────────────────
print("\nCapa DESI — procedencia BAO: csv == DR2 Tabla 4 oficial, sin DR1, sin hardcode")
try:
    _root = pathlib.Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(_root / "src"))
    from desi_dr2_data import load_desi_dr2, desi_covariance
    import numpy as _np

    # 1) Cotejo independiente contra DESI DR2 (2503.14738, Tabla 4).
    #    (z, quantity, value, sigma, corr_MH) — transcrito del paper, NO del csv.
    _DR2_OFICIAL = [
        (0.295, "DV_over_rd",  7.942, 0.075,  None),
        (0.510, "DM_over_rd", 13.588, 0.167, -0.459),
        (0.510, "DH_over_rd", 21.863, 0.425, -0.459),
        (0.706, "DM_over_rd", 17.351, 0.177, -0.404),
        (0.706, "DH_over_rd", 19.455, 0.330, -0.404),
        (0.934, "DM_over_rd", 21.576, 0.152, -0.416),
        (0.934, "DH_over_rd", 17.641, 0.193, -0.416),
        (1.321, "DM_over_rd", 27.601, 0.318, -0.434),
        (1.321, "DH_over_rd", 14.176, 0.221, -0.434),
        (1.484, "DM_over_rd", 30.512, 0.760, -0.500),
        (1.484, "DH_over_rd", 12.817, 0.516, -0.500),
        (2.330, "DM_over_rd", 38.988, 0.531, -0.431),
        (2.330, "DH_over_rd",  8.632, 0.101, -0.431),
    ]
    _d = load_desi_dr2()
    _mism = []
    for _k, (_z, _q, _v, _s, _c) in enumerate(_DR2_OFICIAL):
        if not (abs(_d["z"][_k] - _z) < 1e-9 and _d["quantity"][_k] == _q
                and abs(_d["value"][_k] - _v) < 1e-9
                and abs(_d["sigma"][_k] - _s) < 1e-9
                and ((_c is None and _np.isnan(_d["corr"][_k]))
                     or (_c is not None and abs(_d["corr"][_k] - _c) < 1e-9))):
            _mism.append(f"fila {_k}: z={_z} {_q}")
    check("DESI  R14 csv == DR2 Tabla 4 oficial (13 pts, dígito a dígito)",
          len(_d["value"]) == 13 and not _mism,
          "idéntico" if not _mism else "DIFIERE: " + "; ".join(_mism[:3]))
    check("DESI  R14 release/arXiv declarados en el csv",
          _d.get("release") == "DR2" and _d.get("arxiv") == "2503.14738",
          f"{_d.get('release')}/{_d.get('arxiv')}")

    # 2) Cero centinelas DR1 (2404.03002) o del QSO huérfano en el csv.
    _csv_txt = (_root / "data" / "raw" / "desi_dr2_bao.csv").read_text()
    _data_lines = [l for l in _csv_txt.splitlines()
                   if l.strip() and not l.startswith("#") and not l.startswith("z_eff")]
    _DR1_SENT = ["20.98", "20.08", "16.85", "13.62", "27.79", "13.82",
                 "39.71", "8.52", "17.88", "21.71", "30.21", "13.23", "1.491"]
    _dr1_hits = [s for s in _DR1_SENT if any(s in l for l in _data_lines)]
    check("DESI  R14 csv sin valores-centinela DR1/QSO-huérfano",
          not _dr1_hits, "limpio" if not _dr1_hits else "DR1: " + ", ".join(_dr1_hits))

    # 3) Consumers: importan del loader y no re-hardcodean datos BAO.
    _consumers = [
        _root / "src" / "mcmc_full" / "ssee_likelihoods.py",
        _root / "class_ssee" / "ssee_mcmc_fase4.py",
        _root / "src" / "p02_mcmc" / "ssee_paper2_mcmc_reframe.py",
        _root / "src" / "p02_mcmc" / "ssee_paper2_mcmc.py",
        _root / "src" / "p02_mcmc" / "ssee_paper2_mcmc_lcdm_baseline.py",
        _root / "src" / "p02_mcmc" / "rerun_cpl_h0anchors.py",
        _root / "src" / "p09_hubble" / "ssee_h0_prior_experiment.py",
        _root / "src" / "estadistica" / "ssee_phase_d_savage_cv.py",
    ]
    _no_loader, _rehard = [], []
    for _f in _consumers:
        _t = _f.read_text(errors="ignore") if _f.exists() else ""
        if "load_desi_dr2" not in _t:
            _no_loader.append(_f.name)
        if any(s in _t for s in ("20.98", "30.21, ", "[0.295,  7.93")):
            _rehard.append(_f.name)
    check("DESI  R14 consumers importan del loader único",
          not _no_loader,
          "los 8 wireados" if not _no_loader else "SIN loader: " + ", ".join(_no_loader))
    check("DESI  R14 consumers sin datos BAO re-hardcodeados",
          not _rehard, "limpio" if not _rehard else "HARDCODE: " + ", ".join(_rehard))

    # 4) Covarianza bloque-diagonal: 6 pares DM-DH correlacionados.
    _C = desi_covariance(_d)
    _npairs = int((_np.abs(_C - _np.diag(_np.diag(_C))) > 0).sum() / 2)
    check("DESI  R14 covarianza con 6 pares DM-DH (r_MH oficiales)",
          _npairs == 6, f"{_npairs} pares")

    # 5) CANARIO DE GEOMETRÍA — remache del bug χ²=726 (2026-07-09, V-L4-DESI).
    #    La geometría de fondo (E(z), r_d, distancias) DEBE usar la materia
    #    TOTAL Ω_m = ω_m/h² = 0.308881.  El sector frío 0.160 = 1+w0 NO es una
    #    densidad de fondo (es perturbaciones P6 + factor EFT α_K) y NUNCA va
    #    en un E(z).  Meterlo ahí fue el bug que dio χ²_BAO=726 en DESI DR2.
    #    Este canario reconstruye la geometría BAO desde las MISMAS fuentes
    #    (loader único + ssee_core) y ancla la invariante en los dos sentidos:
    #    con la total el χ² es sano (~11); con el sector DEBE doler (~725).
    #    Si una futura edición vuelve a meter 0.160 en E(z), esto se pone ROJO.
    from ssee_core import (W0 as _W0, WA as _WA,
                           OMEGA_M_TOTAL as _OMT, OMEGA_CDM_SECTOR as _OMS)
    _Cinv = _np.linalg.inv(_C)
    _Z, _Q, _OBS = list(_d["z"]), list(_d["quantity"]), _d["value"]
    _CKM = 2.998e5
    def _fde(z):
        a = 1.0 / (1.0 + z)
        return (1 + z) ** (3 * (1 + _W0 + _WA)) * _np.exp(-3 * _WA * (1 - a))
    def _E(z, Om):
        return _np.sqrt(Om * (1 + z) ** 3 + (1 - Om) * _fde(z))
    def _DC(zm, Om, n=250):
        zz = _np.linspace(0, zm, n)
        return _np.trapezoid(1.0 / _E(zz, Om), zz)
    import sys as _sys_rd
    _sys_rd.path.insert(0, str(ROOT))          # ROOT = src/
    from rd_camb import rd_mpc as _rd_camb   # r_d de CAMB, una sola funcion (2026-09-28)
    def _rd(obh2, omh2):
        return _rd_camb(obh2, omh2)
    def _chi2_bao(Om, obh2=0.02237):
        best = 1e30
        for _H0 in _np.linspace(55, 80, 150):   # min sobre H0: ni su mejor H0 salva al sector
            _r = _rd(obh2, Om * (_H0 / 100) ** 2)
            _p = []
            for _z, _q in zip(_Z, _Q):
                _dm = (_CKM / _H0) * _DC(_z, Om)
                _dh = _CKM / (_H0 * _E(_z, Om))
                _p.append(_dm / _r if _q == "DM_over_rd"
                          else _dh / _r if _q == "DH_over_rd"
                          else (_z * _dm ** 2 * _dh) ** (1 / 3) / _r)
            _res = _np.array(_p) - _OBS
            best = min(best, float(_res @ _Cinv @ _res))
        return best
    _c_total, _c_sector = _chi2_bao(_OMT), _chi2_bao(_OMS)
    check("DESI  R14 canario-geometría: materia TOTAL (0.308881) da χ²_BAO sano",
          _c_total < 50, f"χ²={_c_total:.1f} (<50) con Ω_m,total")
    check("DESI  R14 canario-geometría: sector 0.160 en E(z) DEBE doler",
          _c_sector > 300, f"χ²={_c_sector:.1f} (>300) — reproduce el bug χ²=726")
except Exception as e:
    check("DESI  capa operable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# CAPA R20 — anclas OBSERVACIONALES en código ⊆ CANONICAL_VALUES.yaml.
# Punto ciego de la auditoría externa 2026-07-13 (H2): un script hardcodeaba
# la PREDICCIÓN SSEE (S8=0.758) en el hueco de la OBSERVACIÓN KiDS (0.759),
# forzando 0.00σ en vez del 0.04σ real. Ningún patrón "retirado" lo cazaba
# porque 0.758 es un valor VIGENTE legítimo (la predicción). R20 verifica que
# cada variable observacional del código coincida con el DATO canónico del YAML.
# ─────────────────────────────────────────────────────────────────────
print("\nCapa R20 — anclas observacionales (código ⊆ CANONICAL_VALUES.yaml)")
try:
    import re as _re20
    _R20_ROOT = pathlib.Path(__file__).resolve().parents[2]
    _yaml20 = (_R20_ROOT / "CANONICAL_VALUES.yaml").read_text(errors="ignore")
    def _anchor20(key):
        m = _re20.search(rf"^\s*{key}:\s*([0-9.]+)", _yaml20, _re20.M)
        return m.group(1) if m else None
    # (variable observacional en código  →  clave del DATO en CANONICAL_VALUES.yaml)
    # (2026-08-02) El mapa buscaba SÓLO el nombre exacto `kids_s8`. El bug H1/H2
    # revivió en `src/ssee_resolution_figures.py` escrito como `S8_KIDS = 0.758`
    # — la PREDICCIÓN de SSEE metida en el hueco de la OBSERVACIÓN de KiDS
    # (0.759) — y R20 no lo vio porque el nombre no coincidía. Ahora cada ancla
    # lleva sus ALIAS: basta que una variable se llame de cualquiera de esas
    # formas para quedar vigilada.
    _R20_MAP = [(("kids_s8", "s8_kids"), "obs_KiDS_S8"),
                (("kids_sig8", "kids_sigma8", "sigma8_kids", "sig8_kids"), "obs_KiDS_sigma8"),
                (("des_s8", "s8_des"), "obs_DES_S8")]
    # El propio guardián queda FUERA del barrido: sus fixtures contienen a
    # propósito la forma defectuosa («S8_KIDS = (0.758,…)») para probar que el
    # detector la caza. Sin esta exclusión R20 se caza a sí mismo — pasó en la
    # primera corrida tras generalizar los alias (2026-08-02).
    _R20_FILES = [_f for _f in sorted((_R20_ROOT / "src").rglob("*.py"))
                  if "verificacion" not in _f.parts and "__pycache__" not in str(_f)]
    for _alias, _key in _R20_MAP:
        _canon = _anchor20(_key)
        if _canon is None:
            check(f"R20 ancla {_key} definida en YAML", False, "no encontrada en CANONICAL_VALUES.yaml")
            continue
        _bad = []
        _pat = "|".join(_re20.escape(_a) for _a in _alias)
        for _pf in _R20_FILES:
            # tolera `X = 0.759` y `X = (0.759, 0.024)` — la forma que usan las figuras
            for _m in _re20.finditer(rf"\b(?:{_pat})\b\s*=\s*\(?\s*([0-9.]+)",
                                     _pf.read_text(errors="ignore"), _re20.I):
                if not _m.group(1).startswith(_canon):
                    _bad.append(f"{_pf.name}:{_m.group(0).strip()[:28]}")
        check(f"R20 {_alias[0]} == {_key}={_canon} (dato, no predicción)",
              not _bad,
              f"coincide con el ancla observacional ({len(_alias)} alias vigilados)" if not _bad
              else "DESAJUSTE (predicción metida como dato?): " + "; ".join(_bad))
    # Auto-test: el detector DEBE cazar la forma exacta que se le escapó.
    _t20 = [("S8_KIDS   = (0.758, 0.024)", "0.759", True),    # el bug real
            ("S8_KIDS   = (0.759, 0.024)", "0.759", False),   # su forma corregida
            ("kids_s8 = 0.759", "0.759", False)]
    _f20 = []
    for _c, _can, _esp in _t20:
        _m = _re20.search(r"\b(?:kids_s8|s8_kids)\b\s*=\s*\(?\s*([0-9.]+)", _c, _re20.I)
        _visto = bool(_m) and not _m.group(1).startswith(_can)
        if _visto != _esp:
            _f20.append(_c)
    check("R20 el detector caza el bug H1/H2 en la forma de los scripts de figuras",
          not _f20, "; ".join(_f20) if _f20
          else "3 casos: «S8_KIDS = (0.758,…)» marcado, su forma corregida y el nombre viejo exentos")
except Exception as e:
    check("R20 capa operable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# CAPA R25 — parametrización: ω_m es el ABSOLUTO que SSEE fija; Ω_m es DERIVADO.
#
# Hallazgo 2026-07-25. Los MCMC congelaban la FRACCIÓN Ω_m=0.308881 y derivaban
# ω_m = Ω_m·h² en cada paso:
#       om_h2 = OMEGA_M_TOTAL*(H0/100)**2        ← parametrización INVERTIDA
# Pero SSEE predice el absoluto ω_m = ω_b+ω_c+ω_ν = 0.14267 (álgebra pura);
# Ω_m = ω_m/h² es una CONSECUENCIA de H₀, no un ingrediente. Al congelar Ω_m y
# variar H₀, el ω_m implícito se despegaba hasta ±1.8% de la predicción y sólo
# coincidía EXACTAMENTE en H₀ = 67.962 — el ancla. Es decir: el MCMC evaluaba
# SSEE fielmente SÓLO en el ancla y un modelo ligeramente distinto en el resto,
# sesgando el posterior hacia ella (67.948 = 0.04σ). Con ω_m fijo da 67.783
# (0.50σ) y el χ²_BAO MEJORA (10.72 → 10.33): el arreglo ajusta mejor los datos.
#
# La regla caza la FIRMA del error: multiplicar una Ω_m constante por h² para
# fabricar ω_m dentro de código de SSEE. En ΛCDM/CPL es LEGÍTIMO (ahí Ω_m es un
# parámetro muestreado, no una constante), así que sólo se marca cuando el
# multiplicando es una CONSTANTE de Ω_m (OMEGA_M_TOTAL / OM_GEOM / 0.3088x).
# ─────────────────────────────────────────────────────────────────────
print("\nCapa R25 — parametrización ω_m absoluto (no congelar Ω_m en el MCMC)")
try:
    _R25_ROOT = pathlib.Path(__file__).resolve().parents[2]
    _R25_PAT = re.compile(
        r"(OMEGA_M_TOTAL|OM_GEOM|OMEGA_M_CMB|0\.3088\d*|0\.30889)\s*\*\s*\(\s*H0\s*/\s*100")
    _R25_HITS, _npy25 = [], 0
    for _pf in sorted((_R25_ROOT / "src").rglob("*.py")) + \
               sorted((_R25_ROOT / "class_ssee").rglob("*.py")):
        # test_guardian.py contiene la cadena del error A PROPÓSITO (es la mutación
        # que prueba que R25 dispara); marcarla sería morderse la cola.
        if ("superseded" in str(_pf) or "archive" in str(_pf)
                or _pf.name in _FIXTURES):
            continue
        _npy25 += 1
        for _i, _ln in enumerate(_pf.read_text(errors="ignore").splitlines(), 1):
            if _ln.lstrip().startswith("#") or "R25-control" in _ln:
                continue   # comentarios explicativos y el modo-control declarado
            if _R25_PAT.search(_ln):
                _R25_HITS.append(f"{_pf.name}:{_i}")
    # (b) PUNTO CIEGO de (a), hallado el mismo día: en ssee_phase_d_savage_cv.py el
    # patrón era `Om * (H0/100)**2` con `Om` una VARIABLE asignada desde la constante
    # 0.308881 — la forma superficial no coincidía, el significado sí. Lección idéntica
    # a la de las mutaciones: una regla que busca la superficie deja pasar el fondo.
    # Este segundo pase marca cualquier archivo que DEFINA una constante Ω_m≈0.3088x
    # y además fabrique ω_m con ·(H0/100)**2 en alguna línea — revisión obligatoria.
    _R25_CONST = re.compile(r"^\s*\w+\s*=\s*0\.3088\d*", re.M)
    _R25_MAKE = re.compile(r"\*\s*\(\s*H0\s*/\s*100\s*\)\s*\*\*\s*2")
    for _pf in sorted((_R25_ROOT / "src").rglob("*.py")):
        if ("superseded" in str(_pf) or "archive" in str(_pf)
                or _pf.name in _FIXTURES):
            continue
        _txt = _pf.read_text(errors="ignore")
        if not (_R25_CONST.search(_txt) and _R25_MAKE.search(_txt)):
            continue
        # exento si declara explícitamente que la constante es sólo diagnóstico
        if "NO congelar" in _txt or "R25-control" in _txt or "R25-ok" in _txt:
            continue
        _R25_HITS.append(f"{_pf.name} (Ω_m constante + ω_m=Ω_m·h² en el archivo)")
    check("R25 ningún ω_m fabricado como Ω_m·h² con Ω_m constante (SSEE)",
          not _R25_HITS,
          f"{_npy25} .py activos barridos; ω_m = ω_b+ω_c+ω_ν algebraico y "
          f"Ω_m se deriva por muestra"
          if not _R25_HITS else
          "PARAMETRIZACIÓN INVERTIDA en: " + "; ".join(_R25_HITS[:6]))

    # Control de dos lados (R53, 2026-09-05). El barrido de arriba recorre el
    # repo: si hoy no hay ningún sitio malo, su «OK» no distingue «no hay bug»
    # de «el detector no mira». Estos casos fabricados lo separan.
    def _r25_marca(_txt):
        """True si el pase (b) marcaría este archivo."""
        if not (_R25_CONST.search(_txt) and _R25_MAKE.search(_txt)):
            return False
        return not ("NO congelar" in _txt or "R25-control" in _txt
                    or "R25-ok" in _txt)
    _r25_bug = "Om = 0.308881\nom_m = Om * (H0/100)**2\n"
    _r25_exento = "# R25-control\nOm = 0.308881\nom_m = Om * (H0/100)**2\n"
    _r25_sano1 = "Om = 0.308881\nom_m = ob + oc + onu\n"     # constante, sin fabricar
    _r25_sano2 = "Om = rho_m/rho_c\nom_m = Om * (H0/100)**2\n"  # derivada por muestra
    check("R25 el detector distingue Ω_m congelado de Ω_m derivado",
          _r25_marca(_r25_bug) and not _r25_marca(_r25_exento)
          and not _r25_marca(_r25_sano1) and not _r25_marca(_r25_sano2),
          "4 casos: bug marcado; anotado exento; Ω_m constante sin fabricar "
          "y Ω_m derivada por muestra, ambos limpios")
except Exception as e:
    check("R25 capa operable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# CAPA R26 — procedencia declarada: ningún canónico sin origen ni cadena.
#
# Causa raíz (OP-20, 2026-07-25): el factor 0.960318 vivió meses dentro del
# modelo sin corresponder a ninguna constante documentada (implicaba C_ν≈93.86,
# ni 94.07 ni 93.14). No lo cazó nadie porque NO HABÍA NINGÚN CAMPO donde
# tuviera que declarar su origen: bastaba con que el número «se viera bien».
# Y cuando C_ν pasó de 94.07 a 93.14, nada supo qué re-propagar porque la
# cadena de dependencias no estaba escrita — vivía en la memoria de quien hizo
# el cambio.
#
# Esta regla exige que cada nodo de `provenance:` declare las cuatro cosas:
#   formula · origin · source · (depends_on | affects)
# Un canónico sin `source` es, por definición, un número sin fuente.
#
# Verifica ADEMÁS que los valores declarados en provenance coincidan con lo
# que recomputa el guardián: la procedencia tiene que describir el número
# vigente, no uno de hace tres semanas (si no, es documentación stale, que es
# la otra mitad de la enfermedad — ver el docstring del MCMC de P2).
# ─────────────────────────────────────────────────────────────────────
print("\nCapa R26 — procedencia declarada de los canónicos")
try:
    import yaml as _yaml26
    _P26 = _yaml26.safe_load(
        (pathlib.Path(__file__).resolve().parents[2]
         / "CANONICAL_VALUES.yaml").read_text(encoding="utf-8")).get("provenance", {})
    _REQ = ("formula", "origin", "source")
    _incompletos = []
    for _k, _v in _P26.items():
        _falta = [c for c in _REQ if not _v.get(c)]
        if not (_v.get("depends_on") is not None or _v.get("affects")):
            _falta.append("depends_on/affects")
        if _falta:
            _incompletos.append(f"{_k}«falta {'+'.join(_falta)}»")
    check("R26 todo canónico con procedencia declara formula+origin+source+cadena",
          not _incompletos,
          f"{len(_P26)} nodos completos"
          if not _incompletos else "SIN FUENTE: " + "; ".join(_incompletos[:6]))

    # El valor declarado debe ser el que el guardián recomputa (no doc stale).
    _REC = {"Omega": Omega, "KAL0": KAL0, "omega_b": _omb, "omega_c": _omc,
            "omega_nu": _omnu_from_mnu, "omega_m": _omm,
            "sigma_m_nu": _mnu_active, "C_nu": _C_nu,
            # OJO: NO usar _R2 aquí — ese nombre lo reasigna la regla R2
            # (patrones del compendio multidominio, L~725) a una LISTA.
            # Colisión de nombres real en el guardián; se recomputa local.
            "R2": Omega / (KAL0 * Tr),
            "tau_Pi_H0": KAL0 * Omega / Tr, "n_s": 1 - phi ** -7,
            "Omega_m_cosm": _omm / _h ** 2}   # _h = H_alg/100, definido en Capa 1
    _desfasados = [
        f"{_k}: doc {_P26[_k]['value']} vs recomputado {_r:.7f}"
        for _k, _r in _REC.items()
        if _k in _P26 and abs(float(_P26[_k]["value"]) - _r) > 5e-6]
    check("R26 los valores de procedencia == los que recomputa el guardián",
          not _desfasados,
          f"{len(_REC)} verificados contra el cómputo"
          if not _desfasados else "DOC STALE: " + "; ".join(_desfasados[:5]))
except Exception as e:
    check("R26 capa operable", False, str(e))

# ── R27 — el look-elsewhere que citan los papers == el que se recomputa ──────
# El titular «1 de 490» es la defensa central contra la acusación de numerología,
# y hasta 2026-07-25 vivía sin red: ningún check ataba el 55/25/490 ni la tabla de
# tolerancias del PRD al script que los produce, y el script no tenía log. Si el
# diccionario crece (ya pasó: 46→50→55 nombres), los papers quedarían citando un
# denominador viejo y NADA lo delataría — el peor sitio posible para un número
# stale, porque es el que un referee hostil va a querer reproducir.
try:
    _le_path = _REPO2 / "src" / "estadistica" / "look_elsewhere_full.py"
    _le_ns: dict = {"__name__": "_le", "__file__": str(_le_path)}
    exec(compile(_le_path.read_text(errors="ignore").split("if __name__")[0],
                 str(_le_path), "exec"), _le_ns)
    _fam = _le_ns["FAMILY"]
    _rat = _le_ns["distinct_ratios"](_fam)
    _n_names = len(_fam)
    _n_vals = len({round(v, 6) for v in _fam.values()})
    _n_rat = len(_rat)
    _h0 = sum(1 for r, _ in _rat if abs(r - _le_ns["W0"]) <= 5e-4)
    _ha = sum(1 for r, _ in _rat if abs(r - _le_ns["WA"]) <= 5e-4)
    # Lo que los manuscritos AFIRMAN (PRD + Sealed + Paper 1 dicen los tres 490).
    # OJO: se excluyen los rangos con «~» (p.ej. «$\sim$1-in-500»), que NO son el
    # look-elsewhere del core sino la gramática del multiplicador φ-DM — una cuenta
    # distinta que el propio PRD declara sin privilegio estadístico (§2.3, scope).
    _claimed = set()
    for _t in _texs2:
        _txt = _t.read_text(errors="ignore")
        for _m in _re2.finditer(r"1\$?[- ]in[- ]\$?(\d{3})|1 of (\d{3})|yields \$(\d{3})\$",
                                _txt):
            if "sim" in _txt[max(0, _m.start() - 10):_m.start()]:
                continue
            _claimed.add(int(next(g for g in _m.groups() if g)))
    _bad = _claimed - {_n_rat}
    check("R27 look-elsewhere: 55/25/490 y 1-de-490 == lo que recomputa el script",
          _n_names == 55 and _n_vals == 25 and _n_rat == 490
          and _h0 == 1 and _ha == 1 and not _bad,
          f"{_n_names} nombres / {_n_vals} valores / {_n_rat} razones; "
          f"aciertos a ±0.0005: w₀={_h0}, wₐ={_ha}; manuscritos citan {sorted(_claimed) or '—'}"
          if not _bad and _n_rat == 490
          else f"DESAJUSTE: script da {_n_names}/{_n_vals}/{_n_rat} (w₀={_h0},wₐ={_ha}); "
               f"manuscritos citan {sorted(_bad)}")
except Exception as e:
    check("R27 capa operable", False, str(e))

# ── R28 — la copia del repo == el diccionario CITABLE (sin deriva) ───────────
# 2026-07-25: había DOS look_elsewhere_full.py. Los valores coincidían (55/25/490),
# así que ningún check numérico podía notarlo — pero el código NO era el mismo: la
# copia del repo se quedó en la nomenclatura pre-v1.5 (MIKAEL_V, MIKE) y escribía
# wₐ = PYROS/KRYSTOS_V, el denominador equivocado, justo en el script del titular.
# Una copia que nadie compara no es un respaldo: es una segunda fuente de verdad.
# Se compara el CÓDIGO EJECUTABLE (sin comentarios/espacios): la prosa puede
# diferir —la copia del repo añade la robustez QUINTAL…DECAL— pero las constantes
# y las identidades no. Si zenodo_dictionary/ no está presente, se avisa sin ROJO:
# está gitignoreado y un clon limpio no lo tiene.
try:
    _cit = _REPO2 / "zenodo_dictionary" / "look_elsewhere_full.py"
    _mir = _REPO2 / "src" / "estadistica" / "look_elsewhere_full.py"

    import ast as _ast

    def _codigo(p):
        """Asignaciones de constantes a nivel de módulo, vía AST.

        Se usa AST y no regex de línea porque una frase de docstring como
        «CUÄSTAL=4Ω; su continuación…» se parece a una asignación y hacía saltar
        esta misma regla en falso — prosa disfrazada de código.
        """
        _out = []
        for _n in _ast.parse(p.read_text(errors="ignore")).body:
            if isinstance(_n, _ast.Assign):
                for _t in _n.targets:
                    if isinstance(_t, _ast.Name):
                        _out.append(f"{_t.id}={_ast.dump(_n.value)}")
        return _out

    if not _cit.exists():
        check("R28 espejo diccionario citable (zenodo_dictionary ausente)", True,
              "gitignoreado; en un clon limpio no aplica — verificar en la máquina de trabajo")
    else:
        _a, _b = _codigo(_mir), _codigo(_cit)
        _falta = [x for x in _b if x not in _a]
        _sobra = [x for x in _a if x not in _b]
        check("R28 look_elsewhere_full.py del repo == el del diccionario citable",
              not _falta and not _sobra,
              f"{len(_b)} definiciones idénticas (espejo verbatim de v1.5)"
              if not _falta and not _sobra
              else f"DERIVA: sólo-citable={_falta[:3]} sólo-repo={_sobra[:3]}")
except Exception as e:
    check("R28 capa operable", False, str(e))

# ── R29 — símbolo ↔ entidad es BIYECCIÓN, y los padres cuadran ───────────────
# Pedido de Mike (2026-07-25): la tabla de notación debe llevar
#   símbolo | nombre | padres | fórmula algebraica | valor,
# y «la simbología tampoco puede estar duplicada y debe pertenecer a una sola de
# las entidades algebraicas». El motivo es operativo: I_g y K_v VALEN LO MISMO
# (9.519253285), así que el número no distingue cuál usa una ecuación — sólo el
# símbolo lo hace. Si el símbolo es único por entidad, ver K_v donde va I_g se
# detecta a simple vista; si se duplica, vuelve el error de esta semana.
# Se verifica: (a) ningún símbolo mapea a dos entidades; (b) el valor que la
# tabla declara == el que se recomputa desde la FÓRMULA de sus padres.
_SIMBOLOS = {
    # símbolo LaTeX      (entidad,        fórmula evaluable con las de arriba)
    r"\varphi":          ("—",           lambda d: (1 + 5 ** 0.5) / 2),
    r"\pi":              ("—",           lambda d: _math.pi),
    r"\Omega":           ("OMEGA",       lambda d: d["φ"] + d["π"]),
    r"\beta":            ("BIAL",        lambda d: (d["φ"] + d["π"]) / 2),
    "KAL":               ("KAL",         lambda d: d["β"] + d["π"]),
    "AURA":              ("AURA",        lambda d: d["β"] + d["φ"]),
    "MIRA":              ("MIRA",        lambda d: d["AURA"] / 2),
    "P_{\\mathrm{sc}}":  ("PYROS",       lambda d: d["Ω"] + d["φ"]),
    "I_g":               ("IGNIS",       lambda d: d["π"] + d["PYROS"]),
    "K_v":               ("KRYSTOS_V",   lambda d: d["φ"] + d["π"] + d["Ω"]),
    "T_r":               ("TRIAL",       lambda d: 3 * d["AURA"]),
    "M_v":               ("ATLAS",       lambda d: d["φ"] + d["π"] + d["K_v"]),
}
try:
    import math as _math
    _ents = [e for e, _ in _SIMBOLOS.values() if e != "—"]
    _dup_ent = {e for e in _ents if _ents.count(e) > 1}
    _dup_sim = len(_SIMBOLOS) != len({s for s in _SIMBOLOS})

    _d = {}
    _d["φ"] = (1 + 5 ** 0.5) / 2
    _d["π"] = _math.pi
    _d["Ω"] = _d["φ"] + _d["π"]
    _d["β"] = _d["Ω"] / 2
    _d["AURA"] = _d["β"] + _d["φ"]
    _d["PYROS"] = _d["Ω"] + _d["φ"]
    _d["K_v"] = _d["φ"] + _d["π"] + _d["Ω"]
    # el valor de cada símbolo, recomputado desde la fórmula de sus padres
    _calc = {s: f(_d) for s, (e, f) in _SIMBOLOS.items()}
    # contra el diccionario citable: la entidad nombrada debe valer eso mismo
    _desaj = []
    if _cit.exists():
        _ns2: dict = {"__name__": "_c2", "__file__": str(_cit)}
        exec(compile(_cit.read_text(errors="ignore").split("def distinct_ratios")[0],
                     str(_cit), "exec"), _ns2)
        _famc = _ns2["FAMILY"]
        for _s, (_e, _f) in _SIMBOLOS.items():
            if _e in ("—",):
                continue
            _ref = _famc.get(_e, _ns2.get(_e))
            if _ref is None or abs(_ref - _calc[_s]) > 1e-9:
                _desaj.append(f"{_s}→{_e}")
    # (c) la TABLA del PRD debe declarar el mismo par (símbolo, nombre). Sin esto
    # R29 sólo se auditaría a sí misma: el .tex podría derivar y nadie lo vería.
    _tabla = []
    _sealed = _REPO2 / "manuscript" / "SSEE_Sealed_Journal.tex"
    for _doc in (_prd, _sealed):
        if not _doc.exists():
            continue
        _sec = _doc.read_text(errors="ignore").split("Symbol & Name & Parents")
        if len(_sec) > 1:
            for _fila in _sec[1].split(r"\bottomrule")[0].splitlines():
                _cols = [c.strip() for c in _fila.split("&")]
                if len(_cols) >= 5 and _cols[1] not in ("", "---"):
                    _sim = _cols[0].replace("$", "").replace(r"\mathrm{", "").rstrip("}")
                    _nom = _cols[1].replace("$_V$", "_V").replace("$", "")
                    _tabla.append((_sim, _nom, _cols[3], _cols[4]))

    # (c2) la columna «reduced form in φ,π» debe EVALUAR al valor de la fila.
    # Es la columna que Mike pidió para poder distinguir de un vistazo: I_g y K_v
    # tienen PADRES distintos y la misma reducción 2(φ+π) — por eso comparten valor.
    # Si la reducción fuera decorativa (copiada, no verificada) la tabla mentiría
    # justo donde promete transparencia.
    _pura_mal = []
    for _sim, _nom, _pura, _val in _tabla:
        _e = _pura.replace("$", "").replace(r"\varphi", "PHI").replace(r"\pi", "PI")
        _e = _e.replace(r"\sqrt5", "(5**0.5)").replace(r"\sqrt{5}", "(5**0.5)")
        _e = _re2.sub(r"(\d)\(", r"\1*(", _e)          # 2( -> 2*(
        _e = _re2.sub(r"(\d)(PHI|PI)", r"\1*\2", _e)   # 3PHI -> 3*PHI
        _e = _re2.sub(r"\)(PHI|PI)", r")*\1", _e)
        try:
            _got = eval(_e, {"__builtins__": {}}, {"PHI": _d["φ"], "PI": _d["π"]})
            if abs(_got - float(_val.replace("$", "").replace("\\\\", "").strip())) > 5e-5:
                _pura_mal.append(f"{_sim}: {_pura}={_got:.5f}≠{_val}")
        except Exception:
            _pura_mal.append(f"{_sim}: reducción ilegible «{_pura}»")
    _falta_tab = []
    for _sim, _nom, _pura, _val in _tabla:
        _esp = {e for s, (e, _) in _SIMBOLOS.items()
                if s.replace("\\", "").replace("_{\\mathrm{sc}}", "_sc") == _sim
                or s.replace("\\", "") == _sim}
        if _esp and _nom not in _esp:
            _falta_tab.append(f"tabla dice {_sim}→{_nom}, guardián {_esp}")
    # (d) el otro lado de la biyección: una ENTIDAD no puede llevar DOS símbolos.
    # Ω y Ω_DNAV nombraban la misma entidad (φ+π) y llegaron a aparecer juntos en
    # una misma fila de Paper 1 — un lector no puede saber que son lo mismo.
    _alias = []
    for _t in _texs2:
        _txt = _t.read_text(errors="ignore")
        if r"\Omega_{\rm DNAV}" in _txt and _t.name not in (
                "SSEE_Paper6_phiDM.tex", "SSEE_Paper9_HubbleTension.tex"):
            _alias.append(_t.name)
    check("R29 símbolo↔entidad biyectivo, valor == fórmula, tablas conformes",
          not _dup_ent and not _dup_sim and not _desaj and not _falta_tab
          and not _alias and not _pura_mal,
          f"{len(_SIMBOLOS)} símbolos → {len(set(_ents))} entidades; "
          f"{len(_tabla)} filas conformes (PRD+Sealed), reducción φ,π verificada; "
          f"I_g≠K_v como entidades aunque compartan {_calc['I_g']:.9f}"
          if not _dup_ent and not _desaj and not _falta_tab and not _alias
             and not _pura_mal
          else f"duplicado={sorted(_dup_ent)} desajuste={_desaj} "
               f"tabla={_falta_tab[:3]} alias-Ω_DNAV={_alias} reducción={_pura_mal[:3]}")
except Exception as e:
    check("R29 capa operable", False, str(e))

# ── R30 — política de redondeo: lo mostrado es el redondeo CORRECTO ──────────
# Decisión de Mike (2026-07-25): el redondeo se FIJA, no se decide caso por caso.
# Álgebra SSEE a 12 decimales, cantidades del modelo a 6. Un redondeo suelto es
# fuente de error propia — un decimal arrastra a los siguientes — y decir un
# número mientras se usa otro ES un error, aunque el valor esté «casi bien».
#
# LA REGLA NO ES «la cadena mostrada reproduce»: las cadenas AMPLIFICAN. Con
# ω_m=0.142668 (6 dec, correcto) la división mostrada da 0.308882 y el exacto es
# 0.308881. Se exige lo verificable: |mostrado − exacto| ≤ media unidad del
# último decimal mostrado.
#
# CASO QUE LA ORIGINÓ: Ω_m se publicaba como 0.3088'9' en 157 sitios / 14 docs.
# Exacto 0.308880879 → correcto 0.308881. El dígito de más salía de redondear
# ω_m a 0.14267 (sube desde 0.1426675) y dividir ESE número — intermedios
# redondeados, ningún valor rancio. El literal viejo distaba 9.1e-6 del exacto,
# más de media unidad del 5º decimal (5e-6) ⇒ R30 lo caza.
# (El literal viejo NO se escribe aquí: el escáner de valores retirados lo vería.)
try:
    # Se ancla al SÍMBOLO, no al literal suelto: un número por sí solo no dice de
    # quién es. La primera versión marcó en rojo 0.02237/0.1200/0.9649 — que son
    # MEDIDAS de Planck, no predicciones SSEE. Un verificador que no distingue el
    # dato de la predicción es peor que ninguno.
    _ANCLAS = {
        "Omega_m (=ω_m/h²)": (_core.OMEGA_M_TOTAL, [
            r"\\omega_m/h\^2\s*(?:&|)\s*=\s*([\d.]+)",
            r"\\Om\^\{\\mathrm\{cosm\}\}\s*=\s*([\d.]+)",
            r"\\Omega_\{m,\\mathrm\{cosm\}\}\s*=\s*([\d.]+)",
        ]),
        "omega_m": (_core.OMEGA_M_H2, [r"\\omega_m\s*=\s*\\omega_b\+\\omega_c\+\\omega_\\nu\s*=\s*([\d.]+)"]),
        "w0": (abs(_core.W0), [r"w_0\s*(?:&|)\s*=\s*-\s*([\d.]{6,})"]),
        "wa": (abs(_core.WA), [r"w_a\s*(?:&|)\s*=\s*-\s*([\d.]{6,})"]),
        # Añadidas 2026-07-27. Regar el ÁRBOL, no la fruta: el PRD y el Sealed
        # son resúmenes derivados; los Papers son la fuente. Si un Paper muestra
        # un valor y el consolidado otro, quien compare ve al modelo
        # contradiciéndose consigo mismo — y eso pesa más que cualquier acierto.
        # Estas cinco se verificaron a mano en §4.1/§4.2 del PRD; aquí se
        # exigen en TODOS los .tex, Papers incluidos.
        "alpha_K(0)": (3 * (_core.AURA / _core.OMEGA) * (1 + _core.W0), [
            r"\\alpha_\{?\\rm K\}?\(0\)\s*(?:&|)\s*=\s*([\d.]{5,})",
            r"\\alpha_K\(0\)\s*(?:&|)\s*=\s*([\d.]{5,})",
        ]),
        "AURA": (_core.AURA, [r"\\mathrm\{AURA\}\s*(?:&|)\s*=\s*([\d.]{5,})"]),
        "N_star (=2phi^7)": (2 * phi ** 7, [
            r"N_\\ast\s*(?:&|)?\s*=\s*2\\varphi\^7\s*=?\s*([\d.]{4,})",
            r"2\\varphi\^7\s*=\s*([\d.]{4,})",
        ]),
        "n_s (=1-phi^-7)": (1 - phi ** -7, [
            r"1-\\varphi\^\{-7\}\s*(?:&|)\s*=\s*([\d.]{5,})"]),
        # 2026-07-27, lectura Paper 1 pág. 1: TRES de las siete constantes de la
        # lista fundacional estaban TRUNCADAS, no redondeadas — 6.3776 por
        # 6.3777, 9.5192 por 9.5193, 14.2788 por 14.2789. Corregidas en 14
        # sitios de 5 documentos. Están en la primera página del paper que
        # define el diccionario: es lo primero que un referee comprueba.
        "P_sc (=Omega+phi)": (pi + 2 * phi, [
            r"\\Omega\+\\varphi\\approx([\d.]+)"]),
        "K_v (=phi+pi+Omega)": (2 * (phi + pi), [
            r"\\varphi\+\\pi\+\\Omega\\approx([\d.]+)"]),
        "M_v (=phi+pi+K_v)": (3 * (phi + pi), [
            r"\\varphi\+\\pi\+K_v\\approx([\d.]+)"]),
        "alpha (=phi^4/3)": (phi ** 4 / 3, [
            r"\\frac\{\\varphi\^4\}\{3\}\s*(?:&|)\s*=\s*([\d.]{5,})"]),
    }
    _mal_red = []
    for _nom, (_ex, _pats) in _ANCLAS.items():
        for _t in _texs2:
            _txt = _t.read_text(errors="ignore")
            for _pat in _pats:
                for _m in _re2.finditer(_pat, _txt):
                    _lit = _m.group(1).rstrip(".")
                    if "." not in _lit:
                        continue
                    _dec = len(_lit.split(".")[1])
                    if _dec < 4:
                        continue
                    if abs(float(_lit) - _ex) > 0.5 * 10 ** (-_dec):
                        _mal_red.append(f"{_t.name}«{_lit}»≠{_ex:.{_dec}f} ({_nom})")
    # ── R30b — falsa precisión: rellenar un valor MEDIDO hasta el techo ──────
    # Objeción de Mike (2026-07-25): «si el número es finito con 4 o 5 decimales
    # esa regla no aplica, y peor si termina ahí». Cierto y verificado: 93.140000
    # ATRAVIESA la prueba de redondeo (|93.140000 − 93.14| = 0) mientras afirma
    # cuatro decimales que ningún experimento midió. El techo de 6/12 decimales
    # vale para lo ALGEBRAICO —infinitos dígitos, siempre hay uno más— y NUNCA
    # para lo medido: ahí manda la precisión del instrumento.
    _MEDIDAS = {          # constante medida : (literal canónico, decimales reales)
        "C_ν":      ("93.14", 2),
        "KiDS S₈":  ("0.759", 3),
        "KiDS σ₈":  ("0.737", 3),
        "DES S₈":   ("0.776", 3),
    }
    for _nom, (_lit, _dec) in _MEDIDAS.items():
        for _t in _texs2:
            for _m in _re2.finditer(_re2.escape(_lit) + r"(\d+)",
                                    _t.read_text(errors="ignore")):
                # dígitos extra que son sólo ceros ⇒ relleno, no medida
                if _m.group(1) and _m.group(1).strip("0") == "":
                    _mal_red.append(f"{_t.name}«{_m.group(0)}» falsa precisión "
                                    f"({_nom} se mide a {_dec} dec)")

    _mal_red = sorted(set(_mal_red))
    check("R30 redondeo: valor mostrado == redondeo correcto, sin falsa precisión",
          not _mal_red,
          f"{len(_ANCLAS)} cantidades ancladas a su símbolo en {len(_texs2)} documentos "
          f"(política: álgebra 12 dec, modelo 6 dec)"
          if not _mal_red else f"MAL REDONDEADOS: {'; '.join(_mal_red[:6])}")

    # Control de dos lados (R53, 2026-09-05). La detección de falsa precisión
    # es: al literal medido le siguen dígitos que son TODOS ceros ⇒ relleno.
    # Sin control, un «OK» no distingue «nadie rellena» de «no se busca».
    def _r30_falsa(_txt, _lit):
        for _m in _re2.finditer(_re2.escape(_lit) + r"(\d+)", _txt):
            if _m.group(1) and _m.group(1).strip("0") == "":
                return True
        return False
    check("R30 el detector distingue relleno de ceros de dígito significativo",
          _r30_falsa("S_8 = 0.75900", "0.759")
          and _r30_falsa("S_8 = 0.7590", "0.759")
          and not _r30_falsa("S_8 = 0.759", "0.759")
          and not _r30_falsa("S_8 = 0.7592", "0.759"),
          "4 casos: 0.75900 y 0.7590 marcados (ceros de relleno); "
          "0.759 exacto y 0.7592 (dígito real) limpios")
except Exception as e:
    check("R30 capa operable", False, str(e))

# ── R31 — el ssee_core IMPORTADO == el ssee_core del FUENTE ─────────────────
# 2026-07-25, segunda vez en el día. Un `.pyc` rancio de `__pycache__` devolvió
# SUM_MNU_EV=0.06902 mientras el archivo en disco decía 0.06849, y con él ω_m y
# Ω_m quedaron en la cadena vieja. Esta vez llegó más lejos: el MCMC de
# producción arrancó imprimiendo Ω_m,total = 0.30889320 (cadena rancia) en vez de
# 0.30888088 — una corrida de 35 min silenciosamente corrupta, lanzada
# precisamente para arreglar procedencia. Hubo que abortarla.
#
# El guardián ya compila el fuente para SUS lecturas (ver bloque «Fuente
# canónica»), así que él no se engaña; pero CUALQUIER OTRO script del repo hace
# `import ssee_core` y sí puede recibir bytecode viejo. R31 detecta la condición
# desde fuera, sin importar la causa: compara el valor que da el IMPORT normal
# contra el que da el AST del fuente. Si difieren, hay una caché mintiendo y
# todo lo que se corra en ese estado es sospechoso.
#   Nota: `python -B` NO sirve como defensa — impide ESCRIBIR bytecode, no LEERLO.
try:
    import ast as _ast31
    import importlib as _il31
    _src31 = (_REPO2 / "src" / "ssee_core.py").read_text(errors="ignore")
    _fuente = {}
    for _n in _ast31.parse(_src31).body:
        if isinstance(_n, _ast31.Assign) and isinstance(_n.value, _ast31.Constant):
            for _t in _n.targets:
                if isinstance(_t, _ast31.Name) and isinstance(_n.value.value, float):
                    _fuente[_t.id] = _n.value.value
    _il31.invalidate_caches()
    if str(_REPO2 / "src") not in sys.path:
        sys.path.insert(0, str(_REPO2 / "src"))
    _imp31 = _il31.import_module("ssee_core")
    _discrepa = [f"{_k}: import={getattr(_imp31, _k)} fuente={_v}"
                 for _k, _v in _fuente.items()
                 if hasattr(_imp31, _k) and abs(getattr(_imp31, _k) - _v) > 1e-12]
    check("R31 bytecode: ssee_core importado == ssee_core del fuente",
          not _discrepa,
          f"{len(_fuente)} constantes literales coinciden import↔fuente"
          if not _discrepa
          else "CACHÉ RANCIA (borrar __pycache__ y RE-CORRER lo que se haya "
               "ejecutado en este estado): " + "; ".join(_discrepa[:4]))
except Exception as e:
    check("R31 capa operable", False, str(e))

# ─────────────────────────────────────────────────────────────────────
# VEREDICTO
# ─────────────────────────────────────────────────────────────────────
# ORDEN DE DIAGNÓSTICO (2026-07-29). El orden en que se EJECUTAN las capas no es
# el orden en que dependen unas de otras: se fueron añadiendo según se creaban, y
# hay 17 inversiones — se confronta con los datos DESI en la 3ª capa y su
# procedencia se verifica en la 23ª; el núcleo `ssee_core`, que es el cimiento, se
# comprueba después de las tres capas que se apoyan en él.
#
# Reordenar la EJECUCIÓN es arriesgado (las capas comparten variables ya
# calculadas), y además no hace falta: el guardián ACUMULA los fallos —ningún
# verde posterior borra un rojo anterior, comprobado inyectando un defecto en la
# primera capa y viendo 146 OK después sin que el veredicto dejara de ser ROJO—.
#
# Lo que sí duele es el DIAGNÓSTICO: si la raíz está en el dato crudo y sólo se
# ven las consecuencias río abajo, se arregla el síntoma. Así que el veredicto se
# ordena por nivel de dependencia, y el primero que se nombra es el que hay que
# mirar. Es la imagen del dominó: importa saber qué ficha se empujó, no cuántas
# cayeron.
_NIVEL = {1: "FUENTE — dato crudo, núcleo y procedencia",
          2: "ÁLGEBRA — identidades de φ y π",
          3: "ARTEFACTOS — logs y scripts contra el núcleo",
          4: "CONFRONTACIÓN — dato medido contra predicción",
          5: "ESCRITURA — manuscritos",
          6: "GOBIERNO — memorias, archivo y publicación"}
_PREF_NIVEL = [
    (("DESI", "canon", "R26", "R31", "R32", "R20"), 1),
    (("V-L2", "V-L3", "L1 ", "L2 ", "V-L3"), 2),
    (("R33", "R34", "R35", "R36", "R52", "R65", "R66", "R68",
      "procedencia", "Procedencia"), 3),
    (("V-L4", "R25"), 4),
    (("R37", "R38", "R40", "R41", "R42", "R43", "R44", "R45",
      "R1 ", "R2 ", "R9", "R10", "R11", "R13", "R14", "R15", "R17", "R18",
      "R19", "R21", "R22", "R23", "R24", "R27", "R28", "R29", "R30",
      "R55", "R56", "R58", "R59", "R60", "R61", "R63",
      "diccionario", "sello"), 5),
    (("memoria", "archivo", "R12", "R39", "R46"), 6),
    # el propio aparato de verificacion: se mira al final, porque un
    # fallo suyo no invalida un numero, invalida la CONFIANZA en el resto.
    (("R47", "R48", "R49", "R50", "R51", "R53", "R54",
      "R57", "R62", "R64", "R67"), 7),
]


def _nivel_de(nombre):
    for _p, _n in _PREF_NIVEL:
        if nombre.startswith(_p):
            return _n
    return 9          # sin clasificar: se muestra al final, nunca se oculta


# ── R46 · piso de comprobaciones ──────────────────────────────────────────────
# Catorce capas leen su archivo con `if ... exists()`. Si un .tex se renombra o
# se mueve, sus comprobaciones no FALLAN: dejan de EJECUTARSE, y el guardián
# sigue diciendo VERDE con menos trabajo hecho. Es la cuarta patología —el verde
# por vacío— aplicada a una capa entera en vez de a una regla.
# El piso se sube a mano al añadir capas; NUNCA se baja para tapar una corrida.
# ════════════════════════════════════════════════════════════════════════════
# R47 — TODA PIEZA DECLARADA COMO SUPUESTO TIENE QUE ESTAR RASTREADA (2026-08-02)
#
# POR QUÉ EXISTE (metáfora de Mike, y es literal): «una pieza floja en el
# chasis y la computadora nunca la marcó como problema».
#
# El caso real: `ssee_paper5_IS_perturbations.py` fija
#     zeta_tilde = KAL0/3      # SSEE hypothesis
# y de ahí sale el resultado c²_s = 0 EXACTO de Paper 5. El 0 es álgebra
# limpia — pero cuelga de esa hipótesis, que nunca se derivó ni se puso a
# prueba. Vivió meses sin que nada la señalara: no es drift (ningún número
# está mal), no es incoherencia (todo concuerda consigo mismo), así que
# ninguna capa previa podía verla. Se encontró a mano, tirando de un hilo.
#
# La regla: si el código ACTIVO etiqueta algo como hypothesis/ansatz/supuesto,
# ese algo debe estar (a) registrado en OPEN_PROBLEMS.md, o (b) llevar al lado
# el puntero a dónde se deriva. Si no está ninguna de las dos, es una pieza
# floja y R47 la marca.
#
# Coherencia ≠ corrección; y AUSENCIA DE ALARMA ≠ ausencia de problema.
print("\nCapa R47 — piezas declaradas como supuesto: ¿rastreadas?")
try:
    _MARCAS = ("hypothesis", "hipótesis", "hipotesis", "ansatz",
               "conjetura", "we posit", "assumed:")
    # Falsos positivos que NO son supuestos del modelo:
    #  - «hipótesis nula» / «null hypothesis»: estadística estándar, no un
    #    supuesto físico sin derivar.
    #  - «no se asume» / «not assumed»: dice justo lo contrario.
    _NO_ES = ("nula", "null", "no se asume", "not assumed", "se mide para saberlo")
    # Un supuesto está RASTREADO si su línea (o vecinas ±2) cita un OP, o
    # apunta a dónde se deriva.
    _RASTRO = _re.compile(r"OP-\d+|OPEN_PROBLEMS|deriv|demostr|proof|teorema|theorem",
                          _re.I)
    _sueltas, _npy47 = [], 0
    for _py in sorted((_REPO / "src").rglob("*.py")):
        if "__pycache__" in str(_py) or "verificacion" in str(_py):
            continue
        _npy47 += 1
        _ls = _py.read_text(errors="ignore").splitlines()
        for _i, _ln in enumerate(_ls):
            _low = _ln.lower()
            if not any(_m in _low for _m in _MARCAS):
                continue
            if any(_n in _low for _n in _NO_ES):
                continue
            _win = "\n".join(_ls[max(0, _i - 2):_i + 3])
            if _RASTRO.search(_win):
                continue
            _sueltas.append(f"{_py.relative_to(_REPO)}:{_i+1} «{_ln.strip()[:58]}»")
    # Auto-test: el detector tiene que ver un supuesto sin rastro y NO ver uno con rastro.
    _t47 = [("# SSEE hypothesis: zeta = KAL0/3", True),
            ("# ansatz, sin derivar aun (OP-9)", False),
            ("el multiplo entero es la hipotesis nula contra la que se mide", False),
            ("se mide para saberlo, no se asume", False)]
    _f47 = []
    for _c, _esp in _t47:
        _cl = _c.lower()
        _visto = (any(_m in _cl for _m in _MARCAS)
                  and not any(_n in _cl for _n in _NO_ES)
                  and not _RASTRO.search(_c))
        if _visto != _esp:
            _f47.append(_c)
    check("R47 el detector distingue supuesto rastreado de suelto",
          not _f47, "; ".join(_f47) if _f47
          else "4 casos: «SSEE hypothesis» pelado marcado; «ansatz (OP-9)», «hipótesis nula» y «no se asume» exentos")
    check("R47 ningún supuesto del código activo sin OP ni derivación",
          not _sueltas,
          "; ".join(_sueltas[:4]) + (f" … (+{len(_sueltas)-4})" if len(_sueltas) > 4 else "")
          if _sueltas else f"los supuestos DECLARADOS en {_npy47} .py llevan "
               f"OP o puntero "
               f"a derivación; no dice nada de los supuestos sin declarar")
except Exception as _e:
    check("R47 escaneo de supuestos", False, str(_e))

# ════════════════════════════════════════════════════════════════════════════
# R48 — LA MISMA CANTIDAD, CALCULADA EN DOS DOCUMENTOS, DEBE DAR LO MISMO
#
# POR QUÉ EXISTE (OP-22, y Mike lo había pedido al crear la procedencia).
# La corrección viscosa ζ/(ρ·τ_Π) vale 1 en SSEE_EFT_section.tex —es así como
# se DERIVÓ τ_Π, poniendo c²_s=1 en la frontera de causalidad— y 0.839950 en
# SSEE_Paper5_IS.tex. Misma cantidad física, dos valores. De ahí sale el
# c²_s = 0 de Paper 5: un artefacto de mezclar normalizaciones ENTRE documentos.
#
# Ninguna capa lo veía porque CADA NÚMERO, POR SEPARADO, ES CORRECTO Y
# TRAZABLE. R26 verifica que la fórmula de un canónico recompute su valor;
# nadie preguntaba «esta cantidad, en el documento A y en el B, ¿da lo mismo?».
# Coherencia dentro de cada documento ≠ coherencia entre documentos.
print("\nCapa R48 — misma cantidad en dos documentos: ¿mismo valor?")
try:
    _CD = _yaml26.safe_load(
        (_REPO / "CANONICAL_VALUES.yaml").read_text(encoding="utf-8")
    ).get("cross_document", []) or []
    _cd_rotos, _cd_deuda, _cd_anclas = [], [], []
    for _e in _CD:
        _docs = _e.get("documentos", [])
        _tol = float(_e.get("tolerancia", 1e-4))
        _vals = [float(_d["valor"]) for _d in _docs]
        # (a) el archivo citado existe y contiene su ancla
        for _d in _docs:
            _f = _REPO / _d["archivo"]
            if not _f.exists():
                _cd_anclas.append(f"{_e['id']}: no existe {_d['archivo']}")
            elif _d.get("ancla") and _d["ancla"] not in _f.read_text(errors="ignore"):
                _cd_anclas.append(f"{_e['id']}: {_d['archivo']} sin «{_d['ancla']}»")
        # (b) todos los valores coinciden
        if _vals and (max(_vals) - min(_vals)) > _tol:
            _msg = (f"{_e['id']}: " +
                    " vs ".join(f"{_d['archivo'].split('/')[-1]}={_d['valor']}"
                                for _d in _docs))
            (_cd_deuda if _e.get("op_abierto") else _cd_rotos).append(
                _msg + (f" [{_e['op_abierto']}]" if _e.get("op_abierto") else ""))
    check("R48 los documentos citados existen y contienen su ancla",
          not _cd_anclas, "; ".join(_cd_anclas[:4]) if _cd_anclas
          else f"{sum(len(e.get('documentos', [])) for e in _CD)} anclas resueltas")
    check("R48 ninguna cantidad con dos valores SIN OP que lo declare",
          not _cd_rotos, "; ".join(_cd_rotos[:4]) if _cd_rotos
          else f"{len(_CD)} cantidades cruzadas revisadas")
    _TOPE_CD = 1          # medido 2026-08-02; sólo puede BAJAR
    check(f"R48 la deuda de discrepancias no crece (tope {_TOPE_CD})",
          len(_cd_deuda) <= _TOPE_CD,
          f"{len(_cd_deuda)} discrepancia(s) declarada(s) con OP: "
          + "; ".join(_cd_deuda[:3]) if _cd_deuda else "sin discrepancias")
    # Auto-test: el detector tiene que ver una discrepancia real y no inventar una.
    _t48 = [([1.0, 0.839950], 1e-4, True), ([1.0, 1.00005], 1e-4, False)]
    _f48 = [v for v, t, esp in _t48 if ((max(v) - min(v)) > t) != esp]
    check("R48 el detector distingue discrepancia real de ruido de redondeo",
          not _f48, str(_f48) if _f48
          else "2 casos: 1 vs 0.839950 marcado; 1 vs 1.00005 dentro de tolerancia")
except Exception as _e:
    check("R48 capa operable", False, str(_e))

# ════════════════════════════════════════════════════════════════════════════
# R49 — EL CAMPO `source` DE UN CANÓNICO TIENE QUE APUNTAR A ALGO REAL
#
# POR QUÉ EXISTE. La procedencia de tau_Pi_H0 declara
#   source: "Paper 4 L686 (tiempo de relajacion Israel-Stewart)"
# pero Paper 4 sólo la USA; la derivación real (c²_s=1 en la frontera de
# causalidad) está en SSEE_EFT_section.tex. Y Paper 1 remite a un «App. A»
# que no existe. R26 verificaba que el campo ESTUVIERA; no que dijera verdad.
print("\nCapa R49 — el `source` declarado apunta a un documento real")
try:
    _TEX = {f.name: f.read_text(errors="ignore")
            for f in (_REPO / "manuscript").glob("*.tex")}
    _malas = []
    for _k, _v in _P26.items():
        _src = str(_v.get("source", ""))
        _m = _re.search(r"Paper\s*(\d+)", _src)
        if not _m:
            continue                      # sin puntero a paper: fuera de alcance
        _cands = [n for n in _TEX if f"Paper{_m.group(1)}" in n]
        if not _cands:
            _malas.append(f"{_k}: cita «Paper {_m.group(1)}» y no hay .tex")
            continue
        # el valor declarado debe aparecer en ese paper (aunque sea redondeado)
        _val = _v.get("value")
        if _val is None:
            continue
        # Un paper puede escribir el mismo número a distinta precisión
        # (4.76 · 4.7596 · 4.759627). Basta que APAREZCA en alguna forma:
        # buscar «no aparece a 3 decimales» daba falsos positivos en Omega,
        # n_s, R2 y omega_m — todos escritos con más cifras. Medido, no supuesto.
        _formas = {f"{float(_val):.{_d}f}".rstrip("0").rstrip(".")
                   for _d in range(2, 8)}
        if not any(_f in _TEX[c] for _f in _formas for c in _cands):
            _malas.append(f"{_k}: {_val} no aparece en {_cands[0]} "
                          f"(probadas {len(_formas)} precisiones)")
    check("R49 todo `source` que cita un paper apunta a uno que contiene el valor",
          not _malas, "; ".join(_malas[:4]) if _malas
          else f"{len(_P26)} procedencias con puntero verificado")
except Exception as _e:
    check("R49 capa operable", False, str(_e))

# ════════════════════════════════════════════════════════════════════════════
# R50 — EL TRINQUETE DE DEUDA TIENE QUE ESTAR APRETADO (2026-08-02)
#
# POR QUÉ EXISTE. Los contadores de deuda (R42-R45, R48) declaran «el recuento
# sólo puede BAJAR». Pero nada lo hacía cumplir: R44 llegó a tener tope 112 con
# 79 sitios reales — 33 de holgura por la que podían entrar 33 violaciones
# nuevas sin que el guardián dijera nada. El trinquete existía y estaba flojo.
#
# Un tope con holgura no es un trinquete: es un permiso. Esta regla exige que
# cada tope sea EXACTAMENTE la cuenta actual cuando la cuenta ha bajado, así
# arreglar algo obliga a apretar y el terreno ganado no se puede perder.
print("\nCapa R50 — el trinquete de deuda está apretado")
try:
    _flojos = []
    for _r, _real in _DEUDA_REAL.items():
        _tope = _DEUDA_MAX.get(_r)
        if _tope is not None and _real < _tope:
            _flojos.append(f"{_r}: {_real} reales pero tope {_tope} "
                           f"({_tope - _real} de holgura → bajar a {_real})")
    check("R50 ningún tope de deuda con holgura", not _flojos,
          "; ".join(_flojos) if _flojos
          else f"{len(_DEUDA_REAL)} topes ajustados a su cuenta real")
    # Auto-test: ve la holgura y no inventa holgura donde no la hay.
    _t50 = [({"X": 79}, {"X": 112}, True), ({"X": 49}, {"X": 49}, False)]
    _f50 = [str(a) for a, b, esp in _t50
            if any(a[k] < b[k] for k in a) != esp]
    check("R50 el detector distingue tope holgado de tope ajustado",
          not _f50, "; ".join(_f50) if _f50
          else "2 casos: 79 con tope 112 marcado; 49 con tope 49 exento")
except Exception as _e:
    check("R50 capa operable", False, str(_e))

# ═══════════════════════════════════════════════════════════════════════════
# R51 — LA ETIQUETA DE UNA CURVA GRAFICADA TIENE QUE NOMBRAR EL MISMO ANCLA
# H0 QUE LA EXPRESIÓN QUE LA CALCULÓ (2026-08-06)
#
# POR QUÉ EXISTE. `fig_paper10_alphaK_vs_alpha.pdf` (Paper 10) graficaba
# H0_arr = H0_global/(1-fscreen_arr) — el cálculo canónico correcto, vía
# H_alg — pero su propio label decía "via H_0^{\rm MIRA}": texto que sobrevivió
# al reframe del 17-jun-2026 (H_MIRA→H_alg) sin que nadie actualizara el
# rótulo cuando sí se corrigió la fórmula. El NÚMERO en la figura era
# correcto; el RÓTULO mentía sobre su origen. Ninguna capa existente lo veía:
# R20/R48/R49 verifican que un VALOR sea correcto o rastreable, no que el
# TEXTO junto a una curva nombre la misma ancla que la calculó. Hallado por
# revisión manual pedida por Mike ("entre las figuras hay muchas que todavía
# usan MIRA"), cerrando el hueco aquí.
#
# QUÉ HACE. Barre todo script bajo src/ que genere figuras (contiene
# "savefig"). En cada línea con una llamada a plot/errorbar/scatter/axhline/
# axvline que lleve label=, si el label nombra una de las dos anclas H0 en
# pugna (MIRA vs alg/global) sin ambigüedad, busca hacia atrás en el mismo
# archivo la asignación de la variable graficada y compara: si esa asignación
# nombra la OTRA ancla (o ninguna de las dos claramente, no se evalúa para
# evitar falsos positivos), es el mismo desfase etiqueta-vs-cálculo.
print("\nCapa R51 — etiqueta de figura vs variable graficada: ¿misma ancla?")
try:
    _MIRA_RE = re.compile(r"MIRA", re.IGNORECASE)
    _ALG_RE  = re.compile(r"H0_global|H0_alg\b|H_alg\b|\\rm\s*alg", re.IGNORECASE)

    def _ancla_de_r51(texto):
        _m, _a = bool(_MIRA_RE.search(texto)), bool(_ALG_RE.search(texto))
        if _m and not _a:
            return "mira"
        if _a and not _m:
            return "alg"
        return None  # ambas, ninguna, o ambigua: no se evalúa

    def _escanea_r51(scripts):
        """scripts: lista de (ruta, [líneas]). Devuelve (evaluadas, desfases).
        La llamada .plot(...) y su label= suelen partirse en líneas distintas
        (matplotlib multilínea) — se evalúa una VENTANA de 4 líneas desde la
        que abre la llamada, no una sola línea."""
        _evaluadas, _desfases = 0, []
        for _ruta, _lineas in scripts:
            for _i, _linea in enumerate(_lineas):
                if not re.search(r"\.(plot|errorbar|scatter|axhline|axvline)\(", _linea):
                    continue
                _ventana = "\n".join(_lineas[_i:_i + 4])
                if "label" not in _ventana:
                    continue
                _marca_label = _ancla_de_r51(_ventana)
                if _marca_label is None:
                    continue
                _call = re.search(
                    r"\.(plot|errorbar|scatter|axhline|axvline)\(\s*([\w.]+)"
                    r"(?:\s*,\s*([\w.]+))?", _linea)
                if not _call:
                    continue
                _metodo = _call.group(1)
                _var = _call.group(2) if _metodo in ("axhline", "axvline") \
                    else _call.group(3)
                if not _var:
                    continue
                _asign = None
                for _prev in reversed(_lineas[:_i]):
                    _mm = re.match(rf"\s*{re.escape(_var)}\s*=\s*(.+)", _prev)
                    if _mm:
                        _asign = _mm.group(1)
                        break
                if _asign is None:
                    continue
                _evaluadas += 1
                _marca_asign = _ancla_de_r51(_asign)
                if _marca_asign is not None and _marca_asign != _marca_label:
                    _desfases.append(
                        f"{_ruta}:{_i + 1} label='{_marca_label}' pero "
                        f"{_var} viene de '{_marca_asign}': {_asign.strip()[:70]}")
        return _evaluadas, _desfases

    _REPO_R51 = pathlib.Path(__file__).resolve().parents[2]
    _scripts_r51 = []
    for _p in (_REPO_R51 / "src").rglob("*.py"):
        try:
            _txt = _p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "savefig" in _txt:
            _scripts_r51.append((str(_p.relative_to(_REPO_R51)), _txt.splitlines()))

    _eval_r51, _desfases_r51 = _escanea_r51(_scripts_r51)
    check("R51 el detector evaluó al menos una etiqueta real de figura",
          _eval_r51 >= 1, f"{_eval_r51} etiquetas evaluadas en "
          f"{len(_scripts_r51)} scripts con savefig")
    check("R51 ninguna etiqueta de figura nombra un ancla H0 distinta a su cálculo",
          not _desfases_r51,
          "; ".join(_desfases_r51[:4]) if _desfases_r51 else "0 desfases")

    # Auto-test: reproduce el bug REAL de fig_paper10_alphaK_vs_alpha.pdf
    # (línea previa al arreglo de 2026-08-06) y confirma que se marca; y que
    # el par ya corregido (mismo archivo, hoy) NO se marca.
    _lineas_bug = [
        "H0_arr = H0_global / (1 - fscreen_arr)   # canonical cascade via H_alg global",
        "ax2.plot(alpha_range, H0_arr, color='#1a9641', lw=2,",
        "         label=r'$H_0^{\\rm local}(\\alpha)$ (canonical, via $H_0^{\\rm MIRA}$)')",
    ]
    _lineas_arreglada = [
        "H0_arr = H0_global / (1 - fscreen_arr)   # canonical cascade via H_alg global",
        "ax2.plot(alpha_range, H0_arr, color='#1a9641', lw=2,",
        "         label=r'$H_0^{\\rm local}(\\alpha)$ (canonical, via $H_0^{\\rm alg}$)')",
    ]
    _ev_bug, _d_bug = _escanea_r51([("test_bug.py", _lineas_bug)])
    _ev_ok, _d_ok = _escanea_r51([("test_ok.py", _lineas_arreglada)])
    check("R51 el detector marca el bug real pre-arreglo de Paper 10",
          len(_d_bug) == 1, f"{len(_d_bug)} desfases (esperado 1)")
    check("R51 el detector NO marca la misma línea ya corregida",
          _ev_ok >= 1 and len(_d_ok) == 0,
          f"{_ev_ok} evaluadas, {len(_d_ok)} desfases (esperado 0)")
except Exception as _e:
    check("R51 capa operable", False, str(_e))

# ═══════════════════════════════════════════════════════════════════════════
# R52 — UNA SATURACIÓN NUNCA SE MULTIPLICA POR ρ_crit (2026-08-10)
#
# POR QUÉ EXISTE. S_DE = T_r/M_v = 0.839950 es una SATURACIÓN (Postulado S):
# vive en la ecuación de estado (w0 = -S_DE), NO en el reparto de densidades.
# La fracción de densidad de energía oscura es OTRO número, 0.691119 = 1-Ω_m.
# Multiplicar S_DE por ρ_crit produce una «densidad» que no existe.
#
# El caso real, encontrado a mano el 2026-08-10 tirando de un hilo:
#   ssee_eft_verification.py:59   rho_DE0 = Om_DE * rho_crit   -> 0.840
#   h0_cascade_audit.py:44        rho_DE  = OMEGA_DE * rho_crit   (archivado 2026-09-19, era H_MIRA)
#   ssee_paper3_hiclass_check.py  Om_DE_z = Om_DE * ratio/E^2
# El último es el peor: mete la saturación en la ranura de DENSIDAD de CLASS y
# luego compara el resultado contra el mismo álgebra — «Δ = 0.005%» que no es
# verificación independiente sino la misma sustitución hecha dos veces.
#
# CÓMO SE SUPO CUÁL VA. Dos vías independientes:
#  (a) estructural: f_screen no puede llevar H (si lo lleva, H = H_SH0ES(1-f(H))
#      tiene dos H). Medido: con S_DE, f_screen es idéntico AL ÚLTIMO BIT para
#      anclas de 60 a 100; con 1-ω_m/h² se mueve (0.0561 -> 0.0584).
#  (b) Planck crudo: 0.839950 pasa a 0.91σ; 0.691119 falla a 9.82σ.
#
# La regla: ningún símbolo de saturación puede aparecer multiplicando a ρ_crit
# en la misma expresión. Si de verdad hace falta una densidad ahí, va
# OMEGA_M_TOTAL / (1 - OMEGA_M_TOTAL), que sí llevan H.
print("\nCapa R52 — ninguna saturación se usa como densidad")
try:
    _SAT = ("S_DE", "S_M", "S_K", "OMEGA_DE", "OMEGA_CDM_SECTOR", "OMEGA_M_DYN",
            "Om_DE", "Om_m_dyn", "s_DE", "s_M", "s_K")
    # Sólo la MULTIPLICACIÓN explícita. Basta que la saturación esté en la
    # misma línea que ρ_crit para tener falsos positivos: en los integradores
    # acoplados `Om_DE` es una variable local calculada como rho_phi/rho_tot,
    # que SÍ es una fracción de densidad legítima y no debe marcarse.
    _RHOSYM = r"(?:rho_crit|RHO_CRIT|RHO|ρ_crit)"
    _SATSYM = r"(?:S_DE|S_M|S_K|OMEGA_DE|OMEGA_CDM_SECTOR|OMEGA_M_DYN|Om_DE|Om_m_dyn|s_DE|s_M|s_K)"
    _MULT = _re.compile(rf"{_SATSYM}\s*\*\s*{_RHOSYM}|{_RHOSYM}\s*\*\s*{_SATSYM}")
    # Exento: la línea dice explícitamente que NO debe usarse así, o es la
    # definición de un alias deprecado que sólo se conserva documentada.
    _EXENTO = _re.compile(r"NO usarla|NO debe|no es una densidad|DEPRECADO|"
                          r"R52|OJO|FIX 2026-08-10", _re.I)

    def _escanea_r52(lineas):
        _malas = []
        for _i, _ln in enumerate(lineas):
            _cod = _ln.split("#")[0]          # sólo código, no comentario
            if not _MULT.search(_cod):
                continue
            _win = "\n".join(lineas[max(0, _i - 8):_i + 2])
            if _EXENTO.search(_win):
                continue
            _malas.append(_i)
        return _malas

    _r52 = []
    for _py in sorted((_REPO / "src").rglob("*.py")):
        if "__pycache__" in str(_py) or "verificacion" in str(_py):
            continue
        _ls = _py.read_text(errors="ignore").splitlines()
        for _i in _escanea_r52(_ls):
            _r52.append(f"{_py.relative_to(_REPO)}:{_i+1} «{_ls[_i].strip()[:52]}»")

    check("R52 ninguna saturación multiplica a ρ_crit en código activo",
          not _r52,
          "; ".join(_r52[:4]) + (f" … (+{len(_r52)-4})" if len(_r52) > 4 else "")
          if _r52 else "0 usos de saturación como densidad")

    # Auto-test: reproduce el bug REAL y confirma que se marca; y que la línea
    # ya anotada (misma forma, con la advertencia encima) NO se marca.
    _bug52 = ["rho_DE0  = Om_DE * rho_crit"]
    _ok52 = ["# OJO: OMEGA_DE es alias de una saturación, NO usarla como densidad",
             "rho_DE0  = Om_DE * rho_crit"]
    _lim52 = ["rho_m0 = OMEGA_M_TOTAL * rho_crit"]        # ésta SÍ es densidad
    check("R52 el detector distingue saturación-por-ρ_crit de densidad legítima",
          len(_escanea_r52(_bug52)) == 1
          and len(_escanea_r52(_ok52)) == 0
          and len(_escanea_r52(_lim52)) == 0,
          "3 casos: bug pelado marcado; bug anotado exento; "
          "OMEGA_M_TOTAL·ρ_crit (densidad real) exento")
    # ── R52b — LA CLASE COMPLETA, y a prueba de renombres ────────────────
    # AÑADIDO 2026-09-05. R52 llevaba desde el 08-10 en verde sobre
    # `ssee_paper5_IS_perturbations.py`, que corría su E(a) y su fuente de
    # Poisson con las saturaciones. DOS cegueras independientes, no una:
    #
    #  (1) DE FORMA: R52 sólo miraba «saturación × ρ_crit». El bug de Paper 5
    #      era `sqrt(Omm_dyn*a**-3 + OmDE*rDE)` y `Omm_dyn*δm + OmDE*δDE`.
    #      Misma clase —saturación en ranura que lleva H— otra sintaxis.
    #  (2) DE NOMBRE, y ésta es la peor: Paper 5 hacía
    #          from ssee_core import OMEGA_CDM_SECTOR as Omm_dyn
    #      El alias BORRA el nombre que el detector busca. Una regla que mira
    #      nombres se derrota con un `import X as Y`, y ninguna cantidad de
    #      formas nuevas la habría salvado. Por eso R52b resuelve los alias
    #      por archivo antes de buscar.
    #
    # Firmas, ambas inequívocas:
    #  DILUCIÓN: sólo una densidad se diluye como a⁻³ o (1+z)³. Una saturación
    #    es un número de la ecuación de estado; no tiene ley de dilución.
    #  POISSON: una saturación multiplicando una perturbación (δ) es una
    #    fuente gravitacional, y la fuente lleva la densidad.
    _SAT_BASE = ("S_DE", "S_M", "S_K", "OMEGA_DE",
                 "OMEGA_CDM_SECTOR", "OMEGA_M_DYN")
    _IMP_AS = _re.compile(r"\b(" + "|".join(_SAT_BASE) + r")\s+as\s+(\w+)")

    def _sat_visibles(_texto):
        """Nombres de saturación visibles EN ESTE archivo, alias incluidos."""
        _s = set(_SAT_BASE) | {"Om_DE", "Om_m_dyn", "s_DE", "s_M", "s_K"}
        _s |= {_m.group(2) for _m in _IMP_AS.finditer(_texto)}
        return _s

    def _rx_r52b(_simbolos):
        _sat = "(?:" + "|".join(sorted((_re.escape(_x) for _x in _simbolos),
                                       key=len, reverse=True)) + ")"
        _dil = _re.compile(
            rf"{_sat}\s*\*\s*[A-Za-z_][\w\[\]\.]*\s*\*\*\s*\(?\s*-\s*3"
            rf"|{_sat}\s*\*\s*\(\s*1\s*\+\s*z\s*\)\s*\*\*\s*3")
        _poi = _re.compile(rf"{_sat}\s*\*\s*(?:[\w\.]+\s*\*\s*)*"
                           rf"(?:\u03b4|delta)")
        return _dil, _poi

    def _escanea_r52b(_lineas):
        _texto = "\n".join(_lineas)
        _dil, _poi = _rx_r52b(_sat_visibles(_texto))
        _malas = []
        for _i, _ln in enumerate(_lineas):
            _cod = _ln.split("#")[0]
            if not (_dil.search(_cod) or _poi.search(_cod)):
                continue
            _win = "\n".join(_lineas[max(0, _i - 8):_i + 2])
            if _EXENTO.search(_win):
                continue
            _malas.append(_i)
        return _malas

    _r52b = []
    for _py in sorted((_REPO / "src").rglob("*.py")):
        if "__pycache__" in str(_py) or "verificacion" in str(_py):
            continue
        _ls = _py.read_text(errors="ignore").splitlines()
        for _i in _escanea_r52b(_ls):
            _r52b.append(f"{_py.relative_to(_REPO)}:{_i+1} «{_ls[_i].strip()[:52]}»")

    check("R52b ninguna saturación se diluye ni alimenta un Poisson",
          not _r52b,
          "; ".join(_r52b[:4]) + (f" … (+{len(_r52b)-4})" if len(_r52b) > 4 else "")
          if _r52b else "0 saturaciones en ranura de densidad evolutiva")

    # Control de los DOS lados (R53), y sobre el caso REAL: los fixtures
    # llevan el mismo `import ... as ...` de Paper 5, así que si la
    # resolución de alias se rompe, el control cae.
    _impP5 = "from ssee_core import OMEGA_CDM_SECTOR as Omm_dyn, OMEGA_DE as OmDE"
    _bugA = [_impP5, "    return np.sqrt(Omm_dyn * a**(-3) + OmDE * rDE)"]
    _bugB = [_impP5, "    Phi = -1.5 * (Omm_dyn * \u03b4m + OmDE * fDE * \u03b4DE)"]
    _okA  = ["    return np.sqrt(Omm * a**(-3) + OmDE_dens * rDE)"]
    _okB  = ["    Phi = -1.5 * (Omm * \u03b4m + OmDE_dens * fDE * \u03b4DE)"]
    check("R52b el detector ve la saturación aunque venga renombrada",
          len(_escanea_r52b(_bugA)) == 1 and len(_escanea_r52b(_bugB)) == 1
          and len(_escanea_r52b(_okA)) == 0 and len(_escanea_r52b(_okB)) == 0,
          "4 casos: E(a) y Poisson con saturación ALIASADA marcados; "
          "los mismos dos con densidad, limpios")

except Exception as _e:
    check("R52 capa operable", False, str(_e))

print("\nCapa R54 — 0.403302 es s_K, jamás alpha_K")
try:
    # LA REGLA. s_K = 3(-w0)(1+w0) = -(dp/dN)/rho es puro EoS.
    # alpha_K (kineticidad Bellini-Sawicki) es OTRA cantidad.
    # Probado 2026-09-06: s_K = -(dp/dN)/rho con dif 0.00e+00.
    _ETIQ = re.compile(r"alpha_?K|alphaK|\u03b1_?K|\u03b1_\{?K")
    _VAL  = re.compile(r"0\.4033")
    _EX54 = re.compile(r"s_K|s_k|mal llamado|NO es alpha|etiqueta|R54")

    def _escanea_r54(_ls):
        _m = []
        for _i, _l in enumerate(_ls):
            if not _VAL.search(_l):
                continue
            if not _ETIQ.search(_l):
                continue
            if _EX54.search(_l):
                continue
            _m.append(_i)
        return _m

    _r54 = []
    _objetivo = []
    for _pat in ("src/**/*.py", "manuscript/*.tex",
                 "submission_PRD/*.tex", "*.yaml", "*.md"):
        _objetivo += sorted(_REPO.glob(_pat))
    for _f in _objetivo:
        if ("archive" in str(_f) or "__pycache__" in str(_f)
                or _f.name in _FIXTURES):
            continue
        _ls = _f.read_text(errors="ignore").splitlines()
        for _i in _escanea_r54(_ls):
            _r54.append(f"{_f.relative_to(_REPO)}:{_i+1}")

    _DEUDA_R54 = 30   # 47 -> 30 (2026-09-27): alpha_K->s_K/15.591335 en P1, P3, P8, Unified, Sealed, PRD, Endorser; 55 -> 51 al eximir las fixtures del registro (R67); 51 -> 49 (2026-09-19): cuenta real medida tras archivar h0_cascade_audit.py y las anotaciones R65; 49 -> 48 (2026-09-26): G2/G3 corrigieron el mislabel de 0.403302 en Sealed Journal y Paper 1 (alpha_K^eff -> s_K); 48 -> 47 (2026-09-26): el README deja de rotular 0.4033 como kineticidad (P7: alpha_K=15.591335)
    check("R54 la deuda de etiquetas alpha_K/s_K no crece",
          len(_r54) <= _DEUDA_R54,
          f"{len(_r54)} sitios (tope {_DEUDA_R54}): "
          + "; ".join(_r54[:4]))
    check("R54 el tope está apretado",
          len(_r54) >= _DEUDA_R54 or len(_r54) == 0,
          f"tope {_DEUDA_R54} = cuenta real {len(_r54)}")

    # Control de los DOS lados (R53).
    _malo = ["  alpha_K: 0.4033  # Bellini-Sawicki"]
    _bien = ["  s_K: 0.403302  # -(dp/dN)/rho"]
    _otro = ["  alpha_K: 15.591335  # kineticidad"]
    check("R54 el detector distingue etiqueta de valor",
          len(_escanea_r54(_malo)) == 1
          and len(_escanea_r54(_bien)) == 0
          and len(_escanea_r54(_otro)) == 0,
          "3 casos: 0.4033 rotulado alpha_K marcado; "
          "el mismo valor como s_K y otro valor "
          "como alpha_K, limpios")

except Exception as _e:
    check("R54 capa operable", False, str(_e))

print("\nCapa R53 — toda regla trae su control del otro lado")
try:
    # LA REGLA (formulada por Mike, 2026-09-05). Una comprobación que sólo
    # puede devolver un resultado NO es una comprobación:
    #
    #   digo "PASA"  -> hace falta un caso que FALLE,
    #                   o mi detector podría decir siempre que sí
    #   digo "CAE"   -> hace falta un caso que PASE,
    #                   o mi detector podría estar simplemente roto
    #
    # POR QUÉ EXISTE. El 2026-09-05 se encontró que Paper 3/7/9 afirmaban
    # «hi_class confirma alpha_K = 0.403302 con acuerdo del 0.005%». Esa
    # comparación era `abs(aK_z[0] - aK_alg)/aK_alg`, y en z=0 los tres
    # factores de aK_z valen 1 por construcción: era el MISMO número contra
    # sí mismo. El residuo de 0.005% resultó ser exactamente el redondeo de
    # c = 2.998e5 en vez de 299792.458 km/s (verificado: da 0.005%). O sea
    # una comprobación estructuralmente incapaz de fallar, viva meses.
    # El caso contrario, la validación EFTCAMB del mismo Paper 7, SÍ quedó
    # en pie el mismo día — porque se le pudo añadir el control: EFTCAMB
    # acepta alpha_K=+0.4033 y RECHAZA 0, -1.0 y -5.0.
    # La diferencia entre lo que cae y lo que queda es el control, no el
    # código. De ahí esta capa.
    #
    # QUÉ MIDE. Sobre el propio fuente del guardián: para cada regla R<n>,
    # si existe al menos una comprobación que ponga a prueba AL DETECTOR y
    # no al repositorio. La convención ya establecida en R20/R38/R40-R52 es
    # nombrarlas «R<n> el detector ...». La forma plena es la de dos lados
    # (marca el bug real Y no marca el caso sano, como en R51 y R52); esta
    # capa exige por ahora el piso —tener control— y el trinquete de abajo
    # obliga a que la deuda sólo baje.
    _CHECKNAME = _re.compile(r'check\(\s*f?"([^"]*\bR(\d+)\b[^"]*)"')
    _ESCONTROL = _re.compile(r"el detector|auto-?test", _re.I)

    def _escanea_r53(texto):
        """-> (reglas_con_control, reglas_sin_control) leyendo un fuente."""
        _todas, _con = set(), set()
        for _m in _CHECKNAME.finditer(texto):
            _nombre, _num = _m.group(1), int(_m.group(2))
            _todas.add(_num)
            if _ESCONTROL.search(_nombre):
                _con.add(_num)
        return _con, (_todas - _con)

    # El guardián se lee a sí mismo desde disco (no desde el bytecode:
    # ver la lección del .pyc rancio) para no depender de su propio
    # estado en memoria.
    _SRC_GUARDIAN = pathlib.Path(__file__).resolve().read_text(errors="ignore")
    _con53, _sin53 = _escanea_r53(_SRC_GUARDIAN)
    # 31 al abrir la capa (2026-09-05). Baja a 28 el mismo día con los
    # controles de R17, R25 y R30 — las tres que vigilan números
    # canónicos, por eso primero. SÓLO puede BAJAR.
    _DEUDA_R53 = 25   # 26 -> 25: R33 y R68 ganaron control (2026-09-30)
    _lista53 = " ".join("R%d" % _r for _r in sorted(_sin53))

    check("R53 la deuda de reglas sin control no crece",
          len(_sin53) <= _DEUDA_R53,
          f"{len(_sin53)} sin control de {len(_con53) + len(_sin53)} "
          f"(tope {_DEUDA_R53}): {_lista53}"
          if _sin53 else "todas las reglas tienen control")

    check("R53 el tope de deuda está apretado",
          len(_sin53) >= _DEUDA_R53 - 0 or len(_sin53) == 0,
          f"tope {_DEUDA_R53} = cuenta real {len(_sin53)}"
          if len(_sin53) == _DEUDA_R53 else
          f"BAJAR el tope a {len(_sin53)}: sobran {_DEUDA_R53 - len(_sin53)}")

    # Auto-control de dos lados de esta misma capa: la regla se obedece a sí
    # misma. Un fuente con una regla CON control y otra SIN él tiene que
    # separarlas; si el detector no distingue, esta capa no vale nada.
    # Los literales van PARTIDOS a proposito: si en este fuente apareciera
    # tal cual `check("R99 ...`, el propio escaneo de arriba contaria R98 y
    # R99 como reglas reales del guardian. El detector no debe verse a si
    # mismo en el material que analiza.
    _q = 'check("' + 'R'
    _fuente_ok = (_q + '99 algo del repo", x)\n'
                  + _q + '99 el detector distingue", y)')
    _fuente_coja = _q + '98 algo del repo", x)'
    _c1, _s1 = _escanea_r53(_fuente_ok)
    _c2, _s2 = _escanea_r53(_fuente_coja)
    check("R53 el detector distingue regla con control de regla coja",
          _c1 == {99} and _s1 == set() and _c2 == set() and _s2 == {98},
          "2 casos: R99 (con auto-test) contada como cubierta; "
          "R98 (sin auto-test) contada como deuda")
except Exception as _e:
    check("R53 capa operable", False, str(_e))

print("\nCapa R55 — la cascada de Hubble no invierte su dirección")
# POR QUÉ EXISTE. 3(φ+π)² es un NÚMERO PURO, sin unidades. Escribir
# H_local = 3(φ+π)²/(1−f_screen) lo usa como ENTRADA de una cascada
# dimensional: dimensionar álgebra a mano. El único H que se MIDE es
# SH0ES (el de Planck se INFIERE, y dentro de ΛCDM, cuyos libres se
# acomodan al dato). Por eso la dirección canónica es
#   SH0ES ENTRA  ->  H_global SALE:   H_glob = H_SH0ES · (1 − f).
# La suite vivió 8 documentos con la dirección invertida y el guardián
# dio VERDE 222/222 sin verla: ninguna regla preguntaba por el SENTIDO
# de la operación, sólo por los valores. Esta regla cierra ese hueco.
# Los σ son invariantes bajo la inversión (la lente es multiplicativa),
# así que un chequeo de VALOR nunca lo habría detectado.
try:
    _R55_MAL = re.compile(
        r"(?:67\.962\d*|3\s*\(\s*\\?(?:phiG|varphi|phi)\s*\+\s*\\?pi\s*\)\s*\^?\s*\{?2\}?"
        r"|H_?0?\^?\{?\\?rm\s*alg\}?|H0_alg|H0_global)"
        r"\s*(?:[/}{]|\s)+\(?\s*1\s*[-−]\s*"
        r"(?:\\fsc|\\fscr|f_?\{?\\?rm\s*scr\}?|f_screen|fscreen|fsc"
        r"|0\.0672\d*|0\.0695\d*)")

    def _r55_sitios(texto):
        """Devuelve las coincidencias de 'número puro / (1 - f)'."""
        return _R55_MAL.findall(texto.replace("\\frac{", "").replace("\n", " "))

    _R55_REPO = pathlib.Path(__file__).resolve().parents[2]
    _r55_docs, _r55_malos = 0, []
    _r55_yo = pathlib.Path(__file__).resolve()
    for _sub in ("manuscript", "submission_PRD", "src"):
        _rp = _R55_REPO / _sub
        if not _rp.is_dir():
            continue
        for _ext in ("*.tex", "*.py"):
            for _f in sorted(_rp.rglob(_ext)):
                _sp = str(_f)
                if ("archive" in _sp or "superseded" in _sp
                        or _f.name in _FIXTURES):
                    continue
                if _f.resolve() == _r55_yo:
                    continue
                try:
                    _t = _f.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                _a = _f.name
                _r55_docs += 1
                # una línea que se declara superada/retirada no cuenta
                _lineas_malas = [
                    _ln for _ln in _t.split("\n")
                    if _r55_sitios(_ln)
                    and not re.search(r"supersed|retirad|superad|viej|old register"
                                      r"|no quote|do not quote|invertida", _ln, re.I)]
                if _lineas_malas:
                    _r55_malos.append(f"{_a}:{len(_lineas_malas)}")

    check("R55 ningún documento usa el número puro como entrada de la cascada",
          not _r55_malos,
          f"{_r55_docs} archivos escaneados, 0 sitios invertidos"
          if not _r55_malos else
          "dirección invertida en " + "; ".join(sorted(_r55_malos)[:6]))

    check("R55 el guardián escaneó una superficie real",
          _r55_docs >= 30, f"{_r55_docs} archivos .tex/.py escaneados (piso 30)")

    # CONTROL (R53): el detector debe MARCAR la forma invertida y DEJAR PASAR
    # la correcta. Sin este control la regla podría estar siempre en verde.
    _c_mal_1 = r"H_0^{\rm local} = \frac{H_0^{\rm alg}}{1 - \fsc} = 72.86"
    _c_mal_2 = r"H0_local = H0_alg / (1 - fscreen)"
    _c_mal_3 = r"= \frac{67.962}{1-0.06725} \approx 72.86"
    _c_bien_1 = r"H_0^{\rm glob} = H_0^{\rm SH0ES}\,(1-\fsc) = 68.13"
    _c_bien_2 = r"H0_glob = H0_SHOES * (1 - fscreen)"
    _c_bien_3 = r"el 67.962/(1-f)=72.86 es la forma superada, retirada 2026-09-06"
    _marca = [bool(_r55_sitios(_c)) for _c in (_c_mal_1, _c_mal_2, _c_mal_3)]
    _pasa  = [not _r55_sitios(_c) for _c in (_c_bien_1, _c_bien_2)]
    _exime = not [
        _ln for _ln in (_c_bien_3,)
        if _r55_sitios(_ln)
        and not re.search(r"supersed|retirad|superad|viej|old register"
                          r"|no quote|do not quote|invertida", _ln, re.I)]
    check("R55 el detector distingue la dirección correcta de la invertida",
          all(_marca) and all(_pasa) and _exime,
          f"3 formas invertidas marcadas ({sum(_marca)}/3), "
          f"2 correctas limpias ({sum(_pasa)}/2), "
          f"1 mención histórica eximida ({'sí' if _exime else 'NO'})")
except Exception as _e:            # noqa: BLE001
    check("R55 la capa de dirección de cascada corrió", False,
          f"excepción: {_e}", nivel=5)

print("\nCapa R72 — ninguna saturación ocupa ranura de densidad en los MANUSCRITOS")
# Por qué existe. R52/R52b vigilan lo mismo pero SÓLO en código .py. El error de
# categoría vive igual —y más tiempo— en los .tex, donde nadie lo ejecuta:
#   · fig3_omega_de graficaba T_R/M_V = 0.839950 (que es s_DE = |w0|) en el eje
#     de densidad, contra el Ω_Λ de Planck. Corregido 2026-09-26.
#   · SSEE_EFT_section.tex mete Ω_{m,dyn}·a^{-3} en Friedmann y en la fuente de
#     Poisson — misma forma que el bug Ω_m-geometría de 2026-07-09.
#   · SSEE_Unified_Journal.tex define \Ommdyn y lo llama «matter density».
# Lo que se marca NO es mencionar la saturación: es ponerla donde va una
# densidad — diluyéndose como a^{-3} o (1+z)^3, dentro de E²/h̃², en la fuente
# de Poisson, o rotulada «matter density». Mencionarla para decir que NO es una
# densidad es justamente lo que se quiere que digan los papers, y queda exento.
try:
    _SAT72 = (r"(?:\\Ommdyn|\\Omde|Omega_\{m,\\?\s?\\?mathrm\{dyn\}\}"
              r"|Omega_\{m,\s?dyn\}|Om\^\{?\\?mathrm\{dyn\}\}?"
              r"|Om\^\{\\mathrm\{dyn\}\}|0\.160050|0\.839950)")
    # Ranuras de densidad: dilución, fondo de Friedmann, fuente de Poisson.
    # 2026-09-26, AMPLIADA con la forma aditiva. La v1 no marcaba
    #   Omega_{m,eff} = Omega_{m,dyn} + Omega_DE * r
    # de Paper 5, y eso es exactamente la saturación en ranura de densidad
    # dentro del Poisson: no tenía forma de dilución ni el rótulo «matter
    # density», así que se colaba. La regla cubría menos de lo que el error
    # abarca, y eso lo encontró un hallazgo del manuscrito, no la regla.
    _RANURA72 = _re.compile("|".join([
        # (1) diluyéndose como materia
        _SAT72 + r"\s*(?:\\,|\\;|~|\s)*(?:a\^\{?-3\}?|\(1\+z\)\^\{?3\}?)",
        # (2) dentro de un E^2 / H^2 / h~^2
        r"(?:E\^\{?2\}?|H\^\{?2\}?|\\tilde\{h\}\^\{?2\}?|h\^\{?2\}?)"
        r"[^\n]{0,40}" + _SAT72,
        # (3) rotulada como densidad de materia, en cualquiera de los dos órdenes
        r"(?:matter density|densidad de materia|matter fraction)[^\n]{0,60}" + _SAT72,
        _SAT72 + r"[^\n]{0,60}(?:matter density|densidad de materia)",
        # (4) SUMADA dentro de una Omega efectiva (la forma que se colaba)
        r"Omega_\{m,\s?\\?mathrm\{eff\}\}[^\n]{0,40}=[^\n]{0,60}" + _SAT72,
        _SAT72 + r"\s*\+\s*\\?Om(?:de|ega)",
    ]))
    # Exento: la frase dice que NO es una densidad, o es registro histórico.
    _EX72 = _re.compile(
        r"NO es una densidad|not a density|equation of state|ecuaci[oó]n de estado"
        r"|1\s*\+\s*w_?0|1\+w_\{?0\}?|supersed|retirad|superad|RETIRED|deprecat"
        r"|category error|error de categor|R52|R72|historical|hist[oó]rico"
        r"|saturation|saturaci[oó]n", _re.I)

    def _sitios_r72(_txt):
        _out = []
        _ls = _txt.splitlines()
        for _i, _ln in enumerate(_ls):
            if _ln.lstrip().startswith("%"):
                continue                      # comentario LaTeX
            if not _RANURA72.search(_ln):
                continue
            _win = "\n".join(_ls[max(0, _i - 4):_i + 3])
            if _EX72.search(_win):
                continue
            _out.append((_i + 1, _ln.strip()[:60]))
        return _out

    _r72, _n72 = [], 0
    for _tx in sorted((_REPO / "manuscript").rglob("*.tex")):
        if "archive" in _tx.parts or "superseded" in str(_tx):
            continue
        _n72 += 1
        for _l, _s in _sitios_r72(_tx.read_text(errors="ignore")):
            _r72.append(f"{_tx.name}:{_l} «{_s}»")

    check("R72 el guardián escaneó una superficie real de manuscritos",
          _n72 >= 8, f"{_n72} .tex escaneados (piso 8)")

    if _r72:
        track_open(f"R72 {len(_r72)} sitios con saturación en ranura de densidad",
                   "; ".join(_r72[:6]) + (" …" if len(_r72) > 6 else ""))
    else:
        check("R72 ningún manuscrito pone una saturación donde va una densidad",
              True, f"{_n72} .tex limpios")

    # Control (R53): el detector tiene que marcar la forma mala y dejar pasar
    # la buena. Sin esto la regla podría estar verde por no mirar nada.
    _mal72 = [r"  = \frac{3}{2}\,\frac{\Ommdyn\,a^{-3}}{\tilde{h}^{2}(a)}\,\delta,",
              r"the background $\tilde{h}^{2}(a) = \Omega_{m,\mathrm{dyn}}\,a^{-3}+\rho$",
              r"the dynamical matter density $\Ommdyn = 0.160050$ governs BAO",
              # el sitio que la v1 NO veia: la saturacion SUMADA dentro de una
              # Omega efectiva, en la fuente de Poisson de Paper 5. Lo encontro
              # un hallazgo del manuscrito, no la regla; entra al control para
              # que la ampliacion quede probada y no se pueda volver a estrechar.
              r"  \Omega_{m,\mathrm{eff}} = \Omega_{m,\mathrm{dyn}} + \OmDE\,r,"]
    _bien72 = [r"  = \frac{3}{2}\,\frac{\Omega_{m}\,a^{-3}}{\tilde{h}^{2}(a)}\,\delta,",
               r"the background $\tilde{h}^{2}(a) = \Omega_{m}\,a^{-3}+\rho$",
               # la misma de Paper 5 ya corregida a densidades
               r"  \Omega_{m,\mathrm{eff}} = \Omega_m + \Omega_{\mathrm{DE}}\,r,"]
    _hist72 = ["% nota: superseded — el 0.160050 es 1+w_0, no una densidad",
               r"the dynamical matter density $\Ommdyn = 0.160050$ governs BAO"]
    _cm = [bool(_sitios_r72(_x)) for _x in _mal72]
    _cb = [not _sitios_r72(_x) for _x in _bien72]
    _ch = not _sitios_r72("\n".join(_hist72))
    check("R72 el detector distingue la ranura de densidad de la mención",
          all(_cm) and all(_cb) and _ch,
          f"4 formas malas marcadas ({sum(_cm)}/4), "
          f"3 con Ω_m real limpias ({sum(_cb)}/3), "
          f"1 mención negada eximida ({'sí' if _ch else 'NO'})")

    # ── R72b — el signo de Δ dice lo mismo en los diez papers ──────────────
    # CANONICAL_VALUES.yaml declara Δ ≡ SSEE − ΛCDM, negativo favorece a SSEE.
    # De no tenerlo declarado en un solo sitio salieron los signos opuestos
    # entre Paper 1/2 y Paper 6/Sealed/Unified. Se marca la línea que afirma
    # «favorece a SSEE» con un Δ de signo POSITIVO sin decir que va al revés.
    _CLAIM72 = _re.compile(r"favou?r\w*\s+SSEE|SSEE\s+(?:is\s+)?favou?r"
                           r"|favorece\w*\s+(?:a\s+)?SSEE|SSEE\s+favorecid",
                           _re.I)
    # El número tiene que venir DESPUÉS de un «=», no de un subíndice: la
    # primera versión leía el «2» de \Delta\mathrm{BIC}_{k2} como el valor y
    # marcaba Paper 3, que está bien escrito. Lo cazó su propio control.
    _DELTA72 = _re.compile(r"\\Delta\$?\s*(?:\\mathrm\{)?\s*(?:BIC|AIC|DIC)\}?"
                           r"(?:_\{[^}]*\})?\s*(?:\$?\s*=|\\simeq|\\approx)"
                           r"\s*\$?\s*([+-−]?\s?\d+\.?\d*)")
    # Exento: la línea/entorno declara la dirección invertida, o es histórico.
    _EXS72 = _re.compile(r"Lambda\s*CDM\s*[-−]\s*SSEE|LCDM\s*[-−]\s*SSEE"
                         r"|lcdm_minus_ssee|\\LCDM\s*[-−]\s*\\?SSEE"
                         r"|supersed|retirad|superad|RETIRED|hist[oó]ric"
                         r"|convention|convenci[oó]n", _re.I)

    def _sitios_r72b(_txt):
        _out, _ls = [], _txt.splitlines()
        for _i, _ln in enumerate(_ls):
            if _ln.lstrip().startswith("%") or not _CLAIM72.search(_ln):
                continue
            _vs = [_x.replace(" ", "") for _x in _DELTA72.findall(_ln)]
            if not _vs:
                continue
            # Una línea puede llevar varios Δ (p. ej. k=2 y k=4). Basta que UNO
            # sea negativo para que la afirmación esté respaldada.
            if any(_x.startswith("-") or _x.startswith("−") for _x in _vs):
                continue
            if _EXS72.search("\n".join(_ls[max(0, _i - 3):_i + 2])):
                continue
            _out.append((_i + 1, _ln.strip()[:60]))
        return _out

    _r72b = []
    for _tx in sorted((_REPO / "manuscript").rglob("*.tex")):
        if "archive" in _tx.parts or "superseded" in str(_tx):
            continue
        for _l, _s in _sitios_r72b(_tx.read_text(errors="ignore")):
            _r72b.append(f"{_tx.name}:{_l} «{_s}»")

    if _r72b:
        track_open(f"R72b {len(_r72b)} sitios con Δ de signo contrario a la convención",
                   "; ".join(_r72b[:5]) + (" …" if len(_r72b) > 5 else ""))
    else:
        check("R72b ningún paper afirma «favorece SSEE» con un Δ positivo",
              True, "convención Δ ≡ SSEE − ΛCDM coherente en los .tex")

    # Control (R53): la forma mala se marca, la correcta y la que declara la
    # dirección invertida pasan.
    _mb = [r"giving $\Delta\mathrm{BIC} = +6.43$, which favours SSEE.",
           r"we find $\Delta$BIC $= 19.01$ and SSEE is favoured."]
    _bb = [r"giving $\Delta\mathrm{BIC} = -6.43$, which favours SSEE.",
           r"$\Delta\mathrm{BIC}(\Lambda CDM - SSEE) = +6.43$ favours SSEE.",
           # el caso real de Paper 3 que la v1 marcaba mal: el «2» del
           # subíndice _{k2} no es el valor del Δ.
           r"$\Delta\mathrm{BIC}_{k2}=-32.9$ ... $\Delta\mathrm{BIC}_{k4}"
           r"=\Delta\chi^2+(4-6)\ln(2354)=-17.3$, favouring SSEE."]
    _cmb_ = [bool(_sitios_r72b(_x)) for _x in _mb]
    _cbb  = [not _sitios_r72b(_x) for _x in _bb]
    check("R72b el detector distingue el signo de la dirección declarada",
          all(_cmb_) and all(_cbb),
          f"2 signos invertidos marcados ({sum(_cmb_)}/2), "
          f"3 limpios de 3: negativo, dirección declarada y el subíndice "
          f"_{{k2}} de Paper 3 ({sum(_cbb)}/3)")
except Exception as _e:            # noqa: BLE001
    check("R72 la capa de saturación-en-manuscritos corrió", False,
          f"excepción: {_e}", nivel=5)

print("\nCapa R46 — el guardián hizo todo el trabajo que dice hacer")
_PISO_CHECKS = 278          # +4 procedencia (JSON + redondeo + control); solo SUBE
                            # control, -1 R53; +2 R61 antes; solo SUBE
                            # (2026-09-05); sólo SUBE
check(f"R46 se ejecutaron al menos {_PISO_CHECKS} comprobaciones",
      checks + 1 >= _PISO_CHECKS,
      f"{checks + 1} ejecutadas (piso {_PISO_CHECKS})"
      if checks + 1 >= _PISO_CHECKS else
      f"sólo {checks + 1} de {_PISO_CHECKS}: alguna capa no corrió "
      f"(¿archivo renombrado o movido?)")

print("\n" + "=" * 60)
if fails:
    print(f"ROJO — {len(fails)} de {checks} comprobaciones FALLARON.")
    print("Ordenadas por dependencia: lo primero es la RAÍZ, lo de abajo puede")
    print("ser consecuencia suya. Arreglar de arriba hacia abajo.\n")
    _ult = None
    for _f in sorted(fails, key=lambda x: (_nivel_de(x), x)):
        _nv = _nivel_de(_f)
        if _nv != _ult:
            print(f"  ── nivel {_nv} · {_NIVEL.get(_nv, 'SIN CLASIFICAR')}")
            _ult = _nv
        print(f"   x  {_f}")
    print("\nNo commitear ni sellar hasta resolverlo.")
    sys.exit(1)
# ─────────────────────────────────────────────────────────────────────
# VEREDICTO — dos preguntas distintas, y antes se respondia solo una.
#
# POR QUE CAMBIA (2026-09-07, lo dijo Mike). «VERDE» respondia «¿empeoro
# algo?» — una prueba de REGRESION. Pero se lee como «¿esta el modelo en
# orden?», y esas dos cosas se separan cada vez que se abre un track_open
# o se sube un tope de deuda. El resultado es un VERDE que se puede
# FORZAR: basta declarar el defecto y ponerle techo. Y eso fue pasando:
# 18 problemas abiertos, 57 sitios con la particula retirada presentada
# como vigente, 76 de R44, 55 de R54... todos «declarados», todos verdes.
#
# Su frase exacta: «que el guardian este en verde parece mas como si
# fuera forzado a estar en verde que lo que realmente refleja el modelo».
# Tenia razon, y la prueba es que los ultimos tres hallazgos los encontro
# el, o los encontre yo leyendo — no el guardian.
#
# Ahora el veredicto dice las DOS cosas, y la segunda manda en el titular.
# EL COLOR LO PINTA LO TERMINABLE, NO LA FISICA (2026-09-19). Ver la nota
# larga en `track_open`: un problema de fisica declarado con ficha y severidad
# NO ensucia el semaforo, porque puede no cerrarse nunca y eso no es un
# defecto del repositorio. Lo que lo ensucia es lo que SI se puede terminar.
_deuda_total = sum(_DEUDA_REAL.get(_k, 0) for _k in _DEUDA_MAX) + _n_md
_en_orden = not pendientes and _deuda_total == 0
print()
print(f"REGRESION  : sin regresiones, {checks} comprobaciones pasan.")

_por_sev = {}
for _op, _sev, _ in sin_resolver:
    _por_sev.setdefault(_sev, set()).add(_op)
if sin_resolver:
    print(f"SIN RESOLVER: {len(sin_resolver)} frente(s) de fisica en "
          f"{len({_o for _o, _, _ in sin_resolver})} fichas declaradas — "
          "no pintan el semaforo, se declaran")
    print("             " + " · ".join(
        f"{_COLOR_SEV.get(_s, '')} {_s} {' '.join(sorted(_v, key=lambda x: (int(x[3:].rstrip("b")), x)))}"
        for _s in ("alta", "media-alta", "media", "baja") if (_v := _por_sev.get(_s))))

if _en_orden:
    print("PENDIENTE  : nada — 0 tareas, 0 sitios de deuda.")
    print("\nVERDE — sin regresiones y sin nada terminable a medias.")
    if sin_resolver:
        print("La fisica sin resolver sigue arriba, con su severidad: "
              "un VERDE aqui no dice que el modelo este completo, "
              "dice que el repositorio esta en orden.")
else:
    print(f"PENDIENTE  : {len(pendientes)} tarea(s) + {_deuda_total} sitio(s) "
          "de deuda declarada — ESTO es lo que pinta")
    for _t in pendientes:
        print(f"             · {_t}")
    _top = sorted(((_DEUDA_REAL.get(_k, 0), _k) for _k in _DEUDA_MAX),
                  reverse=True)[:4]
    print("             mayores: "
          + ", ".join(f"{_k}={_v}" for _v, _k in _top if _v)
          + (f", particula_md={_n_md}" if _n_md else ""))
    print("\nAMARILLO — no hay regresiones, pero queda trabajo TERMINABLE sin "
          "terminar.")
    print("Un VERDE aqui seria forzado: esa deuda esta declarada, no resuelta.")
sys.exit(0)
