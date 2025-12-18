
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .transform import transform_cyclonedx


def main() -> int:
    p = argparse.ArgumentParser(prog="compometa")
    p.add_argument("--in", dest="inp", required=True, help="Input CycloneDX JSON")
    p.add_argument("--out", dest="out", required=True, help="Output CycloneDX JSON")
    p.add_argument("--provider", choices=["none"], default="none")  # future: gcs,endoflife,...

    args = p.parse_args()

    data = json.loads(Path(args.inp).read_text(encoding="utf-8"))
    out = transform_cyclonedx(data)

    Path(args.out).write_text(
        json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

