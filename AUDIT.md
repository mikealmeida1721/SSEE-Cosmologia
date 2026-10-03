# SSEE-V3.6 — External Audit Guide

**Author:** Mike Edison Almeida Vallejo  
**ORCID:** 0009-0008-2195-7836  
**Repo:** https://github.com/mikealmeida1721/SSEE  
**Date:** 2026-05-17 (10-paper suite — bibliography audit + Phase 1/2 hardening; Paper 1 Postulates D & S; OPEN_PROBLEMS OP-2/3/4/6 resolved, OP-1/5 partial)

> ⚠️ **Superseded numbers (reframe 2026-06-19 + ν-closure 2026-07-10).** This dated
> snapshot predates the **ω_m-direct reframe** (OP-8 dissolved: Ω_m,CMB = ω_m/h² =
> **0.30889**, no matter factor) and the **SOLAR²·KRYSTOS_V particle** with the unified
> ν-closure constant C=93.14: **m_φ = 40.70 eV, k_fs = 0.754 h/Mpc, S₈ = 0.758**
> (0.04σ KiDS). The Hubble cascade is H_alg = 67.962 → H_local = **72.86** (0.17σ);
> the canonical DR2 posterior is **H₀ = 67.79 ± 0.35** (ω_m algebraic fixed, R25 2026-07-25;
> the 67.95 froze Ω_m and biased the posterior toward the anchor).
> For canonical values see `README.md`, `CANONICAL_VALUES.yaml`,
> and `VERIFICATION_LEDGER.md`. The headline table below is updated; deeper body
> prose retains the 2026-05-17 figures as the record of that audit.

---

## What this framework claims

SSEE-V3.6 (Structural Self-Energy Expansion) is a **minimal-parameter** dark energy model
(~3 effective parameters vs. 6 for $\Lambda$CDM). The shape of the background sector is derived
algebraically from two constants: the golden ratio φ and π. No fitting to data is performed to
obtain the central predictions of that core; the absolute vacuum scale enters as a single measured
input (Postulate D), and the dark-matter-origin extensions are tracked as open problems.

Falsifiable predictions — fixed by algebraic construction, not fitted (Structural Constant Dictionary, Zenodo: 10.5281/zenodo.20684908). Agreement with already-public data below is a parameter-free postdiction; no claim of temporal priority over public data is made.

