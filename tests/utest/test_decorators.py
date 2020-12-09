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

    def test_configurable_with_default(self):
        @transformer
        class TestingTransformer:
            @configurable(default=15)
            def some_value(self, value):
                return value + 2
        transform = TestingTransformer()
        assert getattr(transform, 'some_value', 0) == 15

    def test_configurable_with_default_and_init(self):
        """First the value is set to 15 directly. Then in `__init__` some_value(10) is called which returns 10 + 2. """
        @transformer
        class TestingTransformer:
            def __init__(self):
                self.some_value = 10

            @configurable(default=15)
            def some_value(self, value):
                return value + 2
        transform = TestingTransformer()
        assert getattr(transform, 'some_value', 0) == 12

    def test_configurable_override(self):
        """ Any default value should be overriden by direct assigment
        (it should call some_value(5) which returns 5+2) """
        @transformer
        class TestingTransformer:
            def __init__(self):
                self.some_value = 10

            @configurable(default=15)
            def some_value(self, value):
                return value + 2
        transform = TestingTransformer()
        transform.some_value = 5
        assert getattr(transform, 'some_value', 0) == 7
