#!/usr/bin/env python3
"""P8, quinta lectura (2026-10-12): lo que la lectura encontró, con su porqué en notes/lectura_quinta/P8.md."""
import sys

P = "manuscript/SSEE_Paper8_StrongGravity.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


FF = (r"$F_\phi/F_N\sim\val{quinta_fuerza_Mpc}$ at $1\,\mathrm{Mpc}$ and "
      r"$\sim\val{quinta_fuerza_10kpc}$ at the $10\,\mathrm{kpc}$ scale of galaxy Einstein radii,")

# 1. quinta fuerza sub-Mpc: la cifra salía de la ec. fifth_force_qs a escala de kpc, no «sub-Mpc»
rep(r"""fifth-force is suppressed to $F_\phi/F_N\sim 10^{-15}$ at sub-Mpc scales and""",
    r"""fifth-force is suppressed to """ + FF + r""" and""")
rep(r"""        the residual fifth-force is suppressed to $F_\phi/F_N\sim 10^{-15}$
        at sub-Mpc scales.""",
    r"""        the residual fifth-force is suppressed to """ + FF + r""".""")

# 2. βc no lo fija Paper 7 (el acoplamiento conforme salió de P7); las constantes son de Paper 1
rep(r"""where $\bc \equiv \AURA = (3\phiG+\pi)/2$ is the disformal coupling
constant fixed in Paper~7.""",
    r"""where $\bc \equiv \AURA = (3\phiG+\pi)/2$ is the disformal coupling
constant of this paper (Section~\ref{sec:eft}; Paper~7 carries no coupling).""")
rep(r"""The algebraic constants fixed by $\phiG$ and $\pi$ (Paper~7) are:
\begin{align}
  \KAL    &= \beta + \pi = \frac{\phiG+\pi}{2} + \pi \approx 5.521\,,
              \label{eq:KAL}\\
  \bc \equiv \AURA &= \frac{3\phiG+\pi}{2} \approx 3.998\,,""",
    r"""The algebraic constants fixed by $\phiG$ and $\pi$ (Paper~1) are:
\begin{align}
  \KAL    &= \beta + \pi = \frac{\phiG+\pi}{2} + \pi \approx \val{KAL0_d3}\,,
              \label{eq:KAL}\\
  \bc \equiv \AURA &= \frac{3\phiG+\pi}{2} \approx \val{AURA_d3}\,,""")

# 3. M: Paper 10 lo fija (bajo su Postulado C.1); aquí ningún resultado depende de M
rep(r"""  M       &\approx \Mpl\quad\text{(free EFT parameter; we adopt $M=\Mpl$ as reference)}\,.""",
    r"""  M       &= \phiG^2\,5^{1/4}\,\rhoc^{1/4} \approx \val{M_meV_d2}\,\mathrm{meV}
              \quad\text{(Paper~10, conditional on its Postulate~C.1)}\,.""")
rep(r"""This mechanism operates independently of the value of $M$ and holds in both the
IR ($M = \Mpl$) and UV ($M = 9.68\,\mathrm{meV}$) limits.""",
    r"""This mechanism operates independently of the value of $M$: it holds in the
IR limit $M\to\infty$ and at the Paper~10 value $M = \val{M_meV_d2}\,\mathrm{meV}$ alike.""")

# 4. a mano -> macro
rep(r"""% ORIGEN-VALOR: 44.15 — algebra: 2*KAL0*AURA = 2 x 5.521350 x 3.997847 = 44.147 (beta_c = +AURA, el acoplamiento disforme de este paper)
$2\KAL\,\bc \approx 2\times5.521\times3.998 \approx 44.15$.""",
    r"""$2\KAL\,\bc \approx 2\times\val{KAL0_d3}\times\val{AURA_d3} \approx \val{p8_grad_coef}$.""")
rep(r"""$G_{\mathrm{eff}}/G = 1 + 2\KAL\bc^2 \approx 1 + 2(5.521)(3.998)^2
\approx 177$.""",
    r"""$G_{\mathrm{eff}}/G = 1 + 2\KAL\bc^2 \approx 1 + 2(\val{KAL0_d3})(\val{AURA_d3})^2
\approx \val{p8_Geff}$.""")
rep(r"""the baryonic seed $M_{\mathrm{bary}}$, and $\bc \approx 3.998$ is the""",
    r"""the baryonic seed $M_{\mathrm{bary}}$, and $\bc \approx \val{AURA_d3}$ is the""")
rep(r"""$\sqrt{\bc}=\sqrt{\mathcal{A}}\approx1.9995$, above it""",
    r"""$\sqrt{\bc}=\sqrt{\mathcal{A}}\approx\val{sqrt_AURA_d4}$, above it""")
