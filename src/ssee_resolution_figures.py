"""
Resolution figures — visual closure of claims that previously lived only in text/tables.
All values are canonical (VERIFICATION_LEDGER.md §Valores Canónicos); zero fitting.

Figure A: fig_rd_dual.pdf       — sound horizon r_d: SSEE physical value 147.17 Mpc
                                   (total matter Omega_m,CMB=0.308881, omega_m direct) vs
                                   Planck 147.09±0.26 Mpc and LCDM 147.3 Mpc. The 175.6 Mpc
                                   value is flagged as a CATEGORY ERROR: what one gets by
                                   wrongly inserting the cold sector 1+w0=0.160 into the
                                   background geometry (the DR2 bug, chi2_BAO=726).
Figure B: fig_s8_resolution.pdf — tres determinaciones independientes del UNICO
                                   A_s libre de SSEE (CMB, cizalla, clustering). La
                                   discrepancia es entre DATOS, no del modelo.

Outputs: results/figures/
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import sys as _s66
_s66.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ssee_core import OMEGA_M_TOTAL as _OMT


OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'figures')
os.makedirs(OUT, exist_ok=True)

# ════════════════════════════════════════════════════════════════════════════
# Figure A — dual r_d
# ════════════════════════════════════════════════════════════════════════════
RD_BUG   = 175.6    # Mpc — CATEGORY ERROR: cold sector 1+w0=0.160 wrongly in geometry
# (2026-09-29) RD_CMB y RD_LCDM se CALCULAN con CAMB (rd_camb.py); antes iban tecleados
# (147.17 y un 147.3 de Eisenstein-Hu). ΛCDM en los parámetros de Planck 2018 con SU mν.
from ssee_core import OMEGA_B_H2 as _WB, OMEGA_M_H2 as _WM, SUM_MNU_EV as _SM, OMEGA_NU_H2 as _WNU  # noqa: E402
from rd_camb import rd_mpc as _rd  # noqa: E402
_s66.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p11_sondas'))
from lcdm_planck import LCDM_PLANCK as _LP  # noqa: E402
RD_CMB   = _rd(_WB, _WM)   # Mpc — SSEE physical value, total matter (omega_m direct), CAMB
RD_PLANCK, RD_PLANCK_ERR = 147.09, 0.26   # Mpc, Planck 2018
RD_LCDM  = _rd(_LP['ombh2'], _LP['ombh2'] + _LP['omch2'] + _LP['mnu'] * _WNU / _SM, mnu=_LP['mnu'])  # Mpc — ΛCDM-Planck, CAMB

fig, ax = plt.subplots(figsize=(8.0, 4.2))

bars = [
    (r'Category error' + '\n' + r'($1+w_0=0.160$ in geometry)', RD_BUG,  '#d6604d'),
    (r'SSEE physical' + '\n' + r'($\Omega_{m,\rm CMB}=0.308881$)',  RD_CMB,  '#1a9641'),
    (r'$\Lambda$CDM (Planck 2018,' + '\n' + r'CAMB)',            RD_LCDM,  '#4393c3'),
]
ypos = np.arange(len(bars))[::-1]
for y, (lab, val, col) in zip(ypos, bars):
    hatch = '//' if col == '#d6604d' else None
    ax.barh(y, val, color=col, height=0.55, edgecolor='black', lw=0.6, zorder=3, hatch=hatch)
    tag = ' ✗' if col == '#d6604d' else (' ✓' if col == '#1a9641' else '')
    ax.text(val + 1.2, y, f'{val:.1f} Mpc{tag}', va='center', fontsize=10.5,
            fontweight='bold', color='#222222')

# Planck band
ax.axvspan(RD_PLANCK - RD_PLANCK_ERR, RD_PLANCK + RD_PLANCK_ERR,
           color='#777777', alpha=0.45, zorder=2)
ax.axvline(RD_PLANCK, color='#444444', lw=1.2, ls='--', zorder=2)
ax.text(RD_PLANCK, 2.62, r'Planck 2018: $147.09\pm0.26$ Mpc',
        ha='center', fontsize=9.5, color='#333333')

# Arrow: the bug -> the physical value (total matter density enters the geometry)
ax.annotate('', xy=(RD_CMB + 2, 1.42), xytext=(RD_BUG - 2, 2.0),
            arrowprops=dict(arrowstyle='-|>', lw=1.8, color='#222222',
                            connectionstyle='arc3,rad=0.25'))
ax.text(163, 1.86, r'total $\omega_m$ in geometry' + '\n' + r'($\omega_b+\omega_c+\omega_\nu$)',
        fontsize=9.5, ha='center', color='#222222', style='italic')

ax.set_yticks(ypos)
ax.set_yticklabels([b[0] for b in bars], fontsize=10)
ax.set_xlabel(r'Drag-epoch sound horizon $r_d$ [Mpc]', fontsize=11)
ax.set_xlim(140, 185)
ax.set_ylim(-0.55, 2.95)
ax.set_title(r'Sound horizon: SSEE physical value matches Planck; $175.6$ Mpc is the $0.160$-in-geometry bug',
             fontsize=10.5)
ax.grid(axis='x', lw=0.4, alpha=0.4, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout()
out_a = os.path.join(OUT, 'fig_rd_dual.pdf')
fig.savefig(out_a, bbox_inches='tight')
print(f"Saved: {out_a}")
plt.close(fig)

# ════════════════════════════════════════════════════════════════════════════
# Figure B — S8: challenge -> resolution
# ════════════════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────────────────────
# QUE MUESTRA ESTA FIGURA (reescrita 2026-08-01 tras correccion de Mike)
#
# La version anterior contaba un arco de redencion: "SSEE tenia 3.5 sigma y
# bajo a 0.11". Eso es FALSO y Mike lo corrigio. SSEE nunca tuvo esa tension.
#
# SSEE tiene UN parametro libre a este nivel: A_s. El fondo es identico en las
# tres columnas de abajo (fijado por algebra). Lo unico que cambia es a QUE
# DATO se le pide que fije A_s. Y ahi esta el punto:
#
#   - el CMB pide un A_s alto      -> S8 ~ 0.826
#   - la cizalla pide un A_s bajo  -> S8 ~ 0.756
#
# Esa discrepancia es ENTRE LOS DATOS, no una propiedad de SSEE. Existe igual
# en LCDM (es la tension Planck-KiDS de toda la vida) y no se le puede cobrar
# al modelo que se le ponga encima. Prueba: con el A_s del PROPIO CMB de SSEE
# (0.8142, no el de Planck) la discrepancia sigue en ~2.7 sigma.
# ─────────────────────────────────────────────────────────────────────────────
OM = _OMT
FAC = np.sqrt(OM / 0.3)

# Determinaciones de A_s (expresadas via sigma8), TODAS con el mismo fondo SSEE
DET = [
    (r'$A_s$ from raw cosmic shear' + '\n' + r'(KiDS-1000 $\xi_\pm$, this work)', 0.7446, 0.0189, '#1a9641'),
    (r'$A_s$ from SSEE fit to CMB' + '\n' + r'(Planck plik\_lite, raw)',          0.8142, 0.0053, '#4a6fa5'),
    (r'$A_s$ from galaxy clustering' + '\n' + r'(BOSS DR12 — in progress)',        None,   None,   '#999999'),
]
# Observaciones independientes, para referencia
S8_KIDS   = (0.759, 0.024)   # KiDS-1000 (Asgari+2021) — el DATO (NO 0.758: eso era la prediccion)
S8_DES    = (0.776, 0.017)
S8_PLANCK = (0.832, 0.013)

fig, ax = plt.subplots(figsize=(8.4, 4.8))

rows = []
for lab, s8, e8, col in DET:
    rows.append((lab, None if s8 is None else s8*FAC,
                 None if e8 is None else e8*FAC, col, True))
rows += [(r'KiDS-1000 (published)', S8_KIDS[0], S8_KIDS[1], '#888888', False),
         (r'DES-Y3 (published)',    S8_DES[0],  S8_DES[1],  '#888888', False),
         (r'Planck 2018 (published)', S8_PLANCK[0], S8_PLANCK[1], '#888888', False)]

ypos = np.arange(len(rows))[::-1]
for y, (lab, val, err, col, is_model) in zip(ypos, rows):
    if val is None:
        ax.annotate('pending', xy=(0.795, y), fontsize=9, color='#999999',
                    style='italic', va='center')
        continue
    ax.errorbar(val, y, xerr=err, fmt='o' if is_model else 's', ms=9 if is_model else 7,
                color=col, ecolor=col, elinewidth=2.2, capsize=5,
                markeredgecolor='black', mew=0.7, zorder=4)

ax.axhline(ypos[2] - 0.5, color='#cccccc', lw=1.0, ls='-', zorder=1)
ax.text(0.723, ypos[0] + 0.42, r'\textbf{SSEE, one free $A_s$}' if False
        else 'SSEE — one free $A_s$, same algebraic background',
        fontsize=9.5, color='#333333', fontweight='bold', va='bottom')
ax.text(0.723, ypos[3] + 0.42, 'Published constraints (for reference)',
        fontsize=9.5, color='#666666', va='bottom')

# la separacion entre las dos determinaciones de SSEE
lo, hi = 0.7446*FAC, 0.8142*FAC
ymid = (ypos[0] + ypos[1]) / 2
ax.annotate('', xy=(lo, ymid), xytext=(hi, ymid),
            arrowprops=dict(arrowstyle='<->', lw=1.5, color='#b2182b'))
ax.text((lo + hi) / 2, ymid + 0.13, r'$2.7\sigma$',
        fontsize=10, ha='center', va='bottom', color='#b2182b', fontweight='bold')
# La frase explicativa vive en el pie de figura del paper, no dentro del panel:
# dentro se montaba sobre el punto del CMB.

ax.set_yticks(ypos)
ax.set_yticklabels([r[0] for r in rows], fontsize=9.5)
ax.set_xlabel(r'$S_8 \equiv \sigma_8\,(\Omega_m/0.3)^{0.5}$', fontsize=11)
ax.set_xlim(0.718, 0.885)
ax.set_ylim(-0.75, len(rows) - 0.15)
ax.set_title('One model, one free amplitude, three independent determinations of it',
             fontsize=10.5)
ax.grid(axis='x', lw=0.4, alpha=0.4, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout()
out_b = os.path.join(OUT, 'fig_s8_resolution.pdf')
fig.savefig(out_b, bbox_inches='tight')
print(f"Saved: {out_b}")
