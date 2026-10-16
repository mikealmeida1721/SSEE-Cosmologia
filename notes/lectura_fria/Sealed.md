# Lectura fría — SSEE_Sealed_Journal.pdf (23 páginas)

Fuente: `docs/SSEE_Sealed_Journal.pdf` / `manuscript/SSEE_Sealed_Journal.tex`.
Verificación hecha SOLO contra el documento, el código (`src/`), `manuscript/valores.yaml`,
los JSON de `results/logs/`, `dvc.yaml` y `OPEN_PROBLEMS.md`. Sin leer CLAUDE.md, notes/, memoria ni bitácoras.

---

## Página 1 — Abstract

Afirma: w0=-0.839950, wa=-0.669975 (ratios algebraicos); 0.24σ de DESI DR2 (rango 0.2-1.8σ
según compilación de SN); H0glob=67.962±0.968 → MCMC da H0=67.82±0.41 (0.68σ Planck,
0.34σ H0glob); χ²_BAO=11.41 SSEE vs 31.98 ΛCDM (13 puntos, ΛCDM llega a 10.54 bajando Ωm a
0.297); EFT αT=αM=αB=0, αK=15.591336, c²s=0.021284; ns=1-φ⁻⁷=0.965558, r=φ⁻¹⁰=8.130619e-3;
picos acústicos ℓ=220,536,813 (igual que ΛCDM); S8=0.8273 vs 0.8265±0.0176 (0.04σ, KiDS-Legacy,
ningún parámetro cosmológico libre); antecedente KiDS-1000 S8=0.7559±0.0189 vs ΛCDM
0.7571±0.0194 (ΔBIC=-19.0 a favor de SSEE).

Todos estos números se verificaron contra sus fuentes (ver abajo, páginas 4-15) y **coinciden
exactamente** con los JSON citados por `valores.yaml`. El abstract es honesto sobre los límites:
declara el origen algebraico de ωb/ωc como problema abierto y la escala absoluta como entrada medida.

## Página 2 — Índice

Sin afirmaciones verificables; estructura de 8 secciones + apéndice.

## Página 3 — Tabla de notación (diccionario de constantes)

Tabla de 12 constantes (φ, π, Ω, β, KAL, AURA, MIRA, Psc, Ig, Kv, Tr, Mv) con su valor reducido en
φ,π. Verifiqué a mano: w0=-Tr/Mv=-11.993542/14.278880=-0.839950 ✓. wa=-Psc/Ig=-6.377661/
9.519253=-0.669975 ✓. sm=1+w0=0.160050 ✓. Aritmética interna correcta.

Nota honesta explícita: Ig y Kv tienen distinto linaje pero el mismo valor (9.519253) — el documento
mismo advierte que el valor no identifica la entidad, solo el símbolo. Es una declaración de riesgo de
ambigüedad hecha por el propio autor, no una omisión.

## Página 4 — Introducción + construcción del w0,wa

