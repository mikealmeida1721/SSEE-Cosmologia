#!/usr/bin/env python3
"""P10, quinta lectura (2026-10-12): lo que la lectura encontró, con su porqué en notes/lectura_quinta/P10.md."""
import sys

P = "manuscript/SSEE_Paper10_UVCompletion.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


# 0. un solo H_glob (P9, nota al pie de régimen): nada de «H_0^{glob,UV}»
rep(r"H_0^{\rm glob,UV}", r"H_0^{\rm glob}", n=10)

# 1. resumen
rep(r"""Within the Structural Self-Energy Expansion (SSEE), the infrared (IR) kinetic
Lagrangian $K(X) = X/\KAL$ produces a local Hubble correction""",
    r"""Within the Structural Self-Energy Expansion (SSEE), the dark-energy equation
of state fixes a local Hubble correction""")
rep(r"""$K(X) = X/\KAL + X^2/M^4$ and identify the unique algebraic value of the
UV cutoff $M$ such that the theory remains connected to the inflationary
$\alpha$-attractor of Paper~1.
The $\alpha$-attractor parameter $\alpha = \phiG^4/3$, which fixes the
inflationary tensor-to-scalar ratio $r = 12\alpha/N^2 \approx \val{R_TENSOR_d5}$
(a pre-committed LiteBIRD target), also determines""",
    r"""$K(X) = X/\KAL + X^2/M^4$ and propose (Conjecture~C.1) that its UV cutoff $M$
is set by the inflationary $\alpha$-attractor of Paper~1: the parameter
$\alpha = \phiG^4/3$, which fixes the inflationary tensor-to-scalar ratio
$r = 12\alpha/N^2 \approx \val{R_TENSOR_d5}$ (a pre-committed LiteBIRD target), would
also determine""")
rep(r"""$3(\phiG+\pi)^2 = \val{H0_ALG_d5}$ by $\val{p9_hglob_residuo}$ --- the headline UV
result of this paper, refining the IR residual $\val{p9_sh0es_res_IR}$ ($\val{p9_sh0es_sig_IR}\sigma$).""",
    r"""$3(\phiG+\pi)^2 = \val{H0_ALG_d5}$ by $\val{p9_hglob_residuo}$, far inside the propagated
$\pm\val{p9_hglob_sigma}$: the cascade is consistent with the cutoff but does not
measure it (§\ref{sec:hubble}).""")
rep(r"""The same $\alpha$ that governs inflation at $z \sim 10^{60}$ thus fixes the
dark-energy UV scale today, providing a falsifiable cross-epoch consistency test:
if LiteBIRD measures $r \neq \val{R_TENSOR_d5}$, both $\alpha$ and $M$ change, and the
predicted $H_0^{\rm glob}$ changes accordingly.""",
    r"""If the conjecture holds, the same $\alpha$ that governs inflation fixes the
dark-energy UV scale today. The decisive leg of the resulting cross-epoch test
is $r$ itself; the Hubble leg votes only if LiteBIRD finds
$r < \val{p10_r_umbral}$ (§\ref{sec:cross}).""")

# 2. introducción
rep(r"""$\sK = -3w_0(1+w_0) = \val{S_K_d6}$ \citep{SSEE7,SSEE8} and the lensing factor
$\MIRA = \AURA/2$ combine""",
    r"""$\sK = -3w_0(1+w_0) = \val{S_K_d6}$ \citep{SSEE1,SSEE9} and the structural constant
$\MIRA = \AURA/2$ combine""")
rep(r"""That IR result uses the kinetic Lagrangian $K(X) = X/\KAL$ (the leading term),
and the UV cutoff $M \to \infty$ is implicit.""",
    r"""That IR result uses $w_0$ alone. Describing its UV correction requires a
kinetic functional with a cutoff $M$, and the IR result is its limit
$M\to\infty$.""")
rep(r"""We show that the unique algebraically consistent value of $M$ is""",
    r"""We propose (Conjecture~C.1, §\ref{sec:theorem}) that the cutoff is""")
