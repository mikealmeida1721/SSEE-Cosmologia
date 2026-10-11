"""Quinta lectura P1 (2026-10-11): correcciones tras leer el paper entero. Ver P1.md."""
import pathlib, sys
P = pathlib.Path(__file__).resolve().parents[2] / 'manuscript/SSEE_Paper1_Framework.tex'
s = P.read_text()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f"«{old[:70]}» aparece {c} veces (esperaba {n})")
    s = s.replace(old, new)

# 1. resumen: el fondo y la atribución del ΔBIC (N=16 = DESI + prior Planck, sin cúmulos)
rep(r"""The background sector $(w_0,w_a,\Omega_{\rm DE})$ is fully algebraic
(zero fitted dimensionless parameters).""",
r"""The background sector --- the equation of state $(w_0,w_a)$ and the physical
matter density $\omega_m$ --- is fixed algebraically (zero fitted dimensionless
parameters).""")
rep(r"""These foundational parameters are tested against data in subsequent papers: a full Bayesian MCMC validation against DESI~DR2 \citep{AbdulKarim2025},
Planck~2018 \citep{PlanckVI2020}, and galaxy-cluster mass data ($\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$ for the dynamic
sector relative to $\Lambda$CDM) is presented in the companion Paper~2 \citep{SSEE_paperII}, while""",
r"""These foundational parameters are tested against data in subsequent papers: a full Bayesian MCMC validation against DESI~DR2 \citep{AbdulKarim2025}
with a Planck~2018 prior \citep{PlanckVI2020} ($\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$ relative to $\Lambda$CDM) and a
galaxy-cluster mass test are presented in the companion Paper~2 \citep{SSEE_paperII}, while""")
rep(r"""$r = \varphi^{-10} = 0.008131$ is predicted for LiteBIRD \citep{LiteBIRD2023}""",
    r"""$r = \varphi^{-10} = \val{R_TENSOR_d6}$ is predicted for LiteBIRD \citep{LiteBIRD2023}""")
rep(r"""\approx -0.840,
  \qquad
  w_a = -\frac{P}{I_g} = -\frac{2\varphi+\pi}{2(\varphi+\pi)} \approx -0.670.
\end{equation*}""", r"""\approx \val{W0_d3},
  \qquad
  w_a = -\frac{P}{I_g} = -\frac{2\varphi+\pi}{2(\varphi+\pi)} \approx \val{WA_d3}.
\end{equation*}""")

# 2. τ_Π lleva la saturación T_r/M_v, no la densidad Ω_DE (ssee_core: TAU_PI_H0 = KAL0/(3 S_DE))
rep(r"""($\tau_\Pi H_0 = \KALz/3\OmDE$)""", r"""($\tau_\Pi H_0 = \KALz M_v/3T_r$)""")
rep(r"""$\boldsymbol{I_g}=\pi+P\approx9.5193$""", r"""$\boldsymbol{I_g}=\pi+P\approx\val{IGNIS_d4}$""")

# 3. k_fs está retirado; extrapolación sin log
rep(r"""($k_{\mathrm{fs}}$, $r$, and the pre-registered DESI~DR3 test""", r"""($r$ and the pre-registered DESI~DR3 test""")
rep(r"""as the inverse of the error bar, so the pre-registered arithmetic is explicit:
a further tightening comparable to the DR1$\to$DR2 step leaves us near
$0.4$--$0.5\sigma$, while a joint ${>}3\sigma$ exclusion refutes the algebraic
background outright.""", r"""as the inverse of the error bar, so the pre-registered arithmetic is explicit:
a further tightening comparable to the DR1$\to$DR2 step leaves the point well
inside $1\sigma$ unless the measured centre moves, while a joint ${>}3\sigma$
exclusion refutes the algebraic background outright.""")

