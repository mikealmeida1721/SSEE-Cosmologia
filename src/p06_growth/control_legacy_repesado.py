#!/usr/bin/env python3
"""control_legacy_repesado.py — ¿nuestro evaluador de ξ± reproduce la verosimilitud OFICIAL
de KiDS-Legacy cuando se le da el MÉTODO OFICIAL? (2026-10-22)

POR QUÉ EXISTE. El control ΛCDM libre (control_lcdm_legacy.json, 101 h) NO pasó:
S₈ a −0.50σ de la cadena oficial (criterio 0.3σ) y χ²_min +9.09. Pero esa
corrida usaba un alineamiento intrínseco SIMPLIFICADO (una amplitud, 13 libres)
en vez del NLA-M oficial (A, β y seis masas medias, 20 libres), aunque la
diferencia ya estaba documentada en control_legacy.py desde el 2026-09-19. O
sea: no probaba el pipeline con el método publicado. Antes de gastar otras
~100 h en una cadena con NLA-M, esta prueba mide en ~1.5 h la pregunta que
importa: con el método oficial, ¿nuestro evaluador da la verosimilitud de ellos?

CÓMO (muestreo por importancia sobre la cadena OFICIAL). Se sortean N_SUB filas
de output_nautilus_xipm_Fiducial.txt con probabilidad ∝ su peso. En cada fila
—cosmología, log T_AGN, n(z) y los parámetros NLA-M de ESA fila— se evalúa
nuestro χ² con el MISMO código de control_legacy.py (NLA-M evaluado por bin:
A_eff,i = A·f_r,i·(M_i/M_piv)^β). Δχ²_i = χ²_nuestro − χ²_oficial, con
χ²_oficial = −2·(post − prior) de la fila (convención CosmoSIS verificada en
control_legacy.py). Repesar con exp(−½(Δχ²_i − ⟨Δχ²⟩)) da la posterior que
daría NUESTRA verosimilitud con LOS priors y el muestreo de ellos: así los dos
efectos que no son del evaluador (priors, muestreador) se cancelan.

CRITERIO (fijado ANTES de correr): |S₈ repesado − S₈ de la misma submuestra
sin repesar| < 0.3 σ_oficial. Comparar con la MISMA submuestra cancela el ruido
de Monte Carlo del sorteo. Se reportan también la dispersión de Δχ² (si es
casi constante, las dos verosimilitudes son la misma función salvo una
constante) y el tamaño efectivo de la muestra repesada (si es chico, el
repesado no es fiable y se dice).
S₈ = σ₈ √(Ω_m/0.3) con Ω_m TOTAL (con ν), de las columnas de la cadena oficial.

CONTROL (R53): la fila de máxima verosimilitud oficial se evalúa también y
tiene que reproducir el χ² OFICIAL de esa fila (407.647) a menos de 0.1. Con
el evaluador viejo (centro del bin, l sin converger) daba 410.27; con el
binning por pares y la rejilla convergida, 407.671 (medido el 2026-10-22,
antes de fijar este umbral: es un control de identidad del código, no el
criterio del resultado, que sigue siendo el de S₈).

Salida: results/logs/growth_2026-07/control_legacy_repesado.json (con acta).
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(_R, 'src'))
sys.path.insert(0, os.path.join(_R, 'src', 'p06_growth'))
if __name__ == '__main__':                     # el acta va en la PRIMERA línea del log
    from procedencia import cabecera as _cab
    print(_cab(__file__), flush=True)
import control_legacy as CL                    # noqa: E402  (punto oficial, F_R, M_piv, cadena)
import kids_shear as K                         # noqa: E402
from procedencia import con_acta               # noqa: E402

SALIDA = os.path.join(_R, 'results', 'logs', 'growth_2026-07', 'control_legacy_repesado.json')
REF = os.path.join(_R, 'results', 'logs', 'growth_2026-07', 'control_legacy.json')
N_SUB = 1200        # ORIGEN-VALOR: 1200 — filas sorteadas (~15 s cada una: CAMB + 1 s de teoría), no un dato
SEMILLA = 20261022  # ORIGEN-VALOR: 20261022 — semilla fija del sorteo (la fecha), no un dato
TOL = 0.3           # criterio, fijado antes de correr

_cfg = K.set_dataset('legacy')
_D = K.load_data()
_M = K.scale_mask(_D)
# 2026-10-22, segunda pasada: binning pesado por pares (bin_xi oficial) y
# rejilla en l convergida (N_LGRID = 40000). La primera pasada (sin esto) dio
# S8 repesado −0.42σ: quedó en el historial de git de este log.
K.load_npairs(_D)
with open(CL._CADENA) as _f:
    COL = _f.readline().lstrip('#').split()


def _c(n):
    return COL.index(n)


def chi2_fila(fila):
    v = dict(zip(COL, fila))
    A = v['INTRINSIC_ALIGNMENT_PARAMETERS--A']
    beta = v['INTRINSIC_ALIGNMENT_PARAMETERS--BETA']
    lm = np.array([v[f'INTRINSIC_ALIGNMENT_PARAMETERS--LOG10_M_MEAN_{i}'] for i in range(1, 7)])
    a_eff = A * CL.F_R * 10.0 ** (beta * (lm - CL.LOG10_M_PIV))
    dz = np.array([v[f'NOFZ_SHIFTS--BIAS_{i}'] for i in range(1, 7)])
    try:
        res, p, kh, zpk, pk, gr = K.run_camb(
            As=np.exp(v['COSMOLOGICAL_PARAMETERS--A_S']) / 1e10,
            omch2=v['cosmological_parameters--omch2'], ombh2=v['cosmological_parameters--ombh2'],
            h0=v['cosmological_parameters--h0'], ns=v['cosmological_parameters--n_s'],
            logT_AGN=v['halo_model_parameters--log_t_agn'])
        ells, Cl, idx = K.cl_shear(_D, res, p, kh, zpk, pk, gr, a_eff, dz)
        return float(K.chi2(_D, K.theory_vector(_D, ells, Cl, idx, delta_c=0.0), _M))
    except Exception:
        return float('nan')


def ms(x, w):
    m = float(np.average(x, weights=w))
    return m, float(np.sqrt(np.average((x - m) ** 2, weights=w)))


def main():
    X = np.loadtxt(CL._CADENA)
    s8c, omc = _c('COSMOLOGICAL_PARAMETERS--SIGMA_8'), _c('COSMOLOGICAL_PARAMETERS--OMEGA_M')
    ok = np.isfinite(X[:, _c('log_weight')]) & np.isfinite(X[:, s8c]) & np.isfinite(X[:, omc])
    X = X[ok]
    w = np.exp(X[:, _c('log_weight')] - X[:, _c('log_weight')].max())
    S8 = X[:, s8c] * np.sqrt(X[:, omc] / 0.3)
    chi2_of = -2.0 * (X[:, _c('post')] - X[:, _c('prior')])
    of = ms(S8, w)

    rng = np.random.default_rng(SEMILLA)
    idx = rng.choice(len(X), size=N_SUB, replace=True, p=w / w.sum())
    imax = int(np.argmin(chi2_of))
    filas = [X[i] for i in idx] + [X[imax]]
    with Pool(int(os.environ.get('CTL_NWORK', '3'))) as pool:   # ~1.2 GB por proceso (matriz de Bessel)
        c2 = np.array(pool.map(chi2_fila, filas))
    c2_max, c2 = c2[-1], c2[:-1]
    ref_max = float(chi2_of[imax])
    ctl = bool(abs(c2_max - ref_max) < 0.1)

    bien = np.isfinite(c2)
    d = (c2 - chi2_of[idx])[bien]
    s8s = S8[idx][bien]
    rw = np.exp(-0.5 * (d - d.mean()))
    ess = float(rw.sum() ** 2 / (rw ** 2).sum())
    sub = ms(s8s, np.ones_like(s8s))
    rep = ms(s8s, rw)
    dist = (rep[0] - sub[0]) / of[1]
    out = dict(
        cadena_oficial=CL._CADENA, submuestra=N_SUB, semilla=SEMILLA, filas_fallidas=int((~bien).sum()),
        control_fila_maxlike=dict(chi2=float(c2_max), chi2_oficial=float(ref_max), pasa=ctl),
        delta_chi2=dict(media=float(d.mean()), sigma=float(d.std()), min=float(d.min()), max=float(d.max())),
        tamano_efectivo=ess,
        S8_oficial=dict(media=of[0], sigma=of[1]), S8_submuestra=dict(media=sub[0], sigma=sub[1]),
        S8_repesado=dict(media=rep[0], sigma=rep[1]),
        distancia_sigma=float(dist), criterio_sigma=TOL,
        pasa=bool(ctl and abs(dist) < TOL))
    json.dump(con_acta(out, __file__, entradas=[CL._CADENA, REF]), open(SALIDA, 'w'), indent=1)
    print(f'control fila max-like: chi2 {c2_max:.3f} vs {ref_max:.3f} -> {"PASA" if ctl else "NO PASA"}')
    print(f'Δχ² nuestro−oficial: {d.mean():+.3f} ± {d.std():.3f}  (min {d.min():+.2f}, max {d.max():+.2f}); '
          f'filas fallidas {int((~bien).sum())}')
    print(f'tamaño efectivo del repesado: {ess:.0f} de {int(bien.sum())}')
    print(f'S8 oficial {of[0]:.4f} ± {of[1]:.4f} | submuestra {sub[0]:.4f} | repesado {rep[0]:.4f} ± {rep[1]:.4f}')
    print(f'CONTROL: S8 repesado a {dist:+.2f}σ de la submuestra (criterio {TOL}σ) -> '
          f'{"PASA" if out["pasa"] else "NO PASA"}')
    print(f'escrito -> {SALIDA}')


if __name__ == '__main__':
    main()
