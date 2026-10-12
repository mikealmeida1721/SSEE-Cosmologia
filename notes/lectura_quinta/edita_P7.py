#!/usr/bin/env python3
"""Quinta lectura P7 (2026-10-11): reemplazos exactos; aborta si un conteo no casa.

Hallazgo central: el campo NO está quieto. Sin potencial, a^3 K_X phidot se
conserva (Scherrer 2004) y X rueda hacia X_min (w = -1): su w_a propio es +0.41,
de signo contrario al algebraico. Un solo campo no cruza w = -1 (Vikman 2005).
La viscosidad de Eckart de P1 puesta en la continuidad de este campo no da
(w0, wa). Decisión de Mike (2026-10-11): w0 es dinámico; la pregunta abierta es
por qué ocurre el cruce fantasma. Log: results/logs/p7_fondo_campo.json.
"""
import sys

P = "manuscript/SSEE_Paper7_EFT.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


# ── resumen ──────────────────────────────────────────────────────────────
rep(r"""which reproduces $w_\phi = w_0 = \val{W0_d6}$ exactly and yields the""",
    r"""which reproduces $w_\phi = w_0 = \val{W0_d6}$ today and yields the""")
rep(r"""\emph{ghost condensate}, stabilised at $X/X_{\min} = \val{X_sobre_Xmin_d6}$, where
the no-ghost condition $K_X + 2XK_{XX} > 0$ and the gradient condition
$c_s^2 > 0$ both hold.""",
    r"""\emph{ghost condensate}, today at $X/X_{\min} = \val{X_sobre_Xmin_d6}$, where
the no-ghost condition $K_X + 2XK_{XX} > 0$ and the gradient condition
$c_s^2 > 0$ both hold.
The field is not static: with no potential, $a^3K_X\dot\phi$ is conserved and $X$
rolls towards $X_{\min}$, where $w_\phi=-1$, so the action fixes $w_0$ today while
its own evolution has $w_a^\phi = \val{p7_wa_campo}$, of the opposite sign to the
algebraic $w_a$. A single field cannot cross $w=-1$; what drives the phantom
crossing of the algebraic $w(a)$ is the principal open question, and we show that
a bulk (Eckart) viscosity acting on this field does not supply it.""")

# ── introducción ─────────────────────────────────────────────────────────
rep(r"""$w_0 = -T_r/M_v \approx -0.840$ and $w_a = -P_{sc}/I_g \approx -0.670$""",
    r"""$w_0 = -T_r/M_v = \val{W0_d6}$ and $w_a = -P_{sc}/I_g = \val{WA_d6}$""")
rep(r"""The algebraic point $(w_0,w_a) = (-0.840,-0.670)$ falls within""",
    r"""The algebraic point $(w_0,w_a)$ falls within""")
rep(r"""Bayesian validation (MCMC vs DESI+Planck), CMB confrontation, algebraic
$H_0$ derivation, interacting-sector perturbation theory, and a""",
    r"""Bayesian validation (MCMC vs DESI+Planck), CMB confrontation, the algebraic
derivation of the CMB parameters, Israel--Stewart causal perturbation theory, and a""")
rep(r"""Meanwhile the
$f\sigma_8$ growth-rate tension is already resolved at the single-sector
level ($0.70\sigma$, statistically identical to $\Lambda$CDM $0.73\sigma$)
\citep{ssee_paper5}.""",
    r"""Nor is there an $f\sigma_8$ tension to resolve: across six RSD surveys the
mean single-sector tension is $\val{fs8_tmedia_ssee}\sigma$, statistically identical to
$\Lambda$CDM's $\val{fs8_tmedia_lcdm}\sigma$ \citep{ssee_paper5}.""")

# ── normalización: porcentaje a mano ─────────────────────────────────────
rep(r"""the amplitude error
is $21.5\%$ and it is corrected here.""",
    r"""the amplitude error
is $\val{p7_norm_err_pct}\%$ and it is corrected here.""")

# ── lo que no se toca: w0 es algebraico, no medido ───────────────────────
rep(r"""So is $w_0$ itself, which is measured, not postulated: the algebraic
point""",
    r"""Nor does it touch $w_0$ itself, which is algebraic and confronted with data: the algebraic
point""")

