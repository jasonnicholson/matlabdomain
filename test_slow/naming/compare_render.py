"""Snapshot and compare rendered HTML anchors/links across code versions.

Usage (run from the matlabdomain repo root):

  # snapshot with whatever ``sphinxcontrib.matlab`` the interpreter imports
  PYTHONPATH=<code-root> <python> test_slow/naming/compare_render.py snapshot OUT.json
  <python> test_slow/naming/compare_render.py compare A.json B.json

Builds every ``tests/roots/*``, ``tests/test_docs`` and ``docs`` (copied to a
temp dir) with several ``matlab_*`` variants and records, per HTML page, the
element ids, the internal ``href`` targets, an md5 of the page body, the
decoded ``objects.inv`` entries and the (path-normalized) warnings.
"""

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VARIANTS = {
    "conf": [],
    "keep0": ["-D", "matlab_keep_package_prefix=0"],
    "keep1": ["-D", "matlab_keep_package_prefix=1"],
    "short": ["-D", "matlab_short_links=1"],
    "all": ["-D", "matlab_auto_link=all"],
}
ID_RE = re.compile(r'\bid="([^"]*)"')
HREF_RE = re.compile(r'\bhref="([^"#]*#[^"]*)"')
BODY_RE = re.compile(r'<div class="body"[^>]*>(.*?)<div class="sphinxsidebar"', re.DOTALL)


def projects(tmp):
    out = {}
    for root in sorted((REPO / "tests" / "roots").iterdir()):
        dst = tmp / "roots" / root.name
        shutil.copytree(root, dst, ignore=shutil.ignore_patterns("_build"))
        out[f"roots/{root.name}"] = dst
    tests = tmp / "tests"
    shutil.copytree(
        REPO / "tests",
        tests,
        ignore=shutil.ignore_patterns("_build", "__pycache__", "roots"),
    )
    out["test_docs"] = tests / "test_docs"
    docs = tmp / "docs"
    shutil.copytree(REPO / "docs", docs, ignore=shutil.ignore_patterns("_build"))
    out["docs"] = docs
    return out


def inventory(path):
    from sphinx.util.inventory import InventoryFile

    with open(path, "rb") as f:
        inv = InventoryFile.load(f, "", lambda _base, uri: uri)
    rows = []
    for objtype, items in inv.items():
        if not objtype.startswith("mat:"):
            continue
        for name, item in items.items():
            uri = item[2] if isinstance(item, tuple) else item.uri
            rows.append(f"{objtype} {name} {uri}")
    return sorted(rows)


def snapshot(out_path):
    result = {}
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for name, src in projects(tmp).items():
            for vname, extra in VARIANTS.items():
                outdir = tmp / "out" / name / vname
                warnfile = tmp / "warn.txt"
                cmd = [sys.executable, "-m", "sphinx", "-b", "html", "-E", "-q"]
                cmd += ["-w", str(warnfile), *extra, str(src), str(outdir)]
                proc = subprocess.run(cmd, capture_output=True, text=True)
                warnings = []
                if warnfile.exists():
                    text = warnfile.read_text().replace(str(tmp), "<TMP>")
                    warnings = sorted(set(text.splitlines()))
                pages = {}
                for html in sorted(outdir.glob("**/*.html")):
                    rel = str(html.relative_to(outdir))
                    if rel in ("genindex.html", "search.html"):
                        continue
                    text = html.read_text()
                    m = BODY_RE.search(text)
                    body = m.group(1) if m else text
                    pages[rel] = {
                        "md5": hashlib.md5(body.encode()).hexdigest(),
                        "ids": ID_RE.findall(body),
                        "hrefs": HREF_RE.findall(body),
                    }
                inv = outdir / "objects.inv"
                result[f"{name}|{vname}"] = {
                    "rc": proc.returncode,
                    "warnings": warnings,
                    "pages": pages,
                    "inventory": inventory(inv) if inv.exists() else [],
                }
    Path(out_path).write_text(json.dumps(result, indent=1, sort_keys=True))


def compare(a_path, b_path):
    a = json.loads(Path(a_path).read_text())
    b = json.loads(Path(b_path).read_text())
    same = 0
    for key in sorted(set(a) | set(b)):
        ra, rb = a.get(key), b.get(key)
        if ra is None or rb is None:
            print(f"== {key}: only in {'B' if ra is None else 'A'}")
            continue
        diffs = []
        if ra["rc"] != rb["rc"]:
            diffs.append(f"  rc {ra['rc']} -> {rb['rc']}")
        diffs.extend(f"  -warn {w}" for w in sorted(set(ra["warnings"]) - set(rb["warnings"])))
        diffs.extend(f"  +warn {w}" for w in sorted(set(rb["warnings"]) - set(ra["warnings"])))
        diffs.extend(f"  -inv {i}" for i in sorted(set(ra["inventory"]) - set(rb["inventory"])))
        diffs.extend(f"  +inv {i}" for i in sorted(set(rb["inventory"]) - set(ra["inventory"])))
        for page in sorted(set(ra["pages"]) | set(rb["pages"])):
            pa, pb = ra["pages"].get(page), rb["pages"].get(page)
            if pa is None or pb is None:
                diffs.append(f"  page {page} only in {'B' if pa is None else 'A'}")
                continue
            if pa["md5"] == pb["md5"]:
                continue
            for kind in ("ids", "hrefs"):
                ca, cb = Counter(pa[kind]), Counter(pb[kind])
                for v, n in sorted((ca - cb).items()):
                    diffs.append(f"  {page} -{kind[:-1]} {v} (x{n})")
                for v, n in sorted((cb - ca).items()):
                    diffs.append(f"  {page} +{kind[:-1]} {v} (x{n})")
            if pa["ids"] == pb["ids"] and pa["hrefs"] == pb["hrefs"]:
                diffs.append(f"  {page} body differs (same ids/hrefs)")
        if diffs:
            print(f"== {key}")
            print("\n".join(diffs))
        else:
            same += 1
    print(f"identical builds: {same}/{len(set(a) | set(b))}")


if __name__ == "__main__":
    if sys.argv[1] == "snapshot":
        snapshot(sys.argv[2])
    else:
        compare(sys.argv[2], sys.argv[3])
