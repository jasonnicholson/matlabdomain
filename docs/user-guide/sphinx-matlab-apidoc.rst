======================
sphinx-matlab-apidoc
======================

Generate reStructuredText files for MATLAB projects automatically, similar to
``sphinx-apidoc`` for Python.

When to Use
===========

* You want a complete API reference without hand-writing ``.rst`` files.
* Your MATLAB project has many packages/classes and you need consistent docs.
* You want to regenerate API pages when source code files are added or deleted. Note, regeneration
  is not needed for changes within existing files. Rebuilding the Sphinx docs will pick up
  changes automatically.

Quick Start
===========

From your ``docs`` directory (assuming MATLAB sources are in ``../src``):

.. code-block:: bash

   # Force overwrite (-f), write output to docs/api (-o api), scan ../src
   sphinx-matlab-apidoc -f -o api ../src

Where:

  * ``-f`` forces overwriting existing files
  * ``-o api`` writes generated RST files to the ``api`` folder
  * ``../src`` is the path to your MATLAB source files

Then include the generated index in your toctree (e.g. in ``docs/index.rst``):

.. code-block:: rst

   .. toctree::
      :maxdepth: 2
      :caption: Contents:

      api/index

Re-run the command whenever MATLAB sources are added or deleted to refresh the generated RST.

Common Options
==============

* ``-o OUTPUT`` / ``--output-dir OUTPUT``: Target folder for generated RST (e.g. ``api``)
* ``-f`` / ``--force``: Overwrite existing files
* ``-n`` / ``--dry-run``: Show what would be generated without writing
* ``--max-files N``: Max files per page (pagination), default 50

Examples
========

Basic generation (no overwrite):

.. code-block:: bash

   sphinx-matlab-apidoc -o api ../src

Dry run to inspect changes:

.. code-block:: bash

   sphinx-matlab-apidoc -n -o api ../src

Increase page size to 100 entries:

.. code-block:: bash

   sphinx-matlab-apidoc --max-files 100 -o api ../src

Tips and Pitfalls
=================

* Run from the docs root so relative paths are simple.
* Avoid folders starting with ``_`` and names with hyphens; they may be skipped
  because Python-style rules apply internally.
* MATLAB package and class folders are supported: use ``+mypackage`` and
  ``@MyClass``.
* After generation, ensure ``matlab_src_dir`` in ``conf.py`` still points to your
  MATLAB sources when building Sphinx.

Troubleshooting
===============

* If pages are missing, verify the source path you passed (e.g. ``../src``) and
  rerun with ``--dry-run`` to see what would be emitted.
* If builds warn about missing toctree entries, confirm ``api/index`` is listed
  in your toctree.
* For large projects, use ``--max-files`` to control pagination and keep pages
  readable.
