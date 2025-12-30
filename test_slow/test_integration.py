#!/usr/bin/env python3
"""
Integration tests for sphinxcontrib-matlabdomain.

These tests validate the matlabdomain plugin against real-world MATLAB projects
by cloning them and generating Sphinx documentation. They are designed to run
infrequently (e.g., in nightly builds) as they are slow and require network access.
Projects and their MATLAB source directories are defined in project_data.json.

To run these tests:
    pytest test_slow/test_integration.py -v -s

To run only a specific project (filter by repo name or URL substring):
    pytest test_slow/test_integration.py -v -s -k "matnwb"
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List

import pytest

# Get the test_slow directory
TEST_SLOW_DIR = Path(__file__).resolve().parent
PROJECT_DATA_FILE = TEST_SLOW_DIR / "project_data.json"


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


def clone_repository(url: str, target_dir: Path) -> Path:
    """Clone a repository with --filter=blob:none for shallow cloning."""
    project_name = extract_project_name(url)
    clone_path = target_dir / project_name

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

    with tempfile.TemporaryDirectory(prefix=f"matlab_test_{project_name}_") as tmpdir:
        temp_path = Path(tmpdir)

        print(f"\n{'=' * 70}")
        print(f"Testing project: {project_name}")
        print(f"URL: {url}")
        print(f"{'=' * 70}\n")

        # Clone the repository
        print(f"[1/3] Cloning repository...")
        project_dir = clone_repository(url, temp_path)
        print(f"      ✓ Cloned to {project_dir}")

        # Use configured MATLAB source directory
        print(f"[2/3] Locating MATLAB source directory (configured)...")
        matlab_source = (project_dir / matlab_src_rel).resolve()
        if not matlab_source.exists():
            pytest.skip(f"Configured MATLAB source dir not found: {matlab_source}")
        matlab_count = sum(1 for _ in matlab_source.rglob("*.m"))
        print(f"      ✓ Found {matlab_count} MATLAB files in {matlab_source}")

        if matlab_count == 0:
            pytest.skip(f"No MATLAB files found in {project_name}")

        # Generate documentation with sphinx-matlab-apidoc
        print(f"[3/3] Generating documentation with sphinx-matlab-apidoc...")
        docs_source = temp_path / "docs" / "source"

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

        print(f"\n{'=' * 70}")
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
