from .. import TransformerAcceptanceTest


class TestSplitTooLongLine(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "SplitTooLongLine"

    def test_split_too_long_lines(self):
        self.compare(
            source="tests.robot",
            expected="feed_until_line_length.robot",
            config=":line_length=80:split_on_every_arg=False -s 4",
            target_version=">=5",
        )

    def test_split_too_long_lines_4(self):
        self.compare(
            source="tests.robot",
            expected="feed_until_line_length_4.robot",
            config=":line_length=80:split_on_every_arg=False -s 4",
            target_version="==4",
        )

    def test_split_too_long_lines_split_on_every_arg(self):
        self.compare(
            source="tests.robot",
            expected="split_on_every_arg.robot",
            config=":line_length=80 -s 4",
            target_version=">=5",
        )

    def test_split_too_long_lines_split_on_every_arg_4(self):
        self.compare(
            source="tests.robot",
            expected="split_on_every_arg_4.robot",
            config=":line_length=80 -s 4",
            target_version="==5",
        )

    def test_split_lines_with_multiple_assignments(self):
        self.compare(
            source="multiple_assignments.robot",
            expected="multiple_assignments_until_line_length.robot",
            config=":line_length=80:split_on_every_arg=False -s 4",
        )

    def test_split_lines_with_multiple_assignments_on_every_arg(self):
        self.compare(
            source="multiple_assignments.robot",
            expected="multiple_assignments_on_every_arg.robot",
            config=":line_length=80 -s 4",
        )

    def test_split_lines_with_multiple_assignments_on_every_arg_120(self):
        self.compare(
            source="multiple_assignments.robot",
            expected="multiple_assignments_on_every_arg_120.robot",
        )

    def test_disablers(self):
        self.compare(source="disablers.robot", config=":line_length=80", not_modified=True, target_version=">=5")

    def test_continuation_indent(self):
        self.compare(
            source="continuation_indent.robot",
            expected="continuation_indent_feed.robot",
            config=":line_length=80:split_on_every_arg=False -s 2 --continuation-indent 4 --indent 2",
            target_version=">=5",
        )
        self.compare(
            source="continuation_indent.robot",
            expected="continuation_indent_split.robot",
            config=":line_length=80:split_on_every_arg=True -s 2 --continuation-indent 4 --indent 2",
            target_version=">=5",
        )

    def test_variables_split(self):
        self.compare(
            source="variables.robot",
            expected="variables_split_on_every_value.robot",
            config=":line_length=80:split_on_every_value=True",
        )

    def test_variables_feed(self):
        self.compare(
            source="variables.robot",
            expected="variables_feed.robot",
            config=":line_length=80:split_on_every_value=False",
        )

    def test_skip_keywords(self):
        self.compare(
            source="tests.robot",
            expected="skip_keywords.robot",
            config=":line_length=80:skip_keyword_call=thisisakeyword:skip_keyword_call_pattern=(i?)sets\sthe\svariable",
            target_version=">=5",
        )

    def test_comments(self):
        self.compare(source="comments.robot", config=":split_on_every_value=False --transform AlignVariablesSection")

    def test_ignore_comments(self):
        self.compare(
            source="comments.robot",
            expected="comments_skip_comments.robot",
            config=":split_on_every_value=False --transform AlignVariablesSection --skip-comments",
        )

    def test_split_settings(self):
        self.compare(
            source="settings.robot", expected="settings_on_every_arg.robot", config=":split_on_every_setting_arg=True"
        )

    def test_split_settings_feed_until_line_length(self):
        self.compare(
            source="settings.robot",
            expected="settings_until_line_length.robot",
            config=":split_on_every_setting_arg=False",
        )

    def test_split_settings_feed_until_line_length_skip_comments(self):
        self.compare(
            source="settings.robot",
            expected="settings_until_line_length_skip_comments.robot",
            config=":split_on_every_setting_arg=False:skip_comments=True",
        )