| Observable | SSEE prediction | Observed | Status |
|---|---|---|---|
| (w₀, wₐ) | (−0.840, −0.670) | DESI DR2+CMB+Pantheon+: (−0.838±0.055, −0.617±0.208) | 0.24σ (2D); 0.2–1.8σ across SN compilations (official chains) |
| CMB peak ℓ₁ | 221 | Planck PR4: ~220 | Δℓ = 1 |
| Ωm,CMB | 0.30889 (= ωm/h², ωm-direct) | Planck 2018: 0.3153 | 0.88σ |
| n_s | 1 − φ⁻⁷ = 0.96556 | Planck 2018: 0.9649 | 0.16σ |
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7559 ± 0.0189` (0.10σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.04σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
| ~~m_φ (φ-DM mass)~~ | ~~40.70 eV algebraic~~ | — | **RETRACTED 2026-08-01** |
| k_fs | 0.754 h/Mpc algebraic | DESI Y3/Euclid P(k): 2026–2028 | Future prediction |
| (w₀, wₐ) vs DESI DR3 | same fixed point (−0.840, −0.670) | DR3 w₀wₐCDM (2027): trajectory 0.05σ (DR1) → 0.24σ (DR2, errors −40%); expect ~0.5σ if centrals persist; >3σ joint exclusion falsifies | **Pre-registered prediction** |
| r (tensor-to-scalar) | φ⁻¹⁰ = 0.00813 | LiteBIRD (~2032) | Future prediction |

---

## Repo structure

```
SSEE/
├── manuscript/                     — LaTeX sources (authoritative)
│   ├── SSEE_Paper1_Framework.tex … SSEE_Paper10_UVCompletion.tex  — the 10 papers
│   ├── SSEE_EFT_section.tex         — EFT section (\input by Paper 1)
│   ├── SSEE_appendix_Friedmann.tex  — Friedmann-derivation appendix
│   ├── SSEE_Unified_Journal.tex     — consolidated journal paper (Papers 1–7)
│   ├── SSEE_Endorser_Summary.tex    — 2-page arXiv endorser brief
│   └── *.bib                        — ssee_paper3/5/6, SSEE_Paper4, ssee_unified
├── src/                             — Python scripts, organized per paper
│   ├── p02_mcmc/ … p10_uv/          — per-paper analysis, MCMC, figures (one dir per paper)
│   ├── pB_inflation/                — Paper B groundwork (baryogenesis DW, N_*)
│   ├── estadistica/                 — Bayesian model-selection (DIC, Savage-Dickey, cross-val)
│   ├── mcmc_full/                   — full Cobaya CAMB+PPF pipeline (heavy chains → /mnt/datos)
│   ├── verificacion/                — ssee_verify.py guardian + CANONICAL sync
│   └── ssee_core.py                 — single algebraic source (φ, π → all constants)
├── class_ssee/                      — CLASS Boltzmann fork — SSEE .ini configs + plots
│   ├── ssee_v36.ini                 — SSEE MIRA sector (Ω_m=0.3199)
│   ├── ssee_v36_nomira.ini          — SSEE dynamic sector only (Ω_m=0.160)
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7559 ± 0.0189` (0.10σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.04σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
│   ├── ssee_v36_twosector.ini       — φ-DM two-sector (ncdm m=40.70 eV)
│   └── ssee_v36_IS.ini              — IS viscosity (cs2_fld=0.001)
├── data/                            — observational data (DESI DR2, Planck PR4, clusters)
├── results/                         — generated figures, tables, logs
├── docs/                            — compiled PDFs: 10 papers + endorser + unified journal
├── notebooks/ · submission_packages/ · archive/
├── README.md · CHANGELOG.md · OPEN_PROBLEMS.md · CITATION.cff
└── AUDIT.md                         — this file
```
*(`eftcamb_ssee/` — EFTCAMB fork — is not versioned; clone separately.)*

---

## How to reproduce the results

### Prerequisites
```bash
pip install -r requirements.txt      # numpy scipy matplotlib emcee corner camb cobaya classy getdist astropy pyyaml
```

**Portability.** All in-repo paths are derived from each script's own location — no
hardcoded absolute paths, so the suite runs unchanged from any clone. Heavy MCMC
outputs default to a large disk if one is mounted, else to `results/data/`; override
with `export SSEE_DATA_DIR=/path/to/disk`. The optional Obsidian-vault sync
(`memory_sync.py`) reads `SSEE_VAULT` (default `~/SSEE-Vault`) and is skipped if absent.

### Paper 2 — MCMC validation
```bash
python3 src/p02_mcmc/ssee_paper2_mcmc.py
```
Runtime: ~30–60 min (N_eff ≈ 637,500 for SSEE, 100 walkers × 25,000 steps).

Expected output:
```
H₀ = 67.79 ± 0.35 km/s/Mpc  (DR2, ω_m algebraic fixed R25; 0.66σ Planck, 0.50σ anchor)
χ²_r clusters = 0.122  (4 clusters, IGIMF-corrected, MCMC)
χ²_r clusters = 0.126  (7 clusters, analytic sample)
χ²_2D (w₀-wₐ vs DESI DR2+CMB+Pantheon+) = 0.42 → 0.24σ (rango 0.2–1.8σ según compilado SN, ρ medidos de cadenas oficiales; ver V-L4-DESI)
ΔBIC (dynamic sector, k_SSEE=2 vs k_ΛCDM=3) = −6.43  [SSEE favoured; CPL −6.35]
ΔBIC (full background, k=0 vs k_ΛCDM=6) = +206        [framework penalty]
```

### Paper 3 — CMB power spectrum
```bash
python3 src/p03_cmb/ssee_paper3_cmb.py
```