rep(r"""The physical picture is intriguing: the \emph{same curvature parameter $\alpha$
that shaped the inflationary plateau at $z \sim 10^{60}$} provides the speed
limit $M$ for the dark-energy kinetic term today.""",
    r"""If the conjecture holds, the \emph{same curvature parameter $\alpha$ that shaped
the inflationary plateau} provides the speed limit $M$ of the screening
functional today.""")

# 3. N_* a mano; cota de r: 0.036 es BICEP/Keck 2021, no Planck 2018; LiteBIRD apunta a δr < 0.001
rep(r"""    \;\approx\; \frac{12 \times \val{ALPHA_ATT_d4}}{58.07^2}""",
    r"""    \;\approx\; \frac{12 \times \val{ALPHA_ATT_d4}}{\val{N_star_d2}^2}""")
rep(r"""for $N = 2\varphi^7 \approx 58.07$ e-folds,""",
    r"""for $N = 2\varphi^7 \approx \val{N_star_d2}$ e-folds,""")
rep(r"""This prediction lies below the current upper bound $r < 0.036$
\citep{Akrami2020} and is within the anticipated sensitivity of LiteBIRD
\citep{LiteBIRD2020} (target $\sigma_r \sim 0.002$, expected results 2032)""",
    r"""This prediction lies below the current upper bound $r < 0.036$
\citep{BK2021} (Planck~2018 with BK15 gave $r<0.056$~\citep{Akrami2020}) and
is within the anticipated sensitivity of LiteBIRD \citep{LiteBIRD2020} (total
uncertainty $\delta r < 0.001$; launch planned for the early 2030s)""")
rep(r"""  \item LiteBIRD (2032) should measure""", r"""  \item LiteBIRD should measure""")
rep(r"""$r \approx \val{R_TENSOR_d5}$ (LiteBIRD 2032),""", r"""$r \approx \val{R_TENSOR_d5}$ (LiteBIRD),""")

# 4. M y ρ_c^(1/4) a mano; H_glob no es «el valor anclado al CMB de Paper III»
rep(r"""    \;\approx\; 9.68 \text{ meV}\,,
  \label{eq:Mmev}""",
    r"""    \;\approx\; \val{M_meV_d2} \text{ meV}\,,
  \label{eq:Mmev}""")
rep(r"""where $\rhoc^{1/4} \approx 2.47$ meV is the SSEE critical-density scale today,
evaluated at the model's physical Hubble rate $H_0 = \val{H0_GLOBAL_d5}$~km/s/Mpc
(the CMB-anchored value of Paper~III).""",
    r"""where $\rhoc^{1/4} \approx \val{rhoc14_meV_d2}$ meV is the SSEE critical-density scale today,
evaluated at the model's global rate $H_0^{\rm glob} = \val{H0_GLOBAL_d5}$~km/s/Mpc
(the output of the SH0ES cascade, Paper~9).""")
rep(r"""Root form     & $M = \phiG^2\,5^{1/4}\,\rhoc^{1/4}$ & $9.68$ meV \\""",
    r"""Root form     & $M = \phiG^2\,5^{1/4}\,\rhoc^{1/4}$ & $\val{M_meV_d2}$ meV \\""")
rep(r"""$M$ in meV & $M = \phiG^2\,5^{1/4}\,\rhoc^{1/4}$ & 9.68 meV & Eq.~\eqref{eq:Mmev} \\""",
    r"""$M$ in meV & $M = \phiG^2\,5^{1/4}\,\rhoc^{1/4}$ & \val{M_meV_d2} meV & Eq.~\eqref{eq:Mmev} \\""")

