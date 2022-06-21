import re
from unittest.mock import Mock

import pytest

from robotidy.disablers import Skip, SkipConfig


class TestSkip:
    @pytest.mark.parametrize("keyword_call, str_keyword_call", [(["test", "keyword"], "test,keyword"), (None, "")])
    @pytest.mark.parametrize("return_values, str_return_values", [(True, "True"), (False, "False")])
    @pytest.mark.parametrize("doc, str_doc", [(True, "True"), (False, "False")])
    def test_from_str_cfg(self, doc, str_doc, return_values, str_return_values, keyword_call, str_keyword_call):
        skip_from_str = SkipConfig.from_str_config(  # TODO other tests for global_skip overrides
            global_skip=SkipConfig(),
            documentation=str_doc,
            return_values=str_return_values,
            keyword_call=str_keyword_call,
        )
        skip = SkipConfig(documentation=doc, return_values=return_values, keyword_call=keyword_call)
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
        skip_config = SkipConfig.from_str_config(global_skip=SkipConfig(), keyword_call=skip_config)
        skip = Skip(skip_config=skip_config)
        for name, disable in zip(names, disabled):
            mock_node.keyword = name
            assert disable == skip.keyword_call(mock_node)

    @pytest.mark.parametrize(
        "skip_config, names, disabled",
        [
            ("Execute Javascript", ["Execute Javascript"], [True]),
            ("Execute Javascript", ["executejavascript"], [False]),
            ("(?i)execute\s?javascript", ["Execute Javascript"], [True]),
            ("executejavascript", ["Keyword"], [False]),
            ("Javascript", ["Execute Javascript"], [True]),
            ("^Javascript", ["Execute Javascript"], [False]),
            ("Execute", ["Execute Javascript"], [True]),
            ("Execute1", ["Execute Javascript"], [False]),
            ("Execute", ["Execute Javascript", "Execute Other Stuff", "Keyword"], [True, True, False]),
            (
                "(?i)Library\.",
                ["Library.Stuff", "Library2.Stuff", "library.Other_stuff", "library"],
                [True, False, True, False],
            ),
            ("(?i)execute,javascript", ["Execute", "Quasadilla", "Javascript"], [True, False, False]),
            (None, ["Execute Javascript"], [False]),
            ("executejavascript", [None], [False]),
        ],
    )
    def test_skip_keyword_call_pattern(self, skip_config, names, disabled):
        mock_node = Mock()
        skip_config = SkipConfig.from_str_config(global_skip=SkipConfig(), keyword_call_pattern=skip_config)
        skip = Skip(skip_config=skip_config)
        for name, disable in zip(names, disabled):
            mock_node.keyword = name
            assert disable == skip.keyword_call(mock_node)

    def test_keyword_call_pattern_invalid(self):
        invalid_regex = "[0-9]++"
        skip_config = SkipConfig(keyword_call_pattern=[invalid_regex])
        msg_error = re.escape(f"'{invalid_regex}' is not a valid regular expression.")
        with pytest.raises(ValueError, match=msg_error):
            Skip(skip_config=skip_config)

    def test_global_local_skip_documentation(self):
        # local overrides global
        global_config = SkipConfig(documentation=False)
        local_config = SkipConfig.from_str_config(global_skip=global_config, documentation="True")
        assert local_config.documentation

    def test_global_local_keyword_call(self):
        # list are joined
        global_config = SkipConfig(keyword_call=["name", "name2"])
        local_config = SkipConfig.from_str_config(global_skip=global_config, keyword_call="name,name3")
        assert local_config.keyword_call == ["name", "name3", "name", "name2"]

    def test_only_global_return_values(self):
        # global takes precedence
        global_config = SkipConfig(return_values=True)
        local_config = SkipConfig.from_str_config(global_skip=global_config)
        assert local_config.return_values