# ── estabilidad ──────────────────────────────────────────────────────────
rep(r"""A dark-energy sound speed of this size makes the field clustered rather
than smooth, with a sound horizon $c_s/H_0 \approx \val{horizonte_cs_d0}$~Mpc.""",
    r"""A dark-energy sound speed of this size lets the field cluster below its
sound horizon $c_s/H_0 \approx \val{horizonte_cs_d0}$~Mpc rather than stay smooth, although
weakly: with this $c_s^2$, Paper~5 finds $|\delta_{\rm DE}/\delta_m| = \val{q2_r_k3}$ at
$k=10\,H_0$, falling as $k^{-2}$.""")
rep(r"""phantom.  Since the present action has no coupling, $\weff = \wphi = w_0
= \val{W0_d6} > -1$ at all times, and no phantom crossing is claimed.""",
    r"""phantom.  It stays so: along its free evolution (§\ref{sec:background})
$X > X_{\min}$ at all times, so $1+2u<0$ (with $c_1<0$, $\rho_\phi+p_\phi>0$) and $c_s^2>0$ throughout.  The field
therefore cannot carry the phantom crossing of the algebraic $w(a)$: no single
minimally coupled field crosses $w=-1$ stably \citep{Vikman2005}, and in this
family every state with $w_\phi<-1$ has $c_s^2<0$.  What carries the crossing is
the open question of §\ref{sec:synthesis}.""")

# ── fondo: el campo rueda ────────────────────────────────────────────────
rep(r"""constraint at each integration step.  In terms of the ratio $u$ of
§\ref{sec:action}, Eq.~(\ref{eq:phi_N}) is the statement that
$X$ relaxes towards the condensate point $X_{\rm bg}$ of
Eq.~(\ref{eq:condensate}).""",
    r"""constraint at each integration step.

\paragraph{The field rolls.}
With no potential the Klein--Gordon equation is a conservation law,
$d(a^3K_X\dot\phi)/dt=0$, so $K_X\sqrt{X}\propto a^{-3}$ \citep{Scherrer2004}.
In terms of $y\equiv X/X_{\min}=-2u$,
%
\begin{equation}
  (y-1)\sqrt{y}\propto a^{-3},\qquad
  w_\phi=\frac{y-2}{3y-2},\qquad
  c_s^2=\frac{1-y}{1-3y}.
  \label{eq:rueda}
\end{equation}
%
The field does not stay at $X_{\rm bg}$: it relaxes towards $X_{\min}$, where
$K_X=0$ and $w_\phi=-1$, and $X_{\rm bg}$ of Eq.~(\ref{eq:condensate}) is only its
present value.  Integrating back, $w_\phi=\val{p7_wphi_a05}$ at $a=0.5$ and
$\val{p7_wphi_a03}$ at $a=0.3$; at $a=1$ the field's own
$w_a^\phi\equiv-dw_\phi/da=\val{p7_wa_campo}$, of the opposite sign to the algebraic
$w_a=\val{WA_d6}$.  The action thus fixes $w_0$ and $c_s^2$ today, not the history
$w(a)$ (§\ref{sec:synthesis}).  Since $y>1$ throughout, $c_s^2$ stays positive and
grows into the past.""")

# ── entradas de hi_class ─────────────────────────────────────────────────
rep(r"""  \item $w_\phi = w_0 = \val{W0_d6}$ (constant at the condensate point);""",
    r"""  \item $w_\phi = w_0 = \val{W0_d6}$, the present value (the field's own evolution,
    §\ref{sec:background}, is not entered);""")
rep(r"""as $w_\phi = w_0 = \val{W0_d6}$ with $w_a = 0$ (the field sits at the
condensate point, §\ref{sec:action}), and the""",
    r"""as $w_\phi = w_0 = \val{W0_d6}$ with $w_a = 0$ (the present value of the field held
fixed: the run tests the perturbation sector at $z=0$, not the field's own
background, §\ref{sec:background}), and the""")
rep(r"""$w_a = 0$ (field)  & accepted \\""",
    r"""$w_a = 0$ (field today)  & accepted \\""")
rep(r"""  \item The run does not include the viscosity, which is what produces
    $w_a$.  \textsc{hi\_class} admits no viscous background, so no CMB""",
    r"""  \item The run does not include whatever produces $w_a$ (in the closure of
    Paper~1, a bulk viscosity; §\ref{sec:synthesis} shows that closure fails on
    this field).  \textsc{hi\_class} admits no viscous background, so no CMB""")

# ── síntesis ─────────────────────────────────────────────────────────────
rep(r"""  \item \textbf{Stability:} ghost-free and gradient-stable at the
    condensate point $X/X_{\min} = \val{X_sobre_Xmin_d6}$, with the NEC satisfied and
    no phantom character in the field.""",
    r"""  \item \textbf{Stability:} ghost-free and gradient-stable today at
    $X/X_{\min} = \val{X_sobre_Xmin_d6}$ and along the field's whole free evolution
    ($X>X_{\min}$), with the NEC satisfied and no phantom character in the field.""")
