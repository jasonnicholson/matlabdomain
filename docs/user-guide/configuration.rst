=============
Configuration
=============

This page documents all configuration options for sphinxcontrib-matlabdomain.

Essential Configuration
=======================

These settings are required for basic functionality.

extensions
----------

Add the MATLAB domain to your Sphinx extensions:

.. code-block:: python

   extensions = [
       'sphinx.ext.autodoc',
       'sphinxcontrib.matlab',
       'sphinx.ext.napoleon',  # Optional but recommended
   ]

matlab_src_dir
--------------

**Required**. Specify the path to your MATLAB source code:

.. code-block:: python

   import os

   # Absolute path
   matlab_src_dir = '/absolute/path/to/matlab/src'

   # Relative path (recommended)
   this_dir = os.path.dirname(os.path.abspath(__file__))
   matlab_src_dir = os.path.abspath(os.path.join(this_dir, '..', 'src'))

The extension searches this directory and all subdirectories for ``.m`` files.

.. note::
   Currently only one MATLAB path can be specified, but all subfolders in that tree will be searched.

Optional Configuration
======================

primary_domain
--------------

Make MATLAB the primary domain for convenience:

.. code-block:: python

   primary_domain = 'mat'

This allows you to write:

.. code-block:: rst

   .. autofunction:: myfunction

Instead of:

.. code-block:: rst

   .. mat:autofunction:: myfunction

**Default:** ``'py'`` (Python)

matlab_short_links
------------------

Shorten class, package, and function names to minimum length:

.. code-block:: python

   matlab_short_links = True

**Effect:**

* **False** (default): ``:class:`target.subfolder.ClassFoo```
* **True**: ``:class:`ClassFoo```

This assumes everything is in the path as in MATLAB, providing a more MATLAB-like presentation.

.. note::
   Setting this to ``True`` forces ``matlab_keep_package_prefix = False``.

**Default:** ``False``

**Added in:** Version 0.19.0

matlab_auto_link
----------------

Automatically convert known entity names to links:

.. code-block:: python

   matlab_auto_link = 'all'  # or 'basic'

**Options:**

* ``'basic'`` - Auto-links known entities in "See also" sections and standalone entity names
* ``'all'`` - Auto-links entities anywhere in docstrings
* ``None`` - No automatic linking (default)

**Example:**

With ``matlab_auto_link = 'basic'``:

.. code-block:: matlab

   % See also MyClass, myfunction

Automatically becomes clickable links to ``MyClass`` and ``myfunction``.

**Default:** ``None``

**Added in:** Version 0.21.0

matlab_keep_package_prefix
---------------------------

Control whether package prefixes (``+``) are displayed:

.. code-block:: python

   matlab_keep_package_prefix = True

**Effect:**

* **True**: Display as ``+mypackage.MyClass``
* **False**: Display as ``mypackage.MyClass``

**Default:** ``True``

.. note::
   This is automatically set to ``False`` when ``matlab_short_links = True``.

matlab_show_property_default_values
------------------------------------

Show default values for class properties:

.. code-block:: python

   matlab_show_property_default_values = True

**Effect:**

Shows property initialization values in class documentation.

**Default:** ``False``

**Added in:** Version 0.17.0

Example Complete Configuration
==============================

Here's a complete ``conf.py`` with common settings:

.. code-block:: python

   # Configuration file for the Sphinx documentation builder.
   import os

   # -- Project information -----------------------------------------------------
   project = 'MyMatlabProject'
   copyright = '2025, Your Name'
   author = 'Your Name'
   release = '1.0.0'

   # -- General configuration ---------------------------------------------------
   extensions = [
       'sphinx.ext.autodoc',
       'sphinxcontrib.matlab',
       'sphinx.ext.napoleon',
       'sphinx.ext.viewcode',      # Add links to source code
       'sphinx.ext.intersphinx',   # Link to other projects
   ]

   # MATLAB Configuration
   this_dir = os.path.dirname(os.path.abspath(__file__))
   matlab_src_dir = os.path.abspath(os.path.join(this_dir, '..', 'src'))
   primary_domain = 'mat'
   matlab_short_links = True
   matlab_auto_link = 'basic'
   matlab_show_property_default_values = True

   # Build configuration
   templates_path = ['_templates']
   exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

   # -- Options for HTML output -------------------------------------------------
   html_theme = 'sphinx_rtd_theme'
   html_static_path = ['_static']
   html_logo = '_static/logo.png'  # Optional

   # Theme options
   html_theme_options = {
       'navigation_depth': 4,
       'collapse_navigation': False,
   }

