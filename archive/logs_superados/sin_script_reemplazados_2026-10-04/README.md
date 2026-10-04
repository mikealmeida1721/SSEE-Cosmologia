# Logs sin script, reemplazados por una etapa sellada — archivados 2026-10-04

**Motivo (a): el número sigue vigente, pero ahora sale de una etapa con acta.**

| archivo | qué tenía | de dónde sale ahora |
|---|---|---|
| `p3_h0anchor_reframe.log` | Barrido de Ω_m del CMB con H fijo, incluidos los factores π/φ (retirados con OP-8, 2026-06-18). Se citaba como fuente de «el CMB se minimiza en H_glob», pero no barre H₀ (motivo **b**: superado). | El ancla de H₀ la mide `perfil_h0_ancla.py` → `results/logs/perfil_h0_ancla.json` (etapa sellada): 67.873 ± 0.098, control ΛCDM pasa. Los comentarios de `src/p02_mcmc/ssee_paper2_mcmc_reframe.py` (líneas 12 y 93) todavía lo nombran; se corrigen cuando ese script vuelva a cambiar, porque tocarlo invalida el acta de su MCMC. |
| `paper2_analysis_dr2official.log` | Salida de `ssee_paper2_analysis.py`: plano w₀–wₐ contra las 4 combinaciones oficiales de DESI DR2. Retirado de la cola el 2026-09-07 (PROPAGACION). | Los mismos números (1.68σ, 0.24σ, 1.76σ, 1.46σ y los de ΛCDM) salen de `results/logs/paper2_w0wa.json`, sellado; comparados uno a uno el 2026-10-04: idénticos. |
| `bao_lcdm_planck.json` | χ² BAO DESI DR2 de ΛCDM con sus parámetros de Planck 2018, por CAMB: 31.981952 (2026-09-27). Su script no se conservó («lcdm_planck.py + CAMB»). | `results/logs/lcdm_conjunta_control.json` → `bao_lcdm_planck.chi2` = 31.981898, la misma cuenta por CAMB, sellada (etapa `lcdm_conjunta_control`). Diferencia 5.5e-5: precisión de CAMB. Su único lector, `lya_auditoria.py`, lee ya de ahí; control de la etapa PASA (tolerancia 1e-3). |

**Archivos de esta carpeta** (lista exacta, la que comprueba R77):
- `bao_lcdm_planck.json`
- `p3_h0anchor_reframe.log`
- `paper2_analysis_dr2official.log`
