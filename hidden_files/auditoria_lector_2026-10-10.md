# Auditoría "lector" — 10 papers SSEE, página por página

**Fecha:** 2026-10-10 · **Rama:** main @ `f5388f0` · **Método:** protocolo de `AUDIT.md`
**Regla del lector:** cada número se pone a prueba — si es reproducible se deja pasar, si no, se anota el porqué.
**Archivos tocados:** ninguno (solo lectura). Artefactos de la auditoría: `hidden_files/audit_val_chain_2026-10-10.json`, `hidden_files/check_val_chain.py`.

---

## 1. Verificaciones globales (hechas por el coordinador, no por inferencia)

| Chequeo | Resultado |
|---|---|
| Cadena `\val{N}` → `valores.yaml` → `results/logs/<log>#<clave>` → `valores_generados.tex` | **671/671 OK.** Cada valor del .tex coincide con su log formateado; cada log citado existe con `_procedencia` completa (commit existe en el repo, script existe). Script: `hidden_files/check_val_chain.py` (réplica exacta de `src/valores_tex.py`, incluyendo índices de lista y formato `d`/`,d`/`z.3f`). |
| Álgebra φ/π vs `src/ssee_core.py` | **Exacta.** W0, WA, H0_ALG, F_SCREEN, OMEGA_DE, KAL0, MIRA coinciden bit a bit. |
| `\val` usados en los 14 .tex vs definidos | **Todos definidos** (P1:71, P2:155, P3:144, P4:84, P5:70, P6:102, P7:66, P8:18, P9:59, P10:42, Sealed:174, Unified:118 — cero indefinidos). |
| Tablas generadas (`tabla_sondas_generada.tex`, `tabla_cronometros_generada.tex`) | Con ACTA-PROCEDENCIA y etapa DVC; celdas spot-verificadas contra el log (ej. Pantheon+: 1386.62/1387.33/−0.70 ✓). |
| Verificación estricta de actas (`src/procedencia.verifica`) sobre los 47 logs citados | **24/47 OK byte-a-byte.** 23 fallan por causas ambientales/documentadas: 16 tienen entradas en `/mnt/datos/...` o `results/chains/` (máquina de datos / cadenas pesadas, ausentes en este clon — documentado en AUDIT.md); 7 registran "entrada cambiada" porque el log de entrada fue **re-sellado después** (diffs ~1e-6 documentados en los commits, ej. `9b06108`: "dif 3e-6 vs viejo"). Ninguno afecta los valores que ven los papers (671/671). |
| Guardián (`src/verificacion/ssee_verify.py`, 349 checks) | 338 OK, 11 en rojo — **ninguno es un número mal en un paper**: R61 es falso positivo (marca su propio comentario y el `.md` viejo sin trackear `auditoria_papers_zenodo_2026-09-20.md`, que sí trae "68.13 canonical" rancio — ver nota); R35/R65/R74/R75/R60/R50/R54 son trinquetes de deuda contable; DESI/V-L3-mphi son capas de infraestructura. |
| Manifiesto `data/manifiesto_externos.json` | 110 dependencias, sha256 anidado por archivo — rutas en las máquinas de Mike (`/mnt/datos`, `/home/mike`): **no re-verificables desde este clon** (esperado). |

**Patrón transversal dominante:** los números están bien; la trazabilidad a mano no. Decenas de literales correctos tecleados existiendo `\val` para ellos (deuda de deriva futura, no error presente) — se listan por paper como ADVERTENCIA de trazabilidad sin repetir cada instancia trivial.

---

## 2. Hallazgos por paper

### Paper 1 — `SSEE_Paper1_Framework.tex`

