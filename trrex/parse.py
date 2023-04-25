from sre_constants import (
    ANY,
    ASSERT,
    ASSERT_NOT,
    AT,
    AT_BEGINNING,
    AT_BEGINNING_STRING,
    AT_BOUNDARY,
    AT_END,
    AT_END_STRING,
    AT_NON_BOUNDARY,
    BRANCH,
    CATEGORY,
    CATEGORY_DIGIT,
    CATEGORY_NOT_DIGIT,
    CATEGORY_NOT_SPACE,
    CATEGORY_NOT_WORD,
    CATEGORY_SPACE,
    CATEGORY_WORD,
    GROUPREF,
    IN,
    LITERAL,
    MAX_REPEAT,
    MAXREPEAT,
    MIN_REPEAT,
    NEGATE,
    NOT_LITERAL,
    RANGE,
    SUBPATTERN,
)
from sre_parse import (  # type: ignore
    ASCIILETTERS,
    CATEGORIES,
    DIGITS,
    ESCAPES,
    FLAGS,
    GLOBAL_FLAGS,
    HEXDIGITS,
    OCTDIGITS,
    REPEAT_CHARS,
    SPECIAL_CHARS,
    TYPE_FLAGS,
    WHITESPACE,
    State,
    SubPattern,
    Tokenizer,
)

_REPEATCODES = frozenset({MIN_REPEAT, MAX_REPEAT})


def _uniq(items):
    return list(dict.fromkeys(items))


def _escape(source, escape, state):
    # handle escape code in expression
    code = CATEGORIES.get(escape)
    if code:
        return code
    code = ESCAPES.get(escape)
    if code:
        return code
    try:
        c = escape[1:2]
        if c == "x":
            # hexadecimal escape
            escape += source.getwhile(2, HEXDIGITS)
            if len(escape) != 4:
                raise source.error("incomplete escape %s" % escape, len(escape))
            return LITERAL, int(escape[2:], 16)
        elif c == "u" and source.istext:
            # unicode escape (exactly four digits)
            escape += source.getwhile(4, HEXDIGITS)
            if len(escape) != 6:
                raise source.error("incomplete escape %s" % escape, len(escape))
            return LITERAL, int(escape[2:], 16)
        elif c == "U" and source.istext:
            # unicode escape (exactly eight digits)
            escape += source.getwhile(8, HEXDIGITS)
            if len(escape) != 10:
                raise source.error("incomplete escape %s" % escape, len(escape))
            c = int(escape[2:], 16)
            chr(c)  # raise ValueError for invalid code
            return LITERAL, c
        elif c == "N" and source.istext:
            import unicodedata

            # named unicode escape e.g. \N{EM DASH}
            if not source.match("{"):
                raise source.error("missing {")
            charname = source.getuntil("}", "character name")
            try:
                c = ord(unicodedata.lookup(charname))
            except (KeyError, TypeError):
                raise source.error(
                    "undefined character name %r" % charname,
                    len(charname) + len(r"\N{}"),
                )
            return LITERAL, c
        elif c == "0":
            # octal escape
            escape += source.getwhile(2, OCTDIGITS)
            return LITERAL, int(escape[1:], 8)
        elif c in DIGITS:
            # octal escape *or* decimal group reference (sigh)
            if source.next in DIGITS:
                escape += source.get()
                if (
                    escape[1] in OCTDIGITS
                    and escape[2] in OCTDIGITS
                    and source.next in OCTDIGITS
                ):
                    # got three octal digits; this is an octal escape
                    escape += source.get()
                    c = int(escape[1:], 8)
                    if c > 0o377:
                        raise source.error(
                            "octal escape value %s outside of "
                            "range 0-0o377" % escape,
                            len(escape),
                        )
                    return LITERAL, c
            # not an octal escape, so this is a group reference
            group = int(escape[1:])
            if group < state.groups:
                if not state.checkgroup(group):
                    raise source.error("cannot refer to an open group", len(escape))
                state.checklookbehindgroup(group, source)
                return GROUPREF, group
            raise source.error("invalid group reference %d" % group, len(escape) - 1)
        if len(escape) == 2:
            if c in ASCIILETTERS:
                raise source.error("bad escape %s" % escape, len(escape))
            return LITERAL, rf"\{escape[1]}"
    except ValueError:
        pass
    raise source.error("bad escape %s" % escape, len(escape))


