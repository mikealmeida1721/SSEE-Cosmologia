#!/usr/bin/env python3
"""Unified, quinta lectura (2026-10-12): lo que la lectura encontró, con su porqué en notes/lectura_quinta/Unified.md."""
import sys

P = "manuscript/SSEE_Unified_Journal.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


# 0. un solo H_glob; el residuo no es sigma; la fecha
rep(r"H_0^{\rm glob,UV}", r"H_0^{\rm glob}", n=3)
# la fecha de portada no se toca: la mueve sólo preparar_publicacion.py

# 1. resumen
rep(r"""The dark energy equation of state $\wz = -(3\phiG+\pi)/[2(\phiG+\pi)] \simeq -0.840$
and $\wa \simeq -0.670$ are fixed by the algebraic construction and agree with the
official DESI~DR2 $w_0w_a$CDM posterior within $0.24\sigma$ (Pantheon+;
$0.2$--$1.8\sigma$ across SN compilations)""",
    r"""The dark energy equation of state $\wz = -(3\phiG+\pi)/[2(\phiG+\pi)] = \val{W0_d3}$
and $\wa = \val{WA_d3}$ are fixed by the algebraic construction and agree with the
official DESI~DR2 $w_0w_a$CDM posterior within $\val{p2_w0wa_ssee_ec26}\sigma$ (Pantheon+;
$\val{p2_w0wa_ssee_ec26_d1}$--$\val{p2_w0wa_ssee_ec27_d1}\sigma$ across SN compilations)""")
rep(r"""~km\,s$^{-1}$\,Mpc$^{-1}$, which is also
the value at which Planck~\texttt{plik\_lite} is minimised with SSEE-fixed $\omega_b,\omega_c$; Papers~3, 9--10) yields""",
    r"""~km\,s$^{-1}$\,Mpc$^{-1}$, which lies
$\val{perfil_h0_d}\sigma$ from the value at which Planck~\texttt{plik\_lite} is minimised with SSEE-fixed $\omega_b,\omega_c$; Papers~3, 9--10) yields""")
rep(r"""$\val{h0_p2_dhglob}\sigma$ from $H_0^{\rm glob}$) and $\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$ favouring
\SSEE\ over \LCDM\ ($\val{p2_dBIC_cpl}$ over CPL).""",
    r"""$\val{h0_p2_dhglob}\sigma$ from $H_0^{\rm glob}$). Model selection favours \SSEE\ by
$\Delta\mathrm{BIC}=\val{p2_k0_dBIC_lcdm}$ over \LCDM\ and $\val{p2_k0_dBIC_cpl}$ over CPL with nothing free
($k=0$), and $\val{p2_dBIC_lcdm}$ and $\val{p2_dBIC_cpl}$ in the conservative version that samples
$H_0$ and $\Omega_b h^2$ ($k=2$).""")
# P5 reescrito: la estabilidad la da el campo de P7, no el IS; sigma8 con A_s fijo a Planck
rep(r"""A linear Israel-Stewart perturbation analysis with $\Omega_{m,\mathrm{cosm}}=\val{OMEGA_M_TOTAL_d6}$ in
the Poisson equation yields a growth factor
$\mathcal{G} = 1.0032$ and $\sigma_8 = 0.8136$ (Paper~5), giving a mean
$\fsig$ tension of $\val{fs8_tmedia_ssee}\sigma$ across six RSD surveys --- statistically identical
to $\Lambda$CDM ($0.73\sigma$), resolving the growth-rate sector.""",
    r"""A linear perturbation analysis with $\Omega_{m,\mathrm{cosm}}=\val{OMEGA_M_TOTAL_d6}$ in
the Poisson equation, with the dark-energy sector stabilised by the sound speed of
the field of Paper~7, yields a growth factor
$\mathcal{G} = \val{p5_G}$ (Paper~5) and, with $A_s$ held at Planck's value,
$\sigma_8 = \val{p3_sigma8_IS}$, giving a mean
$\fsig$ tension of $\val{fs8_tmedia_ssee}\sigma$ across six RSD surveys --- statistically identical
to $\Lambda$CDM ($\val{fs8_tmedia_lcdm}\sigma$).""")
# P8
rep(r"""In the strong-field regime Paper~8 analyses two limits: an alternative
MOND-like limit in which the photon deflection is amplified by
$\sqrt{\AURA}\approx \val{sqrt_AURA_d4}$ (numerically close to $\MIRA$ at $0.03\%$ but
algebraically distinct), and the canonical limit with EFT
$\alpha_B=\alpha_M=\alpha_T=0$ in which the residual fifth-force is
suppressed to $F_\phi/F_N\sim 10^{-15}$ and the observable lensing recovers
GR; current SLACS/BELLS data favour the canonical limit (Paper~8;
OPEN\_PROBLEMS.md OP-13).""",
    r"""In the strong-field regime Paper~8 keeps a disformal contrast, in which the photon
deflection would be amplified by $\sqrt{\AURA}=\val{sqrt_AURA_d4}$ (numerically
$\val{sqrtAURA_MIRA_d5}\,\MIRA$ but algebraically distinct) and which makes no
prediction of the model, and derives the canonical limit with EFT
$\alpha_B=\alpha_M=\alpha_T=0$, in which the residual fifth force is
suppressed to $F_\phi/F_N\sim\val{quinta_fuerza_10kpc}$ at $10$~kpc and the observable lensing is
that of GR with the model's cold matter; current SLACS/BELLS data are consistent with it (Paper~8;
OPEN\_PROBLEMS.md OP-13).""")
# f_scr es s_K/(3 MIRA), no alpha_K; la forma es el postulado de P9
rep(r"""A late-time local screening fraction
$f_{\rm scr}^{\rm IR}=\alphaK/(3\MIRA)=(\pi-\phiG)/(\phiG+\pi)^2\simeq0.067$ relates
the locally measured rate to the global background.""",
    r"""A late-time local screening fraction
$f_{\rm scr}^{\rm IR}=s_K/(3\MIRA)=(\pi-\phiG)/(\phiG+\pi)^2=\val{F_SCREEN_IR_d4}$ relates,
under the screening postulate of Paper~9, the locally measured rate to the global background.""")
rep(r"""number, in both cases with zero free parameters (Papers~9 and~10).
A UV completion $K(X)=X/\KAL+X^2/M^4$ with algebraic cutoff $M=9.68$~meV
connects the dark-energy EFT to the inflationary $\alpha$-attractor (Paper~10).""",
    r"""number, far inside the propagated $\pm\val{p9_hglob_sigma}$, in both cases with zero free
parameters (Papers~9 and~10). A UV completion $K(X)=X/\KAL+X^2/M^4$ whose cutoff
$M=\val{M_meV_d2}$~meV is conjectured to be set by the inflationary $\alpha$-attractor
(Conjecture~C.1, Paper~10) is consistent with the cascade, which does not measure it.""")

