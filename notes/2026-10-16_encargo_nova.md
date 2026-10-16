# Encargo a Nova — lecturas frías, postulados y suites del guardián (0439a84..051f1c6)

Fecha: 2026-10-16. Rama: `lectura-publico-2026-09-26`. 19 commits desde el último push.
Protocolo de siempre: verificar en el remoto corriendo las cosas, no leyendo este
resumen. Nada va a `main` hasta que los dos coincidan.

## Lo que más importa verificar (cambia lo que el modelo dice)

1. **Postulados: cuatro, no tres** (`80c3318`). P1 §1.3 decía «three postulates in total»
   (D, S, I) mientras P9 §«The form of the correction» declara postulado la forma
   multiplicativa de la lente, H_local = H_glob/(1−f), que el enunciado de D ya usaba.
   Ahora: D, S fundacionales + I, F auxiliares (F = forma de la lente, OP-6b). La
   Conjecture C.1 de P10 (OP-3) queda FUERA del conteo, marcada condicional (sólo mueve
   68.13 → 67.962, dentro de ±0.968). Revisar: que ningún documento cuente distinto
   (guardián R78) y que los nombres corregidos no sumen supuestos: P4 «Conjecture B.1»
   = Postulado I con la ventana [50,60]; P9 apéndice sin «Postulate P»; P8 β_c ≡ AURA
   sólo del límite (a). Desde la literatura: ¿hay algún argumento publicado que fije la
   forma multiplicativa de una corrección de apantallamiento sobre H₀ local?
2. **Lecturas frías P1–P10, PRD, Sealed, Unified** (`cbf4000`, `d5c1a15`, `aa5912e`,
   `0439a84`): P2 ahora da todas las distancias marginales del MCMC (H₀ 1.79σ, Ω_m 1.69σ,
   w₀ 1.74σ, w_a 1.43σ), no sólo la conjunta favorable; tablas de comparación con
   encabezado ln L_max; fuera dos barras sin fuente del PRD. Unified: frente a la
   columna fσ₈ PUBLICADA de BOSS (que asume geometría ΛCDM) los dos pipelines quedan
   bajos en z = 0.38; decide el χ² sobre los multipolos crudos.
3. **Soberanas** (`2b11c0b`, `be97391`): P4 decía 20 = 6+11+3 sin script; ahora cuenta
   el código: 24 rutas aditivas a M_v = 8+13+3 (+ TRÏSTAL = 25 particiones). HERA =
   Ω+KAL+AURA (no HARMONIA+Ω, que es EUNOMIA).

## El guardián y sus suites (`2f32e50`, `30aefa4`, `80c3318`)

- Tres fallos reales corregidos: la carga del núcleo sin proteger (V-L2-06), R36
  atribuía la figura del CMB del PRD a `registro_reglas.py` en vez de su productor, y el
  piso de R46 estaba en 278 con 349 comprobaciones ejecutándose (ahora 345).
- R75 verifica carpetas de datos por su hash de árbol, como DVC (con control R53).
- `mutacion_guardian.py`: 61/61 detectados, cada uno por su regla; restaura los efectos
  colaterales. `test_guardian.py`: 30/30; R29/R30 inyectaban sobre literales que el PRD
  ya pasó a `\val` (no cambiaban nada); ahora la suite marca «ancla perdida».
- Para correr: `python src/verificacion/ssee_verify.py` (AMARILLO esperado: deuda
  declarada R75 = 25), y las dos suites EN SERIE, nunca a la vez (cerrojo
  `.mutacion.lock`).

## Para el expediente de firmas

La lente aplicada a las 10 mediciones locales de H₀ de `results/logs/h0_por_metodos.json`
las deja todas a menos de 2σ de 67.962 (la peor, JAGB del equipo CCHP, −1.93σ). Con las
tres que no usan la escalera (máseres, lentes con retardo, sirena), «la lente actúa sobre
toda medición local» da χ² 0.64 contra 4.63 si sólo actuara sobre las Cefeidas y 6.15
para ΛCDM-Planck, pero el criterio preregistrado dice SIN POTENCIA (σ combinado hoy 2.25,
hace falta 1.03). Signo: a favor, no concluyente. Qué publicaciones futuras (máseres,
TDCOSMO) bajarían ese σ, y cuándo.
