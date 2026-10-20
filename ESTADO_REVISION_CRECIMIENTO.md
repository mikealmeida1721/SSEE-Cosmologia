# Estado de la revisión del sector de crecimiento (S₈, fσ₈, φ-DM)

> ⬛ **CERRADO 2026-09-20 — la decisión se tomó y la propagación se hizo.**
> Este cajón se abrió el 2026-07-30 diciendo «NO propagado al canon a propósito
> … hasta que Mike decida y el análisis esté completo». Las dos condiciones se
> cumplieron hace tiempo y el cajón se quedó abierto: Mike decidió el
> **2026-08-01** (se retiran la partícula y el segundo sector) y el
> **2026-09-19** (se clava `A_s` al valor del CMB), y las dos cosas están
> propagadas a `CANONICAL_VALUES.yaml`, a Paper 6 y al guardián. Así que su
> aviso —«no uséis estos números como vivos»— ya **no** describe la situación:
> hoy son los canónicos.
>
> **Canónico hoy:** un solo sector, `Ω_m=0.308881`; contra KiDS-1000 con `A_s`
> libre `S₈=0.7555±0.0192` (0.11σ), y contra **KiDS-Legacy con `A_s` clavado
> —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido
> (0.05σ)**. Lo de abajo se conserva como el registro de cómo se llegó ahí:
> es la mesa de trabajo de aquella revisión, no el estado del modelo.
>
> El «Pendiente» del final (el modelo de RSD contra BOSS crudo) **se hizo el 2026-10-20**
> con el montaje de Chen+22 y su control: `results/logs/growth_2026-07/boss_chen21.json`,
> ficha OP-26. Este documento ya no tiene nada vivo.

## Qué se midió (contra datos CRUDOS, no contra valores publicados)

Pipeline propia sobre los **225 puntos de cizalla de KiDS-1000**, validada con
control negativo: reproduce χ² = 261,27 frente al 260,32 oficial (0,4%).
Scripts en `src/p06_growth/`, resultados en `results/logs/growth_2026-07/`.

| corrida | fondo | libres | χ² | logA | σ₈ | S₈ |
|---|---|---|---|---|---|---|
| ΛCDM-Planck fijo | Planck | 8 nuis. | 277,290 | 3,04479 | — | — |
| SSEE fijo | álgebra | 8 nuis. | 276,736 | 3,04070 | — | — |
| ΛCDM A_s libre | Planck | 9 | 264,114 | 2,84622 | 0,73447 | 0,75261 |
| **SSEE A_s libre** | álgebra | 9 | **263,820** | 2,86706 | 0,74597 | **0,75693** |

**Los dos empatan** (Δχ² = 0,294 sobre 225 puntos) con **los mismos 9 libres**.
La ventaja de conteo de SSEE está en el fondo (0 ajustados vs 5), no en esta tabla.

## Los cuatro hallazgos, en orden de gravedad

**1 · No hay tensión S₈ en SSEE.** Con A_s libre —que es libre en ambos modelos—
S₈ = 0,75693 contra KiDS 0,759 ± 0,024: **−0,08σ**. El «3,5σ del desafío»
(S₈ = 0,846) era artefacto de **fijar A_s a Planck**, es decir de importar la
tensión Planck–KiDS. Ver [[project-s8-no-tension-particle-excluded]].

**2 · La partícula de 40,70 eV queda excluida por el dato.** Suprime σ₈ un 10,42%
contra un margen de 3,16%, y **A_s no lo compensa** porque T²(k) cambia la forma
(0,80 en k=0,2 → 0,03 en k=2), no la amplitud. Cota medida: **m_φ > 70,3 eV**
(leyes: k₅₀ = 0,00603·m^1,087 · Δσ₈% = 52088·m^−2,283).

**3 · Ninguna construcción de linaje puede reemplazarla.** Ventana pre-declarada
(`results/logs/growth_2026-07/PREDECLARACION_ventana_frio.md`) ANTES de enumerar:
73 candidatos caen dentro por valor, **0 pasan por rol** (41 violan la ley de copia,
32 no tienen rol de acoplamiento). Control positivo: SOLAR²·KRYSTOS_V sí pasa los
tres tests. **El máximo de la gramática es exactamente 594,28** — el canónico ES el
techo, y la ventana declarada en junio ([295,988]) llegaba justo hasta ahí.