def _class_escape(source, escape):
    # handle escape code inside character class
    code = ESCAPES.get(escape)
    if code:
        return code
    code = CATEGORIES.get(escape)
    if code and code[0] is IN:
        return code
    try:
        c = escape[1:2]
        if c == "x":
            # hexadecimal escape (exactly two digits)
            escape += source.getwhile(2, HEXDIGITS)
            if len(escape) != 4:
                raise source.error("incomplete escape %s" % escape, len(escape))
            return LITERAL, int(escape[2:], 16)
        elif c == "u" and source.istext:
            # unicode escape (exactly four digits)
            escape += source.getwhile(4, HEXDIGITS)
            if len(escape) != 6:
                raise source.error("incomplete escape %s" % escape, len(escape))
            return LITERAL, int(escape[2:], 16)
        elif c == "U" and source.istext:
            # unicode escape (exactly eight digits)
            escape += source.getwhile(8, HEXDIGITS)
            if len(escape) != 10:
                raise source.error("incomplete escape %s" % escape, len(escape))
            c = int(escape[2:], 16)
            chr(c)  # raise ValueError for invalid code
            return LITERAL, c
        elif c == "N" and source.istext:
            import unicodedata

            # named unicode escape e.g. \N{EM DASH}
            if not source.match("{"):
                raise source.error("missing {")
            charname = source.getuntil("}", "character name")
            try:
                c = ord(unicodedata.lookup(charname))
            except (KeyError, TypeError):
                raise source.error(
                    "undefined character name %r" % charname,
                    len(charname) + len(r"\N{}"),
                )
            return LITERAL, c
        elif c in OCTDIGITS:
            # octal escape (up to three digits)
            escape += source.getwhile(2, OCTDIGITS)
            c = int(escape[1:], 8)
            if c > 0o377:
                raise source.error(
                    "octal escape value %s outside of " "range 0-0o377" % escape,
                    len(escape),
                )
            return LITERAL, c
        elif c in DIGITS:
            raise ValueError
        if len(escape) == 2:
            if c in ASCIILETTERS:
                raise source.error("bad escape %s" % escape, len(escape))
            return LITERAL, ord(escape[1])
    except ValueError:
        pass
    raise source.error("bad escape %s" % escape, len(escape))


def _parse_flags(source, state, char):
    sourceget = source.get
    add_flags = 0
    del_flags = 0
    if char != "-":
        while True:
            flag = FLAGS[char]
            if source.istext:
                if char == "L":
                    msg = "bad inline flags: cannot use 'L' flag with a str pattern"
                    raise source.error(msg)
            else:
                if char == "u":
                    msg = "bad inline flags: cannot use 'u' flag with a bytes pattern"
                    raise source.error(msg)
            add_flags |= flag
            if (flag & TYPE_FLAGS) and (add_flags & TYPE_FLAGS) != flag:
                msg = "bad inline flags: flags 'a', 'u' and 'L' are incompatible"
                raise source.error(msg)
            char = sourceget()
            if char is None:
                raise source.error("missing -, : or )")
            if char in ")-:":
                break
            if char not in FLAGS:
                msg = "unknown flag" if char.isalpha() else "missing -, : or )"
                raise source.error(msg, len(char))
    if char == ")":
        state.flags |= add_flags
        return None
    if add_flags & GLOBAL_FLAGS:
        raise source.error("bad inline flags: cannot turn on global flag", 1)
    if char == "-":
        char = sourceget()
        if char is None:
            raise source.error("missing flag")
        if char not in FLAGS:
            msg = "unknown flag" if char.isalpha() else "missing flag"
            raise source.error(msg, len(char))
        while True:
            flag = FLAGS[char]
            if flag & TYPE_FLAGS:
                msg = "bad inline flags: cannot turn off flags 'a', 'u' and 'L'"
                raise source.error(msg)
            del_flags |= flag
            char = sourceget()
            if char is None:
                raise source.error("missing :")
            if char == ":":
                break
            if char not in FLAGS:
                msg = "unknown flag" if char.isalpha() else "missing :"
                raise source.error(msg, len(char))
    assert char == ":"
    if del_flags & GLOBAL_FLAGS:
        raise source.error("bad inline flags: cannot turn off global flag", 1)
    if add_flags & del_flags:
        raise source.error("bad inline flags: flag turned on and off", 1)
    return add_flags, del_flags


