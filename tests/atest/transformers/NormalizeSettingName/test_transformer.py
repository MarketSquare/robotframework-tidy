from .. import TransformerAcceptanceTest


class TestNormalizeSettingName(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "NormalizeSettingName"

    def test_normalize_setting_name(self):
        self.compare(source="tests.robot")

    def test_normalize_setting_name_selected(self):
        self.compare(
            source="tests.robot",
            expected="selected.robot",
            config=" --startline 12 --endline 15",
        )
