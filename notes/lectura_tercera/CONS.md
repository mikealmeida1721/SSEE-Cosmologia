# Consolidados (Sealed, Unified, Endorser, Cover, Cover Letter) — tercera lectura (agente CONS, 2026-10-10)

## Estado: EN PROGRESO

## Estado: COMPLETA
Documentos cubiertos: SSEE_Sealed_Journal.tex (1297 líneas), SSEE_Unified_Journal.tex
(1052), SSEE_Endorser_Summary.tex (159), SSEE_Cover.tex (108), SSEE_Cover_Letter.tex
(96) — íntegros. Más dos archivos del paquete PRD fuera del encargo pero dentro del
mismo objetivo (dejar listo para la revista): submission_PRD/PRD_cover_letter.md y
PRD_justification_statement.md (hallazgo H4, bonus).

Comparación §3 (Sealed vs PRD): el párrafo compartido de ΔBIC CMB (p3_dBIC_diag,
lite_dBIC, b1_dBIC, b1_dBIC_k4) es byte-idéntico vía los mismos macros `\val` en
ambos documentos — sin divergencia de contenido.

## Resumen
4 hallazgos: 1 entidad-confundida/valor-coincidente-pero-macro-incorrecta (H1, ALTA) ·
1 contradicción-interna-mismo-símbolo-dos-valores (H2, ALTA) · 1 PR4/PR3 mal
rotulado fuera del alcance nominal pero dentro del paquete PRD (H4, ALTA) · 1
posible staleness de la carta de JCAP frente al objetivo actual PRD (H3, MEDIA).
0 números titulares que no coincidan con su `\val`/log en Sealed/Unified/Endorser —
el uso extensivo de macros (en vez de cifras a mano) en estos tres documentos hace
que prácticamente todo lo cuantitativo esté trazado y, verificado por muestreo,
coincida con sus logs. 0 conceptos retirados presentados como vigentes (verificado:
sin 72.86/73.040, sin φ-DM/m_φ/k_fs vigente, sin "PR4" mal rotulado DENTRO de los 3
documentos núcleo, sin MOND como lectura canónica — el único MOND mencionado está
correctamente marcado "alt., not canonical"). Las correcciones de hoy (P2 CMB-alone
w0, P3 σ8/S8 Planck/DESY3, P5 "discrepancia del 50%"→cota, P4 68.13 no canónico,
P7 Euclid σ, MIRA=Mirror Ratio, f_scr IR) NO se filtraron a estos 5 documentos en
sus formas erróneas — no aparecen en absoluto (0.073, r*=0.190, "discrepancy is
50%", w0=-1.03±0.03 CMB-alone, 0.4714 a mano, Freedman(2024), Bellini arXiv
1404.3604, Auger/Cao sin bibitem: ninguno de estos defectos de P1-P9/PRD se repite
aquí). `ssee_unified.bib` (compartido por Sealed/Unified/PRD) tiene el Bellini-Sawicki
correcto (arXiv:1404.3713) — el bug 1404.3604 es local a P7.tex/P8.tex, no contaminó
el bib compartido.

## Hallazgos

### H1 · SSEE_Unified_Journal.tex:875 · dimensión 3 (entidades) · ENTIDAD-CONFUNDIDA (mismo valor, otra entidad) · confianza ALTA
- Dice (fila de la tabla "Retrodictions"): `$H_0^{\rm glob,IR} = H_0^{\rm SH0ES}(1-\fscr^{\rm IR})$ & $68.13$ km/s/Mpc & $3(\phiG+\pi)^2=\val{H0_GLOBAL_d5}$ ($0.17\sigma$; IR only, partial) & Retrodiction`.
- Debe decir / por qué: esta fila compara el régimen IR (68.13) contra el **blanco puro**
  $3(\varphi+\pi)^2$. El macro correcto para ese blanco es `H0_ALG_d5` (fuente
  `algebra_derivada.json#nucleo.H0_ALG`), no `H0_GLOBAL_d5` (fuente
  `#nucleo.H0_GLOBAL`, el OUTPUT de la cascada completa). Ambos macros imprimen
  `67.96214` (coinciden a 5 decimales por diseño, residuo +4.2e-06), así que el PDF
  no muestra el error numéricamente — pero es la misma clase de error que advierte
  `src/ssee_core.py` para IGNIS vs K_v, y que el banner de CLAUDE.md prohíbe
  expresamente ("el número puro... NUNCA la semilla [ni] el resultado"). El propio
  documento usa el macro correcto `H0_ALG_d5` para el mismo blanco en las líneas
  155, 781 y 976 (tres apariciones, todas correctas) — sólo la fila de tabla 875
  usa la macro equivocada.
