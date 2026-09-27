#!/usr/bin/env python3
"""
LAS CUATRO SONDAS A LA VEZ, CON EL FONDO UNIFICADO CLAVADO.

===========================================================================
QUE PREGUNTA ES ESTA, Y QUE PREGUNTA NO ES  (encargo de Mike, 2026-09-26)
===========================================================================
Textual: «vamos a poner todas las sondas BAO, CMB, KiDS-Legacy y BOSS con el
fondo unificado clavado para saber si las sondas tienen sesgos. Ya lo hicimos
de manera individual y cada una esta de acuerdo con el fondo viendo sus chi2.
Lo que busco es saber si las sondas EN CONJUNTO tambien dan los mismos chi2.
**Esto no es una prueba para el modelo, es una prueba para la combinacion de
sondas con el fondo unificado fijo.**»

Esa ultima frase manda sobre el diseno, y obliga a separar dos cosas que se
confunden todo el rato:

  (A) Que las sondas se contradigan ENTRE SI            -> sesgo de SONDA
  (B) Que todas se desvien JUNTAS en la misma direccion -> problema del MODELO

Un estadistico que las sume no distingue. Por eso se calculan aparte, y el
titular es (A), que es lo que Mike pidio. (B) se reporta al lado, etiquetado
como lo que es, para no colar una prueba del modelo disfrazada.

===========================================================================
POR QUE NO BASTA CON SUMAR LOS chi2
===========================================================================
Con el fondo clavado al 100% y cada sonda con SUS PROPIOS nuisances, el chi2
conjunto es IDENTICAMENTE la suma de los individuales. Sumar no aporta nada:
el numero saldria bien por construccion. Lo que hace que la pregunta tenga
contenido es que hay un parametro COMPARTIDO de verdad: la amplitud A_s, que
ven el CMB, KiDS-Legacy y BOSS. El eje de la prueba es ese.

  · CMB, KiDS-Legacy, BOSS -> cada una mide logA por su cuenta, con el MISMO
    fondo clavado y con sus propios nuisances marginalizados. Si las tres
    miden la misma cantidad y discrepan, eso es sesgo entre sondas.
  · BAO no ve A_s: es geometria pura. Entra por el otro eje, como bondad de
    ajuste del fondo clavado, y se dice explicitamente que no vota en A_s.

===========================================================================
LOS DOS ESTADISTICOS
===========================================================================
Sea logA_i +- sigma_i la medida de cada sonda del eje amplitud (i = CMB,
KiDS-Legacy, BOSS), todas con el MISMO fondo clavado.

  ESTADISTICO 1 — DISCORDIA ENTRE SONDAS  (el que Mike pidio)
      logA_comun = sum(logA_i/sigma_i^2) / sum(1/sigma_i^2)
      T_sondas   = sum_i (logA_i - logA_comun)^2 / sigma_i^2      ~ chi2(N-1)
    Quita el modo comun, asi que NO puede castigar al modelo: mide solo si las
    sondas se contradicen entre ellas. Es el estadistico model-independent.

  ESTADISTICO 2 — MODO COMUN vs EL CLAVO  (prueba del MODELO, va aparte)
      T_modelo = (logA_comun - logA_clavado)^2 / sigma_comun^2    ~ chi2(1)
    Esto SI es una prueba del modelo. Se reporta etiquetado, no sumado.

===========================================================================
CONTROL DEL OTRO LADO (R53) — sin esto el numero no vale
===========================================================================
Un T_sondas pequeno no significa nada si el estadistico no sabe detectar una
discordia cuando la hay. Se repite el MISMO calculo con las cadenas de fondo
LCDM-clavado (kids_legacy/lcdmfijo, boss/lcdm), que son las mismas sondas con
la misma rigidez y otro fondo. Si T_sondas sale igual en los dos, el
estadistico no discrimina y no se puede concluir nada de el.

===========================================================================
DE DONDE SALE CADA NUMERO — nada tecleado (R65)
===========================================================================
  CMB           results/chains/ssee_cmb.[1-4].txt         col logA, col chi2
  KiDS-Legacy   chains_p6/kids_legacy/ssee.[1-4].txt      col logA, col chi2
  KiDS clavado  chains_p6/kids_legacy/sseefijo.[1-4].txt  logA FIJO -> chi2
  BOSS          chains_p6/boss/ssee.[1-4].txt             col logA, col chi2
  BAO           chi2_bao_posterior.chi2_bao(H0, obh2), 13 pts DESI DR2
  logA clavado  CANONICAL_VALUES.yaml : logA_cmb_ssee
"""
import glob
import json
import os
import sys

import numpy as np
import yaml
from scipy.stats import chi2 as _chi2dist

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "src"))
sys.path.insert(0, os.path.join(_REPO, "src", "p02_mcmc"))

