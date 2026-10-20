# Gemelo ΛCDM del perfil de `ω_c` — el desplazamiento es del DATO

> 🔴 **RETIRADO 2026-10-20.** Esta nota mide BOSS sobre los espectros de Beutler+2017 (tres errores de método: bines solapados, A_s lineal a un lazo, normalización de 2017). Sus números no son vigentes; script y log en `archive/codigo/investigacion/boss_beutler17_RETIRADO_2026-10-20/` y `archive/logs_superados/boss_beutler17_2026-10-20/`. BOSS vigente: `results/logs/growth_2026-07/boss_chen21.json` (OP-26).

**Corrida:** `perfil_wc_boss_lcdm.py`, terminada 2026-09-08 06:38.
**Coste medido:** 18 puntos × ~51 s = **16 min**.
**Estado:** ✅ completa, **control PASA**. Dos lecturas, las dos a favor.

## 1. Qué se preguntó

El perfil en SSEE mostró que al clavar la amplitud del CMB, BOSS desplaza
`ω_c` hacia abajo. Eso admitía dos causas y no las distinguía:

```
(a) propiedad del DATO      BOSS quiere menos amplitud, y punto
(b) propiedad de SSEE       su fondo algebraico lo fabrica
```

Este gemelo corre el mismo perfil con el fondo de ΛCDM. Es igualar la
**rigidez**, no la libertad — la misma lógica que la celda `lcdmfijo` de KiDS.

## 2. Los cuatro números

| perfil | `ω_c` que pide BOSS | vs su propia referencia |
|---|---|---|
| SSEE con `A_s` del CMB | 0.114108 ± 0.003099 | 1.74σ de `KAL₀·ω_b·n_s` |
| SSEE con `A_s` de BOSS *(control)* | **0.117524 ± 0.003933** | **0.51σ** |
| ΛCDM con `A_s` de Planck | 0.112169 ± 0.003455 | 2.27σ de 0.1200 |
| ΛCDM con `A_s` de BOSS *(control)* | **0.114726 ± 0.003714** | **1.42σ** |

Desplazamiento al forzar la amplitud alta:

```
SSEE   0.117524 -> 0.114108    -2.9 %
LCDM   0.114726 -> 0.112169    -2.2 %
```

## 3. Resultado 1 — A FAVOR, y contesta la pregunta

**ΛCDM también se desplaza, y en la misma dirección y magnitud.** Luego la
causa es (a): **es el dato**. Ningún modelo fabrica ese desplazamiento; es la
degeneración amplitud–densidad actuando igual sobre los dos. Queda descartado
que el fondo algebraico de SSEE sea el sospechoso.

Y hay algo más, que no esperaba: **la referencia de SSEE está más cerca de lo
que BOSS pide que la de ΛCDM.**

```
lo que BOSS pide con su propia amplitud
  SSEE   0.117524   su referencia algebraica 0.119514   dista 0.001990   0.51 sigma
  LCDM   0.114726   su referencia de Planck  0.120000   dista 0.005274   1.42 sigma
```

El `ω_c` que sale de φ y π cae **más cerca** del que quiere una encuesta de
estructura a `z≈0.5` que el que Planck ajusta dentro de ΛCDM. Es un punto
limpio a favor de la identidad, y no estaba buscado.

## 4. Resultado 2 — lo corrigió Mike: NO es un resultado, es un diagnóstico

**Versión primera, y estaba mal encuadrada.** Escribí que «con `ω_c` libre ΛCDM
ajusta BOSS mejor, 68.805 frente a 72.423, y la brecha creció de 1.550 a
3.618». Los números son correctos; el encuadre no.

**Por qué está mal.** En SSEE `ω_c` **está fijo por álgebra**. Soltarlo saca al
modelo de sí mismo, así que un χ² con `ω_c` libre no describe a SSEE. Comparar
dos modelos en ese régimen no compara modelos: compara dos cosas que ya no son
ninguno de los dos. El barrido se hizo para **información** —ver hacia dónde se
mueve el dato— y eso es una preferencia del dato, no un veredicto.

**Lo que el mismo número sí dice, leído bien:**

```
                     como ES      w_c LIBRE     gana con la libertad
SSEE                  75.228        72.423            2.805
LCDM                  73.678        68.805            4.873
```

**ΛCDM necesita casi el DOBLE de corrección que SSEE.** Su `ω_c` de Planck está
peor colocado para BOSS que el algebraico. Va en la misma dirección que el
resultado 1 y lo refuerza.

**La comparación legítima** es cada modelo corriendo como es, y ya se conocía
desde R1/R2: ΛCDM 73.678 frente a SSEE 75.228, **diferencia 1.550**. Esta
corrida **no la cambia** y no debe citarse como si la cambiara.

**Lo que sigue abierto** es de dónde sale ese 1.550, y esta corrida sí lo
estrecha: **no viene de `ω_c`**, porque el `ω_c` de SSEE está más cerca del dato
que el de ΛCDM. Quedan `w₀`, `wₐ`, `h` y `n_s`.

## 5. Control (R53)

Pre-registrado en el script: al devolverle a cada modelo su propia amplitud,
`ω_c` debe volver hacia su referencia. Vuelve en los dos casos (SSEE 1.74σ →
0.51σ; ΛCDM 2.27σ → 1.42σ), luego los perfiles miden el dato y no el borde de
la parametrización. Los cuatro mínimos caen dentro de la rejilla.

**Control PASA.**

## 6. Qué tocaría si Mike lo aprueba

- **Paper 6**: junto con el informe hermano, convierte «BOSS prefiere menos
  amplitud» en un enunciado con control ΛCDM al lado, que es lo que R53 pide y
  lo que un referee va a exigir.
- **`OP-19`**: la identidad queda más cerca del dato de estructura que el
  valor de Planck. Es un argumento nuevo y no es débil.

## 7. Qué NO toca

- No toca `ω_c = 0.119514`, ni `S₈`, ni el fondo, ni la geometría.
- **No cambia la comparación de modelos**, que sigue en 1.550 (R1/R2).
- No explica de dónde sale ese 1.550. Sólo descarta a `ω_c` como origen.

## 8. Lo que no cerró — y la corrida que hace falta

**De dónde sale el 1.550 de χ² a favor de ΛCDM** (el de la comparación
legítima, R1/R2). No es `ω_c`, eso está medido aquí. La corrida que lo contestaría es un perfil igual pero barriendo
`w₀` (o `h`) con todo lo demás fijo, en los dos modelos. Coste estimado: otros
~20 min, la misma maquinaria.

**No lo lanzo por mi cuenta**: elegir cuál de los cuatro ingredientes se barre
primero es una decisión de Mike, no mía, y lanzar el equivocado gasta la
máquina mientras la cadena de KiDS sigue corriendo.
