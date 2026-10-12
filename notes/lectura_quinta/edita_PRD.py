#!/usr/bin/env python3
"""PRD, quinta lectura (2026-10-12): lo que la lectura encontró, con su porqué en notes/lectura_quinta/PRD.md."""
import sys

P = "submission_PRD/SSEE_PRD.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


# 1. resumen: el 0.05σ de DR1 no tiene log (y P2 no lo usa); el rango por macro
rep(r"""The point was fixed in
advance and survives \emph{two independent} DESI releases: it sits at
$0.05\sigma$ from the DESI~DR1 $w_0w_a$CDM posterior and, after the uncertainties
tightened, at $\val{p2_w0wa_ssee_ec26}\sigma$ from the newer DESI~DR2 posterior
(Pantheon+; $0.2$--$1.8\sigma$ across supernova compilations,
$\chi^2_{\rm 2D}=\val{p2_chi2_2D_ec26}$)---the prediction did not move while the data improved.""",
    r"""The point was fixed in
advance and sits at $\val{p2_w0wa_ssee_ec26}\sigma$ from the DESI~DR2 $w_0w_a$CDM posterior
(Pantheon+; $\val{p2_w0wa_ssee_ec26_d1}$--$\val{p2_w0wa_ssee_ec27_d1}\sigma$ across supernova compilations,
$\chi^2_{\rm 2D}=\val{p2_chi2_2D_ec26}$).""")

# 2. la escala absoluta: Postulado D de P1 es el H medido (SH0ES), no un rho_Lambda
rep(r"""We are explicit about the framework's limits: the absolute vacuum scale enters
as a single measured input,""",
    r"""We are explicit about the framework's limits: the absolute scale enters
as a single measured input (the local expansion rate),""")
rep(r"""the absolute scale
of the vacuum enters as a single measured input (Postulate~D,
\S\ref{sec:open}),""",
    r"""the absolute scale
enters as a single measured input, the local expansion rate of SH0ES (Postulate~D,
\S\ref{sec:open}),""")
rep(r"""SSEE does not predict the absolute energy density of the dark sector. The
overall scale of the vacuum, $\rho_\Lambda\simeq6\times10^{-10}~\mathrm{J\,
m^{-3}}$, enters as a single measured input, which we label \emph{Postulate~D}.""",
    r"""SSEE does not predict the absolute energy density of the dark sector. The
only dimensionful input is a measured one, the local expansion rate
$H_0^{\rm SH0ES}$ (\emph{Postulate~D}, as in Paper~1); everything with units descends
from it through the screening cascade.""")
rep(r"""$\rho_{\rm vac}$ (abs.\ scale) & Vacuum            & single measured input          & P1,10  & Measured \\""",
    r"""$H_0^{\rm SH0ES}$ (abs.\ scale) & Background   & single measured input          & P1,9   & Measured \\""")

# 3. s_m: el símbolo Omega_m^dyn está retirado (era «sector frío»)
rep(r"""w_a=-\frac{P_{\mathrm{sc}}}{I_g}=\val{WA_d6},\qquad
\Om^{\mathrm{dyn}}=1+w_0=\val{S_M_d6} .""",
    r"""w_a=-\frac{P_{\mathrm{sc}}}{I_g}=\val{WA_d6},\qquad
s_m=1+w_0=\val{S_M_d6} .""")
rep(r"""The equation of state~\eqref{eq:w0wa} fixes the combination that earlier
versions called the \emph{dynamical} matter fraction,
\begin{equation}
  \Om^{\mathrm{dyn}} \;=\; 1+w_0 \;=\; \val{S_M_d6} ,""",
    r"""The equation of state~\eqref{eq:w0wa} fixes the combination
$s_m$ (earlier versions wrote it $\Omega_m^{\rm dyn}$ and called it a ``dynamical''
matter fraction; the name is withdrawn),
\begin{equation}
  s_m \;=\; 1+w_0 \;=\; \val{S_M_d6} ,""")
rep(r"""$\Om^{\mathrm{cosm}}$ to $\Om^{\mathrm{dyn}}$ through a factor-of-two bridge""",
    r"""$\Om^{\mathrm{cosm}}$ to $s_m$ through a factor-of-two bridge""")