# 4. tabla de registro
rep(r"""$f\sigma_8(z{=}0.5)$ & $0.70\sigma$ mean tension""", r"""$f\sigma_8(z{=}0.5)$ & $\val{fs8_tmedia_ssee}\sigma$ mean tension""")
rep(r"""\emph{no} free cosmological parameter & Prediction \\""",
    r"""\emph{no} free cosmological parameter; data public since 2025, no priority claimed & Retrodiction \\""")
rep(r"""$r = \varphi^{-10}$ & $0.008131$ & LiteBIRD ${\sim}2032$ & Prediction \\""",
    r"""$r = \varphi^{-10}$ & $\val{R_TENSOR_d6}$ & LiteBIRD ${\sim}2032$ & Prediction \\""")

# 5. Principio 1: había bariones solos (sin materia oscura fría) y la saturación como densidad
rep(r"""    \lim_{a\to0} H^2(a) \propto \rho_{\rm bar},
    \qquad
    \lim_{a\to\infty} H^2(a) = \frac{8\pi G}{3}\,\rho_{{\rm crit},0}
    \left(\frac{T_r}{M_v}\right).""", r"""    \lim_{a\to0} H^2(a) \propto \rho_r+\rho_m,
    \qquad
    \lim_{a\to\infty} H^2(a) = H_\infty^2 = \text{const}.""")

# 6. Postulado S: s = T_r/M_v es saturación (ecuación de estado), no la densidad Ω_DE
rep(r"""The dark sector is a one-parameter family in $s$, with the density fraction
and the equation of state both fixed by it:
\begin{equation}
  \Omega_{\rm DE} = s, \qquad w_0 = -s.
  \label{eq:sat_correspondence}
\end{equation}
The two endpoints are physically forced and require no assumption:
\begin{itemize}\itemsep2pt
  \item $s\to0$: $(\Omega_{\rm DE},w_0)\to(0,0)$ --- the Einstein--de~Sitter
        (matter-only) limit;
  \item $s\to1$: $(\Omega_{\rm DE},w_0)\to(1,-1)$ --- the exact de~Sitter
        limit, already imposed by Principle~1.
\end{itemize}""", r"""The dark-energy equation of state today is fixed by it:
\begin{equation}
  w_0 = -s.
  \label{eq:sat_correspondence}
\end{equation}
$s$ is a saturation, a number of the equation of state, and \emph{not} the
dark-energy density fraction: that one is $\Omega_{\rm DE}=1-\Omega_m=\val{OMDE_DENS_d6}$
and carries a factor of $H$ through $\Omega_m=\omega_m/h^2$; $s$ carries none.
\emph{(Corrected 2026-10-11: earlier versions wrote $\Omega_{\rm DE}=s$ here,
which read literally makes $1+w_0$ a matter density --- the very conflation
withdrawn in \S\ref{sec:two_omega_m}.)}
The two endpoints are physically forced and require no assumption:
\begin{itemize}\itemsep2pt
  \item $s\to0$: $w_0\to0$ --- a pressureless, matter-like component;
  \item $s\to1$: $w_0\to-1$ --- a cosmological constant, the de~Sitter
        endpoint already imposed by Principle~1.
\end{itemize}""")

