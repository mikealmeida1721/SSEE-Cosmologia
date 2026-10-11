#!/usr/bin/env python3
"""Quinta lectura P3 (2026-10-11): reemplazos exactos; aborta si un conteo no casa."""
import sys

P = "manuscript/SSEE_Paper3_CMB.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


# --- resumen ---
rep(r"(DESI+CMB+Pantheon+; $0.2$--$1.8\sigma$ across SN compilations)",
    r"(DESI+CMB+Pantheon+; up to $\val{p2_w0wa_ssee_ec27_d1}\sigma$ across the other SN compilations)")
rep(r"""yields $\Delta\mathrm{BIC}=\val{b1_dBIC}$, decisively favouring SSEE on the Jeffreys scale.
(A \texttt{plik\_lite} point-estimate cross-check gives a more conservative
$\Delta\mathrm{BIC}=\val{lite_dBIC}$.)""",
    r"""yields $\Delta\mathrm{BIC}=\val{b1_dBIC}$, very strong evidence for SSEE on the scale of
\citet{KassRaftery1995}. (A \texttt{plik\_lite} cross-check, with $\{A_s,\tau\}$ also
minimized, gives a more conservative $\Delta\mathrm{BIC}=\val{lite_dBIC}$.)""")
rep(r"""  = \frac{\val{OMEGA_M_H2_d5}}{0.6796^2} = 0.3089,""",
    r"""  = \frac{\val{OMEGA_M_H2_d5}}{\val{h_glob_d4}^2} = \val{OMEGA_M_TOTAL_d4},""")

# --- tabla de constantes: roles vigentes (los de P1) ---
rep(r"""$\mathrm{AURA}$ & $\varphi+\beta$ & $\val{AURA_d5}\ldots$ & Dimensional limit 1 \\
$\mathrm{MIRA}$ & $\mathrm{AURA}/2$ & $\val{MIRA_d5}\ldots$ & Observational frequency \\""",
    r"""$\mathrm{AURA}$ & $\varphi+\beta$ & $\val{AURA_d5}\ldots$ & Resonance limit \\
$\mathrm{MIRA}$ & $\mathrm{AURA}/2$ & $\val{MIRA_d5}\ldots$ & Screening amplitude (Paper~9) \\""")

# --- omega_m directo ---
rep(r"""and $\omega_\nu=\Sigma m_\nu^{\rm active}/93.14=0.00074$""",
    r"""and $\omega_\nu=\Sigma m_\nu^{\rm active}/93.14=\val{OMEGA_NU_H2_d6}$""")
rep(r"""  \Omega_{m,\mathrm{CMB}} = \frac{\omega_m}{h^2} = \frac{\val{OMEGA_M_H2_d5}}{0.6796^2} = 0.3089""",
    r"""  \Omega_{m,\mathrm{CMB}} = \frac{\omega_m}{h^2} = \frac{\val{OMEGA_M_H2_d5}}{\val{h_glob_d4}^2} = \val{OMEGA_M_TOTAL_d4}""")
rep(r"""    = \frac{\omega_b + \mathrm{KAL}_0\,\omega_b\,n_s + \omega_\nu}{h^2}
    = 0.3089,""",
    r"""    = \frac{\omega_b + \mathrm{KAL}_0\,\omega_b\,n_s + \omega_\nu}{h^2}
    = \val{OMEGA_M_TOTAL_d4},""")
rep(r"""$\mathrm{KAL}_0=\beta+\pi\approx5.521$ that sets""",
    r"""$\mathrm{KAL}_0=\beta+\pi=\val{KAL0_d3}$ that sets""")
rep(r"""SSEE predicts a \emph{single} matter density, $\Omega_m=\val{OMEGA_M_TOTAL_d6}$, at every
redshift and for every probe. A weak-lensing or BAO analysis that required a
background matter density significantly different from $0.3089$ --- in either
direction, at any redshift --- would falsify the framework.""",
    r"""SSEE predicts a \emph{single} present-day matter density, $\Omega_m=\val{OMEGA_M_TOTAL_d6}$
(at $H_0^{\rm glob}$), the same for every probe. A weak-lensing or BAO analysis that
required a background matter density significantly different from it --- in either
direction --- would falsify the framework.""")

