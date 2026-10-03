# Regeneración de logs contaminados (Σm_ν rancio)

**Abierto 2026-07-26.** R33 detectó 8 logs **activos** generados con
`Σm_ν = 0.06902` (retirado; vigente **0.06849**). Un `.log` es un artefacto
congelado: guarda las constantes del día en que se corrió y no se entera de los
cambios posteriores. Ver la memoria `project_propagation_order`, nivel 8.

**Regla de esta tanda:** ninguna corrida se lanza sin `preflight.py` en verde
delante, en la misma línea de comando. Tres MCMC salieron con la misma constante
muerta por lanzar primero y verificar después.

```bash
.venv/bin/python3 src/verificacion/preflight.py && <script>
```

## Estado

| # | Log | Script | Alimenta | Estado |
|---|---|---|---|---|
| 1 | `p6_class_reframe_omega_m.log` | `archive/codigo/p06_phiDM_RETIRADO_2026-08-01/ssee_paper6_canonical_particle.py` | ~~m_φ, k_fs, σ₈, S₈~~ | 🔴 **RETIRADO 2026-08-01** — alimentaba la partícula. «Reproduce lo publicado» dejó de ser cierto al reescribirse Paper 6: `m_φ` y `k_fs` ya no se publican. Canónico: `R3_ssee_kids_S8.json` (S₈=0.7555±0.0192) |
| 2 | `p3_rd_reframe_omega_m.log` | `src/p03_cmb/run_p3_rd_reframe.py` | r_d, θ* (Paper 3) | ✅ **HECHO** — Registro actualizado (θ*) |
| 3 | `p3_cmb_reframe_omega_m.log` | `run_p3_reframe.py` | χ², ΔBIC (Paper 3) | 🗄️ **ARCHIVADO 2026-10-03** (`archive/logs_superados/`): A_s y τ clavados, N=613, y un control con (π/φ)·s_m. Superado por `cmb_dbic_mnu_propia.json` (ΔBIC −26.03) |
| 4 | `p3_h0anchor_reframe.log` | `src/p03_cmb/scan_omega_m.py` | ancla H₀ (Paper 3) | ✅ **HECHO** — el SCRIPT estaba rancio |
| 5 | `paper3_cmb_reframe.log` | `src/p03_cmb/ssee_paper3_cmb.py` | CMB (Paper 3) | ✅ **HECHO** — ΔBIC=−35.0 + 5 figuras |
| 6 | `b1_full_run.log` | `src/p03_cmb/ssee_paper3_b1_mcmc.py` | CMB Fase B | ⬜ pendiente |
| 7 | `b1_lcdm_run.log` | `src/p03_cmb/ssee_paper3_b1_mcmc.py` | CMB Fase B (ΛCDM) | ⬜ pendiente |
| 8 | `b1_mcmc_reframe.log` | `src/p03_cmb/ssee_paper3_b1_mcmc.py` | CMB Fase B (MCMC) | ⬜ pendiente |

Históricos ya declarados en `_LOGS_HISTORICOS` (no se re-corren, quedan como
registro): `mcmc_paper2_3models_om308`, `mcmc_paper2_reframe_om308`,
`mcmc_professional`, `mcmc_paper2_reframe_dr2`.

## Contraste esperado (lo que hay que confirmar, no suponer)

Para el #1 ya sabemos que el log contradice al paper — el **paper** tiene el
valor bueno:

| Cantidad | Paper publica | Log rancio dice |
|---|---|---|
| Σm_ν | 0.06849 | 0.06902 |
> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
| ~~m_φ~~ (**RETIRADO 2026-08-01**) | ~~40.70 eV~~ | ~~41.0187 eV~~ |
| k_fs | 0.754 h/Mpc | 0.7620 |
| σ₈ | 0.747 | 0.7483 |

Para los demás **no se supone nada**: se corre y se compara. Si un número
publicado se mueve, se corrige el paper.

## Bitácora

> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7555±0.0192` (0.11σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.05σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
- **#1 `p6_class` — CERRADO 2026-07-26.** La corrida limpia reproducía lo entonces
  publicado: Σm_ν 0.06849, y los hoy retirados m_φ 40.7024, k_fs 0.7542, σ₈ 0.7470. El paper tenía
  razón; la prueba archivada era la vieja. Ningún número del paper se movió.
- **#2 `p3_rd` — CERRADO 2026-07-26.** r_d = 147.174 (0.32σ) sin cambio. θ* SÍ
  se movió y el Registro se actualizó: anchor 0.59668/1.05σ → **0.59667/1.00σ**;
  posterior (ahora 67.7869, antes 67.9475) 0.59666/0.91σ → **0.59638/0.68σ**.
  Las filas del Registro decían literalmente «mnu=0.069»: la contaminación
  estaba documentada a la vista y nadie la leyó.
- **#3 `p3_cmb` — CERRADO.** χ² = 1005.409, ΔBIC = −24.024. Reproduce lo
  documentado (1005.41 / −24.02). Nada se movió.
- **#5 `paper3_cmb` — CERRADO.** ΔBIC = −35.0, picos ℓ=220/536/813. Regeneró
  además 5 figuras del nivel 9, que también estaban rancias.
- **#4 `p3_h0anchor` — CERRADO, y fue el peor.** No era el log: era el FUENTE.
  `scan_omega_m.py:8` tenía `mnu=0.069` hardcodeado —el residuo de C_ν=94.07—
  mientras el resto de la suite ya usaba 0.06849. Re-correr el log no habría
  servido de nada: habría vuelto a salir rancio. Ahora lee Σm_ν del núcleo.
  → De aquí sale **R34**: ningún .py activo puede re-teclear una constante
  retirada; se lee del núcleo. R33 caza el síntoma, R34 la causa.
  ⚠ ANOTADO (no perseguido): el script hoy barre **Ω_m**, pero el log viejo
  barría **H₀**, y `ssee_paper2_mcmc_reframe.py:11,94` lo cita como «scan …
  χ²=1005.41 mín». La referencia apunta a un log que ahora contiene otra cosa.

## Pendiente de decisión

Los tres `b1_*` los produce `ssee_paper3_b1_mcmc.py`, un MCMC Cobaya completo
(`--mode both`, `--mode lcdm`, `--mode both --fast`). El script YA usa 0.06849
(línea 94): sólo los logs están viejos. Es cómputo de **horas**, posiblemente
de más de un día para el full. Decidir si se lanza ahora o se declara histórico.
