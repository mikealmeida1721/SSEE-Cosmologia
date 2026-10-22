#!/usr/bin/env python3
"""
Pipeline de cizalla cosmica KiDS-1000 xi_pm — evaluador de likelihood independiente.

OBJETIVO: evaluar chi^2 de un modelo cosmologico arbitrario (incluido SSEE)
contra los 225 puntos de xi_pm de KiDS-1000, SIN pasar por un posterior LCDM.

CONTROL NEGATIVO OBLIGATORIO: reproducir like = -130.15735 en el punto de
maxima posterior de la cadena oficial (chain/maxpost_multinest_start_C.txt).
Hasta que eso pase, ningun resultado de este script es utilizable.

Referencias:
  Asgari et al. 2021, A&A 645, A104 (arXiv:2007.15633) — medidas xi_pm KiDS-1000
  Heymans et al. 2021, A&A 646, A140 (arXiv:2007.15632) — 3x2pt / cosmologia
  Hildebrandt et al. 2021, A&A 647, A124 (arXiv:2007.15635) — n(z) SOM gold
  Mead et al. 2015, MNRAS 454, 1958 — HMcode
  Bridle & King 2007, NJP 9, 444 — alineamiento intrinseco NLA
"""
# ORIGEN: /mnt/datos/SSEE_data/kids1000/KiDS1000_cosmis_shear_data_release/chains_and_config_files/main_chains_iterative_covariance/xipm/chain/maxpost_multinest_start_C.txt
import numpy as np
from astropy.io import fits
from scipy.integrate import simpson
from scipy.interpolate import InterpolatedUnivariateSpline as IUS
from scipy.special import jv
import camb

DATA_K1000 = ('/mnt/datos/SSEE_data/kids1000/KiDS1000_cosmis_shear_data_release/'
              'data_fits/xipm_KIDS1000_BlindC_with_m_bias_V1.0.0A_ugriZYJHKs_photoz_'
              'SG_mask_LF_svn_309c_2Dbins_v2_goldclasses_Flag_SOM_Fid.fits')
DATA_LEGACY = ('/mnt/datos/SSEE_data/kids_legacy/'
               'KiDS_Legacy_cosmic_shear_data_release/data/KiDS_Legacy_xipm.fits')

# ---------------------------------------------------------------- datasets
# Un solo evaluador de fisica, dos conjuntos de datos. Los cortes de xi+/xi-
# y el numero de bins tomograficos salen del .ini fiducial de cada release:
#   KiDS-1000  K1K_CorrelationFunctions.data      -> 5 bins, xi+ 0.5', xi- 4'
#   KiDS-Legacy chains_and_config_files/xipm/     -> 6 bins, xi+ 2.0', xi- 4'
#               KiDS_Legacy_xipm_pipeline.ini [scale_cuts]
_DATASETS = {
    'k1000':  dict(DATA=DATA_K1000,  NZBINS=5, KEEP_XIP=(0.5, 300.0),
                   KEEP_XIM=(4.0, 300.0)),
    'legacy': dict(DATA=DATA_LEGACY, NZBINS=6, KEEP_XIP=(2.0, 300.0),
                   KEEP_XIM=(4.0, 300.0)),
}

DATA = DATA_K1000
NZBINS = 5
# cortes de escala del analisis fiducial (K1K_CorrelationFunctions.data)
KEEP_XIP = (0.5, 300.0)
KEEP_XIM = (4.0, 300.0)


def set_dataset(nombre):
    """Conmuta el release de cizalla. Por defecto queda KiDS-1000, de modo
    que todo script que ya importaba este modulo no cambia de comportamiento.
    Devuelve la configuracion aplicada para que quede escrita en el log."""
    if nombre not in _DATASETS:
        raise ValueError(f'dataset desconocido: {nombre!r}; '
                         f'validos {sorted(_DATASETS)}')
    globals().update(_DATASETS[nombre])
    globals()['DATASET'] = nombre
    return dict(_DATASETS[nombre], DATASET=nombre)


