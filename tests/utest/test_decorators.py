import pytest

from robotidy.decorators import transformer, configurable


class TestDecorators:
    def test_transform_decorator(self):
        @transformer()
        class TestingTransformer:
            pass

        class NotATransfomer:
            pass

        assert getattr(TestingTransformer, 'is_transformer', False)
        assert not hasattr(NotATransfomer, 'is_transformer')

    def test_configurable_init(self):
        @transformer
        class TestingTransformer:
            def __init__(self):
                self.some_value = 10

            @configurable
            def some_value(self, value):
                return value + 2
        transform = TestingTransformer()
        assert getattr(transform, 'some_value', 0) == 12

    def test_configurable_override(self):
        @transformer
        class TestingTransformer:
            def __init__(self):
                self.some_value = 10

            @configurable
            def some_value(self, value):
                return value + 2
        transform = TestingTransformer()
        transform.some_value = 5
        assert getattr(transform, 'some_value', 0) == 7
