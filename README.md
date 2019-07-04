# Hashchecker

## What is Hashchecker?

Hashchecker is a command-line tool to calculate [checksum][0], [verify the
integrity][1], and find duplicate files.

## Why Hashchecker?

+ **Based on pure Python:**
Hashchecker is based on the python [`hashlib`][2] library, and is thus extremely efficient.

+ **Built to be CLI:**
Hashchecker does not require a sophisticated GUI to get the job done.
Why summon a fancy application, when you can simply open up the terminal and summon Hashchecker in a split of a second? :wink:

+ **State-of-the-art duplicate file detector:**
  Hashchecker uses a BST (Binary Search Tree) under the hood to quickly go
  through directories with a huge number of files. Duplicates are confirmed via
  comparing their cryptographic hashes.

## Installation

*Hashchecker has not yet been published to PyPI. Will update soon.*

## Get involved

Have ideas to make Hashchecker better? Fork us!

<!--LINKS-->
[0]: https://en.wikipedia.org/wiki/Checksum
[1]: https://en.wikipedia.org/wiki/File_integrity_monitoring
[2]: https://docs.python.org/3/library/hashlib.html