rep(r"""drafts were the footprint of a single error---placing the cold dynamical sector
$\Om^{\mathrm{dyn}}=\val{S_M_d6}$ in the background geometry, where the total density
belongs.""",
    r"""drafts were the footprint of a single error---placing the equation-of-state
number $s_m=\val{S_M_d6}$ in the background geometry, where the total density
belongs.""")
rep(r"""$\Omega_{\varphi\rm DM}=\Omega_{m,\rm CMB}-\Omega_{m,\rm dyn}$, took a measured""",
    r"""$\Omega_{\varphi\rm DM}=\Omega_{m,\rm CMB}-s_m$, took a measured""")

# 4. P7: el campo rueda hacia w=-1; (w0,wa) no son dos proyecciones de un campo (OP-24)
rep(r"""Under the Chevallier--Polarski--Linder
parametrisation $w(a)=w_0+w_a(1-a)$, Eq.~\eqref{eq:w0wa} corresponds to an
$\alpha$-attractor scalar sector with curvature $\alpha=\varphi^4/3$ (derived
in \S\ref{sec:eft}), so the two CPL numbers are not independent fits but two
projections of a single rolling field.""",
    r"""They enter as the two numbers of the Chevallier--Polarski--Linder
parametrisation $w(a)=w_0+w_a(1-a)$. The field of Paper~7 fixes $w_0$ and the
sound speed today but not $w(a)$: it rolls towards $w=-1$, and a single canonical
field does not cross it, so the dynamical origin of $w_a$ is open (OP-24,
\S\ref{sec:eft-functions}).""")
rep(r"""The two CPL numbers are
two projections of one rolling field (\S\ref{sec:w0wa-construction}), not two
separately fitted constants, so the joint look-elsewhere is governed by a
single shared structure rather than by two free choices.""",
    r"""The two CPL numbers are
therefore not two separately fitted constants: the joint look-elsewhere is
governed by a single shared dictionary rather than by two free choices.""")

# 5. sensibilidad a rho sin log: fuera (se usa la rho medida)
rep(r"""The result
is robust to the correlation ($\rho\in[-0.92,-0.70]$ would shift the
Pantheon+ figure by $<0.2\sigma$; the measured value is used).""",
    r"""The correlation is the one measured from the chains, not an assumed value.""")

# 6. a mano -> macro
rep(r"""land on $|w_0|=\val{S_DE_d6}$ and on $|w_a|=0.669975$?""",
    r"""land on $|w_0|=\val{S_DE_d6}$ and on $|w_a|=\val{WA_abs_d6}$?""")
rep(r"""  |w_a|=0.669975:\ \text{1 of 490}\quad(\pm0.0005).""",
    r"""  |w_a|=\val{WA_abs_d6}:\ \text{1 of 490}\quad(\pm0.0005).""")
rep(r"""$\mathrm{SOLAR}/\mathrm{NYX}=\val{SOLAR_NYX_d5}$, which sits $|d|=6.4\times10^{-4}$ from
$|w_a|=\mathrm{PYROS}/\mathrm{IGNIS}=0.669975$.""",
    r"""$\mathrm{SOLAR}/\mathrm{NYX}=\val{SOLAR_NYX_d5}$, which sits $|d|=\val{solarnyx_d}$ from
$|w_a|=\mathrm{PYROS}/\mathrm{IGNIS}=\val{WA_abs_d6}$.""")
rep(r"""  |w_a|=\frac{\mathrm{PYROS}}{\mathrm{IGNIS}}=\frac{P_{\rm sc}}{\pi+P_{\rm sc}}=0.669975 .""",
    r"""  |w_a|=\frac{\mathrm{PYROS}}{\mathrm{IGNIS}}=\frac{P_{\rm sc}}{\pi+P_{\rm sc}}=\val{WA_abs_d6} .""")
rep(r"""$\omega_\nu=\Sigma m_\nu^{\rm active}/C_\nu=0.06849/93.14=0.000735$, using the
same active-neutrino sum $\Sigma m_\nu^{\rm active}=0.06849$~eV and the same""",
    r"""$\omega_\nu=\Sigma m_\nu^{\rm active}/C_\nu=\val{OMEGA_NU_H2_d6}$, using the
same active-neutrino sum $\Sigma m_\nu^{\rm active}=\val{SUM_MNU_EV_d5}$~eV and the same""")
# la cadena de Sigma m_nu vive en P4 (y P1), no en P6
rep(r"""$R_2=\Omega/(\mathrm{KAL_0}T_r)$ (Paper~6).""",
    r"""$R_2=\Omega/(\mathrm{KAL_0}T_r)$ (Paper~4).""")
rep(r"""  \quad (h=H_0^{\rm glob}/100=0.67962).""",
    r"""  \quad (h=H_0^{\rm glob}/100).""")
