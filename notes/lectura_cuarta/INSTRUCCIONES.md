# Cuarta lectura — cada número reproducible (2026-10-10)

Encargo de Mike: revisar **hoja por hoja** cada documento y **reproducir cada número**,
para que no quede ni uno sin origen comprobado, y corregir lo que contradiga el modelo
de hoy (como la fila «c_s² = 1 (canonical)» que sobrevivió tres lecturas).

## Reglas duras
1. **SÓLO LECTURA.** Escribe únicamente `notes/lectura_cuarta/<DOC>.yaml` y
   `notes/lectura_cuarta/<DOC>.md`. Claude aplica los cambios.
2. No corras `ssee_verify.py`, `test_guardian.py`, `mutacion_guardian.py`, `dvc`,
   cobaya, CAMB, CLASS ni MCMC. Python ligero sí: `src/ssee_core.py`, leer JSON de
   `results/logs/`, leer `data/raw/`.
3. Todo en español. Escribe el .yaml **incrementalmente** (cada 20–30 números), para
   que nada se pierda si te cortan.
4. Escrutinio simétrico: verifica antes de afirmar. Busca la salida (banners de
   `CLAUDE.md`, `CANONICAL_VALUES.yaml`, `RETRACCIONES.yaml`, `OPEN_PROBLEMS.md`).

## Tu entrada
`python3 notes/lectura_cuarta/inventario.py <DOC>` lista cada número escrito a mano
(lo que no va por `\val`) con archivo:línea y contexto. `notes/lectura_cuarta/clasificacion.json`
trae una PRE-clasificación automática por coincidencia de VALOR (clase ALG/LIT/LOG/HIS/?/corto
y una fuente candidata). **La coincidencia de valor no prueba nada**: confirma que la fuente es
la MISMA ENTIDAD (mismo observable, mismo modelo, mismo dataset, misma corrida vigente).
`manuscript/valores_generados.tex` lista las macros `\val` que YA existen (nombre, valor,
log#clave): si una sirve, úsala en vez de crear otra.

**PROHIBIDO copiar la pre-clasificación sin abrirla.** Cada `VAL` lleva `nombre` y una
`fuente` que ABRISTE y cuyo significado coincide con el texto. Una entrada con «pre-clasificado,
no reabierto» cuenta como NO hecha (pasó en P1: 21 de 157).

## Qué decides para CADA número (campo `decision`)
- `VAL` — resultado nuestro: debe ir por `\val`. Da `nombre` (macro existente, o nueva en
  minúsculas_con_guiones_bajos), `fuente` = `results/logs/<archivo>.json#<clave.anidada>`
  (comprobada abriendo el JSON) y `formato` (p. ej. `.2f`, `.4f`). Si el valor del texto
  NO coincide con el log a su redondeo, pon además `nuevo` y `nota`.
- `ALG` — álgebra de φ,π: da `expr` (expresión Python con `ssee_core as c`, p. ej.
  `c.W0`) y comprueba el redondeo. Si existe macro `\val` del álgebra, propón `VAL`.
- `LIT` — dato publicado: confirma que la frase/fila cita la fuente correcta y que el número
  coincide con ella (`nota` con dónde lo comprobaste). Si falta la cita, `decision: CITA`.
- `DATO` — viene de `data/raw/` (p. ej. el vector BAO de DESI): da el archivo.
- `HIS` — valor retirado narrado como historia (claramente marcado). OK.
- `DERIVADO` — se calcula de otros números del mismo texto (p. ej. una distancia en σ, una
  resta): da la cuenta y el resultado. Si los insumos van por `\val`, propón `VAL` con una
  clave de log si existe.
- `FIX` — el número está mal o es un concepto retirado presentado como vigente: da `nuevo`
  (texto LaTeX exacto que lo reemplaza) y `nota` con la evidencia.
- `TRIVIAL` — no es un resultado (número de ecuación, versión de software, límites de un
  prior declarados, años, k-cortes de diseño, «2.0» de un exponente…).

## Además: afirmaciones (no sólo números)
Cada tabla, pie de figura, resumen y lista de estado: ¿lo que afirma es el modelo de HOY?
Ejemplos de lo que ya se coló: «c_s² = 1 (canonical)» (hoy 0.021284, condensado de P7);
«off-diagonal CMB covariance» como pendiente (hecho: plik completo); γ = 0.658 sin decir
que lo supera 0.5504; w_a de DESI −0.631±0.226 (es −0.617±0.208). Repórtalo en la lista
`afirmaciones` del .yaml con `linea`, `dice`, `debe_decir` (LaTeX exacto) y `evidencia`.

## Decisiones vigentes (verificar SIEMPRE)
- H con unidades: `H_glob = H_SH0ES(1−f_screen) = 67.962142 ± 0.968`; `3(φ+π)²` es el
  BLANCO puro (no entrada, no ancla). 68.13 = `H_0^{glob,IR}` (régimen IR, no canónico).
  72.86 y 73.040 retirados.
- Un solo sector de materia, Ω_m = 0.308881. s_m = 1+w₀ = 0.160 es ecuación de estado, nunca densidad.
- Partícula φ-DM y segundo sector RETIRADOS (2026-08-01).
- S₈ titular: KiDS-Legacy 0.8273 predicho vs 0.8265±0.0176 (A_s clavado al CMB). KiDS-1000 0.7559±0.0189 es antecedente.
- Energía oscura: acción de P7 `K = c1X + c2X²`, condensado fantasma, `c_s² = 0.021284`,
  α_K = 15.591336. `s_K = 0.403302` es la tasa de dilución (no kineticidad).
  `K = X/KAL₀ + X²/M⁴` es el funcional de apantallamiento de P10, no la acción de EO.
- Planck: espectros 2018 R3.01 (PR3); sólo el lensing es PR4.
- ΔBIC CMB: plik completo −33.83 (b1_k2.json), plik_lite −26.03 (N=669).
- k = 2 {A_s, τ} (k=1 si A_s se clava, P6).
- γ_IS = 0.5504 (P5); el 0.657/0.658 viene del fondo viscoso IS y está superado.
- DES Y3: SSEE 516.108, ΛCDM-Planck 517.290 (logs del 09-28; empate).

## Formato de `notes/lectura_cuarta/<DOC>.yaml`
```yaml
doc: P3
numeros:
  - {archivo: SSEE_Paper3_CMB.tex, linea: 150, num: "0.32", decision: VAL, nombre: rd_sig_planck, fuente: "results/logs/x.json#a.b", formato: ".2f", nota: ""}
  - {archivo: ..., linea: ..., num: "...", decision: LIT, nota: "Planck 2018 VI tabla 2, col. TT,TE,EE+lowE+lensing"}
afirmaciones:
  - {archivo: ..., linea: ..., dice: "...", debe_decir: "...", evidencia: "..."}
```
Y en `<DOC>.md`, 10–20 líneas: conteo por decisión, los FIX y afirmaciones más graves.

Tu mensaje final al coordinador: 5 líneas (conteos + los 3 hallazgos más graves + ruta).