# 5. el IR no «usa K = X/KAL» en Papers 1–9: usa w0 (P7 es c1X + c2X²)
rep(r"""$\KAL = (\phiG+3\pi)/2 \approx 5.521$ is the SSEE structural retention
(Papers 1--7), and $M^4 = 45\alpha^2\rhoc$ is the UV cutoff introduced in
Eq.~\eqref{eq:M4main}.
The IR limit $M \to \infty$ recovers $K(X) = X/\KAL$, which reproduces
$\sK^{\rm IR} = \val{S_K_d6}$ exactly and is the description used in
Papers~1--9.""",
    r"""$\KAL = (\phiG+3\pi)/2 \approx \val{KAL0_d3}$ is the SSEE structural retention
(Paper~1), and $M^4 = 45\alpha^2\rhoc$ is the UV cutoff of Conjecture~C.1,
Eq.~\eqref{eq:M4main}.
The IR limit $M \to \infty$ reduces it to $K(X) = X/\KAL$, whose background
reproduces $\sK^{\rm IR} = \val{S_K_d6}$; Papers~1--9 take $\sK^{\rm IR}$ directly from
$w_0$.""")
rep(r"""different jobs: Paper~7's action reproduces $w_0$ and $c_s^2$ from the
Lagrangian, whereas""",
    r"""different jobs: Paper~7's action reproduces $w_0$ and $c_s^2$ today from the
Lagrangian (its field rolls toward $w=-1$), whereas""")

# 6. cifras del fondo a mano
rep(r"""a 1.7\% reduction from the IR value $X_{\rm bg}^{\rm IR} = \val{X_bg_IR_d5}\,\rhoc$.
The UV correction is perturbative: $\varepsilon \equiv X_{\rm bg}^2/M^4
\approx 5.7\times10^{-4}$.""",
    r"""a \val{p10_X_red_pct}\% reduction from the IR value $X_{\rm bg}^{\rm IR} = \val{X_bg_IR_d5}\,\rhoc$.
The UV correction is perturbative: $\varepsilon \equiv X_{\rm bg}^2/M^4
\approx \val{eps_UV}$ (in units $\rhoc=1$).""")
rep(r"""The screening rate $\sK$ is the fractional dilution of the dark-energy
\emph{pressure} per e-fold. It follows from the continuity equation and is
fixed by the equation of state alone,""",
    r"""The screening rate $\sK$ is the fractional dilution of the dark-energy
\emph{pressure} per e-fold at fixed $w_0$ (Paper~9: the term from the evolution
of $w(a)$ is not part of it). It follows from the continuity equation and is
fixed by the equation of state alone,""")
rep(r"""At the cosmological background $\varepsilon \equiv X_{\rm bg}^2/M^4 \approx 5.7\times10^{-4}$,
the full K(X) formula gives $c_s^2 \approx 0.967$ (see \S\ref{sec:consistency}), well above $1/3$.""",
    r"""At the cosmological background $\varepsilon \equiv X_{\rm bg}^2/M^4 \approx \val{eps_UV}$,
the full K(X) formula gives $c_s^2 \approx \val{p10_cs2_func}$ (see \S\ref{sec:consistency}), well above $1/3$.""")
rep(r"""    At the cosmological background ($u_{\rm bg} = X_{\rm bg}/M^4 \approx 1.55\times10^{-3}$,
    dash-dotted; equivalently $\varepsilon \equiv X_{\rm bg}^2/M^4 \approx 5.7\times10^{-4}$
    in $\rhoc$ units), the IR term dominates and the Hubble flow is in the linear
    kinetic regime.
    Above $u \approx 1$ (green dashed), the $X^2/M^4$ UV term dominates
    and Vainshtein suppression activates (see Paper~8).""",
    r"""    At the cosmological background ($u_{\rm bg} = X_{\rm bg}/M^4 \approx \val{p10_u_bg}$,
    dash-dotted; equivalently $\varepsilon \equiv X_{\rm bg}^2/M^4 \approx \val{eps_UV}$
    in $\rhoc$ units), the IR term dominates and the Hubble flow is in the linear
    kinetic regime.
    Above $u \approx 1$ (green dashed), the $X^2/M^4$ UV term dominates: the
    k-mouflage regime, for which Paper~8 quotes no screening radius.""")
