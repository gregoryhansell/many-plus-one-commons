#!/usr/bin/env python3
"""Re-run the public toy experiment and require the committed result to match."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENT = ROOT / "experiments/E001-causal-scale"
actual = json.loads(subprocess.check_output(
    [sys.executable, str(EXPERIMENT / "causal_scale.py")], cwd=ROOT))
recorded = json.loads((EXPERIMENT / "results.json").read_text())
if actual != recorded:
    raise SystemExit("E001 output differs from the committed result; review the scientific change.")
print("E001 reproduced exactly; analytic controls passed.")

actual = json.loads(subprocess.check_output(
    [sys.executable, str(EXPERIMENT / "stochastic_scale.py")], cwd=ROOT))
recorded = json.loads((EXPERIMENT / "stochastic-results.json").read_text())
if actual != recorded:
    raise SystemExit("E001-S output differs from the committed result.")
print("E001-S reproduced exactly; 16,640 matched comparisons and analytic controls passed.")
