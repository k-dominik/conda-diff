import json

import pytest
import ruyaml


@pytest.fixture
def conda_env_list():
    conda_env_list = [
        {
            "base_url": "https://some.url/blah",
            "build_number": 42,
            "build_string": "0f0f0f0f_42",
            "channel": "blah",
            "dist_name": "blahpackage-0.1.1dev0-0f0f0f0f_42",
            "name": "blahpackage",
            "platform": "linux-64",
            "version": "0.1.1dev0",
        }
    ]
    return conda_env_list


@pytest.fixture
def conda_env_create_list(conda_env_list):
    return {
        "actions": {"FETCH": [], "LINK": conda_env_list, "PREFIX": "/some_prefix"},
        "dry_run": True,
        "prefix": "/some_prefix",
        "success": True,
    }


@pytest.fixture
def conda_env_list_file(tmpdir, conda_env_list):
    filename = tmpdir / "conda-list.json"
    with filename.open("w") as f:
        json.dump(conda_env_list, f)

    return filename


@pytest.fixture
def conda_env_create_list_file(tmpdir, conda_env_create_list):
    filename = tmpdir / "conda-create-list.json"
    with filename.open("w") as f:
        json.dump(conda_env_create_list, f)

    return filename


@pytest.fixture
def conda_export_yaml(tmpdir, conda_env_list):
    filename = tmpdir / "conda-export.yml"
    contents = {
        "name": "will-be-ignored",
        "channels": ["will", "be", "ignored"],
        "dependencies": [f"{pkg['name']}={pkg['version']}={pkg['build_string']}" for pkg in conda_env_list]
    }
    yaml = ruyaml.YAML(typ="safe")
    with filename.open("w") as f:
        yaml.dump(contents, f)

    return filename
