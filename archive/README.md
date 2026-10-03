# Bitácora de Archivado — SSEE

Registro de **qué está archivado, cuándo y por qué**. Nada en `archive/` es
vigente: es el historial del proceso. Lo vivo está en los cajones vigentes
(ver Mapa de Vigencia). **Regla:** cuando algo deja de ser canónico, se mueve
aquí **con una entrada en esta bitácora** (fecha + razón + qué lo reemplaza).
Nada obsoleto se queda en un cajón vivo sin marcar; nada se archiva sin entrada.

**Organización (reorg 2026-06-24):** `archive/` se ordena **por tipo**, no por fecha.
Cada cajón contiene solo su tipo; las fechas y razones viven en esta bitácora.

```
archive/
  pdfs/      — PDFs de documentos viejos (drafts, versiones previas, enmiendas)
  figuras/   — figuras no usadas en los papers finales (.pdf + .png)
  chains/    — cadenas MCMC legacy (datos pesados, pre-reframe)
  codigo/    — scripts y fuentes (.py/.tex/.bib) superados
  superado/  — docs de trabajo superados, plegados al Registro canónico
  audio/     — grabaciones (reportes de auditoría), fuera del snapshot de envío
  zenodo_dictionary.zip — empaquetado histórico del diccionario
```

---

## Mapa de Vigencia (qué cajón debe estar siempre actual)

| Cajón | Estado | Auditado por |
|---|---|---|
| `manuscript/` (12 fuentes .tex) | **VIGENTE** | guardián + compilación + lectura hostil |
| `docs/` (PDFs compilados) | **VIGENTE** | recompilan de `manuscript/` |
| `src/` (módulos `pXX_*`, `verificacion/`, `estadistica/`) | **VIGENTE** | guardián (procedencia) |
| `results/logs/` (logs de procedencia) | **VIGENTE** | guardián R9 |
| `VERIFICATION_LEDGER.md`, `CANONICAL_VALUES.yaml` | **VIGENTE (fuente de verdad)** | guardián |
| `CLAUDE.md`, `SSEE-Vault/` | **VIGENTE (memorias)** | guardián Capa Memorias |
| `zenodo_dictionary/` | **VIGENTE** (registro publicado) | scripts corren limpio |
| `AUDIT.md`, `RIGOR_CHECKLIST.md` | **VIGENTE** (sistema de auditoría) | — |
| `archive/` | **HISTÓRICO** — no se edita, no se cita como vigente | esta bitácora |
| `sandbox_unificado/`, `notes/`, `class_ssee/output/`, `eftcamb_ssee/` | **TRABAJO** — no canónico, no auditado | — |

> `AUDIT_V7_PREFLIGHT.md` y `HALG_PIFI_CHANGEMAP.md` (antes en la raíz) se archivaron
> en `superado/` el 2026-06-24 (snapshots ya ejecutados; llevan banner interno).

---

## Catálogo de Archivado

### `pdfs/` — versiones anteriores de papers
**Archivados:** 2026-04 a 2026-05 · **Razón:** drafts / versiones intermedias superadas.
**Reemplazados por:** `docs/SSEE_PaperN_*.pdf` (recompilan de `manuscript/`).
- `SSEE_Paper1_Framework_v3.6.pdf`, `SSEE_Paper2_MCMC_Validation*.pdf` (draft/v1/v2),
  `SSEE_Paper2_Summary_ES_v1.pdf`, `SSEE_Paper2_draft.pdf`,
  `SSEE_Paper3_CMB_Confrontation*.pdf` (v1/v2), `SSEE_Paper3_Ch1_Perturbations_v1.pdf`,
  `SSEE_Paper3_Conclusion_PlanckPR4_v1.pdf`, `SSEE_Paper3_draft.pdf`,
  `SSEE_Paper3_CMB_backup.pdf` (backup pre-edición).
- `SSEE_Paper6_Holographic_Amendment.pdf` (2026-05-19) · enmienda holográfica explorada,
  no adoptada en el Paper 6 canónico (antes en `experimental/`).

