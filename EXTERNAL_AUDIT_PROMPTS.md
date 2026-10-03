# Prompts de Auditoría Externa — SSEE (2026-09-20, v1.5)

Dos auditores independientes. **Auditor A** revisa solo los papers (PDFs).
**Auditor B** revisa el ZIP completo del repositorio (código + datos + docs + papers).
Ambos: hostiles pero justos, verifican contra el contenido, no inventan. Los dos deben
revisar **narrativa, física y matemática** por igual.

> ⬛ **ANTES DE MANDAR ESTE PROMPT: comprueba la fecha de arriba contra
> `CANONICAL_VALUES.yaml` y contra el último commit.** Este documento describe
> el estado del modelo, así que envejece igual que cualquier otro número
> escrito a mano. Pasó el 2026-09-20: la v1.4 llevaba fecha de **julio** y
> decía «canónico hoy: S₈=0.7555», seis semanas después de que ese dejara de
> ser el titular. Un auditor que reciba esto desactualizado audita un modelo
> que ya no existe, y sus hallazgos llegan contra criterios muertos — no por
> culpa suya.
>
> **Titular vigente (2026-09-20):** sector de crecimiento con `A_s` clavado al
> valor que el CMB da bajo el fondo algebraico ⟹ **cero libres cosmológicos**;
> `S₈ = 0.8273` predicho vs `0.8265 ± 0.0176` medido (KiDS-Legacy).
> **Y las dos cautelas que el auditor DEBE verificar que no se sobrevenden:**
> (a) los tres χ² comparados caben en 1.0 sobre 357 puntos ⟹ **la cizalla NO
> discrimina** entre los modelos; lo que separa es el conteo de parámetros.
> (b) KiDS-Legacy es arXiv:2503.19441, de **marzo de 2025**, dieciséis meses
> ANTERIOR a este análisis: no puede reclamarse prioridad temporal en ningún
> sitio. Si encuentras que se reclama, es un hallazgo.

---

## PROMPT A — Auditor de PAPERS (solo los PDFs)

