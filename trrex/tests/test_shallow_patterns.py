import re

from trrex import assemble


def test_findall_repeat():
    words = ["bad", "bat"]
    patterns = ["ba{1,3}"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall("The ba was bitten by the bad bat") == ["ba", "bad", "bat"]
    assert pattern.findall("The baa was bitten by the bad bat") == ["baa", "bad", "bat"]
    assert pattern.findall("The baaa was bitten by the bad bat") == [
        "baaa",
        "bad",
        "bat",
    ]


def test_findall_character_set():
    words = ["bad", "bat"]
    patterns = ["b[abc]"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall("The ba was bitten by the bad bat") == ["ba", "bad", "bat"]
    assert pattern.findall("The bb was bitten by the bad bat") == ["bb", "bad", "bat"]
    assert pattern.findall("The bc was bitten by the bad bat") == ["bc", "bad", "bat"]


def test_findall_range():
    words = ["bad", "bat"]
    patterns = ["b[d-f]"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall("The bd was bitten by the bad bat") == ["bd", "bad", "bat"]
    assert pattern.findall("The be was bitten by the bad bat") == ["be", "bad", "bat"]
    assert pattern.findall("The bf was bitten by the bad bat") == ["bf", "bad", "bat"]


def test_findall_digit_category():
    words = ["bad", "bat"]
    patterns = [r"b\d"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall("The b1 was bitten by the bad bat") == ["b1", "bad", "bat"]


def test_findall_multiple_prefixed_patterns():
    words = ["bad", "bat"]
    patterns = ["boy|baby"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall("The baby was bitten by the bad bat") == [
        "baby",
        "bad",
        "bat",
    ]
    assert pattern.findall("The boy was bitten by the bad bat") == ["boy", "bad", "bat"]


def test_findall_word_category():
    words = ["bad", "bat"]
    patterns = [r"b\w"]
    pattern = re.compile(assemble(words, patterns))
    assert pattern.findall("The b1 was bitten by the bad bat") == [
        "b1",
        "by",
        "bad",
        "bat",
    ]
