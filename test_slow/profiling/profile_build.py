"""Profiling harness for SCM's eager parse cost (Phase 1 "before" baseline).

The current extension parses **every** ``.m`` file up front on ``builder-inited``
(``analyze()`` -> ``MatObject.parse_mfile`` -> tree-sitter). On a large tree this
is the lock-up we intend to fix (Phase 6, lazy parsing).

Why a direct parse-sweep instead of a full ``sphinx-build``: on the bundled
``vhlab-toolbox-matlab`` tree the current code **crashes** on at least one
unparseable ``.m`` file (``AttributeError: 'NoneType' ... 'text'`` in
``mat_tree_sitter_parser``), aborting the whole ``builder-inited`` handler. That
fault-intolerance is exactly what Phase 5 fixes, but it also means a
Sphinx-driven build cannot complete today. So we profile the eager parse
directly, wrapping each file in try/except to (a) measure the true parse cost
across all files and (b) tally the files that crash the current parser as a
seed for the Phase 5 bug list.

Usage
-----
    python test_slow/profiling/profile_build.py [SRC_DIR]

Defaults ``SRC_DIR`` to the largest bundled fixture
(``../artifacts/vhlab-toolbox-matlab/repo``). Writes cProfile stats to
``before.prof`` and prints top cumulative-time functions plus a parse-failure
summary. Inspect interactively with::

    pip install snakeviz
    snakeviz test_slow/profiling/before.prof

After the Phase 6 lazy rework, re-profile a real ``sphinx-build`` (see the
``conf.py`` beside this file) to capture ``after.prof`` and quantify the speedup.

Baseline captured (Phase 1 — TRUE baseline)
-------------------------------------------
Env: git worktree at commit 0ce8fa0 (../scm-baseline), uv, standard (GIL)
CPython 3.14.6, tree-sitter 0.22.3, tree-sitter-matlab 1.0.4, Sphinx 9.1.0.
Suite: 137 passed, 4 xfailed, 80% coverage, ~12.6 s.
Tree: vhlab-toolbox-matlab/repo, 1726 .m files.
  * Eager parse wall time: ~6.07 s (3.5 ms/file), 0 parse failures.
  * Dominant avoidable overhead (motivates Phase 4/6):
      - tree-sitter ``Language.query`` recompiled on EVERY isFunction/isClass
        call (~2.66 s). Should be module-level compiled queries.
      - ``importlib.metadata.version("tree_sitter")`` called once PER FILE inside
        parse_mfile (~1.7 s in package-metadata parsing). Should be cached once.

Regression found in the working copy (tree-sitter 0.26.0 / matlab 1.3.x)
------------------------------------------------------------------------
Re-running the same sweep against the working-copy code+deps gives ~16.7 s
(2.7x SLOWER) AND crashes on +vlt/+plot/hist2d.m
(AttributeError: 'NoneType' has no attribute 'text'). So the 0.22->0.26 upgrade
regressed both speed and robustness on this grammar: flag for the Phase 1
tree-sitter task and the Phase 5 bug list.
"""

from __future__ import annotations

import cProfile
import pstats
import sys
import time
from pathlib import Path

from sphinxcontrib.mat_types import MatObject

HERE = Path(__file__).resolve().parent
DEFAULT_SRC = HERE / ".." / "artifacts" / "vhlab-toolbox-matlab" / "repo"
PROFILE_OUT = HERE / "before.prof"

_failures: list[tuple[str, str]] = []
_ok = 0


def _sweep(src_dir: Path) -> None:
    global _ok
    for mfile in sorted(src_dir.rglob("*.m")):
        name = mfile.stem
        path = str(mfile.parent)
        try:
            MatObject.parse_mfile(str(mfile), name, path)
            _ok += 1
        except Exception as exc:  # noqa: BLE001 - harness tallies, never aborts
            _failures.append((str(mfile), f"{type(exc).__name__}: {exc}"))


def main() -> None:
    src_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_SRC.resolve()
    total = sum(1 for _ in src_dir.rglob("*.m"))
    print(f"Profiling eager parse of {total} .m files under:\n  {src_dir}\n")

    profiler = cProfile.Profile()
    start = time.perf_counter()
    profiler.enable()
    _sweep(src_dir)
    profiler.disable()
    elapsed = time.perf_counter() - start

    profiler.dump_stats(str(PROFILE_OUT))

    print(f"Parsed OK : {_ok}")
    print(f"Failed    : {len(_failures)}")
    print(f"Wall time : {elapsed:.2f}s  ({elapsed / max(total, 1) * 1000:.2f} ms/file)")
    print(f"Profile   : {PROFILE_OUT}\n")

    if _failures:
        print(f"First {min(10, len(_failures))} parse failures (Phase 5 bug-list seed):")
        for path, err in _failures[:10]:
            print(f"  - {path}\n      {err}")
        print()

    print("Top 20 by cumulative time:")
    pstats.Stats(str(PROFILE_OUT)).strip_dirs().sort_stats("cumulative").print_stats(20)


if __name__ == "__main__":
    main()
