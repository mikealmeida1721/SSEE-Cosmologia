#!/usr/bin/env python3
"""Quinta lectura P5 (2026-10-11): reemplazos exactos; aborta si un conteo no casa.

Fondo: el «0» de Israel–Stewart es un límite de alta frecuencia, no estabilidad
(el modo creciente es inestable con c2_bare = w0); la estabilidad la da el campo
de Paper 7. Q2 se rehace con el sistema IS completo. Logs:
p5_estabilidad_IS_completa.json, p5_IS_perturbations_Q2.json, p5_cruce_fantasma_IS.json.
"""
import sys

P = "manuscript/SSEE_Paper5_IS.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


def blk(ini, fin, new):
    """Reemplaza desde `ini` (incluido) hasta `fin` (excluido); ambos únicos."""
    global s
    for m in (ini, fin):
        if s.count(m) != 1:
            sys.exit(f"ancla no única ({s.count(m)}): {m[:90]!r}")
    i, j = s.index(ini), s.index(fin)
    if j <= i:
        sys.exit(f"orden: {ini[:60]!r}")
    s = s[:i] + new + s[j:]


# --- preámbulo ---
rep(r"""\newcommand{\OmDE}{\Omega_{\mathrm{DE}}}""",
    r"""\newcommand{\OmDE}{\Omega_{\mathrm{DE}}}
\newcommand{\sDE}{s_{\mathrm{DE}}}""")

# --- resumen ---
rep(r"""equation of state $w_0 = -T_r/M_v \simeq -0.8399$ and $w_a \simeq -0.6700$""",
    r"""equation of state $w_0 = -T_r/M_v = \val{W0_d6}$ and $w_a = \val{WA_d6}$""")
rep(r"""in agreement with the official DESI DR2 $w_0w_a$CDM posterior at $0.24\sigma$ (Pantheon+; $0.2$--$1.8\sigma$ across SN compilations).""",
    r"""in agreement with the official DESI DR2 $w_0w_a$CDM posterior at $\val{p2_w0wa_ssee_ec26}\sigma$ (Pantheon+; $\val{p2_w0wa_ssee_ec28_d1}$--$\val{p2_w0wa_ssee_ec27_d1}\sigma$ across SN compilations).""")
blk(r"""For Q1, we prove analytically that the SSEE structure constants satisfy the""",
    r"""For Q3, we compute the IS growth index""",
    r"""For Q1, the SSEE structure constants satisfy the algebraic identity
$\ztilde/(\tauPi H_0) = \sDE = |w_0|$ (the saturation $s_{\rm DE}=T_r/M_v$ of Paper~1),
so that the high-frequency ($\omega\tauPi\to\infty$) sound speed of the IS fluid
vanishes, $c^2_{s,\mathrm{eff}} = w_0 + \sDE = 0$. We show that this is \emph{not}
a stability result. For a mode growing at rate $\lambda$ the viscous stiffness is
$\sDE\,\lambda\tauPi/(1+\lambda\tauPi) < \sDE$, so with $c^2_{s,\rm bare}=w_0$ the
growing branch obeys $\lambda^2 = k^2\sDE/(1+\lambda\tauPi) > 0$ at every $k$
($\lambda = \val{p5_lamIS_k100}\,H_0$ at $k=100\,H_0/c$); the full five-variable
integration confirms it. The stability of the \SSEE\ dark-energy sector is carried
instead by the field of Paper~7, whose own sound speed is
$c^2_s=+\val{cs2_condensado_d6}$: with it, and the same viscosity, no mode grows.
The quasi-static reduction used for this question in earlier versions is the
Navier--Stokes limit, valid only for $\tauPi H\ll1$, which never holds here.

For Q2, integrating the full linear IS system (with the field's sound speed) from
$z=19$ to $z=0$ gives $\delta_{\mathrm{DE}}/\delta_m = \val{q2_r_k3}$ at
$k=10\,H_0/c$, falling as $k^{-2}$: the enhancement
$\Omega_{m,\mathrm{eff}}/\Omega_m = \val{R_media_k10_p5}\pm \val{R_sd_k10_p5}$ ($k\geq10\,H_0/c$)
is a bound on dark-energy clustering, not a factor $\approx2$ --- and there is no
second matter sector for it to supply. The number $\Omega_{m,\mathrm{dyn}}=\val{S_M_d6}$
once paired with $\Omega_{m,\mathrm{CMB}}$ is not a density but $1+w_0$, a quantity of the
equation of state, so the difference $\val{OMEGA_M_TOTAL_d6}-\val{S_M_d6}$ that once defined a
second sector subtracts objects of different kinds; that construction is retracted
(Paper~6). The matter content is a single sector, $\Omega_m = \omega_m/h^2 =
\val{OMEGA_M_TOTAL_d6}$, and the algebraic number $\mathrm{MIRA}=(3\varphi+\pi)/4=\val{MIRA_d6}$
survives only as the Hubble-screening amplitude of Paper~9. The same integration,
written in the regular variable of Kunz \& Sapone, carries the perturbations through
the phantom crossing at $z_*=\val{z_cruce}$ without divergence.

""")
rep(r"""asks for lies $0.49\sigma$ from the one the model's own CMB fit supplies, so""",
    r"""asks for lies $\val{logA_leg_vs_cmb}\sigma$ from the one the model's own CMB fit supplies, so""")
rep(r"""The $f\sigma_8$ mean tension is $0.70\sigma$, essentially identical to $\Lambda$CDM
($0.73\sigma$): SSEE does not suppress""",
    r"""The $f\sigma_8$ mean tension is $\val{fs8_tmedia_ssee}\sigma$, essentially identical to $\Lambda$CDM
($\val{fs8_tmedia_lcdm}\sigma$): SSEE does not suppress""")
blk(r"""Finally, we map the SSEE IS parameters to the EFT-of-dark-energy operator basis""",
    r"""\end{abstract}""",
    r"""Finally, we place the IS layer in the EFT-of-dark-energy language
\citep{Gubitosi2013,Bellini2015}: the dark-energy action of Paper~7 is a
shift-symmetric ghost condensate with $\alpha_T=\alpha_B=\alpha_M=0$, which
produces no bulk viscosity, so the IS layer is a property of the fluid
parametrisation and maps to no operator of the action. An earlier mapping to
$\bar M_2^2$ (which would imply $\alpha_T\neq0$) and an earlier contrast with the
ghost condensate (``$c^2_s=1$'') are withdrawn: the ghost condensate \emph{is} the
\SSEE\ dark-energy sector.
""")

# --- introducción ---
rep(r"""  \simeq -0.8399, \qquad
  w_a = -\frac{P_{sc}}{I_g} \simeq \val{WA_d5},""",
    r"""  = \val{W0_d6}, \qquad
  w_a = -\frac{P_{sc}}{I_g} = \val{WA_d6},""")
rep(r"""Here $\beta=(\pi+\varphi)/2$, $K_v=\varphi+\pi+(\pi+\varphi)$,""",
    r"""Here $\beta=(\pi+\varphi)/2$, $K_v=\varphi+\pi+(\pi+\varphi)$, $I_g = K_v$ (the
structural constraint of Paper~1),""")
rep(r"""The CPL parameters~\eqref{eq:w0_wa} \citep{ChevallierPolarski2001,Linder2003} are consistent with DESI DR2 at $0.24\sigma$ (Pantheon+)
\citep{SSEE_Paper2,AbdulKarim2025} and with Planck 2018 CMB spectra at
$\chi^2_r \leq 1.062$ \citep{SSEE_Paper3}.""",
    r"""The CPL parameters~\eqref{eq:w0_wa} \citep{ChevallierPolarski2001,Linder2003} are consistent with DESI DR2 at $\val{p2_w0wa_ssee_ec26}\sigma$ (Pantheon+)
\citep{SSEE_Paper2,AbdulKarim2025} and with the Planck 2018 CMB spectra \citep{SSEE_Paper3}.""")
rep(r"""  \mathrm{MIRA} &\equiv \frac{3\varphi+\pi}{4} \simeq \val{MIRA_d4}
  \quad\text{(MIRA factor)},""",
    r"""  \mathrm{MIRA} &\equiv \frac{3\varphi+\pi}{4} \simeq \val{MIRA_d4}
  \quad\text{(screening amplitude, Paper~9)},""")
rep(r"""A canonical-kinetic (constant-$w$) $k$-essence proxy with Lagrangian $\mathcal{L} \propto X^n$""",
    r"""A single-power (constant-$w$) $k$-essence proxy with Lagrangian $\mathcal{L} \propto X^n$""")
rep(r"""For SSEE, $w_0 \simeq -0.840$, giving
\begin{equation}
  c^2_{s,\mathrm{bare}} = w_0 \simeq -0.840.""",
    r"""For SSEE this gives
\begin{equation}
  c^2_{s,\mathrm{bare}} = w_0 = \val{W0_d6}.""")
rep(r"""  = 0.021284 ,
  \qquad u \equiv c_2X/c_1 ,""",
    r"""  = \val{cs2_condensado_d6} ,
  \qquad u \equiv c_2X/c_1 ,""")
