.. currentmodule:: trrex
.. _usage:

==============
Advanced usage
==============

By default trrex will use word boundaries (\\b) to delimit keywords, this could be problematic if the words contain
punctuation symbols. You can do the following for those cases:

.. ipython:: python

    import trrex as tx
    import re

    emoticons = [":)", ":D", ":("]
    pattern = tx.make(emoticons, prefix=r"(?<!\w)", suffix=r"(?!\w)")
    result = re.findall(pattern, "The smile :), and the laugh :D and the sad :(")
    result
