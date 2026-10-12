#!/usr/bin/env python3
"""P9, quinta lectura (2026-10-12): lo que la lectura encontró, con su porqué en notes/lectura_quinta/P9.md."""
import sys

P = "manuscript/SSEE_Paper9_HubbleTension.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


# 1. «cero parámetros libres» para todo el modelo: tiene {A_s, tau}
rep(r"""constants $\phiG$ (golden ratio) and $\pi$ determine all parameters with zero
free parameters.
We show that the equation of state of the SSEE dark-energy sector (Paper~7),""",
    r"""constants $\phiG$ (golden ratio) and $\pi$ fix the background, leaving
$\{A_s,\tau\}$ as the only free parameters.
We show that the equation of state of the SSEE dark-energy sector (Paper~1),""")

# 2. el mecanismo es un postulado abierto: no afirmar que «opera a través de la energía cinética»
rep(r"""The correction operates at late times ($z < 0.15$) through the scalar kinetic
energy contribution to the local expansion rate, and does not modify the
sound horizon $r_d$, the CMB peak positions, or the growth factor $\sigma_8$
derived in Papers~3 and~5.
The UV completion of Paper~10 sharpens the residual to
$\val{p9_hglob_residuo}$~km/s/Mpc ($H_0^{\rm glob,UV} = \val{H0_GLOBAL_d5}$), the small-scale
refinement of the same cascade.""",
    r"""The correction acts on locally measured rates only ($z < 0.15$) and does not
modify the sound horizon $r_d$, the CMB peak positions, or the growth factor
$\sigma_8$ derived in Papers~3 and~5.
With the complete screening fraction of Paper~10 the same cascade gives the
single model value $H_0^{\rm glob} = \val{H0_GLOBAL_d5}$, a residual of
$\val{p9_hglob_residuo}$~km/s/Mpc against the pure number, far inside the
propagated $\pm\val{p9_hglob_sigma}$.""")

# 3. 1.1σ a mano
rep(r"""which, read in km/s/Mpc, lies $1.1\sigma$ from Planck \citep{Paper2}.""",
    r"""which, read in km/s/Mpc, lies $\val{h0alg_planck_sig}\sigma$ from Planck \citep{Paper2}.""")
rep(r"""In this paper we show that the same algebraic structure that produces
$\Hzero^{\rm alg}$ also produces a local kinematic correction""",
    r"""In this paper we show that the same algebraic structure that gives the pure
number~\eqref{eq:H0alg} also gives a local correction""")
rep(r"""  \item From Paper~7 \citep{Paper7}: the pressure-dilution rate
        $\sK = -3w_0(1+w_0) = 3\,\sDE(1+w_0)$, a function of the equation
        of state alone.""",
    r"""  \item From the equation of state of Paper~1 \citep{Paper1}: the
        pressure-dilution rate $\sK = -3w_0(1+w_0) = 3\,\sDE(1+w_0)$, a function
        of $w_0$ alone (the field of Paper~7 reproduces $w_0$ today).""")