### `figuras/` — figuras no usadas en los papers finales
**Archivadas:** 2026-06-04 · **Razón:** generadas en exploración; no entran en los
PDFs finales. Conservadas como registro visual del proceso (corner plots, scans,
diagnósticos B1/B3/IS, hi_class, Lyman-α audit, MCMC fase 4, rutas P(k)). 48 archivos (.pdf + .png).

### `chains/` — cadenas B1 CMB legacy pre-reframe
**Archivadas:** 2026-05-08 · **Razón:** cadenas Cobaya MCMC SSEE (`ssee_cmb.*`) de la tabla
B1 de Paper 3 con ingredientes **pre-reframe** (Ω_m,CMB=0.31993 vía MIRA, ω_b=0.02237,
H₀≈67.04). Superadas por el reframe ω_m-directo (ω_b=0.02242, ω_c=0.11951 forward fijo,
Σm_ν=0.0690, ancla H_alg=67.962); re-corrida con `src/p03_cmb/ssee_paper3_b1_mcmc.py`.
Las cadenas ΛCDM (`lcdm_cmb.*`) NO se archivan: sus ingredientes no cambiaron.

### `codigo/` — scripts y fuentes superados
**Archivados:** 2026-04 a 2026-06 · **Razón:** reemplazados por los módulos `pXX_*` vigentes
de `src/`, o experimentos exploratorios de un solo uso.
- **Reemplazados por módulos vigentes:** `ssee_inflation_connection.py` → `src/pB_inflation/`;
  `ssee_uv_completion.py` → `src/p10_uv/`; `ssee_paper3_cobaya.py` →
  `src/p03_cmb/ssee_paper3_cobaya_unified.py`; `ssee_paper2_mcmc_legacy.py` (2026-04-30) →
  `src/p02_mcmc/`.
- **Fuente obsoleta:** `SSEE_EFT_Fundamental_obsolete.tex` (2026-05-07) → Paper 7;
  `SSEE_appendix_Friedmann.tex` (2026-04-21) → integrado en Paper 1/2;
  `ssee_paper3_docs_duplicate.bib`, `ssee_paper6_docs_duplicate.bib` (duplicados de `manuscript/`).
- **Pre-canónico m_φ:** `p6_honest_matrix_PRECANONICAL_2026-06-02.py` (2026-05-25) → Paper 6
  canónico (2026-06-04).
- **MCMC P6 toy superado (archivado 2026-06-30):** `ssee_paper6_mcmc_toy_superseded.py`
  (antes `src/p06_phiDM/ssee_paper6_mcmc.py`). **Razón:** parametrización pre-reframe
  θ=(Ω_φDM, k_fs=0.493, σ₈) con prior 0.1599 y Ω_m,dyn=0.160; daba S₈≈0.817 (2.5σ),
  contradecía el titular two-sector. **Reemplazado por:** `src/p06_phiDM/ssee_paper6_mcmc_v2.py`
  (emulador CLASS validado 0.06%, θ=(Ω_φDM, m_φ, A_s), priors planos; Ω_φDM 0.24σ, S₈=0.782,
  ΔBIC=−14.3) — el que cita el Paper 6 §sec:mcmc.
- **Scratch exploratorio:** sensibilidad de cúmulos, scans α_M/θ*/σ₈, IS growth, candidatos;
  ningún resultado canónico depende de ellos.
- **Tooling deprecado (archivado 2026-06-24):** `ssee_audit_consistency.py`, `ssee_precision_audit.py`
  (verificadores viejos, superados por `ssee_verify.py`+`CANONICAL_VALUES.yaml`);
  `plot_ssee_pk.py`, `plot_ssee_twosector_pk.py` (plots Fase-1/2 huérfanos, no alimentan papers).

#### `codigo/investigacion/` — registro de investigación/mecanismo (archivado 2026-06-24)
**Razón:** material que documenta *cómo se construyó* el modelo pero que el modelo activo
ya no usa. Movido de `src/` para que `src/` quede solo con módulos vigentes. Reversible.
- `mira_attempts/` (8 scripts) — búsqueda del mecanismo MIRA (OP-8, **disuelto** por el reframe ω_m-directo).
- `mecanismos/`, `open_problems/` — exploración de mecanismos y OPs.
- Sueltos: `op8_mira_aura_dimensional.py`, `op10_kX_cubic_term.py`,
  `h_alg_vs_mira_investigation.py`, `ssee_h0_mira_only.py`, `ssee_paper2_mcmc_mira.py` (variante MIRA legacy del MCMC P2).
