"""Lector de la Tabla 2 de Planck 2018 VI (arXiv:1807.06209) desde su extracto LITERAL.

data/raw/planck2018_VI/tabla2.tex es copia byte a byte de ms.tex (sha en data/raw/FUENTES.yaml,
R76 vigila que nadie lo edite). Aquí sólo se parte en celdas: ningún número se teclea.

    from planck2018_tabla2 import lee
    lee("r_drag")   -> (147.09, 0.26)      columna 5 = TT,TE,EE+lowE+lensing
"""
import pathlib
import re

TABLA = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw" / "planck2018_VI" / "tabla2.tex"
# nombre corto -> rótulo literal de la fila en la tabla
FILAS = {"omega_b": r"\Omega_{\mathrm{b}} h^2", "omega_c": r"\Omega_{\mathrm{c}} h^2",
         "H0": r"H_0\,[{\rm km}\,{\rm s}^{-1}\,{\rm Mpc}^{-1}]", "Omega_m": r"\Omega_{\mathrm{m}}",
         "sigma8": r"\sigma_8", "S8": r"S_8\equiv \sigma_8(\Omega_{\rm m}/0.3)^{0.5}",
         "r_drag": r"r_{\mathrm{drag}}\,[\mathrm{Mpc}]", "logA": r"\ln(10^{10} A_\mathrm{s})"}
COLUMNAS = ("TT+lowE", "TE+lowE", "EE+lowE", "TT,TE,EE+lowE", "TT,TE,EE+lowE+lensing", "+BAO")


def _filas():
    out = {}
    for ln in TABLA.read_text().splitlines():
        if ln.startswith("%") or "&" not in ln or "\\pm" not in ln:
            continue
        c = ln.rstrip().removesuffix("\\cr").split("&")
        out[c[0].strip()] = [x.strip() for x in c[1:]]
    return out


def lee(nombre, columna=5):
    """(valor, sigma) de la fila `nombre` en la columna 1..6. Sólo celdas simétricas «x\\pm s»."""
    celda = _filas()[FILAS[nombre]][columna - 1]
    m = re.fullmatch(r"([-+]?\d+\.?\d*)\\pm\s*(\d+\.?\d*)", celda)
    if not m:
        raise ValueError(f"{nombre}, columna {columna}: celda no simétrica «{celda}»")
    return float(m.group(1)), float(m.group(2))


if __name__ == "__main__":
    # CONTROL (R53): el extracto tiene que dar los valores que el resto del repositorio
    # ya cotejó (planck2018_prior.csv) y rechazar una celda asimétrica.
    assert lee("H0") == (67.36, 0.54) and lee("Omega_m") == (0.3153, 0.0073)
    try:
        lee("Omega_m", 3)
        raise SystemExit("no rechazó la celda asimétrica")
    except ValueError:
        pass
    for n in FILAS:
        print(n, lee(n))