# 2. introducción
rep(r"""compelling evidence for dynamical dark energy at $>3\sigma$, with a CPL
equation-of-state posterior centred near $(\wz,\wa) \approx (-0.84, -0.67)$.
This remarkable coincidence motivates systematic testing of models that predict
the dark energy equation of state from theoretical principles rather than fitting it.""",
    r"""evidence for dynamical dark energy at $2.8$--$4.2\sigma$ depending on the supernova
sample, with the DESI\,$+$\,CMB\,$+$\,Pantheon+ posterior centred at
$(\wz,\wa)=(-0.838,-0.62)$. This motivates systematic testing of models that predict
the dark energy equation of state from theoretical principles rather than fitting it.""")
rep(r"""algebraic closure condition: all cosmological background parameters are uniquely
determined by two dimensionless geometric constants,""",
    r"""algebraic closure condition: the dimensionless background parameters are
fixed by two dimensionless geometric constants,""")
rep(r"""\item \textbf{EFT stability} (\S\ref{sec:eft}): the Paper~7 ghost condensate,
  gradient-stable with $c_s^2=0.021284$, and gravitational-wave compatibility""",
    r"""\item \textbf{EFT stability} (\S\ref{sec:eft}): the Paper~7 ghost condensate,
  gradient-stable with $c_s^2=\val{cs2_condensado_d6}$, and gravitational-wave compatibility""")
rep(r"""framework --- the strong-field lensing regime, an algebraic resolution of the
Hubble tension, and a UV completion""",
    r"""framework --- the strong-field lensing regime, an algebraic screening account of
the Hubble tension (under a postulate), and a UV completion""")

# 3. núcleo
rep(r"""From these seven scalars, the dark energy equation of state is derived uniquely:""",
    r"""From these seven scalars, the dark energy equation of state is fixed:""")
rep(r"""     = -\frac{P_{\rm sc}}{\pi+P_{\rm sc}} \simeq -0.66997.""",
    r"""     = -\frac{P_{\rm sc}}{\pi+P_{\rm sc}} = \val{WA_d5}.""")
rep(r"""$s_{\rm DE} = |{\wz}| = T_r/M_v \simeq 0.8399$ --- a number of the equation of""",
    r"""$s_{\rm DE} = |{\wz}| = T_r/M_v = \val{S_DE_d4}$ --- a number of the equation of""")
rep(r"""(The earlier, now superseded MIRA mapping
$\MIRA=(3\phiG+\pi)/4\simeq1.9989$ gave $\OmmCMB=\MIRA\times\sm=0.3199$, superseded;
$\MIRA$ now enters only the Hubble screening fraction, Paper~9.)""",
    r"""(The earlier mapping $\OmmCMB=\MIRA\times\sm$, with $\MIRA=(3\phiG+\pi)/4$,
is withdrawn; $\MIRA$ now enters only the Hubble screening fraction, Paper~9.)""")
rep(r"""is examined in Papers~3 and~5 \citep{AlmeidaSSEE2026P3,AlmeidaSSEE2026P5}.""",
    r"""is examined in Papers~3 and~6 \citep{AlmeidaSSEE2026P3,AlmeidaSSEE2026P6}.""")

