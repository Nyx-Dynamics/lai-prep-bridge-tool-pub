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
# Run test_edge_cases.py + config validation (the only functional tests)
python SCR/code/tests/run_tests.py --all

# Run quietly
python SCR/code/tests/run_tests.py --quiet

# Run test_edge_cases.py directly (requires algorithm on path)
cd SCR/code/tests && PYTHONPATH=../algorithm pytest test_edge_cases.py -v
```

Note: `test_suite.py`, `test_suite_2.py`, `test_suite_3.py`, and `test_suite_4.py` all import a legacy `LAI_DMT_v1` module that no longer exists — they cannot be run until ported to import `lai_prep_decision_tool_v2_1`.

## CLI Usage

```bash
python SCR/code/cli/cli.py --help
python SCR/code/cli/cli.py assess --input patient.json --output result.json
python SCR/code/cli/cli.py batch --input patients.csv --output results.json
python SCR/code/cli/cli.py validate
python SCR/code/cli/cli.py template
```

## Architecture

The tool has three layers connected by a shared JSON config:

**Configuration** (`SCR/lai_prep_config.json`): Single source of truth (v2.1.0). Defines the 7 supported populations with baseline attrition rates, 13 structural barriers with impact weights, 21 evidence-based interventions with mechanism tags, 8 healthcare setting types, and the algorithm's model coefficients. All clinical parameters live here — never hardcoded in the algorithm. `SCR/lai_prep_config_FIXED.json` is an outdated v2.0.0 copy — do not use it.

**Core Engine** (`SCR/code/algorithm/lai_prep_decision_tool_v2_1.py`): `LAIPrEPDecisionTool` takes a `PatientProfile` dataclass and runs four sequential calculations:
1. Baseline success rate — from population + age adjustment
2. Adjusted success rate — baseline modified by active barriers
3. Intervention recommendations — 21 interventions ranked by population-specific effectiveness, with a mechanism diversity penalty to avoid recommending redundant approaches
4. Outcome with interventions — estimated success rate improvement

Supports two calculation methods: linear (default, `use_logit=False`) and logit-space (more mathematically sound, `use_logit=True`). Returns `BridgePeriodAssessment` with both human-readable report (`.generate_report()`) and JSON export (`.to_json()`).

**CLI** (`SCR/code/cli/cli.py`): Click-based wrapper over the engine. Supports single-patient JSON input, batch CSV processing, config validation, and patient template generation.

## Test Organization

`SCR/code/tests/run_tests.py` only runs `test_edge_cases.py` (and optionally `validate_config.py` with `--all`). The other four test files exist but are **broken** — they all import `LAI_DMT_v1`, a legacy module that no longer exists in the repo:

- `test_suite.py` — **broken** (`ModuleNotFoundError: LAI_DMT_v1`)
- `test_suite_2.py` — **broken** (`ModuleNotFoundError: LAI_DMT_v1`)
- `test_suite_3.py` — **broken** (`ModuleNotFoundError: LAI_DMT_v1`)
- `test_suite_4.py` — **broken** (`ModuleNotFoundError: LAI_DMT_v1`); 872 lines
- `test_edge_cases.py` — **runnable** but requires `SCR/code/algorithm/` on `sys.path`

`validate_config.py` validates the JSON configuration file structure separately from functional tests.

To run `test_edge_cases.py` correctly:
```bash
cd SCR/code/tests && PYTHONPATH=../algorithm pytest test_edge_cases.py -v
```

## Figure Generation

`SCR/code/fig_gen/` contains independent scripts that generate the 9 manuscript figures (MDPI format). Each script is standalone — run them individually to regenerate figures. Output goes to `SCR/figures/` as both PDF (vector) and PNG (600 dpi).

## Key Constraints

- The canonical config is `SCR/lai_prep_config.json`. Scripts that load it by relative path assume they are run from `SCR/` or receive the path explicitly via `config_path`. There is no copy in `SCR/code/algorithm/`.
- Populations are keyed by exact string names (`"MSM"`, `"adolescents"`, `"women"`, `"transgender_women"`, `"PWID"`, `"pregnant_lactating"`, `"general"`).
- License is MIT with a pharma restriction (`Project Docs/PHARMA_RESTRICTED_LICENSE.md`) — pharmaceutical companies require separate licensing.
