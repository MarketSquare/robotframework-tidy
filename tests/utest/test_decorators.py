import pytest

from robotidy.decorators import transformer


class TestDecorators:
    def test_transform_decorator(self):
        @transformer()
        class TestingTransformer:
            pass

        class NotATransfomer:
            pass

        assert getattr(TestingTransformer, 'is_transformer', False)
        assert not hasattr(NotATransfomer, 'is_transformer')
