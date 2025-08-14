from dataclasses import asdict, dataclass
from enum import Enum
from typing import Iterable, List, Union


class Missing(Enum):
    token = 0


_missing = Missing.token


class PackageDiffException(Exception):
    pass


@dataclass(eq=True, frozen=True, repr=True)
class Package:
    name: str
    build_string: str
    dist_name: str
    version: str
    build_number: Union[int, Missing] = _missing
    platform: Union[str, Missing] = _missing
    channel: Union[str, Missing] = _missing
    base_url: Union[str, Missing] = _missing


@dataclass(frozen=True, repr=True)
class Diff:
    name: str
    val_a: Union[int, str]
    val_b: Union[int, str]


@dataclass(frozen=True, repr=True)
class PackageDiff:
    name: str
    common: List[Package]
    diff: Iterable[Diff]


def package_diff(package_a: Package, package_b: Package, ignore_missing_details:bool=False) -> PackageDiff:
    if package_a == package_b:
        return PackageDiff(name=package_a.name, common=asdict(package_a), diff=[])
    if package_a.name != package_b.name:
        raise PackageDiffException(f"Cannot compare different packages: '{package_a.name}' and '{package_b.name}'")
    spec_a = asdict(package_a)
    spec_b = asdict(package_b)
    package_diff = []
    package_common = {}
    for k, v in spec_a.items():
        if (b_v := spec_b[k]) != v:
            if ignore_missing_details and any(x == _missing for x in [v, b_v]):
                continue
            package_diff.append(Diff(k, v, b_v))
        else:
            package_common[k] = v

    return PackageDiff(package_a.name, common=package_common, diff=package_diff)
