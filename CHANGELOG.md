# Changelog

## V3.6.4 — Ola de refuerzo tras auditoría externa: reproducibilidad + dato KiDS + R20 (2026-07-13)

Dos auditorías externas hostiles-pero-justas (una sobre los papers, otra sobre el repo
completo). Veredicto de fondo: la **física sobrevive** (núcleo w₀wₐ NO es numerología por
veredicto del auditor; integridad DESI DR2 "ejemplar"; sin fugas de tokens; sin fits ocultos
vigentes). Lo que falló fue **fontanería + un typo de dato**. Cada hallazgo verificado contra
la fuente antes de tocar nada.

- **H1 — reproducibilidad (FATAL-corregible).** El `.gitignore` prohibía `results/logs/*.log`,
  así que el guardián daba **VERDE en local pero ROJO en un clon limpio** (la capa de
  procedencia exige que los logs referenciados en VERIFICATION_LEDGER §B existan). Negación
  `!results/logs/*.log` re-incluye los **28 logs de procedencia** (texto, 3.2 MB). Binarios
  pesados (`*.npz`, chains) siguen fuera → Zenodo/regeneración. **Verificado VERDE 142 en clon
  limpio** (`git archive HEAD`).
- **H2 — dato mal etiquetado (solo código).** `ssee_paper6_verification.py:247` tenía
  `kids_s8=0.758` — que es la **predicción SSEE**, no la observación KiDS (**0.759**) —
  imprimiendo 0.00σ en vez del **0.04σ** real. Corregido; etiquetas `0.01σ→0.04σ`. Los papers
  ya eran correctos (0.04σ); el error vivía solo en el script.
- **H4 — punto ciego → R20.** Nuevo bloque `observational_anchors` en CANONICAL_VALUES.yaml
  (KiDS/DES = el DATO). Nueva **capa R20** del guardián: `kids_s8/kids_sig8/des_s8` en todo
  `src/**.py` deben coincidir con las anclas → caza "predicción metida como dato". +3 checks
  (**139→142**). Documentado en RIGOR_CHECKLIST **R20**.
- **Audit A — Predictive Register completado.** Añadida la fila **S₈ two-sector = 0.758
  (0.04σ KiDS, forward CLASS, Retrodiction)** a la tabla de estatus epistémico de Paper 1
  (antes faltaba el titular "resuelve S₈"). PDF recompilado (32 pp).

## V3.6.3 — OP-19 + covarianza BAO justificada + pre-flight de puerta (2026-07-12)

- **OP-19 formalizado (mecanismo detrás de ω_c = KAL₀·ω_b·n_s).** Nueva frontera abierta:
  la relación es forward y funciona (0.4σ Planck), pero falta el **mecanismo de abundancia
  relic** que derive *por qué esa combinación*. Dos capas: (1) por qué ω_c∝ω_b (coincidencia
  cósmica que ΛCDM deja libre; SSEE fija ω_c/ω_b=KAL₀·n_s≈5.33 → exige origen compartido
  barión-DM, liga OP-1); (2) por qué el coeficiente es KAL₀·n_s. Incluye **plan de ataque**
  (blanco/mapa/filtro/veredicto) y **declaración de honestidad**: el ajuste solo fija el 3er
  factor a la ventana **[0.960, 0.979]** (~2%) — n_s es candidato **líder** (anclaje Planck +
  φ⁻⁷, doble-deber), no una certeza. Garantía hoy = falsabilidad (k_fs=0.754).
- **Covarianza DESI DR2 justificada (Wave 3 / auditoría externa F7).** La covarianza
  bloque-diagonal 2×2 por tracer (r_MH oficiales, Tabla 4) YA es correcta = así se usa el
  vector consenso comprimido (tracers en cáscaras z disjuntas → inter-tracer despreciable;
  LRG3+ELG ya combinado upstream). Nota al pie de Paper 2 reescrita para **justificarlo**
  (antes solo "puede subestimar"); registrado en RIGOR_CHECKLIST **R14**. PDF recompilado.
