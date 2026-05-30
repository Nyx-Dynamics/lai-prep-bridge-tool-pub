import sys
from pathlib import Path

# Add algorithm directory to path so pytest can collect test files that import
# lai_prep_decision_tool_v2_1 without requiring PYTHONPATH to be set manually.
sys.path.insert(0, str(Path(__file__).parent.parent / "algorithm"))
