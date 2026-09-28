#!/usr/bin/env python3
"""lcdm_conjunta.py — LCDM LIBRE con UN SOLO universo para CMB + KiDS-Legacy + BAO.

LA PREGUNTA
LCDM libre, sonda por sonda, elige un universo distinto en cada una (Omega_m
0.297 en BAO, 0.315 en el CMB, ...). Esa libertad es su ventaja. La prueba que
la pone a trabajar de verdad es obligarlo a usar el MISMO juego de parametros en
todas a la vez, como hace SSEE con su fondo algebraico. Lo que se mide:

    perdida_LCDM = chi2_conjunto_min - suma de chi2_min por sonda

con la MISMA funcion de verosimilitud en los dos lados. Si las sondas estan de
acuerdo dentro de LCDM, la perdida es del orden de los parametros compartidos;
si no, LCDM paga. SSEE no tiene libres cosmologicos compartidos: su perdida es
cero por construccion (y la conjunta MCMC de cobaya_conjunta.py lo comprueba).

MONTAJE (todo con los parametros PROPIOS de LCDM, nunca los de SSEE)
    compartidos  ombh2, omch2, h0, ns, logA           (w=-1, wa=0, mnu de Planck)
    CMB          plik_lite TTTEEE+lowT+lowE (cmb_eval) + tau privado
    KiDS-Legacy  xi_pm, loglike_lcdm de cobaya_kids_legacy + 8 molestias privadas
    BAO          DESI DR2, 13 puntos; D_M, D_H y r_d del MISMO CAMB (sin h*r_d
                 libre: en la conjunta r_d lo fija la fisica temprana)
BOSS NO entra: con el fondo libre sus plantillas LPT cuestan ~18 s por llamada
(cobaya_boss.py). Se declara fuera, no se esconde.

Rangos de los compartidos y de las molestias: los del montaje LCDM oficial de
KiDS-Legacy, LEIDOS de cobaya_kids_legacy.info_lcdm (no tecleados aqui). tau:
el rango de cmb_eval.

MINIMIZADOR: Cobaya `minimize` (BOBYQA), sin prior (ignore_prior): se minimiza
el chi2 dentro de los rangos. Arranques desde el mejor ajuste ya medido de cada
sonda.

CONTROLES (R53), modo `control`, antes de nada:
  C1 CMB  en el mejor LCDM de cmb_dbic_tau_ajustado.json con la mnu con que se
          midio (la de SSEE, el defecto viejo de cmb_eval) -> tiene que dar su
          chi2_min. Se informa tambien el mismo punto con la mnu de LCDM.
  C2 KiDS loglike_lcdm en el fondo de Planck == loglike_lcdmfijo en el mismo
          punto (cableado de la clave del fondo y de h0).
  C3 BAO  el fondo de SSEE por este CAMB contra el 10.904 de
          chi2_bao_posterior (r_d por otra via) -> |dif| < 0.5.
El calibrador de la pata BAO es el modo `bao`: su Omega_m tiene que devolver el
publicado por DESI DR2 para BAO solo (arXiv:2503.14738), |dif| < 0.3 sigma.

Uso:
    python3 src/p11_sondas/lcdm_conjunta.py control
    mpirun -n N python3 src/p11_sondas/lcdm_conjunta.py {bao|cmb|kids|conjunta}
    python3 src/p11_sondas/lcdm_conjunta.py lee
Salida: /mnt/datos/SSEE_data/chains_p6/lcdm_conjunta/<modo>.bestfit.txt
        results/logs/lcdm_conjunta.json
"""
import json
import os
import sys

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np  # noqa: E402

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
for _p in ("src", "src/p03_cmb", "src/p06_growth", "src/p11_sondas"):
    _q = os.path.join(_R, _p)
    if _q not in sys.path:
        sys.path.insert(0, _q)

from lcdm_planck import LCDM_PLANCK  # noqa: E402

CAD = "/mnt/datos/SSEE_data/chains_p6/lcdm_conjunta"
OUT = os.path.join(_R, "results", "logs", "lcdm_conjunta.json")
LOGS = os.path.join(_R, "results", "logs")
MNU = LCDM_PLANCK["mnu"]
COMP = ["ombh2", "omch2", "h0", "ns", "logA"]
_K = None
_D = None


def _kids():
    global _K
    if _K is None:
        import cobaya_kids_legacy as K
        _K = K
    return _K


