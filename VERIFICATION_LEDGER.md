# Registro de Verificación — Modelo SSEE-V3.6

> Reconstrucción verificada del modelo. No se reescribe desde cero: cada elemento
> se **verifica** — qué es, qué función cumple, dónde se usa, dónde debe estar, y
> con qué conecta — antes de declararse resuelto y, finalmente, sellarse.

## Por qué existe este registro

La revisión árbitro hostil de los 11 documentos (2026-05-21) encontró que varias
"resoluciones" marcadas `✅ RESUELTO` en `CLAUDE.md` nunca fueron verificadas de
verdad. Caso confirmado por `git`: la fórmula k-mouflage de Paper 8
(`r_km³ = M_obj/(4π M_pl M²)`) es **dimensionalmente inconsistente** y se
introdujo en el commit `295ed6e` ("OP-4 resolved"). Es decir: una corrección
creó un error nuevo, se commiteó como "fix", se escribió como resuelto, y pasó
**siete auditorías posteriores** sin que nadie lo detectara — porque esas
auditorías revisaban strings, citas y retórica, nunca la física.

Este registro existe para que eso no vuelva a pasar: nada se da por resuelto sin
pasar las seis comprobaciones, y nada se sella sin re-verificarse.

## Ciclo de vida de un elemento

1. **pendiente** — identificado, sin verificar.
2. **verificado** — pasó las 6 comprobaciones.
3. **resuelto** — confirmado por Mike; se le asigna el nuevo estado resuelto.
4. **re-verificado** — el estado resuelto se comprueba otra vez, de forma
   independiente. El elemento queda **aprobado**.

## Las 6 comprobaciones

Para cada elemento se verifica y se registra:

1. **Numérica** — el valor o la identidad se calcula y coincide.
2. **Dimensional** — las unidades cierran (esto es lo que faltó en Paper 8).
3. **Derivación** — el elemento se sigue de sus premisas; no es post-hoc ni un fit.
4. **Rol** — qué función cumple en el modelo está claro y es necesario.
5. **Ubicación** — está en el lugar correcto y se usa de forma consistente en
   todos los papers donde aparece.
6. **Conexiones** — de qué depende y qué depende de él; el grafo cierra.

## Sello (por paper)

Un paper se **sella** solo cuando *todos* sus elementos están `re-verificado` **y**
pasa un chequeo completo final. El sello es invisible — no aparece en el PDF: se
registra aquí el **commit git + `sha256` del `.tex`** al momento del sellado. Si
el archivo cambia después, el `sha256` deja de coincidir → el sello se rompe → el
paper vuelve a verificación.

## Capas de verificación (orden ascendente — bottom-up)

| Capa | Contenido | Estado |
|------|-----------|--------|
| **L1** | Axiomas y constantes algebraicas | re-verificado ✓ |
| **L2** | Parámetros cosmológicos derivados | re-verificado ✓ |
| **L3** | Mecanismos y derivaciones (OP-1..OP-7, EFT, IS, dos-sectores, k-mouflage, f_screen, m_φ, K(X) UV, T_μν, disformal, retención MIRA) | re-verificado ✓ (17 elementos; 1 verif., 7 PARCIAL, 9 ABIERTO — dos-Ω_m es el central) |
| **L4** | Confrontaciones con datos (MCMC, CMB, ΔBIC, fσ₈, S₈) | re-verificado ✓ (pipelines re-corridos; CMB+MCMC reproducen, r_d/H₀ derivaron) |
| **L5** | Papers (sellado) | pendiente |

Regla: un elemento de una capa no pasa de `verificado` si sus insumos de capas
inferiores no están al menos `verificado`.

---

# Valores Canónicos del Modelo SSEE

**Esta es la fuente canónica.** "Canónico" no significa *permanente* —
significa **el valor que refleja el estado real más actual del modelo**.
Cuando un pipeline se re-corre y el número cambia, se actualiza **aquí
primero** y luego se propaga a todo lo que lo use.

**Regla estructural.** Si un resultado cambia, cambia en *todas* partes
que lo usan. Cualquier script, paper o cálculo que use uno de estos
números debe reflejar el valor de esta tabla. Un valor distinto sin
justificación es un error que debe detectarse de inmediato.

## A. Constantes algebraicas — invariantes (derivadas de φ, π)

Fuente única: `src/ssee_core.py`. Todo script importa de ahí. El guardián
(sección «Fuente canónica») re-computa cada una y verifica `ssee_core`
contra esa recomputación — si el módulo se edita mal, el guardián → ROJO.

| Símbolo | Valor | Identidad | Rol |
|---|---|---|---|
| φ | 1.6180339887 | (1+√5)/2 | Axioma generador |
| π | 3.1415926536 | — | Axioma generador |
| Ω | 4.7596266423 | φ+π | Métrica de Estabilidad |
| β | 2.3798133212 | (φ+π)/2 | Escalar de Acoplamiento Base |
| KAL₀ | 5.5214059748 | β+π | Retención Estructural |
| P_sc | 6.3776606311 | Ω+φ | Escalar de Evolución Dinámica |
| K_v | 9.5192532847 | φ+π+Ω | Restricción Estructural |
| T_r | 11.9935419298 | 3(φ+β) | Horizonte de Saturación 3D |
| M_v | 14.2788799270 | φ+π+K_v | Invariante Dimensional Máximo |
| AURA | 3.9978473099 | (3φ+π)/2 | = 2·MIRA = φ+β |
| MIRA | 1.9989236550 | AURA/2 | Frecuencia de Observación |
| w₀ | −0.8399497713 | −T_r/M_v | Ecuación de estado hoy |
| wₐ | −0.6699748857 | −P_sc/I_g | Evolución de la EoS (I_g=π+P_sc; vale lo mismo que K_v pero es otra entidad) |
| s_DE | 0.8399497713 | T_r/M_v = \|w₀\| | Saturación de la EoS — **no** es una densidad (la densidad es 1−Ω_m) |
| s_m | 0.1600502287 | 1+w₀ | Saturación complementaria de la EoS — **no** es una densidad, **no** va en E(z) |
| Ω_m | 0.3088808406 | ω_m/h² = (ω_b+ω_c+ω_ν)/h², h=H_glob/100 | Materia total: fondo, Poisson y CMB (2026-10-02: la fila decía MIRA·Ω_m,dyn, el puente RETIRADO el 2026-06-18; su valor queda en el historial de git) |
| H₀^alg | 67.9621373234 | 3(φ+π)² | Número puro, sin unidades: el **blanco** de H_glob = H_SH0ES(1−f_screen) = 67.9621415220, nunca la semilla (banner 2026-09-06) |
| n_s | 0.9655581463 | 1−φ⁻⁷ | Índice espectral |
| α_K | 0.4033024589 | 3·Ω_DE·Ω_m,dyn | Kineticity EFT |
| Ω_b h² (alg) | 0.0224177568 | (π−φ)/(3Ω²) | Densidad bariónica OP-1 (**ABIERTO**) |

## B. Valores de pipeline — dependientes de estado (script + datos + fecha)

Estos **no** se derivan de φ,π — los calcula un pipeline (CAMB/CLASS/emcee).
Cambian si el script o los datos cambian. Cada uno lleva su **procedencia**.