DATASET = 'k1000'
# NLA: C1 * rho_crit en unidades de h^2 Msol/Mpc^3 -> adimensional (Bridle & King)
C1_RHOCRIT = 0.0134   # Bridle & King 2007 (NJP 9, 444), valor KiDS


def load_data():
    """Vector de datos, covarianza y n(z). Devuelve todo crudo, sin cortes."""
    f = fits.open(DATA)
    C = np.array(f['COVMAT'].data, dtype=float)
    xp, xm, nz = f['xiP'].data, f['xiM'].data, f['NZ_SOURCE'].data

    def vec(t):
        # orden del fits: tal cual viene; se respeta para casar con COVMAT
        return (np.array(t['BIN1'], int), np.array(t['BIN2'], int),
                np.array(t['ANG'], float), np.array(t['VALUE'], float))

    b1p, b2p, angp, valp = vec(xp)
    b1m, b2m, angm, valm = vec(xm)

    z_low = np.array(nz['Z_LOW'], float)
    z_high = np.array(nz['Z_HIGH'], float)
    z_mid = np.array(nz['Z_MID'], float)
    dz = z_high - z_low
    # OJO: las columnas BINi suman 1 (probabilidad por bin), NO son densidad.
    # Se convierten a densidad dividiendo por dz.
    nofz = np.array([np.array(nz[f'BIN{i+1}'], float) / dz for i in range(NZBINS)])

    d = np.concatenate([valp, valm])
    return dict(C=C, d=d,
                b1=np.concatenate([b1p, b1m]), b2=np.concatenate([b2p, b2m]),
                ang=np.concatenate([angp, angm]),
                kind=np.array(['p'] * len(valp) + ['m'] * len(valm)),
                z=z_mid, nofz=nofz, dz=dz)


def scale_mask(D):
    """True donde el punto entra en el ajuste fiducial (225 de 270)."""
    m = np.zeros(len(D['d']), bool)
    isp = D['kind'] == 'p'
    m[isp] = (D['ang'][isp] >= KEEP_XIP[0]) & (D['ang'][isp] <= KEEP_XIP[1])
    m[~isp] = (D['ang'][~isp] >= KEEP_XIM[0]) & (D['ang'][~isp] <= KEEP_XIM[1])
    return m


def shift_nz(z, nofz, deltaz):
    """n_biased(z) = n(z - delta_z), renormalizada. Convencion CosmoSIS."""
    out = np.zeros_like(nofz)
    for i in range(NZBINS):
        s = IUS(z, nofz[i], k=1, ext=1)
        n = s(z - deltaz[i])
        n[n < 0] = 0.0
        out[i] = n / simpson(n, x=z)
    return out