rep(r"""        suppressing any residual fifth force to $F_\phi/F_N \sim 10^{-31}$
        at solar-system scales.""",
    r"""        suppressing any residual fifth force to $F_\phi/F_N \sim \val{quinta_fuerza_AU}$
        at solar-system scales.""")
rep(r"""($X_{\rm bg}^2/M^4 \approx 5.7\times10^{-4}$, Paper~10~\citep{SSEE10}),""",
    r"""($X_{\rm bg}^2/M^4 \approx \val{eps_UV}$ in units $\rhoc=1$, Paper~10~\citep{SSEE10}),""")

# 5. erratas
rep(r"""component). This is \emph{not} the canonical SSEE model. The canonical
canonical limit""",
    r"""component). This is \emph{not} the canonical SSEE model. The canonical
limit""")
rep(r"""the cantidad that emerges is""", r"""the quantity that emerges is""")

# 6. la «recurrencia de MIRA» en el lensing: OP-13 la retiró y la propia Discusión dice
#    que MIRA aparece en un solo sitio (Paper 9)
rep(r"""Therefore, to within $0.03\%$, the lensing amplification factor coincides
with the CMB horizon mapping factor:
\begin{equation}
  \thetaE^{\mathrm{SSEE}} \;\approx\; \MIRA \times \thetaE^{\mathrm{GR}}\,,
  \label{eq:thetaE_mira}
\end{equation}
where the same $\MIRA$ (the ``Mirror Ratio'') appears in:
\begin{itemize}
  \item Paper~9: the Hubble screening fraction $f_{\rm scr}^{\rm IR} = s_K^{\rm IR}/(3\,\MIRA) = (\pi-\varphi)/\Omega^2$
  \item This paper: $\thetaE^{\mathrm{SSEE}} \approx \MIRA \times \thetaE^{\mathrm{GR}}$
\end{itemize}
(Under the $\omega_m$-direct reframe, OP-8 dissolved, $\MIRA$ no longer enters
the CMB matter sector: $\Omega_{m,\mathrm{CMB}}=\omega_m/h^2=\val{OMEGA_M_TOTAL_d6}$ with no
matter factor, and $r_d=\val{p2_lyaB_rd}$\,Mpc follows directly from $\omega_m$, both
superseding the earlier MIRA-mapped forms.)

This recurrence of $\MIRA$ across the Hubble-screening and
strong-lensing sectors reflects a single structural input: $\MIRA$ is fixed
algebraically by $\phiG$ and $\pi$, not tuned. The lensing entry holds at the
$0.03\%$ level through the near-coincidence $\sqrt{\bc}\approx\MIRA$
(Section~\ref{sec:mira}), not as an exact identity.""",
    r"""Therefore, to within $0.03\%$, the limit-(a) lensing factor is numerically
close to $\MIRA$,
\begin{equation}
  \thetaE^{\mathrm{SSEE}} \;\approx\; \MIRA \times \thetaE^{\mathrm{GR}}\,,
  \label{eq:thetaE_mira}
\end{equation}
but this is a near-coincidence, not a second appearance of $\MIRA$. $\MIRA$
enters the framework in one place only, the Hubble screening amplitude of
Paper~9, $f_{\rm scr}^{\rm IR} = s_K^{\rm IR}/(3\,\MIRA)$
(Section~\ref{sec:discussion}); under the $\omega_m$-direct reframe (OP-8
dissolved) it no longer enters the CMB matter sector either:
$\Omega_{m,\mathrm{CMB}}=\omega_m/h^2=\val{OMEGA_M_TOTAL_d6}$ with no matter factor, and
$r_d=\val{p2_lyaB_rd}$\,Mpc follows directly from $\omega_m$. An earlier version read
the near-coincidence as a recurrence of $\MIRA$ across the screening and
lensing sectors; that reading is withdrawn (OP-13), and in the canonical
limit neither $\sqrt{\AURA}$ nor $\MIRA$ enters the Einstein radius.""")

# 7. la tabla atribuía a SSEE M_dyn/M_lens > 1; el canónico predice ≈ 1 (ítem 3)
rep(r"""$M_{\mathrm{dyn}}/M_{\mathrm{lens}}$ ratio
  & 1 (GR)
  & $> 1$ (fifth force on DM)
  & Linear regime \\""",
    r"""$M_{\mathrm{dyn}}/M_{\mathrm{lens}}$ ratio
  & 1 (GR)
  & 1 ($\mu-1=0$; $>1$ only in limit~(a))
  & All \\""")

