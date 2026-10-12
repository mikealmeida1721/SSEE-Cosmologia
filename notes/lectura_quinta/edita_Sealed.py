#!/usr/bin/env python3
"""Sealed, quinta lectura (2026-10-12): las correcciones del PRD (del que es fuente) más las suyas; porqué en notes/lectura_quinta/Sealed.md."""
import sys

P = "manuscript/SSEE_Sealed_Journal.tex"
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
    r"""The equation of state~\eqref{eq:w0wa} fixes $s_m$ (written
$\Omega_m^{\rm dyn}$ in earlier versions; that name is withdrawn),
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

# ---- propias del Sealed ----
# A. la prueba look-elsewhere: el denominador de w_a es I_g (su tabla de notación), no K_v=2Omega
rep(r"""(e.g.\ $\mathrm{IGNIS}=K_v$, $\mathrm{SOLAR}=\mathrm{MAR}$, and the Sovereign
convergence at $3\Omega$)""",
    r"""(e.g.\ $\mathrm{IGNIS}$ and $K_v$, $\mathrm{SOLAR}=\mathrm{MAR}$, and the
convergence at $3\Omega$)""")
rep(r"""Both denominators are
integer multiples of the single scaffold $\Omega=\varphi+\pi$:
$K_v=2\Omega$ and $M_v=3\Omega$ to machine precision.""",
    r"""Each is an intra-lineage
ratio of the closed dictionary: $|w_0|=\mathrm{AURA}/\Omega$ is the copy-branch
root over the scaffold, and $|w_a|=\mathrm{PYROS}/\mathrm{IGNIS}$ has a
denominator generated directly from its own numerator by the no-self-sum law
($\mathrm{IGNIS}=\pi+\mathrm{PYROS}$).""")
rep(r"""(the dynamical origin of the
factor-of-two and factor-of-three bridges) remains the open mechanism tracked
in \S\ref{sec:open}.""",
    r"""(the dynamical origin of the
two lineage laws) remains the open mechanism tracked in \S\ref{sec:open}.""")
rep(r"""which sits $|d|=6.4\times10^{-4}$ from""", r"""which sits $|d|=\val{solarnyx_d}$ from""")
rep(r"""the canonical denominator
$\mathrm{IGNIS}=2\Omega$ is an integer multiple of the same scaffold that carries
$|w_0|$ ($M_v=3\Omega$), so $\mathrm{PYROS}/\mathrm{IGNIS}$ belongs to the shared
two-projection structure above, whereas $\mathrm{NYX}=(\varphi+7\pi)/2$ is the
retention-branch floor (charge $q=-3$) with no link to $|w_0|$; the selection is
therefore made by lineage, not by tolerance.""",
    r"""the canonical ratio
$\mathrm{PYROS}/\mathrm{IGNIS}$ is intra-lineage---the denominator is generated
directly from the numerator, $\mathrm{IGNIS}=\pi+\mathrm{PYROS}$, so numerator and
denominator lie on the same $\pi$-branch chain---whereas $\mathrm{SOLAR}$ and
$\mathrm{NYX}=(\varphi+7\pi)/2$ (the retention-branch floor, charge $q=-3$) share
no generative relation; their ratio is a numerical coincidence across lineages, not a
structural identity. The selection is therefore made by lineage, not by tolerance.""")
rep(r"""The same law acts on the scaffold itself, giving the denominators
$K_v=2\Omega$ and $M_v=3\Omega$. The economy noted in
\S\ref{sec:look-elsewhere} is a direct consequence: since
$T_r=3\,\mathrm{AURA}$ and $M_v=3\Omega$, the common factor of three cancels in
\begin{equation}
  |w_0|=\frac{T_r}{M_v}=\frac{3\,\mathrm{AURA}}{3\,\Omega}
        =\frac{\mathrm{AURA}}{\Omega}=\val{S_DE_d6} ,
\end{equation}
so the equation-of-state numerator and denominator are not two independent
draws but a single ratio of the two branch roots, $\mathrm{AURA}/\Omega$.""",
    r"""The denominator of $w_0$ is $M_v=\varphi+\pi+K_v$, a structural convergence built
