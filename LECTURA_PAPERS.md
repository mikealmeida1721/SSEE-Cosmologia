# Lectura de la suite — Papers 1→10, en orden

**Abierta 2026-07-27.** Antes se leyó el PRD (consolidado). Mike corrigió la
prioridad: **el PRD y el Sealed son resúmenes DERIVADOS; los Papers son el
árbol**. Si un Paper y un consolidado dicen cosas distintas, quien compare
concluye que el modelo se contradice a sí mismo — y eso pesa más que cualquier
acierto. Se riega el árbol, no la fruta.

## El método (no cambia)

Se lee **en orden de lectura**, se para en la **primera afirmación**, y no se
avanza hasta que las tres capas coincidan:

1. **la afirmación** — qué dice el texto
2. **la evidencia** — qué la respalda (script, log, figura, cita)
3. **la trazabilidad** — de dónde sale cada número y cada entidad

Reglas que Mike fijó para esta lectura:

- **Ningún número sin origen localizable.** Si no se puede señalar de dónde
  sale, no se afirma.
- **Las figuras cuentan como afirmación.** Una figura rancia miente igual que
  un número mal.
- **Cada MCMC debe apuntar a UNA pregunta declarada.** Es la mayor fuente de
  ambigüedad: unos dejan parámetros libres, otros los fijan, y confundirlos
  invalida la conclusión. Sólo en Paper 2 hay ~5.
- **Una pregunta abierta a la vez.** Lo lateral se anota aquí y NO se persigue
  hasta cerrar la actual.

## ⚠ Las SEIS dimensiones — una página no se cierra hasta pasar las seis

**Fijado 2026-07-27, tras el fallo del `=` vs `≈`.** Mike leyó la página 3 y vio
que las siete constantes usaban «casi igual» donde correspondía una igualdad. Yo
había pasado por esa lista **tres veces** sin verlo. Su diagnóstico:

> «Lo dejaste pasar porque no lo leíste: te centraste en que los decimales fueran
> correctos. Está bien eso, pero no podemos descuidar uno para tener otro bien, ya
> que eso sólo deja otro hueco abierto. Las matemáticas son el lenguaje universal
> porque en ellas no existe la ambigüedad — eso vale igual para ti.»

El defecto de método: **revisar una página buscando UNA cosa**. Los decimales
salían bien, así que la página parecía cerrada. Cada página se lee ahora en las
seis dimensiones, explícitamente, y ninguna se cierra por llevar una bien:

| # | dimensión | la pregunta |
|---|---|---|
| 1 | **Valores** | ¿cada número es el redondeo correcto de su fórmula? |
| 2 | **Relaciones** | ¿el signo dice lo que afirma? `=` exacto, `≈` truncado, `∼` orden de magnitud (**R40**) |
| 3 | **Entidades** | ¿cada símbolo es la entidad correcta, no otra con el mismo valor? (`I_g` ≠ `K_v`) |
| 4 | **Coherencia** | ¿se contradice con otra parte del mismo documento, o con otro paper? |
| 5 | **Trazabilidad** | ¿se puede señalar de dónde sale cada número y cada afirmación? |
| 6 | **Legibilidad** | ¿un lector lo comprueba **de un vistazo**, sin reconstruirlo? |

Regla derivada: **cada hueco que Mike encuentra y el guardián no, obliga a (a)
crear la contramedida y (b) volver atrás a verificar que cubre lo ya revisado.**
Una regla nueva no vale hasta correrla sobre las páginas que ya se dieron por
cerradas.

## Estado

## 🔁🔁 TERCERA PASADA — desde Paper 1, página 1 (2026-09-26)

Mike: la lectura **empieza de nuevo**, porque desde que se inició el modelo
cambió (partícula retirada, dirección de la cascada, β_c, P7 sin potencial,
KiDS-Legacy) y lo ya cerrado pudo quedar leído contra un modelo que no existe.
Se lee sobre la rama `lectura-publico-2026-09-26`, **subida a GitHub**, para
que Mike y Claude vean exactamente el mismo PDF y Mike pueda señalar errores
por página. Las dos pasadas anteriores quedan abajo como histórico.

Orden (acordado 2026-09-26): P1, P4, P5, P7, P8, P9, P10 sin riesgo; P2 y P3
enteros dejando marcado dónde entran las sondas nuevas (SNe; ACT/SPT); **P6 y
los consolidados al final**, porque dependen del veredicto de la conjunta.

| Paper | Páginas (pdfinfo, 2026-09-26) | Estado |
|---|---|---|
| 1 — Framework | 35 | 🔵 siguiente: pág. 1 |
| 4 — ToE | 19 | ⬜ |
| 5 — IS | 33 | ⬜ |
| 7 — EFT | 17 | ⬜ |
| 8 — Strong gravity | 19 | ⬜ |
| 9 — Hubble | 22 | ⬜ |
| 10 — UV | 16 | ⬜ |
| 2 — MCMC | 32 | ⬜ (dejar hueco: SNe nuevas) |
| 3 — CMB | 26 | ⬜ (dejar hueco: ACT DR6 / SPT-3G) |
| 6 — Growth | 17 | ⬜ al final (conjunta) |

Pendiente anotado para cuando se llegue: `α_K(0)=0.403302` rotulado como
kineticidad en P3, P8, Unified, Sealed y PRD, contra P7 (α_K=15.591335).

### Histórico — tabla de estado de la segunda pasada


| Paper | Páginas | Estado |
|---|---|---|
| **1 — Framework** | 33 | 🔵 EN CURSO |
| 2 — MCMC | 26 | ⬜ |
| 3 — CMB | 24 | ⬜ |
| 4 — ToE | 16 | ⬜ |
| 5 — IS | 25 | ⬜ |
| 6 — φ-DM | 24 | ⬜ |
| 7 — EFT | 16 | ⬜ |
| 8 — Strong gravity | 20 | ⬜ |
| 9 — Hubble | 18 | ⬜ |
| 10 — UV | 14 | ⬜ |

