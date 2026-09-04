"""Tests for centralized MATLAB naming helpers."""

from types import SimpleNamespace

import pytest
from sphinx.errors import ConfigError

from sphinxcontrib import matlab
from sphinxcontrib.mat_naming import (
    MatlabName,
    form_matlab_name,
    is_valid_identifier,
    make_target_id,
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
            MatlabName("Class", "Class", "Class.Class", "/tmp/@Class"),
        ),
        (
            "/tmp/+pkg/@Class",
            "helper.m",
            False,
            MatlabName("helper", "pkg.Class", "pkg.Class.helper", "/tmp"),
        ),
        (
            "/tmp/@Class/sub",
            "helper.m",
            False,
            MatlabName("helper", "", "helper", "/tmp/@Class/sub"),
        ),
        (
            "/tmp/+pkg/@Class/sub",
            "helper.m",
            False,
            MatlabName("helper", "", "helper", "/tmp/+pkg/@Class/sub"),
        ),
    ]

    for folder, name, is_class, expected in rows:
        out = form_matlab_name(folder, name, is_class, namelengthmax=63)
        assert out == expected


def test_form_matlab_name_invalid_package_dropped():
    out = form_matlab_name("/tmp/+1bad", "demo.m", False, namelengthmax=63)
    assert out is None


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
        matlab_namelengthmax=64,
    )

    with pytest.raises(ConfigError, match="matlab_namelengthmax"):
        matlab.ensure_configuration(None, env)
