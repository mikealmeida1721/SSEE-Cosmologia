# Afirmaciones con fuente pendiente de localizar

**Abierto 2026-07-27.** Nace de un error de método: al no encontrar la fuente de
una cifra del Paper 1, la **borré**. Mike lo corrigió:

> «No que elimines si no encuentras su origen, sino que lo marques. Puede que
> esté en otra parte donde no buscaste, o puede que no se sostenga — ¿pero cómo
> saberlo si lo eliminaste? Si mañana se borra la fuente de H, no vamos a
> eliminar H: volvemos a revisar de dónde salió y creamos la fuente.»

**Regla.** Una afirmación sin fuente localizada **no se borra**: se anota aquí
con qué dice, dónde vive, qué se buscó y qué hipótesis quedan abiertas. Sale de
esta lista de una de dos formas — se encuentra/reconstruye la prueba y se cita,
o se demuestra que es falsa y **entonces** se corrige. Nunca por no encontrarla.

Nada entra al modelo «porque sí». Si algo se sostiene sólo en intuición, no se
publica; el día que se pueda probar, entra **con su prueba**.

---

## ✅ FP-1 · «DR1→DR2 shrank the uncertainties by ~40%» — CERRADA 2026-07-27

- **Dónde:** `manuscript/SSEE_Paper1_Framework.tex:125` (§Predictive Register)
- **Estado:** ✅ **CERRADA** — fuente primaria localizada y citada
- **Buscado en:** `results/logs/`, `CANONICAL_VALUES.yaml`, `data/raw/` (no hay
  datos DR1), `archive/`, bibliografía de la suite, y literatura pública.

**Reconstrucción numérica.** Con el DR2 que ya cita Paper 2 (σ_w0 = 0.055,
σ_wa = 0.208) y los valores DR1 de literatura (σ_w0 ≈ 0.063, σ_wa ≈ 0.29):

| métrica | reducción |
|---|---|
| σ(w₀) sola | 13% |
| σ(wₐ) sola | 28% |
| **área del contorno 2D** | **37% ≈ ~40%** |

La cifra encaja con la **reducción del área del contorno (w₀,wₐ)**, que además
es la métrica correcta para la frase que la acompaña («el punto siguió dentro
del 68%»): lo que importa es el área, no cada eje por separado.

**Pendiente:** fijar los valores DR1 desde la fuente primaria (DESI 2024,
arXiv:2404.03002) y, o bien citar el área explícitamente, o bien reescribir la
frase como «el área del contorno 68% se redujo ~40%», que es lo que la cifra
mide. **No borrar hasta entonces.**

---

## ✅ FP-2 · «DR3 ~1.5× más preciso → ~0.5σ» — CERRADA 2026-07-27

- **Dónde:** `manuscript/SSEE_Paper1_Framework.tex:128`
- **Estado:** ✅ **CERRADA** — se retiró el factor inventado, no la conclusión

Las dos cifras no se deducen una de la otra. Con el punto inmóvil la tensión
escala con el inverso del error:

    1.5 × 0.24σ = 0.36σ        (no 0.5σ)
    2.0 × 0.24σ = 0.48σ ≈ 0.5σ  ✓

Y la literatura DESI describe el salto DR1→DR2 como una mejora de **factor ~2**
en las constricciones. Si DR2→DR3 repite ese factor, **0.5σ es la cifra
correcta y el «1.5×» es el intruso** — al revés de lo que supuse al principio,
cuando iba a «corregir» el 0.5σ.

**Pendiente:** confirmar el factor esperado para DR3 y dejar UNA sola cifra con
su aritmética a la vista. **No borrar hasta entonces.**

---

## Cómo se cierra una entrada

1. Se localiza o reconstruye la prueba → se cita en el `.tex` y se registra en
   `VERIFICATION_LEDGER.md` con su procedencia.
2. Se demuestra que la afirmación es falsa → se corrige el texto **citando la
   demostración**, no el silencio.

