"""
SSEE Paper 4 — Algebraic Derivation of CMB Background from φ and π
Reproduces: fig_toe_cmb_TT.pdf, fig_toe_derivations.pdf
Run: python3 src/ssee_paper4_toe.py
"""

import numpy as np
import matplotlib.pyplot as plt
import os

import json as _jsacta, os as _osacta, sys as _sysacta  # procedencia (R75, 2026-10-02)
_sysacta.path.insert(0, _osacta.path.dirname(_osacta.path.dirname(_osacta.path.abspath(__file__))))
from procedencia import acta as _acta, cabecera as _cabecera  # noqa: E402
_ENT_ACTA = []
print(_cabecera(__file__, entradas=_ENT_ACTA), flush=True)
# El acta va en los metadatos del PDF (Keywords): un PDF no puede llevarla como linea de texto (R75)
_META = {"Keywords": "ACTA-PROCEDENCIA " + _jsacta.dumps(_acta(__file__, entradas=_ENT_ACTA))}
# ── SSEE constants (zero free parameters) ───────────────────────────────────
import os as _reloc_os, sys as _reloc_sys  # reloc: anclar src/
_reloc_sys.path.insert(0, _reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__))))
from ssee_core import (
    PHI as phi, PI as pi, OMEGA, BETA as BIAL, AURA, MIRA,
    KAL0 as KAL, P_SC as PYROS, K_V as KRYSTOS_V, M_V as SIGMA_SOV,
    W0 as w0, WA as wa, H0_GLOBAL as H0_alg, N_S as ns,
    OMEGA_B_H2 as Omb_h2_alg, OMEGA_M_TOTAL as Om_m,   # canónico ω_m-directo 0.308881 (era GEOMETRIC 0.3201 superseded)
)
# Constantes intermedias (no presentes en ssee_core):
MAR    = phi + 2*pi                 # 7.901219
VITA   = (phi + 5*pi) / 2           # π + KAL = 8.662999  (errata del comentario corregida 2026-09-19)
PHITA  = (3*phi + 5*pi) / 2         # VITA + φ = 10.281033  (errata del comentario corregida 2026-09-19)
MIKA   = 3*phi + 2*pi               # 11.137287
# ORIGEN-VALOR: 8.662999 — (phi + 5 pi)/2 = 8.6629986
# ORIGEN-VALOR: 10.281033 — (3 phi + 5 pi)/2 = 10.2810326
# ORIGEN-VALOR: 2.285338 — 3(pi - phi)/2 = 2.2853380 (= M_v - T_r)
BUFFER = 3*(pi - phi) / 2           # 2.285338

# ── Nine Sovereignties verification ─────────────────────────────────────────
SOLAR = BIAL + KAL   # = MAR algebraically
IGNIS = pi + PYROS   # = KRYSTOS_V algebraically
MIKA_ = 3*phi + 2*pi

sovereignties = {
    "LUCY":      SOLAR + PYROS,
    "LUCIFER":   PHITA + AURA,
    "MIKE":      IGNIS + OMEGA,
    "MIKAEL":    MIKA_ + pi,
    "ERVN":      BIAL + KAL + PYROS,
    "ICEBERG":   MAR + PYROS,
    "GIGAROJ":   PYROS + OMEGA + pi,
    "OSIRIS":    MIKA_ + KAL - BIAL,
    "MIKAEL_V":  phi + pi + KRYSTOS_V,
}

print("=" * 55)
print("Nine Sovereignties — all must equal 3(φ+π) = 14.278880")
print("=" * 55)
for name, val in sovereignties.items():
    diff = abs(val - SIGMA_SOV)
    print(f"  {name:<12}  {val:.12f}   Δ={diff:.2e}")

# ── Derived cosmological parameters ──────────────────────────────────────────
# H0_alg, ns, Omb_h2_alg, Om_m, w0, wa importados de ssee_core (arriba).
# Identidades verificadas: H₀^alg = 3(φ+π)² = SIGMA_SOV·OMEGA ;
#   Ωb h² = (π−φ)/H₀^alg ; Ωm,geom = (π−φ)/(π+φ) ;
#   w₀ = -(3φ+π)/[2(φ+π)] ; wₐ = -(2φ+π)/[2(φ+π)]
Omb_h2_obs    = 0.02237                    # Planck 2018 observed (no algebraico)
Omc_h2_static = KAL * Omb_h2_obs           # +2.9σ Eckart (uses Planck Ωb h²)
Omc_h2_IS     = KAL * Omb_h2_obs * ns      # −0.6σ IS (uses Planck Ωb h²)

print(f"\n{'='*55}")
print("Derived cosmological parameters")
print(f"{'='*55}")
print(f"  H0_alg       = {H0_alg:.4f}  km/s/Mpc  (Planck: 67.36 ± 0.54)")
print(f"  ns           = {ns:.5f}            (Planck: 0.9649 ± 0.0042)")
print(f"  Ωb h² (alg)  = {Omb_h2_alg:.5f}            (Planck: 0.02237)")
print(f"  Ωb h² (obs)  = {Omb_h2_obs:.5f}            (input for IS formula)")
print(f"  Ωc h² static = {Omc_h2_static:.5f}            (+2.9σ Eckart)")
print(f"  Ωc h² IS     = {Omc_h2_IS:.5f}            (−0.6σ, uses Planck Ωb h²)")
print(f"  Ωm           = {Om_m:.4f}            (Planck: 0.3153)")
print(f"  w0           = {w0:.4f}            (DESI DR2: −0.827)")
print(f"  wa           = {wa:.4f}            (DESI DR2: −0.75)")
print(f"  VITA         = {VITA:.6f}")
print(f"  PHITA        = {PHITA:.6f}")