# 8. S8: el titular es KiDS-Legacy con A_s clavado; KiDS-1000 es el antecedente
rep(r"""        free-streaming species to look for. The growth-sector falsifier is now
        the shear amplitude itself, $S_8=\val{S8_k1000_ssee}\pm\val{S8_k1000_ssee_sigma}$\footnote{Updated 2026-09-20. Against the later \textsc{KiDS-Legacy} release (357 raw $\xi_\pm$ points; Wright et al.\ 2025, arXiv:2503.19441 --- published sixteen months before this analysis, over which no temporal priority is claimed) the amplitude the shear asks for lies $0.49\sigma$ from the one the CMB fixes under the \emph{same} algebraic background, so $A_s$ need not be free either: fixed to that value, the growth sector carries \emph{no} free cosmological parameter and predicts $S_8=\val{S8_leg_pred}$ against $\val{S8_legacy_dato}\pm\val{S8_legacy_dato_sigma}$ measured. The three $\chi^2$ compared span $1.0$ over 357 points, so the shear does \emph{not} discriminate between the models; what separates them is the parameter count. See Paper~6.} against raw
        KiDS-1000 $\xi_\pm$ data.""",
    r"""        free-streaming species to look for. The growth-sector falsifier is now
        the shear amplitude itself. Against the 357 raw $\xi_\pm$ points of
        \textsc{KiDS-Legacy} (Wright et al.\ 2025, arXiv:2503.19441, published
        sixteen months before this analysis; no temporal priority is claimed),
        the amplitude the shear asks for lies $0.49\sigma$ from the one the CMB
        fixes under the \emph{same} algebraic background, so $A_s$ is fixed to
        that value: the growth sector then carries \emph{no} free cosmological
        parameter and predicts $S_8=\val{S8_leg_pred}$ against
        $\val{S8_legacy_dato}\pm\val{S8_legacy_dato_sigma}$ measured. The three $\chi^2$
        compared span $1.0$ over 357 points, so the shear does \emph{not}
        discriminate between the models; what separates them is the parameter
        count (Paper~6). Against the earlier KiDS-1000 release, with $A_s$
        free, $S_8=\val{S8_k1000_ssee}\pm\val{S8_k1000_ssee_sigma}$.""")

# 9. M de Paper 10: condicional a su Postulado C.1
rep(r"""Paper~10 of the SSEE series derives
$M^4 = 45\alpha^2\,\rhoc = 5\phiG^8\,\rhoc$ from the inflationary $\alpha$-attractor
parameter $\alpha = \phiG^4/3$, fixing
\begin{equation}
  M \;=\; \phiG^2\,5^{1/4}\,\rhoc^{1/4} \;\approx\; 9.68\;\mathrm{meV}
\end{equation}
algebraically without free parameters.""",
    r"""Paper~10 of the SSEE series obtains
$M^4 = 45\alpha^2\,\rhoc = 5\phiG^8\,\rhoc$ from the inflationary $\alpha$-attractor
parameter $\alpha = \phiG^4/3$, fixing
\begin{equation}
  M \;=\; \phiG^2\,5^{1/4}\,\rhoc^{1/4} \;\approx\; \val{M_meV_d2}\;\mathrm{meV}
\end{equation}
with no free parameter, conditional on its Postulate~C.1 (UV--IR separability).
None of the results of this paper depends on that value.""")

# 10. conclusiones: el resultado canónico es GR con materia oscura; el límite (a) es contraste
rep(r"""  \item \textbf{Gradient closure}: In the quasi-static limit, the scalar
        field profile tracks the Newtonian potential via
        $\nabla\phi = 2\KAL\bc\Mpl\,\nabla\Phi_N$, with
        $\KAL \approx 5.521$ and $\bc \approx 3.998$ fixed algebraically.

  \item \textbf{Lensing amplification}: The total deflection angle is
        amplified by $\bc$ relative to the GR baryonic-mass prediction,
        yielding $\thetaE^{\mathrm{SSEE}} \approx \sqrt{\bc} \approx \MIRA$
        times the GR Einstein radius.

  \item \textbf{MIRA emergence}: The structural constant
        $\MIRA = (3\phiG+\pi)/4 \approx \val{MIRA_d4}$, which enters the Hubble
        screening amplitude of Paper~9, also matches the lensing
        amplification of the alternative limit to within $0.03\%$ (via the
        near-coincidence $\sqrt{\bc} \approx \MIRA$). The former ``two-sector
        mass ratio'' reading is withdrawn with the partition.""",
    r"""  \item \textbf{Canonical lensing}: With real cold dark matter
        ($\omega_c=\KAL\,\omega_b\,n_s$) and $\alpha_B=\alpha_M=\alpha_T=0$ from
        Paper~7, $\mu-1=0$ and the Einstein radius is that of GR with a
        dark-matter halo at all scales. For A1689 this gives $42.6''$ against
        the observed $45''$.

  \item \textbf{The alternative limit as a contrast}: In the limit-(a)
        extension the scalar gradient tracks the Newtonian one,
        $\nabla\phi = 2\KAL\bc\Mpl\,\nabla\Phi_N$ with $\KAL \approx \val{KAL0_d3}$ and
        $\bc \approx \val{AURA_d3}$, and the Einstein radius is
        $\sqrt{\bc}=\sqrt{\AURA}\approx\val{sqrt_AURA_d4}$ times the baryonic GR one.
        A1689 rejects it by a factor $\approx 1.9$.

  \item \textbf{No MIRA in lensing}: $\sqrt{\AURA}$ lies within $0.03\%$ of
        $\MIRA = \AURA/2$ only because $\AURA\approx4$; it is a different
        operation, and $\MIRA$ enters the framework only through the Hubble
        screening amplitude of Paper~9. The former ``two-sector mass ratio''
        reading is withdrawn with the partition.""")