# 7. §1.6: la «acción efectiva» con ρ_crit·T_r/M_v era energía oscura constante (w=−1) con la saturación como densidad
rep(r"""Instead of an arbitrary cosmological constant $\Lambda$, the vacuum energy density is
fixed by the algebraic ratio $T_r/M_v$, leading to the background-level
effective action:
\begin{equation}
  S_{\SSEE}^{\rm bg} = \int d^4x\,\sqrt{-g}
  \left[\frac{R}{16\pi G}
        - \rho_{{\rm crit},0}\!\left(\frac{T_r}{M_v}\right)
        + \mathcal{L}_{\rm matter}\right].
  \label{eq:action}
\end{equation}
This action encodes the background Friedmann dynamics only: the dark-energy
density is constant at the background level and set by the algebraic
ratio $T_r/M_v$.  It does not propagate scalar perturbations; the
perturbation-level dynamics require a scalar-field extension, developed
in the EFT embedding of Appendix~A (Eq.~\ref{eq:eft_action}).  Within the
Horndeski class of scalar-tensor theories \citep{Horndeski1974,Gubitosi2013,Bellini2015},
a minimally coupled k-essence scalar \citep{ArmendarizPicon2001} with the two-term
action $K(X)=c_1X+c_2X^2$ and no potential reproduces $w_0$ algebraically while
remaining ghost-free and gradient-stable: it is a ghost condensate with adiabatic
$c_s^2=\val{cs2_condensado_d6}$ (Paper~7).""",
r"""Instead of a cosmological constant $\Lambda$, the dark-energy sector is a
minimally coupled k-essence scalar \citep{ArmendarizPicon2001} within the
Horndeski class \citep{Horndeski1974,Gubitosi2013,Bellini2015}, with the
two-term action of Paper~7 and no potential:
\begin{equation}
  S_{\SSEE} = \int d^4x\,\sqrt{-g}
  \left[\frac{R}{16\pi G} + c_1X + c_2X^2 + \mathcal{L}_{\rm matter}\right].
  \label{eq:action}
\end{equation}
It reproduces $w_0=-T_r/M_v$ algebraically while remaining ghost-free and
gradient-stable: it is a ghost condensate with adiabatic
$c_s^2=\val{cs2_condensado_d6}$ (Paper~7). Its density today is
$\Omega_{\rm DE}=1-\Omega_m$; the ratio $T_r/M_v$ fixes its equation of state,
not its amount. \emph{(Corrected 2026-10-11: earlier versions wrote here a
constant vacuum term $\rho_{{\rm crit},0}\,T_r/M_v$, which has $w=-1$ and uses
the saturation as a density.)}""")
rep(r"""refuted by: (1) direct detection of a collisionless dark-matter particle accounting for
the missing mass; (2) definitive cosmological constraints proving $\wa=0$; or
(3) high-significance confirmation of a normal neutrino hierarchy with
$\sum m_\nu < 0.06$\,eV.""", r"""refuted by: (1) definitive cosmological constraints proving $\wa=0$, or a
${>}3\sigma$ exclusion of the fixed point $(w_0,w_a)$; (2) a cosmological
measurement of $\sum m_\nu$ excluding the algebraic $\val{SUM_MNU_EV_d4}$\,eV; or
(3) $r$ excluded at the LiteBIRD sensitivity. \emph{(Corrected 2026-10-11: the
detection of a dark-matter particle was listed here as a falsifier; the model
contains cold dark matter, $\omega_c=\KALz\,\omega_b\,n_s$, so such a detection
would test what it is made of (OP-19), not refute it.)}""")

# 8. §2: Friedmann con bariones solos y ρ_DE = ρ_crit·T_r/M_v
rep(r"""\citep{Chevallier2001,Linder2003} $w(a)=\wz+\wa(1-a)$. Motivated by Eq.~\eqref{eq:action}, the expansion is subject to
an effective geometric pressure:
\begin{equation}
  H^2 = \frac{8\pi G}{3}\!\left(\rho_{\rm bar}+\rho_{\rm DE}\right),
  \qquad
  \rho_{\rm DE} = \rho_{{\rm crit},0}\!\left(\frac{T_r}{M_v}\right).
\end{equation}
The baseline state $\wz$ is set by the static geometric ratio $T_r/M_v$, and the evolution""",
r"""\citep{Chevallier2001,Linder2003} $w(a)=\wz+\wa(1-a)$. The expansion obeys
\begin{equation}
  H^2 = \frac{8\pi G}{3}\!\left(\rho_r+\rho_m+\rho_{\rm DE}\right),
  \qquad
  \rho_{\rm DE}(a) = (1-\Omega_m)\,\rho_{{\rm crit},0}\;a^{-3(1+\wz+\wa)}e^{-3\wa(1-a)},
\end{equation}
with the single matter density $\Omega_m=\omega_m/h^2$ (baryons, cold dark
matter and neutrinos). The baseline state $\wz$ is set by the static geometric ratio $T_r/M_v$, and the evolution""")
rep(r"""  \wz = -\frac{T_r}{M_v} \approx -0.840,
  \qquad
  \wa = -\frac{P}{I_g}  \approx -0.670.""", r"""  \wz = -\frac{T_r}{M_v} \approx \val{W0_d3},
  \qquad
  \wa = -\frac{P}{I_g}  \approx \val{WA_d3}.""")
