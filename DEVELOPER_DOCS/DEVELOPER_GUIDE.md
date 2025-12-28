# Developer Guide: sphinxcontrib-matlabdomain

## Project Overview

**sphinxcontrib-matlabdomain** is a Sphinx domain extension that enables automatic documentation generation from MATLAB source code. It's similar to Sphinx's Python autodoc extension but for MATLAB.

### Key Features
- Auto-document MATLAB classes, functions, properties, and methods from source files
- Integration with Sphinx documentation framework
- Support for MATLAB-specific syntax and conventions
- Compatible with Napoleon for Google/NumPy docstring formats
- Works with both `.m` files and `.mlapp` application files

### Project Stats
- **Language**: Python 3.8+
- **Main Dependency**: Sphinx (4.0+), tree-sitter (MATLAB parser)
- **Package**: `sphinxcontrib-matlabdomain`
- **Repository**: https://github.com/sphinx-contrib/matlabdomain

---

## Project Structure

```
matlabdomain/
├── sphinxcontrib/              # Main source code
│   ├── __init__.py
│   ├── matlab.py              # Core domain implementation
│   ├── mat_directives.py      # Autodoc directives
│   ├── mat_documenters.py     # Documenter classes (extract from MATLAB)
│   ├── mat_types.py           # MATLAB type definitions (Class, Function, etc)
│   ├── mat_tree_sitter_parser.py  # AST parser using tree-sitter
│   ├── mat_lexer.py           # Syntax highlighting lexer
│   └── mat_tree_sitter_parser.py  # MATLAB AST parsing
├── tests/                      # Test suite
│   ├── test_*.py             # Individual test modules
│   ├── test_data/            # MATLAB test files (.m files)
│   ├── roots/                # Sphinx test roots (conf.py + source)
│   ├── test_docs/            # Documentation test configuration
│   └── helper.py             # Test utilities
├── docs/                       # Sphinx documentation source
│   ├── conf.py               # Sphinx configuration
│   ├── index.rst             # Documentation index
│   ├── Makefile              # Build documentation
│   └── src/                  # Example MATLAB files
├── .github/
│   └── workflows/            # CI/CD configuration
│       ├── python-package.yml  # Main test workflow
│       └── pre-commit.yml      # Pre-commit checks
├── pyproject.toml            # Project metadata, tool configs
├── setup.py                  # Package installation
├── tox.ini                   # Testing configuration (multiple Python/Sphinx versions)
├── pytest.ini                # pytest configuration
├── dev-requirements.txt      # Development dependencies
└── rtd-requirements.txt      # ReadTheDocs build requirements
```

---

## Code Architecture

### Core Components

#### 1. **matlab.py** - Main Domain
The entry point that registers the MATLAB domain with Sphinx.

- Defines roles (`:class:`, `:func:`, `:meth:`, `:prop:`)
- Registers directives (`.. automodule::`, `.. autoclass::`, etc.)
- Manages cross-references and linking
- ~958 lines - handles domain setup and reference resolution

#### 2. **mat_types.py** - Type System
Represents MATLAB code elements as Python objects.

Classes:
- `MatObject` - Base class for all MATLAB entities
- `MatModule` - Represents a package or folder of MATLAB code
- `MatClass` - MATLAB class (handles attributes, inheritance)
- `MatFunction` - Function file (`.m` file)
- `MatMethod` - Class method
- `MatProperty` - Class property
- `MatScript` - MATLAB script file
- `MatApplication` - MATLAB app (`.mlapp` file)
- `MatEnumeration` - MATLAB enumeration class
- `MatModuleAnalyzer` - Scans filesystem for MATLAB code
- `MatException` - Exception class

Key features:
- Parses docstrings into description/parameters/returns/examples
- Handles MATLAB-specific attributes (class properties, methods)
- Manages hierarchical relationships (package/class/method)

#### 3. **mat_tree_sitter_parser.py** - AST Parser
Uses tree-sitter to parse MATLAB syntax trees.

Classes:
- `MatClassParser` - Parses class definitions
- `MatFunctionParser` - Parses function definitions
- `MatScriptParser` - Parses script files

Features:
- Extracts function signatures and arguments
- Identifies class methods and properties
- Parses docstrings and comments
- Handles MATLAB syntax specifics (e.g., ellipsis continuation)