rep(r"""          \;\approx\; 0.967\,,""", r"""          \;\approx\; \val{p10_cs2_func}\,,""")

# 7. sección de Hubble
rep(r"""\section{UV Completion of the Hubble Tension Resolution}""",
    r"""\section{UV Correction of the Hubble Cascade}""")
rep(r"""The local Hubble constant is
\begin{equation}
  H_0^{\rm glob}""",
    r"""The global rate returned from the SH0ES datum is
\begin{equation}
  H_0^{\rm glob}""")
rep(r"""$3(\phiG+\pi)^2 = \val{H0_ALG_d5}$ by $\val{p9_hglob_residuo}$, refining the IR residual
$\val{p9_sh0es_res_IR}$ ($\val{p9_sh0es_sig_IR}\sigma$) by a factor of $4\times10^4$ with the same input.""",
    r"""$3(\phiG+\pi)^2 = \val{H0_ALG_d5}$ by $\val{p9_hglob_residuo}$, against the IR residual
$\val{p9_sh0es_res_IR}$ ($\val{p9_sh0es_sig_IR}\sigma$) with the same input. What this does
and does not constrain follows.""")
rep(r"""$M^4 \in [0.2, \infty)\times 45\alpha^2\rhoc$ moves the output by at most
$0.57$ km/s/Mpc, so""",
    r"""$M^4 \in [0.2, \infty)\times 45\alpha^2\rhoc$ moves the output by at most
$\val{p10_mueve_M4}$ km/s/Mpc, so""")
rep(r"""$\KAL$ is compensated by a $2.01\%$ increase in $M^4$.""",
    r"""$\KAL$ is compensated by a $\val{p10_dM4_pct}\%$ increase in $M^4$
(\texttt{src/p10\_uv/barrido\_M4.py}).""")
rep(r"""  (the measured SH0ES rate is the input, Postulate~D). The UV completion with $M^4 = 45\alpha^2\rhoc$ sharpens the
  residual from $\val{p9_sh0es_sig_IR}\sigma$ (IR) to $4.3\times10^{-6}\sigma$ (UV),
  conditional on Postulate~C.1 (see §\ref{sec:theorem}).""",
    r"""  (the measured SH0ES rate is the input, Postulate~D). With $M^4 = 45\alpha^2\rhoc$ the
  residual goes from $\val{p9_sh0es_sig_IR}\sigma$ (IR) to $\val{p9_hglob_residuo}$~km/s/Mpc (UV),
  which is not quoted as a significance; conditional on Postulate~C.1 (see §\ref{sec:theorem}).""")
rep(r"""& \textbf{\val{H0_GLOBAL_d5}} & $4.3{\times}10^{-6}\sigma$ (cond.$^{a}$) \\""",
    r"""& \textbf{\val{H0_GLOBAL_d5}} & $\val{p9_hglob_residuo}$ km/s/Mpc (cond.$^{a}$) \\""")

