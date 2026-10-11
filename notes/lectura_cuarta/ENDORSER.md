# Cuarta lectura — ENDORSER (SSEE_Endorser_Summary.tex)

## Conteo por decisión (34 entradas en numeros)
- LIT: 9 (datos observacionales citados — DESI DR2, Planck 2018, SH0ES, BK18)
- VAL: 17 (resultado SSEE con macro `\val` existente o propuesta nueva)
- ALG: 2 (M=9.68 meV, w0≈-0.840 como umbral de falsación)
- HIS: 1 (H0^MIRA=67.04, retirado, correctamente narrado)
- DERIVADO: 2 (gap sqrt(AURA)/MIRA 0.03%; "span 1.0" de los tres χ²)
- FIX: 1 (número real mal calculado)
- afirmaciones: 3

## Los 3 hallazgos más graves
1. **FIX de estado, el más grave del documento**: L111-114 dice que el defecto dimensional del radio de Vainshtein de Paper 8 está "open and under repair (OP-4, reopened 2026-09)". En realidad **OP-4 está CERRADO desde 2026-10-03, por RETIRO COMPLETO de la fórmula** (no por repararla): Paper 8 §Vainshtein dice explícitamente "those values are withdrawn" y "no screening radius is needed". ENDORSER es el primer documento que lee un posible avalador de arXiv — presenta un estado de hace más de un mes como si fuera el actual.
2. **FIX numérico real**: L47, la distancia del blanco puro 3(φ+π)²=67.96214 a Planck (67.36±0.54) se muestra como "1.11σ"; calculado con ssee_core da 1.115069σ → redondea a **1.12**, no 1.11. No existe macro ni log que calcule esta distancia específica (a diferencia de ω_b, n_s, Ω_m que sí tienen `algebra.*_sigma_planck` en algebra_derivada.json); se propone crearla.
3. **Patrón sistemático "macro existente, no usada"**: igual que P8/P10, c_s²=0.021284, r=φ⁻¹⁰=0.008131, y los cinco números de la tabla χ² de KiDS-Legacy (417.97/418.34/418.95/6.24/6.86) YA tienen macro `\val` en `valores_generados.tex` pero el .tex los teclea a mano (en el abstract y en el párrafo de Paper 6). Ningún número retirado (72.86, 73.040, β_c=−AURA, partícula φ-DM, s_m=0.160 como densidad) aparece presentado como vigente — el párrafo de Paper 6 es, de hecho, el más actualizado del documento (titular KiDS-Legacy, sin reclamo de prioridad temporal).

Rutas: `notes/lectura_cuarta/ENDORSER.yaml`, `manuscript/SSEE_Endorser_Summary.tex`.
