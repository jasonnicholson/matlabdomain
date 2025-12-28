# Quick Reference & Cheat Sheet

Fast lookup for common tasks when working on sphinxcontrib-matlabdomain.

---

## Project Quick Facts

| Item | Value |
|------|-------|
| **Repository** | https://github.com/sphinx-contrib/matlabdomain |
| **Package** | `sphinxcontrib-matlabdomain` |
| **Python** | 3.8+ |
| **Sphinx** | 4.0+ (tested 4.5, 5.3, 6.0, 7.0, latest) |
| **Main Deps** | Sphinx, tree-sitter, tree-sitter-matlab |
| **License** | BSD |
| **Documentation** | https://sphinxcontrib-matlabdomain.readthedocs.io |

---

## Essential Commands

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/sphinx-contrib/matlabdomain.git
cd matlabdomain

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e .
pip install -r dev-requirements.txt

# Setup pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_autodoc.py

# Specific test
pytest tests/test_autodoc.py::test_target -v

# With coverage
pytest --cov=sphinxcontrib --cov-report=html
open htmlcov/index.html

# All Python/Sphinx versions (requires tox)
tox

# With pytest output
pytest -v -s
```

### Code Quality

```bash
# Format code
ruff format sphinxcontrib tests

# Check linting
ruff check sphinxcontrib tests

# Check spell
codespell

# Run pre-commit hooks
pre-commit run --all-files
```

### Building Documentation

```bash
# Build HTML docs
cd docs && make html && cd ..
open docs/_build/html/index.html

# Clean build
cd docs && make clean && cd ..

# Check links
sphinx-linkcheck docs/

# Watch for changes (requires sphinx-autobuild)
sphinx-autobuild docs docs/_build/html
```

### Version Management

```bash
# Current version (from git tags)
python -c "from setuptools_scm import get_version; print(get_version())"

# Create release
git tag v0.23.0
git push origin v0.23.0
```

---

## Key Files Reference

### Core Source Code

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| [sphinxcontrib/matlab.py](sphinxcontrib/matlab.py) | Main domain | `MatDomain`, role/directive setup |
| [sphinxcontrib/mat_types.py](sphinxcontrib/mat_types.py) | Type system | `MatObject`, `MatClass`, `MatFunction`, `MatModuleAnalyzer` |
| [sphinxcontrib/mat_tree_sitter_parser.py](sphinxcontrib/mat_tree_sitter_parser.py) | AST parser | `MatClassParser`, `MatFunctionParser`, `MatScriptParser` |
| [sphinxcontrib/mat_documenters.py](sphinxcontrib/mat_documenters.py) | Autodoc | `ModuleDocumenter`, `ClassDocumenter`, `FunctionDocumenter` |
| [sphinxcontrib/mat_directives.py](sphinxcontrib/mat_directives.py) | Autodoc directives | `MatlabAutodocDirective` |
| [sphinxcontrib/mat_lexer.py](sphinxcontrib/mat_lexer.py) | Code highlighting | Pygments lexer |

### Testing

| File | Purpose |
|------|---------|
| [tests/test_autodoc.py](tests/test_autodoc.py) | Core autodoc tests |
| [tests/test_parse_mfile.py](tests/test_parse_mfile.py) | Parser tests |
| [tests/test_matlabify.py](tests/test_matlabify.py) | Type system tests |
| [tests/helper.py](tests/helper.py) | Test utilities |
| [tests/test_data/](tests/test_data/) | Example MATLAB files |

### Configuration

| File | Purpose |
|------|---------|
| [pyproject.toml](pyproject.toml) | Project metadata, tool configs |
| [setup.py](setup.py) | Package installation |
| [pytest.ini](pytest.ini) | pytest configuration |
| [tox.ini](tox.ini) | Multi-version testing |
| [.github/workflows/](github/workflows/) | CI/CD configuration |
| [readthedocs.yml](readthedocs.yml) | ReadTheDocs config |

---

## Common Workflows

### Adding a New Feature

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes to sphinxcontrib/*.py
# 3. Write tests in tests/test_*.py
# 4. Format code
ruff format sphinxcontrib tests

# 5. Run tests
pytest tests/test_mynewtest.py -v

# 6. Commit with clear message
git add .
git commit -m "feat: add new feature

- What does it do
- Why is it needed
- Closes #issue-number"

# 7. Push and create PR
git push origin feature/my-feature
# Create PR on GitHub
```

### Fixing a Bug

```bash
# 1. Find the issue
# - Check GitHub issues
# - Search code with grep_search or semantic_search

# 2. Write failing test first (TDD)
# tests/test_bugfix.py - test that reproduces bug

# 3. Fix the bug
# - Edit sphinxcontrib/mat_*.py

# 4. Verify test passes
pytest tests/test_bugfix.py -v

# 5. Ensure no regressions
pytest
tox

# 6. Commit
git commit -m "fix: describe the bug

Fixes #issue-number"
```

### Reviewing Documentation

The documentation is auto-generated from docstrings and reST files in docs/. To verify your changes:

