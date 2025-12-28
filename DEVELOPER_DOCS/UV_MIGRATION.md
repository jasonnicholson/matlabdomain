# Migration to uv Package Manager

This guide outlines the migration from pip/requirements.txt to `uv`, a fast Python package manager written in Rust.

## Why Migrate to uv?

### Current State (pip)
- `setup.py` - Package definition
- `pyproject.toml` - Tool configuration (already partially set up)
- `dev-requirements.txt` - Development dependencies
- `rtd-requirements.txt` - ReadTheDocs build dependencies
- Manual pip install for each environment

### Benefits of uv
✅ **Performance**: 10-100x faster dependency resolution
✅ **Consistency**: Deterministic lock files (like Poetry/Pipenv)
✅ **Simplicity**: Single tool for all Python dependency management
✅ **CI Integration**: Built-in caching, faster workflows
✅ **Modern PEP Standards**: Full support for PEP 621, PEP 508, PEP 517
✅ **Cross-platform**: Single command works on Windows, macOS, Linux

---

## Migration Plan

### Phase 1: Install uv (Already Available)

```bash
# Install uv globally (recommended)
pip install uv

# Or use uvx (uv in virtual environment)
uvx --python 3.12 --with uv uv --version
```

### Phase 2: Convert pyproject.toml (Most Important)

The project already has `pyproject.toml` with tool configuration. Update it to include dependency metadata:

**Current state**: Tool config only (ruff, codespell)
**Target state**: Full project metadata + dependencies

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "sphinxcontrib-matlabdomain"
dynamic = ["version"]
description = 'Sphinx "matlabdomain" extension'
readme = "README.rst"
license = {text = "BSD"}
authors = [
    {name = "Jørgen Cederberg", email = "jorgen@cederberg.be"}
]
requires-python = ">=3.8"

# Main dependencies
dependencies = [
    "Sphinx>=4.0.0",
    "tree-sitter-matlab>=1.0.2,<1.0.5",
    "tree-sitter>=0.21.3,<0.23.0",
]

# Optional dependencies (optional install groups)
[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-cov",
    "pre-commit",
    "defusedxml>=0.7.1",
    "sphinxcontrib-napoleon",
]

docs = [
    "sphinx",
    "sphinxcontrib-napoleon",
]

test = [
    "pytest",
    "pytest-cov",
    "defusedxml>=0.7.1",
]

[project.urls]
Homepage = "https://github.com/sphinx-contrib/matlabdomain"
Repository = "https://github.com/sphinx-contrib/matlabdomain.git"
Issues = "https://github.com/sphinx-contrib/matlabdomain/issues"
Changelog = "https://github.com/sphinx-contrib/matlabdomain/blob/master/CHANGES.rst"

[tool.setuptools]
packages = ["sphinxcontrib"]

[tool.setuptools.package-data]
sphinxcontrib = ["*.py"]
```

**See**: [Python Packaging Guide - PEP 621](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

### Phase 3: Create uv Configuration

Add to `pyproject.toml`:

```toml
[tool.uv]
# Python version to use in virtual environment
python = "3.12"

# Project metadata for uv
compile-bytecode = false
```

### Phase 4: Generate Lock File

```bash
# Create lock file with all dependencies
uv lock

# This creates uv.lock (similar to requirements.lock)
# Commit this to git for reproducible builds
git add uv.lock
git commit -m "chore: add uv lock file"
```

### Phase 5: Update Development Workflow

Replace old workflow:

```bash
# OLD WAY
python -m venv .venv
source .venv/bin/activate
pip install -r dev-requirements.txt
pip install -e .
```

With new workflow:

```bash
# NEW WAY - uv handles everything
uv sync --group dev  # Sync all deps including dev

# No need to activate venv separately:
uv run pytest        # Run pytest in uv's venv
uv run ruff check .  # Run ruff
uv run pre-commit install
```

### Phase 6: Update CI/CD Workflows

**Old GitHub Actions** (`.github/workflows/python-package.yml`):
```yaml
- name: Install dependencies
  run: |
    pip install --upgrade pip
    pip install -r dev-requirements.txt
    pip install -e .
```

**New with uv**:
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v2

- name: Install dependencies
  run: uv sync --group dev
```

**Benefits**:
- Dependency resolution cached by uv (~10x faster)
- Lock file ensures reproducible builds
- Single dependency: uv (vs pip + setuptools + wheel)

### Phase 7: Update Documentation

Replace installation instructions in README.rst:

**Before**:
```rst
Installation
============

pip install sphinxcontrib-matlabdomain

Development
-----------

pip install -r dev-requirements.txt
pre-commit install
```

**After**:
```rst
Installation
============

pip install sphinxcontrib-matlabdomain

Development
-----------

# Using uv (recommended)
uv sync --group dev
uv run pre-commit install

# Or using pip (legacy)
pip install -r dev-requirements.txt
pre-commit install
```