# 4. MCMC de fondo
rep(r"""For \SSEE, $H_0$ is the sole free parameter; $(\wz,\wa)$ are fixed algebraically.""",
    r"""For \SSEE, $(\wz,\wa)$ are fixed algebraically; $H_0$ and $\Omega_b h^2$ are sampled
in this conservative version ($k=2$), although $\omega_b$ is algebraic and $H_0$ is the
output of the cascade. With nothing free ($k=0$) \SSEE\ is favoured by
$\Delta\mathrm{BIC}=\val{p2_k0_dBIC_lcdm}$ over \LCDM\ and $\val{p2_k0_dBIC_cpl}$ over CPL, and freeing
$H_0$ and $\Omega_b h^2$ lowers $\chi^2$ by only $\val{p2_k0_dchi2}$ (Paper~2).""")
rep(r"""($r_d=147.17$ vs $147.10$~Mpc, CAMB)""",
    r"""($r_d=\val{p2_lyaB_rd}$ vs $\val{p2_rd_lcdm}$~Mpc, CAMB)""")
rep(r"""full-background penalty was an artefact of placing the cold sector
$1+w_0=\val{S_M_d6}$ in $E(z)$ where the total density belongs; with the correct total
density it does not occur.
The $\omega_m$-direct two-$\Omega_m$ construction (\S\ref{sec:mira}) resolves
the background tension, validated in \S\ref{sec:cmb} below.""",
    r"""full-background penalty was an artefact of placing the equation-of-state number
$1+w_0=\val{S_M_d6}$ in $E(z)$ where the total density belongs; with the correct total
density it does not occur. The single matter density (\S\ref{sec:mira}) is checked
against the acoustic peaks in \S\ref{sec:cmb} below.""")

# 5. MCMC multi-sonda: R-1 = 0.020 (no < 0.005), 53 116 filas (no 7e4 efectivas), 1.74 (no 1.73)
rep(r"""free in $[60,80]$; four chains, $\sim$53k post-burn-in samples, Gelman--Rubin
$R-1<0.005$).""",
    r"""free in $[60,80]$; four chains, \val{mf_filas} samples after a $30\%$ burn-in per chain,
Gelman--Rubin $R-1=\val{mf_rminus1}$).""")
rep(r"""The remaining parameters $(H_0,\Omega_m,w_0,w_a)$ sit
$1.4$--$1.8\sigma$ from the algebraic values,""",
    r"""The remaining parameters $(H_0,\Omega_m,w_0,w_a)$ sit
$\val{mf_wa_tens}$--$\val{mf_H0_tens}\sigma$ from the algebraic values,""")
rep(r"""constant $(-1,0)$ at $\val{mf_w0wa_lcdm}\sigma$, while the \SSEE\ algebraic point
$(-0.840,-0.670)$ lies at only $1.31\sigma$ in the correlated ($\rho=-0.93$)
$w_0$--$w_a$ plane --- more than twice as close as \LCDM.\footnote{The
$\sigma_8\approx0.80$, $S_8\approx0.84$ recovered here""",
    r"""constant $(-1,0)$ at $\val{mf_w0wa_lcdm}\sigma$, while the \SSEE\ algebraic point
$(\val{W0_d3},\val{WA_d3})$ lies at only $\val{mf_w0wa_ssee}\sigma$ in the correlated ($\rho=\val{mf_rho}$)
$w_0$--$w_a$ plane --- more than twice as close as \LCDM.\footnote{The
$\sigma_8=\val{mf_sigma8}$, $S_8=\val{mf_S8}$ recovered here""")
rep(r"""values. Four independent chains, Gelman--Rubin $R-1<0.005$ for all parameters,
$\sim7\times10^4$ effective samples. DESI~DR2-corrected vector (V-L4-DESI).}""",
    r"""values. Four independent chains, Gelman--Rubin $R-1=\val{mf_rminus1}$,
\val{mf_filas} samples after burn-in. DESI~DR2-corrected vector (V-L4-DESI).}""")
rep(r"""algebraic point $(-0.840,-0.670)$ lies $1.31\sigma$ from the joint $w_0$--$w_a$
posterior, whereas the cosmological-constant point $(-1,0)$ is excluded at
$3.22\sigma$. The joint distance is smaller than the individual $w_0,w_a$
marginals ($1.73\sigma,\,1.43\sigma$) because the algebraic offset lies
\emph{along} the strong $w_0$--$w_a$ degeneracy ($\rho=-0.93$), not across it.""",
    r"""algebraic point $(\val{W0_d3},\val{WA_d3})$ lies $\val{mf_w0wa_ssee}\sigma$ from the joint $w_0$--$w_a$
posterior, whereas the cosmological-constant point $(-1,0)$ is excluded at
$\val{mf_w0wa_lcdm}\sigma$. The joint distance is smaller than the individual $w_0,w_a$
marginals ($\val{mf_w_tens}\sigma,\,\val{mf_wa_tens}\sigma$) because the algebraic offset lies
\emph{along} the strong $w_0$--$w_a$ degeneracy ($\rho=\val{mf_rho}$), not across it.""")
rep(r"""\LCDM\ spectrum-for-spectrum ($\chi^2_r\simeq1.04$) while spending four fewer""",
    r"""\LCDM\ spectrum-for-spectrum ($\chi^2_r(\mathrm{TT})=\val{p3_chi2r_TT_ssee}$) while spending four fewer""")
