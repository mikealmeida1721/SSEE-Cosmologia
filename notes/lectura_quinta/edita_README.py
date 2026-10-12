#!/usr/bin/env python3
"""README (portada pública), quinta lectura (2026-10-12): cada número cotejado con su log; porqué en notes/lectura_quinta/README.md."""
import sys

P = "README.md"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


# paper2_w0wa.json: ec28 1.46, ec27 1.76, ec25 1.68
rep("and within **1.2–1.5σ** of the DESY5/Union3/no-SN combinations",
    "and within **1.5–1.8σ** of the DESY5/Union3/no-SN combinations")
# class_picos.json: SSEE 220, ΛCDM 220
rep("| CMB first peak | ℓ₁ = 221 | Planck 2018: ~220 | Δℓ = 1 | ✅ |",
    "| CMB first peak | ℓ₁ = 220 | Planck 2018: ~220 (ΛCDM, same code: 220) | Δℓ = 0 | ✅ |")
# DR1 0.05σ y «−40 %»: sin log (PRD.md)
rep("**DR3 w₀wₐCDM (2027)** — trajectory 0.05σ (DR1) → 0.24σ (DR2, errors −40%, still inside 68%); ~0.5σ expected if DR2 centrals persist; >3σ joint exclusion falsifies",
    "**DR3 w₀wₐCDM (2027)** — 0.24σ against DR2 (inside 68%); ~0.5σ expected if DR2 centrals persist; >3σ joint exclusion falsifies")
# kids_publicados.json: logA_k1000_vs_cmb = 3.6
rep("> parameter count; and KiDS-1000 had asked for log(10¹⁰A_s) = 2.864 ± 0.050,\n> 3.5σ away,",
    "> parameter count; and KiDS-1000 had asked for log(10¹⁰A_s) = 2.864 ± 0.050,\n> 3.6σ away,")

# tabla de papers: títulos y páginas de los PDFs vigentes
rep("Galaxy-Cluster Mass Data | 31 |", "Galaxy-Cluster Mass Data | 28 |")
rep("ω_m-Direct CMB Matter Density | 26 |", "ω_m-Direct CMB Matter Density | 24 |")
rep("| 5 | Israel-Stewart Causal Viscous Perturbations in the SSEE Dark Energy Framework — Exact Marginal Stability, ΛCDM-Consistent Structure Growth, and the Amplitude Ceiling *(the two-sector matter section is RETIRED, 2026-08-01)* | 31 |",
    "| 5 | Israel-Stewart Causal Viscous Perturbations in the SSEE Dark Energy Framework — Stability from the Field, Weak Dark-Energy Clustering, and ΛCDM-Consistent Structure Growth *(rewritten 2026-10-11: the stability comes from the field of Paper 7)* | 29 |")
rep("and the coupling left Paper 7 with the potential)* | 17 |", "and the coupling left Paper 7 with the potential)* | 18 |")
rep("| 8 | SSEE in the Strong-Gravity Regime — Disformal Geodesics, MIRA Emergence, and k-mouflage Screening | 19 |",
    "| 8 | SSEE in the Strong-Gravity Regime — GR Lensing in the Canonical Limit, a Disformal Contrast, and Solar-System Compliance | 17 |")
rep("(consolidation of Papers 1–10 + CLASS + MCMC Phase 4) | 24 |", "(consolidation of Papers 1–10 + CLASS + MCMC Phase 4) | 20 |")
rep("two-stage H₀; honest accounting of ~3 vs 6 parameters) | 21 |", "two-stage H₀; honest accounting of k = 2 vs 6 parameters) | 23 |")

# mcmc_paper2_reframe.json: N_eff 79 203
rep("**Paper 2 — MCMC validation** (100-walker, N_eff ≈ 637,500 for SSEE):",
    "**Paper 2 — MCMC validation** (100 walkers, N_eff ≈ 79,203 for SSEE):")
