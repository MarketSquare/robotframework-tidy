import pytest


def pytest_addoption(parser):
    parser.addoption("--e2e", action="store_true", default=False, help="Run end to end tests")


def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark tests as end to end tests")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--e2e"):
        return
    skip_e2e = pytest.mark.skip(reason="Need --e2e option to run")
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_e2e)