rep(r"""  \item \textbf{The origin of $w_a$ --- the principal gap.}
    At the condensate point the field has constant $w_\phi = w_0$, so the
    action of §\ref{sec:action} predicts $w_a = 0$, not the algebraic
    $w_a = -P_{sc}/I_g = \val{WA_d6}$.  The evolution must come from the
    Israel-Stewart viscosity of Paper~5, which no Horndeski solver
    currently admits.  Until that is implemented, this paper accounts for
    $w_0$ and leaves $w_a$ to Paper~5.  The failure of the withdrawn
    potential to produce $w_a$ (§\ref{sec:withdrawn}) is evidence that
    the answer is not in the scalar sector at all.""",
    r"""  \item \textbf{The origin of $w_a$ and of the phantom crossing --- the principal gap.}
    The field is not static (§\ref{sec:background}): it rolls towards
    $w_\phi=-1$, with its own $w_a^\phi=\val{p7_wa_campo}$, opposite in sign to the
    algebraic $w_a = -P_{sc}/I_g = \val{WA_d6}$.  Being a single minimally coupled
    field it cannot cross $w=-1$ \citep{Vikman2005}, while the algebraic $w(a)$
    crosses at $z_*=\val{z_cruce}$; something beyond the field must carry the
    crossing.  Paper~1 assigns it to a bulk viscosity
    $\Pi=-3\Gamma(1-a)\rho_{\rm DE}$ with the algebraic $\Gamma=P_{sc}/(3I_g)$, but
    that closure presupposes a field of constant $w$ --- the single-power field
    shown unstable in §\ref{sec:action}.  Placing the same viscosity in the
    continuity equation of this field gives, fitted over $0.30\le a\le0.773$,
    $(w_0,w_a)=(\val{p7_visc_w0},\val{p7_visc_wa})$, $\val{p7_visc_sig}\sigma$ from
    DESI~DR2+CMB+Pantheon+, a crossing at $z=\val{p7_visc_zc}$ instead of
    $\val{z_cruce}$, and it drives the field itself phantom (hence
    gradient-unstable) for $a<\val{p7_visc_afant}$.  Scanning $\Gamma\in[0,1]$,
    $\val{p7_barrido_muere}$ of $\val{p7_barrido_n}$ values drive $\rho_\phi$ to zero
    before $a=0.3$ and the best of the rest lies $\val{p7_barrido_sig}\sigma$ from
    DESI (\texttt{src/p07\_eft/fondo\_campo\_p7.py}).  Neither the withdrawn
    potential (§\ref{sec:withdrawn}) nor the Eckart closure produces $w_a$; a
    causal (Israel--Stewart) viscosity with its relaxation time, which Paper~5
    shows must be taken beyond the linear regime, is untested.  Why the
    algebraic $w(a)$ crosses $w=-1$ is the open question.""")
rep(r"""  \item \textbf{Full CMB likelihood:} requires a Boltzmann code with a
    viscous background; \textsc{hi\_class} cannot supply one.""",
    r"""  \item \textbf{Full CMB likelihood:} requires a Boltzmann code with the
    background that carries $w_a$; \textsc{hi\_class} cannot supply one.""")

# ── CUARTAL: porcentaje a mano (tres sitios) ─────────────────────────────
rep(r"""$2.50\%$""", r"""$\val{p7_cuartal_pct}\%$""", n=3)

# ── conclusiones ─────────────────────────────────────────────────────────
rep(r"""condensate: a wrong-sign linear term with the field stabilised $4.5\%$
above the minimum of $K$, where ghost and gradient conditions both hold.""",
    r"""condensate: a wrong-sign linear term with the field today $\val{p7_Xbg_pct}\%$
above the minimum of $K$, where ghost and gradient conditions both hold.""")
rep(r"""What this paper accounts for is $w_0$, with a stable Lagrangian behind
it.  What it does not account for is $w_a$: at the condensate point the
field has constant equation of state, and the evolution must come from
the Israel-Stewart viscosity of Paper~5.  We state this as the principal
open gap rather than closing it with a structure that does not work.""",
    r"""What this paper accounts for is $w_0$ and $c_s^2$ today, with a stable
Lagrangian behind them.  What it does not account for is $w_a$: the field is not
static but rolls towards $w=-1$, with its own $w_a^\phi=\val{p7_wa_campo}$ of the wrong
sign; as a single field it cannot cross $w=-1$; and the viscous closure of
Paper~1, placed in this field's continuity equation, misses DESI by
$\val{p7_visc_sig}\sigma$.  Why the algebraic $w(a)$ crosses the phantom divide is
the principal open gap, and we state it as such rather than closing it with a
structure that does not work.""")

# ── bibliografía: títulos reales y dos referencias nuevas ────────────────
rep(r"""  \textit{SSEE: Structural Self-Energy Expansion — Framework and
  Predictive Register}. Zenodo. Paper~1.""",
    r"""  \textit{A Minimal-Parameter Framework for Cosmological Dynamics and Galaxy
  Cluster Mass Discrepancies via Structural Self-Energy Expansion (SSEE)}.
  Zenodo. Paper~1.""")
