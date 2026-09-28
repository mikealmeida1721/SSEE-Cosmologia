"""
Fase B / P3 — r_d y θ* en el punto CANÓNICO del reframe ω_m-DIRECTO (2026-06-18).
  H global = H_glob = SH0ES·(1−f_screen) (ssee_core.H0_GLOBAL); 3(φ+π)² es el blanco.  NO hay factor materia (OP-8 cerrado):
  Ω_m,CMB = ω_m/h² = 0.308881 con cada pieza algebraica de SSEE.

Reusa _run_camb de ssee_paper3_cmb.py. Reporta r_d, θ*, 100θ* y los compara
con Planck 2018 (r_d=147.09±0.26 Mpc, 100θ*=1.04109±0.00030).
"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ssee_core import SUM_MNU_EV as _MNU
from ssee_paper3_cmb import _run_camb

# ── ingredientes SSEE (reframe ω_m-directo) ──────────────────────────────
phi = (1 + 5**0.5) / 2
pi  = np.pi
Omega = pi + phi
H0    = __import__("ssee_core").H0_GLOBAL    # H_glob = SH0ES·(1−f_screen); 3Ω² es el blanco puro
ombh2 = (pi - phi) / (3 * Omega**2)   # 0.02242  SSEE algebraico (OP-1)
ns    = 1 - phi**-7
KAL0  = (pi + phi)/2 + pi             # 5.5214
omch2 = KAL0 * ombh2 * ns            # 0.11951  forward (ya en Paper 1)
mnu   = _MNU                          # Σm_ν canónico del nucleo (C_ν=93.14 PDG)
omega_m = ombh2 + omch2 + mnu/93.14  # 0.14267
h = H0/100.0
Omm_cmb = omega_m / h**2             # 0.308881  DERIVADO, sin factor

# w0, wa algebraicos
Tr = 3*(phi + (pi+phi)/2)            # 11.9935
Mv = phi + pi + (phi + pi + (phi+pi+Omega))  # K_v chain → Σ9 = 14.2788
w0 = -0.840
wa = -0.670
As = np.exp(3.044)*1e-10

print("=== Fase B / P3 — r_d y θ* reframe ω_m-DIRECTO ===")
print(f"H0={H0:.4f}  ombh2={ombh2:.5f}  omch2={omch2:.5f}  mnu={mnu}")
print(f"-> omega_m={omega_m:.5f}  Omega_m,CMB={Omm_cmb:.5f}  (sin factor; OP-8 cerrado)")

t0 = time.time()
print(f"\n--- RESULTADO ({0.0:.1f}s) ---")
# Anchor (H_alg=67.962) y posterior MCMC (67.787, parametrización ω_m-fijo R25;
# el 67.9475 previo congelaba Ω_m y sesgaba hacia el ancla): r_d y θ* (grados + 100θ*)
# ORIGEN: H_glob de ssee_core; posterior de results/logs/mcmc_paper2_reframe.json (leídos, no tecleados)
import json as _j
_HPOST = _j.load(open("results/logs/mcmc_paper2_reframe.json"))["H0_mediana"]
for tag, H0v in ((f"H_glob {H0:.6f}", H0), (f"posterior MCMC {_HPOST:.4f}", _HPOST)):
    total, lens_p, derived = _run_camb(H0v, ombh2, omch2, mnu, w0, wa, As, ns, 2500)
    r_d = derived["rdrag"]
    th100 = derived["thetastar"]            # 100*theta_*
    th_deg = th100 / 100.0 * 180.0 / np.pi  # theta_* en grados
    sig_rd = abs(r_d - 147.09) / 0.26
    sig_th = abs(th100 - 1.04109) / 0.00030
    print(f"[{tag}] r_d = {r_d:.3f} Mpc ({sig_rd:.2f}σ)  "
          f"θ* = {th_deg:.5f}° (100θ*={th100:.5f}, {sig_th:.2f}σ)")
print(f"(Planck: r_d=147.09±0.26 Mpc, 100θ*=1.04109±0.00030; {time.time()-t0:.1f}s)")
