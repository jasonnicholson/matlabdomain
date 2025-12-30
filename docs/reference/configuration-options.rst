======================
Configuration Options
======================

Complete reference of all configuration options.

This page provides a comprehensive reference. For a getting-started guide, see :doc:`../user-guide/configuration`.

Essential Options
=================

extensions
----------

**Type:** List[str]

**Required:** Yes

Add sphinxcontrib.matlab to your extensions:

.. code-block:: python

   extensions = ['sphinxcontrib.matlab', 'sphinx.ext.autodoc']

matlab_src_dir
--------------

**Type:** str

**Required:** Yes

**Default:** None

Path to MATLAB source directory:

.. code-block:: python

   matlab_src_dir = '/path/to/matlab/src'

Optional Options
================

primary_domain
--------------

**Type:** str

**Default:** ``'py'``

Set to ``'mat'`` to make MATLAB the primary domain:

.. code-block:: python

   primary_domain = 'mat'

matlab_short_links
------------------

**Type:** bool

**Default:** ``False``

**Added in:** v0.19.0

Use shorter names in links:

.. code-block:: python

   matlab_short_links = True

matlab_auto_link
----------------

**Type:** str or None

**Default:** ``None``

**Added in:** v0.21.0

**Options:** ``'basic'``, ``'all'``, ``None``

Automatically create links:

.. code-block:: python

   matlab_auto_link = 'basic'

matlab_keep_package_prefix
---------------------------

**Type:** bool

**Default:** ``True``

Show ``+`` prefix in package names:

.. code-block:: python

   matlab_keep_package_prefix = False

matlab_show_property_default_values
------------------------------------

**Type:** bool

**Default:** ``False``

**Added in:** v0.17.0

Show default property values:

.. code-block:: python

   matlab_show_property_default_values = True

See Also
========

* :doc:`../user-guide/configuration` - Configuration guide
* :doc:`../user-guide/autodoc-directives` - Using configured options

.. note::
   Full reference documentation coming soon. See :doc:`../user-guide/configuration` for details.
