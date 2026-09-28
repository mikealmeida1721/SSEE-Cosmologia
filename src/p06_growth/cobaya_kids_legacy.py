#!/usr/bin/env python3
"""
Likelihood de Cobaya para KiDS-Legacy xi_pm (Wright et al. 2025, A&A 703, A158).

LA PREGUNTA QUE VIENE A CONTESTAR. Con el fondo de SSEE CLAVADO por algebra,
que log(10^10 A_s) pide la cizalla de KiDS-Legacy? Si pide el MISMO que el CMB
--- LOGA_CMB_SSEE = 3.0448340130228546 --- dentro de ~1 sigma, entonces no hace
falta ninguna particula para casar CMB y crecimiento: el fondo unico basta, y
la particula se retira por INNECESARIA (no por refutada; ya estaba retirada
desde 2026-08-01 por otras dos razones).

S_8 = 0.815 de la nota de prensa NO entra por ningun lado como entrada. Solo se
usa al final como contraste del posterior.

CONTROL NEGATIVO (R53) --- `control_legacy.py`, obligatorio antes de creer nada:
reproduce el chi^2 del punto de maxima verosimilitud de la cadena oficial,
407.647 (357 puntos), con TODOS los ingredientes puestos en su valor oficial,
sin ninguna traduccion libre: da 410.27, +0.64%.

MONTAJE, y en que se aparta del pipeline oficial:
  - No lineal: HMCode-2020 con retroalimentacion, log10(T_AGN/K) libre en
    [7.3, 8.3] --- el MISMO modelo y el MISMO prior del pipeline fiducial
    (alli servido por el emulador CosmoPower entrenado sobre CAMB, aqui por
    CAMB directo). No hay traduccion que declarar.
  - IA: el oficial es NLA-M con 8 parametros (A, beta y 6 masas medias) con
    priors gaussianos correlacionados cuya matriz vive fuera de este release
    (CosmoPipe/ia_models/mass_dependent_ia). Aqui se toma la FORMA por bin que
    ese modelo produce en el posterior oficial,
        forma_i = A * f_r,i * (M_i/M_piv)^beta,
    y se deja libre UNA amplitud global `A_scale` que la reescala. A_scale = 1
    es el IA oficial. Es 1 libre en vez de 8: aproximacion DECLARADA.
  - dz: los 6 corrimientos, con el prior gaussiano correlacionado real
    (data/Nz_covariance.txt) y sus medias reconstruidas del values.ini oficial
    via la cholesky inferior de esa covarianza.
  - Sin termino c aditivo: el pipeline de Legacy lo apaga
    (add_c_term = 0, add_2d_cterm = 0), al reves que KiDS-1000.
  - Cortes de escala: xi+ 2'-300', xi- 4'-300' (scale_cuts del .ini fiducial).

TRES CONFIGURACIONES:
  ssee     : fondo FIJO por algebra. Libres: logA, logT_AGN, A_scale, dz1..dz6
             -> 9.
  lcdm     : fondo LIBRE (ombh2, omch2, h0, ns; w=-1, wa=0) -> 13.
  lcdmfijo : fondo CLAVADO en Planck 2018 -> 9. Iguala la RIGIDEZ, que es lo
             que hace falta para preguntar de quien es cualquier tension.
"""
import sys
import time

import numpy as np

sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src/p06_growth')
import kids_shear as K                                          # noqa: E402
import ssee_core as S                                           # noqa: E402

np.seterr(all='ignore')

K.set_dataset('legacy')
D = K.load_data()
MASK = K.scale_mask(D)
CINV = np.linalg.inv(D['C'][np.ix_(MASK, MASK)])

RAIZ = ('/mnt/datos/SSEE_data/kids_legacy/'
        'KiDS_Legacy_cosmic_shear_data_release/')

# --- prior de los 6 corrimientos n(z) -------------------------------------
# La covarianza es la oficial. Las medias se reconstruyen del values.ini:
# el modulo `correlated_dz_priors` muestrea en base decorrelacionada y
# devuelve  bias = L @ uncorr,  con L la cholesky INFERIOR de la covarianza.
# Comprobado: L @ uncorr_medio reproduce las medias posteriores de la cadena
# oficial dentro de ~1 sigma en cada bin (la diferencia es el tiron del dato).
# ORIGEN: /mnt/datos/SSEE_data/kids_legacy/KiDS_Legacy_cosmic_shear_data_release/chains_and_config_files/xipm/KiDS_Legacy_values.ini
NZ_COV = np.loadtxt(RAIZ + 'data/Nz_covariance.txt')
NZ_INV = np.linalg.inv(NZ_COV)
_UNCORR = np.array([2.5374, -2.44484, -1.37982, -0.494275, 1.40234, 6.26323])
DZ_MEAN = np.linalg.cholesky(NZ_COV) @ _UNCORR

