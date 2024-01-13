import pytest


@pytest.fixture
def network_connection():
    net_connect = network_manager()
    yield net_connect