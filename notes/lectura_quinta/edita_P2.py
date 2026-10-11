#!/usr/bin/env python3
"""Quinta lectura P2 (2026-10-11): reemplazos exactos; aborta si un conteo no casa."""
import sys

P = "manuscript/SSEE_Paper2_MCMC.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:80]!r}")
    s = s.replace(old, new)


W = r"(\val{W0_d3},\val{WA_d3})"
rep("(-0.840,-0.670)", W, 9)
rep(r"""  \wz^{\SSEE} &= -\frac{T_r}{M_v}\approx-0.840, \quad
  \wa^{\SSEE} = -\frac{P_{sc}}{I_g}\approx-0.670.""",
    r"""  \wz^{\SSEE} &= -\frac{T_r}{M_v}=\val{W0_d6}, \quad
  \wa^{\SSEE} = -\frac{P_{sc}}{I_g}=\val{WA_d6}.""")
rep(r"  & $-0.840\ [\mathrm{alg.}]$", r"  & $\val{W0_d3}\ [\mathrm{alg.}]$")
rep(r"  & $-0.670\ [\mathrm{alg.}]$", r"  & $\val{WA_d3}\ [\mathrm{alg.}]$")
rep(r"$w_0=\val{W0_d6}$ lies $(-0.840+1.57)/0.50\simeq1.5\sigma$ from it.",
    r"$w_0=\val{W0_d6}$ lies $(w_0+1.57)/0.50=\val{w0_cmb_solo_sig}\sigma$ from it.")

# --- resumen: dos parametros muestreados, no uno ---
rep(r"""With $(w_0,w_a)$ fixed algebraically and one free parameter $H_0$, SSEE is
favoured by $\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$ over \LCDM\ and $\val{p2_dBIC_cpl}$ over CPL, and
predicts the DESI~DR2 test set better in leave-one-out cross-validation ---
so the $\wz$--$\wa$ prediction is genuinely preferred by current BAO data.""",
    r"""With $(w_0,w_a)$ fixed algebraically and two sampled parameters ($H_0$ and
$\Omega_b h^2$), against the same DESI~DR2 data and the same compressed Planck prior as
\LCDM\ and CPL, SSEE is favoured by $\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$ over \LCDM\ and
$\val{p2_dBIC_cpl}$ over CPL, and predicts the DESI~DR2 test set better in leave-one-out
cross-validation.""")
rep(r"""for which the SSEE sound horizon matches \LCDM\
($r_d^{\SSEE}/r_d^{\LCDM}=\val{p2_rd_ratio}$)""",
    r"""for which the SSEE sound horizon at the algebraic point matches that of
\LCDM\ at the Planck~2018 parameters ($r_d^{\SSEE}/r_d^{\LCDM}=\val{p2_rd_ratio}$, CAMB)""")

# --- introduccion ---
rep(r"""carries zero dimensionless fitted parameters, and no WIMP, QCD-axion, or SUSY
dark-matter particle is introduced; phenomenological extensions in the dark-matter
sector (Paper~6) introduce ans\"atze tracked as open problems
(see Paper~1, \S1.3, and \texttt{OPEN\_PROBLEMS.md}).
Paper~1, Appendix~A provides a complete Lagrangian (k-essence + Israel--Stewart
viscosity) derived algebraically from $\{\varphi,\pi\}$, with zero free parameters
at the EFT background level.""",
    r"""carries zero dimensionless fitted parameters, and no WIMP, QCD-axion, or SUSY
dark-matter particle is introduced (the cold dark matter density is the algebraic
identity $\omega_c=\mathrm{KAL_0}\,\omega_b\,n_s$; what it is made of is an open problem,
see Paper~1, \S1.3, and \texttt{OPEN\_PROBLEMS.md}).
The effective action of the dark-energy field is that of Paper~7; Paper~1,
Appendix~A gives its motivation, not an independent Lagrangian.""")
rep(r"""  \item Provide a roadmap for the modified Friedmann CMB analysis
    and semi-linear transfer function required in Paper~3.""",
    r"""  \item Prepare the full CMB likelihood test of the same background, carried
    out in Paper~3.""")
