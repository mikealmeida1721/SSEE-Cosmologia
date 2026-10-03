# Campaña «¿qué partícula pide KiDS?» — colas #24 a #29 (2026-09-09 → 09-19) — archivada 2026-10-03

**Motivo: superada por física nueva.** Estas corridas buscaban qué especie térmica masiva
(masa `m_x`, densidad `om_x`) pedía la cizalla de KiDS-1000 con el fondo de SSEE clavado,
y cuánto le costaba al CMB y a BOSS. El 2026-09-20, con KiDS-Legacy, el hueco que la
partícula iba a tapar midió 0.49σ y fijar A_s al del CMB no costó nada (ΔBIC +6.24 a favor
del modelo sin partícula): la partícula quedó **innecesaria** (ver banner de CLAUDE.md y
`OPEN_PROBLEMS.md`). Ningún paper, `\val` ni log vigente lee estos archivos.

| archivo | qué era |
|---|---|
| `precio_cmb_de_la_particula.json` + `precio_cmb_de_la_particula.py` | cola #25: χ² del CMB para cada partícula de la #24 |
| `boss_con_particula.py` | cola #27: BOSS con la partícula (la tercera sonda) |
| `vara_As_libre_perfil.json` + `.py`, `vara_lcdm_fondo_fijo.json` + `.py` | cola #27: las dos varas de control de KiDS (A_s libre; ΛCDM con fondo Planck) |
| `ruido_minimizador_kids.json` / `.log` + `.py` | cola #28, paso 0: ruido del minimizador de molestias de KiDS |
| `rejilla_extendida.json` / `.log` + `.py` | cola #28b: 8 casillas nuevas de (m_x, om_x) hasta el borde del modelo |
| `precio_cmb_rejilla_extendida.json` / `.log` | cola #29: ABORTADA (su control de la base no cerró; nada que leer) |
| `pinza_conjunta.py` | combinación KiDS+CMB de la #24 y la #25 |

**Lo que se queda en `src/`, a propósito:** `particula_que_prefiere_kids.py` (+ su json) lo
nombran los docstrings de `cmb_eval.py` y `kids_shear.py`, que son dependencias de muchas
etapas; editarlos invalidaría sus actas. `conjunta_tres_sondas.py` (+ json) es entrada de
`base_sin_particula.py`, cuya casilla `om_x = 0` (χ² BOSS 198.07) cita Paper 6.
`boss_lpt_R1R2.py` L92 aún nombra el control C0 de `boss_con_particula.py` en un comentario.
