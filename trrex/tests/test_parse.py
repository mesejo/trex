import re

import pytest

from trrex.parse import parse


def test_basic_literal():
    assert [["a"]] == parse("a")


def test_max_repeat():
    assert [["a", "b+", "c"]] == parse(r"ab+c")


def test_alternation_and_digit_category():
    assert [["a", "b", r"\d"], ["b"]] == parse(r"ab\d|b")


def test_alternation_and_character_set():
    assert [["a", "b", r"[c-z]"], ["b"]] == parse(r"ab[c-z]|b")


def test_complex_alternation():
    assert [["a", "b", r"[c-z]", "a{1,3}"], ["b"]] == parse(r"ab[c-z]a{1,3}|b")


def test_simple_alternation():
    assert [["a", "b"], ["b"]] == parse("ab|b")


def test_literal_alternation():
    assert [["a"], ["b"]] == parse("a|b")


def test_complex_pattern():
    assert [["a{1,3}", "[b-z]", r"\d"]] == parse(r"a{1,3}[b-z]\d")


def test_max_repeat_with_min():
    assert [["a{1,3}", "b", "c", "d"]] == parse("a{1,3}bcd")


def test_digit_category_max_repeat():
    assert [[r"\d{1,3}"]] == parse(r"\d{1,3}")


def test_two_char_literal():
    assert [["a", "B"]] == parse("aB")


def test_complex_character_set():
    assert [[r"[\dabc]"]] == parse(r"[\dabc]")


def test_category_digit():
    assert [[r"\d"]] == parse(r"\d")


def test_range_in_character_set():
    assert [["[a-e]"]] == parse("[a-e]")


def test_range_and_literal():
    assert [["[a-e]", "x", "y", "z"]] == parse("[a-e]xyz")


def test_range_and_chars_in_character_set():
    assert [["[a-exyz]"]] == parse("[a-exyz]")


def test_range_and_category_digit():
    assert [[r"[a-e\d]"]] == parse(r"[a-e\d]")


def test_simple_max_repeat():
    assert [["a{1,3}"]] == parse("a{1,3}")


def test_not_digit_category():
    assert [[r"\D"]] == parse(r"\D")


def test_space_category():
    assert [[r"\s"]] == parse(r"\s")


def test_not_space_category():
    assert [[r"\S"]] == parse(r"\S")


def test_word_category():
    assert [[r"\w"]] == parse(r"\w")


def test_not_word_category():
    assert [[r"\W"]] == parse(r"\W")


def test_boundary_category():
    assert [[r"\b"]] == parse(r"\b")


def test_not_boundary_category():
    assert [[r"\B"]] == parse(r"\B")


def test_escaped_parenthesis():
    assert [["("]] == parse(r"\(")


def test_escaped_category_digit():
    assert [["\\", "d"]] == parse(re.escape(r"\d"))


def test_escaped_parenthesis_and_pattern():
    assert [["(", "a", "b", "c"]] == parse(r"\(abc")


def test_not_escaped_parenthesis():
    with pytest.raises(Exception):
        assert [["("]] == parse("(")


def test_parenthesis_comment():
    with pytest.raises(NotImplementedError):
        parse("(?#abc)")


def test_no_nested_patterns():
    with pytest.raises(NotImplementedError):
        parse("(abc)")


def test_not_capturing_patterns():
    with pytest.raises(NotImplementedError):
        parse("(?:abc)?")


def test_no_nested_not_capturing_patterns_escape():
    assert [["(", "?", ":", "a", "b", "c", ")"]] == parse(re.escape("(?:abc)"))


def test_character_set_with_meta_characters():
    assert [["[(?:]"]] == parse("[(?:]")


def test_no_nested_patterns_assert_not():
    with pytest.raises(NotImplementedError):
        parse("(?!abc)")


def test_no_nested_patterns_assert():
    with pytest.raises(NotImplementedError):
        parse("(?=abc)")


def test_no_nested_patterns_assert_positive_lookbehind():
    with pytest.raises(NotImplementedError):
        parse("(?<=abc)def")


def test_no_nested_patterns_assert_negative_lookbehind():
    with pytest.raises(NotImplementedError):
        parse("(?<!abc)def")