# 8. test cruzado: las dos patas no pesan igual; criterio en la dirección vigente
rep(r"""These are \emph{independent observables} at vastly different epochs
($z \sim 10^{60}$ vs.\ $z \lesssim 0.15$) linked only through $\alpha$.
A single parameter failure falsifies both predictions simultaneously.

\paragraph{Quantitative falsification criteria.}
If LiteBIRD measures $r_{\rm obs}$, the implied $\alpha_{\rm obs}
= r_{\rm obs} N^2/12$, and one predicts
\begin{equation}
  H_0^{\rm local}(\alpha_{\rm obs})
  \;=\; \frac{H_0}{1 - \sK^{\rm full}(\alpha_{\rm obs})\,/\,(3\MIRA)}\,.
  \label{eq:Hpred}
\end{equation}
If this differs from SH0ES by more than $1\sigma$ (i.e., if
$|H_0^{\rm local}(\alpha_{\rm obs}) - 73.04| > 1.04$ km/s/Mpc),
the UV-completion proposal is falsified at $1\sigma$.""",
    r"""These are \emph{independent observables} at vastly different epochs, linked
only through $\alpha$ --- but they do not carry equal weight. The cascade does
not measure $M^4$ (§\ref{sec:hubble}): its output moves by one propagated
$\sigma$ only if $M^4$ falls to $\val{p10_f_1sig}$ of its nominal value, that is, if
$\alpha$ falls below $\val{p10_alfa_fac}$ of $\phiG^4/3$.

\paragraph{Quantitative falsification criteria.}
If LiteBIRD measures $r_{\rm obs}$, the implied $\alpha_{\rm obs}
= r_{\rm obs} N^2/12$, and the cascade returns
\begin{equation}
  H_0^{\rm glob}(\alpha_{\rm obs})
  \;=\; H_0^{\rm SH0ES}\left[1 - \sK^{\rm full}(\alpha_{\rm obs})\,/\,(3\MIRA)\right]\,.
  \label{eq:Hpred}
\end{equation}
If this departs from $3(\phiG+\pi)^2$ by more than the propagated $1\sigma$,
the UV proposal is disfavoured at $1\sigma$; with present SH0ES errors that
requires $r_{\rm obs} < \val{p10_r_umbral}$. Any other $r_{\rm obs} \neq \val{R_TENSOR_d5}$
falsifies $\alpha = \phiG^4/3$ directly through Eq.~\eqref{eq:r}, and
Conjecture~C.1 with it; the Hubble leg would then be silent.""")

# 9. primeros principios: la identidad 45α² = 5φ⁸ es exacta; que el corte la valga es la conjetura (OP-3)
rep(r"""The identity $M^4 = 45\alpha^2\rhoc$ has been \emph{found} numerically and
verified algebraically (Section~\ref{sec:alpha}).
Its \emph{derivation} from first principles---without using SH0ES as
input---remains under investigation.
We outline three candidate routes.""",
    r"""The identity $45\alpha^2 = 5\phiG^8$ is exact (Section~\ref{sec:alpha}); that the
cutoff equals $45\alpha^2\rhoc$ is Conjecture~C.1. A derivation of it that uses
neither the value of $M^4$ nor SH0ES is open (OP-3). We record three routes:
Routes~A and~B do not give it, and Route~C is a consistency reading, not a
derivation.""")
rep(r"""  \;\approx\; 418\,\rhoc\,.
  \label{eq:MA}
\end{equation}
Route~A gives $M^4_{\rm A} \approx 418\,\rhoc$, a factor $\approx 1.78$ above""",
    r"""  \;\approx\; \val{seis_alfa_KAL2_d0}\,\rhoc\,.
  \label{eq:MA}
\end{equation}
Route~A gives $M^4_{\rm A} \approx \val{seis_alfa_KAL2_d0}\,\rhoc$, a factor $\approx \val{KAL_KALeff2_d3}$ above""")
rep(r"""  \;=\; M^4_{\rm r2} \;\approx\; 8.20\,\rhoc\,.""",
    r"""  \;=\; M^4_{\rm r2} \;\approx\; \val{M4_r2_d2}\,\rhoc\,.""")
