#!/usr/bin/env python3
"""cmb_dbic_mnu_propia.py — ΔBIC del CMB con ΛCDM en SU propia mν (0.06 eV).

El ΔBIC −26.21 (cmb_dbic_tau_ajustado.json) usaba para ΛCDM un χ² medido con
la mν de SSEE (0.06849). lcdm_conjunta.py cmb re-minimizó ΛCDM con mν 0.06
(Nelder-Mead, control: no peor que el arranque). Aquí solo se leen los dos
logs y se recalcula; N = 669 sale del log viejo (medido del likelihood).
"""
import json, math, os
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
viejo = json.load(open(f"{R}/results/logs/cmb_dbic_tau_ajustado.json"))
nuevo = json.load(open(f"{R}/results/logs/lcdm_conjunta_cmb.json"))
assert nuevo["convergido"] and nuevo["control_no_peor_que_arranque"]
s, l_viejo = viejo["SSEE"], viejo["LCDM"]
N = round(math.exp((s["BIC"] - s["chi2_min"]) / s["k"]))            # N que usó el log viejo
l = nuevo["chi2"]
out = dict(fecha="2026-09-28", N=N, chi2_ssee=s["chi2_min"], k_ssee=s["k"],
           chi2_lcdm_mnu006=l, chi2_lcdm_viejo_mnu_ssee=l_viejo["chi2_min"], k_lcdm=l_viejo["k"],
           dchi2=s["chi2_min"] - l, dchi2_viejo=s["chi2_min"] - l_viejo["chi2_min"],
           dBIC=(s["chi2_min"] + s["k"] * math.log(N)) - (l + l_viejo["k"] * math.log(N)),
           dBIC_viejo=s["BIC"] - l_viejo["BIC"], params_lcdm=nuevo["params"])
json.dump(out, open(f"{R}/results/logs/cmb_dbic_mnu_propia.json", "w"), indent=1)
for k in ("N", "chi2_ssee", "chi2_lcdm_mnu006", "chi2_lcdm_viejo_mnu_ssee", "dchi2", "dchi2_viejo", "dBIC", "dBIC_viejo"):
    print(f"  {k:26s} {out[k]}")