| Cantidad | Valor canónico | Fuente | Re-anclado |
|---|---|---|---|
| H₀ anchor/prior (H_glob, ω_m-directo) y dónde minimiza el CMB | H_glob 67.962 km/s/Mpc; con ω_b, ω_c y n_s fijos por álgebra y A_s, τ perfilados, plik_lite se minimiza en **67.873 ± 0.098** — H_glob queda a **0.90σ**, no en el mínimo. Control ΛCDM (ω de Planck): 67.333 ± 0.094, 0.05σ de su 67.36 — PASA | `src/p03_cmb/perfil_h0_ancla.py` → `results/logs/perfil_h0_ancla.json` (etapa DVC). El log citado antes, `p3_h0anchor_reframe.log`, barre Ω_m con H fijo: no contenía barrido en H₀ | 2026-10-01 (antes 2026-06-19, rejilla gruesa cuyo nodo mínimo era 67.962) |
| ΔBIC CMB (plik FULL, nuisances libres, k=3 vs 6 — cadena de VALIDACIÓN con H₀ libre, no el titular) | **−25.766** — χ²_SSEE=2770.443 vs χ²_ΛCDM=2772.917, Δχ²=−2.474 (SSEE ajusta MEJOR con 3 params menos), N=2354 | `ssee_paper3_b1_mcmc.py --mode both` (Cobaya, R−1=0.017) → `results/logs/b1_analyse.log` | 2026-07-27 |
| H₀ posterior CMB (plik FULL, H₀ flotado k=3) | **67.8809 ± 0.1005 km/s/Mpc** — 0.81σ del ancla 3(φ+π)²=67.9621; la cadena RECUPERA el ancla, no lo asume; σ 5.3× más chico que ΛCDM (67.394±0.528) | `ssee_paper3_b1_mcmc.py` → `results/logs/b1_analyse.log` | 2026-07-27 |
| H₀ MCMC posterior (prior H_glob = SH0ES·(1−f_screen) = 67.962 ± 0.968, DESI DR2, ω_m algebraico fijo R25, r_d y distancias CAMB) | **67.8226 ± 0.4126 km/s/Mpc** — 0.34σ de H_glob, 0.68σ Planck (semilla fija en emcee: determinista, control de dos corridas idénticas 2026-10-01) · DESI sola (prior plano) 67.7843 ± 0.4554 (0.39σ H_glob; era 67.7931 ± 0.4603, log: git:513e84e:results/logs/h0_four_priors.json, sin semilla) | `ssee_paper2_mcmc_reframe.py` (100w×25k, N_eff=80365; re-corrido 2026-10-01 sin el término de cúmulos, que era constante: H₀ se movió 0.004 (ruido MC)) → `results/logs/mcmc_paper2_reframe.json`; distancias `src/p02_mcmc/h0_distancias.py` → `h0_distancias_hglob.json`; DESI sola `h0_four_priors.json` | 2026-09-28 (era 67.7869±0.352, log: git:513e84e:results/logs/mcmc_paper2_reframe.log, con prior número puro ±0.54 y r_d por fórmula; 67.9475 congelaba Ω_m; 66.41 bug 0.160; 67.159 DR1) | <!-- R74: git:509001df85:CANONICAL_VALUES.yaml -->
| ΔBIC MCMC (ΛCDM−SSEE) | **+7.25** (CPL +6.14; ΔAIC +6.48/+3.82; ΔDIC -6.47; Savage-Dickey ln B = 2.34; re-corrido 2026-10-01 sin el término de cúmulos que solo llevaba SSEE — era +6.77) | `ssee_paper2_mcmc.py` → `mcmc_paper2_3models_wmfix.log`; resumen con acta `src/p02_mcmc/resumen_3modelos.py` → `results/logs/resumen_3modelos.json`; DIC `dic_from_chains.json`; SD `savage_cv.json` | 2026-09-30 (re-corrida completa, SSEE incluido; era +6.43/+6.35 del 07-25) <!-- R74: git:d11487679d:CANONICAL_VALUES.yaml -->
| Ω_b h² (posterior MCMC reframe) | **0.02198 ± 0.00048** (≈BBN 0.02218) | `src/p02_mcmc/reframe_obh2.py` lee la cadena de `ssee_paper2_mcmc_reframe.py` (control: mediana H₀ = json) → `results/logs/mcmc_paper2_reframe_obh2.json` | 2026-09-29 (era 0.02207±0.00045 con prior número puro ±0.54) | <!-- R74: git:6fdfa3b03c:CANONICAL_VALUES.yaml -->
| r_d,SSEE (MCMC, ω_m algebraico fijo R25) | 147.71 en la mediana del posterior (ΛCDM 147.59, ratio 1.001); en el punto algebraico 147.17 vs ΛCDM-Planck 147.10 (`rd_dual.json`, `lya_auditoria.json`) | `ssee_paper2_mcmc.py` → `results/logs/mcmc_paper2_3models_wmfix.log` | 2026-09-30 (148.15 con Ω_m congelado; el 175.16 era el bug 0.160 en E(z))
| r_d (CAMB, reframe ω_m-directo @ H_glob=67.962, Ω_m,CMB=0.308881) | 147.17 Mpc — **0.32σ** (ΛCDM-Planck con su mν, mismo código: 147.10) | `run_p3_rd_reframe.py` → `results/logs/p3_rd_reframe_omega_m.log`; ΛCDM `src/ssee_resolution_figures.py` → `rd_dual.json` | 2026-09-29 (re-corrido; sin mapping MIRA; era 146.73@67.037) |
| χ²_r CMB TT (SSEE) | 1.042 | `ssee_paper3_cmb.py` (reframe ω_m-directo @ H=67.962, Σm_ν=0.0685) → `results/logs/paper3_cmb_reframe.log` | 2026-06-19 (era 1.044 @67.04 legacy) |
| ΔBIC CMB diagonal (SSEE−ΛCDM) | −35.0 (SSEE favorecido) | `ssee_paper3_cmb.py` (reframe ω_m-directo @ H=67.962) → `results/logs/p3_pr4_diag_nu_fix.log` | 2026-07-25 (Σm_ν=0.06849 coherente; era −34.9 con 0.0690, −28.0 @67.04 legacy) |
| ΔBIC CMB plik_lite TTTEEE+lowT+lowE (ω_m-directo, k=2) | **−26.03** (χ²=1003.586 vs ΛCDM 1003.596 con SU mν=0.06; N=669 medido; caso k=4 −13.02) | `src/p11_sondas/cmb_dbic_mnu_propia.py` → `results/logs/cmb_dbic_mnu_propia.json` (ΛCDM re-minimizado por `lcdm_conjunta.py cmb`) | 2026-09-29 (era −26.21: ΛCDM con la mν de SSEE. Antes, 2026-09-09 CANÓNICO: {A_s,τ} ajustados y N medido del likelihood). Supersede −24.02 (χ²=1005.41), que clavaba A_s y τ en Planck contándolos como libres y usaba N=613 — con N bien contado habría sido −24.37. Cobaya legacy −32.2 @67.037 superado |
| ΔBIC CMB full plik TTTEEE+lowl+lensing (k=2, H₀ fijo) | **−33.83** — χ² MÍNIMO SSEE 2768.449 vs ΛCDM 2771.227, Δχ² −2.778 (indistinguibles), N=2354, k=2 vs 6; conservador k=4: −18.31. Control (R53): con el mejor muestreado −34.08, mismo signo — PASA. El −32.9 del 23-jun queda retirado: no tenía log (cadenas sobrescritas) | `b1_minimiza.py ssee` y `lcdm` → `b1_min_*.json`; `b1_k2_lee.py` → `results/logs/b1_k2.json` (etapas DVC b1_min_ssee, b1_min_lcdm, b1_k2) | 2026-10-01 (re-corrida k=2, decisión de Mike) |
| θ* (CAMB, en H_glob 67.962, Σm_ν=0.06849) | 0.59667° (100θ*=1.04139) — **1.00σ** | `run_p3_rd_reframe.py` → `results/logs/p3_rd_reframe_omega_m.log` | 2026-09-29 (re-corrido; sin cambio. El log de 07-26 usaba Σm_ν=0.06902 rancio → 0.59668/1.05σ) | <!-- R74: git:d7446ace8a:results/logs/p3_rd_reframe_omega_m.log -->
| θ* (CAMB, en posterior 67.8244, Σm_ν=0.06849) | 0.59645° (100θ*=1.04099) — **0.32σ** (posterior y anchor coinciden; la tensión 6.66σ era el bug del sector 0.160 en E(z), V-L4-DESI) | `run_p3_rd_reframe.py` → `results/logs/p3_rd_reframe_omega_m.log` | 2026-09-29 (era 1.04089/0.68σ en el posterior 67.7869, log: git:513e84e:results/logs/mcmc_paper2_reframe.log; 67.9475/66.41/67.159 superados) | <!-- R74: git:509001df85:CANONICAL_VALUES.yaml -->
| σ₈ / S₈ con A_s FIJADO a Planck — **DIAGNÓSTICO condicionado, NO predicción** | **0.814854 / 0.826827** | `config/class/techo_ssee_canonico.ini` (CLASS v3.3.4, fondo canónico **con Σm_ν=0.06849 eV**); evaluado por `src/p05_IS/techo_sigma8_As_fijo.py`; log `results/logs/p5_techo_sigma8_As_fijo.json` | **2026-09-08 — RETIRA 0.8335 / 0.846.** Aquéllos salían de `can_cold__pk.dat`, un fichero **sin `.ini`**, **fuera del repo** (`class_ssee/output/` está en `.gitignore`) y del mismo minuto que la corrida de dos sectores con la partícula retirada. Le faltaban los **neutrinos masivos** que el fondo canónico sí lleva, y sin ellos sobra grumo a 8 Mpc/h: **+2.3%**. **CONTROL** con criterio escrito ANTES de correr (`config/class/techo_lcdm_referencia.ini`): la línea base de Planck 2018 debe dar σ₈=0.8111±0.006 y da **0.810851**, 0.04σ — **PASA**. Tensiones del S₈: KiDS 3.5σ→**2.74σ** · DES-Y3 3.9σ→**2.82σ** · Planck 1.1σ→**0.36σ**. Coincide con el S₈=0.8256 que Paper 5 saca por su vía independiente. El diagnóstico **no** es el resultado: con A_s libre contra dato crudo, S₈=0.7559 ± 0.0189 (0.10σ, R3). La barra ±0.006 viene de antes y **no** se ha recomputado. Informe: `BANDEJA/2026-09-08_techo_sigma8_neutrinos.md` |
| σ₈ / S₈ (Paper 6, MCMC R3 contra KiDS-1000 CRUDO) — HISTÓRICO, superado por KiDS-Legacy (2026-09-20) | **0.7449 ± 0.0186 / 0.7559 ± 0.0189 — 0.10σ KiDS** | Cobaya+CAMB, 4 cadenas MPI, R−1=0.0189, N_eff=42711 (burn-in por cadena; la lectura vieja 0.7555 cortaba sobre las cadenas pegadas, 2026-10-02); log `results/logs/growth_2026-07/R3_ssee_kids_S8_rehecho.json` | 2026-08-01, releído 2026-10-02 (un sector, A_s libre, fondo fijo por álgebra; χ²_min=265.44/216 dof) |
| **S₈ ΛCDM control metodológico (Paper 6, MCMC R4 contra KiDS CRUDO)** | **0.7571±0.0194 — 0.06σ KiDS** · χ²_min=**262.746**/212 dof | Cobaya+CAMB, 4 cadenas MPI, R−1=0.0256, 13 libres (fondo LIBRE); log `results/logs/growth_2026-07/R4_lcdm_kids_S8.json` | 2026-08-07 (corrida) · 2026-09-07 (χ²_min recuperado de la cadena y escrito al log: Paper 6 ya lo publicaba y el log no lo respaldaba). Licencia la comparación Δχ²=2.69 (265.44−262.75, `kids_publicados.json`; era 2.65 con el χ²_min de R3 tecleado a mano y mal redondeado, 2026-09-30) con Δk=4 de la tabla S₈ |
| **`ω_c` que pide BOSS DR12 (perfil, amplitud propia de cada modelo)** | **SSEE 0.117450±0.004079 → 0.51σ de `KAL₀·ω_b·n_s`** · ΛCDM 0.114346±0.004041 → 1.40σ de Planck 0.1200 | `src/p06_growth/perfil_wc_boss.py` y `perfil_wc_boss_lcdm.py` (minimización robusta `minimo_sesgos.py`); logs `results/logs/perfil_wc_boss.json` + `perfil_wc_boss_lcdm.json` (etapas DVC, P6 por \val) | 2026-10-01 (re-corrido: el minimizador del 09-08 caía en mínimos locales, hasta 26 de χ² arriba; control con 10 arranques al azar PASA en los 4). Con la amplitud del CMB clavada dan 0.109937±0.003994 (2.40σ) y 0.107801±0.003931 (3.10σ): los DOS fondos se desplazan, ΛCDM más ⟹ el desplazamiento es del DATO. Ganancia de soltar `ω_c`: SSEE 1.177, ΛCDM 4.878. El χ² con `ω_c` LIBRE **no se cita** como comparación de modelos. Paper 6 §`par:wc-profile` |
| ~~σ₈/S₈ two-sector 0.747/0.758~~ · ~~m_φ=40.70 eV~~ · ~~k_fs=0.754~~ · ~~α=1.117~~ | **RETIRADOS 2026-08-01** | — | La resta Ω_φDM=0.308881−0.160 mezclaba densidad con ecuación de estado (0.160=1+w₀); histórico, no citar |

**Historial de deriva de H₀ MCMC** (para entender por qué cambió): el MCMC
es determinista (semilla fija 42) — *mismo script → mismo número*. La
deriva corresponde a **ediciones del script / cambios de prior**, no a azar:
- 66.75 ± 0.44 — prior Planck-ΛCDM legacy, 50w×10k.
- 66.533 ± 0.442 — prior MIRA 67.037 self-consistent, 100w×25k. **Superado por el
  reframe ω_m-directo 2026-06-19.**
- 67.159 ± 0.442 — prior H_alg 67.962, 100w×25k, **datos DR1 mal etiquetados. Superado <!-- R74: git:509001df85:CANONICAL_VALUES.yaml -->
  por V-L4-DESI (2026-07-02).** ref `results/logs/mcmc_paper2_reframe.log`.
- 66.412 ± 0.385 — prior H_alg + DESI DR2 REAL pero con **geometría BUGGY**: el sector
  frío Ω_m,dyn=0.160 (=1+w0) metido en E(z)/r_d (debía ser la materia TOTAL 0.308881).
  Daba χ²_BAO=726, Ω_bh² +2.3σ, θ*=13.9σ. **Superado por V-L4-DESI 2026-07-09.**
- **67.8226 ± 0.4126 — (2026-10-01: sin término de cúmulos y con semilla fija en emcee; antes 67.8206 ± 0.4125 (log: git:1de1618:results/logs/mcmc_paper2_reframe.json) y 67.8244 ± 0.4133, ruido MC) prior H_glob 67.962 ± 0.968 + DESI DR2 + ω_m algebraico FIJO (R25) + r_d y
  distancias CAMB (CANÓNICO ACTUAL, 2026-09-28).** `mcmc_paper2_reframe.json`; 0.33σ de H_glob, 0.68σ
  Planck; Ω_bh² 0.02198±0.00048; χ²_BAO 10.43 (11.41 en H_glob).
- 67.7869 ⁺⁰·³⁵¹/₋₀·³⁵² (log: git:513e84e:results/logs/mcmc_paper2_reframe.log) — prior número puro 67.962 ± 0.54 (σ de Planck) + r_d por fórmula
  (superado 2026-09-28). `ssee_paper2_mcmc_reframe.py`, ref `results/logs/mcmc_paper2_reframe.log`.
  N_eff≈78170, acceptance 0.715, cov bloque-diagonal r_MH oficiales. **0.88σ Planck,
  0.04σ H_alg** (el dato DESI DR2 CONFIRMA la predicción algebraica, no la tensa). Ω_bh²
  posterior 0.02207±0.00045 (≈BBN). χ²_BAO~10.3. El "esfuerzo del fondo" (χ²=795, +2.3σ)
  era el bug del sector 0.160 en la geometría; con la total desaparece.

**Anatomía del H₀ (un solo número, dos etapas — ahora COINCIDEN):** el modelo tiene UN H₀.
(1) **Anchor/prior** = H_alg = 67.962 km/s/Mpc: el H₀ que minimiza la
tensión CMB (con ω_b,ω_c fijos por álgebra, plik_lite minimiza ahí —
`results/logs/p3_h0anchor_reframe.log`; superó al viejo H_MIRA 67.037).
(2) **Posterior** = 67.7869 ± 0.351 (log: git:513e84e:results/logs/mcmc_paper2_reframe.log): el mismo H₀ tras dejar que el MCMC ajuste
DESI DR2 BAO encima del prior. Con la geometría total, DESI DR2 lo deja a 0.04σ del
anchor — anchor y posterior COINCIDEN. El "split BAO–CMB" que se veía antes (66.41)
era el bug del sector 0.160 en E(z), no física.

---

# Capa 1 — Axiomas y constantes algebraicas

Verificación numérica: `python3` (2026-05-21). Todas las constantes son
adimensionales → comprobación dimensional trivialmente ✓. Derivación: V-L1-01/02
son axiomas; el resto son definiciones algebraicas de φ y π.

| ID | Constante | Definición | Valor verificado | Rol en el modelo | Estado |
|----|-----------|-----------|------------------|------------------|--------|
| V-L1-01 | φ | (1+√5)/2 | 1.6180339887 | Axioma generador | re-verificado |
| V-L1-02 | π | — | 3.1415926536 | Axioma generador | re-verificado |
| V-L1-03 | Ω | φ+π | 4.7596266423 | Métrica de estabilidad; base de H₀^alg=3Ω² | re-verificado |
| V-L1-04 | β | (φ+π)/2 | 2.3798133212 | Escalar de acoplamiento base | re-verificado |
| V-L1-05 | AURA | (3φ+π)/2 | 3.9978473099 | Acoplamiento EFT βc; genera MIRA | re-verificado |
| V-L1-06 | MIRA | AURA/2 | 1.9989236550 | Razón Ω_m,cosm / Ω_m,dyn | re-verificado |
| V-L1-07 | KAL₀ | (φ+3π)/2 | 5.5214059748 | Retención estructural; fija τ_Π | re-verificado |
| V-L1-08 | T_r | 3(φ+β) | 11.9935419298 | Horizonte de saturación 3D; numerador de w₀ | re-verificado |
| V-L1-09 | K_v | 2(φ+π) | 9.5192532847 | Invariante de restricción estructural | re-verificado |
| V-L1-10 | M_v | φ+π+K_v | 14.2788799270 | Invariante dimensional máximo; denominador de w₀ | re-verificado |

### Conexiones L1 (grafo de dependencias)

- φ, π → todo.
- Ω = φ+π → H₀^alg (L2), K_v.
- β = Ω/2 → T_r, KAL₀ (vía β+π... ver nota).
- AURA → MIRA → Ω_m,cosm (L2), βc (L2/L3).
- T_r, M_v → w₀ (L2).
- KAL₀ → τ_Π, viscosidad IS (L3).

### Notas de verificación L1 (hallazgos)

- **V-L1-07 KAL₀** — definición canónica `(φ+3π)/2`. En varios papers aparece
  también como `β+π`; es equivalente (`β+π = (φ+π)/2+π = (φ+3π)/2`) ✓, pero
  conviene unificar a una sola forma. Comprobación de ubicación: **pendiente de
  barrido cross-paper.**