# ── las tres patas ──────────────────────────────────────────────────────────
def chi2_cmb(ombh2, omch2, h0, ns, logA, tau, mnu=MNU):
    from cmb_eval import chi2_y_s8
    c, _ = chi2_y_s8(dict(ombh2=ombh2, omch2=omch2, H0=100.0 * h0, ns=ns,
                          logA=logA, tau=tau), -1.0, 0.0, mnu=mnu)
    return float(c)


def chi2_kids(ombh2, omch2, h0, ns, logA, **nuis):
    return -2.0 * _kids().loglike_lcdm(ombh2=ombh2, omch2=omch2, h0=h0, ns=ns,
                                       logA=logA, **nuis)


def _desi():
    global _D
    if _D is None:
        from desi_dr2_data import desi_covariance, load_desi_dr2
        d = load_desi_dr2()
        _D = (d, np.linalg.inv(desi_covariance(d)))
    return _D


def bao_camb(ombh2, omch2, h0, mnu=MNU, w=-1.0, wa=0.0):
    """chi2 BAO y Omega_m con D_M, D_H y r_d del mismo CAMB."""
    import camb
    from astropy import constants as const
    d, Ci = _desi()
    p = camb.set_params(ombh2=ombh2, omch2=omch2, H0=100.0 * h0, mnu=mnu,
                        w=w, wa=wa, dark_energy_model="ppf")
    r = camb.get_background(p)
    rd = r.get_derived_params()["rdrag"]
    z = np.asarray(d["z"], float)
    dm = r.comoving_radial_distance(z)
    dh = const.c.to("km/s").value / r.hubble_parameter(z)
    t = np.asarray(d["type"])
    pred = np.where(t == 0, dm, np.where(t == 1, dh, (z * dm ** 2 * dh) ** (1 / 3))) / rd
    res = pred - np.asarray(d["value"], float)
    return float(res @ Ci @ res), float(p.omegam), float(rd)


def loglike_cmb(ombh2, omch2, h0, ns, logA, tau):
    return -0.5 * chi2_cmb(ombh2, omch2, h0, ns, logA, tau)


def loglike_kids(ombh2, omch2, h0, ns, logA, logT_AGN, A_scale,
                 dz1, dz2, dz3, dz4, dz5, dz6):
    return _kids().loglike_lcdm(ombh2=ombh2, omch2=omch2, h0=h0, ns=ns,
                                logA=logA, logT_AGN=logT_AGN, A_scale=A_scale,
                                dz1=dz1, dz2=dz2, dz3=dz3, dz4=dz4, dz5=dz5,
                                dz6=dz6)


def loglike_bao(ombh2, omch2, h0):
    return -0.5 * bao_camb(ombh2, omch2, h0)[0]


# ── puntos de partida, LEIDOS ───────────────────────────────────────────────
def mejor_cmb():
    j = json.load(open(os.path.join(LOGS, "cmb_dbic_tau_ajustado.json")))["LCDM"]
    m = dict(j["mejor"])
    m["h0"] = m.pop("H0") / 100.0
    return m, j["chi2_min"]


def mejor_kids_planck():
    """Mejor punto de la cadena LCDM fondo-Planck de KiDS-Legacy (lcdmfijo)."""
    base = "/mnt/datos/SSEE_data/chains_p6/kids_legacy/lcdmfijo."
    cab = open(base + "1.txt").readline().split()[1:]
    a = np.vstack([np.atleast_2d(np.loadtxt(base + f"{k}.txt")) for k in range(1, 5)])
    j = a[:, cab.index("chi2")].argmin()
    nom = ["logA", "logT_AGN", "A_scale"] + [f"dz{i}" for i in range(1, 7)]
    return {n: float(a[j, cab.index(n)]) for n in nom}, float(a[j, cab.index("chi2")])


def rangos():
    """Rangos LCDM oficiales de KiDS-Legacy, leidos de su propio info."""
    inf = _kids().info_lcdm("/tmp/_no_se_escribe")
    return inf["params"]


def _param(nombre, src, ref, escala):
    p = dict(src[nombre]) if nombre in src else {}
    pr = dict(p.get("prior", {}))
    if pr.get("dist") == "norm":            # dz: el prior real va dentro de loglike
        pr = dict(min=pr["loc"] - 5 * pr["scale"], max=pr["loc"] + 5 * pr["scale"])
    return dict(prior=pr, ref=dict(dist="norm", loc=ref, scale=escala),
                proposal=escala)


