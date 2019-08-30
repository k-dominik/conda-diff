from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Union


@dataclass(eq=True, frozen=True, repr=True)
class Package:
    name: str
    base_url: str
    build_number: int
    build_string: str
    channel: str
    dist_name: str
    platform: str
    version: str


@dataclass(frozen=True, repr=True)
class PackageDiff:
    name: str
    val_a: Union[int, str]
    val_b: Union[int, str]


def package_diff(package_a: Package, package_b: Package) -> Iterable[PackageDiff]:
    if package_a == package_b:
        return []
    spec_a = asdict(package_a)
    spec_b = asdict(package_b)
    package_diff = []
    for k, v in spec_a.items():
        if spec_b[k] != v:
            package_diff.append(PackageDiff(k, v, spec_b[k]))
    return package_diff
