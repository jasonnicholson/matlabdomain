#!/usr/bin/env python3
"""
sphinx-matlab-apidoc
~~~~~~~~~~~~~~~~~~~~

Generate reStructuredText files for MATLAB source code documentation.

Similar to sphinx-apidoc but specifically designed for MATLAB projects.
Generates RST files per namespace and limits to 50 code files per page.

:copyright: Copyright 2024 by the sphinxcontrib-matlabdomain team.
:license: BSD, see LICENSE for details.
"""

import argparse
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

MATLAB_EXTENSIONS = {".m"}
MAX_FILES_PER_PAGE = 50


def find_matlab_files(source_dir: Path) -> List[Path]:
    """Find all MATLAB files in the source directory."""
    matlab_files = []
    for root, dirs, files in os.walk(source_dir):
        # Skip hidden directories and common non-source directories
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".") and d not in ["private", "__pycache__"]
        ]

        for file in files:
            if any(file.endswith(ext) for ext in MATLAB_EXTENSIONS):
                file_path = Path(root) / file
                matlab_files.append(file_path)

    return sorted(matlab_files)


def get_namespace_from_path(file_path: Path, source_dir: Path) -> str:
    """
    Extract namespace from file path.

    MATLAB namespaces are indicated by + prefix in directory names.
    For example: +mypackage/+subpackage/MyClass.m -> mypackage.subpackage
    """
    relative_path = file_path.relative_to(source_dir)
    parts = list(relative_path.parts[:-1])  # Exclude filename

    namespace_parts = []
    for part in parts:
        if part.startswith("+"):
            # Remove the + prefix for namespace
            namespace_parts.append(part[1:])
        elif part.startswith("@"):
            # Class folders - include without @
            namespace_parts.append(part[1:])

    if namespace_parts:
        return ".".join(namespace_parts)
    return "root"


def organize_by_namespace(
    matlab_files: List[Path], source_dir: Path
) -> Dict[str, List[Path]]:
    """Organize MATLAB files by their namespace."""
    namespace_files = defaultdict(list)

    for file_path in matlab_files:
        namespace = get_namespace_from_path(file_path, source_dir)
        namespace_files[namespace].append(file_path)

    return dict(namespace_files)


def generate_module_rst(
    files: List[Path],
    source_dir: Path,
    namespace: str,
    page_num: int = 0,
    total_pages: int = 1,
) -> str:
    """Generate RST content for a module/namespace."""

    # Create title
    if namespace == "root":
        if total_pages > 1:
            title = f"Root Module (Page {page_num + 1}/{total_pages})"
        else:
            title = "Root Module"
    else:
        if total_pages > 1:
            title = f"{namespace} (Page {page_num + 1}/{total_pages})"
        else:
            title = namespace

    underline = "=" * len(title)

    lines = [
        title,
        underline,
        "",
    ]

    # Add navigation if multiple pages
    if total_pages > 1:
        lines.append(".. contents:: Contents")
        lines.append("   :local:")
        lines.append("   :depth: 1")
        lines.append("")

        # Add links to other pages
        nav_links = []
        for i in range(total_pages):
            if i != page_num:
                page_name = get_rst_filename(namespace, i, total_pages)
                nav_links.append(f"   {page_name}")

        if nav_links:
            lines.append("Other pages:")
            lines.append("")
            lines.extend(nav_links)
            lines.append("")

    # Add automodule directives for each file
    for file_path in files:
        relative_path = file_path.relative_to(source_dir)
        module_name = str(relative_path.with_suffix("")).replace(os.sep, ".")

        # Remove + and @ prefixes from module name
        module_name = module_name.replace("+", "").replace("@", "")

        # Bug fix: Sanitize module name for special characters
        # Replace hyphens with underscores
        module_name = module_name.replace("-", "_")
        # Remove parentheses and spaces
        module_name = module_name.replace("(", "").replace(")", "").replace(" ", "_")
        # Handle leading digits by prefixing with 'm_' (for 'module_')
        parts = module_name.split(".")
        parts = ["m_" + p if p and p[0].isdigit() else p for p in parts]
        module_name = ".".join(parts)

        lines.append(f".. automodule:: {module_name}")
        lines.append("   :members:")
        lines.append("   :undoc-members:")
        lines.append("   :show-inheritance:")
        lines.append("")

    return "\n".join(lines)


def get_rst_filename(namespace: str, page_num: int = 0, total_pages: int = 1) -> str:
    """Generate RST filename for a namespace and page number."""
    namespace_safe = namespace.replace(".", "_")

    if total_pages > 1:
        return f"{namespace_safe}_page{page_num + 1}.rst"
    else:
        return f"{namespace_safe}.rst"


