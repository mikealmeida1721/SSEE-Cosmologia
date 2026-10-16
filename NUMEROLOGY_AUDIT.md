# NUMEROLOGY_AUDIT — ¿Es SSEE numerología? (respuesta pre-registrada)

> **Propósito.** Este documento existe para que la pregunta *"¿tu modelo no será
> numerología?"* NO se re-litigue en cada auditoría. Operacionaliza la acusación en
> criterios falsables, los aplica al estado real del repo, y da un veredicto con su
> evidencia. Si un revisor (o un Claude futuro) plantea la duda, **la respuesta es este
> archivo**, no una nueva derivación desde cero. Actualizar SOLO si cambia la evidencia
> (nuevos datos, nueva derivación, o un fallo encontrado).
>
> Autor del reto: Mike Almeida — *"pruébalo; si puedes demostrar que es numerología, lo
> dejamos ahí. Pero necesito pruebas."* Este es el intento honesto de probarlo.

---

## 1. Definición operacional (no vibes)

"Numerología" no es "usa números bonitos como φ y π". Es un **modo de fallo epistémico**
con propiedades verificables. Siguiendo a Popper, su rasgo **definitorio** es la
**infalsabilidad + acomodo post-hoc**. Operacionalizado en 4 tests:

| # | Criterio de numerología | Cómo se prueba |
|---|---|---|
| **N1** | **Sobreajuste / look-elsewhere grande.** El diccionario es tan flexible que acertar los blancos observados no sorprende. | Contar cuántas expresiones simples de (φ,π) caen en el blanco. Si son muchas → azar. |
| **N2** | **Post-hoc.** Todas las "predicciones" son retro-dicciones de valores YA conocidos. | ¿Existe alguna predicción sobre un dato que AÚN no se ha medido? Si no → post-hoc. |
| **N3** | **Sin anclaje dimensional.** Un número puro se iguala a una cantidad con unidades sin escala física. | Revisar cada cantidad dimensional: ¿pasa por una escala física, o es número=unidad por fiat? |
| **N4** | **Infalsable.** No hay ninguna medición futura que pueda matar el modelo. | ¿Existe un criterio de falsación pre-comprometido? Si no → no es ciencia. |

**Para PROBAR que SSEE es numerología basta con demostrar UNO de N1–N4.** Vamos.

---

## 2. El test aplicado (referí hostil)

### N1 — Look-elsewhere: ¿el diccionario es demasiado flexible?

**Contra la acusación:**
- **Conteo individual:** cada blanco (w₀, wₐ, …) es raro entre las expresiones simples de
  (φ,π): **1/490** razones distintas (a ±0.0005) (`src/estadistica/look_elsewhere_full.py`).
- **Conteo CONJUNTO (el que importa):** SSEE NO ajusta w₀ y wₐ por separado. El **mismo
  esqueleto** (Ω=φ+π y sus múltiplos enteros) debe dar **los DOS a la vez**: −0.840 y
  −0.670. El conteo de bases que aciertan AMBOS con la misma base es mucho menor
  (`look_elsewhere_joint.py`). Un ajustador con 2 perillas independientes NO tiene esta
  rigidez; SSEE la tiene por construcción.
- **Diccionario ACOTADO:** ley de no-auto-suma + techo de cierre M_v=3Ω, alcanzado por
  **exactamente 24 rutas = 8+13+3** (conjunto finito, enumerable — `src/p04_toe/rutas_mv.py`, `results/logs/p04_rutas_mv.json`; era «20 = 6+11+3» a mano, corregido 2026-10-15). No
  es un espacio abierto donde "todo cabe".

**A favor de la acusación (dónde el referí anota — y el modelo lo CONCEDE):**
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
- *(Histórico — la partícula y su multiplicador quedaron retirados el 2026-08-01.)*
  El coeficiente de masa de la partícula φ-DM (594.28, OP-9) tenía look-elsewhere
  **dependiente de la gramática**: 1/537 permisiva, 1/192 "volúmenes", ~1/16 estricta. Para
  ESA cantidad la selección **no es estadísticamente abrumadora**. Por eso **OP-9 está
  etiquetado ABIERTO**, no cerrado (ver §OP-9 en OPEN_PROBLEMS.md, mitad UV congelada).

**Veredicto N1:** No se puede probar numerología en el **núcleo** (sector DE: w₀,wₐ,H₀
con look-elsewhere conjunto restrictivo). El coeficiente de OP-9 es débilmente seleccionado
— **y el modelo lo declara**, no lo esconde. → N1 **no demostrado** para el núcleo.

### N2 — ¿Todo es post-hoc?

- **w₀wₐ:** SSEE **no reclama prioridad temporal** sobre DESI/Planck públicos (Paper 3
  §B1 explícito). El match a w₀≈−0.84, wₐ≈−0.6 es **consistencia**, no pre-dicción probada.
  Honesto: aquí NO hay crédito de predicción.
