from pathlib import Path
from typing import List

from click.testing import CliRunner

from robotidy.cli import cli


def save_tmp_model(self, model):
    """ Decorator that disables default robotidy save to file mechanism and replace with mocked one.
    That way we can save output to 'actual' directory for easy comparison with expected files.  """
    path = Path(Path(__file__).parent, 'actual', Path(model.source).name)
    print(path)
    model.save(output=path)


def run_tidy(args: List[str] = None, exit_code: int = 0):
    runner = CliRunner()
    arguments = args if args is not None else []
    result = runner.invoke(cli, arguments)
    if result.exit_code != exit_code:
        print(result.output)
        raise AssertionError(f'robotidy exit code: {result.exit_code} does not match expected: {exit_code}')
    return result