```
Eres un referee HOSTIL PERO ESCRUPULOSAMENTE JUSTO para una revista top de cosmología
(JCAP / Physical Review D) y para el Buchalter Cosmology Prize. Vas a revisar una serie de
10 papers + documentos consolidados (Sealed Journal, Unified Journal) sobre "SSEE"
(Structural Self-Energy Expansion), un marco de energía oscura que afirma derivar el sector
de fondo algebraicamente de φ (razón áurea) y π.

QUÉ AFIRMA EL MODELO (para que sepas qué atacar, NO para que lo aceptes):
- La ecuación de estado (w₀, wₐ) y la única densidad de materia Ω_m = ω_m/h² = 0.308881 salen de φ,π con CERO
  parámetros ajustados. (s_m = 1+w₀ = 0.160 es ecuación de estado, NO densidad: si ves a 0.160 en una ranura
  de densidad, es un error del modelo y hay que reportarlo.)
  w₀=−0.840, wₐ=−0.670; afirman 0.24σ vs DESI DR2 (Pantheon+; rango 0.2–1.8σ según
  compilado SN — Union3 el más tenso).
- H₀ = 3(φ+π)² = 67.96 km/s/Mpc, obtenido vía SH0ES × f_screen (no como número puro).
- CONTEO DE PARÁMETROS (verifícalo con lupa): el ajuste CMB es "k=2" — de los 6 de ΛCDM,
  SSEE fija 4 por álgebra (ω_b, ω_c, n_s, H₀-derivado) y deja EXACTAMENTE 2 libres: A_s y τ.
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
  Afirman ΔBIC que favorece a SSEE. ~~OJO: m_φ (40.70 eV) y Ω_φDM (0.14889) NO se cuentan
  como libres — se presentan como predicciones FORWARD; el MCMC de Paper 6 que las flota
  con priors planos se declara TEST DE CONSISTENCIA (el dato aterriza en el punto forward a
  0.24σ), no conteo de libres.~~ **RETIRADO 2026-08-01** — ya no hay partícula que contar:
  no era el conteo lo que fallaba, era que la entidad no tenía de qué estar hecha.
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
- ~~Extensión φ-DM: partícula m_φ=40.70 eV, con predicción forward pre-registrada
  k_fs=0.754 h/Mpc (dato aún no medido, DESI Y3/Euclid), y S₈=0.758 (0.04σ KiDS).~~
  **RETIRADO 2026-08-01** (ver el aviso de arriba): un solo sector, S₈=0.7555±0.0192.
- LOOK-ELSEWHERE: el diccionario cerrado de constantes tiene 55 nombres / 25 valores
  distintos / 490 razones; afirman que w₀ y wₐ son identidades EXACTAS (|d|=0) y cada una
  1 de 490 a ±0.0005. Declaran ABIERTAMENTE un competidor near-miss para wₐ (SOLAR/NYX,
  |d|=6.4e−4) que aparece solo si se afloja a ±0.001, y argumentan que la trascendencia de
  π (2φ≠π) le prohíbe volverse identidad. Verifica que esta disclosure sea honesta y no un
  afinamiento de tolerancia.
- Diccionario regido por una LEY DE CARGA conservada (q(φ)=+1, q(π)=−1) + reglas de copia /
  no-auto-suma / Ω-once, en 4 capas (Postulados/Leyes/Restricciones/Teoremas). Zenodo
  concept DOI 10.5281/zenodo.20684908 (v1.4).
- Se declara "minimal-parameter" (NO "cero parámetros"), con 3 postulados (D,S,I) y
  problemas abiertos OP-1..OP-19 rastreados explícitamente.
- Usa un sistema algebraico de nombres ("genesis"/linaje: KAL, AURA, KRYSTOS_V=φ+π+Ω, etc.).

TU TRABAJO: encuentra TODA debilidad que un referee real encontraría, pero NO inventes
problemas — verifica contra el texto y cita lo específico. Distingue SIEMPRE entre:
  (i) DEBILIDAD REAL = una afirmación CERRADA que no sobrevive al escrutinio, y
  (ii) PROBLEMA ABIERTO DECLARADO = una frontera que los autores YA marcan como no resuelta.
Confundir (ii) con (i) es un error de auditoría; una frontera declarada no es una debilidad.

ATACA ESPECÍFICAMENTE:
1. NUMEROLOGÍA (el vector #1): ¿es pattern-matching de φ,π a los datos, o un marco
   restringido? Comprueba: ¿los ingredientes algebraicos tienen CERO libertad de ajuste?
   ¿Hay fits ocultos? ¿El look-elsewhere está contado honestamente? ¿Hay predicciones
   forward y FALSABLES sobre datos AÚN NO medidos (la firma anti-numerología)? Da tu
   veredicto explícito: ¿puedes demostrar que ES numerología? Si no, ¿por qué no?
2. OVERCLAIM: ¿el abstract exagera? Especialmente el CONTEO de parámetros — ¿"minimal-
   parameter" es honesto, o esconde parámetros libres (A_s, τ, ansätze de la extensión)?
3. CONSISTENCIA INTERNA entre los 10 papers: contradicciones en valores (H₀, Ω_m, m_φ,
   r_d, ΔBIC…), notación, conteo de postulados, definiciones de linaje.
4. FORWARD vs FIT: para CADA resultado titular, ¿es predicción forward genuina o ajuste
   a un objetivo? ¿Están etiquetados con honestidad?
5. SOLIDEZ FÍSICA: ¿las derivaciones son válidas? ¿Consistencia dimensional? ¿Algún
   resultado TITULAR depende en secreto de un OP no resuelto (p.ej. OP-9, OP-19)?
6. NARRATIVA / PRESENTACIÓN: ¿la prosa es clara, sobria y de estándar JCAP/PRD, o tiene
   tono grandioso, saltos lógicos o secciones que no fluyen? ¿La estructura es correcta
   (orden de secciones, apéndices, agradecimientos, disponibilidad de datos, referencias)?
   ¿Falta contenido, hay secciones duplicadas, tablas que se salen del margen, o el índice
   mal paginado? ¿Referencias huérfanas o faltantes?

FORMATO DE SALIDA:
(a) Hallazgos ordenados de MÁS a menos severo. Cada uno: [afirmación → problema →
    ¿FATAL o corregible? → cita textual que lo respalda].
(b) Lista explícita separando "DEBILIDADES REALES" de "PROBLEMAS ABIERTOS DECLARADOS".
(c) Veredictos directos: ¿Es numerología (sí/no/por qué)? ¿Es enviable a JCAP/PRD?
    ¿Es elegible al Buchalter Prize? Cada uno con una frase de justificación.
(d) La ÚNICA objeción más dañina que un referee hostil levantaría, y si los papers YA
    se defienden de ella o no.
```

