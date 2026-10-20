# Manifiesto de dependencias externas sin trazabilidad (cuarta lectura, reproducibilidad)

Complemento a `REPRO.md` §3. Cubre las ~100 dependencias absolutas de `dvc.yaml`
que NO figuran en `data/manifiesto_descargas_T2.json` ni en `data/raw/FUENTES.yaml`.
Fuente de la lista: `python3 -c "import yaml;y=yaml.safe_load(open('dvc.yaml'))[...]"`
(112 rutas únicas que empiezan en `/`), menos las 34 ya cubiertas por el manifiesto T2.

Clasificación: **A** = dato público de terceros (trazable, se puede volver a bajar),
**B** = producto propio del pipeline SSEE (cadena MCMC, fuera de git/dvc por tamaño),
**C** = literatura (PDF/tex de arXiv cacheado, sólo se cita el id, no se redistribuye).

---

## Grupo: boss_dr12 — Clase A

**Beutler et al. (2017), BOSS DR12 full-shape + RSD power spectrum multipoles**
(el "public material RSD" de la colaboración; usado por `src/p06_growth/boss_dr12_data.py`,
que ya documenta la fuente en su docstring: `https://data.sdss.org/sas/dr12/boss/papers/clustering/`).

- Ruta local: `/mnt/datos/SSEE_data/boss_dr12/public_material_RSD/` (31 archivos, 4.8 MB)
- Origen: https://data.sdss.org/sas/dr12/boss/papers/clustering/ (SDSS SAS, carpeta del paper de Beutler+2017, arXiv:1607.03149)
- Cita: Beutler et al. 2017, MNRAS 466, 2242 (arXiv:1607.03149)
- sha256 (los 31, lista completa):
  - `2e40c75e72a79dc66aa0c4f3652daa307a35268f84cb596314f4430510ca69d8` Beutleretal_cov_patchy_z1_NGC_1_15_1_15_1_10_2045_60.dat
  - `ad49763652014855b3a55c68cf1f935b1c2464d803f45ff137f15c71f11b16f9` Beutleretal_cov_patchy_z1_SGC_1_15_1_15_1_10_2048_60.dat
  - `30345e14b478086f58d37a015b6a644d4093dd7b40550352f13b4315b72f1cf5` Beutleretal_cov_patchy_z2_NGC_1_15_1_15_1_10_2045_60.dat
  - `19c34c3314ec8a25c262487300b6d6387b81ceb666919a8cc6963835aacfb336` Beutleretal_cov_patchy_z2_SGC_1_15_1_15_1_10_2048_60.dat
  - `d5f14088f46e3229c0f114a5c871f516f1ef339f74b182562a7e9f84ede94e8f` Beutleretal_cov_patchy_z3_NGC_1_15_1_15_1_10_2045_60.dat
  - `0513aadfa749bf744439f226bb8eecc91c3194a73405a68ec409231b930e68e0` Beutleretal_cov_patchy_z3_SGC_1_15_1_15_1_10_2048_60.dat
  - `6254eed8e4a8671dcbcedde6f57205cbfd8ee94919840f73dc1c9fd02a6b89bc` Beutleretal_pk_hexadecapole_DR12_NGC_z1_prerecon_120.dat
  - `fd6ce87d65c65d9587d0946fde46abb4d13a4e8b879b0fac4d71ba9771f4b8c9` Beutleretal_pk_hexadecapole_DR12_NGC_z2_prerecon_120.dat
  - `df5d8e51735759fdecd822eec259b5ee4e26ede96720f5e6c9f3364be6d45d1e` Beutleretal_pk_hexadecapole_DR12_NGC_z3_prerecon_120.dat
  - `44a3c8e36f316f85b4c0a401f984d6d44a87bb1bd6b94753a47b747353364d8c` Beutleretal_pk_hexadecapole_DR12_SGC_z1_prerecon_120.dat
  - `5691a0a9fc3eb966824239c7b40e5385b86496a5246774c7004082e933a31c56` Beutleretal_pk_hexadecapole_DR12_SGC_z2_prerecon_120.dat
  - `1088c663d253ae45a532a962988bdc6de02c0779cf9b2393d3ec8f9cdfea0196` Beutleretal_pk_hexadecapole_DR12_SGC_z3_prerecon_120.dat
  - `9c3212045d1f566b037006d0bf009bd4083e19b65cd10912ea048b19572ad085` Beutleretal_pk_monopole_DR12_NGC_z1_prerecon_120.dat
  - `253e381d3d55f34e6c4c90bc2cd683e7421c9f81bf5b3b2140adb5da60a7fc87` Beutleretal_pk_monopole_DR12_NGC_z2_prerecon_120.dat
  - `4eb6697014bfe3eb386a125b38397a58be4296c3b512c20d18501684176139e0` Beutleretal_pk_monopole_DR12_NGC_z3_prerecon_120.dat
  - `a928fd177acc877f678067b02b95ebc11393559c8573aef5f11dac9f7c845305` Beutleretal_pk_monopole_DR12_SGC_z1_prerecon_120.dat
  - `58a5f7387a6980169c0e7f87ee6742a4aeb3fa374d12107ab4873e0df333bcfd` Beutleretal_pk_monopole_DR12_SGC_z2_prerecon_120.dat
  - `aea626b17952dc7eb58633399951b46490b6c5ec8abd6c33cf6bfabe0a64f269` Beutleretal_pk_monopole_DR12_SGC_z3_prerecon_120.dat
  - `8d8f70a587f947601b4ef310fe8aef9a779bdc57b69506b2dfa3f6babdf3836a` Beutleretal_pk_quadrupole_DR12_NGC_z1_prerecon_120.dat
  - `1d32ebcbf6a4a5b519222130c28298da0fc6a13adfdc92aaa30499ac57d9dd82` Beutleretal_pk_quadrupole_DR12_NGC_z2_prerecon_120.dat
  - `42a768ba38af0159c7e356f202a03a356cbbf8b736bacdea1f5c20f37c197bef` Beutleretal_pk_quadrupole_DR12_NGC_z3_prerecon_120.dat
  - `feab0f16f22fbfdcb36387f3acabb5c12a00ca9b651d8992f6ed63acba671570` Beutleretal_pk_quadrupole_DR12_SGC_z1_prerecon_120.dat
  - `5067baa22279b813e5d610af031fd710ab3e9d637e9c12c15e6f4b80cbf400f1` Beutleretal_pk_quadrupole_DR12_SGC_z2_prerecon_120.dat
  - `fc4db482d8e14e786554afe5aea3038def7f219ba32cf5443086f27594878e2e` Beutleretal_pk_quadrupole_DR12_SGC_z3_prerecon_120.dat
  - `396a3d8c5f86cde2647c765c48eea580c65babb992e9acaca9b445527493ee51` Beutleretal_window_z1_NGC.dat
  - `6105eb74e7bb0ca002a0a5209b2df6d0c2a8f17e211f5e7b96223ed8dc691917` Beutleretal_window_z1_SGC.dat
  - `94c98856d60fb6ae71757bd47f64e799fa1bdc5a207a24754e9141efae7df27d` Beutleretal_window_z2_NGC.dat
  - `fb949ab254d41d203ddd97de9be128ed55bbc2a44258198bebaea1be144f2729` Beutleretal_window_z2_SGC.dat
  - `8704b095421aad847b0a816e2bd013717ad6dc9af7c8df8183978a1fa9a8832f` Beutleretal_window_z3_NGC.dat
  - `ce4d571c58845e02b0b46d740848bae065527c3b348963f2b0f896cf5e61da6a` Beutleretal_window_z3_SGC.dat
  - (falta `Beutler_etal_DR12COMBINED_fullshape_powspec.tar.gz`, el .tar.gz original, NO
    es dependencia directa de ningún stage, es el contenedor del que salió la carpeta)