- **Pre-flight de puerta de entrada (para auditoría externa + Zenodo + Buchalter).**
  README: **postulados 4→3** (D, S, I; el factor-materia M quedó disuelto en el reframe
  ωm-directo, OP-8), conteo OP **18→19** (+fila OP-19). Lineaje **KRYSTOS→KRYSTOS_V**
  completado donde se había saltado la fuente de verdad: **CANONICAL_VALUES.yaml** (nombre +
  linaje "2Ω"→"φ+π+Ω", que preserva no-auto-suma) y **AUDIT.md**. Guardián VERDE 139.

## V3.6.2 — Ω_m-geometry fix (V-L4-DESI) + ν-closure unification + full documentation audit (2026-07-10)

- **CRITICAL geometry fix (V-L4-DESI, 2026-07-09).** The background geometry E(z)/r_d
  was mistakenly fed the *cold dynamical sector* Ω_m,dyn=0.160 (=1+w₀, an equation-of-state
  quantity) instead of the *total* matter density Ω_m=ω_m/h²=**0.30889**. The bug inflated
  **six false tensions** that the suite documented as real; all corrected:
  χ²_BAO **726→~11**, Ω_m **21.3σ→0.88σ**, r_d **175.6→148.2 Mpc** (1.002× ΛCDM),
  θ* **6.66σ→0.67σ**, H₀ posterior **66.41→67.79 ± 0.35** (0.66σ Planck, **0.50σ from the
  H_alg anchor** — DR2 *confirms* the prediction), χ²_r(H(z)) **1.86→0.482**. Guardian canary
  R14 now watches for recurrence (0.160-in-E(z) must hurt: χ²=725; total must be sane: χ²=11).
- **ν-closure constant unified to 93.14 (demonstrated from first principles, 2026-07-10).**
  The neutrino closure ω_ν h² = Σm_ν/C was standardised on **C=93.14 eV** (N_eff=3.046, PDG/Planck;
  derived C=ρ_crit/n_ν=94.06 at instantaneous decoupling as the cross-check). Propagated
  suite-wide: **m_φ = 40.70 eV** (was 41.02), **k_fs = 0.754 h/Mpc** (was 0.762),
  **σ₈ = 0.747**, **S₈ = 0.758** (0.04σ KiDS), **Σm_ν = 0.0685 eV**.
- **Full documentation audit — 10 papers + 3 consolidation docs to 10/10.** Hostile
  paper-by-paper pass (grammar + math + physics + coherence + figures + citations +
  provenance); every finding the guardian missed became a permanent rivet (R15–R19).
  The Unified Journal's three legacy figures (CLASS CMB TT, EFTCAMB CMB TT + P(k)) were
  **regenerated at the canonical ω_m-direct background** (0.30889, no MIRA factor),
  restyled to journal quality (white background, µK²), and their Spanish labels
  translated to English; retired-live claims (MIRA=Ω_CMB/Ω_dyn, "MIRA derivation" open
  problem) that contradicted the reframe were corrected.
- **Root refresh.** README, AUDIT.md, CITATION.cff, RIGOR_CHECKLIST.md brought to the
  canonical values (m_φ, k_fs, S₈, n_s tension 0.16σ, CMB ΔBIC −32.9/−24.0/−35.0,
  OPEN_PROBLEMS 18 items). Guardian **VERDE, 139 checks**.

## V3.6.1 — DESI DR2 vector correction: DR1 data mislabelled as DR2 (2026-07-02)

- **CRITICAL data-provenance fix (V-L4-DESI).** The 13-point BAO vector used across
  the entire suite as "DESI DR2 (arXiv:2503.14738)" was in fact **DESI DR1**
  (arXiv:2404.03002): 11/13 points matched the DR1 table digit-for-digit, and the
  anisotropic QSO point at z=1.491 had no official source at all (flagged, excluded).
  Corrected to the official DR2 Table 4 (verified digit-by-digit), with per-tracer
  DM–DH correlations. Single source of truth: `data/raw/desi_dr2_bao.csv` +
  `src/desi_dr2_data.py`; guardián layer R14 (6 checks) makes recurrence impossible.
- **Headline w₀wₐ tension recomputed** against the four official DR2 w₀wₐCDM
  posteriors (eqs. 25–28): **0.24σ (DESI+CMB+Pantheon+)**, 1.23σ (DESY5), 1.50σ
  (Union3), 1.52σ (no-SN) — honest range **0.2–1.5σ set by the SN compilation**
  (the old 0.05σ was DR1-based). Δw₀ = −0.04σ vs Pantheon+: essentially exact.
