# El control: con el A_s del propio fondo, los cuatro ingredientes no tienen nada que hacer

**Corrida:** `archive/logs_superados/punto_de_fuga_2026-09-08/fuga3_por_As.py fondo` ·
**Log:** `results/logs/cmb_fuga3_fondo.json` · **12 h 36 min** ·
**No toca ningún paper.**

**Diseño de Mike:** hay **tres** A_s, uno por dato, porque A_s es libre. El
barrido se corre contra cada uno, y el caso `fondo` es el **control**, porque
con el A_s que el propio fondo cósmico prefiere el castigo es **cero por
construcción**. Sin ese cero, los porcentajes de los otros dos no tienen contra
qué medirse.

## 1. El control se comporta

| | |
|---|---|
| χ² de referencia (logA y τ libres) | 1003.5860 |
| χ² con logA clavado en 3.0448 | 1003.5866 |
| **castigo** | **0.00053** |

Cero, como debía. La máquina no inventa deriva donde no la hay.

## 2. La tabla entera — y lo que hay que mirar es lo pequeños que son los números

Con el A_s del fondo, se sueltan los cuatro ingredientes en los 15
subconjuntos. Se reporta **Δχ² absoluto**, no porcentaje: no hay castigo del que
sacar porcentajes.

| conjunto | gana χ² | desplazamientos (σ de Planck) |
|---|---|---|
| ω_b + ω_c + H₀ | **1.14** | ω_b −0.3 · ω_c +0.4 · H₀ −0.6 |
| **los cuatro** | **1.11** | ω_b −0.2 · ω_c +0.3 · H₀ −0.5 · n_s +0.1 |
| ω_c + H₀ + n_s | 1.05 | ω_c +0.2 · H₀ −0.3 · n_s +0.1 |
| ω_c + H₀ | 1.03 | ω_c +0.3 · H₀ −0.4 |
| H₀ + n_s | 0.96 | H₀ −0.2 · n_s +0.3 |
| ω_b + H₀ + n_s | 0.96 | ω_b −0.1 · H₀ −0.2 · n_s +0.2 |
| ω_b + H₀ | 0.84 | ω_b −0.0 · H₀ −0.2 |
| H₀ | 0.83 | H₀ −0.2 |
| ω_b + ω_c + n_s | 0.83 | ω_b +0.1 · ω_c −0.1 · n_s +0.3 |
| ω_c + n_s | 0.81 | ω_c −0.2 · n_s +0.3 |
| ω_b + n_s | 0.63 | ω_b +0.3 · n_s +0.3 |
| ω_b + ω_c | 0.59 | ω_b +0.2 · ω_c −0.1 |
| ω_c | 0.55 | ω_c −0.2 |
| ω_b | 0.45 | ω_b +0.3 |
| n_s | 0.22 | n_s +0.3 |

**Mayor desplazamiento de toda la tabla: 0.57σ. Ninguno pegado al borde.** Y las
dos cotas —geometría libre y ±3σ— coinciden a **0.016**, porque nada se acerca
siquiera a su límite.

## 3. Lo que esto establece, que es lo que el control existía para establecer

**Toda la estructura monstruosa del barrido con el A_s promedio era fabricada
por clavar el A_s en un valor que nadie prefiere.**

| | castigo | mejor recuperación | precio |
|---|---|---|---|
| A_s promedio 2.8418 (`fuga2`) | **4659.30** | 76.6% | **−24σ a +37σ** |
| A_s del fondo 3.0448 (control) | **0.0005** | Δχ² = 1.1 | **< 0.6σ** |

Los treinta sigmas no eran de los ingredientes: eran del A_s forzado. Quítale el
valor impuesto y **el ajuste se queda quieto**. Esto confirma por el otro lado
lo que ya sospechábamos de `fuga2`, y era la razón de ser de este control.

## 4. Un resultado que no buscaba, y que hay que declarar con cuidado

Soltar **cuatro** parámetros gana **1.11** unidades de χ². Bajo la hipótesis de
que el modelo es correcto, soltar 4 parámetros gana ~4 por puro ruido. Aquí gana
la cuarta parte de eso, **con los límites numéricos anchos y sin nada pegado al
borde**: los ingredientes podían moverse y no quisieron.

**Lectura honesta:** con su propio A_s, el fondo algebraico de SSEE está donde
la verosimilitud del CMB lo quiere, dentro de 0.6σ en los cuatro.

**Lo que NO afirmo:** que esto sea evidencia a favor del modelo frente a
alternativas. Es un control diseñado para medir el cero, no una comparación. Y
τ estaba libre en todas las filas, así que absorbe lo que pueda absorber. Para
convertirlo en un enunciado publicable haría falta correrlo contra ΛCDM con el
mismo protocolo — **no está hecho**.

## 5. Qué habilita

Los otros dos barridos (`kids` en curso, `boss` pendiente) ahora **tienen contra
qué medirse**: cualquier estructura que aparezca en ellos por encima de este
Δχ² ~ 1 y de estos 0.6σ es estructura de verdad, no del método.

**Ninguna cifra pasa a ningún paper por este informe.**
