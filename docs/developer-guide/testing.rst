=======
Testing
=======

This guide covers the testing strategy and how to write and run tests for sphinxcontrib-matlabdomain.

Test Organization
=================

The project uses **pytest** for testing with the following structure:

.. code-block:: text

   tests/
   ├── test_*.py                    # Unit tests
   ├── roots/                       # Sphinx test configurations
   │   └── test-*/                  # Each integration test
   │       ├── conf.py              # Sphinx config
   │       ├── index.rst            # Test documentation
   │       └── src/                 # MATLAB test files
   ├── helper.py                    # Test utilities
   └── conftest.py                  # Pytest configuration

   test_slow/
   ├── test_integration.py          # Slow integration tests
   ├── conftest.py
   └── project_data.json            # Test project metadata

Test Categories
===============

Unit Tests (Fast)
-----------------

**Location:** ``tests/test_*.py``

**Purpose:** Test individual components in isolation

**Examples:**

* ``test_parse_mfile.py`` - Function/class parsing
* ``test_lexer.py`` - Syntax highlighting
* ``test_autodoc.py`` - Autodoc functionality
* ``test_classfolder.py`` - Class folder handling

**Run:** ``pytest tests/``

Integration Tests (Slow)
-------------------------

**Location:** ``test_slow/``

**Purpose:** Test complete documentation builds with real projects

**Run:** ``pytest test_slow/``

Sphinx Tests
------------

**Location:** ``tests/roots/test-*/``

**Purpose:** Test Sphinx integration with different configurations

**Structure:** Each test has its own Sphinx project

Running Tests
=============

All Tests
---------

.. code-block:: bash

   pytest

Fast Tests Only
---------------

.. code-block:: bash

   pytest tests/

Slow Tests Only
---------------

.. code-block:: bash

   pytest test_slow/

Specific Test File
------------------

.. code-block:: bash

   pytest tests/test_parse_mfile.py

Specific Test Function
----------------------

.. code-block:: bash

   pytest tests/test_parse_mfile.py::test_function_docstring

With Coverage
-------------

.. code-block:: bash

   pytest --cov=sphinxcontrib --cov-report=html

   # View coverage report
   open htmlcov/index.html

Verbose Output
--------------

.. code-block:: bash

   pytest -v

Stop on First Failure
---------------------

.. code-block:: bash

   pytest -x

Parallel Execution
------------------

.. code-block:: bash

   pytest -n auto

Writing Tests
=============

Basic Test Structure
--------------------

.. code-block:: python

   """Tests for MATLAB function parsing."""

   import pytest
   from pathlib import Path
   from sphinxcontrib.mat_types import MatFunction


   def test_simple_function():
       """Test parsing a simple function."""
       func = MatFunction.from_file("tests/test_data/simple.m")
       assert func.name == "simple"
       assert len(func.args) == 1


   def test_function_with_docstring():
       """Test function with complete docstring."""
       func = MatFunction.from_file("tests/test_data/documented.m")
       assert func.docstring
       assert "Args:" in func.docstring
       assert "Returns:" in func.docstring


   @pytest.mark.parametrize("filename,expected_name", [
       ("func1.m", "func1"),
       ("func2.m", "func2"),
   ])
   def test_multiple_functions(filename, expected_name):
       """Test multiple functions with parametrize."""
       func = MatFunction.from_file(f"tests/test_data/{filename}")
       assert func.name == expected_name

Using Fixtures
--------------

.. code-block:: python

   import pytest
   from pathlib import Path


   @pytest.fixture
   def test_data_dir():
       """Provide path to test data directory."""
       return Path(__file__).parent / "test_data"


   @pytest.fixture
   def simple_function(test_data_dir):
       """Provide a simple parsed function."""
       return MatFunction.from_file(test_data_dir / "simple.m")


   def test_with_fixture(simple_function):
       """Test using fixture."""
       assert simple_function.name == "simple"

Testing with Sphinx
--------------------

.. code-block:: python

   import pytest
   from sphinx.testing.util import SphinxTestApp


   @pytest.mark.sphinx('html', testroot='basic')
   def test_sphinx_build(app, status, warning):
       """Test a complete Sphinx build."""
       app.build()

       # Check build succeeded
       assert app.statuscode == 0

       # Check no warnings
       assert not warning.getvalue()

       # Check output files
       html_file = app.outdir / 'index.html'
       assert html_file.exists()

Testing Error Handling
----------------------

.. code-block:: python

   import pytest
   from sphinxcontrib.mat_types import MatFunction


   def test_invalid_file():
       """Test error handling for invalid file."""
       with pytest.raises(FileNotFoundError):
           MatFunction.from_file("nonexistent.m")


   def test_malformed_syntax():
       """Test handling of syntax errors."""
       with pytest.raises(ValueError, match="Invalid MATLAB syntax"):
           MatFunction.from_string("function incomplete")

