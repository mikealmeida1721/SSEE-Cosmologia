#!/usr/bin/env python3
"""Quinta lectura P5, segunda pasada (2026-10-11): lo que salió al releer el PDF
después de edita_P5.py. Reemplazos exactos; aborta si un conteo no casa."""
import sys

P = "manuscript/SSEE_Paper5_IS.tex"
s = open(P).read()


def rep(old, new, n=1, txt=None):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


rep(r"""Exact Marginal Stability, $\Lambda$CDM-Consistent Structure Growth,\\
and the Amplitude Ceiling}}""",
    r"""Stability from the Field, Weak Dark-Energy Clustering,\\
and $\Lambda$CDM-Consistent Structure Growth}}""")
rep(r"""negative
bare sound speed $c^2_{s,\mathrm{bare}} = w_0 \simeq -0.840$, implying catastrophic""",
    r"""negative
bare sound speed $c^2_{s,\mathrm{bare}} = w_0 = \val{W0_d6}$, implying catastrophic""")
rep(r"""The marginal-stability result
$c^2_{s,\rm eff} = \wz + \sDE = 0$ is therefore \emph{independent of}""",
    r"""The high-frequency result
$c^2_{s,\rm eff} = \wz + \sDE = 0$ is therefore \emph{independent of}""")
rep(r"""\subsection{The Israel-Stewart resolution}""",
    r"""\subsection{The Israel--Stewart layer}""")
rep(r"""Both conditions are satisfied in SSEE (established in Section~\ref{sec:Q1_stability}).""",
    r"""Both conditions are satisfied in SSEE (Section~\ref{subsec:thermodynamic}).""")
rep(r"""an option. The two operative appendices of this paper both require the other
convention.""",
    r"""an option. The dispersion appendix of this paper requires the other convention.""")
rep(r"""Two further reasons agree: it is what both appendices of
this paper uses, and it is the form consistent with relativistic""",
    r"""Two further reasons agree: it is what the dispersion appendix of
this paper uses, and it is the form consistent with relativistic""")
rep(r"""\subsection{Marginal stability under minimality}""",
    r"""\subsection{The high-frequency identity}""")
rep(r"""The linear growth factor $D_1(a)$ satisfies, in the sub-horizon limit with
IS-suppressed DE perturbations ($\delta_{\mathrm{DE}} \approx 0$):""",
    r"""The linear growth factor $D_1(a)$ satisfies, in the sub-horizon limit with
dark-energy perturbations neglected ($|\delta_{\mathrm{DE}}/\delta_m|\leq\val{q2_r_k3}$ for
$k\geq10\,H_0/c$, Section~\ref{sec:Q2_MIRA}):""")
rep(r"""Future Stage IV surveys (DESI full shape, Euclid) measuring $f\sigma_8(z)$ at
the $1\%$ level will not distinguish SSEE from $\Lambda$CDM via the growth rate alone.""",
    r"""Differences of this size are at the edge of what Stage IV surveys (DESI full
shape, Euclid) will resolve in $f\sigma_8(z)$.""")
rep(r"""field's sound speed, they remain finite:
$|\delta_{\rm DE}/\delta_m| = |\val{p5_cruce_r_k2}|$ at $k=2\,H_0/c$ and
$|\val{p5_cruce_r_k10}|$ at $k=10\,H_0/c$ at $z=0$.""",
    r"""field's sound speed, they remain finite:
$\delta_{\rm DE}/\delta_m = \val{p5_cruce_r_k2}$ at $k=2\,H_0/c$ and
$\val{p5_cruce_r_k10}$ at $k=10\,H_0/c$ at $z=0$.""")
# estructura del paper (§1.4)
i = s.index(r"""Section~\ref{sec:theory} derives the IS perturbation equations from the entropy""")
j = s.index(r"""%======================================================================
\section{Israel-Stewart Theory for SSEE Dark Energy}""")
s = s[:i] + r"""Section~\ref{sec:theory} sets out the IS equations, the normalisation of the
viscosity, and why the quasi-static reduction is the Navier--Stokes limit.
Section~\ref{sec:Q1_stability} separates the high-frequency identity from stability
and shows that the growing branch of the closure $c^2_s=w$ survives the viscosity,
while the field's sound speed removes it. Section~\ref{sec:Q2_MIRA} measures
dark-energy clustering with the full IS system, including the passage through the
phantom crossing. Section~\ref{sec:growth} gives the growth index, $\sigma_8$ and $S_8$.
Section~\ref{sec:EFT} places the IS layer in the EFT-of-dark-energy language,
Section~\ref{sec:discussion} discusses implications and collects the falsifiable
predictions, and Section~\ref{sec:conclusions} concludes. Appendix~\ref{app:dispersion}
derives the dispersion relation and Appendix~\ref{app:eigenvalues} gives the
eigenvalues of the integrated system.

""" + s[j:]
open(P, "w").write(s)

