# TODO: v2.1 Validation Baseline

**Filed during repo-housekeeping session, 2026-05-30.**

## Problem

The published `validation_UNAIDS_21.2M_results.json` (at repo root) is a **v1 validation artifact**
generated with the `LAI_DMT_v1` API. It cannot be reproduced by the migrated `test_suite_4.py`
because the v2.1 config removed the `SEX_WORKER` population that existed in v1.

### Impact on regional weights in `test_suite_4.py`

`get_population_weights_by_region()` assigns weights based on population key substrings. In v1,
`SEX_WORKER` matched in Latin America (15% weight) and Asia-Pacific (20% weight). In v2.1, no
population key contains `SEX_WORKER`, so those patients fall into the general-population bucket.
This changes the effective population weight distribution for both regions, shifting results.

### What changed between v1 and v2.1

The `SEX_WORKER` population was removed in the v2.1 config refactor. The closest remaining
populations are `CISGENDER_WOMEN`, `TRANSGENDER_WOMEN`, and `GENERAL`. No explicit mapping
was defined.

## Decision needed

1. **Accept divergence:** Treat the published JSON as the v1 artifact (historical) and run
   `test_suite_4.py` to establish a new v2.1 validation baseline. Update the repository to
   make clear the published JSON is v1 and the current script produces v2.1 numbers.

2. **Restore parity:** Explicitly map the former `SEX_WORKER` regional weight to one or more
   v2.1 populations (e.g., split between `CISGENDER_WOMEN` and `GENERAL`) so the validation
   can reproduce the published numbers within tolerance.

3. **Add SEX_WORKER back:** Determine whether `SEX_WORKER` should be reinstated as a v2.1
   population with its own baseline attrition rate and barrier profile. Requires algorithm
   and config changes and a new publication note.

## If accepting divergence (option 1)

Run `test_suite_4.py` from `SCR/` to establish the v2.1 baseline:
```bash
cd SCR && python code/tests/test_suite_4.py
# Answer "yes" at the prompt — expected runtime 3-10 min
```

The output JSON should be saved alongside the v1 artifact with a clear version label:
```
validation_UNAIDS_21.2M_results_v1.json   ← rename the current published file
validation_UNAIDS_21.2M_results_v21.json  ← new file from test_suite_4.py run
```

## Related files

- `test_suite_4.py` (see MIGRATION NOTE in file header)
- `validation_UNAIDS_21.2M_results.json` (v1 artifact, repo root)
- `docs/CHANGELOG.md` — v2.1.1 section documents the divergence