```bash
cd docs && make clean && make html
open _build/html/index.html
```

Look for:
- Broken links
- Incorrect formatting
- Missing information
- Typos

---

## Important Configuration Settings

### In `docs/conf.py`

```python
# MATLAB source directory
matlab_src_dir = "../path/to/matlab/code"

# Use short names (ClassFoo instead of package.ClassFoo)
matlab_short_links = False

# Auto-link known entities
matlab_auto_link = "basic"  # or "all"

# Keep package prefix in links
matlab_keep_package_prefix = True
```

### In `pyproject.toml` - Ruff Configuration

```toml
[tool.ruff.lint]
select = ["C", "C4", "E9", "F63", "F7", "F82", "FLY", "I", "PERF", "RUF", "SIM", "W"]
ignore = ["D203", "E203", "PERF203", "PERF401", "PERF403", "RUF001", "RUF012", "SIM102"]
max-complexity = 51
```

---

## Troubleshooting Common Issues

### Tests Fail Locally But Pass in CI

**Possible causes:**
- Different Python version (Check tox.ini - test with correct versions)
- Different dependencies (Update dev-requirements.txt)
- Test ordering issue (Run tests in random order: `pytest --random-order`)

### Import Errors After Editing

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
rm -rf build/ dist/ *.egg-info

# Reinstall in editable mode
pip install -e .
```

### Documentation Won't Build

```bash
# Check for broken reST syntax
rst2html.py docs/index.rst > /dev/null

# Check for MATLAB files referenced
sphinx-linkcheck docs/

# Clear Sphinx cache
rm -rf docs/.doctrees
```

### Pre-commit Hooks Failing

```bash
# Check which hooks are failing
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
pre-commit run codespell --all-files

# Update hooks
pre-commit autoupdate
```

---

## Code Navigation

### Finding Things

```bash
# Search for a function/class
grep -r "class MatClass" sphinxcontrib/

# Find where a config option is used
grep -r "matlab_src_dir" sphinxcontrib/

# Find all TODOs
grep -r "TODO" sphinxcontrib/ tests/

# Find recent changes
git log --oneline -20
```

### Understanding Data Flow

```
MATLAB source file (.m)
    ↓
MatModuleAnalyzer finds and catalogs
    ↓
mat_tree_sitter_parser parses syntax tree
    ↓
MatType objects created (MatClass, MatFunction, etc)
    ↓
Documenter generates reST content
    ↓
Sphinx processes reST → HTML/PDF
```

---

## Git Workflow

### Branch Naming

```bash
# Feature branches
git checkout -b feature/short-description

# Bug fixes
git checkout -b fix/issue-number

# Documentation
git checkout -b docs/topic

# Refactoring
git checkout -b refactor/area
```

### Commit Messages

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```bash
git commit -m "feat(parser): support ellipsis continuation"
git commit -m "fix(autodoc): handle empty doctstrings"
git commit -m "docs(guide): add troubleshooting section"
```

### Pull Request Checklist

- [ ] Tests passing locally: `pytest`
- [ ] Code formatted: `ruff format`
- [ ] Linting clean: `ruff check`
- [ ] Documentation updated (if needed)
- [ ] Commit messages clear
- [ ] Issue referenced in description

---

## Resources & Links

### Documentation
- [Sphinx Domain API](https://www.sphinx-doc.org/en/master/extdev/domainapi.html)
- [Sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)
- [tree-sitter-matlab](https://github.com/acristoffers/tree-sitter-matlab)
- [Read the Docs](https://sphinxcontrib-matlabdomain.readthedocs.io/)

### Tools
- [ruff](https://github.com/astral-sh/ruff) - Linting
- [pytest](https://docs.pytest.org/) - Testing
- [tox](https://tox.wiki/) - Multi-version testing
- [pre-commit](https://pre-commit.com/) - Git hooks

### External References
- [MATLAB Documentation](https://www.mathworks.com/help/matlab/)
- [PEP 257](https://peps.python.org/pep-0257/) - Docstring conventions
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

## Development Guides

For more detailed information, see:

- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Complete development setup and architecture
- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - Known issues and TODOs
- [UV_MIGRATION.md](UV_MIGRATION.md) - Upgrade to uv package manager
- [SPHINX_DOCS_PLAN.md](SPHINX_DOCS_PLAN.md) - Documentation site improvement plan

---

## Quick Links

| Link | Purpose |
|------|---------|
| [GitHub Issues](https://github.com/sphinx-contrib/matlabdomain/issues) | Report bugs, request features |
| [GitHub Discussions](https://github.com/sphinx-contrib/matlabdomain/discussions) | Questions and ideas |
| [Pull Requests](https://github.com/sphinx-contrib/matlabdomain/pulls) | Submit contributions |
| [ReadTheDocs](https://sphinxcontrib-matlabdomain.readthedocs.io/) | Published documentation |
| [PyPI](https://pypi.org/project/sphinxcontrib-matlabdomain/) | Package distribution |
