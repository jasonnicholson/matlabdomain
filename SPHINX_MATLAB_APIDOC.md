# sphinx-matlab-apidoc

A tool to automatically generate reStructuredText files for MATLAB source code documentation, similar to `sphinx-apidoc` but specifically designed for MATLAB projects.

## Features

- 📁 **Namespace Organization**: Automatically detects and organizes files by MATLAB namespaces (+packages, @class folders)
- 📄 **Pagination**: Limits to 50 files per page, automatically creating multiple pages when needed
- 🔍 **Recursive Scanning**: Finds all `.m` files in the source directory
- ⚡ **Fast Generation**: Creates RST files ready for Sphinx build
- 🎯 **Clean Output**: Well-structured documentation with proper toctree entries

## Installation

The tool is included with sphinxcontrib-matlabdomain. After installing the package, `sphinx-matlab-apidoc` will be available as a command-line tool.

```bash
pip install -e .
```

## Usage

### Basic Usage

```bash
sphinx-matlab-apidoc <source_dir> -o <output_dir>
```

### Examples

Generate documentation for a MATLAB project:
```bash
sphinx-matlab-apidoc /path/to/matlab/project -o docs/source
```

Dry run to see what would be generated:
```bash
sphinx-matlab-apidoc /path/to/matlab/project -o docs/source --dry-run
```

Customize maximum files per page:
```bash
sphinx-matlab-apidoc /path/to/matlab/project -o docs/source --max-files 100
```

Force overwrite of existing files:
```bash
sphinx-matlab-apidoc /path/to/matlab/project -o docs/source --force
```

## Command-Line Options

- `source_dir`: Path to MATLAB source code directory (required)
- `-o, --output-dir`: Output directory for RST files (default: `docs/source`)
- `-n, --dry-run`: Show what would be done without creating files
- `-f, --force`: Overwrite existing files without prompting
- `--max-files`: Maximum number of files per page (default: 50)

## Generated Structure

The tool generates:

1. **index.rst**: Main index file with toctree of all modules
2. **Namespace RST files**: One file per namespace (e.g., `mypackage.rst`)
3. **Paginated files**: Multiple pages if namespace has >50 files (e.g., `root_page1.rst`, `root_page2.rst`)

### Example Output Structure

```
docs/source/
├── index.rst
├── root_page1.rst          # First 50 files in root
├── root_page2.rst          # Next 50 files in root
├── mypackage.rst           # Files in +mypackage
├── mypackage_subpkg.rst    # Files in +mypackage/+subpkg
└── MyClass.rst             # Files in @MyClass folder
```

## How It Works

### Namespace Detection

The tool automatically detects MATLAB namespaces from the directory structure:

- **+package folders**: `+mypackage` → namespace: `mypackage`
- **@class folders**: `@MyClass` → namespace: `MyClass`
- **Regular folders**: No namespace prefix, grouped as 'root'
- **Nested packages**: `+pkg1/+pkg2` → namespace: `pkg1.pkg2`

### File Organization

Files are organized by namespace:
```
Source:                          Namespace:
/project/function1.m            → root
/project/+pkg/function2.m       → pkg
/project/+pkg/+sub/class1.m     → pkg.sub
/project/@MyClass/method1.m     → MyClass
```

### Pagination

When a namespace contains more than 50 files:
- Creates multiple pages: `namespace_page1.rst`, `namespace_page2.rst`, etc.
- Each page contains up to 50 files
- Includes navigation links between pages
- Updates index.rst to include all pages

## Integration with Sphinx

After generating RST files:

1. Create a `conf.py` in the output directory if it doesn't exist:
```python
extensions = [
    'sphinxcontrib.matlab',
    'sphinx.ext.autodoc',
]

matlab_src_dir = '../path/to/matlab/source'
matlab_short_links = True
```

2. Build the documentation:
```bash
sphinx-build -b html docs/source docs/build
```

## Testing Results

The tool has been tested on real-world MATLAB projects:

| Project | Files | Namespaces | Pages Generated | Result |
|---------|-------|------------|-----------------|---------|
| WEC-Sim_Applications | 224 | 1 | 6 | ✅ Generated successfully |
| matnwb | 423 | 65 | 67 | ⚠️ Found extension bug |
| vhlab-toolbox-matlab | 1,723 | 91 | 107+ | ✅ Generated successfully |

See [BUG_HUNTING_RESULTS.md](BUG_HUNTING_RESULTS.md) for detailed testing results.

## Known Limitations

1. **Special Characters**: Folder names with hyphens, parentheses, or spaces may cause issues
2. **Import Paths**: Files in subdirectories may fail to import properly
3. **MATLAB Paths**: Requires proper MATLAB source directory configuration

## Contributing

This tool is part of the sphinxcontrib-matlabdomain project. Contributions and bug reports are welcome!

## License

BSD License - See LICENSE file for details
