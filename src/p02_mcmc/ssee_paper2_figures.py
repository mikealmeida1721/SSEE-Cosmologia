"""
SSEE — Paper 2 Figures
Fig 1: w0-wa plane con contornos DESI DR2
Fig 2: Sensibilidad de masas por escenario
Fig 3: Omega_DE SSEE vs Lambda con contexto estructural
Fig 4: KAL(x) interpolation — límites Newtoniano y MONDiano
"""
# ORIGEN-VALOR: 0.6847 — Omega_Lambda de Planck 2018 (arXiv:1807.06209)

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse
from matplotlib import gridspec
from scipy import stats

# Ancla a results/figures/ del repo, sin importar desde dónde se ejecute.
_OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "..", "results", "figures")
os.makedirs(_OUTDIR, exist_ok=True)


def _outpath(name):
    return os.path.join(_OUTDIR, name)

# ── Estilo global ──────────────────────────────────────────────
plt.rcParams.update({
    "font.family":       "serif",
    "font.size":         11,
    "axes.labelsize":    12,
    "axes.titlesize":    12,
    "legend.fontsize":   10,
    "xtick.direction":   "in",
    "ytick.direction":   "in",
    "xtick.top":         True,
    "ytick.right":       True,
    "axes.grid":         True,
    "grid.alpha":        0.3,
    "grid.linestyle":    "--",
    "figure.dpi":        150,
    "savefig.dpi":       300,
    "savefig.bbox":      "tight",
})

# ── Constantes SSEE ────────────────────────────────────────────
PHI  = (1 + np.sqrt(5)) / 2
PI   = np.pi
BETA = (PI + PHI) / 2
KAL0 = BETA + PI
P_sc = PI + PHI + PHI          # P = Ω + Φ = (π+Φ) + Φ
KV   = PHI + PI + (PI + PHI)   # Kv = Φ+π+Ω  (scaffold: solo como sumando de M_v)
IGNIS = PI + P_sc              # IGNIS = π+PYROS — denominador de wₐ (R21)
OMEGA_M_TOTAL = 0.30888087877875237   # ORIGEN: ssee_core.OMEGA_M_TOTAL = omega_m/h^2
TR   = 3 * (PHI + BETA)
MV   = PHI + PI + KV

W0_SSEE       = -TR / MV
WA_SSEE       = -P_sc / IGNIS   # denominador IGNIS, no el scaffold K_v: mismo valor, entidad distinta
# CORREGIDO 2026-09-26 — ERROR DE CATEGORIA en la figura 3.
# TR/MV = 0.839950 NO es una densidad: es s_DE = |w0|, un numero de la ECUACION
# DE ESTADO. La figura lo ponia en un eje de Omega_DE frente a Planck y anotaba
# la diferencia «ΔΩ ≈ +0.155» como si fuera una prediccion del modelo. No lo es:
# es el mismo error que mato a la particula phi-DM (restar una densidad menos un
# 1+w0). La densidad de energia oscura del modelo es 1 − Omega_m.
S_DE_SSEE     = TR / MV                       # |w0| — ecuacion de estado, NO densidad
OMEGA_DE_SSEE = 1.0 - OMEGA_M_TOTAL           # 0.691119 — la densidad de verdad

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FIGURA 1 — Plano w0-wa
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def covariance_ellipse(ax, w0c, wac, sig_w0, sig_wa, rho, n_sigma,
                       color, alpha, label=None, zorder=2):
    cov = np.array([[sig_w0**2, rho*sig_w0*sig_wa],
                    [rho*sig_w0*sig_wa, sig_wa**2]])
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = eigvals.argsort()[::-1]
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]
    angle = np.degrees(np.arctan2(*eigvecs[:, 0][::-1]))
    # χ²(2) para n_sigma equivalentes en 2D
    chi2_val = stats.chi2.ppf(2*stats.norm.cdf(n_sigma) - 1, df=2)
    width  = 2 * np.sqrt(chi2_val * eigvals[0])
    height = 2 * np.sqrt(chi2_val * eigvals[1])
    ell = Ellipse((w0c, wac), width, height, angle=angle,
                  facecolor=color, alpha=alpha, edgecolor=color,
                  linewidth=1.5, zorder=zorder, label=label)
    ax.add_patch(ell)

