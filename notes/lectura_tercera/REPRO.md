# Reproducibilidad — tercera lectura (agente REPRO, 2026-10-10)

## Resumen
6 hallazgos: 1 enlace-roto (H1) · 1 dependencia-de-paquete desactualizada (H2) ·
1 paquete-faltante en requirements (H3) · 1 defecto estructural de portabilidad dvc.yaml
(H4, el más grave) · 2 clasificaciones de rutas externas sin automatizar (bloque B de §3) ·
0 en data/raw (§4, limpio) · 0 nuevo en Zenodo/PDF-staleness (§5, deuda ya autodeclarada) ·
0 en secretos (§6, limpio).

## 1. README.md vs lo que existe en el repo

### H1 · README.md:330 · dimensión 5 (trazabilidad) · enlace-roto · confianza ALTA
- Dice: `[docs/SSEE_Constant_Dictionary.md](docs/SSEE_Constant_Dictionary.md)`.
- El archivo real vive en `zenodo_dictionary/SSEE_Constant_Dictionary.md` (confirmado con `find`); no existe ninguna copia en `docs/`. Un lector que clone el repo y siga el enlace obtiene 404.
- Reemplazo propuesto: `docs/SSEE_Constant_Dictionary.md` → `zenodo_dictionary/SSEE_Constant_Dictionary.md` (las dos apariciones del enlace en esa línea).

### Resto de rutas citadas en README (verificadas, sin defecto)
`src/p02_mcmc/ssee_paper2_mcmc.py`, `src/p03_cmb/b1_minimiza.py`, `src/p03_cmb/ssee_paper3_cobaya_unified.py`,
`VERIFICATION_LEDGER.md`, `RETRACTIONS.md`, `OPEN_PROBLEMS.md`, `AUDIT.md`, `submission_packages/`,
`archive/codigo/build_arxiv_packages.py`, `assets/banner_ssee.svg`, `results/figures/fig1_w0wa_plane.png`,
`results/figures/fig_readme_tensions.png`, `CITATION.cff` — todos existen. El comando de instalación
`pip install -r requirements.txt` corre contra un archivo que existe y que lista versiones (ver §2).
El bloque "Paper 3" (`export COBAYA_PACKAGES_PATH=...` + `python src/p03_cmb/b1_minimiza.py`) es ejecutable
tal cual está escrito (ruta de ejemplo, no hace falta que exista para que el comando sea válido).

## 2. requirements/environment vs imports de dvc.yaml

### H2 · environment.yml:6 · dimensión 4 (coherencia) · número-erróneo (dependencia desactualizada) · confianza ALTA
- Dice: `environment.yml` fija `numpy>=1.24`.
- Debe decir / por qué: `requirements.txt:5` (comentario explícito, 2026-09-19) dice que **ese mismo piso 1.24
  fue corregido a `numpy>=2.0`** porque `src/p06_growth/boss_rsd_model.py` usa `np.trapezoid`, que sólo existe
  desde numpy 2.0 — "una auditoría externa montando el entorno desde cero" reprodujo el fallo con el piso viejo.
  `environment.yml` (la ruta conda) no se actualizó y sigue fijando el piso que causa el mismo fallo documentado.
  Quien instale con `environment.yml` en vez de `requirements.txt` reproduce exactamente el bug ya encontrado.
- Reemplazo propuesto: `numpy>=1.24` → `numpy>=2.0` en `environment.yml:6`.

### H3 · requirements.txt / environment.yml · dimensión 5 (trazabilidad) · paquete-faltante · confianza ALTA
- Dice: ninguno de los dos archivos lista `pandas`, `healpy` ni `pyccl`.
- Debe decir / por qué: tres etapas de `dvc.yaml` los importan de verdad en tiempo de ejecución:
  - `pandas` — `src/p09_hubble/h0_por_profundidad.py:52` (`import pandas as pd`), etapa dvc activa (grep confirma uso en `cmd:`).
  - `pyccl` — `src/p11_sondas/erosita_conteos.py` (líneas 113,132,147,222, import perezoso dentro de función) y
    `src/p11_sondas/erosita_cr.py` (líneas 247,338,370), usado por las etapas `erosita_completitud` (dvc.yaml:1195) y
    `erosita_cr` (dvc.yaml:1370).
  - `healpy` — `src/p11_sondas/erosita_cr.py:195` (import perezoso), misma etapa `erosita_cr`.
  Como los imports están dentro de funciones (lazy), `python -c "import <script>"` no falla al cargar, pero la
  etapa SÍ falla en tiempo de ejecución si el paquete no está instalado — un tercero que siga sólo `requirements.txt`
  no puede reproducir esas 3 etapas.
