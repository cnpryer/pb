from __future__ import annotations
from pathlib import Path
from typing import Any, Iterable


class PathParser:
    """Helpful object for parsing `Content`s from paths."""

    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    def parse(self) -> Iterable[Content]:
        if self.path.is_file() and is_metadata_file(self.path):
            yield Content.file(self.path)
        paths = self.path.glob("*.toml")  # TODO
        for path in paths:
            yield Content.file(path)


def is_metadata_file(path: Path) -> bool:
    return path.suffix in (".toml",)


class Content:
    """Generic object for loading parsed contents into."""

    def __init__(self, name: str, data: list[Any]) -> None:
        self.name = name
        self._data = data

    @property
    def data(self) -> list[Any]:
        return self._data

    @staticmethod
    def file(path: Path) -> Content:
        name = path
        data: list[Any] = []  # TODO
        return Content(str(name), data)  # TODO

    def info(self) -> str:
        return f"""Content Name: {self.name}"""
