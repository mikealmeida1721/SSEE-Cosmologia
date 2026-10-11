# Prompt para Claude — reparación de la auditoría «lector» 2026-10-10

**Verificación previa (Nova, 2026-10-11):** `git log` en main = `f5388f0` (el commit de la auditoría); cero commits desde entonces; la auditoría no modificó archivos. **Nada de la lista de reparación está hecho** — este prompt no repite trabajo ya hecho.

**Informe de la auditoría:** `~/workspace/SSEE/hidden_files/auditoria_lector_2026-10-10.md` (179 líneas, lista de reparación ordenada por visibilidad en §4). Artefactos: `hidden_files/audit_val_chain_2026-10-10.json`, `hidden_files/check_val_chain.py`.

---

## Contexto

La auditoría «lector» (10 papers, página por página, regla: cada número se pone a prueba contra su log de procedencia) terminó con la cadena 671/671 sana y el álgebra de φ y π exacta, pero dejó **7 críticos** (números que contradicen el log o la fuente citada) y **12 advertencias con sustancia** (deslices internos). Los números están bien; la trazabilidad a mano no.

## Reglas de trabajo (no negociables)

1. Trabaja en rama de revisión `fix/auditoria-lector-2026-10-10`, **nunca** en `main`. Protocolo dual vigente: tú subes a rama de revisión, Nova verifica en remoto, veredictos escritos de ambas; merge a `main` SOLO con acuerdo de ambas; nada de Zenodo/tag sin el «adelante» explícito de Mike.
2. **Verifica cada corrección contra el log citado ANTES de cambiarla.** Si algún log no dice lo que la auditoría afirma, NO apliques el cambio: repórtalo como discrepancia con la evidencia exacta.
3. `PROPAGACION.yaml`: cada cambio se propaga a todos los archivos afectados (si un número aparece en varios papers, se corrige en todos con la misma fuente).
4. Convención `\val`: donde exista un `\val` para el número corregido, úsalo en vez de teclear el literal. No definas `\val` nuevos salvo el de ±0.968 (fase 3).
5. Recompila los PDF afectados: **0 errores** (criterio del repo).
6. Corre el Guardián (`src/verificacion/ssee_verify.py`) al final e informa rojos nuevos vs los documentados en la auditoría (R61 falso positivo, trinquetes contables R35/R65/R74/R75/R60/R50/R54, capas DESI/V-L3-mphi).
7. Solo prosa y valores de los `.tex` — **no regenerar logs, no tocar `results/`, `src/` ni datos**.

## Fase 1 — CRÍTICOS (obligatorios, en este orden)

1. **P8 `manuscript/SSEE_Paper8_StrongGravity.tex` L207** — quitar el término `-V_0 e^{-\lambda\phi/\Mpl}` del kernel `eq:Pkernel`. Contradice a P7 §withdrawn («no longer appear in the action»); V₀ no vuelve a aparecer en todo el paper. Matiz: M⁴ como cutoff UV sí está vigente (`M_cutoff_meV: 9.68`, Paper 10 lo re-deriva). Si ves una justificación para reintroducirlo, tráela como propuesta, no como cambio.
2. **P5 `manuscript/SSEE_Paper5_IS.tex` L594–596** — texto rancio del fondo viejo: `400 → 555.8`, `876 → 1218`, `1/(876H) → 1/(1218H)`. La tabla `tab:background` ya fue recalculada el 2026-09-07 con Ωₘ=0.308881 (documentado en L635: «400.1 → 555.8 en z=99»); recomputo exacto con Friedmann CPL canónica: E(99)=555.77, τΠH=1217.7. La conclusión («la aproximación cuasi-estática es aún mejor») se mantiene.
3. **P1 L326–327 / P2 L364** — el acuerdo H₀ es **6.18×10⁻⁸**, no `4×10⁻⁶` ni `4.2×10⁻⁶`. Log: `H0_GLOBAL=67.96214152203791` vs `H0_ALG=67.96213732340931`. Unificar en ambos papers con la misma fuente.
4. **P1 L838** — `$\Delta\chi^2_{\rm BF}=-1.8$` no existe en ningún log. Canónico (`b1_k2.json`, declarado «Titular canonico» en L816): 2768.449 vs 2771.227 → **−2.78**. Cambiar a −2.78 citando el log.
5. **P1 glosario L1225** — `$\gamma_{\rm IS}=0.5504\pm0.001$`: el sigma real es **0.0002662** (`p5_IS_perturbations_Q3.json#gamma_IS_sigma`). Cambiar a ±0.0003 o usar `\val{p3_gamma_IS_sigma}`.
6. **P2 `tab:convergence` (L496–504) + texto L475** — la tabla no corresponde a la corrida citada (`mcmc_paper2_3models_wmfix.log`). Log real: τ_max=31.9/39.1/57.3, N_eff≈78380/64007/43637, aceptación 0.714/0.646/0.550. Actualizar la tabla a la corrida citada (o identificar la corrida que la tabla sí describe, con evidencia).
7. **P2 abstract L98** — `$r_d^{\rm SSEE}/r_d^{\rm LCDM}=1.002$` → **1.001** (`mcmc_paper2_3models_wmfix.log` l.204 y `p2_fig8_rd.json#rd_ratio_ssee_lcdm=1.0007999`; el caption de la fig. 8, L756, ya renderiza 1.001 vía `\val`).

