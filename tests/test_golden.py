from __future__ import annotations

import json
from pathlib import Path

from compometa.transform import transform_cyclonedx

ROOT = Path(__file__).resolve().parents[1]
INP = ROOT / "examples" / "input"
EXP = ROOT / "examples" / "expected"


def _norm(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def test_golden_examples():
    assert INP.exists(), "examples/input missing"
    assert EXP.exists(), "examples/expected missing"

    inputs = sorted(INP.glob("*.json"))
    assert inputs, "no example SBOMs found in examples/input"

    for f in inputs:
        expected_path = EXP / f.name
        assert expected_path.exists(), f"missing expected file for {f.name}"

        inp_obj = json.loads(f.read_text(encoding="utf-8"))
        out_obj = transform_cyclonedx(inp_obj)

        assert _norm(out_obj) == expected_path.read_text(encoding="utf-8"), f"golden mismatch: {f.name}"

