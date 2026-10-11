"""Quinta lectura P1, apéndice EFT (2026-10-11). Ver P1.md, hallazgos E1–E8."""
import pathlib, sys
P = pathlib.Path(__file__).resolve().parents[2] / 'manuscript/SSEE_EFT_section.tex'
s = P.read_text()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f"«{old[:70]}» aparece {c} veces (esperaba {n})")
    s = s.replace(old, new)

# E1. normalización de la viscosidad: P5 (OP-22, 2026-09-06) la fija a la entalpía; la de ρ_crit queda retirada
rep(r"""and the viscosity coupling $\mathrm{KAL}_0$ on superhorizon scales.""",
    r"""and the role of the retention constant $\mathrm{KAL}_0$ on superhorizon scales.""")
rep(r"""\subsubsection{Constant-coupling regime ($w_0$)}

The retention constant $\mathrm{KAL}_{0} \equiv \beta + \pi \approx 5.521$
governs the dissipative sector.  Following the Eckart first-order formalism,
the bulk viscosity coefficient is coupled to the instantaneous expansion rate:
%
\begin{equation}
  \zeta_0 = \frac{\mathrm{KAL}_{0}}{8\pi G}\,H.
  \label{eq:zeta}
\end{equation}
%
This delivers a \emph{constant-coupling} viscous pressure
$\Pi_0 = -3\zeta_0 H = -3\,\mathrm{KAL}_{0}H^{2}/8\pi G$,
which governs the background acceleration (Eq.~\ref{eq:Friedmann_a}) and fixes
the present-day effective equation of state $w_0 = -T_r/M_v$ algebraically
(Section~\ref{sec:eft:PX}).""",
r"""\subsubsection{Normalisation of the viscosity}

The retention constant $\mathrm{KAL}_{0} \equiv \beta + \pi \approx \val{KAL0_d3}$
governs the dissipative sector. Its normalisation is fixed in Paper~5: the bulk
viscosity is measured against the enthalpy $\rho_{\mathrm{DE}}+p_{\mathrm{DE}}$,
so that the viscous pressure vanishes identically for $w=-1$ --- a
cosmological constant has no fluid degrees of freedom. The present-day
equation of state $w_0=-T_r/M_v$ is fixed by the k-essence sector
(Section~\ref{sec:eft:PX}), not by the viscosity.
\emph{(Withdrawn 2026-10-11: earlier versions normalised the coefficient to the
critical density, $\zeta_0=\mathrm{KAL}_0H/8\pi G$, a ``constant-coupling''
pressure $\Pi_0=-3\mathrm{KAL}_0H^2/8\pi G$ said to fix $w_0$. That pressure is
of order $\mathrm{KAL}_0\,\rho_{\rm crit}$ today and would drive $w$ far below
$-1$; it contradicts both $w_0=-T_r/M_v$ and the condition $\zeta\to0$ at $a=1$
below, and it is the normalisation Paper~5 retires.)}""")
rep(r"""\paragraph{Physical motivation for $\zeta \propto H$.}
Bulk viscosity proportional to the Hubble rate arises naturally in
kinetic theory when the dominant relaxation time is set by the expansion
itself \citep{Weinberg1971, Brevik2005}.  Within SSEE the coupling constant
is not fitted but predicted geometrically as
$\mathrm{KAL}_{0} = (\pi+\varphi)/2 + \pi$.""",
r"""\paragraph{Physical motivation.}
Bulk viscosity tied to the expansion rate arises naturally in kinetic theory
when the dominant relaxation time is set by the expansion itself
\citep{Weinberg1971, Brevik2005}.  Within SSEE the coupling constant is not
fitted but fixed geometrically as $\mathrm{KAL}_{0} = (\pi+\varphi)/2 + \pi$.""")
rep(r"""$\Gamma$ the closure $w_a = -3\Gamma$ holds to $0.00\times10^{0}$.""",
    r"""$\Gamma$ the closure $w_a = -3\Gamma$ holds identically.""")

