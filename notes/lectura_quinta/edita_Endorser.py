#!/usr/bin/env python3
"""Endorser, quinta lectura (2026-10-12): lo que la lectura encontró, con su porqué en notes/lectura_quinta/Endorser.md."""
import sys

P = "manuscript/SSEE_Endorser_Summary.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


# H no sale del álgebra: sale de SH0ES por la cascada (Postulado D)
rep(r"""The core cosmological background — $w_0$, $w_a$, $H_0$, $\Omega_m$, $n_s$ — is derived \emph{algebraically} from the
golden ratio $\varphi=(1+\sqrt{5})/2$ and $\pi$ with \textbf{zero fitted dimensionless parameters at the background level}.""",
    r"""The dimensionless core of the cosmological background — $w_0$, $w_a$, $\Omega_m$, $n_s$ — is derived \emph{algebraically} from the
golden ratio $\varphi=(1+\sqrt{5})/2$ and $\pi$ with \textbf{zero fitted dimensionless parameters at the background level}; the
one dimensionful input is the measured local rate (SH0ES), from which the global $H_0$ follows.""")
rep(r"""Planck 2018: $147.09\pm0.26$ Mpc""",
    r"""Planck 2018: $\val{rd_planck}\pm\val{rd_planck_sigma}$ Mpc""")

# títulos y páginas reales
rep(r"""\textbf{Paper 4 (Nine Sovereignties)}: CMB observables""",
    r"""\textbf{Paper 4 (Two-Axiom Cosmology)}: CMB observables""")
# P2: titular k=0
rep(r"""$\Delta\text{BIC}=\val{p2_dBIC_lcdm}$ (SSEE favoured, $k_{\rm SSEE}=2$ vs.\ $k_{\Lambda\rm CDM}=3$), total matter density in the background geometry. [31 pp]""",
    r"""$\Delta\text{BIC}=\val{p2_k0_dBIC_lcdm}$ with nothing free ($k_{\rm SSEE}=0$ vs.\ $k_{\Lambda\rm CDM}=3$; $\val{p2_dBIC_lcdm}$ in the conservative version that samples $H_0$ and $\Omega_b h^2$), total matter density in the background geometry. [28 pp]""")
rep(r"""$\Delta\mathrm{BIC}=\val{b1_dBIC}$ (canonical; $-26.03$ in the \texttt{plik\_lite} point estimate with $\{A_s,\tau\}$ fitted and $N=669$ measured from the likelihood), SSEE favoured under $k=2$ vs $k=6$ model comparison. [26 pp]""",
    r"""$\Delta\mathrm{BIC}=\val{b1_dBIC}$ (canonical; $\val{lite_dBIC}$ in the \texttt{plik\_lite} point estimate with $\{A_s,\tau\}$ fitted and $N=\val{lite_N}$ measured from the likelihood), SSEE favoured under $k=2$ vs $k=6$ model comparison. [24 pp]""")
# P5 reescrito: la estabilidad la da el campo de P7
rep(r"""\textbf{Paper 5 (Israel--Stewart Perturbations)}: Causal bulk viscosity; $c_s^2=0$ as the minimal-viscosity solution (OP-21); $\gamma_{\rm IS}=\val{p3_gamma_IS}\approx\gamma_{\Lambda\rm CDM}$. [31 pp]""",
    r"""\textbf{Paper 5 (Israel--Stewart Perturbations)}: Causal viscosity; the vanishing high-frequency sound speed is \emph{not} a stability result --- the dark-energy sector is stabilised by the sound speed of the field of Paper~7; $\gamma_{\rm IS}=\val{p3_gamma_IS}\approx\gamma_{\Lambda\rm CDM}$. [29 pp]""")
rep(r"""fixes $w_0$ but not $w_a$ (OP-24). [17 pp]""",
    r"""fixes $w_0$ and $c_s^2$ today but not $w_a$: the field rolls towards $w=-1$ and cannot cross it (OP-24). [18 pp]""")
