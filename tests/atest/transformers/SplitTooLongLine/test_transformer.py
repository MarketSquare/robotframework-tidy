from .. import TransformerAcceptanceTest


class TestSplitTooLongLine(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "SplitTooLongLine"

    def test_split_too_long_lines(self):
        self.compare(
            source="tests.robot",
            expected="feed_until_line_length.robot",
            config=":line_length=80:split_on_every_arg=False -s 4",
        )

    def test_split_too_long_lines_split_on_every_arg(self):
        self.compare(
            source="tests.robot",
            expected="split_on_every_arg.robot",
            config=":line_length=80 -s 4",
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