rep(r"""While it yields $w_0+w_a=-1.510$,""", r"""While it yields $w_0+w_a=\val{w0_mas_wa}$,""")
rep(r"""  a_* = 1 + \frac{1+\wz}{\wa} = 0.761
  \quad (z_* = 0.314).""", r"""  a_* = 1 + \frac{1+\wz}{\wa} = \val{a_cruce}
  \quad (z_* = \val{z_cruce}).""")
rep(r"""$w_\varphi=w_0>-1$, where $c_s^2=0.021284>0$.""", r"""$w_\varphi=w_0>-1$, where $c_s^2=\val{cs2_condensado_d6}>0$.""")
rep(r"""$c(a)=-w_a(1-a)/(1+w_0)=4.186\,(1-a)$""", r"""$c(a)=-w_a(1-a)/(1+w_0)=\val{c_cruce_coef}\,(1-a)$""")
rep(r"""($c=2.09$ at
$z=1$)""", r"""($c=\val{c_cruce_z1}$ at
$z=1$)""")
rep(r"""The \SSEE\ algebraic point $(\wz,\wa)=(-0.840,-0.670)$ falls within the
68\% confidence contours of the combined BAO+CMB+DESY5 datasets
(Mahalanobis $\chi^2_{2D}=0.42$, i.e.\ $0.24\sigma$ against DESI+CMB+Pantheon+, $0.2$--$1.8\sigma$ across SN compilations; quantified in Paper~2""",
r"""The \SSEE\ algebraic point $(\wz,\wa)=(\val{W0_d3},\val{WA_d3})$ falls within the
68\% confidence contour of DESI~DR2 BAO+CMB+Pantheon+
(Mahalanobis $\chi^2_{2D}=\val{p2_chi2_2D_ec26}$, i.e.\ $\val{p2_w0wa_ssee_ec26}\sigma$), and at
$\val{p2_w0wa_ssee_ec28_d1}$--$\val{p2_w0wa_ssee_ec27_d1}\sigma$ against the other supernova compilations (quantified in Paper~2""")

# 9. sector dinámico: los cúmulos no prueban el fondo (lo dice §3.2)
rep(r"""  Validated against: DESI~DR2 BAO (13 measurements, $0.295\leq z\leq2.33$),
  galaxy-cluster mass data (IGIMF baseline, Paper~2).
  \textit{Result}: $\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$ favouring SSEE (Paper~2),
  $0.24\sigma$ from""", r"""  Validated against: DESI~DR2 BAO (13 measurements, $0.295\leq z\leq2.33$)
  with a Planck~2018 prior.
  \textit{Result}: $\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$ favouring SSEE (Paper~2),
  $\val{p2_w0wa_ssee_ec26}\sigma$ from""")

# 10. el titular CMB es el χ² mínimo de cada modelo, no una cadena
s = s.replace(r"full \texttt{plik} MCMC", r"full \texttt{plik}")
rep(r"""CMB parsimony, \textbf{canonical} (off-diag.\ TTTEEE+lowl+lensing, Paper~3 §b1)""",
    r"""CMB parsimony, \textbf{canonical} (off-diag.\ TTTEEE+lowl+lensing, $\chi^2$ minimum of each model, Paper~3 §b1)""")
