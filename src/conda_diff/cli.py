import json
from argparse import ArgumentParser

import pathlib
import sh
from conda_diff.env import CondaEnvironment, conda_environment_diff
from conda_diff.pkg import Package
from conda_diff.reader import read_env_json_file
from typing import Iterable, Mapping, Union


class CondaNotFound(Exception):
    pass


def parse_args():
    p = ArgumentParser(description="conda-diff is a tool to compare two conda environments")

    p.add_argument(
        "environment_a", type=str, help="Environment name or path to environment json file for environment a"
    )
    p.add_argument(
        "environment_b", type=str, help="Environment name or path to environment json file for environment b"
    )

    args = p.parse_args()
    return args


def get_conda_list(environment_name: str) -> Iterable[Mapping[str, Union[int, str]]]:
    try:
        specs = sh.conda("list", "--name", environment_name, "--json")
    except sh.CommandNotFound:
        raise CondaNotFound("Conda seems not to be installed or set up properly.")

    spec_list = json.loads(specs.stdout)
    assert isinstance(spec_list, list)

    return [Package(**x) for x in spec_list]


def main():
    args = parse_args()

    lists = []
    for env in [args.environment_a, args.environment_b]:
        if pathlib.Path(env).exists():
            env_list = read_env_json_file(pathlib.Path(env))
            lists.append(env_list)
        else:
            lists.append(get_conda_list(env))

    environment_a = CondaEnvironment(args.environment_a, lists[0])
    environment_b = CondaEnvironment(args.environment_b, lists[1])

    diff = conda_environment_diff(environment_a, environment_b)
    print(diff)


if __name__ == "__main__":
    main()
