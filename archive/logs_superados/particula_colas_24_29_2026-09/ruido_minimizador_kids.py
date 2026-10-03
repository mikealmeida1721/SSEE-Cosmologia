"""PASO 0 — cuanto ruido mete el minimizador de molestias de KiDS (2026-09-13)

=====================================================================
POR QUE
=====================================================================
La puerta 3 de la cascada de Mike pide que KiDS llegue a 266.559 +- 2.30.
Pero el chi2 de KiDS sale de un Nelder-Mead sobre TRES molestias
(halo_A, A_IA, delta_c) con UN SOLO arranque fijo [2.60, 0.55, 0.0] y
maxiter=110. Si ese minimizador se queda corto por ~1, la tolerancia de
2.30 solo vale el doble del ruido y LA PUERTA NO DISCRIMINA.

Aqui se mide ese piso: el MISMO punto, varios arranques distintos, y se
mira la dispersion del chi2 devuelto.

  piso << 2.30  -> la puerta 3 discrimina, la cascada se puede correr
  piso ~  2.30  -> la puerta 3 NO discrimina; hay que ajustar mejor antes
  el minimo real es el MENOR de todos: si el arranque de produccion no lo
  encuentra, toda la rejilla esta corrida HACIA ARRIBA por esa cantidad.

Ninguna cifra entra en ningun paper.
SALIDA: results/logs/growth_2026-07/ruido_minimizador_kids.json
"""
# ORIGEN-VALOR: 3.0450 — nodo de la malla de logA (2.88 + 6*0.0275) donde la rejilla de la #28 dio su minimo, results/logs/growth_2026-07/conjunta_tres_sondas.json
import json, pathlib, sys, time
import numpy as np
from scipy.optimize import minimize

REPO = pathlib.Path(__file__).resolve().parents[2]
for s in ("src", "src/p06_growth", "src/p03_cmb"):
    sys.path.insert(0, str(REPO / s))
import cobaya_kids as C, kids_shear as K                    # noqa: E402

SALIDA = REPO / "results" / "logs" / "growth_2026-07" / "ruido_minimizador_kids.json"
BG = dict(C.SSEE_BG)
LOGA = 3.0450                      # el A_s donde la rejilla evalua todo
PRODUCCION = [2.60, 0.55, 0.0]     # el arranque unico que usa la rejilla
ARRANQUES = [PRODUCCION,
             [2.10, 0.20, 0.0], [3.05, 0.90, 0.0],
             [2.35, 0.75, 0.0], [2.85, 0.35, 0.0],
             [2.60, 0.05, 0.0], [2.60, 1.10, 0.0]]
MAXITER_PROD, MAXITER_LARGO = 110, 600


def chi2(logA, u):
    h, a, d = float(u[0]), float(u[1]), float(u[2])
    if not (2.00 <= h <= 3.13):
        return 1e10
    try:
        r, p, kh, zp, pk, gr = K.run_camb(
            omch2=BG['omch2'], ombh2=BG['ombh2'], h0=BG['h0'], ns=BG['ns'],
            As=np.exp(logA) * 1e-10, mnu=BG['mnu'], w=BG['w0'], wa=BG['wa'],
            halo_A=h, dneff=0.0, meffsterile=0.0)
        e, Cl, i = K.cl_shear(C.D, r, p, kh, zp, pk, gr, a, C.DZ_MEAN)
        th = K.theory_vector(C.D, e, Cl, i, delta_c=d)
    except Exception:
        return 1e10
    dv = (th - C.D['d'])[C.MASK]
    return float(dv @ C.CINV @ dv) + (d / C.DELTA_C_SIG) ** 2


def corre(x0, maxiter):
    t = time.time()
    o = minimize(lambda u: chi2(LOGA, u), x0, method='Nelder-Mead',
                 options=dict(maxiter=maxiter, xatol=1e-3, fatol=1e-3))
    return dict(x0=list(map(float, x0)), maxiter=maxiter, chi2=float(o.fun),
                x=list(map(float, o.x)), nit=int(o.nit), nfev=int(o.nfev),
                exito=bool(o.success), minutos=(time.time() - t) / 60.0)


def main():
    t0 = time.time()
    print("=" * 92)
    print("  PASO 0 — ruido del minimizador de molestias de KiDS")
    print("  mismo punto (fondo SSEE, om_x=0, logA=%.4f); solo cambia el arranque" % LOGA)
    print("=" * 92, flush=True)
    res = []
    for k, x0 in enumerate(ARRANQUES):
        mi = MAXITER_PROD
        r = corre(x0, mi); r['etiqueta'] = 'produccion' if k == 0 else 'alt%d' % k
        res.append(r)
        print("  %-11s x0=%-22s maxiter=%3d -> chi2 %9.4f  "
              "(halo_A %.3f A_IA %.3f dc %+.5f)  nit=%d  %.1f min"
              % (r['etiqueta'], str(x0), mi, r['chi2'], r['x'][0], r['x'][1],
                 r['x'][2], r['nit'], r['minutos']), flush=True)
    print("\n  --- el mismo arranque de produccion, pero SIN tope corto ---", flush=True)
    largo = corre(PRODUCCION, MAXITER_LARGO); largo['etiqueta'] = 'produccion_largo'
    res.append(largo)
    print("  %-11s maxiter=%3d -> chi2 %9.4f  nit=%d  %.1f min"
          % (largo['etiqueta'], MAXITER_LARGO, largo['chi2'], largo['nit'],
             largo['minutos']), flush=True)

    c = np.array([r['chi2'] for r in res if r['chi2'] < 1e9])
    prod = res[0]['chi2']; mejor = float(c.min())
    disp = float(c.max() - c.min()); sd = float(c.std())
    print("\n" + "=" * 92)
    print("  chi2 de produccion .......... %9.4f" % prod)
    print("  mejor encontrado ............ %9.4f   (arranque: %s)"
          % (mejor, [r['etiqueta'] for r in res if r['chi2'] == mejor][0]))
    print("  SESGO de produccion ......... %+9.4f   <- cuanto sobra en TODA la rejilla"
          % (prod - mejor))
    print("  dispersion (max-min) ........ %9.4f" % disp)
    print("  desviacion tipica ........... %9.4f" % sd)
    print("  tolerancia de la puerta 3 ... %9.4f   (1 sigma de Dk=2)" % 2.30)
    if disp < 0.23:
        v = "PISO << tolerancia: la puerta 3 DISCRIMINA"
    elif disp < 2.30:
        v = "piso comparable: la puerta 3 discrimina DEBIL, declararlo"
    else:
        v = "PISO >= tolerancia: la puerta 3 NO DISCRIMINA; hay que ajustar mejor antes"
    print("  VEREDICTO: %s" % v)
    print("=" * 92, flush=True)
    SALIDA.write_text(json.dumps(dict(
        corrida="paso 0 — ruido del minimizador de molestias de KiDS",
        para_que="saber si la puerta 3 de la cascada puede discriminar",
        logA=LOGA, arranque_de_produccion=PRODUCCION,
        maxiter_produccion=MAXITER_PROD, maxiter_largo=MAXITER_LARGO,
        corridas=res, chi2_produccion=prod, chi2_mejor=mejor,
        sesgo_produccion=prod - mejor, dispersion=disp, desviacion=sd,
        tolerancia_puerta3=2.30, veredicto=v,
        alcance="ninguna cifra entra en ningun paper",
        segundos=time.time() - t0), indent=1))
    print("\nescrito -> %s (%.2f h)" % (SALIDA.relative_to(REPO),
                                        (time.time() - t0) / 3600), flush=True)


if __name__ == "__main__":
    main()