rep(r"""(cross-check; $H_0{=}67.962$)""", r"""(cross-check; $H_0{=}\val{H0_GLOBAL_d3}$)""")

# 11. sector algebraico: BBN no mide Σm_ν; H_0 no es salida algebraica; AUDIT.md ya no lo documenta
rep(r"""  Cross-validated against: Planck 2018 ($n_s$, $\Omega_b h^2$, $H_0$),
  LiteBIRD forecast ($r$), BBN ($\sum m_\nu$), Paper~4.""",
    r"""  Cross-validated against: Planck 2018 ($n_s$, $\Omega_b h^2$, $\Omega_c h^2$),
  BBN ($Y_p$, $\Omega_b h^2$), LiteBIRD forecast ($r$), Paper~4.""")
rep(r"""  (documented in Table~\ref{tab:derivation_chain} and \texttt{AUDIT.md}).""",
    r"""  (documented in Table~\ref{tab:derivation_chain}).""")

# 12. DR3 (registro, §1.2) frente a «DR5+»
rep(r"""framework, not to create rescue mechanisms.  If DESI~DR5+ excludes""", r"""framework, not to create rescue mechanisms.  If DESI~DR3 or a later release excludes""")
rep(r"""  \item DESI~DR5+ posterior excludes $(-0.840,-0.670)$ at $>3\sigma$; or""",
    r"""  \item DESI~DR3 or a later posterior excludes $(\val{W0_d3},\val{WA_d3})$ at $>3\sigma$; or""")
rep(r"""  DESI~DR2 $\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$; $w_0,w_a$ within $0.24\sigma$ (Pantheon+) &
  DESI~DR5+ excludes $(-0.840,-0.670)$;""", r"""  DESI~DR2 $\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$; $w_0,w_a$ within $\val{p2_w0wa_ssee_ec26}\sigma$ (Pantheon+) &
  DESI~DR3+ excludes $(\val{W0_d3},\val{WA_d3})$;""")
rep(r"""  Euclid/KiDS $\Omega_m<0.25$ at $z<1$ &""", r"""  $\Omega_m$ outside $[0.25,0.36]$ at $z<1$, or $S_8$ ${>}3\sigma$ from $\val{S8_leg_pred}$ &""")

# 13. apéndice B
rep(r"""& Viscosity; $M_{\rm cluster}$ & A \\""", r"""& Retention; $\omega_c$ & A \\""")
rep(r"""$\val{OMEGA_C_H2_d6}$ ($0.4\sigma$) & Planck 2018 & A \\
$r$       & $\varphi^{-10}$ & $0.008131$ & LiteBIRD 2032 & A \\""", r"""$\val{OMEGA_C_H2_d6}$ ($\val{wc_ns_sigma_abs}\sigma$) & Planck 2018 & A \\
$r$       & $\varphi^{-10}$ & $\val{R_TENSOR_d6}$ & LiteBIRD 2032 & A \\""")
rep(r"""$\val{SUM_MNU_EV_d5}$ eV & Planck+BBN & A \\""", r"""$\val{SUM_MNU_EV_d5}$ eV & Planck+DESI & A \\""")
rep(r"""Similarly, $\mathrm{KAL}_0$ is both a derived constant (Level~2) and
a dynamical viscosity operator scaling cluster masses.""", r"""Similarly, $\mathrm{KAL}_0$ is both a derived constant (Level~2) and the
retention constant that fixes the cold-matter density, $\omega_c=\mathrm{KAL}_0\,\omega_b\,n_s$
(it does not amplify gravity).""")
rep(r"""$\Omega_c h^2 = \val{KAL0_d6}\times\val{OMEGA_B_H2_d5}\times\val{N_S_d5} = \val{OMEGA_C_H2_d6}$""",
    r"""$\Omega_c h^2 = \val{KAL0_d6}\times\val{OMEGA_B_H2_d6}\times\val{N_S_d6} = \val{OMEGA_C_H2_d6}$""")

