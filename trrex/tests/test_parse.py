import re

import pytest

from trrex.parse import parse


def test_basic_literal():
    assert parse("a") == [["a"]]


def test_any():
    assert parse(".") == [["."]]


def test_at_beginning():
    assert parse("^a") == [["^", "a"]]


def test_at_end():
    assert parse("a$") == [["a", "$"]]


def test_max_repeat():
    assert parse(r"ab+c") == [["a", "b+", "c"]]


def test_alternation_and_digit_category():
    assert parse(r"ab\d|b") == [["a", "b", r"\d"], ["b"]]


def test_alternation_and_character_set():
    assert parse(r"ab[c-z]|b") == [["a", "b", r"[c-z]"], ["b"]]


def test_complex_alternation():
    assert parse(r"ab[c-z]a{1,3}|b") == [["a", "b", r"[c-z]", "a{1,3}"], ["b"]]


def test_simple_alternation():
    assert parse("ab|b") == [["a", "b"], ["b"]]


def test_literal_alternation():
    assert parse("a|b") == [["a"], ["b"]]


def test_single_char_inside_character_class():
    assert parse("[a]") == [["a"]]


def test_hyphen_inside_character_class():
    assert parse("[a-]") == [["[a-]"]]


def test_complex_pattern():
    assert parse(r"a{1,3}[b-z]\d") == [["a{1,3}", "[b-z]", r"\d"]]


def test_max_repeat_with_min():
    assert parse("a{1,3}bcd") == [["a{1,3}", "b", "c", "d"]]


def test_digit_category_max_repeat():
    assert parse(r"\d{1,3}") == [[r"\d{1,3}"]]


def test_two_char_literal():
    assert parse("aB") == [["a", "B"]]


def test_complex_character_set():
    assert parse(r"[\dabc]") == [[r"[\dabc]"]]


def test_character_set_with_hyphen():
    assert parse(r"[abc-]") == [[r"[abc-]"]]


def test_category_digit():
    assert parse(r"\d") == [[r"\d"]]


def test_range_in_character_set():
    assert parse("[a-e]") == [["[a-e]"]]


def test_range_and_literal():
    assert parse("[a-e]xyz") == [["[a-e]", "x", "y", "z"]]


def test_range_and_chars_in_character_set():
    assert parse("[a-exyz]") == [["[a-exyz]"]]


def test_digit_category_in_character_set():
    assert parse(r"[\d]") == [[r"\d"]]


def test_multiple_categories_in_character_set():
    assert parse(r"[\d\s]") == [[r"[\d\s]"]]


def test_different_encodings_in_character_set():
    assert parse(r"[\N{LATIN CAPITAL LETTER C WITH CEDILLA}\x61\050]") == [[r"[Ça(]"]]


def test_range_and_category_digit():
    assert parse(r"[a-e\d]") == [[r"[a-e\d]"]]


def test_escape_in_character_class():
    assert parse(r"[\t\a]") == [[r"[\t\a]"]]


def test_simple_max_repeat():
    assert parse("a{1,3}") == [["a{1,3}"]]


def test_empty_repeat():
    assert parse("a{}") == [["a", "{", "}"]]


def test_half_repeat():
    assert parse("a{") == [["a", "{"]]


def test_not_digit_category():
    assert parse(r"\D") == [[r"\D"]]


def test_space_category():
    assert parse(r"\s") == [[r"\s"]]


def test_not_space_category():
    assert parse(r"\S") == [[r"\S"]]


def test_word_category():
    assert parse(r"\w") == [[r"\w"]]


def test_not_word_category():
    assert parse(r"\W") == [[r"\W"]]


def test_boundary_category():
    assert parse(r"\b") == [[r"\b"]]


def test_not_boundary_category():
    assert parse(r"\B") == [[r"\B"]]


def test_at_beginning_category():
    assert parse(r"\A") == [[r"\A"]]


def test_repeat_at_most_one():
    assert parse(r"[a-z]?") == [["[a-z]{0,1}"]]


def test_min_repeat():
    assert parse(r"a??") == [["a{0,1}?"]]


def test_min_repeat_one_or_more():
    assert parse(r"a+?") == [["a+?"]]


def test_max_repeat_zero_or_more():
    assert parse(r"a*") == [["a*"]]


def test_min_repeat_zero_or_more():
    assert parse(r"a*?") == [["a*?"]]


def test_named_unicode():
    assert parse(r"\N{LATIN CAPITAL LETTER C WITH CEDILLA}") == [[r"Ç"]]


def test_unicode_character_set_escape():
    assert parse(r"[\u0061-\u007a]+") == [["[a-z]+"]]


def test_single_unicode():
    assert parse(r"\u0061") == [["a"]]


def test_unicode_character_set_escape_long():
    assert parse(r"[\U00000061-\U0000007a]+") == [["[a-z]+"]]


def test_single_unicode_long():
    assert parse(r"\U00000061") == [["a"]]


def test_hex_numbers():
    assert parse(r"\x61") == [["a"]]


def test_oct_numbers():
    assert parse(r"\050") == [["("]]


def test_at_end_category():
    assert parse(r"\Z") == [[r"\Z"]]


def test_escaped_parenthesis():
    assert parse(r"\(") == [[r"\("]]


def test_escaped_category_digit():
    assert parse(re.escape(r"\d")) == [["\\\\", "d"]]


def test_escaped_parenthesis_and_pattern():
    assert parse(r"\(abc") == [["\\(", "a", "b", "c"]]


def test_escaped_optional():
    assert parse(re.escape("?abc")) == [["\\?", "a", "b", "c"]]


def test_no_nested_not_capturing_patterns_escape():
    assert parse(re.escape("(?:abc)")) == [["\\(", "\\?", ":", "a", "b", "c", "\\)"]]


def test_character_set_with_meta_characters():
    assert parse("[(?:]") == [["[(?:]"]]


def test_named_unicode_missing_name():
    with pytest.raises(Exception):
        parse(r"\N{foobarbruxu}")


def test_unicode_error():
    with pytest.raises(Exception):
        parse(r"\u05+")


def test_unicode_error_long():
    with pytest.raises(Exception):
        parse(r"\U05+")


def test_bad_escape():
    with pytest.raises(Exception):
        parse(r"\C")


def test_bad_escape_in_character_set():
    with pytest.raises(Exception):
        parse(r"[\C]")


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


def test_min_repeat_overflow_error():
    with pytest.raises(OverflowError):
        parse("a{4294967296,4294967297}")


def test_max_repeat_overflow_error():
    with pytest.raises(OverflowError):
        parse("a{0,4294967297}")


def test_min_larger_max_error():
    with pytest.raises(Exception):
        parse("a{5,2}")


def test_bad_range_error():
    with pytest.raises(Exception):
        parse("[z-a]")


def test_unterminated_character_set_error():
    with pytest.raises(Exception):
        parse("[z")


def test_unterminated_character_set_with_range_error():
    with pytest.raises(Exception):
        parse("[z-")
