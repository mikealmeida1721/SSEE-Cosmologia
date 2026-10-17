# How to audit SSEE

This page is for anyone who wants to check the work rather than read it. Every
number in the papers can be traced to the log that produced it, every log to the
script and commit that wrote it, and every external dataset to its download and
checksum. The steps below go from a two-minute check to a full re-run.

*(Last revised 2026-10-17. The previous audit snapshot, from 2026-05-17, described
a model that has since changed — it is kept in
[`archive/superado/AUDIT_2026-05-17.md`](archive/superado/AUDIT_2026-05-17.md)
for the record, not as current.)*

---

## 1. Install

The pipeline names the paths it ran with (`/mnt/datos/SSEE_data/…`,
`/home/mike/cobaya_packages`), and every log's provenance records them. Rewriting them
would change the scripts and void those records, so instead
[`entorno_ssee.sh`](entorno_ssee.sh) opens a sandbox (bubblewrap, no administrator
rights) where your own folders appear at those paths. Run everything inside it.

```bash
git clone https://github.com/mikealmeida1721/SSEE-Cosmologia.git && cd SSEE-Cosmologia
export SSEE_DATOS=~/ssee/datos COBAYA_PACKAGES_PATH=~/ssee/cobaya SSEE_HICLASS=~/ssee/hi_class
mkdir -p $SSEE_DATOS $COBAYA_PACKAGES_PATH $SSEE_HICLASS
./entorno_ssee.sh bash -c "python3.12 -m venv .venv && .venv/bin/pip install -r requirements-lock.txt"
./entorno_ssee.sh                         # a shell inside the sandbox; the commands below run there
```

[`requirements-lock.txt`](requirements-lock.txt) holds the exact versions that ran the
pipeline (153 packages; `camb` is EFTCAMB at commit 16d9c4e, not the PyPI package);
[`requirements.txt`](requirements.txt) only states minimums. The DES Y3 and eROSITA
stages use their own environments, specified exactly in [`data/entornos/`](data/entornos/)
and in the `entornos` block of the manifest (§5); you need them only to re-run those
stages.

## 2. The algebra (two minutes, no data)

Everything the model fixes comes from φ and π in one file,
[`src/ssee_core.py`](src/ssee_core.py). Its values, with their formulas, are in
[`results/logs/algebra_derivada.json`](results/logs/algebra_derivada.json) and the
human-readable table is [`CANONICAL_VALUES.yaml`](CANONICAL_VALUES.yaml).

```bash
.venv/bin/python3 -c "import sys; sys.path.insert(0,'src'); import ssee_core as c; print(c.W0, c.WA)"
```

## 3. From a number in a paper to its source

Papers do not contain hand-typed results. A result is written as `\val{NAME}`, and
[`manuscript/valores_generados.tex`](manuscript/valores_generados.tex) states, next
to each value, the log and the key it was read from, e.g.

```
\expandafter\def\csname ssee@val@b1_dBIC\endcsname{-33.83}  % results/logs/b1_k2.json#dBIC
```

The list of names and formats is [`manuscript/valores.yaml`](manuscript/valores.yaml);
[`src/valores_tex.py`](src/valores_tex.py) regenerates the file from the logs.

## 4. From a log to the script and commit that wrote it

Every result log carries a `_procedencia` block: commit, script path, script
sha256, input files with their sha256, arguments, host, library versions and
thread counts. To check that a log really came from the script it names, at the
commit it names, with the inputs it names:

```bash
.venv/bin/python3 -c "import sys; sys.path.insert(0,'src'); import procedencia as p; print(p.verifica('results/logs/b1_k2.json'))"
```

The whole chain (data → script → log → `\val` → PDF) is declared as a DVC pipeline
in [`dvc.yaml`](dvc.yaml), with hashes in [`dvc.lock`](dvc.lock):

```bash
dvc status            # which stages are out of date with respect to their inputs
dvc repro -s <stage>  # re-run one stage
```

## 5. External data

[`data/manifiesto_externos.json`](data/manifiesto_externos.json) lists every input the
pipeline reads from outside git — 126 of them: DESI DR2 chains, BOSS DR12, KiDS-1000
and KiDS-Legacy, DES Y3, SPT-3G, ACT DR6, eROSITA, Pantheon+, DES-SN5YR, Union3,
Planck via `cobaya-install`, the arXiv sources whose numbers are transcribed, hi_class,
and the project's own MCMC chains. Each entry carries its origin, citation, the sha256
and size of every file as used here, and a **recipe**.
[`src/verificacion/baja_externos.py`](src/verificacion/baja_externos.py) executes the
recipes and then checks every file against its sha256:

```bash
.venv/bin/python3 src/verificacion/baja_externos.py baja --paquete <SSEE data package>
.venv/bin/python3 src/verificacion/baja_externos.py verifica    # also for data you got yourself
```

Public data come **from their owners** (fixed URLs, git repositories at fixed commits,
arXiv at fixed versions); hi_class is compiled at its commit. What no third party can
provide — the project's own chains, the DES nuisance best fit, the Union3 reproduction,
the exact dictionary copy, two quoted arXiv abstracts and one catalogue page — is the
SSEE data package on Zenodo (176 files, 336 MB, built deterministically by
[`empaqueta_datos_propios.py`](src/verificacion/empaqueta_datos_propios.py)). The
manifest is regenerated by
[`src/verificacion/manifiesto_externos.py`](src/verificacion/manifiesto_externos.py),
which fails if any input lacks an origin or a recipe. The Planck spectra in `data/raw/`
are checked byte-for-byte against the official release by
[`src/verificacion/coteja_crudos.py`](src/verificacion/coteja_crudos.py).

**Tested (2026-10-17)** from a fresh clone with empty folders: 252 of 252 files
identical, `dvc status` up to date, and two stages re-run from scratch give the same
numbers. The downloads took 2 h 44 min, 2 h 40 min of it the 1.3 GB DESI file on Zenodo.

## 6. The guardian

[`src/verificacion/ssee_verify.py`](src/verificacion/ssee_verify.py) runs several
hundred checks over the code, the logs and the LaTeX sources: algebraic identities to
machine precision, consistency of each value across papers, provenance of every log,
and a layer of rules that fail if a retracted number or concept reappears as
current. Each rule is tested against the commit before the fix it guards (it must
fire there). Its own self-tests and a mutation suite (injected defects that it must
catch) are [`test_guardian.py`](src/verificacion/test_guardian.py) and
[`mutacion_guardian.py`](src/verificacion/mutacion_guardian.py) — the mutation suite
edits files and takes several minutes; do not interrupt it.

```bash
.venv/bin/python3 src/verificacion/ssee_verify.py
```

Without the external inputs of §5, the provenance layers (R65, R74, R75) report the
missing files and the run ends red: that is the guardian refusing to vouch for logs
whose inputs it cannot see, not a defect of the logs. With them in place, it runs in
full. Everything that depends only on the repository — the algebra, the cross-paper
consistency of every value, and the retracted-claim rules — runs either way. The
guardian's messages are in Spanish.

## 7. Re-running the main results

| Result | Command | Log |
|---|---|---|
| CMB, full Planck `plik`, ΔBIC k=2 vs k=6 | `python src/p03_cmb/b1_minimiza.py` | `results/logs/b1_k2.json` |
| DESI DR2 BAO with both backgrounds fixed | see stage in `dvc.yaml` | `results/logs/bao_lcdm_libre.json` |
| Each probe, background fixed in advance | `dvc repro -s sondas_ssee_vs_lcdm` | `results/logs/sondas_ssee_vs_lcdm.json` |
| S₈ vs raw KiDS-Legacy, A_s fixed to the CMB | see stages in `dvc.yaml` | `results/logs/kids_legacy_bic.json`, `kids_publicados.json` |
| fσ₈ vs raw BOSS DR12 multipoles | see stages in `dvc.yaml` | `results/logs/growth_2026-07/R1R2_boss_lpt_cobaya.json` |
| Paper 2 MCMC (DESI + prior H_glob) | `python src/p02_mcmc/ssee_paper2_mcmc.py` | `results/logs/mcmc_paper2_reframe.json` |

`dvc.yaml` is the authoritative list: every stage gives the exact command,
its inputs and its outputs.

## 8. What has been withdrawn, and what is open

- [`RETRACTIONS.md`](RETRACTIONS.md) / [`RETRACCIONES.yaml`](RETRACCIONES.yaml):
  every retracted claim, why, and what replaced it (e.g. the second dark-matter
  sector and its particle; the reverse H₀ cascade; the "Planck PR4" label of the
  PR3 spectra).
- [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md): physics that is not derived, with status.
- [`VERIFICATION_LEDGER.md`](VERIFICATION_LEDGER.md): the canonical value of each
  quantity and how it was verified.
- [`EXTERNAL_AUDIT_PROMPTS.md`](EXTERNAL_AUDIT_PROMPTS.md) (internal, in Spanish):
  the prompts used for independent hostile reviews of the papers and of the repository.

If you find a number you cannot trace, or a check that does not reproduce, please
open an issue: that is exactly what this page is for.
