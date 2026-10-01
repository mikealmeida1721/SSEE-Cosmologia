#!/usr/bin/env python3
"""hiclass_campo.py — la corrida hi_class del sector campo de Paper 7, con log.

POR QUE (2026-09-30). Paper 7 cita los numeros de hi_class (alpha_K, Omega_smg,
sigma8 con x_k = 1 y 100, el efecto en TT, el c_s^2 negativo de los controles,
el fluido CLP) copiados del README de src/p07_eft/hiclass/, que no es un log:
las corridas del 2026-09-06 se hicieron a mano en la terminal. Este script las
rehace todas desde ssee_core y escribe results/logs/hiclass_campo.json.

QUE CORRE (binario /mnt/datos/hi_class/class, v3.0, un nucleo cada vez):
  1. campo: propto_omega con x_k = 3(5-3w0), fondo w = w0 constante (el w del
     campo). Lee alpha_K(z=0), c_s^2(z=0), Omega_smg y Omega_m del presupuesto.
  2. sigma8 y TT con x_k = 1, x_k del modelo y 100 (efecto de alpha_K).
  3. controles de estabilidad: x_k del modelo con w_a, con LCDM, x_k = 0 y 1
     con w_a. Lee si hi_class acepta y el c_s^2 minimo que reporta.
  4. fluido CLP (CLASS sin campo) con el fondo w0 w_a y c_s^2 = 1, el del
     modelo y 0: sigma8 y TT.
Recetas de la sesion del 2026-09-06: P_k_max = 1 h/Mpc para sigma8 (la que da
hi_class con fourier_verbose); TT referida a x_k = 1 en el paso 2 y a c_s^2 = 1
en el 4.

DOS JUEGOS DE ENTRADAS:
  - "canonico": h, omega_b, omega_c, Sigma m_nu, w0, w_a, x_k y c_s^2 del nucleo.
  - "historico": los mismos pero con omega_b y omega_c a 5 decimales, que es
    como se corrio el 2026-09-06 (ver HISTORICO abajo).
CONTROL (R53): el juego historico tiene que reproducir los numeros que Paper 7
imprime hoy (sigma8 de x_k = 1 y 100, sigma8 del CLP). Si no los reproduce, el
script no sabe rehacer la corrida vieja y su canonico no vale como reemplazo.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
import ssee_core as S  # noqa: E402
from procedencia import con_acta  # noqa: E402

CLASS = "/mnt/datos/hi_class/class"
DIR = "/mnt/datos/SSEE_data/hiclass_campo"
XK = 3 * (5 - 3 * S.W0)
CS2 = (1 + S.W0) / (5 - 3 * S.W0)
# Neutrinos como los pone CLASS para 1 masivo + N_eff = 3.044:
N_UR = 2.0328      # ORIGEN-VALOR: 2.0328 — N_ur de CLASS con 1 ncdm y N_eff = 3.044 (explanatory.ini)
T_NCDM = 0.71611   # ORIGEN-VALOR: 0.71611 — T_ncdm de CLASS que da m/omega = 93.14 eV (explanatory.ini)
N_UR_SIN_NCDM = 3.044  # ORIGEN-VALOR: 3.044 — N_eff estandar, el fluido CLP se corrio sin neutrino masivo
PKMAX = 1.0        # ORIGEN-VALOR: 1.0 — P_k_max_h/Mpc de la receta del 2026-09-06 (sigma8 de hi_class)
ELLS = (2, 5, 10, 30)
HISTORICO = dict(omega_b=0.02242, omega_cdm=0.11951)  # ORIGEN-VALOR: 0.02242, 0.11951 — el ini del 2026-09-06 (ssee_ak.ini), a 5 decimales
CANONICO = dict(omega_b=S.OMEGA_B_H2, omega_cdm=S.OMEGA_C_H2)


def corre(nombre, p):
    ini = os.path.join(DIR, nombre + ".ini")
    p = dict(p, root=os.path.join(DIR, nombre + "_"), overwrite_root="yes")
    with open(ini, "w") as f:
        f.write("\n".join(f"{k} = {v}" for k, v in p.items()) + "\n")
    r = subprocess.run([CLASS, ini], capture_output=True, text=True,
                       env=dict(os.environ, OMP_NUM_THREADS="1"))
    txt = r.stdout + r.stderr
    s8 = re.search(r"sigma8=([0-9.]+) for total matter", txt)
    cs = re.search(r"minimum c_s\^2=(-?(?:inf|nan|[0-9][-0-9.e+]*))", txt)
    ac = re.search(r"minimum c_s\^2=[-0-9.e+]+ at a=([-0-9.e+]+)", txt)
    rech = r.returncode != 0 or "nstabilit" in txt
    return dict(ini=ini, rc=r.returncode, rechaza=bool(rech),
                sigma8=float(s8.group(1)) if s8 else None,
                cs2_min=(float(cs.group(1)) if cs.group(1)[-1].isdigit() else cs.group(1)) if cs else None,
                z_cs2_min=1 / float(ac.group(1)) - 1 if ac else None,
                mensaje=[l for l in txt.splitlines() if "rror" in l or "nstab" in l][:3], txt=txt)


def cl_tt(nombre):
    d = np.loadtxt(os.path.join(DIR, nombre + "__cl.dat"))
    return {int(L): float(v) for L, v in zip(d[:, 0], d[:, 1])}


def base(ent, mnu=True):
    p = dict(h=S.H0_GLOBAL / 100, **{k: repr(float(v)) for k, v in ent.items()})
    if mnu:
        p.update(N_ur=N_UR, N_ncdm=1, m_ncdm=S.SUM_MNU_EV, T_ncdm=T_NCDM)
    else:
        p.update(N_ur=N_UR_SIN_NCDM)
    return p


def campo(ent, xk, exp_model, exp_par, output, extra=None):
    p = base(ent)
    p.update(output=output, Omega_Lambda=0, Omega_fld=0, Omega_smg=-1,
             gravity_model="propto_omega", parameters_smg=f"{xk!r}, 0., 0., 0., 1.",
             expansion_model=exp_model, expansion_smg=exp_par,
             skip_stability_tests_smg="no", method_qs_smg="fully_dynamic",
             output_background_smg=1, background_verbose=2, fourier_verbose=1)
    p.update(extra or {})
    return p


def juego(tag, ent):
    out = {}
    w_campo = f"0.5, {S.W0!r}, 0.0"
    w_cpl = f"0.5, {S.W0!r}, {S.WA!r}"
    # 1. campo
    r = corre(f"{tag}_campo", campo(ent, XK, "wowa", w_campo, "mPk", {"write background": "yes"}))
    bg = os.path.join(DIR, f"{tag}_campo__background.dat")
    hdr = open(bg).read().split("\n")[3]
    cols = {m.group(2): int(m.group(1)) - 1 for m in re.finditer(r"(\d+):([^\s]+)", hdr)}
    a = np.loadtxt(bg)
    z0 = a[np.argmin(a[:, cols["z"]])]
    om = {m.group(1).strip(): float(m.group(2)) for m in
          re.finditer(r"-> ?([A-Za-z][A-Za-z \-]+?)\s+Omega = ([0-9.e+-]+)", r["txt"])}
    out["campo"] = dict(rechaza=r["rechaza"], alpha_K_z0=float(z0[cols["kineticity_smg"]]),
                        cs2_z0=float(z0[cols["c_s^2"]]),
                        Omega_smg=om.get("Scalar Modified Gravity"),
                        Omega_m_presupuesto=om.get("Non-relativistic"))
    # 2. sigma8 y TT contra x_k
    s8, tt = {}, {}
    for nom, xk in (("1", 1.0), ("modelo", XK), ("100", 100.0)):
        n = f"{tag}_xk{nom}"
        s8[nom] = corre(n, campo(ent, xk, "wowa", w_campo, "mPk",
                                 {"P_k_max_h/Mpc": PKMAX}))["sigma8"]
        corre(n + "t", campo(ent, xk, "wowa", w_campo, "tCl"))
        tt[nom] = cl_tt(n + "t")
    out["alpha_K_sigma8"] = s8
    out["alpha_K_sigma8_cambio_rel"] = (s8["100"] - s8["1"]) / s8["1"]
    out["alpha_K_TT_rel"] = {nom: {L: (tt[nom][L] - tt["1"][L]) / tt["1"][L] for L in ELLS}
                             for nom in ("modelo", "100")}
    # 3. controles de estabilidad
    ctl = {}
    for nom, xk, em, ep in (("xk_modelo_wa", XK, "wowa", w_cpl),
                            ("xk_modelo_wa0", XK, "wowa", w_campo),
                            ("xk_modelo_lcdm", XK, "lcdm", "0.5"),
                            ("xk0_wa", 0.0, "wowa", w_cpl),
                            ("xk1_wa", 1.0, "wowa", w_cpl)):
        r = corre(f"{tag}_ctl_{nom}", campo(ent, xk, em, ep, "mPk"))
        ctl[nom] = {k: r[k] for k in ("rechaza", "cs2_min", "z_cs2_min", "mensaje")}
    out["controles"] = ctl
    # 4. fluido CLP, c_s^2
    s8c, ttc = {}, {}
    for nom, cs in (("1", 1.0), ("modelo", CS2), ("0", 0.0)):
        p = base(ent, mnu=False)
        p.update(output="tCl,mPk", Omega_Lambda=0, Omega_smg=0,
                 fluid_equation_of_state="CLP", w0_fld=repr(S.W0), wa_fld=repr(S.WA),
                 cs2_fld=repr(cs), **{"P_k_max_h/Mpc": PKMAX}, fourier_verbose=1)
        s8c[nom] = corre(f"{tag}_clp{nom}", p)["sigma8"]
        ttc[nom] = cl_tt(f"{tag}_clp{nom}")
    out["cs2_sigma8"] = s8c
    out["cs2_sigma8_cambio_rel"] = (s8c["modelo"] - s8c["1"]) / s8c["1"]
    out["cs2_TT_rel"] = {nom: {L: (ttc[nom][L] - ttc["1"][L]) / ttc["1"][L] for L in ELLS}
                         for nom in ("modelo", "0")}
    return out


os.makedirs(DIR, exist_ok=True)
pred = dict(x_k=XK, cs2=CS2, alpha_K_z0=XK * (1 - S.OMEGA_M_TOTAL),
            var_cosmica={L: (2 / (2 * L + 1)) ** 0.5 for L in ELLS})
can = juego("can", CANONICO)
his = juego("his", HISTORICO)
# CONTROL R53: lo que Paper 7 imprime hoy, copiado del README del 2026-09-06
PAPER = {"sigma8_xk1": 0.769916, "sigma8_xk100": 0.769973,   # ORIGEN-VALOR: los sigma8 que imprime Paper 7 L572-573 (blanco del control, no un resultado)
         "sigma8_clp1": 0.828445, "sigma8_clp_modelo": 0.828453}  # ORIGEN-VALOR: Paper 7 L742-743 (blanco del control)
rep = {"sigma8_xk1": his["alpha_K_sigma8"]["1"], "sigma8_xk100": his["alpha_K_sigma8"]["100"],
       "sigma8_clp1": his["cs2_sigma8"]["1"], "sigma8_clp_modelo": his["cs2_sigma8"]["modelo"]}
pasa = all(rep[k] is not None and abs(rep[k] - v) < 5e-7 for k, v in PAPER.items())
can["campo"]["alpha_K_dif_rel"] = can["campo"]["alpha_K_z0"] / pred["alpha_K_z0"] - 1
can["campo"]["cs2_dif_rel"] = can["campo"]["cs2_z0"] / CS2 - 1
out = dict(fecha=str(__import__("datetime").date.today()), prediccion=pred,
           canonico=can, historico=his,
           control=dict(historico_reproduce_paper=dict(paper=PAPER, rehecho=rep), pasa=pasa))
json.dump(con_acta(out, __file__, entradas=[CLASS]),
          open(os.path.join(_R, "results", "logs", "hiclass_campo.json"), "w"), indent=1)
c = can["campo"]
print(f"  campo: alpha_K {c['alpha_K_z0']:.6f} (pred {pred['alpha_K_z0']:.6f}, {100*c['alpha_K_dif_rel']:+.4f}%)"
      f"  cs2 {c['cs2_z0']:.8f}  Omega_smg {c['Omega_smg']}  Omega_m {c['Omega_m_presupuesto']}  rechaza {c['rechaza']}")
for t, j in (("canonico", can), ("historico", his)):
    print(f"  {t}: sigma8 x_k {j['alpha_K_sigma8']}  CLP {j['cs2_sigma8']}")
    print(f"     TT alpha_K {j['alpha_K_TT_rel']}\n     TT cs2 {j['cs2_TT_rel']}")
    print(f"     controles { {k: (v['rechaza'], v['cs2_min'], v['z_cs2_min']) for k, v in j['controles'].items()} }")
print(f"  control historico vs paper: {'PASA' if pasa else 'NO PASA'} {rep}")