---

## Grupo: desi_dr2_official — Clase A

**DESI DR2 BAO — cadenas cosmológicas oficiales (cobaya), Zenodo**

- DOI exacto, encontrado en `main.bbl` del paper cacheado (`paper_2503.14738/main.bbl`,
  cita `DR2KPZenodo`): **10.5281/zenodo.16644577** — "DESI DR2 Results II: Supplementary data"
- Paper: DESI Collaboration, "DESI DR2 Results II: Measurements of Baryon Acoustic
  Oscillations and Cosmological Constraints", arXiv:2503.14738, PRD 112, 083515 (2025)
- Las 24 rutas de `chain.1..4.txt` en `dvc.yaml` (6 combinaciones de datasets ×4 cadenas)
  están dentro de `cosmology_chains/cobaya/base_w_wa/...zip` del Zenodo anterior,
  descomprimido localmente en `/mnt/datos/SSEE_data/desi_dr2_official/cosmology_chains/cobaya/`
- NO se calculó sha256 de las 24 cadenas (cada una son varios cientos de MB de MCMC; el
  total del grupo es 2.8 GB) — quedan identificadas por nombre de combinación (son
  verificables contra el Zenodo, formato legible por `getdist`, documentado en
  `dr2-bao-zenodo/Readme.md`, ya presente localmente)
