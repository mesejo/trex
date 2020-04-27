from trrex import compile
import re
from hypothesis import given, example
from hypothesis.strategies import text, lists
from string import ascii_letters


def test_findall():
    words = ["baby", "bad", "bat"]
    pattern = compile(words)
    assert pattern.findall("The baby was bitten by the bad bat") == words


def test_findall_ignore_case():
    words = ["baby", "bad", "bat"]
    pattern = compile(words, flags=re.IGNORECASE)
    actual = pattern.findall("The BABY was bitten by the bAD Bat")
    assert words == [w.lower() for w in actual]


def test_findall_whitespace():
    words = ["Ray Steam"]
    pattern = compile(words)
    actual = pattern.findall("Ray Steam is Steamboy")
    assert words == actual


def test_match():
    name = "Ray Steam"
    pattern = compile([name, "Edward Elric"])
    match = pattern.match(name)
    assert match is not None


def test_sub():
    replacements = {"Ray Steam": "Steamboy"}
    pattern = compile(list(replacements.keys()))

    def replace(match):
        return replacements.get(match.group(), "")

    actual = pattern.sub(replace, "The kid Ray Steam save the day")
    assert "The kid Steamboy save the day" == actual


@given(text(alphabet=ascii_letters, min_size=1))
def test_single_string_match(s):
    pattern = compile([s])
    assert pattern.match(s) is not None


@example(lst=["B", "BA", "B"])
@given(lists(text(alphabet=ascii_letters, min_size=1)))
def test_multiple_string_match(lst):
    pattern = compile(lst)
    for word in lst:
        assert pattern.match(word) is not None