- **V-L1-09 K_v** — Paper 1 la define con dos formas (`φ+π+Ω` y `2(φ+π)`),
  numéricamente idénticas (Ω=φ+π). Unificar a `2(φ+π)`. Mismo caso M_v
  (`φ+π+K_v` vs `3(φ+π)`). Comprobación de ubicación: **observación abierta.**
- Nomenclatura: AURA, MIRA, KAL₀ se conservan como identificadores físicos
  establecidos. Los nombres mitológicos (BIAL, KRYSTOS, TRIAL, MIKAEL_V, PYROS,
  Ω_DNAV) deben eliminarse — limpieza en curso (Clase A).

**Estado Capa 1:** 10/10 `re-verificado` (confirmado por Mike 2026-05-21;
re-verificado de forma independiente por el guardián `ssee_verify.py`).
Pendiente: barrido de la comprobación 5 (ubicación) en los 11 `.tex`.

---

# Capa 2 — Parámetros cosmológicos derivados

Verificación numérica: `python3` (2026-05-21), todas las identidades recomputadas
desde las constantes de Capa 1. La columna **Dim.** indica si la comprobación
dimensional pasa.

| ID | Parámetro | Definición | Valor verificado | Dim. | Estado |
|----|-----------|-----------|------------------|------|--------|
| V-L2-01 | w₀ | −T_r/M_v | −0.8399497713 | ✓ | verificado |
| V-L2-02 | wₐ | −P_sc/I_g  (P_sc=Ω+φ=6.3776606311, I_g=π+P_sc) | −0.6699748857 | ✓ | verificado (2026-10-02: decía −P_sc/K_v y traía P_sc con un dígito mal) |
| V-L2-03 | s_DE | T_r/M_v (saturación, no densidad) | 0.8399497713 | ✓ | verificado |
| V-L2-04 | s_m | 1+w₀ (saturación, no densidad) | 0.1600502287 | ✓ | verificado |
| V-L2-05 | Ω_m | ω_m/h² (reframe ω_m-directo) | 0.3088808406 | ✓ | verificado (el MIRA·Ω_m,dyn que decía esta fila está RETIRADO desde el 2026-06-18) |
| V-L2-06 | H₀^glob | H_SH0ES(1−f_screen), f_screen IR+UV | 67.9621415220 | ✓ | verificado (SH0ES entra; 3(φ+π)²=67.9621373234 es el blanco; el puente dimensional del número puro sigue **ABIERTO**) |
| V-L2-07 | n_s | 1−φ⁻⁷ | 0.9655581463 | ✓ | verificado |
| V-L2-08 | s_K | 3·s_DE·s_m = −3w₀(1+w₀) | 0.4033024589 | ✓ | verificado — s_K **no** es α_K (R54); la fila decía «αK» |
| V-L2-09 | ~~βc~~ | ~~−AURA~~ | ~~−3.9978473099~~ | — | 🔴 **RETIRADO 2026-09-07**: era el bug de normalización de la saturación; el disparo bien normalizado da +0.235068 (`fondos_exponenciales.json`) |
| V-L2-10 | ~~m_φ~~ | ~~Σm_ν^act·(Ω⁴+AURA·KAL₀)~~ | ~~(su masa)~~ | — | 🔴 **RETIRADO 2026-08-01** con la partícula (su densidad salía de restar 1+w₀, que no es una densidad) |
| V-L2-11 | ~~k_fs~~ | ~~free-streaming de m_φ (output CLASS)~~ | ~~0.754 h/Mpc~~ | — | 🔴 **RETIRADO 2026-08-01, antes de L3** (no «pendiente»: no hay trabajo que hacer, no hay free-streaming que caracterizar) |
| V-L2-12 | r | 12α/N²  (α=φ⁴/3, N=2φ⁷) | 0.00813062 | ✓ | verificado |
| V-L2-13 | f_screen | s_K^full/(3·MIRA), IR+UV | 0.0695216111 | ✓ | verificado (el término IR solo, s_K/(3·MIRA) = (π−φ)/Ω² = 0.0672532703, es el régimen M→∞, no canónico) |

### Cross-checks de identidad (todas pasan)

- **w₀**: dos rutas coinciden — `−T_r/M_v` y `1/(2n−1)` con `n=(T_r−M_v)/(2T_r)`.
- **f_screen**: dos fórmulas coinciden exactamente — `αK/(3·MIRA)` y `(π−φ)/Ω²`.
- **Ω_m,dyn + Ω_DE = 1** ✓; **Ω_m,cosm = MIRA·Ω_m,dyn** ✓.

### Problemas ABIERTOS detectados en Capa 2