## 🔁 SEGUNDA PASADA — desde la página 1 (2026-07-27)

Mike: *«si vas a tu ritmo puede que termines en unos minutos, pero dejas muchos
huecos. Volvamos a empezar desde el principio. No estamos sólo revisando
afirmaciones: es leer todo, revisar todo —desde gráficas hasta afirmaciones— y
en el proceso ir mejorando y actualizando todo lo que sea necesario.»*

Lo que la primera pasada demostró: **cerrar una página no es cerrar la página.**
Las páginas 4 y 5 se dieron por buenas verificando números, y al volver sobre
ellas por la vía de «si la alarma sonó, hay una perturbación» aparecieron tres
defectos de redacción y 19 de política de decimales. El criterio de esta pasada
no es «el número es correcto» sino **«se comprueba de un vistazo»**.

| pág | contenido | 1ª pasada | 2ª pasada |
|---|---|---|---|
| 1 | portada + **abstract** | ✅ | ✅ **3 huecos hallados** |
| 2 | índice | ✅ «sin contenido verificable» | ✅ **defecto de estructura** |
| 3 | §1 las 7 constantes + §1.1 | ✅ | ✅ **4 valores mal redondeados** |
| 4 | **Tabla 1** — Predictive Register | ✅→reabierta | ✅ **5 defectos + contradicción** |
| 5 | §1.2 Principios axiomáticos | ✅ | ✅ **un axioma que era tautología** |
| 6 | §1.3 Postulados D y S | ✅ | ✅ **overclaim + 3 precisiones de H₀** |
| 7 | §1.3 (cont.) Postulado I | ⬜ | 🔵 SIGUIENTE |

### 🔁 Página 3 · addendum — `=` vs `≈` (pregunta de Mike)
Mike preguntó por qué las siete constantes llevan «casi igual» si él las lee como
igualdad: *«para mí φ+π = Ω = 4.7596…»*. Tenía razón, y el paper lo decía mal.

Son **dos relaciones distintas** metidas bajo un solo signo:

```
Ω   =  π + φ      ← IGUALDAD EXACTA — es la definición, cero aproximación
π+φ ≈  4.7596     ← APROXIMACIÓN, y sólo porque el decimal está CORTADO
```

El `≈` no señala una discrepancia oculta: señala que se muestran menos dígitos de
los que hay. `4.7596…` con puntos suspensivos volvería a ser igualdad.

La lista escribía `Ω (π+φ ≈ 4.7596)` — fórmula y decimal bajo un **único** `≈`,
con lo que la definición exacta desaparecía de la vista. Reescritas las siete
(y la nota de `I_g`) como `Ω = π+φ ≈ 4.7596`, más una frase que fija la convención.
Verificado que el patrón ambiguo **no** está en los otros papers: el Unified ya usa
`= … ≃ …` y P3/P4/P7 usan tablas con `\ldots`, que también dice la verdad.

Encaja con la política: tras `=` va lo exacto a 6 decimales; tras `≈` puede ir
corto porque el signo ya avisa. Registrado en [[project_rounding_policy]].

### 🔁 Página 6 (2ª pasada) · §1.3 Postulados D y S
**Relaciones (dim. 2):** siete signos, todos correctos — `≡` define la fracción de
saturación, `∼` para el orden `10⁻⁶¹`, `≈` para el decimal truncado, `=` en las
identidades exactas. **Valores (dim. 1):** `s = T_r/M_v`, `Ω_DE = s`, `w₀ = −s`,
`1+w₀ = 1−s = s_m = 0.160050` ✓ (entonces escrito Ω_m,dyn; es ecuación de estado, no densidad); `H₀/M_Pl ∼ 10⁻⁶¹` ✓ (1.19×10⁻⁶¹).

**Hallazgo (dim. 4): un overclaim que se acota 100 líneas después.** La página
afirma «*SSEE carries one dimensional input (H₀) and **zero dimensionless** ones*».
Pero L408 dice que eso «aplica **estrictamente al sector background**» y L439 que
«quedan **exactamente dos libres**, A_s y τ». Las tres conviven, y sólo la primera
está en la página 6: un lector se lleva «cero adimensionales» a secas, que es el
overclaim exacto que un referee busca — *«usted dice cero y luego admite dos»*.
Acotado **donde se hace la afirmación**, con el k=2 vs k=6 explícito.

**Hallazgo (dim. 4, y el guardián lo amplió): TRES precisiones del mismo número.**
El ancla `3(φ+π)²` aparecía como `67.96` y `67.962` en el mismo documento — y en
**10 de 11 documentos** de la suite, 22 apariciones. Ninguna estaba «mal»
(67.962137 redondea a ambas) y por eso nadie las veía: R37 exime las dimensionales
y R30 valida cada una por separado. Unificadas a `67.962`.

→ Nueva regla **R41** (coherencia de precisión: un símbolo, una precisión por
documento). Y al correrla **encontró dos que mi barrido manual no vio**: `67.9621`
en Sealed y PRD. Eran *tres* precisiones, no dos.

> **Falso positivo instructivo.** Esos `67.9621` son **legítimos**: el texto dice
> «`73.04×(1−0.069522)=67.9621`, reproducing the anchor `3(φ+π)²=67.9621` **to four
> decimals**». Ahí mostrar cuatro decimales **es** la afirmación; recortarlo
> destruiría el argumento. Verificada la aritmética (73.04×0.930478 = 67.96212 ✓).
> R41 exenta ahora las precisiones **declaradas en el texto**. Una regla que fuerza
> coherencia ciega rompe papers correctos.
>
> Y el auto-test de la exención falló en su primera versión porque mis dos casos
> de prueba caían dentro de la misma ventana de ±200 caracteres: la exención se
> aplicaba a los dos y el test no probaba nada. Separados como en el documento real.

11 documentos + PRD recompilan exit=0. Guardián VERDE 179.
→ **CERRADA**

