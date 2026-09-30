#!/usr/bin/env python3
"""reframe_obh2.py — Ω_b h² del posterior del reframe (prior H_glob), con su error.

POR QUÉ (2026-09-29). mcmc_paper2_reframe.json guarda la mediana de Ω_b h² pero no su
error, y Sealed/PRD citan «Ω_b h² = x ± σ». Aquí se lee la MISMA cadena (la guardada
por ssee_paper2_mcmc_reframe.py) y se resume igual que ese script (sin quemado: el
script resume la cadena completa del muestreador). CONTROL: la mediana de H0 que sale
aquí tiene que coincidir con la del json; si no, no se escribe nada.
Salida: results/logs/mcmc_paper2_reframe_obh2.json
"""
import json, os, sys
import numpy as np
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
src = open(os.path.join(R, "src", "p02_mcmc", "ssee_paper2_mcmc_reframe.py")).read()
_v = src.split("\nN_W, N_S, N_B, SAVE = ")[1].split("\n")[0].split(",")
N_W, N_S = int(_v[0]), int(_v[1])   # el quemado N_B ya se descartó con sampler.reset()
ck = src.split('CKPT = _SSEE_DATA + "')[1].split('"')[0]
c = np.load("/mnt/datos/SSEE_data" + ck)["chain"][-N_W * N_S:]
js = json.load(open(os.path.join(R, "results", "logs", "mcmc_paper2_reframe.json")))
h = float(np.median(c[:, 0]))
if abs(h - js["H0_mediana"]) > 1e-9:
    sys.exit(f"CONTROL FALLA: mediana H0 {h} != json {js['H0_mediana']}")
ob = c[:, 1]; p16, p50, p84 = np.percentile(ob, [16, 50, 84])
sys.path.insert(0, os.path.join(R, "src"))
from ssee_core import OMEGA_B_H2  # noqa: E402
out = dict(sigmas_a_obh2_algebraico=float((OMEGA_B_H2 - p50) / np.std(ob)), obh2_algebraico=OMEGA_B_H2, fecha=str(__import__("datetime").date.today()), control_H0_mediana=h, obh2_mediana=float(p50),
           obh2_p16=float(p16), obh2_p84=float(p84), obh2_std=float(np.std(ob)), filas=int(len(c)))
json.dump(out, open(os.path.join(R, "results", "logs", "mcmc_paper2_reframe_obh2.json"), "w"), indent=1)
print(f"  a ω_b algebraico {OMEGA_B_H2}: {(OMEGA_B_H2-p50)/np.std(ob):.2f}σ")
print(f"  control H0 = {h:.4f} (json {js['H0_mediana']:.4f})  Ω_b h² = {p50:.5f} +{p84-p50:.5f}/-{p50-p16:.5f}")
