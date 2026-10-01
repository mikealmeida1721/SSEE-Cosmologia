# BORRADOR para revisión de Mike — NO aplicado al manuscrito

Fecha: 2026-09-25. Todo lo de abajo es propuesta; nada se edita sin tu visto bueno.

---

## 1. Entrada OP-27 propuesta (para `OPEN_PROBLEMS.md`)

## OP-27 — La conjetura δc_SSEE = δc_EdS × n_s no está derivada — 🟡 ABIERTO (2026-09-25)

**Origen.** El Paper 4 (§"Linear Collapse Threshold δc") postula
δc_SSEE = δc_EdS × n_s = 1.6865 × 0.96556 = 1.6284: "el mismo factor
inflacionario n_s que inclina el espectro primordial modula el criterio de
colapso gravitacional". El Paper 5 (§"Implications for JWST early galaxy
counts") usa ese valor para un enhancement de 1.05×–1.9× en la función de
masa de halos a z ≥ 10. La **Ruta 1** (2026-09-25, colapso esférico top-hat
con DE suave en GR — las hipótesis de perturbaciones de los propios Papers
5 y 6: c²_s,eff = 0, γ_IS = 0.5504) **no produce ese valor**: da
δc_SSEE = 1.67634 (z=0) → 1.68647 (z=10), esencialmente idéntico a ΛCDM
(1.67599 → 1.68646). Validación: EdS → 1.68646 vs 1.68647 exacto.
Script: `src/p02_mcmc/spherical_collapse_deltac.py`.

**Por qué es conjetura MOTIVADA y no ocurrencia.** En SSEE n_s no es solo la
inclinación primordial: es cantidad algebraica del sector materia,
n_s = 1 − φ⁻⁷, y entra en la identidad forward ω_c = KAL_0·ω_b·n_s = 0.119514
(OP-19, Papers 1–3). Que el mismo número que construye la densidad de materia
module también su colapso no es descabellado *a priori* — pero el n_s de ω_c
ya está dentro del cálculo de la Ruta 1 (vía Ωm = 0.308881). El factor extra
sobre δc necesita mecanismo propio.

**La apuesta cuantificada (la huella).** Con el fondo SSEE fijo, lo único que
cambia entre el δc derivado y el postulado es la abundancia de halos
(Press–Schechter, `comparar_deltac_ruta1_vs_postulado.py`):

| z  | 10¹¹ M☉ | 10¹² M☉ | 3×10¹² M☉ |
|----|---------|---------|-----------|
| 10 | 1.06×   | 1.41×   | 2.01×     |
| 15 | 1.18×   | 2.16×   | 4.56×     |

(B/A: con n_s dividido por sin n_s.) Si la Ruta 2 se deriva algún día, ESTA
curva es la huella que debe producir. En el régimen JWST (10^10.8 M☉) la
conjetura da ~1.03×: no resuelve el "too big too soon" ni siquiera postulada.

**Qué la cerraría.** Una derivación del factor n_s en el criterio de colapso:
o bien rol dinámico de n_s en la ecuación de colapso no lineal (Ruta 2), o
bien una modificación especificada del colapso esférico desde el sector IS
que produzca δc ≈ 1.63. **Qué la falsaría como predicción:** conteos de
halos a z ~ 10 con precisión ~10–20% a M > 10¹² M☉ compatibles con 1.00×.

**Consecuencia si permanece abierto.** El §δc del Paper 4 y la subsección JWST
del Paper 5 quedan como conjetura declarada, no como predicción. Los ajustes
del fondo (DESI/CMB/BAO) no usan δc y no se ven afectados.

---

## 2. Cambio propuesto al Paper 4 (§"Linear Collapse Threshold δc")

Reemplazar el `boxed` del postulado por:

> The critical overdensity for spherical collapse in an Einstein–de Sitter
> universe is δ_{c,EdS} = 3/20 (12π)^{2/3} ≈ 1.6865. Evaluated on the SSEE
> background with smooth dark energy (the perturbation assumptions of Papers
> 5–6: vanishing DE perturbations at sub-horizon scales, GR-like growth with
> γ = 0.5504), the spherical-collapse calculation gives
> δc_SSEE = 1.676 (z=0) → 1.686 (z≳5), essentially identical to ΛCDM
> (1.676 → 1.686); see OP-27. The previously stated relation
> δc_SSEE = δc_EdS × n_s = 1.6284 is therefore **retired as a derived
> prediction** and kept as a **motivated conjecture** (OP-27): n_s is an
> algebraic matter-sector quantity (n_s = 1 − φ⁻⁷, entering
> ω_c = KAL_0·ω_b·n_s), so a link to collapse is not a priori absurd, but no
> mechanism derives the extra factor — the n_s in ω_c is already accounted
> for in the background via Ωm.

---

## 3. Cambio propuesto al Paper 5 (§"Implications for JWST early galaxy counts")

Reemplazar la tabla y el texto del enhancement por:

> With the derived collapse threshold (δc_SSEE ≈ δc_ΛCDM to better than
> 0.1% at all collapse redshifts; OP-27), the Press–Schechter ratio is
> n_SSEE/n_ΛCDM ≈ 1.00 at all masses and redshifts z = 10–15 — the
> enhancement previously quoted (1.05×–1.9×) rested on the retired conjecture
> δc = δc_EdS × n_s and is withdrawn. SSEE predicts essentially the same
> high-z halo abundance as ΛCDM; it offers no advantage on the "too big too
> soon" question through this channel. The n_s conjecture, if ever derived
> (OP-27), would imprint a mass-dependent fingerprint (1.06× at 10¹¹ M☉,
> 1.41× at 10¹² M☉, 2.01× at 3×10¹² M☉ at z=10) — a quantitative, falsifiable
> target for future high-z halo counts.

---

*Fin del borrador. Dime qué ajustar antes de tocar `manuscript/` y `OPEN_PROBLEMS.md`.*
