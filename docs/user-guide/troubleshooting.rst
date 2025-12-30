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
