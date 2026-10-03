# β_c y el fondo acoplado — RETIRADOS 2026-09-07

## Por qué están aquí

Paper 7 **retiró** el potencial exponencial y el acoplamiento conformal
de la acción (`§withdrawn`, L80). El Lagrangiano vigente es

```
K(X) = c1 X + c2 X^2
```

y **no lleva ni acoplamiento ni potencial**. Estos seis scripts integran
o barren ese fondo retirado, así que ya no reflejan lo que el modelo
dice hoy. No se borran: son el registro de cómo se llegó a retirarlo.

## Qué contienen

| script | qué hacía |
|---|---|
| `ssee_eft_verification.py` | verificaba la acción k-essence **interactuante** (la retirada); producía `fig_eft_beta_convergence` y `fig_eft_verification`, que no cita ningún `.tex` |
| `fondo_acoplado.py` | fondo con acoplamiento, disparo desde época temprana |
| `bc_autoconsistente.py` | β_c con el acoplamiento realimentado |
| `barrido_beta_c.py` | barrido: dónde deja de haber solución |
| `barrido_beta_c_fino.py` | barrido fino entre +0.10 y +0.24 |
| `omega_m_efectivo.py` | qué materia «cree ver» BAO con la materia acoplada |

## Los tres errores que arrastraban

1. **El «β_c = −AURA verificado a <0.2%» era un bug.** El shooting
   calibraba `Ω_φ(a=1)` a `0.839950` (la saturación) en vez de
   `0.691119` (la densidad). Corregido da **`−2.194210`**, a **45%** de
   AURA — no a 0.2%.
2. **Se derivaba de la `K(X)` equivocada.** `P(X) = X/KAL₀ + X²/M⁴` es
   el funcional de **apantallamiento de Paper 10**, no la acción de
   energía oscura. Cuarta aparición de esa confusión.
3. **La brecha que β_c cerraba no era física.** `w = −1 + λ²/3` con
   `λ = √(3(1+w₀))` devuelve `w₀` con diferencia `0.000e+00`: tautología.

## Qué sigue vivo, y dónde

**OP-23 sigue abierto**, pero es otra pregunta: **ningún fondo reproduce
`wₐ = −0.670`** (atractor `−0.093`; `λ=1.0205` da `−0.211`; el acoplado
da `+0.406`, con el signo contrario). El problema es la **forma del
potencial**, no `β_c`.

Su investigación viva se quedó en `src/p07_eft/`:
`busca_lambda.py`, `fondo_viscoso.py`, `resuelve_op23.py`.

## Las figuras

`fig_eft_beta_convergence` y `fig_eft_verification` (`.pdf` y `.png`)
están en `archive/figuras/`. No las citaba ningún `.tex`.

## Reproducción de los números retirados (2026-10-02)

`reproduce_2026-10-02.py` extrae `src/` del commit `d849df0` y corre
`ssee_eft_verification.py` con una sola línea cambiada (la de `M⁴`) en tres
variantes: físico (`5φ⁸ρ_crit`, sin tocar), convención (`M⁴=1`, la retirada) y
sin `X²/M⁴`. Deja `reproduccion_2026-10-02.json` con acta. De ahí salen, con
procedencia, los `β_c = −2.194210`, `−0.691265`, `−0.666255` y sus `w`, `φ̇` y `X`
que citan OPEN_PROBLEMS, el Registro y CLAUDE.md. Control: la variante física
reproduce el `−0.691265` que `d849df0` escribió en su propio comentario.