# 4. s_K: el signo de la definición estaba cambiado y el paso 1 lo tapaba con un (−1);
#    y vale para la parte de w constante: el término w_a no entra
rep(r"""\begin{equation}
  \sK \;\equiv\; -\frac{1}{\rho_\phi}\frac{dp_\phi}{dN}
      \;=\; -3w_0(1+w_0)\,, \qquad N = \ln a,
  \label{eq:sK_def}
\end{equation}
which carries only the equation of state: no factor of $H$, no density, and
no kinetic function.""",
    r"""\begin{equation}
  \sK \;\equiv\; -\frac{1}{\rho_\phi}\frac{d|p_\phi|}{dN}\bigg|_{w=w_0}
      \;=\; -3w_0(1+w_0)\,, \qquad N = \ln a,
  \label{eq:sK_def}
\end{equation}
evaluated with the present $w_0$ held fixed: the term from the evolution of
$w(a)$, $-w_a$ today, is not part of $\sK$, which is a number of the algebra
rather than the full rate of change of the pressure. It carries only the
equation of state: no factor of $H$, no density, and no kinetic function.""")
rep(r"""With $p_\phi = w_0\rho_\phi$ and $w_0$ constant, the continuity equation
$\rho_\phi' = -3(1+w_0)\rho_\phi$ gives
\begin{equation}
  \frac{1}{\rho_\phi}\frac{dp_\phi}{dN}
    = w_0\,\frac{\rho_\phi'}{\rho_\phi}
    = -3w_0(1+w_0)\cdot(-1)\,,
  \qquad\text{hence}\qquad
  \sK = -3w_0(1+w_0)\,.
  \label{eq:sK_exact}
\end{equation}""",
    r"""With $p_\phi = w_0\rho_\phi$ at fixed $w_0<0$, $|p_\phi|=-w_0\rho_\phi$ and the
continuity equation $\rho_\phi' = -3(1+w_0)\rho_\phi$ give
\begin{equation}
  -\frac{1}{\rho_\phi}\frac{d|p_\phi|}{dN}
    = w_0\,\frac{\rho_\phi'}{\rho_\phi}
    = -3w_0(1+w_0)\,,
  \qquad\text{hence}\qquad
  \sK = -3w_0(1+w_0)\,.
  \label{eq:sK_exact}
\end{equation}""")

# 5. 0.31 a mano (cuatro sitios) y 68.44 a mano
rep(r"""$O(\fsc^2)\approx0.31$~km/s/Mpc, below the present SH0ES uncertainty, so the""",
    r"""$O(\fsc^2)\approx\val{p9_add_dif}$~km/s/Mpc, below the present SH0ES uncertainty, so the""")
rep(r"""$O(\fsc^2)\approx0.31$\,km/s/Mpc. Since $\fsc$ is exactly constant""",
    r"""$O(\fsc^2)\approx\val{p9_add_dif}$\,km/s/Mpc. Since $\fsc$ is exactly constant""")
rep(r"""$\fsc^2 H_0^{\rm glob}\approx0.31$\,km/s/Mpc, below the present SH0ES""",
    r"""$\fsc^2 H_0^{\rm glob}\approx\val{p9_add_dif}$\,km/s/Mpc, below the present SH0ES""")
rep(r"""error $\fsc^2\,H_0^{\rm glob} \approx 0.31$\,km/s/Mpc.""",
    r"""error $\fsc^2\,H_0^{\rm glob} \approx \val{p9_add_dif}$\,km/s/Mpc.""")
rep(r"""& $H_0^{\rm SH0ES}/(1+\fsc^{\rm IR})$ & $68.44$ km/s/Mpc & --- \\""",
    r"""& $H_0^{\rm SH0ES}/(1+\fsc^{\rm IR})$ & $\val{p9_add_H}$ km/s/Mpc & --- \\""")

# 6. Ω_DE(z*) ~ 1e-9 es el de ΛCDM; con CPL sale ~3e-13 (cota sin radiación)
rep(r"""        at $z_* \approx 1100$, where the SSEE dark energy density is
        $\Omde(z_*) \sim 10^{-9}$ and the scalar kinetic energy is negligible.""",
    r"""        at $z_* \approx 1100$, where the SSEE dark energy is a fraction
        $\Omde(z_*) < \val{frac_de_zstar}$ of the density and the scalar kinetic
        energy is negligible.""")
# s_DE es la saturación |w0|, no la fracción de densidad a z<0.15
rep(r"""  \item SH0ES measures $H_0$ via the distance ladder at $z < 0.15$, where
        $\sDE \approx \val{S_DE_d3}$ and the scalar field is kinetically active.""",
    r"""  \item SH0ES measures $H_0$ via the distance ladder at $z < 0.15$, where
        dark energy is $\simeq\val{OMDE_DENS_d2}$ of the density today and the scalar
        field is kinetically active.""")

