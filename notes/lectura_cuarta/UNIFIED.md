# Cuarta lectura — SSEE_Unified_Journal.tex

Inventario: 175 líneas num:valor (muchas repetidas; el documento condensa Papers 1-10).
Cobertura: ~70 entradas detalladas en `numeros` + un bloque de repeticiones exactas
agrupado (c_s²=0.021284 ×7, M=9.68 meV ×5, r=0.008131 ×4, residuo 4.2e-6 ×4,
cascada IR 68.13/0.17 ×5-6, trío Planck 2018 ×4-5 cada uno).

## Conteo por decisión (aprox., inventario + agrupados)
- VAL (macro ya existente, reusar): ~40
- LIT (literatura citada correctamente): ~30
- ALG (álgebra φ,π verificada): ~10
- HIS (retirado, narrado correctamente): ~8 (MIRA 0.3199, 0.31993, 0.32010, φ-DM×2, 67.037/71.87/1.12, 72.05/0.96)
- DERIVADO: ~12
- TRIVIAL: ~6
- FIX: **1**
- Afirmaciones registradas: 4 (1 FIX, 1 a verificar, 2 confirmaciones sin cambio)

## Los 3 hallazgos más graves

1. **FIX (L456):** `($-24.0$ for the plik_lite point estimate)` cita el ΔBIC
   **retirado** (results/logs/cmb_dbic_tau_ajustado.json#publicado_con_tau_prestado=-24.02,
   N=613, A_s/τ clavados en Planck). El vigente es **-26.03** (N=669, {A_s,τ}
   ajustados, cmb_dbic_mnu_propia.json#dBIC=-26.0327). El propio
   `SSEE_Endorser_Summary.tex` (L70) ya usa -26.03 para la misma comparación —
   este documento quedó atrás.

2. **A verificar (L476):** "within ≤1.25σ blind (mean 0.72σ)" — la media 0.72σ
   coincide con el banner de CLAUDE.md ("Fase 4 ciego 0.72σ/máx 1.23σ"), pero
   el máximo declarado aquí (1.25σ) no calza con el 1.23σ del banner. No
   localicé el log/script fuente de este test pese a grep amplio en
   `results/logs/*.json` — puede ser una corrida sin log guardado o una
   transcripción imprecisa. Queda abierto, no until confirmar la fuente.

3. **Ambigüedad de precisión (L762/777):** `\fscr \approx 0.0673` coincide con
   el truncamiento de `F_SCREEN_IR_d6=0.067253` (régimen IR), no con
   `F_SCREEN_d5=0.069522` (completo, que redondearía a 0.0695). El número en
   sí es consistente con el contexto (ambas veces precede o sigue al cálculo
   de 68.13 = H_glob,IR), pero conviene confirmar que el superíndice IR esté
   explícito en el LaTeX circundante para no confundirlo con el f_screen
   completo que el mismo documento usa en L1031/L876 para el H_global único.

## Lo que SÍ está bien (contraste con errores históricos de INSTRUCCIONES.md)
- No aparece `c_s²=1 (canonical)` ni `γ=0.657/0.658` sin contexto — este
  documento ya tiene `c_s²=0.021284` y `γ_IS=0.5504 > γ_ΛCDM≈0.55` explícito.
- `w_a` de DESI está correcto: `-0.617±0.208` (no el `-0.631±0.226` retirado).
- Las dos menciones de la partícula φ-DM (L750, L986) están marcadas
  "retracted"/"withdrawn" — no se presentan como predicción vigente.
- Los tres hallazgos de MCMC-full (65.87±1.17 H0, w0wa 1.31σ/3.22σ SSEE/ΛCDM,
  w=-0.655±0.107, wa=-1.104±0.304) reproducen exacto contra
  `results/logs/mcmc_full_posteriores.json`, que trae su propio bloque
  `control` de autoverificación — coinciden al dígito.
- KiDS-Legacy (417.97/418.34/6.24) coincide exacto con
  `results/logs/kids_legacy_bic.json` y sus macros ya existentes.

## Pendiente (no bloqueante)
- Varias repeticiones de `0.021284`, `9.68 meV`, `0.008131` no tienen macro
  `\val` propia pese a repetirse 5-7 veces cada una en este solo documento
  (candidatas a FIX-lite, no error de contenido).
- `G=1.0032`/`σ8=0.8136` (Paper 5) tampoco tienen macro `\val` localizada;
  valor consistente con la tabla de CLAUDE.md pero sin clave JSON confirmada
  línea por línea en esta pasada.
