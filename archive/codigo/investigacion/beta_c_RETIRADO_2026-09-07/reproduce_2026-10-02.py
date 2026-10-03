#!/usr/bin/env python3
"""reproduce_2026-10-02.py — reproduce los números RETIRADOS de β_c que citan los cajones.

POR QUE. OPEN_PROBLEMS, el Registro y CLAUDE.md citan β_c = −2.194210, w = −0.972562,
−0.922851, −0.691265, φ̇ = 0.540727, X = 0.146193… como historia de cómo se retiró β_c
(2026-09-05/07). Ninguno tenía log: R74 los marcaba sin procedencia. Son números
retirados, pero la historia tiene que poder comprobarse.

COMO. Extrae el árbol src/ del commit d849df0 (el que dejó ssee_eft_verification.py
con el M⁴ físico y la saturación ya corregida) con `git archive`, y corre ese script
con UNA línea cambiada, la de M⁴, en tres variantes:
  fisico      M⁴ = 5φ⁸ ρ_crit  (el valor de Paper 10; el script tal cual)
  convencion  M⁴ = ρ_crit = 1  (la convención retirada el 09-05: da el −2.194210)
  sin_X2      M⁴ → ∞           (el término X²/M⁴ apagado)
De cada salida lee w_φ(a=1), φ̇(a=1), β_c y α_pot, y calcula X = φ̇²/2, X/KAL₀ y X²/M⁴.

CONTROL (R53). La variante «fisico» es el script SIN tocar: su β_c tiene que ser el
−0.691265 que el propio d849df0 escribió en su comentario de la línea 84 y en
OPEN_PROBLEMS. Y el otro lado: las tres variantes tienen que dar β_c DISTINTOS
(si el parche de M⁴ no se aplicara, saldrían iguales).

    python3 archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduce_2026-10-02.py
"""
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import io

_R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(_R, "src"))
from procedencia import con_acta  # noqa: E402

COMMIT = "d849df0"   # ORIGEN-VALOR: d849df0 — commit del 2026-09-06 con la saturación corregida y M⁴ físico
SCRIPT = "src/p07_eft/ssee_eft_verification.py"
LINEA_M4 = re.compile(r"^M4 = 5\.0 \* phi\*\*8 \* rho_crit.*$", re.M)
VARIANTES = {"fisico": None, "convencion": "M4 = rho_crit", "sin_X2": "M4 = 1e300"}
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reproduccion_2026-10-02.json")
CAMPOS = {"w_phi": r"w_φ numérico\(a=1\)\s*=\s*(-?[0-9.]+)",
          "phidot": r"φ̇\(a=1\)\s*=\s*(-?[0-9.]+)",
          "beta_c": r"β_c requerido\s*=\s*(-?[0-9.]+)",
          "alfa_pot": r"α_pot\s*=\s*(-?[0-9.]+)",
          "M4": r"M⁴\s*=\s*([0-9.e+]+)\s*\(ρ_crit\)",
          "KAL0": r"KAL₀=([0-9.]+)"}

tar = subprocess.run(["git", "archive", COMMIT, "src"], cwd=_R, capture_output=True, check=True).stdout
res = {}
with tempfile.TemporaryDirectory() as tmp:
    tarfile.open(fileobj=io.BytesIO(tar)).extractall(tmp)
    original = open(os.path.join(tmp, SCRIPT)).read()
    assert len(LINEA_M4.findall(original)) == 1
    for nombre, linea in VARIANTES.items():
        codigo = original if linea is None else LINEA_M4.sub(linea, original)
        ruta = os.path.join(tmp, "src", "p07_eft", f"_rep_{nombre}.py")
        open(ruta, "w").write(codigo)
        env = dict(os.environ, PYTHONPATH=os.path.join(tmp, "src"), OMP_NUM_THREADS="1", MPLBACKEND="Agg")
        o = subprocess.run([sys.executable, ruta], cwd=tmp, env=env, capture_output=True, text=True, timeout=1800)
        if o.returncode != 0:
            sys.exit(f"{nombre}: el script falló\n{o.stderr[-2000:]}")
        v = {k: float(re.search(p, o.stdout).group(1)) for k, p in CAMPOS.items() if k not in ("M4", "KAL0")}
        X = v["phidot"] ** 2 / 2
        from ssee_core import KAL0  # el mismo KAL₀ (no cambió entre d849df0 y hoy)
        M4 = {"fisico": 5.0 * ((1 + 5 ** 0.5) / 2) ** 8, "convencion": 1.0, "sin_X2": float("inf")}[nombre]
        v.update(X=X, X_sobre_KAL=X / KAL0, X2_sobre_M4=X ** 2 / M4, linea_M4=linea or "(sin tocar)")
        res[nombre] = v

esperado = -0.691265   # ORIGEN-VALOR: -0.691265 — beta_c que d849df0 escribió en su propio comentario (ssee_eft_verification.py L93)
pasa = (abs(res["fisico"]["beta_c"] - esperado) < 5e-7
        and len({round(r["beta_c"], 6) for r in res.values()}) == 3)
out = dict(commit=COMMIT, script=SCRIPT, variantes=res,
           control=dict(fisico_reproduce=esperado, distintas=True, pasa=bool(pasa)))
json.dump(con_acta(out, __file__), open(SALIDA, "w"), indent=1, ensure_ascii=False)
for n, r in res.items():
    print(f"{n:11s} w={r['w_phi']:.6f} beta_c={r['beta_c']:.6f} phidot={r['phidot']:.6f} "
          f"X={r['X']:.6f} X/KAL={r['X_sobre_KAL']:.6f} X2/M4={r['X2_sobre_M4']:.6f}")
print("CONTROL:", "PASA" if pasa else "NO PASA")
sys.exit(0 if pasa else 1)
