from pathlib import Path

import json
from typing import Iterable, Mapping, Union

from conda_diff.pkg import Package


def read_env_json_file(env_list_path: Path) -> Iterable[Mapping[str, Union[str, int]]]:
    with open(env_list_path, "r") as f:
        data = json.load(f)
        if isinstance(data, dict):
            data = data["actions"]["LINK"]

        return [Package(**x) for x in data]
