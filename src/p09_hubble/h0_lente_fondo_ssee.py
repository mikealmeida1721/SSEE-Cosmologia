#!/usr/bin/env python3
"""¿Cuanto mueve el fondo de SSEE la H0 que infiere una lente con retraso?

POR QUE EXISTE (2026-09-19, conversacion Castor-Max sobre SN Encore/Requiem).
Las H0 por retraso temporal (Encore, TDCOSMO) se publican ASUMIENDO la forma de
expansion de LCDM plano. Con el retraso medido fijo, H0 es proporcional a la
distancia de retraso adimensional
    F = (1+z_l) chi(0,z_l) chi(0,z_s) / chi(z_l,z_s)     (plano, en c/H0)
asi que la misma medicion leida con el fondo de SSEE (w0, wa del nucleo) da
    H0_SSEE = H0_LCDM * F_SSEE / F_LCDM.
Esto importa para la PREDICCION FECHADA de Requiem: la cascada predice que la
expansion global es H_global; un analisis LCDM de esa misma lente reportaria
H_global / (F_SSEE/F_LCDM), no H_global.

Aproximacion declarada: Omega_m igual en los dos (el de SSEE); en un analisis
real Omega_m se marginaliza con sus priors. Es el efecto de FORMA a primer
orden, no una re-inferencia.

Se corre solo:  python3 src/p09_hubble/h0_lente_fondo_ssee.py
"""
import json
import pathlib
import sys

import numpy as np
from scipy.integrate import quad

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
import ssee_core as S  # noqa: E402
from procedencia import con_acta  # noqa: E402

SALIDA = REPO / "results" / "logs" / "h0_lente_fondo_ssee.json"   # 2026-10-03: era .log con JSON dentro y R75 no leia su acta
OM = S.OMEGA_M_TOTAL
H_GLOBAL = S.H0_GLOBAL                   # H_glob = H_SH0ES*(1-f_screen): el H de SSEE (el blanco puro es S.H0_ALG)


def _canon(clave):
    """Lee un valor de CANONICAL_VALUES.yaml (fuente unica), a cualquier nivel."""
    import yaml
    def busca(d):
        if isinstance(d, dict):
            if clave in d:
                return d[clave]
            for v in d.values():
                r = busca(v)
                if r is not None:
                    return r
        return None
    return float(busca(yaml.safe_load((REPO / "CANONICAL_VALUES.yaml").read_text())))


H_SH0ES = _canon("H0_SH0ES_km_s_Mpc")    # MEDIDO (Riess+2022), la entrada de la cascada

# Sistemas: (nombre, z_lente, z_fuente, fuente del dato)
SISTEMAS = [
    ("Encore/Requiem, MACS J0138.0-2155", 0.336, 1.949, "arXiv:2509.12301"),
    ("cuasar tipico TDCOSMO", 0.5, 2.0, "orden de magnitud, no un sistema"),
]
# H0 publicadas en LCDM plano: (nombre, H0, +err, -err, fuente)
PUBLICADAS = [
    ("SN Encore", 66.9, 11.2, 8.1, "arXiv:2509.12301"),
    ("TDCOSMO-2025", 71.6, 3.9, 3.3, "arXiv:2506.03023"),
    ("TDCOSMO IV solo", 74.5, 5.6, 6.1, "arXiv:2007.02941"),
    ("TDCOSMO IV + SLACS", 67.4, 4.1, 3.2, "arXiv:2007.02941"),
    ("H0LiCOW XIII", 73.3, 1.7, 1.8, "arXiv:1907.04869"),
]


def E(z, w0, wa):
    a = 1 / (1 + z)
    de = (1 - OM) * a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
    return np.sqrt(OM * (1 + z) ** 3 + de)


def chi(z1, z2, w0, wa):
    return quad(lambda z: 1 / E(z, w0, wa), z1, z2)[0]


def F(zl, zs, w0, wa):
    return (1 + zl) * chi(0, zl, w0, wa) * chi(0, zs, w0, wa) / chi(zl, zs, w0, wa)


def sigmas(v, c, up, lo):
    """Distancia en sigma usando el brazo del lado donde cae v."""
    return (v - c) / (up if v > c else lo)


