"""Tests for tree-sitter helpers in ``mat_tree_sitter_parser``."""

from tree_sitter import Parser

from sphinxcontrib.mat_tree_sitter_parser import ML_LANG, get_row


def test_get_row_is_stable_beyond_small_int_cache():
    # Rows above 256 are not cached small ints. tree-sitter 0.26.0's
    # ``Point.row`` returns a borrowed reference for them; repeated reads
    # corrupt the heap and crash (SIGSEGV) on standard CPython builds.
    tree = Parser(ML_LANG).parse(b"\n" * 300 + b"x = 1;\n")
    for _ in range(10000):
        rows = [get_row(tree.root_node.end_point) for _ in range(10)]
        assert rows == [301] * 10
