# NO fueron los neutrinos: el 98% del desplazamiento del A_s de BOSS es el MÉTODO

> 🔴 **RETIRADO 2026-10-20.** Esta nota mide BOSS sobre los espectros de Beutler+2017 (tres errores de método: bines solapados, A_s lineal a un lazo, normalización de 2017). Sus números no son vigentes; script y log en `archive/codigo/investigacion/boss_beutler17_RETIRADO_2026-10-20/` y `archive/logs_superados/boss_beutler17_2026-10-20/`. BOSS vigente: `results/logs/growth_2026-07/boss_chen21.json` (OP-26).

**Corrida:** `archive/codigo/investigacion/boss_beutler17_RETIRADO_2026-10-20/boss_aisla_neutrinos.py` ·
**Log:** `results/logs/growth_2026-07/boss_aisla_neutrinos.json` · 55 min ·
**Pedida por Mike:** *«cuando algo cambia así, incluso si son buenas noticias,
siempre se reverifica antes de pasarlo al paper»*. **No toca ningún paper.**

## 1. El control, que va primero (R24)

| | logA | χ² |
|---|---|---|
| A · canónico, m_ν = 0.06849 | 2.9447867806 | 197.438 |
| C · repetición idéntica de A | 2.9447867806 | 197.559 → *(mismo logA)* |

**|A − C| = 0.00e+00**, criterio < 1e−5. Cero **exacto**: el perfil es
determinista, no hay ruido de método que restar. Cualquier diferencia medida
después es señal entera.

## 2. La descomposición

Total a explicar: el logA de BOSS pasó de **2.7636** (MCMC viejo) a **2.9448**
(perfil nuevo) = **+0.1811**.

| causa | cuánto | fracción | en σ de la barra vieja (0.0981) |
|---|---|---|---|
| masa de neutrino (A − B, método fijo) | **+0.0030** | **2%** | **0.03σ** |
| método (lo que queda) | **+0.1782** | **98%** | **1.82σ** |

Con m_ν prestada (0.06): logA = 2.94181 ± 0.12166, χ² = 197.559.
Con la suya (0.06849): logA = 2.94479 ± 0.12385, χ² = 197.438.

**La masa de neutrino mueve el A_s de BOSS tres milésimas.** Es
indistinguible de nada.

## 3. Corrección de mi informe de ayer — y de la lectura que hicimos los dos

El informe `2026-09-09_boss_R1R2_neutrinos.md` §4 decía: *«no se puede atribuir
el desplazamiento a una sola causa… no digo cuál pesó más»*. Eso era correcto
entonces. Ahora está medido y **la causa es el método, casi por entero**.

La lectura de que «BOSS, al tener en cuenta el peso de los neutrinos, deja de
estar en conflicto con el CMB» **no se sostiene**. Los neutrinos no hicieron
nada. El conflicto no se resolvió: **se leyó con otra regla**.

## 4. Y qué es exactamente ese «método» — verificado, no supuesto

Los dos usan **el mismo dato, el mismo k_max = 0.20, el mismo modelado LPT y el
mismo fondo**. Comprobado: `cobaya_boss.py` L71–73 importa `boss_lpt_R1R2` y le
presta su propio KMAX. **Lo único que cambia es el estimador.**

| | qué reporta | logA | mejor χ² alcanzado |
|---|---|---|---|
| viejo | **media marginal** de una cadena de 104 272 muestras | 2.7636 | **207.638** |
| nuevo | **mínimo del perfil** | 2.9448 | **197.438** |

> 🔻 **RETRACTADO 2026-09-09 (noche) — lo pidió Mike, y tenía razón.**
> Aquí escribí *«la cadena vieja nunca encontró el fondo»* apoyándome en ese
> hueco de 10.2. **Era una acusación sin vara.** Una cadena nunca toca su
> mínimo: muestrea el bulto, no la punta, y el hueco esperado crece con las
> dimensiones. Sin calcular cuánto hueco es el normal, el número no dice nada.
>
> Calculado ahora. La cadena muestrea **19** dimensiones (logA + b1,b2,bs × 6
> conjuntos; las otras 18 se integran en cerrado, así que están en su óptimo por
> construcción — `cobaya_boss.py` L80-82).
>
> | | Δχ² del mejor de 104 272 muestras |
> |---|---|
> | esperado con d = 19 | **2.96** |
> | observado | **10.20** |
>
> Es **3.4× mayor de lo normal** — bandera amarilla de convergencia, con
> `Rminus1_stop = 0.05`, que es flojo. Pero **no es prueba de fallo**, y
> presentarlo como tal fue afirmar de más. El hueco de 10.2 sería justo el
> esperado si la cadena explorara 37 dimensiones; no las explora.

Lo que sí queda establecido es que **el desacuerdo es de estimador**, y hay una
explicación de manual que además predice el signo — la de **volumen**, en §4bis.

## 4bis. ¿Cuál de los dos es el correcto? (lo preguntó Mike)

**No es que uno sea inválido. Contestan preguntas distintas.**

| | qué pregunta | de qué depende |
|---|---|---|
| **mínimo del perfil** | *«a cada A_s, ¿cuál es lo mejor que puede hacer el modelo?»* | sólo del **dato** |
| **media marginal** | *«¿cuánta probabilidad total se acumula en cada A_s?»* | del dato **y del espacio que les queda a las molestias** |

