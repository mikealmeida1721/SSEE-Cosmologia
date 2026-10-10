# Tercera lectura — instrucciones comunes para los agentes (2026-10-10)

Encargo de Mike: dejar el repositorio listo para la nueva versión de Zenodo y luego
la revista (PRD). Revisión **hoja por hoja, carpeta por carpeta**: contradicciones
entre papers, citas y fuentes correctas, reproducibilidad, nada de números a mano
sin registro, nada de conceptos viejos que el modelo ya no sostiene.

## Reglas duras

1. **SÓLO LECTURA.** No edites ningún archivo del repositorio salvo TU informe en
   `notes/lectura_tercera/<tu_id>.md`. Claude (el coordinador) aplica los arreglos.
2. **No corras** `src/verificacion/ssee_verify.py`, `test_guardian.py`,
   `mutacion_guardian.py` (mutan archivos y usan cerrojo), ni `dvc`, ni cobaya,
   CAMB, CLASS, MCMC, ni nada pesado. No toques procesos en curso (hay corridas de
   DES y una cola DVC). Python ligero sí: leer JSON de `results/logs/`, evaluar el
   álgebra con `src/ssee_core.py`, consultar Crossref/arXiv.
3. **Todo en español** en el informe.
4. **Verifica antes de reportar** (escrutinio SIMÉTRICO: lo bueno y lo malo con la
   misma dureza). Antes de llamar defecto a algo, busca la salida: ¿hay una decisión
   ya tomada que lo explica (banners de `CLAUDE.md`, `CANONICAL_VALUES.yaml`,
   `RETRACCIONES.yaml`, `OPEN_PROBLEMS.md`)? Marca la confianza (ALTA/MEDIA/BAJA).

## Fuentes de verdad (en este orden)

- `CLAUDE.md` (banners al tope: dirección de la cascada, partícula retirada,
  Ω_m-geometría, idioma) — manda sobre las tablas de abajo del mismo archivo.
- `CANONICAL_VALUES.yaml` y `src/ssee_core.py` (el núcleo algebraico).
- `manuscript/valores_generados.tex`: cada macro `\val{NOMBRE}` dice en su
  comentario de qué log y clave sale. Un número que va por `\val` ya está trazado;
  verifica que el log diga eso (abre el JSON).
- `results/logs/*.json` (resultados con acta `_procedencia`).
- `RETRACCIONES.yaml` / `RETRACTIONS.md`: lo retirado. Si aparece como VIGENTE en
  un documento, es defecto (si aparece narrado como histórico/retirado, no).
- `OPEN_PROBLEMS.md`: qué está abierto y qué cerrado.

## Decisiones vigentes que más se cuelan (verificar SIEMPRE)

- **H₀:** el H con unidades es `H_glob = H_SH0ES(1−f_screen) = 73.04×(1−0.069522) = 67.962142 ± 0.968`.
  `3(φ+π)² = 67.96214` es el BLANCO puro (sin unidades), NO entrada, NO «anchor»,
  NO «Postulate D», NO «prediction of H₀». 68.13 es el régimen IR (no canónico). 72.86 y 73.040 retirados.
- **Materia:** UN SOLO SECTOR, Ω_m = ω_m/h² = 0.308881. `s_m = 1+w₀ = 0.160` es
  ecuación de estado, NUNCA densidad («Ω_m,dyn», «cold sector» como densidad = retirado).
  Sin factor MIRA de materia (0.31993, 0.3201, π/φ→0.31076 retirados).
- **Partícula φ-DM** (m_φ=40.70 eV, Ω_φDM, k_fs, two-sector) RETIRADA 2026-08-01.
- **S₈:** titular KiDS-Legacy 0.8273 predicho vs 0.8265±0.0176 (0.04σ), A_s clavado
  al CMB. KiDS-1000 0.7559±0.0189 es antecedente. No reclamar prioridad sobre KiDS-Legacy.
- **c_s² de la energía oscura = 0.021284** (condensado de P7; P5 da ≈0 como
  descripción de fluido de la misma onda). El 0.967 de P10 es del funcional de
  apantallamiento, que NO es la acción de energía oscura.
- **α_K:** pendiente conocido: `α_K(0)=0.403302` aparece rotulado como kineticidad
  en P3, P8, Unified, Sealed y PRD, contra P7 (α_K=15.591335). Investígalo en tu
  documento: qué es 0.403302 (es s_K^IR, la fracción) y qué es α_K en P7.
- **β_c = −AURA RETIRADO** (2026-09-07). KAL₀ es RETENCIÓN (ω_c = KAL₀ ω_b n_s), nunca
  amplificador de gravedad / lectura MOND como vigente.
- **Espectros Planck**: son Planck 2018 R3.01 (PR3), no «PR4» (salvo el lensing PR4).
- **k=2** {A_s, τ} a nivel CMB (k=1 si A_s se clava; ver P6).
- ΔBIC CMB titular: full plik −33.83 (b1_k2.json); plik_lite −26.03.

## Las SEIS dimensiones (cada página)

| # | dimensión | pregunta |
|---|---|---|
| 1 | Valores | ¿cada número es el redondeo correcto de su fórmula / log? |
| 2 | Relaciones | `=` exacto, `≈` truncado, `∼` orden de magnitud: ¿el signo dice lo que afirma? |
| 3 | Entidades | ¿cada símbolo es la entidad correcta y no otra con el mismo valor? |
| 4 | Coherencia | ¿contradice otra parte del mismo documento u otro paper? |
| 5 | Trazabilidad | ¿se puede señalar de dónde sale cada número y afirmación (`\val`, log, cita, `% ORIGEN`)? |
| 6 | Legibilidad | ¿un lector lo comprueba de un vistazo? |

Las figuras cuentan como afirmación (pie de figura, valores en la figura, de qué script salen).

## Cómo leer

- Fuente: el `.tex`. Para numerar páginas usa el PDF compilado de `docs/` con
  `pdftotext -layout docs/<nombre>.pdf -` (las páginas van separadas por `\f`).
- Números escritos a mano en el `.tex` (no `\val`) con ≥3 cifras significativas:
  busca su origen (comentario `% ORIGEN-VALOR`, log, cita). Si no lo hay, repórtalo.
- Citas: para cada afirmación con dato externo (Planck 67.36±0.54, DESI, SH0ES 73.04±1.04,
  KiDS, etc.) comprueba que la cita adjunta es la fuente correcta y que el número
  coincide con esa fuente.

## Formato del informe `notes/lectura_tercera/<tu_id>.md`

```
# <documento> — tercera lectura (agente <id>, 2026-10-10)
## Resumen
N hallazgos: X contradicción · Y retirado-vigente · Z número-sin-origen · W valor-erróneo · V cita · U redacción
## Tabla por página
| pág | secciones | estado (✅ limpia / ⚠ con hallazgos) | hallazgos # |
## Hallazgos
### H1 · pág P · archivo.tex:LÍNEA · dimensión N · TIPO · confianza ALTA
- Dice: «...»
- Debe decir / por qué: ... (evidencia: log + clave, fórmula, o fuente con URL/DOI)
- Reemplazo propuesto (exacto, LaTeX): `viejo` → `nuevo`   (si es claro; si requiere decisión, dilo)
```

Tu mensaje final al coordinador: 5–10 líneas con el conteo, los 3 hallazgos más
graves y la ruta del informe. Nada más (el detalle va en el archivo).
