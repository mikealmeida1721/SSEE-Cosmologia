#!/usr/bin/env python3
"""
El FONDO que de verdad produce el campo de Paper 7 (quinta lectura, 2026-10-11).

POR QUE. P7 afirma que «en el punto del condensado w_phi es constante, así que
la acción da w_a = 0». Para un k-essence SIN potencial la ecuación de
Klein-Gordon es d/dt(a^3 K_X phidot) = 0 (Scherrer 2004): X no se queda en
X_bg, FLUYE hacia X_min (K_X = 0, w = -1). Con K = c1 X + c2 X^2 y
y = X/X_min:
    w = (y-2)/(3y-2),  c_s^2 = (1-y)/(1-3y),  (y-1) sqrt(y) ∝ a^-3.
Y fondo_viscoso.py cerraba con el Lagrangiano de P1 (A X^n, un término), que
da w constante pero c_s^2 = w0 < 0: el que P7 prueba inestable.

QUE SE MIDE.
  A. el campo de P7 solo: w_phi(a), su w_a local y su ajuste CPL en el rango DESI;
  B. el campo de P7 con la presión viscosa de P1 en SU continuidad,
     Pi = -3 Gamma (1-a) rho_DE, Gamma = P_sc/(3 I_g):  w_eff(a), CPL, cruce,
     y si el campo se vuelve fantasma (y < 1 => c_s^2 < 0);
  C. barrido en Gamma: ¿algún Gamma da (w0, wa) a 1 sigma de DESI con y > 1?
CONTROLES (R53).
  1. Gamma = 0: la integración conserva (y-1) sqrt(y) a^3 (Scherrer).
  2. el campo de un término con la misma viscosidad devuelve w_a = -P_sc/I_g
     exacto (la tautología de fondo_viscoso.py: si no la reproduce, este
     integrador no mide lo mismo).
"""
import json
import sys

import numpy as np
from scipy import stats
from scipy.integrate import solve_ivp

sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
import ssee_core as S
from procedencia import cabecera, con_acta  # noqa: E402
print(cabecera(__file__), flush=True)

W0, WA = S.W0, S.WA
PSC = 2 * S.PHI + S.PI
IG = S.PI + PSC
GAMMA = PSC / (3.0 * IG)
OM_DE = 1.0 - S.OMEGA_M_TOTAL
Y0 = (2 * W0 - 2) / (3 * W0 - 1)            # w(y0) = w0
KAP = OM_DE / (Y0 * (1.5 * Y0 - 1))          # rho(y0) = Omega_DE
# DESI DR2 + CMB + Pantheon+ (arXiv:2503.14738 ec. 26), igual que fondo_viscoso.py
DESI = dict(w0=-0.8380, sw0=0.0552, wa=-0.6166, swa=0.2076, rho=-0.894)
LO, HI = 0.300, 0.773


def rho(y):
    return KAP * y * (1.5 * y - 1)


def pres(y):
    return KAP * y * (y / 2 - 1)


def integra(gamma, a_fin=0.25, un_termino=False):
    """Hacia atrás desde hoy. Devuelve a, w_phi, w_eff, y."""
    def f(N, Y):
        a = np.exp(N)
        if un_termino:                       # rho_phi con w = w0 fijo
            r = Y[0]
            return [-3 * (r * (1 + W0) - 3 * gamma * (1 - a) * r)]
        y = Y[0]
        Pi = -3 * gamma * (1 - a) * rho(y)
        return [-3 * (rho(y) + pres(y) + Pi) / (KAP * (3 * y - 1))]
    def rho_nula(N, Y):                      # y -> 2/3: rho_phi -> 0, el campo deja de existir
        return 1.0 if un_termino else Y[0] - 0.70
    rho_nula.terminal = True
    N = np.linspace(0, np.log(a_fin), 2001)
    s = solve_ivp(f, (0, N[-1]), [OM_DE if un_termino else Y0], t_eval=N,
                  method='LSODA', rtol=1e-11, atol=1e-14, events=rho_nula)
    a = np.exp(s.t)
    if un_termino:
        wphi = np.full(a.size, W0)
        weff = W0 - 3 * gamma * (1 - a)
        y = np.full(a.size, np.nan)
    else:
        y = s.y[0]
        wphi = pres(y) / rho(y)
        weff = wphi - 3 * gamma * (1 - a)
    return a, wphi, weff, y