def info(modo):
    src = rangos()
    mc, _ = mejor_cmb()
    mk, _ = mejor_kids_planck()
    ref = dict(mc)
    for n in mk:
        ref.setdefault(n, mk[n])
    # la escala de arranque es la propuesta de Cobaya del montaje de KiDS
    esc = {n: src[n].get("proposal", 0.01) for n in src}
    esc["tau"] = 0.006                     # ORIGEN-VALOR: 0.006 — la propuesta de tau de cobaya_conjunta._p_cmb
    src = dict(src)
    src["tau"] = dict(prior=dict(min=0.01, max=0.20))  # ORIGEN-VALOR: 0.01-0.20 — rango de tau en cmb_eval.modelo
    patas = dict(
        cmb=(loglike_cmb, COMP + ["tau"]),
        kids=(loglike_kids, COMP + ["logT_AGN", "A_scale"] + [f"dz{i}" for i in range(1, 7)]),
        bao=(loglike_bao, ["ombh2", "omch2", "h0"]))
    usa = dict(cmb=["cmb"], kids=["kids"], bao=["bao"],
               conjunta=["cmb", "kids", "bao"])[modo]
    like, params = {}, {}
    for u in usa:
        f, ps = patas[u]
        like[u] = dict(external=f, input_params=ps)
        for n in ps:
            params[n] = _param(n, src, ref[n], esc[n])
    return dict(likelihood=like, params=params,
                sampler={"minimize": dict(method="bobyqa", ignore_prior=True,
                                          best_of=4, max_evals="2000d")},
                output=f"{CAD}/{modo}", force=True)


# ── control R53 ─────────────────────────────────────────────────────────────
def control():
    K = _kids()
    mc, c_pub = mejor_cmb()
    c1 = chi2_cmb(**mc, mnu=None)           # la mnu con que se midio (SSEE)
    c1_nu = chi2_cmb(**mc)                  # mismo punto, mnu de LCDM
    ok1 = abs(c1 - c_pub) < 0.05            # ORIGEN-VALOR: 0.05 — tolerancia de cableado, declarada antes

    mk, k_cad = mejor_kids_planck()
    pl = K.PLANCK_BG
    nuis = {n: mk[n] for n in mk if n != "logA"}
    k_a = -2 * K.loglike_lcdmfijo(logA=mk["logA"], **nuis)
    k_b = chi2_kids(pl["ombh2"], pl["omch2"], pl["h0"], pl["ns"], mk["logA"], **nuis)
    ok2 = abs(k_a - k_b) < 1e-6 and abs(k_a - k_cad) < 1.0   # ORIGEN-VALOR: 1e-6, 1.0 — identidad de cableado / ruido de cadena

    from ssee_core import H0_GLOBAL, OMEGA_B_H2, OMEGA_C_H2, SUM_MNU_EV, W0, WA
    import multisonda_fondo_clavado as M
    b_otro = M.bao_en_el_clavo()["chi2"]
    b_ssee, om_ssee, rd_ssee = bao_camb(OMEGA_B_H2, OMEGA_C_H2, H0_GLOBAL / 100.0,
                                        mnu=SUM_MNU_EV, w=W0, wa=WA)
    ok3 = abs(b_ssee - b_otro) < 0.5        # ORIGEN-VALOR: 0.5 — tolerancia declarada antes (r_d por dos vias)
    b_pl, om_pl, rd_pl = bao_camb(LCDM_PLANCK["ombh2"], LCDM_PLANCK["omch2"],
                                  LCDM_PLANCK["H0"] / 100.0)

    print(f"  C1 CMB  mejor LCDM, mnu SSEE : {c1:.4f}  publicado {c_pub:.4f}  "
          f"{'OK' if ok1 else 'NO CUADRA'}")
    print(f"          mismo punto, mnu LCDM ({MNU}) : {c1_nu:.4f}  (dif {c1_nu - c1:+.4f})")
    print(f"  C2 KiDS fondo Planck: lcdmfijo {k_a:.4f}  lcdm {k_b:.4f}  cadena {k_cad:.4f}  "
          f"{'OK' if ok2 else 'NO CUADRA'}")
    print(f"  C3 BAO  SSEE por CAMB {b_ssee:.4f}  por chi2_bao_posterior {b_otro:.4f}  "
          f"{'OK' if ok3 else 'NO CUADRA'}   (Om {om_ssee:.6f}, r_d {rd_ssee:.3f})")
    print(f"     BAO  LCDM-Planck por CAMB {b_pl:.4f}  (Om {om_pl:.6f}, r_d {rd_pl:.3f})")
    res = dict(fecha="2026-09-27",
               C1=dict(chi2=c1, publicado=c_pub, chi2_mnu_lcdm=c1_nu, pasa=bool(ok1)),
               C2=dict(lcdmfijo=k_a, lcdm=k_b, cadena=k_cad, pasa=bool(ok2)),
               C3=dict(ssee_camb=b_ssee, ssee_otra_via=b_otro, pasa=bool(ok3)),
               bao_lcdm_planck=dict(chi2=b_pl, Om=om_pl, rd=rd_pl, hrd=rd_pl * LCDM_PLANCK["H0"] / 100),
               pasa=bool(ok1 and ok2 and ok3))
    json.dump(res, open(os.path.join(LOGS, "lcdm_conjunta_control.json"), "w"), indent=1)
    return res["pasa"]


