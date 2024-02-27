import pytest

from tests.atest import TransformerAcceptanceTest


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
        self.compare(
            source="comments.robot",
            expected="comments_split_scalar.robot",
            config=":split_on_every_value=False:split_single_value=True --transform AlignVariablesSection",
        )

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

    @pytest.mark.parametrize(
        "skip_config",
        [
            # verify both local and global skip sections
            ":skip_sections={section_names}",
            " --skip-sections={section_names}",
        ],
    )
    def test_skip_sections(self, skip_config):
        skip_variables = skip_config.format(section_names="variables")
        self.compare(source="variables.robot", config=skip_variables, not_modified=True)
        self.compare(source="comments.robot", config=skip_variables, not_modified=True)
        skip_multiple = skip_config.format(section_names="settings,testcases,keywords")
        self.compare(source="settings.robot", config=skip_multiple, not_modified=True)
        skip_partial = skip_config.format(section_names="settings,testcases")
        self.compare(source="settings.robot", expected="settings_skip_tests.robot", config=skip_partial)

    def test_split_on_single_value(self):
        self.compare(
            source="variables.robot",
            expected="variables_split_scalar.robot",
            config=":split_single_value=True:line_length=80",
        )

    def test_align_new_lines_alone(self):
        self.compare(
            source="align_new_line.robot",
            config=":align_new_line=True"
            ":split_on_every_arg=False"
            ":split_on_every_setting_arg=False"
            ":line_length=51",
        )

    def test_align_new_lines(self):
        self.compare(
            source="align_new_line.robot",
            expected="align_new_line_all.robot",
            config=f"-c {self.TRANSFORMER_NAME}"
            ":align_new_line=True"
            ":split_on_every_arg=False"
            ":split_on_every_setting_arg=False"
            ":line_length=51 "
            "-c NormalizeSeparators:align_new_line=True "
            "-c NormalizeTags:enabled=False "
            "-c OrderTags:enabled=False",
            run_all=True,
        )

    def test_var_syntax(self):
        self.compare(source="VAR_syntax.robot", target_version=">=7")
