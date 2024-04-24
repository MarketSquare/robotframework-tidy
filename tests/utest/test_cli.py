import os
import shutil
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import pytest
from click import FileError, NoSuchOption
from click.shell_completion import ShellComplete

from robotidy import skip
from robotidy.config import RawConfig
from robotidy.files import DEFAULT_EXCLUDES, find_project_root, get_paths, load_toml_file, read_pyproject_config
from robotidy.transformers.aligners_core import AlignKeywordsTestsSection
from robotidy.transformers.AlignSettingsSection import AlignSettingsSection
from robotidy.utils import misc

from .utils import run_tidy

TEST_DATA_DIR = Path(__file__).parent / "testdata"


@pytest.fixture
def temporary_cwd(tmpdir):
    prev_cwd = Path.cwd()
    os.chdir(tmpdir)
    try:
        yield Path(tmpdir)
    finally:
        os.chdir(prev_cwd)


@contextmanager
def switch_cwd(new_cwd):
    prev_cwd = Path.cwd()
    os.chdir(new_cwd)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


class TestCli:
    @pytest.mark.parametrize(
        "name, similar",
        [
            ("NotExisting", ""),
            ("AlignSettings", " Did you mean:\n    AlignSettingsSection"),
            ("align", " Did you mean:\n    AlignSettingsSection\n    AlignVariablesSection"),
            ("splittoolongline", " Did you mean:\n    SplitTooLongLine"),
            ("AssignmentNormalizer", " Did you mean:\n    NormalizeAssignments"),
        ],
    )
    def test_transform_not_existing_transformer(self, name, similar):
        expected_output = (
            f"Error: Importing transformer '{name}' failed. "
            f"Verify if correct name or configuration was provided.{similar}\n"
        )
        args = f"--transform {name} --transform MissingTransformer --transform DiscardEmptySections -".split()
        result = run_tidy(args, exit_code=1)
        assert expected_output == result.output

    # Disabled until validate_config_names remains commented out
    # @pytest.mark.parametrize(
    #     "name, similar",
    #     [
    #         ("NotExisting", ""),
    #         ("AlignSettings", " Did you mean:\n    AlignSettingsSection"),
    #         ("align", " Did you mean:\n    AlignSettingsSection\n    AlignVariablesSection"),
    #         ("splittoolongline", " Did you mean:\n    SplitTooLongLine"),
    #         ("AssignmentNormalizer", " Did you mean:\n    NormalizeAssignments"),
    #     ],
    # )
    # def test_configure_not_existing_transformer(self, name, similar):
    #     expected_output = (
    #         f"Error: Configuring transformer '{name}' failed. " f"Verify if correct name was provided.{similar}\n"
    #     )
    #     args = f"--configure {name}:param=value -".split()
    #     result = run_tidy(args, exit_code=1)
    #     assert expected_output == result.output

    @pytest.mark.parametrize("option_name", ["-t", "--transform"])
    def test_not_existing_configurable_similar(self, option_name):
        expected_output = (
            "Error: DiscardEmptySections: Failed to import. "
            "Verify if correct name or configuration was provided. Did you mean:\n"
            "    allow_only_comments\n"
        )

        args = f"{option_name} DiscardEmptySections:allow_only_commentss=True -".split()
        result = run_tidy(args, exit_code=1)
        assert result.output == expected_output

    def test_not_existing_configurable(self):
        expected_output = (
            "Error: DiscardEmptySections: Failed to import. "
            "Verify if correct name or configuration was provided. "
            "This transformer accepts following arguments:\n    enabled\n    allow_only_comments\n    skip_sections\n"
        )

        args = "--transform DiscardEmptySections:invalid=True -".split()
        result = run_tidy(args, exit_code=1)
        assert result.output == expected_output

    def test_not_existing_configurable_skip(self):
        expected_args = [
            "enabled",
            "widths",
            "alignment_type",
            "handle_too_long",
            "compact_overflow_limit",
            "skip_documentation",
        ]
        # skip_documentation is overridden in transformer - the order is different because of that
        expected_args += sorted(AlignKeywordsTestsSection.HANDLES_SKIP - {"skip_documentation"})
        expected_args_str = "\n    ".join(expected_args)
        expected_output = (
            "Error: AlignTestCasesSection: Failed to import. "
            "Verify if correct name or configuration was provided. "
            f"This transformer accepts following arguments:\n    {expected_args_str}\n"
        )
        args = "--transform AlignTestCasesSection:invalid=True -".split()
        result = run_tidy(args, exit_code=1)
        assert result.output == expected_output

    def test_invalid_configurable_usage(self):
        expected_output = (
            "Error: Importing transformer 'DiscardEmptySections=allow_only_comments=False' failed. "
            "Verify if correct name or configuration was provided.\n"
        )
        args = "--transform DiscardEmptySections=allow_only_comments=False -".split()
        result = run_tidy(args, exit_code=1)
        assert result.output == expected_output

    def test_too_many_arguments_for_transform(self):
        expected_output = (
            "Error: DiscardEmptySections: Invalid parameter format. "
            "Pass parameters using MyTransformer:param_name=value syntax.\n"
        )
        args = "--transform DiscardEmptySections:allow_only_comments:False -".split()
        result = run_tidy(args, exit_code=1)
        assert result.output == expected_output

    def test_invalid_argument_type_for_transform(self):
        expected_output = (
            "Error: AlignVariablesSection: Failed to import. "
            "Verify if correct name or configuration was provided. "
            "Argument 'up_to_column' got value '1a' that cannot be converted to integer.\n"
        )
        args = "--transform AlignVariablesSection:up_to_column=1a -".split()
        result = run_tidy(args, exit_code=1)
        assert result.output == expected_output

    def test_find_project_root_from_src(self):
        src = TEST_DATA_DIR / "nested" / "test.robot"
        path = find_project_root((str(src),))
        assert path == TEST_DATA_DIR / "nested"

    def test_ignore_git_dir(self):
        """Test if --ignore-git-dir works when locating pyproject.toml file."""
        src = TEST_DATA_DIR / "with_git_dir" / "project_a"
        (src / ".git").mkdir(exist_ok=True)
        root_with_git = src
        root_without_git = TEST_DATA_DIR / "with_git_dir"
        path = find_project_root((str(src),), ignore_git_dir=False)
        assert path == root_with_git
        path = find_project_root((str(src),), ignore_git_dir=True)
        assert path == root_without_git

    def test_read_robotidy_config(self):
        """robotidy.toml follows the same format as pyproject starting from 1.2.0"""
        expected_config = {
            "overwrite": False,
            "diff": False,
            "spacecount": 4,
            "transform": ["DiscardEmptySections:allow_only_comments=True", "ReplaceRunKeywordIf"],
        }
        config_path = TEST_DATA_DIR / "config" / "robotidy.toml"
        config = read_pyproject_config(config_path)
        assert config == expected_config

    def test_read_pyproject_config(self):
        expected_parsed_config = {
            "overwrite": False,
            "diff": False,
            "continuation_indent": 2,
            "startline": 10,
            "endline": 20,
            "transform": ["DiscardEmptySections:allow_only_comments=True", "SplitTooLongLine"],
            "configure": [
                "DiscardEmptySections:allow_only_comments=False",
                "OrderSettings: keyword_before = documentation,tags,timeout,arguments",
            ],
        }
        config_path = TEST_DATA_DIR / "only_pyproject" / "pyproject.toml"
        config = read_pyproject_config(config_path)
        assert config == expected_parsed_config

    def test_read_invalid_config(self):
        config_path = TEST_DATA_DIR / "invalid_pyproject" / "pyproject.toml"
        with pytest.raises(FileError) as err:
            read_pyproject_config(config_path)
        assert "Error reading configuration file: " in str(err)

    @pytest.mark.parametrize("option, correct", [("confgure", "configure"), ("idontexist", None)])
    def test_read_invalid_option_config(self, option, correct):
        config_path = TEST_DATA_DIR / "invalid_options_config" / f"pyproject_{option}.toml"
        with pytest.raises(NoSuchOption) as err:
            config_file = read_pyproject_config(config_path)
            RawConfig().from_config_file(config_file, config_path)
        assert f"No such option: {option}" in str(err)

    @pytest.mark.parametrize("flag", ["--list", "-l"])
    @pytest.mark.parametrize("target_version", ["4", "5", None])
    def test_list_transformers(self, flag, target_version):
        if target_version and target_version == "5" and misc.ROBOT_VERSION.major < 5:
            pytest.skip("Skip RF 5.0 only tests in previous RF versions")
        cmd = [flag]
        if target_version:
            cmd.extend(["--target-version", f"rf{target_version}"])
        result = run_tidy(cmd)
        assert "Non-default transformers needs to be selected explicitly" in result.output
        assert "ReplaceRunKeywordIf        │ Yes" in result.output
        assert "SmartSortKeywords" in result.output  # this transformer is disabled by default
        if (not target_version and misc.ROBOT_VERSION.major == 5) or target_version and target_version == "5":
            assert "│ ReplaceReturns             │ Yes" in result.output
        elif target_version and target_version == "4":
            assert "│ ReplaceReturns             │ No" in result.output

    @pytest.mark.parametrize("flag", ["--list", "-l"])
    def test_list_transformers_filter_enabled(self, flag):
        # --transform X should only have X in output
        cmd = ["--transform", "RenameKeywords", flag, "enabled"]
        result = run_tidy(cmd)
        assert "RenameKeywords" in result.output
        assert "NormalizeNewLines" not in result.output
        # -c X, where X is disabled by default should have default, X in output but not the rest
        cmd = ["--configure", "RenameKeywords:enabled=True", flag, "enabled"]
        result = run_tidy(cmd)
        assert "RenameKeywords" in result.output
        assert "NormalizeNewLines" in result.output
        assert "SmartSortKeywords" not in result.output

    def test_list_no_config(self, temporary_cwd):
        """Execute Robotidy in temporary directory to ensure it supports running without default configuration file."""
        run_tidy(["--list"])

    def test_list_with_config(self):
        config_dir = TEST_DATA_DIR / "pyproject_with_src"
        with switch_cwd(config_dir):
            result = run_tidy(["--list", "enabled"])
        assert "SplitTooLongLine" in result.output
        assert "NormalizeSeparators" not in result.output

    @pytest.mark.parametrize("flag", ["--list", "-l"])
    def test_list_transformers_filter_disabled(self, flag):
        # --transform X should not have X in output, even if it is default transformer
        cmd = ["--transform", "NormalizeSeparators", flag, "disabled"]
        result = run_tidy(cmd)
        assert "NormalizeSeparators" not in result.output
        assert "NormalizeNewLines" in result.output

    @pytest.mark.parametrize("flag", ["--list", "-l"])
    def test_list_transformers_invalid_filter_value(self, flag):
        cmd = [flag, "RenameKeywords"]
        result = run_tidy(cmd, exit_code=2)
        error = self.normalize_cli_error(result.output)
        assert (
            "Invalid value for '--list' / '-l': Not allowed value. Allowed values are: all, enabled, disabled"
        ) in error

    @pytest.mark.parametrize("flag", ["--desc", "-d"])
    @pytest.mark.parametrize(
        "name, expected_doc",
        [
            ("ReplaceRunKeywordIf", "Run Keywords inside Run Keyword If will be split into separate keywords:"),
            ("SmartSortKeywords", "By default sorting is case insensitive, but"),
        ],
    )
    def test_describe_transformer(self, flag, name, expected_doc):
        not_expected_doc = AlignSettingsSection.__doc__.replace("::", ":").replace("``", "'")
        result = run_tidy([flag, name])
        assert expected_doc in result.output
        assert not_expected_doc not in result.output

    def test_describe_transformer_all(self):
        expected_doc = "Any return value will be applied to every"
        expected_doc2 = "You can configure how many columns should"
        result = run_tidy(["--desc", "all"])
        assert expected_doc in result.output
        assert expected_doc2 in result.output

    @pytest.mark.parametrize(
        "name, similar",
        [
            ("NotExisting", ""),
            ("AlignSettings", " Did you mean:\n    AlignSettingsSection"),
            ("align", " Did you mean:\n    AlignSettingsSection\n    AlignVariablesSection"),
            ("splittoolongline", " Did you mean:\n    SplitTooLongLine"),
            ("AssignmentNormalizer", " Did you mean:\n    NormalizeAssignments"),
        ],
    )
    def test_describe_invalid_transformer(self, name, similar):
        expected_output = f"Transformer with the name '{name}' does not exist.{similar}"
        args = f"--desc {name} -".split()
        result = run_tidy(args, exit_code=1)
        assert expected_output in str(result.stderr)

    @pytest.mark.parametrize("flag", ["--help", "-h"])
    def test_help(self, flag):
        result = run_tidy([flag])
        assert f"Robotidy is a tool for formatting" in result.output

    @pytest.mark.parametrize(
        "source, return_status, expected_output",
        [
            ("golden.robot", 0, "\n0 files would be reformatted, 1 file would be left unchanged.\n"),
            ("not_golden.robot", 1, "\n1 file would be reformatted, 0 files would be left unchanged.\n"),
        ],
    )
    def test_check(self, source, return_status, expected_output):
        source = TEST_DATA_DIR / "check" / source
        if return_status:
            expected_output = f"Would reformat {source}\n{expected_output}"
        with patch("robotidy.utils.misc.ModelWriter") as mock_writer:
            result = run_tidy(
                ["--check", "--transform", "NormalizeSectionHeaderName", str(source)],
                exit_code=return_status,
            )
            mock_writer.assert_not_called()
            assert result.output == expected_output

    @pytest.mark.parametrize(
        "source, return_status, expected_output",
        [
            ("golden.robot", 0, "\n0 files reformatted, 1 file left unchanged.\n"),
            ("not_golden.robot", 1, "\n1 file reformatted, 0 files left unchanged.\n"),
        ],
    )
    def test_check_overwrite(self, source, return_status, expected_output):
        source = TEST_DATA_DIR / "check" / source
        if return_status:
            expected_output = f"Reformatted {source}\n{expected_output}"
        with patch("robotidy.utils.misc.ModelWriter") as mock_writer:
            result = run_tidy(
                ["--check", "--overwrite", "--transform", "NormalizeSectionHeaderName", str(source)],
                exit_code=return_status,
            )
            if return_status:
                mock_writer.assert_called()
            else:
                mock_writer.assert_not_called()
            assert result.output == expected_output

    def test_read_only_file(self):
        source = TEST_DATA_DIR / "read_only" / "test.robot"
        # change file permission to read-only
        source.chmod(0o400)
        # overwrite input which is read-only file
        result = run_tidy([str(source)], overwrite_input=True)
        assert "Permission denied" in result.stderr
        assert "\n0 files reformatted, 0 files left unchanged. 1 file skipped.\n" in result.stdout

    @pytest.mark.parametrize("color_flag", ["--color", "--no-color", None])
    @pytest.mark.parametrize("color_env", [True, False])
    def test_disable_coloring(self, color_flag, color_env):
        should_be_colored = not ((color_flag is not None and color_flag == "--no-color") or color_env)
        mocked_env = {"NO_COLOR": ""} if color_env else {}
        source = TEST_DATA_DIR / "check" / "not_golden.robot"
        command = ["--diff", "--no-overwrite"]
        if color_flag:
            command.append(color_flag)
        command.extend(["--transform", "NormalizeSectionHeaderName", str(source)])
        with patch.dict("os.environ", mocked_env), patch("robotidy.utils.misc.decorate_diff_with_color") as mock_color:
            run_tidy(command)
            if should_be_colored:
                mock_color.assert_called()
            else:
                mock_color.assert_not_called()

    def test_diff(self):
        source = TEST_DATA_DIR / "check" / "not_golden.robot"
        result = run_tidy(["--diff", "--no-overwrite", "--transform", "NormalizeSectionHeaderName", str(source)])
        assert "*** settings ***" in result.output
        assert "*** Settings ***" in result.output

    @pytest.mark.parametrize("line_sep", ["unix", "windows", "native", None])
    def test_line_sep(self, line_sep):
        source = TEST_DATA_DIR / "line_sep" / "test.robot"
        expected = TEST_DATA_DIR / "line_sep" / "expected.robot"
        actual = TEST_DATA_DIR.parent / "actual" / "test.robot"
        if line_sep is not None:
            run_tidy(["--lineseparator", line_sep, str(source)], output="test.robot")
        else:
            run_tidy([str(source)], output="test.robot")
        line_end = {"unix": "\n", "windows": "\r\n", "native": os.linesep, None: os.linesep}[line_sep]
        with open(str(expected)) as f:
            expected_str = f.read()
        expected_str = expected_str.replace("\n", line_end)
        with open(str(actual), newline="") as f:
            actual_str = f.read()
        assert actual_str == expected_str, "Line endings does not match"

    @pytest.mark.parametrize("skip_gitignore", [True, False])
    @pytest.mark.parametrize(
        "exclude, extend_exclude, allowed",
        [
            (DEFAULT_EXCLUDES, None, ["nested/test.robot", "test.resource", "test.robot"]),
            ("test.resource", None, ["test.robot", "nested/test.robot"]),
            (DEFAULT_EXCLUDES, "test.resource", ["test.robot", "nested/test.robot"]),
            ("test.resource", "nested/*", ["test.robot"]),
        ],
    )
    def test_exclude_gitignore(self, exclude, extend_exclude, skip_gitignore, allowed):
        if skip_gitignore:
            allowed = allowed + ["test2.robot"]  # extend will not work due to mutability of list
            if not extend_exclude or "nested" not in extend_exclude:
                allowed = allowed + ["nested/test2.robot"]
        source = TEST_DATA_DIR / "gitignore"
        allowed_paths = {Path(source, path) for path in allowed}
        paths = get_paths(
            (str(source),),
            exclude=misc.validate_regex(exclude),
            extend_exclude=misc.validate_regex(extend_exclude),
            skip_gitignore=skip_gitignore,
        )
        assert paths == allowed_paths

    @pytest.mark.parametrize(
        "source, should_parse, summary",
        [
            (
                None,
                ["test.robot", "resources/test.robot"],
                "0 files reformatted, 2 files left unchanged.",
            ),  # calls: robotidy
            (
                "test3.robot",
                ["test3.robot"],
                "0 files reformatted, 1 file left unchanged.",
            ),  # calls: robotidy test3.robot
            ("test.robot", ["test.robot"], "0 files reformatted, 1 file left unchanged."),
            (
                ".",
                ["test.robot", "test3.robot", "resources/test.robot"],
                "0 files reformatted, 3 files left unchanged.",
            ),
        ],
    )
    def test_src_and_space_in_param_in_configuration(self, source, should_parse, summary):
        source_dir = TEST_DATA_DIR / "pyproject_with_src"
        os.chdir(source_dir)
        if source is not None:
            source = source_dir / source
            result = run_tidy([str(source)])
        else:
            result = run_tidy()
        expected = [f"Loaded configuration from {source_dir / 'pyproject.toml'}", summary]
        for file in should_parse:
            path = source_dir / file
            expected.append(f"Found {path} file")
        actual = sorted(line for line in result.output.split("\n") if line.strip())
        assert actual == sorted(expected)

    @pytest.mark.parametrize("source", [1, 2])
    def test_empty_configuration(self, source):
        config_dir = TEST_DATA_DIR / f"empty_pyproject{source}"
        os.chdir(config_dir)
        result = run_tidy(exit_code=1)
        assert "Loaded configuration from" not in result.output

    def test_loading_from_stdin(self):
        input_file = (
            "*** Settings ***\nLibrary  SomeLib\n\n\n"
            "*** Variables ***\n\n\n\n"
            "*** Keywords ***\nKeyword\n    Keyword1 ${arg}\n"
        )
        expected_output = (
            "*** Settings ***\nLibrary  SomeLib\n\n\n" "*** Keywords ***\nKeyword\n    Keyword1 ${arg}\n\n"
        )
        args = "--transform DiscardEmptySections -".split()
        result = run_tidy(args, std_in=input_file)
        assert result.output == expected_output

    @pytest.mark.parametrize("target_version", ["rf", "abc", "5", "rf3"])
    @patch("robotidy.utils.misc.ROBOT_VERSION")
    def test_invalid_target_version(self, mocked_version, target_version):
        mocked_version.major = 5
        result = run_tidy(f"--target-version {target_version} .".split(), exit_code=2)
        error = self.normalize_cli_error(result.output)
        assert f"Invalid value for '--target-version' / '-tv':" in error

    def normalize_cli_error(self, error):
        error = error.replace("│", "").replace("\n", "")
        error = " ".join(error.split())
        return error

    @patch("robotidy.utils.misc.ROBOT_VERSION")
    @pytest.mark.parametrize("option_name", ["-tv", "--target-version"])
    def test_too_recent_target_version(self, mocked_version, option_name):
        target_version = 5
        mocked_version.major = 4
        result = run_tidy(f"{option_name} rf{target_version} .".split(), exit_code=2)
        error = self.normalize_cli_error(result.output)
        assert (
            "Invalid value for '--target-version' / '-tv': "
            f"Target Robot Framework version ({target_version}) "
            "should not be higher than installed version (" in error
        )

    def test_skip_options(self, tmp_path):
        alternate_names = {"--skip-return-statement": "--skip-return"}
        with_values = {"--skip-keyword-call-pattern", "--skip-keyword-call", "--skip-sections"}
        option_names = []
        for skip_option in skip.SkipConfig.HANDLES:
            option = f"--{skip_option.replace('_', '-')}"
            option = alternate_names.get(option, option)
            option_names.append(option)
            if option in with_values:
                option_names.append("empty")
        run_tidy([*option_names, str(tmp_path)])

    @pytest.mark.parametrize("option_name", ["custom_transformers", "load_transformers"])
    def test_load_custom_transformers_from_config(self, option_name):
        config_path = TEST_DATA_DIR / "config_with_custom_transformers" / f"{option_name}.toml"
        config_file = read_pyproject_config(config_path)
        config = RawConfig().from_config_file(config_file, config_path)
        assert config.custom_transformers[0].name == "CustomTransformer.py"

    @pytest.mark.parametrize("option_name", ["--custom-transformers", "--load-transformers"])
    def test_load_custom_transformers_from_cli(self, option_name, tmp_path):
        custom_transformer = TEST_DATA_DIR / "config_with_custom_transformers" / "CustomTransformer.py"
        run_tidy([option_name, str(custom_transformer), str(tmp_path)])


