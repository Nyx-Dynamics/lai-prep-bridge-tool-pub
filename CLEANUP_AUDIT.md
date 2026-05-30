# CLEANUP AUDIT (temporary — delete before final commit)

## File-pair duplicates — all diffs are cosmetic ASCII/Unicode only, no logic diffs

| SCR root copy | SCR/code canonical | Action |
|---|---|---|
| SCR/cli.py | SCR/code/cli/cli.py | IDENTICAL — delete root copy |
| SCR/run_tests.py | SCR/code/tests/run_tests.py | IDENTICAL — delete root copy |
| SCR/test_edge_cases.py | SCR/code/tests/test_edge_cases.py | DIVERGENT (cosmetic) — delete root copy |
| SCR/test_suite.py | SCR/code/tests/test_suite.py | DIVERGENT (cosmetic) — delete root copy |
| SCR/test_suite_4.py | SCR/code/tests/test_suite_4.py | DIVERGENT (cosmetic) — delete root copy |
| SCR/validate_config.py | SCR/code/tests/validate_config.py | DIVERGENT (cosmetic) — delete root copy |

## Filename collision (Category A)
- SCR/lai_prep_decision_tool_v2_1.py (figure script) → rename generate_figures_viruses_2026.py, move to manuscripts/lai_figures/

## Config files
- SCR/lai_prep_config.json (v2.1.0 canonical) → move to SCR/code/algorithm/ (Phase 3)
- SCR/lai_prep_config_FIXED.json (v2.0.0 deprecated) → archive with date-stamp (Phase 6)

## Orphan scripts at SCR/ root
- SCR/fig_seven.py (0 bytes) — DELETE
- SCR/figure_3_convergence.py (1 byte) — DELETE
- SCR/fig_seven_two.py (74 lines, early draft fig7) — DELETE (A.C. confirmed)
- SCR/cascaades_revised.py (492 lines, canonical cascade fig) — rename + move to fig_gen/; archive fig_gen/cascades.py (wrong-machine hardcoded path)

## Root-level utilities
- organize.py (760 lines) — DELETE (A.C. confirmed)
- sync_projects.py (88 lines) — DELETE (A.C. confirmed)

## Validation artifacts
- config/validation_*.json — IDENTICAL to root copies — DELETE
- config/example_patient.json + example_patients.csv — UNIQUE, keep in config/
- Validation_progressive/ remaining: UNAIDS_Executive_Summary.md, WHO_UNAIDS_Policy_Brief.md — move to docs/

## Directory issues
- archieve/ — rename to archive/ (Phase 7)
- .DS_Store — add to .gitignore (Phase 8)
