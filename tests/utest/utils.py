from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from robotidy.cli import cli


def run_tidy(
    args: list[str] = None,
    exit_code: int = 0,
    output: str | None = None,
    std_in: str | None = None,
    overwrite_input: bool = False,
):
    runner = CliRunner(mix_stderr=False)
    arguments = args if args is not None else []
    if not overwrite_input:
        if output:
            output_path = str(Path(Path(__file__).parent, "actual", output))
        else:
            output_path = str(Path(Path(__file__).parent, "actual", "tmp"))
        arguments = ["--output", output_path, *arguments]
    result = runner.invoke(cli, arguments, input=std_in)
    if result.exit_code != exit_code:
        print(result.output)
        raise AssertionError(f"robotidy exit code: {result.exit_code} does not match expected: {exit_code}")
    return result
