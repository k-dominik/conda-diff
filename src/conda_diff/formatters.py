from abc import ABC, abstractmethod

from conda_diff.env import CondaEnvironmentDiff

import textwrap


class FormatterBase(ABC):
    def __init__(self, environment_diff: CondaEnvironmentDiff, **format_spec):
        self._environment_diff = environment_diff
        self._format_spec = format_spec

    @abstractmethod
    def to_json(self, *args, **kwargs) -> str:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...


class SimpleFormatter(FormatterBase):
    def to_json(self):
        pass

    def __repr__(self) -> str:
        packages_only_a = "\n".join(sorted([f"  {x.name}" for x in self._environment_diff.only_a]))
        packages_only_b = "\n".join(sorted([f"  {x.name}" for x in self._environment_diff.only_b]))
        common_packages_no_diff = "\n".join(
            sorted([f"  {x.name}" for x in self._environment_diff.common if not x.diff])
        )
        common_packages_diff = "\n".join(sorted([f"  {x.name}" for x in self._environment_diff.common if x.diff]))
        a_name = self._environment_diff.environment_a.name
        b_name = self._environment_diff.environment_b.name
        rep_str = """\
        Diff report for environments {a_name} and {b_name}:

        Common Packages (without diff)
        ------------------------------
        {common_packages_no_diff}

        Common Packages (with diff)
        ---------------------------
        {common_packages_diff}

        Packages Only In {a_name}:
        --------------------------
        {packages_only_a}

        Packages Only In {b_name}:
        --------------------------
        {packages_only_b}
        """
        rep_str = textwrap.dedent(rep_str)

        rep_str = rep_str.format(
            packages_only_a=packages_only_a,
            a_name=a_name,
            b_name=b_name,
            common_packages_no_diff=common_packages_no_diff,
            common_packages_diff=common_packages_diff,
            packages_only_b=packages_only_b,
        )
        return rep_str
