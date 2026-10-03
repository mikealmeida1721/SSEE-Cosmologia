#!/usr/bin/env python3
"""op19_adm_masa.py — OP-19, primera prueba barata: ¿la masa de una materia oscura asimétrica separa SSEE de LCDM? (2026-10-03)

POR QUE. OP-19 busca el mecanismo detrás de omega_c = KAL0*omega_b*n_s. La familia
que liga omega_c a omega_b de forma natural es la materia oscura ASIMETRICA (ADM):
la misma asimetría que deja bariones deja materia oscura, con razón de números
r = n_DM/n_b. Entonces
    omega_c / omega_b = r * m_DM / m_b     =>     m_DM = (omega_c/omega_b) * m_b / r,
con m_b la masa media por barión. Con r = 1 sale la cifra de «~5 GeV» que se cita
para ADM. La pregunta de esta prueba NO es si existe esa partícula: es si esa masa
sirve para distinguir SSEE de LCDM, o sea, si una búsqueda directa a ~5 GeV pondría
a prueba algo propio de SSEE.

CONTROL (R53), del otro lado. La misma cuenta con el omega_c/omega_b de LCDM-Planck
(lcdm_planck.py, Planck 2018 VI Tabla 2). Si las dos masas casi coinciden, la masa
ADM NO es una predicción de SSEE: la daría cualquier cosmología con ese cociente.
Además se exige que el cociente de SSEE sea exactamente KAL0*n_s (identidad), y que
un cociente falso (el de LCDM) NO lo sea.

QUE NO SE DECIDE AQUI. r no sale del álgebra de SSEE: si se eligiera para acertar
un blanco, sería una perilla (regla 1 de OP-19). Por eso se reporta m_DM*r, y la
dependencia en r se deja explícita.

Masa media por barión: m_b = (1-Y_p)*m_H + Y_p*m_He4/4, con Y_p de CAMB (BBN) leído
de cajones_algebra.json y las masas de CODATA (scipy.constants). Con m_p sola el
resultado cambia menos de 0.2 %; se reportan las dos.

Salida: results/logs/op19_adm_masa.json
"""
import json
import os
import sys

from scipy.constants import physical_constants as pc

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
sys.path.insert(0, os.path.join(_R, "src", "p11_sondas"))
from ssee_core import OMEGA_B_H2, OMEGA_C_H2, KAL0, N_S  # noqa: E402
from lcdm_planck import LCDM_PLANCK  # noqa: E402
from procedencia import con_acta  # noqa: E402

CAJ = os.path.join(_R, "results", "logs", "cajones_algebra.json")
OUT = os.path.join(_R, "results", "logs", "op19_adm_masa.json")


Yp = json.load(open(CAJ))["identidades"]["Yp_BBN_camb"]["valor"]
GeV = 1e-3
m_p = pc["proton mass energy equivalent in MeV"][0] * GeV
m_e = pc["electron mass energy equivalent in MeV"][0] * GeV
m_H = m_p + m_e                                    # átomo de H (la ligadura de 13.6 eV no cuenta a esta precisión)
m_He4 = pc["alpha particle mass energy equivalent in MeV"][0] * GeV + 2 * m_e
m_b = (1 - Yp) * m_H + Yp * m_He4 / 4


def masas(wc, wb):
    q = wc / wb
    return {"omega_c": wc, "omega_b": wb, "cociente": q,
            "m_DM_por_r_GeV": q * m_b, "m_DM_por_r_GeV_solo_mp": q * m_p}


ssee = masas(OMEGA_C_H2, OMEGA_B_H2)
lcdm = masas(LCDM_PLANCK["omch2"], LCDM_PLANCK["ombh2"])
dif_rel = ssee["m_DM_por_r_GeV"] / lcdm["m_DM_por_r_GeV"] - 1

# --- control R53 -------------------------------------------------------------
ident_ssee = abs(ssee["cociente"] - KAL0 * N_S) < 1e-12
ident_lcdm = abs(lcdm["cociente"] - KAL0 * N_S) < 1e-12
assert ident_ssee and not ident_lcdm, "la identidad tiene que valer para SSEE y NO para el cociente de LCDM"

res = {
    "fecha": "2026-10-03",
    "pregunta": "¿la masa ADM (r = n_DM/n_b) separa SSEE de LCDM?",
    "m_b_GeV": m_b, "m_p_GeV": m_p, "Yp_camb": Yp,
    "ssee": ssee, "lcdm_planck": lcdm,
    "diferencia_relativa_masa": dif_rel,
    "control": {"cociente_ssee_es_KAL0_ns": ident_ssee, "cociente_lcdm_es_KAL0_ns": ident_lcdm, "pasa": True},
    "dependencia_r": {str(r): ssee["m_DM_por_r_GeV"] / r for r in (0.5, 1.0, 2.0)},
    "lectura": ("Con r=1 las dos cosmologías dan la misma masa ADM salvo por la diferencia relativa "
                "de esta clave; una búsqueda directa no resuelve esa diferencia. La masa ADM pone a "
                "prueba la familia ADM, no a SSEE. Lo propio de SSEE es que el cociente está fijado "
                "(KAL0*n_s); sólo un mecanismo que prediga r y m_DM a partir del álgebra lo haría medible."),
}
json.dump(con_acta(res, __file__, entradas=[CAJ]), open(OUT, "w"), indent=1, ensure_ascii=False)
print(f"m_b = {m_b:.6f} GeV (Y_p={Yp:.6f})")
print(f"SSEE : omega_c/omega_b = {ssee['cociente']:.6f} = KAL0*n_s -> m_DM*r = {ssee['m_DM_por_r_GeV']:.4f} GeV")
print(f"LCDM : omega_c/omega_b = {lcdm['cociente']:.6f}            -> m_DM*r = {lcdm['m_DM_por_r_GeV']:.4f} GeV")
print(f"diferencia relativa de masa: {dif_rel*100:+.3f} %   control: identidad SSEE sí, LCDM no -> PASA")
