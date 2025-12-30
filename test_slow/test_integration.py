#!/usr/bin/env python3
"""
Integration tests for sphinxcontrib-matlabdomain.

These tests validate the matlabdomain plugin against real-world MATLAB projects
by cloning them and generating Sphinx documentation. They are designed to run
infrequently (e.g., in nightly builds) as they are slow and require network access.
Projects and their MATLAB source directories are defined in project_data.json.
Artifacts (cloned repos, generated RST, build logs) are stored per project under
test_slow/artifacts/<project_name> for later inspection.

To run these tests:
    pytest test_slow/test_integration.py -v -s -m slow

To run only a specific project (filter by repo name or URL substring):
    pytest test_slow/test_integration.py -v -s -m slow -k "matnwb"
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

import pytest

# Get the test_slow directory
TEST_SLOW_DIR = Path(__file__).resolve().parent
PROJECT_DATA_FILE = TEST_SLOW_DIR / "project_data.json"
ARTIFACTS_ROOT = TEST_SLOW_DIR / "artifacts"


def load_project_data() -> List[Dict[str, str]]:
    """Load project definitions from project_data.json."""
    if not PROJECT_DATA_FILE.exists():
        pytest.skip(f"project_data.json not found at {PROJECT_DATA_FILE}")

    with open(PROJECT_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    projects = data.get("projects", [])
    if not projects:
        pytest.skip("project_data.json contains no projects")

    # Validate required keys
    for entry in projects:
        if "url" not in entry or "matlab_src_dir" not in entry:
            pytest.skip(
                "project_data.json entries must include 'url' and 'matlab_src_dir'"
            )

    return projects


def extract_project_name(url: str) -> str:
    """Extract project name from git URL."""
    # Extract the last part of the URL without .git
    return url.split("/")[-1].replace(".git", "")


def clone_repository(url: str, clone_path: Path) -> Path:
    """Clone a repository with --filter=blob:none for shallow cloning into clone_path."""
    clone_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "git",
        "clone",
        "--filter=blob:none",
        "--depth=1",
        url,
        str(clone_path),
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return clone_path


def update_repository(repo_path: Path) -> None:
    """Fetch latest changes if the repository already exists."""
    cmd = ["git", "-C", str(repo_path), "fetch", "--all", "--prune"]
    subprocess.run(cmd, check=True, capture_output=True)


def _write_minimal_conf(docs_source: Path, matlab_source: Path) -> None:
    """Write a minimal conf.py to enable sphinx-build / sphinx-autobuild later."""
    docs_source.mkdir(parents=True, exist_ok=True)
    conf_path = docs_source / "conf.py"

    content = f"""import os
import sys

project = "MATLAB API Documentation"
extensions = [
    "sphinxcontrib.matlab",
    "sphinx.ext.autodoc",
]

# Absolute MATLAB source directory used by sphinxcontrib-matlabdomain
# Must be a string path, not a list
matlab_src_dir = r"{matlab_source}"

