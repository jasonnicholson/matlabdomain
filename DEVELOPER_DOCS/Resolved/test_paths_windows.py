"""
Windows path diagnostic script.

Run this on Windows to understand path handling differences.
"""

import os
import sys
from pathlib import Path

print("=" * 80)
print("WINDOWS PATH DIAGNOSTIC")
print("=" * 80)
print()

print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")
print(f"os.name: {os.name}")
print(f"os.sep: {os.sep!r}")
print(f"os.pathsep: {os.pathsep!r}")
print(f"os.linesep: {os.linesep!r}")
print()

print("=" * 80)
print("PATH OPERATIONS TEST")
print("=" * 80)
print()

# Test 1: Unix-style path
test_path = "test_data/+package/func.m"
print(f"1. Unix-style path: {test_path}")
print(f"   With os.sep:     {test_path.replace('/', os.sep)}")
print(f"   Path object:     {Path(test_path)}")
print(f"   Path as string:  {Path(test_path)!s}")
print(f"   Path.as_posix(): {Path(test_path).as_posix()}")
print()

# Test 2: Module name conversion
modname = "+package.+subpkg.func"
print(f"2. Module name: {modname}")
print(f"   Replace . with os.sep: {modname.replace('.', os.sep)}")
path_obj = Path(modname.replace(".", os.sep))
print(f"   As Path object:        {path_obj}")
print(f"   Path as string:        {path_obj!s}")
print()

# Test 3: Reverse conversion (path to module name)
if os.name == "nt":  # Windows
    win_path = "test_data\\+package\\func.m"
    print(f"3. Windows path: {win_path}")
    print(f"   Replace \\ with .:   {win_path.replace(os.sep, '.')}")
    print(f"   Using Path.as_posix(): {Path(win_path).as_posix()}")
    print(f"   Then replace / with .: {Path(win_path).as_posix().replace('/', '.')}")
else:
    unix_path = "test_data/+package/func.m"
    print(f"3. Unix path: {unix_path}")
    print(f"   Replace / with .: {unix_path.replace('/', '.')}")
print()

# Test 4: Real file operations
print("=" * 80)
print("FILE SYSTEM TEST")
print("=" * 80)
print()

test_dir = Path(__file__).parent / "tests" / "test_data"
print(f"Test directory: {test_dir}")
print(f"Exists: {test_dir.exists()}")
print(f"Is directory: {test_dir.is_dir()}")
print()

if test_dir.exists():
    # List first few MATLAB files
    matlab_files = list(test_dir.glob("*.m"))[:5]
    print(f"Found {len(matlab_files)} .m files (showing first 5):")
    for f in matlab_files:
        print(f"  - {f.name}")
        print(f"    Absolute: {f.absolute()}")
        print(f"    Relative: {f.relative_to(Path.cwd())}")
        print(f"    As posix: {f.as_posix()}")

        # Try to read first line
        try:
            with open(f, "r", encoding="utf-8") as fh:
                first_line = fh.readline().strip()
                print(f"    First line: {first_line[:60]}...")
        except Exception as e:
            print(f"    ERROR reading: {e}")
        print()
else:
    print("ERROR: Test directory not found!")
    print("Make sure you're running this from the project root")

print("=" * 80)
print("POTENTIAL ISSUES")
print("=" * 80)
print()

issues = []

# Check 1: Path separator in string operations
if os.sep == "\\":
    issues.append(
        "⚠ Windows backslash (\\) may cause issues with string replace operations"
    )
    issues.append("  Recommendation: Use pathlib.Path instead of string operations")

# Check 2: Line endings
if os.linesep == "\r\n":
    issues.append("⚠ Windows uses CRLF line endings")
    issues.append("  Check .gitattributes is working correctly")

if issues:
    for issue in issues:
        print(issue)
else:
    print("✓ No obvious issues detected")

print()
print("=" * 80)
print("END DIAGNOSTIC")
print("=" * 80)
