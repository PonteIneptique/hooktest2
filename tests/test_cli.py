import os.path

import pytest
from click.testing import CliRunner
from hooktest.cli import cli
from hooktest.tester import Result


def get_path(xml: str) -> str:
    return os.path.relpath(os.path.join(os.path.dirname(__file__), "test_data", xml))

def count_failing(result: Result) -> int:
    return len([s for s in result.statuses if s.status == False])

@pytest.fixture
def runner():
    return CliRunner()

def test_duplicate_refs(runner):
    """Test whether duplicate ref finding is working"""

    # Test with a file expected to fail.
    result = runner.invoke(cli, ['--no-catalog', get_path("duplicate.xml")], standalone_mode=False)
    assert '✗' in result.output, "File has a failing test"
    assert 'duplicateRefs[Tree=default]' in result.output, "Tree Default has duplicate reff"
    assert count_failing(result.return_value.results[get_path("duplicate.xml")]) == 1, "Only one failing test"

    # Test with a file expected to pass.
    result = runner.invoke(cli, ['--no-catalog', get_path("correct_simple.xml")], standalone_mode=False)
    assert '✗' not in result.output, "File has a failing test"
    assert 'duplicateRefs[Tree=default]' not in result.output, "Tree Default has no dup reff"
    assert count_failing(result.return_value.results[get_path("duplicate.xml")]) == 0, "Zero failing test"