import string
from random import choice, sample

import pandas as pd
import perfplot
from flashtext.keyword import KeywordProcessor

from trrex import make

keyword_processor, compiled_re, union_re = None, None, None


def get_word_of_length(str_length):
    # generate a random word of given length
    let = (choice(string.ascii_lowercase) for _ in range(str_length))
    return "".join(let)


all_words = [get_word_of_length(choice([3, 4, 5, 6, 7, 8])) for i in range(100000)]


def setup(length):
    chosen_words = sample(all_words, 5000)

    frame = pd.DataFrame(
        data=[
            " ".join(chosen_words[pos : pos + 10])
            for pos in range(0, len(chosen_words), 10)
        ],
        columns=["story"],
    )

    # get unique keywords from the list of words generated.
    unique_keywords_sublist = list(set(sample(all_words, length)))

    global compiled_re
    compiled_re = make(unique_keywords_sublist, prefix=r"\b(", suffix=r")\b")

    global union_re
    union_re = fr"\b({'|'.join(unique_keywords_sublist)})\b"

    global keyword_processor
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keywords_from_list(unique_keywords_sublist)

    return frame


def tx_find(frame):
    global compiled_re
    return frame["story"].str.contains(r"{}".format(compiled_re))


def union_find(frame):
    global union_re
    return frame["story"].str.contains(r"{}".format(union_re))


def flash_find(frame):
    global keyword_processor
    res = frame["story"].apply(keyword_processor.extract_keywords)
    return res.str.len() > 0


def equality_check(a, b):
    return pd.Series.equals(a, b)


if __name__ == "__main__":
    n_rng = [length for length in range(1000, 25001, 1000)]
    perfplot.show(
        setup=setup,
        n_range=n_rng,
        kernels=[tx_find, union_find, flash_find],
        labels=["trrex", "union_regex", "flashtext"],
        xlabel="len(keywords)",
        equality_check=equality_check,
        relative_to=0,
    )
