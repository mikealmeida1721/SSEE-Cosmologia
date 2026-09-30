#!/usr/bin/env python3
"""Regenerador standalone de fig8_bao_residuals (Paper 2).

Residuos normalizados (q_pred - q_obs)/σ para los 13 puntos DESI DR2 (Tabla 4,
2503.14738), tres modelos con su MAP propio. Datos: FUENTE ÚNICA
data/raw/desi_dr2_bao.csv (NO hardcodear; drift DR1/DR2 corregido 2026-07-02).
r_d por modelo vía Eisenstein-Hu (eq. 5 del paper). Regenera la figura que estaba
en DR1 (abril) tras el fix DR2.

Uso: python src/p02_mcmc/regenerate_fig8_bao_residuals.py
"""
import os, sys
import numpy as np
from scipy.integrate import quad
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from desi_dr2_data import load_desi_dr2  # noqa: E402

c = 299792.458
d = load_desi_dr2()                      # z, tracer, quantity, value, sigma
OUT = os.path.join(ROOT, "results", "figures")

# ORIGEN-VALOR: 0.1432 — pivote de omega_m h^2 de la eq. rd de Paper 2 (Planck 2018 TT,TE,EE+lowE: 0.1432); la cita EH98 de esa ecuacion esta en FUENTES_PENDIENTES.md
# ORIGEN-VALOR: 0.02187 — omega_b h^2 del MAP de SSEE, results/logs/mcmc_paper2_3models_wmfix.log linea 187
# ORIGEN-VALOR: 0.02233 — omega_b h^2 del MAP de LCDM, results/logs/mcmc_paper2_3models_wmfix.log linea 195
# ORIGEN-VALOR: 0.02238 — omega_b h^2 del MAP de CPL, results/logs/mcmc_paper2_3models_wmfix.log linea 202
import os as _os_rd, sys as _sys_rd
_sys_rd.path.insert(0, _os_rd.path.join(_os_rd.path.dirname(_os_rd.path.abspath(__file__)), ".."))
from rd_camb import rd_mpc as _rd_camb  # r_d de CAMB, una sola funcion (2026-09-28)


def rd_EH(om_h2, ob_h2):                 # eq. 5 del paper
    return _rd_camb(ob_h2, om_h2, mnu=None)  # CAMB; antes 147.27*(...) con normalizacion 0.15 % alta

def f_de(z, w0, wa):
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

def E(z, Om, w0, wa):
    de = 1.0 if (w0 == -1 and wa == 0) else f_de(z, w0, wa)
    return np.sqrt(Om * (1 + z) ** 3 + (1 - Om) * de)

# ── Punto de cada modelo: LEÍDO del log de la corrida de 3 modelos ─────────
# FUENTE: results/logs/mcmc_paper2_3models_wmfix.log, sección «PARÁMETROS
# POSTERIORES». (2026-09-29) Antes estos números iban TECLEADOS aquí y se
# quedaron viejos cuando la corrida se rehizo con r_d de CAMB y la mν de cada
# modelo (ΛCDM H0 68.27 → 68.39). Ahora se leen: un literal no se entera de
# que su fuente cambió.
# SSEE: ω_m ALGEBRAICO fijo y Ω_m = ω_m/h² DERIVADO (parametrización R25,
# igual que lpost_ssee de ssee_paper2_mcmc.py). ΛCDM y CPL: su mν (0.06).
from ssee_core import OMEGA_M_H2 as _WM_ALG, W0 as _W0, WA as _WA  # noqa: E402
_sys_rd.path.insert(0, _os_rd.path.join(ROOT, "src", "p11_sondas"))
_MNU_LCDM = __import__("lcdm_planck").LCDM_PLANCK["mnu"]