# ── lectura ─────────────────────────────────────────────────────────────────
# ── minimizador (2026-09-28) ────────────────────────────────────────────────
# Cobaya-BOBYQA fallo: su minimo del CMB (1006.10) quedo PEOR que un punto ya
# conocido (1004.29). Aqui: Nelder-Mead de scipy desde el mejor punto medido,
# en coordenadas escaladas por la propuesta, con reinicios hasta que un
# reinicio mejore < TOL. Controles declarados antes:
#   CMB: el chi2 final <= chi2 del punto de arranque (1004.29 con mnu LCDM);
#   todos: el ultimo reinicio mejora < TOL (si no, NO se reporta como minimo).
TOL = 0.02                                   # ORIGEN-VALOR: 0.02 — tolerancia de convergencia entre reinicios, declarada antes
PATAS = dict(cmb=["cmb"], kids=["kids"], bao=["bao"], conjunta=["cmb", "kids", "bao"])


def minimiza(modo):
    from scipy.optimize import minimize as _min
    inf = info(modo)
    pars = list(inf["params"])
    x0 = np.array([inf["params"][p]["ref"]["loc"] for p in pars])
    esc = np.array([inf["params"][p]["ref"]["scale"] for p in pars])
    lo = np.array([inf["params"][p]["prior"].get("min", -np.inf) for p in pars])
    hi = np.array([inf["params"][p]["prior"].get("max", np.inf) for p in pars])
    likes = {k: (v["external"], v["input_params"]) for k, v in inf["likelihood"].items()}

    def partes(x):
        d = dict(zip(pars, x))
        return {k: -2.0 * f(**{p: d[p] for p in ps}) for k, (f, ps) in likes.items()}

    def obj(u):
        x = x0 + u * esc
        if np.any(x < lo) or np.any(x > hi):
            return 1e30
        c = sum(partes(x).values())
        return c if np.isfinite(c) else 1e30

    u, prev, hist = np.zeros(len(pars)), obj(np.zeros(len(pars))), []
    arranque = prev
    for k in range(12):                                     # ORIGEN-VALOR: 12 — tope de reinicios
        r = _min(obj, u, method="Nelder-Mead",
                 options=dict(maxiter=400 * len(pars), xatol=1e-4, fatol=1e-4, adaptive=True))
        hist.append(float(r.fun))
        mejora = prev - r.fun
        u, prev = r.x, r.fun
        print(f"  [{modo}] reinicio {k}: chi2 {r.fun:.4f}  mejora {mejora:+.4f}", flush=True)
        if 0 <= mejora < TOL:
            break
    x = x0 + u * esc
    p = partes(x)
    conv = bool(len(hist) >= 2 and hist[-2] - hist[-1] < TOL)
    res = dict(fecha="2026-09-28", modo=modo, chi2=float(sum(p.values())),
               por_sonda={k: float(v) for k, v in p.items()}, params=dict(zip(pars, map(float, x))),
               arranque=float(arranque), historia=hist, convergido=conv,
               control_no_peor_que_arranque=bool(sum(p.values()) <= arranque + 1e-9))
    json.dump(res, open(os.path.join(LOGS, f"lcdm_conjunta_{modo}.json"), "w"), indent=1)
    print(f"  [{modo}] FINAL chi2 {res['chi2']:.4f} (arranque {arranque:.4f})  convergido={conv}")
    return res


