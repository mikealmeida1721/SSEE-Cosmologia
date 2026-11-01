# Protocolo de las 3 Memorias de SSEE

Las tres memorias son el **conocimiento colectivo** del modelo. Deben estar
siempre actualizadas y **sin discrepancia** entre ellas. Cada una tiene su
propósito (no se duplican):

| Memoria | Qué guarda | Dónde |
|---|---|---|
| **Guardián** | Resultados y valores (recomputa la física) | `VERIFICATION_LEDGER.md` + `src/verificacion/ssee_verify.py` |
| **Obsidian** | Conexiones, cadenas, dependencias (el *porqué* y *hasta dónde* de cada cambio) | `/home/mike/Documentos/SSEE/SSEE-Vault` |
| **CLAUDE.md** | Contexto/estado (continuar sin releer todo) | `CLAUDE.md` |

La fuente ÚNICA de los números es **`CANONICAL_VALUES.yaml`**. Si los tres no
concuerdan con él, hay *drift*.

---

## Cuando cambia un valor o se supera algo (orden obligatorio)

El cambio fluye en un solo sentido — **memorias → cajones → archivo** — para que
nada quede fuera de la mesa de trabajo. Hasta lo canónico de hoy puede superarse
mañana (si aparece algo más simple que cierre mejor sin abrir huecos); cuando eso
pasa, se aplica este mismo orden y lo viejo se conserva como prueba del esfuerzo.

**Fase A — Memorias primero (la fuente de verdad):**
1. **Verificar** la física (script que recomputa el nuevo valor → log en `results/logs/`).
2. **`CANONICAL_VALUES.yaml`** ← se actualiza PRIMERO. El valor viejo va a `retired:`
   con su razón (así el guardián lo caza si reaparece en cualquier cajón).
3. **Guardián** (`VERIFICATION_LEDGER.md` + check) → recomputa; el valor de pipeline
   debe tener log de procedencia (R9).
4. **Obsidian** (vault) → la nota del valor y **sus conexiones** (qué cadenas dependían).
5. **CLAUDE.md** → tablas de estado.

**Fase B — Cajones de trabajo (propagar y auditar):**
6. **`manuscript/`, `src/`, `docs/`** → propagar el nuevo valor a todo lo que lo usa.
   El guardián (Capas Manuscritos/Procedencia) verifica que no quede stale; los
   PDFs recompilan de `manuscript/`.

**Fase C — Archivar lo superado (con sello):**
7. Si un **artefacto entero** quedó obsoleto (script, PDF, doc, derivación), se mueve a
   `archive/` con **entrada en la Bitácora** (`archive/README.md`: qué, cuándo, por qué,
   qué lo reemplaza). La Capa Archivo del guardián exige que cada cajón archivado tenga
   entrada. Nada obsoleto se queda en un cajón vivo; nada se archiva en silencio.

> **Regla de cobertura:** todo cajón está en el **Mapa de Vigencia** (`archive/README.md`)
> como VIGENTE, ARCHIVO o TRABAJO. Si aparece un cajón nuevo, se clasifica.

---

## Contabilidad automática de propagación (el "dónde aparece cada canónico")

El cambio de un canónico se propaga de forma **sistemática**, no como texto plano.
La regla es: **DETECTAR todas las apariciones, recomputar/editar con cuidado cada una,
y verificar que ninguna quedó vieja** — nunca un buscar-reemplazar a ciegas (eso produce
el «1+1=3»: p. ej. un `sed 0.320→0.309` corrompe `0.3201→0.3091` y deja ecuaciones falsas
como `0.1601×1.9989=0.3089`).

**Cómo funciona la contabilidad:**
1. Al cambiar un valor en `CANONICAL_VALUES.yaml`, su valor viejo va a `retired:`
   (con un **patrón distintivo** — con unidad si el número suelto colisiona, p. ej.
   `0.659\,h` para no chocar con `wₐ=−0.659`).
2. `memory_sync.py` lee `retired:` y escanea **LEDGER + CLAUDE + `manuscript/*.tex` + vault**.
   Una corrida lista **cada lugar** (archivo:línea) donde un valor retirado quedó como
   vigente. Líneas con marca de contexto (`retired`, `superseded`, `earlier`, `superad`,
   `~~`, sección histórica…) se omiten — son historia legítima, no drift.
3. Se limpian en el **orden** de arriba (fuente → LEDGER → memorias → papers → vault).
4. **`memory_sync` VERDE = propagación completa.** Ese es el criterio de "no quedó número viejo".

Así, cambiar la fuente principal hace que el sistema **señale solo** dónde recomputar —
la propagación es sistemática y verificable de punta a punta.

---

## Cómo se revisa (rápido y barato)

```bash
# ¿La física + memorias + procedencia + manuscritos + archivo siguen íntegros?
.venv/bin/python3 src/verificacion/ssee_verify.py          # el guardián (una corrida, todas las capas)

# ¿Las 3 memorias Y los papers concuerdan con CANONICAL_VALUES.yaml?
.venv/bin/python3 src/verificacion/memory_sync.py          # LEDGER + CLAUDE + manuscript/*.tex + vault

# ¿El guardián mismo sigue detectando? (correr si TOCAS el guardián)
.venv/bin/python3 src/verificacion/test_guardian.py        # el vigilante vigilado
```

- `ssee_verify.py` → **VERDE/ROJO**: la física.
- `memory_sync.py` → **VERDE/DRIFT**: la coherencia entre memorias. Detecta
  cualquier valor de la lista `retired:` que aparezca **sin marca de contexto**
  (retirado, viejo, Type-P, coincidencia, sin re-correr…). Las secciones de
  registro histórico (logs de Sesión, POA, Fases) se omiten automáticamente.

El Guardián (`ssee_verify.py`) invoca a `memory_sync` como su **Capa de
Memorias**, así una sola corrida cubre física + coherencia.

---

## Checklist de cierre de sesión

- [ ] ¿Cambió algún valor? → seguir el orden de arriba (YAML → Guardián → Obsidian → CLAUDE).
- [ ] `ssee_verify.py` VERDE.
- [ ] `memory_sync.py` sin DRIFT (o drift conocido y anotado).
- [ ] Actualizar CLAUDE.md (tablas de estado) y la auto-memoria `~/.claude`.

---

*Por qué existe esto: el modelo crece y la propagación manual deja huecos. El
caso que lo motivó: el vault Obsidian quedó un mes desfasado (m_φ=5.71→36.95,
k_fs=0.493→0.659, cascada H₀) porque el Guardián vivía en el repo y nunca veía
el vault. Este protocolo + `memory_sync.py` cierran ese hueco.*
