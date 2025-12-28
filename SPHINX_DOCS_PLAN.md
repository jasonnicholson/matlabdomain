# Sphinx Documentation Site Improvement Plan

This document outlines the strategy for improving the project's Sphinx documentation site at https://sphinxcontrib-matlabdomain.readthedocs.io/

---

## Current State Analysis

### What Exists
- ✅ Basic README with usage examples
- ✅ Configuration options documented
- ✅ ReadTheDocs integration (reads from `docs/` folder)
- ✅ Example MATLAB files (`docs/src/times_two.m`, `times_two_napoleon.m`)
- ✅ Basic Sphinx setup with Napoleon support

### What's Missing
- ❌ Architecture/design documentation
- ❌ Developer guide (fixed - see DEVELOPER_GUIDE.md)
- ❌ Contributing guidelines
- ❌ Troubleshooting section
- ❌ API reference (documenting MatType classes)
- ❌ Advanced usage patterns
- ❌ Migration guides
- ❌ FAQ section
- ❌ Comparison with other documentation tools

---

## Proposed Documentation Structure

```
docs/
├── conf.py                          # Sphinx configuration (update)
├── index.rst                        # Landing page (redesign)
├── getting-started/
│   ├── installation.rst            # NEW: Installation instructions
│   ├── quick-start.rst             # NEW: 5-minute tutorial
│   └── basic-usage.rst             # Move from README
├── user-guide/
│   ├── configuration.rst           # Move from README + expand
│   ├── docstring-conventions.rst   # NEW: Best practices
│   ├── packages-and-classes.rst    # NEW: MATLAB structure
│   ├── cross-referencing.rst       # NEW: Linking patterns
│   ├── napoleon-integration.rst    # NEW: Napoleon syntax
│   └── html-customization.rst      # NEW: Styling options
├── advanced/
│   ├── large-projects.rst          # NEW: Performance tips
│   ├── custom-extensions.rst       # NEW: Extending domain
│   ├── ci-integration.rst          # NEW: GitHub Actions, etc
│   └── troubleshooting.rst         # NEW: Common issues
├── api-reference/
│   ├── matlab-domain.rst           # NEW: matlab.py API
│   ├── mat-types.rst               # NEW: MatType classes
│   ├── mat-documenters.rst         # NEW: Documenter classes
│   └── mat-parser.rst              # NEW: Parser API
├── developer/
│   ├── contributing.rst            # NEW: Contribution workflow
│   ├── architecture.rst            # NEW: Code structure
│   ├── testing.rst                 # NEW: Test strategy
│   └── roadmap.rst                 # NEW: Future plans
├── examples/
│   ├── simple-project.rst          # NEW: Step-by-step example
│   ├── package-structure.rst       # NEW: Recommended layout
│   └── classfolder-pattern.rst     # NEW: @ClassFolder example
├── src/
│   ├── times_two.m                 # Existing example
│   └── times_two_napoleon.m        # Existing example
└── _static/                         # NEW: Custom CSS/images
```

---

## Key Documentation Pages to Create

### 1. **Getting Started** (New Landing/First Page)
- What is sphinxcontrib-matlabdomain?
- Why use it (vs other MATLAB doc tools)
- 5-minute quick start example
- Link to full guide

### 2. **Installation & Setup**
- pip install
- Virtual environments
- Pre-commit setup
- IDE integration

### 3. **Configuration Reference**
- Complete list of all config options
- Default values
- Type information
- Examples for each

```rst
matlab_src_dir
~~~~~~~~~~~~~~

Type: ``str``
Default: None (not set)

Path to MATLAB source code directory. Can be:
- Absolute path
- Relative to conf.py location
- Relative to Sphinx source directory

Example::

    matlab_src_dir = "../src"
```

### 4. **Docstring Conventions Guide**
- MATLAB comment style
- Help text format
- Parameters/Returns/Examples
- Best practices
- Common mistakes