rep(r"""        suppresses any residual fifth force to $F_\phi/F_N \sim 10^{-31}$
        at $1\,\mathrm{AU}$ (Section~\ref{sec:double_protection}).""",
    r"""        suppresses any residual fifth force to $F_\phi/F_N \sim \val{quinta_fuerza_AU}$
        at $1\,\mathrm{AU}$ (Section~\ref{sec:double_protection}).""")
rep(r"""regime into the non-linear strong-gravity regime, while maintaining the
zero-free-parameter structure of the algebraic framework.""",
    r"""regime into the non-linear strong-gravity regime without adding a free
parameter: the framework's free parameters remain $\{A_s,\tau\}$ (Paper~1).""")

# 11. bibliografía: títulos reales
BIB = {
    r"""  \textit{SSEE: Structural Self-Energy Expansion --- Framework,
  Algebraic Constants, and $\alpha$-Attractor Embedding}.""":
    r"""  \textit{A Minimal-Parameter Framework for Cosmological Dynamics and Galaxy
  Cluster Mass Discrepancies via Structural Self-Energy Expansion (SSEE)}.""",
    r"""  \textit{SSEE: Bayesian Validation Against DESI DR2, Planck, and
  Galaxy Clusters}.""":
    r"""  \textit{Bayesian MCMC Validation of the Structural Self-Energy Expansion
  Framework (SSEE): Model Comparison against $\Lambda$CDM and CPL using
  DESI~DR2, Planck~2018, and Galaxy-Cluster Mass Data}.""",
    r"""  \textit{SSEE: CMB Confrontation with Planck 2018 via CAMB and CLASS}.""":
    r"""  \textit{SSEE and the CMB Power Spectrum: Acoustic Peak Reproduction via
  the $\omega_m$-Direct CMB Matter Density}.""",
    r"""  \textit{SSEE: Nine Sovereignties --- Algebraic Derivation of CMB
  Observables from $\varphi$ and $\pi$}.""":
    r"""  \textit{Structural Self-Energy Expansion as a Two-Axiom Cosmology:
  Algebraic Derivation of the CMB Background from $\varphi$ and $\pi$}.""",
    r"""  \textit{SSEE: Israel--Stewart Causal Perturbations and the
  $f\sigma_8$ Tension}.""":
    r"""  \textit{Israel--Stewart Causal Viscous Perturbations in the SSEE Dark
  Energy Framework: Stability from the Field, Weak Dark-Energy Clustering, and
  $\Lambda$CDM-Consistent Structure Growth}.""",
    r"""  \textit{SSEE as a Working Effective Field Theory: $K$-essence Action,
  Algebraic Coupling, and Bellini-Sawicki Classification}.""":
    r"""  \textit{The SSEE Dark-Energy Sector as a Ghost Condensate: Two-Term
  K-essence, Algebraic Sound Speed, and Bellini--Sawicki Classification}.""",
    r"""  \textit{SSEE UV Completion: $M^4 = 45\alpha^2\rho_{\rm crit}$ and
  the Cross-Epoch Hubble Tension Resolution}.""":
    r"""  \textit{UV Extension of SSEE Dark Energy: $M^4 = 45\alpha^2\rho_{\rm crit}
  = 5\varphi^8\rho_{\rm crit}$ and a Conditional Self-Consistency Check on the
  Hubble Tension}.""",
}
for a, b in BIB.items():
    rep(a, b)

open(P, "w").write(s)
print("P8: quinta lectura aplicada")