def run_camb(omch2, ombh2, h0, ns, As, mnu=0.06, w=-1.0, wa=0.0,
             halo_A=2.6, zmax=6.0, kmax=20.0, nz_pk=100,
             dneff=0.0, meffsterile=0.0, logT_AGN=None):
    """P(k,z) no lineal con HMcode-2015 en la variante de 1 parametro de KiDS:
       c_min = halo_A ; eta_0 = 0.98 - 0.12*c_min  (Mead+2015 ec.30, valores KiDS).

    `dneff`/`meffsterile` anaden una especie termica masiva extra (canal
    `meffsterile` de CAMB). Con los dos en 0 —el defecto— esta funcion es
    IDENTICA a como estaba: `set_cosmology` no recibe ningun argumento nuevo.
    Ver `src/p06_growth/particula_que_prefiere_kids.py` para la traduccion
    (masa, temperatura) -> (dneff, meffsterile) y su control."""
    p = camb.CAMBparams()
    # OJO: NO se pasa `num_massive_neutrinos`. Este pipeline lleva UN solo
    # autoestado masivo cargando todo Sum m_nu (degeneracion 1.0147); pasar 3
    # lo convierte en tres neutrinos ligeros, que escapan mas, y mueve el P(k)
    # un 0.6% PLANO. Lo caso el control C2 de la cola #24.
    extra = (dict(nnu=3.044 + dneff, meffsterile=meffsterile)
             if meffsterile > 0.0 else {})
    p.set_cosmology(H0=h0 * 100.0, ombh2=ombh2, omch2=omch2, mnu=mnu, omk=0.0,
                    **extra)
    p.set_dark_energy(w=w, wa=wa, dark_energy_model='ppf')
    p.InitPower.set_params(As=As, ns=ns)
    zs = np.linspace(0.0, zmax, nz_pk)[::-1]
    p.set_matter_power(redshifts=zs, kmax=kmax, nonlinear=True)
    p.NonLinearModel = camb.nonlinear.Halofit()
    if logT_AGN is None:
        # HMcode-2015, variante de 1 parametro de KiDS-1000:
        #   c_min = halo_A ; eta_0 = 0.98 - 0.12*c_min (Mead+2015 ec.30)
        p.NonLinearModel.set_params(halofit_version='mead2015',
                                    HMCode_A_baryon=halo_A,
                                    HMCode_eta_baryon=0.98 - 0.12 * halo_A)
    else:
        # HMCode-2020 con retroalimentacion, parametrizada por log10(T_AGN/K).
        # Es el MISMO modelo no lineal del pipeline fiducial de KiDS-Legacy
        # (alli servido por el emulador CosmoPower entrenado sobre CAMB), asi
        # que con esta rama no hay traduccion que declarar: es el de ellos.
        p.NonLinearModel.set_params(halofit_version='mead2020_feedback',
                                    HMCode_logT_AGN=logT_AGN)
    r = camb.get_results(p)
    kh, z_pk, pk = r.get_matter_power_spectrum(minkh=1e-4, maxkh=kmax, npoints=400)
    # crecimiento D(z)/D(0) desde el P(k) LINEAL a k grande (escala segura)
    lin = camb.get_matter_power_interpolator(p, nonlinear=False, hubble_units=True,
                                             k_hunit=True, kmax=1.0, zmax=zmax)
    zg = np.linspace(0.0, zmax, 200)
    growth = np.sqrt(lin.P(zg, 0.01) / lin.P(0.0, 0.01))
    return r, p, kh, z_pk, pk, (zg, np.asarray(growth).ravel())


