# Copyright (C) 2018-2020, 2022 Rocky Bernstein <rocky@gnu.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
from typing import Any


def maybe_show_asm(showasm: Any, tokens: list) -> None:
    """
    Show the asm based on the showasm flag (or file object), writing to the
    appropriate stream depending on the type of the flag.

    :param showasm: Flag which determines whether the ingested code is
                    written to sys.stdout or not. (It is also to pass a file
                    like object, into which the asm will be written).
    :param tokens:  The asm tokens to show.
    """
    if showasm:
        stream = showasm if hasattr(showasm, "write") else sys.stdout
        for t in tokens:
            stream.write(str(t))
            stream.write("\n")


def maybe_show_tree(walker, tree) -> None:
    """
    Show the tree based on the tree flag (or file object), writing to the
    appropriate stream depending on the type of the flag.

    :param show_tree: Flag which determines whether the parse tree is
                      written to sys.stdout or not. (It is also to pass a file
                      like object, into which the ast will be written).
    :param tree:     The tree to show.
    """
    if walker.showast:
        if hasattr(walker.showast, "write"):
            stream = walker.showast
        else:
            stream = sys.stdout
        if (
            isinstance(walker.showast, dict)
            and walker.showast.get("after", False)
            and hasattr(walker, "str_with_template")
            and walker.str_with_template
        ):
            walker.str_with_template(tree)
        else:
            stream.write(str(tree))
        stream.write("\n")


def maybe_show_tree_param_default(show_tree, name: str, default):
    """
    Show a function parameter with default for an grammar-tree based on the show_tree flag
    (or file object), writing to the appropriate stream depending on the type
    of the flag.

    :param show_tree: Flag which determines whether the function parameter with
                      default is written to sys.stdout or not. (It is also to
                      pass a file like object, into which the ast will be
                      written).
    :param name:    The function parameter name.
    :param default: The function parameter default.
    """
    if show_tree.get("param", False):
        stream = show_tree if hasattr(show_tree, "write") else sys.stdout
        stream.write("\n")
        stream.write("--" + name)
        stream.write("\n")
        stream.write(str(default))
        stream.write("\n")
        stream.write("--")
        stream.write("\n")