# --- tabla CAMB: el script usa el omega_b PROPIO de SSEE y omega_c, no 0.02237 ---
rep(r"""$\Omega_b h^2$ & 0.02237 & Planck 2018 prior \\
$\Omega_{m,\mathrm{CMB}}$ & 0.3089 & $\omega_m/h^2$ (forward) \\""",
    r"""$\Omega_b h^2$ & \val{OMEGA_B_H2_d6} & $(\pi-\varphi)/[3(\varphi+\pi)^2]$ (Paper~4) \\
$\Omega_c h^2$ & \val{OMEGA_C_H2_d6} & $\mathrm{KAL}_0\,\omega_b\,n_s$ (forward) \\""")
rep(r"""  $\val{logA_aj_ssee}$. The recovered $\tau$ sits
  within $0.1\sigma$ of the Phase-B posterior $\val{b1_tau_ssee}\pm\val{b1_tau_ssee_s}$, so the fiducial
  choice is doing no work.}""",
    r"""  $\val{logA_aj_ssee}$. The recovered $\tau$ sits
  inside the Phase-B posterior $\val{b1_tau_ssee}\pm\val{b1_tau_ssee_s}$, so the fiducial
  choice is doing no work.}""")
rep(r"""The baryon density is fixed to the Planck~2018 prior $\Omega_b h^2 = 0.02237$.
The SSEE algebraic value derived in Paper~4, $\Omega_b h^2 = (\pi-\varphi)/[3(\varphi+\pi)^2]
= \val{OMEGA_B_H2_d6}$, agrees with this prior at $0.3\sigma$ ($0.02237\pm0.00015$); the $0.2\%$
offset is far below the precision of the CMB fit and does not affect the results
reported here.""",
    r"""The baryon density is the SSEE algebraic value of Paper~4,
$\Omega_b h^2 = (\pi-\varphi)/[3(\varphi+\pi)^2] = \val{OMEGA_B_H2_d6}$, which lies
$\val{wb_planck_sig}\sigma$ from the Planck~2018 value $0.02237\pm0.00015$; each model
runs with its own ingredients (the \LCDM\ reference uses the Planck~2018 parameters,
with $\sum m_\nu=0.06$\,eV). An earlier version of this table listed the Planck value
for \SSEE; the computation already used the algebraic one.""")
rep(r"""Although $w_0+w_a=-1.510<-1$, this does not imply a phantom Big Rip:
CPL is a local parametrisation only, and the \SSEE\ energy density saturates
at the finite $T_r/M_v$ boundary at $a\to\infty$ (Paper~1 \S3.4 \citep{AlmeidaSSEE2026a}).""",
    r"""Although $w_0+w_a=\val{w0_mas_wa}<-1$, this does not imply a phantom Big Rip:
CPL is a local parametrisation only, its extrapolation to $a\to\infty$ is not a
prediction of the model, and the stability of the field is that of the effective
action of Paper~7 \citep{AlmeidaSSEE2026a}.""")

# --- horizonte sonoro ---
rep(r"""With $\Omega_{m,\mathrm{CMB}}=0.3089$ and the parameters above, CAMB yields:""",
    r"""With $\omega_b$, $\omega_c$ and $\sum m_\nu$ of Table~\ref{tab:camb_params}, CAMB yields:""")
rep(r"""in agreement with the Planck~2018 directly measured value
$r_d^{\mathrm{obs}}=147.09\pm0.26$ Mpc \citep{Planck2018} at $\val{p3_rd_sig_post}\sigma$.""",
    r"""in agreement with the value Planck~2018 derives under \LCDM,
$r_d=147.09\pm0.26$ Mpc \citep{Planck2018}, at $\val{p3_rd_sig_post}\sigma$.""")
rep(r"""$1.04109\pm0.00030$ --- the earlier $6.66\sigma$ ``tension'' was an artefact of
the cold sector $1+w_0=\val{S_M_d6}$ misplaced in $E(z)$, removed once the total
$\Omega_{m,\mathrm{CMB}}$ sets the geometry.
No Folding Symmetry multiplier and no matter factor are applied; the
$\omega_m$-direct CMB matter density ($\Omega_{m,\mathrm{CMB}}=0.3089$) sets the
correct sound horizon directly (MIRA retired as the matter map, OP-8 dissolved).""",
    r"""$1.04109\pm0.00030$ --- the earlier $6.66\sigma$ ``tension'' was an artefact of
the saturation $1+w_0=\val{S_M_d6}$ misplaced in $E(z)$, removed once the total
$\Omega_{m,\mathrm{CMB}}$ sets the geometry.
No Folding Symmetry multiplier and no matter factor are applied; the
$\omega_m$-direct densities set the sound horizon directly (MIRA retired as the
matter map, OP-8 dissolved).""")