**4 · Y la causa de fondo: el 0,160 no es una densidad.** `src/ssee_core.py:39,48`
dice textual «= |w0|; es la EoS, NO la fracción de densidad» y «NO es materia
total», y el mismo bloque de comentarios la suma con 0,149 para dar 0,308.
**Ω_φDM = 0,308881 − 0,160050 es una resta entre una densidad medida y un número
de la ecuación de estado.** No define una partícula. Es MIRA otra vez.
Ver [[project-0160-is-eos-not-density]].

## Números del canon bajo revisión — NO usar sin leer esto

| valor canónico | estado |
|---|---|
| S₈ = 0,758 «0,04σ KiDS, RESUELVE» | **en cuestión**: sale de A_s fijado a Planck; con A_s libre y un sector da 0,757 |
| ~~σ₈ = 0,747 (two-sector)~~ | **RETIRADO 2026-08-01** con el sector doble; el canónico es σ₈ = 0,7446 ± 0,0189, un solo sector |
| m_φ = 40,70 eV · mult 594,28 | **excluido por el dato** (cota > 70,3 eV) |
| k_fs = 0,754 h/Mpc | **en cuestión**: es la predicción que el dato contradice |
| Ω_φDM = 0,14889 | **en cuestión**: la resta que lo define mezcla magnitudes |
| fσ₈ 0,70σ (un sector); ~~0,93σ (two-sector)~~ **RETIRADO 2026-08-01** | **ninguno fiable**: los fσ₈ publicados llevan fiducial ΛCDM (AP) cocido, igual que el S₈ de KiDS |

**Intactos y no afectados:** geometría E(z)/BAO/r_d/H(z) (usa Ω_m = 0,308881),
w₀ = −0,840, wₐ = −0,670, H_alg = 67,962, α_K = 0,403302 (adimensional×adimensional,
uso legítimo del 1+w₀), Papers 1, 2, 3, 7, 8, 9, 10.

## OPs que caerían si se disuelve el segundo sector

OP-9 (coeficiente) · OP-10 (unificar χ en φ — **y restaura la filosofía de un solo
campo, hoy «technically violated»**) · OP-11 (**elimina ξ, un parámetro libre**) ·
OP-12 (T_φ, que el propio texto llama «bookkeeping, no física»).
Ninguno nuevo se abre.

## Trabajo en curso — BOSS DR12 crudo

Datos descargados y **lectura verificada**: `/mnt/datos/SSEE_data/boss_dr12/`,
lector en `src/p06_growth/boss_dr12_data.py`. 222 puntos (P₀,P₂,P₄ × 3 z × NGC/SGC),
k = 0,016–0,145 h/Mpc (**régimen lineal — sin dependencia de HMcode/halofit**),
covarianzas de 2045-2048 mocks PATCHY (definidas positivas), ventanas incluidas.
Control de lectura: √C_ii/σ_fichero = 1,0000 ± 0,0000 en los 18 multipolos.
k-range coincide con el publicado (0,01–0,15 para P₀/P₂; 0,01–0,10 para P₄).

**Qué decide:** A_s es uno solo y hay tres observables de amplitud (CMB, cizalla,
RSD). Las tres sondas difieren en dos ejes —época y escala— así que la dispersión
de los tres A_s **separa sistemáticos de escala de crecimiento modificado**:

- BOSS con el CMB (~3,04) → discrepa la escala ⟹ sistemáticos no lineales/bariónicos
- BOSS con la cizalla (~2,87) → discrepa la época ⟹ crecimiento modificado
- BOSS en un tercer sitio → problema de los datos, ningún modelo con un A_s los cubre

Beutler reporta que su fσ₈ en z=0,61 ya se desvía ~1,4σ de Planck ΛCDM.

**Pendiente:** modelo de RSD (Kaiser + dispersión, AP vía α∥/α⊥ contra el fiducial
Ω_m=0,31, convolución con ventana) y su control negativo por χ²/dof.

## Regla de propagación cuando Mike decida

Orden obligatorio (ver [[project-propagation-order]]): `ssee_core` → yaml →
**logs** → figuras → tex → docs → Registro → guardián. El nivel de los logs es el
que siempre se olvida: un `.log` es un artefacto congelado y hay que re-correrlo.
~~**Nada de esto se toca hasta que BOSS esté cerrado y Mike decida el alcance.**~~
🔴 **Superado 2026-09-20:** Mike decidió el alcance el 2026-08-01 y el
2026-09-19, y la propagación se hizo en ese orden. Lo que sigue sin tocarse,
y a propósito, es **sólo BOSS** (OP-26): el barrido Kaiser fue sondeo, no
resultado, y el fσ₈ canónico espera a R1/R2 con LPT.