La marginal integra sobre las 36 molestias. Si a A_s bajo las molestias tienen
**más sitio donde caber** que a A_s alto, la marginal se desplaza hacia abajo
**aunque en ningún punto de ahí el ajuste sea mejor**. Eso es el *efecto de
volumen*, y es un problema conocido y documentado justo en este análisis: los
ajustes de forma completa de BOSS sesgan la amplitud **hacia abajo**.

**El signo medido es el que predice esa explicación:** la marginal está
0.1811 **por debajo** del perfil.

### La pista que lo delata: la barra se ENSANCHÓ

| | logA | barra |
|---|---|---|
| marginal | 2.7636 | ± 0.0981 |
| perfil | 2.9448 | ± **0.1238** |

**La barra del perfil es 26% más ancha.** Mike preguntaba si uno se reconcilia
«por tener menos información». Es al revés de como suena: **el estrecho es el
sospechoso.** Un método que promedia sobre volumen puede fabricar una barra
estrecha sin que el dato haya aportado más; el perfil no puede — su anchura
sale de la curvatura de la verosimilitud y de nada más. La precisión extra de
la cadena no era información, era geometría.

### Y hay que corregir la premisa: el perfil se acerca a LOS DOS

| | contra el CMB (3.0448) | contra KiDS (2.8627 ± 0.0508) |
|---|---|---|
| marginal (2.7636) | 2.87σ | 0.90σ |
| perfil (2.9448) | **0.81σ** | **0.61σ** |

No es que un método lo acerque al CMB y el otro a KiDS. **El perfil lo acerca a
ambos.** Que un solo cambio de estimador reduzca las dos distancias a la vez es
lo que se espera si el estimador viejo tenía un sesgo, no si los datos se
contradijeran.

### Pero nada de esto lo DEMUESTRA — y hay una prueba que sí

Todo lo anterior es un argumento coherente, con el signo correcto y una pista
que encaja. **No es una medición.** La prueba que decide es barata y no depende
de ninguna teoría estadística: **dato sintético con la verdad conocida.**

Se fabrica un BOSS falso a partir de un logA que yo elijo (2.90, digamos), con
la misma covarianza y las mismas molestias. Se le pasan **los dos estimadores**.
El que devuelva 2.90 es el correcto **para esta verosimilitud**, y el otro
quedará con su sesgo medido en σ. Es cola **#23**, y hasta que se corra, «cuál
es el bueno» sigue siendo argumento y no dato.

## 5. Qué se salva, y esto es lo importante

**El empate en fσ₈ SÍ se salva, y sale reforzado por dos vías.**

| | Δχ² (SSEE − ΛCDM) |
|---|---|
| método viejo (MCMC) | +0.062 |
| método nuevo (perfil) | +0.402 |

Ambos son cero estadístico sobre 222 puntos. **La conclusión no depende del
método**, porque es una *diferencia* entre dos modelos medidos con la misma
regla, y los errores de regla se cancelan.

Y ahora además sabemos que **no depende del préstamo de la masa**: cambiarla
mueve el χ² 0.12 unidades. El empate no lo compraba la m_ν prestada.

## 6. Lo que NO se puede pasar a Paper 6

**El «0.81σ contra el CMB» no es un resultado, es una comparación mal
emparejada.** Enfrenta el **mínimo del perfil** de BOSS contra la **media
marginal** de Planck. Son dos estadísticos distintos; para un parámetro
degenerado —y el de BOSS lo es, D = 4.01— se separan justamente por lo que aquí
se midió: 1.8σ.

El «2.87σ» viejo tampoco vale, porque su cadena no había llegado al mínimo.

**Ninguno de los dos números de tensión sirve.** Para comparar hay que medir
ambos lados con la misma regla: o perfil contra perfil, o cadena contra cadena.

## 7. Veredicto

| afirmación | estado |
|---|---|
| fσ₈ de BOSS: SSEE y ΛCDM empatan con LPT | ✅ **medido y robusto al método** — pasa a Paper 6 |
| el empate no depende de la masa prestada | ✅ **medido** (Δχ² = 0.12) |
| el A_s de BOSS se movió por los neutrinos | ❌ **falso** — 2%, 0.03σ |
| el A_s de BOSS ya concuerda con el del fondo | ⛔ **indeterminado** — comparación desemparejada |
| el A_s de BOSS mide algo | ❌ ya se sabía (D = 4.01); esto lo confirma otra vez |

## 8. Deuda que deja (va a `COLA_CORRIDAS.md`)

**Nueva #22 — perfil contra perfil.** Medir el A_s del fondo cósmico por
perfil, no por marginal, para que la tensión BOSS–CMB tenga las dos mitades en
la misma unidad. Sin eso no hay número de tensión que citar.

**Toca a #17 y a la cadena de KiDS.** Ambas clavan un A_s de BOSS; la cifra de
2.7636 que usan viene de la cadena que no llegó al fondo. Hay que decidir si se
reemplaza por 2.9448 — pero eso es exactamente lo que la #22 tiene que zanjar
primero.
