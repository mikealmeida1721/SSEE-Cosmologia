# «Punto de fuga» del CMB (2026-09-08 → 09-19) — archivado 2026-10-03

**Motivo: superado por física nueva.** La campaña preguntaba qué ingredientes del fondo
tendría que soltar el CMB para aceptar el A_s bajo que pedía KiDS-1000 (2.84 «tarde»
contra 3.04 del CMB): barrido de ingredientes, 15 combinaciones con sinergia (fuga2) y con
el A_s de una sola sonda (fuga3), y su control. Con KiDS-Legacy (2026-09-20) la cizalla
pide el MISMO A_s que el CMB (0.49σ): no hay tensión que localizar. Ningún paper, `\val`
ni log vigente lee estos archivos.

| archivo | qué era |
|---|---|
| `cmb_punto_de_fuga.json` | v1 (τ fijo), invalidada por la v2 |
| `cmb_punto_de_fuga2.json` + `punto_de_fuga2.py`, `fuga2_control.py` | v2 con τ libre; control al 100 % |
| `cmb_fuga2_combinaciones.json` + `fuga2_combinaciones.py` | 15 subconjuntos con A_s promedio |
| `cmb_fuga3_fondo.json`, `cmb_fuga3_kids.json` + `fuga3_por_As.py` | 15 subconjuntos con el A_s de UNA sonda; `fondo` es el control |
| `cmb_fuga3_kids_3sig_rehecho.json` + `fuga3_rehace_3sig.py` | columna 3σ rehecha (el simplex estaba roto) |
| `cmb_As_perfil.json`, `cmb_combinacion_s8.json`, `cmb_tau_flotado_lcdm.json` | piezas sueltas del 09-08; su script no está en `src/` (commit `01d4369`) |

`cmb_tau_flotado.json` NO se archiva: lo leen `cmb_eval.py`, `perfil_wc_cmb.py` y el guardián.
`cmb_ns_forzado.json` / `cmb_wb_forzado.json` tampoco: miden la pendiente de la identidad
ω_c = KAL₀·ω_b·n_s (OP-19) y siguen siendo útiles; su script falta y queda por re-escribir.