rep(r"""independently prefer a point $1.31\sigma$ from \SSEE\ (with \LCDM\ excluded at
$3.22\sigma$),""",
    r"""independently prefer a point $\val{mf_w0wa_ssee}\sigma$ from \SSEE\ (with \LCDM\ excluded at
$\val{mf_w0wa_lcdm}\sigma$),""")
rep(r"""confronts DESI (Paper~II, $0.24\sigma$ Pantheon+),""",
    r"""confronts DESI (Paper~II, $\val{p2_w0wa_ssee_ec26}\sigma$ Pantheon+),""")

# 6. r_d
rep(r"""$r_d = 147.17$~Mpc, within $1\sigma$ of the Planck~2018 measurement
$r_d = 147.09\pm0.26$~Mpc \citep{Planck2018}""",
    r"""$r_d = \val{p2_lyaB_rd}$~Mpc, $\val{rd_ssee_sig_planck}\sigma$ from the Planck~2018 value
$r_d = \val{rd_planck}\pm\val{rd_planck_sigma}$~Mpc \citep{Planck2018}""")

# 7. crecimiento: P5 reescrito (Q1 no es un resultado de estabilidad)
rep(r"""Paper~5 \citep{AlmeidaSSEE2026P5} performs a causal Israel-Stewart (IS)
analysis \citep{IsraelStewart1979} and demonstrates analytically that the
\SSEE\ structure constants satisfy an algebraic identity that forces the
effective IS sound speed to zero:
$c_{s,\mathrm{eff}}^2(k\to\infty) = 0$, to floating-point precision.""",
    r"""Paper~5 \citep{AlmeidaSSEE2026P5} performs a causal Israel-Stewart (IS)
analysis \citep{IsraelStewart1979}. The \SSEE\ structure constants make the
high-frequency IS sound speed vanish, $c_{s,\mathrm{eff}}^2(\omega\tau_\Pi\to\infty)=0$,
but that is \emph{not} a stability result: with $c^2_{s,\rm bare}=\wz$ the growing
mode is unstable at every $k$. The stability of the dark-energy sector is carried
instead by the field of Paper~7, whose own sound speed is
$c_s^2=+\val{cs2_condensado_d6}$; with it no mode grows.""")
rep(r"""Integrating the full IS linear growth ODE from $z=19$ to $z=0$
with $\Omega_{m,\mathrm{cosm}} = \val{OMEGA_M_TOTAL_d6}$ in the Poisson source:
\begin{equation}
  \mathcal{G} = D_1^{\mathrm{SSEE}}/D_1^{\Lambda\mathrm{CDM}} = 1.0032,
  \qquad
  \sigma_8^{\mathrm{SSEE}} = 0.811 \times \mathcal{G} = 0.8136.
  \label{eq:G_IS}
\end{equation}""",
    r"""Integrating the linear growth equation from $z=19$ to $z=0$
with $\Omega_{m,\mathrm{cosm}} = \val{OMEGA_M_TOTAL_d6}$ in the Poisson source:
\begin{equation}
  \mathcal{G} = D_1^{\mathrm{SSEE}}/D_1^{\Lambda\mathrm{CDM}} = \val{p5_G},
  \qquad
  \sigma_8^{\mathrm{SSEE}} = \val{p3_sigma8_IS} \;\;(A_s\ \text{held at Planck's value}).
  \label{eq:G_IS}
\end{equation}""")
rep(r"""(Paper~5), the growth factor is $\mathcal{G}=1.0032$ and the mean $\fsig$
tension across six RSD surveys is $0.70\sigma$ --- statistically
indistinguishable from $\Lambda$CDM ($0.73\sigma$).""",
    r"""(Paper~5), the growth factor is $\mathcal{G}=\val{p5_G}$ and the mean $\fsig$
tension across six RSD surveys is $\val{fs8_tmedia_ssee}\sigma$ --- statistically
indistinguishable from $\Lambda$CDM ($\val{fs8_tmedia_lcdm}\sigma$).""")
rep(r"""non-linear effects (baryonic feedback beyond HMcode, halo bias) may modify the
predictions at the $10\%$--$20\%$ level.""",
    r"""non-linear effects (baryonic feedback beyond HMcode, halo bias) are not
included.""")

# 8. EFT
rep(r"""  c_s^2 = \frac{M_v-T_r}{5M_v+3T_r} = 0.021284 > 0,""",
    r"""  c_s^2 = \frac{M_v-T_r}{5M_v+3T_r} = \val{cs2_condensado_d6} > 0,""")