def cl_shear(D, res, pars, kh, z_pk, pk, growth, A_IA, deltaz, nell=60,
             ell_min=1.0, ell_max=3e4, nchi=400):
    """C_ell^ij de cizalla (GG + GI + II) por aproximacion de Limber extendida."""
    h = pars.h
    nofz = shift_nz(D['z'], D['nofz'], deltaz)
    z = D['z']

    # geometria comovil (Mpc, no Mpc/h)
    chi_of_z = IUS(z, res.comoving_radial_distance(z), k=3)
    chi = chi_of_z(z)
    chi_max = chi[-1]

    Om = (pars.omch2 + pars.ombh2 + pars.omnuh2) / h**2
    H0_c = 100.0 * h / 299792.458          # 1/Mpc

    # eficiencia de lente q_i(chi) = 1.5 Om H0^2 (chi/a) int_chi^inf n(chi') (chi'-chi)/chi'
    q = np.zeros((NZBINS, len(chi)))
    for i in range(NZBINS):
        n_chi = nofz[i] / np.gradient(chi, z)     # n(chi) = n(z) dz/dchi
        for j, c in enumerate(chi):
            sel = chi >= c
            if sel.sum() < 2:
                continue
            q[i, j] = simpson(n_chi[sel] * (chi[sel] - c) / chi[sel], x=chi[sel])
        q[i] *= 1.5 * Om * H0_c**2 * chi * (1.0 + z)

    # P(k,z) interpolado en (k [1/Mpc], z)
    from scipy.interpolate import RectBivariateSpline
    o = np.argsort(z_pk)                 # CAMB puede devolver z en cualquier orden
    zs_asc = np.asarray(z_pk)[o]
    pk_asc = np.asarray(pk)[o, :]
    spl = RectBivariateSpline(zs_asc, np.log(kh), np.log(pk_asc))

    def P(k_phys, zz):
        """P(k) en Mpc^3 con k en 1/Mpc."""
        kk = np.clip(k_phys / h, kh[0] * 1.001, kh[-1] * 0.999)
        zz = np.clip(zz, zs_asc[0], zs_asc[-1])
        return np.exp(spl.ev(zz, np.log(kk))) / h**3

    # factor de alineamiento intrinseco NLA (Bridle & King 2007):
    #   F(z) = -A_IA * C1*rho_crit * Om / D(z),  D normalizado a D(0)=1
    # A_IA puede ser un escalar (NLA clasico, un solo amplitud para todos los
    # bines) o un vector de NZBINS amplitudes. Lo segundo es como se comporta
    # el modelo NLA-M de KiDS-Legacy una vez evaluado: su amplitud efectiva por
    # bin es A * f_r,i * (M_i/M_piv)^beta, distinta en cada bin tomografico.
    zg, Dg = growth
    Dz_spl = IUS(zg, Dg, k=3)
    _base = -C1_RHOCRIT * Om / np.maximum(Dz_spl(z), 1e-6)
    _A = np.atleast_1d(np.asarray(A_IA, float))
    if _A.size == 1:
        _A = np.repeat(_A, NZBINS)
    elif _A.size != NZBINS:
        raise ValueError(f'A_IA debe ser escalar o vector de {NZBINS}; '
                         f'llego de tamano {_A.size}')
    F_IA = _A[:, None] * _base[None, :]          # (NZBINS, nz)

    ells = np.logspace(np.log10(ell_min), np.log10(ell_max), nell)
    npair = NZBINS * (NZBINS + 1) // 2
    Cl = np.zeros((npair, nell))
    idx = {}
    p_ = 0
    for i in range(NZBINS):
        for j in range(i, NZBINS):
            idx[(i + 1, j + 1)] = p_
            p_ += 1

    n_chi_all = np.array([nofz[i] / np.gradient(chi, z) for i in range(NZBINS)])

    good = chi > 1e-3
    for a, ell in enumerate(ells):
        k_phys = (ell + 0.5) / np.maximum(chi, 1e-3)
        Pk = P(k_phys, z)          # vectorizado sobre chi
        for i in range(NZBINS):
            for j in range(i, NZBINS):
                # GG + GI + IG + II con el kernel NLA
                W_i = q[i] + F_IA[i] * n_chi_all[i]
                W_j = q[j] + F_IA[j] * n_chi_all[j]
                integ = W_i * W_j / np.maximum(chi, 1e-3)**2 * Pk
                Cl[idx[(i + 1, j + 1)], a] = simpson(integ[good], x=chi[good])
    return ells, Cl, idx


# REJILLA EN l DE LA INTEGRAL DE HANKEL (2026-10-22). Era 4000 puntos log en
# [1, 3e4]. A theta grande J(l theta) oscila con periodo 2 pi/theta en l (~72 a
# 300') y la rejilla log a l alto es mucho mas gruesa: la integral NO
# convergia. Medido en el maximo de verosimilitud oficial de KiDS-Legacy,
# contra 200000 puntos: error 0.4 % a 75', 3 % a 130', 6 % a 227', 50 % a 299'
# (con 40000, igual a 200000 en los digitos mostrados). Afecta a TODO
# resultado de cizalla calculado antes de esta fecha, KiDS-1000 incluido.
N_LGRID = 40000


def xi_pm(ells, Cl, theta_arcmin, kind):
    """xi_pm(theta) = 1/(2pi) int dl l C_l J_{0,4}(l theta)."""
    th = theta_arcmin * (np.pi / 180.0 / 60.0)
    order = 0 if kind == 'p' else 4
    lgrid = np.logspace(np.log10(ells[0]), np.log10(ells[-1]), N_LGRID)
    spl = IUS(np.log(ells), np.log(np.maximum(Cl, 1e-40)), k=3)
    Cl_f = np.exp(spl(np.log(lgrid)))
    return simpson(lgrid * Cl_f * jv(order, lgrid * th), x=lgrid) / (2 * np.pi)


