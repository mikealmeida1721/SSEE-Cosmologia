"""¿KiDS y BOSS MIDEN A_s, o solo ven un producto donde A_s va escondido?

LA PREGUNTA (M. Almeida, 2026-09-08). A_s es primordial: no cambia con la
epoca. El fondo cosmico lo mide directamente en la altura de los picos. Si eso
es asi, ¿por que BOSS y KiDS ven MENOS amplitud en su propia epoca? Hay dos
respuestas posibles y hay que separarlas antes de seguir:

  (a) el crecimiento tardio es realmente menor -> es fisica, hay algo que
      contar;
  (b) ninguna de las dos sondas puede separar A_s de su acompañante, asi que
      su A_s «baja» no porque el dato lo pida sino porque el ajuste se desliza
      por una direccion que el dato no distingue. Como dice Mike: «baja no
      porque realmente baje, sino porque no puede verlo».

COMO SE DISTINGUE, y es una medida, no una opinion. Para cada parametro se
comparan dos anchuras sacadas de la MISMA cadena:

  · marginal   = sqrt(C_ii)              lo que la sonda sabe de logA sin
                                          ayuda de nadie
  · condicional= 1/sqrt((C^-1)_ii)       lo que sabria si TODO lo demas
                                          estuviera clavado

Su cociente es el factor de degeneracion:
      D = marginal / condicional
D ~ 1  -> el parametro esta medido POR SI MISMO.
D >> 1 -> casi toda su anchura viene de no poder separarlo de otros: lo que la
          sonda mide es una COMBINACION, y el valor central de logA depende de
          por donde se haya deslizado.

Ademas se reporta con QUIEN esta enredado (la correlacion mas fuerte) y cual es
la combinacion que si esta medida (el eigenvector de menor varianza).

CONTROL (R53, y va PRIMERO por R24). Se fabrica una gaussiana de covarianza
CONOCIDA con una degeneracion puesta a mano (correlacion 0.99 entre dos
parametros y un tercero independiente). El metodo tiene que devolver D ~ 7.1
para los dos enredados y D ~ 1.0 para el libre. Si no los devuelve, no mide
degeneracion y se aborta.

NO TOCA NINGUN PAPER. Es diagnostico sobre cadenas ya corridas.

FUENTE: results/logs/growth_2026-07/As_medido_o_producto.json
"""
import glob
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from procedencia import cabecera, con_acta  # noqa: E402
SALIDA = REPO / "results" / "logs" / "growth_2026-07" / "As_medido_o_producto.json"

IGNORA = ("weight", "minuslogpost", "minuslogprior", "chi2")


