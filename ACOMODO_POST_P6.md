# Acomodo tras la retracción del sector φ-DM

> **Qué es esto.** Lista de trabajo de lo que quedó **descolocado** (no roto) al
> reescribirse Paper 6 el 2026-08-01. Cada ítem lleva **cómo se comprueba**, no
> solo qué hacer — para que nada entre por afirmación. Se tacha lo hecho.
>
> **Regla:** no se marca ✅ sin que la comprobación de su fila esté corrida y
> pegada. «Compila» no es comprobación (los warnings no son errores).
>
> Estado del guardián al abrir la lista: **VERDE 194/194** · memory_sync **0 drifts**.

---

## Bloque 1 — Descolocado y verificado (hallado por barrido, no de memoria)

| # | Qué | Dónde | Cómo se comprueba | Estado |
|---|---|---|---|---|
| ~~1.1~~ | ~~`.bib` con el título viejo de Paper 6~~ | `manuscript/ssee_unified.bib`, `submission_PRD/ssee_unified.bib` | `grep -c "Two-Sector"` → **0 y 0** | ✅ |
| ~~1.2~~ | ~~Endorser cita OP-9/11 como abiertos~~ | `SSEE_Endorser_Summary.tex:33` | `grep -c "OP-9/11"` → **0**; compila 0 err / 0 refs / 2 pp | ✅ |
| ~~1.3~~ | ~~CLAUDE.md con páginas viejas~~ | `CLAUDE.md`, tabla `docs/` | tabla **regenerada desde `pdfinfo`**, no a mano. También corregidas las 3 filas cuyo *estado* había quedado obsoleto (P1 §1.4, P6, P8) | ✅ |
| ~~1.4~~ | ~~`cover_galaxy.jpg` fuera de sitio~~ | — | **FALSO POSITIVO de mi barrido**: vive junto a su `.tex`, la ruta relativa resuelve | ✅ |
| ~~1.5~~ | ~~`ssee_v36_CMB_TT_comparison` fuera de sitio~~ | — | **FALSO POSITIVO**: el `.tex` usa ruta explícita `../class_ssee/output/` | ✅ |

**Barrido de figuras:** `src/verificacion/barrido_figuras.sh` → sale **vacío**.

> ⚠️ **Este barrido mintió DOS veces antes de servir**, y las dos quedan como
> lección:
> 1. Usaba `ls a.pdf a.png`, que **falla si falta cualquiera de los dos** aunque
>    el `.pdf` esté → **10 falsos positivos**. Corregido a `[ -f ]` separados.
> 2. Sólo miraba `results/figures/`, ignorando las rutas relativas al propio
>    `.tex` y las explícitas → **2 falsos positivos más** (1.4, 1.5).
>
> Moraleja anotada: **una herramienta de verificación hay que verificarla
> antes de creerle.** Las tres versiones «funcionaban»; sólo la tercera decía
> la verdad.

---

## Bloque 2 — Contramedidas que quedaron anotadas pero NO implementadas

| # | Qué | Por qué importa | Cómo se comprueba | Estado |
|---|---|---|---|---|
| ~~2.1~~ | ~~R45 al caso simétrico «OP adoptado que fue revertido»~~ | ídem | **implementado + auto-test con el encabezado REAL de OP-17 pre-arreglo** → lo marca; OP-1 y OP-5 exentos. Afinado tras 2 rondas de falsos positivos | ✅ |
| ~~2.2~~ | ~~R20 no cubría los scripts de figuras~~ | ídem | causa hallada: R20 buscaba el nombre EXACTO `kids_s8`; la figura usaba `S8_KIDS`. Ahora cada ancla lleva **alias** + tolera `= (v, err)`. **Auto-test con la línea real del bug** → la marca | ✅ |

---

## Bloque 3 — Físicas abiertas (NO son acomodo; iban con R1/R2, que se cerró el 2026-10-20 con el montaje de Chen+22)

