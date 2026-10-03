"""El termino de VOLUMEN de la cadena de BOSS, medido (lo pidio Mike)

QUE SE ENCONTRO. El desplazamiento del A_s de BOSS (marginal 2.7636 contra
perfil 2.9448) no es «media contra moda de la misma superficie»: mi diagnostico
anterior comparo ambas cosas DENTRO de la cadena y no vio nada (0.07 sigma), y
por eso FALLO su control. La razon es que **las dos superficies son distintas**.

`boss_lpt_R1R2.chi2_marg_set` L262-291 devuelve

    chi2_cadena  =  c(lambda_hat)  +  ln det F        con  F = T^T C^-1 T + Lambda

`ln det F` es el logaritmo del VOLUMEN que les queda a las tres molestias
lineales (a0, a2, sn) una vez integradas. Y las plantillas llevan T ∝ e^logA
(L277), asi que ese volumen DEPENDE DE A_s. La cadena paga por subir A_s un
castigo que no viene del ajuste: viene de que arriba las molestias tienen menos
sitio. El perfil minimiza en vez de integrar, y no lleva ese termino.

Esto es el efecto de volumen, no como analogia sino como una linea de codigo.

LO QUE SE MIDE AQUI. La pendiente d(ln det F)/d(logA) sumada a los 6 conjuntos,
y el desplazamiento que esa pendiente predice:

    desplazamiento  =  pendiente / curvatura_del_perfil        (minimo de una
    parabola desplazada por un termino lineal; curvatura = 2/sigma_perfil^2)

y se compara contra el desplazamiento REALMENTE observado (perfil - marginal,
leido de R1R2_boss_lpt_cobaya.json#perfil_vs_marginal).

CONTROL (R53, va PRIMERO por R24). El algebra predice la pendiente sin correr
nada: F es 3x3 y T ∝ e^logA, luego det F ∝ e^(6 logA) SI el termino de dato
domina sobre Lambda; con 6 conjuntos la pendiente seria 36. La medida tiene que
caer en (0, 36]: positiva (o el mecanismo no empuja hacia abajo) y no mayor que
el techo algebraico (o algo esta mal leido). Si sale fuera, se aborta.

FUENTE: results/logs/growth_2026-07/termino_volumen_boss.json
"""
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "p06_growth"))

import boss_lpt_R1R2 as B                                      # noqa: E402

SALIDA = REPO / "results" / "logs" / "growth_2026-07" / "termino_volumen_boss.json"

TECHO = 36.0          # 6 conjuntos x 3 molestias x 2 (T^2) = pendiente maxima
# Leidos del log VIGENTE de BOSS (2026-10-03). Antes iban tecleados: 0.18115
# era perfil - marginal con la cadena BOSS del 09-08 (marginal 2.7636, m_nu de
# LCDM); la re-corrida del 10-01 con los ingredientes de SSEE da 2.7614, y el
# desplazamiento pasa a 0.1834. El literal no se entero (R65, «un literal no se
# entera de que su fuente cambio»).
_PVM = json.load(open(REPO / "results" / "logs" / "growth_2026-07"
                      / "R1R2_boss_lpt_cobaya.json"))["perfil_vs_marginal"]
OBSERVADO = _PVM["perfil_logA"] - _PVM["marginal_logA"]
SIG_PERFIL = _PVM["perfil_sigma"]
REJILLA = np.linspace(2.70, 3.10, 9)


def main():
    sets = B.build()
    print("  %d conjuntos construidos" % len(sets), flush=True)

    # Las (b1,b2,bs) se dejan en su arranque y FIJAS: lo que se mide es la
    # dependencia del termino de volumen con logA, no el ajuste.
    th3 = [1.0, 0.0, 0.0]

    ld_tot, c_tot = [], []
    for a in REJILLA:
        ld, cc = 0.0, 0.0
        for st in sets:
            chi2m, lam = B.chi2_marg_set(st, 'SSEE', float(a), th3)
            if lam is None:
                print("    AVISO: conjunto en la pared a logA=%.3f" % a)
                continue
            # chi2_marg = c + ln det F  ->  se separa recalculando ln det F
            T = B.templates(st, 'SSEE') * np.exp(float(a))
            F = T.T @ (st['Cinv'] @ T) + B._LAMBDA
            _, l = np.linalg.slogdet(F)
            ld += float(l)
            cc += float(chi2m) - float(l)
        ld_tot.append(ld)
        c_tot.append(cc)
        print("    logA=%.3f   ln det F = %10.4f   c = %12.4f" % (a, ld, cc),
              flush=True)

    ld_tot = np.array(ld_tot)
    pend = float(np.polyfit(REJILLA, ld_tot, 1)[0])
    resid = float(np.max(np.abs(np.polyval(np.polyfit(REJILLA, ld_tot, 1),
                                           REJILLA) - ld_tot)))

    # --- CONTROL PRIMERO (R24) --------------------------------------------
    pasa = 0.0 < pend <= TECHO
    print("\n" + "=" * 70)
    print("  CONTROL: la pendiente cae en (0, %.0f], el techo algebraico?" % TECHO)
    print("     pendiente medida = %.4f   ->  %s" % (pend, "PASA" if pasa else "FALLA"))
    print("     (recta ajusta con residuo maximo %.4f)" % resid)
    print("=" * 70, flush=True)

    curv = 2.0 / SIG_PERFIL ** 2
    pred = pend / curv

    sal = dict(
        corrida="medir el termino de volumen ln det F de la cadena de BOSS",
        mecanismo="boss_lpt_R1R2.chi2_marg_set L262-291 devuelve c + ln det F; "
                  "F = T^T Cinv T + Lambda con T ∝ e^logA (L277), asi que el "
                  "volumen de las molestias lineales depende de A_s",
        control=dict(criterio="0 < pendiente <= %.0f (techo algebraico: F es "
                              "3x3, T ∝ e^logA, 6 conjuntos)" % TECHO,
                     pendiente=pend, residuo_recta=resid, pasa=bool(pasa)),
        rejilla=REJILLA.tolist(), ln_det_F=ld_tot.tolist(), c=c_tot,
        alcance="mide de donde sale el desplazamiento. NO dice cual estimador "
                "es insesgado — eso es la cola #23, con dato sintetico")
    if not pasa:
        sal["veredicto"] = "pendiente fuera del rango algebraico: algo mal leido"
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        SALIDA.write_text(json.dumps(sal, indent=1))
        print("\nescrito -> %s" % SALIDA.relative_to(REPO), flush=True)
        return

    sal["prediccion"] = dict(
        curvatura_perfil=curv, sigma_perfil=SIG_PERFIL,
        desplazamiento_predicho=pred, desplazamiento_observado=OBSERVADO,
        razon=pred / OBSERVADO)
    print("\n  curvatura del perfil  2/sigma^2 = %.2f" % curv)
    print("  desplazamiento PREDICHO por el volumen = %.4f" % pred)
    print("  desplazamiento OBSERVADO               = %.4f" % OBSERVADO)
    print("  razon predicho/observado               = %.2f" % (pred / OBSERVADO))
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(sal, indent=1))
    print("\nescrito -> %s" % SALIDA.relative_to(REPO), flush=True)


if __name__ == "__main__":
    main()
