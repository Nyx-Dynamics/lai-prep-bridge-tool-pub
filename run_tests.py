"""
Convenience script to re-run the test suite for the LAI-PrEP Bridge Tool.

Usage:
  python run_tests.py            # run unit/edge-case tests
  python run_tests.py --all      # run tests and configuration validation
  python run_tests.py --quiet    # minimal pytest output

This is useful after upgrading to a new version to quickly check for regressions.
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
        if validate_script.exists():
            # Run validate_config as a module for portability
            try:
                import runpy
                runpy.run_path(str(validate_script), run_name="__main__")
            except SystemExit as se:
                # Some scripts may call sys.exit; treat non-zero as failure
                if int(se.code or 0) != 0:
                    result_code = result_code or int(se.code)
            except Exception as e:
                print(f"Validation script failed: {e}")
                result_code = result_code or 1
        else:
            print("No validate_config.py found; skipping validation.")

    if result_code == 0:
        print("\n✅ All checks passed.")
    else:
        print("\n❌ Some checks failed.")

    return int(result_code)


if __name__ == "__main__":
    raise SystemExit(main())