- `ssee_paper6_kinetic_braiding.py` (archivado 2026-07-02, auditoría de procedencia
  post-hallazgo DESI DR1/DR2) — exploración αB con target G_eff=MIRA (física retirada
  por el reframe) y set fσ₈ superseded (0.427/0.477, pre-2026-05-18). Sin referencias
  desde manuscripts ni src/.

### `superado/` — docs de trabajo plegados al Registro canónico
**Archivados:** 2026-06-08 (lote inicial) y 2026-06-24 (snapshots de raíz) · **Razón:** su
contenido se consolidó en `VERIFICATION_LEDGER.md`, `CANONICAL_VALUES.yaml` y los papers canónicos.
- `H0_CASCADE_AUDIT.md` → cascada H₀ en P9/P10 + Registro §B.
- `SSEE_CONSTANTS_AUDIT.md` → `CANONICAL_VALUES.yaml` + guardián.
- `P6_CLEANUP_NOTES.md` → Paper 6 canónico.
- `OPEN_PROBLEMS_LAGRANGIAN_MAP.md` → `OPEN_PROBLEMS.md`.
- `SEALED_STATUS.md` → estado del Sealed (vigente en CLAUDE.md).
- `ssee_paper6_mass_derivation.py` (2026-06-04) → derivación m_φ previa; superada por la
  forward-prediction canónica.
- `AUDIT_V7_PREFLIGHT.md` (archivado 2026-06-24) → snapshot de auditoría pre-vuelo del
  2026-06-14; lleva banner interno "pre-reframe ω_m-directo".
- `HALG_PIFI_CHANGEMAP.md` (archivado 2026-06-24) → changemap del H_alg/π-φ ya ejecutado.

### `manuscript_superseded/` — narrativas de paper retiradas
**Archivado:** 2026-07-09 · **Razón:** el fix Ω_m-geometría (V-L4-DESI): el sector frío
0.160 (=1+w₀) estaba en la geometría de fondo E(z)/r_d, donde va la materia TOTAL
0.30889. El bug inflaba seis tensiones falsas; corregidas, la narrativa que las
documentaba se retira.
- `paper2_206_narrative_RETIRED.md` → narrativa "+206 / r_d=175.6 / two-Ω_m / H(z) 1.86 /
  θ* 13.9σ" de Paper 2, con la tabla de las seis tensiones antes/después y las fuentes de
  los valores nuevos. El detalle línea-a-línea vive en git (commits `076b435`+).

### `audio/` — grabaciones de reportes
**Archivado:** 2026-07-19 · **Razón:** activos de audio pesados que no forman parte del
paquete de envío (revista/Zenodo); se mueven fuera de la raíz para dejar el snapshot limpio.
- `auditoria_reporte.mp3` → reporte de auditoría en audio (4.2 MB). Movido desde la raíz
  del repo por recomendación de auditoría externa (M-4): un snapshot Zenodo no debe llevar
  binarios de audio en la raíz.

### `codigo/p06_phiDM_RETIRADO_2026-08-01/` — el sector φ-DM y su partícula
**Archivado:** 2026-08-01 · **Razón:** doble fallo independiente, cada uno suficiente.
(1) La resta que definía la partícula, Ω_φDM = Ω_m,CMB − Ω_m,dyn = 0.308881 − 0.160,
restaba una densidad medida menos un número de la **ecuación de estado** (0.160 = 1+w₀):
bien formada aritméticamente, vacía de física ⟹ la partícula no tenía de qué estar hecha.
(2) La tensión S₈ que motivaba el sector no existe en el dato crudo — se medía contra el
estadístico comprimido S₈ (reducido bajo ΛCDM) y con A_s fijado a Planck. Con un solo
sector y A_s libre, el MCMC contra los 225 puntos de ξ± de KiDS-1000 da
**S₈ = 0.7555 ± 0.0192 → 0.11σ**.
**Reemplazado por:** `src/p06_growth/` (código vigente) y
`manuscript/SSEE_Paper6_Growth.tex` (paper reescrito).
**Cierra por disolución:** OP-9, OP-10, OP-11, OP-12 — ninguno resuelto; todos dejaron de
ser preguntas al retirarse el objeto del que trataban. Ver el README del cajón.
- `ssee_paper6_verification.py`, `ssee_paper6_sterile_neutrino.py`,
  `ssee_paper6_canonical_particle.py`, `ssee_paper6_particle_scan.py`,
  `ssee_paper6_mcmc_v2.py`, `ssee_paper6_mcmc_grid.py`, `p6_canonical_table.py`,
  `p6_complete_matrix.py` → toda la cadena m_φ → k_fs → α → σ₈/S₈ del sector retirado.

