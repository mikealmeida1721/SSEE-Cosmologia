#!/usr/bin/env python3
"""
QUE A_s EXIGE CADA OBSERVABLE, bajo el fondo de SSEE.

Idea: con el fondo clavado por algebra, A_s es la unica perilla de amplitud, y
     sigma8 propto sqrt(A_s),   fsigma8(z) propto sigma8   (lineal).
Asi que cada observable de amplitud puede traducirse a un unico numero: el logA
que exigiria. Si todos coinciden, hay una tension real de amplitud. Si el de la
cizalla es el unico bajo, la cizalla es el outlier.

  logA_pedido = logA_modelo + 2*ln(obs / teoria)

CAVEAT DECLARADO: los fsigma8 publicados se derivan con una cosmologia fiducial
LCDM (efecto Alcock-Paczynski dentro del numero reportado). Estan contaminados
igual que lo estaba el S8 de KiDS. Este calculo es una PRIMERA ESTIMACION, no el
analisis limpio — ese exige bajar a los multipolos P0/P2/P4 crudos.
"""
import numpy as np, sys, csv
sys.path.insert(0, '/home/mike/Proyectos/SSEE/src')
import ssee_core as S
import camb

# El blanco del CMB NO se teclea: se lee del canonico. Antes estaba escrito
# a mano como 3.040704 +- 0.014375, valores del ajuste de julio de 2026 que
# el reframe dejo atras — la cadena results/chains/ssee_cmb.*.txt da
# 3.044335 +- 0.013872, y el canonico vigente es logA_cmb_ssee. Un literal
# no se entera de que su fuente cambio; una lectura si.
import yaml as _yaml
_CV = _yaml.safe_load(open('/home/mike/Proyectos/SSEE/CANONICAL_VALUES.yaml'))


def _canon(clave):
    for _blq in _CV.values():
        if isinstance(_blq, dict) and clave in _blq:
            return float(_blq[clave])
    raise KeyError(f'{clave} no esta en CANONICAL_VALUES.yaml')


LOGA_CMB = _canon('logA_cmb_ssee')
# ORIGEN: results/chains/ssee_cmb.*.txt — sigma de logA de la cadena del CMB
# con el fondo de SSEE, recalculada al vuelo para que no pueda quedar rancia.
import numpy as _np, glob as _glob
_f = sorted(_glob.glob('/home/mike/Proyectos/SSEE/results/chains/ssee_cmb.[0-9].txt'))
_c = open(_f[0]).readline().lstrip('#').split()
_a = _np.vstack([_np.loadtxt(x) for x in _f])
_x, _w = _a[:, _c.index('logA')], _a[:, 0]
_m = _np.average(_x, weights=_w)
SIG_LOGA_CMB = float(_np.sqrt(_np.average((_x - _m) ** 2, weights=_w)))
AS = 1e-10 * np.exp(LOGA_CMB)

d = list(csv.DictReader(
    l for l in open('/home/mike/Proyectos/SSEE/data/raw/fsigma8_rsd.csv')
    if not l.startswith('#')))
Z = np.array([float(r['z_eff']) for r in d])
FS = np.array([float(r['fsigma8']) for r in d])
ER = np.array([float(r['sigma']) for r in d])
SV = [r['survey'] for r in d]

p = camb.CAMBparams()
p.set_cosmology(H0=S.H0_GLOBAL, ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2,
                mnu=S.SUM_MNU_EV, omk=0.0)
p.set_dark_energy(w=S.W0, wa=S.WA, dark_energy_model='ppf')
p.InitPower.set_params(As=AS, ns=S.N_S)
p.set_matter_power(redshifts=list(Z[::-1]) + [0.0], kmax=2.0)
r = camb.get_results(p)
s8_0 = r.get_sigma8_0()
fs8_th = np.array(r.get_fsigma8())[::-1][1:]      # mismo orden que Z

print(f'fondo SSEE:  H0={S.H0_GLOBAL:.5f}  Om={S.OMEGA_M_CMB:.6f}  '
      f'w0={S.W0:.6f}  wa={S.WA:.6f}')
