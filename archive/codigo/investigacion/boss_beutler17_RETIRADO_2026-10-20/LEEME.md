# BOSS DR12 sobre los espectros de Beutler+2017 — RETIRADO 2026-10-20

Aquí está todo lo que medía BOSS con el montaje anterior. Lo reemplaza el montaje
de Chen, Vlah y White 2022 (arXiv:2110.05530), con control:

- script: `src/p06_growth/cobaya_boss_chen21.py` (control ΛCDM libre),
  `src/p06_growth/cobaya_boss_chen21_fijo.py` (SSEE y ΛCDM-Planck clavados),
  `src/p06_growth/analiza_boss_chen21.py` (etapa DVC `analiza_boss_chen21`);
- log: `results/logs/growth_2026-07/boss_chen21.json`; Paper 6 lo cita por `\val{bossC_*}`.

## Por qué se retira

El montaje viejo tenía tres errores, y los tres afectaban a los dos modelos por igual:

1. **Bines solapados.** Los tres bines públicos (0.2–0.5, 0.4–0.6, 0.5–0.75) se solapan
   y sus covarianzas vienen sin términos cruzados; usar los tres contaba dos veces las
   galaxias comunes (Δχ² −2.03 → −0.33). Corregido el 2026-10-17 (sólo z1 y z3).
2. **A_s lineal sobre la salida a un lazo.** La tabla LPT se hacía una vez a A_REF y la
   salida se escalaba por A_s/A_REF; a un lazo eso es falso (+3.88 en χ² en el mejor
   punto de SSEE). Corregido el 2026-10-17 (tablas en nodos de logA).
3. **Espectros de 2017.** Llevan el desajuste de normalización de ~10 % que corrigieron
   Beutler & McDonald 2021 (medido aquí: P₀ viejo/nuevo = 0.90–0.92), que baja σ₈.

Con el montaje viejo el control ΛCDM quedaba hasta 1.1σ de lo publicado. Con el de
Chen+22 queda a −0.13/−0.10/−0.11/−0.25σ en logA/Ω_m/H₀/σ₈ (criterio 0.3σ, fijado antes).

## Qué números quedan retirados (no citar como vigentes)

- Δχ² SSEE−ΛCDM de BOSS **−2.03** (tres bines) y **−0.21** (R1/R2, z1+z3, A_s escalado);
- χ² de BOSS en el logA del CMB (**0.60**, antes 0.63) y su «costo de clavar A_s»;
- el `ω_c` que pide BOSS por perfil (SSEE 0.117450, ΛCDM 0.114346) y su ganancia;
- los perfiles de logA de BOSS, el término de volumen, la separación de neutrinos;
- las conjuntas CMB+KiDS+BOSS (`conjunta`, `conjunta_b3`, `conjunta_control`).

El vigente: χ² crudo de 144 puntos, SSEE todo clavado 117.10 contra ΛCDM libre 114.26
(Δχ² +2.84, ΔBIC −12.1); ΛCDM-Planck clavado 115.34. Empate.

## Qué hay aquí

| archivo | qué hacía |
|---|---|
| `cobaya_boss.py`, `analiza_boss_R1R2.py` | cadenas R1/R2 y su lectura (log `R1R2_boss_lpt_cobaya.json`) |
| `cobaya_boss_lcdm_libre.py`, `analiza_boss_lcdm_libre.py` | primer control ΛCDM libre (no reproducía lo publicado) |
| `mide_interpolacion_logA.py` | prueba de la interpolación en logA con los datos viejos (la vigente: `boss_chen21_malla.json`) |
| `mide_termino_volumen.py`, `marginal_vs_perfil.py` | término log det F y marginal contra perfil |
| `perfil_wc_boss.py`, `perfil_wc_boss_lcdm.py`, `minimo_sesgos.py`, `ganancia_wc_libre.py` | perfil de `ω_c` |
| `boss_chi2_en_logA_cmb.py` | χ² de BOSS con el logA del CMB |
| `boss_aisla_neutrinos.py` | separación método/neutrinos (tres bines) |
| `cobaya_conjunta.py`, `leer_conjunta.py`, `vigila_y_lee.sh`, `conjunta_perfil_logA.py` | conjuntas CMB+KiDS+BOSS |
| `verifica_boss.py` | verificación de la lectura de los ficheros de 2017 |

Los logs están en `archive/logs_superados/boss_beutler17_2026-10-20/`. Las cadenas
siguen en disco en `/mnt/datos/SSEE_data/chains_p6/{boss,conjunta}/` (no se borran).

## Lo que siguió vivo

- `src/p06_growth/boss_lpt_R1R2.py`, `boss_rsd_model.py`, `boss_dr12_data.py`: biblioteca
  del montaje nuevo (nodos de logA, tablas LPT, Alcock-Paczynski).
- `multisonda_fondo_clavado.py` y `mide_As_o_producto.py`: se les quitó BOSS y dan los
  mismos números que antes (BOSS no votaba en amplitud; la parte de KiDS es idéntica).
- `coteja_transcripciones.py`: sin las transcripciones del BOSS viejo ni la cabecera b3.

El guardián vigila el BOSS vigente: FaseB (log con acta y Δχ²), R79 (sólo z1 y z3) y
R80 (A_s por la tabla, malla contra tablas exactas con el control del método viejo).
