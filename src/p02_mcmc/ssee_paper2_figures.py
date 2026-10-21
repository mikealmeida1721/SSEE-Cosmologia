"""
SSEE — Paper 2 Figures (etapa DVC `p2_figuras`)
Fig 1: plano w0-wa con los contornos oficiales de DESI DR2
Fig 3: Omega_DE de SSEE contra las restricciones observacionales

2026-10-21: todo número sale de su fuente, nada tecleado.
  - SSEE (w0, wa, Omega_m): ssee_core.
  - Contornos de la fig. 1: results/logs/desi_dr2_w0wa_momentos.log (cadenas oficiales).
  - Distancia de SSEE en la fig. 1: results/logs/paper2_w0wa.json.
  - Omega_DE de DESI en la fig. 3: las cadenas oficiales w0wa de DESI DR2 (columna
    omegal, burn-in 30 %, con pesos); antes eran dos pares tecleados sin fuente.
Retiradas del script: la fig. 2 (cúmulos con los datos atribuidos a Zhang+2026, que no
salían de ahí; rehecho en cumulos_zhang2026.json) y la fig. 4 (interpolación KAL(x)
Newton-MOND, lectura retirada de P2 el 2026-10-01: KAL0 es retención). Ninguna entra en
un paper.
"""
# ORIGEN-VALOR: 0.6847 — Omega_Lambda de Planck 2018 (arXiv:1807.06209)

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json as _jm_fig, sys as _sm_fig, os as _om_fig  # noqa: E402
_sm_fig.path.insert(0, _om_fig.path.join(_om_fig.path.dirname(_om_fig.path.abspath(__file__)), ".."))
from procedencia import acta as _acta_fig  # noqa: E402
# R75: cada figura lleva su acta en los metadatos del PDF/PNG (2026-10-21, al entrar a DVC)
_META = {"Keywords": "ACTA-PROCEDENCIA " + _jm_fig.dumps(_acta_fig(__file__))}
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
import sys as _sys
import json as _json
_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_sys.path.insert(0, os.path.join(_R, "src"))
from ssee_core import OMEGA_M_TOTAL, W0 as _W0, WA as _WA  # noqa: E402
TR   = 3 * (PHI + BETA)
MV   = PHI + PI + KV

W0_SSEE       = -TR / MV
WA_SSEE       = -P_sc / IGNIS   # denominador IGNIS, no el scaffold K_v: mismo valor, entidad distinta
assert abs(W0_SSEE - _W0) < 1e-12 and abs(WA_SSEE - _WA) < 1e-12   # la figura y el núcleo dicen lo mismo
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
_mom_txt = open(os.path.join(_R, "results/logs/desi_dr2_w0wa_momentos.log")).read()
_mom_txt = _mom_txt.split("\n", 1)[1]                  # la 1.ª línea es el acta
_MOM = _json.loads(_mom_txt[_mom_txt.index("{"):_mom_txt.rindex("}") + 1])["combos"]
def _kw(nombre):
    c = _MOM[nombre]
    return dict(w0c=c["w0_bf"], wac=c["wa_bf"], sig_w0=c["sigma_w0"], sig_wa=c["sigma_wa"], rho=c["rho"])
for _nom, _col, _a2, _a1, _lab in (
        ("DESI+CMB+Pantheon+ (DR2 ec.26)", "#2166AC", 0.18, 0.35, "DESI DR2+CMB+Pantheon+ 1σ/2σ"),
        ("DESI+CMB+DESY5 (DR2 ec.28)", "#4DAF4A", 0.12, 0.28, "DESI DR2+CMB+DESY5 1σ/2σ"),
        ("DESI+CMB+Union3 (DR2 ec.27)", "#D95F02", 0.12, 0.30, "DESI DR2+CMB+Union3 1σ/2σ")):
    covariance_ellipse(ax1, **_kw(_nom), n_sigma=2, color=_col, alpha=_a2, zorder=1)
    covariance_ellipse(ax1, **_kw(_nom), n_sigma=1, color=_col, alpha=_a1, zorder=2, label=_lab)