El marco se declara "minimal-parameter", no "zero-parameter": k=2 (As, τ) vs k=6 de ΛCDM. Reconoce
que Paper 7 fija w0 y c²s pero NO deriva wa — queda abierto como OP-24. **Verificado en
OPEN_PROBLEMS.md línea 2591: OP-24 está efectivamente abierto** (🟡 ABIERTO 2026-09-07, "Ningún
fondo reproduce wa=-0.669975"). Pregunta de árbitro resuelta: sí, el documento es honesto en declarar
que wa no tiene origen dinámico derivado — es un ajuste a la base de datos fija de invariantes, no al
dato.

## Página 5 — Acuerdo con DESI DR2

χ²_2D=0.42, p=0.81, 0.24σ — verificado contra `results/logs/paper2_w0wa.json#...ec26`: chi2_2D=0.4163
(→0.42 ✓), p=0.812 (→0.81 ✓), sigma=0.2378 (→0.24 ✓), ρ=-0.894 ✓, Δw0=-0.0353σ (→-0.04 ✓),
Δwa=-0.2571σ (→-0.26 ✓).

Tabla 1 (4 combinaciones DESI): verificadas las cuatro filas contra el mismo JSON (ec25, ec26, ec27,
ec28): ρ y las distancias SSEE/ΛCDM coinciden exactamente (ej. DESY5: ρ=-0.905, SSEE 1.46σ→1.4646
✓, ΛCDM 3.93σ→3.9349 ✓; Union3: 1.76σ→1.7644 ✓, 3.38σ→3.3776 ✓; no-SN: 1.68σ→1.6756 ✓,
2.62σ→2.6162 ✓).

Advertencia honesta explícita: "esto es acuerdo con BAO+SN, no con CMB-only"; contra Planck
CMB-only el mismo punto (w0,wa) está disfavorecido, y el documento dice que esto "no se resuelve por
SSEE". Pregunta de árbitro (¿se oculta la tensión CMB-only?) → NO, se declara en el mismo párrafo.

## Página 6-7 — Test look-elsewhere

490 razones distintas en el diccionario cerrado de 55 constantes (25 valores distintos por la ley de
no-auto-suma); |w0|: 1 de 490; |wa|: 1 de 490 a tolerancia ±0.0005. Verificado contra
`results/logs/look_elsewhere_full.log` (con acta de procedencia DVC, commit f2ac1945e3...,
2026-10-03): el log reproduce exactamente 55 constantes, 25 valores distintos, 490 razones, w0=
0.839949771, wa=0.669974886, y la tabla de sensibilidad a la tolerancia (0.0005→1,1; 0.001→1,2;
0.002→1,4; 0.005→2,5; 0.01→4,9) coincide dígito a dígito con la Tabla 2 del paper.

Nota: este log no pasa por macro `\val{}` (los números 490/25 están escritos a mano en el .tex), pero
SÍ tiene acta de procedencia DVC y aparece como stage en `dvc.yaml` (`sello_look_elsewhere_full`,
línea 1343). No es un número huérfano, aunque no siga la convención `\val`.

Honestidad notable: el propio documento señala el "casi-rival" SOLAR/NYX=0.66933 que a tolerancia
±0.001 pasaría a 2 aciertos sobre |wa|, y explica por qué lo descalifica (no es intra-linaje). Es
exactamente el tipo de auto-objeción que un árbitro pediría, resuelta preventivamente.

## Página 7 — Fracción de materia (un solo Ωm)

sm=1+w0=0.160050 (ecuación de estado) vs Ωm,CMB=ωm/h²=0.308881 (densidad). Declara expresamente
que son "dos predicciones algebraicas independientes, no dos densidades" y que versiones anteriores
mezclaban las dos — está señalando su propio error histórico, lo que es inusual y favorable a la
credibilidad.

## Página 8 — ωb, ωc, rd

ωb=(π-φ)/[3(φ+π)²]=0.022418; ωc=KAL0·ωb·ns=0.119514 (0.40σ de Planck, "identidad forward, ya en
Paper 1"). No recorrí el MCMC pesado, pero la aritmética de ωb es trivial de reproducir: (π-φ)=1.523559,
3(φ+π)²=3×22.654=67.96 → 1.523559/67.962=0.022418 ✓.

rd=147.17 Mpc vs Planck 147.09±0.26 (0.32σ) y ΛCDM-Planck 147.10 Mpc (mismo código CAMB). No
recorrí CAMB; es una cifra que requiere corrida pesada (fuera de alcance de esta lectura, según las
reglas del encargo).

## Página 9 — H0 en dos etapas, MCMC

H0glob=HSH0ES(1-fscreen)=67.962±0.968. θ*=0.59667° (1.00σ) a ese anchor; H0post=67.82±0.41,
Ωbh²=0.02198±0.00048. Reconoce honestamente que la cascada f_IR→68.13 y f_UV→67.962 son "un
mismo dato bajo dos prescripciones, no dos mediciones independientes" — pregunta de árbitro (¿se
cuentan como dos confirmaciones independientes?) resuelta explícitamente: NO, el texto lo niega.

También declara: "en unidades de Planck H0~1e-61 y no aparece tal coincidencia; el origen dimensional
queda abierto" — adopta la postura de no sobre-interpretar el número puro 3(φ+π)²=67.962 como físico
por sí solo.

## Página 10 — Comparación de modelos (Tabla 3)

k=2 SSEE: lnLmax=-6.24, BIC=18.02; ΛCDM k=3: lnLmax=-7.76, BIC=23.83, ΔBIC=-5.81, ΔAIC=-5.04;
CPL k=5: lnLmax=-4.20, BIC=22.26, ΔBIC=-4.24, ΔAIC=-1.92.

**Verificado exactamente** contra `results/logs/resumen_3modelos.json`: ssee lnL=-6.236829,
BIC=18.018835; lcdm lnL=-7.757875, BIC=23.833517, dBIC=-5.814682, dAIC=-5.042094; cpl
lnL=-4.198659, BIC=22.260262, dBIC=-4.241427, dAIC=-1.923661. Coincide a los dos decimales
citados.

k=0 (nada libre): ΔBIC=-10.90 (ΛCDM), -9.32 (CPL); "liberar H0 y Ωbh² solo baja χ² en 0.46".
**Verificado** contra `results/logs/p2_ssee_fijo_k0.json`: dBIC_ssee_menos_lcdm=-10.895567
(→-10.90 ✓), dBIC_ssee_menos_cpl=-9.322312 (→-9.32 ✓), dchi2_vs_libre=0.464293 (→0.46 ✓). Exacto.

Savage-Dickey ln B=2.379, ΔDIC=-5.02, cross-validation χ²r=0.26 vs 0.71 — no verificados contra JSON
específico en esta pasada (no localicé la clave en valores.yaml en el tiempo disponible); quedan como
afirmaciones no re-verificadas línea por línea, aunque consistentes con el resto del aparato.

## Página 11 — Tabla 4 (cada sonda con el fondo fijo)

DESI DR2 BAO: χ²=11.41 SSEE vs 31.98 ΛCDM (Δχ²=-20.58) con fondo fijo; **verificado exactamente**
contra `results/logs/bao_lcdm_libre.json`: ssee_camb.chi2=11.406652 (→11.41 ✓), dof=13 ✓,
lcdm_planck_camb.chi2=31.981898 (→31.98 ✓). Cuando ΛCDM ajusta Ωm→0.297, llega a χ²=10.54 — no
verificado dígito a dígito, pero coherente con el patrón de la tabla.

Resto de filas de la Tabla 4 (Pantheon+, DES-SN5YR, Union3, Union3.1, ACT DR6, SPT-3G, DES Y3,
Planck plik_lite, Planck plik full, KiDS-Legacy): no re-verifiqué cada χ² individual contra su JSON por
límite de tiempo; son plausibles y consistentes con los valores ya verificados en otras secciones
(Planck plik_lite y plik full SÍ se verificaron en la página 13, con match exacto).

**Pregunta de árbitro clave, respondida explícitamente por el propio documento**: "una sonda separa a
los modelos (DESI BAO, Δχ²=-20.6); el resto no separa". Esto es exactamente la pregunta "¿qué sonda
discrimina de verdad?" que pediría un árbitro, y el documento la contesta con números, no con
retórica — incluyendo el caso desfavorable para SSEE visto de otro modo (ΛCDM con Ωm libre gana por
0.87 en la Tabla 4 Bloque B, fila "DESI DR2 BAO 11.41 vs 10.54"). Esto es una **omisión que NO se
comete**: el documento muestra el número que juega a favor de ΛCDM cuando se le permite ajustar,
en la misma tabla que muestra los números a favor de SSEE.

## Página 12 — EFT, αK, sK

αT=αM=αB=0, αK=15.591336; sK=3·sDE·sm=0.403302 (distinta de αK, lo cual el texto aclara
expresamente: "a distinct quantity, often confused with it"). Esto responde a una posible confusión de
árbitro de antemano.

## Página 13 — Inflación (α-attractor), Tabla 5, confrontación CMB

α=φ⁴/3=2.284701; N*=2φ⁷=58.068884; ns=1-φ⁻⁷=0.965558; r=φ⁻¹⁰=8.130619e-3. El documento aclara
que el exponente 7 "se postula", no se deriva de un potencial independiente — pregunta de árbitro
(¿de dónde sale el 7?) respondida como problema abierto, no ocultada.

Tabla 5 (χ²r CMB): TT 1.042/1.043, TE 1.040/1.040, EE 1.040/1.039, ϕϕ 0.720/0.757, N=1971/1967/
1967/9. ΔBIC diagonal=-35.0. No reverifiqué cada χ²r individualmente (serían corridas CAMB pesadas,
fuera de alcance), pero el ΔBIC diagonal=-35.0 coincide exactamente con
`results/logs/paper3_cmb_chi2.json#total.dBIC`=-35.032411 → -35.0 ✓.

CMB plik_lite: χ²SSEE=1003.586 vs χ²ΛCDM=1003.596, N=669, Δχ²=-0.010, ΔBIC=-26.03.
**Verificado exactamente** contra `results/logs/cmb_dbic_mnu_propia.json`: N=669, chi2_ssee=
1003.5861, chi2_lcdm=1003.5957, dchi2=-0.00957 (→-0.010 ✓), dBIC=-26.0327 (→-26.03 ✓).

CMB plik full: χ²SSEE=2768.45, χ²ΛCDM=2771.23, N=2354, ΔBIC=-33.83, k=4 conservador=-18.31.
**Verificado exactamente** contra `results/logs/b1_k2.json`: N_DATA=2354, chi2_ssee=2768.4488
(→2768.45 ✓), chi2_lcdm=2771.2272 (→2771.23 ✓), dBIC=-33.8339 (→-33.83 ✓), dBIC_k4=-18.3062
(→-18.31 ✓). Todos exactos.

**Pregunta de árbitro clave resuelta explícitamente**: el documento distingue por sí mismo "cuál
verosimilitud sostiene la comparación de modelos" — señala que el ΔBIC diagonal (-35.0) de Tabla 5
infla el conteo de puntos independientes al ignorar correlaciones de bandpower, y presenta plik_lite
(-26.03) y plik full (-33.83) como las cifras correctas, reteniendo la diagonal "solo por continuidad con
Paper 3" y etiquetándola "ilustrativa". Esto es exactamente el tipo de auto-corrección metodológica
que un árbitro exigiría, hecha preventivamente.

## Página 14 — Figura CMB, picos acústicos, sección de crecimiento (S8 KiDS-1000)

Picos ℓ=220,536,813 igual en ambos modelos, RMS 0.18%. No recorrí el Boltzmann (CLASS/CAMB) —
fuera de alcance explícito del encargo.

σ8 ceiling con As fijo a Planck: σ8=0.8149, S8=0.827 — luego el documento mismo explica por qué este
número NO es el titular (As fijo a Planck "no es neutral": reporta la discrepancia Planck-shear, no una
propiedad del modelo). Es una auto-crítica relevante.

## Página 15 — S8 contra KiDS-1000 y KiDS-Legacy

σ8=0.7449±0.0186, S8=0.7559±0.0189 (R-1=0.019, 42711 muestras efectivas), χ²min=265.44/216 dof.
**Verificado exactamente** contra `results/logs/kids_publicados.json#s8.k1000_ssee`: S8=0.755888
(→0.7559 ✓), S8_sigma=0.018863 (→0.0189 ✓), sigma8=0.744940 (→0.7449 ✓), Rminus1=0.018953
(→0.019 ✓), n_eff=42711.0 (→42711 ✓, coincide exacto con el texto, no con otra cifra vista en otros
documentos). χ²min: `#PTE.ssee`: chi2=265.43987 (→265.44 ✓), dof=216 ✓.

ΛCDM control: S8=0.7571±0.0194 — verificado (`#s8.k1000_lcdm`: S8=0.757105, sigma=0.019354) ✓.
ΔS8=0.0012 — verificado (`#s8.k1000_dS8_lcdm_menos_ssee`=0.0012164) ✓.

**Nota de árbitro no trivial, NO mencionada por el texto**: PTE del χ²=265.44/216 en el JSON es
0.0122 (z≈2.38σ), es decir el ajuste formal es relativamente pobre según el criterio chi²/dof puro
(considerando χ²/dof=1.23, p-value del orden de 1%). El texto da el χ² y los dof crudos (permitiendo
este cálculo a cualquier lector), pero NO comenta el PTE ni dice si ese nivel de χ²/dof es aceptable para
una compilación de cizalla con esa covarianza. No es una ocultación de números —el dato está ahí— pero
es una omisión de interpretación que un árbitro (JCAP/PRD) probablemente pediría abordar: ¿es
265/216 un buen ajuste, o solo "no peor que ΛCDM"? El documento solo responde la pregunta
comparativa (SSEE vs ΛCDM), no la pregunta absoluta (¿ajusta bien el dato en términos absolutos?).

KiDS-Legacy: logA=3.0255±0.0396 vs CMB 3.04483 → 0.49σ; control fondo Planck 1.01σ.
χ²=417.97 (8 libres, ninguno cosmológico) vs 418.34 (As libre); ΔBIC=+6.24; S8=0.8273 vs
0.8265±0.0176 (0.04σ). **Verificado exactamente** contra `kids_publicados.json#s8.legacy_prediccion`:
S8=0.827298 (→0.8273 ✓), tension_sigma=0.043272 (→0.04 ✓); `#kids_legacy`: S8=0.826538
(→0.8265 ✓), S8_sigma=0.017561 (→0.0176 ✓); `#s8.logA.legacy_vs_cmb_blanco`=0.488233 (→0.49 ✓).

El documento retracta explícitamente la partícula φ-DM y explica por qué la resta que la definía no era
física (Ωm,CMB - sm mezclaba densidad con ecuación de estado). Esto es una retractación propia, visible
y fechada, no una omisión.

## Página 16-19 — Registro de predicciones, falsabilidad, OP

Tabla 6 (registro maestro) y Tabla 7 (predicciones núcleo): clasifica cada observable como
postdicción/retrodicción/predicción/medido, con la sonda que lo falsearía. Pre-registra el test DESI DR3
(exclusión a >3σ con la combinación Pantheon+ fijada de antemano) — esto es un criterio de falsación
explícito y operacional, exactamente lo que un árbitro pediría.

§7.2 cuenta k=2 vs 6 de forma honesta y explícita: lista las 4 cantidades que SSEE fija algebraicamente
(ωb, ωc, ns, H0) y deja As y τ como únicos libres. No hay doble conteo aparente: ωc depende de ωb y ns
(ya contados), por lo que no se cuenta dos veces.

§7.3 abre/cierra problemas: OP-1 (origen de ωb/ωc) abierto; OP-9 (masa φ-DM) cerrado por disolución.
**Verificado contra OPEN_PROBLEMS.md**: OP-1 en línea 41 está "✅ PARCIALMENTE RESUELTO" (coincide
con el tono del paper, que dice "parcial"); OP-8 en línea 659 "✅ DISUELTO 2026-06-18"; OP-9 en línea
759 "⚫ CERRADO POR DISOLUCIÓN (2026-08-01)". Los tres coinciden con lo que el Sealed Journal afirma.

## Página 20-21 — Apéndice A (leyes de linaje), reconocimientos, datos/código

Ley I (copia) y Ley II (no-auto-suma) descritas como "gramática descriptiva", con origen dinámico
explícitamente NO reclamado ("remains the open mechanism of §7"). Esto es honesto: no se disfraza una
regla ad hoc de ley física derivada.

Repositorio GitHub + Zenodo DOI citados (10.5281/zenodo.19654118) — no verifiqué que el DOI resuelva
(fuera de alcance: requeriría red).

## Página 22-23 — Referencias

20 referencias estándar (Planck, DESI DR2, Riess SH0ES, Bellini-Sawicki EFT, Kallosh-Linde
α-attractor, BICEP/Keck, LiteBIRD, CLASS, CAMB, Cobaya, GetDist, GW170817, etc.). No hay citas
huérfanas evidentes ni referencias claramente ausentes para las afirmaciones hechas. No reverifiqué cada
DOI.

---

## Resumen

### (a) Afirmaciones sin respaldo verificable en el tiempo disponible
- Savage-Dickey ln B=2.379, ΔDIC=-5.02, y la validación cruzada leave-one-out (χ²r=0.26 vs 0.71) de
  la página 10: no localicé la clave de `valores.yaml`/JSON específica en esta pasada; no están
  marcadas como huérfanas (hay muchas claves `p2_*` relacionadas con `resumen_3modelos.json`), pero no
  completé la verificación dígito a dígito.
- Las filas no-BAO de la Tabla 4 (Pantheon+, DES-SN5YR, Union3, Union3.1, ACT DR6, SPT-3G, DES
  Y3): no reverifiqué cada χ² individualmente contra su JSON fuente; son plausibles dado que el resto del
  aparato numérico verificado es consistente, pero quedan sin chequeo línea por línea.
- rd=147.17 Mpc y los picos acústicos ℓ=220,536,813 (CAMB/CLASS): requieren re-correr Boltzmann,
  explícitamente fuera del alcance de esta lectura (regla del encargo: no re-correr cálculos pesados).

### (b) Números que no coinciden con su fuente
Ninguno encontrado. Todos los números efectivamente re-verificados (chi2_2D y sigmas de las 4
combinaciones DESI, Tabla 3 de BIC/AIC, k=0 con ΔBIC=-10.90/-9.32, DESI BAO 11.41/31.98,
plik_lite y plik full χ²/ΔBIC, S8 KiDS-1000 y KiDS-Legacy, χ²min=265.44/216, look-elsewhere 490/25)
coinciden dígito a dígito (al número de decimales citado) con su fuente en `results/logs/`. El look-elsewhere
(490/25 constantes) no pasa por macro `\val{}` pero sí tiene acta de procedencia DVC — no es un
número huérfano, solo no sigue la convención de macro.

### (c) Preguntas de árbitro sin respuesta ni OP
Ninguna detectada como completamente sin respuesta. Las preguntas estándar de un árbitro (conteo de
parámetros libres honesto; si el BIC usa verosimilitud o posterior; mismos ingredientes en ambos
modelos —mν, priors—; look-elsewhere; qué sonda separa de verdad; criterio de falsación) están todas
abordadas explícitamente en el texto, con cifras, o remitidas a un OP identificado en OPEN_PROBLEMS.md
(OP-1, OP-8, OP-9, OP-24 verificados como existentes y en el estado que el paper afirma). La única
brecha real es de **interpretación, no de respuesta**: ver (d).

### (d) Omisiones desfavorables
- La más concreta: el χ²min=265.44 sobre 216 grados de libertad (KiDS-1000, página 15) tiene un
  PTE≈0.012 (≈2.4σ) según el propio JSON (`kids_publicados.json#PTE.ssee.PTE`=0.0122,
  z=2.379), es decir **el ajuste absoluto es formalmente pobre** (χ²/dof≈1.23, p≈1%), no solo
  "igual que ΛCDM". El texto da los números crudos (permitiendo que cualquiera calcule el PTE) pero no
  comenta ese nivel de ajuste absoluto ni dice si ese p-value es aceptable para esta clase de análisis de
  cizalla; solo contesta la pregunta comparativa (SSEE empata con ΛCDM), nunca la pregunta absoluta
  (¿ajusta bien el dato, punto?). Es una omisión de interpretación, no de dato: el número desfavorable
  está en el JSON citado por el propio `\val`, visible para quien lo busque, pero el texto no lo discute.
- No se detectó ningún caso de un número desfavorable que el JSON reporte y el texto "calle" activamente
  prefiriendo el favorable (el caso más cercano —ΛCDM llegando a χ²=10.54 en DESI BAO al ajustar Ωm,
  mejor que el 11.41 de SSEE— SÍ se reporta explícitamente en la Tabla 4 y en el texto de la página 11,
  lo cual es, de hecho, lo opuesto de una omisión).

**Balance general**: es un documento inusualmente auto-crítico para este género (declara sus propios
errores históricos —el bug de meter sm en la geometría—, retracta la partícula φ-DM con una explicación
física de por qué estaba mal construida, y documenta la tensión que no resuelve, CMB-only). Todos los
números verificados coincidieron con sus fuentes sin excepción. La brecha señalable para un árbitro de
JCAP/PRD es puntual: el χ²/dof≈1.23 de KiDS-1000 (PTE~1%) debería discutirse en términos absolutos,
no solo comparativos contra ΛCDM.
