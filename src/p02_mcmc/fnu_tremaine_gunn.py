#!/usr/bin/env python3
"""fnu_tremaine_gunn.py — rehace la cuenta de f_nu que el Paper I de abril dice haber hecho.

POR QUE (2026-10-01). La formula de cumulos de Paper 2,
    M_dyn = M_bar^IGIMF * KAL0 * (1 + f_nu),   f_nu = 0.020,
viene del Paper I del 2026-04-20 (Zenodo, SSEE_V3.6.pdf, §3.2 «Neutrino
Bridge»). Alli f_nu se define como «la fraccion de masa de neutrinos reliquia
ATRAPADOS» en el cumulo, y se dice que sale de integrar la distribucion de
Fermi-Dirac (Tremaine & Gunn 1979) con Sum m_nu = 0.085 eV y velocidad de
escape v_esc ~ 2000 km/s, dando 0.018-0.022. Ningun script del repo hacia esa
integral: el 0.020 entro tecleado. Aqui se hace.

LA CUENTA. Un neutrino queda atrapado si su velocidad es menor que v_esc, es
decir si su momento es p < p_max = m v_esc / c. Por Liouville la ocupacion
del espacio de fases no puede crecer por encima de la primordial, asi que la
densidad atrapada esta acotada por:
  (a) «lentos a densidad cosmica»: todos los neutrinos con p < p_max, a la
      densidad media del universo (lo que da la integral de Fermi-Dirac);
  (b) techo de Tremaine-Gunn: la esfera p < p_max llena con la ocupacion
      maxima primordial, 1/2 por estado (cota dura, no alcanzable).
La fraccion de masa del cumulo es rho_nu,atrapada / rho_cumulo, con
rho_cumulo = 500 rho_crit (las masas de la tabla de abril son dentro de R500).

CONTROLES (R53):
  1. de lectura: la densidad cosmica de neutrinos calculada aqui (desacople
     instantaneo) debe coincidir con la convencion independiente del nucleo,
     omega_nu = Sum m_nu / 93.14, dentro del 1.5 % que separa el desacople
     instantaneo (94.1) del suave (93.14); y la densidad numerica por sabor
     debe dar los ~112 /cm^3 del libro. (El Paper I cita 28.6 eV/cm^3 para
     0.085 eV: es 336/cm^3, los TRES sabores, por la SUMA de masas, o sea la
     masa contada tres veces. Se registra, no se usa de control.)
  2. del otro lado: el mismo codigo con un neutrino pesado de 11 eV (el esteril
     que Angus 2009 propone para MOND en cumulos) tiene que dar una fraccion
     grande. Si el metodo diera siempre ~0, no distinguiria nada.

Salida: results/logs/fnu_tremaine_gunn.json
"""
import json
import os
import sys

import numpy as np
from scipy import constants as C
from scipy import integrate, optimize
from scipy.special import zeta

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
import ssee_core as S  # noqa: E402
from procedencia import cabecera, con_acta  # noqa: E402

print(cabecera(__file__), flush=True)

T_CMB = 2.7255          # ORIGEN-VALOR: 2.7255 — K, Fixsen 2009 (ApJ 707, 916)
V_ESC = 2000.0          # ORIGEN-VALOR: 2000.0 — km/s, v_esc del cumulo que usa el Paper I de abril (§3.2)
SUM_ABRIL = 0.085       # ORIGEN-VALOR: 0.085 — eV, Sum m_nu que usa el Paper I de abril (§3.2)
RHO_ABRIL = 28.6        # ORIGEN-VALOR: 28.6 — eV/cm^3, densidad cosmica de neutrinos que cita el Paper I de abril
F_NU_P2 = 0.020         # ORIGEN-VALOR: 0.020 — f_nu que usa Paper 2 (punto medio de 0.018-0.022 del Paper I)
DELTA = 500.0           # ORIGEN-VALOR: 500.0 — sobredensidad de R500, donde el Paper I da sus masas
DM21 = 7.42e-5          # ORIGEN-VALOR: 7.42e-5 — eV^2, NuFIT 5.2 (2022), Delta m^2_21
DM31 = 2.515e-3         # ORIGEN-VALOR: 2.515e-3 — eV^2, NuFIT 5.2 (2022), Delta m^2_31 ordenamiento normal
M_ESTERIL = 11.0        # ORIGEN-VALOR: 11.0 — eV, neutrino esteril de Angus 2009 (MNRAS 394, 527) para cumulos MOND

kT = C.k * T_CMB * (4.0 / 11.0) ** (1.0 / 3.0) / C.e          # T_nu hoy, en eV
L3 = (C.k * T_CMB * (4.0 / 11.0) ** (1.0 / 3.0) / (C.hbar * C.c * 100.0)) ** 3   # (kT/hbar c)^3 en cm^-3
FD = lambda x: x * x / (np.exp(x) + 1.0)
I_TOT = 1.5 * zeta(3)                                          # int_0^inf x^2/(e^x+1)
N_SABOR = 2.0 / (2.0 * np.pi ** 2) * I_TOT * L3                # nu + nubar, una helicidad cada uno
h = S.H0_GLOBAL / 100.0
RHO_CRIT = 3.0 * (S.H0_GLOBAL * 1e3 / (C.parsec * 1e6)) ** 2 / (8 * np.pi * C.G) * C.c ** 2 / C.e / 1e6   # eV/cm^3
RHO_CUM = DELTA * RHO_CRIT