Test Data Organization
======================

MATLAB Test Files
-----------------

Create MATLAB test files in ``tests/test_data/``:

.. code-block:: matlab

   % tests/test_data/example.m
   function result = example(x, y)
   % EXAMPLE An example function for testing
   %
   % Args:
   %     x (double): First input
   %     y (double): Second input
   %
   % Returns:
   %     double: Sum of inputs

   result = x + y;
   end

Then test it:

.. code-block:: python

   def test_example():
       func = MatFunction.from_file("tests/test_data/example.m")
       assert func.name == "example"
       assert len(func.args) == 2

Sphinx Test Roots
------------------

Create a Sphinx test configuration in ``tests/roots/test-myfeature/``:

.. code-block:: text

   tests/roots/test-myfeature/
   ├── conf.py
   ├── index.rst
   └── src/
       └── myfile.m

**conf.py:**

.. code-block:: python

   extensions = ['sphinxcontrib.matlab']
   matlab_src_dir = 'src'

**index.rst:**

.. code-block:: rst

   Test My Feature
   ===============

   .. autofunction:: myfile.myfunction

Testing Best Practices
=======================

1. **Test one thing per test**

   Each test should verify one specific behavior.

2. **Use descriptive names**

   .. code-block:: python

      def test_function_with_multiple_return_values():
          # Clear what's being tested

3. **Arrange-Act-Assert pattern**

   .. code-block:: python

      def test_something():
          # Arrange: Setup
          func = create_function()

          # Act: Execute
          result = func.process()

          # Assert: Verify
          assert result == expected

4. **Test edge cases**

   * Empty inputs
   * Large inputs
   * Invalid inputs
   * Boundary conditions

5. **Use pytest.mark for organization**

   .. code-block:: python

      @pytest.mark.slow
      def test_large_project():
          pass

      @pytest.mark.windows
      def test_windows_specific():
          pass

Coverage Goals
==============

Aim for:

* **Overall:** >80% coverage
* **Critical paths:** >90% coverage
* **New code:** 100% coverage

Check coverage:

.. code-block:: bash

   pytest --cov=sphinxcontrib --cov-report=term-missing

This shows which lines aren't covered.

Continuous Integration
======================

GitHub Actions
--------------

Tests run automatically on:

* Push to main branch
* Pull requests
* Multiple Python versions (3.8, 3.9, 3.10, 3.11)
* Multiple Sphinx versions
* Multiple operating systems (Ubuntu, Windows, macOS)

Configuration: ``.github/workflows/python-package.yml``

Running CI Locally
------------------

Approximate CI environment with tox:

.. code-block:: bash

   # Install tox
   pip install tox

   # Run all test environments
   tox

   # Run specific Python version
   tox -e py310

   # Run specific Sphinx version
   tox -e py38-sphinx40

Debugging Failing Tests
========================

Verbose Output
--------------

.. code-block:: bash

   pytest -vv

Show Print Statements
---------------------

.. code-block:: bash

   pytest -s

Debug on Failure
----------------

.. code-block:: bash

   pytest --pdb

Show Local Variables
--------------------

.. code-block:: bash

   pytest -l

Rerun Failed Tests
------------------

.. code-block:: bash

   pytest --lf  # last failed

Test Maintenance
================

Updating Test Data
------------------

When updating MATLAB test files:

1. Update the ``.m`` file in ``tests/test_data/``
2. Run affected tests
3. Update test assertions if needed

Updating Baselines
------------------

For snapshot/golden tests:

1. Verify changes are correct
2. Update baseline files
3. Document changes in commit message

Removing Obsolete Tests
------------------------

When removing features:

1. Remove related tests
2. Clean up test data
3. Update test documentation

Common Test Patterns
====================

Testing Parsers
---------------

.. code-block:: python

   def test_parse_function():
       code = """
       function y = f(x)
           y = x * 2;
       end
       """
       func = MatFunction.from_string(code)
       assert func.name == "f"

Testing Documenters
-------------------

.. code-block:: python

   @pytest.mark.sphinx('html', testroot='autodoc')
   def test_autofunction(app):
       app.build()
       content = (app.outdir / 'index.html').read_text()
       assert 'function signature' in content

Testing Links
-------------

.. code-block:: python

   def test_cross_reference():
       # Build docs
       app.build()

       # Check link exists
       html = (app.outdir / 'index.html').read_text()
       assert '<a href="other.html#MyClass">' in html

See Also
========

* :doc:`contributing` - Contribution workflow
* :doc:`quick-reference` - Testing commands
* :doc:`architecture` - Understanding the codebase
* `pytest documentation <https://docs.pytest.org/>`_
