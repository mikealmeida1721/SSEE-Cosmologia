#!/usr/bin/env python3
"""algebra_derivada.py — el ALGEBRA que los papers imprimen y el nucleo no nombra.

POR QUE (2026-09-30). Los papers escriben combinaciones de phi y pi (2 phi^7,
phi^-10, sqrt(AURA), 3 Omega_DE (5 - 3 w0), ...) a mano. Tienen fuente —el
algebra—, pero nada las calculaba en un sitio que alguien pudiera abrir, y a
mano se cuelan errores: al armar esta tabla salieron mal la ultima cifra de
sqrt(AURA) en Paper 8, dos celdas de la tabla de Paper 4 (pi+KAL y
phi+pi+KAL) y alpha_K en 22 sitios (calculado con el H viejo: Omega_m =
omega_m / h^2 y h cambio el 09-28). Los valores buenos estan en el log; los
malos, en migra_a_val.CORRIGE.

Cada entrada: nombre, formula sobre ssee_core y para que se usa. Este script
evalua todas y escribe results/logs/algebra_derivada.json (con acta); los
papers las imprimen con \\val{nombre} via manuscript/valores.yaml.

CONTROL (R53): las identidades que el algebra exige (u por sus dos formas
cerradas, AURA = 2 MIRA, n por sus dos formas) tienen que cumplirse a 1e-12; y
una entrada con formula rota (division por cero) tiene que fallar ruidosa.
"""
import json
import math
import os
import sys

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(_R, "src"))
import ssee_core as S  # noqa: E402
from procedencia import con_acta  # noqa: E402

N = {k: getattr(S, k) for k in dir(S) if k.isupper()}
N["math"] = math
N["OMDE_DENS"] = 1.0 - S.OMEGA_M_TOTAL      # Omega_DE como DENSIDAD (no la saturacion S_DE)

