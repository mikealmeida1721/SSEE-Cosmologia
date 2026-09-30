# SSEE — Lista de Rigurosidad (Estándar de Auditoría)

> Cada regla de esta lista nació de algo que **se pasó por alto** en auditorías
> previas. Es el estándar de revisión obligatorio antes de enviar cualquier
> manuscrito. Cuando se detecte un nuevo tipo de fallo, se **marca aquí** para que
> el sistema de auditoría no vuelva a dejarlo pasar.
>
> Leyenda: 🔴 letal (hunde el paper) · 🟠 grave · 🟡 de presentación
> Estado: ⛔ se pasó por alto en el pasado · ✅ regla activa

---

## R1 — Prioridad temporal: verificar fechas SIEMPRE 🔴 ⛔
**Regla:** nunca afirmar "prior to / predating / before / committed before [dataset]"
sin verificar que la fecha del registro (DOI, commit, Zenodo) es **objetivamente
anterior** a la fecha de publicación del dataset.
**Por qué (caso real):** los papers afirmaban que MIRA/w₀ fueron "fixed prior to
DESI DR2", citando Zenodo 19679049 (**2026-01-28**). DESI DR2 es **2025-03-19**.
El registro es ~10 meses POSTERIOR. Una línea decía literalmente "2026 January 28,
prior to the DESI DR2 release on 2025 March 19" — cronológicamente imposible.
**Verificación:** `grep -rniE "predat|prior to|before (desi|the release)|committed before|timestamp"` en todos los `.tex`; cruzar cada fecha contra la del dato.
**Marco correcto:** el match con datos ya públicos es **postdicción libre de
parámetros**; la fortaleza es la **rigidez estructural**, no la cronología. La
prioridad temporal genuina solo se reclama sobre datos NO publicados (DESI DR3, Euclid).

## R2 — Enlaces a material multidominio / numerológico 🔴 ⛔
**Regla:** ningún manuscrito, README, ni Zenodo citado puede enlazar a material que
aplique el sistema a dominios no-cosmológicos (medicina, química, paz, ADN…) ni a
versiones numerológicas crudas. Activa el detector "crackpot" del referee.
**Por qué (caso real):** el repo público `SSEE_UNIFICADO` (Génesis 5.12) aplica φ,π
a 8 dominios y tiene H₀ crudo ("73.483 = H_global + KAL") que **contradice** la
versión sofisticada de los papers (f_screen algebraico).
**Verificación:** seguir cada enlace/DOI de los papers hasta su destino final;
confirmar que solo expone estructura algebraica + física cosmológica.
**Resuelto (2026-06-14):** creado registro limpio dedicado
`SSEE-Constant-Dictionary` (Zenodo concept DOI `10.5281/zenodo.20684908`), solo
diccionario + predicciones, sin material multidominio. Todas las citas del
diccionario (P1, P2, P3, P4, Unified, Sealed + bibs + AUDIT.md) reapuntadas del
viejo `19679049` (SSEE_UNIFICADO multidominio) al DOI limpio. Disponibilidad de
**código** sigue apuntando al archivo legítimo `20093447` (serie de papers + CLASS).

## R3 — Look-elsewhere sobre el diccionario COMPLETO 🟠 ⛔
**Regla:** el conteo look-elsewhere se hace sobre TODAS las constantes del diccionario
fuente, nunca un subconjunto. Reportar la **curva de sensibilidad a la tolerancia** y
la **robustez a extensiones futuras**.
**Por qué (caso real):** el conteo usaba 21 de 31 constantes → acusable de "subset a
conveniencia". Corregido al diccionario COMPLETO (hoy **55** constantes / 25 valores
tras formalizar las leyes de linaje: 490 razones, 1/490 a ±0.0005); verificado robusto
a las copias QUINTAL–DECAL (5Ω…10Ω): el espacio crece 490→664 razones y **no añade
ningún acierto** a ±0.0005/±0.001/±0.002.
Script: `src/estadistica/look_elsewhere_full.py` · log: `results/logs/look_elsewhere_full.log`.
Vigilado por **R27** (el 55/25/490 recomputado debe coincidir con el que citan los .tex).

> **2026-07-25:** hasta hoy este párrafo decía «50 constantes» (stale) y afirmaba la
> robustez QUINTAL–DECAL apuntando a un script que **nunca las mencionaba**. La
> afirmación resultó cierta al computarla, pero estaba escrita sin fuente — la misma
> patología que OP-20. Ahora el script la calcula y deja log.