Configuration for Different Project Structures
===============================================

Single Directory
----------------

If all your MATLAB files are in one directory:

.. code-block:: python

   matlab_src_dir = os.path.abspath(os.path.join(this_dir, '..', 'matlab'))

Multiple Levels with Packages
------------------------------

If you have packages and classes in subdirectories:

.. code-block:: text

   src/
   ├── utilities.m
   ├── +mypackage/
   │   ├── helper.m
   │   └── +subpackage/
   │       └── tool.m
   └── @MyClass/
       └── MyClass.m

.. code-block:: python

   matlab_src_dir = os.path.abspath(os.path.join(this_dir, '..', 'src'))
   matlab_short_links = True

Documentation Next to Source
-----------------------------

If your docs are in the same directory as source:

.. code-block:: text

   project/
   ├── docs/
   │   └── conf.py
   └── src/
       └── *.m

.. code-block:: python

   matlab_src_dir = os.path.abspath(os.path.join(this_dir, '..', 'src'))

Separate Docs Project
----------------------

If documentation is in a completely separate repository:

.. code-block:: python

   # Use absolute path
   matlab_src_dir = '/path/to/matlab/project/src'

   # Or use environment variable
   import os
   matlab_src_dir = os.environ.get('MATLAB_SRC_DIR', '/default/path')

Advanced Configuration
======================

Napoleon Extension
------------------

Enable Google or NumPy style docstrings:

.. code-block:: python

   extensions = [
       'sphinx.ext.autodoc',
       'sphinxcontrib.matlab',
       'sphinx.ext.napoleon',
   ]

   # Napoleon settings
   napoleon_google_docstring = True
   napoleon_numpy_docstring = True
   napoleon_include_init_with_doc = True
   napoleon_use_param = True
   napoleon_use_rtype = True

Custom CSS
----------

Add custom styling:

.. code-block:: python

   html_static_path = ['_static']
   html_css_files = ['custom.css']

Create ``_static/custom.css`` for your styles.

Intersphinx Linking
-------------------

Link to other project documentation:

.. code-block:: python

   extensions = [
       # ... other extensions
       'sphinx.ext.intersphinx',
   ]

   intersphinx_mapping = {
       'python': ('https://docs.python.org/3', None),
       'numpy': ('https://numpy.org/doc/stable/', None),
   }

Troubleshooting Configuration
==============================

Configuration Not Working
-------------------------

1. **Restart the build** - Run ``make clean && make html``
2. **Check syntax** - Python is whitespace-sensitive
3. **Verify paths** - Use ``print(matlab_src_dir)`` to debug
4. **Check imports** - Make sure all extensions are installed

matlab_src_dir Not Found
-------------------------

Add debug output to ``conf.py``:

.. code-block:: python

   import os
   this_dir = os.path.dirname(os.path.abspath(__file__))
   matlab_src_dir = os.path.abspath(os.path.join(this_dir, '..', 'src'))

   print(f"Looking for MATLAB sources in: {matlab_src_dir}")
   print(f"Directory exists: {os.path.exists(matlab_src_dir)}")

Run the build to see the output.

Extension Not Loaded
--------------------

Check if sphinxcontrib-matlabdomain is installed:

.. code-block:: bash

   pip show sphinxcontrib-matlabdomain
   python -c "import sphinxcontrib.matlab; print('OK')"

See Also
========

* :doc:`autodoc-directives` - Using the configured extension
* :doc:`troubleshooting` - Common issues and solutions
* :doc:`../getting-started/first-project` - Complete setup walkthrough