ALGEBRA = {
    # nombre: (formula, uso)
    "alpha_K_z0":     ("3*OMDE_DENS*(5-3*W0)", "kineticidad hoy, Paper 7 y resumenes"),
    "x_K":            ("3*(5-3*W0)", "alpha_K(a) = x_K Omega_DE(a), Paper 7"),
    "r_tensor":       ("PHI**-10", "tensor-escalar r = phi^-10"),
    "r_tensor_mil":   ("1e3*PHI**-10", "r en unidades de 10^-3 (como lo escriben los papers)"),
    "r_staro":        ("3/PHI**14", "r de Starobinsky con N = 2 phi^7"),
    "dos_phi6":       ("2*PHI**6", "ventana de e-folds, Paper 1"),
    "dos_phi7":       ("2*PHI**7", "N_* = 2 phi^7"),
    "dos_phi8":       ("2*PHI**8", "ventana de e-folds, Paper 1"),
    "sqrt_AURA":      ("math.sqrt(AURA)", "deflexion del limite MOND-like, Paper 8"),
    "cuatro_AURA":    ("4*AURA", "CUARTAL, tabla de Paper 7"),
    "inv_phi":        ("1/PHI", "gamma algebraico = phi^-1"),
    "dos_AURA":       ("2*AURA", "DUAL, tabla de Paper 7"),
    "tres_MIRA":      ("3*MIRA", "3 MIRA = 3 AURA/2, Paper 9"),
    "sqrtAURA_MIRA":  ("math.sqrt(AURA)/MIRA", "sqrt(beta_c)/MIRA con beta_c = AURA, Paper 8"),
    "seis_alfa_KAL2": ("6*ALPHA_ATT*KAL0**2", "M^4 de la Ruta A en rho_crit, Paper 10"),
    "X_UV_sobre_IR":  ("_X_UV/(S_K*KAL0/6)", "X_bg UV / IR, Paper 10"),
    "c2X_c1_KX":      ("_X_UV*KAL0/_M4_UV", "c2 X / c1 del K(X) de Paper 10 (1/KAL0, 1/M^4)"),
    "M_meV_rhoLambda": ("(5*PHI**8)**0.25*2.25", "M con la escala LCDM rho_Lambda^(1/4) = 2.25 meV: la INCONSISTENTE que Paper 10 descarta"),   # ORIGEN-VALOR: 2.25 — rho_Lambda^(1/4) en meV de LCDM, el valor que Paper 10 cita para descartarlo
    "inv_1pw0":       ("1/(1+W0)", "entalpia rho+p en unidades de rho_DE(1+w0)"),
    "inv_1pw0_m1":    ("1/(1+W0)-1", "c_s^2 efectivo del intento descartado, Paper 5"),
    "MIRA_m1":        ("MIRA-1", "Paper 5 Q2"),
    "kcrit_p5":       ("1/TAU_PI_H0", "k de transicion NS-IS en z=0, Paper 5 (x=1)"),
    "zeta_tilde":     ("KAL0/3", "viscosidad adimensional, Paper 5"),
    "r_star_q2":      ("(MIRA-1)*OMEGA_M_TOTAL/OMDE_DENS", "r que haria falta para R=MIRA (blanco retirado), Paper 5 Q2"),
    "smnu_kal11":     ("SUM_MNU_EV/1.1**2", "Sigma m_nu con KAL0 -> 1.1 KAL0 (va como KAL0^-2), Paper 5"),
    "cs2_rho_norm":   ("W0+1/(1+W0)-1", "c_s^2 con zeta normalizada a rho_DE (superluminico), Paper 5"),
    "tau_saturado":   ("KAL0/3*(1+W0)", "tau_Pi H0 de la saturacion causal con la entalpia, Paper 5"),
    "n_ssee":         ("(1+W0)/(2*W0)", "exponente n, seccion EFT"),
    "n_ssee_TM":      ("(T_R-M_V)/(2*T_R)", "la misma n por T_r, M_v (control)"),
    "wa_viejo":       ("-3*WA", "w_a con Gamma = w_a (version retirada), seccion EFT"),
    "u_condensado":   ("(1-W0)/(3*W0-1)", "u del condensado, Paper 7"),
    "u_condensado_TM": ("-(M_V+T_R)/(3*T_R+M_V)", "la misma u por T_r, M_v (control)"),
    "uno_mas_3u":     ("1+3*(1-W0)/(3*W0-1)", "Paper 7"),
    "uno_mas_6u":     ("1+6*(1-W0)/(3*W0-1)", "Paper 7 (no-ghost)"),
    "uno_mas_2u":     ("1+2*(1-W0)/(3*W0-1)", "Paper 7 (NEC)"),
    "X_sobre_Xmin":   ("-2*(1-W0)/(3*W0-1)", "punto del condensado, Paper 7"),
    "p7_Xbg_pct":     ("100*(-2*(1-W0)/(3*W0-1)-1)", "X_bg sobre X_min en %, Paper 7"),
    "p7_norm_err_pct": ("100*(S_DE/OMDE_DENS-1)", "error de amplitud de la normalizacion vieja de K (s_DE en vez de Omega_DE), Paper 7"),
    "p7_cuartal_pct": ("100*(4*AURA-3*OMDE_DENS*(5-3*W0))/(4*AURA)", "distancia de alpha_K a CUARTAL=4 AURA, Paper 7"),
    "phi_mas_2pi":    ("PHI+2*PI", "SOLAR = MAR, Papers 1 y 4"),
    "pi_mas_KAL":     ("PI+KAL0", "tabla de Paper 4"),
    "phi_pi_KAL":     ("PHI+PI+KAL0", "tabla de Paper 4"),
    "dos_Omega_phi":  ("2*OMEGA+PHI", "tabla de Paper 4"),
    "dos_phi_":       ("2*PHI", "Sealed / PRD"),
    "SOLAR_NYX":      ("(PHI+2*PI)/((PHI+7*PI)/2)", "Sealed / PRD"),
    "KAL_KALeff":     ("KAL0/(PHI**2*math.sqrt(5/2))", "Paper 10, Ruta A"),
    "KAL_KALeff2":    ("(KAL0/(PHI**2*math.sqrt(5/2)))**2", "Paper 10, Ruta A"),
    "sK_tercio":      ("S_K/3", "rho_phi(1+w0) en rho_crit = 1, Paper 10"),
    "X_bg_IR":        ("S_K*KAL0/6", "X_bg IR en rho_crit = 1, Paper 10"),
    "cs2_condensado": ("(1+W0)/(5-3*W0)", "c_s^2 del condensado, Paper 7"),
    "cs2_condensado_TM": ("(M_V-T_R)/(5*M_V+3*T_R)", "la misma c_s^2 por T_r, M_v (control)"),
    "sK_con_KX_de_P7": ("3*(5-3*W0)*S_DE", "6(XK_X+2X^2K_XX) con la K(X) de Paper 7 y rho_phi = S_DE (Paper 10, las dos K(X))"),
    "sK_con_KX_de_P7_c1": ("6*S_DE/(1+3*(1-W0)/(3*W0-1))*(1+6*(1-W0)/(3*W0-1))", "lo mismo desde c1 X y u (control)"),
    "factor_dos_KX":  ("3*(5-3*W0)*S_DE/S_K_FULL", "cociente contra s_K completo de Paper 10"),
    "wc_estatico_planck": ("KAL0*0.02237", "Omega_c h^2 = KAL0 * omega_b(Planck), relacion estatica de Paper 4"),   # ORIGEN-VALOR: 0.02237 — omega_b de Planck 2018 VI Tabla 2, la entrada que declara Paper 4
    "wc_estatico_sigma": ("(KAL0*0.02237-0.1200)/0.0012", "distancia a Planck 0.1200 +- 0.0012, Paper 4"),   # ORIGEN-VALOR: 0.02237, 0.1200, 0.0012 — Planck 2018 VI Tabla 2
    "wc_estatico_ssee": ("KAL0*OMEGA_B_H2", "Omega_c h^2 estatico con el omega_b PROPIO de SSEE (2026-10-01: Paper 4 usaba el de Planck, ingrediente de otro modelo)"),
    "wc_estatico_ssee_sigma": ("(KAL0*OMEGA_B_H2-0.1200)/0.0012", "su distancia a Planck"),   # ORIGEN-VALOR: 0.1200, 0.0012 — Planck 2018 VI Tabla 2
    "wc_ns_sigma":    ("(OMEGA_C_H2-0.1200)/0.0012", "omega_c = KAL0 omega_b n_s frente a Planck"),   # ORIGEN-VALOR: 0.1200, 0.0012 — Planck 2018 VI Tabla 2
    "Omega_b_planck": ("0.02237/0.6736**2", "Omega_b de LCDM-Planck = omega_b/h^2 con SUS ingredientes"),   # ORIGEN-VALOR: 0.02237, 0.6736 — Planck 2018 VI Tabla 2
    "Omega_b_pct_vs_planck": ("100*(OMEGA_B_H2/(H0_ALG/100)**2/(0.02237/0.6736**2)-1)", "diferencia en %; casi toda es h_SSEE > h_Planck"),   # ORIGEN-VALOR: 0.02237, 0.6736 — Planck 2018 VI Tabla 2
    "wc_ns_sigma_abs": ("abs(OMEGA_C_H2-0.1200)/0.0012", "lo mismo en valor absoluto, para «a X sigma de Planck»"),   # ORIGEN-VALOR: 0.1200, 0.0012 — Planck 2018 VI Tabla 2
    "wb_sigma_planck": ("abs(OMEGA_B_H2-0.02237)/0.00015", "omega_b algebraico frente a Planck, en sigma"),   # ORIGEN-VALOR: 0.02237, 0.00015 — Planck 2018 VI Tabla 2
    "ns_sigma_planck": ("abs(N_S-0.9649)/0.0042", "n_s = 1-phi^-7 frente a Planck, en sigma"),   # ORIGEN-VALOR: 0.9649, 0.0042 — Planck 2018 VI Tabla 2
    "Om_sigma_planck": ("abs(OMEGA_M_TOTAL-0.3153)/0.0073", "Omega_m = omega_m/h^2 frente a Planck, en sigma"),   # ORIGEN-VALOR: 0.3153, 0.0073 — Planck 2018 VI Tabla 2
    "H0alg_sigma_planck": ("abs(H0_ALG-67.36)/0.54", "el numero puro 3(phi+pi)^2 frente al H0 de Planck, en sigma"),   # ORIGEN-VALOR: 67.36, 0.54 — Planck 2018 VI Tabla 2
    "WA_abs":          ("abs(WA)", "|w_a| = P_sc/IGNIS, para la busqueda look-elsewhere (Sealed)"),
    "Om_sin_nu":       ("(OMEGA_B_H2+OMEGA_C_H2)/(H0_GLOBAL/100)**2", "Omega_m sin omega_nu: muestra que el neutrino no es opcional (Sealed)"),
    "Om_sin_nu_pct":   ("100*OMEGA_M_H2/(OMEGA_B_H2+OMEGA_C_H2)-100", "corrimiento relativo en % al quitar omega_nu"),
    "Yp_ssee":        ("0.2471+0.0016*273.9*(OMEGA_B_H2-0.02237)", "Y_p lineal, Paper 4"),   # ORIGEN-VALOR: 0.2471 y 0.02237 — Y_p BBN de Planck 2018 VI en su omega_b; 0.0016 = dY_p/d(eta_10) y 273.9 = eta_10/omega_b — Steigman 2007 (ARNPS 57, 463). Era 0.96 «de AlterBBN (Pisanti 2008)»: 2.2 veces la sensibilidad publicada (quinta lectura P4, 2026-10-11); Y_p no cambia a 4 decimales
    "Yp_aver_sig":    ("abs(0.2471+0.0016*273.9*(OMEGA_B_H2-0.02237)-0.2449)/0.0040", "Y_p de SSEE frente a las regiones HII (P4)"),   # ORIGEN-VALOR: 0.2449 +- 0.0040 — Aver, Olive & Skillman 2015
    "eta_ssee_1e10":  ("273.9*OMEGA_B_H2", "eta_10 = 1e10 n_b/n_gamma de SSEE (P4)"),   # ORIGEN-VALOR: 273.9 — Steigman 2007
    "halg_planck_sig": ("abs(H0_ALG-67.36)/0.54", "el numero puro 3(phi+pi)^2 leido en km/s/Mpc frente al H0 de Planck (P4)"),   # ORIGEN-VALOR: 67.36 +- 0.54 — Planck 2018 VI Tabla 2
    "Omega_b_alg":    ("OMEGA_B_H2/(H0_ALG/100)**2", "Omega_b = omega_b/h^2 con h = 3 Omega^2/100, Paper 4"),
    "Omega_b_alg_cerrada": ("1e4*(PI-PHI)/(27*OMEGA**6)", "la misma en forma cerrada (control)"),
    # auditoría del lector externo (2026-10-11): cifras que P1/P2/P5/P8 tecleaban a mano
    "hglob_residuo_rel": ("(H0_GLOBAL-H0_ALG)/H0_ALG", "residuo relativo de H_glob frente al numero puro (P1, P2)"),
    "hglob_planck_sig": ("abs(H0_GLOBAL-67.36)/math.hypot(SIG_H0_GLOBAL,0.54)", "H_glob (con su sigma) frente al H0 de Planck, errores combinados (P5)"),   # ORIGEN-VALOR: 67.36, 0.54 — Planck 2018 VI Tabla 2
    "k_bao_c_H0":     ("0.1*299792.458/H0_GLOBAL", "k = 0.1/Mpc en unidades de H0/c (P5)"),   # ORIGEN-VALOR: 0.1 — escala BAO de diseño; 299792.458 — c en km/s
    "frac_de_z19":    ("(1-OMEGA_M_TOTAL)*20**(3*(1+W0+WA))*math.exp(-3*WA*19/20)/(OMEGA_M_TOTAL*20**3+(1-OMEGA_M_TOTAL)*20**(3*(1+W0+WA))*math.exp(-3*WA*19/20))", "fraccion de energia oscura en z=19, CPL (P5)"),
    "ck_H0_AU":       ("299792.458/(H0_GLOBAL*4.84813681109536e-12)", "c k/H0 a k = 1/UA (P8)"),   # ORIGEN-VALOR: 4.84813681109536e-12 — 1 UA en Mpc (IAU 2012)
    "quinta_fuerza_AU": ("(H0_GLOBAL*4.84813681109536e-12/299792.458)**2*abs(1+W0)*(1-OMEGA_M_TOTAL)", "F_phi/F_N cuasi-estatico a 1 UA (P8 eq. fifth_force_qs)"),
    "quinta_fuerza_margen": ("1e-5/((H0_GLOBAL*4.84813681109536e-12/299792.458)**2*abs(1+W0)*(1-OMEGA_M_TOTAL))", "margen frente a la cota de Cassini 1e-5 (P8)"),   # ORIGEN-VALOR: 1e-5 — Cassini (Will 2014)
    "H_glob_IR_aditiva":     ("H0_SH0ES/(1+F_SCREEN_IR)", "forma aditiva del apantallamiento IR (P9 eq. H0local_add)"),
    "H_glob_IR_aditiva_res": ("H0_SH0ES/(1+F_SCREEN_IR)-H0_ALG", "su residuo frente al numero puro (P9)"),
    "H_glob_IR_aditiva_sig": ("(H0_SH0ES/(1+F_SCREEN_IR)-H0_ALG)/(SIG_H0_SH0ES*(1-F_SCREEN_IR))", "ese residuo en unidades del sigma SH0ES propagado (P9)"),
    "H_glob_IR_aditiva_dif": ("H0_SH0ES/(1+F_SCREEN_IR)-H0_SH0ES*(1-F_SCREEN_IR)", "aditiva menos multiplicativa, km/s/Mpc (P9)"),
    # quinta lectura P1 (2026-10-11): el cruce fantasma de CPL lo tecleaba a mano
    "a_cruce":        ("1+(1+W0)/WA", "factor de escala del cruce fantasma w(a*)=-1, CPL (P1)"),
    "z_cruce":        ("-(1+W0)/WA/(1+(1+W0)/WA)", "z del cruce fantasma (P1)"),
    "c_cruce_coef":   ("-WA/(1+W0)", "c(a)=coef*(1-a): fraccion viscosa que reproduce CPL (P1)"),
    "c_cruce_z1":     ("-WA/(1+W0)*0.5", "esa fraccion en z=1 (P1)"),
    "w0_mas_wa":      ("W0+WA", "w(a->0) de CPL (P1)"),
    # quinta lectura P2 (2026-10-11): cifras que P2 tecleaba a mano
    "wb_bbn_sig":     ("abs(OMEGA_B_H2-0.02218)/0.00055", "omega_b algebraico frente al prior BBN de DESI (P2)"),   # ORIGEN-VALOR: 0.02218, 0.00055 — Schöneberg 2024 (prior BBN de DESI DR2)
    "w0_cmb_solo_sig": ("(W0+1.57)/0.50", "w0 de SSEE frente al w constante de Planck CMB solo, error superior (P2)"),   # ORIGEN-VALOR: -1.57 +0.50 — Planck 2018 VI, w constante, TT,TE,EE+lowE+lensing
    "h_glob":         ("H0_GLOBAL/100", "h adimensional del H global (P3)"),
    "horizonte_cs_Mpc": ("math.sqrt((1+W0)/(5-3*W0))*299792.458/H0_GLOBAL", "horizonte sonoro c_s c/H0 del condensado, Paper 7"),   # ORIGEN-VALOR: 299792.458 — c en km/s (definicion SI)
    # quinta lectura P8 (2026-10-12): cifras que P8 tecleaba a mano
    "p8_grad_coef":   ("2*KAL0*AURA", "coeficiente del cierre de gradientes, limite (a) de Paper 8"),
    "p8_Geff":        ("1+2*KAL0*AURA**2", "G_eff/G lineal sobre la materia oscura, limite (a) de Paper 8"),
    "quinta_fuerza_Mpc":   ("(H0_GLOBAL/299792.458)**2*abs(1+W0)*(1-OMEGA_M_TOTAL)", "F_phi/F_N cuasi-estatico a k = 1/Mpc (P8)"),
    "quinta_fuerza_10kpc": ("(H0_GLOBAL*0.01/299792.458)**2*abs(1+W0)*(1-OMEGA_M_TOTAL)", "F_phi/F_N cuasi-estatico a k = 1/(10 kpc), radio de Einstein galactico (P8)"),
    "M_meV":          ("1e3*(5*PHI**8*3*(H0_GLOBAL*1e3/3.0856775814913673e22*6.582119569e-16)**2*2.435323e27**2)**0.25", "M = (5 phi^8 rho_crit)^(1/4) en meV con H_glob (P8, P10)"),   # ORIGEN-VALOR: 3.0856775814913673e22 m = 1 Mpc (IAU 2015); 6.582119569e-16 eV s = hbar (CODATA 2018, exacta); 2.435323e27 eV = masa de Planck reducida (CODATA 2018 G)
    "eps_UV":         ("_X_UV**2/_M4_UV", "X_bg^2/M^4 en unidades rho_crit = 1 (P8, P10)"),
    # quinta lectura P9 (2026-10-12)
    "frac_de_zstar":  ("(1-OMEGA_M_TOTAL)*1090**(3*(1+W0+WA))*math.exp(-3*WA*1089/1090)/(OMEGA_M_TOTAL*1090**3+(1-OMEGA_M_TOTAL)*1090**(3*(1+W0+WA))*math.exp(-3*WA*1089/1090))", "fraccion de energia oscura en z*=1089, CPL sin radiacion: cota superior (P9)"),   # ORIGEN-VALOR: 1089 — z* de Planck 2018 VI (1089.9)
}

