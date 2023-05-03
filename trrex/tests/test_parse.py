import re

import pytest

from trrex.parse import parse


def test_basic_literal():
    assert parse("a") == [(1, 1, ["a"])]


def test_any():
    assert parse(".") == [(1, 1, ["."])]


def test_at_beginning():
    # TODO analise if at beginning should count
    assert parse("^a") == [(2, 2, ["^", "a"])]


def test_at_end():
    # TODO analise if at end should count
    assert parse("a$") == [(2, 2, ["a", "$"])]


def test_max_repeat():
    assert parse(r"ab+c") == [(3, 4294967297, ["a", "b+", "c"])]


def test_alternation_and_digit_category():
    assert parse(r"ab\d|b") == [(3, 3, ["a", "b", r"\d"]), (1, 1, ["b"])]


def test_alternation_and_character_set():
    assert parse(r"ab[c-z]|b") == [(3, 3, ["a", "b", "[c-z]"]), (1, 1, ["b"])]


def test_complex_alternation():
    assert parse(r"ab[c-z]a{1,3}|b") == [
        (4, 6, ["a", "b", "[c-z]", "a{1,3}"]),
        (1, 1, ["b"]),
    ]


def test_simple_alternation():
    assert parse("ab|b") == [(2, 2, ["a", "b"]), (1, 1, ["b"])]


def test_literal_alternation():
    assert parse("a|b") == [(1, 1, ["a"]), (1, 1, ["b"])]


def test_single_char_inside_character_class():
    assert parse("[a]") == [(1, 1, ["a"])]


def test_hyphen_inside_character_class():
    assert parse("[a-]") == [(1, 1, ["[a-]"])]


def test_complex_pattern():
    assert parse(r"a{1,3}[b-z]\d") == [(3, 5, ["a{1,3}", "[b-z]", r"\d"])]


def test_max_repeat_with_min():
    assert parse("a{1,3}bcd") == [(4, 6, ["a{1,3}", "b", "c", "d"])]


def test_digit_category_max_repeat():
    assert parse(r"\d{1,3}") == [(1, 3, ["\\d{1,3}"])]


def test_two_char_literal():
    assert parse("aB") == [(2, 2, ["a", "B"])]


def test_complex_character_set():
    assert parse(r"[\dabc]") == [(1, 1, [r"[\dabc]"])]


def test_character_set_with_hyphen():
    assert parse(r"[abc-]") == [(1, 1, ["[abc-]"])]


def test_category_digit():
    assert parse(r"\d") == [(1, 1, ["\\d"])]


def test_range_in_character_set():
    assert parse("[a-e]") == [(1, 1, ["[a-e]"])]


def test_range_and_literal():
    assert parse("[a-e]xyz") == [(4, 4, ["[a-e]", "x", "y", "z"])]


def test_range_and_chars_in_character_set():
    assert parse("[a-exyz]") == [(1, 1, ["[a-exyz]"])]


def test_digit_category_in_character_set():
    assert parse(r"[\d]") == [(1, 1, [r"\d"])]


def test_multiple_categories_in_character_set():
    assert parse(r"[\d\s]") == [(1, 1, [r"[\d\s]"])]


def test_different_encodings_in_character_set():
    assert parse(r"[\N{LATIN CAPITAL LETTER C WITH CEDILLA}\x61\050]") == [
        (1, 1, ["[Ça(]"])
    ]


def test_range_and_category_digit():
    assert parse(r"[a-e\d]") == [(1, 1, ["[a-e\\d]"])]


def test_escape_in_character_class():
    assert parse(r"[\t\a]") == [(1, 1, ["[\\t\\a]"])]


def test_simple_max_repeat():
    assert parse("a{1,3}") == [(1, 3, ["a{1,3}"])]


def test_empty_repeat():
    assert parse("a{}") == [(3, 3, ["a", "{", "}"])]


def test_half_repeat():
    assert parse("a{") == [(2, 2, ["a", "{"])]


def test_not_digit_category():
    assert parse(r"\D") == [(1, 1, [r"\D"])]


def test_space_category():
    assert parse(r"\s") == [(1, 1, [r"\s"])]


def test_not_space_category():
    assert parse(r"\S") == [(1, 1, [r"\S"])]


def test_word_category():
    assert parse(r"\w") == [(1, 1, [r"\w"])]


def test_not_word_category():
    assert parse(r"\W") == [(1, 1, [r"\W"])]


def test_boundary_category():
    assert parse(r"\b") == [(1, 1, [r"\b"])]


def test_not_boundary_category():
    assert parse(r"\B") == [(1, 1, [r"\B"])]


def test_at_beginning_category():
    assert parse(r"\A") == [(1, 1, [r"\A"])]


def test_repeat_at_most_one():
    assert parse(r"[a-z]?") == [(0, 1, ["[a-z]{0,1}"])]


def test_min_repeat():
    assert parse(r"a??") == [(0, 1, ["a{0,1}?"])]


def test_min_repeat_one_or_more():
    assert parse(r"a+?") == [(1, 4294967295, ["a+?"])]


def test_max_repeat_zero_or_more():
    assert parse(r"a*") == [(0, 4294967295, ["a*"])]


def test_min_repeat_zero_or_more():
    assert parse(r"a*?") == [(0, 4294967295, ["a*?"])]


def test_named_unicode():
    assert parse(r"\N{LATIN CAPITAL LETTER C WITH CEDILLA}") == [(1, 1, ["Ç"])]


def test_unicode_character_set_escape():
    assert parse(r"[\u0061-\u007a]+") == [(1, 4294967295, ["[a-z]+"])]


def test_single_unicode():
    assert parse(r"\u0061") == [(1, 1, ["a"])]


def test_unicode_character_set_escape_long():
    assert parse(r"[\U00000061-\U0000007a]+") == [(1, 4294967295, ["[a-z]+"])]


def test_single_unicode_long():
    assert parse(r"\U00000061") == [(1, 1, ["a"])]


def test_hex_numbers():
    assert parse(r"\x61") == [(1, 1, ["a"])]


def test_oct_numbers():
    assert parse(r"\050") == [(1, 1, ["("])]


def test_at_end_category():
    assert parse(r"\Z") == [(1, 1, ["\\Z"])]


def test_escaped_parenthesis():
    assert parse(r"\(") == [(1, 1, ["\\("])]


def test_escaped_category_digit():
    assert parse(re.escape(r"\d")) == [(2, 2, ["\\\\", "d"])]


def test_escaped_parenthesis_and_pattern():
    assert parse(r"\(abc") == [(4, 4, ["\\(", "a", "b", "c"])]


def test_escaped_optional():
    assert parse(re.escape("?abc")) == [(4, 4, ["\\?", "a", "b", "c"])]


def test_no_nested_not_capturing_patterns_escape():
    assert parse(re.escape("(?:abc)")) == [
        (7, 7, ["\\(", "\\?", ":", "a", "b", "c", "\\)"])
    ]


def test_character_set_with_meta_characters():
    assert parse("[(?:]") == [(1, 1, ["[(?:]"])]


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
