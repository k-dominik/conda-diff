from dataclasses import dataclass
from typing import Iterable

from conda_diff.pkg import Package, PackageDiff, package_diff


@dataclass(eq=True, frozen=True, repr=True)
class CondaEnvironment:
    name: str
    package_spec: Iterable[Package]

    @property
    def package_names(self) -> Iterable[str]:
        return [p.name for p in self.package_spec]

    def get_package(self, name) -> Package:
        return self.package_spec[self.package_names.index(name)]


@dataclass(eq=True, frozen=True, repr=True)
class CondaEnvironmentDiff:
    environment_a: CondaEnvironment
    environment_b: CondaEnvironment
    common: Iterable[Package]
    only_a: Iterable[Package]
    only_b: Iterable[Package]

    @property
    def diff(self):
        diffs = [x for x in self.common if x.diff]
        return diffs


def conda_environment_diff(
    environment_a: CondaEnvironment, environment_b: CondaEnvironment, ignore_missing_details: bool = False
) -> CondaEnvironmentDiff:
    assert environment_a.name != environment_b.name
    pnames_a = set(environment_a.package_names)
    pnames_b = set(environment_b.package_names)
    common = set(pnames_a).intersection(pnames_b)
    only_a = [environment_a.get_package(x) for x in (pnames_a - pnames_b)]
    only_b = [environment_b.get_package(x) for x in (pnames_b - pnames_a)]

    # check common packages for diffs
    package_diffs = [
        package_diff(
            environment_a.get_package(x), environment_b.get_package(x), ignore_missing_details=ignore_missing_details
        )
        for x in common
    ]

    return CondaEnvironmentDiff(
        environment_a=environment_a, environment_b=environment_b, common=package_diffs, only_a=only_a, only_b=only_b
    )
