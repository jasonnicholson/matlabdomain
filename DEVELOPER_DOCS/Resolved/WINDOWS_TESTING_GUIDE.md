# Windows Testing Guide

This guide walks through testing sphinxcontrib-matlabdomain on Windows to identify and fix platform-specific issues.

---

## Prerequisites

**On your Windows machine:**
- Python 3.8+ installed
- Git for Windows
- PowerShell or Command Prompt
- Text editor (VS Code, Notepad++, etc.)

---

## Step 1: Clone and Setup

### Clone the Repository

```powershell
# In PowerShell
cd C:\Users\YourUsername\Desktop
git clone <your-repo-url> matlabdomain
cd matlabdomain
```

### Create Virtual Environment

```powershell
# Create venv
python -m venv .venv

# Activate (PowerShell)
.\.venv\Scripts\Activate.ps1

# Or activate (Command Prompt)
.\.venv\Scripts\activate.bat
```

**If you get execution policy error**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Install Dependencies

```powershell
# Install package in development mode
pip install -e .

# Install dev dependencies
pip install -r dev-requirements.txt
```

**Expected output**: All packages install successfully

---

## Step 2: Run Tests and Collect Failures

### Run All Tests

```powershell
python -m pytest -v
```

### Expected Issues

Based on code analysis, we expect these types of failures:

#### 1. **Path Separator Issues**
**Symptom**: Tests fail with path mismatches
```
Expected: 'package.subpkg.func'
Got:      'package\\subpkg\\func'
```

**Location**: `mat_types.py` lines 419, 497, 577

#### 2. **Test Assertion Failures**
**Symptom**: String comparisons fail due to paths
```
AssertionError: '+package/func.m' != '+package\\func.m'
```

#### 3. **File Not Found Errors**
**Symptom**: MATLAB files not found due to wrong path construction
```
FileNotFoundError: [Errno 2] No such file or directory: 'test_data\\+package/func.m'
```

### Document Failures

**Create a file `windows-test-results.txt`** with:
```
Python Version: [run `python --version`]
Date: [today's date]
Number of tests: [total collected]
Passed: [X]
Failed: [Y]
Errors: [Z]

Failed Tests:
=============
[Paste full output of failed tests here]
```

---

## Step 3: Run Specific Test Categories

To narrow down issues, run tests by category:

### Parser Tests
```powershell
python -m pytest tests/test_parse_mfile.py -v
```
**What to check**: File reading, path handling

### Module Analysis Tests
```powershell
python -m pytest tests/test_matlabify.py -v
```
**What to check**: Module discovery, path conversion

### Integration Tests
```powershell
python -m pytest tests/test_autodoc.py -v
```
**What to check**: Full workflow with Sphinx

### Path-Specific Tests
```powershell
python -m pytest tests/test_module_class_names.py -v
python -m pytest tests/test_classfolder.py -v
python -m pytest tests/test_package_links.py -v
```
**What to check**: Package/module name resolution

---

## Step 4: Investigate Specific Failures

### Check Path Separators

Run this diagnostic script:

**Create `test_paths_windows.py`**:
```python
import os
import sys
from pathlib import Path

print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")
print(f"os.sep: {repr(os.sep)}")
print(f"os.pathsep: {repr(os.pathsep)}")
print(f"os.linesep: {repr(os.linesep)}")
print()

# Test path operations
test_path = "test_data/+package/func.m"
print(f"Original: {test_path}")
print(f"With os.sep: {test_path.replace('/', os.sep)}")
print(f"Path object: {Path(test_path)}")
print(f"Path as string: {str(Path(test_path))}")
print()

# Test module name conversion
modname = "+package.+subpkg.func"
print(f"Module name: {modname}")
print(f"Replace . with sep: {modname.replace('.', os.sep)}")
print()

# Test reverse conversion
winpath = "test_data\\+package\\func.m"
print(f"Windows path: {winpath}")
print(f"Replace sep with .: {winpath.replace(os.sep, '.')}")
print(f"Using Path: {Path(winpath).as_posix()}")
```

**Run it**:
```powershell
python test_paths_windows.py
```

**Share the output** - this will help identify exact issues

---

## Step 5: Check Specific Files

### File 1: mat_types.py Line 419

```python
# Current code (problematic on Windows)
objname = objname.replace(".", os.sep)
fullpath = os.path.join(MatObject.basedir, objname)
```

**Check**: Does this create valid paths on Windows?

### File 2: mat_types.py Line 497

```python
# Current code (problematic on Windows)
modname = path.replace(os.sep, ".")
```

**Check**: Does this correctly convert `+package\\func` to `+package.func`?

### File 3: mat_types.py Line 577

Similar to above - converts paths to module names.

---

## Step 6: Test MATLAB File Discovery

Create a simple test:

