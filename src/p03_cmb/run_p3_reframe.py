"""
Fase B / P3 CMB — evaluar el punto CANÓNICO del reframe omega_m-DIRECTO (2026-06-18).
  H global = H_glob = SH0ES·(1−f_screen) (ssee_core.H0_GLOBAL). NO hay factor materia (OP-8 cerrado): Omega_m,CMB = omega_m/h²
  con cada pieza algebraica de SSEE:
    omega_b = (pi-phi)/(3 Omega^2)   (OP-1)
    omega_c = KAL0 * omega_b * n_s   (forward, ya en Paper 1)
    omega_nu = Sigma_m_nu / 93.14 eV
Compara chi2 vs LCDM y reporta DeltaBIC. Marca claramente que As/tau son EXTERNOS
(se mantienen fijos para ambos), todo lo demas es SSEE.
"""
import time, math, numpy as np
import ssee_paper3_cobaya_unified as P3
import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))))
from ssee_core import SUM_MNU_EV as _MNU, OMEGA_M_CMB_PIPHI as _OM_PIPHI

# --- ingredientes SSEE (reframe omega_m-directo) ---
phi = (1+5**0.5)/2; pi = math.pi
Omega = pi + phi
KAL0  = (pi+phi)/2 + pi
n_s   = 1 - phi**-7
H0      = __import__("ssee_core").H0_GLOBAL   # H_glob = SH0ES·(1−f_screen); 3Ω² es el blanco puro
ombh2   = (pi-phi)/(3*Omega**2)      # 0.02242  SSEE algebraico (OP-1)
omch2   = KAL0 * ombh2 * n_s         # 0.11951  forward (Paper 1)
mnu     = _MNU                       # Sigma_m_nu activos del nucleo (C_nu=93.14)
omega_m = ombh2 + omch2 + mnu/93.14  # 0.14267  omega_m fisico
Omm_cmb = omega_m / (H0/100)**2      # 0.308881  DERIVADO, sin factor

print(f"=== Fase B / P3 CMB reframe omega_m-DIRECTO ===")
print(f"H0={H0:.4f}  omega_b={ombh2:.5f}  omega_c={omch2:.5f}  omega_m={omega_m:.5f}")
print(f"-> Omega_m,CMB = omega_m/h² = {Omm_cmb:.5f}   (sin factor; OP-8 cerrado)")

t0=time.time()
chi2_ssee = P3.evaluate_model(H0, ombh2, omch2, P3.w0_ssee, P3.wa_ssee,
                              P3.As_ssee, P3.ns_ssee, P3.tau_ssee, mnu=mnu, quiet=True)
print(f"SSEE omega_m-directo chi2_eff = {chi2_ssee:.3f}   ({time.time()-t0:.1f}s)")

# CONTROL contra la identidad RETIRADA (2026-06-18, con el factor materia):
# factor pi/phi (0.31076, retirado) con MISMO H/omega_b para aislar el efecto.
# Se evalua para MOSTRAR que el canonico gana, no como valor en uso.
omch2_piphi = _OM_PIPHI*(H0/100)**2 - ombh2
chi2_piphi = P3.evaluate_model(H0, ombh2, omch2_piphi, P3.w0_ssee, P3.wa_ssee,
                               P3.As_ssee, P3.ns_ssee, P3.tau_ssee, mnu=mnu, quiet=True)
print(f"SSEE factor pi/phi({_OM_PIPHI:.5f})@H={H0:.3f} chi2_eff = {chi2_piphi:.3f}  (superado)")

t0=time.time()
chi2_lcdm = P3.evaluate_model(P3.H0_lcdm, P3.ombh2_lcdm, P3.omch2_lcdm, -1.0, 0.0,
                              P3.As_lcdm, P3.ns_lcdm, P3.tau_lcdm, mnu=P3.mnu_lcdm, quiet=True)
print(f"LCDM chi2_eff = {chi2_lcdm:.3f}   ({time.time()-t0:.1f}s)")

N_data = 613
dchi2 = chi2_ssee - chi2_lcdm
dbic  = dchi2 + (2-6)*np.log(N_data)
print(f"\n--- RESULTADO ---")
print(f"chi2 SSEE reframe = {chi2_ssee:.3f}")
print(f"chi2 LCDM         = {chi2_lcdm:.3f}")
print(f"Dchi2 (SSEE-LCDM) = {dchi2:+.3f}")
print(f"DeltaBIC (k2 vs k6) = {dbic:+.3f}")