En ambos casos la entrada se archiva con la fecha y el desenlace.


---

## Desenlace de FP-1 y FP-2 (2026-07-27)

**FP-1.** Fuente primaria localizada: DESI 2024 VI (arXiv:2404.03002),
DESI+CMB+PantheonPlus da w₀ = −0.827 ± 0.063, wₐ = −0.75 (+0.29/−0.25). Contra
DR2 (w₀ = −0.838 ± 0.055, wₐ = −0.617 ± 0.208):

| métrica | reducción |
|---|---|
| σ(w₀) | 13% |
| σ(wₐ) | 23% |
| **área del contorno 68%** | **33–37%** |

La cifra era real; le faltaba la cita y el nombre de la métrica. El texto ahora
da **ambos valores con su referencia** y dice «~35% en el ÁREA del contorno»,
que es lo que la cifra mide y lo que la frase necesita. Si la hubiera borrado,
habríamos perdido un dato correcto.

**FP-2.** El «~1.5× tighter» no tenía fuente y era el número equivocado; el
«~0.5σ» era el defendible (la literatura describe DR1→DR2 como factor ~2, y
2 × 0.24σ = 0.48σ). Reescrito sin inventar factor: se enuncia la ley
—«con el punto inmóvil la tensión escala con el inverso del error»— y se da el
rango 0.4–0.5σ para un salto comparable al de DR1→DR2. La fecha 2027 se
conserva; la proyección numérica sin fuente, no.

**Lección de método:** en los dos casos mi primer impulso —borrar el 40%,
«corregir» el 0.5σ— habría empeorado el paper. Investigar antes de tocar no es
lentitud: es la diferencia entre corregir y romper.

---

## ✅ FP-3 · ¿Cuál de los dos α_K es el falsador de Euclid? — CERRADA 2026-07-27

- **Dónde:** Paper 1 Tabla 1 (fila α_K^field), Paper 7 §504/§600, PRD §4.1.
- **Estado:** ✅ **CERRADA — no había contradicción. La alarma fue mía.**

**Desenlace.** Leí `σ(α_{K,0}) < 0.1` como una **cota superior** cuando es la
**precisión** del forecast de Euclid. Con esa lectura correcta:

| valor | frente a σ=0.1 | lectura |
|---|---|---|
| α_K^field = 0.072567 | por debajo de la barra de error | indistinguible de cero, **no testeable aún** ✓ |
| α_K^eff = 0.403302 | ~4σ sobre cero | sería **detección**, no exclusión |

Nada quedaba «ya excluido». Paper 1 y Paper 7 **coinciden**: ambos ponen
α_K^field frente a Euclid, y la frase de Paper 1 («el valor usado para el
cross-check de hi\_class/EFTCAMB») es literalmente cierta — 0.403302 es lo que
se le *pasa* a esos códigos, no lo que ellos devuelven.

Queda en pie lo bueno de la investigación: la **unificación de nomenclatura**
(la misma cantidad se llamaba de tres formas y la otra de dos → ahora
α_K^field / α_K^eff en toda la suite).

→ Lo que la investigación SÍ destapó, en el Paper 7 y sólo ahí, se anota como
**FP-4** y se trata **cuando la lectura llegue al Paper 7**, no antes.

---

## FP-4 · Dos sobreafirmaciones en Paper 7 — ATENDER AL LLEGAR AL PAPER 7

- **Dónde:** `manuscript/SSEE_Paper7_EFT.tex` líneas 553 y 584 (y sus ecos en la
  Tabla `tab:alpha`, notas al pie $^a$/$^b$).
- **Estado:** 🟡 **anotado, NO perseguir** — detectado de paso mientras se leía
  Paper 1 pág. 4. Verificado que **no está en Paper 1** (su redacción es exacta).
  Verificar si aparece en Papers 2–6 al pasar por ellos.
- **No toca ningún número del modelo.** Son afirmaciones *sobre la evidencia*.