| # | Número / ubicación | Sev. | Causa y evidencia |
|---|---|---|---|
| C1 | "agree to $4\times10^{-6}$" (L326–327) | CRÍTICO | El log da acuerdo relativo 6.18×10⁻⁸ (`H0_GLOBAL=67.96214152203791` vs `H0_ALG=67.96213732340931`), ~65× menor. Ningún log contiene 4×10⁻⁶. Además **contradice a Paper 2** (L364: $4.2\times10^{-6}$). Literal sin fuente. |
| C2 | $\Delta\chi^2_{\rm BF}=-1.8$ (L838) | CRÍTICO | El log canónico `b1_k2.json` (declarado "Titular canonico" en L816): 2768.449 vs 2771.227 → **−2.78**; `dchi2_muestreado`=−3.02; `b1_analyse.log`: −2.47. Ninguna fuente da −1.8. |
| C3 | $\gamma_{\rm IS}=0.5504\pm0.001$ (glosario L1225) | CRÍTICO | `p5_IS_perturbations_Q3.json`: `gamma_IS_sigma=0.0002662`. El ±0.001 **infla el sigma ~4×** sin justificación; existe `\val{p3_gamma_IS_sigma}` sin usar. |
| A13 | Bloque BIC cross-check: `−26.03`, `χ²=1003.586 vs 1003.596`, `N=669`, `−35.0`, `N=5914` (L820–841, L950–951, L1069–1070, L1266) | ADVERTENCIA | Verificados contra `cmb_dbic_mnu_propia.json` y `paper3_cmb_chi2.json` ✓ correctos, pero **no existen `\val`** para ellos — todo a mano. |
| A14 | `±0.968` (L322; P2 L354/L734/L982) | ADVERTENCIA | Correcto (`ssee_core.SIG_H0_GLOBAL`; el retirado era ±0.970), pero **no existe `\val`** para este sigma. |
| A15 | "0.05σ against DR1" (L167) | ADVERTENCIA | Legítimo atribuido a DR1 (el retirado lo permite), pero sin log ni `\val` → intrazable. |
| — | ~12 literales con `\val` disponible (`−0.840`/`−0.670`, `0.008131`, `0.70σ`, `0.550`, `0.0685 eV`, `0.021284`, `67.962`, `147.17`, `0.02242`, `0.24σ`, AURA/MIRA redondeos) | ADVERTENCIA | Todos numéricamente correctos; trazabilidad rota. |
| OK | Tablas (registro predictivo, BIC, falsificación, tipos, entidades) 100% `\val`; externos citados (DESI DR1/DR2, Planck 2018, SH0ES, BBN, GW170817); retirados con marca histórica (`67.037`, `0.31993`, `0.31076`, `−32.2`, `0.02285 (3.2σ)` como placeholder); derivaciones inline verificadas (`a_*=0.761`, `w₀+wₐ=−1.510`, `N=2φ⁷≈58.07`, `0.88σ`, `0.4σ`). Sin mal uso semántico de `\val`. | — | — |

### Paper 2 — `SSEE_Paper2_MCMC.tex`

| # | Número / ubicación | Sev. | Causa y evidencia |
|---|---|---|---|
| C4 | Tabla de convergencia `tab:convergence` (L496–504) + texto L475 | CRÍTICO | La nota al pie cita "the three-model comparison run" (`mcmc_paper2_3models_wmfix.log`): tabla dice τ_max=32.7/41.5/57.3, N_eff=4402/3471/2514, aceptación 0.25–0.50; el log real da τ_max=31.9/39.1/57.3, **N_eff≈78380/64007/43637**, aceptación **0.714/0.646/0.550**. Ningún log alternativo (`mcmc_professional`, `om308`, `reframe`) produce los números de la tabla. Solo coincide τ_max de CPL. Diagnósticos obsoletos. |
| C5 | Abstract L98: $r_d^{\rm SSEE}/r_d^{\rm LCDM}=1.002$ | CRÍTICO | El log (`mcmc_paper2_3models_wmfix.log` l.204 y `p2_fig8_rd.json#rd_ratio_ssee_lcdm`=1.0007999) dice **1.001**; el caption de la fig. 8 (L756) renderiza 1.001 vía `\val`. El abstract contradice al log y al propio paper. |
| C6 | L364: "to $4.2\times10^{-6}$" | CRÍTICO | Mismo origen que C1 de P1: el log da 6.18×10⁻⁸. Sin fuente; inconsistente con P1 (4×10⁻⁶). |
| A17 | Tabla w₀–wₐ (L637–640) y texto (8 celdas: 0.24/1.46/1.76/1.68; 2.58/3.93/3.38/2.62) | ADVERTENCIA | **Verificada celda por celda** contra `paper2_w0wa.json` ✓ (ec26: 0.2378→0.24, 2.5759→2.58; ec28: 1.4646→1.46, 3.9349→3.93; ec27: 1.7644→1.76, 3.3776→3.38; ec25: 1.6756→1.68, 2.6162→2.62) — pero existen `\val{p2_w0wa_ssee_ec2*}`/`p2_w0wa_lcdm_ec2*` sin usar. |
| A19 | "1.2σ" CPL free-fit (L615) | ADVERTENCIA | Sin `\val`, sin fuente localizable (candidatos 0.256/0.380/1.31/1.64 — ninguno es 1.2). Intrazable. |
| A20 | "ρ=−0.93" (L964) | ADVERTENCIA | Sin fuente en `mcmc_full_posteriores.json` (`p2_rho_cpl`=−0.95 es de otra corrida). Intrazable. |
| A25 | Caption fig. L578: "H₀≈68.0, Ω_m≈0.307" | ADVERTENCIA | El log da 68.39 y 0.302 — aproximación floja (debería ser ≈68.4, ≈0.302). |
| — | ~8 literales con `\val` disponible (`−0.840/−0.670`, `147.17/0.32σ`, `0.5504`, `0.0685 eV`, `1.042`) | ADVERTENCIA | Correctos; a mano. |
| OK | Tabla BAO DESI DR2 (L324–342): **13/13 valores+errores idénticos a `data/raw/desi_dr2_bao.csv`**; tablas clusters/BIC 100% `\val`; externos citados correctamente; retirados históricos marcados; nota: dos pares r_d (147.17 CAMB vs 147.71 MAP/EH) etiquetados distinto pero confundibles — convendría nota aclaratoria. | — | — |

