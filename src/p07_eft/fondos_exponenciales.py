#!/usr/bin/env python3
"""fondos_exponenciales.py — los tres fondos exponenciales que Paper 7 descarta, con log.

POR QUE (2026-09-30). Paper 7 (§ el potencial no da w_a) cita el w_a del
atractor (-0.093), el lambda calibrado (1.0205) con su w_a (-0.211), el fondo
acoplado (+0.406) y el beta_c del disparo bien normalizado (+0.235068). Los
cuatro salieron de tres scripts que solo IMPRIMEN (fondo_disparo.py,
busca_lambda.py y fondo_acoplado.py, este archivado con el retiro de beta_c el
2026-09-07); ninguno dejo log. Aqui se corren los tres y se guardan.

QUE HACE, sin tocar la fisica de ninguno (los importa y llama a sus funciones):
  atractor  fondo_disparo: alpha del atractor, disparo en phi_i a Omega_DE(a=1).
  lambda    busca_lambda: (phi_i, alpha) tales que Omega_DE y w(a=1) = w0, sin
            acoplamiento; lambda = alpha sqrt(KAL)/sqrt(3).
  acoplado  fondo_acoplado: (phi_i, rho_c,i, beta_c) a Omega_DE, rho_c y
            w_eff(a=1) = w0; el w que ve DESI es w_eff.
  Para cada fondo, ajuste CPL w(a) = w0 + wa (1-a) por minimos cuadrados en
  a = 0.300 .. 0.773 (el rango de DESI DR2: z = 2.330 .. 0.295).
CONTROL (R53): busca_lambda, con el alpha del atractor, tiene que reproducir el
w(a=1) que da fondo_disparo por su propio camino (dos integradores distintos,
el mismo fondo), a < 1e-5; y cada disparo tiene que cumplir sus condiciones
en a=1 a < 1e-8.

Salida: results/logs/fondos_exponenciales.json
"""
import importlib.util
import json
import os
import sys

import numpy as np
from scipy.optimize import brentq, fsolve

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
import ssee_core as S  # noqa: E402
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)   # acta de procedencia: primera linea del log

RUTAS = {"disparo": "src/p07_eft/fondo_disparo.py", "lambda": "src/p07_eft/busca_lambda.py",
         "acoplado": "archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/fondo_acoplado.py"}


def carga(n):
    sp = importlib.util.spec_from_file_location(f"_{n}", os.path.join(_R, RUTAS[n]))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


A_DESI = (1 / (1 + 2.330), 1 / (1 + 0.295))   # ORIGEN-VALOR: z 0.295 y 2.330 — extremos de DESI DR2 BAO (data/raw/desi_dr2_bao.csv)


def cpl(a, w):
    m = (a >= A_DESI[0]) & (a <= A_DESI[1])
    wa, w0 = np.polyfit(1 - a[m], w[m], 1)
    return dict(w0=float(w0), wa=float(wa))


D, L, C = carga("disparo"), carga("lambda"), carga("acoplado")
res = {}

# atractor
phi = brentq(lambda p: D.objetivo([p]), -40.0, 60.0, xtol=1e-13)
r = D.corre(phi, 1e-8)
ode1, w1 = D._en_a1(r)
# El residuo del disparo se mide en SU rejilla (objetivo: 600 puntos hasta
# a=1.05). La primera corrida (2026-10-01) lo midio en la de 3000 hasta a=3 y
# dio 1.3e-5 por interpolar entre rejillas: el control fallo por resolucion, no
# por fisica; el criterio (1e-8) no se toca.
res["atractor"] = dict(alpha=float(D.ALPHA), lam=float(D.LAM), phi_i=float(phi), w_a1=float(w1),
                       residuo_Om_DE=float(D.objetivo([phi])),
                       residuo_Om_DE_rejilla_fina=float(ode1 - D.OM_PHI), cpl=cpl(r["a"], r["w"]))

# lambda calibrado
p = fsolve(L.solo_phi, 0.5, args=(L.ALPHA_ATR,), xtol=1e-12)[0]
w_ctrl = L._en_a1(L.corre(p, L.ALPHA_ATR), "w")
sol = None
for a0 in (0.51, 0.8, 1.2, 2.0, 3.0, 5.0, 0.3):
    for p0 in (0.5, 0.0, 1.0, 2.0):
        u, _, ier, _ = fsolve(L.objetivo, [p0, a0], full_output=True, xtol=1e-13)
        if ier == 1 and max(abs(np.array(L.objetivo(u)))) < 1e-9:
            sol = u
            break
    if sol is not None:
        break
if sol is None:
    sys.exit("busca_lambda: el disparo no converge — no se reporta ningun numero")
r = L.corre(sol[0], sol[1], a_fin=1.05, n=4000)
res["lambda"] = dict(alpha=float(sol[1]), lam=float(sol[1] * np.sqrt(L.KAL) / np.sqrt(3.0)),
                     lam_sobre_atractor=float(sol[1] / L.ALPHA_ATR), phi_i=float(sol[0]),
                     residuos=[float(x) for x in L.objetivo(sol)], cpl=cpl(r["a"], r["w"]))

# acoplado
l0 = np.log(C.OM_C * C.A_I ** -3)
sol = None
for p0 in (1.158, 0.0, 3.0, 8.0, 20.0):
    for b0 in (0.0, -0.5, -1.0, -2.0, -3.9978, -6.0):
        u, _, ier, _ = fsolve(C.objetivo, [p0, l0, b0], full_output=True, xtol=1e-12)
        if ier == 1 and max(abs(np.array(C.objetivo(u)))) < 1e-8:
            sol = u
            break
    if sol is not None:
        break
if sol is None:
    sys.exit("fondo_acoplado: el disparo no converge — no se reporta ningun numero")
r = C.corre(sol[0], np.exp(sol[1]), sol[2])
res["acoplado"] = dict(beta_c=float(sol[2]), phi_i=float(sol[0]),
                       residuos=[float(x) for x in C.objetivo(sol)],
                       cpl_w_eff=cpl(r["a"], r["w_eff"]), cpl_w_phi=cpl(r["a"], r["w_phi"]),
                       beta_c_sobre_bug=float(abs(sol[2]) / 3.989910))   # ORIGEN-VALOR: 3.989910 — beta_c del disparo mal normalizado (Paper 7 viejo, impreso por fondo_acoplado.py)

ctrl = dict(w_a1_busca_lambda=float(w_ctrl), w_a1_fondo_disparo=res["atractor"]["w_a1"],
            dif=float(abs(w_ctrl - res["atractor"]["w_a1"])))
pasa = (ctrl["dif"] < 1e-5 and abs(res["atractor"]["residuo_Om_DE"]) < 1e-8
        and max(map(abs, res["lambda"]["residuos"])) < 1e-8 and max(map(abs, res["acoplado"]["residuos"])) < 1e-8)
out = dict(fecha=str(__import__("datetime").date.today()), a_desi=list(A_DESI), objetivo=dict(w0=S.W0, wa=S.WA),
           fondos=res, control=dict(ctrl, pasa=bool(pasa)))
json.dump(con_acta(out, __file__, entradas=[os.path.join(_R, x) for x in RUTAS.values()]),
          open(os.path.join(_R, "results", "logs", "fondos_exponenciales.json"), "w"), indent=1)
for k, v in res.items():
    print(f"  {k:9s} {json.dumps(v)}")
print(f"  control {ctrl} -> {'PASA' if pasa else 'NO PASA'}")