rep(r"""$H_0^{\rm glob}=H_0^{\rm SH0ES}(1-f_{\rm scr})=\val{H0_GLOBAL_d5}$~km\,s$^{-1}$\,Mpc$^{-1}$
(Postulate~D, Paper~1), which equals the pure number $3(\phiG+\pi)^2$ to
$4\times10^{-6}$, so""",
    r"""$H_0^{\rm glob}=H_0^{\rm SH0ES}(1-f_{\rm scr})=\val{H0_GLOBAL_d5}$~km\,s$^{-1}$\,Mpc$^{-1}$
(Postulate~D, Paper~1), which equals the pure number $3(\phiG+\pi)^2$ to
$\val{p9_hglob_residuo}$, so""")
rep(r"""Conjecture~C.1 is promoted below to a conditional theorem (Conditional
Theorem~C.1), under the UV-IR separability postulate; the UV-completion chain
then closes within the SSEE algebraic structure:""",
    r"""Below we show that Conjecture~C.1 is consistent with a UV-IR separability
postulate; it is not derived from it, because the argument uses the value of
$M^4$ (OP-3). Under the conjecture the chain closes within the SSEE algebraic
structure:""")
rep(r"""and obtains $M^4_{\rm A} = 6\alpha\,\KAL^2 = 2\phiG^4\,\KAL^2 \approx 418\,\rhoc$.""",
    r"""and obtains $M^4_{\rm A} = 6\alpha\,\KAL^2 = 2\phiG^4\,\KAL^2 \approx \val{seis_alfa_KAL2_d0}\,\rhoc$.""")
rep(r"""$(10\phiG^4)/(\phiG+3\pi)^2 \approx 0.562$ --- precisely the inverse of""",
    r"""$(10\phiG^4)/(\phiG+3\pi)^2 \approx \val{KALeff2_sobre_KAL2_d3}$ --- precisely the inverse of""")
rep(r"""\paragraph{UV-IR separability and the conditional derivation.}

We now show that Conjecture~C.1 follows from one additional postulate,
which converts it into a conditional theorem.""",
    r"""\paragraph{UV-IR separability: a consistency reading.}

We now show what Conjecture~C.1 implies for the kinetic normalisation, and
that the result is compatible with one additional postulate.""")
rep(r"""$M^4_{\rm A} = 6\alpha\,\KAL^2 \approx 418\,\rhoc$
--- too large""",
    r"""$M^4_{\rm A} = 6\alpha\,\KAL^2 \approx \val{seis_alfa_KAL2_d0}\,\rhoc$
--- too large""")
rep(r"""Under this postulate, $\KALeff^2$ must be a polynomial in $\phiG$ with rational
coefficients.
The constraint Eq.~\eqref{eq:M4_KALeff} then reads""",
    r"""Under this postulate, $\KALeff^2$ must be a polynomial in $\phiG$ with rational
coefficients --- but the postulate does not say which: every rational multiple
of a power of $\phiG$ qualifies.
The constraint Eq.~\eqref{eq:M4_KALeff} reads""")
rep(r"""The unique monomial in $\phiG$ satisfying both Eq.~\eqref{eq:KALeff_constraint}
and the empirically established $M^4 = 5\phiG^8\,\rhoc$ is""",
    r"""Given the conjectured $M^4 = 5\phiG^8\,\rhoc$ (the cascade does not measure it,
§\ref{sec:hubble}), Eq.~\eqref{eq:KALeff_constraint} is solved by""")
rep(r"""Substituting back into Eq.~\eqref{eq:M4_KALeff}:""",
    r"""Substituting back into Eq.~\eqref{eq:M4_KALeff} returns the input, as it must:""")