rep(r"""this paper establishes which
sectors pass Bayesian scrutiny and which require a modified background
treatment.""",
    r"""this paper establishes which
sectors pass Bayesian scrutiny.""")

# --- seccion 2: saturacion, no densidad ---
rep(r"""not as the fundamental dynamics.  In the \SSEE\ framework, the dark-energy
density saturates at the finite $T_r/M_v$ boundary of the action at
$a\to\infty$, guaranteeing universal stability; see Paper~1 \S3.4
\citep{SSEE_paperI} for the full stability argument.
The equation-of-state-sector saturation quantity is similarly fixed:
$s_{\rm DE}^{\SSEE}=T_r/M_v\approx0.840$ (not a density fraction), with the
algebraic matter-sector complement
\begin{equation}
  s_m = 1-s_{\rm DE}^{\SSEE} \approx 0.160.
  \label{eq:om_eff}
\end{equation}""",
    r"""not as the fundamental dynamics; its extrapolation to $a\to\infty$ is not a
prediction of the model, and the stability of the field is that of the
effective action of Paper~7 \citep{SSEE_paperI}.
The equation-of-state saturation is similarly fixed:
$s_{\rm DE}^{\SSEE}=T_r/M_v=\val{S_DE_d6}=-w_0$ (not a density fraction), with its
complement, also a number of the equation of state,
\begin{equation}
  s_m = 1-s_{\rm DE}^{\SSEE} = 1+w_0 = \val{S_M_d6}.
  \label{eq:om_eff}
\end{equation}""")
rep(r"""The only sampled cosmological parameter is $H_0$; the algebraic
quantities ($\wz,\wa,s_{\rm DE}^{\SSEE},\KALz$) are fixed by geometry
as described in Section~\ref{sec:model}. The equation-of-state-sector
quantities $s_{\rm DE}^{\SSEE}=T_r/M_v\approx0.840$ and
$s_m=1-s_{\rm DE}^{\SSEE}\approx0.160$ do not enter the background
densities (see \S\ref{sec:folding}).""",
    r"""The sampled parameters are $H_0$ and $\Omega_b h^2$; the algebraic
quantities ($\wz,\wa,s_{\rm DE}^{\SSEE},\KALz$) are fixed by geometry
as described in Section~\ref{sec:model}. The equation-of-state
quantities $s_{\rm DE}^{\SSEE}=T_r/M_v=\val{S_DE_d6}$ and
$s_m=1-s_{\rm DE}^{\SSEE}=\val{S_M_d6}$ do not enter the background
densities (see \S\ref{sec:folding}).""")
rep(r"\caption{\textit{Left}: $s_{\rm DE}^{\SSEE}=T_r/M_v\approx0.840$ (red line),",
    r"\caption{\textit{Left}: $s_{\rm DE}^{\SSEE}=T_r/M_v=\val{S_DE_d3}$ (red line),")
rep(r"""  \item Document why the naive $\OmDE^{\SSEE}\approx0.840$ vs""",
    r"""  \item Document why the naive $\OmDE^{\SSEE}\approx\val{S_DE_d3}$ vs""")

# --- titular CMB: chi2 minimo, no MCMC ---
rep(r"""(canonical $\Delta\mathrm{BIC}=\val{b1_dBIC}$ full \texttt{plik}
MCMC; $-26.03$ \texttt{plik\_lite} TTTEEE+low-$\ell$ point estimate)""",
    r"""(canonical $\Delta\mathrm{BIC}=\val{b1_dBIC}$ full \texttt{plik}, minimum $\chi^2$ of
each model; $\val{lite_dBIC}$ \texttt{plik\_lite} TTTEEE+low-$\ell$)""")
rep(r"""likelihood ($\Delta\mathrm{BIC}=\val{b1_dBIC}$, full \texttt{plik} MCMC).""",
    r"""likelihood ($\Delta\mathrm{BIC}=\val{b1_dBIC}$, full \texttt{plik}, minimum $\chi^2$ of each model).""")
