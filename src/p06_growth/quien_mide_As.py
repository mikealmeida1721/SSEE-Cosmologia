"""¿Cuál de las dos sondas mide MEJOR A_s? (pregunta de Mike)

Misma regla para las dos: se barre logA, se perfila todo lo demas, y se toma la
anchura donde el chi2 sube 1 desde su minimo. Eso es la barra de esa sonda sobre
logA, medida del DATO CRUDO, no de un resumen.

  CMB  : plik_lite TTTEEE + lowT + lowE, 669 puntos. Libre ademas: tau.
  KiDS : 225 puntos xi_pm. Libres ademas: halo_A, A_IA, delta_c.

Fondo de SSEE CLAVADO en las dos. dz clavados en su media.
FUENTE: results/logs/growth_2026-07/quien_mide_As.json
"""
import json, pathlib, sys, time
import numpy as np
from scipy.optimize import minimize
REPO = pathlib.Path(__file__).resolve().parents[2]
for s in ("src","src/p06_growth","src/p03_cmb"): sys.path.insert(0,str(REPO/s))
import cobaya_kids as C, kids_shear as K, cmb_eval as E, ssee_core as S

BG=dict(C.SSEE_BG); BASE=dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2,
                              H0=S.H0_GLOBAL, ns=S.N_S)
_CA={}
def chi2_kids(logA):
    def f(u):
        h,a,d=float(u[0]),float(u[1]),float(u[2])
        if not (2.00<=h<=3.13): return 1e10
        k=(round(logA,6),round(h,4))
        if k not in _CA:
            if len(_CA)>50: _CA.clear()
            _CA[k]=K.run_camb(omch2=BG['omch2'],ombh2=BG['ombh2'],h0=BG['h0'],
                ns=BG['ns'],As=np.exp(logA)*1e-10,mnu=BG['mnu'],
                w=BG['w0'],wa=BG['wa'],halo_A=h)
        try:
            r,p,kh,zp,pk,gr=_CA[k]
            e,Cl,i=K.cl_shear(C.D,r,p,kh,zp,pk,gr,a,C.DZ_MEAN)
            th=K.theory_vector(C.D,e,Cl,i,delta_c=d)
        except Exception: return 1e10
        dv=(th-C.D['d'])[C.MASK]
        return float(dv@C.CINV@dv)+(d/C.DELTA_C_SIG)**2
    o=minimize(f,[2.60,0.55,0.0],method='Nelder-Mead',
               options=dict(maxiter=120,xatol=1e-3,fatol=1e-3))
    return float(o.fun)

def chi2_cmb(logA):
    def f(u):
        ta=float(u[0])
        if not (0.010<ta<0.200): return 1e30
        return E.chi2_y_s8(dict(BASE,logA=logA,tau=ta),S.W0,S.WA)[0]
    sim=np.array([[0.054],[0.059]])
    o=minimize(f,[0.054],method='Nelder-Mead',
               options=dict(maxiter=200,xatol=1e-5,fatol=1e-3,initial_simplex=sim))
    return float(o.fun)

def anchura(fn, centro, paso, n=5, etq=""):
    g=centro+paso*np.arange(-(n//2),n//2+1)
    c=np.array([fn(float(x)) for x in g])
    for x,y in zip(g,c): print("    logA=%.4f  chi2=%.4f"%(x,y),flush=True)
    cf=np.polyfit(g,c,2)
    if cf[0]<=0: return float('nan'),float('nan')
    return float(-cf[1]/(2*cf[0])), float(np.sqrt(1.0/cf[0]))

t0=time.time()
print("=== CMB (669 puntos, tau libre) ===",flush=True)
mC,sC=anchura(chi2_cmb, 3.0448, 0.010)
print("  minimo en logA=%.5f   sigma = %.5f\n"%(mC,sC),flush=True)
print("=== KiDS (225 puntos, 3 molestias libres) ===",flush=True)
mK,sK=anchura(chi2_kids, 2.858, 0.050)
print("  minimo en logA=%.5f   sigma = %.5f\n"%(mK,sK),flush=True)
print("  RAZON de precision (KiDS/CMB): %.1f veces"%(sK/sC),flush=True)
print("  distancia entre los dos minimos: %.4f = %.2f sigma de KiDS, %.2f del CMB"
      %(mC-mK,(mC-mK)/sK,(mC-mK)/sC),flush=True)
sal=REPO/"results"/"logs"/"growth_2026-07"/"quien_mide_As.json"
sal.write_text(json.dumps(dict(
  corrida="quien mide mejor A_s — misma regla, dato crudo",
  regla="se barre logA, se perfila el resto, sigma = anchura a dchi2=1",
  CMB=dict(npts=669, logA=mC, sigma=sC, libres_ademas=["tau"]),
  KiDS=dict(npts=225, logA=mK, sigma=sK,
            libres_ademas=["halo_A","A_IA","delta_c"]),
  razon_sigma_kids_sobre_cmb=float(sK/sC),
  separacion_logA=float(mC-mK),
  separacion_en_sigmas_de_kids=float((mC-mK)/sK),
  separacion_en_sigmas_del_cmb=float((mC-mK)/sC),
  segundos=time.time()-t0),indent=1,default=float))
print("escrito -> %s (%.1f min)"%(sal.relative_to(REPO),(time.time()-t0)/60),flush=True)