# el 0.6 % estaba mal: el log da 0.5 %
rep(r"""The neutrino piece is not optional: dropping it returns $0.30729$, a $0.6\%$
shift,""",
    r"""The neutrino piece is not optional: dropping it returns $\val{Om_sin_nu_d5}$, a $\val{Om_sin_nu_pct}\%$
shift,""")
rep(r"""$H_0=\val{h0_p2}\pm\val{h0_p2_s}~\kms$ and $\Omega_b h^2 = \val{p2_obh2}\pm0.00048$""",
    r"""$H_0=\val{h0_p2}\pm\val{h0_p2_s}~\kms$ and $\Omega_b h^2 = \val{p2_obh2}\pm\val{p2_obh2_s}$""")
rep(r"""$r=\varphi^{-10}$             & Inflation         & $8.1\times10^{-3}$              & P1     & \textbf{Prediction} \\""",
    r"""$r=\varphi^{-10}$             & Inflation         & $\val{r_tensor_mil_d1}\times10^{-3}$              & P1     & \textbf{Prediction} \\""")
rep(r"""$\gamma_{\rm IS}$ (Israel--Stewart) & Growth      & $0.550$                         & P5     & Retrodiction \\""",
    r"""$\gamma_{\rm IS}$ (Israel--Stewart) & Growth      & $\val{p3_gamma_IS}$                         & P5     & Retrodiction \\""")
rep(r"""value, $r\simeq8.1\times10^{-3}$, lies squarely""",
    r"""value, $r\simeq\val{r_tensor_mil_d1}\times10^{-3}$, lies squarely""")
rep(r"""predicts $n_s=\val{N_S_d6}$ and $r=8.1\times10^{-3}$;""",
    r"""predicts $n_s=\val{N_S_d6}$ and $r=\val{r_tensor_mil_d1}\times10^{-3}$;""")
rep(r"""(TT+TE+EE, $613$ bandpowers, nuisance parameters marginalised by the Planck
Collaboration) together with the low-$\ell$ TT and EE likelihoods, for $N=669$""",
    r"""(TT+TE+EE, $613$ bandpowers, nuisance parameters marginalised by the Planck
Collaboration) together with the low-$\ell$ TT and EE likelihoods, for $N=\val{lite_N}$""")

# 7. P10: M es condicional a la Conjetura C.1 (la cascada no mide M^4)
rep(r"""$M=(5\varphi^8\rho_{\rm crit})^{1/4}$ & UV compl.  & $9.68\,$meV                    & P10    & Derived (UV) \\""",
    r"""$M=(5\varphi^8\rho_{\rm crit})^{1/4}$ & UV compl.  & $\val{M_meV_d2}\,$meV                    & P10    & Conditional (Conj.~C.1) \\""")
rep(r"""(conditional on the derivation of $M^4=5\varphi^8\rho_{\rm crit}$ from UV--IR
$\varphi/\pi$ separability, Postulate~C.1),""",
    r"""(with the cutoff $M^4=5\varphi^8\rho_{\rm crit}$ of Conjecture~C.1; the cascade is
consistent with that cutoff but does not measure it),""")
rep(r"""The leftover, $4\times10^{-6}~\kms$, lies below""",
    r"""The leftover, $\val{p9_hglob_residuo}~\kms$, lies below""")

# 8. el ancla no es «CMB-optimal»: es la salida de la cascada SH0ES
rep(r"""We first anchor the
early-time geometry at the CMB-optimal value""",
    r"""We first anchor the
early-time geometry at the output of the screening cascade""")
# f_screen: la forma multiplicativa es el postulado de P9
rep(r"""and de-screen it with
the algebraically-derived (not fit) fraction""",
    r"""and, under the screening postulate of Paper~9 (the correction acts only on
locally measured rates), de-screen it with the algebraically-derived (not fit) fraction""")
# chi2_BAO = 10.43 en el posterior: sin log
rep(r"""away ($\chi^2_{\rm BAO}=10.43$ over 13 points at the posterior, $\val{desi_clav_ssee}$ at the
anchor, against $\simeq726$ for the incorrect background geometry)""",
    r"""away ($\chi^2_{\rm BAO}=\val{desi_clav_ssee}$ over $\val{desi_N}$ points at the
anchor, against $\simeq726$ for the incorrect background geometry)""")

