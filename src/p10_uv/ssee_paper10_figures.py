"""
Figures for SSEE Paper 10: UV completion via K(X) = X/KAL + X^2/M^4.
Generates:
  - fig_paper10_KX_profile.pdf   : K(X)/X vs X/M^4 — IR vs UV kinetic regimes
  - fig_paper10_alphaK_vs_alpha.pdf : H0_local vs alpha (cross-epoch falsification)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'figures')
os.makedirs(OUT, exist_ok=True)

# ── SSEE algebraic constants ──────────────────────────────────────────────────
phi   = (1 + 5**0.5) / 2
pi    = np.pi
Omega = phi + pi
AURA  = (3*phi + pi) / 2
MIRA  = AURA / 2
KAL0  = (phi + 3*pi) / 2  # ≈ 5.5214
alpha_att = phi**4 / 3     # ≈ 2.2847  (alpha-attractor)
# 3*Omega**2 es un NUMERO PURO: blanco de comparacion, NO entrada
NUM_ALG   = 3*Omega**2     # ≈ 67.9621  puro, sin unidades
H0_SHOES  = 73.04          # km/s/Mpc  MEDIDO -> unica entrada legitima
SIG_SHOES = 1.04
# UV cutoff: M^4 = 45 alpha^2 rho_c  (Paper 10 Postulate C.1)
# alphaK_IR = (phi+pi-Omega) already ≈ 0 … use Bellini-Sawicki definition
alphaK_IR  = 3*AURA*(pi - phi) / (2*Omega**2)   # ≈ 0.40330
# alphaK_UV quadratic correction:
# alphaK_full = alphaK_IR * (1 + delta), where delta = 3/(45*alpha_att^2) * (X_bg/rho_c)
# For background X_bg/rho_c ≈ 2*KAL0*(1+w0)*Omega_DE*H0^2/(3*H0^2) ... algebraic route:
# alphaK_full = alphaK_IR + (3/M^4) * X_bg^2  → Paper 10 gives 0.41691
# s_K^full CALCULADO (no hardcodeado): raiz de la cuadratica
#   4 X^2/M4 + 2 X/KAL - rho_phi(1+w0) = 0,  rho_c = 1
_M4  = 45*alpha_att**2
_rhs = alphaK_IR/3.0
_X   = (-2/KAL0 + (4/KAL0**2 + 16*_rhs/_M4)**0.5)/(8/_M4)
alphaK_UV = alphaK_IR + 24*_X*_X/_M4

fscreen_IR = alphaK_IR / (3*MIRA)    # 0.06725
fscreen_UV = alphaK_UV / (3*MIRA)    # 0.06952
# SH0ES ENTRA, H_global SALE
H0_UV    = H0_SHOES * (1 - fscreen_UV)   # ≈ 67.96214
SIG_GLOB = SIG_SHOES * (1 - fscreen_UV)  # ≈ 0.968 (con f completo; 0.970 es el del régimen IR)

# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: K(X)/X vs X/M^4
# ─────────────────────────────────────────────────────────────────────────────
# K(X) = X/KAL0 + X^2/M^4
# K(X)/X = 1/KAL0 + X/M^4
# Let u = X/M^4 (dimensionless kinetic ratio)

u = np.logspace(-5, 2, 500)
KX_over_X = 1/KAL0 + u   # K(X)/X = 1/KAL0 + X/M^4

# Mark regimes
# Background kinetic ratio on the x-axis u = X/M^4:
#   X_bg^UV = 0.36490 (rho_crit units), M^4 = 5 phi^8 rho_crit = 234.887
#   u_bg = X_bg/M^4 = 1.553e-3   (NOTE: the perturbativity parameter of the
#   paper is eps = X_bg^2/M^4 = 5.67e-4 — a DIFFERENT quantity, not this axis)
M4   = 5 * phi**8            # = 45*alpha_att^2 = 234.887 (rho_crit units)
# ORIGEN-VALOR: 0.36490 — X_bg_UV/rho_crit = 13.643945/37.393588 meV^4 = 0.364874 (src/p10_uv/ssee_paper10_verification.py, Step 3). El literal difiere en 3e-5; figura ilustrativa
# ORIGEN-VALOR: 0.01361 — s_K_UV - s_K_IR = 0.41690518 - 0.40330246 = 0.01360 (ssee_paper10_verification.py); 0.41691 - 0.40330 = 0.01361 con los redondeados
X_bg = 0.36490               # background X (rho_crit units, Paper 10 §4)
u_bg = X_bg / M4             # = 1.553e-3

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.loglog(u, KX_over_X, 'k-', lw=2, label=r'$K(X)/X = 1/\mathrm{KAL}_0 + X/M^4$')
ax.loglog(u, np.ones_like(u)/KAL0, '--', color='#2166ac', lw=1.2,
          label=fr'IR limit: $1/\mathrm{{KAL}}_0 = {1/KAL0:.4f}$')
ax.loglog(u, u, ':', color='#d6604d', lw=1.2, label=r'UV limit: $X/M^4$')
ax.axvline(u_bg, color='gray', lw=1, ls='-.', alpha=0.7,
           label=fr'Background $X_{{\rm bg}}/M^4={u_bg:.2e}$')
ax.axvline(1.0, color='#1a9641', lw=0.9, ls='--', alpha=0.7,
           label=r'Non-linear onset: $X = M^4$')
ax.fill_betweenx([0.05, 1.5], 1e-5, u_bg*5, alpha=0.06, color='#2166ac',
                 label='Linear (background) regime')
ax.fill_betweenx([0.05, 1.5], 0.2, 100, alpha=0.06, color='#d6604d',
                 label='Non-linear (Vainshtein) regime')

ax.set_xlabel(r'$u \equiv X/M^4$', fontsize=11)
ax.set_ylabel(r'$K(X)/X$', fontsize=11)
ax.set_title(r'SSEE kinetic function $K(X)=X/\mathrm{KAL}_0 + X^2/M^4$: IR$\to$UV crossover',
             fontsize=9.5)
ax.set_xlim(1e-5, 1e2)
ax.set_ylim(5e-3, 1.5e2)
ax.legend(fontsize=7.5, loc='upper left', ncol=2)
ax.grid(which='both', lw=0.4, alpha=0.4)
fig.tight_layout()
out1 = os.path.join(OUT, 'fig_paper10_KX_profile.pdf')
fig.savefig(out1, bbox_inches='tight')
fig.savefig(out1.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"Saved: {out1}")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: H0_local vs alpha (cross-epoch falsification test)
# ─────────────────────────────────────────────────────────────────────────────
# If LiteBIRD measures r, then alpha changes, M^4 changes, alphaK_full changes,
# H0_local changes.
# alphaK_full(alpha) = alphaK_IR + delta_alphaK(alpha)
# where delta_alphaK ~ 3/(45*alpha^2) * (X_bg/M^4) * (alphaK_IR)
# More precisely: alphaK_UV - alphaK_IR = 0.41691 - 0.40330 = 0.01361
# at alpha = phi^4/3 = 2.2847.
# Scaling: delta_alphaK ∝ 1/alpha^2  (since M^4 ∝ alpha^2 and X_bg is fixed)
delta_IR = alphaK_UV - alphaK_IR   # 0.01361 at alpha = alpha_att

alpha_range = np.linspace(0.5, 6, 400)
delta_alpha = delta_IR * (alpha_att / alpha_range)**2
alphaK_full_arr = alphaK_IR + delta_alpha
fscreen_arr = alphaK_full_arr / (3*MIRA)
H0_arr = H0_SHOES * (1 - fscreen_arr)   # SH0ES entra, H_global sale

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)

ax1.plot(alpha_range, alphaK_full_arr, 'k-', lw=2)
ax1.axvline(alpha_att, color='#1a9641', ls='--', lw=1.3, alpha=0.8,
            label=fr'$\alpha=\varphi^4/3={alpha_att:.4f}$ (this work)')
ax1.axhline(alphaK_UV, color='gray', ls=':', lw=1, alpha=0.7)
ax1.axhline(alphaK_IR, color='#2166ac', ls='-.', lw=1, alpha=0.7,
            label=fr'IR limit $\alpha_K^{{IR}}={alphaK_IR:.5f}$')
ax1.set_ylabel(r'$s_K^{\rm full}(\alpha)$', fontsize=10)
ax1.legend(fontsize=8.5, loc='upper right')
ax1.grid(lw=0.4, alpha=0.4)
ax1.annotate(fr'UV value: {alphaK_UV:.5f}',
             xy=(alpha_att, alphaK_UV), xytext=(alpha_att+0.5, alphaK_UV+0.003),
             fontsize=8, arrowprops=dict(arrowstyle='->', lw=0.8), color='#1a9641')

ax2.plot(alpha_range, H0_arr, color='#1a9641', lw=2,
         label=r'$H_0^{\rm glob}(\alpha)=H_0^{\rm SH0ES}(1-f)$')
ax2.axvline(alpha_att, color='#1a9641', ls='--', lw=1.3, alpha=0.8)
ax2.fill_between(alpha_range, NUM_ALG-SIG_GLOB, NUM_ALG+SIG_GLOB,
                 color='#d6604d', alpha=0.10)
ax2.axhline(NUM_ALG, color='#2166ac', ls=':', lw=1.2,
            label=r'$3(\varphi+\pi)^2=67.9621$ (pure target)')
ax2.set_xlabel(r'$\alpha$-attractor curvature parameter', fontsize=11)
ax2.set_ylabel(r'$H_0^{\rm glob}$ [km s$^{-1}$ Mpc$^{-1}$]', fontsize=10)
ax2.set_ylim(65.5, 70.5)
ax2.legend(fontsize=8.5, loc='upper right')
ax2.grid(lw=0.4, alpha=0.4)
ax2.annotate(fr'$H_0^{{\rm glob,UV}}={H0_UV:.5f}$',
             xy=(alpha_att, H0_UV), xytext=(alpha_att+0.3, H0_UV+0.6),
             fontsize=8.5, color='#1a9641',
             arrowprops=dict(arrowstyle='->', lw=0.8, color='#1a9641'))

fig.suptitle(r'Cross-epoch falsification: $H_0^{\rm glob}$ vs inflationary $\alpha$'
             r' (LiteBIRD measures $r \Rightarrow \alpha$; this shifts the UV prediction)',
             fontsize=9.5)
fig.tight_layout()
out2 = os.path.join(OUT, 'fig_paper10_alphaK_vs_alpha.pdf')
fig.savefig(out2, bbox_inches='tight')
fig.savefig(out2.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"Saved: {out2}")

print(f"\nPaper 10 constants check:")
print(f"  KAL0         = {KAL0:.6f}")
print(f"  alpha_att    = {alpha_att:.7f}")
print(f"  alphaK_IR    = {alphaK_IR:.5f}")
print(f"  alphaK_UV    = {alphaK_UV:.5f}")
print(f"  fscreen_IR   = {fscreen_IR:.6f}")
print(f"  fscreen_UV   = {fscreen_UV:.6f}")
print(f"  H0_glob UV (from SH0ES) = {H0_UV:.6f} +/- {SIG_GLOB:.4f}")
print(f"  residual vs NUM_ALG     = {H0_UV-NUM_ALG:+.3e}")
print(f"  u_bg = X_bg/M^4               = {u_bg:.4e}")
print(f"  eps  = X_bg^2/M^4             = {X_bg**2/M4:.4e}")