## R4 — Likelihoods reales, no comprimidas (modelos no-ΛCDM) 🟠 ⛔
**Regla:** no presentar distance priors comprimidos de Planck como equivalentes a la
likelihood completa de los Cℓ, especialmente en un modelo no-ΛCDM (los distance priors
se calibran asumiendo ΛCDM → posible sesgo).
**Por qué (caso real):** el MCMC Fase 4 usaba prior comprimido; un referee objeta el
sesgo. Mitigación: MCMC full con `plik_lite_native` + lensing + DESI + fσ₈ (en curso).

## R5 — Benchmark = ancla canónica, no conjetura obsoleta 🟠 ⛔
**Regla:** comparar posteriores contra el valor canónico vigente, no contra valores
heredados de iteraciones previas.
**Por qué (caso real):** el ancla canónica ha cambiado con el modelo. Era H_MIRA=67.037
(escenario MIRA), y el reframe ω_m-directo (2026-06-19) la movió a H_alg=67.962 (la CMB
minimiza ahí con ω_b,ω_c fijos por álgebra). Cualquier benchmark de H₀ debe usar el
canónico VIGENTE (hoy H_glob 67.962±0.968 ancla / 67.82±0.41 posterior DR2 con prior H_glob y r_d CAMB, 2026-09-28 —el 67.79±0.35 previo usaba el prior número puro ±0.54; el 67.95 congelaba Ω_m—; el 66.41 previo metía el sector 0.160 en E(z) —bug V-L4-DESI, superseded 2026-07-09— y el 67.16 usaba datos DR1 mal etiquetados), no un valor heredado. El guardián
+ memory_sync ahora cazan este drift automáticamente (lista `retired:` con 67.037/66.53).

## R6 — Conteo y valores exactos contra la fuente 🟡 ⛔
**Regla:** todo número citado (nº de constantes, razones, valores) debe regenerarse
desde el script/fuente, no copiarse de iteraciones previas.
**Por qué (caso real):** "21 constantes" / "29" cuando el diccionario fuente tiene 31;
valores con ruido en el último decimal copiados de un compendio viejo.

## R7 — Jerga inventada / nombres mitológicos 🟡
**Regla:** la cara del paper usa notación algebraica; los nombres de linaje (IGNIS,
SOLAR, OSIRIS…) van solo en un apéndice de linaje, nunca en ecuaciones del cuerpo.
**Por qué:** activan el detector crackpot. Pendiente de limpieza transversal en el Sealed.

## R8 — Drift de estado (notas/memorias/papers) 🟡 ⛔
**Regla:** antes de enviar, verificar que notas, memorias y papers reflejan el estado
REAL del trabajo (no un estado congelado).
**Por qué (caso real):** el vault marcaba "§8 pendiente / MCMC corriendo" cuando ya
estaba escrito, commiteado y compilado desde mayo.

## R9 — Valor de pipeline sin log que lo reproduzca 🔴 ⛔
**Regla:** ningún valor de pipeline (sección B del Registro: ΔBIC, χ²_r, H₀ posterior,
r_d, θ*, σ₈…) puede ser canónico si no existe un **log committeado** en `results/logs/`
que lo reproduzca. El valor del Registro debe **aparecer en ese log**, no estar
escrito a mano. La fuente de verdad es el log, no la tabla.
**Por qué (caso real, F1 2026-06-14):** el Registro daba ΔBIC=−24.7 y χ²_r TT=1.045
(supuesto re-anclaje Σm_ν=0.069) — valores que **no aparecían en ningún log** y que una
re-corrida CAMB desmintió (reales: −28.0 / 1.044, = los papers). El "source of truth"
estaba mal y casi se "corrigen" los papers a un valor falso. Causa: el guardián
verificaba constantes algebraicas (sección A) y memorias, pero **no** los valores de
pipeline (sección B).
**Verificación (automatizada):** la **Capa Procedencia** del guardián
(`src/verificacion/ssee_verify.py`) extrae el valor de cada fila de la sección B y exige
que aparezca en su log committeado; si no coincide → **ROJO** (probado con prueba
negativa); sin log → **ABIERTO** (grieta visible, no bloquea). Para añadir un valor de
pipeline: guardar su log en `results/logs/` y registrarlo en `PIPELINE_PROVENANCE`.

