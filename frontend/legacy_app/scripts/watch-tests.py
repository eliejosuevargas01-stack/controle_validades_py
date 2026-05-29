#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WATCH_EXTS = {".html", ".js", ".mjs", ".py", ".md"}
POLL_INTERVAL = 1.0


def snapshot() -> dict[str, float]:
    data: dict[str, float] = {}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in WATCH_EXTS:
            continue
        try:
            data[str(path)] = path.stat().st_mtime
        except OSError:
            continue
    return data


def run_tests() -> int:
    print("\n[watch] running tests...")
    result = subprocess.run(["node", str(ROOT / "scripts" / "run-tests.mjs")], cwd=ROOT)
    return result.returncode


def main() -> int:
    previous = snapshot()
    run_tests()
    while True:
        time.sleep(POLL_INTERVAL)
        current = snapshot()
        if current != previous:
            previous = current
            run_tests()

if __name__ == "__main__":
    raise SystemExit(main())