# ---------------------------------------------------------------- binning pesado por pares
# (2026-10-22) El pipeline oficial de KiDS-Legacy NO evalua xi(theta) en el
# centro del bin: el modulo bin_xi (KiDS_Legacy_xipm_pipeline.ini, [xip_binned]
# y [xim_binned], weighted_binning = 1) PROMEDIA xi sobre los 1000 angulos finos
# de treecorr dentro de cada uno de los 9 bins logaritmicos entre 2' y 300',
# pesando con npairs_weighted y evaluando en meanr. El ANG del FITS es el centro
# GEOMETRICO del bin; el meanr pesado cae ~6 % mas afuera (2.80' contra 2.64'
# en el primero). Evaluar en el centro era la unica diferencia declarada en
# control_legacy.py que seguia abierta, y el control por repesado
# (control_legacy_repesado.json) mostro que el sesgo de -0.42 sigma en S8 era
# del evaluador y no del alineamiento.
# Sin load_npairs(D) todo queda IGUAL que antes: theory_vector solo cambia de
# camino si D trae 'fino'.
NPAIRS_LEGACY = ('/mnt/datos/SSEE_data/kids_legacy/KiDS_Legacy_cosmic_shear_data_release/'
                 'data/cosmosis_xipm/XI_KiDS_Legacy_NScomb_nBins_6_Bin{}_Bin{}.ascii')
THETA_BORDES_LEGACY = np.logspace(np.log10(2.0), np.log10(300.0), 10)   # theta_min, theta_max, ntheta = 9 del .ini


def load_npairs(D, plantilla=NPAIRS_LEGACY, bordes=THETA_BORDES_LEGACY):
    """Adjunta a D, por punto de datos, los angulos finos (meanr) y pesos
    (npairs_weighted) de su bin angular. Devuelve D."""
    fino = []
    tablas = {}
    for n in range(len(D['d'])):
        b = (min(D['b1'][n], D['b2'][n]), max(D['b1'][n], D['b2'][n]))
        if b not in tablas:
            with open(plantilla.format(*b)) as f:
                col = f.readline().split()
            a = np.loadtxt(plantilla.format(*b), skiprows=1)
            tablas[b] = (a[:, col.index('r_nom')], a[:, col.index('meanr')],
                         a[:, col.index('npairs_weighted')])
        rnom, meanr, w = tablas[b]
        D['theta_nom'] = rnom
        k = int(np.searchsorted(bordes, D['ang'][n]) - 1)
        s = (rnom >= bordes[k]) & (rnom < bordes[k + 1])
        fino.append((meanr[s], w[s] / w[s].sum()))
    D['fino'] = fino
    return D


_JCACHE = {}


def xi_pm_tabla(ells, Cl, theta_arcmin, kind):
    """xi_pm en MUCHOS angulos a la vez: la misma integral de xi_pm (misma
    rejilla en l, mismo spline de C_l, Simpson) hecha como producto matricial."""
    th = np.asarray(theta_arcmin, float) * (np.pi / 180.0 / 60.0)
    order = 0 if kind == 'p' else 4
    lgrid = np.logspace(np.log10(ells[0]), np.log10(ells[-1]), N_LGRID)
    spl = IUS(np.log(ells), np.log(np.maximum(Cl, 1e-40)), k=3)
    Cl_f = np.exp(spl(np.log(lgrid)))
    clave = (order, float(ells[0]), float(ells[-1]), th.tobytes())
    if clave not in _JCACHE:
        if len(_JCACHE) > 64:
            _JCACHE.clear()
        _JCACHE[clave] = jv(order, np.outer(lgrid, th))
    return simpson((lgrid * Cl_f)[:, None] * _JCACHE[clave], x=lgrid, axis=0) / (2 * np.pi)