rep(r"""  \textit{Bayesian Validation of SSEE against DESI DR2, Planck and
  Galaxy Clusters}. Zenodo. Paper~2.""",
    r"""  \textit{Bayesian MCMC Validation of the Structural Self-Energy Expansion
  Framework (SSEE): Model Comparison against $\Lambda$CDM and CPL using DESI~DR2,
  Planck~2018, and Galaxy-Cluster Mass Data}. Zenodo. Paper~2.""")
rep(r"""  \textit{IS Causal Perturbation Theory in SSEE: Stability, MIRA,
  $S_8$ and $f\sigma_8$}. Zenodo. Paper~5.""",
    r"""  \textit{Israel-Stewart Causal Viscous Perturbations in the SSEE Dark Energy
  Framework: Stability from the Field, Weak Dark-Energy Clustering, and
  $\Lambda$CDM-Consistent Structure Growth}. Zenodo. Paper~5.""")
rep(r"""  \textit{The Growth Sector of SSEE against Raw Data: a Single Matter
  Sector and the Retraction of $\phi$-DM}. Zenodo. Paper~6.""",
    r"""  \textit{SSEE and the Growth Sector Re-examined: No Second Matter Component,
  and No $S_8$ Tension, on Raw Survey Data}. Zenodo. Paper~6.""")
rep(r"""  \textit{SSEE in the Strong-Gravity Regime: Disformal Geodesics,
  MIRA Lensing Emergence, and Vainshtein Screening}. Zenodo. Paper~8.""",
    r"""  \textit{SSEE in the Strong-Gravity Regime: Disformal Geodesics, MIRA
  Emergence, and Solar-System Compliance}. Zenodo. Paper~8.""")
rep(r"""\bibitem[Amendola(2000)]{amendola2000}""",
    r"""\bibitem[Scherrer(2004)]{Scherrer2004}
  Scherrer, R.~J. (2004).
  Purely kinetic k-essence as unified dark matter.
  \textit{Phys.\ Rev.\ Lett.}, 93, 011301.
  arXiv:astro-ph/0402316.

\bibitem[Vikman(2005)]{Vikman2005}
  Vikman, A. (2005).
  Can dark energy evolve to the phantom?
  \textit{Phys.\ Rev.\ D}, 71, 023515.
  arXiv:astro-ph/0407107.

\bibitem[Amendola(2000)]{amendola2000}""")

open(P, "w").write(s)

# ── P1, sección EFT ──────────────────────────────────────────────────────
E = "manuscript/SSEE_EFT_section.tex"
e = open(E).read()
o = r"""($c_1<0$, $c_2>0$) that reproduces $w_\phi=w_0$ through
$w_\phi=K/(2XK_X-K)$ and has $c_s^2=\val{cs2_condensado_d6}>0$, free of ghost and
gradient instabilities."""
n = r"""($c_1<0$, $c_2>0$) that reproduces $w_\phi=w_0$ today through
$w_\phi=K/(2XK_X-K)$ and has $c_s^2=\val{cs2_condensado_d6}>0$, free of ghost and
gradient instabilities.  That field is not static: with no potential it rolls
towards $w_\phi=-1$, with its own $w_a^\phi=\val{p7_wa_campo}$, and as a single field it
cannot cross $w=-1$; what carries the algebraic $w_a$ and the phantom crossing is
open (Paper~7)."""
if e.count(o) != 1:
    sys.exit("EFT section: conteo")
open(E, "w").write(e.replace(o, n))

# ── P5, la línea del cierre ──────────────────────────────────────────────
Q = "manuscript/SSEE_Paper5_IS.tex"
q = open(Q).read()
o = r"""$\rho_{\rm DE}(1+\wz)>0$: in the closure of Paper~1 the field carries $w_0$ and the
background viscous pressure carries the rest of $w(a)$, including the phantom
crossing at $z_*=\val{z_cruce}$"""
n = r"""$\rho_{\rm DE}(1+\wz)>0$: in the closure of Paper~1 the field is assigned $w_0$ and the
background viscous pressure the rest of $w(a)$, including the phantom
crossing at $z_*=\val{z_cruce}$ (an algebraic split: the field of Paper~7 rolls towards
$w=-1$ and does not hold $w_0$ by itself, and that closure does not reproduce
$w_a$ dynamically --- Paper~7, OP-24; we keep the present-day inertia and $c_s^2$, the
latter only growing into the past)"""
if q.count(o) != 1:
    sys.exit("P5: conteo")
open(Q, "w").write(q.replace(o, n))
print("P7, sección EFT de P1 y P5: reemplazos aplicados")
