#!/usr/bin/env python3
"""Quinta lectura P4 (2026-10-11): reemplazos exactos; aborta si un conteo no casa."""
import sys

P = "manuscript/SSEE_Paper4_ToE.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


# --- resumen ---
rep(r"""A third structural constant, $\Omega = \varphi+\pi$, follows as
a theorem rather than an independent axiom;""",
    r"""A third structural constant, $\Omega = \varphi+\pi$, is a definition
rather than an independent axiom;""")
rep(r"""(notably the neutrino mass sum $\Sigma m_\nu$, classified as Type~P later in the paper)""",
    r"""(notably the neutrino mass sum $\Sigma m_\nu$, formerly classified as Type~P)""")
rep(r"""From these two axioms alone we derive, without fitting:""",
    r"""From these two axioms --- and, for the Hubble rate, the measured SH0ES rate as the single
dimensional input --- we derive, without fitting:""")
rep(r"""which read in km\,s$^{-1}$\,Mpc$^{-1}$ lies $1.1\sigma$ from Planck~2018.""",
    r"""which read in km\,s$^{-1}$\,Mpc$^{-1}$ lies $\val{halg_planck_sig}\sigma$ from Planck~2018.""")
rep(r"""where the exponent~7 equals the number of primary structural registers in the \SSEE\ hierarchy;""",
    r"""where the exponent~7 is fixed by Postulate~I of Paper~1 ($N_*=2\varphi^n$ e-folds falls in the
inflation window $[50,60]$ only for $n=7$);""")
rep(r"""\item[(iv)] a local Hubble constant from the screening mechanism of Paper~9,
$H_0^{\rm glob,IR} = H_0^{\rm SH0ES}(1-f_{\rm scr}^{\rm IR}) = \val{p9_sh0es_glob_IR}$~km\,s$^{-1}$\,Mpc$^{-1}$
($\val{p9_sh0es_sig_IR}\sigma$ from the pure algebraic number $3(\varphi+\pi)^2=\val{H0_ALG_d6}$),
taking \citet{Riess2022} as the input (2026 reframe); the earlier""",
    r"""\item[(iv)] the global Hubble rate of the screening cascade of Papers~9--10, with
\citet{Riess2022} as the input: $H_0^{\rm glob}=H_0^{\rm SH0ES}(1-f_{\rm screen})=\val{H0_GLOBAL_d6}\pm\val{p9_hglob_sigma}$~km\,s$^{-1}$\,Mpc$^{-1}$
with the complete screening fraction (with the IR term alone,
$H_0^{\rm glob,IR}=\val{p9_sh0es_glob_IR}$, $\val{p9_sh0es_sig_IR}\sigma$ from $3(\varphi+\pi)^2$); the earlier""")
rep(r"""In the static (Eckart) regime $\Omega_c h^2 = K_{\rm AL}\,\Omega_b h^2 = \val{wc_estatico_ssee_d4}$ ($\val{wc_estatico_ssee_sigma}\sigma$);
modulated by the IS inflationary factor $n_s = 1-\varphi^{-7}$ this becomes""",
    r"""The static relation $\Omega_c h^2 = K_{\rm AL}\,\Omega_b h^2 = \val{wc_estatico_ssee_d4}$ ($\val{wc_estatico_ssee_sigma}\sigma$);
with the primordial tilt $n_s = 1-\varphi^{-7}$ as a factor it becomes""")

# --- introduccion ---
rep(r"""$(w_0, w_a) = (-0.840, -0.670)$ in the Chevallier--Polarski--Linder""",
    r"""$(w_0, w_a) = (\val{W0_d6}, \val{WA_d6})$ in the Chevallier--Polarski--Linder""")
rep(r"""(Pantheon+; $0.2$--$1.8\sigma$ across SN compilations)""",
    r"""(Pantheon+; up to $\val{p2_w0wa_ssee_ec27_d1}\sigma$ across the other SN compilations)""")
rep(r"""(B-1) treating $\Omega = \varphi+\pi$ as an axiom rather than a theorem;""",
    r"""(B-1) treating $\Omega = \varphi+\pi$ as an axiom rather than a definition;""")

