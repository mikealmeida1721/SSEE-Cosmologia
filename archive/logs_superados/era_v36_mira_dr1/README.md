# Logs de la era V3.6: MIRA, DESI DR1 mal etiquetado, Ω_m congelado (abril → julio 2026) — archivados 2026-10-03

**Motivo: superados por física nueva y corridas malas reemplazadas.** Salidas de los MCMC y
análisis de Paper 2/3 anteriores a los cambios que los dejaron sin validez: el prior MIRA
(retirado 2026-06-18, OP-8), los BAO DR1 etiquetados como DR2 (banner 2026-07-02), el sector
0.160 metido en la geometría y el Ω_m congelado en E(z) (banner 2026-07-09 y fix R25), y el
Σm_ν 0.0690 rancio (2026-07-25). Lo vigente está en la cadena: MCMC de P2 (etapa con acta,
H₀ 67.82±0.41), CMB de P3 (`paper3_cmb_chi2.json`, ΔBIC diagonal −35.03) y B1 (`b1_k2.json`).

| archivo | qué era |
|---|---|
| `mcmc_run.log`, `mcmc_run2.log`, `mcmc_run_20260420.txt` | MCMC P2 v2 de abril (w₀,wₐ fijos; prior Planck) |
| `mcmc_paper2_mira.log`, `mcmc_om320_run.log`, `mcmc_professional2.log` | prior MIRA / Ω_m 0.320 |
| `mcmc_paper2_3models_dr2.log`, `mcmc_paper2_reframe_dr2.log`, `mcmc_paper2_reframe_om308.log`, `lcdm_baseline_dr2.log`, `lcdm_baseline_om308.log` | 3 modelos y ΛCDM base con DR1 mal etiquetado o Ω_m congelado |
| `paper2_analysis_dr2real.log` | análisis plano w₀–wₐ de julio, antes del Σm_ν coherente |
| `paper3_cmb_canonical.log`, `p3_pr4_diag_nu_fix.log`, `p3_cmb_reframe_nu_fix.log`, `p3_rd_reframe_nu_fix.log` | P3 de julio («PR4», que era PR3; ΔBIC −24.02 con A_s/τ prestados; r_d por fórmula). Reemplazos: `paper3_cmb_chi2.json`, `cmb_dbic_tau_ajustado.json`, `rd_dual.json` |
| `b1_mcmc_reframe.log` | B1 «fast» del 2026-06-20, cortado a 150 358 pasos |

`mcmc_paper2_3models_om308.log` se queda en `results/logs/` porque lo nombra un comentario
de `CANONICAL_VALUES.yaml`; editarlo re-sella ~30 etapas. Se archiva con el próximo cambio
físico de ese archivo.
