import re
from io import StringIO

class _Trie:

    def __init__(self, words):

        data = {}
        self.root = {(r'\b', False): data}
        for word in set(words):
            ref = data
            for char in word[:-1]:
                fk, tk = (char, False), (char, True)
                key = tk if tk in ref else fk
                ref[key] = key in ref and ref[key] or {}
                ref = ref[key]
            if word:
                char = word[-1]
                ref[(char, True)] = ref.pop((char, False), {})  # mark as end

    def _to_regex(self):
        # both data structures are deque
        stack = [*self.root.items()]
        cumulative = StringIO()

        while stack:

            (char, end), children = stack.pop()
            cumulative.write(char)

            if children:

                if end:  # the children are optional
                    stack.append((('?', False), {}))

                single, multiple = [], []
                for key, values in children.items():
                    if values:
                        multiple.append((key, values))
                    else:
                        single.append((key, values))

                character_set = len(single) > 1
                choices = (multiple and single) or len(multiple) > 1
                capture_group = choices or (end and multiple)

                if capture_group:
                    stack.append(((')', False), {}))

                if character_set:
                    stack.append(((']', False), {}))

                for child in single:
                    stack.append(child)

                if character_set:
                    stack.append((('[', False), {}))

                if choices and single:
                    stack.append((('|', False), {}))

                for child in multiple:
                    stack.append(child)
                    stack.append((('|', False), {}))
                else:
                    if multiple:
                        stack.pop()

                if capture_group:
                    stack.append((('(?:', False), {}))

        return cumulative.getvalue()

    def compile(self, flags=0):
        return re.compile(rf'{self._to_regex()}\b', flags=flags)


def compile(words, flags=0):
    return _Trie(words).compile(flags)