- **V-L2-06 H₀^alg = 3Ω²** — numéricamente da 67.962. La lectura ANTERIOR
  ("`3Ω²` es adimensional → unidades por fiat → coincidencia Type-P") queda
  **DISUELTA** por la inversión de Mike: **H_alg es DERIVADO de SH0ES × f_screen.**
  Se toma SH0ES (medido, CON unidades km/s/Mpc: 73.04±1.04, Riess+2022) y se le
  quita el screening: H_global = SH0ES·(1−f_screen) = 73.04·0.93275 = 68.13±0.97,
  y el número puro `3Ω²` = **67.962 coincide a 0.17σ**. Las unidades vienen de la
  MEDICIÓN, el número adimensional del álgebra; es física normal (¿es f_screen
  correcto? ¿precisión?), **no numerología**. (Ver [[project-h-alg-typeP-dissolved]].)
  **Pregunta SEPARADA (CERRADA 2026-06-10):** H_alg NO es la *tasa física del
  fondo a todo z* (la "sábana desnuda"): (1) metido como tasa de expansión real
  en el CMB da θ*=7.80σ, r_d=5.35σ fuera de Planck; (2) límite de Sitter
  H_dS=H_MIRA·√Ω_DE=61.44 < H_MIRA, signo invertido; Friedmann ata H₀ al
  contenido total. Es decir: H_alg es el **anchor GLOBAL de fondo** (H₀ de hoy:
  prior del MCMC, ancla del fit CMB, normalización del background; aplicarle
  f_screen relaciona con el valor LOCAL medido). NO es la tasa dinámica H(z) "bare-sheet" a
  todo z — eso es lo refutado. Las dos lecturas (anchor global derivado por
  de-screening de SH0ES vs. tasa dinámica) conviven sin contradicción. La veta
  abierta restante es el origen dimensional de la escala Mpc↔Planck (roadmap #1),
  no el estatus de coincidencia (ya disuelto).
- **V-L2-10 m_φ = Σm_ν^active · (Ω⁴+AURA·KAL₀)** — forward-prediction canónica:
  `[eV]·(número puro)=[eV]`, dimensionalmente **consistente**. Con
  Σm_ν^active = (Ω/(KAL₀·T_r))·0.960318 eV = 0.069023 eV y multiplicador
  Ω⁴+AURA·KAL₀ = 535.2795 → m_φ = 36.9463 eV (cero fiteo). *(Cadena **RETIRADA**:
  factor 0.960318 ⇒ C_ν≈93.86 SIN FUENTE, y multiplicador viejo. La cadena que la
  sucedió —Σm_ν 0.06849 · SOLAR²·KRYSTOS_V = 40.70 eV— **también está RETIRADA**
  desde el 2026-08-01, con la partícula entera: su densidad salía de restar
  0.308881 − 0.160, y ese 0.160 es 1+w₀, no una densidad. Las dos se conservan
  para trazar el linaje, ninguna está vigente.)* Reemplaza la vieja
  cadena numerológica `Σm_ν·H₀^alg = 5.60 eV` (RETIRADA — sí era `[eV]·[km/s/Mpc]`).
  Lo que queda **ABIERTO** es el Lagrangiano φ-DM que justifique el multiplicador
  (OP-9), no la dimensión.

### Dependencias hacia Capa 3 (derivación — comprobación 3)

Estos parámetros pasan numérica y dimensionalmente, pero su **derivación** se
apoya en mecanismos de Capa 3 aún no verificados — no pueden pasar de
`verificado` a `resuelto` hasta que Capa 3 los sostenga:

- **n_s** (V-L2-07): el exponente 7 depende de OP-2 (N_*=2φ⁷ + α-attractor).
- **βc** (V-L2-09): depende de OP-7 (unicidad EFT; el árbitro lo llamó fit al 0.2 %).
- **αK** (V-L2-08): depende de la acción EFT de P7.
- **r** (V-L2-12): depende de α=φ⁴/3 y N=2φ⁷ (OP-2).
- **f_screen** (V-L2-13): la *identidad algebraica* está verificada, pero el
  *mecanismo* de screening depende de P9 (el árbitro lo llamó circular).
- ~~**k_fs** (V-L2-11)~~: **RETIRADO 2026-08-01** junto con la partícula — no hay free-streaming que caracterizar.

**Estado Capa 2:** 11/13 `verificado` (numérica + dimensional + identidades);
1 `ABIERTO` (H₀^alg — adimensional vs km/s/Mpc); 1 `RETIRADO antes de L3` (k_fs, 2026-08-01).
m_φ pasa a `verificado (dim.)` tras la cadena forward-prediction canónica; su
derivación del multiplicador alcanza la Capa 3 (OP-9). Ninguno pasa a
`resuelto` todavía: la comprobación 3 (derivación) de varios alcanza la Capa 3.

# Capa 3 — Mecanismos y derivaciones

Aquí vive la "nueva física". Cada OP-1..OP-7 está marcada `✅ RESUELTO` en
CLAUDE.md — se re-verifican una por una, paso a paso. Estado por elemento:
`verificado` (la derivación cierra), `ABIERTO` (coincidencia/conjetura vestida
de derivación), o `PARCIAL` (mezcla — partes verificadas, partes abiertas).

## V-L3-OP2 — n_s = 1 − φ⁻⁷ (índice espectral) — **PARCIAL**

*Claim CLAUDE.md:* "✅ RESUELTO — α-attractor universality + N_*=2φ⁷".

Cadena de derivación, paso a paso:

1. **✓** Universalidad α-attractor: `n_s = 1 − 2/N_*` (Kallosh & Linde 2013).
   Física estándar correcta.
2. **⚠ pendiente** `α = φ⁴/3` — insumo de Paper 1, aún sin verificar
   (elemento V-L3-alpha, pendiente en esta misma capa).
3. **✓** Álgebra exacta: con `N_* = 2φ⁷` → `n_s = 1−2/(2φ⁷) = 1−φ⁻⁷`, y
   `r = 12(φ⁴/3)/(2φ⁷)² = φ⁻¹⁰`. Ambas identidades exactas — el guardián
   las recomputa.
4. **✗** `N_* = 2φ⁷` — **NO derivado.** Es la Conjecture B.1. El script
   `ssee_paperB_Nstar.py` es honesto: *invierte* la fórmula para hallar el
   T_rh que da 2φ⁷; la cuasi-coincidencia ρ_end/ρ_rh≈3 necesita un ajuste
   δ~O(1/N) en la constante 58.25 de la fórmula estándar para cerrar; y el
   puente físico (eficiencia de reheating gravitacional con α=φ⁴/3 → ρ_rh=V_end)
   está **ausente**. El argumento alterno "contar 7 constantes SSEE" es
   racionalización post-hoc — el conteo depende de cómo se agrupen.

**Veredicto:** dado N_*=2φ⁷, todo cierra exacto. Pero N_*=2φ⁷ es una conjetura
no probada. OP-2 NO está "RESUELTO": es **condicional a la Conjecture B.1**.

## V-L3-OP7 — βc = −AURA (acoplamiento EFT) — 🔴 **RETIRADO 2026-09-07 (histórico)**

> El «<0.2%» de esta entrada era el **bug de normalización de la saturación**
> (el shooting calibraba Ω_φ(a=1) a 0.839950 en vez de 0.691119). Corregido da
> **−2.194210**, a 45% de −AURA. Y `βc` ya **no está en la acción**: Paper 7 <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
> retiró el acoplamiento conformal y el potencial. La entrada se conserva
> entera para trazar el linaje; nada de lo que sigue está vigente.

*Claim CLAUDE.md:* "PARCIALMENTE RESUELTO — unicidad EFT vía dualidad Z₂".

1. **✓** Extracción numérica: integrar el fondo EFT (P7 §6, shooting con
   Ω_φ(a=1)=Ω_DE) da `βc ≈ −3.990`, sin parámetros libres.
2. **✗** Identificación `βc = −AURA`: −AURA = −3.99785; el valor extraído
   −3.990 está a **0.2 %** (|Δ|/βc = 0.196 %). La ecuación `\boxed{βc=−AURA}`
   de P7 lo presenta como exacto — no lo es. El origen del 0.2 % se atribuye
   a la aproximación de shooting, pero el árbitro halló que el plateau test
   muestra que NO viene de las condiciones iniciales. "Bariones+radiación lo
   llevarían a −AURA dentro de 0.01 %" es una predicción no ejecutada.
3. **✓** Dualidad Z₂: `KAL₀=(φ+3π)/2 ↔ AURA=(3φ+π)/2` bajo φ↔π es una
   identidad algebraica exacta — el guardián la recomputa.
4. **✗** Pero la dualidad **no genera** βc. Es una relación entre dos
   constantes hechas con la misma plantilla, no una simetría de la acción EFT
   (V₀e^{αφ}, K(X) no son φ↔π-invariantes). "βc queda determinado por KAL a
   través de la dualidad" es un overclaim lógico: una coincidencia notacional
   no es una derivación.

**Veredicto:** el resultado numérico βc≈−3.990 es sólido; `βc=−AURA` es una
coincidencia numérica al 0.2 %, no una derivación; la dualidad Z₂ es álgebra
real pero descriptiva, no generativa. **ABIERTO.**

## V-L3-alpha — α = φ⁴/3 (parámetro α-attractor) — **verificado (como consecuencia de axiomas)**

Al verificar de dónde sale α=φ⁴/3 se descubre la lógica real de P1
(§Inflationary Embedding) — y es más honesta de lo que CLAUDE.md sugiere:

1. **P1 declara explícitamente** que `n_s=1−φ⁻⁷` y `r=φ⁻¹⁰` son **AXIOMAS**
   (postulados algebraicos de {φ,π}): *"Neither is derived from the
   α-attractor framework"* (P1 EFT, L498). Son predicciones falsables.
2. **✓** Dados esos dos axiomas: `N = 2/φ⁻⁷ = 2φ⁷`, y
   `α = r·N²/12 = φ⁻¹⁰·(2φ⁷)²/12 = φ⁴/3` — consecuencia algebraica exacta
   (guardián la recomputa). Identidad Fibonacci: φ⁴=3φ+2 ⇒ α=φ+2/3.
3. El resultado genuino: los dos axiomas son **mutuamente consistentes** —
   seleccionan una única geometría α-attractor. Eso es honesto y correcto.

**Hallazgo nuevo — error aritmético en P1 (corregido):** la curvatura de
Kähler. P1 escribía `R = −2/(3α) = −2/φ⁴ = −φ⁻⁴ ≈ −0.146`; el último paso
perdía un factor 2. Correcto: `−2/φ⁴ = −2φ⁻⁴ ≈ −0.292`. Corregido en
`SSEE_EFT_section.tex` (eq:kahler_curvature + tabla). El guardián lo comprueba.

**Contradicción de framing detectada:** P1 dice que n_s es un AXIOMA;
`ssee_op2_spectral_index.py` y CLAUDE.md dicen "exponent 7 → derivado" y
marcan OP-2 "✅ RESUELTO". No pueden ser ambas ciertas. La honesta es la de
P1: n_s y r son postulados. El error está en CLAUDE.md y el script, no en P1.

**Veredicto:** α=φ⁴/3 `verificado` como consecuencia exacta de los axiomas
n_s, r — no es derivación independiente, y P1 nunca afirmó que lo fuera.

## V-L3-OP4 — radio de screening k-mouflage (P8) — **ABIERTO (fórmula rota)**

*Claim CLAUDE.md:* "OP-4 ✅ RESUELTO 2026-05-15 — k-mouflage + αB=αM=0".

`git blame` confirma que la fórmula `r_km³ = M_obj/(4π·M_pl·M²)` (P8
eq:rkm) nació en el commit `295ed6e` ("OP-4 resolved — replace Galileon
Vainshtein with k-mouflage") y pasó 7 auditorías posteriores sin detectarse.

**✗ Comprobación dimensional (falla):** el lado derecho tiene dimensión
`[GeV]/([GeV]·[GeV²]) = GeV⁻²`. Entonces `r_km = (RHS)^{1/3}` tiene dimensión
`GeV^{−2/3}` — **no es una longitud** (una longitud es GeV⁻¹). La fórmula es
dimensionalmente inconsistente. Toda la §4–5 de P8 (Tabla 2, Fig. 2, ejemplo
A1689) descansa sobre ella.

**Forma dimensionalmente correcta:** del propio Lagrangiano de P8
(K(X)=X/KAL+X²/M⁴, cruce X=M⁴/KAL, cierre de gradiente
∇φ=2·KAL·βc·M_pl·∇Φ_N) el cruce da `r_km⁴ ∝ M_obj²/(M_pl²·M⁴)` — raíz
cuarta con escala M_obj², no la raíz cúbica de M_obj¹ del paper.

**Veredicto:** OP-4 NO está resuelto. La "resolución" introdujo un error de
derivación. Requiere re-derivar el radio k-mouflage desde cero y propagar a
P8 §4–5 (tabla, figura, ejemplo A1689). **ABIERTO** — remediación grande,
pendiente de sesión dedicada.

**Cierre 2026-10-03:** no se re-derivó el radio; se **retiró**. P8 reduce la sección a un
párrafo que no cita radio (fórmula, valores, tabla y figura fuera) y dice por qué: sin el
acople βc en la acción de Paper 7 (retirado 2026-09-07) no hay quinta fuerza que apantallar,
y el Sistema Solar y la lente canónica descansan en el acople selectivo y en
α_B=α_M=α_T=0 (μ−1=0), que valen para cualquier M. Ver OPEN_PROBLEMS OP-4. **CERRADO.**

## V-L3-OP1 — Ω_b h² = (π−φ)/(3Ω²) (densidad bariónica) — **ABIERTO (coincidencia escaneada)**

*Claim CLAUDE.md:* "OP-1 PARCIAL — (π−φ)/H₀_SSEE = 0.32σ".

1. **✓ numérico:** (π−φ)/(3Ω²) = 1.52356/67.962 = 0.022418; Planck
   0.02237±0.00015 → tensión **0.32σ**. La identidad pura (número/número)
   es dimensionalmente correcta.
2. **✗ no derivado:** la fórmula sale de un **scan** — `ssee_op1_baryon_density.py`
   Paso 5 prueba 7 expresiones {(π−φ)/(3Ω²), 3(π−φ)/200, (π−φ)/φ¹¹, …} y
   elige la de menor tensión. Eso es ajuste a un objetivo conocido.
3. **✗ interpretación rota:** el script reescribe (π−φ)/(3Ω²) como
   "(π−φ)/H₀_SSEE" — pero con H₀ en km/s/Mpc eso tiene unidades, no es
   adimensional. La "derivación desde la tasa de esfalerón" se difiere a
   Paper B/C.

**Veredicto:** una coincidencia numérica decente (0.32σ) hallada por scan,
no una derivación. **ABIERTO.**

## V-L3-OP3 — separabilidad UV-IR / KALeff = φ²√(5/2) — **ABIERTO (cota asertada, dimensión confusa)**

*Claim CLAUDE.md:* "OP-3 RESUELTO — jerarquía EFT (H₀/M)²≈10⁻⁶²".

1. **✓** La jerarquía es real: (H₀/M)² ≈ 2.3×10⁻⁶² (M=9.68 meV ≫ H₀).
2. **✗** Que esa jerarquía *pruebe* la separabilidad (Postulate C.1 →
   Theorem C.1) es una **aserción**: `ssee_op3_separability.py` (L176–179)
   admite que el jacobiano ∂φ/∂χ que mide el mezclado real se difiere a
   Paper B. "RESUELTO (cota EFT)" asevera la cota y aplaza el cálculo.
3. **✗ dimensión confusa:** KALeff² = M⁴/(6α). Con M⁴=5φ⁸ρ_crit y 6α=2φ⁴
   da KALeff² = (5/2)φ⁴·ρ_crit — el script escribe "5φ⁴/2", **dropeando
   ρ_crit**. KALeff resulta dimensional (∝GeV²) pero se factoriza
   `KAL₀=KALeff·F` contra KAL₀=(φ+3π)/2, que es adimensional.
4. El script contiene una auto-corrección sin resolver
   (√(6α)=φ² → "corrección: =φ²√2") — la derivación no está limpia.

**Veredicto:** la jerarquía (H₀/M)²~10⁻⁶² es un hecho; la "prueba" de
separabilidad no lo es (jacobiano diferido), y KALeff arrastra un ρ_crit
dropeado. OP-3 NO está "RESUELTO". **ABIERTO.**

## V-L3-OP5 — tensión S₈ weak-lensing / HMcode bariónico — **ABIERTO (anclado en rama secundaria)**

*Claim CLAUDE.md (canónico 2026-06-19, RETIRADO 2026-08-01):* titular two-sector S₈_eff=0.758 (0.04σ KiDS). Canónico vigente: un sector, A_s libre, S₈=0.7559 ± 0.0189 (0.10σ).

1. **✓ definición:** S₈ = σ₈(Ω_m/0.3)^½ con Ω_m,CMB=0.308881 (√(Ω_m/0.3)=1.0147).
2. **✓ single-sector, A_s FIJO:** σ₈=0.814854 → S₈=0.826827 — **2.74σ KiDS**.
   *(Actualizado 2026-09-08: era 0.8335 → 0.846 → 3.5σ. Aquella corrida de CLASS
   no llevaba neutrinos masivos; con ellos sobra un 2.3% menos de grumo. Y NO es
   un baseline que el modelo deba resolver: el 2.74σ es artefacto de fijar A_s.)*
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7559 ± 0.0189` (0.10σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.04σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
3. ~~**✓ two-sector φ-DM (TITULAR, forward):** el free-streaming en k_fs=0.754
   h/Mpc (de m_φ=40.70 eV SOLAR²·KRYSTOS, cero fiteo) baja σ₈_eff a 0.7470 → **S₈_eff=0.758
   = 0.04σ KiDS-1000**. RESUELVE la tensión S₈, sin parámetros libres.~~
   **RETIRADO 2026-08-01** — y la tensión que resolvía tampoco existía.
4. **○ refinamiento no-lineal (Nivel 2, diferido):** el cierre no-lineal pleno
   con feedback bariónico (N-body SSEE, ~5k–20k CPU-h) queda pendiente; HMcode-2020
   da una corrección ~0.4% (B_σ₈≈0.996). No altera el resultado lineal forward.

**Veredicto (reescrito 2026-09-19).** ~~La tensión S₈ la resuelve el two-sector
lineal forward (0.766, 0.01σ).~~ **RETIRADO**: no hay tensión que resolver. El
«3.5σ» se medía con A_s FIJADO a Planck —o sea importando la discrepancia
Planck–cizalla— y contra el estadístico comprimido S₈, cuya reducción asume ΛCDM.
Contra el dato **crudo** de KiDS-1000 con un solo sector y A_s libre:
**S₈ = 0.7559 ± 0.0189 → 0.10σ** (MCMC R3), con control ΛCDM sobre el mismo dato
en 0.7571 ± 0.0194. Las ramas viejas σ₈=0.737/0.794 → S₈=0.761/0.820 (HMcode,
internamente inconsistentes) y 0.702/0.725 (G=0.866, Ω_m,dyn) siguen **retiradas**.
Queda ABIERTO sólo el refinamiento no-lineal Nivel 2 (ficha OP-5b).

*(Este veredicto llevaba el 0.766 —patrón retirado— bajo un cartel que ya decía
RETIRADO. Lo encontró una auditoría externa el 2026-09-19: el cartel de arriba no
alcanza al párrafo de abajo, que es el mismo defecto del vecino que exonera.)*

## V-L3-OP6 — forma de screening f_screen / universo separado — **PARCIAL (forma derivada, valor con insumo)**

*Claim CLAUDE.md:* "OP-6 ✅ RESUELTO — universo separado k-essence + identidad 1+w₀=Ω_m".

1. **✓ valor:** f_screen = α_K/(3·MIRA) = (π−φ)/Ω² = 0.067253 — álgebra
   exacta, ya verificada en V-L2-13 y en la identidad cruzada de Capa 2.
   **Canónico (reframe ω_m-directo, espeja Paper 9):**
   **Dirección canónica (2026-09-06): SH0ES ENTRA, H_global SALE.**
   H₀,glob = H₀^SH0ES·(1−f_screen) = 73.04×0.93275 = **68.13 km/s/Mpc**,
   a 0.17σ del NÚMERO PURO 3(φ+π)²=67.96214. La escritura anterior
   67.962/(1−f)=72.86 metía un número sin unidades como entrada de una
   cascada dimensional: mismo enunciado leído al revés (los σ son
   invariantes bajo la inversión porque la lente es multiplicativa), pero
   con la carga de prueba invertida. Control del otro lado: la misma lente
   sobre el TRGB adoptado por CCHP (arXiv:2408.06153v3, 70.39±1.94) da 65.66
   en IR (−1.28σ) y 65.50 completo (−1.37σ) — `results/logs/p9_cascada_control.json`
   (2026-10-03). El viejo «69.96 → 65.26, 1.88σ» usaba la v1 de ese artículo,
   superada por la v3. Las rutas H₀^MIRA
   (71.87/72.05) quedan **superadas** por partida doble.
   H_alg es un anchor **DERIVADO** (de-screened SH0ES × f_screen; el cargo Type-P
   quedó disuelto, ver V-L2-06 arriba), no una coincidencia.
2. **✓ forma:** que la corrección sea **multiplicativa** sí sigue de la
   aproximación de universo separado para k-essence (Wands 2000; Brax &
   Valageas 2014) — ese paso es una derivación legítima.
3. **✗ paso δρ_φ afirmado sin derivar:** `ssee_op6_screening_form.py` (L68) escribe
   δρ_φ/ρ_crit = (α_K/3)(Ω_m,dyn/MIRA)δ_local/(1+w₀) sin derivarla; el
   factor 1/MIRA se justifica con un argumento de plausibilidad, no un
   cálculo. El c²_s aparece y desaparece entre L65 y L73.
4. **✗ insumo δ_local=2:** el valor f_screen=α_K/(3·MIRA) exige fijar
   δ_local=2 (sobredensidad del Grupo Local) para cancelar el δ_local/2.
   Es un insumo astrofísico razonable, **no derivado de φ,π**.

**Veredicto:** la forma multiplicativa está derivada; el valor f_screen es
álgebra exacta *condicionada* a δ_local=2 y a una expresión δρ_φ asertada.
No es "RESUELTO" pleno. **PARCIAL.**

## V-L3-mphi — masa del campo φ-DM — 🔴 **RETIRADO 2026-08-01 (histórico)**

> **La partícula no existe.** Esta entrada se conserva como registro de cómo se
> llegó a retirarla, NO como verificación viva. La cadena dimensional era
> correcta (masa × número adimensional cierra unidades) — lo que falla es que
> su densidad Ω_φDM salía de restar 0.308881 − 0.160, y ese 0.160 es 1+w₀, un
> número de la ecuación de estado, no una densidad. **Lección:** verificar
> unidades no sustituye verificar que cada término sea la clase de cosa que
> dice ser. Todo lo que sigue en esta sección es histórico.

*Claim CLAUDE.md (canónico 2026-06-04):* "m_φ = Σm_ν^active × (Ω⁴+AURA·KAL₀)
= 40.70 eV — forward-prediction, cero fiteo".

1. **✓ numérico:** *(cadena **RETIRADA** — registro histórico del multiplicador
   viejo Ω⁴+AURA·KAL₀ y del factor 0.960318 (C_ν≈93.86, sin fuente); superada por SOLAR²·KRYSTOS_V con
   C_ν=93.14 PDG → Σm_ν=0.06849 eV, m_φ=40.70 eV. Conservada para trazar el linaje.)*
   Σm_ν^active = (Ω/(KAL₀·T_r))·0.960318 eV
   = 0.071875·0.960318 = 0.069023 eV (valor **anterior**, C_ν viejo); multiplicador
   Ω⁴+AURA·KAL₀ = 535.2795; m_φ = 0.069023·535.2795 = 36.9463 eV.
2. **✓ dimensional:** `[eV]·(número puro)=[eV]`. El multiplicador es
   combinación de constantes adimensionales (Ω, AURA, KAL₀). Reemplaza la vieja
   cadena `Σm_ν·H₀^alg` (RETIRADA — esa sí era `[eV]·[km/s/Mpc]`).
3. **✓ cero entero pelado:** la razón Σm_ν usa R₂=Ω/(KAL₀·T_r), cociente puro
   de constantes — ya no la resta `4·KAL₀−22` de la versión numerológica.
4. **✗ Lagrangiano no cerrado:** falta la acción P(X,φ) que produzca el
   multiplicador Ω⁴+AURA·KAL₀ desde primeros principios. Es forward-prediction
   estructural, no derivación de mecanismo (**OP-9 ABIERTO**).

**Veredicto:** la cadena es dimensionalmente consistente y sin fiteo (cero
parámetros libres), pero su justificación desde un Lagrangiano sigue abierta
(OP-9). **PARCIAL** (era ABIERTO bajo la cadena 5.60 eV retirada).

## V-L3-2sec — modelo dos sectores φ-DM — 🔴 **RETIRADO 2026-08-01 (histórico)**

> Era «PARCIAL (identidad sí, split físico no)», y el split físico resultó no
> existir: Ω_φDM salía de restar Ω_m,CMB − Ω_m,dyn = 0.308881 − 0.160, y ese
> 0.160 es **1+w₀**, un número de la ecuación de estado, no una densidad. La
> entrada se conserva entera para trazar el linaje; nada de lo que sigue está
> vigente.

*Claim CLAUDE.md:* "Ω_total (dos sectores) = 0.308881 ≈ Ω_m,CMB — unificación algebraica".

1. **✓ identidad:** Ω_CDM + Ω_φDM = Ω_m,dyn + (MIRA−1)·Ω_m,dyn =
   MIRA·Ω_m,dyn = 0.308881. Diferencia con V-L2-05 = 0 exacto. Es una
   **re-partición algebraica** de Ω_m,cosm en dos mitades casi iguales.
2. **🔴 split físico: RETIRADO 2026-08-01 (histórico).** El split descansaba en
   m_φ y k_fs, ambos retirados con la partícula. Y la re-partición del punto 1
   es exactamente el problema: restar 0.308881 − 0.160 mezcla una densidad con
   un número de la ecuación de estado. No hay dos sectores.

**Veredicto:** la suma Ω_total es un re-enunciado exacto de V-L2-05; el
modelo físico de dos sectores hereda la apertura del Lagrangiano de m_φ
(OP-9). **PARCIAL.**

## V-L3-EFT — acción EFT canónica (Paper 7) — **PARCIAL (parámetros sí, M⁴ inconsistente)**

*Claim CLAUDE.md:* "Paper 7: EFT canónico — λ/V₀/M/g² bloqueados".

1. **✓ λ, α_pot, V₀:** son consecuencias algebraicas exactas de constantes
   ya verificadas — λ²=3·Ω_m,dyn (λ=0.6929), α_pot=λ/√KAL₀ (=0.2949), <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
   V₀=Ω_DE·ρ_crit (=0.8400). No son parámetros libres: re-enuncian
   Ω_m,dyn (V-L2-04), KAL₀ (V-L1-07) y Ω_DE (V-L2-03).
2. **✗ M⁴ inconsistente entre papers:** `archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/ssee_eft_verification.py` (L70, RETIRADO 2026-09-07)
   fija **M⁴ = ρ_crit = 1**; `ssee_paper10_verification.py` (L30) fija
   **M⁴ = 5φ⁸·ρ_crit = 234.9**. Factor ~235 de diferencia en el mismo
   término X²/M⁴ del mismo Lagrangiano K(X). Con M⁴=1 el término UV no es
   perturbativo; con M⁴=234.9 sí. Es una incoherencia cruzada P7↔P10.

**Veredicto:** los parámetros λ, α_pot, V₀ están algebraicamente fijados;
M⁴ tiene dos valores incompatibles según el paper. **PARCIAL.**

## V-L3-KX — completación UV K(X) (Paper 10) — **ABIERTO (M⁴=5φ⁸ subdeterminado; anchor-free, NO calibrado a SH0ES)**

*Claim CLAUDE.md:* "Paper 10: M⁴=5φ⁸ρ_crit exacto; H₀^UV: la cascada devuelve 67.96214 desde SH0ES (residuo +4.2e-06); condicional C.1. Viejo 72.05 vía MIRA=67.037/0.96σ superado".

1. **✓ identidad 45α² = 5φ⁸:** exacta a precisión de máquina (α=φ⁴/3 →
   45α²=45φ⁸/9=5φ⁸=234.89). El *valor numérico* de M⁴/ρ_crit cierra.
2. **f_screen es anchor-free (probado 2026-06-23):** αK, f_screen y la cascada
   H₀ NO usan SH0ES como input — SH0ES entra solo como *objetivo de comparación*.
   f_screen_UV=0.06952 es idéntico para cualquier H de entrada (67.962/67.36/73.04/100).
   Por tanto M⁴ **NO está calibrado a SH0ES**: la caracterización vieja del LEDGER
   (que citaba un VERDICT obsoleto del script, hoy inexistente) era incorrecta.
   El script actual dice *"CONDITIONAL on Postulate C.1"* y *"PENDING first-principles
   derivation of M⁴=45α² without using SH0ES as input"* (que ya no se usa).
3. **near-derivación estructural (2026-06-23):** la redefinición de campo del
   α-attractor (|df/dχ|²=9/16 en tanh=½, medio-polo) reproduce M⁴=5φ⁸ vía
   (10φ⁴)/(φ+3π)²=0.562 a **0.076%** — origen estructural, NO ajuste a objetivo.
   El residuo 0.076% es la huella de π (Lindemann: π trascendente ≠ racional;
   no puede ser identidad exacta). Ver [[project_m4_field_redefinition]].
4. **subdeterminación honesta (lo que sigue ABIERTO):** la normalización exacta
   no está cerrada — Ruta A (K(X) Taylor) da M⁴=6αKAL²≈418 ≠ 234.9; la redefinición
   de campo da 5φ⁸ a 0.076% pero no exacto. s_K_full=0.41691 y H₀^glob,UV=67.96214 son
   aguas abajo de este M⁴ **subdeterminado** (no circular, sí incompleto).

**Veredicto:** la forma 5φ⁸=45α² es exacta en álgebra y tiene near-derivación
estructural (field-redef, 0.076%); la cascada H₀ es **anchor-free** (no usa SH0ES).
Lo ABIERTO no es circularidad sino la *selección* única de 45α² entre rutas
(A≈418 vs field-redef 5φ⁸). **ABIERTO (subdeterminado, no calibrado).**

## V-L3-IS — perturbaciones Israel-Stewart (Paper 5) — **PARCIAL (c²_s,eff=0 sí, mecanismo afirmado sin derivar)**

*Claim CLAUDE.md:* "Paper 5: c²_s,eff = 0 (exacto algebraico) — todos los modos estables".

1. **✓ c²_s,eff = 0:** la corrección IS es ζ̃/τ_Π = (KAL₀/3)/(KAL₀/(3Ω_DE))
   = Ω_DE, y c²_s,eff = w₀ + Ω_DE = −0.8399 + 0.8399 = 0. Cierra exacto.
2. **✗ el mecanismo IS no hace trabajo:** el factor KAL₀/3 **se cancela**
   — ζ̃=KAL₀/3 y τ_Π=KAL₀/(3Ω_DE) comparten KAL₀/3, así que ζ̃/τ_Π=Ω_DE
   para *cualquier* ζ̃. El resultado se reduce a la identidad ya verificada
   w₀ = −Ω_DE (V-L2-01/03). La hipótesis ζ̃=KAL₀/3 es decorativa; la
   derivación de τ_Π (estado estacionario IS) está **asertada, no mostrada**
   en el script. Si τ_Π se deriva de verdad independientemente, el resultado
   es no-trivial; tal como está, es la tautología w₀+|w₀|=0.
3. **✓ Q2 — REENCUADRADO 2026-09-26:** el test daba
   R = Ω_m,eff/Ω_m = 0.9897 ± 0.0167 (k≥10) vs el blanco 1.999, y de ahí
   concluía «discrepancia del 50%». Pero ese blanco era el factor materia
   Ω_m,CMB = MIRA×Ω_m,dyn = 0.3199, **retirado el 2026-06-18** al cerrarse
   OP-8: ya no hay factor de dos que derivar, así que una discrepancia contra
   él no es un resultado. Lo que el número mide sí lo es, enunciado como
   **cota**: |r| = |δ_DE/δ_m| ≤ 0.0175 en k≥10 H₀/c, cayendo a 2e-5 en k=100
   — a lo sumo el 3.9% del r*=0.4464 que una duplicación habría exigido. La
   energía oscura de este modelo NO se agrupa donde opera la supresión IS, y
   medir δ_DE/δ_m por encima del 1% a z=0 y k≳10 lo falsaría.
   La tabla del paper llevaba además Ω_m,eff≈0.15, del run viejo con
   Ω_m=0.160050; el script ya se había corregido a 0.308881 el 2026-09-05 y
   nadie rehízo la tabla, porque el script no dejaba log. Ahora lo deja:
   `results/logs/p5_IS_perturbations_Q2.json`.
   MIRA sigue viva como entidad de apantallamiento en Paper 9; nada de esto
   la toca.

**Veredicto:** c²_s,eff=0 es cierto pero se reduce a w₀=−Ω_DE; el aparato
IS (ζ̃, τ_Π) está construido para reproducir esa identidad y su parte
no-trivial (derivación de τ_Π) no se muestra. **PARCIAL.**

## V-L3-cs2 — extracción del T_μν efectivo del sector k-essence — **ABIERTO (resultado clave)**

*Origen:* el autor pidió extraer el tensor de energía efectivo de la
acción para ver si el sector geométrico puede ser la materia que el CMB
exige (la «0.320»). Extracción hecha 2026-05-22.

**La extracción (k-essence estándar, Garriga–Mukhanov 1999).** Para la
acción de SSEE P(X,φ) = X/KAL₀ + X²/M⁴ − V(φ):
- ρ_φ = 2X·P_X − P = X/KAL₀ + 3X²/M⁴ + V
- p_φ = P = X/KAL₀ + X²/M⁴ − V
- w_φ = p_φ/ρ_φ
- **c_s² = P_X/(P_X + 2X·P_XX) = (A + 2BX)/(A + 6BX)**, con A=1/KAL₀>0,
  B=1/M⁴>0.

**Resultado clave (exacto, analítico, parámetro-independiente).** c_s² es
monótona decreciente en X: vale 1 en X=0, tiende a 1/3 en X→∞. Por tanto
**c_s² ∈ [1/3, 1] para todo X≥0, cualquier M⁴>0, cualquier KAL₀>0.**
Depende solo de la *forma* K = A·X + B·X² (suma de coeficientes
positivos), no de los valores. La inconsistencia M⁴ P7↔P10 no lo afecta.

**Qué significa — respuesta a «¿la geometría tiene peso?».**
- **Peso de fondo: SÍ.** El sector tiene una densidad ρ_φ genuina; su
  w_φ de fondo puede transitar (kinético→potencial).
- **Peso de agrupamiento: NO.** Un fluido se agrupa como materia fría
  solo si c_s² ≈ 0. La k-essence de SSEE **nunca baja de 1/3** — se
  difumina, no forma pozos de potencial. No puede agruparse como CDM.

**Veredicto.** El CMB necesita materia que se *agrupe* (que forme los
pozos donde oscila el fluido fotón-barión). El sector k-essence de SSEE,
tal como está la acción, **no puede hacerlo** — su c_s² es estructuralmente
demasiado alto. **El mecanismo MIRA no está en la acción vigente.** Es un
resultado negativo limpio: descarta «la k-essence es la materia geométrica»
y dice qué hay que buscar — un sector cuyo c_s² pueda anularse a alto z
(la viscosidad IS pretendía eso, pero V-L3-IS la halló decorativa).
**ABIERTO.**

## V-L3-disf — mecanismo disformal de Paper 8 (Ruta B) — **ABIERTO (inconsistencia interna P1↔P8)**

*Origen:* tras el resultado negativo de V-L3-cs2 (la k-essence no se
agrupa), se exploró la «Ruta B»: que el 0.320 no sea sustancia sino
gravedad amplificada. Paper 8 ya invoca «MIRA emergence» vía geodésicas
disformales — se auditó si ese mecanismo deriva MIRA sin materia oscura.
Auditoría hecha 2026-05-22.

**Lo que dice Paper 8.** La acción (P8 eq.1) es
S = ∫√−g[M_pl²R/2 + P(X,φ)] + **S_DM[g̃_μν; ψ_DM]** + S_b[g_μν; ψ_b].
Contiene un **campo de materia oscura ψ_DM** acoplado a la métrica
disformal g̃_μν = g_μν + (2/M⁴)∂_μφ∂_νφ. Todo el mecanismo se sostiene
en ρ_DM: la ecuación del escalar (1/KAL)∇²φ = (β_c/M_pl)·ρ_DM (P8 L221),
el «régimen dominado por materia oscura» (L238), «la fuerza sobre una
partícula de materia oscura» (L271).

**La contradicción.** Paper 1 L51: el modelo se construye «without
introducing free parameters or exotic dark-matter particles». Paper 1
L278: SSEE «is refuted by direct detection of a collisionless
dark-matter particle». **Paper 8 presupone exactamente lo que Paper 1
declara falsador.** No es una extensión — es una violación del postulado
fundacional.

**Además, MIRA no «emerge».** El propio Paper 8 (L69) admite que
√β_c/MIRA = 1.00027 (√AURA/MIRA, `cajones_algebra.json`; la cita vieja traía el último dígito mal) es «a near-coincidence, **not an algebraic
identity**». La «emergencia» de MIRA en el lensing es una coincidencia
numérica al 0.03 %, no una derivación.

**Veredicto.** La Ruta B tal como está escrita en Paper 8 **no deriva
MIRA sin materia oscura** — la introduce. Con V-L3-cs2 (sustancia que se
agrupa: descartada) y α_B=α_M=0 de Paper 7 (Poisson modificada μ>1:
imposible, μ=1 exacto), **los tres mecanismos posibles para el 0.320 en
un marco sin materia oscura fallan.** El 0.320/MIRA no está derivado en
ninguno de los 10 papers.

**Lo rescatable.** La ecuación (1/KAL)∇²φ = (β_c/M_pl)·ρ, con ρ → materia
bariónica + dinámica real (0.160) en vez de ρ_DM, sería un modified
gravity genuino sin materia oscura: el campo geométrico φ desarrolla
perfiles alrededor de materia ordinaria y amplifica su gravedad. Pero
(a) Paper 8 da G_eff/G ≈ 177 en cúmulos, no ≈2=MIRA en el fondo
cosmológico — régimen distinto, sin verificar; (b) amplificar el
agrupamiento no mueve las posiciones de los picos del CMB, fijadas por
r_d/D_A del fondo. Rescate posible en principio, no hecho. **ABIERTO.**

**Bloquea:** sellado de Paper 8 (inconsistencia con Paper 1); y deja a
P3/P6/P9 sin un mecanismo válido para el 0.320.

## V-L3-mira — test del mecanismo de retención conformal para MIRA — **ABIERTO (mecanismo candidato FALLA)**

*Origen:* tras V-L3-cs2 y V-L3-disf se construyó y probó la «Ruta B» en su
forma más concreta — MIRA como retención de energía vía un acoplamiento
conformal de quintaesencia entre φ y la materia real (el L_int de Paper 7
re-apuntado de materia oscura a materia real, como exige Paper 1).
Cálculo: `archive/codigo/investigacion/mira_attempts/ssee_mira_mechanism.py`, 2026-05-22.

**El mecanismo (física estándar, quintaesencia acoplada Amendola 2000).**
Un acoplamiento conformal da, en el fondo:
- ρ_m = ρ_m,0 a⁻³·exp[−β_c(φ−φ_0)]  ⟹  R(a) = exp[−β_c·Δφ(a)]
- KG con fuente: (P_X+2X P_XX)φ̈ + 3H P_X φ̇ + V_φ = β_c ρ_m
- Tasa de retención Γ = |β_c φ̇|; desacople en Γ = H.
Para R_temprano = MIRA se requiere AURA·Δφ_total = ln(MIRA) = 0.693, i.e.
una excursión del campo Δφ ≈ 0.173 M_pl.

**El test (β_c = −AURA fijo, sin ajustar nada).** Integración del fondo
acoplado Friedmann+KG hacia atrás desde hoy hasta z=1100:

| | Necesario | Obtenido |
|---|---|---|
| R(hoy) | 1 | 1.00000 ✓ (maquinaria OK) |
| R(z=1100) | MIRA ≈ 1.999 | ≈ 0 ✗ |
| AURA·Δφ_total | +0.693 | **−12.3** ✗ |
| signo | R>1 (carga materia) | R<1 (drena materia) ✗ |
| timing | retención activa temprano | activa tarde (Γ/H≈3 hoy) ✗ |

**Veredicto — negativo limpio.** β_c = AURA ≈ 4 es un acoplamiento
cosmológico enorme (los límites realistas de quintaesencia acoplada dan
β ≲ 0.1; AURA es ~40× ese techo). Con esa fuerza el término β_c ρ_m de la
KG **golpea el campo** y lo hace rodar Δφ ≈ −3.1 (×18 lo necesario) con
signo invertido: en vez de cargar el sector materia lo **drena** —
R(z=2) ≈ 0.016, la materia casi desaparece. Además la KG empuja la
k-essence a un régimen sin solución real de Friedmann en el 44 % de la
trayectoria. Tres fallas independientes (magnitud, signo, timing) ⟹ no es
«casi» — es el mecanismo equivocado.

**Estado del problema MIRA.** Cuatro mecanismos probados para el «0.320»,
cuatro negativos: sustancia que se agrupa (V-L3-cs2), Poisson modificada
μ>1 (α_B=α_M=0, Paper 7), disformal (V-L3-disf, exige ψ_DM), y retención
conformal (esta entrada). **MIRA no tiene derivación en el marco vigente
de SSEE por ninguno de los cuatro mecanismos naturales.** El «0.320» de
P3/P6/P8/P9 está insertado, no derivado. El núcleo w₀wₐ (DESI 0.5σ) no se
ve afectado. Ver [[feedback-impact-analysis]] y V-L3-2Om. **ABIERTO.**

## V-L3-saturacion — α por saturación φ-MDE (veta-2, Amendola-rescaled) — **PARCIAL: álgebra OK, dinámica FALLA**

*Origen:* tras V-L3-mira (β_c=−AURA falla con tres modos independientes), se
abrió la búsqueda de un **principio físico** que fije α en el L_int conformal
sin recurrir a fits ni a numerología. Hipótesis: α toma el valor *saturado*
de una desigualdad física estándar (veta-2 del programa de reconstrucción).
Cálculo: `archive/codigo/investigacion/mira_attempts/ssee_alpha_saturation_stepD2.py`, 2026-05-22.

**La desigualdad física (Amendola 2000, canonical).** En quintaesencia
acoplada con K=X y conformal coupling, el φ-MDE (fixed-point y=0 durante era
de materia) está en x = −α√6/3 y tiene Ω_φ = 2α²/3. La condición Ω_φ ≤ 1
(la era de materia debe existir, *the universe must pass through matter
domination*) impone:

> α² ≤ 3/2 → α_sat,canonical = √(3/2) ≈ 1.2247

**Traducción a SSEE.** Con K(X) = X/KAL + X²/M⁴, en el límite σ→0 (régimen
X/KAL dominante, baja energía / σ = H²M_pl²/M⁴ ≪ 1), la renormalización
natural del campo χ = φ/√KAL traduce la cota canónica a:

> **α_sat = √(3/(2·KAL₀)) = √(3/(φ+3π)) ≈ 0.5212**

Equivalente: **α² · 2·KAL₀ = 3**, o (α·√KAL₀)² = 3/2. Identidad estructural,
no fit.

**Verificación numérica.**

| | Esperado (analítico) | Obtenido (numérico) | Desvío |
|---|---|---|---|
| α_sat canónico (σ=0, KAL=1) | √(3/2) = 1.22474487 | 1.22474487 | 1.4·10⁻⁷ % |
| x_φMDE canónico (α=1.2) | −α√6/3 = −0.97980 | −0.97980 | exacto |
| α_sat SSEE (σ→0, KAL=KAL₀) | √(3/(φ+3π)) = 0.521220 | *sin log* (ningún script archivado lo reproduce) | — |

**Las 6 comprobaciones:**

1. **Numérica:** OK, 0.10 % de error al límite σ→0 (la diferencia es
   suppresión por σ finito; en σ=10⁻⁹ ya converge).
2. **Dimensional:** α adimensional (sale en exp(α·φ/M_pl)); 2·KAL₀ adimensional;
   √(3/(2·KAL₀)) adimensional. OK.
3. **Derivación:** Amendola 2000 (literatura física estándar, no ad-hoc),
   aplicado a K(X) de Paper 7 con normalización canónica del campo.
   *No es post-hoc, no es fit.*
4. **Rol:** fija el coeficiente del L_int conformal en el sector φ-materia.
   *Candidato* para mecanismo MIRA — pendiente test dinámico.
5. **Ubicación:** *no aplicado todavía* en ningún paper. Esta entrada lo registra
   como candidato derivado, no como resultado de un paper.
6. **Conexiones:** depende de KAL₀ (V-L1) y de la estructura k-essence de Paper 7.
   Sería insumo de V-L3-mira si reemplaza a β_c=−AURA.

**Test dinámico (2026-05-22).** `archive/codigo/investigacion/mira_attempts/ssee_mira_saturated_diagnostic.py`:
matriz 2×2 con β_c = ±α_sat y u₀ = ±|u_w₀|, integrando hacia atrás desde el
estado de hoy (fijado por w_φ(hoy)=w₀=−0.840) hasta z=1100, régimen lineal
puro K=X/KAL₀ (donde la derivación aplica):

| β_c | u₀ signo | resultado |
|---|---|---|
| +α_sat | + | integración rompe ~z<1 (runaway u) |
| +α_sat | − | rompe |
| −α_sat | + | rompe |
| −α_sat | − | rompe |

Las cuatro fallan. **No existe trayectoria suave** desde el atractor tardío
(estado de hoy, u₀≈+1.5) hasta el φ-MDE (u≈−2α_sat≈−1.04) con esta familia
de modelos y esta normalización. Cualquier signo se vuelve runaway antes de
cruzar la transición de régimen.

**Interpretación física.** La cota Amendola garantiza que el φ-MDE *exista*
como FP cuando α² < 3/(2KAL₀), pero **no garantiza** que la trayectoria
backward desde el atractor tardío de DE alcance ese FP suavemente. Son dos
preguntas distintas: (a) ¿hay FP físico? — sí. (b) ¿el atractor tardío
desciende a él? — no, al menos no con la α y la inicialización canónicas
del modelo. La veta-2 produjo un número honesto, pero la dinámica acoplada
en SSEE no lo aprovecha.

**Lo que sí queda como producto positivo:**

- **Primer número derivado por saturación** en SSEE: α_sat=√(3/(φ+3π))
  cumple las 6 comprobaciones de la entrada y no es numerología.
- **Confirmación estructural:** Amendola 2000 generaliza limpiamente a
  SSEE bajo la normalización inducida por KAL₀ — el método funciona, lo
  que falla es la aplicación al mecanismo MIRA específico.
- **Evidencia adicional** para V-L3-2Om: ni el coupling AURA-grande
  (V-L3-mira) ni la cota Amendola-saturada conectan el background tardío
  con z=1100. Quinto mecanismo descartado para MIRA.

**Estado.** Álgebra **verificada**. Dinámica acoplada **falla** numéricamente
en las cuatro variantes de signo — el bound es real pero no derivado en una
forma constructiva del mecanismo MIRA. **PARCIAL.**

### Extensión #6+#7 (2026-05-22) — derivativo + forward desde φ-MDE

Tras V-L3-saturacion, se cazaron dos mecanismos adicionales:

**Mecanismo #6 — acoplamiento derivativo** `L_int=(X/M⁴)·L_DM`.
Script `archive/codigo/investigacion/mira_attempts/ssee_mira_derivative_test.py`. Coupling β_eff=u/√M⁴ depende
de la *velocidad* del campo (no del valor), encendido en matter era y
apagado hoy (lo que MIRA "necesita"). Barrido en M⁴_code:
- M⁴ ∈ {0.01, 1, 10}: integración OK, **R(z=1100)∈[1.32, 1.41]** — ~70%
  del log de MIRA, no llega.
- M⁴ ∈ {100, 462 (físico M≈9.68 meV canónico; el 8.81 meV era normalización ρ_crit previa), 10⁴}: integración rompe en z≈1–2.

Diagnóstico: el mecanismo funciona como mecanismo, pero requiere M
muchísimo más chico que Λ_SSEE para producir MIRA — UV-incompatible.

**Mecanismo #7 — integración forward desde φ-MDE hacia hoy.** Script
`archive/codigo/investigacion/mira_attempts/ssee_mira_phimde_forward_test.py`. Estado inicial Ω_m≈0.99 en
matter era, integrar hasta N=0. Barrido α∈{0.295, 0.521, 0.8, 1.0, 1.5}:

| α | w_φ(0) | Ω_m(0) | resultado |
|---|---|---|---|
| 0.295 (Copeland exp puro) | −0.88 ✓ | **0.00** ✗ | drenaje total |
| 0.521 (α_sat veta-2)     | −0.70   | **0.00** ✗ | drenaje |
| 0.8–1.5                  | crece   | **0.00** ✗ | drenaje |

**Hallazgo central:** las trayectorias forward llegan a N=0, pero el
coupling conformal drena *toda* la materia hacia el scalar en ~7 e-folds.
Ningún α reproduce simultáneamente w₀=−0.840 y Ω_m=0.32.

**Cierre matrix backward+forward.** Combinando #5 (backward) y #7 (forward):
no existe coupling conformal canónico que conecte φ-MDE con el estado de
hoy preservando materia. **6 mecanismos descartados para MIRA**, dos
cualitativamente distintos (topología #5/#7, escala #6).

Las dos lecturas siguen abiertas:
- **A**: continuar caza (disformal velocity-dependent, screening, ...)
- **B**: pivot a MIRA-como-etiqueta de transición, no engranaje.

## V-L3-2Om — mecanismo MIRA / transición Ω_m(z) — **ABIERTO (problema central del modelo)**

*Corrección de criterio (2026-05-22):* una versión anterior de esta entrada
marcaba esto «verificado (regla)». **Era una sobreafirmación.** Lo único
verificado es el *álgebra*; la *regla física* de uso no está derivada.

1. **✓ álgebra:** Ω_m,dyn = 1+w₀ = 0.16005 **sí** se deriva de φ,π.
   Ω_m,cosm = MIRA·Ω_m,dyn = 0.31993 (factor materia retirado 2026-06-18;
   hoy Ω_m = ω_m/h² = 0.308881, derivado) — el número es algebraico, pero
   **MIRA es hipótesis auxiliar no derivada** (lo dice `ssee_core.py` L41).
2. **✗ la regla NO está derivada.** «Ω_m,dyn fija w₀ y no entra en E(z);
   Ω_m,cosm va en E(z)/Poisson/CMB» es una **aserción**, no un teorema.
   No existe:
   - una derivación de *por qué* MIRA (≈2) amplifica la materia gravitante;
   - una función Ω_m,eff(z) que conecte el régimen tardío (BAO: 0.160
     funciona, 0.5σ DESI, cero parámetros libres) con el temprano (CMB:
     0.320 encaja). El modelo usa 0.320 y 0.160 como dos regímenes sin
     puente — **no se sabe qué pasa en la transición**.
3. **✗ riesgo de fondo:** poner 0.320 como término ∝(1+z)³ en E(z) es,
   fenomenológicamente, **materia oscura** — y el postulado fundacional de
   SSEE es *sin materia oscura, solo geometría y viscosidad*. Usar 0.320 en
   el fondo sin un mecanismo derivado puede estar contradiciendo el axioma
   que el modelo dice no necesitar.

**Por qué importa.** El resultado más fuerte de SSEE (DESI 0.5σ, cero
parámetros) se construyó con 0.160 en el fondo. El commit `4892b53`
(«corrección dos-Ω_m») cambió E(z) a 0.320 y, con el prior Planck-ΛCDM legacy,
movió H₀ a 67.756 — que producía r_d/θ* a 4–5σ. **El switch de prior MIRA
(2026-05-24) reancló H₀ a 66.533 posterior / 67.037 anchor** (ambos superados por el
reframe ω_m-directo 2026-06-19 → 67.159 / 67.962), y con esos H₀ <!-- R74: git:509001df85:CANONICAL_VALUES.yaml -->
r_d queda a ≤1.5σ y θ* a 0.66σ *en el anchor* (ver V-L4-rd/θ* re-corridas;
reframe da r_d 0.32σ y θ* 1.05σ). Lo que queda abierto NO es ya un 5σ duro en r_d, sino: (a) la
ausencia de Ω_m,eff(z) que puentee 0.160↔0.320, y (b) el split BAO–CMB de
1.2σ en H₀, que se manifiesta como tensión en θ* solo si se usa el posterior
en el observable CMB. Sigue siendo un cambio de configuración con
consecuencias, no una «corrección» sin costo.

**Veredicto.** Qué es MIRA físicamente, por qué la materia gravitante es 2×
la dinámica sin partícula de materia oscura, qué papel cumple AURA (=2·MIRA),
y cuál es Ω_m(z) entre CMB y BAO — **ése es el problema central abierto del
modelo**. Todo lo demás (r_d, θ*, H₀) son síntomas de esta brecha. **ABIERTO.**

## Estado final de Capa 3

Re-verificados **15 elementos**: OP-1..OP-7, α=φ⁴/3, m_φ, dos sectores (estos dos
retirados después, el 2026-08-01),
EFT, K(X), IS, c_s² (T_μν), dos-Ω_m.

| Veredicto | Elementos |
|---|---|
| **verificado** | α=φ⁴/3 |
| **PARCIAL** (álgebra/forma cierra, insumo físico no) | OP-2, OP-6, OP-7, EFT, IS — ~~dos sectores~~ y ~~m_φ~~ **RETIRADOS 2026-08-01** (la cadena cerraba unidades, pero la partícula no tenía de qué estar hecha) |
| **ABIERTO** | OP-1, OP-3, ~~OP-4~~ (cerrado 2026-10-03, radio retirado), OP-5, K(X), c_s² (T_μν), **dos-Ω_m (central)** |

2 bugs corregidos/detectados de paso: curvatura de Kähler (P1, **corregido**)
y M⁴ inconsistente P7↔P10 (**detectado**, pendiente de re-derivación).
Patrón confirmado en 14/14: ninguna "✅ RESUELTO" de CLAUDE.md lo estaba
sin reservas. **Ninguno es regresión** — todos son brechas preexistentes,
ahora rastreadas por el guardián (67 comprobaciones, 15 ABIERTO).

# Capa 4 — Confrontaciones con datos — *en progreso*

Aquí se verifica la **aritmética** que conecta cantidades reportadas:
tensiones (model−obs)/σ, S₈=σ₈√(Ω_m/0.3), χ²_r=χ²/N, ΔBIC. Los χ² de CMB
y los posteriores MCMC en sí salen de CAMB/CLASS/emcee — el guardián
verifica que los números encajen entre ellos, no re-corre los pipelines.

## V-L4-S8 — cadena S₈ weak-lensing (canónico 2026-06) — **verificado (aritmética)**

Usa Ω_m,CMB=0.308881 → √(Ω_m,CMB/0.3)=1.0147 (S₈ es amplitud gravitacional).

1. **✓ single-sector con A_s FIJO:** σ₈ = 0.814854 (techo CLASS todo-frío
   **con Σm_ν=0.06849 eV**, fuente Poisson Ω_m,CMB=0.308881).
   S₈ = 0.814854·1.0147 = 0.826827 → **2.74σ KiDS-1000** (DES-Y3 2.82σ).
   *(2026-09-08: era σ₈=0.8335 → S₈=0.846 → 3.5σ, de una corrida sin `.ini`,
   fuera del repo y sin neutrinos masivos. Ver la fila del techo en §B.)*
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7559 ± 0.0189` (0.10σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.04σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
2. ~~**✓ two-sector φ-DM (TITULAR, forward):** σ₈_eff = 0.7470 (free-streaming
   CLASS, k_fs=0.754 de m_φ=40.70 eV SOLAR²·KRYSTOS, cero fiteo). S₈_eff = 0.7470·1.0147 =
   **0.758 → 0.04σ KiDS-1000**. RESUELVE la tensión.~~ **RETIRADO 2026-08-01.**

**Veredicto (reescrito 2026-09-20):** la cadena S₈ es aritméticamente correcta
y usa la Ω_m correcta — eso sigue en pie. Lo que **ya no** se sostiene es a qué
llamaba titular: decía «el titular es el two-sector (0.758, 0.01σ)» **en
presente**, bajo su propio cartel de RETIRADO y bajo la línea 2 ya tachada, y
además mezclaba el 0.01σ (que era del viejo 0.766) con el 0.758 (que era 0.04σ).
Ese titular murió con la partícula el 2026-08-01.

**Propagación completa (2026-09-20), por niveles y en orden.** La primera vez
que se metió este resultado se hizo al revés —tomando el número y escribiéndolo
a mano en los documentos según se iban descubriendo— y el síntoma fue el de
siempre: documentos llamando canon a un valor ya superado. Rehecha siguiendo
`project_propagation_order`:

| nivel | artefacto | estado |
|---|---|---|
| N6 | `src/ssee_core.py` | n/a — S₈ es RESULTADO de corrida, no constante algebraica |
| N7 | `CANONICAL_VALUES.yaml` | ✅ fuente: `S8_ssee_unif: 0.8273` |
| N8 | `results/logs/` | ✅ 2 logs con el S₈ histórico de R3 verificados: son artefactos legítimos de SU corrida (R3, 2026-08-01, con fecha dentro). **2026-10-02:** esa lectura cortaba el burn-in sobre las cadenas pegadas; la vigente es `R3_ssee_kids_S8_rehecho.json` (0.7559) |
| N9 | `results/figures/` | ✅ 0 de 42 figuras muestran el valor |
| N10 | `manuscript/*.tex` | ✅ 7 papers (1,2,3,5,7,8,9): nota al sitio que cita a P6; fila nueva en las tablas de registro de P1 y P9; **criterio de falsación de P1 reescrito** |
| N11 | `docs/*.pdf` | ✅ 7 recompilados (bibtex + 2 pasadas), 0 refs rotas, verificado en la capa de texto |
| N12 | este Registro | ✅ esta entrada |
| N13 | guardián + memorias | ✅ R69 y R69b; memoria del método |

**Titular vigente:** un solo sector, Ω_m=0.308881. Contra KiDS-1000 crudo con
A_s libre, S₈=0.7559 ± 0.0189 (0.10σ). Contra KiDS-Legacy con A_s **clavado** al
del CMB —cero libres cosmológicos— S₈=0.8273 predicho contra 0.8265±0.0176
medido (0.05σ). Las dos cadenas viejas, la two-sector (0.758) y la G=0.866 →
σ₈ y S₈ con fuente Ω_m,dyn (cifras en git; ninguna corrida guardó log), están **retiradas**. **Verificado.**

## V-L4-DES — referencia DES-Y3 inconsistente entre scripts — **ABIERTO**

`ssee_paper5_IS_perturbations.py` usa **S₈_DES = 0.776±0.017** (DES-Y3
3×2pt, Abbott et al. 2022). `ssee_op5_hmcode.py` usa **S₈_DES = 0.759±0.023**
(DES-Y3 cosmic shear, Amon et al. 2022). Son dos análisis DES-Y3 reales y
distintos, pero la suite debería fijar **una** referencia para que las
tensiones reportadas sean comparables entre papers. Un árbitro lo marcaría.

## V-L4-CMB — espectro CMB Planck 2018 (Paper 3) — **verificado (re-run CAMB 2026-05-22)**

Re-corrido `ssee_paper3_cmb.py` con CAMB 1.6.5. Reproduce **exactamente**
lo reportado en CLAUDE.md:

*(NOTA 2026-07-08: esta tabla es el re-run histórico 2026-05-22 PRE-reframe,
valores superados; el canónico vigente es el de Paper 3 @ ω_m-directo:
TT 1.042, TE 1.040, EE 1.040, PP 0.720, ΔBIC diagonal −35.0.)*

| Espectro | SSEE χ²_r | ΛCDM χ²_r | N |
|---|---|---|---|
| TT | 1.047 | 1.043 | 1971 |
| TE | 1.041 | 1.040 | 1967 |
| EE | 1.041 | 1.039 | 1967 |
| PP | 0.837 | 0.757 | 9 |
| **ΔBIC(SSEE−ΛCDM)** | **−20.8** | — | N=5914 |

Picos TT en ℓ = 220, 536, 812 — también reproducidos. La aritmética
χ²_r→ΔBIC solo acota a [−22.9, −11.1] por el redondeo de χ²_r a 3
decimales; el −20.8 del pipeline cae dentro. **El test de datos central
de Paper 3 es reproducible. Verificado.**

## V-L4-rd — horizonte de sonido r_d — **r_d sano en ambos anclajes**

Re-corrido con CAMB en el reframe ω_m-directo (2026-06-19). Con los H₀
de entonces (anchor H_alg 67.962, posterior DR2 66.412 —hoy superado por
67.82±0.41, que da el mismo r_d = 147.174 Mpc: `run_p3_rd_reframe.py`,
re-corrido 2026-09-29—; el 67.159 previo usaba el vector DR1 mal etiquetado, superado): <!-- R74: git:509001df85:CANONICAL_VALUES.yaml -->

| H₀ usado | r_d resultante | tensión Planck (147.09±0.26) |
|---|---|---|
| 67.962 (anchor H_alg, CMB-óptimo ω_m-directo) | 147.17 Mpc | **0.32σ ✓** |
| 67.159 (posterior MCMC reframe con DR1 mal etiquetado, superado) | 147.17 Mpc | **0.32σ ✓** (r_d es H₀-invariante a ω fijo) | <!-- R74: git:509001df85:CANONICAL_VALUES.yaml -->
| 67.037 / 66.533 (anchor/posterior MIRA viejo) | 146.73 / *(sin log)* Mpc | *superado por reframe* |

**Mecanismo (ω_m-directo):** la parametrización SSEE fija la densidad física
ω_m = ω_b+ω_c+ω_ν = 0.14267 (forward, ω_c=KAL₀·ω_b·n_s), y Ω_m,CMB=ω_m/h²=0.308881
es DERIVADO. Como r_d depende de ω_m y ω_b (ambos algebraicos, independientes de
H₀), r_d es robusto: **147.17 Mpc (0.32σ) en ambas etapas**.
**El "✅" de r_d se restituye, ahora a 0.32σ (mejor que el 1.38σ del anchor MIRA viejo).**

## V-L4-θ* — escala acústica angular θ* — **RESUELTO (posterior coincide con anchor)**

θ* es el observable CMB *más preciso* (σ≈0.08%) y por eso es hipersensible a
H₀ vía D_A. Re-run CAMB **geometría total corregida 2026-07-09** (V-L4-DESI),
vs Planck 2018 **0.59668±0.00046°** (100θ*=1.04109±0.00030): <!-- R74: git:d7446ace8a:results/logs/p3_rd_reframe_omega_m.log -->

| H₀ usado | θ* resultante | tensión |
|---|---|---|
| 67.962 (anchor H_alg, CMB-óptimo ω_m-directo) | 0.59667° (100θ*=1.04139) | **1.00σ ✓** |
| **67.8244 (posterior MCMC DR2, prior H_glob, 2026-09-28)** | **0.59645° (100θ*=1.04099)** | **0.32σ ✓** |
| 67.7869 (log: git:513e84e:results/logs/mcmc_paper2_reframe.log) (posterior previo, prior número puro ±0.54) | 0.59638° (100θ*=1.04089) | 0.67σ *superado* |
| 66.412 (posterior con bug: sector 0.160 en E(z)) | 100θ*=1.03693 | ~~13.9σ~~ *bug superado* | <!-- R74: git:6039ffdbd0:CANONICAL_VALUES.yaml -->
| 67.159 (posterior con vector DR1 mal etiquetado) | 100θ*=1.03910 | ~~6.6σ~~ *superado* | <!-- R74: git:509001df85:CANONICAL_VALUES.yaml -->

**El giro (V-L4-DESI 2026-07-09):** la tensión de 13.9σ/6.66σ **era el bug de geometría** —
el sector frío 0.160 metido en E(z) hundía el posterior a 66.41 y desalineaba el θ*.
Con la materia TOTAL y ω_m algebraico fijo (R25), el posterior queda en 67.7869 (log: git:513e84e:results/logs/mcmc_paper2_reframe.log), **compatible con el anchor
CMB 67.962** (0.04σ). El θ* del posterior es entonces 0.91σ — sano por sí solo.
Ya NO hace falta el parche "no propagar el posterior a θ*": anchor y posterior dan
el MISMO CMB. Un control ΛCDM (w=−1) al mismo H₀ da θ* casi idéntico: la escala
acústica la fija H₀+ω, no la energía oscura w₀wₐ.

**Lectura para el documento de journal:** el H₀ del CMB (anchor 67.962) y el H₀ de
BAO (posterior 67.7869 (log: git:513e84e:results/logs/mcmc_paper2_reframe.log)) coinciden; r_d 0.32σ y θ* 0.67–1.00σ en ambos. El "split
BAO–CMB" desaparece — no era feature de w₀wₐ, era el sector 0.160 en la geometría.

## V-L4-MCMC — MCMC DESI+Planck (Paper 2) — **re-run 2026-07-09; geometría total corregida**

> **CERRADO 2026-09-30.** Re-corrida completa (SSEE incluido; el 29-sep había cargado la
> cadena SSEE de julio). Números de las cadenas con acta: `results/logs/resumen_3modelos.json`
> (`src/p02_mcmc/resumen_3modelos.py`, control contra la tabla del log: PASA).

Re-corrido `ssee_paper2_mcmc.py` (100 walkers × 25000 pasos × 3 modelos, 2.11 h,
DESI DR2 + geometría total Ω_m=0.308881, prior Planck común, r_d CAMB, cada modelo con su mν):

| Modelo | k | H₀ | ln P_MAP | BIC | ΔBIC |
|---|---|---|---|---|---|
| **SSEE** | 2 | 67.617 ± 0.349 | −5.52 | 16.58 | **0.00** |
| ΛCDM | 3 | 68.387 ± 0.278 | −7.76 | 23.83 | +7.25 |
| CPL | 5 | 67.264 ± 0.515 | −4.43 | 22.72 | +6.14 |

1. **✓ aritmética BIC:** BIC = k·ln(16) − 2·lnP_MAP se recomputa exacto desde las cadenas —
   **ΔBIC=+7.25 (ΛCDM), +6.14 (CPL) a favor de SSEE** (2026-10-01; era +6.77/+5.65 con el término de cúmulos asimétrico), el modelo más simple.
   ΔAIC +5.99/+3.34, ΔDIC −6.00 / −3.34 (`dic_from_chains.json`),
   Savage-Dickey lnB=2.34 (`savage_cv.json`; era 2.90 con la cadena CPL de julio).
   (lnB₁₀=7.42 RETIRADO: Laplace de una tabla huérfana, sin script vivo.)
   Cross-val: SSEE χ²_r(test)=0.262 < ΛCDM 0.711; CPL NO se cita (su ajuste de
   entrenamiento queda en el borde H₀=50; `savage_cv.json#alguno_en_borde`).
2. **✓ H₀ consistente:** 67.61±0.35 con prior Planck (0.40σ) y 67.82±0.41 con prior
   H_glob (reframe, 2026-09-28). Suben del 66.41 con bug 0.160.
3. **✓ Ω_b h² ≈ BBN:** posterior 0.02198±0.00048 vs OP-1 algebraico 0.02242 (0.91σ; `mcmc_paper2_reframe_obh2.json`, 2026-09-29).
   El "1.2σ menos barión" era el bug (0.02183/0.02285 con geometría 0.160). <!-- R74: git:6fdfa3b03c:results/logs/mcmc_professional.log -->
4. **✓ r_d(SSEE)=147.71 Mpc** ≈ r_d(ΛCDM) 147.59 (ratio 1.001; medianas del posterior, CAMB). El 175.16 crudo
   era Ω_m,dyn=0.160 en E(z) — el bug de geometría; con la total es el estándar.
5. **✓ Ω_m tensión = 0.88σ** (Ω_m,total=0.308881 vs Planck 0.315). La "21.3σ" era
   comparar el sector frío 0.160 con Planck — el bug dos-Ω_m, ahora DISUELTO.

**Veredicto:** la aritmética estadística (BIC, ΔBIC, tensión H₀) cierra y
**SSEE sigue favorecido (ΔBIC=+7.91)**. Pero el headline H₀ registrado
(66.75) está obsoleto — el valor vivo es 67.76. Y el dato bariónico
empuja en contra de OP-1.

## V-L4-DESI — datos BAO eran DR1 mal etiquetados como DR2 — **CORREGIDO (fuente única, 2026-07-01); re-runs PENDIENTES**

**Hallazgo (2026-07-01, pre-flight del mcmc_full).** Los 13 puntos BAO usados
por TODA la suite como "DESI DR2 (2503.14738)" eran en realidad **DESI DR1**
(2404.03002): 11/13 coinciden dígito a dígito con la Tabla 1 de DR1 (verificado
contra ambas tablas oficiales). Humo delator: LRG1 z=0.510 DH/rd = 20.98 (DR1, retirado)
cuando DR2 da **21.863** — el punto que más se movió entre releases. Además el
csv y los scripts ni coincidían entre sí (2 valores DH divergentes: el csv tenía
20.08/19.50 donde el código tenía 20.98/20.08 — todos valores viejos retirados).

**Punto QSO huérfano — EN REVISIÓN.** El vector viejo incluía un QSO
anisotrópico en z=1.491 (DM/rd=30.21±0.79, DH/rd=13.23±0.55) que **no existe en
ninguna fuente oficial**: DR1 solo publicó QSO isotrópico (DV/rd=26.07±0.67) y
DR2 publica DM/DH pero en z=1.484 con otros valores (30.512/12.817). Origen
desconocido (¿transcripción de una proyección? ¿preprint retirado?). Queda
marcado para rastrear su procedencia; mientras tanto está EXCLUIDO de la
fuente única (reemplazado por el QSO oficial DR2).

**Impacto en el titular w₀wₐ (FASE 0, recomputado):** con DR2 real la tensión
del punto algebraico (−0.840, −0.670) depende del compilado SN del contraste
w0waCDM: **0.24σ (Pantheon+: −0.838±0.055 / −0.62⁺⁰·²²)**, ~1.06σ
(DES-Y5, lit.), ~1.62σ (Union3, lit.). El "0.05σ" histórico era DR1+Pantheon+.
Titular honesto nuevo: *consistente con DR2 en 0.2–1.6σ según compilado SN,
con w₀ casi exacto*. DESY5/Union3 exactos: pinnear de 2503.14738 §VII en F3.

> **CORRECCIÓN 2026-09-08 — aquí ponía 0.09σ y no reproducía.** Lo cazó Mike:
> *«verifica eso bien porque yo también recuerdo 0.24 sigmas en DR2 y 0.05 en
> DR1»*. Tenía razón. Con los números que esta misma línea cita:
> ```
> chi2_2D = 0.42 con 2 g.l. (covarianza COMPLETA, Paper 2 ecs. 25-28)
>   -> P(exceder) = 0.81058  ->  0.2397 sigma equivalente  ->  0.24
> ```
> **Y una trampa que hay que dejar escrita**: la cuadratura *sin* correlación
> da un valor que **se parece por casualidad** (en la segunda cifra). No es la vía. Yo mismo derivé el
> 0.24 así el 2026-09-08 y salió bien de chiripa; creer esa vía llevaría a
> exigir 0.23 y a «corregir» un valor que está bien. La vía correcta es χ²
> bidimensional convertido a σ de una dimensión por su probabilidad de
> exceder.
> Ninguna lectura da 0.09: por w₀ solo sale 0.036, por wₐ solo 0.227, la
> cuadratura 0.230 y el χ² 2D 0.240. El 0.24σ es
> además lo que ya decían Paper 7 (3 sitios), CLAUDE.md, LECTURA_PAPERS.md y
> FUENTES_PENDIENTES.md. El sitio rancio era el Registro, o sea **el archivo
> que manda en caso de discrepancia** — el peor lugar donde tenerlo.
> Vigilado por **R63**, que recalcula la cuadratura en vez de comparar un
> literal.

**Corrección estructural (anti-recurrencia):**
1. `data/raw/desi_dr2_bao.csv` = fuente única: 13 valores DR2 Tabla 4 +
   corr_MH oficiales + release/arXiv/tabla por fila + historia del error.
2. `src/desi_dr2_data.py` = cargador único (`load_desi_dr2`,
   `desi_covariance` bloque-diagonal 2×2). Prohibido hardcodear.
3. Consumers wireados: `ssee_likelihoods.py` (mcmc_full), `ssee_mcmc_fase4.py`,
   `ssee_paper2_mcmc_reframe.py` — los 3 con covarianza completa.
4. Guardián CAPA DESI (R14, 6 checks): csv==Tabla 4 dígito a dígito, cero
   centinelas DR1, consumers importan del loader, 6 pares correlacionados.

**PENDIENTE (F3/F4):** re-correr Paper 2 MCMC reframe + Fase 4 + mcmc_full con
DR2; re-derivar contorno CPL de `ssee_paper2_analysis.py`; propagar a
manuscripts/figuras/README/AUDIT. Los headlines actuales (0.05σ, tabla Unified
§8) siguen siendo DR1 hasta esos re-runs.

## Estado final de Capa 4

Re-corridos los tres pipelines (CAMB r_d, CAMB CMB, emcee MCMC) el
2026-05-22.

| Veredicto | Elemento |
|---|---|
| **verificado / reproducido** | S₈ (P5), χ²+ΔBIC del CMB (P3), BIC+ΔBIC del MCMC (P2) |
| **ABIERTO — tensión grave (enmascarada)** | r_d 4.47σ, θ* 5.62σ — al usar el H₀ canónico |
| **ABIERTO — deriva de valor (resuelta)** | H₀ MCMC 66.75→67.76 — re-anclado a 67.756 |
| **ABIERTO — tensión física** | Ω_b h² −1.2σ vs OP-1 |
| **ABIERTO — inconsistencia de referencia** | DES-Y3 (0.776 vs 0.758; el 0.758 es valor RETIRADO 2026-08-01) |

**Lo que reprodujo es sólido**: el ajuste al CMB (χ²_r) y la preferencia
estadística por SSEE (ΔBIC negativo en P2 y P3) se sostienen al re-correr.

**Lo que la campaña destapó** — y es lo más importante de toda Capa 4: el
valor stale H₀=66.75 estaba **enmascarando** una tensión de 4.47σ en r_d
y 5.62σ en θ*. Al re-anclar H₀ al canónico 67.756 y propagarlo, las
tensiones aparecieron. El "r_d ✅ 0.25σ" era un artefacto. **Esta es la
brecha más grave del modelo y bloquea el sellado de Papers 2, 3 y 9**
hasta que se encare (revisar la parametrización Ω_m,cosm, o aceptar la
tensión y reportarla). Pendiente menor: fσ₈ (Papers 5–6).

# Capa 5 — Sellado de papers — *pendiente*

| Paper | Todos los elementos re-verificados | Chequeo completo | Sello (commit + sha256) |
|-------|-----------------------------------|------------------|-------------------------|
| P1–P10, Unified | — | — | — |

---

*Registro iniciado 2026-05-21 tras la revisión árbitro hostil de los 11 documentos.*
