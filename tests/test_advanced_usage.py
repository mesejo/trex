import re

from trrex import make


def compile(lst, flags=0, left=r"\b", right=r"\b"):
    return re.compile(make(lst, left, right), flags)


def test_left_pattern():
    pattern = compile(["bad", "bat", "bebop"], left="^")
    match = pattern.match("bad")
    assert match is not None


def test_left_pattern_no_match():
    pattern = compile(["bad", "bat", "bebop"], left="^")
    match = pattern.match(" bad")
    assert match is None


def test_right_pattern():
    pattern = compile(["bad", "bat", "bebop"], right="$")
    match = pattern.match("bad")
    assert match is not None


def test_right_pattern_no_match():
    pattern = compile(["bad", "bat", "bebop"], right="$")
    match = pattern.match("bad ")
    assert match is None


def test_prefix():
    pattern = compile(["bad", "bat", "bebop"], right=r"\w+")
    match = pattern.match("baddest bat in the planet")
    assert match is not None
    assert match.group() == "baddest"


def test_suffix():
    pattern = compile(["bebop"], left=r"\w+")
    match = pattern.search("cowboy bebebop")
    assert match is not None
    assert match.group() == "bebebop"
