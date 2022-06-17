from .. import TransformerAcceptanceTest


class TestSplitTooLongLine(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "SplitTooLongLine"

    def test_split_too_long_lines(self):
        self.compare(
            source="tests.robot",
            expected="feed_until_line_length.robot",
            config=":line_length=80:split_on_every_arg=False -s 4",
            target_version=5,
        )

    def test_split_too_long_lines_4(self):
        self.compare(
            source="tests.robot",
            expected="feed_until_line_length_4.robot",
            config=":line_length=80:split_on_every_arg=False -s 4",
            target_version=4,
        )

    def test_split_too_long_lines_split_on_every_arg(self):
        self.compare(
            source="tests.robot", expected="split_on_every_arg.robot", config=":line_length=80 -s 4", target_version=5
        )

    def test_split_too_long_lines_split_on_every_arg_4(self):
        self.compare(
            source="tests.robot", expected="split_on_every_arg_4.robot", config=":line_length=80 -s 4", target_version=4
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
        self.compare(source="disablers.robot", config=":line_length=80", not_modified=True, target_version=5)

    def test_continuation_indent(self):
        self.compare(
            source="continuation_indent.robot",
            expected="continuation_indent_feed.robot",
            config=":line_length=80:split_on_every_arg=False -s 2 --continuation-indent 4 --indent 2",
            target_version=5,
        )
        self.compare(
            source="continuation_indent.robot",
            expected="continuation_indent_split.robot",
            config=":line_length=80:split_on_every_arg=True -s 2 --continuation-indent 4 --indent 2",
            target_version=5,
        )
