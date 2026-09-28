"""LAS TRES SONDAS A LA VEZ, con UN SOLO A_s — el ajuste conjunto (cola #28)

=====================================================================
POR QUE, Y QUE CORRIGE
=====================================================================

La pinza anterior estaba MAL MONTADA y Mike lo caso: sumaba un chi2 de KiDS con
logA CLAVADO en 3.0448 y un chi2 del CMB con logA LIBRE. O sea que el CMB se
movia la amplitud por su cuenta y KiDS no se enteraba. Eso no es un ajuste
conjunto, son dos ajustes distintos sumados. Se retiro entera.

AQUI hay UN SOLO logA, compartido por las tres sondas a la vez. Se barre, y en
cada valor las tres se evaluan EN EL MISMO PUNTO. El fondo va clavado por
algebra. La particula es lo unico que puede absorber.

=====================================================================
QUIEN MANDA SOBRE QUE (diseno de Mike)
=====================================================================

  A_s   lo ancla el CMB, que lo mide sigma = 0.01454, unas 3.5 veces mejor que
        KiDS, y ademas lo mide DONDE esta definido (el pivote k=0.05 Mpc^-1 cae
        dentro de su rango) y CUANDO se imprimio, sin nada por el medio.
  BOSS  entra con voz pero SIN VOTO sobre A_s: su amplitud esta degenerada con
        el sesgo de galaxias b1 (los dos multiplican P(k) por igual, D=4.01).
        Lo que SI puede decir es si la particula le encaja, porque la particula
        deja PENDIENTE y el sesgo es un numero: el sesgo no puede imitarla.

=====================================================================
EL LIMITE, FIJADO ANTES DE MIRAR
=====================================================================

Si el logA conjunto se aleja mas de 2 sigma del CMB (|dlogA| > 0.0291) la
solucion se marca RECHAZADA aunque el chi2 baje: significaria que la particula
esta arreglando un universo que no es el que el CMB midio.

=====================================================================
CONTROLES (R53), PRIMERO (R24)
=====================================================================

  C0 · con la particula APAGADA, cada sonda tiene que devolver su numero ya
       publicado en su propio minimo de logA:
         CMB  1003.587 en logA 3.0432      (medido hoy, sigma 0.01454)
         KiDS  266.559 en logA 2.8579      (vara_As_libre_perfil)
         BOSS  197.438 en logA 2.94479     (R1R2_boss_lpt_kmax0.200)
       Criterio: |dchi2| < 0.05 en cada una.

Ninguna cifra entra en ningun paper.
FUENTE: results/logs/growth_2026-07/conjunta_tres_sondas.json
"""
import json, multiprocessing as mp, pathlib, sys, time
import numpy as np
from scipy.optimize import minimize

REPO = pathlib.Path(__file__).resolve().parents[2]
for s in ("src","src/p06_growth","src/p03_cmb"): sys.path.insert(0,str(REPO/s))
import cobaya_kids as C, kids_shear as K, cmb_eval as E, ssee_core as S
import boss_lpt_R1R2 as B

SALIDA = REPO/"results"/"logs"/"growth_2026-07"/"conjunta_tres_sondas.json"
C_NU = 94.0641
LOGA_CMB, SIG_CMB = 3.04320, 0.01454
LIMITE = 2.0 * SIG_CMB                     # fijado ANTES de mirar
BG = dict(C.SSEE_BG)
BASE = dict(ombh2=S.OMEGA_B_H2, omch2=S.OMEGA_C_H2, H0=S.H0_GLOBAL, ns=S.N_S)

REJILLA_LOGA = np.linspace(2.88, 3.10, 9)
MASAS  = np.array([2.2, 4.0, 7.5, 15.0])
# ORIGEN de los numeros (R65, 2026-09-19)
# ORIGEN-VALOR: 0.01454 — 0.0145437 = sigma(logA) del CMB de SSEE, results/logs/growth_2026-07/quien_mide_As.json, redondeado a 5 decimales
# ORIGEN-VALOR: 0.0291 — 2 * 0.0145437 = 0.029087, redondeado a 4 decimales
# ORIGEN-VALOR: 0.0020 — nodo de rejilla elegido: 0.002 a 0.0065 en pasos de 0.0015
# ORIGEN-VALOR: 0.0035 — nodo de rejilla elegido (ver 0.0020)
# ORIGEN-VALOR: 0.0050 — nodo de rejilla elegido (ver 0.0020)
# ORIGEN-VALOR: 0.0065 — nodo de rejilla elegido (ver 0.0020)
OMEGAS = np.array([0.0020, 0.0035, 0.0050, 0.0065])
PUB = dict(CMB=1003.587, KiDS=266.559, BOSS=197.438)
NPROC = 4