### `logs_superados/` — logs de resultado reemplazados por una re-corrida (2026-10-01)
- `R1R2_boss_lpt_cobaya_20260908_mnu006.json`: resumen R1/R2 de BOSS DR12 del 2026-09-08. Su bloque SSEE salió de
  cadenas corridas con el Σm_ν de ΛCDM (0.06 en vez de 0.06849). Lo reemplaza `results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json`,
  que escribe `src/p06_growth/analiza_boss_R1R2.py`. Se conserva porque es el CONTROL de ese script (el bloque ΛCDM,
  con cadenas que no se rehicieron, tiene que reproducirse) y porque P6 cita su Δχ² = +0.06 como registro de la corrección.
- `cumulos_7.json`, `cumulos_7.log` (2026-10-01): la prueba de cúmulos de P2 con la fórmula MOND de abril
  (M = M_bar·KAL₀·(1+f_ν)) sobre 4 cúmulos atribuidos a Zhang+2026 que no están en sus tablas, más 3 de
  extensión circulares. La reemplaza `results/logs/cumulos_zhang2026.json` (46 sistemas reales, RG, control ΛCDM).

### `codigo/p02_cumulos_mond_2026-04/` — la prueba de cúmulos del marco MOND (2026-10-01)
- `cumulos_7.py`: generaba la tabla de cúmulos de P2 con M = M_bar·KAL₀·(1+f_ν). Retirado porque el modelo vigente
  es relatividad general (α_T=α_M=α_B=0, P7; límite canónico de P8) y porque sus datos no salían de la fuente citada.
  Lo reemplaza `src/p02_mcmc/cumulos_zhang2026.py`.

- `codigo/investigacion/huerfanos_2026-10-02/` (2026-10-02): `ssee_paper3_hiclass_check.py` y `ssee_eftcamb_validation.py` con sus figuras; ningun documento los citaba y su fisica estaba retirada (0.160 en la geometria; w constante). Ver su README.

### `datos_retirados/` — datos crudos que la fuente contradice (2026-10-02)
- `cluster_masses_2026-10-02.csv`: las masas de cúmulos (Coma, A2029, A478 y Bullet) que citaban a Zhang+2026. Al cotejarlas con la fuente (R76), Coma y Bullet no aparecen y A2029 y A478 vienen con otros números. Nadie lo usaba ya. Lo reemplaza `data/raw/zhang2026/tablas_II_III.tex`, leído por `src/p02_mcmc/cumulos_zhang2026.py`. El detalle está en `archive/datos_retirados/README.md`.

- `boss_control.py`, `boss_fit.py` — salen de `src/p06_growth/` el 2026-10-03 hacia `logs_superados/boss_kaiser_20260808/`: ajuste Kaiser lineal de BOSS, superado por LPT (`boss_lpt_R1R2.py`, en la cadena). Detalle en el README de esa carpeta.

