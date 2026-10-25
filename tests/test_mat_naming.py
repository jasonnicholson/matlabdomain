"""Tests for centralized MATLAB naming helpers."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from sphinx.errors import ConfigError

from sphinxcontrib import matlab
from sphinxcontrib.mat_naming import (
    DEFAULT_MATLAB_VERSION,
    MATLAB_VERSION_FLOOR,
    MATLAB_VERSION_RULES,
    MatlabName,
    canonical_name,
    default_namelengthmax,
    form_matlab_name,
    has_matlab_behavior,
    is_valid_identifier,
    make_module_target_id,
    make_target_id,
    path_order_key,
    registered_name_candidates,
    resolve_found_first,
    resolve_namelengthmax,
    short_link_modname,
    split_canonical,
    validate_matlab_version,
    validate_namelengthmax,
)


def test_form_matlab_name_reference_cases():
    rows = [
        ("/tmp", "demo.m", False, MatlabName("demo", "", "demo", "/tmp")),
        (
            "/tmp/+pkg",
            "demo.m",
            False,
            MatlabName("demo", "pkg", "pkg.demo", "/tmp"),
        ),
        (
            "/tmp/+pkg/+sub",
            "demo.m",
            False,
            MatlabName("demo", "pkg.sub", "pkg.sub.demo", "/tmp"),
        ),
        (
            "/tmp/@Class",
            "Class.m",
            True,
            MatlabName("Class", "Class", "Class", "/tmp/@Class"),
        ),
        (
            "/tmp/+pkg/@Class",
            "helper.m",
            False,
            MatlabName("helper", "pkg.Class", "helper", "/tmp"),
        ),
        ("/tmp/@Class/end", "x.m", False, None),
        (
            "/tmp/@Class",
            "end.m",
            False,
            MatlabName("end", "Class", "end", "/tmp/@Class"),
        ),
        ("/tmp/@Class/sub", "x.m", False, None),
        ("/tmp/+pkg/@Class/sub", "x.m", True, None),
        (
            "/tmp/+pkg/private",
            "pf.m",
            False,
            MatlabName("pf", "", "pf", "/tmp/+pkg/private", True),
        ),
        (
            "/tmp/@C/private",
            "cp.m",
            False,
            MatlabName("cp", "", "cp", "/tmp/@C/private", True),
        ),
        ("/tmp/private", "PrivCls.m", True, None),
        ("/tmp/@C/sub/private", "x.m", False, None),
        ("/tmp/private/private", "x.m", False, None),
        ("/tmp/+1bad/private", "x.m", False, None),
        (
            "/tmp/private/mcode",
            "tut.m",
            False,
            MatlabName("tut", "", "tut", "/tmp/private/mcode"),
        ),
    ]

    for folder, name, is_class, expected in rows:
        out = form_matlab_name(folder, name, is_class, namelengthmax=63)
        assert out == expected


def test_form_matlab_name_invalid_package_dropped():
    out = form_matlab_name("/tmp/+1bad", "demo.m", False, namelengthmax=63)
    assert out is None


def test_form_matlab_name_class_folder_under_invalid_package_dropped():
    assert form_matlab_name("/tmp/+for/@C", "m.m", False, namelengthmax=63) is None
    assert form_matlab_name("/tmp/+1bad/@C", "C.m", True, namelengthmax=63) is None
    assert (
        form_matlab_name("/tmp/+1bad/@C/private", "p.m", False, namelengthmax=63)
        is None
    )


def test_form_matlab_name_keyword_top_package_invalid():
    out = form_matlab_name("/tmp/+for/+nested", "demo.m", False, namelengthmax=63)
    assert out is None


def test_form_matlab_name_keyword_nested_package_valid():
    out = form_matlab_name("/tmp/+pkg/+for", "demo.m", False, namelengthmax=63)
    assert out == MatlabName("demo", "pkg.for", "pkg.for.demo", "/tmp")


def test_validate_namelengthmax_values():
    assert validate_namelengthmax(63) == 63
    assert validate_namelengthmax(2048) == 2048

    with pytest.raises(ValueError, match="matlab_namelengthmax"):
        validate_namelengthmax(64)


def test_identifier_validation_respects_namelengthmax():
    name_63 = "a" + ("b" * 62)
    name_64 = "a" + ("b" * 63)

    assert is_valid_identifier(name_63, 63, allow_keywords=False)
    assert not is_valid_identifier(name_64, 63, allow_keywords=False)
    assert is_valid_identifier(name_64, 2048, allow_keywords=False)


def test_target_id_is_stable_and_normalized():
    assert make_target_id(" package.Class ") == "package.Class"
    assert make_target_id("pkg.Class Name") == "pkg.Class-Name"


def test_ensure_configuration_validates_namelengthmax():
    env = SimpleNamespace(
        matlab_short_links=False,
        matlab_keep_package_prefix=True,
        matlab_version="R2026a",
        matlab_namelengthmax=64,
    )

    with pytest.raises(ConfigError, match="matlab_namelengthmax"):
        matlab.ensure_configuration(None, env)


def test_ensure_configuration_derives_namelengthmax_from_version():
    env = SimpleNamespace(
        matlab_short_links=False,
        matlab_keep_package_prefix=True,
        matlab_version="R2025a",
        matlab_namelengthmax=None,
    )
    matlab.ensure_configuration(None, env)
    assert env.matlab_namelengthmax == 2048


@pytest.mark.parametrize("version", ["R2024b", "2026a", "R2026c", "r2026a", None])
def test_ensure_configuration_rejects_bad_matlab_version(version):
    env = SimpleNamespace(
        matlab_short_links=False,
        matlab_keep_package_prefix=True,
        matlab_version=version,
        matlab_namelengthmax=None,
    )
    with pytest.raises(ConfigError, match="matlab_version"):
        matlab.ensure_configuration(None, env)


def test_matlab_version_rules():
    assert validate_matlab_version("R2025a") == "R2025a"
    assert validate_matlab_version("R2027b") == "R2027b"
    assert default_namelengthmax("R2025a") == 2048
    assert default_namelengthmax("R2026a") == 2048


@pytest.mark.parametrize(
    ("folder", "name", "is_class", "expected"),
    [
        ("/tmp/@C/sub", "x.m", False, MatlabName("x", "", "x", "/tmp/@C/sub")),
        (
            "/tmp/@C/sub/deeper",
            "x.m",
            False,
            MatlabName("x", "", "x", "/tmp/@C/sub/deeper"),
        ),
        (
            "/tmp/+pkg/@C/sub",
            "x.m",
            False,
            MatlabName("x", "", "x", "/tmp/+pkg/@C/sub"),
        ),
        ("/tmp/@C/sub", "K.m", True, None),
        ("/tmp/@C/sub/private", "y.m", False, None),
        ("/tmp/@C/sub/+p", "f.m", False, None),
    ],
)
def test_class_subfolder_callable_before_r2026a(folder, name, is_class, expected):
    for version in ("R2025a", "R2025b"):
        assert form_matlab_name(folder, name, is_class, 2048, version) == expected
    assert form_matlab_name(folder, name, is_class, 2048, "R2026a") is None


# --- form_matlab_name reference tests ----------------------------------------
# The reference tests use a table that drops rows without a name;
# form_matlab_name returns None for those rows, so ``_form_matlab_names``
# builds the same table.


def _form_matlab_names(rows, version="R2026a"):
    out = {}
    for folder, name, is_class in rows:
        result = form_matlab_name(folder, name, is_class, 2048, version)
        if result is not None:
            out[(folder, name)] = result
    return out


DERIVE_ROWS = [
    ("/tmp", "demo.m", False),
    ("/tmp/+pkg", "demo.m", False),
    ("/tmp/+pkg/+sub", "demo.m", False),
    ("/tmp/@Class", "Class.m", True),
    ("/tmp/+pkg/@Class", "helper.m", False),
    ("/tmp/@Class/sub", "helper.m", False),
    ("/tmp/+pkg/@Class/sub", "helper.m", False),
]


def _triple(n):
    return n.pseudo_name, n.pseudo_package, n.pseudo_fullname


def test_form_matlab_name_derives_pseudo_names_and_packages():
    # The reference tests predate R2026a: @Class/sub files are callable there.
    out = _form_matlab_names(DERIVE_ROWS, "R2025b")
    assert len(out) == 7
    assert _triple(out["/tmp", "demo.m"]) == ("demo", "", "demo")
    assert _triple(out["/tmp/+pkg", "demo.m"]) == ("demo", "pkg", "pkg.demo")
    assert _triple(out["/tmp/+pkg/+sub", "demo.m"]) == (
        "demo",
        "pkg.sub",
        "pkg.sub.demo",
    )
    assert _triple(out["/tmp/@Class", "Class.m"]) == ("Class", "Class", "Class")
    assert _triple(out["/tmp/+pkg/@Class", "helper.m"]) == (
        "helper",
        "pkg.Class",
        "helper",
    )
    assert _triple(out["/tmp/@Class/sub", "helper.m"]) == ("helper", "", "helper")
    assert _triple(out["/tmp/+pkg/@Class/sub", "helper.m"]) == ("helper", "", "helper")


def test_form_matlab_name_derives_without_class_subfolders_from_r2026a():
    out = _form_matlab_names(DERIVE_ROWS, "R2026a")
    assert set(out) == {(f, n) for f, n, _ in DERIVE_ROWS[:5]}


def test_form_matlab_name_uses_constructor_token_for_class_definitions_in_packages():
    out = _form_matlab_names(
        [("/tmp/+pkg", "Class.m", True), ("/tmp/+pkg/@Class", "Class.m", True)]
    )
    assert len(out) == 2
    for key in out:
        assert out[key].pseudo_package == "pkg.Class"
        assert out[key].pseudo_fullname == "pkg.Class"


def test_form_matlab_name_errors_when_required_columns_missing():
    with pytest.raises(TypeError):
        form_matlab_name("/tmp", "demo.m")  # is_class and namelengthmax missing


def test_form_matlab_name_warns_and_drops_files_with_invalid_package_path():
    out = _form_matlab_names(
        [("/tmp", "demo.m", False), ("/tmp/+1bad", "demo.m", False)]
    )
    assert [n.pseudo_fullname for n in out.values()] == ["demo"]


def test_form_matlab_name_warns_and_drops_class_nested_and_keyword_packages():
    rows = [
        ("/tmp", "demo.m", False),
        ("/tmp/@Class/+pkg", "demo.m", False),
        ("/tmp/+for", "demo.m", False),
    ]
    for version in ("R2025a", "R2026a"):
        out = _form_matlab_names(rows, version)
        assert [n.pseudo_fullname for n in out.values()] == ["demo"]


def test_form_matlab_name_allows_keyword_method_names_in_folder_classes():
    out = _form_matlab_names(
        [("/tmp/@Class", "end.m", False), ("/tmp/+pkg/@Class", "end.m", False)]
    )
    assert _triple(out["/tmp/@Class", "end.m"]) == ("end", "Class", "end")
    assert _triple(out["/tmp/+pkg/@Class", "end.m"]) == ("end", "pkg.Class", "end")


# --- R2026a oracle (reference/matlab_names_reference.json) -------------------

_ORACLE_EDGE_CASES = json.loads(
    (Path(__file__).parent / "naming_oracle_edge_cases.json").read_text()
)
# form_matlab_name, like the reference, names an old-style constructor in a
# package class folder; R2026a does not call it. Kept on purpose.
_KNOWN_DIVERGENCES = {("/oracle/+pkg/@Old2", "Old2.m")}


def _oracle_check(row):
    out = form_matlab_name(row["folder"], row["name"], row["is_class"], 2048, "R2026a")
    got = (
        (out.pseudo_name, out.pseudo_package, out.pseudo_fullname, out.is_private)
        if out
        else ("", "", "", False)
    )
    expected = (
        row["exp_pseudo_name"],
        row["exp_pseudo_package"],
        row["exp_pseudo_full_name"],
        row["is_private"],
    )
    return got, expected


@pytest.mark.parametrize(
    "row",
    [
        pytest.param(
            row,
            id=f"{row['folder']}/{row['name']}",
            marks=[pytest.mark.xfail(strict=True)]
            if (row["folder"], row["name"]) in _KNOWN_DIVERGENCES
            else [],
        )
        for row in _ORACLE_EDGE_CASES
        if not row["ignore"]
    ],
)
def test_oracle_edge_cases(row):
    got, expected = _oracle_check(row)
    assert got == expected


_FULL_ORACLE = Path(__file__).parents[2] / "reference" / "matlab_names_reference.json"


def _snake_keys(row):
    # The reference corpus uses camelCase column names.
    return {
        "".join(f"_{c.lower()}" if c.isupper() else c for c in k): v
        for k, v in row.items()
    }


@pytest.mark.skipif(not _FULL_ORACLE.exists(), reason="reference corpus not present")
def test_oracle_full_corpus():
    rows = [
        _snake_keys(r)
        for r in json.loads(_FULL_ORACLE.read_text())
        if not r["ignore"]
    ]
    assert len(rows) > 60000
    mismatches = []
    for row in rows:
        got, expected = _oracle_check(row)
        if got != expected:
            mismatches.append(row)
    # Every mismatch is a file MATLAB does not call for reasons the path cannot
    # show (empty file, shadowed toolbox internals, old-style class in a
    # package); the port never misnames a file MATLAB does call.
    assert all(
        not r["oracle_callable"] and not r["exp_pseudo_full_name"] for r in mismatches
    )
    assert len(mismatches) <= 11


# --- Spaces, invalid identifiers, keywords and both length limits ------------


@pytest.mark.parametrize(
    ("folder", "name", "is_class", "expected"),
    [
        ("/tmp/my folder", "demo.m", False, "demo"),
        ("/tmp/my folder/+pkg", "demo.m", False, "pkg.demo"),
        ("/tmp/+my pkg", "demo.m", False, None),
        ("/tmp", "my file.m", False, None),
        ("/tmp/@My Class", "My Class.m", True, None),
        ("/tmp/+pkg", "bad-name.m", False, None),
        ("/tmp/+pkg", "_x.m", False, None),
        ("/tmp/+pkg", "for.m", False, None),
        ("/tmp/+pkg/@C", "for.m", False, "for"),
        ("/tmp/class", "C.m", True, "C"),
        # Python keywords are ordinary MATLAB identifiers.
        ("/tmp/+lambda/+import", "def.m", False, "lambda.import.def"),
        ("/tmp/+None/@pass", "pass.m", True, "None.pass"),
        ("/tmp/import/from", "yield.m", False, "yield"),
    ],
)
def test_form_matlab_name_spaces_and_invalid_identifiers(
    folder, name, is_class, expected
):
    out = form_matlab_name(folder, name, is_class, 2048)
    assert (out.pseudo_fullname if out else None) == expected


@pytest.mark.parametrize("length", [63, 64, 2048, 2049])
def test_form_matlab_name_both_length_limits(length):
    ident = "a" * length
    for folder, name, is_class, expected in [
        (f"/tmp/+{ident}", "f.m", False, f"{ident}.f"),
        ("/tmp/+pkg", f"{ident}.m", False, f"pkg.{ident}"),
        (f"/tmp/@{ident}", f"{ident}.m", True, ident),
    ]:
        for limit in (63, 2048):
            out = form_matlab_name(folder, name, is_class, limit)
            want = expected if length <= limit else None
            assert (out.pseudo_fullname if out else None) == want


# --- matlab_version / matlab_namelengthmax -----------------------------------


def _config(version="R2026a", namelengthmax=None):
    return SimpleNamespace(
        matlab_short_links=False,
        matlab_keep_package_prefix=True,
        matlab_version=version,
        matlab_namelengthmax=namelengthmax,
    )


@pytest.mark.parametrize(
    ("version", "explicit", "expected"),
    [
        ("R2025a", None, 2048),
        ("R2026a", None, 2048),
        ("R2026a", 63, 63),
        ("R2025a", 63, 63),
        ("R2025b", 2048, 2048),
    ],
)
def test_namelengthmax_explicit_override_wins(version, explicit, expected):
    assert resolve_namelengthmax(version, explicit) == expected
    env = _config(version, explicit)
    matlab.ensure_configuration(None, env)
    assert env.matlab_namelengthmax == expected


@pytest.mark.parametrize("value", [0, 64, 2047, True, 63.0, "63"])
def test_namelengthmax_rejects_other_values(value):
    with pytest.raises(ConfigError, match="matlab_namelengthmax"):
        matlab.ensure_configuration(None, _config(namelengthmax=value))


def test_version_rules_table_drives_defaults(monkeypatch):
    # Thresholds live only in MATLAB_VERSION_RULES.
    monkeypatch.setitem(MATLAB_VERSION_RULES, "namelengthmax_2048", "R2026a")
    assert default_namelengthmax("R2025b") == 63
    assert resolve_namelengthmax("R2025b", 2048) == 2048
    assert has_matlab_behavior("class_subfolder_not_callable", "R2026a")
    assert not has_matlab_behavior("class_subfolder_not_callable", "R2025b")
    assert MATLAB_VERSION_FLOOR == "R2025a"
    assert DEFAULT_MATLAB_VERSION == "R2026a"


# --- Target-ID contract -------------------------------------------------------


def test_target_id_is_identity_for_matlab_names():
    # Existing anchors are the registered names, so they must not change.
    names = {
        canonical_name(n)
        for r in _ORACLE_EDGE_CASES
        if (n := form_matlab_name(r["folder"], r["name"], r["is_class"], 2048))
    }
    names |= {
        "+pkg.@Cls.Cls",
        "target.+package.ClassBar",
        "pkg.Cls.method",
        "naïve.Ünïcode",
        "a" * 2048,
    }
    for name in names:
        assert make_target_id(name) == name
        assert make_module_target_id(name) == f"module-{name}"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        (" package.Class ", "package.Class"),
        ("pkg.Class Name", "pkg.Class-Name"),
        ("my  folder.f", "my-folder.f"),
        ("..f", "f"),
        ("", ""),
        (None, ""),
    ],
)
def test_target_id_normalization(name, expected):
    assert make_target_id(name) == expected


def test_target_id_is_unique_for_distinct_matlab_names():
    names = {
        canonical_name(n)
        for r in _ORACLE_EDGE_CASES
        if (n := form_matlab_name(r["folder"], r["name"], r["is_class"], 2048))
    }
    assert len({make_target_id(n) for n in names}) == len(names)


def test_canonical_name_qualifies_class_folder_methods():
    assert canonical_name(MatlabName("helper", "pkg.C", "helper", "/t")) == (
        "pkg.C.helper"
    )
    assert canonical_name(MatlabName("C", "pkg.C", "pkg.C", "/t")) == "pkg.C"
    assert canonical_name(MatlabName("f", "pkg", "pkg.f", "/t")) == "pkg.f"
    assert canonical_name(MatlabName("Old", "Old", "Old", "/t")) == "Old"
    assert canonical_name(MatlabName("f", "", "f", "/t", True)) == "f"


def test_registered_name_candidates():
    assert registered_name_candidates("src.+pkg.@Cls.Cls") == [
        "src.+pkg.@Cls.Cls",
        "src.+pkg.Cls",
        "src.pkg.@Cls.Cls",
        "src.pkg.Cls",
        "pkg.Cls",
    ]
    assert registered_name_candidates("f") == ["f"]
    assert short_link_modname("target.+package.+sub") == "+package.+sub"
    assert short_link_modname("target") == ""
    assert short_link_modname(None) == ""


def test_split_canonical_takes_longest_prefix():
    names = {"pkg.Cls": "K1", "pkg": "K0"}
    assert split_canonical("pkg.Cls.method", names) == ("K1", ["method"])
    assert split_canonical("pkg.Cls", names) == ("K1", [])
    assert split_canonical("other.f", names) == (None, [])


def test_found_first_resolution_follows_root_then_path_order():
    roots = ["/r1", "/r2"]
    files = [
        ("/r2", "/r2", "shared", "r2-root"),
        ("/r1", "/r1/b", "shared", "r1-b"),
        ("/r1", "/r1/a/deep", "shared", "r1-a-deep"),
        ("/r1", "/r1/a", "shared", "r1-a"),
        ("/r1", "/r1/a", "other", "r1-other"),
    ]
    entries = sorted(
        (path_order_key(roots.index(root), root, folder), canonical, value)
        for root, folder, canonical, value in files
    )
    winners, shadowed = resolve_found_first((c, v) for _, c, v in entries)
    assert winners == {"shared": "r1-a", "other": "r1-other"}
    assert [(n, s) for n, s, _ in shadowed] == [
        ("shared", "r1-a-deep"),
        ("shared", "r1-b"),
        ("shared", "r2-root"),
    ]
    assert all(w == "r1-a" for _, _, w in shadowed)
