# SSEE-V3.6 — Open Problems and Known Limitations

This document records the open theoretical questions and **frontiers in progress** of the
SSEE framework. These are **not** hidden flaws: they are declared, in-process work — the
opposite of numerology (which would pretend they are solved). Ver `NUMEROLOGY_AUDIT.md`.

Last updated: 2026-07-12

---

## Leyenda de estado — cómo leer este documento (FIJADO 2026-07-12, no re-frasear)

Un problema abierto (OP) es una **frontera en proceso, NO una debilidad.** La distinción es
referee-proof y se aplica a todo el documento:

| Estado | Qué significa | ¿Bloquea publicación? |
|---|---|---|
| **CERRADO** | Derivado/verificado; se defiende ante un referí. Las afirmaciones titulares del modelo descansan aquí. | No |
| **PARCIAL** (resource-gated) | Responde bien la pregunta **hasta donde los recursos actuales permiten**; la verificación PROFUNDA requiere recursos que hoy no tengo (supercómputo, datos futuros, N-body). El resultado inmediato suele ser **falseable**. | No |
| **ABIERTO** (frontera) | Pregunta clara y bien planteada, en proceso. | No |
| **DEBILIDAD** | Una afirmación **CERRADA** que **NO se puede defender** ante un referí, por razones claras. | **Sí** |

**Regla anti-inconsistencia (para auditorías futuras — incluido Claude):** un OP **no es una
debilidad**. Una debilidad es algo que ya *afirmamos como cerrado* y que **falla ante un
referí**. El TEST para saber si un OP es debilidad: *¿alguna afirmación titular del modelo
depende en secreto de que ese OP esté resuelto?* Si **no** → es frontera (el modelo se para sin
él). Si **sí** → es carga, y hay que reclasificarla. **A hoy SSEE tiene 0 debilidades:** ningún
titular (w₀wₐ validado por DESI, r=φ⁻¹⁰=0.008131 falseable por LiteBIRD/CMB-S4,
cascada H con unidades ancladas empíricamente) depende de un OP sin resolver.
*(Corregido 2026-09-20: aquí decía «k_fs falseable», y k_fs está retirado desde
el 2026-08-01 con la partícula. El falsificador vivo es r, como ya decía el
README — los dos documentos de entrada se contradecían.)* Los OPs son profundizaciones, no huecos que
sostengan lo publicado.

**Readiness para Zenodo:** publicable = **(0 debilidades) + (OPs declarados con honestidad)**.
NO es *(0 OPs)* — eso es imposible: hasta ΛCDM tiene el problema de la constante cosmológica
abierto. No encadenar la publicación al mecanismo (OP-9/OP-10) — ver [[project_publication_strategy]].

---

## OP-1 — First-Principles Derivation of ω_b = (π−φ)/(3Ω²) (Paper 4 / baryogenesis) ✅ PARCIALMENTE RESUELTO

**Severidad: Media-Alta.** ω_b es la raíz de la que cuelgan ω_c (identidad forward de Paper 1) y Ω_m,CMB; mientras la cadena BBN no esté hecha, la coincidencia a 0.32σ es resultado de un barrido de 7 candidatos, no una derivación.

> **El "factor 200" YA NO EXISTE en el modelo (corregido en el título 2026-06-24).**
> El ω_b canónico es la fórmula algebraica `(π−φ)/(3Ω²) = 0.02242` (0.32σ Planck),
> sin ningún 200. El viejo `3(π−φ)/200` (3.2σ) quedó retirado; φ¹¹≈199 mostró que 200
> era solo una aproximación. Lo que permanece ABIERTO no es el factor — es derivar
> `(π−φ)/(3Ω²)` desde primeros principios (bariogénesis Γ_sph, programa Paper B/C).

**Location:** Paper 4, §3.2 (baryon buffer constant) — **revisado 2026-05-16**

**Corrección (sustitución algebraica del antiguo factor 200, ya retirado):**

La fórmula de Paper 4 `3(π−φ)/200 = 0.022853` tiene un error de **3.2σ** respecto a
Planck 2018 (Ω_b h² = 0.02237 ± 0.00015). La afirmación de "cuatro cifras significativas"
en el texto original era incorrecta.

**Fórmula corregida:**
$$\Omega_b h^2 = \frac{\pi - \varphi}{3\Omega^2} = \frac{\pi - \varphi}{H_0^{\rm SSEE}}$$

donde H₀^SSEE = 3(φ+π)² ≈ 67.96 km/s/Mpc es la escala de Hubble algebraica del modelo.
Tensión con Planck 2018: **0.32σ** (mejora de factor 10×).

**Identidad:** 3Ω² = 3(φ+π)² = H₀^SSEE — el denominador es la escala de Hubble,
no un parámetro libre. El factor φ¹¹ ≈ 199.005 explica por qué 200 era una aproximación.

**Scan de unicidad:** (π−φ)/(3Ω²) es el único candidato SSEE con tensión < 1σ
(7 candidatos evaluados en `archive/codigo/investigacion/open_problems/ssee_op1_baryon_density.py`).

**Interpretación física:** (π−φ) = asimetría CP del sector bariogénico; 3Ω² = H₀_SSEE =
escala de expansión cosmológica. El ratio expresa la fracción bariónica como violación CP / expansión.

**Límite residual:** La derivación desde primera principios requiere calcular Γ_sph en el
background SSEE y demostrar η_B ∝ (π−φ)/Ω³ — programa de Paper B/C (bariogénesis SSEE).

**Script:** `archive/codigo/investigacion/open_problems/ssee_op1_baryon_density.py` (cálculo completo, todos los asserts pasan)

**Argumento de bariogénesis Sakharov (refuerzo formal — 2026-05-16):**

El script `archive/codigo/investigacion/open_problems/ssee_op1_baryogenesis.py` establece la estructura Sakharov que sustenta
la fórmula (π−φ)/H₀_SSEE:

**Condición 1 — Violación de número bariónico:** Esfalerón electroweak con tasa
Γ_sph ~ α_W⁵ T⁴ (Arnold & McLerran 1987); activo para T > T_sph ≈ 131.7 GeV.

**Condición 2 — Violación CP:** δ_CP = (π−φ)/Ω = 0.3201. Este es el parámetro SSEE
que mide la asimetría entre el sector trascendental π (gauge boson loops) y el sector
algebraico φ (campo escalar). A temperatura T_EW: H_EW = (π/√90)×√g*×T_EW²/M_Pl ≈ 2.8×10⁻¹⁵ GeV.

**Condición 3 — No-equilibrio térmico:** Inflación quintaesencial → reheating gravitacional
con T_rh ≪ T_EW. El factor de dilución requerido f_dil ≈ 1.095×10⁻¹⁸ implica T_rh ~ 10⁻⁴ GeV, <!-- R74: git:a509d91104:archive/codigo/investigacion/open_problems/salidas_2026-10-02/ssee_op1_baryogenesis.log -->
consistente con el rango T_rh ~ 10⁻² – 10⁴ GeV para producción gravitacional de partículas.

**Estructura algebraica de η_B:**
$$\eta_B \sim \frac{\delta_{\rm CP} \times \Gamma_{\rm sph}}{T_{\rm EW}^4 H_{\rm EW}} \times f_{\rm dil}^{-1} \propto \frac{\pi - \varphi}{\Omega} \cdot \frac{\alpha_W^5}{H_{\rm EW}/T_{\rm EW}^4} \cdot f_{\rm dil}^{-1}$$

Cuando se normaliza con el denominador cosmológico H₀_SSEE = 3Ω², la dependencia estructural
η_B ∝ (π−φ)/Ω³ ∝ (π−φ)/(3Ω²) × (1/Ω) reproduce la fórmula empírica Ω_b h² = (π−φ)/H₀_SSEE
a nivel de conteo de potencias en Ω.

**ESTATUS HONESTO (auditoría 2026-05-16):** lo anterior NO es una derivación de η_B.
El script `ssee_op1_baryogenesis.py` calcula un η_B^naive ~ 5×10⁸ (no físico: η_B ≤ 1)
y **retro-calcula** el factor de dilución f_dil ~ 10⁻¹⁸ exigiendo que el producto
iguale el η_B observado. Es un *consistency check* (verifica que el T_rh implicado,
~10⁻⁴ GeV, cae en el rango de reheating gravitacional), NO una predicción. El scan
del paso [7] del script no discrimina entre candidatos δ_CP — todos "funcionan" con
algún f_dil. La fórmula Ω_b h²=(π−φ)/(3Ω²) es un ansatz algebraico (Type-P, Postulado D
de Paper 1); el mecanismo Sakharov motiva su FORMA, no deriva su valor. Paper 4 §3.2
revisado en consecuencia (commit de la sesión).

**EL MECANISMO SAKHAROV QUEDA EXCLUIDO (2026-09-08) — la fórmula NO se mueve.**

Lo pidió Mike, con el orden correcto: *antes de buscar el puente al sector oscuro,
probar la máquina con bariones*. Se probó, y no arranca. La temperatura de
recalentamiento que el propio argumento exige, `T_rh = 1.031×10⁻⁴ GeV`, choca con <!-- R74: git:a509d91104:archive/codigo/investigacion/open_problems/salidas_2026-10-02/ssee_op1_baryogenesis.log -->
**tres** cotas, y dos de ellas no dependen de SSEE:

