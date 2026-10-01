# Ruta 1 — δc desde la dinámica (colapso esférico): RESULTADO

Fecha: 2026-09-25. Script: `src/p02_mcmc/spherical_collapse_deltac.py` (movido desde este directorio el 2026-09-30).

## Pregunta

¿El postulado del Paper 4, δc_SSEE = δc_EdS × n_s = 1.6284, se deriva de la
dinámica del modelo o hay que retirarlo?

## Método

Ecuación exacta del top-hat esférico con DE suave (no se agrupa — consistente
con Paper 5: c²_s,eff = 0, perturbaciones de DE nulas a sub-horizonte) en GR:

δ'' + (2+H'/H)δ' − (4/3)(δ')²/(1+δ) = (3/2)Ω_m(a)δ(1+δ),  ' = d/d ln a.

Shooting sobre δ_i (modo creciente) para colapso en a_c; δc(a_c) = δ_lin(a_c).
Richardson de 3 niveles a δ_i → 0 + D_MAX = 10¹⁰.

Supuestos declarados: (i) GR, (ii) DE suave, (iii) top-hat esférico.

## Validación

EdS → 1.68646 a todo z_c (esperado 1.68647). PASA (< 2×10⁻⁵).

## Tabla

| z_c | EdS     | ΛCDM    | SSEE    | SSEE/EdS−1 | SSEE/ΛCDM−1 |
|-----|---------|---------|---------|------------|-------------|
| 0   | 1.68646 | 1.67599 | 1.67634 | −0.60%     | +0.021%     |
| 1   | 1.68646 | 1.68438 | 1.68496 | −0.09%     | +0.034%     |
| 2   | 1.68646 | 1.68580 | 1.68613 | −0.02%     | +0.020%     |
| 5   | 1.68646 | 1.68638 | 1.68644 | −0.00%     | +0.004%     |
| 10  | 1.68647 | 1.68646 | 1.68647 | −0.00%     | +0.001%     |

ΛCDM con Planck 2018 (Ωm=0.3153); SSEE con (Ωm=0.308881, w₀=−0.83995, wₐ=−0.66997).

## Veredicto

**El postulado no sobrevive a la derivación.** La dinámica del modelo da
δc_SSEE = 1.676 (z=0), esencialmente idéntico a ΛCDM (1.676), no 1.6284.
El factor n_s no tiene por dónde entrar: a alto z el universo SSEE está
dominado por materia igual que el estándar, y con DE suave el colapso
esférico casi no se entera de (w₀, wₐ).

## Impacto

1. **Paper 4 §"Linear Collapse Threshold δc"**: el postulado δc = δc_EdS × n_s
   debe retirarse o moverse a OP como conjetura sin derivación. La Ruta 2
   (rol dinámico de n_s en el colapso) no existe todavía.
2. **Paper 5 §"Implications for JWST early galaxy counts"**: el enhancement
   1.05×–1.9× venía del δc reducido. Con δc ≈ 1.676 ≈ ΛCDM, el enhancement
   se evapora: SSEE y ΛCDM predicen abundancias de halos prácticamente
   idénticas a alto z (consistente con D(z) difiriendo ≤0.2%).
3. **Nota Press–Schechter de hoy** (`RESULTADO.md`): los ratios 1.03×–1.80×
   quedan superados — usaban el δc postulado. Con el δc derivado, el ratio
   honesto es ≈1.00× en todo el rango.
4. **Lo que NO se toca**: los ajustes del fondo (DESI, CMB, BAO) no usan δc;
   siguen intactos. Esto solo afecta las afirmaciones de formación de
   estructura construidas sobre el postulado.

## Lectura del sistema Guardiola

Se declaró lo que salió, en contra del postulado. El modelo pierde una
ventaja reclamada en "too big too soon", pero queda más sólido: una
predicción menos sin derivación es una debilidad menos.
