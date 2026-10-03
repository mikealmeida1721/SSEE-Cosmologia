"""REGISTRO DE REGLAS — la única declaración de qué vigila el guardián.

POR QUÉ EXISTE (2026-07-29). Mike: «que el guardián me dé verde no significa que
esté bien, y eso es preocupante, porque lo creamos para tener la confianza de que
está bien». Tenía razón: un VERDE demostraba que nada saltó, no que algo habría
saltado. Y la primera prueba de mutación destapó un valor sencillamente MAL que
pasaba verde porque la exención de una regla caía justo en el hueco de otra.

CUATRO MANERAS DE ESTAR VERDE SIN ESTAR BIEN, y qué las detecta:

  vacía        la regla no examina ningún candidato    → caso de MUTACIÓN obligatorio
  enmascarada  la exención de otra tapa el hallazgo     → cada exención dice QUIÉN cubre
  duplicada    dos reglas, misma intención y ámbito     → colisión (intencion, ambito)
  huérfana     regla añadida sin poder verificarla      → sin entrada aquí, no entra

CONTRATO PARA AÑADIR UNA REGLA (esto es el método que faltaba):

  1. ¿Existe ya una regla con esta misma `intencion` y `ambito`? Si sí, se REFINA
     esa. No se crea una nueva «igual pero con cambios».
  2. Se declara aquí: intencion, ambito, exenciones (cada una con `cubierta_por`)
     y al menos un caso de `mutacion`.
  3. Se corre `mutacion_guardian.py`: el caso debe poner el guardián en ROJO.
     Si no enrojece, la regla no sirve todavía — no se commitea.
  4. `meta_guardian.py` comprueba 1–3 y que ninguna capa del código quede sin
     entrada aquí (ni al revés).

`ambito` responde «¿sobre qué mira?»; `intencion`, «¿qué exige?». Dos reglas
pueden compartir una de las dos, nunca las dos.
"""

# Anclas de mutación: texto REAL del Paper 1 sobre el que se inyecta el defecto.
# Si un ancla deja de existir, la prueba avisa en vez de pasar en silencio.
TEX_MUTACION = "manuscript/SSEE_Paper1_Framework.tex"