- BAO likelihoods de Cobaya: https://github.com/CobayaSampler/bao_data (mencionado en
  el propio paper como mecanismo de instalación, no está pineado a un commit en el repo)

---

## Grupo: cmb_lensing — mixto

### A. ACT DR6 lensing — YA en manifiesto T2 (bandpowers). Lo que falta:
- `/mnt/datos/SSEE_data/cmb_lensing/papers/2304.05202/main.tex` → Clase **C**,
  arXiv:2304.05202 (Qu et al. 2024, ACT DR6 lensing power spectrum)
- `/mnt/datos/SSEE_data/cmb_lensing/papers/2608.31136/sec8_summary.tex` → Clase **C**,
  arXiv:2608.31136 (del nombre de archivo, validación/inferencia de un lensing map;
  no se abrió el contenido completo, sólo se confirmó que es .tex de paper cacheado,
  carpeta con `src.tgz` + secciones separadas, patrón típico de e-print)

### A. SPT-3G D1 KK bandpowers — YA en manifiesto T2. Lo que falta son los CONFIGS
del mismo repo (no son datos nuevos, son YAMLs de cobaya del propio repo):
- `cmb_lensing/spt3g/spt_candl_data` es un fork git con remoto
  `https://github.com/SouthPoleTelescope/spt_candl_data.git`, commit local
  `efe35b7bfd815a115d5123e210a6849a4175bc81` ("compatibility", autor yomori)
- `cmb_lensing/spt3g/cobaya/SPT3G_D1_KK/base_lens/gmv.yaml`
  sha256 `7fbbc2dbfe5df3e0e857c9a47773906a55c4a871b4fd3e1ee16c2f41006c48d8`
- `cmb_lensing/spt3g/cobaya/SPT3G_D1_KK/configs/likelihoods/lens/nocmb/gmv.yaml`
  sha256 `35f72bb7166f101257f615989b37a0205e788d8bdc0f34a6cdd86f803141d1d3`
- Cita: Omori et al. 2026 (ya anotada en manifiesto T2 para el bandpower hermano)

### B. Cadenas de calibración propias (NO son dato externo — son nuestras corridas
cobaya para verificar que reproducimos el ΛCDM publicado antes de meter SSEE):
- `cmb_lensing/act_dr6_calibrador/act_lcdm.{1..4}.txt` — generadas por
  `src/p11_sondas/act_dr6_calibra.py` (`corre`), salida en
  `results/logs/act_dr6_calibrador.json`. Tamaño del grupo completo: 4.2 MB.
- `cmb_lensing/spt3g_calibrador/spt_lcdm.{1..4}.txt` — mismo patrón, generador análogo
  para SPT-3G (`src/p11_sondas/` tiene script hermano, no identificado por nombre exacto
  en esta pasada, pero el patrón de archivos — `.progress`, `.covmat`, `.checkpoint`,
  `corre.log` — es idéntico a act_dr6_calibra.py). Tamaño: 14 MB.
- **Decisión recomendada:** regenerar, no subir a Zenodo — son outputs chicos (<20 MB)
  y reproducibles con las verosimilitudes oficiales ya citadas arriba.

---

## Grupo: kids1000 — Clase A

**KiDS-1000 cosmic shear data release** (Asgari et al. 2021, A&A 645, A104,
arXiv:2007.15633, "KiDS-1000 cosmology: Cosmic shear constraints and comparison
between two point statistics")

- Página oficial: https://kids.strw.leidenuniv.nl/ (releases bajo la sección DR4;
  no se confirmó la URL exacta del .tar/.zip de descarga en esta pasada — requiere
  navegar el portal, que no es accesible por API simple)
- Ruta local: `/mnt/datos/SSEE_data/kids1000/KiDS1000_cosmis_shear_data_release/`
  (365 MB totales, incluye `kcap` = pipeline CosmoSIS, que es código no dato)