### 🔁 Página 5 (2ª pasada) · §1.2 Principios Axiomáticos — leída en las SEIS dimensiones
**Relaciones (dim. 2), lo primero ahora.** Los cuatro signos están bien tipados:
`∝` en el límite a→0 (la constante no se conoce), `=` en el límite a→∞ (sí se
conoce), `=` en la dependencia funcional y `≡` en la ec. (3) — identidad, no
ecuación. La asimetría `∝`/`=` dentro de la misma ecuación es deliberada y correcta.

**Hallazgo (dim. 4-5): el Principio 3 era verdadero por definición.** La ec. (3)
afirma `μ_SSEE(x)·KAL(x) ≡ 1` como axioma fundacional. Pero §4.4 (línea 771)
define `KAL(x) = 1/μ_SSEE(x)` con un `\implies`. Es decir: uno de los tres
principios del marco se cumple **trivialmente por la definición que viene 16
páginas después**. Un referee lo dice en una línea: *«su Principio 3 no es un
principio, es una definición reescrita»*.

**La salida, buscada antes de reportarlo como debilidad** (según
[[feedback_audit_philosophy]]): el contenido real del principio **sí existe** —
es que la reciprocidad sea *exacta*, sin factor `f(x)≠1` entre respuesta y
fuente. Eso restringe la teoría: fija `KAL(x)` una vez elegida `μ_SSEE(x)`. Lo
que fallaba era que el texto no lo decía y la definición parecía salida de la
nada. Ahora la ec. (3) lleva `\label`, §4.4 declara que **realiza** el principio
en vez de definirlo, y la página 5 explica qué se está afirmando.

**Legibilidad (dim. 6):** `μ_SSEE(x)` y `KAL(x)` se usaban en un principio
fundacional y no se definían hasta 506 líneas después. Añadida la definición
breve y el reenvío a Eq. (49) §4.4.

**Entidades (dim. 3):** la primera frase del Principio 3 —«estados con idénticos
valores geométricos pero funciones dinámicas divergentes»— **es literalmente** la
doctrina `I_g ≠ K_v`, y no se aprovechaba. Enlazada: el principio ahora justifica
explícitamente por qué dos registros comparten 9.519253 sin ser el mismo objeto.

**Valores (dim. 1):** sin decimales sueltos en la página. `T_r/M_v` en el límite
de Sitter = Ω_DE ✓. **Trazabilidad (dim. 5):** los tres principios se declaran
como axiomas, no como derivaciones — correcto que así sea.
→ **CERRADA**

### 🔁 Página 4 (2ª pasada) · Tabla 1 — Predictive Register
**Primero, un defecto que introduje yo en la 1ª pasada:** al añadir el criterio de
Euclid a la fila de α_K la celda quedó larguísima. Acortada a «Euclid weak lensing
2026--2028; forecast σ(α_K,0)≈0.1» + estatus «Prediction (below sensitivity)»:
dice lo mismo y cabe.

**Una contradicción viva en la misma página.** El párrafo afirmaba que «*a single
null detection would rule out the SSEE framework*» mientras la fila de α_K dice
que el valor está por debajo de la sensibilidad del experimento. No puede ser
falsable y no discriminante a la vez. Reescrito: donde la sensibilidad ya
resuelve el valor, una exclusión refuta; donde no —α_K^field— la entrada se marca
*below sensitivity* y una no-detección **no pesa en ninguna dirección**. La nota
al pie decía además «this is the Euclid weak-lensing **falsifier**», contradiciendo
a su propia tabla dos centímetros más arriba; corregida.

**Dos filas tenían las columnas cruzadas:** `γ_IS = 0.550` llevaba el VALOR en la
columna «Quantity» y una comparación en la columna «Value»; `fσ₈` igual. Un lector
que recorre la tabla en columna encuentra un valor donde espera una fórmula.
Reordenadas al contrato de la tabla.

**Y dos de política:** `ω_c = 0.11951` (5 dec) y `H₀ = 67.96` frente al 67.962 que
usa el resto de la suite. **ω_b y ω_c no estaban entre las constantes vigiladas** —
sólo el diccionario y los observables inflacionarios— así que nadie los miraba:
añadidos, y el barrido encontró **37 igualdades más** en 8 documentos (P1, P2, P3,
P4, P6, Sealed, PRD). Los valores de Planck (0.02237, 0.1200) quedaron intactos:
son datos medidos y llevan su propia precisión.

> **Dos falsas alarmas de la herramienta, no del paper.** `pdftotext` mostraba la
> fila de α_K partida en dos y un «p» suelto en S₈. Renderizando la página a
> imagen y mirándola: la tabla está perfecta y el «p» era el signo `√`. Leer el
> volcado de texto no es leer el PDF.

→ **CERRADA**

### 🔁 Página 3 (2ª pasada) · §1 las siete constantes + §1.1 Predictive Register
Las siete constantes de la lista: **todas correctas** con «≈» y bien redondeadas.

**Hallazgo mayor — cuatro valores MAL REDONDEADOS en la tabla de símbolos**
(Apéndice C, la tabla de referencia del paper). No es política: están mal.

| | exacto | decía | correcto |
|---|---|---|---|
| β | 2.379813**321** | 2.379814 | **2.379813** |
| K_v | 9.519253**285** | 9.519254 | **9.519253** |
| I_g | 9.519253**285** | 9.519254 | **9.519253** |
| T_r | 11.99354**1930** | 11.993541 | **11.993542** |

Y en el Paper 7, misma tabla: `w₀ = −0.8400` y `Ω_DE = 0.8400` cuando el exacto
−0.839**950** redondea a −0.8399.

**Por qué sobrevivieron.** R30 ancla K_v con el patrón
`\varphi+\pi+\Omega\approx([\d.]+)` — exige `\approx` **pegado**, que es la forma
de la lista de §1. En la tabla la forma es `$K_v$ & $\varphi+\pi+\Omega$ &
$9.519254$`, con `&` en medio: el patrón nunca llega. Y **β y T_r ni siquiera
tenían ancla**. R38 tampoco, porque miraba sólo la columna 1.