**Create `test_discovery_windows.py`**:
```python
import os
from pathlib import Path

# Point to test data
test_dir = Path(__file__).parent / "tests" / "test_data"

print(f"Looking in: {test_dir}")
print(f"Exists: {test_dir.exists()}")
print()

# Walk the directory
for root, dirs, files in os.walk(test_dir):
    matlab_files = [f for f in files if f.endswith('.m')]
    if matlab_files:
        print(f"Directory: {root}")
        for f in matlab_files:
            full_path = os.path.join(root, f)
            print(f"  - {f}")
            print(f"    Full: {full_path}")

            # Try to read it
            try:
                with open(full_path, 'r', encoding='utf-8') as fh:
                    first_line = fh.readline()
                print(f"    First line: {first_line.strip()}")
            except Exception as e:
                print(f"    ERROR: {e}")
        print()
```

**Run it**:
```powershell
python test_discovery_windows.py
```

**What to check**: Are all MATLAB files found and readable?

---

## Step 7: Test Line Endings

Check if CRLF vs LF causes issues:

**Create `test_line_endings.py`**:
```python
import os
from pathlib import Path

test_file = Path("tests/test_data/ClassExample.m")

# Read as binary to see actual line endings
with open(test_file, 'rb') as f:
    content = f.read()

    # Count line endings
    crlf_count = content.count(b'\r\n')
    lf_only = content.count(b'\n') - crlf_count

    print(f"File: {test_file}")
    print(f"CRLF (\\r\\n): {crlf_count}")
    print(f"LF only (\\n): {lf_only}")

    if crlf_count > 0:
        print("WARNING: File has Windows line endings (CRLF)")
        print("This may cause issues in parsing")
    else:
        print("OK: File has Unix line endings (LF)")

# Test if parser handles both
print("\nTesting parser with different line endings...")

from sphinxcontrib.mat_types import MatClass

try:
    cls = MatClass(str(test_file))
    print(f"✓ Parser handled the file successfully")
    print(f"  Class name: {cls.name}")
    print(f"  Methods: {len(cls.methods)}")
except Exception as e:
    print(f"✗ Parser failed: {e}")
```

**Run it**:
```powershell
python test_line_endings.py
```

---

## Step 8: Document Findings

**Create `WINDOWS_ISSUES.md`** with:

```markdown
# Windows Testing Results

## Environment
- OS: Windows [version]
- Python: [version]
- Date: [date]

## Test Results
- Total tests: X
- Passed: X
- Failed: X
- Errors: X

## Issues Found

### Issue 1: [Description]
**Test**: test_name
**Error**: [error message]
**Root cause**: [explanation]
**Location**: file.py:line
**Fix needed**: [description]

### Issue 2: [Description]
...

## Files to Fix
1. mat_types.py - Path separator handling
2. [other files]

## Next Steps
1. [ordered list of fixes]
```

---

## Step 9: Share Results

**Send to collaborator**:
1. `windows-test-results.txt` - Full test output
2. `WINDOWS_ISSUES.md` - Analysis
3. Output from diagnostic scripts
4. Screenshots if helpful

---

## Common Windows-Specific Issues

### Issue: Import Errors
**Symptom**: `ModuleNotFoundError`
**Cause**: Case-sensitive imports on case-insensitive filesystem
**Fix**: Check import statement capitalization

### Issue: Permission Errors
**Symptom**: `PermissionError` when running tests
**Cause**: File in use by another process
**Fix**: Close editors, antivirus interference

### Issue: Long Paths
**Symptom**: `FileNotFoundError` with long paths
**Cause**: Windows MAX_PATH limitation (260 chars)
**Fix**: Enable long path support or use shorter paths

### Issue: Unicode in Paths
**Symptom**: `UnicodeDecodeError`
**Cause**: Windows default encoding
**Fix**: Ensure UTF-8 encoding everywhere

---

## Quick Command Reference

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Run all tests
python -m pytest -v

# Run specific test
python -m pytest tests/test_autodoc.py::test_target -v

# Run with verbose output
python -m pytest -vv -s

# See print statements
python -m pytest -s

# Stop on first failure
python -m pytest -x

# Show locals on failure
python -m pytest -l

# Generate coverage report
python -m pytest --cov=sphinxcontrib --cov-report=html
```

---

## After Testing

Once you have results:
1. Share findings (failures, diagnostic output)
2. We'll create fixes together
3. Test fixes on Windows
4. Verify on Linux (should still pass)
5. Update CI_AND_PLATFORM_FIXES.md with learnings
6. Prepare to add Windows/macOS to CI

---

## Tips

**Use PowerShell ISE or VS Code** for easier testing
- Syntax highlighting
- Integrated terminal
- Easy file navigation

**Install Windows Terminal** (optional but recommended)
- Better terminal experience
- Multiple tabs
- Better font rendering

**Keep a test log** as you go
- Note what works and what doesn't
- This helps identify patterns
- Makes fixes easier
