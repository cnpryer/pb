from __future__ import annotations
from pathlib import Path
from argparse import ArgumentParser
from pb.parser import PathParser
from pb import fmt_bite


def cli() -> None:
    parser = ArgumentParser(
        "PBite",
        description="""\
PBite: `ls` for project metadata. Use `pb .` to parse metadata from the current
directory.
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