# 9. P2: el titular es k=0; la tabla con H0 y omega_b muestreados es la conservadora
rep(r"""SSEE is favoured over both $\Lambda$CDM ($\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm_abs}$) and CPL
($\val{p2_dBIC_cpl_abs}$) by parsimony,""",
    r"""This is the conservative version: it lets SSEE sample $H_0$ and $\Omega_b h^2$ and
charges it $k=2$ for them, although $\omega_b$ is algebraic and $H_0$ is the output of
the cascade. Evaluated at its algebraic point with nothing free ($k=0$), SSEE is
favoured by $\Delta\mathrm{BIC}(\text{SSEE}-\text{model})=\val{p2_k0_dBIC_lcdm}$ over $\Lambda$CDM and
$\val{p2_k0_dBIC_cpl}$ over CPL (Paper~2); freeing $H_0$ and $\Omega_b h^2$ lowers $\chi^2$ by only
$\val{p2_k0_dchi2}$. In the conservative version
SSEE is favoured over both $\Lambda$CDM ($\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm_abs}$) and CPL
($\val{p2_dBIC_cpl_abs}$) by parsimony,""")
rep(r"""\caption{Bayesian model comparison on DESI~DR2 ($100$ walkers $\times\,25{,}000$
steps). $\Delta$ values are relative to SSEE; positive favours SSEE.}""",
    r"""\caption{Bayesian model comparison on DESI~DR2 BAO with the compressed Planck prior
($100$ walkers $\times\,25{,}000$ steps), conservative version with $H_0$ and
$\Omega_b h^2$ sampled in SSEE. $\Delta$ values are relative to SSEE; positive favours
SSEE. With nothing free ($k=0$) the preference grows (text).}""")

# 10. s_K: la definición de P9 (signo y w fijo)
rep(r"""  s_K \equiv -\frac{1}{\rho_\phi}\frac{dp_\phi}{dN} = -3w_0(1+w_0)
      = 3\,s_{\rm DE}\,s_m = \val{S_K_d6} ,
  \label{eq:sK_sealed}
\end{equation}
%
the fractional dilution rate of the dark-energy \emph{pressure} per e-fold.""",
    r"""  s_K \equiv -\frac{1}{\rho_\phi}\frac{d|p_\phi|}{dN}\bigg|_{w=w_0} = -3w_0(1+w_0)
      = 3\,s_{\rm DE}\,s_m = \val{S_K_d6} ,
  \label{eq:sK_sealed}
\end{equation}
%
the fractional dilution rate of the dark-energy \emph{pressure} per e-fold,
evaluated with $w_0$ held fixed: the term from the evolution of $w(a)$ is not part
of $s_K$, which is a number of the algebra rather than the full rate (Paper~9).""")

# 11. r < 0.036 es BICEP/Keck 2021; LiteBIRD con su cita
rep(r"""the current bound $r<0.036$ and within reach of LiteBIRD and CMB-S4.""",
    r"""the current bound $r<0.036$~\citep{BICEPKeck2021} and within reach of
LiteBIRD~\citep{LiteBIRD2023} and CMB-S4.""")

# 12. la tabla CMB es CAMB (pipeline de P3); los picos, CLASS
rep(r"""we computed the CMB angular power spectra with the
\texttt{CLASS} Boltzmann code~\citep{Lesgourgues2011} and compared against
Planck 2018~\citep{PlanckLikelihood2020} (TT, TE, EE and lensing).""",
    r"""we computed the CMB angular power spectra with \texttt{CAMB}~\citep{Lewis2000}
(the Paper~3 pipeline) and compared against Planck
2018~\citep{PlanckLikelihood2020} (TT, TE, EE and lensing); the peak positions
are cross-checked with \texttt{CLASS}~\citep{Lesgourgues2011}.""")

# 13. P4 no usa soberanías
rep(r"""(a Sovereign
convergence coinciding in value with $3\Omega$)""",
    r"""(a convergence coinciding in value with $3\Omega$)""")

# 14. trayectoria DR1 -> DR2 sin log: fuera
rep(r"""The trajectory to date: against the legacy DR1 posterior the
point sat at ${\sim}0.05\sigma$; against DR2,
whose uncertainties are ${\sim}40\%$ tighter, it sits at $\val{p2_w0wa_ssee_ec26}\sigma$
(Pantheon+; \S\ref{sec:desi-agreement})---the contour shrank and the fixed
point stayed inside the $68\%$ region, which a fitted model can always do but
a rigid one need not.""",
    r"""Against DR2 it sits at $\val{p2_w0wa_ssee_ec26}\sigma$
(Pantheon+; \S\ref{sec:desi-agreement}), inside the $68\%$ region, which a fitted
model can always arrange but a rigid one need not.""")

open(P, "w").write(s)
print("PRD editado")