- Archivos que SÍ son dependencia directa de dvc.yaml:
  - `data_fits/xipm_KIDS1000_BlindC_..._Fid.fits` (608 KB)
    sha256 `466d1d761fedac02e53b5468cdbab20f622c2f04b830085cccdae5b629ebe66c`
  - `chains_and_config_files/main_chains_iterative_covariance/xipm/chain/maxpost_multinest_start_C.txt`
    (cadena MultiNest oficial de la colaboración — NO calculado sha256, cadena grande)
  - `kcap/runs/3x2pt/data_iterated_cov/.../SOM_cov_multiplied.asc` (parte del pipeline
    kcap, covarianza SOM; es dato auxiliar del repo oficial `KiDS-WL/kcap`, no un
    producto nuestro)
- Adicional (no dependencia dvc, pero vive en la misma carpeta y es útil anotar):
  `data_fits/bp_KIDS1000..._Fid.fits` sha256 `e6d60d3b93bcb30a2f850c90651527dcee32a3a2e7f6e4bbe21b18b1cb7ed2b7`,
  `data_fits/cosebis_KIDS1000..._Fid.fits` sha256 `a10bfb74664ff484aec4287e2e915d32cf2380a746e55e6bcf869361c80179c9`

---

## Grupo: kids_legacy — Clase A

**KiDS-Legacy cosmic shear data release** (Wright et al. 2025, A&A 703, A158,
arXiv:2503.19441 et al. — serie completa citada en el README.txt del propio release:
Wright 2025 A&A 686 A170, Wright 2025 A&A 703 A158, Stölzner 2025 A&A 702 A169,
Reischke 2025 A&A 699 A124, Wright 2025 A&A 703 A144)

- Página oficial: https://kids.strw.leidenuniv.nl/DR5/legacy_wl.php
- Ruta local: `/mnt/datos/SSEE_data/kids_legacy/KiDS_Legacy_cosmic_shear_data_release/`
  (394 MB)
- `data/KiDS_Legacy_xipm.fits` (1.2 MB) sha256
  `aeedfec802c83f468a7459b11be7b9978029fd87985c9e3930cd3d8be38a664d`
- `chains_and_config_files/xipm/output_nautilus_xipm_Fiducial.txt` (101 MB, cadena
  Nautilus fiducial de la colaboración — no se calculó sha256 por tamaño, pero es un
  solo archivo, perfectamente viable si se quiere en una pasada futura)
- El README.txt local (texto completo revisado) exige citar las 5 referencias arriba
  y el acknowledgement ESO (programas 179.A-2004, 177.A-3016/7/8, 298.A-5015)

---

## Grupo: erosita — mixto

### A. Catálogos eROSITA (datos públicos MPE/eSASS)
- `erosita/erass1/erass1cl_cosmology_v1.1.fits` (1.2 MB)
  sha256 `fe2310495ce2fdba5876e248ab3415012d6f2e79280d87c8bfd1177ca11a779e`
- `erosita/erass1/erass1cl_primary_v3.2.fits` (49 MB)
  sha256 `e79c392e2d7b9e26105ead7d56787713465aa853feb040a227891fb9571b9a54`
- `erosita/efeds/eFEDS_clusters_V3.2.fits.gz` (108 KB)
  sha256 `53a2e07f55b3bc8c783fe071d8039c75f5682d04975ff310909abef37612789b`
- Origen: eROSITA Data Release vía MPE (`https://erosita.mpe.mpg.de/`), catálogo
  eRASS1 de cúmulos (Bulbul et al. 2024, A&A 685, A106, arXiv:2402.08452) y catálogo
  eFEDS (Liu et al. 2022 / Bahar et al. 2022, con `ReadMe_Bahar2022.txt` y tablas CDS
  ya presentes localmente en `erosita/efeds/`, lo que confirma que el origen real es
  el VizieR/CDS de esos papers, no sólo el portal MPE)
- `erosita/Ghirardini2024_abstract.txt` y `erosita/efeds/Liu2022_abstract.txt` →
  Clase **C** (abstracts cacheados, no datos) — arXiv de Ghirardini et al. 2024 es
  2402.08452-adjacent (el archivo `paper_ghirardini2024/48852corr.tex` es el manuscrito
  completo A&A, probablemente el mismo arXiv:2402.08452 o un companion)

