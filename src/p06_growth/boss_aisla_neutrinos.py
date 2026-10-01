"""¿El A_s de BOSS se movio por los NEUTRINOS o por el METODO? (lo pidio Mike)

EL PROBLEMA. Al re-correr R1/R2 (cola #10) el logA de SSEE paso de
2.7636 +- 0.0981 a 2.9448 +- 0.1238 — 1.85 sigmas de su propia barra — y su
tension con el fondo cosmico cayo de 2.87 a 0.81 sigma. Pero **cambiaron DOS
cosas a la vez**:

  (1) la masa de neutrino dejo de estar prestada (SSEE pasa de 0.06 a 0.06849);
  (2) el metodo cambio: la vieja era una cadena MCMC de Cobaya, la nueva es un
      perfil por minimizacion a k_max = 0.200.

Con dos cambios simultaneos NO se puede decir «fue por los neutrinos». Esta
corrida separa las causas de la unica manera que vale: **misma maquina, mismo
metodo, mismo k_max, y se mueve UN SOLO ingrediente**.

QUE SE CORRE. Tres veces el MISMO perfil:
    A  canonico     SSEE con m_nu = 0.06849 (la suya)   <- reproduce la #10
    B  prestado     SSEE con m_nu = 0.06    (la de LCDM)
    C  repeticion   identico a A            <- prueba de REPRODUCIBILIDAD

  A - B  = el efecto LIMPIO de la masa de neutrino, a metodo fijo.
  A - C  = el ruido del propio metodo. Si no es ~0, nada de lo demas vale.
  (viejo MCMC) - A  = lo que queda, y eso es el efecto del METODO.

CONTROL (R53, y va PRIMERO por R24). La repeticion C tiene que devolver el
mismo logA que A hasta la 5a cifra. Si el metodo no se reproduce a si mismo,
ninguna diferencia medida despues significa nada y se aborta.

FUENTE: results/logs/growth_2026-07/boss_aisla_neutrinos.json
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "p06_growth"))

import boss_lpt_R1R2 as B                              # noqa: E402

SALIDA = REPO / "results" / "logs" / "growth_2026-07" / "boss_aisla_neutrinos.json"

# El valor que traia la version con el prestamo, y el de la cadena MCMC vieja.
# ORIGEN-VALOR: 0.0981 — sigma marginal de logA de la cadena SSEE con m_nu 0.06, archive/logs_superados/R1R2_boss_lpt_cobaya_20260908_mnu006.json (hoy 0.1010)
MNU_PRESTADA = 0.06
# ORIGEN: results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json      (el viejo, 2.7636 +- 0.0981)
# ORIGEN: results/logs/growth_2026-07/R1R2_boss_lpt_kmax0.200.json   (el nuevo, 2.9448 +- 0.1238)
VIEJO_MCMC = dict(logA=2.763639661108589, sig=0.09813161759644874,
                  fuente="results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json")


def corre(mnu):
    """Perfil de SSEE con la masa indicada. Todo lo demas, identico.

    `build()` lee COSMO al llamarse y construye ahi las tablas LPT, asi que la
    masa se cambia ANTES de construir y las tablas salen del fondo correcto.
    (Primera version: se le quitaba `lpt` a unos conjuntos ya construidos, lo
    que rompia `model_set` con KeyError. Verificado en el codigo, no supuesto:
    build() -> camb_lin(c, z) con c = COSMO[name].)
    """
    B.MNU['SSEE'] = mnu
    B.COSMO['SSEE']['mnu'] = mnu
    return B.run('SSEE', B.build())


def main():
    print("\n=== A · canonico  m_nu = %.5f (la de SSEE)" % B.S.SUM_MNU_EV, flush=True)
    A = corre(B.S.SUM_MNU_EV)
    print("    logA = %.5f +- %.5f   chi2 = %.3f" % (A["logA"], A["sig_logA"], A["chi2"]))

    print("\n=== C · REPETICION de A (control de reproducibilidad, va antes de leer nada)",
          flush=True)
    C = corre(B.S.SUM_MNU_EV)
    print("    logA = %.5f +- %.5f   chi2 = %.3f" % (C["logA"], C["sig_logA"], C["chi2"]))
    d_rep = abs(A["logA"] - C["logA"])
    ok = d_rep < 1e-5
    print("    |A - C| = %.2e   (criterio < 1e-5)  -> %s"
          % (d_rep, "PASA" if ok else "FALLA"), flush=True)
    if not ok:
        SALIDA.write_text(json.dumps(dict(
            control=dict(pasa=False, A=A["logA"], C=C["logA"], dif=d_rep),
            veredicto="el metodo no se reproduce a si mismo: no se mide nada"),
            indent=1))
        return

    print("\n=== B · con la masa PRESTADA  m_nu = %.5f (la de LCDM)" % MNU_PRESTADA,
          flush=True)
    Bb = corre(MNU_PRESTADA)
    print("    logA = %.5f +- %.5f   chi2 = %.3f" % (Bb["logA"], Bb["sig_logA"], Bb["chi2"]))

    d_nu = A["logA"] - Bb["logA"]
    d_tot = A["logA"] - VIEJO_MCMC["logA"]
    d_met = d_tot - d_nu

    print("\n" + "=" * 68)
    print("  DESCOMPOSICION del desplazamiento total (%.4f)" % d_tot)
    print("=" * 68)
    print("  por la MASA DE NEUTRINO (A - B, metodo fijo) = %+.4f  (%.0f%%)"
          % (d_nu, 100 * d_nu / d_tot if d_tot else 0))
    print("  por el METODO (lo que queda)                 = %+.4f  (%.0f%%)"
          % (d_met, 100 * d_met / d_tot if d_tot else 0))
    print("  en sigmas de la barra vieja (%.4f):" % VIEJO_MCMC["sig"])
    print("     neutrinos %.2f sigma   ·   metodo %.2f sigma"
          % (abs(d_nu) / VIEJO_MCMC["sig"], abs(d_met) / VIEJO_MCMC["sig"]),
          flush=True)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(dict(
        corrida="separar el efecto de la masa de neutrino del efecto del metodo",
        pregunta="M. Almeida — cuando algo cambia asi, aunque sea a mejor, se "
                 "reverifica antes de pasarlo al paper",
        control=dict(criterio="la repeticion devuelve el mismo logA a <1e-5",
                     A=A["logA"], C=C["logA"], dif=d_rep, pasa=True),
        A_canonico=dict(mnu=B.S.SUM_MNU_EV, **{k: A[k] for k in
                        ("logA", "sig_logA", "chi2", "dof")}),
        B_prestada=dict(mnu=MNU_PRESTADA, **{k: Bb[k] for k in
                        ("logA", "sig_logA", "chi2", "dof")}),
        viejo_mcmc=VIEJO_MCMC,
        descomposicion=dict(total=d_tot, por_neutrinos=d_nu, por_metodo=d_met,
                            frac_neutrinos=d_nu / d_tot if d_tot else None,
                            frac_metodo=d_met / d_tot if d_tot else None),
        alcance="mide de que fue el desplazamiento. NO decide si el numero "
                "nuevo entra en Paper 6 — eso es decision de Mike"), indent=1))
    print("\nescrito -> %s" % SALIDA.relative_to(REPO), flush=True)


if __name__ == "__main__":
    main()
