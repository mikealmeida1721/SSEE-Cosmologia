# Primera exploración de Paper 6 sobre KiDS crudo (2026-07-30) — archivada 2026-10-03

**Motivo: corrida reemplazada por otra que ya está en el modelo y cumple.** Ajustes por
minimización (no MCMC) del 2026-07-30 contra los ξ± de KiDS-1000, con A_s clavado al CMB:
`ssee_kids_results.json`, `lcdm_kids_results.json`, `ssee_om_libre.json` (+ su script, Ω_m
libre) y `test_hueco.json` (huecos en H(z) a bajo z). Los reemplazan el MCMC R3 (SSEE) y R4
(ΛCDM) sobre KiDS-1000 y, como titular, KiDS-Legacy con A_s clavado (S₈ 0.8273 vs 0.8265).
Ningún paper ni `\val` los lee. También `s8_barra_kids.json` (barrido de logA contra KiDS-1000
con A_s del CMB) y `no_circular.py`, la prueba de que el despeje σ₈ ← fσ₈ no es circular
(g(z) no depende de A_s): pertenecía al tratamiento Kaiser de fσ₈, que reemplazó el LPT de
BOSS (R1/R2); nadie lo importa (archivados 2026-10-03, segundo pase, al destaparlos R65).

**Archivos de esta carpeta** (lista exacta, la que comprueba R77):
- `lcdm_kids_results.json`
- `ssee_kids_results.json`
- `ssee_om_libre.json`
- `ssee_om_libre.py`
- `test_hueco.json`
- `no_circular.py`
- `s8_barra_kids.json`
