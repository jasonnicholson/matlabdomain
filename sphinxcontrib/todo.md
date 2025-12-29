- [ ] Change sphinx_matlab_apidoc.py to the following spec.
  - Break up rst pages into namespaces. Make a page for the global namespace, and a page for each package namespace. Limit the number of items per page to 50 (make this configurable like it is now).
    - Each page should have a table of contents at the top with links to each class/function/script on the page.
    - Examples are shown below. If there are more than 50 items in a namespace, create multiple pages for that namespace with suffixes like `_1`, `_2`, etc.
    - Include .mlapp as you see fit. They seem like their own type of item. I don't have any examples of them.
    - Handle folders begin with non valid python identifiers appropriately. The one error I have seen is `_folder/files/file.m`. I am not sure what's going to work. I do know that `+namespace1/+namespace2/file.m` works fine as `+namespace1.+namespace2.file`. I am open here if you have ideas.
    - Write unit tests to verify this functionality.
    - Use the `test_projects` to demonstrate this functionality.

```rst
Global Namespace
=================

.. contents: Table of Contents
  :depth: 10
  :local:

Classes
-------

Function Reference: class1
^^^^^^^^^^^^^^^^^^^^^^^

.. mat:autoclass:: class1
  :show-inheritance:
  :members:
  :private-members:
  :special-members:
  :undoc-members:


Functions
---------

Function Reference: function1
^^^^^^^^^^^^^^^^^^^^^^^^^
.. mat:autofunction:: function1

Scripts
-------

Function Reference: script1
^^^^^^^^^^^^^^^^^^^^^^^
.. mat:autoscript:: script1


```

```rst
namespace1 Namespace
=================

.. contents: Table of Contents
  :depth: 10
  :local:

Classes
-------

Function Reference: namespace1.class1
^^^^^^^^^^^^^^^^^^^^^^^

.. mat:autoclass:: namespace1.class1
  :show-inheritance:
  :members:
  :private-members:
  :special-members:
  :undoc-members:


Functions
---------

Function Reference: namespace1.function1
^^^^^^^^^^^^^^^^^^^^^^^^^
.. mat:autofunction:: namespace1.function1

Scripts
-------

Function Reference: namespace1.script1
^^^^^^^^^^^^^^^^^^^^^^^
.. mat:autoscript:: namespace1.script1


```

- [ ] Namespaced custom validating functions for properties does not work. It works fine for arguments blocks.

```matlab
classdef MyClass
  properties
    Prop1 {myNamespace.myValidatorFunction(Prop1)}
  end
end
```

- [ ] Adding a validator function to a comment after the property does not work.

```matlab
  arguments
    value1
    value2 {mustBeA(value2, ["double", "single"])} %{mustBeText(value2)}
  end
```
- [ ] Folders that begin with a `_` cause failures. Is there a way around this? MATLAB does not care about this.
