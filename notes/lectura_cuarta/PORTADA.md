# Cuarta lectura — PORTADA (SSEE_Cover.tex)

## Conteo por decisión (12 entradas en numeros, cubriendo ~26 cifras del inventario)
- TRIVIAL: 5 entradas (~21 cifras: coordenadas, rotación, opacidad de la textura tikz y del marco decorativo)
- ALG: 5 (fórmulas puras sin valor numérico mostrado: Ω, n_s, f_screen, Ω_m, H_0^glob)
- VAL: 2 (w0=-0.839950, wa=-0.669975, ambos tecleados a mano pero correctos)
- afirmaciones: 2

## Los hallazgos más relevantes
1. **Hallazgo conceptual (el más importante)**: las líneas 48 y 50 muestran, una junto a la otra en la textura decorativa, $f_{\rm screen}=(\pi-\varphi)/(\varphi+\pi)^2$ y $H_0^{\rm glob}=H_{\rm SH0ES}(1-f_{\rm screen})\simeq3(\varphi+\pi)^2$. La primera fórmula es ALGEBRAICAMENTE IDÉNICA a `F_SCREEN_IR_d6`=0.067253 — es decir, es SOLO el término IR de Paper 9. Con ese f_screen el resultado es 68.13 km/s/Mpc (0.17σ del blanco), NO 67.962142 (el blanco con residuo +4.2e-6) que requiere el f_screen COMPLETO (IR+UV=0.069522). Ninguna cifra está mal (no se muestra ningún número en esas dos ecuaciones), pero la yuxtaposición sugiere al lector que la fórmula simple IR cierra el "≃3(φ+π)²" con precisión — justo la confusión IR-vs-completo que el banner de CLAUDE.md marca como superada.
2. Los dos valores numéricos que sí aparecen (w0=-0.839950, wa=-0.669975) son correctos y coinciden con las macros W0_d6/WA_d6, pero la portada es un documento TikZ standalone sin `\input{valores_generados.tex}`: si esos valores cambiaran, esta página no se actualizaría sola.
3. Sin números retirados: ninguna de las 8 ecuaciones decorativas usa 72.86, 73.040, β_c=−AURA, la partícula φ-DM, s_m=0.160 como densidad, ni radios de Vainshtein. El 95% de las cifras del inventario son coordenadas de diseño gráfico, no resultados.

Rutas: `notes/lectura_cuarta/PORTADA.yaml`, `manuscript/SSEE_Cover.tex`.
