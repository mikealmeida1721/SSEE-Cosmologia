#!/usr/bin/env python3
"""control_lcdm_legacy.py — el CONTROL ΛCDM LIBRE de KiDS-Legacy, leído de sus cadenas (2026-10-21).

POR QUÉ EXISTE. El titular de Paper 6 (S₈ = 0.8273 predicho con A_s del CMB
contra 0.8265 ± 0.0176) se apoyaba en un pipeline propio de ξ± que nunca había
corrido el modelo que KiDS publicó: ΛCDM con el fondo LIBRE. La regla «el
control se mide primero» (H1 de Nova, 2026-10-17) pide justo eso: si este
pipeline, con ΛCDM libre, no devuelve el S₈ de KiDS, ningún número de SSEE que
salga de él vale. La corrida (cola_1017b, Cobaya, 4 cadenas MPI, 13 libres)
terminó el 2026-10-21 tras 101.4 h.

QUÉ SE COMPARA (criterio fijado ANTES de mirar el resultado): la media de S₈
de nuestra cadena frente a la de la cadena OFICIAL de Wright+2025
(output_nautilus_xipm_Fiducial.txt, pesos exp(log_weight), columna
s_8_input), con la σ oficial. PASA si |Δ| < 0.3 σ — el mismo criterio del
control de BOSS. Se reportan también σ₈, Ω_m, χ²_min contra el χ² del máximo
de verosimilitud oficial (407.647, el de control_legacy.py) y la R−1 final
leída del progreso de Cobaya.

CÓMO: las cadenas no guardan σ₈ (no es un parámetro derivado de la
verosimilitud), así que se calcula con CAMB LINEAL sobre una submuestra de la
posterior: 30 % de burn-in por cadena (la convención de R3/R4 y de
kids_legacy_bic.py), filas sorteadas con probabilidad ∝ peso (semilla fija),
y en cada fila la MISMA cosmología que lee la verosimilitud (_bg de
cobaya_kids_legacy: mnu = 0.06, w = −1, un autoestado masivo). σ₈ lineal no
depende de logT_AGN. Ω_m = (ω_c + ω_b + ω_ν,CAMB)/h², S₈ = σ₈ √(Ω_m/0.3).
CONTROL del muestreo (R53): media de logA de la submuestra contra la de la
cadena completa, a < 0.1 σ; si no, la submuestra no representa la posterior.

Salida: results/logs/growth_2026-07/control_lcdm_legacy.json (con acta).
"""
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(_R, 'src'))
if __name__ == '__main__':                     # el acta va en la PRIMERA línea del log
    from procedencia import cabecera as _cab
    print(_cab(__file__), flush=True)
import camb                                    # noqa: E402
from procedencia import con_acta               # noqa: E402

CAD = '/mnt/datos/SSEE_data/chains_p6/kids_legacy'
OFICIAL = ('/mnt/datos/SSEE_data/kids_legacy/KiDS_Legacy_cosmic_shear_data_release/'
           'chains_and_config_files/xipm/output_nautilus_xipm_Fiducial.txt')
SALIDA = os.path.join(_R, 'results', 'logs', 'growth_2026-07', 'control_lcdm_legacy.json')
BURN = 0.30
N_SUB = 1200        # ORIGEN-VALOR: 1200 — tamaño de la submuestra para σ₈ (error MC ~ σ/35; CAMB ~5 s por fila), no un dato
SEMILLA = 20261021  # ORIGEN-VALOR: 20261021 — semilla fija del sorteo (la fecha), no un dato
TOL = 0.3           # criterio del control, fijado antes de correr (el mismo de BOSS)
MNU = 0.06          # ORIGEN-VALOR: 0.06 — la mnu que usa _bg() de cobaya_kids_legacy para ΛCDM libre


def sigma8(fila):
    ombh2, omch2, h0, ns, logA = fila
    p = camb.CAMBparams()
    p.set_cosmology(H0=h0 * 100.0, ombh2=ombh2, omch2=omch2, mnu=MNU, omk=0.0)
    p.set_dark_energy(w=-1.0, wa=0.0, dark_energy_model='ppf')
    p.InitPower.set_params(As=math.exp(logA) * 1e-10, ns=ns)
    p.set_matter_power(redshifts=[0.0], kmax=2.0, nonlinear=False)
    r = camb.get_results(p)
    om = (p.omch2 + p.ombh2 + p.omnuh2) / h0 ** 2
    s8 = float(r.get_sigma8_0())
    return s8, om, s8 * math.sqrt(om / 0.3)


def media_sigma(x, w):
    m = float(np.average(x, weights=w))
    return m, float(math.sqrt(np.average((x - m) ** 2, weights=w)))


