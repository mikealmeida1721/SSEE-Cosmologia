#!/usr/bin/env python3
"""spt3g_kk.py — SPT-3G D1 lente kappa-kappa contra el fondo clavado.

QUE PREGUNTA. Igual que ACT DR6: con el fondo fijado por algebra y logA clavado
al del CMB, el modelo PREDICE C_L^kk. SPT-3G D1 lo midio (Omori & Wu et al.
2026, GMV, 17 bandpowers). Cuanto paga esa prediccion?

NO ES CERO LIBRES, al reves que ACT --- y me equivoque al meterla en la cola
como "barata". El emulador de sistematicos pide 14 parametros; la COLABORACION
fija 7 de ellos (beta_pol a 90/150/220 y los cuatro de haz beam1-4 a cero) y
deja 7 con prior gaussiano ESTRECHO, medidos de la posterior CMB-SPA:
    Tcal_lens 0.999107 +- 0.002685    Pcal_lens 1.007472 +- 0.004001
    Atsz      0.9782   +- 0.0223      Acib150   0.9732   +- 0.0027
    Acib220   0.9998   +- 0.0024      Arad90    0.963    +- 0.0084
    Arad150   0.9502   +- 0.018
Se usan TAL CUAL los publica la colaboracion en
`cobaya/SPT3G_D1_KK/configs/likelihoods/lens/nocmb/gmv.yaml`. Ninguno inventado.

VARIANTE Y ESCALA. `GMV` (lensing-only, covarianza CMB-marginalizada), que es
la baseline de la colaboracion y la que corresponde a medir la sonda SOLA. Si
esta sonda entrara despues en una conjunta CON el CMB primario, hay que pasar a
`GMV_withcmb`, que usa la covarianza noCMBmarg: son DOS ESCALAS y no se mezclan
--- la misma leccion que el +12.45 de BOSS.

CONTROL (R53), los dos del otro lado:
  (a) fondo LCDM-Planck. Si el chi2 saliera bueno con cualquier fondo, la sonda
      no discrimina.
  (b) logA a +-1 sigma del clavo. Si el chi2 no se moviera, SPT no veria A_s y
      no podria confirmar ni negar nada --- lo que le pasa a BOSS.

Salida: results/logs/spt3g_kk_en_el_clavo.json
"""
import json
import os
import sys

import numpy as np

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
OUT = os.path.join(_R, "results", "logs", "spt3g_kk_en_el_clavo.json")

# Priors y fijos LEIDOS del yaml de la colaboracion, no copiados a mano.
# ORIGEN: /mnt/datos/SSEE_data/cmb_lensing/spt3g/cobaya/SPT3G_D1_KK/configs/likelihoods/lens/nocmb/gmv.yaml
_GMV = "/mnt/datos/SSEE_data/cmb_lensing/spt3g/cobaya/SPT3G_D1_KK/configs/likelihoods/lens/nocmb/gmv.yaml"


def _lee_gmv():
    import yaml

    class _L(yaml.SafeLoader):
        pass
    _L.add_multi_constructor("tag:yaml.org,2002:python/", lambda ld, suf, nodo: None)
    with open(_GMV) as fh:
        cfg = yaml.load(fh, Loader=_L)
    par = next(iter(cfg.values()))["params"]
    libres = {k: (v["prior"]["loc"], v["prior"]["scale"]) for k, v in par.items()
              if isinstance(v, dict) and "prior" in v}
    fijos = {k: float(v["value"]) for k, v in par.items()
             if isinstance(v, dict) and "value" in v}
    return libres, fijos


LIBRES, FIJOS = _lee_gmv()
_M = {}


def modelo(bg, w, wa):
    cl = tuple(sorted(bg.items())) + (w, wa)
    if cl not in _M:
        import spt_candl_data
        from cobaya.model import get_model
        pars = dict({k: float(v) for k, v in bg.items()}, **FIJOS)
        pars.update(
            logA={'prior': {'min': 1.0, 'max': 5.0}, 'drop': True},
            As={'value': lambda logA: 1e-10 * np.exp(logA), 'derived': False},
            tau=TAU_CLAVO, mnu=SUM_MNU_EV, omk=0.0, w=w, wa=wa)
        for k, (c, s) in LIBRES.items():
            pars[k] = {'prior': {'dist': 'norm', 'loc': c, 'scale': s},
                       'ref': c, 'proposal': s / 3.0}
        _M[cl] = get_model({
            'likelihood': {'candl.interface.CandlCobayaLikelihood': {
                'data_set_file': spt_candl_data.SPT3G_D1_KK,
                # add_logdet FALSE a proposito. La colaboracion lo pone a
                # True, pero eso mete el termino de volumen ln det C DENTRO del
                # -2lnL y el resultado ya no es un chi2: con True salia -614.87,
                # negativo, que es imposible. Con la covarianza FIJA ese termino
                # es una CONSTANTE, asi que quitarlo no cambia ningun minimo ni
                # ninguna diferencia --- solo devuelve el cero de la escala, y
                # entonces el chi2 se puede contrastar contra sus dof. Es la
                # misma trampa de dos escalas que costo el +12.45 de BOSS.
                'variant': 'GMV', 'lensing': True, 'add_logdet': False,
                'clear_internal_priors': True}},
            'theory': {'camb': {'extra_args': {
                'dark_energy_model': 'ppf', 'halofit_version': 'mead',
                'WantTensors': False, 'lens_potential_accuracy': 4}}},
            'params': pars, 'debug': False})
    return _M[cl]


