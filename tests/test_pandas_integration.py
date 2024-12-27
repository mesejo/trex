from string import ascii_letters

import pandas as pd
from hypothesis import given
from hypothesis.strategies import lists, text

from trrex import make


@given(lists(text(alphabet=ascii_letters, min_size=1), min_size=1))
def test_extract(lst):
    pattern = make(lst, prefix=r"\b(", suffix=r")\b")
    frame = pd.DataFrame({"txt": lst})
    actual = frame["txt"].str.extract(pattern)
    assert actual[0].tolist() == lst
