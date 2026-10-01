"""El techo de sigma8 con A_s FIJADO a Planck: 0.814854, no 0.8335.

QUE CONTESTA EL NUMERO. Cuanta estructura da el fondo de SSEE si la amplitud
primordial A_s se HEREDA de Planck en vez de ajustarse. **No es una prediccion
del modelo**: A_s es uno de los dos libres del sector CMB (k=2), asi que
clavarlo al valor de Planck importa una inferencia hecha dentro de LCDM, y con
ella la discrepancia Planck-cizalla. Por eso el "3.5 sigma" que salia de aqui
era artefacto del condicionamiento. El resultado vivo es el otro: con A_s libre
contra el xi_pm CRUDO de KiDS-1000, S8 = 0.7555 +/- 0.0192, 0.11 sigma
(Paper 6, R3). Esto es DIAGNOSTICO bajo condicion declarada.

HISTORIA, porque el numero cambio (2026-09-08). Los papers publicaban
sigma8 = 0.8335 / S8 = 0.846. Salia de `class_ssee/output/can_cold__pk.dat`, un
fichero que:
  · no tenia `.ini` — no constaba con que se corrio;
  · estaba FUERA del repositorio (`class_ssee/output/` en .gitignore);
  · era del mismo minuto que `can_part__pk.dat`, la corrida de dos sectores con
    la particula retirada el 2026-08-01. El techo nacio como su comparacion.
Al re-correrlo con `.ini` versionado y el fondo canonico —que lleva NEUTRINOS
MASIVOS, Sum m_nu = 0.06849 eV— sale **0.814854**, un 2.3% por debajo. Los
neutrinos, por ligeros, viajan casi a c y no se dejan atrapar en los pozos: se
llevan un poco de grumo a 8 Mpc/h. Sin ellos sobra estructura.

COMO. sigma8^2 = (1/2pi^2) Int k^2 P(k) W^2(kR) dk, R = 8 Mpc/h,
W(x) = 3(sin x - x cos x)/x^3 (Peebles 1980), interpolando log-log a 4000
puntos porque la rejilla de CLASS no basta para el filtro.

CONTROL (R53), con el criterio escrito en `config/class/techo_lcdm_referencia.ini`
ANTES de correr: el mismo integrador sobre la linea base de Planck 2018 tiene
que dar sigma8 = 0.8111 +/- 0.006. Da **0.810851**, o sea 0.04 sigma. PASA, y
por tanto el metodo esta calibrado, no solo el numero de SSEE.
(El intento previo daba 0.8221, un 1.4% alto. La causa era la misma: a la
referencia LCDM guardada tambien le faltaban los neutrinos masivos.)

LO QUE NO ESTABLECE. La barra +/- 0.006 que arrastran los papers viene de antes
y NO se ha recomputado aqui.

FUENTE: results/logs/p5_techo_sigma8_As_fijo.json
"""
# ORIGEN-VALOR: 0.8221 — sigma8 del intento PREVIO, con la referencia LCDM
# sin neutrinos masivos. Numero de una corrida retirada, sin log propio: se
# conserva en el texto porque es la evidencia de cual era el fallo.
import json
import pathlib

import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from procedencia import con_acta  # noqa: E402
import ssee_core as S  # noqa: E402
EVID = REPO / "results" / "logs" / "p5_techo_evidencia"
# CANONICO desde 2026-09-08: .ini versionado y con neutrinos masivos
PK_SSEE = EVID / "techo_ssee_canonico__pk.dat"    # config/class/techo_ssee_canonico.ini
PK_LCDM = EVID / "techo_lcdm_referencia__pk.dat"  # config/class/techo_lcdm_referencia.ini
# RETIRADOS: la corrida vieja, sin .ini y sin neutrinos. Se conservan para poder
# recomputar el 0.8335 publicado y ensenar de donde salia el +2.3%. NO alimentan
# ningun numero canonico.
PK_SSEE_VIEJO = EVID / "can_cold__pk.dat"
PK_LCDM_VIEJO = EVID / "lcdm_planck2018__pk.dat"

SALIDA = REPO / "results" / "logs" / "p5_techo_sigma8_As_fijo.json"
R_TOPHAT = 8.0            # Mpc/h
N_INTERP = 4000
OM_CMB = S.OMEGA_M_TOTAL         # Omega_m,CMB = omega_m/h^2 (algebraico; era el literal 0.3088808787787524)
SIGMA8_PLANCK = 0.8111           # ORIGEN-VALOR: 0.8111 — Planck 2018 VI, Tabla 2, TT,TE,EE+lowE+lensing; criterio del control
SIGMA8_PLANCK_ERR = 0.006        # ORIGEN-VALOR: 0.006 — su barra, misma tabla


def sigma8(archivo):
    k, P = np.loadtxt(archivo, unpack=True)
    lk = np.log(k)
    kk = np.exp(np.linspace(lk[0], lk[-1], N_INTERP))
    PP = np.exp(np.interp(np.log(kk), lk, np.log(P)))
    x = kk * R_TOPHAT
    W = 3.0 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return float(np.sqrt(np.trapezoid(kk ** 2 * PP * W ** 2, kk) / (2 * np.pi ** 2)))