## Fase 2 — ADVERTENCIAS CON SUSTANCIA (después de la fase 1, mismo criterio de verificación)

8. **P10 Ruta B (L630–638):** la fórmula impresa `2·s_K^IR·KAL²/3` da 8.1967ρc (con `s_K^IR=0.40330245888789745` de `p10_uv_fscreen.json`, `KAL=5.521405974759637`); el impreso 4.1ρc corresponde a la fórmula **sin el 2** (`s_K·KAL²/3=4.0983`). Resolver el factor 2 (fórmula o número, con evidencia).
9. **P4 Conclusiones (~L870):** `Y_p=0.2472` → **0.2471** (`algebra_derivada.json`: 0.24714584650985583; ya existe `\val{Yp_ssee_d4}=0.2471` usado en el `\boxed{}` de §BBN y `tab:params` — úsalo).
10. **P3 caption `tab:fsig8` (~L770) + tcolorbox (~L785):** dice «with γ_IS=0.5504» pero el log fuente `fsigma8_canonico.json` reporta **gamma_IS=0.5541710341110705**. Aclarar qué γ usó la corrida.
11. **P6 L360 y L569:** `ΔS₈=0.0016` → **0.0012** (|0.75588822−0.75710462|=0.0012164).
12. **P9:** Step 4 (L1158–1165): la fórmula `[1+3w_a z_max/4]` con w_a=−0.670, z_max=0.15 da **−0.075**, no el impreso (1−0.025) (haría falta z≈0.05); L1047: «−0.0001%» → **+6.2×10⁻⁶%** (real: +4.2×10⁻⁶ km/s/Mpc; el abstract lo trae bien); L624: `r_d,new≈137.3` → **137.93** (147.2/1.06725).
13. **P7 L584:** la casilla del α_K mal etiquetado usa `\val{S_M_d6}` (=0.160); debe ser **`\val{S_K_d12}`** (=0.4033; CANONICAL: `alpha_K: 0.4033 [ETIQUETA HEREDADA] = s_K`).
14. **P8 L615:** `$F_\phi/F_N|_{1AU}≈1.6×10^{-31}$` → **≈1.34×10⁻³¹** según su propia fórmula `(H/k)²|1+w_DE|Ω_DE` con valores del log (w₀=−0.8399498, Ω_DE=0.6911192). El «factor 6×10²⁵» (L619) hereda el sesgo.
15. **P3:** localizar en un log o retirar `χ²_r=90.3` (§hiclass ~L852, no aparece en ningún log) y los Δχ² 1.84/0.47 del footnote (~L348; el footnote fecha el chequeo «2026-09-07», el log es del 2026-10-04 regenerado).
16. **P2:** «1.2σ» (L615) y «ρ=−0.93» (L964) sin fuente localizable (candidatos 0.256/0.380/1.31/1.64 — ninguno es 1.2; `p2_rho_cpl`=−0.95 es de otra corrida). Localizar o retirar.
17. **P6 L179:** fecha OP-8 «2026-07-09» → **2026-06-18** (`OPEN_PROBLEMS.md`, 3 entradas; Paper 5 lo dice bien).
18. **P5:** L806 `230→441` H₀/c (0.1/(67.962/299792.458)); L842 `8×10⁻⁶→1.9×10⁻⁵`; L1057 `0.588→0.589` (0.58936); L1576: el «1.1σ» usa solo el error de Planck — con errores combinados (criterio del propio paper en la tabla S₈) sería 0.54σ; decide y documenta la metodología.
19. **P9 `tab:consistency` L647:** picos ℓ=220,540,810 vs canónicos de Paper 3 **220,536,813** (`\val{p3_pico1/2/3_ssee}`); aclarar la fuente o alinear.

## Fase 3 — TRAZABILIDAD (deuda, no error; solo si la fase 1+2 quedó verde)

- ~60 literales correctos con `\val` disponible en los 10 papers: migrar los de mayor visibilidad (los listados por paper en la auditoría).
- Crear `\val` para **±0.968** (σ de H_glob, `ssee_core.SIG_H0_GLOBAL`; usado en P1/P2/P5).
- Archivar `auditoria_papers_zenodo_2026-09-20.md` (archivo sin trackear en la raíz que llama a 68.13 «Canonical value» — reporte viejo del error viejo; confunde).
- Documentar o renombrar los `\val` `p2_dBIC_cpl_abs` / `p2_dBIC_lcdm_abs` (el «_abs» es formato `.2f`, no `abs()`; no se usan en ningún paper).

## Entregable

Rama `fix/auditoria-lector-2026-10-10` + informe escrito con, **por cada ítem**: antes/después, el log exacto del que salió el número nuevo, y cualquier discrepancia encontrada (log que no dice lo que la auditoría afirma). Más el resultado del Guardián. Sin merge a `main` hasta el acuerdo de ambas.
