from pathlib import Path
from unittest.mock import patch
import filecmp

from click.testing import CliRunner

from robotidy.cli import cli


def save_tmp_model(self, model):
    path = Path('actual', Path(model.source).name)
    model.save(output=path)


def run_tidy(transformer_name, sources, *args):
    runner = CliRunner()
    arguments = [*args]
    paths = [str(Path('source', source)) for source in sources]
    cmd = ['--transform', transformer_name] + arguments + paths
    return runner.invoke(cli, cmd)


def compare_file(actual_name, expected_name=None):
    if expected_name is None:
        expected_name = actual_name
    expected = Path('expected', expected_name)
    actual = Path('actual', actual_name)
    if not filecmp.cmp(expected, actual):
        raise AssertionError(f'File {actual_name} is not same as expected')


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestDiscardEmptySections:
    def test_removes_empty_sections(self):
        result = run_tidy('DiscardEmptySections', sources=['removes_empty_sections.robot'])
        assert result.exit_code == 0
        compare_file('removes_empty_sections.robot')

    def test_removes_empty_sections_except_comments(self):
        result = run_tidy('DiscardEmptySections:allow_only_comments=True', sources=['removes_empty_sections.robot'])
        assert result.exit_code == 0
        # we're using the same actual name (since we used the same source) but different expected
        # that's because our expected changed with modified transformation configuration
        compare_file('removes_empty_sections.robot', 'removes_empty_sections_except_comments.robot')
