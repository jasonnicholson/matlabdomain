.. sphinxcontrib-matlabdomain documentation master file, created by
   sphinx-quickstart on Tue Jul 17 11:53:15 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

sphinxcontrib-matlabdomain
==========================

**sphinxcontrib-matlabdomain** is `Sphinx`_ extension to generate API
documentation for `MATLAB`_, it also provides *autodoc* facilities, that lets
you generate documentation *automatically* from MATLAB source files. It works
similar to the  `Python Domain`_.


Getting started
---------------

If you are completely new to `Sphinx`_, follow this `Tutorial`_.

Install **sphinxcontrib-matlabdomain** with

::

   pip install sphinxcontrib-matlabdomain

In order for the Sphinx MATLAB domain to auto-document MATLAB source code, set
the config value of ``matlab_src_dir`` to the absolute root path. Currently
only one MATLAB path can be specified, but all subfolders in that tree will be
searched.

For convenience the `primary domain <http://sphinx-doc.org/config.html#confval-primary_domain>`_
can be set to ``mat``.

Assuming that the directory structure of the project is ike this:

::

   docs/
       conf.py
       index.rst
       make.bat
       Makefile
   src
       <matlab source files>

The ``docs/conf.py`` would look like this:

.. code-block:: python

   import os

   # other statements

   extensions = ['sphinx.ext.autodoc', 'sphinxcontrib.matlab']
   this_dir = os.path.dirname(os.path.abspath(__file__))
   matlab_src_dir = os.path.abspath(os.path.join(this_dir, '..'))
   primary_domain = 'mat'

Example
-------

.. automodule:: src

.. autofunction:: times_two

.. autofunction:: times_two_napoleon

Using auto-directives
---------------------

* Creating a Sphinx project
* Modifying ``conf.py`` to include **sphinxcontrib-matlabdomain**  and autodoc.
* Add ``matlab_src_dir`` with root of MATLAB sources
* List directives and options
* Using auto-directives
* Using napoleon - different style docstrings, that are almost like MATLAB
* Examples

  * Function
  * Function in package
  * Class with inheritance and properties
  * Class folder (have to use autofunction)

* Known limitations

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   CHANGES.rst
   DEVELOPMENT.rst


MATLAB names and link anchors
-----------------------------

Source files get their MATLAB name the way MATLAB forms it: ``+pkg`` folders
are namespaces, ``@Cls`` folders define class ``Cls``, and files in plain
folders are global names. ``matlab_version`` (default ``"R2026a"``, oldest
``"R2025a"``) selects release-dependent rules, and ``matlab_namelengthmax``
(``63`` or ``2048``; default derived from ``matlab_version``) the identifier
length limit. When several files have the same MATLAB name, the first one on
the path wins (the source root first, then folders before subfolders, in name
order). Cross-references by MATLAB name (for example ``pkg.fun`` or
``pkg.Cls.method``) resolve to the object, however it was documented.

The HTML anchor of a documented object is its documented full name with
surrounding whitespace and leading dots removed and each whitespace run
replaced by ``-``; all other characters are kept. A module's anchor is
``module-`` followed by the same transformation of its name. This scheme is a
stable contract: anchors, deep links and intersphinx inventories only change if
the documented name changes.

Directives
----------

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Sphinx: https://http://www.sphinx-doc.org
.. _Python Domain: http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-python-domain
.. _Tutorial: http://www.sphinx-doc.org/en/1.7/tutorial.html
.. _MATLAB: https://mathworks.com
