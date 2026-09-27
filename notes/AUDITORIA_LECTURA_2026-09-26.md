# Auditoría completa previa a la tercera lectura — 2026-09-26 (noche)

Rama `lectura-publico-2026-09-26`. Cuaderno de trabajo: cada línea es un hallazgo con su
archivo:línea. ★ = importante · ★★ = contradice el modelo vigente o a otro paper.

## Qué YA se corrigió (commit ec4f2da)
P2a, P2d (−24.0), P2g (0.39σ), P2h (anchos 0.839950), P2m (BAO sin prior), P2x (φ-DM en
conclusiones), P2y (Ly-α 8.1σ/1.1σ), P2j/P3u/U7 (URL del repo), P3a, P3b, P3c, P3j, P3l
(el σ, NO el orden), P3o, P3s, P3u (ruta), y las citas: Bellini & Sawicki (todas las
copias), Weinberg arXiv, Angus 2007, Brevik, Kroupa & Weidner, Deffayet, Freedman 2024.
Guardián: R37 ya no confunde `\textwidth` con w₀.

## Qué NO se tocó y por qué
Todo lo demás. Son de dos clases:
1. **Decisiones de física de Mike** (no se corrigen a solas): E1 (Ω_DE 0.84 vs 0.691),
   X1 (cruce fantasma), X2 (origen de w_a), P8/P9 (pata física de MIRA, acoplamiento
   disforme), P1h (CDM vs «sin CDM»), el «7» de P4, el teorema circular de P10, k=1 vs k=2
   (P6j), qué γ se predice (P3q), qué se hace con BOSS/A_s (P6c).
2. **Correcciones claras pero que cambian el sentido de una frase** — se hacen EN la lectura,
   página a página: los ~20 α_K→s_K (T6, lista por R54), α_K^field=0.072567 (T7), β_c=−AURA
   en Sealed/PRD (T3), titulares S₈ KiDS-1000→KiDS-Legacy (P3p, P6b, U3), conclusiones
   rancias de P2 (P2w: «el fondo FALLA») y de P6 (P6b), la tabla \TODO de P6 (P6a, se llena
   con la conjunta), la carta de presentación (U6).

## Guardián al cerrar
ROJO por R54 (48/47), R65 (24 números sin origen en p06/p11) y R66 (3 constantes
re-tecleadas en p11_sondas) — todos previos a esta noche. R68 se limpia con el commit.