# E2. límite temprano con el Γ viejo (=w_a) y Π total con un término de fondo retirado y un 3H de dimensión errónea
rep(r"""    \zeta \to -\frac{2\varphi+\pi}{2(\varphi+\pi)}\,
              \frac{\rho_{\mathrm{DE,0}}\,a^{-3(1+w_0+w_a)}\,e^{-3w_a}}{H(a)},""",
    r"""    \zeta \to \frac{2\varphi+\pi}{6(\varphi+\pi)}\,
              \frac{\rho_{\mathrm{DE,0}}\,a^{-3(1+w_0+w_a)}\,e^{-3w_a}}{H(a)},""")
rep(r"""The viscous pressure is therefore
%
\begin{equation}
  \Pi(a)
    = \underbrace{-\frac{3\,\mathrm{KAL}_{0}\,H^{2}}{8\pi G}}_{\text{background}}
      \underbrace{-\;3H\,w_a\,(1-a)\,\rho_{\mathrm{DE}}(a)}_{\text{CPL evolution}},
  \label{eq:Pi_total}
\end{equation}
%
where the first term is the constant-coupling Eckart pressure that sustains
$\ddot a > 0$ and the second term generates the running $w(a)$ observed by
DESI~DR2 \citep{AbdulKarim2025}.""",
r"""The viscous pressure is therefore the single term of Eq.~(\ref{eq:Pi_evolving}),
%
\begin{equation}
  \Pi(a) = w_a\,(1-a)\,\rho_{\mathrm{DE}}(a),
  \label{eq:Pi_total}
\end{equation}
%
which generates the running $w(a)$ observed by DESI~DR2 \citep{AbdulKarim2025}
and vanishes today. \emph{(Corrected 2026-10-11: this equation carried a
``background'' term $-3\mathrm{KAL}_0H^2/8\pi G$, withdrawn above, and wrote the
CPL term with an extra factor $3H$, which is not a pressure.)}""")

# E3. Friedmann II/III con el término 9 KAL0 H² del acople retirado
rep(r"""\paragraph{II. Acceleration equation:}
\begin{equation}
  \frac{\ddot{a}}{a}
    = -\frac{4\pi G}{3}
      \!\left[\rho_{m} + 2\rho_{r}
        + \rho_{\mathrm{SSEE}}\!\left(1 + 3w_{0}\right)
        - \frac{9\,\mathrm{KAL}_{0}\,H^{2}}{8\pi G}
      \right].
  \label{eq:Friedmann_a}
\end{equation}

\paragraph{III. Conservation equation with dissipative source:}
\begin{equation}
  \dot{\rho}_{\mathrm{SSEE}}
    + 3H\,\rho_{\mathrm{SSEE}}\!\left(1 + w_{0}\right)
    = \frac{9\,\mathrm{KAL}_{0}\,H^{3}}{8\pi G}.
  \label{eq:continuity}
\end{equation}
""", r"""\paragraph{II. Acceleration equation:}
\begin{equation}
  \frac{\ddot{a}}{a}
    = -\frac{4\pi G}{3}
      \!\left[\rho_{m} + 2\rho_{r}
        + \rho_{\mathrm{SSEE}}\!\left(1 + 3w(a)\right)
      \right],
  \label{eq:Friedmann_a}
\end{equation}
with $p_{\mathrm{SSEE}} = w(a)\,\rho_{\mathrm{SSEE}} = w_0\rho_{\mathrm{SSEE}}+\Pi$.

\paragraph{III. Conservation equation with dissipative source:}
\begin{equation}
  \dot{\rho}_{\mathrm{SSEE}}
    + 3H\,\rho_{\mathrm{SSEE}}\!\left(1 + w_{0}\right)
    = -3H\,\Pi,
  \label{eq:continuity}
\end{equation}
which with Eq.~(\ref{eq:Pi_total}) is the CPL equation~(\ref{eq:cont_CPL}).
""")
rep(r"""\noindent\textbf{Derivation of the coefficient 9.}\par\smallskip
\noindent From Eq.~(\ref{eq:zeta}), the viscous pressure is
$\Pi = -3\mathrm{KAL}_{0}H^{2}/8\pi G$.
In the Raychaudhuri equation the effective pressure of the SSEE sector enters as
$p_{\mathrm{eff}} = w_{0}\rho_{\mathrm{SSEE}} + \Pi$, so the acceleration term becomes
%
\begin{align}
  -\frac{4\pi G}{3}\bigl(\rho_{\mathrm{SSEE}} + 3p_{\mathrm{eff}}\bigr)
  &= -\frac{4\pi G}{3}
     \!\left[\rho_{\mathrm{SSEE}}(1+3w_{0}) + 3\Pi\right] \notag\\
  &= -\frac{4\pi G}{3}
     \!\left[\rho_{\mathrm{SSEE}}(1+3w_{0})
             - \frac{9\,\mathrm{KAL}_{0}\,H^{2}}{8\pi G}\right],
  \label{eq:deriv_coeff9}
\end{align}
which is exactly Eq.~(\ref{eq:Friedmann_a}).  The factor 9 arises from
$3 \times |\Pi|/(H^{2}) = 3 \times 3\mathrm{KAL}_{0}/8\pi G$; a factor
of 3 rather than 9 would correspond to including $\Pi$ only once instead
of as the trace of the viscous stress.

Similarly, the conservation law $\nabla_{\!\mu}T^{\mu\nu}=0$ for the effective
fluid $(w_{0},\Pi)$ gives
$\dot{\rho} + 3H(\rho + w_{0}\rho + \Pi) = 0$, hence
$\dot{\rho} + 3H\rho(1+w_{0}) = 9\mathrm{KAL}_{0}H^{3}/8\pi G$,
confirming that Eq.~(\ref{eq:Friedmann_a}) and Eq.~(\ref{eq:continuity})
are mutually consistent.""",
r"""\noindent Both follow from $\nabla_{\!\mu}T^{\mu\nu}=0$ and the Raychaudhuri
equation for the effective fluid $(w_0,\Pi)$:
$\dot{\rho} + 3H(\rho + w_{0}\rho + \Pi) = 0$. \emph{(Withdrawn 2026-10-11:
earlier versions carried a source $9\mathrm{KAL}_0H^2/8\pi G$ in
Eqs.~(\ref{eq:Friedmann_a})--(\ref{eq:continuity}) and a paragraph deriving
its ``coefficient~9''; it came from the critical-density normalisation
withdrawn above.)}""")