- Reemplazo propuesto: `3(\phiG+\pi)^2=\val{H0_GLOBAL_d5}` → `3(\phiG+\pi)^2=\val{H0_ALG_d5}`
  (misma cifra impresa, 67.96214, macro correcta).

### H2 · SSEE_Endorser_Summary.tex:116 vs :48 · dimensión 3/4 (entidades/coherencia) · CONTRADICCIÓN-INTERNA (mismo símbolo, dos valores) · confianza ALTA
- Dice (línea 48, tabla): `$H_0^{\rm glob}$ & $H_0^{\rm SH0ES}(1-f_{\rm scr}) = \val{H0_GLOBAL_d6}$ km/s/Mpc & ... & residual $+4.2\times10^{-6}$` → imprime **67.962142** (correcto, canónico).
- Dice (línea 116, prosa, §Paper 9): `...applied to the measured SH0ES rate $73.04\pm1.04$ returns a global background $H_0^{\rm glob}=68.13$~km/s/Mpc, $0.17\sigma$ from the pure algebraic number $3(\varphi+\pi)^2=\val{H0_ALG_d5}$...`
- Debe decir / por qué: el mismo símbolo `$H_0^{\rm glob}$` (sin superíndice IR) se usa
  en el mismo documento para DOS valores distintos: 67.962142 (línea 48, correcto,
  f_screen completo) y 68.13 (línea 116, régimen IR solo, M→∞, "incompleto, no
  canónico" según el banner de CLAUDE.md 2026-09-06/2026-10-03). El banner exige
  explícitamente que 68.13 lleve el símbolo `H_0^{\rm glob,IR}` "para que no se
  confunda" — aquí falta el superíndice y el lector ve dos definiciones de
  "$H_0^{\rm glob}$" a 68 líneas de distancia. Es el mismo patrón que el commit
  `7a9e72c`/`dbcb604` corrigió en otros documentos (P4, P8, etc.) pero no llegó a
  esta línea del Endorser.
- Reemplazo propuesto: `$H_0^{\rm glob}=68.13$~km/s/Mpc` → `$H_0^{\rm glob,IR}=68.13$~km/s/Mpc`
  (línea 116), dejando `$H_0^{\rm glob}$` (sin IR) reservado para 67.962142.

### H3 · SSEE_Cover_Letter.tex:15 (y SSEE_Cover.tex, tono general) · dimensión 4 (coherencia del paquete) · OBJETIVO-DE-REVISTA-POSIBLEMENTE-DESACTUALIZADO · confianza MEDIA
- Dice: `\begin{letter}{The Editorial Board\\Journal of Cosmology and Astroparticle Physics (JCAP)}`.
- Debe decir / por qué: el encargo de Mike y los commits recientes (`submission_PRD/`,
  `PRD_cover_letter.md`, `PRD_justification_statement.md`, `SSEE_PRD.pdf`,
  `SSEE_PRD_submission.zip`) indican que el objetivo de envío vigente es **PRD**,
  no JCAP. `manuscript/SSEE_Cover_Letter.tex` sigue dirigida a JCAP y vive en la
  misma carpeta que los consolidados (Sealed/Unified) que este informe revisa.
  No es necesariamente un error — puede ser intencional (Mike podría enviar el
  paquete consolidado de 10 papers a JCAP por separado del paper único de PRD,
  o puede ser un remanente de un plan anterior, ver CLAUDE.md sesión 2026-05-10
  "nueva estrategia de publicación", donde JCAP era la primera opción listada
  antes de que existiera `submission_PRD/`). Marco confianza MEDIA porque requiere
  una decisión de Mike sobre a qué envío corresponde cada carta, no es un error
  mecánico. `SSEE_Cover.tex` (la portada con imagen) no menciona revista, por lo
  que no tiene este problema; sólo incluyo la observación aquí porque comparten
  propósito (paquete de envío).
- Reemplazo propuesto: ninguno sin decisión de Mike/coordinador: (a) si el plan es
  enviar el documento consolidado (Sealed/Unified) a JCAP como antes, la carta
  está bien y sólo falta confirmarlo; (b) si el plan es sólo PRD, archivar o
  actualizar `SSEE_Cover_Letter.tex` para evitar que un lector futuro confunda los
  dos envíos.

### H4 (bonus, fuera del encargo nominal de 5 documentos, pero dentro del paquete PRD) · submission_PRD/PRD_cover_letter.md:12,20 y PRD_justification_statement.md:12 · dimensión 1 (valores)/trazabilidad · RETIRADO-PRESENTADO-COMO-VIGENTE · confianza ALTA
- Dice: título del manuscrito propuesto en la carta — `"Fixing the Dark-Energy
  Equation of State with Two Dimensionless Constants, φ and π: A Falsifiable,
  Parameter-Frugal Test Against DESI DR2 and Planck PR4."` y en el cuerpo:
  `carries a pre-committed DESI DR3 falsification criterion` ... `and Planck PR4`;
  y en `PRD_justification_statement.md:12`: `against DESI DR2 (0.24σ) and Planck
  PR4, with a pre-committed DESI DR3 falsifier.`
- Debe decir / por qué: el repositorio ya corrigió esta confusión exacta el
  2026-10-02 (`project_planck_pr4_era_pr3`, commit referenciado en MEMORY.md): los
  espectros usados en todo el proyecto son **Planck 2018 R3.01 (PR3)**, no PR4
  (sólo el lensing es PR4) — corregido en 13 documentos según esa memoria. Estos
  dos archivos `.md` del paquete de envío a PRD (la revista) no estaban entre los
  13 corregidos y siguen llamando "Planck PR4" a los espectros TT/TE/EE que son
  PR3. Es exactamente el error que el banner/memoria marca como cerrado en el
  resto del repositorio, reaparecido aquí — y esto está en el **título mismo**
  del manuscrito propuesto a la revista (línea 12 del cover letter), por lo que
  es el lugar de mayor visibilidad posible para este defecto.
- Reemplazo propuesto: `Planck PR4` → `Planck 2018 (PR3)` en las tres apariciones
  (título y cuerpo de `PRD_cover_letter.md`, cuerpo de `PRD_justification_statement.md`);
  verificar si el lensing mencionado en algún otro lugar de estos dos archivos sí
  debe quedar como PR4 (el lensing SÍ es PR4 en el proyecto).

## Nota (NO defecto, severidad mínima) · ssee_unified.bib:285 Bellini2015
La entrada `@article{Bellini2015,...}` tiene `year={2014}` pero la clave BibTeX
dice "2015" — es una entrada duplicada de `Bellini2014` (línea 14, misma cita,
mismo arXiv 1404.3713 correcto) con una etiqueta de clave inconsistente con su
propio campo `year`. No afecta ningún número citado (ambas entradas tienen el
arXiv correcto), es sólo un duplicado con nombre de clave confuso. Severidad
mínima, no numerado como hallazgo.

## Ruta
`notes/lectura_tercera/CONS.md` (este archivo).
