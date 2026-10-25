"""MATLAB names in a build: discovery, found-first, anchors and cross-references."""

import re
from collections import Counter

import pytest
from sphinx.util.inventory import InventoryFile

from sphinxcontrib import mat_naming


@pytest.fixture
def srcdir(rootdir):
    return rootdir / "roots" / "test_naming"


def html(app):
    text = (app.outdir / "index.html").read_text()
    return text.split('<div class="body"')[1].split('<div class="sphinxsidebar"')[0]


def index_names(app):
    index = app.env.domaindata["mat"]["index"]
    return {
        str(path.relative_to(app.srcdir)): entry
        for path, entry in ((app.srcdir.joinpath(p), e) for p, e in index.items())
    }


@pytest.mark.parametrize("confdict", [{}])
def test_discovery_uses_matlab_names(app):
    index = index_names(app)
    assert {path: e["canonical_name"] for path, e in index.items()} == {
        "+for/nm_kw.m": None,  # keyword package
        "+nmpkg/@NmCls/NmCls.m": "nmpkg.NmCls",
        "+nmpkg/@NmCls/nm_helper.m": "nmpkg.NmCls.nm_helper",
        "+nmpkg/nm_func.m": "nmpkg.nm_func",
        "@NmBox/NmBox.m": "NmBox",
        "@NmBox/sub/nm_legacy.m": None,  # R2026a: class subfolder
        "alpha/nm_shared.m": "nm_shared",
        "beta/nm_shared.m": "nm_shared",
        "my folder/nm_spaced.m": "nm_spaced",
        "private/nm_priv.m": "nm_priv",
    }
    assert [p for p, e in index.items() if e["private"]] == ["private/nm_priv.m"]
    # Legacy entity keys are kept alongside.
    assert index["my folder/nm_spaced.m"]["name"] == "my folder.nm_spaced"
    assert app.env.domaindata["mat"]["canonical_names"] == {
        "NmBox": "@NmBox.NmBox",
        "nm_shared": "alpha.nm_shared",
        "nm_spaced": "my folder.nm_spaced",
        "nmpkg.NmCls": "+nmpkg.@NmCls.NmCls",
        "nmpkg.nm_func": "+nmpkg.nm_func",
    }


@pytest.mark.parametrize("confdict", [{}])
def test_found_first_shadowing(app):
    assert (
        f"nm_shared in {app.srcdir / 'beta' / 'nm_shared.m'} is shadowed by "
        f"{app.srcdir / 'alpha' / 'nm_shared.m'}"
    ) in app.status.getvalue()
    # The bare MATLAB name documents and links the found-first file.
    text = html(app)
    assert "Alpha version (first on the path)." in text
    assert 'href="#alpha.nm_shared"' in text


@pytest.mark.parametrize(
    ("confdict", "prefix"),
    [
        ({"matlab_keep_package_prefix": False}, ""),
        ({"matlab_keep_package_prefix": True}, "+"),
    ],
)
def test_anchors_and_matlab_name_xrefs(app, prefix):
    text = html(app)
    ids = re.findall(r'\bid="([^"]*)"', text)
    expected = [
        f"{prefix}nmpkg.nm_func",
        f"{prefix}nmpkg.NmCls",
        f"{prefix}nmpkg.NmCls.NmCls",
        f"{prefix}nmpkg.NmCls.nm_helper",
        "alpha.nm_shared",
        "beta.nm_shared",
        "nm_spaced",
    ]
    assert [i for i in ids if i not in ("naming", "matlab-names")] == expected
    assert all(n == 1 for n in Counter(ids).values())

    # Every "MATLAB names" xref resolves, whatever name the object was
    # documented under.
    xrefs = text.split('id="matlab-names"')[1]
    hrefs = re.findall(r'href="#([^"]*)"', xrefs)
    assert hrefs == [
        "matlab-names",  # heading permalink
        f"{prefix}nmpkg.nm_func",
        f"{prefix}nmpkg.NmCls",
        f"{prefix}nmpkg.NmCls.nm_helper",
        "alpha.nm_shared",
        "nm_spaced",
        f"{prefix}nmpkg.nm_func",
    ]
    assert "WARNING" not in app.warning.getvalue()


@pytest.mark.parametrize("confdict", [{}])
def test_inventory_anchors_follow_contract(app):
    dom = app.env.get_domain("mat")
    for name, _, _, _, anchor, _ in dom.get_objects():
        if name in dom.data["modules"]:
            assert anchor == mat_naming.make_module_target_id(name)
        else:
            assert anchor == mat_naming.make_target_id(name) == name
    with open(app.outdir / "objects.inv", "rb") as f:
        inv = InventoryFile.load(f, "", lambda _base, uri: uri)
    funcs = inv["mat:function"]
    uri = funcs["nmpkg.nm_func"]
    uri = uri[2] if isinstance(uri, tuple) else uri.uri
    assert uri == "index.html#nmpkg.nm_func"


@pytest.mark.parametrize(
    ("confdict", "callable_"),
    [
        ({"matlab_version": "R2025a"}, True),
        ({"matlab_version": "R2025b"}, True),
        ({"matlab_version": "R2026a"}, False),
    ],
)
def test_class_subfolder_callability_follows_matlab_version(app, callable_):
    entry = index_names(app)["@NmBox/sub/nm_legacy.m"]
    assert entry["canonical_name"] == ("nm_legacy" if callable_ else None)
    assert ("nm_legacy" in app.env.domaindata["mat"]["canonical_names"]) is callable_


@pytest.mark.parametrize(
    ("confdict", "expected"),
    [
        ({"matlab_version": "R2025a"}, 2048),
        ({"matlab_version": "R2026a", "matlab_namelengthmax": 63}, 63),
        ({"matlab_version": "R2025a", "matlab_namelengthmax": 2048}, 2048),
    ],
)
def test_namelengthmax_in_build(app, expected):
    assert app.config.matlab_namelengthmax == expected


def test_target_id_collision_warns(make_app, tmp_path):
    (tmp_path / "conf.py").write_text('extensions = ["sphinxcontrib.matlab"]\n')
    (tmp_path / "index.rst").write_text(
        "first\n=====\n\n.. mat:function:: first\n\n.. mat:function:: second\n"
    )
    app = make_app(srcdir=tmp_path)
    app.build()
    assert "first and first share the target id 'first'" in app.warning.getvalue()
    assert "second" not in app.warning.getvalue()
    assert "first" not in app.env.domaindata["mat"]["objects"]
