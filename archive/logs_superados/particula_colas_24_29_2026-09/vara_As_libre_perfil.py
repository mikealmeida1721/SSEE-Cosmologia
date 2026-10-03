"""La vara que faltaba: KiDS con A_s LIBRE, en el MISMO perfil que la particula.

POR QUE HACE FALTA. Vengo comparando 271.31 (particula, perfil de 3 molestias,
los dz clavados en su media) contra 265.44 (cadena R3, 9 libres, dz incluidos).
ESO NO ES COMPARABLE: es un perfil contra un marginal, con distinto numero de
libres — el mismo desemparejamiento de reglas de la cola #22.

Mike pregunto exactamente esto: cuanto se mueve la particula respecto de lo que
el modelo presenta con A_s libre. Para responderlo hace falta el A_s libre
medido EN EL MISMO PERFIL.

LIBRES AQUI: logA, halo_A, A_IA, delta_c.  (4)
Contra la particula: m_x, omega_x, halo_A, A_IA, delta_c, con logA CLAVADO. (5)
Fondo de SSEE clavado en los dos. dz clavados en su media en los dos.

CONTROL (R53): con logA forzado a 3.0448340130228546 este perfil tiene que
devolver 282.1758, el que ya midio la pinza. Criterio < 0.05.
"""
import json, pathlib, sys, time
import numpy as np
from scipy.optimize import minimize

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src")); sys.path.insert(0, str(REPO / "src" / "p06_growth"))
import cobaya_kids as C
import kids_shear as K

LOGA_CMB = 3.0448340130228546
BG = dict(C.SSEE_BG)
_CA = {}

def chi2(logA, halo_A, A_IA, delta_c):
    if not (2.00 <= halo_A <= 3.13) or not (1.0 < logA < 5.0):
        return 1e10
    k = (round(logA, 6), round(halo_A, 4))
    if k not in _CA:
        if len(_CA) > 60: _CA.clear()
        _CA[k] = K.run_camb(omch2=BG['omch2'], ombh2=BG['ombh2'], h0=BG['h0'],
                            ns=BG['ns'], As=np.exp(logA)*1e-10, mnu=BG['mnu'],
                            w=BG['w0'], wa=BG['wa'], halo_A=halo_A)
    try:
        r, p, kh, zpk, pk, gr = _CA[k]
        ells, Cl, idx = K.cl_shear(C.D, r, p, kh, zpk, pk, gr, A_IA, C.DZ_MEAN)
        th = K.theory_vector(C.D, ells, Cl, idx, delta_c=delta_c)
    except Exception:
        return 1e10
    dv = (th - C.D['d'])[C.MASK]
    return float(dv @ C.CINV @ dv) + (delta_c / C.DELTA_C_SIG)**2

t0 = time.time()
print("CONTROL: logA clavado en %.6f debe dar 282.1758" % LOGA_CMB, flush=True)
o = minimize(lambda u: chi2(LOGA_CMB, u[0], u[1], u[2]), [2.60, 0.55, 0.0],
             method='Nelder-Mead', options=dict(maxiter=150, xatol=1e-3, fatol=1e-3))
err = abs(float(o.fun) - 282.1758); ok = bool(err < 0.05)
print("  da %.4f  err %.4f -> %s" % (o.fun, err, "PASA" if ok else "FALLA"), flush=True)

print("\nAhora con logA LIBRE:", flush=True)
o2 = minimize(lambda u: chi2(u[0], u[1], u[2], u[3]), [2.90, 2.60, 0.55, 0.0],
              method='Nelder-Mead', options=dict(maxiter=300, xatol=1e-4, fatol=1e-3))
lA, hA, aIA, dC = [float(v) for v in o2.x]
print("  chi2 = %.4f   logA = %.4f (CMB pide %.4f)  halo_A = %.3f  A_IA = %.4f"
      % (o2.fun, lA, LOGA_CMB, hA, aIA), flush=True)

sal = REPO / "results" / "logs" / "growth_2026-07" / "vara_As_libre_perfil.json"
sal.write_text(json.dumps(dict(
    corrida="vara: KiDS con A_s libre en el MISMO perfil que la particula",
    motivo="Mike — cuanto se mueve la particula respecto de lo que el modelo "
           "presenta con A_s libre. El 265.44 de la cadena R3 NO es comparable: "
           "es marginal con 9 libres contra perfil con 3.",
    control_logA_clavado=dict(chi2=float(o.fun), esperado=282.1758,
                              err=float(err), pasa=ok),
    libres=["logA", "halo_A", "A_IA", "delta_c"],
    dz="clavados en su media, igual que en la corrida de la particula",
    chi2=float(o2.fun), logA=lA, logA_del_CMB=LOGA_CMB,
    halo_A=hA, A_IA=aIA, delta_c=dC,
    segundos=time.time()-t0), indent=1, default=float))
print("\nescrito -> %s (%.1f min)" % (sal.relative_to(REPO), (time.time()-t0)/60), flush=True)