res, errores = {}, []
for k, (f, uso) in ALGEBRA.items():
    try:
        res[k] = dict(formula=f, valor=float(eval(f, {}, N)), uso=uso)
    except Exception as e:
        errores.append(f"{k}: {e}")
ctl = {
    "u dos formas": abs(res["u_condensado"]["valor"] - res["u_condensado_TM"]["valor"]),
    "n dos formas": abs(res["n_ssee"]["valor"] - res["n_ssee_TM"]["valor"]),
    "AURA = 2 MIRA": abs(S.AURA - 2 * S.MIRA),
    "s_K con K(X) de P7, dos formas": abs(res["sK_con_KX_de_P7"]["valor"] - res["sK_con_KX_de_P7_c1"]["valor"]),
    "Omega_b dos formas": abs(res["Omega_b_alg"]["valor"] - res["Omega_b_alg_cerrada"]["valor"]),
    "c_s^2 dos formas": abs(res["cs2_condensado"]["valor"] - res["cs2_condensado_TM"]["valor"]),
}
try:
    eval("1/(1+W0-1-W0)", {}, N)
    roto = False
except ZeroDivisionError:
    roto = True
# El nucleo tambien, evaluado: los papers imprimen el valor de K_V, no la formula.
nucleo = {k: float(v) for k, v in N.items()
          if k.isupper() and isinstance(v, (int, float)) and not isinstance(v, bool)}
out = dict(fecha=str(__import__("datetime").date.today()), algebra=res, nucleo=nucleo,
           control=dict(identidades=ctl, pasa=bool(all(v < 1e-12 for v in ctl.values()) and roto and not errores),
                        formula_rota_falla=roto, errores=errores))
json.dump(con_acta(out, __file__), open(os.path.join(_R, "results", "logs", "algebra_derivada.json"), "w"), indent=1)
print(f"  {len(res)} valores · identidades {ctl} · formula rota falla: {roto} · errores {errores}")
print(f"  control: {'PASA' if out['control']['pasa'] else 'NO PASA'}")
