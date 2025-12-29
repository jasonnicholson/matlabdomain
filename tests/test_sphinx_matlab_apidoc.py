import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_PROJECTS = PROJECT_ROOT / "test_projects"


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


@pytest.mark.skipif(not TEST_PROJECTS.exists(), reason="test_projects missing")
def test_namespace_paging_and_sections(tmp_path):
    src_dir = tmp_path / "src"
    out_dir = tmp_path / "out"
    src_dir.mkdir()

    project = TEST_PROJECTS / "vhlab-toolbox-matlab"
    samples = [
        Path("+vlt/+data/assign.m"),
        Path("+vlt/+data/cache.m"),
        Path("+vlt/+data/catCellStr.m"),
        Path("datastructures/@struct/eq.m"),
        Path("vlt_Init.m"),
    ]
    _copy_samples(project, src_dir, samples)

    _run_apidoc(src_dir, out_dir, max_files=2)

    index_text = (out_dir / "index.rst").read_text(encoding="utf-8")
    assert "global_namespace" in index_text
    assert "vlt_data_1" in index_text
    assert "vlt_data_2" in index_text

    global_page = (out_dir / "global_namespace.rst").read_text(encoding="utf-8")
    assert "Global Namespace" in global_page
    assert ".. contents:: Table of Contents" in global_page
    assert ".. mat:autofunction:: vlt_Init" in global_page

    vlt_page1 = (out_dir / "vlt_data_1.rst").read_text(encoding="utf-8")
    assert "vlt.data Namespace" in vlt_page1
    assert ".. mat:autoclass:: vlt.data.cache" in vlt_page1
    assert ".. mat:autofunction:: vlt.data.assign" in vlt_page1

    vlt_page2 = (out_dir / "vlt_data_2.rst").read_text(encoding="utf-8")
    assert "vlt.data Namespace" in vlt_page2
    assert ".. mat:autofunction:: vlt.data.catCellStr" in vlt_page2

    class_page = (out_dir / "datastructures_struct.rst").read_text(encoding="utf-8")
    assert "datastructures.struct Namespace" in class_page
    assert ".. mat:autofunction:: datastructures.@struct.eq" in class_page


@pytest.mark.skipif(not TEST_PROJECTS.exists(), reason="test_projects missing")
def test_handles_underscored_folder(tmp_path):
    src_dir = tmp_path / "src"
    out_dir = tmp_path / "out"
    src_dir.mkdir()

    project = TEST_PROJECTS / "vhlab-toolbox-matlab"
    sample = Path("+vlt/+data/assign.m")
    # Place inside a leading-underscore folder to ensure we keep the name
    dest = src_dir / "_folder" / "files" / sample.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(project / sample, dest)

    _run_apidoc(src_dir, out_dir, max_files=10)

    page = (out_dir / "_folder_files.rst").read_text(encoding="utf-8")
    assert "_folder.files Namespace" in page
    # module name should retain leading underscore
    assert ".. mat:autofunction:: _folder.files.assign" in page
