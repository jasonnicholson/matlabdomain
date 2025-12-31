=============
Known Issues
=============

This page tracks known bugs and limitations in sphinxcontrib-matlabdomain.

Current Known Issues
====================

For the most up-to-date list of known issues, see:

* `GitHub Issues <https://github.com/sphinx-contrib/matlabdomain/issues>`_
* Project IMPLEMENTATION_GUIDE.md in the repository

Documented TODOs
================

The codebase contains several TODO items that are documented in the DEVELOPER_DOCS:

1. **mat_types.py** - Module scanning and path handling improvements
2. **Test organization** - Test ordering and dependencies
3. **Windows path handling** - Cross-platform compatibility

See the DEVELOPER_DOCS/IMPLEMENTATION_GUIDE.md file in the repository for detailed information about each TODO.

Limitations
===========

MATLAB Version Support
----------------------

The extension works with most MATLAB syntax but may not support:

* Very old MATLAB syntax (pre-R2014b)
* Cutting-edge features from the latest MATLAB release
* All MATLAB App Designer features

Single matlab_src_dir
---------------------

Currently only one ``matlab_src_dir`` can be specified. If you have MATLAB code in multiple separate locations, you'll need to:

* Organize code into a single directory tree, or
* Use symbolic links to consolidate sources

Workarounds
===========

For known issues with workarounds, check:

* :doc:`../user-guide/troubleshooting`
* GitHub Issues with "workaround" label

Reporting New Issues
====================

Found a bug? Please report it:

1. Check if it's already reported on `GitHub Issues <https://github.com/sphinx-contrib/matlabdomain/issues>`_
2. If not, create a new issue with:

   * Clear description of the problem
   * Minimal example to reproduce
   * Your environment (Python, Sphinx, OS versions)
   * Full error messages

See :doc:`contributing` for more details.

See Also
========

* :doc:`contributing` - How to contribute fixes
* :doc:`../user-guide/troubleshooting` - Common problems and solutions
* `GitHub Issues <https://github.com/sphinx-contrib/matlabdomain/issues>`_