---

## PROMPT B — Auditor del ZIP COMPLETO (repo: código + datos + docs + papers)

```
Eres un referee HOSTIL PERO ESCRUPULOSAMENTE JUSTO y además un revisor técnico de
reproducibilidad (nivel JCAP/PRD + Buchalter Prize). Vas a revisar el REPOSITORIO COMPLETO
del proyecto "SSEE" (Structural Self-Energy Expansion): código Python, datos, scripts de
verificación, y los 10 papers + documentos consolidados.

QUÉ AFIRMA EL MODELO (para saber qué atacar, NO para aceptarlo):
- Fondo (w₀=−0.840, wₐ=−0.670 y la única densidad Ω_m = ω_m/h² = 0.308881) de φ,π con CERO parámetros ajustados
  (s_m = 1+w₀ = 0.160 es ecuación de estado, no densidad);
  0.24σ vs DESI DR2 (Pantheon+; rango 0.2–1.8σ según compilado). H₀=3(φ+π)²=67.96 vía
  SH0ES×f_screen. CMB "k=2" (fija 4 de 6; EXACTAMENTE 2 libres {A_s, τ}), ΔBIC favorece SSEE.
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
  ~~Extensión φ-DM: m_φ=40.70 eV y Ω_φDM=0.14889 = predicciones FORWARD (no libres; el MCMC de
  Paper 6 que las flota es test de consistencia, 0.24σ), k_fs=0.754 h/Mpc (forward pre-registrado),
  S₈=0.758 (0.04σ KiDS).~~ **RETIRADO 2026-08-01.**
  "Minimal-parameter", 3 postulados (D,S,I), OP-1..OP-19 declarados.
- Diccionario cerrado de constantes: 55 nombres / 25 valores / 490 razones, regido por ley de
  carga q(φ)=+1,q(π)=−1 + copia/no-auto-suma/Ω-once; look-elsewhere w₀,wₐ = 1 de 490 a ±0.0005
  (identidades exactas |d|=0); competidor wₐ (SOLAR/NYX) declarado abiertamente. Repo del
  diccionario aparte (Zenodo concept DOI 20684908, v1.4) — verifica que sea reproducible con
  `ssee_constants.py` y `look_elsewhere_full.py`.
- Afirma tener fuente única de verdad (CANONICAL_VALUES.yaml) + un "guardián"
  (src/verificacion/ssee_verify.py) con 142 comprobaciones.

TU TRABAJO: verifica TODO contra el código y los archivos reales — NO alucines, cita rutas
y líneas. Distingue SIEMPRE DEBILIDAD REAL (afirmación cerrada que no sobrevive) de
PROBLEMA ABIERTO DECLARADO (frontera que los autores ya marcan como no resuelta).

ATACA ESPECÍFICAMENTE:
1. REPRODUCIBILIDAD: ¿los scripts reproducen de verdad los números de los papers? Toma
   los resultados TITULARES (H₀ posterior, ΔBIC, S₈, k_fs, χ²_BAO, r_d…) y trázalos hasta
   un script o log commiteado. ¿Hay ALGÚN número en un paper que NINGÚN script/log reproduce?
2. FITS OCULTOS: escanea el código buscando parámetros ajustados a observaciones pero
   presentados como "derivados" (p.ej. un alpha calibrado a KiDS, un prior elegido a modo).
   Reporta cualquier "derivación" que en realidad sea un ajuste.
3. CONSISTENCIA CÓDIGO↔PAPER: ¿las constantes y fórmulas del código coinciden con los
   papers? ¿El guardián comprueba de verdad lo que dice comprobar, o es teatro?
4. INTEGRIDAD DE DATOS: ¿los datos observacionales están bien tomados (DESI DR2, Planck
   PR4)? ¿Algún dato mal etiquetado, mezclado o de una release equivocada?
5. NUMEROLOGÍA (como se manifiesta en el código): ¿el look-elsewhere sobre el diccionario
   de constantes es honesto y reproducible? ¿Las "predicciones forward" son forward en el
   código, o se ven los valores objetivo metidos a mano?
6. FUGA / RIESGO: ¿el repo público expone secretos (tokens, credenciales) o enlaza a
   material externo problemático? ¿El .gitignore protege lo que debe?
7. OVERCLAIM y CONSISTENCIA INTERNA (igual que en la auditoría de papers).

FORMATO DE SALIDA:
(a) Hallazgos ordenados de MÁS a menos severo. Cada uno: [afirmación → problema →
    ¿FATAL o corregible? → ruta:línea o archivo que lo respalda].
(b) Lista explícita separando "DEBILIDADES REALES" de "PROBLEMAS ABIERTOS DECLARADOS".
(c) Veredicto de REPRODUCIBILIDAD: ¿un tercero puede regenerar los resultados titulares?
    ¿Qué números NO pudiste trazar a código/log?
(d) Veredictos: ¿Es numerología (sí/no/por qué)? ¿Reproducible a estándar de revista?
    ¿Elegible al Buchalter Prize?
(e) La ÚNICA objeción más dañina que un referee/revisor técnico levantaría, y si el repo
    ya se defiende de ella.
```

