# Quinta lectura — README (portada pública, lectura completa, 2026-10-12)

El README no puede usar \val: cada número se cotejó a mano contra su log.

## Errores de número (log manda)
1. «within 1.2–1.5σ of DESY5/Union3/no-SN» → 1.5–1.8σ (paper2_w0wa.json: 1.46/1.76/1.68).
2. ℓ₁ = 221, Δℓ = 1 → 220, Δℓ = 0 (class_picos.json; ΛCDM 220).
3. KiDS-1000 «3.5σ away» → 3.6σ (kids_publicados.json).
4. N_eff ≈ 637 500 → 79 203 (mcmc_paper2_reframe; el viejo era de la corrida MIRA).
5. 1.47σ/1.77σ → 1.46σ/1.76σ.
6. r_drag 0.14σ → 0.10σ; w₀ 1.73σ → 1.74σ (mcmc_full_posteriores.json).
7. Y_p «CAMB BBN PArthENoPE 0.2472, 0.58σ» → lineal de P4, 0.2471, 0.6σ.
8. «31 invariants» → 55 nombres, 25 valores (el diccionario y PRD/Sealed).
9. Techo S₈ ΛCDM 0.830 sin log → «—».

## Sin log → fuera
DR1 0.05σ y «errores −40 %»; fila «IS cs² effect 0.03 %» (CLASS de mayo); σ_M y la fila
3×10¹¹ de Press-Schechter (el log no los tiene).

## Contradicciones
- Títulos y páginas: P5 (título nuevo, 29 pp), P8 (título nuevo, 17 pp), P2 28, P3 24, P7 18,
  Unified 20, Sealed 23 y «~3 vs 6 parámetros» → k = 2 vs 6.
- τ_Π H₀ = KAL₀/(3Ω_DE) y «(Ω_DE, w₀) = (s, −s)»: es la saturación s_DE = |w₀|.
- Σm_ν en la tabla de P6: la cadena es de P4.
- MCMC multi-sonda «+ clusters»: no lleva cúmulos.

## Pendiente para el día de publicar
«Status (2026-10-10)… 288 checks… green» y la insignia «guardian green»: hoy son 349
comprobaciones y el guardián está en rojo con 4 fallas conocidas. Se actualiza cuando
quede en verde, junto con la fecha de portada.