rep(r"""integration reproduces $c_s^2$ to $0.000\%$ and $\alphaK$ to $0.011\%$, with
the internal stability tests enabled (Paper~7). The kineticity itself is
\emph{not} observationally accessible: a factor $100$ change moves $\sigma_8$ by
$0.007\%$ and the TT spectrum only at $\ell<10$, seven times below cosmic
variance.""",
    r"""integration reproduces $c_s^2$ to $\val{p7_hc_cs2_pct}\%$ and $\alphaK$ to $\val{p7_hc_alphaK_pct}\%$, with
the internal stability tests enabled (Paper~7). The kineticity itself is
\emph{not} observationally accessible: a factor $100$ change moves $\sigma_8$ by
$\val{p7_hc_s8_xk_pct}\%$ and the TT spectrum only at the lowest multipoles, below cosmic
variance (Paper~7).""")
# el campo de P7 RUEDA; w no es constante; por qué cruza w=-1 es OP-24
rep(r"""When the CPL EoS $w(z) = \wz + \wa z/(1+z)$ is used in the EFTCAMB run,
the phantom boundary $w = -1$ is crossed at $z \simeq 0.31$.""",
    r"""When the CPL EoS $w(z) = \wz + \wa z/(1+z)$ is used in the EFTCAMB run,
the phantom boundary $w = -1$ is crossed at $z = \val{z_cruce}$.""")
rep(r"""That reading is superseded,
and the reason is that the phantom regime itself is gone.  In the revised
action of Paper~7 the field is minimally coupled and its equation of state is
constant at $\wz = \val{W0_d6} > -1$: the null energy condition holds at all
times and there is no crossing for $\alphaB$ to absorb.  The phantom crossing
of earlier versions was produced by the conformal dark-sector coupling, which
is withdrawn.

The prediction survives, with its sign reversed and its status improved.
SSEE now predicts $\alphaB = \alphaM = 0$ \emph{exactly and
unconditionally}, so a detection of $\alphaB \neq 0$ above $2\sigma$ by
DESI~Y3 or Euclid ($\sigma \simeq 0.05$) would \emph{falsify} the sector
rather than support it.  What was a discriminating prediction conditional on
a two-sector picture --- an extension withdrawn on 2026-08-01 --- is now an
unconditional one.""",
    r"""That reading is superseded.
In the action of Paper~7 the field is minimally coupled and fixes $w_0$ and $c_s^2$
today, but it is not static: it rolls towards $w=-1$, with its own
$w_a^\phi=\val{p7_wa_campo}$, and a single canonical field cannot cross $w=-1$. The
algebraic $w(a)$ does cross it; what produces the crossing is open (OP-24). The
conformal dark-sector coupling of earlier versions, which produced a crossing, is
withdrawn.

For the action of Paper~7, $\alphaB = \alphaM = 0$ exactly, so a detection of
$\alphaB \neq 0$ by DESI~Y3 or Euclid would falsify that action. What was a
discriminating prediction conditional on a two-sector picture --- an extension
withdrawn on 2026-08-01 --- is now a test of the action itself.""")

# 9. extensiones
rep(r"""$H_0^{\rm glob} = H_{\rm SH0ES}(1-f_{\rm screen}) = 67.96214$~km\,s$^{-1}$\,Mpc$^{-1}$ (residual $+4.2{\times}10^{-6}$ against the dimensionless target $3(\varphi+\pi)^2$,
not a significance: the propagated uncertainty is $\pm\val{p9_hglob_sigma}$) --- that is explicitly
conditional on a separability postulate and is therefore presented as a
self-consistency check, not an independent prediction.""",
    r"""$H_0^{\rm glob} = H_{\rm SH0ES}(1-f_{\rm screen}) = \val{H0_GLOBAL_d5}$~km\,s$^{-1}$\,Mpc$^{-1}$ (residual $+\val{p9_hglob_residuo}$ against the dimensionless target $3(\varphi+\pi)^2$,
not a significance: the propagated uncertainty is $\pm\val{p9_hglob_sigma}$) --- whose UV
term rests on Conjecture~C.1 and is therefore presented as a
consistency check, not an independent prediction.""")
rep(r"""suppressed to $F_\phi/F_N\sim(H/k)^2\sim 10^{-15}$ at kpc scales and the""",
    r"""suppressed to $F_\phi/F_N\sim(H/k)^2\sim\val{quinta_fuerza_10kpc}$ at $10$~kpc and the""")
