.. currentmodule:: trrex
.. _integration:

============
Integrations
============

As trrex builds a regular expression pattern, it can be used by any library that expects a regular expression

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

Efficient gazetteer for spacy
-----------------------------

It can be used in conjunction with spacy EntityRuler to build a gazetteer

.. ipython:: python

    import trrex as tx
    from spacy.lang.en import English

    nlp = English()
    ruler = nlp.add_pipe("entity_ruler")
    patterns = [
        {
            "label": "ORG",
            "pattern": [
                {"TEXT": {"REGEX": tx.make(["Amazon", "Apple", "Netflix", "Netlify"])}}
            ],
        },
        {"label": "GPE", "pattern": [{"LOWER": "san"}, {"LOWER": "francisco"}]},
    ]
    ruler.add_patterns(patterns)

    doc = nlp("Netflix HQ is in Los Gatos.")
    [(ent.text, ent.label_) for ent in doc.ents]

Fuzzy matching with regex
-------------------------

We can take advantage of the fuzzy matching of the regex module:

.. ipython:: python

    import regex
    import trrex as tx

    pattern = tx.make(
        ["monkey", "monster", "dog", "cat"], prefix="", suffix=r"{1<=e<=2}"
    )
    regex.search(pattern, "This is really a master dag", regex.BESTMATCH)