- **H₀ posterior (P2 reframe MCMC, corrected vector): 66.41 ± 0.39 km/s/Mpc**
  (1.43σ Planck). The ~40% tighter DR2 errors strain the raw dynamic-sector
  background (χ²_BAO 239→795); interpretation tracked for Paper 2.
- **Full Fase 4 (flat w₀/wₐ, corrected vector): SSEE algebraic point 1.31σ from joint w₀-wₐ posterior** — the
  rigidly fixed background still survives the blind full-likelihood test (where ΛCDM is excluded at 3.22σ).
- Propagated to all 12 documents + README + AUDIT + CANONICAL (4 retired patterns)
  + fig1_w0wa_plane regenerated with official DR2 contours. Old DR1-era chains
  (~10 GB) preserved on HDD as `*_DR1_superseded`.


## V3.6 — ω_m-direct reframe: MIRA matter factor dissolved (OP-8 closed) (2026-06-18)

- **OP-8 dissolved — no matter-rescaling factor.** The CMB matter density is now
  the standard physical observable ω_m = ω_b + ω_c + ω_ν, each piece algebraic in
  (φ, π): ω_b = (π−φ)/(3Ω²) = 0.02242, ω_c = KAL₀·ω_b·n_s = 0.11951 (forward
  identity, 0.41σ Planck), ω_ν = Σm_ν/93.14 = 0.000741. This gives the **derived**
  Ω_m,CMB = ω_m/h² = 0.30889 at the global background anchor H_alg = 3(φ+π)² =
  67.962. **Ω_m,dyn = 0.160 (DESI) and Ω_m,CMB (Planck) are now two independent
  predictions**, no longer linked by the "MIRA factor" (the earlier mapping
  Ω_m,CMB = Ω_m,dyn × MIRA = 0.3199 is retired). MIRA = 1.9989 survives only in the
  P9 screening fraction f_screen.
- **CMB ΔBIC (canonical):** full `plik` MCMC (TTTEEE+lowl+lensing, k=2 vs k=6,
  N=2354) gives χ²_BF = 2771.3 (SSEE) vs 2773.1 (ΛCDM) — indistinguishable fits —
  and **ΔBIC = −32.9** (parsimony-driven). Cross-checks: −24.0 (plik_lite, N=613),
  −35.0 (diagonal, N=5914). The earlier legacy-MIRA Cobaya −32.2 is superseded.
- **φ-DM canonical particle:** m_φ = Σm_ν·(SOLAR²·KRYSTOS) = 0.06849 eV × 594.28 =
  **41.02 eV** (retired 36.95 and 42.47); k_fs = **0.762 h/Mpc**; CLASS forward
  σ₈_eff = 0.748, **S₈ = 0.759 (0.04σ KiDS-1000)**; fσ₈ mean tension 0.70σ.
- **Growth:** G_growth = D₁_SSEE/D₁_ΛCDM = **1.003** (ΛCDM-consistent at the reframed
  Ω_m=0.30889; the earlier 0.979 carried a non-flat-background bug).
- **H₀ cascade (global anchor H_alg=67.962):** posterior 67.16±0.44; H_IR = 72.86
  (0.17σ SH0ES); H_UV = 73.040 (0.00σ); M = 9.68 meV (retired 8.81). H_MIRA=67.037
  dissolved.
- Entries below this point predate the reframe and record the project's history as
  it stood at the time (including the now-retired MIRA-mapping); they are left
  unchanged as a faithful record. Canonical current values live in
  `CANONICAL_VALUES.yaml`.

## V3.6 — Bibliography audit + Phase 1/2 hardening + repo cleanup (2026-05-16)

- **Bibliography audit (all 10 papers)**: 0 orphan bibitems, 0 undefined citations,
  0 bibtex warnings. All papers compile clean (0 LaTeX errors).
  - **P1 regression fixed**: a prior grep-based audit had deleted 10 bibitems flagged
    as orphans — they were in fact cited in `SSEE_EFT_section.tex` (an `\input` file
    the grep missed). All 10 restored (Eckart1940, Weinberg1971, Brevik2005,
    HiscockLindblom1983/1985, Muller1967, Maartens1996, Guth1981, Linde1982,
    Mukhanov1992); P1 back to 41 refs. Also fixed `\ref{app:derivation}` typo
    and added missing `\label{sec:w0wa}` in P2.
