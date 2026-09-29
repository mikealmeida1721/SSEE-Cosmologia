#!/usr/bin/env python3
"""
cobaya_conjunta.py — CORRIDA CONJUNTA de las cuatro sondas con el fondo clavado.

QUE PRUEBA ESTO, Y QUE NO
-------------------------
NO prueba el modelo. El modelo ya hizo lo suyo: sonda por sonda empata con LCDM
con el fondo clavado por algebra y A_s clavado, que se paga UNA VEZ en el CMB y
no se vuelve a cobrar. Cero libres cosmologicos.

Esto prueba LAS SONDAS. La pregunta es si combinarlas introduce sesgos que por
separado no tienen: corridas juntas, ¿devuelven cada una el MISMO chi2 que dan
por separado? Lo esperado es que si. Si NO, el problema es la combinacion de
sondas, no el fondo.

POR QUE HAY QUE CORRERLO AUNQUE «SE SEPA» EL RESULTADO
Sumar los chi2 individuales sobre el papel da la respuesta por construccion y no
demuestra nada: con todo clavado el verosimil conjunto ES separable. Pero eso es
algebra, no la corrida. Un muestreador de 27 dimensiones puede devolver otra
cosa por convergencia, por efectos de volumen en los nuisance, por priors que
muerden al juntar, o por cache compartida entre patas. Con fisica real el
resultado se PREDICE, no se sabe. Se corre para estar seguros.

MONTAJE
    logA        CONSTANTE = 3.0448340130228546 (CANONICAL logA_cmb_ssee).
                No es libre: es parte del fondo clavado.
    fondo       omega_b, omega_c, H0, n_s, w0, wa del nucleo. Nada se ajusta.

    sonda                         libres PRIVADOS        referencia individual
    CMB plik_lite TTTEEE+lowT+lowE  tau            (1)   1003.586
    KiDS-Legacy xi_pm               logT_AGN,A_scale,
                                    dz1..dz6       (8)    417.971
    BOSS DR12 P(k) LPT              b1,b2,bs x 6   (18)   la mide `boss_clavado`
                                    (escala MARGINAL; en escala real es
                                     197.438 libre / 198.07 clavado = 0.63)
    BAO DESI DR2                    ninguno        (0)     10.859
                                                   --
                                                   27 muestreados

BAO queda FUERA del muestreador. No es un atajo: con cero libres su chi2 es una
constante, y una constante en el log-verosimil no puede mover el posterior de
nada. Cobaya ademas la rechaza («seems not to depend on any parameters»), y
meterla habria exigido inventarle una dependencia falsa. Se suma al total al
leer, declarada aparte. Es la unica sonda cuyo chi2 es identico sola o
acompanada por construccion, y por la razon mas fuerte que existe: no depende de
nada que se mueva.

LO QUE YA SE SABIA DE BOSS, Y QUE NO HAY QUE VOLVER A DESCUBRIR
BOSS casi no ve A_s. Medido el 2026-09-13 en `base_sin_particula.log`, que YA
era una corrida conjunta con un solo A_s compartido (3 sondas, 1.01 h):

       logA        CMB       KiDS       BOSS        TOTAL
     3.0175    1006.71     277.19     197.80      1481.70   <- min conjunto
     3.0450    1003.59     282.21     198.07      1483.87   <- el del CMB

  recorrido en toda la malla de 9 nodos:  BOSS 1.37 · KiDS 29.79 · CMB 2109.5
  BOSS con A_s libre 197.438 -> en el clavo 198.07 = 0.63

Ese 0.63 es la razon por la que se puede unificar el fondo con A_s clavado:
BOSS no lo ve, el CMB lo fija, y con el mismo fondo los dos ven el mismo
universo. (Aquella corrida usaba KiDS-1000, que entonces pedia un A_s mas bajo
y tiraba el minimo conjunto a 3.0175. Con KiDS-LEGACY, desde el 2026-09-20, la
cizalla pide el MISMO A_s que el CMB a 0.49 sigma; rehacer la conjunta con
Legacy es justo lo que falta y es lo que hace este modulo.)

LAS DOS ESCALAS DE CHI2 DE BOSS — LA TRAMPA, POR TERCERA VEZ
BOSS tiene dos chi2 distintos y NO son comparables entre si:
  REAL      perfil con las 6 molestias por conjunto ajustadas (`cobaya_boss.run`).
            Es el que da 197.438 / 198.07. Es el publicado.
  MARGINAL  `chi2_marg_set`, que lleva dentro el termino de volumen ln det F.
            Da 75.23 en el minimo. Es el que devuelve el verosimil de cobaya.
`conjunta_tres_sondas.py` ya se equivoco con esto una vez y lo dejo escrito: la
version marginal «descuadraba el logA de BOSS 1.85 sigma». El 2026-09-26 se
volvio a caer en ella: leer el perfil MARGINAL de la cadena en banda estrecha
dio un coste de +12.45 para BOSS, veinte veces el 0.63 real, y contradecia una
medicion que ya estaba en el repo desde el 09-13.
Aqui el muestreador usa el MARGINAL —que es lo correcto para muestrear— y por
eso la referencia individual de BOSS se mide con el modo `boss_clavado`, que
corre BOSS SOLA con el MISMO verosimil. Nunca contra el 197.438/198.07.

COMO SE LEE EL RESULTADO
Cobaya escribe una columna chi2__<sonda> por pata. Se compara, sonda a sonda, el
chi2 del mejor ajuste conjunto contra el de su corrida individual:
    diferencia ~ 0    -> combinar no sesga. Es lo que se espera.
    diferencia grande -> la combinacion crea degeneracion que la sonda sola no
                         tiene. Seria un hallazgo sobre las SONDAS.

CONTROL (R53). Antes de muestrear, el script evalua las cuatro patas en el punto
de referencia y comprueba que el CMB da 1003.586 y KiDS 417.971. Si el cableado
no reproduce lo ya publicado, para: lo que venga despues no valdria.

Uso:
    mpirun -n 4 .venv/bin/python3 src/p06_growth/cobaya_conjunta.py conjunta
    .venv/bin/python3          src/p06_growth/cobaya_conjunta.py boss_clavado
    .venv/bin/python3          src/p06_growth/cobaya_conjunta.py control
"""
import json
import os
import sys