- Reemplazo propuesto: añadir a `requirements.txt` (y a la sección `pip:` de `environment.yml`): `pandas>=2.0`,
  `pyccl>=2.0` (CCL, LSST-DESC; requiere compilador C/CMake — anotarlo), `healpy>=1.16`.

### Nota aparte — venv distinto para erosita_cr (ver H6 en §3)
`dvc.yaml:1370` invoca `/mnt/datos/SSEE_data/erosita/venv/bin/python` en vez de `.venv/bin/python3` para la etapa
`erosita_cr`, el único lugar de todo `dvc.yaml` que usa un intérprete fuera del venv estándar del repo — indicio de
que `pyccl`/`healpy` no se instalaron en `.venv` sino en un entorno aparte. Esto agrava H3: ni `requirements.txt`
ni `environment.yml` documentan la necesidad de ese segundo entorno.

## 3. dvc.yaml — deps/outs y rutas absolutas

227 líneas de `dvc.yaml` contienen `/home/mike` o `/mnt/datos` (literal, no vía
variable de entorno — confirmado: `grep -c SSEE_DATA_DIR dvc.yaml` → 0). Esto
contradice directamente lo que dice el propio README.md:132-142: *"Scripts derive
all in-repo paths from their own location (no hardcoded absolute paths)... Override
the output location with `export SSEE_DATA_DIR=...`"*. La variable SÍ existe y SÍ la
respetan los scripts Python (`src/p02_mcmc/ssee_paper2_mcmc.py:28` y otros 4 archivos:
`os.environ.get("SSEE_DATA_DIR") or ("/mnt/datos/SSEE_data" if os.path.isdir("/mnt/datos")
else "results/data")`), pero **`dvc.yaml` nunca la usa**: sus `deps:`/`outs:` llevan la
ruta absoluta tecleada. Resultado práctico: ejecutar un script Python suelto es portable;
ejecutar `dvc repro` de cualquiera de estas ~40 etapas, no — DVC comparará contra una ruta
que en una máquina nueva no existe, sin importar qué diga `SSEE_DATA_DIR`.

### H4 · dvc.yaml (227 líneas) · dimensión 5 (trazabilidad) · dependencia-rota-portabilidad · confianza ALTA
- Dice: README promete portabilidad total vía `SSEE_DATA_DIR`; `dvc.yaml` hardcodea
  `/mnt/datos/SSEE_data/...` y `/home/mike/cobaya_packages/...` en `deps:`/`outs:` de
  decenas de etapas (`mcmc_full_posteriores`, `h0_por_profundidad`, `h0_por_metodos`,
  `kids_publicados`, `spt3g_calibrador`, `hiclass_campo`, `R3_rehecho`, `leer_conjunta`,
  `sello_*`, `lcdm_conjunta_*`, `desi_dr2_w0wa_momentos`, etc.)
- Debe decir / por qué: para que `dvc repro` sea reproducible por un tercero, las rutas
  fuera del repo deben pasar por una variable de entorno (p.ej. `${SSEE_DATA_DIR}` que DVC
  sí soporta interpolar) o documentarse como requisito explícito de infraestructura
  ("clona con /mnt/datos montado en este punto exacto, o exporta SSEE_DATA_DIR antes de
  `dvc repro`" — y aun así, `dvc.yaml` no lo interpola, así que hoy ni exportando la
  variable funcionaría sin editar el archivo).
- Reemplazo propuesto: (a) documentar explícitamente en AUDIT.md/README que `dvc repro`
  NO es portable fuera de la máquina de Mike sin editar `dvc.yaml`, o (b) sustituir las
  227 ocurrencias por `${SSEE_DATA_DIR}/...` si la versión de DVC en uso interpola env vars
  en `dvc.yaml` (verificar con `dvc --version`; requiere sintaxis `${...}` + `vars:`/`.env`).
  Dado el volumen, esto es una decisión de alcance para Mike, no un parche de una línea.

### Clasificación de las rutas externas (dato descargable vs dependencia rota)

**A. Dato externo con manifiesto (origen URL + sha256) — reproducible con trabajo manual:**
`data/manifiesto_descargas_T2.json` (35 ficheros, fecha 2026-09-26) documenta origen y
sha256 para los grupos **des_y3, sn_ia (Pantheon+SH0ES), union3, cmb_lensing, eROSITA/erosita**.
`src/verificacion/manifiesto_datos_T2.py` sólo **verifica** bytes contra ese manifiesto — no
hay script de descarga automática (confirmado: sin `requests.get`/`urlretrieve`/`wget` en ese
archivo ni en otro que lo invoque). Un tercero debe bajar cada URL a mano al path exacto.
Clasificación: dato externo descargable, documentado, SIN automatizar.