**Example MATLAB with proper docstrings**:
```matlab
classdef Example
    % Example class demonstrating docstring conventions.
    %
    % This class shows the recommended format for docstrings
    % compatible with sphinxcontrib-matlabdomain.
    
    properties
        prop1   % First property description
        prop2   % Second property with more details
    end
    
    methods
        function obj = Example(prop1, prop2)
            % Constructor
            %
            % Parameters
            % ----------
            % prop1 : <type>
            %     Description of prop1
            % prop2 : <type>
            %     Description of prop2
            %
            % Examples
            % --------
            % Create an instance::
            %
            %     obj = Example(1, 2);
            
            obj.prop1 = prop1;
            obj.prop2 = prop2;
        end
        
        function out = myMethod(obj, arg1)
            % Brief description of myMethod.
            %
            % Longer description can span multiple lines
            % and provide more context.
            %
            % Parameters
            % ----------
            % arg1 : <type>
            %     Description of arg1
            %
            % Returns
            % -------
            % out : <type>
            %     Description of output
            %
            % See Also
            % --------
            % :class:`OtherClass` : Related class
            % :func:`otherFunc` : Related function
        end
    end
end
```

### 5. **Cross-Referencing Guide**
Reference syntax examples:

```rst
Link to classes:
    :class:`mypackage.MyClass`
    :class:`MyClass` (if matlab_short_links=True)

Link to functions:
    :func:`mypackage.myFunction`
    :func:`myFunction`

Link to methods:
    :meth:`MyClass.myMethod`
    :meth:`~MyClass.myMethod` (short name only)

Link to properties:
    :attr:`MyClass.myProperty`
    :prop:`MyClass.myProperty`

In docstrings:
    See also :class:`OtherClass`, :meth:`MyClass.method`
```

### 6. **Advanced Usage Patterns**
- Using @ClassFolder structure
- Inheritance documentation
- Property getters/setters
- MATLAB apps (.mlapp)
- Enumerations

### 7. **Troubleshooting**
Common issues and solutions:

| Issue | Cause | Solution |
|-------|-------|----------|
| "Source file not found" | matlab_src_dir incorrect | Verify path in conf.py |
| Docstrings not appearing | Comment format wrong | Use proper help text format |
| Broken links | Reference doesn't exist | Check spelling and existence |
| Slow builds | Too many files | Use matlab_exclude_patterns |

### 8. **Examples**
Step-by-step walkthrough:

1. Create simple MATLAB package
2. Write Sphinx documentation
3. Build and view output
4. Common customizations

### 9. **API Reference** (Auto-generated)
Use Sphinx autodoc to document Python API:

```python
# In docs/api-reference/matlab-domain.rst
.. automodule:: sphinxcontrib.matlab
    :members:
    :undoc-members:
    :show-inheritance:
```

### 10. **Contributing Guide**
- Code of conduct
- Setting up dev environment (link to DEVELOPER_GUIDE.md)
- Submitting issues
- Pull request process
- Style guide (use ruff)

---

## Sphinx Configuration Updates

Update `docs/conf.py`:

```python
import os
import sys

# Add path for autodoc
sys.path.insert(0, os.path.abspath('..'))

project = 'sphinxcontrib-matlabdomain'
copyright = '2024 sphinxcontrib-matlabdomain contributors'
author = 'sphinxcontrib-matlabdomain contributors'
release = '0.22.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinxcontrib.matlab',
    'sphinx_rtd_theme',  # Modern theme
]

# Theme
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'titles_only': False
}

# MATLAB configuration
matlab_src_dir = os.path.abspath('../docs/src')
primary_domain = 'mat'
matlab_short_links = False

# Napoleon for docstring parsing
napoleon_use_param = True
napoleon_use_rtype = True
```

---

## Content Strategy