# --- forma por bin del IA, evaluada en el posterior oficial ---------------
# ORIGEN-VALOR: 5.70591 — media posterior ponderada de INTRINSIC_ALIGNMENT_PARAMETERS--A en output_nautilus_xipm_Fiducial.txt (1069 filas NaN fuera)
# ORIGEN-VALOR: 0.44424 — media posterior ponderada de INTRINSIC_ALIGNMENT_PARAMETERS--BETA, misma cadena
# ORIGEN-VALOR: 11.57762 — media posterior de LOG10_M_MEAN_1, misma cadena
# ORIGEN-VALOR: 12.30926 — media posterior de LOG10_M_MEAN_2, misma cadena
# ORIGEN-VALOR: 12.61513 — media posterior de LOG10_M_MEAN_3, misma cadena
# ORIGEN-VALOR: 12.80061 — media posterior de LOG10_M_MEAN_4, misma cadena
# ORIGEN-VALOR: 12.96842 — media posterior de LOG10_M_MEAN_5, misma cadena
# ORIGEN-VALOR: 13.12889 — media posterior de LOG10_M_MEAN_6, misma cadena
# (Se dejan escritas y no se leen de la cadena para no cambiar la verosimilitud
#  de dos corridas que estan en marcha y se reanudan con este modulo.)
_IA_A = 5.70591                      # posterior medio de la cadena oficial
_IA_BETA = 0.44424
_LOG10_M_PIV = 13.5                                        # values.ini
_F_R = np.array([0.158, 0.198, 0.206, 0.258, 0.207, 0.026])  # values.ini
_LOG10_M = np.array([11.57762, 12.30926, 12.61513, 12.80061, 12.96842,
                     13.12889])
IA_FORMA = _IA_A * _F_R * 10.0 ** (_IA_BETA * (_LOG10_M - _LOG10_M_PIV))

# fondo SSEE, fijo, leido del nucleo algebraico
SSEE_BG = dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2, h0=S.H0_GLOBAL / 100.0,
               ns=S.N_S, mnu=S.SUM_MNU_EV, w0=S.W0, wa=S.WA)
PLANCK_BG = dict(ombh2=0.02237, omch2=0.1200, h0=0.6736, ns=0.9649,
                 mnu=0.06, w0=-1.0, wa=0.0)

# EL BLANCO. logA que el CMB fija con el fondo de SSEE. No se toca aqui.
LOGA_CMB_SSEE = 3.0448340130228546

_CACHE = {}


def _bg(bg_key):
    if bg_key == 'SSEE':
        return dict(SSEE_BG)
    if bg_key == 'PLANCK':
        return dict(PLANCK_BG)
    ombh2, omch2, h0, ns = bg_key
    return dict(ombh2=ombh2, omch2=omch2, h0=h0, ns=ns, mnu=0.06,
                w0=-1.0, wa=0.0)


def _camb_cached(bg_key, As, logT_AGN):
    key = (bg_key, round(As, 15), round(logT_AGN, 6))
    if key not in _CACHE:
        bg = _bg(bg_key)
        # CACHE ACOTADA A 3 (2026-09-19). Antes guardaba hasta 300 espectros de
        # CAMB, y cada uno ocupa ~11 MB (medido): hasta ~3.3 GB por proceso. Con
        # dos corridas MPI (8 procesos) crecieron de 0.8 a 1.7 GB cada uno en una
        # hora, la maquina se quedo sin memoria, el kernel mato VS Code cuatro
        # veces y a las 09:23 se corto en seco. No hacian falta 300: con el
        # reparto rapido/lento Cobaya mueve los parametros rapidos con los lentos
        # FIJOS, asi que solo se reusa el punto lento actual (y el anterior si se
        # rechaza el paso). Se descarta el MAS VIEJO, no se vacia todo.
        while len(_CACHE) >= 3:
            _CACHE.pop(next(iter(_CACHE)))
        _CACHE[key] = K.run_camb(
            omch2=bg['omch2'], ombh2=bg['ombh2'], h0=bg['h0'], ns=bg['ns'],
            As=As, mnu=bg['mnu'], w=bg['w0'], wa=bg['wa'], logT_AGN=logT_AGN)
    return _CACHE[key]


