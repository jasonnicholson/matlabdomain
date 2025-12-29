# Test Projects Summary

## Overview

Three real-world open-source MATLAB projects were used to test sphinxcontrib-matlabdomain:

## 1. WEC-Sim_Applications

**Repository**: https://github.com/WEC-Sim/WEC-Sim_Applications.git
**Description**: Wave Energy Converter Simulation applications
**Size**: 224 MATLAB files
**Structure**: Flat folder structure, no +packages

### Characteristics
- Folders with special characters (hyphens, parentheses, spaces)
- Examples: `Body-to-Body_Interactions`, `Passive (P)`, `Reactive (PI)`
- Deep nesting (up to 5 levels)
- Heavy use of `wecSimInputFile.m` and `userDefinedFunctions.m` patterns

### Test Results
- ✅ RST files generated successfully
- ⚠️ 255 warnings during Sphinx build
  - 52 invalid signature errors (special characters in folder names)
  - 203 failed imports (nested file imports)
- 📊 Generated 6 files (index + 5 pages for root namespace)

### Key Findings
- Exposed issues with special characters in folder names
- Revealed import path resolution problems
- Demonstrated need for better error handling

## 2. matnwb

**Repository**: https://github.com/NeurodataWithoutBorders/matnwb.git
**Description**: MATLAB interface for Neurodata Without Borders (NWB) format
**Size**: 423 MATLAB files
**Structure**: Proper +package namespace organization (65 namespaces)

### Characteristics
- Extensive use of +package folders
- Well-organized namespace hierarchy
- Examples: `+file/+interface`, `+io/+config/+enum`, `+types/+untyped/+datapipe`
- Mix of classes, functions, and tests
- Deep package nesting (up to 4 levels)

### Test Results
- ✅ RST files generated successfully (67 files)
- ❌ **CRITICAL**: Sphinx build crashes with "NoneType object is not iterable"
- 🐛 Discovered critical bug in mat_types.py analyze() function

### Key Findings
- Revealed critical bug preventing documentation of proper MATLAB packages
- Demonstrated the tool works with complex namespace structures
- Showed pagination works (types.core split into 2 pages)

## 3. vhlab-toolbox-matlab

**Repository**: https://github.com/VH-Lab/vhlab-toolbox-matlab.git
**Description**: MATLAB toolbox for neuroscience research
**Size**: 1,723 MATLAB files
**Structure**: Mix of +packages and regular folders (91 namespaces)

### Characteristics
- Largest test project
- Mix of namespace styles
- Examples: `+vlt/+daq/+MCCUSB1208FS`, regular folders like `dirstruct`
- Extensive root namespace (694 files)
- Wide variety of file types and patterns

### Test Results
- ✅ RST files generated successfully (107+ files)
- 📊 Root namespace paginated into 14 pages
- 🎯 Successfully handled large-scale project

### Key Findings
- Demonstrated scalability with 1,700+ files
- Showed pagination works well for large namespaces
- Proved the tool can handle mixed namespace styles
- Not attempted to build with Sphinx (would likely crash like matnwb)

## Comparative Analysis

| Metric | WEC-Sim | matnwb | vhlab-toolbox |
|--------|---------|---------|---------------|
| Files | 224 | 423 | 1,723 |
| Namespaces | 1 | 65 | 91 |
| Max Nesting | 5 | 4 | 5+ |
| Package Style | None | +packages | Mixed |
| Pages Generated | 6 | 67 | 107+ |
| Build Result | Warnings | Crash | Not tested |

## Lessons Learned

### What Works Well
1. ✅ RST generation for all project sizes and structures
2. ✅ Namespace detection (both +packages and @classes)
3. ✅ Pagination logic (handles 50-700 files per namespace)
4. ✅ Handles mixed namespace styles

### What Needs Fixing
1. ❌ Extension crashes on proper +package structures (CRITICAL)
2. ❌ Special characters in folder names cause invalid signatures
3. ❌ Import path resolution for nested files
4. ⚠️ Better error messages for invalid structures

## Recommendations

### For Testing
- ✅ Use WEC-Sim for testing folder name handling
- ✅ Use matnwb for testing +package support
- ✅ Use vhlab-toolbox for scalability testing

### For Bug Fixing
1. **Priority 1**: Fix matnwb crash (affects all +package projects)
2. **Priority 2**: Fix WEC-Sim import failures (affects nested files)
3. **Priority 3**: Handle special characters in names

### For Future Development
- Add validation mode to detect problematic file/folder names
- Improve import path generation logic
- Add support for mixed case package names
- Better handling of @class folders
- Add progress indicators for large projects

## Reproduction

To reproduce these tests:

```bash
# Clone test projects
mkdir -p test_projects
cd test_projects
git clone https://github.com/WEC-Sim/WEC-Sim_Applications.git
git clone https://github.com/NeurodataWithoutBorders/matnwb.git
git clone https://github.com/VH-Lab/vhlab-toolbox-matlab.git

# Generate RST files
cd ..
python sphinx_matlab_apidoc.py test_projects/WEC-Sim_Applications -o test_projects/WEC-Sim_docs --force
python sphinx_matlab_apidoc.py test_projects/matnwb -o test_projects/matnwb_docs --force
python sphinx_matlab_apidoc.py test_projects/vhlab-toolbox-matlab -o test_projects/vhlab_docs --force

# Try building (will reveal bugs)
cd test_projects/WEC-Sim_docs
sphinx-build -b html . _build

cd ../matnwb_docs
sphinx-build -b html . _build  # Will crash
```

## Files Generated

All test artifacts are in:
- `test_projects/WEC-Sim_Applications_docs/` - Generated RST files + build log
- `test_projects/matnwb_docs/` - Generated RST files (crash on build)
- `test_projects/vhlab_docs/` - Generated RST files

Build logs:
- `test_projects/WEC-Sim_Applications_docs/build_log_wecsim.txt`
- `test_projects/matnwb_docs/build_log_matnwb.txt`