# 7. «por qué el CMB no cambia»: sin afirmar el mecanismo; P5 ya no es «la viscosidad IS»
rep(r"""The correction $\fsc$ is a late-time effect generated by scalar kinetic energy
that is negligible at $z \gg 1$.
Specifically:""",
    r"""Under the postulate~\eqref{eq:screen_postulate} the correction acts only on
locally measured rates; it does not enter the early-universe physics.
Specifically:""")
rep(r"""  \item \textbf{Growth factor $\sigma_8$}: not modified.
        The IS viscosity (Paper~5) operates through the growth equation,
        not through $H_0$, so the growth results of Paper~6 (the $S_8$
        prediction against KiDS-Legacy) are unaffected.""",
    r"""  \item \textbf{Growth factor $\sigma_8$}: not modified.
        The growth computations of Papers~5 and~6 run on the global
        background, so their results (the $S_8$ prediction against
        KiDS-Legacy) are unaffected.""")
rep(r"""give $r_{d,\rm new} = r_d\,(1-\fsc) \approx 137.3$\,Mpc, a shift of the acoustic
scale by the full $\fsc$ --- which is excluded by Paper~3.
The present mechanism does \emph{not} modify $r_d$; it operates entirely
at $z < 0.15$ through the scalar kinetic energy, a physically distinct sector.""",
    r"""shorten $r_d$ by the full fraction $\fsc\approx\val{F_SCREEN_IR_d4}$, a shift of the
acoustic scale that is excluded by Paper~3.
The present correction does \emph{not} modify $r_d$: under the postulate it
acts only on locally measured rates at $z < 0.15$.""")

# 8. tabla de consistencia: P4 ya no es «Sovereignties»; P5 no es «IS viscosity»; s_K sale de w0 (P1)
rep(r"""4 (Sovereignties) & $H_0^{\rm glob}$ as first sovereignty & No —
               $H_0^{\rm local}$ is a new sector \\
5 (IS viscosity) &""",
    r"""4 (Two-axiom CMB) & $\omega_b$, $n_s$ and the CMB background from $\phiG,\pi$ & No ---
               $H_0^{\rm local}$ is a new sector \\
5 (IS perturbations) &""")
rep(r"""7 (EFT)       & $s_K = \val{S_K_d6}$, $c_s^2 = \val{cs2_condensado_d6}$ & Provides $s_K$
               (input to Paper~9) \\""",
    r"""7 (EFT)       & $\alpha_K = \val{alpha_K_z0_d6}$, $c_s^2 = \val{cs2_condensado_d6}$; the field reproduces $w_0$ today & No ---
               $s_K$ follows from $w_0$ (Paper~1) \\""")
rep(r"""Its one input from the series is $\sK$ (Paper~7); $\MIRA$ is a structural
constant of the dictionary.""",
    r"""Its one input from the series is $w_0$ (Paper~1), through $\sK$; $\MIRA$ is a
structural constant of the dictionary.""")

# 9. criterio de falsación 1: 71.5/74.2 sin origen (restos de la cascada al revés)
rep(r"""  \item If future SH0ES or SHOES-equivalent measurements (post-2027)
        converge to $H_0^{\rm local} < 71.5$ or $> 74.2$ km/s/Mpc,
        the prediction is excluded at $\geq 1\sigma$.""",
    r"""  \item If future SH0ES or SH0ES-equivalent measurements (post-2027)
        converge to a local rate whose cascade output $H_0^{\rm local}(1-\fsc)$
        departs from $3(\phiG+\pi)^2$ by more than $3\sigma$ of the propagated
        uncertainty, the prediction is excluded.""")