def main():
    out = {"Omega_m": OM, "w0": S.W0, "wa": S.WA, "H_global": H_GLOBAL, "H_SH0ES": H_SH0ES,
           "sistemas": [], "publicadas": []}
    r_enc = None
    for nom, zl, zs, fu in SISTEMAS:
        r = F(zl, zs, S.W0, S.WA) / F(zl, zs, -1.0, 0.0)
        r_enc = r if r_enc is None else r_enc
        out["sistemas"].append(dict(nombre=nom, z_l=zl, z_s=zs, fuente=fu,
                                    razon_H0_SSEE_sobre_LCDM=r,
                                    H_global_leido_en_LCDM=H_GLOBAL / r))
        print(f"  {nom:36s} H0_SSEE/H0_LCDM = {r:.4f}   "
              f"H_global leido por un analisis LCDM = {H_GLOBAL / r:.2f}")
    r_q = out["sistemas"][1]["razon_H0_SSEE_sobre_LCDM"]
    print()
    for nom, h, up, lo, fu in PUBLICADAS:
        r = r_enc if "Encore" in nom else r_q
        hs, ups, los = h * r, up * r, lo * r
        d_lcdm = sigmas(H_GLOBAL, h, up, lo)
        d_ssee = sigmas(H_GLOBAL, hs, ups, los)
        d_sh0es = sigmas(H_SH0ES, h, up, lo)
        out["publicadas"].append(dict(nombre=nom, H0_LCDM=h, mas=up, menos=lo,
                                      fuente=fu, H0_con_fondo_SSEE=hs,
                                      sigma_Hglobal_leida_LCDM=d_lcdm,
                                      sigma_Hglobal_leida_SSEE=d_ssee,
                                      sigma_SH0ES=d_sh0es))
        print(f"  {nom:20s} {h:5.1f} -> con fondo SSEE {hs:6.2f}   "
              f"H_global a {abs(d_lcdm):.2f}s (LCDM) / {abs(d_ssee):.2f}s (SSEE);  "
              f"SH0ES a {abs(d_sh0es):.2f}s")
    # FECHA de reaparicion de Requiem. arXiv:2509.12319 (resumen), cuatro mejores
    # modelos, 1 sigma: H0=73 -> abril-diciembre 2026; H0=67 -> marzo-noviembre
    # 2027. A modelo de lente fijo el retraso escala como 1/H0, asi que se
    # interpola en 1/H0 entre los CENTROS de las dos ventanas (ano decimal, mitad
    # de mes). Es una lectura de la prediccion publicada, no un modelo propio.
    VENT = {73.0: (2026 + 3.5 / 12, 2026 + 11.5 / 12),     # abr..dic 2026
            67.0: (2027 + 2.5 / 12, 2027 + 10.5 / 12)}     # mar..nov 2027
    c73, c67 = (sum(VENT[73.0]) / 2, sum(VENT[67.0]) / 2)
    def fecha(h):
        f = (1 / h - 1 / 73.0) / (1 / 67.0 - 1 / 73.0)
        return c73 + f * (c67 - c73)
    def mes(t):
        a = int(t); m = int((t - a) * 12) + 1
        return f"{a}-{m:02d}"
    h_lcdm = out["sistemas"][0]["H_global_leido_en_LCDM"]
    out["requiem_fecha"] = dict(
        fuente="arXiv:2509.12319 (ventanas 1 sigma); interpolacion en 1/H0 entre centros",
        centro_H73=mes(c73), centro_H67=mes(c67),
        SSEE_leida_LCDM=dict(H0=h_lcdm, fecha=mes(fecha(h_lcdm))),
        SH0ES=dict(H0=H_SH0ES, fecha=mes(fecha(H_SH0ES))),
        # Lectura P (OP-8b, Mike, registrada 2026-10-03): el apantallamiento lo ve TODO metodo
        # local, la lente incluida, asi que la lente lee el valor local H_glob/(1-f) = H_SH0ES
        # con el fondo de SSEE; un analisis LCDM plano reporta eso dividido por la razon.
        P_plano_leida_LCDM=dict(H0=H_SH0ES / out["sistemas"][0]["razon_H0_SSEE_sobre_LCDM"],
                                fecha=mes(fecha(H_SH0ES / out["sistemas"][0]["razon_H0_SSEE_sobre_LCDM"]))),
        nota="la ventana de cada centro es de ~+-4 meses (incertidumbre del modelo de lente)")
    print(f"\n  Requiem, centro de la ventana: SSEE (LCDM-leido {h_lcdm:.2f}) -> "
          f"{mes(fecha(h_lcdm))};  SH0ES ({H_SH0ES}) -> {mes(fecha(H_SH0ES))}")
    SALIDA.write_text(json.dumps(con_acta(out, __file__, entradas=[REPO / "CANONICAL_VALUES.yaml"]), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  escrito en {SALIDA.relative_to(REPO)}")


if __name__ == "__main__":
    main()
