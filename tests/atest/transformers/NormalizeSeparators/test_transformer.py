import pytest

from tests.atest import TransformerAcceptanceTest


class TestNormalizeSeparators(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "NormalizeSeparators"

    def test_normalize_separators(self):
        self.compare(source="test.robot")

    def test_normalize_with_8_spaces(self):
        self.compare(source="test.robot", expected="test_8spaces.robot", config=" --spacecount 8")

    def test_pipes(self):
        self.compare(source="pipes.robot")

    @pytest.mark.parametrize(
        "skip_sections",
        ["all", "testcases,keywords", "settings,variables,testcases", ""],
    )
    def test_disable_section(self, skip_sections):
        if skip_sections == "all":
            self.compare(
                source="test.robot",
                not_modified=True,
                config=f":skip_sections=settings,variables,testcases,keywords,comments",
            )
        elif not skip_sections:
            self.compare(source="test.robot", expected="skip_none.robot")
        else:
            self.compare(
                source="test.robot",
                expected=skip_sections.replace(",", "_") + ".robot",
                config=f":skip_sections={skip_sections}",
            )

    def test_rf5_syntax(self):
        self.compare(source="rf5_syntax.robot", target_version=">=5")

    def test_disablers(self):
        self.compare(source="disablers.robot", not_modified=True)

    def test_skip_documentation_default(self):
        self.compare(source="test.robot", config=":skip_documentation=False")

    def test_skip_documentation(self):
        self.compare(source="test.robot", expected="skip_documentation.robot", config=":skip_documentation=True")

    def test_continuation_indent(self):
        self.compare(source="continuation_indent.robot", config=" --continuation-indent 4 --indent 4 --spacecount 2")

    @pytest.mark.parametrize("indent", [2, 4])
    @pytest.mark.parametrize("spaces", [2, 4])
    def test_inline_if(self, spaces, indent):
        not_modified = indent == 4 and spaces == 4
        self.compare(
            source="inline_if.robot",
            expected=f"inline_if_{indent}indent_{spaces}spaces.robot",
            config=f" --spacecount {spaces} --indent {indent}",
            not_modified=not_modified,
            target_version=">=5",
        )

    def test_skip_keyword_call(self):
        self.compare(
            source="test.robot",
            expected="test_skip_keyword.robot",
            config=":skip_keyword_call_pattern=(?i)should\sbe\sequal",
        )

    def test_file_with_pipes_bug390(self):
        self.compare(source="bug390.robot")

    @pytest.mark.parametrize(
        "config", [":skip_comments=True:skip_block_comments=True", ":skip_comments=True", ":skip_block_comments=True"]
    )
    def test_comments(self, config):
        if "skip_comments" in config:
            expected = "comments_skip_comments.robot"
        else:
            expected = "comments_skip_block_comments.robot"
        self.compare(source="comments.robot", expected=expected, config=config, target_version=">=5")

    def test_flatten_lines(self):
        # self.compare(source="test.robot", config=":flatten_lines=True")
        # self.compare(source="rf5_syntax.robot", config=":flatten_lines=True")
        self.compare(source="continuation_indent.robot", config=":flatten_lines=True")
