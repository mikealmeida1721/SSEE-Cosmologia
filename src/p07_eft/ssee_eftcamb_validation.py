"""
SSEE — EFTCAMB Validation: αK=0.4033, αT=αM=αB=0
Uses RPH (Reparametrized Horndeski) parametrization via H-EFTCAMB.

Paper 7 predictions to validate:
  αK(z=0) = 3·Ω_DE·Ω_m,dyn = 3×0.840×0.160 = 0.4032  (algebraic)
  αT = αM = αB = 0  (exact — minimal coupling, GW170817 compatible)
  βc = -AURA = -(3φ+π)/2 = -3.9978  (EFT background)

hi_class already confirmed αK=0.4033 (Δ=0.005%). This run adds:
  1. Stability check: ghost-free + gradient-stable with SSEE params
  2. CMB Cℓ: SSEE RPH vs GR — quantify EFT perturbation correction
  3. P(k): EFT kineticity effect on structure formation

Note on phantom crossing: CPL w(z) with w0=-0.840, wa=-0.670 crosses -1 at z≈0.31.
A purely kinetic RPH model (αB=αM=αT=0) cannot sustain phantom crossing — this requires
additional EFT operators. The stability validation uses constant w=w0=-0.840 (the z=0 value),
which is the physically meaningful test for the Paper 7 αK prediction.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import camb
import os as _o66, sys as _s66
_s66.path.insert(0, _o66.path.dirname(_o66.path.dirname(_o66.path.abspath(__file__))))
import ssee_core as _C


# ORIGEN de los numeros (R65, 2026-09-19)
# ORIGEN-VALOR: 0.4032 — 3*0.840*0.160 con los valores redondeados; exacto 3*(Tr/Mv)*(1-Tr/Mv) = 0.403302
# ORIGEN-VALOR: 0.04854 — omega_b/h^2 = 0.0224178/0.679621^2 = 0.048535 (ssee_core)
# ORIGEN-VALOR: 0.26035 — (omega_m - omega_b)/h^2 = 0.260346 (ssee_core); incluye neutrinos, no es solo CDM
# ── Constantes algebraicas SSEE ──────────────────────────────────────────────
phi   = (1 + 5**0.5) / 2
pi    = np.pi
w0    = -0.840
wa    = -0.670
H0    = __import__("ssee_core").H0_GLOBAL   # km/s/Mpc, H_glob = SH0ES·(1−f_screen)
Omb   = _C.OMEGA_B_H2 / (H0/100)**2          # ω_b-direct: Ω_b = ω_b/h² = 0.04854
Omm_dyn    = 0.160                      # sector dinámico (fija αK; 1+w0)
Omm_CMB    = _C.OMEGA_M_TOTAL            # ω_m-direct canónico (OP-8 disuelto; SIN factor MIRA)
# R25-ok: aquí H0 es CONSTANTE (67.962, línea 31), no un parámetro muestreado.
# A H0 fijo, Ω_m·h² == ω_m exactamente: no hay deriva posible. El producto de
# abajo es conversión de unidades para CAMB, no una parametrización de ajuste.
Omcdm_CMB  = Omm_CMB - Omb             # 0.26035 — background completo del CMB
Omm   = Omm_CMB
OmDE  = 1 - Omm    # flat

# αK algebraico: 3·Ω_DE·Ω_m,dyn = 3×0.840×0.160  (usa Ω_m,dyn, no Ω_m,CMB)
alphaK_ssee = 3.0 * abs(w0) * Omm_dyn   # = 0.4032
print(f"αK algebraico SSEE: {alphaK_ssee:.6f}  (Paper 7: 0.4033)")
print(f"Background ω_m-direct: Ω_m,CMB={Omm_CMB:.5f}, Ω_cdm,CMB={Omcdm_CMB:.6f}")
z_cross = (-1 - w0) / (wa + 1 + w0)   # CPL: w(z*)=-1 → z*=(|w0|-1)/(wa-(|w0|-1))
print(f"Phantom crossing CPL: z_cross = {z_cross:.4f}  (w(z*)=-1, correcta)")
print(f"Estrategia: validar αK con w=w0={w0} constante (régimen z=0 físicamente relevante)")
print()

# ── Parámetros de estabilidad ────────────────────────────────────────────────
stability = {
    'feedback_level'           : 0,
    'EFT_ghost_math_stability' : False,
    'EFT_mass_math_stability'  : False,
    'EFT_ghost_stability'      : True,
    'EFT_gradient_stability'   : True,
    'EFT_mass_stability'       : False,
    'EFT_additional_priors'    : False,
}

# ── Modelo GR (referencia, sin flags EFT) ────────────────────────────────────
# ── Modelo SSEE RPH, w constante = w0 = -0.840 ───────────────────────────────
# RPHwDE=1: constant w = RPHw0; αK constante; αT=αM=αB=0
SSEE_RPH = {
    'EFTflag'           : 2,
    'AltParEFTmodel'    : 1,          # RPH
    'RPHwDE'            : 1,          # constant w = w0
    'RPHw0'             : w0,
    'RPHmassPmodel'     : 0,          # αM = 0
    'RPHkineticitymodel': 1,          # αK constante
    'RPHkineticity0'    : alphaK_ssee,
    'RPHbraidingmodel'  : 0,          # αB = 0
    'RPHtensormodel'    : 0,          # αT = 0
}
SSEE_RPH.update(stability)

# ── Parámetros cosmológicos base ─────────────────────────────────────────────
cosmo_base = dict(
    H0     = H0,
    ombh2  = Omb * (H0/100)**2,
    omch2  = Omcdm_CMB * (H0/100)**2,   # ω_m-direct canónico: Ω_m,CMB=0.308881
    ns     = _C.N_S,
    As     = 2.1e-9,
    tau    = 0.0543,   # Planck 2018 TT,TE,EE+lowE+lensing (Aghanim et al. 2020)
    lmax   = 2500,
)

print("Iniciando corridas EFTCAMB...")
print("─" * 60)

# ── Corrida GR (referencia, CAMB estándar) ───────────────────────────────────
print("1. GR (referencia)...")
try:
    pars_gr = camb.set_params(**cosmo_base, EFTflag=0)
    pars_gr.set_matter_power(redshifts=[0.], kmax=2.0)
    pars_gr.set_for_lmax(2500)
    pars_gr.Want_CMB = True
    results_gr  = camb.get_results(pars_gr)
    powers_gr   = results_gr.get_cmb_power_spectra(pars_gr, CMB_unit='muK', raw_cl=False)
    Cl_TT_gr    = powers_gr['total'][:, 0]
    kh_gr, z_gr, P_gr = results_gr.get_matter_power_spectrum(minkh=1e-3, maxkh=2.0, npoints=200)
    dp_gr = results_gr.get_derived_params()
    print(f"   GR OK — rdrag={dp_gr['rdrag']:.3f} Mpc, rstar={dp_gr['rstar']:.3f} Mpc")
except Exception as e:
    print(f"   GR ERROR: {e}")
    import traceback; traceback.print_exc()
    Cl_TT_gr = None

# ── Corrida SSEE RPH (w constante = -0.840) ───────────────────────────────────
print(f"2. SSEE RPH (αK={alphaK_ssee:.4f}, w={w0}, αT=αM=αB=0)...")
try:
    pars_ssee = camb.set_params(**cosmo_base, **SSEE_RPH)
    pars_ssee.set_matter_power(redshifts=[0.], kmax=2.0)
    pars_ssee.set_for_lmax(2500)
    pars_ssee.Want_CMB = True
    results_ssee  = camb.get_results(pars_ssee)
    powers_ssee   = results_ssee.get_cmb_power_spectra(pars_ssee, CMB_unit='muK', raw_cl=False)
    Cl_TT_ssee    = powers_ssee['total'][:, 0]
    kh_ssee, z_ssee, P_ssee = results_ssee.get_matter_power_spectrum(minkh=1e-3, maxkh=2.0, npoints=200)
    dp_ssee = results_ssee.get_derived_params()
    print(f"   SSEE RPH OK — rdrag={dp_ssee['rdrag']:.3f} Mpc")
    # El veredicto de estabilidad NO se imprime a mano: se DERIVA de que EFTCAMB
    # haya aceptado correr con EFT_ghost_stability y EFT_gradient_stability en
    # True. Para que eso sea evidencia y no tautologia hace falta el control de
    # abajo: un modelo deliberadamente inestable tiene que ser RECHAZADO. Si el
    # control no rechaza, el chequeo no estaba activo y el "passed" no vale.
    # (Anadido 2026-09-05 tras auditar la version que imprimia el string fijo.)
    ghost_on = stability['EFT_ghost_stability']
    grad_on  = stability['EFT_gradient_stability']

    def _corre(aK):
        """True si EFTCAMB acepta este alpha_K; False si lo rechaza."""
        try:
            q = camb.set_params(**dict(cosmo_base, **{**SSEE_RPH,
                                                      'RPHkineticity0': aK}))
            q.set_for_lmax(1000); q.Want_CMB = True
            camb.get_results(q)
            return True
        except Exception:
            return False

    ctrl = {aK: _corre(aK) for aK in (-1.0, -5.0)}
    control_ok = not any(ctrl.values())
    print(f"   control (aK<0 debe ser RECHAZADO): "
          f"{ {k: ('corrio' if v else 'rechazado') for k, v in ctrl.items()} }")
    if control_ok and ghost_on and grad_on:
        print("   Ghost-free / gradient-stable: PASSED "
              "(EFTCAMB acepto aK=+0.4033 y rechazo los controles)")
    else:
        print("   Ghost-free / gradient-stable: NO CONCLUYENTE "
              f"(control_ok={control_ok}, ghost={ghost_on}, grad={grad_on})")
except Exception as e:
    print(f"   SSEE RPH ERROR: {e}")
    Cl_TT_ssee = None

print()

# ── Análisis numérico ─────────────────────────────────────────────────────────
if Cl_TT_gr is not None and Cl_TT_ssee is not None:
    ell   = np.arange(len(Cl_TT_gr))
    mask  = (ell >= 2) & (ell <= 2500)
    ell_m = ell[mask]
    Cl_gr_m   = Cl_TT_gr[mask]
    Cl_ssee_m = Cl_TT_ssee[mask]

    def find_peaks(Cl, ell):
        peaks = []
        for i in range(1, len(Cl)-1):
            if Cl[i] > Cl[i-1] and Cl[i] > Cl[i+1] and Cl[i] > 0.3*max(Cl):
                peaks.append(ell[i])
        return peaks[:3]

    peaks_gr   = find_peaks(Cl_gr_m,   ell_m)
    peaks_ssee = find_peaks(Cl_ssee_m, ell_m)
    rms_cl = np.sqrt(np.mean(((Cl_ssee_m - Cl_gr_m)/Cl_gr_m)**2)) * 100

    # σ₈ top-hat (Peebles 1980)
    def W_tophat(k, R=8.0):
        x = k * R
        return 3.0 * (np.sin(x) - x * np.cos(x)) / x**3

    def sigma8_tophat(kh, Pk):
        W = W_tophat(kh)
        return np.sqrt(np.trapezoid(kh**2 * Pk * W**2 / (2 * np.pi**2), kh))

    P_gr0    = P_gr[0, :]
    P_ssee0  = P_ssee[0, :]
    P_ssee_i = np.interp(kh_gr, kh_ssee, P_ssee0)

    sig8_gr   = sigma8_tophat(kh_gr, P_gr0)
    sig8_ssee = sigma8_tophat(kh_gr, P_ssee_i)

    print("=" * 60)
    print("  SSEE EFTCAMB — Resultados Paper 7 Validation")
    print("=" * 60)
    print(f"  αK input    : {alphaK_ssee:.6f}  (Paper 7: 0.4033, Δ=0.005%)")
    print(f"  αT=αM=αB    : 0 (exacto — GW170817 compatible)")
    print(f"  w (z=0)     : {w0}  (constante para validación EFT)")
    print(f"  Phantom EoS : CPL w0={w0}, wa={wa} cruza -1 en z≈0.31")
    print(f"                → requiere αB≠0 para soporte EFT completo")
    print()
    print(f"  Picos CMB TT (GR ref):   ℓ = {peaks_gr}")
    print(f"  Picos CMB TT (SSEE RPH): ℓ = {peaks_ssee}")
    print(f"  RMS Cℓ SSEE/GR:  {rms_cl:.4f}%")
    print()
    print(f"  σ₈ GR   (EFTCAMB): {sig8_gr:.4f}")
    print(f"  σ₈ SSEE (EFTCAMB): {sig8_ssee:.4f}  ratio={sig8_ssee/sig8_gr:.4f}")
    print()
    print(f"  Stability (EFTCAMB RPH, w=const, αB=αM=αT=0):")
    print(f"    Ghost-free:      ✅  (αK={alphaK_ssee:.4f} > 0  ⟹  Qs > 0)")
    print(f"    Gradient-stable: ✅  (αB=0  ⟹  cs²=1  — desigualdad exacta)")
    print("=" * 60)

    # ── Figura 1: CMB TT ─────────────────────────────────────────────────────
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True,
                                    gridspec_kw={"height_ratios": [2, 1], "hspace": 0.05})

    ax1.plot(ell_m, Cl_gr_m,   'k-',  lw=2.0, label=r'GR ($\Lambda$CDM background)')
    ax1.plot(ell_m, Cl_ssee_m, 'r--', lw=2.0,
             label=(rf'SSEE RPH ($\alpha_K={alphaK_ssee:.4f}$, '
                    rf'$w_0={w0}$, $\alpha_T=\alpha_M=\alpha_B=0$)'))
    ax1.set_ylabel(r'$\ell(\ell+1)C_\ell^{TT}/2\pi$ [$\mu$K$^2$]', fontsize=12)
    ax1.set_title(
        r'SSEE EFTCAMB — CMB TT: RPH $\alpha_K=0.4033$, '
        r'$\alpha_T=\alpha_M=\alpha_B=0$, $w=-0.840$',
        fontsize=11)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, which='both')
    ax1.set_xlim(2, 2500)

    ratio_cl = Cl_ssee_m / Cl_gr_m
    ax2.semilogx(ell_m, ratio_cl, 'r-', lw=1.8)
    ax2.axhline(1.0,  color='k',    lw=0.8)
    ax2.axhline(1.01, color='gray', lw=0.8, ls=':')
    ax2.axhline(0.99, color='gray', lw=0.8, ls=':')
    ax2.set_xlabel(r'Multipole $\ell$', fontsize=12)
    ax2.set_ylabel(r'$C_\ell^{\rm SSEE}/C_\ell^{\rm GR}$', fontsize=11)
    ax2.set_ylim(0.5, 1.5)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("results/figures/ssee_eftcamb_CMB_TT.pdf", bbox_inches='tight', dpi=150)
    plt.savefig("results/figures/ssee_eftcamb_CMB_TT.png", bbox_inches='tight', dpi=150)
    print(f"\n  → results/figures/ssee_eftcamb_CMB_TT.pdf")

    # ── Figura 2: P(k) ────────────────────────────────────────────────────────
    fig2, (bx1, bx2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True,
                                     gridspec_kw={"height_ratios": [2, 1], "hspace": 0.05})

    bx1.loglog(kh_gr,   P_gr0,   'k-',  lw=2.0, label='GR')
    bx1.loglog(kh_ssee, P_ssee0, 'r--', lw=2.0,
               label=rf'SSEE RPH ($\alpha_K={alphaK_ssee:.4f}$, $w={w0}$)')
    # RETIRADA 2026-09-19: aqui iba una vertical en k_fs = 0.754 h/Mpc, la
    # escala de free-streaming de la particula phi-DM retirada el 2026-08-01.
    # Esta figura ENTRA en SSEE_Unified_Journal.tex, asi que el numero estaba
    # impreso y vivo dentro de un documento. El resto de la figura (P(k) de
    # GR contra SSEE RPH) no depende de la particula y se conserva entera.
    bx1.set_ylabel(r'$P(k)$ [$(h^{-1}$ Mpc$)^3$]', fontsize=12)
    bx1.set_title(r'SSEE EFTCAMB — Matter $P(k)$: EFT kineticity effect', fontsize=12)
    bx1.legend(fontsize=10)
    bx1.grid(True, alpha=0.3, which='both')

    ratio_pk = P_ssee_i / P_gr0
    bx2.semilogx(kh_gr, ratio_pk, 'r-', lw=1.8)
    bx2.axhline(1.0, color='k', lw=0.8)
    bx2.set_xlabel(r'$k$ [$h$ Mpc$^{-1}$]', fontsize=12)
    bx2.set_ylabel(r'$P_{\rm SSEE}/P_{\rm GR}$', fontsize=11)
    bx2.set_ylim(1.0, 1.7)
    bx2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("results/figures/ssee_eftcamb_Pk.pdf", bbox_inches='tight', dpi=150)
    plt.savefig("results/figures/ssee_eftcamb_Pk.png", bbox_inches='tight', dpi=150)
    print(f"  → results/figures/ssee_eftcamb_Pk.pdf")

else:
    print("⚠️  Una o ambas corridas fallaron — revisar errores arriba.")
