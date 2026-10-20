# BANDEJA — trabajo hecho sin Mike delante

**Abierta 2026-09-08, a petición de Mike.** Nace de una frase suya: *«te dejo
solo, pero como tenía miedo de que pudiera haber un error mientras no estoy
pendiente, te designo un área donde puedes trabajar»*.

## La regla, y es la única que importa

**Nada de esta carpeta entra a un paper, al Registro, a CANONICAL_VALUES.yaml
ni a CLAUDE.md hasta que Mike lo lea y lo apruebe.** Aquí se acumula; el
traspaso es un acto suyo, después, y es la parte fácil.

Esto NO es una excepción al orden de propagación (`[[project_propagation_order]]`).
Es su antesala: el trabajo se hace cuando la corrida termina, no cuando Mike
está despierto, y espera aquí a que él decida si vale.

## Qué va en cada informe

Un archivo por corrida, `AAAA-MM-DD_<corrida>.md`, con:

1. **Qué se preguntó** y qué corrida la contesta (número de la cola).
2. **El número**, con su incertidumbre, y separando medido de deducido.
3. **Su control** (R53). Sin control el informe se marca INCOMPLETO y no
   se propone para traspaso.
4. **Qué documentos tocaría** si Mike lo aprueba, con línea y archivo.
5. **Qué NO toca**, explícito.
6. **Lo que no cerró** — candidato a OPEN_PROBLEMS, nunca omitido.

## Estado

| informe | corrida | estado | listo para traspaso |
|---|---|---|---|
| `2026-09-08_R4_lcdm_kids.md` | `analiza_lcdm_R4` | ✅ completa, control PASA | **no hace falta** — ningún número se mueve; sólo repone el log |
| `2026-09-08_perfil_wc_boss.md` | `perfil_wc_boss` | ✅ completa, control PASA | 🔴 **RETIRADO 2026-10-20** (BOSS de 2017; re-medido en el montaje de Chen+22: `perfil_wc_boss_chen21.json`) · antes: ✅ **TRASPASADO 2026-09-08** — Paper 6 §par:wc-profile, OP-19, Registro |
| `2026-09-08_perfil_wc_boss_lcdm.md` | `perfil_wc_boss_lcdm` | ✅ completa, control PASA | 🔴 **RETIRADO 2026-10-20** (ídem) · antes: ✅ **TRASPASADO 2026-09-08** — junto con su hermano |

## Corriendo mientras Mike duerme (2026-09-08)

| corrida | lanzada | qué contesta |
|---|---|---|
| `cobaya_kids lcdmfijo` | 07-09 19:43 | la casilla que falta: ¿ΛCDM con fondo fijo también muestra la tensión en `A_s`? |
| ~~`perfil_wc_boss`~~ | 08-09 06:05 | ✅ terminada 06:18 |
| ~~`perfil_wc_boss_lcdm`~~ | 08-09 06:22 | ✅ terminada 06:38 |
