===============
Quick Reference
===============

Essential commands and workflows for development. Bookmark this page!

Common Commands
===============

Setup
-----

.. code-block:: bash

   # Clone repository
   git clone https://github.com/sphinx-contrib/matlabdomain.git
   cd matlabdomain

   # Create virtual environment
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate      # Windows

   # Install dependencies
   pip install -r dev-requirements.txt
   pip install -r rtd-requirements.txt
   pip install -e .

   # Install pre-commit hooks
   pre-commit install

Testing
-------

.. code-block:: bash

   # Run all tests
   pytest

   # Run specific test file
   pytest tests/test_parse_mfile.py

   # Run specific test
   pytest tests/test_parse_mfile.py::test_function_name

   # With coverage
   pytest --cov=sphinxcontrib --cov-report=html

   # Verbose output
   pytest -v

   # Stop on first failure
   pytest -x

   # Run slow integration tests
   pytest tests/ test_slow/

Code Quality
------------

.. code-block:: bash

   # Run all pre-commit checks
   pre-commit run --all-files

   # Lint and format
   ruff check .
   ruff format .

   # Type check (if mypy configured)
   mypy sphinxcontrib/

Documentation
-------------

.. code-block:: bash

   # Build HTML docs
   cd docs && make html && cd ..

   # Clean build
   cd docs && make clean && make html && cd ..

   # View docs (Linux)
   xdg-open docs/_build/html/index.html

   # View docs (macOS)
   open docs/_build/html/index.html

   # View docs (Windows)
   start docs/_build/html/index.html

Git Workflow
------------

.. code-block:: bash

   # Create feature branch
   git checkout -b feature/my-feature

   # Make changes, then
   git add .
   git commit -m "feat: add new feature"

   # Push to GitHub
   git push origin feature/my-feature

Key Files Reference
===================

Source Code
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - File
     - Purpose
   * - ``sphinxcontrib/matlab.py``
     - Main domain implementation, roles, directives
   * - ``sphinxcontrib/mat_types.py``
     - MATLAB type definitions (Class, Function, etc.)
   * - ``sphinxcontrib/mat_documenters.py``
     - Autodoc documenters for extracting docs
   * - ``sphinxcontrib/mat_directives.py``
     - Autodoc directive implementations
   * - ``sphinxcontrib/mat_tree_sitter_parser.py``
     - AST parser using tree-sitter
   * - ``sphinxcontrib/mat_lexer.py``
     - Syntax highlighting lexer

Configuration
-------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - File
     - Purpose
   * - ``pyproject.toml``
     - Project metadata, tool configs (ruff, pytest, etc.)
   * - ``setup.py``
     - Package installation configuration
   * - ``pytest.ini``
     - pytest configuration
   * - ``tox.ini``
     - Testing across multiple Python/Sphinx versions
   * - ``.pre-commit-config.yaml``
     - Pre-commit hook configuration
   * - ``docs/conf.py``
     - Sphinx documentation configuration

Dependencies
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - File
     - Purpose
   * - ``dev-requirements.txt``
     - Development dependencies (pytest, ruff, etc.)
   * - ``rtd-requirements.txt``
     - ReadTheDocs build requirements
   * - ``setup.py``
     - Package dependencies (install_requires)

Common Workflows
================

Adding a New Feature
--------------------

1. Create branch: ``git checkout -b feature/my-feature``
2. Write code in ``sphinxcontrib/``
3. Add tests in ``tests/test_myfeature.py``
4. Run tests: ``pytest``
5. Update documentation in ``docs/``
6. Update ``CHANGES.rst``
7. Commit: ``git commit -m "feat: description"``
8. Push and create PR

Fixing a Bug
------------

1. Create branch: ``git checkout -b fix/issue-description``
2. Write failing test that reproduces the bug
3. Fix the bug in ``sphinxcontrib/``
4. Verify test passes: ``pytest``
5. Update ``CHANGES.rst``
6. Commit: ``git commit -m "fix: description"``
7. Push and create PR

Adding Documentation
--------------------

1. Create ``.rst`` file in appropriate ``docs/`` subdirectory
2. Add to ``toctree`` in parent page
3. Write content in reStructuredText
4. Build: ``cd docs && make html``
5. Review in browser
6. Commit and push

Reviewing a PR
--------------

1. Checkout PR branch: ``git fetch origin && git checkout pr-branch``
2. Install: ``pip install -e .``
3. Run tests: ``pytest``
4. Build docs: ``cd docs && make html``
5. Review code changes
6. Test manually if needed
7. Leave feedback on GitHub

Important Configuration Settings
================================

conf.py (Sphinx)
----------------

.. code-block:: python

   # Essential MATLAB configuration
   extensions = ['sphinxcontrib.matlab', 'sphinx.ext.autodoc']
   matlab_src_dir = '/path/to/matlab/src'
   primary_domain = 'mat'

   # Optional enhancements
   matlab_short_links = True
   matlab_auto_link = 'basic'
   matlab_show_property_default_values = True

pyproject.toml
--------------

.. code-block:: toml

   [tool.ruff]
   line-length = 88
   target-version = "py38"

   [tool.pytest.ini_options]
   testpaths = ["tests"]
   python_files = "test_*.py"

Troubleshooting Quick Fixes
============================

Tests Failing
-------------

.. code-block:: bash

   # Clean and reinstall
   pip uninstall sphinxcontrib-matlabdomain
   pip install -e .
   pytest

Import Errors
-------------

.. code-block:: bash

   # Verify environment
   which python
   pip list | grep sphinx

   # Reinstall in editable mode
   pip install -e .

Pre-commit Failing
------------------

.. code-block:: bash

   # Update hooks
   pre-commit autoupdate

   # Run manually
   pre-commit run --all-files

Documentation Not Building
--------------------------

.. code-block:: bash

   # Clean build
   cd docs
   make clean
   make html

CI Failing on GitHub
--------------------

* Check ``.github/workflows/python-package.yml``
* Run same commands locally
* Ensure all tests pass locally first

Useful Links
============

* **Repository:** https://github.com/sphinx-contrib/matlabdomain
* **Issues:** https://github.com/sphinx-contrib/matlabdomain/issues
* **Documentation:** https://sphinxcontrib-matlabdomain.readthedocs.io/
* **PyPI:** https://pypi.org/project/sphinxcontrib-matlabdomain/
* **Sphinx Docs:** https://www.sphinx-doc.org/

Code Snippets
=============

Testing a MATLAB Function
--------------------------

.. code-block:: python

   from sphinxcontrib.mat_types import MatFunction

   # Parse a MATLAB file
   func = MatFunction.from_file("path/to/function.m")
   print(func.name)
   print(func.args)
   print(func.docstring)

Creating a Test
---------------

.. code-block:: python

   import pytest
   from sphinxcontrib.mat_types import MatClass

   def test_class_parsing():
       cls = MatClass.from_file("MyClass.m")
       assert cls.name == "MyClass"
       assert len(cls.methods) > 0

Debugging Sphinx Build
----------------------

.. code-block:: python

   # In conf.py, add logging
   import logging
   logging.basicConfig(level=logging.DEBUG)

Environment Variables
=====================

Useful environment variables:

.. code-block:: bash

   # Set MATLAB source directory
   export MATLAB_SRC_DIR=/path/to/matlab

   # Python debugging
   export PYTHONVERBOSE=1

   # Pytest options
   export PYTEST_ADDOPTS="-v --tb=short"

See Also
========

* :doc:`architecture` - Understand the codebase
* :doc:`contributing` - Full contribution guide
* :doc:`testing` - Testing details
* :doc:`known-issues` - Current bugs and limitations