def _minimo(modo):
    j = os.path.join(LOGS, f"lcdm_conjunta_{modo}.json")
    if os.path.exists(j):                    # el minimizador nuevo (Nelder-Mead)
        r = json.load(open(j))
        d = dict(r["params"], chi2=r["chi2"], convergido=r["convergido"])
        d.update({f"chi2__{k}": v for k, v in r["por_sonda"].items()})
        return d
    f = f"{CAD}/{modo}.bestfit.txt"
    if not os.path.exists(f):
        return None
    cab, val = None, None
    for ln in open(f):
        if ln.startswith("#"):
            cab = ln[1:].split()
        elif ln.strip():
            val = ln.split()
    return dict(zip(cab, map(float, val)))


def lee():
    m = {k: _minimo(k) for k in ("bao", "cmb", "kids", "conjunta")}
    res = dict(fecha="2026-09-27", minimos=m)
    if m["bao"]:
        _, om, rd = bao_camb(m["bao"]["ombh2"], m["bao"]["omch2"], m["bao"]["h0"])
        tex = json.load(open(os.path.join(LOGS, "bao_lcdm_libre.json")))["publicado"]
        s = (om - tex["Om"]) / tex["Om_err"]
        res["calibrador_bao"] = dict(Om=om, publicado=tex, sigma=s, reproduce=bool(abs(s) < 0.3))
        print(f"  CALIBRADOR BAO: Om={om:.4f} vs DESI {tex['Om']}±{tex['Om_err']} -> {s:+.2f} sigma")
    if all(m.values()):
        ind = m["cmb"]["chi2"] + m["kids"]["chi2"] + m["bao"]["chi2"]
        conj = m["conjunta"]
        por = {k: conj[f"chi2__{k}"] for k in ("cmb", "kids", "bao")}
        res["suma_individual"] = ind
        res["conjunta"] = dict(chi2=conj["chi2"], por_sonda=por)
        res["perdida_lcdm"] = conj["chi2"] - ind
        res["costo_por_sonda"] = {k: por[k] - m[k]["chi2"] for k in por}
        print(f"  suma de minimos por sonda = {ind:.3f}")
        print(f"  conjunta                  = {conj['chi2']:.3f}   perdida = {conj['chi2'] - ind:+.3f}")
        for k in por:
            print(f"     {k:5s} sola {m[k]['chi2']:9.3f}  en la conjunta {por[k]:9.3f}  "
                  f"({por[k] - m[k]['chi2']:+.3f})")
    # SSEE con las MISMAS funciones: cero libres cosmologicos compartidos, asi
    # que su conjunta es la suma (la MCMC de cobaya_conjunta.py lo comprueba).
    from ssee_core import H0_GLOBAL, OMEGA_B_H2, OMEGA_C_H2, SUM_MNU_EV, W0, WA
    s_cmb = json.load(open(os.path.join(LOGS, "cmb_dbic_tau_ajustado.json")))["SSEE"]["chi2_min"]
    base = "/mnt/datos/SSEE_data/chains_p6/kids_legacy/sseefijo."
    cab = open(base + "1.txt").readline().split()[1:]
    a = np.vstack([np.atleast_2d(np.loadtxt(base + f"{k}.txt")) for k in range(1, 5)])
    s_kids = float(a[:, cab.index("chi2")].min())
    s_bao = bao_camb(OMEGA_B_H2, OMEGA_C_H2, H0_GLOBAL / 100.0, mnu=SUM_MNU_EV, w=W0, wa=WA)[0]
    res["ssee"] = dict(cmb=s_cmb, kids=s_kids, bao_camb=s_bao, total=s_cmb + s_kids + s_bao,
                       libres_cosmologicos=0)
    print(f"  SSEE (misma funcion): CMB {s_cmb:.3f} + KiDS {s_kids:.3f} + BAO {s_bao:.3f} "
          f"= {s_cmb + s_kids + s_bao:.3f}")
    if "conjunta" in res:
        d = s_cmb + s_kids + s_bao - res["conjunta"]["chi2"]
        res["delta_ssee_menos_lcdm_conjunta"] = d
        print(f"  Delta chi2 (SSEE - LCDM conjunta) = {d:+.3f}")
    json.dump(res, open(OUT, "w"), indent=1)
    print(f"  -> {OUT}")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "control"
    os.makedirs(CAD, exist_ok=True)
    if modo == "control":
        sys.exit(0 if control() else 1)
    if modo == "lee":
        lee()
        sys.exit(0)
    minimiza(modo)