def generate_index_rst(
    namespace_files: Dict[str, List[Path]], output_dir: Path, max_files_per_page: int
) -> str:
    """Generate the main index.rst file."""
    lines = [
        "MATLAB API Documentation",
        "========================",
        "",
        ".. toctree::",
        "   :maxdepth: 2",
        "   :caption: Modules:",
        "",
    ]

    # Sort namespaces
    sorted_namespaces = sorted(namespace_files.keys())

    for namespace in sorted_namespaces:
        files = namespace_files[namespace]
        total_pages = (len(files) + max_files_per_page - 1) // max_files_per_page

        if total_pages > 1:
            for page_num in range(total_pages):
                rst_file = get_rst_filename(namespace, page_num, total_pages)
                lines.append(f"   {rst_file[:-4]}")  # Remove .rst extension
        else:
            rst_file = get_rst_filename(namespace, 0, 1)
            lines.append(f"   {rst_file[:-4]}")

    lines.append("")

    # Add indices and tables
    lines.extend(
        [
            "Indices and tables",
            "==================",
            "",
            "* :ref:`genindex`",
            "* :ref:`modindex`",
            "* :ref:`search`",
            "",
        ]
    )

    return "\n".join(lines)


def write_rst_files(
    namespace_files: Dict[str, List[Path]],
    source_dir: Path,
    output_dir: Path,
    max_files_per_page: int,
    dry_run: bool = False,
) -> None:
    """Write RST files for all namespaces."""

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Generate index.rst
    index_content = generate_index_rst(namespace_files, output_dir, max_files_per_page)
    index_path = output_dir / "index.rst"

    if dry_run:
        print(f"Would create: {index_path}")
    else:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)
        print(f"Created: {index_path}")

    # Generate RST files for each namespace
    for namespace, files in sorted(namespace_files.items()):
        total_pages = (len(files) + max_files_per_page - 1) // max_files_per_page

        print(f"\nNamespace '{namespace}': {len(files)} files, {total_pages} page(s)")

        for page_num in range(total_pages):
            start_idx = page_num * max_files_per_page
            end_idx = min(start_idx + max_files_per_page, len(files))
            page_files = files[start_idx:end_idx]

            rst_content = generate_module_rst(
                page_files, source_dir, namespace, page_num, total_pages
            )
            rst_filename = get_rst_filename(namespace, page_num, total_pages)
            rst_path = output_dir / rst_filename

            if dry_run:
                print(f"  Would create: {rst_path} ({len(page_files)} files)")
            else:
                with open(rst_path, "w", encoding="utf-8") as f:
                    f.write(rst_content)
                print(f"  Created: {rst_path} ({len(page_files)} files)")


def main():
    """Main entry point for sphinx-matlab-apidoc."""
    parser = argparse.ArgumentParser(
        description="Generate reStructuredText files for MATLAB source code documentation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  sphinx-matlab-apidoc -o docs/source /path/to/matlab/code
  sphinx-matlab-apidoc -o docs/source /path/to/matlab/code --dry-run
        """,
    )

    parser.add_argument(
        "source_dir", type=Path, help="Path to MATLAB source code directory"
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("docs/source"),
        help="Output directory for RST files (default: docs/source)",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Do not create files, just show what would be done",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Overwrite existing files"
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=50,
        help=f"Maximum files per page (default: 50)",
    )

    args = parser.parse_args()

    # Update max files per page if specified
    max_files_per_page = args.max_files

    # Validate source directory
    if not args.source_dir.exists():
        print(
            f"Error: Source directory does not exist: {args.source_dir}",
            file=sys.stderr,
        )
        return 1

    if not args.source_dir.is_dir():
        print(
            f"Error: Source path is not a directory: {args.source_dir}", file=sys.stderr
        )
        return 1

    # Check if output directory exists and is not empty
    if args.output_dir.exists() and not args.force and not args.dry_run:
        if any(args.output_dir.iterdir()):
            response = input(
                f"Output directory {args.output_dir} is not empty. Continue? [y/N] "
            )
            if response.lower() not in ["y", "yes"]:
                print("Aborted.")
                return 0

    print(f"Scanning MATLAB files in: {args.source_dir}")

    # Find all MATLAB files
    matlab_files = find_matlab_files(args.source_dir)

    if not matlab_files:
        print("Warning: No MATLAB files found!")
        return 0

    print(f"Found {len(matlab_files)} MATLAB file(s)")

    # Organize by namespace
    namespace_files = organize_by_namespace(matlab_files, args.source_dir)

    print(f"Organized into {len(namespace_files)} namespace(s)")

    # Write RST files
    write_rst_files(
        namespace_files,
        args.source_dir,
        args.output_dir,
        max_files_per_page,
        args.dry_run,
    )

    if args.dry_run:
        print("\nDry run completed. No files were created.")
    else:
        print(f"\nRST files generated in: {args.output_dir}")
        print("You can now run 'sphinx-build' to generate documentation.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
