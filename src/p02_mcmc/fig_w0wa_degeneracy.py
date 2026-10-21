#!/usr/bin/env python3
import os
import json
import sys
_SSEE_DATA = os.environ.get("SSEE_DATA_DIR") or ("/mnt/datos/SSEE_data" if os.path.isdir("/mnt/datos") else "results/data")  # portable: HDD si existe, si no results/ local
"""
Figura de robustez (Paper 2, 2026-06-14): la degeneracion w0-wa-H0.
Muestra que tres analisis independientes (full-pipeline Cobaya, BAO+Planck CPL,
y la prediccion algebraica SSEE) caen sobre la MISMA linea de degeneracion, y que
LCDM (w0=-1,wa=0) queda excluido mientras SSEE queda dentro.

Genera: results/figures/fig_w0wa_degeneracy.{pdf,png} (etapa DVC `fig_w0wa_degeneracy`).

2026-10-21: los puntos ya no van tecleados. El de SSEE sale de ssee_core; el de CPL,
de la corrida vigente de 3 modelos (resumen_3modelos.json, mediana); aquí decía
un par tecleado de un ajuste viejo, sin log. La σ de ΛCDM de la leyenda sale del log del
pipeline completo (mcmc_full_posteriores.json), el mismo que cita el pie de P2, y se
comprueba contra la que calcula esta figura con las mismas cadenas.
"""
import numpy as np, glob
import matplotlib.pyplot as plt
import json as _jm_fig, sys as _sm_fig, os as _om_fig  # noqa: E402
_sm_fig.path.insert(0, _om_fig.path.join(_om_fig.path.dirname(_om_fig.path.abspath(__file__)), ".."))
from procedencia import acta as _acta_fig  # noqa: E402
# R75: cada figura lleva su acta en los metadatos del PDF/PNG (2026-10-21, al entrar a DVC)
_META = {"Keywords": "ACTA-PROCEDENCIA " + _jm_fig.dumps(_acta_fig(__file__))}
from matplotlib.patches import Ellipse
from scipy.stats import chi2 as chi2dist

# ── Fase 4: pipeline completo (CAMB + plik_lite + lensing + DESI + fsigma8) ──
files = sorted(glob.glob(_SSEE_DATA + '/mcmc/mcmc_full/c*/ssee_full.1.txt'))
proc = [np.loadtxt(f)[int(0.3 * len(np.loadtxt(f))):] for f in files]
allc = np.vstack(proc)
W, w0, wa = allc[:, 0], allc[:, 8], allc[:, 9]

mu = np.array([np.average(w0, weights=W), np.average(wa, weights=W)])
d0, d1 = w0 - mu[0], wa - mu[1]
C = np.array([[np.average(d0 * d0, weights=W), np.average(d0 * d1, weights=W)],
              [np.average(d0 * d1, weights=W), np.average(d1 * d1, weights=W)]])
evals, evecs = np.linalg.eigh(C)
ang = np.degrees(np.arctan2(evecs[1, -1], evecs[0, -1]))

# ── puntos de referencia (leídos, no tecleados) ──
_R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(_R, 'src'))
from ssee_core import W0, WA  # noqa: E402
SSEE = (W0, WA)
_cpl = json.load(open(os.path.join(_R, 'results/logs/resumen_3modelos.json')))['modelos']['cpl']['posterior']
BAO_CPL = (_cpl['w0']['mediana'], _cpl['wa']['mediana'])
_MF = json.load(open(os.path.join(_R, 'results/logs/mcmc_full_posteriores.json')))['distancia_w0wa']
LCDM = (-1.0, 0.0)

fig, ax = plt.subplots(figsize=(7.4, 6.2))

# nube Fase 4 (submuestreo) + elipses 1/2 sigma
rng = np.random.default_rng(0)
idx = rng.choice(len(w0), min(30000, len(w0)), replace=False)
ax.scatter(w0[idx], wa[idx], s=2, c='0.78', alpha=0.25, rasterized=True, zorder=1)
# contornos de confianza 2D estandar: 68.3% (dchi2=2.30) y 95.4% (dchi2=6.18)
for dchi2, lw in [(2.30, 1.6), (6.18, 1.2)]:
    ax.add_patch(Ellipse(mu, 2 * np.sqrt(dchi2 * evals[-1]), 2 * np.sqrt(dchi2 * evals[0]),
                         angle=ang, fill=False, ec='tab:blue', lw=lw, zorder=3))

# la linea de degeneracion (eje principal)
t = np.linspace(-3, 3, 2)
line = mu[:, None] + evecs[:, -1:] * np.sqrt(evals[-1]) * t
ax.plot(line[0], line[1], 'b--', alpha=0.5, lw=1, zorder=2,
        label='degeneracy axis ($\\rho=%.2f$)' % (C[0, 1] / np.sqrt(C[0, 0] * C[1, 1])))

# the reference points + LCDM
ax.plot(*mu, 'o', ms=11, color='tab:blue', mec='k', zorder=5,
        label='Full pipeline (CAMB+CMB): %.3f, %.3f' % (mu[0], mu[1]))
ax.plot(*BAO_CPL, 's', ms=10, color='tab:orange', mec='k', zorder=5,
        label='BAO+Planck CPL (Paper 2 run, median): %.3f, %.3f' % BAO_CPL)
ax.plot(*SSEE, '*', ms=22, color='crimson', mec='k', zorder=6,
        label='SSEE algebraic: %.3f, %.3f' % SSEE)
ax.plot(*LCDM, 'X', ms=13, color='dimgray', mec='k', zorder=5,
        label='$\\Lambda$CDM (excluded at %.2f$\\sigma$)' % _MF['lcdm']['sigma'])

# significancia estandar (2 dof -> sigma equivalente via p-value, convencion DESI)
Cinv = np.linalg.inv(C)
def sig(p):
    d = np.array(p) - mu
    c2 = d @ Cinv @ d
    pval = chi2dist.sf(c2, 2)
    return np.sqrt(chi2dist.isf(pval, 1)) if pval > 0 else 99.0
ax.annotate('%.1f$\\sigma$' % sig(SSEE), SSEE, textcoords='offset points',
            xytext=(12, -4), color='crimson', fontsize=11, fontweight='bold')
ax.annotate('%.1f$\\sigma$' % sig(LCDM), LCDM, textcoords='offset points',
            xytext=(8, 8), color='dimgray', fontsize=11, fontweight='bold')

ax.set_xlabel('$w_0$'); ax.set_ylabel('$w_a$')
ax.set_title('Full-likelihood $w_0$-$w_a$ posterior: SSEE lies within the data-preferred region')
ax.legend(loc='lower left', fontsize=8.5, framealpha=0.95)
for _m in ('ssee', 'lcdm'):   # la figura y el log tienen que decir lo mismo
    _p = SSEE if _m == 'ssee' else LCDM
    assert abs(sig(_p) - _MF[_m]['sigma']) < 0.01, (_m, sig(_p), _MF[_m]['sigma'])
ax.set_xlim(-1.15, -0.45); ax.set_ylim(-1.9, 0.35)
ax.grid(alpha=0.2)
plt.tight_layout()
for ext in ('pdf', 'png'):
    plt.savefig(os.path.join(_R, f'results/figures/fig_w0wa_degeneracy.{ext}'), dpi=150, bbox_inches='tight', metadata=_META)
print('figura guardada. SSEE a %.2f sigma, LCDM a %.2f sigma del full pipeline.'
      % (sig(SSEE), sig(LCDM)))
