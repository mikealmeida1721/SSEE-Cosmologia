# PREGUNTA REGISTRADA — cola #28, escrita con la rejilla corriendo

**Escrito:** 2026-09-11, 04:20. Los tres controles PASARON, las 16 casillas en
marcha, ninguna terminada. **No he visto ningun resultado de casilla.**
**Corrida:** `archive/logs_superados/particula_colas_24_29_2026-09/conjunta_tres_sondas.py` (archivado 2026-10-17 con la partícula)
**Autor de la pregunta:** Mike. Yo la anoto y la mido.
**No toca ningun paper.**

---

## 1 · QUE CONTESTO LA CORRIDA ANTERIOR (la de los ingredientes)

**La pregunta era:** con `A_s` CLAVADO, cuando queda un hueco de chi2 sin tapar,
**cual de los ingredientes del fondo se mueve para taparlo, y hacia donde.**

No era "cuanto se mueve". Por eso la caja era de 3 sigma y no de 1: una caja
ancha deja ver la DIRECCION del empuje aunque el borde corte la magnitud.

**Contesto:** el que tapa el hueco es `omega_c`, y lo tapa BAJANDO.

| combinacion | absorbe | direccion |
|---|---|---|
| `omega_c` solo | +17.5% | baja 3 sigma (pegada al tope) |
| `omega_c + n_s` | +21.0% | `omega_c` baja 3 · `n_s` sube 2.7 |
| `omega_b + omega_c + n_s` | +21.9% | los tres bajan o casi no se mueven |
| `H0` solo | +2.4% | baja 1.7, LIBRE, sin pegar |
| `n_s` solo | +2.3% | sube 1.4, LIBRE, sin pegar |

Sin techo, `omega_c` se va 4.7 sigma por debajo. **Nunca sube. Ni una vez, en
ninguna fila.** Todo lo demas que se mueve libre vale 2.4% o menos.

**Aviso: 8 de las 15 filas de esa columna NO valen.** Violan el anidamiento
(soltar mas ingredientes daba MENOS absorcion que soltar un subconjunto, lo
cual es imposible). Las 5 filas de arriba son de las 7 limpias.

## 2 · POR QUE ESO HACE QUE VALGA LA PENA BUSCAR LA PARTICULA

El dato pide **menos materia oscura fria**. Pero bajar `omega_c` 3-4.7 sigma a
secas esta PROHIBIDO: el CMB mide `omega_m` y no la deja moverse ahi.

**La particula hace exactamente eso por una puerta que no cuesta chi2 de CMB:**
se le RESTA a `omega_c` pero se le SUMA a `omega_m`, asi que la materia total
no se mueve ni un poco (control C1 de la #24: 2.78e-17). El CMB pesa la misma
gravedad en z=1100. Lo unico que cambia es que una parte de esa materia iba
rapida y se freno tarde.

**O sea: la particula entrega la direccion que el dato pide sin pagar el precio
que el dato prohibe.** Eso es lo que la corrida anterior confirmo, y es la
razon de que esta se lance.

Lo que NO confirmo: que la particula exista, ni su masa, ni su densidad.

## 3 · LA PREGUNTA QUE ESTA CORRIDA VA A CONTESTAR

> **Con el fondo algebraico clavado y UNA SOLA amplitud compartida por las tres
> sondas, existe alguna particula (m_x, omega_x) que deje a KiDS, al CMB y a
> BOSS simultaneamente dentro de su propia medicion?**

Lo que se barre:

| |  valores | libre o fijo |
|---|---|---|
| `m_x` | 2.2 · 4.0 · 7.5 · 15.0 eV | se barre, 4 pasos |
| `omega_x` | 0.0020 · 0.0035 · 0.0050 · 0.0065 | se barre, 4 pasos |
| `logA` | rejilla 2.88 a 3.10, **paso 0.0275** | LIBRE, pero COMPARTIDO |
| fondo (`omega_b`,`omega_c`,`H0`,`n_s`) | algebraico SSEE | FIJO |
| halo, alineamiento, molestias de BOSS | — | LIBRES |

## 4 · LOS CRITERIOS, FIJADOS ANTES DE MIRAR

**El limite:** `|logA - 3.04320| <= 0.0291`, que son 2 sigma de la medida del
CMB. Cualquier casilla que necesite salirse sale marcada RECHAZADA aunque su
chi2 total sea el mejor de todos.

**La vara publicada, sin particula:** CMB 1003.587 · KiDS 266.559 · BOSS 197.438.

| lo CONFIRMA | lo FALSA |
|---|---|
| alguna casilla baja el chi2 total y su `logA` cae dentro del limite | ninguna casilla dentro del limite mejora |
| el minimo NO esta en un borde de la rejilla de masa/densidad | el mejor sale en 15.0 eV o en 0.0065, o sea que la rejilla no contenia el minimo |
| las tres sondas mejoran o quedan igual a la vez | una mejora a costa de empeorar otra |

## 5 · UN LIMITE DE ESTA CORRIDA QUE HAY QUE DECIR AHORA, NO DESPUES

**El paso de la rejilla de `logA` es 0.0275 y el limite vale 0.0291.** Eso deja
**solo DOS puntos de la rejilla dentro del limite:**

| punto | distancia al CMB |
|---|---|
| 3.0175 | −1.77 sigma |
| **3.0450** | **+0.12 sigma** |

El siguiente, 3.0725, queda fuera por 0.0002 — o sea, por nada.

**Consecuencia:** la amplitud que devuelva cada casilla no es una medida fina,
es una eleccion entre dos casillas de amplitud. Si el resultado sale bueno, el
numero de `logA` que lo acompanie hay que citarlo SIEMPRE con su paso, y la
corrida fina hace falta antes de afirmar nada sobre el valor de la amplitud.
Lo que si es fiable con este paso: **si mejora o no, y cual particula gana.**

---

**Ninguna cifra de aqui entra en ningun paper.**
FUENTE: `archive/logs_superados/particula_colas_24_29_2026-09/conjunta_tres_sondas.json`
