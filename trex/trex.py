import re


class _Node:

    def __init__(self, char):
        self.char = char
        self.lo = None
        self.hi = None
        self.eq = None
        self.endpoint = False

    def __repr__(self):
        # useful in debugging
        return ''.join(['[', self.char,
                        ('' if not self.endpoint else ' <end>'),
                        ('' if self.lo is None else ' lo: ' + self.lo.__repr__()),
                        ('' if self.eq is None else ' eq: ' + self.eq.__repr__()),
                        ('' if self.hi is None else ' hi: ' + self.hi.__repr__()), ']'])


def _insert(node, string):
    if not string:
        return node

    head, *tail = string
    if node is None:
        node = _Node(head)

    if head < node.char:
        node.lo = _insert(node.lo, string)
    elif head > node.char:
        node.hi = _insert(node.hi, string)
    else:
        if not tail:
            node.endpoint = True
        else:
            node.eq = _insert(node.eq, tail)
    return node


def is_leave(node: _Node):
    children = (node.eq, node.lo, node.hi)
    return node.endpoint and not any(child is not None for child in children)


def _to_pattern(node: _Node):
    if is_leave(node):
        return node.char

    pattern = node.char
    if node.eq is not None:
        tail = _to_pattern(node.eq)
        if node.endpoint:
            tail = f'(?:{tail})?' if len(tail) > 1 else f'{tail}?'
        pattern += tail

    branches = [_to_pattern(child) for child in (node.lo, node.hi) if child is not None]

    if not branches:
        return pattern

    branches.append(pattern)

    alternation = any(len(branch) > 1 for branch in branches)  # requires |
    return f'(?:{"|".join(branches)})' if alternation else f'[{"".join(branches)}]'


class _Trie:
    root = None

    def __init__(self, words):
        for word in words:
            self.append(word)

    def append(self, string):
        self.root = _insert(self.root, string)

    def compile(self, flags=0):
        if self.root:
            return re.compile(fr'\b{_to_pattern(self.root)}\b', flags=flags)
        return re.compile('')

    def __repr__(self):
        return repr(self.root)


def compile(words, flags=0):
    return _Trie(words).compile(flags)
