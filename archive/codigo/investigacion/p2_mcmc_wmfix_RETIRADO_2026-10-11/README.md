# ssee_paper2_mcmc_wmfix.py — archivado el 2026-10-11

**Qué era.** El MCMC del 2026-07-25 que corrigió la parametrización de SSEE: ω_m fijo
(algebraico) y Ω_m = ω_m/h² derivado en cada muestra, en vez de Ω_m congelado en 0.308881.

**Por qué se archiva.** Su corrección ya está en los dos scripts vigentes
(`src/p02_mcmc/ssee_paper2_mcmc.py`, 3 modelos; `src/p02_mcmc/ssee_paper2_mcmc_reframe.py`,
producción). Ninguna etapa DVC lo corre y ningún log vigente sale de él. Además seguía
sumando `LL_CLUSTERS`: los 4 cúmulos que no están en Zhang+2026 y la fórmula
M_ig·KAL0·(1+f_ν) del marco MOND, ambos retirados el 2026-10-01 (la prueba de cúmulos
vive en `src/p02_mcmc/cumulos_zhang2026.py`, simétrica y con los 46 sistemas reales).

**Hallado en.** La quinta lectura de P2 (`notes/lectura_quinta/P2.md`).

**Referencia que queda.** Un comentario de `ssee_paper2_mcmc_reframe.py` (L113) todavía lo
nombra en su ruta vieja; no se tocó para no cambiar el sha del script que selló la cadena
de producción (`mcmc_paper2_reframe.json`). Se corrige en la próxima re-corrida de esa cadena.
