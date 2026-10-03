#!/usr/bin/env python3
"""regenerate_corners_p2.py — los tres corner plots del MCMC de 3 modelos de Paper 2 (2026-10-03).

POR QUE. ssee_paper2_mcmc.py dibuja los corners al final de un MCMC de ~2 h. El
2026-10-02 ese script cambió (los cronómetros pasan a leerse del CSV), y R36 marcó
los tres corners como más viejos que su script. Los corners sólo dependen de las
cadenas guardadas (mcmc_chains_professional.npz), no de los cronómetros, así que se
regeneran aquí desde el npz con las MISMAS llamadas a `corner.corner` que el MCMC
(sección 9), sin re-muestrear. fig_corner_lcdm_professional entra en Paper 2.

Salida: results/figures/fig_corner_{ssee,lcdm,cpl}_professional.pdf, con el acta en
los metadatos del PDF.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import corner  # noqa: E402

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import acta  # noqa: E402

NPZ = "/mnt/datos/SSEE_data/mcmc/paper2_3models/mcmc_chains_professional.npz"
OUT = os.path.join(_R, "results", "figures")
ETIQ = {"ssee": ([r"$H_0$", r"$\Omega_b h^2$"], "SSEE"),
        "lcdm": ([r"$H_0$", r"$\Omega_m$", r"$\Omega_b h^2$"], "ΛCDM"),
        "cpl": ([r"$H_0$", r"$\Omega_m$", r"$w_0$", r"$w_a$", r"$\Omega_b h^2$"], "CPL")}

d = np.load(NPZ)
md = {"Keywords": "ACTA-PROCEDENCIA " + json.dumps(acta(__file__, entradas=[NPZ]))}
for m, (labels, nombre) in ETIQ.items():
    fig = corner.corner(d[f"{m}_flat"], labels=labels, quantiles=[0.16, 0.5, 0.84],
                        show_titles=True, title_kwargs={"fontsize": 10})
    fig.suptitle(f"{nombre} posterior (N=25000, covarianza DESI completa)", y=1.01)
    fig.savefig(os.path.join(OUT, f"fig_corner_{m}_professional.pdf"), bbox_inches="tight", metadata=md)
    plt.close(fig)
    print(f"fig_corner_{m}_professional.pdf")
