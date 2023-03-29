import functools
import shutil
from pathlib import Path
from typing import List, Tuple

import pytest
from click.testing import CliRunner

from robotidy.cli import cli
from robotidy.transformers import TransformConfigMap, load_transformers
from robotidy.utils import ROBOT_VERSION

RERUN_NEEDED_4 = {
    "RenameKeywords": {"run_keywords": 2, "disablers": 2},
    "ReplaceReturns": {"replace_returns_disablers": 2, "return_from_keyword_if": 2},
}
# Transformer_name: {"name of test file from atest": "reruns until stable"}
RERUN_NEEDED = {
    "AddMissingEnd": {"test": 2},
    "AlignKeywordsSection": {"blocks_rf5": 2, "non_ascii_spaces": 2},
    "AlignSettingsSection": {"blank_line_doc": 2, "multiline_keywords": 2},
    "AlignTemplatedTestCases": {"with_settings": 2},
    "AlignTestCasesSection": {
        "blocks_rf5": 2,
        "compact_overflow_bug": 2,
        "dynamic_compact_overflow": 2,
        "dynamic_compact_overflow_limit_1": 2,
        "non_ascii_spaces": 2,
        "skip_keywords": 2,
        "overflow_first_line": 2,
        "skip_return_values_overflow": 2,
    },
    "IndentNestedKeywords": {"run_keyword": 2},
    "InlineIf": {
        "invalid_if": 2,
        "invalid_inline_if": 3,
        "test": 2,
        "test_disablers": 2,
    },
    "MergeAndOrderSections": {"disablers": 3, "parsing_error": 2, "translated": 2, "tests": 3},
    "NormalizeNewLines": {"tests": 2, "multiline": 2},
    "NormalizeSeparators": {"continuation_indent": 2, "test": 2, "disablers": 2, "pipes": 2},
    "NormalizeSettingName": {"disablers": 2, "translated": 2, "tests": 2},
    "NormalizeTags": {"disablers": 2, "duplicates": 2, "tests": 2, "preserve_format": 2},
    "OrderSettings": {"test": 2, "translated": 2},
    "OrderSettingsSection": {"test": 2},
    "OrderTags": {"tests": 2},
    "RemoveEmptySettings": {"empty": 2, "disablers": 2, "overwritten": 2},
    "RenameKeywords": {"disablers": 2},
    "ReplaceBreakContinue": {"test": 2},
    "ReplaceReturns": {
        "replace_returns_disablers": 2,
        "return_from_keyword": 2,
        "test": 2,
        "return_from_keyword_if": 2,
    },
    "ReplaceRunKeywordIf": {
        "configure_whitespace": 2,
        "disablers": 3,
        "set_variable_workaround": 2,
        "tests": 2,
        "keyword_name_in_var": 2,
    },
    "SmartSortKeywords": {"multiple_sections": 2, "sort_input": 2},
    "SplitTooLongLine": {"continuation_indent": 2, "disablers": 2, "tests": 2, "comments": 2, "settings": 2},
    "Translate": {"pl_language_header": 2},
}
SKIP_TESTS_4 = {"ReplaceReturns": {"test"}}
SKIP_TESTS = {"ReplaceRunKeywordIf": {"invalid_data"}, "SplitTooLongLine": {"variables"}}


def run_tidy(cmd, enable_disabled: bool):
    if enable_disabled:
        cmd = get_enable_disabled_config() + cmd
    runner = CliRunner()
    return runner.invoke(cli, cmd)


def run_with_source(source: Path, enable_disabled: bool, reruns: int):
    cmd = ["--reruns", str(reruns), str(source)]
    result = run_tidy(cmd, enable_disabled)
    if result.exit_code != 0:
        raise AssertionError(f"Run failed for {source}")


def run_with_source_and_check(source: Path, orig: Path, enable_disabled: bool):
    cmd = ["--diff", "--check", "--overwrite", str(source)]
    result = run_tidy(cmd, enable_disabled)
    if result.exit_code != 0:
        print(result.output)
        raise AssertionError(f"The code was modified for {orig}")


@functools.lru_cache(1)
def get_enable_disabled_config() -> List[str]:
    """Returns config required to enable all disabled transformers."""

    def is_transformer_disabled(transformer):
        return not getattr(transformer, "ENABLED", True)

    transformers = load_transformers(
        TransformConfigMap([], [], []),
        allow_disabled=True,
        target_version=ROBOT_VERSION.major,
        allow_version_mismatch=False,
    )
    config = []
    for transformer in transformers:
        if not is_transformer_disabled(transformer.instance):
            continue
        config.extend(["--configure", f"{transformer.name}:enabled=True"])
    return config


def is_e2e_only(path: Path) -> bool:
    return path.parent.parent.name == "e2e"


def get_test_attributes_from_path(path: Path) -> Tuple[str, str]:
    transformer = path.parent.parent.name
    test_name = path.stem
    return transformer, test_name


def should_be_skip(path: Path) -> bool:
    """
    Checks if test file is in list of invalid data that cannot pass stability checks.
    """
    if is_e2e_only(path):
        return False
    transformer, test_name = get_test_attributes_from_path(path)
    if ROBOT_VERSION.major == 4 and transformer in SKIP_TESTS_4:
        return test_name in SKIP_TESTS_4[transformer]
    if transformer not in SKIP_TESTS:
        return False
    return test_name in SKIP_TESTS[transformer]


def reruns_needed(path: Path) -> int:
    """
    Check if test data requires extra rerun.
    An example would be for example missing END, which is added in the first run,
    newly created blocks fixed in the second and third run should not modify code.
    Returns number of reruns needed.
    """
    if is_e2e_only(path):
        return 1
    transformer, test_name = get_test_attributes_from_path(path)
    if ROBOT_VERSION.major == 4 and transformer in RERUN_NEEDED_4:
        return RERUN_NEEDED_4[transformer].get(test_name, 1)
    if transformer in RERUN_NEEDED:
        return RERUN_NEEDED[transformer].get(test_name, 1)
    return 1


def gen_test_data():
    """
    Yields list of test data paths. Paths are:
      - *.robot files inside e2e/test_data directory
      - *.robot files inside atest/*/source directories
    """
    e2e_dir = Path(__file__).parent
    atest_dir = e2e_dir.parent / "atest" / "transformers"

    yield from e2e_dir.rglob("test_data/*.robot")
    for path in atest_dir.rglob("*/source/*.robot"):
        yield path


def get_test_id_from_path(path) -> str:
    """Generate test id from path to the source file."""
    test_name = path.stem
    if path.parent.parent.name == "e2e":
        return f"e2e_{test_name}"
    transformer = path.parent.parent.name
    return f"{transformer}_{test_name}"


@pytest.mark.e2e
@pytest.mark.parametrize("test_file", gen_test_data(), ids=get_test_id_from_path)
@pytest.mark.parametrize("enable_disabled", [False, True], ids=["defaults", "all"])
def test_stability_of_transformation(tmpdir, test_file, enable_disabled):
    if should_be_skip(test_file):
        pytest.skip("Skip invalid test data")
    reruns = reruns_needed(test_file)
    # copy test data to temp directory
    test_data_dst = tmpdir / test_file.name
    shutil.copy(test_file, test_data_dst)
    run_with_source(test_data_dst, enable_disabled, reruns)
    for _ in range(2):
        # rerun with --check twice to confirm stability
        run_with_source_and_check(test_data_dst, test_file, enable_disabled)