fig1, ax1 = plt.subplots(figsize=(7, 6))

# Contornos w0waCDM OFICIALES DESI DR2 — momentos y ρ MEDIDOS de las cadenas
# oficiales (Zenodo 16644577, burn-in 30%, pesos). DR1 viejos RETIRADOS (V-L4-DESI).
pant_kw = dict(w0c=-0.838, wac=-0.617, sig_w0=0.055, sig_wa=0.208, rho=-0.894)
covariance_ellipse(ax1, **pant_kw, n_sigma=2, color="#2166AC", alpha=0.18, zorder=1)
covariance_ellipse(ax1, **pant_kw, n_sigma=1, color="#2166AC", alpha=0.35, zorder=2,
                   label="DESI DR2+CMB+Pantheon+ 1σ/2σ")

desy_kw = dict(w0c=-0.752, wac=-0.861, sig_w0=0.057, sig_wa=0.221, rho=-0.905)
covariance_ellipse(ax1, **desy_kw, n_sigma=2, color="#4DAF4A", alpha=0.12, zorder=1)
covariance_ellipse(ax1, **desy_kw, n_sigma=1, color="#4DAF4A", alpha=0.28, zorder=2,
                   label="DESI DR2+CMB+DESY5 1σ/2σ")

uni_kw = dict(w0c=-0.667, wac=-1.085, sig_w0=0.088, sig_wa=0.293, rho=-0.933)
covariance_ellipse(ax1, **uni_kw, n_sigma=2, color="#D95F02", alpha=0.12, zorder=1)
covariance_ellipse(ax1, **uni_kw, n_sigma=1, color="#D95F02", alpha=0.30, zorder=2,
                   label="DESI DR2+CMB+Union3 1σ/2σ")

# ΛCDM
ax1.scatter(-1.0, 0.0, marker="+", s=120, color="black", linewidths=2.5,
            zorder=6, label=r"$\Lambda$CDM ($w_0=-1,\,w_a=0$)")

# Punto SSEE
ax1.scatter(W0_SSEE, WA_SSEE, marker="*", s=260, color="#E6002B",
            edgecolors="black", linewidths=0.8, zorder=7,
            label=fr"SSEE ($w_0={W0_SSEE:.3f},\,w_a={WA_SSEE:.3f}$)")

# Cruz de incertidumbre SSEE (algebraica → 0, pero indicamos con símbolo)
ax1.annotate(
    fr"SSEE: 0.24$\sigma$ (Pantheon+)",
    xy=(W0_SSEE, WA_SSEE), xytext=(W0_SSEE + 0.05, WA_SSEE + 0.15),
    fontsize=9, color="#E6002B",
    arrowprops=dict(arrowstyle="->", color="#E6002B", lw=1.2),
)

# Línea w0+wa = -1 (phantom divide)
w0_line = np.linspace(-1.4, -0.4, 200)
ax1.plot(w0_line, -1 - w0_line, "k--", lw=1.0, alpha=0.5,
         label=r"$w_0+w_a=-1$ (phantom divide)")