- **Clasificación de los logs fuera de la cadena (2026-10-03, regla de Mike):** 57 logs y 15 scripts salen de `results/logs/` y `src/` hacia `logs_superados/{particula_colas_24_29_2026-09, punto_de_fuga_2026-09-08, p6_exploracion_2026-07-30, era_v36_mira_dr1, corridas_cortadas, pruebas_puntuales}/` y `codigo/investigacion/{beta_c_RETIRADO_2026-09-07, particula_RETIRADA_2026-08-01}/logs/`. Cada carpeta lleva su README con el motivo (corrida mala reemplazada, o superada por física nueva) y lo que la reemplaza. Detalle y lo que se quedó, con su porqué: `VERIFICATION_LEDGER.md` §V-L5-CLASIF. Segundo pase (R65): `no_circular.py` + `s8_barra_kids.json` a `logs_superados/p6_exploracion_2026-07-30/` y `kids_twosector.py` (two-sector contra KiDS-1000 crudo, sector φ retirado) a `codigo/investigacion/particula_RETIRADA_2026-08-01/`.
- **R3 de KiDS-1000 con burn-in sobre cadenas pegadas (2026-10-03):** `R3_ssee_kids_S8.json` a `logs_superados/r3_burnin_concatenado_2026-09-30/`; lo reemplaza `R3_ssee_kids_S8_rehecho.json` (etapa `R3_rehecho`), que lo sigue leyendo como control del método viejo.

## Inventario declarado (2026-10-03)

**Por qué existe esta sección.** La regla de arriba («nada se archiva sin entrada») no la
verificaba nadie, y 172 archivos llegaron sin estar nombrados. Desde el 2026-10-03 la vigila
**R77** del guardián: todo archivo de `archive/` debe aparecer por su nombre en esta bitácora
o en un README de su carpeta. Aquí van los que faltaban, cada uno con el commit que lo trajo
a `archive/` y su mensaje: el porqué sale del historial, no de la memoria. Cuando ese commit
es una reorganización (p. ej. `642bffa` o `b3ba7c5`), el motivo original **no quedó
registrado**: vale entonces el de su cajón en el Catálogo de arriba.

### `archive/chains/`
- `ssee_cmb.1.txt` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_cmb.checkpoint` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_cmb.covmat` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_cmb.input.yaml` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_cmb.progress` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_cmb.updated.dill_pickle` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_cmb.updated.yaml` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»

### `archive/codigo/`
- `build_arxiv_packages.py` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fix_p1.py` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fix_p9.py` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `regenerate_fig_corner_p2_legacy.py` — llegó en `7026bf6` (2026-07-10): «audit(zenodo): purga masiva de valores legacy en OPEN_PROBLEMS y archivado de scripts obsoletos»
- `ssee_b3_mira.py` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_candidate1_test.py` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_cluster_sensitivity.py` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_is_growth.py` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_mira_background_IS.py` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_nonlinear_s8_legacy.py` — llegó en `7026bf6` (2026-07-10): «audit(zenodo): purga masiva de valores legacy en OPEN_PROBLEMS y archivado de scripts obsoletos»
- `ssee_option_b_IS_sigma8.py` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_paper3_diagnostic.py` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_paper3_sigma8.py` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_paper3_theta_scan.py` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_paper6_alphaM_scan.py` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_paper6_lyman_alpha_audit_legacy.py` — llegó en `7026bf6` (2026-07-10): «audit(zenodo): purga masiva de valores legacy en OPEN_PROBLEMS y archivado de scripts obsoletos»
- `ssee_paper6_phi_dark_matter.py` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_phase_c_dic_legacy.py` — llegó en `7026bf6` (2026-07-10): «audit(zenodo): purga masiva de valores legacy en OPEN_PROBLEMS y archivado de scripts obsoletos»

### `archive/codigo/investigacion/huerfanos_2026-10-02/figuras/`
- `fig_hiclass_TT.pdf` — llegó en `fb37984` (2026-10-02): «Restos que la propagacion no alcanzo: P4 (H_glob era el numero puro; 'el CMB prefiere 67.962'; A_s/tau 'est…»
- `fig_hiclass_TT.png` — llegó en `fb37984` (2026-10-02): «Restos que la propagacion no alcanzo: P4 (H_glob era el numero puro; 'el CMB prefiere 67.962'; A_s/tau 'est…»
- `fig_hiclass_alpha.pdf` — llegó en `fb37984` (2026-10-02): «Restos que la propagacion no alcanzo: P4 (H_glob era el numero puro; 'el CMB prefiere 67.962'; A_s/tau 'est…»
- `fig_hiclass_alpha.png` — llegó en `fb37984` (2026-10-02): «Restos que la propagacion no alcanzo: P4 (H_glob era el numero puro; 'el CMB prefiere 67.962'; A_s/tau 'est…»
- `ssee_eftcamb_CMB_TT.png` — llegó en `fb37984` (2026-10-02): «Restos que la propagacion no alcanzo: P4 (H_glob era el numero puro; 'el CMB prefiere 67.962'; A_s/tau 'est…»
- `ssee_eftcamb_Pk.png` — llegó en `fb37984` (2026-10-02): «Restos que la propagacion no alcanzo: P4 (H_glob era el numero puro; 'el CMB prefiere 67.962'; A_s/tau 'est…»

### `archive/codigo/investigacion/mira_attempts/`
- `ssee_alpha_saturation.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_alpha_saturation_stepB.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_alpha_saturation_stepC.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_alpha_saturation_stepD.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_alpha_saturation_stepD2.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_mira_saturated_test.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»

