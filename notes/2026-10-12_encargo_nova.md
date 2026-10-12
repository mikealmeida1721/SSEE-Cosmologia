# Encargo a Nova — verificar la cuarta y quinta lectura (65ad1a3..HEAD)

Fecha: 2026-10-12. Rama: `lectura-publico-2026-09-26`. Último push verificado en
`SSEE-Cosmologia/main`: `65ad1a3` (2026-10-10). Desde ahí, 82+ commits de Claude.
Protocolo de siempre: Nova verifica en el remoto, corriendo las cosas, no leyendo
este resumen. Nada va a `main` hasta que los dos coincidan.

## Lo que más importa verificar (cambia lo que el modelo dice)

1. **P2, titular k = 0** (`3043d3b`, `dd6489b`): SSEE sin nada libre (ω_b algebraico,
   H de la cascada) frente a DESI DR2 + Planck: ΔBIC −10.90 (ΛCDM) / −9.32 (CPL).
   La versión conservadora k = 2 queda −5.81 / −4.24. Log `p2_ssee_fijo_k0.json`.
   Revisar: que BIC use ln L (no el posterior; `8ae1a27`) y que el N y el k sean los
   del log.
2. **P5 reescrito** (`ccbab90`, `781b86b`, `78c89df`, `1eb5da8`): con c²_bare = w₀ el
   modo creciente del sistema Israel–Stewart completo es inestable a todo k; la
   estabilidad la da el c²_s = +0.021284 del campo de P7. El viejo R = 0.9897 salía
   de una integración con la gravedad al revés. Literatura: Kunz–Sapone para la
   inercia total en el cruce.
3. **P7, el campo rueda** (`7be5d70`, `ca872f4`): w_a propio +0.41, hacia w = −1, sin
   cruzarlo; Eckart sobre él da 7.8σ. Por qué cruza el w(a) algebraico es OP-24
   (z = 0.314). Log `p7_fondo_campo.json`.
4. **P10, C.1 es Conjetura** (`c343f53`, `8246d03`, `b9a6764`): la cascada de Hubble
   no mide M⁴ (banda ±0.968); la pata de Hubble sólo vota si r < 0.0028. Un solo
   nombre en P8/P9/P10/OPEN_PROBLEMS.
5. **DESI en el Unified** (`d896ad8`): w₀ = −0.838 ± 0.055 y w_a = −0.617 ± 0.208 son
   momentos de las cadenas oficiales (como P2); el publicado de w_a es
   −0.62^{+0.22}_{−0.19}. El 0.057 que había era el σ de DESY5.

## Cifras corregidas contra su log (muestrear)

R−1 del MCMC multi-sonda 0.020 (no < 0.005; `mcmc_full_posteriores.json#gelman_rubin`) ·
N_eff P2 79 203 · ℓ₁ = 220 · quinta fuerza 6e-13 a 10 kpc · quitar ω_ν mueve Ω_m 0.5 %
· KiDS-1000 log A a 3.6σ del CMB · r_drag 0.10σ · w₀ 1.74σ · Y_p 0.2471 (0.6σ) ·
el «0.05σ contra DR1» retirado (sin log) en PRD, Sealed y README.

## Para el expediente de firmas (literatura, con signo)

- A favor: k = 0 frente a DESI DR2 + Planck (ΔBIC −10.90).
- Neutro: S₈ KiDS-Legacy 0.04σ (sin prioridad temporal; KiDS-Legacy es de 2025-03).
- Abierto: OP-24 (por qué cruza w = −1) y C.1 (M⁴ no medido por la cascada).

## Estado del árbol al escribir esto

PDF de `docs/` recompilados (`784a68a`, R68 0). `cola_1010` sigue en
`lcdm_conjunta_min_kids` (Nelder-Mead, reinicio 3 con mejora 0.04, TOL 0.02); detrás
quedan `_bao`, `_conjunta`, `_control`, `_lee`, `auditoria_pdfs_zenodo` y `des_y3_nla`.
El push al remoto espera la confirmación de Mike.
