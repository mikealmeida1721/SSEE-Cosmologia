# Dos corridas de KiDS-1000 que ninguna etapa lee (septiembre 2026) — archivadas 2026-10-16

**Motivo: superadas por KiDS-Legacy y sin lector.** Las encontró el cotejo de transcripciones
(`src/verificacion/coteja_transcripciones.py`) al pagar la deuda R75: ninguna etapa de
`dvc.yaml` lee sus cadenas y ningún documento cita sus números. El crecimiento vigente se mide
contra KiDS-Legacy (`kids_legacy_bic`, `s8_kids_legacy_camb`); el control ΛCDM de KiDS-1000
vigente es R4 (`analiza_lcdm_R4`).

| archivo | qué era |
|---|---|
| `kids_ssee_wc_h.log` | SSEE con el fondo rígido salvo ω_c y H, contra KiDS-1000. Se cortó el 2026-09-10 a las 03:39 sin terminar (≈4 400 aceptados por cadena, sin «Sampling complete»); su cadena es `/mnt/datos/SSEE_data/chains_p6/kids/ssee_wc_h.*`. |
| `kids_lcdm_fondofijo_reparto.log` | ΛCDM con su fondo Planck fijo contra KiDS-1000, terminada y convergida: 24 805 pasos, igual a las filas de `/mnt/datos/SSEE_data/chains_p6/kids/lcdmfijo.*` (cotejado). Nadie la lee. |

**Archivos de esta carpeta** (lista exacta, la que comprueba R77):
- `kids_lcdm_fondofijo_reparto.log`
- `kids_ssee_wc_h.log`
