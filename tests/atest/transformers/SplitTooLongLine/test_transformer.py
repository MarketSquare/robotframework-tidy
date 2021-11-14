from .. import run_tidy_and_compare


class TestSplitTooLongLine:
    TRANSFORMER_NAME = "SplitTooLongLine"

    def test_split_too_long_lines(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="tests.robot",
            expected="feed_until_line_length.robot",
            config=":line_length=80:split_on_every_arg=False -s 4",
        )

    def test_split_too_long_lines_split_on_every_arg(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="tests.robot",
            expected="split_on_every_arg.robot",
            config=":line_length=80:split_on_every_arg=True -s 4",
        )

    def test_split_lines_with_multiple_assignments(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="multiple_assignments.robot",
            expected="multiple_assignments_until_line_length.robot",
            config=":line_length=80:split_on_every_arg=False -s 4",
        )

    def test_split_lines_with_multiple_assignments_on_every_arg(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="multiple_assignments.robot",
            expected="multiple_assignments_on_every_arg.robot",
            config=":line_length=80:split_on_every_arg=True -s 4",
        )