print(f'A_s del CMB de SSEE: logA={LOGA_CMB:.6f}  ->  sigma8={s8_0:.5f}\n')
print(f'{"z":>6} {"encuesta":16} {"fs8 obs":>9} {"fs8 teo":>9} '
      f'{"obs/teo":>8} {"logA pedido":>12} {"sigma":>7}')
lg, wt = [], []
for z, fo, e, sv, ft in zip(Z, FS, ER, SV, fs8_th):
    L = LOGA_CMB + 2 * np.log(fo / ft)
    sL = 2 * e / fo                                # d logA = 2 d fs8 / fs8
    n = (fo - ft) / e
    print(f'{z:6.3f} {sv:16} {fo:9.3f} {ft:9.3f} {fo/ft:8.4f} '
          f'{L:12.4f} {n:+7.2f}')
    lg.append(L); wt.append(1.0 / sL**2)
lg = np.array(lg); wt = np.array(wt)
L_rsd = np.sum(lg * wt) / np.sum(wt)
sL_rsd = 1.0 / np.sqrt(np.sum(wt))
s8_rsd = s8_0 * np.exp((L_rsd - LOGA_CMB) / 2)

chi2 = float(np.sum(((FS - fs8_th) / ER) ** 2))
print(f'\nchi2 de los 6 fsigma8 con el A_s del CMB = {chi2:.3f}  (N=6)')
print(f'  tension media = {np.mean(np.abs((FS-fs8_th)/ER)):.3f} sigma')

L_kids, sL_kids = 2.8671, 0.0544
print(f'\n{"="*66}\nQUE logA EXIGE CADA OBSERVABLE (fondo SSEE):')
for nm, L, sL in (('CMB Planck TTTEEE  ', LOGA_CMB, SIG_LOGA_CMB),
                  ('cizalla KiDS-1000  ', L_kids, sL_kids),
                  ('RSD fsigma8 (6 enc.)', L_rsd, sL_rsd)):
    s8 = s8_0 * np.exp((L - LOGA_CMB) / 2)
    print(f'  {nm}  logA = {L:.4f} +- {sL:.4f}   -> sigma8 = {s8:.4f}')
print(f'\n  CMB   vs cizalla : '
      f'{abs(LOGA_CMB-L_kids)/np.hypot(SIG_LOGA_CMB,sL_kids):.2f} sigma')
print(f'  CMB   vs RSD     : '
      f'{abs(LOGA_CMB-L_rsd)/np.hypot(SIG_LOGA_CMB,sL_rsd):.2f} sigma')
print(f'  RSD   vs cizalla : '
      f'{abs(L_rsd-L_kids)/np.hypot(sL_rsd,sL_kids):.2f} sigma')
print(f'\n  sigma8 que pide RSD = {s8_rsd:.4f}')

# ---- que le cuesta a RSD bajar la amplitud a lo que pide la cizalla ----
print(f'\n{"="*66}\nPRECIO EN fsigma8 DE BAJAR LA AMPLITUD A LO QUE PIDE LA CIZALLA:')
for nm, L in (('A_s del CMB      ', LOGA_CMB), ('A_s que pide KiDS', L_kids)):
    f = np.exp((L - LOGA_CMB) / 2)
    th = fs8_th * f
    n = (FS - th) / ER
    print(f'  {nm}  sigma8={s8_0*f:.4f}  chi2={np.sum(n**2):7.3f}  '
          f'|tension| media={np.mean(np.abs(n)):.3f} sigma')
# combinado CMB+RSD contra cizalla
wc, wr = 1/SIG_LOGA_CMB**2, 1/sL_rsd**2
Lc = (LOGA_CMB*wc + L_rsd*wr)/(wc+wr); sc = 1/np.sqrt(wc+wr)
print(f'\n  CMB+RSD combinados: logA = {Lc:.4f} +- {sc:.4f}  '
      f'-> sigma8 = {s8_0*np.exp((Lc-LOGA_CMB)/2):.4f}')
print(f'  CMB+RSD  vs  cizalla : '
      f'{abs(Lc-L_kids)/np.hypot(sc,sL_kids):.2f} sigma')