**R38 generalizada** — una fila afirma una igualdad de dos formas y ahora cubre
las dos: (a) `=` en la columna 1, (b) **la columna 2 ES la fórmula**, sin ningún
signo igual. Distingue *mal redondeado* (grave) de *política de 6 decimales*.
Exentos: `≈`, unidades, y `\ldots` (truncamiento explícito, que es honesto).
Auto-test de 8 filas reales. → **10 valores más** corregidos en P9 y Unified.

> **Dos trampas del propio detector, cazadas por correrlo:**
> 1. La ventana de identificación era `0.6·10⁻ᵈ` — **demasiado estrecha para ver
>    justo el error que busca**: un valor mal redondeado en el último dígito
>    dista hasta `1.5·10⁻ᵈ`. Subida a `2·10⁻ᵈ`.
> 2. `$w_0$ & $-T_r/M_v$` no se reconocía como fórmula por no llevar φ ni π
>    literales. Ampliado a cualquier expresión matemática.
>
> **Y una del método:** un script imprimió «Ω_m,dyn → 0.160050» y **no escribió
> nada** — falló después y nunca llegó al `write`. Un `print` no es una
> escritura; hay que verificar contra el archivo.

**Otros tres huecos de la página:**
- «reduction of ~35% in the area» → el área `σ_w0×σ_wa` con la media de los
  errores asimétricos de DR1 da **32.7%**. El 35% sale sólo del extremo alto.
  Corregido a **~33%** con la aritmética a la vista.
- «unique at machine precision — a 1-in-490 specificity (at ±0.0005, the
  exact-identity tolerance |d|=0)»: tres precisiones distintas en una frase.
  Reescrito en el orden que se comprueba: tolerancia **generosa** ±0.0005, cae
  **una** de 490 dentro, y esa una coincide a precisión de máquina.
- **`I_g` se usaba sin estar definido**: aparece en el abstract y en la ecuación
  central de wₐ, pero no en la lista de §1; se definía 500 líneas después.
  *(Primero lo añadí a la lista — y eso rompía el conteo «siete registros», que
  es coherente en 3 sitios y se desglosa 4 L1 + 3 L2 en el Apéndice E.
  Verificado a tiempo:* ahora va como nota justo después de la lista, sin tocar
  el conteo.*)*
→ **CERRADA**

### 🔁 Página 2 (2ª pasada) · índice
La primera pasada lo despachó como **«sin contenido verificable»**. Un índice
afirma la estructura del documento, y la estructura estaba mal.

**Los agradecimientos estaban en medio del paper.** El orden real era:

```
§4 Galaxy Cluster Dynamics
Data Availability          ← pág 22
Acknowledgements           ← pág 22
§5 Domain of Validity          (5.1 Model-Comparison Table, 5.2 Falsification Manifesto)
Apéndices A–E                  (25–33)
```

Quien llega a «Acknowledgements» en la página 22 **asume que el paper terminó** —
y lo que sigue es lo que un referee más busca: la tabla unificada de comparación
de modelos y el **Manifiesto de Falsación**. El material más falsable del paper
estaba enterrado detrás de lo que parecía el final.

Reubicados al cierre y en el orden convencional (Acknowledgements → Data
Availability), justo antes de `\appendix`. Ahora §5 va en la 22, el Manifiesto
en la 23, y los cierres en la 25. 33 pp., exit=0, docs/ sincronizado.

**Verificado además:** el índice lista todas las secciones del fuente; §2
(EFT Embedding, 8 subsecciones, pp. 10–17) vive en `\input{SSEE_EFT_section}` —
archivo aparte, a leer al llegar a esas páginas.

**Anotado al pasar (no perseguir):** el título promete «*and* Galaxy Cluster Mass
Discrepancies» y §4 ocupa ~2 páginas de 33, con 4.1/4.2/4.3 enteras en una sola
página. Desbalance título↔contenido a evaluar al llegar a la pág. 20.
→ **CERRADA**

### 🔁 Página 1 (2ª pasada) · portada + abstract
Números todos correctos: `w₀ ≈ −0.840` (−0.839950), `wₐ ≈ −0.670` (−0.669975),
`KAL₀ = β+π ≈ 5.5214` (5.521406), `r = φ⁻¹⁰ = 0.008131`, `ΔBIC = −6.43`
(CANONICAL `deltaBIC_lcdm_minus_ssee: 6.43`, signo correcto), 7 registros. Sin
figuras. **La primera pasada los verificó y cerró la página. Había tres huecos.**

1. **El abstract colapsaba dos entidades.** Escribía ambos denominadores como
   `2(φ+π)`, mientras el cuerpo (§583–585) distingue `w₀ = −T_r/M_v` de
   `wₐ = −P/I_g`. El abstract contradecía a su propio cuerpo. Restaurado el
   linaje delante de la reducción, con la aclaración a la vista.
   *(Y al escribirla puse «M_v = I_g = 9.519253», que es falso —M_v = 14.278880—:
   colapsé las entidades justo al explicar por qué no deben colapsarse. Cazado
   antes de compilar. La forma REDUCIDA comparte 2(φ+π); el LINAJE no.)*
2. **Subdeclaraba los problemas abiertos:** decía «(OP-9, OP-11)» cuando el
   sector oscuro tiene cuatro abiertos — **OP-9, OP-10, OP-11, OP-12**. Enumerar
   parcialmente es peor que no enumerar. Corregido a los cuatro.
3. **`\date{April 2026}`** en un documento con resultados de junio–julio (reframe
   ω_m-directo, Ω_m=0.308881, DESI DR2). 🟡 **NO tocado**: la fecha de un
   preprint es un acto de registro, no una corrección técnica — decide Mike.