## R10 — Overclaim "zero-parameter" global 🟠 ⛔ (automatizada)
**Regla:** ningún paper afirma ser un "zero-parameter framework/model" de forma global.
El claim honesto es **scoped**: "el sector background tiene cero parámetros ajustados".
**Por qué (caso real, 2026-06-14):** el TÍTULO de Paper 1 seguía siendo "A Zero-Parameter
Framework" (+cita en P2), contradiciendo el reframe aprobado minimal-parameter y su propio
abstract. La lectura hostil lo encontró; la automatización lo blindó.
**Verificación:** Capa Manuscritos del guardián, patrón asertivo
`(achieves|is|provides…) a zero-parameter (framework|model|theory)`. NO marca claims
scoped, recantaciones ("described as… however"), ni citas de títulos.

## R11 — Conteo de la serie congelado 🟠 ⛔ (automatizada)
**Regla:** las referencias al alcance de la serie deben reflejar los **10 papers + 2
journals** actuales, no un estado anterior.
**Por qué (caso real, 2026-06-14):** el abstract de P1 decía "extensiones en Papers~3--7"
mientras el cuerpo ya decía "3--10". Stale interno.
**Verificación:** Capa Manuscritos, patrón `papers 3--[789]` y `(seven|eight|nine)-paper
series`. NO marca referencias correctas de un paper a sus previos (P8 «1--7», P10 «1--9»).

## R12 — Vigente vs archivado, con bitácora 🟠 ⛔ (automatizada)
**Regla:** cada cajón está en una de dos clases — **VIGENTE** (siempre actual, auditado:
`manuscript/`, `docs/`, `src/`, Registro, memorias…) o **ARCHIVO** (histórico, no se edita
ni se cita como vigente). Lo obsoleto se mueve a `archive/` **con entrada en la Bitácora de
Archivado** (`archive/README.md`: qué, cuándo, por qué, qué lo reemplaza). Nada obsoleto se
queda en un cajón vivo sin marcar; nada se archiva sin entrada.
**Por qué (caso real, 2026-06-14):** el `archive/` mezclaba PDFs viejos, código superado y
figuras sin un "cuándo/por qué" completo; el README de archivo era parcial e inexacto. Sin
un mapa de vigencia, lo viejo se confunde con lo vivo.
**Verificación:** **Capa Archivo** del guardián — toda subcarpeta de `archive/` debe estar
documentada en la bitácora; cajón sin entrada → **ROJO** (probado con prueba negativa).
Mapa de Vigencia completo en `archive/README.md`.

---

## Protocolo de uso
1. Antes de cada envío, recorrer R1–R9 con sus comandos de verificación.
2. Cualquier hallazgo nuevo de "esto se pasó por alto" → **añadir una regla R-n aquí**.
3. La auditoría referee-hostil de los 10 papers usa esta lista como base.
4. Correr el guardián (`src/verificacion/ssee_verify.py`) — debe dar VERDE — antes de
   cualquier sello, commit de resultados o actualización de Zenodo.

## R13 — No vaciar el hueco al quitar un nombre 🟠
**Regla:** en los papers, un nombre del sistema (MIKAEL_V, KRYSTOS, DNAV…) codifica una
**función/ley** del sistema SSEE. Al quitarlo NO se deja un hueco: o (a) se conserva en la
columna de linaje/rol-de-sistema claramente etiquetada como andamiaje heurístico (como hace
la tabla de notación de P1), o (b) si sale de la prosa, se reemplaza por su etiqueta neutra
**ya establecida** (p.ej. "geometric form"), nunca por nada. La cara es álgebra; la función
vive en la capa de linaje + el diccionario citado.
**Por qué (caso real, 2026-06-14):** quité "MIKAEL_V" de la tabla de notación dejando a M_v
como única fila sin nombre de sistema → inconsistente y con el hueco vacío. Revertido. Las
leyes (copia / no-auto-suma) se pierden si se borra el nombre sin reemplazo que las preserve.

## R14 — Covarianza BAO: justificar el bloque-diagonal, no solo declararlo 🟡 (documentación)
**Regla:** al usar el vector comprimido de DESI DR2 con covarianza bloque-diagonal
(2×2 $D_M$–$D_H$ por tracer, sin términos inter-tracer), NO basta con decir "puede
subestimar errores": hay que **justificar** por qué es legítimo, o un referee lo lee como
atajo.
**Justificación (en acta, aplicada en Paper 2 nota al pie §III):** el producto público de
DESI entrega correlaciones $r_{MH}$ **por tracer** (Tabla 4, 2503.14738) pero **no** una
matriz inter-tracer, porque las cinco poblaciones ocupan cáscaras de redshift casi disjuntas
($0.3\lesssim z\lesssim2.3$) → sus medidas BAO son casi independientes; el único par que
solapa (LRG3+ELG) DESI ya lo reporta como bin combinado, absorbiendo esa correlación aguas
arriba. Es **exactamente** como se debe usar el vector consenso comprimido. El término
off-diagonal dominante ($D_M$–$D_H$ intra-tracer, $|r_{MH}|\!\sim\!0.4$) **sí** está incluido.
**Estado:** ✅ documentado (no requiere re-correr; el código en `src/desi_dr2_data.py` ya
construye esta covarianza). Si un referee insiste, un re-run con covarianza inflada cierra el
punto, pero no es necesario para que la afirmación sea honesta.