ax1.set_xlabel(r"$w_0$")
ax1.set_ylabel(r"$w_a$")
ax1.set_title("SSEE in the $w_0$-$w_a$ plane — official DESI DR2 $w_0w_a$CDM (2503.14738)")
ax1.set_xlim(-1.35, -0.45)
ax1.set_ylim(-1.6, 0.8)
ax1.legend(loc="upper left", framealpha=0.9, fontsize=9)
fig1.tight_layout()
fig1.savefig(_outpath("fig1_w0wa_plane.pdf"))
fig1.savefig(_outpath("fig1_w0wa_plane.png"))
print("Fig 1 guardada: fig1_w0wa_plane.pdf/.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FIGURA 2 — Sensibilidad de masas en cúmulos
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FNU = 0.020
IGIMF_FACTOR = 1.718   # promedio M_IGIMF / M_std de los 4 cúmulos

clusters = {
    "Coma":         {"M_ig": 1.8, "dM_ig": 0.2, "M_obs": 9.8,  "dM_obs": 1.0, "M_std": 1.0},
    "A2029":        {"M_ig": 2.2, "dM_ig": 0.2, "M_obs": 12.0, "dM_obs": 1.2, "M_std": 1.3},
    "A478":         {"M_ig": 1.5, "dM_ig": 0.2, "M_obs": 8.0,  "dM_obs": 1.0, "M_std": 0.9},
    "Bullet":       {"M_ig": 1.2, "dM_ig": 0.2, "M_obs": 6.5,  "dM_obs": 1.0, "M_std": 0.7},
}

cnames   = list(clusters.keys())
x_pos    = np.arange(len(cnames))
bar_w    = 0.20

scenarios = {
    "SSEE completo":  lambda c: c["M_ig"] * KAL0 * (1 + FNU),
    r"$f_\nu=0$":     lambda c: c["M_ig"] * KAL0,
    "STD IMF":        lambda c: c["M_std"] * KAL0 * (1 + FNU),
    r"KAL$_0$ solo":  lambda c: c["M_std"] * KAL0,
}

colors_bar = ["#E6002B", "#F4A261", "#2A9D8F", "#8338EC"]

fig2, ax2 = plt.subplots(figsize=(9, 5.5))

for i, (label, func) in enumerate(scenarios.items()):
    masses = [func(clusters[c]) for c in cnames]
    offset = (i - 1.5) * bar_w
    bars = ax2.bar(x_pos + offset, masses, bar_w,
                   label=label, color=colors_bar[i], alpha=0.85,
                   edgecolor="black", linewidth=0.5)

# Puntos observados con barras de error
for j, c in enumerate(cnames):
    d = clusters[c]
    ax2.errorbar(x_pos[j], d["M_obs"], yerr=d["dM_obs"],
                 fmt="D", color="black", ms=7, capsize=5, zorder=8,
                 label="$M^{\\rm obs}_{\\rm dyn}$" if j == 0 else "")

ax2.set_xticks(x_pos)
ax2.set_xticklabels(cnames, fontsize=11)
ax2.set_ylabel(r"Masa efectiva $[10^{14}\,M_\odot]$")
ax2.set_title("Sensibilidad de masas de cúmulos por escenario SSEE")
ax2.legend(loc="upper left", ncol=2, framealpha=0.9)
ax2.set_ylim(0, 17)

# Anotaciones chi2_red
chi2s = {
    "SSEE completo": 0.122,
    r"$f_\nu=0$":    0.032,
    "STD IMF":       11.927,
    r"KAL$_0$ solo": 12.646,
}
y_annot = 15.5
for i, (label, c2r) in enumerate(chi2s.items()):
    color = colors_bar[i]
    ax2.text(0.02 + i * 0.25, 0.96,
             f"{label}\n$\\chi^2_r={c2r:.2f}$",
             transform=ax2.transAxes, fontsize=8.5,
             color=color, va="top", ha="left",
             bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                       edgecolor=color, alpha=0.7))

