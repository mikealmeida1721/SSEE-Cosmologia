#!/usr/bin/env python3
"""
Likelihood de Cobaya para los multipolos CRUDOS de BOSS DR12 — R1/R2.

POR QUE EXISTE. La fisica (LPT de velocileptors + ventana + Alcock-Paczynski)
ya estaba escrita y probada en boss_lpt_R1R2.py. Lo que fallaba era el
EXPLORADOR: scipy.minimize sobre 37 libres daba un perfil que saltaba +-100 en
chi2 segun donde tuviera suerte cada busqueda, y la diferencia que queremos
medir entre modelos es de orden 3. Medido el 2026-09-07:

    logA   3.20    3.25    3.30    3.35
    chi2  404.2   330.8   359.1   250.7        <- eso no es una curva

Ademas el minimo caia en el borde de la rejilla, en logA=3.37 (A_s un 38% por
encima de Planck), que ningun dato de galaxias pide. Aqui no se BUSCA el
minimo: se MUESTREA el posterior, que es lo que ya funciono en R3/R4 con
cobaya_kids.py. El modelo no cambia; cambia quien lo recorre.

LOS DOS FONDOS VAN FIJOS. SSEE por algebra, LCDM por Planck. No es la misma
eleccion que en KiDS (alli LCDM llevaba el fondo LIBRE, 13 vs 9 libres) y la
razon es de coste, no de gusto: con el fondo libre habria que reconstruir los
templates LPT en cada muestra (~3 s por conjunto, ~18 s por llamada), lo que
pone la cadena en cientos de horas. Con el fondo fijo los templates se calculan
UNA vez y la llamada baja a milisegundos.

Consecuencia honesta, que hay que escribir en el paper: aqui Delta k = 0. Los
dos modelos llevan exactamente los mismos 37 libres y la comparacion es de
chi2 puro, sin credito por parsimonia. La ventaja en numero de parametros de
SSEE vive donde se gana de verdad --- el CMB (k=2 frente a 6) y la cizalla de
KiDS (9 frente a 13) ---, no aqui. Lo que esta corrida contesta es mas estrecho
y mas limpio: con la MISMA libertad de molestia, el fondo algebraico ajusta el
agrupamiento crudo tan bien como el de Planck?

LIBRES (37), de los que se MUESTREAN 19:
    logA                      (1)   amplitud primordial ln(1e10 A_s), COMPARTIDA
    b1, b2, bs                (18)  bias por (z_bin, hemisferio); b1 es LAGRANGIANO
    alpha0, alpha2            (12)  contraterminos EFT   --- marginalizados
    SN0                        (6)  ruido de disparo residual --- marginalizado

POR QUE SE MARGINALIZAN 18. Entran LINEALES en el modelo, asi que su integral
tiene forma cerrada (R.chi2_marg_set) y muestrearlos no aporta nada. Y eran
justo los que impedian converger: R-1 por familia tras 45 min de la primera
cadena LCDM (4 cadenas, mitad de burn-in) daba
    a0 1.955   a2 1.502   sn 0.919  |  b1 0.524  b2 0.579  bs 0.618  logA 0.218
--- los tres peores son los tres lineales. La cuenta de libres que se declara
en el paper sigue siendo 37: marginalizar no es fijar.

PRIORS. Se declaran SOLO aqui, en Cobaya, y NO se suma ningun termino de prior
dentro de loglike. Es la leccion del bug que cobaya_kids.py documenta en su
NOTA CRITICA: alli delta_c llevaba el mismo prior gaussiano declarado en Cobaya
y sumado en la verosimilitud, o sea contado dos veces. Aqui hay una sola
puerta.

f*sigma8 NO es un parametro: es DERIVADO. Con el fondo fijo, f y la forma de
sigma8 son constantes por (modelo, z), y la amplitud entra como factor exacto
sqrt(A_s/A_ref). Asi que f*sigma8(z) = f * s8_ref(z) * sqrt(e^logA * 1e-10 /
A_ref), funcion determinista de logA: sale de la cadena sin re-correr nada.
Mismo truco que R3 uso con sqrt(As) en KiDS.
"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src/p06_growth')
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src/p11_sondas')

np.seterr(all='ignore')

KMAX = float(os.environ.get('BOSS_KMAX', '0.20'))
_ARGV = list(sys.argv)                        # boss_lpt_R1R2 lee KMAX de argv,
sys.argv = [sys.argv[0], str(KMAX)]           # asi que se le presta y se
import boss_lpt_R1R2 as R                     # noqa: E402   devuelve intacto
sys.argv = _ARGV

SETS = R.build()
NSET = len(SETS)
NPTS = sum(st['npts'] for st in SETS)
NMUESTRA = 1 + 3 * NSET      # logA + (b1,b2,bs) x conjunto
NMARG = 3 * NSET             # (a0,a2,sn), integrados en cerrado
NFREE = NMUESTRA + NMARG     # 37: la cuenta que va en el paper


# ACANTILADOS DE LA VENTANA --- MEDIDOS, Y YA CORREGIDOS (2026-09-07).
# La convolucion extrapolaba en ley de potencias con un indice sacado de los
# propios valores del borde (mcfit, extrap=True). Si los multipolos llegaban al
# borde con una forma rara, la extrapolacion explotaba. Medido en z1 NGC a
# logA=3.04, ANTES del arreglo:
#     th = [1.2, 0, 0, 0, 0,     0]  ->  modelo -2.3e9   (el dato es 7.7e4)
#     th = [1.2, 0, 0, 0, 0, -3000]  ->  modelo  1.6e80
#     th = [1.0,-1.0,0.5,30,20,-2000] -> modelo  7.5e4, chi2 = 161  (sano)
# O sea paredes de 80 ordenes de magnitud a un paso de la zona buena. NO era
# culpa del minimizador: era fragilidad numerica del modelo.
# El indice del relleno es ahora FIJO (boss_rsd_model.Window, NOTA CRITICA),
# con lo que la ventana vuelve a ser un operador lineal y los acantilados
# desaparecen. El techo de abajo se conserva igualmente como red.
CHI2_TECHO = 1.0e8


def loglike(name, v):
    """v = [logA, (b1,b2,bs) x NSET].

    (a0, a2, sn) NO se muestrean: se integran en forma cerrada dentro de
    R.chi2_marg_set, que devuelve chi2(lambda_hat) + ln det F. Su prior
    gaussiano vive alli, en R.SIGMA_LIN --- una sola puerta, como manda la
    leccion de delta_c en cobaya_kids.py.
    """
    logA = v[0]
    c = 0.0
    for i, st in enumerate(SETS):
        ci, _ = R.chi2_marg_set(st, name, logA, v[1 + 3 * i: 4 + 3 * i])
        c += ci
        if not np.isfinite(c) or c >= CHI2_TECHO:
            return -1e10
    return -0.5 * c


def _nombres():
    n = ['logA']
    for st in SETS:
        for p in ('b1', 'b2', 'bs'):
            n.append(f'{p}_{st["zb"]}{st["cap"]}')
    return n


NOMBRES = _nombres()


def loglike_ssee(**kw):
    return loglike('SSEE', [kw[n] for n in NOMBRES])


def loglike_lcdm(**kw):
    return loglike('LCDM', [kw[n] for n in NOMBRES])


# ---------------- configuracion Cobaya ----------------
# Cotas y escalas de propuesta: las mismas que se midieron al arreglar el
# minimizador. b1 es LAGRANGIANO, asi que b1~1.0-1.3 corresponde al b_Euleriano
# ~2.0-2.3 que BOSS publica. Los contraterminos y el ruido de disparo llevan
# gaussianas anchas centradas en cero --- son direcciones casi planas y sin
# ellas la cadena se va a la deriva, que es media culpa del fallo del
# minimizador.
# Solo los tres NO lineales se declaran aqui. Los priors de (a0,a2,sn)
# se mudaron a R.SIGMA_LIN, dentro de la marginalizacion.
_PRIOR = dict(
    b1=dict(prior=dict(min=0.5, max=5.0), proposal=0.03),
    b2=dict(prior=dict(dist='norm', loc=0.0, scale=5.0), proposal=0.3),
    bs=dict(prior=dict(dist='norm', loc=0.0, scale=5.0), proposal=0.3),
)
_ORDEN = ('b1', 'b2', 'bs')
# Semilla dentro de la zona sana, medida arriba. No es un ajuste: es solo el
# punto desde el que se busca el arranque de cada conjunto.
_SEMILLA = [1.0, -1.0, 0.5]


def arranques(name, logA=2.90):
    """Punto de partida por conjunto: una bajada CORTA desde la semilla, solo
    para que la cadena no nazca lejos. No define el resultado --- el resultado
    sale del posterior. Con (a0,a2,sn) marginalizados la bajada es sobre 3
    libres bien escalados, sin el problema de escala que tenia antes
    (b1~1 junto a SN0~1e4 en el mismo vector)."""
    from scipy.optimize import minimize
    cot = [(0.5, 5.0), (-10.0, 10.0), (-10.0, 10.0)]
    out = []
    for st in SETS:
        u = np.array(_SEMILLA, dtype=float)
        for _ in range(3):
            rr = minimize(
                lambda w: R.chi2_marg_set(st, name, logA, w)[0], u,
                method='Nelder-Mead', bounds=cot,
                options=dict(maxiter=2000, xatol=1e-4, fatol=1e-4))
            u = rr.x
        out.append(u.tolist())
    return out


def _params(name):
    p = dict(logA=dict(prior=dict(min=2.0, max=4.0), ref=2.90, proposal=0.02,
                       latex=r'\log(10^{10}A_s)'))
    ini = arranques(name)
    for st, u0 in zip(SETS, ini):
        for j, k in enumerate(_ORDEN):
            q = dict(_PRIOR[k])
            q['ref'] = float(u0[j])
            q['latex'] = rf'{k}^{{{st["zb"]}{st["cap"]}}}'
            p[f'{k}_{st["zb"]}{st["cap"]}'] = q
    return p


def _info(name, chains_dir, fn):
    p = _params(name.upper())
    return dict(
        likelihood={f'p06_growth.cobaya_boss.loglike_{name}': {
            'external': fn, 'input_params': list(p.keys())}},
        params=p,
        sampler={'mcmc': {'Rminus1_stop': 0.05, 'max_tries': 20000}},
        output=f'{chains_dir}/{name}', force=True, resume=False)


def info_ssee(chains_dir):
    return _info('ssee', chains_dir, loglike_ssee)


def info_lcdm(chains_dir):
    return _info('lcdm', chains_dir, loglike_lcdm)


def plantilla_fsigma8():
    """f y sigma8 de referencia por (modelo, conjunto). f*sigma8 se reconstruye
    de la cadena como f * s8_ref * sqrt(e^logA * 1e-10 / A_ref)."""
    out = {}
    for m in ('SSEE', 'LCDM'):
        out[m] = [dict(zb=st['zb'], cap=st['cap'], z=st['z'],
                       f=float(st['lpt'][m]['f']),
                       s8_ref=float(st['lpt'][m]['sigma8']))
                  for st in SETS]
    out['A_ref'] = R.AS_REF
    return out


if __name__ == '__main__':
    from cobaya.run import run
    nombre = _ARGV[1] if len(_ARGV) > 1 else 'ssee'
    chains = (_ARGV[2] if len(_ARGV) > 2 and not _ARGV[2].startswith('--')
              else '/mnt/datos/SSEE_data/chains_p6/boss')
    os.makedirs(chains, exist_ok=True)
    print(f'  R1/R2 BOSS LPT — {nombre.upper()}  k_max={KMAX}')
    print(f'  {NSET} conjuntos, {NPTS} puntos, {NFREE} libres')
    # INGREDIENTES (regla de Mike, 2026-10-01): cada modelo con los SUYOS. Se
    # imprimen los que de verdad entran y se comparan contra su fuente; si uno
    # no cuadra, no se corre (R1/R2 del 2026-09-07 corrio SSEE con el m_nu de LCDM).
    import ssee_core as _S
    from lcdm_planck import LCDM_PLANCK as _LP
    _fuente = {'SSEE': dict(Om=_S.OMEGA_M_TOTAL, h=_S.H0_GLOBAL / 100, ombh2=_S.OMEGA_B_H2, ns=_S.N_S,
                            w0=_S.W0, wa=_S.WA, mnu=_S.SUM_MNU_EV),
               'LCDM': dict(h=_LP['H0'] / 100, ombh2=_LP['ombh2'], mnu=_LP['mnu'], w0=-1.0, wa=0.0)}[nombre.upper()]
    _usa = R.COSMO[nombre.upper()]
    print('  INGREDIENTES ' + nombre.upper() + ': ' + '  '.join(f'{k}={_usa[k]!r}' for k in sorted(_usa)), flush=True)
    _mal = [k for k, v in _fuente.items() if abs(_usa[k] - v) > 1e-9]
    if _mal:
        sys.exit(f'  INGREDIENTES QUE NO CUADRAN con su fuente: {_mal} -> no se corre')
    print('  ingredientes verificados contra su fuente: OK', flush=True)
    if '--solo-ingredientes' in _ARGV:   # verifica sin correr cadenas (para cadenas ya hechas)
        sys.exit(0)
    info = info_ssee(chains) if nombre == 'ssee' else info_lcdm(chains)
    t0 = time.time()
    run(info)
    print(f'\nTERMINADO en {(time.time()-t0)/3600:.2f} h', flush=True)
