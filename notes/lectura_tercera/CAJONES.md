# Cajones (raíz) — tercera lectura (agente CAJONES, 2026-10-10)
## Resumen
4 hallazgos: 0 contradicción · 2 retirado-vigente (H2 parcial, H3) · 2 valor-erróneo
(H1, H4) con el MISMO origen (Σm_ν rancio 0.06902 → Ω_m=0.30889, debería ser
Σm_ν=0.06849 → 0.308881) propagado en README.md, AUDIT.md y OPEN_PROBLEMS.md
(16 ocurrencias vigentes en total); RETRACTIONS.md y VERIFICATION_LEDGER.md están
limpios de este bug. No se revisaron a fondo: ACOMODO_POST_P6.md, COLA_CORRIDAS.md,
ESTADO_REVISION_CRECIMIENTO.md, EXTERNAL_AUDIT_PROMPTS.md, FUENTES_PENDIENTES.md,
HANDOFF_CLAUDE_pre_zenodo_2026-09-25.md, LECTURA_PAPERS.md, MEMORY_PROTOCOL.md,
NUMEROLOGY_AUDIT.md, PEER_REVIEW_PROMPT.md, PLAN_ORDEN.md, REGEN_LOGS.md,
RIGOR_CHECKLIST.md, CHANGELOG.md (grep de patrones sí, lectura completa no) ni el
cuerpo completo de VERIFICATION_LEDGER.md (1322 líneas, leídas ~180) ni de
OPEN_PROBLEMS.md (3268 líneas, leídas ~660 + grep del resto) ni de AUDIT.md (438
líneas, leídas ~80) por presupuesto de tiempo — quedan como pendiente de una pasada
más fina si el coordinador lo pide.
## Tabla por página
| archivo | estado | hallazgos # |
|---|---|---|
| README.md | ⚠ con hallazgos | H1, H2 |
| OPEN_PROBLEMS.md | ⚠ con hallazgos (parcial) | H4 |
| AUDIT.md | ⚠ con hallazgos (parcial) | H3 |
| RETRACTIONS.md | ✅ limpia | — |
| VERIFICATION_LEDGER.md | ✅ limpia (parcial, primeras 180 líneas) | — |
| CANONICAL_VALUES.yaml | ✅ fuente de verdad confirmada | — |
## Hallazgos

### H1 · README.md:32,189,207,241,261,273 · dimensión 1 (Valores) · valor-erróneo · confianza ALTA
- Dice: `Ω_m,CMB = 0.30889` (6 ocurrencias: líneas 32, 189, 207, 241, 261, 273).
- Debe decir: `0.308881` (o `0.30888` si se redondea a 5 decimales). CANONICAL_VALUES.yaml
  líneas 721-744 documenta explícitamente que **0.30889 es el valor RANCIO**: sale de
  Σm_ν=0.06902 (constante vieja); con el Σm_ν canónico 0.06849 el resultado exacto es
  0.308880879 → redondea a 0.308881 (o 0.30888, nunca 0.30889). Es justo el caso que
  originó la `rounding_policy` de ese archivo (157 sitios con el mismo bug, ya corregidos
  en 14 documentos — README quedó fuera de esa limpieza).
- Reemplazo propuesto: `0.30889` → `0.308881` en las 6 líneas. En la línea 261 (tabla MCMC
  Fase 4, columna "Algebraic") aplica igual: es el valor algebraico, no el posterior.

### H2 · README.md:186 · dimensión 1 (Valores) · retirado-vigente · confianza ALTA
- Dice: `ΔBIC (plik_lite point est., TTTEEE, k=2 vs k=6, N=613) | **−24.0** (cross-check)`.
- Debe decir: ese es el valor **SUPERSEDED** (−24.02), no un cross-check vigente.
  CANONICAL_VALUES.yaml líneas 327-337 y el banner de CLAUDE.md (tabla Paper 3) son
  explícitos: el −24.02 "tenía DOS defectos — A_s y τ clavados en Planck contándolos
  como libres, y N=613 (sólo plik_lite) cuando el χ² ya incluía lowT+lowE"; el vigente
  es **−26.03** (N=669, χ²=1003.586, A_s y τ AJUSTADOS). El párrafo de abajo (línea 189)
  sólo retira el −32.2 (legacy-MIRA) pero no corrige esta fila de la tabla, que quedó
  con el número viejo etiquetado como si fuera un cross-check válido.
- Reemplazo propuesto: cambiar la fila a `ΔBIC (plik_lite TTTEEE+lowT+lowE, k=2 vs k=6,
  N=669, τ ajustado) | **−26.03** (cross-check)` y, si se quiere conservar el −24.0 como
  nota histórica, marcarlo expresamente "superseded" como se hizo con el −32.2.