**(a) La falsación invierte el test — línea 584.**
Dice: «una detección de $\alpha_K > 0.1$ por Euclid falsificaría el EFT de SSEE».
Pero 0.1 es la **precisión** σ, no un techo. Si el que Euclid reconstruye fuera
α_K^eff = 0.403, entonces α_K > 0.1 sería justo **lo que SSEE predice** — el
paper estaría ofreciendo como falsador lo que sería su confirmación.

**(b) «hi\_class confirma independientemente al 0.005%» — línea 553.**
El script `archive/codigo/investigacion/huerfanos_2026-10-02/ssee_paper3_hiclass_check.py` (archivado 2026-10-02) calculaba:

```
línea  57:  aK_alg = 3 * Om_DE   * (1 + w0_)
línea 212:  aK_z   = 3 * Om_DE_z * (1 + weff_z)     # "desde CLASS"
```

En z=0 son **la misma cuenta**: `weff_z[0] = w0_` y `Om_DE_z[0] = Om_DE/E²(0)`
con E²(0)=1 por construcción. El 0.005% es el residuo numérico de que CLASS no
devuelve E²(0) exactamente 1. **No es confirmación independiente.** Además no es
hi\_class: usa CLASS con fluido `w0_fld/wa_fld`, sin el módulo `eft_smg` — y el
propio Paper 7 (línea 850) lista implementar hi\_class como **trabajo futuro**.

Igual con EFTCAMB: `'RPHkineticity0': alphaK_ssee` — recibe α_K como **input**,
no lo mide.

**Corrección propuesta (nada se borra):**
0. *(añadido 07-27, ver FP-5)* revisar junto con la tensión P7↔P9 sobre la
   definición de $\alpha_K$ — puede que (a) se resuelva sola al fijarla.
1. reescribir la falsación en términos de σ: a cuántas σ mediría Euclid cada
   valor, sin invertir el signo del test;
2. degradar «confirma independientemente» a lo que el script sí prueba —
   **consistencia interna de la evolución del fondo**, que es cierto;
3. conservar EFTCAMB por lo que demuestra (**ghost-free, gradient-stable**), que
   es un resultado real, y no por lo que no demuestra (el valor).

**El problema.** La suite es consistente en que existen dos kineticidades, cada
una válida en su marco (Paper 7 lo explica bien). Lo que NO queda resuelto es
cuál de las dos confronta el dato:

| | valor | qué es |
|---|---|---|
| `α_K^field` | 0.072567 | campo desnudo, antes del acoplamiento conformal |
| `α_K^eff` | 0.403302 | fondo efectivo con el w₀ **observado**; confirmado por hi_class (0.005%) y EFTCAMB |

- Paper 1 Tabla 1 y Paper 7 §600 ponen **α_K^field** frente al umbral de Euclid
  (σ(α_K,0) < 0.1) → cómodo, 0.073 < 0.1.
- Pero Paper 7 §508 dice, textual, que «the observationally relevant effective
  value is α_K^eff = 0.403302».

Si lo observacionalmente relevante es el efectivo y el umbral de Euclid es 0.1,
**0.403 > 0.1** y la predicción se leería como ya excluida. Si Euclid mide el
campo desnudo, no hay problema.

**No se resuelve con grep ni redondeos:** depende de qué cantidad reconstruye el
weak lensing de Euclid. Hay que fijarlo desde la definición de Bellini–Sawicki y
declararlo en UN solo sitio, del que los demás documentos citen.

**Riesgo si no se cierra:** es una fila marcada «Prediction» en el Predictive
Register. Un referee que tire de ese hilo encuentra dos respuestas en el mismo
paper.

**Hecho mientras tanto (nomenclatura, sin tocar la física):** la misma cantidad
se llamaba de tres formas (`α_K^field` ×7, `α_K^bare` ×2, `α_K` a secas ×7) y la
otra de dos (`α_K^eff` ×5, `α_K^fluid` ×4). Unificado a los nombres de la fuente
—**α_K^field** y **α_K^eff**— y retirada de Unified la frase «using w₀
overestimates α_K by ≈5.5», que contradecía el marco de «dos frames
autoconsistentes» de Paper 7 al presentar uno de los dos como error.