_CAD = "/mnt/datos/SSEE_data/chains_p6"
_QUEMA = 0.3          # burn-in descartado, fraccion de cada cadena
_LOG = os.path.join(_REPO, "results", "logs", "multisonda_fondo_clavado.json")

_lineas = []


def di(s=""):
    print(s)
    _lineas.append(s)


# ── el clavo, leido del canonico ────────────────────────────────────────────
def _canon(clave):
    _cv = yaml.safe_load(open(os.path.join(_REPO, "CANONICAL_VALUES.yaml")))
    for _b in _cv.values():
        if isinstance(_b, dict) and clave in _b:
            return float(_b[clave])
    raise KeyError(clave)


LOGA_CLAVADO = _canon("logA_cmb_ssee")


# ── lectura de cadenas ──────────────────────────────────────────────────────
def lee(patron):
    """Devuelve (cols, array apilado) descartando el burn-in de CADA cadena."""
    fs = sorted(glob.glob(patron))
    if not fs:
        raise FileNotFoundError(patron)
    cols = open(fs[0]).readline().lstrip("#").split()
    trozos = []
    for f in fs:
        a = np.loadtxt(f)
        if a.ndim == 1:
            a = a[None, :]
        trozos.append(a[int(len(a) * _QUEMA):])
    return cols, np.vstack(trozos), len(fs)


def medida(patron, etiqueta):
    """logA +- sigma (marginalizado sobre los nuisances de ESA sonda) y su chi2
    minimo, leidos de la cadena. Nada se recalcula: la cadena es el origen."""
    cols, a, ncad = lee(patron)
    w = a[:, 0]
    x = a[:, cols.index("logA")]
    c2 = a[:, cols.index("chi2")]
    m = float(np.average(x, weights=w))
    s = float(np.sqrt(np.average((x - m) ** 2, weights=w)))
    return dict(sonda=etiqueta, logA=m, sigma=s, chi2_min=float(c2.min()),
                n_muestras=int(len(x)), n_cadenas=ncad,
                logA_en_min=float(x[int(np.argmin(c2))]))


def chi2_en_el_clavo(patron, etiqueta, ancho=None):
    """chi2 de la sonda CON logA en el valor clavado.

    Si la cadena ya tiene logA fijo (no aparece como columna), su chi2 minimo
    ES el del clavo. Si logA es libre, se toma el minimo entre las muestras que
    caen en una banda estrecha alrededor del clavo: es un perfil LEIDO de la
    cadena, y por tanto una COTA SUPERIOR del minimo verdadero (el MCMC no
    visita el optimo exacto). Queda declarado como tal, no disimulado."""
    cols, a, _ = lee(patron)
    c2 = a[:, cols.index("chi2")]
    if "logA" not in cols:
        return dict(sonda=etiqueta, chi2=float(c2.min()), modo="logA fijo en la corrida",
                    exacto=True, n_en_banda=int(len(c2)))
    x = a[:, cols.index("logA")]
    if ancho is None:
        ancho = 0.15 * float(np.sqrt(np.average(
            (x - np.average(x, weights=a[:, 0])) ** 2, weights=a[:, 0])))
    sel = np.abs(x - LOGA_CLAVADO) < ancho
    if sel.sum() < 30:
        sel = np.abs(x - LOGA_CLAVADO) < 3 * ancho
    return dict(sonda=etiqueta, chi2=float(c2[sel].min()),
                modo=f"perfil leido de la cadena, banda +-{ancho:.4f}",
                exacto=False, n_en_banda=int(sel.sum()))


def degeneracion(patron, etiqueta, param="logA"):
    """D = anchura marginal / anchura condicional, de la MISMA cadena.

    D ~ 1  -> la sonda mide el parametro por si misma.
    D >> 1 -> casi toda su anchura viene de no poder separarlo de otro: lo que
              mide es una COMBINACION, y donde cae su valor central depende de
              por donde se haya deslizado. Hay que saberlo ANTES de comparar
              dos sondas, o se comparan cosas que no son la misma."""
    cols, a, _ = lee(patron)
    w = a[:, 0]
    ig = ("weight", "minuslogpost", "sigma8", "H0")
    idx = [i for i, c in enumerate(cols)
           if c not in ig and not c.startswith(("minuslogprior", "chi2"))]
    nom = [cols[i] for i in idx]
    X = a[:, idx]
    C = np.cov(X.T, aweights=w)
    j = nom.index(param)
    marg = float(np.sqrt(C[j, j]))
    cond = float(1.0 / np.sqrt(np.linalg.inv(C)[j, j]))
    r = C[j] / np.sqrt(np.diag(C) * C[j, j])
    o = [k for k in np.argsort(-np.abs(r)) if nom[k] != param][:2]
    return dict(sonda=etiqueta, marginal=marg, condicional=cond, D=marg / cond,
                enredado_con=[(nom[k], float(r[k])) for k in o])


