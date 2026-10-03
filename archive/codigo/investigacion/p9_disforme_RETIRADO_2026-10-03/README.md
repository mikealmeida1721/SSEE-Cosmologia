# Paper 9 — lo retirado el 2026-10-03

- `fig_paper9_fscreen_z.{pdf,png}`: f_screen(z) escalando s_K con un Ω_DE(z)
  construido con Ω_m = 1 − 0.840 = 0.160. Ese 0.160 es 1+w₀ (ecuación de
  estado), no una densidad; y la curva contradecía el Paso 4 del propio paper
  (f contiene sólo w₀ y es constante a todo z). La generaba la versión anterior
  de `src/p09_hubble/ssee_paper9_figures.py` (ver git log de ese archivo).
- En el texto de P9 se retiraron, declarándolo: MIRA como acople óptico de la
  geodésica disforme de P8, la compresión disforme de d_L y el paso de universo
  separado (cancelaba Ω_m/(1+w₀) con la falsa identidad 1+w₀ = Ω_m). La forma
  multiplicativa queda como POSTULADO (P9 §3.4). Ver OPEN_PROBLEMS.md OP-8b.
- El control «Freedman 69.96 → 65.26, 1.88σ» usaba la v1 de arXiv:2408.06153;
  la v3 adopta 70.39 ± 1.94 y el control vigente vive en
  `results/logs/p9_cascada_control.json`.
