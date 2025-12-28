# CI and Cross-Platform Fixes Plan

This document tracks the work needed to get all tests passing on Windows, Linux, and macOS.

## Current Status

### ✅ Linux (Ubuntu)
- **Status**: All tests passing (137 passed, 4 xfailed)
- **Tested on**: Ubuntu via GitHub Actions and locally
- **Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

### ❓ Windows
- **Status**: Unknown - needs testing
- **GitHub Actions**: Not configured (only runs on ubuntu-latest)
- **Known issues**: Path separators (`\` vs `/`), line endings (CRLF vs LF)

### ❓ macOS
- **Status**: Unknown - needs testing
- **GitHub Actions**: Not configured (only runs on ubuntu-latest)
- **Known issues**: File system case sensitivity

---

## Investigation Needed

### 1. Check GitHub Actions Failures
**Action**: Check actual GitHub Actions runs on the origin repository
- URL: https://github.com/sphinx-contrib/matlabdomain/actions
- Look at recent failures
- Identify which Python/Sphinx combinations fail
- Capture error messages

### 2. Identify Path Separator Issues
**Locations found** (potential Windows issues):
- `mat_types.py:419` - `objname.replace(".", os.sep)`
- `mat_types.py:497` - `path.replace(os.sep, ".")`
- `mat_types.py:577` - `path.replace(os.sep, ".")`

**Risk**: These assume single character separator. On Windows, mixing `/` and `\` could cause issues.

### 3. Test Locally on Multiple Platforms

**Linux (Current)** ✅
```bash
python -m pytest -v
# Result: 137 passed, 4 xfailed ✅
```

**Windows** (To test):
```powershell
python -m pytest -v
# Check for path-related failures
```

**macOS** (To test):
```bash
python -m pytest -v
# Check for case-sensitivity issues
```

---

## Implementation Plan

### Phase 1: Enable Multi-OS CI (Priority: HIGH)

**Task 1.1**: Update GitHub Actions workflow to test on all platforms

Current:
```yaml
runs-on: ubuntu-latest
```

Change to:
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
    sphinx-version: ["53", "60", "70", "latest"]
runs-on: ${{ matrix.os }}
```

**Considerations**:
- Will increase CI time significantly (3x more runs)
- May want to test fewer combinations initially
- Could exclude some Python/Sphinx combos on non-Linux

**Recommended initial matrix**:
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.10", "3.11", "3.12"]  # Reduced set
    sphinx-version: ["60", "70", "latest"]     # Reduced set
```

---

### Phase 2: Fix Path Handling (Priority: HIGH)

**Issue**: Code uses `os.sep` which is `\` on Windows, `/` on Unix

**Files to review**:
1. `sphinxcontrib/mat_types.py`
2. Any place that constructs file paths
3. Any place that parses module names from paths

**Strategy**: Use `pathlib.Path` for all path operations

**Example fix**:
```python
# Before
objname = objname.replace(".", os.sep)
fullpath = os.path.join(MatObject.basedir, objname)

# After
from pathlib import Path
objname_path = Path(objname.replace(".", os.sep))
fullpath = Path(MatObject.basedir) / objname_path
```

**Benefits**:
- `pathlib.Path` handles separators automatically
- Works consistently across platforms
- More readable code

---

### Phase 3: Fix Line Ending Issues (Priority: MEDIUM)

**Issue**: Windows uses CRLF (`\r\n`), Unix uses LF (`\n`)

**Impact**: May affect:
- MATLAB file parsing
- Test fixtures
- String comparisons in tests

**Solution**: Ensure consistent handling
```python
# When reading files
with open(file, 'r', newline='') as f:  # Don't translate line endings
    content = f.read()

# Or normalize
content = content.replace('\r\n', '\n')
```

**Git Configuration**: Add `.gitattributes`
```
*.m text eol=lf
*.py text eol=lf
*.rst text eol=lf
```

---

### Phase 4: Test Locally Before CI (Priority: HIGH)

**Windows Testing Checklist**:
- [ ] Clone repo on Windows machine
- [ ] Create virtual environment
- [ ] Install dependencies: `pip install -e . && pip install -r dev-requirements.txt`
- [ ] Run tests: `pytest -v`
- [ ] Document failures
- [ ] Check path separator issues
- [ ] Check line ending issues

**macOS Testing Checklist**:
- [ ] Clone repo on macOS machine
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Run tests: `pytest -v`
- [ ] Document failures
- [ ] Check case-sensitivity issues (HFS+ vs APFS)

---

### Phase 5: Fix Identified Issues (Priority: HIGH)

Based on test results, fix issues in priority order:

1. **Path separator bugs** - Breaks core functionality
2. **Test assertion failures** - Tests expect Unix paths
3. **Import errors** - Windows-specific module issues
4. **Performance issues** - Slower file I/O on some platforms

---

## Code Review Areas

### Areas Likely to Have Platform Issues:

**1. File Path Construction**
```python
# mat_types.py
os.path.join(app.env.srcdir, app.env.config.matlab_src_dir)
objname.replace(".", os.sep)
path.replace(os.sep, ".")
```

**2. Directory Traversal**
```python
# mat_types.py - MatModuleAnalyzer
for dirpath, dirnames, filenames in os.walk(self.path):
    # Process files
```

**3. Test Fixtures**
```python
# tests/helper.py
rootdir = Path(__file__).parent.absolute() / "roots" / testroot
```

**4. Module Name Resolution**
```python
# Converting between paths and module names
# e.g., "+package/+subpkg/func.m" -> "package.subpkg.func"
```

---

## Testing Strategy

### Approach 1: Start with CI
**Pros**:
- Automated
- Tests all platforms simultaneously
- Documents issues

**Cons**:
- Slower feedback loop
- Uses GitHub Actions minutes
- Harder to debug

### Approach 2: Start with Local Testing
**Pros**:
- Faster iteration
- Can use debugger
- Better for investigation

**Cons**:
- Requires access to all platforms
- Manual work

### Recommended: Hybrid Approach
1. **Enable multi-OS CI** (shows current state)
2. **Let it fail** (collect all errors)
3. **Fix locally** on available platforms
4. **Push fixes and verify** in CI

---

## Quick Wins

### 1. Add .gitattributes
```
# .gitattributes
*.m text eol=lf
*.py text eol=lf
*.rst text eol=lf
*.md text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.txt text eol=lf
```

### 2. Use pathlib consistently
Replace `os.path` operations with `pathlib.Path`:
- More robust
- Platform-independent
- Cleaner code

### 3. Normalize in tests
Ensure test comparisons are platform-independent:
```python
# In tests
expected_path = str(Path(expected_path))  # Normalize
assert actual_path == expected_path
```

---

## Collaboration Workflow

**UPDATED**: Using local testing first to avoid CI costs

### Step 1: Windows Local Testing (IN PROGRESS)
✅ Created `.gitattributes` for line ending normalization
✅ Created `WINDOWS_TESTING_GUIDE.md` with detailed instructions
✅ Created `test_paths_windows.py` diagnostic script

**Next**: Test on Windows machine
1. Clone repo on Windows
2. Follow WINDOWS_TESTING_GUIDE.md
3. Run `python test_paths_windows.py`
4. Run `python -m pytest -v`
5. Document failures in `WINDOWS_ISSUES.md`

### Step 2: Analyze Windows Failures
Once test results are collected:
1. Review failures together
2. Identify root causes (path separators, line endings, etc.)
3. Prioritize fixes

### Step 3: Fix Issues Together
For each failure:
1. Identify root cause
2. Create minimal fix
3. Test on Windows (verify fix works)
4. Test on Linux (verify no regression)
5. Commit fix

### Step 4: Verify macOS (If Available)
If macOS machine available:
1. Clone and test
2. Document any macOS-specific issues
3. Fix as needed

### Step 5: Update CI (After Local Testing Complete)
Only after all platforms work locally:
1. Update `.github/workflows/python-package.yml`
2. Add Windows + macOS to test matrix
3. Push changes
4. Monitor CI runs
5. CI should pass on first try (since we tested locally)

### Step 6: Document Fixes
Update this file with:
- What failed
- Why it failed
- How it was fixed
- Lessons learned

---

## Timeline Estimate

| Phase | Task | Time Estimate |
|-------|------|---------------|
| 1 | Update CI workflow | 30 min |
| 2 | Wait for CI run | 10-20 min |
| 3 | Analyze failures | 1-2 hours |
| 4 | Fix path issues | 2-4 hours |
| 5 | Fix line endings | 1 hour |
| 6 | Fix remaining issues | 2-4 hours |
| 7 | Verify all platforms | 30 min |
| **Total** | | **8-12 hours** |

---

## Success Criteria

✅ All tests pass on:
- Ubuntu (Python 3.8-3.13, Sphinx 5.3-latest)
- Windows (Python 3.10-3.12, Sphinx 6.0-latest)
- macOS (Python 3.10-3.12, Sphinx 6.0-latest)

✅ CI runs without failures

✅ No platform-specific code paths needed

✅ Documentation updated with any platform notes

---

## Next Steps

**Immediate**:
1. [ ] Update GitHub Actions workflow to test Windows + macOS
2. [ ] Commit and push changes
3. [ ] Monitor CI run
4. [ ] Collect all failures

**Then**:
1. [ ] Create branch: `fix/cross-platform-compatibility`
2. [ ] Fix issues systematically
3. [ ] Test locally where possible
4. [ ] Create PR with fixes

**Finally**:
1. [ ] Update documentation
2. [ ] Add any Windows/macOS specific notes
3. [ ] Celebrate! 🎉

---

## Resources

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **pathlib Guide**: https://docs.python.org/3/library/pathlib.html
- **Cross-Platform Python**: https://docs.python.org/3/library/os.html#os.name
- **Testing on Windows**: https://docs.pytest.org/en/stable/