def perfil(patron, etiqueta, nbins=40):
    """Perfil de verosimilitud en logA LEIDO de la cadena: minimo de chi2 en
    cada bin. Da el valor SIN efecto de proyeccion --- que es lo que hay que
    comparar entre sondas cuando las degeneraciones difieren--- y su anchura
    por el corte Delta chi2 = 1.

    Es una COTA SUPERIOR del perfil verdadero (el MCMC no visita el optimo
    exacto de cada bin) y algo ruidoso en las colas. Declarado, no disimulado."""
    cols, a, _ = lee(patron)
    x, c2 = a[:, cols.index("logA")], a[:, cols.index("chi2")]
    bins = np.linspace(np.percentile(x, 0.5), np.percentile(x, 99.5), nbins)
    ib = np.digitize(x, bins)
    pr = np.array([c2[ib == k].min() if (ib == k).sum() > 5 else np.nan
                   for k in range(1, len(bins))])
    ctr = 0.5 * (bins[1:] + bins[:-1])
    ok = ~np.isnan(pr)
    ctr, pr = ctr[ok], pr[ok]
    k = int(np.argmin(pr))
    d = pr - pr[k]
    # anchura por Delta chi2 = 1, a cada lado, promediada
    def cruce(lado):
        if lado == "izq":
            xx, dd = ctr[:k + 1][::-1], d[:k + 1][::-1]
        else:
            xx, dd = ctr[k:], d[k:]
        j = np.argmax(dd >= 1.0)
        if dd.max() < 1.0 or j == 0:
            return np.nan
        return abs(np.interp(1.0, [dd[j - 1], dd[j]], [xx[j - 1], xx[j]]) - ctr[k])
    anchos = [v for v in (cruce("izq"), cruce("der")) if not np.isnan(v)]
    return dict(sonda=etiqueta, logA=float(ctr[k]), chi2_min=float(pr[k]),
                sigma=float(np.mean(anchos)) if anchos else float("nan"),
                lados=len(anchos))


# ── BAO: geometria pura, no ve A_s ──────────────────────────────────────────
def bao_en_el_clavo():
    import importlib.util
    ruta = os.path.join(_REPO, "src", "p02_mcmc", "chi2_bao_posterior.py")
    spec = importlib.util.spec_from_file_location("_bao", ruta)
    mod = importlib.util.module_from_spec(spec)
    import io
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    from ssee_core import H0_ALG as H_ALG, OMEGA_B_H2
    # 2026-09-27: antes llevaba obh2=0.02207 TECLEADO (el posterior viejo de P2),
    # que no es el fondo clavado: daba chi2=10.8588 en vez de 10.9040.
    c2, om = mod.chi2_bao(H_ALG, OMEGA_B_H2)
    return dict(sonda="BAO DESI DR2", chi2=float(c2), n_datos=13,
                modo=f"fondo clavado H0={H_ALG:.6f}, Om derivado={om:.6f}",
                exacto=True)


# ── los dos estadisticos ────────────────────────────────────────────────────
def estadisticos(medidas):
    x = np.array([m["logA"] for m in medidas])
    s = np.array([m["sigma"] for m in medidas])
    p = 1.0 / s ** 2
    comun = float((x * p).sum() / p.sum())
    sig_comun = float(1.0 / np.sqrt(p.sum()))
    T_sondas = float((((x - comun) ** 2) * p).sum())
    gl_sondas = len(x) - 1
    T_modelo = float((comun - LOGA_CLAVADO) ** 2 / sig_comun ** 2)
    return dict(logA_comun=comun, sigma_comun=sig_comun,
                T_sondas=T_sondas, gl_sondas=gl_sondas,
                p_sondas=float(_chi2dist.sf(T_sondas, gl_sondas)),
                sigmas_sondas=float(np.sqrt(_chi2dist.isf(
                    _chi2dist.sf(T_sondas, gl_sondas), 1))) if T_sondas > 0 else 0.0,
                T_modelo=T_modelo, gl_modelo=1,
                p_modelo=float(_chi2dist.sf(T_modelo, 1)),
                sigmas_modelo=float(np.sqrt(T_modelo)))


def tabla_tirones(medidas):
    """Cuanto y HACIA DONDE tira cada sonda respecto del clavo. El signo es lo
    que separa «las sondas se contradicen» de «todas se desvian igual»."""
    out = []
    for m in medidas:
        d = m["logA"] - LOGA_CLAVADO
        out.append(dict(sonda=m["sonda"], logA=m["logA"], sigma=m["sigma"],
                        delta=d, sigmas=d / m["sigma"],
                        direccion="arriba" if d > 0 else "abajo"))
    return out