### C. Literatura cacheada (sólo citar arXiv, no redistribuir)
- `erosita/paper_2602.20483/AA_final.tex` → arXiv:2602.20483
- `erosita/paper_ghirardini2024/48852corr.tex` → manuscrito Ghirardini et al. 2024

---

## Grupo: literatura — Clase C (sólo arXiv id, sin redistribución)

De los `.tex` referenciados directamente por `dvc.yaml`:
- 1807.06209 (Planck 2018 — Planck Collaboration, "Planck 2018 results. VI. Cosmological parameters")
- h0_metodos/1710.05835
- h0_metodos/2001.09213
- h0_metodos/2101.02221
- h0_metodos/2112.04510 (shoes6.tex — SH0ES, Riess et al.)
- h0_metodos/2408.06153 (Ho2024.tex — CCHP, Freedman/Ho 2024/2025)
- h0_metodos/2408.11770
- h0_metodos/2506.03023
- sn_ia/papers/2202.04077 (Scolnic et al., Pantheon+)

(2111.03604 existe en el árbol local de `h0_metodos/` pero NO aparece en la lista de
dependencias absolutas de `dvc.yaml` extraída al inicio — no se incluye como hallazgo,
sólo se anota que la carpeta local tiene un .tex adicional no referenciado por ningún stage.)

No se descarga nada de este grupo: son e-prints de arXiv cacheados únicamente para
verificación manual de citas; el patrón ya establecido en el proyecto (ver
`data/raw/FUENTES.yaml`) es anotar "arXiv id + fecha de bajada", no redistribuir el .tex.

---

## Grupo: cobaya_packages — Clase A

**Planck 2018 — datos oficiales de verosimilitud, vía `cobaya-install`**

- `/home/mike/cobaya_packages/data/planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/lkl_0/_external/cl_cmb_plik_v22.dat`
  (48 KB) sha256 `dac0d9d493213e77c940a10a968cf0da3c5730bae60e1356c4cd8bcff96377ff`
- `/home/mike/cobaya_packages/data/planck_supp_data_and_covmats/lensing/2018/smicadx12_Dec5_ftl_mv2_ndclpp_p_teb_agr2_bandpowers.dat`
  (12 KB) sha256 `022ecd45a4dc0d8ea42643b084811e5ff295040cbc3fead7d4e7ecf6c0c2254e`
- Mecanismo de obtención oficial: `cobaya-install planck_2018_highl_plik.TTTEEE_lite_native
  planck_2018_lensing.native --packages-path /home/mike/cobaya_packages` (o el paquete
  equivalente que instale `plc_3.0`); Cobaya descarga esto de los servidores del PLA
  (Planck Legacy Archive) de forma automática. El `COBAYA_PACKAGES_PATH` que usa el
  repo NO está documentado en ningún README/AUDIT.md, como ya señala REPRO.md §3.
- Esta ruta depende de que `/home/mike` sea el usuario — es la causa raíz H4 que ya
  documenta REPRO.md (rutas no parametrizadas).

---

## Grupo: hi_class — Clase A (software, no dato)

- `/mnt/datos/hi_class/class` — binario compilado de un fork git de CLASS/hi_class
- `/mnt/datos/hi_class` es un repo git real:
  - remoto: `https://github.com/miguelzuma/hi_class_public.git`
  - commit local: `0009f51d89e6465c79e570b496c66fc90058fa77`
    ("Split the release news item's last clause into its own sentence")
- Reproducción: clonar ese remoto, `git checkout 0009f51d8`, compilar con
  `make class` (requiere gfortran si se activa classy, lapack para algunos módulos;
  el repo local ya tiene `build/` con artefactos de compilación)
- No se calculó sha256 del binario (es compilado localmente, el sha256 de un binario
  no es portable entre arquitecturas; lo verificable es el commit del fork)

---

## Grupo: chains_p6 — Clase B (producto propio)

Cadenas Cobaya de Paper 6 (crecimiento de estructura), generadas y leídas por los
scripts en `src/p06_growth/` (`multisonda_fondo_clavado.py`, `leer_conjunta.py`,
`cobaya_kids_legacy.py`, `cobaya_boss_chen21.py`, `analiza_boss_chen21.py`, entre otros; las cadenas de `boss/` y `conjunta/` son del BOSS de 2017, retirado el 2026-10-20).

