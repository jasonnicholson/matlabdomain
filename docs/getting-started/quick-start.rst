===========
Quick Start
===========

Get started with sphinxcontrib-matlabdomain in 5 minutes! This guide assumes you
have already :doc:`installed <installation>` the extension.

What You'll Build
=================

In this tutorial, you'll:

1. Create a minimal Sphinx project
2. Configure it to document MATLAB code
3. Add some MATLAB source files
4. Generate HTML documentation

Step 1: Create a Sphinx Project
================================

If you don't have a Sphinx project yet, create one:

.. code-block:: bash

   # Create a docs directory
   mkdir docs
   cd docs

   # Run Sphinx quickstart
   sphinx-quickstart

Answer the prompts:

* **Separate source and build directories?** No (just press Enter)
* **Project name:** My MATLAB Project
* **Author name:** Your Name
* **Project release:** 1.0
* **Project language:** en (or your language)

This creates a basic Sphinx structure:

.. code-block:: text

   docs/
   ├── conf.py          # Configuration file
   ├── index.rst        # Main page
   ├── Makefile         # Build commands (Linux/Mac)
   └── make.bat         # Build commands (Windows)

Step 2: Configure for MATLAB
=============================

Open ``conf.py`` and add sphinxcontrib.matlab to your extensions:

.. code-block:: python

   # Add these lines to conf.py
   import os

   extensions = [
       'sphinx.ext.autodoc',
       'sphinxcontrib.matlab',
       'sphinx.ext.napoleon',  # Optional: for Google/NumPy style docstrings
   ]

   # Point to your MATLAB source directory
   matlab_src_dir = os.path.abspath('../src')

   # (Optional) Make MATLAB the primary domain
   primary_domain = 'mat'

Step 3: Add MATLAB Source Files
================================

Create a ``src`` directory next to ``docs`` and add a MATLAB file:

.. code-block:: bash

   # From your project root
   mkdir src
   cd src

Create a file ``src/hello.m``:

.. literalinclude:: ../src/hello.m
   :language: matlab

Step 4: Document Your Code
===========================

Edit ``docs/index.rst`` to include your MATLAB documentation:

.. code-block:: rst

   Welcome to My MATLAB Project
   =============================

   .. autofunction:: hello

Step 5: Build the Documentation
================================

Now build your HTML documentation:

.. code-block:: bash

   # On Linux/macOS
   cd docs
   make html

   # On Windows
   cd docs
   make.bat html

Open the generated documentation:

.. code-block:: bash

   # On Linux
   xdg-open _build/html/index.html # This likely works too: open _build/html/index.html

   # On macOS
   open _build/html/index.html

   # On Windows
   start _build/html/index.html # or call it directly: _build/html/index.html

You should see your documentation with the ``hello`` function documented! As shown below:

.. mat:autofunction:: hello

What Just Happened?
===================

1. **Sphinx quickstart** created a basic documentation project
2. **conf.py** was configured to find your MATLAB source files
3. **autofunction directive** automatically extracted documentation from your MATLAB code
4. **make html** built your documentation into HTML

Next Steps
==========

Now that you have a working setup, explore more features:

* :doc:`first-project` - More detailed walkthrough with classes and packages
* :doc:`../user-guide/autodoc-directives` - Learn all autodoc directives
* :doc:`../user-guide/configuration` - Customize your setup
* :doc:`../user-guide/examples` - See more complex examples

Common Next Questions
=====================

How do I document a class?
---------------------------

Use the ``autoclass`` directive:

.. code-block:: rst

   .. autoclass:: MyClass
      :members:

How do I document an entire package?
-------------------------------------

Use the ``automodule`` directive:

.. code-block:: rst

   .. automodule:: mypackage
      :members:

How do I customize the output?
-------------------------------

See :doc:`../user-guide/configuration` for all available options like:

* ``matlab_short_links`` - Use shorter names
* ``matlab_auto_link`` - Automatically create cross-references
* ``matlab_keep_package_prefix`` - Control package name display

Where do I go for help?
------------------------

* :doc:`../user-guide/troubleshooting` - Common issues and solutions
* `GitHub Issues <https://github.com/sphinx-contrib/matlabdomain/issues>`_ - Report bugs or ask questions
* :doc:`../user-guide/examples` - See working examples
