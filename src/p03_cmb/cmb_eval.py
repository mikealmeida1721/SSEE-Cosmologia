"""Evaluador de Planck (plik_lite TTTEEE + lowT + lowE): chi2 y sigma8.

FIX 2026-09-08 — LA ENERGIA OSCURA ERA UN LITERAL. La version del scratchpad
traia `'w': -0.840015, 'wa': -0.670141` clavados dentro del modelo, o sea la
ecuacion de estado de SSEE, para TODAS las corridas. Cualquier fila rotulada
LCDM que pasara por aqui NO era LCDM: no fallaba, devolvia un numero
plausible y equivocado. Ya invalido una fila real, la de LCDM en
`results/logs/cmb_tau_flotado.json`, que quedo marcada "NO USAR".

Ahora la ecuacion de estado es un ARGUMENTO OBLIGATORIO de `modelo()`. No hay
valor por defecto a proposito: el que llama tiene que decir con que fondo
esta corriendo, y asi no se puede heredar el de otro por descuido. Se
mantiene un objeto por (w, wa) para no reconstruir CAMB en cada evaluacion.

Vigilado por R64.
"""
import os, logging
import numpy as np
import sys as _s66
_s66.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ssee_core import SUM_MNU_EV as _MNU


logging.getLogger('cobaya').setLevel(logging.ERROR)
PK = os.environ.get('COBAYA_PACKAGES_PATH',
                    os.path.expanduser('~/cobaya_packages'))
LIB = ['ombh2', 'omch2', 'H0', 'ns', 'logA', 'tau']
_M = {}          # cache por (w, wa)


def modelo(w, wa, dneff=0.0, meffsterile=0.0, mnu=None):
    """w y wa son OBLIGATORIOS: sin defecto no se hereda el fondo ajeno.

    `mnu=None` usa la masa de SSEE (el defecto de siempre, misma clave de cache
    y mismo `info`). LCDM tiene que pasar la SUYA (lcdm_planck.LCDM_PLANCK):
    darle la de SSEE es no dejarlo usar sus propios parametros (2026-09-27).

    `dneff`/`meffsterile` anaden una especie termica masiva extra (canal
    `meffsterile` de CAMB). Con los dos en 0 —el defecto— la CLAVE de cache y
    el `info` son EXACTAMENTE los de antes: el modelo sin particula es el mismo
    objeto de siempre, bit a bit. Vigilado por el control C0 de la cola #25.
    Ver `src/p06_growth/particula_que_prefiere_kids.py` para la traduccion
    (masa, temperatura) -> (dneff, meffsterile).
    """
    cl = (round(float(w), 12), round(float(wa), 12))
    if meffsterile > 0.0:
        cl = cl + (round(float(dneff), 12), round(float(meffsterile), 12))
    if mnu is not None:
        cl = cl + ('mnu', round(float(mnu), 12))
    if cl not in _M:
        from cobaya.model import get_model
        info = {
            'packages_path': PK,
            'likelihood': {'planck_2018_highl_plik.TTTEEE_lite': None,
                           'planck_2018_lowl.TT': None,
                           'planck_2018_lowl.EE': None},
            'theory': {'camb': {'extra_args': {
                'dark_energy_model': 'ppf', 'halofit_version': 'mead',
                'WantTensors': False, 'lens_potential_accuracy': 1}}},
            'params': {
                'ombh2': {'prior': {'min': 0.005, 'max': 0.100}},
                'omch2': {'prior': {'min': 0.001, 'max': 0.990}},
                'H0':    {'prior': {'min': 20.0,  'max': 100.0}},
                'ns':    {'prior': {'min': 0.500, 'max': 1.500}},
                'logA':  {'prior': {'min': 1.0,   'max': 5.0},
                          'drop': True},
                'As': {'value': lambda logA: 1e-10 * np.exp(logA),
                       'derived': False},
                'tau':   {'prior': {'min': 0.010, 'max': 0.200}},
                'mnu': _MNU if mnu is None else float(mnu), 'omk': 0.0,
                'w': cl[0], 'wa': cl[1],
                'A_planck': 1.0,
                'sigma8': None},
            'debug': False}
        if meffsterile > 0.0:
            info['params']['nnu'] = 3.044 + float(dneff)
            info['params']['meffsterile'] = float(meffsterile)
        _M[cl] = get_model(info)
    return _M[cl]


def chi2_particula(p, w, wa, dneff=0.0, meffsterile=0.0):
    """Como `chi2_y_s8`, pero con una especie termica masiva extra dentro.

    Con dneff = meffsterile = 0 devuelve EXACTAMENTE lo mismo que `chi2_y_s8`:
    usa el mismo objeto de modelo. Eso es el control C0 de la cola #25."""
    m = modelo(w, wa, dneff, meffsterile)
    try:
        ll, der = m.loglikes({k: float(p[k]) for k in LIB})
    except Exception:
        return 1e30, np.nan
    c = -2.0 * float(np.sum(ll))
    if not np.isfinite(c):
        return 1e30, np.nan
    s8 = float(der[list(m.parameterization.derived_params()).index('sigma8')])
    return c, s8


def chi2_y_s8(p, w, wa, mnu=None):
    """p = dict con LIB; w y wa obligatorios. Devuelve (chi2, sigma8)."""
    m = modelo(w, wa, mnu=mnu)
    try:
        ll, der = m.loglikes({k: float(p[k]) for k in LIB})
    except Exception:
        return 1e30, np.nan
    c = -2.0 * float(np.sum(ll))
    if not np.isfinite(c):
        return 1e30, np.nan
    s8 = float(der[list(m.parameterization.derived_params()).index('sigma8')])
    return c, s8
