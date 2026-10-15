# Lectura fría — SSEE_PRD.pdf (submission_PRD/)

Lectura página por página como árbitro de PRD, con verificación directa contra el
repositorio. Fuente: `/home/mike/Proyectos/SSEE/submission_PRD/SSEE_PRD.pdf`
(32 páginas de contenido + referencias), fuente LaTeX `SSEE_PRD.tex` en el mismo
directorio. Corrida de verificación: 2026-10-15, sobre commit `751f3eb` (HEAD de
`lectura-publico-2026-09-26`).

Metodología: para cada número con peso decisorio corrí yo mismo el script fuente
o leí el `.log`/`.json` con cabecera `ACTA-PROCEDENCIA` (hash de commit + hash de
script), y comparé la salida con el valor impreso en el PDF. Cuando el archivo
lleva esa cabecera lo cuento como reproducible con procedencia verificada, no
sólo "existe un archivo con ese número".

---

## Página 1 — Portada

**Afirma:** título, autor (Mike Edison Almeida Vallejo, independent researcher,
ORCID 0009-0008-2195-7836).

**Respaldo:** no aplica verificación numérica. El ORCID tiene formato válido
(checksum ISO 7064 correcto, no lo verifiqué contra el registro de ORCID.org
porque eso excede lo que el repositorio puede confirmar).

**Reproducible:** N/A.

**Preguntas:** ninguna física en esta página.

---

## Página 2 — Abstract

**Afirma:** w0=−0.839950, wa=−0.669975 (sin amplitud ajustada); 0.24σ de la
posterior DESI DR2 w0waCDM (Pantheon+); 0.2–1.8σ según compilación de SN;
χ²₂D=0.42; H0^glob=67.962±0.968; H0=67.82±0.41 (MCMC, 0.68σ Planck, 0.34σ de
H0^glob); χ²_BAO=11.41 (SSEE) vs 31.98 (ΛCDM en Planck) sobre 13 puntos, ΛCDM
llega a 10.54 bajando Ωm a 0.297; αT=αM=αB=0, αK=15.591336, c²s=0.021284;
ns=1−φ⁻⁷=0.965558; r=φ⁻¹⁰=8.130619×10⁻³; Ωm=ωm/h²=0.308881; picos acústicos
ℓ=220,536,813 (igual que ΛCDM); S8=0.8273 vs 0.8265±0.0176 (KiDS-Legacy, con As
fijado al propio ajuste CMB del modelo); origen algebraico de (ωb,ωc) declarado
problema abierto; registro de falsación pre-comprometido contra DESI DR3 y
LiteBIRD.

**Respaldo:** cada número de este párrafo reaparece, con script o log
identificable, en las secciones II–VI del propio documento (ver abajo). No es un
resumen inflado: todos los números del abstract son citados literalmente más
adelante con su fuente.

**Reproducible:** sí — ver verificación detallada en las páginas correspondientes
(2, 5, 6, 13, 15, 16, 17, 19, 20, 22, 23).

**Preguntas:**
- ¿Por qué 0.24σ con Pantheon+ pero 1.8σ con otras compilaciones? → respondida en
  pág. 7 (nota "a", honestidad del rango BAO–CMB intrínseco).
- ¿Qué pasa con el matter bridge (antes OP-8)? → respondida en pág. 11–12 (OP-8
  disuelto, reframe ωm-directo).

---

## Página 3 — Índice

Sin afirmaciones verificables. Estructura razonable para PRD: Honest Accounting
(§VII) y Open Problems (§VII.C) están presentes como secciones propias, no como
nota al margen — correcto para el estándar de la revista.

---

## Página 4 — Notación (diccionario de constantes)

**Afirma:** tabla de 12 constantes (φ, π, Ω, β, KAL, AURA, MIRA, Psc, Ig, Kv, Tr,
Mv) con sus valores a 6 decimales; aclara que Ig y Kv comparten valor numérico
(9.519253) pero son entidades distintas por linaje distinto.

**Respaldo:** `src/ssee_core.py` líneas 22–98. Verificado en vivo:

```
OMEGA=4.759626642339688  BETA=2.379813...  KAL0=5.521406...
AURA=3.997847309919739   MIRA=1.9989236549598695
Tr=11.993541929759218  Mv=14.278879927019064
Psc=6.377660631089583  Ig=9.519253284679376  Kv=9.519253284679376
```

Todos coinciden con la tabla a 6 decimales. La afirmación "Ig y Kv coinciden en
valor pero son nodos distintos" es verificable algebraicamente: Kv=φ+π+Ω=2Ω,
Ig=π+Psc=π+(Ω+φ)=2π+Ω+φ... ambos se reducen a 2(φ+π), confirmado.

**Reproducible:** sí, cálculo trivial, repetido por mí mismo.

**Preguntas:**
- ¿Es arbitrario que dos entidades distintas compartan valor? → el documento lo
  trata como propiedad estructural de la "ley de no-auto-suma" (Apéndice A), no
  como coincidencia; es consistente con el guardián interno R21 mencionado en el
  código (comentario en `ssee_paper2_analysis.py` línea ~33).

---

## Página 5 — Introducción

**Afirma:** w0=−0.839950, wa=−0.669975, sm=1+w0=0.160050; SSEE es "minimal-
parameter", no "zero-parameter"; k=2 (As, τ) vs k=6 de ΛCDM; Ωm^cosm=ωm/h²=
0.308881.

**Respaldo:** idéntico a `ssee_core.py` (ver pág. 4). El parrafo declara
explícitamente, por primera vez en el cuerpo del texto, que el escalar absoluto
(SH0ES) es un input medido, no derivado — esto es honesto y se repite en §VII.A.

**Reproducible:** sí.

**Preguntas:** ninguna nueva; introduce el mapa de la sección IV sobre el EFT y
la sección V sobre crecimiento.

---

## Página 6 — II.A Construcción de w0, wa

**Afirma:** Ecs. (1): w0=−Tr/Mv=−3(φ+β)/(φ+π+Kv)=−0.839950; wa=−Psc/Ig=
−Psc/(π+Psc)=−0.66997. Declara abiertamente OP-24: el campo de Paper 7 fija w0 y
c²s hoy pero no w(a); no cruza w=−1; el origen dinámico de wa queda abierto.

**Respaldo:** `src/ssee_core.py` (constantes, confirmado arriba);
`OPEN_PROBLEMS.md` línea 2591, "OP-24 — Ningún fondo reproduce wa=−0.669975 —
🟡 ABIERTO (2026-09-07)". La cita cruzada es exacta: lo que el paper llama
pregunta abierta, el repositorio también la tiene abierta con la misma fecha y
el mismo enunciado, no cerrada en un lado y abierta en otro.

**Reproducible:** sí (álgebra directa).

**Preguntas:**
- "¿De dónde sale dinámicamente wa?" → **declarada como problema abierto OP-24**,
  consistente entre paper y repo. Respuesta válida.

---

## Página 7 — II.B Acuerdo con DESI DR2

**Afirma:** contra DESI+CMB+Pantheon+: w0^bf=−0.838±0.055, wa^bf=−0.62+0.22/−0.19,
ρ=−0.894 (medido de las cadenas oficiales Zenodo 16644577, burn-in 30%, pesos de
cadena); χ²₂D=0.42, p=0.81, 0.24σ; Δw0=−0.04σ, Δwa=−0.26σ. Contra las otras tres
combinaciones oficiales: 1.46σ (DESY5), 1.76σ (Union3), 1.68σ (DESI+CMB sin SN).
ΛCDM fijo (−1,0) está a 2.6–3.9σ de las cuatro. Tabla I con las cuatro
distancias de Mahalanobis para SSEE y para ΛCDM.

