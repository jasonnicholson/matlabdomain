====================
Your First Project
====================

This guide walks you through creating a complete Sphinx documentation project
for MATLAB code, from scratch. No Sphinx experience required!

By the end, you'll have:

* A working Sphinx documentation site
* Automatic documentation for MATLAB functions, classes, and packages
* A generated HTML website you can share or host

Project Setup
=============

Let's say you have a MATLAB project with this structure:

.. code-block:: text

   MyMatlabProject/
   ├── src/
   │   ├── hello.m
   │   ├── Calculator.m
   │   └── +mypackage/
   │       └── utils.m
   └── docs/
       (we'll create this)

Step 1: Install Prerequisites
==============================

First, make sure you have Python 3.8+ installed:

.. code-block:: bash

   python --version

Create and activate a virtual environment:

.. code-block:: bash

   # Navigate to your project root
   cd MyMatlabProject

   # Create virtual environment
   python -m venv .venv

   # Activate it (Linux/macOS)
   source .venv/bin/activate # on Windows: .venv\Scripts\activate


Install Sphinx and sphinxcontrib-matlabdomain:

.. code-block:: bash

   pip install sphinx sphinxcontrib-matlabdomain sphinx-autobuild

Step 2: Create Documentation Directory
=======================================

Create a ``docs`` directory and initialize Sphinx:

.. code-block:: bash

   mkdir docs
   cd docs
   sphinx-quickstart

Answer the quickstart questions:

.. code-block:: text

   > Separate source and build directories (y/n) [n]: n
   > Project name: MyMatlabProject
   > Author name(s): Your Name
   > Project release []: 1.0.0
   > Project language [en]: en

This creates:

.. code-block:: text

   docs/
   ├── conf.py          # Configuration
   ├── index.rst        # Homepage
   ├── _static/         # Static files (CSS, images)
   ├── _templates/      # HTML templates
   ├── Makefile         # Build commands
   └── make.bat         # Build commands (Windows)

Step 3: Configure for MATLAB
=============================

Edit ``docs/conf.py`` to enable MATLAB documentation.

**Find the extensions list** and modify it:

.. code-block:: python

   # Find this line in conf.py
   extensions = []

   # Replace it with
   extensions = [
       'sphinx.ext.autodoc',      # Auto-generate docs
       'sphinxcontrib.matlab',    # MATLAB domain
       'sphinx.ext.napoleon',     # Google/NumPy docstrings
   ]

**Add MATLAB configuration** after the extensions:

.. code-block:: python

   import os

   # Point to your MATLAB source directory
   this_dir = os.path.dirname(os.path.abspath(__file__))
   matlab_src_dir = os.path.abspath(os.path.join(this_dir, '..', 'src'))

   # Make MATLAB the primary domain (optional but convenient)
   primary_domain = 'mat'

   # Use shorter links (optional)
   matlab_short_links = True

Your ``conf.py`` should now look like this (abbreviated):

.. code-block:: python

   # Configuration file for Sphinx
   import os

   project = 'MyMatlabProject'
   copyright = '2025, Your Name'
   author = 'Your Name'
   release = '1.0.0'

   extensions = [
       'sphinx.ext.autodoc',
       'sphinxcontrib.matlab',
       'sphinx.ext.napoleon',
   ]

   this_dir = os.path.dirname(os.path.abspath(__file__))
   matlab_src_dir = os.path.abspath(os.path.join(this_dir, '..', 'src'))
   primary_domain = 'mat'
   matlab_short_links = True

   templates_path = ['_templates']
   exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

   html_theme = 'alabaster'  # or 'sphinx_rtd_theme'
   html_static_path = ['_static']

Step 4: Create MATLAB Source Files
===================================

Let's create some example MATLAB files to document.

**src/hello.m** - A simple function:

.. code-block:: matlab

   function greeting = hello(name)
   % HELLO Say hello to someone
   %
   % Args:
   %     name (char): Name of the person to greet
   %
   % Returns:
   %     char: A greeting message
   %
   % Example:
   %     >> greeting = hello('World')
   %     greeting = 'Hello, World!'

   greeting = ['Hello, ' name '!'];
   end

**src/Calculator.m** - A class:

.. code-block:: matlab

   classdef Calculator
       % CALCULATOR A simple calculator class
       %
       % This class demonstrates basic arithmetic operations.

       methods
           function result = add(obj, a, b)
               % ADD Add two numbers
               %
               % Args:
               %     a (double): First number
               %     b (double): Second number
               %
               % Returns:
               %     double: Sum of a and b

               result = a + b;
           end

           function result = multiply(obj, a, b)
               % MULTIPLY Multiply two numbers
               %
               % Args:
               %     a (double): First number
               %     b (double): Second number
               %
               % Returns:
               %     double: Product of a and b

               result = a * b;
           end
       end
   end

**src/+mypackage/utils.m** - A package function:

.. code-block:: matlab

   function result = double_value(x)
   % DOUBLE_VALUE Double a numeric value
   %
   % Args:
   %     x (double): Input value
   %
   % Returns:
   %     double: Value multiplied by 2

   result = x * 2;
   end

The documentation comments are called docstrings. Sphinx will extract these to build your docs. They
are reStructuredText formatted. When you use Napoleon, you can write them in Google style as shown above.
Refer to :doc:`../user-guide/napoleon-docstrings` for more details on writing docstrings.
For more information on reStructuredText syntax, see the `Sphinx documentation on reStructuredText
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_. The best way to learn
reStructuredText is by using `sphinx-autobuild` as described in Step 7 below, which provides live
previewing as you edit your docstrings and RST files.


Step 5: Generate API docs with ``sphinx-matlab-apidoc``
========================================================

Instead of hand-writing ``api.rst``, generate it automatically from your MATLAB
sources using the bundled ``sphinx-matlab-apidoc`` CLI.

From the ``docs`` folder run:

.. code-block:: bash

   # Linux/macOS
   sphinx-matlab-apidoc -f -o api ../src # Windows: sphinx-matlab-apidoc -f -o api ..\src

Where:

  * ``-f`` forces overwriting existing files
  * ``-o api`` specifies output directory for generated RST files
  * ``../src`` points to the MATLAB source directory


What this does
--------------

* Scans ``../src`` for MATLAB packages, classes, and functions
* Writes a set of ``.rst`` files into ``docs/api`` (including ``index.rst``)
* Adds autodoc directives for every discovered item

Wire it into your main table of contents by editing ``docs/index.rst`` so the
toctree includes the generated entry:

.. code-block:: rst

   .. toctree::
      :maxdepth: 2
      :caption: Contents:

      api/index

Regenerate after adding or deleting source files
--------------------------------------------------

When add or delete MATLAB files, re-run ``sphinx-matlab-apidoc -f -o api ../src`` to
refresh the generated ``.rst`` files before rebuilding HTML. You do not need to rerun if
updated a docstring.

.. note::

  After working with this tool for a while, what you find is that you will want your API
  documentation to be organized a certain way. Take a look at :code:`sphinx-matlab-apidoc --help` for
  all the options to customize the output structure. If that doesn't meet your needs,
  you can always:


  - Maintain .rst files yourself. Manually edit ``.rst`` files using :doc:`../user-guide/matlab-domain`.
    This is good for small projects that don't change often. This gives you full customization control.
    The autodoc directives such as ``mat:automodule``, ``mat:autofunction``, ``mat:autoclass``, etc. are likely
    the main players.
  - copy `sphinx_matlab_apidoc.py` from the package source and modify it to suit
    your needs. Your AI variant can help you. Then wire it in to your build process. If you have a lot
    of files and don't like what `sphinx-matlab-apidoc` generates, then this is probably the best option.



Step 6: Build Your Documentation
=================================

Now build the HTML documentation:

.. code-block:: bash

   # Make sure you're in the docs/ directory
   cd docs

   # Build HTML (Linux/macOS)
   make html

   # Build HTML (Windows)
   make.bat html

The documentation will be generated in ``docs/_build/html/``.

The ``Makefile`` and ``make.bat`` scripts provide convenient commands to build
the docs. Take a look at your ``Makefile`` for other options like ``make clean``
and to understand how to call `sphinx-build` directly if needed.

Generally, the command is:

.. code-block:: bash

   sphinx-build -b html . _build/html

Where:

  * ``-b html`` specifies the HTML builder
  * ``.`` is the source directory (current folder)
  * ``_build/html`` is the output directory


Step 7: View Your Documentation
================================

Use ``sphinx-autobuild`` for live reloading as you edit:

.. code-block:: bash

   # From the docs/ directory, start the live server
   sphinx-autobuild --open-browser . _build/html --watch ../src

Where:

  * ``--open-browser`` opens your default web browser automatically
  * ``.`` is the source directory
  * ``_build/html`` is the output directory
  * ``--watch ../src`` tells it to also watch your MATLAB source files for changes

The server will start and watch your files for changes. Your browser should automatically open to:

.. code-block:: text

   http://localhost:8000

You should see:

* Your project homepage
* API documentation with all functions and classes
* Automatically extracted docstrings
* Cross-references and navigation

**The page will automatically reload** whenever you edit a ``.rst`` or ``.m`` file.
Press ``Ctrl+C`` to stop the server.

Understanding What Happened
============================

Let's break down what Sphinx did:

1. **Parsed conf.py** to understand your project configuration
2. **Found MATLAB sources** in the directory specified by ``matlab_src_dir``
3. **Extracted docstrings** from your ``.m`` files
4. **Processed RST files** (``index.rst``, ``api.rst``) with autodoc directives
5. **Generated HTML** from the processed content

The Magic of Autodoc Directives
--------------------------------

The ``autofunction``, ``autoclass``, and ``automodule`` directives:

* Find your MATLAB source files
* Parse them to extract function signatures and docstrings
* Format them into nice HTML documentation
* Create cross-references automatically

Customizing Your Documentation
===============================

Change the Theme
----------------

Edit ``conf.py`` to use the Read the Docs theme:

.. code-block:: python

   html_theme = 'sphinx_rtd_theme'

You'll need to install it first:

.. code-block:: bash

   pip install sphinx-rtd-theme

Add a Logo
----------

Place your logo in ``docs/_static/logo.png`` and add to ``conf.py``:

.. code-block:: python

   html_logo = '_static/logo.png'

Add More Pages
--------------

Create new ``.rst`` files in ``docs/`` and add them to the ``toctree`` in ``index.rst``.

Next Steps
==========

You now have a working Sphinx documentation site! Explore more:

* :doc:`../user-guide/configuration` - Advanced configuration options
* :doc:`../user-guide/autodoc-directives` - Learn all autodoc features
* :doc:`../user-guide/napoleon-docstrings` - Better docstring styles
* :doc:`../user-guide/cross-referencing` - Link between pages

Common Issues
=============

"No module named 'sphinxcontrib.matlab'"
-----------------------------------------

Make sure you:

1. Installed sphinxcontrib-matlabdomain: ``pip install sphinxcontrib-matlabdomain``
2. Are using the correct Python environment

"WARNING: matlab_src_dir not set"
----------------------------------

Check that ``matlab_src_dir`` in ``conf.py`` points to the correct directory.

"WARNING: don't know which module to import"
---------------------------------------------

This usually means:

* The MATLAB file doesn't exist in ``matlab_src_dir``
* The file or function name is misspelled
* The path in ``matlab_src_dir`` is incorrect

Functions/classes not showing up
---------------------------------

Verify:

1. The source files are in ``matlab_src_dir`` or its subdirectories
2. The function/class names match in your ``.rst`` files
3. Run ``make clean`` then ``make html`` to rebuild from scratch
