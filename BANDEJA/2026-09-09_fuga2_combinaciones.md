# Los 15 subconjuntos: la sinergia es enorme, y **un cuarto del castigo no lo absorbe nadie**

**Corrida:** `archive/logs_superados/punto_de_fuga_2026-09-08/fuga2_combinaciones.py` ·
**Log:** `results/logs/cmb_fuga2_combinaciones.json` · 7 h 30 min ·
**Control PASA al 100%** antes de medir nada. **No toca ningún paper.**

## 1. Qué se midió

Con la amplitud clavada en 2.8418, el fondo cósmico castiga con
**Δχ² = 4659.298**. Se sueltan los cuatro ingredientes del fondo en los **15
subconjuntos** y se mide cuánto del castigo recupera cada uno. `τ` libre
siempre.

**Control primero (R24):** soltar solo la amplitud recupera el **100.00%**.
La máquina mide lo que dice medir.

## 2. La tabla completa, ordenada por lo que recupera

| conjunto | recupera | suma de sus partes | **sinergia** |
|---|---|---|---|
| ω_c + H₀ + n_s | **76.6%** | 35.2% | **+41.4** |
| ω_b + ω_c + H₀ + n_s | 76.5% | 37.4% | +39.1 |
| ω_b + ω_c + H₀ | 58.5% | 24.5% | +34.0 |
| ω_c + H₀ | 58.4% | 22.3% | +36.1 |
| ω_b + ω_c + n_s | 46.8% | 35.2% | +11.6 |
| ω_b + ω_c | 39.4% | 22.2% | +17.1 |
| ω_c + n_s | 27.7% | 32.9% | **−5.2** |
| ω_b + H₀ + n_s | 22.6% | 17.4% | +5.2 |
| ω_c | 20.0% | — | — |
| ω_b + H₀ | 15.4% | 4.5% | +10.8 |
| ω_b + n_s | 15.4% | 15.1% | +0.2 |
| H₀ + n_s | 13.6% | 15.2% | **−1.6** |
| n_s | 12.9% | — | — |
| H₀ | 2.3% | — | — |
| ω_b | 2.2% | — | — |

## 3. Lo que dice, en cuatro lecturas

**(a) Sumar no vale, y ahora está medido.** La objeción de Mike era correcta y
el tamaño del error es enorme: el mejor conjunto recupera **76.6%** cuando la
suma de sus miembros da **35.2%**. Se habría subestimado por más del doble.

**(b) El cuarto ingrediente sobra.** Soltar los cuatro da 76.5%; soltar solo
tres (ω_c, H₀, n_s) da 76.6%. **ω_b no aporta nada** una vez sueltos los otros
tres — de hecho el conjunto completo sale una décima peor, que es ruido del
optimizador. La estructura del castigo vive en tres ingredientes, no en cuatro.

**(c) Hay parejas que se ESTORBAN.** Dos sinergias son negativas: ω_c+n_s
(−5.2) y H₀+n_s (−1.6). Juntos recuperan **menos** que por separado: lo que uno
consigue, el otro lo deshace.

**(d) Y lo más importante: hay un SUELO.** Aun soltando **los cuatro** a la
vez, queda un **23.5% del castigo que nadie absorbe**. Eso no es un ingrediente
mal elegido: es una parte de la discrepancia que **el fondo no puede explicar
por mucho que se le suelte**.

## 4. El precio, que es la columna que hay que leer al lado

| conjunto | desplazamientos que lo compran |
|---|---|
| ω_c + H₀ + n_s (76.6%) | ω_c **−24.4σ**, H₀ **+25.6σ**, n_s **+22.2σ** |
| los cuatro (76.5%) | ω_b +13.4σ, ω_c **−29.9σ**, H₀ **+37.6σ**, n_s +26.8σ |

**Ningún porcentaje de esta tabla es físico.** Todos se compran con
desplazamientos de veinte a treinta y siete sigmas respecto a lo que el propio
dato mide. Lo que la tabla describe es la **geometría de la verosimilitud** —
por dónde se puede deslizar el ajuste — no una preferencia del dato.

La corrida acotada a ±3σ (cola #16) es la que dirá cuánto se absorbe **sin
salirse de lo permitido**. Sospecho que muy poco, pero eso es sospecha, no
medida.

## 5. Aviso: el A_s que clava esta corrida acaba de quedar obsoleto

Los 4659.298 de castigo salen de clavar `logA = 2.8418`, que es el promedio de
KiDS con **el BOSS viejo**. Esa mitad se movió **1.85σ** hoy mismo
(`BANDEJA/2026-09-09_boss_R1R2_neutrinos.md`).

**Qué se salva y qué no:** las sinergias son *fracciones* del castigo, así que
la **estructura** —quién se empuja con quién, quién estorba, que ω_b sobre— es
previsiblemente robusta. Lo que no se salva es el **valor absoluto** del
castigo ni los porcentajes exactos. Hay que rehacerlo con el A_s de KiDS solo,
que es la cola **#17**.