---

## FP-5 · La misma definición de α_K da dos valores en P7 y P9 — AL LLEGAR AL PAPER 7/9

- **Dónde:** `SSEE_Paper7_EFT.tex:525` vs `SSEE_Paper9_HubbleTension.tex:190,254`
- **Estado:** 🟡 **anotado, NO perseguir** — detectado desde Paper 1 pág. 6.
  **No bloquea Paper 1:** ahí la aritmética decide sin ambigüedad (ver abajo).

Los dos papers parten de la definición Bellini–Sawicki y llegan a números
distintos por un factor ≈5.6:

```
P7 §525:  α_K = 2X /(H² M_Pl²)        con X = ρ_φ(1+w_φ)/2  →  3Ω_DE(1+w_φ) = 0.072567
P9 §254:  α_K = 2X /(KAL H² M_Pl²)    →  3·AURA(π−φ)/(2(φ+π)²) = 0.403302
```

La diferencia aparente es el **K_X = 1/KAL** que P9 incluye y P7 (con K(X)=X,
K_X=1) no. Puede ser perfectamente consistente —son acciones distintas— pero
**los dos papers escriben la misma ecuación con el mismo símbolo**. Hay que
fijar cuál acción corresponde a cuál valor y decirlo en UN sitio.

**Relación con FP-4:** si esto se resuelve, probablemente resuelva también la
afirmación (b) de FP-4 — porque aclararía qué es lo que hi\_class debería
reproducir y qué significa el 0.005%.

**Ya hecho, y es independiente de cómo se resuelva:** la fórmula
`f_screen = α_K/(3·MIRA) = (π−φ)/Ω²` se citaba con el símbolo **pelado** en 12
sitios de 6 documentos. La aritmética no admite duda —sólo α_K^eff = 0.403302
da 0.067253; α_K^field da 0.012101, factor 5.6 fuera— así que el símbolo se
marcó `α_K^{\rm eff}` en P1(4), P4(1), P7(1), P8(2), Sealed(2), PRD(2).
**Paper 9 y 10 NO se tocaron**: son los que *derivan* la fórmula, con el símbolo
definido localmente, y se revisan al llegar a ellos.

---

## FP-6 · El ancla H₀: número puro vs cantidad física — SEPARAR AL LEER CADA DOCUMENTO

- **Dónde:** las 123 apariciones de `67.962` en la suite; el pasaje crítico en
  `SSEE_Sealed_Journal.tex:565-574` y su gemelo `SSEE_PRD.tex:558-567`.
- **Estado:** 🟡 **abierto, decidido el criterio — se aplica leyendo, no barriendo**
- **Decisión de Mike (2026-07-27):** separar los dos objetos.

**Los dos objetos.** El Postulado D ya los distingue («the *dimensionless* value
is fixed algebraically, while the *absolute* scale is not claimed to be derived»):

| | qué es | precisión que le toca |
|---|---|---|
| `3(φ+π)² = 67.962137…` | **número puro**, álgebra SSEE | 6 decimales |
| `H₀ = 67.96 km/s/Mpc` | cantidad **física**, vs Planck 67.36±0.54 | la del dato |

**Por qué NO se barre automáticamente.** Se simuló con el criterio «¿lleva unidad
detrás?» y clasificó **75 apariciones como adimensionales que no lo son**: son H₀
físico con la unidad omitida por brevedad (la cascada `H_local=72.86` —RETIRADA
2026-09-06, la dirección iba al revés—, la división
`67.962/(1−0.0673)`, «the chain recovers the anchor»). El criterio sintáctico no
distingue el *número* de la *cantidad*; hace falta leer. Forzarlo con una regex
introduciría 75 errores para corregir uno. **Se separa documento por documento
conforme la lectura llegue a cada uno.**

