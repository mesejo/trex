import random
import re
import string

import perfplot
from flashtext.keyword import KeywordProcessor

from trrex import make

keyword_processor, compiled_re, union_re = None, None, None


def compile(lst, flags=0, left=r"\b", right=r"\b"):
    return re.compile(make(lst, left, right), flags)


def get_word_of_length(str_length):
    # generate a random word of given length
    return "".join(random.choice(string.ascii_lowercase) for _ in range(str_length))


all_words = [
    get_word_of_length(random.choice([3, 4, 5, 6, 7, 8])) for i in range(100000)
]


def setup(length):
    all_words_chosen = random.sample(all_words, 5000)
    story = " ".join(all_words_chosen)

    # get unique keywords from the list of words generated.
    unique_keywords_sublist = list(set(random.sample(all_words, length)))

    global compiled_re
    compiled_re = compile(unique_keywords_sublist)

    # add keywords to flashtext
    global keyword_processor
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keywords_from_list(unique_keywords_sublist)

    global union_re
    union_re = re.compile(
        "|".join([r"\b" + keyword + r"\b" for keyword in unique_keywords_sublist])
    )

    return story


def ft_find(story):
    global keyword_processor
    return keyword_processor.extract_keywords(story)


def tx_find(story):
    global compiled_re
    return compiled_re.findall(story)


def union_find(story):
    global union_re
    return union_re.findall(story)


def equality_check(a, b):
    return a == b


if __name__ == "__main__":

    perfplot.show(
        setup=setup,
        n_range=[keywords_length for keywords_length in range(1000, 20001, 1000)],
        kernels=[tx_find, ft_find, union_find],
        labels=["trrex", "flashtext", "union_regex"],
        xlabel="len(keywords)",
        equality_check=equality_check,
        relative_to=0,
    )
