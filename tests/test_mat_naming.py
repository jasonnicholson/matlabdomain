"""Tests for centralized MATLAB naming helpers."""

from types import SimpleNamespace

import pytest
from sphinx.errors import ConfigError

from sphinxcontrib import matlab
from sphinxcontrib.mat_naming import (
    MatlabName,
    default_namelengthmax,
    form_matlab_name,
    is_valid_identifier,
    make_target_id,
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
