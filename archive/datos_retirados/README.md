# Datos crudos retirados

## cluster_masses_2026-10-02.csv (retirado el 2026-10-02)

- **Qué era.** Las masas de 4 cúmulos (Coma, A2029, A478 y Bullet) que Paper 2 usaba en su χ² de cúmulos. El archivo citaba como fuente a Zhang+2026 (arXiv:2602.06082).
- **Por qué se retiró.** Al cotejarlo con la fuente (R76, 2026-10-01), Coma y Bullet no aparecen en Zhang+2026, y A2029 y A478 vienen allí con otros números. La fuente declarada contradice al archivo.
- **Qué lo reemplaza.** El análisis de cúmulos se rehízo con las 46 entradas reales de las Tablas II y III de Zhang+2026: `data/raw/zhang2026/tablas_II_III.tex`, leídas por `src/p02_mcmc/cumulos_zhang2026.py`.
- **Uso actual.** Ningún script ni documento lo usaba ya (comprobado con grep en `src/`, `manuscript/`, `submission_PRD/`, `dvc.yaml` y `PROPAGACION.yaml`).
