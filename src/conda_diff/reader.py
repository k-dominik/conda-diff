import json
from pathlib import Path
from typing import Dict, List, Union

from ruyaml import YAML

from conda_diff.pkg import Package


def read_env_file(env_list_path: Path) -> List[Package]:
    if env_list_path.suffix == ".json":
        return read_env_json_file(env_list_path)
    elif env_list_path.suffix in [".yml", ".yaml"]:

        return read_env_yaml_file(env_list_path)

    raise NotImplementedError(f"Reading not implemented for {env_list_path.name} file.")


def read_env_json_file(env_list_path: Path) -> List[Package]:
    with open(env_list_path, "r") as f:
        data = json.load(f)
        if isinstance(data, dict):
            data = data["actions"]["LINK"]

        return [Package(**x) for x in data]


def _yaml_data_adapter(dep_str: str) -> Dict[str, Union[str, int]]:
    """
    parses dependency strings and transforms them to something we can
    throw into a Package instance

    Basically anything we can extract from a yaml env export

    example:
        ilastik=1.4.1b18=0

        {
            "dist_name": "ilastik-1.4.1b18-0",
            "name": "ilastik",
            "build_number": 0,
            "build_string": "0",
            "version": "1.4.1b18",
        }
    """
    name, version, bld = dep_str.split("=")
    try:
        bldnum = int(bld.split("_")[-1])
    except ValueError:
        bldnum = None

    try:
        ret_dict = {
            "dist_name": f"{name}-{version}-{bld}",
            "name": name,
            "build_string": bld,
            "version": version,
        }
    except ValueError as e:
        raise ValueError(f"could not parse {dep_str}") from e

    if bldnum is not None:
        ret_dict["build_number"] = bldnum

    return ret_dict


def read_env_yaml_file(env_list_path: Path) -> List[Package]:
    yaml = YAML(typ="safe")
    with open(env_list_path, "r") as f:
        data = yaml.load(f)["dependencies"]

        return [Package(**_yaml_data_adapter(x)) for x in data]
