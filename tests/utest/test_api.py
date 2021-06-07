from pathlib import Path

from robot.api import get_model

from robotidy.api import transform_model


class TestAPI:
    def test_load_pyproject_and_transform(self):
        expected = "*** Settings ***\n" \
                   "\n\n" \
                   "*** Test Cases ***\n" \
                   "Test\n" \
                   "    [Documentation]  doc\n" \
                   "    [Tags]  sometag\n" \
                   "    Pass\n" \
                   "    Keyword\n" \
                   "    One More\n" \
                   "\n\n" \
                   "*** Comments ***\n" \
                   "robocop: disable=all"
        config_path = str(Path(Path(__file__).parent, 'testdata', 'only_pyproject'))
        source = str(Path(Path(__file__).parent.parent, 'atest', 'transformers', 'DiscardEmptySections', 'source',
                          'removes_empty_sections.robot'))
        model = get_model(source)
        transformed = transform_model(model, config_path)
        assert transformed == expected

    def test_with_default_parameters(self):
        expected = "*** Comments ***\n" \
                   "robocop: disable=all\n" \
                   "\n" \
                   "*** Test Cases ***\n" \
                   "Test\n" \
                   "        [Documentation]        doc\n" \
                   "        [Tags]        sometag\n" \
                   "        Pass\n" \
                   "        Keyword\n" \
                   "        One More\n"

        config_path = '.'
        source = str(Path(Path(__file__).parent.parent, 'atest', 'transformers', 'DiscardEmptySections', 'source',
                          'removes_empty_sections.robot'))
        model = get_model(source)
        transformed = transform_model(model, config_path, spacecount=8, linestart=10, endline=20)
        assert transformed == expected
