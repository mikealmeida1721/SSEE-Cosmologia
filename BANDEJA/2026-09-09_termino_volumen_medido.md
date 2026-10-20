# El efecto de volumen deja de ser analogía: es `ln det F`, y explica el 75%

**Corridas:** `archive/codigo/investigacion/boss_beutler17_RETIRADO_2026-10-20/marginal_vs_perfil.py` (control FALLA — y por eso
sirve) y `archive/codigo/investigacion/boss_beutler17_RETIRADO_2026-10-20/mide_termino_volumen.py` (control PASA) ·
**Logs:** `results/logs/growth_2026-07/marginal_vs_perfil.json`,
`.../termino_volumen_boss.json` · **No toca ningún paper.**

**Lo pidió Mike:** *«si realmente el perfil tiene menos sesgos… pero como sabes
no hacemos la elección por beneficio, la hacemos por rigurosidad»*. Y además
señaló dónde mirar: **BOSS no mide A_s de todos modos; lo que hay que resolver
es KiDS contra el fondo.**

## 1. Lo primero que encontré al hacerle caso: la tensión que importa TAMBIÉN mezcla reglas

Verificado leyendo los logs, no supuesto:

| número | de dónde sale | regla |
|---|---|---|
| CMB **3.0448** | `SSEE/mejor/logA` de una minimización (`cmb_dbic_tau_ajustado.json`) | **perfil** |
| KiDS **2.8627** | `logA/media` de una cadena MCMC (`R3_ssee_kids_S8.json`) | **marginal** |

Los **3.46σ** que llamamos «la tensión real» enfrentan un perfil contra una
marginal, exactamente el mismo defecto que invalidó el 0.81σ de BOSS.

## 2. Un diagnóstico que FALLA su control — y por eso resulta útil

Comparé, dentro de cada cadena, la media marginal contra el logA del mejor
punto. En BOSS, donde el desplazamiento **ya estaba medido** (0.1811):

| | media marginal | mejor punto | diferencia |
|---|---|---|---|
| BOSS (control) | 2.76452 | 2.75756 | **−0.0070 = −0.07σ** |
| KiDS | 2.86367 | 2.88314 | +0.0195 = +0.39σ |

**Control FALLA** (criterio: ver > 0.05 en BOSS). El diagnóstico está ciego, así
que **no leo la fila de KiDS**. Ambas medias reproducen lo publicado, o sea que
leo bien los ficheros; lo que no sirve es la idea.

**Y el fallo localiza el problema.** El desplazamiento de BOSS **no es media
contra moda**: dentro de su cadena esas dos coinciden (0.07σ). Si no está ahí,
está en que **las dos superficies son distintas**.

## 3. Lo son. Y está escrito en el código

`boss_lpt_R1R2.py` L262-291 — el χ² que la cadena muestrea es:

```
chi2_cadena  =  c(λ̂)  +  ln det F        con  F = Tᵀ C⁻¹ T + Λ ,   T ∝ e^logA
```

`ln det F` **es el logaritmo del volumen** que les queda a las tres molestias
lineales (a₀, a₂, sₙ) al integrarlas. Y como las plantillas escalan con `e^logA`
(L277), **ese volumen depende de A_s**. La cadena paga por subir la amplitud un
castigo que no viene del ajuste, sino de que arriba las molestias tienen menos
sitio. El perfil **minimiza** en vez de integrar, y no lleva ese término.

El efecto de volumen no es una analogía prestada de la literatura. **Es una
línea de código, y se puede medir.**

## 4. Medido

**Control primero (R24), y es algebraico:** `F` es 3×3 y `T ∝ e^logA`, luego
`det F ∝ e^(6·logA)` si el término de dato domina al prior `Λ`. Con 6 conjuntos
el techo de la pendiente es **36**.

| | |
|---|---|
| pendiente `d(ln det F)/d(logA)` medida | **32.753** |
| techo algebraico | 36 |
| fracción | **91%** — el término de dato domina al prior |
| linealidad | residuo **0.061** sobre un recorrido de **13.1** |

**Control PASA.** Y la linealidad dice cómo actúa: `ln det F` es una recta, o sea
una **inclinación pura** — mueve el mínimo sin cambiar la anchura.

Un término lineal desplaza el mínimo de una parábola en `pendiente / curvatura`:

| | |
|---|---|
| curvatura a lo largo del valle (sesgos libres, que es lo que hace la cadena) | 130.4 |
| desplazamiento **predicho** | **0.2512** |
| desplazamiento **observado** (perfil 2.94479 → moda de la cadena 2.75756) | **0.1872** |
| **el término de volumen explica** | **75%** |

## 5. Un error mío en el camino, declarado

Primero hice la resta «directa» —mínimo de `c` contra mínimo de `c + ln det F`—
y me dio 0.004, el 2%. **Ese número es el engañoso, y llegué a presentarlo como
mejor que la fórmula.** El defecto: ahí los sesgos estaban **fijos** en
`[1,0,0]`, donde la curvatura es **7776** y el A_s queda inmovilizado a ±0.016.
Esa no es la situación de la cadena, en la que los sesgos se mueven y abren la
degeneración `b1`–`A_s` (r = −0.89). Pareé una pendiente medida en un sitio con
una curvatura medida en otro.

Que la pendiente sea válida en ambos sitios lo garantiza el propio código:
`templates(st, name)` **no depende de los sesgos**, así que `ln det F` es función
de `logA` y de nada más.

## 6. Qué queda establecido, y qué no

| afirmación | estado |
|---|---|
| el χ² de la cadena de BOSS lleva un término de volumen que depende de A_s | ✅ **leído en el código y medido** |
| ese término inclina hacia A_s bajo y explica ~¾ del desplazamiento | ✅ **medido** (32.75 de techo 36; 0.2512 predicho vs 0.1872) |
| el desplazamiento de BOSS es media-contra-moda | ❌ **descartado** (0.07σ dentro de la cadena) |
| KiDS no tiene este mecanismo | ✅ **verificado**: sus 9 libres se muestrean todos, sin marginalización en cerrado — no hay `ln det` que dependa de A_s |
| KiDS está libre de volumen **por completo** | ⛔ **no demostrado** — sólo se descartó esta vía |
| el perfil es el estimador INSESGADO | ⛔ **no demostrado** — sigue siendo la cola **#23** |

**El 25% que falta** no está explicado. Puede ser que la curvatura de la
superficie marginalizada no sea exactamente la del perfil, o que la
marginalización sobre los sesgos aporte lo suyo. No lo sé, y no lo invento.

## 7. Lo que esto NO autoriza

Nada de esto dice que 2.9448 sea el A_s verdadero de BOSS. Dice **de dónde sale
la diferencia** entre los dos números. Que el perfil sea el insesgado sigue
necesitando la #23 — dato sintético con la verdad conocida — y esa es la única
que convierte el argumento en medida.

**Ninguna cifra pasa a Paper 6 por este informe.**