| cota | piso | T_rh exigida está |
|---|---|---|
| rango quintaesencial que el propio script cita | 10⁻² GeV | 97× por debajo |
| BBN — el helio primordial que SÍ se observa (de Salas+2015, 95% CL) | 4.1×10⁻³ GeV | 40× por debajo |
| esfalerón activo (d'Onofrio+2014); `T_rh` es la T **máxima** tras la inflación | 131.7 GeV | 10⁶× por debajo |

La tercera es la letal: si el universo nunca alcanzó `131.7 GeV` después de inflar,
el esfalerón **nunca corrió**, y no pudo producir los bariones que este mismo
mecanismo dice que produjo. El argumento se contradice a sí mismo entre su
condición (i) y su condición (iii).

**Por qué sobrevivió cuatro meses.** El `η_B` se retro-calcula (ver ESTATUS HONESTO
arriba), así que se ajusta siempre y no puede fallar. El **único** sitio donde el
argumento podía romperse era el rango de `T_rh` — y ese chequeo estaba escrito
`if T_rh_required < 1e4`, mirando sólo el techo, nunca el piso. Un verde de una
sola cara sobre el único punto falsable. Corregido a tres cotas en el script;
regla **R62** instalada para que ningún chequeo de rango vuelva a mirar un solo
extremo.

**QUÉ NO SE MUEVE.** `ω_b = (π−φ)/(3Ω²) = 0.022418` sigue intacto: 0.32σ de Planck,
y el barrido `fuerza_wb` del 2026-09-08 pone el mínimo de χ² del CMB **exactamente
en el valor algebraico** (χ²=1003.00; los vecinos del barrido suben más de 200 — el barrido no guardó script ni log, las cifras exactas quedan en git). La
fórmula nunca se apoyó en este mecanismo — el documento ya declaraba que Sakharov
motivaba su FORMA, no derivaba su valor. Lo que cae es el relato de respaldo.
Ningún número de ningún paper se mueve.

**Consecuencia para OP-19.** El puente al sector oscuro (`n_c = n_b`) se apoyaba en
que `δ_CP` fuera única y llegara tanto al sector visible como al oscuro. Es única y es estructural (no
está pegada a ninguna especie), pero la ruta que la convierte en materia es
esfalerónica, y el esfalerón sólo actúa sobre el Modelo Estándar. Con el mecanismo
excluido, **la ruta ni siquiera llega a los bariones**. Ver OP-19.

**Límite residual de OP-1 — la derivación genuina (programa Paper B/C):**
1. Calcular T_rh exacto desde V(φ_inf) con α = φ⁴/3 (quintessential inflation)
2. Integrar g*(T) desde T_rh hasta T_EW para obtener el factor de dilución exacto
3. Evaluar Γ_sph(T_EW)/H(T_EW) en el background SSEE (no ΛCDM)
4. Resolver la ecuación de Boltzmann para η_B sin f_dil retro-calculado y demostrar
   que el producto reproduce η_B = 6.12×10⁻¹⁰ (BBN observacional) ab initio

**Scripts:** `archive/codigo/investigacion/open_problems/ssee_op1_baryon_density.py` + `archive/codigo/investigacion/open_problems/ssee_op1_baryogenesis.py`

---

## OP-2 — Spectral Index Exponent ns = 1 − φ⁻⁷ (Paper 4) ✅ RESUELTO (condicionado)

**Location:** Paper 4, §3.3 (inflationary sector) — **revisado 2026-05-16**

**Resolución (universalidad α-attractor + N_* = 2φ⁷):**

**Argumento primario — teorema de universalidad (Kallosh & Linde 2013):**
Para toda familia de α-atractores con α > 0 y N_* >> √α, al orden dominante en 1/N:
$$n_s = 1 - \frac{2}{N_*} + O(1/N_*^2), \quad r = \frac{12\alpha}{N_*^2}$$

En SSEE: α = φ⁴/3 (establecido en Paper 1, Appendix A.5). Los términos O(1/N_*²)
están suprimidos por ~1/(4φ¹⁴) ≈ 3×10⁻⁴ — despreciables frente al error Planck ±0.0042.

**Derivación algebraica con N_* = 2φ⁷:**
$$n_s = 1 - \frac{2}{2\varphi^7} = 1 - \varphi^{-7} = 0.9656 \quad (0.16\sigma\ \text{Planck 2018})$$
$$r = \frac{12(\varphi^4/3)}{(2\varphi^7)^2} = \frac{4\varphi^4}{4\varphi^{14}} = \varphi^{-10} \approx 0.00813$$

Ambas son consecuencias algebraicas exactas (|diferencia numérica| = 0 en doble precisión).

**Predicción nueva falsificable:** r = φ⁻¹⁰ ≈ 0.00813 — dentro del límite Planck+BKP
(r < 0.056), detectable por CMB-S4 (δr~0.002, 2030) y LiteBIRD (δr~0.001, 2028).

**Estructura Fibonacci:** N_* = 2φ⁷ = 26φ+16 ≈ 58.07 e-folds, dentro del rango
estándar N_* ∈ [50,65]. Los coeficientes {26,16} = {F₁₀, 2F₇} son números de Fibonacci.

**Consistencia slow-roll:** ε = 3α/(4N_*²) ≈ 0.000508, η = −1/N_* ≈ −0.01722.
A orden dominante en 1/N_*, n_s = 1−2/N_* = 1−φ⁻⁷ = 0.96556 ✓ (exacto) y r = 16ε = 0.00813 = φ⁻¹⁰ ✓ (exacto).
Con el slow-roll completo, 1+2η−6ε = 0.96251: la corrección O(1/N_*²) baja n_s en 0.0031.
Cuentas en `results/logs/cajones_algebra.json` (`src/verificacion/cajones_algebra.py`).
*(Errata 2026-10-02: los η y n_s que había aquí no salían de N_* = 2φ⁷; el valor viejo está en git.)*

**Límite residual:** La derivación de N_* = 2φ⁷ desde el modelo de inflación quintaesencial
SSEE (potencial V(φ_inf) con α=φ⁴/3) cierra OP-2 incondicionalmente — programa de Paper B.

**Resultado numérico Paper B (ssee_paperB_Nstar.py):**

Script `src/pB_inflation/ssee_paperB_Nstar.py` verifica la Conjetura B.1 numéricamente:
- V_end^(1/4) = 2.27×10¹⁶ GeV  (φ_end = 1.382 Mpl, ε(φ_end) = 1.000 ✓)
- T_rh que produce N_* = 2φ⁷ exacto: **9.345×10¹⁵ GeV**
- Este T_rh corresponde a ρ_rh ≈ V_end → T_rh ≈ (30/π²g*)^(1/4) × V_end^(1/4) ≈ 0.41 × V_end^(1/4)
- Elegante: si ρ_end/ρ_rh = 3 exacto (físicamente ρ_end = 3V_end con ε=1 y ρ_rh = V_end):
  N_* = 58.25 − ln(3)/6 = 58.067 ≈ 2φ⁷ = 58.069 → Δ = 0.002 e-folds = O(1/N_*)

**Nota:** T_rh(inflación) ≈ 9.4×10¹⁵ GeV es la temperatura de reheating para N_*;
distinta de T_bary ~ 10⁻⁴ GeV del argumento Sakharov (OP-1), que corresponde al
epoch de bariogénesis. Estas son dos temperaturas físicamente distintas.

**Script:** `archive/codigo/investigacion/open_problems/ssee_op2_spectral_index.py` (n_s, r) + `src/pB_inflation/ssee_paperB_Nstar.py` (T_rh completo)

**Resultado numérico Paper B (ssee_paperB_DW.py, archivado 2026-10-03) — RESULTADO NEGATIVO:**

> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7559 ± 0.0189` (0.10σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.04σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
Script `archive/codigo/investigacion/s_m_como_densidad_RETIRADO_2026-10-03/ssee_paperB_DW.py` evaluaba el segundo problema de Paper B: el
mecanismo de producción de la φ-DM **retirada** (m_φ=40.70 eV) que reproducía su densidad Ω_φDM h² (la resta retirada; el valor queda en el script archivado).

- Mecanismo Dodelson-Widrow (mezcla activo-estéril): el ángulo requerido es
  sin²(2θ)_DW ≈ 5×10⁻⁵ (fórmula Boyarsky-Ruchayskiy-Shaposhnikov 2009; el valor exacto colgaba de la m_φ retirada y el script ya no lo reproduce).
- Scan de ~80 combinaciones algebraicas de φ,π,Ω,MIRA,AURA: el mejor candidato es
  φ⁻²¹ = 4.086×10⁻⁵, con **Δ = 14.6%** — supera el umbral del 10% para "limpio".
- **Conclusión:** el ángulo de mezcla DW NO admite forma algebraica SSEE. Si se
  adoptara DW, sin²(2θ) sería un parámetro libre — violando el principio de cero
  parámetros. Es el primer resultado del modelo que no entra en el rango esperado.
- Nota de rigor: la fórmula DW (constante C_DW) tiene ~15–20% de incertidumbre
  teórica propia, por lo que perseguir un match sub-1% contra ese blanco carece
  de sentido — `Ω×10⁻⁵` (mantisa 0.5%) es numerología: el factor 10⁻⁵ no es
  algebraico (φ⁻ⁿ no genera 10⁻⁵ con n entero; requeriría n=23.92).
- **Ruta correcta (abierta):** producción gravitacional (Parker; Chung-Kolb-Riotto)
  — sin ángulo de mezcla, depende solo de m_φ y V(φ), ya fijos en SSEE. La
  estimación de orden de magnitud del script sale corta por un factor grande
  (solo prefactor); requiere la integral de producción completa con α=φ⁴/3.

**Script:** `archive/codigo/investigacion/s_m_como_densidad_RETIRADO_2026-10-03/ssee_paperB_DW.py` (DW scan + producción gravitacional preliminar; archivado con la partícula)

---

## OP-3 — Separabilidad UV-IR / el origen del `5/2` en `M⁴ = 5φ⁸ρ_c` (Paper 10) — 🟡 **PARCIAL (reabierto 2026-09-06, alineado con el Registro)**

**Severidad: Media.** No mueve ningún número publicado —la cascada UV ya declara que no mide M⁴, con σ propagado ±0.968— pero deja sin fundamentar el corte sobre el que se reformuló el Postulado C.1.

**Location:** Paper 10, Postulate C.1 / Conditional Theorem C.1.

> **Por qué se reabre.** No es una decisión nueva: `VERIFICATION_LEDGER.md`
> §V-L3-OP3 lo tiene **ABIERTO** desde la campaña de verificación, con tres
> defectos nombrados, mientras esta ficha y el README decían RESUELTO. El
> Registro manda. Esto alinea los tres documentos.

**La premisa (lo que hay que vigilar):** que `KAL_eff` se puede *elegir* sin π
y que eso basta. El teorema condicional despeja `KAL_eff` **a partir de** `M⁴`
—su propio texto dice «Dada M⁴ = 5φ⁸ρ_crit, establecido independientemente»—
así que no puede darse la vuelta y derivar `M⁴`. Es consistencia, no
derivación.

**Lo que SÍ está establecido:**

1. La jerarquía `(H₀/M)² ≈ 2.3×10⁻⁶²` es un hecho (M = 9.68 meV ≫ H₀).
2. `M⁴ = 2φ⁴·KAL_eff²` es exacto, y con `KAL_eff² = (5/2)φ⁴ρ_c` da
   `M⁴ = 5φ⁸ρ_c = 234.893569`, dif `0.0e+00`.
3. `ρ_crit` se cancela en `f_screen`: barrido de `ρ_c` por 58 órdenes de
   magnitud devuelve `f = 0.069521611144` invariante. **`M` se usa y no mete
   `H`.** (Arreglado en Paper 10 §Units, 2026-09-06.)
4. Ruta A (`KAL_eff = KAL`) queda excluida: `417.91ρ_c` vs `234.89ρ_c`. Es
   **33% en la normalización y 78% en el corte** — la misma discrepancia a dos
   potencias, porque `M⁴ ∝ KAL_eff²`.
5. Regularidad de linaje que apoya el postulado: **todo el sector
   inflacionario de SSEE es φ puro** (`α = φ⁴/3`, `n_s = 1−φ⁻⁷`, `r = φ⁻¹⁰`,
   `N_* = 2φ⁷`), y π aparece sólo de BBN en adelante (`ω_b`, `Ω`, `H_alg`,
   `w₀`, `KAL`, `MIRA`). El corte `M` se fija en la transición inflacionaria.

**Rutas cerradas por medición (2026-09-05/06). El fracaso también es dato:**

| Ruta | Cómo falla | Medido |
|---|---|---|
| **A** — el atractor produce `M⁴` vía `K_DE(X)=K_α(X/N)` | **sobredeterminada**: 2 condiciones, 1 botón | lineal pide `N=KAL ⟹ M⁴=417.91`; cuadrática pide `M⁴=5φ⁸ ⟹ N=4.139475=KAL_eff`, y entonces el término lineal pide `0.241577` donde el paper usa `0.181113`, razón `1.333842` |
| **C** — aterrizaje sobre la acción de Paper 7 | **subdeterminada Y la serie no trunca** | con `A` (el coeficiente de Paper 7) fijo y `N` libre: `M⁴` recorre cuatro órdenes de magnitud según `N` (cuenta de sesión del 2026-09-06, sin script guardado); y `X₃/X₂ = −0.6970` independiente de `N` |
| **Hubble** — que la cascada *mida* el corte | **sin poder de restricción** | σ propagado de SH0ES `±0.968` km/s/Mpc vs residuo `+4.2e-06`: `M⁴` compatible de `0.2×` a `∞` (sólo se excluye `0.1×`). Degeneración: `+1% KAL ↔ +2.01% M⁴` |

Consecuencia para el método de ingredientes: `c₂ = 1/M⁴` es un ingrediente
**libre que ningún dato disponible determina**. Tiene que venir de la teoría
(sector inflacionario, `α = φ⁴/3`), y el aterrizaje de Hubble sólo lo testea
por consistencia. **No buscarlo ahí.**

**Las tres piezas que faltan, con su dependencia:**

| Pieza | Estado | Si llega el `5/2` |
|---|---|---|
| El `5/2` — `KAL_eff` de fuente propia | **falta** | — |
| Sobre qué objeto aterriza el inflatón | **nuevo bloqueo** (rutas A y C cerradas) | — |
| `ρ_crit` en la contabilidad | ✅ **hecho 2026-09-06** | ya está |
| Jacobiano `∂φ/∂χ` en la transición | diferido a un Paper B inexistente | **deja de hacer falta** (el postulado se disuelve) |

**Criterio de cierre (pre-registrado):** una derivación del número **`5/2`**
—equivalentemente de `KAL_eff² = (5/2)φ⁴ρ_c`, o de `M⁴ = 5φ⁸ρ_c`— que
**no use el valor de `M⁴` ni SH0ES**, y que cierre en `0.0e+00`. Un parecido
no cuenta. Si eso llega, el postulado de separabilidad pasa de suposición a
resultado y el jacobiano deja de ser necesario.

**Lo que NO está en juego:** el `H₀^glob,IR = 68.13` (0.17σ vs 3(φ+π)²) de Paper 9 no
usa `M⁴` y no es condicional. Aunque OP-3 nunca cierre, esa predicción hacia
adelante queda en pie.

**Parecido registrado, NO usado como argumento:** `KAL/KAL_eff = 1.333842`
contra `4/3 = 1.333333` (dif 0.0382%). No es cero.

**Script:** `archive/codigo/investigacion/open_problems/ssee_op3_separability.py`
(contiene una autocorrección sin cerrar, `√(6α)=φ²` → «corrección: `=φ²√2`»).

---

## OP-4 — Vainshtein Radius Exceeds Observable Universe (Paper 8) — ✅ **CERRADO 2026-10-03 (por retiro del radio)**

> **Cierre 2026-10-03 (decisión de Mike: opción 2, reducir la sección a un párrafo).**
> Paper 8 ya **no cita ningún radio de apantallamiento**. La antigua §5.1–5.2 (fórmula
> `eq:rkm`, sus tres valores, la tabla `tab:vainshtein` y la figura `fig_paper8_vainshtein`)
> queda sustituida por un párrafo que dice tres cosas: (1) K(X) es de clase k-mouflage;
> (2) la fórmula anterior no cerraba dimensiones y cambiaba un factor 10³ entre GeV y eV,
> así que sus valores se retiran; (3) ningún resultado del paper necesita un radio: el
> Sistema Solar y la lente del límite canónico descansan en el acople selectivo (los
> bariones no ven el escalar) y en α_B = α_M = α_T = 0 de Paper 7 (μ−1 = 0), que valen
> para cualquier M. También se quitaron las menciones del radio en el título, la
> introducción, §2, §3, la tabla de firmas, la discusión, las conclusiones y en Unified.
> **Por qué no la opción 1 (rehacer el radio con r²):** el radio sólo importa si hay una
> quinta fuerza que apantallar, y la quinta fuerza viene del acople βc, que salió de la
> acción de Paper 7 el 2026-09-07. Calcular bien el radio de una fuerza que ya no está en
> la acción sería medir con cuidado algo que no existe. Los radios corregidos (823 AU,
> 4.0 kpc, 126 kpc) quedan en `results/logs/cajones_algebra.json` como registro.
> **Lo que queda abierto, y no es este OP:** el perfil no lineal del escalar alrededor de
> un halo (cálculo numérico), que ninguna predicción del paper usa.

> **Verificación independiente de la auditoría externa (Max, commit 17acccd) — 2026-09-19.**
> Los dos hallazgos son REALES. Se miden, no se discuten:
>
> **H1 — `eq:rkm` no cierra dimensiones.** `r³ = M_obj/(4π·Mpl·M²)`: el lado derecho es
> E/(E·E²) = E⁻² = longitud², el izquierdo longitud³. Prueba de fuego: evaluada toda en GeV
> da r☉ = 1.44×10⁴ m; toda en eV da 1.44×10⁷ m. **Un factor 1000 según la unidad elegida**:
> una fórmula bien formada no depende de eso. Los números impresos en P8 (`eq:rkm_sun`, `eq:rkm_mw`, `eq:rkm_cluster`)
> salen de evaluarla en eV (script `ssee_paper8_figures.py`), y la figura `fig_paper8_vainshtein`
> cuelga de ella.
> Forma que cierra: `r² = M_obj/(4π·Mpl·M²)` (Brax & Valageas 2014, que además lleva el
> acople). Da el MISMO radio en GeV y en eV: Sol 1.23×10¹⁴ m (823 AU), Vía Láctea 1.23×10²⁰ m
> (**4.0 kpc**), cúmulo 3.89×10²¹ m (126 kpc).
> Derivada desde la ecuación de campo del propio paper (ec. 260, Gauss + cruce
> X²/M⁴ = X/KAL): `r*² = (KAL^{3/2}/√2)·βc·M_obj/(4π·Mpl·M²)`, factor 9.17·βc sobre la
> forma de Brax. Vía Láctea: **12 kpc** (βc=1), **18 kpc** (|βc|=2.194210), 24 kpc (|βc|=AURA). <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
>
> **H2 — `eq:grad_vainshtein` tiene dimensión E⁴ para un gradiente (E²).** Con
> X = −½g^{μν}∂φ∂φ (ec. 202), el cruce da X* = M⁴/KAL y `|∇φ|* = √(2/KAL)·M²`.
>
> **La física se invierte.** La tabla dice «r_km ≪ 1 kpc: la quinta fuerza está activa a
> escala galáctica». Corregido, el apantallamiento de la Vía Láctea mide 4–24 kpc: cubre
> la galaxia interior, y con los factores del propio paper llega más allá del radio solar
> (8 kpc). A cambio, el Sistema Solar queda apantallado (823 AU), que antes NO lo estaba.
>
> **Tercer problema, que la auditoría no ve.** Toda la §4 (ec. 260, `eq:grad_closure`)
> descansa en el acople βc, y βc **salió de la acción de Paper 7 el 2026-09-07** con el
> potencial. Sin acople no hay quinta fuerza que apantallar. Lo que NO cae: la predicción
> de lensing (α_B = α_M = α_T = 0 ⟹ μ−1 = 0), que no usa βc ni esta sección.

> **Por qué se reabre.** El cierre de 2026-05-15 sustituyó la fórmula Galileon por una
> fórmula k-mouflage (Brax & Valageas 2014) en §4.2 y regeneró la figura con ella. El
> guardián mide que **esa fórmula está dimensionalmente rota**: `r_km` sale con dimensión
> GeV^(−0.667) y una longitud es GeV^(−1). Introducida en el commit `295ed6e`. El argumento
> primario (α_B = α_M = α_T = 0 ⟹ μ−1 = 0) **sigue en pie** y no depende de la fórmula; lo
> que hay que rehacer es la expresión del radio y la tabla que cuelga de ella.
>
> **Severidad: Alta.** Es una fórmula publicada en Paper 8, no una nota interna.

**Resolución previa (conservada — su argumento primario sigue válido):**

**Location:** Paper 8, §4.2 (solar system screening) — **revisado 2026-05-15**

**Resolución (dos argumentos independientes):**

**Argumento primario — estructura EFT Bellini-Sawicki:**
Paper 7 establece αB = αM = αT = 0 para SSEE, con αK = 0.4033 único. Esto implica:
- μ − 1 = (αB + αM)²/αK = 0 (constante de Newton no modificada)
- γ_PPN − 1 = −2αT/(1+αT) = 0 (sin lente gravitacional modificada)

La quinta fuerza en el límite quasi-estático se suprime como (H/k)²:
$$\frac{F_\phi}{F_N}\bigg|_{\rm 1\,AU} \approx 1.6 \times 10^{-31} \ll 10^{-5}\ (\text{Cassini})$$
Satisface la restricción solar por un factor de 6×10²⁵.

**Argumento secundario — k-mouflage (Brax & Valageas 2014):**
K(X) = X/KAL + X²/M⁴ es k-mouflage, NO Galileon. La fórmula Galileon usada en Paper 8 §4.2 original era inaplicable. Radio k-mouflage correcto:
$$r_{\rm km}^3 = \frac{M_{\rm obj}}{4\pi M_{\rm Pl} M^2}, \quad M = 9.62\ \text{meV (valor anterior; vigente 9.68)}$$
$$r_{\rm km}(\odot) \sim 10^7\ \text{m} \approx 0.02\,R_\odot \ll r_{\rm Hubble}$$ *(cifra de la resolución previa; con la fórmula rota y todo en eV hoy da 1.44×10⁷ m, ver arriba)*
Todo objeto astrofísico tiene r_km ≪ 1 kpc → quinta fuerza DM activa a escalas cosmológicas.

**Cambios aplicados en Paper 8:**
- §4.1: "Vainshtein-like" → "k-mouflage" (Brax & Valageas 2014)
- §4.2: Reemplazado fórmula Galileon con fórmula k-mouflage + Tabla revisada
- §4.4: "Double GR protection" (Vainshtein) → "EFT suppression" (αB=αM=αT=0)
- Bibitem `brax2014` añadido
- `archive/codigo/investigacion/op4_rkm_RETIRADO_2026-10-03/ssee_paper8_figures.py` (archivado 2026-10-03 con OP-4): figura regenerada con fórmula k-mouflage

**Scripts:** `archive/codigo/investigacion/open_problems/ssee_op4_vainshtein.py` (cálculo completo), `archive/codigo/investigacion/op4_rkm_RETIRADO_2026-10-03/ssee_paper8_figures.py` (figura, archivada con el radio)

---

## OP-5 — S₈ Weak-Lensing Tension (Papers 5–6) — ⚫ **DISUELTO 2026-08-01**

> **No hay tensión que resolver.** El «3.5σ» se medía con A_s FIJADO al valor de
> Planck (o sea importando la discrepancia Planck–cizalla) y contra el
> estadístico comprimido S₈, cuya reducción asume ΛCDM. Ajustando A_s al dato
> **crudo** de KiDS-1000 con un solo sector: **S₈ = 0.7559 ± 0.0189 → 0.10σ**.
> El OP no se resolvió: dejó de ser una pregunta. Lo de abajo es histórico.

**Location:** Paper 5, Table 3; Paper 6, Table 2 — **revisado 2026-05-16**

**Clarification — what IS and IS NOT resolved (canónico ω_m-directo, Ω_m=0.30889):**
- **fσ₈ (growth-rate):** NO es donde el φ-DM ayuda. El single-sector canónico (Paper 5,
  Ω_m=0.30889) da media 0.70σ; el two-sector da 0.70σ (idéntico) — ambos **empatan ΛCDM**
  (0.73σ). A escalas RSD (k≪k_fs) el φ-DM agrupa como frío, sin firma two-sector en fσ₈.
  (El viejo "2.56σ→0.50σ" usaba datos fσ₈ erróneos y/o el baseline no-canónico Ω_m=0.160;
  el "0.74/0.76σ" usaba Ω_m=0.30889 vía MIRA — ambos retirados.)
- ~~**S₈ (weak-lensing) — el desafío REAL:** single-sector S₈=0.827 (2.7σ KiDS). El
  two-sector free-streaming lo baja a **S₈_eff=0.758 (0.00σ KiDS) — RESUELVE** a nivel
  lineal/forward (m_φ=40.70 eV, cero fiteo).~~ **RETIRADO 2026-08-01.** El 0.827 es un
  **techo** medido con A_s FIJADO a Planck, no una predicción; y el 0.758 salía del
  baseline two-sector, retirado con la partícula. Con A_s libre contra el dato crudo:
  **S₈ = 0.7559 ± 0.0189, 0.10σ**. No había desafío.

**Residual abierto:** solo el refinamiento NO LINEAL pleno (N-body con feedback bariónico,
Nivel 2) — ficha **OP-5b**, severidad Baja. Ya no es la vía de rescate de ninguna tensión.

**Nivel 1 — HMcode-2020 baryonic feedback (CLASS, laptop) — COMPLETADO 2026-05-16:**

Script `archive/codigo/investigacion/open_problems/ssee_op5_hmcode.py` implementa retroalimentación bariónica AGN via
HMcode-2020_baryonic_feedback en CLASS (Mead et al. 2020, log10T_heat=7.8):

Resultados CLASS HMcode-2020 con parámetros SSEE (H₀=66.75 — input de la corrida 2026-05-16, anterior al posterior canónico 66.53 km/s/Mpc; Ω_m=0.30889, w₀=−0.840, wₐ=−0.670): <!-- R74: git:8a705d375b:archive/logs_superados/era_v36_mira_dr1/mcmc_run_20260420.txt -->

| k [h/Mpc] | B(k) = P_bar/P_hm |
|---|---|
| 0.1 | 0.9974 | <!-- R74: git:5480fef325:archive/codigo/investigacion/open_problems/salidas_2026-10-02/ssee_op5_hmcode.log -->
| 0.3 | 0.9878 | <!-- R74: git:5480fef325:archive/codigo/investigacion/open_problems/salidas_2026-10-02/ssee_op5_hmcode.log -->
| 0.5 | 0.9765 | <!-- R74: git:5480fef325:archive/codigo/investigacion/open_problems/salidas_2026-10-02/ssee_op5_hmcode.log -->
| 1.0 | 0.9560 | <!-- R74: git:5480fef325:archive/codigo/investigacion/open_problems/salidas_2026-10-02/ssee_op5_hmcode.log -->
| 2.0 | 0.9203 | <!-- R74: git:5480fef325:archive/codigo/investigacion/open_problems/salidas_2026-10-02/ssee_op5_hmcode.log -->

B_eff (lensing k=0.03–2 h/Mpc, peso k) = **0.9447** (supresión 5.53% en P(k))
B_sigma8 (top-hat integral, k<2 h/Mpc) = **0.9956** (supresión 0.44% en σ₈_eff)

> 🔴 **Tabla HISTÓRICA (retirada 2026-08-01).** Toda ella cuelga del baseline
> two-sector S₈=0.761, que se retiró con la partícula. Se conserva como registro de
> lo que se calculó entonces; **ninguna de sus filas es citable como vigente**.
> Además, la fila «DES Y3 (observado) = 0.758» debe cotejarse con la publicación
> antes de reutilizarse: el valor 3×2pt publicado por DES Y3 es 0.776 ± 0.017, y el
> 0.758 parece ser de otra combinación.

| ~~Escenario~~ | ~~S₈~~ | ~~DES Y3~~ | ~~KiDS-1000~~ |
|---|---|---|---|
| ~~Paper 6 baseline (φ-DM + WDM)~~ | ~~0.761~~ | ~~0.09σ~~ | ~~−0.25σ~~ |
| ~~+ HMcode-2020 baryonic (Mead+20)~~ | ~~0.758~~ | ~~−0.06σ~~ | ~~−0.42σ~~ |
| ~~DES Y3 (observado)~~ | ~~0.758~~ | ~~0.00σ~~ | — |
| ~~KiDS-1000 (observado)~~ | ~~0.759~~ | — | ~~0.00σ~~ |

**El baseline Paper 6 ya está dentro de 1σ DES** (0.09σ). HMcode añade Δσ = 0.03σ de mejora.

~~**Por qué el baseline está tan bien:** El two-sector φ-DM (m_φ=40.70 eV, k_fs=0.754 h/Mpc)
ya suprime P(k) en k > k_fs, sobre Ω_m,CMB=0.30889 (ω_m-directo). El HMcode añade supresión bariónica
suave adicional, principalmente a k > 0.5 h/Mpc.~~ 🔴 **RETIRADO 2026-08-01**
junto con la partícula: no hay segundo sector que suprima P(k), así que esta
explicación del baseline ya no explica nada. La supresión que queda es la
bariónica de HMcode sola, sobre un único sector Ω_m=0.308881.

**Nivel 2 — N-body completo (proyección):**

HMcode-2020 captura ~60–70% de la supresión bariónica real (McCarthy+2017, Chisari+2019).
Rango adicional N-body: ΔB_sigma8 ~ 0.03–0.07 (estimación a mano de mayo, sin log; histórica).

~~Tensión DES proyectada (estimación a mano sin log, sobre el S₈ de la partícula retirada): los dos extremos del rango quedaban entre −1σ y −2.4σ de DES.~~

~~**Falsificación:** Si N-body produce S₈ < 0.785 → OP-5 resuelto (<1.2σ DES).~~
**RETIRADO**: la proyección se medía contra el 0.758 del baseline two-sector.

**Recursos Nivel 2:** BAHAMAS-SSEE: ~5,000–10,000 CPU-horas (~USD 500–1,000);
IllustrisTNG-SSEE: ~10,000–20,000 CPU-horas (~USD 1,000–2,000).

**Script:** `archive/codigo/investigacion/open_problems/ssee_op5_hmcode.py` (HMcode-2020 completo en CLASS, todos los pasos documentados)

---

## OP-6 — Screening Form Ambiguity in Hubble Tension Resolution (Paper 9) ⚠️ RESOLUCIÓN RETIRADA (2026-10-03) — lo abierto vive en OP-6b

> **2026-10-03 — esta resolución ya no vale.** Cancelaba Ω_m,dyn/(1+w₀) con la identidad
> «1+w₀ = Ω_m», y 1+w₀ = s_m es un número de la ecuación de estado, no una densidad
> (ver banner del 0.160). Sin la identidad, el paso de universo separado no cierra. Paper 9
> lo retira (§`sec:withdrawn`) y adopta la forma multiplicativa como **postulado**
> (`eq:screen_postulate`). El valor de f_screen sigue siendo identidad exacta. El texto de abajo
> se conserva como registro de la resolución de mayo.

**Location:** Paper 9, §3 (f_screen derivation) — **revisado 2026-05-15**

**Resolución — aproximación de universo separado para k-essence:**

La forma multiplicativa sigue de primer principios de la aproximación de universo separado
(Wands et al. 2000; Brax & Valageas 2014). Para k-essence con K(X) = X/KAL + X²/M⁴,
una región sobredensa local corrige H multiplicativamente:

$$\frac{H_{\rm local}^2}{H_{\rm global}^2} = 1 + \frac{8\pi G}{3H^2}\,\delta\rho_{\phi,\rm local}$$

La perturbación de densidad del escalar en el límite cuasi-estático:

$$\frac{\delta\rho_\phi}{\rho_{\rm crit}} = \frac{\alpha_K}{3}\,\frac{\Omega_{m,\rm dyn}}{\mathcal{M}\,(1+w_0)}\,\delta_{\rm local}$$

La **identidad algebraica SSEE** $1 + w_0 = \Omega_{m,\rm dyn}$ (exacta desde el álgebra
φ,π, verificada numéricamente con |diferencia| = 0) cancela el factor Ω_m,dyn:

$$f_{\rm screen} = \frac{\alpha_K}{3\,c_s^2\,\mathcal{M}} = \frac{\alpha_K}{3\,\mathcal{M}} = 0.06725$$

(usando c²_s = 1 del Paper 5, Q1). La forma aditiva correspondería a un sesgo de velocidad
peculiar (Δv/c), no a una corrección de densidad de energía oscura — físicamente distinto.

**Verificación numérica** (`archive/codigo/investigacion/open_problems/ssee_op6_screening_form.py`):
- f_screen (universo separado) = 0.067253
- f_screen (algebraico (π−φ)/Ω²) = 0.067253
- |diferencia| = 4.1×10⁻⁷ < 10⁻⁴ ✓
- H₀,glob con el `f_screen` **IR solo** (0.067253) = 68.13 km/s/Mpc — 0.17σ,
  resultado **parcial**. El enunciado canónico usa el `f_screen` **completo**
  (IR+UV, 0.069522): 73.04 × (1 − 0.069522) = **67.962142**, residuo **+4.2e-06**
- Con la corrección UV (Paper 10, condicional a Postulate C.1): 67.962142, residuo +4.2e-06 — pero σ propagado ±0.968 lo domina

**Cambios aplicados en Paper 9:**
- §3: Derivación desde universo separado k-essence (primer principios)
- §3: Identidad 1+w₀ = Ω_m,dyn explicitada como justificación de la cancelación
- Bibitem `wands2000` y `brax2014` añadidos

**Script:** `archive/codigo/investigacion/open_problems/ssee_op6_screening_form.py` (verificación completa)

---

## OP-7 — QFT Derivation of Genesis Role Assignments (Transversal) — PARCIALMENTE RESUELTO

**Location:** Transversal — Papers 4, 7, 8 principalmente; también Papers 1, 9, 10

**Añadido:** 2026-05-19  
**Actualizado:** 2026-09-07 (el punto 2 se retiró; la cabecera decía 2026-05-21
mientras el cuerpo ya llevaba la corrección — arreglado el 2026-09-08)

**Resolución parcial (2026-05-21):**

El argumento de unicidad estructural para $\beta_c = -\mathrm{AURA}$ está ahora
formalizado en dos lugares:

1. **Paper 7 §5.2** (Eq.~`eq:phi_pi_duality`, añadida en esta sesión): el párrafo
   "Discrete duality $\varphi\leftrightarrow\pi$" muestra que KAL₀ y AURA son imágenes
   duales bajo la $\mathbb{Z}_2$ discreta, y que por lo tanto $\beta_c = -\mathrm{AURA}$
   es la única elección consistente con esa simetría — no un parámetro libre.
2. **Paper 1 §5.3** (Eqs.~`eq:id_kal`–`eq:id_aura`): las identidades algebraicas exactas
   están enunciadas formalmente con nota explícita "The open question of whether this
   discrete symmetry is an exact symmetry of the full $P(X,\varphi)$ action is catalogued
   as OP-7."

El argumento de unicidad a nivel EFT está cerrado. Lo que permanece abierto es el nivel
QFT más profundo (puntos 1–3 abajo).

**Statement:**

SSEE Genesis 5.12 (sistema algebraico adimensional, preexistente a todos los papers)
asigna roles funcionales a las constantes algebraicas:

- **AURA = (3φ+π)/2** → "Portal / Contenedor dimensional" — límite umbral 1
- **KAL₀ = (φ+3π)/2** → "Retención / Anclaje Local" — sector cinético escalar

Los papers cosmológicos dan peso dimensional a estos roles vía observables:

- ~~Paper 7: βc = −AURA para el acoplamiento disformal del fotón~~ — **retirado
  2026-09-07**: βc salió de la acción de Paper 7 con el potencial; el «<0.2%» era
  el bug de saturación (valor real −2.194210) <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
- Paper 8: geodésicas disformales del fotón usan AURA
- Papers 1–6: el sector cinético escalar usa KAL₀ como constante de retención estructural (en la capa de fluido esa retención se manifiesta como viscosidad)

**La dualidad φ↔π (establecida en esta sesión, 2026-05-19):**

La intercambiabilidad exacta es verificable numéricamente con error = 0 en doble precisión:

```
KAL₀|_{φ↔π} = AURA      (error = 0.00e+00)
AURA|_{φ↔π} = KAL₀      (error = 0.00e+00)
```

Los dos sectores son duales: el escalar/clustering φ usa la combinación π-dominada (KAL₀);
el sector φ-dominado (AURA) aparece en el screening de Hubble (MIRA=AURA/2, Paper 9). Bajo
el reframe ω_m-directo (OP-8 disuelto) la densidad de materia del CMB sale DIRECTA, sin factor
materia — el escalar usa KAL₀ dentro de ω_c:

```
ω_c = KAL₀ · ω_b · n_s = 0.11951   →   Ω_m,CMB = ω_m/h² = 0.30889
```

(0.88σ de Planck 2018: 0.3153±0.0073; la vieja cadena MIRA×Ω_m,dyn=0.30889 queda retirada)

**El gap:**

La dualidad es estructuralmente consistente y numéricamente verificada, pero **no existe un
teorema que derive por qué la teoría cuántica de campos debe reproducir estas asignaciones
de roles** desde primeros principios.

Específicamente, falta demostrar:

1. **Por qué el sector disformal (fotón) debe acoplarse con AURA y no con KAL₀:** El
   argumento actual es la dualidad φ↔π — como el sector cinético usa la combinación
   π-dominada (KAL₀), el sector fotónico debe usar la φ-dominada (AURA). Esta es una
   restricción estructural plausible, pero no un teorema de QFT.

2. ~~**Por qué βc = −AURA es la única solución**~~ — 🔴 **PREGUNTA RETIRADA
   2026-09-07.** Ya no hay que explicar por qué `βc = −AURA`: **`βc` fue
   retirado de Paper 7** junto con el potencial y el acoplamiento conformal
   (P7 §withdrawn, L80), y el nuevo Lagrangiano `K = c₁X + c₂X²` **no lleva
   ni acoplamiento ni potencial**. La pregunta presuponía un ingrediente que
   ya no existe. Además arrastraba tres errores independientes:
   - el «`βc = −AURA` verificado a <0.2%» (retirado) era el **bug de normalización de la
     saturación** (el shooting calibraba `Ω_φ(a=1)` a `0.839950` en vez de
     `0.691119`); corregido da `−2.194210`, a **45%** de AURA, no a 0.2%; <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
   - `P(X) = X/KAL₀ + X²/M⁴` **no es la acción de energía oscura** — es el
     funcional de apantallamiento de Paper 10 (cuarta aparición de la
     confusión de las dos `K(X)`);
   - y la brecha `Δw` que `βc` cerraba **no era física**: `w = −1 + λ²/3` con
     `λ = √(3(1+w₀))` devuelve `w₀` con diferencia `0.000e+00`, o sea es
     tautología.

   Lo que queda de verdad en pie es **OP-23**, y es otra pregunta: **ningún
   fondo reproduce `wₐ = −0.670`** (atractor `−0.093`, `λ=1.0205` da `−0.211`,
   acoplado `+0.408` con el signo contrario; `results/logs/fondos_exponenciales.json`). El problema es la **forma del
   potencial**, no `βc`.

3. **La conexión escala Planck → escala cosmológica:** El sistema Genesis 5.12 es
   adimensional. La dimensional weight se asigna vía cosmología (Papers 1–10). Falta el
   teorema que muestre que la física de QFT en la escala de Planck reproduce inevitablemente
   los roles de Genesis 5.12. Esta es la "Derivación Cuántica Dimensional" de la arquitectura.

**Consecuencia si permanece abierto:**

~~La predicción βc=−AURA es correcta (verificada por CAMB, CLASS, DESI a <0.2%)~~
🔴 **RETIRADO 2026-09-07** — ese «<0.2%» era el bug de saturación, y `βc` ya no
está en la acción. Lo que sí sigue en pie de OP-7 es el punto 1 (por qué el
sector disformal se acopla con AURA y no con KAL₀) y el punto 3 (el puente
escala de Planck → escala cosmológica): el argumento de unicidad descansa en la
dualidad estructural φ↔π, no en una simetría explícita de la acción. Un referee
podría aceptarlo como condición de consistencia pero no como derivación. Ese
sigue siendo el gap más profundo del modelo.

**Programa de cierre (largo plazo):**

Identificar la simetría en el espacio de parámetros de KAL₀ / AURA bajo φ↔π como una
simetría discreta de la acción P(X,φ), y mostrar que esa simetría discreta — cuando se
impone a nivel de QFT — fuerza βc=−AURA como valor único del acoplamiento disformal
(vía **retirada 2026-09-07**: βc ya no está en la acción, así que esta ruta de cierre
queda sólo como registro).
Esto conectaría el sistema Genesis 5.12 con la física de campos desde primeros principios.

**Severidad:** Alta — es el gap conceptual más profundo. No falsifica SSEE a la precisión
observacional actual, pero es el requisito para que el modelo tenga derivación completa
desde primeros principios (necesario para aspirar a nivel de premio).

---

## OP-8 — MIRA Dynamical Mechanism (Papers 3, 5, 7, 8, 9) — ✅ DISUELTO 2026-06-18

> **CIERRE (reframe ω_m-directo, 2026-06-18).** OP-8 preguntaba por qué el factor
> de duplicación materia $\Omega_{m,{\rm CMB}}/\Omega_{m,{\rm dyn}}$ vale
> $(3\varphi+\pi)/4$ (MIRA) y no $2$. **El reframe elimina la premisa:** la materia
> del CMB ya **no** se obtiene duplicando el sector dinámico. Es el observable
> físico estándar $\omega_m = \omega_b + \omega_c + \omega_\nu = 0.14267$, con cada
> pieza algebraica de SSEE:
> - $\omega_b = (\pi-\varphi)/(3\Omega^2) = 0.02242$  (OP-1)
> - $\omega_c = \mathrm{KAL_0}\cdot\omega_b\cdot n_s = 0.11951$  (identidad **forward**, ya en Paper 1, 0.41σ)
> - $\omega_\nu = \Sigma m_\nu/93.14\,\mathrm{eV} = 0.000735$
>
> y $\Omega_{m,{\rm CMB}} = \omega_m/h^2 = 0.30889$ es **derivado**, no postulado.
> Es la **única** densidad de materia del modelo. $s_m=1+w_0=0.160$ es un número de la
> **ecuación de estado**, no una densidad (2026-07-30); lo que DESI prueba es $(w_0,w_a)$
> y la geometría con este mismo $\Omega_m$. *(Hasta el 2026-10-03 este bloque llamaba a
> 0.160 «$\Omega_{m,\rm dyn}$ (DESI)» y lo presentaba como una segunda predicción de
> densidad; corregido.)*
> Verificación CMB Fase B (Planck plik_lite+lowT+lowE, $H=67.962$, $\{A_s,\tau\}$ ajustados, $N=669$):
> $\chi^2_{\rm SSEE}=1003.586$ vs $\chi^2_{\Lambda{\rm CDM}}=1003.596$ (su mν 0.06),
> $\Delta\mathrm{BIC}=-26.03$ → SSEE favorecido (era −26.21 con ΛCDM en la mν de SSEE, y antes −24.02 con $A_s,\tau$ clavados y $N=613$)
> (`results/logs/cmb_dbic_mnu_propia.json`; el log de la Fase B vieja quedó en `archive/logs_superados/p3_cmb_reframe_omega_m.log`).
>
> **Residuo honesto (no es perilla nueva):** $\Omega_{m,{\rm CMB}}$ ahora descansa
> en que $\omega_b$ (OP-1) y la identidad $\omega_c=\mathrm{KAL_0}\cdot\omega_b\cdot n_s$
> sean correctos — piezas que el modelo **ya tenía**. **MIRA persiste como entidad**
> $=\mathrm{AURA}/2$ y conserva su rol en $f_{\rm screen}=(\pi-\varphi)/\Omega^2$
> (invariante); lo que se retira es su rol de **factor-materia**. El análisis
> histórico abajo (siete mecanismos, identidad $\Omega_{m,{\rm dyn}}=\Omega_{\rm geom}/2$)
> queda como registro; ya no carga el peso de un problema abierto.

**[HISTÓRICO — premisa superada por el reframe ω_m-directo]**

**Location:** Transversal — referenced in Papers 3, 5, 6, 7, 8, 9 as "the MIRA bridge."

**Problem:** The MIRA factor $(3\varphi+\pi)/4 \approx 1.9989$ is **algebraically exact**
and **observationally required** (CLASS validation 2026-05-09 showed CMB peaks shift
10% wrong without MIRA, RMS 31.5% vs 1.4%). However, **no dynamical mechanism derives
its value from first principles.** Seven candidate mechanisms have been tested and
ruled out (VERIFICATION_LEDGER §V-L3-mira, V-L3-saturacion, derivative coupling,
forward φ-MDE, etc.):

1. $c_s^2$ clustering — fails by magnitude (~100× too small)
2. $\mu>1$ Poisson modification — fails structurally (P7 forced $\alpha_B=\alpha_M=0$)
3. Disformal P8 — fails axiomatically (requires $\psi_{DM}$, P1 originally prohibited)
4. Conformal coupling $\beta_c = -$AURA — fails magnitude+sign+timing
5. Conformal coupling $\beta_c = \pm\alpha_{\rm sat}$ (veta-2) — fails connectivity
6. Derivative coupling $L_{\rm int} = (X/M^4) L_{DM}$ — fails UV scale
7. Forward integration from φ-MDE — fails matter drainage

**Current status:** MIRA enters the model as an **empirical input with exact algebraic
value**, not as a derived consequence. The framework's working interpretation
(two-sector dark matter, Paper 6) provides a phenomenological structure that
reproduces MIRA's numerical value via $\Omega_{m,{\rm CMB}}/\Omega_{m,{\rm dyn}} \approx 2$,
but this is a parametrization, not a dynamical derivation.

**Finding 2026-06-05 — OP-8 and Roadmap-point-2 collapse to a single number.**
The previously separate "$\Omega_{m,{\rm CMB}}$ dual" puzzle (Roadmap-point-2:
geometric route $\Omega_{\rm geom}=(\pi-\varphi)/(\pi+\varphi)=0.3201005$ vs
MIRA route $\mathrm{MIRA}\times\Omega_{m,{\rm dyn}}$ (retired; digits in git, no log), a $0.054\%$ gap
read as a possible loop/self-energy correction) is **not a second coincidence**.
It is the **same object** as MIRA's deviation from the integer $2$. Proven to
machine precision (difference at the $10^{-17}$ level) and by hand:
- $M_v = \varphi+\pi+K_v = 3\Omega$ (since $K_v=2\Omega$, $\Omega=\varphi+\pi$);
  $\mathrm{TRIAL}=3(3\varphi+\pi)/2$, so $M_v-\mathrm{TRIAL}=3(\pi-\varphi)/2$.
- Therefore $\Omega_{m,{\rm dyn}}=(M_v-\mathrm{TRIAL})/M_v=(\pi-\varphi)/\big(2(\pi+\varphi)\big)=\Omega_{\rm geom}/2$ **exactly**.
- The dual's fractional deviation is then identically
  $(\Omega_{\rm geom}-\mathrm{MIRA}\cdot\Omega_{m,{\rm dyn}})/\Omega_{\rm geom}
  = 1-\mathrm{MIRA}/2 = (2-\mathrm{MIRA})/2 = (8-3\varphi-\pi)/8 = 0.0538\%$.

So MIRA's distance from $2$ **fully determines** the $\Omega_m$ dual: one number,
$(8-3\varphi-\pi)/8$, not two independent $\sim0.054\%$ near-coincidences. This
gives MIRA a concrete root as $\mathrm{AURA}/2$ (half of the first dimensional
ceiling $\mathrm{AURA}=(3\varphi+\pi)/2$), which propagates the dimensional reading
to the **entire AURA branch** (the copy-law ladder MIRA·1, AURA·1, DUAL·2,
TRIAL·3, … spaced by exactly one AURA — the "dimensional ceilings"). The dual
exists *because* $\mathrm{AURA}\neq4$ exactly. Verification: `archive/codigo/investigacion/op8_mira_aura_dimensional.py`.

**Status of this finding (audit phase 2 — honest residue):** the identity is
**internal** (everything follows from the $\varphi,\pi$ definitions of $K_v$,
$M_v$, TRIAL), so it **tightens** the problem from two knobs to one but does
**not** supply the dynamical mechanism. The interpretation "MIRA = half dimensional
ceiling" stays in the *sistema SSEE* (interpretive layer) until a physical
mechanism validates it; the algebra $\Omega_{m,{\rm dyn}}=\Omega_{\rm geom}/2$ is
already *modelo*-grade. The problem is now **surrounded, not solved**: one must
still derive why the doubling factor is exactly $(3\varphi+\pi)/4$ and not $2$.

**Path to resolution:** A first-principles QFT/UV derivation showing why MIRA must
take this specific value — equivalently, why the matter-sector doubling is
$(3\varphi+\pi)/4$ rather than the integer $2$ (the $(8-3\varphi-\pi)/8$ residue).
Possible candidates not yet tested: k-mouflage with matter-coupled
velocity-dependent screening, two-scale UV completion with discrete
self-similarity, holographic principle constraint.

**Severity:** High — this is the central open problem of SSEE-V3.6. Until resolved,
the model has ~3 effective free parameters (vs 6 in $\Lambda$CDM); when resolved,
it returns to ≤2 (only $H_0$ and $\Omega_b h^2$ as observation-tunable).

---

## OP-9 — UV Origin of the Mass Multiplier — ⚫ CERRADO POR DISOLUCIÓN (2026-08-01)

> 🔴 **CERRADO POR DISOLUCIÓN — 2026-08-01.** El objeto del que trataba este OP
> ya no existe: el sector φ-DM y su partícula fueron **retirados** en el Paper 6,
> por dos razones independientes.
> **(1)** Su densidad se definía como Ω_φDM = Ω_m,CMB − Ω_m,dyn = 0.308881 − 0.160,
> restando una densidad medida menos un número de la **ecuación de estado**
> (0.160 = 1+w₀). La resta está bien formada aritméticamente y vacía de física
> ⟹ la partícula no tenía de qué estar hecha.
> **(2)** La tensión S₈ que motivaba todo el sector no existe en el dato crudo:
> con un solo sector y A_s libre, el MCMC contra los 225 puntos de ξ± de
> KiDS-1000 da **S₈ = 0.7559 ± 0.0189 → 0.10σ**.
>
> **No está resuelto: dejó de ser una pregunta.** Se conserva lo de abajo como
> registro de qué se preguntaba y por qué. **No citar como abierto.**
>
> **Lección durable:** la falsabilidad es requisito mínimo para que una hipótesis
> sea científica, **no evidencia de que la entidad exista**. Y una cadena puede
> ser dimensionalmente impecable y aun así no significar nada.


<details><summary>Registro histórico (la pregunta tal como estaba planteada)</summary>


> [!nota] ESTADO CANÓNICO ÚNICO (2026-07-12) — leer esto, ignorar redacciones antiguas abajo.
> **Estado en UNA palabra: OP-9 está ABIERTO.** No lo llamamos "cerrado" en ninguna mitad —
> eso confundía. Lo que existe es una partícula usable y una derivación pendiente; solo la
> segunda es OP-9.
>
> $m_\phi = \Sigma m_\nu^{\rm act}\cdot\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V = 0.0685\cdot594.28 = 40.70$ eV.
> $\mathrm{SOLAR}=\mathrm{BIAL}+\mathrm{KAL}=\varphi+2\pi$; $\mathrm{KRYSTOS}_V=\varphi+\pi+\Omega$
> (padres {φ,π,Ω} — **NO** "2Ω"). Forma $g^2v$, escrita en el Lagrangiano escalar libre de Paper 6.
>
> **Para que quede claro qué falta y qué no:**
> - **Lo que YA funciona (esto NO es lo que OP-9 pregunta):** la partícula tiene masa
>   dimensionalmente correcta, sin fiteo, escrita como término $g^2v$ de un Lagrangiano real, y
>   es **falseable** ($k_{\rm fs}=0.754\,h/$Mpc, DESI Y3/Euclid). La *decisión* de usar esta
>   partícula ya está tomada — eso es **OP-17**, no OP-9.
> - **Lo que FALTA — LA PREGUNTA ABIERTA, exacta (esto SÍ es OP-9):**
>   > ¿Existe un potencial $V(\phi)$ construido **solo de φ,π** cuya **curvatura en el mínimo**
>   > reproduzca el coeficiente 594.28 —es decir, $m_\phi=\Sigma m_\nu\cdot594.28$— **sin
>   > meterlo a mano**?
>   >
>   > (Imagen: la masa = qué tan curvado está el fondo del valle del campo. La pregunta es si un
>   > valle con forma pura φ,π se curva *exactamente* eso. $m_\phi^2 = V''(\phi_{\min})$.)
>
> **Relación OP-9 ↔ OP-10 (para NO marear la pregunta):** comparten la **misma respuesta** — el
> potencial. **OP-10** = derivar el potencial completo (la *función*, el valle entero). **OP-9**
> = el *número* que ese valle debe escupir (la curvatura del fondo). Resuelto OP-10, OP-9 **cae
> solo**: son **un problema en dos resoluciones**, no dos problemas. Lo que le da nombre propio a
> OP-9: es la parte del potencial **ya expuesta a datos** ($k_{\rm fs}=0.754$) → el programa se
> puede **FALSAR por OP-9 antes** de tener OP-10. El intento acotado de derivarlo por transporte
> (Camino B, KAL, 2026-07-11) dio **CORTE**; la vía viva es el $V(\phi)$ de OP-10, más allá del
> horizonte TRIAL.
>
> **No confundir con OP-17** (¿la partícula sirve y es falseable?) → eso YA está decidido (sí).
> OP-9 pregunta SOLO por el origen del coeficiente. Mezclarlas produce el falso vaivén
> "falta/no-falta".
>
> Que OP-9 esté abierto **y declarado abierto con la pregunta exacta** es lo CONTRARIO de
> numerología (que fingiría tenerlo resuelto). Incompletitud, no inconsistencia. El bloque
> histórico (615.33, 1/537) es rastro, no estado. Ver [[project-op17-particle-deferred]], <!-- R74: git:f3b01e5c2d:CANONICAL_VALUES.yaml -->
> [[project-nine-sovereigns-naming]].

**Location:** Paper 6, §3.2 (subsec:mass_derivation), §3.4 (subsec:lagrangian), §6 (subsec:origin).

**Status change (2026-06-04):** The old phenomenological ansatz $m_\phi = \Sigma m_\nu
\times 3(\varphi+\pi)^2 = 5.602$ eV is **superseded**. The canonical particle is now <!-- R74: git:85e680ef29:results/logs/cmb_dbic_tau_ajustado.json -->
fixed by a **zero-fitting forward chain** (Vía 2 + multiplier), locked by Mike:

```
R₂   = Ω_DNAV/(KAL·TRIAL)          = 0.07188      (pure φ,π number)
Σm_ν = R₂·ω_b·C_ν/(τ_Π·H₀)          = 0.0685 eV     (fixed mass scale)
mult = SOLAR² · KRYSTOS_V            = 594.28        (PURE φ,π number)
m_φ  = Σm_ν × mult                 = 40.70 eV      (forward prediction, zero fitting)
T_φ                                = 0.5385 T_ν    (from relic-abundance constraint) <!-- R74: git:d7446ace8a:results/logs/p6_class_reframe_omega_m.log -->
```

**What changed in the gap:** the coefficient is no longer a *loose* numerological factor.
The canonical multiplier $\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V = 594.28$
is a **pure $(\varphi,\pi)$ number**, so $m_\phi = \Sigma m_\nu \times (\text{pure number})
= [{\rm eV}]$ is **dimensionally consistent**. Crucially, this coefficient is now the
**mass term of a written scalar Lagrangian**:
$$\mathcal{L}_\Phi = \tfrac{1}{2}\partial_\mu\Phi\,\partial^\mu\Phi
  - \tfrac{1}{2}\bigl[\Sigma m_\nu(\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V)\bigr]^2 \Phi^2.$$
The coefficient enters as $m_\Phi^2$ in a Lagrangian that is *written down*, not as a
floating ansatz. **This closes the incompleteness flagged in the original OP-9** (the
coefficient now comes from a Lagrangian mass term, not a bare numerological multiplier).

**What remains open (the refined OP-9):** the **UV origin of the canonical multiplier**
$\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V=594.28$ (adopted 2026-06-19; supersedes the
intermediate $\mathrm{PYROS}\cdot\mathrm{VITA}\cdot\mathrm{MIKA}=615.33$ and the older <!-- R74: git:f3b01e5c2d:CANONICAL_VALUES.yaml -->
$\Omega_{\rm DNAV}^4+\mathrm{AURA}\cdot\mathrm{KAL}=535.28$) — i.e.,
why *this* particular combination of $(\varphi,\pi)$ constants sets the curvature of the
potential at its minimum. The Lagrangian is written, but the multiplier's derivation from
a unified $V(\phi)$ (OP-10) is the next step. This is **incompleteness, not inconsistency**.

> [!warning] Bloque histórico (615.33-era). El análisis look-elsewhere que sigue <!-- R74: git:f3b01e5c2d:CANONICAL_VALUES.yaml -->
> (1/537, 1/192) corresponde al multiplicador **intermedio** $\mathrm{PYROS}\cdot
> \mathrm{VITA}\cdot\mathrm{MIKA}=615.33$, hoy **superado** por $\mathrm{SOLAR}^2\cdot <!-- R74: git:f3b01e5c2d:CANONICAL_VALUES.yaml -->
> \mathrm{KRYSTOS}_V=594.28$. La selección vigente bajo la gramática de linaje estricta
> es **1/3**, no 1/cientos — ver «Methodological note» más abajo. Se conserva por registro.

**Look-elsewhere of the multiplier (2026-06-18, `op9_particle_existence.py`).** Honest
test before enshrining the particle: of all closed-dictionary constructions (21 named
entities + root powers) landing in the *physically viable* window $M=m_\phi/\Sigma m_\nu
\in[295,988]$ (i.e.\ $k_{\rm fs}\in[0.3,1.5]\,h/$Mpc, relevant to $S_8$ without erasing
structure — **not** a fit to a target), the count is strongly grammar-dependent:
permissive grammar (powers+products+sums) gives $1/537$; pure triple-products
("volumes", 3 ceilings) give $1/192$. **Verdict:** PYROS, VITA, MIKA are *real*
dictionary entities, but the multiplier is **not statistically privileged** under a
permissive grammar — its uniqueness is exactly as strong as the lineage-law grammar we
can rigorously justify (the narrow "no-self-sum" rule once gave $\sim1/16$; pinning this
down is the substance of OP-7/OP-9). Versus the old 535.28: statistically similar, but
615.33 is a **pure 3-volume** (cleaner, more Lagrangian-derivable) vs a power$+$product <!-- R74: git:f3b01e5c2d:CANONICAL_VALUES.yaml -->
*sum* — a better *form* for a UV derivation, **not** a stronger statistical selection.
Implication: OP-9 is **not** closed by the dictionary; the promising route is a UV
completion whose $V''(\phi_{\rm min})$ is literally a 3-volume of structural scales.

**Leading mechanism candidate (2026-06-19) — $M=\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V$.**
A data-driven probe (let $m_\phi$ float in CLASS, find what $S_8$ prefers;
`ssee_paper6_particle_scan.py`) gives a data-preferred $m_\phi\simeq41.0$ eV
($M\simeq594$, $S_8=0.00\sigma$ vs the forward 615.33 at $0.24\sigma$). At that value the <!-- R74: git:f3b01e5c2d:CANONICAL_VALUES.yaml -->
construction $M=\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V=(\varphi+2\pi)^2\cdot(\varphi+\pi+\Omega)=594.28$
($m_\phi=40.70$ eV) is notable because — unlike a generic look-elsewhere hit — every
ingredient is **lineage-anchored** to an *already-established* role (the standard set by
KAL$\to$viscosity and MIRA$\to f_{\rm screen}$):
- $\mathrm{KRYSTOS}_V=\varphi+\pi+\Omega$ (padres {φ,π,Ω}; Paper 4), already anchors $w_a=-P_{sc}/K_v=-0.670$
  (DESI). The vacuum scale is **not** assigned here.
- $\mathrm{SOLAR}=\mathrm{BIAL}+\mathrm{KAL}$: BIAL ($=(\varphi+\pi)/2$, the genesis
  "first heat/pulse" — radiative seed) $+$ KAL ($=\beta+\pi$, the **established bulk
  viscosity** $\tilde\zeta=\mathrm{KAL}_0/3$, Paper 5). Both parents are thermal/dissipative,
  so SOLAR as the **radiative–dissipative coupling** is *inherited*, not chosen; its value
  $\varphi+2\pi$ is forced by the lineage.
- Form $m_\phi=g^2 v\,\Sigma m_\nu$ is a standard generated mass (self-energy $\propto g^2$,
  vacuum $v$, neutrino-portal seed). The $\times594$ is an **enhancement** (seesaw/geometric),
  not a loop (loops suppress) — so a loop-radiative narrative is wrong; enhancement is right.

**Honest residue (why this is *candidate*, not *closed*):** (i) it was assembled after
fitting $m_\phi$ to $S_8$ (timing — not forward); (ii) the quantitative coefficient
$\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V$ is dimensionally standard but **not yet derived** by
solving the dissipative ($\mathrm{KAL}_0$-governed) free-streaming/mass equation — the
obvious shortcuts (relic $T_\phi$, $V''$) don't yield SOLAR trivially; (iii) free-streaming
(collisionless) vs IS bulk viscosity (fluid) are technically different dissipations, so the
"single $\mathrm{KAL}_0$ governs both" unification is the claim to prove. Status: SOLAR moved
from "a number that fit nicely" to "BIAL(first-heat)+KAL(anchored viscosity), standard
$g^2v$ form" — a real qualitative anchor; the closing calculation is the explicit
dissipative mass derivation. Scripts: `op9_multiplier_search.py`,
`ssee_paper6_particle_scan.py`. **Canonical particle is now SOLAR²·KRYSTOS_V=594.28
($m_\phi=40.70$ eV), adopted 2026-06-19 (OP-17); the open OP-9 residue is deriving its
coefficient from KAL-governed dissipative transport.**

**Methodological note — lineage-restricted prediction, not blind search (2026-06-20).**
The construction was *not* obtained by combining dictionary constants until one hit 594.
The procedure was: (1) ask what *value* the physics requires (the $M$ that makes $S_8$
close, given our neutrino data + SSEE physics); (2) ask which construction the **lineage
laws** emit *naturally* — i.e. constrained by rules that pre-exist the particle
(no-self-sum, the AURA copy-law at the bifurcation, role-inheritance). SOLAR=BIAL+KAL and
KRYSTOS_V=2Ω came out of step (2) because their *parents already had roles*, not because
their numeric value was convenient. This is **lineage-restricted selection**, categorically
different from a free fit: the admissible space is fixed by laws, not by the datum. The
honest residue is therefore **not** "it was post-hoc" in the loose sense — it is that the
*strength* of "emerged from the lineage" equals **how restrictive the lineage grammar
provably is**, and that number has not yet been measured. The look-elsewhere scans run so
far used *permissive* grammars (products+sums+powers → 1/537; triple-products → 1/192);
the **lineage-strict grammar** (no-self-sum ∧ copy-law ∧ each factor role-anchored ∧ $g^2v$
form) has **not** been counted. **DONE — residue (i) quantified (2026-06-20,
`op9_lineage_grammar_scan.py`):** counting admissible constructions in the viable window
$M\in[295,988]$ under each rule of the lineage grammar gives a sharp gradient:
permissive → 1/hundreds; **L1** (physical form $g^2v$, $M=X^2Y$) → 1/143; **L1+L2**
(+no-self-sum) → 1/80; **L1+L2+L4** (+prior role: coupling$^2\cdot$scale, with
couplings $\{$BIAL,KAL,SOLAR,AURA$\}$ and scales $\{$KRYSTOS_V$=2\Omega$,OMEGA,PYROS$\}$,
each role declared with paper provenance) → **1/3**. The three survivors all share
$\mathrm{SOLAR}^2$ and differ only in the scale (SOLAR²·OMEGA=297, SOLAR²·PYROS=398,
**SOLAR²·KRYSTOS_V=594**); of the three, KRYSTOS_V$=2\Omega$ is the only scale that already
anchors $w_a$ (the DE vacuum scale) — a physical reason to prefer it within the 1/3.
Crucially the old $\Omega^4+\mathrm{AURA}\cdot\mathrm{KAL}=535.28$ is a **sum**, so it
**fails L1** ($g^2v$ form) and is excluded by physics, not by tuning. **Verdict:** the
timing objection (i) is answered — selection is 1/3 under the grammar actually used, not
1/hundreds. Caveat (honest): the role assignment (L4) is *declared, not unique*; this
measures how constrained the choice was, it does **not** prove the coefficient. Residue
(ii) — deriving 594.28 as the *output* of the $\mathrm{KAL}_0$ transport equation —
remains the deeper closure via OP-10. See [[project-op17-particle-deferred]],
[[project-ssee-lineage-laws]].

**Bounded transport-derivation attempt (2026-07-11, negative — do not re-run blind;
`archive/codigo/investigacion/open_problems/op9_transport_derivation.py`).** A pre-committed
attempt to derive $\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V$ as the *output* of the
$\mathrm{KAL}_0$-governed dissipative transport (cutoff: simple fraction + residue $<0.5\%$,
no circular re-parametrization). Result: the only exact rewrite found,
$\mathrm{SOLAR}=(\varphi+4\,\mathrm{KAL}_0)/3$, is a **trivial algebraic restatement** of the
natural form $\mathrm{SOLAR}=\mathrm{BIAL}+\mathrm{KAL}_0=\varphi+2\pi$: substituting
$\pi=(2\mathrm{KAL}_0-\varphi)/3$ turns the $2\pi$ into $4\mathrm{KAL}_0/3$, so the factor
$4=2\times2$ is a **substitution artifact with no physical content** — it carries no
transport meaning and **fails the cutoff** (re-parametrization, not derivation). The natural
two-term form $\mathrm{BIAL}+\mathrm{KAL}_0$ (radiative seed $+$ bulk viscosity) is the
honest statement; no cleaner one exists.
Simple-fraction probes against transport combinations ($\mathrm{KAL}_0^3$, etc.) returned
only coincidental hits (24/11, 11/2), excluded by the anti-numerology lock (small residue
$\wedge$ *simple* fraction, both required). **Verdict:** the $g^2v$ form remains the ceiling
of what is derivable without solving the full $V(\phi)$; residue (ii) is genuinely OP-10-level,
not a shortcut away. This confirms — does not weaken — the honest status above.

**Strong rule (still in effect):** the physical Hubble scale
$H_0^{\rm MIRA}=67.068$~km/s/Mpc **must NOT be substituted** into any mass formula. <!-- R74: git:71598acba2:results/planck_cobaya_unified.txt -->
The canonical chain uses the mass scale $\omega_b C_\nu/(\tau_\Pi H_0)$ (canonical form, `CANONICAL_VALUES.yaml`) and pure $(\varphi,\pi)$
numbers only — no Hubble rate enters. The dimensionally-inconsistent
"$\times H_0^{\rm alg}$" framing of the old 5.602 eV ansatz is retired. <!-- R74: git:85e680ef29:results/logs/cmb_dbic_tau_ajustado.json -->

**Canonical CLASS verification (zero fitting, SOLAR²·KRYSTOS_V adopted 2026-06-19):** the
forward-predicted particle ($m_\phi=40.70$ eV, $\Omega_{\phi{\rm DM}}=0.14889$) yields <!-- R74: git:f3b01e5c2d:CANONICAL_VALUES.yaml -->
$\sigma_8^{\rm eff} = 0.747$, $S_8 = 0.758$ ($0.04\sigma$ KiDS-1000 $0.759\pm0.024$ —
**resolves** the lensing tension), single-sector ceiling $S_8=0.827$ ($2.7\sigma$, "the
challenge"). $\sigma_8$ is a **direct CLASS output** (top-hat on the two-sector $P(k)$),
not the retired $\alpha_{\rm WDM}$ fit; the Viel $\alpha = 1.108$ Mpc/h is a CLASS
diagnostic output. log (archivado 2026-10-03): `archive/codigo/investigacion/particula_RETIRADA_2026-08-01/logs/p6_class_reframe_omega_m.log`.

**Falsifiable anchor:** $k_{\rm fs} = 0.754\,h/$Mpc (analytic; CLASS-measured half-mode
$k_{1/2} = 0.339\,h/$Mpc), set by $m_\phi = 40.70$ eV (SOLAR²·KRYSTOS_V; the prediction
*updates* with the particle — was 0.798 at 42.47, 0.659 at the old 36.95 eV). The whole chain is forward:
$\Sigma m_\nu=0.069$ eV is itself a prediction ($\mathcal{R}_2$), comfortably allowed in
the dynamical-DE background (the tight DESI $\Sigma m_\nu\lesssim0.064$–$0.072$ eV bound
is $\Lambda$CDM-specific; with $w_0,w_a$ free it relaxes to $\sim0.13$–$0.16$ eV). If
DESI Y3/Euclid disconfirms $k_{\rm fs}$, the particle dies cleanly.

**Path to full resolution:** Derive the unified $V(\phi)$ (OP-10) such that
$m_\phi^2 = V''(\phi_{\rm min})$ reproduces the multiplier $\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V=594.28$
($g^2v$ form: coupling$^2\cdot$scale) as the curvature of the potential at its minimum,
built from structural scales at the eV scale.

**Severity:** Medium — downgraded from Medium-High. The dimensional contradiction is
resolved (pure-number multiplier + written Lagrangian, dimensionally consistent); what
remains is the *derivation* of the multiplier from first principles, which is
incompleteness on the natural OP-10 path.

**Search file:** `archive/codigo/investigacion/open_problems/op9_phi_dm_formula_search.py` — historical inventory of mass
combinations (now superseded by the canonical Vía-2 chain).

---

</details>

## OP-10 — Unification of φ and χ into a Single Field — ⚫ CERRADO POR DISOLUCIÓN (2026-08-01)

> 🔴 **CERRADO POR DISOLUCIÓN — 2026-08-01.** El objeto del que trataba este OP
> ya no existe: el sector φ-DM y su partícula fueron **retirados** en el Paper 6,
> por dos razones independientes.
> **(1)** Su densidad se definía como Ω_φDM = Ω_m,CMB − Ω_m,dyn = 0.308881 − 0.160,
> restando una densidad medida menos un número de la **ecuación de estado**
> (0.160 = 1+w₀). La resta está bien formada aritméticamente y vacía de física
> ⟹ la partícula no tenía de qué estar hecha.
> **(2)** La tensión S₈ que motivaba todo el sector no existe en el dato crudo:
> con un solo sector y A_s libre, el MCMC contra los 225 puntos de ξ± de
> KiDS-1000 da **S₈ = 0.7559 ± 0.0189 → 0.10σ**.
>
> **No está resuelto: dejó de ser una pregunta.** Se conserva lo de abajo como
> registro de qué se preguntaba y por qué. **No citar como abierto.**
>
> **Lección durable:** la falsabilidad es requisito mínimo para que una hipótesis
> sea científica, **no evidencia de que la entidad exista**. Y una cadena puede
> ser dimensionalmente impecable y aun así no significar nada.


<details><summary>Registro histórico (la pregunta tal como estaba planteada)</summary>


**Location:** Paper 6 introduces χ (the DM scalar) as **distinct** from Paper 7's φ
(the DE k-essence scalar). L394-395: "We model φ-dark matter as a single real scalar
field $\chi$ (distinct from the SSEE background k-essence scalar $\phi$ of Paper 7)."

**Problem:** This historically arose post-hoc as a fix for the fσ8 tension in Paper 5.
The current potential $V(\phi) = V_0 \exp(-\alpha\phi)$ of Paper 7 has **no minimum**,
so the same field cannot also produce matter-mode oscillations. Hence χ was
introduced as a separate species with its own mass term.

**Consequence:** The "single field" philosophical claim of SSEE (one φ, derived from
$\varphi,\pi$) is technically violated — there are two cosmological scalar fields.
Both have parameters constrained by $(\varphi,\pi)$ but they are not the same entity.

**Path to resolution:** Find a potential $V(\phi)$ with:
- A slow-roll region (produces DE behavior at low energy)
- A stable minimum (produces matter-mode oscillation, hence DM)
- Both regions parametrized by $\varphi,\pi$ only

If such a $V(\phi)$ exists, χ becomes the matter-phase of φ itself, m_φ emerges as
the curvature at the minimum (resolving OP-9), and the "zero free parameters"
philosophy is restored.

**Severity:** Medium-High — does not affect observational predictions of SSEE-V3.6
but is the natural next step toward genuine zero-parameter status.

### Registro de rutas exploradas (actualizado 2026-06-11)

Protocolo en todas las fases: **forward, cero fiteo** — solo escalas ya bloqueadas
por Papers 6/7/10 (V₀ = 0.840 ρ_crit, λ = √(3·0.160) ≈ 0.693, M_UV = 9.68 meV,
m_φ = 40.70 eV). Requisitos declarados ANTES de calcular. Scripts en
`archive/codigo/investigacion/open_problems/`.

| Ruta | Mecanismo | Veredicto | Causa del descarte |
|---|---|---|---|
| F1 (pozo local) | mínimo cuadrático añadido al exponencial | ❌ | el pozo contamina el plateau DE — w₀ se aleja de −0.840 |
| F2 (tanh²) | doble-escala suave | ❌ | jerarquía DE/DM exige 33 órdenes de magnitud en el parámetro de forma |
| F3 (axion-like) | V₀e^(−λφ) + M_UV⁴[1−cos(φ/f)] | ❌ | atrapamiento topológico: si el axion engancha, φ se fija → w = −1; si no engancha, m_φ ≈ H₀ ≠ 40.70 eV — masa **RETIRADA 2026-08-01**, la fila se conserva como historia de la búsqueda (`ssee_op10_family3_axion.py`) |
| F4 (see-saw escalas) | m_φ² = m_h·m_l con escalas SSEE | ❌ | predicción off por ~10³³ (`ssee_op10_seesaw_search.py`) |
| Opción A (UV-inducido) | corrección de loop de K(X) genera el mínimo | ❌ | K(X) es φ-independiente a nivel árbol; curvatura de loop ~ M = 9.68 meV, factor ~4 238 bajo m_φ (`ssee_op10_uv_induced_minimum.py`) |
| 2c (K-essence boost) | K_X renormaliza la masa efectiva | ❌ analítico | K_X ≥ 1/KAL acota el boost a √KAL ≈ 2.35× — insuficiente para 10³⁻⁴ |
| 2e (masa tracking) | m_eff²(z) = ρ_m(z)/M_*², M_* = M_UV | ❌ estructural | ver R1–R3 abajo (`ssee_op10_phase2e_dynamic_mass.py`) |

**Fase 2e en detalle** (cerrada 2026-06-10; idea sobreviviente de la propuesta
"conversión DM→DE" de Mike): masa inducida por densidad ambiente, chameleon-like,
con la única escala bloqueada M_* = M_UV. Hallazgo sugestivo: el cruce
m_eff = 40.70 eV cae en z_x ≈ 2 370, época de igualdad materia-radiación
(z_x/z_eq ≈ 0.70) sin ajustar nada. Pero falla los tres requisitos pre-declarados:

- **R1 (estructural, independiente de M_*):** con m ∝ √ρ_m ∝ a^(−3/2) y el
  invariante adiabático n ∝ a⁻³, la energía oscilante diluye como
  ρ_osc = m·n ∝ a^(−4.5) → w_eff = +0.5: se evapora más rápido que la radiación,
  no es CDM para NINGÚN M_*.
- **R2:** m_eff(0) = 0.355 meV, factor ~10⁵ bajo el canónico 40.70 eV (rompe
  k_fs = 0.754 h/Mpc de Paper 6).
- **R3:** m_eff(0)/H₀ ~ 10²⁹ — el campo queda clavado hoy → w = −1, no −0.840.
- Rescate M_* = 92.4 neV sería escala nueva fiteada (prohibido) y R1 persiste.

### Teorema del escalón (lección estructural consolidada, 2026-06-10)

Los 7 descartes consolidan un patrón: **ni un pozo estático ni una masa que
trackea ρ_m de forma continua pueden unificar DE+DM en un solo campo SSEE.**
R1 lo prohíbe estructuralmente: mientras la masa cambie durante las oscilaciones,
la energía no diluye como materia.

⇒ La transición DM↔DE, si existe en un solo campo, tiene que ser un **escalón**
(transición de fase única): el potencial cambia de forma UNA sola vez cerca de
z_eq, con masa constante = 40.70 eV en la fase oscilante. El escenario
escalón + masa constante ES el misalignment frío ya estudiado (cierre Osiris
2026-05-30): viable como DM, pero φ_i ~ 10⁻⁶ M_Pl no sale algebraico de
(φ,π) → empata ΛCDM en conteo de parámetros, no lo supera.

**Única ruta no excluida:** transición de fase única cerca de z_eq cuyo
DISPARADOR esté bloqueado por (φ,π). Sin candidato a la fecha.

---

</details>

## OP-11 — Free Non-Minimal Coupling ξ — ⚫ CERRADO POR DISOLUCIÓN (2026-08-01)

> 🔴 **CERRADO POR DISOLUCIÓN — 2026-08-01.** El objeto del que trataba este OP
> ya no existe: el sector φ-DM y su partícula fueron **retirados** en el Paper 6,
> por dos razones independientes.
> **(1)** Su densidad se definía como Ω_φDM = Ω_m,CMB − Ω_m,dyn = 0.308881 − 0.160,
> restando una densidad medida menos un número de la **ecuación de estado**
> (0.160 = 1+w₀). La resta está bien formada aritméticamente y vacía de física
> ⟹ la partícula no tenía de qué estar hecha.
> **(2)** La tensión S₈ que motivaba todo el sector no existe en el dato crudo:
> con un solo sector y A_s libre, el MCMC contra los 225 puntos de ξ± de
> KiDS-1000 da **S₈ = 0.7559 ± 0.0189 → 0.10σ**.
>
> **No está resuelto: dejó de ser una pregunta.** Se conserva lo de abajo como
> registro de qué se preguntaba y por qué. **No citar como abierto.**
>
> **Lección durable:** la falsabilidad es requisito mínimo para que una hipótesis
> sea científica, **no evidencia de que la entidad exista**. Y una cadena puede
> ser dimensionalmente impecable y aun así no significar nada.


<details><summary>Registro histórico (la pregunta tal como estaba planteada)</summary>


**Location:** Paper 6, Eq.~\eqref{eq:phiDM_lagrangian}, L406-407.

**Problem:** The action of χ contains a non-minimal coupling $\xi R \chi^2/2$ where ξ
is **explicitly a free continuous parameter** (P6 L416-417: "no free continuous
parameter other than ξ"). No algebraic constraint from $(\varphi,\pi)$ is provided
to fix ξ.

**Current status:** ξ is treated as a free parameter, partially constrained by the
production mechanism (gravitational particle production, OP-12).

**Path to resolution:** Either derive ξ from the underlying field theory (e.g., a
conformal symmetry requirement giving $\xi=1/6$, or a specific algebraic value), or
absorb χ into φ (OP-10) so that ξ becomes a structural piece of $V(\phi)$ rather
than a free input.

**Severity:** Medium — contributes one free parameter to the current model count.

---

</details>

## OP-12 — Origen físico de T_φ y de Ω_φ-DM h² — ⚫ CERRADO POR DISOLUCIÓN (2026-08-01)

> 🔴 **CERRADO POR DISOLUCIÓN — 2026-08-01.** El objeto del que trataba este OP
> ya no existe: el sector φ-DM y su partícula fueron **retirados** en el Paper 6,
> por dos razones independientes.
> **(1)** Su densidad se definía como Ω_φDM = Ω_m,CMB − Ω_m,dyn = 0.308881 − 0.160,
> restando una densidad medida menos un número de la **ecuación de estado**
> (0.160 = 1+w₀). La resta está bien formada aritméticamente y vacía de física
> ⟹ la partícula no tenía de qué estar hecha.
> **(2)** La tensión S₈ que motivaba todo el sector no existe en el dato crudo:
> con un solo sector y A_s libre, el MCMC contra los 225 puntos de ξ± de
> KiDS-1000 da **S₈ = 0.7559 ± 0.0189 → 0.10σ**.
>
> **No está resuelto: dejó de ser una pregunta.** Se conserva lo de abajo como
> registro de qué se preguntaba y por qué. **No citar como abierto.**
>
> **Lección durable:** la falsabilidad es requisito mínimo para que una hipótesis
> sea científica, **no evidencia de que la entidad exista**. Y una cadena puede
> ser dimensionalmente impecable y aun así no significar nada.


<details><summary>Registro histórico (la pregunta tal como estaba planteada)</summary>


**Location:** Paper 6, §4.2; pipeline CLASS `archive/codigo/p06_phiDM_RETIRADO_2026-08-01/ssee_paper6_canonical_particle.py`.

**Problem (actualizado):** la partícula canónica φ-DM ($m_\phi=\mathrm{SOLAR}^2\cdot
\mathrm{KRYSTOS}_V\cdot\Sigma m_\nu=40.70$ eV; antes 36.95) entra en CLASS como especie
**térmica** (ncdm) con temperatura $T_\phi$. Pero hoy $T_\phi$ se **despeja** de la
fórmula del relic usando $m_\phi$ y $\Omega_{\phi DM}$:
$$T_\phi = T_\nu\left(\Omega_{\phi DM}h^2\cdot 93.14/m_\phi\right)^{1/3}=0.5385\,T_\nu.$$ <!-- R74: git:d7446ace8a:results/logs/p6_class_reframe_omega_m.log -->
Es **bookkeeping** (densidad = número × peso), no una temperatura derivada de física.
Verificado en CLASS: con $(m_\phi,T_\phi)$ el Boltzmann completo reproduce
$\Omega_{\phi DM}=0.14889$ ($\Omega h^2=\Omega_{\phi DM}h^2$) a 5 cifras — el lazo cierra, pero <!-- R74: git:f3b01e5c2d:CANONICAL_VALUES.yaml -->
porque se construyó así. $m_\phi$ descansa en una sola pata (SOLAR²·KRYSTOS_V, OP-9).

**Bifurcación (cold vs thermal) — y una inconsistencia interna a corregir:** el texto
de P6 asume la rama **FRÍA** (producción gravitacional Parker-Kolb-Riotto, "escalar
libre, sin portal SM, invisible"), mientras el **pipeline CLASS trata φ como TÉRMICO**
(ncdm a $T_\phi$). No pueden ser ambas: un campo frío no tiene distribución térmica.
Esto hay que unificarlo.

- **Rama fría** (misalignment / producción gravitacional): consistente con "sin portal",
  pero entonces $(T_\phi/T_\nu)^3$ es ficción de bookkeeping y la 2ª pata de $m_\phi$
  debe venir del potencial $V''(\phi_{\min})$ (ruta OP-10), no del freeze-out.
- **Rama térmica** (freeze-out): $T_\phi$ es una temperatura real → el tratamiento
  ncdm de CLASS es consistente, y el freeze-out **podría derivar $T_\phi$** y cerrar
  $m_\phi$ por una 2ª vía independiente de SOLAR²·KRYSTOS_V. Requiere un **portal**.

**Insight (Mike, 2026-06-20):** el portal de la rama térmica **NO es nuevo** — es la
**viscosidad** que ya está en el modelo ($\mathrm{KAL}_0$, $\tilde\zeta=\mathrm{KAL}_0/3$,
Paper 5 IS). Disipación = interacción con un baño; un escalar libre no tiene viscosidad.
$\mathrm{SOLAR}=\mathrm{BIAL}+\mathrm{KAL}$ hereda el rol **radiativo-disipativo** →
señala que el baño es la **radiación**. Esto empuja hacia la rama térmica y **revisa**
el "sin portal SM" (φ pasaría a ser débilmente acoplado, casi invisible pero no nulo).

**Paso 1 — VIABILIDAD (✅ hecho, `archive/codigo/investigacion/open_problems/op12_thermal_decoupling.py`):** si φ
es relic térmico, la dilución de entropía $(T_\phi/T_\nu)^3=10.75/g_{*s}(T_{\rm dec})$
exige $g_{*s}\approx 68.8 \Rightarrow T_{\rm dec}\approx 217$ MeV — **justo la transición
QCD**. Época física, no absurda: la rama térmica es **viable y falsable** (predice
*cuándo* se desenchufa φ). Coincidencia a vigilar (no afirmar): $g_{*s}=68.8$ vs
$H_{\rm alg}=3\Omega^2=67.96$.

**Naturaleza del relic (auto-consistencia):** a $T_{\rm dec}=217$ MeV, $m_\phi/T_{\rm
dec}\sim2\times10^{-7}\ll1$ → φ desacopla **ultra-relativista** (relic **caliente**,
como el ν). Esto **justifica** la fórmula de dilución $(T_\phi/T_\nu)^3$ (solo vale si
desacopla relativista) → el "bookkeeping" no es arbitrario. φ se vuelve no-relativista
en $z\approx4.5\times10^5$ (mucho antes del CMB) → DM **templada** en recombinación,
encajando con el tratamiento WDM/$k_{\rm fs}$ que P6 ya usa. La rama térmica se
**enchufa** a la física existente, no la contradice.

**Pasos 2–3 (abiertos):** (2) mostrar que la viscosidad KAL es el portal y fijar su
estructura/escala $\Lambda$; (3) freeze-out forward → ¿da $T_\phi/T_\nu=0.5385$? Si sí, <!-- R74: git:d7446ace8a:results/logs/p6_class_reframe_omega_m.log -->
2ª pata de $m_\phi$. **Obstáculo honesto:** $\mathrm{SOLAR}\approx 7.9$ no es un
acoplamiento perturbativo ($g>1$) → el portal es casi seguro suprimido por escala
(operador dim$>4$); el desconocido real pasa a ser la escala $\Lambda$ del portal.

**Paso 2 — dos rutas exploradas 2026-06-21 (scripts `op12_route2_freezeout.py`):**
- **Ruta 2 (cross-section, número duro):** freeze-out a 217 MeV exige $\sigma\approx
  6\times10^{-19}$ GeV$^{-2}$ → portal **dim-4** $g\sim3\times10^{-5}$ (débil) o **dim-5**
  $\Lambda\sim8.8$ TeV. **HALLAZGO (correctness burden):** el portal **NO es SOLAR**
  ($g_{\rm portal}\sim10^{-5}$ vs SOLAR$\sim$7.9, ~5 órdenes). **La masa (SOLAR, g²v) y el
  portal son acoplamientos DISTINTOS** — la idea "mismo SOLAR hace masa Y portal" no
  cierra. Coherencia: acoplamiento débil $\Leftrightarrow$ viscosidad alta (signo del
  Bridge 2) → portal débil es consistente con KAL grande.
- **Ruta 1 (linaje, "cuándo"):** el desacople cae en la transición QCD (217 MeV) porque
  un portal al **sector QCD** (quarks/gluones) se apaga al **confinarse** los quarks
  (~200 MeV) → el confinamiento es el **gatillo físico** (no perilla). El plasma
  quark-gluón es el medio viscoso por excelencia ↔ KAL=viscosidad. **Rima, no deriva**
  (emparejamiento de roles SOLAR=BIAL+KAL = térmico+viscoso ↔ QGP).
- **Convergencia:** portal débil al plasma QCD viscoso, desacople = confinamiento; KAL
  es la huella macroscópica.
- **$\Lambda\sim8.8$ TeV NO es blanco a derivar (disuelto 2026-06-21, regla dimensional
  de Mike):** la condición de freeze-out lo FIJA, $\Lambda=[O(1)\cdot M_{\rm Pl}\cdot
  T_{\rm dec}^3]^{1/4}$ — anclado a $M_{\rm Pl}$ (gravedad) y $T_{\rm dec}$ (escala QCD),
  ambas físicas. No hay número que sacar de $\varphi,\pi$; es la "sombra" de QCD+gravedad.
  La pregunta real se afila a: **¿el linaje de SOLAR pone a φ en el sector QCD?** (Ruta 1).
- **2ª pata de $m_\phi$ (consistente, no cerrada):** si φ↔QCD, confinamiento $\to g_{*s}
  \to T_\phi \to m_\phi$ (con $\Omega_{\phi DM}$), SIN SOLAR²·KRYSTOS_V. Coincide con 41 eV
  **solo si el desacople se completa en la cima del confinamiento** ($g_{*s}=69$, 217 MeV);
  más abajo baja hasta ~12 eV. Dos rutas independientes (linaje=41, térmica-en-onset=41)
  riman → alentador, PERO sub-asunción (punto de desacople) + Ruta 1 es rima no derivación.
  **Promesa, no prueba.** Scripts: `op12_thermal_decoupling.py`, `op12_route2_freezeout.py`.
- **Paso 2 INTENTADO 2026-06-21 (`op12_trace_lights_qcd.py`) — resultado NEGATIVo honesto:**
  el término candidato $\mathcal L=(\varphi/\Lambda)T^\mu_\mu$ (acoplo a la traza, fuente de
  KAL). (a) La interaction measure $(1-3w)$ SÍ pica en QCD (~190 MeV) ✓. PERO (b) en
  $\Gamma/H\propto I^2 T^3 M_{\rm Pl}/\Lambda^2$ el factor $T^3$ domina → el bulto de QCD
  es solo ~4% del máximo → **el desacople NO se ancla en QCD** (ocurre en alta T, fijado
  por Λ). **La historia "φ se desacopla en QCD gratis por la traza" NO sobrevive el
  cálculo** — caer en QCD exigiría ajustar Λ~8.8 TeV a mano (no derivado). El gatillo de
  confinamiento queda DEBILITADO. **Saldo:** la rama térmica NO cierra elegante; $m_\phi$=41
  sigue en 1 pata (SOLAR²·KRYSTOS_V). 2ª pata regresa a $V''(\phi_{\min})$/OP-10 (rama fría) o
  admitir Λ sin explicar. (Corrige una narrativa previa optimista; el cálculo mandó.)

**Path to resolution:** elegir rama (la viscosidad ya presente favorece la térmica) y
o bien (térmica) cerrar Pasos 2–3, o bien (fría) derivar $\Omega_{\phi DM}h^2$ del
$V(\phi)$ unificado (OP-10) sin tuning. Ligado a OP-10/OP-11.

**Severity:** Medium — el relic match es algebraico; cualquiera de las dos ramas, bien
cerrada, lo vuelve dinámico. La inconsistencia cold/thermal del pipeline es **a
corregir sí o sí** (independiente de qué rama gane).

---

</details>

## OP-13 — Inconsistencia interna Paper 8: §3-4 (factor √AURA) vs §4.5 (B-S) — ✅ RESUELTO 2026-05-23 (Opción A)

**Location:** Paper 8, §3-4 ("Disformal null geodesic" + "MIRA emerges in lensing") vs
§4.5 ("EFT suppression of fifth-force corrections") vs §6.2 item 3 (falsifiability).

**Diagnóstico (revisión 2026-05-23):**

P8 contiene dos derivaciones que asumen físicas incompatibles:

| Sección | Asunción física | Predicción |
|---|---|---|
| §3-4 | "DM efectiva sourced enteramente por baryonic seed" (escenario MOND-like, sin DM real) | $\theta_E^{\rm SSEE}/\theta_E^{\rm GR-bary} = \sqrt{\beta_c} \approx 2$ |
| §4.5 | DM real existe (Ω_CDM=0.16 + Ω_φDM=0.16), EFT con α_B=α_M=α_T=0 | $F_\phi/F_N \sim (H/k)^2 \sim 10^{-15}$ a escala kpc |
| §6.2 item 3 | (saca de §3-4) | $M_{\rm dyn}/M_{\rm lens} \approx 4$ |

**El propio paper admite** (P8 L363-370) que §3-4 es "working phenomenological estimate"
y difiere "full solution to future N-body simulations". Sin embargo §6.2 item 3 lo
presenta como predicción rígida falsable.

**Datos confrontados (revisión literatura 2026-05-23):**
- SLACS γ = 2.078 ± 0.027 (Auger 2010; Sonnenfeld 2015)
- M_E/M_dyn ≈ 1.207 (SIS, Cao et al. 2018, arXiv:1803.00819) — i.e., M_lens excede M_dyn ~20%
- Power-law profiles: M_E/M_dyn within 1σ de 1
- NO desviaciones factor 2 ni factor 4 reportadas en ningún sample

**Confrontación:**
- §3-4 predice $M_{\rm dyn}/M_{\rm lens}\approx 4$ → datos dan ≈ 0.83 (factor 5 wrong direction)
- §4.5 predice $M_{\rm dyn}/M_{\rm lens}\approx 1$ → datos compatibles (offset ~20% atribuible
  a contaminación línea-de-vista y errores de modelo)

**Veredicto:**
1. La física correcta para el modelo real (entonces two-sector con DM existente; el
   segundo sector se retiró el 2026-08-01 y §4.5 quedó sobre un solo sector) es §4.5
2. §3-4 describe un escenario MOND-like que NO corresponde al modelo SSEE canónico
3. La identidad "$\sqrt{\beta_c}\approx$ MIRA al 0.03%" es una near-coincidence
   numérica entre dos cantidades de regímenes incompatibles, no derivación física

**Implicaciones cross-paper:**
- P8 título/abstract: "MIRA emerges in lensing" pierde fuerza si §3-4 no es la física canónica
- P1 §1.4 / P8 introducción: la "unificación CMB↔lensing via MIRA" descansa en
  near-coincidence numérica, no en identidad estructural
- P6 y P7: no afectados directamente (no usan factor √β_c en lensing)

**Path to resolution:**
1. **Opción A (defensiva)**: Reformular P8 §3-4 como "alternative limit scenario", marcar
   §4.5 como predicción canónica. §6.2 item 3 ajustado a $M_{\rm dyn}/M_{\rm lens}\approx 1$
   (consistente con datos). Reescribir narrativa MIRA↔lensing como "near-coincidence
   numérica" en lugar de "emergencia estructural".
2. **Opción B (constructiva)**: Derivar consistentemente el lensing en el escenario
   two-sector real (retirado 2026-08-01; con DM existente + EFT B-S), determinar si hay alguna firma
   observable distinta de ΛCDM, reformular P8 alrededor de eso.
3. **Opción C (radical)**: Aceptar que P8 §3-4 fue overclaim y reescribir el paper
   sin la afirmación factor 2.

**Severity:** **High** — afecta la narrativa central de P8 ("MIRA emerges in lensing")
y la cadena de argumentos de unificación. NO afecta la solidez del background
SSEE (Papers 1-5, 7, 9, 10), solo el régimen de gravedad fuerte (Paper 8).

**Cómo este OP escapó de la auditoría previa:** la auditoría hostil chequeó consistencia
**dentro** de cada sección y entre paper↔scripts↔ssee_core, pero no consistencia
**entre secciones del mismo paper** ni paper↔datos publicados. Patch metodológico:
añadir Capa 8 "consistencia inter-sección" al guardián.

---

### Resolución aplicada (Opción A — 2026-05-23)

**Insight clave (correctión de terminología señalada por Mike):** el factor
derivado en P8 §3-4 NO es $\MIRA$ — es $\sqrt{\AURA}$. Son dos operaciones
algebraicas distintas sobre $\AURA$ (división por 2 vs raíz cuadrada). Coinciden
numéricamente al 0.03% porque $\AURA\approx 4$ hace que ambas rondan 2. Drafts
previos de P8 conflated los dos bajo la etiqueta "$\MIRA$ emerges in lensing";
esa identificación se retira.

**Cambios aplicados (commit de la sesión):**

1. **P8 abstract reescrito**: framing "dos límites" explícito (alternative MOND-like
   vs canonical two-sector —éste retirado 2026-08-01—); $\sqrt{\AURA}$ en lugar de "√β_c ≈ MIRA"; canonical
   limit prediction declarada como $\thetaE^{\rm SSEE}\approx\thetaE^{\rm GR-with-DM}$.

2. **P8 §1 (Introduction) reescrito**: dos limits identificados explícitamente;
   $\MIRA$ aparece estructuralmente solo en CMB y LSS, no en lensing; aclaración
   $\sqrt{\AURA}\neq\MIRA$ algebraicamente.

3. **P8 §3-4 (Disformal geodesic)** ahora titulado "Alternative MOND-like limit";
   tcolorbox al inicio aclarando scope; sección retenida como pedagógica/histórica,
   no canónica.

4. **P8 §5 (formerly "MIRA emerges in lensing")** re-titulado "Lensing factor
   $\sqrt{\AURA}$ in the Alternative Limit (and Its Numerical Near-Coincidence with
   $\MIRA$)"; tcolorbox naming clarification explícito al inicio.

5. **P8 §6.2 items 2 y 3 (Falsifiable predictions)** reformulados a predicción
   canónica: $\thetaE^{\rm SSEE}\approx\thetaE^{\rm GR-with-DM}$ y
   $M_{\rm dyn}/M_{\rm lens}\approx 1$, consistente con SLACS/BELLS observados
   ($\gamma=2.078\pm 0.027$; $M_E/M_{\rm dyn}\approx 1.21$ SIS). Footnote retira
   explícitamente la predicción "$\sim 30\%$ deficit" previa.

6. **P8 §8.1 (Discussion)** reescrita: $\MIRA$ aparece exactly en 2 sectores
   (no 3); la aparición en lensing era name-conflation de $\sqrt{\AURA}$ con
   $\MIRA$ vía near-coincidence numérica, retirada en esta versión.

7. **Unified Journal §2 + tabla predicciones**: framing dos-límites; entry de
   lensing marcado como "Conditional prediction (not canonical; OP-13)".

8. **Endorser Summary §IV (Paper 8 bullet)**: framing dos-límites; SLACS/BELLS
   citado como evidencia del canonical limit.

**PDFs regenerados:** P8 (18 pp, +1), Unified (21 pp), Endorser (2 pp).
Guardián: VERDE 102/102.

**Estado del modelo tras resolución:**
- $\MIRA$ aparece exactly en 2 sectores estructurales: CMB horizon mapping
  (Paper 3) y two-sector mass ratio (Paper 6, retirado 2026-08-01 con el segundo
  sector). Ambos: $\MIRA=\AURA/2$ exacto.
- $\sqrt{\AURA}$ aparece en lensing alternative-limit (P8 §3-4) — preservado como
  derivación válida pero marcado explícitamente como no canónico.
- Canonical SSEE lensing prediction: $\thetaE^{\rm SSEE}\approx\thetaE^{\rm GR-with-DM}$
  (de EFT B-S structure P8 §4.5), consistente con datos SLACS/BELLS.
- La "unificación CMB↔DM↔lensing via $\MIRA$" se degrada a "unificación CMB↔DM
  via $\MIRA$ exacta; lensing es near-coincidence numérica con $\sqrt{\AURA}$".

**Lo que NO cambia:**
- Postulado M ($\MIRA=(3\phiG+\pi)/4$) sigue siendo central del framework.
- Papers 1-7, 9, 10 no afectados.
- EFT canonical (P7), Hubble tension (P9), UV completion (P10): intactos.

**Lo que cambia (honesto):**
- P8 ya no es "MIRA-in-lensing paper" sino "two-limit analysis paper": el factor
  $\sqrt{\AURA}$ del alternative MOND-like limit es preservado como derivación
  pedagógica; la predicción canónica observable es GR-with-DM.
- El claim "MIRA aparece en 3 sectores" se retira de la narrativa cross-paper.

---

## OP-14 — Σm_ν Phenomenological Derivation (Paper 4) — ✅ RESUELTO (2026-06-04)

**Location:** Paper 4, §"Neutrino Mass Sum", L675-700.

**Fórmula canónica (resuelta):**
$$\Sigma m_\nu^{\rm active} = \mathcal{R}_2\,\omega_b C_\nu/(\tau_\Pi H_0) = 0.0685~\mathrm{eV},
\qquad \mathcal{R}_2 = \frac{\Omega_{\rm DNAV}}{\mathrm{KAL}\cdot\mathrm{TRIAL}}
= \frac{4.7596}{5.5214 \times 11.9935} = 0.07188.$$

El cociente $\mathcal{R}_2$ es un número puro de $(\varphi,\pi)$: $\Omega_{\rm DNAV}=\pi+\varphi$,
$\mathrm{KAL}=(\pi+\varphi)/2+\pi$, $\mathrm{TRIAL}=3(\varphi+(\pi+\varphi)/2)$. No hay
sustracción de enteros, no hay offset 22.

**Por qué esto resuelve el problema:**

1. **El offset 22 queda eliminado.** La forma anterior $\mathcal{R}=4\cdot\mathrm{KAL}-22=0.0856$
   era una diferencia entre números casi iguales (22.086 vs 22.000) y se ajustaba para
   reproducir la cota cosmológica. La forma canónica $\mathcal{R}_2=\Omega_{\rm DNAV}/(\mathrm{KAL}\cdot\mathrm{TRIAL})$
   es un cociente limpio de constantes estructurales — sin parámetro ajustado.
2. **Σm_ν asciende de Type P → Type A (algebraico).** El único input externo que queda es
   $\omega_b C_\nu/(\tau_\Pi H_0)$ eV (forma canónica de `CANONICAL_VALUES.yaml`; constante de normalización fija del Modelo Estándar relíquica↔masa), igual
   que cualquier predicción dimensional de SSEE usa una escala física fija.

> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7559 ± 0.0189` (0.10σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.04σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
**Cascada (retirada 2026-08-01):** ~~Σm_ν alimenta a $m_\varphi = \Sigma m_\nu^{\rm active}\,(\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V)=40.70$ eV
en P6 (ver OP-9). Con OP-14 resuelto y OP-9 refinado, la cadena $\varphi,\pi \to \Sigma m_\nu \to m_\varphi$
es forward-prediction sin parámetros libres.~~ La cadena cerraba unidades, pero su destino
—la partícula— no tenía de qué estar hecho. Σm_ν sigue vigente; lo que colgaba de ella, no.

> **Nota histórica (lo de abajo precede a la resolución 2026-06-04).** El registro
> del ataque 2026-05-23 se conserva por honestidad: muestra por qué la forma antigua
> $\mathcal{R}=4\cdot\mathrm{KAL}-22$ era frágil y por qué se descartó en favor del
> cociente limpio $\mathcal{R}_2=\Omega_{\rm DNAV}/(\mathrm{KAL}\cdot\mathrm{TRIAL})$.

### Ataque ejecutado (2026-05-23) — script `archive/codigo/investigacion/open_problems/ssee_op14_neutrino_mass.py`

Tres hipótesis testadas:

**H1 — Fragilidad estructural: CONFIRMADA**

| Perturbación δ(φ,π)/x | Drift en Σm_ν |
|---|---|
| 10⁻⁶ | −0.2% |
| 10⁻⁴ | +2.4% |
| 10⁻³ | **+25.5%** |
| 10⁻² | +257% |

La forma $\mathcal{R} = 4\cdot\text{KAL} - 22$ es una diferencia entre números casi
iguales (22.086 vs 22.000). Pequeñas perturbaciones en (φ,π) se amplifican
relativamente. Una predicción genuinamente estructural debería ser estable bajo
perturbaciones de orden 10⁻³ — esta no lo es.

**H2 — ¿22 = conteo físico de DoF?: SIN MATCH**

- SM tiene 12 generadores gauge (≠22), 28 parámetros libres (≠22), 13 bosones (≠22).
- "22 = 2 × 11 (dim M-theory)" o "22 = 2·rank(E11)" son post-hoc sin argumento físico
  independiente.

**H3 — Scan algebraico (~150 monomios): SIN IDENTIDAD EXACTA**

Mejor candidato: $\mathcal{R} \approx 1/[3(\text{KAL}-\varphi)] = 2/[3(3\pi-\varphi)]$
con error de **−0.27%**. Más limpio que "$4\text{KAL}-22$" pero sigue siendo
aproximación numérica, no identidad. Si fuera estructural el error sería 0%.

### Conclusión: OP-14 colapsa con OP-9 — CONTENIDO HISTÓRICO (m_φ y su multiplicador retirados 2026-08-01)

Reformulación crítica: $\Sigma m_\nu$ y $m_\varphi$ comparten el **mismo grado de
libertad fenomenológico** vía la identidad canónica de Paper 6:
$$m_\varphi = \Sigma m_\nu^{\rm active}\cdot(\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V) = 0.0685\,\text{eV}\times 594.28 = 40.70\ \text{eV}$$

> **Nota (2026-06-14):** la forma previa $m_\varphi=\Sigma m_\nu\cdot H_0^{\rm alg}$
> (que daba 5.602 eV) está **RETIRADA** — era dim-inconsistente (eV × km/s/Mpc). <!-- R74: git:85e680ef29:results/logs/cmb_dbic_tau_ajustado.json -->
> El argumento de abajo NO cambia: $m_\varphi$ sigue construido a partir de
> $\Sigma m_\nu$ (multiplicador adimensional puro), así que comparten el mismo DoF.

OP-14 y OP-9 NO son problemas independientes — son **dos caras del mismo
problema**. Atacar OP-14 directamente no produce derivación porque no hay
ataque local: la única salida es derivar $m_\varphi$ desde la curvatura
de un potencial $V(\varphi)$ fundamental.

### Cadena de dependencias (post-resolución 2026-06-04) — CONTENIDO HISTÓRICO (la rama OP-9/m_φ se retiró 2026-08-01)

```
OP-14  Σm_ν = R₂·ω_b·C_ν/(τ_Π·H₀) = 0.0685 eV    ✅ RESUELTO (R₂=Ω_DNAV/(KAL·TRIAL), sin offset 22)
   │
   └──► OP-9   m_φ = Σm_ν·(SOLAR²·KRYSTOS_V) = 40.70 eV   ✅ refinado: dim-consistente, forward-prediction
           │     (queda abierto SOLO el origen UV del multiplicador 594.28)
           │
           ├──► OP-11  (ξ acoplamiento → funcional de V)        depende de OP-10
           └──► OP-12  (Ω_φDM h² desde dinámica de V)            depende de OP-10

OP-10  V(φ) unificador DE + DM   (daría el origen UV del multiplicador; ya no bloquea Σm_ν ni m_φ)
OP-8   MIRA mecanismo (independiente, eslabón duro)
```

La antigua flecha OP-10→…→OP-14 queda obsoleta: la cadena $\varphi,\pi\to\Sigma m_\nu\to m_\varphi$
ya cierra como predicción algebraica sin V(φ). OP-10 sigue abierto pero su rol es dar el
**origen UV del multiplicador** $\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V=594.28$,
no rescatar la masa.

### Acción sobre Paper 4 (completada 2026-06-04)

El §"Neutrino Mass Sum" se actualiza a la fórmula canónica
$\Sigma m_\nu^{\rm active}=\mathcal{R}_2\,\omega_b C_\nu/(\tau_\Pi H_0)$ $=0.0685$ eV con
$\mathcal{R}_2=\Omega_{\rm DNAV}/(\mathrm{KAL}\cdot\mathrm{TRIAL})$, promoviendo Σm_ν de
**Type P → Type A**. El offset 22 queda eliminado del manuscrito.

---

## OP-15 — Bullet Cluster Offset κ(θ) from KAL(x) Not Computed (Paper 1) — ⚪ CERRADO POR CAMBIO DE PREGUNTA (2026-10-01)

> **Cierre (decisión de Mike, 2026-10-01).** OP-15 preguntaba si un *refuerzo de la gravedad* que sigue a los
> bariones, KAL(x), podía poner la lente del Bala sobre las galaxias y no sobre el gas. Esa pregunta solo existe
> en la lectura MOND. El modelo vigente es relatividad general (α_T=α_M=α_B=0, P7; límite canónico de P8) y KAL₀
> es **retención**: fija cuánta materia oscura fría hay por barión, ω_c = KAL₀·ω_b·n_s. Esa materia no colisiona y
> pasa con las galaxias, que es la explicación estándar del Bala. SSEE **la hereda** porque tiene el mismo
> ingrediente que ΛCDM; no aporta una propia. **No se resolvió gratis: el costo pasa a OP-19** (de qué está hecha
> ω_c). En P1 se retiraron la ecuación μ(x)·KAL(x)≡1 del Principio 3 y la convergencia ponderada por KAL(x).
> Lo de abajo queda como registro histórico.

**Location:** Paper 1, §3.4 (Gravitational Lensing and the Newtonian Limit), L618-629.

**Problem:** The mass-discrepancy result (§3.1-3.3, Table of 4 clusters, χ²_r=0.122) is
solid: the structural amplifier KAL₀ maps the IGIMF baryonic baseline onto the full
Newtonian-equivalent dynamical mass without cold dark matter. **A separate, harder claim
is not yet demonstrated:** that the *environment-dependent* amplifier KAL(x) reproduces
the **spatial offset** between the X-ray gas and the lensing-mass peak in the Bullet
Cluster (1E 0657-56) — the single most-cited evidence for particulate dark matter.

The paper currently states only:
> "SSEE proposes a *qualitative* mechanism for this offset … A quantitative calculation
> of the projected convergence κ(θ⃗) from first principles is deferred to future work."

**Why this matters (audit lesson, 2026-06-14):** this was a *soft* hedge buried in prose,
easy to read as finished. A modified-gravity boost that tracks the baryons must put the
extra gravity where the baryons are; the Bullet's offset (gravity displaced toward the
collisionless galaxies, away from the gas) is precisely the configuration that challenges
any baryon-tracking amplifier. SSEE's proposed escape is that KAL(x) amplifies more in the
compact galactic potential wells than in the diffuse stripped gas — but this is asserted,
not computed.

**Path to resolution:** compute Σ_SSEE(θ⃗) = ∫ ρ_bar^IGIMF · KAL(x) dℓ for the Bullet's
observed gas+galaxy distribution and show the resulting κ(θ⃗) peak lands on the galaxies
(matching Clowe+2006 lensing), not the gas. Falsifiable: if the KAL(x)-weighted convergence
peak coincides with the gas instead, the qualitative mechanism fails.

**Severity:** Medium-High — the Bullet offset is a headline dark-matter argument; leaving it
at "proposed mechanism" is honest but a referee will press on it. Not fatal to the mass
result (OP-15 is about *where* the effective mass sits, not *how much*).

**Relation:** distinct from OP-13 (Paper 8 lensing, RESUELTO). OP-13 established the
canonical θ_E^SSEE ≈ θ_E^GR-with-DM (lensing *amplitude*); OP-15 is the *spatial*
distribution in a merging cluster.

---

## OP-21 — La viscosidad estructural ζ̃ (Paper 5) — 🟡 **REDUCIDO 2026-08-02**: no es un número libre, es un principio de selección

> **Estado tras el ataque del 2026-08-02.** Se abrió como «ζ̃ = KAL₀/3 es una
> hipótesis no derivada». Ya **no es eso**. ζ̃ no tiene libertad: queda
> determinada por dos resultados independientes ya existentes más un principio.
> Lo que queda abierto es el principio, no el número.

### Lo que se estableció

**1. La otra mitad SÍ tenía origen independiente.** `τ_Π H₀ = KAL₀·Ω/T_r`
viene de Paper 4 (tiempo de relajación Israel-Stewart), construida con tres
soberanías, y **no** se eligió para producir estabilidad.

**2. La condición de estabilidad, escrita en la gramática, cancela T_r:**

    ζ̃ = |w₀|·(τ_Π H₀) = (T_r/M_v)·(KAL₀·Ω/T_r) = KAL₀·Ω/M_v

usando `w₀ = −T_r/M_v` (Paper 1). El `T_r` se cancela **siempre**.

**3. ζ̃ y τ_Π son la MISMA construcción con el denominador cambiado:**

| | forma | valor |
|---|---|---|
| τ_Π H₀ | KAL₀·Ω / **T_r** (TRIAL) | 2.191165 |
| ζ̃ | KAL₀·Ω / **M_v** (ATLAS) | 1.840469 |
| razón | T_r/M_v = **Ω_DE** = \|w₀\| | 0.839950 |

El «3» de `KAL₀/3`, que parecía arbitrario, es sólo **M_v = 3Ω**. Escrita como
`KAL₀/3` parece ad hoc; escrita como `KAL₀·Ω/M_v` es una construcción de
linaje, hermana de τ_Π.

**4. La estabilidad marginal es el MÍNIMO, no una elección de gusto.**
`c²_s,bare = w₀ < 0` es inestabilidad de gradiente (fatal). Medido:

| ζ̃ | c²_s,eff | estado |
|---|---|---|
| 1.500000 | −0.155382 | inestable |
| **1.840469** | **+0.000000** | **marginal — el mínimo** |
| 2.200000 | +0.164082 | estable, viscosidad de sobra |

Menos viscosidad rompe la teoría; más sobra sin razón. **«Viscosidad mínima
compatible con estabilidad»** es un principio de selección —como
«acoplamiento mínimo»— y fija ζ̃ **unívocamente**.

### 🔴 HALLAZGO 2026-08-02: la derivación del apéndice pierde un factor (1+w)

Atacando 3.1b («derivar τ_Π del Lagrangiano») se rederivó la relación de
dispersión desde **las propias ecuaciones del Apéndice A de Paper 5**. El
apéndice escribe la ecuación de Euler **correctamente**, con la inercia
relativista igual a la entalpía:

    (ρ̄+p̄)·v̇ + ∇(δp + δΠ) = 0        ← correcto

pero al despejar ω² sustituye esa inercia por ρ:

    ω² = [c²_bare + (ζ/τ_Π·ρ)/(1+(ωτ_Π)⁻²)]k²        ← aquí aparece ρ, no ρ+p

y remata: *«Using the SSEE normalisation ζ = ζ̃ρ_DE H₀ and ρ = ρ_DE»*.
La rederivación simbólica da inequívocamente

    c²_eff = c²_bare + ζ /((ρ+p)·τ_Π),      ρ+p = ρ_DE(1+w₀)

**Consecuencia numérica.** Con la ζ̃ tal como el paper la DEFINE:

| lectura | c²_s,eff | veredicto |
|---|---|---|
| (A) ζ̃ ≡ ζ/(ρ_DE H₀) — *lo que dice el paper* | **+4.408** | **SUPERLUMÍNICO**, viola causalidad |
| (B) ζ̃ ≡ ζ/((ρ_DE+p_DE)H₀) — normalización por entalpía | **+0.000000** | exacto, todo se sostiene |

El cociente entre ambas es exactamente 1/(1+w₀) = 6.248: el factor perdido.

**Resolución propuesta: (B), y no es un rescate.** En hidrodinámica relativista
la inercia de una onda de sonido *es* la entalpía — aparece así en la ecuación
de Euler que el propio apéndice escribe bien, y en el término de presión
1/(1+w) de la ecuación de θ del formalismo estándar de perturbaciones. Definir
ζ̃ por la entalpía es lo que hace que ζ̃/(τ_Π H₀) sea directamente una velocidad
del sonido al cuadrado, sin factores sueltos.

**Lo que hay que corregir:** la *frase* del apéndice y del código
(«ζ̃ = ζ/(ρ_DE H₀)», «ρ = ρ_DE»), **no** el número ni la estructura. Bajo (B),
ζ̃ = KAL₀·Ω/M_v = 1.840469 sigue siendo el valor, la hermandad con τ_Π sigue en
pie, y la ζ física es 0.294567·ρ_DE·H₀ (6.25× menor que la declarada).

**Estado:** ⬜ pendiente de corregir en `SSEE_Paper5_IS.tex` (Ap. A + §Q1) y en
`ssee_paper5_IS_perturbations.py`. **No cambia ningún resultado numérico
publicado**, pero sí lo que significa el símbolo ζ̃.

**Cómo se encontró:** no por el guardián. Rederivando a mano desde las
ecuaciones del propio apéndice, al intentar cerrar 3.1b. Es el mismo patrón que
OP-21 y R47: coherente consigo mismo, y por eso invisible.

### Lo que NO se estableció (honestidad)

- **La forma hermana NO es evidencia independiente.** Es consecuencia
  algebraica de (τ_Π, w₀, estabilidad). Dado esos tres, el resultado **no podía
  ser otro**.
- **Se intentó un test look-elsewhere y se RETIRÓ**: contar «aciertos» sobre un
  valor forzado por identidad es auto-engaño. (Daba 1-de-25 y 1-de-1570; ambos
  sin significado aquí.)
- **Sigue abierto:** derivar `τ_Π H₀ = KAL₀·Ω/T_r` del Lagrangiano, y
  justificar el principio de minimalidad desde primeros principios.

### Consecuencia para los papers

`c²_s = 0` puede llamarse **consecuencia de la minimalidad**, no «hipótesis».
Pero **no** «predicción sin supuestos»: el supuesto es la minimalidad, y hay
que declararlo.

**Severidad:** bajada de Media a **Baja-Media**. No hay número ajustado.

---

<details><summary>Registro histórico (cómo se abrió el 2026-08-02)</summary>


**Cómo se encontró.** Mike preguntó, sobre el resultado `c²_s = 0` de Paper 5:
*«si está ahí tiene su origen y puedes rastrearlo»*. Al rastrearlo apareció que
el 0 es álgebra exacta, pero cuelga de un supuesto que el propio código etiqueta
como tal y que nunca se derivó ni se puso a prueba. Su metáfora, y es literal:
**«una pieza floja en el chasis, y la computadora nunca la marcó como problema».**

**La cadena, en `src/p05_IS/ssee_paper5_IS_perturbations.py`:**

```
τ_Π·H₀  = KAL₀/(3·Ω_DE) ≈ 2.191      ← definido
ζ̃       = KAL₀/3        ≈ 1.8405     ← "SSEE hypothesis"  (línea 62)
ζ̃/(τ_Π·H₀) = Ω_DE = |w₀|
c²_s,eff = w₀ + |w₀| = 0             ← EXACTO, pero condicionado a la hipótesis
```

**Qué falta.** Derivar ζ̃ = KAL₀/3 del Lagrangiano, o mostrar que la
estabilidad marginal (c²_s = 0) la exige — en cuyo caso la hipótesis deja de
serlo y pasa a ser consecuencia. Mientras tanto, `c²_s = 0` es un resultado
**condicional**, no una predicción del modelo.

**Por qué importa ahora.** Es el único ingrediente de SSEE con la *época*
correcta para tocar la veta de A_s (ver `project_as_drift_growth_veta`):
τ_Π·H(a) va de 2.19 hoy a 43821 en recombinación, o sea actúa en la era de
materia, donde ocurre el 86.5% del crecimiento. **Advertencia:** c²_s es la
velocidad del sonido de la ENERGÍA OSCURA, no del crecimiento de materia —
antes de usarlo hay que establecer si el sector IS toca δ_m más allá del fondo
(hoy el efecto medido es 0.3%, sólo vía E(a)).

**Severidad:** Media. No invalida ningún número publicado (el 0 es exacto dado
el supuesto, y está declarado). Sí impide llamar «predicción» a c²_s = 0.

**Contramedida instalada:** regla **R47** del guardián — todo lo que el código
activo etiquete como hypothesis/ansatz debe estar registrado en este documento
o llevar puntero a su derivación. Antes no existía ninguna regla para esta clase
de fallo: no es drift (ningún número está mal) ni incoherencia (todo concuerda
consigo mismo), así que **ausencia de alarma no era ausencia de problema**.

</details>

---
## OP-22 — La forma del ansatz de estado estacionario IS: ¿Π ∝ ρ o Π ∝ (ρ+p)? — ✅ **CERRADO 2026-09-06** (queda OP-22b)

> **Cierre.** Es **Π ∝ (ρ+p)**. El argumento decisivo es un **test de límite,
> independiente de SSEE**: con `w → −1` exacto, `ρ+p → 0`, y una constante
> cosmológica **no tiene grados de libertad de fluido**, así que su presión
> viscosa debe anularse. `Π ∝ (ρ+p)` lo da solo; `Π ∝ ρ_DE` deja presión
> viscosa finita para una constante cosmológica — no es un límite viable.
> *(El argumento ya estaba escrito en `ssee_paper5_IS_perturbations.py`; lo que
> faltaba era correrlo contra las alternativas.)*
>
> **Testigo interno reproducible:** el apéndice de autovalores de Paper 5
> reporta `F = (1−3c²_s) + ζ̃(k/H)² ≈ 186` en `k=10`. La normalización de
> entalpía da **185.05**; la de `ρ_crit` da **1370**, un orden de magnitud
> fuera. Sólo una de las tres lecturas reproduce el número que el paper ya
> tenía impreso.
>
> **Consecuencia:** `c²_s,eff = w₀ + Ω_DE = 0` **es un resultado**, marginal y
> subluminal — no el artefacto que la caja naranja de Paper 5 declaraba el
> 2026-08-02. Esa caja está corregida.
>
> **Lo que se retira:** la *justificación* de `τ_Π` en el apéndice EFT de
> Paper 1, que decía derivar `τ_Π H₀ = KAL₀/(3Ω_DE)` saturando
> `ζ/(ρ_DE τ_Π) ≤ 1`. Con la inercia correcta esa saturación da **0.2946**, no
> 2.191; el acuerdo era exactamente el factor `(1+w₀)⁻¹ = 6.248` que faltaba.
> **Ningún número se mueve:** `τ_Π H₀ = KAL₀·Ω/T_r` es álgebra y ya estaba
> escrito así, y `Σm_ν = 0.06849` queda intacto. Lo que cae es la afirmación de
> que la causalidad lo *deriva*.
>
> **OP-22b (abierto), y de paso una atribución corregida.** Paper 5 citaba el
> «modo campo» como `c²_s,ad ∈ [0.60, 1]`, atribuyendo el Lagrangiano a
> «Papers 7 y 10». Ese número está calculado con `K = X/KAL + X²/M⁴`, que es el
> **funcional de apantallamiento de Paper 10**, no la acción de energía oscura.
> La acción es el condensado fantasma de Paper 7, y su velocidad es
> `c²_s,ad = (1+2u)/(1+6u) = 0.021284` con `u = c₂X/c₁ = −0.522735`.
> *(Es la misma confusión de las dos `K(X)` que ya se separó entre P7 y P10.)*
>
> Con la atribución correcta, los dos valores del sector son:
>
> | modo | fuente | `c²_s` |
> |---|---|---|
> | fluido viscoso | IS, `w₀+Ω_DE` | `0` |
> | campo, adiabático | condensado fantasma P7 | `0.021284` |
>
> No chocan en **carácter** —ambos son energía oscura **agrupada**, `c²_s ≪ 1`.
>
> **Actualización 2026-09-07 — NO son dos canales (conteo de grados de
> libertad).** Un escalar k-essence lleva **exactamente un** modo escalar
> propagante (P7, matriz cinética `K_X + 2X·K_XX`), y en el fluido IS la
> presión viscosa `Π` es un auxiliar que relaja, esclavo de la perturbación de
> densidad, no un segundo modo que viaje. Las dos descripciones cuentan
> **una** onda ⟹ los dos números describen **la misma**, y la del campo es la
> fundamental de las dos: sale de la acción.
>
> Y se ve *cuál* es la aproximada:
>
> | | velocidad de base | rescate | total |
> |---|---|---|---|
> | fluido | `c²_ad = w₀ = −0.839950` (inestable) | `+Ω_DE` | `0` |
> | campo | `+0.021284` (estable) | ninguno | `0.021284` |
>
> El fluido toma prestado `c² = w₀`, que por sí solo es inestable a gradientes,
> y la viscosidad entra exactamente a rescatarlo. El campo no necesita rescate.
>
> **Actualización 2026-09-07 (segunda) — de dónde saldría `ζ`: de ningún
> lado.** Dos verificaciones, ambas corridas:
>
> 1. **`KAL₀` no está en la acción de energía oscura.** P7 es
>    `K = c₁X + c₂X²`; `KAL₀` sólo aparece allí en el potencial *retirado*, en
>    `ω_c` y en la tabla de constantes. El `X/KAL₀` es el funcional de
>    **apantallamiento de P10**. La frase de P5 «la misma `KAL₀` que normaliza
>    `K(X)` fija la viscosidad» señalaba el objeto equivocado — es la tercera
>    aparición de la confusión de las dos `K(X)`. Corregida en P5.
> 2. **La acción de P7 es exactamente adiabática.** Con simetría de shift
>    (sin potencial, sin acoplamiento), `δp − c²_s·δρ = 0` **idénticamente** en
>    `(c₁,c₂,X)`. Control: el mismo `K` con un potencial `V₀e^{−αφ}` devuelve
>    coeficiente no nulo, o sea el detector sí ve la parte no adiabática cuando
>    la hay. Sin producción de entropía **no hay viscosidad de volumen: `ζ = 0`
>    desde la acción**.
>
> ⟹ La capa IS de Paper 5 **no es una propiedad del campo**: es una reparación
> de la parametrización `(w, c²_s)` que imponen los códigos de Boltzmann, donde
> el cierre ingenuo `c²_s = w₀ < 0` reventaría. La predicción propia del sector
> es la del campo, `c²_s = 0.021284`. El `0` es lo que se escribe en un código,
> no un número rival.
>
> **Actualización 2026-09-07 (tercera) — `KAL₀` se cancela; ¿entonces qué es?**
> En el observable sólo entra la **razón** `ζ̃/(τ_Π H₀) = Ω_DE`, y como `ζ̃` y
> `τ_Π` comparten el factor `KAL₀`, **se cancela**. Comprobado con `KAL₀`
> ×0.5, ×1, ×2, ×7.3: `c²_eff = 0` en los cuatro. El `0` sale de la identidad
> `Ω_DE = |w₀|`, no de `KAL₀`. Luego **la partición `ζ̃ = KAL₀/3` no está
> determinada por nada de esta capa** — y no se reclama que lo esté.
>
> **Pero `KAL₀` no es decorativo en el marco.** Su rol medible es otro:
>
> | rol | ¿mueve un observable? |
> |---|---|
| `ζ̃ = KAL₀/3` → `c²_eff` (P5) | **no** — se cancela |
> | `ω_c = KAL₀·ω_b·n_s` (P1) | **sí** — ~10σ por cada 10% |
> | `Σm_ν` vía `R₂` y `τ_Π` (P1) | **sí** — `KAL₀` entra **al cuadrado** |
> | `X/KAL₀` apantallamiento (P10) | **sí**, pero degenerado con `M⁴` |
>
> **Corrección dentro de la misma sesión:** primero escribí que `KAL₀` se mide
> «por la materia oscura, no por la viscosidad». Es demasiado fuerte. La
> cancelación es **local a `c²_eff`**. `τ_Π` sí está anclado, y precisamente por
> la cadena de viscosidad: `Σm_ν = R₂·ω_b·93.14/(τ_Π H₀)` con
> `R₂ = Ω/(KAL₀T_r)` y `τ_Π H₀ = KAL₀/(3Ω_DE)`, o sea `KAL₀` al cuadrado. Con
> `KAL₀ ×1.1` sale `Σm_ν = 0.056604 eV`, **bajo el piso de oscilaciones 0.058
> ⟹ falsado**. El rol de viscosidad no está ocioso en el marco: está ocioso en
> *ese* observable.
>
> **Rótulo unificado 2026-09-07 (formulación de Mike): `KAL₀` es la ley de
> retener.** No eran dos nombres compitiendo: en un fluido, retener *es* lo que
> se llama viscosidad. Medido en las cuatro dependencias, todas apuntan al mismo
> lado — `KAL₀` mayor ⟹ el sistema **cede menos**:
>
> | | `×1` | `×1.2` | |
> |---|---|---|---|
> | `ω_c` | `0.119514` | `0.143417` | más materia retenida |
> | `τ_Π H₀` | `2.191165` | `2.629398` | responde más lento |
> | `R₂` | `0.071875` | `0.059896` | se desvía menos |
> | `X/KAL₀` | `0.181113` | `0.150928` | campo más costoso de mover |
>
> Y «retención» **ya estaba en la suite**: Paper 1 §EFT L138 dice literalmente
> *«the retention constant KAL₀ ≡ β+π»*; la ley de linaje de la rama π la
> fabrica como retención (`look_elsewhere_full.py:56`); `prueba_rol.py:45`
> llevaba los dos nombres en la misma línea. No fue un renombre sino retirar un
> préstamo: se le había puesto a toda la constante el nombre de su instancia de
> fluido — justo el uso en que `KAL₀` se cancela.
>
> **El símbolo `KAL₀` no cambia.** Se unificó la etiqueta en 13 sitios vivos;
> `archive/` no se toca, y `ζ̃` sigue llamándose viscosidad porque ahí sí lo es.
>
> **Lo que queda abierto (OP-22b, ahora más estrecho):** el mapa de los
> parámetros del campo a los del fluido efectivo `(ζ̃, τ_Π)` **no está
> derivado** —y por lo anterior no puede estarlo dentro de la acción actual—, así que *por qué* el límite de fluido cae exactamente en `0` y no
> en `0.021284` sigue sin establecerse. La brecha `0.021284` es *toda* la
> predicción de Paper 7: una medida de `c²_s` discrimina.

<details><summary>Diagnóstico original (2026-08-02), conservado</summary>


**Cómo se encontró.** Mike pidió *«primero dale una leída y revisa todo que esté
bien, si se aplicaron los cambios bien»* antes de seguir. El repaso encontró que
mi propio arreglo del mismo día (3.1b-i) era **prematuro y creaba una
contradicción interna**. Retirado; el problema real queda declarado aquí.

### Los hechos

1. **La inercia correcta es la entalpía.** La ecuación de Euler relativista —que
   el Apéndice A de Paper 5 escribe bien— lleva $(\bar\rho+\bar p)$, no
   $\bar\rho$. Rederivado simbólicamente:
   $c^2_{s,\rm eff} = c^2_{s,\rm bare} + \zeta/[(\rho+p)\tau_\Pi]$.
   *(Esta parte sí es corrección firme y ya está aplicada al Apéndice A.)*

2. **Con la ζ que fija el ansatz actual, sale superlumínico.** De
   $\Pi=-\mathrm{KAL_0}\rho_{\rm DE}H$ y $\Pi=-3\zeta H$ sale
   $\zeta=\mathrm{KAL_0}\rho_{\rm DE}/3$, y entonces
   $c^2_{s,\rm eff} = -0.840 + 5.248 = \mathbf{+4.41}$.

3. **La atribución es huérfana.** Paper 5 dice «Paper~1 identifies the IS
   steady-state condition as $\Pi=-\mathrm{KAL_0}\rho_{\rm DE}H$». **Paper 1 no
   la contiene**: su glosario lista $\tau_\Pi H_0\simeq2.191$ apuntando a un
   apéndice que no la deriva. ($\Pi$ aparece 3 veces en todo Paper 1.)

4. **Renombrar el símbolo NO arregla nada.** Intenté redefinir
   $\tilde\zeta \equiv \zeta/[(\rho+p)H_0]$; pero la $\zeta$ **física** está
   fijada por el ansatz, así que el $+4.41$ no se mueve. Mi nota al pie quedaba
   además contradiciendo al párrafo siguiente. Retirada.

### 🔎 LA FUENTE APARECIÓ — y el número de Paper 5 SÍ sale de ella (2026-08-02)

> ⚠️ **Esta sección corrige una afirmación mía anterior del mismo día.** Primero
> escribí «la fuente no dice lo que Paper 5 le atribuye». **Parcialmente falso**:
> el NÚMERO sí sale; la ETIQUETA no. Ver «corrección» abajo.

Mike: *«¿por qué no buscas en archive a qué Paper 1 apuntaba? … lo que yo
recuerdo de viscosidad es KAL»*. **Tenía razón en las dos cosas.** La
derivación existe, en `archive/codigo/SSEE_appendix_Friedmann.tex`, y la
viscosidad **sí** es KAL:

    ζ = KAL₀·H/(8πG)                     [ec. app_zeta de la fuente]
    Π = −3ζH = −3·KAL₀·H²/(8πG)          [ec. app_Pi]

Como $\rho_{\rm crit}\equiv 3H^2/(8\pi G)$, eso es **Π = −KAL₀·ρ_crit** — la
densidad **crítica total**, no la de energía oscura.

**Paper 5 afirma otra cosa:** «Paper~1 identifies … $\Pi = -\mathrm{KAL_0}\rho_{\rm DE}H$».
Dos discrepancias: $\rho_{\rm crit}$ vs $\rho_{\rm DE}$, y un $H$ suelto de más.

**Consecuencia numérica.** Adimensionalizando $\tilde\zeta \equiv \zeta H_0/\rho_{\rm DE}$:

    ζ̃ de la fuente  = KAL₀/(3·Ω_DE) = 2.191165
    ζ̃ de Paper 5    = KAL₀/3        = 1.840469
    difieren por exactamente Ω_DE

**Y algo notable que la fuente sí da:** con su valor, $\tilde\zeta = \tau_\Pi H_0$
**exactamente** (ambos son KAL₀/(3Ω_DE); diferencia 0.00e+00), así que la razón
vale 1 y

    c²_s,eff = w₀ + 1 = 1 + w₀ = 0.160050

Positivo, estable, subluminal, y sale limpio. **Pero no es el 0 que publica
Paper 5.**

### ⚠️ Corrección: el número de Paper 5 SÍ está derivado

Adimensionalizar $\zeta = \mathrm{KAL_0}H/(8\pi G) = \mathrm{KAL_0}\rho_{\rm crit}/(3H)$
admite **dos** normalizaciones, y yo probé sólo una:

| normalización | resultado |
|---|---|
| $\tilde\zeta\equiv\zeta H/\rho_{\rm crit}$ | $\mathrm{KAL_0}/3 = 1.840469$ ← **el de Paper 5** |
| $\tilde\zeta\equiv\zeta H/\rho_{\rm DE}$ | $\mathrm{KAL_0}/(3\Omega_{\rm DE}) = 2.191165$ ← el que usé yo |

⟹ **El valor $\tilde\zeta = \mathrm{KAL_0}/3$ de Paper 5 está derivado de la
fuente archivada**, normalizando a $\rho_{\rm crit}$. Lo que está mal es la
*etiqueta* del texto de Paper 5, que dice $\rho_{\rm DE}$. Error de escritura,
no de número.

Mike tenía razón al desconfiar de mi diagnóstico: *«si el problema fuera tan
simple ya lo hubieras visto cuando se hizo esto en primer lugar»*. La pieza no
era arbitraria; estaba derivada, sólo mal etiquetada.

### Lo que SÍ sigue en pie, y es lo que importa

**1. El problema de la entalpía es independiente de la etiqueta.** La inercia
sale de la física de la onda, no de cómo se llame $\tilde\zeta$:
$c^2_{s,\rm eff} = +5.41$ con inercia $(\rho+p)$, en cualquier normalización. <!-- R74: git:f6dca4727c:results/logs/b1_full_run.log -->

**2. La pieza que de verdad falta es $\tau_\Pi$, no $\tilde\zeta$:**

| cantidad | estado |
|---|---|
| $\tilde\zeta = \mathrm{KAL_0}/3$ | ✅ **DERIVADA** (`archive/codigo/SSEE_appendix_Friedmann.tex`) |
| $\tau_\Pi H_0 = \mathrm{KAL_0}/(3\Omega_{\rm DE})$ | ❌ **NO derivada en ningún documento del repo** |

Papers 4 y 5 la **usan**; Paper 1 apunta a un «App. A» que no existe. Paper 5
la describe como *«derived from background IS steady state»*, pero el estado
estacionario ($\Pi=-3\zeta H$) **no fija $\tau_\Pi$** — es el límite de
Navier-Stokes, donde $\tau_\Pi$ ha desaparecido de la ecuación.

**3. Σm_ν depende de $\tau_\Pi$.**
$\Sigma m_\nu = \mathcal{R}_2\,\omega_b\,93.14/(\tau_\Pi H_0) = 0.068490$ eV.
Si $\tau_\Pi$ fuese $\mathrm{KAL_0}/3$ en vez de $\mathrm{KAL_0}/(3\Omega_{\rm DE})$,
$\Sigma m_\nu$ subiría **+19.1%** a 0.0815 eV, arrastrando $\omega_\nu$,
$\omega_m$ y $\Omega_{m,\rm CMB}$.

### ✅ LOCALIZADO: τ_Π SÍ está derivada — y ahí está el bug (2026-08-02)

**Origen real:** `manuscript/SSEE_EFT_section.tex` (apéndice EFT de Paper 1),
commit `6248350` del **2026-04-26**, *anterior* a que existiera Paper 5:

```
c²_s = ζ/(ρ_DE·τ_Π) = KAL₀/(3·Ω_DE·τ_Π H₀) ≤ 1     [eq:IS_causality]

Poniendo c²_s = 1 (frontera de causalidad, Hiscock-Lindblom 1985):
τ_Π H₀ = KAL₀/(3·Ω_DE) = KAL₀·M_v/(3·T_r) ≈ 2.191   [eq:tau_IS]
```

**No era arbitraria.** Se fija exigiendo que la señal viscosa no supere a la luz.

### El bug, exacto

La MISMA cantidad física ζ/(ρ·τ_Π) tiene **dos valores** en la suite:

| documento | valor | por qué |
|---|---|---|
| `SSEE_EFT_section.tex` | **1.000000** | es así como se DERIVÓ τ_Π |
| `SSEE_Paper5_IS.tex` | **0.839950** | ζ̃/(τ_Π H₀) = Ω_DE |

Difieren por exactamente Ω_DE. **Causa:** EFT_section normaliza ζ a ρ_DE y con
eso fija τ_Π; Paper 5 normaliza ζ a ρ_crit (por eso obtiene KAL₀/3) pero luego
divide ese ζ̃ por el τ_Π derivado con la *otra* normalización.

**Consecuencia:**

    consistente (una sola normalización):  c²_s,eff = w₀ + 1     = 1+w₀ = 0.160050
    Paper 5 (normalizaciones mezcladas):   c²_s,eff = w₀ + Ω_DE  = 0

**El «0» es el artefacto.** Si τ_Π se fijó poniendo c²_s = 1, entonces por
construcción la corrección viscosa vale 1, no 0.84. Y el resultado consistente,
$c^2_{s,\rm eff}=1+w_0=0.160050$, es **positivo, subluminal y ya vive en el
modelo** (es el mismo número que α_K y λ usan legítimamente como cantidad de la
ecuación de estado).

### Contramedida instalada: R48 y R49

- **R48** — sección `cross_document:` en `CANONICAL_VALUES.yaml`: la misma
  cantidad calculada en dos documentos debe dar el mismo valor. **Probada
  contra el estado previo a esta declaración: la caza en ROJO.** Con OP-22
  declarada cuenta como deuda (tope 1, sólo baja); al resolverse, cae a 0.
- **R49** — el campo `source` de un canónico debe apuntar a un documento que
  contenga el valor. El de τ_Π decía «Paper 4 L686» — que la **usa**, no la
  deriva. Corregido al origen real.

### Por qué esto pasó todas las auditorías (la pregunta de Mike)

Porque **no hay ningún número mal**. $\tilde\zeta$ está derivada, $\tau_\Pi$ es
consistente con todo lo que la usa, y el guardián compara valores contra el
Registro — que los tiene. Lo que falta es una **derivación**, y ninguna capa
verificaba «¿existe la derivación que este documento dice que existe?».
Es el mismo hueco que R47 abrió para los supuestos: coherente consigo mismo,
por eso invisible.

### Los tres valores en circulación

| origen | ζ̃ | c²_s,eff | inercia usada |
|---|---|---|---|
| fuente archivada (ρ_crit) | 2.191165 | **+0.160050** = 1+w₀ | ρ |
| Paper 5 publicado (ρ_DE) | 1.840469 | +0.000000 | ρ |
| lo que pide estab. marginal | 0.294567 | 0 | ρ+p |

**Ninguna combinación da a la vez la inercia correcta (ρ+p) y un c²_s causal
con los ansätze hoy en el registro.** Ése es el problema, y es más profundo que
la normalización de un símbolo.

### La resolución candidata (NO adoptada)

    Π = −KAL₀·(ρ+p)·H     ⟹   ζ = KAL₀(ρ+p)/3   ⟹   c²_s,eff = 0 idénticamente

**Argumento independiente a su favor:** con $w=-1$ exacto se tiene $\rho+p=0$, y
una constante cosmológica no tiene grados de libertad de fluido, así que su
presión viscosa **debe** anularse. $\Pi\propto(\rho+p)$ lo da; $\Pi\propto\rho$
no —predice viscosidad para una Λ pura, que es absurdo.

**Por qué no se adopta aquí:** cambia un **ansatz estructural** del marco, no una
convención de escritura. Es decisión de Mike, y además obliga a escribir en
Paper 1 la derivación que hoy falta (punto 3).

### Qué hacer

1. Decidir la forma del ansatz (o derivarla del Lagrangiano — es 3.1b-ii).
2. Escribir en Paper 1 la derivación de $\tau_\Pi H_0$ y del estado
   estacionario, que hoy sólo existen como entrada de glosario.
3. Si se adopta $(\rho+p)$: todo cierra y $c^2_s=0$ vuelve a ser exacto, con la
   ζ física $=0.2946\,\rho_{\rm DE}H_0$ en vez de $1.8405$.

**Estado de Paper 5 mientras tanto:** lleva una caja naranja declarando que sus
resultados de estabilidad son **condicionales a OP-22**. Ningún número impreso
cambió; cambió lo que se afirma de ellos.

**Severidad:** Alta. Toca el resultado Q1 (estabilidad), que es el central del paper.

---

</details>

## OP-16 — ¿Coincide $(\pi-\varphi)/(\pi+\varphi)=0.3201$ con una fracción medida de la descomposición masa-energía del protón? (origen génesis) — ABIERTO / ESPECULATIVO

**Origen.** El sistema fenomenológico génesis (`SSEE_UNIFICADO`, "Resolución Física de
Partículas") asignaba al protón un "registro" $\mathrm{Ygg}_P = 0.319$ ("66% gravedad +
34% fotones / pensamiento cristalizado"). Ese número se había filtrado a Paper 4 como
"Proton register" y fue **retirado en la auditoría P4-A (2026-06-15)** por dos defectos:
(1) **circular** — el "valor observado" era $0.319$ (YGG, interno), no una medición;
(2) **mal etiquetado** — $0.3201 = \Omega_{m,\rm CMB}$ es materia **total** (dominada por DM),
no bariónica ($\Omega_b \approx 0.049$). No es física de partículas: es cosmología disfrazada.

**Por qué NO está muerto (la salida honesta).** La intuición génesis *"la masa del protón
es energía de campo, no constituyentes"* **es físicamente correcta**: la descomposición
lattice-QCD de la masa del protón (p.ej. Ji / Yang et al.\ 2018) da masa de quarks $\sim 9\%$,
energía cinética de quarks $\sim 32\%$, energía de gluones $\sim 37\%$, anomalía de traza
$\sim 23\%$. La masa del protón **sí** es mayoritariamente energía de campo.

**El test falsable (requisitos de entrada — las tres reglas).** Para que $0.3201$ se gane un
lugar en física de partículas (dominio del Modelo Estándar, **independiente** de la cosmología;
distinto de $m_\varphi$ que vive *dentro* del sector oscuro cosmológico):
1. **Comparar contra una fracción MEDIDA** de la descomposición (con barras de error de lattice),
   NO contra un número interno YGG.
2. **Forward-prediction:** la fórmula $(\pi-\varphi)/(\pi+\varphi)$ fija de antemano, sin elegir
   a posteriori cuál de las 4 fracciones "casa mejor" (evitar look-elsewhere oculto).
3. **Anclaje físico:** idealmente atado a una escala/Lagrangiano (no una coincidencia adimensional
   suelta), igual que se exige en [[feedback_three_principles]].

**Criterio de cierre.** Si $0.3201$ está a $>2\sigma$ de **toda** fracción estándar de la
descomposición → coincidencia, se cierra. Si casa con **una** dentro de error Y se puede atar
estructuralmente a $\{\varphi,\pi\}$ → merece una nota dedicada (no antes).

**Severidad: Baja / especulativa.** Cero impacto sobre la suite cosmológica de 10 papers
(la cosmología no depende de esto). Es una **dirección de investigación**, no un claim de paper.
Abordar SOLO después de las auditorías. Relacionado con la advertencia [[project_genesis_repo_risk]].

---

## Summary Table

| ID | Paper | Problem | Severity | Path to Resolution |
|----|-------|---------|----------|--------------------|
| OP-1 | P4 | ~~Factor 200 in Ω_b h²~~ | ✅ PARCIAL | (π−φ)/H₀_SSEE=0.32σ Planck; BBN derivation → Paper B/C; script op1 |
| OP-2 | P4 | ~~n_s exponent 7 not derived from V(φ)~~ | ✅ RESUELTO | α-attractor universality + N_*=2φ⁷; r=φ⁻¹⁰ nueva predicción; script op2 |
| OP-3 | P10 | Origen del `5/2` en `M⁴ = 5φ⁸ρ_c` | 🟡 PARCIAL | Reabierto 2026-09-06 (Registro V-L3-OP3). `KAL_eff` se despeja DE `M⁴`, no al revés. **3 rutas cerradas por medición**: A sobredeterminada, C subdeterminada + serie no trunca, y la cascada de Hubble NO mide `M⁴` (banda ±0.968 vs residuo 4.2e-06). Falta el `5/2` sin usar `M⁴` ni SH0ES |
| OP-4 | P8 | r_V > r_Hubble para Vainshtein | ✅ **CERRADO 2026-10-03** | P8 ya no cita radio de apantallamiento (sección reducida a un párrafo; sin acople βc en la acción no hay quinta fuerza que apantallar). Historia: El cierre de 2026-05-15 (k-mouflage + αB=αM=αT=0) sigue en pie para la *selección del límite*, pero la auditoría externa (Max, commit 17acccd) encontró que `eq:rkm` **no cierra dimensiones**: evaluada en GeV da r☉=1.44e4 m y en eV 1.44e7 m — un factor 1000 según la unidad elegida. Ver la ficha completa arriba. NO entra en la predicción de lensing del límite canónico, que descansa en ω_c (OP-8) y α_B=α_M=0 (P7) |
| OP-5 | P5-6 | ~~S₈ weak-lensing tension~~ | ✅ **DISUELTO 2026-08-01, confirmado 2026-09-20** | No hay tensión. Contra KiDS-1000 con A_s libre: S₈=0.7559 ± 0.0189 (0.10σ). Contra **KiDS-Legacy con A_s CLAVADO al del CMB** (cero libres cosmológicos): S₈=0.8273 predicho vs 0.8265±0.0176 medido = **0.04σ**, χ²=417.97/357. El 3.5σ era artefacto de fijar A_s a Planck, o sea de importar la tensión Planck–KiDS |
| OP-6 | P9 | Screening form ambiguity | ⚠️ RETIRADA 2026-10-03 → OP-6b | La identidad 1+w₀=Ω_m era falsa; la forma multiplicativa es POSTULADO en Paper 9 (eq:screen_postulate) |
| OP-7 | P4/7/8 | QFT derivation of Genesis role assignments | ✅ PARCIAL | EFT uniqueness formalizado P7 §5.2 + P1 §5.3; QFT desde primeros principios → largo plazo |
| OP-8 | Transv. | ~~MIRA dynamical mechanism~~ → factor-materia DISUELTO | ✅ DISUELTO 2026-06-18 | Reframe ω_m-directo: Ω_m,CMB=ω_m/h²=0.30889 sin factor (ω_c=KAL₀·ω_b·n_s forward); MIRA persiste solo en f_screen; CMB χ²=1003.586/ΔBIC=−26.03 (ΛCDM con su mν 0.06, 2026-09-29) |
| OP-9 | P6 | ~~UV origin of mass multiplier~~ | ⚫ **CERRADO POR DISOLUCIÓN 2026-08-01** | La partícula fue retirada (la resta que definía Ω_φDM mezclaba densidad con ecuación de estado); no queda multiplicador que derivar. No resuelto: dejó de ser pregunta |
| OP-10 | P6/P7 | ~~Unify χ into φ via richer V(φ)~~ | ⚫ **CERRADO POR DISOLUCIÓN 2026-08-01** | No hay segundo campo χ que unificar |
| OP-11 | P6 | ~~ξ (non-minimal coupling) is free parameter~~ | ⚫ **CERRADO POR DISOLUCIÓN 2026-08-01** | ξ vivía en el sector φ-DM retirado |
| OP-12 | P6 | ~~Ω_φ-DM h² not computed ab initio~~ | ⚫ **CERRADO POR DISOLUCIÓN 2026-08-01** | Ω_φDM no era una densidad: era el residuo de una resta mal planteada |
| OP-13 | P8 | ~~Contradicción interna §3-4 vs §4.5~~ | ✅ RESUELTO | Opción A aplicada: framing dos-límites, retirado claim "MIRA en lensing", $\sqrt{\AURA}$ ≠ $\MIRA$ aclarado, canonical prediction = GR-with-DM (2026-05-23) |
| OP-14 | P4 | ~~Σm_ν Type P; offset 22 ad hoc~~ → canónico Type A | ✅ RESUELTO | $\Sigma m_\nu^{\rm active}=\mathcal{R}_2\,\omega_b C_\nu/(\tau_\Pi H_0)$ $=0.0685$ eV con $\mathcal{R}_2=\Omega_{\rm DNAV}/(\mathrm{KAL}\cdot\mathrm{TRIAL})=0.07188$; offset 22 eliminado, Σm_ν promovido Type P→Type A (2026-06-04) |
| OP-15 | P1 | Bullet offset κ(θ) desde KAL(x) no calculado | Medium-High | Computar Σ_SSEE(θ)=∫ρ_bar·KAL(x)dℓ del Bala; mostrar pico κ sobre galaxias, no gas (falsable vs Clowe+2006). Distinto de OP-13 (amplitud); esto es distribución espacial (2026-06-14) |
| OP-16 | — (génesis) | ¿0.3201=(π−φ)/(π+φ) casa con fracción medida de la masa-energía del protón? | Baja/especulativa | Retirado de P4 (P4-A, era circular+materia total mal-etiquetada). Test: comparar vs descomposición lattice-QCD (quark 9%/gluón 37%/anomalía 23%) con barras, forward, anclado a (φ,π). Cero impacto en cosmología; dirección de investigación post-auditoría (2026-06-15) |
| OP-21 | P5 | ~~ζ̃ hipótesis no derivada~~ → ζ̃ = KAL₀·Ω/M_v, **hermana de τ_Π = KAL₀·Ω/T_r** | 🟡 **REDUCIDO 2026-08-02** | No es número libre: lo fijan τ_Π (P4) + w₀ (P1) + minimalidad. Queda abierto el PRINCIPIO (minimalidad) y derivar τ_Π del Lagrangiano. Look-elsewhere intentado y RETIRADO (valor forzado por identidad) |
| OP-22 | P5, P4, P1 | ✅ **CERRADO 2026-09-06**: es Π ∝ (ρ+p) (test de límite w→−1; testigo F≈186). El `0` es resultado. Se retira la *derivación* de τ_Π por causalidad (usaba ρ, daba 0.2946). Queda OP-22b. — *diagnóstico viejo:* **τ_Π H₀ = KAL₀/(3Ω_DE) no está derivada en ningún documento** (P4 y P5 la usan; P1 apunta a un App.A inexistente). ζ̃=KAL₀/3 SÍ está derivada (archive/…Friedmann.tex, normalizando a ρ_crit; P5 la etiqueta mal como ρ_DE). Y con la inercia correcta (ρ+p) c²_s sale superlumínico | ✅ **CERRADO 2026-09-06** | **Σm_ν depende de τ_Π** y NO se mueve: τ_Π no cambia. Pasó las auditorías porque NINGÚN número está mal: falta una DERIVACIÓN, y ninguna capa verificaba que exista la derivación que un documento dice tener |
| OP-23 | P7 | ~~Dentro del acoplamiento conformal no existe $\beta_c$ que reproduzca $w_0$~~ | ⚫ **CERRADO POR DISOLUCIÓN 2026-09-06** | Su premisa era «el acoplamiento es conformal». Ya no hay acoplamiento de ningún tipo: la acción de Paper 7 es un condensado fantasma mínimamente acoplado. El OP nombró él mismo esta salida en su §5 — «SSEE no admite acoplamiento oscuro, $\beta_c=0$» — y es la que ocurrió, por vía independiente |

**Severity legend:** High = referee would likely request resolution before acceptance;
Medium = requires acknowledgment and discussion; Low = cosmetic or presentational.

---

## Note on Methodology

These problems are documented here rather than concealed because scientific integrity
requires pre-registration of known limitations. Referees and collaborators should be
directed to this document when evaluating the strength of the SSEE predictions.

## OP-17 — Partícula canónica — ⚫ **RETIRADA 2026-08-01** (la adopción de 2026-06-19 queda revertida)

> 🔴 **DECISIÓN REVERTIDA.** El 2026-06-19 esta partícula se **adoptó**. El
> 2026-08-01 se **retira**, junto con todo el sector φ-DM: la resta que definía
> su densidad, Ω_φDM = Ω_m,CMB − Ω_m,dyn = 0.308881 − 0.160, restaba una
> densidad medida menos un número de la **ecuación de estado** (0.160 = 1+w₀).
> Bien formada aritméticamente, vacía de física ⟹ la partícula no tenía de qué
> estar hecha. Y la tensión S₈ que la motivaba no existe contra el dato crudo
> (S₈ = 0.7559 ± 0.0189, 0.10σ).
>
> **Cómo se escapó esta entrada en la ola de propagación del 2026-08-01:** el
> guardián busca **números** retirados, no **decisiones** revertidas. Un
> encabezado que dice «✅ ADOPTADA» sin citar ninguna cifra retirada pasa
> invisible. Contramedida pendiente: extender R45 (que ya cruza «OP resuelto
> citado como abierto») al caso simétrico, «OP adoptado que fue revertido».
>
> Lo de abajo es registro histórico. **No citar como vigente.**

### Contenido histórico (la adopción, tal como se decidió en su momento)

**Status:** ✅ **CERRADO / ADOPTADO** (Mike, 2026-06-19). El diferimiento se revirtió
en la misma sesión ("Mira bien lo que NO es, es SOLAR"): se adoptó la partícula con
mecanismo en vez de seguir con PYROS·VITA·MIKA. **HECHO:** CLASS forward real @ 40.70 eV
($\sigma_8=0.747$, $S_8=0.758=0.04\sigma$ KiDS, $k_{\rm fs}=0.754$, $\alpha=1.108$,
$T_\phi=0.5385\,T_\nu$, $N_{\rm ur}=2.9619$) → propagado a `CANONICAL_VALUES.yaml`, <!-- R74: git:d7446ace8a:results/logs/p6_class_reframe_omega_m.log -->
guardián (VERDE 119), manuscrito Paper 6 completo (Lagrangiano g²·v escrito, fσ8
recomputado 0.82σ, 25 pp, `docs/`), 3 memorias. **RETIRADO** 615.33/42.47. <!-- R74: git:f3b01e5c2d:CANONICAL_VALUES.yaml -->
Residuo único: OP-9 (derivar el coeficiente del transporte).

**Qué cambió:** la partícula canónica pasó de $m_\phi=42.47$ eV (PYROS·VITA·MIKA=615.33, <!-- R74: git:f3b01e5c2d:CANONICAL_VALUES.yaml -->
triple-producto plano, sin mecanismo, $S_8=0.24\sigma$) a
$$m_\phi = \mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V\cdot\Sigma m_\nu = (\varphi+2\pi)^2\cdot (\varphi+\pi+\Omega)\cdot 0.0685 = 40.70\ \text{eV},$$
que **resuelve $S_8$ de lleno ($0.04\sigma$ KiDS)** — el valor que los datos prefieren
(`ssee_paper6_particle_scan.py`, CLASS real). Esta era la finalidad del mecanismo.

**Por qué es mejor partícula (peso, no certeza):**
- $\mathrm{KRYSTOS}_V=\varphi+\pi+\Omega$ (padres {φ,π,Ω}), **anclado** por $w_a=-P_{sc}/K_v=-0.670$ (DESI).
- $\mathrm{SOLAR}=\mathrm{BIAL}+\mathrm{KAL}$ = (primer-calor/pulso, radiativo) + (viscosidad
  anclada P5). Rol radiativo **por linaje**, valor $\varphi+2\pi$ forzado.
- Forma $m=g^2 v\,\Sigma m_\nu$ = masa generada estándar (enhancement, no loop).
- **Peso vía KAL (clave):** KAL₀ aparece en 5 lugares — $\omega_c=\mathrm{KAL}_0\,\omega_b\,n_s$
  (¡la densidad de materia del CMB! → **"CMB prefiere KAL"**, igual que "CMB prefiere MIRA"),
  $K(X)=X/\mathrm{KAL}_0$ (cinético que maneja la cascada Hubble), $\tilde\zeta=\mathrm{KAL}_0/3$
  (viscosidad), y ahora el acoplamiento φ-DM. SOLAR hereda el peso del KAL que el CMB exige.

**Lo honesto (no lo decidimos nosotros):** es una partícula **en camino a ser falseada**
($k_{\rm fs}$ en DESI Y3/Euclid 2026–2028 decide). Le damos **más peso** por el multi-anclaje
de KAL, NO certeza. El coeficiente $\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V$ aún NO está derivado
del transporte disipativo (ver el "mecanismo líder" en OP-9) — eso es lo que cerraría OP-9.

**Trabajo de implementación (cuando se haga):**
1. Correr CLASS exacto en el $m_\phi$ intermedio (retirado) → tomar $S_8/k_{\rm fs}/\sigma_8$ reales (no interpolados).
2. Propagar los $m_\phi$ y multiplicadores intermedios (retirados) por: `ssee_core`, `CANONICAL_VALUES.yaml`, guardián,
   3 memorias, vault (kfs/sigma8_eff/Cadena), Papers 1/6.
3. Escribir el mecanismo del **Lagrangiano** ($m_\phi=g^2 v\,\Sigma m_\nu$, $g$=SOLAR disipativo,
   $v$=KRYSTOS_V vacío) y **mostrar cómo resuelve $S_8$** en Paper 6.
4. Guardián VERDE + memory_sync VERDE.

---

None of these problems falsify SSEE at the current observational precision — they define
the boundary of what has been rigorously established versus what remains as working
hypotheses. The resolution of OP-1 through OP-6 constitutes the research agenda for
SSEE-V4.0; OP-8 through OP-13 constitute the agenda for SSEE-V5.0 (full unification
of the dark sector).

## Parameter-Count Status (2026-05-22) — CONTENIDO HISTÓRICO (conteo vigente: P1 §1.3)

SSEE-V3.6 currently has **~2 effective free parameters** vs **6 for $\Lambda$CDM**
(tras DISOLVER OP-8 el 2026-06-18: el factor-materia ya no es input — Ω_m,CMB sale
de ω_m algebraico; restan $H_0$ y $\Omega_b h^2$ como inputs ajustables):

| Parameter | Status | Comment |
|---|---|---|
| $H_0$ | Sampled in MCMC | Algebraic prediction 67.96 (coincidencia, V-L2-06) vs posterior canónico 66.53 |
| $\Omega_b h^2$ | Sampled in MCMC | Algebraic 0.02242 vs Planck 0.02237 |
| ~~MIRA factor~~ | ✅ DISUELTO 2026-06-18 — no hay factor materia; Ω_m,CMB=ω_m/h² (ω_c=KAL₀·ω_b·n_s forward) | OP-8 cerrado |
| $m_\phi$ | Phenomenological ansatz | OP-9 (paper admits) |
| $\xi$ | **Free parameter** (P6 L416) | OP-11 |
| $\Sigma m_\nu$ | **Phenomenological** (P4 L691-697 admite Type P) | offset 22 ad hoc — OP-14 |
| $\alpha$ (attractor) | $\varphi^4/3$ derived | from $\varphi$ |
| $V(\phi)$ form | Adopted exponential | locks DE-only behavior — OP-10 |

**Path to zero parameters:** OP-14 (✅ resuelto) y OP-9 (✅ refinado, forward-prediction)
cerrados; **OP-8 ✅ DISUELTO 2026-06-18** (factor-materia eliminado vía ω_m-directo).
Resta OP-10 (unify χ into φ via richer $V(\phi)$, daría el origen UV del multiplicador
de la masa φ-DM). End state ya alcanzado en el sector materia: $H_0$ y $\Omega_b h^2$
son los únicos inputs ajustables por observación.

**Dependency chain (cascada, actualizada 2026-06-04):** OP-14 ✅ → OP-9 ✅; ambos cerrados
sin V(φ). OP-10 ya no bloquea la masa — solo daría el origen UV del multiplicador
$\mathrm{SOLAR}^2\cdot\mathrm{KRYSTOS}_V=594.28$.

---

## OP-18 — Derivación de la amplitud primordial $A_s$ desde $(\varphi,\pi)$ (Paper 3 / inflación) — ABIERTO (2026-06-20)

**Origin.** Tras el reframe $\omega_m$-directo, el conteo honesto del sector CMB es
$k=2=\{A_s,\tau\}$: $H_0=3(\varphi+\pi)^2$ es derivado (SH0ES–$f_{\rm screen}$, Paper 9),
$\omega_b,\omega_c,n_s,w_0,w_a$ son algebraicos. Las **dos** únicas cantidades que el
ajuste CMB de SSEE **no** deriva de $\{\varphi,\pi\}$ son la amplitud escalar primordial
$A_s$ y la profundidad óptica de reionización $\tau$. OP-18 ataca la primera.

**El problema.** $A_s\simeq2.1\times10^{-9}$ entra como normalización del espectro
primordial; hoy se toma de Planck. SSEE ya fija el resto del sector inflacionario:
$\alpha=\varphi^4/3$ (α-attractor), $N_*=2\varphi^7$, $n_s=1-\varphi^{-7}=0.96556$,
$r=\varphi^{-10}$ (OP-2). En α-attractor la amplitud es
$A_s = \dfrac{V(\phi_*)}{24\pi^2\,\epsilon(\phi_*)\,M_{\rm Pl}^4}$, evaluada en $N_*$.
Con $\epsilon$ ya fijado por $r=16\epsilon$ (i.e.\ $\epsilon=\varphi^{-10}/16$), el **único
ingrediente faltante** es la **escala del potencial** $V_0$ (equivalentemente $M$, la
escala de inflación).

**Cálculo realizado (2026-06-20, `op18_As_from_inflation.py`) — resultado honesto.**
En el plateau, $A_s=(2\varphi^{10}/3\pi^2)\,(V_0/M_{\rm Pl}^4)$. El **prefactor
$2\varphi^{10}/3\pi^2=8.308$ es puro $(\varphi,\pi)$** — SSEE fija la FORMA del espectro
por completo ($n_s,r,\alpha,N_*$ y el prefactor). PERO la normalización exige
$V_0/M_{\rm Pl}^4=2.53\times10^{-10}$, i.e.\ $V_0^{1/4}\approx9.7\times10^{15}$ GeV <!-- R74: git:a509d91104:archive/codigo/investigacion/open_problems/salidas_2026-10-02/op18_As_from_inflation.log -->
(escala GUT/inflación, razonable). **Esa jerarquía NO sale limpia de potencias
$(\varphi,\pi)$** ($\varphi^{-46}$ cae a 4\% pero $-46$ no tiene razón estructural →
coincidencia, no derivación). **Corrección de una nota previa errónea:** anclar $A_s$ a
$\Lambda_{\rm SSEE}=M=9.68$ meV es **INCORRECTO** — esa escala es IR (energía oscura);
$V_0$ es UV (inflación), separadas $\sim10^{27}$. La "ruta alcanzable vía $M$" queda
**retirada**. OP-18 sigue abierto de verdad: el residuo es la **escala de inflación
$V_0$**, una jerarquía UV análoga al problema de jerarquía, no un anclaje trivial.

**Lo defendible hoy (check de consistencia, no derivación):** dado $A_s$ medido y la forma
SSEE fijada, la escala de inflación inferida cae en el rango GUT esperado ($\sim10^{16}$ GeV).
$A_s$ permanece como **1 input de escala** del modelo; lo que SSEE aporta es que $n_s,r$ ya
no son perillas. Cierre futuro: una teoría de $V_0$ desde la UV-completion (liga a OP-10/OP-3).

**Test cuantitativo (forward, falsable) — pendiente de una teoría de $V_0$.** Si en el
futuro $V_0$ se deriva estructuralmente, calcular $A_s^{\rm SSEE}$ y comparar con Planck
$\ln(10^{10}A_s)=3.044\pm0.014$. Si cae dentro de $\sim1\sigma$ **sin** ajustar $V_0$ al
dato, $A_s$ pasa de parámetro a predicción → el sector CMB del modelo baja a
**$k=1$ del modelo + $\tau$ nuisance**.

**Sobre $\tau$ (por qué NO es un OP gemelo).** $\tau$ no se deriva de $\{\varphi,\pi\}$
puros porque su cadena pasa por astrofísica bariónica (eficiencia de formación estelar
$f_*$, escape de fotones ionizantes $f_{\rm esc}$): $(\varphi,\pi)\to A_s\to\sigma_8\to D_1
\to$ primeros halos $\to[f_*,f_{\rm esc}]\to z_{\rm reion}\to\tau$. Lo honesto es tratar
$\tau$ como **nuisance astrofísico compartido** con ΛCDM (se cancela en $\Delta$BIC), o
—como mucho— convertirlo en *output predicho* dado $A_s$ + un modelo de reionización
estándar (no derivado de $(\varphi,\pi)$). No es imposible, pero no es derivación pura;
por eso $\tau$ queda como residuo nuisance, no como OP de derivación.

**Severity:** Medium. Es el último parámetro genuinamente cosmológico no-derivado del
modelo; cerrarlo lleva el conteo a "0 parámetros del modelo + $\tau$ nuisance".
**Relation:** depende de OP-2 (✅, da $\epsilon,N_*$) y de la escala $M$ de Paper 10.
Script a crear: `op18_As_from_inflation.py`.

---

## OP-19 — Mecanismo de producción detrás de $\omega_c = \mathrm{KAL_0}\cdot\omega_b\cdot n_s$ (Papers 1, 6 / abundancia relic) — ABIERTO (2026-07-12)

> **2026-10-03 — primera prueba barata: la masa ADM NO separa SSEE de ΛCDM.** Si la materia oscura
> comparte asimetría con los bariones (ADM, razón de números r = n_DM/n_b), su masa es
> m_DM·r = (ω_c/ω_b)·m_b. Con m_b la masa media por barión (Y_p de CAMB): **SSEE 4.996 GeV**
> (cociente 5.331 = KAL₀·n_s) contra **ΛCDM-Planck 5.027 GeV** (cociente 5.364): difieren un 0.6 %,
> que ninguna búsqueda directa resuelve. Control R53: la identidad KAL₀·n_s vale para el cociente de
> SSEE y NO para el de ΛCDM. **Lectura:** una búsqueda directa a ~5 GeV pondría a prueba la familia
> ADM, no a SSEE; y r no sale del álgebra, así que elegirlo para acertar sería una perilla (regla 1).
> Lo propio de SSEE es que el cociente está FIJADO; sólo un mecanismo que dé r y m_DM desde el álgebra
> lo volvería medible. Log `results/logs/op19_adm_masa.json` (etapa `op19_adm_masa`).

> **2026-10-01 — hereda el costo de OP-15.** Con la gravedad sin modificar, la masa extra de los cúmulos (y el
> desfase del Bala) es esta materia oscura fría. La cantidad la fija el álgebra y pasa contra Planck, BOSS (perfil de
> w_c) y 46 cúmulos reales (2.32σ con IGIMF, `cumulos_zhang2026.json`); **qué es** sigue abierto aquí. Por eso no se
> puede decir «SSEE no necesita partículas» sin esta OP.

> **2026-10-01 — PLAN DE BÚSQUEDA DE MECANISMO (decisión de Mike).** A diferencia de la partícula retirada, que
> tapaba un hueco que resultó no existir, aquí la relación **ya funciona** (Planck, BOSS, 46 cúmulos): el
> mecanismo tiene que **encajar debajo de ella sin dañar nada más**. Se buscan mecanismos con el blanco conocido,
> intentando derribar cada uno.
>
> **Hipótesis de trabajo de Mike (no es resultado):** n_s = 1 − 2/N_* mide qué tan cerca del final de la caída
> del inflatón se estamparon nuestras escalas. ω_c/ω_b = KAL₀·n_s = KAL₀·(1 − 2/N_*) diría que la retención no
> llega completa porque la caída no había terminado. Huecos declarados: (i) en la fórmula la inclinación
> *reduce* la retención, no se le opone; (ii) falta el puente físico entre la época de la caída (inflación) y la
> de la retención (abundancia de materia oscura). Candidata natural: producción de materia oscura al final de
> la caída (recalentamiento / producción gravitacional).
>
> **Reglas, escritas ANTES de probar el primer candidato:**
> 1. Cero perillas ajustadas al blanco: KAL₀·n_s tiene que salir de la física del mecanismo. Todo número que no
>    salga del álgebra cuenta como libre; si se elige para acertar, el mecanismo queda descartado.
> 2. Debe predecir algo más, medible y que hoy no sepamos (masa, temperatura o free-streaming de la materia
>    oscura —KiDS, Lyman-α—, isocurvatura en el CMB…), y no romper nada de lo que ya pasa.
> 3. Control R53: alimentado con blancos falsos (otro cociente, otro n_s), el mecanismo tiene que FALLAR.
> 4. Capa 1 antes que capa 2: explicar por qué ω_c ∝ ω_b (origen compartido con la bariogénesis, OP-1).
>
> **Primer paso (barato, sin corridas):** criba en papel de las cuatro familias (freeze-out, freeze-in,
> misalignment, producción gravitacional / en el recalentamiento). Se busca en cuál la abundancia contiene de
> forma natural N_* o la pendiente de la caída, para que (1 − 2/N_*) aparezca sin insertarlo. Si ninguna lo
> contiene, eso también es resultado: el factor n_s pediría física nueva. Nova aporta los artículos que
> conectan con esto o podrían refutarlo.

**Origen.** Tras el reframe $\omega_m$-directo (OP-8 disuelto), la densidad de materia
oscura fría del CMB entra por la **identidad forward**
$$\omega_c = \mathrm{KAL_0}\cdot\omega_b\cdot n_s = 5.5214\times0.02242\times0.96556 = 0.11951,$$
que junto a $\omega_b$ (OP-1) y $\omega_\nu$ da $\Omega_{m,\mathrm{CMB}}=\omega_m/h^2=0.30889$
(**0.88σ** de Planck 2018). Hoy es una **relación observada que ajusta**, sin una acción de
la que se **derive**. Una auditoría externa (2026-07-12) la señaló como el residuo teórico
para nivel PRD. Esta OP fija la pregunta correcta.

**La pregunta NO es "solo escribir un Lagrangiano".** Son **dos capas**, y la segunda es la
difícil:

1. **¿Por qué $\omega_c$ debe ser proporcional a $\omega_b$?** En ΛCDM, $\omega_b$ y
   $\omega_c$ son **dos parámetros libres independientes**. El cociente $\omega_c/\omega_b
   \approx5.3$ es la célebre *coincidencia cósmica* (¿por qué la materia oscura es solo
   $\sim5\times$ los bariones, y no $10^5\times$ ni $10^{-5}\times$?), que el modelo estándar
   **deja sin explicar**. SSEE afirma que ese cociente **no es libre**:
   $\omega_c/\omega_b = \mathrm{KAL_0}\cdot n_s\approx5.33$. Esto es una afirmación física
   **real y no trivial** sobre la razón barión–materia oscura. Requiere un **origen
   compartido**: el proceso que fija la abundancia de bariones (bariogénesis, OP-1) debe
   ser el mismo que fija la abundancia de la materia oscura fría. La proporcionalidad **es** el
   contenido físico.

2. **¿Por qué la constante es exactamente $\mathrm{KAL_0}\cdot n_s$?** Esta es la parte que
   necesita el cálculo de producción (freeze-out / freeze-in / misalignment / producción
   gravitacional): un escenario cosmológico en el que la abundancia relic de la materia oscura fría
   salga proporcional a la bariónica **con coeficiente $\mathrm{KAL_0}\cdot n_s$**, sin
   insertarlo a mano. $\mathrm{KAL_0}=\beta+\pi$ es la retención estructural (transporte);
   $n_s$ es el índice espectral (la inclinación del espectro primordial). Que el transporte
   $\times$ la inclinación fijen la abundancia oscura es una hipótesis de mecanismo, no una
   identidad de simetría de la acción.

**Por qué es OP-19 y no parte de OP-7/OP-8.** OP-7 (ítem 3) pregunta por qué la QFT en la
escala de Planck reproduce las **asignaciones de rol** ($\mathrm{KAL_0}$ vs AURA, dualidad
$\varphi\leftrightarrow\pi$); OP-8 quedó **disuelto** (la $\Omega_m$ del CMB sale directa,
sin factor materia). OP-19 es más específica y más física: el **mecanismo de abundancia
relic** que produce el coeficiente. Liga fuerte a **OP-1** (origen de $\omega_b$ /
bariogénesis, $\delta_{CP}=(\pi-\varphi)/\Omega$, $T_{\rm rh}\sim10^{-4}$ GeV — **ese mecanismo quedó EXCLUIDO 2026-09-08**) porque un
origen compartido barión–DM es el camino natural a la capa 1.

**Su garantía HOY (falsabilidad, como OP-9 con $k_{fs}$).** La relación ya es una
**predicción forward de cero parámetros** que enlaza dos números medidos: dado
$\omega_b$ y $n_s$, $\omega_c$ **está fijo**. Si datos futuros de CMB/BBN mueven
$\omega_c/\omega_b$ fuera de $\mathrm{KAL_0}\cdot n_s$ más allá del error, la relación se
**falsa**. No me apoyo en la estadística del coeficiente; me apoyo en que la relación es un
candado medible. La **derivación** (esta OP) es el mecanismo; la **relación** ya es una
predicción bloqueada a 0.88σ.

**Consecuencia si permanece abierto.** El sector materia del CMB descansa en que $\omega_b$
(OP-1) y esta identidad sean correctos — no es una perilla nueva (no se ajustó a Planck; es
forward), pero **tampoco es una derivación desde una acción**. Un referee de PRD puede
aceptarlo como relación fenomenológica predictiva y falsable, no como primeros principios.

**Programa de cierre (largo plazo, no garantizado).** (a) Proponer el canal de producción
de la materia oscura fría ligado a la asimetría bariónica de OP-1; (b) mostrar que la abundancia relic
resultante lleva el prefactor $\mathrm{KAL_0}\cdot n_s$; (c) conectar con la
UV-completion (OP-10) y la dualidad de transporte (OP-7). Es frontera abierta de la misma
clase que OP-1/OP-9: puede no cerrar con los recursos actuales, y eso está declarado.

**REFUERZO 2026-09-08 — la identidad cae MÁS CERCA del dato de estructura que
el valor de Planck.**

El perfil de `ω_c` en BOSS DR12 (§`par:wc-profile` de Paper 6) pregunta lo
simétrico de lo ya sabido: con la amplitud clavada, ¿qué `ω_c` pide una
encuesta de galaxias a `z≈0.5`? Con cada modelo en su propia amplitud:

| modelo | `ω_c` que pide BOSS | su referencia | distancia |
|---|---|---|---|
| SSEE | 0.117450 ± 0.004079 | `KAL₀·ω_b·n_s` = 0.119514 | **0.51σ** |
| ΛCDM | 0.114346 ± 0.004041 | Planck 0.1200 | 1.40σ |

*(Re-corrido 2026-10-01 con minimización robusta; fuente `results/logs/perfil_wc_boss*.json`.)*

**El `ω_c` que sale de φ y π queda más cerca de lo que pide el dato de
estructura que el que Planck ajusta dentro de ΛCDM.** No estaba buscado, y es
un argumento **independiente del CMB**: hasta ahora la identidad sólo se había
confrontado con Planck (0.08σ). Ahora también con clustering de galaxias, que
es otra época, otro sistemático y otro instrumento.

Control (R53) pre-registrado en el script y pasa: al devolverle a cada modelo
su propia amplitud, `ω_c` vuelve hacia su referencia (SSEE 1.74σ→0.51σ; ΛCDM
2.27σ→1.42σ), luego el perfil mide el dato y no el borde de la
parametrización. Logs: `results/logs/perfil_wc_boss.log` y
`perfil_wc_boss_lcdm.log`. Informes: `BANDEJA/2026-09-08_perfil_wc_boss*.md`.

**Lo que NO dice.** No es una derivación, sigue siendo una identidad observada
que ajusta. Y el χ² con `ω_c` libre **no se cita**: en SSEE ese parámetro está
fijo por álgebra, así que soltarlo saca al modelo de sí mismo.

**ANOTACIÓN FECHADA 2026-09-08 — la premisa de números iguales y su masa.**

La vio Mike razonando en voz alta, y llega al mismo sitio que un programa publicado
(*asymmetric dark matter*). Si en vez de leer $\omega_c/\omega_b=5.3312$ como «hay 5.33
veces más», se lee como «hay **la misma cantidad** y cada una pesa 5.33 veces más»,
entonces la razón de pesos deja de ser una abundancia y **es una razón de masas**:

$$m_{\rm DM} = \mathrm{KAL_0}\cdot n_s\cdot m_{\rm barión} = 5.331239\times0.937103\ \mathrm{GeV} = \mathbf{4.996\ GeV}$$

La densidad crítica, el $h^2$ y todas las unidades **se cancelan** en el cociente: la
fórmula final tiene tres factores y nada más. `m_barión = 0.937103 GeV` es la masa media
por barión del universo (75% H + 25% He + electrones), **no** la del protón (0.938272,
0.12% distinta). Control de la cadena de conteo: $n_b=2.5207\times10^{-7}\,\mathrm{cm^{-3}}$
da $\eta=n_b/n_\gamma=6.137\times10^{-10}$ contra el publicado $6.12\times10^{-10}$
(+0.28%, que es el +0.21% al que nuestro $\omega_b$ está de Planck). Script:
`src/verificacion/cajones_algebra.py` → `results/logs/cajones_algebra.json` (2026-10-02; el original vivía en un
scratchpad que ya no existe; rehecho con CODATA cambia el último dígito de $m_{\rm barión}$ y de $n_b$).

**Qué es de SSEE y qué no, en ese 4.996:**

| pieza | origen |
|---|---|
| $\mathrm{KAL_0}$, $n_s$ | SSEE, algebraicos |
| $m_{\rm barión}$ | externo, **medido** en laboratorio (entra limpio: escala medida, no ajuste) |
| $n_{\rm DM}=n_b$ | **PREMISA** — ni medida ni derivada |

**Lo que la premisa vale y lo que no.** Explica la coincidencia cósmica de un golpe: sin
ella, que el cociente caiga cerca de la unidad queda medido pero sin explicar. Pero incluso
dentro del programa asimétrico la predicción es $n_{\rm DM}/n_b=\mathcal{O}(1)$, no
exactamente 1, así que la predicción honesta de esta línea es **«unos pocos GeV»**; el
cuarto decimal es precisión falsa mientras el cociente de cantidades no esté fijado. Toda
la tarea se reduce entonces a **un solo número adimensional**, que es exactamente la clase
de objeto que SSEE produce.

**Estado del puente (revisado 2026-09-08).** $\delta_{CP}=(\pi-\varphi)/\Omega=0.3201$ es
**única y estructural** — no está pegada a ninguna especie, es la proyección de la
separación $\pi-\varphi$ sobre $\Omega$. Esa mitad sirve. La otra mitad **no existe**: la
ruta que convierte esa asimetría en materia es esfalerónica, y el esfalerón sólo actúa
sobre partículas del Modelo Estándar. Haría falta un **operador de transferencia** entre
sectores, que SSEE no tiene y que no puede tener mientras el sector oscuro no tenga ningún
objeto al que colgárselo. Y por encima de todo eso: el mecanismo Sakharov de OP-1 quedó
**EXCLUIDO por tres cotas** el mismo día (ver OP-1), así que la ruta ni siquiera llega a
los bariones. Construir el puente ahora sería construir sobre una máquina que no arranca.

**Qué mediría esto.** La cizalla es **ciega** a una partícula de esta masa: su escala de
free-streaming caería en $k_{\rm fs}\sim9\times10^{7}\,h/$Mpc, unas $10^{7}$ veces más allá
de lo que KiDS mide ($k\sim0.1$–5). Eso es bueno (no hay conflicto con $S_8$, $f\sigma_8$ ni
con R3) y es malo (la prueba que mató a la partícula **retirada** de 40.70 eV — histórica,
no vigente desde 2026-08-01 — no puede testear ésta). La
única prueba real es un detector directo. **Y esto NO reabre la retracción del 2026-08-01:**
aquélla era un sector EXTRA definido por una resta no física; ésta no añade materia a nada,
dice de qué está hecho el $\omega_c$ que el CMB **ya** confirma a 0.08σ.

**Cómo atacarlo — plan concreto para retomar EN FRÍO (imagen mental primero).**
La relación se lee: *materia oscura = bariones × (transporte $\mathrm{KAL_0}$) × (inclinación
del espectro $n_s$)*. El $n_s$ es la pista: es una propiedad del **espectro primordial**, así
que si aparece en la abundancia de DM es porque esa abundancia **hereda las mismas semillas**
que todo lo demás → **origen compartido** (cogénesis), no dos procesos separados.

> 🔴 **RETIRADO 2026-08-01.** La partícula φ-DM y el segundo sector fueron retirados: `Ω_φDM` salía de restar una densidad medida menos `1+w₀`, que es un número de la ecuación de estado. **Canónico hoy:** un solo sector, `Ω_m=0.308881`. Contra KiDS-1000 crudo con `A_s` libre, `S₈=0.7559 ± 0.0189` (0.10σ). Y contra **KiDS-Legacy con `A_s` CLAVADO al del CMB** —cero libres cosmológicos— `S₈=0.8273` predicho vs `0.8265±0.0176` medido (0.04σ), χ²=417.97/357 (2026-09-20; KiDS-Legacy es de 2025-03-25, dieciséis meses anterior: no se reclama prioridad). Lo de abajo es histórico.
~~El truco que lo hace atacable (misma jugada que OP-17/$k_{fs}$): **$m_\phi=40.70$ eV ya
está fijo** (forward), así que casi no queda libertad.~~ *(Histórico: retirada la partícula,
la palanca que lo hacía atacable ya no existe; el blanco ω_c/ω_b = 5.331 sí sigue en pie.)* Cada mecanismo de producción tiene una
fórmula de abundancia $\Omega_{\rm DM}(\text{params})$; con los params ya clavados, **cada
mecanismo predice un número** para $\omega_c/\omega_b$, y solo hay UNO que valga:
$$\omega_c/\omega_b = \mathrm{KAL_0}\cdot n_s = 5.5214\times0.96556 = 5.331.$$
Todo el problema colapsa a: *¿qué mecanismo da exactamente 5.331 sin meterlo a mano?*

Pasos (papel + `op19_omega_c_mechanism.py`, factible en hardware actual):
1. **Blanco:** target = número puro `ω_c/ω_b = 5.331`.
2. **Mapa:** las ~4 rutas de producción de un bosón ligero — *misalignment* (tipo ALP/axión),
   *freeze-in*, *producción gravitacional*, *cogénesis/ADM* — con su fórmula de abundancia.
> 🔴 **Histórico:** el filtro descrito usaba `m_φ=40.70 eV`, retirado el 2026-08-01. El método (fijar una cantidad y ver qué predice cada fórmula) sigue siendo válido; la cantidad concreta, no.
3. **Filtro** *(histórico)*: meter el retirado $m_\phi=40.70$ eV fijo en cada fórmula → cada una predice un
   $\omega_c/\omega_b$; comparar con 5.331. Los que fallan por órdenes de magnitud mueren.
4. **Veredicto:** si sobrevive uno → derivar $\mathrm{KAL_0}\cdot n_s$ de su Lagrangiano (= el
   paper). Si ninguno → resultado igual: no es relic estándar → empuja al origen primordial
   compartido, liga OP-1/OP-18.

**Referee honesto (cuenta gruesa ya hecha):** ADM con asimetrías iguales **NO cuadra** para
40 eV — daría una razón de masas $m_{\rm DM}/m_p$, no un número $\sim10^8$ en $n_{\rm DM}/n_b$;
falla por órdenes. La ruta viva es **misalignment/cogénesis** (donde $n_s$ tiene hogar
natural), sin probar. Frontera real.

**Declaración de honestidad — la ventana de identidad del tercer factor (2026-07-12).**
El ajuste fija el tercer factor a la ventana $[0.960,\,0.979]$ ($\pm1\sigma$ Planck en torno
a $\omega_c=0.1200\pm0.0012$), un ancho de solo $\sim2\%$. **Cualquier** cantidad física en
esa ventana reproduciría $\omega_c$ igual de bien: **el dato identifica un número
($\sim0.965$), no una identidad.** Por tanto **NO** es correcto afirmar como hecho "el tercer
factor es $n_s$"; $n_s$ es el **candidato líder**, no una certeza. Verificación numérica
(`op19` inline): $n_s=1.0\to+3.2\sigma$, $n_s=0.99\to+2.1\sigma$, $n_s=0.9656\to-0.4\sigma$
— el factor es **load-bearing** (sin él, $3.2\sigma$), no decoración.

Lo que eleva a $n_s$ por encima de un $0.973$ arbitrario **NO es su valor** (eso es
degenerado dentro de la ventana) sino **dos** propiedades que un número inventado no tendría:
(a) **anclaje independiente** — Planck lo **mide** ($0.9649\pm0.0042$) y $\varphi^{-7}$ lo
**deriva** ($0.96556$), y coinciden; (b) **doble función** — es observable primario del CMB
y del sector inflación (OP-2), no un número acuñado para esta relación. Es el mismo criterio
que legitima a $\mathrm{KAL_0}$ (carga peso en el EFT, no solo aquí). **El discriminador real
entre candidatos de la ventana = este doble-deber + el mecanismo:** un cálculo de producción
(cuerpo de OP-19) escupiría UNA cantidad específica, y ahí se sabría cuál es. Hasta entonces,
lo honesto es **declarar la ventana** y llamar a $n_s$ *hipótesis-de-identidad-motivada*, no
identidad probada.

**Matiz (no es parámetro libre).** Un parámetro libre se ajustaría al centro **sin ancla**;
aquí el valor está pinchado desde afuera (Planck + $\varphi^{-7}$) y la ventana es una
**restricción**, no una perilla. La libertad que sí queda es **combinatoria** (qué cantidad
de la ventana, y por qué el producto $\mathrm{KAL_0}\cdot\omega_b\cdot n_s$ y no otro) —
la misma "libertad de gramática" fichada en el multiplicador de la partícula (§numerología).
Cerrarla = OP-19.

**Severidad:** Media-Alta — es el residuo teórico del sector materia para nivel PRD. No
falsa SSEE (la relación es forward y falsable), pero cerrar el mecanismo es lo que la
llevaría de "relación predictiva" a "derivación desde una acción".
**Relación:** OP-1 (✅ parcial, $\omega_b$/bariogénesis), OP-7 (dualidad de transporte),
OP-8 (disuelto), OP-10 (UV). Script a crear: `op19_omega_c_mechanism.py` (exploratorio).

---

## OP-20 — El factor `0.960318` no tiene fuente (histórico, ya retirado del cálculo)

**Estado:** CERRADO en el código (2026-07-25), ABIERTO como registro de procedencia.

**Qué es.** Hasta 2026-07-25 la cadena del neutrino se escribía
`Σm_ν^active = R₂ · 0.960318 eV`. Ese `0.960318` es dimensional (eV) y nunca
tuvo derivación documentada.

**Qué se verificó.** Si se lo lee como `ω_b · C_ν / τ_Π`, el C_ν implicado es

    C_ν = 0.960318 · τ_Π / ω_b = 93.8638 eV <!-- R74: git:7866edc8ef:CANONICAL_VALUES.yaml -->

que **no es ninguno de los dos valores documentados**: ni 94.07 eV (desacople <!-- R74: git:7e7e6f98f8:src/ssee_core.py -->
instantáneo, N_eff=3) ni 93.14 eV (Mangano+2005 / PDG, N_eff=3.046). Es un
tercer valor sin origen. Las notas previas que lo describían como «C_ν=94.07 <!-- R74: git:7e7e6f98f8:src/ssee_core.py -->
horneado» eran **incorrectas** (94.07 daría 0.962428) y se corrigieron. <!-- R74: git:7e7e6f98f8:src/ssee_core.py -->

**Por qué importaba.** C_ν aparece arriba (cadena SSEE de Σm_ν) y abajo
(conversión ω_ν = Σm_ν/C_ν), así que **se cancela**: ω_ν es INVARIANTE bajo la
elección de C_ν. El único modo de obtener un ω_ν distinto era usar valores
distintos en los dos lados — que es exactamente lo que ocurría (0.960318 arriba,
93.14 abajo), dando ω_ν = 0.000741 en vez de 0.000735 (0.78%).

**Resolución.** La cadena se escribe ahora explícita, `Σm_ν = R₂·ω_b·C_ν/τ_Π`
con C_ν = 93.14 eV en ambos lados, y la cancelación se cumple. Vigilado por
V-L2-11a/b/c.

**Residuo abierto.** No se sabe de dónde salió el 93.86. Puede haber sido una
constante de una versión intermedia de la relación relic, un ajuste, o un error
de transcripción. Se registra porque el modelo no debe contener números sin
origen, aunque estén retirados: el registro histórico también tiene que ser
trazable.

**Lección de método.** El valor sobrevivió porque su efecto era invisible
(0.004% en ω_m) y porque quien lo revisó aceptó una explicación plausible
—«es C_ν viejo»— sin comprobar la aritmética. Comprobarla toma una división.

---

## OP-24 — Ningún fondo reproduce $w_a = -0.669975$ — 🟡 **ABIERTO (2026-09-07)**

**Por qué se abre ahora.** OP-23 preguntaba si algún `β_c` del acoplamiento
conformal daba `w₀` sin exceso de energía oscura temprana, y quedó **cerrado
por disolución** al retirarse el acoplamiento de Paper 7. Pero al disolverse
se llevó por delante la etiqueta de una pregunta **distinta** que sigue viva y
que se venía citando como «OP-23» sin serlo. Se le da número propio.

**La premisa** (lo que habría que tumbar para disolverlo): que `wₐ` deba salir
del fondo escalar. Si `wₐ` fuera un parámetro de *ajuste* del observador —una
propiedad de la parametrización CPL y no del campo— la pregunta desaparece.
Mientras se sostenga que SSEE **predice** `wₐ = -P_sc/K_v = -0.669975`, hay
que enseñar el fondo que lo produce.

**Lo medido, no lo argumentado:**

| fondo | `wₐ` |
|---|---|
| atractor | `-0.093` |
| `λ = 1.0205` | `-0.211` |
| acoplado | `+0.408` (signo contrario; `fondos_exponenciales.json`) |
| **objetivo algebraico** | **`-0.669975`** |

Ninguno se acerca, y el acoplado va en dirección opuesta.

**Por qué no se cierra con la prueba barata:** ya se corrió. El barrido en
`β_c` y el fondo autoconsistente están en
`archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/`; el resultado fue
que el problema **no es el acoplamiento** sino la **forma del potencial**.

**Qué lo cerraría:** un `V(φ)` derivado de `φ,π` cuyo fondo integrado devuelva
`wₐ = -0.669975`; o la demostración de que `wₐ` no es una predicción del
fondo. Investigación viva: `src/p07_eft/busca_lambda.py`,
`fondo_viscoso.py`, `resuelve_op23.py`.

**Riesgo si permanece abierto:** `wₐ` es la mitad del titular `w₀wₐ` frente a
DESI DR2. Que el valor cuadre con el dato pero no salga de ningún fondo
integrado es exactamente el tipo de cosa que un referee llama ajuste.

**Acotado 2026-09-27 — quién puede llevar el cruce fantasma** (pregunta de
Mike: P1 decía «el cruce no es inestable», P7 «c_s² cambia de signo»; ver cuál
es cierta). Script `src/p07_eft/cruce_fantasma_quien_lo_lleva.py`, log
`results/logs/cruce_fantasma_quien_lo_lleva.json`; los dos controles pasan
(w(u0)=w0 y c_s²=0.021284 de P7 recuperados; c(a*)=1 exacto).
- **El campo NO puede.** Con K = c1X + c2X², derivando K por diferencias
  finitas, los 10 puntos del barrido con w < −1 tienen c_s² < 0 (0 de 10 con
  c_s² > 0). P7 tenía razón; la frase de P1 estaba mal y se corrigió.
- **Si el cruce es físico, lo lleva la viscosa Π.** Con la normalización de
  OP-22 (Π ∝ ρ+p): 1+w_eff = (1+w0)(1−c), c = |Π|/(ρ+p), y el CPL exige
  **c(a) = −wₐ(1−a)/(1+w0) = 4.186(1−a)**: c = 1 exacto en z* = 0.314,
  2.09 en z = 1, 2.93 en z = 2.33.
- **La prueba que decide:** si |Π| > ρ+p cae dentro de la validez de
  Israel–Stewart. Si no cae, la vía viscosa también se cierra y wₐ tendría que
  salir de otro sitio. Es la siguiente pregunta de este OP.

## OP-23 — Dentro del acoplamiento conformal, ningún $\beta_c$ da $w_0$ sin pasarse de energía oscura temprana — ⚫ CERRADO POR DISOLUCIÓN (2026-09-06)

> ## ⚫ DISUELTO AL DÍA SIGUIENTE — cayó su premisa, y cayó entera
>
> **La premisa nombrada en §2 era: «el acoplamiento campo↔materia oscura es
> CONFORMAL».** El OP anticipaba que podría ser disformal, y que entonces se
> disolvería. Lo que pasó es más fuerte: **no hay acoplamiento de ningún tipo.**
> La acción de Paper 7 quedó en
> ```
> S = int [ Mpl^2/2 R + c1 X + c2 X^2 + L_m ]
> ```
> sin potencial y sin acoplamiento. Tres resultados independientes lo forzaron:
>
> 1. **El «0.199 % de acuerdo con AURA» era el bug de normalización.** El
>    disparo calibraba $\Omega_\phi(a{=}1)$ a **0.839950**, que es $|w_0|$ —una
>    cantidad de la ecuación de estado— donde va la fracción de densidad
>    **0.691119**. Con el objetivo correcto sale $\beta_c=+0.235068$: signo
>    contrario y factor 17.
> 2. **Cota independiente del sector frío.** Cualquier $|\beta_c|\gtrsim0.027$
>    aparta $\omega_c$ de su identidad forward $\mathrm{KAL}_0\,\omega_b\,n_s$
>    más que su error de Planck. AURA es **151×** esa cota.
> 3. **Ningún número publicado dependía de $\beta_c$:** no está en
>    `CANONICAL_VALUES.yaml` ni lo usa ningún script de producción.
>
> **Lo que ocupó su lugar es más de lo que se fue.** Sin potencial ni
> acoplamiento, $K(X)$ tiene que sostener $w_0$ solo, y eso deja ver un
> **teorema**: para $K=A X^n$ se cumple $w_\phi=c_s^2=1/(2n-1)$ *idénticamente*,
> así que acelerar implica $c_s^2<0$. Ningún k-essence de un término puede
> acelerar y ser estable. Con dos términos, $u=c_2X/c_1$ queda fijo por $w_0$:
> ```
> u     = -(M_v+T_r)/(3T_r+M_v) = -0.522735380747
> c_s^2 = (M_v-T_r)/(5M_v+3T_r) = +0.021283701571
> ```
> y los signos exigen $c_1<0$, $c_2>0$: **condensado fantasma**, estabilizado en
> $X/X_{\min}=1.045471$. Verificado con `hi_class` (commit `0009f51`):
> $c_s^2$ a **0.000 %**, $\alpha_K$ a **0.011 %**, acepta el modelo y rechaza
> los cuatro controles.
>
> **Lo que este cierre NO resuelve:** de dónde sale $w_a$. En el punto del
> condensado $w_\phi$ es constante, así que la acción da $w_a=0$. El
> $w_a=-P_{sc}/I_g$ viene de la viscosidad IS, cuya amplitud quedó cerrada el
> mismo día ($\Gamma=P_{sc}/(3I_g)$, dif $0.00\mathrm{e}{+}00$) pero cuyo
> *ansatz* sigue siendo **OP-22**. Es ahí donde vive ahora el hueco.
>
> <details><summary>Texto del OP mientras estuvo abierto (conservado)</summary>

> ## ✅ SUSPENSIÓN LEVANTADA EL MISMO DÍA — el barrido SÍ usaba el Lagrangiano correcto
>
> **Mike, de memoria:** *«estoy seguro que los dos M no son lo mismo… esos dos
> Lagrangianos se usaban para derivar H global con SH0ES y f_screen completo,
> IR y UV»*. **Tenía razón en las dos cosas, y mi suspensión estaba mal.**
>
> No hay colisión de símbolo: hay una **jerarquía declarada**.
> ```
> P7  IR   M^4 = rho_crit    CONVENCION
>          (P7 tex L169-173 lo dice: "a working
>           convention, NOT an algebraic
>           determination of M")
> P10 UV   M^4 = 5phi^8 rho_c = 234.8936
>          el valor FISICO, derivado (L66, L135)
> P8       M ~ M_Pl, otro regimen
> ```
> **El bug era usar la CONVENCIÓN para calcular un β_c FÍSICO.** Con
> $M^4=1$ el término $X^2/M^4$ pesa 20.5 % del lineal; con el $M^4$ físico pesa
> **0.34 %** — despreciable, tal como afirma Paper 7. *(Corregido: primero cité
> 0.087 %, calculado con la solución vieja; con la solución del $M$ físico
> —$\dot\phi=0.540727$, $X=0.146193$— sale 0.34 %.)* Medido: <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
> ```
> M4 = 1 (convencion)  w -0.972562  b_c -2.194210 <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
> M4 = 5phi^8 (fisico) w -0.922851  b_c -0.691265 <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
> fondos K = X/KAL     w -0.927318
> ```
> La brecha de 0.045 cae a **0.0045**. ⟹ `fondo_acoplado` y `fondo_disparo`, que
> implementan $K(X)=X/\KAL$ a secas, **son correctos**, porque a $M$ físico el
> término no lineal no cuenta. **El barrido fino probaba el Lagrangiano bueno y
> OP-23 sigue en pie.** Corregido en `ssee_eft_verification.py:84`.
>
> Y la conexión que Mike recordaba es real: los dos Lagrangianos son el IR y el
> UV, y son los que dan $\alpha_K=0.4033$ / $\alpha_K^{\rm full}=0.41691$, de ahí
> $f_{\rm screen}$ IR/UV y los dos $H_{\rm glob}$ (68.13 con el IR solo, que es
> el resultado **parcial**; 67.962142 con el completo, que es el canónico). La corrección
> UV es del 3.4 % — subdominante, coherente con todo lo anterior.
>
> <details><summary>Texto de la suspensión errónea (conservado)</summary>
>
> 🟠 **SUSPENDIDO HORAS DESPUÉS DE ABRIRSE. LA EVIDENCIA NO LO SOSTIENE.**
> Mike preguntó de dónde salía cada uno de los tres valores de $w$ que yo le
> daba, *«porque puede que se parezcan y no sea lo que señala»*. Tenía razón.
>
> **El barrido corrió con el Lagrangiano equivocado.** `archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/fondo_acoplado.py` y
> `fondo_disparo.py` implementan $K(X)=X/\KAL$ **y nada más** — no contienen el
> término $X^2/M^4$ en ninguna línea. Paper 7 declara
> $K(X)=X/\KAL+X^2/M^4$ (tex L55, L162). El barrido probó una **truncación IR**,
> no el modelo de Paper 7.
>
> **Y el término que falta NO es despreciable para el fondo.** Medido apagándolo
> en `archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/ssee_eft_verification.py` (el único de los tres que sí lo implementa):
> ```
> con X^2/M^4   w_phi = -0.972562   beta_c = -2.194210 <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
> sin X^2/M^4   w_phi = -0.921054   beta_c = -0.666255 <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
> ```
> Mueve $w$ en **0.0515**, y la brecha que este OP intenta cerrar es 0.087. Es el
> 59 % de lo que está en juego. En $K_X$ —que fija $\rho+p$ y por tanto $1+w$—
> el término no lineal pesa **41 %** ($X=0.037128$, $X/\KAL=0.006724$, <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
> $X^2/M^4=0.001378$). <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
>
> **Nótese además que $\beta_c$ pasa de $-2.194$ a $-0.666$**, o sea **entra en
> la región $|\beta_c|\le0.8$ donde el barrido sí encuentra solución.** La
> conclusión «no hay ningún punto bueno» podría invertirse con el Lagrangiano
> correcto. No se sabe: no se ha corrido.
>
> **Colisión de símbolo detectada de paso:** Paper 7 L170 declara
> $M^4\equiv\rhocrit$ (normalización de fondo), y L177 afirma que $X^2/M^4$ es
> «subdominante» — pero hablando del régimen de gravedad fuerte con
> $M\approx\Mpl$. **El mismo símbolo $M$ con dos valores en el mismo paper.**
> Con $M\approx\Mpl$ el término es nulo; con $M^4=\rhocrit$ pesa el 41 %.
>
> **PARA LEVANTAR LA SUSPENSIÓN:** añadir $X^2/M^4$ a `archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/fondo_acoplado.py` y
> repetir el barrido fino. Sólo entonces se sabrá si el problema existe.
>
> </details>
>
> **Lo que SÍ queda establecido:** $\beta_c=-\mathrm{AURA}$
> está retirado (ver «Lo que este OP RETIRA» abajo, que se apoya en el bug R52,
> no en el barrido); y las tres implementaciones quedaron reconciliadas —
> `fondo_disparo` interpolado a $a=1$ da $-0.927316$ contra $-0.927318$ de
> `fondo_acoplado` con $\beta_c=0$, diferencia $2\times10^{-6}$: **el integrador
> acoplado se reduce correctamente al no acoplado.** El «0.045 sin explicar»
> del 2026-08-10 queda **explicado: era el término $X^2/M^4$.**

### Contenido original del OP (evidencia con el Lagrangiano truncado)

**Anatomía.** Este OP se abre siguiendo el criterio que Mike formuló el
2026-09-05: un problema no se declara abierto hasta que se ha comprobado que
*hoy* no se puede cerrar. Las cinco piezas obligatorias van explícitas abajo.
La segunda —**la premisa**— es la que faltaba en OPs anteriores: OP-8, OP-9 y
OP-14 no se resolvieron, se **disolvieron**, porque su premisa era falsa. Un OP
sin premisa nombrada no se puede disolver, sólo se puede chocar contra él.

### 1. POR QUÉ se abre — el hecho medido  ⭐ **RAZÓN DEFINITIVA (2026-09-05)**

> **El $\beta_c$ que da $w_0$ parte por la mitad la materia en recombinación.**
> ```
> omega_m ACOPLADO (b_c=+0.235068)  0.06900
> omega_m SSEE algebraico           0.14267
>                                    -51.6%
> ```
> La vara es **la propia predicción de SSEE**: $\omega_m=\omega_b+\omega_c+\omega_\nu
> =0.14267$, la que da $\chi^2_{\rm CMB}=1003.586$ y $\Delta$BIC$=-26.03$ en Paper 3.
> Medido sobre `results/logs/fondo_acoplado.npz` en $a=0.001$:
> $\rho_m/\rho_{c,0}$ acoplado $\approx1.5\times10^8$ vs estándar $\Omega_m(1+z)^3\approx3.1\times10^8$,
> razón $\approx0.48$. Equivalente: $E(z{=}999)$ va **≈ −30 %** por debajo. *(Re-medido 2026-10-02 sobre el
> mismo npz: 0.484 y −30.4 %; las cifras de 4 dígitos de antes no se reproducen, y el npz está ignorado
> por git, así que sólo se sostiene el redondeo.)*
>
> **Física:** para arreglar $w_0$ hoy, el acoplamiento tiene que haber drenado
> materia oscura hacia el campo toda la historia ⟹ temprano había mucha menos.
> El CMB ve cuánta había. **El acoplamiento conformal arregla Paper 7 rompiendo
> Paper 3.**
>
> ⚠️ **ESTO REEMPLAZA EL CRITERIO ORIGINAL, QUE ERA INVÁLIDO.** El
> `LIM_EDE = 0.03` de `barrido_beta_c_fino.py:39` **no tiene fuente: lo escribí
> yo**, no está en `CANONICAL_VALUES.yaml`, ningún paper lo cita, y compara la
> cantidad equivocada en la época equivocada (lo comparable en la suite es
> Paper 9 L677, $f_{\rm EDE}\sim0.1$ cerca de la igualdad $z\sim3000$–5000; yo
> usaba $\Omega_{\rm DE}(z{=}9)$, en plena dominación de materia). Contra H(z)
> crudo el fondo acoplado **NO se excluye**: su χ² quedaba a la par del estándar. *(Esa cuenta usó el
> CSV viejo, con 23 de los 32 puntos de Moresco+2022; no se rehízo porque el fondo acoplado está retirado.)* El umbral inventado hacía todo el
> trabajo. Mike lo cazó preguntando de dónde salía. Ver
> `memory/project_op23_measuring_stick.md`.

### 1b. El hecho original (criterio inválido, conservado por trazabilidad)

El fondo acoplado tiene que cumplir dos cosas a la vez: reproducir
$w_0=-0.839950$ hoy, y no dejar más de $\sim3\%$ de energía oscura en $z=9$.
Barrido fino de 31 puntos en $\beta_c\in[+0.100,+0.245]$
(`archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/logs/barrido_beta_c_fino.log`, script
`archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/barrido_beta_c_fino.py`):

| $\beta_c$ | $w_{\rm eff}(a{=}1)$ | $\lvert w-w_0\rvert$ | $\Omega_{\rm DE}(z{=}9)$ |
|---|---|---|---|
| 0.1000 | $-0.892879$ | 0.052929 | 1.19 % | <!-- R74: git:d849df0ec7:results/logs/barrido_beta_c.log git:d849df0ec7:results/logs/barrido_beta_c_fino.log -->
| 0.1800 | $-0.862144$ | 0.022200 | **2.99 %** ← frontera | <!-- R74: git:d849df0ec7:results/logs/barrido_beta_c_fino.log -->
| 0.2351 | $-0.839949$ | **0.000001** | **4.53 %** | <!-- R74: git:d849df0ec7:results/logs/barrido_beta_c.log -->

**Ningún punto cumple las dos.** Las dos condiciones se mueven en sentidos
opuestos y se cruzan en el lado prohibido. Lo mejor que se consigue dentro del
límite observacional es $w_{\rm eff}=-0.862144$, a $0.0222$ de $w_0$. <!-- R74: git:d849df0ec7:results/logs/barrido_beta_c_fino.log -->

*Control del barrido:* incluye $\beta_c=0.1000$ y $0.235068$, que ya tenían
respuesta del barrido grueso, y los **reproduce** ambos. Sin eso, las 29 filas
nuevas no valdrían nada.

### 2. LA PREMISA que sostiene el problema

> **El acoplamiento campo↔materia oscura es CONFORMAL.**

Es lo único que hace falta que sea cierto para que este problema exista. Y es
**testeable, y puede ser falsa**: Paper 8 ya usa acoplamiento **disformal**
mientras Paper 7 usa conformal — la suite no es coherente en este punto. Si el
acoplamiento correcto es disformal, OP-23 no se resuelve: **se disuelve**, como
OP-8 y OP-9.

### 3. QUÉ PRUEBA lo resolvería

Rehacer el fondo acoplado con acoplamiento disformal y repetir el barrido. Si
aparece un punto que cumpla las dos, el OP cierra por disolución de su premisa.

### 4. QUÉ HERRAMIENTA falta hoy

El integrador disformal. `archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/fondo_acoplado.py` implementa **sólo** el
conformal ($\beta_c$ entra en Klein–Gordon y en la conservación de la materia
oscura). El término disformal cambia la estructura de las ecuaciones, no un
coeficiente: no se obtiene ajustando nada de lo que hay.

*Por eso es un OP y no una tarea.* La alternativa barata —el barrido fino— **ya
se corrió**, y por eso este OP se abre con el hueco cerrado detrás.

### 5. CÓMO SE SABRÁ que cerró

Un punto con $\lvert w_{\rm eff}-w_0\rvert<0.005$ y $\Omega_{\rm DE}(z{=}9)<3\%$
simultáneamente. Si el barrido disformal tampoco lo encuentra, el resultado deja
de ser un OP y pasa a ser una **predicción falsable**: SSEE no admite
acoplamiento oscuro, $\beta_c=0$.

### Qué NO dice este OP

- **No dice que $\beta_c$ sea desconocido.** Dice que el conformal no cierra.
- **No compromete la estabilidad.** $c^2_s\in[0.632,0.980]$, positivo en todo el
  rango, tras el fix R52 de 2026-09-05.
- **No compromete $w_0$ ni $\alpha_K$.** $w_0=-T_r/M_v=-\mathrm{AURA}/\Omega$ es
  identidad algebraica exacta (diferencia $0.0$ a 40 dígitos) y no pasa por
  $\beta_c$. Con $\beta_c=0$ el fondo da $\alpha_K=0.150696$, que coincide con <!-- R74: git:d849df0ec7:results/logs/barrido_beta_c.log -->
  el $0.150703$ algebraico por vía independiente.

### Lo que este OP RETIRA

$\beta_c=-\mathrm{AURA}$ (Paper 7). Ese valor venía de un despeje **en un solo
punto** que además metía saturaciones en ranuras de densidad. Corregido el bug
(R52, 2026-09-05) el mismo despeje da $-2.194210$, a **45 %** de $-\mathrm{AURA}$: <!-- R74: git:4b90e2e:archive/codigo/investigacion/beta_c_RETIRADO_2026-09-07/reproduccion_2026-10-02.json -->
el «acuerdo al 0.199 %» era el bug. Y el barrido muestra que no hay solución para
$\lvert\beta_c\rvert\ge1.0$, así que $-3.997847$ está cinco veces fuera de la
región donde el fondo acoplado admite solución.

</details>

---

## OP-25 — R44 no mira las celdas de tabla — ⚪ ABIERTO (2026-09-08)

> *(Renumerado de OP-24 a OP-25 el 2026-09-08: el 24 ya estaba ocupado por «ningún fondo reproduce $w_a$», abierto el día anterior. La colisión la creé yo al abrir éste sin mirar la lista.)*

**Severidad:** baja para la física, media para la presentación.

### El hueco

R44 exige *«constante de la lectura con `=` a 6 decimales»*. En una tabla el
valor va solo en su celda, sin signo igual, así que **R44 no ve ninguna tabla**.
Lo destapó un caso de mutación cuyo ancla caía justo ahí: `$9.519253$` cambiado
a `$9.52$` dentro de una celda pasaba VERDE.

### Medida

Barriendo `manuscript/*.tex` y `submission_PRD/*.tex` con el patrón de celda
`& $valor$ &` y el mismo rango de 2 a 5 decimales que usa R44:

| Documento | Sitios | Ejemplo |
|---|---|---|
| Unified Journal | 10 | `& $-0.840$ &` (w₀ a 3 dec) |
| Paper 1 | 8 | `& 4.7596 &` (Ω a 4 dec) |
| Paper 3 | 8 | `& $-0.66997$ &` (wₐ a 5 dec) |
| Paper 4 | 8 | `& 67.96214 &` |
| Paper 5 | 4 | `& 0.309 &` (Ω_m a 3 dec) |
| Papers 10, 2, 9, Sealed, PRD | 3+3+2+2+2 | — |
| **Total** | **50** | — |

### Por qué NO se ensanchó sin decidirlo

Ensanchar R44 a celdas pondría 50 rojos en **diez documentos publicables**, y la
mayoría son tablas de resumen donde redondear es la convención tipográfica, no
un error. La política de redondeo del proyecto (álgebra 12 decimales, modelo 6)
no dice qué precisión debe llevar una tabla de resumen, y decidirlo cambia la
presentación de la suite entera. Es una decisión de autor, no del guardián.

### Las tres salidas

1. **Declarar la precisión en el encabezado de cada tabla** (*«values quoted to
   4 decimals»*) y que R44 lea esa declaración. Es lo que ya hace R41 con
   *«to three decimals»*. Coste: tocar ~14 tablas; ganancia: la regla se vuelve
   universal sin falsas alarmas.
2. **Llevar las 50 celdas a 6 decimales.** Coherente con la política, pero
   ensucia tablas cuyo propósito es leerse de un vistazo.
3. **Dejarlo como punto ciego declarado**, que es el estado de hoy.

**Recomendación:** la 1. Conserva la legibilidad de las tablas, cierra el hueco
de verdad, y la infraestructura para leer una precisión declarada ya existe en
R41. Pendiente de la decisión de Mike.


---

# Residuos de problemas cerrados

Un OP puede cerrarse y dejar algo detrás. Hasta el 2026-09-19 esos restos vivían sólo
dentro del guardián, que los listaba como «abiertos» mientras su ficha decía RESUELTO o
DISUELTO — una contradicción entre las dos fuentes que nadie veía porque cada una se leía
por separado. Ahora cada resto tiene su ficha, su severidad y su criterio de cierre. El
sufijo `b` dice de qué problema es resto.

---

## OP-2b — La Conjetura B.1 (N_* = 2φ⁷) no está derivada — 🟡 ABIERTO (resto de OP-2)

**De dónde viene.** OP-2 cerró el exponente 7 de `n_s = 1 − φ⁻⁷` como **corolario** de la
universalidad α-attractor con `N_* = 2φ⁷`: es la única solución entera en la ventana
[50,60] e-folds. Lo que no cerró es **por qué** `N_*` toma esa forma.

**Lo que falta.** El puente de reheating gravitacional que fije `N_*` sin postular su forma.

**Criterio de cierre.** Una derivación de `N_*` desde la historia de reheating del propio
campo, que no meta `2φ⁷` como entrada.

**Severidad: Media.** `n_s` está confrontado y encaja; lo que falta es el origen, no el valor.

---

## OP-5b — El cierre no lineal pleno de S₈ sigue diferido — 🟢 ABIERTO (resto de OP-5)

**De dónde viene.** OP-5 se **disolvió** el 2026-08-01: con A_s libre no hay tensión S₈ que
resolver (MCMC R3 sobre KiDS crudo, S₈ = 0.7559 ± 0.0189, 0.10σ). Lo que queda no es una
tensión, es un refinamiento.

**Lo que falta.** El régimen no lineal pleno con feedback bariónico (N-body tipo
BAHAMAS / IllustrisTNG adaptadas a SSEE), ~5.000–20.000 horas de CPU.

**Criterio de cierre.** Una corrida N-body propia, o la constatación de que HMcode-2020
basta a la precisión de la próxima generación de datos.

**Severidad: Baja.** No afecta a ningún número publicado y ya no es la vía de rescate de
ninguna tensión — ese encuadre murió con la partícula.

---

## OP-6b — La forma multiplicativa de f_screen es postulado, y su paso δρ_φ con δ_local = 2 no está derivado — 🟡 ABIERTO (resto de OP-6)

**De dónde viene.** El **valor** de f_screen = (π−φ)/Ω² es identidad exacta. La **forma**
multiplicativa H_loc = H_glob/(1−f) se creyó cerrada en OP-6 por el universo separado, pero
ese paso usaba la identidad falsa 1+w₀ = Ω_m. Desde el 2026-10-03 Paper 9 la adopta como
postulado (`eq:screen_postulate`). La variante aditiva difiere en f²·H ≈ 0.31 km/s/Mpc,
por debajo de la incertidumbre actual de SH0ES.

**Lo que falta.** Un mecanismo que dé la forma desde la acción de Paper 7. El viejo paso
también tomaba δ_local = 2 (sobredensidad del Grupo Local) como insumo observacional y
una expresión de δρ_φ asertada, no derivada.

**Criterio de cierre.** Derivar la forma de la acción, o medir la diferencia entre
multiplicativa y aditiva. Las pruebas por profundidad y por métodos de OP-8b
(2026-10-03) no tienen potencia con los datos de hoy.

**Severidad: Media.** Toca el titular de Paper 9 sólo en la forma, no en el valor.

---

## OP-8b — MIRA sigue sin mecanismo dinámico — ✅ CERRADO 2026-10-03 (decisión de Mike: MIRA es constante)

> **CIERRE (2026-10-03, Mike).** MIRA es una **constante**, como cada entidad del álgebra
> SSEE: no cambian. Lo dinámico son sus **funciones**, y al combinarlas dan entidades nuevas.
> No hay, por tanto, una dinámica de MIRA que buscar: los cuatro mecanismos descartados
> (c²_s, Poisson-μ, disforme, retención conformal) buscaban algo que no existe. El álgebra
> produce **razones**; los **mecanismos** las conectan con medidas (SH0ES, el TRGB de CCHP…).
> Lo que sigue abierto es **qué mecanismo produce la razón** f_screen sobre una tasa medida:
> eso es la forma multiplicativa, postulado de Paper 9, y vive en **OP-6b**. (KAL₀ como
> retención tampoco es elección del modelo: ya era así antes.) Todo lo de abajo queda como
> registro de cómo se llegó aquí.


> **2026-10-03 — HIPÓTESIS DE MIKE y su prueba, escritas ANTES de correr nada.**
> **La lectura.** AURA es la «irradiación», el nivel donde solo queda energía o luz. Sus copias
> (ley de copia del diccionario) dan las dimensiones: MIRA = ½AURA, DUAL = 2AURA,
> TRIAL = 3AURA = T_r. La lente NO es MIRA: es la distorsión de esa luz por la masa (RG).
> El apantallamiento de Paper 9 sería una proyección del crecimiento local sobre la medida de H.
> **Lo que el álgebra ya dice (identidades exactas, comprobadas en código):**
> f_screen = s_K/(3·MIRA) = 2(Ω−AURA)/Ω² = (K_v − DUAL)/Ω² = (π−φ)/Ω², con K_v = 2Ω y 3·MIRA = TRIAL/2.
> AURA se cancela. f vive en el nivel 2 de las copias (K_v y DUAL) sobre un área (Ω²), y
> w₀ = TRIAL/M_v en el nivel 3. Esto es lectura de un resultado algebraico: no lo deriva.
> **La prueba (datos: Pantheon+SH0ES, 77 calibradores con distancia Cefeida y 277 SNe del flujo de
> Hubble de SH0ES, 0.023 < z < 0.15, covarianza STAT+SYS completa).** Si el apantallamiento es un
> efecto del VOLUMEN local que se promedia al crecer el volumen, el H₀ que da cada capa de
> profundidad debe BAJAR con z hacia H_glob = 67.962. Si es una propiedad de la escalera de
> distancias (o vive solo en el volumen de los calibradores, < ~40 Mpc), todas las capas dan el mismo H₀.
> Ajuste: M_B común + −5·log₁₀H₀ lineal en z (y aparte, H₀ por cuartiles de z), forma de d_L de cada
> modelo con SUS ingredientes (SSEE: w₀, w_a, Ω_m = 0.308881; ΛCDM: Planck 2018).
> **Criterios, fijados ahora:**
> - **Apoya la versión de volumen:** H₀(z=0.023) − H₀(z=0.15) > 0 a ≥ 2σ.
> - **Excluye la versión de volumen hasta ~600 Mpc:** caída compatible con 0 (< 2σ) y H₀ de la capa
>   más profunda a > 3σ por encima de 67.962. Entonces el apantallamiento, si existe, actúa igual a
>   toda profundidad o solo en el paso de calibración; no es crecimiento local que se promedia.
> - **No concluye:** cualquier otro caso.
> **Controles (R53):** (1) el mismo código con el ajuste de Brout+2022 (ΛCDM plano, SNe con z > 0.01 +
> calibradores) debe dar su H₀ = 73.6 ± 1.1 publicado, con tolerancia 0.3; (2) un catálogo simulado con
> H₀ que cae de 73 a 68 a lo largo de 0.023–0.15 (mismas z y covarianza) TIENE que salir «apoya»; (3) uno
> plano en 73 TIENE que salir «excluye». Si un control falla, la prueba no vale.
> **REVISIÓN DEL CRITERIO (2026-10-03, decisión de Mike, DESPUÉS de ver el dato — se declara).**
> El control 3 falló: el plano en 73 solo salió «excluye» en el 56 % (se exigía 80 %). Causa (error
> de diseño mío): el criterio sumaba el ±0.968 de H_glob, que sale del mismo ±1.04 de SH0ES que ya
> lleva la calibración común de todas las capas, o sea, contaba dos veces el mismo error. Criterio nuevo:
> **excluye si la caída es menor que H_SH0ES·f_screen (el exceso local entero) a más de 3σ**, usando
> solo la caída, donde el M_B común se cancela. Se reporta además la fracción máxima del apantallamiento
> que podría promediarse antes de z = 0.15. El veredicto con el criterio original se sigue reportando.
> **RESULTADO (log `results/logs/h0_por_profundidad.json`, etapa `h0_por_profundidad`).** Controles: Brout+2022
> reproducido (73.53 contra 73.6 publicado), la caída simulada detectada en el 100 % y el plano en el 96 %. Con
> SSEE: H₀ = 73.26 en z = 0.023 y 73.11 en z = 0.15, caída +0.15 ± 1.05; le faltan 4.70σ para la caída
> entera ⟹ **EXCLUYE la versión de volumen que se promedia del todo antes de ~600 Mpc** (ΛCDM-Planck: 5.12σ).
> No excluye una parcial: hasta el 65 % de f podría promediarse antes de z = 0.15 (3σ). Lo que queda vivo de la
> lectura de Mike: el apantallamiento actúa igual a toda profundidad del flujo de Hubble o vive en el paso de
> calibración (anfitriones Cefeida, < ~40 Mpc). Próxima prueba que separa esas dos: H₀ por subgrupos de
> calibradores según su distancia.
> **2026-10-03 — PRUEBA POR MÉTODOS (decisión de Mike), escrita ANTES de correr.** Sustituye a la de
> calibradores cercanos contra lejanos porque la incluye. Pregunta: ¿el apantallamiento lo ve TODO método
> local (lectura de plano/nivel, «P») o solo el que se calibra con Cefeidas («C»)?
> **Predicción sin SH0ES (para no ser circular):** H_glob medido por DESI DR2 sola con prior plano
> (`h0_four_priors.json`, plano), y el f_screen del álgebra. P: todo método local da H_glob,DESI/(1−f).
> C: los métodos sin Cefeidas dan H_glob,DESI. Control del otro lado: ΛCDM sin apantallamiento, todo método
> local da el H₀ de Planck 2018 (67.36 ± 0.54, leído de su .tex).
> **Datos (valor titular leído del LaTeX de cada artículo, ninguno tecleado):**
> - PRIMARIO, sin escalera estelar: máseres MCP (arXiv:2001.09213), lentes TDCOSMO-2025 (arXiv:2506.03023),
>   sirena GW170817 (arXiv:1710.05835). Independientes entre sí.
> - SECUNDARIO, escalera sin Cefeidas, POR EQUIPO y sin combinar (comparten supernovas dentro de cada
>   equipo y difieren entre equipos por selección de muestra, según arXiv:2408.11770): TRGB de CCHP (arXiv:2408.06153),
>   TRGB y JAGB de SH0ES con JWST (arXiv:2408.11770). JAGB de CCHP como referencia.
> - Con Cefeidas, solo como referencia: SH0ES HST (arXiv:2112.04510, la entrada de la cascada) y SBF (arXiv:2101.02221, calibración mixta).
> **Criterios (sobre el PRIMARIO):** errores asimétricos como normal partida; errores separados (estadístico,
> sistemático) en cuadratura. «Apoya P frente a C»: Δχ²(C−P) ≥ 9 y χ²_P con p > 0.05. «Apoya C frente a P»:
> Δχ²(P−C) ≥ 9 y χ²_C con p > 0.05. Lo demás: no concluye.
> **Control de potencia (R53), antes de leer el veredicto:** 2000 simulaciones del PRIMARIO con sus errores
> reales, bajo P y bajo C. Si el criterio no recupera la hipótesis verdadera en ≥ 80 % de los casos, la
> prueba **no tiene potencia con estos datos**. Se reporta eso y la precisión combinada que haría falta,
> no un veredicto. Control de lectura: cada valor se vuelve a buscar en su .tex, y un dígito alterado
> tiene que no encontrarse.
> **RESULTADO (log `results/logs/h0_por_metodos.json`, etapa `h0_por_metodos`): SIN POTENCIA.** Con los errores
> reales de máseres, lentes y la sirena, el criterio recupera P solo el 22 % de las veces y C el 11 % (se exigía
> el 80 %). No hay veredicto. Haría falta que esos métodos, combinados, midan H₀ con un error de ~1.0 km/s/Mpc;
> hoy es ~2.25. Descriptivo, no veredicto: los tres primarios caen a ≤ 0.35σ de P (72.85) y a 0.28–2.02σ de C
> (67.78). La escalera TRGB depende del EQUIPO: SH0ES-JWST 72.1 (−0.33σ de P), CCHP 70.39 (a medio camino entre
> las dos). Un cambio de método no separa las hipótesis mientras el cambio de equipo pese más.
> **Corrección declarada (después de la primera corrida):** TDCOSMO publica su H₀ con fondo ΛCDM plano. Las
> predicciones P y C se pasan a ese marco con la razón de distancias de retraso de `h0_lente_fondo_ssee`
> (el mismo descuido de ingredientes por modelo de siempre). Con eso: χ² P 0.64, C 4.63; la potencia sigue
> igual (23 % / 11 %). Sigue SIN POTENCIA.
> **REGISTRADO 2026-10-03 (decisión de Mike): la lectura P como rival del criterio 4 de Paper 9 (SN Requiem).**
> P: la lente ve el valor local, y un análisis ΛCDM plano de MACS J0138 daría ~74.2 → la cuarta imagen reaparece
> en 2026 (centro de la interpolación: junio, ±4 meses). C (criterio 4, ya registrado el 2026-09-19): ~69.1 →
> 2027. Reaparición en 2026 ⟹ cae el criterio 4 y queda P; en 2027 ⟹ cae P. **Registro tardío, declarado:** la
> mayor parte de la ventana de P ya pasó sin reporte público de la imagen (búsqueda del 2026-10-03); la
> ausencia ya pesa contra P, a la espera de los resultados de la campaña HST/JWST (programa 9330). Valores en
> `h0_lente_fondo_ssee.log` (`requiem_fecha`). Paper 9, criterio 5.

**De dónde viene.** OP-8 se **disolvió** el 2026-06-18 en su forma original: con el reframe
ω_m-directo ya no hay «factor materia» que derivar, y Ω_m,CMB = ω_m/h² es derivada. Pero
MIRA no desapareció con él: sigue siendo una entidad del modelo (`MIRA = AURA/2`), y sigue
sin salir de la acción.

**Lo que falta.** Cuatro mecanismos naturales probados y **los cuatro descartados por
medición**, no por opinión: c²_s, Poisson-μ, disformal, y retención conformal β_c = −AURA
(esta última da excursión ×18 excesiva, signo invertido y timing invertido —
`ssee_mira_mechanism.py`).

**Criterio de cierre.** Un mecanismo que produzca MIRA desde la acción vigente, o la
declaración explícita de que MIRA es un valor algebraico sin dinámica asociada.

> **2026-10-03 — Paper 9 reescrito sin lo retirado (rama `cierre-op4-desi`).** P9 ya no
> toma MIRA de la geodésica disforme de P8 ni deriva la forma multiplicativa del paso de
> universo separado: éste cancelaba Ω_m/(1+w₀) con la «identidad» 1+w₀ = Ω_m, y 1+w₀ = 0.160
> es ecuación de estado, no densidad (Ω_m = 0.308881). Queda: (i) MIRA = AURA/2 como
> **definición algebraica** (3·MIRA = T_r/2); (ii) f = s_K/(3MIRA) como identidad; (iii)
> H_loc = H_glob/(1−f) como **POSTULADO de apantallamiento** (P9 §3.4, eq:screen_postulate),
> con las dos pruebas de hoy en §Limitations (profundidad: la versión de volumen se excluye
> a 4.70σ; métodos: sin potencia) y los criterios 4 y 5 intactos. También se retiró la figura
> f_screen(z) (usaba 0.160 como densidad) y el control de Freedman pasó al TRGB adoptado por
> CCHP v3 (70.39 ± 1.94 → −1.28σ IR; antes 69.96 de la v1 → 1.88σ), leído de su .tex
> (`p9_cascada_control.json`). P7 L350 y el Unified dicen ya lo mismo.
> **Decidido (ver cierre arriba):** cumple la segunda vía del criterio de cierre («MIRA es un
> valor algebraico sin dinámica»). El mecanismo del apantallamiento pasa a OP-6b.

**Severidad:** cerrado.

---

## OP-10b — P7 y P10 usan el mismo símbolo M⁴ para dos cosas — 🟡 ABIERTO (resto de OP-10)

**De dónde viene.** OP-10 cerró por disolución. Pero `ssee_eft_verification.py` usa
`M⁴ = ρ_crit` (= 1 en sus unidades) y `ssee_paper10_verification.py` usa `M⁴ = 5φ⁸ρ_crit`
(= 234.9). **La separación está entendida** —son dos K(X) distintas y eso es correcto, el
factor al cruzarlas es 45.5— pero el símbolo es el mismo en los dos sitios.

**Lo que falta.** Notación distinta para cada uno, o una nota en ambos scripts que diga cuál
es cuál. Mientras tanto, cualquiera que cruce los dos ficheros obtiene un número sin sentido.

**Criterio de cierre.** Símbolos separados en código y en los dos papers.

**Severidad: Media.** No mueve ningún resultado; es una trampa de lectura ya activada una vez.

---

## OP-22b — El mapa campo → fluido (ζ̃, τ_Π) no está derivado — 🟡 ABIERTO (resto de OP-22)

**De dónde viene.** OP-22 **cerró** el 2026-09-06: la viscosidad va con la entalpía ρ+p,
cerrado por test de límite. Y el conteo de grados de libertad (2026-09-07) cerró la parte
de «dos canales»: ambos cuentan UNA onda, luego el 0 del fluido y el 0.021284 del campo
describen la misma, y la del campo es la fundamental.

**Lo que falta.** El mapa de los parámetros del campo a los del fluido efectivo (ζ̃, τ_Π) no
está derivado, así que **por qué el límite de fluido cae exactamente en 0 y no en 0.021284
sigue sin establecerse**. Queda además RETIRADA la derivación de τ_Π por saturación de
causalidad del apéndice EFT de Paper 1 (usaba ρ en vez de ρ+p; daba 0.2946).

**Criterio de cierre.** Derivar el mapa, o medir c²_s: la brecha 0.021284 es toda la
predicción de Paper 7, así que una medida discrimina.

**Severidad: Media.** No mueve un número publicado, pero es el eslabón que sostiene la
predicción propia del sector.


---

## OP-26 — fσ₈ contra el dato crudo de BOSS — ✅ MEDIDO (R1/R2 LPT 2026-09-07, re-corrido con los ingredientes de cada modelo 2026-10-01)

> **CIERRE (anotado 2026-10-03; la medición es del 2026-10-01).** Este OP quedó escrito como abierto
> después de que se midiera, y el banner de CLAUDE.md lo repetía: el 2026-10-03 se citó a Mike como
> «pendiente» por leer la ficha y no el log. Medido (`results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json`,
> `analiza_boss_R1R2.py`, velocileptors LPT, k ≤ 0.20, 222 puntos, SSEE con Σm_ν 0.06849 y ΛCDM con 0.06):
> - χ²_real mínimo: SSEE 205.55 vs ΛCDM 207.58 → Δχ² = -2.03, a igual número de libres.
> - fσ₈ de SSEE en z = 0.38 / 0.51 / 0.61: 0.410 / 0.411 / 0.409 (± 0.021).
>   Contra el fσ₈ comprimido publicado (Alam+2017): 1.76σ / 1.08σ / 0.68σ; ΛCDM, con el mismo pipeline: 1.55σ / 0.91σ / 0.55σ. El pipeline queda bajo en z = 0.38 con los DOS modelos: es del método, no de SSEE.
> - Control del otro lado: ΛCDM reproduce su propia cadena (logA y fσ₈ a < 0.004σ, χ² idéntico).
> - **BOSS no vota en A_s:** el logA de perfil y el marginal difieren 1.82σ ⟹ el valor central se mueve con el estimador (ver `memory/feedback_check_repo_before_deriving.md`).
> Ya está en Paper 6 por `\val` (`bossR_*`). Lo que queda vivo es sólo de lectura: la cizalla discrimina en A_s, BOSS no.

**Texto original (2026-09-19), conservado:**


**De dónde viene.** Era el último punto vivo de la Fase B del reframe ω_m-directo. Los otros
tres se cerraron y tienen log: r_d = 147.174 Mpc (0.32σ) con Ω_m = 0.308881
(`p3_rd_reframe_omega_m.log`), el posterior H₀ = 67.787 ± 0.353 bajo prior H_alg <!-- R74: git:2a4d76415b:CANONICAL_VALUES.yaml -->
(`mcmc_paper2_reframe.log`) y el control metodológico ΛCDM R4
(`growth_2026-07/R4_lcdm_kids_S8.json`). Éste no.

**Lo que falta.** R1/R2 con LPT (velocileptors, k ≤ 0.20, 222 puntos) contra el dato crudo.
El barrido Kaiser del 2026-08-08 **fue un sondeo, no un resultado**: midió que Δχ² depende
del corte (de +0.8 a −11.3 entre k = 0.06 y 0.12), y de ahí se sigue que Kaiser no publica.

**Por qué importa.** Paper 6 tiene su fila de S₈ cerrada contra KiDS crudo (0.10σ) y la de
fσ₈ vacía. Mientras siga vacía, el sector de crecimiento está medido a medias.

**Criterio de cierre.** Una corrida R1/R2 con LPT y su control del otro lado, o la
constatación medida de que el dato crudo no discrimina a las escalas accesibles.

**Severidad: Media-Alta.** No invalida ningún número publicado, pero es la mitad que falta
del titular de Paper 6.


---

## OP-27 — La relación δc = δc,EdS × n_s no está derivada, y su consecuencia cambia de signo — 🟡 ABIERTO (2026-09-25)

**De dónde viene.** Paper 4 §«Linear Collapse Threshold δc» postulaba
δc_SSEE = δc_EdS × n_s = 1.6865 × 0.96556 = 1.6284, con el argumento de que «el mismo
factor inflacionario n_s que inclina el espectro primordial modula el criterio de colapso
gravitacional». Paper 5 §JWST usaba ese valor para un enhancement de 1.05×–1.89× en la
función de masa de halos a z ≳ 10.

**Qué se midió.** Colapso esférico top-hat, ecuación no lineal exacta con *shooting* sobre
δ_i, sobre el fondo del propio modelo:

| z_c | EdS | ΛCDM | SSEE | SSEE vs ΛCDM |
|---|---|---|---|---|
| 0  | 1.68646 | 1.67599 | **1.67634** | +0.021 % |
| 10 | 1.68647 | 1.68646 | **1.68647** | +0.001 % |

Control del otro lado (R53): EdS reproduce el analítico 3/20·(12π)^(2/3) = 1.68647 a una
parte en 10⁵. El postulado 1.6284 está a 2.9 % y **la dinámica del modelo no lo produce**.
Script: `src/p02_mcmc/spherical_collapse_deltac.py`.

**El supuesto, y por qué se sostiene por la puerta correcta.** El cálculo asume DE suave.
La justificación NO es c²_s,eff = 0 —un horizonte sonoro nulo es justamente la condición
para que un fluido de DE **sí** se agrupe a toda escala sub-horizonte— sino la fricción
viscosa IS del propio Paper 5 (§«IS damping hierarchy»):
`F(k,a) = (1 − 3c_s²) + z̃·(k/aH)²`, que con c_s²=0 vale `1 + z̃(k/aH)²` y crece como k²,
con δ_DE/δ_m → 0⁻ medido a toda escala. La DE de este modelo no se agrupa **a pesar** de
c_s²=0, no **por** c_s²=0. Si algún día el sector IS modificara el colapso no lineal más
allá de DE suave, este cálculo no lo captura y la carga de especificarlo es del modelo.

**Por qué sigue siendo conjetura MOTIVADA y no ocurrencia.** n_s no es sólo la inclinación
primordial: es cantidad algebraica del sector materia, n_s = 1 − φ⁻⁷, y entra en la
identidad forward ω_c = KAL₀·ω_b·n_s (OP-19). Que el mismo número que construye la densidad
de materia module también su colapso no es descabellado *a priori*. Pero **el n_s de ω_c ya
está dentro del cálculo**, vía Ω_m = 0.308881; el factor extra sobre δc necesita mecanismo
propio.

**Lo que cuesta, y no es que el efecto se anule — se INVIERTE.** Press-Schechter sobre los
dos fondos, con el δc derivado (`src/p02_mcmc/ssee_press_schechter.py`):

| z | 3×10¹⁰ M☉ | 10¹¹ M☉ | 10¹² M☉ | 3×10¹² M☉ |
|---|---|---|---|---|
| 10 | 0.998 | 0.990 | 0.945 | 0.892 |
| 15 | — | 0.972 | 0.878 | 0.774 |

SSEE forma **menos** halos masivos tempranos que ΛCDM, no más. La causa no es la amplitud
—SSEE tiene σ₈ **mayor**, 0.8153 contra 0.811— sino D(z): Ω_m menor (0.308881 vs 0.3153) y
el fondo CPL crecen menos entre z ~ 10 y hoy. A las masas que JWST realmente mide
(~10^10.8 M☉) el cociente es 0.99. **El modelo no explica el exceso JWST, y en el extremo
de masa alta apunta ligeramente en contra.**

**Criterio de cierre.** Una derivación del factor n_s en el criterio de colapso: o bien un
rol dinámico de n_s en la ecuación de colapso no lineal, o bien una modificación
especificada del colapso desde el sector IS que produzca δc ≈ 1.63.
**Qué lo falsaría como predicción:** conteos de halos a z ~ 10 con precisión 10–20 % a
M > 10¹² M☉ compatibles con 1.00×.

**Severidad: Media.** No mueve ningún ajuste de fondo —DESI, CMB y BAO no usan δc— pero
retira un resultado publicado en dos papers y convierte una firma que estaba anotada a
favor del modelo en una levemente en contra. Eso hay que asentarlo con el signo correcto
antes de cruzarlo con la literatura.
