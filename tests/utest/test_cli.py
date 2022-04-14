import os
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
from click import FileError, NoSuchOption

from robotidy.cli import read_config, validate_regex
from robotidy.files import find_project_root, read_pyproject_config, get_paths, DEFAULT_EXCLUDES
from robotidy.transformers import load_transformers
from robotidy.transformers.AlignSettingsSection import AlignSettingsSection
from robotidy.transformers.ReplaceRunKeywordIf import ReplaceRunKeywordIf
from robotidy.transformers.SmartSortKeywords import SmartSortKeywords
from robotidy.version import __version__
from .utils import run_tidy


@pytest.fixture(scope="session")
def test_data_dir():
    return Path(__file__).parent / "testdata"


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
    def test_configure_not_existing_transformer(self, name, similar):
        expected_output = (
            f"Error: Configuring transformer '{name}' failed. " f"Verify if correct name was provided.{similar}\n"
        )
        args = f"--configure {name}:param=value -".split()
        result = run_tidy(args, exit_code=1)
        assert expected_output == result.output

    def test_transformer_order(self):
        order_1 = ["NormalizeSeparators", "OrderSettings"]
        order_2 = ["OrderSettings", "NormalizeSeparators"]
        transformers_1 = load_transformers([(transf, []) for transf in order_1], {})
        transformers_2 = load_transformers([(transf, []) for transf in order_2], {})
        assert all(t1.__class__.__name__ == t2.__class__.__name__ for t1, t2 in zip(transformers_1, transformers_2))

    def test_transformer_force_order(self):
        # default_order = ['NormalizeSeparators', 'OrderSettings']
        custom_order = ["OrderSettings", "NormalizeSeparators"]
        transformers = load_transformers([(transf, []) for transf in custom_order], {}, force_order=True)
        assert all(t1.__class__.__name__ == t2 for t1, t2 in zip(transformers, custom_order))

    def test_not_existing_configurable_similar(self):
        expected_output = (
            "Error: DiscardEmptySections: Failed to import. "
            "Verify if correct name or configuration was provided. Did you mean:\n"
            "    allow_only_comments\n"
        )

        args = "--transform DiscardEmptySections:allow_only_commentss=True -".split()
        result = run_tidy(args, exit_code=1)
        assert result.output == expected_output

    def test_not_existing_configurable(self):
        expected_output = (
            "Error: DiscardEmptySections: Failed to import. "
            "Verify if correct name or configuration was provided. "
            "This transformer accepts following arguments: allow_only_comments\n"
        )

        args = "--transform DiscardEmptySections:invalid=True -".split()
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

    def test_transform_without_args(self):
        expected_output = (
            "Error: AddMissingEnd: Failed to import. "
            "Verify if correct name or configuration was provided. "
            "This transformer does not accept arguments but they were provided.\n"
        )
        args = "--transform AddMissingEnd:made_up=value -".split()
        result = run_tidy(args, exit_code=1)
        assert result.output == expected_output

    def test_find_project_root_from_src(self, test_data_dir):
        src = test_data_dir / "nested" / "test.robot"
        path = find_project_root((src,))
        assert path == test_data_dir / "nested"

    def test_read_robotidy_config(self, test_data_dir):
        """robotidy.toml follows the same format as pyproject starting from 1.2.0"""
        expected_config = {
            "overwrite": False,
            "diff": False,
            "spacecount": 4,
            "transform": ["DiscardEmptySections:allow_only_comments=True", "ReplaceRunKeywordIf"],
        }
        config_path = str(test_data_dir / "config" / "robotidy.toml")
        config = read_pyproject_config(config_path)
        assert config == expected_config

    def test_read_pyproject_config(self, test_data_dir):
        expected_parsed_config = {
            "overwrite": False,
            "diff": False,
            "startline": 10,
            "endline": 20,
            "transform": ["DiscardEmptySections:allow_only_comments=True", "SplitTooLongLine"],
            "configure": [
                "DiscardEmptySections:allow_only_comments=False",
                "OrderSettings: keyword_before = documentation,tags,timeout,arguments",
            ],
        }
        config_path = str(test_data_dir / "only_pyproject" / "pyproject.toml")
        config = read_pyproject_config(config_path)
        assert config == expected_parsed_config

    def test_read_pyproject_config_e2e(self, test_data_dir):
        expected_parsed_config = {
            "overwrite": "False",
            "diff": "False",
            "startline": "10",
            "endline": "20",
            "transform": ["DiscardEmptySections:allow_only_comments=True", "SplitTooLongLine"],
            "configure": [
                "DiscardEmptySections:allow_only_comments=False",
                "OrderSettings: keyword_before = documentation,tags,timeout,arguments",
            ],
        }
        config_path = str(test_data_dir / "only_pyproject")
        ctx_mock = MagicMock()
        ctx_mock.params = {"src": (config_path,)}
        ctx_mock.command.params = None
        param_mock = Mock()
        read_config(ctx_mock, param_mock, value=None)
        assert ctx_mock.default_map == expected_parsed_config

    def test_read_invalid_config(self, test_data_dir):
        config_path = str(test_data_dir / "invalid_pyproject" / "pyproject.toml")
        with pytest.raises(FileError) as err:
            read_pyproject_config(config_path)
        assert "Error reading configuration file: " in str(err)

    @pytest.mark.parametrize("option, correct", [("confgure", "configure"), ("idontexist", None)])
    def test_read_invalid_option_config(self, option, correct, test_data_dir):
        config_path = str(test_data_dir / "invalid_options_config" / f"pyproject_{option}.toml")
        ctx_mock = MagicMock()
        param_mock = MagicMock()
        with pytest.raises(NoSuchOption) as err:
            read_config(ctx_mock, param_mock, config_path)
        similar = "" if correct is None else f" Did you mean {correct}"
        assert f"no such option: {option}{similar}"

    def test_read_config_from_param(self, test_data_dir):
        expected_parsed_config = {
            "overwrite": "False",
            "diff": "False",
            "spacecount": "4",
            "transform": ["DiscardEmptySections:allow_only_comments=True", "ReplaceRunKeywordIf"],
        }
        config_path = str(test_data_dir / "config" / "robotidy.toml")
        ctx_mock = MagicMock()
        ctx_mock.command.params = None
        param_mock = Mock()
        read_config(ctx_mock, param_mock, config_path)
        assert ctx_mock.default_map == expected_parsed_config

    def test_read_config_without_param(self, test_data_dir):
        expected_parsed_config = {
            "overwrite": "False",
            "diff": "False",
            "spacecount": "4",
            "transform": ["DiscardEmptySections:allow_only_comments=True", "ReplaceRunKeywordIf"],
        }
        config_path = str(test_data_dir / "config" / "robotidy.toml")
        ctx_mock = MagicMock()
        ctx_mock.params = {"src": (config_path,)}
        ctx_mock.command.params = None
        param_mock = Mock()
        read_config(ctx_mock, param_mock, value=None)
        assert ctx_mock.default_map == expected_parsed_config

    @pytest.mark.parametrize("flag", ["--list", "-l"])
    def test_list_transformers(self, flag):
        result = run_tidy([flag])
        assert (
            "To see detailed docs run --desc <transformer_name> or --desc all. Transformers with (disabled) "
            "tag \nare executed only when selected explicitly with --transform or configured with param "
            "`enabled=True`.\n"
            "Available transformers:\n" in result.output
        )
        assert "ReplaceRunKeywordIf\n" in result.output
        assert "SmartSortKeywords (disabled)\n" in result.output  # this transformer is disabled by default
        assert "Available transformers:\n\nAddMissingEnd\n" in result.output  # assert order

    @pytest.mark.parametrize("flag", ["--desc", "-d"])
    @pytest.mark.parametrize(
        "name, expected_doc",
        [
            ("ReplaceRunKeywordIf", ReplaceRunKeywordIf.__doc__.replace("::", ":").replace("``", "'")),
            ("SmartSortKeywords", SmartSortKeywords.__doc__.replace("::", ":").replace("``", "'")),
        ],
    )
    def test_describe_transformer(self, flag, name, expected_doc):
        not_expected_doc = AlignSettingsSection.__doc__.replace("::", ":").replace("``", "'")
        result = run_tidy([flag, name])
        assert expected_doc in result.output
        assert not_expected_doc not in result.output

    def test_describe_transformer_all(self):
        expected_doc = ReplaceRunKeywordIf.__doc__.replace("::", ":").replace("``", "'")
        expected_doc2 = AlignSettingsSection.__doc__.replace("::", ":").replace("``", "'")
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
        assert expected_output in str(result.output)

    @pytest.mark.parametrize("flag", ["--help", "-h"])
    def test_help(self, flag):
        result = run_tidy([flag])
        assert f"Version: {__version__}" in result.output

    @pytest.mark.parametrize("source, return_status", [("golden.robot", 0), ("not_golden.robot", 1)])
    def test_check(self, source, return_status, test_data_dir):
        source = test_data_dir / "check" / source
        with patch("robotidy.app.ModelWriter") as mock_writer:
            run_tidy(
                ["--check", "--transform", "NormalizeSectionHeaderName", str(source)],
                exit_code=return_status,
            )
            mock_writer.assert_not_called()

    @pytest.mark.parametrize("source, return_status", [("golden.robot", 0), ("not_golden.robot", 1)])
    def test_check_overwrite(self, source, return_status, test_data_dir):
        source = test_data_dir / "check" / source
        with patch("robotidy.app.ModelWriter") as mock_writer:
            run_tidy(
                ["--check", "--overwrite", "--transform", "NormalizeSectionHeaderName", str(source)],
                exit_code=return_status,
            )
            if return_status:
                mock_writer.assert_called()
            else:
                mock_writer.assert_not_called()

    def test_diff(self, test_data_dir):
        source = test_data_dir / "check" / "not_golden.robot"
        result = run_tidy(["--diff", "--no-overwrite", "--transform", "NormalizeSectionHeaderName", str(source)])
        assert "*** settings ***" in result.output
        assert "*** Settings ***" in result.output

    def test_disabled_transformer(self):
        transformers = load_transformers(None, {})
        assert all(transformer.__class__.__name__ != "SmartSortKeywords" for transformer in transformers)

    def test_enable_disable_transformer(self):
        transformers = load_transformers([("SmartSortKeywords", [])], {})
        assert transformers[0].__class__.__name__ == "SmartSortKeywords"

    def test_configure_transformer(self):
        transformers = load_transformers(None, {"AlignVariablesSection": ["up_to_column=4"]})
        transformers_not_configured = load_transformers(None, {})
        assert len(transformers) == len(transformers_not_configured)
        for transformer in transformers:
            if transformer.__class__.__name__ == "AlignVariablesSection":
                assert transformer.up_to_column + 1 == 4

    def test_configure_transformer_overwrite(self):
        transformers = load_transformers(
            [("AlignVariablesSection", ["up_to_column=3"])], {"AlignVariablesSection": ["up_to_column=4"]}
        )
        assert transformers[0].up_to_column + 1 == 4

    @pytest.mark.parametrize("line_sep", ["unix", "windows", "native", None])
    def test_line_sep(self, line_sep, test_data_dir):
        source = test_data_dir / "line_sep" / "test.robot"
        expected = test_data_dir / "line_sep" / "expected.robot"
        actual = test_data_dir.parent / "actual" / "test.robot"
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

    @pytest.mark.parametrize("force_order", [True, False])
    @pytest.mark.parametrize("allow_disabled", [True, False])
    @pytest.mark.parametrize(
        "transformers, configure, present, test_for",
        [
            # robotidy .
            (None, {}, True, "AlignVariablesSection"),
            # robotidy -c AlignVariablesSection:enabled=True .
            (None, {"AlignVariablesSection": ["enabled=True"]}, True, "AlignVariablesSection"),
            # robotidy -c AlignVariablesSection:enabled=false .
            (None, {"AlignVariablesSection": ["enabled=false"]}, False, "AlignVariablesSection"),
            # robotidy -c SmartSortKeywords:enabled=True .
            (None, {"SmartSortKeywords": ["enabled=True"]}, True, "SmartSortKeywords"),  # disabled by default
            # robotidy -c SmartSortKeywords:enabled=False .
            (None, {"SmartSortKeywords": ["enabled=False"]}, False, "SmartSortKeywords"),
            # robotidy --transform SmartSortKeywords:enabled=True .
            ([("SmartSortKeywords", ["enabled=True"])], {}, True, "SmartSortKeywords"),
            # robotidy --transform NormalizeAssignments .
            ([("NormalizeAssignments", [])], {}, False, "AlignVariablesSection"),
            # robotidy --transform NormalizeAssignments --transform AlignVariablesSection .
            ([("NormalizeAssignments", []), ("AlignVariablesSection", [])], {}, True, "AlignVariablesSection"),
            # robotidy --transform NormalizeAssignments --transform AlignVariablesSection:up_to_column=4 .
            (
                [("NormalizeAssignments", []), ("AlignVariablesSection", ["up_to_column=4"])],
                {},
                True,
                "AlignVariablesSection",
            ),
            # robotidy --transform NormalizeAssignments --transform AlignVariablesSection:up_to_column=4:enabled=True .
            (
                [("NormalizeAssignments", []), ("AlignVariablesSection", ["up_to_column=4", "enabled=True"])],
                {},
                True,
                "AlignVariablesSection",
            ),
            # robotidy --transform NormalizeAssignments --transform AlignVariablesSection:up_to_column=4:enabled=False .
            (
                [("NormalizeAssignments", []), ("AlignVariablesSection", ["up_to_column=4", "enabled=False"])],
                {},
                False,
                "AlignVariablesSection",
            ),
            # robotidy --transform NormalizeAssignments --transform AlignVariablesSection:up_to_column=4 -c
            # AlignVariablesSection:enabled=True .
            (
                [("NormalizeAssignments", []), ("AlignVariablesSection", ["up_to_column=4"])],
                {"AlignVariablesSection": ["enabled=True"]},
                True,
                "AlignVariablesSection",
            ),
            # robotidy --transform NormalizeAssignments --transform AlignVariablesSection:up_to_column=4 -c
            # AlignVariablesSection:enabled=False .
            (
                [("NormalizeAssignments", []), ("AlignVariablesSection", ["up_to_column=4"])],
                {"AlignVariablesSection": ["enabled=False"]},
                False,
                "AlignVariablesSection",
            ),
        ],
    )
    def test_disable_transformers(self, transformers, configure, present, force_order, allow_disabled, test_for):
        if force_order and not transformers:
            present = False
        loaded_transformers = load_transformers(
            transformers, configure, allow_disabled=allow_disabled, force_order=force_order
        )
        if present:
            assert any(transformer.__class__.__name__ == test_for for transformer in loaded_transformers)
        else:
            assert all(transformer.__class__.__name__ != test_for for transformer in loaded_transformers)

    @pytest.mark.parametrize(
        "exclude, extend_exclude, allowed",
        [
            (DEFAULT_EXCLUDES, None, ["nested/test.robot", "test.resource", "test.robot"]),
            ("test.resource", None, ["test.robot", "nested/test.robot"]),
            (DEFAULT_EXCLUDES, "test.resource", ["test.robot", "nested/test.robot"]),
            ("test.resource", "nested/*", ["test.robot"]),
        ],
    )
    def test_exclude_gitignore(self, exclude, extend_exclude, allowed, test_data_dir):
        source = test_data_dir / "gitignore"
        allowed_paths = {Path(source, path) for path in allowed}
        paths = get_paths(
            (str(source),), exclude=validate_regex(exclude), extend_exclude=validate_regex(extend_exclude)
        )
        assert paths == allowed_paths

    @pytest.mark.parametrize(
        "source, should_parse",
        [
            (None, ["test.robot", "resources/test.robot"]),  # calls: robotidy
            ("test3.robot", ["test3.robot"]),  # calls: robotidy test3.robot
            ("test.robot", ["test.robot"]),
            (".", ["test.robot", "test3.robot", "resources/test.robot"]),
        ],
    )
    def test_src_in_configuration(self, source, should_parse, test_data_dir):
        source_dir = test_data_dir / "pyproject_with_src"
        os.chdir(source_dir)
        if source is not None:
            source = source_dir / source
            result = run_tidy([str(source)])
        else:
            result = run_tidy()
        expected = [f"Loaded configuration from {source_dir / 'pyproject.toml'}"]
        for file in should_parse:
            path = source_dir / file
            expected.append(f"Transforming {path} file")
        actual = sorted(line for line in result.output.split("\n") if line.strip())
        assert actual == sorted(expected)

    @pytest.mark.parametrize("source", [1, 2])
    def test_empty_configuration(self, source, test_data_dir):
        config_dir = test_data_dir / f"empty_pyproject{source}"
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