def chi2(bg, w, wa, logA):
    """chi2 minimizando los 7 nuisance dentro de sus priors publicados."""
    from scipy.optimize import minimize
    m = modelo(bg, w, wa)
    nom = list(LIBRES)
    x0 = np.array([LIBRES[k][0] for k in nom])
    sg = np.array([LIBRES[k][1] for k in nom])

    def f(u):                      # u en unidades de sigma del prior
        p = dict(zip(nom, x0 + u * sg)); p['logA'] = float(logA)
        try:
            ll, _ = m.loglikes(p)
        except Exception:
            return 1e9
        v = -2.0 * float(np.sum(ll))
        return v if np.isfinite(v) else 1e9

    r = minimize(f, np.zeros(len(nom)), method="Nelder-Mead",
                 options=dict(xatol=1e-3, fatol=1e-3, maxiter=2000, maxfev=2000))
    return float(r.fun), dict(zip(nom, (x0 + r.x * sg).tolist()))


def main():
    from scipy import stats
    from ssee_core import H0_GLOBAL, N_S, OMEGA_B_H2, OMEGA_C_H2, W0, WA
    ssee = dict(ombh2=OMEGA_B_H2, omch2=OMEGA_C_H2, H0=H0_GLOBAL, ns=N_S)
    # ORIGEN: Planck 2018 VI (arXiv:1807.06209), Tabla 2, TT,TE,EE+lowE+lensing
    lcdm = dict(ombh2=0.02237, omch2=0.1200, H0=67.36, ns=0.9649)
    n, k = 17, 7
    dof = n - k

    c, best = chi2(ssee, W0, WA, LOGA_CLAVO)
    pte = float(stats.chi2.sf(c, dof))
    print(f"\n  SPT-3G D1 KK (GMV, {n} bandpowers, {k} nuisance con prior)")
    print(f"    fondo SSEE + logA clavado : chi2 = {c:8.3f}/{dof} dof   "
          f"PTE = {pte:.4f}   {stats.norm.isf(pte/2):.2f} sigma")

    ca, _ = chi2(lcdm, -1.0, 0.0, LOGA_CLAVO)
    print(f"\n  CONTROL (a) fondo LCDM-Planck : chi2 = {ca:8.3f}   "
          f"diferencia {c - ca:+.3f}")

    cm, _ = chi2(ssee, W0, WA, LOGA_CLAVO - SIG_LOGA)
    cp, _ = chi2(ssee, W0, WA, LOGA_CLAVO + SIG_LOGA)
    ve = max(abs(cm - c), abs(cp - c))
    print(f"  CONTROL (b) logA -1sigma      : chi2 = {cm:8.3f}   {cm - c:+.3f}")
    print(f"              logA +1sigma      : chi2 = {cp:8.3f}   {cp - c:+.3f}")
    print(f"\n  -> SPT {'SI' if ve > 1.0 else 'NO'} ve A_s (mayor salto: {ve:.3f})")

    json.dump(dict(
        fecha="2026-09-26", sonda="SPT-3G D1 KK", variante="GMV",
        paquete="candl 2.2.0 + spt_candl_data (oficial)",
        bandpowers=n, nuisance_libres=k, nuisance_fijados_por_colaboracion=7,
        dof=dof, logA_clavo=LOGA_CLAVO,
        chi2_en_el_clavo=c, PTE=pte, sigma_equivalente=float(stats.norm.isf(pte/2)),
        mejor_ajuste_nuisance=best,
        control_a_fondo_lcdm=dict(chi2=ca, diferencia=c - ca),
        control_b_sensibilidad_As=dict(sigma_logA=SIG_LOGA, chi2_menos=cm,
                                       chi2_mas=cp, mayor_salto=ve,
                                       ve_As=bool(ve > 1.0))),
        open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"\n  -> {OUT}")


if __name__ == "__main__":
    main()
