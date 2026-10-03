"""
SSEE — Paper 3: CMB Power Spectrum vs Planck 2018
Computes Cl_TT/TE/EE/lensing under SSEE background, applies r_d,eff mapping,
compares against Planck 2018 data, and produces chi2 + figures.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import urllib.request

matplotlib.use("Agg")

# ---------------------------------------------------------------------------
# SSEE constants (algebraically fixed)
# ---------------------------------------------------------------------------
import os as _reloc_os, sys as _reloc_sys  # reloc: anclar src/
_reloc_sys.path.insert(0, _reloc_os.path.dirname(_reloc_os.path.dirname(_reloc_os.path.abspath(__file__))))
from ssee_core import (
    PHI as phi, PI as pi, OMEGA as Omega, BETA as beta, KAL0,
    P_SC as P_sc, K_V as Kv, T_R as Tr, M_V as Mv, W0 as w0, WA as wa,
    OMEGA_DE as OmDE, S_M as s_m, AURA, MIRA,
    OMEGA_M_CMB as Omm_cmb, N_S as ns, SUM_MNU_EV,
)
M_SSEE = abs(w0)   # acoustic saturation factor (= |w0|)
# Reframe ω_m-DIRECTO (OP-8 cerrado): NO hay factor materia. ω_b y ω_c son densidades
# físicas FIJAS algebraicamente (forward); Ω_m,CMB = ω_m/h² es DERIVADO (= Omm_cmb, diagnóstico).

H0       = __import__("ssee_core").H0_GLOBAL  # H_glob = SH0ES·(1−f_screen) (2026-09-28; era el literal 67.962)
Omb_h2   = (pi - phi) / (3.0 * Omega**2)   # 0.02242 — ω_b directo (era 0.02237 Planck input)
# n_s = 1 - phi^-7 = 0.96556 (predicción algebraica SSEE, Paper 4) — importado arriba
ln_As    = 3.044
As       = np.exp(ln_As) * 1e-10


# ---------------------------------------------------------------------------
# Output directories
# ---------------------------------------------------------------------------
FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "results", "figures")
DAT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(DAT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Download Planck 2018 TT spectrum (COM_PowerSpect_CMB-TT-full_R3.01.txt)
# ---------------------------------------------------------------------------
PLANCK_FILE = os.path.join(DAT_DIR, "planck2018_TT.txt")
PLANCK_URL  = (
    "https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/"
    "cosmoparams/COM_PowerSpect_CMB-TT-full_R3.01.txt"
)

PLANCK_TE_FILE = os.path.join(DAT_DIR, "planck2018_TE.txt")
PLANCK_TE_URL  = (
    "https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/"
    "cosmoparams/COM_PowerSpect_CMB-TE-full_R3.01.txt"
)

PLANCK_EE_FILE = os.path.join(DAT_DIR, "planck2018_EE.txt")
PLANCK_EE_URL  = (
    "https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/"
    "cosmoparams/COM_PowerSpect_CMB-EE-full_R3.01.txt"
)

PLANCK_LENS_FILE = os.path.join(DAT_DIR, "planck2018_lensing.txt")
PLANCK_LENS_URL  = (
    "https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/"
    "cosmoparams/COM_PowerSpect_CMB-lensing_R3.01.txt"
)


def _download(url, path, label):
    if os.path.exists(path):
        return
    print(f"Descargando {label}...")
    try:
        urllib.request.urlretrieve(url, path)
        print(f"  Guardado en {path}")
    except Exception as e:
        print(f"  Descarga fallida ({label}): {e}")


def download_planck():
    _download(PLANCK_URL,      PLANCK_FILE,      "Planck TT")
    _download(PLANCK_TE_URL,   PLANCK_TE_FILE,   "Planck TE")
    _download(PLANCK_EE_URL,   PLANCK_EE_FILE,   "Planck EE")
    _download(PLANCK_LENS_URL, PLANCK_LENS_FILE, "Planck lensing")


def _load_spectrum(path, label):
    if not os.path.exists(path):
        return None, None, None
    try:
        data = np.loadtxt(path, comments="#")
        ell   = data[:, 0].astype(int)
        Dl    = data[:, 1]
        sigma = 0.5 * (np.abs(data[:, 2]) + np.abs(data[:, 3]))
        return ell, Dl, sigma
    except Exception as e:
        print(f"  Error leyendo {label}: {e}")
        return None, None, None


def load_planck():
    tt  = _load_spectrum(PLANCK_FILE,      "TT")
    te  = _load_spectrum(PLANCK_TE_FILE,   "TE")
    ee  = _load_spectrum(PLANCK_EE_FILE,   "EE")
    # lensing file: columns ell, Cl_phiphi, sigma (dimensionless)
    lens = _load_spectrum(PLANCK_LENS_FILE, "lensing")
    return tt, te, ee, lens


# ---------------------------------------------------------------------------
# Compute SSEE / ΛCDM spectra with CAMB
# ---------------------------------------------------------------------------
def _run_camb(H0_val, ombh2, omch2, mnu, w0_val, wa_val, As_val, ns_val, lmax):
    import camb
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0_val, ombh2=ombh2, omch2=omch2,
                       mnu=mnu, omk=0, tau=0.054)
    pars.set_dark_energy(w=w0_val, wa=wa_val, dark_energy_model="ppf")
    pars.InitPower.set_params(As=As_val, ns=ns_val)
    pars.set_for_lmax(lmax, lens_potential_accuracy=2)
    pars.Want_CMB = True
    pars.WantTensors = False
    results = camb.get_results(pars)
    powers  = results.get_cmb_power_spectra(pars, CMB_unit="muK", raw_cl=False)
    # lensed total: columns 0=TT, 1=EE, 2=BB, 3=TE
    total   = powers["total"]
    lens_p  = results.get_lens_potential_cls(lmax=lmax)  # cols: 0=phiphi, 1=Tphi, 2=Ephi
    derived = results.get_derived_params()
    return total, lens_p, derived


def compute_ssee_spectrum(lmax=2500):
    h      = H0 / 100.0
    omch2  = KAL0 * Omb_h2 * ns   # 0.11951 — ω_c FORWARD (KAL₀·ω_b·n_s); era Omm_cmb·h²−ω_b (MIRA)
    total, lens_p, derived = _run_camb(
        H0, Omb_h2, omch2, SUM_MNU_EV, w0, wa, As, ns, lmax)  # Σm_ν canónico del core (0.06849; C_ν=93.14)
    r_d_camb = derived["rdrag"]
    ells     = np.arange(total.shape[0])
    return ells, total, lens_p, r_d_camb, derived


# 2026-10-03: aquí vivía compute_naive_spectrum, el «caso naive» que ponía
# s_m = 1+w0 = 0.160 como Omega_m en la geometría. s_m es un número de la ecuación
# de estado, no una densidad: el caso no es una versión del modelo sino el error de
# categoría retirado el 2026-07-30, y Paper 3 ya no lo usa como contraejemplo.


def picos(ells, Dl):
    from scipy.signal import argrelmax
    i = argrelmax(Dl[50:1500], order=60)[0] + 50
    return [int(ells[j]) for j in i[:3]]


def compute_lcdm_spectrum(lmax=2500):
    # ORIGEN-VALOR: 67.36, 0.02237, 0.1200, 0.06, 3.044, 0.9649 — Planck 2018 TT,TE,EE+lowE+lensing (tabla 2, col. 5), la referencia LCDM
    total, lens_p, derived = _run_camb(
        67.36, 0.02237, 0.1200, 0.06, -1.0, 0.0,
        np.exp(3.044)*1e-10, 0.9649, lmax)
    r_d = derived["rdrag"]
    ells = np.arange(total.shape[0])
    return ells, total, lens_p, r_d


# ---------------------------------------------------------------------------
# Chi2 calculation
# ---------------------------------------------------------------------------
def chi2_vs_planck(ell_obs, Dl_obs, sigma_obs, ell_model, Dl_model,
                   ell_min=30, ell_max=2000):
    mask      = (ell_obs >= ell_min) & (ell_obs <= ell_max)
    ell_sel   = ell_obs[mask]
    Dl_sel    = Dl_obs[mask]
    sig_sel   = sigma_obs[mask]
    Dl_interp = np.interp(ell_sel, ell_model, Dl_model)
    residuals = (Dl_interp - Dl_sel) / sig_sel
    chi2      = np.sum(residuals**2)
    chi2_r    = chi2 / len(ell_sel)
    return chi2, chi2_r, len(ell_sel)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def _residual_panel(ax, ell_obs, Dl_obs, sigma_obs, ells_model, Dl_model,
                    color="tab:blue"):
    Dl_interp = np.interp(ell_obs, ells_model, Dl_model)
    res = (Dl_interp - Dl_obs) / sigma_obs
    ax.plot(ell_obs, res, ".", ms=2, alpha=0.5, color=color)
    ax.axhline(0,  color="k",    lw=0.8)
    ax.axhline(+1, color="gray", lw=0.6, ls="--")
    ax.axhline(-1, color="gray", lw=0.6, ls="--")
    ax.set_ylim(-5, 5)
    ax.grid(True, alpha=0.3)


def _spectrum_figure(ells_s, Dl_s, ells_l, Dl_l,
                     ell_obs, Dl_obs, sigma_obs,
                     ylabel, title, outname,
                     xlim=(2, 2500), ylim=None,
                     ssee_label=None, lcdm_label=None):
    fig, axes = plt.subplots(2, 1, figsize=(10, 8),
                             gridspec_kw={"height_ratios": [3, 1]})
    ax = axes[0]
    if ell_obs is not None:
        ax.errorbar(ell_obs, Dl_obs, yerr=sigma_obs,
                    fmt="k.", ms=2, lw=0.5, alpha=0.6, label="Planck 2018")
    lbl_l = lcdm_label or r"$\Lambda$CDM"
    lbl_s = ssee_label or r"SSEE"
    ax.plot(ells_l[2:], Dl_l[2:], color="tab:orange", lw=1.5, ls="--", label=lbl_l)
    ax.plot(ells_s[2:], Dl_s[2:], color="tab:blue",   lw=1.8, label=lbl_s)
    ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    ax.set_ylabel(ylabel, fontsize=13)
    ax.legend(fontsize=10)
    ax.set_title(title, fontsize=13)
    ax.grid(True, alpha=0.3)

    ax2 = axes[1]
    if ell_obs is not None:
        _residual_panel(ax2, ell_obs, Dl_obs, sigma_obs, ells_s, Dl_s)
        ax2.set_ylabel(r"$(D_\ell^{\rm SSEE}-D_\ell^{\rm Planck})/\sigma$", fontsize=10)
        ax2.set_xlabel(r"Multipole $\ell$", fontsize=13)
        ax2.set_xlim(*xlim)
    else:
        ax2.set_visible(False)

    plt.tight_layout()
    out = os.path.join(FIG_DIR, outname)
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  Figura guardada: {out}")


def plot_spectrum(ells_s, Dl_s, ells_l, Dl_l, ell_obs, Dl_obs, sigma_obs):
    _spectrum_figure(
        ells_s, Dl_s, ells_l, Dl_l, ell_obs, Dl_obs, sigma_obs,
        ylabel=r"$D_\ell^{TT}$ [$\mu$K$^2$]",
        title="SSEE vs Planck 2018: CMB TT Power Spectrum",
        outname="fig_cmb_spectrum.pdf",
        ylim=(0, 6500),
        ssee_label=r"SSEE ($\Omega_{m,\rm CMB}=0.308881$)",
        lcdm_label=r"$\Lambda$CDM ($\Omega_m=0.315$)",
    )


def plot_te_spectrum(ells_s, Dl_s, ells_l, Dl_l, ell_obs, Dl_obs, sigma_obs):
    _spectrum_figure(
        ells_s, Dl_s, ells_l, Dl_l, ell_obs, Dl_obs, sigma_obs,
        ylabel=r"$D_\ell^{TE}$ [$\mu$K$^2$]",
        title="SSEE vs Planck 2018: CMB TE Power Spectrum",
        outname="fig_cmb_te.pdf",
        ssee_label=r"SSEE",
        lcdm_label=r"$\Lambda$CDM",
    )


def plot_ee_spectrum(ells_s, Dl_s, ells_l, Dl_l, ell_obs, Dl_obs, sigma_obs):
    _spectrum_figure(
        ells_s, Dl_s, ells_l, Dl_l, ell_obs, Dl_obs, sigma_obs,
        ylabel=r"$D_\ell^{EE}$ [$\mu$K$^2$]",
        title="SSEE vs Planck 2018: CMB EE Power Spectrum",
        outname="fig_cmb_ee.pdf",
        ssee_label=r"SSEE",
        lcdm_label=r"$\Lambda$CDM",
    )


def plot_lensing(ells_s, Cl_s, ells_l, Cl_l, ell_obs, Cl_obs, sigma_obs):
    """Lensing potential power spectrum [L(L+1)]^2 C_L^phiphi / (2pi).

    Both CAMB outputs (Cl_s, Cl_l) and observed data (Cl_obs) are already in
    [L(L+1)]^2 C_L^phiphi / (2pi) units — no additional transformation needed.
    """
    fig, axes = plt.subplots(2, 1, figsize=(10, 7),
                             gridspec_kw={"height_ratios": [3, 1]})
    ax = axes[0]

    if ell_obs is not None and Cl_obs is not None:
        ax.errorbar(ell_obs, Cl_obs * 1e7, yerr=sigma_obs * 1e7,
                    fmt="k.", ms=5, lw=1.0, alpha=0.8, label="Planck 2018",
                    capsize=3)

    m_l = ells_l > 1
    m_s = ells_s > 1
    ax.plot(ells_l[m_l], Cl_l[m_l] * 1e7,
            color="tab:orange", lw=1.5, ls="--", label=r"$\Lambda$CDM")
    ax.plot(ells_s[m_s], Cl_s[m_s] * 1e7,
            color="tab:blue", lw=1.8, label=r"SSEE")
    ax.set_xlim(2, 1300)
    ax.set_ylabel(r"$[L(L+1)]^2 C_L^{\phi\phi} / (2\pi)\ [\times 10^{-7}]$", fontsize=11)
    ax.set_title("SSEE vs Planck 2018: CMB Lensing Potential", fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    ax2 = axes[1]
    if ell_obs is not None and Cl_obs is not None and sigma_obs is not None:
        Cl_s_interp = np.interp(ell_obs, ells_s, Cl_s)
        res = (Cl_s_interp - Cl_obs) / sigma_obs
        ax2.plot(ell_obs, res, "b.", ms=5, alpha=0.7)
        ax2.axhline(0,  color="k",    lw=0.8)
        ax2.axhline(+1, color="gray", lw=0.6, ls="--")
        ax2.axhline(-1, color="gray", lw=0.6, ls="--")
        ax2.set_ylim(-4, 4)
        ax2.set_ylabel(r"$(C_L^{\rm SSEE}-C_L^{\rm Planck})/\sigma$", fontsize=10)
        ax2.set_xlabel(r"Multipole $L$", fontsize=13)
        ax2.set_xlim(2, 1300)
        ax2.grid(True, alpha=0.3)
    else:
        ax2.set_visible(False)

    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig_cmb_lensing.pdf")
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  Figura guardada: {out}")


def plot_peak_zoom(ells_s, Dl_s, ells_l, Dl_l, ell_obs, Dl_obs, sigma_obs):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    ranges = [(150, 350, 220), (420, 650, 540), (700, 950, 810)]
    labels = ["1er pico", "2do pico", "3er pico"]

    for ax, (lo, hi, expected), lbl in zip(axes, ranges, labels):
        if ell_obs is not None:
            m = (ell_obs >= lo) & (ell_obs <= hi)
            ax.errorbar(ell_obs[m], Dl_obs[m], yerr=sigma_obs[m],
                        fmt="k.", ms=3, lw=0.7, alpha=0.7)
        m_s = (ells_s >= lo) & (ells_s <= hi)
        m_l = (ells_l >= lo) & (ells_l <= hi)
        ax.plot(ells_l[m_l], Dl_l[m_l], "tab:orange", lw=1.5, ls="--")
        ax.plot(ells_s[m_s], Dl_s[m_s], "tab:blue", lw=1.8)
        ax.axvline(expected, color="green", lw=0.8, ls=":", alpha=0.7,
                   label=rf"$\ell={expected}$")
        ax.set_title(lbl, fontsize=12)
        ax.set_xlabel(r"$\ell$")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

    axes[0].set_ylabel(r"$D_\ell^{TT}$ [$\mu$K$^2$]")
    plt.suptitle("SSEE: Zoom en Picos Acústicos vs Planck 2018", fontsize=13)
    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig_cmb_peaks_zoom.pdf")
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  Figura guardada: {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("SSEE — Paper 3: CMB vs Planck 2018 (TT+TE+EE+lensing)")
    print("=" * 60)
    print(f"\nParámetros SSEE:")
    print(f"  w0={w0:.4f}  wa={wa:.4f}")
    print(f"  s_m=1+w0={s_m:.4f}  (ecuación de estado, NO densidad)  Ω_DE={OmDE:.4f}")
    print(f"  MIRA={MIRA:.6f}  (AURA/2 — Frecuencia de Observación, Genesis 5.12)")
    print(f"  Ω_m,CMB={Omm_cmb:.6f}  (sector observacional: CMB, Planck: 0.3153)")
    print(f"  M_SSEE=|w0|={M_SSEE:.4f}")
    print(f"  KAL0={KAL0:.4f}")

    # 1. Descargar datos Planck
    download_planck()
    (ell_tt, Dl_tt, sig_tt), \
    (ell_te, Dl_te, sig_te), \
    (ell_ee, Dl_ee, sig_ee), \
    (ell_lens, Cl_lens, sig_lens) = load_planck()

    if ell_tt is not None:
        print(f"\nDatos Planck 2018 TT: {len(ell_tt)} puntos, ℓ={ell_tt[0]}–{ell_tt[-1]}")
    if ell_te is not None:
        print(f"Datos Planck 2018 TE: {len(ell_te)} puntos")
    if ell_ee is not None:
        print(f"Datos Planck 2018 EE: {len(ell_ee)} puntos")
    if ell_lens is not None:
        print(f"Datos Planck 2018 lensing: {len(ell_lens)} puntos")

    # 2. Calcular espectros SSEE
    print("\nCalculando espectros SSEE con CAMB (TT+TE+EE+lensing)...")
    ells_s, total_s, lens_s, r_d_raw, derived = compute_ssee_spectrum()
    Dl_TT_s = total_s[:, 0]   # TT lensed
    Dl_EE_s = total_s[:, 1]   # EE lensed
    Dl_TE_s = total_s[:, 3]   # TE lensed
    # lensing potential: CAMB lens_potential_cls col 0 = phiphi
    Cl_pp_s = lens_s[:, 0]
    ells_lens_s = np.arange(len(Cl_pp_s))

    print(f"  r_d,SSEE (CAMB)   = {r_d_raw:.2f} Mpc  (Planck: ~147.1 Mpc)")
    print(f"  z_drag            = {derived.get('zdrag', 'N/A'):.2f}")
    print(f"  100θ_MC           = {derived.get('thetastar', derived.get('theta_MC_100', 'N/A'))}")

    # 3. Calcular espectros ΛCDM
    print("\nCalculando espectros ΛCDM con CAMB...")
    ells_l, total_l, lens_l, r_d_lcdm = compute_lcdm_spectrum()
    Dl_TT_l = total_l[:, 0]
    Dl_EE_l = total_l[:, 1]
    Dl_TE_l = total_l[:, 3]
    Cl_pp_l = lens_l[:, 0]
    ells_lens_l = np.arange(len(Cl_pp_l))
    print(f"  r_d,ΛCDM = {r_d_lcdm:.2f} Mpc")

    # 4. Chi2 total por espectro
    print("\n--- χ² vs Planck 2018 ---")
    chi2_results = {}
    total_chi2_s = 0
    total_chi2_l = 0
    total_N = 0

    for label, ell_o, Dl_o, sig_o, Dl_model_s, Dl_model_l, ell_model, \
        ell_min, ell_max in [
        ("TT", ell_tt,  Dl_tt,  sig_tt,  Dl_TT_s, Dl_TT_l, ells_s,      30, 2000),
        ("TE", ell_te,  Dl_te,  sig_te,  Dl_TE_s, Dl_TE_l, ells_s,      30, 2000),
        ("EE", ell_ee,  Dl_ee,  sig_ee,  Dl_EE_s, Dl_EE_l, ells_s,      30, 2000),
        ("PP", ell_lens,Cl_lens,sig_lens,Cl_pp_s, Cl_pp_l, ells_lens_s,  8,  400),
    ]:
        if ell_o is None:
            print(f"  {label}: datos no disponibles")
            continue
        chi2_s, chi2r_s, n = chi2_vs_planck(ell_o, Dl_o, sig_o, ell_model, Dl_model_s,
                                              ell_min=ell_min, ell_max=ell_max)
        chi2_l, chi2r_l, _ = chi2_vs_planck(ell_o, Dl_o, sig_o, ell_model, Dl_model_l,
                                              ell_min=ell_min, ell_max=ell_max)
        print(f"  {label}:  SSEE χ²_r={chi2r_s:.3f} (χ²={chi2_s:.1f})  |  ΛCDM χ²_r={chi2r_l:.3f} (χ²={chi2_l:.1f})  (N={n})")
        chi2_results[label] = (chi2_s, chi2r_s, chi2_l, chi2r_l, n)
        total_chi2_s += chi2_s
        total_chi2_l += chi2_l
        total_N += n

    if total_N > 0:
        print(f"\n  COMBINADO:  SSEE χ²_r={total_chi2_s/total_N:.3f}  |  "
              f"ΛCDM χ²_r={total_chi2_l/total_N:.3f}  (N_total={total_N})")
        # BIC (k=2 for SSEE since H0 and Obh2 were inferred; k_LCDM=6)
        k_ssee  = 2
        k_lcdm  = 6
        BIC_ssee = total_chi2_s + k_ssee  * np.log(total_N)
        BIC_lcdm = total_chi2_l + k_lcdm  * np.log(total_N)
        dBIC = BIC_ssee - BIC_lcdm
        print(f"  ΔBIC(SSEE−ΛCDM) = {dBIC:.1f}  (negativo = SSEE favorecido)")
        # Log con acta (2026-09-30): los chi2 sin redondear que cita Paper 3
        import json as _json
        from procedencia import con_acta as _con_acta
        pk = dict(ssee=picos(ells_s, Dl_TT_s), lcdm=picos(ells_l, Dl_TT_l))
        _out = dict(fecha=str(__import__("datetime").date.today()),
                    picos_TT=pk,
                    espectros={k: dict(chi2_ssee=v[0], chi2r_ssee=v[1], chi2_lcdm=v[2],
                                       chi2r_lcdm=v[3], N=v[4], dchi2=v[0] - v[2],
                                       dchi2r=v[1] - v[3])
                               for k, v in chi2_results.items()},
                    total=dict(chi2_ssee=total_chi2_s, chi2_lcdm=total_chi2_l, N=total_N,
                               chi2r_ssee=total_chi2_s / total_N, chi2r_lcdm=total_chi2_l / total_N,
                               dchi2r=(total_chi2_s - total_chi2_l) / total_N,
                               k_ssee=k_ssee, k_lcdm=k_lcdm,
                               penalizacion_dk_lnN=float((k_ssee - k_lcdm) * np.log(total_N)),
                               dBIC=float(dBIC)))
        _json.dump(_con_acta(_out, __file__),
                   open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                     "results", "logs", "paper3_cmb_chi2.json"), "w"), indent=1)

    # 5. Posiciones de picos TT
    print("\nPosición de picos TT SSEE (primeros 3):")
    from scipy.signal import argrelmax
    peaks_idx = argrelmax(Dl_TT_s[50:1500], order=60)[0] + 50
    for i, idx in enumerate(peaks_idx[:3]):
        print(f"  Pico {i+1}: ℓ={ells_s[idx]}  Dℓ={Dl_TT_s[idx]:.1f} μK²")

    # 6. Figuras
    print("\nGenerando figuras...")
    plot_spectrum(ells_s, Dl_TT_s, ells_l, Dl_TT_l, ell_tt, Dl_tt, sig_tt)
    plot_te_spectrum(ells_s, Dl_TE_s, ells_l, Dl_TE_l, ell_te, Dl_te, sig_te)
    plot_ee_spectrum(ells_s, Dl_EE_s, ells_l, Dl_EE_l, ell_ee, Dl_ee, sig_ee)
    plot_lensing(ells_lens_s, Cl_pp_s, ells_lens_l, Cl_pp_l, ell_lens, Cl_lens, sig_lens)
    plot_peak_zoom(ells_s, Dl_TT_s, ells_l, Dl_TT_l, ell_tt, Dl_tt, sig_tt)

    print("\n✓ Listo. TT + TE + EE + lensing completados.")


if __name__ == "__main__":
    from procedencia import cabecera as _cab
    print(_cab(__file__), flush=True)   # acta de procedencia: primera linea del log
    main()