# --- phi es algebraico ---
rep(r"""Both are \emph{transcendental} numbers defined independently of any physical
measurement.""",
    r"""$\varphi$ is algebraic (a root of $x^2-x-1=0$) and $\pi$ is transcendental; both are
defined independently of any physical measurement.""")
rep(r"""\subsection{Theorem 1: \texorpdfstring{$\Omega = \varphi+\pi$}{Omega = phi+pi}}""",
    r"""\subsection{Definition: \texorpdfstring{$\Omega = \varphi+\pi$}{Omega = phi+pi}}""")
rep(r"""It is the unique combination that encodes the sum of the two geometric axioms:""",
    r"""It is defined as the sum of the two axioms:""")

# --- tabla cruzada ---
rep(r"""\quad $H_0$ target (pure number) & $3(\varphi+\pi)^2$ & \val{H0_ALG_d6} & $67.4\pm0.5$ & $1.1\sigma$ \\""",
    r"""\quad $H_0$ target (pure number) & $3(\varphi+\pi)^2$ & \val{H0_ALG_d6} & $67.36\pm0.54$ & $\val{halg_planck_sig}\sigma$ \\""")
rep(r"""\textbf{Hubble tension} & & & & \\
\quad Fractional correction & $K/H_0 = \frac{\varphi+3\pi}{6(\varphi+\pi)^2}$ & $8.12\%$ & $\approx 8\%$ & — \\
""", "")

# --- Sakharov: excluido (OPEN_PROBLEMS OP-1, 2026-09-08) ---
rep(r"""\textbf{Sakharov-mechanism motivation (not a quantitative derivation).}
We are explicit about the status of Eq.~\eqref{eq:Obh2}: it is an algebraic
ansatz whose \emph{form} is motivated by --- but not derived from --- the
Sakharov conditions for baryogenesis \citep{Sakharov1967}. The three conditions
are realised structurally in \SSEE\ as follows:
\begin{itemize}
  \item \textbf{B-violation:} sphaleron transitions at $T_{\rm EW}\sim\Omega$
    (SSEE units), with rate $\Gamma_{\rm sph} \propto (\alpha_W T)^4 e^{-E_{\rm sph}/T}$.
  \item \textbf{CP-violation:} $\delta_{\rm CP} = (\pi-\varphi)/\Omega$, the ratio of
    the transcendental excess ($\pi$, gauge-boson loops) to the algebraic scalar sector
    ($\varphi$), normalised by $\Omega = \varphi+\pi$.
  \item \textbf{Non-equilibrium:} gravitational reheating with
    $T_{\rm rh}\sim10^{-4}$~GeV $\ll T_{\rm EW}$ ensures departure from equilibrium.
\end{itemize}
The Sakharov scaling $\eta_B \propto \delta_{\rm CP}/(\text{expansion rate})$
motivates the \emph{shape} $\Omega_b h^2 \sim (\pi-\varphi)/(3\Omega^2)$, with
$(\pi-\varphi)$ as the CP-asymmetry numerator and $3\Omega^2$ as the
normalising denominator. Two caveats are stated openly. First, $3\Omega^2$""",
    r"""\textbf{Status: an algebraic ansatz, with no baryogenesis mechanism behind it.}
Eq.~\eqref{eq:Obh2} is an algebraic ansatz. Earlier drafts motivated its \emph{form}
with the Sakharov conditions \citep{Sakharov1967} --- electroweak sphalerons, a CP
phase $\delta_{\rm CP}=(\pi-\varphi)/\Omega$, and departure from equilibrium through a
late reheating --- read as $\eta_B\propto\delta_{\rm CP}/(\text{expansion rate})$, with
$(\pi-\varphi)$ as numerator and $3\Omega^2$ as denominator. That mechanism is
\emph{withdrawn}: the reheating it requires, $T_{\rm rh}\approx10^{-4}$~GeV, lies below
the BBN lower bound $T_{\rm rh}\gtrsim4\times10^{-3}$~GeV \citep{deSalas2015} and six
orders of magnitude below the temperature at which sphalerons are active, so the
sphalerons it invokes would never have run. The formula does not depend on it and
does not move. Two caveats on the form remain. First, $3\Omega^2$""")
rep(r"""the algebraic \emph{form} only, not the absolute normalisation.
A scan of 96 algebraic candidates (see \texttt{ssee\_op1\_baryon\_density.py})
shows Eq.~\eqref{eq:Obh2} is the unique \SSEE\ monomial within $1\sigma$ of
Planck --- a selection statement, not a dynamical derivation.
The genuine quantitative test --- integrating the Boltzmann equation with the
sphaleron rate and the SSEE reheating history to obtain $\eta_B$
\emph{ab initio} --- is deferred to Paper~B; the companion framework script
\texttt{ssee\_op1\_baryogenesis.py} currently only verifies that the required
entropy-dilution factor is consistent with a quintessential-reheating
temperature $T_{\rm rh}\sim10^{-4}$~GeV, which is a consistency check, not a
prediction of $\eta_B$.""",
    r"""the algebraic \emph{form} only, not the absolute normalisation.
The formula was chosen among a handful of $\varphi,\pi$ monomials compared with Planck
(an early scan, archived without a log): a selection statement, not a dynamical
derivation. A derivation of $\omega_b$ from first principles remains open (OP-1).""")