## R20 — Ancla observacional en código ⊆ CANONICAL_VALUES.yaml 🔴 ⛔ (automatizada)
**Regla:** ninguna constante **observacional** (el DATO medido: KiDS S₈, DES S₈, KiDS σ₈…)
hardcodeada en `src/` puede diferir del ancla en `CANONICAL_VALUES.yaml §observational_anchors`.
**Por qué existe:** punto ciego cazado por auditoría externa (2026-07-13, H2). El script
`ssee_paper6_verification.py` tenía `kids_s8 = 0.758` — pero 0.758 era la **predicción SSEE** de entonces (retirada 2026-08-01),
no la observación KiDS (**0.759**). Metía la predicción en el hueco del dato, imprimiendo
**0.00σ** en vez del **0.04σ** real. Ningún patrón "retirado" lo cazaba porque 0.758 es un valor
vigente legítimo; la falla era **semántica** (dato vs predicción), no un valor obsoleto.
**Automatización:** capa R20 del guardián — lee las anclas del YAML y verifica que
`kids_s8`, `kids_sig8`, `des_s8` en todo `src/**.py` coincidan. Si alguien vuelve a meter la
predicción como dato → ROJO. Los papers ya eran correctos (0.04σ); el error vivía solo en código.
**Estado:** ✅ corregido + automatizado.

## R21 — Un préstamo se declara y se CUENTA como libre 🔴 ⛔
**Regla (formulada por M. Almeida, 2026-09-08):** cada modelo entra en un cálculo
con **el ingrediente que ese modelo tiene**, leído de su propia fuente. Si el
modelo **no lo tiene**, tomarlo prestado del otro es legítimo —al principio no
estaban derivados todos, y no se puede afirmar lo que no se tiene—, pero
entonces:

  1. **se declara** en el sitio donde se reporta el número, con su origen;
  2. **cuenta como parámetro libre**, porque no lo produce el modelo. Prestado y
     libre valen lo mismo en el conteo `k`;
  3. **se devuelve** en cuanto exista el propio, y el número se re-corre.

Un préstamo es eso: se pide, se anota de quién, y se devuelve. Lo que **no** vale
es el préstamo silencioso: usar el ingrediente ajeno, no declararlo, y además
contar `k` como si el modelo lo hubiera derivado. Eso es cobrarse una perilla
que no se ha pagado.

**Hoy SSEE tiene casi todos**, así que la regla actúa sobre todo como prohibición
del préstamo silencioso; queda escrita para cuando aparezca un ingrediente que
el modelo no derive y ΛCDM sí mida con precisión.

**Además:** lo que está fijo y lo que está libre se elige **por lo que se
pregunta**, no por comodidad. Para SSEE, el fondo por álgebra y libres sólo sus
dos; para ΛCDM, el fondo libre, que es como lo hace su propia comunidad.
**Los dos casos reales de hoy NO eran préstamos legítimos, eran silenciosos:**
en los dos, SSEE **sí tenía** su propio valor y aun así se usó el ajeno. Lo que está fijo y lo que está libre se elige **por lo que se pregunta**,
no por comodidad: para SSEE, el fondo por álgebra y libres sólo sus dos; para
ΛCDM, el fondo libre, que es como lo hace su propia comunidad.
**Por qué (dos casos reales, el mismo día 2026-09-08):**
1. El `ΔBIC = −24.02` de Paper 3 evaluaba SSEE con el `τ` fiducial de ΛCDM. Con
   `τ` ajustado en los dos, SSEE gana 1.82 en χ² y el ΔBIC pasa a **−22.59**.
2. `boss_lpt_R1R2.py` tenía `MNU = 0.06` suelto para **los dos** modelos. Ése es
   el fiducial de Planck; el de SSEE es `Σm_ν = 0.06849 eV`. Medido:
   σ₈ −0.276%, fσ₈ −0.247% = **0.058σ**.
