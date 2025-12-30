============
Contributing
============

Thank you for your interest in contributing to sphinxcontrib-matlabdomain!
This guide will help you get started.

Development Setup
=================

Prerequisites
-------------

* Python 3.8 or higher
* Git
* A code editor (VS Code recommended)

Clone the Repository
--------------------

.. code-block:: bash

   git clone https://github.com/sphinx-contrib/matlabdomain.git
   cd matlabdomain

Create Virtual Environment
---------------------------

.. code-block:: bash

   # Create virtual environment
   python -m venv .venv

   # Activate it (Linux/macOS)
   source .venv/bin/activate

   # Activate it (Windows)
   .venv\Scripts\activate

Install Dependencies
--------------------

.. code-block:: bash

   # Install development dependencies
   pip install -r dev-requirements.txt

   # Install documentation dependencies
   pip install -r rtd-requirements.txt

   # Install package in editable mode
   pip install -e .

Install Pre-commit Hooks
-------------------------

.. code-block:: bash

   pre-commit install

This ensures code quality checks run before each commit.

Verify Installation
-------------------

.. code-block:: bash

   # Run tests
   pytest

   # Build documentation
   cd docs && make html && cd ..

If everything passes, you're ready to contribute!

Development Workflow
====================

1. Create a Branch
------------------

.. code-block:: bash

   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description

2. Make Changes
---------------

Edit code, add tests, update documentation as needed.

3. Run Tests
------------

.. code-block:: bash

   # Run all tests
   pytest

   # Run specific test file
   pytest tests/test_parse_mfile.py

   # Run with coverage
   pytest --cov=sphinxcontrib --cov-report=html

4. Check Code Quality
---------------------

.. code-block:: bash

   # Lint and format (pre-commit does this automatically)
   pre-commit run --all-files

5. Commit Changes
-----------------

.. code-block:: bash

   git add .
   git commit -m "feat: add new feature"

   # Or for bug fixes
   git commit -m "fix: resolve issue with class parsing"

**Commit Message Convention:**

* ``feat:`` - New feature
* ``fix:`` - Bug fix
* ``docs:`` - Documentation changes
* ``test:`` - Test additions/changes
* ``refactor:`` - Code refactoring
* ``chore:`` - Maintenance tasks

6. Push and Create Pull Request
--------------------------------

.. code-block:: bash

   git push origin feature/your-feature-name

Then create a pull request on GitHub.

Code Style
==========

We use **ruff** for code formatting and linting.

Formatting Rules
----------------

* **Indentation:** 4 spaces
* **Line length:** 88 characters (Black style)
* **Quotes:** Double quotes preferred
* **Import sorting:** Automatic via ruff

Example:

.. code-block:: python

   """Module docstring."""

   import os
   from pathlib import Path

   from sphinx.util import logging

   logger = logging.getLogger(__name__)


   class MyClass:
       """Class docstring.

       Args:
           param: Description of parameter.
       """

       def __init__(self, param):
           self.param = param

       def method(self):
           """Method docstring."""
           return self.param * 2

Documentation Style
-------------------

* **Docstrings:** Google style or NumPy style
* **Comments:** Explain *why*, not *what*
* **Type hints:** Use where helpful, but not required

Testing Guidelines
==================

Writing Tests
-------------

1. **Create test file:** ``tests/test_yourfeature.py``
2. **Use pytest fixtures** for setup
3. **Test edge cases** and error handling
4. **Aim for high coverage** (>80%)

Test Structure:

.. code-block:: python

   import pytest
   from sphinxcontrib.mat_types import MatFunction


   def test_function_parsing():
       """Test basic function parsing."""
       func = MatFunction.from_file("path/to/function.m")
       assert func.name == "function_name"
       assert len(func.args) == 2


   def test_function_with_no_args():
       """Test function without arguments."""
       func = MatFunction.from_file("path/to/no_args.m")
       assert func.args == []


   def test_invalid_function():
       """Test error handling for invalid function."""
       with pytest.raises(ValueError):
           MatFunction.from_file("invalid.m")

Running Tests
-------------

.. code-block:: bash

   # All tests
   pytest

   # Specific test file
   pytest tests/test_parse_mfile.py

   # Specific test function
   pytest tests/test_parse_mfile.py::test_function_name

   # With verbose output
   pytest -v

   # With coverage
   pytest --cov=sphinxcontrib --cov-report=html

   # Stop on first failure
   pytest -x

