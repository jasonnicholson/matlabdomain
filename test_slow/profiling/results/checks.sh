#!/usr/bin/env bash
# Phase 1 (#24/#26) verification checks; logs go to results/checks/.
#
# usage: bash test_slow/profiling/results/checks.sh   (from any directory)
#
# Requires matlabdomain/.venv (free-threaded CPython 3.14) and
# matlabdomain/.tox/py312-sphinxlatest (CPython 3.12, GIL; holds an older
# sdist, so the checkout's sphinxcontrib is prepended to the namespace path).
# PYTHONPATH is unset: the inherited value ended in ':', which put the
# checkout on sys.path and shadowed the sphinxcontrib namespace package.
set -u
root=$(cd "$(dirname "$0")/../../.." && pwd)
out="$root/test_slow/profiling/results/checks"
tmp=$(mktemp -d)
mkdir -p "$out"
cd "$root" || exit 1
unset PYTHONPATH
ulimit -c 0
py312=.tox/py312-sphinxlatest/bin/python
summary="$out/summary.txt"
{
  echo "date: $(date -Is)"
  echo "code: $(git rev-parse HEAD) (+ uncommitted Phase 1 changes)"
  git status --short
} > "$summary"

# prctl(PR_SET_DUMPABLE, 0): expected crashes leave no systemd-coredump entries
# (ulimit -c 0 does not stop a piped core_pattern).
prefix='import ctypes, pathlib, sys, sphinxcontrib
ctypes.CDLL(None).prctl(4, 0)
sphinxcontrib.__path__ = [str(pathlib.Path("sphinxcontrib").resolve())] + list(sphinxcontrib.__path__)
import sphinxcontrib.mat_tree_sitter_parser as tsp
assert pathlib.Path(tsp.__file__).resolve().is_relative_to(pathlib.Path(".").resolve())
import os, pytest
'

# 1. Regression test discriminates: fixed get_row vs tree-sitter 0.26.0 Point.row.
regtest="$prefix"'if os.environ["P1_VARIANT"] == "old_row_getter":
    tsp.get_row = lambda point: point.row
sys.exit(pytest.main(["tests/test_mat_tree_sitter_parser.py", "-q", "-o", "addopts=", "-p", "no:cacheprovider"]))
'
for variant in fixed old_row_getter; do
  for t in 1 2 3 4 5; do
    P1_VARIANT=$variant "$py312" -X faulthandler -c "$regtest" \
      > "$out/regtest-py312-$variant-$t.log" 2>&1
    echo "regtest py312 $variant run $t rc=$?" >> "$summary"
  done
done

# 2. Full suite with current code on CPython 3.12 (GIL).
fullsuite="$prefix"'sys.exit(pytest.main(["-q", "-o", "addopts=", "-p", "no:cacheprovider"]))
'
for t in 1 2; do
  "$py312" -X faulthandler -c "$fullsuite" > "$out/fullsuite-py312-$t.log" 2>&1
  echo "fullsuite py312 run $t rc=$? $(tail -n 1 "$out/fullsuite-py312-$t.log")" >> "$summary"
done

# 3. Full suite + coverage in the project venv (recorded #23 method).
COVERAGE_FILE="$tmp/.coverage" .venv/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider --cov > "$out/fullsuite-venv-cov.log" 2>&1
echo "fullsuite venv rc=$? $(grep -E '^TOTAL' "$out/fullsuite-venv-cov.log") $(tail -n 1 "$out/fullsuite-venv-cov.log")" >> "$summary"

# 4. Existing launch.json targets (#24). The harness sphinx-build is expected
#    to fail on +vlt/+plot/hist2d.m (deferred to Phase 5).
.venv/bin/python -m sphinx.cmd.build -b html docs "$tmp/docs-html" > "$out/launch-docs.log" 2>&1
echo "launch docs build rc=$?" >> "$summary"
.venv/bin/python -m pytest tests/test_mat_tree_sitter_parser.py -o addopts= -vv \
  -p no:cacheprovider > "$out/launch-pytest-file.log" 2>&1
echo "launch pytest current file rc=$?" >> "$summary"
.venv/bin/python -m sphinx.cmd.build -b html -E test_slow/profiling "$tmp/harness-html" \
  > "$out/launch-harness-sphinx-build.log" 2>&1
echo "launch harness sphinx-build rc=$? (expected 2: hist2d)" >> "$summary"
errlog=$(grep -o '/tmp/sphinx-err-[A-Za-z0-9_]*\.log' "$out/launch-harness-sphinx-build.log" | head -n 1)
if [ -n "$errlog" ]; then
  cp "$errlog" "$out/launch-harness-sphinx-err.log" && rm -f "$errlog"
fi

# 5. Lint on the changed parser and new test (ruff/codespell versions from
#    .pre-commit-config.yaml; its duplicate `repos:` key disables those hooks).
f=sphinxcontrib/mat_tree_sitter_parser.py
uvx -q ruff@0.14.10 check --output-format concise "$f" 2>/dev/null \
  | grep "^$f:" | sed -E 's/:[0-9]+:[0-9]+:/:/' | sort > "$out/ruff-parser-new.txt"
git show "HEAD:$f" | uvx -q ruff@0.14.10 check --output-format concise --stdin-filename "$f" - 2>/dev/null \
  | grep "^$f:" | sed -E 's/:[0-9]+:[0-9]+:/:/' | sort > "$out/ruff-parser-head.txt"
echo "ruff parser findings (line numbers ignored): HEAD=$(wc -l < "$out/ruff-parser-head.txt") new=$(wc -l < "$out/ruff-parser-new.txt") added=$(comm -13 "$out/ruff-parser-head.txt" "$out/ruff-parser-new.txt" | wc -l) removed=$(comm -23 "$out/ruff-parser-head.txt" "$out/ruff-parser-new.txt" | wc -l)" >> "$summary"
git show "HEAD:$f" | uvx -q ruff@0.14.10 format --check --stdin-filename "$f" - > /dev/null 2>&1
echo "ruff format --check parser at HEAD rc=$? (pre-existing drift if 1)" >> "$summary"
uvx -q ruff@0.14.10 format --diff "$f" > "$out/ruff-format-parser.diff" 2>/dev/null
echo "ruff format --check parser now rc=$? (diff in ruff-format-parser.diff)" >> "$summary"
uvx -q ruff@0.14.10 check tests/test_mat_tree_sitter_parser.py > "$out/ruff-test.txt" 2>&1
echo "ruff check new test rc=$?" >> "$summary"
uvx -q ruff@0.14.10 format --check tests/test_mat_tree_sitter_parser.py >> "$out/ruff-test.txt" 2>&1
echo "ruff format --check new test rc=$?" >> "$summary"
uvx -q --with tomli codespell@2.4.1 --toml pyproject.toml "$f" tests/test_mat_tree_sitter_parser.py \
  > "$out/codespell.txt" 2>&1
echo "codespell rc=$?" >> "$summary"

rm -rf "$tmp"
cat "$summary"
