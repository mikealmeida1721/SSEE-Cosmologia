# Respuesta punto por punto a la auditoría del lector (2026-10-10)

Informe: rama `auditoria-lector-2026-10-10` (`hidden_files/auditoria_lector_2026-10-10.md`),
hecho sobre `f5388f0`. Cotejo contra `lectura-publico-2026-09-26` el 2026-10-11.

- **Antes**: ya estaba corregido por `eb359cb` o por la cuarta lectura (10-10/10-11).
- **Ahora**: corregido en este commit.
- **No procede**: se comprobó y el texto estaba bien; va la razón.

## Críticos y advertencias con sustancia (lista §4)

| # | Punto | Estado | Qué se hizo / evidencia |
|---|---|---|---|
| 1 | P8 V₀ en el kernel | Antes | `eq:Pkernel` es `X/KAL + X²/M⁴`; V₀ sólo aparece como retirado (L217). La acción se rotula como extensión del funcional de P10, no la de P7 |
| 2 | P5 400/876 | Antes | 556 / 1218 |
| 3 | Acuerdo H: 4×10⁻⁶ (P1) / 4.2×10⁻⁶ (P2) | **Ahora** (P1) | P2 ya decía `\val{p9_hglob_residuo}` km/s/Mpc. P1 seguía con «4×10⁻⁶» sin unidades → `\val{p9_hglob_residuo}` km/s/Mpc + relativo `\val{hglob_residuo_rel}` = 6×10⁻⁸ (nuevo en `algebra_derivada`; también en P2) |
| 4 | P1 Δχ² −1.8 | Antes | `\val{b1_dchi2}` = −2.78 |
| 5 | P1 γ_IS ±0.001 | Antes | `\val{p3_gamma_IS_sigma}` |
| 6 | P2 tabla de convergencia | Antes | toda la tabla y el texto por `\val` de `resumen_3modelos.json` |
| 7 | P2 r_d 1.002 | Antes | `\val{p2_rd_ratio}` |
| 8 | P10 ruta B, factor 2 | Antes | imprime 8.20 ρc |
| 9 | P4 Y_p 0.2472 | Antes | `\val{Yp_ssee_d4}` |
| 10 | P3 γ de la tabla fσ₈ | **Ahora** | El script **no usa γ**: integra la ecuación de crecimiento y toma f = dlnD/dlna. El 0.5542 del log es el índice efectivo ajustado después (z 0–2). Corregido el método descrito (decía Ω_m^γ), el pie y el recuadro; el índice efectivo va por `\val{p3_fs8_gamma_ef}` junto al γ_IS de P5 |
| 11 | P6 ΔS₈ 0.0016 | Antes | 0.0012 por `\val` |
| 12a | P9 Step 4 (1−0.025) | Antes | sección reescrita: f_screen es constante exacta en z, no hay promedio |
| 12b | P9 −0.0001 % | Antes | `\val{p9_hglob_residuo}` km/s/Mpc |
| 12c | P9 r_d 137.3 | No procede | La fórmula impresa hoy es r_d(1−f) = 147.17×0.93275 = 137.27 → 137.3. El 137.93 sale de r_d/(1+f), que no es la fórmula del texto |
| 13 | P7 `\val{S_M_d6}` como α_K | **Ahora** | → `s_K=\val{S_K_d6}`, «the number the old label wrongly called α_K» |
| 14 | P8 F_φ/F_N 1.6×10⁻³¹ | **Ahora** | Recalculado de la propia ecuación: `\val{quinta_fuerza_AU}` = 1.3×10⁻³¹, margen `\val{quinta_fuerza_margen}` = 7×10²⁵ (era 6×10²⁵), ck/H₀ = `\val{ck_H0_AU}` |
| 15 | P3 χ²_r 90.3 y 1.84 / 0.47 | Antes (90.3) / **Ahora** | 90.3 ya no está (salió con el caso «naive» el 10-03). 1.84/0.47 no están en ningún log (`cmb_dbic_tau_ajustado.json` da el mínimo, no el χ² del punto fiducial) → frase reformulada sin ellos; τ y logA recuperados por `\val{tau_aj_ssee}`, `\val{logA_aj_ssee}` |
| 16 | P2 «1.2σ» y ρ=−0.93 | Antes / **Ahora** | 1.2σ ya no está. ρ no tenía log: `leer_mcmc_full.py` ahora escribe `distancia_w0wa.rho` = −0.934 → `\val{p2_rho_w0wa_full}` (el número era correcto) |
| 17 | P6 fecha OP-8 | **Ahora** | 2026-07-09 → 2026-06-18 |
| 18a | P5 230 H₀/c | **Ahora** | `\val{k_bao_c_H0}` = 441 |
| 18b | P5 8×10⁻⁶ en z=19 | **Ahora** | `\val{frac_de_z19}` = 1.9×10⁻⁵ |
| 18c | P5 tabla f(z), Ω_m(0.5) | **Ahora** | La tabla salía del punto de rejilla más cercano y sólo en pantalla. El script ahora interpola en z exacto y la escribe en `p5_IS_perturbations_Q3.json#tabla_f`; las 12 celdas van por `\val`. Cambian 0.790→0.791, 0.880→0.881, 0.876→0.877, 0.588→0.589, 0.747→0.749, 0.760→0.761. Q2/Q3 sin otro cambio |
| 18d | P5 1.1σ con Planck | **Ahora** | Es H_glob con su σ → errores combinados: `\val{hglob_planck_sig}` = 0.54σ |
| 19 | P9 picos 220,540,810 | **Ahora** | `\val{p3_pico1/2/3_ssee}` = 220, 536, 813 |

