import random
import string

import pandas as pd
import perfplot

from trrex import make

compiled_re, union_re = None, None


def get_word_of_length(str_length):
    # generate a random word of given length
    return "".join(random.choice(string.ascii_lowercase) for _ in range(str_length))


all_words = [
    get_word_of_length(random.choice([3, 4, 5, 6, 7, 8])) for i in range(100000)
]


def setup(length):
    chosen_words = random.sample(all_words, 5000)

    frame = pd.DataFrame(
        data=[
            " ".join(chosen_words[pos : pos + 10])
            for pos in range(0, len(chosen_words), 10)
        ],
        columns=["story"],
    )

    # get unique keywords from the list of words generated.
    unique_keywords_sublist = list(set(random.sample(all_words, length)))

    global compiled_re
    compiled_re = make(unique_keywords_sublist, prefix=r"\b(", suffix=r")\b")

    global union_re
    union_re = fr"\b({'|'.join(unique_keywords_sublist)})\b"

    return frame


def tx_find(frame):
    global compiled_re
    return frame["story"].str.findall(r"{}".format(compiled_re))


def union_find(frame):
    global union_re
    return frame["story"].str.findall(r"{}".format(union_re))


def equality_check(a, b):
    return pd.Series.equals(a, b)


if __name__ == "__main__":
    perfplot.show(
        setup=setup,
        n_range=[keywords_length for keywords_length in range(1000, 25001, 1000)],
        kernels=[tx_find, union_find],
        labels=["trrex", "union_regex"],
        xlabel="len(keywords)",
        equality_check=equality_check,
        relative_to=0,
    )