# 10. comparación: 0.17σ a mano; «0.00σ» contradice el apéndice; «mejor que todo finalista» compara cosas distintas
rep(r"""Residual                & $5\sigma$ & $1.6$--$2\sigma$ & $2$--$3\sigma$ & $\sim 1\sigma$ & $\mathbf{0.17\sigma}$ \\""",
    r"""Residual                & $5\sigma$ & $1.6$--$2\sigma$ & $2$--$3\sigma$ & $\sim 1\sigma$ & $\mathbf{\val{p9_sh0es_sig_IR}\sigma}$ \\""")
rep(r"""  \item \textbf{Sub-sigma residual, zero added parameters.}  The
        SSEE output $H_0^{\rm SH0ES}(1-\fsc^{\rm IR})$, compared against the pure
        number $3(\phiG+\pi)^2$, sits at $\val{p9_sh0es_sig_IR}\sigma$
        from it when the IR cascade is applied to SH0ES --- better than every finalist of the
        $H_0$ Olympics, \emph{and} achieves this with zero added parameters.
        The UV completion (Paper~10) sharpens it to $0.00\sigma$.""",
    r"""  \item \textbf{Sub-sigma residual, zero added parameters.}  The
        SSEE output $H_0^{\rm SH0ES}(1-\fsc^{\rm IR})$, compared against the pure
        number $3(\phiG+\pi)^2$, sits at $\val{p9_sh0es_sig_IR}\sigma$
        from it when the IR cascade is applied to SH0ES, with zero added
        parameters. The residual is not directly comparable with those of the
        $H_0$ Olympics finalists, which predict the local rate rather than take
        it as input (caption of Table~\ref{tab:comparison}). With the complete
        $\fsc$ of Paper~10 the residual is $\val{p9_hglob_residuo}$~km/s/Mpc, which
        is not quoted as a significance: the propagated
        $\pm\val{p9_hglob_sigma}$~km/s/Mpc dominates it.""")

# 11. M de Paper 10: condicional a su Postulado C.1
rep(r"""Paper~10 of this series \citep{Paper10} derives $M^4 = 45\alpha^2\rho_{\rm crit} = 5\phiG^8\rho_{\rm crit}$
from the same $\alpha$-attractor that governs inflation (Paper~1), yielding""",
    r"""Paper~10 of this series \citep{Paper10} obtains $M^4 = 45\alpha^2\rho_{\rm crit} = 5\phiG^8\rho_{\rm crit}$
from the same $\alpha$-attractor that governs inflation (Paper~1), conditional on its
Postulate~C.1 (UV--IR separability), yielding""")

# 12. conclusiones
rep(r"""We have shown that the SSEE equation of state (Paper~7), with the structural""",
    r"""We have shown that the SSEE equation of state (Paper~1), with the structural""")
rep(r"""The correction is a late-time effect ($z < 0.15$) driven by the scalar
kinetic energy of the dark energy field; it does not modify the sound
horizon $r_d$, the CMB peak structure, or the growth factor $\sigma_8$
established in Papers~2--6.

The result is pre-committed: both values were derived from
the algebraic structure of SSEE before this comparison was made.
Future SH0ES""",
    r"""The correction acts on locally measured rates only ($z < 0.15$); it does
not modify the sound horizon $r_d$, the CMB peak structure, or the growth
factor $\sigma_8$ established in Papers~2--6.

The screening fraction has no parameter that could be tuned to the
comparison: it is fixed by $\phiG$ and $\pi$.
Future SH0ES""")

