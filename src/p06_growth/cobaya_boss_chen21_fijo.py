#!/usr/bin/env python3
"""cobaya_boss_chen21_fijo.py — BOSS con TODO clavado, en el montaje que reproduce a Chen+22 (2026-10-20).

QUE ES. El control (cobaya_boss_chen21.py) reprodujo a Chen, Vlah & White 2022 con
LCDM libre (logA, Omega_m, H_0, sigma_8 a menos de 0.3 sigma con su covarianza).
Este script usa EXACTAMENTE ese montaje —datos B21 renorm, ventana W M, l = 0, 2,
0.02 < k < 0.20, P_cb, velocileptors, priors de Chen para los nuisance, su
covarianza conjunta NGC+SGC— pero con la cosmologia ENTERA fija. Lo unico que se
muestrea son los nuisance de BOSS: (1+b1) sigma_8, b2, bs por muestra (12), y los
cuatro lineales por muestra (16) se integran en forma cerrada como en el control.

LOS DOS FONDOS (ninguno ajusta nada cosmologico):
  SSEE        Omega_m, h, omega_b, n_s, w0, wa, Sum m_nu del nucleo algebraico
              (ssee_core, mismos ingredientes que boss_lpt_R1R2.COSMO['SSEE']) y
              ln(1e10 A_s) = logA_cmb_ssee de CANONICAL_VALUES.yaml (el A_s que pide
              el CMB del propio modelo, clavado como en KiDS-Legacy).
  LCDM_PLANCK Planck 2018 TT,TE,EE+lowE+lensing (arXiv:1807.06209, Tabla 2):
              boss_lpt_R1R2.COSMO['LCDM'] y ln(1e10 A_s) = 3.044. Es la
              «comparacion de fondos», NO el control.

f(z). Chen usa la f de LCDM por hipergeometrica, que no sirve para w0 wa. Aqui f
se mide del propio fondo: f = -(1+z) dln D_cb/dz con D_cb de P_cb(k=0.02 h/Mpc) de
CAMB a z +- 0.01 (diferencia centrada). Mismo metodo para los dos fondos; para
LCDM se coteja contra la formula de Chen en el modo `prueba` (criterio < 0.5 %).

La comparacion que importa —SSEE contra lo PUBLICADO (LCDM libre de Chen+22)— la
hace analiza_boss_chen21.py con las tres cadenas.

Uso:
  .venv/bin/python3 src/p06_growth/cobaya_boss_chen21_fijo.py prueba
  mpirun -n 4 .venv/bin/python3 src/p06_growth/cobaya_boss_chen21_fijo.py {SSEE|LCDM_PLANCK} <dir>
"""
import json
import os
import sys
import time

import camb
import numpy as np
import yaml

_ARGV = list(sys.argv)
sys.argv = [sys.argv[0]]
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src/p06_growth')
import cobaya_boss_chen21 as C      # noqa: E402  (datos, ventana, covarianza, chi2 del control)
sys.argv = _ARGV
R = C.R
from velocileptors.LPT.lpt_rsd_fftw import LPT_RSD   # noqa: E402

_REPO = '/home/mike/Proyectos/SSEE'


def _canon(clave):
    cv = yaml.safe_load(open(f'{_REPO}/CANONICAL_VALUES.yaml'))
    for b in cv.values():
        if isinstance(b, dict) and clave in b:
            return float(b[clave])
    raise KeyError(clave)


FONDOS = {
    'SSEE': dict(R.COSMO['SSEE'], logA=_canon('logA_cmb_ssee')),
    'LCDM_PLANCK': dict(R.COSMO['LCDM'], logA=3.044),   # ORIGEN-VALOR: Planck 2018 (1807.06209) Tabla 2, TT,TE,EE+lowE+lensing
}
K0, DZ = 0.02, 0.01


def _camb(c, zs):
    p = camb.CAMBparams()
    p.set_cosmology(H0=100 * c['h'], ombh2=c['ombh2'], omch2=c['Om'] * c['h'] ** 2 - c['ombh2'] - c['mnu'] / 93.14,
                    mnu=c['mnu'], omk=0.0)
    p.set_dark_energy(w=c['w0'], wa=c['wa'], dark_energy_model='ppf')
    p.InitPower.set_params(As=np.exp(c['logA']) * 1e-10, ns=c['ns'])
    p.set_matter_power(redshifts=sorted(set(zs) | {0.0}, reverse=True), kmax=3.0)
    return camb.get_results(p)