### Paper 3 — `SSEE_Paper3_CMB.tex`

| # | Número / ubicación | Sev. | Causa y evidencia |
|---|---|---|---|
| C7 | Caption `tab:fsig8` (~L770) y tcolorbox (~L785): "with $\gamma_{\rm IS}=0.5504$" | ADVERTENCIA (sustancia) | El log fuente de esa tabla, `fsigma8_canonico.json`, reporta **`gamma_IS=0.5541710341110705`**, no 0.5504 (este es el `\val{p3_gamma_IS}` canónico de P5). El caption declara un input que la corrida no usó (dif. ~0.7% en γ). El `σ_8=0.8136` sí cuadra (`sigma8_ssee=0.8136026`). |
| C8 | Footnote `tab:camb_params` (~L348): "lowers χ² by only 1.84" / "ΛCDM gains 0.47" | ADVERTENCIA | Los valores recuperados sí están en `cmb_dbic_tau_ajustado.json` (τ=0.05546 ✓, logA=3.04484 ✓, 0.24σ ✓), pero **ningún log contiene los Δχ² 1.84/0.47**. El footnote fecha el chequeo "2026-09-07"; el log es de 2026-10-04 (regenerado). |
| C9 | "χ²_r=90.3" (§hiclass, ~L852) | ADVERTENCIA | Buscado en todos los `.json`/`.log`/`.py` de `results/` y `src/`: **no aparece en ningún log**. Número a mano sin trazabilidad. |
| — | ~11 literales con `\val` disponible o redondeos (`0.3089`, `67.96214`, `147.17`/`147.10` ✓ vs `rd_ssee_camb=147.1743`, `0.88σ` ✓, `1003.586/1003.596/−0.010` ✓, `669/613/28+28` ✓, `−26.03/−13.02` ✓, `4.2×10⁻⁶` ✓ vs `p9_cascada_control.json`, `±0.968` sin `\val`, `0.160` debería ser `\val{S_M_d6}`, `0.309`, `w₀+wₐ=−1.510`) | ADVERTENCIA | Todos numéricamente correctos; a mano. |
| menor | `Ω_m^Planck=0.3153±0.0073` (P3) vs `0.3153±0.007` (P4) | ADVERTENCIA | El cálculo 0.88σ usa 0.0073; la conclusión no cambia. |
| OK | Tablas (`tab:constants`, `tab:peaks`, `tab:chi2`, `tab:bic`, `tab:sigma8`, `tab:fsig8`) 100% `\val`; picos Planck ~220/540/810 con Δℓ≤5 vs `class_picos.json` (SSEE [220,536,813]); N=2354 (2289+28+28+9) ✓; `b1_k2.json` (−33.83, −18.31 k4) ✓; retirados con marca histórica (`6.66σ` como artefacto, `67.037` superseded). Ningún `\val` con significado cambiado. | — | — |

### Paper 4 — `SSEE_Paper4_ToE.tex`