rep(r"""carry different coefficient ratios ($+0.008577$ against $\val{u_condensado_d6}$) and do""",
    r"""carry different coefficient ratios ($+\val{c2X_c1_KX_d6}$ against $\val{u_condensado_d6}$) and do""")
rep(r"""The IS bulk viscosity is $\ztilde = \KALz/3$, so the fluid-level regularisation
introduces no new parameter.""",
    r"""The IS bulk viscosity is $\ztilde = \KALz/3$, so the fluid-level layer
introduces no new parameter. We show in Section~\ref{sec:Q1_stability} that this
layer does \emph{not}, by itself, remove the instability of the closure
$c^2_s=w$; what removes it is the field's own sound speed above.""")
rep(r"""enters the observable: $\ztilde/(\tauPi H_0) = \OmDE$, and since $\ztilde$ and""",
    r"""enters the observable: $\ztilde/(\tauPi H_0) = \sDE$, and since $\ztilde$ and""")
rep(r"""$c^2_{s,\rm eff} = \wz + \OmDE = 0$ is therefore \emph{independent of}""",
    r"""$c^2_{s,\rm eff} = \wz + \sDE = 0$ is therefore \emph{independent of}""")
rep(r"""follows from the algebraic identity $\OmDE = |\wz|$ alone. The individual split""",
    r"""follows from the algebraic identity $\sDE = |\wz|$ alone. The individual split""")
rep(r"""and $\tauPi H_0 = \KALz/(3\OmDE)$, so that $\KALz \to 1.1\,\KALz$ gives
$\Sigma m_\nu = 0.0566$~eV,""",
    r"""and $\tauPi H_0 = \KALz/(3\sDE)$, so that $\KALz \to 1.1\,\KALz$ gives
$\Sigma m_\nu = \val{smnu_kal11}$~eV,""")
rep(r"""prediction is the field value $c^2_s = 0.021284$. The recurrence of $\KALz$ in""",
    r"""prediction is the field value $c^2_s = \val{cs2_condensado_d6}$. The recurrence of $\KALz$ in""")
rep(r"""The central claim of the present paper is that \emph{these algebraically determined
IS parameters exactly neutralise the gradient instability}.""",
    r"""Earlier versions of this paper claimed that \emph{these algebraically determined
IS parameters exactly neutralise the gradient instability}. They neutralise it only
for oscillations in the limit $\omega\tauPi\to\infty$; the growing branch survives
(Section~\ref{sec:Q1_stability}). The claim is withdrawn, and the stability of
the sector is assigned to the field.""")

# --- teoría: causalidad, normalización ---
rep(r"""  \item \textbf{Causality}: the IS relaxation limits signal propagation to
    $v_{\rm sig} = \sqrt{\zeta/[\tauPi(\rho_{\mathrm{DE}}+p_{\mathrm{DE}})]} < c$
    \citep{HiscockLindblom1983} --- the enthalpy again, as the inertia of the
    propagating mode.""",
    r"""  \item \textbf{Causality}: the IS relaxation gives a finite characteristic speed,
    $v^2_{\rm sig} = c^2_{s,\rm bare} + \zeta/[\tauPi(\rho_{\mathrm{DE}}+p_{\mathrm{DE}})] \leq c^2$
    \citep{HiscockLindblom1983} --- the enthalpy again, as the inertia of the
    propagating mode.""")
rep(r"""  \ztilde &\equiv \frac{\zeta}{(\rho_{\mathrm{DE}}+p_{\mathrm{DE}})\,H_0}
           = \frac{\zeta}{\rho_{\mathrm{DE}}(1+\wz)\,H_0}, \\""",
    r"""  \ztilde &\equiv \frac{\zeta\,H_0}{\rho_{\mathrm{DE}}+p_{\mathrm{DE}}}
           = \frac{\zeta\,H_0}{\rho_{\mathrm{DE}}(1+\wz)}, \\""")
rep(r"""$c^2_{s,\mathrm{eff}} = \wz + 5.248 = +4.41$: superluminal, and therefore not""",
    r"""$c^2_{s,\mathrm{eff}} = \wz + \val{inv_1pw0_m1_d3} = \val{cs2_rho_norm}$: superluminal, and therefore not""")
blk(r"""\emph{The answer, from two independent witnesses inside this paper.}""",
    r"""\emph{The resolution, and why it is not merely a choice.}""",
    r"""\emph{The answer from inside this paper.}
The relativistic inertia of a sound wave is the enthalpy, so the dispersion
relation of Appendix~\ref{app:dispersion} carries
$\zeta/[\tauPi(\bar\rho+\bar p)]$; it reduces to $\ztilde/(\tauPi H_0)$
\emph{only if} $\ztilde$ is enthalpy-normalised, $\zeta =
\ztilde\,(\rho_{\rm DE}+p_{\rm DE})/H_0$, which is what that appendix states.
(Earlier versions cited a second witness, a friction coefficient $\approx186$ in
the eigenvalue appendix; that number had no recorded computation and is withdrawn.)

""")
rep(r"""this paper already use, and it is the form consistent with relativistic""",
    r"""this paper uses, and it is the form consistent with relativistic""")
rep(r"""\emph{Consequence.} $c^2_{s,\mathrm{eff}} = \wz + \ztilde/(\tauPi H_0)
= \wz + \OmDE = 0$ stands: marginally stable, manifestly subluminal, and
\textbf{not} an artefact. The $0$ is a result.""",
    r"""\emph{Consequence.} $c^2_{s,\mathrm{eff}} = \wz + \ztilde/(\tauPi H_0)
= \wz + \sDE = 0$ stands as the \emph{high-frequency} sound speed of the IS fluid:
subluminal, and not an artefact of normalisation. It is not a stability
statement --- the growing branch is treated in Section~\ref{sec:Q1_stability}.""")
rep(r"""$\tauPi H_0 = \KALz/(3\OmDE)$ by saturating the causality bound written as""",
    r"""$\tauPi H_0 = \KALz/(3\sDE)$ by saturating the causality bound written as""")
rep(r"""belongs; imposed correctly it returns $\tauPi H_0 = \ztilde(1+\wz) = 0.2946$,
not $2.191$. The factor between them is exactly $(1+\wz)^{-1}=6.248$. Nothing""",
    r"""belongs; imposed correctly it returns $\tauPi H_0 = \ztilde(1+\wz) = \val{tau_saturado}$,
not $\val{TAU_PI_H0_d3}$. The factor between them is exactly $(1+\wz)^{-1}=\val{inv_1pw0_d3}$. Nothing""")
rep(r"""viscous fluid (this paper) & IS, $\wz+\OmDE$ & $0$ \\
field, adiabatic & Paper~7 ghost condensate & $0.021284$ \\""",
    r"""viscous fluid, $\omega\tauPi\to\infty$ (this paper) & IS, $\wz+\sDE$ & $0$ \\
field, adiabatic & Paper~7 ghost condensate & $\val{cs2_condensado_d6}$ \\""")
rep(r"""rescues to $0$; the field needs no such rescue, returning $+0.021284$""",
    r"""``rescues'' to $0$ only at high frequency; the field needs no such rescue, returning $+\val{cs2_condensado_d6}$""")
rep(r"""exactly on $0$ rather than on $0.021284$ is not established. The gap is the""",
    r"""exactly on $0$ rather than on $\val{cs2_condensado_d6}$ is not established
(and, since the $0$ is only a high-frequency limit, the physical value is the
field's). The gap is the""")
rep(r"""  \boxed{\ztilde = \frac{\KALz\,\Omega}{M_v} = \frac{\KALz}{3} \simeq 1.8405,
  \qquad
  \tauPi H_0 = \frac{\KALz\,\Omega}{T_r} \simeq 2.191.}""",
    r"""  \boxed{\ztilde = \frac{\KALz\,\Omega}{M_v} = \frac{\KALz}{3} = \val{zeta_tilde_d4},
  \qquad
  \tauPi H_0 = \frac{\KALz\,\Omega}{T_r} = \val{TAU_PI_H0_d4}.}""")
rep(r"""  \frac{\ztilde}{\tauPi H_0} = \frac{\KALz/3}{\KALz/(3\OmDE)} = \OmDE = |\wz|""",
    r"""  \frac{\ztilde}{\tauPi H_0} = \frac{\KALz/3}{\KALz/(3\sDE)} = \sDE = |\wz|""")
blk(r"""  \item $\tauPi > 0$: satisfied, $\tauPi H_0 = 2.191 > 0$.""",
    r"""\subsection{Linearised perturbation equations in Newtonian gauge}""",
    r"""  \item $\tauPi > 0$: satisfied, $\tauPi H_0 = \val{TAU_PI_H0_d3} > 0$.
  \item $\zeta \geq 0$: satisfied, $\ztilde = \val{zeta_tilde_d4} > 0$, with the
    enthalpy of the field, $\rho_{\rm DE}(1+\wz)>0$, at all times.
  \item The characteristic speed of the viscous mode,
    $v^2_{\rm sig} = c^2_{s,\rm bare} + \zeta/[\tauPi(\rho_{\mathrm{DE}}+p_{\mathrm{DE}})]
    = \wz + \sDE = 0 \leq 1$: causal.
\end{enumerate}
Earlier versions of this subsection divided by $\rho_{\rm DE}$ instead of the
enthalpy, obtained $v_{\rm sig}=c$, and described the configuration as
``maximally causal''. With the enthalpy normalisation adopted above the viscous
contribution alone is $\sDE=\val{S_DE_d6}$ and the total characteristic speed is
$0$: subluminal, not saturating.

""")

