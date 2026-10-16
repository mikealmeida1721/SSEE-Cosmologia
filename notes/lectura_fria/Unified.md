# Lectura fría — SSEE Unified Journal (20 páginas)

Fuente: `docs/SSEE_Unified_Journal.pdf` / `manuscript/SSEE_Unified_Journal.tex`.
Verificación hecha contra `manuscript/valores.yaml` (macros `\val{}`), los JSON de
`results/logs/`, `dvc.yaml` y `OPEN_PROBLEMS.md`. No se recorrieron MCMC/Boltzmann;
sólo lectura de JSON y aritmética ligera en Python.

---

## Página 1 (Abstract)

Afirma: k=2 en el CMB (A_s, τ libres; H0, ωb, ωc, ns fijos algebraicamente); w0=-0.839950,
wa=-0.669975 a 0.24σ de DESI DR2 w0waCDM (Pantheon+); H0=67.82±0.41 bajo prior H0glob
(0.68σ Planck, 0.34σ H0glob); ΔBIC=-10.90/-9.32 (k=0) y -5.81/-4.24 (k=2 conservador);
MCMC multi-sonda con likelihood completo da 1.31σ en el plano w0-wa.

Verificación:
- ΔBIC k=0 (-10.90/-9.32): coincide EXACTO con `results/logs/p2_ssee_fijo_k0.json`
  (`dBIC_ssee_menos_lcdm=-10.8956`, `dBIC_ssee_menos_cpl=-9.3223`).
- ΔBIC k=2 (-5.81/-4.24): coincide con `results/logs/resumen_3modelos.json`
  (`dBIC_vs_ssee` lcdm=5.8147, cpl=4.2414) y `dic_from_chains.json` para ΔDIC
  (-5.0215/-1.7008, citado en la Tabla 1 de la pág. 6).
- H0=67.82±0.41: no verificado directamente en esta pasada (viene de
  `mcmc_paper2_reframe.json` según `manuscript/valores_generados.tex` L386-388,
  coincide ahí 0.41/0.41/0.41 — no se abrió el JSON crudo).
- "0.90σ" (minimización plik_lite): coincide con `results/logs/perfil_h0_ancla.json`
  (H0_min_parabola=67.8734, σ=0.098, distancia a H0glob=0.9048σ → 67.87±0.10, 0.90σ).

Sin objeciones de respaldo en esta página.

## Página 2

Afirma: Ωm,CMB=0.308881; sm=0.160050 (no densidad); RMS CLASS 0.18%; G=1.0032,
σ8=0.8136, fσ8 0.70σ (ΛCDM 0.73σ); S8=0.8273 vs 0.8265±0.0176 (0.04σ); αK=15.591336,
c_s²=0.021284; √AURA≈1.9995 (texto extraído muestra "√" desplazado por el PDF, no es
error del documento); fscreen^IR=0.0673→H0glob,IR=68.13 (0.17σ); fscreen^full=0.069522→
H0glob=67.962142 (residuo +4.2e-6); M=9.68 meV.

Verificación — TODO coincide exacto:
- αK, c_s²: recalculado en Python desde φ,π con las fórmulas del propio texto →
  15.591332 y 0.0212837 (el papel redondea a 15.591336/0.021284; diferencia de la 6ª
  cifra por usar Ωde=0.308881 redondeado vs el valor completo — no es error).
- f_screen^IR=0.06725327, f_screen^full=0.06952161, H0_glob=67.96214152,
  residuo=4.1986e-6, σ_H0_glob=0.9677: todos en `results/logs/p10_uv_fscreen.json`,
  coinciden a 4-5 cifras.
- H0glob,IR histórico = 68.1278 (`p10_barrido_M4.json#barrido_H_glob.inf`), coincide
  con "68.13".
- G=1.0032, σ8=0.8136, tensión fσ8 0.6963σ/0.7251σ: `results/logs/fsigma8_canonico.json`.
- S8=0.8273, tensión 0.0433σ: `results/logs/kids_publicados.json#s8.legacy_prediccion`.

Nota al pie 1 (KiDS-1000 Appendix I, 2.39σ→1.42σ por n(z)): no verificable contra el
repo (es una cita de la literatura externa, Wright et al. 2025 Apéndice I) — aceptada
como cita, no como número propio del pipeline.

