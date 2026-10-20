# Perfil de `ω_c` en BOSS — la brecha de amplitud NO es `ω_c` disfrazado

> 🔴 **RETIRADO 2026-10-20.** Esta nota mide BOSS sobre los espectros de Beutler+2017 (tres errores de método: bines solapados, A_s lineal a un lazo, normalización de 2017). Sus números no son vigentes; script y log en `archive/codigo/investigacion/boss_beutler17_RETIRADO_2026-10-20/` y `archive/logs_superados/boss_beutler17_2026-10-20/`. BOSS vigente: `results/logs/growth_2026-07/boss_chen21.json` (OP-26).

**Corrida:** `perfil_wc_boss.py`, terminada 2026-09-08 06:18.
**Coste medido:** 18 puntos × ~59 s = **18 min**.
**Estado:** ✅ completa, **control PASA**.

> ⚠️ Esta corrida **anula e invalida** el perfil del 2026-09-07. Aquél corrió
> antes del arreglo de la caché de plantillas de `boss_lpt_R1R2.py`, que
> reutilizaba las plantillas del PRIMER `ω_c` calculado para todos los demás.
> Sus números **no se citan**.

## 1. Qué se preguntó

Ya sabíamos que BOSS, con el `ω_c` clavado por el álgebra, pide una amplitud
más baja que la del CMB (`logA = 2.7636 ± 0.0981` frente a `3.0438`). La
pregunta simétrica es: **con la amplitud del CMB clavada, ¿qué `ω_c` pide
BOSS?** Si pidiera uno muy distinto, lo que parecía un `A_s` bajo sería en
realidad `ω_c` disfrazado, porque los dos suben la amplitud y son degenerados.

## 2. El número

| perfil | `ω_c` que pide BOSS | vs identidad `KAL₀·ω_b·n_s` |
|---|---|---|
| con `A_s` del CMB (`logA = 3.0438`) | **0.114108 ± 0.003099** | **1.74σ** |
| con `A_s` de BOSS (`logA = 2.7636`) — *control* | **0.117524 ± 0.003933** | **0.51σ** |

Forzar la amplitud del CMB desplaza `ω_c` un **−2.9%**, y sólo eso.

**Contra las otras sondas**, el `ω_c` que BOSS pide con la amplitud del CMB:

| comparación | σ |
|---|---|
| vs `ω_c` del CMB (0.119534 ± 0.000248) | 1.75 |
| vs `ω_c` de BAO DESI DR2 (0.123542 ± 0.003828) | 1.92 |

## 3. El resultado, que es lo importante

**Cuánto compra cada libertad, sobre los mismos 222 puntos:**

```
w_c algebraico + A_s del CMB       chi2 = 78.760
w_c LIBRE      + A_s del CMB       chi2 = 76.828    gana 1.93
w_c LIBRE      + A_s de BOSS       chi2 = 72.423    gana 4.41
```

Un parámetro cada uno. **Soltar `ω_c` compra 1.93; soltar la amplitud compra
4.41**, más del doble. Y con la amplitud que BOSS mismo prefiere, `ω_c` vuelve
a caer sobre la identidad algebraica a **0.51σ**.

O sea: la discrepancia vive en la **amplitud**, no en `ω_c`. BOSS no está
pidiendo otra densidad de materia oscura disfrazada de amplitud baja; está
pidiendo amplitud baja, y `ω_c` sólo se mueve lo que la degeneración le
obliga.

Esto **refuerza** la identidad `ω_c = KAL₀·ω_b·n_s`: la sonda que más lejos
está del CMB en amplitud sigue queriendo el `ω_c` algebraico cuando se la deja
en paz.

## 4. Control (R53)

El control estaba pre-registrado en el propio script: *«el mismo perfil con
`logA` al valor que BOSS mismo prefiere. Ahí `ω_c` debe volver a ~la
identidad; si no vuelve, el perfil está midiendo el borde de la
parametrización, no el dato.»*

Vuelve: **0.117524, a 0.51σ de 0.119514**. El perfil mide el dato.

Segundo control implícito: las dos parábolas tienen curvatura sana y el mínimo
cae dentro de la rejilla (no en un extremo), en `0.114375` de un barrido que
va de `0.090` a `0.155`.

**Control PASA.**

## 5. Qué tocaría si Mike lo aprueba

- **Paper 6**, sección de `fσ₈`/R1-R2: es un resultado nuevo y publicable.
  Convierte «BOSS prefiere menos amplitud» en «BOSS prefiere menos amplitud
  **y no menos materia**», que es un enunciado mucho más fuerte y cierra la
  vía de escape obvia de un referee.
- **`OP-19`**: añadir que la identidad sobrevive a la prueba simétrica en una
  sonda de estructura a `z≈0.5`, no sólo en el CMB.

## 6. Qué NO toca

- No toca `ω_c = 0.119514`: lo confirma, no lo mueve.
- No toca `S₈` ni R3/R4.
- No toca el fondo ni la geometría.
- **No** dice nada sobre de dónde sale la brecha de amplitud del 8.6%. Sólo
  descarta a `ω_c` como culpable.

## 7. Lo que no cerró

**La brecha de amplitud sigue sin dueño.** Con esta corrida quedan descartados
como absorbentes: `ω_c` (aquí), `ω_b`, `n_s`, `H₀`, `Σm_ν`, `μ` tardía (todos
medidos antes). El único candidato con la época correcta sigue siendo `τ_Π`,
la viscosidad IS, y eso cuelga de OP-22b.

**No abro OP nuevo:** esto es la veta de `A_s` que Mike ya tiene abierta, y
esta corrida la estrecha en vez de ensancharla.