# --- ecuaciones de perturbaciones ---
blk(r"""limit $k \gg aH$ are \citep{Hu1998,Maartens1996}:""",
    r"""\subsection{Quasi-static IS approximation and stiffness reduction}""",
    r"""limit $k \gg aH$ are \citep{Hu1998,Maartens1996}:
\begin{align}
  \delta'_m &= -\frac{k}{aH}\,v_m + 3\Phi',
  \label{eq:deltam} \\
  v'_m      &= -v_m + \frac{k}{aH}\,\Phi,
  \label{eq:vm} \\
  \delta'_{\mathrm{DE}} &= -(1+\wz)\!\left[\frac{k}{aH}\,v_{\mathrm{DE}} - 3\Phi'\right],
  \label{eq:deltaDE} \\
  v'_{\mathrm{DE}} &= -(1-3c^2_s)\,v_{\mathrm{DE}}
    + \frac{k}{aH}\!\left[\frac{c^2_s\,\delta_{\mathrm{DE}}}{1+\wz}
    + \Pitilde + \Phi\right],
  \label{eq:vDE} \\
  \tauPi H\,\Pitilde' &= -\Pitilde - \ztilde\,\frac{k}{aH}\,\frac{H}{H_0}\,v_{\mathrm{DE}},
  \label{eq:Pi}
\end{align}
where $\Pitilde = \delta\Pi/[\rho_{\mathrm{DE}}(1+\wz)]$ is the bulk viscous pressure
perturbation normalised to the enthalpy of the field, and the Newtonian potential satisfies
\begin{equation}
  k^2\,\Phi = -\frac{3}{2}\,\frac{H_0^2}{c^2}\left[\frac{\Omega_m\,\delta_m}{a}
    + a^2\,\OmDE\,f_{\mathrm{DE}}(a)\,\delta_{\mathrm{DE}}\right],
  \label{eq:Poisson}
\end{equation}
with comoving $k$ and $f_{\mathrm{DE}}(a) = \rho_{\mathrm{DE}}(a)/\rho_{\mathrm{DE},0}$.
The inertia of the dark-energy perturbation is the enthalpy of the \emph{field},
$\rho_{\rm DE}(1+\wz)>0$: in the closure of Paper~1 the field carries $w_0$ and the
background viscous pressure carries the rest of $w(a)$, including the phantom
crossing at $z_*=\val{z_cruce}$ (Section~\ref{subsec:crossing} treats the total
inertia, which changes sign there). Earlier versions used $1+w(a)$ clipped at
$10^{-6}$ in the phantom era, wrote the gravitational terms of
Eqs.~\eqref{eq:vm}--\eqref{eq:vDE} with the opposite sign --- which made gravity
repulsive in the integration --- and divided the dark-energy one by $1+w$; all three are corrected.
The $3\Phi'$ terms arise from the metric perturbation and are dropped in the
sub-horizon integration, consistent with standard practice \citep{Hu1998}.

""")
blk(r"""\subsection{Quasi-static IS approximation and stiffness reduction}""",
    r"""%======================================================================
\section{Q1: Gradient Stability""",
    r"""\subsection{The quasi-static reduction is the Navier--Stokes limit}
\label{subsec:QS}

Earlier versions set $\Pitilde' = 0$ in Eq.~\eqref{eq:Pi}, obtaining
\begin{equation}
  \Pitilde_{\mathrm{QS}} = -\ztilde\,\frac{k}{aH}\,\frac{H}{H_0}\,v_{\mathrm{DE}},
  \label{eq:PiQS}
\end{equation}
which turns the viscosity into a velocity friction
$\mathcal{F}(k,a) = (1-3c^2_s) + \ztilde(k/aH)^2(H/H_0)$, and justified it by
$\tauPi H \gg 1$. The condition is the reverse. Dropping $\tauPi H\,\Pitilde'$
requires the viscous pressure to relax faster than the perturbation evolves,
$\tauPi H \ll 1$; here $\tauPi H \geq \tauPi H_0 = \val{TAU_PI_H0_d3}$ at all times and grows
into the past. Equation~\eqref{eq:PiQS} is first-order (Navier--Stokes) viscosity,
the acausal limit that Israel--Stewart was built to replace, and in that limit the
viscosity only damps: it bounds the growth rate of the $c^2_s=w_0$ branch at
$1/(\tauPi H_0)=\val{p5_lamNS}$ per Hubble time, which is why the earlier integration
showed nothing alarming. All results below integrate the full five-variable system
(\texttt{LSODA}, relative tolerance $10^{-9}$).

""")

# --- Q1 ---
rep(r"""\section{Q1: Gradient Stability — Exact Marginal Stability Theorem}""",
    r"""\section{Q1: Gradient Stability --- What the IS Identity Does and Does Not Do}""")
blk(r"""For a relativistic viscous fluid with IS relaxation, the full dispersion relation""",
    r"""The full $k$-dependent interpolation between the Navier-Stokes ($k\to 0$) and""",
    r"""For a relativistic viscous fluid with IS relaxation, a perturbation
$\propto e^{i(kx-\omega t)}$ obeys (Appendix~\ref{app:dispersion})
\begin{equation}
  \omega^2 = \left[c^2_{s,\mathrm{bare}}
    + \frac{\zeta}{\tauPi(\rho_{\mathrm{DE}}+p_{\mathrm{DE}})}\,
      \frac{-i\omega\tauPi}{1-i\omega\tauPi}\right]k^2 .
  \label{eq:disprel_full}
\end{equation}
In the limit $|\omega|\tauPi \gg 1$ the viscous term becomes a pure stiffness and
\begin{equation}
  \omega^2 = \left(c^2_{s,\mathrm{bare}} + \frac{\ztilde}{\tauPi H_0}\right)k^2
  \equiv c^2_{s,\mathrm{eff}}\,k^2.
  \label{eq:cs2_eff_def}
\end{equation}
""")
rep(r"""\begin{tcolorbox}[colback=blue!5!white,colframe=blue!60!black,title={\textbf{SSEE Marginal Stability (given minimality)}}]""",
    r"""\begin{tcolorbox}[colback=blue!5!white,colframe=blue!60!black,title={\textbf{High-frequency marginality (not stability)}}]""")
rep(r"""  = \frac{\KALz/3}{\KALz/(3\,\OmDE)}
  = \OmDE = |\wz|,""",
    r"""  = \frac{\KALz/3}{\KALz/(3\,\sDE)}
  = \sDE = |\wz|,""")
rep(r"""\textit{and therefore}
\begin{equation}
  c^2_{s,\mathrm{eff}}(k\to\infty)""",
    r"""\textit{and therefore, for oscillations with $\omega\tauPi\to\infty$,}
\begin{equation}
  c^2_{s,\mathrm{eff}}""")
rep(r"""than a theorem constraining all IS models: SSEE supports an IS embedding for
which dark-energy perturbations are exactly marginally stable in the
high-$k$ limit.}""",
    r"""than a theorem constraining all IS models. It fixes the high-frequency sound
speed of the fluid; it does not make the fluid stable (Section~\ref{subsec:growing}).}""")
blk(r"""The proof follows directly from Eq.~\eqref{eq:ratio_identity}.""",
    r"""\subsection{Uniqueness of the minimal-viscosity solution}""",
    r"""The identity follows directly from Eq.~\eqref{eq:ratio_identity}.

\subsection{The growing branch: the closure $c^2_s=w_0$ stays unstable}
\label{subsec:growing}

Stability is decided by modes that grow, not by modes that oscillate. For
$e^{\lambda t}$ ($\omega=i\lambda$), Eq.~\eqref{eq:disprel_full} with
$c^2_{s,\rm bare}=\wz=-\sDE$ gives
\begin{equation}
  \lambda^2 = k^2\left[\sDE - \sDE\,\frac{\lambda\tauPi}{1+\lambda\tauPi}\right]
            = \frac{k^2\,\sDE}{1+\lambda\tauPi} > 0
  \qquad\text{for every } k .
  \label{eq:growing_branch}
\end{equation}
The viscous stiffness reaches $\sDE$ only as $\lambda\tauPi\to\infty$, so it never
fully cancels the negative bare stiffness: at large $k$,
$\lambda\simeq(k^2\sDE/\tauPi)^{1/3}$, which is $\val{p5_lamIS_k10}\,H_0$ at
$k=10\,H_0/c$ and $\val{p5_lamIS_k100}\,H_0$ at $k=100\,H_0/c$ --- far faster than the
expansion. The full cosmological integration agrees: with $c^2_{s,\rm bare}=\wz$ the
ratio $\delta_{\rm DE}/\delta_m$ at $z=0$ reaches $\val{p5_rw0_k20}$ at $k=20\,H_0/c$ and
$\val{p5_rw0_k100}$ at $k=100\,H_0/c$ (\texttt{src/p05\_IS/estabilidad\_IS\_completa.py};
its controls --- $\zeta=0$ returns $\lambda=k\sqrt{\sDE}$, and the field's sound speed
returns no growing mode --- both pass).

\textbf{What stabilises the sector is the field.} Paper~7's ghost condensate has
its own positive sound speed, $c^2_s=+\val{cs2_condensado_d6}$. With it in place of $\wz$,
Eq.~\eqref{eq:disprel_full} has no growing root, with or without viscosity, and the
full integration gives $|\delta_{\rm DE}/\delta_m|=\val{q2_r_k3}$ at $k=10\,H_0/c$, falling
as $k^{-2}$ (Section~\ref{sec:Q2_MIRA}). The closure $c^2_s=w$ is the
parametrisation a Boltzmann code imposes, not a property of the field
(Section~\ref{subsec:instability}); the IS layer does not repair it, and it does not
need to be repaired: the field never had the instability.

""")
rep(r"""In SSEE both sides equal $\OmDE = |\wz|$, and the $\KALz$ dependence cancels""",
    r"""In SSEE both sides equal $\sDE = |\wz|$, and the $\KALz$ dependence cancels""")
