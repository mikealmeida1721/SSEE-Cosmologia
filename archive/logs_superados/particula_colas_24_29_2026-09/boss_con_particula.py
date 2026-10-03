"""BOSS con la particula dentro — la TERCERA sonda (cola #27)

=====================================================================
DE DONDE VIENE: prediccion de Mike, registrada antes de correr
=====================================================================

«con esta particula tomada en cuenta deberia corregir eso que falta, y de esa
manera con el fondo clavado y la particula deberia dar chi2 dentro de 1 sigma»

QUE MIDE, Y POR QUE ES UNA PRUEBA DE VERDAD. KiDS eligio la densidad. El CMB
eligio la masa. Los dos estan GASTADOS y ya no pueden confirmar nada. BOSS no
se ha usado: sus 222 puntos no han visto la particula. Es el primer dato que
puede decir que no.

LA DIRECCION, que es lo falsable. La particula FRENA el crecimiento. Con menos
crecimiento, para reproducir lo que BOSS ve hace falta MAS amplitud. O sea que
la particula empuja el logA de BOSS HACIA ARRIBA, hacia el 3.0448 del CMB.

  hoy, sin particula (perfil):  logA = 2.94479 +- 0.12385  ->  0.81 sigma
  si la particula acierta:      sube hacia 3.04, bajando esa distancia
  si se pasa:                   se cruza el 3.0448 y aparece tension AL REVES

Esa ultima es la falsacion limpia: no es un empate, es un fallo con signo.

=====================================================================
CONTROL (R53), PRIMERO (R24)
=====================================================================

  C0 · con om_x = 0 la maquinaria tiene que devolver EXACTAMENTE el logA y el
       chi2 ya publicados (2.94479 y 197.43784, kmax=0.20). Toque `camb_lin`,
       que es codigo validado; si esto se mueve, nada de lo demas vale.
       Criterio: |dlogA| < 1e-4 y |dchi2| < 0.01.

Ninguna cifra entra en ningun paper.
FUENTE: results/logs/growth_2026-07/boss_con_particula.json
"""
import json, pathlib, sys, time
import numpy as np
REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO/"src")); sys.path.insert(0, str(REPO/"src"/"p06_growth"))
import boss_lpt_R1R2 as B

C_NU = 94.0641
LOGA_CMB = 3.0448340130228546
REF = dict(logA=2.94479, sig=0.12385, chi2=197.43784)   # publicado, kmax=0.20

# ORIGEN-VALOR: 0.0030 — mejor punto de la #25 (m=4.0 eV), results/logs/precio_cmb_de_la_particula.json
# ORIGEN-VALOR: 0.0050 — punto intermedio ELEGIDO entre el de la #25 y el de la #28 (m=5.5 eV), no es medida
# ORIGEN-VALOR: 0.0065 — mejor punto de la #28 (m=7.5 eV), results/logs/growth_2026-07/conjunta_tres_sondas.json
PUNTOS = [(None, 0.0), (4.0, 0.0030), (5.5, 0.0050), (7.5, 0.0065)]


def cosmo_con(m_x, om_x):
    c = dict(B.COSMO['SSEE'])
    if om_x > 0:
        xi = (C_NU * om_x / m_x) ** (1/3.)
        c.update(om_x=om_x, dneff=xi**4, meffsterile=om_x*C_NU)
        return c, xi
    return c, 0.0


def main():
    t0 = time.time()
    print("="*78, flush=True)
    print("  BOSS con la particula — 222 puntos, k_max = %.2f" % B.KMAX, flush=True)
    print("="*78, flush=True)
    sets = B.build()

    # --- CONTROL C0, primero ---
    B.COSMO['SSEE'] = cosmo_con(None, 0.0)[0]
    r0 = B.run('SSEE', sets)
    dA = abs(r0['logA'] - REF['logA']); dC = abs(r0['chi2'] - REF['chi2'])
    ok = bool(dA < 1e-4 and dC < 0.01)
    print("\n  C0 · sin particula: logA %.5f (err %.2e)  chi2 %.5f (err %.2e) -> %s"
          % (r0['logA'], dA, r0['chi2'], dC, "PASA" if ok else "FALLA"), flush=True)
    if not ok:
        print("  CONTROL FALLA — no se lee nada.", flush=True); return

    res = [dict(m_x=None, omega_x=0.0, xi=0.0, dNeff=0.0, logA=r0['logA'],
                sig_logA=r0['sig_logA'], chi2=r0['chi2'],
                sigmas_del_CMB=(LOGA_CMB-r0['logA'])/r0['sig_logA'])]
    print("\n%8s %8s %8s %8s | %9s %9s %9s | %s" % (
        "m_x eV","om_x","xi","dNeff","logA","+-","chi2","vs CMB 3.04483"), flush=True)
    print("%8s %8s %8s %8s | %9.5f %9.5f %9.3f | %+.2f sigma" % (
        "--","0","--","--", r0['logA'], r0['sig_logA'], r0['chi2'],
        res[0]['sigmas_del_CMB']), flush=True)

    for m_x, om_x in PUNTOS[1:]:
        c, xi = cosmo_con(m_x, om_x)
        B.COSMO['SSEE'] = c
        r = B.run('SSEE', sets)
        s = (LOGA_CMB - r['logA']) / r['sig_logA']
        res.append(dict(m_x=m_x, omega_x=om_x, xi=float(xi), dNeff=float(xi**4),
                        logA=r['logA'], sig_logA=r['sig_logA'], chi2=r['chi2'],
                        sigmas_del_CMB=float(s),
                        fsigma8=[b['fsigma8'] for b in r['bins']]))
        print("%8.1f %8.4f %8.4f %8.4f | %9.5f %9.5f %9.3f | %+.2f sigma" % (
            m_x, om_x, xi, xi**4, r['logA'], r['sig_logA'], r['chi2'], s), flush=True)

    sal = REPO/"results"/"logs"/"growth_2026-07"/"boss_con_particula.json"
    sal.write_text(json.dumps(dict(
        corrida="cola #27 — BOSS con la particula, la TERCERA sonda",
        prediccion_de="M. Almeida, registrada antes de correr",
        enunciado="la particula frena el crecimiento => BOSS necesita MAS "
                  "amplitud => su logA sube hacia el 3.0448 del CMB",
        falsacion="que no suba, o que se pase y aparezca tension al reves",
        control_C0=dict(pasa=ok, err_logA=float(dA), err_chi2=float(dC),
                        referencia=REF),
        logA_del_CMB=LOGA_CMB, kmax=B.KMAX, puntos=res,
        alcance="ninguna cifra entra en ningun paper",
        segundos=time.time()-t0), indent=1, default=float))
    print("\nescrito -> %s  (%.2f h)" % (sal.relative_to(REPO),(time.time()-t0)/3600),
          flush=True)


if __name__ == '__main__':
    main()