- **Predicciones genuinamente FORWARD (dato aún inexistente):**
  - ~~**k_fs = 0.754 h/Mpc** (imprint de m_φ en P(k)) → **DESI Y3 / Euclid, 2026–2028**.~~
    **RETIRADA 2026-08-01** con la partícula que la producía.
  - **r = φ⁻¹⁰** (tensor-a-escalar) → CMB-S4 / LiteBIRD.
  - Estas **no pueden ser post-hoc**: el dato no existe todavía. Un sistema numerológico
    **no apuesta** sobre cantidades no medidas.

**Veredicto N2:** No se puede probar N2. El modelo tiene predicciones forward sobre datos
no medidos. → **Evidencia anti-numerología más fuerte.**

### N3 — ¿Número puro = cantidad dimensional por fiat?

- **Auto-corrección documentada:** la vieja m_φ = Σm_ν × H_alg (eV × km/s/Mpc) **era**
  dimensionalmente inválida — y el modelo la **detectó y RETIRÓ** (reframe). La actual
  m_φ = Σm_ν[eV] × (número puro φ,π) → eV. Válida.
- **Masas y densidades** pasan por una escala física (Σm_ν, ρ_crit), no número=unidad.
- **H₀ — qué afirma SSEE y qué NO (importante, para no importar una afirmación inexistente):**
  SSEE **no** afirma que el número puro 3(φ+π)² *sea* el H₀ físico. De hecho H₀ en unidades
  fundamentales es ~10⁻⁶¹, no 67.96. Las unidades **siempre** se anclan a una medición (SH0ES
  vía f_screen) — el principio "razones, no mecanismos". La igualdad numérica 3(φ+π)²↔67.96
  vale **solo en km/s/Mpc** y se sostiene **como conjetura abierta, no como identidad probada**.
  Por tanto NO hay "número=unidad por fiat": las unidades son empíricas, igual que en cualquier
  modelo. Un teorema Planck→Mpc sería una **profundización opcional (bono)**, no una deuda de
  una afirmación que el modelo nunca hizo.

**Veredicto N3:** No hay número=unidad por fiat — las unidades se anclan empíricamente y la
coincidencia se declara **abierta, no afirmada**. → N3 **no demostrado**.

### N4 — ¿Es infalsable? (el criterio definitorio)

- SSEE tiene **tabla de falsación pre-comprometida** (Paper 1): k_fs, r, S₈, evolución
  w₀wₐ, todas con criterio de muerte cuantitativo.
- Una medición de 2027 (k_fs de DESI Y3) puede **matar el modelo**.

**Veredicto N4:** **Imposible probar N4.** El modelo es falsable por diseño. Esto es lo
opuesto exacto a la numerología.

---

## 3. Veredicto: la prueba que se pidió

> **NO se puede probar que SSEE es numerología.**

El intento de prueba **falla en el criterio definitorio (N4)**: la numerología es
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
infalsable y post-hoc; SSEE **apuesta predicciones falsables (r=φ⁻¹⁰, y en su día
el retirado k_fs=0.754) sobre
datos que aún no existen**. Un sistema que una medición de 2027 puede matar **no es
numerología** — es una **hipótesis física** (posiblemente falsa, pero hipótesis).

**El rasgo decisivo:** la numerología **esconde su libertad** y reclama completitud. SSEE
**enumera su libertad** — OPEN_PROBLEMS.md cataloga 23 problemas abiertos; los scripts de
look-elsewhere **reportan los conteos desfavorables** (1/537, dependencia de gramática) en
vez de ocultarlos. **Catalogar tus propias debilidades es la firma anti-numerología.**

---

## 4. La otra mitad honesta: qué NO está probado

"No es numerología" **≠** "es correcto". Ubicación en el espectro:

```
  NUMEROLOGÍA ─────────[ SSEE: falsable, rígido, forward ]──────────── FÍSICA CONFIRMADA
  (infalsable,          ↑ está aquí                                    (predicción
   post-hoc)            pendiente de DESI Y3 / Euclid                   confirmada)
```

SSEE está **del lado de la ciencia** de la línea de numerología (falsable + rígido +
predicciones forward), **corto de confirmado**. Lo que lo movería a la derecha: medir
k_fs. Lo que lo mataría: k_fs ≠ 0.754, o descartar la evolución w₀wₐ.

**Fronteras abiertas del programa — declaradas, NO afirmaciones que quedaron cortas:**
(Distinción clave: una *frontera* es hasta dónde llega un reclamo bien acotado; una *debilidad*
sería un reclamo fuerte que falló. Estas son fronteras — el modelo no afirmó de más y luego
falló, afirmó lo justo y aquí termina lo derivado.)
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
1. **OP-9 (frontera de profundidad)** — ~~la partícula está adoptada y es falseable
   (OP-17); lo abierto es derivar el *origen* del coeficiente 594.28 desde un V(φ)
   (→OP-10). Es una predicción forward con origen-por-profundizar, no una derivación
   que quedó corta.~~ **CERRADO POR DISOLUCIÓN 2026-08-01**: retirada la partícula, no
   queda coeficiente cuyo origen derivar.