# --- materia ---
rep(r"""  = \frac{\val{OMEGA_M_H2_d5}}{(0.67962)^2} = \val{OMEGA_M_TOTAL_d6},""",
    r"""  = \frac{\val{OMEGA_M_H2_d5}}{(\val{H_GLOBAL_h_d5})^2} = \val{OMEGA_M_TOTAL_d6},""")
rep(r"""The quantity $s_m=(\pi-\varphi)/[2(\varphi+\pi)]\approx 0.160$ ($=1+w_0$) is an
equation-of-state-sector identity, not a density.""",
    r"""The quantity $s_m=(\pi-\varphi)/[2(\varphi+\pi)]=\val{S_M_d6}$ ($=1+w_0$) is an
equation-of-state-sector identity, not a density.""")
rep(r"""structural retention $K_{\rm AL} = \beta + \pi \approx \val{KAL0_d4}$:
\begin{equation}
\Omega_c h^2 = K_{\rm AL}\,\Omega_b h^2 = \val{wc_estatico_planck_d5} \quad (+\val{wc_estatico_sigma_d1}\sigma\text{ Eckart static}).
\label{eq:omch2_static}
\end{equation}
When the Israel--Stewart inflationary correction is applied, the primordial spectral
factor $n_s = 1-\varphi^{-7}$ modulates the dark-matter density:""",
    r"""structural retention $K_{\rm AL} = \beta + \pi = \val{KAL0_d6}$:
\begin{equation}
\Omega_c h^2 = K_{\rm AL}\,\Omega_b h^2 = \val{wc_estatico_ssee_d4} \quad (\val{wc_estatico_ssee_sigma}\sigma\text{, static}).
\label{eq:omch2_static}
\end{equation}
With the primordial tilt $n_s = 1-\varphi^{-7}$ as a factor (the forward identity of
Paper~1):""")
rep(r"""\textbf{Note on $\Omega_b h^2$ input.}
The static relation (Eq.~\ref{eq:omch2_static}) is evaluated with the Planck~2018
\emph{observed} value $\Omega_b h^2 = 0.02237\pm0.00015$ \citep{PlanckCollaboration2020a}. The IS
relation (Eq.~\ref{eq:omch2_IS}), which is the canonical one, uses the \SSEE\ algebraic
$\Omega_b h^2 = (\pi-\varphi)/(3\Omega^2) = \val{OMEGA_B_H2_d6}$ ($\val{wb_planck_sig}\sigma$ from Planck)
and gives $\Omega_c h^2 = \val{OMEGA_C_H2_d6}$, $\val{wc_ns_sigma_abs}\sigma$ from Planck: no
observed input enters it.

Planck~2018: $0.1200\pm0.0012$; deviation~$= -0.6\sigma$ (using Planck observed $\Omega_b h^2$).
The IS modulation reduces the tension from $+\val{wc_estatico_sigma_d1}\sigma$ (Eckart) to $-0.6\sigma$ (IS),
within $1\sigma$ of the observed value and consistent with zero tension at $1\sigma$.""",
    r"""\textbf{Note on $\Omega_b h^2$ input.}
Both relations use the \SSEE\ algebraic
$\Omega_b h^2 = (\pi-\varphi)/(3\Omega^2) = \val{OMEGA_B_H2_d6}$ ($\val{wb_planck_sig}\sigma$ from Planck);
no observed input enters either. An earlier version evaluated the static one with
Planck's $\omega_b$, an ingredient of the other model.
Against Planck~2018 ($0.1200\pm0.0012$) the tilted relation, the canonical one, lies
$\val{wc_ns_sigma_abs}\sigma$ away; the static one, $\val{wc_estatico_ssee_sigma}\sigma$.""")