#### 4. **mat_documenters.py** - Documenter Classes
Sphinx autodoc-style documenters that extract documentation from MATLAB files.

Classes:
- `MatlabDocumenter` - Base class
- `ModuleDocumenter` - Handles MATLAB packages/modules
- `ClassDocumenter` - Documents MATLAB classes
- `FunctionDocumenter` - Documents functions
- `PropertyDocumenter` - Documents class properties
- `MethodDocumenter` - Documents methods
- `ApplicationDocumenter` - Documents MATLAB apps
- `EnumerationDocumenter` - Documents enumerations

Each documenter:
- Finds MATLAB source files
- Parses them using mat_tree_sitter_parser
- Generates reST documentation
- Handles cross-references to other entities

#### 5. **mat_directives.py** - Autodoc Directives
Extends Sphinx's autodoc directive system.

Classes:
- `MatlabAutodocDirective` - Base autodoc directive

Provides:
- `.. automodule::` - Auto-document MATLAB packages
- `.. autoclass::` - Auto-document MATLAB classes
- `.. autofunction::` - Auto-document functions
- `.. autoproperty::` - Auto-document properties
- `.. automethod::` - Auto-document methods
- `.. autoenum::` - Auto-document enumerations
- `.. autoapp::` - Auto-document MATLAB apps

#### 6. **mat_lexer.py** - Syntax Highlighting
Provides MATLAB code syntax highlighting for Sphinx HTML output.

Features:
- Tokenizes MATLAB code
- Maps MATLAB syntax to Pygments tokens
- Used by `.. code-block:: matlab` in documentation

---

## Data Flow

```
Developer writes MATLAB code + docstrings
              ↓
Sphinx reads conf.py (matlab_src_dir setting)
              ↓
Autodoc directive triggered (e.g., .. autoclass::)
              ↓
MatDocumenter finds MATLAB file on filesystem
              ↓
mat_tree_sitter_parser parses MATLAB AST
              ↓
MatType objects created (MatClass, MatFunction, etc)
              ↓
Documenter generates reST formatted documentation
              ↓
Sphinx processes reST and builds HTML/PDF
```

---

## Testing Strategy

### Test Framework
- **Framework**: pytest
- **Sphinx Testing**: `sphinx.testing.fixtures` (make_app)
- **Structure**: Test roots under `tests/roots/test_*/` contain minimal Sphinx projects

### Test Categories

#### 1. **Autodoc Tests** (`test_autodoc.py`)
- Tests that MATLAB code is correctly parsed and documented
- Checks docstring extraction and formatting
- Verifies cross-references work correctly

#### 2. **Parser Tests** (`test_parse_mfile.py`)
- Tests tree-sitter parser on various MATLAB syntax
- Verifies function/class/property extraction
- Tests edge cases (comments, attributes, etc)

#### 3. **Module Analysis Tests**
- `test_module_class_names.py` - Class name resolution
- `test_classfolder.py` - @ClassName folder conventions
- `test_package_prefix.py` - Package path handling
- `test_pymat.py` - Common integration scenarios

#### 4. **Feature Tests**
- `test_lexer.py` - Syntax highlighting
- `test_autodoc_short_links.py` - Short vs full names
- `test_autodoc_properties.py` - Property documentation
- `test_package_links.py` - Cross-package references
- `test_numad.py` - Napoleon docstring support
- `test_matlabify.py` - MATLAB file conversion

### Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_autodoc.py::test_target

# Run with coverage
pytest --cov=sphinxcontrib

# Run tox (multiple Python and Sphinx versions)
tox
```

### Test Data
Located in `tests/test_data/`:
- Example MATLAB files (ClassExample.m, ClassWithEvent.m, etc)
- Used to verify parser correctness
- Includes edge cases and error scenarios

---

## CI/CD Configuration

### GitHub Actions Workflows

#### 1. **python-package.yml** - Main Test Suite
Runs on every push and PR.

**Matrix**:
- Python: 3.10, 3.11, 3.12, 3.13
- Sphinx: 5.3, 6.0, 7.0, latest

**Steps**:
1. Install dependencies
2. Lint with ruff
3. Run pytest with coverage
4. Upload coverage to Codecov

**Key**: Tests package against multiple Sphinx versions to ensure compatibility.

#### 2. **pre-commit.yml**
Runs pre-commit checks.

**Hooks** (defined in `.pre-commit-config.yaml`):
- ruff (linting and formatting)
- codespell (spell checking)
- trailing whitespace
- YAML validation
- etc.

### Local Pre-commit Setup
```bash
pre-commit install
pre-commit run --all-files  # Run manually
```

### ReadTheDocs Configuration
- **Config**: `readthedocs.yml`
- **Build OS**: Ubuntu 22.04
- **Python**: 3.12
- **Requirements**: `rtd-requirements.txt`
- **Sphinx Config**: `docs/conf.py`

---

## Development Setup

### Prerequisites
- Python 3.8+
- git
- Virtual environment (recommended)

### Quick Start

```bash
# 1. Clone repo
git clone https://github.com/sphinx-contrib/matlabdomain.git
cd matlabdomain

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install in editable mode with dev dependencies
pip install -e .
pip install -r dev-requirements.txt