## Página 3 — Índice. Sin contenido verificable.

## Página 4 — Introducción

Afirma DESI DR2 2.8–4.2σ dependiendo de la muestra de SN y posterior central
(w0,wa)=(-0.838,-0.62). Cita externa (Abdul-Karim et al. 2025) — no verificable contra
el repo, es un dato de la literatura, consistente con lo citado en otros papers del
proyecto.

## Página 5 — Marco algebraico

Siete registros (Ω, β, KAL0, Psc, Kv, Tr, Mv) y w0, wa, sDE, sm, ns, Ωm,CMB.
Verificación: recalculados en Python desde φ=(1+√5)/2, π — TODOS coinciden a 6 cifras
con `results/logs/algebra_derivada.json#nucleo` (W0, WA, N_S, S_DE, S_M, OMEGA, BETA,
KAL0, K_V, M_V, P_SC).

## Página 6 — Validación MCMC, Tabla 1

H0: ssee 67.87±0.28, ΛCDM 68.39±0.28, CPL 67.26±0.52; Neff 79203/65893/44343;
ΔBIC ref/-5.81/-4.24; ΔDIC ref/-5.02/-1.70; clusters χ²/N 67.6(2.32σ)/68.9(2.41σ).
Verificación: TODO coincide exacto con `resumen_3modelos.json`, `dic_from_chains.json`
y `cumulos_zhang2026.json#modelos.ssee_rg_igimf/lcdm_igimf` (67.635/2.316σ,
68.852/2.405σ → redondean a 67.6/2.32 y 68.9/2.41).

## Página 7 — rd, clusters, MCMC multi-sonda

rd=147.17 vs 147.10 (CAMB); "+206" artefacto retirado (consistente con OP-8 y el
banner de CLAUDE.md, aunque CLAUDE.md no se usó como fuente — el propio OPEN_PROBLEMS
y el texto del paper narran el mismo retiro). Clusters 46 sistemas, IGIMF: ssee
2.32σ, ΛCDM 2.41σ; IMF canónica 8.64σ/8.46σ — verificado arriba.
MCMC multi-sonda libre: ωb,ωc,rdrag recuperados ≤0.2σ; H0=65.87±1.17; (w0,wa) libre
excluye ΛCDM a 3.22σ, ssee a 1.31σ.
Verificación: TODO coincide exacto con `results/logs/mcmc_full_posteriores.json`
(tensiones ombh2=0.0754σ, omch2=0.1955σ, rdrag=0.1024σ — todos ≤0.2σ; H0 tensión
1.786σ; distancia conjunta ssee=1.3137σ, lcdm=3.2211σ, ρ=-0.934).

## Página 8 — Tabla 2 y prueba fija

Tabla 2 (Ωbh², Ωch², rdrag, H0, Ωm, w0, wa posteriores vs algebraico): coincide EXACTO,
dígito a dígito, con `mcmc_full_posteriores.json` (incluido el control interno del
propio JSON, que ya compara "tabla" vs "lector" y dice `coincide: true` para H0, w, wa,
ombh2 — es decir, el propio pipeline ya se auto-verificó antes de escribir el PDF).
"∆BIC=-33.83 ... -26.03 (plik_lite)": coincide con `b1_k2.json` (dBIC=-33.8339) y
`cmb_dbic_mnu_propia.json` (dBIC=-26.0327).
"χ²r(TT)=1.042": no re-verificado en esta pasada (viene de Paper 3, no re-abierto el
JSON de CAMB).

## Página 9 — CLASS Boltzmann

Picos ℓ=220,536,813, RMS=0.18%. Coincide exacto con `results/logs/class_picos.json`
(generado 2026-10-16, el mismo día de esta lectura — es la versión más reciente del
repo, consistente con `git status` mostrando el archivo modificado sin commit).
rd=147.17 Mpc, 0.32σ de Planck (147.09±0.26): 147.17 viene de Paper 3 según el texto,
no reabierto aquí; la aritmética (147.17-147.09)/0.26=0.31σ es consistente con "0.32σ"
dentro del redondeo.

## Página 10 — Figura 1 y §5 (IS / crecimiento)

