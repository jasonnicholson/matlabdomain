import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_DATA = Path(__file__).resolve().parent / "test_data"


def _copy_samples(src_root: Path, dest_root: Path, relatives):
    for rel in relatives:
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_root / rel, dest)


def _run_apidoc(source: Path, output: Path, max_files: int = 50):
    cmd = [
        sys.executable,
        "-m",
        "sphinxcontrib.sphinx_matlab_apidoc",
        str(source),
        "-o",
        str(output),
        "--max-files",
        str(max_files),
        "--force",
    ]
    subprocess.run(cmd, check=True, cwd=PROJECT_ROOT)


def test_namespace_paging_and_sections(tmp_path):
    src_dir = tmp_path / "src"
    out_dir = tmp_path / "out"
    src_dir.mkdir()

    # Use existing test data to simulate namespaced structure
    samples = [
        Path("+package/package_func.m"),
        Path("@ClassFolder/ClassFolder.m"),
        Path("@ClassFolder/classMethod.m"),
        Path("@ClassFolder/a_static_func.m"),
        Path("ClassExample.m"),
        Path("f_example.m"),
    ]
    _copy_samples(TEST_DATA, src_dir, samples)

    _run_apidoc(src_dir, out_dir, max_files=2)

    index_text = (out_dir / "index.rst").read_text(encoding="utf-8")
    assert "global_namespace" in index_text or "package" in index_text

    # Check that some namespace pages were created
    rst_files = list(out_dir.glob("*.rst"))
    assert len(rst_files) > 1  # Should have index.rst plus namespace pages

    # Check for package namespace content
    package_pages = [f for f in rst_files if "package" in f.name.lower()]
    if package_pages:
        package_content = package_pages[0].read_text(encoding="utf-8")
        assert "package" in package_content.lower()


def test_handles_underscored_folder(tmp_path):
    src_dir = tmp_path / "src"
    out_dir = tmp_path / "out"
    src_dir.mkdir()

    # Place test file inside a leading-underscore folder to ensure we keep the name
    dest = src_dir / "_folder" / "files" / "f_example.m"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEST_DATA / "f_example.m", dest)

    _run_apidoc(src_dir, out_dir, max_files=10)

    page = (out_dir / "_folder_files.rst").read_text(encoding="utf-8")
    assert "_folder.files" in page
    # module name should retain leading underscore
    assert "_folder.files.f_example" in page