rep(r"""independently favours \SSEE\ at $\Delta\mathrm{BIC}=\val{b1_dBIC}$ (full \texttt{plik} MCMC).""",
    r"""independently favours \SSEE\ at $\Delta\mathrm{BIC}=\val{b1_dBIC}$ (full \texttt{plik}, minimum $\chi^2$ of each model).""")

# --- r_d: CAMB, no la formula de potencias ---
rep(r"""with the sound horizon from a power-law expansion about the Planck~2018
point \citep{Planck2018}, used here as an auxiliary approximation for model
comparison. Its exponents are the local logarithmic derivatives of the
\citet{EisensteinHu1998} fitting formula at that point, and its normalization
is the Boltzmann value there (compare the global fit of
\citealt{Aubourg2015}):
\begin{equation}
  r_d = 147.27\!\left(\frac{\Omega_m h^2}{0.1432}\right)^{\!-0.255}\!
  \left(\frac{\Omega_b h^2}{0.02237}\right)^{\!-0.134}\!\text{Mpc}.
  \label{eq:rd}
\end{equation}""",
    r"""with the sound horizon $r_d$ computed by CAMB for every sample, from its
$(\omega_b,\omega_m)$ and each model's own $\sum m_\nu$ (the algebraic value for
\SSEE, $0.06$\,eV for \LCDM\ and CPL). An earlier version used a power-law
expansion of the \citet{EisensteinHu1998} formula about the Planck point
\citep[compare][]{Aubourg2015}, whose normalization ran $0.13\%$ long; it is
retired. The production chain of \S\ref{sec:prior_mira} also takes $D_M$ and $D_H$
from CAMB; the three-model run integrates $E(z)$.""")

# --- seccion del ancla: el perfil CMB, no «minimizado exactamente» ---
rep(r"""the CMB $\chi^2$ is minimised at the global rate returned by the SSEE
screening cascade (Papers~9--10), which takes the measured SH0ES rate as input:""",
    r"""the CMB $\chi^2$ profile has its minimum at
$H_0=\val{perfil_h0_min}\pm\val{perfil_h0_sig}$ (parabola through the grid; lowest node at the
value below), $\val{perfil_h0_d}\sigma$ from the global rate returned by the SSEE
screening cascade (Papers~9--10), which takes the measured SH0ES rate as input:""")
rep(r"""The background
$H$ and the CMB anchor coincide --- they are not two numbers --- and the
matter density follows""",
    r"""The background
$H$ and the CMB anchor agree within the width of the CMB profile, and the
matter density follows""")
rep(r"""algebra, the Planck~\texttt{plik\_lite} likelihood is minimised exactly at
that value (Paper~3, \S\ref{sec:prior_mira}). The background $H$ and the
CMB anchor therefore coincide --- they are the same number, $H_0^{\rm glob}=\val{H0_GLOBAL_d3}\pm\val{p9_hglob_sigma}$ ---""",
    r"""algebra, the Planck~\texttt{plik\_lite} profile has its minimum at
$\val{perfil_h0_min}\pm\val{perfil_h0_sig}$, $\val{perfil_h0_d}\sigma$ from that value
(\S\ref{sec:prior_mira}). The background $H$ and the CMB anchor therefore agree,
$H_0^{\rm glob}=\val{H0_GLOBAL_d3}\pm\val{p9_hglob_sigma}$,""")

