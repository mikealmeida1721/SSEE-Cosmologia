"""
Resolution figures — visual closure of claims that otherwise live only in text/tables.
Every number drawn here is READ (CAMB, a sealed log, or a literal extract of the
published table); none is typed. All of them are written to results/logs/rd_dual.json
with their source, and the stage `rd_dual` (dvc.yaml) seals that log and both figures.

Figure A: fig_rd_dual.pdf       — drag-epoch sound horizon r_d. SSEE with the full
                                   algebraic omega_m (CAMB) against Planck 2018 and
                                   against LCDM at the Planck parameters (same code).
Figure B: fig_s8_resolution.pdf — S8 on the algebraic background of SSEE: the
                                   prediction with A_s fixed to the model's own CMB
                                   fit (KiDS-Legacy, the headline), A_s fitted to the
                                   raw shear (KiDS-Legacy and, as antecedent, KiDS-1000),
                                   the LCDM control, and the published constraints.

2026-10-03 (rewritten). Figure A used to carry a third bar, 175.6 Mpc, labelled
«category error»: r_d with s_m = 1+w0 = 0.160 put in the density slot. s_m is an
equation-of-state number, not a density, so that bar was not a version of the model
and is removed (as the equivalent curve was removed from Paper 3); the figure keeps
only physical values. Figure B used to show KiDS-1000 against the CMB with a 2.7 sigma
arrow and BOSS «in progress»; KiDS-Legacy (2026-09-20) closed that, and the headline
is now the prediction with A_s fixed to the model's CMB. Both old versions, and their
typed numbers (175.6, 147.09, 0.7446, 0.8142, 0.759, 0.776, 0.832), are retired.

Outputs: results/figures/, results/logs/rd_dual.json
"""
import json
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import yaml  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, 'p11_sondas'))
from ssee_core import OMEGA_B_H2 as _WB, OMEGA_M_H2 as _WM, SUM_MNU_EV as _SM, OMEGA_NU_H2 as _WNU  # noqa: E402
from rd_camb import rd_mpc as _rd  # noqa: E402
from lcdm_planck import LCDM_PLANCK as _LP  # noqa: E402
from planck2018_tabla2 import lee as _planck  # noqa: E402
from procedencia import con_acta  # noqa: E402

OUT = os.path.join(REPO, 'results', 'figures')
os.makedirs(OUT, exist_ok=True)
KIDS = os.path.join(REPO, 'results', 'logs', 'kids_publicados.json')
CANON = os.path.join(REPO, 'CANONICAL_VALUES.yaml')
TABLA2 = os.path.join(REPO, 'data', 'raw', 'planck2018_VI', 'tabla2.tex')

# ════════════════════════════════════════════════════════════════════════════
# Figure A — r_d
# ════════════════════════════════════════════════════════════════════════════
RD_SSEE = _rd(_WB, _WM)                                    # SSEE: total algebraic omega_m, CAMB
RD_LCDM = _rd(_LP['ombh2'], _LP['ombh2'] + _LP['omch2'] + _LP['mnu'] * _WNU / _SM, mnu=_LP['mnu'])
RD_PLANCK, RD_PLANCK_ERR = _planck('r_drag')               # Planck 2018 VI, Tabla 2, TT,TE,EE+lowE+lensing
SIG_SSEE = (RD_SSEE - RD_PLANCK) / RD_PLANCK_ERR
SIG_LCDM = (RD_LCDM - RD_PLANCK) / RD_PLANCK_ERR

fig, ax = plt.subplots(figsize=(8.0, 3.2))
ax.axvspan(RD_PLANCK - RD_PLANCK_ERR, RD_PLANCK + RD_PLANCK_ERR, color='#777777', alpha=0.35, zorder=1)
ax.axvline(RD_PLANCK, color='#444444', lw=1.2, ls='--', zorder=2)
ax.text(RD_PLANCK, 1.62, rf'Planck 2018: ${RD_PLANCK:.2f}\pm{RD_PLANCK_ERR:.2f}$ Mpc',
        ha='center', fontsize=9.5, color='#333333')
filas = [(r'SSEE (algebraic $\omega_m$, CAMB)', RD_SSEE, SIG_SSEE, '#1a9641'),
         (r'$\Lambda$CDM at Planck 2018 (CAMB)', RD_LCDM, SIG_LCDM, '#4393c3')]
for y, (lab, val, sg, col) in zip([1, 0], filas):
    ax.plot(val, y, 'o', ms=11, color=col, markeredgecolor='black', mew=0.7, zorder=4)
    ax.text(val + 0.06, y + 0.18, f'{val:.2f} Mpc  ({sg:+.2f}$\\sigma$)', fontsize=10, color='#222222')