def _parse_sub(source, state, verbose, nested):
    # parse an alternation: a|b|c

    items = []
    itemsappend = items.append
    sourcematch = source.match
    while True:
        itemsappend(
            _parse(source, state, verbose, nested + 1, not nested and not items)
        )
        if not sourcematch("|"):
            break

    if len(items) == 1:
        return items[0]

    subpattern = SubPattern(state)

    # check if all items share a common prefix
    while True:
        prefix = None
        for item in items:
            if not item:
                break
            if prefix is None:
                prefix = item[0]
            elif item[0] != prefix:
                break
        else:
            # all subitems start with a common "prefix".
            # move it out of the branch
            for item in items:
                del item[0]
            subpattern.append(prefix)
            continue  # check next one
        break

    # check if the branch can be replaced by a character set
    set = []
    for item in items:
        if len(item) != 1:
            break
        op, av = item[0]
        if op is LITERAL:
            set.append((op, av))
        elif op is IN and av[0][0] is not NEGATE:
            set.extend(av)
        else:
            break
    else:
        # we can store this as a character set instead of a
        # branch (the compiler may optimize this even more)
        subpattern.append((IN, _uniq(set)))
        return subpattern

    subpattern.append((BRANCH, (None, items)))
    return subpattern


def _parse(source, state, verbose, nested, first=False):
    # parse a simple pattern
    subpattern = SubPattern(state)

    # precompute constants into local variables
    subpatternappend = subpattern.append
    sourceget = source.get
    sourcematch = source.match
    _len = len
    _ord = ord

    while True:
        this = source.next
        if this is None:
            break  # end of pattern
        if this in "|)":
            break  # end of subpattern
        sourceget()

        if verbose:
            # skip whitespace and comments
            if this in WHITESPACE:
                continue
            if this == "#":
                while True:
                    this = sourceget()
                    if this is None or this == "\n":
                        break
                continue

        if this[0] == "\\":
            code = _escape(source, this, state)
            subpatternappend(code)

        elif this not in SPECIAL_CHARS:
            subpatternappend((LITERAL, _ord(this)))

        elif this == "[":
            here = source.tell() - 1
            # character set
            set = []
            setappend = set.append
            if source.next == "[":
                import warnings

                warnings.warn(
                    "Possible nested set at position %d" % source.tell(),
                    FutureWarning,
                    stacklevel=nested + 6,
                )
            negate = sourcematch("^")
            # check remaining characters
            while True:
                this = sourceget()
                if this is None:
                    raise source.error(
                        "unterminated character set", source.tell() - here
                    )
                if this == "]" and set:
                    break
                elif this[0] == "\\":
                    code1 = _class_escape(source, this)
                else:
                    if set and this in "-&~|" and source.next == this:
                        import warnings

                        warnings.warn(
                            "Possible set %s at position %d"
                            % (
                                "difference"
                                if this == "-"
                                else "intersection"
                                if this == "&"
                                else "symmetric difference"
                                if this == "~"
                                else "union",
                                source.tell() - 1,
                            ),
                            FutureWarning,
                            stacklevel=nested + 6,
                        )
                    code1 = LITERAL, _ord(this)
                if sourcematch("-"):
                    # potential range
                    that = sourceget()
                    if that is None:
                        raise source.error(
                            "unterminated character set", source.tell() - here
                        )
                    if that == "]":
                        if code1[0] is IN:
                            code1 = code1[1][0]
                        setappend(code1)
                        setappend((LITERAL, _ord("-")))
                        break
                    if that[0] == "\\":
                        code2 = _class_escape(source, that)
                    else:
                        if that == "-":
                            import warnings

                            warnings.warn(
                                "Possible set difference at position %d"
                                % (source.tell() - 2),
                                FutureWarning,
                                stacklevel=nested + 6,
                            )
                        code2 = LITERAL, _ord(that)
                    if code1[0] != LITERAL or code2[0] != LITERAL:
                        msg = "bad character range %s-%s" % (this, that)
                        raise source.error(msg, len(this) + 1 + len(that))
                    lo = code1[1]
                    hi = code2[1]
                    if hi < lo:
                        msg = "bad character range %s-%s" % (this, that)
                        raise source.error(msg, len(this) + 1 + len(that))
                    setappend((RANGE, (lo, hi)))
                else:
                    if code1[0] is IN:
                        code1 = code1[1][0]
                    setappend(code1)

            set = _uniq(set)
            # XXX: <fl> should move set optimization to compiler!
            if _len(set) == 1 and set[0][0] is LITERAL:
                # optimization
                if negate:
                    subpatternappend((NOT_LITERAL, set[0][1]))
                else:
                    subpatternappend(set[0])
            else:
                if negate:
                    set.insert(0, (NEGATE, None))
                # charmap optimization can't be added here because
                # global flags still are not known
                subpatternappend((IN, set))

        elif this in REPEAT_CHARS:
            # repeat previous item
            here = source.tell()
            if this == "?":
                min, max = 0, 1
            elif this == "*":
                min, max = 0, MAXREPEAT

            elif this == "+":
                min, max = 1, MAXREPEAT
            elif this == "{":
                if source.next == "}":
                    subpatternappend((LITERAL, _ord(this)))
                    continue

                min, max = 0, MAXREPEAT
                lo = hi = ""
                while source.next in DIGITS:
                    lo += sourceget()
                if sourcematch(","):
                    while source.next in DIGITS:
                        hi += sourceget()
                else:
                    hi = lo
                if not sourcematch("}"):
                    subpatternappend((LITERAL, _ord(this)))
                    source.seek(here)
                    continue

                if lo:
                    min = int(lo)
                    if min >= MAXREPEAT:
                        raise OverflowError("the repetition number is too large")
                if hi:
                    max = int(hi)
                    if max >= MAXREPEAT:
                        raise OverflowError("the repetition number is too large")
                    if max < min:
                        raise source.error(
                            "min repeat greater than max repeat", source.tell() - here
                        )
            else:
                raise AssertionError("unsupported quantifier %r" % (this,))
            # figure out which item to repeat
            if subpattern:
                item = subpattern[-1:]
            else:
                item = None
            if not item or item[0][0] is AT:
                raise source.error(
                    "nothing to repeat", source.tell() - here + len(this)
                )
            if item[0][0] in _REPEATCODES:
                raise source.error("multiple repeat", source.tell() - here + len(this))
            if item[0][0] is SUBPATTERN:
                group, add_flags, del_flags, p = item[0][1]
                if group is None and not add_flags and not del_flags:
                    item = p
            if sourcematch("?"):
                subpattern[-1] = (MIN_REPEAT, (min, max, item))
            else:
                subpattern[-1] = (MAX_REPEAT, (min, max, item))

        elif this == ".":
            subpatternappend((ANY, None))

        elif this == "(":
            raise NotImplementedError("No nested patterns")

        elif this == "^":
            subpatternappend((AT, AT_BEGINNING))

        elif this == "$":
            subpatternappend((AT, AT_END))

        else:
            raise AssertionError("unsupported special character %r" % (this,))

    # unpack non-capturing groups
    for i in range(len(subpattern))[::-1]:
        op, av = subpattern[i]
        if op is SUBPATTERN:
            group, add_flags, del_flags, p = av
            if group is None and not add_flags and not del_flags:
                subpattern[i : i + 1] = p

    return subpattern