Compila exit=0, 33 pp., docs/ sincronizado, guardián VERDE 172.

---

## Bitácora — Paper 1 · PRIMERA pasada (histórico)

| pág | contenido | estado |
|---|---|---|
| 1 | portada + **abstract** | ✅ |
| 2 | índice | ✅ (sin contenido verificable) |
| 3 | §1 las 7 constantes + §1.1 Predictive Register | ✅ |
| 4 | **Tabla 1** — Predictive Register (17 filas) | ✅ |
| 5 | Principio 3 + §1.3 alcance + **Postulados D y S** | ✅ |
| 6 | endpoints de S + **Postulados M (retirado) e I** | ✅ |
| 7 | — | 🔵 SIGUIENTE |
| 8–33 | — | ⬜ |

### Página 6 · Postulado M retirado, Postulado I, y f_screen
Ocho afirmaciones verificadas, **todas correctas**, dos de ellas identidades
exactas a precisión de máquina: `1+w₀ = 1−s = s_m` (0.160050; entonces escrito Ω_m,dyn),
`ω_b = (π−φ)/(3Ω²)` (0.022418 → «0.02242»), `ω_c = KAL₀·ω_b·n_s` (0.119514),
`Ω_m,CMB = ω_m/h² = 0.308881`, `MIRA = (3φ+π)/4 = AURA/2` (las dos formas dan
1.998924), `N* = 2φ⁷ = 58.068884` con 2φ⁶=35.889 y 2φ⁸=93.957 fuera de [50,60],
`n_s = 1−2/N* = 1−φ⁻⁷` y `r = 12α/N*² = φ⁻¹⁰` (identidades exactas).

**Hallazgo — el símbolo pelado otra vez.** La página escribe
`f_screen = α_K/(3·MIRA) = (π−φ)/Ω²` con **α_K sin superíndice**, y la identidad
sólo es cierta con uno de los dos:

| | resultado | vs (π−φ)/Ω² = 0.067253 |
|---|---|---|
| α_K^eff = 0.403302 | **0.067253** | exacto ✓ |
| α_K^field = 0.072567 | 0.012101 | factor 5.6 fuera ✗ |

Un lector que tome el α_K de la Tabla 1 —que es el `field`— obtiene un número
que no es el de la ecuación. La aritmética decide sin ambigüedad, así que se
marcó `α_K^{\rm eff}` en **12 sitios de 6 documentos** (P1×4, P4, P7, P8×2,
Sealed×2, PRD×2). **P9 y P10 NO** — son los que derivan la fórmula y se revisan
al llegar. Paper 1 recompila limpio, 33 pp.
→ **CERRADA**  ·  residuo anotado como **FP-5**

### ⚠ Reapertura de las páginas 4 y 5 — «si la alarma sonó, hay una perturbación»
Cerré dos alarmas verificando el NÚMERO y declarándolas «nada». Mike lo corrigió:
si al leer con atención me confundí, **un referee se confunde igual** — la causa
no era el número, era el texto. Verificado que ambas tenían causa real:

**Causa A (pág. 5).** «*Two* foundational postulates… both are stated here» y a
continuación **cuatro viñetas** (D, S, M retirado, I). La aclaración —dos
fundacionales + una auxiliar = tres— llegaba **110 líneas después**. Reescrito
para anunciar la estructura completa **antes** de las viñetas.

**Causa B (pág. 4, Tabla 1).** La fila de α_K era **la única de su bloque sin
criterio**: la de α_T lleva «GW170817 $|\alpha_T|<10^{-15}$», la de S₈ lleva
«KiDS-1000 $0.759\pm0.024$ (0.04σ)», y la de α_K sólo decía «Euclid weak
lensing, 2026–2028». Sin la precisión a la vista es imposible juzgar de un
vistazo si 0.072567 pasa. **Esa fila fue la que me mandó a saltar de paper.**
Ahora lleva «$\sigma(\alpha_{K,0})\approx0.1$: value lies *below* the forecast
error bar» y el estatus «Prediction (not yet discriminating)».

**Y al mirarla de cerca, un tercer caso:** `r = φ⁻¹⁰ | 0.00813` — cinco
decimales. R37 no lo veía porque **el «=» está en una celda y el número en
otra**. Barrido de toda la suite con ese patrón → **19 casos en 6 documentos**
corregidos a 6 decimales (P1×4, P5, P9, Sealed×3, Unified×7, PRD×3).
→ Nueva regla **R38** en el guardián, con auto-test permanente. VERDE **172**.

> **Trampa registrada:** mi primer barrido devolvió «0 casos» y era VACÍO —
> comparaba contra el redondeo correcto, y `0.00813` **sí** es el redondeo
> correcto de 0.008130618 a 5 decimales. Lo que se violaba era la **política**
> (un «=» lleva 6 decimales), no el redondeo. Medir lo que no es se ve idéntico
> a estar limpio.

### Página 5 · §1.3 — alcance del «cero parámetros», Postulados D y S
Verificadas las cuatro afirmaciones numéricas: `3(φ+π)² ≈ 67.96` (67.962137 ✓),
`s = T_r/M_v = 0.839950` con `Ω_DE = s` y `w₀ = −s` ✓, `H₀/M_Pl ∼ 10⁻⁶¹`
(1.19×10⁻⁶¹ ✓, con M_Pl estándar), y el conteo de ΛCDM = 1 dimensional (H₀) +
5 adimensionales ✓.

**Alarma verificada y descartada:** la página dice «two foundational postulates»
mientras la 4 dice «three register-level postulates (D, S, I)». No es
contradicción — la §1.3 lo enuncia explícito: **dos fundacionales (D, S) más uno
auxiliar (I) = tres**, y el entero n=7 dentro de I es corolario, no supuesto.
Cierra en las tres líneas donde aparece el conteo (236, 247, 357).
→ **CERRADA**

