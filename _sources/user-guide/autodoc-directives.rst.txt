==================
Autodoc Directives
==================

Autodoc directives automatically generate documentation from your MATLAB source code.
This page covers all available directives and their options.

Overview
========

The MATLAB domain provides these autodoc directives:

* ``automodule`` - Document entire modules/packages
* ``autofunction`` - Document functions
* ``autoclass`` - Document classes
* ``automethod`` - Document class methods
* ``autoattribute`` - Document class properties/attributes
* ``autoexception`` - Document exception classes (if applicable)

All directives extract docstrings and signatures from your ``.m`` files automatically.

autofunction
============

Documents a MATLAB function.

Basic Usage
-----------

.. code-block:: rst

   .. autofunction:: myfunction

This extracts the function signature and docstring from ``myfunction.m``.

With Package Prefix
-------------------

.. code-block:: rst

   .. autofunction:: mypackage.utilities.helper

Options
-------

``:noindex:``
   Don't add this function to the index.

   .. code-block:: rst

      .. autofunction:: myfunction
         :noindex:

Example
-------

Given this MATLAB function:

.. code-block:: matlab

   function result = calculate_area(width, height)
   % CALCULATE_AREA Calculate rectangle area
   %
   % Args:
   %     width (double): Width of rectangle
   %     height (double): Height of rectangle
   %
   % Returns:
   %     double: Area of the rectangle

   result = width * height;
   end

This directive:

.. code-block:: rst

   .. autofunction:: calculate_area

Produces documentation showing:

* Function name and signature
* Full docstring
* Parameter descriptions
* Return value description

autoclass
=========

Documents a MATLAB class.

Basic Usage
-----------

.. code-block:: rst

   .. autoclass:: MyClass

Options
-------

``:members:``
   Include all members (methods and properties).

   .. code-block:: rst

      .. autoclass:: MyClass
         :members:

``:undoc-members:``
   Include members without docstrings.

   .. code-block:: rst

      .. autoclass:: MyClass
         :members:
         :undoc-members:

``:show-inheritance:``
   Show the class inheritance diagram.

   .. code-block:: rst

      .. autoclass:: MyClass
         :show-inheritance:

``:member-order:``
   Control the order of members. Options: ``alphabetical``, ``bysource``, ``groupwise``.

   .. code-block:: rst

      .. autoclass:: MyClass
         :members:
         :member-order: bysource

``:exclude-members:``
   Exclude specific members.

   .. code-block:: rst

      .. autoclass:: MyClass
         :members:
         :exclude-members: internal_method, helper

``:special-members:``
   Include special methods (like constructors).

   .. code-block:: rst

      .. autoclass:: MyClass
         :members:
         :special-members: __init__

``:private-members:``
   Include private members (methods starting with underscore or in private blocks).

   .. code-block:: rst

      .. autoclass:: MyClass
         :members:
         :private-members:

Selective Members
-----------------

Include only specific members:

.. code-block:: rst

   .. autoclass:: MyClass
      :members: method1, method2, property1

Example
-------

Given this MATLAB class:

.. code-block:: matlab

   classdef Calculator
       % CALCULATOR A simple calculator class
       %
       % This class provides basic arithmetic operations.

       properties
           % LASTRESULT The result of the last operation
           LastResult
       end

       methods
           function obj = Calculator()
               % CALCULATOR Constructor
               obj.LastResult = 0;
           end

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
               obj.LastResult = result;
           end
       end
   end

This directive:

.. code-block:: rst

   .. autoclass:: Calculator
      :members:
      :undoc-members:

Documents the entire class with all methods and properties.

automodule
==========

Documents an entire MATLAB package or directory.

Basic Usage
-----------

.. code-block:: rst

   .. automodule:: mypackage

For MATLAB packages (directories starting with ``+``):

.. code-block:: rst

   .. automodule:: +mypackage

Options
-------

``:members:``
   Include all functions and classes in the module.

   .. code-block:: rst

      .. automodule:: mypackage
         :members:

``:undoc-members:``
   Include members without docstrings.

   .. code-block:: rst

      .. automodule:: mypackage
         :members:
         :undoc-members:

``:show-inheritance:``
   Show inheritance diagrams for all classes.

   .. code-block:: rst

      .. automodule:: mypackage
         :members:
         :show-inheritance:

``:synopsis:``
   Provide a synopsis that appears in module listings.

   .. code-block:: rst

      .. automodule:: mypackage
         :synopsis: Utility functions for data processing