**Hallazgo asociado — comparar un número puro con una cantidad dimensional.**
El Sealed/PRD declara que `3(φ+π)²=67.962` «is a pure number with no units» y
catorce líneas después escribe: «`H₀^SH0ES(1−f_scr)=68.13 km/s/Mpc`, within
**0.17σ of the pure number** 67.962». La aritmética es correcta
(0.168 / [1.04×(1−0.06725)] = 0.173σ), pero la comparación sólo cierra si al
«número puro» se le adscriben calladamente las unidades — el mismo pecado que el
Paper 6 denuncia al retirar `m_φ = Σm_ν × H_alg` («sólo funcionaba quitándoles las
unidades»). La lógica de fondo del pasaje **sí es honesta** (no se afirma el número
puro como físico: se parte del dato medido y se des-apantalla); lo que falla es la
frase. Se corrige al leer el Sealed y el PRD, **no antes**.

### FP-6b · La asimetría IR/UV — verificada 2026-07-28

Mike señaló que el reparo anterior sólo aplica a **una** de las dos direcciones, y
tenía razón. Lo primero que había que descartar era la **circularidad**: si
`α_K^full` heredara H₀ por vía de `ρ_crit`, derivar 67.962 desde SH0ES sería dar
vueltas. **No la hay** — Paper 10 trabaja en unidades `ρ_crit = 1` (L209), donde
`M_Pl²H² = 1/3` y `M⁴/ρ_crit = 5φ⁸ = 234.89` es número puro: **H₀ se cancela**. El
único sitio donde `ρ_crit` arrastra H_alg es la conversión cosmética a `M = 9.68`
meV (L601), que no entra en `α_K`. La cadena UV es φ y π de punta a punta.

| dirección | qué entra | qué sale | estado |
|---|---|---|---|
| **forward (UV)** | álgebra (6 cifras) | `3(φ+π)²/(1−f_scr^UV) = 73.0400` vs dato `73.04` | **limpio** — se comparan las 4 c.s. que el dato tiene |
| **inverso** | dato `73.04` (**4 c.s.**) | «reproduce `67.9621` **a cuatro decimales**» | **inflado** — el dato no sostiene 6 c.s., sólo `67.96` |

La frase inflada está justamente en la dirección que **no** es la derivación, así
que corregirla no toca el resultado.

**Tres correcciones pendientes (al leer Sealed/PRD y Paper 10):**

1. **Sealed:580-581 / PRD:573-574** — «reproducing the anchor to four decimals»
   se contradice con la frase siguiente («the input is quoted at two»). `73.04`
   tiene 4 cifras significativas; el producto sostiene `67.96`, no `67.9621`.
   Bajar a dos decimales, o decir «a las cuatro cifras significativas del dato».
2. **Paper 10, tabla L411** — vende un `0.00σ` pelado. Con `σ = 1.04` ese 1σ va de
   **72.0 a 74.1**: casi cualquier valor cae dentro. Lo fuerte no es la σ sino
   *«reproduce las cuatro cifras significativas del valor central publicado»*. El
   Sealed ya lo dice bien («'to the quoted precision' rather than 'exactly'»); la
   tabla no. Sustituir la celda por «central value to 4 s.f. (cond.)».
3. **Sealed:585 / PRD:578** — el residuo `4×10⁻⁶ km/s/Mpc` **no se reproduce desde
   ningún número impreso**: reconstruido con las propias ecuaciones de Paper 10
   (`X_bg^UV = 0.36487`, `M⁴ = 234.89`, `α_K^IR = 0.403302`) da **1.3×10⁻⁵**; con
   la `f = 0.069522` que imprime el Sealed, **2.4×10⁻⁵**. Recomputar `α_K^full` a
   precisión completa y decidir cuántos dígitos mostrar.

**Fraseo adoptado (palabra de Mike):** no es una igualdad —una cantidad con
unidades no puede igualar un irracional adimensional— sino una **similitud
estructural**, cierta a la precisión que el dato publica.