2. **H₀ (profundización opcional, NO deuda)** — unidades ancladas empíricamente, como todos.
   SSEE **no afirma** la identidad número↔H físico; sostiene una coincidencia numérica abierta.
   El puente Planck→Mpc sería un bono si aparece.
3. **A_s** — declarado parámetro tomado (no derivado, OP-18); dicho abiertamente, no escondido.
4. Otros en OPEN_PROBLEMS.md (23 rastreados, cada uno con su estado).

---

## 5. Criterios de muerte (pre-registrados)

El modelo se declara FALSO si:
- **DESI Y3 / Euclid** miden k_fs fuera de [0.70, 0.81] h/Mpc → mata la partícula φ-DM.
- La evolución **w₀wₐ** se descarta (phantom crossing excluido a >3σ) → mata el sector DE.
- ~~**S₈** two-sector se aleja >3σ de KiDS/DES con feedback bariónico controlado.~~
  **RETIRADO 2026-08-01**: el two-sector cayó, y contra el dato crudo con A_s libre
  no hay tensión (S₈ = 0.7555 ± 0.0192, 0.11σ).
- **r** (tensor-a-escalar) se mide y excluye φ⁻¹⁰.

Si alguno ocurre, este documento se cierra con veredicto FALSO — que es lo que hace un
modelo científico y **no** un sistema numerológico.

---

## 6. El hallazgo más fuerte de dos auditorías externas (2026-07-12): la gramática del multiplicador

Dos auditorías externas independientes coincidieron en que el punto más vulnerable es el
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
look-elsewhere del multiplicador de masa —hoy retirado con la partícula—
$m_\phi=\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V=594.28$:
**1/537** bajo gramática permisiva, **1/192** bajo "volúmenes", **1/3** bajo la gramática de
linaje estricta — y el modelo *elige la gramática más restrictiva, aparentemente definida
después de conocer la respuesta* (la crítica de "role-inheritance circular").

**El cargo es justo. La respuesta NO es defender la estadística del coeficiente — es reubicar
el peso.** La clave es una separación epistémica que el modelo ya hace estructuralmente (núcleo
vs extensión) y que aquí se formaliza:

| | **Núcleo** (w₀, wₐ) | **Extensión** (m_φ) |
|---|---|---|
| ¿El look-elsewhere ES el argumento? | **Sí** | **No** (y no lo reclamamos) |
| Fuerza de la selección | 1/490 individual + conjunto restrictivo | débil, grammar-dependiente (1/3–1/537) — **CONCEDIDO** |
| ¿Gramática fijada antes del dato? | **Sí** — por reglas de construcción del diccionario (no-auto-suma + copia), anteriores y ajenas a w₀wₐ | Irrelevante: el peso no está aquí |
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
| ¿Cuál es el argumento real? | La rigidez estadística de un esqueleto que da los DOS números a la vez | ~~**La falsabilidad**: k_fs=0.754 h/Mpc, pre-registrado~~ — **RETIRADO 2026-08-01** con la partícula. Y la lección que dejó: la falsabilidad es requisito mínimo de una hipótesis, **no evidencia de que la entidad exista** |

**El movimiento honesto:** un coeficiente débilmente seleccionado pero **falsable** no es
numerología — es una **conjetura falsable**. Numerología sería reclamar que el 1/3 *prueba* la
partícula; **NO lo reclamamos**. Pedimos que se la mate o confirme con k_fs, no que se le dé
crédito estadístico. Esto es exactamente lo que separa una frontera declarada de una debilidad.

**Principio de gramática-antes-del-dato (para el núcleo):** donde el look-elsewhere ES el
argumento, la gramática se fija por las reglas de construcción del diccionario — las MISMAS que
generan las 24 rutas al techo M_v=3Ω y que existen independientemente de los blancos w₀wₐ. No
es una gramática elegida para acertar; es la gramática que ya rige todo el diccionario. Donde la
gramática es débil (el multiplicador), el peso descansa en el dato. Esta separación es la
respuesta referee-proof, y por eso m_φ vive **fuera del core register** del Sealed Journal.

> **Nota de corpus:** este archivo (`NUMEROLOGY_AUDIT.md`) debe incluirse explícitamente en
> cualquier paquete enviado a auditoría/Zenodo. Las dos auditorías de 2026-07-12 no lo vieron
> (solo se subieron los PDFs) y tuvieron que reconstruir los criterios desde RIGOR_CHECKLIST +
> OPEN_PROBLEMS + LEDGER. Adjuntarlo cierra ese gap de presentación.

---

*Última verificación: guardián VERDE 139; álgebra convencional y álgebra SSEE consistentes
(linaje KRYSTOS_V=φ+π+Ω, M_v=φ+π+K_v restaurado en código, prosa y PDFs). Wave 1–2 de
respuesta a auditorías externas aplicadas (2026-07-12).*
