#!/usr/bin/env python3
"""perfil_wc_boss_chen21.py — ¿qué ω_c pide BOSS DR12 con todo lo demás clavado? (2026-10-20)

POR QUÉ EXISTE. OPEN_PROBLEMS §OP-19 citaba como refuerzo de la identidad
ω_c = KAL₀·ω_b·n_s el perfil de ω_c en BOSS (0.51σ SSEE, 1.40σ ΛCDM-Planck). Ese
perfil corría sobre los espectros de Beutler+2017 y se retiró con ellos
(archive/codigo/investigacion/boss_beutler17_RETIRADO_2026-10-20/). Este script
lo mide de nuevo en el montaje vigente de Chen, Vlah y White 2022 (el mismo de
analiza_boss_chen21.py: espectros de Beutler & McDonald 2021, ventana W·M, P_cb,
covarianza conjunta NGC+SGC de Chen, tablas LPT EXACTAS en cada punto).

QUÉ SE MIDE. Para cada modelo, su fondo clavado (SSEE: álgebra y ln(10¹⁰A_s) del
CMB del modelo; ΛCDM: Planck 2018 y 3.044) con UNA sola cosa suelta, ω_c. h, ω_b,
n_s, Σm_ν, w₀, wₐ y A_s quedan fijos; Ω_m = (ω_b + ω_c + ω_ν)/h² se recalcula, y
con él el crecimiento y Alcock-Paczynski. En cada nodo de ω_c, el χ² CRUDO de los
144 puntos (más la penalización de los lineales) minimizado sobre los 12 sesgos
con tres minimizadores (la medida acordada: χ² crudo, nunca el marginal).
De la parábola alrededor del mínimo: ω_c que pide BOSS y su σ (Δχ² = 1).
Se compara con la referencia de cada modelo: KAL₀·ω_b·n_s (ssee_core) y el ω_c
de Planck 2018 que trae su fondo.

CONTROL (R53, va PRIMERO). El mismo perfil sobre el mejor punto del control ΛCDM
libre (Ω_m, H₀, ln A de boss_chen21.json, que reproduce a Chen+22): ahí el ω_c
del perfil tiene que caer donde ese mejor punto pone ω_c (Ω_m h² − ω_b − ω_ν), a
menos de 0.3σ del propio perfil. Si no cae, el perfil mide la parametrización y
no el dato, y no se escribe nada de los modelos.

Salida: results/logs/growth_2026-07/perfil_wc_boss_chen21.json (con acta).
"""
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_ARGV = list(sys.argv)
sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.join(_R, 'src'))
sys.path.insert(0, os.path.join(_R, 'src', 'p06_growth'))
if __name__ == '__main__' and _ARGV[1:2] != ['uno']:   # el acta va en la PRIMERA linea del log
    from procedencia import cabecera as _cab
    print(_cab(__file__), flush=True)
import cobaya_boss_chen21 as C          # noqa: E402
import cobaya_boss_chen21_fijo as F     # noqa: E402
import analiza_boss_chen21 as A         # noqa: E402
import ssee_core as S                   # noqa: E402
from procedencia import cabecera, con_acta   # noqa: E402
sys.argv = _ARGV

LOG = os.path.join(_R, 'results', 'logs', 'growth_2026-07', 'boss_chen21.json')
SALIDA = os.path.join(_R, 'results', 'logs', 'growth_2026-07', 'perfil_wc_boss_chen21.json')
REJILLA = np.round(np.arange(0.095, 0.1451, 0.005), 4)   # 11 nodos; se amplía sola si el mínimo cae al borde  # ORIGEN-VALOR: 0.1451 — tope de arange para incluir 0.145 (último nodo), no un dato
TOL_CTL = 0.3                                            # criterio del control, fijado antes de correr
NWORK = int(os.environ.get('PERFIL_NWORK', '3'))


def omega_c(c):
    return c['Om'] * c['h'] ** 2 - c['ombh2'] - c['mnu'] / 93.14   # ORIGEN-VALOR: 93.14 — clausura ν del núcleo (ω_ν = Σm_ν/93.14)


def con_wc(c, wc):
    d = dict(c)
    d['Om'] = (c['ombh2'] + wc + c['mnu'] / 93.14) / c['h'] ** 2
    return d


def chi2_nodo(arg):
    """χ² crudo mínimo sobre los sesgos con el fondo `c` (sesgos de arranque x0)."""
    c, x0, nuis = arg
    F.FONDOS['_nodo'] = c
    T = F.tablas('_nodo')
    s8 = T[C.MUESTRAS[0][1]]['sigma8_0']

    def pz(d):
        out = {}
        for st in C.SETS:
            t = st['tag']
            out.setdefault(st['zb'], []).append((st, T[st['z']]['Y'], d[f'bsig8_{t}'] / s8 - 1.0, d[f'b2_{t}'], d[f'bs_{t}']))
        return out
    chi2, mejor, rastro = A.min_crudo(x0, nuis, lambda d: A.chi2_crudo(pz(d)))
    return dict(Om=c['Om'], omega_c=omega_c(c), chi2=chi2, sigma8_0=s8, mejor=mejor,
                minimizadores=[r['chi2'] for r in rastro])


