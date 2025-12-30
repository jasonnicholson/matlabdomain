============
Architecture
============

This guide explains the internal architecture of sphinxcontrib-matlabdomain for developers who want to contribute or understand how it works.

Project Overview
================

**sphinxcontrib-matlabdomain** is a Sphinx domain extension that enables automatic documentation generation from MATLAB source code, similar to Sphinx's Python autodoc extension.

**Key Features:**

* Auto-document MATLAB classes, functions, properties, and methods from source files
* Integration with Sphinx documentation framework
* Support for MATLAB-specific syntax and conventions
* Compatible with Napoleon for Google/NumPy docstring formats
* Works with both ``.m`` files and ``.mlapp`` application files

**Project Stats:**

* **Language:** Python 3.8+
* **Main Dependencies:** Sphinx (4.0+), tree-sitter (MATLAB parser)
* **Package:** ``sphinxcontrib-matlabdomain``
* **Repository:** https://github.com/sphinx-contrib/matlabdomain

Core Components
===============

The extension consists of six main Python modules:

matlab.py - Main Domain (958 lines)
------------------------------------

**Purpose:** Entry point that registers the MATLAB domain with Sphinx.

**Key Responsibilities:**

* Defines roles (``:class:``, ``:func:``, ``:meth:``, ``:prop:``)
* Registers directives (``.. automodule::``, ``.. autoclass::``, etc.)
* Manages cross-references and linking
* Handles domain setup and reference resolution

**Main Classes:**

* ``MatObject`` - Base class for all MATLAB object descriptions
* ``MatDomain`` - The MATLAB domain itself
* Various directive classes for manual documentation

mat_types.py - Type System
---------------------------

**Purpose:** Represents MATLAB code elements as Python objects.

**Classes:**

* ``MatObject`` - Base class for all MATLAB entities
* ``MatModule`` - Represents a package or folder of MATLAB code
* ``MatClass`` - MATLAB class (handles attributes, inheritance)
* ``MatFunction`` - Function file (``.m`` file)
* ``MatMethod`` - Class method
* ``MatProperty`` - Class property
* ``MatScript`` - MATLAB script file
* ``MatApplication`` - MATLAB app (``.mlapp`` file)
* ``MatEnumeration`` - MATLAB enumeration class
* ``MatModuleAnalyzer`` - Scans filesystem for MATLAB code
* ``MatException`` - Exception class

**Key Features:**

* Parses docstrings into description/parameters/returns/examples
* Handles MATLAB-specific attributes (class properties, methods)
* Manages hierarchical relationships (package/class/method)
* File system scanning and module discovery

mat_tree_sitter_parser.py - AST Parser
---------------------------------------

**Purpose:** Uses tree-sitter to parse MATLAB syntax trees.

**Classes:**

* ``MatClassParser`` - Parses class definitions
* ``MatFunctionParser`` - Parses function definitions
* ``MatScriptParser`` - Parses script files

**Features:**

* Extracts function signatures and arguments
* Identifies class methods and properties
* Parses docstrings and comments
* Handles MATLAB syntax specifics (e.g., ellipsis continuation)
* Provides fast, accurate parsing using tree-sitter

mat_documenters.py - Documenter Classes
----------------------------------------

**Purpose:** Sphinx autodoc-style documenters that extract documentation from MATLAB files.

**Classes:**

* ``MatlabDocumenter`` - Base class
* ``ModuleDocumenter`` - Handles MATLAB packages/modules
* ``ClassDocumenter`` - Documents MATLAB classes
* ``FunctionDocumenter`` - Documents functions
* ``PropertyDocumenter`` - Documents class properties
* ``MethodDocumenter`` - Documents methods
* ``ApplicationDocumenter`` - Documents MATLAB apps
* ``EnumerationDocumenter`` - Documents enumerations

**Each documenter:**

* Finds MATLAB source files
* Parses them using mat_tree_sitter_parser
* Generates reStructuredText documentation
* Handles cross-references to other entities

mat_directives.py - Autodoc Directives
---------------------------------------

**Purpose:** Extends Sphinx's autodoc directive system.

**Provides These Directives:**

* ``.. automodule::`` - Auto-document MATLAB packages
* ``.. autoclass::`` - Auto-document MATLAB classes
* ``.. autofunction::`` - Auto-document functions
* ``.. autoproperty::`` - Auto-document properties
* ``.. automethod::`` - Auto-document methods
* ``.. autoenum::`` - Auto-document enumerations
* ``.. autoapp::`` - Auto-document MATLAB apps

mat_lexer.py - Syntax Highlighting
-----------------------------------

**Purpose:** Provides MATLAB code syntax highlighting for Sphinx HTML output.

**Features:**

* Tokenizes MATLAB code
* Maps MATLAB syntax to Pygments tokens
* Used by ``.. code-block:: matlab`` in documentation

Data Flow
=========

Understanding how documentation is generated:

1. User Setup
-------------

User configures ``conf.py``:

.. code-block:: python

   extensions = ['sphinxcontrib.matlab']
   matlab_src_dir = '/path/to/matlab/src'

2. Sphinx Build Starts
-----------------------

* Sphinx reads configuration
* Loads extensions including sphinxcontrib.matlab
* matlab.py registers the domain, roles, and directives

3. Module Discovery
-------------------

When ``matlab_src_dir`` is set:

* ``MatModuleAnalyzer`` scans the directory tree
* Finds all ``.m`` and ``.mlapp`` files
* Builds a map of available modules, classes, and functions

