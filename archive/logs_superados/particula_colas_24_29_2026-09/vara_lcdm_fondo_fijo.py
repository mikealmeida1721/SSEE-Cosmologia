"""El numero que falta para la simetria: LCDM con el fondo de Planck CLAVADO,
logA incluido, contra KiDS. El analogo exacto del 282.18 de SSEE.

Sin esto la tabla compara SSEE con fondo fijo contra LCDM con fondo libre, que
es justo el doble rasero que Mike senalo.

LIBRES: halo_A, A_IA, delta_c.   FIJOS: ombh2, omch2, H0, ns, logA de Planck.
dz clavados en su media, igual que en la corrida de la particula.

CONTROL (R53): el mismo perfil con el fondo de SSEE tiene que devolver 282.1758.
"""
# ORIGEN-VALOR: 0.6736 — h de Planck 2018 (arXiv:1807.06209)
import json, pathlib, sys, time
import numpy as np
from scipy.optimize import minimize
REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO/"src")); sys.path.insert(0, str(REPO/"src"/"p06_growth"))
import cobaya_kids as C, kids_shear as K

SSEE = dict(C.SSEE_BG); SSEE['logA'] = 3.0448340130228546
LCDM = dict(ombh2=0.02237, omch2=0.1200, h0=0.6736, ns=0.9649,
            mnu=0.06, w0=-1.0, wa=0.0, logA=3.0450790027403647)
_CA = {}
def chi2(bg, halo_A, A_IA, delta_c):
    if not (2.00 <= halo_A <= 3.13): return 1e10
    k = (bg['logA'], round(halo_A,4), bg['omch2'])
    if k not in _CA:
        if len(_CA)>40: _CA.clear()
        _CA[k] = K.run_camb(omch2=bg['omch2'], ombh2=bg['ombh2'], h0=bg['h0'],
                            ns=bg['ns'], As=np.exp(bg['logA'])*1e-10,
                            mnu=bg['mnu'], w=bg['w0'], wa=bg['wa'], halo_A=halo_A)
    try:
        r,p,kh,zpk,pk,gr = _CA[k]
        ells,Cl,idx = K.cl_shear(C.D,r,p,kh,zpk,pk,gr,A_IA,C.DZ_MEAN)
        th = K.theory_vector(C.D,ells,Cl,idx,delta_c=delta_c)
    except Exception: return 1e10
    dv=(th-C.D['d'])[C.MASK]
    return float(dv@C.CINV@dv)+(delta_c/C.DELTA_C_SIG)**2

def perfila(bg):
    o = minimize(lambda u: chi2(bg,u[0],u[1],u[2]), [2.60,0.55,0.0],
                 method='Nelder-Mead', options=dict(maxiter=150,xatol=1e-3,fatol=1e-3))
    return float(o.fun), [float(v) for v in o.x]

t0=time.time()
c,_ = perfila(SSEE); err=abs(c-282.1758)
print("CONTROL · el mismo perfil con SSEE: %.4f vs 282.1758  err %.4f -> %s"
      % (c, err, "PASA" if err<0.05 else "FALLA"), flush=True)
cl, arg = perfila(LCDM)
print("LCDM fondo Planck CLAVADO (logA=%.6f): chi2 = %.4f" % (LCDM['logA'], cl))
print("  halo_A=%.3f  A_IA=%.4f  delta_c=%.2e%s"
      % (arg[0],arg[1],arg[2], "  PEGADO" if arg[0]<=2.01 or arg[0]>=3.12 else ""))
sal = REPO/"results"/"logs"/"growth_2026-07"/"vara_lcdm_fondo_fijo.json"
sal.write_text(json.dumps(dict(
    corrida="LCDM con el fondo de Planck clavado, logA incluido, contra KiDS",
    motivo="Mike — la tabla comparaba SSEE con fondo fijo contra LCDM con fondo "
           "libre. Este es el analogo exacto del 282.18 de SSEE.",
    control_ssee=dict(chi2=c, esperado=282.1758, err=err, pasa=bool(err<0.05)),
    libres=["halo_A","A_IA","delta_c"], dz="clavados en su media",
    fondo_lcdm=LCDM, chi2_kids=cl,
    halo_A=arg[0], A_IA=arg[1], delta_c=arg[2],
    segundos=time.time()-t0), indent=1, default=float))
print("\nescrito -> %s (%.1f min)" % (sal.relative_to(REPO),(time.time()-t0)/60), flush=True)