# --- residuos: no hay exceso; quitar la frase sin contenido ---
rep(r"""The TE and EE spectra show the smallest discrepancies ($|\Delta\chi^2_r|\le0.001$
each), indicating that SSEE reproduces the polarization anisotropies
almost identically to $\Lambda$CDM.""",
    r"""The TE and EE spectra agree with \LCDM\ to the third decimal
($\Delta\chi^2_r=\val{p3_dchi2r_TE}$ and $\val{p3_dchi2r_EE}$).""")
rep(r"""with the \val{p3_N_PP} Planck MV bandpowers, both $\chi^2_r<1$ indicating a good fit.
All residuals are consistent with a non-parametric model.

\subsection{Interpretation of residuals}

The excess $\Delta\chi^2_r\lesssim0.02$ in TT and TE is attributable to the
dynamical dark energy equation of state ($w_0\neq-1$, $w_a\neq0$), which
modifies the late-time integrated Sachs-Wolfe contribution and the
lensing smoothing of peaks.
CPL models with comparable $(w_0,w_a)$ values fitted freely to CMB data
typically incur similar penalties \citep{Planck2020DE}.
""",
    r"""with the \val{p3_N_PP} Planck MV bandpowers, both $\chi^2_r<1$ indicating a good fit.

\subsection{Interpretation of residuals}

There is no excess to explain: the dynamical equation of state ($w_0\neq-1$,
$w_a\neq0$) changes the late-time integrated Sachs--Wolfe contribution and the
lensing smoothing of the peaks, but at the level of these spectra the effect is
below the third decimal of $\chi^2_r$ (cf.\ the CPL fits of \citealt{Planck2020DE}).
""")
rep(r"""smaller parameter set. This diagonal cross-check is evaluated at the global
global rate""", r"""smaller parameter set. This diagonal cross-check is evaluated at the
global rate""")
rep(r"""The diagonal approximation neglects bin-to-bin covariances in the Planck 2018 bandpowers. Based on the Planck 2018 likelihood analysis \citep{PlanckLikelihood2020}, off-diagonal elements contribute corrections of $\lesssim5\%$ to $\chi^2$ for $\ell>30$. To ensure""",
    r"""The diagonal approximation neglects bin-to-bin covariances in the Planck 2018 bandpowers \citep{PlanckLikelihood2020}, so its $\chi^2$ is only indicative. To ensure""")

# --- plik_lite: minimizado en A_s, tau; numeros por \val ---
rep(r"""reproduces the dimensionless target $3(\varphi+\pi)^2$ to $4.2\times10^{-6}$; it is not fitted""",
    r"""reproduces the dimensionless target $3(\varphi+\pi)^2$ to $\val{p9_hglob_residuo}$~km\,s$^{-1}$\,Mpc$^{-1}$; it is not fitted""")
rep(r"""The two models therefore fit \emph{equally well}: $\Delta\chi^2 = -0.010$, which""",
    r"""The two models therefore fit \emph{equally well}: $\Delta\chi^2 = \val{lite_dchi2}$, which""")