### `archive/codigo/investigacion/op4_rkm_RETIRADO_2026-10-03/`
- `fig_paper8_vainshtein.png` — llegó en `eda1f97` (2026-10-03): «tabla_sondas_tex: la tabla SSEE contra LCDM sonda por sonda para PRD y Sealed, leida del log de sondas, con…»

### `archive/codigo/investigacion/open_problems/`
- `op10_dimensional_bridge.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op10_mechanisms_2to6.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op10_principled_search.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op10_systematic_search.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op11_xi_from_overproduction.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op12_route2_freezeout.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op12_thermal_decoupling.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op12_trace_lights_qcd.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op14_yukawa_attack.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op18_As_from_inflation.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op8_constants_network.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op8_coupled_dm_de.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op8_lambda_P7_coupling.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op8_tracker_delta_phi.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op9_gravitational_production.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op9_lineage_grammar_scan.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op9_misalignment_relic.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op9_multiplier_search.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op9_particle_existence.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op9_phi_dm_formula_search.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op9_phi_i_search.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op9_physical_formula.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op9_transport_derivation.py` — llegó en `7220fce` (2026-07-11): «close(OP-9): intento transporte acotado → CORTE, congelar Camino A»
- `op_As_from_potential.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op_osiris_kretschmann_trigger.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `op_osiris_primordial_split.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op10_family2_dynamics.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op10_family3_axion.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op10_phase2e_dynamic_mass.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op10_potential_catalog.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op10_seesaw_search.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op10_uv_induced_minimum.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op13_canonical_lensing.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op14_neutrino_mass.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op1_baryogenesis.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op1_baryon_density.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op3_separability.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op4_vainshtein.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op5_hmcode.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»
- `ssee_op6_screening_form.py` — llegó en `b592853` (2026-06-24): «chore(organización mesa Stage 2): mover investigación+tooling deprecado a archive/»

### `archive/codigo/investigacion/open_problems/salidas_2026-10-02/`
- `op18_As_from_inflation.log` — llegó en `a509d91` (2026-10-02): «salidas de OP-1 y OP-18 (forzadas: *.log se ignora en archive/)»
- `ssee_op1_baryogenesis.log` — llegó en `a509d91` (2026-10-02): «salidas de OP-1 y OP-18 (forzadas: *.log se ignora en archive/)»
- `ssee_op5_hmcode.log` — llegó en `5480fef` (2026-10-02): «R74: fuente_git respeta el exponente; salida con acta de HMcode (OP-5); cifras sin log ni script reproducib…»

