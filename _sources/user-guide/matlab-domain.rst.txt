=============
MATLAB Domain
=============

The MATLAB domain provides manual documentation directives for when you want more control than autodoc provides.

Overview
========

In addition to autodoc directives, you can manually document MATLAB code using these directives:

* ``.. mat:module::`` - Document a module/package
* ``.. mat:function::`` - Document a function
* ``.. mat:class::`` - Document a class
* ``.. mat:method::`` - Document a method
* ``.. mat:attribute::`` - Document a property/attribute

These give you full control over documentation but require manual maintenance.

Roles for Cross-Referencing
============================

* ``:mat:func:`function_name``` - Link to a function
* ``:mat:class:`ClassName``` - Link to a class
* ``:mat:meth:`ClassName.method``` - Link to a method
* ``:mat:attr:`ClassName.property``` - Link to a property/attribute

When to Use Manual Directives
==============================

Use manual directives when:

* You need custom documentation that differs from source code
* You want to document external code without source access
* You need fine-grained control over what's documented

Use autodoc directives when:

* You want to keep documentation in sync with source
* You have access to MATLAB source files
* You want automatic extraction of signatures

See Also
========

* :doc:`autodoc-directives` - Automatic documentation
* :doc:`cross-referencing` - Linking between pages
* :doc:`examples` - Real-world examples

.. note::
   This page is a placeholder. Full documentation coming soon.