def loglike(bg_key, logA, logT_AGN, A_scale, dz):
    dz = np.asarray(dz, float)
    As = np.exp(logA) * 1e-10
    try:
        r, p, kh, zpk, pk, gr = _camb_cached(bg_key, As, logT_AGN)
        ells, Cl, idx = K.cl_shear(D, r, p, kh, zpk, pk, gr,
                                   A_scale * IA_FORMA, dz)
        th = K.theory_vector(D, ells, Cl, idx, delta_c=0.0)   # Legacy: sin c
    except Exception:
        return -1e10
    dv = (th - D['d'])[MASK]
    chi2 = float(dv @ CINV @ dv)
    rr = dz - DZ_MEAN
    return -0.5 * (chi2 + float(rr @ NZ_INV @ rr))


def loglike_ssee(logA, logT_AGN, A_scale, dz1, dz2, dz3, dz4, dz5, dz6):
    return loglike('SSEE', logA, logT_AGN, A_scale,
                   [dz1, dz2, dz3, dz4, dz5, dz6])


def loglike_lcdmfijo(logA, logT_AGN, A_scale, dz1, dz2, dz3, dz4, dz5, dz6):
    return loglike('PLANCK', logA, logT_AGN, A_scale,
                   [dz1, dz2, dz3, dz4, dz5, dz6])


def loglike_lcdm(ombh2, omch2, h0, ns, logA, logT_AGN, A_scale,
                 dz1, dz2, dz3, dz4, dz5, dz6):
    bg_key = (round(ombh2, 6), round(omch2, 6), round(h0, 5), round(ns, 5))
    return loglike(bg_key, logA, logT_AGN, A_scale,
                   [dz1, dz2, dz3, dz4, dz5, dz6])


# ---------------- configuracion Cobaya ----------------
# NOTA: el prior REAL de los dz (gaussiano correlacionado, NZ_INV) se aplica
# UNA sola vez dentro de `loglike`. Lo que se declara aqui es deliberadamente
# ANCHO (escala 1.0, ~100x el corrimiento fisico de ~0.01) para que el
# muestreador sepa donde buscar sin volver a contar la restriccion. Es el
# mismo cuidado que en `cobaya_kids.py`, donde contar dos veces un prior fue
# un fallo encontrado antes de lanzar.
NUISANCE = {
    'logT_AGN': dict(prior=dict(min=7.3, max=8.3), ref=8.0, proposal=0.1,
                     latex=r'\log_{10}(T_\mathrm{AGN}/\mathrm{K})'),
    'A_scale': dict(prior=dict(min=-2.0, max=4.0), ref=1.0, proposal=0.15,
                    latex=r'A_\mathrm{IA}/A_\mathrm{IA}^\mathrm{off}'),
}
for _i in range(6):
    NUISANCE[f'dz{_i+1}'] = dict(
        prior=dict(dist='norm', loc=float(DZ_MEAN[_i]), scale=1.0),
        ref=float(DZ_MEAN[_i]), proposal=0.01, latex=rf'\delta z_{_i+1}')

LOGA = dict(prior=dict(min=1.5, max=4.5), ref=3.04, proposal=0.05,
            latex='\\log(10^{10}A_s)')

# Reparto rapido/lento: solo logA y logT_AGN entran en CAMB; A_scale y los 6
# dz actuan sobre el espectro ya calculado y la cache les acierta siempre.
# Razon MEDIDA en esta maquina para Legacy, no heredada de KiDS-1000:
#     paso que toca CAMB      3.70 s
#     paso que NO lo toca     0.69 s   -> 5.4x
# Es menor que el 18x de KiDS-1000 porque con 6 bines hay 21 pares en vez de
# 15, y el trozo barato (C_ell + xi_pm) crece mientras CAMB no.
_RAPIDOS = ['A_scale'] + [f'dz{i}' for i in range(1, 7)]
_RAZON = 5
import os as _os
_REANUDAR = _os.environ.get('KIDS_REANUDAR') == '1'
_MCMC = dict(Rminus1_stop=0.03, max_tries=10000, oversample_power=0.7,
             measure_speeds=False)