rep(r"""    \Delta\mathrm{BIC} = -0.010 + (2 - 6)\ln(669) = -26.03.
\end{equation}
A $\Delta\mathrm{BIC} < -10$ constitutes decisive evidence on the Jeffreys scale. Even under a hyper-conservative penalty where SSEE is assigned $k=4$ (additionally counting two algebraically-fixed inputs, $\omega_b$ and $H_0$, as if they were fitted), the result remains $\Delta\mathrm{BIC} = -0.010 + (4-6)\ln(669) = -13.02$, still strongly favouring""",
    r"""    \Delta\mathrm{BIC} = \val{lite_dchi2} + (2 - 6)\ln(669) = \val{lite_dBIC}.
\end{equation}
A $|\Delta\mathrm{BIC}|>10$ is very strong evidence on the scale of \citet{KassRaftery1995}. Even under a hyper-conservative penalty where SSEE is assigned $k=4$ (additionally counting two algebraically-fixed inputs, $\omega_b$ and $H_0$, as if they were fitted), the result remains $\Delta\mathrm{BIC} = \val{lite_dchi2} + (4-6)\ln(669) = \val{lite_dBIC_k4}$, still strongly favouring""")
rep(r"""The point-estimate scan of \S\ref{sec:cobaya} evaluates""",
    r"""The fixed-anchor evaluation of \S\ref{sec:cobaya} evaluates""")
rep(r"""reimplementation of \texttt{clik} (validated to $|\Delta\ln\mathcal{L}|<10^{-5}$ against the released test point), so no""",
    r"""reimplementation of \texttt{clik}, so no""")
rep(r"""Chains are run to Gelman--Rubin criterion $R{-}1 < 0.02$ \citep{GelmanRubin1992} (production run) or $R{-}1 < 0.05$ (validation).""",
    r"""All three runs (\SSEE, \LCDM\ and the validation chain) are stopped by the Cobaya Gelman--Rubin criterion $R{-}1 < 0.02$ \citep{GelmanRubin1992}.""")
rep(r"""same side, so the result does not hinge on the estimator), decisively below the Jeffreys threshold ($\Delta\mathrm{BIC}<-10$) and driven""",
    r"""same side, so the result does not hinge on the estimator), very strong evidence on the scale of \citet{KassRaftery1995} ($|\Delta\mathrm{BIC}|>10$) and driven""")

# --- el H0 estrecho: lo fija omega_m, no Omega_m ---
rep(r"""  the $H_0$--$\Omega_m$ degeneracy by algebraically fixing
  $\Omega_{m,\mathrm{CMB}}=0.3089$.}""",
    r"""  the $H_0$--$\Omega_m$ degeneracy by algebraically fixing $\omega_b$ and
  $\omega_c$.}""")
rep(r"""  reflects the geometric constraint imposed by $\Omega_{m,\mathrm{CMB}} = 0.3089$ (algebraically fixed),
  which eliminates""",
    r"""  reflects the geometric constraint imposed by the algebraically fixed $\omega_b$ and $\omega_c$,
  which eliminates""")

# --- tabla resumen: minimo chi2, no MCMC ---
rep(r"""the full off-diagonal \texttt{plik} MCMC (evaluated at the global anchor
$H_0=\val{H0_GLOBAL_d5}$, $\omega_m$-direct) is the canonical result.}""",
    r"""the full off-diagonal \texttt{plik} minimum $\chi^2$ of each model (\SSEE\ at the
global anchor $H_0=\val{H0_GLOBAL_d5}$, $\omega_m$-direct) is the canonical result.}""")
rep(r"""\texttt{plik\_lite} point est. & TTTEEE+lowl     & 669  & 2 & 6 & $\val{lite_dBIC}$ (SSEE decisively favoured) \\
Full \texttt{plik} MCMC   & TTTEEE+lowl+lensing""",
    r"""\texttt{plik\_lite} ($A_s,\tau$ min.) & TTTEEE+lowl     & 669  & 2 & 6 & $\val{lite_dBIC}$ (SSEE favoured) \\
Full \texttt{plik} ($\chi^2$ min.) & TTTEEE+lowl+lensing""")
rep(r"""The full \texttt{plik} MCMC (Cobaya + \texttt{clipy}, official off-diagonal covariance) is the canonical result.""",
    r"""The full \texttt{plik} minimum (Cobaya + \texttt{clipy}, official off-diagonal covariance) is the canonical result.""")
rep(r"""  \item \textbf{Full off-diagonal \texttt{plik} MCMC (canonical):}""",
    r"""  \item \textbf{Full off-diagonal \texttt{plik}, minimum $\chi^2$ (canonical):}""")

