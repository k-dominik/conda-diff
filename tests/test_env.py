import pytest
from conda_diff.env import CondaEnvironment, conda_environment_diff
from conda_diff.pkg import Package

from contextlib import nullcontext


expect_no_raise = nullcontext


def package(**kwargs) -> dict:
    spec = {
        "base_url": "A",
        "build_number": 1,
        "build_string": "B",
        "channel": "C",
        "dist_name": "D",
        "name": "E",
        "platform": "F",
        "version": "G",
    }
    spec.update(**kwargs)
    return Package(**spec)


@pytest.mark.parametrize("package_specs", [([]), ([{"name": "a"}]), ([{"name": "a"}, {"name": "whatever"}])])
def test_conda_env_construction(package_specs):
    specs = [package(**x) for x in package_specs]
    conda_env = CondaEnvironment("TestEnv", specs)

    assert conda_env.name == "TestEnv"
    assert conda_env.package_spec == specs


def test_conda_env_different_pacakges():
    names_a = ["A", "B", "C", "D"]
    names_b = ["A", "B", "C", "E"]
    package_updates_a = [{"name": x} for x in names_a]
    package_updates_b = [{"name": x} for x in names_b]
    specs_a = [package(**x) for x in package_updates_a]
    specs_b = [package(**x) for x in package_updates_b]

    env_a = CondaEnvironment("Env-A", specs_a)
    env_b = CondaEnvironment("Env-B", specs_b)

    diff = conda_environment_diff(env_a, env_b)

    assert diff.environment_a == env_a
    assert diff.environment_b == env_b
    assert sorted([p.name for p in diff.common]) == ["A", "B", "C"]
    assert len(diff.diff) == 0
    assert len(diff.only_a) == 1
    assert diff.only_a[0].name == "D"
    assert len(diff.only_b) == 1
    assert diff.only_b[0].name == "E"


def test_conda_env_different_pacakge_diffs():
    names = ["A", "B", "C", "D"]
    package_updates_a = [{"name": x} for x in names]
    package_updates_b = [{"name": x} for x in names]
    package_updates_b[0].update(build_number=2)
    specs_a = [package(**x) for x in package_updates_a]
    specs_b = [package(**x) for x in package_updates_b]

    env_a = CondaEnvironment("Env-A", specs_a)
    env_b = CondaEnvironment("Env-B", specs_b)

    diff = conda_environment_diff(env_a, env_b)

    assert diff.environment_a == env_a
    assert diff.environment_b == env_b
    assert sorted([p.name for p in diff.common]) == names
    assert len(diff.diff) == 1
    assert diff.diff[0].name == "A"