# --- n_s: Postulado I, no «siete registros» ---
rep(r"""\subsection{Primordial Spectral Index and the Seven-Level Hierarchy}""",
    r"""\subsection{Primordial Spectral Index}""")
i0 = s.index(r"\paragraph{Independent justification of the exponent~7.}")
i1 = s.index(r"\begin{equation}" + "\n" + r"\boxed{n_s = 1 - \varphi^{-7}")
s = s[:i0] + r"""\paragraph{Origin of the exponent~7 (Postulate~I of Paper~1).}
The form $N_*=2\varphi^n$ of the e-fold number, with $\alpha=\varphi^4/3$, is
Postulate~I of Paper~1. The integer is not chosen: of the powers of $\varphi$,
only $n=7$ puts $N_*$ inside the canonical inflation window $[50,60]$
($2\varphi^6$ falls below it, $2\varphi^8$ above). The spectral index follows:

""" + s[i1:]
rep(r"""The exponent~7 is not merely an ansatz: it follows from $\alpha$-attractor inflation
with $\alpha = \varphi^4/3$ (derived in Paper~1, App.~A.5) via the universality theorem
of \citet{Kallosh2013}. For all $\alpha$-attractors with $N_\ast \gg \sqrt\alpha$, the
spectral index satisfies $n_s = 1 - 2/N_\ast$ at leading order. Setting
$N_\ast = 2\varphi^7 \approx 58.07$~e-folds (within the standard window $N_\ast \in[50,65]$):""",
    r"""It uses the universality of $\alpha$-attractor inflation \citep{Kallosh2013}: for all
$\alpha$-attractors with $N_\ast \gg \sqrt\alpha$, the spectral index satisfies
$n_s = 1 - 2/N_\ast$ at leading order. Setting $N_\ast = 2\varphi^7 = \val{dos_phi7_d6}$~e-folds:""")
rep(r"""$N_\ast = 2\varphi^7 \approx 58.07$ is the number of inflationary e-folds of the
SSEE quintessential inflation model with $\alpha = \varphi^4/3$ and a reheating
temperature $T_{\rm rh} \approx (30/\pi^2 g_*)^{1/4}\,V_{\rm end}^{1/4}
\approx 9.4\times10^{15}$~GeV (corresponding to $\rho_{\rm rh}\approx V_{\rm end}$).""",
    r"""$N_\ast = 2\varphi^7 = \val{dos_phi7_d6}$ is the number of inflationary e-folds of the
SSEE quintessential inflation model with $\alpha = \varphi^4/3$ and a reheating with
$\rho_{\rm rh}\approx V_{\rm end}$.""")
rep(r"""Its value, $N_\ast = \val{dos_phi7_d6}$, lies within the standard window $[50, 65]$ for
inflation with reheating (consistent with, but not proven by, the framework).
Numerically, the condition $\rho_{\rm end}/\rho_{\rm rh} = 3$ — which follows from
$\rho_{\rm end}=3V_{\rm end}$ (at $\varepsilon=1$) together with
$\rho_{\rm rh}=V_{\rm end}$ — gives $N_\ast = 58.25 - \ln(3)/6 = \val{N_star_rh_d3}$,
matching $2\varphi^7 = \val{dos_phi7_d6}$ to within $O(1/N_\ast)\approx 0.002$ e-folds.
The physical mechanism""",
    r"""Its value lies within the standard window $[50,60]$ for inflation with reheating
(consistent with, but not proven by, the framework). An earlier draft matched it to an
e-fold estimate built on a reference value $N_\ast=58.25$ that has no source in the
literature; that comparison is withdrawn. The physical mechanism""")
rep(r"""Planck~2018: $n_s = 0.9649\pm0.0042$; deviation $= 0.157\sigma$.""",
    r"""Planck~2018: $n_s = 0.9649\pm0.0042$; deviation $= \val{ns_planck_sig}\sigma$.""")