def masas(suma, orden):
    if orden == "degeneradas":
        return [suma / 3.0] * 3
    m1 = optimize.brentq(lambda m: m + np.sqrt(m * m + DM21) + np.sqrt(m * m + DM31) - suma, 0.0, suma)
    return [m1, np.sqrt(m1 * m1 + DM21), np.sqrt(m1 * m1 + DM31)]


def atrapados(m):
    """densidad de masa atrapada [eV/cm^3] de un sabor de masa m (eV): (a) lentos cosmicos, (b) techo TG."""
    xmax = m * (V_ESC * 1e3 / C.c) / kT
    lentos = 2.0 / (2.0 * np.pi ** 2) * integrate.quad(FD, 0.0, xmax)[0] * L3 * m
    techo = 2.0 / (2.0 * np.pi ** 2) * 0.5 * xmax ** 3 / 3.0 * L3 * m
    return lentos, techo, xmax


def caso(suma, orden):
    ms = masas(suma, orden)
    a = [atrapados(m) for m in ms]
    lentos, techo = sum(x[0] for x in a), sum(x[1] for x in a)
    return dict(sum_mnu=suma, orden=orden, masas_eV=ms, p_max_sobre_T=[x[2] for x in a],
                rho_cosmica=N_SABOR * suma, rho_lentos=lentos, rho_techo_TG=techo,
                f_nu_lentos=lentos / RHO_CUM, f_nu_techo_TG=techo / RHO_CUM,
                f_nu_si_todo_el_fondo=N_SABOR * suma / RHO_CUM,
                veces_bajo_0020_techo=F_NU_P2 / (techo / RHO_CUM))


res = {k: caso(*v) for k, v in dict(nucleo_degeneradas=(S.SUM_MNU_EV, "degeneradas"),
                                    nucleo_normal=(S.SUM_MNU_EV, "normal"),
                                    abril_degeneradas=(SUM_ABRIL, "degeneradas"),
                                    abril_normal=(SUM_ABRIL, "normal")).items()}
for k, r in res.items():
    print(f"  {k:20s} f_nu lentos {r['f_nu_lentos']:.3e}  techo TG {r['f_nu_techo_TG']:.3e}  "
          f"(todo el fondo {r['f_nu_si_todo_el_fondo']:.3e})  -> 0.020 es {r['veces_bajo_0020_techo']:.2e} veces el techo")

# controles
rho_conv = S.SUM_MNU_EV / 93.14 * RHO_CRIT / h ** 2   # omega_nu * rho_crit/h^2, convencion del nucleo
c1 = dict(rho_cosmica_aqui=N_SABOR * S.SUM_MNU_EV, rho_cosmica_convencion_nucleo=rho_conv,
          desvio_rel=N_SABOR * S.SUM_MNU_EV / rho_conv - 1.0, n_por_sabor_cm3=N_SABOR,
          pasa=bool(abs(N_SABOR * S.SUM_MNU_EV / rho_conv - 1.0) < 0.015 and 110 < N_SABOR < 114))
abril = dict(cita_eV_cm3=RHO_ABRIL, correcto_eV_cm3=N_SABOR * SUM_ABRIL, cociente=RHO_ABRIL / (N_SABOR * SUM_ABRIL),
             causa="336/cm^3 (tres sabores) por la SUMA de masas: masa contada tres veces")
lento_s, techo_s, x_s = atrapados(M_ESTERIL)
c2 = dict(m_eV=M_ESTERIL, p_max_sobre_T=x_s, f_lentos=lento_s / RHO_CUM, f_techo_TG=techo_s / RHO_CUM,
          criterio="con un esteril de 11 eV el techo TG debe superar el 0.020; si no, el metodo no distingue",
          pasa=bool(techo_s / RHO_CUM > F_NU_P2))
print(f"  control lectura: rho_nu {c1['rho_cosmica_aqui']:.4f} vs convencion {rho_conv:.4f} eV/cm3 "
      f"({c1['desvio_rel']:+.4f}), n/sabor {N_SABOR:.1f} /cm3 -> {'PASA' if c1['pasa'] else 'NO PASA'}")
print(f"  abril citaba {RHO_ABRIL} eV/cm3 para 0.085 eV; correcto {abril['correcto_eV_cm3']:.2f} (x{abril['cociente']:.3f})")
print(f"  control otro lado: esteril 11 eV, techo TG {c2['f_techo_TG']:.3g} -> {'PASA' if c2['pasa'] else 'NO PASA'}")
if not (c1["pasa"] and c2["pasa"]):
    sys.exit("un control no pasa: no se escribe")

out = dict(fecha=str(__import__("datetime").date.today()),
           que="f_nu de la formula de cumulos, rehecho con el metodo que declara el Paper I de abril (§3.2)",
           T_nu_eV=kT, rho_crit_eV_cm3=RHO_CRIT, rho_cumulo_eV_cm3=RHO_CUM, v_esc_km_s=V_ESC, delta=DELTA,
           f_nu_paper2=F_NU_P2, casos=res, rho_nu_abril=abril, control_lectura=c1, control_otro_lado=c2)
json.dump(con_acta(out, __file__), open(os.path.join(_R, "results", "logs", "fnu_tremaine_gunn.json"), "w"), indent=1)
print("  escrito -> results/logs/fnu_tremaine_gunn.json")