**B. Dato externo SIN manifiesto en el repo — dependencia rota para un tercero:**
- `/home/mike/cobaya_packages/data/planck_2018/.../plik_lite_v22_TTTEEE.clik/...` y
  `.../planck_supp_data_and_covmats/lensing/2018/...` (Planck 2018 vía `cobaya-install`,
  existe mecanismo oficial de Cobaya, pero ni el nombre de usuario `mike` ni el paquete
  concreto a instalar están documentados en AUDIT.md/README más allá de la env var
  `COBAYA_PACKAGES_PATH`, que tampoco usa `dvc.yaml`).
- `/mnt/datos/SSEE_data/kids1000/...` y `.../kids_legacy/...` (KiDS-1000 / KiDS-Legacy, datos
  públicos de la colaboración KiDS) — sin entrada en ningún manifiesto del repo.
- `/mnt/datos/SSEE_data/boss_dr12/public_material_RSD` (BOSS DR12 público) — sin manifiesto.
- `/mnt/datos/SSEE_data/desi_dr2_official/cosmology_chains/cobaya/...` (cadenas oficiales
  DESI DR2, probablemente Zenodo) — sin manifiesto ni URL en el repo.
- `/mnt/datos/SSEE_data/literatura/h0_metodos/*/main.tex`, `.../cmb_lensing/papers/*/main.tex`,
  `.../erosita/paper_*/...tex` (fuentes LaTeX de arXiv cacheadas para verificación de citas) —
  sin manifiesto; se sabe por `data/raw/FUENTES.yaml` que el patrón del proyecto es
  "bajado de arxiv.org/e-print" en tal fecha, pero esos .tex de `/mnt/datos` no están en
  `FUENTES.yaml` (que sólo cubre `data/raw/`).
- `/mnt/datos/hi_class/class` — binario compilado del fork hi_class; ni descargable ni
  documentado (requiere compilar desde `class_ssee/`/hi_class fork; no hay instrucción de
  build en AUDIT.md/README para esta ruta concreta).

**C. NO son datos externos — son salidas pesadas del propio pipeline SSEE, fuera de
git/dvc por tamaño (cadenas MCMC):** `/mnt/datos/SSEE_data/chains_p6/...` (boss, kids,
kids_legacy, conjunta), `/mnt/datos/SSEE_data/mcmc/mcmc_full/...`,
`/mnt/datos/SSEE_data/mcmc/paper2_3models/...`. Para un tercero esto es regenerable
en principio (son outputs de otras etapas dvc), pero sólo si antes resuelve H4 — hoy
`dvc repro` desde cero en una máquina limpia fallaría al no encontrar ni poder crear
esas rutas exactas sin montar algo en `/mnt/datos`.

**Conclusión de §3:** de los tres bloques, B es el más grave (dato real, externo,
cero trazabilidad en el repo) y A es intermedio (trazable pero manual). Ambos quedan
subordinados al defecto estructural H4: mientras `dvc.yaml` no parametrice las rutas,
ningún manifiesto por sí solo basta para que `dvc repro` corra en otra máquina.

## 4. data/raw — fuentes citadas

**Sin hallazgo.** Los 15 archivos de datos de `data/raw/` (excluyendo el propio
`FUENTES.yaml`) tienen entrada en `data/raw/FUENTES.yaml` con cita (autor/año/arXiv/tabla)
y, para los que tienen extracto literal, sha256 verificable. `data/README.md` documenta
además el propósito de cada csv y la regla de procedencia (post-incidente DR1/DR2,
2026-07-01: "scripts hardcoding data en vez de cargar el csv son regresión"). Dos huecos
declarados HONESTAMENTE por el propio `FUENTES.yaml` (no son hallazgos nuevos, ya están
anotados ahí con "Deuda abierta"): `cosmic_chronometers.csv` no lo usa el MCMC de P2 (su
prueba H(z) usa 11 puntos tecleados a mano, uno de ellos BAO de WiggleZ mal etiquetado como
cronómetro) y `ρ(H₀,Ωm)=−0.85` de `planck2018_prior.csv` no está cotejado contra Tabla 2
(viene de cadenas). Confianza ALTA en que §4 está limpia; estas dos deudas ya están
reconocidas en el cajón correcto y no se duplican aquí.

