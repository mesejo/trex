import re

from hypothesis import given
from hypothesis.strategies import from_regex

from trrex import merge


@given(from_regex("ba{1,3}", fullmatch=True))
def test_findall_repeat(string):
    words = ["bad", "bat"]
    patterns = ["ba{1,3}"]
    pattern = re.compile(merge(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "bad",
        "bat",
    ]


@given(from_regex("b[abc]", fullmatch=True))
def test_findall_character_set(string):
    words = ["bad", "bat"]
    patterns = ["b[abc]"]
    pattern = re.compile(merge(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "bad",
        "bat",
    ]


@given(from_regex("b[d-f]", fullmatch=True))
def test_findall_range(string):
    words = ["bad", "bat"]
    patterns = ["b[d-f]"]
    pattern = re.compile(merge(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "bad",
        "bat",
    ]


@given(from_regex(r"b\d", fullmatch=True))
def test_findall_digit_category(string):
    words = ["bad", "bat"]
    patterns = [r"b\d"]
    pattern = re.compile(merge(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "bad",
        "bat",
    ]


@given(from_regex("boy|baby", fullmatch=True))
def test_findall_multiple_prefixed_patterns(string):
    words = ["bad", "bat"]
    patterns = ["boy|baby"]
    pattern = re.compile(merge(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "bad",
        "bat",
    ]


@given(from_regex(r"b\w", fullmatch=True))
def test_findall_word_category(string):
    words = ["bad", "bat"]
    patterns = [r"b\w"]
    pattern = re.compile(merge(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "by",
        "bad",
        "bat",
    ]


@given(from_regex(r"ba+", fullmatch=True))
def test_findall_no_limit_repeat(string):
    words = ["bad", "bat"]
    patterns = [r"ba+"]
    pattern = re.compile(merge(words, patterns))
    assert pattern.findall(f"The {string} was bitten by the bad bat") == [
        string,
        "bad",
        "bat",
    ]


@given(from_regex(r"ba+d", fullmatch=True))
def test_left_pattern(string):
    pattern = re.compile(merge(["bat", "bebop"], ["ba+d"], prefix="^"))
    match = pattern.match(string)
    assert match is not None


@given(from_regex(r"ba+d", fullmatch=True))
def test_left_pattern_no_match(string):
    pattern = re.compile(merge(["bat", "bebop"], ["ba+d"], prefix="^"))
    match = pattern.match(f" {string}")
    assert match is None


@given(from_regex(r"ba+d", fullmatch=True))
def test_right_pattern(string):
    pattern = re.compile(merge(["bat", "bebop"], ["ba+d"], suffix="$"))
    match = pattern.match(string)
    assert match is not None


@given(from_regex(r"ba+d", fullmatch=True))
def test_right_pattern_no_match(string):
    pattern = re.compile(merge(["bat", "bebop"], ["ba+d"], suffix="$"))
    match = pattern.match(f"{string} ")
    assert match is None


@given(from_regex(r"ba+ddest", fullmatch=True))
def test_prefix(string):
    pattern = re.compile(merge(["bat", "bebop"], ["ba+d"], suffix=r"\w+"))
    match = pattern.match(f"{string} bat in the planet")
    assert match is not None
    assert match.group() == string


@given(from_regex(r"bebe+bop", fullmatch=True))
def test_suffix(string):
    pattern = re.compile(merge(["bat"], ["be+bop"], prefix=r"\w+"))
    match = pattern.search(f"cowboy {string}")
    assert match is not None
    assert match.group() == string


@given(from_regex(r"ba+|baq|ba\d", fullmatch=True))
def test_multiple_patterns(string):
    pattern = re.compile(merge([], ["ba+", r"ba\d", "baq"]))
    match = pattern.fullmatch(string)
    assert match is not None
    assert match.group() == string


@given(from_regex(r"ba+|baq|ba\d", fullmatch=True))
def test_multiple_patterns_with_capturing_group(string):
    pattern = re.compile(
        merge([], ["ba+", r"ba\d", "baq"], prefix=r"\b(", suffix=r")\b")
    )
    match = pattern.fullmatch(string)
    assert match is not None
    assert match.group() == string


@given(from_regex("ba+|bo{1,2}[st]{1,2}", fullmatch=True))
def test_findall_punctuation(string):
    words = ["bab.y", "b#ad", "b?at"]
    patterns = ["ba+", r"bo{1,2}[st]{1,2}"] + [re.escape(word) for word in words]
    pattern = re.compile(merge([], patterns))
    assert pattern.findall(
        f"The bab.y was bitten by the b#ad b?at and also find this {string}"
    ) == words + [string]


@given(from_regex("ba+|bo{1,2}", fullmatch=True))
def test_match_max_repeat_different_versions(string):
    patterns = ["ba+", r"bo{1,2}"]
    pattern = re.compile(merge([], patterns))
    match = pattern.fullmatch(string)
    assert match is not None
    assert match.group() == string