# 4. Setup pre-commit hooks
pre-commit install

# 5. Run tests
pytest

# 6. Build documentation
cd docs && make html && cd ..
# Output in: docs/_build/html/index.html
```

### Tool Configuration

#### **Ruff** (Linting & Formatting)
Config in `pyproject.toml` `[tool.ruff]`:
- Line length: 88 characters
- Include: tests, sphinxcontrib, docs
- Rules: docstring formatting, imports, performance, code quality
- Max complexity: 51

Usage:
```bash
ruff check sphinxcontrib tests
ruff format sphinxcontrib tests  # Auto-fix
```

#### **Pre-commit**
Config in `.pre-commit-config.yaml`:
- Runs ruff, codespell, YAML checks
- Runs automatically on `git commit`

### Useful Commands

```bash
# Format code
ruff format sphinxcontrib tests

# Check formatting
ruff check sphinxcontrib tests

# Run tests with verbose output
pytest -v

# Run specific test
pytest tests/test_autodoc.py::test_target -v

# Run tests and show print statements
pytest -s

# Run tests with coverage report
pytest --cov=sphinxcontrib --cov-report=html

# Build docs locally
cd docs && make html && cd ..

# Clean build artifacts
cd docs && make clean && cd ..
rm -rf build dist .eggs *.egg-info
```

---

## Known Issues & Bugs

To be documented - identify specific issues in GitHub issues or code comments.

### Areas to Investigate
1. Parser edge cases with complex MATLAB syntax
2. Cross-reference resolution in large projects
3. Performance with large codebases
4. Compatibility with latest Sphinx versions
5. MATLAB app (.mlapp) parsing completeness

---

## Migration to `uv` Package Manager

### Current State
- Uses pip with `requirements*.txt`
- Uses setuptools/setup.py
- Uses tox for testing across versions

### Migration Plan

1. **Install uv**
   ```bash
   pip install uv
   ```

2. **Create `pyproject.toml` entries** (already started)
   - Convert `setup.py` dependencies to `[project]` section
   - Define optional groups: dev, test, docs

3. **Replace requirements files**
   ```bash
   # Convert dev-requirements.txt
   uv pip compile dev-requirements.txt -o requirements-dev.lock

   # Install from lock file
   uv pip install -r requirements-dev.lock
   ```

4. **Update tox.ini** for uv
   - Use `uv run` instead of direct pytest calls

5. **Update CI workflows**
   - Use `uv` for faster dependency resolution
   - Cache uv's built-in cache

### Benefits
- Faster dependency resolution
- Built-in lock file support
- Better caching in CI
- Simpler Python environment management

---

## Next Steps for Contributors

1. **Set up development environment** (see Development Setup)
2. **Read the docstrings** in sphinxcontrib/matlab.py
3. **Run tests** to understand current behavior
4. **Pick an issue** from GitHub issues
5. **Create feature branch** and make changes
6. **Run tests locally** before pushing
7. **Submit PR** with clear description

### Good First Issues
- Documentation improvements
- Adding type hints (see `source.addTypeAnnotation`)
- Improving error messages
- Adding tests for edge cases
- Performance improvements

---

## Resources

- **Sphinx Documentation**: https://www.sphinx-doc.org/
- **Sphinx Domains**: https://www.sphinx-doc.org/en/master/extdev/domainapi.html
- **tree-sitter-matlab**: https://github.com/acristoffers/tree-sitter-matlab
- **Repository**: https://github.com/sphinx-contrib/matlabdomain
- **Read the Docs**: https://sphinxcontrib-matlabdomain.readthedocs.io/