class TestGenerateConfig:
    def validate_generated_default_configuration(
        self, config_path: Path, diff: bool, add_missing_enabled: bool, rename_variables_enabled: bool
    ):
        assert config_path.is_file()
        config = load_toml_file(config_path)
        configured_transformers = config["tool"]["robotidy"].pop("configure")
        expected_config = {
            "tool": {
                "robotidy": {
                    "diff": diff,
                    "overwrite": True,
                    "verbose": False,
                    "separator": "space",
                    "spacecount": 4,
                    "line_length": 120,
                    "lineseparator": "native",
                    "skip_gitignore": False,
                    "ignore_git_dir": False,
                }
            }
        }
        assert expected_config == config
        assert f"AddMissingEnd:enabled={add_missing_enabled}" in configured_transformers
        assert f"RenameVariables:enabled={rename_variables_enabled}" in configured_transformers

    def test_generate_default_config(self, temporary_cwd):
        config_path = temporary_cwd / "pyproject.toml"
        run_tidy(["--generate-config"])
        self.validate_generated_default_configuration(
            config_path, diff=False, add_missing_enabled=True, rename_variables_enabled=False
        )

    def test_generate_config_ignore_existing_config(self, temporary_cwd):
        config_path = temporary_cwd / "pyproject.toml"
        orig_config_path = TEST_DATA_DIR / "only_pyproject" / "pyproject.toml"
        shutil.copy(orig_config_path, config_path)
        run_tidy(["--generate-config"])
        self.validate_generated_default_configuration(
            config_path, diff=False, add_missing_enabled=True, rename_variables_enabled=False
        )

    def test_generate_config_with_filename(self, temporary_cwd):
        config_path = temporary_cwd / "different.txt"
        run_tidy(["--generate-config", "different.txt"])
        self.validate_generated_default_configuration(
            config_path, diff=False, add_missing_enabled=True, rename_variables_enabled=False
        )

    def test_generate_config_with_cli_config(self, temporary_cwd):
        config_path = temporary_cwd / "pyproject.toml"
        run_tidy(["--generate-config", "--diff", "--transform", "RenameVariables"])
        self.validate_generated_default_configuration(
            config_path, diff=True, add_missing_enabled=False, rename_variables_enabled=True
        )

    def test_missing_dependency(self, monkeypatch, temporary_cwd):
        with patch.dict("sys.modules", {"tomli_w": None}):
            result = run_tidy(["--generate-config"], exit_code=1)
        expected_output = (
            "Error: Missing optional dependency: tomli_w. Install robotidy with extra `generate_config` "
            "profile:\n\npip install robotframework-tidy[generate_config]\n"
        )
        assert result.output == expected_output


