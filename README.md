<p align="center">
<a href="https://github.com/mesejo/trex"><img src="https://raw.githubusercontent.com/mesejo/trex/images/trrex_logo.png" width="150" height="150"/></a>
</p>


# Efficient keyword extraction with regex

This package contains a function for efficiently representing a set of keywords as regex. This regex can be used to replace keywords in sentences or extract keywords 
from sentences

[![Build Status](https://travis-ci.com/mesejo/trex.svg?branch=master)](https://travis-ci.com/mesejo/trex) 
[![codecov](https://codecov.io/gh/mesejo/trex/branch/master/graph/badge.svg)](https://codecov.io/gh/mesejo/trex)
[![PyPI version](https://badge.fury.io/py/trrex.svg)](https://badge.fury.io/py/trrex)
![PyPI - Status](https://img.shields.io/pypi/status/trrex)

## Why use trrex?

- Pure Python, no other dependencies
- trrex is fast, about 300 times faster than a regex union, and about 2.5 times faster than FlashText
- Plays well with others, can be integrated easily with pandas

## Install trrex

Use pip,

```bash
pip install trrex
```

## Usage

```python
import trrex as tx

pattern = tx.compile(['baby', 'bat', 'bad'])
hits = pattern.findall('The baby was scared by the bad bat.')
# hits = ['baby', 'bat', 'bad']
```

## Why the name?

Naming is difficult, but as we had to call it something:

* trex: **tr**ie to **re**ge**x**
* trex: [Tyrannosaurus rex](https://en.wikipedia.org/wiki/Tyrannosaurus), a large dinosaur species with small arms  (rex meaning "king" in Latin)

## Acknowledgments

This project is based on the following resources:

- [Speed up regex](https://stackoverflow.com/questions/42742810/speed-up-millions-of-regex-replacements-in-python-3)
- [Triegex](https://github.com/ZhukovAlexander/triegex) 