# Configuraciones de CLASS — versionadas aquí a propósito

**Abierto el 2026-09-08, y la razón es un fallo real, no orden por gusto.**

`class_ssee/` es un fork de CLASS, y trae **el `.gitignore` de CLASS**, que
ignora `*.ini` y `output/` porque para el proyecto original son artefactos de
corrida. La consecuencia para nosotros: **ninguna configuración de CLASS que
haya usado este proyecto estaba en el repositorio.** Ni una. Vivían sólo en el
disco de Mike.

Así se descubrió: el `σ₈ = 0.8335` que publican cinco documentos salía de
`class_ssee/output/can_cold__pk.dat`, un fichero sin `.ini`, fuera del control
de versiones, del mismo minuto que la corrida de dos sectores con la partícula
retirada. Al re-correrlo con el fondo canónico y sus neutrinos masivos salió
**0.8268**, un 2.3% más bajo, y esta vez con un control que pasa.

## La regla

**Toda configuración de CLASS que produzca un número citable vive aquí**, y se
corre desde aquí:

```bash
cd class_ssee && OMP_NUM_THREADS=1 ./class ../config/class/<nombre>.ini
```

Una copia en `class_ssee/` es de trabajo y se puede perder. La de aquí es la
que manda.

## Qué hay

| archivo | qué es |
|---|---|
| `techo_ssee_canonico.ini` | techo σ₈ con A_s clavado a Planck, fondo canónico **con** Σm_ν=0.06849 eV |
| `techo_lcdm_referencia.ini` | su control: línea base de Planck 2018, criterio σ₈=0.8111±0.006 escrito antes de correr |
| `ssee_v36_canonical.ini` | fondo canónico SSEE (rescatado; **sin neutrinos masivos** — revisar antes de citar nada suyo) |
| ~~`ssee_v36.ini`, `ssee_v36_IS.ini`, `ssee_v36_nomira.ini`, `ssee_v36_twosector.ini`~~ | **archivados 2026-10-03** en `archive/codigo/investigacion/s_m_como_densidad_RETIRADO_2026-10-03/config_class/`: ponían s_m = 1+w₀ = 0.160 (o MIRA × 0.160) en la ranura de densidad |
| `lcdm_planck2018_ref.ini` | referencia ΛCDM vieja; pide `output = tCl,pCl,lCl`, o sea **no genera espectro de materia**: el fichero que llevaba ese nombre vino de otra corrida sin identificar |

## Lo que queda por revisar

Los rescatados de `ssee_v36*` **no llevan neutrinos masivos**. Cualquier número
que salga de ellos y se cite en un documento hereda el mismo sesgo del 2.3% que
se acaba de encontrar en el techo. No están auditados uno por uno.
