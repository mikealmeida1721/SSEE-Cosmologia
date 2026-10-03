#!/bin/bash
# R1/R2 (preliminar) — barrido en k_max con la maquinaria Kaiser VALIDADA
# (Fase 0, 16/16 verde: results/logs/growth_2026-07/VERIFICACION_BOSS.md).
#
# Por que un barrido y no un solo k_max: Kaiser es teoria lineal y su sesgo
# crece con k. Si el resultado (Delta chi2 entre modelos, y el logA preferido)
# se mueve con k_max, el numero depende del corte y NO es publicable. Si es
# plano, el corte no manda. Eso es lo que este barrido mide.
#
# PENDIENTE declarado: la corrida DEFINITIVA usa LPT (velocileptors) hasta
# k_max=0.20. Ver src/p06_growth/boss_lpt_R1R2.py y el bloqueo documentado ahi.
set -u
cd /home/mike/Proyectos/SSEE
LOG=results/logs/growth_2026-07
for K in 0.06 0.08 0.10 0.12; do
  echo "############ k_max = $K ############"
  .venv/bin/python -u src/p06_growth/boss_control.py "$K" 2>&1
  .venv/bin/python -u src/p06_growth/boss_fit.py "$K" 2>&1
done
echo "BARRIDO TERMINADO"
