import pytest

@pytest.fixture(scope="module")
def dummy_from_conftest():
    return 2
