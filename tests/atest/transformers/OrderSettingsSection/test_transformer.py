import pytest

from tests.atest import TransformerAcceptanceTest


class TestOrderSettingsSection(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "OrderSettingsSection"

    def test_order(self):
        self.compare(source="test.robot")

    def test_missing_group(self):
        self.compare(source="missing_group.robot")

    def test_just_comment(self):
        self.compare(source="just_comment.robot", not_modified=True)

    def test_last_section(self):
        self.compare(source="last_section.robot")

    def test_parsing_error(self):
        self.compare(source="parsing_error.robot")

    @pytest.mark.parametrize("lines", [0, 2])
    def test_lines_between_groups(self, lines):
        self.compare(
            source="test.robot",
            expected=f"test_{lines}_newline.robot",
            config=f":new_lines_between_groups={lines}",
        )

    def test_empty_group_order(self):
        self.compare(source="test.robot", expected="test_empty_group_order.robot", config=":group_order=")

    def test_custom_group_order(self):
        self.compare(
            source="test.robot",
            expected="test_group_order.robot",
            config=":group_order=tags,documentation,imports,settings",
        )

    def test_custom_group_order_import_ordered(self):
        self.compare(
            source="test.robot",
            expected="test_group_order_import_ordered.robot",
            config=":group_order=tags,documentation,imports,settings:imports_order=library,resource,variables",
        )

    def test_missing_group_from_param(self):
        self.compare(
            source="test.robot",
            expected="test_missing_group_from_param.robot",
            config=":group_order=documentation,imports,settings",
        )

    def test_invalid_group(self):
        result = self.run_tidy(
            args=f"--transform {self.TRANSFORMER_NAME}:group_order=invalid,imports,settings".split(),
            source="test.robot",
            exit_code=1,
        )
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'group_order' parameter value: 'invalid,imports,settings'. "
            "Custom order should be provided in comma separated list with valid group names:\n"
            "('documentation', 'imports', 'settings', 'tags')\n"
        )
        assert expected_output in result.output

    def test_custom_order_inside_group(self):
        self.compare(
            source="test.robot",
            expected="test_resource_metadata_first.robot",
            config=":documentation_order=metadata,documentation:imports_order=resource,library,variables",
        )

    def test_invalid_token_name_in_order(self):
        result = self.run_tidy(
            args=f"--transform {self.TRANSFORMER_NAME}:documentation_order=invalid,metadata".split(),
            source="test.robot",
            exit_code=1,
        )
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'order' parameter value: 'invalid,metadata'. "
            f"Custom order should be provided in comma separated list with valid group names:\n"
            f"['documentation', 'metadata']\n"
        )
        assert expected_output in result.output

    def test_remote_library_as_external(self):
        self.compare(source="remote_library.robot", config=":imports_order=library,resource,variables")

    def test_disablers(self):
        self.compare(source="disablers.robot", not_modified=True)

    def test_test_tags(self):
        self.compare(source="test_tags.robot", target_version=">=6")
