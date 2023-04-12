from tests.atest import TransformerAcceptanceTest


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

    def test_disablers(self):
        self.compare(source="disablers.robot", not_modified=True)

    def test_translated(self):
        self.compare(source="translated.robot", target_version=">=6")

    def test_rf6_syntax(self):
        self.compare(source="rf6.robot", target_version=">=6")