def main():
    di("=" * 78)
    di("MULTISONDA CON EL FONDO UNIFICADO CLAVADO")
    di("Prueba de la COMBINACION de sondas, NO del modelo (encargo de Mike)")
    di("=" * 78)
    di(f"  clavo: logA = {LOGA_CLAVADO:.10f}   (CANONICAL_VALUES: logA_cmb_ssee)")
    di(f"  burn-in descartado: {_QUEMA:.0%} de cada cadena")
    di("")

    # ── eje AMPLITUD: las tres que ven A_s ──────────────────────────────────
    global PATRONES
    PATRONES = [os.path.join(_REPO, "results", "chains", "ssee_cmb.[0-9].txt"),
                f"{_CAD}/kids_legacy/ssee.[0-9].txt",
                f"{_CAD}/boss/ssee.[0-9].txt"]
    ETIQ = ["CMB (plik_lite TTTEEE+lowl+lensing)", "KiDS-Legacy xi_pm",
            "BOSS DR12 P(k) LPT"]
    med = [medida(p_, e_) for p_, e_ in zip(PATRONES, ETIQ)]
    di("EJE AMPLITUD — cada sonda mide logA con el MISMO fondo clavado")
    di(f"  {'sonda':38s} {'logA':>10s} {'sigma':>8s} {'muestras':>9s}")
    for m in med:
        di(f"  {m['sonda']:38s} {m['logA']:10.5f} {m['sigma']:8.5f} {m['n_muestras']:9d}")
    di("")

    # ── ANTES de comparar: ¿mide cada sonda lo mismo? ───────────────────────
    di("-" * 78)
    di("¿MIDE CADA SONDA EL logA, O UNA COMBINACION?  (hay que saberlo ANTES)")
    di("  D = anchura marginal / anchura condicional.  D~1 lo mide;  D>>1 no.")
    di(f"  {'sonda':38s} {'marg':>8s} {'cond':>8s} {'D':>7s}  enredado con")
    degs = [degeneracion(pat, m["sonda"]) for pat, m in zip(PATRONES, med)]
    for g in degs:
        con = ", ".join(f"{n} r={r:+.2f}" for n, r in g["enredado_con"])
        di(f"  {g['sonda']:38s} {g['marginal']:8.5f} {g['condicional']:8.5f}"
           f" {g['D']:7.2f}  {con}")
    di("")
    di("  LO QUE ESTO OBLIGA A CAMBIAR. El CMB es la MAS degenerada de las tres")
    di("  (D=11 con tau, la degeneracion A_s e^-2tau de siempre), no BOSS. Con")
    di("  degeneraciones tan distintas, comparar MEDIAS MARGINALES compara cosas")
    di("  que no son la misma: la media se desplaza hacia donde hay volumen de")
    di("  prior. Por eso abajo se calcula tambien por PERFIL, que no tiene ese")
    di("  efecto, y el titular es el del perfil.")
    di("")
    prof = [perfil(pat, m["sonda"]) for pat, m in zip(PATRONES, med)]
    di(f"  {'sonda':38s} {'marginal':>10s} {'perfil':>10s} {'desplaz.':>9s}")
    for m, pf in zip(med, prof):
        dsp = (m["logA"] - pf["logA"]) / m["sigma"]
        di(f"  {m['sonda']:38s} {m['logA']:10.5f} {pf['logA']:10.5f} {dsp:+8.2f}s")
    di("  Un desplazamiento grande = la media marginal NO es donde el dato")
    di("  prefiere: es donde el volumen de los nuisances la empuja.")
    di("")

    # ── ¿SIRVE LA ANCHURA DEL PERFIL? Prueba de imposibilidad ───────────────
    # El perfil deja moverse a TODO lo demas, asi que su anchura NUNCA puede
    # ser MENOR que la condicional, que clava todo lo demas. Si sale menor, el
    # estimador esta roto y su numero no se publica.
    di("  ¿sirve la anchura del PERFIL? (tiene que ser >= la condicional)")
    perfil_sirve = True
    for pf, g in zip(prof, degs):
        ok = pf["sigma"] >= g["condicional"]
        perfil_sirve &= ok
        di(f"    {pf['sonda']:36s} sig_perfil={pf['sigma']:.5f}"
           f"  sig_cond={g['condicional']:.5f}   {'ok' if ok else 'IMPOSIBLE'}")
    if not perfil_sirve:
        di("    -> El perfil LEIDO DE LA CADENA no sirve para anchuras: el minimo")
        di("       por bin baja mas donde hay mas muestras, o sea justo en el modo,")
        di("       y eso afila el perfil artificialmente. Sacarlo de aqui daria un")
        di("       sigma demasiado estrecho y una discordia inflada.")
        di("       SE DESCARTA el estadistico por perfil. El titular es el MARGINAL,")
        di("       que ademas es el tratamiento estandar: marginalizar sobre los")
        di("       nuisances PROPIOS de cada sonda es lo correcto, y su sigma ya")
        di("       lleva dentro el castigo de la degeneracion.")
        di("       Del perfil se conserva SOLO la posicion, como diagnostico de")
        di("       proyeccion (la tabla de arriba).")
    di("-" * 78)
    di("")

    # ── PUERTA: solo vota en amplitud quien MIDE la amplitud ────────────────
    # Lo senalo Mike: «BOSS no ve A_s, no se por que jalarla si esta fija». Y no
    # es una opinion suya: ya estaba MEDIDO en el repo antes de esta corrida
    # (mide_As_o_producto.py, memoria project_As_kids_measures_boss_slides):
    #   · BOSS D = 4.01, enredado con b1 a r = -0.89.
    #   · Su logA se DESPLAZO 1.85 sigma de su propia barra (2.7636 -> 2.9448)
    #     al pasar de media marginal a minimo de perfil. 98% metodo, 2% neutrinos.
    #   · Y esta escrito como regla: «nunca promediar KiDS con BOSS para el A_s:
    #     mezcla una medicion con un numero degenerado».
    # Meter a BOSS en el estadistico era exactamente eso. La puerta lo impide, y
    # se decide por la D MEDIDA de cada sonda, no por quien sea.
    # La puerta NO puede ser un umbral en D que me invente yo. Una D alta sola no
    # descalifica: la companera del CMB es tau, que ESTA medida por lowE, mientras
    # que la de BOSS es un sesgo que se mueve con ella. El sintoma que SI decide, y
    # que ya esta MEDIDO en el repo, es otro: ¿se mueve el valor central al cambiar
    # de estimador? Un numero que depende de con que regla lo mires no es una medida.
    DESLIZA = {   # ORIGEN: mide_As_o_producto.py + boss_aisla_neutrinos.py (09-09)
        "BOSS DR12 P(k) LPT": (1.85, "2.7636 (media marginal) -> 2.9448 (minimo de "
                                     "perfil); 98% metodo, 2% neutrinos"),
    }
    vota = [m["sonda"] not in DESLIZA for m in med]
    di("-" * 78)
    di("PUERTA DE VOTO — ¿es el logA de esta sonda una MEDIDA de A_s?")
    di("  Criterio: que su valor central NO dependa del estimador. Medido antes")
    di("  de esta corrida, no decidido aqui.")
    for m, g, v in zip(med, degs, vota):
        if v:
            di(f"  {m['sonda']:38s} D={g['D']:6.2f}   VOTA")
        else:
            _sg, _pq = DESLIZA[m["sonda"]]
            di(f"  {m['sonda']:38s} D={g['D']:6.2f}   NO VOTA — se desplazo "
               f"{_sg} sigma de su propia barra")
            di(f"  {'':38s}          {_pq}")
    di("  Lo de BOSS no es un juicio de esta corrida: esta medido en")
    di("  mide_As_o_producto.py y escrito como regla — «nunca promediar KiDS con")
    di("  BOSS para el A_s: mezcla una medicion con un numero degenerado».")
    di("  La D del CMB es alta (11.1) pero su companera es tau, que SI esta medida")
    di("  por lowE; la de BOSS es un sesgo que se desliza con ella. Por eso D sola")
    di("  no sirve de puerta.")
    di("-" * 78)
    di("")

    med_voto = [m for m, v in zip(med, vota) if v]
    est = estadisticos(med_voto)
    est_todas = estadisticos(med)          # solo para ENSENAR el dano de incluirla
    est_pf = estadisticos(prof)            # NO se publica si el perfil no valida
    di("TIRONES respecto del clavo (el SIGNO es lo que informa)")
    di(f"  {'sonda':38s} {'delta':>9s} {'sigmas':>8s}  direccion")
    for t in tabla_tirones(med):
        di(f"  {t['sonda']:38s} {t['delta']:+9.5f} {t['sigmas']:+8.2f}  {t['direccion']}")
    di("")

    di("-" * 78)
    di("ESTADISTICO 1 — DISCORDIA ENTRE SONDAS   (esto es lo que se pidio)")
    di(f"  Sondas que votan: {', '.join(m['sonda'] for m in med_voto)}")
    di(f"  logA comun = {est['logA_comun']:.5f} +- {est['sigma_comun']:.5f}   (media pesada)")
    di(f"  T_sondas = {est['T_sondas']:.3f}  con {est['gl_sondas']} g.l."
       f"   p = {est['p_sondas']:.4f}   ->  {est['sigmas_sondas']:.2f} sigma")
    di("  Quita el modo comun: NO puede castigar al modelo. Mide SOLO si las")
    di("  sondas se contradicen entre ellas.")
    di("")
    di(f"  [para ver el dano] metiendo tambien a BOSS: T = {est_todas['T_sondas']:.3f}"
       f" ({est_todas['gl_sondas']} g.l.) -> {est_todas['sigmas_sondas']:.2f} sigma.")
    di("  Ese numero NO se publica: es lo que sale de promediar una medicion con")
    di("  un numero degenerado, y es justo lo que la regla del repo prohibe.")
    di("")
    di("ESTADISTICO 2 — el modo comun contra el clavo  [PRUEBA DEL MODELO]")
    di(f"  T_modelo = {est['T_modelo']:.3f} (1 g.l.)  ->  {est['sigmas_modelo']:.2f} sigma")
    di("  Va aparte y etiquetado: NO es la prueba que se pidio.")
    di("-" * 78)
    di("")

    # ── BONDAD DE AJUSTE en el clavo, sonda por sonda ───────────────────────
    clav = [
        chi2_en_el_clavo(os.path.join(_REPO, "results", "chains", "ssee_cmb.[0-9].txt"),
                         "CMB (plik_lite TTTEEE+lowl+lensing)"),
        chi2_en_el_clavo(f"{_CAD}/kids_legacy/sseefijo.[0-9].txt", "KiDS-Legacy xi_pm"),
        chi2_en_el_clavo(f"{_CAD}/boss/ssee.[0-9].txt", "BOSS DR12 P(k) LPT"),
        bao_en_el_clavo(),
    ]
    di("BONDAD DE AJUSTE con logA EN EL CLAVO, sonda por sonda")
    di(f"  {'sonda':38s} {'chi2':>10s}  procedencia")
    for c in clav:
        marca = "" if c["exacto"] else "  [cota superior]"
        di(f"  {c['sonda']:38s} {c['chi2']:10.3f}  {c['modo']}{marca}")
    # ── grados de libertad, que es lo que convierte un chi2 en un juicio ────
    # N y libres de cada sonda, de su propia corrida. Con el fondo clavado NO
    # hay libres cosmologicos en ninguna: solo nuisances propios.
    GL = {  # ORIGEN: la cabecera de corrida de cada sonda
        "CMB (plik_lite TTTEEE+lowl+lensing)":
            (2354, 24, "N: plik TTTEEE 2289 + lowT 28 + lowE 28 + lensing 9; "
                       "libres = tau + 23 nuisances Planck (logA CLAVADO)"),
        "KiDS-Legacy xi_pm":
            (357, 8, "N: 357 puntos xi_pm; libres = logT_AGN, A_scale, dz1..dz6"),
        "BOSS DR12 P(k) LPT":
            (222, 18, "N: 222 puntos P(k) k<=0.20; libres = 18 sesgos "
                      "(b1,b2,bs x 3z x 2 hemisferios); logA CLAVADO"),
        "BAO DESI DR2":
            (13, 0, "N: 13 puntos DESI DR2; CERO libres, el fondo va clavado"),
    }
    # LA REFERENCIA ES EL OTRO MODELO SOBRE EL MISMO DATO, no una distribucion
    # teorica (regla de Mike, feedback_chi2_is_the_reference). Para plik en
    # particular el PTE de una chi2 estandar no significa nada: sus bandpowers
    # estan correlacionados y el propio mejor ajuste LCDM de Planck da ~1.19 de
    # chi2 reducido. Compararlo contra 1.0 marcaria «mal ajuste» a un ajuste que
    # es el estado del arte. Asi que la columna que manda es Delta vs LCDM.
    REF, REF_MODO = {}, {}
    try:
        for _et, _pat in (
                ("CMB (plik_lite TTTEEE+lowl+lensing)",
                 os.path.join(_REPO, "results", "chains", "lcdm_cmb.[0-9].txt")),
                ("KiDS-Legacy xi_pm", f"{_CAD}/kids_legacy/lcdmfijo.[0-9].txt"),
                ("BOSS DR12 P(k) LPT", f"{_CAD}/boss/lcdm.[0-9].txt")):
            _c, _a, _ = lee(_pat)
            # MISMA REGLA EN LOS DOS LADOS. Si el chi2 de SSEE se lee CON logA
            # clavado, el de LCDM tambien tiene que leerse clavado. Comparar
            # «SSEE clavado» contra «LCDM en su minimo libre» regala al segundo
            # toda la libertad de la amplitud: eso fabricaba un Delta=+14.0 en
            # BOSS donde con la misma regla hay +3.4.
            if "logA" in _c:
                _x = _a[:, _c.index("logA")]
                _sel = np.abs(_x - LOGA_CLAVADO) < 0.015
                REF[_et] = float(_a[_sel, _c.index("chi2")].min())
                REF_MODO[_et] = f"clavado, {_sel.sum()} muestras en banda"
            else:
                REF[_et] = float(_a[:, _c.index("chi2")].min())
                REF_MODO[_et] = "logA fijo en la corrida"
    except Exception as _e:                                   # noqa: BLE001
        di(f"  (referencia LCDM no disponible: {_e})")
    di(f"  {'sonda':38s} {'chi2':>9s} {'N':>5s} {'libres':>7s} {'g.l.':>5s}"
       f" {'chi2/gl':>8s} {'LCDM':>9s} {'Delta':>8s}")
    filas, tot, gtot = [], 0.0, 0
    for c in clav:
        n, k, proc = GL[c["sonda"]]
        gl = n - k
        pte = float(_chi2dist.sf(c["chi2"], gl))
        filas.append(dict(sonda=c["sonda"], chi2=c["chi2"], N=n, libres=k,
                          gl=gl, chi2_red=c["chi2"] / gl, PTE=pte,
                          procedencia=proc))
        tot += c["chi2"]
        gtot += gl
        _r = REF.get(c["sonda"])
        filas[-1]["chi2_lcdm"] = _r
        filas[-1]["delta_vs_lcdm"] = (c["chi2"] - _r) if _r is not None else None
        _rs = f"{_r:9.3f}" if _r is not None else f"{'—':>9s}"
        _ds = f"{c['chi2'] - _r:+8.3f}" if _r is not None else f"{'—':>8s}"
        di(f"  {c['sonda']:38s} {c['chi2']:9.3f} {n:5d} {k:7d} {gl:5d}"
           f" {c['chi2'] / gl:8.4f} {_rs} {_ds}")
    pte_tot = float(_chi2dist.sf(tot, gtot))
    di(f"  {'TOTAL (4 sondas)':38s} {tot:9.3f} "
       f"{sum(f['N'] for f in filas):5d} {sum(f['libres'] for f in filas):7d}"
       f" {gtot:5d} {tot / gtot:8.4f} {'—':>9s} {'—':>8s}")
    # El total de Delta se da SOLO sobre las tres que tienen referencia con la
    # MISMA rigidez. No se le suma BAO poniendo su propio chi2 como si fuera el
    # de LCDM: eso seria fabricar un Delta=0 gratis para esa fila.
    _con_ref = [f for f in filas if f.get("chi2_lcdm") is not None]
    _dtot = sum(f["delta_vs_lcdm"] for f in _con_ref)
    di(f"  {'Delta total (solo las 3 con referencia)':38s} {'':9s} {'':5s} {'':7s}"
       f" {'':5s} {'':8s} {'':9s} {_dtot:+8.3f}")
    di("")
    di("")
    di("  LO QUE BOSS SI PUEDE DECIR, ya que no vota en amplitud: cuanto le")
    di("  CUESTA que la amplitud vaya clavada, y si ese coste depende del fondo.")
    try:
        _cs, _as_, _ = lee(f"{_CAD}/boss/ssee.[0-9].txt")
        _cl, _al, _ = lee(f"{_CAD}/boss/lcdm.[0-9].txt")
        _costes = {}
        for _et, _c, _a in (("SSEE", _cs, _as_), ("LCDM", _cl, _al)):
            _x = _a[:, _c.index("logA")]
            _y = _a[:, _c.index("chi2")]
            _sel = np.abs(_x - LOGA_CLAVADO) < 0.015
            _costes[_et] = (float(_y.min()), float(_y[_sel].min()))
            di(f"    BOSS con fondo {_et:5s}: min libre {_y.min():8.3f}"
               f"   con logA clavado {_y[_sel].min():8.3f}"
               f"   coste {_y[_sel].min() - _y.min():+7.3f}")
        di(f"    El coste es parecido con los dos fondos "
           f"({_costes['SSEE'][1] - _costes['SSEE'][0]:+.2f} contra "
           f"{_costes['LCDM'][1] - _costes['LCDM'][0]:+.2f}): BOSS quiere menos")
        di("    amplitud de la que el CMB fija, y la quiere igual en los dos. Eso")
        di("    NO es un problema del fondo unificado, y tampoco es una medida de")
        di("    A_s: es el sintoma conocido de su degeneracion con el sesgo.")
    except Exception as _e:                                  # noqa: BLE001
        di(f"    (no disponible: {_e})")
    di("")
    di("  COMO SE LEE, que es la pregunta literal de Mike:")
    di("  Con el fondo clavado NO hay libres cosmologicos en ninguna sonda: estos")
    di("  chi2 son bondad de ajuste PURA, sin ajustar nada del modelo. La columna")
    di("  que manda es Delta = chi2(SSEE) - chi2(LCDM) SOBRE EL MISMO DATO. El")
    di("  chi2 reducido contra 1.0 NO sirve de juez aqui: el propio mejor ajuste")
    di("  de Planck da ~1.19 en plik, asi que 1.0 marcaria como malo al estado")
    di("  del arte. Y el chi2 conjunto es la SUMA de los individuales por")
    di("  construccion —cada sonda tiene sus nuisances y el fondo no se mueve—,")
    di("  asi que la suma no es un dato nuevo. El reparto si: CMB y KiDS-Legacy")
    di("  prefieren el fondo de SSEE (Delta negativo) y BOSS el de LCDM por +3.4,")
    di("  con los mismos libres y LA MISMA REGLA en los dos lados (los dos chi2")
    di("  leidos con logA clavado). Nada de eso es grande.")
    di("")
    di("  CORRECCION DE ESTA MISMA CORRIDA. La primera version dio +14.0 para")
    di("  BOSS. Era una mezcla de reglas: comparaba el chi2 de SSEE CON logA")
    di("  clavado contra el de LCDM en su minimo LIBRE, regalandole al segundo")
    di("  toda la libertad de la amplitud. Con la misma regla en los dos lados el")
    di("  numero es +3.414 clavado, o +1.550 si se dejan libres los dos.")
    di("")

    # ── CONTROL DEL OTRO LADO (R53) ─────────────────────────────────────────
    di("=" * 78)
    di("CONTROLES R53 — dos, porque hacen falta dos cosas distintas")
    di("=" * 78)
    di("")
    di("CONTROL A — POSITIVO: ¿sabe el estadistico VER una discordia?")
    di("  Se le inyecta a KiDS-Legacy un desplazamiento CONOCIDO en logA y se")
    di("  comprueba que T_sondas sube como debe. Si no subiera, un T pequeno no")
    di("  significaria «concuerdan», significaria «el estadistico esta ciego».")
    di(f"  {'inyectado en KiDS':>18s} {'T_sondas':>9s} {'sigma':>7s}")
    ctrlA = []
    for _iny in (0.0, 0.05, 0.10, 0.20):
        _m2 = [dict(x) for x in med]
        _m2[1]["logA"] = med[1]["logA"] + _iny
        _e2 = estadisticos(_m2)
        ctrlA.append(dict(inyectado=_iny, T=_e2["T_sondas"], sigmas=_e2["sigmas_sondas"]))
        di(f"  {_iny:18.2f} {_e2['T_sondas']:9.3f} {_e2['sigmas_sondas']:7.2f}")
    _sube = all(ctrlA[i + 1]["T"] > ctrlA[i]["T"] for i in range(len(ctrlA) - 1))
    di(f"  -> monotono creciente: {'SI, el estadistico ve' if _sube else 'NO — CIEGO, no concluir nada'}")
    di("")
    di("CONTROL B — el MISMO estadistico con el fondo LCDM clavado")
    di("  Las mismas sondas, la misma rigidez, otro fondo. Si la discordia sale")
    di("  igual con los dos fondos, entonces NO la causa el fondo: es de las")
    di("  sondas. Que es exactamente lo que se venia a averiguar.")
    ctrl_ok, est_c = True, None
    try:
        med_c = [
            medida(os.path.join(_REPO, "results", "chains", "lcdm_cmb.[0-9].txt"),
                   "CMB (fondo LCDM)"),
            medida(f"{_CAD}/kids_legacy/lcdmfijo.[0-9].txt", "KiDS-Legacy (fondo LCDM)"),
            medida(f"{_CAD}/boss/lcdm.[0-9].txt", "BOSS (fondo LCDM)"),
        ]
        for m in med_c:
            di(f"  {m['sonda']:38s} {m['logA']:10.5f} {m['sigma']:8.5f}")
        est_c = estadisticos(med_c)
        di(f"  T_sondas(LCDM) = {est_c['T_sondas']:.3f} ({est_c['gl_sondas']} g.l.)"
           f"  p = {est_c['p_sondas']:.4f}  -> {est_c['sigmas_sondas']:.2f} sigma")
    except Exception as e:                                   # noqa: BLE001
        ctrl_ok = False
        di(f"  CONTROL NO DISPONIBLE: {e}")
        di("  SIN CONTROL EL RESULTADO NO SE PUEDE FIRMAR (R53).")
    di("")

    res = dict(clavo_logA=LOGA_CLAVADO, burn_in=_QUEMA,
               eje_amplitud=med, estadisticos=est,
               estadisticos_perfil=est_pf, perfil_sirve=bool(perfil_sirve), degeneracion=degs, perfiles=prof,
               tirones=tabla_tirones(med),
               bondad_en_el_clavo=clav, chi2_total=tot, gl_total=gtot,
               PTE_total=pte_tot, tabla_gl=filas,
               control_lcdm=est_c, control_disponible=ctrl_ok,
               control_positivo=ctrlA, control_positivo_ve=bool(_sube))
    os.makedirs(os.path.dirname(_LOG), exist_ok=True)
    with open(_LOG, "w") as f:
        json.dump(res, f, indent=2)
    di(f"Log -> {_LOG}")
    with open(_LOG.replace(".json", ".log"), "w") as f:
        f.write("\n".join(_lineas) + "\n")
    return res


if __name__ == "__main__":
    main()