def fondo(nombre, z):
    """P_cb(k, z) al A_s clavado, f(z) medida del fondo, sigma8(0) y f sigma8(z) totales, alphas AP."""
    c = FONDOS[nombre]
    r = _camb(c, [z - DZ, z, z + DZ])
    k, zz, pk = r.get_matter_power_spectrum(minkh=1e-4, maxkh=2.0, npoints=800, var1='delta_nonu', var2='delta_nonu')
    zz = np.asarray(zz)
    i = {zv: int(np.argmin(np.abs(zz - zv))) for zv in (z - DZ, z, z + DZ)}
    D = {zv: np.sqrt(np.interp(K0, k, pk[j])) for zv, j in i.items()}
    f = float(-(1 + z) * (np.log(D[z + DZ]) - np.log(D[z - DZ])) / (2 * DZ))
    zt = np.asarray(r.transfer_redshifts)
    s8 = np.asarray(r.get_sigma8())
    fs8 = np.asarray(r.get_fsigma8())
    a_par, a_per = R.M.alphas(z, c['Om'], c['w0'], c['wa'])
    return dict(k=k, pcb=pk[i[z]], f=f, sigma8_0=float(s8[int(np.argmin(np.abs(zt)))]),
                fsigma8=float(fs8[int(np.argmin(np.abs(zt - z)))]), a_par=float(a_par), a_per=float(a_per))


def tablas(nombre):
    """Tablas LPT EXACTAS (sin malla) en el punto fijo, por muestra."""
    out = {}
    for zb, z in C.MUESTRAS:
        b = fondo(nombre, z)
        L = LPT_RSD(b['k'], b['pcb'], kIR=0.2, cutoff=10, extrap_min=-4, extrap_max=3, N=2000, threads=1, jn=5)
        L.make_pltable(b['f'], kv=C.KMOD, apar=b['a_par'], aperp=b['a_per'], ngauss=3)
        out[z] = dict(Y=np.stack([L.p0ktable, L.p2ktable, L.p4ktable]), **{x: b[x] for x in ('f', 'sigma8_0', 'fsigma8', 'a_par', 'a_per')})
    return out


DERIV = tuple(f'b1_{zb}{cap}' for zb, _ in C.MUESTRAS for cap in ('NGC', 'SGC'))


def hace_loglike(T):
    s8 = T[C.MUESTRAS[0][1]]['sigma8_0']

    def loglike(**b):
        pares, der = {}, {}
        for st in C.SETS:
            t = st['tag']
            b1 = b[f'bsig8_{t}'] / s8 - 1.0
            der[f'b1_{t}'] = b1
            pares.setdefault(st['zb'], []).append((st, T[st['z']]['Y'], b1, b[f'b2_{t}'], b[f'bs_{t}']))
        return -0.5 * sum(C.chi2_muestra(zb, pp) for zb, pp in pares.items()), der
    return loglike


def _params():
    p = {k: v for k, v in C._params().items() if k.startswith(('bsig8_', 'b2_', 'bs_'))}
    for d in DERIV:
        p[d] = dict(latex=d)
    return p


def prueba():
    """f medida contra la formula de Chen en LCDM-Planck (criterio < 0.5 %)."""
    c = FONDOS['LCDM_PLANCK']
    peor = 0.0
    for _, z in C.MUESTRAS:
        f = fondo('LCDM_PLANCK', z)['f']
        fnu = (c['mnu'] / 93.14) / (c['Om'] * c['h'] ** 2)
        fc = float(C.f_of_a(1 / (1 + z), c['Om']) * (1 - 0.6 * fnu))
        peor = max(peor, abs(f / fc - 1))
        print(f'  z={z}: f medida {f:.5f}  formula Chen {fc:.5f}  ({100 * (f / fc - 1):+.3f} %)', flush=True)
    for n in FONDOS:
        print(f'  {n}: ' + ', '.join(f'{k}={v:.6g}' for k, v in FONDOS[n].items()), flush=True)
    return peor


if __name__ == '__main__':
    modo = _ARGV[1] if len(_ARGV) > 1 else 'prueba'
    if modo == 'prueba':
        sys.exit(0 if prueba() < 0.005 else 1)
    assert modo in FONDOS, modo
    assert C.COV == 'chen', 'el montaje fijo usa la covarianza de Chen, como el control'
    from cobaya.run import run
    chains = _ARGV[2] if len(_ARGV) > 2 else '/mnt/datos/SSEE_data/chains_p6/boss_chen21'
    T = tablas(modo)
    meta = dict(fondo=FONDOS[modo], por_z={str(z): {k: v for k, v in T[z].items() if k != 'Y'} for z in T})
    os.makedirs(chains, exist_ok=True)
    json.dump(meta, open(f'{chains}/fijo_{modo}.fondo.json', 'w'), indent=1)
    print(json.dumps(meta, indent=1), flush=True)
    p = _params()
    info = dict(likelihood={'boss_chen21_fijo': {'external': hace_loglike(T),
                                                 'input_params': [k for k in p if 'prior' in p[k]],
                                                 'output_params': list(DERIV)}},
                params=p, sampler={'mcmc': {'Rminus1_stop': 0.01, 'max_tries': 20000}},
                output=f'{chains}/fijo_{modo}', force=True, resume=False)
    t0 = time.time()
    run(info)
    print(f'\nTERMINADO en {(time.time() - t0) / 3600:.2f} h', flush=True)