| # | Número / ubicación | Sev. | Causa y evidencia |
|---|---|---|---|
| C10 | "Y_p = 0.2472" (Conclusiones, ~L870) | ADVERTENCIA (sustancia) | `algebra_derivada.json#algebra.Yp_ssee.valor=0.24714584650985583` → a 4 decimales es **0.2471**, no 0.2472 (**doble redondeo**: 0.2471458→0.24715→0.2472). Además **duplica** `\val{Yp_ssee_d4}` (=0.2471) usado en el `\boxed{}` de §BBN y en `tab:params`. Las tensiones citadas sí verifican con el log (+0.2σ Planck, +0.6σ HII). |
| C11 | `H₀^{glob,IR}=68.13` literal (abstract L66, `tab:cross`) | ADVERTENCIA | Numéricamente ✓ (`p9_cascada_control.json#sh0es.IR.H_glob=68.1278`, σ=0.1708→0.17σ), pero el mismo paper usa `\val{p9_sh0es_glob_IR}` para la misma cantidad en el footnote y en §hubble_tension → misma cantidad, dos representaciones. |
| — | ~6 literales con `\val` disponible (`Σm_ν=0.0685 eV` ✓, `(−0.840,−0.670)` ✓, `0.022420/0.02242` ✓, `0.17σ` ✓, `r=φ⁻¹⁰=0.008131` ✓) | ADVERTENCIA | Correctos; a mano. |
| menor | "K_AL×0.02242×n_s=0.11952" (§matter) | ADVERTENCIA | Con los inputs citados da 0.11953 (1 ulp); el canónico `\val{OMEGA_C_H2_d6}`=0.1195144. Tensiones citadas verifican (+2.9σ, −0.6σ, −0.4σ ✓). |
| menor | "151 times below AURA" (apéndice L907) | ADVERTENCIA | Con el bound citado `|β_c|≲0.027` sale 3.99782/0.027=**148.1**, no 151 (requeriría 0.0265). Bound exacto no localizado en log. |
| OK | Cálculos inline verificados (`8.12%`, `1.1σ`, `0.16σ`, `0.32σ`, `2.191`, `6.14×10⁻¹⁰`, `58.07`, `δ_c` vs `deltac_spherical_collapse.json` ✓); tablas 100% `\val`; `wc_estatico_ssee_*` vs `wc_estatico_planck_*` distinguidos correctamente; retirados con marca (`67.037`, `0.31993`, `1.6284` como conjetura OP-27, `0.040 eV` superseded). | — | — |

### Paper 5 — `SSEE_Paper5_IS.tex`

| # | Número / ubicación | Sev. | Causa y evidencia |
|---|---|---|---|
| C12 | "at z=99, $H/H_0 \approx 400$, so $\tau_\Pi H \approx 876$" y "timescale $\sim 1/(876 H)$" (L594–596) | CRÍTICO | **Texto rancio del fondo viejo.** La tabla `tab:background` fue recalculada el 2026-09-07 con Ωₘ=0.308881 (el comentario L635 lo documenta: "400.1 → 555.8 en z=99"); recomputo exacto con Friedmann CPL canónica: **555.8 / 1218** (E(99)=555.77, τΠH=1217.7 ✓). El cuerpo conserva los números del fondo retirado (Ωₘ,ₔᵧₙ=0.160050). La conclusión ("la aproximación cuasi-estática es aún mejor") se mantiene, pero prosa y tabla se contradicen. |
| A13 | "k ≈ 0.1 Mpc⁻¹ ≈ 230 H₀/c" (L806) | ADVERTENCIA | Recomputo: 0.1/(67.962/299792.458)=**≈441 H₀/c**, no 230. Factor ~2. La conclusión (a_stab≪10⁻³) no se afecta. |
| A14 | "Ω_DE f_DE/(H/H₀)² ≈ 8×10⁻⁶" en z=19 (L842) | ADVERTENCIA | Recomputo canónico: **≈1.9×10⁻⁵**. Factor ~2.4; el "negligible" se mantiene. |
| A15 | Tensión H₀ "at 1.1σ" (L1576) | ADVERTENCIA | La aritmética (0.602/0.54=1.11) usa **solo el error de Planck**; con errores combinados —criterio del propio paper en la tabla S₈— sería 0.54σ. Metodología inconsistente. |
| A12b | Tabla crecimiento: Ωₘ^SSEE(z=0.5)=0.588 (L1057) | ADVERTENCIA | Recomputo canónico: 0.58936→**0.589**. Resto de la tabla cuadra (<0.2%). |
| — | ~11 literales con `\val` disponible (`−0.8399/−0.6700`, `γ_IS=0.5504±0.0003` ✓, `𝓖=1.0032±0.005` ✓, `σ₈=0.8136±0.006` ✓, `S₈^IS=0.8256` ✓, techo CLASS ✓, `0.70σ/0.73σ` ✓, `0.49σ` ✓, `c²_s,ad=0.021284` ✓, `±0.968` sin `\val`, `k_crit≃0.456` derivado ✓) | ADVERTENCIA | Correctos; a mano. |
| OK | Tablas MIRA (28 celdas + media 0.9897±0.0167 ✓ vs `p5_IS_perturbations_Q2.json`), background (14/14 ✓), S₈, fσ₈, JWST (todo `\val`) verificadas; `0.3199` siempre con marca de retirado; "3.04 y 52%" como historia explícita (OP-8); 357/225 puntos ✓; `S_M_d6`/`S_DE_d6` solo en contexto histórico. Nota editorial: el outline promete un apéndice "background IS Friedmann modification" que no existe. | — | — |

