from pathlib import Path
from unittest.mock import Mock

import pytest
from robot.api import get_model

from robotidy.disablers import DisabledLines, RegisterDisablers, Skip
from robotidy.utils import ROBOT_VERSION


@pytest.mark.parametrize(
    "check_start, check_end, start_line, end_line, lines, full_match, expected",
    [
        # only start/end line and no full_match
        (15, 30, 15, None, [], False, True),
        (15, 30, 15, 30, [], False, False),
        (14, 30, 15, 30, [], False, True),
        (15, 31, 15, 30, [], False, True),
        (15, 30, None, 30, [], False, False),
        (15, 30, None, None, [], False, False),
        (15, 30, 32, 50, [], False, True),
        # only start/end line and full_match
        (15, 30, 15, None, [], True, False),
        (15, 30, 15, 30, [], True, False),
        (14, 30, 15, 30, [], True, False),
        (15, 31, 15, 30, [], True, False),
        (15, 30, None, 30, [], True, False),
        (15, 30, None, None, [], True, False),
        (15, 30, 32, 50, [], True, True),
        # with lines (# robotidy: off)
        (2, 5, None, None, [(2, 5), (10, 15)], False, True),
        (2, 5, None, None, [(2, 6), (10, 15)], False, True),
        (2, 5, None, None, [(1, 5), (10, 15)], False, True),
        (2, 5, None, None, [(3, 4), (10, 15)], False, True),
        (2, 5, None, None, [(10, 15)], False, False),
        (2, 5, 1, 6, [(2, 5), (10, 15)], False, True),
        (2, 5, 1, 6, [(10, 15)], False, False),
    ],
)
def test_is_node_disabled(check_start, check_end, start_line, end_line, lines, full_match, expected):
    disablers = DisabledLines(start_line, end_line, 99)
    disablers.parse_global_disablers()
    for start, end in lines:
        disablers.add_disabler(start, end)
    node = Mock()
    node.lineno = check_start
    node.end_lineno = check_end
    assert disablers.is_node_disabled(node, full_match=full_match) == expected


@pytest.mark.parametrize(
    "test_file, expected_lines, file_disabled, rf_version",
    [
        ("file_disabled.robot", [(14, 15)], True, 4),
        ("test.robot", [(13, 14), (25, 37), (30, 33), (40, 41), (46, 48), (57, 58), (67, 67)], False, 5),
        ("open_disabler_in_section.robot", [(5, 8), (13, 15), (20, 23)], False, 4),
        ("empty.robot", [], False, 4),
    ],
)
def test_register_disablers(test_file, expected_lines, file_disabled, rf_version):
    if ROBOT_VERSION.major < rf_version:
        pytest.skip(f"Test enabled only for RF {rf_version}.*")
    test_file_path = Path(__file__).parent / "testdata" / "disablers" / test_file
    model = get_model(test_file_path)
    register_disablers = RegisterDisablers(None, None)
    register_disablers.visit(model)
    assert register_disablers.disablers.lines == expected_lines
    assert register_disablers.file_disabled == file_disabled


class TestSkip:
    @pytest.mark.parametrize("keyword_call, str_keyword_call", [(["test", "keyword"], "test,keyword"), (None, "")])
    @pytest.mark.parametrize("return_values, str_return_values", [(True, "True"), (False, "False")])
    @pytest.mark.parametrize("doc, str_doc", [(True, "True"), (False, "False")])
    def test_from_str_cfg(self, doc, str_doc, return_values, str_return_values, keyword_call, str_keyword_call):
        skip_from_str = Skip.from_str_config(
            documentation=str_doc, return_values=str_return_values, keyword_call=str_keyword_call
        )
        skip = Skip(documentation=doc, return_values=return_values, keyword_call=keyword_call)
        assert skip_from_str == skip

    @pytest.mark.parametrize(
        "skip_config, names, disabled",
        [
            ("executejavascript", ["Execute Javascript"], [True]),
            ("executejavascript", ["OtherLib.Execute Javascript"], [False]),
            ("executejavascript", ["Keyword"], [False]),
            ("Execute_Javascript", ["Keyword", "Execute_Javas cript"], [False, True]),
            ("executejavascript", [None], [False]),
            (None, ["Execute Javascript"], [False]),
            (
                "executejavascript,otherkeyword",
                ["Execute Javascript", "Test Keyword", "Other_keyword"],
                [True, False, True],
            ),
        ],
    )
    def test_skip_keyword_call(self, skip_config, names, disabled):
        mock_node = Mock()
        skip = Skip.from_str_config(keyword_call=skip_config)
        for name, disable in zip(names, disabled):
            mock_node.keyword = name
            assert disable == skip.keyword_call(mock_node)

    @pytest.mark.parametrize(
        "skip_config, names, disabled",
        [
            ("executejavascript", ["Execute Javascript"], [True]),
            ("Execute Javascript", ["executejavascript"], [True]),
            ("executejavascript", ["Keyword"], [False]),
            ("Execute", ["Execute Javascript"], [True]),
            ("Execute1", ["Execute Javascript"], [False]),
            ("Execute", ["Execute Javascript", "Execute Other Stuff", "Keyword"], [True, True, False]),
            (
                "Library.",
                ["Library.Stuff", "Library2.Stuff", "library.Other_stuff", "library"],
                [True, False, True, False],
            ),
            (None, ["Execute Javascript"], [False]),
            ("executejavascript", [None], [False]),
        ],
    )
    def test_skip_keyword_call_starts_with(self, skip_config, names, disabled):
        mock_node = Mock()
        skip = Skip.from_str_config(keyword_call_starts_with=skip_config)
        for name, disable in zip(names, disabled):
            mock_node.keyword = name
            assert disable == skip.keyword_call(mock_node)

    @pytest.mark.parametrize(
        "skip_config, names, disabled",
        [
            ("java", ["Java", "javascript", "script"], [True, True, False]),
            ("javascript", ["java", "javascript", "Execute Javascript"], [False, True, True]),
            (
                "Library.",
                ["Library.Stuff", "Library2.Stuff", "library.Other_stuff", "library"],
                [True, False, True, False],
            ),
            (None, ["Keyword"], [False]),
            ("Keyword", [None], [False]),
        ],
    )
    def test_skip_keyword_call_contains(self, skip_config, names, disabled):
        mock_node = Mock()
        skip = Skip.from_str_config(keyword_call_contains=skip_config)
        for name, disable in zip(names, disabled):
            mock_node.keyword = name
            assert disable == skip.keyword_call(mock_node)
