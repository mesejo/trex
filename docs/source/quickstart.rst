==========
Quickstart
==========

Find some simple instructions below

Installation
============

First, obtain at least Python 3.6 and virtualenv if you do not already have them. Using a virtual environment is strongly
recommended, since it will help you to avoid clutter in your system-wide libraries. Once the requirements are met, you can use pip:

.. code-block:: bash

   pip install trrex

Examples
========

Here are some quick examples of what you can do with trrex.

To begin, import re and trrex:

.. ipython:: python

    import re
    import trrex as tx

Search for any keyword
----------------------
You can search for keywords by using re.search:

.. ipython:: python

    keywords = tx.make(["baby", "bad", "bat"])
    match = re.search(keywords, "I saw a bat")
    match

In this case we find *bat* the only keyword appearing in the text.

Replace a keyword
-----------------
You can replace a keyword by using re.sub:

.. ipython:: python

    keywords = tx.make(["baby", "bad", "bat"])
    replaced = re.sub(keywords, "bowl", "The bat is round")
    replaced

How not to use it
-----------------
The code below makes a pattern for each word and hence does not take advantage of trrex. The code will offer no performance benefit against a standard Python string search.

.. code-block:: python

    import trrex as tx
    import re

    text = "The bad bat scared the baby"
    words = ["bad", "baby", "bat"]
    for word in words:
        pattern = tx.make([word])
        match = re.search(pattern, text)

