# Cuarta lectura — PRD (submission_PRD/SSEE_PRD.tex)

## Conteo por decisión (99 números revisados: 87 del inventario + 12 hallados a mano)
- ALG (álgebra φ,π recalculada con `ssee_core`/P10): 24 — todas confirmadas exactas.
- VAL (resultado nuestro, debería ir por `\val`, ya correcto en valor): 25 — todas
  confirmadas exactas contra su log; 23 ya tienen macro `\val` existente que el
  texto no usa en ese punto (duplica el número a mano en vez de reutilizar la macro).
- LIT (dato publicado con cita): 19 — citas presentes y valores plausibles; **2 no
  pude cotejar contra la tabla primaria** (w₀,wₐ best-fit DESI DR2+CMB+Pantheon+,
  línea 222: sólo tuve el abstract vía WebFetch, no la Tabla 3 del arXiv:2503.14738).
- CITA (falta la referencia): 2 — `r<0.036` (BICEP/Keck) aparece dos veces sin `\citep`.
- HIS (retirado, narrado como historia): 10 — todos correctamente marcados como
  superados en el propio texto, varios con comentario `% ORIGEN-VALOR` inline.
- TRIVIAL: 17 — tolerancias de diseño, rangos descriptivos, proyecciones
  cualitativas para DR3, fila de referencia de tabla.
- DERIVADO: 3 — barrido de sensibilidad a ρ, diferencia porcentual Ω_m con/sin ν.
- Pendiente real (no resuelto esta sesión): **1** (ver hallazgo 2 abajo).

## Los 3 hallazgos más graves
1. **Núcleo algebraico perfecto.** Recalculé con `ssee_core.py` y el script ligero
   de P10 TODA la cadena dura: w₀=-0.839950, wₐ=-0.669975, S_K=0.403302,
   α_K=15.591336, c_s²=0.021284, Ω_m=0.308881 (con y sin ν: 0.307289, el "0.6%"
   del texto), H_glob=67.962142 (=SH0ES·(1−f_screen)), M=9.68 meV (vía M⁴=5φ⁸ρ_crit,
   NO confundir con la macro `M_meV_rhoLambda_d2`=8.81 que el propio
   `algebra_derivada.py` marca como "la INCONSISTENTE que Paper 10 descarta"),
   los tres exponentes alternativos de n_s (6.84/6.90/6.88) y la tabla completa
   del test look-elsewhere (55/25/490, hits 1-1/1-2/1-4/2-5/4-9). **Cero errores
   algebraicos encontrados** — este documento ya pasó por una limpieza reciente.
2. **"1.01σ" sin rastro (línea 894).** El texto dice que el control con fondo
   Planck (misma rigidez que SSEE) da 1.01σ. La memoria de Mike
   (`project_as_clavado_k1.md`, 2026-09-19) registra ese mismo control en **1.03σ**.
   Revisé `kids_legacy_bic.json`, `kids_legacy_lcdmfijo.log`, `s8_kids_legacy_camb.json`
   y `kids_publicados.json` sin encontrar el campo. Puede ser una re-corrida
   legítima (la memoria es aproximada por regla propia) o un desliz — hay que
   trazar el script antes de dar la cifra por buena.
3. **Gap de herramienta: `inventario.py` no detecta números tras `\pm`.** El
   lookbehind de la regex se come la "m" de "\pm". Encontré a mano 12 números
   adicionales (0.968 ×2, 0.0005 ×6, 0.001 ×2, 0.002, 0.005 ×2, 0.01, 0.006) que el
   inventario automático había dejado fuera — todos confirmados correctos, pero
   si esta cuarta lectura se repite en otros documentos el mismo hueco se repite.
   Vale la pena arreglar la regex de `inventario.py` antes de la próxima pasada.

## Afirmaciones
Ninguna de las trampas típicas de `INSTRUCCIONES.md` (c_s²=1 canónico,
off-diagonal CMB pendiente, γ=0.658 sin superar, w_a=-0.631) aparece en este
documento — ya usa c_s²=0.021284, el full plik k=2vs6, γ_IS=0.550, y w_a=-0.617
nunca se menciona por ese valor viejo. Lista `afirmaciones` vacía.

## Ruta
`notes/lectura_cuarta/PRD.yaml`, `notes/lectura_cuarta/PRD.md`.
