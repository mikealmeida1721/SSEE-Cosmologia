"""
Regenerador standalone de fig7_Hz_comparison y fig8_tension_summary (Paper 2).

Lee las cadenas CORREGIDAS de 3 modelos (geometría total Ω_m=0.308881, ω_m-directo;
el bug del sector frío 0.160 en E(z) quedó retirado, V-L4-DESI 2026-07-09) desde
el .npz profesional en el HDD y reproduce las dos figuras con los valores canónicos:
  fig7 : H(z) MAP vs Cosmic Chronometers  (χ²_r SSEE=0.482 ≈ ΛCDM 0.459)
  fig8 : posteriores H0 (SSEE 67.95, 0.88σ Planck) + barras r_d MAP (148.2 ≈ ΛCDM)

Uso: python src/p02_mcmc/regenerate_fig7_fig8_p2.py
Salida: results/figures/fig7_Hz_comparison.{pdf,png}, fig8_tension_summary.{pdf,png}
"""
# ORIGEN-VALOR: 0.1432 — pivote omega_m h^2 de la eq. rd de Paper 2 (Planck 2018 TT,TE,EE+lowE); cita EH98 en FUENTES_PENDIENTES.md FP-7
import os, sys
import numpy as np
import matplotlib
_SSEE_DATA = os.environ.get("SSEE_DATA_DIR") or ("/mnt/datos/SSEE_data" if os.path.isdir("/mnt/datos") else "results/data")  # portable: HDD si existe, si no results/ local
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ssee_core import (
    W0 as W0_SSEE, WA as WA_SSEE,
    OMEGA_M_TOTAL as OM_GEOM, OMEGA_M_H2 as WM_ALG,   # 0.308881 — materia TOTAL, la ÚNICA que entra en E(z)/r_d
)

CHAIN_FILE = _SSEE_DATA + "/mcmc/paper2_3models/mcmc_chains_professional.npz"
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "results", "figures")
os.makedirs(OUT, exist_ok=True)
C_KM = 2.998e5
PLANCK_H0 = (67.36, 0.54)

# ── funciones E(z) / r_d idénticas al MCMC (ssee_paper2_mcmc.py) ──
def f_de_cpl(z, w0, wa):
    a = 1.0 / (1.0 + z)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))

def E_ssee(z):
    return np.sqrt(OM_GEOM * (1 + z) ** 3 + (1 - OM_GEOM) * f_de_cpl(z, W0_SSEE, WA_SSEE))

def E_lcdm(z, Om):
    return np.sqrt(Om * (1 + z) ** 3 + (1 - Om))

def E_cpl(z, Om, w0, wa):
    return np.sqrt(Om * (1 + z) ** 3 + (1 - Om) * f_de_cpl(z, w0, wa))

import os as _os_rd, sys as _sys_rd
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), ".."))
from rd_camb import rd_mpc as _rd_camb  # r_d de CAMB, una sola funcion (2026-09-28)


def sound_horizon_rd(ob_h2, om_h2):
    return _rd_camb(ob_h2, om_h2, mnu=None)  # CAMB; antes 147.27*(...) con normalizacion 0.15 % alta

# ── Cosmic Chronometers (Jimenez–Loeb 2002; Moresco+ 2022 compilación) ──
CC_DATA = np.array([
    [0.070, 69.0, 19.6], [0.179, 75.0,  4.0], [0.199, 75.0,  5.0],
    [0.352, 83.0, 14.0], [0.400, 95.0, 17.0], [0.440, 82.6,  7.8],
    [0.593, 104.0, 13.0], [0.680, 92.0,  8.0], [0.781, 105.0, 12.0],
    [0.875, 125.0, 17.0], [1.037, 154.0, 20.0],
])
Z_CC, H_CC, DH_CC = CC_DATA[:, 0], CC_DATA[:, 1], CC_DATA[:, 2]

# ── cargar cadenas corregidas ──
d = np.load(CHAIN_FILE, allow_pickle=True)
ssee, lcdm, cpl = d["ssee_flat"], d["lcdm_flat"], d["cpl_flat"]
ssee_lp, lcdm_lp, cpl_lp = d["ssee_lp"], d["lcdm_lp"], d["cpl_lp"]

# MAP de cada modelo (máximo del log-posterior)
map_ssee = ssee[np.argmax(ssee_lp)]   # [H0, ob_h2]
map_lcdm = lcdm[np.argmax(lcdm_lp)]   # [H0, Om, ob_h2]
map_cpl  = cpl[np.argmax(cpl_lp)]     # [H0, Om, w0, wa, ob_h2]

def H_ssee(z): return map_ssee[0] * E_ssee(z)
def H_lcdm(z): return map_lcdm[0] * E_lcdm(z, map_lcdm[1])
def H_cpl(z):  return map_cpl[0] * E_cpl(z, map_cpl[1], map_cpl[2], map_cpl[3])

def chi2_cc(Hfunc):
    return np.sum(((Hfunc(Z_CC) - H_CC) / DH_CC) ** 2) / len(Z_CC)

chi2 = {"SSEE": chi2_cc(H_ssee), "ΛCDM": chi2_cc(H_lcdm), "CPL": chi2_cc(H_cpl)}
print("χ²_r(H(z)):", {k: round(v, 3) for k, v in chi2.items()})

colors = {"SSEE": "#E6002B", "ΛCDM": "#1a55a9", "CPL": "#2ca02c"}
ls_map = {"SSEE": "-", "ΛCDM": "--", "CPL": "-."}

