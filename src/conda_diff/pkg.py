from dataclasses import asdict, dataclass
from typing import Iterable, Union, Dict


class PackageDiffException(Exception):
    pass


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
class Diff:
    name: str
    val_a: Union[int, str]
    val_b: Union[int, str]


@dataclass(frozen=True, repr=True)
class PackageDiff:
    name: str
    common: Iterable[Dict[str, Union[str, int]]]
    diff: Iterable[Diff]


def package_diff(package_a: Package, package_b: Package) -> PackageDiff:
    if package_a == package_b:
        return PackageDiff(name=package_a.name, common=asdict(package_a), diff=[])
    if package_a.name != package_b.name:
        raise PackageDiffException(f"Cannot compare different packages: '{package_a.name}' and '{package_b.name}'")
    spec_a = asdict(package_a)
    spec_b = asdict(package_b)
    package_diff = []
    package_common = {}
    for k, v in spec_a.items():
        if spec_b[k] != v:
            package_diff.append(Diff(k, v, spec_b[k]))
        else:
            package_common[k] = v

    return PackageDiff(package_a.name, common=package_common, diff=package_diff)
