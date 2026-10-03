# PREDICCIÓN DE MIKE — BOSS con la partícula, registrada ANTES de correr

**Escrito:** 2026-09-11, con la corrida sin lanzar.
**Autor de la predicción:** Mike. Yo la anoto, la afilo en números y la mido.
**Corrida:** `archive/logs_superados/particula_colas_24_29_2026-09/boss_con_particula.py` · **No toca ningún paper.**

## El enunciado, textual

> «con esta partícula tomada en cuenta debería corregir eso que falta, y de esa
> manera con el fondo clavado y la partícula debería dar χ² dentro de 1 sigma»

## Por qué BOSS es una prueba de verdad y KiDS y el CMB ya no

| sonda | qué eligió | ¿puede confirmar? |
|---|---|---|
| KiDS | la **densidad** `ω_x` | **no**, está gastada |
| CMB | la **masa** `m_x` | **no**, está gastada |
| **BOSS** | nada | **sí**, sus 222 puntos no han visto la partícula |

## La dirección, que es lo falsable

La partícula **frena** el crecimiento. Con menos crecimiento, para reproducir lo
que BOSS observa hace falta **más** amplitud. O sea que la partícula empuja el
`logA` de BOSS **hacia arriba**, hacia el 3.0448 del CMB.

| | `logA` de BOSS | vs el CMB |
|---|---|---|
| hoy, sin partícula (perfil, k_max=0.20) | **2.94479 ± 0.12385** | **0.81σ** |
| si la partícula acierta | sube hacia 3.04 | **< 0.81σ** |
| si se pasa | cruza el 3.0448 | tensión **al revés** |

**Esa última es la falsación limpia.** No sería un empate, sería un fallo con
signo: la partícula habría corregido de más.

| resultado | veredicto |
|---|---|
| `logA` sube y la distancia al CMB **baja** | la predicción de Mike acierta |
| `logA` no se mueve | la partícula no hace nada en BOSS: **falla** |
| `logA` se pasa del 3.0448 y la distancia **sube** por el otro lado | **falla**, y falla de forma informativa |

## Un aviso que hay que dar antes

**BOSS ya estaba dentro de 1σ sin partícula.** El arreglo del método (perfil en
vez de marginal, por el término de volumen `ln det F`) lo llevó de **2.87σ** a
**0.81σ**. Así que el enunciado de Mike ya se cumple hoy, y lo que esta corrida
pone a prueba es **si la partícula lo mejora o lo estropea**, no si lo arregla.

Y hay poco margen: partiendo de 0.81σ, la partícula tiene sitio para mejorar
pero también para pasarse.

## Los cuatro puntos que se corren

El óptimo conjunto **no está fijado**: se mueve cada vez que amplío la rejilla
(4.0 eV → 7.5 eV, y las dos veces pegado al borde en `ω_x`). Así que se corren
tres puntos que cubren el valle, más el control.

| `m_x` | `ω_x` | % de `ω_m` | de dónde sale |
|---|---|---|---|
| — | 0 | 0% | **control C0** |
| 4.0 eV | 0.0030 | 2.10% | óptimo de la primera rejilla |
| 5.5 eV | 0.0050 | 3.50% | centro del valle |
| 7.5 eV | 0.0065 | 4.56% | óptimo de la segunda rejilla (borde) |

## El control

**C0** · Con `ω_x` = 0 la maquinaria tiene que devolver **exactamente** lo ya
publicado: `logA` = 2.94479 y χ² = 197.43784. Toqué `camb_lin`, que es código
validado. Criterio: |Δ`logA`| < 1e−4 y |Δχ²| < 0.01. Si falla, nada de lo demás
se lee.
