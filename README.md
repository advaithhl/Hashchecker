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

You can install Hashchecker using `pip`:

`$ pip3 install --upgrade hashchecker`

Additionally, you may consider using the `--user` option.

## Requirements

+ [Click][3]: Command line parsing.

+ [Colorama][4]: Coloring text wherever necessary.

+ [Tabulate][5]: Displaying results in tabular format.

## Get involved

Have ideas to make Hashchecker better? Fork us!

<!--LINKS-->
[0]: https://en.wikipedia.org/wiki/Checksum
[1]: https://en.wikipedia.org/wiki/File_integrity_monitoring
[2]: https://docs.python.org/3/library/hashlib.html
[3]: https://github.com/pallets/click/
[4]: https://github.com/tartley/colorama
[5]: https://bitbucket.org/astanin/python-tabulate/src/master/
