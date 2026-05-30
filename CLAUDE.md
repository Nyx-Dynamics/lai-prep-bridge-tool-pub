# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Summary

LAI-PrEP Bridge Period Decision Support Tool — a clinical decision support system for assessing bridge period success probability during Long-Acting Injectable HIV Prevention (the critical 2-8 week gap between LAI-PrEP prescription and first injection). Published research; companion paper in *Viruses* 2026.

## Setup

```bash
pip install -r "Project Docs/requirements.txt"
pip install -r "Project Docs/requirements-dev.txt"
```

No `setup.py` or `pyproject.toml` — this is a pure Python project with a JSON-driven configuration.

## Running Tests

```bash
# Run test_edge_cases.py + config validation (run from SCR/ directory)
cd SCR && python code/tests/run_tests.py --all

# Run quietly
cd SCR && python code/tests/run_tests.py --quiet
```

Standalone simulation scripts (run directly from SCR/, not via run_tests.py):
```bash
cd SCR && python code/tests/test_suite.py            # unit tests (1K patients)
cd SCR && python code/tests/test_suite_2.py          # 1M patient validation
cd SCR && python code/tests/test_suite_3.py          # 10M streaming validation
cd SCR && python code/tests/test_suite_4.py          # 21.2M UNAIDS-scale validation
```

`test_suite_4.py` results will differ from the published `validation_UNAIDS_21.2M_results.json` — the v1 API included a `SEX_WORKER` population removed in v2.1, changing regional weight distributions. The published JSON is the v1 validation artifact; the script now establishes the v2.1 baseline.

## CLI Usage

```bash
# Run from repo root
python SCR/code/cli/cli.py --help
python SCR/code/cli/cli.py assess --input patient.json --output result.json
python SCR/code/cli/cli.py batch --input patients.csv --output results.json
python SCR/code/cli/cli.py validate --config SCR/lai_prep_config.json
python SCR/code/cli/cli.py template
```

## Architecture

The tool has three layers connected by a shared JSON config:

**Configuration** (`SCR/lai_prep_config.json`): Single source of truth (v2.1.0). Defines the 7 supported populations with baseline attrition rates, 13 structural barriers with impact weights, 21 evidence-based interventions with mechanism tags, 8 healthcare setting types, and the algorithm's model coefficients. All clinical parameters live here — never hardcoded in the algorithm.

**Core Engine** (`SCR/code/algorithm/lai_prep_decision_tool_v2_1.py`): `LAIPrEPDecisionTool` takes a `PatientProfile` dataclass and runs four sequential calculations:
1. Baseline success rate — from population + age adjustment
2. Adjusted success rate — baseline modified by active barriers
3. Intervention recommendations — 21 interventions ranked by population-specific effectiveness, with a mechanism diversity penalty to avoid recommending redundant approaches
4. Outcome with interventions — estimated success rate improvement

Supports two calculation methods: linear (default, `use_logit=False`) and logit-space (more mathematically sound, `use_logit=True`). Returns `BridgePeriodAssessment` with both human-readable report (`.generate_report()`) and JSON export (`.to_json()`).

**CLI** (`SCR/code/cli/cli.py`): Click-based wrapper over the engine. The CLI adds `SCR/code/algorithm/` to `sys.path` at startup so it can be invoked from any working directory.

## Test Organization

`SCR/code/tests/run_tests.py` runs `test_edge_cases.py` (18 tests) via pytest and optionally `validate_config.py` with `--all`. A `conftest.py` in the same directory adds the algorithm to `sys.path` so pytest finds it automatically.

- `test_edge_cases.py` — **runnable**, 18 pytest tests (boundary conditions, error handling)
- `test_suite.py` — **runnable**, standalone unit tests (oral PrEP, barriers, populations, 1K patients)
- `test_suite_2.py` — **runnable**, standalone 1M patient large-scale validation
- `test_suite_3.py` — **runnable**, standalone 10M patient streaming validation
- `test_suite_4.py` — **runnable**, standalone 21.2M UNAIDS-scale validation (see note above)

All five were migrated from a legacy `LAI_DMT_v1` API to the current `lai_prep_decision_tool_v2_1` API during the v2.1.1 housekeeping release (2026-05-30).

## Figure Generation

`SCR/code/fig_gen/` contains independent scripts that generate manuscript figures (MDPI format). Each is standalone — run individually to regenerate figures. Output goes to `SCR/figures/` as PDF (vector) and PNG (600 dpi). The cascade figure is `cascades_revised.py` (the canonical, portable version).

## Key Constraints

- **Working directory matters for the algorithm.** The canonical config is `SCR/lai_prep_config.json`. The algorithm's `_find_config_file()` searches `Path(__file__).parent / "lai_prep_config.json"` first but the config is NOT co-located with the algorithm — it's at `SCR/lai_prep_config.json`. All invocations that don't pass an explicit `config_path` must be run from `SCR/`. The CLI handles this via its own path resolution; `run_tests.py` passes the config path explicitly. See `TODO_config_loading.md` for the deferred robustness fix.
- Population keys are **UPPERCASE_SNAKE_CASE**: `"MSM"`, `"CISGENDER_WOMEN"`, `"TRANSGENDER_WOMEN"`, `"ADOLESCENT"`, `"PWID"`, `"PREGNANT_LACTATING"`, `"GENERAL"`.
- Barrier keys are **UPPERCASE_SNAKE_CASE**: e.g., `"TRANSPORTATION"`, `"CHILDCARE"`, `"INSURANCE_DELAYS"`, `"MEDICAL_MISTRUST"` (13 total — see config for full list).
- Healthcare setting keys are **UPPERCASE_SNAKE_CASE**: e.g., `"COMMUNITY_HEALTH_CENTER"`, `"HARM_REDUCTION"`, `"LGBTQ_CENTER"` (8 total).
- License is MIT with a pharma restriction (`Project Docs/PHARMA_RESTRICTED_LICENSE.md`) — pharmaceutical companies require separate licensing.
- `Project Docs/` holds infrastructure files (requirements, license, CHANGELOG, contributing guides). `docs/` holds dissemination-facing materials (policy briefs, UNAIDS executive summaries).
