# Figuras archivadas — por qué está aquí cada una

Este cajón guarda figuras que **ya no ilustran nada vivo**. No se borran
porque un resultado retirado sigue siendo parte del registro: quien lea la
historia del modelo tiene derecho a ver qué se afirmó y cómo se dibujaba.

Lo que no pueden hacer es seguir en `results/figures/`, porque de ahí las
toman los documentos y una figura huérfana se cuela en un paper por
descuido — que es exactamente lo que pasó (ver abajo).

| figura | de dónde venía | por qué se archiva |
|---|---|---|
| `fig_paper6_verification.pdf` | Paper 6, versión de dos sectores | Dibuja la partícula φ-DM (`m_φ = 40.70 eV`) y el sector doble, **retirados el 2026-08-01**. Ningún documento vivo la incluye. Archivada el 2026-09-19. |
| `fig2_cluster_sensitivity.png` … `fig8_tension_summary.png` | figuras de versiones anteriores de Papers 2–5 | superadas por las que hoy genera `src/ssee_*_figures.py` |
| `retiradas_2026-10-21/fig2_cluster_sensitivity.pdf`, `retiradas_2026-10-21/fig2_cluster_sensitivity.png` | `ssee_paper2_figures.py` (fig. 2) | cúmulos con los datos atribuidos a Zhang+2026, que no salían de ahí (rehecho en `cumulos_zhang2026.json`, 2026-10-01); ningún paper la incluye. Archivada el 2026-10-21 al meter las figuras a DVC. |
| `retiradas_2026-10-21/fig4_KAL_interpolation.pdf`, `retiradas_2026-10-21/fig4_KAL_interpolation.png` | `ssee_paper2_figures.py` (fig. 4) | interpolación KAL(x) Newton-MOND, lectura retirada de P2 el 2026-10-01 (KAL₀ es retención, no amplificador). Archivada el 2026-10-21. |
| `retiradas_2026-10-21/fig_paper5_growth_rate.pdf` | `ssee_paper5_IS_perturbations.py` | no entra en P5; el script deja de generarla. Archivada el 2026-10-21. |
| `retiradas_2026-10-21/fig_paper5_S8_comparison.pdf` | `ssee_paper5_IS_perturbations.py` | «S8 Tension: SSEE IS predicts lowered amplitude», relato retirado el 2026-08-01; no entra en P5. Archivada el 2026-10-21. |

## La lección que deja la primera fila

El barrido de retractaciones miraba `.tex`, `.md` y `.py`. **Una figura no es
ninguna de las tres.** Por ese hueco la partícula sobrevivió 49 días dentro de
`fig_s8_resolution.pdf` del paquete de PRD: el pie de figura ya contaba la
historia nueva y el dibujo seguía contando la vieja.

Desde el 2026-09-19 el guardián barre también la capa de texto de las figuras
(R60), y con una regla **más estricta** que la de la prosa: un documento
*puede* nombrar lo retirado, porque tiene que retractarlo; una figura no
retracta nada, así que cualquier resto dentro de una figura es un resto.

Esa regla encontró esta figura el mismo día en que se escribió.
