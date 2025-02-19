# trrex: efficient keyword mining with regular expressions

The package includes a function that represents a collection of keywords
(strings) as a regular expression. This regular expression can be used
for multiple purposes, such as keyword replacement, keyword extraction,
fuzzy matching, and other similar tasks.

```python
import re
import trrex as tx

pattern = tx.make(["baby", "bat", "bad"])
re.findall(pattern, "The baby was scared by the bad bat.")
```

## Installation

First, obtain at least Python 3.6 and virtualenv if you do not already
have them. Using a virtual environment is strongly recommended, since it
will help you to avoid clutter in your system-wide libraries. Once the
requirements are met, you can use pip:

```bash
pip install trrex
```

## Examples

Here are some quick examples of what you can do with trrex.

To begin, import re and trrex:

```python
import re
import trrex as tx
```

### Search for any keyword

You can search for keywords by using re.search:

```python
keywords = tx.make(["baby", "bad", "bat"])
match = re.search(keywords, "I saw a bat")
```

In this case we find *bat* the only keyword appearing in the text.

### Replace a keyword

You can replace a keyword by using re.sub:

```python
keywords = tx.make(["baby", "bad", "bat"])
replaced = re.sub(keywords, "bowl", "The bat is round")
```
