#!/usr/bin/env python3
"""
Recálculo fσ8 para la tabla de Paper 3 con el MÉTODO CANÓNICO de Paper 5
(ODE de crecimiento completo, NO el Ω_m^γ analítico con γ=0.657 viejo).

Verificación de datos (Mike: "siempre verifica los datos con que se calcula"):
 - Fondo SSEE = H_ssee_exact de ssee_paper5_IS_perturbations.py:
     H/H0 = sqrt(Ω_m,CMB·a⁻³ + (1−Ω_m,CMB)·rDE_CPL), Ω_m,CMB=0.308881 (ω_m-directo)
 - σ8_SSEE = σ8_LCDM·G (G = D1_SSEE/D1_LCDM, suppression de la ODE)
 - fσ8(z) = f(z)·σ8·D(z)/D(0), con f=dlnD/dlna de la ODE (no Ω_m^γ)
 - DATASET = los 6 puntos RSD canónicos de Paper 5 (peer-reviewed, citables):
   6dFGRS, SDSS MGS, BOSS DR12 ×3, eBOSS DR16. Las 6 filas "DESI DR1" del viejo
   Paper 3 se ELIMINARON: fσ8 no verificable en la fuente oficial y NO hay fσ8 de
   DESI DR2 (DR2 = solo BAO). Paper 3 queda consistente con Paper 5 en método Y datos.
"""
import numpy as np
from scipy.integrate import solve_ivp
import os as _o66, sys as _s66
_s66.path.insert(0, _o66.path.dirname(_o66.path.dirname(_o66.path.abspath(__file__))))
import ssee_core as _C


PHI = (1+np.sqrt(5))/2; PI = np.pi
w0, wa = _C.W0, _C.WA   # del nucleo (2026-10-01: estaban tecleados a 4 decimales, -0.8399/-0.6699)
Omm_CMB = _C.OMEGA_M_TOTAL  # ω_m-directo (fondo gravitacional + fuente Poisson)
Omm_LCDM = 0.3153          # ORIGEN-VALOR: 0.3153 — Omega_m de Planck 2018 VI, Tabla 2
sigma8_LCDM = 0.811        # ORIGEN-VALOR: 0.811 — sigma8 de Planck 2018 VI, Tabla 2 (A_s heredado de Planck: diagnostico, no prediccion)

def H_ssee(a):
    rDE = a**(-3.0*(1.0+w0+wa))*np.exp(-3.0*wa*(1.0-a))
    return np.sqrt(Omm_CMB*a**-3 + (1.0-Omm_CMB)*rDE)
def H_lcdm(a):
    return np.sqrt(Omm_LCDM*a**-3 + (1.0-Omm_LCDM))

def dlnH_dlna(a, Hf, eps=5e-5):
    da = max(a*eps, 1e-9)
    return (Hf(a+da)-Hf(max(a-da,1e-9)))/(2*da)*a/Hf(a)

def growth(x, Y, Hf, Omsrc):
    a = np.exp(x); H = Hf(a); dH = dlnH_dlna(a, Hf)
    Om_a = Omsrc/(H**2*a**3); D1, u = Y
    return [u, -(2.0+dH)*u + 1.5*Om_a*D1]

a_ini = 1e-3; x_g = np.linspace(np.log(a_ini), 0.0, 1200); Y0 = [a_ini, a_ini]
sol_s = solve_ivp(lambda x,Y: growth(x,Y,H_ssee,Omm_CMB), [x_g[0],0.0], Y0,
                  method='DOP853', t_eval=x_g, rtol=1e-11, atol=1e-14)
sol_l = solve_ivp(lambda x,Y: growth(x,Y,H_lcdm,Omm_LCDM), [x_g[0],0.0], Y0,
                  method='DOP853', t_eval=x_g, rtol=1e-11, atol=1e-14)