def carga(patron):
    fs = sorted(glob.glob(patron))
    if not fs:
        return None, None, None
    hdr = open(fs[0]).readline().lstrip("#").split()
    X, W = [], []
    for f in fs:
        a = np.loadtxt(f)
        a = a[len(a) // 2:]                      # quema la primera mitad
        X.append(a)
        W.append(a[:, 0])
    X = np.concatenate(X)
    W = np.concatenate(W)
    keep = [i for i, n in enumerate(hdr)
            if not any(n.startswith(p) for p in IGNORA)]
    return X[:, keep], W, [hdr[i] for i in keep]


def degeneracion(X, W, nombres):
    C = np.cov(X.T, aweights=W)
    Ci = np.linalg.inv(C)
    marg = np.sqrt(np.diag(C))
    cond = 1.0 / np.sqrt(np.diag(Ci))
    D = marg / cond
    sd = np.outer(marg, marg)
    R = C / sd
    return C, R, marg, cond, D


def socio(R, nombres, j):
    r = R[j].copy()
    r[j] = 0.0
    k = int(np.argmax(np.abs(r)))
    return nombres[k], float(r[k])


def main():
    print(cabecera(__file__), flush=True)
    # ── CONTROL PRIMERO (R24) ───────────────────────────────────────────
    rng = np.random.default_rng(7)
    s = np.array([1.0, 1.0, 1.0])
    Rv = np.array([[1.0, 0.99, 0.0], [0.99, 1.0, 0.0], [0.0, 0.0, 1.0]])
    Cv = Rv * np.outer(s, s)
    Y = rng.multivariate_normal(np.zeros(3), Cv, size=400000)
    _, _, _, _, Dc = degeneracion(Y, np.ones(len(Y)), ["a", "b", "libre"])
    esperado = 1.0 / np.sqrt(1.0 - 0.99 ** 2)
    ok = (abs(Dc[0] - esperado) < 0.3 and abs(Dc[1] - esperado) < 0.3
          and abs(Dc[2] - 1.0) < 0.05)
    print("=== CONTROL (va primero): gaussiana con degeneracion puesta a mano")
    print("    D enredados = %.2f y %.2f   (debe ser %.2f)" % (Dc[0], Dc[1], esperado))
    print("    D libre     = %.2f          (debe ser 1.00)" % Dc[2])
    print("    -> %s\n" % ("PASA" if ok else "FALLA"), flush=True)
    if not ok:
        SALIDA.write_text(json.dumps(dict(
            control=dict(pasa=False, D=list(map(float, Dc))),
            veredicto="el metodo no detecta una degeneracion conocida"), indent=1))
        return

    FUENTES = {
        "KiDS (SSEE)": "/mnt/datos/SSEE_data/chains_p6/kids/ssee.[1-4].txt",
        "BOSS (SSEE)": "/mnt/datos/SSEE_data/chains_p6/boss/ssee.[1-4].txt",
        "KiDS (LCDM, fondo libre)":
            "/mnt/datos/SSEE_data/chains_p6/kids/lcdm.[1-4].txt",
        "BOSS (LCDM, fondo libre)":
            "/mnt/datos/SSEE_data/chains_p6/boss/lcdm.[1-4].txt",
    }

    out, usadas = {}, []
    for nombre, patron in FUENTES.items():
        X, W, nom = carga(patron)
        usadas += sorted(glob.glob(patron))
        if X is None:
            print("== %s: sin cadenas, saltada" % nombre, flush=True)
            continue
        C, R, marg, cond, D = degeneracion(X, W, nom)
        j = nom.index("logA") if "logA" in nom else None
        print("== %s   (%d muestras, %d parametros)" % (nombre, len(X), len(nom)))
        print("   %-12s %10s %11s %7s  %s"
              % ("param", "marginal", "condicional", "D", "mas enredado con"))
        filas = {}
        for i, n in enumerate(nom):
            sn, rn = socio(R, nom, i)
            filas[n] = dict(marginal=float(marg[i]), condicional=float(cond[i]),
                            D=float(D[i]), socio=sn, correlacion=rn)
            if n == "logA" or D[i] > 2.0:
                print("   %-12s %10.4f %11.4f %7.2f  %s (r=%+.2f)"
                      % (n, marg[i], cond[i], D[i], sn, rn), flush=True)
        # la combinacion que SI esta medida: eigenvector de menor varianza
        w, V = np.linalg.eigh(C)
        v = V[:, 0]
        orden = np.argsort(-np.abs(v))[:3]
        comb = " ".join("%+.2f·%s" % (v[k], nom[k]) for k in orden)
        print("   combinacion mejor medida: %s   (sigma %.4f)"
              % (comb, np.sqrt(w[0])), flush=True)
        if j is not None:
            print("   >>> logA: D = %.2f  -> %s\n"
                  % (D[j], "MEDIDO por si mismo" if D[j] < 1.5
                     else "NO lo mide solo: ve una COMBINACION"), flush=True)
        out[nombre] = dict(
            n_muestras=int(len(X)), parametros=filas,
            combinacion_mejor_medida=comb,
            sigma_de_esa_combinacion=float(np.sqrt(w[0])),
            logA_D=float(D[j]) if j is not None else None)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(con_acta(dict(
        corrida="¿KiDS y BOSS miden A_s o ven un producto?",
        pregunta="M. Almeida — si A_s es primordial y el CMB lo mide bien, "
                 "¿por que las sondas tardias ven menos en su misma epoca? "
                 "¿es fisica, o es que no pueden separarlo de su acompañante?",
        metodo="D = sigma_marginal / sigma_condicional sobre las cadenas ya "
               "corridas. D~1 medido por si mismo; D>>1 lo que se mide es una "
               "combinacion",
        control=dict(criterio="recuperar D=7.09 en una degeneracion r=0.99 "
                              "puesta a mano, y D=1 en el parametro libre",
                     D=list(map(float, Dc)), pasa=True),
        fuentes=out,
        alcance="diagnostico sobre cadenas existentes; lo cita Paper 6 por \\val (2026-10-01)"),
        __file__, entradas=usadas), indent=1))
    print("escrito -> %s" % SALIDA.relative_to(REPO), flush=True)


if __name__ == "__main__":
    main()
