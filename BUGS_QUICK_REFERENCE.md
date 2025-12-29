# Bugs Found - Quick Reference

## Bug #1: CRITICAL - NoneType Iteration Crash

**File**: `sphinxcontrib/mat_types.py`
**Lines**: 154-161
**Function**: `recursive_find_all(obj)`

**Current Code**:
```python
def recursive_find_all(obj):
    # Recursively finds all entities in all "modules" aka directories.
    for _, o in obj.entities:  # LINE 156 - CRASHES HERE
        if isinstance(o, MatModule):
            o.safe_getmembers()
            if o.entities:
                recursive_find_all(o)
```

**Error**:
```
Extension error (sphinxcontrib.matlab):
Handler <function analyze at 0x730027a65a20> for event 'builder-inited' threw an exception
(exception: 'NoneType' object is not iterable)
```

**Triggered By**:
- Projects with +package folders (matnwb)
- Proper MATLAB namespace structures

**Fix**:
```python
def recursive_find_all(obj):
    # Recursively finds all entities in all "modules" aka directories.
    if not hasattr(obj, 'entities') or obj.entities is None:
        return
    for _, o in obj.entities:
        if isinstance(o, MatModule):
            o.safe_getmembers()
            if o.entities:
                recursive_find_all(o)
```

---

## Bug #2: Invalid Signature for Special Characters

**File**: Generated RST files by `sphinx_matlab_apidoc.py`
**Function**: Module name generation, line ~115

**Problem**:
The following folder name patterns cause "invalid signature" errors:
- Hyphens: `Body-to-Body_Interactions` → `Body-to-Body_Interactions.B2B_Case1`
- Parentheses: `Passive (P)` → `Controls.Passive (P).wecSimInputFile`
- Spaces: `Reactive (PI)` → `Controls.Reactive (PI).wecSimInputFile`
- Leading digits: `1m-ME` → `Free_Decay.1m-ME.wecSimInputFile`

**Example Error**:
```
WARNING: invalid signature for automodule ('Body-to-Body_Interactions.B2B_Case1.wecSimInputFile') [autodoc]
WARNING: don't know which module to import for autodocumenting 'Body-to-Body_Interactions.B2B_Case1.wecSimInputFile'
```

**Current Code** (sphinx_matlab_apidoc.py, lines ~113-123):
```python
# Add automodule directives for each file
for file_path in files:
    relative_path = file_path.relative_to(source_dir)
    module_name = str(relative_path.with_suffix('')).replace(os.sep, '.')

    # Remove + and @ prefixes from module name
    module_name = module_name.replace('+', '').replace('@', '')

    lines.append(f".. automodule:: {module_name}")
```

**Fix**:
```python
# Add automodule directives for each file
for file_path in files:
    relative_path = file_path.relative_to(source_dir)
    module_name = str(relative_path.with_suffix('')).replace(os.sep, '.')

    # Remove + and @ prefixes from module name
    module_name = module_name.replace('+', '').replace('@', '')

    # Sanitize module name for special characters
    # Replace hyphens with underscores
    module_name = module_name.replace('-', '_')
    # Remove parentheses and spaces
    module_name = module_name.replace('(', '').replace(')', '').replace(' ', '_')
    # Handle leading digits by prefixing with underscore
    parts = module_name.split('.')
    parts = ['_' + p if p[0].isdigit() else p for p in parts]
    module_name = '.'.join(parts)

    lines.append(f".. automodule:: {module_name}")
```

**Note**: This may also require changes in mat_types.py to match the sanitized names.

---

## Bug #3: Failed Module Imports

**File**: `sphinxcontrib/mat_types.py`
**Context**: Module path resolution

**Problem**:
Files in subdirectories fail to import with errors like:
```
WARNING: autodoc: failed to import module 'TestCable' from module 'Cable';
the following exception was raised: No module named 'Cable.TestCable'
```

**Pattern**:
- Source file: `Cable/TestCable.m`
- Generated RST: `.. automodule:: Cable.TestCable`
- Error: Cannot find module

**Affected Modules** (203 instances in WEC-Sim):
- All files in subdirectories
- Pattern: `FolderName/FileName.m` → `FolderName.FileName`

**Root Cause**:
MATLAB's path system works differently than Python's module system:
- Regular folders are not packages in MATLAB
- Only +folders create true packages
- Files in regular folders need to be on MATLAB path

**Potential Fixes**:

1. **Option A**: Treat regular folders as flat namespace
```python
# Instead of: Cable.TestCable
# Use: TestCable (if unique) or Cable_TestCable
```

2. **Option B**: Add all folders to matlab_src_dir as searchable paths
```python
# In conf.py, collect all folders
import os
from pathlib import Path

src = Path('path/to/matlab')
all_folders = [str(d) for d in src.rglob('*') if d.is_dir()]
matlab_src_dir = [str(src)] + all_folders
```

3. **Option C**: Generate different RST for package vs non-package folders
```python
if is_package_folder(folder):  # Starts with +
    module_name = f"{namespace}.{filename}"
else:  # Regular folder
    module_name = filename  # No namespace prefix
```

---

## Testing Commands

### Reproduce Bug #1 (matnwb crash):
```bash
cd test_projects/matnwb_docs
sphinx-build -b html . _build
```

### Reproduce Bug #2 (invalid signatures):
```bash
cd test_projects/WEC-Sim_Applications_docs
sphinx-build -b html . _build 2>&1 | grep "invalid signature"
```

### Reproduce Bug #3 (failed imports):
```bash
cd test_projects/WEC-Sim_Applications_docs
sphinx-build -b html . _build 2>&1 | grep "failed to import"
```

---

## Priority Order

1. **Fix Bug #1 FIRST** - Blocks all +package projects (matnwb, many real-world projects)
2. **Fix Bug #3** - Affects nested file structures (most projects have nested files)
3. **Fix Bug #2** - Affects projects with non-standard naming (less common but still important)

---

## Testing Checklist

After fixes:
- [ ] Build matnwb without crash
- [ ] Build WEC-Sim with <50 warnings
- [ ] Build vhlab-toolbox-matlab successfully
- [ ] Verify nested files import correctly
- [ ] Verify special character folder names work
- [ ] Verify +package namespaces work
- [ ] Verify @class folders work
- [ ] Verify pagination links work

---

## Additional Investigation Needed

### Question 1: How does MATLAB handle regular folder imports?
Need to understand:
- Do files in regular folders form a package?
- How does MATLAB resolve `addpath` vs packages?
- Should we treat all folders as packages or only +folders?

### Question 2: What is the correct module name format?
Options:
- `Folder.File` (current, doesn't work)
- `File` (flat, may have collisions)
- `Folder_File` (safe but ugly)
- `+Folder.File` (keep + in name?)

### Question 3: Should we validate folder names?
Consider adding validation:
```python
def validate_folder_name(name):
    """Check if folder name is valid for documentation."""
    invalid_chars = ['-', '(', ')', ' ']
    if any(char in name for char in invalid_chars):
        logger.warning(f"Folder name '{name}' contains invalid characters")
        return False
    if name[0].isdigit():
        logger.warning(f"Folder name '{name}' starts with a digit")
        return False
    return True
```