# --- hi_class: numeros de P7 por \val ---
rep(r"""sound speed is $c_s^2=(M_v-T_r)/(5M_v+3T_r)=0.021284$. An independent
\textsc{hi\_class} integration reproduces $c_s^2$ to $0.000\%$ and
$\alpha_K(0)$ to $0.011\%$ (Paper~7). The kineticity is not observationally
accessible: a factor $100$ change moves $\sigma_8$ by $0.007\%$.""",
    r"""sound speed is $c_s^2=(M_v-T_r)/(5M_v+3T_r)=\val{cs2_condensado_d6}$. An independent
\textsc{hi\_class} integration reproduces $c_s^2$ to $\val{p7_hc_cs2_pct}\%$ and
$\alpha_K(0)$ to $\val{p7_hc_alphaK_pct}\%$ (Paper~7). The kineticity is not observationally
accessible: a factor $100$ change moves $\sigma_8$ by $\val{p7_hc_s8_xk_pct}\%$.""")

# --- falsadores: theta* en vez de picos con bandas sin base; 3 sigma como P1/P2 ---
rep(r"""  \item \textbf{Peak positions:} $\ell_1=\val{p3_pico1_ssee}\pm3$, $\ell_2=\val{p3_pico2_ssee}\pm5$, $\ell_3=\val{p3_pico3_ssee}\pm8$.
    A measurement placing $\ell_1$ outside this range by more than $2\sigma$
    would falsify the $\omega_m$-direct CMB matter density.""",
    r"""  \item \textbf{Acoustic scale:} at $H_0^{\rm glob}$ the algebraic densities give
    $100\theta_*=\val{p3_th100_anc}$ ($\val{p3_th_sig_anc}\sigma$ from Planck~2018). A CMB
    measurement placing $\theta_*$ more than $3\sigma$ from this value would falsify the
    $\omega_m$-direct CMB matter density.""")
rep(r"""    equation of state: a joint fit requiring $w_0$ more than $2\sigma$""",
    r"""    equation of state: a joint fit requiring $w_0$ more than $3\sigma$""")

# --- conclusiones ---
rep(r"""reproduces the Planck 2018 CMB TT power spectrum without introducing fitted
dimensionless parameters.""",
    r"""reproduces the Planck 2018 CMB power spectra with only the two primordial
parameters $\{A_s,\tau\}$ fitted.""")
rep(r"""decisively favouring SSEE over $\Lambda$CDM at equal fit quality ($\Delta\chi^2=-0.010$).""",
    r"""favouring SSEE over $\Lambda$CDM at equal fit quality ($\Delta\chi^2=\val{lite_dchi2}$).""")
rep(r"""  \item The sound horizon $r_d=\val{p2_lyaB_rd}$ Mpc matches $\Lambda$CDM to $0.05\%$.""",
    r"""  \item The sound horizon $r_d=\val{p2_lyaB_rd}$ Mpc matches $\Lambda$CDM (ratio $\val{p2_rd_ratio}$).""")
rep(r"""evaluation establishes that the SSEE algebraic geometry is not only viable
but statistically preferred by the CMB data when fully penalized for free parameters.""",
    r"""evaluation establishes that the SSEE algebraic geometry is viable and, fitting as
well as \LCDM\ with fewer parameters, preferred on the BIC.""")
rep(r"""a residual of $+4.2\times10^{-6}$ from the pure-number target""",
    r"""a residual of $\val{p9_hglob_residuo}$~km\,s$^{-1}$\,Mpc$^{-1}$ from the pure-number target""")

open(P, "w").write(s)

# --- bibliografia ---
B = "manuscript/ssee_paper3.bib"
b = open(B).read()
if "KassRaftery1995" not in b:
    b += """
@article{KassRaftery1995,
  author  = {Kass, R. E. and Raftery, A. E.},
  title   = {Bayes Factors},
  journal = {J. Am. Statist. Assoc.},
  year    = {1995},
  volume  = {90},
  pages   = {773},
  doi     = {10.1080/01621459.1995.10476572}
}
"""
    open(B, "w").write(b)
print("P3: reemplazos aplicados")