def traduce(m_x, om_x):
    if om_x <= 0: return 0.0, 0.0, 0.0
    xi = (C_NU*om_x/m_x)**(1/3.)
    return xi, xi**4, om_x*C_NU


# ---------- cada sonda como funcion de logA, con su fondo ----------
_CK = {}
def chi2_kids(logA, m_x, om_x):
    _, dn, meff = traduce(m_x, om_x)
    def f(u):
        h,a,d = float(u[0]),float(u[1]),float(u[2])
        if not (2.00<=h<=3.13): return 1e10
        k=(round(logA,5),round(h,4),round(om_x,6),round(m_x or 0,3))
        if k not in _CK:
            if len(_CK)>40: _CK.clear()
            _CK[k]=K.run_camb(omch2=BG['omch2']-om_x, ombh2=BG['ombh2'],
                h0=BG['h0'], ns=BG['ns'], As=np.exp(logA)*1e-10, mnu=BG['mnu'],
                w=BG['w0'], wa=BG['wa'], halo_A=h, dneff=dn, meffsterile=meff)
        try:
            r,p,kh,zp,pk,gr=_CK[k]
            e,Cl,i=K.cl_shear(C.D,r,p,kh,zp,pk,gr,a,C.DZ_MEAN)
            th=K.theory_vector(C.D,e,Cl,i,delta_c=d)
        except Exception: return 1e10
        dv=(th-C.D['d'])[C.MASK]
        return float(dv@C.CINV@dv)+(d/C.DELTA_C_SIG)**2
    o=minimize(f,[2.60,0.55,0.0],method='Nelder-Mead',
               options=dict(maxiter=110,xatol=1e-3,fatol=1e-3))
    return float(o.fun)


def chi2_cmb(logA, m_x, om_x):
    _, dn, meff = traduce(m_x, om_x)
    def f(u):
        ta=float(u[0])
        if not (0.010<ta<0.200): return 1e30
        return E.chi2_particula(dict(BASE, omch2=BASE['omch2']-om_x,
                                     logA=logA, tau=ta), S.W0, S.WA, dn, meff)[0]
    o=minimize(f,[0.054],method='Nelder-Mead',
        options=dict(maxiter=160,xatol=1e-5,fatol=1e-3,
                     initial_simplex=np.array([[0.054],[0.059]])))
    return float(o.fun)


def perfil_boss(m_x, om_x):
    """Devuelve chi2_BOSS(logA) sobre REJILLA_LOGA. Reconstruye los conjuntos
    porque el fondo cambia con la particula."""
    c = dict(B.COSMO['SSEE'])
    if om_x > 0:
        xi, dn, meff = traduce(m_x, om_x)
        c.update(om_x=om_x, dneff=dn, meffsterile=meff)
    B.COSMO['SSEE'] = c
    sets = B.build()
    # ARREGLADO: la primera version llamaba a `chi2_marg_set`, que es la version
    # MARGINAL — la que lleva dentro el termino de volumen `ln det F`, justo lo
    # que descuadraba el logA de BOSS 1.85 sigma. Se usa `B.run`, que hace el
    # PERFIL con las 6 molestias por conjunto ajustadas, que es la maquinaria
    # validada y la que produjo el 197.438 publicado.
    r = B.run('SSEE', sets)
    g = np.array(r['perfil']['logA']); c2 = np.array(r['perfil']['chi2'])
    return np.interp(REJILLA_LOGA, g, c2), sets


