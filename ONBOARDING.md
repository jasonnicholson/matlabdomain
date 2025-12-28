# Repository Onboarding Summary

Welcome to the sphinxcontrib-matlabdomain project! This document provides a quick overview of what has been documented and where to go next.

---

## What Is This Project?

**sphinxcontrib-matlabdomain** is a Sphinx domain extension that enables automatic documentation generation from MATLAB source code, similar to how Python's autodoc works.

### Key Stats
- **GitHub**: https://github.com/sphinx-contrib/matlabdomain
- **PyPI**: https://pypi.org/project/sphinxcontrib-matlabdomain/
- **Docs**: https://sphinxcontrib-matlabdomain.readthedocs.io/
- **Python**: 3.8+
- **Sphinx**: 4.0+
- **License**: BSD

---

## Documentation Created for You

I've created comprehensive documentation to help you understand and contribute to this project. Here's what's available:

### 📘 **DEVELOPER_GUIDE.md** - Start Here!
The most comprehensive guide covering:
- **Project Overview** - What the project does
- **Project Structure** - How files are organized
- **Code Architecture** - What each component does
- **Data Flow** - How information moves through the system
- **Testing Strategy** - How tests are organized and run
- **CI/CD Configuration** - How automation works
- **Development Setup** - Step-by-step setup instructions
- **Tool Configuration** - ruff, pre-commit, etc.
- **Testing Commands** - How to run tests

👉 **Read this first to understand the project holistically.**

### 🐛 **IMPLEMENTATION_GUIDE.md** - Known Issues & TODOs
Documents specific work items:
- **3 Known TODOs** in the codebase with details and fixes
- **Test Ordering Issues** - test_matlabify.py edge case
- **Bug History** - Recent fixes from CHANGES.rst
- **Architecture Notes** - Future improvement areas
- **Priority Action Items** - Ranked by importance

👉 **Reference this when you want to start fixing bugs.**

### 🚀 **UV_MIGRATION.md** - Modernize the Toolchain
Complete migration plan for the uv package manager:
- **Why migrate** - Benefits of uv
- **Step-by-step implementation** - Phases 1-8
- **Timeline** - ~2 hours total work
- **CI/CD updates** - How to update GitHub Actions
- **Rollback plan** - If something goes wrong
- **Compatibility notes** - Python/Sphinx versions

👉 **Use this when you're ready to modernize the package management.**

### 📖 **SPHINX_DOCS_PLAN.md** - Improve the Documentation Site
Strategic plan for the Sphinx documentation:
- **Current state analysis** - What exists vs what's missing
- **Proposed structure** - New docs/folder organization
- **10 Key pages to create** - With detailed content outlines
- **Visual improvements** - Styling and branding
- **Maintenance plan** - How to keep docs up-to-date
- **Work breakdown** - Estimated hours per section

👉 **Reference this when improving the documentation site.**

### ⚡ **QUICK_REFERENCE.md** - Cheat Sheet
Fast lookup reference with:
- Essential commands (setup, test, build docs)
- Key files reference table
- Common workflows (feature, bug fix, docs review)
- Important configuration settings
- Troubleshooting common issues
- Git workflow and commit message style

👉 **Bookmark this and return often during development.**

---

## Quick Start (5 Minutes)

```bash
# 1. Setup development environment
git clone https://github.com/sphinx-contrib/matlabdomain.git
cd matlabdomain
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
pip install -r dev-requirements.txt
pip install -r rtd-requirements.txt
pre-commit install

# 2. Run tests to verify setup
pytest

# 3. Build documentation
cd docs && make html && cd ..
open docs/_build/html/index.html

# 4. Read DEVELOPER_GUIDE.md
# Done! You're ready to contribute
```

---

## What to Do Next

### 🎯 Option 1: Understand the Codebase (Next 1-2 hours)
1. Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) sections:
   - Project Overview
   - Project Structure
   - Code Architecture
2. Browse the main files mentioned:
   - `sphinxcontrib/matlab.py` (domain)
   - `sphinxcontrib/mat_types.py` (type system)
   - `sphinxcontrib/mat_documenters.py` (autodoc)
3. Run tests to see how it works: `pytest -v`

**Time investment**: 1-2 hours
**Benefit**: Understand how everything works

---