_SIG_PANT = _json.load(open(os.path.join(_R, "results/logs/paper2_w0wa.json")))["w0wa_ssee_vs_lcdm"]["ec26"]["ssee_sigma"]

# ΛCDM
ax1.scatter(-1.0, 0.0, marker="+", s=120, color="black", linewidths=2.5,
            zorder=6, label=r"$\Lambda$CDM ($w_0=-1,\,w_a=0$)")

# Punto SSEE
ax1.scatter(W0_SSEE, WA_SSEE, marker="*", s=260, color="#E6002B",
            edgecolors="black", linewidths=0.8, zorder=7,
            label=fr"SSEE ($w_0={W0_SSEE:.3f},\,w_a={WA_SSEE:.3f}$)")

# Cruz de incertidumbre SSEE (algebraica → 0, pero indicamos con símbolo)
ax1.annotate(
    fr"SSEE: {_SIG_PANT:.2f}$\sigma$ (Pantheon+)",
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
fig1.savefig(_outpath("fig1_w0wa_plane.pdf"), metadata=_META)
fig1.savefig(_outpath("fig1_w0wa_plane.png"), metadata=_META)
print("Fig 1 guardada: fig1_w0wa_plane.pdf/.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FIGURA 3 — Omega_DE: SSEE vs observaciones + diagrama estructural
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_DESI_W0WA = os.path.join(os.environ.get("SSEE_DATA_DIR", "/mnt/datos/SSEE_data"),
                          "desi_dr2_official/cosmology_chains/cobaya/base_w_wa")
_PLK = "planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_planck-NPIPE-highl-CamSpec-TTTEEE_planck-act-dr6-lensing"


def _omega_de_desi(sn):
    """Omega_DE (columna omegal) de la cadena oficial w0wa de DESI DR2: media y sigma con pesos, burn-in 30 %."""
    w, x = [], []
    for k in (1, 2, 3, 4):
        f = os.path.join(_DESI_W0WA, f"desi-bao-all_{sn}{_PLK}", f"chain.{k}.txt")
        cols = open(f).readline().lstrip("#").split()
        a = np.loadtxt(f)
        a = a[int(0.3 * len(a)):]
        w.append(a[:, cols.index("weight")]); x.append(a[:, cols.index("omegal")])
    w, x = np.concatenate(w), np.concatenate(x)
    m = np.average(x, weights=w)
    return float(m), float(np.sqrt(np.average((x - m) ** 2, weights=w)))


# ORIGEN-VALOR: 0.0073 — sigma de Omega_Lambda de Planck 2018 (arXiv:1807.06209, tabla 2, TT,TE,EE+lowE+lensing)
omega_obs = {
    "Planck 2018":          (0.6847, 0.0073),
    "DESI DR2\n+CMB":       _omega_de_desi(""),
    "DESI DR2\n+CMB+DESY5": _omega_de_desi("desy5sn_"),
}
print("Omega_DE de las cadenas DESI DR2 w0wa:", {k.replace(chr(10), " "): v for k, v in omega_obs.items()})

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
ax3a.legend(fontsize=8.5, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2)

# Anotación de la diferencia estructural
ax3a.annotate(
    "$s_{DE}=T_r/M_v$ is $|w_0|$,\nan equation-of-state\nnumber. It does not\nlive on this axis.",
    xy=(S_DE_SSEE, 1.0), xytext=(0.745, 1.25),
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
fig3.savefig(_outpath("fig3_omega_de.pdf"), metadata=_META)
fig3.savefig(_outpath("fig3_omega_de.png"), metadata=_META)
print("Fig 3 guardada: fig3_omega_de.pdf/.png")



print("\nFiguras 1 y 3 generadas (las 2 y 4 se retiraron el 2026-10-21, ver docstring).")
