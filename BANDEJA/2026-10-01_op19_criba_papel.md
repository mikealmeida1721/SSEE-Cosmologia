# OP-19 — Criba en papel de las cuatro familias (2026-10-01, noche)

> Primer paso del plan de OP-19 (decisión de Mike, commit cf695c8). **Sin corridas.**
> Blanco: ω_c/ω_b = KAL₀·n_s = KAL₀·(1 − 2/N_*), con N_* = 2φ⁷.
> Reglas pre-registradas: (1) cero perillas ajustadas al blanco; (2) predice algo más y no rompe nada;
> (3) con blancos falsos tiene que FALLAR; (4) capa 1 (ω_c ∝ ω_b) antes que capa 2 (el coeficiente).
> **Las referencias van marcadas «→ Nova»: son de memoria y nada se cita sin que Nova las verifique.**

## Las dos preguntas por familia

- **Capa 1.** ¿La familia hace que ω_c sea proporcional a ω_b *sin elegirlo*, por un origen compartido?
- **Capa 2.** ¿La abundancia contiene de forma natural N_* o la pendiente de la caída del inflatón, de modo
  que (1 − 2/N_*) aparezca sin insertarlo?

## 1 · Freeze-out (reliquia térmica, tipo WIMP)

- **Qué fija la abundancia.** La sección eficaz de aniquilación ⟨σv⟩ y, débilmente, la masa por x_f = m/T_f.
- **Capa 1: no.** La abundancia no sabe nada de los bariones; el cociente ≈5 sería una coincidencia.
- **Capa 2: no.** No aparece N_*; el freeze-out ocurre mucho después de la inflación y borra la memoria de ella.
- **Variante que sí toca la capa 1: materia oscura asimétrica** (Kaplan, Luty y Zurek 2009 → Nova). Una
  asimetría compartida da n_c ≈ n_b, y entonces ω_c/ω_b ≈ m_c/m_p × (factor de transferencia). El ≈5 pasa a
  ser una **masa** (unos 5 GeV).
  - **Cómo cae.** La masa sería una perilla elegida para acertar el blanco (regla 1). Que la masa saliera de
    KAL₀·n_s exigiría una razón para que el inflatón fije la masa de la partícula, y en esta familia no la hay.
  - **Además:** el puente n_c = n_b se apoyaba en la bariogénesis de OP-1, que quedó EXCLUIDA el 2026-09-08
    (OPEN_PROBLEMS, línea del puente al sector oscuro).
- **Veredicto:** capa 1 posible solo en la variante asimétrica, con la masa libre; **capa 2 ausente.**

## 2 · Freeze-in (producción fuera de equilibrio)

- **Qué fija la abundancia.** Un acoplamiento muy débil y, en el caso UV, la temperatura de recalentamiento
  T_rh (Ω ∝ potencia de T_rh).
- **Capa 1: no** por sí sola: el acoplamiento a los bariones no es obligatorio.
- **Capa 2: indirecta y débil.** N_* sí depende del recalentamiento, pero **logarítmicamente**:
  N_* ≈ cte + (1/3)·ln(T_rh/…) para recalentamiento tipo materia (Liddle y Leach 2003 → Nova). La abundancia
  depende de T_rh como **potencia**. Una dependencia logarítmica en n_s no se convierte en el factor *lineal*
  (1 − 2/N_*) de la abundancia sin una función elegida a mano.
  - **Cómo cae:** regla 1. Para que salga KAL₀·(1 − 2/N_*) habría que ajustar el acoplamiento.
  - Además, en SSEE N_* = 2φ⁷ está fijo por el álgebra, no derivado de T_rh: el puente iría al revés.
- **Veredicto:** comparte una variable con la caída (T_rh), pero **no produce la forma del blanco.**

## 3 · Misalignment (campo ligero tipo axión)

- **Qué fija la abundancia.** El ángulo inicial θ_i, la escala f y la masa (Ω ∝ m^{1/2} f² θ_i² para un ALP).
- **Capa 1: no.** No hay conexión con los bariones.
- **Capa 2: no** de forma natural. La inflación entra por las fluctuaciones de θ (isocurvatura,
  ∝ H_inf/f). En el régimen estocástico de inflación larga el ángulo de equilibrio depende de H_inf y m, no
  de N_* (se olvida el número de e-folds una vez que N es grande).
  - **Cómo cae:** sin capa 1 falla la regla 4 antes de llegar a la capa 2. Además, cualquier θ_i elegido
    para acertar es una perilla (regla 1).