- **Phase 2 — foundational postulates (Paper 1 §2.4)**: D1/D2 analysed and formalised.
  - **Postulate D (Dimensional Anchor)**: SSEE predicts only dimensionless quantities;
    H₀ is the single dimensional input — identical status to ΛCDM. "Zero free
    parameters" = zero *dimensionless fitted* parameters. 3(φ+π)²≈67.96 recorded as
    a Type-P numerical coincidence; the absolute H₀ scale (H₀/M_Pl~10⁻⁶¹) is the
    cosmological-constant problem, beyond any framework.
  - **Postulate S (Saturation Correspondence)**: (Ω_DE, w₀) = (s, −s) with s=T_r/M_v;
    endpoints physically forced (s→0 Einstein-de Sitter, s→1 de Sitter). The identity
    1+w₀=Ω_m is the content of Postulate S, not an independent assumption.
- **Paper 6 — explicit φ-DM Lagrangian**: φ-DM modelled as a real scalar χ with
  S=∫√-g[-½(∂χ)²-½m_φ²χ²-½ξRχ²]. Dodelson-Widrow route excluded (mixing angle has
  no zero-parameter SSEE form, script `ssee_paperB_DW.py`); gravitational production
  adopted. Neutrino-detectability claims (KATRIN/PTOLEMY) removed — falsification
  channel is k_fs on the matter power spectrum. 22→24 pp.
- **Paper 9 — quantitative comparison section**: 7-axis comparison table vs EDE,
  SIDR, and late-DE transitions; +Aloni2022, +Kreisch2020. 16→18 pp.
- **Paper 4 — baryogenesis claim calibrated (D3)**: §3.2 header "Physical derivation"
  → "Sakharov-mechanism motivation (not a quantitative derivation)". The companion
  script back-computes the entropy-dilution factor — a consistency check, not a
  prediction; ab-initio η_B deferred to Paper B. OPEN_PROBLEMS OP-1 updated.
- **Hostile-referee sweep**: overclaim language reviewed across all 10 papers — suite
  is honest (most "first-principles" mentions are admissions of open limits).
  P5 Q1 consistency fix vs Postulate S.
- **Repository cleanup**: removed stray LaTeX artifacts (root + docs/); docs/ now holds
  exactly the 10 current paper PDFs + endorser brief; `.gitignore` adds `.obsidian/`,
  `eftcamb_ssee/` (857 MB external fork), and root-level `*.pdf`; README.md refreshed
  (page counts, OP-table status, m_φ channel, roadmap).

## V3.6 — Session 20: hi_class cross-check + Paper 3 update + endorser doc (2026-05-07)

- **CLASS/hi_class cross-check** (`src/ssee_paper3_hiclass_check.py`):
  - αK(z=0) = 0.4033 from CLASS background (es s_K, no la kineticidad α_K de P7; R54) — matches algebraic prediction to **Δ=0.005%**
  - αT=αM=αB=0 verified exact (minimal Horndeski construction)
  - Raw SSEE (Ωm,dyn=0.160) gives χ²_r=90.3 vs Planck PR4 — expected without MIRA mapping
  - ΛCDM reference (k=6): χ²_r=1.219 (confirms Planck fits standard cosmology)
  - Outputs: `fig_hiclass_TT.pdf`, `fig_hiclass_alpha.pdf`, `results/tables/hiclass_summary.txt`
- **Paper 3 updated** (`manuscript/SSEE_Paper3_CMB.tex`):
  - New §5.x "CLASS/hi_class cross-check of Bellini–Sawicki α-functions"
  - Added `Bellini2015` and `GW170817` to `ssee_paper3.bib`
  - Recompiled: **18 pages** (was 19 — minor reflow from new bib entries)
- **Endorser synthesis document** (`docs/SSEE_Endorser_Summary.tex/.pdf`):
  - 2-page LaTeX: table of 8 falsifiable predictions, 7-paper summary, explicit falsifiability section
  - Ready to send directly to Shafieloo, Lee, Di Valentino or new contacts
