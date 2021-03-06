<p align="center">
<a href="https://github.com/mesejo/trex"><img src="https://raw.githubusercontent.com/mesejo/trex/images/trrex_logo.png" width="150" height="150"/></a>
</p>


# Efficient keyword extraction with regex

This package contains a function for efficiently representing a set of keywords as regex. This regex can be used to replace keywords in sentences or extract keywords
from sentences

[![Build Status](https://github.com/mesejo/trex/workflows/trrex/badge.svg)](https://github.com/mesejo/trex)
[![codecov](https://codecov.io/gh/mesejo/trex/branch/master/graph/badge.svg)](https://codecov.io/gh/mesejo/trex)
[![PyPI version](https://badge.fury.io/py/trrex.svg)](https://badge.fury.io/py/trrex)
![PyPI - Status](https://img.shields.io/pypi/status/trrex)

## Install trrex

Use pip,

```bash
pip install trrex
```

## Usage

```python
import trrex as tx
import re

pattern = tx.make(['baby', 'bat', 'bad'])
hits = re.findall(pattern, 'The baby was scared by the bad bat.')
# hits = ['baby', 'bat', 'bad']
```

### pandas

```python
import trrex as tx
import pandas as pd

frame = pd.DataFrame({
    "txt": ["The baby", "The bat"]
})
pattern = tx.make(['baby', 'bat', 'bad'], prefix=r"\b(", suffix=r")\b") # need to specify capturing groups
frame["match"] = frame["txt"].str.extract(pattern)
hits = frame["match"].tolist()
print(hits)
# hits = ['baby', 'bad']
```

## Why use trrex?

- trrex builds a *better* regex pattern, than the simple regex union, therefore searching (and replacing) keywords is
about 300 times faster than a regex union pattern, and about 2.5 times faster than FlashText algorithm. See below for a performance
comparison:

![Performance comparison](https://github.com/mesejo/trex/blob/images/find_comparison.png?raw=true)

- Plays well with others, can be integrated easily with pandas, spacy and any other regex engine. See the [documentation](https://trrex.readthedocs.io/en/latest/integration.html)
for examples.
- Pure Python, no other dependencies

## Why the name?

Naming is difficult, but as we had to call it something:

* trex: **tr**ie to **re**ge**x**
* trex: [Tyrannosaurus rex](https://en.wikipedia.org/wiki/Tyrannosaurus), a large dinosaur species with small arms  (rex meaning "king" in Latin)

## Acknowledgments

This project is based on the following resources:

- [Speed up regex](https://stackoverflow.com/questions/42742810/speed-up-millions-of-regex-replacements-in-python-3)
- [Triegex](https://github.com/ZhukovAlexander/triegex)