c²s,bare=w0≈-0.840 (inestable); estabilidad viene del campo de Paper 7, c_s²=+0.021284.
G=1.0032, σ8=0.8136 (con A_s de Planck). γ_IS=0.5504±0.0003.
Verificación: γ_IS no se abrió el JSON `p5_IS_perturbations_Q3.json` en esta pasada
(fuera de presupuesto); el resto ya verificado arriba.

## Página 11 — Cizalla y fσ8

As libre: log(10^10 As)=3.0255±0.0396 vs 3.04483 (0.49σ); χ²=417.97 (fijo) vs 418.34
(libre), ΔBIC=6.24; S8=0.8273 (0.04σ). BOSS: χ²=205.55(ssee)/207.58(ΛCDM), Δχ²=-2.03.
Verificación: TODO coincide exacto con `kids_publicados.json#s8.logA`,
`kids_legacy_bic.json` (deltaBIC=6.2432) y `results/logs/growth_2026-07/
R1R2_boss_lpt_cobaya.json` (chi2_real_min 205.549/207.576, dchi2_real=-2.027).

**Omisión parcial detectada**: el mismo JSON de BOSS (`R1R2_boss_lpt_cobaya.json`,
campo `vs_publicado`) muestra que, desglosado por bin de z, SSEE está PEOR que ΛCDM en
z=0.38 (tensión 1.758σ SSEE vs 1.548σ ΛCDM contra el dato publicado de Alam+2017) y
casi igual en z=0.51/0.61. El texto reporta sólo el χ² total (que sí favorece a SSEE,
-2.03) sin mencionar que ese resultado agregado esconde un bin donde el modelo
algebraico es el peor de los dos. No es necesariamente deshonesto (el agregado es el
número relevante para el test), pero es una desagregación desfavorable que el texto no
menciona y que sí aparece en su propio log. El mismo JSON tiene también
`perfil_vs_marginal.sigmas=1.815` (BOSS "no vota" en A_s — perfil vs marginal), dato que
tampoco aparece en el Unified (sí se menciona en otros papers del proyecto, según
CLAUDE.md, pero no en este documento).

## Página 12 — EFT, §6.2–6.3

hi_class: c_s² a 0.000%, αK a 0.011%. X/Xmin=1.045471. sK=0.403302=3·sDE·sm.
CPL: cruce fantasma en z=0.314; waφ propio=+0.41; OP-24 abierto.
Verificación: `hiclass_campo.json` da cs2_dif_rel=-1.21e-9 (→0.000%) y
alpha_K_dif_rel=-1.132e-4 (→0.011%): EXACTO. `algebra_derivada.json#algebra.
X_sobre_Xmin.valor`=1.045471 y `#algebra.z_cruce.valor`=0.314: EXACTO.
`results/logs/p7_fondo_campo.json#A_campo_solo.wa_local`=+0.41 (vía
valores_generados.tex L786): EXACTO. OP-24 existe en OPEN_PROBLEMS.md como "ABIERTO
(2026-09-07)" — la referencia es honesta.

## Página 13 — Extensiones: lensing fuerte y tensión de Hubble

√AURA≈1.9995 (histórico, no predicción); Fφ/FN~6e-13 a 10 kpc; SLACS/BELLS γ=2.078±0.027,
ME/Mdyn≈1.21; fscreen^IR=(π-φ)/(π+φ)²≈0.0673; H0glob,IR=73.04×(1-0.06725)=68.13 (0.17σ);
"el postulado... su mecanismo es abierto" (honesto).

**Hallazgo**: γ=2.078±0.027 y ME/Mdyn≈1.21 (muestras SLACS/BELLS) están tecleados a
mano en `manuscript/SSEE_Unified_Journal.tex` líneas 753-754, SIN macro `\val{}` y SIN
comentario `% ORIGEN-VALOR` cercano, y no aparecen en `manuscript/valores.yaml` ni en
ningún JSON de `results/logs/`. Son presumiblemente una cita de literatura externa
(compilaciones SLACS de Bolton et al. / BELLS de Shu et al.), pero el documento no cita
la referencia específica ni el repo tiene un cálculo propio que los reproduzca — no se
puede verificar de dónde salen esos dos números concretos dentro de este repositorio.

## Página 14 — UV completion y falsificación