# P8: título nuevo; contraste disforme sin predicción; quinta fuerza del log
rep(r"""\textbf{Paper 8 (Strong Gravity)} [\emph{draft; its canonical lensing prediction rests on $\omega_c=\mathrm{KAL}_0\,\omega_b\,n_s$ and $\alpha_B=\alpha_M=0$ (Paper~7), and is unconditional}]: Disformal null geodesic analysed in
  two limits: alternative MOND-like (deflection $\sqrt{\text{AURA}}\approx \val{sqrt_AURA_d4}$,
  numerically close to $\mathcal{M}=\text{AURA}/2$ at $0.03\%$ but algebraically
  distinct) and the canonical limit with EFT $\alpha_B=\alpha_M=\alpha_T=0$
  (residual fifth-force $\sim 10^{-15}$ at kpc, observable lensing recovers GR);
  selective coupling satisfies solar-system tests. Current SLACS/BELLS data
  favour the canonical limit (OPEN\_PROBLEMS.md OP-13).""",
    r"""\textbf{Paper 8 (GR Lensing in the Canonical Limit)}: its canonical lensing prediction rests on $\omega_c=\mathrm{KAL}_0\,\omega_b\,n_s$ and $\alpha_B=\alpha_M=0$ (Paper~7), and is unconditional. In the canonical limit
  the residual fifth force is $\sim\val{quinta_fuerza_10kpc}$ at $10$~kpc and the observable lensing is that of GR with
  the model's cold matter; a disformal contrast (deflection $\sqrt{\text{AURA}}=\val{sqrt_AURA_d4}$) is kept
  only for comparison and makes no prediction. Baryons do not couple to the scalar, so
  solar-system tests are satisfied. Current SLACS/BELLS data are consistent with the
  canonical limit (OPEN\_PROBLEMS.md OP-13).""")
rep(r"""input; no fitted parameters) (2026 reframe; the earlier CMB-mapped
  $H_0^{\rm MIRA}=67.04$ is superseded). [20 pp]""",
    r"""input; no fitted parameters; the multiplicative screening is a postulate). With the
  UV term of Paper~10 the same cascade gives the single global rate
  $H_0^{\rm glob}=\val{H0_GLOBAL_d5}$. [22 pp]""")
rep(r"""$K(X)=X/\mathrm{KAL}_0+X^2/M^4$ with algebraic cutoff $M=9.68$ meV; connects
  the dark-energy EFT to the inflationary $\alpha$-attractor. [16 pp]""",
    r"""$K(X)=X/\mathrm{KAL}_0+X^2/M^4$ whose cutoff $M=\val{M_meV_d2}$ meV is conjectured to be set by
  the inflationary $\alpha$-attractor (Conjecture~C.1); the Hubble cascade is consistent with
  it but does not measure it. [16 pp]""")

# falsación: macros
rep(r"""and KiDS-Legacy for $3.0255\pm0.0396$ ($0.49\sigma$);""",
    r"""and KiDS-Legacy for $\val{leg_logA}\pm\val{leg_logA_s}$ ($\val{logA_leg_vs_cmb}\sigma$);""")
rep(r"""\item $r=\varphi^{-10}=0.008131$ — LiteBIRD ($\sim$2032) will confirm or refute the tensor-to-scalar ratio.""",
    r"""\item $r=\varphi^{-10}=\val{R_TENSOR_d6}$ — LiteBIRD will confirm or refute the tensor-to-scalar ratio.""")
rep(r"""\item A $>3\sigma$ deviation of $w_0$ from $-0.840$ would falsify""",
    r"""\item A $>3\sigma$ deviation of $(w_0,w_a)$ from $(\val{W0_d3},\val{WA_d3})$ in DESI~DR3 would falsify""")

rep(r"""$\alpha_B=\alpha_M=0$. [19 pp]""", r"""$\alpha_B=\alpha_M=0$. [17 pp]""")

open(P, "w").write(s)
print("Endorser editado")
