#!/usr/bin/env python3
"""barrido_omega_b.py — el barrido de candidatos del que salió ω_b = (π−φ)/(3Ω²) (2026-10-16).

POR QUE. Paper 4 decía que la fórmula de ω_b «se eligió entre un puñado de monomios φ,π
comparados con Planck (un barrido temprano, archivado sin log)». El barrido SÍ existe:
es el paso [5] de archive/codigo/investigacion/open_problems/ssee_op1_baryon_density.py
(7 candidatos, citado en OPEN_PROBLEMS.md OP-1). Lo que faltaba era un log con acta. Este
script reproduce ese paso tal cual (mismas 7 expresiones, mismo dato) y lo sella, para que
la frase de P4 apunte a algo verificable. La lectura fría de P4 lo marcó.

LO QUE MIDE. Para cada candidato: valor y distancia a Planck en σ. Es una afirmación de
SELECCIÓN, no una derivación: con 7 candidatos, uno a <1σ es lo que se eligió. Por eso se
escribe el número de candidatos junto al resultado.

Nota: el script archivado imprime «3(π−φ)/φ¹¹ sigue siendo 1.8σ»; el cálculo da 3.98σ
(su propia tabla). Aquí sólo se escribe lo calculado.

Salida: results/logs/p04_barrido_omega_b.json (con acta).
"""
import json
import os
import sys

_R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import con_acta  # noqa: E402
from ssee_core import PHI, PI, OMEGA, K_V, T_R, MIRA, OMEGA_B_H2  # noqa: E402

ARCHIVADO = os.path.join(_R, "archive", "codigo", "investigacion", "open_problems",
                         "ssee_op1_baryon_density.py")
# ORIGEN-VALOR: 0.02237, 0.00015 — Planck 2018 VI Tabla 2 (el mismo dato del barrido archivado)
WB_PLANCK, SIG_PLANCK = 0.02237, 0.00015

D = PI - PHI
candidatos = {
    "(pi-phi)/(3 Omega^2)":      D / (3 * OMEGA**2),
    "3(pi-phi)/200":             3 * D / 200,
    "(pi-phi)/phi^11":           D / PHI**11,
    "3(pi-phi)/phi^11":          3 * D / PHI**11,
    "(pi-phi)/(Omega K_v)":      D / (OMEGA * K_V),
    "(pi-phi)^2/(MIRA Omega^3)": D**2 / (MIRA * OMEGA**3),
    "(pi-phi)/(T_r MIRA)":       D / (T_R * MIRA),
}
tabla = [dict(expresion=k, valor=v, sigma=abs(v - WB_PLANCK) / SIG_PLANCK)
         for k, v in candidatos.items()]
tabla.sort(key=lambda r: r["sigma"])
bajo_1s = [r["expresion"] for r in tabla if r["sigma"] < 1]
elegido = tabla[0]

# control: el elegido es la fórmula que usa el modelo
control = elegido["expresion"] == "(pi-phi)/(3 Omega^2)" and abs(elegido["valor"] - OMEGA_B_H2) < 1e-15

for r in tabla:
    print(f"  {r['expresion']:28s} {r['valor']:.6f}  {r['sigma']:8.2f} sigma")
print(f"\n  candidatos {len(tabla)}   bajo 1 sigma: {bajo_1s}   segundo mejor "
      f"{tabla[1]['sigma']:.2f} sigma   control {'PASA' if control else 'FALLA'}")

json.dump(con_acta(dict(
    que="barrido de candidatos phi,pi para omega_b frente a Planck (paso [5] del script OP-1 archivado)",
    dato=dict(omega_b_planck=WB_PLANCK, sigma=SIG_PLANCK, fuente="Planck 2018 VI Tabla 2"),
    n_candidatos=len(tabla),
    n_bajo_1sigma=len(bajo_1s),
    elegido=elegido["expresion"], elegido_sigma=elegido["sigma"],
    segundo=tabla[1]["expresion"], segundo_sigma=tabla[1]["sigma"],
    tabla=tabla,
    lectura="seleccion entre candidatos, no derivacion; el residuo es OP-1",
    control_pasa=control,
), __file__, entradas=[ARCHIVADO]),
    open(os.path.join(_R, "results", "logs", "p04_barrido_omega_b.json"), "w"), indent=1, ensure_ascii=False)
if not control:
    sys.exit("CONTROL FALLA")