# --- produccion: omega_m fijo, Omega_m derivado ---
rep(r"""The matter density is not sampled. The background geometry --- $E(z)$, the
sound horizon $r_d$, and every BAO distance --- uses the \emph{total} algebraic
matter density $\Omega_{m,\mathrm{CMB}}=\omega_m/h^2=\val{OMEGA_M_TOTAL_d6}$
(\S\ref{sec:folding}, \S\ref{sec:results_cosmo}); the value""",
    r"""The matter density is not sampled. The background geometry --- $E(z)$, the
sound horizon $r_d$, and every BAO distance --- uses the \emph{total} algebraic
matter density $\omega_m=\val{OMEGA_M_H2_d5}$, fixed, with $\Omega_m=\omega_m/h^2$
derived for each sample ($\val{OMEGA_M_TOTAL_d6}$ at $H_0^{\rm glob}$;
\S\ref{sec:folding}, \S\ref{sec:results_cosmo}); the value""")
rep(r"""equation of state, not a density, and does \emph{not} enter $E(z)$. Thus $r_d$ is computed from
$\omega_m = \Omega_{m,\mathrm{CMB}}(H_0/100)^2$ self-consistently.""",
    r"""equation of state, not a density, and does \emph{not} enter $E(z)$. Thus $r_d$ is computed from
the algebraic $\omega_m$ at every sample.""")
rep(r"""$\Omega_b h^2 = (\pi-\varphi)/[3(\varphi+\pi)^2] = \val{OMEGA_B_H2_d6}$ (Paper~4)
at $0.4\sigma$.""",
    r"""$\Omega_b h^2 = (\pi-\varphi)/[3(\varphi+\pi)^2] = \val{OMEGA_B_H2_d6}$ (Paper~4)
at $\val{wb_bbn_sig}\sigma$.""")

# --- priors del run de 3 modelos: mismos datos para los tres ---
rep(r"""All models share a BBN prior $\Omega_b h^2\sim\mathcal{N}(0.02218,\,0.00055^2)$ \citep{Schoneberg2024}.
For \LCDM\ and CPL, the full 3D Planck prior is applied. For \SSEE,
the Planck prior reduces to a marginal Gaussian on $H_0$ only, since
$\Omega_m$ is fixed. CPL carries weakly informative priors
$\wz\sim\mathcal{N}(-1,0.5^2)$ and $\wa\sim\mathcal{N}(0,1^2)$.""",
    r"""In the three-model comparison all three models see the same data: the 13
DESI~DR2 points and the full compressed Planck prior on $(H_0,\Omega_m,\omega_b)$.
For \SSEE\ $\Omega_m=\omega_m/h^2$ is derived for each sample, not sampled. CPL
carries in addition weakly informative priors $\wz\sim\mathcal{N}(-1,0.5^2)$ and
$\wa\sim\mathcal{N}(0,1^2)$. The production chain of the \SSEE\ $H_0$ posterior
(\S\ref{sec:prior_mira}) replaces the Planck prior by the $H_0^{\rm glob}$ prior and a
BBN prior $\Omega_b h^2\sim\mathcal{N}(0.02218,\,0.00055^2)$ \citep{Schoneberg2024}.""")

# --- tabla de jerarquia ---
rep(r"""\textbf{Sampled} = inferred via MCMC; \textbf{Derived} = computed from
sampled values; \textbf{Mapped} = structural hypothesis (acoustic-scale mapping), to be validated in Paper~3.}""",
    r"""\textbf{Sampled} = inferred via MCMC; \textbf{Derived} = computed from
sampled values.}""")
rep(r"""$H_0$                & \textbf{Sampled}           & $\mathcal{U}[60,80]$      & Only cosmological free parameter \\
$\Omega_b h^2$       & \textbf{Sampled}           & BBN prior                 & Shared with \LCDM, CPL \\
$r_d$                & \textbf{Derived}           & Friedmann background      & Eq.~\eqref{eq:rd}; carries background mismatch \\
$\rdeff$             & \textbf{Mapped (hypothesis)}& Acoustic-scale hypothesis & Eq.~\eqref{eq:rd_mapping}; Paper~3 test \\""",
    r"""$H_0$                & \textbf{Sampled}           & Gaussian prior; $40<H_0<100$ & Planck (3 models) or $H_0^{\rm glob}$ (production) \\
$\Omega_b h^2$       & \textbf{Sampled}           & Planck or BBN prior       & Planck (3 models), BBN (production) \\
$\Omega_m$           & \textbf{Derived}           & $\omega_m/h^2$            & $\omega_m$ algebraic, fixed \\
$r_d$                & \textbf{Derived}           & CAMB, $(\omega_b,\omega_m,\sum m_\nu)$ & Eq.~\eqref{eq:rd_mapping} at the algebraic point \\""")

