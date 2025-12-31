====================
Napoleon Docstrings
====================

Napoleon is a Sphinx extension that allows you to write docstrings in Google or NumPy style, which are more readable than traditional reStructuredText.

Overview
========

sphinxcontrib-matlabdomain works great with Napoleon to support cleaner docstring formats.

Google Style (Recommended)
===========================

.. code-block:: matlab

   function result = calculate(x, y)
   % CALCULATE Perform a calculation
   %
   % Args:
   %     x (double): First input value
   %     y (double): Second input value
   %
   % Returns:
   %     double: The calculated result
   %
   % Example:
   %     result = calculate(5, 10);

   result = x + y;
   end

NumPy Style
===========

.. code-block:: matlab

   function result = calculate(x, y)
   % CALCULATE Perform a calculation
   %
   % Parameters
   % ----------
   % x : double
   %     First input value
   % y : double
   %     Second input value
   %
   % Returns
   % -------
   % double
   %     The calculated result

   result = x + y;
   end

Configuration
=============

Enable Napoleon in your ``conf.py``:

.. code-block:: python

   extensions = [
       'sphinxcontrib.matlab',
       'sphinx.ext.napoleon',  # Add this
   ]

   # Napoleon settings
   napoleon_google_docstring = True
   napoleon_numpy_docstring = True

See Also
========

* :doc:`configuration` - Full configuration options
* :doc:`examples` - More examples
* `Napoleon documentation <https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_

.. note::
   This page is a placeholder. Full documentation coming soon.