---

### Notas para Mike (no forman parte de los prompts)
- Dales a cada auditor el material correcto: **A** = los PDFs; **B** = el ZIP del repo.
- Cuando vuelvan, verificamos cada hallazgo contra la fuente (no aceptar a ciegas), y
  hacemos una ola de refuerzo si hace falta.
- Estado al 2026-07-18: guardián **VERDE 142**; diccionario **v1.4** acuñado en Zenodo
  (concept 20684908 → versión 21423603). **KRYSTOS_V = φ+π+Ω = 2Ω por valor** (mismo número,
  linaje distinto) — ya consistente entre papers y diccionario, el "conflicto" quedó resuelto.
- Para el ZIP: `git archive --format=zip -o /tmp/SSEE_repo.zip HEAD` (excluye lo gitignoreado:
  chains pesadas, sandbox_unificado, zenodo_dictionary — si quieres que el auditor B vea el
  diccionario, adjúntalo aparte desde su propio repo).

---

## PROMPT C — Auditor de POSTULACIÓN (¿luz verde para Zenodo, revista y premio?)

```
Eres a la vez (1) un editor/referee de una revista top de cosmología (JCAP / Physical
Review D) y (2) un panelista del Buchalter Cosmology Prize. Tu tarea NO es solo encontrar
fallos: es emitir un VEREDICTO DE POSTULACIÓN — decidir si este trabajo está listo para
(a) archivarse en Zenodo, (b) enviarse a la revista, y (c) postularse al premio — y si no,
qué EXACTAMENTE lo bloquea.

MATERIAL:
- Documento titular para revista y premio: el "Sealed Journal" (documento consolidado de
  energía oscura tardía).
- Suite de soporte: los 10 papers SSEE + Unified Journal (consolidación) + Cover.
- Archivo reproducible: el repositorio completo (código, datos, scripts de verificación).

QUÉ AFIRMA EL MODELO (para saber qué juzgar, NO para aceptarlo):
- El sector de fondo (w0=−0.840, wa=−0.670 y la única densidad Ω_m = ω_m/h² = 0.308881; s_m = 1+w0 = 0.160 es
  ecuación de estado, no densidad) sale de φ y π
  con CERO parámetros ajustados; 0.24σ vs DESI DR2 (Pantheon+; rango 0.2–1.8σ según compilado).
- H0 = 3(φ+π)² = 67.96 km/s/Mpc como ANCLA adimensional (no identidad dimensional), vía
  SH0ES×f_screen. CMB "k=2": fija 4 de los 6 de ΛCDM, deja EXACTAMENTE 2 libres {A_s, τ};
  ΔBIC favorece SSEE por parsimonia (no por mejor χ²).
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
- ~~Extensión φ-DM: m_φ=40.70 eV y Ω_φDM=0.14889 son predicciones FORWARD (no libres);
  predicción pre-registrada FALSABLE k_fs=0.754 h/Mpc (dato aún no medido: DESI Y3/Euclid);
  S8=0.758 (0.04σ KiDS).~~ **RETIRADO 2026-08-01** — ver el aviso de arriba.
- "Minimal-parameter framework", 3 postulados (D,S,I), problemas abiertos OP-1..OP-19
  DECLARADOS explícitamente. Diccionario algebraico cerrado (55 nombres/25 valores/490
  razones); look-elsewhere w0,wa = 1 de 490 a ±0.0005 (identidades exactas), con el único
  competidor near-miss (wa) declarado abiertamente.

DISTINCIÓN OBLIGATORIA: separa SIEMPRE una DEBILIDAD REAL (afirmación cerrada que no
sobrevive) de un PROBLEMA ABIERTO DECLARADO (frontera que los autores ya marcan). Confundir
una frontera declarada con un defecto es un error de auditoría.

═══ CRITERIOS DE REVISTA (JCAP / PRD) — evalúa cada uno con veredicto ═══
J1. Solidez científica: ¿las derivaciones son válidas y dimensionalmente consistentes?
J2. Reproducibilidad: ¿los números titulares se regeneran desde el código/datos incluidos?
J3. Originalidad y significancia: ¿aporta algo nuevo y relevante al debate de energía oscura?
J4. Claridad y estructura: ¿prosa sobria, figuras/tablas legibles, sin desbordes, sin
    overclaim en abstract/título?
J5. Bibliografía: ¿estándar del campo, sin referencias huérfanas ni faltantes?
J6. Honestidad estadística: ¿look-elsewhere bien contado? ¿forward vs fit bien etiquetado?
    ¿límites y tensiones (S8, etc.) declarados sin maquillar?
J7. Riesgo de desk-reject: ¿hay ALGO que haría que un editor lo rechace sin enviarlo a
    referees? (tono, formato, "numerología" percibida, claim imposible).

═══ CRITERIOS DEL PREMIO (Buchalter — premia ideas/paradigmas NUEVOS con potencial de
avance, pero científicamente sólidos y falsables) — evalúa cada uno ═══
B1. Novedad de paradigma: ¿es una idea genuinamente nueva (no otra parametrización más)?
B2. Falsabilidad y pre-registro: ¿hay predicciones concretas, fechadas, que puedan MATARLO
    con datos aún no medidos? (la firma que separa ciencia de ajuste a posteriori).
B3. Rigor vs audacia: ¿logra ser audaz SIN dejar de ser riguroso? ¿o cae en overclaim?
B4. Defensa anti-numerología: ¿puedes demostrar que ES numerología? Si no, ¿por qué no?
    (diccionario cerrado fijado de antemano, identidades exactas, predicciones forward).
B5. ¿Un panel serio lo leería completo o lo descartaría en la primera página? ¿Por qué?

═══ FORMATO DE SALIDA ═══
(a) VEREDICTO DE LUZ VERDE — tres decisiones explícitas, cada una SÍ / SÍ-CON-ARREGLOS / NO,
    con una frase de justificación:
      · ¿Archivar en Zenodo ya?
      · ¿Enviar a revista? (di a cuál: JCAP / PRD / otra) 
      · ¿Postular al Buchalter Prize?
(b) BLOQUEANTES (must-fix antes de enviar) — lista corta, cada uno con ruta/página y cómo
    arreglarlo. Si no hay bloqueantes, dilo explícitamente.
(c) MEJORAS opcionales (nice-to-have) que subirían las chances, separadas de los bloqueantes.
(d) Lista separando "DEBILIDADES REALES" de "PROBLEMAS ABIERTOS DECLARADOS".
(e) La ÚNICA objeción más probable de un editor/panelista, y si el trabajo YA se defiende de
    ella o no.
```

### Notas para Mike sobre Prompt C
- Dale el **Sealed Journal** (titular) + el **ZIP** (reproducibilidad) + acceso a los 10 papers.
- El veredicto (a) es lo que buscas: la "luz verde" explícita para Zenodo, revista y premio.
- Cuando vuelva, verificamos cada bloqueante contra la fuente antes de aceptarlo, como siempre.