**Verificación:** por cada constante de un evaluador, preguntar *¿de qué modelo
es este número?* Si la respuesta es «del fiducial» y el modelo evaluado no es
ése, es préstamo. Los ingredientes de SSEE se **leen del núcleo**, nunca se
re-teclean (R66 del guardián).
**Lección de fondo (M. Almeida, 2026-09-08):** *«no tenemos los ingredientes de
adorno; son para que den el modelo».* Un ingrediente algebraico que existe y no
se usa en la corrida es un ingrediente que no se ha probado.

## R22 — Un desvío pequeño sigue siendo un desvío 🟠 ⛔
**Regla:** que un error no mueva la conclusión **no** es razón para dejarlo. Se
corrige, se mide cuánto valía, y la medida queda escrita. Un sesgo con signo no
es ruido: varios pequeños del mismo signo se suman.
**Por qué (caso real):** el `MNU` prestado valía 0.058σ y por eso era invisible.
Llevaba ahí desde que se escribió el archivo. En el mismo día aparecieron el `τ`
prestado (1.82 en χ²) y el techo de σ₈ sin neutrinos (2.3%): tres del mismo
signo, todos «demasiado pequeños para importar» por separado.
**Verificación:** todo arreglo de este tipo lleva su número medido **antes** de
arreglarlo, en el comentario del propio código. Sin la medida no se sabe si era
pequeño; se supone.

## R23 — Al reemplazar un número, no se pierde el que había 🔴
**Regla:** cuando una corrida nueva sustituye a un número publicado, y sobre todo
cuando **sólo cambian los decimales**, el reemplazo lleva las cuatro cosas:
**(a)** de qué modelo es · **(b)** qué estaba fijo y qué libre · **(c)** su log y
su control · **(d)** el número viejo, con la razón por la que se retira. Sin (d)
no se puede volver atrás si el nuevo resulta peor.
**Por qué (advertencia de M. Almeida, 2026-09-08):** *«si sólo cambian los
decimales es muy probable que dejes algún resultado bueno por uno nuevo y
después no puedas encontrar de dónde lo sacaste».* Ya pasó en pequeño con el
`ω_c` de Paper 8: el `0.119534` publicado quedó sin log y hubo que rastrearlo
por la transcripción.
**Verificación:** la fila del Registro y la nota del `.tex` contienen las cuatro.
Y el diagnóstico condicionado **nunca** se cuela como si fuera el resultado
publicable: el techo de σ₈ con `A_s` fijo es diagnóstico; el `S₈` con `A_s`
libre contra dato crudo es el resultado.

## R24 — El control va PRIMERO, no al final 🔴 ⛔
**Regla (objeción de M. Almeida, 2026-09-08):** en un barrido que mide cuánto
aporta cada pieza, **el control se corre antes que las piezas**. Si el control
falla, todo lo medido después se tira, así que medirlo primero no es orden: es
no gastar la corrida. Y mientras el control no haya pasado, **ningún número
intermedio se reporta como resultado**, ni siquiera de paso.
**Por qué (caso real):** `punto_de_fuga2.py` dejaba su control —soltar el
parámetro que está clavado, que debe recuperar >95% del castigo— para el
**último** de cinco. Se estuvo una hora midiendo ingredientes sin saber si la
máquina hacía lo que decía. Corregido con `fuga2_control.py`, que lo corre
primero y **aborta** si no pasa.
**Verificación:** en todo script de barrido, el caso de control aparece antes
del bucle, y hay una salida temprana si no pasa.

## R25 — De uno en uno no ve las combinaciones 🟠 ⛔
**Regla (objeción de M. Almeida, 2026-09-08):** soltar las piezas **de una en
una** supone que el efecto se reparte entre culpables individuales. Puede no ser
así: dos que por separado aportan poco pueden aportar mucho **juntas**, porque
entre ellas hay degeneración. Todo barrido de uno en uno lleva al lado su
**versión conjunta**, y se compara la suma de los individuales con lo que
consiguen todos a la vez. Si el conjunto recupera bastante más, **el reparto de
uno en uno está contando de menos** y hay que decirlo al reportarlo.
**Por qué (caso real):** el punto de fuga medía `ω_b` 2.2% y `ω_c` 20.0% por
separado, y de ahí se leía «ninguno explica la protesta». Esa lectura sólo vale
si los cuatro juntos tampoco la explican, y eso **no estaba medido**.
**Verificación:** el log del barrido incluye la fila «todos a la vez» y la suma
de las individuales, las dos.
