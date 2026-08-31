"""Sphinx config for the SCM profiling harness (Phase 1 "before" profile).

Points `matlab_src_dir` at a large real MATLAB tree (~1700 .m files) so a build
reproduces the current lock-up: on `builder-inited`, `analyze()` eagerly walks
AND tree-sitter-parses every file before any doc is rendered.
"""

import os

_here = os.path.dirname(os.path.abspath(__file__))

project = "SCM profiling harness"
author = "SCM"
extensions = ["sphinx.ext.autodoc", "sphinxcontrib.matlab"]

# Largest bundled fixture: vhlab-toolbox-matlab (~1726 .m files).
matlab_src_dir = os.path.normpath(
    os.path.join(_here, "..", "artifacts", "vhlab-toolbox-matlab", "repo")
)

master_doc = "index"
exclude_patterns = ["_build"]