rep("0.42 → 0.24σ (2D); 1.47σ DESY5, 1.77σ Union3", "0.42 → 0.24σ (2D); 1.46σ DESY5, 1.76σ Union3")
# techo de S8: el de ΛCDM no tiene log
rep("| S₈ (IS, single-sector ceiling) | 0.827 | 0.830 |", "| S₈ with A_s fixed to Planck (CLASS ceiling) | 0.827 | — |")
# Σm_ν: la cadena vive en P4
rep("| Σm_ν = R₂ · ω_b · C_ν / (τ_Π · H₀) | 0.0685 eV |", "| Σm_ν = R₂ · ω_b · C_ν / (τ_Π · H₀) (chain of Paper 4) | 0.0685 eV |")
# fila sin log (CLASS Fase 3, mayo)
rep("| IS cs² effect on σ₈ | 0.03% | — | Negligible ✓ |\n", "")
# mcmc_full_posteriores.json: r_drag 0.10σ, w0 1.74σ
rep("| r_drag (Mpc) | 147.17 | 147.20 ± 0.21 | **0.14σ** ✅ |", "| r_drag (Mpc) | 147.17 | 147.20 ± 0.21 | **0.10σ** ✅ |")
rep("| w₀ | −0.840 | −0.655 ± 0.107 | **1.73σ** ✅ |", "| w₀ | −0.840 | −0.655 ± 0.107 | **1.74σ** ✅ |")
# P4: Y_p lineal 0.2471, 0.6σ (Yp_aver_sig)
rep("| Y_p (BBN) | CAMB BBN (PArthENoPE, Ωb h²=0.02242) = 0.2472 | 0.2449 ± 0.0040 (Aver+2015) | 0.58σ |",
    "| Y_p (BBN) | linear BBN sensitivity at Ωb h² = 0.02242 (Paper 4) = 0.2471 | 0.2449 ± 0.0040 (Aver+2015) | 0.6σ |")
# press_schechter.json: sin σ_M ni 3e11 en el log
rep("""| Halo mass | σ_M(z=10) | n_SSEE/n_ΛCDM |
|---|---|---|
| 3×10^10 M☉ | 1.442 | 0.998 |
| 10^11 M☉ | 1.005 | 0.990 |
| 3×10^11 M☉ | 0.723 | 0.976 |
| 10^12 M☉ | 0.504 | 0.945 |
| 3×10^12 M☉ | 0.362 | 0.892 |""",
    """| Halo mass | n_SSEE/n_ΛCDM (z=10) |
|---|---|
| 3×10^10 M☉ | 0.998 |
| 10^11 M☉ | 0.990 |
| 10^12 M☉ | 0.945 |
| 3×10^12 M☉ | 0.892 |""")
# saturación, no densidad
rep("| IS relaxation time τ_Π H₀ | KAL₀/(3Ω_DE) ≈ 2.191 | algebraic |", "| IS relaxation time τ_Π H₀ | KAL₀/(3\\|w₀\\|) ≈ 2.191 | algebraic |")
rep("saturation correspondence (Ω_DE, w₀) = (s, −s) interpolates", "saturation correspondence (s_DE, w₀) = (s, −s) interpolates")
# diccionario: 55 nombres, 25 valores (SSEE_Constant_Dictionary.md §5)
rep("— 31 invariants\n  generated from φ and π", "— 55 named invariants\n  (25 distinct values) generated from φ and π")
# el MCMC multi-sonda no lleva cúmulos
rep("- [x] Multi-probe MCMC (corrected DESI DR2 + Planck + fσ8 + clusters, blind flat w0/wa)",
    "- [x] Multi-probe MCMC (corrected DESI DR2 + Planck + fσ8, blind flat w0/wa)")
rep("- [x] Third page-by-page reading (2026-10-10):",
    "- [x] Fifth page-by-page reading (2026-10-12): every paper and consolidated document read whole and cross-checked against the others; every number traced to its log\n- [x] Third page-by-page reading (2026-10-10):")

open(P, "w").write(s)
print("README editado")
