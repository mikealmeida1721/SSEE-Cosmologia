#!/usr/bin/env python3
"""
PRUEBA DE NO-CIRCULARIDAD del despeje sigma8 <- fsigma8.

Lo que se mide:   fsigma8(z) = g(z) * sigma8,   g(z) = f(z) * D(z)/D(0)
g(z) es un COCIENTE de P(k) a distintos z, asi que A_s se cancela dentro.
=>  sigma8_pedido = fsigma8_obs / g(z)   sin usar ninguna amplitud.

PRUEBA: correr el MISMO fondo con dos A_s que difieren un factor 2 y verificar
que g(z) sale identico. Si g(z) cambiara, el despeje seria circular.
"""
import numpy as np, sys, csv
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
import ssee_core as S
import camb

d = list(csv.DictReader(
    l for l in open('/home/mike/Proyectos/SSEE/data/raw/fsigma8_rsd.csv')
    if not l.startswith('#')))
Z = np.array([float(r['z_eff']) for r in d])
FS = np.array([float(r['fsigma8']) for r in d])
ER = np.array([float(r['sigma']) for r in d])
SV = [r['survey'] for r in d]


def g_of_z(As):
    """g(z) = f(z) D(z)/D(0) = fsigma8(z)/sigma8(0).  Sin amplitud dentro."""
    p = camb.CAMBparams()
    p.set_cosmology(H0=S.H0_GLOBAL, ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2,
                    mnu=S.SUM_MNU_EV, omk=0.0)
    p.set_dark_energy(w=S.W0, wa=S.WA, dark_energy_model='ppf')
    p.InitPower.set_params(As=As, ns=S.N_S)
    p.set_matter_power(redshifts=list(Z[::-1]) + [0.0], kmax=2.0)
    r = camb.get_results(p)
    s8_0 = r.get_sigma8_0()
    fs8 = np.array(r.get_fsigma8())[::-1][1:]
    s8z = np.array(r.get_sigma8())[::-1][1:]
    return fs8 / s8_0, s8_0, fs8 / s8z, s8z / s8_0    # g, sigma8(0), f(z), D(z)/D(0)


A1 = 1e-10 * np.exp(3.040704)
A2 = 2.0 * A1
g1, s1, f1, D1 = g_of_z(A1)
g2, s2, f2, D2 = g_of_z(A2)

print(f'A_s(1) = {A1:.6e}   -> sigma8(0) = {s1:.6f}')
print(f'A_s(2) = {A2:.6e}   -> sigma8(0) = {s2:.6f}   '
      f'(cociente {s2/s1:.6f}, sqrt(2)={np.sqrt(2):.6f})\n')
print(f'{"z":>6} {"f(z) A1":>9} {"f(z) A2":>9} {"D/D0 A1":>9} {"D/D0 A2":>9} '
      f'{"g(z) A1":>9} {"g(z) A2":>9} {"g2/g1-1":>11}')
for i, z in enumerate(Z):
    print(f'{z:6.3f} {f1[i]:9.6f} {f2[i]:9.6f} {D1[i]:9.6f} {D2[i]:9.6f} '
          f'{g1[i]:9.6f} {g2[i]:9.6f} {g2[i]/g1[i]-1:+11.2e}')
print(f'\n  desviacion maxima de g(z) al DUPLICAR A_s: '
      f'{np.max(np.abs(g2/g1-1)):.3e}')

print(f'\n{"="*70}\nDESPEJE DIRECTO  sigma8 = fsigma8_obs / g(z)   (sin usar ninguna amplitud)')
print(f'{"z":>6} {"encuesta":16} {"fs8 obs":>8} {"g(z)":>9} '
      f'{"sigma8 pedido":>14} {"+-":>7}')
s8p = FS / g1
s8e = ER / g1
for z, sv, fo, g, sp, se in zip(Z, SV, FS, g1, s8p, s8e):
    print(f'{z:6.3f} {sv:16} {fo:8.3f} {g:9.6f} {sp:14.4f} {se:7.4f}')
w = 1 / s8e**2
m = np.sum(s8p * w) / np.sum(w); sm = 1 / np.sqrt(np.sum(w))
print(f'\n  sigma8 que pide RSD (media ponderada) = {m:.4f} +- {sm:.4f}')
# ORIGEN-VALOR: 0.7459 — sigma8 del perfil KiDS: parabola sobre los 7 puntos de results/logs/growth_2026-07/s8_barra_kids.json da 0.74592 +- 0.02029
# ORIGEN-VALOR: 0.0203 — ancho de esa misma parabola (Delta chi2 = 1): 0.02029
# ORIGEN-VALOR: 0.8243 — sigma8 por la ruta ANTERIOR (cociente), que este
# script reemplaza; se imprime como control de que ambas rutas coinciden.
print(f'  [la ruta anterior via cociente dio 0.8243 — deben coincidir]')
print(f'\n  sigma8 del CMB de SSEE      = {s1:.4f} +- 0.0058')
print(f'  sigma8 que pide la cizalla  = 0.7459 +- 0.0203')
print(f'\n  RSD     vs CMB     : {abs(m-s1)/np.hypot(sm,0.0058):.2f} sigma')
print(f'  RSD     vs cizalla : {abs(m-0.7459)/np.hypot(sm,0.0203):.2f} sigma')