rep(r"""What remains an input is the \emph{requirement} of marginal stability itself,
and it is a selection principle rather than a fitted number. Its justification
is minimality: since $c^2_{s,\mathrm{bare}} = \wz < 0$ is a gradient
instability, some viscosity is mandatory, and $\ztilde = \KALz\Omega/M_v$ is
the \emph{smallest} value that removes it --- any less leaves the instability,
any more is unmotivated surplus. We therefore state the result as a consequence
of minimality, not as a prediction free of assumptions.""",
    r"""What remains an input is the \emph{requirement} that the high-frequency sound
speed vanish, a selection principle rather than a fitted number. Earlier versions
justified it as the smallest viscosity that removes the instability;
Section~\ref{subsec:growing} shows that no finite $\tauPi$ removes it on the growing
branch, so that justification is withdrawn and the principle is stated as what it
is: the choice that makes the fluid's high-frequency limit match marginality.""")
blk(r"""The IS stabilisation transition occurs at $x = 1$, defining the critical wavenumber""",
    r"""\begin{figure}[h!]
\centering
\includegraphics[width=\textwidth]{fig_paper5_IS_stability.pdf}""",
    r"""The transition between the Navier--Stokes and the IS regime of the oscillatory
branch occurs at $x = 1$, defining
\begin{equation}
  k_\mathrm{crit}(a) = \frac{aH}{c\,\tauPi H_0},
  \qquad
  \frac{k_\mathrm{crit}}{H_0/c}\bigg|_{z=0} = \frac{1}{\tauPi H_0} = \val{kcrit_p5}.
  \label{eq:kcrit_z0}
\end{equation}
Earlier versions read $k_\mathrm{crit}<H_0/c$ as ``all sub-horizon modes are
IS-stabilised''. That reading concerned the oscillatory branch only; the growing
branch of the closure $c^2_s=\wz$ is unstable on both sides of $k_\mathrm{crit}$
(Section~\ref{subsec:growing}).

""")
rep(r"""  (blue solid line), interpolating from the bare value $c^2_s = w_0 \simeq -0.840$""",
    r"""  of the oscillatory branch (blue solid line), interpolating from the bare value $c^2_s = w_0 = \val{W0_d6}$""")
rep(r"""  The red shaded region marks gradient instability ($c^2_{s,\mathrm{eff}} < 0$);
  the green region marks stability.
  The IS transition at $k_\mathrm{crit} \simeq 0.456\,H_0/c$ (grey dash-dot)
  lies \emph{outside} the sub-horizon regime ($k > H_0/c$), so all
  observationally accessible modes are stabilised.""",
    r"""  The IS transition is at $k_\mathrm{crit} = \val{kcrit_p5}\,H_0/c$ (grey dash-dot).
  This curve is the high-frequency sound speed; it does not decide stability, which
  is set by the growing branch (Section~\ref{subsec:growing}).""")
rep(r"""  for representative wavenumbers $k/(H_0/c) = 2, 3, 5, 10, 20, 50, 100$.
  IS bulk viscous friction damps DE perturbations as $k^2$;
  at $k = 20\,H_0/c$ the ratio $|\delta_{\mathrm{DE}}/\delta_m| < 10^{-3}$
  throughout cosmic history.}""",
    r"""  for representative wavenumbers $k/(H_0/c) = 2, 3, 5, 10, 20, 50, 100$, from the
  full IS integration with the field's sound speed $c^2_s=\val{cs2_condensado_d6}$;
  at $z=0$ the ratio is $\val{q2_r_k4}$ at $k = 20\,H_0/c$.}""")