### Paper 6 — `SSEE_Paper6_Growth.tex` — el más limpio de los diez

| # | Número / ubicación | Sev. | Causa y evidencia |
|---|---|---|---|
| C13 | "ΔS₈ = 0.0016" (L360 y L569) | ADVERTENCIA (sustancia) | \|0.75588822−0.75710462\|=**0.0012164 → 0.0012**, no 0.0016. Lo cualitativo ("under a tenth of either error bar") se mantiene (0.0012<0.0019). |
| C14 | "retired 2026-07-09" (L179, partición Ωₘ vía MIRA) | ADVERTENCIA | **Fecha incorrecta**: `OPEN_PROBLEMS.md` registra OP-8 disuelto el **2026-06-18** (3 entradas) y Paper 5 lo dice bien. 2026-07-09 es el fix de geometría BAO — confusión de fechas. |
| A16 | "1.01σ" (L67, L477, L484) | ADVERTENCIA | Con valores redondeados da 1.02–1.03 (\|3.0069−3.0445167\|/0.0368=1.022); 1.01 solo cuadra sin redondear. |
| A17 | "2.00%" (L479) | ADVERTENCIA | (0.315−0.30888084)/0.315=**1.94%** (el "1.88%" de la misma frase sí es exacto). |
| — | Literales con `\val` disponible (`3.0255±0.0396`, `3.04483`, `0.49σ`, `χ²=417.97 vs 418.34` — existen `\val{leg_logA}`, `\val{logA_leg_vs_cmb}`, `\val{chi2_leg_unif}` sin usar) | ADVERTENCIA | Correctos; a mano. |
| menor | Ley 52088·m^−2.283 en m=40.70 da **11.0%**, no el 10.4% citado (párrafo histórico, no resultado vigente). | ADVERTENCIA | — |
| OK | Tablas s8 KiDS-1000 (χ²/dof, Δχ²=2.6937, ΔAIC=−5.31, ΔBIC=−18.97 ✓), Legacy (Δχ²=−0.365, span 0.984 ✓), BOSS (222 pts/37 par/185 dof ✓, Δχ²=−2.027 ✓), r7 (todo `\val`) verificadas; 102 `\val` sin colisiones; retirados (40.70 eV, 594.28, 70.3, 0.160) solo como historia; "1.73×" ✓. | — | — |

### Paper 7 — `SSEE_Paper7_EFT.tex`

| # | Número / ubicación | Sev. | Causa y evidencia |
|---|---|---|---|
| C15 | L584: "distinguish $\alpha_K=\val{alpha_K_z0_d1}$ from $\alpha_K=$ **$\val{S_M_d6}$**" | ADVERTENCIA (sustancia) | **`\val` con significado distinto al de su nombre.** La constante mal etiquetada como α_K que el propio paper corrige dos párrafos antes es $s_K=\val{S_K_d12}=0.4033$ (CANONICAL: `alpha_K: 0.4033 [ETIQUETA HEREDADA] = s_K`), no $s_m=\val{S_M_d6}=0.160$. El argumento (inobservabilidad, ambos ≪15.6) sobrevive, pero el número en la casilla es el equivocado. |
| — | ~9 literales con `\val` disponible (`0.000%` abstract — log 1.214e-7%, existe `\val{p7_hc_cs2_pct}`; `0.011%` — existe `\val{p7_hc_alphaK_pct}`; `0.007%` — existe `\val{p7_hc_s8_xk_pct}`; `0.1%`/`0.03%` ℓ≥30 ✓; `2.50%` ✓; `4.5%` ✓; `z=0.31` ✓) | ADVERTENCIA | Correctos; a mano. |
| A18 | §7: "$D_1^{\rm SSEE}/D_1^{\Lambda{\rm CDM}}(\Omega_m{=}0.315)=1.003$" | ADVERTENCIA | `fsigma8_canonico.json`: G=1.0032091 ✓, pero **no existe `\val`** y el texto dice "derived in Paper 6" — ese número **no aparece** en `SSEE_Paper6_Growth.tex`. Atribución huérfana. |
| menor | §3: "appears in **nine** scripts under `src/`" | ADVERTENCIA | Conteo real: **8** archivos (7 `.py` + 1 `.pyc`) contienen `beta_c`. |
| OK | 4 tablas limpias (todo `\val` o ceros teóricos); tabla hi_class verificada (`cs2_z0`, `alpha_K_z0`, `Omega_smg=0.691041` vs `OMDE_DENS=0.691119` con explicación ✓, `Omega_m_presupuesto=0.308881` ✓); retirados declarados explícitamente (`−0.971`, `c_s²∈[0.60,0.95]`, `V_0`, `M^4=ρ_crit`, `βc=−AURA`); externos citados. Retired scan: 0 coincidencias. | — | — |