# 14. apéndice C: el acople disforme está retirado; T_r fija w_0 (saturación), no Ω_DE
rep(r"""& Portal / coupling & Disformal coupling (P8); cancels in $H_0$ cascade & $\times1$ \\""",
    r"""& Portal / coupling & Cancels in $H_0$ cascade (the coupling $\beta_c=-\mathrm{AURA}$ is withdrawn, P7) & $\times1$ \\""")
rep(r"""3D saturation horizon $\to w_0,\Omega_{\rm DE}$ & $\times3$ \\""", r"""3D saturation horizon $\to w_0$ & $\times3$ \\""")
rep(r"""($\varphi+\beta=(3\varphi+\pi)/2\approx3.998$)""", r"""($\varphi+\beta=(3\varphi+\pi)/2\approx\val{AURA_d3}$)""")
rep(r"""($\mathrm{AURA}/2=(3\varphi+\pi)/4\approx1.9989$)""", r"""($\mathrm{AURA}/2=(3\varphi+\pi)/4\approx\val{MIRA_d4}$)""")
rep(r"""(dimensionless, $\approx2.191$)""", r"""(dimensionless, $\approx\val{TAU_PI_H0_d3}$)""")

# 15. tipo M: el MCMC de P2 no lleva cúmulos
rep(r"""  pipeline described in Paper~2, using DESI~DR2 BAO, Planck~2018
  priors, and galaxy-cluster mass data. These results""", r"""  pipeline described in Paper~2, using DESI~DR2 BAO and Planck~2018
  priors. These results""")

# 16. niveles: el apéndice E contradecía la tabla maestra (K_v, M_v en L1 aquí; L2 allí; P_sc al revés)
rep(r"""Four constants ($\Omega$, $\beta$, $K_v$, $M_v$) are Level~1 — direct
combinations of $\varphi$ and $\pi$; three ($\mathrm{KAL}_0$, $P_{sc}$, $T_r$)
are Level~2 — using Level~1 constants ($\Omega$, $\beta$) as intermediates:""",
r"""Following the levels of Table~\ref{tab:derivation_chain}, three constants
($\Omega$, $\beta$, $P_{sc}$) are Level~1 --- one operation on $\varphi$, $\pi$ and
their sum $\Omega$; four ($\mathrm{KAL}_0$, $K_v$, $T_r$, $M_v$) are Level~2 ---
built on a Level~1 register ($\beta$ or $\Omega$) or, for $M_v$, on $K_v$:""")
rep(r"""$\beta$  & BIAL / Base Coupling     & $(\varphi+\pi)/2$ & \val{BETA_d6} & L1\\
$K_v$    & KRYSTOS$_V$ / Structural Constraint & $\varphi+\pi+\Omega$ & \val{K_V_d6} & L1\\
$M_v$    & ATLAS / Maximal Invariant & $\varphi+\pi+K_v$ & \val{M_V_d6} & L1\\
\midrule
$\mathrm{KAL}_0$ & Structural Retention & $\beta+\pi$ & \val{KAL0_d6} & L2\\
$P_{sc}$ & PYROS / Dynamical Scalar & $\Omega+\varphi$ & \val{P_SC_d6} & L2\\
$T_r$    & TRIAL / Saturation Horizon & $3(\varphi+\beta)$ & \val{T_R_d6} & L2\\""",
r"""$\beta$  & BIAL / Base Coupling     & $(\varphi+\pi)/2$ & \val{BETA_d6} & L1\\
$P_{sc}$ & PYROS / Dynamical Scalar & $\Omega+\varphi$ & \val{P_SC_d6} & L1\\
\midrule
$\mathrm{KAL}_0$ & Structural Retention & $\beta+\pi$ & \val{KAL0_d6} & L2\\
$K_v$    & KRYSTOS$_V$ / Structural Constraint & $\varphi+\pi+\Omega$ & \val{K_V_d6} & L2\\
$T_r$    & TRIAL / Saturation Horizon & $3(\varphi+\beta)$ & \val{T_R_d6} & L2\\
$M_v$    & ATLAS / Maximal Invariant & $\varphi+\pi+K_v$ & \val{M_V_d6} & L2\\""")
rep(r"""$M_v = 3(\varphi+\pi)$
is the maximal element at Layer~1, and no additional Layer~2 combination""", r"""$M_v = 3(\varphi+\pi)$
is the maximal element, and no additional Layer~2 combination""")
rep(r"""= \frac{\pi+\varphi}{2} + \varphi = \frac{3\varphi+\pi}{2} \approx 3.9978.""", r"""= \frac{\pi+\varphi}{2} + \varphi = \frac{3\varphi+\pi}{2} \approx \val{AURA_d5}.""")
rep(r"""\mathrm{MIRA} = \frac{\beta+\varphi}{2} = \frac{3\varphi+\pi}{4} \approx 1.9989.""", r"""\mathrm{MIRA} = \frac{\beta+\varphi}{2} = \frac{3\varphi+\pi}{4} \approx \val{MIRA_d4}.""")
rep(r"""under the discrete exchange $\varphi\leftrightarrow\pi$, the scalar-kinetic constant
$\mathrm{KAL}_0=(\varphi+3\pi)/2$ maps \emph{exactly} to the photon-sector constant
$\mathrm{AURA}=(3\varphi+\pi)/2$, and vice versa.""", r"""under the discrete exchange $\varphi\leftrightarrow\pi$, the retention constant
$\mathrm{KAL}_0=(\varphi+3\pi)/2$ maps \emph{exactly} to
$\mathrm{AURA}=(3\varphi+\pi)/2$, and vice versa.""")

