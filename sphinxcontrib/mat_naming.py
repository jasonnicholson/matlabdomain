"""sphinxcontrib.mat_naming
~~~~~~~~~~~~~~~~~~~~~~~~~~

MATLAB naming helpers.

This module is the single contract point for:
- MATLAB identifier validation (including namelengthmax variants)
- package/class-folder/name normalization
- stable target-id generation for cross-reference anchors
- file-to-name mapping for callable MATLAB files (``form_matlab_name``)
- found-first resolution of duplicate canonical names

Target-ID contract (stable; changing it breaks deep links and intersphinx):

- An object's HTML anchor is ``make_target_id(name)`` where ``name`` is the
  name the object is registered under (``mat:`` directive full name).
- A module's anchor is ``make_module_target_id(modname)``
  (``"module-" + make_target_id(modname)``).
- ``make_target_id`` strips surrounding whitespace and leading dots and
  replaces each whitespace run with ``-``. Everything else (``.``, ``+``,
  ``@``, ``_``, digits, letters, non-ASCII) is kept verbatim and case is
  preserved, so every valid MATLAB name is its own anchor.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path


VALID_MATLAB_NAMELENGTHMAX = {63, 2048}

# Oldest supported MATLAB release and the default target release.
MATLAB_VERSION_FLOOR = "R2025a"
DEFAULT_MATLAB_VERSION = "R2026a"

# Version-dependent MATLAB behavior: rule -> first release with the new behavior.
# Every row needs MATLAB evidence (see plan.md, "matlab_version").
MATLAB_VERSION_RULES = {
    # namelengthmax went from 63 to 2048 (R2025a release notes).
    "namelengthmax_2048": "R2025a",
    # Scripts/functions in a subfolder of a class folder (@C/sub/x.m) stopped
    # being callable (callable in R2024a and R2025b, not in R2026a).
    "class_subfolder_not_callable": "R2026a",
}

_MATLAB_RELEASE = re.compile(r"^R(\d{4})([ab])$")

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
    is_private: bool = False


def validate_namelengthmax(namelengthmax: int) -> int:
    if (
        not isinstance(namelengthmax, int)
        or isinstance(namelengthmax, bool)
        or namelengthmax not in VALID_MATLAB_NAMELENGTHMAX
    ):
        raise ValueError(
            "matlab_namelengthmax must be one of "
            f"{VALID_MATLAB_NAMELENGTHMAX}; got {namelengthmax}."
        )
    return namelengthmax


def _release_key(release: str) -> tuple[int, str]:
    match = _MATLAB_RELEASE.match(release) if isinstance(release, str) else None
    if match is None:
        raise ValueError(
            f"matlab_version must look like 'R2026a' or 'R2025b'; got {release!r}."
        )
    return int(match.group(1)), match.group(2)


def validate_matlab_version(matlab_version: str) -> str:
    if _release_key(matlab_version) < _release_key(MATLAB_VERSION_FLOOR):
        raise ValueError(
            f"matlab_version {matlab_version} is older than the oldest supported "
            f"release {MATLAB_VERSION_FLOOR}."
        )
    return matlab_version


def has_matlab_behavior(rule: str, matlab_version: str) -> bool:
    """Return True if ``matlab_version`` includes the behavior change ``rule``."""
    return _release_key(matlab_version) >= _release_key(MATLAB_VERSION_RULES[rule])


def default_namelengthmax(matlab_version: str) -> int:
    return 2048 if has_matlab_behavior("namelengthmax_2048", matlab_version) else 63


def resolve_namelengthmax(matlab_version: str, namelengthmax: int | None) -> int:
    """Explicit ``namelengthmax`` wins; ``None`` derives it from the version."""
    validate_matlab_version(matlab_version)
    if namelengthmax is None:
        return default_namelengthmax(matlab_version)
    return validate_namelengthmax(namelengthmax)


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
    return name not in MATLAB_KEYWORDS


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
    """Anchor for a registered object name (see the module docstring)."""
    target = (canonical_name or "").strip().lstrip(".")
    return re.sub(r"\s+", "-", target)


def make_module_target_id(modname: str) -> str:
    """Anchor for a ``mat:module`` (see the module docstring)."""
    return f"module-{make_target_id(modname)}"


def short_link_modname(modname: str | None) -> str:
    """Keep only the ``+package`` parts of a module name (matlab_short_links).

    ``"target.+package"`` -> ``"+package"``; ``"target"`` -> ``""``.
    """
    return ".".join(part for part in (modname or "").split(".") if part.startswith("+"))


def registered_name_candidates(legacy_key: str) -> list[str]:
    """Names an entity with discovery key ``legacy_key`` may be registered as.

    Covers ``matlab_keep_package_prefix`` on/off, class-folder collapsing and
    ``matlab_short_links``. Ordered, without duplicates.
    """
    collapsed = classfolder_class_name(legacy_key)
    names = [
        legacy_key,
        collapsed,
        strip_package_prefix(legacy_key),
        strip_package_prefix(collapsed),
        shortest_name(legacy_key),
        shortest_name(collapsed),
    ]
    return list(dict.fromkeys(names))


def canonical_name(name: MatlabName) -> str:
    """Documentation name of a file.

    ``pseudo_fullname``, except that class-folder methods are qualified by
    their class (``pkg.C.helper``, not the callable ``helper``).
    """
    package, fullname = name.pseudo_package, name.pseudo_fullname
    if not package or fullname == package or fullname.startswith(f"{package}."):
        return fullname
    return f"{package}.{name.pseudo_name}"


def resolve_found_first(entries):
    """Resolve duplicate names like the MATLAB path: the first entry wins.

    ``entries`` is an iterable of ``(name, value)`` in precedence order (the
    caller sorts by source-root order, then path order). Returns
    ``(winners, shadowed)``: ``winners`` maps name -> first value, and
    ``shadowed`` lists ``(name, shadowed_value, winning_value)``.
    """
    winners = {}
    shadowed = []
    for name, value in entries:
        if name in winners:
            shadowed.append((name, value, winners[name]))
        else:
            winners[name] = value
    return winners, shadowed


def split_canonical(name: str, canonical_names: dict):
    """Split ``name`` into its longest known canonical prefix and the rest.

    Returns ``(canonical_names[prefix], remaining_parts)`` or ``(None, [])``;
    e.g. ``pkg.Cls.method`` -> ``(canonical_names["pkg.Cls"], ["method"])``.
    """
    parts = name.split(".")
    for i in range(len(parts), 0, -1):
        value = canonical_names.get(".".join(parts[:i]))
        if value is not None:
            return value, parts[i:]
    return None, []


def path_order_key(root_index: int, root: str, folder: str) -> tuple:
    """Sort key for MATLAB-path precedence of ``folder`` below ``root``.

    Earlier roots win; within a root, folders are ordered like ``genpath``
    (a folder before its subfolders, siblings by name).
    """
    rel = os.path.relpath(os.path.normpath(folder), os.path.normpath(root))
    parts = () if rel == os.curdir else Path(rel).parts
    return (root_index, parts)


def _split_folder(folder: str) -> list[str]:
    return list(Path(os.path.normpath(str(folder))).parts)


def _join_parts(parts: list[str]) -> str:
    if not parts:
        return ""
    out = parts[0]
    for part in parts[1:]:
        out = os.path.join(out, part)
    return out


def _package_chain(
    folder_parts: list[str], namelengthmax: int
) -> tuple[list[str], int] | None:
    """Collect trailing '+pkg' folders. Returns (segments, index below chain)."""
    segments: list[str] = []
    idx = len(folder_parts) - 1
    while idx >= 0 and folder_parts[idx].startswith("+"):
        segments.append(folder_parts[idx][1:])
        idx -= 1
    segments.reverse()
    if not segments:
        return None
    if not is_valid_identifier(segments[0], namelengthmax, allow_keywords=False):
        return None
    if not all(
        is_valid_identifier(seg, namelengthmax, allow_keywords=True)
        for seg in segments[1:]
    ):
        return None
    return segments, idx


def _location(
    folder_parts: list[str],
    namelengthmax: int,
    matlab_version: str = DEFAULT_MATLAB_VERSION,
) -> tuple[str, str, str] | None:
    """Classify a folder as (kind, qualified prefix, parent folder).

    kind is "plain", "package", "class" or "class_subfolder"; the prefix is the
    package name or the qualified class name. Returns None for folders that hold
    no callable files (invalid packages, subfolders of class folders on
    R2026a+, ...).
    """
    last = folder_parts[-1]
    folder = _join_parts(folder_parts)

    if last.startswith("@"):
        class_name = last[1:]
        if not is_valid_identifier(class_name, namelengthmax, allow_keywords=False):
            return None
        chain = _package_chain(folder_parts[:-1], namelengthmax)
        if chain is None:
            # A class folder directly under an invalid package is not callable.
            if len(folder_parts) >= 2 and folder_parts[-2].startswith("+"):
                return None
            if any(part.startswith("@") for part in folder_parts[:-1]):
                return None
            return "class", class_name, folder
        segments, idx = chain
        if any(part.startswith("@") for part in folder_parts[: idx + 1]):
            return None
        return (
            "class",
            ".".join([*segments, class_name]),
            _join_parts(folder_parts[: idx + 1]),
        )

    if last.startswith("+"):
        chain = _package_chain(folder_parts, namelengthmax)
        if chain is None:
            return None
        segments, idx = chain
        # Packages below a class folder are not callable.
        if any(part.startswith("@") for part in folder_parts[: idx + 1]):
            return None
        return "package", ".".join(segments), _join_parts(folder_parts[: idx + 1])

    # Plain folder below a class folder: scripts/functions were callable before
    # R2026a; classes never were.
    if any(part.startswith("@") for part in folder_parts[:-1]):
        if has_matlab_behavior("class_subfolder_not_callable", matlab_version):
            return None
        return "class_subfolder", "", folder
    return "plain", "", folder


def _private_name(
    folder_parts: list[str], stem: str, is_class: bool, namelengthmax: int
) -> MatlabName | None:
    if is_class or not is_valid_identifier(stem, namelengthmax, allow_keywords=False):
        return None
    parent_parts = folder_parts[:-1]
    if not parent_parts or parent_parts[-1] == "private":
        return None
    # Default (R2026a) rules on purpose: private folders below a class subfolder
    # were never verified as callable in older releases.
    if _location(parent_parts, namelengthmax) is None:
        return None
    return MatlabName(
        pseudo_name=stem,
        pseudo_package="",
        pseudo_fullname=stem,
        parent_folder=_join_parts(folder_parts),
        is_private=True,
    )


def form_matlab_name(
    folder: str,
    filename: str,
    is_class: bool,
    namelengthmax: int,
    matlab_version: str = DEFAULT_MATLAB_VERSION,
) -> MatlabName | None:
    """Forms the callable MATLAB name for a single file.

    Pure string/path function; returns None for non-callable/invalid entries.
    ``matlab_version`` selects version-dependent rules (MATLAB_VERSION_RULES).
    """
    validate_namelengthmax(namelengthmax)
    validate_matlab_version(matlab_version)

    folder_parts = _split_folder(folder)
    if not folder_parts:
        return None

    stem = Path(filename).stem
    if folder_parts[-1] == "private":
        return _private_name(folder_parts, stem, is_class, namelengthmax)

    location = _location(folder_parts, namelengthmax, matlab_version)
    if location is None:
        return None
    kind, prefix, parent_folder = location

    if kind == "class":
        class_name = folder_parts[-1][1:]
        if is_class:
            if stem != class_name:
                return None
            return MatlabName(stem, prefix, prefix, parent_folder)
        if not is_valid_identifier(stem, namelengthmax, allow_keywords=True):
            return None
        return MatlabName(stem, prefix, stem, parent_folder)

    if not is_valid_identifier(stem, namelengthmax, allow_keywords=False):
        return None

    if kind == "class_subfolder":
        if is_class:
            return None
        return MatlabName(stem, "", stem, parent_folder)
    if is_class:
        qualified = f"{prefix}.{stem}" if prefix else stem
        return MatlabName(stem, qualified, qualified, parent_folder)
    if kind == "package":
        return MatlabName(stem, prefix, f"{prefix}.{stem}", parent_folder)
    return MatlabName(stem, "", stem, parent_folder)