### `archive/codigo/investigacion/p9_disforme_RETIRADO_2026-10-03/`
- `fig_paper9_fscreen_z.png` — llegó en `a587d6a` (2026-10-03): «P9 figura: lee cada medida de su fuente (h0_por_metodos) y escribe log con acta; control CCHP v3 70.39 (el …»

### `archive/codigo/investigacion/particula_RETIRADA_2026-08-01/`
- `circular_test.py` — llegó en `aaf0a58` (2026-09-19): «verde, tramo 3: R44b a cero, R60 de 58 a 34 y los papers recompilados»
- `class_probe3.py` — llegó en `aaf0a58` (2026-09-19): «verde, tramo 3: R44b a cero, R60 de 58 a 34 y los papers recompilados»
- `precio_cmb_rejilla_extendida.py` — llegó en `c127be7` (2026-10-01): «R35: b1_analyse re-corrido (identico: -25.766, k=3 validacion); experimento 4 priors sin el termino de cumu…»
- `ssee_kids.py` — llegó en `aaf0a58` (2026-09-19): «verde, tramo 3: R44b a cero, R60 de 58 a 34 y los papers recompilados»
- `ssee_paper6_cmb_fs8_filter.py` — llegó en `aaf0a58` (2026-09-19): «verde, tramo 3: R44b a cero, R60 de 58 a 34 y los papers recompilados»
- `t2_grid.py` — llegó en `aaf0a58` (2026-09-19): «verde, tramo 3: R44b a cero, R60 de 58 a 34 y los papers recompilados»
- `t2_nl.py` — llegó en `aaf0a58` (2026-09-19): «verde, tramo 3: R44b a cero, R60 de 58 a 34 y los papers recompilados»

### `archive/figuras/`
- `fig3_omega_de.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig4_KAL_interpolation.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig5_corner_ssee.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig5_corner_ssee.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig6_corner_lcdm.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig6_corner_lcdm.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig7_Hz_comparison.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig8_bao_residuals.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_b1_corner_lcdm.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_b1_h0_sigma8_ssee.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_b3_mira.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_b3_mira.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_candidate1_fsig8.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_candidate1_fsig8.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_cluster_residuals.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_cluster_sensitivity.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_corner_cpl_professional.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_corner_ssee_mira_prior.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_corner_ssee_professional.pdf` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_eft_beta_convergence.pdf` — llegó en `85caadf` (2026-09-07): «chore(archive): beta_c al cajon — y 20 rutas que apuntaban al vacio»
- `fig_eft_beta_convergence.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_eft_verification.pdf` — llegó en `85caadf` (2026-09-07): «chore(archive): beta_c al cajon — y 20 rutas que apuntaban al vacio»
- `fig_eft_verification.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_h0_four_priors.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_h0_three_priors.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_hiclass_TT.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_hiclass_TT.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_hiclass_alpha.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_hiclass_alpha.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_inflation_connection.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_inflation_connection.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_is_growth.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_is_growth.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_optionB_sigma8_selfconsistent.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_optionB_sigma8_selfconsistent.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper10_KX_profile.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_paper10_alphaK_vs_alpha.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_paper5_S8_comparison.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper5_growth_rate.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper5b_MIRA_background.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_alphaM_scan.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_corner.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_corner.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_fsig8_mcmc.pdf` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_paper6_fsig8_mcmc.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_paper6_kinetic_braiding.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_lyman_alpha_audit.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_lyman_alpha_audit.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_mcmc.pdf` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_paper6_mcmc.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_paper6_mcmc_v2_corner.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_paper6_phi_dark_matter.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_sigma8_tension.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_sigma8_tension.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_sterile_neutrino.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_trace.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper6_trace.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_paper8_lensing_ratio.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_paper8_vainshtein.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_paper9_fscreen_z.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_paper9_h0_tension.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_pk_cuatro_rutas.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_pk_diferencia_lcdm.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_press_schechter.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_press_schechter.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `fig_toe_cmb_TT.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_toe_derivations.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `fig_w0wa_degeneracy.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `mcmc_fase4_corner.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `mcmc_fase4_corner.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `mcmc_fase4_traces.png` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `ssee_eftcamb_CMB_TT.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»
- `ssee_eftcamb_Pk.png` — llegó en `9d132be` (2026-07-11): «chore(repo): limpieza de docs, figuras redundantes y scripts temporales para zenodo»

### `archive/logs_superados/`
- `erosita_cr.json` — llegó en `df161d6` (2026-10-03): «archivo: barrido Kaiser de BOSS (sondeo 08-08, superado por LPT R1/R2, no reproduce: minimizador mal condic…»
- `p3_cmb_reframe_omega_m.log` — llegó en `409be7e` (2026-10-03): «s_m no es densidad, propagacion en el codigo: fuera el caso naive (s_m como Omega_m) de ssee_paper3_cmb y c…»

### `archive/logs_superados/boss_kaiser_20260808/`
- `boss_control_kmax0.060.json` — llegó en `df161d6` (2026-10-03): «archivo: barrido Kaiser de BOSS (sondeo 08-08, superado por LPT R1/R2, no reproduce: minimizador mal condic…»
- `boss_control_kmax0.080.json` — llegó en `df161d6` (2026-10-03): «archivo: barrido Kaiser de BOSS (sondeo 08-08, superado por LPT R1/R2, no reproduce: minimizador mal condic…»
- `boss_control_kmax0.100.json` — llegó en `df161d6` (2026-10-03): «archivo: barrido Kaiser de BOSS (sondeo 08-08, superado por LPT R1/R2, no reproduce: minimizador mal condic…»
- `boss_control_kmax0.120.json` — llegó en `df161d6` (2026-10-03): «archivo: barrido Kaiser de BOSS (sondeo 08-08, superado por LPT R1/R2, no reproduce: minimizador mal condic…»
- `boss_fit_kmax0.060.json` — llegó en `df161d6` (2026-10-03): «archivo: barrido Kaiser de BOSS (sondeo 08-08, superado por LPT R1/R2, no reproduce: minimizador mal condic…»
- `boss_fit_kmax0.080.json` — llegó en `df161d6` (2026-10-03): «archivo: barrido Kaiser de BOSS (sondeo 08-08, superado por LPT R1/R2, no reproduce: minimizador mal condic…»
- `boss_fit_kmax0.100.json` — llegó en `df161d6` (2026-10-03): «archivo: barrido Kaiser de BOSS (sondeo 08-08, superado por LPT R1/R2, no reproduce: minimizador mal condic…»
- `boss_fit_kmax0.120.json` — llegó en `df161d6` (2026-10-03): «archivo: barrido Kaiser de BOSS (sondeo 08-08, superado por LPT R1/R2, no reproduce: minimizador mal condic…»

### `archive/manuscript_superseded/`
- `SSEE_Paper6_phiDM_TWOSECTOR_RETIRED.pdf` — llegó en `36aa061` (2026-07-31): «docs(P6): publica el PDF renacido, archiva el viejo (dos sectores)»
- `SSEE_Paper6_phiDM_TWOSECTOR_RETIRED.tex` — llegó en `88cbd16` (2026-07-31): «feat(P6): renace el Paper 6 — retracta dos sectores y particula, mide en crudo»
- `ssee_paper6_TWOSECTOR_RETIRED.bib` — llegó en `88cbd16` (2026-07-31): «feat(P6): renace el Paper 6 — retracta dos sectores y particula, mide en crudo»

### `archive/manuscript_superseded/envios_2026-05_RANCIOS/`
- `abstracts_arXiv.txt` — llegó en `81b1556` (2026-10-03): «s_m no es densidad, propagacion en papers y cajones: PRD y Sealed sin la 'prueba Boltzmann' que comparaba c…»
- `cover_letter_paper2_JCAP.txt` — llegó en `81b1556` (2026-10-03): «s_m no es densidad, propagacion en papers y cajones: PRD y Sealed sin la 'prueba Boltzmann' que comparaba c…»
- `cover_letter_paper3_JCAP.txt` — llegó en `81b1556` (2026-10-03): «s_m no es densidad, propagacion en papers y cajones: PRD y Sealed sin la 'prueba Boltzmann' que comparaba c…»

### `archive/pdfs/`
- `SSEE_Paper2_MCMC_Validation.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `SSEE_Paper2_MCMC_Validation_draft.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `SSEE_Paper2_MCMC_Validation_v1.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `SSEE_Paper2_MCMC_Validation_v2.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `SSEE_Paper3_CMB_Confrontation.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `SSEE_Paper3_CMB_Confrontation_v1.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
- `SSEE_Paper3_CMB_Confrontation_v2.pdf` — llegó en `2dc8729` (2026-06-24): «chore(organización mesa): reorganizar archive/ por tipo + limpiar raíz»