- **MCMC Paper 6 in progress**: 64 walkers × 15000 steps, ~2.47 it/s, background task bczkiso9t

## V3.6 — Session 19: Paper 6 MCMC (completo) + Paper 7 αK derivation (2026-05-07)

- **Paper 7 αK algebraic derivation**: New `\subsection{Algebraic determination of αK(a)}` added
  - For canonical K(X)=X (K_X=1, K_XX=0): αK(a) = 2X/(H²M_Pl²) = 3Ω_DE(a)[1+w_φ(a)]
  - At z=0: αK⁽⁰⁾ = 3×(Tr/Mv)×(BUFFER/Mv) = 3×0.840×0.1601 = 0.403 (fully algebraic, zero free params)
  - New Table: SSEE α-function predictions vs GW170817 constraints and Euclid forecasts
    - αT=0 exact (GW170817 <10⁻¹⁵ ✓), αM=0 exact, αB=0 exact, αK=0.403 (Euclid will probe)
  - Paper 7 recompiled: 13 p → **14 pages**
- **Paper 6 MCMC (full, 64 walkers × 15000 steps)**: `src/ssee_paper6_mcmc.py` (complete rewrite)
  - 3 free parameters: (Ω_φDM, k_fs, σ₈_in) — background algebraically fixed
  - Algebraic Gaussian priors: Ω_φDM = 0.1599 ± 0.020, k_fs = 0.493 ± 0.100, σ₈_in = 0.811 ± 0.006
  - Growth factor via full Heath integral D₁(z) ∝ E(z)∫da'/(a'E(a'))³
  - IS growth index γ_IS=0.554 from Paper 5; IS σ₈ suppression G=D₁_SSEE/D₁_ΛCDM^{0.55} applied
  - Soft transfer function T(k)=[1+(k/k_fs)^4]^(−5/4) (scalar condensate, not thermal WDM)
  - Data: 6 fσ₈ surveys (6dFGS, SDSS MGS, BOSS LOWZ, BOSS CMASS, eBOSS LRG, eBOSS QSO) + KiDS σ₈ + DES S₈
  - 4 output figures: corner (3×3), fσ₈ CI bands, σ₈/S₈ tension, trace plots
  - Convergence diagnostics: τ autocorrelation, N_eff, acceptance fraction, ΔBIC vs ΛCDM
- **Cross-paper audit**: `src/ssee_audit_consistency.py` — scans all 7 .tex + all .py with regex
  - Result: no critical inconsistencies; H₀ three values (67.96/66.75/66.66) documented as distinct contexts
- **README**: Updated — Paper 7 added, all 12 scripts listed, falsifiable predictions table expanded
- **CITATION.cff / CHANGELOG**: Updated to reflect 7-paper suite

## V3.6 — Session 18: Paper 6 φ-DM two-sector + Paper 7 EFT canonical (2026-05-07)

- **Paper 7 created**: `manuscript/SSEE_Paper7_EFT.tex` — 13 pages
  - Canonical action S = ∫d⁴x√(−g)[−X + V₀e^{β_c φ}]
  - β_c = −AURA = −(3φ+π)/2 = −3.9978 (algebraic exact)
  - Plateau test: 8 initial conditions → β_c = −3.98991 ± 0.00001 (Δ=0.199% systematic — Ω_b+Ω_r excluded)
  - αT = αM = αB = 0 exactly (minimal Horndeski G3=G5=0, G4=M_Pl²/2)
  - GW170817 compatible at machine precision
  - EFT verification script: `src/ssee_eft_verification.py`
- **Paper 6 Lyman-α defense**: New `\subsection{Compatibility with Lyman-α and WDM constraints}`
  - 3 steps: (1) non-thermal condensate → effective bound 0.1–0.5 keV; (2) k_fs=0.493 h/Mpc correct observable; (3) ΔP/P≈−f²(k/k_fs)² quantified prediction
  - Citation fix: Boyarsky2009 → Boyarsky2019 (key mismatch resolved)
  - Paper 6: 14 p → 15 pages; recompiled → `docs/SSEE_Paper6_phiDM.pdf`
- **Paper 6 G_2s=0.979**: adopted self-consistent two-sector (removed invalid WDM mechanism)
  - fσ₈ tension: 3.66σ → 0.50σ (6-survey mean); σ₈_eff=0.794, S₈_eff=0.820

## V3.6 — Session 17: Paper 5 IS causal perturbations complete (2026-04-28)

- **Paper 5 complete**: `manuscript/SSEE_Paper5_IS.tex` — 24 pages (commit 0a9d21c)
  - Q1: c²_s,eff = 0 exact (all modes stable in IS sector)
  - Q2: MIRA_num = 0.989 ± 0.017 (IS background origin confirmed, not perturbative)
  - Q3: γ_IS = 0.554 ± 0.001 (≈ γ_ΛCDM = 0.55; growth index IS sector)
  - Growth suppression G = D₁_SSEE/D₁_ΛCDM = 0.866 (13.4% suppression)
  - σ₈_SSEE = 0.702 ± 0.005; S₈_SSEE = 0.725 ± 0.005 (1.96σ KiDS / 2.84σ DES)
  - fσ₈(z=0.5) = 0.341 → 2.67σ vs BOSS (structural tension, Ω_m,dyn=0.160)
  - Script: `src/ssee_paper5_IS_perturbations.py`

## V3.6 — Session 13: ΔBIC consistency fix +218 → +206 (2026-04-26)

- **ΔBIC audit**: Detected discrepancy between script output (+206) and paper text (+218)
  - Root cause: paper table used lp_MAP=-124.87 from less-converged prior run; current run (N_eff=637,500) gives lp_MAP=-118.67 → ΔBIC=+206.19
  - The ΛCDM MAP (-14.19) was unchanged; full change came from improved SSEE MCMC convergence
  - Three ΔBIC values now clearly distinguished in script and docs:
    - [1] MCMC (k_SSEE=2 vs k_ΛCDM=3): +206 ← updated everywhere
    - [2] Framework (k_SSEE=0 vs k_ΛCDM=6): +192 ← noted in script (not in paper prose, avoids confusion)
    - [3] Dynamic sector (k=1 w₀,wₐ): −5.55 ← unchanged, SSEE favoured
  - Updated: Paper 2 table + all prose, README, AUDIT.md, CLAUDE.md, cover letters ×2
  - Paper 2 recompiled: 20 p → docs/SSEE_Paper2_draft.pdf
- **Script improvement**: `ssee_paper2_mcmc.py` now prints all three ΔBIC values with labels
- **README fix**: ΔBIC +206 → +218 stale value corrected; limitation item #7 added (ΔBIC TT+TE+EE+PP=+13.7)

## V3.6 — Session 12: Task 2B — Press-Schechter quantitative comparison (2026-04-26)

- **Task 2B completed**: Paper 4 §sec:deltac replaces "deferred to Paper 5" with computed values
  - New script `src/ssee_press_schechter.py`: numerically integrates D(z)/D(0), computes σ_M(M,z)
    via Eisenstein-Hu fit, evaluates PS ratio n_SSEE/n_ΛCDM = (δc_SSEE/δc_ΛCDM) × exp[…]
  - D(z=10)/D(0) = 0.1153 (Planck 2018 cosmology, flat ΛCDM)
  - Correction: σ_M≈0.5 at z=10 corresponds to M~10^12 M☉ (not 10^11 M☉ as stated before)
  - Results: M=10^11 M☉ → ×1.06; M=10^12 M☉ → ×1.41; M=3×10^12 M☉ → ×2.0
  - Honest conclusion: SSEE partially alleviates JWST tension but ~10–100× ΛCDM deficit remains
  - New figures: `results/figures/fig_press_schechter.{pdf,png}` (ratio vs σ_M and vs z)
  - New reference in Paper 4.bib: Boylan-Kolchin2023 (Nature Astronomy 7, 728)
  - Paper 4: 13 pages (was 12; +1 for Table 8 + eq:ps_ratio)
- **Internal audit session 11** (commits 7fbe5bc + 3e2918d): fixes C3–C7 + bonus macros (see session 11 entry)

## V3.6 — Session 11: Internal audit C3–C7 + bonus Paper 3 macros (2026-04-26)

- **C3**: Paper 1 r=0.0083 → 0.00813 (abstract + Predictive Register table); AUDIT.md ×3; README.md ×1
- **C4**: Paper 1 cluster table caption R_500 → R_200 (coherent with Paper 2 M1/M2 mass corrections)
- **C5**: Paper 3 χ²_r=0.131 → 0.122 (abstract + conclusions + abstracts_arXiv.txt)
- **C6**: Paper 2 prose "χ²_r=12.95" → 14.91 (KAL₀ only; coherent with sensitivity table)
- **C7**: Paper 2 fig2 caption Δχ²≈+85 → ≈+97 (coherent with table)
- **Bonus**: Paper 3 \SSEE and \LCDM macros undefined → added to preamble (silent pre-existing error)
- Papers recompiled: Paper 1 (11 p), Paper 2 (20 p), Paper 3 (17 p) → docs/
- All 4 papers audited; Paper 4 clean (r=0.00813 correct, M3 applied earlier)

## V3.6 — Session 9: Task 1C — Nine Sovereignties explicit table + Independence Appendix (2026-04-25)

- **Task 1C completed** (Paper 4 Theorem 2): replaced `= \ldots` ellipsis with explicit table of all 9 paths
  - Table~6 (`tab:sovereignties`): all 9 sovereignty names, named-constant formulas, expanded φ,π forms, values
  - Appendix A (`app:independence`): formal statement of independence — hierarchy-level vs formula-level;
    documents SOLAR=MAR and IGNIS=KRYSTOS algebraic equalities; explains why redundant pairs are retained
- **Fixed**: ICEBERG formula in `ssee-data.json` corrected from "MIRA + PYROS" → "MAR + PYROS"
- **Fixed**: Paper 4 params table — Ωb h² tension 2.1σ → 3.2σ; Y_p 0.2473 → 0.2476, tension 0.7σ → 1.7σ
- **Fixed**: Conclusion section — Y_p 0.2473 → 0.2476, updated tensions
- Paper 4 PDF recompiled → 12 pages (was 11) → `docs/SSEE_Paper4_ToE.pdf`

## V3.6 — Session 8: r_d numerical verification + Paper 3 §2.3 fix (2026-04-25)

- **Task 2A completed**: CAMB numerical verification of SSEE sound horizon vs Planck 2018 measured r_d
  - Case A (SSEE+MIRA, Ωb h²=0.02237): r_d = 147.156 Mpc → **0.25σ** from Planck (147.09 ± 0.26 Mpc) ✅
  - Case B (SSEE+MIRA+IS, Ωb h²=0.02285): r_d = 146.749 Mpc → 1.31σ ✅
  - Case C (SSEE dynamic, Ωm=0.160, no MIRA): r_d = 171.650 Mpc → 94.46σ ❌ (expected; MIRA essential)
  - θ* residual tension: 4.46σ in Case A (requires full D_A geometry match — linked to CMB likelihood blocker)
- **Script added**: `src/ssee_verify_rd.py` — standalone CAMB verification, arbiter = Planck observation
- **Paper 3 §2.3 fixed**: removed erroneous "r_d,eff = r_d × |w₀|" claim; MIRA resolves r_d directly
- **Paper 3 §4.1 fixed**: replaced "0.03% of ΛCDM reference" with "0.25σ of Planck 2018 measured r_d"
- **CHANGELOG/AUDIT fixed**: Ωb h² IS 0.02260 → 0.02285; wrong formula corrected to 3(π−φ)/200

## V3.6 — Session 7: Repo audit & documentation (2026-04-25)

- Repo structure: `docs/` reduced to 4 canonical PDFs (one per paper)
- Consolidated `docs/archive/` → `archive/` at root (eliminated nested archive)
- Fixed `manuscript/SSEE_Paper2_draft.pdf` removed from git tracking
- Cleaned root: removed `texput.log`; moved `mcmc_run.log` to `results/logs/`
- Updated AUDIT.md: Paper 4 section, IS Ωc h², Predictive Register table, ΔBIC two-question distinction
- Updated CHANGELOG, CITATION.cff, archive/README.md, data/README.md

## V3.6 — Session 6: Peer-review fixes 1B, 1F, 1G, 2C (2026-04-25)

- **Paper 2**: added "Two ΔBIC values — two physical questions" paragraph (ΔBIC=+218 background vs ΔBIC=−5.55 dynamic sector)
- **Paper 3**: added asymmetry paragraph (k=1 SSEE predictions vs k=6 ΛCDM fits; Zenodo timestamp)
- **Paper 1**: added Predictive Register table (w₀, wₐ, MIRA pre-DESI; Ωm, n_s, H₀ retrodictions; r future)
- **Paper 4**: Y_p BBN = 0.2473 (AlterBBN, Ωb h²=0.02285, 0.7σ); Ωc h² IS = 0.11926 (−0.6σ); δc = 1.6284 *(RETIRADO 2026-09-25 — OP-27: el colapso esférico sobre el fondo del modelo da 1.67634, ΛCDM-like)*
- **EFT section**: fixed 3 broken refs (eq:Pi→eq:zeta, DESI2025DR2→AbdulKarim2025, sec:constants→sec:axioms)
- **Paper 4 bib**: added Pisanti2008 (AlterBBN, doi:10.1016/j.cpc.2007.11.013)

## V3.6 — Paper 4: Algebraic ToE (2026-04-22)

- Added Paper 4: algebraic derivation of all CMB background observables from φ and π only
- Nine Sovereignties: 9 independent algebraic paths to 3(φ+π)
- Ωb h² derived: 3(π−φ)/200 = 0.02285 (3.2σ; Paper 4 §sec:baryons)
- Ωc h² IS: KAL₀ × Ωb h² × n_s = 0.11926 (−0.6σ)
- δc SSEE: δc,EdS × n_s = 1.6284 (linked to JWST early galaxy excess) *(RETIRADO 2026-09-25 — OP-27; el enlace JWST no sólo se cae, cambia de signo)*
- Y_p BBN: 0.2473 (AlterBBN, 0.7σ)
- Title revised to "Algebraic Derivation of CMB Background from φ and π"

## V3.6 — Paper 3: CMB Confrontation (2026-04-20)

- **MIRA hypothesis confirmed**: Ωm,CMB = Ωm,dyn × MIRA = 0.160 × 1.9989 = 0.3199 (within 0.63σ of Planck 0.3153)
- MIRA = (φ+β)/2, pre-existing in Genesis 5.12 as "Observational Frequency"
- CMB TT peaks with SSEE+MIRA: ℓ=221, 538, 815 (Planck: 220, ~540, ~810)
- χ²_r = 1.062 vs ΛCDM 1.043 over 1971 multipoles; ΔBIC(TT, k=1 vs k=6) = −40.3 (plik_lite)
- TT+TE+EE+PP lensing all computed; SSEE favoured in lensing (χ²_r=0.730 vs 0.757)
- Added `src/ssee_paper3_cmb.py` — full CAMB implementation with IS growth suppression (γ=φ⁻¹)
- Added `manuscript/SSEE_Paper3_draft.tex` — complete paper (Sections 1–7, 17 pages)

## V3.6 — Paper 2 (2026-04-20)

- Bayesian MCMC validation against DESI DR2 BAO + Planck 2018 + cluster masses (IGIMF-corrected)
- N_eff ≈ 637,500 (SSEE), 63,789 (ΛCDM), 43,793 (CPL); 100 walkers
- Full 13×13 DESI DR2 covariance matrix implemented
- Dynamic sector (w₀, wₐ): 0.05σ from DESI best-fit; ΔBIC = −5.55 (SSEE favoured)
- Full-model ΔBIC = +218 (background mismatch, not falsification; documented explicitly)
- H₀ = 66.75⁺⁰·⁴⁴₋₀.₄⁴ km/s/Mpc; χ²_r clusters = 0.122 (4 clusters)
- Added `manuscript/SSEE_Paper2_draft.tex` — 18 pages, submission-ready

## V3.6 — Paper 1 (2026-04-15)

- First derivation of SSEE algebraic constants from φ and π
- EFT section: Israel-Stewart viscosity framework, Ωc h² IS derivation
- Lagrangian action (phenomenological), σ8/S8 prediction via IS growth index γ=φ⁻¹=0.618
- Qualitative comparison with ΛCDM background

## V3.5 — Paper 2 draft

- Initial analytic comparison on w₀-wₐ plane
- Ω_DE chi-squared analysis vs DESI

## V3.0 — Paper 1 initial

- First derivation of SSEE algebraic constants from φ and π
- Qualitative comparison with ΛCDM background
