#!/usr/bin/env python3
"""barrido_M4.py — qué mide (y qué no) la cascada de Hubble sobre el corte M (Paper 10).

POR QUE (2026-10-12, quinta lectura de P10). Paper 10 tecleaba a mano tres cifras
sin log: «variar M⁴ en [0.2, ∞)×45α²ρ_c mueve la salida a lo sumo 0.57 km/s/Mpc»,
«+1 % en KAL se compensa con +2.01 % en M⁴» (las dos están en OP-3 como medidas de
sesión) y el criterio «si LiteBIRD mide r_obs y la salida difiere de SH0ES en más
de 1σ, la extensión UV cae», que nunca se evaluó. Este script las calcula.

QUE SE MIDE. Con la misma fórmula que ssee_core (S_K_FULL = S_K + 24 X²/M⁴, X la
raíz física de la cuadrática de fondo, unidades ρ_c = 1):
  1. H_glob(M⁴) = H_SH0ES (1 − s_K^full/(3 MIRA)) para M⁴ = f × 45α², f ∈ [0.1, ∞);
  2. el f más chico cuya salida queda a 1σ (σ propagado de SH0ES) de 3(φ+π)²;
     como M⁴ ∝ α², eso fija el α — y el r = 12α/N² — por debajo del cual la
     pata de Hubble del test cruzado empieza a votar;
  3. la degeneración: cuánto M⁴ compensa un +1 % en KAL (s_K^full igual);
  4. cifras del fondo que P10 imprime: X_bg UV/IR, u = X/M⁴, c_s² del funcional,
     y ρ_c^(1/4) en meV.

CONTROL (R53). Con f = 1 y KAL sin tocar, el barrido tiene que devolver
H0_GLOBAL de ssee_core a 1e-10; si no, no calcula la misma cascada.
"""
import json
import math
import os
import sys

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
import ssee_core as S  # noqa: E402
from procedencia import cabecera, con_acta  # noqa: E402
print(cabecera(__file__), flush=True)

H_SH0ES, SIG_SH0ES = S.H0_SH0ES, S.SIG_H0_SH0ES
M4_NOM = 45.0 * S.ALPHA_ATT ** 2


def x_bg(m4, kal):
    """raíz física de 4X²/M⁴ + 2X/KAL − s_K/3 = 0 (ρ_c = 1); M⁴ = inf da el IR."""
    if math.isinf(m4):
        return S.S_K * kal / 6.0
    return (-2.0 / kal + (4.0 / kal ** 2 + 16.0 * (S.S_K / 3.0) / m4) ** 0.5) / (8.0 / m4)


def s_k_full(m4, kal=S.KAL0):
    return S.S_K if math.isinf(m4) else S.S_K + 24.0 * x_bg(m4, kal) ** 2 / m4


def h_glob(m4, kal=S.KAL0):
    return H_SH0ES * (1.0 - s_k_full(m4, kal) / (3.0 * S.MIRA))


sig = SIG_SH0ES * (1.0 - S.F_SCREEN)

# 1. barrido
fs = [0.1, 0.2, 0.5, 1.0, 2.0, 10.0, math.inf]
barrido = {("inf" if math.isinf(f) else f"{f:g}"): h_glob(f * M4_NOM) for f in fs}
h_nom = h_glob(M4_NOM)
mueve_02_inf = max(abs(h_glob(f * M4_NOM) - h_nom) for f in (0.2, math.inf))
desde_IR = h_glob(0.2 * M4_NOM) - h_glob(math.inf)

# 2. f a 1σ del número puro (bisección en log f; la salida baja al bajar f)
lo, hi = 1e-4, 1.0
for _ in range(200):
    mid = math.sqrt(lo * hi)
    if abs(h_glob(mid * M4_NOM) - S.H0_ALG) > sig:
        lo = mid
    else:
        hi = mid
f_1sig = hi
alfa_fac = math.sqrt(f_1sig)                 # M⁴ ∝ α²
r_nom = 12.0 * S.ALPHA_ATT / (2.0 * S.PHI ** 7) ** 2
r_umbral = r_nom * alfa_fac

# 3. degeneración: +1 % KAL, buscar M⁴ con el mismo s_K^full
obj = s_k_full(M4_NOM)
lo, hi = M4_NOM, 2.0 * M4_NOM
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if s_k_full(mid, 1.01 * S.KAL0) > obj:
        lo = mid
    else:
        hi = mid
dM4_pct = 100.0 * (0.5 * (lo + hi) / M4_NOM - 1.0)

# 4. cifras del fondo
X_uv, X_ir = x_bg(M4_NOM, S.KAL0), x_bg(math.inf, S.KAL0)
u_bg = X_uv / M4_NOM
cs2_func = (1.0 / S.KAL0 + 2.0 * u_bg) / (1.0 / S.KAL0 + 6.0 * u_bg)
eps = X_uv ** 2 / M4_NOM
H_eV = S.H0_GLOBAL * 1e3 / 3.0856775814913673e22 * 6.582119569e-16   # ORIGEN-VALOR: 1 Mpc (IAU 2015) y hbar (CODATA 2018)
rhoc14_meV = 1e3 * (3.0 * H_eV ** 2 * 2.435323e27 ** 2) ** 0.25        # ORIGEN-VALOR: masa de Planck reducida, CODATA 2018

control = dict(H_f1=h_nom, H0_GLOBAL=S.H0_GLOBAL, dif=abs(h_nom - S.H0_GLOBAL))
pasa = control["dif"] < 1e-10
out = dict(
    barrido_H_glob=barrido, sigma_prop=sig,
    mueve_max_02_inf=mueve_02_inf, rango_02_inf=desde_IR,
    f_a_1sigma=f_1sig, alfa_factor_1sigma=alfa_fac, r_nominal=r_nom, r_umbral_1sigma=r_umbral,
    degeneracion_dM4_pct_por_1pct_KAL=dM4_pct,
    X_UV_sobre_IR=X_uv / X_ir, X_reduccion_pct=100.0 * (1.0 - X_uv / X_ir),
    u_bg=u_bg, cs2_funcional=cs2_func, eps=eps, rhoc14_meV=rhoc14_meV,
    control=dict(criterio="f = 1 reproduce H0_GLOBAL de ssee_core a 1e-10", **control, pasa=pasa))
print(json.dumps({k: v for k, v in out.items() if k != "barrido_H_glob"}, indent=1))
assert pasa, "CONTROL NO PASA: el barrido no calcula la cascada de ssee_core"
with open(os.path.join(_R, "results", "logs", "p10_barrido_M4.json"), "w") as fh:
    json.dump(con_acta(out, __file__, entradas=[]), fh, indent=1, ensure_ascii=False)
