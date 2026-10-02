# Huérfanos archivados el 2026-10-02

Dos scripts que ningún documento cita y cuyos resultados no son física vigente.
Salieron a la luz porque R36 los marcaba como rancios. Al regenerarlos, el log
mostró que el problema no era la fecha: era el contenido.

## ssee_paper3_hiclass_check.py (P3, mayo 2026)

- Mete **Ω_m,dyn = 0.160** en la geometría de CLASS (`omega_cdm = (0.160 − 0.049)·h²`).
  Ese número es 1+w₀, una cantidad de la ecuación de estado, no una densidad (banner del
  2026-07-09). Con eso sale **χ²_r(TT) = 90.3** contra 1.2 de ΛCDM: es el bug, no el modelo.
- Compara el C_ℓ **sin lente** (`raw_cl`) contra el dato **con lente**, con A_s = 2.1e-9
  tecleado y sin neutrinos.
- Su «αK(z) desde CLASS, Δ = 0.005 %» es la misma sustitución hecha dos veces: en z=0,
  E=1 y `Om_DE·ratio/E²` devuelve el valor algebraico por construcción. Ya lo había
  anotado R52 (2026-08-10) y `ssee_paper9_verification.py`.
- **Lo reemplaza** `src/p07_eft/hiclass_campo.py` (etapa DVC `hiclass_campo`), que es el
  que cita P7 con `\val`.

## ssee_eftcamb_validation.py (P7, mayo 2026)

- Corre EFTCAMB con **w = −0.84 constante**, no con el CPL del modelo, a H₀ y ω fijos.
  Los picos se corren a ℓ = 242/590/893 (RMS 41 % contra GR) y sale σ₈ = 1.026. Las
  figuras `ssee_eftcamb_CMB_TT` y `ssee_eftcamb_Pk` mostraban ese régimen, no SSEE.
- Ningún .tex incluye ya esas figuras. El Unified solo conserva la historia del segfault
  en el cruce fantasma (§eftcamb) y P7 los parámetros de entrada.

## Qué hay aquí

- los dos scripts, con la cabecera de procedencia que se les puso el 2026-10-02;
- `figuras/`: las figuras tal como estaban commiteadas (no las regeneradas);
- `logs/`: los logs de la re-corrida del 2026-10-02, que muestran los números rotos
  (χ²_r 90.3; picos 242/590/893);
- `hiclass_summary.txt`: la tabla de mayo.