# --- BBN: la sensibilidad publicada; el 0.2471 de Planck no es una medida ---
rep(r"""Using the linearised sensitivity from PArthENoPE \citep{Pisanti2008},
$dY_p/d(\Omega_b h^2) \approx 0.96$, and the Planck~2018 anchor
$Y_p = 0.2471$ at $\Omega_b h^2 = 0.02237$:
\begin{equation}
\boxed{Y_p^{\rm SSEE} = 0.2471 + 0.96\times(\val{OMEGA_B_H2_d5}-0.02237) = \val{Yp_ssee_d4}.}
\label{eq:yp}
\end{equation}
Observed values: $Y_p = 0.2471\pm0.0003$ (Planck CMB, $+0.2\sigma$);
$Y_p = 0.2449\pm0.0040$ (HII regions, Aver et al.\ 2015, $+0.6\sigma$).
Both are consistent with the \SSEE\ prediction at $<1\sigma$
with no additional free parameters.""",
    r"""Using the linearised BBN sensitivity $dY_p/d\eta_{10}\approx0.0016$ with
$\eta_{10}=273.9\,\Omega_b h^2$ \citep{Steigman2007}, anchored on the BBN value
$Y_p = 0.2471$ that Planck~2018 derives at its $\Omega_b h^2 = 0.02237$:
\begin{equation}
\boxed{Y_p^{\rm SSEE} = 0.2471 + 0.0016\times273.9\times(\val{OMEGA_B_H2_d5}-0.02237) = \val{Yp_ssee_d4}.}
\label{eq:yp}
\end{equation}
The Planck value is itself a BBN computation from $\omega_b$, not an independent
measurement, so the test is against the helium observed in HII regions,
$Y_p = 0.2449\pm0.0040$ \citep{Aver2015}: $\val{Yp_aver_sig}\sigma$, with no additional free parameter.""")

# --- w0 wa ---
rep(r"""  K_v    &= \varphi+\pi+\Omega         \approx  \val{K_V_d4} \quad \text{(Structural Constraint)}.
\end{align}""",
    r"""  K_v    &= \varphi+\pi+\Omega         \approx  \val{K_V_d4} \quad \text{(Structural Constraint)},
\end{align}
with $I_g=\pi+P_{sc}=2(\varphi+\pi)$.""")
rep(r"""The algebraic point $(-0.840,-0.670)$ lies within the 68\% confidence region
of DESI~DR2+CMB+DESY5 data \citep{desidr2_2025}""",
    r"""The algebraic point lies within the 68\% confidence region
of DESI~DR2+CMB+Pantheon+ data \citep{desidr2_2025}""")

# --- tabla de parametros ---
rep(r"""$3(\varphi+\pi)^2$ (target)     & \val{H0_ALG_d6} & $67.4\pm0.5$  & $1.1\sigma$ & pure number (Type~P$^\dagger$) \\""",
    r"""$3(\varphi+\pi)^2$ (target)     & \val{H0_ALG_d6} & $67.36\pm0.54$  & $\val{halg_planck_sig}\sigma$ & pure number (Type~P$^\dagger$) \\""")
rep(r"""residual $+\val{p9_hglob_residuo}$ &""", r"""residual $\val{p9_hglob_residuo}$ km/s/Mpc &""")
rep(r"""$\Omega_c h^2$ (IS) &""", r"""$\Omega_c h^2$ &""")
rep(r"""$Y_p$               & \val{Yp_ssee_d4} & $0.2471\pm0.0003$   & $0.2\sigma$ & BBN (no fit) \\""",
    r"""$Y_p$               & \val{Yp_ssee_d4} & $0.2449\pm0.0040$ (HII) & $\val{Yp_aver_sig}\sigma$ & BBN (no fit) \\""")
rep(r"""\multicolumn{5}{l}{\footnotesize IS = Israel--Stewart modulation by $n_s=1-\varphi^{-7}$; reduces tension from $\val{wc_estatico_ssee_sigma}\sigma$ (Eckart) to $\val{wc_ns_sigma}\sigma$.}\\""",
    r"""\multicolumn{5}{l}{\footnotesize $\Omega_c h^2=\mathrm{KAL}_0\,\omega_b\,n_s$; without the factor $n_s$ (static) it would be $\val{wc_estatico_ssee_sigma}\sigma$ away.}\\""")
rep(r"""quantity $s_m=(\pi-\varphi)/[2(\varphi+\pi)]\approx 0.160$ ($=1+w_0$)}\\""",
    r"""quantity $s_m=(\pi-\varphi)/[2(\varphi+\pi)]=\val{S_M_d6}$ ($=1+w_0$)}\\""")