- **Veredicto:** **descartada** para OP-19.

## 4 · Producción gravitacional / en el recalentamiento (decaimiento del inflatón)

- **Qué fija la abundancia.** Para el decaimiento del inflatón:
  n_DM/s ≈ (3/4)·(T_rh/m_φ)·BR(φ→DM). La bariogénesis no térmica desde el mismo decaimiento da
  n_B/s ≈ (3/4)·ε·(T_rh/m_φ)·BR(φ→N)·(factor esfalerón).
- **Capa 1: SÍ, de forma natural.** El factor T_rh/m_φ es **el mismo** y se cancela en el cociente:
  ω_c/ω_b = (m_DM/m_p)·BR_DM/(ε·BR_N·factor). Es la idea de un origen común barión–materia oscura en el
  decaimiento de un campo (cladogénesis: Allahverdi, Dutta y Sinha 2011 → Nova; también Kitano, Murayama y
  Ratz 2008 → Nova). **Es la única de las cuatro donde la proporcionalidad sale sin elegirla.**
- **Capa 2: no aparece.** Lo que queda en el cociente son una masa, cocientes de ramificación y la asimetría
  CP ε. Ninguno contiene N_* ni la pendiente de la caída. En un α-atractor, la masa del inflatón en el mínimo
  y n_s = 1 − 2/N_* comparten la forma del potencial, pero m_φ **se cancela** en el cociente: justamente lo
  que vincularía con la caída es lo que desaparece.
  - **Cómo cae (a buscar):** que KAL₀·n_s se reproduzca solo eligiendo BR_DM/BR_N, lo cual violaría la
    regla 1. Para que no caiga, BR_DM/BR_N tendría que venir de los acoplamientos fijados por φ y π, y eso
    hoy no existe.
  - **Producción puramente gravitacional** (Chung, Kolb y Riotto 1998 → Nova; Garny, Sandora y Sloth 2016
    → Nova): depende de H al final de la inflación y de T_rh. Sí lleva memoria de la caída (H_e), pero no
    tiene conexión con los bariones (capa 1: no).
- **Veredicto:** **la mejor candidata para la capa 1**; la capa 2 no sale de forma natural.

## Resultado de la criba

| familia | capa 1 (ω_c ∝ ω_b) | capa 2 (aparece 1 − 2/N_*) | estado |
|---|---|---|---|
| freeze-out | solo en la variante asimétrica, con la masa libre | no | cae por la regla 1 |
| freeze-in | no | indirecta (log T_rh), no da la forma | cae por la regla 1 |
| misalignment | no | no | descartada (regla 4) |
| decaimiento del inflatón (cladogénesis) | **sí, natural** (T_rh/m_φ se cancela) | no (m_φ se cancela) | **sigue viva para la capa 1** |

**Lo que dice la criba, sin adornar:**

1. **Ninguna de las cuatro familias contiene de forma natural el factor n_s.** Según el plan, eso también es
   resultado: el factor (1 − 2/N_*) **pediría física nueva**, o la identidad tiene otra lectura.
2. **La capa 1 sí tiene un hogar natural:** el decaimiento común (inflatón o módulo) a bariones y a materia
   oscura. Es el siguiente lugar donde intentar derribar.
3. **El hueco (i) de tu hipótesis sigue en pie y la criba lo agrava.** En el decaimiento común, lo que lleva
   memoria de la caída (m_φ, H_e) se cancela justo en el cociente que necesitamos. Para que la inclinación
   reduzca la retención, el factor tendría que entrar *después* del cociente, en algo como una eficiencia de
   transferencia, y ninguna familia la tiene.

## Siguiente paso (propuesta, sin corridas todavía)

- **Derribar la cladogénesis con las reglas.** ¿Puede BR_DM/BR_N salir de acoplamientos fijados por φ y π sin
  elegirlos? Si la única forma es elegirlos, cae por la regla 1.
- **Control R53 en papel:** con el blanco falso ω_c/ω_b = 4 (o con n_s = 0.95), ¿se acomodaría igual de bien
  eligiendo BR? Si sí, el mecanismo no predice el coeficiente y solo sirve para la capa 1.
- **Nova:** verificar las cinco referencias marcadas y buscar artículos donde la abundancia de materia oscura
  dependa de N_* o de n_s de forma no logarítmica (si existen, son los que pueden refutar o salvar la capa 2).