M⁴=45α²ρc=5φ⁸ρc≈234.9ρc, M=9.68 meV; sK^full=0.41691 (+3.37%); "mueve el resultado a lo
sumo 0.57 km/s/Mpc" variando M⁴ de 0.2× a infinito; "votaría sólo si LiteBIRD r<0.0028".
Verificación: 45α²=5φ⁸=234.8936 EXACTO (recalculado). sK_full=0.4169052 (texto: 0.41691,
+3.37%: `s_K_UV_pct`=3.3728%) EXACTO. `p10_barrido_M4.json`: mueve_max_02_inf=0.5681
(→"0.57"), r_umbral_1sigma=0.002797 (→"0.0028") EXACTO.

Criterio de falsificación (§8): 5 criterios explícitos, incluido que el S8=0.8273 "no
tiene parámetro libre donde absorber la discrepancia" — bien planteado y auto-consciente
de que supersede un criterio más débil anterior (0.7559±0.0189).

## Página 15 — Tabla 4, Registro predictivo

**Inconsistencia interna detectada**: la Tabla 4 etiqueta "S8 (KiDS-Legacy, As fijado
por el CMB) = 0.8273 predicho... Status: **Prediction**". Pero la propia definición del
documento (pág. 4, §Introduction) dice: "prediction: fixed now, tested against
not-yet-released data" — y el mismo documento aclara en la nota al pie de la pág. 2 y en
§5.2 que "KiDS-Legacy predates this analysis by sixteen months, and no temporal priority
is claimed". Es decir: los datos de KiDS-Legacy YA estaban públicos cuando se hizo esta
comparación. Por la propia taxonomía del documento esto debería llamarse "Retrodiction"
(o "Postdiction"), no "Prediction" — es el mismo tipo de comparación que la fila
siguiente de la misma tabla ("earlier: KiDS-1000...") que SÍ está etiquetada
"Retrodiction". Esto no es un matiz menor: S8=0.8273 es el resultado estelar del
documento (aparece en el abstract, la introducción, las conclusiones y el criterio de
falsificación), y se llama repetidamente "predicts" en el cuerpo del texto cuando, según
la propia regla epistémica del documento, debería llamarse "retrodice".

## Página 16 — Discusión

Reconoce honestamente: (i) Ωm,CMB depende de que ωb (OP-1, parcial) y la identidad ωc
sean correctas — "a dependency chain, not an undetermined parameter" (afirmación
matizada correctamente); (ii) S8 a nivel no lineal requiere N-body, diferido por costo
computacional (consistente con OP-5b); (iii) la coincidencia H0glob vs 3(φ+π)² es
"a comparison, not a derivation" — QFT completa queda abierta para este y "todos los
modelos" (frase defendible). Todo esto tiene respaldo en OPEN_PROBLEMS.md (OP-1, OP-5b,
OP-19).

## Página 17 — Conclusiones y Tabla 5

Resumen de los 4 niveles; repite los mismos números ya verificados arriba, sin números
nuevos. Tabla 5 (parámetro completo) coincide con `algebra_derivada.json` ya verificado.

## Página 18 — Agradecimientos y disponibilidad de datos. Sin números a verificar.

## Páginas 19–20 — Referencias. No contienen afirmaciones numéricas propias del modelo.

---

# RESUMEN FINAL

## (a) Afirmaciones sin respaldo verificable en el repositorio
1. **γ=2.078±0.027 y M_E/M_dyn≈1.21 (SLACS/BELLS, pág. 13, líneas 753-754 del .tex)**:
   tecleados a mano, sin macro `\val{}`, sin comentario de origen, sin entrada en
   `valores.yaml` ni en ningún JSON de `results/logs/`. Presumible cita externa, pero
   no identificable dentro del repo qué compilación o script los produjo.
2. El dato externo de DESI DR2 "2.8–4.2σ según la muestra de SN" (pág. 4) y el
   posterior central "(w0,wa)=(-0.838,-0.62)" son citas de Abdul-Karim et al. 2025, no
   verificables contra el repo (aceptables como cita de la literatura, no como cálculo
   propio).