def main():
    s_ssee = sigma8(PK_SSEE)
    s_lcdm = sigma8(PK_LCDM)
    s_viejo = sigma8(PK_SSEE_VIEJO)
    s_lcdm_viejo = sigma8(PK_LCDM_VIEJO)
    S8 = s_ssee * (OM_CMB / 0.3) ** 0.5
    desv = abs(s_lcdm - SIGMA8_PLANCK) / SIGMA8_PLANCK_ERR
    pasa = desv < 2.0

    tens = {}
    # ORIGEN-VALOR: 0.759, 0.024 — KiDS-1000 Asgari+2021 (cota superior de su barra asimetrica)
    # ORIGEN-VALOR: 0.776, 0.017 — DES-Y3 3x2pt, Abbott+2022
    # ORIGEN-VALOR: 0.832, 0.013 — Planck 2018 VI, Tabla 2
    # ORIGEN-VALOR: 0.006 — barra heredada del techo (ver «no_establece» en la salida)
    for nom, val, err in [("KiDS-1000", 0.759, 0.024), ("DES-Y3", 0.776, 0.017),
                          ("Planck 2018", 0.832, 0.013)]:
        tens[nom] = abs(S8 - val) / np.sqrt(err ** 2 + 0.006 ** 2)

    out = {
        "corrida": "techo sigma8/S8 con A_s FIJADO a Planck — DIAGNOSTICO, no prediccion",
        "que_contesta": "cuanta estructura da el fondo de SSEE si A_s se hereda "
                        "de Planck en vez de ajustarse; A_s es libre en el modelo",
        "ini": "config/class/techo_ssee_canonico.ini",
        "fuente_Pk": str(PK_SSEE.relative_to(REPO)),
        "metodo": "top-hat R=8 Mpc/h, Peebles 1980; interp log-log a %d puntos"
                  % N_INTERP,
        "lleva_neutrinos_masivos": "si — Sum m_nu = 0.06849 eV",
        "sigma8_techo": s_ssee,
        "Omega_m_CMB": OM_CMB,
        "S8_techo": S8,
        "tensiones_S8_sigmas": tens,
        "control": {
            "criterio": "el mismo integrador sobre la baseline de Planck 2018 "
                        "debe dar sigma8 = 0.8111 +/- 0.006; escrito en el .ini "
                        "ANTES de correr",
            "ini": "config/class/techo_lcdm_referencia.ini",
            "sigma8_LCDM": s_lcdm,
            "desvio_sigmas": desv,
            "pasa": bool(pasa),
            "razon_SSEE_sobre_LCDM": s_ssee / s_lcdm,
        },
        "retirado_2026_09_08": {
            "publicado_como": [0.8335, 0.846],
            "sigma8_recomputado_del_Pk_viejo": s_viejo,
            "sigma8_LCDM_viejo": s_lcdm_viejo,
            "fuente_Pk": str(PK_SSEE_VIEJO.relative_to(REPO)),
            "razon": "corrida SIN .ini, FUERA del repo y SIN neutrinos masivos; "
                     "sin ellos sobra grumo a 8 Mpc/h. Su gemela del mismo "
                     "minuto es la corrida de dos sectores con la particula "
                     "retirada",
            "desvio_pct": 100.0 * (s_viejo / s_ssee - 1.0),
            "tensiones_que_citaba": {"KiDS-1000": 3.5, "DES-Y3": 3.9,
                                     "Planck 2018": 1.1},
        },
        "no_establece": "la barra +/- 0.006 de los papers viene de antes y no se "
                        "ha recomputado aqui",
        "superado_por": {
            "valor": "S8 = 0.7555 +/- 0.0192 (0.11 sigma vs KiDS-1000)",
            "log": "results/logs/growth_2026-07/R3_ssee_kids_S8.json",
            "razon": "A_s libre contra el dato crudo; el 3.5 sigma del techo era "
                     "artefacto de fijar A_s",
        },
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    INI = REPO / "config" / "class"
    SALIDA.write_text(json.dumps(con_acta(out, __file__, entradas=[
        str(p) for p in (PK_SSEE, PK_LCDM, PK_SSEE_VIEJO, PK_LCDM_VIEJO,
                         INI / "techo_ssee_canonico.ini", INI / "techo_lcdm_referencia.ini")]), indent=1))
    print("sigma8 techo (A_s fijo) = %.6f    [retirado: 0.8335]" % s_ssee)
    print("S8 techo                = %.6f    [retirado: 0.846]" % S8)
    print("tensiones S8: " + " · ".join("%s %.2f sig" % (k, v)
                                        for k, v in tens.items()))
    print("CONTROL  sigma8 LCDM   = %.6f  vs %.4f -> %.2f sigma  %s"
          % (s_lcdm, SIGMA8_PLANCK, desv, "PASA" if pasa else "FALLA"))
    print("del Pk viejo (sin neutrinos): %.6f  (+%.2f%%)"
          % (s_viejo, 100.0 * (s_viejo / s_ssee - 1.0)))
    print("escrito ->", SALIDA.relative_to(REPO))


if __name__ == "__main__":
    main()
