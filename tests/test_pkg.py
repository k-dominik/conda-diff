import dataclasses
import pytest
from conda_diff.pkg import Package, package_diff, PackageDiffException


def spec(**kwargs) -> dict:
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
    return spec


def test_package_create():
    sp = spec()
    p = Package(**sp)
    assert dataclasses.asdict(p) == sp


@pytest.mark.parametrize(
    "update_dict,expected_package_diff",
    [
        ({}, []),
        ({"build_number": 12}, [("build_number", 1, 12)]),
        ({"base_url": "A2"}, [("base_url", "A", "A2")]),
        ({"build_string": "abc"}, [("build_string", "B", "abc")]),
        ({"channel": "something"}, [("channel", "C", "something")]),
        ({"dist_name": "nope"}, [("dist_name", "D", "nope")]),
        ({"platform": "1234"}, [("platform", "F", "1234")]),
        ({"version": "xxxxx"}, [("version", "G", "xxxxx")]),
        ({"base_url": "A2", "version": "xxxxx"}, [("base_url", "A", "A2"), ("version", "G", "xxxxx")]),
    ],
)
def test_package_package_diff(update_dict, expected_package_diff):
    package_a = Package(**spec())
    spec_b = spec(**update_dict)
    package_b = Package(**spec_b)
    diff = package_diff(package_a, package_b)
    # make sure to get a defined sorted order of differences for this test, in case of multiple diffs
    # these need to be also in the same order in the parametrized tests above
    differences = sorted([dataclasses.astuple(x) for x in diff.diff], key=lambda x: x[0])
    assert differences == expected_package_diff


def test_package_incompatible_diff():
    spec_a = spec()
    spec_b = spec(name="something_else")
    package_a = Package(**spec_a)
    package_b = Package(**spec_b)
    with pytest.raises(PackageDiffException):
        package_diff(package_a, package_b)