### Paper 8 — `SSEE_Paper8_StrongGravity.tex`

| # | Número / ubicación | Sev. | Causa y evidencia |
|---|---|---|---|
| C16 | Eq. `eq:Pkernel` (L207): $P(X,\phi)=X/\KAL+X^2/M^4\mathbf{-V_0 e^{-\lambda\phi/\Mpl}}$ | CRÍTICO (estructural) | **Contradice la fuente que el propio paper cita.** L200: "We adopt the SSEE canonical action from Paper 7"; Paper 7 §withdrawn: "All four belonged to the potential and coupling withdrawn in §sec:withdrawn and **no longer appear in the action**" (V₀, α, M⁴, βc). **V₀ no vuelve a aparecer en todo el paper** (término muerto, solo L207). Matiz: M⁴ como cutoff UV sí está vigente (CANONICAL `M_cutoff_meV: 9.68`; Paper 10 lo re-deriva) — hay colisión de nomenclatura, pero V₀ no tiene re-derivación en ningún paper. (Observación física adicional, no numérica: el cinético X/𝒦 con 𝒦>0 tensiona el c₁<0 —ghost condensate— exigido por Paper 7.) |
| C17 | "$F_\phi/F_N\|_{1\rm AU}\approx1.6\times10^{-31}$" (L615) | ADVERTENCIA (sustancia) | **No se reproduce de la propia fórmula del paper** $(H/k)^2\|1+w_{\rm DE}\|\Omega_{\rm DE}$ con valores del log ($w_0=−0.8399498$, $\Omega_{\rm DE}=0.6911192$): sale **$1.34\times10^{-31}$** (~20% menos; probado con H₀∈{67.037,67.4,67.96,68.13}: rango 1.30–1.34×10⁻³¹). El "factor $6\times10^{25}$" (L619) es consistente con 1.6e-31 pero hereda el sesgo. |
| menor | "$ck/H_0\approx9.2\times10^{14}$" (L612) | ADVERTENCIA | Recomputado $9.10\times10^{14}$ con H₀=67.962 (~1%; $9.22\times10^{14}$ saldría con el H₀=67.037 viejo). |
| menor | "thirty orders of magnitude below $\Mpl$" | ADVERTENCIA | $2.435\times10^{27}/9.68=2.5\times10^{26}$ → **26.4** órdenes, no 30. Prosa laxa. |
| — | ~8 literales con `\val` disponible (`βc≈4`/`3.998` ✓, `𝒦≈5.521` ✓, `2𝒦βc≈44.15` ✓, `G_eff/G≈177` ✓, `gap 0.03%` ✓, `√βc≈1.9995` ✓, `r_d=147.17` ✓, `M≈9.68 meV` ✓, `within 2%` ✓) | ADVERTENCIA | Correctos; a mano. |
| OK | Tabla `tab:lensing_numbers` limpia (teóricos exactos + retirado declarado `$1/\sqrt{\MIRA}\approx0.707$` ✓); ejemplo A1689 verificado ($42.65''$, $6.003''$, $23.91''$, 5.22%, factor 1.88 ✓; astrofísica citada a Limousin2007); identidad $f_{\rm scr}^{\rm IR}=s_K/(3\MIRA)$ exacta en el log; externos citados; retired scan: 0. | — | — |

### Paper 9 — `SSEE_Paper9_HubbleTension.tex`

