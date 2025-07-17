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


def test_simple_passing_file(runner):
    """Test with a file expected to pass."""
    result = runner.invoke(cli, ['--no-catalog', get_path("correct_simple.xml")], standalone_mode=False)
    assert '✗' not in result.output, "File has a failing test"
    assert 'duplicateRefs[Tree=default]' not in result.output, "Tree Default has no dup reff"
    assert count_failing(result.return_value.results[get_path("correct_simple.xml")]) == 0, "Zero failing test"


def test_double_tree_file(runner):
    """Test with a file expected to pass."""
    result = runner.invoke(cli, ['--no-catalog', '-v', 'verbose', get_path("correct_double_tree.xml")], standalone_mode=False)
    assert '✗' not in result.output, "File has a failing test"
    assert "parse(citeStructures): Tree:default->line(15) " in result.output, "Both tree are documented"
    assert "Tree:translations->language(3)->[line(12)]" in result.output, "Both tree are documented"
    assert "forbiddenRefs[Tree=default]: ✔" in result.output, "Both tree are documented"
    assert "duplicateRefs[Tree=default]: ✔" in result.output, "Both tree are documented"
    assert "forbiddenRefs[Tree=translations]: ✔" in result.output, "Both tree are documented"
    assert "duplicateRefs[Tree=translations]: ✔" in result.output, "Both tree are documented"
    assert count_failing(result.return_value.results[get_path("correct_double_tree.xml")]) == 0, "Zero failing test"


def test_duplicate_refs(runner):
    """Test whether duplicate ref finding is working"""
    result = runner.invoke(cli, ['--no-catalog', get_path("duplicate.xml")], standalone_mode=False)
    assert '✗' in result.output, "File has a failing test"
    assert 'duplicateRefs[Tree=default]' in result.output, "Tree Default has duplicate reff"
    assert "`1`" in result.output, "Level 1 reference `1` is duplicated"
    assert "`1.2`" in result.output, "Level 2 reference `1.2` is duplicated within the first 1"
    assert "`1.3`" in result.output, "Level 2 reference `1.3` is duplicated across both 1"
    assert "`1.1`" not in result.output, "Level 2 reference `1.1` is not duplicated across both 1"
    assert count_failing(result.return_value.results[get_path("duplicate.xml")]) == 1, "Only one failing test"


def test_forbidden_ref(runner):
    """Test with a file expected to fail on forbidden refs."""
    result = runner.invoke(cli, ['--no-catalog', get_path("forbid.xml")], standalone_mode=False)
    assert '✗' in result.output, "File has a failing test"
    assert 'forbiddenRefs[Tree=default]' in result.output, "Tree Default has forbidden references"
    assert count_failing(result.return_value.results[get_path("forbid.xml")]) == 1, "Only one failing test"
