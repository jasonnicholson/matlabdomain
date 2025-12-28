# Implementation Guide & Known Issues

This document outlines the current implementation state, known issues, and areas for improvement.

---

## Known TODOs in Codebase

### 1. **TODO: Method Attributes in ClassFolder** (mat_types.py:279)
**Location**: [sphinxcontrib/mat_types.py](sphinxcontrib/mat_types.py#L279)

**Issue**: Find and document method attributes defined in classfolder class definition.

**Context**: 
- MATLAB supports `@ClassFolder` syntax where methods are defined in separate files
- Currently extracting method attributes from method files, but missing attributes from the class definition file
- Should parse the main class file for `methods (Attributes)` blocks

**Severity**: Medium - Affects @ClassFolder projects where methods have attributes

**Steps to Fix**:
1. In `MatModuleAnalyzer.analyze_class()`, extend parsing logic
2. Look for `methods (...) ... end` blocks in class file
3. Extract method names and their attributes
4. Apply attributes to corresponding method objects

---

### 2. **TODO: Module Contents Documentation** (mat_types.py:582)
**Location**: [sphinxcontrib/mat_types.py](sphinxcontrib/mat_types.py#L582)

**Issue**: Get docstring and `__all__` from `contents.m` if it exists.

**Context**:
- MATLAB packages can have a `contents.m` file that documents the entire package
- Currently only extracting docstring from `+package/functionname.m` files
- Should also look for `+package/contents.m` and use that as module docstring

**Severity**: Medium - Affects package documentation completeness

**Steps to Fix**:
1. In `MatModuleAnalyzer.__init__()`, after finding the package folder
2. Check for `contents.m` file in the package directory
3. Parse docstring from `contents.m`
4. Also extract function list from `contents.m` to populate `__all__`

---

### 3. **TODO: Method Args Removal in Tests** (test_matlabify.py:218)
**Location**: [tests/test_matlabify.py](tests/test_matlabify.py#L218-L219)

**Issue**: Method args contain 'obj' when run standalone vs removed when run after test_autodoc.py.

**Context**:
- When tests run individually, method argument lists include 'obj' (the implicit self parameter)
- When tests run together with test_autodoc.py, 'obj' is removed
- Suggests state pollution or test ordering dependency
- Likely related to parser state or cached analysis

**Severity**: High - Test reliability issue

**Steps to Fix**:
1. Investigate why test_autodoc.py affects test_matlabify.py
2. Check MatModuleAnalyzer for cached state
3. Ensure each test gets fresh parser/analyzer instances
4. Add proper test fixtures to isolate state
5. Run tests in random order with pytest-random to catch ordering issues

---

## Bug Analysis from CHANGES.rst

### Recent Fixes (0.22.x)
- ✅ Issue #262: ReadTheDocs Sphinx 8.0.2 `doc2path` API change
- ✅ Issue #249: Multiline property default value parsing
- ✅ Issue #252: Missing class and method attributes
- ✅ Issue #243: Autolinking short names matching module names
- ✅ Issue #250: Removed unused `MatInstanceAttributeDocumentor`

### Recent Fixes (0.21.x)
- ✅ Issue #240: Links in literal blocks not detected
- ✅ Issue #235: Multiple directories with same name causing dict in entities_table
- ✅ Issue #204: Module named same as class short name causing AttributeError
- ✅ Issue #221: Using builtins in class folder definition methods
- ✅ Issue #225: Empty @classfolder causing assertion error
- ✅ Issue #220: Property docstring parsing with blank lines between comments

### Likely Remaining Issues (Areas to investigate)

1. **Complex MATLAB Syntax Parsing**
   - Nested function scopes
   - Functions with ellipsis line continuation
   - Complex property getter/setter methods
   - Events and enumerations edge cases

2. **Large Codebase Performance**
   - First build time with many MATLAB files
   - Memory usage with large class hierarchies
   - Incremental build efficiency

3. **Cross-reference Resolution**
   - References to nested packages (pkg.sub.Class)
   - Forward references (methods using classes defined later)
   - Generic class references without full paths

4. **Documentation Generation**
   - Inherited method documentation
   - Abstract method documentation
   - Property getter/setter separation
   - Event documentation

5. **Edge Cases**
   - MATLAB files with syntax errors (should warn gracefully)
   - Circular imports
   - Ambiguous class/function names
   - Unicode characters in comments

---

## Architecture Notes for Future Work

### Parser Limitations
The tree-sitter MATLAB parser (`mat_tree_sitter_parser.py`) is powerful but:
- Relies on third-party tree-sitter-matlab package
- Limited control over parsing errors
- May not support all MATLAB syntax variations
- Consider fallback parsing for error cases

### Module Analysis Strategy
`MatModuleAnalyzer` walks the filesystem and builds entity tree:
- O(n) filesystem walk where n = number of MATLAB files
- Could benefit from caching analyzed metadata
- ReadTheDocs builds could be optimized with persistent cache

### Documenter Architecture
Documenters (`mat_documenters.py`) follow Sphinx autodoc pattern:
- `generate()` method creates reST content
- Cross-references created dynamically during parse
- Links validated during Sphinx resolution phase
- Currently no validation of reference validity

---

## Configuration Improvements Needed

Current configuration options:
- `matlab_src_dir` - Path to MATLAB source
- `matlab_short_links` - Use short vs qualified names
- `matlab_auto_link` - Auto-link known entities
- `matlab_keep_package_prefix` - Include/exclude package path

**Recommended additions**:
1. `matlab_exclude_patterns` - Ignore certain files/folders
2. `matlab_inherit_docstrings` - Inherit parent class docs
3. `matlab_show_property_specs` - Already added in 0.22.0
4. `matlab_parse_timeout` - Timeout for parsing large files
5. `matlab_cache_dir` - Persistent parse cache location

---

## Testing Improvements Needed

Current test coverage:
- Core autodoc functionality ✅
- Parser edge cases ✅
- Module/package structure ✅
- Link generation ✅

**Recommended additions**:
1. Error handling tests - What happens with invalid MATLAB?
2. Performance tests - Time/memory with large codebases
3. Integration tests - Real-world projects
4. Regression tests - Each bug fix should add test
5. Compatibility tests - Different Sphinx versions (already using tox)

---

## Documentation Improvements Needed

Current documentation:
- README.rst - Basic usage ✅
- Configuration options in README ✅
- Example in docs/src/ ✅
- ReadTheDocs site ✅

**Recommended additions**:
1. **Advanced Usage Guide**
   - Package structure best practices
   - Docstring conventions for MATLAB
   - Cross-referencing patterns
   - Custom styling

2. **API Documentation**
   - Document MatType classes
   - Document Documenter classes
   - Parser plugin architecture
   - Extension points for customization

3. **Troubleshooting Guide**
   - Common parsing errors
   - Reference resolution issues
   - Build performance
   - Compatibility issues

4. **Migration Guides**
   - Python 2 → Python 3
   - Old Sphinx → New Sphinx
   - Updating docstrings for Napoleon

---

## Sphinx Version Compatibility

Tox tests against:
- Sphinx 4.5 (legacy support)
- Sphinx 5.3
- Sphinx 6.0
- Sphinx 7.0
- Sphinx latest

**Known compatibility notes**:
- Issue #262: Sphinx 8.0.2 requires `doc2path` handling change
- Likely need to update tox.ini to include Sphinx 8.0+ testing

---

## Priority Action Items

### High Priority
1. [ ] Fix test ordering issue (test_matlabify.py TODOs)
2. [ ] Add support for contents.m module docstrings
3. [ ] Improve error messages for invalid MATLAB

### Medium Priority
1. [ ] Extract method attributes from @ClassFolder definitions
2. [ ] Add caching/memoization for analyzer
3. [ ] Expand test coverage for edge cases
4. [ ] Performance profiling on large projects

### Low Priority
1. [ ] Configuration improvements
2. [ ] Documentation enhancements
3. [ ] Support for undocumented MATLAB features
4. [ ] Code refactoring for maintainability

---

## Resources for Contributors

- **Tree-sitter MATLAB**: https://github.com/acristoffers/tree-sitter-matlab
- **Sphinx Domain API**: https://www.sphinx-doc.org/en/master/extdev/domainapi.html
- **Sphinx Autodoc**: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