Expected output:
```
TT: SSEE χ²_r=1.042  |  ΛCDM χ²_r=1.043  (N=1971)
TE: SSEE χ²_r=1.040  |  ΛCDM χ²_r=1.040  (N=1967)
EE: SSEE χ²_r=1.040  |  ΛCDM χ²_r=1.039  (N=1967)
PP: SSEE χ²_r=0.720  |  ΛCDM χ²_r=0.757  (N=9)    [lensing — SSEE favoured]
ΔBIC (full plik MCMC, TTTEEE+lowl+lensing, k=2 vs k=6, N=2354) = −33.83 (results/logs/b1_k2.json, 2026-10-01)  [canonical — SSEE decisively favoured]
ΔBIC (plik_lite point est., TTTEEE, k=2 vs k=6, N=613) = −24.0          [cross-check]
ΔBIC (diagonal, TT+TE+EE+PP, k=2 vs k=6, N=5914) = −35.0                [cross-check]
Peak positions: ℓ = 221, 538, 815
```

CLASS cross-check (αK Bellini-Sawicki): el script de mayo (`archive/codigo/investigacion/huerfanos_2026-10-02/ssee_paper3_hiclass_check.py`) quedó
ARCHIVADO el 2026-10-02: metía Ω_m,dyn = 0.160 en CLASS y su «Δ = 0.005 %» era la misma
sustitución dos veces. El hi_class vigente es la etapa DVC `hiclass_campo`
(`src/p07_eft/hiclass_campo.py`), que P7 cita por `\val`.

### Paper 4 — Press-Schechter δc comparison
```bash
python3 src/p02_mcmc/ssee_press_schechter.py
```
Expected output:
```
δc(SSEE) = 1.67634  (colapso esférico; el 1.6284 = δc,EdS × n_s está RETIRADO, OP-27)
δc(ΛCDM) = 1.67599
M [M☉]      σ_M(z=10)    n_SSEE/n_ΛCDM
1.00e+11      1.0104       0.990
3.00e+11      0.7267       0.976
1.00e+12      0.5064       0.945
```

### Paper 5 — Israel-Stewart causal perturbations
```bash
python3 src/p05_IS/ssee_paper5_IS_perturbations.py
```
Expected output:
```
c²_s,eff = 0 (exact algebraic)
R = Om_m,eff/Om_m (k≥10) = 0.9897 ± 0.0167   [cota: la EO no se agrupa;
                                    antes «MIRA_num», contra un blanco retirado]
γ_IS = 0.5504 ± 0.0003             [≈ γ_ΛCDM = 0.55]
G = D₁_SSEE/D₁_ΛCDM = 1.0032       [~0.3% enhancement; Poisson source Ω_m,CMB=0.30889]
σ₈_SSEE = 0.8136 ± 0.006           [single-sector ODE; CLASS top-hat ceiling 0.8149]
S₈_SSEE = 0.8256 ± 0.006           [single-sector; ceiling 0.827 — see note below]
S₈ tension SSEE vs DES-Y3 = 2.74σ  [single-sector baseline; see note below]
```
> **Nota (2026-09-08).** Estas dos líneas decían «resolved by Paper 6
> two-sector» y «Paper 6 two-sector → S₈=0.758». Ese sector se **retiró el
> 2026-08-01** junto con la partícula, así que el documento citaba como
> vigente una solución muerta. Y no hacía falta ninguna solución: el techo
> 0.827 y su «2.7σ» salen de **fijar A_s al valor de Planck**, y A_s es uno
> de los dos libres del modelo. Con A_s libre contra el ξ± crudo de KiDS-1000
> el mismo sector único da **S₈ = 0.7559 ± 0.0189, 0.10σ** (Paper 6, R3;
> log `results/logs/growth_2026-07/R3_ssee_kids_S8_rehecho.json`). El techo se
> conserva como diagnóstico bajo condición declarada, no como predicción.

### Paper 6 — 🔴 **RETIRADO 2026-08-01: NO forma parte de la auditoría**

El sector φ-DM y la partícula `m_φ = 40.70 eV` fueron **retirados**. Los tres
scripts que estaban aquí (`ssee_paper6_verification.py`, `..._mcmc_grid.py`,
`..._mcmc_v2.py`) viven en `archive/codigo/p06_phiDM_RETIRADO_2026-08-01/` y
**no se corren como parte de la auditoría**: modelan un sector que ya no existe.

Lo que **sí** se audita de Paper 6 es el resultado canónico contra dato crudo,
un solo sector y `A_s` libre:

