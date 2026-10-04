# Logs sin script, reemplazados por una etapa sellada — archivados 2026-10-04

**Motivo (a): el número sigue vigente, pero ahora sale de una etapa con acta.**

| archivo | qué tenía | de dónde sale ahora |
|---|---|---|
| `bao_lcdm_planck.json` | χ² BAO DESI DR2 de ΛCDM con sus parámetros de Planck 2018, por CAMB: 31.981952 (2026-09-27). Su script no se conservó («lcdm_planck.py + CAMB»). | `results/logs/lcdm_conjunta_control.json` → `bao_lcdm_planck.chi2` = 31.981898, la misma cuenta por CAMB, sellada (etapa `lcdm_conjunta_control`). Diferencia 5.5e-5: precisión de CAMB. Su único lector, `lya_auditoria.py`, lee ya de ahí; control de la etapa PASA (tolerancia 1e-3). |

**Archivos de esta carpeta** (lista exacta, la que comprueba R77):
- `bao_lcdm_planck.json`
