from .. import run_tidy_and_compare


class TestSmartSortKeywords:
    TRANSFORMER_NAME = 'SmartSortKeywords'

    def test_ci_sort(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='sort_input.robot',
            expected='sort_ci.robot',
            config=":ignore_other_underscore=False"
        )

    def test_ci_ilu(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='sort_input.robot',
            expected='sort_ci_ilu.robot',
            config=":ignore_leading_underscore=True:ignore_other_underscore=False"
        )

    def test_ci_iou(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='sort_input.robot',
            expected='sort_ci_iou.robot'
        )

    def test_ci_ilu_iou(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='sort_input.robot',
            expected='sort_ci_ilu_iou.robot',
            config=":ignore_leading_underscore=True"
        )

    def test_ilu_iou(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='sort_input.robot',
            expected='sort_ilu_iou.robot',
            config=":case_insensitive=False:ignore_leading_underscore=True"
        )

    def test_iou(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='sort_input.robot',
            expected='sort_iou.robot',
            config=":case_insensitive=False"
        )

    def test_ilu(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='sort_input.robot',
            expected='sort_ilu.robot',
            config=":case_insensitive=False:ignore_leading_underscore=True:ignore_other_underscore=False"
        )

    def test_(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='sort_input.robot',
            expected='sort_.robot',
            config=":case_insensitive=False:ignore_other_underscore=False"
        )

    def test_empty_section(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='empty_before_fist_keyword.robot')

    def test_multiple_sections(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='multiple_sections.robot')
