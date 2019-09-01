import json
from argparse import ArgumentParser

from typing import Mapping, Union

import sh

from conda_diff.env import CondaEnvironment, conda_environment_diff
from conda_diff.pkg import Package


class CondaNotFound(Exception):
    pass


def parse_args():
    p = ArgumentParser(description="conda-diff is a tool to compare two conda environments")

    p.add_argument("environment_a", type=str, help="Environment name for environment a")
    p.add_argument("environment_b", type=str, help="Environment name for environment b")

    args = p.parse_args()
    return args


def get_conda_list(environment_name: str) -> Mapping[str, Union[int, str]]:
    try:
        specs = sh.conda("list", "--name", environment_name, "--json")
    except sh.CommandNotFound:
        raise CondaNotFound("Conda seems not to be installed or set up properly.")

    spec_list = json.loads(specs.stdout)
    assert isinstance(spec_list, list)

    return [Package(**x) for x in spec_list]


def main():
    args = parse_args()

    list_a = get_conda_list(args.environment_a)
    list_b = get_conda_list(args.environment_b)

    environment_a = CondaEnvironment(args.environment_a, list_a)
    environment_b = CondaEnvironment(args.environment_b, list_b)

    diff = conda_environment_diff(environment_a, environment_b)
    print(diff)


if __name__ == "__main__":
    main()