# E4. transporte IS: misma normalización; τ_Π con la saturación, no con Ω_DE
rep(r"""\begin{equation}
  \tau_{\Pi} H_{0}\,\tilde{h}(a)\,
    \frac{\mathrm{d}\tilde{\Pi}}{\mathrm{d}\ln a}
  + \tilde{\Pi}
  = -\,\mathrm{KAL}_{0}\,\tilde{h}^{2}(a),
  \label{eq:IS_transport}
\end{equation}
%
where $\tilde{h} = H/H_{0}$, $\tilde{\Pi} = \Pi\,8\pi G/H_{0}^{2}$, and
all densities are normalised to $\rho_{\mathrm{crit},0}$.  In the
limit $\tau_{\Pi} \to 0$, Eq.~(\ref{eq:IS_transport}) reduces to the
Eckart result $\tilde{\Pi} = -\mathrm{KAL}_{0}\tilde{h}^{2}$.""",
r"""\begin{equation}
  \tau_{\Pi}\,\dot{\Pi} + \Pi = -3\zeta H,
  \label{eq:IS_transport}
\end{equation}
%
with $\zeta$ normalised to the enthalpy as in Paper~5, where the equation is
solved. In the limit $\tau_{\Pi} \to 0$ it reduces to the Eckart result
$\Pi = -3\zeta H$.""")
rep(r"""    \;=\; \frac{\mathrm{KAL}_{0}}{3\,\Omega_{\mathrm{DE}}}
    \;\approx\; 2.191,""", r"""    \;=\; \frac{\mathrm{KAL}_{0}}{3\,T_r/M_v}
    \;\approx\; \val{TAU_PI_H0_d3},""")

