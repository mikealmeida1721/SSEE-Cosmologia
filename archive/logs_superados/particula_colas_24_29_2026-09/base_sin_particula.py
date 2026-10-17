"""LA CASILLA QUE FALTABA: el ajuste conjunto SIN particula (control de la cola #28)

=====================================================================
QUE FALTA Y POR QUE IMPORTA
=====================================================================

`conjunta_tres_sondas.py` barrio 16 casillas (4 masas x 4 omegas) y devolvio un
minimo de chi2_total = 1470.83 en m_x=7.5 eV, om_x=0.0065. Ese numero NO SE
PUEDE LEER, porque la rejilla NO CONTIENE la casilla om_x = 0: no hay un
chi2_total conjunto sin particula contra el que compararlo.

El control C0 de esa corrida NO sirve para esto, y hay que decirlo claro:
evalua cada sonda en SU PROPIO minimo de logA (CMB en 3.0432, KiDS en 2.8579,
BOSS en 2.94479). Sumar esos tres es precisamente el error que la cola #28 se
escribio para corregir — tres ajustes distintos sumados. Su suma, 1467.58, NO
es un chi2 conjunto y no es la linea base.

Esto corre UNA casilla con om_x = 0.0, con la MISMA maquinaria, la MISMA
rejilla de logA y UN SOLO logA compartido. Eso, y solo eso, da la referencia.

=====================================================================
COMO SE LEE EL RESULTADO (fijado ANTES de mirar, R24)
=====================================================================

  dchi2 = 1470.83 - chi2_total(om_x=0)

  dchi2 > 0  ->  la particula EMPEORA el ajuste conjunto. La cola #28 no
                 encontro nada; el minimo de su rejilla es peor que no poner
                 nada, y la rejilla simplemente no llegaba al borde.
  dchi2 < 0  ->  la particula mejora, y entonces hay que pesar la mejora
                 contra los parametros que cuesta (2: m_x y om_x).
                 Referencia de honestidad: con Dk=2, un dchi2 de -2 es ruido;
                 hace falta |dchi2| >~ 6 para hablar de preferencia.

No se lee nada mas. Ninguna cifra entra en ningun paper.

=====================================================================
POR QUE VA EN SERIE, Y NO CON UN POOL (2026-09-13)
=====================================================================

La primera version de este archivo repartia los 9 valores de logA en un
mp.Pool(4) y SE COLGO: 3 h 20 min con los cuatro hijos a 0.0 % de CPU y
tiempo acumulado 00:00:00, o sea sin ejecutar una sola instruccion.

La causa es de manual y fue mia: `perfil_boss` corre CAMB, que arranca
sus hilos (OpenMP/BLAS), y el Pool se creaba DESPUES. Al hacer fork, los
hijos heredan los mutexes de esos hilos en el estado en que estaban
—bloqueados— y no hay quien los suelte, porque los hilos que los tenian
no se copian al hijo. Deadlock silencioso: ni error, ni CPU, ni fin.

`conjunta_tres_sondas.py` NO tiene el problema aunque use Pool, y la
diferencia es el ORDEN: alli el Pool se crea antes de tocar CAMB y cada
hijo corre su propio BOSS ya dentro del proceso hijo.

Aqui se va EN SERIE, en un solo proceso, sin fork de ninguna clase. Es
una sola casilla: no vale la pena arriesgar el resto por un 4x.

REGLA QUE ESTO DEJA: no crear un Pool despues de haber llamado a CAMB en
el proceso padre. O el Pool primero, o nada de Pool.

R53: este archivo ES el control de conjunta_tres_sondas.json.
FUENTE: results/logs/growth_2026-07/base_sin_particula.json
"""
# ORIGEN-VALOR: 0.0065 — minimo de la #28 en m_x=7.5 eV, results/logs/growth_2026-07/conjunta_tres_sondas.json
import json, pathlib, sys, time
import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[2]
for s in ("src", "src/p06_growth", "src/p03_cmb"): sys.path.insert(0, str(REPO/s))
import conjunta_tres_sondas as Q

SALIDA = REPO/"results"/"logs"/"growth_2026-07"/"base_sin_particula.json"
CONJUNTA = REPO/"results"/"logs"/"growth_2026-07"/"conjunta_tres_sondas.json"


