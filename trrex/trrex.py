from io import StringIO
from typing import Sequence

from .parse import parse


class _TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False


_OPTION = ("?", _TrieNode())
_OPEN_PARENTHESIS = ("(?:", _TrieNode())
_CLOSE_PARENTHESIS = (")", _TrieNode())
_OPEN_BRACKETS = ("[", _TrieNode())
_CLOSE_BRACKETS = ("]", _TrieNode())
_ALTERNATION = ("|", _TrieNode())


class _Trie:
    def __init__(self, words, patterns=None, left=r"\b", right=r"\b"):
        self.root = _TrieNode()
        self.left = left
        self.right = right

        for word in words:
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = _TrieNode()
                node = node.children[char]
            node.end = True

        if patterns is not None:
            for pattern in map(parse, patterns):
                for sub_pattern in pattern:
                    node = self.root
                    for component in sub_pattern:
                        if component not in node.children:
                            node.children[component] = _TrieNode()
                        node = node.children[component]
                    node.end = True

    def _to_regex(self):
        stack = [(self.left, self.root)]
        cumulative = StringIO()

        while stack:
            char, node = stack.pop()
            cumulative.write(char)

            if not node.children:
                continue  # skip

            if node.end:
                stack.append(_OPTION)

            single, multiple = [], []
            for key, child in node.children.items():
                if child.children or len(key) > 1:
                    multiple.append((key, child))
                else:
                    single.append((key, child))

            requires_character_set = len(single) > 1
            requires_alternation = (multiple and single) or len(multiple) > 1
            requires_group = requires_alternation or (node.end and multiple)

            if requires_group:
                stack.append(_CLOSE_PARENTHESIS)

            if requires_character_set:
                stack.append(_CLOSE_BRACKETS)

            for child in single:
                stack.append(child)

            if requires_character_set:
                stack.append(_OPEN_BRACKETS)

            if requires_alternation and single:
                stack.append(_ALTERNATION)

            if multiple:
                head, *tail = multiple
                stack.append(head)

                for child in tail:
                    stack.append(_ALTERNATION)
                    stack.append(child)

            if requires_group:
                stack.append(_OPEN_PARENTHESIS)

        return cumulative.getvalue()

    def make(self):
        return f"{self._to_regex()}{self.right}"


def make(strings: Sequence[str], prefix: str = r"\b", suffix: str = r"\b") -> str:
    """
    Create a string that represents a regular expression object from a set of strings

    Parameters
    ----------
    strings : Sequence[str]
        Sequence or set of strings to be made into a regex

    prefix : str, optional
           Left delimiter for pattern

    suffix : str, optional
            Right delimiter for pattern

    Returns
    -------
    String
            A string representing a regular expression pattern

    Examples
    --------
    >>> import re
    >>> import trrex as tx
    >>> pattern = tx.make(["baby", "bat", "bad"])
    >>> re.findall(pattern, "The baby was scared by the bad bat.")
    ['baby', 'bad', 'bat']
    """

    return _Trie(strings, left=prefix, right=suffix).make()


def merge(
    strings: Sequence[str],
    patterns: Sequence[str],
    prefix: str = r"\b",
    suffix: str = r"\b",
) -> str:
    """
    Create a string that represents a regular expression object from a set of strings

    Parameters
    ----------
    strings : Sequence[str]
        Sequence or set of strings to be made into a regex

    patterns: Sequence[str]
        Sequence or set of non-literal regular expression patterns to be made into a regex

    prefix : str, optional
           Left delimiter for pattern

    suffix : str, optional
            Right delimiter for pattern

    Returns
    -------
    String
            A string representing a regular expression pattern

    Examples
    --------
    >>> import re
    >>> import trrex as tx
    >>> pattern = tx.merge(["baby", "bat", "bad"])
    >>> re.findall(pattern, "The baby was scared by the bad bat.")
    ['baby', 'bad', 'bat']
    """

    return _Trie(strings, patterns, left=prefix, right=suffix).make()