by lineage on $K_v\,(\mathrm{KRYSTOS}=\varphi+\pi+\Omega)$; it \emph{coincides in
value} with $3\Omega$ but is not the scaffold tripled---the construction, not the
magnitude, is what fixes its identity. With the copy-law wall
$T_r=\mathrm{TRIAL}=3\,\mathrm{AURA}$ as numerator,
\begin{equation}
  |w_0|=\frac{T_r}{M_v}=\frac{\mathrm{TRIAL}}{\varphi+\pi+\mathrm{KRYSTOS}}=\val{S_DE_d6} ,
\end{equation}
which reduces \emph{numerically} to $\mathrm{AURA}/\Omega$---an identity of value
between distinct named entities, not a construction by scaffold multiples. So
$w_0$ and $w_a$ are ratios internal to the closed dictionary, not two
independent draws.""")
rep(r"""without being the same entity: by construction
$\mathrm{IGNIS}=K_v=\val{IGNIS_d6}$ (disruptive vs.\ structural lineage) and""",
    r"""without being the same entity: $\mathrm{IGNIS}=\pi+\mathrm{PYROS}$ (disruptive,
$\pi$-branch) and $K_v\,(\mathrm{KRYSTOS})=\varphi+\pi+\Omega$ (structural) both
equal $\val{IGNIS_d6}$, yet are distinct nodes; likewise""")
rep(r"""where the denominator is read as the $\pi$-branch node IGNIS rather than the
scaffold copy $K_v$---the two coincide in value by Law~II.""",
    r"""where the denominator is the $\pi$-branch node IGNIS, not the structural $K_v$,
though the two coincide in value.""")
# B. s_m
rep(r"""The dynamical fraction $\Om^{\mathrm{dyn}}=\val{S_M_d6}$ (DESI)
is not a second matter density at all""",
    r"""The equation-of-state number $s_m=\val{S_M_d6}$ (tested by DESI through $w_0$)
is not a second matter density at all""")
# C. P2: titular k=0
rep(r"""steps). $\Delta\equiv\mathrm{SSEE}-\mathrm{model}$; negative $\Delta$ favours SSEE.}""",
    r"""steps), with the compressed Planck prior; conservative version with $H_0$ and
$\Omega_b h^2$ sampled in SSEE. $\Delta\equiv\mathrm{SSEE}-\mathrm{model}$; negative $\Delta$
favours SSEE. With nothing free ($k=0$) the preference grows (text).}""")
rep(r"""SSEE is favoured over both $\Lambda$CDM ($\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$) and CPL
($\val{p2_dBIC_cpl}$) by parsimony,""",
    r"""This is the conservative version: it lets SSEE sample $H_0$ and $\Omega_b h^2$ and
charges it $k=2$ for them, although $\omega_b$ is algebraic and $H_0$ is the output of
the cascade. Evaluated at its algebraic point with nothing free ($k=0$), SSEE is
favoured by $\Delta\mathrm{BIC}=\val{p2_k0_dBIC_lcdm}$ over $\Lambda$CDM and
$\val{p2_k0_dBIC_cpl}$ over CPL (Paper~2); freeing $H_0$ and $\Omega_b h^2$ lowers $\chi^2$ by only
$\val{p2_k0_dchi2}$. In the conservative version
SSEE is favoured over both $\Lambda$CDM ($\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$) and CPL
($\val{p2_dBIC_cpl}$) by parsimony,""")
# E. Zenodo como en PRD
rep(r"""\url{https://github.com/mikealmeida1721/SSEE-Cosmologia}.""",
    r"""\url{https://github.com/mikealmeida1721/SSEE-Cosmologia} and permanently archived on Zenodo, DOI \href{https://doi.org/10.5281/zenodo.19654118}{10.5281/zenodo.19654118} (concept DOI, all versions).""")

# ---- comunes con PRD (la escala absoluta es el H medido) ----
rep(r"""\subsection{What is measured, not derived: the vacuum scale}""",
    r"""\subsection{What is measured, not derived: the absolute scale}""")
rep(r"""We have been equally explicit about its limits: the vacuum scale is a
measured input""",
    r"""We have been equally explicit about its limits: the absolute scale is a
measured input (the local expansion rate)""")

open(P, "w").write(s)
print("Sealed editado")