def _lee_posteriores(ruta=os.path.join(ROOT, "results", "logs", "mcmc_paper2_3models_wmfix.log")):
    import re
    txt = open(ruta, encoding="utf-8").read().split("PARÁMETROS POSTERIORES")[1]
    bloques = re.split(r"\[(SSEE|ΛCDM|CPL)\]", txt)
    out = {}
    for nom, cuerpo in zip(bloques[1::2], bloques[2::2]):
        d = {}
        for clave, pat in (("H0", r"H₀\s*=\s*([-0-9.]+)"), ("ob", r"Ω_b·h²\s*=\s*([-0-9.]+)"),
                           ("Om", r"Ω_m\s+=\s*([-0-9.]+)"), ("w0", r"w₀\s+=\s*([-0-9.]+)"),
                           ("wa", r"wₐ\s+=\s*([-0-9.]+)")):
            m = re.search(pat, cuerpo)
            if m:
                d[clave] = float(m.group(1))
        out[nom] = d
    return out


_P = _lee_posteriores()
models = {
    "SSEE": dict(H0=_P["SSEE"]["H0"], Om=_WM_ALG / (_P["SSEE"]["H0"] / 100) ** 2, w0=_W0, wa=_WA,
                 ob=_P["SSEE"]["ob"], wm=_WM_ALG, mnu=None, c="#c0392b"),
    r"$\Lambda$CDM": dict(H0=_P["ΛCDM"]["H0"], Om=_P["ΛCDM"]["Om"], w0=-1.0, wa=0.0,
                          ob=_P["ΛCDM"]["ob"], mnu=_MNU_LCDM, c="#2c6fbb"),
    "CPL": dict(H0=_P["CPL"]["H0"], Om=_P["CPL"]["Om"], w0=_P["CPL"]["w0"], wa=_P["CPL"]["wa"],
                ob=_P["CPL"]["ob"], mnu=_MNU_LCDM, c="#27ae60"),
}
print({k: {q: round(v, 5) for q, v in m.items() if q not in ("c",) and v is not None} for k, m in models.items()})

def predict(z, quantity, m):
    wm = m.get("wm", m["Om"] * (m["H0"] / 100) ** 2)
    rd = _rd_camb(m["ob"], wm, mnu=m["mnu"])
    DH = c / (m["H0"] * E(z, m["Om"], m["w0"], m["wa"]))
    DM = c * quad(lambda zz: 1 / (m["H0"] * E(zz, m["Om"], m["w0"], m["wa"])), 0, z)[0]
    if quantity.startswith("DV"):
        return (z * DM ** 2 * DH) ** (1 / 3) / rd
    return (DM if quantity.startswith("DM") else DH) / rd

# ── figura ──
plt.rcParams.update({"font.size": 12, "savefig.dpi": 300, "savefig.bbox": "tight"})
fig, ax = plt.subplots(figsize=(9, 5))
labels = [f"{zz:.2f} {q.split('_')[0]}" for zz, q in zip(d["z"], d["quantity"])]
x = np.arange(len(labels))
chi2_by_model = {}
for name, m in models.items():
    pulls = [(predict(zz, q, m) - v) / s
             for zz, q, v, s in zip(d["z"], d["quantity"], d["value"], d["sigma"])]
    chi2 = float(np.sum(np.array(pulls) ** 2))
    chi2_by_model[name] = round(chi2, 1)
    ax.plot(x, pulls, "o-", color=m["c"], lw=1.4, ms=6,
            label=fr"{name} ($\chi^2={chi2:.1f}$)")
for lvl in (-2, -1, 1, 2):
    ax.axhline(lvl, color="0.8", lw=0.8, ls="--", zorder=0)
ax.axhline(0, color="0.4", lw=1.0, zorder=0)
ax.set_xticks(x); ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
ax.set_ylabel(r"$(q_{\rm pred}-q_{\rm obs})/\sigma$")
ax.set_title("DESI DR2 BAO residuals (13 points, 2503.14738 Table 4)")
ax.legend(frameon=False); ax.set_ylim(-3.2, 3.2)
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(OUT, f"fig8_bao_residuals.{ext}"))
print("fig8_bao_residuals regenerada (DR2). χ² por modelo:", chi2_by_model)