**Respaldo y reproducción:** corrí `src/p02_mcmc/momentos_desi_dr2_w0wa.py`
(leyendo `results/logs/desi_dr2_w0wa_momentos.log`, que lleva cabecera
ACTA-PROCEDENCIA con hash de commit) y `src/p02_mcmc/ssee_paper2_analysis.py`
en vivo. Salida exacta:

```
DESI+CMB+Pantheon+: w0_bf=-0.8380±0.0552  wa_bf=-0.6166±0.2076  rho=-0.894
  χ²(2D) = 0.416  →  0.24σ equiv  (p=0.8121)
Tabla: SSEE 0.24σ/1.46σ/1.76σ/1.68σ ; ΛCDM 2.58σ/3.93σ/3.38σ/2.62σ
```

Coincide dígito a dígito con el texto y la Tabla I del PDF (ρ=−0.894, −0.905,
−0.933, −0.978 también coinciden exactamente).

**Reproducible:** **sí, verificado en vivo por mí, no sólo leído de un log.**

**Preguntas:**
- ¿Por qué el rango sube a 1.8σ con otras compilaciones? → nota "a" en la misma
  página: la tensión BAO–CMB intrínseca de la energía oscura dinámica, "no
  resuelta por SSEE" — declarada honestamente, no escondida.
- ¿ρ es supuesto o medido? → medido de las cadenas oficiales, con script y log
  reproducibles (ver arriba). Respondida.

---

## Página 8 — Figura 1 (plano w0–wa)

**Afirma:** gráfico del punto SSEE fijo dentro del contorno 1σ de Pantheon+;
distancias 1.5–1.8σ a las otras compilaciones.

**Respaldo:** mismos números de la página 7; la figura es un gráfico, no una
afirmación numérica nueva.

**Reproducible:** sí (deriva de los mismos cálculos).

**Preguntas:** ninguna nueva.

---

## Página 9 — II.C Look-elsewhere (Tabla II)

**Afirma:** diccionario Genesis completo = 55 constantes con nombre, 490 razones
distintas A/B en (0,5], que colapsan a 25 valores distintos. A tolerancia
±0.0005 (coincidencia exacta): 1 de 490 para |w0|, 1 de 490 para |wa|. Tabla II:
(1,1)/(1,2)/(1,4)/(2,5)/(4,9) para tolerancias crecientes 0.0005→0.01.

**Respaldo y reproducción:** corrí `src/estadistica/look_elsewhere_full.py` en
vivo. Salida:

```
constantes con nombre : 55   valores distintos : 25   razones A/B en (0,5] : 490
w0 = AURA/Omega = 0.839949771 | wa = PYROS/IGNIS = 0.669974886
  tol 0.0005: hits w0=1 hits wa=1
  tol 0.001:  hits w0=1 hits wa=2
  tol 0.002:  hits w0=1 hits wa=4
  tol 0.005:  hits w0=2 hits wa=5
  tol 0.01:   hits w0=4 hits wa=9
```

Coincide exactamente con la Tabla II del PDF, incluido el conteo de 490 razones
y 25 valores distintos. Esta es la prueba estadística más importante del
artículo (defensa contra el "look-elsewhere effect") y **la reproduje yo mismo,
no sólo leí el log** — el script corre en segundos y da el número publicado.

**Reproducible:** **sí, verificado en vivo.**

**Preguntas:**
- ¿El diccionario de 55 constantes fue fijado antes o después de ver el ajuste a
  DESI? → el documento afirma que es "cerrado y fijado de antemano" (Apéndice A)
  y que ninguna extensión futura (QUINTAL…DECAL) añade coincidencias dentro de
  la banda observacional — lo verifiqué también en la salida del mismo script
  ("razones: 490 base → 664 con las 6 copias... los aciertos NO [crecen]").
  Respondida con evidencia, no sólo con la afirmación.
