from pathlib import Path
from typing import List, Optional

from typer.testing import CliRunner

from robotidy.cli_typer import cli_app


def run_tidy(
    args: List[str] = None,
    exit_code: int = 0,
    output: Optional[str] = None,
    std_in: Optional = None,
    overwrite_input: bool = False,
):
    runner = CliRunner(mix_stderr=False)
    arguments = args if args is not None else []
    if not overwrite_input:
        if output:
            output_path = str(Path(Path(__file__).parent, "actual", output))
        else:
            output_path = str(Path(Path(__file__).parent, "actual", "tmp"))
        arguments = ["--output", output_path] + arguments
    result = runner.invoke(cli_app, arguments, input=std_in)
    if result.exit_code != exit_code:
        print(result.output)
        raise AssertionError(f"robotidy exit code: {result.exit_code} does not match expected: {exit_code}")
    return result