| # | Número / ubicación | Sev. | Causa y evidencia |
|---|---|---|---|
| C18 | Step 4 (L1158–1165): fórmula $[1+3w_az_{\rm max}/4]$ → impreso $(1-0.025)$ | ADVERTENCIA (sustancia) | Con $w_a=−0.670$, $z_{\rm max}=0.15$ la fórmula da **−0.075**, no −0.025 (haría falta z≈0.05). Lo que sigue (0.0656, 2.5%, <0.05, 0.1%) es autoconsistente con (1−0.025), pero el primer paso no se deriva de la fórmula impresa. La conclusión vale igual con 7.5%. |
| C19 | L1047: "The agreement … is `−0.0001%`" | ADVERTENCIA (sustancia) | El valor real es **+4.2×10⁻⁶ km/s/Mpc = +6.2×10⁻⁶%** — **signo invertido y ~16× sobrestimado**. (El abstract trae bien el `+4.2×10⁻⁶`.) |
| C20 | L624: $r_{d,{\rm new}}=r_d/(1+f_{\rm sc})\approx137.3$ Mpc | ADVERTENCIA (sustancia) | Con los propios inputs (147.2/1.06725) da **137.93** — desvío ~0.6 Mpc en un contrafactual ilustrativo; la exclusión no depende de ello. |
| C21 | `tab:consistency` L647: picos `ℓ=220,540,810` | ADVERTENCIA | Los `\val` canónicos de Paper 3 son **220, 536, 813** (`p3_pico1/2/3_ssee`); el literal no coincide y no cita fuente (lo más cercano: picos observados de Planck redondeados — ambiguo). |
| — | ~13 literales con `\val` disponible (`68.13`×9 — `\val{p9_sh0es_glob_IR}` **existe y no se usa en ningún paper**; `0.06725`×9; `67.96214`×10; `0.17σ` — `\val{p9_sh0es_sig_IR}` tampoco se usa; `c_s²=0.021284`; `σ₈=0.8136`; `G=1.0032`; `r_d=147.2`; `H₀≃69.1` (`\val{requiem_C_H0}`); `+3.37%`; `(−0.840,−0.670)`) | ADVERTENCIA | Correctos; a mano. |
| OK | Retirados limpios (`71.87`, `67.037` siempre "superseded"; `±0.970` en L541 es el valor IR correcto 1.04×(1−0.06725327)=0.97006, no el redondeo retirado); `\val` H0_ALG/H0_GLOBAL/H0_glob/fscreen usados con el rol correcto tras el re-rotulado 92449fd; externos citados (Planck2018, SH0ES/Riess2022, TRGB/Freedman2024, Suyu2026). Duplicados informativos: `H0_glob` (p10 log) vs `H0_GLOBAL_d5` (álgebra) = 67.96214152203791 idénticos; `fscreen_full` vs `F_SCREEN_d6` = 0.06952161114406; `sK_full` vs `S_K_FULL_d5` — redundancia, no error. | — | — |

### Paper 10 — `SSEE_Paper10_UVCompletion.tex`

| # | Número / ubicación | Sev. | Causa y evidencia |
|---|---|---|---|
| C22 | Ruta B (L630–638): fórmula $\frac{2\,s_K^{\rm IR}\,\KAL^2}{3}$ → impreso $\approx4.1\,\rho_c$ | ADVERTENCIA (sustancia) | Con $s_K^{\rm IR}=0.40330245888789745$ (`p10_uv_fscreen.json`) y $\KAL=5.521405974759637$: la fórmula impresa da **8.1967 ρc**; 4.1 corresponde a la fórmula **sin el 2** ($s_K\KAL^2/3=4.0983$). **Factor 2** entre fórmula y número. La conclusión cualitativa ("da la escala de auto-acoplo, no 5φ⁸ρc") no cambia. |
| — | ~8 literales con `\val` disponible (`234.9 ρc`×3, `67.96214`×12, `0.06952`×3, `0.06725`, `68.13`×6, `0.17σ`, `418 ρc`×3, `1.779`) | ADVERTENCIA | Correctos; a mano (varios párrafos después sí usan el `\val`). |
| OK | Derivaciones verificadas (`9.68 meV` ✓, `2.47 meV` ✓, `r≈0.00813` ✓, `N=58.07=2φ⁷` ✓, `u_bg`, `ε`, `c_s²≈0.967`, `1.779/0.562/33%/78%`, `2.01%`, residuo `4.2×10⁻⁶` y `4.3×10⁻⁶σ` ✓, `sK_UV_pct`=3.3728% ✓, cadena CCHP ✓, `KAL_KALeff²=1.779135` ✓); `8.81 meV` solo con negación explícita (contexto que el retirado documenta ✓); 44 `\val` con semántica correcta. | — | — |

---

## 3. Notas transversales

