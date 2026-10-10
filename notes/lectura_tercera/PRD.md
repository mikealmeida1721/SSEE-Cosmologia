# submission_PRD/SSEE_PRD.tex — tercera lectura (agente PRD, 2026-10-10)

## Estado: COMPLETA (documento leído íntegro, líneas 1-1283)

## Resumen
3 hallazgos: 1 contradicción interna (H1, confianza ALTA) · 1 número-sin-origen
posiblemente residuo pre-fix (H3, confianza MEDIA) · 1 trazabilidad menor
(H2, confianza MEDIA/baja severidad). 0 conceptos retirados presentados como
vigentes (verificado: sin 68.13 como canónico, sin 72.86/73.040, sin partícula
φ-DM/m_φ/k_fs vigente, sin MOND, sin "PR4" mal rotulado — todo lo retirado
aparece correctamente narrado en pasado). Citas (14 claves bib revisadas)
todas presentes y correctas en `ssee_unified.bib`. α_K vs s_K: el PRD es,
de los documentos de la suite, el que SÍ distingue correctamente ambas
cantidades (nota positiva, no hallazgo) — salvo la línea 461 (H1).

## Tabla por página
Mapeo aproximado por sección (PDF de 33 páginas incl. índice; no se hizo
mapeo línea-por-línea exhaustivo por presupuesto, las referencias exactas
van por línea del .tex, que es la fuente):

| sección (líneas .tex) | tema | estado |
|---|---|---|
| 1-140 (portada, notación) | tabla de constantes, abstract | ✅ limpia |
| 141-440 (§core, DESI, look-elsewhere, Ω_m) | w0,wa, DESI DR2, dos-Ω_m | ✅ limpia |
| 440-670 (§2 cont., MCMC H0) | ωm, r_d, MCMC H0 | ✅ limpia |
| 670-730 (§EFT) | α_K, s_K, inflación | ⚠ H1 (línea 461, antes de esta sección pero referida aquí) |
| 730-990 (§CMB, §growth, §falsifiability) | CMB χ², S8 KiDS, registro | ⚠ H2 (líneas 316-1259), H3 (línea 990) |
| 990-1200 (§open problems, conclusiones, apéndice) | k=2, OPs, leyes del diccionario | ✅ limpia |
| 1200-1283 (agradecimientos, disponibilidad, bib) | citas, DOI Zenodo | ✅ limpia |

## Hallazgos

### H1 · pág ~9 (sección 3, "One matter density") · SSEE_PRD.tex:461 · dimensión 3/4 · ENTIDAD-CONFUSA · confianza ALTA
- Dice: `$f_{\rm scr}=\alpha_K^{\rm eff}/(3\,\mathrm{MIRA})$ (Paper~9), where it is the ``Mirror Ratio''.`
- Debe decir / por qué: el PROPIO documento, 250 líneas más adelante (línea 704-713), explica con detalle que
  la cantidad correcta en el apantallamiento es $s_K$ (ecuación de estado, saturación, "no entra H",
  invariante bajo cambio de ancla) y que confundirla con la kineticidad $\alpha_K$ (EFT, $\val{alpha_K_z0_d6}=15.591336$)
  es exactamente el error a evitar: "A distinct quantity, often confused with it [...] $s_K$ [...] Because $s_K$
  is pure equation of state, the screening amplitude $f_{\rm scr}=s_K/(3\,\mathrm{MIRA})$ is invariant [...] whereas
  a kineticity would not be." La línea 461 usa el símbolo que el propio §3.2 (EFT) advierte no usar ahí.
  Es autocontradicción dentro del mismo PRD: dos fórmulas distintas para $f_{\rm scr}$ ($\alpha_K^{\rm eff}$ en L461
  vs $s_K$ en L705-713), y L461 aparece ANTES en el texto, por lo que el lector ve primero la versión equivocada.
  Esto es justamente el pendiente de INSTRUCCIONES.md sobre 0.403302 ($s_K$) vs 15.591335 ($\alpha_K$ de P7):
  el PRD YA tiene la aclaración correcta (L700-716) pero no corrigió esta mención anterior.