import numpy as np

# MODO COLA. CAMB abre hilos OpenMP por su cuenta: el 2026-09-26 el control
# declaraba 1 core, uso 592% y la carga de la maquina llego a 18 con el tope
# puesto en 10. Se fija ANTES de importar nada que arrastre BLAS o CAMB.
for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
           "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, os.environ.get("SSEE_HILOS", "1"))

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
for _p in ("src", "src/p03_cmb", "src/p06_growth"):
    _q = os.path.join(_R, _p)
    if _q not in sys.path:
        sys.path.insert(0, _q)

LOGA_CLAVO = 3.0448340130228546      # ORIGEN: CANONICAL_VALUES.yaml (logA_cmb_ssee)
CAD = "/mnt/datos/SSEE_data/chains_p6/conjunta"

# Referencias individuales, con el MISMO logA clavado.
#   CMB  : results/logs/cmb_dbic_tau_ajustado.json -> SSEE/chi2_min
#   KiDS : CANONICAL_VALUES chi2_min_ssee_unif (corrida sseefijo)
#   BAO  : results/logs/multisonda_fondo_clavado.json, cero libres
# ORIGEN: results/logs/base_sin_particula.log  (la tabla de BOSS del docstring)
REF = dict(cmb=1003.5860397789045, kids=417.971, bao=10.858822657229455)

# ── el fondo, del nucleo. Nada de esto se ajusta en ningun sitio ────────────
from ssee_core import (H0_GLOBAL, N_S, OMEGA_B_H2,  # noqa: E402
                       OMEGA_C_H2, W0, WA)

_BG = dict(ombh2=OMEGA_B_H2, omch2=OMEGA_C_H2, H0=H0_GLOBAL, ns=N_S)

_cmb_eval = None
_kids = None
_boss = None


def _carga():
    global _cmb_eval, _kids, _boss
    if _cmb_eval is None:
        from cmb_eval import chi2_y_s8
        _cmb_eval = chi2_y_s8
    if _kids is None:
        import cobaya_kids_legacy as K
        _kids = K
    if _boss is None:
        import cobaya_boss as B
        _boss = B


# ── las cuatro patas, cada una con sus libres PRIVADOS ──────────────────────
def loglike_cmb(tau):
    _carga()
    c, _ = _cmb_eval(dict(_BG, logA=LOGA_CLAVO, tau=tau), W0, WA)
    return -0.5 * float(c)


def loglike_kids(logT_AGN, A_scale, dz1, dz2, dz3, dz4, dz5, dz6):
    _carga()
    return _kids.loglike_ssee(logA=LOGA_CLAVO, logT_AGN=logT_AGN,
                              A_scale=A_scale, dz1=dz1, dz2=dz2, dz3=dz3,
                              dz4=dz4, dz5=dz5, dz6=dz6)


def loglike_boss(**kw):
    _carga()
    return _boss.loglike_ssee(logA=LOGA_CLAVO, **kw)


