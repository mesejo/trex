from trex import compile
import re


def test_findall():
    words = ['baby', 'bad', 'bat']
    pattern = compile(words)
    assert pattern.findall("The baby was bitten by the bad bat") == words


def test_findall_ignore_case():
    words = ['baby', 'bad', 'bat']
    pattern = compile(words, flags=re.IGNORECASE)
    actual = pattern.findall("The BABY was bitten by the bAD Bat")
    assert words == [w.lower() for w in actual]


def test_findall_whitespace():
    words = ['Ray Steam']
    pattern = compile(words)
    actual = pattern.findall('Ray Steam is Steamboy')
    assert words == actual


def test_match():
    name = 'Ray Steam'
    pattern = compile([name, 'Edward Elric'])
    match = pattern.match(name)
    assert match is not None


def test_sub():
    replacements = {'Ray Steam': 'Steamboy'}
    pattern = compile(list(replacements.keys()))

    def replace(match):
        return replacements.get(match.group(), "")

    actual = pattern.sub(replace, "The kid Ray Steam save the day")
    assert "The kid Steamboy save the day" == actual