## 5. Paquete Zenodo (00–15 + zip fuente)

No existe en el repo un script o lista que arme exactamente "16 archivos 00–15 + zip
fuente" con esa numeración — búsqueda exhaustiva (`find -iname "*zenodo*"`, grep de
"00-15"/"16 archivos" en todos los .md) no encuentra ese esquema. Lo que SÍ existe:

- `zenodo_dictionary/` — paquete YA preparado para el Zenodo del diccionario de
  constantes (DOI concept 20684908 según MEMORY.md), con su propio `.zenodo.json`,
  `SSEE_Constant_Dictionary.md`, `ssee_constants.py`, `SSEE_Prediction_Register.md`, LICENSE.
- `submission_packages/` — 10 `.tar.gz` arXiv (uno por paper) + README, generados por
  `archive/codigo/build_arxiv_packages.py` (confirmado existente). **El propio
  `submission_packages/README.md` declara que estos 10 bundles están STALE** (fecha
  2026-06-12, anteriores al reframe ω_m-directo de 2026-06-18/19 y a la partícula φ-DM
  canónica): el bundle de Paper 6 todavía contiene **m_φ = 36.95 eV** (una era retirada
  dos reframes antes de los 40.70 eV, que a su vez quedaron retirados por completo el
  2026-08-01). Esto NO es un hallazgo nuevo — ya está auto-declarado con instrucción
  explícita de regenerar antes de enviar ("How to regenerate... do this at submission
  time"). Confirmo que la condición sigue vigente hoy (los .tar.gz no se han regenerado,
  README fecha jul-25). Clasificación: deuda ya declarada, confianza ALTA en que sigue abierta.
- `src/verificacion/audita_pdfs_zenodo.py` — audita el TEXTO IMPRESO de los PDF de `docs/`
  contra `CANONICAL_VALUES.yaml` (vivo vs. narrado), pero **no construye** el paquete de
  subida; es un auditor de contenido, no un empaquetador.
- No hay script de empaquetado/subida real a Zenodo en el repo (ni API call, ni zip de
  todo el paquete). La publicación Zenodo pasada (DOI 10.5281/zenodo.20093447, ver README)
  se hizo manualmente, a juzgar por la ausencia de cualquier `requests`/`zenodo`-API call
  en `src/`. Para la nueva versión, Mike necesitará armar y subir el paquete a mano (o un
  agente futuro deberá escribir el empaquetador, que hoy no existe).

### PDF vs .tex (más nuevo que su fuente) — verificado con el historial de git, no sólo mtime
El `mtime` de archivo es engañoso en esta sesión porque hay ediciones concurrentes de
otros agentes de la "tercera lectura" (confirmado: varios `.tex` mostraban mtime de hoy
sin diff real, o con diffs aún no commiteados). Verificación correcta: para cada PDF de
`docs/` con `.tex` en `manuscript/`, comparé `git diff <commit-que-generó-el-PDF>..HEAD`
sobre su `.tex` — **el diff es vacío para los 15 pares** (ningún `.tex` tiene cambios
COMMITEADOS posteriores a la última recompilación de su PDF). Los casos que parecían
"stale" por mtime (Paper7, Paper8, Endorser, Paper1, Paper4, Sealed, Unified) resultaron
ser: (a) ediciones en curso SIN commitear de esta misma sesión multi-agente (ya resueltas:
Paper8 se recompiló mientras yo auditaba, commit `1250265`), o (b) un comentario LaTeX
(`% ORIGEN-VALOR: ...`, commit `b08f141`) que no cambia el texto renderizado. **Sin hallazgo
nuevo en esta dimensión**, confianza ALTA (verificado contra git, no sólo contra el reloj
del sistema de archivos).

## 6. Secretos

- `.env` (raíz, 26 bytes) y `.zenodo_token` — **ambos en `.gitignore`** (líneas 5/85 para
  `.env`/`*.env`, líneas 86/87 para `zenodo_token`/`.zenodo_token`) y **ninguno trackeado**
  (`git ls-files | grep -E "^\.env$|^\.zenodo_token$"` → vacío). Correcto.
- `git grep -I -n -E "ZENODO_TOKEN\s*=|api[_-]?key\s*[:=]"` sobre todo el árbol versionado
  (excluyendo `.venv`) → **0 resultados**. Sin tokens ni api-keys filtrados en archivos
  versionados.
- **Sin hallazgo.** Confianza ALTA.
