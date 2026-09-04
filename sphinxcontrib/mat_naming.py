"""sphinxcontrib.mat_naming
~~~~~~~~~~~~~~~~~~~~~~~~~~

MATLAB naming helpers.

This module is the single contract point for:
- MATLAB identifier validation (including namelengthmax variants)
- package/class-folder/name normalization
- stable target-id generation for cross-reference anchors
- file-to-name mapping for callable MATLAB files
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path


VALID_MATLAB_NAMELENGTHMAX = {63, 2048}

# MATLAB language keywords. Top-level package names cannot use these.
# https://www.mathworks.com/help/releases/R2026a/matlab/ref/iskeyword.html
MATLAB_KEYWORDS = frozenset(
    {
        "break",
        "case",
        "catch",
        "classdef",
        "continue",
        "else",
        "elseif",
        "end",
        "for",
        "function",
        "global",
        "if",
        "otherwise",
        "parfor",
        "persistent",
        "return",
        "spmd",
        "switch",
        "try",
        "while",
    }
)


@dataclass(frozen=True)
class MatlabName:
    pseudo_name: str
    pseudo_package: str
    pseudo_fullname: str
    parent_folder: str


def validate_namelengthmax(namelengthmax: int) -> int:
    if namelengthmax not in VALID_MATLAB_NAMELENGTHMAX:
        raise ValueError(
            "matlab_namelengthmax must be one of "
            f"{VALID_MATLAB_NAMELENGTHMAX}; got {namelengthmax}."
        )
    return namelengthmax


def _identifier_pattern(namelengthmax: int) -> re.Pattern[str]:
    validate_namelengthmax(namelengthmax)
    return re.compile(rf"^[A-Za-z][A-Za-z0-9_]{{0,{namelengthmax - 1}}}$")


def is_valid_identifier(
    name: str,
    namelengthmax: int,
    *,
    allow_keywords: bool,
) -> bool:
    if not isinstance(name, str) or not name:
        return False
    if not _identifier_pattern(namelengthmax).match(name):
        return False
    if allow_keywords:
        return True
    return name.lower() not in MATLAB_KEYWORDS


def strip_package_prefix(varname: str | None) -> str | None:
    """Remove leading '+' prefix from package segments in dotted names."""
    if not varname:
        return varname
    return ".".join(part.lstrip("+") for part in varname.split("."))


def classfolder_class_name(dotted_path: str) -> str:
    """Collapse @ClassFolder.ClassFolder -> ClassFolder for classfolder roots."""
    if "@" not in dotted_path:
        return dotted_path

    parts = dotted_path.split(".")
    if len(parts) == 1:
        return dotted_path  

    stripped_parts = [part.lstrip("@") for part in parts]
    if stripped_parts[-1] == stripped_parts[-2]:
        return ".".join([*parts[:-2], stripped_parts[-1]])
    return dotted_path


def shortest_name(dotted_path: str) -> str:
    """Create shortest valid MATLAB name from a dotted traversal path."""
    parts = dotted_path.split(".")
    if len(parts) == 1:
        return parts[0].lstrip("+")

    if "@" in dotted_path:
        return dotted_path

    parts_to_keep = []
    for part in parts[:-1]:
        if part.startswith("+"):
            parts_to_keep.append(part.lstrip("+"))
        elif len(parts_to_keep) > 0:
            parts_to_keep = []

    parts_to_keep.append(parts[-1].lstrip("+"))
    return ".".join(parts_to_keep)


def make_target_id(canonical_name: str) -> str:
    """Stable target-id contract for rendered anchors.

    This currently preserves legacy behavior (dotted canonical names) while
    normalizing leading dots and whitespace. Keeping this helper as the single
    call site allows future explicit migrations without touching directive/xref
    code paths.
    """
    target = (canonical_name or "").strip().lstrip(".")
    return re.sub(r"\s+", "-", target)


def _split_folder(folder: str) -> list[str]:
    return list(Path(os.path.normpath(str(folder))).parts)


def _join_parts(parts: list[str]) -> str:
    if not parts:
        return ""
    out = parts[0]
    for part in parts[1:]:
        out = os.path.join(out, part)
    return out


def _form_package(folder_parts: list[str], namelengthmax: int) -> tuple[str, str]:
    package_parts_reversed: list[str] = []
    idx = len(folder_parts) - 1
    while idx >= 0 and folder_parts[idx].startswith("+"):
        candidate = folder_parts[idx][1:]
        if not is_valid_identifier(
            candidate, namelengthmax, allow_keywords=True
        ):
            return "", ""
        package_parts_reversed.append(candidate)
        idx -= 1

    if not package_parts_reversed:
        return "", ""

    # Package levels below a classfolder are not callable.
    if idx >= 0 and folder_parts[idx].startswith("@"):
        return "", ""

    # first package level must be isvarname-like.
    top_package = package_parts_reversed[-1]
    if not is_valid_identifier(top_package, namelengthmax, allow_keywords=False):
        return "", ""

    package = ".".join(reversed(package_parts_reversed))
    parent = _join_parts(folder_parts[: len(folder_parts) - len(package_parts_reversed)])
    return package, parent


def _no_package_no_folderclass(
    folder: str,
    filename: str,
    is_class: bool,
    process_classes: bool,
    namelengthmax: int,
) -> MatlabName | None:
    stem = Path(filename).stem
    if not is_valid_identifier(stem, namelengthmax, allow_keywords=False):
        return None

    if is_class:
        if not process_classes:
            return None
        return MatlabName(
            pseudo_name=stem,
            pseudo_package=stem,
            pseudo_fullname=f"{stem}.{stem}",
            parent_folder=folder,
        )

    return MatlabName(
        pseudo_name=stem,
        pseudo_package="",
        pseudo_fullname=stem,
        parent_folder=folder,
    )


def _no_package_folderclass(
    folder: str,
    folder_parts: list[str],
    filename: str,
    is_class: bool,
    namelengthmax: int,
) -> MatlabName | None:
    stem = Path(filename).stem
    if not is_valid_identifier(stem, namelengthmax, allow_keywords=False):
        return None

    class_candidate = folder_parts[-1][1:] if folder_parts and folder_parts[-1].startswith("@") else ""
    if not is_valid_identifier(class_candidate, namelengthmax, allow_keywords=False):
        return None

    is_valid_folder_class_def = is_class and stem == class_candidate
    is_valid_non_classdef = not is_class
    if not (is_valid_folder_class_def or is_valid_non_classdef):
        return None

    return MatlabName(
        pseudo_name=stem,
        pseudo_package=class_candidate,
        pseudo_fullname=f"{class_candidate}.{stem}",
        parent_folder=folder,
    )


def _combine_package_name(
    package: str,
    parent_folder: str,
    item: MatlabName | None,
) -> MatlabName | None:
    if not package or item is None or not item.pseudo_name:
        return None

    if item.pseudo_package:
        pseudo_package = f"{package}.{item.pseudo_package}"
    else:
        pseudo_package = package

    return MatlabName(
        pseudo_name=item.pseudo_name,
        pseudo_package=pseudo_package,
        pseudo_fullname=f"{pseudo_package}.{item.pseudo_name}",
        parent_folder=parent_folder,
    )


def form_matlab_name(
    folder: str,
    filename: str,
    is_class: bool,
    namelengthmax: int,
) -> MatlabName | None:
    """Forms the callable MATLAB name for a single file.

    Returns None for non-callable/invalid entries.
    """
    validate_namelengthmax(namelengthmax)

    folder_parts = _split_folder(folder)
    if not folder_parts:
        return None

    possible_package = folder_parts[-1].startswith("+")
    possible_folder_class = folder_parts[-1].startswith("@")
    possible_subfolder_of_folder_class = any(
        part.startswith("@") for part in folder_parts[:-1]
    )
    possible_package_folder_class = (
        possible_folder_class
        and len(folder_parts) >= 2
        and folder_parts[-2].startswith("+")
    )

    no_package_no_folder_class = (
        not possible_package
        and not possible_folder_class
        and not possible_subfolder_of_folder_class
    )
    if no_package_no_folder_class:
        return _no_package_no_folderclass(
            folder, filename, is_class, True, namelengthmax
        )

    no_package_folder_class = (
        possible_folder_class
        and not possible_subfolder_of_folder_class
        and not possible_package_folder_class
    )
    if no_package_folder_class:
        return _no_package_folderclass(
            folder, folder_parts, filename, is_class, namelengthmax
        )

    subfolder_of_folder_class = (
        possible_subfolder_of_folder_class
        and not is_class
        and not possible_package
        and not possible_folder_class
    )
    if subfolder_of_folder_class:
        return _no_package_no_folderclass(
            folder, filename, is_class, False, namelengthmax
        )

    if possible_package_folder_class:
        package, parent_folder = _form_package(folder_parts[:-1], namelengthmax)
        folder_item = _no_package_folderclass(
            folder, folder_parts, filename, is_class, namelengthmax
        )
        return _combine_package_name(package, parent_folder, folder_item)

    package, parent_folder = _form_package(folder_parts, namelengthmax)
    package_item = _no_package_no_folderclass(
        folder, filename, is_class, True, namelengthmax
    )
    return _combine_package_name(package, parent_folder, package_item)