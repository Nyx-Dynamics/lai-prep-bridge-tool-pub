# TODO: Config Loading Robustness

**Filed during repo-housekeeping session, 2026-05-30.**

## Problem

`SCR/code/algorithm/lai_prep_decision_tool_v2_1.py` — `Configuration._find_config_file()` tries
`Path(__file__).parent / "lai_prep_config.json"` but only as the *first* fallback path (index 0 of
the search list). The config lives at `SCR/lai_prep_config.json`, which is NOT in
`Path(__file__).parent` (`SCR/code/algorithm/`). This means all CWD-relative paths are tried first,
and the tool only works reliably when invoked from `SCR/`.

## Proposed fix (approved, deferred)

1. Move `SCR/lai_prep_config.json` → `SCR/code/algorithm/lai_prep_config.json`
2. In `_find_config_file`, set `Path(__file__).parent / "lai_prep_config.json"` as the **primary**
   path (not just the first fallback).
3. Update CLI `validate` command's `--config` default to point at the new location.
4. Update `validate_config.py` to default to `Path(__file__).parent / "../algorithm/lai_prep_config.json"`
   when no CLI argument is given.

**Authorized change scope:** Only config-loading path logic. The four-stage calculation flow and
all model coefficients in the algorithm are off-limits.

## Verification required after fix

```bash
cd / && python /path/to/SCR/code/tests/run_tests.py --all   # must pass from any CWD
cd ~/Desktop && python /path/to/SCR/code/cli/cli.py validate  # must pass from any CWD
```