# E5. γ_bg se calculó sobre el fondo con la normalización retirada
rep(r"""we solve the system numerically (\texttt{ssee\_is\_growth.py}) with
the IS background $\tilde{h}^{2}(a) = \Omega_{m}\,a^{-3}+\rho_{\mathrm{DE}}(a)$,""",
r"""the earlier background integration (\texttt{ssee\_is\_growth.py}, which still
sources $\Pi$ with the critical-density normalisation withdrawn above) used
$\tilde{h}^{2}(a) = \Omega_{m}\,a^{-3}+\rho_{\mathrm{DE}}(a)$,""")

# E6. regímenes: el término 9 KAL0 H³ retirado, «sin materia oscura», y la partícula φ-DM retirada
rep(r"""At low redshift $H \approx H_{0}$, so the viscous source
$\propto \mathrm{KAL}_{0}H^{3}/8\pi G$ is small compared to
$\rho_{\mathrm{SSEE}}$.  The acceleration equation is dominated by
$\rho_{\mathrm{SSEE}}(1+3w_{0}) < 0$
(since $w_{0} \approx -0.840 < -1/3$), driving $\ddot{a} > 0$
without dark matter.  This regime is the one tested against DESI~DR2
in Paper~2, where the algebraic prediction $(w_{0},w_{a})$ matches
the data at $0.24\sigma$ (Pantheon+; $0.2$--$1.8\sigma$ across SN compilations).""",
r"""At low redshift the viscous pressure $\Pi=w_a(1-a)\rho_{\mathrm{SSEE}}$ is
small and vanishes today. The acceleration equation is dominated by
$\rho_{\mathrm{SSEE}}(1+3w_{0}) < 0$
(since $w_{0} \approx \val{W0_d3} < -1/3$), driving $\ddot a > 0$.
This regime is the one tested against DESI~DR2
in Paper~2, where the algebraic prediction $(w_{0},w_{a})$ matches
the data at $\val{p2_w0wa_ssee_ec26}\sigma$ (Pantheon+; $\val{p2_w0wa_ssee_ec28_d1}$--$\val{p2_w0wa_ssee_ec27_d1}\sigma$ across the other SN compilations).""")
rep(r"""At recombination $H \gg H_{0}$, the geometric retention term
$9\,\mathrm{KAL}_{0}H^{3}/8\pi G$ acts as a dissipative source in
Eq.~(\ref{eq:continuity}), injecting energy into the dark-energy fluid
and modifying its effective equation of state.  The matter density that""",
r"""At recombination the dark-energy fraction is negligible
($\rho_{\mathrm{DE}}/\rho_m\propto a^{-3(w_0+w_a)}$ with $w_0+w_a=\val{w0_mas_wa}$),
and so is its viscous pressure.  The matter density that""")
rep(r"""$\omega_\nu$, with $\phi$-DM already non-relativistic and contributing to the
matter budget at recombination. The earlier""", r"""$\omega_\nu$. The earlier""")

