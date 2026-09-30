#!/usr/bin/env python3
"""h0_distancias.py — distancias en σ del H₀ que mide DESI al H_glob de SSEE y a Planck.

POR QUÉ EXISTE (2026-09-29). results/logs/h0_distancias_hglob.json se escribió el
28-sep sin script que lo reprodujera. Este lo regenera LEYENDO los logs:
  posterior (prior H_glob)   ← results/logs/mcmc_paper2_reframe.json
  DESI sola, prior plano      ← results/logs/h0_four_priors.json [plano]
  H_glob ± σ                  ← ssee_core (SH0ES·(1−f_screen), σ propagado)
  Planck H₀                   ← ssee_paper2_mcmc.PLANCK_H0 (Planck 2018 VI)

CONVENCIONES (las de los papers):
  a H_glob: (H_glob − H₀)/σ_posterior   — H_glob es la PREDICCIÓN; se mide
            cuántas σ del dato la separan (la misma cuenta que daba el 0.50σ viejo).
  a Planck: |H₀ − H_Planck| / sqrt(σ² + σ_Planck²) — dos medidas, σ en cuadratura.
Salida: results/logs/h0_distancias_hglob.json
"""
import json, os, sys
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "src"))
from ssee_core import H0_GLOBAL, SIG_H0_GLOBAL  # noqa: E402
L = os.path.join(R, "results", "logs")
post = json.load(open(os.path.join(L, "mcmc_paper2_reframe.json")))
plano = json.load(open(os.path.join(L, "h0_four_priors.json")))["plano"]
src = open(os.path.join(R, "src", "p02_mcmc", "ssee_paper2_mcmc.py")).read()
HP, SP = eval(src.split("PLANCK_H0   = ")[1].split("\n")[0])   # la tupla tal cual está en el código


def fila(h, s):
    return dict(H0=h, sd=s, sigmas_a_Hglob=(H0_GLOBAL - h) / s,
                sigmas_a_Planck=abs(h - HP) / (s * s + SP * SP) ** 0.5)


res = dict(fecha=str(__import__("datetime").date.today()), H_glob=H0_GLOBAL, sig_H_glob=SIG_H0_GLOBAL,
           Planck=dict(H0=HP, sd=SP), posterior=fila(post["H0_mediana"], post["H0_std"]),
           desi_plano=fila(plano["H0_mediana"], plano["H0_std"]), script="src/p02_mcmc/h0_distancias.py")
# DESI sola frente al posterior completo (dos estimaciones del mismo dato; σ en cuadratura, orientativo)
res["plano_vs_posterior_sigmas"] = abs(res["desi_plano"]["H0"] - res["posterior"]["H0"]) / (
    res["desi_plano"]["sd"] ** 2 + res["posterior"]["sd"] ** 2) ** 0.5
json.dump(res, open(os.path.join(L, "h0_distancias_hglob.json"), "w"), indent=1)
for k in ("posterior", "desi_plano"):
    f = res[k]
    print(f"  {k:11s} H0 = {f['H0']:.3f} ± {f['sd']:.3f}   a H_glob {f['sigmas_a_Hglob']:.2f}σ   a Planck {f['sigmas_a_Planck']:.2f}σ")
print(f"  DESI sola vs posterior: {res['plano_vs_posterior_sigmas']:.2f}σ")
