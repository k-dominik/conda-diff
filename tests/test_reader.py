import pytest
from conda_diff.pkg import Package
from conda_diff.reader import read_env_json_file


@pytest.fixture
def conda_env_package_list(conda_env_list):
    return [Package(**x) for x in conda_env_list]


def test_read_list_file(conda_env_list_file, conda_env_package_list):
    conda_list = read_env_json_file(conda_env_list_file)
    assert conda_list == conda_env_package_list


def test_read_create_list_file(conda_env_create_list_file, conda_env_package_list):
    conda_list = read_env_json_file(conda_env_create_list_file)
    assert conda_list == conda_env_package_list