# --- seccion de la tension de Hubble: lo vigente primero ---
i0 = s.index(r"The dimensionless scalar $K=(\varphi+3\pi)/2")
i1 = s.index(r"series, where a structural screening fraction")
s = s[:i0] + r"""The Hubble tension between early- and late-universe measurements
\citep{Verde2019,Kamionkowski2023} is currently unresolved by $\Lambda$CDM. The
\SSEE\ treatment is that of Paper~9 of this
""" + s[i1:]
rep(r"""Paper~10 provides a UV-completion self-consistency check, sharpening the
residual to $\val{p9_hglob_residuo}$ ($H_0^{\rm glob} = \val{H0_GLOBAL_d6}$ with the complete $f_{\rm screen}$, IR$+$UV),
conditional on the UV--IR separability postulate.""",
    r"""Paper~10 provides a UV-completion self-consistency check, sharpening the
residual to $\val{p9_hglob_residuo}$~km\,s$^{-1}$\,Mpc$^{-1}$ ($H_0^{\rm glob} = \val{H0_GLOBAL_d6}$ with the complete $f_{\rm screen}$, IR$+$UV),
conditional on the UV--IR separability postulate. An earlier draft of this section
used an additive coincidence, $3(\varphi+\pi)^2+\mathrm{KAL}$, compared with the SH0ES
rate; it had no mechanism and is withdrawn.""")

# --- r: consecuencia del alfa-atractor, no analogia ---
rep(r"""By analogy with the seven-level spectral tilt, the tensor-to-scalar ratio is
predicted at the tenth golden harmonic:""",
    r"""For $\alpha$-attractors $r=12\alpha/N_*^2$ \citep{Kallosh2013}; with $\alpha=\varphi^4/3$ and
$N_*=2\varphi^7$ (Postulate~I), the tensor-to-scalar ratio is""")

# --- eta: por \val ---
rep(r"""standard BBN proportionality $\eta \approx 2.74\times10^{-8}\,\Omega_b h^2$:
\begin{equation}
  \eta_{\rm SSEE} = 2.74\times10^{-8}\times\frac{\pi-\varphi}{3(\varphi+\pi)^2}
    = 2.74\times10^{-8}\times0.02242 = 6.14\times10^{-10}.
\end{equation}
Measured value: $\eta = 6.1\times10^{-10}$ (Planck~2018); deviation $<3\%$.
\textbf{Falsification criterion:} $\eta < 5.8\times10^{-10}$ or $\eta > 6.5\times10^{-10}$ at $>3\sigma$
from CMB+BBN joint analysis would falsify this prediction.""",
    r"""standard BBN proportionality $\eta_{10} = 273.9\,\Omega_b h^2$ \citep{Steigman2007}:
\begin{equation}
  \eta_{\rm SSEE} = 273.9\times10^{-10}\times\frac{\pi-\varphi}{3(\varphi+\pi)^2}
    = \val{eta_ssee_d2}\times10^{-10}.
\end{equation}
It is $\Omega_b h^2$ restated, so it carries the same $\val{wb_planck_sig}\sigma$ from Planck and
the same falsification criterion.""")

# --- suma de neutrinos: criterio como P1/P2 ---
rep(r"""\textbf{Falsification criterion:} $\Sigma m_\nu > 0.12~\mathrm{eV}$ or
$\Sigma m_\nu < 0.058~\mathrm{eV}$ at $>3\sigma$ would falsify this prediction.""",
    r"""\textbf{Falsification criterion:} a measurement that excludes $\Sigma m_\nu=\val{SUM_MNU_EV_d4}$~eV at
$>3\sigma$ would falsify this prediction.""")

# --- discusion ---
rep(r"""$\Omega = \varphi+\pi$ is a \emph{theorem} (Section~\ref{sec:omega}),
not an axiom.""",
    r"""$\Omega = \varphi+\pi$ is a \emph{definition} (Section~\ref{sec:omega}),
not an axiom.""")
rep(r"""With $\alpha = \varphi^4/3$ (established in Paper~1) and $N_* = 2\varphi^7$""",
    r"""With $\alpha = \varphi^4/3$ (Postulate~I of Paper~1) and $N_* = 2\varphi^7$""")
