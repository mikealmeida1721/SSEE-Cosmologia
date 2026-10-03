"""Pendiente de la identidad w_c = KAL0*w_b*n_s contra Planck crudo (OP-19).

QUE MIDE. Se FUERZA un ingrediente algebraico (n_s o w_b) a valores fuera del
suyo y se deja que Planck elija w_c (junto con logA y tau); el resto del fondo
queda fijo. Si la identidad fuera una relacion que el DATO impone, w_c
seguiria al ingrediente con pendiente d ln w_c / d ln x = +1. Lo que se mide
es la pendiente de la VEROSIMILITUD: forzar un ingrediente saca al modelo de
si mismo, asi que esto no prueba ni refuta la formula; dice si el CMB, por si
solo, la reconoce.

HISTORIA. La corrida original (2026-09-08, commit 01d4369) dejo sus dos logs
(cmb_ns_forzado.json: -0.042; cmb_wb_forzado.json: +0.430) pero su script
nunca entro al repositorio. Este lo re-escribe (2026-10-03, decision de Mike:
un script util que se perdio se re-escribe y se re-mide) con la misma
rejilla, para comparar punto a punto, y anade lo que faltaba:
  - el chi2 de cada punto (el original solo guardo w_c);
  - CONTROL DEL METODO: en el punto algebraico, el w_c que sale tiene que
    reproducir el vertice de results/logs/cmb_perfil_wc.json (perfil de w_c
    con logA y tau minimizados, mismo fondo) dentro de un decimo de su sigma;
  - CONTROL DEL OTRO LADO (R53): el mismo barrido con el fondo de LCDM y sus
    propios ingredientes (lcdm_planck.LCDM_PLANCK, su m_nu). Si las pendientes
    salen del mismo orden, la pendiente la pone la degeneracion del dato, no
    el algebra de SSEE.

USO: python src/p03_cmb/cmb_identidad_forzada.py ns|wb
Nucleos: 2 (SSEE y LCDM en paralelo, 1 hilo cada uno).
"""
# ORIGEN-VALOR: 0.0207 — punto de la rejilla de w_b de la corrida 2026-09-08 (commit 01d4369), conservado para comparar punto a punto

import json
import multiprocessing as mp
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(REPO, 'src'))
sys.path.insert(0, os.path.join(REPO, 'src', 'p11_sondas'))
sys.path.insert(0, AQUI)

import numpy as np  # noqa: E402
from scipy.optimize import minimize  # noqa: E402

import ssee_core as S  # noqa: E402
from lcdm_planck import LCDM_PLANCK as LP, LOGA_PLANCK, TAU_PLANCK  # noqa: E402
from procedencia import con_acta  # noqa: E402

PERFIL = os.path.join(REPO, 'results', 'logs', 'cmb_perfil_wc.json')

# Rejillas de la corrida 2026-09-08; el punto central es el valor algebraico EXACTO
REJ = {
    'ns': [0.80, 0.85, 0.90, S.N_S, 1.00, 1.05, 1.10, 1.15],
    'wb': [0.017, 0.019, 0.0207, S.OMEGA_B_H2, 0.024, 0.026, 0.028, 0.030],
}
FONDOS = {
    'SSEE': dict(ombh2=S.OMEGA_B_H2, H0=S.H0_GLOBAL, ns=S.N_S, w=S.W0, wa=S.WA, mnu=None,
                 wc0=S.OMEGA_C_H2),
    'LCDM': dict(ombh2=LP['ombh2'], H0=LP['H0'], ns=LP['ns'], w=-1.0, wa=0.0, mnu=LP['mnu'],
                 wc0=LP['omch2']),
}


