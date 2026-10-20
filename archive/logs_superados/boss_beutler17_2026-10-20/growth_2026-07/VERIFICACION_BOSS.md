# Verificación del sector de crecimiento — BOSS DR12 (Fase 0)

> **2026-07-30.** Se corre entera con `.venv/bin/python -u src/p06_growth/verifica_boss.py`.
> No lee logs: re-ejecuta cada control desde cero y compara contra el valor
> esperado con tolerancia declarada. **Nada del canon tocado.**

## Resultado: 16/16 VERDE

| # | control | resultado |
|---|---|---|
| V1 | √C_ii del fichero de covarianza vs σ del fichero de datos, emparejado por (multipolo, k) | desvío máximo **3,08e−09** sobre 222 puntos |
| V2 | covarianzas definidas positivas | autovalor mínimo **1,09e+04** en los 6 conjuntos |
| V3 | normalización de la ventana, 6 conjuntos | W₀(8) ∈ [0,9925, 1,0074]; decae en octavas |
| V4 | convolución con ventana: control de **identidad** | **1,000000 ± 0,000000** en P₀, P₂ y P₄ |
| V5 | deformación Alcock-Paczynski contra el fiducial Ω_m = 0,31 | ΛCDM 0,28–0,41 % · SSEE 1,14–1,35 % |
| V5 | Ω_m total de SSEE | **0,308881** (canónico; regla del banner) |
| V6 | rejilla en k | bajar 2048→1024 mueve **4,72 %** → necesaria |
| V6 | cuadratura angular | bajar 120→80 mueve **0,0099 %** → margen para MCMC |

## Bugs REALES encontrados y corregidos (en el código de física)

1. **Bines de `s` logarítmicos.** Los conteos de pares van como `s²·ds`, no `s²`.
   Normalizar por `s²` dejaba una pendiente espuria: W₀ subía a ~13 en s = 200 en
   vez de decaer a 0.
2. **`lowring=True` desalinea las rejillas.** mcfit elige un desplazamiento
   distinto por cada multipolo, así que ξ₂ vivía en una rejilla `s` que no era la
   de ξ₀, y la mezcla los combinaba como si lo fuera. Sesgo del 2,3 % en P₂.
   Corregido a `lowring=False`, que da rejilla común.
3. **`extrap=True` en la vuelta.** La ventana anula ξ fuera de su soporte y la
   extrapolación en ley de potencias dividía por cero → NaN.

## Controles PROPIOS que estaban mal (encontrados al verificar)

| control | qué estaba mal | corrección |
|---|---|---|
| monotonía de la ventana | exigía monotonía estricta a datos con ruido de conteo del 1,2 % | tolerancia = 3/√N_pares, en octavas |
| rango de normalización | elegido a ojo; moverlo cambia la escala 1,3–3,7 % | criterio medible: el rango que deja W₀(8) = 1 (→ [2,20], da 1,0005 ± 0,0057) |
| V6 con ventana trivial | la convolución es la identidad: no puede haber efecto | usar la ventana real |
| V6 solo el monopolo | el efecto de resolución vive en P₂/P₄ | mirar los tres multipolos |

Se probó además **extrapolar** la normalización con un ajuste pesado `g = A + B s²`:
sale **peor** (dispersión 2–3,8 %, W₀ > 1 donde ya debería bajar). Retirado.

## Limitaciones conocidas, declaradas

- **Sistemática de ~2 %** en la escala de la ventana, heredada de la elección de
  rango. Menor que el sesgo de Kaiser pero no nula. Tratamiento en la fase de
  rigor: marginalizar la normalización.
- **Sesgo de la fórmula de Kaiser: −9 %, −10 %, −15 %** (creciente con z), medido
  contra el consenso publicado. Es la limitación dominante.
- Todo lo de esta fase usa **minimización, no MCMC**: no hay posterior
  marginalizada. Los valores absolutos NO son publicables; lo comparable es la
  comparación entre modelos con la misma vara.

## Control negativo contra el resultado publicado

Con la tasa de crecimiento **libre**, como en el análisis de Beutler:

| z | medido | publicado (Alam+2017) | desvío |
|---|---|---|---|
| 0,38 | 0,4528 ± 0,0563 | 0,497 ± 0,045 | −0,61σ |
| 0,51 | 0,4141 ± 0,0428 | 0,458 ± 0,038 | −0,77σ |
| 0,61 | 0,3683 ± 0,0355 | 0,436 ± 0,034 | −1,38σ |

χ²/dof = 1,048 · tensión media **0,92σ** → **maquinaria sana**.