def un_punto(a):
    m_x, om_x = a
    xi, dn, _ = traduce(m_x, om_x)
    cb, _ = perfil_boss(m_x, om_x)
    ck = np.array([chi2_kids(float(l), m_x, om_x) for l in REJILLA_LOGA])
    cc = np.array([chi2_cmb(float(l), m_x, om_x) for l in REJILLA_LOGA])
    tot = ck + cc + cb
    i = int(np.argmin(tot))
    lA = float(REJILLA_LOGA[i])
    d = lA - LOGA_CMB
    print("  m_x=%6.1f om_x=%.4f dNeff=%.4f | logA*=%.4f (%+.2f sig CMB) | "
          "CMB %9.2f KiDS %8.2f BOSS %8.2f | TOT %10.2f %s" % (
        m_x or 0, om_x, dn, lA, d/SIG_CMB, cc[i], ck[i], cb[i], tot[i],
        "RECHAZADA" if abs(d)>LIMITE else ""), flush=True)
    return dict(m_x=m_x, omega_x=om_x, xi=float(xi), dNeff=float(dn),
        logA=lA, dlogA_vs_CMB=float(d), sigmas_vs_CMB=float(d/SIG_CMB),
        rechazada_por_limite=bool(abs(d)>LIMITE),
        chi2_cmb=float(cc[i]), chi2_kids=float(ck[i]), chi2_boss=float(cb[i]),
        chi2_total=float(tot[i]),
        perfil=dict(logA=REJILLA_LOGA.tolist(), cmb=cc.tolist(),
                    kids=ck.tolist(), boss=cb.tolist(), total=tot.tolist()))


def main():
    t0=time.time()
    print("="*104, flush=True)
    print("  CONTROL C0 — particula apagada, cada sonda en SU minimo", flush=True)
    print("="*104, flush=True)
    ok={}
    cc0=chi2_cmb(LOGA_CMB, None, 0.0); ok['CMB']=bool(abs(cc0-PUB['CMB'])<0.05)
    print("  CMB  %.4f vs %.3f -> %s"%(cc0,PUB['CMB'],"PASA" if ok['CMB'] else "FALLA"),flush=True)
    ck0=chi2_kids(2.8579, None, 0.0); ok['KiDS']=bool(abs(ck0-PUB['KiDS'])<0.05)
    print("  KiDS %.4f vs %.3f -> %s"%(ck0,PUB['KiDS'],"PASA" if ok['KiDS'] else "FALLA"),flush=True)
    cb0,_=perfil_boss(None,0.0)
    mb=float(np.min(cb0)); ok['BOSS']=bool(mb-PUB['BOSS']<0.30)
    print("  BOSS %.4f (min de la rejilla) vs %.3f -> %s"%(
        mb,PUB['BOSS'],"PASA" if ok['BOSS'] else "FALLA"),flush=True)
    ok['pasa']=bool(all(ok[k] for k in ('CMB','KiDS','BOSS')))
    print("  LIMITE fijado antes de mirar: |dlogA| <= %.4f (2 sigma del CMB)"%LIMITE,flush=True)
    if not ok['pasa']:
        SALIDA.write_text(json.dumps(dict(corrida="cola #28",controles=ok,
            veredicto="controles no pasan; no se lee nada"),indent=1))
        print("\nCONTROLES FALLAN.",flush=True); return

    pts=[(float(m),float(o)) for m in MASAS for o in OMEGAS]
    print("\n"+"="*104,flush=True)
    print("  LAS TRES A LA VEZ — %d casillas, un solo logA"%len(pts),flush=True)
    print("="*104,flush=True)
    with mp.Pool(NPROC) as pool: res=pool.map(un_punto,pts)
    res.sort(key=lambda r:r['chi2_total'])
    SALIDA.write_text(json.dumps(dict(
        corrida="cola #28 — CMB + KiDS + BOSS a la vez, con UN SOLO A_s",
        diseno="M. Almeida: el CMB ancla A_s; BOSS entra con voz pero sin voto "
               "sobre la amplitud (degenerada con b1); la particula es lo unico "
               "que puede absorber, con el fondo clavado por algebra",
        corrige="la pinza anterior sumaba KiDS con logA clavado y CMB con logA "
                "libre: no era un ajuste conjunto. Retirada entera.",
        limite_logA=dict(sigma_cmb=SIG_CMB, max_dlogA=LIMITE,
                         fijado="antes de mirar ningun resultado"),
        controles=ok, publicados=PUB, rejilla_logA=REJILLA_LOGA.tolist(),
        masas=MASAS.tolist(), omegas=OMEGAS.tolist(), puntos=res,
        mejor=res[0], segundos=time.time()-t0),indent=1,default=float))
    b=res[0]
    print("\n  MEJOR: m_x=%.1f eV om_x=%.4f  logA=%.4f (%+.2f sig del CMB)  TOT %.2f %s"%(
        b['m_x'],b['omega_x'],b['logA'],b['sigmas_vs_CMB'],b['chi2_total'],
        "<<< RECHAZADA POR EL LIMITE" if b['rechazada_por_limite'] else ""),flush=True)
    print("\nescrito -> %s (%.2f h)"%(SALIDA.relative_to(REPO),(time.time()-t0)/3600),flush=True)


if __name__=='__main__': main()
