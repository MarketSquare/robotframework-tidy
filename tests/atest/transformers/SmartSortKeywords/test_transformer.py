from tests.atest import TransformerAcceptanceTest


class TestSmartSortKeywords(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "SmartSortKeywords"

    def test_ci_sort(self):
        self.compare(
            source="sort_input.robot",
            expected="sort_ci.robot",
            config=":ignore_other_underscore=False",
        )

    def test_ci_ilu(self):
        self.compare(
            source="sort_input.robot",
            expected="sort_ci_ilu.robot",
            config=":ignore_leading_underscore=True:ignore_other_underscore=False",
        )

    def test_ci_iou(self):
        self.compare(source="sort_input.robot", expected="sort_ci_iou.robot")

    def test_ci_ilu_iou(self):
        self.compare(
            source="sort_input.robot",
            expected="sort_ci_ilu_iou.robot",
            config=":ignore_leading_underscore=True",
        )

    def test_ilu_iou(self):
        self.compare(
            source="sort_input.robot",
            expected="sort_ilu_iou.robot",
            config=":case_insensitive=False:ignore_leading_underscore=True",
        )

    def test_iou(self):
        self.compare(
            source="sort_input.robot",
            expected="sort_iou.robot",
            config=":case_insensitive=False",
        )

    def test_ilu(self):
        self.compare(
            source="sort_input.robot",
            expected="sort_ilu.robot",
            config=":case_insensitive=False:ignore_leading_underscore=True:ignore_other_underscore=False",
        )

    def test_(self):
        self.compare(
            source="sort_input.robot",
            expected="sort_.robot",
            config=":case_insensitive=False:ignore_other_underscore=False",
        )

    def test_empty_section(self):
        self.compare(source="empty_before_fist_keyword.robot", not_modified=True)

    def test_multiple_sections(self):
        self.compare(source="multiple_sections.robot")

    def test_disablers(self):
        self.compare(source="disablers.robot", not_modified=True)