### Phase 8: Clean Up Old Requirements Files

After confirming everything works:

```bash
# Keep for reference initially
# git mv dev-requirements.txt docs/legacy/dev-requirements.txt
# git mv rtd-requirements.txt docs/legacy/rtd-requirements.txt

# Or just remove if confident
# git rm dev-requirements.txt rtd-requirements.txt
# git rm setup.py  # Deprecated with PEP 517
```

---

## UpdateAction tox.ini for uv

Modern approach with uv:

```ini
[tox]
envlist = py{310,311,312,313}-sphinx{53,60,70,latest}
skip_missing_interpreters = true

# Use uv to manage environments
package = skip

[testenv]
description = Run pytest with different Python/Sphinx versions

download = true

commands =
    uv run --python {basepython} -m pytest {posargs}

deps =
    .
    pytest
    defusedxml>=0.7.1
    sphinx53: Sphinx>=5.3,<5.4
    sphinx53: sphinxcontrib-devhelp==1.0.2
    # ... rest of Sphinx versions
```

Or simpler with uv-managed Python versions:

```ini
[tox]
envlist = py310-sphinx53,py311-sphinx60,py312-sphinx70,py313-sphinxlatest

[testenv]
description = Run tests with uv

deps =
    uv

commands =
    uv sync --group test
    uv run pytest {posargs}
```

---

## Step-by-Step Implementation

### 1. Create updated pyproject.toml
   ```bash
   # Edit pyproject.toml with project metadata above
   # Keep existing [tool.ruff], [tool.codespell] sections
   ```

### 2. Test lock file generation
   ```bash
   uv lock --all-extras
   cat uv.lock  # Verify it contains all dependencies
   ```

### 3. Test local development
   ```bash
   rm -rf .venv
   uv sync --group dev  # Create venv in .venv by default
   uv run pytest        # Should work
   uv run ruff check .  # Should work
   ```

### 4. Test CI locally
   ```bash
   # Simulate GitHub Actions locally
   act -j build  # Requires https://github.com/nektos/act

   # Or manually test the commands
   uv sync --group test
   uv run pytest
   uv run coverage report
   ```

### 5. Commit changes
   ```bash
   git add pyproject.toml uv.lock .github/workflows/
   git commit -m "chore: migrate to uv package manager"
   ```

---

## Compatibility Notes

### Python Versions
- `requires-python = ">=3.8"` maintains current compatibility
- uv itself works with Python 3.8+

### Sphinx Versions
- Lock file will capture exact versions used
- Different Sphinx versions tested via tox with uv

### Read the Docs
- ReadTheDocs can use uv starting from config v2
- Update `readthedocs.yml`:

```yaml
version: 2

build:
    os: ubuntu-22.04
    tools:
        python: '3.12'
        uv: 'latest'  # Add this

python:
    install:
    -   method: uv
        path: .
        extra-requirements: docs

sphinx:
    configuration: docs/conf.py
```

---

## Rollback Plan

If issues arise:

```bash
# Keep old requirements files for fallback
git stash pyproject.toml changes
pip install -r dev-requirements.txt
# Debug and create issue

# Restore after fix
git stash pop
```

---

## Benefits Summary

| Aspect | pip | uv |
|--------|-----|-----|
| Dependency Resolution | ~30-60s | ~2-10s |
| Lock File | None | uv.lock |
| Version Pinning | Via requirements.txt | Via uv.lock |
| Tool Management | External | Included |
| CI Caching | Manual | Built-in |
| Python Management | External | Via uv python |
| Configuration | Multiple files | Single pyproject.toml |

---

## Resources

- **uv Documentation**: https://docs.astral.sh/uv/
- **PEP 621**: https://peps.python.org/pep-0621/ (pyproject.toml metadata)
- **PEP 508**: https://peps.python.org/pep-0508/ (Dependency specification)
- **GitHub Actions Setup**: https://github.com/astral-sh/setup-uv

---

## Estimated Timeline

- Phase 1: Install uv - 5 min
- Phase 2-3: Update pyproject.toml - 30 min
- Phase 4: Generate lock file - 5 min
- Phase 5: Test locally - 15 min
- Phase 6: Update CI - 15 min
- Phase 7: Documentation - 20 min
- Phase 8: Cleanup & commit - 10 min

**Total**: ~2 hours for complete migration

---

## Next Steps

1. [ ] Review and update `pyproject.toml` with full project metadata
2. [ ] Run `uv lock` and verify lock file
3. [ ] Test `uv sync --group dev` locally
4. [ ] Update GitHub Actions workflow
5. [ ] Test in CI
6. [ ] Update documentation
7. [ ] Merge to main branch
8. [ ] Deprecate old requirements files (in next release)
