#!/usr/bin/env python3
"""act_dr6_lensing.py — ACT DR6 lensing contra el fondo clavado.

QUE PREGUNTA. Con el fondo fijado por algebra y log(10^10 A_s) clavado al que
mide el CMB, el modelo PREDICE el espectro de convergencia C_L^kk sin ninguna
perilla. ACT DR6 lo ha medido. Cuanto vale el chi2 de esa prediccion?

CERO LIBRES. Esta sonda no tiene nuisance: ni calibracion, ni sesgos, ni
desplazamientos de n(z). Con el fondo y A_s clavados no queda NADA que ajustar,
asi que esto es una EVALUACION, no un muestreo. Por eso tampoco entra en el
muestreador de la conjunta: un chi2 constante no puede mover ningun posterior
(la misma razon por la que BAO se quedo fuera).

VERSION Y ESCALA. Se usa la verosimilitud OFICIAL `act_dr6_lenslike` v1.2.1
contra los datos v1.2 --- no una reimplementacion. Variante `act_baseline`
(10 bandpowers, L=40-763), con `lens_only=False` y `like_corrections=True`:
NO es "solo lente", porque el CMB primario esta en la misma prueba, y las
correcciones de normalizacion y N1 dependen de los espectros primarios. Esa
misma eleccion tiene que repetirse si la sonda entra en una conjunta, o se
estarian sumando dos escalas distintas --- el error que ya costo el +12.45 de
BOSS.

CONTROL (R53), dos, y los dos del otro lado:
  (a) el fondo de LCDM-Planck en vez del algebraico. Si el chi2 saliera bueno
      con CUALQUIER fondo, la sonda no discrimina y no dice nada.
  (b) el mismo fondo algebraico con A_s desplazado +-1 sigma del clavo. Si el
      chi2 no se moviera, ACT no veria A_s y no podria confirmar ni negar nada
      --- que es justo lo que le pasa a BOSS.

Salida: results/logs/act_dr6_en_el_clavo.json
"""
import json
import os
import sys

import numpy as np
from scipy import stats

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from ssee_core import SUM_MNU_EV  # noqa: E402

# ORIGEN: results/logs/cmb_dbic_tau_ajustado.json -> SSEE/mejor (plik_lite TTTEEE+lowT+lowE, N=669,
# chi2=1003.586). Se LEE del log: un literal no se entera si la corrida del CMB cambia.
with open(os.path.join(_R, "results", "logs", "cmb_dbic_tau_ajustado.json")) as _fh:
    _CMB = json.load(_fh)["SSEE"]["mejor"]
LOGA_CLAVO = _CMB["logA"]
TAU_CLAVO = _CMB["tau"]
# ORIGEN: results/logs/multisonda_fondo_clavado.json -> eje_amplitud[CMB].sigma (sigma marginal de
# logA en la cadena CMB, calculada por src/p06_growth/multisonda_fondo_clavado.py). Se LEE del log.
with open(os.path.join(_R, "results", "logs", "multisonda_fondo_clavado.json")) as _fh:
    SIG_LOGA = next(e["sigma"] for e in json.load(_fh)["eje_amplitud"] if e["sonda"].startswith("CMB"))
OUT = os.path.join(_R, "results", "logs", "act_dr6_en_el_clavo.json")
_M = {}


def modelo(bg, w, wa):
    cl = tuple(sorted(bg.items())) + (w, wa)
    if cl not in _M:
        from cobaya.model import get_model
        _M[cl] = get_model({
            'packages_path': os.environ.get('COBAYA_PACKAGES_PATH',
                                            os.path.expanduser('~/cobaya_packages')),
            'likelihood': {'act_dr6_lenslike.ACTDR6LensLike': {
                'lens_only': False, 'variant': 'act_baseline',
                'lmax': 4000, 'stop_at_error': True}},
            'theory': {'camb': {'extra_args': {
                'dark_energy_model': 'ppf', 'halofit_version': 'mead',
                'WantTensors': False, 'lens_potential_accuracy': 4}}},
            'params': dict(
                {k: float(v) for k, v in bg.items()},
                logA={'prior': {'min': 1.0, 'max': 5.0}, 'drop': True},
                As={'value': lambda logA: 1e-10 * np.exp(logA), 'derived': False},
                tau={'prior': {'min': 0.010, 'max': 0.200}},
                mnu=SUM_MNU_EV, omk=0.0, w=w, wa=wa),
            'debug': False})
    return _M[cl]


