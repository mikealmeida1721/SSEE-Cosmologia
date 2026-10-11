#!/usr/bin/env python3
"""CONTROL NEGATIVO: reproducir like = -130.157350 de la cadena oficial KiDS-1000 xi_pm.
Punto de maxima posterior, Blind C (maxpost_multinest_start_C.txt)."""
import numpy as np, time, sys, pathlib
import kids_shear as K

# --- punto de maxima posterior de la cadena oficial ---
# LEIDO DEL ARCHIVO, no tecleado (2026-09-19). Antes estos valores iban escritos
# a mano y REDONDEADOS: `0.079140` donde el archivo dice `0.07914`, `0.002320`
# donde dice `2.31956e-03`, y un delta_c de `-0.000001` donde el archivo dice
# `-6.32757e-07`. R65 no podia rastrearlos porque no casaban letra a letra con
# su fuente. Ahora salen de ella: la ultima fila del maxpost, por nombre de
# columna.
_MAXPOST = ('/mnt/datos/SSEE_data/kids1000/KiDS1000_cosmis_shear_data_release/'
            'chains_and_config_files/main_chains_iterative_covariance/xipm/'
            'chain/maxpost_multinest_start_C.txt')
with open(_MAXPOST) as _f:
    _col = _f.readline().lstrip('#').split()
    _fila = [l for l in _f if l.strip() and not l.startswith('#')][-1].split()
_v = {c: float(x) for c, x in zip(_col, _fila)}
MP = dict(omch2=_v['cosmological_parameters--omch2'],
          ombh2=_v['cosmological_parameters--ombh2'],
          h0=_v['cosmological_parameters--h0'],
          ns=_v['cosmological_parameters--n_s'],
          halo_A=_v['halo_model_parameters--a'],
          A_IA=_v['intrinsic_alignment_parameters--a'],
          delta_c=_v['shear_c_bias--delta_c'],
          sigma8_target=_v['cosmological_parameters--sigma_8'],
          S8_ref=_v['cosmological_parameters--S_8'],
          Om_ref=_v['cosmological_parameters--omega_m'])
DZ = np.array([_v[f'delta_z_out--bin_{i}'] for i in range(1, 6)])
LIKE_REF = _v['like']

D = K.load_data(); m = K.scale_mask(D)
print(f'puntos usados: {int(m.sum())} de {len(D["d"])}', flush=True)

# --- calibrar A_s para el sigma8 del punto de maxima posterior ---
As = 2.1e-9
for it in range(6):
    res, p, kh, zpk, pk, gr = K.run_camb(As=As, omch2=MP['omch2'], ombh2=MP['ombh2'],
                                         h0=MP['h0'], ns=MP['ns'], halo_A=MP['halo_A'])
    s8 = res.get_sigma8_0()
    print(f'  iter {it}: As={As:.6e}  sigma8={s8:.6f}', flush=True)
    if abs(s8 - MP['sigma8_target']) < 1e-5:
        break
    As *= (MP['sigma8_target'] / s8) ** 2

Om = (p.omch2 + p.ombh2 + p.omnuh2) / p.h**2
print(f'Om calculado = {Om:.6f}   (cadena: {MP["Om_ref"]:.6f})', flush=True)
print(f'S8 calculado = {s8*np.sqrt(Om/0.3):.6f}   (cadena: {MP["S8_ref"]:.6f})', flush=True)

t = time.time()
ells, Cl, idx = K.cl_shear(D, res, p, kh, zpk, pk, gr, MP['A_IA'], DZ)
print(f'C_ell listo en {time.time()-t:.1f}s', flush=True)
th = K.theory_vector(D, ells, Cl, idx, delta_c=MP['delta_c'])
c2 = K.chi2(D, th, m)

# CONVENCION (corregida 2026-09-19). CosmoSIS reporta loglike = -0.5*chi2, SIN
# el termino de normalizacion -0.5*ln|2 pi C|. La comprobacion es directa:
#     -2 * (-130.157350) = 260.31  =  chi2 = 260.32 publicado por KiDS-1000.
# Las tres lineas que este script imprimia antes (`like completo` = 2649.06 y
# `chi2 implicito` = 5819.71) sumaban esa normalizacion y por eso no casaban
# con nada: eran decorativas, nunca fueron el numero que se comparo. Se dejan
# calculadas abajo, pero rotuladas como lo que son.
Csub = D['C'][np.ix_(m, m)]
sign, logdet = np.linalg.slogdet(2 * np.pi * Csub)
print()
print(f'chi2            = {c2:.4f}   (ndata={int(m.sum())})')
print(f'REFERENCIA      = {-2*LIKE_REF:.4f}   (= -2 * {LIKE_REF:.6f})')
print(f'   -> desvio    = {100*(c2 + 2*LIKE_REF)/(-2*LIKE_REF):+.2f}%')
print()
print(f'[informativo, NO es la comparacion] -0.5*ln|2piC| = {-0.5*logdet:.4f}')
# Ruta ABSOLUTA, no relativa: con `control_theory.npy` a secas el artefacto
# caia en el directorio desde el que se lanzara — el 2026-09-19 aterrizo
# dentro de src/. Un resultado vive en results/, lo lance quien lo lance.
_SAL = pathlib.Path(__file__).resolve().parents[2] / 'results' / 'control_theory.npy'
np.save(_SAL, th)
print(f'  vector teorico -> {_SAL}')

# Persistido a log (cuarta lectura 2026-10-11): Paper 6 cita este chi2 como control negativo
# y sólo vivía en la salida por pantalla.
import json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from procedencia import con_acta  # noqa: E402
_LOG = pathlib.Path(__file__).resolve().parents[2] / 'results' / 'logs' / 'kids1000_control.json'
json.dump(con_acta(dict(chi2=float(c2), ndata=int(m.sum()), chi2_publicado=float(-2 * LIKE_REF),
                        desvio_pct=float(100 * (c2 + 2 * LIKE_REF) / (-2 * LIKE_REF)),
                        punto="maxima posterior de la cadena oficial KiDS-1000 xi_pm, Blind C"),
                   __file__, entradas=[_MAXPOST]),
          open(_LOG, 'w'), indent=1, ensure_ascii=False)
print(f'  log -> {_LOG}')