# 13. apéndice A: no es una cadena «al revés» (es la del cuerpo) y sí usa phi y pi (vía f);
#     la «doble identidad» es la misma expresión; nombres del diccionario viejo retirados de P4
rep(r"""This appendix supplies the independent self-consistency check that motivates
adopting $\val{H0_ALG_d5}$ as the algebraic target: it works the screening chain
\emph{backwards} from the SH0ES datum, assuming no algebraic value in advance,
and recovers exactly the same number.

\paragraph{Step P1: the inverse chain --- what background does SH0ES demand?}""",
    r"""This appendix records why $\val{H0_ALG_d5}$ is the algebraic target: it runs
the cascade of the body from the SH0ES datum with the complete screening
fraction, without using the target, and lands on it.

\paragraph{Step P1: what background does SH0ES demand?}""")
rep(r"""which asks, using only the measured datum and the derived screening fraction
(no model constant): \emph{what homogeneous""",
    r"""which asks, using only the measured datum and the screening fraction:
\emph{what homogeneous""")
rep(r"""This number is obtained by deducing \emph{backwards} from the data; $\phiG$ and
$\pi$ have not yet been invoked.

\paragraph{Step P2: the recovered value carries a double algebraic identity.}
Only now do we ask whether $\val{H0_GLOBAL_d5}$~km/s/Mpc has structure in the closed
$(\phiG,\pi)$ dictionary. It does, in two independent ways:
\begin{equation}
  \frac{H_0^{\rm base}}{\mathrm{km\,s^{-1}\,Mpc^{-1}}}
  \;\simeq\; \underbrace{3(\pi+\phiG)^2}_{\text{algebraic expression}}
  \;=\; \underbrace{\textsc{mikael}\times\Omega_{\rm DNAV}}_{\text{SSEE expression}}
  \;=\; \val{H0_ALG_d5}\,,
  \label{eq:double_identity}
\end{equation}
where $\Omega_{\rm DNAV}=\pi+\phiG=\val{OMEGA_d6}$ is the Stability Metric and
$\textsc{mikael}=3\Omega_{\rm DNAV}=\val{M_V_d6}$ coincides in value with the Maximal
Dimensional Invariant $M_v$ (one of the 25 Sovereign paths to $3\Omega$), generated in
the lineage from $\textsc{mika}+\pi$ with $\textsc{mika}=K_v+\phiG=\val{dos_Omega_phi_d4}$. The inverse-chain value~\eqref{eq:Hbase_value} exceeds the pure number by""",
    r"""This number uses $\phiG$ and $\pi$ only through $\fsc$; the target
$3(\phiG+\pi)^2$ has not been invoked.

\paragraph{Step P2: the recovered value and the pure number.}
Only now do we compare $\val{H0_GLOBAL_d5}$~km/s/Mpc with the $(\phiG,\pi)$ dictionary:
\begin{equation}
  \frac{H_0^{\rm base}}{\mathrm{km\,s^{-1}\,Mpc^{-1}}}
  \;\simeq\; 3(\pi+\phiG)^2 \;=\; M_v\,\Omega
  \;=\; \val{H0_ALG_d5}\,,
  \label{eq:double_identity}
\end{equation}
where $\Omega=\pi+\phiG=\val{OMEGA_d6}$ and $M_v=3\Omega=\val{M_V_d6}$ is the maximal
dimensional invariant of the dictionary. The two forms are the same expression,
not two independent identities. The value~\eqref{eq:Hbase_value} exceeds the pure number by""")
rep(r"""The background that SH0ES requires for exact closure ($\val{H0_GLOBAL_d5}$~km/s/Mpc) coincides, to
five figures, with the pure number $3(\phiG+\pi)^2$ already present in the
SSEE dictionary (and independently with $\textsc{mikael}\times\Omega_{\rm DNAV}$).
This double identity --- recognised a posteriori, not fitted --- is the
self-consistency evidence that, under the 2026 reframe, justifies adopting""",
    r"""The background that SH0ES requires for exact closure ($\val{H0_GLOBAL_d5}$~km/s/Mpc) coincides, to
five figures, with the pure number $3(\phiG+\pi)^2$ already present in the
SSEE dictionary. This coincidence --- recognised a posteriori, not fitted --- is
the self-consistency evidence that, under the 2026 reframe, justifies adopting""")
rep(r"""is built from $w_0$ alone, and $w_0$ is a constant of the model, so $\sK$ is a
number and not a function of redshift.""",
    r"""is built from $w_0$ alone, and $w_0$ is an algebraic constant (the present
value; it is $w(a)$ that evolves), so $\sK$ is a number and not a function of
redshift.""")