a_g = np.exp(x_g); z_g = 1/a_g - 1
D1_s, u_s = sol_s.y; D1_l, u_l = sol_l.y
f_s = u_s/D1_s; f_l = u_l/D1_l                 # f = dlnD/dlna
D1_s_n = D1_s/D1_s[-1]; D1_l_n = D1_l/D1_l[-1]  # normalizado a a=1
G = D1_s[-1]/D1_l[-1]
sigma8_SSEE = sigma8_LCDM * G
print(f"  G = D1_SSEE/D1_LCDM = {G:.4f}   σ8_SSEE = {sigma8_SSEE:.4f}  (σ8_LCDM={sigma8_LCDM})")
gam = np.polyfit(np.log(Omm_CMB/(H_ssee(a_g)**2*a_g**3))[(z_g>=0)&(z_g<=2)],
                 np.log(f_s)[(z_g>=0)&(z_g<=2)], 1)[0]
print(f"  γ_IS (fit de la ODE, z=0..2) = {gam:.4f}   (canónico ~0.550)")

fs8_s = f_s*sigma8_SSEE*D1_s_n
fs8_l = f_l*sigma8_LCDM*D1_l_n

# datos: (z, obs, err, label) — DATASET CANÓNICO de Paper 5 (idéntico, peer-reviewed).
# Se eliminaron las 6 filas "DESI DR1" del viejo Paper 3: sus valores fσ8 no se
# pudieron verificar contra la fuente oficial (DESI 2024 VII, arXiv:2411.12022, no
# tabula fσ8 directo per-tracer; el paper conjunto P+B da σ_s8 comprimido). Además NO
# existe un release DESI DR2 de fσ8 (DR2 = solo BAO, arXiv:2503.14738). Se alinea
# Paper 3 al dataset canónico de Paper 5 → mismo método Y mismos datos.
data = [
 (0.067,0.423,0.055,"6dFGRS (Beutler+2012)"),
 (0.150,0.490,0.145,"SDSS MGS (Howlett+2015)"),
 (0.380,0.497,0.045,"BOSS DR12 z=0.38 (Alam+2017)"),
 (0.510,0.458,0.038,"BOSS DR12 z=0.51 (Alam+2017)"),
 (0.610,0.436,0.034,"BOSS DR12 z=0.61 (Alam+2017)"),
 (1.480,0.462,0.045,"eBOSS DR16 (Hou+2021)"),
]
print(f"\n  {'survey':34s} {'z':5s} {'obs':13s} {'SSEE':6s} {'t_S':5s} {'ΛCDM':6s} {'t_L':5s}")
tS=[]; tL=[]; chiS=0; chiL=0; filas=[]
for z,o,e,lab in data:
    i = np.argmin(np.abs(z_g-z))
    s = fs8_s[i]; l = fs8_l[i]
    ts = abs(s-o)/e; tl = abs(l-o)/e
    tS.append(ts); tL.append(tl); chiS += ((s-o)/e)**2; chiL += ((l-o)/e)**2
    filas.append(dict(survey=lab, z=z, obs=o, err=e, ssee=float(s), lcdm=float(l), pull_ssee=float((s-o)/e), pull_lcdm=float((l-o)/e)))
    print(f"  {lab:34s} {z:.3f} {o:.3f}±{e:.3f} {s:.3f}  {ts:.2f}σ  {l:.3f}  {tl:.2f}σ")
N=len(data)
print(f"\n  χ²/N  SSEE={chiS/N:.3f}   ΛCDM={chiL/N:.3f}   (N={N})")
print(f"  tensión media  SSEE={np.mean(tS):.2f}σ   ΛCDM={np.mean(tL):.2f}σ")

# ── Salida con acta (2026-10-01; antes solo se imprimia) ──
import json as _json  # noqa: E402
from procedencia import con_acta as _acta  # noqa: E402
_R0 = _o66.path.dirname(_o66.path.dirname(_o66.path.dirname(_o66.path.abspath(__file__))))
_json.dump(_acta(dict(G=float(G), sigma8_ssee=float(sigma8_SSEE), gamma_IS=float(gam), filas=filas,
                      chi2N_ssee=float(chiS / N), chi2N_lcdm=float(chiL / N),
                      tension_media_ssee=float(np.mean(tS)), tension_media_lcdm=float(np.mean(tL)),
                      max_pull_ssee=float(max(tS))), __file__),
           open(_o66.path.join(_R0, "results", "logs", "fsigma8_canonico.json"), "w"), indent=1)