# E7. α-attractor: α es el postulado (Postulado I), r su consecuencia; «dos axiomas independientes» era circular
rep(r"""The SSEE axioms pre-commit two \emph{independent} inflationary observables:
$n_s = 1-\varphi^{-7}$ (Axiom~1, spectral tilt) and $r = \varphi^{-10}$
(Axiom~2, tensor-to-scalar ratio).
Neither is derived from the $\alpha$-attractor framework;
they are algebraic predictions from $\{\varphi,\pi\}$ that can be tested
for \emph{mutual consistency} within that framework.

From Axiom~1 alone, the standard slow-roll relation $n_s = 1 - 2/N$ gives""",
r"""Postulate~I (Paper~1, \S\ref{sec:scope}) takes the $\alpha$-attractor class with
$\alpha=\varphi^4/3$ and $N_*=2\varphi^n$; the inflation window selects $n=7$.
Read the other way, the algebraic tilt $n_s = 1-\varphi^{-7}$ and the standard
slow-roll relation $n_s = 1 - 2/N$ give""")
rep(r"""  N = \frac{2}{\varphi^{-7}} = 2\varphi^{7} \approx 58.07,""", r"""  N = \frac{2}{\varphi^{-7}} = 2\varphi^{7} \approx \val{dos_phi7_d2},""")
rep(r"""\emph{Independently}, inserting $N = 2\varphi^{7}$ and Axiom~2 ($r = \varphi^{-10}$)
into the second attractor relation $r = 12\alpha/N^2$:
\begin{equation}
  \alpha = \frac{r\,N^{2}}{12}
         = \frac{\varphi^{-10}\cdot 4\varphi^{14}}{12}
         = \frac{4\varphi^{4}}{12}
         = \frac{\varphi^{4}}{3}.
  \label{eq:alpha_ssee}
\end{equation}
This is a \emph{non-trivial internal consistency}: two independently pre-committed
predictions simultaneously select a unique $\alpha$-attractor geometry.
The identification is algebraically exact (verified to machine precision;
see \texttt{ssee\_inflation\_connection.py}).""",
r"""With the postulated $\alpha$, the second attractor relation $r = 12\alpha/N^2$ then
fixes the tensor ratio:
\begin{equation}
  r = \frac{12\alpha}{N^{2}}
    = \frac{12\,\varphi^{4}/3}{4\varphi^{14}}
    = \varphi^{-10}.
  \label{eq:alpha_ssee}
\end{equation}
$r=\varphi^{-10}$ is therefore a consequence of the postulated $\alpha$, not an
independent check of it: the falsifiable content is that LiteBIRD measures
$r=\val{R_TENSOR_d6}$. \emph{(Corrected 2026-10-11: earlier versions presented
$n_s$ and $r$ as two independently pre-committed axioms that ``select'' $\alpha$;
that reverses Postulate~I and makes the agreement circular.)}""")
rep(r"""SSEE is therefore \emph{not} Starobinsky inflation; it is a generalised
$\alpha$-attractor that reduces to Starobinsky only in the limit
$\varphi \to 1$ (i.e.\ $\alpha \to 1$, the fixed point of the golden-ratio
recursion $x = 1 + 1/x$).""", r"""SSEE is therefore \emph{not} Starobinsky inflation; it is the
$\alpha$-attractor with $\alpha=\varphi^4/3\approx2.28$.""")

# E8. resumen y tabla
rep(r"""The action~(\ref{eq:eft_action}) with kinetic exponent~(\ref{eq:n_ssee})
and viscosity~(\ref{eq:zeta_ssee}) constitutes a self-consistent,
zero-free-parameter description of the SSEE background evolution.
Every constant ($n$, $\mathrm{KAL}_{0}$, $w_0$, $w_a$, $\Omega_{\mathrm{DE}}$) is
derived from $\varphi$ and $\pi$ alone;""", r"""The action~(\ref{eq:eft_action}) with kinetic exponent~(\ref{eq:n_ssee})
and viscosity~(\ref{eq:zeta_ssee}) is a zero-free-parameter description of the
SSEE background evolution, motivational at the perturbation level (its
power-law sector is gradient-unstable; see below).
Every constant ($n$, $\mathrm{KAL}_{0}$, $w_0$, $w_a$) is
derived from $\varphi$ and $\pi$ alone;""")
rep(r"""        that reduces to $P(X) = \mathcal{A}X^n$ at late times""", r"""        that reduces to the two-term action $K(X)=c_1X+c_2X^2$ of Paper~7 at late times""")
rep(r"""Viscosity coupling $\zeta$ & \checkmark Algebraic & $\zeta=\mathrm{KAL}_{0}H/8\pi G$ \\
Friedmann eqs.\ I--III & \checkmark Consistent & Factor 9 verified in \S\ref{sec:eft:friedmann} \\""",
r"""Viscosity normalisation & \checkmark Fixed & To the enthalpy (Paper~5); the critical-density form is withdrawn \\
Friedmann eqs.\ I--III & \checkmark Consistent & CPL conservation, \S\ref{sec:eft:friedmann} \\""")
rep(r"""$\tau_\Pi H_0 = \mathrm{KAL}_0/(3|w_0|) \approx 2.191$ \\""", r"""$\tau_\Pi H_0 = \mathrm{KAL}_0/(3|w_0|) \approx \val{TAU_PI_H0_d3}$ \\""")
P.write_text(s); print("EFT ok")