ax.set_yticks([1, 0])
ax.set_yticklabels([f[0] for f in filas], fontsize=10)
ax.set_xlabel(r'Drag-epoch sound horizon $r_d$ [Mpc]', fontsize=11)
pad = 4 * RD_PLANCK_ERR
ax.set_xlim(min(RD_SSEE, RD_LCDM, RD_PLANCK) - pad, max(RD_SSEE, RD_LCDM, RD_PLANCK) + pad)
ax.set_ylim(-0.6, 2.0)
ax.set_title('Sound horizon: the full algebraic matter density gives the Planck value', fontsize=10.5)
ax.grid(axis='x', lw=0.4, alpha=0.4, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout()
out_a = os.path.join(OUT, 'fig_rd_dual.pdf')
fig.savefig(out_a, bbox_inches='tight')
plt.close(fig)
print(f'r_d SSEE {RD_SSEE:.3f} ({SIG_SSEE:+.2f} sigma)  LCDM-Planck {RD_LCDM:.3f} ({SIG_LCDM:+.2f} sigma)  '
      f'Planck {RD_PLANCK}±{RD_PLANCK_ERR}')

# ════════════════════════════════════════════════════════════════════════════
# Figure B — S8 on the algebraic background
# ════════════════════════════════════════════════════════════════════════════
K = json.load(open(KIDS))
S = K['s8']
LEG = K['kids_legacy']
with open(os.path.join(REPO, 'results', 'logs', 's8_kids_legacy_camb.json')) as f:
    LIB = json.load(f)['libre']
C = yaml.safe_load(open(CANON))
_obs = {k: v for blk in C.values() if isinstance(blk, dict) for k, v in blk.items()}
# la sigma de DES-Y3 vive en el comentario de su ancla en CANONICAL («# DES-Y3 S8; ±σ»)
DES = next((_obs['obs_DES_S8'], float(ln.split('±')[1].split()[0]))
           for ln in open(CANON) if ln.strip().startswith('obs_DES_S8:'))
PLANCK_S8 = _planck('S8')

model = [  # (label, S8, sigma or None, colour, marker)
    ('SSEE, $A_s$ fixed to its own CMB fit\n(KiDS-Legacy era; no free cosmological parameter)',
     S['legacy_prediccion']['S8'], None, '#7a3fb5', 'D'),
    ('SSEE, $A_s$ fitted to raw KiDS-Legacy $\\xi_\\pm$', LIB['S8'], LIB['S8_sigma'], '#1a9641', 'o'),
    ('SSEE, $A_s$ fitted to raw KiDS-1000 $\\xi_\\pm$\n(antecedent)', S['k1000_ssee']['S8'],
     S['k1000_ssee']['S8_sigma'], '#66a61e', 'o'),
    ('$\\Lambda$CDM control, raw KiDS-1000 $\\xi_\\pm$', S['k1000_lcdm']['S8'], S['k1000_lcdm']['S8_sigma'],
     '#4393c3', 's'),
]
publ = [
    ('KiDS-Legacy (published chain)', LEG['S8'], LEG['S8_sigma']),
    ('KiDS-1000 (published)', S['k1000_dato']['S8'], S['k1000_dato']['S8_sigma']),
    ('DES-Y3 (published)', DES[0], DES[1]),
    ('Planck 2018 (published)', PLANCK_S8[0], PLANCK_S8[1]),
]
fig, ax = plt.subplots(figsize=(8.6, 5.0))
ax.axvspan(LEG['S8'] - LEG['S8_sigma'], LEG['S8'] + LEG['S8_sigma'], color='#7a3fb5', alpha=0.10, zorder=1)
n = len(model) + len(publ)
ys = np.arange(n)[::-1]
for y, (lab, v, e, col, mk) in zip(ys[:len(model)], model):
    if e is None:
        ax.plot(v, y, mk, ms=10, color=col, markeredgecolor='black', mew=0.7, zorder=4)
    else:
        ax.errorbar(v, y, xerr=e, fmt=mk, ms=9, color=col, ecolor=col, elinewidth=2.2, capsize=5,
                    markeredgecolor='black', mew=0.7, zorder=4)
for y, (lab, v, e) in zip(ys[len(model):], publ):
    ax.errorbar(v, y, xerr=e, fmt='s', ms=7, color='#888888', ecolor='#888888', elinewidth=2,
                capsize=5, markeredgecolor='black', mew=0.6, zorder=4)
ax.axhline(ys[len(model) - 1] - 0.5, color='#cccccc', lw=1.0, zorder=1)
ax.set_yticks(ys)
ax.set_yticklabels([m[0] for m in model] + [p[0] for p in publ], fontsize=8.8)
ax.set_xlabel(r'$S_8 \equiv \sigma_8\,(\Omega_m/0.3)^{0.5}$', fontsize=11)
allv = [m[1] for m in model] + [p[1] for p in publ]
ax.set_xlim(min(allv) - 0.05, max(allv) + 0.05)
ax.set_ylim(-0.7, n - 0.3)
ax.set_title('One algebraic background: the CMB-fixed prediction and the shear data', fontsize=10.5)
ax.grid(axis='x', lw=0.4, alpha=0.4, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout()
out_b = os.path.join(OUT, 'fig_s8_resolution.pdf')
fig.savefig(out_b, bbox_inches='tight')
plt.close(fig)

res = dict(
    rd_ssee_camb=RD_SSEE, rd_lcdm_planck_camb=RD_LCDM,
    rd_planck_medido=[RD_PLANCK, RD_PLANCK_ERR], rd_ssee_sigmas=SIG_SSEE, rd_lcdm_sigmas=SIG_LCDM,
    s8_figura=dict(modelo={m[0]: [m[1], m[2]] for m in model}, publicados={p[0]: [p[1], p[2]] for p in publ}),
    fuentes=dict(rd='src/rd_camb.py (CAMB)', planck='data/raw/planck2018_VI/tabla2.tex (columna 5)',
                 s8='results/logs/kids_publicados.json y s8_kids_legacy_camb.json', des='CANONICAL_VALUES.yaml obs_DES_S8'),
    script='src/ssee_resolution_figures.py')
json.dump(con_acta(res, __file__, entradas=[KIDS, CANON, TABLA2,
                                             os.path.join(REPO, 'results', 'logs', 's8_kids_legacy_camb.json')]),
          open(os.path.join(REPO, 'results', 'logs', 'rd_dual.json'), 'w'), indent=1)
print(f'Saved: {out_a}, {out_b}')