def perfil(c0, x0, nuis, etiqueta):
    rej = list(REJILLA)
    nodos = {}
    t0 = time.time()
    while True:
        falta = [w for w in rej if w not in nodos]
        with Pool(NWORK) as p:
            for w, r in zip(falta, p.map(chi2_nodo, [(con_wc(c0, w), x0, nuis) for w in falta])):
                nodos[w] = r
        ws = sorted(nodos)
        i = int(np.argmin([nodos[w]['chi2'] for w in ws]))
        if 0 < i < len(ws) - 1:
            break
        paso = ws[1] - ws[0]
        rej = rej + ([round(ws[0] - paso, 4)] if i == 0 else [round(ws[-1] + paso, 4)])
        print(f'  {etiqueta}: mínimo en el borde, se amplía la rejilla', flush=True)
    ws = np.array(sorted(nodos))
    ch = np.array([nodos[w]['chi2'] for w in ws])
    j = int(np.argmin(ch))
    sel = slice(max(j - 2, 0), min(j + 3, len(ws)))     # 5 nodos alrededor del mínimo
    a, b, cc = np.polyfit(ws[sel], ch[sel], 2)
    wbest = -b / (2 * a)
    sig = 1.0 / np.sqrt(a)
    chi2min = cc - b * b / (4 * a)
    for w in ws:
        print(f'  {etiqueta}: ω_c={w:.4f}  χ²={nodos[w]["chi2"]:.3f}', flush=True)
    print(f'  {etiqueta}: ω_c = {wbest:.5f} ± {sig:.5f}  (χ²min parábola {chi2min:.3f}, nodo {ch[j]:.3f})'
          f'  [{(time.time() - t0) / 60:.1f} min]', flush=True)
    return dict(omega_c=float(wbest), sigma=float(sig), chi2_min_parabola=float(chi2min),
                chi2_min_nodo=float(ch[j]), parabola=[float(a), float(b), float(cc)],
                nodos=[dict(omega_c_nodo=float(w), **nodos[w]) for w in ws])


def main():
    L = json.load(open(LOG))
    nuis = [k for k in L['SSEE']['mejor_crudo']]
    out = dict(rejilla=list(map(float, REJILLA)), criterio_control_sigma=TOL_CTL,
               medida='chi2 crudo de 144 puntos + penalizacion de los lineales, minimizado sobre 12 sesgos')

    # CONTROL PRIMERO: el mejor punto del ΛCDM libre que reproduce a Chen+22
    ctl = L['control_lcdm_libre']['mejor_crudo']
    h = ctl['H0'] / 100.0
    c_ctl = dict(Om=ctl['Om'], h=h, ombh2=C.OMBH2, ns=C.NS, w0=-1.0, wa=0.0, mnu=C.MNU, logA=ctl['logA'])
    blanco = omega_c(c_ctl)
    pc = perfil(c_ctl, [ctl[n] for n in nuis], nuis, 'control ΛCDM libre')
    d = (pc['omega_c'] - blanco) / pc['sigma']
    pc.update(fondo=c_ctl, blanco_omega_c=blanco, distancia_sigma=float(d), pasa=bool(abs(d) < TOL_CTL))
    out['control'] = pc
    print(f'CONTROL: ω_c del perfil {pc["omega_c"]:.5f}, del mejor punto {blanco:.5f} -> {d:+.2f}σ '
          f'{"PASA" if pc["pasa"] else "FALLA"}', flush=True)
    if not pc['pasa']:
        json.dump(con_acta(out, __file__, entradas=[LOG]), open(SALIDA, 'w'), indent=1)
        sys.exit('CONTROL NO PASA: no se miden los modelos')

    refs = {'SSEE': (S.OMEGA_C_H2, 'KAL0*omega_b*n_s (ssee_core.OMEGA_C_H2)'),
            'LCDM_PLANCK': (omega_c(F.FONDOS['LCDM_PLANCK']), 'Planck 2018 (el fondo de la fila Planck)')}
    for m in ('SSEE', 'LCDM_PLANCK'):
        c0 = F.FONDOS[m]
        p = perfil(c0, [L[m]['mejor_crudo'][n] for n in nuis], nuis, m)
        ref, que = refs[m]
        p.update(fondo=c0, referencia=float(ref), referencia_es=que,
                 distancia_sigma=float((p['omega_c'] - ref) / p['sigma']),
                 chi2_en_referencia=float(np.polyval(p['parabola'], ref)))
        out[m] = p
        print(f'{m}: BOSS pide ω_c = {p["omega_c"]:.5f} ± {p["sigma"]:.5f}; referencia {ref:.5f} -> '
              f'{p["distancia_sigma"]:+.2f}σ', flush=True)
    out['resumen'] = dict(
        ctl_dist=pc['distancia_sigma'],
        ssee_wc=out['SSEE']['omega_c'], ssee_sig=out['SSEE']['sigma'], ssee_ref=out['SSEE']['referencia'],
        ssee_dist=out['SSEE']['distancia_sigma'],
        planck_wc=out['LCDM_PLANCK']['omega_c'], planck_sig=out['LCDM_PLANCK']['sigma'],
        planck_ref=out['LCDM_PLANCK']['referencia'], planck_dist=out['LCDM_PLANCK']['distancia_sigma'])
    json.dump(con_acta(out, __file__, entradas=[LOG]), open(SALIDA, 'w'), indent=1)
    print(f'escrito -> {SALIDA}', flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'uno':      # medir lo que cuesta un nodo
        L = json.load(open(LOG))
        nuis = list(L['SSEE']['mejor_crudo'])
        t0 = time.time()
        r = chi2_nodo((F.FONDOS['SSEE'], [L['SSEE']['mejor_crudo'][n] for n in nuis], nuis))
        print(f'nodo SSEE en su ω_c: χ² {r["chi2"]:.3f} (la fila fija da {L["SSEE"]["chi2_crudo_min"]:.3f}); '
              f'{time.time() - t0:.0f} s', flush=True)
    else:
        main()
