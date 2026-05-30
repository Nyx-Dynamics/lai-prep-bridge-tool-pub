"""
Convenience script to re-run the test suite for the LAI-PrEP Bridge Tool.

Usage:
  python run_tests.py            # run unit/edge-case tests + simulation tests
  python run_tests.py --all      # run tests and configuration validation
  python run_tests.py --quiet    # minimal pytest output

Pytest-runnable tests (collected automatically):
  test_edge_cases.py  -- boundary conditions, error handling (18 tests)

Standalone simulation scripts (run directly, not via this runner):
  test_suite.py       -- unit tests: oral PrEP, barriers, populations (python test_suite.py)
  test_suite_2.py     -- 1M patient validation (~30 min)
  test_suite_3.py     -- 10M patient streaming validation (~5 min)
  test_suite_4.py     -- 21.2M UNAIDS-scale validation (~10 min)
                         NOTE: results will differ from published validation_UNAIDS_21.2M_results.json
                         because v2.1 config removed the SEX_WORKER population present in v1.

Must be run from SCR/ directory (config is at SCR/lai_prep_config.json).
"""
from __future__ import annotations

import argparse
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run LAI-PrEP Bridge Tool tests")
    parser.add_argument("--all", action="store_true", help="Run tests and config validation")
    parser.add_argument("--quiet", action="store_true", help="Minimize pytest output")
    args = parser.parse_args(argv)

    # Ensure pytest is available
    try:
        import pytest  # type: ignore
    except Exception as e:
        print("pytest is required. Install dev requirements:")
        print("  pip install -r requirements-dev.txt")
        return 1

    repo_root = Path(__file__).parent
    test_file = repo_root / "test_edge_cases.py"
    if not test_file.exists():
        print(f"Could not find test file: {test_file}")
        return 1

    pytest_args = [str(test_file), "-v", "--tb=short"]
    if args.quiet:
        pytest_args = [str(test_file), "-q"]

    print("==> Running test suite\n")
    result_code = pytest.main(pytest_args)

    if args.all:
        print("\n==> Running configuration validation\n")
        validate_script = repo_root / "validate_config.py"
        config_path = repo_root.parent.parent / "lai_prep_config.json"
        if validate_script.exists():
            try:
                import sys as _sys
                import runpy
                _old_argv = _sys.argv[:]
                _sys.argv = [str(validate_script), str(config_path)]
                try:
                    runpy.run_path(str(validate_script), run_name="__main__")
                finally:
                    _sys.argv = _old_argv
            except SystemExit as se:
                if int(se.code or 0) != 0:
                    result_code = result_code or int(se.code)
            except Exception as e:
                print(f"Validation script failed: {e}")
                result_code = result_code or 1
        else:
            print("No validate_config.py found; skipping validation.")

    if result_code == 0:
        print("\n[SUCCESS] All checks passed.")
    else:
        print("\n[FAILED] Some checks failed.")

    return int(result_code)


if __name__ == "__main__":
    raise SystemExit(main())