# --- tabla de posteriores: Omega_m de SSEE es derivado ---
rep(r"""  & $\val{OMEGA_M_TOTAL_d6}\ [\mathrm{total}]$""",
    r"""  & $\val{p2_ssee_Om_mediana}^{+\val{p2_ssee_Om_mas}}_{-\val{p2_ssee_Om_menos}}\ [\mathrm{derived}]$""")

# --- plano w0-wa: rho y chi2 por \val ---
rep(r"""(DESI+CMB+Pantheon+, $w_0=-0.838\pm0.055$, $w_a=-0.617\pm0.208$;
arXiv:2503.14738, eq.~26; moments and $\rho=-0.894$ measured directly from the
official DESI chains, Zenodo record 16644577) is:""",
    r"""(DESI+CMB+Pantheon+, $w_0=-0.838\pm0.055$, $w_a=-0.617\pm0.208$;
arXiv:2503.14738, eq.~26; moments and $\rho=\val{p2_w0wa_rho_ec26}$ measured directly from the
official DESI chains, Zenodo record 16644577) is:""")
rep(r"""  = \Delta\mathbf{w}^\top\mathbf{C}^{-1}\Delta\mathbf{w} = 0.42""",
    r"""  = \Delta\mathbf{w}^\top\mathbf{C}^{-1}\Delta\mathbf{w} = \val{p2_chi2_2D_ec26}""")
rep(r"""chain-measured correlations $\rho=-0.905$ to $-0.978$): the""",
    r"""chain-measured correlations $\rho=\val{p2_w0wa_rho_ec28}$ to $\val{p2_w0wa_rho_ec25}$): the""")
rep(r"""exact against Pantheon+ ($\Delta w_0=-0.04\sigma$). The result is robust to
the correlation ($\rho\in[-0.92,-0.70]$ would shift Pantheon+ by
$<0.2\sigma$; the chain-measured value is used).
This distance means the \SSEE\ algebraic point""",
    r"""exact against Pantheon+ ($\Delta w_0=\val{p2_dw0_ec26}\sigma$); the chain-measured
correlation is used throughout.
This distance means the \SSEE\ algebraic point""")
rep(r"""well inside the DESI~DR2 $1\sigma$ contour in the $\wz$--$\wa$ plane.""",
    r"""inside the $1\sigma$ contour of the DESI~DR2+CMB+Pantheon+ posterior in the $\wz$--$\wa$ plane.""")
rep(r"""    DESI+CMB+Pantheon+ & $-0.894$ &""", r"""    DESI+CMB+Pantheon+ & $\val{p2_w0wa_rho_ec26}$ &""")
rep(r"""    DESI+CMB+DES~Y5    & $-0.905$ &""", r"""    DESI+CMB+DES~Y5    & $\val{p2_w0wa_rho_ec28}$ &""")
rep(r"""    DESI+CMB+Union3    & $-0.933$ &""", r"""    DESI+CMB+Union3    & $\val{p2_w0wa_rho_ec27}$ &""")
rep(r"""    DESI+CMB (no SN)   & $-0.978$ &""", r"""    DESI+CMB (no SN)   & $\val{p2_w0wa_rho_ec25}$ &""")

# --- r_d en eq:rd_ratio ---
rep(r"""  r_d^{\SSEE}=147.17\ \text{Mpc},\quad""", r"""  r_d^{\SSEE}=\val{p2_lyaB_rd}\ \text{Mpc},\quad""")
rep(r"""the \SSEE\ sound horizon matches \LCDM\ ($r_d=\val{p2_lyaB_rd}$ vs $147.10$\,Mpc, CAMB) and \SSEE\ is""",
    r"""the \SSEE\ sound horizon matches \LCDM\ ($r_d=\val{p2_lyaB_rd}$ vs $\val{p2_rd_lcdm}$\,Mpc, CAMB) and \SSEE\ is""")