- Reemplazo propuesto: `f_{\rm scr}=\alpha_K^{\rm eff}/(3\,\mathrm{MIRA})` → `f_{\rm scr}=s_K/(3\,\mathrm{MIRA})`
  (consistente con Eq. eq:sK_sealed y con Paper 9 canónico, $s_K=\val{S_K_d6}=0.403302$, NO con $\alpha_K=15.591336$ de P7).

### H2 · pág ~5-6 · SSEE_PRD.tex:316,328,351,378,1259 · dimensión 5 · NÚMERO-SIN-\val · confianza MEDIA
- Dice: `|w_a|=0.669975` (hand-typed, 4-5 apariciones) en vez de `\val{WA_d6}` (que da exactamente `-0.669975`,
  mismo valor en magnitud).
- Debe decir / por qué: la regla del proyecto es "nada de números tecleados a mano"; aquí el valor SÍ es
  correcto (coincide con `manuscript/valores_generados.tex:122`, `WA_d6=-0.669975`, log `algebra_derivada.json#nucleo.WA`)
  pero no está trazado por macro — es `|WA_d6|` sin macro de valor absoluto. No hay macro `WA_ABS_d6` disponible.
  Severidad baja: el número es correcto, sólo falta trazabilidad automática (si cambiara el álgebra, estos 5
  lugares no se actualizarían solos, a diferencia de los `\val{}`).
- Reemplazo propuesto: crear macro `WA_ABS_d6` en `valores_generados.tex` (o usar `-\val{WA_d6}` con signo) y
  sustituir las 5 ocurrencias; decisión del coordinador si vale la pena por tan poco riesgo.

### H3 · pág ~15 (tabla "Master register") · SSEE_PRD.tex:990 · dimensión 5 · NÚMERO-SIN-ORIGEN · confianza MEDIA
- Dice: `$\alpha_K^{\rm field}$ (bare, pre-integration) & EFT & $0.073$ & P7 & Internal check`
- Debe decir / por qué: busqué el origen de "0.073" en `manuscript/SSEE_Paper7_EFT.tex` (la fuente citada en la
  propia fila) y NO aparece: P7 sólo define $\alpha_K=\val{alpha_K_z0_d6}=15.591336$ (Eq. alphak, boxed, línea 534)
  y dedica un párrafo entero (líneas 543-563) a decir que "$\alpha_K$ is \textbf{not} the constant $\val{S_K_d6}$" —
  o sea, P7 ya NO reconoce una variante "bare, pre-integration" = 0.073. El mismo "0.073" aparece también en
  `manuscript/SSEE_Sealed_Journal.tex:1009` y `manuscript/SSEE_Endorser_Summary.tex:138`, pero en ninguno de los
  tres hay macro `\val` ni log que lo respalde — parece residuo de una versión anterior de P7 (antes de que
  "evaluado" diera 15.591336) que nadie limpió al actualizar la tabla. Al no estar en el documento que se cita
  como fuente, viola la regla de trazabilidad (dimensión 5) y posiblemente también la de coherencia (dimensión 4):
  P7 vigente no sostiene este número con esa etiqueta.
- Reemplazo propuesto: verificar en el histórico de P7 si "0.073" fue alguna vez $\alpha_K$ antes de la corrección
  de normalización (commit del 2026-09-07, análogo al caso $\beta_c=-$AURA retirado); si es un residuo pre-fix,
  retirar la fila o sustituirla por una referencia actual de P7 con macro `\val`. Decisión del coordinador
  (requiere revisar historial git de P7, fuera del alcance de sólo-lectura de este agente).

### Nota (NO defecto, confirmación positiva) · α_K vs s_K
- El PRD, a diferencia de lo que advierte INSTRUCCIONES.md para P3/P8/Unified/Sealed, SÍ distingue correctamente
  $\alpha_K$ (kineticidad EFT, Paper 7, $\val{alpha_K_z0_d6}=15.591336$, línea 693) de $s_K$ (ecuación de estado,
  Paper 9, $\val{S_K_d6}=0.403302$, línea 705), con una nota explícita de por qué no deben confundirse (L700-716).
  El ÚNICO lugar que no sigue esa regla es la línea 461 (H1 arriba). Confianza ALTA (verificado contra
  manuscript/valores_generados.tex líneas 112 y 131).

