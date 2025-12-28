# Windows Testing Checklist

Use this checklist when testing on your Windows machine.

## Before You Start

- [x] Windows machine ready
- [x] Python 3.8+ installed
- [x] Git for Windows installed
- [x] Editor ready (VS Code, etc.)

## Setup (Do Once)

- [x] Clone repository to Windows machine
- [x] Navigate to project directory
- [x] Create virtual environment: `python -m venv .venv`
- [x] Activate venv: `.\.venv\Scripts\Activate.ps1` (PowerShell)
- [x] Install package: `pip install -e .`
- [x] Install dev dependencies: `pip install -r dev-requirements.txt`
- [x] Verify installation: `python -c "import sphinxcontrib.matlab; print('OK')"`

## Run Diagnostics

- [x] Run path diagnostic: `python test_paths_windows.py`
- [x] Save output to: `windows-diagnostic-output.txt`
- [x] Review output for warnings

## Run Tests

- [x] Run all tests: `.venv\Scripts\python.exe -m pytest -v > windows-test-full.txt 2>&1`
- [x] Count results:
  - Total: 141
  - Passed: 137
  - Failed: 0
  - Errors: 0
  - xfailed: 4

## If Tests Fail

- [ ] Run specific category tests:
  - [x] Parser: `python -m pytest tests/test_parse_mfile.py -v`. Output saved to `windows-test-parse-mfile.txt` because of failure.
  - [x] Matlabify: `python -m pytest tests/test_matlabify.py -v`
  - [x] Autodoc: `python -m pytest tests/test_autodoc.py -v`
  - [x] Module names: `python -m pytest tests/test_module_class_names.py -v`

- [ ] For each failed test, document:
  - Test name: ___________________
  - Error type: ___________________
  - Error message: ___________________
  - Stack trace location: ___________________

## Document Issues

- [ ] Create `WINDOWS_ISSUES.md` (template in WINDOWS_TESTING_GUIDE.md)
- [ ] List all failures
- [ ] Group by type (path issues, line endings, etc.)
- [ ] Prioritize by severity

## Share Results

- [x] Copy these files to share:
  - [x] `windows-test-full.txt`
  - [x] `windows-diagnostic-output.txt`
  - [x] `WINDOWS_ISSUES.md`
  - [x] Screenshots (if helpful)

## After Fixes

- [x] Pull latest fixes from Linux machine
- [x] Re-run tests: `python -m pytest -v`
- [x] Verify all tests pass
- [x] Document any remaining issues

## Notes

Write any observations here:
- Fixed Sphinx import issues: Changed `sphinx.util.logging.getLogger()` to direct imports from `sphinx.util.logging`, `sphinx.util.inspect`, and `sphinx.util.docstrings` in mat_types.py, mat_documenters.py, mat_directives.py, and matlab.py
- All tests pass on Windows after fixing imports (137 passed, 4 xfailed as expected)
- **TIP**: Use venv Python directly to avoid "No module named pytest" errors: `.venv\Scripts\python.exe -m pytest`
- **Why Windows caught this**: Windows virtual environments have stricter module isolation and different import caching behavior than Unix systems. The attribute-style access (`sphinx.util.logging`) required multiple import resolution steps that could fail under Windows' stricter conditions, while direct imports (`from sphinx.util.logging import getLogger`) bypass these intermediate steps. This reveals hidden assumptions about path handling that work "by accident" on Unix but fail on Windows.

## Questions

Write any questions here:
-
-
-
