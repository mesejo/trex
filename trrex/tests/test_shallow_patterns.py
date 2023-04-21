import re

from hypothesis import given
from hypothesis.strategies import from_regex

from trrex import assemble


@given(from_regex("ba{1,3}", fullmatch=True))
def test_findall_repeat(string):
    words = ["bad", "bat"]
    patterns = ["ba{1,3}"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "bad",
        "bat",
    ]


@given(from_regex("b[abc]", fullmatch=True))
def test_findall_character_set(string):
    words = ["bad", "bat"]
    patterns = ["b[abc]"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "bad",
        "bat",
    ]


@given(from_regex("b[d-f]", fullmatch=True))
def test_findall_range(string):
    words = ["bad", "bat"]
    patterns = ["b[d-f]"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "bad",
        "bat",
    ]


@given(from_regex(r"b\d", fullmatch=True))
def test_findall_digit_category(string):
    words = ["bad", "bat"]
    patterns = [r"b\d"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "bad",
        "bat",
    ]


@given(from_regex("boy|baby", fullmatch=True))
def test_findall_multiple_prefixed_patterns(string):
    words = ["bad", "bat"]
    patterns = ["boy|baby"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "bad",
        "bat",
    ]


@given(from_regex(r"b\w", fullmatch=True))
def test_findall_word_category(string):
    words = ["bad", "bat"]
    patterns = [r"b\w"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "by",
        "bad",
        "bat",
    ]
