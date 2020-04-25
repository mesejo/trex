<a href="https://github.com/mesejo/trex"><img src="https://raw.githubusercontent.com/mesejo/trex/images/trex_logo.png" width="150" height="150" align="left" /></a>

# Efficient keyword extraction with regex

This package contains a function for efficiently representing a set of keywords as regex. This regex can be used to replace keywords in sentences or extract keywords 
from sentences

## Why use trex?

- Pure Python, no other dependencies
- trex is fast, about 300 times faster than a regex union, and about 2.5 times faster than FlashText
- Plays well with others, can be integrated easily with pandas

## Why the name?

Naming is difficult, but as we had to call it something:

* trex: **t**rie to **re**ge**x**
* trex: [Tyrannosaurus rex](https://en.wikipedia.org/wiki/Tyrannosaurus), a large dinosaur species with small arms  (rex meaning "king" in Latin)

## Acknowledgments

This project is based on the following resources:

- [Speed up regex](https://stackoverflow.com/questions/42742810/speed-up-millions-of-regex-replacements-in-python-3)
- [Triegex](https://github.com/ZhukovAlexander/triegex) 