def cpl(a, w):
    m = (a >= LO) & (a <= HI)
    A = np.vstack([np.ones(m.sum()), 1 - a[m]]).T
    c = np.linalg.lstsq(A, w[m], rcond=None)[0]
    return float(c[0]), float(c[1])


def sig_desi(w0f, waf):
    s0, sa, r = DESI['sw0'], DESI['swa'], DESI['rho']
    C = np.array([[s0 ** 2, r * s0 * sa], [r * s0 * sa, sa ** 2]])
    d = np.array([w0f - DESI['w0'], waf - DESI['wa']])
    c2 = float(d @ np.linalg.inv(C) @ d)
    return float(stats.norm.isf(stats.chi2.sf(c2, df=2) / 2))


def cruce(a, w):
    i = np.where(np.diff(np.sign(w + 1)) != 0)[0]
    return None if i.size == 0 else float(1 / a[i[0]] - 1)


if __name__ == '__main__':
    out = dict(y0=Y0, gamma_algebraica=GAMMA, rango_cpl=[LO, HI])

    # control 1
    a, wp, we, y = integra(0.0)
    inv = (y - 1) * np.sqrt(y) * a ** 3
    c1 = float(np.max(np.abs(inv / inv[0] - 1)))
    out['control_scherrer_desv_max'] = c1
    # control 2
    a2, _, we2, _ = integra(GAMMA, un_termino=True)
    w0t, wat = cpl(a2, we2)
    out['control_un_termino'] = dict(w0=w0t, wa=wat, wa_alg=WA,
                                     dif=abs(wat - WA))

    # A. campo solo
    w0A, waA = cpl(a, we)
    h = 1e-4
    aa, wpp, _, _ = integra(0.0, a_fin=1 - h)
    wa_loc = float((wpp[-1] - W0) / h)       # -dw/da en a=1  (w(1-h) - w(1))/h
    tab = {f'a{round(100*x):03d}': float(np.interp(x, a[::-1], wp[::-1]))
           for x in (0.3, 0.5, 0.7, 0.9, 1.0)}
    out['A_campo_solo'] = dict(w_phi=tab, wa_local=wa_loc,
                               cpl=dict(w0=w0A, wa=waA),
                               sigma_desi=sig_desi(w0A, waA))

    # B. campo + viscosidad algebraica
    aB, wpB, weB, yB = integra(GAMMA)
    w0B, waB = cpl(aB, weB)
    m = aB >= LO
    out['B_campo_mas_viscosidad'] = dict(
        cpl=dict(w0=w0B, wa=waB), sigma_desi=sig_desi(w0B, waB),
        z_cruce=cruce(aB, weB), y_min=float(yB[m].min()),
        campo_fantasma=bool(yB[m].min() < 1),
        a_campo_fantasma=(float(aB[m][yB[m] < 1].max())
                          if (yB[m] < 1).any() else None))

    # C. barrido en Gamma
    filas = []
    for g in np.linspace(0, 1.0, 101):
        ag, _, wg, yg = integra(g)
        if not np.all(np.isfinite(yg)) or ag[-1] > LO + 1e-9:
            filas.append(dict(gamma=float(g), corta_en_a=float(ag[-1])))
            continue
        w0g, wag = cpl(ag, wg)
        mg = ag >= LO
        filas.append(dict(gamma=float(g), w0=w0g, wa=wag,
                          sigma=sig_desi(w0g, wag),
                          y_min=float(yg[mg].min())))
    sanas = [f for f in filas if 'sigma' in f]
    ok = [f for f in sanas if f['sigma'] < 1 and f['y_min'] > 1]
    out['C_barrido'] = dict(n=len(filas), n_campo_muere=len(filas) - len(sanas),
                            gamma_max=1.0,
                            mejor=min(sanas, key=lambda f: f['sigma']),
                            mejor_estable=(min([f for f in sanas if f['y_min'] > 1],
                                               key=lambda f: f['sigma'])
                                           if any(f['y_min'] > 1 for f in sanas) else None),
                            n_ok_1sigma_y_estable=len(ok))

    print(json.dumps(out, indent=1))
    assert c1 < 1e-7, 'control Scherrer falla'
    assert abs(wat - WA) < 1e-8, 'control de un término falla'
    with open('results/logs/p7_fondo_campo.json', 'w') as fh:
        json.dump(con_acta(out, __file__), fh, indent=1, ensure_ascii=False)