``:platform:``
   Specify platforms (e.g., "Windows, Linux").

   .. code-block:: rst

      .. automodule:: mypackage
         :platform: MATLAB R2020b and later

Example
-------

For this MATLAB package structure:

.. code-block:: text

   +mypackage/
   ├── helper.m
   ├── validator.m
   └── +subpackage/
       └── tool.m

This directive:

.. code-block:: rst

   .. automodule:: mypackage
      :members:

Documents all functions in the package.

automethod
==========

Documents a specific class method.

Basic Usage
-----------

.. code-block:: rst

   .. automethod:: MyClass.mymethod

This is useful when you want to document a specific method without including the entire class.

Options
-------

Same as ``autofunction``:

* ``:noindex:``

Example
-------

.. code-block:: rst

   .. autoclass:: Calculator
      :noindex:

   .. automethod:: Calculator.add

   .. automethod:: Calculator.multiply

autoattribute
=============

Documents a class property or attribute.

Basic Usage
-----------

.. code-block:: rst

   .. autoattribute:: MyClass.property_name

Options
-------

``:annotation:``
   Add a custom annotation.

   .. code-block:: rst

      .. autoattribute:: MyClass.MAX_SIZE
         :annotation: = 100

Example
-------

Given a class with properties:

.. code-block:: matlab

   classdef DataProcessor
       properties
           % BUFFER_SIZE Maximum buffer size
           BufferSize = 1024
       end
   end

Document the property:

.. code-block:: rst

   .. autoattribute:: DataProcessor.BufferSize

Combining Directives
====================

Full Class Documentation
------------------------

Document a class completely with methods and properties:

.. code-block:: rst

   API Reference
   =============

   Calculator Class
   ----------------

   .. autoclass:: Calculator
      :members:
      :undoc-members:
      :show-inheritance:

Selective Documentation
-----------------------

Document only specific parts:

.. code-block:: rst

   Important Functions
   ===================

   .. autofunction:: validate_input

   .. autofunction:: process_data

   Calculator Class
   ================

   .. autoclass:: Calculator
      :members: add, subtract
      :noindex:

Package Overview
----------------

Document multiple packages:

.. code-block:: rst

   Utility Packages
   ================

   Core Utilities
   --------------
   .. automodule:: utils.core
      :members:

   Data Utilities
   --------------
   .. automodule:: utils.data
      :members:

Directive Options Reference
============================

Common Options
--------------

These options work with most directives:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Option
     - Description
   * - ``:noindex:``
     - Don't add to index
   * - ``:members:``
     - Include all members (classes/modules)
   * - ``:undoc-members:``
     - Include undocumented members
   * - ``:show-inheritance:``
     - Show inheritance diagrams (classes)
   * - ``:member-order:``
     - Order: alphabetical, bysource, groupwise
   * - ``:exclude-members:``
     - Comma-separated list to exclude
   * - ``:private-members:``
     - Include private members
   * - ``:special-members:``
     - Include special members

Tips and Best Practices
========================

1. **Start with :members:**

   .. code-block:: rst

      .. autoclass:: MyClass
         :members:

   Then add ``:undoc-members:`` if needed.

2. **Use :show-inheritance: for class hierarchies**

   Helps users understand relationships between classes.

3. **Exclude internal methods**

   .. code-block:: rst

      .. autoclass:: MyClass
         :members:
         :exclude-members: internal_helper, temp_method

4. **Order members logically**

   Use ``:member-order: bysource`` to preserve your source file order.

5. **Document packages with automodule**

   More convenient than listing every function.

Troubleshooting
===============

Function/Class Not Found
------------------------

* Verify the name matches the file name exactly (case-sensitive)
* Check that ``matlab_src_dir`` is configured correctly
* Ensure the file is in ``matlab_src_dir`` or a subdirectory

No Documentation Appearing
---------------------------

* Check that your MATLAB files have docstring comments
* Verify docstrings are in the correct format (starting with ``%``)
* Run ``make clean && make html`` to rebuild

Members Not Showing
-------------------

* Add ``:members:`` option to ``autoclass`` or ``automodule``
* Add ``:undoc-members:`` if methods lack docstrings
* Check ``:exclude-members:`` isn't filtering them out

See Also
========

* :doc:`configuration` - Configure matlab_src_dir and options
* :doc:`matlab-domain` - Manual documentation directives
* :doc:`napoleon-docstrings` - Better docstring formatting
* :doc:`examples` - Real-world examples