- Tamaño total: **440 MB**
- Subgrupos: `boss/` (lcdm+ssee ×4), `kids/` (lcdm+ssee ×4 + progress/updated.yaml),
  `kids_legacy/` (lcdm fijo + ssee + ssee fijo ×4 cada uno), `conjunta/`
  (conjunta, conjunta_b3, boss_clavado ×4 cada uno)
- **Decisión recomendada:** no redistribuir en Zenodo como blob; son regenerables
  corriendo los scripts citados contra los datos externos ya manifestados (KiDS,
  KiDS-Legacy, BOSS DR12) — 440 MB es manejable si Mike decide subirlas igual como
  dataset complementario, pero no es necesario para que un tercero reproduzca,
  sólo para ahorrarle el tiempo de cómputo MCMC.

---

## Grupo: mcmc — Clase B (producto propio, con resaca de corridas superadas)

Generado principalmente por `src/mcmc_full/lanzar_mcmc_full.sh` +
`src/mcmc_full/ssee_full.yaml` (lee `src/mcmc_full/leer_mcmc_full.py`), más scripts de
`src/p02_mcmc/` para las figuras de degeneración w0-wa.

- **Tamaño total: 26 GB**, desglose relevante:
  - `paper2_3models/` — 8.6 GB (dependencia directa: `mcmc_chains_professional.npz`)
  - `superseded_om160/` — 7.5 GB — **marcado "superseded" por el propio nombre de
    carpeta**; no debería tener dependencias vivas en dvc.yaml (verificado: ninguna
    ruta de `superseded_om160` aparece en la lista de 112 deps absolutas)
  - `chains_DR1_superseded/` — 7.4 GB — mismo caso, nombre auto-declarado superado,
    sin dependencias vivas en dvc.yaml
  - `paper2_reframe/` — 2.0 GB (no aparece como dependencia directa tampoco, pero es
    más reciente — podría ser output intermedio de una etapa, no confirmado)
  - `mcmc_full/` (las 4 cadenas `ssee_full.{1..4}.txt`, dependencia directa) — 34 MB
  - `grid_class/` — 215 MB (grilla de emulador, no confirmado si es dependencia viva)
- Dependencias directas de dvc.yaml en este grupo: las 4 cadenas de `mcmc_full/c{1..4}/`
  (34 MB total) + `paper2_3models/mcmc_chains_professional.npz` (tamaño no desglosado
  aparte, dentro de los 8.6 GB del directorio)
- **Hallazgo a reportar a Mike:** 14.9 GB de los 26 GB (`superseded_om160` +
  `chains_DR1_superseded`) son corridas YA declaradas superadas por su propio nombre
  y no tienen ninguna dependencia viva en `dvc.yaml` — son candidatas a archivar fuera
  del HDD de trabajo o borrar, no a documentar en el manifiesto de reproducibilidad
  (siguiendo la regla de `feedback_archivo_declarado_y_clasificar_logs`: ya tienen
  nota del porqué en el nombre, sólo falta decidir si se archivan).
- **Decisión recomendada para lo vivo:** no subir los 8.6 GB+34 MB a Zenodo como blob;
  regenerable vía `lanzar_mcmc_full.sh` contra Planck 2018 + DESI DR2 (ya manifestados).

---

## Grupo: sn_ia — residual (lo nuevo no cubierto por manifiesto T2)

- `papers/2202.04077/main.tex` → Clase **C**, ya listado arriba en "literatura"
  (Scolnic et al. 2022, Pantheon+)
- `union3/pipeline/data_release/union31_unity18_binned_mu/mu_mat.fits` → Clase **A**,
  es el release original de `rubind/union3_release` (mismo repo ya citado en
  manifiesto T2 para `mu_mat_union3_cosmo=2_mu.fits`; esta ruta es la copia dentro de
  la estructura `pipeline/data_release/` del propio repo clonado)
- `union3/runs/union31_repro/mu_mat.fits` → Clase **B**, es NUESTRA reproducción
  (carpeta `runs/`, contiene además `mcmc_samples.parquet` de 9 MB) — generada por
  `src/p11_sondas/union3_repro_compara.py` o `read_and_sample.py` (ambos en el repo
  original clonado, no en `src/` de SSEE — requiere verificar cuál de los dos stan/
  read scripts del repo union3 clonado se usó, no confirmado en esta pasada)

---

