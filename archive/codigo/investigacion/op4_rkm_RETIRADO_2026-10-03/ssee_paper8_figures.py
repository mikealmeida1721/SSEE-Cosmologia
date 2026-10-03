"""
Figures for SSEE Paper 8: Strong gravity, disformal lensing, k-mouflage screening.
Generates:
  - fig_paper8_vainshtein.pdf : r_km vs M_obj (k-mouflage, Brax & Valageas 2014)
  - fig_paper8_lensing_ratio.pdf : theta_E^SSEE / theta_E^GR vs k/k_fs
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'figures')
os.makedirs(OUT, exist_ok=True)

# ── SSEE constants ────────────────────────────────────────────────────────────
phi  = (1 + 5**0.5) / 2
pi   = np.pi
AURA = (3*phi + pi) / 2    # ≈ 3.998
MIRA = AURA / 2             # ≈ 1.999
c    = 3e8                  # m/s
Msun = 1.989e30             # kg
Mpc  = 3.0857e22            # m

# K-mouflage constants (natural units: ℏ=c=1)
# M = 9.68 meV = Λ_SSEE  (Paper 10: M^4 = 5φ^8 ρ_crit, display canónico)
M_eV   = 9.68e-3            # eV
M_Pl_eV = 2.435e27          # eV  (reduced Planck mass)
Msun_eV = Msun * c**2 / 1.602e-19  # kg→eV
hbar_c_eVm = 1.9733e-7      # ℏc in eV·m  (1 eV^-1 = 1.9733e-7 m)

# ── Figure 1: K-mouflage radius r_km vs object mass ──────────────────────────
# r_km^3 = M_obj / (4π M_Pl M²)   [Brax & Valageas 2014, eq. for static source]
# (natural units, then convert to meters via ℏc)

M_range = np.logspace(-1, 18, 500)  # in Msun
M_obj_eV = M_range * Msun_eV

r_km3_nu = M_obj_eV / (4 * pi * M_Pl_eV * M_eV**2)  # eV^-3
r_km_nu  = r_km3_nu**(1/3)                            # eV^-1
r_km_m   = r_km_nu * hbar_c_eVm                       # meters
r_km_kpc = r_km_m / (Mpc * 1e-3)                      # kpc

fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(M_range, r_km_kpc, 'k-', lw=2)

# Annotate representative objects with their physical radii for comparison
objects = [
    (1,     r'Sun ($1\,M_\odot$)',           'below'),
    (1e6,   r'M31 core ($10^6\,M_\odot$)',   'above'),
    (1e12,  r'Milky Way ($10^{12}\,M_\odot$)', 'above'),
    (1e15,  r'Cluster ($10^{15}\,M_\odot$)', 'above'),
]
for m, name, pos in objects:
    m_ev = m * Msun_eV
    r_nu = (m_ev / (4*pi * M_Pl_eV * M_eV**2))**(1/3)
    r_kpc = r_nu * hbar_c_eVm / (Mpc * 1e-3)
    ax.plot(m, r_kpc, 'o', color='#d6604d', ms=8, zorder=5)
    dy = 0.6 if pos == 'above' else -0.6
    ax.annotate(name, xy=(m, r_kpc),
                xytext=(m*1.5, r_kpc * 10**dy),
                fontsize=8.5, ha='left', color='#d6604d',
                arrowprops=dict(arrowstyle='->', color='#d6604d', lw=0.8))

# Mark 1 kpc reference line
ax.axhline(1.0, color='#2166ac', lw=1.0, ls='--', alpha=0.7, label=r'$1\,\mathrm{kpc}$')
ax.set_xlabel(r'Object mass $M_{\rm obj}$ [$M_\odot$]', fontsize=11)
ax.set_ylabel(r'K-mouflage radius $r_{\rm km}$ [kpc]', fontsize=11)
ax.set_title(r'SSEE k-mouflage: $r_{\rm km}^3 = M_{\rm obj}\,/\,(4\pi M_{\rm Pl} M^2)$,'
             r'$\quad M=9.68\,\mathrm{meV}$', fontsize=10)
ax.legend(fontsize=9)
ax.grid(which='both', lw=0.4, alpha=0.4)
ax.set_xlim(0.05, 1e18)
fig.tight_layout()
out1 = os.path.join(OUT, 'fig_paper8_vainshtein.pdf')
fig.savefig(out1, bbox_inches='tight')
fig.savefig(out1.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"Saved: {out1}")

# Print numerical check
r_sun_m = (Msun_eV / (4*pi * M_Pl_eV * M_eV**2))**(1/3) * hbar_c_eVm
print(f"  r_km(Sun)       = {r_sun_m:.3e} m  (R_sun = 6.96e8 m)")
print(f"  r_km(MW 1e12)   = {r_sun_m * 1e4:.3e} m  (~1 AU = 1.50e11 m)")
print(f"  r_km(cluster 1e15) = {r_sun_m * 1e5:.3e} m")

# ── Figure 2 RETIRADA 2026-09-19 ───────────────────────────────────────────
# Aqui se dibujaba `fig_paper8_lensing_ratio`: la razon theta_E^SSEE/theta_E^GR
# construida como `1 + (MIRA-1)*T_WDM(k)` con k_fs = 0.754 h/Mpc,
# alpha_WDM = 1.117 Mpc/h y m_phi = 40.70 eV. Los tres son de la particula
# phi-DM, retirada el 2026-08-01, asi que la figura entera colgaba de una
# entidad que ya no existe.
#
# Por que se quita y no se rehace: la prediccion de lensing de Paper 8 SI
# sobrevive —se rescato el 2026-08-02 sobre omega_c = KAL0*omega_b*n_s (OP-8)
# y alpha_B = alpha_M = 0 de Paper 7— pero esta figura NO era esa prediccion:
# era una ilustracion cualitativa del corte por free-streaming, que es
# justamente la parte que murio. Y el .tex de Paper 8 nunca la incluyo: solo
# incluye `fig_paper8_vainshtein.pdf` (linea 602). Era huerfana ademas de
# rancia.
#
# El PDF y el PNG que quedaban en results/figures se borran con ella.


print(f"\nPaper 8 constants check:")
print(f"  AURA = {AURA:.6f}")
print(f"  MIRA = {MIRA:.6f}")