rep(r"""This is precisely Conjecture~C.1.""",
    r"""This is Conjecture~C.1 again: the argument is a consistency check, not a
derivation, because $M^4$ was used to fix $\KALeff$ (OP-3).""")
rep(r"""the factor by which Route~A overshoots ($\val{seis_alfa_KAL2_d2}\,\rhoc$ against
$\val{_M4_UV_d2}\,\rhoc$). The discrepancy is thus $33\%$ in the normalisation and
$78\%$ in the cutoff:""",
    r"""the factor by which Route~A overshoots ($\val{seis_alfa_KAL2_d2}\,\rhoc$ against
$\val{_M4_UV_d2}\,\rhoc$). The discrepancy is thus $\val{KAL_KALeff_pct}\%$ in the normalisation and
$\val{KAL_KALeff2_pct}\%$ in the cutoff:""")
rep(r"""\textbf{Conditional Theorem~C.1.}
\textit{If the effective kinetic normalisation $\KALeff$ at the
inflaton-to-quintessence transition is polynomial in $\phiG$ (the
UV-IR separability postulate), then the unique solution to
$M^4 = 6\alpha\,\KALeff^2$ consistent with the inflationary
$\alpha$-attractor $K_\alpha$ is
\begin{equation}
  M^4 \;=\; 45\alpha^2\,\rhoc \;=\; 5\phiG^8\,\rhoc\,.
  \label{eq:CT1}
\end{equation}
The UV ladder closes:""",
    r"""\textbf{Consistency statement~C.1.}
\textit{If $M^4 = 45\alpha^2\rhoc$ (Conjecture~C.1), the effective kinetic
normalisation at the inflaton-to-quintessence transition is
$\KALeff = \phiG^2\sqrt{5/2}$, a polynomial in $\phiG$ alone, as the UV-IR
separability postulate requires, and Route~A ($\KALeff=\KAL$) is excluded:
\begin{equation}
  M^4 \;=\; 6\alpha\,\KALeff^2 \;=\; 45\alpha^2\,\rhoc \;=\; 5\phiG^8\,\rhoc\,.
  \label{eq:CT1}
\end{equation}
Under the conjecture the UV ladder closes:""")
rep(r"""The unconditional proof requires an explicit derivation of $\KALeff$
from the $P(X,\phi)$ Lagrangian at the inflationary transition ---
specifically, showing that the field-space Jacobian $\partial\phi/\partial\chi|_{\rm transition}$
evaluates to $\phiG^2\sqrt{5/2}$ rather than $\KAL = (\phiG+3\pi)/2$.
This is deferred to Paper~B of the SSEE series.""",
    r"""A derivation requires the number $5/2$ from a source of its own ---
equivalently $\KALeff$ from the $P(X,\phi)$ Lagrangian at the inflationary
transition, the field-space Jacobian $\partial\phi/\partial\chi|_{\rm transition}$
evaluating to $\phiG^2\sqrt{5/2}$ rather than $\KAL = (\phiG+3\pi)/2$ --- without
using the value of $M^4$ or SH0ES. It is open, with a pre-registered closing
criterion (OP-3).""")

# 10. s_K^full no se observa vía w0 (w0 queda igual por construcción): sin el «3.4σ_syst»
rep(r"""The UV-corrected screening rate $\sK^{\rm full} = \val{S_K_FULL_d5}$ is measurable
through the equation of state, since $\sK^{\rm IR} = -3w_0(1+w_0)$.
Current constraints from DESI DR2 BAO \citep{AbdulKarim2025} set the background
context; forthcoming Euclid and DESI~Y5 data will probe $w_0$, and hence $\sK$, at the
$\sim1\%$ level, distinguishing the UV-completed theory from the IR limit by
$3.4\,\sigma_{\rm syst}$.""",
    r"""The UV-corrected screening rate $\sK^{\rm full} = \val{S_K_FULL_d5}$ is \emph{not}
observable through the equation of state: the background matching below holds
$w_0$ fixed, and what a measurement of $w_0$ gives is $\sK^{\rm IR} = -3w_0(1+w_0)$.
Forthcoming Euclid and DESI~Y5 data \citep{AbdulKarim2025} will sharpen $w_0$,
and hence $\sK^{\rm IR}$, but not the UV term, which enters only through $\fsc$,
i.e.\ through the cascade, and the cascade does not measure $M^4$
(§\ref{sec:hubble}). No present observable separates the UV-extended theory
from its IR limit.""")
rep(r"""  \;\approx\; +2.4\times10^{-3}\,.
\end{equation}
Either way, $|\Delta w_0| \lesssim 0.002$ lies well below the projected""",
    r"""  \;\approx\; +\val{p10_dw0}\,.
\end{equation}
Either way, $|\Delta w_0| \lesssim \val{p10_dw0}$ lies well below the projected""")
rep(r"""IR limit, and the discriminating observable remains $\sK$.""",
    r"""IR limit.""")