# figura 1 (script)
F = "src/p05_IS/ssee_paper5_IS_perturbations.py"
f = open(F).read()
for a, b in [("label=rf'$r^*={r_MIRA:.3f}$ (MIRA target)')", "label=rf'$r^*={r_MIRA:.3f}$ (former MIRA target)')"),
             ("ax.set_title('DE Perturbation Growth\\n(IS causal regularization)')",
              "ax.set_title('DE Perturbation Growth\\n(full IS, field $c^2_s$)')")]:
    if f.count(a) != 1:
        sys.exit(f"figura: {a}")
    f = f.replace(a, b)
open(F, "w").write(f)

# bibliografía: títulos reales de los papers hermanos
B = "manuscript/ssee_paper5.bib"
b = open(B).read()
for a, c in [
    ("""  title   = {A Zero-Parameter Framework for Cosmological Dynamics and Galaxy Cluster
             Mass Discrepancies via Structural Self-Energy Expansion ({SSEE})},""",
     """  title   = {A Minimal-Parameter Framework for Cosmological Dynamics and Galaxy Cluster
             Mass Discrepancies via Structural Self-Energy Expansion ({SSEE})},"""),
    ("""  title   = {Bayesian Validation of the {SSEE} Framework against
             {DESI DR2}, {Planck 2018}, and Galaxy Cluster Data},""",
     """  title   = {Bayesian {MCMC} Validation of the Structural Self-Energy Expansion
             Framework ({SSEE}): Model Comparison against {$\\Lambda$CDM} and {CPL}
             using {DESI DR2}, {Planck 2018}, and Galaxy-Cluster Mass Data},"""),
    ("""  title   = {{CMB} Planck {PR4} Confrontation of the {SSEE} Dark Energy Framework},""",
     """  title   = {{SSEE} and the {CMB} Power Spectrum: Acoustic Peak Reproduction via the
             $\\omega_m$-Direct {CMB} Matter Density},"""),
    ("""  title   = {Algebraic Derivation of {CMB} Parameters from $\\varphi$ and $\\pi$:
             The Nine Sovereignties of {SSEE}},""",
     """  title   = {Structural Self-Energy Expansion as a Two-Axiom Cosmology: Algebraic
             Derivation of the {CMB} Background from $\\varphi$ and $\\pi$},"""),
    ("""  title   = {{UV} Completion of {SSEE}: $K(X)=X/\\mathrm{KAL}+X^2/M^4$ and the
             Cutoff $M=9.68$~meV},""",
     """  title   = {{UV} Extension of {SSEE} Dark Energy: $M^4 = 45\\alpha^2\\rho_{\\rm crit}$
             and a Conditional Self-Consistency Check on the {Hubble} Tension},"""),
]:
    if b.count(a) != 1:
        sys.exit(f"bib: {a[:60]}")
    b = b.replace(a, c)
open(B, "w").write(b)
print("P5 segunda pasada aplicada")