1. **Nomenclatura `_abs` engañosa (leve):** `\val{p2_dBIC_cpl_abs}` / `\val{p2_dBIC_lcdm_abs}` usan formato `.2f`, no `abs()` — hoy los valores son positivos (6.14, 7.25) así que renderizan bien, pero si el signo cambiara, el "abs" mostraría el negativo. Además **no se usan en ningún paper**.
2. **`\val` definidos y jamás usados:** `p9_sh0es_glob_IR` (=68.13), `p9_sh0es_sig_IR` (=0.17) — P9/P10 teclean esos números a mano teniendo el `\val`.
3. **Sin `\val` para:** `±0.968` (σ de H_glob, `ssee_core.SIG_H0_GLOBAL`), usado en P1/P2/P5.
4. **Duplicados benignos:** variantes `_d4/_d5/_d6` = misma cantidad, distinta precisión (diseño intencional). `h0_3mod`≡`p2_ssee_H0_mediana`, `h0_3mod_s`≡`p2_ssee_H0_std` — mismo log#clave, mismo formato; redundancia.
5. **R61 del guardián (falso positivo):** el único "rojo" de escritura marca `auditoria_papers_zenodo_2026-09-20.md` (archivo **sin trackear** en la raíz, del 2026-09-20) que llama a 68.13 "`Canonical value`" — es un reporte viejo describiendo el error viejo, no un paper. Recomendación: archivarlo (está en `archive/` el de mayo; este quedó suelto) para que nadie lo lea como vigente.
6. **Manifiesto externo:** 110 dependencias con sha256 por archivo — verificable solo en la máquina de datos.

## 4. Lista de reparación sugerida (ordenada por visibilidad)

**CRÍTICO (contradicen log o fuente citada):**
1. P8 L207 — quitar $V_0$ del kernel o justificar su reintroducción (contradice a P7 §withdrawn).
2. P5 L594–596 — actualizar 400→555.8, 876→1218, 1/(876H)→1/(1218H) (tabla ya corregida).
3. P1 L326–327 / P2 L364 — el acuerdo H₀ es 6.2×10⁻⁸, no 4×10⁻⁶ ni 4.2×10⁻⁶ (unificar).
4. P1 L838 — $\Delta\chi^2_{\rm BF}=-1.8$ no existe en ningún log (canónico: −2.78).
5. P1 L1225 — $\gamma_{\rm IS}$: ±0.001 → ±0.0003 (o `\val{p3_gamma_IS_sigma}`).
6. P2 `tab:convergence` + L475 — la tabla no corresponde a la corrida citada (N_eff, τ_max, aceptación).
7. P2 abstract L98 — ratio r_d: 1.002 → 1.001 (log + fig. 8).

**ADVERTENCIA con sustancia (deslices internos):**
8. P10 Ruta B — fórmula↔número factor 2 (8.20 vs 4.1).
9. P4 conclusiones — Y_p: 0.2472 → `\val{Yp_ssee_d4}` (=0.2471).
10. P3 caption `tab:fsig8` — aclarar qué γ_IS usó la corrida (log: 0.5541710, no 0.5504).
11. P6 — ΔS₈: 0.0016 → 0.0012 (L360, L569).
12. P9 — Step 4 (1−0.025 vs −0.075), L1047 (−0.0001% vs +6.2×10⁻⁶%), L624 (137.3 vs 137.93).
13. P7 L584 — `\val{S_M_d6}` → `\val{S_K_d12}` en la casilla del α_K mal etiquetado.
14. P8 L615 — 1.6×10⁻³¹ no sale de su fórmula (1.34×10⁻³¹).
15. P3 — localizar o retirar χ²_r=90.3 y los deltas 1.84/0.47 del footnote.
16. P2 — "1.2σ" (L615) y "ρ=−0.93" (L964) sin fuente localizable.
17. P6 L179 — fecha OP-8: 2026-07-09 → 2026-06-18.
18. P5 — 230→441 H₀/c (L806); 8×10⁻⁶→1.9×10⁻⁵ (L842); 0.588→0.589 (L1057); revisar criterio 1.1σ (L1576).
19. P9 `tab:consistency` — picos 220,540,810 vs canónicos 220,536,813: aclarar fuente.

**Trazabilidad (deuda, no error):** ~60 literales correctos con `\val` disponible en los 10 papers; crear `\val` para ±0.968; archivar `auditoria_papers_zenodo_2026-09-20.md`; renombrar o documentar los `_abs`.

---
*Fin del informe. Ningún archivo del repo fue modificado.*