### H3 · AUDIT.md:1-76 (snapshot congelado, mal etiquetado) · dimensión 2/4 (Relaciones/Coherencia) · retirado-vigente · confianza ALTA
- Dice (línea 12): «The Hubble cascade is H_alg = 67.962 → H_local = **72.86** (0.17σ)».
  Línea 34: «CMB peak ℓ₁ ... Planck **PR4**: ~220». Línea 39: `k_fs | 0.754 h/Mpc
  algebraic | DESI Y3/Euclid P(k): 2026–2028 | Future prediction` (sin marca de retiro).
  Línea 35, 67, 69: `0.30889` (valor rancio, ver H1).
- Debe decir / por qué: el banner propio del archivo (línea 8-17) se autodeclara
  "superseded snapshot (2026-05-17)" pero NO retracta cada número individualmente dentro
  del cuerpo, así que un lector externo que entra a la tabla de predicciones (líneas 31-41)
  lee **72.86 como el H local vigente** — es justo el valor que el banner de CLAUDE.md
  marca **RETIRADO** ("72.86 y 73.040 quedan RETIRADOS: eran el mismo enunciado leído al
  revés"). El pico CMB a `ℓ₁=221` usa el espectro TT/TE/EE, que es **Planck 2018 PR3**
  (R3.01), no PR4 (PR4 es sólo el lensing) — mismo patrón que ya se corrigió en P1-P10/Unified
  el 2026-10-09 (commit `7976fa6`) pero no se propagó a AUDIT.md. Y `k_fs` queda listado como
  "Future prediction" sin la nota de retiro que SÍ lleva la fila de `m_φ` justo arriba —
  inconsistente: k_fs se retiró junto con la partícula (banner φ-DM, 2026-08-01).
- Reemplazo propuesto: (1) línea 12, tachar «72.86» y anotar RETIRADO, o sustituir todo el
  párrafo por un remite a README/CANONICAL (ya lo dice la línea 15, pero el número queda
  escrito igual arriba); (2) línea 34: `Planck PR4` → `Planck 2018 (PR3)`; línea 69:
  `Planck PR4` → `Planck 2018 (PR3 + lensing PR4)`; (3) línea 39: añadir la misma marca
  RETRACTED 2026-08-01 que lleva `m_φ` en la línea anterior, o borrar la fila; (4) las 3
  ocurrencias de `0.30889` (líneas 35, 67, 69) → `0.308881` (ver H1, mismo patrón).
- Nota de alcance: no revisé el cuerpo completo de AUDIT.md (438 líneas) más allá de la
  cabecera y la tabla de predicciones — el resto puede tener más del mismo snapshot congelado.

### H4 · OPEN_PROBLEMS.md:410,412,589,592,671,2114,2348 · dimensión 1 (Valores) · valor-erróneo · confianza ALTA
- Dice: `Ω_m,CMB = 0.30889` presentado como **canónico/vigente** (no dentro de un bloque
  tachado o marcado RETIRADO) en al menos 7 sitios: la frase "canónico ω_m-directo,
  Ω_m=0.30889" de OP-5 (línea 410); "sobre Ω_m,cosm=0.30889" (línea 412, en texto activo,
  no en la parte tachada de abajo); la derivación de OP-7 "ω_c = KAL₀·ω_b·n_s = 0.11951 →
  Ω_m,CMB = ω_m/h² = 0.30889" (línea 589, repetida en 592); la fórmula de la línea 671; y
  la tabla resumen de OPs, filas OP-8 (línea 2114) y la línea 2348.
- Debe decir: `0.308881` — mismo bug que H1/H2, confirmado por CANONICAL_VALUES.yaml
  (0.30889 es el valor RANCIO de Σm_ν=0.06902; el correcto, con Σm_ν=0.06849, es
  0.308880879 → 0.308881). Este archivo entra al zip público de Zenodo (OP-1..OP-19
  son parte de lo que un referí lee primero), así que el error se propaga a la pieza
  más visible del "estado abierto" del modelo.
- Nota: otras 3 ocurrencias de 0.30889 en OPEN_PROBLEMS.md (líneas 415, 431, 461) están
  dentro de texto EXPLÍCITAMENTE marcado "retirado"/histórico (tachado o con nota R74 de
  procedencia de un log viejo) — esas sí son legítimas como registro.
- Reemplazo propuesto: `0.30889` → `0.308881` en las líneas 410, 412 (la mención activa,
  no la retirada), 589, 592, 671, 2114, 2348.
- Nota adicional (confianza MEDIA, dimensión 6/legibilidad): la cabecera del archivo
  (línea 7) dice «Last updated: 2026-07-12», pero el cuerpo tiene entradas fechadas hasta
  2026-10-03 (OP-4 cierre) — la fecha de cabecera quedó rancia y puede hacer pensar a un
  lector externo que el documento no refleja el estado reciente.



