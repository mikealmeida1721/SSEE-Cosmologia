"""
README hero figure: canonical SSEE tension summary (horizontal sigma bars).
All values are canonical (VERIFICATION_LEDGER.md §Valores Canónicos).
Output: results/figures/fig_readme_tensions.png
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'figures')
os.makedirs(OUT, exist_ok=True)

# (label, tension_sigma, reference dataset)
#
# CORREGIDO 2026-09-19. Esta figura es la PORTADA del README y llevaba dos
# filas retiradas el 2026-08-01 con la particula:
#   - «S_8 (two-sector phi-DM) 0.04 sigma»: el sector phi-DM esta retirado, y
#     ese 0.04 se medira contra el estadistico COMPRIMIDO con A_s fijado a
#     Planck. El canonico es el MCMC R3 contra el dato CRUDO, un solo sector
#     y A_s libre: S_8 = 0.7555 +- 0.0192 -> 0.11 sigma de KiDS-1000
#     (0.759 +- 0.024). Fuente: CANONICAL_VALUES.yaml `S8_kids_mcmc`.
#   - «mean f sigma_8 0.93 sigma»: ese 0.93 era la variante two-sector CON
#     free-streaming, retirada con la particula. El vigente es el de un solo
#     sector, 0.70 sigma (Paper 5, sigma_8 = 0.8136). Y hay que decir lo que
#     todavia NO esta: el f sigma_8 canonico contra BOSS crudo esta PENDIENTE
#     (R1/R2 con LPT). Fuente: CANONICAL_VALUES.yaml `fsigma8_single_sigma`.
# La fila del S_8 sobrevivio porque la barre R60 en el CODIGO, pero la figura
# es un .png y el barrido de figuras lee capa de texto de PDF: un .png no
# tiene. El agujero queda anotado aparte.
# 2026-10-02: cada barra se LEE de su log o se calcula del nucleo contra el dato
# crudo; antes todas iban tecleadas (y dos rancias: el S8 de KiDS-1000, superado
# por KiDS-Legacy, y el H_0 IR 68.13, que no es el canonico).
import csv
import json
import sys
_R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(_R, 'src'))
import ssee_core as S  # noqa: E402


def _log(rel, *ruta):
    o = json.load(open(os.path.join(_R, 'results', 'logs', rel)))
    for k in ruta:
        o = o[k]
    return float(o)


_pl = {r['parameter']: (float(r['mean']), float(r['sigma']))
       for r in csv.DictReader(l for l in open(os.path.join(_R, 'data', 'raw', 'planck2018_prior.csv'))
                               if not l.startswith('#'))}
NS_PLANCK = (0.9649, 0.0042)  # ORIGEN-VALOR: 0.9649 ± 0.0042 — Planck 2018 VI (A&A 641, A6), Tabla 2, TT,TE,EE+lowE+lensing


def _t(x, ref):
    return abs(x - ref[0]) / ref[1]


entries = [
    (r'$S_8$ predicted ($A_s$ fixed by the CMB)',
     _log('kids_publicados.json', 's8', 'legacy_prediccion', 'tension_sigma'), 'KiDS-Legacy (raw)'),
    (r'$n_s = 1-\varphi^{-7}$', _t(S.N_S, NS_PLANCK), 'Planck 2018'),
    (r'$w_0$–$w_a$ plane',
     _log('paper2_w0wa.json', 'w0wa_ssee_vs_lcdm', 'ec26', 'ssee_sigma'), 'DESI DR2 (Pantheon+)'),
    (r'$r_d$ (joint posterior)',
     _log('mcmc_full_posteriores.json', 'tensiones', 'rdrag', 'tension_abs'), 'MCMC multi-probe'),
    (r'$\Omega_b h^2 = (\pi-\varphi)/3\Omega^2$', _t(S.OMEGA_B_H2, _pl['Omega_b_h2']), 'Planck 2018'),
    (r'$\Omega_{m} = \omega_m/h^2$', _t(S.OMEGA_M_TOTAL, _pl['Omega_m']), 'Planck 2018'),
    (r'mean $f\sigma_8$ (6 RSD surveys)', _log('fsigma8_canonico.json', 'tension_media_ssee'), 'one sector'),
    (r'$H_0$ posterior (DESI DR2)', _log('mcmc_paper2_reframe.json', 'sigma_a_Hglob'),
     r'$H_0^{\rm glob}=H_0^{\rm SH0ES}(1-f_{\rm screen})$'),
]
# Ordenado POR sigma, no a mano. Antes la lista se escribia ordenada y se
# invertia; con eso el H_0 (0.17) llevaba tiempo al fondo fuera de sitio, y al
# bajar f sigma_8 de 0.93 a 0.70 se descolocaba tambien. Que lo ordene el
# codigo: la figura promete «smallest tension on top» y ahora lo cumple.
entries = sorted(entries, key=lambda e: e[1], reverse=True)

labels = [e[0] for e in entries]
sig    = [e[1] for e in entries]
refs   = [e[2] for e in entries]

fig, ax = plt.subplots(figsize=(8.2, 4.6))
colors = ['#1a9641' if s < 1 else '#fdae61' for s in sig]
bars = ax.barh(range(len(sig)), sig, color=colors, height=0.62,
               edgecolor='black', lw=0.5, zorder=3)

for i, (s, r) in enumerate(zip(sig, refs)):
    ax.text(s + 0.04, i, fr'{s:.2f}$\sigma$  ·  {r}', va='center',
            fontsize=9, color='#333333')

ax.axvline(1.0, color='#999999', ls='--', lw=1.0, zorder=2)
ax.axvline(2.0, color='#d6604d', ls='--', lw=1.0, zorder=2)
ax.text(1.02, -0.62, r'1$\sigma$', color='#777777', fontsize=9, ha='left')
ax.text(2.02, -0.62, r'2$\sigma$', color='#d6604d', fontsize=9, ha='left')

ax.set_yticks(range(len(labels)))
ax.set_yticklabels(labels, fontsize=10)
ax.set_xlabel(r'Tension vs observation [$\sigma$]', fontsize=11)
ax.set_xlim(0, 2.6)
ax.set_title('SSEE — canonical predictions vs data (algebraic background + forward extensions)',
             fontsize=10.5)
ax.set_ylim(-0.9, len(sig)-0.4)
ax.grid(axis='x', lw=0.4, alpha=0.4, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout()

out = os.path.join(OUT, 'fig_readme_tensions.png')
fig.savefig(out, dpi=170, bbox_inches='tight')
print(f"Saved: {out}")