## (b) Números que no coinciden con su fuente
Ninguno detectado. Los ~40 números verificados (constantes algebraicas, ΔBIC/ΔAIC/ΔDIC
en sus tres variantes k=0/k=2/Table2, posteriores MCMC, S8/σ8/logA de KiDS-Legacy y
KiDS-1000, χ² de BOSS, picos CLASS, f_screen en sus tres piezas, M⁴/M UV, barrido de M⁴,
clusters Zhang+2026) coinciden con sus fuentes en `results/logs/*.json`, muchas veces a
4-6 cifras decimales exactas. El repositorio tiene una cadena de procedencia (DVC +
actas internas en cada JSON) inusualmente sólida para este tipo de documento.

## (c) Preguntas de árbitro sin responder ni señaladas como OP
1. **Conteo honesto de libres fuera del CMB**: el documento es cuidadoso en decir k=2
   para el ajuste CMB, pero la "postulate" de la forma multiplicativa de f_screen
   (pág. 13, reconocida como postulado) y la Conjetura C.1 (UV) no se cuentan en ningún
   "k" global del documento — ¿cuántos postulados/conjeturas no derivadas sostienen el
   edificio completo, más allá de A_s y τ? El documento lista honestamente que son
   postulados/conjeturas (buena señal), pero nunca da un conteo total consolidado de
   "postulados + conjeturas" como contraparte del k=2 que sí cuenta explícitamente. No
   es un hueco grave porque OPEN_PROBLEMS.md sí lleva ese inventario (postulados D, S,
   I mencionados en CLAUDE.md, que no debía leerse aquí) — pero dentro del propio
   Unified Journal esa cuenta total no aparece en ningún lugar, ni se referencia.
2. **Look-elsewhere / barrido de fórmulas**: el documento afirma "no optimisation over
   formula space was performed" (pág. 4) pero no cuantifica cuántas combinaciones de
   φ,π se probaron antes de fijar cada fórmula (salvo ω_b, donde OPEN_PROBLEMS.md sí
   documenta un barrido de 7 candidatos). Para w0, wa, ns, M, sK no hay mención de
   barrido ni de unicidad en este documento (sólo para ω_b). Pregunta sin responder NI
   señalada como OP para esas fórmulas específicas.
3. **¿Por qué el campo de Paper 7 "rueda" y produce wa, pero un solo campo canónico no
   puede cruzar w=-1?** El documento es honesto en declarar esto como OP-24 abierto
   (bien señalado, no es un hueco).
4. **Ingredientes iguales para ambos modelos en cada sonda**: el documento declara en
   la pág. 11 que BOSS se corrió "each with its own Σmν" (ingredientes propios por
   modelo) y en la Tabla 2 (pág. 8) usa el mismo likelihood completo para ambos — buena
   señal de que la pregunta SÍ se responde explícitamente para estas dos sondas. No se
   verificó aquí si ocurre lo mismo en los clusters (Zhang+2026) o en el run CLASS de
   §4, por falta de presupuesto en esta pasada.

## (d) Omisiones desfavorables
1. **BOSS por bin de z (pág. 11)**: el Δχ²=-2.03 total favorece a SSEE, pero el propio
   log (`R1R2_boss_lpt_cobaya.json#vs_publicado`) muestra que en z=0.38 SSEE está a
   1.76σ del dato publicado y ΛCDM a 1.55σ — SSEE es el modelo PEOR ajustado en ese bin
   específico. El texto no menciona esta desagregación, sólo el total agregado.
2. **Etiqueta "Prediction" para S8=0.8273 (Tabla 4, pág. 15)**: ver hallazgo (c) arriba
   — por la propia regla epistémica del documento (pág. 4) este resultado, comparado
   contra datos ya públicos 16 meses antes, debería llamarse "Retrodiction", no
   "Prediction". El verbo "predicts" se usa reiteradamente en el abstract, la
   introducción y las conclusiones para describir este mismo resultado. No es un error
   numérico, pero sí usa una palabra epistémicamente más fuerte de la que el propio
   marco de clasificación del documento permite para ese caso.
3. El `perfil_vs_marginal` de BOSS (1.82σ, "BOSS no vota en A_s") que aparece en el
   mismo JSON citado por el texto no se menciona en este documento (sí, según
   CLAUDE.md, en otros papers del proyecto) — es un matiz que templa la fuerza del
   Δχ²=-2.03 citado como "a mild, not decisive, preference", pero el propio texto ya
   usa ese lenguaje templado, así que el impacto de esta omisión es menor.