| # | Qué | Estado |
|---|---|---|
| ~~3.1a~~ | **OP-21 REDUCIDO** — ζ̃ ya no es un número libre: la fijan τ_Π (P4) + w₀ (P1) + minimalidad. `ζ̃ = KAL₀·Ω/M_v` es **hermana** de `τ_Π = KAL₀·Ω/T_r`; el «3» era M_v=3Ω. Medido que la estabilidad marginal es el **mínimo** (menos rompe, más sobra) | 🟡 reducido |
| 3.1b-i | ⚠️ **ARREGLO RETIRADO** — era prematuro: el Ap. A de Paper 5 escribe bien la ecuación de Euler (inercia = ρ+p) pero al despejar la sustituye por ρ. Con la ζ̃ *tal como la define el paper*, c²_s,eff = **+4.41 → superlumínico**. Resolución: ζ̃ debe normalizarse por la **entalpía** (ρ+p); entonces c²_s = 0 exacto y todo se sostiene. Renombrar el símbolo NO resolvía nada: la ζ **física** la fija el ansatz Π=−KAL₀ρ_DE·H, así que el +4.41 no se movía, y mi nota al pie contradecía al párrafo siguiente. **Retirado.** Lo que SÍ queda aplicado y es firme: la corrección de la inercia (ρ→ρ+p) en el Apéndice A. El problema real es **OP-22** | 🔴 → OP-22 |
| 3.1b-ii | Derivar `τ_Π H₀ = KAL₀·Ω/T_r` del Lagrangiano, y justificar el principio de minimalidad | 🔴 abierto |
| ~~3.1c~~ | Papers: «c²_s=0 exacto» → «c²_s=0 por minimalidad» | 8 ediciones en P5 (títulos de §, teorema, §unicidad con el párrafo que separa lo determinado de lo supuesto) + Endorser. Barrido en P7/Unified/Sealed/PRD: **sin claims que corregir**. Extra: el Unified llamaba «single sector» a Ω_m=0.160 en una corrida de diagnóstico — reetiquetada | ✅ |
| 3.2 | **Veta A_s** — las tres determinaciones (CMB / cizalla / clustering) | ✅ medido: la cizalla pide el A_s del CMB (0.49σ, KiDS-Legacy); el clustering no lo fija (degenerado con el sesgo) y clavarlo al del CMB le cuesta Δχ² +2.84 frente a ΛCDM libre (`boss_chen21.json`, 2026-10-20) |
| 3.3 | **OP-18** — derivar A_s. Bloqueado *por* 3.2: no se puede validar una derivación contra un blanco que tiene dos valores | ⏳ bloqueado |

---

## Lo que NO hay que hacer

- Paper 8: predicción **incondicional** (ω_c de OP-8 + α_B=α_M=0 de Paper 7).
  ⚠️ **Aviso**: el 2026-08-02 dije «no tocar más» tras arreglar SÓLO el abstract
  y la caja de falsabilidad. Mike preguntó «¿ya quedó sólido?» y el barrido
  mostró **6 sitios más** con la construcción viva en el CUERPO (incluida una
  subsección entera y una referencia colgante a la §1.4 que yo mismo disolví).
  Arreglado en la misma sesión. **Lección: arreglar el abstract no es arreglar
  el paper**, y «lo dejé listo» sin barrido es una afirmación, no un hecho.
- **No** publicar ni sellar hasta que Mike termine la lectura página por página
  (regla R39, `project_publication_gate`).
- ~~**No** buscar mecanismo para la veta A_s antes de R1/R2.~~ (R1/R2 cerrado el 2026-10-20: ver 3.2)

---

## Bitácora

| Fecha | Qué |
|---|---|
| 2026-08-02 | Lista abierta. Inventario levantado por barrido del repo, no de memoria. Guardián VERDE 194/194. |
| 2026-08-02 | **Bloque 1 cerrado** (5/5). 3 defectos reales + 2 falsos positivos de mi propio barrido. |
| 2026-08-02 | **Paper 8 cerrado DE VERDAD**: el arreglo previo era cosmético (abstract + caja). El cuerpo tenía 6 sitios vivos: definición del límite (b) sobre «Ω_CDM=0.160, Ω_φDM=0.149», la falla de categoría otra vez, referencia colgante a Paper 1 §1.4 (disuelta), subsección entera «Two-sector lensing signature», dos filas de la tabla de referencia y el ejemplo de A1689. Barrido final: sólo queda prosa de retracción. 0 err / 0 refs / 19 pp. |
| 2026-08-02 | **REPASO pedido por Mike antes de seguir.** Encontró que mi propio arreglo 3.1b-i, hecho ese mismo día, era prematuro y creaba una contradicción interna. Retirado. Tres hallazgos: (1) con la inercia correcta el c²_s de P5 sale **+4.41 superlumínico**; (2) renombrar el símbolo no lo arregla porque la ζ física la fija el ansatz; (3) la atribución «Paper 1 identifies…» es **huérfana** — P1 no contiene esa ecuación. Registrado como **OP-22**; P5 lleva ahora una caja declarando sus resultados Q1 condicionales. **Lección: mi propio arreglo necesitaba el mismo escrutinio que el defecto que arreglaba.** |
| 2026-08-02 | **Bloque 2 cerrado** (2/2). Guardián **VERDE 197/197** (piso 194→197). Hallazgo extra: OP-5 tenía el encabezado desfasado respecto a su fila del resumen — lo destapó el detector nuevo al dar un falso positivo sobre él. |
