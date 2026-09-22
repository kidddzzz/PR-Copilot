"""Existing tests -- shows the repo DOES have a testing habit, which makes
the missing test for parse_date() a meaningful, believable gap rather than
a repo that just has no tests at all."""

from src.utils.parser import normalize_whitespace


def test_normalize_whitespace_collapses_spaces():
    assert normalize_whitespace("a    b   c") == "a b c"


def test_normalize_whitespace_strips_ends():
    assert normalize_whitespace("  a b  ") == "a b"