rep(r"""The equation of state of Paper~7, with the structural constants of the
algebra, fixes a late-time \emph{local screening fraction}""",
    r"""The equation of state of Paper~1, with the structural constants of the
algebra, fixes a late-time \emph{local screening fraction}""")
rep(r"""rate is $H_0^{\rm glob}=\val{H0_GLOBAL_d5}$. (The earlier MIRA anchor
$H_0^{\rm MIRA}=67.037$ gave $71.87$ at $1.12\sigma$, now superseded by the
reframe.)""",
    r"""rate is $H_0^{\rm glob}=\val{H0_GLOBAL_d5}$. (The earlier MIRA anchor is
superseded by the reframe.)""")
rep(r"""The infrared kinetic Lagrangian $K(X)=X/\KAL$ is extended by the leading
higher-derivative operator, $K(X)=X/\KAL + X^2/M^4$. The inflationary
$\alpha$-attractor parameter $\alpha=\phiG^4/3$ (Paper~1, Appendix~A.5), which
fixes the tensor-to-scalar ratio $r=12\alpha/N_*^2\approx0.00813$, also fixes the
UV cutoff:""",
    r"""The infrared screening uses only the equation of state. Paper~10 adds a kinetic
function with a higher-derivative operator, $K(X)=X/\KAL + X^2/M^4$, and conjectures
(Conjecture~C.1) that the inflationary $\alpha$-attractor parameter
$\alpha=\phiG^4/3$ (Paper~1, Appendix~A.5), which fixes the tensor-to-scalar ratio
$r=12\alpha/N_*^2=\val{R_TENSOR_d5}$, also sets the UV cutoff:""")
rep(r"""\qquad M \approx 9.68~{\rm meV} ,""", r"""\qquad M = \val{M_meV_d2}~{\rm meV} ,""")
rep(r"""measured SH0ES rate this gives the canonical UV value
$H_0^{\rm glob}=73.04\times(1-\val{F_SCREEN_d6})=\val{H0_GLOBAL_d5}$~km\,s$^{-1}$\,Mpc$^{-1}$ (residual $+4.2{\times}10^{-6}$ against $3(\varphi+\pi)^2$, $\sigma=0.968$;
the earlier MIRA-anchored $72.05$ at $0.96\sigma$ is superseded by the reframe).""",
    r"""measured SH0ES rate this gives the single global rate
$H_0^{\rm glob}=73.04\times(1-\val{F_SCREEN_d6})=\val{H0_GLOBAL_d5}$~km\,s$^{-1}$\,Mpc$^{-1}$ (residual $+\val{p9_hglob_residuo}$ against $3(\varphi+\pi)^2$; propagated $\pm\val{p9_hglob_sigma}$;
the earlier MIRA-anchored value is superseded by the reframe).""")
rep(r"""We state the epistemic status of these figures plainly: the UV value is
\emph{conditional on Postulate~C.1} (UV--IR $\phiG/\pi$ separability) and is
\emph{not independent of SH0ES}, since the postulate was formulated with the
SH0ES central value as its target. It is a self-consistency check, not a
prediction. The independent prediction remains the IR-regime value
$H_0^{\rm glob,IR}=68.13$~km\,s$^{-1}$\,Mpc$^{-1}$ ($0.17\sigma$) of \S\ref{sec:ext-ht}, which does
not rely on the postulate. The construction does, however, supply a falsifiable
cross-epoch consistency test: the same $\alpha$ governs inflation at $z\sim10^{60}$
and the dark-energy UV scale today, so a LiteBIRD measurement of $r\neq0.00813$
would shift both $\alpha$ and $M$ and change the predicted $H_0^{\rm glob}$
accordingly.""",
    r"""We state the epistemic status of these figures plainly: the UV term rests on
Conjecture~C.1 and is \emph{not independent of SH0ES}, which is the input of the
cascade. The cascade does not measure the cutoff: varying $M^4$ from $0.2\times$ its
value to infinity moves the output by at most $\val{p10_mueve_M4}$~km\,s$^{-1}$\,Mpc$^{-1}$, inside
the propagated uncertainty. The IR value $H_0^{\rm glob,IR}=\val{p9_sh0es_glob_IR}$ of
\S\ref{sec:ext-ht} is the same cascade with the IR term alone, not a second rate. The
construction does supply a cross-epoch test, but its decisive leg is $r$: the
Hubble leg would vote only if LiteBIRD found $r<\val{p10_r_umbral}$ (Paper~10).""")

# 10. falsación y registro
rep(r"""(superseding the weaker earlier form, $3\sigma$ from $\val{S8_k1000_ssee}\pm\val{S8_k1000_ssee_sigma}$ with $A_s$ fitted)
when the primordial amplitude is fitted to raw $\xi_\pm$ data with the \SSEE\
background held fixed;""",
    r"""(superseding the weaker earlier form, $3\sigma$ from $\val{S8_k1000_ssee}\pm\val{S8_k1000_ssee_sigma}$ with $A_s$
fitted to raw $\xi_\pm$ data and the \SSEE\ background held fixed);""")
rep(r"""(v) the strong-lensing Einstein-radius ratio is inconsistent with
$\sqrt{\AURA}\approx\MIRA$ at $>3\sigma$ in HST/JWST surveys.""",
    r"""(v) strong-lensing Einstein radii depart from GR with the model's cold matter
at $>3\sigma$ in HST/JWST surveys (the $\sqrt{\AURA}$ ratio belongs to the
non-canonical disformal contrast of Paper~8 and is not a prediction).""")
rep(r"""$\MIRA = (3\phiG+\pi)/4$ & $\val{MIRA_d6}$ & $\fscr=\alphaK/(3\MIRA)$ (Papers 8, 9) & Postdiction \\""",
    r"""$\MIRA = (3\phiG+\pi)/4$ & $\val{MIRA_d6}$ & $\fscr=s_K/(3\MIRA)$ (Paper 9) & Postdiction \\""")