def una_kids(l):  return float(Q.chi2_kids(float(l), None, 0.0))
def una_cmb(l):   return float(Q.chi2_cmb(float(l), None, 0.0))


def main():
    t0 = time.time()
    R = Q.REJILLA_LOGA
    print("="*104, flush=True)
    print("  BASE SIN PARTICULA — una casilla, om_x = 0, un solo logA", flush=True)
    print("  rejilla logA: %s" % np.round(R, 4).tolist(), flush=True)
    print("="*104, flush=True)

    cb, _ = Q.perfil_boss(None, 0.0)
    print("  BOSS listo (min %.3f)" % float(np.min(cb)), flush=True)

    ck = np.empty(len(R))
    for j, l in enumerate(R):
        t = time.time(); ck[j] = una_kids(l)
        print("  KiDS %d/%d  logA=%.4f  chi2=%9.3f  (%.1f min)" % (
            j+1, len(R), l, ck[j], (time.time()-t)/60), flush=True)
    print("  KiDS listo (min %.3f)" % float(ck.min()), flush=True)

    cc = np.empty(len(R))
    for j, l in enumerate(R):
        t = time.time(); cc[j] = una_cmb(l)
        print("  CMB  %d/%d  logA=%.4f  chi2=%9.3f  (%.1f min)" % (
            j+1, len(R), l, cc[j], (time.time()-t)/60), flush=True)
    print("  CMB listo (min %.3f)" % float(cc.min()), flush=True)

    tot = ck + cc + cb
    i = int(np.argmin(tot))
    lA = float(R[i]); d = lA - Q.LOGA_CMB

    print("\n  %9s %10s %10s %10s %12s" % ("logA", "CMB", "KiDS", "BOSS", "TOTAL"), flush=True)
    for j, l in enumerate(R):
        print("  %9.4f %10.2f %10.2f %10.2f %12.2f %s" % (
            l, cc[j], ck[j], cb[j], tot[j], "<-- min" if j == i else ""), flush=True)

    base = float(tot[i])
    mejor = json.loads(CONJUNTA.read_text())["mejor"]
    dchi2 = mejor["chi2_total"] - base

    print("\n  BASE  om_x=0        logA=%.4f (%+.2f sig CMB)  TOT %10.2f" % (
        lA, d/Q.SIG_CMB, base), flush=True)
    print("  MEJOR m_x=%.1f om_x=%.4f logA=%.4f              TOT %10.2f" % (
        mejor["m_x"], mejor["omega_x"], mejor["logA"], mejor["chi2_total"]), flush=True)
    print("\n  dchi2 = %+.2f  (Dk=2)  ->  %s" % (dchi2,
        "la particula EMPEORA: la cola #28 no encontro nada" if dchi2 > 0 else
        ("mejora pero por debajo del ruido de 2 parametros" if dchi2 > -6 else
         "mejora por encima del ruido de 2 parametros")), flush=True)

    SALIDA.write_text(json.dumps(dict(
        corrida="base sin particula — la casilla om_x=0 que le faltaba a la cola #28",
        para_que="dar la referencia contra la que leer el chi2_total=1470.83; "
                 "el control C0 de la cola #28 NO sirve porque evalua cada sonda "
                 "en su propio minimo de logA, que es el error que esa corrida corrige",
        lectura_fijada_antes="dchi2>0 la particula empeora; dchi2<0 hay que pesarla "
                             "contra Dk=2, y por debajo de |6| es ruido",
        rejilla_logA=R.tolist(), cmb=cc.tolist(), kids=ck.tolist(), boss=cb.tolist(),
        total=tot.tolist(), logA_base=lA, sigmas_vs_CMB=float(d/Q.SIG_CMB),
        chi2_base=base, chi2_mejor_con_particula=mejor["chi2_total"],
        mejor_con_particula=mejor, dchi2=dchi2, delta_k=2,
        veredicto=("la particula EMPEORA el ajuste conjunto" if dchi2 > 0 else
                   ("mejora por debajo del ruido de 2 parametros" if dchi2 > -6 else
                    "mejora por encima del ruido de 2 parametros")),
        segundos=time.time()-t0), indent=1, default=float))
    print("\nescrito -> %s (%.2f h)" % (SALIDA.relative_to(REPO), (time.time()-t0)/3600), flush=True)


if __name__ == '__main__':
    main()