```
KiDS-1000 (A_s libre, 225 puntos):
  S₈ = 0.7559 ± 0.0189   →  0.10σ vs KiDS-1000 (0.759 ± 0.024)
  σ₈ = 0.7449 ± 0.0186
  χ²_min = 265.4 / 216 dof
  log: results/logs/growth_2026-07/R3_ssee_kids_S8_rehecho.json

KiDS-Legacy (A_s CLAVADO al del CMB — CERO libres cosmologicos, 357 puntos)
  — este es el TITULAR vigente desde 2026-09-20:
  S₈ = 0.8273 predicho  vs  0.8265 ± 0.0176 medido  →  0.04σ
  χ²_min = 417.971 / 357 puntos, 8 libres (todos nuisance)
  logA de la cizalla = 3.0255 ± 0.0396  →  0.49σ del 3.04483 que fija el CMB
  control con fondo Planck igual de rigido: 1.01σ · χ²=418.955
  log: results/logs/kids_legacy_sseefijo.log
  CAUTELA que el auditor debe verificar: los tres χ² caben en 1.0 sobre 357
  puntos ⟹ la cizalla NO discrimina entre los modelos. Lo que separa es el
  conteo de parametros. Y KiDS-Legacy es de 2025-03-25: NO hay prioridad temporal.
```
~~Expected output (verification):~~ 🔴 **HISTÓRICO — los dos bloques de abajo
son la salida esperada de la partícula RETIRADA el 2026-08-01. NO se verifican:
describen un sector que ya no existe. Se conservan para que quien audite
reconozca estos números si los encuentra en un documento viejo.**
```
m_φ = 40.70 eV = Σm_ν × (SOLAR²·KRYSTOS_V)  (algebraic, zero free parameters)
k_fs = 0.754 h/Mpc  (falsable DESI Y3/Euclid 2026–2028)
Ω_CDM = 0.160050
Ω_φDM = 0.148844
Ω_total = 0.308895 ≈ Ω_m,CMB (ω_m-directo)
σ₈_eff = 0.7470  (CLASS forward two-sector, free-streaming)
S₈_eff = 0.7580  (0.04σ KiDS-1000 — resuelve tensión S₈)
Mean fσ₈ tension: 0.93σ two-sector (σ₈=0.747)  [single-sector 0.70σ; ΛCDM 0.73σ]
```
Expected output (MCMC v2, emulador CLASS):
```
Ω_φDM = 0.165  (0.24σ del algebraico 0.14889)
m_φ   = 51.9 eV (0.67σ del algebraico 40.70)
S₈    = 0.782
ΔBIC = −14.3  [SSEE favoured]
```

### Paper 7 — 🔴 **βc RETIRADO 2026-09-07: NO forma parte de la auditoría**

`βc` fue retirado de Paper 7 junto con el potencial y el acoplamiento conformal
(§withdrawn, L80): el Lagrangiano vigente `K = c₁X + c₂X²` no lleva ninguno de
los dos. El script del test de meseta está en
`archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/` con el README que
explica los tres errores que arrastraba. **No se corre.**

Lo que sigue abierto es **OP-23**, y es otra pregunta: ningún fondo reproduce
`wₐ = −0.670`. Su investigación viva está en `src/p07_eft/`.
Expected output:
```
βc = −3.990 ± 0.001  (8 initial conditions)
AURA = (3φ+π)/2 = 3.997847
Gap = 0.199%  [attributed to Ωb+Ωr excluded from background]
αT = αM = αB = 0 (exact)
αK(0) = 0.4033 (algebraic)
```

### CLASS Boltzmann — MIRA test and two-sector P(k)

```bash
# Build CLASS (requires gfortran + python3-dev):
cd class_ssee && make
# Run MIRA vs no-MIRA comparison:
./class ssee_v36.ini && ./class ssee_v36_nomira.ini
python3 plot_ssee_cmb.py
```

Expected output (peak positions):
```
SSEE+MIRA:   ℓ₁=220  ℓ₂=535  ℓ₃=810   RMS vs ΛCDM = 1.4%
SSEE no-MIRA: ℓ₁=240  ℓ₂=597  ℓ₃=922   RMS vs ΛCDM = 31.5%
```
*Without MIRA, all three CMB peaks shift ~10% and RMS rises 22×.*