# --- «sector frio» 0.160 -> saturacion; sin el 2.9 sigma sin log ---
rep(r"""\emph{coincides} with $H_0^{\rm glob}$ rather than pulling away from it: the
earlier ``$2.9\sigma$ below anchor'' reading was the cold sector $0.160$
misplaced in $E(z)$, now corrected.""",
    r"""\emph{coincides} with $H_0^{\rm glob}$ rather than pulling away from it: an
earlier reading of a shift below the anchor came from the saturation
$1+w_0=\val{S_M_d6}$ misplaced in $E(z)$, now corrected.""")
rep(r"""  Planck; the earlier ``$2.9\sigma$ below anchor'' reading was the cold sector
  $0.160$ misplaced in $E(z)$, now corrected.}""",
    r"""  Planck; an earlier reading of a shift below the anchor came from the saturation
  $1+w_0=\val{S_M_d6}$ misplaced in $E(z)$, now corrected.}""")
rep(r"""reading --- a $2.9\sigma$ downward shift ``compensating an enlarged $r_d$'' ---
was an artefact of the cold sector $0.160$ misplaced in $E(z)$: with the correct""",
    r"""reading --- a downward shift ``compensating an enlarged $r_d$'' ---
was an artefact of the saturation $1+w_0=\val{S_M_d6}$ misplaced in $E(z)$: with the correct""")
rep(r"""arose only from comparing the cold \emph{sector} ($1+w_0=\val{S_M_d6}$) against the
Planck \emph{total} $\Omega_m$ --- a category error of matching a partial
density to a full one, traced to the dynamical value being used in the
background geometry where the total belongs (corrected here).""",
    r"""arose only from comparing $1+w_0=\val{S_M_d6}$, a number of the equation of state,
against the Planck matter density $\Omega_m$ --- a category error, traced to that
number being used in the background geometry where the matter density belongs
(corrected here).""")
rep(r"""drafts was an artefact of placing the cold sector $1+w_0=\val{S_M_d6}$ in the""",
    r"""drafts was an artefact of placing the saturation $1+w_0=\val{S_M_d6}$ in the""")
rep(r"""cold sector $1+w_0=\val{S_M_d6}$ as the background matter density; with the correct""",
    r"""saturation $1+w_0=\val{S_M_d6}$ as the background matter density; with the correct""")

# --- Savage-Dickey: escala ---
rep(r"""CPL posterior --- strong evidence on the Jeffreys scale --- and leave-one-out""",
    r"""CPL posterior ($B=\val{p2_B_sddr}$: at the threshold of ``strong'' on Jeffreys'
original scale, ``weak'' on the stricter scale of \citealt{Trotta2008}) --- and leave-one-out""")
rep(r"""On the Jeffreys scale~\cite{Trotta2008} $\ln B=\val{p2_lnB_signo}$ ($>2.3$) constitutes
\emph{strong} evidence in favour of the SSEE dynamic sector within
the CPL framework.""",
    r"""With $B=\val{p2_B_sddr}$ ($\ln B=\val{p2_lnB_signo}$) the evidence for the SSEE dynamic sector
within the CPL framework sits at the threshold of ``strong'' on Jeffreys' original
scale ($B>10$; \citealt{Jeffreys1961}) and is ``weak'' on the stricter scale of
\citet{Trotta2008} ($1<\ln B<2.5$); we read it as positive, not decisive.""")
rep(r"""  Jeffreys criterion: $|\Delta| > 5$ = strong.""",
    r"""  Scale of \citet{KassRaftery1995} for $\Delta$BIC: 2--6 positive, 6--10 strong.""")
rep(r"""confirming that all three chains are well-converged.""",
    r"""as expected for data-dominated, near-Gaussian posteriors.""")

# --- sensibilidad al prior ---
rep(r"""Removing the Planck $H_0$ prior shifts the \SSEE\ posterior by
$<0.3\sigma$. The BAO data dominate the $H_0$ constraint.
\textit{This confirms that the quoted posteriors are driven by the BAO
geometry rather than the CMB prior, making them robust to prior choice.}""",
    r"""Under the compressed Planck prior the \SSEE\ posterior is
$H_0=\val{p2_ssee_H0_mediana}\pm\val{p2_ssee_H0_std}$; with a flat prior (DESI~DR2 and a BBN prior
on $\omega_b$ only) it is $\val{h0_desi_plano}\pm\val{h0_desi_plano_s}$. The BAO data carry
most of the constraint; the prior narrows it but does not move it.""")