def main():
    rutas = [f'{CAD}/lcdm.{i}.txt' for i in range(1, 5)]
    with open(rutas[0]) as f:
        col = f.readline().lstrip('#').split()
    trozos = []
    for r in rutas:
        a = np.loadtxt(r)
        trozos.append(a[int(BURN * len(a)):])
    d = np.concatenate(trozos)
    w = d[:, col.index('weight')]
    c = {n: d[:, col.index(n)] for n in ('ombh2', 'omch2', 'h0', 'ns', 'logA', 'chi2')}

    rng = np.random.default_rng(SEMILLA)
    idx = rng.choice(len(d), size=N_SUB, replace=True, p=w / w.sum())
    filas = [tuple(float(c[n][i]) for n in ('ombh2', 'omch2', 'h0', 'ns', 'logA')) for i in idx]
    with Pool(int(os.environ.get('CTL_NWORK', '4'))) as pool:
        res = np.array(pool.map(sigma8, filas))
    s8s, oms, S8s = res[:, 0], res[:, 1], res[:, 2]
    uno = np.ones(N_SUB)

    la_full = media_sigma(c['logA'], w)
    la_sub = media_sigma(c['logA'][idx], uno)
    ctl_sub = abs(la_sub[0] - la_full[0]) / la_full[1]

    # oficial: Nautilus con pesos exp(log_weight); filas con NaN fuera
    with open(OFICIAL) as f:
        oc = f.readline().lstrip('#').split()
    o = np.loadtxt(OFICIAL)
    uso = [oc.index(n) for n in ('cosmological_parameters--s_8_input', 'COSMOLOGICAL_PARAMETERS--SIGMA_8',
                                 'COSMOLOGICAL_PARAMETERS--OMEGA_M', 'log_weight', 'post', 'prior')]
    o = o[np.isfinite(o[:, uso]).all(axis=1)]
    ow = np.exp(o[:, oc.index('log_weight')] - o[:, oc.index('log_weight')].max())
    of = dict(S8=media_sigma(o[:, uso[0]], ow), sigma8=media_sigma(o[:, uso[1]], ow),
              Om=media_sigma(o[:, uso[2]], ow))
    chi2_of = float(-2.0 * (o[:, oc.index('post')] - o[:, oc.index('prior')]).max())

    nu = dict(S8=media_sigma(S8s, uno), sigma8=media_sigma(s8s, uno), Om=media_sigma(oms, uno))
    dist = {k: (nu[k][0] - of[k][0]) / of[k][1] for k in nu}

    prog = [l.split() for l in open(f'{CAD}/lcdm.progress') if not l.startswith('#') and l.strip()]
    rm1, rm1_cl = float(prog[-1][3]), float(prog[-1][4])

    out = dict(
        corrida='ΛCDM libre (ombh2, omch2, h, n_s, logA + logT_AGN, A_IA, 6 dz) sobre ξ± KiDS-Legacy crudo',
        cadenas=rutas, burn_in=BURN, filas_post_burnin=int(len(d)), submuestra=N_SUB, semilla=SEMILLA,
        convergencia=dict(Rminus1=rm1, Rminus1_cl=rm1_cl, pasos_aceptados=int(float(prog[-1][0]))),
        control_submuestra=dict(logA_cadena=la_full, logA_submuestra=la_sub, distancia_sigma=ctl_sub,
                                pasa=bool(ctl_sub < 0.1)),
        nuestro={k: dict(media=v[0], sigma=v[1]) for k, v in nu.items()},
        oficial={k: dict(media=v[0], sigma=v[1]) for k, v in of.items()},
        distancia_sigma_oficial=dist,
        chi2_min=float(c['chi2'].min()), chi2_maxlike_oficial=chi2_of,
        delta_chi2_min=float(c['chi2'].min()) - chi2_of,
        logA=dict(media=la_full[0], sigma=la_full[1]),
        criterio_sigma=TOL, pasa=bool(abs(dist['S8']) < TOL))
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(con_acta(out, __file__, entradas=rutas + [OFICIAL, f'{CAD}/lcdm.progress']),
              open(SALIDA, 'w'), indent=1)
    print(f'R-1 {rm1:.4f} (bordes {rm1_cl:.3f}); submuestra logA a {ctl_sub:.3f}σ de la cadena '
          f'-> {"PASA" if ctl_sub < 0.1 else "NO PASA"}')
    for k in ('S8', 'sigma8', 'Om'):
        print(f'{k:7s} nuestro {nu[k][0]:.4f} ± {nu[k][1]:.4f}   oficial {of[k][0]:.4f} ± {of[k][1]:.4f}'
              f'   -> {dist[k]:+.2f}σ')
    print(f'chi2_min {c["chi2"].min():.3f}  vs max-like oficial {chi2_of:.3f}  (Δ {c["chi2"].min() - chi2_of:+.3f})')
    print(f'logA {la_full[0]:.4f} ± {la_full[1]:.4f}')
    print(f'CONTROL S8: {dist["S8"]:+.2f}σ de la cadena oficial (criterio {TOL}σ) -> '
          f'{"PASA" if out["pasa"] else "NO PASA"}')
    print(f'escrito -> {SALIDA}')


if __name__ == '__main__':
    main()