### Página 4 · Tabla 1 — Predictive Register (17 filas)
Verificadas fila por fila contra `ssee_core`: w₀, wₐ, ωc, Ω_m,CMB, n_s, H₀, γ_IS,
fσ₈, m_φ, k_fs, S₈, α_T/M/B, β_c, r. Todas correctas y con su clasificación
epistémica sostenible (postdicción / predicción / retrodicción).

**Falsa alarma bien cazada:** la fila de α_K decía **0.073** mientras toda la
suite usa **0.403302**. Parecía contradicción — y NO lo es: son dos kineticidades
físicamente distintas, α_K^bare = 3Ω_DE(1+w_φ) con w_φ=−0.971202 (el falsador de
Euclid) frente a α_K^eff = 3Ω_DE(1+w₀). El paper lo explica… **20 líneas después
de la tabla**. Un lector que compare con Paper 7 concluye «se contradicen» antes
de llegar a la nota.
→ La fila ahora se llama **α_K^bare**, autosuficiente. Símbolo distinto para
entidad distinta, que es la misma ley que aplicamos a I_g vs K_v.

**Y dos cadenas con intermedios redondeados:** `3×0.840×0.029 = 0.073` no
reproduce el exacto (da 0.0731). Corregidas a `3×0.839950×0.028798 = 0.072567`
en Paper 3 y Unified. R37 ampliada a 16 constantes (+α_K^bare) → 13 correcciones
en 5 documentos más.
→ **CERRADA**

### Página 1 · abstract
Verificados: w₀ ≈ −0.840, wₐ ≈ −0.670, KAL₀ ≈ 5.5214 (los tres con «≈», cortos
pero bien redondeados ✓); ωc = KAL₀·ωb·ns (identidad forward ✓);
ΔBIC = −6.43 del sector dinámico (coincide con CANONICAL_VALUES, signo correcto:
ΛCDM−SSEE = +6.43 ⟹ SSEE−ΛCDM = −6.43 ✓).
**Hallazgo:** `r = φ⁻¹⁰ = 0.00813` lleva signo IGUAL y sólo 5 decimales →
**0.008131**. R37 no lo cazaba: su lista tenía las constantes del diccionario
pero no los OBSERVABLES algebraicos, que son igual de puros en φ,π.
Ampliada de 10 a 15 constantes (+r, n_s, α, N_*, α_K) → **48 correcciones en 14
documentos**. → **CERRADA**



### Afirmación 1 · §1 pág. 1 — la lista de las siete constantes fundacionales
**Dice:** Ω≈4.7596, β≈2.3798, KAL₀≈5.5214, P≈6.3776, K_v≈9.5192, T_r≈11.9935,
M_v≈14.2788.
**Verificado contra `ssee_core`:** cuatro correctas. **TRES TRUNCADAS**, no
redondeadas — en la primera página del paper que define el diccionario:

| | exacto | decía | correcto |
|---|---|---|---|
| P (PYROS) | 6.377661 | 6.3776 | **6.3777** |
| K_v | 9.519253 | 9.5192 | **9.5193** |
| M_v | 14.278880 | 14.2788 | **14.2789** |

Corregidas en **14 sitios de 5 documentos** (P1, P4, P6, P9, Unified) — regar el
árbol, no sólo donde se vio. Ancladas en R30 (12 cantidades × 18 documentos).
→ **CERRADA**

### Afirmación 2 · §3 ec. (w₀,wₐ) — la caja destacada
**Dice:** `w₀ = −(3φ+π)/(2(φ+π)) = −0.8399`, `wₐ = −(2φ+π)/(2(φ+π)) = −0.6699`.
**Dos hallazgos:**
1. **`−0.6699` está MAL.** Exacto −0.669974886 → a 4 decimales **−0.6700**
   (el 5.º dígito es 7). Error 7.5e−5, por encima de la media unidad. Corregido
   en P1, P4, P5 y P6. (`w₀ = −0.8399` sí es correcto: su 5.º dígito es 4.)
2. **La entidad estaba colapsada a su reducción.** La forma `(2φ+π)/(2(φ+π))`
   es algebraicamente correcta —equivale exacto a P/I_g— pero aparecía SOLA.
   Los dos denominadores dan el mismo número, 9.5193, y son entidades
   DISTINTAS: M_v = φ+π+K_v vs I_g = π+P. Ningún chequeo numérico las separa;
   sólo la construcción. Restaurado el linaje delante de la reducción, con nota
   explícita de por qué el orden importa.
→ **CERRADA**

### Afirmación 3 · §1.1 — Predictive Register y el look-elsewhere
**Dice:** el diccionario cerrado da 490 razones en (0,5]; cada valor de la
ecuación de estado lo acierta UNA sola, a ±0.0005 — especificidad 1-en-490.
**Verificado** corriendo `look_elsewhere_full.py`: 490 razones, **1 acierto**
para w₀ y 1 para wₐ. Y la robustez: extendiendo el diccionario a 664 razones
(QUINTAL…DECAL) los aciertos NO aumentan. La afirmación central se sostiene.
→ **CERRADA**

**Pero dos cifras acompañantes NO tenían respaldo:**

1. **«DR1→DR2 shrank the uncertainties by ~40%»** — sin fuente localizable: no
   está en logs, ni en CANONICAL_VALUES, ni hay datos DR1 en el repo, y la
   búsqueda en la literatura no devolvió los valores con la precisión necesaria.
   **RETIRADA.** El texto ahora afirma sólo lo respaldado: el punto es inmóvil y
   el dato pasó dos veces sin excluirlo (0.05σ de DR1, 0.24σ de DR2), dentro del
   68% en ambos.

2. **«DR3 ~1.5× más preciso → ~0.5σ»** — no se deduce de su propia premisa. Con
   el punto fijo la tensión escala con el inverso del error: 1.5 × 0.24 = **0.36σ**.
   Para 0.5σ haría falta 2.1×. **CORREGIDA a 0.36σ**, y reescrita para mostrar la
   aritmética (1.5× → 0.36σ, 3× → 0.7σ) en vez de una cifra suelta.

