==================
Cross-Referencing
==================

Learn how to create links between different parts of your documentation.

Automatic Links
===============

With ``matlab_auto_link`` enabled, entity names are automatically linked:

.. code-block:: python

   # In conf.py
   matlab_auto_link = 'basic'  # or 'all'

Manual Links
============

Use roles to create explicit links:

.. code-block:: rst

   See :func:`myfunction` for details.
   The :class:`MyClass` implements this.
   Call :meth:`MyClass.method` to execute.

Short Links
===========

With ``matlab_short_links = True``, use shorter names:

.. code-block:: rst

   :class:`MyClass`  instead of  :class:`package.subpackage.MyClass`

See Also
========

* :doc:`configuration` - Configure linking behavior
* :doc:`examples` - Examples with links

.. note::
   This page is a placeholder. Full documentation coming soon.