# 17. n_s: este párrafo invertía la dirección del Postulado I (§1.3)
rep(r"""The SSEE algebraic commitment is $n_s = 1 - \varphi^{-7}$, fixed by the
register structure independently of any inflationary framework
(Structural Constant Dictionary, Zenodo~10.5281/zenodo.20684908); we make no
claim of temporal priority over the public Planck releases, which predate this work.
It is not derived from the $\alpha$-attractor class
\citep{Starobinsky1980,KalloshLinde2013,Ferrara2013}; rather, compatibility with
that class is established \emph{a posteriori} in App.~A §A.5: the two
independent SSEE axioms ($n_s = 1-\varphi^{-7}$ and $r = \varphi^{-10}$)
determine $N = 2\varphi^7\approx58.07$ and $\alpha = \varphi^4/3$ exactly
as a consistency check, not as a derivation.""",
r"""The value $n_s = 1 - \varphi^{-7}$ entered the Structural Constant Dictionary
(Zenodo~10.5281/zenodo.20684908) as an algebraic commitment; we make no claim of
temporal priority over the public Planck releases, which predate this work.
Its physical embedding is Postulate~I (\S\ref{sec:scope}): an $\alpha$-attractor
\citep{Starobinsky1980,KalloshLinde2013,Ferrara2013} with $\alpha=\varphi^4/3$ and
$N_*=2\varphi^n$, where the inflation window selects $n=7$, $N_*=\val{dos_phi7_d2}$. From it
$n_s=1-2/N_*=1-\varphi^{-7}$ follows, and $r=12\alpha/N_*^2=\varphi^{-10}$ is then a
consequence of the postulated $\alpha$, not an independent axiom (App.~A §A.5).""")
rep(r"""gives $0.02242$, at $\val{wb_planck_sig}\sigma$""", r"""gives $\val{OMEGA_B_H2_d5}$, at $\val{wb_planck_sig}\sigma$""")
rep(r"""ratio $r=\varphi^{-10}=0.008131$ (LiteBIRD, CMB-S4)""", r"""ratio $r=\varphi^{-10}=\val{R_TENSOR_d6}$ (LiteBIRD, CMB-S4)""")
P.write_text(s); print("P1 ok")