Two-sector P(k) calibration:
```bash
./class ssee_v36_twosector.ini
python3 calibrate_wdm_alpha.py
```
Expected (legacy α_WDM fit-to-KiDS): α_WDM = 1.6561 h/Mpc, σ₈_eff = 0.737.
> **Superado:** el valor canónico es el **forward** two-sector de CLASS
> (σ₈_eff = 0.747, S₈ = 0.758), salida directa sin fitear α_WDM. La calibración
> `calibrate_wdm_alpha.py` se conserva solo como registro del método retirado.

IS viscosity test:
```bash
./class ssee_v36_IS.ini && python3 plot_IS_viscosity.py
```
Expected: cs² effect on σ₈ = 0.03% (negligible); G = D₁_SSEE/D₁_ΛCDM = 1.0032
(canonical Poisson source Ω_m,CMB=0.30889; the retired 0.866 used the bare Ω_m,dyn=0.160).

### OP-5 — HMcode-2020 baryonic feedback (requires CLASS + classy)

`archive/codigo/investigacion/open_problems/ssee_op5_hmcode.py` needs CLASS compiled with the Python wrapper and
HMcode-2020 enabled. A bare `pip install classy` does **not** enable
HMcode-2020 — the local CLASS build is required:
```bash
cd class_ssee && make
cd python && python setup.py install
# Verify HMcode-2020 is available:
python -c "from classy import Class; c=Class(); c.set({'non_linear':'hmcode','hmcode_version':'2020_baryonic_feedback'})"
```

### MCMC Fase 4 — multi-probe background

5 parameters (H₀, w₀, wₐ, Ωm, r_d); 100 walkers × 11,000 steps; N_eff = 4,402.

Expected output (corrected DESI DR2 vector, V-L4-DESI; run 2026-07-02):
```
H₀    = 66.84 ± 0.91    (algebraic: 67.96,   tension: 1.23σ)
Ω_b h² = 0.02237 ± 0.00015 (algebraic: 0.02237, tension: 0.01σ)
Ω_m   = 0.3241 ± 0.0125  (algebraic: 0.30889, tension: 1.21σ)
w₀    = −0.740 ± 0.126   (algebraic: −0.840,  tension: 0.79σ)
wₐ    = −0.839 ± 0.458   (algebraic: −0.670,  tension: 0.37σ)
Mean tension (5 params): 0.72σ  (BLIND: flat w0/wa priors; max 1.23σ H₀)
```

---

## Known limitations — full disclosure

### 1. H(z) tension (Paper 2, §Results)
SSEE χ²_r(H(z)) = 1.861 vs ΛCDM = 0.458.
Genuine tension (4× worse), not a calibration artefact. Paper 2 states this explicitly.
Physical explanation: SSEE's modified expansion history shifts H(z) predictions systematically.

### 2. ΔBIC = +206 (Paper 2, §BIC) — background penalty
Applies BIC within the standard Friedmann framework, penalising SSEE's modified background
against ΛCDM's 6 fitted parameters. Paper 2 explicitly distinguishes this from the
dynamic-sector test (ΔBIC = −5.55, SSEE favoured). These address different physical questions.

### 3. CMB pipeline — canonical result and H0-anchoring sensitivity (Paper 3)

**Canonical CMB result (Paper 3 §5, ω_m-direct reframe):** at the algebraic global anchor
H0 = 3(φ+π)² = 67.962, the full `plik` MCMC (TTTEEE+lowl+lensing, N=2354) gives
ΔBIC = −33.83 (k=2 vs k=6) — decisively favours SSEE. Cross-checked by the `plik_lite`
point estimate (−24.0, N=613) and the diagonal approximation (−35.0, N=5914); all three
agree. *(The earlier legacy-MIRA `plik_lite` Cobaya scan — H0=67.066 optimum, ΔBIC≈−31.3 —
is superseded by the reframe.)*

