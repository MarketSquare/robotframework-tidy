import pytest

from .. import run_tidy_and_compare, run_tidy


class TestOrderSettingsSection:
    TRANSFORMER_NAME = 'OrderSettingsSection'

    def test_order(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='test.robot')

    def test_missing_group(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='missing_group.robot')

    def test_just_comment(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='just_comment.robot')

    def test_last_section(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='last_section.robot')

    def test_parsing_error(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='parsing_error.robot')

    @pytest.mark.parametrize('lines', [
        0,
        2
    ])
    def test_lines_between_groups(self, lines):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected=f'test_{lines}_newline.robot',
            config=f':new_lines_between_groups={lines}'
        )

    def test_empty_group_order(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='test_empty_group_order.robot',
            config=':group_order='
        )

    def test_custom_group_order(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='test_group_order.robot',
            config=':group_order=tags,documentation,imports,settings'
        )

    def test_custom_group_order_import_ordered(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='test_group_order_import_ordered.robot',
            config=':group_order=tags,documentation,imports,settings:imports_order=library,resource,variables'
        )

    def test_missing_group_from_param(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='test_missing_group_from_param.robot',
            config=':group_order=documentation,imports,settings'
        )

    def test_invalid_group(self):
        result = run_tidy(
            self.TRANSFORMER_NAME,
            args=f'--transform {self.TRANSFORMER_NAME}:group_order=invalid,imports,settings'.split(),
            source='test.robot',
            exit_code=1
        )
        expected_output = f"Importing 'robotidy.transformers.{self.TRANSFORMER_NAME}' failed: " \
                          "Creating instance failed: BadOptionUsage: " \
                          f"Invalid configurable value: 'invalid,imports,settings' for group_order for OrderSettingsSection transformer." \
                          f" Custom order should be provided in comma separated list with valid group names:\n" \
                          f"('documentation', 'imports', 'settings', 'tags')"
        assert expected_output in str(result.exception)

    def test_custom_order_inside_group(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='test_resource_metadata_first.robot',
            config=':documentation_order=metadata,documentation:imports_order=resource,library,variables'
        )

    def test_invalid_token_name_in_order(self):
        result = run_tidy(
            self.TRANSFORMER_NAME,
            args=f'--transform {self.TRANSFORMER_NAME}:documentation_order=invalid,metadata'.split(),
            source='test.robot',
            exit_code=1
        )
        expected_output = f"Importing 'robotidy.transformers.{self.TRANSFORMER_NAME}' failed: " \
                          "Creating instance failed: BadOptionUsage: " \
                          f"Invalid configurable value: 'invalid,metadata' for order for OrderSettingsSection transformer." \
                          f" Custom order should be provided in comma separated list with valid group names:\n" \
                          f"['documentation', 'metadata']"
        assert expected_output in str(result.exception)

    def test_remote_library_as_external(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='remote_library.robot',
            config=':imports_order=library,resource,variables'
        )