def chi2(bg, w, wa, logA, tau=TAU_CLAVO):
    ll, _ = modelo(bg, w, wa).loglikes({'logA': float(logA), 'tau': float(tau)})
    return -2.0 * float(np.sum(ll))


def main():
    from ssee_core import H0_GLOBAL, N_S, OMEGA_B_H2, OMEGA_C_H2, W0, WA
    ssee = dict(ombh2=OMEGA_B_H2, omch2=OMEGA_C_H2, H0=H0_GLOBAL, ns=N_S)
    # CONTROL (a): fondo LCDM-Planck 2018 TT,TE,EE+lowE+lensing
    # ORIGEN: Planck 2018 VI (arXiv:1807.06209), Tabla 2, TT,TE,EE+lowE+lensing
    lcdm = dict(ombh2=0.02237, omch2=0.1200, H0=67.36, ns=0.9649)

    c = chi2(ssee, W0, WA, LOGA_CLAVO)
    n = 10                       # bandpowers de la variante act_baseline
    print(f"\n  ACT DR6 lensing (act_baseline, {n} bandpowers, CERO libres)")
    print(f"    fondo SSEE + logA clavado : chi2 = {c:8.3f}   chi2/n = {c/n:.3f}")

    ca = chi2(lcdm, -1.0, 0.0, LOGA_CLAVO)
    print(f"\n  CONTROL (a) fondo LCDM-Planck : chi2 = {ca:8.3f}   "
          f"diferencia {c - ca:+.3f}")

    # CONTROL (b): +-1 sigma del clavo (SIG_LOGA, leida del log)
    s = SIG_LOGA
    cm, cp = chi2(ssee, W0, WA, LOGA_CLAVO - s), chi2(ssee, W0, WA, LOGA_CLAVO + s)
    print(f"  CONTROL (b) logA -1sigma      : chi2 = {cm:8.3f}   "
          f"diferencia {cm - c:+.3f}")
    print(f"              logA +1sigma      : chi2 = {cp:8.3f}   "
          f"diferencia {cp - c:+.3f}")
    ve = max(abs(cm - c), abs(cp - c))
    print(f"\n  -> ACT {'SI' if ve > 1.0 else 'NO'} ve A_s "
          f"(mayor salto a 1 sigma: {ve:.3f})")

    pte = float(stats.chi2.sf(c, n))          # 0 libres: dof = bandpowers
    res = dict(
        fecha="2026-09-26", sonda="ACT DR6 lensing", variante="act_baseline",
        paquete="act_dr6_lenslike 1.2.1 (oficial)", datos="v1.2",
        lens_only=False, like_corrections=True,
        bandpowers=n, libres=0,
        logA_clavo=LOGA_CLAVO, tau=TAU_CLAVO,
        chi2_en_el_clavo=c, chi2_por_bandpower=c / n,
        dof=n, PTE=pte, sigma_equivalente=float(stats.norm.isf(pte / 2)),
        control_a_fondo_lcdm=dict(
            chi2=ca, diferencia=c - ca, PTE=float(stats.chi2.sf(ca, n)),
            nota="se evalua LCDM con el MISMO logA clavado del CMB de SSEE, no con el suyo: "
                 "la pregunta del control es si ACT da chi2 bueno con cualquier fondo."),
        control_b_sensibilidad_As=dict(
            sigma_logA=s, chi2_menos=cm, chi2_mas=cp,
            mayor_salto=ve, ve_As=bool(ve > 1.0)))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"\n  -> {OUT}")


if __name__ == "__main__":
    main()
