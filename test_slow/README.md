# Slow Integration Tests

This directory contains integration tests that validate the `sphinxcontrib-matlabdomain` plugin against real-world MATLAB projects. These tests are designed to run infrequently (e.g., in nightly CI builds) as they are slow and require network access.

## Overview

The integration test suite (`test_integration.py`) performs end-to-end testing by:

1. **Cloning Projects**: Downloads real MATLAB projects from GitHub using shallow cloning (`--filter=blob:none --depth=1`) to minimize bandwidth
2. **Using Declared Sources**: Uses explicit MATLAB source directories defined in `project_data.json`
3. **Generating Documentation**: Runs `sphinx-matlab-apidoc` to generate reStructuredText files for all MATLAB code
4. **Validating Success**: Ensures the plugin can process real-world MATLAB projects without errors

## Methodology

### Why Slow Tests?

- **Real-world validation**: Tests against actual MATLAB projects with complex structures
- **Complete workflow**: Validates the entire documentation generation pipeline
- **Error detection**: Catches plugin failures that unit tests might miss
- **Infrequent execution**: Heavy network/I/O operations make them unsuitable for regular test runs

### Test Projects

Projects are defined in `project_data.json` with explicit MATLAB source directories, for example:

```
{
	"projects": [
		{
			"url": "https://github.com/NeurodataWithoutBorders/matnwb.git",
			"matlab_src_dir": "."
		},
		{
			"url": "https://github.com/VH-Lab/vhlab-toolbox-matlab.git",
			"matlab_src_dir": "."
		},
		{
			"url": "https://github.com/WEC-Sim/WEC-Sim.git",
			"matlab_src_dir": "."
		},
		{
			"url": "https://github.com/WEC-Sim/WEC-Sim_Applications.git",
			"matlab_src_dir": "."
		},
		{
			"url": "https://github.com/jasonnicholson/regularizeNd.git",
			"matlab_src_dir": "source/"
		}
	]
}
```

Each project tests different aspects:
- **matnwb**: Large project with complex namespace hierarchies and class structures
- **vhlab-toolbox-matlab**: Multiple packages with various MATLAB patterns
- **WEC-Sim / WEC-Sim_Applications**: Application-heavy structure
- **regularizeNd**: Simpler project structure for baseline testing (source in `source/`)

### How It Works

#### 1. Project Cloning
```bash
git clone --filter=blob:none --depth=1 <URL> <local_path>
```

The `--filter=blob:none` flag enables Git's partial clone feature, downloading only file metadata and commit history while deferring blob (file content) downloads. Combined with `--depth=1`, this significantly reduces bandwidth and cloning time.

#### 2. Source Directory Selection
The test uses the MATLAB source directory specified in `project_data.json` for each project. No auto-discovery is performed.

#### 3. Documentation Generation
```bash
python -m sphinxcontrib.sphinx_matlab_apidoc <matlab_source> -o <docs_output>
```

This generates reStructuredText files organized by MATLAB namespace, similar to `sphinx-apidoc` for Python packages. The tests validate that:
- No encoding errors occur when reading MATLAB files
- RST files are successfully generated for all detected MATLAB code
- The plugin handles large and complex projects without crashing

#### 4. Validation
The test checks that:
- sphinx-matlab-apidoc exits with code 0 (success)
- At least one RST file was generated
- No errors or unhandled exceptions occurred during processing

## Running the Tests

### Run all slow tests
```bash
pytest test_slow/test_integration.py -v -s -m slow
```

### Run tests for a specific project
Use a `-k` filter matching the URL or repo name, e.g.:
```bash
pytest test_slow/test_integration.py -v -s -m slow -k "matnwb"
```

### Run with coverage
```bash
pytest test_slow/test_integration.py --cov=sphinxcontrib --cov-report=html -v -s -m slow
```

### Skip slow tests in regular test runs
```bash
pytest tests/ -v  # Doesn't include test_slow/
```

By default, pytest will only run tests in the `tests/` directory. Use the `-k` flag to selectively run slow tests:

```bash
pytest -k "slow" -v
```

## Adding New Projects

Add new projects to `project_data.json` (one entry per project with `url` and `matlab_src_dir`). The test framework automatically parametrizes over this list.

## CI Integration

### Important Note

These tests are **not suitable for CI environments** because they:
- Require network access to clone large repositories
- Take 15-30+ seconds per project to complete
- Download significant amounts of data (slow and potentially expensive)

For local testing and code validation, use the regular test suite:
```bash
pytest tests/ -v
```

If you want to validate against real projects, run the slow tests locally:
```bash
pytest test_slow/ -v -s
```

## Troubleshooting

### "No MATLAB files found" skip

This means the configured `matlab_src_dir` contained no `.m` files. Check the path in `project_data.json` for that project.

### "sphinx-build" command not found

Install Sphinx:
```bash
pip install sphinx
```

### Network errors during cloning

- Check your internet connection
- Some repositories may be large or have rate limiting
- The test uses shallow cloning to minimize bandwidth

### Sphinx build failures

These indicate real issues with the matlabdomain plugin. Check:
- The generated RST files in the temporary directory (test output shows the path)
- MATLAB code patterns that trigger the issue
- Open an issue with the generated RST snippets

## Performance Characteristics

Expected test execution times (per project):
- Clone: 10-30 seconds
- Documentation generation: 5-15 seconds
- **Total per project**: ~20-45 seconds

For 5 projects: ~2-4 minutes total

## File Structure

```
test_slow/
├── test_integration.py      # Main test suite
├── project_data.json        # Project definitions (url + matlab_src_dir)
└── README.md                # This file
```

## Related Documentation

- [MATLAB Domain Documentation](../SPHINX_MATLAB_APIDOC.md)
- [Developer Guide](../DEVELOPER_DOCS/DEVELOPER_GUIDE.md)
- [Implementation Guide](../DEVELOPER_DOCS/IMPLEMENTATION_GUIDE.md)