## Bloque JSON para fusionar con `data/manifiesto_descargas_T2.json`

Sólo se incluyen entradas Clase A con sha256 calculado (archivos pequeños/medianos
verificados en esta pasada). Las cadenas grandes, los directorios completos y los
productos propios (B) y literatura (C) quedan documentados en prosa arriba, no en
este bloque, siguiendo el esquema `ficheros` ya usado por T2 (campos: grupo, nombre,
ruta, bytes, sha256, origen, nota).

```json
{
  "ficheros_nuevos_cuarta_lectura": [
    {
      "grupo": "boss_dr12",
      "nombre": "BOSS DR12 full-shape+RSD, Beutler et al. 2017 (31 archivos)",
      "ruta": "/mnt/datos/SSEE_data/boss_dr12/public_material_RSD/",
      "bytes": 4800000,
      "sha256_por_archivo": "ver seccion boss_dr12 de MANIFIESTO_EXTERNOS.md (31 entradas)",
      "origen": "https://data.sdss.org/sas/dr12/boss/papers/clustering/",
      "nota": "Beutler et al. 2017, MNRAS 466, 2242 (arXiv:1607.03149). Usado por src/p06_growth/boss_dr12_data.py"
    },
    {
      "grupo": "desi_dr2_official",
      "nombre": "DESI DR2 Results II: Supplementary data (cosmology_chains/cobaya)",
      "ruta": "/mnt/datos/SSEE_data/desi_dr2_official/cosmology_chains/cobaya/",
      "bytes": 2800000000,
      "sha256": null,
      "origen": "https://doi.org/10.5281/zenodo.16644577",
      "nota": "DESI Collaboration, arXiv:2503.14738, PRD 112, 083515. DOI confirmado en main.bbl cacheado localmente (cita DR2KPZenodo). 24 cadenas usadas como deps directas de dvc.yaml bajo base_w_wa/; sha256 no calculado por tamaño (2.8 GB total)"
    },
    {
      "grupo": "cmb_lensing",
      "nombre": "SPT-3G D1 KK — configs cobaya (gmv.yaml x2)",
      "ruta": "/mnt/datos/SSEE_data/cmb_lensing/spt3g/cobaya/SPT3G_D1_KK/",
      "bytes": 8000,
      "sha256_base_lens_gmv_yaml": "7fbbc2dbfe5df3e0e857c9a47773906a55c4a871b4fd3e1ee16c2f41006c48d8",
      "sha256_nocmb_gmv_yaml": "35f72bb7166f101257f615989b37a0205e788d8bdc0f34a6cdd86f803141d1d3",
      "origen": "https://github.com/SouthPoleTelescope/spt_candl_data.git",
      "nota": "commit local efe35b7bfd815a115d5123e210a6849a4175bc81. Mismo repo que el bandpower SPT3G_D1_KK_GMV_bdp.txt ya en manifiesto T2"
    },
    {
      "grupo": "kids1000",
      "nombre": "KiDS-1000 cosmic shear data release — xipm Fid",
      "ruta": "/mnt/datos/SSEE_data/kids1000/KiDS1000_cosmis_shear_data_release/data_fits/xipm_KIDS1000_BlindC_with_m_bias_V1.0.0A_ugriZYJHKs_photoz_SG_mask_LF_svn_309c_2Dbins_v2_goldclasses_Flag_SOM_Fid.fits",
      "bytes": 622592,
      "sha256": "466d1d761fedac02e53b5468cdbab20f622c2f04b830085cccdae5b629ebe66c",
      "origen": "https://kids.strw.leidenuniv.nl/ (portal DR4; URL exacta del paquete descargable no confirmada en esta pasada)",
      "nota": "Asgari et al. 2021, A&A 645, A104 (arXiv:2007.15633)"
    },
    {
      "grupo": "kids_legacy",
      "nombre": "KiDS-Legacy cosmic shear data release — xipm",
      "ruta": "/mnt/datos/SSEE_data/kids_legacy/KiDS_Legacy_cosmic_shear_data_release/data/KiDS_Legacy_xipm.fits",
      "bytes": 1258291,
      "sha256": "aeedfec802c83f468a7459b11be7b9978029fd87985c9e3930cd3d8be38a664d",
      "origen": "https://kids.strw.leidenuniv.nl/DR5/legacy_wl.php",
      "nota": "Wright et al. 2025, A&A 703, A158 (serie completa en README.txt local, 5 papers)"
    },
    {
      "grupo": "erosita",
      "nombre": "eRASS1 cluster cosmology catalog v1.1",
      "ruta": "/mnt/datos/SSEE_data/erosita/erass1/erass1cl_cosmology_v1.1.fits",
      "bytes": 1200000,
      "sha256": "fe2310495ce2fdba5876e248ab3415012d6f2e79280d87c8bfd1177ca11a779e",
      "origen": "https://erosita.mpe.mpg.de/ (eRASS1 data release)",
      "nota": "Bulbul et al. 2024, A&A 685, A106 (arXiv:2402.08452)"
    },
    {
      "grupo": "erosita",
      "nombre": "eRASS1 cluster primary catalog v3.2",
      "ruta": "/mnt/datos/SSEE_data/erosita/erass1/erass1cl_primary_v3.2.fits",
      "bytes": 49000000,
      "sha256": "e79c392e2d7b9e26105ead7d56787713465aa853feb040a227891fb9571b9a54",
      "origen": "https://erosita.mpe.mpg.de/ (eRASS1 data release)",
      "nota": "Bulbul et al. 2024, A&A 685, A106 (arXiv:2402.08452)"
    },
    {
      "grupo": "erosita",
      "nombre": "eFEDS cluster catalog V3.2",
      "ruta": "/mnt/datos/SSEE_data/erosita/efeds/eFEDS_clusters_V3.2.fits.gz",
      "bytes": 110592,
      "sha256": "53a2e07f55b3bc8c783fe071d8039c75f5682d04975ff310909abef37612789b",
      "origen": "CDS/VizieR (confirmado por ReadMe_Bahar2022.txt local, mismo directorio)",
      "nota": "Liu et al. 2022 / Bahar et al. 2022, eFEDS cluster catalog"
    },
    {
      "grupo": "cobaya_packages",
      "nombre": "Planck 2018 plik_lite TTTEEE native",
      "ruta": "/home/mike/cobaya_packages/data/planck_2018/baseline/plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik/clik/lkl_0/_external/cl_cmb_plik_v22.dat",
      "bytes": 49152,
      "sha256": "dac0d9d493213e77c940a10a968cf0da3c5730bae60e1356c4cd8bcff96377ff",
      "origen": "cobaya-install planck_2018_highl_plik.TTTEEE_lite_native --packages-path <COBAYA_PACKAGES_PATH>",
      "nota": "Planck Legacy Archive, via Cobaya. Ruta depende de usuario /home/mike, ya senalado en REPRO.md H4"
    },
    {
      "grupo": "cobaya_packages",
      "nombre": "Planck 2018 lensing SMICA bandpowers",
      "ruta": "/home/mike/cobaya_packages/data/planck_supp_data_and_covmats/lensing/2018/smicadx12_Dec5_ftl_mv2_ndclpp_p_teb_agr2_bandpowers.dat",
      "bytes": 12288,
      "sha256": "022ecd45a4dc0d8ea42643b084811e5ff295040cbc3fead7d4e7ecf6c0c2254e",
      "origen": "cobaya-install planck_2018_lensing.native --packages-path <COBAYA_PACKAGES_PATH>",
      "nota": "Planck Legacy Archive, via Cobaya"
    },
    {
      "grupo": "hi_class",
      "nombre": "hi_class fork (binario class compilado)",
      "ruta": "/mnt/datos/hi_class/class",
      "bytes": null,
      "sha256": null,
      "origen": "https://github.com/miguelzuma/hi_class_public.git",
      "nota": "software, no dato. commit local 0009f51d89e6465c79e570b496c66fc90058fa77. Reproducir con git clone + checkout + make"
    }
  ]
}
```

---

## Resumen (ver también mensaje final al llamador)

Grupos sin fuente pública identificable con certeza en esta pasada:
- **mcmc** (26 GB, de los cuales 14.9 GB ya están auto-marcados "superseded" sin deps
  vivas) — es 100% producto propio, no requiere fuente externa, pero requiere decisión
  de archivado.
- **chains_p6** (440 MB) y las cadenas calibrador de **cmb_lensing** — producto propio,
  regenerable.
- La URL exacta de descarga de **kids1000** (más allá del portal general) no se
  confirmó en esta pasada — requeriría navegar `kids.strw.leidenuniv.nl` manualmente.