**Illustrative H0-anchored comparison** (`results/tables/planck_fulllike_results.txt`):
When H0 is fixed to a DESI-BAO-calibrated value instead of the CMB-preferred anchor, ΔBIC
rises sharply — this is NOT a contradiction, it decomposes into the H0-offset penalty plus
the small intrinsic w0/wa effect. The file is explicitly labelled as illustrative; the
primary result is the canonical ΔBIC = −33.83.

**k count fixed** (BC2): SSEE uses k=2 in all CMB comparisons (H0 + Ωb h² prior borrowed
from Planck). k=0 counting appears only in the illustrative file with matching caveat.

**Parameter table** (authoritative):

| Parameter | Status in SSEE | k contribution |
|---|---|---|
| w₀, wₐ | algebraic (Zenodo pre-data) | 0 |
| n_s | algebraic (1−φ⁻⁷) | 0 |
| Ωm,CMB | algebraic (ω_m-direct = ω_m/h²; OP-8 dissolved) | 0 |
| H₀ | scanned to CMB minimum | 1 |
| Ωb h² | fixed to Planck prior | 1 (conservative) |
| τ, As | fixed to Planck priors | 0 (conservative option: +2) |
| **Total SSEE** | | **k=2** (k=4 hyper-conservative) |
| **ΛCDM baseline** | | **k=6** |

Diagonal covariance gives ΔBIC = −35.0 (canonical ω_m-direct fit, N=5914; cross-check of the −33.83 full-plik headline).
Full plik/CamSpec likelihood with official off-diagonal Planck covariance matrix remains a refinement for PRD/PRL.

### 4. Two-sector Ωm (Papers 2, 3, 5, 6) — ω_m-direct reframe (OP-8 dissolved)
Ωm,dyn = 0.160 (DESI dynamic sector) and Ωm,CMB = 0.30889 (Planck) are **two independent
algebraic predictions**, NOT linked by any matter factor. Ωm,CMB = ω_m/h² with
ω_m = ω_b + ω_c + ω_ν, where ω_b = (π−φ)/(3Ω²) = 0.02242 and ω_c = KAL₀·ω_b·n_s = 0.11951
(a forward identity already in Paper 1). The earlier MIRA-mapping bridge
(Ωm,CMB = MIRA·Ωm,dyn = 0.3199) is **RETIRED** (OP-8 dissolved, 2026-06 reframe).

### 5. MIRA — status and provenance (BC3)

**Formal status:** MIRA = (3φ+π)/4 = 1.998924 is a **phenomenological auxiliary hypothesis**
(not yet a derived quantity). Following the ω_m-direct reframe it **no longer bridges Ωm**
(OP-8 dissolved); it now enters only the Hubble screening of Paper 9,
f_screen = αK/(3·MIRA) = 0.06725. Its derivation from first-principles field equations
(OP-8) remains open. It is NOT simultaneously a free parameter and a derived quantity —
it is a fixed hypothesis whose anti-post-hoc guarantee rests on **algebraic rigidity, not
chronology**:

MIRA = (3φ+π)/4 is fixed by construction (Structural Constant Dictionary,
Zenodo: 10.5281/zenodo.20684908); it has no adjustable amplitude that could be tuned to
the CMB fit. We make no claim of temporal priority over the public Planck/DESI releases,
which predate this work.

This status (hypothesis pending formal derivation) is stated explicitly in Papers 1, 3, 5, 6.
All MIRA-dependent claims are sector-specific and conditional on this hypothesis.

### 6. Israel-Stewart perturbations (Papers 5, 6)
Full causal IS (Hiscock-Lindblom 1985) perturbation theory is implemented for background sector.
B-mode LiteBIRD forecasts requiring IS tensor perturbations remain future work.

### 7. Ωc h² (Paper 4)
Static Eckart: 3.7σ tension. IS derivation: KAL₀ × Ωb h² × n_s = 0.11926 → −0.6σ.
Note: Ωb h² algebraic = (π−φ)/(3Ω²) = 0.02242 (0.32σ from Planck — see OPEN_PROBLEMS OP-1; the earlier 3(π−φ)/200 form is superseded).