# ── Figure 1: Algebraic derivation tree ─────────────────────────────────────
fig1, axes = plt.subplots(1, 2, figsize=(12, 5))

ax = axes[0]
params = {
    r"$H_0$ (km/s/Mpc)": (H0_alg, 67.36, 0.54),
    r"$\Omega_m$":        (Om_m,   0.3153, 0.007),
    r"$n_s$":             (ns,     0.9649, 0.0042),
    r"$\Omega_b h^2$":    (Omb_h2_alg, 0.02237, 0.00015),
    r"$\Omega_c h^2$ (IS)":(Omc_h2_IS,  0.1200,  0.0012),
}
colors = ["#2077b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
y_pos = np.arange(len(params))
for i, (label, (pred, obs, sigma)) in enumerate(params.items()):
    pull = (pred - obs) / sigma
    ax.barh(y_pos[i], pull, color=colors[i], alpha=0.8, height=0.6)
ax.set_yticks(y_pos)
ax.set_yticklabels(list(params.keys()), fontsize=11)
ax.axvline(0, color="black", linewidth=1)
ax.axvline(-1, color="gray", linewidth=1, linestyle="--", alpha=0.5)
ax.axvline(+1, color="gray", linewidth=1, linestyle="--", alpha=0.5)
ax.axvline(-2, color="gray", linewidth=1, linestyle=":", alpha=0.3)
ax.axvline(+2, color="gray", linewidth=1, linestyle=":", alpha=0.3)
ax.set_xlabel(r"Pull $(\mathrm{SSEE} - \mathrm{obs})/\sigma$", fontsize=11)
ax.set_title("SSEE algebraic predictions vs Planck 2018", fontsize=11)
ax.set_xlim(-4.5, 4.5)

ax2 = axes[1]
names = list(sovereignties.keys())
vals  = [v - SIGMA_SOV for v in sovereignties.values()]
colors2 = ["#2077b4"] * 9
bars = ax2.bar(names, [abs(v) for v in vals], color=colors2, alpha=0.8)
ax2.set_yscale("log")
ax2.set_ylabel(r"$|S_i - M_v|$", fontsize=11)
ax2.set_title(r"Nine Sovereignties: deviation from $3(\phi+\pi)$", fontsize=11)
ax2.tick_params(axis="x", rotation=45, labelsize=8)
ax2.axhline(1e-14, color="red", linestyle="--", label="Float. pt. limit")
ax2.legend(fontsize=9)

plt.tight_layout()
os.makedirs("results/figures", exist_ok=True)
fig1.savefig("results/figures/fig_toe_derivations.pdf", bbox_inches="tight", metadata=_META)
fig1.savefig("results/figures/fig_toe_derivations.png", dpi=150, bbox_inches="tight")
print("\nSaved: results/figures/fig_toe_derivations.pdf")

# ── Figure 2: CMB TT spectrum (SSEE vs ΛCDM via CAMB) ───────────────────────
try:
    import camb

    def get_camb_cl(H0, ombh2, omch2, w0=-1.0, wa=0.0, ns=0.9649, As=2.1e-9, lmax=2500):
        pars = camb.CAMBparams()
        pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=0.06, omk=0)
        pars.set_dark_energy(w=w0, wa=wa, dark_energy_model="ppf")
        pars.InitPower.set_params(ns=ns, As=As)
        pars.set_for_lmax(lmax, lens_potential_accuracy=0)
        results = camb.get_results(pars)
        powers = results.get_cmb_power_spectra(pars, CMB_unit="muK")
        return powers["total"][:, 0]  # D_ℓ TT

    h_ssee = H0_alg / 100
    Cl_ssee = get_camb_cl(
        H0=H0_alg, ombh2=Omb_h2_obs,
        omch2=Omc_h2_IS,
        w0=w0, wa=wa, ns=ns
    )
    Cl_lcdm = get_camb_cl(
        H0=67.36, ombh2=0.02237,
        omch2=0.1200,
        w0=-1.0, wa=0.0, ns=0.9649
    )

    ell = np.arange(Cl_ssee.shape[0])
    fig2, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ell[2:], Cl_ssee[2:], color="#2077b4", lw=1.5, label="SSEE (algebraic params)")
    ax.plot(ell[2:], Cl_lcdm[2:], color="#ff7f0e", lw=1.5, ls="--", label=r"$\Lambda$CDM (Planck 2018)")
    ax.set_xlabel(r"Multipole $\ell$", fontsize=12)
    ax.set_ylabel(r"$D_\ell^{TT}$ $[\mu\mathrm{K}^2]$", fontsize=12)
    ax.set_title("CMB TT power spectrum: SSEE vs ΛCDM", fontsize=12)
    ax.set_xlim(2, 2500)
    ax.legend(fontsize=11)
    plt.tight_layout()
    fig2.savefig("results/figures/fig_toe_cmb_TT.pdf", bbox_inches="tight", metadata=_META)
    fig2.savefig("results/figures/fig_toe_cmb_TT.png", dpi=150, bbox_inches="tight")
    print("Saved: results/figures/fig_toe_cmb_TT.pdf")

except ImportError:
    print("CAMB not installed — skipping CMB figure (pip install camb)")

plt.show()
print("\nDone.")