## Advertencias por paper (tablas §2)

| Punto | Estado | Detalle |
|---|---|---|
| P1 A13 bloque BIC a mano | Antes | cuarta lectura |
| P1/P2/P5 A14 ±0.968 sin `\val` | **Ahora** | existía `p9_hglob_sigma`; reemplazado en P1–P5, Unified, PRD y carta (13 sitios) |
| P1 A15 0.05σ DR1 | **Ahora** | sin log → frase sin el número de DR1; DR2 por `\val{p2_w0wa_ssee_ec26}` |
| P2 A25 pie 68.0 / 0.307 | **Ahora** | `\val{p2_lcdm_H0_mediana}` = 68.39, `\val{p2_lcdm_Om_mediana}` = 0.302 |
| P3 Ω_m Planck ±0.007 en P4 | No procede | P4 dice 0.3153±0.0073 en sus dos sitios; el ±0.007 de P4 es el τ de Planck (0.054±0.007) |
| P4 0.11952, 68.13 literal | Antes | — |
| P4 «151 veces bajo AURA» con cota 0.027 | **Ahora** | La cota |β_c|≲0.027 no está en P7 ni en ningún log (sólo en OPEN_PROBLEMS). Frase reescrita sin ella: el disparo bien normalizado da `\val{p7_beta_c_ok}`, de signo opuesto, y ningún número publicado depende de β_c |
| P5 apéndice prometido «IS Friedmann modification» | **Ahora** | quitado del anuncio |
| P6 1.01σ | Antes | `\val{leg_lcdm_vs_planck}` |
| P6 2.00 % | No procede (número) / **Ahora** (log) | El fondo Planck del pipeline (`cobaya_kids_legacy.py`, con m_ν=0.06) tiene Ω_m=0.31519 → 2.00 % exacto; el 1.94 % usa 0.315. El 1.88 % de A_s da 1.886 → **1.89**. Los dos salen ahora de `kids_publicados.json` por `\val` |
| P6 10.4 % (partícula) | No procede | párrafo histórico de la corrida retirada, rotulado como tal |
| P7 «nine scripts» | **Ahora** | hoy son 7, y no todos son OP-23 (guardián, álgebra) → frase sin conteo |
| P7 G 1.003 «derived in Paper 6» | **Ahora** | es de P5 (Q3) → `\val{p5_G}`, «Paper 5» |
| P7 0.000 % / 0.011 % / 0.007 % | Antes | — |
| P8 «thirty orders below M_Pl» | No procede | M_Pl = 2.435×10¹⁸ GeV = 2.4×10³⁰ meV; /9.68 meV = 2.5×10²⁹ → 29.4 órdenes. El 26.4 del informe mezcla eV con meV |
| P8 ck/H₀ 9.2×10¹⁴ | Antes / **Ahora** | ya decía 9.1; ahora por `\val` |
| P9 68.13 ×9, 0.06725 ×7, 0.17σ ×10 | **Ahora** | `\val{p9_sh0es_glob_IR}`, `\val{F_SCREEN_IR_d5}`, `\val{p9_sh0es_sig_IR}`. De paso: la ecuación `eq:prediction` rotulaba H₀^glob la fórmula IR → H₀^{glob,IR}; «0.17σ from SH0ES» y «Residual from SH0ES» → es la distancia al número puro en unidades del σ SH0ES propagado. La forma aditiva (68.44, 0.31, 0.475, 0.49σ) no tenía log → 4 entradas nuevas en `algebra_derivada` |
| P10 literales | Antes | — |

## Notas transversales (§3)

| Nota | Estado |
|---|---|
| `_abs` con formato `.2f` | No procede: se usan en el PRD; el nombre fija la convención positiva (ΛCDM − SSEE) |
| `p9_sh0es_glob_IR` / `p9_sh0es_sig_IR` sin usar | **Ahora** en uso (P9) |
| R61 / `auditoria_papers_zenodo_2026-09-20.md` | No está en esta máquina (sólo en tu copia) |

## Hallado de paso (no estaba en el informe)

- **P5**: una `tcolorbox` de ~100 líneas no partible desbordaba la página 9 por 328 pt: el texto se perdía al pie. Ahora es `breakable`. Ya existía en HEAD.
- **PRD**: desborde vertical de 28.5 pt en la página 9 (tabla look-elsewhere con nota al pie) → flotante `[tbp]`; |w_a| = 0.669975 a `\val{WA_abs_d6}`.
- **valores_tex**: 7 fuentes sin declarar como dependencia DVC (R75b) → declaradas.

Compilación: P1–P10, Unified, Sealed, PRD y carta, todos con 0 errores, 0 referencias indefinidas y 0 desbordes >15 pt.
Guardián: 4 rojos, todos de sellado o publicación (R68 PDFs de `docs/`, R75×2 re-sellado pendiente de la cola 1010, R50 tope de R75). Ninguno es un número de un paper.
