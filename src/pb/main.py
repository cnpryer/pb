from __future__ import annotations
from pathlib import Path
from argparse import ArgumentParser
from pb.parser import PathParser
from pb import fmt_bite


def cli() -> None:
    parser = ArgumentParser(
        "PBite",
        description="""\
PBite is a command line tool for parsing small bites of info from directories
containing project metadata.

`pbite .` will print some info about any project metadata in the current directory.
""",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="The path to print data from (default: '.')",
    )
    parser.add_argument(
        "-p", "--path", dest="path", help="Specify a path to process data from."
    )
    args = parser.parse_args()

    path = Path(args.path).resolve()
    for content in PathParser(path).parse():
        print(fmt_bite(content))