fig2.tight_layout()
fig2.savefig(_outpath("fig2_cluster_sensitivity.pdf"))
fig2.savefig(_outpath("fig2_cluster_sensitivity.png"))
print("Fig 2 guardada: fig2_cluster_sensitivity.pdf/.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FIGURA 3 — Omega_DE: SSEE vs observaciones + diagrama estructural
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

omega_obs = {
    "Planck 2018":          (0.6847, 0.0073),
    "DESI DR2\n+CMB":       (0.6900, 0.0100),
    "DESI DR2\n+CMB+DESY5": (0.6910, 0.0120),
}

fig3, axes3 = plt.subplots(1, 2, figsize=(11, 5),
                            gridspec_kw={"width_ratios": [1.4, 1]})

ax3a = axes3[0]
ax3b = axes3[1]

# Panel izquierdo: comparación de valores
x3 = np.arange(len(omega_obs))
bar_colors3 = ["#D95F02", "#2166AC", "#4DAF4A"]

for i, (dname, (om, sig)) in enumerate(omega_obs.items()):
    ax3a.barh(i, om, xerr=3*sig, height=0.5,
              color=bar_colors3[i], alpha=0.75,
              edgecolor="black", linewidth=0.6,
              error_kw=dict(capsize=5, elinewidth=1.5),
              label=f"{dname.replace(chr(10), ' ')} (±3σ)")

ax3a.axvline(OMEGA_DE_SSEE, color="#E6002B", lw=2.0, ls="-",
             label=fr"$\Omega_{{DE,SSEE}} = 1-\Omega_m = {OMEGA_DE_SSEE:.4f}$")
ax3a.axvline(S_DE_SSEE, color="#7A5C9E", lw=1.6, ls="--",
             label=fr"$s_{{DE}}=|w_0|={S_DE_SSEE:.4f}$ — not a density")
ax3a.axvline(0.6847, color="black", lw=1.0, ls=":",
             label=r"$\Omega_\Lambda$ Planck 2018")

ax3a.set_yticks(x3)
ax3a.set_yticklabels([k.replace("\n", " ") for k in omega_obs.keys()], fontsize=10)
ax3a.set_xlabel(r"$\Omega_{DE}$")
ax3a.set_title(r"$\Omega_{DE,SSEE}=1-\Omega_m$ vs observational constraints")
ax3a.set_xlim(0.63, 0.88)
ax3a.legend(fontsize=9, loc="upper left")

# Anotación de la diferencia estructural
ax3a.annotate(
    "$s_{DE}=T_r/M_v$ is $|w_0|$,\nan equation-of-state\nnumber. It does not\nlive on this axis.",
    xy=(S_DE_SSEE, 2), xytext=(0.700, 2.55),
    fontsize=8.0, color="#7A5C9E",
    arrowprops=dict(arrowstyle="->", color="#7A5C9E", lw=1.0),
    bbox=dict(boxstyle="round", facecolor="white", edgecolor="#7A5C9E", alpha=0.85)
)

# Panel derecho: descomposición energética SSEE vs ΛCDM
labels_pie = [r"$\Omega_m$", r"$\Omega_{DE}=1-\Omega_m$"]
sizes_ssee = [OMEGA_M_TOTAL, OMEGA_DE_SSEE]   # [0.308881, 0.691119] — UNA densidad de materia

labels_lcdm = [r"$\Omega_m$", r"$\Omega_\Lambda$"]
sizes_lcdm  = [1 - 0.6847, 0.6847]                 # ≈ [0.315, 0.685]

angles = [0, 0]
colors_ssee = ["#E6002B", "#FCBF49"]
colors_lcdm = ["#2166AC", "#A8DADC"]

width = 0.35
r_outer = 0.9
r_inner = 0.55

# Anillo externo = SSEE, interno = ΛCDM
wedges_outer, _ = ax3b.pie(
    sizes_ssee, labels=None, colors=colors_ssee,
    radius=r_outer, startangle=90,
    wedgeprops=dict(width=width, edgecolor="white", linewidth=1.5),
    autopct=None
)
wedges_inner, _ = ax3b.pie(
    sizes_lcdm, labels=None, colors=colors_lcdm,
    radius=r_inner, startangle=90,
    wedgeprops=dict(width=width, edgecolor="white", linewidth=1.5),
    autopct=None
)

ax3b.text(0, 0, "SSEE\nvs\nΛCDM", ha="center", va="center", fontsize=9,
          fontweight="bold")

legend_handles = [
    mpatches.Patch(color=colors_ssee[0], label=fr"SSEE: $\Omega_m$ ({sizes_ssee[0]:.3f})"),
    mpatches.Patch(color=colors_ssee[1], label=fr"SSEE: $\Omega_{{DE}}$ ({sizes_ssee[1]:.3f})"),
    mpatches.Patch(color=colors_lcdm[0], label=fr"ΛCDM: $\Omega_m$ ({sizes_lcdm[0]:.3f})"),
    mpatches.Patch(color=colors_lcdm[1], label=fr"ΛCDM: $\Omega_\Lambda$ ({sizes_lcdm[1]:.3f})"),
]
ax3b.legend(handles=legend_handles, loc="lower center",
            bbox_to_anchor=(0.5, -0.22), fontsize=8.5, ncol=2)
ax3b.set_title("Energy budget\n(outer=SSEE, inner=ΛCDM)", fontsize=10)

fig3.tight_layout()
fig3.savefig(_outpath("fig3_omega_de.pdf"))
fig3.savefig(_outpath("fig3_omega_de.png"))
print("Fig 3 guardada: fig3_omega_de.pdf/.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FIGURA 4 — Función de interpolación KAL(x)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

x  = np.logspace(-2, 2, 400)

KAL_x   = (x + KAL0) / (x + 1)
mu_SSEE = (x + 1) / (x + KAL0)

# MOND estándar (simple): mu(x) = x / (1+x)
mu_MOND = x / (1 + x)
KAL_MOND = 1 / mu_MOND   # diverge en x→0, solo para comparar

fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(10, 5))

# Panel izq: KAL(x)
ax4a.semilogx(x, KAL_x, color="#E6002B", lw=2.5, label=r"$\mathrm{KAL}(x)$ SSEE")
ax4a.axhline(KAL0, color="#E6002B", ls="--", lw=1.2, alpha=0.7,
             label=fr"$\mathrm{{KAL}}_0 = {KAL0:.4f}$ (deep-MOND limit)")
ax4a.axhline(1.0,  color="gray",    ls=":",  lw=1.2, alpha=0.8,
             label="KAL → 1 (Newtonian limit)")
ax4a.axvline(1.0,  color="black",   ls="-.", lw=0.8, alpha=0.5,
             label=r"$x = 1$ (transition)")

# Zonas
ax4a.axvspan(1e-2, 1.0, alpha=0.06, color="#E6002B",  label="Deep MONDian")
ax4a.axvspan(1.0, 1e2,  alpha=0.06, color="#2166AC",  label="Newtonian")

ax4a.set_xlabel(r"$x = |\nabla\Phi| / a_0$")
ax4a.set_ylabel(r"$\mathrm{KAL}(x)$")
ax4a.set_title(r"Retención estructural $\mathrm{KAL}(x)$ — SSEE")
ax4a.set_ylim(0.8, KAL0 + 0.5)
ax4a.legend(fontsize=9, loc="center right")

# Panel der: µ_SSEE(x) vs µ_MOND
ax4b.semilogx(x, mu_SSEE, color="#E6002B", lw=2.5, label=r"$\mu_\mathrm{SSEE}(x)$")
ax4b.semilogx(x, mu_MOND,  color="#2166AC", lw=2.0, ls="--",
              label=r"$\mu_\mathrm{MOND}(x) = x/(1+x)$")
ax4b.axhline(1.0, color="gray", ls=":", lw=1.2, alpha=0.8)
ax4b.axvline(1.0, color="black", ls="-.", lw=0.8, alpha=0.5)

ax4b.set_xlabel(r"$x = |\nabla\Phi| / a_0$")
ax4b.set_ylabel(r"$\mu(x)$")
ax4b.set_title(r"$\mu_\mathrm{SSEE}$ vs $\mu_\mathrm{MOND}$ — dualidad asimétrica")
ax4b.set_ylim(-0.05, 1.15)
ax4b.legend(fontsize=10)

# Anotación asimétrica
ax4b.annotate(
    r"$\mu_\mathrm{SSEE}(x) \cdot \mathrm{KAL}(x) \equiv 1$",
    xy=(0.3, 0.45), xytext=(0.015, 0.78),
    fontsize=9.5, color="#E6002B",
    arrowprops=dict(arrowstyle="->", color="#E6002B", lw=1.0),
    bbox=dict(boxstyle="round", facecolor="white", edgecolor="#E6002B", alpha=0.8)
)

fig4.tight_layout()
fig4.savefig(_outpath("fig4_KAL_interpolation.pdf"))
fig4.savefig(_outpath("fig4_KAL_interpolation.png"))
print("Fig 4 guardada: fig4_KAL_interpolation.pdf/.png")

print("\nTodas las figuras generadas exitosamente.")