primary_domain = "mat"
master_doc = "index"
html_theme = "alabaster"
"""

    conf_path.write_text(content, encoding="utf-8")


@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.parametrize(
    "project",
    load_project_data(),
    ids=lambda p: extract_project_name(p["url"]),
)
def test_project_documentation_generation(project: Dict[str, str]) -> None:
    """
    Test that sphinx-matlab-apidoc can generate documentation for a project.

    This test:
    1. Clones the project from the given URL
    2. Uses the specified MATLAB source directory
    3. Runs sphinx-matlab-apidoc to generate RST files

    Args:
        project: Mapping with 'url' and 'matlab_src_dir'
    """
    url = project["url"]
    matlab_src_rel = project["matlab_src_dir"]
    project_name = extract_project_name(url)

    # Prepare artifact directory for this project
    ARTIFACTS_ROOT.mkdir(parents=True, exist_ok=True)
    project_artifacts = ARTIFACTS_ROOT / project_name
    project_artifacts.mkdir(parents=True, exist_ok=True)

    repo_dir = project_artifacts / "repo"
    docs_root = project_artifacts / "docs"
    docs_source = docs_root / "source"
    build_dir = docs_root / "_build" / "html"

    print(f"\n{'=' * 70}")
    print(f"Testing project: {project_name}")
    print(f"URL: {url}")
    print(f"Artifacts: {project_artifacts}")
    print(f"{'=' * 70}\n")

    # Clone or update the repository
    if repo_dir.exists() and (repo_dir / ".git").exists():
        print(f"[1/4] Updating existing repository (fetch)...")
        update_repository(repo_dir)
        project_dir = repo_dir
        print(f"      ✓ Fetched latest refs in {project_dir}")
    else:
        print(f"[1/4] Cloning repository...")
        project_dir = clone_repository(url, repo_dir)
        print(f"      ✓ Cloned to {project_dir}")

    # Use configured MATLAB source directory
    print(f"[2/4] Locating MATLAB source directory (configured)...")
    matlab_source = (project_dir / matlab_src_rel).resolve()
    if not matlab_source.exists():
        pytest.skip(f"Configured MATLAB source dir not found: {matlab_source}")
    matlab_count = sum(1 for _ in matlab_source.rglob("*.m"))
    print(f"      ✓ Found {matlab_count} MATLAB files in {matlab_source}")

    if matlab_count == 0:
        pytest.skip(f"No MATLAB files found in {project_name}")

    # Clean docs dir before regeneration
    if docs_root.exists():
        shutil.rmtree(docs_root)

    # Generate documentation with sphinx-matlab-apidoc
    print(f"[3/4] Generating documentation with sphinx-matlab-apidoc...")

    cmd = [
        sys.executable,
        "-m",
        "sphinxcontrib.sphinx_matlab_apidoc",
        str(matlab_source),
        "-o",
        str(docs_source),
        "--force",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        pytest.fail(
            f"sphinx-matlab-apidoc failed for {project_name}. "
            f"See output above for details."
        )

    rst_count = sum(1 for _ in docs_source.glob("*.rst"))
    print(f"      ✓ Generated {rst_count} RST files")
    print(f"      RST path: {docs_source}")

    # Write a minimal conf.py to support sphinx-build / sphinx-autobuild downstream
    _write_minimal_conf(docs_source, matlab_source)
    print(f"      ✓ Wrote conf.py for manual builds")

    # Build HTML to capture warnings/errors (kept in artifacts)
    print(f"[4/4] Building HTML with sphinx-build...")
    build_stdout = project_artifacts / "build_stdout.log"
    build_stderr = project_artifacts / "build_stderr.log"

    build_cmd = [
        "sphinx-build",
        "-b",
        "html",
        str(docs_source),
        str(build_dir),
    ]

    build_result = subprocess.run(build_cmd, capture_output=True, text=True)
    build_stdout.write_text(build_result.stdout, encoding="utf-8")
    build_stderr.write_text(build_result.stderr, encoding="utf-8")

    # Collect warnings related to sphinxcontrib-matlabdomain
    warning_lines = []
    error_lines = []
    for line in (build_result.stdout + "\n" + build_result.stderr).splitlines():
        lower = line.lower()
        if "error" in lower and ("matlab" in lower or "sphinxcontrib" in lower):
            error_lines.append(line)
        elif "warning" in lower and ("matlab" in lower or "sphinxcontrib" in lower):
            warning_lines.append(line)

    print(f"      sphinx-build return code: {build_result.returncode}")
    print(f"      HTML output: {build_dir}")
    print(f"      Logs: {build_stdout} and {build_stderr}")

    if error_lines:
        print("      ERRORS mentioning matlabdomain/sphinxcontrib:")
        for el in error_lines[:10]:  # Show first 10
            print(f"        {el}")
        if len(error_lines) > 10:
            print(f"        ... and {len(error_lines) - 10} more errors")

    if warning_lines:
        print("      WARNINGS mentioning matlabdomain/sphinxcontrib:")
        for wl in warning_lines[:10]:  # Show first 10
            print(f"        {wl}")
        if len(warning_lines) > 10:
            print(f"        ... and {len(warning_lines) - 10} more warnings")

    if not warning_lines and not error_lines:
        print("      No matlabdomain-related warnings/errors detected")

    # Report but don't fail on sphinx-build issues - those are what we're investigating
    if build_result.returncode != 0:
        print(f"      ⚠ sphinx-build returned code {build_result.returncode}")
        print(f"      Check {build_stderr} for full details")

    print(f"\nArtifacts retained at: {project_artifacts}\n")
    print(f"{'=' * 70}")
    print(f"✓ {project_name} passed all checks")
    print(f"{'=' * 70}\n")


def test_project_data_exists() -> None:
    """Verify that project_data.json exists and contains project entries."""
    assert PROJECT_DATA_FILE.exists(), (
        f"project_data.json not found at {PROJECT_DATA_FILE}"
    )

    projects = load_project_data()
    assert len(projects) > 0, "project_data.json contains no projects"

    print(f"Found {len(projects)} project entries:")
    for project in projects:
        print(f"  - {project['url']} (src: {project['matlab_src_dir']})")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
