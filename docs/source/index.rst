.. trrex documentation master file, created by
   sphinx-quickstart on Mon Feb  8 23:15:03 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

trrex: efficient keyword mining with regular expressions
==============================================================

The package includes a function that represents a collection of keywords (strings) as a regular expression. This regular expression
can be used for multiple purposes, such as keyword replacement, keyword extraction, fuzzy matching, and other similar tasks.

.. ipython:: python

    import re
    import trrex as tx

    pattern = tx.make(["baby", "bat", "bad"])
    re.findall(pattern, "The baby was scared by the bad bat.")


User Guide
----------

.. toctree::
   :maxdepth: 2

   quickstart
   usage
   integration
   api