# 14. bibliografía interna: títulos reales (P8 con su título nuevo)
BIB = {
    r"""Almeida Vallejo, M.E.\ 2026a, SSEE Paper~1: Framework (this series).""":
    r"""Almeida Vallejo, M.E.\ 2026a, A Minimal-Parameter Framework for Cosmological
Dynamics and Galaxy Cluster Mass Discrepancies via Structural Self-Energy
Expansion (SSEE), Paper~1 of this series.""",
    r"""Almeida Vallejo, M.E.\ 2026b, SSEE Paper~2: MCMC DESI (this series).""":
    r"""Almeida Vallejo, M.E.\ 2026b, Bayesian MCMC Validation of the Structural
Self-Energy Expansion Framework (SSEE), Paper~2 of this series.""",
    r"""Almeida Vallejo, M.E.\ 2026c, SSEE Paper~3: CMB (this series).""":
    r"""Almeida Vallejo, M.E.\ 2026c, SSEE and the CMB Power Spectrum: Acoustic Peak
Reproduction via the $\omega_m$-Direct CMB Matter Density, Paper~3 of this series.""",
    r"""Almeida Vallejo, M.E.\ 2026g, SSEE Paper~7: EFT (this series).""":
    r"""Almeida Vallejo, M.E.\ 2026g, The SSEE Dark-Energy Sector as a Ghost
Condensate: Two-Term K-essence, Algebraic Sound Speed, and Bellini--Sawicki
Classification, Paper~7 of this series.""",
    r"""Almeida Vallejo, M.E.\ 2026h, SSEE Paper~8: Strong Gravity (this series).""":
    r"""Almeida Vallejo, M.E.\ 2026h, SSEE in the Strong-Gravity Regime: GR Lensing in
the Canonical Limit, a Disformal Contrast, and Solar-System Compliance, Paper~8
of this series.""",
    r"""Almeida Vallejo, M.E.\ 2026j, SSEE Paper~10: UV Completion (this series).""":
    r"""Almeida Vallejo, M.E.\ 2026j, UV Extension of SSEE Dark Energy:
$M^4 = 45\alpha^2\rho_{\rm crit}$ and a Conditional Self-Consistency Check on the
Hubble Tension, Paper~10 of this series.""",
}
for a, b in BIB.items():
    rep(a, b)

open(P, "w").write(s)

# P8: su título prometía «MIRA Emergence», que OP-13 retiró y su propio texto niega
P8 = "manuscript/SSEE_Paper8_StrongGravity.tex"
t = open(P8).read()
old = r"""\title{\textbf{SSEE in the Strong-Gravity Regime:\\
       Disformal Geodesics, MIRA Emergence,\\
       and Solar-System Compliance}}"""
new = r"""\title{\textbf{SSEE in the Strong-Gravity Regime:\\
       GR Lensing in the Canonical Limit, a Disformal Contrast,\\
       and Solar-System Compliance}}"""
if t.count(old) != 1:
    sys.exit("P8: título no encontrado")
open(P8, "w").write(t.replace(old, new))
B = "manuscript/ssee_unified.bib"
b = open(B).read()
old = "{{SSEE in the Strong-Gravity Regime: Disformal Geodesics, MIRA Emergence, and Solar-System Compliance}}"
if b.count(old) != 1:
    sys.exit("bib: título de P8 no encontrado")
open(B, "w").write(b.replace(old, "{{SSEE in the Strong-Gravity Regime: GR Lensing in the Canonical Limit, a Disformal Contrast, and Solar-System Compliance}}"))
print("P9: quinta lectura aplicada; P8 retitulado")