# --- MCMC completo: de su log ---
rep(r"""(four chains, $\sim$53k post-burn-in samples, Gelman--Rubin $R-1<0.003$).
The free-fit posterior $(\wz,\wa)=(-0.655,-1.104)$ \emph{excludes} the cosmological""",
    r"""(four chains, $\val{mf_filas}$ samples after discarding the first $30\%$ of each,
Gelman--Rubin $R-1=\val{mf_rminus1}$ across the four chains).
The free-fit posterior $(\wz,\wa)=(\val{mf_w_media},\val{mf_wa_media})$ \emph{excludes} the cosmological""")
rep(r"""  + lensing + DESI~DR2 + $f\sigma_8$, with $\wz,\wa$ free; $R-1<0.003$).""",
    r"""  + lensing + DESI~DR2 + $f\sigma_8$, with $\wz,\wa$ free; $R-1=\val{mf_rminus1}$).""")

# --- tension de Hubble: errores combinados ---
rep(r"""lies within $1.1\sigma$ of Planck~2018 and is consistent""",
    r"""lies $\val{hglob_planck_sig}\sigma$ from Planck~2018 (errors combined) and is consistent""")

# --- falsadores ---
rep(r"""    $\sum m_\nu^{\rm active}=0.0685$\,eV at $>3\sigma$, the algebraic neutrino""",
    r"""    $\sum m_\nu^{\rm active}=\val{SUM_MNU_EV_d4}$\,eV at $>3\sigma$, the algebraic neutrino""")
rep(r"""  \item \textbf{If future high-$z$ BAO or CMB measure} $r_d$ outside
    $147\pm3$\,Mpc, the $\omega_m$-direct construction
    ($r_d=\val{p2_lyaB_rd}$\,Mpc from the algebraic $\omega_m$) is falsified ---""",
    r"""  \item \textbf{If a determination of} $r_d$ that does not assume \LCDM\ places it
    more than $3\sigma$ from $\val{p2_lyaB_rd}$\,Mpc, the $\omega_m$-direct construction
    (CAMB from the algebraic $\omega_m$) is falsified ---""")

# --- conclusion central: los criterios son de DESI + Planck ---
rep(r"""\noindent\textbf{Central finding}: an algebraic background with no fitted
dark-energy parameter describes DESI~DR2, the CMB and galaxy-cluster masses as
well as \LCDM, and is preferred on every information criterion because it
does so with fewer free parameters.""",
    r"""\noindent\textbf{Central finding}: an algebraic background with no fitted
dark-energy parameter describes DESI~DR2 and the compressed Planck prior as well as
\LCDM, and is preferred on every information criterion because it does so with
fewer free parameters; galaxy-cluster masses, tested separately, are consistent
with its matter content as with that of \LCDM.""")
rep(r"""with the BOSS galaxy clustering (Paper~6). Virialised clusters confirm, at a
third and independent scale, that the matter-to-baryon ratio it implies is the
one structures actually carry.""",
    r"""with the BOSS galaxy clustering (Paper~6). Virialised clusters are consistent,
at a third and independent scale and given the IGIMF baryon census, with the
matter-to-baryon ratio it implies.""")

# --- bibliografia: Kass & Raftery ---
rep(r"""\bibitem[Jeffreys(1961)]{Jeffreys1961}""",
    r"""\bibitem[Kass \& Raftery(1995)]{KassRaftery1995}
Kass, R.~E., \& Raftery, A.~E.\ (1995).
Bayes factors.
\textit{J.~Am.\ Statist.\ Assoc.} \textbf{90}, 773.

\bibitem[Jeffreys(1961)]{Jeffreys1961}""")

open(P, "w").write(s)
print("P2: reemplazos aplicados")
