# Barrido Kaiser de BOSS en k_max (2026-08-08) — archivado 2026-10-03

`boss_control_kmax*.json`, `boss_fit_kmax*.json`, `barrido_kmax_20260808.log` y el
orquestador `barrido_kmax.sh` (corría `src/p06_growth/boss_control.py` y `boss_fit.py`
con k_max = 0.06, 0.08, 0.10, 0.12).

**Por qué se archiva.** Era un SONDEO con teoría lineal de Kaiser para ver si el resultado
dependía del corte en k. Lo superó la corrida LPT (velocileptors) R1/R2 hasta k_max = 0.20
(`results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json`, en la cadena). Ningún paper, `\val`
ni log vigente lo cita.

**Lo que mostró la re-ejecución (recorre_logs, 2026-10-03).** Re-corridos CON su k_max, no
reproducen: σ(fσ₈) se mueve 2–25 %, el χ² 1–2 unidades y el nuisance `sv` salta órdenes de
magnitud. El minimizador está mal condicionado en una dirección plana de `sv`, de modo que un
cambio mínimo de entrada (H0_GLOBAL en ssee_core, 2026-09-28) lo desplaza. Es otra razón para
no usarlo como resultado. Ver VERIFICATION_LEDGER.md §V-L5-RECORRE.

`boss_fit.py` y `boss_control.py` siguen en `src/`: la ventana de `boss_fit.py` es la que pasó
los 16 controles de Fase 0 y la que reutiliza `boss_lpt_R1R2.py`.

`erosita_cr.json` (en esta carpeta): segundo intento de eROSITA; el script vigente
escribe `results/logs/erosita_cr_v3.json`. La docstring de `erosita_cr.py` todavía dice
que «sigue en erosita_cr.json»; no se tocó para no invalidar el candado de su etapa.
