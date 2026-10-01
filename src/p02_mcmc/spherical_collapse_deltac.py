#!/usr/bin/env python3
"""
Ruta 1: δc desde la dinámica del modelo (colapso esférico), sin postular n_s.

Integra la ecuación EXACTA no lineal del top-hat esférico con DE suave
(no se agrupa) y en relatividad general:

    OJO CON LA JUSTIFICACIÓN (corregido 2026-09-25, Claude). La versión
    anterior de este docstring decía «no se agrupa: consistente con Paper 5,
    c²_s,eff=0». Esa razón está INVERTIDA: c_s²=0 anula el horizonte sonoro y
    es justamente la condición para que un fluido de DE SÍ se agrupe a toda
    escala sub-horizonte. Si esa fuera la razón, el supuesto de DE suave
    estaría mal y δc se movería.
    La razón CORRECTA, y que sí sostiene el supuesto, es la fricción viscosa
    IS del propio Paper 5 (§«IS damping hierarchy», l.900-905):
        F(k,a) = (1 − 3c_s²) + z̃·(k/aH)²      con c_s²=0  ⟹  F = 1 + z̃(k/aH)²
    crece como k² y suprime las perturbaciones de DE; medido en el mismo
    paper, δ_DE/δ_m → 0⁻ a toda escala sub-horizonte (l.111).
    O sea: la DE de este modelo no se agrupa A PESAR de c_s²=0, no POR c_s²=0.

    δ'' + (2 + H'/H) δ' − (4/3)(δ')²/(1+δ) = (3/2) Ω_m(a) δ (1+δ)

(' = d/d ln a). Para un colapso objetivo a_c se hace shooting sobre δ_i
(condición inicial en dominación de materia, modo creciente δ'=δ);
δc(a_c) = δ_lin(a_c) con la ecuación lineal y las mismas condiciones iniciales.

Validación: EdS debe dar 1.68647 a todo z_c; ΛCDM z_c=0 debe dar ≈1.676.

Supuestos declarados: (i) GR, (ii) DE suave, (iii) top-hat esférico.
Si el sector IS del modelo modifica el colapso no lineal más allá de DE
suave, este cálculo no lo captura — la carga de especificarlo es del modelo.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── fondos ────────────────────────────────────────────────────────────────
def make_bg(Om, w0, wa):
    Ode = 1.0 - Om
    def E2(a):
        return Om * a**-3 + Ode * a**(-3*(1 + w0 + wa)) * np.exp(-3*wa*(1 - a))
    def Om_a(a):
        return Om * a**-3 / E2(a)
    def HoverH(a):                      # d ln H / d ln a = −3/2 (1+w_tot)
        w = w0 + wa * (1 - a)
        return -1.5 * (1 + w * (1 - Om_a(a)))
    return Om_a, HoverH

import os as _os0, sys as _sys0
_sys0.path.insert(0, _os0.path.dirname(_os0.path.dirname(_os0.path.abspath(__file__))))
import ssee_core as _S  # noqa: E402

BG = {
    "EdS":   make_bg(1.0, -1.0, 0.0),
    "LCDM":  make_bg(0.3153, -1.0, 0.0),          # Planck 2018
    "SSEE":  make_bg(_S.OMEGA_M_TOTAL, _S.W0, _S.WA),  # canónico algebraico, del núcleo (2026-09-30: antes tecleado a 5-6 cifras)
}

A_I = 1.0 / 501.0          # a inicial, dominación de materia profunda
A_I2 = 1.0 / 1001.0         # niveles para Richardson a δ_i → 0
A_I3 = 1.0 / 2001.0
D_MAX = 1e10               # umbral de colapso (δ → ∞); sesgo < 2e-5 verificado en EdS

def rhs(x, Y, Om_a, HoverH, linear):
    d, dp = Y
    c = 2.0 + HoverH(np.exp(x))
    om = Om_a(np.exp(x))
    if linear:
        ddp = -c * dp + 1.5 * om * d
    else:
        ddp = -c * dp + (4.0/3.0) * dp**2 / (1 + d) + 1.5 * om * d * (1 + d)
    return [dp, ddp]

def collapse_a(di, Om_a, HoverH, a_i):
    """a de colapso para δ_i dado (modo creciente). inf si no colapsa antes de a=1."""
    def event(x, Y, *a):
        return Y[0] - D_MAX
    event.terminal = True
    event.direction = 1
    sol = solve_ivp(rhs, (np.log(a_i), 0.0), [di, di], args=(Om_a, HoverH, False),
                    method="DOP853", rtol=1e-10, atol=1e-14,
                    events=event, dense_output=False)
    if sol.t_events[0].size:
        return np.exp(sol.t_events[0][0])
    return np.inf

def _delta_c_fixed_ai(a_c, Om_a, HoverH, a_i):
    """Shooting con a_i fijo: δ_i tal que el colapso ocurra en a_c; devuelve δ_lin(a_c)."""
    lo, hi = 1e-7, 0.2
    assert collapse_a(lo, Om_a, HoverH, a_i) > a_c, "lo colapsa antes que a_c"
    assert collapse_a(hi, Om_a, HoverH, a_i) < a_c, "hi no colapsa antes que a_c"
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if collapse_a(mid, Om_a, HoverH, a_i) > a_c:
            lo = mid
        else:
            hi = mid
    di = 0.5 * (lo + hi)
    sol = solve_ivp(rhs, (np.log(a_i), np.log(a_c)), [di, di],
                    args=(Om_a, HoverH, True),
                    method="DOP853", rtol=1e-12, atol=1e-15)
    return sol.y[0, -1], di

def delta_c(a_c, Om_a, HoverH):
    """δc con Richardson de 3 niveles a δ_i → 0 (error O(δ_i) ∝ a_i, luego O(a_i²))."""
    v1, _ = _delta_c_fixed_ai(a_c, Om_a, HoverH, A_I)
    v2, _ = _delta_c_fixed_ai(a_c, Om_a, HoverH, A_I2)
    v3, di3 = _delta_c_fixed_ai(a_c, Om_a, HoverH, A_I3)
    return (8*v3 - 6*v2 + v1)/3.0, di3

# ── corrida ───────────────────────────────────────────────────────────────
zcs = [0, 1, 2, 5, 10]
print(f"{'z_c':>5}  {'a_c':>8}  {'EdS':>9}  {'ΛCDM':>9}  {'SSEE':>9}  "
      f"{'SSEE/EdS-1':>10}  {'SSEE/ΛCDM-1':>11}")
print("-" * 70)
res = {k: [] for k in BG}
for zc in zcs:
    a_c = 1.0 / (1 + zc)
    row = {}
    for name, (Om_a, HoverH) in BG.items():
        dc, di = delta_c(a_c, Om_a, HoverH)
        row[name] = dc
        res[name].append(dc)
    e, l, s = row["EdS"], row["LCDM"], row["SSEE"]
    print(f"{zc:5d}  {a_c:8.5f}  {e:9.5f}  {l:9.5f}  {s:9.5f}  "
          f"{(s/e-1)*100:9.3f}%  {(s/l-1)*100:10.3f}%")

# ── validación ────────────────────────────────────────────────────────────
eds0 = res["EdS"][0]
print(f"\nValidación EdS(z=0): {eds0:.5f} (esperado 1.68647) → "
      f"{'PASA' if abs(eds0-1.68647) < 1e-4 else 'FALLA'}")
print(f"Postulado Paper 4: δc_SSEE = 1.6284; dinámica Ruta 1 (z=0): {res['SSEE'][0]:.5f}")

# ── LOG: este es el ORIGEN de los δc que consumen los demás scripts ─────────
import json as _json, os as _os, datetime as _dt
_log = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__)))), "results", "logs", "deltac_spherical_collapse.json")
_os.makedirs(_os.path.dirname(_log), exist_ok=True)
with open(_log, "w") as _f:
    _json.dump({
        "fecha": _dt.date.today().isoformat(),
        "script": "src/p02_mcmc/spherical_collapse_deltac.py",
        "metodo": "top-hat esferico, ec. no lineal exacta, shooting sobre delta_i, DE suave",
        "supuesto_DE_suave_justificado_por": "friccion viscosa IS de Paper 5 (F ~ k^2), NO por c_s^2=0",
        "control_EdS_analitico": 3/20 * (12*np.pi)**(2/3),
        "z_c": list(zcs),
        "deltac": {k: [float(x) for x in v] for k, v in res.items()},
        "deltac_SSEE_zc0": float(res["SSEE"][0]),
        "deltac_LCDM_zc0": float(res["LCDM"][0]),
        "postulado_retirado_OP27": 1.6865 * (1 - ((1+5**0.5)/2)**-7),
        # Redondeos A 5 CIFRAS: son los que se IMPRIMEN en los papers y en los
        # cajones. Van en el log para que sean rastreables tal como se citan,
        # no solo como float completo (lo pidio R65 al marcarlos sin origen).
        "citado_deltac_SSEE_zc0":  round(float(res["SSEE"][0]), 5),
        "citado_deltac_LCDM_zc0":  round(float(res["LCDM"][0]), 5),
        "citado_deltac_SSEE_zc10": round(float(res["SSEE"][-1]), 5),
        "citado_deltac_LCDM_zc10": round(float(res["LCDM"][-1]), 5),
        "citado_deltac_EdS":       round(float(res["EdS"][-1]), 5),
    }, _f, indent=2)
print(f"Log → {_log}")

# ── figura ────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.5))
for name, sty in [("EdS", "k:"), ("LCDM", "b-"), ("SSEE", "r-")]:
    ax.plot(zcs, res[name], sty, lw=2, label=name)
ax.axhline(1.6284, color="r", ls="--", lw=1.2, label="postulado Paper 4 (1.6284)")
ax.set_xlabel("redshift de colapso $z_c$")
ax.set_ylabel(r"$\delta_c(z_c)$")
ax.set_title("Umbral de colapso esférico desde la dinámica (DE suave, GR)")
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
out = "results/figures/fig_deltac_ruta1"
plt.savefig(out + ".pdf", bbox_inches="tight")
plt.savefig(out + ".png", dpi=150, bbox_inches="tight")
print(f"Figura → {out}.pdf/.png")