# --- Q2 ---
blk(r"""\section{Q2: Do IS Perturbations Link the Two Matter Sectors?}""",
    r"""%======================================================================
\section{Q3: Growth Rate""",
    r"""\section{Q2: How Much Does Dark Energy Cluster?}
\label{sec:Q2_MIRA}
%======================================================================

\subsection{Numerical setup and initial conditions}
\label{subsec:setup}

We integrate Eqs.~\eqref{eq:deltam}--\eqref{eq:Poisson} with $\Pitilde$ dynamical
and the field's sound speed $c^2_s=\val{cs2_condensado_d6}$, from $a_{\rm ini}=0.05$ ($z=19$)
to $a=1$. At $z=19$ the dark energy density fraction is
$\OmDE f_{\mathrm{DE}}(a_{\rm ini})/(H/H_0)^2 = \val{frac_de_z19}$ and the matter
growing mode sets the initial conditions:
\begin{equation}
  \delta_m(a_{\rm ini}) = a_{\rm ini}, \quad
  v_m(a_{\rm ini}) = -\frac{a_{\rm ini}\,H(a_{\rm ini})}{k}\,\delta_m(a_{\rm ini}), \quad
  \delta_{\mathrm{DE}} = v_{\mathrm{DE}} = \Pitilde = 0,
  \label{eq:IC}
\end{equation}
the velocity being the one for which $\delta'_m=\delta_m$ (earlier versions set
$v_m=-a_{\rm ini}H/H_0$, too large by $k/aH$, which is why their $\delta_m(z=0)$
grew with $k$). The normalisation of $\delta_m$ cancels in all ratios
(\texttt{src/p05\_IS/ssee\_paper5\_IS\_perturbations.py}).

\subsection{The scale that a two-fold enhancement would need}
\label{subsec:MIRA_requirement}

The effective matter density seen through the Poisson equation is
\begin{equation}
  \Omega_{m,\mathrm{eff}} = \Omega_m + \Omega_{\mathrm{DE}}\,r,
  \quad r \equiv \frac{\delta_{\mathrm{DE}}}{\delta_m}\bigg|_{z=0},
  \qquad \Omega_m = \val{OMEGA_M_TOTAL_d6},\ \ \Omega_{\mathrm{DE}} = \val{OMDE_DENS_d6},
  \label{eq:Omeff}
\end{equation}
with the \emph{densities} in both slots (until 2026-09-26 it carried the saturations
$s_m$ and $\sDE$), and we write $\mathcal{R} \equiv \Omega_{m,\mathrm{eff}}/\Omega_m$.
Earlier versions posed $\mathcal{R}$ as a test of whether the perturbations
reproduce $\mathrm{MIRA}=\val{MIRA_d4}$, under a matter factor
$\Omega_{m,\mathrm{CMB}} = \mathrm{MIRA}\times\Omega_{m,\mathrm{dyn}}$ withdrawn on
2026-06-18 (OP-8). There is no factor of two to supply. The ratio a two-fold
enhancement would have needed,
\begin{equation}
  r^* = \frac{(\mathrm{MIRA}-1)\,\Omega_m}{\Omega_{\mathrm{DE}}}
  = \frac{\val{MIRA_m1_d6} \times \val{OMEGA_M_TOTAL_d6}}{\val{OMDE_DENS_d6}}
  = \val{r_star_q2},
  \label{eq:r_required}
\end{equation}
is kept only as the scale against which the measured $r$ is small.

\subsection{Numerical results}
\label{subsec:results_MIRA}

\begin{table}[h!]
\centering
\caption{Full linear IS integration from $z=19$ to $z=0$ with the field's sound
  speed. $\delta_m(z=0)$ for $\delta_m(z=19)=0.05$; $r = \delta_{\mathrm{DE}}/\delta_m$;
  $\Omega_{m,\mathrm{eff}}$ via Eq.~\eqref{eq:Omeff}. The mean is over $k\geq10\,H_0/c$.}
\label{tab:MIRA}
\begin{tabular}{ccccc}
\toprule
$k\,[H_0/c]$ & $\delta_m(z=0)$ & $r = \delta_{\mathrm{DE}}/\delta_m$
  & $\Omega_{m,\mathrm{eff}}$ & $\mathcal{R}$ \\
\midrule
2   & \val{q2_deltam_k0} & $\val{q2_r_k0}$ & \val{q2_Omeff_k0} & \val{q2_R_k0} \\
3   & \val{q2_deltam_k1} & $\val{q2_r_k1}$ & \val{q2_Omeff_k1} & \val{q2_R_k1} \\
5   & \val{q2_deltam_k2} & $\val{q2_r_k2}$ & \val{q2_Omeff_k2} & \val{q2_R_k2} \\
10  & \val{q2_deltam_k3} & $\val{q2_r_k3}$ & \val{q2_Omeff_k3} & \val{q2_R_k3} \\
20  & \val{q2_deltam_k4} & $\val{q2_r_k4}$ & \val{q2_Omeff_k4} & \val{q2_R_k4} \\
50  & \val{q2_deltam_k5} & $\val{q2_r_k5}$ & \val{q2_Omeff_k5} & \val{q2_R_k5} \\
100 & \val{q2_deltam_k6} & $\val{q2_r_k6}$ & \val{q2_Omeff_k6} & \val{q2_R_k6} \\
\midrule
\multicolumn{4}{l}{Mean ($k \geq 10\,H_0/c$):}
  & $\val{R_media_k10_p5} \pm \val{R_sd_k10_p5}$ \\
\multicolumn{4}{l}{Would require ($r = r^*$):} & $\val{MIRA_d4}$ \\
\bottomrule
\end{tabular}
\end{table}

The enhancement is $\mathcal{R} = \val{R_media_k10_p5} \pm \val{R_sd_k10_p5}$ at
$k \geq 10\,H_0/c$: no enhancement. Its content is a bound on dark-energy clustering:
$r = \val{q2_r_k3}$ at $k = 10\,H_0/c$, falling to $\val{q2_r_k6}$ at $k = 100\,H_0/c$,
small and positive at every scale. The matter growth is the same at every $k$, as it
must be for pressureless matter on sub-horizon scales. A measurement of
$\delta_{\rm DE}/\delta_m$ at the per-cent level at $k \gtrsim 10\,H_0/c$ and $z=0$ would
contradict the model.
Earlier versions reported $\mathcal{R}=0.9897\pm0.0167$ and a negative $r$ bounded by
$0.0175$; those came from the integration with repulsive gravity, the
growing-mode error in the initial velocity and the Navier--Stokes reduction, and are
withdrawn.

\subsection{Why the ratio falls as $k^{-2}$}
\label{subsec:damping}

With a positive sound speed the dark-energy perturbation below its sound horizon is
a damped acoustic oscillation driven by the potential: the eigenvalues of the
linearised system at $k=10\,H_0/c$, $z=0$ include the pair
$\val{p5_eig2}\pm\val{p5_eig_im}\,i$ (Appendix~\ref{app:eigenvalues}). Its forced
amplitude is $\delta_{\rm DE}\sim(1+\wz)\Phi/c^2_s$, and the Poisson
equation~\eqref{eq:Poisson} gives $\Phi\propto\delta_m/k^2$, so $r\propto k^{-2}$
--- the scaling in Table~\ref{tab:MIRA}.

\begin{figure}[h!]
\centering
\includegraphics[width=0.7\textwidth]{fig_paper5_DE_clustering.pdf}
\caption{$|\delta_{\rm DE}/\delta_m|$ at $z=0$ from the full Israel--Stewart
  integration. Blue: with the sound speed of the field of Paper~7,
  $c^2_s=\val{cs2_condensado_d6}$; the ratio falls as $k^{-2}$
  (Table~\ref{tab:MIRA}). Red: with the fluid closure $c^2_{s,\rm bare}=w_0$ and the
  same viscosity; the growing branch of Eq.~\eqref{eq:growing_branch} drives it to
  $\val{p5_rw0_k100}$ at $k=100\,H_0/c$. Earlier versions of this figure plotted
  $\mathcal{R}(k)$ against the withdrawn target $\mathrm{MIRA}$.}
\label{fig:MIRA_test}
\end{figure}

\subsection{Through the phantom crossing}
\label{subsec:crossing}

The CPL history crosses $w=-1$ at $z_*=\val{z_cruce}$ (Paper~1). The field cannot carry
the crossing (its $c^2_s<0$ for $w<-1$, Paper~1); in the closure used here the
background viscous pressure carries it, $1+w=(1+\wz)(1-c)$ with
$c=|\Pi|/[\rho_{\rm DE}(1+\wz)]$. Two questions follow, and both are measured
(\texttt{src/p05\_IS/cruce\_fantasma\_IS.py}).

\emph{Do the perturbations cross?} With the \emph{total} inertia $1+w(a)$, which
vanishes at $z_*$, the rest-frame variables are singular. Written in
$U=(1+w)\theta/k$ with the pressure perturbation kept finite outside the rest frame
\citep{KunzSapone2006}, and with the field's sound speed, they remain finite:
$|\delta_{\rm DE}/\delta_m| = |\val{p5_cruce_r_k2}|$ at $k=2\,H_0/c$ and
$|\val{p5_cruce_r_k10}|$ at $k=10\,H_0/c$ at $z=0$. The control with
$c^2_s=\wz$ reaches $\val{p5_cruce_ctrl_k100}$ at $k=100\,H_0/c$.

\emph{Is the crossing within Israel--Stewart?} The truncated (linear) theory is
a near-equilibrium expansion, $|\Pi|\ll|p|$. Here
$|\Pi|/|p| = |\wa|(1-a)/|\wz|$ is $\val{p5_Pip_zc}$ at the crossing,
$\val{p5_Pip_z1}$ at $z=1$ and $\val{p5_Pip_z233}$ at $z=2.33$: beyond the linear
theory for $z\gtrsim z_*$. That regime is the one of the nonlinear extension of
\citet{MaartensMendez1997}, in which phantom solutions driven by bulk viscosity
have been constructed \citep{CruzLepe2017,CruzCruzLepe2017}. The second law holds
throughout, since $\zeta=\ztilde\rho_{\rm DE}(1+\wz)/H_0>0$. Whether the nonlinear
theory with the algebraic $(\ztilde,\tauPi)$ returns $w_a=\val{WA_d6}$ is the open
part of the question (OP-24).

""")

# --- Q3 ---
rep(r"""  = \frac{3}{2}\,\frac{\Omega_m(a)}{1}\,D_1,""",
    r"""  = \frac{3}{2}\,\Omega_m(a)\,D_1,""")
rep(r"""We integrate Eq.~\eqref{eq:D1_ode} from $a=0.008131$ to $a=1$ using
the SSEE Hubble rate (Table~\ref{tab:background}).
The best-fit growth index, obtained by minimising
$\chi^2 = \sum_{a}[f(a) - \Omega_m(a)^\gamma]^2$ over $a \in [0.3, 1]$
(the observationally accessible range), is""",
    r"""We integrate Eq.~\eqref{eq:D1_ode} from $a=10^{-3}$ to $a=1$ (\texttt{DOP853})
with the SSEE Hubble rate. The growth index, from a least-squares fit of
$\ln f = \gamma\ln\Omega_m(a)$ over $0\leq z\leq2$, is""")
rep(r"""The SSEE and $\Lambda$CDM growth rates are essentially identical at all redshifts,
with differences of $\lesssim 2\%$ (and $\lesssim 1.6\%$ at $z=0.5$).""",
    r"""The SSEE and $\Lambda$CDM growth rates differ at the per-cent level
(Table~\ref{tab:growth}).""")
rep(r"""at $z=99$ (matter-dominated epoch, $D_1 \propto a$).
We find
\begin{equation}
  \mathcal{G} = \val{p5_G} \pm 0.005.""",
    r"""at $a=10^{-3}$ (matter-dominated epoch, $D_1 \propto a$).
We find
\begin{equation}
  \mathcal{G} = \val{p5_G}.""")
rep(r"""The tiny enhancement reflects the slightly different DE equation-of-state
history $w(z)$ with $w_0=\val{W0_d6}$, $w_a=\val{WA_d6}$: the energy density transferred
from DE to matter-like perturbations at intermediate redshifts slightly boosts
$D_1$ relative to a $\Lambda$CDM universe with the same $\Omega_{m,\mathrm{cosm}}$.
The $\omega_m$-direct background $\Omega_{m,\mathrm{cosm}}=\val{OMEGA_M_TOTAL_d6}$ is slightly
\emph{below} $\Omega_{m,\Lambda\mathrm{CDM}}=0.3153$, so the net enhancement
($0.3\%$) is smaller than under the superseded $\Omega_{m}=0.3199$ background
($1.1\%$), and lies below near-term weak-lensing growth sensitivity.""",
    r"""Two background effects compete: $\Omega_{m,\mathrm{cosm}}=\val{OMEGA_M_TOTAL_d6}$ is slightly
\emph{below} $\Omega_{m,\Lambda\mathrm{CDM}}=0.3153$, which slows growth, while the CPL
history ($w_0=\val{W0_d6}$, $w_a=\val{WA_d6}$) has $w<-1$ for $z>z_*$, i.e.\ less dark
energy than a cosmological constant in the past, which prolongs matter domination.
The net is a small enhancement, below near-term weak-lensing growth sensitivity.""")
rep(r"""  \sigma_8^{\mathrm{SSEE}} = 0.811 \times \val{p5_G} = \val{p3_sigma8_IS} \pm 0.006.""",
    r"""  \sigma_8^{\mathrm{SSEE}} = 0.811 \times \val{p5_G} = \val{p3_sigma8_IS} \pm \val{p5_sigma8_IS_sigma},""")
