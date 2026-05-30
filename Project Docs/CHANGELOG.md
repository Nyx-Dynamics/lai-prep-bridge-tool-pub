# Changelog

All notable changes to the LAI-PrEP Bridge Period Decision Support Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.1] - 2026-05-30

### Housekeeping release — no algorithm logic changes, no schema changes

#### Fixed
- Resolved filename collision: `SCR/lai_prep_decision_tool_v2_1.py` (figure generation suite, 696 lines) renamed to `manuscripts/lai_figures/generate_figures_viruses_2026.py`. Previously, `from lai_prep_decision_tool_v2_1 import LAIPrEPDecisionTool` was ambiguous if `SCR/` appeared before `SCR/code/algorithm/` on sys.path.
- Fixed `run_tests.py --all` sys.argv bug: config validation step was receiving `--all` as the config file path instead of the actual config path.
- Fixed CLI import: `SCR/code/cli/cli.py` now adds the algorithm directory to sys.path at startup, enabling invocation from any working directory.
- Corrected CLAUDE.md population keys (were lowercase snake_case; actual keys are UPPERCASE_SNAKE_CASE).

#### Changed
- Migrated all four previously-broken test suites (`test_suite.py`, `test_suite_2.py`, `test_suite_3.py`, `test_suite_4.py`) from the removed `LAI_DMT_v1` module to the current `lai_prep_decision_tool_v2_1` API. All five test files are now runnable.
- Added `SCR/code/tests/conftest.py` so pytest finds the algorithm module without manual `PYTHONPATH` export.
- Moved `SCR/lai_prep_config_FIXED.json` (deprecated v2.0.0 copy) to `archive/lai_prep_config_v2.0.0_2025-01-12.json`.
- Consolidated validation JSONs: removed duplicates from `config/` (identical to copies at repo root). Canonical location is repo root.
- Moved UNAIDS policy documents from `Validation_progressive/` to `docs/`.
- Renamed `archieve/` → `archive/mdpi_figures_viruses_2026/` (directory typo fix).
- Removed 6 duplicate Python files at `SCR/` root (cosmetic ASCII/Unicode diffs only; canonical versions in `SCR/code/`).
- Renamed `SCR/cascaades_revised.py` → `SCR/code/fig_gen/cascades_revised.py` (fixed double-a typo; this is the canonical cascade figure generator).
- Removed `organize.py` and `sync_projects.py` (personal developer utilities not appropriate for a public research repo).
- Untracked `.DS_Store` (was already in .gitignore).

#### Known divergence (documented, not a bug)
- `test_suite_4.py` (21.2M UNAIDS validation) will produce different numbers from the published `validation_UNAIDS_21.2M_results.json`. Root cause: v1 included a `SEX_WORKER` population absent from v2.1's config, changing regional weight distributions in Latin America and Asia-Pacific. The published JSON remains the v1 validation artifact. Config-loading robustness deferred to a future session; see `TODO_config_loading.md`.

## [Unreleased]

### Planned Features
- EHR integration modules (Epic, Cerner)
- Real-time outcome tracking dashboard
- Multi-language support (Spanish, French)
- Mobile application
- Machine learning enhancements
- Config loading robustness: move config into `SCR/code/algorithm/` and load via `Path(__file__).parent` (see `TODO_config_loading.md`)

## [1.0.0] - 2025-10-10

### Added
- **Core Decision Algorithm**
  - Patient risk assessment for bridge period navigation
  - Population-specific barrier identification
  - Evidence-based intervention recommendations
  - Predicted outcome calculations

- **Population Support**
  - Men who have sex with men (MSM)
  - Cisgender women
  - Transgender women
  - Adolescents and young adults (16-24 years)
  - People who inject drugs (PWID)
  - Pregnant and lactating individuals

- **Healthcare Settings**
  - Academic medical centers
  - Community health centers
  - Private practices
  - Pharmacy-based care
  - Harm reduction sites
  - LGBTQ+ community centers
  - Mobile clinics
  - Telehealth-integrated settings

- **Evidence-Based Interventions**
  - Patient navigation programs
  - RNA testing (accelerated diagnostics)
  - Oral-to-injectable PrEP transitions
  - Telehealth integration
  - Pharmacy-based delivery
  - Same-day initiation protocols
  - Community-based distribution

- **Documentation**
  - Comprehensive clinical guide (NON_TECHNICAL_GUIDE.md)
  - Quick reference card for clinicians
  - Implementation checklist
  - Technical documentation
  - Data privacy and security guide
  - Training materials
  - GitHub upload instructions

- **Testing**
  - Unit tests for core functionality
  - Integration tests for workflow
  - Population-specific test cases
  - Barrier combination testing

- **Examples**
  - Clinical case studies
  - Implementation scenarios
  - Population-specific examples
  - Outcome prediction examples

### Documentation
- README.md with comprehensive project overview
- CONTRIBUTING.md with contribution guidelines
- CODE_OF_CONDUCT.md with community standards
- LICENSE file (MIT License)
- CHANGELOG.md (this file)

### Research Foundation
- Based on manuscript: "Bridging the Gap: The PrEP Cascade Paradigm Shift for Long-Acting Injectable HIV Prevention"
- Evidence synthesis from HPTN 083, 084 trials
- Real-world implementation data from multiple sites
- Population-specific barrier research
- Intervention effectiveness analysis

## [0.9.0-beta] - 2025-09-15

### Added
- Beta version for clinical validation
- Core decision algorithm (preliminary)
- Basic documentation
- Initial test suite

### Testing
- Clinical validation at 3 sites
- 150+ patient assessments
- Feedback collection from clinicians

## [0.5.0-alpha] - 2025-08-01

### Added
- Alpha version for internal testing
- Proof-of-concept decision algorithm
- Basic intervention recommendations

### Research
- Literature review completed
- Evidence synthesis begun
- Population barrier analysis

## [0.1.0-concept] - 2025-06-01

### Initial Concept
- Project conception
- Research proposal
- Stakeholder consultation
- Feasibility assessment

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

## Types of Changes

- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security vulnerability fixes

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to suggest changes or report issues.

## Release Notes

Detailed release notes for each version are available in the [Releases](https://github.com/yourusername/lai-prep-bridge-tool/releases) section.

---

*Last updated: October 10, 2025*