## Anotado al pasar (NO perseguir hasta cerrar la pregunta en curso)

- **FP-4 · Paper 7 líneas 553 y 584** — dos sobreafirmaciones sobre la EVIDENCIA
  (ninguna toca un número): la falsación de Euclid confunde precisión σ con cota
  superior, y el «hi\_class confirma independientemente al 0.005%» es la misma
  fórmula evaluada dos veces. Verificado que **no está en Paper 1**. Se atiende
  **al llegar al Paper 7**; si aparece en Papers 2–6, allí. Detalle y corrección
  propuesta en `FUENTES_PENDIENTES.md`.
  → *Lección de método: esto se detectó saltando del Paper 1 al Paper 7. La regla
  es anotar y volver, no perseguir.*

- Propagar a Paper 3 los ΔBIC verificados hoy: plik_lite −24.02 y plik full
  −25.77 (hoy sólo viven en PRD/Sealed y en el Registro).
- Los Papers muestran menos decimales que los consolidados (0.4033 vs 0.403302).
  No es error —son redondeos correctos— pero R30 ya vigila las 9 anclas en los
  18 documentos.

---

## Segunda pasada — Paper 1, página 7 (aviso previo: el ancla H₀)

Antes de entrar a la página 7 Mike hizo la pregunta que cerró un hueco de tipo
**dimensional**, no numérico:

> «Recuerda que está el H con unidades y el sin unidades — ese sí es el algebraico.
> `3(φ+π)²` es un número puro; el que tiene unidades es el H_global derivado desde
> SH0ES. No digo que sean iguales: más bien es una **similitud estructural**.»

**Lo que quedó en pie.** La prosa ya lo dice desde el Postulado D («the
*dimensionless* value is fixed algebraically, while the *absolute* scale is not
claimed to be derived»). No había que corregir física.

**Lo que cambió — la notación contradecía a la prosa.** Se escribía
`H_0 = 3(φ+π)²` con «=» pelado: una tasa en km/s/Mpc igualada a un irracional
adimensional. Corregido en **Paper 1** (7 sitios) a `H_0 = 3(φ+π)² km s⁻¹ Mpc⁻¹`,
con macro `\kmsu` para que la unidad no se pierda al copiar la expresión.

**Hallazgo adicional, apéndice OP-1 (L1458).** Se leía
`Ω_b h² = (π−φ)/[3(φ+π)²] = (π−φ)/H_0^SSEE`: la segunda forma divide un
adimensional por una tasa física, y además haría la identidad **dependiente de la
unidad elegida para H₀**. Reescrito: el contenido es la relación entre números
puros, y se dice explícitamente por qué no se escribe de la otra forma.

**Contramedida — R42 (tipo dimensional).** R40 vigila truncamiento (`=` vs `≈`);
R42 vigila dimensión (número puro vs cantidad física). Incluye exención de
**mención** (un texto que explica por qué una forma es incorrecta tiene que poder
escribirla, y se reconoce por la negación que la precede).

**La primera versión de R42 era parcialmente vacía y Mike lo preguntó antes de
seguir.** Yo había afirmado que «la corrida hacia atrás encontró el sitio de la
página 4»; no era cierto — ese sitio lo hallé con `grep` y lo corregí *antes* de
escribir la regla, y la regla, probada contra la versión previa, **no lo cazaba**:
aceptaba cualquier unidad dentro de los 28 caracteres siguientes, incluida la de
la **columna siguiente** de la tabla (L177) y la que va **tras el decimal** (L803).
Corregido: la unidad debe ir *pegada*. Prueba contra el commit anterior:

| | hallazgos en Paper 1 |
|---|---|
| R42 v1 | 5 — se le escapaban L177 (**pág. 4**) y L803 (pág. 22) |
| R42 v2 | **8** |
| Paper 1 hoy | **0** |

Mapa de páginas: **pág. 4** (tabla, *ya cerrada*), 7, 8, 10, 22, 27 ×2 y el
apéndice OP-1. De los ocho, **uno solo** caía en el tramo ya revisado; el resto
estaba por delante. Guardián **VERDE 181**.

*Alcance honesto:* R42 cubre el patrón `H_0 = 3(φ+π)²` y la división de un
adimensional por H₀ físico. **No** cubre todo colapso dimensional posible
(`m_φ`, `r_d`, `M` en meV); esos se miran al leer sus documentos.

**Anotado, no perseguido** (`FUENTES_PENDIENTES.md`, FP-6b): la asimetría IR/UV
—forward limpio, inverso inflado a «cuatro decimales»—, el `0.00σ` pelado de la
tabla L411 de Paper 10 y el residuo `4×10⁻⁶` no reproducible. **41 sitios** de
`=` sin unidad siguen abiertos en el resto de la suite.

---

## Segunda pasada — Paper 1, página 7 (Postulados auxiliares M e I) · CERRADA

Cuatro hallazgos, en cuatro dimensiones distintas. Ninguno lo vio el guardián.

**1 · Coherencia — el párrafo anuncia dos postulados y concluye uno.** El
encabezado decía «the framework rests on **two** additional auxiliary postulates»
y el cierre, catorce líneas después, «two foundational (D, S) plus **one**
auxiliary (I) — three total». Residuo de haber retirado el Postulado M sin
actualizar el encabezado. Reescrito a «*one* additional auxiliary postulate», con
M conservado en la lista y marcado como retirado — para que la **reducción** del
presupuesto de supuestos sea auditable en vez de silenciosa. *(Es el mismo defecto
que Mike ya había cazado en la pág. 4/5: anunciar un número y listar otro.)*

