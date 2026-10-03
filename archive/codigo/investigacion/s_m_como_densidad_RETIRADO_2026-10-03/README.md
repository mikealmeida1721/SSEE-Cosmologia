# s_m como densidad — RETIRADO 2026-10-03

`s_m = 1 + w₀ = 0.160` es un número de la **ecuación de estado**, no una
densidad (retirado como densidad el 2026-07-30; la partícula que salía de restarlo,
el 2026-08-01). Lo que hay aquí ponía ese número —o un múltiplo suyo— en una
ranura de densidad:

| archivo | qué hacía |
|---|---|
| `config_class/ssee_v36.ini` | Ω_cdm desde MIRA × 0.160 = 0.3199 (factor materia, retirado 2026-06-18) |
| `config_class/ssee_v36_IS.ini` | Ω_cdm = 0.160 − Ω_b («un solo sector» con s_m como materia) |
| `config_class/ssee_v36_nomira.ini` | el «test crítico sin MIRA» de mayo: 0.160 como Ω_m |
| `config_class/ssee_v36_twosector.ini` | 0.160 como CDM activa + la partícula de 36.95 eV |
| `run_p3_reframe.py` | Fase B vieja (A_s y τ clavados, N=613 → ΔBIC −24.02), con un «control» en (π/φ)·0.160. Superada por −26.03 (`results/logs/cmb_dbic_mnu_propia.json`). Su log está en `archive/logs_superados/p3_cmb_reframe_omega_m.log` |
| `ssee_paperB_DW.py` | mecanismo de producción de la φ-DM retirada; tecleaba 0.160 como Ω_m,dyn |

**Por qué no basta con anotarlo.** Un caso con s_m en la ranura de densidad no es una
versión del modelo: es el error de categoría. Mientras vivía en `src/` como
«contraejemplo», tres documentos (PRD, Sealed, Unified) lo usaban como prueba de
que «la densidad completa es físicamente necesaria», es decir, demostraban que
falla una densidad que el modelo nunca propone.

Con este retiro salen también el caso «naive» de `ssee_paper3_cmb.py` y de
`class_picos.py` y su «factor de degradación».