### Phase 1: Essential Documentation (Weeks 1-2)
- [ ] Installation guide
- [ ] Quick start (5 min example)
- [ ] Basic configuration reference
- [ ] Move README content to docs

### Phase 2: Core Content (Weeks 2-3)
- [ ] Docstring conventions guide
- [ ] Cross-referencing guide
- [ ] Configuration reference (all options)
- [ ] MATLAB structure guide

### Phase 3: Advanced Content (Weeks 3-4)
- [ ] API reference (auto-generated)
- [ ] Advanced usage patterns
- [ ] Troubleshooting guide
- [ ] Examples gallery

### Phase 4: Polish (Week 4+)
- [ ] Contributing guide
- [ ] Developer documentation
- [ ] Search optimization
- [ ] Styling/branding improvements

---

## Visual Improvements

### 1. Landing Page
Add attractive index.rst with:
- Project description
- Key features (badges, icons)
- Quick start button
- Links to main sections

### 2. Custom Styling
Create `docs/_static/custom.css`:
```css
/* Improve readability */
.rst-content code {
    font-size: 0.95em;
}

/* Highlight MATLAB code blocks */
.highlight-matlab {
    border-left: 3px solid #0066cc;
    padding-left: 10px;
}
```

### 3. Logo/Branding
- Add project logo if available
- Use consistent colors
- Add GitHub/issues badges

### 4. Responsive Design
- Ensure mobile friendly
- Test on different screen sizes

---

## Interactive Elements

### 1. Code Examples
Use literal include to keep examples DRY:
```rst
.. literalinclude:: ../src/times_two.m
    :language: matlab
    :caption: Example MATLAB function
```

### 2. Try It Online
Link to playground/sandbox if available

### 3. Video Tutorials
Consider adding links to demo videos

---

## Maintenance Plan

### Regular Updates
- [ ] Review docs quarterly
- [ ] Update examples with new releases
- [ ] Add troubleshooting for reported issues
- [ ] Keep API reference in sync with code

### Documentation Workflow
1. Update code → Add docstring
2. Write/update feature docs
3. Add test for new feature
4. PR review includes docs review
5. Merge to main → Docs auto-build on ReadTheDocs

### Docs Testing
```bash
# Build docs locally
cd docs && make html

# Check for broken links
sphinx-linkcheck docs/

# Validate reST
restructuredtext-lint docs/*.rst
```

---

## Build & Deploy

### Local Testing
```bash
cd docs
pip install -r ../rtd-requirements.txt  # or: uv sync --group docs
make html
# Open _build/html/index.html
```

### ReadTheDocs Integration
- Enabled via GitHub webhook
- Builds on every push to main
- Builds on every PR (preview)
- Published to https://sphinxcontrib-matlabdomain.readthedocs.io/

### Versioning
Document multiple versions:
- `latest` (development)
- `stable` (latest release)
- Previous major versions (0.21, 0.20, etc)

---

## Estimated Work

| Section | Pages | Est. Hours |
|---------|-------|-----------|
| Getting Started | 3 | 5 |
| User Guide | 6 | 12 |
| Advanced | 4 | 8 |
| API Reference | 3 | 6 |
| Developer | 4 | 6 |
| Examples | 3 | 5 |
| Polish/Review | - | 8 |
| **Total** | **23** | **50** |

---

## Quick Wins (Start Here)

1. **Reorganize index.rst** - Better navigation
2. **Create installation.rst** - Move from README
3. **Create quick-start.rst** - Simple example
4. **Add troubleshooting.rst** - From issues/discussions
5. **Auto-doc Python API** - Use sphinx.ext.autodoc

---

## Resources

- **Sphinx Documentation**: https://www.sphinx-doc.org/
- **Read the Docs Theme**: https://sphinx-rtd-theme.readthedocs.io/
- **reStructuredText Guide**: https://docutils.sourceforge.io/rst.html
- **Napoleon Extension**: https://sphinxext-napoleon.readthedocs.io/