# FIXME
# class TestAutoCompletion:
#     def _get_completions(self, cli, args, incomplete):
#         comp = ShellComplete(cli, {}, "robotidy", "_robotidy_COMPLETE")
#         return comp.get_completions(args, incomplete)
#
#     def _get_words(self, cli, args, incomplete):
#         return [c.value for c in self._get_completions(cli, args, incomplete)]
#
#     @pytest.mark.parametrize(
#         "supported_transf_opt, with_params",
#         [
#             ("transform", True),
#             ("configure", True),
#             ("desc", False),
#             ("load-transformers", True),
#             ("custom-transformers", True),
#         ],
#     )
#     def test_autocompletion_for_transformer(self, temporary_cwd, supported_transf_opt, with_params):
#         expected_transformers = [
#             "AlignSettingsSection",
#             "AlignVariablesSection",
#             "AlignTemplatedTestCases",
#             "AlignTestCasesSection",
#             "AlignKeywordsSection",
#         ]
#         # transformer_completions = self._get_words(cli, [f"--{supported_transf_opt}"], "Align")
#         # assert expected_transformers == transformer_completions
#         transformer_completions = self._get_words(cli, [f"--{supported_transf_opt}"], "ReplaceVar")
#         if with_params:
#             align_settings_params = [
#                 "enabled=True",
#                 "up_to_column=2",
#                 "argument_indent=4",
#                 "min_width=",
#                 "fixed_width=",
#                 "skip_documentation=",
#             ]
#             param_completions = self._get_words(cli, [f"--{supported_transf_opt}"], "AlignSettingsSection:")
#             assert param_completions == align_settings_params
