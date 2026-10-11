#!/usr/bin/env python3
"""Quinta lectura P6 (2026-10-11): reemplazos exactos; aborta si un conteo no casa."""
import sys

P = "manuscript/SSEE_Paper6_Growth.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


# resumen
rep(r"""free, $\Delta\mathrm{BIC}=\val{dBIC_leg_libre}$, and the nuisance parameters do not move to""",
    r"""free, $\Delta\mathrm{BIC}=\val{dBIC_leg_libre}$ in favour of fixing it, and the nuisance parameters do not move to""")
rep(r"""sector was defined by subtracting $1+w_0\approx0.160$ --- a number of the""",
    r"""sector was defined by subtracting $1+w_0=\val{S_M_d6}$ --- a number of the""")

# introducción
rep(r"""The background sector of \SSEE{} --- the algebraic derivation of $H_0$,
$\omega_b$, $\omega_c$, $n_s$, $w_0$ and $w_a$ from $\varphi$ and $\pi$ --- has
been tested against Planck 2018, DESI DR2 BAO, and Pantheon+ in Papers~1--4,
9--10. The growth-of-structure sector --- how matter perturbations evolve once
the background is fixed --- is tested independently, against two late-time
probes: weak gravitational lensing (cosmic shear, KiDS-1000) and redshift-space
galaxy clustering (BOSS DR12). Both probes report their results as derived
quantities: KiDS-1000 publishes $S_8\equiv\sigma_8\sqrt{\Omega_m/0.3}$, and BOSS
publishes $f\sigma_8(z)$, the growth rate times the amplitude of clustering.""",
    r"""The background sector of \SSEE{} --- the algebraic derivation of $\omega_b$,
$\omega_c$, $n_s$, $w_0$ and $w_a$ from $\varphi$ and $\pi$, with the global $H_0$
the output of the SH0ES screening cascade (Papers~9--10) --- has been tested
against Planck 2018, DESI DR2 BAO, and Pantheon+ in Papers~1--4 and~9--10. The
growth-of-structure sector --- how matter perturbations evolve once the
background is fixed --- is tested independently, against two late-time probes:
weak gravitational lensing (cosmic shear: KiDS-1000 and KiDS-Legacy) and
redshift-space galaxy clustering (BOSS DR12). Both probes report their results as
derived quantities: KiDS publishes $S_8\equiv\sigma_8\sqrt{\Omega_m/0.3}$, and BOSS
publishes $f\sigma_8(z)$, the growth rate times the amplitude of clustering.""")
rep(r"""This paper re-does both measurements on the raw data products --- KiDS-1000
$\xi_\pm(\theta)$ (Asgari et al.~2021 \citep{Asgari2021}) and BOSS DR12 power-spectrum multipoles""",
    r"""This paper re-does both measurements on the raw data products --- the KiDS-1000
and KiDS-Legacy $\xi_\pm(\theta)$ (Asgari et al.~2021 \citep{Asgari2021}; Wright et
al.~2025 \citep{Wright2025}) and BOSS DR12 power-spectrum multipoles""")

# retractación: 1+w0 no es «menos la ecuación de estado»
rep(r"""by the CMB-calibrated background. $\Omega_{m,\rm dyn}=1+w_0\approx0.160050$ is,
by construction, minus the dark-energy equation of state --- an algebraic""",
    r"""by the CMB-calibrated background. $\Omega_{m,\rm dyn}=1+w_0=\val{S_M_d6}$ is,
by construction, one plus the dark-energy equation of state (the saturation
$s_m$ of Paper~1) --- an algebraic""")
rep(r"""inconsistency once both statements are read together. ($1+w_0$ is
dimensionless and is, by construction, minus the dark-energy equation of
state; the parenthetical gloss is ours, not the source comment's.)""",
    r"""inconsistency once both statements are read together. ($1+w_0$ is
dimensionless and is, by construction, one plus the dark-energy equation of
state; the parenthetical gloss is ours, not the source comment's.)""")

# diseño del test de transporte: las sondas de la tabla
rep(r"""following test (a design due to M.~Almeida): the three probes --- Planck
CMB, KiDS-1000 shear, BOSS DR12 clustering --- are combined with the shared""",
    r"""following test (a design due to M.~Almeida): the three probes --- Planck
CMB, KiDS-Legacy shear, DESI DR2 BAO --- are combined with the shared""")
rep(r"""For \SSEE{}, $\Delta\chi^2\equiv0$ by construction on every background
parameter except $A_s$: there is no ingredient to transport, because none of
$\omega_b,\omega_c,h,n_s,w_0,w_a$ are free to begin with. For $\Lambda$CDM,
$\Delta\chi^2>0$ is measured, not assumed. Results in
Table~\ref{tab:r7}.""",
    r"""For \SSEE{}, $\Delta\chi^2\equiv0$ by construction on every background
parameter: there is no ingredient to transport, because none of
$\omega_b,\omega_c,h,n_s,w_0,w_a$ are free to begin with. The one transported
quantity is $A_s$, taken from the CMB; for the CMB that is its own fit, BAO does not
depend on it, and for the shear the cost is measured (\S\ref{sec:legacy}). For
$\Lambda$CDM, $\Delta\chi^2>0$ is measured, not assumed. Results in
Table~\ref{tab:r7}.""")
rep(r"""\SSEE{}, $\Delta\chi^2$ & 0 (by construction) & 0 (by construction) & 0 (by construction) \\""",
    r"""\SSEE{}, $\Delta\chi^2$ & 0 (own fit) & $\val{dchi2_leg_unif_libre}$ (sampling noise) & 0 (no $A_s$) \\""")

# KiDS-1000: control y escala
rep(r"""(negative control: $\chi^2=\val{k1000_control_chi2}$""",
    r"""(control: $\chi^2=\val{k1000_control_chi2}$""")
rep(r"""$\Delta\mathrm{BIC}=\val{dBIC_k1000}$, both favouring \SSEE{}, the latter in the
\emph{strong} range on the Jeffreys scale.""",
    r"""$\Delta\mathrm{BIC}=\val{dBIC_k1000}$, both favouring \SSEE{}, the latter
\emph{very strong} on the scale of \citet{KassRaftery1995}.""")

# Legacy: Δχ² a mano y rango a mano
rep(r"""($-0.365$), which cannot be a true improvement""",
    r"""($\val{dchi2_leg_unif_libre}$), which cannot be a true improvement""")
rep(r"""width means any prediction between $0.809$ and $0.844$ would have agreed.""",
    r"""width means any prediction within one such width of the measured value would have agreed.""")

# BOSS: referencias internas
rep(r"""the fit, and therefore a product of the model, the same lesson $S_8$ taught in
\S\ref{sec:retraction}.""",
    r"""the fit, and therefore a product of the model, the same lesson $S_8$ taught in
\S\ref{sec:s8}.""")
rep(r"""enter the model linearly are marginalised in closed form
(\S\ref{sec:boss-method}) and $19$ are sampled.""",
    r"""enter the model linearly are marginalised analytically and $19$ are sampled.""")

open(P, "w").write(s)

B = "manuscript/ssee_paper6_growth.bib"
b = open(B).read()
if "KassRaftery1995" not in b:
    b += """
@article{KassRaftery1995,
  author  = {Kass, R. E. and Raftery, A. E.},
  title   = {Bayes Factors},
  journal = {J. Am. Statist. Assoc.},
  year    = {1995},
  volume  = {90},
  pages   = {773},
  doi     = {10.1080/01621459.1995.10476572}
}
"""
open(B, "w").write(b)
print("P6: reemplazos aplicados")