rep(r"""\label{eq:sigma8_SSEE}
\end{equation}
This IS linear-growth amplitude""",
    r"""\label{eq:sigma8_SSEE}
\end{equation}
the error being Planck's on $\sigma_8$, propagated. This IS linear-growth amplitude""")
rep(r"""= \val{p3_S8_IS}$ ($2.7\sigma$ KiDS-1000), milder than the conservative CLASS amplitude""",
    r"""= \val{p3_S8_IS}$ ($\val{p5_tS8_ssee_kids}\sigma$ from KiDS-1000), close to the conservative CLASS amplitude""")
rep(r"""The Planck–lensing tension is $2.4\sigma$ with KiDS and $2.7\sigma$ with DES,
representing one of the most persistent $\Lambda$CDM discrepancies \citep{Weinberg2013}.""",
    r"""Planck's $\Lambda$CDM ($\sigma_8=0.811$, $\Omega_m=0.3153$, $S_8=\val{p5_S8_lcdm}$) lies
$\val{p5_tS8_lcdm_kids}\sigma$ from KiDS-1000 and $\val{p5_tS8_lcdm_des}\sigma$ from DES-Y3 with the
same error treatment as below, one of the most persistent $\Lambda$CDM
discrepancies \citep{Weinberg2013}.""")
rep(r"""    = \val{p3_sigma8_techo} \times \sqrt{\frac{\val{OMEGA_M_TOTAL_d6}}{0.3}}
    = \val{p3_sigma8_techo} \times 1.0147
    = \val{p3_S8_techo} \pm 0.006.}""",
    r"""    = \val{p3_sigma8_techo} \times \sqrt{\frac{\val{OMEGA_M_TOTAL_d6}}{0.3}}
    = \val{p3_S8_techo}.}""")
rep(r"""This single-sector ceiling is $0.4\sigma$ above Planck~2018, $2.7\sigma$ above
KiDS-1000, and $2.8\sigma$ above DES-Y3 ($S_8 = 0.776\pm0.017$, 3$\times$2pt).""",
    r"""This single-sector ceiling is $\val{tension_s8_planck_techo}\sigma$ from Planck~2018, $\val{tension_s8_kids1000_techo}\sigma$ from
KiDS-1000, and $\val{tension_s8_desy3_techo}\sigma$ from DES-Y3 ($S_8 = 0.776\pm0.017$, 3$\times$2pt).""")
blk(r"""\begin{table}[h!]
\centering
\caption{$S_8$ comparison: SSEE prediction versus observations.""",
    r"""\paragraph{Note on the amplitude convention, and on Paper~6.}""",
    r"""\begin{table}[h!]
\centering
\caption{$S_8$: the \SSEE\ single-sector ceiling ($A_s$ fixed to Planck,
  $\Omega_{m,\mathrm{CMB}} = \val{OMEGA_M_TOTAL_d6}$, $\sigma_8 = \val{p3_sigma8_techo}$)
  against observations, in units of the observational error
  (\texttt{p5\_techo\_sigma8\_As\_fijo.json}).}
\label{tab:S8}
\begin{tabular}{lcc}
\toprule
Dataset & $S_8$ & $|S_8^{\mathrm{SSEE}} - S_8|/\sigma$ \\
\midrule
Planck 2018 & $0.832 \pm 0.013$ & \val{tension_s8_planck_techo} \\
KiDS-1000   & $\val{S8_k1000_dato}\pm\val{S8_k1000_dato_sigma}$ & \val{tension_s8_kids1000_techo} \\
DES-Y3      & $0.776 \pm 0.017$ & \val{tension_s8_desy3_techo} \\
\midrule
SSEE (ceiling, this work) & $\val{p3_S8_techo}$ & --- \\
\bottomrule
\end{tabular}
\end{table}

With the same error treatment for both models, the IS linear-growth $S_8$ is
$\val{p5_tS8_ssee_kids}\sigma$/$\val{p5_tS8_ssee_des}\sigma$ from KiDS-1000/DES-Y3 and Planck's $\Lambda$CDM
$\val{p5_tS8_lcdm_kids}\sigma$/$\val{p5_tS8_lcdm_des}\sigma$: with $A_s$ fixed to Planck the two are in the
same position, \SSEE\ marginally less tense because its $\Omega_m$ is lower.
(Earlier versions quoted $3.0\sigma$/$3.3\sigma$ for $\Lambda$CDM using only the
observational error for it and the combined error for \SSEE; the asymmetry is
corrected.) The falsification criterion of the growth sector is the one of
Paper~6: a measurement placing $S_8$ more than $3\sigma$ from the prediction
$S_8=\val{S8_leg_pred}$ made with $A_s$ fixed to the model's own CMB fit.

""")
rep(r"""    is essentially identical to $\Lambda$CDM at $z < 1$, with a mean tension
    of $0.70\sigma$ across six data points (vs.\ $0.73\sigma$ for $\Lambda$CDM).}""",
    r"""    is essentially identical to $\Lambda$CDM at $z < 1$, with a mean tension
    of $\val{fs8_tmedia_ssee}\sigma$ across six data points (vs.\ $\val{fs8_tmedia_lcdm}\sigma$ for $\Lambda$CDM).}""")
rep(r"""The tiny $\sim$1\% difference in $\mathcal{G}$ propagates to at most $0.01\sigma$
extra tension — well below the precision of current surveys.""",
    r"""The small difference in $\mathcal{G}$ ($\val{p5_G}$) is well below the precision of
current surveys.""")

# --- EFT ---
blk(r"""\section{EFT Correspondence}""",
    r"""%======================================================================
\section{Discussion}""",
    r"""\section{EFT Correspondence}
\label{sec:EFT}
%======================================================================

In the effective field theory of dark energy \citep{Horndeski1974,Gubitosi2013,Bellini2015}
the action of Paper~7, $S=\int\!\sqrt{-g}\,[M_{\rm Pl}^2R/2+K(X)]$ with
$K=c_1X+c_2X^2$, is a shift-symmetric $k$-essence: the only non-vanishing
Bellini--Sawicki function is the kineticity $\alpha_K$, with
$\alpha_T=\alpha_B=\alpha_M=0$, and the sound speed is $c^2_s=\val{cs2_condensado_d6}$
(Paper~7, verified there with \texttt{hi\_class}). Two consequences for the IS layer:

\begin{itemize}
  \item \textbf{No operator carries the viscosity.} For shift-symmetric $K(X)$ the
    pressure perturbation is exactly adiabatic, $\delta p-c^2_s\delta\rho=0$
    (Section~\ref{subsec:instability}), so the action produces no bulk viscosity.
    The IS layer is a property of the fluid parametrisation used by Boltzmann codes
    and maps to no term of the action. Earlier versions identified
    $\ztilde/(\tauPi H_0)$ with $\bar M_2^2/M_{\rm Pl}^2$; that operator changes the
    tensor speed, $\alpha_T\neq0$, which GW170817 excludes at
    $|\alpha_T|\lesssim10^{-15}$ \citep{Abbott2017GW} and Paper~7 sets to zero. The
    mapping is withdrawn.
  \item \textbf{The ghost condensate is the SSEE sector, not an alternative.}
    Earlier versions contrasted \SSEE\ with the ghost condensate
    \citep{Arkani-Hamed2004} as a mechanism ``with $c^2_s=1$''. The ghost condensate
    has $c^2_s=0$ at its condensate point, and Paper~7's realisation, displaced from
    it to $X/X_{\min}=\val{X_sobre_Xmin_d6}$, has $c^2_s=\val{cs2_condensado_d6}$: it is
    the dark-energy sector of \SSEE. The comparison table that accompanied the
    contrast is withdrawn with it.
\end{itemize}

""")