def parse(string):
    source = Tokenizer(string)
    state = State()
    state.str = string
    items = sub_parse(source, state, 0, 0)

    return items_to_list(items)


def items_to_list(items):
    res = []
    for item in items:
        lst = []
        for op, val in item:
            if op == IN:
                lst.append(extract_in_node(val))
            elif op == LITERAL:
                lst.append(extract_literal_node(val))
            elif op == AT:
                lst.append(extract_at_node(val))
            elif op == MAX_REPEAT:
                lst.append(extract_max_repeat_node(val))
            elif op == SUBPATTERN or op == ASSERT_NOT or op == ASSERT:
                raise NotImplementedError("Not nested patterns allowed")
        res.append(lst)
    return res


def extract_at_node(val):
    if val == AT_BOUNDARY:
        return r"\b"
    elif val == AT_NON_BOUNDARY:
        return r"\B"
    elif val == AT_BEGINNING_STRING:
        return r"\A"
    elif val == AT_END_STRING:
        return r"\Z"


def extract_literal_node(val):
    if isinstance(val, str) and "\\" in val:
        return val
    return chr(val)


def extract_in_node(val):
    ii = ""
    category = False
    for a, v in val:
        if a == CATEGORY:
            if v == CATEGORY_DIGIT:
                ii += r"\d"
            elif v == CATEGORY_NOT_DIGIT:
                ii += r"\D"
            elif v == CATEGORY_SPACE:
                ii += r"\s"
            elif v == CATEGORY_NOT_SPACE:
                ii += r"\S"
            elif v == CATEGORY_WORD:
                ii += r"\w"
            elif v == CATEGORY_NOT_WORD:
                ii += r"\W"
            category = True
        elif a == RANGE:
            start, end = v
            ii += f"{chr(start)}-{chr(end)}"
        elif a == LITERAL:
            ii += chr(v)
    return ii if category and len(val) == 1 else f"[{ii}]"


def sub_parse(source, state, verbose, nested):
    items = []
    items_append = items.append
    source_match = source.match
    while True:
        items_append(
            _parse(source, state, verbose, nested + 1, not nested and not items)
        )
        if not source_match("|"):
            break

    return items


def extract_max_repeat_node(val):
    start, end, pat = val
    p = ""

    for op, v in pat:
        if op == LITERAL:
            p += extract_literal_node(v)
        elif op == IN:
            p += extract_in_node(v)

    if end == MAXREPEAT:
        return f"{p}+"

    return rf"{p}{{{start},{end}}}"