**2 · Relaciones y valores — dos igualdades falsas en el argumento de n=7.**
Se escribía `(2φ⁶ = 35.9, 2φ⁷ = 58.068884, 2φ⁸ = 94.0)`: tres precisiones en un
renglón (1, 6, 1 decimales) y dos afirmaciones falsas bajo `=` —
`2φ⁶ = 35.888544` y `2φ⁸ = 93.957428`. Corregidas a 6 decimales, y añadido qué
hace cada una («the first falls below the window, the third above it»), que era
el contenido del paréntesis y no se decía.

**3 · Precisión — `Ω_m,dyn = 0.160` junto a `Ω_m,CMB = 0.308881`.** Tres decimales
contra seis, en la misma frase, **nueve veces** en el documento, con el apéndice
dando `0.160050`. Las **22** apariciones pasan a `0.160050`.

**4 · Mi propio texto** — escribí «we list it here, *struck*» y no está tachada.
Corregido a «marked as such».

### Por qué el guardián no vio nada, y qué se instaló

`Ω_m,dyn` caía en el **hueco exacto entre dos reglas**: R37 no lo miraba (no estaba
en su lista de constantes) y R41 lo saltaba (sólo cubre cantidades *con unidades*).
Y las potencias de φ no las cubría nadie.

- **R43** — potencias de φ con `=`: el decimal debe ser el valor a 6 decimales.
  Anclada en la **expresión**, no en el número. *Se intentó primero ampliar R37 a
  un decimal: **inservible** — «= 12.0», «= 2.3», «= 1.0», «= 6.4» cazan χ², z_S y
  tolerancias; 7 falsos positivos y 0 verdaderos.*
- **R44** — `Ω_m,dyn` con `=` a 6 decimales. Su primera versión también arrancaba
  en un decimal y disparó al instante con «= 0.2» (a un decimal, 0.160050 redondea
  a 0.2). Corregida y convertida en caso de prueba.
- **Frontera de lectura** (`_LEIDOS`) — las reglas nacidas de la lectura se
  **exigen** en los documentos ya leídos y se **cuentan como deuda** en el resto,
  con dos condiciones: la deuda se imprime siempre y **sólo puede bajar**. Deuda
  hoy: R42 49 · R43 24 · R44 100.

Prueba hacia atrás (contra el commit anterior, no contra el corregido):
R43 **2 → 0**, R44 **10 → 0**. Guardián **VERDE 188**. Paper 1: 34 pp, 0 errores.

---

## Segunda pasada — Paper 1, página 8 (contabilidad honesta y §1.4) · CERRADA

**1 · Coherencia — un OP abierto y cerrado en la misma página.** Arriba:
«the remaining open problems **OP-9/11/14** for the dark-matter sector»; veinte
líneas más abajo: «…**closing OP-14**». Y `OPEN_PROBLEMS.md` lo da **✅ RESUELTO
desde 2026-06-04**. Corregido a «OP-9 and OP-11», con una frase que dice
explícitamente que OP-14 está cerrado y dónde verificarlo.

> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
**2 · Precisión — `SOLAR²·KRYSTOS_V = 594.28`** *(lectura histórica: el multiplicador
murió con la partícula el 2026-08-01; se conserva porque la observación sobre la
falsa precisión sigue valiendo para cualquier otro número).* Dos decimales con signo igual,
siendo un número puro en (φ,π) (SOLAR = φ+2π, KRYSTOS_V = 2Ω). Valor exacto
**594.279999**; a 6 decimales por política. *(De paso: el multiplicador cae a
1.1×10⁻⁶ de 594.28 redondo — el paper no lo comenta y no lo hemos añadido.)*

**3 · Estructura — una lista de «parámetros efectivos» cuya primera entrada niega
serlo.** La viñeta 1 decía «The CMB matter density is **no longer** an effective
parameter … What remains:» — una negación dentro de la lista, terminada en dos
puntos colgando. Sacada del `itemize` al párrafo introductorio: la lista queda con
las dos entradas que sí son parámetros efectivos.

**4 · Trazabilidad — «Ω_m via ω_c».** El conteo k=2 decía que SSEE fija Ω_m «via
ω_c = KAL₀ω_b n_s», pero Ω_m,CMB = ω_m/h² necesita además ω_b, ω_ν y h. No era
falso —todos están fijados— pero obligaba al lector a reconstruirlo. Explicitado.

**Verificado y descartado (no eran defectos):** la referencia «Table 7» resuelve a
la cadena de derivación, que **sí** contiene la fila de Σm_ν; y esa fila,
`Σm_ν = R₂ ω_b · 93.14/(τ_Π H₀)`, **no** divide por un H₀ físico — `τ_Π H₀` está
declarado adimensional (≈2.191), y la aritmética da 0.0685 eV. También la frase
«zero-parameter status» está acotada en su propia oración al sector background.

### Contramedidas

- **R45 — estado de los OP**: la prosa se cruza contra `OPEN_PROBLEMS.md`, que es
  la fuente. Ningún número estaba mal, y por eso ninguna regla numérica podía
  verlo: era una contradicción de **coherencia**. *Su auto-test falló a la primera
  y por el motivo que importaba: `OP-(\d+)` sólo leía el «9» de «OP-9/11/14» y se
  perdía justo los dos de la lista con barras.*
- **R44 generalizada** de una constante suelta a las **constantes de la lectura**
  (Ω_m,dyn + SOLAR²·K_v). Nacen aquí y no en R37 porque R37 es global por diseño y
  estas aún tienen deuda; cuando su deuda llegue a cero, su sitio es R37.
- *Aviso de método:* el primer intento de generalizar R44 sólo alcanzó los
  **mensajes** y no el código — el guardián quedó un momento diciendo «casos
  reales de las págs. 7 y 8» mientras probaba sólo la 7. Un VERDE que describe
  trabajo no hecho. Detectado al comparar la deuda esperada (112) con la impresa
  (100).

Prueba hacia atrás (commit anterior): R44 **1 → 0**, R45 **1 → 0**.
Guardián **VERDE 191**. Paper 1: 34 pp, 0 errores. Deuda: R42 49 · R43 24 ·
R44 112 · R45 8.
