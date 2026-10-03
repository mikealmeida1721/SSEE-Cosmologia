"""
Figura de Paper 9 y su log: la cascada SH0ES -> H_glob y su control del otro
lado (la misma lente sobre el TRGB de CCHP).

Genera
  - results/figures/fig_paper9_h0_tension.pdf (+ .png)
  - results/logs/p9_cascada_control.json  (con acta)

Ningún número tecleado: las constantes salen de ssee_core y las mediciones
publicadas de results/logs/h0_por_metodos.json, que las lee de su .tex.

2026-10-03: el control usaba «Freedman 69.96 ± 1.54» tecleado. Era el valor
de la v1 de arXiv:2408.06153 (agosto 2024, 69.96 ± 1.05 ± 1.12); la v3 (marzo
2025), que es la que está en /mnt/datos, adopta 70.39 ± 1.22 (stat) ± 1.33 (sys)
± 0.70 (σ_SN) y conserva 69.96 sólo como variante (sin SN2007af). Además la segunda figura (f_screen(z)) se RETIRA: escalaba
s_K con un Ω_DE(z) construido con Ω_m = 1 − 0.840 = 0.160, que es 1+w₀ y no
una densidad, y contradecía el Paso 4 del propio paper (f es constante).
"""
import json
import os
import pathlib
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import ssee_core as sc                     # noqa: E402
from procedencia import acta, con_acta    # noqa: E402

METODOS = RAIZ / "results" / "logs" / "h0_por_metodos.json"
LOG = RAIZ / "results" / "logs" / "p9_cascada_control.json"
OUT = RAIZ / "results" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

m = json.load(open(METODOS))
med = m["medidas"]
cchp = med["trgb_cchp"]
assert "70.39" in cchp["texto"], "CCHP: el valor leído no es el adoptado por el artículo"


def cascada(H, sH, f):
    """Lente sobre una tasa medida: sale H_glob, se compara con el número puro."""
    hg = H * (1.0 - f)
    sg = sH * (1.0 - f)
    return dict(H_glob=hg, H_glob_s=sg, residuo=hg - sc.H0_ALG,
                sigma=(hg - sc.H0_ALG) / sg)


res = dict(
    numero_puro=sc.H0_ALG,
    f_screen_IR=sc.F_SCREEN_IR,
    f_screen=sc.F_SCREEN,
    sh0es=dict(H0=sc.H0_SH0ES, H0_s=sc.SIG_H0_SH0ES,
               IR=cascada(sc.H0_SH0ES, sc.SIG_H0_SH0ES, sc.F_SCREEN_IR),
               completo=cascada(sc.H0_SH0ES, sc.SIG_H0_SH0ES, sc.F_SCREEN)),
    cchp=dict(H0=cchp["H0"], H0_s=cchp["err_mas"], fuente=cchp["fuente"],
              texto=cchp["texto"],
              IR=cascada(cchp["H0"], cchp["err_mas"], sc.F_SCREEN_IR),
              completo=cascada(cchp["H0"], cchp["err_mas"], sc.F_SCREEN)),
    planck=dict(H0=m["H0_planck"], H0_s=m["H0_planck_s"]),
)
json.dump(con_acta(res, __file__, [METODOS]), open(LOG, "w"), indent=1, ensure_ascii=False)

# ── Figura: mediciones publicadas y salida de la cascada ─────────────────────
# grupo 0 = temprano (inferido en ΛCDM) | 1 = local medido | 2/3 = salida SSEE
filas = [
    ("Planck 2018\n(CMB, ΛCDM)", m["H0_planck"], m["H0_planck_s"], m["H0_planck_s"], 0),
]
for k, nom in (("trgb_cchp", "TRGB, CCHP 2024\n(HST+JWST)"),
               ("lentes", "Time delays\n(TDCOSMO 2025)"),
               ("maseres", "Masers\n(MCP)"),
               ("cefeidas_hst", "SH0ES 2022\n(Cepheids, input)")):
    x = med[k]
    filas.append((nom, x["H0"], x["err_menos"], x["err_mas"], 1))
sh, cc = res["sh0es"]["completo"], res["cchp"]["completo"]
filas.append((f"SSEE $H_0^{{\\rm glob}}$ from SH0ES\n({sh['sigma']:+.2f}$\\sigma$ vs $3(\\varphi+\\pi)^2$)",
              sh["H_glob"], sh["H_glob_s"], sh["H_glob_s"], 2))
filas.append((f"SSEE $H_0^{{\\rm glob}}$ from CCHP\n({cc['sigma']:+.2f}$\\sigma$ vs $3(\\varphi+\\pi)^2$)",
              cc["H_glob"], cc["H_glob_s"], cc["H_glob_s"], 3))

colores = {0: '#2166ac', 1: '#d6604d', 2: '#1a9641', 3: '#7fbf7b'}
leyenda = {0: 'Early universe (inferred in ΛCDM)', 1: 'Local measurements',
           2: 'SSEE cascade output (from SH0ES)', 3: 'SSEE cascade output (from CCHP)'}

fig, ax = plt.subplots(figsize=(7, 5))
for i, (nom, h0, slo, shi, g) in enumerate(filas):
    c = colores[g]
    ax.errorbar(h0, i, xerr=[[slo], [shi]], fmt='o', color=c,
                markersize=6, capsize=4, linewidth=1.5, elinewidth=1.5)
    ax.text(h0, i + 0.32, f'{h0:.2f}', ha='center', va='bottom', fontsize=7.5, color=c)
ax.set_yticks(range(len(filas)))
ax.set_yticklabels([f[0] for f in filas], fontsize=8.5)
ax.set_xlabel(r'$H_0$ [km s$^{-1}$ Mpc$^{-1}$]', fontsize=11)
ax.set_title('Hubble constant: SSEE cascade output vs measurements', fontsize=11)
ax.axvline(sc.H0_ALG, color='#555555', lw=0.9, ls=':', alpha=0.8)
ax.text(sc.H0_ALG, -0.75, r'$3(\varphi+\pi)^2$', ha='center', fontsize=8, color='#555555')
ax.set_xlim(60, 82)
ax.grid(axis='x', lw=0.4, alpha=0.4)
ax.legend(handles=[mpatches.Patch(color=colores[g], label=leyenda[g]) for g in range(4)],
          loc='lower right', fontsize=8, framealpha=0.9)
ax.invert_yaxis()
fig.tight_layout()
out = OUT / 'fig_paper9_h0_tension.pdf'
_META = {'Keywords': 'ACTA-PROCEDENCIA ' + json.dumps(acta(__file__, entradas=[METODOS]))}   # R75: acta de la figura
fig.savefig(out, bbox_inches='tight', metadata=_META)
fig.savefig(out.with_suffix('.png'), dpi=150, bbox_inches='tight', metadata=_META)
plt.close(fig)

for k in ("sh0es", "cchp"):
    for r in ("IR", "completo"):
        x = res[k][r]
        print(f"{k:6s} {r:9s} H_glob={x['H_glob']:.4f} ± {x['H_glob_s']:.4f}  "
              f"residuo={x['residuo']:+.4f}  ({x['sigma']:+.3f} σ)")
print(f"Guardado: {out} y {LOG}")
