import sys
from unittest.mock import patch

from conda_diff import cli


def test_parse_args():
    mock_args = ["conda-diff", "env_a", "env_b"]
    with patch.object(sys, "argv", mock_args):
        args = cli.parse_args()

    assert args.environment_a == "env_a"
    assert args.environment_b == "env_b"