plt.rcParams.update({"font.size": 11, "figure.dpi": 150,
                     "savefig.dpi": 300, "savefig.bbox": "tight"})

# ══ Fig 7: H(z) ══
z_plot = np.linspace(0, 1.5, 200)
fig7, ax7 = plt.subplots(figsize=(8, 5.5))
ax7.errorbar(Z_CC, H_CC, yerr=DH_CC, fmt="o", color="black", ms=5, capsize=3,
             zorder=6, label="Cosmic Chronometers")
for lab, Hf in [("SSEE", H_ssee), ("ΛCDM", H_lcdm), ("CPL", H_cpl)]:
    ax7.plot(z_plot, Hf(z_plot), color=colors[lab], lw=2.3, ls=ls_map[lab],
             label=fr"{lab} (MAP, $\chi^2_r$={chi2[lab]:.2f})")
# banda 68% posterior SSEE
rng = np.random.default_rng(0)
idx_s = rng.integers(0, len(ssee), 400)
H_band = np.array([ssee[i][0] * E_ssee(z_plot) for i in idx_s])
ax7.fill_between(z_plot, np.percentile(H_band, 16, 0), np.percentile(H_band, 84, 0),
                 color="#E6002B", alpha=0.15, label="SSEE 68% posterior")
ax7.set_xlabel("Redshift $z$")
ax7.set_ylabel(r"$H(z)$ [km s$^{-1}$ Mpc$^{-1}$]")
ax7.set_title(r"Posterior predictive check — $H(z)$ (total matter $\Omega_m=0.308881$ in geometry)")
ax7.legend(fontsize=9)
ax7.set_xlim(0, 1.5)
fig7.tight_layout()
fig7.savefig(os.path.join(OUT, "fig7_Hz_comparison.pdf"))
fig7.savefig(os.path.join(OUT, "fig7_Hz_comparison.png"))
plt.close(fig7)
print("Fig 7 guardada")

# ══ Fig 8: posteriores H0 + barras r_d ══
fig8, (ax8a, ax8b) = plt.subplots(1, 2, figsize=(11, 4.5))
chains = [("SSEE", ssee, map_ssee), ("ΛCDM", lcdm, map_lcdm), ("CPL", cpl, map_cpl)]
for lab, ch, _ in chains:
    ax8a.hist(ch[:, 0], bins=60, density=True, color=colors[lab], alpha=0.55, label=lab)
ax8a.axvline(PLANCK_H0[0], color="black", ls="--", lw=1.5,
             label=f"Planck: {PLANCK_H0[0]}±{PLANCK_H0[1]}")
ax8a.fill_betweenx([0, ax8a.get_ylim()[1]], PLANCK_H0[0] - PLANCK_H0[1],
                   PLANCK_H0[0] + PLANCK_H0[1], color="black", alpha=0.12)
h0_ssee = np.mean(ssee[:, 0]); s_ssee = np.std(ssee[:, 0])
sig_planck = abs(h0_ssee - PLANCK_H0[0]) / np.hypot(s_ssee, PLANCK_H0[1])
ax8a.set_xlabel(r"$H_0$ [km s$^{-1}$ Mpc$^{-1}$]")
ax8a.set_ylabel("Posterior density")
ax8a.set_title(fr"$H_0$ posteriors — SSEE ${h0_ssee:.2f}\pm{s_ssee:.2f}$ ({sig_planck:.2f}$\sigma$ Planck)")
ax8a.legend(fontsize=9)
ax8a.set_ylim(0, None)

# r_d MAP por modelo (om_h2 de la materia TOTAL en cada caso)
def rd_of(lab, m):
    if lab == "SSEE":
        H0, ob = m[0], m[1]; om_h2 = WM_ALG   # ω_m algebraico fijo (R25), no Ω_m·h²
    elif lab == "ΛCDM":
        H0, Om, ob = m[0], m[1], m[2]; om_h2 = Om * (H0 / 100) ** 2
    else:
        H0, Om, ob = m[0], m[1], m[4]; om_h2 = Om * (H0 / 100) ** 2
    return sound_horizon_rd(ob, om_h2)

rd_vals = [rd_of(lab, m) for lab, _, m in chains]
y_pos = np.arange(len(chains))
bars = ax8b.barh(y_pos, rd_vals, color=[colors[l] for l, _, _ in chains],
                 alpha=0.8, edgecolor="black", linewidth=0.6)
ax8b.axvline(147.09, color="black", ls="--", lw=1.5, label=r"Planck: $147.09$ Mpc")
ax8b.set_yticks(y_pos)
ax8b.set_yticklabels([l for l, _, _ in chains])
ax8b.set_xlabel("$r_d$ [Mpc]")
ax8b.set_title(r"Sound horizon $r_d$ (MAP) — SSEE matches $\Lambda$CDM")
ax8b.legend(fontsize=9)
for bar, v in zip(bars, rd_vals):
    ax8b.text(v + 0.4, bar.get_y() + bar.get_height() / 2, f"{v:.1f}", va="center", fontsize=10)
fig8.tight_layout()
fig8.savefig(os.path.join(OUT, "fig8_tension_summary.pdf"))
fig8.savefig(os.path.join(OUT, "fig8_tension_summary.png"))
plt.close(fig8)
print("Fig 8 guardada")
print(f"r_d MAP: SSEE={rd_vals[0]:.2f}  ΛCDM={rd_vals[1]:.2f}  CPL={rd_vals[2]:.2f}")
print(f"H0 SSEE={h0_ssee:.3f}±{s_ssee:.3f}  ({sig_planck:.2f}σ Planck)")
