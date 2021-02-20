.. currentmodule:: trrex
.. _integration:

================================
Integration with other libraries
================================

As trrex builds a regex pattern, it can be used by any library that expects
a regular expression

Working with pandas
-------------------

.. ipython:: python

    import trrex as tx
    import pandas as pd

    df = pd.DataFrame(
        ["The quick brown fox", "jumps over", "the lazy dog"], columns=["text"]
    )
    pattern = tx.make(["dog", "fox"])
    df["text"].str.contains(pattern)

As you can see from the above example it works with any pandas function that receives a regular expression.
