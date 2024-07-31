from pathlib import Path
from unittest import mock

import conda_diff.reader
import pytest
from conda_diff.pkg import Package
from conda_diff.reader import read_env_file, read_env_json_file, read_env_yaml_file

from tests.conftest import conda_export_yaml


@pytest.fixture
def conda_env_package_list(conda_env_list):
    return [Package(**x) for x in conda_env_list]


def test_read_list_file(conda_env_list_file, conda_env_package_list):
    conda_list = read_env_json_file(conda_env_list_file)
    assert conda_list == conda_env_package_list


def test_read_create_list_file(conda_env_create_list_file, conda_env_package_list):
    conda_list = read_env_json_file(conda_env_create_list_file)
    assert conda_list == conda_env_package_list


def test_read_export_yaml_file(conda_export_yaml, conda_env_list):
    conda_list = read_env_yaml_file(conda_export_yaml)

    assert len(conda_list) == 1

    p_a = conda_list[0]
    p_b = conda_env_list[0]

    for k in ["name", "version", "build_string", "build_number"]:
        assert getattr(p_a, k) == p_b[k]


@pytest.mark.parametrize(
    "filename, expected_func_name",
    [
        (Path("something.json"), "read_env_json_file"),
        (Path("something.yaml"), "read_env_yaml_file"),
        (Path("something.yml"), "read_env_yaml_file"),
    ],
)
def test_read_files(monkeypatch, filename: Path, expected_func_name: str):
    with monkeypatch.context() as m:
        func_mock = mock.MagicMock()
        m.setattr(conda_diff.reader, expected_func_name, func_mock)
        _ = read_env_file(filename)

    func_mock.assert_called_once_with(filename)