rep(r"""$\gamma_{\rm IS} = 0.5504$ & $\approx \gamma_{\Lambda\rm CDM} = 0.55$ & RSD surveys & Retrodiction \\""",
    r"""$\gamma_{\rm IS}$ & $\val{p3_gamma_IS}$ ($\gamma_{\Lambda\rm CDM}\simeq0.55$) & RSD surveys & Retrodiction \\""")
rep(r"""& $3(\phiG+\pi)^2$ (residual $+4.2{\times}10^{-6}$) & Retrodiction \\""",
    r"""& $3(\phiG+\pi)^2$ (residual $+\val{p9_hglob_residuo}$) & Retrodiction \\""")
rep(r"""$c_s^2 = (M_v-T_r)/(5M_v+3T_r)$ & $0.021284$ & dark-energy clustering (Euclid, LSST) & Prediction \\
$r = \phiG^{-10}$ & $0.008131$ & LiteBIRD $\sim$2032 & Prediction \\""",
    r"""$c_s^2 = (M_v-T_r)/(5M_v+3T_r)$ & $\val{cs2_condensado_d6}$ & dark-energy clustering (Euclid, LSST) & Prediction \\
$r = \phiG^{-10}$ & $\val{R_TENSOR_d6}$ & LiteBIRD & Prediction \\""")

# 11. discusión
rep(r"""operator $X^2/M^4$ with algebraic cutoff $M = 9.68$~meV --- but a derivation of""",
    r"""operator $X^2/M^4$ with cutoff $M = \val{M_meV_d2}$~meV (Conjecture~C.1) --- but a derivation of""")
rep(r"""factor; the earlier MIRA-mapped $0.31993$ and geometric
$(\pi-\phiG)/(\pi+\phiG)=0.32010$ forms are superseded.""",
    r"""factor; the earlier MIRA-mapped and geometric $(\pi-\phiG)/(\pi+\phiG)$ forms are
superseded.""")

# 12. conclusiones
rep(r"""  $(\wz, \wa) = (-0.840, -0.670)$, fixed by construction (not fitted), lies within
  $0.24\sigma$ of the official DESI~DR2 $w_0w_a$CDM posterior (Pantheon+).""",
    r"""  $(\wz, \wa) = (\val{W0_d3}, \val{WA_d3})$, fixed by construction (not fitted), lies within
  $\val{p2_w0wa_ssee_ec26}\sigma$ of the official DESI~DR2 $w_0w_a$CDM posterior (Pantheon+).""")
rep(r"""  as prior ($\val{h0_p2_dhglob}\sigma$ from it), and $\Delta\mathrm{BIC} = \val{p2_dBIC_lcdm}$ favouring \SSEE\ over \LCDM.""",
    r"""  as prior ($\val{h0_p2_dhglob}\sigma$ from it), and $\Delta\mathrm{BIC} = \val{p2_k0_dBIC_lcdm}$ favouring \SSEE\ over \LCDM\
  with nothing free ($\val{p2_dBIC_lcdm}$ in the conservative $k=2$ version).""")
rep(r"""  $1.31\sigma$ in the $w_0$--$w_a$ plane, where \LCDM\ is excluded at $3.22\sigma$.""",
    r"""  $\val{mf_w0wa_ssee}\sigma$ in the $w_0$--$w_a$ plane, where \LCDM\ is excluded at $\val{mf_w0wa_lcdm}\sigma$.""")
rep(r"""\item \textbf{Structure growth.} The IS perturbation analysis
  ($\OmmCMB=\val{OMEGA_M_TOTAL_d6}$ in Poisson) gives $\mathcal{G} = 1.0032$ and $\sigma_8 = 0.8136$,
  with mean $f\sigma_8$ tension $0.70\sigma$ (Paper~5) --- statistically identical
  to $\Lambda$CDM ($0.73\sigma$).""",
    r"""\item \textbf{Structure growth.} The linear perturbation analysis
  ($\OmmCMB=\val{OMEGA_M_TOTAL_d6}$ in Poisson) gives $\mathcal{G} = \val{p5_G}$ and, with $A_s$ at Planck's
  value, $\sigma_8 = \val{p3_sigma8_IS}$, with mean $f\sigma_8$ tension $\val{fs8_tmedia_ssee}\sigma$ (Paper~5) --- statistically identical
  to $\Lambda$CDM ($\val{fs8_tmedia_lcdm}\sigma$).""")
rep(r"""  condensate, ghost-free and gradient-stable with $c_s^2 = 0.021284$;""",
    r"""  condensate, ghost-free and gradient-stable with $c_s^2 = \val{cs2_condensado_d6}$;""")