rep(r"""The exponent~7 counts the depth of the algebraic hierarchy (Table~\ref{tab:hierarchy}),
and the same calculation""",
    r"""The exponent~7 is the only one that places $N_*$ in the inflation window,
and the same calculation""")
rep(r"""The static (Eckart) $\Omega_c h^2$ prediction of $\val{wc_estatico_ssee_d4}$ is $\val{wc_estatico_ssee_sigma}\sigma$
from Planck, but the IS modulation $\Omega_c h^2 \times n_s = \val{OMEGA_C_H2_d6}$ reduces
this to $\val{wc_ns_sigma}\sigma$ — within $1\sigma$ of observation (Eq.~\ref{eq:omch2_IS}).
Both use the SSEE baryon density $\omega_b=\val{OMEGA_B_H2_d6}$, not Planck's.
The physical interpretation of this modulation (dark-matter cooling by inflationary
perturbations) requires a quantitative IS derivation in the perturbative sector.
The $\delta_c$ prediction and $A_s,\tau$ derivation are reserved for Paper~5.""",
    r"""The static $\Omega_c h^2$ relation gives $\val{wc_estatico_ssee_d4}$, $\val{wc_estatico_ssee_sigma}\sigma$
from Planck; with the factor $n_s$ it gives $\val{OMEGA_C_H2_d6}$, $\val{wc_ns_sigma}\sigma$ (Eq.~\ref{eq:omch2_IS}).
Both use the SSEE baryon density $\omega_b=\val{OMEGA_B_H2_d6}$, not Planck's.
Why the primordial tilt multiplies the dark-matter density has no mechanism yet;
what the dark matter is made of is OP-19. A derivation of $A_s$ is OP-18.""")

# --- conclusion ---
rep(r"""(pure number; read in km\,s$^{-1}$\,Mpc$^{-1}$, $1.1\sigma$ from Planck), on which the measured SH0ES cascade lands""",
    r"""(pure number; read in km\,s$^{-1}$\,Mpc$^{-1}$, $\val{halg_planck_sig}\sigma$ from Planck), on which the measured SH0ES cascade lands""")
rep(r"""$Y_p = \val{Yp_ssee_d4}$ ($0.2\sigma$ from Planck CMB, $0.6\sigma$ from HII — no fit)""",
    r"""$Y_p = \val{Yp_ssee_d4}$ ($\val{Yp_aver_sig}\sigma$ from HII regions --- no fit)""")
rep(r"""motivates the
connection $H_0 = M_v \times \Omega$.""",
    r"""motivates taking
$M_v \times \Omega$ as the target against which the global rate is compared.""")
rep(r"""Script: \texttt{src/ssee\_paper4\_toe.py} (repository root).""",
    r"""Script: \texttt{src/p04\_toe/ssee\_paper4\_toe.py}.""")
rep(r"""Run: \texttt{python3 src/ssee\_paper4\_toe.py} — reproduces""",
    r"""Run: \texttt{python3 src/p04\_toe/ssee\_paper4\_toe.py} --- reproduces""")
rep(r"""disformal coupling $\beta_c=-\mathrm{AURA}$ of earlier drafts; Paper~7""",
    r"""coupling $\beta_c=-\mathrm{AURA}$ of earlier drafts; Paper~7""")
rep(r"""live disformal coupling is claimed here.""", r"""live coupling is claimed here.""")

open(P, "w").write(s)

B = "manuscript/SSEE_Paper4.bib"
b = open(B).read()
add = ""
if "deSalas2015" not in b:
    add += """
@article{deSalas2015,
  author  = {de Salas, P. F. and Lattanzi, M. and Mangano, G. and Miele, G. and Pastor, S. and Pisanti, O.},
  title   = {Bounds on very low reheating scenarios after {Planck}},
  journal = {Phys. Rev. D},
  year    = {2015},
  volume  = {92},
  pages   = {123534},
  eprint  = {1511.00672}
}
"""
if "Steigman2007" not in b:
    add += """
@article{Steigman2007,
  author  = {Steigman, G.},
  title   = {Primordial Nucleosynthesis in the Precision Cosmology Era},
  journal = {Ann. Rev. Nucl. Part. Sci.},
  year    = {2007},
  volume  = {57},
  pages   = {463},
  eprint  = {0712.1100}
}
"""
if "Aver2015" not in b:
    add += """
@article{Aver2015,
  author  = {Aver, E. and Olive, K. A. and Skillman, E. D.},
  title   = {The effects of {He I} $\\lambda$10830 on helium abundance determinations},
  journal = {JCAP},
  year    = {2015},
  volume  = {07},
  pages   = {011},
  eprint  = {1503.08146}
}
"""
open(B, "w").write(b + add)
print("P4: reemplazos aplicados")
