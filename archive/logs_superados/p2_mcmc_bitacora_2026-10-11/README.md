# Bitácora acumulada del MCMC de Paper 2 (2026-10-11) — archivada 2026-10-16

**Motivo: registro de corrida, no fuente.** `ssee_paper2_mcmc.py` ESCRIBE AÑADIENDO a
`results/logs/mcmc_professional.log`, así que ese archivo juntó las tres corridas del 11 de
octubre (2.11 h, 1.85 h y 1.90 h). Las dos primeras quedaron superadas el mismo día por el
commit a7fb5c9 (SSEE con los mismos datos que ΛCDM/CPL). La tercera es, byte a byte,
`results/logs/mcmc_paper2_3models_wmfix.log`, la transcripción que leen las etapas
`resumen_3modelos` y `ppc_cronometros` y que desde hoy es salida de la etapa
`mcmc_paper2_3models` (con acta). La cadena vigente es
`/mnt/datos/SSEE_data/mcmc/paper2_3models/mcmc_chains_professional.npz` (11-10 17:54).

**`mcmc_paper2_lcdm_baseline.log`** (llegó 2026-10-16): ΛCDM sola del 2026-09-29, «para ΔBIC vs SSEE-MIRA»,
con N distinto (16 contra 15) y ΔBIC sólo orientativo. La reemplaza la corrida de los tres modelos con
los MISMOS datos (`resumen_3modelos.json`).

**Archivos de esta carpeta** (lista exacta, la que comprueba R77):
- `mcmc_paper2_lcdm_baseline.log`
- `mcmc_professional.log`