### 8. φ-DM mass scale and field content (Paper 6)
m_φ = 40.70 eV is not keV-scale WDM; φ-DM is modelled as a real scalar field (explicit
Lagrangian in Paper 6 §4) populated by gravitational particle production. The
Dodelson-Widrow (sterile-neutrino) route is excluded — its mixing angle has no
zero-parameter SSEE form. φ-DM has no Standard-Model portal, so it is not accessible
to neutrino-mass experiments; free-streaming suppression enters observation via
k_fs = 0.754 h/Mpc, not direct m_φ. Lyman-α bounds apply to thermal relics; the
scalar fraction f_φ ≈ 0.50 gives an effective ~0.1–0.5 keV equivalent — within
observational bounds. Quantified in Paper 6 §Lyman-α. The ab-initio relic abundance
from the gravitational-production integral is deferred to Paper B.

---

## What would falsify SSEE

1. CMB peak ℓ₁ outside 221 ± 3 by more than 2σ in a new measurement
2. DESI DR2+ requiring Ωm > 0.20 in the dynamic BAO sector
3. ~~S₈ measured above 0.85 by Euclid weak-lensing (two-sector φ-DM predicts S₈ ≈ 0.76)~~ — **retired 2026-08-01** with the second sector; the live single-sector figure is S₈ = 0.7559 ± 0.0189
4. k_fs cutoff absent or at significantly different scale in Euclid/DESI Y3 P(k) (2026–28)
5. Tensor-to-scalar ratio r ≠ φ⁻¹⁰ = 0.00813 measured by LiteBIRD (~2032)
6. |w₀ + 0.840| > 3σ confirmed by DESI DR5 or Euclid

---

## Predictive Register — structural-rigidity defence

Agreement with **already-public** data is a parameter-free **postdiction**: the values
are fixed by algebraic construction, but the data predate this work. **No claim of
temporal priority over public data is made** — the defence is the structural rigidity of
the closed dictionary. Genuine pre-committed predictions concern **unreleased** data
(DESI DR3, Euclid, LiteBIRD); see the Prediction Register at the dictionary DOI.

| Quantity | Algebraic formula | Value | Test dataset | Status |
|---|---|---|---|---|
| w₀ | −Tr/Mv | −0.8399 | DESI DR2 (2025) | Parameter-free postdiction |
| wₐ | −Psc/Kv | −0.6699 | DESI DR2 (2025) | Parameter-free postdiction |
| MIRA | (3φ+π)/4 | 1.9989 | f_screen (P9) | Structural |
| Ω_m,CMB | ω_m/h² (ω_m-direct) | 0.30889 | Planck 2018 | Postdiction |
| n_s | 1 − φ⁻⁷ | 0.96556 | Planck 2018 | Postdiction |
| H₀ | 3(φ+π)² | 67.962 | Planck 2018 | Postdiction |
| r_d | CAMB, ω_m-direct Ω_m,CMB=0.30889 | 147.17 Mpc | Planck 2018: 147.09 ± 0.26 Mpc | 0.3σ postdiction |
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7559 ± 0.0189` (0.10σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.04σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
| ~~m_φ~~ | ~~Σm_ν × SOLAR²·KRYSTOS_V~~ | ~~40.70 eV~~ | — | **RETRACTED 2026-08-01** — no longer a prediction of the model |
| k_fs | free-streaming (m_φ) | 0.754 h/Mpc | DESI Y3/Euclid 2026–28 | Future prediction (cond. OP-9) |
| r | φ⁻¹⁰ | 0.00813 | LiteBIRD (~2032) | Future prediction |

Constant dictionary repo: https://github.com/mikealmeida1721/SSEE-Constant-Dictionary
Zenodo DOI (concept): https://doi.org/10.5281/zenodo.20684908

---

## Open blockers (path to PRD/PRL)

| Blocker | Description | Status |
|---|---|---|
| **B1** | full `plik` MCMC done (ΔBIC=−33.83, canonical); plik_lite cross-check −24.0; full CamSpec off-diagonal covariance pending | Weeks |
| **B2** | Full causal IS tensor perturbations (Hiscock-Lindblom 1985) — B-mode forecasts | Months |
| **B3** | MIRA: geometric derivation given in Paper 8 (disformal geodesic); full field-equation closure partial | Months |
| **B4** | arXiv endorsement — deferred by choice (journal-first strategy, see README) | External |