rep(r"""  $\fscr^{\rm IR}=(\pi-\phiG)/(\phiG+\pi)^2\approx0.067$ takes the measured SH0ES
  rate as input and returns the global background
  $H_0^{\rm glob,IR}=H_0^{\rm SH0ES}(1-\fscr^{\rm IR})=68.13$~km\,s$^{-1}$\,Mpc$^{-1}$,
  $0.17\sigma$ from the pure number $3(\phiG+\pi)^2=\val{H0_ALG_d5}$, with
  zero free parameters (Paper~9). A UV completion $K(X)=X/\KAL+X^2/M^4$ with
  algebraic cutoff $M=9.68$~meV connects the dark-energy EFT to the inflationary
  $\alpha$-attractor; the associated $H_0^{\rm glob}=\val{H0_GLOBAL_d5}$~km\,s$^{-1}$\,Mpc$^{-1}$
  ($4.3{\times}10^{-6}\sigma$ from $3(\varphi+\pi)^2$; the earlier MIRA-anchored $72.05$ at $0.96\sigma$ is superseded)
  is a self-consistency check conditional on a separability postulate, not an
  independent prediction (Paper~10).""",
    r"""  $\fscr^{\rm IR}=(\pi-\phiG)/(\phiG+\pi)^2=\val{F_SCREEN_IR_d4}$ takes, under the screening
  postulate of Paper~9, the measured SH0ES rate as input and returns
  $H_0^{\rm glob,IR}=H_0^{\rm SH0ES}(1-\fscr^{\rm IR})=\val{p9_sh0es_glob_IR}$~km\,s$^{-1}$\,Mpc$^{-1}$
  with the IR term alone, $\val{p9_sh0es_sig_IR}\sigma$ from the pure number $3(\phiG+\pi)^2=\val{H0_ALG_d5}$, with
  zero free parameters (Paper~9). A UV completion $K(X)=X/\KAL+X^2/M^4$ whose cutoff
  $M=\val{M_meV_d2}$~meV is conjectured to be set by the inflationary $\alpha$-attractor
  (Conjecture~C.1) completes the fraction; the single global rate
  $H_0^{\rm glob}=\val{H0_GLOBAL_d5}$~km\,s$^{-1}$\,Mpc$^{-1}$ (residual $+\val{p9_hglob_residuo}$ against
  $3(\varphi+\pi)^2$, propagated $\pm\val{p9_hglob_sigma}$) is a consistency check, not an
  independent prediction, and does not measure $M$ (Paper~10).""")
rep(r"""with the particle; \S\ref{sec:growth_raw}): the dark-energy sound speed $c_s^2 = 0.021284$, $\alphaB = 0$ (a detection
would falsify the sector), $r = 0.008131$ (LiteBIRD),""",
    r"""with the particle; \S\ref{sec:growth_raw}): the dark-energy sound speed $c_s^2 = \val{cs2_condensado_d6}$, $\alphaB = 0$ (a detection
would falsify the action of Paper~7), $r = \val{R_TENSOR_d6}$ (LiteBIRD),""")

# 13. tabla del apéndice
rep(r"""$-0.838\pm0.057$ (DESI) \\""", r"""$-0.838\pm0.055$ (DESI DR2+CMB+Pantheon+, chain moments) \\""")
rep(r"""$-0.617\pm0.208$ (DESI DR2+CMB+Pantheon+) \\""", r"""$-0.617\pm0.208$ (DESI DR2+CMB+Pantheon+, chain moments) \\""")
rep(r"""$c_s^2$ & $(M_v-T_r)/(5M_v+3T_r)$ & $0.021284$ & --- \\""",
    r"""$c_s^2$ & $(M_v-T_r)/(5M_v+3T_r)$ & $\val{cs2_condensado_d6}$ & --- \\""")
rep(r"""$r$ & $\phiG^{-10}$ & $0.008131$ & $<0.036$ (BK18) \\""",
    r"""$r$ & $\phiG^{-10}$ & $\val{R_TENSOR_d6}$ & $<0.036$ \citep{BICEPKeck2021} \\""")
rep(r"""$\fscr$ & $(\pi-\phiG)/(\phiG+\pi)^2$ & $0.0673$ & --- \\""",
    r"""$\fscr^{\rm IR}$ & $(\pi-\phiG)/(\phiG+\pi)^2$ & $\val{F_SCREEN_IR_d4}$ & --- \\""")
rep(r"""& $3(\phiG+\pi)^2$, residual $+4.2{\times}10^{-6}$ \\""",
    r"""& $3(\phiG+\pi)^2$, residual $+\val{p9_hglob_residuo}$ \\""")
rep(r"""$M$ (UV cutoff) & $(5\phiG^8\rho_c)^{1/4}$ & $9.68$ meV & --- \\""",
    r"""$M$ (UV cutoff) & $(5\phiG^8\rho_c)^{1/4}$ (Conj.~C.1) & $\val{M_meV_d2}$ meV & --- \\""")

open(P, "w").write(s)
print("Unified editado")