**Contramedida instalada:** guardián **R42** (tipo dimensional). Paper 1 quedó
limpio; **49 sitios** siguen abiertos en el resto de la suite (P9 14, P3 8, P4 8,
Unified 7, P10 6, P2 3, P5 1, Cover 1, Endorser 1) y se cierran documento por
documento conforme la lectura llegue a cada uno.

**Primera versión de R42 tenía un falso negativo** (corregido el mismo día): daba
por buena una unidad que apareciera en cualquier punto de los 28 caracteres
siguientes, con lo que aceptaba `$H_0 = 3(\varphi+\pi)^2$ & $67.962\,\mathrm{km...}$`
—unidad en la **columna siguiente** de una tabla— y
`$H_0 = 3(\varphi+\pi)^2 \approx 67.962$\,km\,s...` —unidad tras el **decimal**—.
Ninguna de las dos se distribuye hacia atrás. Ahora la unidad debe ir **pegada**
(sólo `\,`, `~`, `\;` o espacio en medio). Con el arreglo, la versión previa del
Paper 1 arroja **8** hallazgos en vez de 5, e incluye la fila de tabla de la
**página 4**, que ya estaba dada por cerrada.

## ✅ FP-7 · La fórmula de r_d de Paper 2 va citada a Eisenstein & Hu 1998 — CERRADA 2026-09-19

**Dónde:** `manuscript/SSEE_Paper2_MCMC.tex`, ec. `eq:rd`; se usa en
`src/p02_mcmc/regenerate_fig8_bao_residuals.py` (`rd_EH`).

**Qué dice:** `r_d = 147.27 (Ω_m h²/0.1432)^−0.255 (Ω_b h²/0.02237)^−0.134 Mpc`,
«from the EisensteinHu1998 fitting formula».

**Por qué se duda (hallado por R65 el 2026-09-19 al pedir el origen de 0.1432):**
EH98 da r_s(z_d) con z_eq, z_d (con b₁, b₂) y R; no es una ley de potencias. Una
ley de potencias con pivotes en valores de Planck (0.1432 = Ω_m h² de Planck 2018
TT,TE,EE+lowE; 0.02237 = su Ω_b h²) es una aproximación posterior normalizada a
Planck. Los exponentes −0.255 / −0.134 y la normalización 147.27 hay que
encontrarlos en su fuente real, o derivarlos ajustando EH98 (o CAMB) alrededor de
ese pivote y decirlo así.

**Cómo se cierra:** localizar la referencia de esa forma exacta, o reproducir los
tres números (147.27, −0.255, −0.134) con un ajuste declarado y cambiar la cita.
El paper la usa «as an auxiliary approximation for model comparison»; el r_d
canónico (148.2 / CAMB 147.17) no depende de ella.

**Desenlace (2026-09-19, el mismo día).** Medido en
`src/p02_mcmc/verifica_formula_rd.py` → `results/logs/formula_rd_exponentes.log`:

| | r_d en el pivote | exp. ω_m | exp. ω_b |
|---|---|---|---|
| Paper 2 | 147.27 | −0.255 | −0.134 |
| EH98, derivada local | 150.86 | −0.261 | −0.132 |
| CAMB, derivada local | 147.05 | −0.257 | −0.129 |
| Aubourg 2015 / DESI (ajuste global) | 147.05 | −0.23 | −0.13 |

Es una **expansión en ley de potencias alrededor del punto de Planck**: los
exponentes son las derivadas locales (EH98 y CAMB coinciden entre sí), y la
normalización es la de Boltzmann (0.15 % de CAMB), no la de EH98 (+2.6 %). La
cita decía «the EH98 fitting formula», que era inexacto. **Corregido en el
.tex** (ahora: expansión alrededor de Planck, exponentes de EH98 local,
normalización de Boltzmann, y se compara con Aubourg et al. 2015, añadido a la
bibliografía). PDF recompilado, 0 citas sin resolver. Ningún número del paper
cambia: la fórmula es la misma, sólo se dice bien de dónde sale.