# --- Discusión ---
blk(r"""The failure of linear IS perturbations to reproduce MIRA""",
    r"""The physical basis once attributed to Paper~6 is withdrawn, and the reason is""",
    r"""Earlier versions asked whether the factor between $\Omega_{m,\mathrm{CMB}}$ and
$1+\wz$ could arise from the IS viscous pressure at the background level, and
reported a background integration giving an effective ratio of $3.04$. No script
or log of that integration survives, so the figure is withdrawn. The question
itself no longer exists: the matter factor $\Omega_{m,\mathrm{CMB}} =
\mathrm{MIRA}\times\Omega_{m,\mathrm{dyn}}$ was withdrawn on 2026-06-18 when OP-8 closed,
$\Omega_{m,\mathrm{CMB}}=\omega_m/h^{2}=\val{OMEGA_M_TOTAL_d6}$ is derived with no factor,
and $\Omega_{m,\mathrm{dyn}}=1+w_0$ is a saturation, not a density.

""")
rep(r"""defined had nothing to be made of.  The near-equality
$\Omega_{m,\mathrm{CMB}}/\Omega_{m,\mathrm{dyn}} \approx 1.93$, once read as
an echo of $\mathrm{MIRA} \simeq 1.999$, is a ratio between objects of
different kinds and carries no information.""",
    r"""defined had nothing to be made of.  The near-equality of
$\Omega_{m,\mathrm{CMB}}/\Omega_{m,\mathrm{dyn}}$ with $\mathrm{MIRA}$, once read as
an echo, is a ratio between objects of different kinds and carries no information.""")
rep(r"""model --- not because $c^2_{s,\mathrm{eff}}=0$, which alone would make the
fluid cluster everywhere, but because the IS friction
$\mathcal{F}(k,a)=(1-3c_s^2)+\tilde z\,(k/aH)^2$ grows as $k^2$
(\S\ref{subsec:damping}) and drives $\delta_{\rm DE}/\delta_m\to0^-$.""",
    r"""model, because the field's positive sound speed turns them into damped acoustic
oscillations below the sound horizon, with $\delta_{\rm DE}/\delta_m\propto k^{-2}$
($\val{q2_r_k3}$ at $k=10\,H_0/c$; \S\ref{subsec:damping}).""")
rep(r"""$\delta_c^{\mathrm{SSEE}} = \val{deltac_ssee_z0}$ at $z_c=0$ and $1.68647$ at $z_c=10$,
against $\Lambda$CDM's $\val{deltac_lcdm_z0} \to 1.68646$: the two are the same to
$0.02\%$.""",
    r"""$\delta_c^{\mathrm{SSEE}} = \val{deltac_ssee_zc0}$ at $z_c=0$ and $\val{deltac_ssee_zc10}$ at $z_c=10$,
against $\Lambda$CDM's $\val{deltac_lcdm_zc0} \to \val{deltac_lcdm_zc10}$: the two agree to the
third decimal.""")
rep(r"""        The IS linear-growth estimate is $S_8 = \val{p3_S8_IS} \pm 0.006$, $2.7\sigma$
        above KiDS-1000/DES-Y3 --- slightly \emph{better} than $\Lambda$CDM
        ($3.0\sigma$/$3.3\sigma$); the conservative CLASS amplitude ceiling is
        $S_8 = \val{p3_S8_techo}$ ($2.7\sigma$ KiDS-1000).""",
    r"""        The IS linear-growth estimate is $S_8 = \val{p3_S8_IS} \pm \val{p5_S8_IS_sigma}$,
          $\val{p5_tS8_ssee_kids}\sigma$/$\val{p5_tS8_ssee_des}\sigma$ from KiDS-1000/DES-Y3, against
          $\val{p5_tS8_lcdm_kids}\sigma$/$\val{p5_tS8_lcdm_des}\sigma$ for Planck's $\Lambda$CDM with the same
          error treatment; the conservative CLASS amplitude ceiling is
          $S_8 = \val{p3_S8_techo}$ ($\val{tension_s8_kids1000_techo}\sigma$ KiDS-1000).""")
rep(r"""        The mean tension across six RSD surveys is $0.70\sigma$, essentially
        identical to $\Lambda$CDM ($0.73\sigma$).""",
    r"""          The mean tension across six RSD surveys is $\val{fs8_tmedia_ssee}\sigma$, essentially
          identical to $\Lambda$CDM ($\val{fs8_tmedia_lcdm}\sigma$).""")
rep(r"""The IS mechanism does not modify $H_0$ directly, since the viscous pressure
$\Pi_{\mathrm{bulk}}$ averages to zero at early times ($z > 5$) when
$\OmDE \to 0$.
The $H_0$ tension between Planck and SH0ES therefore remains at the same
level in SSEE as in $\Lambda$CDM — SSEE does not worsen nor resolve the
$H_0$ tension, but introduces a new prediction for $\sigma_8$ and $S_8$
that partially resolves the lensing tension.""",
    r"""The IS layer does not enter the screening cascade of Paper~9, so nothing in this
paper bears on the $H_0$ comparison; and, as Section~\ref{sec:growth} shows, it
does not move $\sigma_8$ or $S_8$ either.""")
blk(r"""The IS theory satisfies the Hiscock-Lindblom stability criteria""",
    r"""\subsection{Falsifiable predictions summary}""",
    r"""The IS theory satisfies the Hiscock--Lindblom criteria \citep{HiscockLindblom1983}
--- non-negative entropy production and causal propagation --- provided
$\tauPi > 0$ and $\zeta \geq 0$, both of which hold here
(\S\ref{subsec:thermodynamic}); the characteristic speed is
$v^2_{\rm sig}=\wz+\sDE=0\leq c^2$. Those criteria concern the equilibrium state and
the characteristic cone; they do not by themselves forbid a growing mode, and
Section~\ref{subsec:growing} shows that the closure $c^2_s=\wz$ has one. Earlier
versions stated that the signal speed ``saturates the causality bound'' and added
that Eckart theories would produce instabilities in the CMB at $\ell>1000$; the
first came from the $\rho$-normalisation abandoned above and the second had no
calculation behind it. Both are withdrawn.

""")
rep(r"""$c^2_s$ of the dark-energy field (Paper~7; the IS fluid limit is $0$, OP-22b) & $\val{cs2_condensado_d6}$ & $|c^2_s| < 0.05$ & CMB lensing/$T_{\ell\ell'}$ cross \citep{Calabrese2011} / current \\
$S_8$, $A_s$ fixed to the model's own CMB fit (Paper~6) & $\val{S8_leg_pred}$ (no free cosmological parameter) & $\val{S8_leg_tension}\sigma$ from KiDS-Legacy $\val{S8_legacy_dato}\pm\val{S8_legacy_dato_sigma}$ & KiDS-Legacy / current; Euclid / 2027 \\""",
    r"""$c^2_s$ of the dark-energy field (Paper~7; the IS high-frequency limit is $0$, OP-22b) & $\val{cs2_condensado_d6}$ & not yet measured & CMB lensing cross-correlations \citep{Calabrese2011} / forecast \\
$S_8$, $A_s$ fixed to the model's own CMB fit (Paper~6) & $\val{S8_leg_pred}$ (no free cosmological parameter) & $>3\sigma$ (now $\val{S8_leg_tension}\sigma$ from KiDS-Legacy) & KiDS-Legacy / current; Euclid / 2027 \\""")
rep(r"""$D_1$ ratio $\mathcal{G}$ & $\val{p5_G}$ & $0.3\%$ enhancement; below near-term ($\gtrsim 1\%$) sensitivity & Euclid weak lensing / 2027 \\
No DE clustering ($|\delta_{\mathrm{DE}}/\delta_m| < 10^{-3}$) & $< 10^{-3}$ at $k > 20\,H_0/c$ & cosmic variance & Future 21cm surveys / 2030+ \\""",
    r"""$D_1$ ratio $\mathcal{G}$ & $\val{p5_G}$ & below near-term sensitivity & Euclid weak lensing / 2027 \\
DE clustering $\delta_{\mathrm{DE}}/\delta_m$ at $z=0$ & $\val{q2_r_k3}$ at $k=10\,H_0/c$, $\propto k^{-2}$ & per-cent level excluded & Future 21cm surveys / 2030+ \\""")

# --- conclusiones ---
blk(r"""\paragraph{Q1 — Gradient stability (proved analytically).}""",
    r"""\paragraph{Q3 — Growth rate and $S_8$ (SSEE tracks $\Lambda$CDM closely).}""",
    r"""\paragraph{Q1 --- Gradient stability.}
The SSEE structure constants satisfy $\ztilde/(\tauPi H_0) = \sDE = |\wz|$, so the
high-frequency sound speed of the IS fluid vanishes, $\wz+\sDE=0$. That is not
stability: on the growing branch the viscous stiffness never reaches $\sDE$, and the
closure $c^2_s=\wz$ grows at every $k$ ($\lambda=\val{p5_lamIS_k100}\,H_0$ at
$k=100\,H_0/c$). The dark-energy sector is stable because the field of Paper~7 has
$c^2_s=+\val{cs2_condensado_d6}$; with it no mode grows. The quasi-static reduction of
earlier versions was the Navier--Stokes limit and hid the growing branch.

\paragraph{Q2 --- Dark-energy clustering.}
The full IS integration with the field's sound speed gives
$\mathcal{R} = \val{R_media_k10_p5} \pm \val{R_sd_k10_p5}$ at $k\geq10\,H_0/c$ and
$\delta_{\rm DE}/\delta_m=\val{q2_r_k3}$ at $k=10\,H_0/c$, falling as $k^{-2}$: a bound on
dark-energy clustering. The perturbations cross the phantom divide at
$z_*=\val{z_cruce}$ without divergence; the viscous pressure that carries the crossing
exceeds the near-equilibrium range of linear Israel--Stewart for $z\gtrsim z_*$
($|\Pi|/|p|=\val{p5_Pip_z1}$ at $z=1$), and whether the nonlinear theory returns $w_a$
is open (OP-24). MIRA has no carrier in this sector and survives only as the
algebraic invariant entering $f_{\rm screen}$ (Paper~9).

""")
rep(r"""$\sigma_8^{\mathrm{SSEE}} = \val{p3_sigma8_IS} \pm 0.006$ and an IS linear-growth
$S_8^{\mathrm{IS}} = \val{p3_S8_IS} \pm 0.006$ ($2.7\sigma$ above KiDS-1000, slightly
\emph{better} than $\Lambda$CDM at $3.0\sigma$).""",
    r"""$\sigma_8^{\mathrm{SSEE}} = \val{p3_sigma8_IS} \pm \val{p5_sigma8_IS_sigma}$ and an IS linear-growth
$S_8^{\mathrm{IS}} = \val{p3_S8_IS} \pm \val{p5_S8_IS_sigma}$ ($\val{p5_tS8_ssee_kids}\sigma$ from KiDS-1000,
against $\val{p5_tS8_lcdm_kids}\sigma$ for Planck's $\Lambda$CDM with the same error treatment).""")
rep(r"""($2.7\sigma$ KiDS-1000), coincides with the IS linear-growth estimate above:""",
    r"""($\val{tension_s8_kids1000_techo}\sigma$ KiDS-1000), coincides with the IS linear-growth estimate above:""")
