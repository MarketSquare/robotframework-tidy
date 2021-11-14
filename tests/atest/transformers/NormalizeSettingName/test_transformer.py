from .. import run_tidy_and_compare


class TestNormalizeSettingName:
    TRANSFORMER_NAME = "NormalizeSettingName"

    def test_normalize_setting_name(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="tests.robot")

    def test_normalize_setting_name_selected(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="tests.robot",
            expected="selected.robot",
            config=" --startline 12 --endline 15",
        )
