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
the config value of ``matlab_src_code_project_root`` to the root folder of the
MATLAB sources. A relative path is relative to the Sphinx source directory
(the folder with ``index.rst``). All subfolders of the root are searched.
``matlab_src_dir`` is deprecated: it still works as the root, with a warning.

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

   # other statements

   extensions = ['sphinx.ext.autodoc', 'sphinxcontrib.matlab']
   matlab_src_code_project_root = '..'
   primary_domain = 'mat'

Example
-------

.. autofolder:: src

.. autofunction:: times_two

.. autofunction:: times_two_napoleon

Using auto-directives
---------------------

* Creating a Sphinx project
* Modifying ``conf.py`` to include **sphinxcontrib-matlabdomain**  and autodoc.
* Add ``matlab_src_code_project_root`` with root of MATLAB sources
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

Every documented object is identified by its *path reference*: its path
relative to ``matlab_src_code_project_root``, with ``/`` separators, Unicode
NFC and the file extension. Members follow the file with ``.``; folders end
with ``/`` and the root is ``./``.

.. list-table::
   :header-rows: 1

   * - Source
     - Path reference
     - MATLAB name (displayed)
   * - ``target/+package/ClassBar.m``
     - ``target/+package/ClassBar.m``
     - ``package.ClassBar``
   * - its method ``myMethod``
     - ``target/+package/ClassBar.m.myMethod``
     - ``package.ClassBar.myMethod``
   * - ``src/+pkg/@Cls/Cls.m``
     - ``src/+pkg/@Cls/Cls.m``
     - ``pkg.Cls``
   * - ``src/private/helper.m``
     - ``src/private/helper.m``
     - ``helper``
   * - folder ``target/+package``
     - ``target/+package/``
     - ``package``

Signatures and the inventory's display names show the MATLAB name, formed the
way MATLAB forms it: ``+pkg`` folders are namespaces, ``@Cls`` folders define
class ``Cls``, and files in plain folders are global names. ``matlab_version``
(default ``"R2026a"``, oldest ``"R2025a"``) selects release-dependent rules,
and ``matlab_namelengthmax`` (``63`` or ``2048``; default derived from
``matlab_version``) the identifier length limit. Files MATLAB cannot call
(keyword namespaces such as ``+for``, invalid file names, class files that do
not match their ``@`` folder, ``@C/sub`` files from R2026a, ...) have no
MATLAB name: they are documented and displayed by path, with one
``mat.not_callable`` warning each, which ``suppress_warnings`` can turn off.
Files below ``private/`` never warn.

Auto directives, cross-references (``:mat:func:`...```), auto-links and "See
also" entries resolve a name in this order:

1. an exact path reference (``target/+package/ClassBar.m``);
2. relative to the current folder (set by ``mat:folder`` or
   ``mat:currentfolder``; inside a docstring, the documented file's folder):
   a path below it (``ClassBar.m``) or a MATLAB name visible from it,
   including the folder's ``private/`` files, like MATLAB;
3. a MATLAB name (``package.ClassBar``, ``package.ClassBar.myMethod``) that
   exactly one object has; ``private/`` files are not considered. If several
   objects have the name, a ``mat.ambiguous`` warning lists their path
   references, which you can use instead.

Folders use one directive, ``mat:folder`` (and ``mat:autofolder``); refer to
them with ``:mat:folder:``. A valid ``+`` folder shows ``namespace
package.sub`` and can also be referred to by that name; any other folder shows
``folder target/`` and is referred to by path. ``@Cls`` folders are documented
through their class. ``mat:currentfolder`` sets the current folder without
documenting it (``.`` is the root, ``None`` clears it).

The HTML anchor of an object is ``mat-`` followed by its path reference, in
which every ASCII character other than letters, digits and
``- . _ ! $ & ' ( ) * + , ; = : @ /`` is written as ``~XX`` per UTF-8 byte
(for example ``#mat-target/+package/ClassBar.m`` and
``#mat-my~20folder/f.m``). Distinct references never share an anchor. This
scheme is a stable contract: anchors, deep links and intersphinx inventories
only change if a file moves.

``matlab_keep_package_prefix`` and ``matlab_short_links`` were removed;
setting them is an error.

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
