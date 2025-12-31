===============
Troubleshooting
===============

Common issues and their solutions.

Installation Issues
===================

Package Not Found
-----------------

**Symptom:** ``pip install sphinxcontrib-matlabdomain`` fails

**Solution:**

.. code-block:: bash

   pip install --upgrade pip
   pip install sphinxcontrib-matlabdomain

Configuration Issues
====================

matlab_src_dir Not Found
-------------------------

**Symptom:** Warning: "matlab_src_dir not set" or "directory not found"

**Solution:** Check your ``conf.py``:

.. code-block:: python

   import os
   this_dir = os.path.dirname(os.path.abspath(__file__))
   matlab_src_dir = os.path.abspath(os.path.join(this_dir, '..', 'src'))

   # Debug: print the path
   print(f"Looking for MATLAB sources in: {matlab_src_dir}")

Extension Not Loading
---------------------

**Symptom:** Extension not recognized

**Solution:** Verify installation:

.. code-block:: bash

   pip show sphinxcontrib-matlabdomain
   python -c "import sphinxcontrib.matlab; print('OK')"

Build Issues
============

Functions Not Appearing
-----------------------

**Symptom:** ``autofunction`` directive produces no output

**Possible causes:**

1. File not in ``matlab_src_dir``
2. Typo in function name (case-sensitive)
3. Need to rebuild: ``make clean && make html``

Classes Not Showing Members
----------------------------

**Symptom:** Class documented but no methods/properties shown

**Solution:** Add ``:members:`` option:

.. code-block:: rst

   .. autoclass:: MyClass
      :members:
      :undoc-members:

Build Warnings
--------------

**Symptom:** Warnings during build

**Solutions:**

* Read the warning message carefully
* Check file paths and names
* Verify MATLAB syntax is valid
* Run ``make clean && make html``

Folders Starting with Underscore Not Found
-------------------------------------------

**Symptom:** MATLAB files in folders starting with ``_`` are not being documented

**Cause:** Sphinx follows Python package naming conventions where folders starting
with ``_`` are typically treated as private/internal and may be excluded by default.

**Solutions:**

1. **Rename folders** to not start with underscore (recommended):

   .. code-block:: text

      Before: src/_internal/myfile.m
      After:  src/internal/myfile.m

2. **Update exclude_patterns** in ``conf.py`` if the folder is being excluded:

   .. code-block:: python

      # Default excludes _build, etc.
      exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

Python Package Naming Rules
----------------------------

**Important:** sphinxcontrib-matlabdomain uses Python import mechanisms internally,
which means it follows Python naming conventions:

* **Folders starting with** ``_`` may be treated as private
* **Folders with** ``-`` (hyphen) won't work - use ``_`` (underscore) instead for
  multi-word names
* **Module names** must be valid Python identifiers

**Best practices:**

* Use alphanumeric folder names: ``utils``, ``helpers``, ``core``
* For MATLAB packages, use the ``+`` prefix: ``+mypackage``
* For MATLAB class folders, use the ``@`` prefix: ``@MyClass``
* Avoid special characters in folder/file names except ``+`` and ``@``
* Don't use a number or symbol as the first character of a folder name

What'll notice here is these rules are very similar to MATLAB's own naming conventions for
packages, classes, and variables. When you deviate, it may work but can lead to unexpected
and hard to debug issues.

**Example structure that works well:**

.. code-block:: text

   src/
   ├── utilities.m           # Simple function
   ├── +mypackage/           # MATLAB package (note the +)
   │   ├── helper.m
   │   └── validator.m
   ├── @MyClass/             # MATLAB class folder (note the @)
   │   └── MyClass.m
   └── submodule/            # Regular folder (no underscore prefix)
       └── tools.m

Getting Help
============

If you're still stuck:

1. Check :doc:`configuration` for correct settings
2. Search `GitHub Issues <https://github.com/sphinx-contrib/matlabdomain/issues>`_
3. Create a new issue with:

   * Your ``conf.py``
   * Example MATLAB file
   * Full error message
   * Python/Sphinx versions

See Also
========

* :doc:`configuration` - Configuration reference
* :doc:`../getting-started/installation` - Installation guide
* `GitHub Issues <https://github.com/sphinx-contrib/matlabdomain/issues>`_

.. note::
   This page will be expanded with more troubleshooting scenarios.