rep(r"""The mean $f\sigma_8$ tension across six RSD surveys is $0.70\sigma$,
essentially identical to $\Lambda$CDM ($0.73\sigma$).""",
    r"""The mean $f\sigma_8$ tension across six RSD surveys is $\val{fs8_tmedia_ssee}\sigma$,
essentially identical to $\Lambda$CDM ($\val{fs8_tmedia_lcdm}\sigma$).""")
rep(r"""(i) causally and thermodynamically stable (Q1),""",
    r"""(i) stable, through the field's positive sound speed rather than through the IS
    layer, which is causal and thermodynamically consistent but does not by itself
    remove the instability of the closure $c^2_s=w$ (Q1),""")
rep(r"""    with $f\sigma_8$ tension of $0.70\sigma$ (vs.\ $0.73\sigma$ for $\Lambda$CDM), and""",
    r"""    with $f\sigma_8$ tension of $\val{fs8_tmedia_ssee}\sigma$ (vs.\ $\val{fs8_tmedia_lcdm}\sigma$ for $\Lambda$CDM), and""")
rep(r"""(iii) strictly bounded: the MIRA factor cannot be derived from IS dynamics (Q2);""",
    r"""(iii) weakly clustered, $\delta_{\rm DE}/\delta_m\propto k^{-2}$ (Q2), with no MIRA factor to derive;""")
rep(r"""The Python script \texttt{src/ssee\_paper5\_IS\_perturbations.py} (including
the growth rate and $S_8$ computations) and all output figures are available in""",
    r"""The Python scripts \texttt{src/p05\_IS/ssee\_paper5\_IS\_perturbations.py} (Q1--Q3,
growth rate and $S_8$), \texttt{estabilidad\_IS\_completa.py} (growing branch) and
\texttt{cruce\_fantasma\_IS.py} (phantom crossing), their logs, and all output figures are available in""")
rep(r"""All computations use publicly available Python packages (NumPy, SciPy, Matplotlib).""",
    r"""All computations use publicly available Python packages (NumPy, SciPy, Matplotlib)
and, for the amplitude ceiling, CLASS.""")

# --- apéndice A ---
rep(r"""For modes $e^{i(\mathbf{k}\cdot\mathbf{x} - \omega t)}$:
\begin{equation}
  \delta\Pi = -\frac{i\zeta k}{\tauPi(-i\omega)+1}\,v_\parallel,
\end{equation}""",
    r"""For modes $e^{i(\mathbf{k}\cdot\mathbf{x} - \omega t)}$:
\begin{equation}
  \delta\Pi = -\frac{i\zeta k}{1-i\omega\tauPi}\,v_\parallel,
\end{equation}""")
blk(r"""Combining with the Euler equation --- whose inertia is the enthalpy""",
    r"""%======================================================================
\section{Eigenvalue Analysis of the IS Perturbation Matrix}""",
    r"""Combining with the continuity and Euler equations --- whose inertia is the enthalpy
$\bar\rho+\bar p$, as written above, \emph{not} $\bar\rho$:
\begin{equation}
  \omega^2 = \left[c^2_{s,\mathrm{bare}}
    + \frac{\zeta}{\tauPi(\bar\rho+\bar p)}\,\frac{-i\omega\tauPi}{1-i\omega\tauPi}\right]k^2 .
\end{equation}
For $|\omega|\tauPi \gg 1$ the bracket tends to
$c^2_{s,\mathrm{bare}} + \zeta/[\tauPi(\bar\rho+\bar p)]$. With the \SSEE\ normalisation
$\zeta = \ztilde\,(\rho_{\mathrm{DE}}+p_{\mathrm{DE}})/H_0$
(Section~\ref{subsec:IS_params}) this is
\begin{equation}
  c^2_{s,\mathrm{eff}} = c^2_{s,\mathrm{bare}} + \frac{\ztilde}{\tauPi H_0},
\end{equation}
recovering Eq.~\eqref{eq:cs2_eff_def}. For a growing mode, $\omega=i\lambda$, the
factor $-i\omega\tauPi/(1-i\omega\tauPi)$ becomes $\lambda\tauPi/(1+\lambda\tauPi)<1$,
which gives Eq.~\eqref{eq:growing_branch}. (Earlier versions wrote
$\zeta=\ztilde(\rho+p)H_0$ and equated $\ztilde H_0/\tauPi$ with $\ztilde/(\tauPi H_0)$;
the placement of $H_0$ is corrected, and the result is unchanged.)

""")
blk(r"""The quasi-static 4-variable system""",
    r"""%======================================================================
\clearpage
\bibliographystyle{plainnat}""",
    r"""The five-variable system $\mathbf{Y} = [\delta_m, v_m, \delta_{\mathrm{DE}},
v_{\mathrm{DE}}, \Pitilde]^\top$ of Eqs.~\eqref{eq:deltam}--\eqref{eq:Poisson}, with the
field's sound speed, is linear; its Jacobian with respect to $\ln a$, evaluated by the
same code that integrates it at $z=0$ and $k=10\,H_0/c$
(\texttt{p5\_IS\_perturbations\_Q2.json}, \texttt{autovalores\_k10\_z0}), has
eigenvalues
\begin{equation}
  \lambda = \val{p5_eig0},\quad \val{p5_eig1},\quad
  \val{p5_eig2}\pm\val{p5_eig_im}\,i,\quad \val{p5_eig4}.
\end{equation}
The positive one is the matter growing mode at frozen coefficients and the most
negative the decaying one; the complex pair is the damped acoustic oscillation of the
dark-energy perturbation, which carries the $k^{-2}$ suppression of
Section~\ref{subsec:damping}. No dark-energy mode grows. Earlier versions printed four
eigenvalues for a different matrix with no recorded computation; they are withdrawn.

""")

open(P, "w").write(s)

# --- bibliografía ---
B = "manuscript/ssee_paper5.bib"
b = open(B).read()
add = ""
for key, ent in [
    ("KunzSapone2006", """
@article{KunzSapone2006,
  author  = {Kunz, M. and Sapone, D.},
  title   = {Crossing the phantom divide},
  journal = {Phys. Rev. D},
  year    = {2006},
  volume  = {74},
  pages   = {123503},
  eprint  = {astro-ph/0609040}
}
"""),
    ("MaartensMendez1997", """
@article{MaartensMendez1997,
  author  = {Maartens, R. and M\\'endez, V.},
  title   = {Nonlinear bulk viscosity and inflation},
  journal = {Phys. Rev. D},
  year    = {1997},
  volume  = {55},
  pages   = {1937},
  eprint  = {astro-ph/9611205}
}
"""),
    ("CruzLepe2017", """
@article{CruzLepe2017,
  author  = {Cruz, N. and Lepe, S.},
  title   = {Crossing the phantom divide with dissipative normal matter in the {Israel--Stewart} formalism},
  journal = {Phys. Lett. B},
  year    = {2017},
  doi     = {10.1016/j.physletb.2017.01.035},
  eprint  = {1607.04192}
}
"""),
    ("CruzCruzLepe2017", """
@article{CruzCruzLepe2017,
  author  = {Cruz, M. and Cruz, N. and Lepe, S.},
  title   = {Phantom solution in a non-linear {Israel--Stewart} theory},
  journal = {Phys. Lett. B},
  year    = {2017},
  volume  = {769},
  pages   = {159},
  eprint  = {1701.06724}
}
"""),
    ("Abbott2017GW", """
@article{Abbott2017GW,
  author  = {{LIGO Scientific Collaboration} and {Virgo Collaboration} and {Fermi GBM} and {INTEGRAL}},
  title   = {Gravitational Waves and Gamma-rays from a Binary Neutron Star Merger: {GW170817} and {GRB 170817A}},
  journal = {Astrophys. J. Lett.},
  year    = {2017},
  volume  = {848},
  pages   = {L13},
  eprint  = {1710.05834}
}
"""),
]:
    if key not in b:
        add += ent
open(B, "w").write(b + add)
print("P5: reemplazos aplicados")