def barrido(args):
    var, nombre = args
    os.environ['OMP_NUM_THREADS'] = '1'
    from cmb_eval import chi2_y_s8
    f = FONDOS[nombre]
    u0 = np.array([f['wc0'], LOGA_PLANCK, TAU_PLANCK])
    filas = []
    # se recorre desde el punto algebraico hacia fuera, con arranque en caliente
    rej = REJ[var]
    ic = 3
    orden = [ic] + list(range(ic + 1, len(rej))) + list(range(ic - 1, -1, -1))
    sol = {}
    for i in orden:
        x = rej[i]
        base = dict(ombh2=f['ombh2'], H0=f['H0'], ns=f['ns'])
        base['ns' if var == 'ns' else 'ombh2'] = x

        def obj(u):
            if not (0.05 < u[0] < 0.25 and 1.5 < u[1] < 4.5 and 0.011 < u[2] < 0.16):
                return 1e9
            return chi2_y_s8(dict(base, omch2=u[0], logA=u[1], tau=u[2]),
                             f['w'], f['wa'], mnu=f['mnu'])[0]
        vecino = sol.get(i - 1 if i > ic else i + 1)
        x0 = np.array(vecino['u']) if vecino else u0
        simp = np.array([x0, x0 + [0.002, 0, 0], x0 + [0, 0.02, 0], x0 + [0, 0, 0.005]])
        r = minimize(obj, x0, method='Nelder-Mead',
                     options=dict(xatol=1e-6, fatol=1e-4, maxiter=1500, initial_simplex=simp))
        sol[i] = dict(x=float(x), u=[float(v) for v in r.x], chi2=float(r.fun),
                      nfev=int(r.nfev), convergio=bool(r.success))
        print(f'[{nombre} {var}] {x:.6f}  w_c={r.x[0]:.6f}  chi2={r.fun:.3f}  '
              f'nfev={r.nfev}  ok={r.success}', flush=True)
    filas = [sol[i] for i in range(len(rej))]
    xs = np.array([s['x'] for s in filas])
    wc = np.array([s['u'][0] for s in filas])
    pend = float(np.polyfit(np.log(xs), np.log(wc), 1)[0])
    return nombre, dict(
        x=xs.tolist(), wc=wc.tolist(), logA=[s['u'][1] for s in filas], tau=[s['u'][2] for s in filas],
        chi2=[s['chi2'] for s in filas], nfev=[s['nfev'] for s in filas],
        convergio=[s['convergio'] for s in filas], pendiente=pend)


if __name__ == '__main__':
    var = sys.argv[1]
    assert var in REJ, 'uso: ns | wb'
    print(f'NÚCLEOS: 2 (SSEE y LCDM en paralelo, OMP_NUM_THREADS=1)', flush=True)
    with mp.get_context('spawn').Pool(2) as pool:
        res = dict(pool.map(barrido, [(var, 'SSEE'), (var, 'LCDM')]))
    ssee, lcdm = res['SSEE'], res['LCDM']
    # control del metodo: el punto algebraico reproduce el vertice del perfil de w_c
    perf = json.load(open(PERFIL))['SSEE']
    d_perf = (ssee['wc'][3] - perf['wc0']) / perf['sigma']
    ctl_metodo = abs(d_perf) < 0.1
    print(f"\nCONTROL METODO: w_c(algebraico) = {ssee['wc'][3]:.6f}  vs perfil "
          f"{perf['wc0']:.6f} ± {perf['sigma']:.6f}  ->  {d_perf:+.3f} sigma  "
          f"{'PASA' if ctl_metodo else 'FALLA'}", flush=True)
    print(f"PENDIENTE d ln w_c / d ln {var}:  SSEE {ssee['pendiente']:+.4f}   "
          f"LCDM (control) {lcdm['pendiente']:+.4f}   identidad +1", flush=True)
    out = dict(
        variable=var,
        # claves de la corrida original, para compararla punto a punto
        **{var: ssee['x'], 'wc': ssee['wc'], 'pendiente': ssee['pendiente']},
        chi2=ssee['chi2'], logA=ssee['logA'], tau=ssee['tau'], convergio=ssee['convergio'],
        prediccion_identidad=1.0,
        control_lcdm=lcdm,
        control_metodo=dict(wc_algebraico=ssee['wc'][3], perfil_wc0=perf['wc0'],
                            perfil_sigma=perf['sigma'], dsigma=d_perf, pasa=ctl_metodo),
        metodo='min chi2 Planck plik_lite TTTEEE+lowT+lowE sobre (w_c, logA, tau), resto del fondo fijo; '
               'pendiente = ajuste lineal de ln w_c contra ln x',
        script='src/p03_cmb/cmb_identidad_forzada.py')
    json.dump(con_acta(out, __file__, entradas=[PERFIL]),
              open(os.path.join(REPO, 'results', 'logs', f'cmb_{var}_forzado.json'), 'w'), indent=1)
    sys.exit(0 if ctl_metodo else 1)