Test Organization
-----------------

.. code-block:: text

   tests/
   ├── test_*.py              # Unit tests
   ├── roots/                 # Integration test configurations
   │   └── test-*/
   │       ├── conf.py
   │       ├── index.rst
   │       └── src/           # MATLAB test files
   └── helper.py              # Test utilities

Documentation Contributions
============================

Documentation is just as important as code!

Building Documentation
----------------------

.. code-block:: bash

   cd docs
   make html

   # View in browser (Linux)
   xdg-open _build/html/index.html

   # View in browser (macOS)
   open _build/html/index.html

   # View in browser (Windows)
   start _build/html/index.html

Adding New Pages
----------------

1. Create ``.rst`` file in appropriate directory
2. Add to ``toctree`` in ``index.rst`` or parent page
3. Write content in reStructuredText format
4. Build and verify

Documentation Structure:

.. code-block:: text

   docs/
   ├── getting-started/       # Tutorials for new users
   ├── user-guide/            # Feature documentation
   ├── developer-guide/       # Contributing guides
   └── reference/             # API reference

ReStructuredText Tips
---------------------

**Headings:**

.. code-block:: rst

   =======
   Title
   =======

   Section
   =======

   Subsection
   ----------

   Subsubsection
   ^^^^^^^^^^^^^

**Code blocks:**

.. code-block:: rst

   .. code-block:: python

      def hello():
          print("Hello!")

**Links:**

.. code-block:: rst

   :doc:`page-name`
   :ref:`section-label`
   `External link <https://example.com>`_

Pull Request Guidelines
=======================

Before Submitting
-----------------

✅ **Checklist:**

* [ ] Tests pass (``pytest``)
* [ ] Code is formatted (``pre-commit run --all-files``)
* [ ] Documentation is updated
* [ ] CHANGES.rst is updated (for features/fixes)
* [ ] Commit messages follow convention

PR Description
--------------

Include:

* **What:** Brief description of changes
* **Why:** Motivation and context
* **How:** Implementation approach
* **Testing:** How you tested the changes
* **Screenshots:** For UI changes (if applicable)

Template:

.. code-block:: markdown

   ## Description
   Brief summary of changes

   ## Motivation
   Why this change is needed

   ## Changes
   - Added X
   - Fixed Y
   - Updated Z

   ## Testing
   How to verify the changes work

   ## Checklist
   - [x] Tests pass
   - [x] Documentation updated
   - [x] CHANGES.rst updated

Review Process
--------------

1. Automated checks run (GitHub Actions)
2. Maintainer reviews code
3. Feedback and discussion
4. Approval and merge

Reporting Issues
================

Found a Bug?
------------

`Create an issue <https://github.com/sphinx-contrib/matlabdomain/issues/new>`_ with:

* **Title:** Clear, descriptive
* **Description:** What happened vs. what you expected
* **Reproduction:** Minimal example to reproduce
* **Environment:** Python version, Sphinx version, OS
* **Error messages:** Full error output

Template:

.. code-block:: markdown

   ## Bug Description
   Clear description of the bug

   ## To Reproduce
   1. Configure conf.py with...
   2. Run sphinx-build...
   3. See error

   ## Expected Behavior
   What should happen

   ## Environment
   - Python: 3.10
   - Sphinx: 6.2.1
   - sphinxcontrib-matlabdomain: 0.22.0
   - OS: Ubuntu 22.04

   ## Error Output
   ```
   Paste error here
   ```

Feature Request?
----------------

`Create an issue <https://github.com/sphinx-contrib/matlabdomain/issues/new>`_ with:

* **Title:** Feature: description
* **Use case:** Why you need this
* **Proposed solution:** How it might work
* **Alternatives:** Other approaches considered

Getting Help
============

* **GitHub Issues:** For bugs and feature requests
* **GitHub Discussions:** For questions and ideas
* **Documentation:** Check :doc:`../user-guide/troubleshooting`

Code of Conduct
===============

* **Be respectful** and inclusive
* **Be patient** with beginners
* **Give constructive feedback**
* **Focus on the issue**, not the person
* **Assume good intentions**

See Also
========

* :doc:`architecture` - Understand the codebase
* :doc:`testing` - Testing strategy details
* :doc:`known-issues` - Current limitations
* :doc:`quick-reference` - Command cheat sheet