# BAO NO entra como pata del muestreador, y no es un atajo: es exacto.
# Cobaya la rechaza —«Component 'bao' seems not to depend on any parameters»—
# y tiene razon: con el fondo clavado por algebra, BAO tiene CERO libres, asi
# que su chi2 es una CONSTANTE. Una constante en el log-verosimil no puede
# mover el posterior de ningun otro parametro: desplaza el total y nada mas.
# Incluirla habria exigido inventarle una dependencia falsa. Se suma al total
# al leer el resultado, declarada aparte, y su chi2 es el mismo sola o
# acompanada por la razon mas fuerte que hay: no depende de nada que se mueva.
CHI2_BAO = REF["bao"]      # 10.858822657229455 · 13 puntos · 0 libres


# ── parametros ──────────────────────────────────────────────────────────────
def _p_cmb():
    return dict(tau=dict(prior=dict(min=0.01, max=0.20), ref=0.0554590468914248,
                         proposal=0.006, latex=r'\tau'))


def _p_kids():
    _carga()
    p = {k: dict(v) for k, v in _kids.NUISANCE.items()}
    return p


def _p_boss():
    _carga()
    p = _boss._params('SSEE')
    p.pop('logA')
    return p


# Matriz de PROPUESTA (no toca verosimilitud ni prior: no puede mover ningun
# chi2). La construye covmat_conjunta.py. Sin ella la conjunta daba 1.8
# muestras/min/cadena, porque con logA clavado la degeneracion A_s-tau esta
# rota y el CMB fija tau a sigma=0.00077 --- cuarenta veces mas estrecho que
# el ancho del prior --- y tau vive en el bloque LENTO, asi que cada propuesta
# rechazada costaba un CAMB entero.
COVMAT = f'{CAD}/propuesta_conjunta.covmat'
COVMAT_BOSS = '/mnt/datos/SSEE_data/chains_p6/boss/ssee.covmat'


def _velocidades(pk, pb, n=5):
    """Segundos por evaluacion de KiDS y de BOSS en el punto de referencia, MEDIDOS aqui."""
    import time
    ref = lambda p: {k: (v['ref'] if not isinstance(v.get('ref'), dict) else v['ref'].get('loc'))
                     for k, v in p.items() if isinstance(v, dict) and 'prior' in v}
    rk, rb = ref(pk), ref(pb)
    loglike_kids(**rk); loglike_boss(**rb)          # calentamiento (caches)
    t0 = time.perf_counter(); [loglike_kids(**rk) for _ in range(n)]; tk = (time.perf_counter() - t0) / n
    t0 = time.perf_counter(); [loglike_boss(**rb) for _ in range(n)]; tb = (time.perf_counter() - t0) / n
    return tk, tb


def info_conjunta(b3=False):
    pc, pk, pb = _p_cmb(), _p_kids(), _p_boss()
    todos = dict(pc); todos.update(pk); todos.update(pb)
    # Reparto rapido/lento medido en esta maquina: tau toca CAMB (0.33 s) y
    # logT_AGN toca CAMB de KiDS (3.5 s); el resto viaja sobre espectros ya
    # calculados (KiDS 0.69 s, BOSS 0.022 s).
    lentos = ['tau', 'logT_AGN']
    rapidos = [k for k in todos if k not in lentos]
    bloques, covmat, salida = [[1, lentos], [5, rapidos]], COVMAT, 'conjunta'
    if b3:
        # RELANZADA 29-sep (decision de Mike). La conjunta de 3 dias se estanco en
        # R-1 0.33: el bloque rapido juntaba KiDS (lento entre los rapidos) y BOSS
        # (30x mas rapido), y cada paso de BOSS pagaba un KiDS. BOSS sola convergio
        # en <2 h. Se parte el bloque en KiDS | BOSS y BOSS se sobremuestrea en la
        # razon de tiempos MEDIDA al arrancar, para que cada bloque reciba el mismo
        # tiempo. Solo cambia la PROPUESTA: ni verosimilitud ni prior.
        # Propuesta de arranque: la covarianza que aprendio la corrida anterior.
        tk, tb = _velocidades(pk, pb)
        fb = max(5, int(round(5 * tk / tb)))
        rk = [k for k in rapidos if k in pk]; rb = [k for k in rapidos if k in pb]
        bloques, covmat, salida = [[1, lentos], [5, rk], [fb, rb]], f'{CAD}/conjunta.covmat', 'conjunta_b3'
        json.dump(dict(fecha=str(__import__('datetime').date.today()), seg_kids=tk, seg_boss=tb,
                       sobremuestreo=dict(lentos=1, kids=5, boss=fb), covmat=covmat),
                  open(os.path.join(_R, 'results', 'logs', 'conjunta_b3_bloques.json'), 'w'), indent=1)
        print(f'  bloques: KiDS {tk:.3f} s, BOSS {tb:.4f} s -> sobremuestreo BOSS {fb}')
    return dict(
        likelihood={
            'cmb':  dict(external=loglike_cmb,  input_params=list(pc.keys())),
            'kids': dict(external=loglike_kids, input_params=list(pk.keys())),
            'boss': dict(external=loglike_boss, input_params=list(pb.keys())),
        },
        params=todos,
        sampler={'mcmc': dict(Rminus1_stop=0.05, max_tries=20000,
                              oversample_power=0.7, measure_speeds=False,
                              covmat=covmat,
                              blocking=bloques)},
        output=f'{CAD}/{salida}', force=True, resume=False)