def _info(nombre, like, extra_params, lentos, chains_dir, covmat=None,
          loga_fijo=None, salida=None):
    p = dict(extra_params)
    # loga_fijo != None -> logA deja de ser parametro y entra como constante.
    p['logA'] = float(loga_fijo) if loga_fijo is not None else dict(LOGA)
    p.update(NUISANCE)
    mcmc = dict(_MCMC, blocking=[[1, lentos], [_RAZON, _RAPIDOS]])
    if covmat:
        mcmc['covmat'] = covmat
    return dict(
        likelihood={f'p06_growth.cobaya_kids_legacy.{nombre}': {
            'external': like, 'input_params': list(p.keys())}},
        params=p,
        sampler={'mcmc': mcmc},
        output=f'{chains_dir}/{salida or nombre.replace("loglike_", "")}',
        # REANUDAR (2026-09-19). Con force=True y resume=False, relanzar tras
        # un corte BORRABA las cadenas: el 2026-09-19 la maquina se corto con
        # ~680 pasos aceptados por cadena y dos horas de covmat aprendida.
        # `KIDS_REANUDAR=1` retoma desde el checkpoint; sin ella, arranque limpio.
        force=not _REANUDAR, resume=_REANUDAR)


def info_ssee(chains_dir, covmat=None):
    return _info('loglike_ssee', loglike_ssee, {}, ['logA', 'logT_AGN'],
                 chains_dir, covmat)


def info_sseefijo(chains_dir, covmat=None):
    """LA CONFIGURACION QUE SE PRESENTA (2026-09-19, decision de Mike).

    Fondo de SSEE clavado por algebra Y logA clavado en el valor que el CMB
    fija con ese mismo fondo (LOGA_CMB_SSEE). El crecimiento NO vuelve a
    cobrar un parametro que ya se pago en el CMB: A_s se cuenta UNA vez, y
    solo hasta que OP-18 lo derive de V_0.

    Libres aqui: los 8 nuisance (logT_AGN, A_scale, dz1..dz6). Cero libres
    cosmologicos. La version con logA suelto (`ssee`) queda como informacion
    adicional: al soltarlo se va a 0.49 sigma de este valor, o sea a nada.
    """
    return _info('loglike_ssee', loglike_ssee, {}, ['logT_AGN'],
                 chains_dir, covmat, loga_fijo=LOGA_CMB_SSEE,
                 salida='sseefijo')


def info_lcdmfijo(chains_dir, covmat=None):
    return _info('loglike_lcdmfijo', loglike_lcdmfijo, {},
                 ['logA', 'logT_AGN'], chains_dir, covmat)


def info_lcdm(chains_dir, covmat=None):
    extra = dict(
        ombh2=dict(prior=dict(min=0.019, max=0.026), ref=0.02237,
                   # ORIGEN-VALOR: 0.0005 — paso inicial de propuesta de Cobaya para ombh2, no es una medida
                   proposal=0.0005, latex=r'\Omega_b h^2'),
        omch2=dict(prior=dict(min=0.051, max=0.255), ref=0.1157,
                   proposal=0.005, latex=r'\Omega_c h^2'),
        h0=dict(prior=dict(min=0.64, max=0.82), ref=0.6898, proposal=0.02,
                latex='h'),
        ns=dict(prior=dict(min=0.84, max=1.1), ref=0.969, proposal=0.02,
                latex='n_s'))
    return _info('loglike_lcdm', loglike_lcdm, extra,
                 ['ombh2', 'omch2', 'h0', 'ns', 'logA', 'logT_AGN'],
                 chains_dir, covmat)


if __name__ == '__main__':
    from cobaya.run import run
    modelo = sys.argv[1] if len(sys.argv) > 1 else 'ssee'
    chains_dir = (sys.argv[2] if len(sys.argv) > 2
                  else '/mnt/datos/SSEE_data/chains_p6/kids_legacy')
    cov = sys.argv[3] if len(sys.argv) > 3 else None
    info = {'ssee': info_ssee, 'lcdm': info_lcdm,
            'lcdmfijo': info_lcdmfijo,
            'sseefijo': info_sseefijo}[modelo](chains_dir, cov)
    t0 = time.time()
    run(info)
    print(f'\nTERMINADO en {(time.time()-t0)/3600:.2f} h', flush=True)
