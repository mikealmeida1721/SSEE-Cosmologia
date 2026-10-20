"""minimo_sesgos.py — minimizacion robusta de los sesgos (b1, b2, bs) a lo largo de un perfil.

POR QUE (2026-10-01). Los perfiles de w_c en BOSS minimizaban los sesgos con
Nelder-Mead desde un solo punto P0 = (2, 0, 0). El mismo punto de la rejilla dio
chi2 = 68.805 el 2026-09-08 y 69.118 el 2026-10-01, y arrancando solo desde P0
hubo puntos atascados hasta 23 de chi2 por encima: minimos locales. Un perfil
con minimos locales dibuja una curva que no es la del dato.

QUE HACE, por punto de la rejilla y por conjunto de datos:
  1. arranques fijos: P0 y cuatro semillas de un medio factorial en
     (b1, b2, bs) = (2 -+ 0.5, -+2, -+2); se queda el menor;
  2. barridos adelante/atras: cada punto re-arranca desde el optimo de sus dos
     vecinos; se repite hasta que un barrido entero no mejora nada en mas de
     TOL_BARRIDO (maximo MAX_BARRIDOS).
CONTROL (R53), del otro lado: en el minimo del perfil y en los dos extremos,
una busqueda INDEPENDIENTE con N_CONTROL arranques aleatorios (semilla fija)
no debe bajar el chi2 en mas de TOL_CONTROL. Si lo baja, el perfil no vale.
"""
import time

import numpy as np
from scipy.optimize import minimize

P0 = np.array([2.0, 0.0, 0.0])
# ORIGEN-VALOR: 0.5, 2 — semillas: medio factorial alrededor de P0, dentro de las cotas
SEMILLAS = [np.array(s) for s in ([1.5, -2.0, -2.0], [1.5, 2.0, 2.0], [2.5, -2.0, 2.0], [2.5, 2.0, -2.0])]
COTAS = [(0.5, 5.0), (-10.0, 10.0), (-10.0, 10.0)]
TOL_BARRIDO = 0.01      # ORIGEN-VALOR: 0.01 — en chi2; 100 veces por debajo de Delta chi2 = 1
MAX_BARRIDOS = 4
N_CONTROL = 10
TOL_CONTROL = 0.01      # ORIGEN-VALOR: 0.01 — mismo umbral que el barrido
SEMILLA_RNG = 20261001


def min_set(f, u0):
    """Nelder-Mead con 3 reinicios desde u0 -> (chi2, u)."""
    u, best = np.asarray(u0, float).copy(), np.inf
    for _ in range(3):
        rr = minimize(f, u, method='Nelder-Mead', bounds=COTAS,
                      options=dict(maxiter=3000, xatol=1e-4, fatol=1e-4))
        if rr.fun < best:
            best, u = float(rr.fun), rr.x
    return best, u


def perfil_robusto(rej, fun_punto, etiq=''):
    """rej: valores del parametro; fun_punto(x) -> lista de funciones chi2(u), una por conjunto.

    Devuelve dict con chi2 final, chi2 solo-P0, chi2 tras arranques fijos,
    barridos hechos, mejora del ultimo barrido y el control."""
    fs = [fun_punto(x) for x in rej]
    n, m = len(rej), len(fs[0])
    c = np.full((n, m), np.inf)
    u = [[None] * m for _ in range(n)]
    c_p0 = np.zeros(n)
    for i in range(n):
        t0 = time.time()
        for j in range(m):
            for k, s in enumerate([P0] + SEMILLAS):
                cc, uu = min_set(fs[i][j], s)
                if k == 0:
                    c_p0[i] += cc
                if cc < c[i, j]:
                    c[i, j], u[i][j] = cc, uu
        print(f'  [{etiq}] {rej[i]:.6f}  P0 {c_p0[i]:10.3f}  arranques {c[i].sum():10.3f}  [{time.time()-t0:.0f}s]', flush=True)
    c_fijos = c.sum(axis=1).copy()
    mejoras = []
    for b in range(MAX_BARRIDOS):
        mejor = 0.0
        orden = list(range(n)) if b % 2 == 0 else list(range(n - 1, -1, -1))
        for i in orden:
            for v in (i - 1, i + 1):
                if 0 <= v < n:
                    for j in range(m):
                        cc, uu = min_set(fs[i][j], u[v][j])
                        if cc < c[i, j] - 1e-9:
                            mejor = max(mejor, c[i, j] - cc)
                            c[i, j], u[i][j] = cc, uu
        mejoras.append(float(mejor))
        print(f'  [{etiq}] barrido {b + 1}: mejora maxima {mejor:.4f}', flush=True)
        if mejor < TOL_BARRIDO:
            break
    tot = c.sum(axis=1)
    rng = np.random.default_rng(SEMILLA_RNG)
    imin = int(np.argmin(tot))
    ctrl = {}
    for i in sorted({0, imin, n - 1}):
        mejor_azar = 0.0
        for _ in range(N_CONTROL):
            for j in range(m):
                s = np.array([rng.uniform(1.0, 3.5), rng.uniform(-5, 5), rng.uniform(-5, 5)])
                cc, _u = min_set(fs[i][j], s)
                mejor_azar = max(mejor_azar, c[i, j] - cc)
        ctrl[f'{rej[i]:.6f}'] = float(mejor_azar)
        print(f'  [{etiq}] control azar en {rej[i]:.6f}: baja {mejor_azar:.4f}', flush=True)
    pasa = bool(mejoras[-1] < TOL_BARRIDO and max(ctrl.values()) < TOL_CONTROL)
    return dict(chi2=[float(x) for x in tot], chi2_solo_P0=[float(x) for x in c_p0],
                chi2_arranques_fijos=[float(x) for x in c_fijos],
                barridos=len(mejoras), mejora_por_barrido=mejoras,
                control=dict(criterio=f'{N_CONTROL} arranques aleatorios (semilla {SEMILLA_RNG}) en minimo y extremos '
                                      f'no bajan mas de {TOL_CONTROL}; ultimo barrido mejora < {TOL_BARRIDO}',
                             baja_por_punto=ctrl, pasa=pasa))
