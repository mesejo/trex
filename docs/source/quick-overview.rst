##############
Quick overview
##############

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
