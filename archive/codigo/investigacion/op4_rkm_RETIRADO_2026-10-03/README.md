# OP-4 — radio k-mouflage de Paper 8, RETIRADO 2026-10-03

`ssee_paper8_figures.py` dibujaba `fig_paper8_vainshtein` con
`r_km³ = M_obj/(4π·M_pl·M²)`. Esa fórmula no cierra dimensiones: el lado
derecho es longitud², no longitud³, y por eso daba valores distintos (un factor
10³) según se evaluara en GeV o en eV. Ver OPEN_PROBLEMS, OP-4.

**Decisión de Mike (opción 2):** Paper 8 ya no cita ningún radio. Sin el acople
β_c en la acción de Paper 7 (retirado 2026-09-07) no hay quinta fuerza que
apantallar, y el Sistema Solar y la lente canónica descansan en el acople
selectivo y en α_B=α_M=α_T=0, que valen para cualquier M.

Los radios con la forma que sí cierra (r²: Sol 823 AU, Vía Láctea 4.0 kpc,
cúmulo 126 kpc) quedan en `results/logs/cajones_algebra.json` como registro.
El script y la figura se conservan aquí tal cual; no los usa ningún documento.