---
# Auditoría 2026-09-26 noche
## Transversales
- T1 guardián ROJO R54 (48>47: RETRACTIONS.md:117 y LECTURA nuevos), R65/R66 (p11_sondas sin commitear + cobaya_conjunta.py 10 números sin origen)
- T2 CANONICAL_VALUES.yaml chi2_CMB_SSEE 1005.41 rancio (canónico 1003.586, ΔBIC -26.21)
- T3 Sealed+PRD: β_c=−AURA vivo (fila tabla "Retrodiction" L1030/1003; OP-7 item "agrees 0.2%" L1199/1177; párrafo símbolos L142/136; eq betac L722/695)
- T4 Sealed+PRD tabla predicciones "Extension tier — depends on φ-DM sector"
- T5 PRD fig s8 caption: "carries the 3.5σ tension ... reported" + figura centrada en KiDS-1000
- T6 α_K: Sealed 65/1077/1227 α_K(0)=0.403302 como predicción DESI/Euclid; Unified 143,757,778,784,799,811,1140; PRD 53,1028,1050,1206; P8 657; P3 951 (α_K^CLASS=0.403302)
- T7 α_K^field=0.072567 (w_φ≈−0.971, potencial RETIRADO) como predicción Euclid: P1 L208, L229-235; Endorser; Sealed tabla; Unified 757. P7 NO lo contiene; P7: w_φ=w0, α_K=15.591335 no observable, falsable = c_s², w0
- T8 P3 γ_IS=0.554 (L871, L905) vs 0.5504 canónico P5; P3 caja "Two-Ω_m criterion (Paper 1 Sec 1.4)" disuelto
- T9 manuscript/SSEE_Paper6_phiDM.pdf residuo
## Paper 1
- P1a L157 "k_fs ... genuine predictions" — k_fs RETIRADO
- P1b L202 S8 KiDS-Legacy rotulado "Prediction" contra la definición de la propia tabla (dato no publicado) y contra no-prioridad (KiDS-Legacy 2025-03)
- P1c L64 "two axioms" vs "three postulates" (terminología)
- P1d L324 α_K listado entre funciones "directly falsifiable"
- P1e L408 f_screen=α_K^eff/(3MIRA) — etiqueta vieja, debe ser s_K
- P1f L557 \paragraph{The CMB-sector matter density under the single global anchor.} huérfano (cabecera sin texto, sigue \subsection)
- P1g L577-580 "K(X)=X/KAL0 reproduces w0 ... c_s²=1 IR, 0.60–0.95 UV" — contradice P7 (K=c1X+c2X², ghost condensate, c_s²=0.021284)
- P1h L583-587/683 "sin CDM" + falsador "detección de partícula DM" vs ω_c=KAL0ωb n_s en Ω_m (P8: "materia oscura fría real") — PREGUNTA A MIKE (OP-19)
- P1i L655 NEC "deferred to Paper 4" — verificar
- P1j L639 "w0,wa derived as Taylor coefficients of the full effective EoS" — P7 da w=w0 constante; origen de wa abierto (sobreafirma)
- P1k tabla cúmulos Bullet: 1.2×5.5214×1.02=6.758 → 6.8, no 6.7
- P1i CONFIRMADO: NEC está en P7 (L377,772), no en P4
- P1l L835/L1012 χ²_r TT=1.044 vs P3 1.042 (P3 L540,561,1030)
- P1m L1048 URL repo github.com/mikealmeida1721/SSEE → SSEE-Cosmologia (también P2 1277, P3 1058, P5 1693, Endorser 23/152, Sealed/PRD/Unified)
- P1n L1119 f_screen=α_K^eff otra vez (→ s_K)
- P1o L1092/L1127 KAL0 "Viscosity"/"viscosity operator" — rótulo renombrado a Retention 09-07
- P1p L870-874 tabla BIC "every BIC ... four manuscripts ... No BIC outside this table" — P6 tiene ΔBIC KiDS −19.01 y +6.24; "four papers" en L811,878,943,992,1061 (son 10)
- P1q L1009-1012 tabla falsación "binding": sector observacional sin criterio S8 3σ de 0.8273 ni Ω_m>0.36 (sí están en la caja)
- P1r L1103 H0^MCMC "67.962 (anchor, fixed)" tipo M — un ancla fija no es MCMC
- P1s L1243 tabla linaje: AURA model role "|β_c|; cancels in H0 cascade" — β_c RETIRADO
- P1t L1289 MIRA = "Mapped Inference Resonance Amplitude" vs texto "Mirror Ratio" (dos expansiones)
- P1u L414-434 (Post. I: n_s SALE del α-attractor) vs L1449-1458 ("n_s NO derivado del α-attractor; n_s y r son dos axiomas") — CONTRADICCIÓN
- P1v L430 "Planck PR4 0.16σ" vs L1459 "Planck 2018 0.9649±0.0042 0.16σ" — etiqueta de dato
- P1w L1297 γ_IS ±0.001 vs P5 ±0.0003
- P1x CITA Angus2007: es ApJ 654 L13 (no MNRAS 374 1248) Y dice lo CONTRARIO (Bullet dominado por componente sin colisiones incluso en MOND) — P1 L784 lo usa como apoyo
- P1y CITA Bellini2015 → JCAP 07(2014)050; Brevik2005 → PRD 70 (2004); Kroupa2003 título real "Galactic-Field IMFs of Massive Stars"
- P2 4 bibitems no citados (Amendola2000, Deffayet2010, Gubitosi2013, HuSugiyama1996); P7 10 no citados
## Paper 1 — apéndice EFT (SSEE_EFT_section.tex, entra en P1)
- ★E1 DECISIÓN MIKE: Postulado S "Ω_DE = s = T_r/M_v = 0.84" (P1 L357) + Principio 1 L266 + acción L567 + L602 ρ_DE=ρ_crit(T_r/M_v) — saturación en ranura de densidad; el MISMO P1 (EFT L108-111) lo llama error 21.5% y usa 1−Ω_m=0.691119; Ω_m+Ω_DE=1.149. P7: α_K=3Ωde(5−3w0)=15.59 ⟹ Ωde=0.691 en P7. τ_ΠH0=KAL0/(3Ω_DE)=2.191 usa 0.84 (=s).
- E2 L31-36, L675-676, L728: "resuelto en P7 y P10 con K=X/KAL0 (c_s²=1) y X/KAL+X²/M⁴ (c_s²∈(1/3,1)); ambas reproducen w0" — P7 canónico es c1X+c2X² ghost condensate c_s²=0.021284; X/KAL puro da w=+1; X/KAL es el funcional de apantallamiento de P10 (memoria two_kx)
- E3 L18,46-50,144-157: viscosidad Eckart dentro de la ACCIÓN — memoria 09-07: la acción de P7 es exactamente adiabática, ζ=0 desde la acción; la capa IS es parametrización de Boltzmann
- E4 L510 "S8 ceiling 0.827, 1.1σ ABOVE Planck 0.832±0.013" — está DEBAJO y a 0.38σ; el 1.1σ era del viejo 0.846
- E5 L557 "with φ-DM already non-relativistic and contributing to the matter budget at recombination" — φ-DM VIVO
- E6 L587-592 "Axiom 1 n_s, Axiom 2 r, neither derived from α-attractor" vs Post. I (P1 L414-434) — misma contradicción P1u
- E7 L656-659 "reduces to Starobinsky in limit φ→1 (α→1, fixed point of x=1+1/x)": φ→1 da α=1/3, y el punto fijo de x=1+1/x es φ, no 1
- E8 L726 τ_ΠH0=KAL0/(3|w0|) vs L406 KAL0/(3Ω_DE) (mismo número, símbolos distintos)
- E9 L464 "Paper 3 §5.4 reports γ_alg=0.618 and γ_bg=0.657" — verificar P3
- E10 L483-495 párrafo S8 abre con KiDS-1000/0.8256 "2.7σ KiDS", Legacy en nota al pie (P5/Unified ya reescritos para abrir con Legacy)
## Paper 4
- ★P4a L250, L316-318, L356: Ω_b = 100(π−φ)/(6(φ+π)⁴) = 0.04948 (+0.53σ) — FÓRMULA MAL. Ω_b = ω_b/h² = 10⁴(π−φ)/(27Ω⁶) = 0.048535 → −1.91σ vs 0.0493±0.0004 (calculado)
- ★P4b "7" con TRES justificaciones: P4 L62/L412-444 = nº de registros primarios (lista φ,π,β,Ω,AURA,KAL,MIRA); P1 App prior_space lista OTROS siete (Ω,β,Kv,Mv,KAL,Psc,Tr); P1 Post. I = corolario de ventana [50,60]; P4 L446 "follows from α-attractor α=φ⁴/3 derived in P1 App A.5" pero P1 App A.5 deriva α DE n_s y r (circular); ventana [50,65] (P4 L450) vs [50,60] (P1)
- P4c abstract L74-77 ω_c=0.1193 (−0.6σ) con ω_b de Planck; L388 ecuación usa 0.02242 → 0.119514; L392 dice "ambas usan Planck 0.02237" — contradicción; canónico 0.119514 (−0.4σ) con ω_b algebraico. "IS inflationary factor n_s" mezcla viscosidad IS con inflación
- P4d L253 "Hubble tension fractional correction KAL/H0 = 8.12% ≈ 8%" — fórmula vieja, canónico f_screen 0.06725 (IR)/0.06952
- P4e L52 "Ω=φ+π follows as a theorem" — es una definición
- P4f L328-333 "sphaleron at T_EW ∼ Ω (SSEE units)", δ_CP "π gauge loops / φ scalar" — especulativo sin soporte
- P4g L297 r_d 148.2 (EH) vs P1 canónico CAMB 147.17
- P4h L255 marca ^P de nota al pie sin uso en la tabla
- ★P4i T_rh: L334 "gravitational reheating T_rh∼10⁻⁴ GeV" vs L461 Conjetura B.1 "T_rh≈9.4×10¹⁵ GeV" — 20 órdenes, mismo paper
- P4j L469 "N*=58.25 − ln3/6" — 58.25 sin fuente
- P4k CITA Pisanti2008 bib: autores de PArthENoPE con título "AlterBBN" (AlterBBN es Arbey 2012 CPC 183,1822; PArthENoPE es Pisanti+ 2008 CPC 178,956); texto L533 dice AlterBBN
- P4l L541 "Aver et al. 2015" sin \cite; L540 Y_p Planck 0.2471±0.0003 — verificar fuente
- P4m L575-577 + tabla L604-605: A_s, τ "retained at standard values ... deferred to Paper 5" — A_s ahora se clava al CMB del modelo (k=1 {τ}, 09-19); P5 no los deriva
- P4n L646-653 sección Hubble abre con H0+K=73.48 (0.5σ Riess) antes de decir "superseded"
- P4o L659 f_scr=α_K^eff/(3MIRA) (→ s_K)
- P4p L786 "δc prediction reserved for Paper 5" — δc ya está en este paper (§deltac)
- P4q L820 script "src/ssee_paper4_toe.py (repository root)" — está en src/p04_toe/
- P4r L884 "disformal coupling β_c=−AURA" — era CONFORMAL (P1 L1435-1443, P7); el disformal de P8-9 es otro objeto
- P4s L795 "Ω_b = 0.0495 (<0.4% from Planck)" — ver P4a (es −1.5%)
## Paper 5
- ★P5a Ω_DE con DOS valores DENTRO de P5: 0.84 (L94-95 "Ω_DE=|w0| Postulado S", L424 tabla ρ_crit→0.839950, L528, L720) y 0.691119 (L862). = E1
- ★P5b abstract L165-167 "ghost condensate [Arkani-Hamed] ≠ SSEE: ghost condensation gives c_s²=1" vs L242 "la acción ES el ghost condensate de P7, c_s²=0.021284"; además el ghost condensate de Arkani-Hamed tiene c_s²→0 (ω²∝k⁴), no 1
- ★P5c §2.3 L541-548 v_sig=√(ζ/(τρ_DE)) = c exacto — usa ρ, pero L382 y la caja OP-22 dicen que la inercia es la entalpía ρ+p; con entalpía v_sig≠c
- P5d L102-106 "k_crit=0.456 H0/c ... outside sub-horizon ... factor ∼2.2 inside the horizon" — contradictorio (está fuera)
- P5e L198 "Planck PR4 χ²_r ≤ 1.062" — P3 da 1.042/1.040/1.040
- P5f L204-205 MIRA rotulado "(MIRA factor)" — retirado como factor, ahora amplitud de apantallamiento
- P5g L869-872 frase rota ". and we write R ≡ Ω_m,eff/Ω_m,dyn" — minúscula tras punto Y R normalizado a Ω_m,dyn (=s_m, saturación) justo tras decir que no es densidad
- P5h L832 título §Q2 "Do IS perturbations link the two matter sectors?" — concepto retirado en el título
- P5i L576 Π̃ "normalised to ρ_DE" vs caja: normalización a entalpía
- ★P5j L983 pie fig MIRA: "r* = 0.190 ... 19% level" — la ecuación da r*=0.4464; L981 "1/Ω_m,dyn ≃ 6.25" normalizado a saturación
- ★P5k L1195-1199 "S8 > 0.86 would be favoured by SSEE over ΛCDM ... primary falsifiability criterion" SIGUE VIVA en §S8 (se quitó sólo de conclusiones); contradice la predicción 0.8273
- ★P5l L1217-1219 "the nominal SSEE prediction is ... A_s free, S8=0.7555" — contradice abstract/conclusiones (0.8273, A_s clavado, KiDS-Legacy). §S8, tabla S8 y fig s8_resolution centrados en KiDS-1000, sin Legacy
- P5m L1028 "integrate from a=0.008131" — 0.008131 es r=φ⁻¹⁰; sospechoso (¿a_ini?) — verificar en script
- P5n L1128 "Planck–lensing tension 2.4σ KiDS, 2.7σ DES": con los valores citados sale 2.67σ y 2.62σ; cita Weinberg2013 anterior a KiDS-1000
- P5o L1297 "tiny ∼1% difference in G" — G=1.0032 (0.3%); el 1% es del viejo 1.011
- ★P5p §6.2 L1370-1407 + tabla L1387-1396: "ghost condensate c_s²=1, δ_DE∼δ_m, S8 grande" — P7 dice que la acción de SSEE ES un ghost condensate (c_s²=0.021284); comparación entera contradice P7. Fila "DESI DR2 >3σ" para ghost/k-essence sin fuente
- ★P5q L1421-1425 Friedmann IS "3H²M²=ρm+ρDE+Π_bulk" — la presión viscosa NO entra en la ligadura de Friedmann (entra en la aceleración); y usa Π=−KAL0 ρ_DE H (forma ρ, retirada por la caja en favor de la entalpía)
- ★P5r L1573-1576 "introduces a new prediction for σ8 and S8 that partially resolves the lensing tension" — rancio, contradice todo el paper
- ★P5s tabla falsables L1605-1611: fila S8 "S8>0.86 favours SSEE" (sin fila 0.8273); fila c²_s,eff=0 test |c_s²|<0.05 (la predicción del campo es 0.021284); fila MIRA "Ω_m direct measurement" (MIRA ya no toca Ω_m)
- ★P5t conclusiones L1641-1646 "Q2 — MIRA factor ... discrepancy is 50%" — L882 del mismo paper dice que ese 50% "no es un resultado" (reencuadre 09-26 como cota |r|≤0.0175)
- P5u L1545 fσ8(z=0.5)=0.4714 vs tabla z=0.51 → 0.478 (1.4% distinto)
- P5v L1690 script "src/ssee_paper5_IS_perturbations.py" → src/p05_IS/; DOI 20093447 viejo; existen src/p05_is Y src/p05_IS (duplicado)
- P5w L1517 "inverts the result to a deficit" — ya era déficit; lo profundiza
- P5x L1362 M̄2²/M_Pl² = Ω_DE (0.84 = s) — E1
## Paper 7
- ★★X1 (cruce P1↔P7) P1 L647-655: el cruce fantasma z*=0.31 "does not signal a ghost or gradient instability in the SSEE action"; P7 L713-717: c_s²=(1+w)/(5−3w) CAMBIA DE SIGNO en el cruce (z=0.31) "beyond that point the field is no longer what carries the EoS"; P7 L378: w_eff=w0 siempre, "no phantom crossing is claimed"
- ★★X2 (cruce P1↔P5↔P7) origen de w_a: P7 L797-805/L877-881 "w_a=0 desde la acción; debe venir de la viscosidad IS de P5"; P5 L285-298: la viscosidad NO sale de la acción (ζ=0), la capa IS es reparación de parametrización; P1 EFT §wa_derivation: w_a "emerges algebraically" de ζ(a) con Eckart DENTRO de la acción. Lazo sin fuente física; P1 lo presenta como derivado
- ★P7a L144 signatura (+,−,−,−) con X ≡ −½g^{μν}∂φ∂φ = φ̇²/2 — con esa signatura sale −φ̇²/2 (signo); P1 EFT usa (−,+,+,+)
- P7b L112 "interacting-sector perturbation theory" (P5 es Israel–Stewart, no "interacting"); L513 "α_B=0 in the interacting sector as well" — ya no hay sector interactuante
- P7c L470-474 "G_2s=1.003 derived in Paper 6" — es de P5 (1.0032)
- P7d L476-481 "canonical amplitude ... KiDS-1000 0.7555" en cuerpo; Legacy sólo en nota
- P7e L373/L485/L833 "sound horizon c_s/H0 ≈ 600 Mpc": √0.021284 × c/H0(67.962) = 643 Mpc
- P7f bib: Weinberg2013review arXiv 1201.2434 (P1 dice 1201.1084 — P1 MAL); euclid2024 arXiv:2405.13491 es "Euclid I. Overview" (Mellier+), no "Cosmological forecasts"; self-cites Paper1/2 año 2025; 10 bibitems sin citar se imprimen
- P7g L99 "DESI DR2 3.1σ from ΛCDM" — especificar combinación (DESI+CMB); rango 2.8–4.2σ
## Paper 8
- ★★P8a L192-207 "adoptamos la acción canónica de P7": P = X/KAL + X²/M⁴ − V0 e^{−λφ/M_Pl} + DM acoplada a métrica disforme. P7 canónico: K=c1X+c2X², SIN potencial (retirado), SIN acoplamiento a materia ("matter follows its own geodesics"). La acción de P8 es la retirada
- ★★P8b L153-154, L228-239 "β_c ≡ AURA, disformal coupling constant FIXED IN PAPER 7" — P7 L349 dice que el disforme de P8-9 "es otro objeto" y no lo fija; β_c=+AURA queda sin derivación en ninguna parte
- ★P8c L225 "M ≈ M_Pl (free EFT parameter)" vs L567/P10 M=9.68 meV fijo; L1091 "zero-free-parameter"
- ★P8d L563 r_km³ = M_obj/(4π M_Pl M²): dimensionalmente inconsistente (derecha GeV⁻², izquierda GeV⁻³). Brax & Valageas: R_K = (β M/(4π M_Pl Λ²))^{1/2}. Con raíz cuadrada: Sol ~10¹⁴ m (~800 AU), 10¹² M☉ ~kpc — cambia "r_km ≪ 1 kpc" (VERIFICAR contra brax2014)
- ★P8e L389-393 "Einstein radius matches GR-with-DM on all scales. The effective source ... suppressed by ≈1.93 ... Einstein radius reduced" — dos frases contiguas contradictorias; 1.93 = Ω_m/(1+w0) retirado
- ★P8f conclusiones L1062-1072 encabezan con "lensing amplification √β_c ≈ MIRA" y "MIRA emergence" (límite pedagógico) — el abstract dice canónico = GR sin amplificación
- P8g tabla L759-762 canónica "M_dyn/M_lens > 1 (fifth force on DM)" vs §falsables item 3 "canonical predicts ≈1"
- P8h L657 α_K=0.403302 "sole non-vanishing EFT parameter" → α_K=15.591335 (P7)
- P8i A1689 L784-805: compara ángulo de deflexión α̂=42.6" con θ_E=45" (θ_E = α̂·D_LS/D_S); b=250 kpc a z=0.183 ↔ ~80", no 45" (45" ↔ ~140 kpc); "factor ≈1.9" es 1.78
- P8j L978 palabra en español "the cantidad that emerges"
- P8k L892-893 Auger 2010 y Cao 2018 sin \cite; L697/L1081 0.022 R☉ vs L575 0.021 R☉
- P8l L156, L519 f_screen=α_K^eff (→ s_K)
## Paper 9
- ★★P9a L184-205 "The SSEE action (Paper 7)": K = X/KAL + X²/M⁴ − V0e^{−λφ}, "conformally coupled to dark matter" — P7: c1X+c2X², sin potencial, sin acoplamiento. L155-157 "s_K follows from ... k-essence action K(X)=X/KAL" (esa es la función de apantallamiento de P10)
- ★★P9b MIRA "emerges from the disformal null geodesic of Paper 8" (L64-65, L158-160, L255 "θ_E ratio ≈ √β_c ≈ MIRA", L324, L601, L608-613, L674, L919) — P8 dice: la geodésica da √AURA, NO MIRA; en el límite canónico no hay amplificación; MIRA "aparece sólo en f_screen de P9". Circular: P9 toma MIRA de P8 y P8 dice que MIRA sólo vive en P9 → f_screen sin pata física (el VALOR algebraico no cambia)
- ★★P9c §sep_universe L369-402 + L885-887: usa "c_s²=1 (Paper 5, Q1)" (P5: 0; P7: 0.021284), "M accounts for total-versus-dynamical coupling (Paper 6)" (retirado) y la IDENTIDAD "1+w0 = Ω_m (exact)" — RETIRADA (1+w0=0.160 ≠ Ω_m=0.308881; el cociente es 1.93, no 1). El argumento "multiplicativo" (ii) se cae
- ★P9d L631-633 "φ-DM free-streaming (Paper 6) ... σ8^eff = 0.747 result of Paper 6 is unaffected" — VALORES RETIRADOS VIVOS
- ★P9e L501-506 ρ_kin = 3M²H² s_DE(1+w0)/2: usa ρ_φ = s_DE·ρ_crit = 0.84 (E1); P7 ρ_DE,0 = 0.691 ρ_crit
- ★P9f L707 y L440 "0.17σ from SH0ES" — el 0.17σ es contra el número puro (SH0ES es la ENTRADA)
- P9g L712-714 falsación "SH0ES fuera de 71.5–74.2 → excluido ≥1σ": centro 72.86 = el 72.86 retirado (lectura inversa); y "≥1σ" no es criterio de falsación (P1 usa 3σ)
- ★P9h L839-844 "0.17σ — better than every finalist of the H0 Olympics": métrica distinta (residuo contra su propio número con SH0ES de entrada vs residuo de los otros contra SH0ES); sobreafirma
- P9i L437/L541-545 "additive" = H/(1+f) (no es aditivo); L547 "f² ≈ 0.31 km/s/Mpc" (f²H0)
- P9j L126-129 "Planck PR4" con 67.4±0.5 (es Planck 2018/PR3)
- ★★P9k App B Step 2 L1083-1110: "photons propagate on disformal null geodesics" — P8 L349-351: "Baryons AND PHOTONS couple to the physical metric g, NOT the disformal metric". Además: fotones más rápidos (c/(1−f)) recorren MÁS distancia comóvil, pero el texto concluye χ "comprimida" (1−f); "Paper 8 eq.(17)-(18)" citada para β_c φ̇²/(M⁴a²) ≈ −f no existe en P8
- ★P9l métrica disforme con dos normalizaciones: L243 g + (2/M⁴)∂φ∂φ vs L1087 g + (β_c/M⁴)∂φ∂φ
- ★P9m Step 4 L1140-1153 "f_screen exactamente constante a todo z" y a continuación L1163-1172 "f(z) medio ≈ f(0)[1+3w_a z/4] ... corrección 2.5%" — contradicción interna (párrafo sobrante)
- ★P9n App A L1001-1023 "assuming no algebraic value in advance ... φ and π have not yet been invoked" — f^UV=0.069522 SÍ se construye con φ,π (y M⁴=5φ⁸ρ_crit): el paso "hacia atrás" no es independiente
- P9o App A L1031-1038 nombres mitológicos MIKAEL, MIKA, Ω_DNAV (política 2026-05-15 los eliminó de P4) y "25 Sovereign paths" (P4: VEINTE rutas); "−0.0001%" vs residuo 4.2e-6 (=6e-6 %)
- P9p L998-999 "reduces the ∼5σ Planck–SH0ES discrepancy to below the percent level" — sobreafirma (mapea SH0ES a un número; no reconcilia Planck)
- nota: edad t0 verificada 13.7325 Gyr (texto 13.733; frontera de redondeo)
## Paper 10
- ★P10a abstract L51-53 "the IR kinetic Lagrangian K=X/KAL produces the local Hubble correction"; L262 "K=X/KAL ... is the description used in Papers 1–9"; L950 conclusiones "the SSEE dark-energy Lagrangian K = X/KAL + X²/M⁴" — contradice su propio L275 ("This is NOT the dark-energy action of Paper 7") y L248 (s_K independiente de cualquier Lagrangiano)
- ★P10b "Teorema Condicional C.1" circular: L573-576 "M⁴ ... has been FOUND numerically"; L780 "the unique monomial satisfying ... and the EMPIRICALLY ESTABLISHED M⁴=5φ⁸ρc" — usa el blanco como entrada; "único" no se sigue (infinitos polinomios en φ)
- ★P10c L851-856 "s_K^full medible vía la EoS; Euclid/DESI Y5 distinguen UV de IR a 3.4σ_syst" — pero L866-867: w0 NO cambia por construcción ⇒ s_K desde w0 no distingue; "3.4σ_syst" sin fuente
- ★P10d L882-898 c_s,ad²≈0.967 "of scalar-field excitations ... on top of the dark-energy background" — omite P7 (0.021284); la suite tiene 3 c_s² para "el campo": 0.967 (P10), 0.021284 (P7), 0 (P5 fluido)
- ★P10e tabla L924 "Paper 8 Vainshtein r_V ∝ 1/M²; r_V enlarged to ∼10⁴⁴ m at UV" — P8 tabla: r_km(Sol)=1.45×10⁷ m con M=9.68 meV, y es k-mouflage, no Vainshtein
- P10f L311 ρ_φ(1+w0) = s_K/3 ⇒ ρ_φ = s_DE = 0.84 ρ_crit (E1)
- P10g CITA Freedman2024 → arXiv:2308.02474 "CCHP IX" ApJ 963,84; el valor 69.96±1.05±1.12 es de arXiv:2408.06153 (ApJ 985, 203, 2025) [verificado]; BelliniSawicki2014 título "Maximal freedom at the cost of fine tuning" — real "at minimum cost"
- P10h L398 "Vainshtein suppression activates (see Paper 8)" — P8 es k-mouflage; L208 "Paper III" (romano)
- P10i falsación L542-544 a 1σ
- P9q CITA Freedman2024 igual que P10 (ApJ 963,84 con valor de 2408.06153)

## Paper 2 (P2a–P2z)
- P2a Resumen: "H0 único libre" vs k=2 {H0, Ω_bh²} (L992).
- P2b Rango "1.2–1.5σ" (resumen, L1225) vs tabla 1.46/1.76/1.68.
- P2c ★ "sector frío 0.160 agrupa (Paper 6) / fija α_K=3|w0|·0.160 (Paper 7)" L93, L110, L373, L722-725 — partícula/sector retirado y α_K mal nombrado.
- P2d ★ ΔBIC CMB −24.0 rancio (→ −26.21): L274, L1008.
- P2e ★ ΔBIC "−32.9 full plik MCMC" L1140, L1242, L1345 — sin fuente; CLAUDE.md sólo tiene −32.2 legacy PENDIENTE y −26.21 canónico.
- P2f Leyendas rancias KAL/r_d mapping L283, L503.
- P2g H0 "0.39σ de Planck" L1005 (67.53 es 0.26σ; canónico 67.79 es 0.66σ). Cifra no cuadra con ninguna corrida.
- P2h `width=0.839950\textwidth` L880 y L952 (sustitución masiva de 0.84 que entró en un ancho de figura).
- P2i CPL w_a −0.557 (L1380) vs −0.558 (L1108).
- P2j URL repo L1277 → SSEE-Cosmologia.
- P2k Bib sin citar: Amendola2000, Deffayet2010, Gubitosi2013, HuSugiyama1996 (+ revisar Cooke2018, DESY52024, Eisenstein2005, JimenezLoeb2002, Clifton2012). Deffayet2010 = PRD 79 084003 es de 2009. Weinberg2013 arXiv 1201.2434 (no 1201.1084).
- P2l L1043 "all four clusters" — la tabla tiene siete.
- P2m ★ L1050 BAO-only H0=65.8(+1.2/−1.1) "0.6σ del completo" — rancio: canónico DESI solo prior plano 67.66±0.46; y 65.8 vs 67.79 no es 0.6σ.
- P2n ★ L1094-1096 "resolver 5σ requiere cambiar r_s o Cefeidas" contradice P9 (SH0ES entra, H_global sale vía f_screen).
- P2o ★ L1113 "Ω_m (0.34σ)" vs 0.88σ en L1139/L1245 — misma cantidad, dos σ.
- P2p ★ §Structural reinterpretation L1119-1130: discute una "penalidad ΔBIC" que ya no existe (ΔBIC −6.43 favorece). Subsección entera rancia.
- P2q ★ L1154-1155 S8=0.827 "2.7σ con KiDS-1000 y DES Y3" y L1160 cuerpo encabeza con KiDS-1000 R3 0.7555; KiDS-Legacy (canónico 0.8273) en nota al pie. Orden invertido.
- P2r ★ L1172-1173 "brecha 3.4σ entre determinaciones, no resuelta" — con KiDS-Legacy es 0.49σ en A_s. Rancio.
- P2s L1164 τ_Π H0≈2.191 "Paper 3 §5.4" — verificar (E9). "redistribución matter↔radiation" dudoso.
- P2t §Roadmap for Paper 3 (L1175-1194) y conclusión 6 (L1257) en futuro: Paper 3 existe. Rancio.
- P2u ★ L1205-1208 "neutrino bridge = único mecanismo de cúmulos" vs L927 "los cúmulos no requieren el puente" (f_ν=0 da χ²_r 0.028). Contradicción interna.
- P2v r_d 148.2 (E(z) analítico) vs 147.17 (CAMB) coexisten sin explicar cuál es cuál; falsador 147±3.
- P2w ★★ L1220 "background sector FAILS under standard calibration" y L1262-1267 "Central finding: background geometry fails" — contradice todo el cuerpo (ΔBIC −6.43 a favor). Conclusión central rancia.
- P2x ★ L1251 "donde φ-DM es no relativista" — partícula retirada, viva en conclusiones.
- P2y ★ Ly-α: conclusiones L1249/1252 "8.1σ / 1.1σ" vs apéndice 12.5σ / 0.7σ; (8.71−8.632)/0.101=0.77σ, (9.89−8.632)/0.101=12.46σ ⟹ el apéndice es el correcto, las conclusiones son rancias.
- P2z L1436-1439 "11.8 (31σ)" sin fuente en log; L1428 "χ²=12.0 = ΛCDM 12.0" vs χ²_BAO~10.86 canónico — verificar.
- (corrección P2e) −32.9 SÍ tiene fuente: CANONICAL_VALUES.yaml L318 (full plik, χ² 2771.30 vs 2773.11). Lo rancio es sólo el −24.0 de plik_lite (→ −26.21).

## Paper 3 (P3a–P3z)
- P3a ★ Resumen L45 "H0 y Ω_bh² son k=2" vs L77 "k=2={A_s,τ}"; tabla BIC diagonal L606 "k=2 (H0 + Ω_bh² prior)". Dos definiciones de k en el mismo paper.
- P3b ★ Resumen L63 Ω_m "dentro de 0.6σ de Planck" vs L340/L1035 0.88σ (|0.3089−0.3153|/0.0073=0.88).
- P3c Resumen L84 plik_lite "−24.0" rancio → −26.21 (el cuerpo L653 ya dice −26.21).
- P3d ★ Caja "Two independent matter densities" L90-98 y L64-65/L240-242 "dos predicciones independientes... s_m (DESI)" tratan 0.160 como densidad validada en P2, contra L154 "s_m nunca es densidad". Contradicción interna; restos del reframe.
- P3e ★★ H0 "derivado de la inversión SH0ES–f_screen (Paper 9)" L167, L374, L631, L645, L665 — es la dirección RETIRADA (banner 09-06: el número puro es el BLANCO, no la semilla). Debe decir: anclaje de Postulado D (P1), y P9 compara la salida contra él.
- P3f ★ Ω_bh²: tabla CAMB L375 usa 0.02237 (prior Planck) vs L645/L665/L716 0.022418 algebraico fijo. ¿Cuál corrió en plik_lite 1003.586? Aclarar (y L400-404 dice "fixed to the Planck prior").
- P3g Picos ℓ3: 813 (L75, L1029) vs 812 (tabla L448, falsador L978).
- P3h L583 "exceso Δχ²_r≲0.02 en TT y TE" contradice la tabla (−0.001, 0.000). Rancio.
- P3i L631 "The MIRA factor is not a free parameter" — el factor MIRA está retirado; frase sobra.
- P3j L732/L749 leyendas "B1 full plik_lite MCMC" — la B1 es plik completo.
- P3k ★★ §hi_class L931-952: "escalar canónico conformemente acoplado (P7 §4.3)", w_φ=−0.971 "P7 Tabla 2", "corriente de acoplamiento Q^ν" y α_K^eff=0.403302 "valor citado en Papers 7–10" — P7 vigente es ghost condensate SIN potencial ni acoplamiento; su α_K=15.591335; 0.403302 es s_K. = T6+T7 en P3.
- P3l L786-826 γ_alg=φ⁻¹=0.618 "por análisis dimensional" sin fuente; y "tensión ~3–4σ con KiDS-1000 y DES Y3": 0.827 vs 0.759±0.024 = 2.8σ, vs DES 0.773±0.025 = 2.2σ. Cifra mal + encabeza con KiDS-1000.
- P3m L825 "Paper 6 resuelve con φ-DM (0.758), ahora retractado" — frase que narra lo retirado primero.
- P3n γ_IS=0.554 (L871, L905) vs 0.5504 (L793) — T8. Caja L903 cita "Two-Ω_m criterion (Paper 1 §1.4)" retirado — T8. L908-916 narra la partícula (0.747, k_1/2) en la caja vigente.
- P3o L964 "buen ajuste χ²_r≈1.06" vs 1.042 de la tabla.
- P3p ★ Falsador 4 L996-999: S8=0.7555 KiDS-1000 → canónico 0.8273 predicho (KiDS-Legacy).
- P3q Falsador 5 L1004: γ_alg=0.618 "predicción algebraica" y 0.657 conviven con 0.5504; la memoria dice γ lo fija w(a) (≈0.54). Decidir qué γ se predice.
- P3r Conclusión L1033-1034 titular −26.21 (plik_lite) vs tabla L770 "−32.9 canónico". Dos titulares.
- P3s L1036 "r_d 147.17 coincide con ΛCDM al 0.03%": vs 147.09 es 0.054%.
- P3t ★ L1044-1049 "68.13 aborda la tensión de Hubble al 0.17σ" — el 0.17σ es contra el número puro, no una resolución de la tensión; mismo mal rótulo que P9.
- P3u L1056 ruta `src/ssee_paper3_cmb.py` → `src/p03_cmb/ssee_paper3_cmb.py`; URL repo L1058.
- P3v L298-302 "el sector viscoso que sobrevive es ζ(a) de P1, que entrega w_a" — choca con X2 (w_a sin fuente física; la viscosidad IS no sale de la acción). Y "factor 9.5" sin fuente.
- P3w L410 "satura en T_r/M_v cuando a→∞ (P1 §3.4)" — verificar que P1 §3.4 exista y lo diga.

## Paper 6 (P6a–P6r)
- P6a ★★ Tabla R7 L290: celdas \TODO{joint fit} VIVAS en el PDF. Es exactamente lo que mide la conjunta en curso ⟹ se llenan con su resultado. Y la fila SSEE "0 (by construction)" (L275-277, L291) es la afirmación que la conjunta PONE A PRUEBA (los nuisance pueden migrar): no se puede dejar "por construcción", va el número medido.
- P6b ★★ Conclusiones L770-798 NO mencionan KiDS-Legacy: cierran con "3.4σ residual, no resuelto" y "desplazamiento en la época" — el §Legacy del mismo paper lo disuelve (0.49σ). Conclusión rancia respecto de su propio cuerpo.
- P6c ★★ §fσ8 L700-706 y conclusión L791-798: "clustering sitúa A_s por debajo del CMB, igual que la cizalla ⟹ la época". Con memoria [[project_As_kids_measures_boss_slides]]/[[feedback_check_repo_before_deriving]]: BOSS NO vota en A_s (el central se mueve 0.63 con el estimador). Y la cizalla Legacy ya no está por debajo. Afirmación retirable.
- P6d ★ Resumen L87-91: "0.8262, 3.4σ, sin resolver" antes que Legacy; el titular canónico (0.8273 predicho) aparece al final. Decisión de orden para Mike (cronológico vs canónico).
- P6e ★ log(10¹⁰A_s) del CMB con fondo algebraico: 3.042±0.013 (L421), 3.0438±0.0151 (L702), 3.04483 (L502, = clavo 3.0448340), y P3 3.043±0.014. Cuatro cifras para una cantidad. Unificar con fuente.
- P6f ★ Nuisance KiDS-1000: L310 "Nine nuisance" pero enumera 8; L311 "c-term ADITIVO" vs L345 "calibración MULTIPLICATIVA δ_c". Contradicción.
- P6g Controles KiDS-1000: 261.27 vs 260.32 (0.4%, L307) y 262.75 vs 260.32 (0.9%, L404) — los dos llamados "reproducción"; aclarar que uno es punto máx-posterior y otro mínimo de cadena.
- P6h ★ §Método BOSS L330-334: "Kaiser en esta etapa; TNS/EFT es el objetivo" — rancio: la tabla usa LPT (velocileptors). L760 "resultados con k>0.10 léanse con esta advertencia" contradice que la producción es LPT.
- P6i L254-256 "el único parámetro que varía entre sondas es A_s, libre en SSEE y ΛCDM" — superado por A_s clavado (k=1, §Legacy).
- P6j L645 "k=2 contra 6 en el CMB" — con A_s clavado, ¿k=1={τ}? Decisión de Mike ([[project_as_clavado_k1]]); si se adopta, propagar a P1/P2/P3/Unified.
- P6k L697 "ΛCDM con fondo libre en BOSS = pendiente" — sigue abierto; decidir si se corre.
- P6l L754 "(§boss-method)" no contiene los 0.92σ/1.048 que cita.
- P6m L209-210 "OP-8 retirado 2026-07-09" — el reframe ω_m-directo que cerró OP-8 es 2026-06-18 (07-09 fue el bug de geometría). Verificar fecha.
- P6n BOSS: 37 libres/19 muestreados/222 pts aquí vs conjunta con 18 muestreados de BOSS y ref 82.636 (escala marginal). Dos montajes de BOSS; el paper no dice cuál es la referencia de la conjunta.

## Consolidados (Unified / Sealed / Endorser / Carta)
- U1 Unified L330 "H0 es el único libre" (= P2a). L462 "−24.0 plik_lite" rancio → −26.21.
- U2 ★ Unified: α_K=0.072567 como predicción Euclid viva L144, L728, L737, L757, L777, L1040, L1142, L1166, L1201 (= T7). Tabla de predicciones y conclusiones.
- U3 ★ Unified/Sealed/Endorser: titular S8 en tablas = 0.7555 KiDS-1000 (Unified L1033, L1205; Sealed L1036; Endorser L85 ya como "earlier" ✓). Canónico: 0.8273 predicho (KiDS-Legacy).
- U4 Sealed L946 y Endorser L140 "3.5σ" (2.863 vs 3.04483 con σ=0.051) vs P6 "3.4σ" (vs 3.042 con σ combinada 0.053). Misma separación, dos cifras.
- U5 ★★ Endorser L108: "Paper 8 [draft; su predicción de lensing es CONDICIONAL al límite (b) porque se retractó el φ-DM]" — contradice CLAUDE.md/banner 2026-08-02: la predicción es INCONDICIONAL (ω_c + α_B=α_M=0).
- U6 ★ Carta de presentación L60-72: párrafos tipo bitácora "(Updated 2026-09-07: earlier versions of this letter said...)" dentro de una carta al editor, que nunca vio versiones previas; y encabeza con KiDS-1000 0.7555. Reescribir limpia con el titular canónico.
- U7 URL repo en Endorser L23/L152 (y Unified/Sealed/PRD, ya en P1 lista).
- U8 Sealed β_c=−AURA vivo (T3) — confirmado L142, L722-726, L1030, L1199.
- U9 PRD = submission_PRD/SSEE_PRD.tex (mismo contenido que Sealed; T3–T6 ya anotados).

## Cajones
- C1 CANONICAL_VALUES.yaml L304 `chi2_CMB_SSEE: 1005.41` (Δχ²=+1.65) vs Delta_BIC −26.21 que usa 1003.586 (Δχ²=−0.183). El YAML se contradice a sí mismo (= T2).
- C2 CANONICAL_VALUES.yaml L312 `Delta_BIC_cobaya: -32.2 PENDIENTE re-confirmar` — P3 L655 ya lo declara superado. Pasar a retirados.
- C3 CANONICAL_VALUES.yaml L407 comentario: "Σm_ν = 0.06849 (=40.70/594.28)" — describe el Σm_ν canónico como cociente de la PARTÍCULA retirada. La fuente vigente es L295 (R₂·ω_b·C_ν/(τ_Π·H₀)). Corregir el comentario.
- C4 ★ OPEN_PROBLEMS OP-26 "fσ8 contra BOSS crudo sin medirse" (09-19) vs P6 §fσ8 con números de results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json (09-20). O se cierra OP-26, o el paper publica algo no aceptado. El JSON NO registra R−1 ⟹ convergencia sin constancia (regla de lectura: reportar R−1 real).
- C5 CLAUDE.md (proyecto): P7 "αK=0.4033" en la lista de papers y tabla docs; Paper 6 "fσ8 pendiente (R1/R2)"; sección manuscripts lista `SSEE_Paper6_phiDM.tex`, "Paper 7 βc=-AURA al 0.2%", `SSEE_Paper10`... ; tabla P5 dice G, etc. Varias entradas rancias (el banner de arriba manda, pero el cuerpo confunde).