def info_boss_clavado():
    """BOSS SOLA con el mismo logA clavado: la referencia individual de BOSS
    en la MISMA escala que usa la conjunta (chi2 marginalizado)."""
    pb = _p_boss()
    return dict(
        likelihood={'boss': dict(external=loglike_boss,
                                 input_params=list(pb.keys()))},
        params=pb,
        sampler={'mcmc': dict(Rminus1_stop=0.05, max_tries=20000,
                              covmat=COVMAT_BOSS)},
        output=f'{CAD}/boss_clavado', force=True, resume=False)


def control():
    """R53: si el cableado no reproduce lo ya publicado, nada de lo que venga
    despues vale. Se corre SIEMPRE antes de muestrear.

    NO minimiza: evalua en el mejor ajuste YA conocido de cada sonda. Minimizar
    los 8 nuisance de KiDS costaba mas de 45 min y no hacia falta --- lo que se
    comprueba es el CABLEADO, no el minimo. Medido 2026-09-26:
        CMB  1003.5860 contra 1003.5860 publicado
        KiDS  417.9705 contra  417.9710 publicado
    (log: results/logs/conjunta_control.json)
    """
    _carga()
    # tau: el mejor ajuste del CMB (cmb_dbic_tau_ajustado.json -> SSEE/mejor)
    with open(os.path.join(_R, 'results', 'logs', 'cmb_dbic_tau_ajustado.json')) as fh:
        tau = json.load(fh)['SSEE']['mejor']['tau']
    c_cmb = -2 * loglike_cmb(tau)
    # nuisances de KiDS: el mejor ajuste de la corrida sseefijo, LEIDO de la cadena
    base = '/mnt/datos/SSEE_data/chains_p6/kids_legacy/sseefijo.'
    cab = open(base + '1.txt').readline().split()[1:]
    nuis = ['logT_AGN', 'A_scale', 'dz1', 'dz2', 'dz3', 'dz4', 'dz5', 'dz6']
    filas = [np.atleast_2d(np.loadtxt(base + f'{k}.txt')) for k in range(1, 5)]
    a = np.vstack(filas)
    j = a[:, cab.index('chi2')].argmin()
    x0 = tuple(float(a[j, cab.index(n)]) for n in nuis)
    c_kids = -2 * loglike_kids(*x0)
    ok_c = abs(c_cmb - REF['cmb']) < 0.5
    ok_k = abs(c_kids - REF['kids']) < 1.0
    print(f"  CONTROL con logA = {LOGA_CLAVO:.10f}")
    print(f"    CMB  chi2 = {c_cmb:10.4f}   publicado {REF['cmb']:.4f}   "
          f"dif {c_cmb - REF['cmb']:+.4f}   {'OK' if ok_c else 'NO CUADRA'}")
    print(f"    KiDS chi2 = {c_kids:10.4f}   publicado {REF['kids']:.4f}   "
          f"dif {c_kids - REF['kids']:+.4f}   {'OK' if ok_k else 'NO CUADRA'}")
    print(f"    BAO  chi2 = {REF['bao']:10.4f}   cero libres")
    json.dump(dict(logA=LOGA_CLAVO, cmb=c_cmb, cmb_ref=REF['cmb'],
                   kids=c_kids, kids_ref=REF['kids'], bao=REF['bao'],
                   hilos=os.environ.get('OMP_NUM_THREADS'),
                   pasa=bool(ok_c and ok_k)),
              open(os.path.join(_R, 'results', 'logs',
                                'conjunta_control.json'), 'w'), indent=1)
    return ok_c and ok_k


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'control'
    os.makedirs(CAD, exist_ok=True)
    if modo == 'control':
        sys.exit(0 if control() else 1)
    # El control va SIEMPRE antes de muestrear, no como paso aparte que se
    # pueda olvidar. Solo en el rango 0 si es MPI.
    _rango = int(os.environ.get('OMPI_COMM_WORLD_RANK',
                                os.environ.get('PMI_RANK', '0')))
    if _rango == 0 and not control():
        print('  El cableado no reproduce lo publicado. NO se muestrea.')
        sys.exit(1)
    from cobaya.run import run
    run(info_conjunta() if modo == 'conjunta' else
        info_conjunta(b3=True) if modo == 'conjunta_b3' else info_boss_clavado())