4. Directive Processing
------------------------

When Sphinx encounters ``.. autofunction:: myfunction``:

* The appropriate documenter (e.g., ``FunctionDocumenter``) is invoked
* Documenter locates the source file in ``matlab_src_dir``
* File is read and passed to parser

5. Parsing
----------

``mat_tree_sitter_parser.py`` processes the source:

* Creates an Abstract Syntax Tree (AST)
* Extracts function signature, parameters, return values
* Extracts docstring comments
* Identifies code structure

6. Type Creation
----------------

Parser output creates ``MatType`` objects:

* ``MatFunction`` with signature and docstring
* Properties filled: name, args, returns, description
* Relationships established (e.g., method → class)

7. Documentation Generation
----------------------------

Documenter generates reStructuredText:

* Formats function signature
* Converts docstring to reST
* Adds cross-references for known entities
* Returns formatted documentation

8. Cross-Reference Resolution
------------------------------

``MatDomain`` resolves references like ``:func:`myfunction```:

* Looks up entity in domain's inventory
* Creates clickable links in HTML output
* Handles short names if ``matlab_short_links = True``

9. HTML Generation
------------------

* Sphinx converts reST to HTML
* ``mat_lexer.py`` provides syntax highlighting for code blocks
* Final HTML documentation is generated

File System Organization
========================

Source Code Layout
------------------

.. code-block:: text

   sphinxcontrib/
   ├── __init__.py                    # Package initialization
   ├── matlab.py                      # Domain, roles, directives
   ├── mat_types.py                   # Type system
   ├── mat_tree_sitter_parser.py      # AST parsing
   ├── mat_documenters.py             # Autodoc documenters
   ├── mat_directives.py              # Autodoc directives
   ├── mat_lexer.py                   # Syntax highlighting
   └── sphinx_matlab_apidoc.py        # CLI tool

Test Organization
-----------------

.. code-block:: text

   tests/
   ├── test_*.py                      # Test modules
   ├── roots/                         # Sphinx test configurations
   │   └── test-*/                    # Each test has its own root
   │       ├── conf.py
   │       ├── index.rst
   │       └── test_data/             # MATLAB test files
   └── helper.py                      # Test utilities

Key Algorithms
==============

Module Discovery
----------------

``MatModuleAnalyzer.find_modules()``:

1. Walk directory tree starting from ``matlab_src_dir``
2. Identify MATLAB packages (``+`` directories)
3. Find class folders (``@`` directories)
4. Catalog all ``.m`` and ``.mlapp`` files
5. Build hierarchical module structure

Name Resolution
---------------

When resolving ``matlab_short_links``:

1. User references ``:class:`MyClass```
2. System searches for matching classes
3. If multiple matches, uses context to disambiguate
4. Returns full path or shortest unique path
5. Creates cross-reference in output

Docstring Parsing
-----------------

From MATLAB comments to structured documentation:

1. Extract comment block above function/class
2. Identify sections (Args, Returns, Example, See also)
3. Parse parameter descriptions
4. Convert to docutils node tree
5. Apply Napoleon transformations if enabled

Design Patterns
===============

The Documenter Pattern
-----------------------

Each MATLAB entity type has a corresponding documenter:

.. code-block:: python

   class FunctionDocumenter(MatlabDocumenter):
       objtype = 'function'

       def parse_definition(self):
           # Extract function signature
           pass

       def generate(self):
           # Generate documentation
           pass

This follows Sphinx's autodoc pattern, making it familiar to Sphinx developers.

The Type System
---------------

MATLAB entities are represented as Python objects inheriting from ``MatObject``:

.. code-block:: python

   class MatFunction(MatObject):
       def __init__(self, name, path, docstring):
           self.name = name
           self.path = path
           self.docstring = docstring
           self.args = []
           self.returns = []

This provides a clean abstraction over MATLAB's diverse code structures.

Extension Points
================

For developers extending this project:

Adding New Directive Types
---------------------------

1. Create a new class in ``mat_directives.py``
2. Inherit from ``ObjectDescription``
3. Implement ``handle_signature()`` and ``transform_content()``
4. Register in ``setup()`` function

Adding New MatTypes
-------------------

1. Create class in ``mat_types.py`` inheriting from ``MatObject``
2. Implement parsing logic
3. Create corresponding documenter in ``mat_documenters.py``
4. Add handling to ``mat_tree_sitter_parser.py``

Custom Parsing
--------------

To handle new MATLAB syntax:

1. Update tree-sitter grammar (external dependency)
2. Modify parser in ``mat_tree_sitter_parser.py``
3. Extract new information into MatType objects

Dependencies
============

Core Dependencies
-----------------

* **Sphinx (≥4.0.0)** - Documentation framework
* **tree-sitter (≥0.21.3, <0.23.0)** - Parser infrastructure
* **tree-sitter-matlab (≥1.0.2, <1.0.5)** - MATLAB grammar
* **docutils** - Document utilities (via Sphinx)

Development Dependencies
------------------------

* **pytest** - Testing framework
* **pytest-cov** - Coverage reporting
* **ruff** - Linting and formatting
* **pre-commit** - Git hooks
* **tox** - Testing across multiple environments

See Also
========

* :doc:`contributing` - How to contribute to the project
* :doc:`testing` - Testing strategy and how to run tests
* :doc:`known-issues` - Current bugs and limitations
* :doc:`quick-reference` - Command cheat sheet
