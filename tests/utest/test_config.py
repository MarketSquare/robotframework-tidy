import pytest

from robotidy.config import FormattingConfig


@pytest.mark.parametrize(
    "configure, expected",
    [
        ([4, None, None], [4, 4, 4]),
        ([8, None, None], [8, 8, 8]),
        ([4, 8, None], [4, 8, 4]),
        ([2, 4, None], [2, 4, 2]),
        ([2, None, 4], [2, 2, 4]),
        ([4, None, 2], [4, 4, 2]),
    ],
)
def test_spacecount_and_indents(configure, expected):
    spacecount, indent, cont_indent = configure
    exp_spacecount, exp_indent, exp_cont_indent = expected
    formatting = FormattingConfig(
        space_count=spacecount,
        indent=indent,
        continuation_indent=cont_indent,
        line_sep="native",
        start_line=None,
        end_line=None,
        separator="space",
        line_length=120,
    )
    assert formatting.separator == exp_spacecount * " "
    assert formatting.indent == exp_indent * " "
    assert formatting.continuation_indent == exp_cont_indent * " "
