============
Installation
============

This guide will help you install sphinxcontrib-matlabdomain, even if you've never used Sphinx before.

Prerequisites
=============

Before installing, make sure you have:

* Python 3.8 or higher
* pip (Python package installer)

You can check your Python version with:

.. code-block:: bash

   python --version

Installing sphinxcontrib-matlabdomain
======================================

Basic Installation
------------------

Install the package using pip:

.. code-block:: bash

   pip install sphinxcontrib-matlabdomain

This will automatically install all required dependencies including:

* Sphinx (≥4.0.0)
* tree-sitter-matlab
* tree-sitter

Installing in a Virtual Environment (Recommended)
--------------------------------------------------

It's best practice to use a virtual environment to avoid conflicts with other Python packages.

**On Linux/macOS:**

.. code-block:: bash

   # Create a virtual environment
   python -m venv .venv

   # Activate it
   source .venv/bin/activate # Windows: .venv\Scripts\activate

   # Install the package
   pip install sphinxcontrib-matlabdomain

Verifying Installation
======================

To verify the installation was successful, run:

.. code-block:: bash

   python -c "import sphinxcontrib.matlab; print('Installation successful!')"

You should see "Installation successful!" printed.

What Gets Installed?
====================

When you install sphinxcontrib-matlabdomain, you get:

1. **The Sphinx extension** - For documenting MATLAB code in Sphinx projects
2. **sphinx-matlab-apidoc** - A command-line tool for bulk documentation generation
3. **MATLAB lexer** - Syntax highlighting for MATLAB code blocks
4. **Tree-sitter parser** - Fast and accurate MATLAB code parsing

Next Steps
==========

Now that you have sphinxcontrib-matlabdomain installed, you can:

* Follow the :doc:`quick-start` guide for a 5-minute tutorial
* Create :doc:`first-project` with step-by-step instructions
* Explore the :doc:`../user-guide/configuration` options

Installing Sphinx Separately
=============================

If you already have a Sphinx project and just want to add MATLAB support,
the basic installation above is all you need. Then add ``'sphinxcontrib.matlab'``
to your ``extensions`` list in ``conf.py``.

If you're starting from scratch, see :doc:`first-project` for complete setup instructions.

Troubleshooting
===============

Installation Fails
------------------

If installation fails, try upgrading pip first:

.. code-block:: bash

   pip install --upgrade pip
   pip install sphinxcontrib-matlabdomain

ImportError After Installation
-------------------------------

If you get an ImportError when trying to use the extension, make sure:

1. You activated your virtual environment (if using one)
2. You're using the correct Python interpreter
3. The package was installed in the right environment

You can check where packages are installed:

.. code-block:: bash

   pip show sphinxcontrib-matlabdomain

Python Version Issues
---------------------

This extension requires Python 3.8 or higher. If you have an older Python version,
you can:

1. Install a newer Python version from `python.org <https://www.python.org/downloads/>`_
2. Use version 0.11.8 which supports Python 2:

   .. code-block:: bash

      pip install sphinxcontrib-matlabdomain==0.11.8