### 🐛 Option 2: Fix Known Bugs (Next 2-4 hours)
1. Check [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for:
   - 3 TODOs with difficulty/priority
   - Test ordering issues
   - Priority action items
2. Pick one TODO and implement it
3. Write tests for your fix
4. Run: `pytest` and `ruff check`
5. Create a pull request

**Time investment**: 2-4 hours per fix
**Benefit**: Improve project functionality

---

### 📖 Option 3: Improve Documentation (Next 3-5 hours)
1. Review [SPHINX_DOCS_PLAN.md](SPHINX_DOCS_PLAN.md)
2. Pick a section to write (installation, quick-start, etc)
3. Create .rst files in docs/
4. Build: `cd docs && make html`
5. Review in browser
6. Commit and push

**Time investment**: 3-5 hours per major doc section
**Benefit**: Help other users learn the project

---

### 🚀 Option 4: Upgrade to uv (Next 2 hours)
1. Read [UV_MIGRATION.md](UV_MIGRATION.md)
2. Follow phases 1-8:
   - Update pyproject.toml
   - Generate uv.lock
   - Test locally
   - Update CI workflows
3. Create PR with changes

**Time investment**: 2 hours
**Benefit**: Faster builds, modern tooling

---

## Project Layout at a Glance

```
sphinxcontrib-matlabdomain/
├── sphinxcontrib/          # Source code
│   ├── matlab.py          # Main domain (entry point)
│   ├── mat_types.py       # Type system (important!)
│   ├── mat_tree_sitter_parser.py  # MATLAB AST parser
│   ├── mat_documenters.py # Autodoc documenters
│   ├── mat_directives.py  # Sphinx directives
│   └── mat_lexer.py       # Syntax highlighting
├── tests/                  # Test suite
│   ├── test_*.py         # Test files
│   ├── test_data/        # Example MATLAB files
│   └── roots/            # Sphinx test configurations
├── docs/                   # Sphinx documentation
│   ├── conf.py           # Sphinx config
│   ├── index.rst         # Doc index
│   └── src/              # Example MATLAB
├── DEVELOPER_GUIDE.md     # 👈 READ THIS FIRST
├── IMPLEMENTATION_GUIDE.md # Known bugs & TODOs
├── UV_MIGRATION.md        # uv upgrade plan
├── SPHINX_DOCS_PLAN.md    # Docs improvement plan
├── QUICK_REFERENCE.md     # Cheat sheet
└── README.rst             # Original readme
```

---

## Key Concepts to Understand

### 1. **Sphinx Domain**
- Sphinx can document multiple languages via "domains"
- This project adds a domain for MATLAB (like Python, C++, etc)
- Provides roles (`:class:`, `:func:`) and directives (`.. autoclass::`)

### 2. **Documenters**
- Sphinx autodoc uses "Documenters" to extract docs from source
- We have `ClassDocumenter`, `FunctionDocumenter`, etc.
- They parse MATLAB files and generate reST content

### 3. **Type System**
- `MatType` classes represent MATLAB code elements
- `MatClass`, `MatFunction`, `MatProperty`, etc.
- `MatModuleAnalyzer` walks filesystem and builds entity tree

### 4. **Parser**
- Uses tree-sitter (AST parsing library)
- `mat_tree_sitter_parser.py` converts MATLAB AST to our types
- Handles function signatures, docstrings, class structure

### 5. **Testing Strategy**
- Use pytest with Sphinx test fixtures
- `tests/roots/` contain minimal Sphinx projects to test against
- Tests verify documentation is generated correctly

---

## Important Files to Know

| File | Why It Matters |
|------|----------------|
| `sphinxcontrib/matlab.py` | Main entry point, domain registration |
| `sphinxcontrib/mat_types.py` | Represents MATLAB code structure |
| `sphinxcontrib/mat_documenters.py` | Extracts docs from MATLAB files |
| `tests/test_autodoc.py` | Main test for autodoc functionality |
| `docs/conf.py` | Documentation configuration |
| `pyproject.toml` | Project metadata and tool configs |
| `.github/workflows/python-package.yml` | CI/CD pipeline |

---

## Common Commands

```bash
# Run tests
pytest tests/test_autodoc.py::test_target -v

# Format code
ruff format sphinxcontrib tests

# Check code quality
ruff check sphinxcontrib tests

# Build documentation
cd docs && make html && cd ..

# Run all tests with coverage
pytest --cov=sphinxcontrib

# Test multiple Python/Sphinx versions
tox
```

---

## Before You Code

### Checklist
- [ ] Set up development environment (see DEVELOPER_GUIDE.md)
- [ ] Run tests successfully: `pytest`
- [ ] Read code architecture (DEVELOPER_GUIDE.md)
- [ ] Understand the issue you're fixing (GitHub issues)
- [ ] Check if tests exist for similar functionality
- [ ] Create a branch: `git checkout -b feature/your-feature`

### Pre-Commit Hooks
Automated checks run before each commit:
- ✅ Code formatting (ruff)
- ✅ Spelling (codespell)
- ✅ Trailing whitespace
- ✅ YAML validation

If hooks fail, ruff will auto-fix most issues:
```bash
ruff format sphinxcontrib tests  # Auto-fix
git add .
git commit -m "your message"     # Try again
```

---

## Getting Help

### Documentation
1. **DEVELOPER_GUIDE.md** - Architecture & setup
2. **IMPLEMENTATION_GUIDE.md** - Known issues
3. **QUICK_REFERENCE.md** - Commands & workflows
4. **SPHINX_DOCS_PLAN.md** - Documentation strategy

### External Resources
- **Sphinx Docs**: https://www.sphinx-doc.org/
- **GitHub Issues**: Search for similar problems
- **Discussion Forum**: GitHub Discussions on the repo

### When Stuck
1. Check the relevant .md file in this folder
2. Search GitHub issues for similar problems
3. Run with verbose output: `pytest -v -s`
4. Create an issue with reproducible example

---

## Contributing Workflow

```
1. Find an issue or feature idea
   ↓
2. Create feature branch (git checkout -b feature/name)
   ↓
3. Make changes to sphinxcontrib/*.py
   ↓
4. Write or update tests
   ↓
5. Format & lint: ruff format && ruff check
   ↓
6. Run tests: pytest
   ↓
7. Commit with clear message
   ↓
8. Push and create PR (describe changes clearly)
   ↓
9. Address review feedback
   ↓
10. Merge! 🎉
```

---

## Next Steps

### Right Now (5 min)
- [ ] Read this document
- [ ] Skim DEVELOPER_GUIDE.md
- [ ] Run `pytest` to verify setup

### This Week (2-4 hours)
- [ ] Read DEVELOPER_GUIDE.md in detail
- [ ] Explore sphinxcontrib/matlab.py
- [ ] Run tests and understand what they test

### Next Tasks
- [ ] Fix one TODO from IMPLEMENTATION_GUIDE.md
- [ ] Improve one area of documentation
- [ ] Or start your own feature/bug fix

---

## Questions?

### Check These First
1. **DEVELOPER_GUIDE.md** - Comprehensive overview
2. **IMPLEMENTATION_GUIDE.md** - Specific issues
3. **QUICK_REFERENCE.md** - Common commands
4. **GitHub Issues** - Has this been discussed?

### If Still Stuck
1. Create a GitHub issue with:
   - What you're trying to do
   - What error you got
   - Steps to reproduce
2. Ask in GitHub Discussions
3. Check project's contribution guidelines

---

## Summary

You now have:
✅ Complete project overview
✅ Architecture documentation
✅ Step-by-step setup guide
✅ Known bugs with fixes
✅ Modernization plan
✅ Documentation improvement plan
✅ Quick reference cheat sheet

**Ready to contribute!** Start with [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) and pick a task from IMPLEMENTATION_GUIDE.md or SPHINX_DOCS_PLAN.md.

Good luck! 🚀

---

## Document Index

| Document | Purpose | When to Read |
|----------|---------|--------------|
| [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) | Complete project guide | First - comprehensive overview |
| [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) | Bugs & TODOs | When fixing issues |
| [UV_MIGRATION.md](UV_MIGRATION.md) | Upgrade to uv | When modernizing tooling |
| [SPHINX_DOCS_PLAN.md](SPHINX_DOCS_PLAN.md) | Documentation strategy | When improving docs |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Cheat sheet | During development |
| [ONBOARDING.md](ONBOARDING.md) | This file | Quick overview |
