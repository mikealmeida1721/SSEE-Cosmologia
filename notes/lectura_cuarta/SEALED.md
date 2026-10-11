# Cuarta lectura — SEALED (SSEE_Sealed_Journal.tex)

104 números del inventario cubiertos en 74 entradas (muchas repiten la misma
entidad en 2-9 lugares del documento; agrupadas con "repite Lxx").

## Conteo por decisión
- VAL: 27 (incluye los ~15 casos de FIX-lite: macro \val YA EXISTE pero el
  texto teclea el número a mano)
- DERIVADO: 15 (cuentas verificadas con `src/ssee_core.py` o contra logs
  ligeros; incluye la tabla look-elsewhere completa, VERIFICADA EXACTA contra
  `results/logs/look_elsewhere_full.log`)
- LIT: 13 (datos externos: DESI DR2 eqs.25-28, Planck 2018, PDG, BBN Schoneberg2024)
- HIS: 7 (valores retirados narrados correctamente como historia: 67.037/66.533/
  66.412/67.159, 3.5σ, 13.9σ, 0.05σ DR1)
- TRIVIAL: 7
- ALG: 3 (+1 combinada ALG+LIT+ALG)
- 1 DERIVADO+FIX

## Los 3 hallazgos más graves

1. **FIX real (no sólo FIX-lite): el 0.6% de L469 no reproduce su propia
   cuenta.** `0.30729` (Ω_m sin el término de neutrinos) sí reproduce exacto,
   pero el desvío relativo asociado da **0.5%**, no 0.6%, verificado con
   `ssee_core.py` (OMEGA_B_H2+OMEGA_C_H2 vs OMEGA_M_TOTAL, H0_GLOBAL_d5). Error
   pequeño pero es el único número de esta lectura que falla una verificación
   aritmética directa, no sólo una falta de macro.

2. **Patrón sistemático de FIX-lite en el par `(w_0,w_a)=(-0.840,-0.670)` y en
   `|w_a|=0.669975`**: las macros `W0_d6`/`WA_d6` existen y se usan bien en el
   abstract, pero se repiten tecleadas a mano en 9 lugares (pies de figura,
   tablas de predicción, criterio de pre-registro DR3, apéndice). Mismo patrón
   en las correlaciones ρ de la Tabla DESI DR2 (`p2_w0wa_rho_ec25..28`, 4
   macros ya existentes, tecleadas a mano 2 veces cada una) y en `p2_obh2`/
   `p2_obh2_s` y `p3_gamma_IS` (éste último con riesgo real de confundirse con
   el 0.657/0.658 retirado si no se usa `\val`).

3. **Trazabilidad floja en dos números del cascade H₀**: `χ²_BAO=10.43` (al
   posterior MCMC, L584) y `2.9σ` (la "BAO-CMB split" histórica, L605) coinciden
   con la tabla canónica de CLAUDE.md/VERIFICATION_LEDGER pero no les encontré
   la clave JSON exacta con una búsqueda ligera — su compañero `13.9σ` SÍ está
   confirmado en VERIFICATION_LEDGER L142. Reportados en `afirmaciones`, no
   bloqueantes (son correctos por coincidencia documental), pero sin macro
   `\val` ni procedencia JSON directa verificada por este lector.

## Nota positiva
La sección de look-elsewhere completa (Tabla de tolerancias, 490 razones,
dictionary Génesis de 55 constantes) reproduce dígito a dígito contra
`results/logs/look_elsewhere_full.log` — es la pieza mejor instrumentada de
todo el documento, a pesar de no usar ninguna macro `\val` (son conteos
enteros). Ningún caso de retiro vigente (φ-DM, β_c=-AURA, s_m como densidad,
c_s²=1, 72.86/73.040) sobrevive sin marcar como historia en este documento.

Ruta: `notes/lectura_cuarta/SEALED.yaml`, `notes/lectura_cuarta/SEALED.md`.
