# KiDS-Legacy con el evaluador VIEJO de cizalla (2026-09-20) — superado

Transcripciones de las tres corridas MCMC de septiembre (sseefijo, ssee, lcdmfijo) sobre
`/mnt/datos/SSEE_data/chains_p6/kids_legacy/`. El evaluador de ξ± que usaban tenía dos defectos
(ξ en el centro geométrico del bin en vez del promedio por pares; integral de Hankel sin converger
a θ grande), corregidos en 282c083; el control por repesado de la cadena oficial pasa con el
evaluador corregido (69f87ec).

Las corridas se rehicieron con el evaluador corregido (cadenas `chains_p6/kids_legacy_v2/`,
2026-10-22…25). Sus transcripciones vigentes están en `results/logs/kids_legacy_{sseefijo,ssee,lcdmfijo}.log`,
separadas de la bitácora de la cola `cola_1022.log` por sus marcas `=== <modelo> INICIO/FIN`.

Valores que cambiaron (viejo → corregido): χ² 417.971/418.336/418.955 → 415.594/414.993/415.735;
logA 3.0255 (0.49σ) → 3.0544 (0.25σ); ΔBIC +6.24/+6.86 → +5.28/+6.02. Retirados en CANONICAL_VALUES.yaml.

Archivos: `kids_legacy_sseefijo.log`, `kids_legacy_ssee.log`, `kids_legacy_lcdmfijo.log`.

**Añadido 2026-11-01:** `cola_kids_legacy.log`, la nota de cola de la v1 (2026-09-19: lcdm encolada
y detenida por decisión de Mike hasta reiniciar). Es registro de la corrida vieja, no fuente de
ningún número. R35 no podía compararlo con su lanzador (`lanzar_kids_legacy.sh`, que no es Python)
y el lanzador cambió para la v2 el 10-28. La cola de la v2 quedó en `cola_1022.log` y siguientes.
