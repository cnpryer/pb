from __future__ import annotations
from pathlib import Path
from typing import Any, Iterable
import rtoml  # type: ignore


class PathParser:
    """Helpful object for parsing `Content`s from paths."""

    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    def parse(self) -> Iterable[Content]:
        if self.path.is_file() and is_toml_file(self.path):
            return [Content.toml(self.path)]
        paths = self.path.glob("*.toml")  # TODO(cnpryer)
        deduper = ContentDeduper()
        for path in paths:
            # Currently .toml is only supported
            if not is_toml_file(path):
                continue
            deduper.add(Content.toml(path))
        return deduper.dedupe()


class Content:
    """Generic object for loading parsed contents into."""

    def __init__(self, name: str, data: dict[str, Any], source: Path) -> None:
        self.name = name
        self._data = data
        self._source = source
        self._hash = content_hash(self)  # TODO(cnpryer)

    @property
    def data(self) -> dict[str, Any]:
        return self._data

    def contains(self, key: str) -> bool:
        return key in self.data

    @staticmethod
    def file(path: Path) -> Content:
        return Content(str(path), {}, source=path)  # TODO

    @staticmethod
    def toml(path: Path) -> Content:
        data = toml_data(path)
        project = data.get("project", {})
        if "name" in project:
            data["name"] = project["name"]
        if "version" in project:
            data["version"] = project["version"]
        if "description" in project:
            data["description"] = project["description"]
        data["name"] = data.get("name", project.get("name", str(path)))
        data["source"] = path
        return Content(data["name"], data, source=data["source"])

    @property
    def version(self) -> str:
        return self.data.get("version", "could not parse version")

    @property
    def description(self) -> str:
        return self.data.get("description", "could not parse description")

    @property
    def source(self) -> Path:
        return self._source

    def info(self) -> str:
        return f"""\
  Name: {self.name}
  Version: {self.version}
  Description: {self.description}
  Source: {self.source}
"""


def toml_data(path: Path) -> dict[str, Any]:
    return rtoml.load(path)


def is_toml_file(path: Path) -> bool:
    return path.suffix == ".toml"


class ContentDeduper:
    def __init__(self) -> None:
        self._hashes: list[str] = []
        self._content: list[Content] = []

    def add(self, content: Content) -> None:
        self._content.append(content)

    def contains(self, content: Content) -> bool:
        return content._hash in self._hashes

    def dedupe(self) -> list[Content]:
        d = {}
        for ct in self._content:
            if ct._hash not in d:
                d[ct._hash] = ct.data
                continue
            merge_data(d[ct._hash], ct.data)
        return [Content(d[h]["name"], d[h], d[h]["source"]) for h in d]


def merge_data(a: dict[str, Any], b: dict[str, Any]) -> None:
    if a["name"] == str(a["source"]) and "name" in b:
        a["name"] = b["name"]
    if "version" not in a and "version" in b:
        a["version"] = b["version"]
    if "description" not in a and "description" in b:
        a["description"] = b["description"]


# TODO(cnpryer): __hash__ for hash(content)
def content_hash(content: Content) -> str:
    name = content.name
    if name == str(content.source):
        name = content.source.parent.stem  # TODO(cnrpyer): Could index by dir path
    return normalize_name(name)


def normalize_name(name: str) -> str:
    return name.strip().lower()