def theory_vector(D, ells, Cl, idx, delta_c=0.0):
    if 'fino' in D:
        return _theory_vector_pesado(D, ells, Cl, idx, delta_c)
    t = np.zeros(len(D['d']))
    for n in range(len(D['d'])):
        p_ = idx[(min(D['b1'][n], D['b2'][n]), max(D['b1'][n], D['b2'][n]))]
        t[n] = xi_pm(ells, Cl[p_], D['ang'][n], D['kind'][n])
        if D['kind'][n] == 'p':
            t[n] += delta_c**2          # termino c aditivo (xip_add_c_term = 1)
    return t


_WCACHE = {}


def _xi_nom(ells, Cl, theta_arcmin, kind):
    """xi en los angulos nominales comunes como UN producto matriz-vector: los
    pesos de la regla del trapecio en l, el factor l y J(l theta) van dentro de
    una matriz que se arma una vez por (orden, rango de l). Con la rejilla de
    N_LGRID = 40000 ya convergida, trapecio y Simpson coinciden en chi2 (medido
    en control_legacy_repesado.py); Simpson con axis=0 armaba una temporal de
    320 MB por par y tardaba 32 s por vector de teoria."""
    order = 0 if kind == 'p' else 4
    clave = (order, float(ells[0]), float(ells[-1]), np.asarray(theta_arcmin).tobytes())
    lgrid = np.logspace(np.log10(ells[0]), np.log10(ells[-1]), N_LGRID)
    if clave not in _WCACHE:
        if len(_WCACHE) > 4:
            _WCACHE.clear()
        th = np.asarray(theta_arcmin, float) * (np.pi / 180.0 / 60.0)
        w = np.zeros(N_LGRID)
        dl = np.diff(lgrid)
        w[:-1] += dl / 2
        w[1:] += dl / 2
        _WCACHE[clave] = (w * lgrid)[:, None] * jv(order, np.outer(lgrid, th)) / (2 * np.pi)
    spl = IUS(np.log(ells), np.log(np.maximum(Cl, 1e-40)), k=3)
    return np.exp(spl(np.log(lgrid))) @ _WCACHE[clave]


def _theory_vector_pesado(D, ells, Cl, idx, delta_c=0.0):
    """Como theory_vector, pero cada punto es el promedio de xi sobre los
    angulos finos de su bin, pesado por npairs_weighted (bin_xi oficial)."""
    t = np.zeros(len(D['d']))
    grupos = {}
    for n in range(len(D['d'])):
        p_ = idx[(min(D['b1'][n], D['b2'][n]), max(D['b1'][n], D['b2'][n]))]
        grupos.setdefault((p_, D['kind'][n]), []).append(n)
    for (p_, kind), ns in grupos.items():
        th = np.concatenate([D['fino'][n][0] for n in ns])
        # Los 1000 angulos NOMINALES de treecorr (r_nom) son los mismos para
        # los 21 pares: la matriz de Bessel se arma UNA vez por orden y se
        # reusa. meanr difiere de r_nom hasta 3e-4 relativo; se pasa con
        # interpolacion lineal en log(theta). Medido en el maximo oficial:
        # una rejilla maestra de 300 angulos con spline movia chi2 en 0.41
        # (407.26 contra 407.67 del calculo directo en cada meanr) — no sirve
        # para un control; esta forma se mide igual en control_legacy_repesado.py.
        xi_c = _xi_nom(ells, Cl[p_], D['theta_nom'], kind)
        xi = np.interp(np.log(th), np.log(D['theta_nom']), xi_c)
        i = 0
        for n in ns:
            th_n, w_n = D['fino'][n]
            t[n] = float(np.dot(w_n, xi[i:i + len(th_n)]))
            i += len(th_n)
            if kind == 'p':
                t[n] += delta_c**2
    return t


def chi2(D, theory, mask):
    dv = (theory - D['d'])[mask]
    Ci = np.linalg.inv(D['C'][np.ix_(mask, mask)])
    return float(dv @ Ci @ dv)


if __name__ == '__main__':
    D = load_data()
    m = scale_mask(D)
    print(f'puntos totales {len(D["d"])}  usados {m.sum()} '
          f'(xi+ {(m & (D["kind"]=="p")).sum()}, xi- {(m & (D["kind"]=="m")).sum()})')
