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
    r"$\Omega_c h^2$ (IS)":(KAL * Omb_h2_alg * ns, 0.1200, 0.0012),   # 2026-10-02: omega_b ALGEBRAICO (= OMEGA_C_H2 del nucleo), como la tabla del texto; antes usaba el de Planck
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
# 2026-10-02: las cuatro rutas representativas que cita el texto de P4 (notacion
# neutra), no las nueve con nombre mitologico (dos estaban repetidas y una restaba).
RUTAS = {r"$\Omega+K_v$": OMEGA + KRYSTOS_V,
         r"$\beta+\mathrm{KAL}+P_{sc}$": BIAL + KAL + PYROS,
         r"$P_{sc}+\Omega+\pi$": PYROS + OMEGA + pi,
         r"$\varphi+\pi+K_v$": phi + pi + KRYSTOS_V}
names = list(RUTAS.keys())
vals  = [v - SIGMA_SOV for v in RUTAS.values()]
# ORIGEN-VALOR: 1e-17 — piso para la escala log: una diferencia exactamente cero no se puede dibujar
bars = ax2.bar(names, [max(abs(v), 1e-17) for v in vals], color="#2077b4", alpha=0.8)
ax2.set_yscale("log")
ax2.set_ylabel(r"$|\mathrm{route} - M_v|$", fontsize=11)
ax2.set_title(r"Additive routes to $M_v = 3(\varphi+\pi)$", fontsize=11)
ax2.tick_params(axis="x", rotation=20, labelsize=9)
ax2.axhline(1e-14, color="red", linestyle="--", label="Float. pt. limit")
ax2.legend(fontsize=9)

plt.tight_layout()
os.makedirs("results/figures", exist_ok=True)
fig1.savefig("results/figures/fig_toe_derivations.pdf", bbox_inches="tight", metadata=_META)
fig1.savefig("results/figures/fig_toe_derivations.png", dpi=150, bbox_inches="tight")
print("\nSaved: results/figures/fig_toe_derivations.pdf")

# ── Figure 2: CMB TT spectrum (SSEE vs ΛCDM via CAMB) ───────────────────────
# 2026-10-02: cada modelo con SUS ingredientes. Antes SSEE corria con mnu 0.06
# (el de LCDM), omega_b de Planck (0.02237) y omega_c de la formula IS con ese
# omega_b (0.11926), y A_s/tau tecleados: el pie de P4 decia «todo algebraico»
# y no lo era. Ahora: SSEE = nucleo (omega_b, omega_c, n_s, w0, wa, H_glob,
# Sum m_nu 0.06849) con A_s y tau del clavo del CMB (cmb_dbic_tau_ajustado.json);
# LCDM = Planck 2018 (lcdm_planck.py, mnu 0.06). Los picos se CALCULAN aqui y
# van a results/logs/paper4_toe.json; el pie los cita por \val.
try:
    import camb
    import json as _json
    from scipy.signal import find_peaks
    _R4 = _reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__))))
    _reloc_sys.path.insert(0, _reloc_os.path.join(_R4, "src", "p11_sondas"))
    from ssee_core import OMEGA_C_H2, SUM_MNU_EV
    from lcdm_planck import LCDM_PLANCK as _P, LOGA_PLANCK, TAU_PLANCK
    _CLAVO = _reloc_os.path.join(_R4, "results", "logs", "cmb_dbic_tau_ajustado.json")
    _ENT_ACTA.append(_CLAVO)
    _cl = _json.load(open(_CLAVO))["SSEE"]["mejor"]

    def get_camb_cl(H0, ombh2, omch2, w0, wa, ns, logA, tau, mnu, lmax=2500):
        pars = camb.CAMBparams()
        pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=mnu, omk=0, tau=tau)
        pars.set_dark_energy(w=w0, wa=wa, dark_energy_model="ppf")
        pars.InitPower.set_params(ns=ns, As=np.exp(logA) * 1e-10)
        pars.set_for_lmax(lmax, lens_potential_accuracy=1)
        powers = camb.get_results(pars).get_cmb_power_spectra(pars, CMB_unit="muK")
        return powers["total"][:, 0]  # D_ℓ TT con lente

    ING = dict(
        SSEE=dict(H0=H0_alg, ombh2=Omb_h2_alg, omch2=OMEGA_C_H2, w0=w0, wa=wa, ns=ns,
                  logA=_cl["logA"], tau=_cl["tau"], mnu=SUM_MNU_EV),
        LCDM=dict(H0=_P["H0"], ombh2=_P["ombh2"], omch2=_P["omch2"], w0=-1.0, wa=0.0, ns=_P["ns"],
                  logA=LOGA_PLANCK, tau=TAU_PLANCK, mnu=_P["mnu"]),
    )
    Cl = {n: get_camb_cl(**d) for n, d in ING.items()}

    def picos(dl, n=3):
        # ORIGEN-VALOR: 100 — prominencia minima en muK^2 para contar un pico acustico (los tres primeros superan 1000)
        k, _ = find_peaks(dl[100:1500], prominence=100)   # ORIGEN-VALOR: 100-1500 — ventana de l de los tres primeros picos
        return [int(x + 100) for x in k[:n]]

    PICOS = {n: picos(c) for n, c in Cl.items()}
    for n in ING:
        print(f"  {n:5s} picos TT l = {PICOS[n]}   ingredientes: mnu {ING[n]['mnu']}, ombh2 {ING[n]['ombh2']:.5f}, omch2 {ING[n]['omch2']:.5f}")
    _dif = [abs(a - b) / b for a, b in zip(PICOS["SSEE"], PICOS["LCDM"])]
    print(f"  diferencia relativa SSEE-LCDM por pico: {[f'{100 * d:.2f}%' for d in _dif]}")
    from procedencia import con_acta as _con_acta
    _json.dump(_con_acta(dict(ingredientes=ING, picos=PICOS, dif_rel=_dif, dif_rel_max=max(_dif)),
                         __file__, entradas=_ENT_ACTA),
               open(_reloc_os.path.join(_R4, "results", "logs", "paper4_toe.json"), "w"), indent=1)
    _META = {"Keywords": "ACTA-PROCEDENCIA " + _jsacta.dumps(_acta(__file__, entradas=_ENT_ACTA))}

    ell = np.arange(Cl["SSEE"].shape[0])
    fig2, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ell[2:], Cl["SSEE"][2:], color="#2077b4", lw=1.5, label="SSEE (algebraic background; $A_s$, $\\tau$ from the CMB fit)")
    ax.plot(ell[2:], Cl["LCDM"][2:], color="#ff7f0e", lw=1.5, ls="--", label=r"$\Lambda$CDM (Planck 2018)")
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
