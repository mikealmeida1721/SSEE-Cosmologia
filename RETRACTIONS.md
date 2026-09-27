# Retractions — SSEE cosmology

Results that earlier versions of this project reported and that are withdrawn.
Each entry says what was claimed, why it fell, and what replaces it. They are kept
because a reader who met the older numbers (Zenodo versions up to 2026-07-20, older
README revisions) should be able to see exactly what changed and why.

| Withdrawn | Date | Why | Replaced by |
|---|---|---|---|
| Second dark-matter sector Ω_φDM = 0.14889 and the particle m_φ = 40.70 eV (with k_fs = 0.754 h/Mpc, α = 1.117, σ₈/S₈ two-sector 0.747/0.758, multiplier 594.28) | 2026-08-01 | Ω_φDM came from subtracting 0.160 from Ω_m = 0.308881, and 0.160 is 1+w₀, a number from the equation of state, not a density. The S₈ tension it was built to close does not exist in the raw shear data | One matter sector, Ω_m = 0.308881 (Paper 6) |
| "3.5σ S₈ challenge" | 2026-08-01 | Measured against the compressed S₈ statistic with A_s fixed to Planck, i.e. importing the Planck–KiDS offset | S₈ = 0.8273 predicted vs 0.8265 ± 0.0176 (KiDS-Legacy, A_s fixed by the model's own CMB fit) |
| Ω_m,dyn = 0.160 used as a matter density in the background | 2026-07-09 | 0.160 is 1+w₀; the geometry takes the total Ω_m | Ω_m = ω_m/h² = 0.308881 |
| Exponential potential and conformal coupling β_c = −AURA (Paper 7) | 2026-09-07 | The shooting normalised the field density to \|w₀\| = 0.839950 instead of the density fraction 0.691119; with the correct target the coupling is −2.194210, and the potential is not needed | Two-term k-essence K(X) = c₁X + c₂X² (Paper 7) |
| α_K(z=0) = 0.4033 as the kineticity | 2026-09-06 | 0.403302 is s_K = 3(−w₀)(1+w₀), a pure equation-of-state quantity | α_K(z=0) = 15.591335 (Paper 7); s_K enters f_screen |
| Local H₀ = 72.86 km/s/Mpc from H_alg | 2026-09-06 | A pure number, 3(φ+π)², cannot be the input of a dimensional cascade | SH0ES is the input: H_glob = 73.04 × (1 − 0.069522) = 67.962142 km/s/Mpc (Paper 9–10) |
| δc = δc,EdS × n_s = 1.6284 and the JWST halo "enhancement" | 2026-09-25 | The threshold was not derived from spherical collapse on the model background | δc = 1.67634; no enhancement (OP-27) |

---

## The README text as it stood before 2026-09-26

Moved here verbatim when the README was rewritten to lead with the current model.

### Retraction banner (formerly under the predictions table)

> 🔴 **Retracted 2026-08-01 — the φ-DM sector and its particle (m_φ = 40.70 eV,
> k_fs = 0.754 h/Mpc).** Two independent reasons. (1) The subtraction defining its
> density, Ω_φDM = Ω_m,CMB − Ω_m,dyn = 0.308881 − 0.160, mixed a measured density
> with a number from the **equation of state** (0.160 = 1+w₀) — dimensionally well
> formed, physically empty, so the particle had nothing to be made of. (2) The S₈
> tension it was built to close does not exist in the raw data: it appeared only
> against the *compressed* S₈ statistic (itself derived under ΛCDM) with A_s fixed
> to Planck. Fitted directly to the 225 raw KiDS-1000 ξ± points with A_s free and a
> **single** matter sector, SSEE gives S₈ = 0.7555 ± 0.0192 — **0.11σ**. See Paper 6.
>
> **Closed 2026-09-20 against KiDS-Legacy** (357 raw ξ± points; Wright et al.
> 2025, [arXiv:2503.19441](https://arxiv.org/abs/2503.19441) — published sixteen
> months before this analysis, **no temporal priority is claimed**). The shear
> asks for log(10¹⁰A_s) = 3.0255 ± 0.0396 against the 3.04483 the CMB fixes
> *under the same algebraic background*: **0.49σ** (Planck background, held
> equally rigid: 1.01σ). So A_s need not be refitted at all — fixing it costs
> nothing (χ² = 417.97 with **eight free parameters, all nuisance, none
> cosmological**, vs 418.34 with A_s free; ΔBIC = +6.24), and S₈ = 0.8273
> becomes a *prediction* against 0.8265 ± 0.0176 measured. **Two cautions, in
> the open:** the three χ² compared span 1.0 over 357 points, so the shear does
> **not** discriminate between these models — what separates them is the
> parameter count; and KiDS-1000 had asked for log(10¹⁰A_s) = 2.863 ± 0.051,
> 3.5σ away, with the two releases differing from each other by 2.5σ. What
> changed is the data (the n(z) calibration, by the collaboration's own
> Appendix I), not the model. A future release returning to the lower
> amplitude would reopen the sector.

### Paper 5 section (S₈ ceiling row and diagnostic)

| **S₈_SSEE (ceiling, A_s FIXED to Planck)** | **0.827** | the old "3.5σ KiDS challenge" — an artefact of fixing A_s (now 2.7σ). The two-sector answer is RETIRED (2026-08-01); with A_s free: 0.7555, 0.11σ |
| Mean fσ₈ tension (6 surveys, single-sector) | 0.70σ | the two-sector variant (0.93σ) is RETIRED with the particle (2026-08-01); canonical fσ₈ vs raw BOSS is pending (R1/R2) |

**Diagnostic:** with A_s *fixed* to Planck the model predicts an S₈ above weak-lensing surveys.
That gap was RETIRED as an artefact on 2026-08-01: A_s is a free parameter of the model (k=2), and with A_s free the MCMC against raw KiDS-1000 ξ± gives S₈ = 0.7555 ± 0.0192 — **0.11σ, no tension**. The two-sector φ-DM extension that formerly closed it (S₈ = 0.758) is RETIRED. **Update 2026-09-20:** against KiDS-Legacy the amplitude the shear asks for lands 0.49σ from the one the CMB fixes under the same background, so A_s need not be free either — fixed, the sector predicts S₈ = 0.8273 against 0.8265 ± 0.0176 measured, with **no free cosmological parameter**.

### Paper 6 section as it stood

### Paper 6 (Growth against raw data — single sector)

> The two-sector φ-DM rows below are RETIRED (2026-08-01) and kept only as history.
> The subtraction defining Ω_φDM mixed a measured density with a number from the
> equation of state (0.160 = 1+w₀), so the particle had nothing to be made of.

| Result | Value | Status |
|---|---|---|
| Ω_CDM | 0.160 | Active at all k |
| ~~Ω_φDM = Ω_m,CMB − Ω_m,dyn~~ | ~~0.14889~~ | **RETRACTED 2026-08-01** — the subtraction mixed a measured density with 1+w₀, an equation-of-state number |
| Ω_m = ωm/h² (~~two-sector total~~ — **single sector since 2026-08-01**) | 0.308881 = Ω_m,CMB | ωm-direct (OP-8 dissolved). The value stands; only the name «total of two sectors» is retracted — there is one sector |
| Σm_ν = R₂ × 0.9530 eV | 0.0685 eV | R₂ = Ω/(KAL·TRIAL) = 0.071875 (ν-closure C=93.14) |
| ~~m_φ = Σm_ν × (SOLAR²·KRYSTOS_V)~~ | ~~40.70 eV~~ | **RETRACTED 2026-08-01** — the particle had nothing to be made of once the subtraction fell; also excluded by the raw shear (m_φ > 70.3 eV) |
| ~~α (Viel fit to particle/cold P(k) ratio)~~ | ~~1.117 Mpc/h~~ | **RETIRED 2026-08-01** with the particle |
| ~~k_fs (free-streaming)~~ | ~~0.754 h/Mpc~~ | **RETIRED 2026-08-01** with the particle |
| σ₈_eff (two-sector particle) | 0.747 | RETIRED 2026-08-01 |
| **σ₈, S₈ (single sector, A_s free, MCMC vs raw KiDS-1000 ξ±)** | **0.7446±0.0189, 0.7555±0.0192** | **0.11σ — no S₈ tension.** Converged Cobaya+CAMB run, R−1=0.019, N_eff=4.2×10⁴, χ²=265.4/216 dof |
| Same background with A_s **fixed** to Planck | σ₈=0.8149, S₈=0.827 | the old "3.5σ challenge" — an artefact of fixing A_s, i.e. of importing the Planck–KiDS tension (2.7σ with the corrected ceiling) |
> **Actualizado 2026-09-08.** Estos dos valores eran `σ₈=0.8335 / S₈=0.846`, con
> tensiones 1.1σ / 3.5σ / 3.9σ. Salían de una corrida de CLASS **sin `.ini`**, fuera
> del repositorio y **sin neutrinos masivos**; el fondo canónico sí los lleva
> (Σm_ν=0.06849 eV) y sin ellos sobra un 2.3% de grumo. Re-corrido con
> `config/class/techo_ssee_canonico.ini`; su control, con criterio escrito antes de
> correr, exige que la línea base de Planck dé σ₈=0.8111±0.006 y da **0.810851**.
> Log: `results/logs/p5_techo_sigma8_As_fijo.json`

| fσ₈ vs raw BOSS DR12 multipoles | pending (R1/R2) | single-sector baseline 0.70σ |

> **Note (2026-08-01):** there is **one** matter sector, Ω_m = 0.308881, with no
> partition — no second φ-DM sector and no particle. What closes S₈ is not extra
> freedom but the opposite: the background is *more* constrained here than in
> ΛCDM, and A_s — one of the model's two free CMB-level parameters — is the only
> quantity allowed to move. Fixing it to Planck's preferred value, as earlier
> versions did, imports the Planck–KiDS tension into a model that does not
> otherwise have it; that, and not new physics, produced the "3.5σ challenge".
>
> **Methodological point:** the earlier tension was measured against the
> *compressed* S₈ statistic, whose data-reduction pipeline itself assumes a ΛCDM
> background. A published number with an error bar can still be the output of
> fitting a fiducial template — before treating one as a target, ask whether it is
> a raw observable or a model-conditioned summary.

### Paper 7 section as it stood (exponential potential, β_c)

### Paper 7 (Canonical EFT)

| Result | Value | Status |
|---|---|---|
| Action | S = ∫d⁴x√(−g)[−X + V₀e^{β_c φ}] | Canonical, minimal coupling |
| β_c | −AURA = −3.9978 | Algebraic exact |
| ~~β_c (plateau test, 8 ICs)~~ | ~~−3.98991 ± 0.00001~~ | **RETRACTED 2026-09-07** — the «verified to <0.2%» was the saturation normalisation bug; the real value is −2.194210, and β_c itself left P7 with the potential |
| αT | 0 exact | GW170817 \|αT\| < 10⁻¹⁵ satisfied ✓ |
| αM | 0 exact | Euclid forecast < 0.05 satisfied ✓ |
| αB | 0 exact | Euclid forecast < 0.05 satisfied ✓ |
| αK(z=0) | 3·Ω_DE·Ω_m,dyn = 0.4033 | Algebraic (Euclid will constrain < 0.1) |
| G₂_s (running) | 1.003 | ΛCDM-consistent linear growth @ Ω_m=0.30889 ✓ |

### CLASS table row

| ~~α free-streaming (CLASS output, φ-DM particle)~~ | ~~**1.117 Mpc/h**~~ | — | — | **RETIRED 2026-08-01**: there is no canonical particle |

### CLASS table row

| ~~S₈ (two-sector, canonical particle)~~ — RETIRED 2026-08-01 | ~~**0.758**~~ | — | ~0.83 | superseded: single sector gives 0.7555±0.0192 (0.11σ, KiDS-1000, A_s free) and 0.8273 predicted vs 0.8265±0.0176 (0.05σ, KiDS-Legacy, A_s fixed by the CMB) |

### Open-problems table as it stood (dated 2026-07-10)

### Open physics problems (see [OPEN_PROBLEMS.md](OPEN_PROBLEMS.md))
| ID | Problem | Status (2026-07-10) |
|----|---------|---------------------|
| OP-1 | Baryon density Ω_b h² | **Partial** — formula (π−φ)/(3Ω²) = 0.32σ Planck; ab-initio baryogenesis → Paper B |
| OP-2 | n_s = 1−φ⁻⁷ exponent | **Resolved** (conditional) — α-attractor universality + N_*=2φ⁷; new prediction r=φ⁻¹⁰ |
| OP-3 | Origin of the `5/2` in `M⁴ = 5φ⁸ρ_c` | **Partial** — reopened 2026-09-06; `KAL_eff` is solved FROM `M⁴`, not derived independently |
| OP-4 | Solar Vainshtein radius | **Resolved** — k-mouflage (not Galileon) + αB=αM=αT=0 EFT suppression |
| OP-5 | ~~S₈ weak-lensing tension~~ | **Dissolved (2026-08-01)** — there is no tension to resolve: with a single sector and A_s free, the MCMC against raw KiDS-1000 ξ± gives S₈ = 0.7555 ± 0.0192 (0.11σ). The 3.5σ was an artefact of fixing A_s to Planck; the two-sector answer is retracted. Full non-linear N-body remains desirable, but no longer as a rescue |
| OP-6 | Screening form (mult. vs add.) | **Resolved** — separate-universe k-essence + identity 1+w₀=Ω_m,dyn |
| OP-7 | QFT derivation of genesis role assignments | **Partial** |
| OP-8 | MIRA/matter-factor mechanism | **Dissolved (2026-06-18)** — ωm-direct: Ω_m,CMB = ωm/h² = 0.30889 is the standard physical observable, no matter factor to derive; MIRA survives only in f_screen |
| OP-9 | ~~UV origin of the mass multiplier~~ | **Closed by dissolution (2026-08-01)** — no multiplier to derive: the particle is retracted |
| OP-10 | ~~Unification of φ and χ into a single field~~ | **Closed by dissolution (2026-08-01)** — there is no second field χ to unify |
| OP-11 | ~~Free non-minimal coupling ξ~~ | **Closed by dissolution (2026-08-01)** — ξ lived in the retracted φ-DM sector |
| OP-12 | ~~Relic abundance Ω_φDM h² ab initio~~ | **Closed by dissolution (2026-08-01)** — Ω_φDM came from a subtraction that mixed a density with an equation-of-state number; there is no relic abundance to derive |
| OP-13 | Paper 8 internal consistency (√AURA vs B-S) | **Resolved (2026-05-23)** — Option A |
| OP-14 | Σm_ν phenomenological derivation | **Resolved (2026-06-04)** — Σm_ν = 0.0685 eV self-consistent cascade (ν-closure C=93.14 demonstrated) |
| OP-15 | Bullet-cluster offset κ(θ) from KAL(x) | **Open** — not yet computed (Paper 1) |
| OP-16 | (π−φ)/(π+φ)=0.3201 vs proton mass-energy fraction | **Open / speculative** (genesis; retired from Paper 4, zero cosmological impact) |
| OP-17 | ~~Canonical φ-DM particle SOLAR²·KRYSTOS_V~~ | **Closed by dissolution (2026-08-01)** — the particle is retracted; there is no canonical mass to adopt |
| OP-18 | Primordial amplitude A_s from (φ,π) | **Open (2026-06-20)** — inflation-scale residue (Paper 3) |
| OP-19 | Production mechanism behind ω_c = KAL₀·ω_b·n_s | **Open (2026-07-12)** — forward relation (0.4σ Planck) works; deriving why *this* combination = relic-abundance mechanism (links OP-1). n_s is the leading candidate, not a certainty (identity window [0.960, 0.979]) |

### Roadmap fragment

> The previous Status block, dated 2026-07-10, announced a canonical φ-DM particle
> m_φ = 40.70 eV as a forward prediction. **That particle was retracted on
> 2026-08-01** and this block was not updated with it — one of the leftovers the
> 2026-09-19 audit found. See the retraction banner above.

### Roadmap fragment

- [x] ~~Canonical φ-DM particle (m_φ = 40.70 eV, forward prediction)~~ — **RETRACTED
      2026-08-01**. What survives is the Hubble cascade, and with its direction
      corrected on 2026-09-06 (SH0ES is the input, the global H is the output):
      73.04 × (1 − f_screen^full = 0.069522) = 67.962142 km/s/Mpc, residual
      +4.2e-06 against the pure number 3(φ+π)²; with the IR f_screen alone
      (0.067253) it gives 68.13, 0.17σ. Propagated σ = ±0.970 dominates

### Roadmap fragment

> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
- [x] ~~OP-9 residual — UV origin of the multiplier 594.28 (SOLAR² · KRYSTOS_V)~~ —
      **closed by dissolution 2026-08-01**: with the particle retracted there is no
      multiplier left whose UV origin to derive.

