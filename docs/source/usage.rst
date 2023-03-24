.. currentmodule:: trrex
.. _usage:

==============
Advanced usage
==============

By default trrex will use word boundaries :code:`"(\\b)"` to delimit keywords, this could be problematic if the words contain
punctuation symbols. You can do the following for those cases:

.. ipython:: python

    import trrex as tx
    import re

    emoticons = [":)", ":D", ":("]
    pattern = tx.make(emoticons, prefix=r"(?<!\w)", suffix=r"(?!\w)")
    result = re.findall(pattern, "The smile :), and the laugh :D and the sad :(")
    result

In the above example the parenthesis need no escaping because they are inside in a character set:

.. ipython:: python

    pattern

In general, however, the regex meta characters need to be escaped in order to match them:

.. ipython:: python

    words = ["bab.y", "b#ad", "b?at"]
    pattern = tx.make(map(re.escape, words))
    pattern

Notice that you need to use `re.escape <https://docs.python.org/3/library/re.html#re.escape>`_ for each character of the
string in order to work properly with trrex.
