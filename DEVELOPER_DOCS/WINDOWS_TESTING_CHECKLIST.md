# Windows Testing Checklist

Use this checklist when testing on your Windows machine.

## Before You Start

- [ ] Windows machine ready
- [ ] Python 3.8+ installed
- [ ] Git for Windows installed
- [ ] Editor ready (VS Code, etc.)

## Setup (Do Once)

- [ ] Clone repository to Windows machine
- [ ] Navigate to project directory
- [ ] Create virtual environment: `python -m venv .venv`
- [ ] Activate venv: `.\.venv\Scripts\Activate.ps1` (PowerShell)
- [ ] Install package: `pip install -e .`
- [ ] Install dev dependencies: `pip install -r dev-requirements.txt`
- [ ] Verify installation: `python -c "import sphinxcontrib.matlab; print('OK')"`

## Run Diagnostics

- [ ] Run path diagnostic: `python test_paths_windows.py`
- [ ] Save output to: `windows-diagnostic-output.txt`
- [ ] Review output for warnings

## Run Tests

- [ ] Run all tests: `python -m pytest -v > windows-test-full.txt 2>&1`
- [ ] Count results:
  - Total: ___
  - Passed: ___
  - Failed: ___
  - Errors: ___
  - xfailed: ___

## If Tests Fail

- [ ] Run specific category tests:
  - [ ] Parser: `python -m pytest tests/test_parse_mfile.py -v`
  - [ ] Matlabify: `python -m pytest tests/test_matlabify.py -v`
  - [ ] Autodoc: `python -m pytest tests/test_autodoc.py -v`
  - [ ] Module names: `python -m pytest tests/test_module_class_names.py -v`

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

- [ ] Copy these files to share:
  - [ ] `windows-test-full.txt`
  - [ ] `windows-diagnostic-output.txt`
  - [ ] `WINDOWS_ISSUES.md`
  - [ ] Screenshots (if helpful)

## After Fixes

- [ ] Pull latest fixes from Linux machine
- [ ] Re-run tests: `python -m pytest -v`
- [ ] Verify all tests pass
- [ ] Document any remaining issues

## Notes

Write any observations here:
-
-
-

## Questions

Write any questions here:
-
-
-