# ORIGEN de los numeros de los casos de `mutacion` (R65, 2026-09-19). Casi
# todos son DEFECTOS INYECTADOS A PROPOSITO: su origen es que alguien los
# invento para ver si la regla enrojece. Uno es el texto real del ancla.
# ORIGEN-VALOR: 0.8399497813 — defecto inyectado (canon): -Tr/Mv con la ultima cifra movida
# ORIGEN-VALOR: 0.7000 — defecto inyectado (yaml): techo sigma8 alterado a proposito
# ORIGEN-VALOR: 66.1234 — defecto inyectado (procedencia): H0 que ningun log respalda
# ORIGEN-VALOR: 0.965123 — defecto inyectado (precision): n_s con error 4e-4
# ORIGEN-VALOR: 0.965548 — defecto inyectado (precision): n_s con error 1e-5
# ORIGEN-VALOR: 0.935558 — defecto inyectado (precision): n_s con error 3e-2
# ORIGEN-VALOR: 0.812340 — defecto inyectado (precision): w0 alterado en otra fila
# ORIGEN-VALOR: 58.068884 — ancla REAL: 2*phi^7 = 58.0688837 redondeado a 6 decimales
# ORIGEN-VALOR: 0.700000 — defecto inyectado (coherencia yaml): valor distinto sin OP
# ORIGEN-VALOR: 67.51111 — defecto inyectado (log-respaldo): H0 que el log no contiene
REGLAS = {
    # ── capas de FÍSICA ──────────────────────────────────────────────────────
    # No viven en un manuscrito: afirman identidades algebraicas. Se prueban
    # tocando el archivo donde vive lo que afirman.
    "canon": dict(
        capa="Fuente canónica — ssee_core.py",
        intencion="nucleo-vs-recomputacion",
        ambito="src/ssee_core.py contra el álgebra rehecha por el guardián",
        # Es el eslabón que conecta las capas de física con el MODELO: la Capa 2
        # compara su propia recomputación contra literales; sola no notaría que
        # ssee_core derivó. Esta sí, porque rehace el álgebra por su cuenta.
        exenciones=[],
        archivo="src/ssee_core.py",
        mutacion=[("una constante del núcleo alterada",
                   "W0          = -T_R / M_V", "W0          = -T_R / M_V * 1.0001")],
    ),
    "V-L2": dict(
        capa="2 — parámetros cosmológicos derivados",
        intencion="identidad-algebraica",
        ambito="álgebra de fondo (w0, wa, Ω_DE, Ω_m, H_alg, n_s, α_K)",
        # La mutación prueba VIVEZA —que la comprobación compara de verdad y está
        # clavada a un número— no que el modelo sea correcto. El puente al modelo
        # lo pone «canon»; el puente al registro publicado, R20/R26.
        exenciones=[],
        archivo="src/verificacion/ssee_verify.py",
        # Historia de este caso, que enseña más que el caso: la primera versión
        # movía el literal 7.7e-7 y NO enrojecía, porque la capa toleraba 1e-6
        # absoluto. Al medir el residuo REAL (peor: 3.9e-9) resultó que la holgura
        # era 256× — y dentro cabía un literal equivocado: r estaba escrito
        # 0.0081306227 en vez de 0.0081306188. Se corrigió el literal y se apretó
        # la tolerancia a 1e-9. Ahora basta con mover el último dígito.
        mutacion=[("el valor esperado de w0 movido en su última cifra",
                   '"V-L2-01 w0":        (-Tr / Mv,                      -0.8399497713)',
                   '"V-L2-01 w0":        (-Tr / Mv,                      -0.8399497813)')],
    ),
    "V-L3": dict(
        capa="3 — mecanismos y derivaciones",
        intencion="identidad-algebraica",
        ambito="mecanismos (n_s/r, f_screen, m_φ, EFT, IS, dos sectores)",
        exenciones=[],
        archivo="src/verificacion/ssee_verify.py",
        prefijos=["V-L3"],
        # Se muta la AFIRMACIÓN, no la etiqueta: un primer caso añadía «[MUT]» al
        # nombre del check y por supuesto no cambiaba nada — el rótulo no es lo
        # que se comprueba. Y un segundo rompía f_screen, que resultó ser un
        # check de la Capa 2 («L2 identidad»), no de la 3. Lo dijo la atribución,
        # que existe justamente para eso.
        mutacion=[("la identidad EFT lambda^2 = 3 Om_m,dyn rota",
                   "abs(lam_eft ** 2 - 3 * Om_m_dyn) < 1e-12",
                   "abs(lam_eft ** 2 - 4 * Om_m_dyn) < 1e-12")],
    ),
    "V-L4": dict(
        capa="4 — confrontaciones con datos",
        intencion="dato-vs-prediccion",
        ambito="σ8/S8, tensiones KiDS, ΔBIC de P2/P3/P6",
        exenciones=[],
        archivo="CANONICAL_VALUES.yaml",
        prefijos=["V-L4"],
        # Se muta el YAML, no el guardián: desde 2026-07-29 estas comprobaciones
        # LEEN el valor de la fuente en vez de llevarlo escrito. Antes σ8 se
        # asignaba «= 0.8335» y se comprobaba «abs(σ8 − 0.8335) < 1e-2» — una
        # tautología imposible de fallar. La mutación es la única forma en que
        # eso salía a la luz: el check estaba VERDE y no miraba nada.
        # El ancla NO lleva el valor (2026-09-19). Lo llevaba —«0.8335»— y se
        # quedo rancia el 2026-09-08, cuando la propagacion del techo S8 lo
        # movio a 0.814854: desde entonces este caso no mutaba nada y la suite
        # lo reportaba como ANCLA?. Mismo error que el de los .md, en el
        # cajon de al lado: un literal copiado se queda atras en silencio.
        # Anclando a la CLAVE y comentando el resto de la linea, la mutacion
        # sobrevive a cualquier futuro cambio de valor.
        mutacion=[("el techo σ8 del YAML alterado",
                   "sigma8_single_ceiling:",
                   "sigma8_single_ceiling: 0.7000  #")],
    ),
    "DESI": dict(
        capa="DESI — procedencia BAO: csv == DR2 Tabla 4 oficial",
        intencion="procedencia-del-dato",
        ambito="data/raw/desi_dr2_bao.csv contra la tabla oficial 2503.14738",
        exenciones=[],
        archivo="data/raw/desi_dr2_bao.csv",
        prefijos=["DESI"],
        mutacion=[("un punto BAO alterado respecto a la tabla oficial",
                   "0.295", "0.296")],
    ),
    # ── capas de PROCEDENCIA: artefacto contra su fuente ─────────────────────
    "R33": dict(
        capa="R33 — logs vs núcleo: ningún log activo con constante retirada",
        intencion="artefacto-sin-constante-retirada",
        ambito="results/logs/*.log",
        exenciones=[("logs declarados históricos en PROPAGACION.yaml", None)],
        archivo="results/logs/mcmc_paper2_reframe.log",
        prefijos=["R33"],
        mutacion=[("un log activo imprimiendo un Σm_ν retirado",
                   "[   0.0m] ======================================================================",
                   "[   0.0m] Sigma_m_nu = 0.06902 eV\n[   0.0m] ==================================")],
    ),
    "R34": dict(
        capa="R34 — fuentes vs núcleo: ningún .py hardcodea constante retirada",
        intencion="fuente-sin-constante-retirada",
        ambito="src/**/*.py (salvo el núcleo y el propio guardián)",
        # La infraestructura de verificación queda fuera porque lleva los valores
        # retirados a propósito. Punto ciego DECLARADO: si un día un script de
        # modelo se llamara igual que uno de estos, R34 no lo miraría.
        exenciones=[("núcleo, guardián, registro y mutación (llevan los retirados a propósito)",
                     None)],
        archivo="src/desi_dr2_data.py",
        prefijos=["R34"],
        mutacion=[("un script activo con Σm_ν retirado escrito a mano",
                   '"""\nDESI DR2 BAO',
                   '"""\nDESI DR2 BAO"""\nC_nu = 94.07\n"""')],
    ),
    "Procedencia": dict(
        capa="Procedencia — valores de pipeline vs log committeado",
        intencion="valor-de-pipeline-con-log",
        ambito="sección B del VERIFICATION_LEDGER contra results/logs/",
        exenciones=[],
        archivo="VERIFICATION_LEDGER.md",
        prefijos=["procedencia", "Procedencia"],
        mutacion=[("un valor de pipeline que su log no respalda",
                   "**67.7869 ⁺⁰·³⁵¹/₋₀·³⁵² km/s/Mpc**",
                   "**66.1234 ⁺⁰·³⁵¹/₋₀·³⁵² km/s/Mpc**")],
    ),
    "R20": dict(
        capa="R20 — anclas observacionales (código ⊆ CANONICAL_VALUES.yaml)",
        intencion="dato-observacional-desde-el-yaml",
        ambito="constantes de datos en el código contra CANONICAL_VALUES.yaml",
        exenciones=[],
        archivo="CANONICAL_VALUES.yaml",
        prefijos=["R20"],
        # Ya la prueba `test_guardian.py`, que llegó antes y también atribuye.
        # Duplicar el caso no es sólo trabajo repetido: cuando una copia se
        # actualiza y la otra no, el guardián «demuestra» dos cosas del mismo
        # punto y nadie sabe cuál manda. Lo detectó M7.
        probada_en="test_guardian.py",
        mutacion=[],
    ),
    "R26": dict(
        capa="R26 — procedencia declarada de los canónicos",
        intencion="canonico-con-procedencia-completa",
        ambito="bloque `provenance` de CANONICAL_VALUES.yaml",
        exenciones=[],
        archivo="CANONICAL_VALUES.yaml",
        prefijos=["R26"],
        # Ya la prueba `test_guardian.py`, que llegó antes y también atribuye.
        # Duplicar el caso no es sólo trabajo repetido: cuando una copia se
        # actualiza y la otra no, el guardián «demuestra» dos cosas del mismo
        # punto y nadie sabe cuál manda. Lo detectó M7.
        probada_en="test_guardian.py",
        mutacion=[],
    ),
    "archivo": dict(
        capa="Archivo — bitácora cubre cada cajón archivado",
        intencion="cajon-archivado-documentado",
        ambito="subcarpetas de archive/ contra archive/README.md",
        # Punto ciego DECLARADO: la capa comprueba «¿aparece el nombre del cajón
        # en el texto?» como SUBCADENA. Un cajón llamado «chain» quedaría
        # documentado por una mención de «chains», y una mención en prosa ajena
        # cuenta igual que una entrada de bitácora. Lo descubrió esta mutación:
        # el primer caso renombraba «audio», que sale 5 veces, así que quitar una
        # no cambiaba nada. Se usa el cajón mencionado UNA sola vez.
        exenciones=[("el nombre del cajón se busca como subcadena, no como entrada", None)],
        archivo="archive/README.md",
        prefijos=["archivo"],
        mutacion=[("el único cajón mencionado una vez, borrado de la bitácora",
                   "manuscript_superseded", "manuscript_XXXXXXXXXX")],
    ),
    "diccionario": dict(
        capa="Diccionario — integridad de nodos (script ⊆ maestro)",
        intencion="nodo-del-script-existe-en-el-maestro",
        ambito="FAMILY de look_elsewhere_full.py contra el diccionario maestro",
        # Se muta el CONSUMIDOR, nunca el maestro: vive en sandbox_unificado/, que
        # es submódulo del repo público y no se toca antes del envío.
        exenciones=[("alias de nombre declarados en el guardián "
                     "(KRYSTOS_V, ATLAS, PHOENIX) mientras el maestro no se resincroniza",
                     None)],
        archivo="src/estadistica/look_elsewhere_full.py",
        prefijos=["diccionario", "R13"],
        mutacion=[("un nodo del script que no existe en el maestro",
                   '"IGNIS": IGNIS, "KRYSTOS_V": KRYSTOS_V,',
                   '"IGNIS": IGNIS, "KRYSTOS_V": KRYSTOS_V, "NODO_FANTASMA": IGNIS,')],
    ),
    "memorias": dict(
        capa="Memorias — coherencia de las 3 memorias",
        intencion="memoria-sin-valor-retirado",
        ambito="CLAUDE.md, VERIFICATION_LEDGER.md y el vault Obsidian",
        exenciones=[("valores retirados marcados explícitamente como tales", None)],
        prefijos=["memoria"],
        probada_en="test_guardian.py",
        mutacion=[],
    ),
    "manuscritos": dict(
        capa="Manuscritos — reglas R1 (cronología) y R2 (multidominio)",
        intencion="prosa-sin-cronologia-ni-multidominio",
        ambito="manuscript/*.tex y README.md",
        exenciones=[],
        prefijos=["R1 ", "R2 ", "manuscritos", "R17", "R19"],
        probada_en="test_guardian.py",
        # R17 y R19 viven bajo esta entrada y test_guardian.py YA las
        # prueba (lineas 152 y 164). Escribi casos propios para ambas y
        # los verifique antes de descubrirlo: eran duplicados. M7 los
        # cazo. La deuda real de M9 era 22, no 24 — los contaba como
        # descubiertos por leer la CLAVE del registro y no sus prefijos.
        mutacion=[],
    ),
    "R25": dict(
        capa="R25 — parametrización ω_m absoluto (no congelar Ω_m en el MCMC)",
        intencion="parametrizacion-correcta-del-mcmc",
        ambito="src/**/*.py y class_ssee/**/*.py",
        exenciones=[("test_guardian.py, que lleva la cadena del error a propósito", None)],
        prefijos=["R25"],
        probada_en="test_guardian.py",
        mutacion=[],
    ),
    "R35": dict(
        capa="R35 — artefacto vs fuente: ningún log más viejo que su script",
        intencion="artefacto-no-anterior-a-su-fuente",
        ambito="results/logs/*.log contra la fecha de commit de su script",
        exenciones=[("logs históricos y muestreo certificado, declarados en PROPAGACION.yaml",
                     None),
                    ("cambios que sólo tocan prosa: se compara el AST, no el texto",
                     None)],
        archivo="PROPAGACION.yaml",
        prefijos=["R35"],
        # Se repunta un log a un script committeado DESPUÉS y con código distinto:
        # es la forma exacta del defecto que la capa persigue —un resultado que
        # dice venir de un código que ya no es el que corrió—.
        mutacion=[("un log apuntado a un script posterior a él",
                   "  chi2_bao_posterior:         src/p02_mcmc/chi2_bao_posterior.py",
                   "  chi2_bao_posterior:         src/verificacion/ssee_verify.py")],
    ),
    "R39": dict(
        capa="R39 — compuerta de publicación: conoce todas las portadas",
        intencion="compuerta-ve-toda-la-suite",
        ambito="preparar_publicacion.py contra los .tex con \\date{}",
        exenciones=[],
        archivo="src/verificacion/preparar_publicacion.py",
        prefijos=["R39"],
        # Si la compuerta deja de ver un directorio, publicaría dejando ese
        # documento con la fecha vieja y nadie lo notaría: es un fallo silencioso
        # en el único punto donde la suite sale al mundo.
        mutacion=[("la compuerta deja de mirar un directorio de la suite",
                   'for tx in sorted((_REPO / d).glob("*.tex")):',
                   'for tx in sorted((_REPO / d).glob("NADA*.tex")):')],
    ),
    "R30": dict(
        capa="R30 — política de redondeo",
        intencion="redondeo-correcto",
        ambito="prosa .tex, anclas símbolo↔patrón",
        exenciones=[("valores con menos de 4 decimales (no discriminan)", None),
                    ("medidas de Planck/SH0ES, que no son predicciones", None)],
        # Ya la prueba `test_guardian.py`, que llegó antes y también atribuye.
        # Duplicar el caso no es sólo trabajo repetido: cuando una copia se
        # actualiza y la otra no, el guardián «demuestra» dos cosas del mismo
        # punto y nadie sabe cuál manda. Lo detectó M7.
        probada_en="test_guardian.py",
        mutacion=[],
    ),
    "R41": dict(
        capa="R41 — coherencia de precisión",
        intencion="una-precision-por-simbolo",
        ambito="prosa .tex, cantidades CON unidades",
        exenciones=[("precisión declarada en el texto («to three decimals»)", None)],
        mutacion=[("misma cantidad dimensional con dos precisiones",
                   "3(\\varphi+\\pi)^2 \\approx 67.962",
                   "3(\\varphi+\\pi)^2 \\approx 67.9621")],
    ),
    "R37": dict(
        capa="R37 — igualdades de constantes SSEE a 6 decimales",
        intencion="precision-igualdad",
        ambito="prosa .tex, constantes de _C37",
        exenciones=[("cantidades con unidades", "R41")],
        # El caso va en PROSA, no en una fila de tabla: la primera versión usaba
        # «$w_0 = -T_r/M_v$ & $-0.83995$» y la prueba de atribución avisó de que
        # quien lo cazaba era R38 —cuyo ámbito son las tablas— y no R37. Un
        # defecto detectado por la regla equivocada deja a la propia sin probar.
        mutacion=[("constante SSEE en prosa a 5 decimales",
                   "\\times0.96556 = 0.119514$",
                   "\\times0.96556 = 0.11951$")],
    ),
    "R38": dict(
        capa="R38 — igualdades que cruzan celdas de tabla",
        intencion="precision-igualdad",
        ambito="filas de tabla .tex",
        exenciones=[("≈/≃/∼ en la columna 1", "R40"),
                    ("unidad pegada al valor", "R41"),
                    ("\\ldots explícito", None)],
        mutacion=[("valor MAL, error 4e-4 (el que se escapó)",
                   "$n_s = 1-\\varphi^{-7}$ & $0.965558$",
                   "$n_s = 1-\\varphi^{-7}$ & $0.965123$"),
                  ("valor MAL, error 1e-5 (último dígito)",
                   "$n_s = 1-\\varphi^{-7}$ & $0.965558$",
                   "$n_s = 1-\\varphi^{-7}$ & $0.965548$"),
                  ("valor MAL, error 3e-2 (grosero)",
                   "$n_s = 1-\\varphi^{-7}$ & $0.965558$",
                   "$n_s = 1-\\varphi^{-7}$ & $0.935558$"),
                  ("valor MAL en otra fila y otra fórmula",
                   "$w_0 = -T_r/M_v$ & $-0.839950$",
                   "$w_0 = -T_r/M_v$ & $-0.812340$")],
    ),
    "R40": dict(
        capa="R40 — tipo de relación: «=» exacto vs «≈» truncado",
        intencion="tipo-de-relacion",
        ambito="prosa .tex, símbolo↔fórmula↔decimal",
        exenciones=[],
        mutacion=[("igualdad exacta escondida bajo un «≈»",
                   "\\item $\\boldsymbol{\\Omega} = \\pi+\\varphi \\approx 4.7596$",
                   "\\item $\\boldsymbol{\\Omega}$ ($\\pi+\\varphi \\approx 4.7596$)")],
    ),
    "R42": dict(
        capa="R42 — tipo dimensional: número puro vs cantidad física",
        intencion="tipo-dimensional",
        ambito="prosa .tex, H_0 y cocientes adimensionales",
        exenciones=[("mención negada («we do not write it as…»)", None)],
        mutacion=[("igualdad sin unidad",
                   "anchor $H_0/\\kmsu=3(\\varphi+\\pi)^2$ (derived, Paper~9)",
                   "anchor $H_0=3(\\varphi+\\pi)^2$ (derived, Paper~9)"),
                  ("CONFLICTO: ¿la exención de mención enmascara?",
                   "anchor $H_0/\\kmsu=3(\\varphi+\\pi)^2$ (derived, Paper~9)",
                   "This is not a fitted quantity: the anchor "
                   "$H_0=3(\\varphi+\\pi)^2$ (derived, Paper~9)")],
    ),
    "R43": dict(
        capa="R43 — potencias de φ: el decimal tras «=» es el valor",
        intencion="precision-igualdad",
        ambito="prosa .tex, expresiones φ^n",
        exenciones=[("≈/≃ (truncamiento declarado)", "R30")],
        mutacion=[("potencia de φ truncada con «=»",
                   "$2\\varphi^7=58.068884$", "$2\\varphi^7=58.07$")],
    ),
    "R44": dict(
        capa="R44 — constantes de la lectura con «=» a 6 decimales",
        intencion="precision-igualdad",
        ambito="prosa .tex, constantes incorporadas por la lectura",
        exenciones=[("documentos aún no leídos (deuda contada, sólo baja)", None)],
        mutacion=[("Ω_m,dyn a 3 decimales",
                   "$\\Omega_{m,\\rm dyn}=0.160050$ (DESI)",
                   "$\\Omega_{m,\\rm dyn}=0.160$ (DESI)")],
        # SEGUNDO CASO RETIRADO (2026-09-08). Vigilaba SOLAR2_KRYSTOS_V, que
        # es (phi+2pi)^2 * 2Omega = 594.28 — el multiplicador de la particula.
        # Al retirarse esta el 2026-08-01 sus sitios quedaron EXENTOS por la
        # regla de valores retirados, asi que el caso ya no prueba nada. Mi
        # intento de reapuntarlo a «2(varphi+pi)=9.519253» fue un error mio:
        # ese numero es 2Omega, no SOLAR2_KRYSTOS_V, y lo cazaba R37.
    ),
    "R45": dict(
        capa="R45 — estado de los OP: la prosa concuerda con OPEN_PROBLEMS.md",
        intencion="coherencia-con-registro",
        ambito="prosa .tex, menciones OP-N",
        exenciones=[("documentos aún no leídos (deuda contada)", None)],
        mutacion=[# El ancla vieja estaba rodeada de narracion legitima («not solved,
        # but no longer questions»), asi que la exencion la eximia CON RAZON:
        # el caso probaba la exencion, no la regla. Reapuntada a una frase
        # neutra, y con el OP DELANTE de la afirmacion, que es la forma que el
        # detector no veia hasta el ensanchamiento del 2026-09-08. Se inserta al
        # abrir una seccion, lejos de la prosa de retracciones: dentro de
        # ella la exencion actua CON RAZON y el caso probaria la exencion.
        ("OP resuelto citado como abierto, con el OP delante",
                   "\\section{Dark Energy Evolution}",
                   "OP-9 is still open. \\section{Dark Energy Evolution}")],
    ),
    "R46": dict(
        capa="R46 — el guardián hizo todo el trabajo que dice hacer",
        intencion="cobertura-no-vacía",
        ambito="el propio guardián: número de comprobaciones ejecutadas",
        # Catorce capas leen su archivo con `if ... exists()` y varias recorren
        # una SECCIÓN de un documento buscando su encabezado. Si el archivo se
        # mueve o el encabezado se renombra, esas comprobaciones no fallan:
        # desaparecen, y el guardián sigue en VERDE con menos trabajo hecho.
        # R46 es el tripwire: el total sólo puede subir.
        archivo="VERIFICATION_LEDGER.md",
        exenciones=[("subir el piso al añadir capas es legítimo; bajarlo NO", None)],
        mutacion=[("una sección entera del Registro deja de recorrerse",
                   "## B. Valores de pipeline",
                   "## B2. Valores de pipeline")],
    ),

    # ── Lote 2026-09-08 · reglas nuevas que corrían SIN prueba de mutación ──
    # Las 28 reglas de R47 en adelante tenían su auto-test INTERNO (el control
    # de dos polos de R53) pero ninguna había sido probada por fuera: romper el
    # artefacto real y exigir que enrojezca ESA regla y no otra. Un auto-test
    # comprueba el detector contra casos que escribe el propio detector; la
    # mutación lo comprueba contra el repositorio de verdad.
    "R66": dict(
        capa="R66 — constantes del núcleo re-tecleadas como literal",
        intencion="literal-vs-simbolo",
        ambito="todo src/**.py salvo núcleo, guardián y suites",
        archivo="src/p06_growth/prueba_rol.py",
        exenciones=[("líneas marcadas # R66-OK: el literal es deliberado "
                     "(valor citado de un paper, MAP de una cadena, centro "
                     "de una rejilla)", None)],
        mutacion=[("una constante del núcleo vuelta a teclear como literal",
                   "SMNU = _MNU", "SMNU = 0.06849")],
    ),
    "R56": dict(
        capa="R56 — el rótulo general de KAL_0 es retención, no viscosidad",
        intencion="rotulo-vs-entidad",
        ambito="núcleo, guardián y prosa",
        archivo="src/ssee_core.py",
        exenciones=[],
        mutacion=[("KAL_0 rotulado otra vez como viscosidad",
                   "# Structural Retention", "# Structural Viscosity")],
    ),
    "R52": dict(
        capa="R52 — ninguna saturación multiplica a ρ_crit en código activo",
        intencion="saturacion-no-es-densidad",
        ambito="src/**.py fuera de verificacion/",
        archivo="src/p07_eft/fondo_disparo.py",
        exenciones=[("línea que dice explícitamente que NO debe usarse así", None)],
        mutacion=[("una saturación usada como densidad, el bug de β_c",
                   "OM_M = S.OMEGA_M_TOTAL",
                   "OM_M = S.OMEGA_DE * rho_crit"),
                  # 2026-10-03, R52c: la cuarta forma, s_m convertida en densidad
                  # FISICA (× h²), el «caso naive» de ssee_paper3_cmb y class_picos.
                  ("s_m convertida en densidad física (× h²), el caso naive",
                   "OM_M = S.OMEGA_M_TOTAL",
                   "OM_M = S.S_M * h**2")],
    ),
    "R72": dict(
        capa="R72 — ninguna saturación ocupa ranura de densidad en los MANUSCRITOS",
        intencion="saturacion-no-es-densidad",
        ambito="manuscript/*.tex y submission_PRD/*.tex",
        archivo="manuscript/SSEE_Paper3_CMB.tex",
        exenciones=[("frase que lo declara historia o dice que no es densidad", None)],
        # 2026-10-03: la capa existia sin entrada (fallo M1 previo). El caso es el
        # defecto REAL del resumen del PRD hasta 81b1556: Ω_m,dyn presentado como la
        # densidad «dinamica» que no basta para el CMB. Lo atrapa R72c (simbolo).
        mutacion=[("s_m presentada como densidad dinámica, el resumen del PRD",
                   "\\section{The Acoustic Scale and the Matter Density}",
                   "The bare dynamical $\\Omega_{m,\\rm dyn}=0.160$ alone cannot reproduce\n"
                   "the acoustic peaks.\n\\section{The Acoustic Scale and the Matter Density}")],
    ),
    # ── R69–R76: reglas que vivían dentro de la Capa 3 sin caso de mutación ──
    # (M9 las marcaba desde que nacieron; registradas el 2026-10-03). Cada caso
    # inyecta el defecto REAL que la regla existe para ver, en un archivo real.
    "R69": dict(
        capa="R69 — ningún cajón declara un titular que el canónico ya movió",
        intencion="titular-rancio-no-reaparece",
        ambito="*.md de la raiz (salvo CHANGELOG/MEMORY), por parrafo",
        archivo="README.md",
        exenciones=[("parrafos que narran lo que un documento decia (era, decia, historico)", None)],
        mutacion=[("un cajon declara «titular vigente» con el S8 de KiDS-1000, ya movido",
                   "## 📄 Papers",
                   "Titular vigente de crecimiento: S8 = 0.7559 contra KiDS-1000.\n\n## 📄 Papers")],
    ),
    "R70": dict(
        capa="R70 — el régimen IR (68.13) no se presenta como el H_global canónico",
        intencion="regimen-incompleto-no-es-canonico",
        ambito="manuscript/*.tex, submission_PRD/*.tex, *.md de la raiz, CANONICAL_VALUES.yaml",
        archivo="manuscript/SSEE_Paper2_MCMC.tex",
        exenciones=[("el 68.13 rotulado como regimen IR / M->inf / historico", None)],
        mutacion=[("un paper llama canonico al 68.13 sin declararlo regimen IR",
                   "\\section{Conclusions}",
                   "The canonical global expansion rate is $68.13$~km/s/Mpc.\n\n\\section{Conclusions}")],
    ),
    "R71": dict(
        capa="R71 — el delta_c retirado no vuelve como resultado vivo (OP-27)",
        intencion="retractado-no-vigente",
        ambito="manuscript/*.tex, *.md de la raiz, src/**.py",
        archivo="manuscript/SSEE_Paper4_ToE.tex",
        exenciones=[("texto que declara el retiro, lo niega o lo narra en pasado", None)],
        mutacion=[("el postulado delta_c = 1.6284 reaparece como vivo",
                   "\\section{Conclusion}",
                   "The collapse threshold is $\\delta_c = 1.6284$.\n\n\\section{Conclusion}")],
    ),
    "R73": dict(
        capa="R73 — de dónde sale cada número-resultado de los papers",
        intencion="numero-con-origen",
        ambito="manuscript/*.tex (numeros de 3+ cifras)",
        archivo="manuscript/SSEE_Paper2_MCMC.tex",
        exenciones=[("cita en la misma frase o `% ORIGEN-VALOR: <n> — <razon>`", None)],
        mutacion=[("un paper gana un resultado tecleado que no sale de ningun log",
                   "\\section{Conclusions}",
                   "We obtain $H_0 = 71.2837\\pm0.4123$~km/s/Mpc.\n\n\\section{Conclusions}")],
    ),
    "R74": dict(
        capa="R74 — procedencia universal: ningún número sin fuente",
        intencion="numero-con-origen",
        ambito="logs, CANONICAL_VALUES.yaml, papers y cajones",
        archivo="OPEN_PROBLEMS.md",
        exenciones=[("algebra evaluada por el nucleo, referencias arXiv/DOI", None)],
        mutacion=[("un cajon gana un numero sin procedencia",
                   "## OP-2 — Spectral Index",
                   "La razón medida queda en 4.271936.\n\n## OP-2 — Spectral Index")],
    ),
    "R75": dict(
        capa="R75 — cada resultado de la cadena es el que su lock dice",
        intencion="resultado-sellado-intacto",
        ambito="salidas de dvc.yaml contra dvc.lock y sus actas",
        archivo="results/logs/p9_cascada_control.json",
        exenciones=[],
        mutacion=[("un log sellado editado a mano",
                   "\"H0\": 70.39,",
                   "\"H0\": 70.40,")],
    ),
    "R76": dict(
        capa="R76 — dato crudo cotejado contra su fuente",
        intencion="dato-crudo-cotejado",
        ambito="data/raw/** contra data/raw/FUENTES.yaml",
        archivo="data/raw/planck2018_VI/tabla2.tex",
        exenciones=[],
        mutacion=[("un extracto literal de la fuente editado (su sha ya no casa)",
                   "67.36\\pm 0.54",
                   "67.37\\pm 0.54")],
    ),
    "R77": dict(
        capa="R77 — todo lo archivado entra declarado",
        intencion="archivo-declarado",
        ambito="archive/** (versionado) contra archive/README.md y los README de cada carpeta",
        archivo="archive/README.md",
        exenciones=[],
        # Regla de Mike (2026-10-03): a archive se entra con la nota de por qué.
        mutacion=[("un archivo archivado pierde su entrada en la bitácora",
                   "- `SSEE_Paper2_MCMC_Validation_v1.pdf` — llegó en",
                   "- (entrada borrada) — llegó en")],
    ),
    "R59": dict(
        capa="R59 — ninguna ruta de script citada en la prosa apunta al vacío",
        intencion="ruta-viva",
        ambito=".md de la raíz y subcarpetas, .tex de manuscript y PRD",
        archivo="VERIFICATION_LEDGER.md",
        exenciones=[],
        mutacion=[("una ruta de script que ya no existe",
                   "src/p06_growth/perfil_wc_boss.py",
                   "src/p06_growth/perfil_wc_boss_VIEJO.py")],
    ),
    "R60": dict(
        capa="R60 — los papers están limpios de todo lo retirado",
        intencion="retractado-no-vigente",
        ambito="manuscript/*.tex, submission_PRD/*.tex, *.md, src/**.py",
        archivo="manuscript/SSEE_Paper6_Growth.tex",
        exenciones=[("texto que lo narra explícitamente como retirado", None)],
        # 2026-09-19: dos casos mas, y NO son de una regla nueva — son el
        # alcance que le falto a esta. Los dos son defectos REALES del commit
        # 1f05380^, uno por cada pregunta que cerro el punto ciego: el item
        # eximido por el «archived» de su vecino, y la frase que afirma
        # vigencia pese a llevar la marca tres lineas mas abajo.
        mutacion=[("la partícula retirada presentada como vigente",
                   "\\section{Introduction: why",
                   "The particle mass is 40.70 eV.\n\\section{Introduction: why"),
                  ("un item eximido por la marca del item de al lado",
                   "\\section{Introduction: why",
                   "\\begin{itemize}\n\\item Papers archived (Zenodo).\n"
                   "\\item Canonical particle m_phi = 40.70 eV, forward.\n"
                   "\\end{itemize}\n\\section{Introduction: why"),
                  ("una frase que AFIRMA vigencia dentro de un parrafo marcado",
                   "\\section{Introduction: why",
                   "Canonical phi-DM particle m_phi = 40.70 eV (forward "
                   "prediction, zero fitting).\nRetired numbers purged from "
                   "text and figures.\n\\section{Introduction: why")],
    ),

    # ── Lote 2026-09-08 (2/2) · las 24 que corrian sin prueba de mutacion ──
    # Cada caso se verifico UNO A UNO antes de escribirlo aqui: se inyecta el
    # defecto, se corre el guardian y se comprueba a QUE regla se atribuye el
    # fallo. Los que primero cayeron en otra regla o pasaron desapercibidos
    # estan corregidos, no apuntados como estaban.
    "R54": dict(
        capa="R54 — 0.403302 es s_K, jamás alpha_K",
        intencion="etiqueta-vs-valor", ambito="src/**.py, .tex, .yaml, .md",
        archivo="manuscript/SSEE_Paper7_EFT.tex", exenciones=[],
        mutacion=[("el valor de s_K rotulado como alpha_K",
                   "\\section{", "The EFT gives $\\alpha_K = 0.4033$ today.\n\\section{")],
    ),
    "R58": dict(
        capa="R58 — beta_c = -AURA no figura como prediccion viva",
        intencion="retractado-no-vigente", ambito="manuscript/ y submission_PRD/ .tex",
        archivo="manuscript/SSEE_Paper7_EFT.tex",
        exenciones=[("texto que lo narra como retirado o como bug", None)],
        mutacion=[("beta_c = -AURA presentado como correcto al 0.2%",
                   "\\section{",
                   "The conformal coupling is beta_c = -AURA, correct to 0.2\\%.\n\\section{")],
    ),
    "R63": dict(
        capa="R63 — el 0.09 sigma rancio de w0wa",
        intencion="valor-rancio-no-reaparece", ambito="*.md de la raiz y manuscript/*.tex",
        archivo="manuscript/SSEE_Paper7_EFT.tex", exenciones=[],
        mutacion=[("el 0.09 sigma retirado, junto a w0wa",
                   "\\section{",
                   "The w0wa point sits at 0.09 sigma from DESI DR2.\n\\section{")],
    ),
    "R61": dict(
        capa="R61 — la comparacion con el numero puro usa el f_screen COMPLETO",
        intencion="comparacion-con-el-valor-canonico",
        ambito="manuscript/, submission_PRD/, *.md y src/**.py",
        archivo="manuscript/SSEE_Paper7_EFT.tex",
        exenciones=[("el texto rotula el valor como parcial o IR-only", None)],
        mutacion=[("el 68.13 parcial comparado con el numero puro sin rotularlo",
                   "\\section{",
                   "The cascade returns 68.13, compared with the pure number.\n\\section{")],
    ),
    "R55": dict(
        capa="R55 — la cascada de Hubble no invierte su dirección",
        intencion="direccion-de-la-cascada", ambito="manuscript/, submission_PRD/, src/",
        archivo="manuscript/SSEE_Paper7_EFT.tex",
        exenciones=[("linea que lo narra como superado o invertido", None)],
        mutacion=[("el numero puro usado como ENTRADA de la cascada",
                   "\\section{",
                   "The global value follows as 67.962 / (1 - f_screen).\n\\section{")],
    ),
    "R64": dict(
        capa="R64 — ningun evaluador clava w0/wa de SSEE como literal",
        intencion="ecuacion-de-estado-como-argumento", ambito="src/**.py",
        archivo="src/p03_cmb/cmb_eval.py",
        exenciones=[("la cabecera que EXPLICA el bug cita el literal", None)],
        mutacion=[("la ecuacion de estado de SSEE clavada en el dict del modelo",
                   "'mnu': _MNU, 'omk': 0.0,",
                   "'w': -0.8399, 'wa': -0.6700, 'mnu': _MNU, 'omk': 0.0,")],
    ),
    "R67": dict(
        capa="R67 — ninguna regla teclea su propia lista de fixtures",
        intencion="exencion-en-un-solo-sitio", ambito="src/verificacion/ssee_verify.py",
        archivo="src/verificacion/ssee_verify.py",
        exenciones=[("la linea marcada # R67-OK, que es el control de la regla", None)],
        mutacion=[("una regla que vuelve a teclear la lista suelta",
                   'if "archive" in str(_f66) or _f66.name in (_FIXTURES | {"ssee_core.py"}):',
                   'if "archive" in str(_f66) or _f66.name in ("ssee_core.py", "test_guardian.py"):')],
    ),
    "R50": dict(
        capa="R50 — el trinquete de deuda está apretado",
        intencion="tope-sin-holgura", ambito="los topes _DEUDA_MAX del guardian",
        archivo="src/verificacion/ssee_verify.py", exenciones=[],
        mutacion=[("un tope de deuda con holgura sobre la cuenta real",
                   '    "R66": 0,            # constantes del nucleo re-tecleadas (2026-09-08)',
                   '    "R66": 9,            # constantes del nucleo re-tecleadas (2026-09-08)')],
    ),
    "R53": dict(
        capa="R53 — toda regla trae su control del otro lado",
        intencion="regla-con-control", ambito="los checks del propio guardian",
        archivo="src/verificacion/ssee_verify.py", exenciones=[],
        mutacion=[("el tope de reglas sin control, aflojado",
                   "_DEUDA_R53 = 26", "_DEUDA_R53 = 31")],
    ),
    "R47": dict(
        capa="R47 — piezas declaradas como supuesto: ¿rastreadas?",
        intencion="supuesto-con-rastro", ambito="src/**.py fuera de verificacion/",
        archivo="src/p06_growth/prueba_rol.py",
        exenciones=[("la linea dice que NO se asume, o que se mide para saberlo", None)],
        mutacion=[("un supuesto en codigo activo sin OP ni derivacion cerca",
                   "SMNU = _MNU", "# SSEE hypothesis: zeta = KAL0/3\nSMNU = _MNU")],
    ),
    "R48": dict(
        capa="R48 — misma cantidad en dos documentos: ¿mismo valor?",
        intencion="cantidad-cruzada-coherente", ambito="cross_document de CANONICAL_VALUES.yaml",
        archivo="CANONICAL_VALUES.yaml",
        exenciones=[("la entrada declara un op_abierto que explica la discrepancia", None)],
        mutacion=[("dos documentos con valores distintos y sin OP que lo declare",
                   '        valor:   0.839950\n        nota:    "zeta_tilde/(tau_Pi H0) = Omega_DE, con zeta_tilde normalizada\n                  a la entalpia — misma cantidad, mismo valor"\n    op_abierto: "OP-22b"',
                   '        valor:   0.700000\n        nota:    "zeta_tilde/(tau_Pi H0) = Omega_DE, con zeta_tilde normalizada\n                  a la entalpia — misma cantidad, mismo valor"')],
    ),
    "R49": dict(
        capa="R49 — el `source` declarado apunta a un documento real",
        intencion="source-verificable", ambito="los `source:` de CANONICAL_VALUES.yaml",
        archivo="CANONICAL_VALUES.yaml", exenciones=[],
        mutacion=[("un source que cita un paper que no contiene el valor",
                   '    source:     "Paper 1 (registro estructural); src/ssee_core.py:OMEGA"',
                   '    source:     "Paper 8 (registro estructural); src/ssee_core.py:OMEGA"')],
    ),
    "R51": dict(
        capa="R51 — etiqueta de figura vs variable graficada: ¿misma ancla?",
        intencion="etiqueta-concuerda-con-lo-graficado", ambito="src/**.py con matplotlib",
        archivo="src/p09_hubble/ssee_paper9_figures.py", exenciones=[],
        mutacion=[("la etiqueta nombra un ancla distinta de la que se grafica",
                   "ax1.plot(z, fscreen_z, 'k-', lw=2, label=r'$f_{\\rm screen}(z)$')",
                   "curva = H0_alg * fscreen_z\nax1.plot(z, curva, 'k-', lw=2, "
                   "label=r'MIRA anchor $f(z)$')")],
    ),
    "R57": dict(
        capa="R57 — ninguna figura se escribe fuera de results/figures",
        intencion="ruta-de-salida-correcta", ambito="src/**.py a 2+ niveles",
        archivo="src/p06_growth/prueba_rol.py",
        exenciones=[("scripts en src/ directo, donde un solo '..' SI es la raiz", None)],
        mutacion=[("un solo '..' desde un script anidado: la figura cae fuera",
                   "SMNU = _MNU",
                   "import os\nSAL = os.path.join(os.path.dirname(os.path.abspath(__file__)),\n"
                   "    '..',\n    'results', 'figures')\nSMNU = _MNU")],
    ),
    "R62": dict(
        capa="R62 — ningun veredicto de rango con una sola cota",
        intencion="rango-con-sus-dos-cotas", ambito="src/**.py y los scripts citados por OPEN_PROBLEMS",
        archivo="src/p06_growth/prueba_rol.py",
        exenciones=[("un error contra su tolerancia: tiene UNA cota por construccion", None)],
        mutacion=[("un rango de dos extremos validado mirando solo uno",
                   "SMNU = _MNU",
                   "# el rango tipico va de 1e-2 a 10 GeV\nT_rh = 1e-4\nif T_rh < 10:\n"
                   "    print('T_rh dentro del rango')\nSMNU = _MNU")],
    ),
    "R65": dict(
        capa="R65 — los numeros de un script coinciden con su log fuente",
        intencion="numero-respaldado-por-su-log", ambito="src/**.py que declaran `FUENTE: results/logs/`",
        archivo="src/p02_mcmc/regenerate_fig8_bao_residuals.py",
        exenciones=[("identificadores de arXiv y DOI, que no son resultados", None)],
        mutacion=[("un numero que el log declarado como fuente no contiene",
                   "H0=67.52954", "H0=67.51111")],   # ORIGEN-VALOR: 67.52954 — numero de PRUEBA de la mutacion, no un resultado
    ),
    "R36": dict(
        capa="R36 — figura del PRD vs el script que la produce",
        intencion="artefacto-no-mas-viejo-que-su-fuente", ambito="results/figures/*.pdf citadas por el PRD",
        archivo="src/estadistica/ssee_phase_d_savage_cv.py",
        exenciones=[("cambios que solo tocan prosa: se compara el AST", None)],
        mutacion=[("la figura del PRD se atribuye a un script mas nuevo que ella",
                   "import warnings", "import warnings\n_FIG36 = 'fig_cmb_spectrum'")],
    ),
    "R27": dict(
        capa="R27 — look-elsewhere: lo afirmado == lo recomputado",
        intencion="titular-estadistico-recomputado", ambito="manuscript/ y submission_PRD/ .tex",
        archivo="manuscript/SSEE_Paper7_EFT.tex",
        exenciones=[("rangos con «$\\sim$», que son otra cuenta declarada sin privilegio", None)],
        # CEDIDO a test_guardian.py, que ya la prueba (M7 prohibe que las
        # DOS suites lleven caso del mismo punto: cuando una se actualiza y
        # la otra no, el guardian «demuestra» dos cosas y nadie sabe cual
        # manda). El caso propio quedo verificado antes de cederlo.
        probada_en="test_guardian.py",
        mutacion=[],
    ),
    "R28": dict(
        capa="R28 — espejo del diccionario citable",
        intencion="dos-copias-no-derivan", ambito="src/estadistica/look_elsewhere_full.py vs el citable",
        archivo="src/estadistica/look_elsewhere_full.py",
        exenciones=[("el diccionario citable esta gitignoreado: en un clon limpio no aplica", None)],
        # CEDIDO a test_guardian.py, que ya la prueba (M7 prohibe que las
        # DOS suites lleven caso del mismo punto: cuando una se actualiza y
        # la otra no, el guardian «demuestra» dos cosas y nadie sabe cual
        # manda). El caso propio quedo verificado antes de cederlo.
        probada_en="test_guardian.py",
        mutacion=[],
    ),
    "R29": dict(
        capa="R29 — símbolo↔entidad biyectivo",
        intencion="un-simbolo-por-entidad", ambito="manuscript/ y submission_PRD/ .tex",
        archivo="manuscript/SSEE_Paper7_EFT.tex",
        exenciones=[("Paper 6 retirado y Paper 9, declarados aparte", None)],
        # CEDIDO a test_guardian.py, que ya la prueba (M7 prohibe que las
        # DOS suites lleven caso del mismo punto: cuando una se actualiza y
        # la otra no, el guardian «demuestra» dos cosas y nadie sabe cual
        # manda). El caso propio quedo verificado antes de cederlo.
        probada_en="test_guardian.py",
        mutacion=[],
    ),
    "R32": dict(
        capa="R32 — unicidad de N_* = 2 phi^7",
        intencion="unicidad-de-la-solucion", ambito="el barrido m·phi^n del guardian",
        archivo="src/verificacion/ssee_verify.py", exenciones=[],
        mutacion=[("la condicion de pureza alterada: la solucion deja de ser unica",
                   "        _k = -_math.log(1 - (1 - 2 / _N)) / _math.log(phi)",
                   "        _k = -_math.log(1 - (1 - 3 / _N)) / _math.log(phi)")],
    ),
    "R68": dict(
        capa="R68 — el PDF publicado vs el .tex que lo produce",
        intencion="documento-publicado-al-dia",
        ambito="docs/*.pdf contra manuscript/*.tex",
        archivo="manuscript/SSEE_Paper7_EFT.tex",
        exenciones=[("cambios que solo tocan comentarios de LaTeX (%): no "
                     "pueden mover una pagina", None)],
        # El trinquete de 14 es la deuda medida el dia que se abrio la regla.
        # Aflojarlo es la unica forma de que un PDF atrasado pase inadvertido,
        # asi que eso es lo que se muta.
        # Se muta el .tex, que es el defecto REAL: tocar la fuente sin
        # recompilar deja el PDF publicado diciendo otra cosa. El caso
        # anterior aflojaba el trinquete y dejo de valer al llegar la
        # deuda a 0 — un trinquete vacio no se puede aflojar.
        mutacion=[("el .tex cambia y el PDF publicado se queda atras",
                   "\\section{Conclusions}",
                   "The screening fraction is now 0.5.\n\\section{Conclusions}")],
    ),
    "R31": dict(
        capa="R31 — bytecode: lo importado == el fuente",
        intencion="artefacto-compilado-al-dia", ambito="src/ssee_core.py y su __pycache__",
        archivo="src/ssee_core.py", exenciones=[],
        # Caso de ESTADO, no de texto: lo que vigila es un .pyc rancio con el
        # fuente INTACTO byte a byte, y eso no cabe en (archivo, viejo, nuevo).
        # Lo prepara src/verificacion/mutacion_estado.py, que ademas explica la
        # sutileza del mtime que hizo fallar el primer intento.
        estado="r31_pyc_rancio",
        mutacion=[],
    ),
}

# Capas que EXISTEN en el código y todavía NO tienen entrada arriba. No es una
# lista de perdón: es la deuda visible, y sólo puede bajar. Mientras una capa
# esté aquí, su VERDE no está demostrado — puede ser verde por vacío.
SIN_COBERTURA = [
    # VACIA desde el 2026-09-08. Las 8 que estaban aqui —R47 a R55— quedaron
    # registradas y PROBADAS en la tanda de casos de mutacion de ese dia. Una
    # lista de deuda que no se vacia al saldarla miente igual que una que se
    # llena para tapar: el numero deja de decir lo que dice decir.
]
