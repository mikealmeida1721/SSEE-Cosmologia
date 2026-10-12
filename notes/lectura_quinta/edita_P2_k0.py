#!/usr/bin/env python3
"""P2 (2026-10-11, pregunta de Mike): SSEE con NADA libre es el titular.

ω_b es algebraico y H sale de la cascada SH0ES; {A_s, τ} no entran en BAO ni en
el prior comprimido ⟹ k = 0 en esta prueba. La versión con H0 y ω_b muestreados
queda como fila conservadora (k = 2). Log: results/logs/p2_ssee_fijo_k0.json.
"""
import sys

P = "manuscript/SSEE_Paper2_MCMC.tex"
s = open(P).read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f"conteo {c} != {n}: {old[:90]!r}")
    s = s.replace(old, new)


K0 = (r"$\Delta\mathrm{BIC}=\val{p2_k0_dBIC_lcdm}$ over \LCDM\ and $\val{p2_k0_dBIC_cpl}$ over CPL "
      r"with nothing free ($k=0$), and $\val{p2_dBIC_lcdm}$ and $\val{p2_dBIC_cpl}$ in the conservative "
      r"version that samples $H_0$ and $\Omega_b h^2$ ($k=2$)")

# resumen
rep(r"""by $\pi$ and the golden ratio $\varphi$ — with $H_0$ and $\Omega_b h^2$ as the only
sampled parameters — we compare""",
    r"""by $\pi$ and the golden ratio $\varphi$ — evaluated at its algebraic point, and
conservatively with $H_0$ and $\Omega_b h^2$ sampled — we compare""")
rep(r"""With $(w_0,w_a)$ fixed algebraically and two sampled parameters ($H_0$ and
$\Omega_b h^2$), against the same DESI~DR2 data and the same compressed Planck prior as
\LCDM\ and CPL, SSEE is favoured by $\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$ over \LCDM\ and
$\val{p2_dBIC_cpl}$ over CPL, and predicts the DESI~DR2 test set better in leave-one-out
cross-validation.""",
    r"""In this test \SSEE\ has no free parameter: $(w_0,w_a)$ and $\omega_b$ are algebraic,
$H_0$ is the output of the screening cascade, and its two free parameters $\{A_s,\tau\}$
do not enter BAO distances or the compressed prior. Against the same DESI~DR2 data and
the same compressed Planck prior as \LCDM\ and CPL, \SSEE\ at its algebraic point is
favoured by """ + K0 + r""". Freeing $H_0$ and $\Omega_b h^2$ lowers $\chi^2$ by only
$\val{p2_k0_dchi2}$: the data do not ask for them. \SSEE\ also predicts the DESI~DR2
test set better in leave-one-out cross-validation.""")

# introducción
rep(r"""$\Lambda$CDM and model selection yields a single, unambiguous figure:
$\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$ favouring SSEE over $\Lambda$CDM and $\val{p2_dBIC_cpl}$ over CPL
(Section~\ref{sec:bic}).""",
    r"""$\Lambda$CDM and model selection favours SSEE by """ + K0 + r""" (Section~\ref{sec:bic}).""")

# sección de la retractación
rep(r"""$\omega_b$ and the forward identity for $\omega_c$ hold), model selection
favours SSEE by $\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$ over \LCDM\ and $\val{p2_dBIC_cpl}$ over CPL, with
SSEE the most economical model (Section~\ref{sec:bic}).""",
    r"""$\omega_b$ and the forward identity for $\omega_c$ hold), model selection
favours SSEE by """ + K0 + r""", with SSEE the most economical model (Section~\ref{sec:bic}).""")

# comparación de modelos: tras la tabla
rep(r"""$\Delta\mathrm{DIC}=\val{p2_dDIC_lcdm}$ relative to \LCDM\ (Appendix~\ref{app:dic}). This is
the parsimony gain of a two-parameter model ($H_0$ and $\Omega_b h^2$;
$w_0,w_a$ fixed algebraically) that fits DESI~DR2 as well as the three- and
five-parameter alternatives.""",
    r"""$\Delta\mathrm{DIC}=\val{p2_dDIC_lcdm}$ relative to \LCDM\ (Appendix~\ref{app:dic}).

\paragraph{The algebraic point, with nothing free.}
Table~\ref{tab:model_comp} is the conservative version: it lets \SSEE\ sample $H_0$
and $\Omega_b h^2$ and charges it $k=2$ for them. The model does not have those
freedoms. $\omega_b=(\pi-\varphi)/[3(\varphi+\pi)^2]$ is algebraic, $H_0$ is the output
of the screening cascade ($H_0^{\rm glob}=\val{H0_GLOBAL_d3}$, Papers~9--10), and the two
free parameters of the model, $\{A_s,\tau\}$, enter neither the BAO distances nor the
compressed prior. Evaluated at that point, with $k=0$, \SSEE\ pays and earns on each
probe as follows (each model at its maximum likelihood):
\begin{center}
\begin{tabular}{lrrrrr}
\toprule
Model & $k$ & $\chi^2_{\rm BAO}$ (13) & $\chi^2_{\rm Planck}$ (3) & BIC & $\Delta$BIC (\SSEE$_{k=0}-$model) \\
\midrule
\SSEE, algebraic point & 0 & $\val{p2_k0_chi2_bao}$ & $\val{p2_k0_chi2_pl}$ & $\val{p2_k0_BIC}$ & --- \\
\SSEE, $H_0,\Omega_b h^2$ sampled & 2 & $\val{p2_max_bao_ssee}$ & $\val{p2_max_pl_ssee}$ & $\val{p2_BIC_ssee}$ & $\val{p2_k0_dBIC_libre}$ \\
\LCDM & 3 & $\val{p2_max_bao_lcdm}$ & $\val{p2_max_pl_lcdm}$ & $\val{p2_BIC_lcdm}$ & $\val{p2_k0_dBIC_lcdm}$ \\
CPL & 5 & $\val{p2_max_bao_cpl}$ & $\val{p2_max_pl_cpl}$ & $\val{p2_BIC_cpl}$ & $\val{p2_k0_dBIC_cpl}$ \\
\bottomrule
\end{tabular}
\end{center}
Freeing $H_0$ and $\Omega_b h^2$ improves the fit by $\Delta\chi^2=\val{p2_k0_dchi2}$, far
below the $2\ln 16$ it costs, so the algebraic point is where the data put \SSEE\ anyway.
On the scale of \citet{KassRaftery1995} the preference is very strong over \LCDM\ and
strong over CPL. \LCDM\ pays mainly in the Planck prior: following DESI pulls its $H_0$
and $\Omega_m$ away from the CMB values (\S\ref{sec:results_cosmo}). Script and control:
\texttt{src/p02\_mcmc/ssee\_fijo\_k0.py} (the same likelihood functions reproduce
$\ln L_{\max}$ of every chain to $10^{-6}$).""")

# conclusiones
rep(r"""    favoured on model selection by $\Delta\mathrm{BIC}=\val{p2_dBIC_lcdm}$ over \LCDM\ and
    $\val{p2_dBIC_cpl}$ over CPL, predicting the held-out BAO data better in
    cross-validation.""",
    r"""    favoured on model selection by """ + K0 + r""", predicting the held-out BAO data
    better in cross-validation.""")

open(P, "w").write(s)
print("P2: k = 0 como titular")
