#!/usr/bin/env python3
"""TEST DE CONSISTENCIA: SSEE con Omega_m LIBRE contra la cizalla de KiDS.
No es un cambio de modelo: se suelta Om para ver si el dato empuja hacia el
0.308881 algebraico o lejos de el. Om se implementa via omch2 con h algebraico
y omega_b fijo (atado a BBN): omch2 = Om*h^2 - omb - omnu.   A_s tambien libre."""
import numpy as np, sys, time, json
from scipy.optimize import minimize
sys.path.insert(0,'/tmp/claude-1000/-home-mike-Proyectos-SSEE/238cf748-10c3-466e-9be3-e8e03009063e/scratchpad')
sys.path.insert(0,'/home/mike/Proyectos/SSEE/src')
import kids_shear as K, ssee_core as S
OMB,HH,NS,MNU,W0,WA = S.OMEGA_B_H2,S.H0_GLOBAL/100,S.N_S,S.SUM_MNU_EV,S.W0,S.WA
OMNU = MNU/93.14
SOM=np.loadtxt('/mnt/datos/SSEE_data/kids1000/kcap/runs/3x2pt/data_iterated_cov/cosmology/multinest_blindC_EE_nE_w/data/KiDS/SOM_cov_multiplied.asc')
DZM=np.array([0.,-0.002,-0.013,-0.011,0.006]); SI=np.linalg.inv(SOM)
D=K.load_data(); M=K.scale_mask(D); CI=np.linalg.inv(D['C'][np.ix_(M,M)])
_C={}
def cam(As,hA,Om):
    oc=Om*HH**2-OMB-OMNU
    k=(round(As,18),round(hA,6),round(oc,8))
    if k not in _C:
        if len(_C)>250: _C.clear()
        _C[k]=K.run_camb(omch2=oc,ombh2=OMB,h0=HH,ns=NS,As=As,mnu=MNU,w=W0,wa=WA,halo_A=hA)
    return _C[k]
def nlp(x):
    lgA,Om,hA,aI=x[0],x[1],x[2],x[3]; dz=x[4:9]; dc=x[9]
    if not(0.15<=Om<=0.45) or not(2.0<=hA<=3.13) or not(-6<=aI<=6): return 1e10
    if not(2.0<=lgA<=4.2): return 1e10
    try:
        r,p,kh,zp,pk,gr=cam(1e-10*np.exp(lgA),hA,Om)
        e,Cl,ix=K.cl_shear(D,r,p,kh,zp,pk,gr,aI,dz); th=K.theory_vector(D,e,Cl,ix,delta_c=dc)
    except Exception: return 1e10
    dv=(th-D['d'])[M]; c2=float(dv@CI@dv); rr=dz-DZM
    return 0.5*(c2+float(rr@SI@rr)+(dc/2.3e-4)**2)
t=time.time()
x0=np.array([2.8671,S.OMEGA_M_CMB,2.6,0.6]+list(DZM)+[0.])
r=minimize(nlp,x0,method='Nelder-Mead',options=dict(maxiter=6000,xatol=1e-4,fatol=1e-3))
x=r.x; As=1e-10*np.exp(x[0])
res,p,kh,zp,pk,gr=cam(As,x[2],x[1])
e,Cl,ix=K.cl_shear(D,res,p,kh,zp,pk,gr,x[3],x[4:9]); th=K.theory_vector(D,e,Cl,ix,delta_c=x[9])
dv=(th-D['d'])[M]; c2=float(dv@CI@dv); s8=float(res.get_sigma8_0())
Om=(p.omch2+p.ombh2+p.omnuh2)/p.h**2
o=dict(label='d1_ssee_Om_LIBRE_As_libre',chi2=c2,ndata=int(M.sum()),Om=Om,
       Om_algebraico=S.OMEGA_M_CMB,sigma8=s8,S8=s8*np.sqrt(Om/0.3),logA=float(x[0]),
       halo_A=float(x[2]),A_IA=float(x[3]),nfree=10,secs=time.time()-t)
print(json.dumps(o),flush=True)
json.dump(o,open('ssee_om_libre.json','w'),indent=1)
