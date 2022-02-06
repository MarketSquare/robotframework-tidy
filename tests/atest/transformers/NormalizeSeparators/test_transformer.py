import pytest

from .. import run_tidy_and_compare, run_tidy


class TestNormalizeSeparators:
    TRANSFORMER_NAME = "NormalizeSeparators"

    def test_normalize_separators(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="test.robot")

    def test_normalize_with_8_spaces(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME, source="test.robot", expected="test_8spaces.robot", config=" --spacecount 8"
        )

    def test_pipes(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="pipes.robot")

    @pytest.mark.parametrize(
        "sections",
        ["", "comments,settings,variables", "comment,keywords", "comments,settings,variable,keywords,testcases"],
    )
    def test_disable_section(self, sections):
        expected = "empty_sections.robot" if not sections else sections.replace(",", "_") + ".robot"
        run_tidy_and_compare(
            self.TRANSFORMER_NAME, source="test.robot", expected=expected, config=f":sections={sections}"
        )

    def test_configure_invalid_section(self):
        result = run_tidy(
            self.TRANSFORMER_NAME,
            args=f"--transform {self.TRANSFORMER_NAME}:sections=settings,invalid".split(),
            source="test.robot",
            exit_code=1,
        )
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'sections' parameter value: 'settings,invalid'. "
            f"Sections to be transformed should be provided in comma separated list with valid section names:\n"
            f"['comments', 'keywords', 'settings', 'testcases', 'variables']\n"
        )
        assert expected_output == result.output