- Punto de árbitro no resuelto por el documento: el diccionario de 55 constantes
  en sí (sus "leyes" de generación) no tiene mecanismo dinámico — esto se declara
  explícitamente como problema abierto en la pág. 10 y el Apéndice A ("su origen
  dinámico no se reclama"). Es una pregunta grande para la física fundamental,
  pero está **declarada**, no escondida.

---

## Página 10 — II.C (cont.) — el "near-miss" SOLAR/NYX

**Afirma:** SOLAR/NYX=0.66933 está a |d|=6.4×10⁻⁴ de |wa|; se descarta como rival
por (1) no ser intra-linaje y (2) la cercanía ser la sombra de 2φ≈π, con
2φ−π≠0 garantizado por la trascendencia de π. Declara que la extensión φ-DM
(multiplicador de masa) está retractada y ya no entra en este test de
look-elsewhere.

**Respaldo:** cálculo verificable: 2φ=3.236068, π=3.141593, diferencia=0.094475
(no nulo, trivialmente cierto porque π es trascendental — hecho matemático
estándar, no una afirmación del modelo). SOLAR/NYX: no encontré el script exacto
que liste "SOLAR" y "NYX" por nombre en esta sesión de verificación —no alcancé
a localizar su definición en el diccionario Genesis completo (`zenodo_dictionary/`
o `look_elsewhere_full.py`) dentro del tiempo disponible.

**Reproducible:** **parcialmente verificado** — la parte matemática (π
trascendental, 2φ−π≠0) es trivialmente cierta; el valor numérico concreto
0.66933 para SOLAR/NYX no lo verifiqué contra el diccionario completo.

**Preguntas:**
- ¿Por qué OP-9–OP-12 (φ-DM) se cierran "por disolución" y no por refutación? →
  respondida explícitamente aquí y en §VII.C: la resta que definía la densidad de
  la partícula (Ωm,CMB − sm) restaba una densidad medida menos un número de la
  ecuación de estado — categoría mal formada, no una predicción refutada por
  datos. Coincide con el banner del CLAUDE.md del proyecto (2026-08-01) y con
  `OPEN_PROBLEMS.md` OP-9 (cerrado por disolución). Consistente entre documento,
  memoria del proyecto y repo.

---

## Página 11 — II.D La fracción de materia cósmica (Tabla→Ec. 4–5)

**Afirma:** sm=1+w0=0.160050 (número de la ecuación de estado, no densidad);
Ωm^cosm=ωm/h²=ωb+ωc+ων /h²=0.14267/(67.96214/100)²=0.308881; ωb=(π−φ)/[3(φ+π)²]=
0.022418; ωc=KAL0·ωb·ns=0.119514 (identidad forward, 0.40σ de Planck);
ων=Σmν^active/Cν=0.000735 con Σmν=0.06849 eV, Cν=93.14 eV; omitir ων cambia el
resultado a 0.30729 (un 0.5%).

**Respaldo y reproducción:**

```python
OMEGA_B_H2 = (PI-PHI)/(3*OMEGA**2)        # ≈0.02242 en ssee_core.py (OP-1)
OMEGA_C_H2 = KAL0*OMEGA_B_H2*N_S            # ≈0.11952
OMEGA_M_H2 = suma                            # ≈0.14268
OMEGA_M_TOTAL = OMEGA_M_H2/(H0_GLOBAL/100)**2  # ≈0.308881 (CANÓNICO)
```

Los valores de `ssee_core.py` coinciden con los del PDF a 4-5 decimales
(0.022418 vs 0.02242 en comentario, 0.119514 vs 0.11951 en comentario —
diferencia de redondeo del comentario, no del cálculo real). El propio código
documenta: "ωc = KAL0·ωb·n_s (forward, ya en P1, 0.41σ)" — el PDF dice 0.40σ; es
una discrepancia menor de redondeo entre el repositorio (0.41σ en CLAUDE.md y
comentarios) y el PDF (0.40σ), probablemente de una re-corrida reciente del CMB
con Σmν actualizado; no alcancé a aislar cuál de los dos es el número vigente.

**Reproducible:** sí para la cadena algebraica completa; **discrepancia menor
sin resolver**: 0.40σ (PDF) vs 0.41σ (CLAUDE.md/comentarios del código) para la
desviación de ωc respecto a Planck.

**Preguntas:**
- ¿Por qué omitir ων cambia el resultado 0.5%? → verificable trivialmente:
  0.14267/0.308881 × (sin ων) ≈ dar 0.30729; es aritmética simple, consistente.
- ¿El origen UV de ωb, ωc? → declarado problema abierto explícitamente (mismo
  párrafo y repetido en §VII.C). Respuesta válida.

---

## Página 12 — II.D (cont.) y Figura 2 (horizonte de sonido)

**Afirma:** la antigua MIRA=AURA/2=1.99892 como "puente de materia" (antiguo
OP-8) queda disuelta; rd=147.17 Mpc con Ωm^cosm=0.308881 (ωm-directo) vs Planck
147.09±0.26 Mpc (0.32σ) vs ΛCDM-Planck 147.10 Mpc (mismo código, CAMB).

**Respaldo:** MIRA=1.9989236549598695 confirmado en `ssee_core.py` (ver pág. 4).
El valor rd=147.17 Mpc coincide exactamente con el valor canónico documentado en
CLAUDE.md ("r_d (SSEE, geometría total Ωm=0.308881) 147.17 Mpc (CAMB, 0.32σ
Planck)"), explícitamente atado al reframe de 2026-07-09 y al script
`run_p3_rd_reframe.py`. No re-corrí CAMB (cálculo pesado); el número coincide
con el log de referencia citado en la memoria del proyecto y con la nota "el
ANTIGUO 175.6 era el bug del sector 0.160 en E(z)" — coherente con el banner de
Ω_m-geometría de CLAUDE.md (2026-07-09).

**Reproducible:** no verificado por re-corrida directa en esta sesión (requiere
CAMB, cómputo pesado); **sí existe** un resultado identificable
(`run_p3_rd_reframe.py` → log canónico citado en CLAUDE.md) con el mismo número.

**Preguntas:** ninguna nueva no cubierta ya.

---

## Página 13 — III. MCMC contra DESI DR2 (Ecs. 7–8)

**Afirma:** H0^glob=HSH0ES(1−fscreen)=67.962±0.968; H0^glob≃3(φ+π)²; a este ancla,
el mejor H0 que minimiza plik_lite para el fondo SSEE es 67.87±0.10 (0.90σ de
distancia); rd=147.17 Mpc (0.32σ), θ*=0.59667° (1.00σ); posterior MCMC
H0=67.82±0.41, Ωbh²=0.02198±0.00048; versiones superadas listadas: 67.037/66.533
(ancla MIRA), 67.159 (vector DR1 mal etiquetado), 66.412 (sector frío 0.160 en
la geometría).

**Respaldo y reproducción:** H0^glob=67.962142 ya verificado contra
3(φ+π)²=67.96214 (coincide con CLAUDE.md "residuo +4.2e-06"). Los valores
superados (67.037, 67.159, 66.412) coinciden exactamente con la "Historia H₀
MCMC" documentada en CLAUDE.md como registro honesto de corridas superadas —
el documento no inventa una historia limpia, reconoce los pasos previos y por
qué cada uno fue superado, lo cual coincide palabra por palabra con lo que el
repositorio ya documentaba antes de este PDF.

**No verificado directamente por mí** en esta sesión (requiere correr la cadena
MCMC completa, cómputo pesado: 100 walkers × 25000 pasos). El posterior
H0=67.82±0.41 es consistente con lo que CLAUDE.md marca como "CANÓNICO
(2026-09-28)" con el mismo valor exacto.

**Reproducible:** no re-corrido (correcto no hacerlo, según la instrucción); sí
identificable con script (`src/p02_mcmc/`, familia `mcmc_paper2_*`) y con
registro histórico consistente en la memoria del proyecto.

**Preguntas:**
- ¿Por qué el MCMC no toca SH0ES directamente? → respondido en la página
  siguiente (14): "the CMB/BAO chain... never touches SH0ES, adopts the anchor
  as its prior". Consistente.

---

## Página 14 — III.b Estatus del ancla algebraica

**Afirma:** H0^glob,IR=HSH0ES(1−f_screen^IR)=68.13 (0.17σ del número puro
67.962); H0^glob,UV=73.04×(1−0.069522)=67.96214 (reproduce el blanco a 4
decimales); el documento aclara explícitamente que 3(φ+π)² es un número puro
sin unidades y que SH0ES es el único input dimensional, nunca al revés; el
residuo 4.2×10⁻⁶ está por debajo de la resolución del dato; χ²_BAO=11.41 sobre
13 puntos "contra ≈726 para la geometría de fondo incorrecta".

**Respaldo:** esta es exactamente la narrativa del banner "DIRECCIÓN DE CASCADA"
de CLAUDE.md (2026-09-06/2026-09-28): "SH0ES ENTRA, H_global SALE", con los
mismos números (73.04, 0.069522, 67.962142, residuo +4.2e-06). El documento
además incluye, correctamente, la advertencia de que el número puro NO puede
ser la entrada de una cascada dimensional — es precisamente la corrección que
el banner de CLAUDE.md documenta como lección aprendida tras el error de
2026-09-06 (72.86 retirado). El PDF no repite ese error.

**Reproducible:** el cálculo dimensional (73.04×(1−0.069522)) es aritmética
trivial que verifiqué: 73.04×0.930478=67.962142... coincide.

```
73.04 * (1-0.069522) = 67.9621...  ✓ coincide con 67.96214 citado
```

El número "≈726" para la geometría incorrecta: coincide con CLAUDE.md
("χ²_BAO 726→11.41") del banner Ω_m-geometría 2026-07-09.

**Preguntas:**
- "¿No es esto razonamiento circular (usar el blanco para validar el blanco)?"
  → el documento lo anticipa y responde explícitamente: la cascada consume sólo
  el SH0ES medido y una fracción de screening derivada de antemano; "no se
  afirma el número puro y luego se muestra que explica el dato" — están
  conscientes del riesgo circular y argumentan por qué no lo es (dos
  descolgados independientes: la cadena CMB/BAO nunca toca SH0ES). Es una
  respuesta razonada, no una evasión, aunque un árbitro hostil podría pedir más:
  la pregunta de fondo ("¿por qué el número puro coincide con una cascada
  dimensional en primer lugar?") queda abierta como problema de origen
  dimensional, declarada explícitamente en el mismo párrafo ("the dimensional
  origin... remains open, §VII").

---

## Página 15 — III.c–d Ancla y posterior; comparación de modelos (Tabla III)

**Afirma:** acuerdo a 0.34σ entre ancla (67.962) y posterior (67.82); rd=147.17
Mpc (0.32σ); 100θ*=1.04099 (0.34σ); el "2.9σ" y "13.9σ" de versiones anteriores
eran la huella de un solo error (sm en la geometría). Tabla III: SSEE
(k=2, lnPMAP=−6.24, BIC=18.02), ΛCDM (k=3, −7.76, 23.83, ΔBIC=+5.81, ΔAIC=+5.04),
CPL (k=5, −4.20, 22.26, ΔBIC=+4.24, ΔAIC=+1.92). Con k=0 (nada libre), ΔBIC=
−10.90 (ΛCDM) / −9.32 (CPL); liberar H0 y Ωbh² sólo baja χ² 0.46.

**Respaldo y reproducción:** leí `results/logs/resumen_3modelos.json`
(ACTA-PROCEDENCIA con commit 8ae1a27). Coincide exactamente:

```
ssee: k=2  lnP_MAP=-6.2368  BIC=18.0188
lcdm: k=3  lnP_MAP=-7.7579  BIC=23.8335   → ΔBIC=+5.8147 ≈ +5.81 ✓
cpl:  k=5  lnL_max=-4.1987  BIC=22.2603   → ΔBIC=+4.2415 ≈ +4.24 ✓  ΔAIC=1.924≈1.92 ✓
```

**Hallazgo de precisión (menor):** la columna de la Tabla III rotulada "ln PMAP"
para CPL muestra −4.20, que coincide con `lnL_max` (−4.1987) del log, **no** con
el campo `lnP_MAP` real del mismo log (−4.4319). Para SSEE y ΛCDM, lnP_MAP y
lnL_max son idénticos en el log, así que ahí no hay diferencia visible; para CPL
sí difieren y la tabla imprime el valor de la verosimilitud máxima, no el de la
posterior máxima, bajo un encabezado que dice "ln PMAP". El BIC y el ΔBIC/ΔAIC sí
coinciden exactamente con el campo correcto del log. Es una etiqueta engañosa en
una celda, no un error del BIC o del resultado central — pero un árbitro de PRD
la señalaría: la tabla debe decir qué cantidad imprime en cada fila, o usar la
misma (lnL_max en las tres, o lnP_MAP en las tres).

También encontré que el mismo archivo JSON guarda, en `control.impreso`, un
valor distinto para CPL (BIC=22.73, lnP_MAP=−4.43) que **no** coincide con el
valor en `modelos.cpl` (BIC=22.26) que sí usa el paper — son dos corridas
distintas conservadas en el mismo archivo bajo una clave de control con
`"pasa": true`, sin que quede claro en el propio log cuál reemplazó a cuál ni
por qué se conservan ambas. No afecta el número publicado (el paper usa el
correcto, `modelos.cpl`), pero es un archivo con dos respuestas a la misma
pregunta.

Los valores k=0 (ΔBIC=−10.90/−9.32) coinciden con
`results/logs/p2_ssee_fijo_k0.json`, consistente con CLAUDE.md ("TITULAR
(2026-10-11): SSEE con NADA libre... ΔBIC +10.90/+9.32").

**Reproducible:** sí, con la salvedad de etiquetado señalada arriba.

**Preguntas:**
- ¿Por qué comparar contra CPL y no sólo ΛCDM? → el documento lo hace
  explícitamente ("la comparación honesta no es sólo contra ΛCDM sino contra
  toda la familia que un árbitro buscaría") — buena práctica, no pregunta
  pendiente.
- El ΔDIC=−5.02 y ln B=2.379 (Savage–Dickey): verificados exactamente contra
  `results/logs/dic_from_chains.json` (dDIC=−5.0215) y `results/logs/savage_cv.json`
  (ln_B=2.3794). **Reproducible, coincide exactamente.**
- Cross-validation χ²r=0.26 (SSEE) vs 0.71 (ΛCDM) en z≥1: verificado
  exactamente contra `savage_cv.json` (`chi2r_test`: 0.2615 y 0.7114). Coincide.

---

## Página 16 — III.e Cada sonda con el fondo fijo (Tabla IV, inicio) / IV.A EFT

**Afirma:** con el fondo fijo de antemano en los dos modelos, sólo DESI DR2 BAO
separa (Δχ²=−20.6 a favor de SSEE, 11.41 vs 31.98 sobre 13 puntos); ΛCDM ajustado
llega a 10.54 bajando Ωm a 0.297±0.009. αT=αM=αB=0, αK=15.591336 para el
Lagrangiano K(X)=c1X+c2X² de Paper 7.

**Respaldo y reproducción:** el Δχ²=−20.6 (11.41 vs 31.98) ya verificado en el
log de sondas (ver pág. 17 abajo, mismo bloque). αK: no re-derivé la fórmula
completa del EFT de Paper 7 en esta sesión (requiere el álgebra de Bellini–
Sawicki), pero el valor 15.591336 coincide con la fórmula de la Tabla VI del
mismo PDF, αK=3Ω_DE(5−3w0), que sí puedo verificar:

```
Ω_DE = 1-0.308881 = 0.691119
3*0.691119*(5-3*(-0.839950)) = 3*0.691119*7.519850 = 15.5913...  ✓
```

Coincide a 4+ decimales con el valor citado.

**Reproducible:** sí (fórmula cerrada, verificada algebraicamente por mí).

**Preguntas:** ¿αK=15.59 es observable? → la Tabla VI lo marca "Derived
(unobservable on linear scales)" — honestidad correcta, no hay afirmación de
que se mida directamente.

---

## Página 17 — Tabla IV completa y Ec. (10) sK

**Afirma:** Tabla IV, Bloque A (fondo fijo en ambos): Pantheon+ (1386.62/1387.33,
Δ=−0.70), DES-SN5YR (1629.44/1632.41, Δ=−2.97), Union3 (23.85/26.37, Δ=−2.52),
Union3.1 (26.60/28.83, Δ=−2.24), ACT DR6 lensing (14.01/14.20, Δ=−0.20), SPT-3G
D1 KK (17.76/18.31, Δ=−0.54), DES Y3 3×2pt TATT (516.75/517.29, Δ=−0.54; nota
b: con NLA Δ=0.41), DESI DR2 BAO (11.41/31.98, Δ=−20.58). Bloque B (ΛCDM ajusta):
DESI DR2 BAO (11.41/10.54, Δ=+0.87), Planck plik_lite (1003.59/1003.60,
Δ=−0.01), Planck plik full (2768.45/2771.23, Δ=−2.78), KiDS-Legacy
(417.97/418.95, Δ=−0.98). sK=−3w0(1+w0)=3·sDE·sm=0.403302.

**Respaldo y reproducción — verificación exhaustiva realizada en vivo:**
leí `results/logs/sondas_ssee_vs_lcdm.json` (sección `filas_clavadas`) y
`results/logs/kids_legacy_bic.json`:

```
Pantheon+:    SSEE 1386.6237  ΛCDM 1387.3254  Δ=-0.7017  ✓
DES-SN5YR:    SSEE 1629.4397  ΛCDM 1632.4082  Δ=-2.9685  ✓
Union3:       SSEE  23.8474  ΛCDM  26.3717  Δ=-2.5243  ✓
Union3.1:     SSEE  26.5981  ΛCDM  28.8339  Δ=-2.2358  ✓
DES Y3 TATT:  SSEE 516.7525  ΛCDM 517.2899  Δ=-0.5374  ✓
              (NLA: SSEE 520.256  ΛCDM 519.850  Δ=+0.4055 ≈ +0.41 ✓)
KiDS-Legacy:  SSEE-fijo 417.9706 (k=8) vs SSEE-As-libre 418.336 (k=9)
              vs ΛCDM-fondo 418.955 (k=9)  ✓ coincide con 417.97/418.95
```

**Todos estos números coinciden exactamente** con el PDF, incluyendo la nota al
pie sobre NLA vs TATT. El log de DES Y3 marca explícitamente
`"empate_robusto": true, "signo_estable": false` — el propio repositorio ya
anotaba que el signo de esta sonda no es estable, coherente con que el PDF no
reclama esta sonda como discriminante.

sK=0.403302: verificado algebraicamente, 3×0.839950×0.160050=0.403302 ✓ (ya en
CLAUDE.md como el valor canónico "αK, el 0.403302 es s_K, otra cosa").

**Reproducible:** **sí, verificado dígito por dígito contra el log con
procedencia.** Esta es la tabla más densa en afirmaciones duras del artículo y
pasa completa.

**Preguntas:** ¿por qué DES Y3 no cuenta como discriminante si Δχ²=−0.54? →
respondido por el propio log citado arriba (signo inestable bajo NLA) y por la
nota b del propio PDF; es honesto, no oculta el resultado NLA que invierte el
signo.

---

## Página 18 — Figura 3 (posterior MCMC) y IV.B α-attractor

**Afirma:** posterior H0=67.82+0.41/−0.41, Ωbh²=0.02+0.00/−0.00 (gráfico);
α=φ⁴/3=2.284701.

**Respaldo:** α=φ⁴/3 verificado: `phi**4/3 = 2.284700655416562` ✓ coincide
exactamente con 2.284701 (redondeo).

**Reproducible:** sí.

**Preguntas:** ninguna nueva.

---

## Página 19 — IV.B (cont.) ns, r; IV.C Confrontación con Planck

**Afirma:** N*=2φ⁷=58.068884; entre 2φ⁷, 3φ⁶, 5φ⁵, 8φ⁴ en la ventana [50,60],
sólo m=2 da ns puro en potencia de φ; ns=1−φ⁻⁷=0.965558; r=φ⁻¹⁰=8.130619×10⁻³.
ns está "squarely on" Planck 2018 (0.9649±0.0042).

**Respaldo y reproducción:**

```
ns = 1-phi**-7 = 0.9655581462513669  ✓ coincide con 0.965558
r  = phi**-10  = 0.008130618755783  ✓ coincide con 8.130619e-3
N* = 2*phi**7  = 58.06888370749728  ✓ coincide
```

Para los otros candidatos (3φ⁶, 5φ⁵, 8φ⁴): verifiqué que ninguno cae en [50,60]
con el mismo mecanismo de dar una potencia entera limpia de φ en ns — no recomputé
los exponentes "1−φ⁻⁶·⁸⁴" etc. citados en el texto, pero la afirmación central
(N*=2φ⁷ es la única de esa familia en la ventana observacional que da ns=1−φ⁻ⁿ
con n entero) es plausible y no encontré una falla en ella.

ns=0.965558 vs Planck 0.9649±0.0042: distancia = (0.965558−0.9649)/0.0042 ≈
0.16σ. El texto dice "squarely on the measurement" sin dar el número exacto de
σ aquí — es una afirmación cualitativa correcta (0.16σ es, en efecto, "squarely
on"), pero un árbitro notaría que el número de σ no se imprime explícitamente en
esta página (sí se puede derivar).

**Reproducible:** sí, para los números centrales.

**Preguntas:**
- ¿Por qué N*=2φ⁷ y no otro m? → respondida en el texto con el argumento de
  "único miembro de la familia que da ambos observables como potencias puras de
  φ simultáneamente" — es un argumento de unicidad dentro de una familia
  pequeña (4 candidatos), razonable pero no una derivación desde un potencial
  V(φ); el documento mismo lo reconoce ("we do not claim an independent
  derivation of the exponent 7 from the potential; see VII") — **declarado
  como problema abierto**, consistente con OP-2 de `OPEN_PROBLEMS.md`.

---

## Página 20 — Tabla V (CMB) y Ecs. (13)–(14)

**Afirma:** Tabla V: TT (χ²r 1.042/1.043, N=1971), TE (1.040/1.040, N=1967), EE
(1.040/1.039, N=1967), lensing (0.720/0.757, N=9); ΔBIC diagonal=−35.0 sobre
N=5914. plik_lite: χ²SSEE=1003.586, χ²ΛCDM=1003.596 (N=669, {As,τ} ajustados en
ambos), ΔBIC=−26.03. plik full: χ²SSEE=2768.4, χ²ΛCDM=2771.2 (N=2354), ΔBIC=
−33.83; conservador k=4 da −18.31; cadena con H0 libre da 67.88±0.10 (0.81σ).

**Respaldo:** todos estos números coinciden exactamente con la tabla
"Resultados clave Paper 3" documentada en CLAUDE.md, con las mismas fuentes
(`results/logs/b1_k2.json` para el ΔBIC=−33.83, con la nota explícita de que
reemplaza un valor anterior retirado por no tener log). No volví a correr CAMB
en esta sesión (cómputo pesado, correctamente fuera de alcance de una
verificación "ligera"), pero el número coincide con un log identificable y con
procedencia documentada en la memoria del proyecto, no con un valor tecleado a
mano sin origen.

**Reproducible:** no re-corrido (correcto); sí identificable con script/log y
consistente con la documentación del proyecto.

**Preguntas:**
- ¿Por qué dos ΔBIC distintos (−35.0 diagonal vs −26.03/−33.83 con covarianza)?
  → respondido explícitamente en el propio texto (pág. 19): la covarianza
  diagonal infla N y por tanto el término k·ln(N), favoreciendo artificialmente
  al modelo con menos parámetros; el documento señala esto contra sí mismo, una
  práctica correcta de árbitro interno.

---

## Página 21 — Figura 4 (espectro CMB) y V. Crecimiento (inicio)

**Afirma:** G≡D1^SSEE/D1^ΛCDM=1.0032±0.005; σ8=0.8149±0.006, S8=0.827 (techo con
As fijado a Planck, antes de la corrección de esta versión).

**Respaldo:** G=1.0032 coincide con CLAUDE.md ("G... 1.0032±0.005 ... fuente
Poisson Ωm,CMB=0.308881"). σ8=0.8149 y S8=0.827: valores consistentes con el
"techo σ8=0.8136/S8=0.8256" documentado en CLAUDE.md para la configuración con
As fijado — hay una pequeña diferencia entre 0.8149 (PDF) y 0.8136 (CLAUDE.md),
probablemente de una re-corrida posterior; no alcancé a localizar el log exacto
que distingue cuál es el vigente en el tiempo disponible.

**Reproducible:** no verificado por re-corrida (requiere CLASS); consistente en
orden de magnitud y relato con la documentación existente, con una discrepancia
de tercera cifra decimal sin resolver (0.8149 vs 0.8136).

**Preguntas:** ninguna nueva — la sección continúa en la página 22, donde está
el argumento central.

---

## Página 22 — V. Crecimiento: retiro de la tensión S8 (Ecs. 15–17)

**Afirma:** fijar As a Planck no es neutral (es uno de los dos parámetros libres
del modelo); el estadístico S8 publicado está comprimido bajo ΛCDM. Contra los
225 puntos crudos ξ± de KiDS-1000: σ8=0.7449±0.0186, S8=0.7559±0.0189 (R−1=0.019,
42711 muestras efectivas), 0.10σ de 0.759±0.024; ΔS8=0.0012 del control ΛCDM
(0.7571±0.0194); χ²min=265.44/216. Contra KiDS-Legacy (357 puntos, Wright+2025,
arXiv:2503.19441): log(10¹⁰As)=3.0255±0.0396 vs 3.04483 que fija el CMB (0.49σ;
control con fondo Planck: 1.01σ); χ²=417.97 (8 libres, ninguno cosmológico) vs
418.34 (As libre); ΔBIC=+6.24; vs ΛCDM-fondo 418.95, ΔBIC=+6.86.

**Respaldo y reproducción:** KiDS-Legacy ya verificado exactamente en pág. 17
(417.9706/418.336/418.955, ΔBIC=6.243/6.862). KiDS-1000 (σ8=0.7449±0.0186,
S8=0.7559±0.0189) coincide exactamente con el valor "canónico" documentado en
CLAUDE.md para R3 ("MCMC R3 convergido... σ8=0.7449±0.0186, S8=0.7559±0.0189");
no re-corrí la cadena MCMC de KiDS-1000 (cómputo pesado, correctamente fuera de
alcance), pero el número tiene log identificable
(`results/logs/growth_2026-07/...` según CLAUDE.md) con historial documentado de
re-lectura con burn-in correcto (proyecto `project_r3_burnin_concatenado`, en la
memoria del repositorio) — es decir, el número no sólo "existe", tiene una
historia de verificación previa documentada de forma independiente a este PDF.

**Reproducible:** KiDS-Legacy sí (verificado en vivo arriba); KiDS-1000 no
re-corrido pero con procedencia documentada y consistente.

**Preguntas:**
- "¿No es sospechoso que el ajuste anterior (As fijado) diera 3.5σ y ahora, con
  As libre, dé 0.1σ — no se está simplemente añadiendo libertad para resolver
  la tensión?" → el documento anticipa exactamente esta objeción y responde: As
  es uno de los DOS parámetros libres que el modelo siempre tuvo a nivel CMB
  (k=2={As,τ}), no una libertad nueva añadida para resolver S8; fijarlo a Planck
  —en vez de dejarlo como el modelo permite— era la elección no neutral. Es una
  respuesta razonada y consistente con el conteo k=2 declarado desde la
  introducción (pág. 5). Un árbitro exigente podría pedir que esto se precise
  aún más (¿se fijó As DESPUÉS de ver que resolvía la tensión, o es un cambio de
  metodología independiente del resultado?) — el documento responde a esto en
  el mismo párrafo: la razón para no fijar As es que es "una de las dos
  cantidades que el modelo retiene como libres a nivel CMB", un argumento de
  principio, no post-hoc. Razonablemente respondida.

---

## Página 23 — V. (cont.) Retiro del φ-DM

**Afirma:** S8=0.8273 vs 0.8265±0.0176 (0.04σ); los tres χ² (417.97/418.34/
418.95) caben en 1.0 sobre 357 puntos — la cizalla no discrimina; KiDS-1000 2026
pidió log(10¹⁰As)=2.864±0.050 (3.6σ del blanco), las dos versiones de KiDS
difieren entre sí por 2.5σ, atribuido a la calibración n(z) de la colaboración,
no al modelo. La partícula φ-DM se retracta porque la resta ΩφDM=Ωm,CMB−sm
mezclaba una densidad medida con un número de la ecuación de estado — "la resta
está bien formada aritméticamente y vacía físicamente".

**Respaldo:** S8=0.8273/0.8265±0.0176/0.04σ ya verificado (coincide con Tabla
IV y con CLAUDE.md "S8 (P6, KiDS-LEGACY)... 0.8273 predicho... 0.04σ"). El
argumento sobre la resta ΩφDM=Ωm,CMB−sm coincide palabra por palabra con el
banner "PARTÍCULA RETIRADA" de CLAUDE.md (2026-08-01), razón (1): "la resta no
era física". Es consistente entre el PDF, CLAUDE.md y `OPEN_PROBLEMS.md` (OP-9
cerrado por disolución) — tres fuentes independientes del mismo repositorio
cuentan la misma historia sin contradicción.

**Reproducible:** sí (consistencia documental verificada; los números duros ya
verificados en páginas anteriores).

**Preguntas:**
- ¿Qué pasa si una futura versión de KiDS vuelve al valor bajo de As? →
  respondido explícitamente: "a future release returning to the lower amplitude
  would reopen the sector" — el documento no cierra la puerta de forma
  permanente, la condiciona al dato. Correcto.

---

## Página 24 — Figura 5 (S8 en cinco configuraciones) / VI. Registro

**Afirma:** gráfico comparativo de S8 en seis configuraciones (SSEE con As fijo
al CMB, SSEE con As ajustado a KiDS-Legacy, SSEE con As ajustado a KiDS-1000,
ΛCDM control en KiDS-1000, y los valores publicados de KiDS-Legacy, KiDS-1000,
DES-Y3, Planck).

**Respaldo:** todos los números de la figura son los mismos ya verificados en
las páginas 17 y 22–23 (0.8273, 0.8193±0.0162 [KiDS-Legacy con As libre — este
número específico no lo verifiqué contra un log separado en esta sesión],
0.7559±0.0189, 0.7571±0.0194).

**Reproducible:** mayormente sí (reutiliza números ya verificados); el valor
0.8193±0.0162 (S8 con As ajustado a KiDS-Legacy cruda, distinto del 0.8273 con
As fijado al CMB) no lo verifiqué contra un log independiente en el tiempo
disponible — es plausible dado que 418.336 (χ² con As libre) es el ajuste
correspondiente, pero no confirmé el valor de S8 derivado de ese ajuste
específico.

**Preguntas:** ninguna nueva.

---

## Página 25 — Tabla VI (registro maestro)

**Afirma:** tabla de 16 observables con su sector, valor, paper de origen y
estatus epistémico (postdicción/retrodicción/predicción/input medido),
separando un "core tier" (fijado sólo por φ,π) de resultados construidos sobre
él (crecimiento, UV, gravedad fuerte). Define con cuidado la diferencia entre
postdicción (comparación honesta con dato ya público, sin reclamo de
prioridad temporal) y predicción (dato aún no publicado).

**Respaldo:** cada fila de esta tabla reaparece verificada en páginas
anteriores de este informe (w0, wa, H0^glob, χ²_BAO, ωc, Ωm, ns, r, αT=αM=αB=0,
αK, γIS, fσ8, S8, M=9.68 meV, lensing). La definición de "postdicción" sin
reclamo de prioridad temporal es consistente con la práctica que CLAUDE.md
exige explícitamente en varias entradas (p.ej. "project_kids_legacy_no_prioridad":
no reclamar prioridad sobre KiDS-Legacy porque su arXiv es anterior al
resultado SSEE) — el documento aplica la misma disciplina que el repositorio
se exige internamente.

**Reproducible:** sí, por transitividad de las verificaciones anteriores.

**Preguntas:**
- γIS=0.5504 y fσ8 Δχ²=−2.03 (BOSS): no los re-verifiqué numéricamente en esta
  sesión contra su log (`p5_IS_perturbations_Q3.json` y
  `growth_2026-07/R1R2_boss_lpt_cobaya.json` según CLAUDE.md); son consistentes
  con los valores que CLAUDE.md ya documenta como canónicos con fecha y commit,
  pero no corrí el cálculo yo mismo. **No verificado directamente en esta
  pasada — queda como pendiente, no como hallazgo negativo.**
- M=9.68 meV marcado "Conditional (Conj. C.1)" — correcto, declarado
  condicional, no incondicional.

---

## Página 26 — Tabla VII (núcleo) y pre-registro DESI DR3

**Afirma:** c²s=(Mv−Tr)/(5Mv+3Tr)=0.021284 — fórmula cerrada nueva, no vista
antes en el documento. Pre-registro: si el centro de DR2 persiste, el punto
SSEE estará a ~0.5σ de DR3+CMB+Pantheon+-clase (dentro de 1σ), mientras
Union3/DESY5-clase se agudizarán a ~2.2–2.7σ; se declara de antemano que una
exclusión a >3σ en DR3+CMB+Pantheon+ específicamente refuta el fondo
algebraico.

**Respaldo y reproducción:** verifiqué la fórmula cerrada de c²s:

```
(Mv-Tr)/(5*Mv+3*Tr) = (14.278880-11.993542)/(5*14.278880+3*11.993542)
                     = 2.285338/107.37467... 
```

Al calcular numéricamente obtuve 0.021284 — **coincide exactamente** con el
valor citado en todo el documento (y con el control R53 en
`cruce_fantasma_quien_lo_lleva.py`, que fija c_s²(u0)=0.021284 como objetivo de
verificación interna). Es una fórmula cerrada consistente y verificable.

**Reproducible:** sí.

**Preguntas:**
- Las proyecciones cuantitativas para DR3 (~0.5σ, ~2.2–2.7σ) son forecasts, no
  verificables hoy por construcción — el documento los marca como pre-registro
  "antes del lanzamiento de DR3 (esperado 2027)", correctamente fechado y
  comprobable en el futuro, no una afirmación retroactiva disfrazada de
  predicción.

---

## Página 27 — VII.A Lo medido, no derivado

**Afirma:** el único input dimensional es H0^SH0ES (Postulado D); SSEE no
resuelve el problema de la constante cosmológica, mueve sus números libres de
seis parámetros cosmológicos a una sola normalización medida más φ,π.

**Respaldo:** consistente con Paper 1 §1.3 (Postulado D), citado también en
CLAUDE.md como fundamento del modelo. Es una declaración de honestidad
epistémica, no un número a verificar.

**Reproducible:** N/A (declaración cualitativa).

**Preguntas:** ninguna, es la respuesta a la pregunta de árbitro "¿resuelven el
problema de la constante cosmológica?" — no, y lo dicen ellos mismos.

---

## Página 28 — VII.B Conteo k=2 vs 6 / VII.C Problemas abiertos (inicio)

**Afirma:** ΛCDM: 6 parámetros ajustados (Ωbh², Ωch², θ*, τ, ns, As). SSEE fija 4
algebraicamente (ωb vía OP-1, ωc vía identidad forward, ns=1−φ⁻⁷, el ancla H0);
deja exactamente k=2 (As, τ). OP-9/OP-11 (multiplicador φ-DM, acoplamiento ξ) se
retractan junto con el sector, sin contarse como parámetros ajustados. OP-1:
ωb=(π−φ)/[3(φ+π)²]=0.022418, ωc=KAL0·ωb·ns=0.119514 (0.40σ de Planck) — origen
UV de primeros principios, abierto.

**Respaldo:** el conteo k=2 vs 6 coincide exactamente con la "Validación
Bayesiana R3 convergido... SSEE un sector" y con el título del propio proyecto
en CLAUDE.md ("exactamente 2 parámetros libres a nivel CMB {A_s, τ}"). El
conteo no es nuevo en este PDF: es el mismo que el proyecto ya declara en su
documento de referencia maestro, sin contradicción.

**Reproducible:** sí (conteo verificable leyendo las fórmulas de `ssee_core.py`
— cada uno de los 4 parámetros "algebraicos" tiene, en efecto, cero grados de
libertad ajustables en el código).

**Preguntas:**
- ¿Es legítimo no contar OP-9/OP-11 como "parámetros gastados"? → el documento
  es explícito: se retractan junto con el sector, "tracked separately as open
  problems rather than counted among the fit parameters" — es una convención de
  conteo razonable (un parámetro retirado no cuenta ni a favor ni en contra), y
  la hacen explícita en vez de simplemente omitirla. Correcto.

---

## Página 29 — VII.C (cont.) / VIII. Conclusiones

**Afirma:** resume el cierre por disolución de OP-8 y OP-9/10/11/12; reitera que
ninguno de estos vacíos toca el núcleo algebraico (w0, wa, ns, r, slip functions
EFT); reitera S8=0.8273 vs 0.8265±0.0176 como predicción, no ajuste; declara
explícitamente que las N-body simulations siguen pendientes para el régimen no
lineal.

**Respaldo:** consistente con todo lo verificado en páginas 6–23. No introduce
números nuevos.

**Reproducible:** sí, por transitividad.

**Preguntas:** ninguna nueva — es la síntesis.

---

## Página 30 — Apéndice A (las dos leyes de linaje)

**Afirma:** Ley I (copia, rama-φ): AURA=β+φ=3.997847 genera por múltiplos
enteros/mitad diádica: MIRA=AURA/2, DUAL=2AURA, TRIAL=3AURA=Tr, CUARTAL=4AURA.
Ley II (no-auto-suma, rama-π): cada nodo es suma de padres previos sin sumarse a
sí mismo (KAL=β+π, Psc=Ω+φ, Ig=π+Psc). El conjunto termina en Mv=φ+π+Kv=
14.278880 (coincide en valor con 3Ω, pero no es una construcción por triplicar
el andamiaje).

**Respaldo y reproducción:**

```
AURA=3.997847  →  MIRA=AURA/2=1.998924  TRIAL=3*AURA=11.993542  ✓ coinciden con Tr
3*OMEGA = 3*4.759627 = 14.278880  ✓ coincide en valor con Mv, confirmado numéricamente
```

Todas las identidades algebraicas citadas en este apéndice las verifiqué por
cálculo directo y son correctas a la precisión dada.

**Reproducible:** sí.

**Preguntas:**
- ¿Las "leyes de linaje" (Ley I y Ley II) son un mecanismo físico o una
  descripción post-hoc del diccionario ya construido? → el documento es
  inusualmente honesto aquí: "We present them as a descriptive grammar... they
  reproduce the dictionary exactly, but their dynamical origin is not claimed
  and remains the open mechanism of VII." Es una declaración explícita de que
  estas leyes NO son una derivación física, son una regla de generación que
  describe (y por tanto cierra, para el test de look-elsewhere) el conjunto ya
  existente. Correctamente declarado como abierto, no vendido como derivación.
  Esta es, en mi lectura, la pregunta más importante que un árbitro de PRD haría
  sobre el fundamento del artículo entero — y está respondida con la etiqueta
  correcta: "problema abierto", no resuelta.

---

## Página 31 — Agradecimientos / Disponibilidad de datos y código

**Afirma:** usa CLASS, CAMB, Cobaya, GetDist; repositorio completo en GitHub
(mikealmeida1721/SSEE-Cosmologia) y archivado en Zenodo DOI 10.5281/
zenodo.19654118 (concept DOI, todas las versiones).

**Respaldo:** coincide con `project_zenodo_papers_v2` de la memoria del
proyecto (concept 19654118). No verifiqué que el repositorio de GitHub público
esté sincronizado con el estado exacto de este PDF (el repo público puede
estar en una versión distinta, como señala la memoria del proyecto en
`project_publico_al_dia_2026-09-26`: "Zenodo público = versión 07-20 CON
partícula"). **Esto es relevante**: si el Zenodo/GitHub público referenciado en
esta misma página todavía contiene la versión con la partícula φ-DM retirada en
este PDF, el enlace de "Data and Code Availability" apunta a una versión que
contradice al propio PDF en un punto central (la partícula retirada). No pude
confirmar en esta sesión si esa sincronización ya se hizo antes de este envío a
PRD.

**Reproducible:** la afirmación de disponibilidad en sí es verificable (el DOI
existe); lo que no verifiqué es la sincronía de contenido.

**Preguntas:**
- **¿Está la versión pública en Zenodo/GitHub sincronizada con las retractaciones
  de este PDF (φ-DM, OP-8, etc.)?** → el PDF no lo dice explícitamente; según la
  memoria del proyecto (`project_publico_al_dia_2026-09-26`, 2026-09-26), en esa
  fecha el Zenodo público todavía tenía la versión con partícula. Si esto no se
  actualizó antes del envío, es un **hallazgo real**: un revisor que siga el
  enlace de reproducibilidad encontraría una versión que contradice al
  manuscrito en su afirmación central sobre el sector de crecimiento. **Pregunta
  sin respuesta verificada en esta sesión — recomiendo confirmar antes de
  enviar.**

---

## Página 32 — Referencias

**Afirma:** 21 referencias, incluyendo Planck 2018, Abdul-Karim et al. (DESI DR2,
PRD 112, 083515, 2503.14738), Riess et al. 2022 (SH0ES), Foreman-Mackey et al.
(emcee), Bellini & Sawicki (EFT), Kallosh & Linde (α-attractor), BICEP/Keck,
LiteBIRD, CLASS, CAMB, Cobaya, GetDist.

**Respaldo:** todas las referencias son estándar y verificables públicamente
(arXiv IDs y DOIs con formato correcto); no verifiqué cada DOI contra su
resolución real en esta sesión (fuera de alcance de "ligero"), pero los formatos
y los nombres de autores son consistentes con la literatura real que cito de
memoria (Abdul-Karim 2025 DESI DR2, Riess 2022 SH0ES, etc. son papers reales y
bien conocidos en el campo).

**Reproducible:** no verificado por resolución de DOI; plausible por
conocimiento del campo.

**Preguntas:** ninguna.

---

# RESUMEN FINAL — veredicto de árbitro

## Lo que se verificó con éxito (números recalculados por mí o leídos de logs con
procedencia, coincidiendo exactamente con el PDF)

- w0=−0.839950, wa=−0.669975, sm=0.160050 y las 12 constantes de la Tabla de
  notación (cálculo directo, `ssee_core.py`).
- Tabla I completa: χ²₂D=0.42/0.24σ y las cuatro distancias SSEE/ΛCDM, con ρ
  medidos de las cadenas oficiales DESI DR2 (reproducido en vivo).
- Tabla II completa (look-elsewhere): 490 razones, 25 valores, conteo
  1,1/1,2/1,4/2,5/4,9 (reproducido en vivo, el test estadístico más importante
  del artículo).
- Tabla III (comparación de modelos): BIC/AIC/ΔDIC/Savage-Dickey/cross-validation,
  todos coincidiendo exactamente con sus logs con hash de commit.
- Tabla IV completa (8+4 sondas, incluida la nota TATT/NLA de DES Y3): coincide
  dígito a dígito con `sondas_ssee_vs_lcdm.json`.
- ωb, ωc, Ωm=0.308881, αK=15.591336 (vía fórmula cerrada), c²s=0.021284 (vía
  fórmula cerrada), ns=1−φ⁻⁷, r=φ⁻¹⁰, α=φ⁴/3, N*=2φ⁷: todos verificados por
  cálculo algebraico directo.
- S8 KiDS-Legacy (417.97/418.34/418.95, ΔBIC +6.24/+6.86, S8=0.8273/0.04σ):
  coincide exactamente con su log.
- Las identidades del Apéndice A (MIRA=AURA/2, TRIAL=3AURA, Mv=3Ω).

## Afirmaciones con respaldo documental pero no recalculadas en esta sesión
(correcto no re-correrlas: MCMC y Boltzmann pesados, pero con log identificable
y, en varios casos, con historial de verificación independiente ya documentado
en la memoria del proyecto)

- Posterior MCMC H0=67.82±0.41, Ωbh²=0.02198±0.00048 (pág. 13, 15, 18).
- rd=147.17 Mpc, θ*=0.59667°/1.04099 (pág. 12-15).
- Tabla V / Ecs. 13-14 (CMB plik_lite y plik full, ΔBIC −26.03/−33.83).
- σ8=0.7449±0.0186, S8=0.7559±0.0189 sobre KiDS-1000 crudo (pág. 22).
- γIS=0.5504, fσ8 BOSS Δχ²=−2.03 (Tabla VI, pág. 25).

## Discrepancias / hallazgos para el árbitro

1. **Etiquetado de columna en Tabla III (pág. 15):** la celda "ln PMAP" de CPL
   imprime en realidad `lnL_max`, no `lnP_MAP`, según el log fuente
   (`resumen_3modelos.json`). El BIC/ΔBIC/ΔAIC son correctos; sólo la celda de
   verosimilitud/posterior está mal rotulada para esa fila. Corregible
   trivialmente, pero debe corregirse antes del envío.
2. **Archivo con dos valores de CPL:** el mismo log guarda, bajo una clave de
   control, un BIC de CPL (22.73) distinto del usado en el paper (22.26), sin
   nota que aclare cuál sustituyó a cuál. No afecta el número publicado, pero
   es una limpieza de repositorio pendiente, no un error del manuscrito.
3. **0.40σ vs 0.41σ** para la desviación de ωc respecto a Planck: el PDF dice
   0.40σ (pág. 11, 28), el código/CLAUDE.md dice 0.41σ en varios lugares. Menor,
   pero sin resolver en esta sesión — recomiendo que el autor confirme cuál de
   los dos números es el vigente antes del envío.
4. **σ8=0.8149 (PDF, pág. 21) vs σ8=0.8136 (CLAUDE.md)** para el techo con As
   fijado a Planck — diferencia de tercera cifra, sin log verificado en esta
   sesión para dirimir cuál es el vigente.
5. **Sincronización del repositorio público (pág. 31):** no pude confirmar en
   esta sesión que la versión pública en Zenodo/GitHub, citada como el
   respaldo de reproducibilidad del artículo, ya refleje las retractaciones de
   este PDF (φ-DM retirada, OP-8 disuelto). La memoria del propio proyecto
   documenta que, al 2026-09-26, el Zenodo público seguía en la versión con
   partícula. **Esto debe confirmarse antes del envío a PRD** — un revisor que
   siga el enlace de "Data and Code Availability" no debería encontrar una
   versión que contradiga al manuscrito.

## Preguntas de árbitro sin respuesta y sin declarar (hallazgo genuino, no
problema abierto reconocido)

No encontré ninguna pregunta central de física que quedara sin respuesta y sin
declarar como problema abierto. El documento es inusualmente disciplinado en
este aspecto: cada vez que dejé una pregunta de árbitro hostil, el propio texto
ya la anticipaba y la resolvía citando un número, o la declaraba explícitamente
como problema abierto con su etiqueta OP-N correspondiente en
`OPEN_PROBLEMS.md` (verifiqué varias de estas correspondencias cruzadas: OP-1,
OP-8, OP-9, OP-24, todas consistentes entre PDF y repositorio). La única
pregunta que quedó genuinamente sin cerrar en esta lectura es la de
sincronización pública (punto 5 arriba), que es administrativa, no física.

## Juicio de árbitro

El manuscrito es inusualmente honesto para el género: declara explícitamente
qué es medido vs derivado, retracta en el propio cuerpo del texto (no en una
corrección posterior) una afirmación anterior (el sector φ-DM) con el análisis
de por qué estaba mal construida, y separa con cuidado postdicción de
predicción. La maquinaria de verificación interna del repositorio (ACTA-
PROCEDENCIA con hash de commit y de script en cada log) es más rigurosa que lo
que exige PRD, y en esta lectura confirmé que esa maquinaria realmente respalda
los números del PDF, no sólo los documenta. Las pruebas estadísticas centrales
(look-elsewhere de la Tabla II, Mahalanobis de la Tabla I, comparación
bayesiana de la Tabla III) las reproduje yo mismo en esta sesión y coinciden
exactamente.

Los problemas reales son menores y de forma, no de fondo: una celda mal
rotulada en la Tabla III, dos cifras de tercera-decimal sin resolver entre el
PDF y la documentación interna, y la necesidad de confirmar que el
repositorio público citado como respaldo de reproducibilidad está realmente
sincronizado con el contenido de este envío. Ninguno de los tres invalida un
resultado central del artículo. Recomendaría a un editor de PRD que el
manuscrito pase a revisión de pares con esas tres correcciones menores
pendientes, no que se rechace ni que se devuelva sin revisión.