# 11. tabla de consistencia
rep(r"""Paper 7 & Ghost condensate: $w_0$, $c_s^2$ from the Lagrangian &""",
    r"""Paper 7 & Ghost condensate: $w_0$, $c_s^2$ today from the Lagrangian (the field rolls) &""")
rep(r"""Paper 8 & $\MIRA = \AURA/2$; strong-field regime &""",
    r"""Paper 8 & Lensing with $\mu-1=0$; strong-field regime &""")
rep(r"""UV closes to $\val{H0_GLOBAL_d5}$ ($4.3{\times}10^{-6}\sigma$; conditional$^{a}$) \\""",
    r"""UV closes to $\val{H0_GLOBAL_d5}$ (residual $\val{p9_hglob_residuo}$; conditional$^{a}$) \\""")

# 12. conclusiones
rep(r"""We have shown that the SSEE dark-energy Lagrangian $K(X) = X/\KAL + X^2/M^4$
admits a unique algebraically consistent UV cutoff""",
    r"""We have proposed (Conjecture~C.1) that the screening functional
$K(X) = X/\KAL + X^2/M^4$ --- not the dark-energy action of Paper~7 --- has the
UV cutoff""")
rep(r"""Postulate~C.1, reproducing $3(\phiG+\pi)^2$ to the seventh digit.""",
    r"""Postulate~C.1, reproducing $3(\phiG+\pi)^2$ to the seventh digit, far inside the
propagated $\pm\val{p9_hglob_sigma}$.""")
rep(r"""        ($\varepsilon \approx 5.7\times10^{-4}$) and shifts""",
    r"""        ($\varepsilon \approx \val{eps_UV}$) and shifts""")
rep(r"""  \item A first-principles derivation of $M^4 = 45\alpha^2\rhoc$ remains
        under investigation (Section~\ref{sec:firstprinciples}), with Route~C
        (full $P(X,\phi)$ Lagrangian) identified as the most promising path.""",
    r"""  \item A derivation of $M^4 = 45\alpha^2\rhoc$ that uses neither its value
        nor SH0ES remains open (Section~\ref{sec:firstprinciples}; OP-3):
        Routes~A and~B do not give it, and the separability reading of
        Route~C is a consistency check, not a derivation.""")

# 13. bibliografía: títulos reales; BICEP/Keck 2021
rep(r"""\emph{SSEE: Algebraic Framework, EFT, and $\alpha$-Attractor Inflation},""",
    r"""\emph{A Minimal-Parameter Framework for Cosmological Dynamics and Galaxy
Cluster Mass Discrepancies via Structural Self-Energy Expansion (SSEE)},""")
rep(r"""\emph{Strong-Gravity Regime: Disformal Geodesics and $\MIRA$ Lensing},""",
    r"""\emph{SSEE in the Strong-Gravity Regime: GR Lensing in the Canonical Limit,
a Disformal Contrast, and Solar-System Compliance},""")
rep(r"""\emph{Hubble Tension via Algebraic Screening Fraction:
$\fsc = \sK/(3\MIRA) = (\pi-\phiG)/(\phiG+\pi)^2$},""",
    r"""\emph{SSEE and the Hubble Tension: An Algebraic Local Screening Fraction},""")
rep(r"""\bibitem{Akrami2020}""",
    r"""\bibitem{BK2021}
P.~A.~R.~Ade et al.\ (BICEP/Keck Collaboration),
\emph{Improved Constraints on Primordial Gravitational Waves using Planck,
WMAP, and BICEP/Keck Observations through the 2018 Observing Season},
Phys.\ Rev.\ Lett.\ \textbf{127}, 151301 (2021) [arXiv:2110.00483].

\bibitem{Akrami2020}""")

open(P, "w").write(s)
print("P10: quinta lectura aplicada")
